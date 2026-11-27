### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 127 paths and 7 of 1003 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.204 (0.460) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.087 (0.244) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.084 (0.273) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.070 (0.261) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.114 (0.277) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.090 (0.244) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.098 (0.257) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.111 (0.282) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.101 (0.317) | fits | 0 acmp | 1 | 0 |
| ACMP's last record of its burst at a registering triple | 0 | `acmp.register_burst.t0.if0` (srp-register-burst) | 3.040 (3.910) | fits | 11 acmp | 1 | 0 |
| ACMP's last record of its burst at a registering triple | 0 | `acmp.register_burst.t1.if0` (srp-register-burst) | 3.550 (4.589) | fits | 11 acmp | 1 | 0 |
| ACMP's last record of its burst at a registering triple | 0 | `acmp.register_burst.t2.if0` (srp-register-burst) | 1.255 (2.475) | fits | 11 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.153 (0.516) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.172 (0.537) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.254 (0.692) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.063 (0.432) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.109 (0.535) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.174 (0.526) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.144 (0.415) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.054 (0.178) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.022 (0.160) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.023 (0.330) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.032 (0.301) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.047 (0.215) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.126 (0.444) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.188 (0.525) | fits | 0 aecp | 1 | 0 |
| get_as_path | 0 | `aecp.get_as_path.if0` (aecp) | 0.266 (0.617) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.182 (0.522) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.158 (0.498) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.232 (0.579) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.185 (0.518) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR held for a token (#917) | 0 | `aecp.held.read_descriptor.if0` (aecp-held) | 5.231 (5.428) | fits | 15 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.219 (0.672) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.148 (0.474) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.340 (0.684) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.181 (0.517) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.175 (0.506) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.210 (0.551) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.252 (0.593) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.176 (0.523) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.206 (0.547) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.211 (0.553) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i79.c0.if0` (aecp) | 0.179 (0.510) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.213 (0.553) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.179 (0.512) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.211 (0.553) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.184 (0.517) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.209 (0.549) | fits | 0 aecp | 1 | 0 |
| AECP's last record of its burst at a registering triple | 0 | `aecp.register_burst.t0.if0` (srp-register-burst) | 3.943 (4.433) | fits | 15 aecp | 1 | 0 |
| AECP's last record of its burst at a registering triple | 0 | `aecp.register_burst.t1.if0` (srp-register-burst) | 5.044 (5.443) | fits | 15 aecp | 1 | 0 |
| AECP's last record of its burst at a registering triple | 0 | `aecp.register_burst.t2.if0` (srp-register-burst) | 5.041 (5.459) | fits | 15 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.142 (0.480) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.287 (0.762) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.190 (0.531) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.263 (0.667) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 3.295 (3.638) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 3.243 (3.589) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 0.972 (1.223) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.555 (0.871) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.624 (0.990) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 3.435 (3.783) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.552 (0.943) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 0.928 (1.298) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.555 (0.870) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.600 (0.973) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.057 (3.396) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 2.528 (2.882) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.549 (0.864) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 2.425 (2.773) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.318 (2.757) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.006 (3.420) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.332 (3.743) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.452 (1.822) | fits | 0 aecp | 1 | 0 |
| REBOOT | 0 | `aecp_reboot.accepted.if0` (aecp-reboot) | 0.464 (0.777) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | 0 | `aecp_reboot.entity_1.if0` (aecp-reboot) | 0.242 (0.640) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused ENTITY_LOCKED | 0 | `aecp_reboot.locked.if0` (aecp-reboot) | 0.233 (0.639) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused BAD_ARGUMENTS | 0 | `aecp_reboot.short.if0` (aecp-reboot) | 0.243 (0.642) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NOT_SUPPORTED | 0 | `aecp_reboot.stream_input.if0` (aecp-reboot) | 0.219 (0.609) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.135 (6.376) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-3.adp_available.if0` (backlog-adp@program-3) | 6.401 (7.844) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.118 (0.470) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.671 (2.318) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 64.021 (64.334) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.868 (65.181) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.345 (0.502) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-burst.held.acmp.if0` (save-burst) | 3.255 | fits | 11 acmp | 4 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-burst.held.adp.if0` (save-burst) | 3.457 | fits | 7 adp | 4 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-flight.held.aecp.if0` (save-flight) | 5.811 | fits | 14 aecp | 4 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 4.239 | fits | 6 maap | 4 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 10.239 | fits | 31 srp | 4 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.220 (0.559) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.114 (0.254) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.134 (0.301) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.200 (0.559) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.255 (0.572) | fits | 0 events | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-burst.mrpdu.periodic.if0` (save-burst) | 3.149 | fits | 0 srp | 10 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@program-3.service.acmp.first.if0` (backlog-adp@program-3) | 5.389 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 63.060 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@program-3.service.adp.first.if0` (backlog-adp@program-3) | 5.380 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-3.service.adp.last.if0` (backlog-adp@program-3) | 6.892 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@program-aged1-6.service.aecp.first.if0` (backlog-adp@program-aged1-6) | 2.974 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 63.095 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@program-3.service.maap.first.if0` (backlog-adp@program-3) | 5.415 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-3.service.maap.last.if0` (backlog-adp@program-3) | 6.930 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-3.service.srp.first.if0` (backlog-adp@program-3) | 8.225 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-1.service.srp.last.if0` (backlog-adp@blank-1) | 11.832 | fits | 31 srp | 77 | 0 |
| Talker Advertise RX for every input, bound | 0 | `srp.bound_advertise.if0` (srp-bound) | 1.050 (1.050) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.632 (0.698) | fits | 0 srp | 1 | 0 |
| Talker Advertise RX for every input, no binding (kept) | 0 | `srp.kept_advertise.if0` (srp-kept) | 0.997 (0.998) | fits | 0 srp | 1 | 0 |
| Talker Failed RX for every input, no binding (kept) | 0 | `srp.kept_failed.if0` (srp-kept) | 0.931 (0.932) | fits | 0 srp | 1 | 0 |
| Talker RX at the bound after a freed block (count) | 0 | `srp.kept_recount.if0` (srp-kept) | 0.638 (0.639) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.408 (0.408) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.244 (0.244) | fits | 0 srp | 2 | 0 |
| Talker Advertise RX for every input, bound | 0 | `srp.register_advertise.if0` (srp-register) | 1.052 (1.053) | fits | 0 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t0.r0.if0` (srp-register-burst) | 1.485 (2.413) | fits | 0 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t0.r1.if0` (srp-register-burst) | 1.484 (2.412) | fits | 1 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t0.r2.if0` (srp-register-burst) | 1.483 (2.412) | fits | 2 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t1.r0.if0` (srp-register-burst) | 1.637 (2.589) | fits | 0 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t1.r1.if0` (srp-register-burst) | 1.636 (2.588) | fits | 1 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t1.r2.if0` (srp-register-burst) | 1.635 (2.587) | fits | 2 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t2.r0.if0` (srp-register-burst) | 1.024 (1.228) | fits | 0 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t2.r1.if0` (srp-register-burst) | 1.023 (1.227) | fits | 1 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t2.r2.if0` (srp-register-burst) | 1.022 (1.226) | fits | 2 srp | 1 | 0 |
| our MRPDU after a registering triple (JoinTime wait) | 0 | `srp.register_tx.t0.if0` (srp-register-burst) | 4.643 (5.952) | fits | 2 srp | 1 | 0 |
| our MRPDU after a registering triple (JoinTime wait) | 0 | `srp.register_tx.t1.if0` (srp-register-burst) | 84.434 (85.938) | fits | 2 srp | 1 | 0 |
| our MRPDU after a registering triple (JoinTime wait) | 0 | `srp.register_tx.t2.if0` (srp-register-burst) | 166.083 (166.752) | fits | 2 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.523 (0.588) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 13.836 | 8 | 152,551 (1.526) | yes | - |
| backlog-adp@blank-1 | 0 | 14.622 | 8 | 152,729 (1.527) | yes | - |
| backlog-adp@blank-2 | 0 | 14.497 | 8 | 152,729 (1.527) | yes | - |
| backlog-adp@blank-3 | 0 | 14.372 | 8 | 152,729 (1.527) | yes | - |
| backlog-adp@blank-4 | 0 | 14.247 | 8 | 152,729 (1.527) | yes | - |
| backlog-adp@blank-5 | 0 | 14.122 | 8 | 152,729 (1.527) | yes | - |
| backlog-adp@blank-6 | 0 | 13.997 | 8 | 152,729 (1.527) | yes | - |
| backlog-adp@blank-7 | 0 | 13.872 | 8 | 152,729 (1.527) | yes | - |
| backlog-adp@program-0 | 1 | 12.337 | 7 | 153,251 (1.533) | yes | - |
| backlog-adp@program-1 | 1 | 12.337 | 7 | 153,251 (1.533) | yes | - |
| backlog-adp@program-2 | 0 | 12.344 | 8 | 153,500 (1.535) | yes | - |
| backlog-adp@program-3 | 0 | 13.247 | 8 | 152,337 (1.523) | yes | - |
| backlog-adp@program-4 | 0 | 12.997 | 8 | 152,337 (1.523) | yes | - |
| backlog-adp@program-5 | 0 | 12.747 | 8 | 152,337 (1.523) | yes | - |
| backlog-adp@program-6 | 0 | 12.497 | 8 | 152,337 (1.523) | yes | - |
| backlog-adp@program-7 | 0 | 13.202 | 8 | 153,694 (1.537) | yes | - |
| backlog-adp@verify-0 | 0 | 13.700 | 7 | 150,998 (1.510) | yes | - |
| backlog-adp@verify-1 | 0 | 16.500 | 9 | 153,585 (1.536) | yes | - |
| backlog-adp@verify-2 | 0 | 16.375 | 9 | 153,585 (1.536) | yes | - |
| backlog-adp@verify-3 | 0 | 16.250 | 9 | 153,585 (1.536) | yes | - |
| backlog-adp@verify-4 | 0 | 16.125 | 9 | 153,585 (1.536) | yes | - |
| backlog-adp@verify-5 | 0 | 16.000 | 9 | 153,585 (1.536) | yes | - |
| backlog-adp@verify-6 | 0 | 15.875 | 9 | 153,585 (1.536) | yes | - |
| backlog-adp@verify-7 | 0 | 15.750 | 9 | 153,585 (1.536) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 13.570 | 8 | 153,277 (1.533) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 14.446 | 8 | 152,339 (1.523) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 14.444 | 7 | 153,526 (1.535) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 14.562 | 8 | 153,277 (1.533) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 14.537 | 8 | 152,339 (1.523) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 16.532 | 9 | 151,847 (1.518) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 15.571 | 9 | 153,708 (1.537) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 14.460 | 8 | 152,491 (1.525) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 13.733 | 8 | 153,277 (1.533) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 13.701 | 8 | 152,339 (1.523) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 13.690 | 8 | 153,526 (1.535) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 13.676 | 7 | 153,720 (1.537) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 13.798 | 8 | 152,339 (1.523) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 13.779 | 8 | 151,847 (1.518) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 14.828 | 9 | 153,090 (1.531) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 13.725 | 9 | 152,283 (1.523) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 13.004 | 8 | 152,225 (1.522) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 13.198 | 8 | 153,218 (1.532) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 13.167 | 8 | 152,281 (1.523) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 13.149 | 8 | 153,467 (1.535) | yes | - |
| backlog-adp@program-aged2-4 | 1 | 13.131 | 7 | 152,425 (1.524) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 13.253 | 8 | 152,281 (1.523) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 14.368 | 9 | 154,816 (1.548) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 13.212 | 8 | 153,794 (1.538) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 13.041 | 7 | 153,467 (1.535) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 13.157 | 8 | 153,218 (1.532) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 13.128 | 8 | 152,281 (1.523) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 13.122 | 8 | 153,467 (1.535) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 13.097 | 8 | 152,425 (1.524) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 13.065 | 8 | 152,225 (1.522) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 13.472 | 8 | 150,686 (1.507) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 13.178 | 9 | 153,661 (1.537) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 13.642 | 8 | 153,500 (1.535) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 14.522 | 8 | 153,694 (1.537) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 14.498 | 8 | 152,281 (1.523) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 14.485 | 8 | 153,251 (1.533) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 14.470 | 7 | 152,337 (1.523) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 16.608 | 9 | 152,281 (1.523) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 15.666 | 9 | 154,549 (1.545) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 14.543 | 8 | 152,567 (1.526) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 13.808 | 8 | 153,500 (1.535) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 13.773 | 8 | 153,694 (1.537) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 13.749 | 8 | 152,281 (1.523) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 13.745 | 8 | 153,251 (1.533) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 13.716 | 8 | 152,337 (1.523) | yes | - |
| backlog-adp@verify-aged1-5 | 1 | 13.701 | 7 | 151,821 (1.518) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 14.915 | 9 | 153,694 (1.537) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 13.798 | 9 | 152,337 (1.523) | yes | - |
| backlog | 0 | 8.316 | 8 | 177,277 (1.773) | yes | - |
| backlog-adp | 0 | 11.418 | 8 | 152,849 (1.528) | yes | - |
| backlog-adp-refill | 0 | 40.925 | 14 | 150,144 (1.501) | yes | - |
| backlog-owed | 0 | 65.533 | 23 | 173,876 (1.739) | yes | - |
| fixture | 0 | 1.455 | 2 | 96,189 (0.962) | yes | - |

Composed maximum over the 4 backlog windows: 177,277 CPU cycles (1.773 ms), backlog.
Over the windows that released their whole load only: 177,277 (1.773 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 162751 | 0 | 52,387 (0.524) | fits |
| srp-kept | 1909 | 0 | 99,750 (0.998) | fits |
| save-burst | 2975 | 0 | 159,631 (1.596) | fits |
| save-held | 3172 | 0 | 164,269 (1.643) | fits |
| save-starved | 74700 | 0 | 164,752 (1.648) | fits |
| save-flight | 2726 | 0 | 164,568 (1.646) | fits |
| acmp-notk | 1103 | 0 | 116,019 (1.160) | fits |
| srp-bound | 764 | 0 | 115,105 (1.151) | fits |
| adp-advertise | 741 | 0 | 30,395 (0.304) | fits |
| backlog-adp@blank-0 | 347 | 0 | 152,551 (1.526) | fits |
| backlog-adp@blank-1 | 347 | 0 | 152,729 (1.527) | fits |
| backlog-adp@blank-2 | 347 | 0 | 152,729 (1.527) | fits |
| backlog-adp@blank-3 | 347 | 0 | 152,729 (1.527) | fits |
| backlog-adp@blank-4 | 347 | 0 | 152,729 (1.527) | fits |
| backlog-adp@blank-5 | 347 | 0 | 152,729 (1.527) | fits |
| backlog-adp@blank-6 | 347 | 0 | 152,729 (1.527) | fits |
| backlog-adp@blank-7 | 347 | 0 | 152,729 (1.527) | fits |
| backlog-adp@program-0 | 357 | 0 | 153,251 (1.533) | fits |
| backlog-adp@program-1 | 357 | 0 | 153,251 (1.533) | fits |
| backlog-adp@program-2 | 358 | 0 | 153,500 (1.535) | fits |
| backlog-adp@program-3 | 358 | 0 | 152,337 (1.523) | fits |
| backlog-adp@program-4 | 358 | 0 | 152,337 (1.523) | fits |
| backlog-adp@program-5 | 358 | 0 | 152,337 (1.523) | fits |
| backlog-adp@program-6 | 358 | 0 | 152,337 (1.523) | fits |
| backlog-adp@program-7 | 358 | 0 | 153,694 (1.537) | fits |
| backlog-adp@verify-0 | 364 | 0 | 161,571 (1.616) | fits |
| backlog-adp@verify-1 | 365 | 0 | 153,585 (1.536) | fits |
| backlog-adp@verify-2 | 365 | 0 | 153,585 (1.536) | fits |
| backlog-adp@verify-3 | 365 | 0 | 153,585 (1.536) | fits |
| backlog-adp@verify-4 | 365 | 0 | 153,585 (1.536) | fits |
| backlog-adp@verify-5 | 365 | 0 | 153,585 (1.536) | fits |
| backlog-adp@verify-6 | 365 | 0 | 153,585 (1.536) | fits |
| backlog-adp@verify-7 | 365 | 0 | 153,585 (1.536) | fits |
| backlog-adp@blank-aged2-0 | 650 | 0 | 153,277 (1.533) | fits |
| backlog-adp@blank-aged2-1 | 658 | 0 | 152,339 (1.523) | fits |
| backlog-adp@blank-aged2-2 | 666 | 0 | 153,526 (1.535) | fits |
| backlog-adp@blank-aged2-3 | 675 | 0 | 153,277 (1.533) | fits |
| backlog-adp@blank-aged2-4 | 683 | 0 | 152,339 (1.523) | fits |
| backlog-adp@blank-aged2-5 | 692 | 0 | 151,847 (1.518) | fits |
| backlog-adp@blank-aged2-6 | 700 | 0 | 153,708 (1.537) | fits |
| backlog-adp@blank-aged2-7 | 707 | 0 | 152,491 (1.525) | fits |
| backlog-adp@blank-aged1-0 | 585 | 0 | 153,277 (1.533) | fits |
| backlog-adp@blank-aged1-1 | 593 | 0 | 152,339 (1.523) | fits |
| backlog-adp@blank-aged1-2 | 601 | 0 | 153,526 (1.535) | fits |
| backlog-adp@blank-aged1-3 | 609 | 0 | 153,720 (1.537) | fits |
| backlog-adp@blank-aged1-4 | 618 | 0 | 152,339 (1.523) | fits |
| backlog-adp@blank-aged1-5 | 626 | 0 | 151,847 (1.518) | fits |
| backlog-adp@blank-aged1-6 | 635 | 0 | 153,090 (1.531) | fits |
| backlog-adp@blank-aged1-7 | 643 | 0 | 152,283 (1.523) | fits |
| backlog-adp@program-aged2-0 | 633 | 0 | 152,225 (1.522) | fits |
| backlog-adp@program-aged2-1 | 641 | 0 | 153,218 (1.532) | fits |
| backlog-adp@program-aged2-2 | 649 | 0 | 152,281 (1.523) | fits |
| backlog-adp@program-aged2-3 | 657 | 0 | 153,467 (1.535) | fits |
| backlog-adp@program-aged2-4 | 665 | 0 | 152,425 (1.524) | fits |
| backlog-adp@program-aged2-5 | 674 | 0 | 152,281 (1.523) | fits |
| backlog-adp@program-aged2-6 | 683 | 0 | 154,816 (1.548) | fits |
| backlog-adp@program-aged2-7 | 690 | 0 | 153,794 (1.538) | fits |
| backlog-adp@program-aged1-0 | 567 | 0 | 153,467 (1.535) | fits |
| backlog-adp@program-aged1-1 | 576 | 0 | 153,218 (1.532) | fits |
| backlog-adp@program-aged1-2 | 584 | 0 | 152,281 (1.523) | fits |
| backlog-adp@program-aged1-3 | 592 | 0 | 153,467 (1.535) | fits |
| backlog-adp@program-aged1-4 | 600 | 0 | 152,425 (1.524) | fits |
| backlog-adp@program-aged1-5 | 608 | 0 | 152,225 (1.522) | fits |
| backlog-adp@program-aged1-6 | 617 | 0 | 151,081 (1.511) | fits |
| backlog-adp@program-aged1-7 | 626 | 0 | 153,661 (1.537) | fits |
| backlog-adp@verify-aged2-0 | 654 | 0 | 153,500 (1.535) | fits |
| backlog-adp@verify-aged2-1 | 662 | 0 | 153,694 (1.537) | fits |
| backlog-adp@verify-aged2-2 | 670 | 0 | 152,281 (1.523) | fits |
| backlog-adp@verify-aged2-3 | 678 | 0 | 153,251 (1.533) | fits |
| backlog-adp@verify-aged2-4 | 686 | 0 | 152,337 (1.523) | fits |
| backlog-adp@verify-aged2-5 | 696 | 0 | 152,281 (1.523) | fits |
| backlog-adp@verify-aged2-6 | 704 | 0 | 154,549 (1.545) | fits |
| backlog-adp@verify-aged2-7 | 711 | 0 | 152,567 (1.526) | fits |
| backlog-adp@verify-aged1-0 | 589 | 0 | 153,500 (1.535) | fits |
| backlog-adp@verify-aged1-1 | 597 | 0 | 153,694 (1.537) | fits |
| backlog-adp@verify-aged1-2 | 605 | 0 | 152,281 (1.523) | fits |
| backlog-adp@verify-aged1-3 | 613 | 0 | 153,251 (1.533) | fits |
| backlog-adp@verify-aged1-4 | 621 | 0 | 152,337 (1.523) | fits |
| backlog-adp@verify-aged1-5 | 629 | 0 | 151,821 (1.518) | fits |
| backlog-adp@verify-aged1-6 | 639 | 0 | 153,694 (1.537) | fits |
| backlog-adp@verify-aged1-7 | 647 | 0 | 152,337 (1.523) | fits |
| acmp-noresp | 644 | 0 | 115,254 (1.153) | fits |
| save | 608 | 0 | 86,801 (0.868) | fits |
| srp-register-burst | 526 | 0 | 165,182 (1.652) | fits |
| adp-link | 234 | 0 | 43,196 (0.432) | fits |
| adp-gm | 233 | 0 | 30,395 (0.304) | fits |
| adp-discover | 233 | 0 | 30,395 (0.304) | fits |
| control | 233 | 0 | 30,395 (0.304) | fits |
| srp | 289 | 0 | 40,818 (0.408) | fits |
| backlog | 286 | 0 | 177,277 (1.773) | fits |
| backlog-adp | 295 | 0 | 152,849 (1.528) | fits |
| backlog-adp-refill | 301 | 0 | 150,144 (1.501) | fits |
| backlog-owed | 307 | 0 | 173,876 (1.739) | fits |
| acmp-disc | 332 | 0 | 115,081 (1.151) | fits |
| srp-register | 244 | 0 | 114,336 (1.143) | fits |
| maap | 183 | 0 | 30,395 (0.304) | fits |
| aecp-fanout | 121 | 0 | 95,532 (0.955) | fits |
| acmp-cmd | 81 | 0 | 45,715 (0.457) | fits |
| aecp | 112 | 0 | 49,921 (0.499) | fits |
| aecp-reboot | 107 | 0 | 52,601 (0.526) | fits |
| aecp-largest-notice | 104 | 0 | 148,516 (1.485) | fits |
| aecp-held | 103 | 0 | 41,295 (0.413) | fits |
| datapath-events | 109 | 0 | 30,074 (0.301) | fits |
| fixture | 68 | 0 | 96,189 (0.962) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | +10.948 ms, 76,915 (0.769 ms), read-back | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 10.911 (20) | 9.089 |
| backlog-adp@blank-aged2-1 | 2 | +10.007 ms, 76,915 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 11.655 (20) | 8.345 |
| backlog-adp@blank-aged2-2 | 2 | +8.761 ms, 77,050 (0.770 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 11.652 (20) | 8.348 |
| backlog-adp@blank-aged2-3 | 2 | none | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 11.770 (20) | 8.230 |
| backlog-adp@blank-aged2-4 | 2 | +6.058 ms, 76,704 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 11.746 (20) | 8.254 |
| backlog-adp@blank-aged2-5 | 2 | +6.038 ms, 76,704 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 11.729 (20) | 8.271 |
| backlog-adp@blank-aged2-6 | 2 | +4.458 ms, 76,757 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 11.680 (20) | 8.320 |
| backlog-adp@blank-aged2-7 | 2 | +2.984 ms, 76,503 (0.765 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 11.672 (20) | 8.328 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 10.943 (20) | 9.057 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 10.908 (20) | 9.092 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 10.896 (20) | 9.104 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 10.882 (20) | 9.118 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 11.006 (20) | 8.994 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 10.987 (20) | 9.013 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 10.937 (20) | 9.063 |
| backlog-adp@blank-aged1-7 | 1 | none | +11.121 ms, 76,575 (0.766 ms), read-back | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 10.881 (20) | 9.119 |
| backlog-adp@program-aged2-0 | 2 | none | +11.005 ms, 80,747 (0.807 ms), issue | `backlog-adp@program-aged2-0.service.srp.last.if0` | 10.968 (20) | 9.032 |
| backlog-adp@program-aged2-1 | 2 | +10.082 ms, 80,747 (0.807 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 11.773 (20) | 8.227 |
| backlog-adp@program-aged2-2 | 2 | +8.810 ms, 80,882 (0.809 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 11.743 (20) | 8.257 |
| backlog-adp@program-aged2-3 | 2 | none | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 11.722 (20) | 8.278 |
| backlog-adp@program-aged2-4 | 2 | +5.971 ms, 80,570 (0.806 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 11.705 (20) | 8.295 |
| backlog-adp@program-aged2-5 | 2 | +6.097 ms, 80,570 (0.806 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 11.828 (20) | 8.172 |
| backlog-adp@program-aged2-6 | 2 | +4.531 ms, 80,642 (0.806 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 11.802 (20) | 8.198 |
| backlog-adp@program-aged2-7 | 2 | +3.051 ms, 80,106 (0.801 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 11.785 (20) | 8.215 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 10.866 (20) | 9.134 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 10.983 (20) | 9.017 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 10.953 (20) | 9.047 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 10.948 (20) | 9.052 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 10.923 (20) | 9.077 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 10.890 (20) | 9.110 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 10.900 (20) | 9.100 |
| backlog-adp@program-aged1-7 | 1 | none | +11.190 ms, 80,483 (0.805 ms), issue | `backlog-adp@program-aged1-7.service.srp.last.if0` | 10.950 (20) | 9.050 |
| backlog-adp@verify-aged2-0 | 2 | none | +11.004 ms, 77,582 (0.776 ms), read-back | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 10.967 (20) | 9.033 |
| backlog-adp@verify-aged2-1 | 2 | +10.063 ms, 77,582 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 11.718 (20) | 8.282 |
| backlog-adp@verify-aged2-2 | 2 | +8.796 ms, 77,717 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 11.693 (20) | 8.307 |
| backlog-adp@verify-aged2-3 | 2 | none | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 11.678 (20) | 8.322 |
| backlog-adp@verify-aged2-4 | 2 | +5.970 ms, 77,472 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 11.663 (20) | 8.337 |
| backlog-adp@verify-aged2-5 | 2 | +6.087 ms, 77,472 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 11.778 (20) | 8.222 |
| backlog-adp@verify-aged2-6 | 2 | +4.520 ms, 77,471 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 11.755 (20) | 8.245 |
| backlog-adp@verify-aged2-7 | 2 | +3.041 ms, 77,221 (0.772 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 11.735 (20) | 8.265 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 10.999 (20) | 9.001 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 10.964 (20) | 9.036 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 10.940 (20) | 9.060 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 10.936 (20) | 9.064 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 10.908 (20) | 9.092 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 10.894 (20) | 9.106 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 11.002 (20) | 8.998 |
| backlog-adp@verify-aged1-7 | 1 | none | +11.177 ms, 77,242 (0.772 ms), read-back | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 10.937 (20) | 9.063 |

Least margin over the aged windows: 8.172 ms, `backlog-adp@program-aged2-5.service.srp.last.if0` at 11.828 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 23789.566 | 23,830 | 398 | 2 | 30.893 | yes | within |
| save-held | 1358.030 | 12,950 | 398 | - | 32.707 | no | within |
| save-starved | 12927.599 | 12,950 | 398 | - | 35.190 | yes | within |
| save | 1304.605 | 12,950 | 398 | - | 104.055 | no | within |

Names from their response to durable (save_burst.py; #920, #665's ruling of 2026-11-15, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-burst | 115 | 1364.053 (0) | 5,000 | 7 | - | - | sequence 7, 0 missing | within |
| save-flight | 1 | 674.408 (0) | 5,000 | 2 | - | - | 61 steps (want 61), 27.901 ms | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1112 | 82,292 (0.823) | 78,402 (0.784) |
| srp-kept | 1844 | 23,231 (0.232) | 2,757 (0.028) |
| save-burst | 4214 | 104,547 (1.045) | 78,977 (0.790) |
| save-held | 1972 | 98,405 (0.984) | 78,878 (0.789) |
| save-starved | 714 | 82,545 (0.825) | 78,756 (0.788) |
| save-flight | 2094 | 98,333 (0.983) | 79,247 (0.792) |
| acmp-notk | 1432 | 116,019 (1.160) | 78,604 (0.786) |
| srp-bound | 2904 | 115,105 (1.151) | 78,664 (0.787) |
| adp-advertise | 717 | 22,908 (0.229) | 2,666 (0.027) |
| backlog-adp@blank-0 | 383 | 92,721 (0.927) | 76,495 (0.765) |
| backlog-adp@blank-1 | 384 | 92,740 (0.927) | 76,495 (0.765) |
| backlog-adp@blank-2 | 384 | 92,740 (0.927) | 76,495 (0.765) |
| backlog-adp@blank-3 | 384 | 92,740 (0.927) | 76,495 (0.765) |
| backlog-adp@blank-4 | 384 | 92,740 (0.927) | 76,495 (0.765) |
| backlog-adp@blank-5 | 384 | 92,740 (0.927) | 76,495 (0.765) |
| backlog-adp@blank-6 | 384 | 92,740 (0.927) | 76,495 (0.765) |
| backlog-adp@blank-7 | 384 | 92,740 (0.927) | 76,495 (0.765) |
| backlog-adp@program-0 | 498 | 95,584 (0.956) | 78,494 (0.785) |
| backlog-adp@program-1 | 498 | 95,584 (0.956) | 78,494 (0.785) |
| backlog-adp@program-2 | 498 | 95,584 (0.956) | 78,494 (0.785) |
| backlog-adp@program-3 | 500 | 95,584 (0.956) | 78,494 (0.785) |
| backlog-adp@program-4 | 500 | 95,584 (0.956) | 78,494 (0.785) |
| backlog-adp@program-5 | 500 | 95,584 (0.956) | 78,494 (0.785) |
| backlog-adp@program-6 | 500 | 95,584 (0.956) | 78,494 (0.785) |
| backlog-adp@program-7 | 501 | 96,764 (0.968) | 78,931 (0.789) |
| backlog-adp@verify-0 | 608 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-1 | 611 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-2 | 611 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-3 | 611 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-4 | 611 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-5 | 611 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-6 | 611 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-7 | 611 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@blank-aged2-0 | 381 | 94,077 (0.941) | 76,001 (0.760) |
| backlog-adp@blank-aged2-1 | 382 | 92,755 (0.928) | 76,340 (0.763) |
| backlog-adp@blank-aged2-2 | 382 | 92,921 (0.929) | 76,412 (0.764) |
| backlog-adp@blank-aged2-3 | 382 | 92,888 (0.929) | 76,495 (0.765) |
| backlog-adp@blank-aged2-4 | 382 | 92,770 (0.928) | 76,495 (0.765) |
| backlog-adp@blank-aged2-5 | 384 | 92,789 (0.928) | 76,495 (0.765) |
| backlog-adp@blank-aged2-6 | 383 | 92,784 (0.928) | 76,495 (0.765) |
| backlog-adp@blank-aged2-7 | 382 | 92,813 (0.928) | 76,412 (0.764) |
| backlog-adp@blank-aged1-0 | 381 | 93,019 (0.930) | 76,569 (0.766) |
| backlog-adp@blank-aged1-1 | 381 | 92,986 (0.930) | 76,571 (0.766) |
| backlog-adp@blank-aged1-2 | 381 | 93,080 (0.931) | 76,571 (0.766) |
| backlog-adp@blank-aged1-3 | 381 | 93,018 (0.930) | 76,654 (0.767) |
| backlog-adp@blank-aged1-4 | 381 | 92,929 (0.929) | 76,654 (0.767) |
| backlog-adp@blank-aged1-5 | 381 | 92,948 (0.929) | 76,654 (0.767) |
| backlog-adp@blank-aged1-6 | 382 | 92,943 (0.929) | 76,654 (0.767) |
| backlog-adp@blank-aged1-7 | 381 | 92,675 (0.927) | 75,977 (0.760) |
| backlog-adp@program-aged2-0 | 495 | 95,584 (0.956) | 78,505 (0.785) |
| backlog-adp@program-aged2-1 | 496 | 95,584 (0.956) | 78,505 (0.785) |
| backlog-adp@program-aged2-2 | 496 | 95,584 (0.956) | 78,505 (0.785) |
| backlog-adp@program-aged2-3 | 496 | 95,584 (0.956) | 78,759 (0.788) |
| backlog-adp@program-aged2-4 | 496 | 95,584 (0.956) | 78,620 (0.786) |
| backlog-adp@program-aged2-5 | 496 | 95,584 (0.956) | 78,620 (0.786) |
| backlog-adp@program-aged2-6 | 497 | 95,584 (0.956) | 78,494 (0.785) |
| backlog-adp@program-aged2-7 | 496 | 95,640 (0.956) | 78,494 (0.785) |
| backlog-adp@program-aged1-0 | 495 | 96,804 (0.968) | 78,931 (0.789) |
| backlog-adp@program-aged1-1 | 495 | 96,750 (0.968) | 78,931 (0.789) |
| backlog-adp@program-aged1-2 | 495 | 96,825 (0.968) | 78,931 (0.789) |
| backlog-adp@program-aged1-3 | 495 | 96,787 (0.968) | 79,014 (0.790) |
| backlog-adp@program-aged1-4 | 495 | 96,707 (0.967) | 79,014 (0.790) |
| backlog-adp@program-aged1-5 | 495 | 96,693 (0.967) | 79,014 (0.790) |
| backlog-adp@program-aged1-6 | 496 | 96,693 (0.967) | 79,014 (0.790) |
| backlog-adp@program-aged1-7 | 495 | 95,584 (0.956) | 78,494 (0.785) |
| backlog-adp@verify-aged2-0 | 608 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-aged2-1 | 609 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-aged2-2 | 609 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-aged2-3 | 609 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-aged2-4 | 609 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-aged2-5 | 611 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-aged2-6 | 610 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-aged2-7 | 609 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-aged1-0 | 608 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-aged1-1 | 608 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-aged1-2 | 608 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-aged1-3 | 608 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-aged1-4 | 608 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-aged1-5 | 608 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-aged1-6 | 609 | 97,363 (0.974) | 78,664 (0.787) |
| backlog-adp@verify-aged1-7 | 608 | 97,363 (0.974) | 78,664 (0.787) |
| acmp-noresp | 982 | 115,254 (1.153) | 78,664 (0.787) |
| save | 953 | 97,363 (0.974) | 78,664 (0.787) |
| srp-register-burst | 699 | 175,847 (1.758) | 78,883 (0.789) |
| adp-link | 219 | 22,908 (0.229) | 2,666 (0.027) |
| adp-gm | 219 | 22,908 (0.229) | 2,666 (0.027) |
| adp-discover | 219 | 22,908 (0.229) | 2,666 (0.027) |
| control | 219 | 22,908 (0.229) | 2,666 (0.027) |
| srp | 271 | 22,908 (0.229) | 2,757 (0.028) |
| backlog | 266 | 22,908 (0.229) | 2,672 (0.027) |
| backlog-adp | 271 | 22,908 (0.229) | 2,877 (0.029) |
| backlog-adp-refill | 274 | 22,908 (0.229) | 2,749 (0.027) |
| backlog-owed | 277 | 22,908 (0.229) | 2,824 (0.028) |
| acmp-disc | 673 | 115,081 (1.151) | 78,664 (0.787) |
| srp-register | 513 | 114,336 (1.143) | 78,616 (0.786) |
| maap | 172 | 22,730 (0.227) | 2,666 (0.027) |
| aecp-fanout | 84 | 22,730 (0.227) | 2,830 (0.028) |
| acmp-cmd | 65 | 22,730 (0.227) | 2,666 (0.027) |
| aecp | 80 | 22,730 (0.227) | 2,666 (0.027) |
| aecp-reboot | 78 | 22,730 (0.227) | 2,666 (0.027) |
| aecp-largest-notice | 78 | 22,730 (0.227) | 2,906 (0.029) |
| aecp-held | 93 | 22,730 (0.227) | 2,666 (0.027) |
| datapath-events | 70 | 22,730 (0.227) | 2,666 (0.027) |
| fixture | 54 | 17,539 (0.175) | 2,749 (0.027) |

Longest pass that carries a step: 175,847 CPU cycles (1.758 ms), srp-register-burst; longest step: 79,247 (0.792 ms), save-flight.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| Talker Advertise RX for every input, no binding (kept) | `srp.kept_advertise.if0` | 99,684 | 0.997 | 20 | 20 | fits | 99,750 | 25 | 0.873 |
| Talker RX at the bound after a freed block (count) | `srp.kept_recount.if0` | 63,798 | 0.638 | 20 | 20 | fits | 63,864 | 25 | 0.856 |
| Talker Failed RX for every input, no binding (kept) | `srp.kept_failed.if0` | 93,105 | 0.931 | 20 | 20 | fits | 93,173 | 23 | 0.881 |
| ADP record, every channel at its refill rate, the longest | `save-burst.held.adp.if0` | 345,747 | 3.457 | 20 | 200 | fits | 110,407 | 99 | 0.518 |
| ACMP record, every channel at its refill rate, the longest | `save-burst.held.acmp.if0` | 325,479 | 3.255 | 20 | 20 | fits | 110,407 | 99 | 0.518 |
| AECP record, every channel at its refill rate, the longest | `save-burst.held.aecp.if0` | 258,542 | 2.585 | 20 | 24 | fits | 135,680 | 118 | 0.679 |
| MAAP record, every channel at its refill rate, the longest | `save-burst.held.maap.if0` | 286,004 | 2.860 | 20 | 50 | fits | 110,407 | 99 | 0.518 |
| SRP record, every channel at its refill rate, the longest | `save-burst.held.srp.if0` | 737,364 | 7.374 | 20 | 20 | fits | 116,988 | 110 | 0.679 |
| an MRPDU its join timer owes, the longest | `save-burst.mrpdu.join.if0` | 41,222 | 0.412 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-burst.mrpdu.leaveall.if0` | 34,263 | 0.343 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-burst.mrpdu.periodic.if0` | 314,894 | 3.149 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 292,309 | 2.923 | 20 | 200 | fits | 133,618 | 150 | 0.546 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 319,170 | 3.192 | 20 | 20 | fits | 94,083 | 81 | 0.575 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 467,149 | 4.671 | 20 | 24 | fits | 60,695 | 27 | 0.588 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 185,612 | 1.856 | 20 | 50 | fits | 153,921 | 223 | 0.363 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 1,012,676 | 10.127 | 20 | 20 | fits | 68,918 | 60 | 0.698 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 40,629 | 0.406 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 38,435 | 0.384 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 284,991 | 2.850 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 295,030 | 2.950 | 20 | 200 | fits | 136,339 | 156 | 0.557 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 274,893 | 2.749 | 20 | 20 | fits | 136,339 | 156 | 0.557 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 443,121 | 4.431 | 20 | 24 | fits | 93,364 | 65 | 0.665 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 235,418 | 2.354 | 20 | 50 | fits | 136,339 | 156 | 0.557 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 1,023,889 | 10.239 | 20 | 20 | fits | 103,639 | 105 | 0.638 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 41,530 | 0.415 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 37,082 | 0.371 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 265,793 | 2.658 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 292,309 | 2.923 | 20 | 200 | fits | 133,618 | 150 | 0.546 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 313,951 | 3.140 | 20 | 20 | fits | 82,801 | 68 | 0.584 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 581,066 | 5.811 | 20 | 24 | fits | 136,358 | 121 | 0.630 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 423,924 | 4.239 | 20 | 50 | fits | 113,447 | 184 | 0.395 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 992,383 | 9.924 | 20 | 20 | fits | 46,694 | 34 | 0.772 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 138,239 | 1.382 | 49 | 49 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 10,930 | 0.109 | 20 | 20 | fits | 34,805 | 19 (14) | 0.875 |
| Talker Advertise RX for every input, bound | `srp.bound_advertise.if0` | 104,962 | 1.050 | 20 | 20 | fits | 105,028 | 25 | 0.889 |
| LINK_UP | `adp.link_up.if0` | 3,245 | 0.032 | 20 | 200 | fits | 30,074 | 44 (12) | 0.702 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,555 | 0.126 | 20 | 200 | fits | 21,294 | 23 (39) | 0.604 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 4,741 | 0.047 | 20 | 200 | fits | 2,283 | 10 (11) | 0.400 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 551,922 | 5.519 | 20 | 20 | fits | 152,551 | 192 | 0.397 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 447,710 | 4.477 | 20 | 200 | fits | 151,764 | 131 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 599,645 | 5.996 | 20 | 200 | fits | 152,551 | 192 | 0.397 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 448,634 | 4.486 | 20 | 20 | fits | 151,764 | 131 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 728,341 | 7.283 | 20 | 20 | fits | 127,992 | 116 | 0.649 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 154,133 | 1.541 | 20 | 24 | fits | 150,035 | 109 | 0.410 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 451,284 | 4.513 | 20 | 24 | fits | 151,764 | 131 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 451,218 | 4.512 | 20 | 50 | fits | 151,764 | 131 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 603,373 | 6.034 | 20 | 50 | fits | 152,551 | 192 | 0.397 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 731,299 | 7.313 | 20 | 20 | fits | 127,992 | 116 | 0.649 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,104,600 | 11.046 | 20 | 20 | fits | 90,683 | 86 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 630,123 | 6.301 | 20 | 20 | fits | 152,729 | 191 | 0.395 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 526,184 | 5.262 | 20 | 200 | fits | 151,881 | 131 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 678,297 | 6.783 | 20 | 200 | fits | 152,729 | 191 | 0.395 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 527,108 | 5.271 | 20 | 20 | fits | 151,881 | 131 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 806,938 | 8.069 | 20 | 20 | fits | 127,937 | 116 | 0.648 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 232,572 | 2.326 | 20 | 24 | fits | 150,035 | 109 | 0.410 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 529,758 | 5.298 | 20 | 24 | fits | 151,881 | 131 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 529,692 | 5.297 | 20 | 50 | fits | 151,881 | 131 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 682,025 | 6.820 | 20 | 50 | fits | 152,729 | 191 | 0.395 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 809,896 | 8.099 | 20 | 20 | fits | 127,937 | 116 | 0.648 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 1,183,197 | 11.832 | 20 | 20 | fits | 90,669 | 86 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 617,623 | 6.176 | 20 | 20 | fits | 152,729 | 191 | 0.395 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 513,684 | 5.137 | 20 | 200 | fits | 151,881 | 131 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 665,797 | 6.658 | 20 | 200 | fits | 152,729 | 191 | 0.395 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 514,608 | 5.146 | 20 | 20 | fits | 151,881 | 131 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 794,438 | 7.944 | 20 | 20 | fits | 127,937 | 116 | 0.648 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 220,072 | 2.201 | 20 | 24 | fits | 150,035 | 109 | 0.410 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 517,258 | 5.173 | 20 | 24 | fits | 151,881 | 131 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 517,192 | 5.172 | 20 | 50 | fits | 151,881 | 131 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 669,525 | 6.695 | 20 | 50 | fits | 152,729 | 191 | 0.395 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 797,396 | 7.974 | 20 | 20 | fits | 127,937 | 116 | 0.648 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 1,170,697 | 11.707 | 20 | 20 | fits | 90,669 | 86 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 605,123 | 6.051 | 20 | 20 | fits | 152,729 | 191 | 0.395 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 501,184 | 5.012 | 20 | 200 | fits | 151,881 | 131 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 653,297 | 6.533 | 20 | 200 | fits | 152,729 | 191 | 0.395 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 502,108 | 5.021 | 20 | 20 | fits | 151,881 | 131 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 781,938 | 7.819 | 20 | 20 | fits | 127,937 | 116 | 0.648 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 207,572 | 2.076 | 20 | 24 | fits | 150,035 | 109 | 0.410 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 504,758 | 5.048 | 20 | 24 | fits | 151,881 | 131 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 504,692 | 5.047 | 20 | 50 | fits | 151,881 | 131 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 657,025 | 6.570 | 20 | 50 | fits | 152,729 | 191 | 0.395 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 784,896 | 7.849 | 20 | 20 | fits | 127,937 | 116 | 0.648 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 1,158,197 | 11.582 | 20 | 20 | fits | 90,669 | 86 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 592,623 | 5.926 | 20 | 20 | fits | 152,729 | 191 | 0.395 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 488,684 | 4.887 | 20 | 200 | fits | 151,881 | 131 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 640,797 | 6.408 | 20 | 200 | fits | 152,729 | 191 | 0.395 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 489,608 | 4.896 | 20 | 20 | fits | 151,881 | 131 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 769,438 | 7.694 | 20 | 20 | fits | 127,937 | 116 | 0.648 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 195,072 | 1.951 | 20 | 24 | fits | 150,035 | 109 | 0.410 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 492,258 | 4.923 | 20 | 24 | fits | 151,881 | 131 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 492,192 | 4.922 | 20 | 50 | fits | 151,881 | 131 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 644,525 | 6.445 | 20 | 50 | fits | 152,729 | 191 | 0.395 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 772,396 | 7.724 | 20 | 20 | fits | 127,937 | 116 | 0.648 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 1,145,697 | 11.457 | 20 | 20 | fits | 90,669 | 86 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 580,123 | 5.801 | 20 | 20 | fits | 152,729 | 191 | 0.395 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 476,184 | 4.762 | 20 | 200 | fits | 151,881 | 131 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 628,297 | 6.283 | 20 | 200 | fits | 152,729 | 191 | 0.395 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 477,108 | 4.771 | 20 | 20 | fits | 151,881 | 131 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 756,938 | 7.569 | 20 | 20 | fits | 127,937 | 116 | 0.648 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 182,572 | 1.826 | 20 | 24 | fits | 150,035 | 109 | 0.410 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 479,758 | 4.798 | 20 | 24 | fits | 151,881 | 131 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 479,692 | 4.797 | 20 | 50 | fits | 151,881 | 131 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 632,025 | 6.320 | 20 | 50 | fits | 152,729 | 191 | 0.395 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 759,896 | 7.599 | 20 | 20 | fits | 127,937 | 116 | 0.648 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 1,133,197 | 11.332 | 20 | 20 | fits | 90,669 | 86 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 567,623 | 5.676 | 20 | 20 | fits | 152,729 | 191 | 0.395 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 463,684 | 4.637 | 20 | 200 | fits | 151,881 | 131 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 615,797 | 6.158 | 20 | 200 | fits | 152,729 | 191 | 0.395 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 464,608 | 4.646 | 20 | 20 | fits | 151,881 | 131 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 744,438 | 7.444 | 20 | 20 | fits | 127,937 | 116 | 0.648 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 170,072 | 1.701 | 20 | 24 | fits | 150,035 | 109 | 0.410 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 467,258 | 4.673 | 20 | 24 | fits | 151,881 | 131 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 467,192 | 4.672 | 20 | 50 | fits | 151,881 | 131 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 619,525 | 6.195 | 20 | 50 | fits | 152,729 | 191 | 0.395 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 747,396 | 7.474 | 20 | 20 | fits | 127,937 | 116 | 0.648 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 1,120,697 | 11.207 | 20 | 20 | fits | 90,669 | 86 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 555,123 | 5.551 | 20 | 20 | fits | 152,729 | 191 | 0.395 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 451,184 | 4.512 | 20 | 200 | fits | 151,881 | 131 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 603,297 | 6.033 | 20 | 200 | fits | 152,729 | 191 | 0.395 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 452,108 | 4.521 | 20 | 20 | fits | 151,881 | 131 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 731,938 | 7.319 | 20 | 20 | fits | 127,937 | 116 | 0.648 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 157,572 | 1.576 | 20 | 24 | fits | 150,035 | 109 | 0.410 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 454,758 | 4.548 | 20 | 24 | fits | 151,881 | 131 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 454,692 | 4.547 | 20 | 50 | fits | 151,881 | 131 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 607,025 | 6.070 | 20 | 50 | fits | 152,729 | 191 | 0.395 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 734,896 | 7.349 | 20 | 20 | fits | 127,937 | 116 | 0.648 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 1,108,197 | 11.082 | 20 | 20 | fits | 90,669 | 86 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 541,338 | 5.413 | 20 | 20 | fits | 153,251 | 196 | 0.349 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 445,458 | 4.455 | 20 | 200 | fits | 151,631 | 131 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 598,093 | 5.981 | 20 | 200 | fits | 153,251 | 196 | 0.349 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 446,382 | 4.464 | 20 | 20 | fits | 151,631 | 131 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 728,675 | 7.287 | 20 | 20 | fits | 129,878 | 119 | 0.670 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 151,100 | 1.511 | 20 | 24 | fits | 152,910 | 109 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 449,032 | 4.490 | 20 | 24 | fits | 151,631 | 131 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 448,966 | 4.490 | 20 | 50 | fits | 151,631 | 131 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 601,821 | 6.018 | 20 | 50 | fits | 153,251 | 196 | 0.349 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 731,633 | 7.316 | 20 | 20 | fits | 129,878 | 119 | 0.670 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 1,091,292 | 10.913 | 20 | 20 | fits | 84,917 | 79 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 541,338 | 5.413 | 20 | 20 | fits | 153,251 | 196 | 0.349 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 445,458 | 4.455 | 20 | 200 | fits | 151,631 | 131 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 598,093 | 5.981 | 20 | 200 | fits | 153,251 | 196 | 0.349 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 446,382 | 4.464 | 20 | 20 | fits | 151,631 | 131 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 728,675 | 7.287 | 20 | 20 | fits | 129,878 | 119 | 0.670 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 151,100 | 1.511 | 20 | 24 | fits | 152,910 | 109 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 449,032 | 4.490 | 20 | 24 | fits | 151,631 | 131 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 448,966 | 4.490 | 20 | 50 | fits | 151,631 | 131 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 601,821 | 6.018 | 20 | 50 | fits | 153,251 | 196 | 0.349 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 731,633 | 7.316 | 20 | 20 | fits | 129,878 | 119 | 0.670 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 1,091,292 | 10.913 | 20 | 20 | fits | 84,917 | 79 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 541,844 | 5.418 | 20 | 20 | fits | 153,500 | 195 | 0.349 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 446,074 | 4.461 | 20 | 200 | fits | 151,692 | 131 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 598,958 | 5.990 | 20 | 200 | fits | 153,500 | 195 | 0.349 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 446,998 | 4.470 | 20 | 20 | fits | 151,692 | 131 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 729,304 | 7.293 | 20 | 20 | fits | 129,642 | 119 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 152,695 | 1.527 | 20 | 24 | fits | 149,281 | 109 | 0.399 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 449,648 | 4.496 | 20 | 24 | fits | 151,692 | 131 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 449,582 | 4.496 | 20 | 50 | fits | 151,692 | 131 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 602,686 | 6.027 | 20 | 50 | fits | 153,500 | 195 | 0.349 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 732,262 | 7.323 | 20 | 20 | fits | 129,642 | 119 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 1,091,921 | 10.919 | 20 | 20 | fits | 84,903 | 79 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 640,098 | 6.401 | 20 | 20 | fits | 151,889 | 204 | 0.371 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 537,954 | 5.380 | 20 | 200 | fits | 152,337 | 119 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 689,227 | 6.892 | 20 | 200 | fits | 151,889 | 204 | 0.371 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 538,878 | 5.389 | 20 | 20 | fits | 152,337 | 119 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 819,494 | 8.195 | 20 | 20 | fits | 129,563 | 119 | 0.667 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 243,758 | 2.438 | 20 | 24 | fits | 150,527 | 109 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 541,528 | 5.415 | 20 | 24 | fits | 152,337 | 119 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 541,462 | 5.415 | 20 | 50 | fits | 152,337 | 119 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 692,955 | 6.930 | 20 | 50 | fits | 151,889 | 204 | 0.371 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 822,452 | 8.225 | 20 | 20 | fits | 129,563 | 119 | 0.667 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 1,182,063 | 11.821 | 20 | 20 | fits | 90,654 | 86 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 615,098 | 6.151 | 20 | 20 | fits | 151,889 | 204 | 0.371 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 512,954 | 5.130 | 20 | 200 | fits | 152,337 | 119 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 664,227 | 6.642 | 20 | 200 | fits | 151,889 | 204 | 0.371 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 513,878 | 5.139 | 20 | 20 | fits | 152,337 | 119 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 794,494 | 7.945 | 20 | 20 | fits | 129,563 | 119 | 0.667 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 218,758 | 2.188 | 20 | 24 | fits | 150,527 | 109 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 516,528 | 5.165 | 20 | 24 | fits | 152,337 | 119 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 516,462 | 5.165 | 20 | 50 | fits | 152,337 | 119 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 667,955 | 6.680 | 20 | 50 | fits | 151,889 | 204 | 0.371 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 797,452 | 7.975 | 20 | 20 | fits | 129,563 | 119 | 0.667 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 1,157,063 | 11.571 | 20 | 20 | fits | 90,654 | 86 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 590,098 | 5.901 | 20 | 20 | fits | 151,889 | 204 | 0.371 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 487,954 | 4.880 | 20 | 200 | fits | 152,337 | 119 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 639,227 | 6.392 | 20 | 200 | fits | 151,889 | 204 | 0.371 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 488,878 | 4.889 | 20 | 20 | fits | 152,337 | 119 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 769,494 | 7.695 | 20 | 20 | fits | 129,563 | 119 | 0.667 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 193,758 | 1.938 | 20 | 24 | fits | 150,527 | 109 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 491,528 | 4.915 | 20 | 24 | fits | 152,337 | 119 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 491,462 | 4.915 | 20 | 50 | fits | 152,337 | 119 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 642,955 | 6.430 | 20 | 50 | fits | 151,889 | 204 | 0.371 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 772,452 | 7.725 | 20 | 20 | fits | 129,563 | 119 | 0.667 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 1,132,063 | 11.321 | 20 | 20 | fits | 90,654 | 86 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 565,098 | 5.651 | 20 | 20 | fits | 151,889 | 204 | 0.371 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 462,954 | 4.630 | 20 | 200 | fits | 152,337 | 119 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 614,227 | 6.142 | 20 | 200 | fits | 151,889 | 204 | 0.371 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 463,878 | 4.639 | 20 | 20 | fits | 152,337 | 119 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 744,494 | 7.445 | 20 | 20 | fits | 129,563 | 119 | 0.667 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 168,758 | 1.688 | 20 | 24 | fits | 150,527 | 109 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 466,528 | 4.665 | 20 | 24 | fits | 152,337 | 119 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 466,462 | 4.665 | 20 | 50 | fits | 152,337 | 119 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 617,955 | 6.180 | 20 | 50 | fits | 151,889 | 204 | 0.371 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 747,452 | 7.475 | 20 | 20 | fits | 129,563 | 119 | 0.667 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 1,107,063 | 11.071 | 20 | 20 | fits | 90,654 | 86 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 562,201 | 5.622 | 20 | 20 | fits | 153,694 | 209 | 0.366 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 456,625 | 4.566 | 20 | 200 | fits | 150,345 | 115 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 609,703 | 6.097 | 20 | 200 | fits | 153,694 | 209 | 0.366 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 457,549 | 4.575 | 20 | 20 | fits | 150,345 | 115 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 740,417 | 7.404 | 20 | 20 | fits | 130,010 | 119 | 0.671 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 164,554 | 1.646 | 20 | 24 | fits | 150,188 | 109 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 460,199 | 4.602 | 20 | 24 | fits | 150,345 | 115 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 460,133 | 4.601 | 20 | 50 | fits | 150,345 | 115 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 613,431 | 6.134 | 20 | 50 | fits | 153,694 | 209 | 0.366 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 743,375 | 7.434 | 20 | 20 | fits | 130,010 | 119 | 0.671 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 1,102,946 | 11.029 | 20 | 20 | fits | 90,654 | 86 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 543,353 | 5.434 | 20 | 20 | fits | 150,998 | 189 | 0.399 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 450,950 | 4.510 | 20 | 200 | fits | 147,617 | 175 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 601,332 | 6.013 | 20 | 200 | fits | 150,998 | 189 | 0.399 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 451,874 | 4.519 | 20 | 20 | fits | 147,617 | 175 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 731,800 | 7.318 | 20 | 20 | fits | 129,764 | 119 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 159,987 | 1.600 | 20 | 24 | fits | 161,571 | 68 | 0.410 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 454,524 | 4.545 | 20 | 24 | fits | 147,617 | 175 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 454,458 | 4.545 | 20 | 50 | fits | 147,617 | 175 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 605,060 | 6.051 | 20 | 50 | fits | 150,998 | 189 | 0.399 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 734,758 | 7.348 | 20 | 20 | fits | 129,764 | 119 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,089,231 | 10.892 | 20 | 20 | fits | 79,566 | 73 | 0.668 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 631,235 | 6.312 | 20 | 20 | fits | 153,585 | 206 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 517,698 | 5.177 | 20 | 200 | fits | 148,436 | 114 | 0.477 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 670,667 | 6.707 | 20 | 200 | fits | 153,585 | 206 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 518,622 | 5.186 | 20 | 20 | fits | 148,436 | 114 | 0.477 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 798,907 | 7.989 | 20 | 20 | fits | 127,536 | 116 | 0.646 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 227,468 | 2.275 | 20 | 24 | fits | 149,903 | 109 | 0.410 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 521,272 | 5.213 | 20 | 24 | fits | 148,436 | 114 | 0.477 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 521,206 | 5.212 | 20 | 50 | fits | 148,436 | 114 | 0.477 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 674,395 | 6.744 | 20 | 50 | fits | 153,585 | 206 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 801,865 | 8.019 | 20 | 20 | fits | 127,536 | 116 | 0.646 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 1,167,116 | 11.671 | 20 | 20 | fits | 90,659 | 86 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 618,735 | 6.187 | 20 | 20 | fits | 153,585 | 206 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 505,198 | 5.052 | 20 | 200 | fits | 148,436 | 114 | 0.477 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 658,167 | 6.582 | 20 | 200 | fits | 153,585 | 206 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 506,122 | 5.061 | 20 | 20 | fits | 148,436 | 114 | 0.477 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 786,407 | 7.864 | 20 | 20 | fits | 127,536 | 116 | 0.646 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 214,968 | 2.150 | 20 | 24 | fits | 149,903 | 109 | 0.410 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 508,772 | 5.088 | 20 | 24 | fits | 148,436 | 114 | 0.477 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 508,706 | 5.087 | 20 | 50 | fits | 148,436 | 114 | 0.477 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 661,895 | 6.619 | 20 | 50 | fits | 153,585 | 206 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 789,365 | 7.894 | 20 | 20 | fits | 127,536 | 116 | 0.646 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 1,154,616 | 11.546 | 20 | 20 | fits | 90,659 | 86 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 606,235 | 6.062 | 20 | 20 | fits | 153,585 | 206 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 492,698 | 4.927 | 20 | 200 | fits | 148,436 | 114 | 0.477 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 645,667 | 6.457 | 20 | 200 | fits | 153,585 | 206 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 493,622 | 4.936 | 20 | 20 | fits | 148,436 | 114 | 0.477 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 773,907 | 7.739 | 20 | 20 | fits | 127,536 | 116 | 0.646 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 202,468 | 2.025 | 20 | 24 | fits | 149,903 | 109 | 0.410 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 496,272 | 4.963 | 20 | 24 | fits | 148,436 | 114 | 0.477 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 496,206 | 4.962 | 20 | 50 | fits | 148,436 | 114 | 0.477 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 649,395 | 6.494 | 20 | 50 | fits | 153,585 | 206 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 776,865 | 7.769 | 20 | 20 | fits | 127,536 | 116 | 0.646 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 1,142,116 | 11.421 | 20 | 20 | fits | 90,659 | 86 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 593,735 | 5.937 | 20 | 20 | fits | 153,585 | 206 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 480,198 | 4.802 | 20 | 200 | fits | 148,436 | 114 | 0.477 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 633,167 | 6.332 | 20 | 200 | fits | 153,585 | 206 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 481,122 | 4.811 | 20 | 20 | fits | 148,436 | 114 | 0.477 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 761,407 | 7.614 | 20 | 20 | fits | 127,536 | 116 | 0.646 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 189,968 | 1.900 | 20 | 24 | fits | 149,903 | 109 | 0.410 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 483,772 | 4.838 | 20 | 24 | fits | 148,436 | 114 | 0.477 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 483,706 | 4.837 | 20 | 50 | fits | 148,436 | 114 | 0.477 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 636,895 | 6.369 | 20 | 50 | fits | 153,585 | 206 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 764,365 | 7.644 | 20 | 20 | fits | 127,536 | 116 | 0.646 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 1,129,616 | 11.296 | 20 | 20 | fits | 90,659 | 86 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 581,235 | 5.812 | 20 | 20 | fits | 153,585 | 206 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 467,698 | 4.677 | 20 | 200 | fits | 148,436 | 114 | 0.477 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 620,667 | 6.207 | 20 | 200 | fits | 153,585 | 206 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 468,622 | 4.686 | 20 | 20 | fits | 148,436 | 114 | 0.477 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 748,907 | 7.489 | 20 | 20 | fits | 127,536 | 116 | 0.646 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 177,468 | 1.775 | 20 | 24 | fits | 149,903 | 109 | 0.410 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 471,272 | 4.713 | 20 | 24 | fits | 148,436 | 114 | 0.477 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 471,206 | 4.712 | 20 | 50 | fits | 148,436 | 114 | 0.477 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 624,395 | 6.244 | 20 | 50 | fits | 153,585 | 206 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 751,865 | 7.519 | 20 | 20 | fits | 127,536 | 116 | 0.646 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 1,117,116 | 11.171 | 20 | 20 | fits | 90,659 | 86 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 568,735 | 5.687 | 20 | 20 | fits | 153,585 | 206 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 455,198 | 4.552 | 20 | 200 | fits | 148,436 | 114 | 0.477 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 608,167 | 6.082 | 20 | 200 | fits | 153,585 | 206 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 456,122 | 4.561 | 20 | 20 | fits | 148,436 | 114 | 0.477 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 736,407 | 7.364 | 20 | 20 | fits | 127,536 | 116 | 0.646 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 164,968 | 1.650 | 20 | 24 | fits | 149,903 | 109 | 0.410 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 458,772 | 4.588 | 20 | 24 | fits | 148,436 | 114 | 0.477 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 458,706 | 4.587 | 20 | 50 | fits | 148,436 | 114 | 0.477 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 611,895 | 6.119 | 20 | 50 | fits | 153,585 | 206 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 739,365 | 7.394 | 20 | 20 | fits | 127,536 | 116 | 0.646 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 1,104,616 | 11.046 | 20 | 20 | fits | 90,659 | 86 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 556,235 | 5.562 | 20 | 20 | fits | 153,585 | 206 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 442,698 | 4.427 | 20 | 200 | fits | 148,436 | 114 | 0.477 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 595,667 | 5.957 | 20 | 200 | fits | 153,585 | 206 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 443,622 | 4.436 | 20 | 20 | fits | 148,436 | 114 | 0.477 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 723,907 | 7.239 | 20 | 20 | fits | 127,536 | 116 | 0.646 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 152,468 | 1.525 | 20 | 24 | fits | 149,903 | 109 | 0.410 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 446,272 | 4.463 | 20 | 24 | fits | 148,436 | 114 | 0.477 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 446,206 | 4.462 | 20 | 50 | fits | 148,436 | 114 | 0.477 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 599,395 | 5.994 | 20 | 50 | fits | 153,585 | 206 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 726,865 | 7.269 | 20 | 20 | fits | 127,536 | 116 | 0.646 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 1,092,116 | 10.921 | 20 | 20 | fits | 90,659 | 86 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 541,030 | 5.410 | 20 | 20 | fits | 153,277 | 196 | 0.349 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 445,150 | 4.452 | 20 | 200 | fits | 151,654 | 131 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 597,811 | 5.978 | 20 | 200 | fits | 153,277 | 196 | 0.349 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 446,074 | 4.461 | 20 | 20 | fits | 151,654 | 131 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 728,429 | 7.284 | 20 | 20 | fits | 129,914 | 119 | 0.670 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 151,767 | 1.518 | 20 | 24 | fits | 148,626 | 106 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 448,724 | 4.487 | 20 | 24 | fits | 151,654 | 131 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 448,658 | 4.487 | 20 | 50 | fits | 151,654 | 131 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 601,539 | 6.015 | 20 | 50 | fits | 153,277 | 196 | 0.349 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 731,387 | 7.314 | 20 | 20 | fits | 129,914 | 119 | 0.670 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 1,091,088 | 10.911 | 20 | 20 | fits | 84,859 | 79 | 0.687 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 545,323 | 5.453 | 20 | 20 | fits | 151,948 | 204 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 443,179 | 4.432 | 20 | 200 | fits | 152,339 | 119 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 594,511 | 5.945 | 20 | 200 | fits | 151,948 | 204 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 444,103 | 4.441 | 20 | 20 | fits | 152,339 | 119 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 724,896 | 7.249 | 20 | 20 | fits | 129,681 | 119 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 149,111 | 1.491 | 20 | 24 | fits | 148,626 | 106 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 446,753 | 4.468 | 20 | 24 | fits | 152,339 | 119 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 446,687 | 4.467 | 20 | 50 | fits | 152,339 | 119 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 598,239 | 5.982 | 20 | 50 | fits | 151,948 | 204 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 727,854 | 7.279 | 20 | 20 | fits | 129,681 | 119 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 1,165,464 | 11.655 | 20 | 20 | fits | 91,631 | 87 | 0.662 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 536,537 | 5.365 | 20 | 20 | fits | 153,526 | 195 | 0.349 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 440,767 | 4.408 | 20 | 200 | fits | 151,715 | 131 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 593,677 | 5.937 | 20 | 200 | fits | 153,526 | 195 | 0.349 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 441,691 | 4.417 | 20 | 20 | fits | 151,715 | 131 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 724,059 | 7.241 | 20 | 20 | fits | 129,678 | 119 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 146,455 | 1.465 | 20 | 24 | fits | 148,626 | 106 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 444,341 | 4.443 | 20 | 24 | fits | 151,715 | 131 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 444,275 | 4.443 | 20 | 50 | fits | 151,715 | 131 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 597,405 | 5.974 | 20 | 50 | fits | 153,526 | 195 | 0.349 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 727,017 | 7.270 | 20 | 20 | fits | 129,678 | 119 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,165,164 | 11.652 | 20 | 20 | fits | 79,529 | 73 | 0.668 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 548,355 | 5.484 | 20 | 20 | fits | 153,277 | 196 | 0.349 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 452,475 | 4.525 | 20 | 200 | fits | 151,654 | 131 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 605,136 | 6.051 | 20 | 200 | fits | 153,277 | 196 | 0.349 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 453,399 | 4.534 | 20 | 20 | fits | 151,654 | 131 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 742,718 | 7.427 | 20 | 20 | fits | 136,878 | 127 | 0.669 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 159,092 | 1.591 | 20 | 24 | fits | 148,626 | 106 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 456,049 | 4.560 | 20 | 24 | fits | 151,654 | 131 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 455,983 | 4.560 | 20 | 50 | fits | 151,654 | 131 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 608,864 | 6.089 | 20 | 50 | fits | 153,277 | 196 | 0.349 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 745,676 | 7.457 | 20 | 20 | fits | 136,878 | 127 | 0.669 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,176,985 | 11.770 | 20 | 20 | fits | 79,545 | 73 | 0.668 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 560,176 | 5.602 | 20 | 20 | fits | 150,519 | 200 | 0.414 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 450,504 | 4.505 | 20 | 200 | fits | 152,339 | 119 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 600,407 | 6.004 | 20 | 200 | fits | 150,519 | 200 | 0.414 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 451,428 | 4.514 | 20 | 20 | fits | 152,339 | 119 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 806,190 | 8.062 | 20 | 20 | fits | 128,375 | 117 | 0.651 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 156,436 | 1.564 | 20 | 24 | fits | 148,626 | 106 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 454,078 | 4.541 | 20 | 24 | fits | 152,339 | 119 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 454,012 | 4.540 | 20 | 50 | fits | 152,339 | 119 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 604,135 | 6.041 | 20 | 50 | fits | 150,519 | 200 | 0.414 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 809,148 | 8.091 | 20 | 20 | fits | 128,375 | 117 | 0.651 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,174,622 | 11.746 | 20 | 20 | fits | 90,601 | 86 | 0.649 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 550,469 | 5.505 | 20 | 20 | fits | 151,847 | 191 | 0.390 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 447,224 | 4.472 | 20 | 200 | fits | 151,715 | 131 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 598,455 | 5.985 | 20 | 200 | fits | 151,847 | 191 | 0.390 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 448,148 | 4.481 | 20 | 20 | fits | 151,715 | 131 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 804,412 | 8.044 | 20 | 20 | fits | 128,549 | 117 | 0.653 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 153,780 | 1.538 | 20 | 24 | fits | 148,626 | 106 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 450,798 | 4.508 | 20 | 24 | fits | 151,715 | 131 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 450,732 | 4.507 | 20 | 50 | fits | 151,715 | 131 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 602,183 | 6.022 | 20 | 50 | fits | 151,847 | 191 | 0.390 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 807,370 | 8.074 | 20 | 20 | fits | 128,549 | 117 | 0.653 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,172,882 | 11.729 | 20 | 20 | fits | 90,601 | 86 | 0.649 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 623,174 | 6.232 | 20 | 20 | fits | 153,708 | 209 | 0.369 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 441,085 | 4.411 | 20 | 200 | fits | 148,232 | 114 | 0.478 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 670,934 | 6.709 | 20 | 200 | fits | 153,708 | 209 | 0.369 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 442,009 | 4.420 | 20 | 20 | fits | 148,232 | 114 | 0.478 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 799,777 | 7.998 | 20 | 20 | fits | 128,139 | 116 | 0.651 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 151,124 | 1.511 | 20 | 24 | fits | 148,626 | 106 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 444,659 | 4.447 | 20 | 24 | fits | 148,232 | 114 | 0.478 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 444,593 | 4.446 | 20 | 50 | fits | 148,232 | 114 | 0.478 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 674,662 | 6.747 | 20 | 50 | fits | 153,708 | 209 | 0.369 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 802,735 | 8.027 | 20 | 20 | fits | 128,139 | 116 | 0.651 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,168,033 | 11.680 | 20 | 20 | fits | 90,601 | 86 | 0.649 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 607,251 | 6.073 | 20 | 20 | fits | 151,933 | 205 | 0.365 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 522,631 | 5.226 | 20 | 200 | fits | 152,491 | 119 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 673,948 | 6.739 | 20 | 200 | fits | 151,933 | 205 | 0.365 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 523,555 | 5.236 | 20 | 20 | fits | 152,491 | 119 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 804,529 | 8.045 | 20 | 20 | fits | 129,877 | 119 | 0.669 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 148,468 | 1.485 | 20 | 24 | fits | 148,626 | 106 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 526,205 | 5.262 | 20 | 24 | fits | 152,491 | 119 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 526,139 | 5.261 | 20 | 50 | fits | 152,491 | 119 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 677,676 | 6.777 | 20 | 50 | fits | 151,933 | 205 | 0.365 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 807,487 | 8.075 | 20 | 20 | fits | 129,877 | 119 | 0.669 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,167,240 | 11.672 | 20 | 20 | fits | 84,942 | 79 | 0.687 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 544,236 | 5.442 | 20 | 20 | fits | 153,277 | 196 | 0.349 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 448,356 | 4.484 | 20 | 200 | fits | 151,654 | 131 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 601,017 | 6.010 | 20 | 200 | fits | 153,277 | 196 | 0.349 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 449,280 | 4.493 | 20 | 20 | fits | 151,654 | 131 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 731,635 | 7.316 | 20 | 20 | fits | 129,914 | 119 | 0.670 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 154,973 | 1.550 | 20 | 24 | fits | 148,626 | 106 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 451,930 | 4.519 | 20 | 24 | fits | 151,654 | 131 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 451,864 | 4.519 | 20 | 50 | fits | 151,654 | 131 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 604,745 | 6.047 | 20 | 50 | fits | 153,277 | 196 | 0.349 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 734,593 | 7.346 | 20 | 20 | fits | 129,914 | 119 | 0.670 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 1,094,294 | 10.943 | 20 | 20 | fits | 84,859 | 79 | 0.687 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 548,529 | 5.485 | 20 | 20 | fits | 151,948 | 204 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 446,385 | 4.464 | 20 | 200 | fits | 152,339 | 119 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 597,717 | 5.977 | 20 | 200 | fits | 151,948 | 204 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 447,309 | 4.473 | 20 | 20 | fits | 152,339 | 119 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 728,102 | 7.281 | 20 | 20 | fits | 129,681 | 119 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 152,317 | 1.523 | 20 | 24 | fits | 148,626 | 106 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 449,959 | 4.500 | 20 | 24 | fits | 152,339 | 119 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 449,893 | 4.499 | 20 | 50 | fits | 152,339 | 119 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 601,445 | 6.014 | 20 | 50 | fits | 151,948 | 204 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 731,060 | 7.311 | 20 | 20 | fits | 129,681 | 119 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 1,090,775 | 10.908 | 20 | 20 | fits | 90,651 | 86 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 538,875 | 5.389 | 20 | 20 | fits | 153,526 | 195 | 0.349 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 443,105 | 4.431 | 20 | 200 | fits | 151,715 | 131 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 596,015 | 5.960 | 20 | 200 | fits | 153,526 | 195 | 0.349 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 444,029 | 4.440 | 20 | 20 | fits | 151,715 | 131 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 726,397 | 7.264 | 20 | 20 | fits | 129,678 | 119 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 149,661 | 1.497 | 20 | 24 | fits | 148,626 | 106 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 446,679 | 4.467 | 20 | 24 | fits | 151,715 | 131 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 446,613 | 4.466 | 20 | 50 | fits | 151,715 | 131 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 599,743 | 5.997 | 20 | 50 | fits | 153,526 | 195 | 0.349 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 729,355 | 7.294 | 20 | 20 | fits | 129,678 | 119 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 1,089,570 | 10.896 | 20 | 20 | fits | 79,602 | 73 | 0.669 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 545,581 | 5.456 | 20 | 20 | fits | 153,720 | 209 | 0.366 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 440,005 | 4.400 | 20 | 200 | fits | 150,403 | 115 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 593,109 | 5.931 | 20 | 200 | fits | 153,720 | 209 | 0.366 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 440,929 | 4.409 | 20 | 20 | fits | 150,403 | 115 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 730,826 | 7.308 | 20 | 20 | fits | 137,013 | 127 | 0.671 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 147,005 | 1.470 | 20 | 24 | fits | 148,626 | 106 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 443,579 | 4.436 | 20 | 24 | fits | 150,403 | 115 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 443,513 | 4.435 | 20 | 50 | fits | 150,403 | 115 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 596,837 | 5.968 | 20 | 50 | fits | 153,720 | 209 | 0.366 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 733,784 | 7.338 | 20 | 20 | fits | 137,013 | 127 | 0.671 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 1,088,180 | 10.882 | 20 | 20 | fits | 79,531 | 73 | 0.668 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 563,382 | 5.634 | 20 | 20 | fits | 150,519 | 200 | 0.414 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 453,710 | 4.537 | 20 | 200 | fits | 152,339 | 119 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 603,613 | 6.036 | 20 | 200 | fits | 150,519 | 200 | 0.414 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 454,634 | 4.546 | 20 | 20 | fits | 152,339 | 119 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 732,133 | 7.321 | 20 | 20 | fits | 127,816 | 116 | 0.648 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 159,642 | 1.596 | 20 | 24 | fits | 148,626 | 106 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 457,284 | 4.573 | 20 | 24 | fits | 152,339 | 119 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 457,218 | 4.572 | 20 | 50 | fits | 152,339 | 119 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 607,341 | 6.073 | 20 | 50 | fits | 150,519 | 200 | 0.414 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 735,091 | 7.351 | 20 | 20 | fits | 127,816 | 116 | 0.648 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 1,100,583 | 11.006 | 20 | 20 | fits | 90,601 | 86 | 0.649 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 553,675 | 5.537 | 20 | 20 | fits | 151,847 | 191 | 0.390 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 450,430 | 4.504 | 20 | 200 | fits | 151,715 | 131 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 601,661 | 6.017 | 20 | 200 | fits | 151,847 | 191 | 0.390 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 451,354 | 4.514 | 20 | 20 | fits | 151,715 | 131 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 730,173 | 7.302 | 20 | 20 | fits | 127,808 | 116 | 0.648 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 156,986 | 1.570 | 20 | 24 | fits | 148,626 | 106 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 454,004 | 4.540 | 20 | 24 | fits | 151,715 | 131 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 453,938 | 4.539 | 20 | 50 | fits | 151,715 | 131 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 605,389 | 6.054 | 20 | 50 | fits | 151,847 | 191 | 0.390 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 733,131 | 7.331 | 20 | 20 | fits | 127,808 | 116 | 0.648 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 1,098,661 | 10.987 | 20 | 20 | fits | 90,601 | 86 | 0.649 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 549,310 | 5.493 | 20 | 20 | fits | 153,090 | 208 | 0.361 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 444,291 | 4.443 | 20 | 200 | fits | 148,232 | 114 | 0.478 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 596,765 | 5.968 | 20 | 200 | fits | 153,090 | 208 | 0.361 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 445,215 | 4.452 | 20 | 20 | fits | 148,232 | 114 | 0.478 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 725,486 | 7.255 | 20 | 20 | fits | 128,017 | 116 | 0.650 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 154,330 | 1.543 | 20 | 24 | fits | 148,626 | 106 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 447,865 | 4.479 | 20 | 24 | fits | 148,232 | 114 | 0.478 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 447,799 | 4.478 | 20 | 50 | fits | 148,232 | 114 | 0.478 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 600,493 | 6.005 | 20 | 50 | fits | 153,090 | 208 | 0.361 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 728,444 | 7.284 | 20 | 20 | fits | 128,017 | 116 | 0.650 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 1,093,671 | 10.937 | 20 | 20 | fits | 90,601 | 86 | 0.649 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 533,647 | 5.336 | 20 | 20 | fits | 151,775 | 205 | 0.363 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 449,126 | 4.491 | 20 | 200 | fits | 152,283 | 119 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 600,285 | 6.003 | 20 | 200 | fits | 151,775 | 205 | 0.363 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 450,050 | 4.500 | 20 | 20 | fits | 152,283 | 119 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 730,789 | 7.308 | 20 | 20 | fits | 129,800 | 119 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 151,674 | 1.517 | 20 | 24 | fits | 148,626 | 106 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 452,700 | 4.527 | 20 | 24 | fits | 152,283 | 119 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 452,634 | 4.526 | 20 | 50 | fits | 152,283 | 119 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 604,013 | 6.040 | 20 | 50 | fits | 151,775 | 205 | 0.363 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 733,747 | 7.337 | 20 | 20 | fits | 129,800 | 119 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 1,088,068 | 10.881 | 20 | 20 | fits | 79,508 | 73 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 536,921 | 5.369 | 20 | 20 | fits | 151,716 | 205 | 0.363 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 452,400 | 4.524 | 20 | 200 | fits | 152,225 | 119 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 603,500 | 6.035 | 20 | 200 | fits | 151,716 | 205 | 0.363 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 453,324 | 4.533 | 20 | 20 | fits | 152,225 | 119 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 734,133 | 7.341 | 20 | 20 | fits | 129,929 | 119 | 0.669 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 158,488 | 1.585 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 455,974 | 4.560 | 20 | 24 | fits | 152,225 | 119 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 455,908 | 4.559 | 20 | 50 | fits | 152,225 | 119 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 607,228 | 6.072 | 20 | 50 | fits | 151,716 | 205 | 0.363 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 737,091 | 7.371 | 20 | 20 | fits | 129,929 | 119 | 0.669 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 1,096,775 | 10.968 | 20 | 20 | fits | 84,864 | 79 | 0.687 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 544,974 | 5.450 | 20 | 20 | fits | 153,218 | 196 | 0.348 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 449,094 | 4.491 | 20 | 200 | fits | 151,575 | 131 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 601,696 | 6.017 | 20 | 200 | fits | 153,218 | 196 | 0.348 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 450,018 | 4.500 | 20 | 20 | fits | 151,575 | 131 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 732,443 | 7.324 | 20 | 20 | fits | 130,043 | 119 | 0.671 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 155,832 | 1.558 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 452,668 | 4.527 | 20 | 24 | fits | 151,575 | 131 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 452,602 | 4.526 | 20 | 50 | fits | 151,575 | 131 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 605,424 | 6.054 | 20 | 50 | fits | 153,218 | 196 | 0.348 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 735,401 | 7.354 | 20 | 20 | fits | 130,043 | 119 | 0.671 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 1,177,296 | 11.773 | 20 | 20 | fits | 92,053 | 87 | 0.665 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 549,288 | 5.493 | 20 | 20 | fits | 151,889 | 204 | 0.371 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 447,144 | 4.471 | 20 | 200 | fits | 152,281 | 119 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 598,417 | 5.984 | 20 | 200 | fits | 151,889 | 204 | 0.371 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 448,068 | 4.481 | 20 | 20 | fits | 152,281 | 119 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 728,931 | 7.289 | 20 | 20 | fits | 129,810 | 119 | 0.669 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 153,176 | 1.532 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 450,718 | 4.507 | 20 | 24 | fits | 152,281 | 119 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 450,652 | 4.507 | 20 | 50 | fits | 152,281 | 119 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 602,145 | 6.021 | 20 | 50 | fits | 151,889 | 204 | 0.371 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 731,889 | 7.319 | 20 | 20 | fits | 129,810 | 119 | 0.669 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,174,257 | 11.743 | 20 | 20 | fits | 79,521 | 73 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 539,613 | 5.396 | 20 | 20 | fits | 153,467 | 195 | 0.348 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 443,843 | 4.438 | 20 | 200 | fits | 151,636 | 131 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 596,694 | 5.967 | 20 | 200 | fits | 153,467 | 195 | 0.348 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 444,767 | 4.448 | 20 | 20 | fits | 151,636 | 131 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 734,169 | 7.342 | 20 | 20 | fits | 136,771 | 127 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 150,520 | 1.505 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 447,417 | 4.474 | 20 | 24 | fits | 151,636 | 131 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 447,351 | 4.474 | 20 | 50 | fits | 151,636 | 131 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 600,422 | 6.004 | 20 | 50 | fits | 153,467 | 195 | 0.348 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 737,127 | 7.371 | 20 | 20 | fits | 136,771 | 127 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,172,189 | 11.722 | 20 | 20 | fits | 79,424 | 73 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 553,216 | 5.532 | 20 | 20 | fits | 152,425 | 205 | 0.408 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 439,941 | 4.399 | 20 | 200 | fits | 150,345 | 115 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 591,750 | 5.918 | 20 | 200 | fits | 152,425 | 205 | 0.408 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 440,865 | 4.409 | 20 | 20 | fits | 150,345 | 115 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 802,053 | 8.021 | 20 | 20 | fits | 129,029 | 117 | 0.656 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 147,041 | 1.470 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 443,515 | 4.435 | 20 | 24 | fits | 150,345 | 115 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 443,449 | 4.434 | 20 | 50 | fits | 150,345 | 115 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 595,478 | 5.955 | 20 | 50 | fits | 152,425 | 205 | 0.408 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 805,011 | 8.050 | 20 | 20 | fits | 129,029 | 117 | 0.656 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,170,528 | 11.705 | 20 | 20 | fits | 90,601 | 86 | 0.649 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 564,141 | 5.641 | 20 | 20 | fits | 150,460 | 200 | 0.413 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 454,469 | 4.545 | 20 | 200 | fits | 152,281 | 119 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 604,313 | 6.043 | 20 | 200 | fits | 150,460 | 200 | 0.413 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 455,393 | 4.554 | 20 | 20 | fits | 152,281 | 119 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 814,307 | 8.143 | 20 | 20 | fits | 128,720 | 117 | 0.653 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 160,501 | 1.605 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 458,043 | 4.580 | 20 | 24 | fits | 152,281 | 119 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 457,977 | 4.580 | 20 | 50 | fits | 152,281 | 119 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 608,041 | 6.080 | 20 | 50 | fits | 150,460 | 200 | 0.413 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 817,265 | 8.173 | 20 | 20 | fits | 128,720 | 117 | 0.653 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,182,801 | 11.828 | 20 | 20 | fits | 90,601 | 86 | 0.649 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 634,301 | 6.343 | 20 | 20 | fits | 154,816 | 208 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 448,303 | 4.483 | 20 | 200 | fits | 148,771 | 114 | 0.482 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 683,145 | 6.831 | 20 | 200 | fits | 154,816 | 208 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 449,227 | 4.492 | 20 | 20 | fits | 148,771 | 114 | 0.482 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 811,800 | 8.118 | 20 | 20 | fits | 127,951 | 116 | 0.649 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 157,845 | 1.578 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 451,877 | 4.519 | 20 | 24 | fits | 148,771 | 114 | 0.482 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 451,811 | 4.518 | 20 | 50 | fits | 148,771 | 114 | 0.482 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 686,873 | 6.869 | 20 | 50 | fits | 154,816 | 208 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 814,758 | 8.148 | 20 | 20 | fits | 127,951 | 116 | 0.649 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,180,233 | 11.802 | 20 | 20 | fits | 90,601 | 86 | 0.649 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 637,521 | 6.375 | 20 | 20 | fits | 153,794 | 209 | 0.367 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 531,812 | 5.318 | 20 | 200 | fits | 151,390 | 115 | 0.468 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 684,990 | 6.850 | 20 | 200 | fits | 153,794 | 209 | 0.367 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 532,736 | 5.327 | 20 | 20 | fits | 151,390 | 115 | 0.468 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 815,869 | 8.159 | 20 | 20 | fits | 130,175 | 119 | 0.672 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 155,189 | 1.552 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 535,386 | 5.354 | 20 | 24 | fits | 151,390 | 115 | 0.468 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 535,320 | 5.353 | 20 | 50 | fits | 151,390 | 115 | 0.468 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 688,718 | 6.887 | 20 | 50 | fits | 153,794 | 209 | 0.367 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 818,827 | 8.188 | 20 | 20 | fits | 130,175 | 119 | 0.672 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,178,508 | 11.785 | 20 | 20 | fits | 84,923 | 79 | 0.687 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 536,362 | 5.364 | 20 | 20 | fits | 153,467 | 195 | 0.348 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 440,592 | 4.406 | 20 | 200 | fits | 151,636 | 131 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 593,443 | 5.934 | 20 | 200 | fits | 153,467 | 195 | 0.348 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 441,516 | 4.415 | 20 | 20 | fits | 151,636 | 131 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 723,954 | 7.240 | 20 | 20 | fits | 129,807 | 119 | 0.669 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 146,401 | 1.464 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 444,166 | 4.442 | 20 | 24 | fits | 151,636 | 131 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 444,100 | 4.441 | 20 | 50 | fits | 151,636 | 131 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 597,171 | 5.972 | 20 | 50 | fits | 153,467 | 195 | 0.348 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 726,912 | 7.269 | 20 | 20 | fits | 129,807 | 119 | 0.669 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 1,086,620 | 10.866 | 20 | 20 | fits | 84,845 | 79 | 0.687 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 548,180 | 5.482 | 20 | 20 | fits | 153,218 | 196 | 0.348 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 452,300 | 4.523 | 20 | 200 | fits | 151,575 | 131 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 604,902 | 6.049 | 20 | 200 | fits | 153,218 | 196 | 0.348 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 453,224 | 4.532 | 20 | 20 | fits | 151,575 | 131 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 735,649 | 7.356 | 20 | 20 | fits | 130,043 | 119 | 0.671 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 159,038 | 1.590 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 455,874 | 4.559 | 20 | 24 | fits | 151,575 | 131 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 455,808 | 4.558 | 20 | 50 | fits | 151,575 | 131 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 608,630 | 6.086 | 20 | 50 | fits | 153,218 | 196 | 0.348 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 738,607 | 7.386 | 20 | 20 | fits | 130,043 | 119 | 0.671 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 1,098,312 | 10.983 | 20 | 20 | fits | 90,610 | 86 | 0.649 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 552,494 | 5.525 | 20 | 20 | fits | 151,889 | 204 | 0.371 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 450,350 | 4.503 | 20 | 200 | fits | 152,281 | 119 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 601,623 | 6.016 | 20 | 200 | fits | 151,889 | 204 | 0.371 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 451,274 | 4.513 | 20 | 20 | fits | 152,281 | 119 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 732,137 | 7.321 | 20 | 20 | fits | 129,810 | 119 | 0.669 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 156,382 | 1.564 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 453,924 | 4.539 | 20 | 24 | fits | 152,281 | 119 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 453,858 | 4.539 | 20 | 50 | fits | 152,281 | 119 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 605,351 | 6.054 | 20 | 50 | fits | 151,889 | 204 | 0.371 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 735,095 | 7.351 | 20 | 20 | fits | 129,810 | 119 | 0.669 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 1,095,337 | 10.953 | 20 | 20 | fits | 79,602 | 73 | 0.669 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 542,819 | 5.428 | 20 | 20 | fits | 153,467 | 195 | 0.348 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 447,049 | 4.470 | 20 | 200 | fits | 151,636 | 131 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 599,900 | 5.999 | 20 | 200 | fits | 153,467 | 195 | 0.348 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 447,973 | 4.480 | 20 | 20 | fits | 151,636 | 131 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 737,375 | 7.374 | 20 | 20 | fits | 136,771 | 127 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 153,726 | 1.537 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 450,623 | 4.506 | 20 | 24 | fits | 151,636 | 131 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 450,557 | 4.506 | 20 | 50 | fits | 151,636 | 131 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 603,628 | 6.036 | 20 | 50 | fits | 153,467 | 195 | 0.348 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 740,333 | 7.403 | 20 | 20 | fits | 136,771 | 127 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 1,094,766 | 10.948 | 20 | 20 | fits | 79,531 | 73 | 0.668 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 556,377 | 5.564 | 20 | 20 | fits | 152,425 | 205 | 0.408 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 443,102 | 4.431 | 20 | 200 | fits | 150,345 | 115 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 594,911 | 5.949 | 20 | 200 | fits | 152,425 | 205 | 0.408 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 444,026 | 4.440 | 20 | 20 | fits | 150,345 | 115 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 723,869 | 7.239 | 20 | 20 | fits | 128,254 | 116 | 0.652 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 151,070 | 1.511 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 446,676 | 4.467 | 20 | 24 | fits | 150,345 | 115 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 446,610 | 4.466 | 20 | 50 | fits | 150,345 | 115 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 598,639 | 5.986 | 20 | 50 | fits | 152,425 | 205 | 0.408 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 726,827 | 7.268 | 20 | 20 | fits | 128,254 | 116 | 0.652 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 1,092,260 | 10.923 | 20 | 20 | fits | 90,601 | 86 | 0.649 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 534,376 | 5.344 | 20 | 20 | fits | 150,402 | 201 | 0.407 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 442,326 | 4.423 | 20 | 200 | fits | 152,225 | 119 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 592,112 | 5.921 | 20 | 200 | fits | 150,402 | 201 | 0.407 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 443,250 | 4.433 | 20 | 20 | fits | 152,225 | 119 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 720,584 | 7.206 | 20 | 20 | fits | 127,768 | 116 | 0.649 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 148,414 | 1.484 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 445,900 | 4.459 | 20 | 24 | fits | 152,225 | 119 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 445,834 | 4.458 | 20 | 50 | fits | 152,225 | 119 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 595,840 | 5.958 | 20 | 50 | fits | 150,402 | 201 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 723,542 | 7.235 | 20 | 20 | fits | 127,768 | 116 | 0.649 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 1,089,041 | 10.890 | 20 | 20 | fits | 90,620 | 86 | 0.649 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 536,946 | 5.369 | 20 | 20 | fits | 150,686 | 90 | 0.457 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 143,764 | 1.438 | 20 | 200 | fits | 151,081 | 234 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 592,698 | 5.927 | 20 | 200 | fits | 150,686 | 90 | 0.457 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 144,688 | 1.447 | 20 | 20 | fits | 151,081 | 234 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 721,655 | 7.217 | 20 | 20 | fits | 128,253 | 116 | 0.652 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 297,381 | 2.974 | 20 | 24 | fits | 149,053 | 106 | 0.404 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 596,888 | 5.969 | 20 | 24 | fits | 150,686 | 90 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 147,272 | 1.473 | 20 | 50 | fits | 151,081 | 234 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 146,876 | 1.469 | 20 | 50 | fits | 151,081 | 234 | 0.375 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 724,613 | 7.246 | 20 | 20 | fits | 128,253 | 116 | 0.652 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 1,089,975 | 10.900 | 20 | 20 | fits | 90,615 | 86 | 0.649 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 559,443 | 5.594 | 20 | 20 | fits | 153,661 | 209 | 0.365 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 453,867 | 4.539 | 20 | 200 | fits | 150,345 | 115 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 606,912 | 6.069 | 20 | 200 | fits | 153,661 | 209 | 0.365 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 454,791 | 4.548 | 20 | 20 | fits | 150,345 | 115 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 737,791 | 7.378 | 20 | 20 | fits | 130,175 | 119 | 0.672 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 158,395 | 1.584 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 457,441 | 4.574 | 20 | 24 | fits | 150,345 | 115 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 457,375 | 4.574 | 20 | 50 | fits | 150,345 | 115 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 610,640 | 6.106 | 20 | 50 | fits | 153,661 | 209 | 0.365 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 740,749 | 7.407 | 20 | 20 | fits | 130,175 | 119 | 0.672 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 1,095,016 | 10.950 | 20 | 20 | fits | 79,489 | 73 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 546,677 | 5.467 | 20 | 20 | fits | 153,500 | 195 | 0.349 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 450,907 | 4.509 | 20 | 200 | fits | 151,712 | 131 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 603,791 | 6.038 | 20 | 200 | fits | 153,500 | 195 | 0.349 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 451,831 | 4.518 | 20 | 20 | fits | 151,712 | 131 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 734,055 | 7.341 | 20 | 20 | fits | 129,560 | 119 | 0.667 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 157,508 | 1.575 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 454,481 | 4.545 | 20 | 24 | fits | 151,712 | 131 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 454,415 | 4.544 | 20 | 50 | fits | 151,712 | 131 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 607,519 | 6.075 | 20 | 50 | fits | 153,500 | 195 | 0.349 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 737,013 | 7.370 | 20 | 20 | fits | 129,560 | 119 | 0.667 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 1,096,672 | 10.967 | 20 | 20 | fits | 84,903 | 79 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 552,516 | 5.525 | 20 | 20 | fits | 153,694 | 209 | 0.366 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 446,940 | 4.469 | 20 | 200 | fits | 150,401 | 115 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 600,018 | 6.000 | 20 | 200 | fits | 153,694 | 209 | 0.366 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 447,864 | 4.479 | 20 | 20 | fits | 150,401 | 115 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 730,650 | 7.306 | 20 | 20 | fits | 129,928 | 119 | 0.671 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 154,852 | 1.549 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 450,514 | 4.505 | 20 | 24 | fits | 150,401 | 115 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 450,448 | 4.504 | 20 | 50 | fits | 150,401 | 115 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 603,746 | 6.037 | 20 | 50 | fits | 153,694 | 209 | 0.366 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 733,608 | 7.336 | 20 | 20 | fits | 129,928 | 119 | 0.671 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 1,171,822 | 11.718 | 20 | 20 | fits | 91,715 | 87 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 530,685 | 5.307 | 20 | 20 | fits | 151,749 | 205 | 0.363 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 446,164 | 4.462 | 20 | 200 | fits | 152,281 | 119 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 597,297 | 5.973 | 20 | 200 | fits | 151,749 | 205 | 0.363 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 447,088 | 4.471 | 20 | 20 | fits | 152,281 | 119 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 727,683 | 7.277 | 20 | 20 | fits | 129,682 | 119 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 152,196 | 1.522 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 449,738 | 4.497 | 20 | 24 | fits | 152,281 | 119 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 449,672 | 4.497 | 20 | 50 | fits | 152,281 | 119 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 601,025 | 6.010 | 20 | 50 | fits | 151,749 | 205 | 0.363 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 730,641 | 7.306 | 20 | 20 | fits | 129,682 | 119 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,169,274 | 11.693 | 20 | 20 | fits | 79,499 | 73 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 538,758 | 5.388 | 20 | 20 | fits | 153,251 | 196 | 0.349 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 442,878 | 4.429 | 20 | 200 | fits | 151,651 | 131 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 595,513 | 5.955 | 20 | 200 | fits | 153,251 | 196 | 0.349 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 443,802 | 4.438 | 20 | 20 | fits | 151,651 | 131 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 733,101 | 7.331 | 20 | 20 | fits | 136,884 | 127 | 0.669 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 149,540 | 1.495 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 446,452 | 4.465 | 20 | 24 | fits | 151,651 | 131 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 446,386 | 4.464 | 20 | 50 | fits | 151,651 | 131 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 599,241 | 5.992 | 20 | 50 | fits | 153,251 | 196 | 0.349 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 736,059 | 7.361 | 20 | 20 | fits | 136,884 | 127 | 0.669 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,167,760 | 11.678 | 20 | 20 | fits | 79,494 | 73 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 551,448 | 5.514 | 20 | 20 | fits | 150,493 | 200 | 0.414 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 441,776 | 4.418 | 20 | 200 | fits | 152,337 | 119 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 591,653 | 5.917 | 20 | 200 | fits | 150,493 | 200 | 0.414 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 442,700 | 4.427 | 20 | 20 | fits | 152,337 | 119 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 797,949 | 7.979 | 20 | 20 | fits | 128,120 | 117 | 0.648 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 146,884 | 1.469 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 445,350 | 4.454 | 20 | 24 | fits | 152,337 | 119 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 445,284 | 4.453 | 20 | 50 | fits | 152,337 | 119 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 595,381 | 5.954 | 20 | 50 | fits | 150,493 | 200 | 0.414 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 800,907 | 8.009 | 20 | 20 | fits | 128,120 | 117 | 0.648 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,166,339 | 11.663 | 20 | 20 | fits | 90,659 | 86 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 545,539 | 5.455 | 20 | 20 | fits | 150,435 | 201 | 0.407 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 453,489 | 4.535 | 20 | 200 | fits | 152,281 | 119 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 603,308 | 6.033 | 20 | 200 | fits | 150,435 | 201 | 0.407 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 454,413 | 4.544 | 20 | 20 | fits | 152,281 | 119 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 809,427 | 8.094 | 20 | 20 | fits | 127,943 | 117 | 0.649 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 159,521 | 1.595 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 457,063 | 4.571 | 20 | 24 | fits | 152,281 | 119 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 456,997 | 4.570 | 20 | 50 | fits | 152,281 | 119 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 607,036 | 6.070 | 20 | 50 | fits | 150,435 | 201 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 812,385 | 8.124 | 20 | 20 | fits | 127,943 | 117 | 0.649 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,177,817 | 11.778 | 20 | 20 | fits | 90,678 | 86 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 630,782 | 6.308 | 20 | 20 | fits | 154,549 | 209 | 0.375 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 447,250 | 4.473 | 20 | 200 | fits | 148,698 | 114 | 0.482 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 678,654 | 6.787 | 20 | 200 | fits | 154,549 | 209 | 0.375 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 448,174 | 4.482 | 20 | 20 | fits | 148,698 | 114 | 0.482 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 807,204 | 8.072 | 20 | 20 | fits | 127,846 | 116 | 0.649 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 156,865 | 1.569 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 450,824 | 4.508 | 20 | 24 | fits | 148,698 | 114 | 0.482 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 450,758 | 4.508 | 20 | 50 | fits | 148,698 | 114 | 0.482 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 682,382 | 6.824 | 20 | 50 | fits | 154,549 | 209 | 0.375 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 810,162 | 8.102 | 20 | 20 | fits | 127,846 | 116 | 0.649 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,175,524 | 11.755 | 20 | 20 | fits | 90,673 | 86 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 631,324 | 6.313 | 20 | 20 | fits | 151,978 | 204 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 529,124 | 5.291 | 20 | 200 | fits | 152,567 | 119 | 0.452 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 680,486 | 6.805 | 20 | 200 | fits | 151,978 | 204 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 530,048 | 5.300 | 20 | 20 | fits | 152,567 | 119 | 0.452 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 810,835 | 8.108 | 20 | 20 | fits | 129,645 | 119 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 154,209 | 1.542 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 532,698 | 5.327 | 20 | 24 | fits | 152,567 | 119 | 0.452 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 532,632 | 5.326 | 20 | 50 | fits | 152,567 | 119 | 0.452 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 684,214 | 6.842 | 20 | 50 | fits | 151,978 | 204 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 813,793 | 8.138 | 20 | 20 | fits | 129,645 | 119 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,173,492 | 11.735 | 20 | 20 | fits | 84,981 | 79 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 549,883 | 5.499 | 20 | 20 | fits | 153,500 | 195 | 0.349 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 454,113 | 4.541 | 20 | 200 | fits | 151,712 | 131 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 606,997 | 6.070 | 20 | 200 | fits | 153,500 | 195 | 0.349 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 455,037 | 4.550 | 20 | 20 | fits | 151,712 | 131 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 737,261 | 7.373 | 20 | 20 | fits | 129,560 | 119 | 0.667 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 160,714 | 1.607 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 457,687 | 4.577 | 20 | 24 | fits | 151,712 | 131 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 457,621 | 4.576 | 20 | 50 | fits | 151,712 | 131 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 610,725 | 6.107 | 20 | 50 | fits | 153,500 | 195 | 0.349 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 740,219 | 7.402 | 20 | 20 | fits | 129,560 | 119 | 0.667 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 1,099,878 | 10.999 | 20 | 20 | fits | 84,903 | 79 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 555,722 | 5.557 | 20 | 20 | fits | 153,694 | 209 | 0.366 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 450,146 | 4.501 | 20 | 200 | fits | 150,401 | 115 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 603,224 | 6.032 | 20 | 200 | fits | 153,694 | 209 | 0.366 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 451,070 | 4.511 | 20 | 20 | fits | 150,401 | 115 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 733,856 | 7.339 | 20 | 20 | fits | 129,928 | 119 | 0.671 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 158,058 | 1.581 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 453,720 | 4.537 | 20 | 24 | fits | 150,401 | 115 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 453,654 | 4.537 | 20 | 50 | fits | 150,401 | 115 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 606,952 | 6.070 | 20 | 50 | fits | 153,694 | 209 | 0.366 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 736,814 | 7.368 | 20 | 20 | fits | 129,928 | 119 | 0.671 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 1,096,440 | 10.964 | 20 | 20 | fits | 90,709 | 86 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 533,891 | 5.339 | 20 | 20 | fits | 151,749 | 205 | 0.363 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 449,370 | 4.494 | 20 | 200 | fits | 152,281 | 119 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 600,503 | 6.005 | 20 | 200 | fits | 151,749 | 205 | 0.363 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 450,294 | 4.503 | 20 | 20 | fits | 152,281 | 119 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 730,889 | 7.309 | 20 | 20 | fits | 129,682 | 119 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 155,402 | 1.554 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 452,944 | 4.529 | 20 | 24 | fits | 152,281 | 119 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 452,878 | 4.529 | 20 | 50 | fits | 152,281 | 119 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 604,231 | 6.042 | 20 | 50 | fits | 151,749 | 205 | 0.363 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 733,847 | 7.338 | 20 | 20 | fits | 129,682 | 119 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 1,094,019 | 10.940 | 20 | 20 | fits | 79,621 | 73 | 0.669 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 541,964 | 5.420 | 20 | 20 | fits | 153,251 | 196 | 0.349 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 446,084 | 4.461 | 20 | 200 | fits | 151,651 | 131 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 598,719 | 5.987 | 20 | 200 | fits | 153,251 | 196 | 0.349 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 447,008 | 4.470 | 20 | 20 | fits | 151,651 | 131 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 736,307 | 7.363 | 20 | 20 | fits | 136,884 | 127 | 0.669 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 152,746 | 1.527 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 449,658 | 4.497 | 20 | 24 | fits | 151,651 | 131 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 449,592 | 4.496 | 20 | 50 | fits | 151,651 | 131 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 602,447 | 6.024 | 20 | 50 | fits | 153,251 | 196 | 0.349 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 739,265 | 7.393 | 20 | 20 | fits | 136,884 | 127 | 0.669 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 1,093,645 | 10.936 | 20 | 20 | fits | 79,494 | 73 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 553,786 | 5.538 | 20 | 20 | fits | 150,493 | 200 | 0.414 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 444,114 | 4.441 | 20 | 200 | fits | 152,337 | 119 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 593,991 | 5.940 | 20 | 200 | fits | 150,493 | 200 | 0.414 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 445,038 | 4.450 | 20 | 20 | fits | 152,337 | 119 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 722,393 | 7.224 | 20 | 20 | fits | 127,698 | 116 | 0.647 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 150,090 | 1.501 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 447,688 | 4.477 | 20 | 24 | fits | 152,337 | 119 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 447,622 | 4.476 | 20 | 50 | fits | 152,337 | 119 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 597,719 | 5.977 | 20 | 50 | fits | 150,493 | 200 | 0.414 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 725,351 | 7.254 | 20 | 20 | fits | 127,698 | 116 | 0.647 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 1,090,801 | 10.908 | 20 | 20 | fits | 90,659 | 86 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 544,553 | 5.446 | 20 | 20 | fits | 151,821 | 191 | 0.390 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 441,308 | 4.413 | 20 | 200 | fits | 151,712 | 131 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 592,513 | 5.925 | 20 | 200 | fits | 151,821 | 191 | 0.390 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 442,232 | 4.422 | 20 | 20 | fits | 151,712 | 131 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 720,907 | 7.209 | 20 | 20 | fits | 127,690 | 116 | 0.647 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 147,041 | 1.470 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 444,882 | 4.449 | 20 | 24 | fits | 151,712 | 131 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 444,816 | 4.448 | 20 | 50 | fits | 151,712 | 131 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 596,241 | 5.962 | 20 | 50 | fits | 151,821 | 191 | 0.390 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 723,865 | 7.239 | 20 | 20 | fits | 127,690 | 116 | 0.647 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 1,089,353 | 10.894 | 20 | 20 | fits | 90,659 | 86 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 555,978 | 5.560 | 20 | 20 | fits | 153,694 | 208 | 0.366 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 450,456 | 4.505 | 20 | 200 | fits | 148,698 | 114 | 0.482 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 603,534 | 6.035 | 20 | 200 | fits | 153,694 | 208 | 0.366 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 451,380 | 4.514 | 20 | 20 | fits | 148,698 | 114 | 0.482 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 732,002 | 7.320 | 20 | 20 | fits | 127,764 | 116 | 0.648 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 160,071 | 1.601 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 454,030 | 4.540 | 20 | 24 | fits | 148,698 | 114 | 0.482 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 453,964 | 4.540 | 20 | 50 | fits | 148,698 | 114 | 0.482 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 607,262 | 6.073 | 20 | 50 | fits | 153,694 | 208 | 0.366 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 734,960 | 7.350 | 20 | 20 | fits | 127,764 | 116 | 0.648 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 1,100,249 | 11.002 | 20 | 20 | fits | 90,673 | 86 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 557,023 | 5.570 | 20 | 20 | fits | 151,922 | 204 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 454,879 | 4.549 | 20 | 200 | fits | 152,337 | 119 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 606,185 | 6.062 | 20 | 200 | fits | 151,922 | 204 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 455,803 | 4.558 | 20 | 20 | fits | 152,337 | 119 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 736,452 | 7.365 | 20 | 20 | fits | 129,563 | 119 | 0.667 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 157,415 | 1.574 | 20 | 24 | fits | 148,511 | 106 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 458,453 | 4.585 | 20 | 24 | fits | 152,337 | 119 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 458,387 | 4.584 | 20 | 50 | fits | 152,337 | 119 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 609,913 | 6.099 | 20 | 50 | fits | 151,922 | 204 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 739,410 | 7.394 | 20 | 20 | fits | 129,563 | 119 | 0.667 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 1,093,675 | 10.937 | 20 | 20 | fits | 79,547 | 73 | 0.668 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 14,394 | 0.144 | 20 | 20 | fits | 31,054 | 21 (35) | 0.802 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 6,262 | 0.063 | 20 | 20 | fits | 26,508 | 17 (14) | 0.814 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 17,449 | 0.174 | 20 | 20 | fits | 26,358 | 18 (14) | 0.804 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 15,347 | 0.153 | 20 | 20 | fits | 32,610 | 27 (35) | 0.747 |
| a registering record of the burst | `srp.register_burst.t0.r0.if0` | 148,475 | 1.485 | 20 | 20 | fits | 110,657 | 36 | 0.866 |
| a registering record of the burst | `srp.register_burst.t0.r1.if0` | 148,392 | 1.484 | 20 | 20 | fits | 110,657 | 36 | 0.866 |
| a registering record of the burst | `srp.register_burst.t0.r2.if0` | 148,311 | 1.483 | 20 | 20 | fits | 110,657 | 36 | 0.866 |
| our MRPDU after a registering triple (JoinTime wait) | `srp.register_tx.t0.if0` | 464,291 | 4.643 | 220 | 220 | fits | 73,661 | 8 | 0.911 |
| ACMP's last record of its burst at a registering triple | `acmp.register_burst.t0.if0` | 304,008 | 3.040 | 20 | 20 | fits | 48,881 | 32 | 0.624 |
| AECP's last record of its burst at a registering triple | `aecp.register_burst.t0.if0` | 394,348 | 3.943 | 20 | 24 | fits | 83,918 | 36 | 0.521 |
| a registering record of the burst | `srp.register_burst.t1.r0.if0` | 163,699 | 1.637 | 20 | 20 | fits | 143,372 | 23 | 0.895 |
| a registering record of the burst | `srp.register_burst.t1.r1.if0` | 163,618 | 1.636 | 20 | 20 | fits | 143,372 | 23 | 0.895 |
| a registering record of the burst | `srp.register_burst.t1.r2.if0` | 163,535 | 1.635 | 20 | 20 | fits | 143,372 | 23 | 0.895 |
| our MRPDU after a registering triple (JoinTime wait) | `srp.register_tx.t1.if0` | 8,443,389 | 84.434 | 220 | 220 | fits | 127,508 | 9 | 0.701 |
| ACMP's last record of its burst at a registering triple | `acmp.register_burst.t1.if0` | 354,953 | 3.550 | 20 | 20 | fits | 115,131 | 120 | 0.383 |
| AECP's last record of its burst at a registering triple | `aecp.register_burst.t1.if0` | 504,442 | 5.044 | 20 | 24 | fits | 84,056 | 36 | 0.526 |
| a registering record of the burst | `srp.register_burst.t2.r0.if0` | 102,388 | 1.024 | 20 | 20 | fits | 101,707 | 36 | 0.832 |
| a registering record of the burst | `srp.register_burst.t2.r1.if0` | 102,307 | 1.023 | 20 | 20 | fits | 101,707 | 36 | 0.832 |
| a registering record of the burst | `srp.register_burst.t2.r2.if0` | 102,224 | 1.022 | 20 | 20 | fits | 101,707 | 36 | 0.832 |
| our MRPDU after a registering triple (JoinTime wait) | `srp.register_tx.t2.if0` | 16,608,282 | 166.083 | 220 | 220 | fits | 118,603 | 4 | 0.756 |
| ACMP's last record of its burst at a registering triple | `acmp.register_burst.t2.if0` | 125,539 | 1.255 | 20 | 20 | fits | 145,838 | 140 | 0.255 |
| AECP's last record of its burst at a registering triple | `aecp.register_burst.t2.if0` | 504,136 | 5.041 | 20 | 24 | fits | 86,275 | 48 | 0.518 |
| LINK_UP | `adp.link_up.if0` | 3,245 | 0.032 | 20 | 200 | fits | 30,074 | 44 (12) | 0.702 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,555 | 0.126 | 20 | 200 | fits | 21,294 | 23 (39) | 0.604 |
| LINK_DOWN | `adp.link_down.if0` | 1,935 | 0.019 | 20 | 200 | fits | 30,724 | 23 (9) | 0.667 |
| LINK_UP | `adp.link_up.if0` | 3,245 | 0.032 | 20 | 200 | fits | 30,074 | 44 (12) | 0.702 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,555 | 0.126 | 20 | 200 | fits | 21,294 | 23 (39) | 0.604 |
| GM_CHANGE | `adp.gm_change.if0` | 2,189 | 0.022 | 20 | 200 | fits | 15,971 | 17 (11) | 0.417 |
| LINK_UP | `adp.link_up.if0` | 3,245 | 0.032 | 20 | 200 | fits | 30,074 | 44 (12) | 0.702 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,555 | 0.126 | 20 | 200 | fits | 21,294 | 23 (39) | 0.604 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 5,393 | 0.054 | 20 | 200 | fits | 17,759 | 16 (31) | 0.569 |
| LINK_UP | `adp.link_up.if0` | 3,245 | 0.032 | 20 | 200 | fits | 30,074 | 44 (12) | 0.702 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,555 | 0.126 | 20 | 200 | fits | 21,294 | 23 (39) | 0.604 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 5,393 | 0.054 | 20 | 200 | fits | 17,759 | 16 (31) | 0.569 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 52,302 | 0.523 | 20 | 20 | fits | 14,485 | 9 | 0.845 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 40,752 | 0.408 | 20 | 20 | fits | 40,818 | 21 | 0.855 |
| malformed MRPDU discard | `srp.malformed.if0` | 24,043 | 0.240 | 20 | 20 | fits | 24,109 | 21 | 0.707 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 63,231 | 0.632 | 220 | 220 | fits | 34,104 | 7 | 0.919 |
| an event behind 15 others | `backlog.event.if0` | 167,128 | 1.671 | 20 | 200 | fits | 73,864 | 78 | 0.549 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 613,484 | 6.135 | 20 | 20 | fits | 144,142 | 131 | 0.275 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 493,205 | 4.932 | 20 | 200 | fits | 177,277 | 91 | 0.458 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 636,731 | 6.367 | 20 | 200 | fits | 144,142 | 131 | 0.275 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 488,883 | 4.889 | 20 | 20 | fits | 177,277 | 91 | 0.458 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 632,189 | 6.322 | 20 | 20 | fits | 144,142 | 131 | 0.275 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 157,088 | 1.571 | 20 | 24 | fits | 157,979 | 112 | 0.417 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 491,533 | 4.915 | 20 | 24 | fits | 177,277 | 91 | 0.458 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 491,467 | 4.915 | 20 | 50 | fits | 177,277 | 91 | 0.458 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 635,213 | 6.352 | 20 | 50 | fits | 144,142 | 131 | 0.275 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 686,124 | 6.861 | 20 | 20 | fits | 48,406 | 165 | 0.165 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 777,123 | 7.771 | 20 | 20 | fits | 42,375 | 118 | 0.199 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 544,911 | 5.449 | 20 | 20 | fits | 152,849 | 209 | 0.365 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 439,906 | 4.399 | 20 | 200 | fits | 149,718 | 115 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 592,139 | 5.921 | 20 | 200 | fits | 152,849 | 209 | 0.365 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 440,830 | 4.408 | 20 | 20 | fits | 149,718 | 115 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 730,019 | 7.300 | 20 | 20 | fits | 137,176 | 127 | 0.671 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 148,574 | 1.486 | 20 | 24 | fits | 148,760 | 109 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 443,480 | 4.435 | 20 | 24 | fits | 149,718 | 115 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 443,414 | 4.434 | 20 | 50 | fits | 149,718 | 115 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 595,867 | 5.959 | 20 | 50 | fits | 152,849 | 209 | 0.365 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 732,977 | 7.330 | 20 | 20 | fits | 137,176 | 127 | 0.671 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,087,585 | 10.876 | 20 | 20 | fits | 79,597 | 73 | 0.669 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 11,780 | 0.118 | 20 | 20 | fits | 27,849 | 19 | 0.740 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 439,906 | 4.399 | 20 | 200 | fits | 149,718 | 115 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 30,154 | 0.302 | 20 | 200 | fits | 27,849 | 19 | 0.740 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 440,830 | 4.408 | 20 | 20 | fits | 149,718 | 115 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 590,138 | 5.901 | 20 | 20 | fits | 150,144 | 208 | 0.305 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 148,574 | 1.486 | 20 | 24 | fits | 148,760 | 109 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 443,480 | 4.435 | 20 | 24 | fits | 149,718 | 115 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 443,414 | 4.434 | 20 | 50 | fits | 149,718 | 115 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 593,162 | 5.932 | 20 | 50 | fits | 150,144 | 208 | 0.305 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 728,334 | 7.283 | 20 | 20 | fits | 135,238 | 131 | 0.654 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,055,560 | 10.556 | 20 | 20 | fits | 58,961 | 51 | 0.698 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,402,113 | 64.021 | 20 | 20 | MISS ceiling | 19,903 | 13 | 0.541 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,425,828 | 64.258 | 20 | 20 | MISS ceiling | 22,824 | 18 | 0.648 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,444,941 | 64.449 | 20 | 20 | MISS ceiling | 21,854 | 13 | 0.558 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,466,730 | 64.667 | 20 | 20 | MISS ceiling | 20,530 | 13 | 0.600 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,486,788 | 64.868 | 20 | 20 | MISS ceiling | 19,740 | 13 | 0.542 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 312,665 | 3.127 | 20 | 200 | fits | 153,526 | 238 | 0.388 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 447,739 | 4.477 | 20 | 200 | fits | 135,690 | 135 | 0.642 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 308,343 | 3.083 | 20 | 20 | fits | 153,526 | 238 | 0.388 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,306,035 | 63.060 | 20 | 20 | MISS ceiling | 95,187 | 42 | 0.538 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 158,457 | 1.585 | 20 | 24 | fits | 147,093 | 107 | 0.413 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,309,521 | 63.095 | 20 | 24 | MISS ceiling | 95,187 | 42 | 0.538 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 310,927 | 3.109 | 20 | 50 | fits | 153,526 | 238 | 0.388 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 446,221 | 4.462 | 20 | 50 | fits | 135,690 | 135 | 0.642 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 446,155 | 4.462 | 20 | 20 | fits | 135,690 | 135 | 0.642 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 802,810 | 8.028 | 20 | 20 | fits | 91,883 | 86 | 0.665 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 6,693 | 0.067 | 20 | 20 | fits | 24,638 | 13 (29) | 0.707 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 8,400 | 0.084 | 20 | 20 | fits | 27,278 | 19 (35) | 0.744 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 17,235 | 0.172 | 20 | 20 | fits | 30,157 | 21 (12) | 0.786 |
| Talker Advertise RX for every input, bound | `srp.register_advertise.if0` | 105,204 | 1.052 | 20 | 20 | fits | 105,270 | 25 | 0.887 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 13,373 | 0.134 | 20 | 50 | fits | 30,074 | 44 | 0.702 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 13,113 | 0.131 | 20 | 50 | fits | 25,494 | 35 | 0.614 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 25,509 | 0.255 | 20 | 50 | fits | 28,146 | 41 | 0.576 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 20,046 | 0.200 | 20 | 50 | fits | 30,395 | 61 | 0.575 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 21,968 | 0.220 | 20 | 50 | fits | 30,395 | 61 | 0.575 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 11,396 | 0.114 | 20 | 50 | fits | 25,435 | 30 | 0.617 |
| set_name | `aecp_fanout.set_name.if0` | 60,036 | 0.600 | 20 | 24 | fits | 63,183 | 89 | 0.594 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 55,184 | 0.552 | 20 | 24 | fits | 57,100 | 78 | 0.624 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 55,532 | 0.555 | 20 | 24 | fits | 52,081 | 79 | 0.600 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 54,030 | 0.540 | 20 | 24 | fits | 51,035 | 78 | 0.593 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 62,420 | 0.624 | 20 | 24 | fits | 65,208 | 110 | 0.607 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 329,481 | 3.295 | 20 | 24 | fits | 61,147 | 109 | 0.580 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 343,487 | 3.435 | 20 | 24 | fits | 75,779 | 110 | 0.608 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 324,332 | 3.243 | 20 | 24 | fits | 74,095 | 109 | 0.603 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 305,652 | 3.057 | 20 | 24 | fits | 54,493 | 67 | 0.627 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 92,838 | 0.928 | 20 | 24 | fits | 95,532 | 77 | 0.637 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 252,839 | 2.528 | 20 | 24 | fits | 60,875 | 78 | 0.633 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 55,454 | 0.555 | 20 | 24 | fits | 51,631 | 78 | 0.599 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 54,894 | 0.549 | 20 | 24 | fits | 51,252 | 79 | 0.592 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 97,205 | 0.972 | 20 | 24 | fits | 41,348 | 59 | 0.486 |
| BIND_RX | `acmp.bind_rx.if0` | 20,212 | 0.202 | 20 | 20 | fits | 45,715 | 26 (77) | 0.801 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 10,113 | 0.101 | 20 | 20 | fits | 31,678 | 19 (32) | 0.826 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 11,361 | 0.114 | 20 | 20 | fits | 27,749 | 15 (47) | 0.778 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 14,448 | 0.144 | 20 | 20 | fits | 41,526 | 18 (50) | 0.843 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 11,104 | 0.111 | 20 | 20 | fits | 28,197 | 17 (48) | 0.758 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,811 | 0.098 | 20 | 20 | fits | 25,650 | 16 (48) | 0.673 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 8,655 | 0.087 | 20 | 20 | fits | 24,391 | 16 (48) | 0.651 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 8,973 | 0.090 | 20 | 20 | fits | 24,383 | 16 (48) | 0.651 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 14,180 | 0.142 | 20 | 24 | fits | 28,267 | 20 | 0.763 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 33,957 | 0.340 | 20 | 24 | fits | 42,041 | 20 | 0.720 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 18,132 | 0.181 | 20 | 24 | fits | 29,355 | 20 | 0.746 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 21,132 | 0.211 | 20 | 24 | fits | 28,999 | 20 | 0.737 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 21,148 | 0.211 | 20 | 24 | fits | 28,990 | 20 | 0.738 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 18,375 | 0.184 | 20 | 24 | fits | 29,332 | 20 | 0.738 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 20,914 | 0.209 | 20 | 24 | fits | 28,550 | 20 | 0.741 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 17,479 | 0.175 | 20 | 24 | fits | 28,303 | 20 | 0.751 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 21,026 | 0.210 | 20 | 24 | fits | 28,604 | 20 | 0.759 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 25,177 | 0.252 | 20 | 24 | fits | 36,949 | 27 | 0.646 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 17,555 | 0.176 | 20 | 24 | fits | 28,689 | 20 | 0.777 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 20,645 | 0.206 | 20 | 24 | fits | 28,346 | 20 | 0.776 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i79.c0.if0` | 17,880 | 0.179 | 20 | 24 | fits | 28,650 | 20 | 0.743 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 21,325 | 0.213 | 20 | 24 | fits | 29,007 | 20 | 0.744 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 17,928 | 0.179 | 20 | 24 | fits | 28,817 | 20 | 0.743 |
| get_configuration | `aecp.get_configuration.if0` | 15,805 | 0.158 | 20 | 24 | fits | 26,616 | 20 | 0.765 |
| entity_available | `aecp.entity_available.if0` | 18,836 | 0.188 | 20 | 24 | fits | 26,206 | 20 | 0.747 |
| get_name | `aecp.get_name.if0` | 18,550 | 0.185 | 20 | 24 | fits | 29,582 | 20 | 0.763 |
| get_counters | `aecp.get_counters.if0` | 23,186 | 0.232 | 20 | 24 | fits | 31,072 | 20 | 0.762 |
| get_avb_info | `aecp.get_avb_info.if0` | 18,240 | 0.182 | 20 | 24 | fits | 29,542 | 20 | 0.800 |
| get_as_path | `aecp.get_as_path.if0` | 26,642 | 0.266 | 20 | 24 | fits | 35,280 | 100 | 0.567 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 18,990 | 0.190 | 20 | 24 | fits | 26,668 | 20 | 0.771 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 14,802 | 0.148 | 20 | 24 | fits | 25,085 | 20 | 0.730 |
| set_name | `aecp.set_name.if0` | 28,682 | 0.287 | 20 | 24 | fits | 49,921 | 44 | 0.774 |
| lock_entity | `aecp.lock_entity.if0` | 21,917 | 0.219 | 20 | 24 | fits | 38,916 | 33 | 0.808 |
| unlock_entity | `aecp.unlock_entity.if0` | 26,281 | 0.263 | 20 | 24 | fits | 38,985 | 33 | 0.807 |
| REBOOT, refused BAD_ARGUMENTS | `aecp_reboot.short.if0` | 24,317 | 0.243 | 20 | 24 | fits | 29,975 | 17 | 0.791 |
| REBOOT, refused NOT_SUPPORTED | `aecp_reboot.stream_input.if0` | 21,853 | 0.219 | 20 | 24 | fits | 29,766 | 17 | 0.788 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | `aecp_reboot.entity_1.if0` | 24,166 | 0.242 | 20 | 24 | fits | 29,865 | 17 | 0.790 |
| REBOOT, refused ENTITY_LOCKED | `aecp_reboot.locked.if0` | 23,336 | 0.233 | 20 | 24 | fits | 30,929 | 17 | 0.809 |
| REBOOT | `aecp_reboot.accepted.if0` | 46,415 | 0.464 | 20 | 24 | fits | 43,960 | 66 | 0.560 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 145,188 | 1.452 | 20 | 24 | fits | 148,516 | 137 | 0.326 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 242,460 | 2.425 | 20 | 24 | fits | 140,473 | 119 | 0.288 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 231,846 | 2.318 | 20 | 24 | fits | 46,787 | 18 | 0.649 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 300,577 | 3.006 | 20 | 24 | fits | 79,204 | 17 | 0.651 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 333,176 | 3.332 | 20 | 24 | fits | 90,198 | 17 | 0.646 |
| READ_DESCRIPTOR held for a token (#917) | `aecp.held.read_descriptor.if0` | 523,054 | 5.231 | 20 | 24 | fits | 41,295 | 17 | 0.728 |
| LINK_UP | `fixture.link_up.if0` | 3,245 | 0.032 | 20 | 200 | fits | 30,074 | 44 (12) | 0.702 |
| malformed MRPDU discard | `fixture.malformed.if0` | 24,355 | 0.244 | 20 | 20 | fits | 24,421 | 21 | 0.712 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 34,529 | 0.345 | 20 | 24 | fits | 50,176 | 43 | 0.781 |
| LINK_DOWN | `fixture.link_down.if0` | 2,300 | 0.023 | 20 | 200 | fits | 33,026 | 23 (9) | 0.727 |
| BIND_RX | `fixture.bind_rx.if0` | 20,429 | 0.204 | 20 | 20 | fits | 45,977 | 26 (77) | 0.809 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 25,373 | 0.254 | 20 | 20 | fits | 37,934 | 29 (35) | 0.770 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 6,977 | 0.070 | 20 | 20 | fits | 26,091 | 13 (29) | 0.750 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 96,085 | 0.961 | 20 | 200 | fits | 96,189 | 86 | 0.730 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 96,085 | 0.961 | 20 | 200 | fits | 96,189 | 86 | 0.730 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 95,811 | 0.958 | 20 | 20 | fits | 96,189 | 86 | 0.730 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 95,811 | 0.958 | 20 | 20 | fits | 96,189 | 86 | 0.730 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 96,019 | 0.960 | 20 | 24 | fits | 96,189 | 86 | 0.730 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 96,019 | 0.960 | 20 | 24 | fits | 96,189 | 86 | 0.730 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 95,953 | 0.960 | 20 | 50 | fits | 96,189 | 86 | 0.730 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 95,953 | 0.960 | 20 | 50 | fits | 96,189 | 86 | 0.730 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 95,887 | 0.959 | 20 | 20 | fits | 96,189 | 86 | 0.730 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 95,887 | 0.959 | 20 | 20 | fits | 96,189 | 86 | 0.730 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
