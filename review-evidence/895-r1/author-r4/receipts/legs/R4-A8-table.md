### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 137 paths and 7 of 994 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.187 (0.505) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 0.169 (0.486) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.089 (0.328) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 0.080 (0.319) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.085 (0.465) | fits | 0 adp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 0.163 (0.465) | fits | 1 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.076 (0.443) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 0.150 (0.443) | fits | 1 adp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.096 (0.334) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 0.101 (0.341) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.081 (0.315) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 0.082 (0.323) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.090 (0.327) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 0.094 (0.329) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.089 (0.335) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 0.098 (0.338) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.132 (0.440) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 0.099 (0.404) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.222 (0.771) | fits | 0 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 0.335 (1.645) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.244 (0.885) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 0.360 (0.858) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.120 (0.804) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 0.236 (0.804) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.331 (0.898) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 0.422 (0.898) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.343 (0.845) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 0.220 (0.824) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.342 (0.889) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 0.429 (0.889) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.140 (0.471) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 0.148 (0.491) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.053 (0.292) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.071 (0.292) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.029 (0.274) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.049 (0.274) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.029 (0.549) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 0.211 (0.549) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.032 (0.540) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.199 (0.540) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.256 (0.513) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.232 (0.513) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.151 (0.641) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 0.099 (0.641) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.152 (0.640) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 0.246 (0.744) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.328 (0.822) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 1 | `aecp.get_avb_info.if1` (aecp) | 0.286 (0.790) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.229 (0.727) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 0.171 (0.660) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.195 (0.695) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 1 | `aecp.get_counters.if1` (aecp) | 0.211 (0.712) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.254 (0.754) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 0.273 (0.774) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.417 (0.835) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 0.362 (0.829) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.152 (0.638) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 0.173 (0.675) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.297 (0.805) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 0.298 (0.809) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.187 (0.681) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 0.204 (0.715) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.255 (0.757) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.178 (0.671) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.301 (0.810) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.177 (0.672) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.176 (0.685) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.184 (0.694) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 0.277 (0.781) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.257 (0.760) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.188 (0.683) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.261 (0.765) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.257 (0.762) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.189 (0.683) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.256 (0.758) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.162 (0.661) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 0.250 (0.753) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.440 (0.922) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 0.432 (0.889) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.237 (0.736) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 1 | `aecp.unknown_command.if1` (aecp) | 0.178 (0.669) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.348 (0.773) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 0.445 (0.871) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.733 (1.193) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 0.730 (1.189) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.695 (1.190) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 0.756 (1.242) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.731 (1.190) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 0.727 (1.186) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.710 (1.219) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 0.672 (1.168) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.686 (1.178) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.736 (1.195) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 0.735 (1.194) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 5.029 (5.820) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 4.898 (5.659) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.140 (0.665) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.746 (2.311) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.718 (64.186) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.858 (65.338) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 3.773 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `save-starved.held.adp.if1` (save-starved) | 2.995 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `save-starved.held.aecp.if1` (save-starved) | 3.415 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 2.362 | fits | 6 maap | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 1 | `save-starved.held.maap.if1` (save-starved) | 2.214 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `save-starved.held.srp.if1` (save-starved) | 8.602 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.392 (0.899) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 0.236 (0.749) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.112 (0.323) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 0.113 (0.326) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.167 (0.413) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 0.151 (0.397) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.368 (0.899) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 0.217 (0.749) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.297 (0.793) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 0.303 (0.799) | fits | 0 events | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 3.045 | fits | 0 srp | 6 | 0 |
| an MRPDU its join timer owes, the longest | 1 | `save-starved.mrpdu.periodic.if1` (save-starved) | 3.886 | fits | 0 srp | 4 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.571 | fits | 0 acmp | 76 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.356 | MISS ceiling | 11 acmp | 76 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.615 | fits | 0 adp | 76 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 5.649 | fits | 7 adp | 74 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 5.812 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.150 | fits | 0 aecp | 76 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 61.992 | MISS ceiling | 15 aecp | 76 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.597 | fits | 0 maap | 76 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.maap.last.if0` (backlog-adp@program-aged2-7) | 5.687 | fits | 6 maap | 76 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-7.service.srp.first.if0` (backlog-adp@blank-aged2-7) | 6.993 | fits | 0 srp | 76 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@program-aged2-4.service.srp.last.if1` (backlog-adp@program-aged2-4) | 10.245 | fits | 31 srp | 76 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.902 (0.972) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 0.894 (0.963) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.520 (0.521) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 0.484 (0.485) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.299 (0.300) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 0.289 (0.290) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.896 (0.964) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 0.847 (0.904) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.714 | 10 | 160,758 (1.608) | yes | - |
| backlog-adp@blank-1 | 0 | 10.836 | 7 | 158,642 (1.586) | yes | - |
| backlog-adp@blank-2 | 0 | 11.068 | 8 | 158,782 (1.588) | yes | - |
| backlog-adp@blank-3 | 0 | 11.025 | 8 | 158,752 (1.588) | yes | - |
| backlog-adp@blank-4 | 0 | 11.000 | 8 | 158,782 (1.588) | yes | - |
| backlog-adp@blank-5 | 0 | 12.103 | 10 | 158,816 (1.588) | yes | - |
| backlog-adp@blank-6 | 0 | 11.632 | 10 | 160,570 (1.606) | yes | - |
| backlog-adp@blank-7 | 0 | 12.407 | 9 | 157,948 (1.579) | yes | - |
| backlog-adp@program-0 | 0 | 11.127 | 9 | 158,402 (1.584) | yes | - |
| backlog-adp@program-1 | 0 | 10.870 | 8 | 158,402 (1.584) | yes | - |
| backlog-adp@program-2 | 0 | 11.176 | 9 | 159,856 (1.599) | yes | - |
| backlog-adp@program-3 | 0 | 10.935 | 8 | 157,845 (1.578) | yes | - |
| backlog-adp@program-4 | 0 | 10.467 | 9 | 159,673 (1.597) | yes | - |
| backlog-adp@program-5 | 0 | 10.583 | 10 | 160,641 (1.606) | yes | - |
| backlog-adp@program-6 | 0 | 10.329 | 8 | 159,344 (1.593) | yes | - |
| backlog-adp@program-7 | 0 | 10.279 | 8 | 157,745 (1.577) | yes | - |
| backlog-adp@verify-0 | 0 | 11.656 | 10 | 158,472 (1.585) | yes | - |
| backlog-adp@verify-1 | 0 | 11.013 | 8 | 159,169 (1.592) | yes | - |
| backlog-adp@verify-2 | 0 | 11.000 | 8 | 159,199 (1.592) | yes | - |
| backlog-adp@verify-3 | 0 | 10.959 | 8 | 159,169 (1.592) | yes | - |
| backlog-adp@verify-4 | 0 | 10.946 | 8 | 159,199 (1.592) | yes | - |
| backlog-adp@verify-5 | 0 | 12.048 | 10 | 161,669 (1.617) | yes | - |
| backlog-adp@verify-6 | 0 | 11.566 | 10 | 160,852 (1.609) | yes | - |
| backlog-adp@verify-7 | 0 | 12.361 | 9 | 157,958 (1.580) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 12.082 | 9 | 158,852 (1.589) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 10.651 | 8 | 159,195 (1.592) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 12.038 | 10 | 158,916 (1.589) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 11.292 | 10 | 160,686 (1.607) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 10.914 | 8 | 159,605 (1.596) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 10.963 | 8 | 159,217 (1.592) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 10.995 | 8 | 159,656 (1.597) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 12.541 | 9 | 161,779 (1.618) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 11.190 | 9 | 158,422 (1.584) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 11.001 | 8 | 158,567 (1.586) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 11.003 | 8 | 158,422 (1.584) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 11.872 | 9 | 158,367 (1.584) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 11.333 | 10 | 158,466 (1.585) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 11.190 | 10 | 159,427 (1.594) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 10.791 | 7 | 157,565 (1.576) | yes | - |
| backlog-adp@blank-aged1-7 | 1 | 10.808 | 7 | 159,999 (1.600) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.663 | 11 | 159,456 (1.595) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 11.209 | 9 | 160,381 (1.604) | yes | - |
| backlog-adp@program-aged2-2 | 1 | 10.848 | 7 | 160,328 (1.603) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 11.033 | 8 | 159,219 (1.592) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 11.047 | 8 | 159,326 (1.593) | yes | - |
| backlog-adp@program-aged2-5 | 1 | 10.846 | 7 | 160,523 (1.605) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 10.861 | 8 | 163,916 (1.639) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 12.834 | 11 | 162,361 (1.624) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 11.336 | 8 | 158,372 (1.584) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.843 | 8 | 157,455 (1.575) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 10.881 | 8 | 157,475 (1.575) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 11.514 | 10 | 158,444 (1.584) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 10.866 | 8 | 159,241 (1.592) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 10.919 | 8 | 159,009 (1.590) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 10.946 | 8 | 159,292 (1.593) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 11.784 | 9 | 157,510 (1.575) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 12.311 | 10 | 160,460 (1.605) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 10.746 | 8 | 159,318 (1.593) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 11.026 | 8 | 159,601 (1.596) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 11.014 | 8 | 159,318 (1.593) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 10.786 | 7 | 159,566 (1.596) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 10.832 | 8 | 159,043 (1.590) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 11.014 | 9 | 160,646 (1.606) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 12.615 | 9 | 157,932 (1.579) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 12.464 | 11 | 157,401 (1.574) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 11.213 | 10 | 158,444 (1.584) | yes | - |
| backlog-adp@verify-aged1-2 | 1 | 10.808 | 7 | 158,026 (1.580) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 10.830 | 8 | 158,868 (1.589) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 10.845 | 8 | 159,013 (1.590) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 10.878 | 8 | 158,868 (1.589) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 10.892 | 8 | 161,168 (1.612) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 12.605 | 10 | 162,413 (1.624) | yes | - |
| backlog | 0 | 8.864 | 8 | 162,528 (1.625) | yes | - |
| backlog-adp | 0 | 10.427 | 10 | 160,056 (1.601) | yes | - |
| backlog-adp-refill | 0 | 42.257 | 25 | 159,255 (1.593) | yes | - |
| backlog-owed | 0 | 65.863 | 23 | 162,100 (1.621) | yes | - |

Composed maximum over the 4 backlog windows: 162,528 CPU cycles (1.625 ms), backlog.
Over the windows that released their whole load only: 162,528 (1.625 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 93247 | 0 | 59,415 (0.594) | fits |
| save-held | 2979 | 0 | 166,301 (1.663) | fits |
| save-starved | 44629 | 0 | 166,301 (1.663) | fits |
| acmp-notk | 4646 | 0 | 110,450 (1.105) | fits |
| backlog-adp@blank-0 | 568 | 0 | 160,758 (1.608) | fits |
| backlog-adp@blank-1 | 568 | 0 | 158,642 (1.586) | fits |
| backlog-adp@blank-2 | 568 | 0 | 158,782 (1.588) | fits |
| backlog-adp@blank-3 | 568 | 0 | 158,752 (1.588) | fits |
| backlog-adp@blank-4 | 568 | 0 | 158,782 (1.588) | fits |
| backlog-adp@blank-5 | 570 | 0 | 158,816 (1.588) | fits |
| backlog-adp@blank-6 | 570 | 0 | 160,570 (1.606) | fits |
| backlog-adp@blank-7 | 571 | 0 | 157,948 (1.579) | fits |
| backlog-adp@program-0 | 954 | 0 | 158,402 (1.584) | fits |
| backlog-adp@program-1 | 953 | 0 | 158,402 (1.584) | fits |
| backlog-adp@program-2 | 955 | 0 | 159,856 (1.599) | fits |
| backlog-adp@program-3 | 955 | 0 | 157,845 (1.578) | fits |
| backlog-adp@program-4 | 957 | 0 | 159,673 (1.597) | fits |
| backlog-adp@program-5 | 958 | 0 | 160,641 (1.606) | fits |
| backlog-adp@program-6 | 958 | 0 | 159,344 (1.593) | fits |
| backlog-adp@program-7 | 958 | 0 | 157,745 (1.577) | fits |
| backlog-adp@verify-0 | 1332 | 0 | 158,472 (1.585) | fits |
| backlog-adp@verify-1 | 1332 | 0 | 159,169 (1.592) | fits |
| backlog-adp@verify-2 | 1332 | 0 | 159,199 (1.592) | fits |
| backlog-adp@verify-3 | 1332 | 0 | 159,169 (1.592) | fits |
| backlog-adp@verify-4 | 1332 | 0 | 159,199 (1.592) | fits |
| backlog-adp@verify-5 | 1334 | 0 | 161,669 (1.617) | fits |
| backlog-adp@verify-6 | 1334 | 0 | 160,852 (1.609) | fits |
| backlog-adp@verify-7 | 1335 | 0 | 157,958 (1.580) | fits |
| backlog-adp@blank-aged2-0 | 754 | 0 | 158,852 (1.589) | fits |
| backlog-adp@blank-aged2-1 | 758 | 0 | 159,195 (1.592) | fits |
| backlog-adp@blank-aged2-2 | 765 | 0 | 158,916 (1.589) | fits |
| backlog-adp@blank-aged2-3 | 770 | 0 | 160,686 (1.607) | fits |
| backlog-adp@blank-aged2-4 | 773 | 0 | 159,605 (1.596) | fits |
| backlog-adp@blank-aged2-5 | 778 | 0 | 159,217 (1.592) | fits |
| backlog-adp@blank-aged2-6 | 783 | 0 | 159,656 (1.597) | fits |
| backlog-adp@blank-aged2-7 | 789 | 0 | 161,779 (1.618) | fits |
| backlog-adp@blank-aged1-0 | 715 | 0 | 158,422 (1.584) | fits |
| backlog-adp@blank-aged1-1 | 719 | 0 | 158,567 (1.586) | fits |
| backlog-adp@blank-aged1-2 | 724 | 0 | 158,422 (1.584) | fits |
| backlog-adp@blank-aged1-3 | 730 | 0 | 158,367 (1.584) | fits |
| backlog-adp@blank-aged1-4 | 735 | 0 | 158,466 (1.585) | fits |
| backlog-adp@blank-aged1-5 | 740 | 0 | 159,427 (1.594) | fits |
| backlog-adp@blank-aged1-6 | 743 | 0 | 157,565 (1.576) | fits |
| backlog-adp@blank-aged1-7 | 748 | 0 | 159,999 (1.600) | fits |
| backlog-adp@program-aged2-0 | 1139 | 0 | 159,456 (1.595) | fits |
| backlog-adp@program-aged2-1 | 1142 | 0 | 160,381 (1.604) | fits |
| backlog-adp@program-aged2-2 | 1146 | 0 | 160,328 (1.603) | fits |
| backlog-adp@program-aged2-3 | 1151 | 0 | 159,219 (1.592) | fits |
| backlog-adp@program-aged2-4 | 1156 | 0 | 159,326 (1.593) | fits |
| backlog-adp@program-aged2-5 | 1160 | 0 | 160,523 (1.605) | fits |
| backlog-adp@program-aged2-6 | 1165 | 0 | 163,916 (1.639) | fits |
| backlog-adp@program-aged2-7 | 1173 | 0 | 162,361 (1.624) | fits |
| backlog-adp@program-aged1-0 | 1097 | 0 | 158,372 (1.584) | fits |
| backlog-adp@program-aged1-1 | 1101 | 0 | 157,455 (1.575) | fits |
| backlog-adp@program-aged1-2 | 1106 | 0 | 157,475 (1.575) | fits |
| backlog-adp@program-aged1-3 | 1113 | 0 | 158,444 (1.584) | fits |
| backlog-adp@program-aged1-4 | 1116 | 0 | 159,241 (1.592) | fits |
| backlog-adp@program-aged1-5 | 1121 | 0 | 159,009 (1.590) | fits |
| backlog-adp@program-aged1-6 | 1126 | 0 | 159,292 (1.593) | fits |
| backlog-adp@program-aged1-7 | 1132 | 0 | 157,510 (1.575) | fits |
| backlog-adp@verify-aged2-0 | 1520 | 0 | 160,460 (1.605) | fits |
| backlog-adp@verify-aged2-1 | 1523 | 0 | 159,318 (1.593) | fits |
| backlog-adp@verify-aged2-2 | 1528 | 0 | 159,601 (1.596) | fits |
| backlog-adp@verify-aged2-3 | 1533 | 0 | 159,318 (1.593) | fits |
| backlog-adp@verify-aged2-4 | 1537 | 0 | 159,566 (1.596) | fits |
| backlog-adp@verify-aged2-5 | 1542 | 0 | 159,043 (1.590) | fits |
| backlog-adp@verify-aged2-6 | 1548 | 0 | 160,646 (1.606) | fits |
| backlog-adp@verify-aged2-7 | 1554 | 0 | 157,932 (1.579) | fits |
| backlog-adp@verify-aged1-0 | 1481 | 0 | 157,401 (1.574) | fits |
| backlog-adp@verify-aged1-1 | 1485 | 0 | 158,444 (1.584) | fits |
| backlog-adp@verify-aged1-2 | 1489 | 0 | 158,026 (1.580) | fits |
| backlog-adp@verify-aged1-3 | 1493 | 0 | 158,868 (1.589) | fits |
| backlog-adp@verify-aged1-4 | 1498 | 0 | 159,013 (1.590) | fits |
| backlog-adp@verify-aged1-5 | 1503 | 0 | 158,868 (1.589) | fits |
| backlog-adp@verify-aged1-6 | 1508 | 0 | 161,168 (1.612) | fits |
| backlog-adp@verify-aged1-7 | 1515 | 0 | 162,413 (1.624) | fits |
| adp-advertise | 615 | 0 | 54,010 (0.540) | fits |
| maap | 355 | 0 | 48,198 (0.482) | fits |
| acmp-noresp | 2597 | 0 | 109,052 (1.091) | fits |
| save | 627 | 0 | 54,010 (0.540) | fits |
| srp | 315 | 0 | 52,076 (0.521) | fits |
| backlog | 298 | 0 | 162,528 (1.625) | fits |
| backlog-adp | 323 | 0 | 160,056 (1.601) | fits |
| backlog-adp-refill | 338 | 0 | 159,255 (1.593) | fits |
| backlog-owed | 319 | 0 | 162,100 (1.621) | fits |
| acmp-disc | 1332 | 0 | 109,299 (1.093) | fits |
| adp-link | 96 | 0 | 54,912 (0.549) | fits |
| adp-gm | 94 | 0 | 54,010 (0.540) | fits |
| adp-discover | 94 | 0 | 54,010 (0.540) | fits |
| control | 94 | 0 | 54,010 (0.540) | fits |
| aecp-fanout | 153 | 0 | 78,204 (0.782) | fits |
| acmp-cmd | 112 | 0 | 54,010 (0.540) | fits |
| aecp | 141 | 0 | 54,010 (0.540) | fits |
| datapath-events | 164 | 0 | 54,010 (0.540) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.srp.last.if1` | 9.198 (20) | 10.802 |
| backlog-adp@blank-aged2-1 | 2 | none | +9.355 ms, 77,377 (0.774 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if1` | 9.318 (20) | 10.682 |
| backlog-adp@blank-aged2-2 | 2 | +8.528 ms, 77,563 (0.776 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if1` | 10.130 (20) | 9.870 |
| backlog-adp@blank-aged2-3 | 2 | +7.288 ms, 77,433 (0.774 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if1` | 10.104 (20) | 9.896 |
| backlog-adp@blank-aged2-4 | 2 | +5.983 ms, 77,563 (0.776 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if1` | 10.112 (20) | 9.888 |
| backlog-adp@blank-aged2-5 | 2 | +4.835 ms, 77,858 (0.779 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if1` | 10.161 (20) | 9.839 |
| backlog-adp@blank-aged2-6 | 2 | +4.868 ms, 77,858 (0.779 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if1` | 10.194 (20) | 9.806 |
| backlog-adp@blank-aged2-7 | 2 | +3.294 ms, 77,834 (0.778 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if1` | 10.168 (20) | 9.832 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if1` | 9.327 (20) | 10.673 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if1` | 9.432 (20) | 10.568 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if1` | 9.437 (20) | 10.563 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if1` | 9.197 (20) | 10.803 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if1` | 9.160 (20) | 10.840 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if1` | 9.213 (20) | 10.787 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if1` | 9.222 (20) | 10.778 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if1` | 9.240 (20) | 10.760 |
| backlog-adp@program-aged2-0 | 2 | none | +9.669 ms, 80,971 (0.810 ms), issue | `backlog-adp@program-aged2-0.service.srp.last.if1` | 9.325 (20) | 10.675 |
| backlog-adp@program-aged2-1 | 2 | none | +9.215 ms, 81,074 (0.811 ms), issue | `backlog-adp@program-aged2-1.service.srp.last.if1` | 9.177 (20) | 10.823 |
| backlog-adp@program-aged2-2 | 2 | none | none | `backlog-adp@program-aged2-2.service.srp.last.if1` | 10.044 (20) | 9.956 |
| backlog-adp@program-aged2-3 | 2 | none | none | `backlog-adp@program-aged2-3.service.srp.last.if1` | 10.232 (20) | 9.768 |
| backlog-adp@program-aged2-4 | 2 | none | none | `backlog-adp@program-aged2-4.service.srp.last.if1` | 10.245 (20) | 9.755 |
| backlog-adp@program-aged2-5 | 2 | none | none | `backlog-adp@program-aged2-5.service.srp.last.if1` | 10.044 (20) | 9.956 |
| backlog-adp@program-aged2-6 | 2 | +4.889 ms, 81,360 (0.814 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if1` | 10.055 (20) | 9.945 |
| backlog-adp@program-aged2-7 | 2 | none | none | `backlog-adp@program-aged2-7.service.srp.last.if1` | 10.056 (20) | 9.944 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if1` | 9.109 (20) | 10.891 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if1` | 9.223 (20) | 10.777 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if1` | 9.261 (20) | 10.739 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if1` | 9.244 (20) | 10.756 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if1` | 9.246 (20) | 10.754 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if1` | 9.303 (20) | 10.697 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if1` | 9.331 (20) | 10.669 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if1` | 9.304 (20) | 10.696 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if1` | 9.294 (20) | 10.706 |
| backlog-adp@verify-aged2-1 | 2 | none | +9.437 ms, 78,309 (0.783 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if1` | 9.399 (20) | 10.601 |
| backlog-adp@verify-aged2-2 | 2 | +8.527 ms, 78,252 (0.783 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if1` | 10.225 (20) | 9.775 |
| backlog-adp@verify-aged2-3 | 2 | +7.383 ms, 78,252 (0.783 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if1` | 10.213 (20) | 9.787 |
| backlog-adp@verify-aged2-4 | 2 | +5.932 ms, 78,298 (0.783 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if1` | 9.985 (20) | 10.015 |
| backlog-adp@verify-aged2-5 | 2 | +4.794 ms, 78,560 (0.786 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if1` | 10.024 (20) | 9.976 |
| backlog-adp@verify-aged2-6 | 2 | +4.878 ms, 78,559 (0.786 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if1` | 10.207 (20) | 9.793 |
| backlog-adp@verify-aged2-7 | 2 | +3.326 ms, 78,648 (0.786 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if1` | 10.236 (20) | 9.764 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if1` | 9.160 (20) | 10.840 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if1` | 9.228 (20) | 10.772 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if1` | 9.229 (20) | 10.771 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if1` | 9.254 (20) | 10.746 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if1` | 9.269 (20) | 10.731 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if1` | 9.300 (20) | 10.700 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if1` | 9.311 (20) | 10.689 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if1` | 9.333 (20) | 10.667 |

Least margin over the aged windows: 9.755 ms, `backlog-adp@program-aged2-4.service.srp.last.if1` at 10.245 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 22829.753 | 22,870 | 382 | 2 | 32.109 | yes | within |
| save-held | 4817.708 | 12,470 | 382 | - | 15.422 | no | within |
| save-starved | 12447.465 | 12,470 | 382 | - | 35.778 | yes | within |
| save | 4818.263 | 12,470 | 382 | - | 11.197 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1080 | 80,998 (0.810) | 78,395 (0.784) |
| save-held | 1562 | 106,069 (1.061) | 78,928 (0.789) |
| save-starved | 698 | 81,448 (0.814) | 78,631 (0.786) |
| acmp-notk | 1065 | 114,080 (1.141) | 78,988 (0.790) |
| backlog-adp@blank-0 | 339 | 100,751 (1.008) | 76,228 (0.762) |
| backlog-adp@blank-1 | 339 | 102,245 (1.022) | 76,303 (0.763) |
| backlog-adp@blank-2 | 339 | 101,939 (1.019) | 76,305 (0.763) |
| backlog-adp@blank-3 | 339 | 101,881 (1.019) | 76,303 (0.763) |
| backlog-adp@blank-4 | 339 | 101,938 (1.019) | 76,305 (0.763) |
| backlog-adp@blank-5 | 339 | 102,244 (1.022) | 76,305 (0.763) |
| backlog-adp@blank-6 | 339 | 102,316 (1.023) | 76,305 (0.763) |
| backlog-adp@blank-7 | 340 | 102,150 (1.022) | 76,303 (0.763) |
| backlog-adp@program-0 | 448 | 105,547 (1.055) | 78,859 (0.789) |
| backlog-adp@program-1 | 448 | 105,782 (1.058) | 78,936 (0.789) |
| backlog-adp@program-2 | 448 | 105,547 (1.055) | 78,999 (0.790) |
| backlog-adp@program-3 | 448 | 105,722 (1.057) | 78,934 (0.789) |
| backlog-adp@program-4 | 449 | 105,547 (1.055) | 78,628 (0.786) |
| backlog-adp@program-5 | 449 | 105,547 (1.055) | 78,628 (0.786) |
| backlog-adp@program-6 | 449 | 105,547 (1.055) | 78,628 (0.786) |
| backlog-adp@program-7 | 449 | 105,547 (1.055) | 78,628 (0.786) |
| backlog-adp@verify-0 | 555 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@verify-1 | 555 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@verify-2 | 555 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@verify-3 | 555 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@verify-4 | 555 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@verify-5 | 555 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@verify-6 | 555 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@verify-7 | 556 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@blank-aged2-0 | 338 | 102,004 (1.020) | 76,306 (0.763) |
| backlog-adp@blank-aged2-1 | 337 | 85,020 (0.850) | 75,997 (0.760) |
| backlog-adp@blank-aged2-2 | 337 | 85,020 (0.850) | 75,999 (0.760) |
| backlog-adp@blank-aged2-3 | 337 | 85,020 (0.850) | 75,997 (0.760) |
| backlog-adp@blank-aged2-4 | 337 | 85,020 (0.850) | 75,999 (0.760) |
| backlog-adp@blank-aged2-5 | 337 | 85,020 (0.850) | 76,067 (0.761) |
| backlog-adp@blank-aged2-6 | 337 | 85,020 (0.850) | 76,067 (0.761) |
| backlog-adp@blank-aged2-7 | 338 | 100,368 (1.004) | 76,198 (0.762) |
| backlog-adp@blank-aged1-0 | 337 | 100,760 (1.008) | 76,229 (0.762) |
| backlog-adp@blank-aged1-1 | 337 | 101,988 (1.020) | 76,304 (0.763) |
| backlog-adp@blank-aged1-2 | 337 | 101,939 (1.019) | 76,306 (0.763) |
| backlog-adp@blank-aged1-3 | 337 | 102,109 (1.021) | 76,304 (0.763) |
| backlog-adp@blank-aged1-4 | 337 | 110,014 (1.100) | 76,552 (0.766) |
| backlog-adp@blank-aged1-5 | 337 | 102,851 (1.029) | 76,468 (0.765) |
| backlog-adp@blank-aged1-6 | 337 | 102,013 (1.020) | 76,369 (0.764) |
| backlog-adp@blank-aged1-7 | 337 | 101,948 (1.019) | 76,304 (0.763) |
| backlog-adp@program-aged2-0 | 446 | 105,547 (1.055) | 78,628 (0.786) |
| backlog-adp@program-aged2-1 | 446 | 105,547 (1.055) | 78,628 (0.786) |
| backlog-adp@program-aged2-2 | 446 | 105,547 (1.055) | 78,830 (0.788) |
| backlog-adp@program-aged2-3 | 446 | 105,547 (1.055) | 78,828 (0.788) |
| backlog-adp@program-aged2-4 | 446 | 105,547 (1.055) | 78,898 (0.789) |
| backlog-adp@program-aged2-5 | 446 | 105,547 (1.055) | 78,998 (0.790) |
| backlog-adp@program-aged2-6 | 446 | 105,547 (1.055) | 78,649 (0.786) |
| backlog-adp@program-aged2-7 | 447 | 105,547 (1.055) | 78,717 (0.787) |
| backlog-adp@program-aged1-0 | 447 | 105,904 (1.059) | 78,936 (0.789) |
| backlog-adp@program-aged1-1 | 446 | 105,977 (1.060) | 79,030 (0.790) |
| backlog-adp@program-aged1-2 | 446 | 106,009 (1.060) | 78,936 (0.789) |
| backlog-adp@program-aged1-3 | 446 | 105,952 (1.060) | 78,934 (0.789) |
| backlog-adp@program-aged1-4 | 446 | 106,081 (1.061) | 79,032 (0.790) |
| backlog-adp@program-aged1-5 | 446 | 105,784 (1.058) | 78,934 (0.789) |
| backlog-adp@program-aged1-6 | 446 | 105,784 (1.058) | 78,934 (0.789) |
| backlog-adp@program-aged1-7 | 447 | 105,912 (1.059) | 78,936 (0.789) |
| backlog-adp@verify-aged2-0 | 556 | 110,931 (1.109) | 78,961 (0.790) |
| backlog-adp@verify-aged2-1 | 555 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@verify-aged2-2 | 555 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@verify-aged2-3 | 555 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@verify-aged2-4 | 555 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@verify-aged2-5 | 555 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@verify-aged2-6 | 555 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@verify-aged2-7 | 556 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@verify-aged1-0 | 556 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@verify-aged1-1 | 555 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@verify-aged1-2 | 555 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@verify-aged1-3 | 555 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@verify-aged1-4 | 555 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@verify-aged1-5 | 555 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@verify-aged1-6 | 555 | 109,798 (1.098) | 78,961 (0.790) |
| backlog-adp@verify-aged1-7 | 556 | 109,798 (1.098) | 78,961 (0.790) |
| adp-advertise | 577 | 31,209 (0.312) | 2,851 (0.029) |
| maap | 325 | 32,467 (0.325) | 2,853 (0.029) |
| acmp-noresp | 615 | 113,814 (1.138) | 78,890 (0.789) |
| save | 585 | 105,610 (1.056) | 78,669 (0.787) |
| srp | 278 | 31,147 (0.311) | 2,851 (0.029) |
| backlog | 266 | 31,209 (0.312) | 2,851 (0.029) |
| backlog-adp | 271 | 31,209 (0.312) | 2,851 (0.029) |
| backlog-adp-refill | 274 | 31,209 (0.312) | 2,851 (0.029) |
| backlog-owed | 277 | 31,209 (0.312) | 2,851 (0.029) |
| acmp-disc | 336 | 114,080 (1.141) | 78,726 (0.787) |
| adp-link | 79 | 31,209 (0.312) | 2,851 (0.029) |
| adp-gm | 79 | 31,209 (0.312) | 2,851 (0.029) |
| adp-discover | 79 | 31,209 (0.312) | 2,851 (0.029) |
| control | 79 | 31,209 (0.312) | 2,851 (0.029) |
| aecp-fanout | 94 | 31,209 (0.312) | 2,851 (0.029) |
| acmp-cmd | 67 | 31,209 (0.312) | 2,851 (0.029) |
| aecp | 89 | 31,209 (0.312) | 2,851 (0.029) |
| datapath-events | 74 | 31,209 (0.312) | 2,851 (0.029) |

Longest pass that carries a step: 114,080 CPU cycles (1.141 ms), acmp-notk; longest step: 79,032 (0.790 ms), backlog-adp@program-aged1-4.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if1` | 295,827 | 2.958 | 20 | 200 | fits | 130,466 | 127 | 0.541 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 288,414 | 2.884 | 20 | 20 | fits | 94,031 | 55 | 0.509 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if1` | 268,785 | 2.688 | 20 | 24 | fits | 77,764 | 56 | 0.487 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 236,215 | 2.362 | 20 | 50 | fits | 130,466 | 127 | 0.541 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if1` | 840,502 | 8.405 | 20 | 20 | fits | 104,117 | 41 | 0.553 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 157,919 | 1.579 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if1` | 107,225 | 1.072 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 187,384 | 1.874 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 275,514 | 2.755 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if1` | 379,650 | 3.796 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if1` | 299,471 | 2.995 | 20 | 200 | fits | 134,110 | 133 | 0.558 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 377,315 | 3.773 | 20 | 20 | fits | 116,410 | 69 | 0.517 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if1` | 341,453 | 3.415 | 20 | 24 | fits | 79,240 | 61 | 0.488 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if1` | 221,430 | 2.214 | 20 | 50 | fits | 159,414 | 232 | 0.300 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if1` | 860,239 | 8.602 | 20 | 20 | fits | 116,590 | 51 | 0.571 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 156,578 | 1.566 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if1` | 99,862 | 0.999 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 203,130 | 2.031 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 304,486 | 3.045 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if1` | 388,605 | 3.886 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 34,335 | 0.343 | 20 | 20 | fits | 44,858 | 33 (14) | 0.812 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 21,979 | 0.220 | 20 | 20 | fits | 44,610 | 19 (14) | 0.894 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 461,156 | 4.612 | 20 | 20 | fits | 148,549 | 186 | 0.339 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 381,199 | 3.812 | 20 | 200 | fits | 160,758 | 214 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 529,132 | 5.291 | 20 | 200 | fits | 148,549 | 186 | 0.339 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 382,123 | 3.821 | 20 | 20 | fits | 160,758 | 214 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 529,836 | 5.298 | 20 | 20 | fits | 148,549 | 186 | 0.339 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 215,043 | 2.150 | 20 | 24 | fits | 155,844 | 171 | 0.317 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if1` | 384,773 | 3.848 | 20 | 24 | fits | 160,758 | 214 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 384,707 | 3.847 | 20 | 50 | fits | 160,758 | 214 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 532,860 | 5.329 | 20 | 50 | fits | 148,549 | 186 | 0.339 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 652,602 | 6.526 | 20 | 20 | fits | 119,808 | 37 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if1` | 970,319 | 9.703 | 20 | 20 | fits | 75,473 | 30 | 0.609 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 383,055 | 3.831 | 20 | 20 | fits | 150,721 | 177 | 0.324 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 308,214 | 3.082 | 20 | 200 | fits | 158,642 | 220 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 458,319 | 4.583 | 20 | 200 | fits | 150,721 | 177 | 0.324 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 309,138 | 3.091 | 20 | 20 | fits | 158,642 | 220 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 459,023 | 4.590 | 20 | 20 | fits | 150,721 | 177 | 0.324 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 154,136 | 1.541 | 20 | 24 | fits | 155,202 | 170 | 0.317 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if1` | 311,788 | 3.118 | 20 | 24 | fits | 158,642 | 220 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 311,722 | 3.117 | 20 | 50 | fits | 158,642 | 220 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 462,047 | 4.620 | 20 | 50 | fits | 150,721 | 177 | 0.324 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 581,756 | 5.818 | 20 | 20 | fits | 119,775 | 37 | 0.714 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if1` | 926,653 | 9.267 | 20 | 20 | fits | 95,565 | 39 | 0.671 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 406,497 | 4.065 | 20 | 20 | fits | 151,079 | 177 | 0.329 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 332,064 | 3.321 | 20 | 200 | fits | 158,782 | 220 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 482,527 | 4.825 | 20 | 200 | fits | 151,079 | 177 | 0.329 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 332,988 | 3.330 | 20 | 20 | fits | 158,782 | 220 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 483,231 | 4.832 | 20 | 20 | fits | 151,079 | 177 | 0.329 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 177,846 | 1.778 | 20 | 24 | fits | 155,071 | 170 | 0.315 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if1` | 335,638 | 3.356 | 20 | 24 | fits | 158,782 | 220 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 335,572 | 3.356 | 20 | 50 | fits | 158,782 | 220 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 486,255 | 4.863 | 20 | 50 | fits | 151,079 | 177 | 0.329 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 606,127 | 6.061 | 20 | 20 | fits | 119,938 | 38 | 0.714 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if1` | 949,995 | 9.500 | 20 | 20 | fits | 94,006 | 37 | 0.557 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 405,498 | 4.055 | 20 | 20 | fits | 151,231 | 178 | 0.331 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 331,000 | 3.310 | 20 | 200 | fits | 158,752 | 220 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 481,615 | 4.816 | 20 | 200 | fits | 151,231 | 178 | 0.331 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 331,924 | 3.319 | 20 | 20 | fits | 158,752 | 220 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 482,319 | 4.823 | 20 | 20 | fits | 151,231 | 178 | 0.331 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 176,812 | 1.768 | 20 | 24 | fits | 155,112 | 170 | 0.316 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if1` | 334,574 | 3.346 | 20 | 24 | fits | 158,752 | 220 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 334,508 | 3.345 | 20 | 50 | fits | 158,752 | 220 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 485,343 | 4.853 | 20 | 50 | fits | 151,231 | 178 | 0.331 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 620,373 | 6.204 | 20 | 20 | fits | 124,694 | 43 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if1` | 946,043 | 9.460 | 20 | 20 | fits | 85,250 | 33 | 0.578 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 408,862 | 4.089 | 20 | 20 | fits | 154,269 | 182 | 0.352 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 329,914 | 3.299 | 20 | 200 | fits | 158,782 | 220 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 483,567 | 4.836 | 20 | 200 | fits | 154,269 | 182 | 0.352 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 330,838 | 3.308 | 20 | 20 | fits | 158,782 | 220 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 484,271 | 4.843 | 20 | 20 | fits | 154,269 | 182 | 0.352 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 175,696 | 1.757 | 20 | 24 | fits | 155,071 | 170 | 0.315 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if1` | 333,488 | 3.335 | 20 | 24 | fits | 158,782 | 220 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 333,422 | 3.334 | 20 | 50 | fits | 158,782 | 220 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 487,295 | 4.873 | 20 | 50 | fits | 154,269 | 182 | 0.352 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 625,941 | 6.259 | 20 | 20 | fits | 128,115 | 43 | 0.737 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if1` | 943,406 | 9.434 | 20 | 20 | fits | 75,282 | 29 | 0.607 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 427,741 | 4.277 | 20 | 20 | fits | 155,148 | 178 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 328,914 | 3.289 | 20 | 200 | fits | 158,816 | 221 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 493,889 | 4.939 | 20 | 200 | fits | 155,148 | 178 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 329,838 | 3.298 | 20 | 20 | fits | 158,816 | 221 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 622,328 | 6.223 | 20 | 20 | fits | 127,735 | 44 | 0.692 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 174,662 | 1.747 | 20 | 24 | fits | 155,112 | 170 | 0.316 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if1` | 332,488 | 3.325 | 20 | 24 | fits | 158,816 | 221 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 332,422 | 3.324 | 20 | 50 | fits | 158,816 | 221 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 497,617 | 4.976 | 20 | 50 | fits | 155,148 | 178 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 625,286 | 6.253 | 20 | 20 | fits | 127,735 | 44 | 0.692 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if1` | 943,001 | 9.430 | 20 | 20 | fits | 75,282 | 29 | 0.607 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 424,123 | 4.241 | 20 | 20 | fits | 160,570 | 179 | 0.376 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 339,255 | 3.393 | 20 | 200 | fits | 160,314 | 225 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 499,209 | 4.992 | 20 | 200 | fits | 160,570 | 179 | 0.376 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 340,179 | 3.402 | 20 | 20 | fits | 160,314 | 225 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 499,913 | 4.999 | 20 | 20 | fits | 160,570 | 179 | 0.376 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 173,587 | 1.736 | 20 | 24 | fits | 155,112 | 171 | 0.315 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if1` | 342,829 | 3.428 | 20 | 24 | fits | 160,314 | 225 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 342,763 | 3.428 | 20 | 50 | fits | 160,314 | 225 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 502,937 | 5.029 | 20 | 50 | fits | 160,570 | 179 | 0.376 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 623,085 | 6.231 | 20 | 20 | fits | 120,214 | 37 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if1` | 940,386 | 9.404 | 20 | 20 | fits | 75,282 | 29 | 0.607 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 393,633 | 3.936 | 20 | 20 | fits | 157,794 | 195 | 0.322 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 310,584 | 3.106 | 20 | 200 | fits | 157,948 | 203 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 467,762 | 4.678 | 20 | 200 | fits | 157,794 | 195 | 0.322 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 311,508 | 3.115 | 20 | 20 | fits | 157,948 | 203 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 468,466 | 4.685 | 20 | 20 | fits | 157,794 | 195 | 0.322 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 157,200 | 1.572 | 20 | 24 | fits | 155,747 | 170 | 0.319 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if1` | 314,158 | 3.142 | 20 | 24 | fits | 157,948 | 203 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 314,092 | 3.141 | 20 | 50 | fits | 157,948 | 203 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 471,490 | 4.715 | 20 | 50 | fits | 157,794 | 195 | 0.322 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 591,308 | 5.913 | 20 | 20 | fits | 119,884 | 37 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if1` | 927,037 | 9.270 | 20 | 20 | fits | 82,293 | 35 | 0.689 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 387,669 | 3.877 | 20 | 20 | fits | 150,821 | 177 | 0.324 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 312,728 | 3.127 | 20 | 200 | fits | 158,402 | 220 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 462,933 | 4.629 | 20 | 200 | fits | 150,821 | 177 | 0.324 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 313,652 | 3.137 | 20 | 20 | fits | 158,402 | 220 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 463,637 | 4.636 | 20 | 20 | fits | 150,821 | 177 | 0.324 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 158,890 | 1.589 | 20 | 24 | fits | 154,933 | 170 | 0.314 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if1` | 316,302 | 3.163 | 20 | 24 | fits | 158,402 | 220 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 316,236 | 3.162 | 20 | 50 | fits | 158,402 | 220 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 466,661 | 4.667 | 20 | 50 | fits | 150,821 | 177 | 0.324 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 585,864 | 5.859 | 20 | 20 | fits | 119,269 | 38 | 0.711 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if1` | 921,445 | 9.214 | 20 | 20 | fits | 85,263 | 33 | 0.578 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 385,519 | 3.855 | 20 | 20 | fits | 150,908 | 178 | 0.325 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 310,578 | 3.106 | 20 | 200 | fits | 158,402 | 220 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 460,870 | 4.609 | 20 | 200 | fits | 150,908 | 178 | 0.325 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 311,502 | 3.115 | 20 | 20 | fits | 158,402 | 220 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 461,574 | 4.616 | 20 | 20 | fits | 150,908 | 178 | 0.325 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 156,740 | 1.567 | 20 | 24 | fits | 154,933 | 170 | 0.314 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if1` | 314,152 | 3.142 | 20 | 24 | fits | 158,402 | 220 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 314,086 | 3.141 | 20 | 50 | fits | 158,402 | 220 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 464,598 | 4.646 | 20 | 50 | fits | 150,908 | 178 | 0.325 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 599,278 | 5.993 | 20 | 20 | fits | 124,152 | 43 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if1` | 925,381 | 9.254 | 20 | 20 | fits | 85,579 | 33 | 0.585 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 394,943 | 3.949 | 20 | 20 | fits | 151,051 | 177 | 0.329 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 319,816 | 3.198 | 20 | 200 | fits | 159,856 | 225 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 470,251 | 4.703 | 20 | 200 | fits | 151,051 | 177 | 0.329 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 320,740 | 3.207 | 20 | 20 | fits | 159,856 | 225 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 470,955 | 4.710 | 20 | 20 | fits | 151,051 | 177 | 0.329 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 154,640 | 1.546 | 20 | 24 | fits | 154,983 | 171 | 0.314 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if1` | 323,390 | 3.234 | 20 | 24 | fits | 159,856 | 225 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 323,324 | 3.233 | 20 | 50 | fits | 159,856 | 225 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 473,979 | 4.740 | 20 | 50 | fits | 151,051 | 177 | 0.329 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 600,115 | 6.001 | 20 | 20 | fits | 126,202 | 43 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if1` | 917,448 | 9.174 | 20 | 20 | fits | 75,356 | 30 | 0.606 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 398,303 | 3.983 | 20 | 20 | fits | 157,845 | 195 | 0.321 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 315,203 | 3.152 | 20 | 200 | fits | 157,608 | 203 | 0.406 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 472,432 | 4.724 | 20 | 200 | fits | 157,845 | 195 | 0.321 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 316,127 | 3.161 | 20 | 20 | fits | 157,608 | 203 | 0.406 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 473,136 | 4.731 | 20 | 20 | fits | 157,845 | 195 | 0.321 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 162,159 | 1.622 | 20 | 24 | fits | 154,897 | 170 | 0.314 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if1` | 318,777 | 3.188 | 20 | 24 | fits | 157,608 | 203 | 0.406 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 318,711 | 3.187 | 20 | 50 | fits | 157,608 | 203 | 0.406 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 476,160 | 4.762 | 20 | 50 | fits | 157,845 | 195 | 0.321 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 595,434 | 5.954 | 20 | 20 | fits | 119,340 | 37 | 0.714 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if1` | 931,924 | 9.319 | 20 | 20 | fits | 85,623 | 33 | 0.588 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 389,133 | 3.891 | 20 | 20 | fits | 148,780 | 187 | 0.347 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 325,830 | 3.258 | 20 | 200 | fits | 159,673 | 209 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 473,994 | 4.740 | 20 | 200 | fits | 148,780 | 187 | 0.347 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 326,754 | 3.268 | 20 | 20 | fits | 159,673 | 209 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 474,698 | 4.747 | 20 | 20 | fits | 148,780 | 187 | 0.347 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 170,721 | 1.707 | 20 | 24 | fits | 156,175 | 170 | 0.317 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if1` | 329,404 | 3.294 | 20 | 24 | fits | 159,673 | 209 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 329,338 | 3.293 | 20 | 50 | fits | 159,673 | 209 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 477,722 | 4.777 | 20 | 50 | fits | 148,780 | 187 | 0.347 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 612,686 | 6.127 | 20 | 20 | fits | 124,357 | 43 | 0.733 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if1` | 930,481 | 9.305 | 20 | 20 | fits | 75,391 | 29 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 399,233 | 3.992 | 20 | 20 | fits | 148,826 | 186 | 0.348 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 335,841 | 3.358 | 20 | 200 | fits | 160,641 | 214 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 484,051 | 4.841 | 20 | 200 | fits | 148,826 | 186 | 0.348 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 336,765 | 3.368 | 20 | 20 | fits | 160,641 | 214 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 484,755 | 4.848 | 20 | 20 | fits | 148,826 | 186 | 0.348 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 169,788 | 1.698 | 20 | 24 | fits | 155,019 | 171 | 0.314 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if1` | 339,415 | 3.394 | 20 | 24 | fits | 160,641 | 214 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 339,349 | 3.393 | 20 | 50 | fits | 160,641 | 214 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 487,779 | 4.878 | 20 | 50 | fits | 148,826 | 186 | 0.348 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 607,127 | 6.071 | 20 | 20 | fits | 119,414 | 37 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if1` | 933,417 | 9.334 | 20 | 20 | fits | 85,601 | 34 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 395,318 | 3.953 | 20 | 20 | fits | 148,574 | 186 | 0.344 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 332,134 | 3.321 | 20 | 200 | fits | 159,344 | 209 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 480,092 | 4.801 | 20 | 200 | fits | 148,574 | 186 | 0.344 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 333,058 | 3.331 | 20 | 20 | fits | 159,344 | 209 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 480,796 | 4.808 | 20 | 20 | fits | 148,574 | 186 | 0.344 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 177,354 | 1.774 | 20 | 24 | fits | 154,897 | 170 | 0.314 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if1` | 335,708 | 3.357 | 20 | 24 | fits | 159,344 | 209 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 335,642 | 3.356 | 20 | 50 | fits | 159,344 | 209 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 483,820 | 4.838 | 20 | 50 | fits | 148,574 | 186 | 0.344 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 610,043 | 6.100 | 20 | 20 | fits | 126,289 | 43 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if1` | 946,612 | 9.466 | 20 | 20 | fits | 85,799 | 33 | 0.593 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 410,603 | 4.106 | 20 | 20 | fits | 157,731 | 195 | 0.322 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 328,385 | 3.284 | 20 | 200 | fits | 157,745 | 203 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 485,500 | 4.855 | 20 | 200 | fits | 157,731 | 195 | 0.322 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 329,309 | 3.293 | 20 | 20 | fits | 157,745 | 203 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 486,204 | 4.862 | 20 | 20 | fits | 157,731 | 195 | 0.322 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 175,204 | 1.752 | 20 | 24 | fits | 154,897 | 170 | 0.314 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if1` | 331,959 | 3.320 | 20 | 24 | fits | 157,745 | 203 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 331,893 | 3.319 | 20 | 50 | fits | 157,745 | 203 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 489,228 | 4.892 | 20 | 50 | fits | 157,731 | 195 | 0.322 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 624,098 | 6.241 | 20 | 20 | fits | 124,274 | 43 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if1` | 941,471 | 9.415 | 20 | 20 | fits | 75,282 | 29 | 0.607 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 456,594 | 4.566 | 20 | 20 | fits | 150,118 | 189 | 0.339 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 373,155 | 3.732 | 20 | 200 | fits | 158,472 | 210 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 522,657 | 5.227 | 20 | 200 | fits | 150,118 | 189 | 0.339 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 374,079 | 3.741 | 20 | 20 | fits | 158,472 | 210 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 523,361 | 5.234 | 20 | 20 | fits | 150,118 | 189 | 0.339 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 209,334 | 2.093 | 20 | 24 | fits | 155,647 | 171 | 0.315 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if1` | 376,729 | 3.767 | 20 | 24 | fits | 158,472 | 210 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 376,663 | 3.767 | 20 | 50 | fits | 158,472 | 210 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 526,385 | 5.264 | 20 | 50 | fits | 150,118 | 189 | 0.339 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 646,299 | 6.463 | 20 | 20 | fits | 119,980 | 37 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if1` | 963,693 | 9.637 | 20 | 20 | fits | 75,364 | 30 | 0.606 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 390,864 | 3.909 | 20 | 20 | fits | 148,509 | 186 | 0.344 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 327,745 | 3.277 | 20 | 200 | fits | 159,169 | 209 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 475,638 | 4.756 | 20 | 200 | fits | 148,509 | 186 | 0.344 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 328,669 | 3.287 | 20 | 20 | fits | 159,169 | 209 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 476,342 | 4.763 | 20 | 20 | fits | 148,509 | 186 | 0.344 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 173,140 | 1.731 | 20 | 24 | fits | 154,887 | 170 | 0.314 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if1` | 331,319 | 3.313 | 20 | 24 | fits | 159,169 | 209 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 331,253 | 3.313 | 20 | 50 | fits | 159,169 | 209 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 479,366 | 4.794 | 20 | 50 | fits | 148,509 | 186 | 0.344 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 599,128 | 5.991 | 20 | 20 | fits | 119,828 | 37 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if1` | 943,702 | 9.437 | 20 | 20 | fits | 93,866 | 39 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 389,713 | 3.897 | 20 | 20 | fits | 148,444 | 186 | 0.344 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 326,659 | 3.267 | 20 | 200 | fits | 159,199 | 209 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 474,487 | 4.745 | 20 | 200 | fits | 148,444 | 186 | 0.344 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 327,583 | 3.276 | 20 | 20 | fits | 159,199 | 209 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 475,191 | 4.752 | 20 | 20 | fits | 148,444 | 186 | 0.344 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 172,024 | 1.720 | 20 | 24 | fits | 154,846 | 170 | 0.313 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if1` | 330,233 | 3.302 | 20 | 24 | fits | 159,199 | 209 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 330,167 | 3.302 | 20 | 50 | fits | 159,199 | 209 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 478,215 | 4.782 | 20 | 50 | fits | 148,444 | 186 | 0.344 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 598,067 | 5.981 | 20 | 20 | fits | 119,918 | 38 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if1` | 942,324 | 9.423 | 20 | 20 | fits | 94,115 | 37 | 0.560 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 388,714 | 3.887 | 20 | 20 | fits | 148,596 | 187 | 0.345 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 325,595 | 3.256 | 20 | 200 | fits | 159,169 | 209 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 473,575 | 4.736 | 20 | 200 | fits | 148,596 | 187 | 0.345 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 326,519 | 3.265 | 20 | 20 | fits | 159,169 | 209 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 474,279 | 4.743 | 20 | 20 | fits | 148,596 | 187 | 0.345 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 170,990 | 1.710 | 20 | 24 | fits | 154,887 | 170 | 0.314 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if1` | 329,169 | 3.292 | 20 | 24 | fits | 159,169 | 209 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 329,103 | 3.291 | 20 | 50 | fits | 159,169 | 209 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 477,303 | 4.773 | 20 | 50 | fits | 148,596 | 187 | 0.345 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 612,470 | 6.125 | 20 | 20 | fits | 124,831 | 43 | 0.733 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if1` | 938,458 | 9.385 | 20 | 20 | fits | 85,351 | 33 | 0.581 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 392,301 | 3.923 | 20 | 20 | fits | 152,944 | 193 | 0.365 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 324,509 | 3.245 | 20 | 200 | fits | 159,199 | 209 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 476,837 | 4.768 | 20 | 200 | fits | 152,944 | 193 | 0.365 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 325,433 | 3.254 | 20 | 20 | fits | 159,199 | 209 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 477,541 | 4.775 | 20 | 20 | fits | 152,944 | 193 | 0.365 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 169,874 | 1.699 | 20 | 24 | fits | 154,846 | 170 | 0.313 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if1` | 328,083 | 3.281 | 20 | 24 | fits | 159,199 | 209 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 328,017 | 3.280 | 20 | 50 | fits | 159,199 | 209 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 480,565 | 4.806 | 20 | 50 | fits | 152,944 | 193 | 0.365 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 619,151 | 6.192 | 20 | 20 | fits | 128,056 | 43 | 0.737 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if1` | 936,970 | 9.370 | 20 | 20 | fits | 75,391 | 29 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 411,171 | 4.112 | 20 | 20 | fits | 161,669 | 194 | 0.414 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 323,509 | 3.235 | 20 | 200 | fits | 159,233 | 210 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 495,094 | 4.951 | 20 | 200 | fits | 161,669 | 194 | 0.414 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 324,433 | 3.244 | 20 | 20 | fits | 159,233 | 210 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 495,798 | 4.958 | 20 | 20 | fits | 161,669 | 194 | 0.414 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 168,840 | 1.688 | 20 | 24 | fits | 154,887 | 170 | 0.314 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if1` | 327,083 | 3.271 | 20 | 24 | fits | 159,233 | 210 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 327,017 | 3.270 | 20 | 50 | fits | 159,233 | 210 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 498,822 | 4.988 | 20 | 50 | fits | 161,669 | 194 | 0.414 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 618,843 | 6.188 | 20 | 20 | fits | 120,087 | 37 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if1` | 936,503 | 9.365 | 20 | 20 | fits | 75,391 | 29 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 407,788 | 4.078 | 20 | 20 | fits | 158,214 | 188 | 0.390 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 334,020 | 3.340 | 20 | 200 | fits | 160,852 | 214 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 491,618 | 4.916 | 20 | 200 | fits | 158,214 | 188 | 0.390 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 334,944 | 3.349 | 20 | 20 | fits | 160,852 | 214 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 492,322 | 4.923 | 20 | 20 | fits | 158,214 | 188 | 0.390 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 167,765 | 1.678 | 20 | 24 | fits | 154,887 | 171 | 0.314 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if1` | 337,594 | 3.376 | 20 | 24 | fits | 160,852 | 214 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 337,528 | 3.375 | 20 | 50 | fits | 160,852 | 214 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 495,346 | 4.953 | 20 | 50 | fits | 158,214 | 188 | 0.390 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 615,474 | 6.155 | 20 | 20 | fits | 120,194 | 37 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if1` | 933,098 | 9.331 | 20 | 20 | fits | 75,391 | 29 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 411,572 | 4.116 | 20 | 20 | fits | 157,636 | 194 | 0.323 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 329,362 | 3.294 | 20 | 200 | fits | 157,958 | 203 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 486,382 | 4.864 | 20 | 200 | fits | 157,636 | 194 | 0.323 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 330,286 | 3.303 | 20 | 20 | fits | 157,958 | 203 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 487,086 | 4.871 | 20 | 20 | fits | 157,636 | 194 | 0.323 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 175,968 | 1.760 | 20 | 24 | fits | 154,778 | 170 | 0.313 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if1` | 332,936 | 3.329 | 20 | 24 | fits | 157,958 | 203 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 332,870 | 3.329 | 20 | 50 | fits | 157,958 | 203 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 490,110 | 4.901 | 20 | 50 | fits | 157,636 | 194 | 0.323 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 609,856 | 6.099 | 20 | 20 | fits | 119,812 | 37 | 0.714 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if1` | 945,556 | 9.456 | 20 | 20 | fits | 82,293 | 35 | 0.689 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 395,028 | 3.950 | 20 | 20 | fits | 148,384 | 187 | 0.336 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 315,279 | 3.153 | 20 | 200 | fits | 158,852 | 209 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 463,047 | 4.630 | 20 | 200 | fits | 148,384 | 187 | 0.336 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 316,203 | 3.162 | 20 | 20 | fits | 158,852 | 209 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 463,751 | 4.638 | 20 | 20 | fits | 148,384 | 187 | 0.336 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 160,991 | 1.610 | 20 | 24 | fits | 154,067 | 164 | 0.306 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if1` | 318,853 | 3.189 | 20 | 24 | fits | 158,852 | 209 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 318,787 | 3.188 | 20 | 50 | fits | 158,852 | 209 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 466,775 | 4.668 | 20 | 50 | fits | 148,384 | 187 | 0.336 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 602,050 | 6.021 | 20 | 20 | fits | 124,669 | 43 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if1` | 919,782 | 9.198 | 20 | 20 | fits | 75,388 | 29 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 402,750 | 4.027 | 20 | 20 | fits | 152,732 | 193 | 0.356 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 318,328 | 3.183 | 20 | 200 | fits | 159,195 | 209 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 470,444 | 4.704 | 20 | 200 | fits | 152,732 | 193 | 0.356 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 319,252 | 3.193 | 20 | 20 | fits | 159,195 | 209 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 471,148 | 4.711 | 20 | 20 | fits | 152,732 | 193 | 0.356 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 163,697 | 1.637 | 20 | 24 | fits | 154,067 | 164 | 0.306 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if1` | 321,902 | 3.219 | 20 | 24 | fits | 159,195 | 209 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 321,836 | 3.218 | 20 | 50 | fits | 159,195 | 209 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 474,172 | 4.742 | 20 | 50 | fits | 152,732 | 193 | 0.356 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 605,795 | 6.058 | 20 | 20 | fits | 120,823 | 37 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if1` | 931,761 | 9.318 | 20 | 20 | fits | 83,578 | 35 | 0.671 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 416,333 | 4.163 | 20 | 20 | fits | 153,568 | 192 | 0.386 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 320,978 | 3.210 | 20 | 200 | fits | 158,916 | 210 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 484,732 | 4.847 | 20 | 200 | fits | 153,568 | 192 | 0.386 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 321,902 | 3.219 | 20 | 20 | fits | 158,916 | 210 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 485,436 | 4.854 | 20 | 20 | fits | 153,568 | 192 | 0.386 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 166,626 | 1.666 | 20 | 24 | fits | 154,067 | 164 | 0.306 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if1` | 324,552 | 3.246 | 20 | 24 | fits | 158,916 | 210 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 324,486 | 3.245 | 20 | 50 | fits | 158,916 | 210 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 488,460 | 4.885 | 20 | 50 | fits | 153,568 | 192 | 0.386 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 608,343 | 6.083 | 20 | 20 | fits | 119,949 | 37 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if1` | 1,013,000 | 10.130 | 20 | 20 | fits | 86,386 | 33 | 0.604 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 415,240 | 4.152 | 20 | 20 | fits | 148,430 | 186 | 0.337 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 335,402 | 3.354 | 20 | 200 | fits | 160,686 | 214 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 483,216 | 4.832 | 20 | 200 | fits | 148,430 | 186 | 0.337 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 336,326 | 3.363 | 20 | 20 | fits | 160,686 | 214 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 483,920 | 4.839 | 20 | 20 | fits | 148,430 | 186 | 0.337 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 169,364 | 1.694 | 20 | 24 | fits | 154,099 | 165 | 0.307 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if1` | 338,976 | 3.390 | 20 | 24 | fits | 160,686 | 214 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 338,910 | 3.389 | 20 | 50 | fits | 160,686 | 214 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 486,944 | 4.869 | 20 | 50 | fits | 148,430 | 186 | 0.337 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 606,616 | 6.066 | 20 | 20 | fits | 119,738 | 37 | 0.714 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if1` | 1,010,412 | 10.104 | 20 | 20 | fits | 85,400 | 34 | 0.581 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 381,441 | 3.814 | 20 | 20 | fits | 148,466 | 186 | 0.344 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 318,365 | 3.184 | 20 | 200 | fits | 159,605 | 209 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 466,215 | 4.662 | 20 | 200 | fits | 148,466 | 186 | 0.344 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 319,289 | 3.193 | 20 | 20 | fits | 159,605 | 209 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 466,919 | 4.669 | 20 | 20 | fits | 148,466 | 186 | 0.344 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 163,324 | 1.633 | 20 | 24 | fits | 154,302 | 164 | 0.310 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if1` | 321,939 | 3.219 | 20 | 24 | fits | 159,605 | 209 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 321,873 | 3.219 | 20 | 50 | fits | 159,605 | 209 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 469,943 | 4.699 | 20 | 50 | fits | 148,466 | 186 | 0.344 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 596,547 | 5.965 | 20 | 20 | fits | 126,670 | 43 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if1` | 1,011,220 | 10.112 | 20 | 20 | fits | 85,799 | 33 | 0.593 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 394,373 | 3.944 | 20 | 20 | fits | 158,013 | 188 | 0.387 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 320,718 | 3.207 | 20 | 200 | fits | 159,217 | 209 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 478,115 | 4.781 | 20 | 200 | fits | 158,013 | 188 | 0.387 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 321,642 | 3.216 | 20 | 20 | fits | 159,217 | 209 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 478,819 | 4.788 | 20 | 20 | fits | 158,013 | 188 | 0.387 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 166,065 | 1.661 | 20 | 24 | fits | 154,006 | 164 | 0.306 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if1` | 324,292 | 3.243 | 20 | 24 | fits | 159,217 | 209 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 324,226 | 3.242 | 20 | 50 | fits | 159,217 | 209 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 481,843 | 4.818 | 20 | 50 | fits | 158,013 | 188 | 0.387 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 679,962 | 6.800 | 20 | 20 | fits | 120,327 | 38 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if1` | 1,016,055 | 10.161 | 20 | 20 | fits | 85,351 | 33 | 0.581 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 397,676 | 3.977 | 20 | 20 | fits | 157,948 | 188 | 0.386 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 324,086 | 3.241 | 20 | 200 | fits | 159,656 | 209 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 481,418 | 4.814 | 20 | 200 | fits | 157,948 | 188 | 0.386 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 325,010 | 3.250 | 20 | 20 | fits | 159,656 | 209 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 482,122 | 4.821 | 20 | 20 | fits | 157,948 | 188 | 0.386 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 168,994 | 1.690 | 20 | 24 | fits | 154,006 | 164 | 0.306 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if1` | 327,660 | 3.277 | 20 | 24 | fits | 159,656 | 209 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 327,594 | 3.276 | 20 | 50 | fits | 159,656 | 209 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 485,146 | 4.851 | 20 | 50 | fits | 157,948 | 188 | 0.386 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 687,689 | 6.877 | 20 | 20 | fits | 124,751 | 44 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if1` | 1,019,386 | 10.194 | 20 | 20 | fits | 75,362 | 29 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 489,111 | 4.891 | 20 | 20 | fits | 161,779 | 201 | 0.340 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 324,686 | 3.247 | 20 | 200 | fits | 157,550 | 203 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 563,683 | 5.637 | 20 | 200 | fits | 161,779 | 201 | 0.340 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 325,610 | 3.256 | 20 | 20 | fits | 157,550 | 203 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 564,387 | 5.644 | 20 | 20 | fits | 161,779 | 201 | 0.340 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 171,700 | 1.717 | 20 | 24 | fits | 154,006 | 164 | 0.306 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if1` | 328,260 | 3.283 | 20 | 24 | fits | 157,550 | 203 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 328,194 | 3.282 | 20 | 50 | fits | 157,550 | 203 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 567,411 | 5.674 | 20 | 50 | fits | 161,779 | 201 | 0.340 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 699,293 | 6.993 | 20 | 20 | fits | 120,943 | 37 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if1` | 1,016,758 | 10.168 | 20 | 20 | fits | 75,282 | 29 | 0.607 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 397,691 | 3.977 | 20 | 20 | fits | 150,786 | 177 | 0.325 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 322,785 | 3.228 | 20 | 200 | fits | 158,422 | 220 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 472,955 | 4.730 | 20 | 200 | fits | 150,786 | 177 | 0.325 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 323,709 | 3.237 | 20 | 20 | fits | 158,422 | 220 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 473,659 | 4.737 | 20 | 20 | fits | 150,786 | 177 | 0.325 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 168,927 | 1.689 | 20 | 24 | fits | 154,067 | 164 | 0.306 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if1` | 326,359 | 3.264 | 20 | 24 | fits | 158,422 | 220 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 326,293 | 3.263 | 20 | 50 | fits | 158,422 | 220 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 476,683 | 4.767 | 20 | 50 | fits | 150,786 | 177 | 0.325 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 596,242 | 5.962 | 20 | 20 | fits | 119,625 | 37 | 0.712 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if1` | 932,657 | 9.327 | 20 | 20 | fits | 85,647 | 33 | 0.589 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 400,700 | 4.007 | 20 | 20 | fits | 150,721 | 177 | 0.324 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 325,859 | 3.259 | 20 | 200 | fits | 158,567 | 220 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 475,964 | 4.760 | 20 | 200 | fits | 150,721 | 177 | 0.324 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 326,783 | 3.268 | 20 | 20 | fits | 158,567 | 220 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 476,668 | 4.767 | 20 | 20 | fits | 150,721 | 177 | 0.324 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 171,856 | 1.719 | 20 | 24 | fits | 154,067 | 164 | 0.306 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if1` | 329,433 | 3.294 | 20 | 24 | fits | 158,567 | 220 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 329,367 | 3.294 | 20 | 50 | fits | 158,567 | 220 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 479,692 | 4.797 | 20 | 50 | fits | 150,721 | 177 | 0.324 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 599,341 | 5.993 | 20 | 20 | fits | 119,715 | 38 | 0.711 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if1` | 943,168 | 9.432 | 20 | 20 | fits | 93,485 | 39 | 0.641 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 403,326 | 4.033 | 20 | 20 | fits | 150,873 | 178 | 0.326 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 328,420 | 3.284 | 20 | 200 | fits | 158,422 | 220 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 478,677 | 4.787 | 20 | 200 | fits | 150,873 | 178 | 0.326 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 329,344 | 3.293 | 20 | 20 | fits | 158,422 | 220 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 479,381 | 4.794 | 20 | 20 | fits | 150,873 | 178 | 0.326 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 174,562 | 1.746 | 20 | 24 | fits | 154,067 | 164 | 0.306 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if1` | 331,994 | 3.320 | 20 | 24 | fits | 158,422 | 220 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 331,928 | 3.319 | 20 | 50 | fits | 158,422 | 220 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 482,405 | 4.824 | 20 | 50 | fits | 150,873 | 178 | 0.326 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 617,637 | 6.176 | 20 | 20 | fits | 124,626 | 43 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if1` | 943,674 | 9.437 | 20 | 20 | fits | 85,579 | 33 | 0.585 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 404,122 | 4.041 | 20 | 20 | fits | 154,807 | 195 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 305,619 | 3.056 | 20 | 200 | fits | 158,367 | 211 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 470,524 | 4.705 | 20 | 200 | fits | 154,807 | 195 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 306,543 | 3.065 | 20 | 20 | fits | 158,367 | 211 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 471,228 | 4.712 | 20 | 20 | fits | 154,807 | 195 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 151,816 | 1.518 | 20 | 24 | fits | 154,067 | 164 | 0.306 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if1` | 309,193 | 3.092 | 20 | 24 | fits | 158,367 | 211 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 309,127 | 3.091 | 20 | 50 | fits | 158,367 | 211 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 474,252 | 4.743 | 20 | 50 | fits | 154,807 | 195 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 594,078 | 5.941 | 20 | 20 | fits | 119,892 | 37 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if1` | 919,682 | 9.197 | 20 | 20 | fits | 85,247 | 33 | 0.578 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 401,987 | 4.020 | 20 | 20 | fits | 150,118 | 189 | 0.339 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 318,548 | 3.185 | 20 | 200 | fits | 158,466 | 210 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 468,050 | 4.681 | 20 | 200 | fits | 150,118 | 189 | 0.339 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 319,472 | 3.195 | 20 | 20 | fits | 158,466 | 210 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 468,754 | 4.688 | 20 | 20 | fits | 150,118 | 189 | 0.339 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 154,849 | 1.548 | 20 | 24 | fits | 154,171 | 165 | 0.307 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if1` | 322,122 | 3.221 | 20 | 24 | fits | 158,466 | 210 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 322,056 | 3.221 | 20 | 50 | fits | 158,466 | 210 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 471,778 | 4.718 | 20 | 50 | fits | 150,118 | 189 | 0.339 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 598,661 | 5.987 | 20 | 20 | fits | 126,949 | 43 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if1` | 915,975 | 9.160 | 20 | 20 | fits | 75,279 | 29 | 0.607 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 415,030 | 4.150 | 20 | 20 | fits | 159,427 | 192 | 0.382 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 321,261 | 3.213 | 20 | 200 | fits | 158,583 | 210 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 480,072 | 4.801 | 20 | 200 | fits | 159,427 | 192 | 0.382 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 322,185 | 3.222 | 20 | 20 | fits | 158,583 | 210 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 480,776 | 4.808 | 20 | 20 | fits | 159,427 | 192 | 0.382 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 157,445 | 1.574 | 20 | 24 | fits | 154,061 | 165 | 0.307 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if1` | 324,835 | 3.248 | 20 | 24 | fits | 158,583 | 210 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 324,769 | 3.248 | 20 | 50 | fits | 158,583 | 210 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 483,800 | 4.838 | 20 | 50 | fits | 159,427 | 192 | 0.382 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 603,950 | 6.040 | 20 | 20 | fits | 120,216 | 37 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if1` | 921,259 | 9.213 | 20 | 20 | fits | 75,279 | 29 | 0.607 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 395,412 | 3.954 | 20 | 20 | fits | 157,231 | 207 | 0.386 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 305,271 | 3.053 | 20 | 200 | fits | 157,565 | 226 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 461,886 | 4.619 | 20 | 200 | fits | 157,231 | 207 | 0.386 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 306,195 | 3.062 | 20 | 20 | fits | 157,565 | 226 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 462,590 | 4.626 | 20 | 20 | fits | 157,231 | 207 | 0.386 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 152,270 | 1.523 | 20 | 24 | fits | 156,000 | 133 | 0.293 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if1` | 308,845 | 3.088 | 20 | 24 | fits | 157,565 | 226 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 308,779 | 3.088 | 20 | 50 | fits | 157,565 | 226 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 465,614 | 4.656 | 20 | 50 | fits | 157,231 | 207 | 0.386 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 585,748 | 5.857 | 20 | 20 | fits | 120,200 | 37 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if1` | 922,206 | 9.222 | 20 | 20 | fits | 85,878 | 33 | 0.593 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 397,516 | 3.975 | 20 | 20 | fits | 157,267 | 187 | 0.377 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 307,482 | 3.075 | 20 | 200 | fits | 159,999 | 214 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 464,133 | 4.641 | 20 | 200 | fits | 157,267 | 187 | 0.377 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 308,406 | 3.084 | 20 | 20 | fits | 159,999 | 214 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 464,837 | 4.648 | 20 | 20 | fits | 157,267 | 187 | 0.377 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 152,047 | 1.520 | 20 | 24 | fits | 154,006 | 164 | 0.306 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if1` | 311,056 | 3.111 | 20 | 24 | fits | 159,999 | 214 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 310,990 | 3.110 | 20 | 50 | fits | 159,999 | 214 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 467,861 | 4.679 | 20 | 50 | fits | 157,267 | 187 | 0.377 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 587,869 | 5.879 | 20 | 20 | fits | 120,074 | 38 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if1` | 924,021 | 9.240 | 20 | 20 | fits | 85,348 | 33 | 0.581 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 423,300 | 4.233 | 20 | 20 | fits | 153,589 | 192 | 0.385 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 327,968 | 3.280 | 20 | 200 | fits | 159,456 | 210 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 491,655 | 4.917 | 20 | 200 | fits | 153,589 | 192 | 0.385 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 328,892 | 3.289 | 20 | 20 | fits | 159,456 | 210 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 492,359 | 4.924 | 20 | 20 | fits | 153,589 | 192 | 0.385 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 173,076 | 1.731 | 20 | 24 | fits | 154,367 | 164 | 0.310 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if1` | 331,542 | 3.315 | 20 | 24 | fits | 159,456 | 210 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 331,476 | 3.315 | 20 | 50 | fits | 159,456 | 210 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 495,383 | 4.954 | 20 | 50 | fits | 153,589 | 192 | 0.385 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 614,792 | 6.148 | 20 | 20 | fits | 119,475 | 37 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if1` | 932,460 | 9.325 | 20 | 20 | fits | 75,388 | 29 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 383,457 | 3.835 | 20 | 20 | fits | 152,270 | 192 | 0.365 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 316,701 | 3.167 | 20 | 200 | fits | 160,381 | 214 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 468,355 | 4.684 | 20 | 200 | fits | 152,270 | 192 | 0.365 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 317,625 | 3.176 | 20 | 20 | fits | 160,381 | 214 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 469,059 | 4.691 | 20 | 20 | fits | 152,270 | 192 | 0.365 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 151,017 | 1.510 | 20 | 24 | fits | 154,462 | 165 | 0.311 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if1` | 320,275 | 3.203 | 20 | 24 | fits | 160,381 | 214 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 320,209 | 3.202 | 20 | 50 | fits | 160,381 | 214 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 472,083 | 4.721 | 20 | 50 | fits | 152,270 | 192 | 0.365 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 591,795 | 5.918 | 20 | 20 | fits | 119,778 | 37 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if1` | 917,709 | 9.177 | 20 | 20 | fits | 83,705 | 35 | 0.672 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 371,711 | 3.717 | 20 | 20 | fits | 148,509 | 186 | 0.344 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 308,592 | 3.086 | 20 | 200 | fits | 160,328 | 214 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 456,485 | 4.565 | 20 | 200 | fits | 148,509 | 186 | 0.344 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 309,516 | 3.095 | 20 | 20 | fits | 160,328 | 214 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 457,189 | 4.572 | 20 | 20 | fits | 148,509 | 186 | 0.344 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 152,828 | 1.528 | 20 | 24 | fits | 156,138 | 169 | 0.321 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if1` | 312,166 | 3.122 | 20 | 24 | fits | 160,328 | 214 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 312,100 | 3.121 | 20 | 50 | fits | 160,328 | 214 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 460,213 | 4.602 | 20 | 50 | fits | 148,509 | 186 | 0.344 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 579,501 | 5.795 | 20 | 20 | fits | 119,354 | 37 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if1` | 1,004,371 | 10.044 | 20 | 20 | fits | 91,928 | 39 | 0.661 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 390,353 | 3.904 | 20 | 20 | fits | 148,574 | 186 | 0.344 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 327,169 | 3.272 | 20 | 200 | fits | 159,219 | 209 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 475,127 | 4.751 | 20 | 200 | fits | 148,574 | 186 | 0.344 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 328,093 | 3.281 | 20 | 20 | fits | 159,219 | 209 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 475,831 | 4.758 | 20 | 20 | fits | 148,574 | 186 | 0.344 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 172,514 | 1.725 | 20 | 24 | fits | 154,093 | 164 | 0.307 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if1` | 330,743 | 3.307 | 20 | 24 | fits | 159,219 | 209 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 330,677 | 3.307 | 20 | 50 | fits | 159,219 | 209 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 478,855 | 4.789 | 20 | 50 | fits | 148,574 | 186 | 0.344 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 598,115 | 5.981 | 20 | 20 | fits | 119,326 | 37 | 0.714 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if1` | 1,023,157 | 10.232 | 20 | 20 | fits | 94,335 | 37 | 0.566 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 393,324 | 3.933 | 20 | 20 | fits | 148,509 | 186 | 0.344 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 330,205 | 3.302 | 20 | 200 | fits | 159,326 | 209 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 478,098 | 4.781 | 20 | 200 | fits | 148,509 | 186 | 0.344 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 331,129 | 3.311 | 20 | 20 | fits | 159,326 | 209 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 478,802 | 4.788 | 20 | 20 | fits | 148,509 | 186 | 0.344 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 175,443 | 1.754 | 20 | 24 | fits | 154,093 | 164 | 0.307 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if1` | 333,779 | 3.338 | 20 | 24 | fits | 159,326 | 209 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 333,713 | 3.337 | 20 | 50 | fits | 159,326 | 209 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 481,826 | 4.818 | 20 | 50 | fits | 148,509 | 186 | 0.344 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 608,137 | 6.081 | 20 | 20 | fits | 126,377 | 44 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if1` | 1,024,476 | 10.245 | 20 | 20 | fits | 85,351 | 33 | 0.581 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 391,996 | 3.920 | 20 | 20 | fits | 160,523 | 180 | 0.373 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 307,251 | 3.073 | 20 | 200 | fits | 159,681 | 225 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 467,158 | 4.672 | 20 | 200 | fits | 160,523 | 180 | 0.373 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 308,175 | 3.082 | 20 | 20 | fits | 159,681 | 225 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 467,862 | 4.679 | 20 | 20 | fits | 160,523 | 180 | 0.373 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 152,134 | 1.521 | 20 | 24 | fits | 154,093 | 164 | 0.307 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if1` | 310,825 | 3.108 | 20 | 24 | fits | 159,681 | 225 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 310,759 | 3.108 | 20 | 50 | fits | 159,681 | 225 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 470,886 | 4.709 | 20 | 50 | fits | 160,523 | 180 | 0.373 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 686,942 | 6.869 | 20 | 20 | fits | 124,168 | 43 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if1` | 1,004,404 | 10.044 | 20 | 20 | fits | 75,282 | 29 | 0.607 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 408,280 | 4.083 | 20 | 20 | fits | 163,916 | 185 | 0.398 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 309,607 | 3.096 | 20 | 200 | fits | 158,768 | 221 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 483,538 | 4.835 | 20 | 200 | fits | 163,916 | 185 | 0.398 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 310,531 | 3.105 | 20 | 20 | fits | 158,768 | 221 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 484,242 | 4.842 | 20 | 20 | fits | 163,916 | 185 | 0.398 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 155,403 | 1.554 | 20 | 24 | fits | 154,093 | 164 | 0.307 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if1` | 313,181 | 3.132 | 20 | 24 | fits | 158,768 | 221 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 313,115 | 3.131 | 20 | 50 | fits | 158,768 | 221 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 487,266 | 4.873 | 20 | 50 | fits | 163,916 | 185 | 0.398 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 688,242 | 6.882 | 20 | 20 | fits | 119,682 | 37 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if1` | 1,005,490 | 10.055 | 20 | 20 | fits | 75,282 | 29 | 0.607 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 489,841 | 4.898 | 20 | 20 | fits | 162,361 | 200 | 0.365 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 311,544 | 3.115 | 20 | 200 | fits | 157,776 | 204 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 564,939 | 5.649 | 20 | 200 | fits | 162,361 | 200 | 0.365 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 312,468 | 3.125 | 20 | 20 | fits | 157,776 | 204 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 565,643 | 5.656 | 20 | 20 | fits | 162,361 | 200 | 0.365 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 158,332 | 1.583 | 20 | 24 | fits | 154,093 | 164 | 0.307 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if1` | 315,118 | 3.151 | 20 | 24 | fits | 157,776 | 204 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 315,052 | 3.151 | 20 | 50 | fits | 157,776 | 204 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 568,667 | 5.687 | 20 | 50 | fits | 162,361 | 200 | 0.365 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 688,229 | 6.882 | 20 | 20 | fits | 119,628 | 37 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if1` | 1,005,559 | 10.056 | 20 | 20 | fits | 75,282 | 29 | 0.607 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 388,754 | 3.888 | 20 | 20 | fits | 149,870 | 190 | 0.335 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 305,606 | 3.056 | 20 | 200 | fits | 158,372 | 210 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 454,860 | 4.549 | 20 | 200 | fits | 149,870 | 190 | 0.335 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 306,530 | 3.065 | 20 | 20 | fits | 158,372 | 210 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 455,564 | 4.556 | 20 | 20 | fits | 149,870 | 190 | 0.335 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 151,798 | 1.518 | 20 | 24 | fits | 154,239 | 164 | 0.308 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if1` | 309,180 | 3.092 | 20 | 24 | fits | 158,372 | 210 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 309,114 | 3.091 | 20 | 50 | fits | 158,372 | 210 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 458,588 | 4.586 | 20 | 50 | fits | 149,870 | 190 | 0.335 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 593,483 | 5.935 | 20 | 20 | fits | 124,289 | 43 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if1` | 910,885 | 9.109 | 20 | 20 | fits | 75,279 | 29 | 0.607 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 395,972 | 3.960 | 20 | 20 | fits | 154,194 | 196 | 0.357 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 308,175 | 3.082 | 20 | 200 | fits | 157,455 | 205 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 461,753 | 4.618 | 20 | 200 | fits | 154,194 | 196 | 0.357 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 309,099 | 3.091 | 20 | 20 | fits | 157,455 | 205 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 462,457 | 4.625 | 20 | 20 | fits | 154,194 | 196 | 0.357 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 155,284 | 1.553 | 20 | 24 | fits | 154,310 | 164 | 0.309 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if1` | 311,749 | 3.117 | 20 | 24 | fits | 157,455 | 205 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 311,683 | 3.117 | 20 | 50 | fits | 157,455 | 205 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 465,481 | 4.655 | 20 | 50 | fits | 154,194 | 196 | 0.357 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 596,699 | 5.967 | 20 | 20 | fits | 120,418 | 37 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if1` | 922,335 | 9.223 | 20 | 20 | fits | 83,469 | 35 | 0.669 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 410,495 | 4.105 | 20 | 20 | fits | 154,872 | 195 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 311,904 | 3.119 | 20 | 200 | fits | 157,475 | 206 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 476,897 | 4.769 | 20 | 200 | fits | 154,872 | 195 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 312,828 | 3.128 | 20 | 20 | fits | 157,475 | 206 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 477,601 | 4.776 | 20 | 20 | fits | 154,872 | 195 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 158,993 | 1.590 | 20 | 24 | fits | 154,310 | 164 | 0.309 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if1` | 315,478 | 3.155 | 20 | 24 | fits | 157,475 | 206 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 315,412 | 3.154 | 20 | 50 | fits | 157,475 | 206 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 480,625 | 4.806 | 20 | 50 | fits | 154,872 | 195 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 599,977 | 6.000 | 20 | 20 | fits | 119,418 | 37 | 0.714 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if1` | 926,111 | 9.261 | 20 | 20 | fits | 85,658 | 33 | 0.586 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 409,780 | 4.098 | 20 | 20 | fits | 150,213 | 189 | 0.340 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 326,246 | 3.262 | 20 | 200 | fits | 158,444 | 210 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 475,843 | 4.758 | 20 | 200 | fits | 150,213 | 189 | 0.340 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 327,170 | 3.272 | 20 | 20 | fits | 158,444 | 210 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 476,547 | 4.765 | 20 | 20 | fits | 150,213 | 189 | 0.340 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 162,520 | 1.625 | 20 | 24 | fits | 154,351 | 165 | 0.310 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if1` | 329,820 | 3.298 | 20 | 24 | fits | 158,444 | 210 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 329,754 | 3.298 | 20 | 50 | fits | 158,444 | 210 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 479,571 | 4.796 | 20 | 50 | fits | 150,213 | 189 | 0.340 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 599,011 | 5.990 | 20 | 20 | fits | 119,506 | 37 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if1` | 924,367 | 9.244 | 20 | 20 | fits | 85,271 | 33 | 0.578 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 390,983 | 3.910 | 20 | 20 | fits | 148,371 | 186 | 0.336 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 311,160 | 3.112 | 20 | 200 | fits | 159,241 | 209 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 458,915 | 4.589 | 20 | 200 | fits | 148,371 | 186 | 0.336 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 312,084 | 3.121 | 20 | 20 | fits | 159,241 | 209 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 459,619 | 4.596 | 20 | 20 | fits | 148,371 | 186 | 0.336 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 156,483 | 1.565 | 20 | 24 | fits | 154,446 | 164 | 0.312 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if1` | 314,734 | 3.147 | 20 | 24 | fits | 159,241 | 209 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 314,668 | 3.147 | 20 | 50 | fits | 159,241 | 209 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 462,643 | 4.626 | 20 | 50 | fits | 148,371 | 186 | 0.336 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 588,671 | 5.887 | 20 | 20 | fits | 126,094 | 43 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if1` | 924,568 | 9.246 | 20 | 20 | fits | 82,213 | 35 | 0.689 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 403,743 | 4.037 | 20 | 20 | fits | 157,391 | 187 | 0.378 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 313,629 | 3.136 | 20 | 200 | fits | 159,009 | 209 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 470,404 | 4.704 | 20 | 200 | fits | 157,391 | 187 | 0.378 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 314,553 | 3.146 | 20 | 20 | fits | 159,009 | 209 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 471,108 | 4.711 | 20 | 20 | fits | 157,391 | 187 | 0.378 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 159,184 | 1.592 | 20 | 24 | fits | 154,150 | 164 | 0.308 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if1` | 317,203 | 3.172 | 20 | 24 | fits | 159,009 | 209 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 317,137 | 3.171 | 20 | 50 | fits | 159,009 | 209 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 474,132 | 4.741 | 20 | 50 | fits | 157,391 | 187 | 0.378 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 593,586 | 5.936 | 20 | 20 | fits | 119,520 | 37 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if1` | 930,284 | 9.303 | 20 | 20 | fits | 85,979 | 33 | 0.596 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 406,980 | 4.070 | 20 | 20 | fits | 157,456 | 187 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 316,801 | 3.168 | 20 | 200 | fits | 159,292 | 209 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 473,641 | 4.736 | 20 | 200 | fits | 157,456 | 187 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 317,725 | 3.177 | 20 | 20 | fits | 159,292 | 209 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 474,345 | 4.743 | 20 | 20 | fits | 157,456 | 187 | 0.379 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 162,073 | 1.621 | 20 | 24 | fits | 154,150 | 164 | 0.308 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if1` | 320,375 | 3.204 | 20 | 24 | fits | 159,292 | 209 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 320,309 | 3.203 | 20 | 50 | fits | 159,292 | 209 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 477,369 | 4.774 | 20 | 50 | fits | 157,456 | 187 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 596,913 | 5.969 | 20 | 20 | fits | 119,610 | 38 | 0.714 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if1` | 933,065 | 9.331 | 20 | 20 | fits | 85,348 | 33 | 0.581 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 408,122 | 4.081 | 20 | 20 | fits | 157,510 | 194 | 0.323 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 317,517 | 3.175 | 20 | 200 | fits | 157,342 | 203 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 474,411 | 4.744 | 20 | 200 | fits | 157,510 | 194 | 0.323 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 318,441 | 3.184 | 20 | 20 | fits | 157,342 | 203 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 475,115 | 4.751 | 20 | 20 | fits | 157,510 | 194 | 0.323 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 164,739 | 1.647 | 20 | 24 | fits | 154,150 | 164 | 0.308 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if1` | 321,091 | 3.211 | 20 | 24 | fits | 157,342 | 203 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 321,025 | 3.210 | 20 | 50 | fits | 157,342 | 203 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 478,139 | 4.781 | 20 | 50 | fits | 157,510 | 194 | 0.323 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 613,009 | 6.130 | 20 | 20 | fits | 124,274 | 43 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if1` | 930,414 | 9.304 | 20 | 20 | fits | 75,279 | 29 | 0.607 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 420,432 | 4.204 | 20 | 20 | fits | 148,430 | 186 | 0.337 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 340,594 | 3.406 | 20 | 200 | fits | 160,460 | 214 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 488,408 | 4.884 | 20 | 200 | fits | 148,430 | 186 | 0.337 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 341,518 | 3.415 | 20 | 20 | fits | 160,460 | 214 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 489,112 | 4.891 | 20 | 20 | fits | 148,430 | 186 | 0.337 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 174,782 | 1.748 | 20 | 24 | fits | 154,144 | 165 | 0.309 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if1` | 344,168 | 3.442 | 20 | 24 | fits | 160,460 | 214 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 344,102 | 3.441 | 20 | 50 | fits | 160,460 | 214 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 492,136 | 4.921 | 20 | 50 | fits | 148,430 | 186 | 0.337 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 611,808 | 6.118 | 20 | 20 | fits | 119,738 | 37 | 0.714 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if1` | 929,440 | 9.294 | 20 | 20 | fits | 75,388 | 29 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 386,626 | 3.866 | 20 | 20 | fits | 148,466 | 186 | 0.344 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 323,550 | 3.236 | 20 | 200 | fits | 159,318 | 209 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 471,400 | 4.714 | 20 | 200 | fits | 148,466 | 186 | 0.344 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 324,474 | 3.245 | 20 | 20 | fits | 159,318 | 209 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 472,104 | 4.721 | 20 | 20 | fits | 148,466 | 186 | 0.344 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 168,796 | 1.688 | 20 | 24 | fits | 154,123 | 164 | 0.309 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if1` | 327,124 | 3.271 | 20 | 24 | fits | 159,318 | 209 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 327,058 | 3.271 | 20 | 50 | fits | 159,318 | 209 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 475,128 | 4.751 | 20 | 50 | fits | 148,466 | 186 | 0.344 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 594,862 | 5.949 | 20 | 20 | fits | 119,800 | 37 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if1` | 939,947 | 9.399 | 20 | 20 | fits | 95,716 | 39 | 0.674 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 389,680 | 3.897 | 20 | 20 | fits | 148,531 | 186 | 0.345 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 326,539 | 3.265 | 20 | 200 | fits | 159,601 | 209 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 474,454 | 4.745 | 20 | 200 | fits | 148,531 | 186 | 0.345 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 327,463 | 3.275 | 20 | 20 | fits | 159,601 | 209 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 475,158 | 4.752 | 20 | 20 | fits | 148,531 | 186 | 0.345 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 171,502 | 1.715 | 20 | 24 | fits | 154,069 | 164 | 0.308 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if1` | 330,113 | 3.301 | 20 | 24 | fits | 159,601 | 209 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 330,047 | 3.300 | 20 | 50 | fits | 159,601 | 209 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 478,182 | 4.782 | 20 | 50 | fits | 148,531 | 186 | 0.345 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 597,916 | 5.979 | 20 | 20 | fits | 119,800 | 37 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if1` | 1,022,452 | 10.225 | 20 | 20 | fits | 95,222 | 37 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 392,261 | 3.923 | 20 | 20 | fits | 148,553 | 187 | 0.345 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 329,185 | 3.292 | 20 | 200 | fits | 159,318 | 209 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 477,122 | 4.771 | 20 | 200 | fits | 148,553 | 187 | 0.345 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 330,109 | 3.301 | 20 | 20 | fits | 159,318 | 209 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 477,826 | 4.778 | 20 | 20 | fits | 148,553 | 187 | 0.345 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 174,431 | 1.744 | 20 | 24 | fits | 154,069 | 164 | 0.308 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if1` | 332,759 | 3.328 | 20 | 24 | fits | 159,318 | 209 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 332,693 | 3.327 | 20 | 50 | fits | 159,318 | 209 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 480,850 | 4.809 | 20 | 50 | fits | 148,553 | 187 | 0.345 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 616,117 | 6.161 | 20 | 20 | fits | 124,831 | 43 | 0.733 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if1` | 1,021,319 | 10.213 | 20 | 20 | fits | 85,443 | 33 | 0.585 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 381,157 | 3.812 | 20 | 20 | fits | 151,203 | 178 | 0.331 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 306,687 | 3.067 | 20 | 200 | fits | 159,566 | 225 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 457,274 | 4.573 | 20 | 200 | fits | 151,203 | 178 | 0.331 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 307,611 | 3.076 | 20 | 20 | fits | 159,566 | 225 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 457,978 | 4.580 | 20 | 20 | fits | 151,203 | 178 | 0.331 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 151,685 | 1.517 | 20 | 24 | fits | 154,069 | 164 | 0.308 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if1` | 310,261 | 3.103 | 20 | 24 | fits | 159,566 | 225 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 310,195 | 3.102 | 20 | 50 | fits | 159,566 | 225 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 461,002 | 4.610 | 20 | 50 | fits | 151,203 | 178 | 0.331 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 591,492 | 5.915 | 20 | 20 | fits | 120,054 | 45 | 0.753 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if1` | 998,505 | 9.985 | 20 | 20 | fits | 85,274 | 33 | 0.578 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 407,870 | 4.079 | 20 | 20 | fits | 155,221 | 178 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 308,870 | 3.089 | 20 | 200 | fits | 159,043 | 221 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 474,018 | 4.740 | 20 | 200 | fits | 155,221 | 178 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 309,794 | 3.098 | 20 | 20 | fits | 159,043 | 221 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 681,637 | 6.816 | 20 | 20 | fits | 128,355 | 44 | 0.693 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 154,391 | 1.544 | 20 | 24 | fits | 154,069 | 164 | 0.308 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if1` | 312,444 | 3.124 | 20 | 24 | fits | 159,043 | 221 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 312,378 | 3.124 | 20 | 50 | fits | 159,043 | 221 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 477,746 | 4.777 | 20 | 50 | fits | 155,221 | 178 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 684,595 | 6.846 | 20 | 20 | fits | 128,355 | 44 | 0.693 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if1` | 1,002,374 | 10.024 | 20 | 20 | fits | 75,282 | 29 | 0.607 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 407,365 | 4.074 | 20 | 20 | fits | 160,646 | 179 | 0.377 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 322,421 | 3.224 | 20 | 200 | fits | 159,800 | 225 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 482,451 | 4.825 | 20 | 200 | fits | 160,646 | 179 | 0.377 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 323,345 | 3.233 | 20 | 20 | fits | 159,800 | 225 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 483,155 | 4.832 | 20 | 20 | fits | 160,646 | 179 | 0.377 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 157,388 | 1.574 | 20 | 24 | fits | 154,137 | 165 | 0.309 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if1` | 325,995 | 3.260 | 20 | 24 | fits | 159,800 | 225 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 325,929 | 3.259 | 20 | 50 | fits | 159,800 | 225 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 486,179 | 4.862 | 20 | 50 | fits | 160,646 | 179 | 0.377 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 685,205 | 6.852 | 20 | 20 | fits | 120,533 | 37 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if1` | 1,020,744 | 10.207 | 20 | 20 | fits | 81,964 | 35 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 488,583 | 4.886 | 20 | 20 | fits | 157,932 | 194 | 0.324 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 327,886 | 3.279 | 20 | 200 | fits | 157,460 | 203 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 563,850 | 5.638 | 20 | 200 | fits | 157,932 | 194 | 0.324 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 328,810 | 3.288 | 20 | 20 | fits | 157,460 | 203 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 564,554 | 5.646 | 20 | 20 | fits | 157,932 | 194 | 0.324 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 174,990 | 1.750 | 20 | 24 | fits | 154,105 | 164 | 0.309 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if1` | 331,460 | 3.315 | 20 | 24 | fits | 157,460 | 203 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 331,394 | 3.314 | 20 | 50 | fits | 157,460 | 203 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 567,578 | 5.676 | 20 | 50 | fits | 157,932 | 194 | 0.324 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 687,216 | 6.872 | 20 | 20 | fits | 119,704 | 37 | 0.713 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if1` | 1,023,565 | 10.236 | 20 | 20 | fits | 85,634 | 33 | 0.588 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 408,635 | 4.086 | 20 | 20 | fits | 154,807 | 195 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 310,132 | 3.101 | 20 | 200 | fits | 157,401 | 206 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 475,037 | 4.750 | 20 | 200 | fits | 154,807 | 195 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 311,056 | 3.111 | 20 | 20 | fits | 157,401 | 206 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 475,741 | 4.757 | 20 | 20 | fits | 154,807 | 195 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 157,295 | 1.573 | 20 | 24 | fits | 154,059 | 164 | 0.307 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if1` | 313,706 | 3.137 | 20 | 24 | fits | 157,401 | 206 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 313,640 | 3.136 | 20 | 50 | fits | 157,401 | 206 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 478,765 | 4.788 | 20 | 50 | fits | 154,807 | 195 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 598,591 | 5.986 | 20 | 20 | fits | 119,892 | 37 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if1` | 915,953 | 9.160 | 20 | 20 | fits | 75,279 | 29 | 0.607 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 407,426 | 4.074 | 20 | 20 | fits | 150,118 | 189 | 0.339 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 323,987 | 3.240 | 20 | 200 | fits | 158,444 | 210 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 473,489 | 4.735 | 20 | 200 | fits | 150,118 | 189 | 0.339 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 324,911 | 3.249 | 20 | 20 | fits | 158,444 | 210 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 474,193 | 4.742 | 20 | 20 | fits | 150,118 | 189 | 0.339 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 160,310 | 1.603 | 20 | 24 | fits | 154,216 | 165 | 0.309 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if1` | 327,561 | 3.276 | 20 | 24 | fits | 158,444 | 210 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 327,495 | 3.275 | 20 | 50 | fits | 158,444 | 210 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 477,217 | 4.772 | 20 | 50 | fits | 150,118 | 189 | 0.339 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 597,131 | 5.971 | 20 | 20 | fits | 119,980 | 37 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if1` | 922,779 | 9.228 | 20 | 20 | fits | 83,618 | 35 | 0.671 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 389,458 | 3.895 | 20 | 20 | fits | 149,783 | 189 | 0.335 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 306,310 | 3.063 | 20 | 200 | fits | 158,026 | 210 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 455,477 | 4.555 | 20 | 200 | fits | 149,783 | 189 | 0.335 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 307,234 | 3.072 | 20 | 20 | fits | 158,026 | 210 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 456,181 | 4.562 | 20 | 20 | fits | 149,783 | 189 | 0.335 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 152,848 | 1.528 | 20 | 24 | fits | 156,158 | 169 | 0.323 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if1` | 309,884 | 3.099 | 20 | 24 | fits | 158,026 | 210 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 309,818 | 3.098 | 20 | 50 | fits | 158,026 | 210 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 459,205 | 4.592 | 20 | 50 | fits | 149,783 | 189 | 0.335 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 579,059 | 5.791 | 20 | 20 | fits | 119,920 | 37 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if1` | 922,941 | 9.229 | 20 | 20 | fits | 91,783 | 39 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 389,850 | 3.898 | 20 | 20 | fits | 148,297 | 186 | 0.335 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 310,101 | 3.101 | 20 | 200 | fits | 158,868 | 209 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 457,782 | 4.578 | 20 | 200 | fits | 148,297 | 186 | 0.335 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 311,025 | 3.110 | 20 | 20 | fits | 158,868 | 209 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 458,486 | 4.585 | 20 | 20 | fits | 148,297 | 186 | 0.335 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 155,797 | 1.558 | 20 | 24 | fits | 154,069 | 164 | 0.308 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if1` | 313,675 | 3.137 | 20 | 24 | fits | 158,868 | 209 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 313,609 | 3.136 | 20 | 50 | fits | 158,868 | 209 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 461,510 | 4.615 | 20 | 50 | fits | 148,297 | 186 | 0.335 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 581,094 | 5.811 | 20 | 20 | fits | 119,650 | 37 | 0.713 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if1` | 925,415 | 9.254 | 20 | 20 | fits | 94,472 | 37 | 0.571 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 392,636 | 3.926 | 20 | 20 | fits | 148,232 | 186 | 0.334 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 312,952 | 3.130 | 20 | 200 | fits | 159,013 | 209 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 460,568 | 4.606 | 20 | 200 | fits | 148,232 | 186 | 0.334 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 313,876 | 3.139 | 20 | 20 | fits | 159,013 | 209 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 461,272 | 4.613 | 20 | 20 | fits | 148,232 | 186 | 0.334 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 158,503 | 1.585 | 20 | 24 | fits | 154,069 | 164 | 0.308 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if1` | 316,526 | 3.165 | 20 | 24 | fits | 159,013 | 209 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 316,460 | 3.165 | 20 | 50 | fits | 159,013 | 209 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 464,296 | 4.643 | 20 | 50 | fits | 148,232 | 186 | 0.334 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 590,959 | 5.910 | 20 | 20 | fits | 126,729 | 44 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if1` | 926,894 | 9.269 | 20 | 20 | fits | 85,348 | 33 | 0.581 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 405,885 | 4.059 | 20 | 20 | fits | 157,546 | 188 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 315,736 | 3.157 | 20 | 200 | fits | 158,868 | 209 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 472,666 | 4.727 | 20 | 200 | fits | 157,546 | 188 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 316,660 | 3.167 | 20 | 20 | fits | 158,868 | 209 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 473,370 | 4.734 | 20 | 20 | fits | 157,546 | 188 | 0.379 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 161,432 | 1.614 | 20 | 24 | fits | 154,069 | 164 | 0.308 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if1` | 319,310 | 3.193 | 20 | 24 | fits | 158,868 | 209 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 319,244 | 3.192 | 20 | 50 | fits | 158,868 | 209 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 476,394 | 4.764 | 20 | 50 | fits | 157,546 | 188 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 611,909 | 6.119 | 20 | 20 | fits | 124,589 | 43 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if1` | 930,003 | 9.300 | 20 | 20 | fits | 75,388 | 29 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 422,909 | 4.229 | 20 | 20 | fits | 161,168 | 193 | 0.407 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 318,751 | 3.188 | 20 | 200 | fits | 159,177 | 210 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 489,870 | 4.899 | 20 | 200 | fits | 161,168 | 193 | 0.407 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 319,675 | 3.197 | 20 | 20 | fits | 159,177 | 210 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 490,574 | 4.906 | 20 | 20 | fits | 161,168 | 193 | 0.407 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 164,138 | 1.641 | 20 | 24 | fits | 154,069 | 164 | 0.308 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if1` | 322,325 | 3.223 | 20 | 24 | fits | 159,177 | 210 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 322,259 | 3.223 | 20 | 50 | fits | 159,177 | 210 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 493,598 | 4.936 | 20 | 50 | fits | 161,168 | 193 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 613,385 | 6.134 | 20 | 20 | fits | 119,853 | 37 | 0.714 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if1` | 931,077 | 9.311 | 20 | 20 | fits | 75,388 | 29 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 425,772 | 4.258 | 20 | 20 | fits | 162,413 | 199 | 0.368 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 319,759 | 3.198 | 20 | 200 | fits | 157,256 | 204 | 0.402 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 492,357 | 4.924 | 20 | 200 | fits | 162,413 | 199 | 0.368 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 320,683 | 3.207 | 20 | 20 | fits | 157,256 | 204 | 0.402 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 493,061 | 4.931 | 20 | 20 | fits | 162,413 | 199 | 0.368 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 167,067 | 1.671 | 20 | 24 | fits | 154,069 | 164 | 0.308 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if1` | 323,333 | 3.233 | 20 | 24 | fits | 157,256 | 204 | 0.402 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 323,267 | 3.233 | 20 | 50 | fits | 157,256 | 204 | 0.402 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 496,085 | 4.961 | 20 | 50 | fits | 162,413 | 199 | 0.368 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 615,964 | 6.160 | 20 | 20 | fits | 119,945 | 37 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if1` | 933,305 | 9.333 | 20 | 20 | fits | 75,279 | 29 | 0.607 |
| LINK_UP | `adp.link_up.if0` | 3,223 | 0.032 | 20 | 200 | fits | 54,010 | 79 (11) | 0.657 |
| LINK_UP | `adp.link_up.if1` | 19,933 | 0.199 | 20 | 200 | fits | 54,010 | 79 (11) | 0.657 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,059 | 0.151 | 20 | 200 | fits | 35,745 | 39 (39) | 0.644 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 9,936 | 0.099 | 20 | 200 | fits | 35,745 | 39 (39) | 0.644 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 25,551 | 0.256 | 20 | 200 | fits | 5,483 | 19 (11) | 0.533 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 23,181 | 0.232 | 20 | 200 | fits | 5,483 | 19 (11) | 0.533 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 16,661 | 0.167 | 20 | 50 | fits | 41,270 | 44 | 0.735 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 29,724 | 0.297 | 20 | 50 | fits | 38,585 | 36 | 0.724 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 27,416 | 0.274 | 20 | 50 | fits | 38,362 | 36 | 0.722 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 36,840 | 0.368 | 20 | 50 | fits | 48,198 | 68 | 0.623 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 39,229 | 0.392 | 20 | 50 | fits | 48,198 | 68 | 0.623 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 11,233 | 0.112 | 20 | 50 | fits | 32,326 | 31 | 0.639 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 15,122 | 0.151 | 20 | 50 | fits | 39,749 | 44 | 0.729 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 16,466 | 0.165 | 20 | 50 | fits | 37,513 | 37 | 0.717 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 30,327 | 0.303 | 20 | 50 | fits | 36,448 | 36 | 0.706 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 21,708 | 0.217 | 20 | 50 | fits | 42,315 | 62 | 0.647 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 23,587 | 0.236 | 20 | 50 | fits | 42,315 | 62 | 0.647 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 11,324 | 0.113 | 20 | 50 | fits | 32,614 | 31 | 0.639 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 12,021 | 0.120 | 20 | 20 | fits | 53,143 | 42 (35) | 0.745 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 23,594 | 0.236 | 20 | 20 | fits | 53,143 | 42 (35) | 0.745 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 33,070 | 0.331 | 20 | 20 | fits | 50,370 | 38 (14) | 0.809 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 42,223 | 0.422 | 20 | 20 | fits | 50,370 | 38 (14) | 0.809 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 34,210 | 0.342 | 20 | 20 | fits | 49,355 | 39 (14) | 0.809 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 42,891 | 0.429 | 20 | 20 | fits | 49,355 | 39 (14) | 0.809 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 22,243 | 0.222 | 20 | 20 | fits | 46,036 | 28 (35) | 0.814 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 33,480 | 0.335 | 20 | 20 | fits | 41,098 | 22 (35) | 0.824 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 89,589 | 0.896 | 20 | 20 | fits | 26,693 | 8 | 0.797 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 84,689 | 0.847 | 20 | 20 | fits | 25,472 | 8 | 0.789 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 52,010 | 0.520 | 20 | 20 | fits | 52,076 | 13 | 0.886 |
| malformed MRPDU discard | `srp.malformed.if0` | 29,934 | 0.299 | 20 | 20 | fits | 30,000 | 13 | 0.726 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 90,245 | 0.902 | 220 | 220 | fits | 47,758 | 6 | 0.920 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 48,386 | 0.484 | 20 | 20 | fits | 48,452 | 13 | 0.876 |
| malformed MRPDU discard | `srp.malformed.if1` | 28,897 | 0.289 | 20 | 20 | fits | 28,963 | 13 | 0.717 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 89,425 | 0.894 | 220 | 220 | fits | 48,811 | 6 | 0.917 |
| an event behind 15 others | `backlog.event.if0` | 174,550 | 1.746 | 20 | 200 | fits | 68,561 | 81 | 0.621 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 502,926 | 5.029 | 20 | 20 | fits | 120,310 | 83 | 0.506 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 461,466 | 4.615 | 20 | 200 | fits | 160,856 | 172 | 0.403 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 581,160 | 5.812 | 20 | 200 | fits | 120,310 | 83 | 0.506 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 457,144 | 4.571 | 20 | 20 | fits | 160,856 | 172 | 0.403 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 576,618 | 5.766 | 20 | 20 | fits | 120,310 | 83 | 0.506 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 161,637 | 1.616 | 20 | 24 | fits | 162,528 | 173 | 0.334 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 459,794 | 4.598 | 20 | 24 | fits | 160,856 | 172 | 0.403 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 459,728 | 4.597 | 20 | 50 | fits | 160,856 | 172 | 0.403 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 459,332 | 4.593 | 20 | 50 | fits | 160,856 | 172 | 0.403 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 579,576 | 5.796 | 20 | 20 | fits | 120,310 | 83 | 0.506 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 804,073 | 8.041 | 20 | 20 | fits | 46,676 | 23 | 0.777 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 403,614 | 4.036 | 20 | 20 | fits | 160,056 | 179 | 0.377 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 319,187 | 3.192 | 20 | 200 | fits | 159,255 | 225 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 478,627 | 4.786 | 20 | 200 | fits | 160,056 | 179 | 0.377 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 320,111 | 3.201 | 20 | 20 | fits | 159,255 | 225 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 479,331 | 4.793 | 20 | 20 | fits | 160,056 | 179 | 0.377 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 154,648 | 1.546 | 20 | 24 | fits | 154,834 | 171 | 0.313 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 322,761 | 3.228 | 20 | 24 | fits | 159,255 | 225 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 322,695 | 3.227 | 20 | 50 | fits | 159,255 | 225 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 482,355 | 4.824 | 20 | 50 | fits | 160,056 | 179 | 0.377 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 602,206 | 6.022 | 20 | 20 | fits | 119,917 | 37 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 919,485 | 9.195 | 20 | 20 | fits | 75,277 | 29 | 0.607 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 13,992 | 0.140 | 20 | 20 | fits | 36,823 | 20 | 0.795 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 319,187 | 3.192 | 20 | 200 | fits | 159,255 | 225 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 41,070 | 0.411 | 20 | 200 | fits | 36,823 | 20 | 0.795 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 320,111 | 3.201 | 20 | 20 | fits | 159,255 | 225 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 468,561 | 4.686 | 20 | 20 | fits | 149,286 | 173 | 0.326 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 154,648 | 1.546 | 20 | 24 | fits | 154,834 | 171 | 0.313 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 322,761 | 3.228 | 20 | 24 | fits | 159,255 | 225 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 322,695 | 3.227 | 20 | 50 | fits | 159,255 | 225 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 471,585 | 4.716 | 20 | 50 | fits | 149,286 | 173 | 0.326 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 590,870 | 5.909 | 20 | 20 | fits | 119,351 | 37 | 0.712 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 908,104 | 9.081 | 20 | 20 | fits | 75,277 | 29 | 0.607 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,371,838 | 63.718 | 20 | 20 | MISS ceiling | 34,586 | 19 | 0.746 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,398,850 | 63.989 | 20 | 20 | MISS ceiling | 29,756 | 14 | 0.595 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,428,764 | 64.288 | 20 | 20 | MISS ceiling | 29,101 | 14 | 0.671 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,457,527 | 64.575 | 20 | 20 | MISS ceiling | 28,352 | 14 | 0.654 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,485,808 | 64.858 | 20 | 20 | MISS ceiling | 28,265 | 14 | 0.641 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 179,629 | 1.796 | 20 | 200 | fits | 162,100 | 209 | 0.413 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 305,577 | 3.056 | 20 | 200 | fits | 126,564 | 187 | 0.361 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 175,307 | 1.753 | 20 | 20 | fits | 162,100 | 209 | 0.413 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,235,571 | 62.356 | 20 | 20 | MISS ceiling | 39,817 | 16 | 0.717 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 178,947 | 1.789 | 20 | 24 | fits | 162,100 | 209 | 0.413 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,199,240 | 61.992 | 20 | 24 | MISS ceiling | 147,052 | 117 | 0.336 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 177,891 | 1.779 | 20 | 50 | fits | 162,100 | 209 | 0.413 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 304,059 | 3.041 | 20 | 50 | fits | 126,564 | 187 | 0.361 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 423,137 | 4.231 | 20 | 20 | fits | 119,144 | 37 | 0.703 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 747,282 | 7.473 | 20 | 20 | fits | 84,681 | 33 | 0.563 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 7,562 | 0.076 | 20 | 20 | fits | 44,308 | 21 (29) | 0.687 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 14,951 | 0.150 | 20 | 20 | fits | 44,308 | 21 (29) | 0.687 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 8,494 | 0.085 | 20 | 20 | fits | 46,542 | 32 (35) | 0.682 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 16,326 | 0.163 | 20 | 20 | fits | 46,542 | 32 (35) | 0.682 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 24,449 | 0.244 | 20 | 20 | fits | 45,799 | 25 (12) | 0.844 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 36,046 | 0.360 | 20 | 20 | fits | 46,074 | 33 (12) | 0.819 |
| LINK_UP | `adp.link_up.if0` | 3,223 | 0.032 | 20 | 200 | fits | 54,010 | 79 (11) | 0.657 |
| LINK_UP | `adp.link_up.if1` | 19,933 | 0.199 | 20 | 200 | fits | 54,010 | 79 (11) | 0.657 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,059 | 0.151 | 20 | 200 | fits | 35,745 | 39 (39) | 0.644 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 9,936 | 0.099 | 20 | 200 | fits | 35,745 | 39 (39) | 0.644 |
| LINK_DOWN | `adp.link_down.if0` | 2,908 | 0.029 | 20 | 200 | fits | 54,912 | 39 (9) | 0.719 |
| LINK_DOWN | `adp.link_down.if1` | 21,052 | 0.211 | 20 | 200 | fits | 54,912 | 39 (9) | 0.719 |
| LINK_UP | `adp.link_up.if0` | 3,223 | 0.032 | 20 | 200 | fits | 54,010 | 79 (11) | 0.657 |
| LINK_UP | `adp.link_up.if1` | 19,933 | 0.199 | 20 | 200 | fits | 54,010 | 79 (11) | 0.657 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,059 | 0.151 | 20 | 200 | fits | 35,745 | 39 (39) | 0.644 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 9,936 | 0.099 | 20 | 200 | fits | 35,745 | 39 (39) | 0.644 |
| GM_CHANGE | `adp.gm_change.if0` | 2,917 | 0.029 | 20 | 200 | fits | 27,425 | 27 (11) | 0.690 |
| GM_CHANGE | `adp.gm_change.if1` | 4,873 | 0.049 | 20 | 200 | fits | 27,425 | 27 (11) | 0.690 |
| LINK_UP | `adp.link_up.if0` | 3,223 | 0.032 | 20 | 200 | fits | 54,010 | 79 (11) | 0.657 |
| LINK_UP | `adp.link_up.if1` | 19,933 | 0.199 | 20 | 200 | fits | 54,010 | 79 (11) | 0.657 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,059 | 0.151 | 20 | 200 | fits | 35,745 | 39 (39) | 0.644 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 9,936 | 0.099 | 20 | 200 | fits | 35,745 | 39 (39) | 0.644 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 5,328 | 0.053 | 20 | 200 | fits | 29,235 | 27 (31) | 0.500 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 7,115 | 0.071 | 20 | 200 | fits | 29,235 | 27 (31) | 0.500 |
| LINK_UP | `adp.link_up.if0` | 3,223 | 0.032 | 20 | 200 | fits | 54,010 | 79 (11) | 0.657 |
| LINK_UP | `adp.link_up.if1` | 19,933 | 0.199 | 20 | 200 | fits | 54,010 | 79 (11) | 0.657 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,059 | 0.151 | 20 | 200 | fits | 35,745 | 39 (39) | 0.644 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 9,936 | 0.099 | 20 | 200 | fits | 35,745 | 39 (39) | 0.644 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 5,328 | 0.053 | 20 | 200 | fits | 24,715 | 17 (31) | 0.617 |
| set_name | `aecp_fanout.set_name.if0` | 71,033 | 0.710 | 20 | 24 | fits | 78,204 | 160 | 0.430 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 69,543 | 0.695 | 20 | 24 | fits | 73,879 | 140 | 0.464 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 73,055 | 0.731 | 20 | 24 | fits | 68,334 | 140 | 0.424 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 72,514 | 0.725 | 20 | 24 | fits | 68,566 | 140 | 0.418 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 68,570 | 0.686 | 20 | 24 | fits | 72,365 | 116 | 0.463 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 73,255 | 0.733 | 20 | 24 | fits | 68,388 | 139 | 0.426 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 73,562 | 0.736 | 20 | 24 | fits | 68,489 | 140 | 0.427 |
| set_name | `aecp_fanout.set_name.if1` | 67,228 | 0.672 | 20 | 24 | fits | 71,349 | 117 | 0.428 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 75,562 | 0.756 | 20 | 24 | fits | 73,887 | 139 | 0.466 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 72,674 | 0.727 | 20 | 24 | fits | 68,008 | 140 | 0.421 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 66,260 | 0.663 | 20 | 24 | fits | 67,727 | 140 | 0.415 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 73,008 | 0.730 | 20 | 24 | fits | 68,435 | 140 | 0.425 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 73,461 | 0.735 | 20 | 24 | fits | 68,356 | 140 | 0.424 |
| BIND_RX | `acmp.bind_rx.if0` | 18,707 | 0.187 | 20 | 20 | fits | 50,521 | 27 (77) | 0.793 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 13,217 | 0.132 | 20 | 20 | fits | 43,953 | 27 (32) | 0.831 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 9,593 | 0.096 | 20 | 20 | fits | 33,405 | 16 (47) | 0.769 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 14,005 | 0.140 | 20 | 20 | fits | 47,124 | 19 (50) | 0.840 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 8,899 | 0.089 | 20 | 20 | fits | 33,470 | 18 (48) | 0.739 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 8,983 | 0.090 | 20 | 20 | fits | 32,654 | 17 (48) | 0.709 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 8,900 | 0.089 | 20 | 20 | fits | 32,822 | 17 (48) | 0.736 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 8,109 | 0.081 | 20 | 20 | fits | 31,471 | 17 (48) | 0.689 |
| BIND_RX | `acmp.bind_rx.if1` | 16,891 | 0.169 | 20 | 20 | fits | 48,591 | 28 (77) | 0.755 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 9,901 | 0.099 | 20 | 20 | fits | 40,429 | 21 (32) | 0.825 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 10,139 | 0.101 | 20 | 20 | fits | 34,124 | 17 (47) | 0.768 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 14,786 | 0.148 | 20 | 20 | fits | 49,145 | 20 (50) | 0.843 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if1` | 9,751 | 0.098 | 20 | 20 | fits | 33,783 | 20 (48) | 0.720 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 9,415 | 0.094 | 20 | 20 | fits | 32,861 | 18 (48) | 0.703 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 7,958 | 0.080 | 20 | 20 | fits | 31,850 | 18 (48) | 0.689 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if1` | 8,245 | 0.082 | 20 | 20 | fits | 32,261 | 18 (48) | 0.710 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 16,179 | 0.162 | 20 | 24 | fits | 35,685 | 22 | 0.794 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 29,738 | 0.297 | 20 | 24 | fits | 40,390 | 22 | 0.737 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 18,655 | 0.187 | 20 | 24 | fits | 36,220 | 22 | 0.759 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 18,443 | 0.184 | 20 | 24 | fits | 36,157 | 22 | 0.750 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 25,695 | 0.257 | 20 | 24 | fits | 36,204 | 22 | 0.750 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 18,932 | 0.189 | 20 | 24 | fits | 36,422 | 22 | 0.750 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 25,585 | 0.256 | 20 | 24 | fits | 35,616 | 22 | 0.754 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 25,513 | 0.255 | 20 | 24 | fits | 35,455 | 22 | 0.766 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 17,806 | 0.178 | 20 | 24 | fits | 35,217 | 22 | 0.766 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 30,110 | 0.301 | 20 | 24 | fits | 41,028 | 23 | 0.687 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 17,706 | 0.177 | 20 | 24 | fits | 35,111 | 22 | 0.784 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 17,649 | 0.176 | 20 | 24 | fits | 35,215 | 22 | 0.790 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 25,652 | 0.257 | 20 | 24 | fits | 35,831 | 22 | 0.758 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 18,847 | 0.188 | 20 | 24 | fits | 36,416 | 22 | 0.754 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 26,136 | 0.261 | 20 | 24 | fits | 36,475 | 22 | 0.760 |
| get_configuration | `aecp.get_configuration.if0` | 22,948 | 0.229 | 20 | 24 | fits | 32,626 | 22 | 0.762 |
| entity_available | `aecp.entity_available.if0` | 15,236 | 0.152 | 20 | 24 | fits | 32,251 | 22 | 0.752 |
| get_name | `aecp.get_name.if0` | 25,434 | 0.254 | 20 | 24 | fits | 35,562 | 22 | 0.769 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 19,512 | 0.195 | 20 | 24 | fits | 37,273 | 29 | 0.746 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 32,766 | 0.328 | 20 | 24 | fits | 37,457 | 31 | 0.782 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 23,734 | 0.237 | 20 | 24 | fits | 33,246 | 22 | 0.775 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 15,204 | 0.152 | 20 | 24 | fits | 32,046 | 22 | 0.748 |
| set_name | `aecp.set_name.if0` | 44,000 | 0.440 | 20 | 24 | fits | 52,328 | 65 | 0.712 |
| lock_entity | `aecp.lock_entity.if0` | 41,738 | 0.417 | 20 | 24 | fits | 43,391 | 47 | 0.754 |
| unlock_entity | `aecp.unlock_entity.if0` | 34,754 | 0.348 | 20 | 24 | fits | 43,127 | 46 | 0.755 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 25,022 | 0.250 | 20 | 24 | fits | 35,156 | 20 | 0.787 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 29,849 | 0.298 | 20 | 24 | fits | 46,683 | 26 | 0.740 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 20,358 | 0.204 | 20 | 24 | fits | 35,809 | 20 | 0.760 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 27,674 | 0.277 | 20 | 24 | fits | 35,739 | 20 | 0.750 |
| get_configuration | `aecp.get_configuration.if1` | 17,116 | 0.171 | 20 | 24 | fits | 32,041 | 20 | 0.757 |
| entity_available | `aecp.entity_available.if1` | 24,593 | 0.246 | 20 | 24 | fits | 32,242 | 20 | 0.760 |
| get_name | `aecp.get_name.if1` | 27,296 | 0.273 | 20 | 24 | fits | 35,074 | 20 | 0.768 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if1` | 21,105 | 0.211 | 20 | 24 | fits | 36,861 | 27 | 0.745 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if1` | 28,553 | 0.286 | 20 | 24 | fits | 36,669 | 29 | 0.777 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if1` | 17,824 | 0.178 | 20 | 24 | fits | 32,714 | 20 | 0.770 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 17,289 | 0.173 | 20 | 24 | fits | 32,210 | 20 | 0.760 |
| set_name | `aecp.set_name.if1` | 43,172 | 0.432 | 20 | 24 | fits | 46,600 | 25 | 0.777 |
| lock_entity | `aecp.lock_entity.if1` | 36,161 | 0.362 | 20 | 24 | fits | 43,844 | 49 | 0.738 |
| unlock_entity | `aecp.unlock_entity.if1` | 44,481 | 0.445 | 20 | 24 | fits | 44,079 | 49 | 0.738 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
