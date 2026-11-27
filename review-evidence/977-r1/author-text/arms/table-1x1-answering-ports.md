### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 127 paths and 7 of 997 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.191 (0.380) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.089 (0.197) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.070 (0.202) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.154 (0.408) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.112 (0.226) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.089 (0.197) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.094 (0.209) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.115 (0.227) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.095 (0.263) | fits | 0 acmp | 1 | 0 |
| ACMP's last record of its burst at a registering triple | 0 | `acmp.register_burst.t0.if0` (srp-register-burst) | 1.442 (2.545) | fits | 11 acmp | 1 | 0 |
| ACMP's last record of its burst at a registering triple | 0 | `acmp.register_burst.t1.if0` (srp-register-burst) | 2.349 (3.175) | fits | 11 acmp | 1 | 0 |
| ACMP's last record of its burst at a registering triple | 0 | `acmp.register_burst.t2.if0` (srp-register-burst) | 1.046 (1.249) | fits | 11 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.104 (0.369) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.105 (0.370) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.134 (0.404) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.065 (0.340) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.090 (0.415) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.076 (0.329) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.133 (0.342) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.047 (0.132) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.021 (0.118) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.025 (0.220) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.032 (0.239) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.068 (0.187) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.116 (0.344) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.128 (0.369) | fits | 0 aecp | 1 | 0 |
| get_as_path | 0 | `aecp.get_as_path.if0` (aecp) | 0.209 (0.466) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.182 (0.434) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.150 (0.394) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.179 (0.432) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.171 (0.421) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR held for a token (#917) | 0 | `aecp.held.read_descriptor.if0` (aecp-held) | 5.147 (5.394) | fits | 16 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.211 (0.518) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.144 (0.385) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.207 (0.459) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.159 (0.408) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.153 (0.399) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.167 (0.416) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.174 (0.423) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.166 (0.418) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.143 (0.392) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.171 (0.423) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.170 (0.421) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.156 (0.404) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.150 (0.400) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.160 (0.408) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.178 (0.428) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.171 (0.420) | fits | 0 aecp | 1 | 0 |
| AECP's last record of its burst at a registering triple | 0 | `aecp.register_burst.t0.if0` (srp-register-burst) | 1.752 (2.005) | fits | 15 aecp | 1 | 0 |
| AECP's last record of its burst at a registering triple | 0 | `aecp.register_burst.t1.if0` (srp-register-burst) | 2.510 (3.033) | fits | 15 aecp | 1 | 0 |
| AECP's last record of its burst at a registering triple | 0 | `aecp.register_burst.t2.if0` (srp-register-burst) | 2.916 (3.748) | fits | 15 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.109 (0.238) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.214 (0.571) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.150 (0.398) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.192 (0.516) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.733 (3.011) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 3.452 (3.706) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 0.724 (0.910) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.357 (0.613) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.489 (0.743) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 3.462 (3.718) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.404 (0.652) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 0.515 (0.759) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.372 (0.601) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.418 (0.685) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.344 (3.587) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 3.559 (3.843) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.389 (0.622) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 3.377 (3.625) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.402 (2.707) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.936 (4.242) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.520 (3.825) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.370 (1.504) | fits | 0 aecp | 1 | 0 |
| REBOOT | 0 | `aecp_reboot.accepted.if0` (aecp-reboot) | 0.321 (0.533) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | 0 | `aecp_reboot.entity_1.if0` (aecp-reboot) | 0.097 (0.384) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused ENTITY_LOCKED | 0 | `aecp_reboot.locked.if0` (aecp-reboot) | 0.111 (0.423) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused BAD_ARGUMENTS | 0 | `aecp_reboot.short.if0` (aecp-reboot) | 0.094 (0.382) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NOT_SUPPORTED | 0 | `aecp_reboot.stream_input.if0` (aecp-reboot) | 0.109 (0.399) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.520 (3.711) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 3.918 (4.453) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.107 (0.352) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.486 (1.855) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.460 (62.586) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.039 (63.166) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.302 (0.426) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-flight.held.acmp.if0` (save-flight) | 2.261 | fits | 11 acmp | 4 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-burst.held.adp.if0` (save-burst) | 1.548 | fits | 7 adp | 4 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-flight.held.aecp.if0` (save-flight) | 2.714 | fits | 14 aecp | 4 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 2.030 | fits | 6 maap | 4 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 7.905 | fits | 31 srp | 4 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.193 (0.443) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.087 (0.183) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.105 (0.239) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.174 (0.443) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.158 (0.387) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 1.678 | fits | 0 srp | 4 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 3.665 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 61.740 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 3.709 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 4.447 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@program-7.service.aecp.first.if0` (backlog-adp@program-7) | 2.156 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.521 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 3.691 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.maap.last.if0` (backlog-adp@program-aged2-7) | 4.484 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-6.service.srp.first.if0` (backlog-adp@program-aged2-6) | 5.311 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-5.service.srp.last.if0` (backlog-adp@program-aged2-5) | 9.435 | fits | 31 srp | 77 | 0 |
| Talker Advertise RX for every input, bound | 0 | `srp.bound_advertise.if0` (srp-bound) | 0.493 (0.493) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.576 (0.655) | fits | 0 srp | 1 | 0 |
| Talker Advertise RX for every input, no binding (kept) | 0 | `srp.kept_advertise.if0` (srp-kept) | 0.434 (0.434) | fits | 0 srp | 1 | 0 |
| Talker Failed RX for every input, no binding (kept) | 0 | `srp.kept_failed.if0` (srp-kept) | 0.442 (0.443) | fits | 0 srp | 1 | 0 |
| Talker RX at the bound after a freed block (count) | 0 | `srp.kept_recount.if0` (srp-kept) | 0.405 (0.406) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.343 (0.344) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.188 (0.189) | fits | 0 srp | 2 | 0 |
| Talker Advertise RX for every input, bound | 0 | `srp.register_advertise.if0` (srp-register) | 0.491 (0.491) | fits | 0 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t0.r0.if0` (srp-register-burst) | 1.022 (1.150) | fits | 0 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t0.r1.if0` (srp-register-burst) | 1.021 (1.149) | fits | 1 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t0.r2.if0` (srp-register-burst) | 1.020 (1.148) | fits | 2 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t1.r0.if0` (srp-register-burst) | 0.633 (0.760) | fits | 0 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t1.r1.if0` (srp-register-burst) | 0.632 (0.759) | fits | 1 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t1.r2.if0` (srp-register-burst) | 0.631 (0.758) | fits | 2 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t2.r0.if0` (srp-register-burst) | 0.855 (0.982) | fits | 0 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t2.r1.if0` (srp-register-burst) | 0.854 (0.981) | fits | 1 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t2.r2.if0` (srp-register-burst) | 0.853 (0.980) | fits | 2 srp | 1 | 0 |
| our MRPDU after a registering triple (JoinTime wait) | 0 | `srp.register_tx.t0.if0` (srp-register-burst) | 1.318 (1.587) | fits | 2 srp | 1 | 0 |
| our MRPDU after a registering triple (JoinTime wait) | 0 | `srp.register_tx.t1.if0` (srp-register-burst) | 76.704 (77.008) | fits | 2 srp | 1 | 0 |
| our MRPDU after a registering triple (JoinTime wait) | 0 | `srp.register_tx.t2.if0` (srp-register-burst) | 156.683 (156.986) | fits | 2 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.475 (0.558) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.888 | 9 | 147,968 (1.480) | yes | - |
| backlog-adp@blank-1 | 0 | 11.763 | 9 | 147,968 (1.480) | yes | - |
| backlog-adp@blank-2 | 0 | 11.638 | 9 | 147,968 (1.480) | yes | - |
| backlog-adp@blank-3 | 0 | 11.513 | 9 | 147,968 (1.480) | yes | - |
| backlog-adp@blank-4 | 0 | 11.388 | 9 | 147,968 (1.480) | yes | - |
| backlog-adp@blank-5 | 0 | 11.263 | 9 | 147,968 (1.480) | yes | - |
| backlog-adp@blank-6 | 0 | 11.154 | 8 | 144,342 (1.443) | yes | - |
| backlog-adp@blank-7 | 0 | 13.740 | 10 | 147,107 (1.471) | yes | - |
| backlog-adp@program-0 | 0 | 10.222 | 9 | 143,095 (1.431) | yes | - |
| backlog-adp@program-1 | 0 | 9.972 | 9 | 143,095 (1.431) | yes | - |
| backlog-adp@program-2 | 0 | 10.632 | 9 | 144,186 (1.442) | yes | - |
| backlog-adp@program-3 | 0 | 10.534 | 9 | 143,930 (1.439) | yes | - |
| backlog-adp@program-4 | 0 | 10.284 | 9 | 143,930 (1.439) | yes | - |
| backlog-adp@program-5 | 0 | 10.034 | 9 | 143,930 (1.439) | yes | - |
| backlog-adp@program-6 | 0 | 10.758 | 9 | 148,317 (1.483) | yes | - |
| backlog-adp@program-7 | 0 | 10.617 | 9 | 143,150 (1.431) | yes | - |
| backlog-adp@verify-0 | 0 | 11.821 | 9 | 147,995 (1.480) | yes | - |
| backlog-adp@verify-1 | 0 | 11.696 | 9 | 147,995 (1.480) | yes | - |
| backlog-adp@verify-2 | 0 | 11.571 | 9 | 147,995 (1.480) | yes | - |
| backlog-adp@verify-3 | 0 | 11.446 | 9 | 147,995 (1.480) | yes | - |
| backlog-adp@verify-4 | 0 | 11.321 | 9 | 147,995 (1.480) | yes | - |
| backlog-adp@verify-5 | 0 | 11.196 | 9 | 147,995 (1.480) | yes | - |
| backlog-adp@verify-6 | 0 | 11.949 | 9 | 146,579 (1.466) | yes | - |
| backlog-adp@verify-7 | 0 | 11.824 | 9 | 146,579 (1.466) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 12.089 | 9 | 143,926 (1.439) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 11.220 | 10 | 143,893 (1.439) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 12.042 | 9 | 148,043 (1.480) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 11.983 | 9 | 143,113 (1.431) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 11.974 | 9 | 143,058 (1.431) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 11.929 | 9 | 143,912 (1.439) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 11.939 | 9 | 143,893 (1.439) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 13.770 | 10 | 147,311 (1.473) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 12.128 | 10 | 143,893 (1.439) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 11.229 | 9 | 148,043 (1.480) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 11.177 | 9 | 143,113 (1.431) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 11.169 | 9 | 143,058 (1.431) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 11.143 | 9 | 143,912 (1.439) | yes | - |
| backlog-adp@blank-aged1-5 | 1 | 11.118 | 8 | 144,761 (1.448) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 11.135 | 8 | 143,504 (1.435) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 11.129 | 8 | 143,981 (1.440) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 10.811 | 10 | 143,893 (1.439) | yes | - |
| backlog-adp@program-aged2-1 | 1 | 10.537 | 9 | 143,504 (1.435) | yes | - |
| backlog-adp@program-aged2-2 | 1 | 10.625 | 8 | 143,981 (1.440) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 10.642 | 8 | 143,926 (1.439) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 10.694 | 9 | 143,893 (1.439) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 10.725 | 9 | 148,043 (1.480) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 10.678 | 9 | 143,113 (1.431) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 10.670 | 9 | 146,402 (1.464) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 10.888 | 10 | 143,113 (1.431) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.706 | 10 | 143,058 (1.431) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 10.602 | 9 | 143,912 (1.439) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 10.587 | 9 | 143,893 (1.439) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 10.637 | 9 | 148,043 (1.480) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 10.565 | 9 | 143,113 (1.431) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 10.570 | 9 | 143,058 (1.431) | yes | - |
| backlog-adp@program-aged1-7 | 1 | 10.554 | 8 | 144,780 (1.448) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 12.129 | 9 | 143,519 (1.435) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 11.258 | 10 | 143,057 (1.431) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 12.020 | 9 | 143,911 (1.439) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 12.008 | 9 | 143,892 (1.439) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 12.058 | 9 | 148,058 (1.481) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 11.975 | 9 | 143,112 (1.431) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 11.982 | 9 | 143,057 (1.431) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 13.827 | 10 | 148,525 (1.485) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 12.180 | 10 | 143,057 (1.431) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 11.282 | 10 | 143,911 (1.439) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 11.185 | 9 | 143,892 (1.439) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 11.239 | 9 | 148,058 (1.481) | yes | - |
| backlog-adp@verify-aged1-4 | 1 | 11.177 | 8 | 143,980 (1.440) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 11.164 | 8 | 143,925 (1.439) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 11.169 | 8 | 144,779 (1.448) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 11.239 | 9 | 147,218 (1.472) | yes | - |
| backlog | 0 | 5.248 | 7 | 139,368 (1.394) | yes | - |
| backlog-adp | 0 | 8.955 | 9 | 148,665 (1.487) | yes | - |
| backlog-adp-refill | 0 | 40.733 | 16 | 148,665 (1.487) | yes | - |
| backlog-owed | 0 | 63.515 | 25 | 147,147 (1.471) | yes | - |
| fixture | 0 | 1.134 | 2 | 77,011 (0.770) | yes | - |

Composed maximum over the 4 backlog windows: 148,665 CPU cycles (1.487 ms), backlog-adp.
Over the windows that released their whole load only: 148,665 (1.487 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-kept | 1909 | 0 | 44,298 (0.443) | fits |
| save-flight | 2990 | 0 | 155,658 (1.557) | fits |
| save-burst | 2742 | 0 | 155,658 (1.557) | fits |
| acmp-notk | 1103 | 0 | 47,266 (0.473) | fits |
| save-second | 66939 | 0 | 44,813 (0.448) | fits |
| adp-advertise | 880 | 0 | 23,900 (0.239) | fits |
| backlog-adp@blank-0 | 346 | 0 | 147,968 (1.480) | fits |
| backlog-adp@blank-1 | 346 | 0 | 147,968 (1.480) | fits |
| backlog-adp@blank-2 | 346 | 0 | 147,968 (1.480) | fits |
| backlog-adp@blank-3 | 346 | 0 | 147,968 (1.480) | fits |
| backlog-adp@blank-4 | 346 | 0 | 147,968 (1.480) | fits |
| backlog-adp@blank-5 | 346 | 0 | 147,968 (1.480) | fits |
| backlog-adp@blank-6 | 346 | 0 | 144,342 (1.443) | fits |
| backlog-adp@blank-7 | 347 | 0 | 147,107 (1.471) | fits |
| backlog-adp@program-0 | 349 | 0 | 143,095 (1.431) | fits |
| backlog-adp@program-1 | 349 | 0 | 143,095 (1.431) | fits |
| backlog-adp@program-2 | 349 | 0 | 144,186 (1.442) | fits |
| backlog-adp@program-3 | 349 | 0 | 143,930 (1.439) | fits |
| backlog-adp@program-4 | 349 | 0 | 143,930 (1.439) | fits |
| backlog-adp@program-5 | 349 | 0 | 143,930 (1.439) | fits |
| backlog-adp@program-6 | 349 | 0 | 148,317 (1.483) | fits |
| backlog-adp@program-7 | 349 | 0 | 143,150 (1.431) | fits |
| backlog-adp@verify-0 | 350 | 0 | 147,995 (1.480) | fits |
| backlog-adp@verify-1 | 350 | 0 | 147,995 (1.480) | fits |
| backlog-adp@verify-2 | 350 | 0 | 147,995 (1.480) | fits |
| backlog-adp@verify-3 | 350 | 0 | 147,995 (1.480) | fits |
| backlog-adp@verify-4 | 350 | 0 | 147,995 (1.480) | fits |
| backlog-adp@verify-5 | 350 | 0 | 147,995 (1.480) | fits |
| backlog-adp@verify-6 | 350 | 0 | 146,579 (1.466) | fits |
| backlog-adp@verify-7 | 350 | 0 | 146,579 (1.466) | fits |
| backlog-adp@blank-aged2-0 | 738 | 0 | 143,926 (1.439) | fits |
| backlog-adp@blank-aged2-1 | 750 | 0 | 143,893 (1.439) | fits |
| backlog-adp@blank-aged2-2 | 760 | 0 | 148,043 (1.480) | fits |
| backlog-adp@blank-aged2-3 | 771 | 0 | 143,113 (1.431) | fits |
| backlog-adp@blank-aged2-4 | 782 | 0 | 143,058 (1.431) | fits |
| backlog-adp@blank-aged2-5 | 793 | 0 | 143,912 (1.439) | fits |
| backlog-adp@blank-aged2-6 | 804 | 0 | 143,893 (1.439) | fits |
| backlog-adp@blank-aged2-7 | 816 | 0 | 147,311 (1.473) | fits |
| backlog-adp@blank-aged1-0 | 650 | 0 | 143,893 (1.439) | fits |
| backlog-adp@blank-aged1-1 | 660 | 0 | 148,043 (1.480) | fits |
| backlog-adp@blank-aged1-2 | 671 | 0 | 143,113 (1.431) | fits |
| backlog-adp@blank-aged1-3 | 682 | 0 | 143,058 (1.431) | fits |
| backlog-adp@blank-aged1-4 | 693 | 0 | 143,912 (1.439) | fits |
| backlog-adp@blank-aged1-5 | 704 | 0 | 144,761 (1.448) | fits |
| backlog-adp@blank-aged1-6 | 715 | 0 | 143,504 (1.435) | fits |
| backlog-adp@blank-aged1-7 | 726 | 0 | 143,981 (1.440) | fits |
| backlog-adp@program-aged2-0 | 701 | 0 | 143,893 (1.439) | fits |
| backlog-adp@program-aged2-1 | 712 | 0 | 143,504 (1.435) | fits |
| backlog-adp@program-aged2-2 | 722 | 0 | 143,981 (1.440) | fits |
| backlog-adp@program-aged2-3 | 733 | 0 | 143,926 (1.439) | fits |
| backlog-adp@program-aged2-4 | 745 | 0 | 143,893 (1.439) | fits |
| backlog-adp@program-aged2-5 | 756 | 0 | 148,043 (1.480) | fits |
| backlog-adp@program-aged2-6 | 767 | 0 | 143,113 (1.431) | fits |
| backlog-adp@program-aged2-7 | 778 | 0 | 146,402 (1.464) | fits |
| backlog-adp@program-aged1-0 | 613 | 0 | 143,113 (1.431) | fits |
| backlog-adp@program-aged1-1 | 624 | 0 | 143,058 (1.431) | fits |
| backlog-adp@program-aged1-2 | 634 | 0 | 143,912 (1.439) | fits |
| backlog-adp@program-aged1-3 | 645 | 0 | 143,893 (1.439) | fits |
| backlog-adp@program-aged1-4 | 656 | 0 | 148,043 (1.480) | fits |
| backlog-adp@program-aged1-5 | 667 | 0 | 143,113 (1.431) | fits |
| backlog-adp@program-aged1-6 | 678 | 0 | 143,058 (1.431) | fits |
| backlog-adp@program-aged1-7 | 689 | 0 | 144,780 (1.448) | fits |
| backlog-adp@verify-aged2-0 | 727 | 0 | 143,519 (1.435) | fits |
| backlog-adp@verify-aged2-1 | 739 | 0 | 143,057 (1.431) | fits |
| backlog-adp@verify-aged2-2 | 749 | 0 | 143,911 (1.439) | fits |
| backlog-adp@verify-aged2-3 | 760 | 0 | 143,892 (1.439) | fits |
| backlog-adp@verify-aged2-4 | 771 | 0 | 148,058 (1.481) | fits |
| backlog-adp@verify-aged2-5 | 782 | 0 | 143,112 (1.431) | fits |
| backlog-adp@verify-aged2-6 | 793 | 0 | 143,057 (1.431) | fits |
| backlog-adp@verify-aged2-7 | 805 | 0 | 148,525 (1.485) | fits |
| backlog-adp@verify-aged1-0 | 639 | 0 | 143,057 (1.431) | fits |
| backlog-adp@verify-aged1-1 | 650 | 0 | 143,911 (1.439) | fits |
| backlog-adp@verify-aged1-2 | 660 | 0 | 143,892 (1.439) | fits |
| backlog-adp@verify-aged1-3 | 671 | 0 | 148,058 (1.481) | fits |
| backlog-adp@verify-aged1-4 | 682 | 0 | 143,980 (1.440) | fits |
| backlog-adp@verify-aged1-5 | 693 | 0 | 143,925 (1.439) | fits |
| backlog-adp@verify-aged1-6 | 704 | 0 | 144,779 (1.448) | fits |
| backlog-adp@verify-aged1-7 | 716 | 0 | 147,218 (1.472) | fits |
| save-held | 1404 | 0 | 155,658 (1.557) | fits |
| save-starved | 35815 | 0 | 155,658 (1.557) | fits |
| srp-bound | 518 | 0 | 49,323 (0.493) | fits |
| acmp-noresp | 648 | 0 | 46,496 (0.465) | fits |
| save | 609 | 0 | 41,039 (0.410) | fits |
| srp-register-burst | 628 | 0 | 147,180 (1.472) | fits |
| adp-link | 373 | 0 | 31,563 (0.316) | fits |
| adp-gm | 372 | 0 | 23,900 (0.239) | fits |
| adp-discover | 372 | 0 | 23,900 (0.239) | fits |
| control | 372 | 0 | 23,900 (0.239) | fits |
| srp | 289 | 0 | 34,357 (0.344) | fits |
| backlog | 285 | 0 | 139,368 (1.394) | fits |
| backlog-adp | 296 | 0 | 148,665 (1.487) | fits |
| backlog-adp-refill | 303 | 0 | 148,665 (1.487) | fits |
| backlog-owed | 309 | 0 | 147,147 (1.471) | fits |
| acmp-disc | 331 | 0 | 46,543 (0.465) | fits |
| maap | 177 | 0 | 23,900 (0.239) | fits |
| aecp-fanout | 122 | 0 | 59,825 (0.598) | fits |
| acmp-cmd | 81 | 0 | 37,920 (0.379) | fits |
| aecp | 112 | 0 | 41,371 (0.414) | fits |
| srp-register | 157 | 0 | 49,141 (0.491) | fits |
| aecp-reboot | 108 | 0 | 45,774 (0.458) | fits |
| aecp-largest-notice | 106 | 0 | 150,373 (1.504) | fits |
| aecp-held | 108 | 0 | 31,022 (0.310) | fits |
| datapath-events | 108 | 0 | 23,900 (0.239) | fits |
| fixture | 68 | 0 | 77,011 (0.770) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 8.460 (20) | 11.540 |
| backlog-adp@blank-aged2-1 | 2 | none | +8.726 ms, 76,354 (0.764 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 8.538 (20) | 11.462 |
| backlog-adp@blank-aged2-2 | 2 | +8.273 ms, 76,690 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 9.412 (20) | 10.588 |
| backlog-adp@blank-aged2-3 | 2 | +7.139 ms, 76,690 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 9.353 (20) | 10.647 |
| backlog-adp@blank-aged2-4 | 2 | +5.424 ms, 76,773 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 9.344 (20) | 10.656 |
| backlog-adp@blank-aged2-5 | 2 | none | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 9.298 (20) | 10.702 |
| backlog-adp@blank-aged2-6 | 2 | +3.668 ms, 76,566 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 9.308 (20) | 10.692 |
| backlog-adp@blank-aged2-7 | 2 | +2.838 ms, 76,335 (0.763 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 9.285 (20) | 10.715 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 8.499 (20) | 11.501 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 8.595 (20) | 11.405 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 8.543 (20) | 11.457 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 8.536 (20) | 11.464 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 8.510 (20) | 11.490 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 8.484 (20) | 11.516 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 8.501 (20) | 11.499 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 8.495 (20) | 11.505 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 8.458 (20) | 11.542 |
| backlog-adp@program-aged2-1 | 2 | none | +8.632 ms, 80,525 (0.805 ms), issue | `backlog-adp@program-aged2-1.service.srp.last.if0` | 8.444 (20) | 11.556 |
| backlog-adp@program-aged2-2 | 2 | +7.918 ms, 80,745 (0.807 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 9.333 (20) | 10.667 |
| backlog-adp@program-aged2-3 | 2 | +7.084 ms, 80,745 (0.807 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 9.350 (20) | 10.650 |
| backlog-adp@program-aged2-4 | 2 | +5.432 ms, 80,828 (0.808 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 9.404 (20) | 10.596 |
| backlog-adp@program-aged2-5 | 2 | none | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 9.435 (20) | 10.565 |
| backlog-adp@program-aged2-6 | 2 | +3.696 ms, 80,707 (0.807 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 9.387 (20) | 10.613 |
| backlog-adp@program-aged2-7 | 2 | +2.855 ms, 80,589 (0.806 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 9.378 (20) | 10.622 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 8.535 (20) | 11.465 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 8.528 (20) | 11.472 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 8.556 (20) | 11.444 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 8.543 (20) | 11.457 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 8.592 (20) | 11.408 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 8.520 (20) | 11.480 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 8.525 (20) | 11.475 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 8.509 (20) | 11.491 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 8.453 (20) | 11.547 |
| backlog-adp@verify-aged2-1 | 2 | none | +8.731 ms, 77,369 (0.774 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 8.543 (20) | 11.457 |
| backlog-adp@verify-aged2-2 | 2 | +7.979 ms, 77,705 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 9.357 (20) | 10.643 |
| backlog-adp@verify-aged2-3 | 2 | +7.115 ms, 77,705 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 9.343 (20) | 10.657 |
| backlog-adp@verify-aged2-4 | 2 | +5.688 ms, 77,818 (0.778 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 9.393 (20) | 10.607 |
| backlog-adp@verify-aged2-5 | 2 | none | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 9.310 (20) | 10.690 |
| backlog-adp@verify-aged2-6 | 2 | +3.665 ms, 77,515 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 9.316 (20) | 10.684 |
| backlog-adp@verify-aged2-7 | 2 | +2.843 ms, 77,256 (0.773 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 9.286 (20) | 10.714 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 8.504 (20) | 11.496 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 8.481 (20) | 11.519 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 8.518 (20) | 11.482 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 8.572 (20) | 11.428 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 8.510 (20) | 11.490 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 8.497 (20) | 11.503 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 8.501 (20) | 11.499 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 8.572 (20) | 11.428 |

Least margin over the aged windows: 10.565 ms, `backlog-adp@program-aged2-5.service.srp.last.if0` at 9.435 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.447 | 6,070 | 102 | 2 | 30.762 | yes | within |
| save-held | 1085.109 | 4,070 | 102 | - | 21.188 | no | within |
| save-starved | 4049.071 | 4,070 | 102 | - | 30.888 | yes | within |
| save | 1076.434 | 4,070 | 102 | - | 24.106 | no | within |

Names from their response to durable (save_burst.py; #920, #665's ruling of 2026-11-15, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-flight | 1 | 147.501 (0) | 5,000 | 2 | - | - | 19 steps (want 19), 5.974 ms | within |
| save-burst | 39 | 1099.115 (0) | 5,000 | 1 | - | - | sequence 1, 0 missing | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-kept | 1844 | 19,199 (0.192) | 2,258 (0.023) |
| save-flight | 1554 | 91,715 (0.917) | 78,562 (0.786) |
| save-burst | 1479 | 91,314 (0.913) | 78,216 (0.782) |
| acmp-notk | 1159 | 91,921 (0.919) | 78,216 (0.782) |
| save-second | 520 | 80,519 (0.805) | 78,086 (0.781) |
| adp-advertise | 853 | 18,959 (0.190) | 2,258 (0.023) |
| backlog-adp@blank-0 | 342 | 87,997 (0.880) | 75,956 (0.760) |
| backlog-adp@blank-1 | 342 | 87,997 (0.880) | 75,956 (0.760) |
| backlog-adp@blank-2 | 342 | 87,997 (0.880) | 75,956 (0.760) |
| backlog-adp@blank-3 | 342 | 87,997 (0.880) | 75,956 (0.760) |
| backlog-adp@blank-4 | 342 | 87,997 (0.880) | 75,956 (0.760) |
| backlog-adp@blank-5 | 342 | 87,997 (0.880) | 75,956 (0.760) |
| backlog-adp@blank-6 | 342 | 87,997 (0.880) | 75,956 (0.760) |
| backlog-adp@blank-7 | 345 | 87,978 (0.880) | 75,956 (0.760) |
| backlog-adp@program-0 | 371 | 91,324 (0.913) | 78,137 (0.781) |
| backlog-adp@program-1 | 371 | 91,324 (0.913) | 78,137 (0.781) |
| backlog-adp@program-2 | 372 | 92,288 (0.923) | 78,608 (0.786) |
| backlog-adp@program-3 | 373 | 91,324 (0.913) | 78,137 (0.781) |
| backlog-adp@program-4 | 373 | 91,324 (0.913) | 78,137 (0.781) |
| backlog-adp@program-5 | 373 | 91,324 (0.913) | 78,137 (0.781) |
| backlog-adp@program-6 | 374 | 92,249 (0.922) | 78,608 (0.786) |
| backlog-adp@program-7 | 375 | 91,324 (0.913) | 78,137 (0.781) |
| backlog-adp@verify-0 | 398 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-1 | 398 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-2 | 398 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-3 | 398 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-4 | 398 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-5 | 398 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-6 | 399 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-7 | 399 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@blank-aged2-0 | 340 | 88,158 (0.882) | 76,245 (0.762) |
| backlog-adp@blank-aged2-1 | 339 | 87,313 (0.873) | 75,744 (0.757) |
| backlog-adp@blank-aged2-2 | 340 | 87,615 (0.876) | 75,789 (0.758) |
| backlog-adp@blank-aged2-3 | 340 | 87,740 (0.877) | 75,796 (0.758) |
| backlog-adp@blank-aged2-4 | 340 | 87,740 (0.877) | 75,796 (0.758) |
| backlog-adp@blank-aged2-5 | 340 | 90,039 (0.900) | 75,960 (0.760) |
| backlog-adp@blank-aged2-6 | 340 | 87,836 (0.878) | 75,923 (0.759) |
| backlog-adp@blank-aged2-7 | 342 | 87,855 (0.879) | 75,923 (0.759) |
| backlog-adp@blank-aged1-0 | 340 | 88,158 (0.882) | 76,245 (0.762) |
| backlog-adp@blank-aged1-1 | 339 | 88,104 (0.881) | 76,194 (0.762) |
| backlog-adp@blank-aged1-2 | 339 | 88,138 (0.881) | 76,194 (0.762) |
| backlog-adp@blank-aged1-3 | 339 | 88,138 (0.881) | 76,194 (0.762) |
| backlog-adp@blank-aged1-4 | 339 | 88,152 (0.882) | 76,194 (0.762) |
| backlog-adp@blank-aged1-5 | 339 | 88,158 (0.882) | 76,245 (0.762) |
| backlog-adp@blank-aged1-6 | 339 | 88,177 (0.882) | 76,245 (0.762) |
| backlog-adp@blank-aged1-7 | 339 | 88,158 (0.882) | 76,245 (0.762) |
| backlog-adp@program-aged2-0 | 369 | 92,185 (0.922) | 78,659 (0.787) |
| backlog-adp@program-aged2-1 | 368 | 91,317 (0.913) | 78,302 (0.783) |
| backlog-adp@program-aged2-2 | 369 | 91,066 (0.911) | 78,347 (0.783) |
| backlog-adp@program-aged2-3 | 369 | 91,072 (0.911) | 78,347 (0.783) |
| backlog-adp@program-aged2-4 | 369 | 91,011 (0.910) | 78,347 (0.783) |
| backlog-adp@program-aged2-5 | 369 | 93,514 (0.935) | 78,518 (0.785) |
| backlog-adp@program-aged2-6 | 369 | 90,925 (0.909) | 78,246 (0.782) |
| backlog-adp@program-aged2-7 | 369 | 91,115 (0.911) | 78,137 (0.781) |
| backlog-adp@program-aged1-0 | 369 | 92,185 (0.922) | 78,659 (0.787) |
| backlog-adp@program-aged1-1 | 368 | 91,317 (0.913) | 78,590 (0.786) |
| backlog-adp@program-aged1-2 | 368 | 92,179 (0.922) | 78,608 (0.786) |
| backlog-adp@program-aged1-3 | 368 | 92,165 (0.922) | 78,608 (0.786) |
| backlog-adp@program-aged1-4 | 368 | 92,184 (0.922) | 78,608 (0.786) |
| backlog-adp@program-aged1-5 | 368 | 92,185 (0.922) | 78,659 (0.787) |
| backlog-adp@program-aged1-6 | 368 | 92,185 (0.922) | 78,659 (0.787) |
| backlog-adp@program-aged1-7 | 368 | 92,199 (0.922) | 78,659 (0.787) |
| backlog-adp@verify-aged2-0 | 399 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-aged2-1 | 398 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-aged2-2 | 399 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-aged2-3 | 399 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-aged2-4 | 399 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-aged2-5 | 399 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-aged2-6 | 399 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-aged2-7 | 401 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-aged1-0 | 399 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-aged1-1 | 398 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-aged1-2 | 398 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-aged1-3 | 398 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-aged1-4 | 398 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-aged1-5 | 398 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-aged1-6 | 398 | 91,324 (0.913) | 78,216 (0.782) |
| backlog-adp@verify-aged1-7 | 398 | 91,324 (0.913) | 78,216 (0.782) |
| save-held | 816 | 91,077 (0.911) | 78,216 (0.782) |
| save-starved | 418 | 80,830 (0.808) | 78,449 (0.784) |
| srp-bound | 583 | 92,065 (0.921) | 78,279 (0.783) |
| acmp-noresp | 709 | 91,251 (0.913) | 78,216 (0.782) |
| save | 680 | 91,251 (0.913) | 78,216 (0.782) |
| srp-register-burst | 497 | 91,971 (0.920) | 78,216 (0.782) |
| adp-link | 355 | 18,959 (0.190) | 2,258 (0.023) |
| adp-gm | 355 | 18,959 (0.190) | 2,258 (0.023) |
| adp-discover | 355 | 18,959 (0.190) | 2,258 (0.023) |
| control | 355 | 18,959 (0.190) | 2,258 (0.023) |
| srp | 271 | 18,959 (0.190) | 2,258 (0.023) |
| backlog | 265 | 18,959 (0.190) | 2,258 (0.023) |
| backlog-adp | 271 | 18,959 (0.190) | 2,258 (0.023) |
| backlog-adp-refill | 274 | 18,959 (0.190) | 2,258 (0.023) |
| backlog-owed | 276 | 18,959 (0.190) | 2,258 (0.023) |
| acmp-disc | 399 | 91,251 (0.913) | 78,216 (0.782) |
| maap | 165 | 18,941 (0.189) | 2,258 (0.023) |
| aecp-fanout | 84 | 18,687 (0.187) | 2,258 (0.023) |
| acmp-cmd | 65 | 18,687 (0.187) | 2,258 (0.023) |
| aecp | 79 | 18,687 (0.187) | 2,258 (0.023) |
| srp-register | 138 | 19,789 (0.198) | 2,258 (0.023) |
| aecp-reboot | 78 | 18,687 (0.187) | 2,258 (0.023) |
| aecp-largest-notice | 78 | 18,687 (0.187) | 2,258 (0.023) |
| aecp-held | 98 | 18,687 (0.187) | 2,258 (0.023) |
| datapath-events | 69 | 18,687 (0.187) | 2,258 (0.023) |
| fixture | 54 | 12,790 (0.128) | 2,258 (0.023) |

Longest pass that carries a step: 93,514 CPU cycles (0.935 ms), backlog-adp@program-aged2-5; longest step: 78,659 (0.787 ms), backlog-adp@program-aged2-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| Talker Advertise RX for every input, no binding (kept) | `srp.kept_advertise.if0` | 43,380 | 0.434 | 20 | 20 | fits | 43,446 | 25 | 0.854 |
| Talker RX at the bound after a freed block (count) | `srp.kept_recount.if0` | 40,497 | 0.405 | 20 | 20 | fits | 40,563 | 25 | 0.853 |
| Talker Failed RX for every input, no binding (kept) | `srp.kept_failed.if0` | 44,232 | 0.442 | 20 | 20 | fits | 44,298 | 23 | 0.863 |
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 154,718 | 1.547 | 20 | 200 | fits | 155,658 | 255 | 0.445 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 226,092 | 2.261 | 20 | 20 | fits | 91,511 | 108 | 0.673 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 271,407 | 2.714 | 20 | 24 | fits | 71,980 | 61 | 0.595 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 203,046 | 2.030 | 20 | 50 | fits | 91,564 | 202 | 0.359 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 758,320 | 7.583 | 20 | 20 | fits | 40,606 | 34 | 0.766 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 51,401 | 0.514 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-burst.held.adp.if0` | 154,849 | 1.548 | 20 | 200 | fits | 155,658 | 255 | 0.445 |
| ACMP record, every channel at its refill rate, the longest | `save-burst.held.acmp.if0` | 224,692 | 2.247 | 20 | 20 | fits | 90,111 | 104 | 0.692 |
| AECP record, every channel at its refill rate, the longest | `save-burst.held.aecp.if0` | 164,442 | 1.644 | 20 | 24 | fits | 87,384 | 70 | 0.748 |
| MAAP record, every channel at its refill rate, the longest | `save-burst.held.maap.if0` | 185,217 | 1.852 | 20 | 50 | fits | 90,111 | 104 | 0.692 |
| SRP record, every channel at its refill rate, the longest | `save-burst.held.srp.if0` | 690,324 | 6.903 | 20 | 20 | fits | 88,343 | 84 | 0.707 |
| an MRPDU its periodic timer owes, the longest | `save-burst.mrpdu.periodic.if0` | 164,434 | 1.644 | 49 | 49 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 8,969 | 0.090 | 20 | 20 | fits | 26,991 | 19 (14) | 0.877 |
| LINK_UP | `adp.link_up.if0` | 3,199 | 0.032 | 20 | 200 | fits | 23,900 | 44 (12) | 0.714 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 11,592 | 0.116 | 20 | 200 | fits | 17,049 | 23 (39) | 0.628 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 6,774 | 0.068 | 20 | 200 | fits | 2,351 | 10 (11) | 0.429 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 388,253 | 3.883 | 20 | 20 | fits | 80,534 | 121 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 352,682 | 3.527 | 20 | 200 | fits | 147,968 | 262 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 432,600 | 4.326 | 20 | 200 | fits | 80,534 | 121 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 353,606 | 3.536 | 20 | 20 | fits | 147,968 | 262 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 433,304 | 4.333 | 20 | 20 | fits | 80,534 | 121 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 209,278 | 2.093 | 20 | 24 | fits | 135,301 | 161 | 0.302 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 356,256 | 3.563 | 20 | 24 | fits | 147,968 | 262 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 356,190 | 3.562 | 20 | 50 | fits | 147,968 | 262 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 436,328 | 4.363 | 20 | 50 | fits | 80,534 | 121 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 517,741 | 5.177 | 20 | 20 | fits | 81,479 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 925,526 | 9.255 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 375,753 | 3.758 | 20 | 20 | fits | 80,534 | 121 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 340,182 | 3.402 | 20 | 200 | fits | 147,968 | 262 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 420,100 | 4.201 | 20 | 200 | fits | 80,534 | 121 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 341,106 | 3.411 | 20 | 20 | fits | 147,968 | 262 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 420,804 | 4.208 | 20 | 20 | fits | 80,534 | 121 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 196,778 | 1.968 | 20 | 24 | fits | 135,301 | 161 | 0.302 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 343,756 | 3.438 | 20 | 24 | fits | 147,968 | 262 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 343,690 | 3.437 | 20 | 50 | fits | 147,968 | 262 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 423,828 | 4.238 | 20 | 50 | fits | 80,534 | 121 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 505,241 | 5.052 | 20 | 20 | fits | 81,479 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 913,026 | 9.130 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 363,253 | 3.633 | 20 | 20 | fits | 80,534 | 121 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 327,682 | 3.277 | 20 | 200 | fits | 147,968 | 262 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 407,600 | 4.076 | 20 | 200 | fits | 80,534 | 121 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 328,606 | 3.286 | 20 | 20 | fits | 147,968 | 262 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 408,304 | 4.083 | 20 | 20 | fits | 80,534 | 121 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 184,278 | 1.843 | 20 | 24 | fits | 135,301 | 161 | 0.302 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 331,256 | 3.313 | 20 | 24 | fits | 147,968 | 262 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 331,190 | 3.312 | 20 | 50 | fits | 147,968 | 262 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 411,328 | 4.113 | 20 | 50 | fits | 80,534 | 121 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 492,741 | 4.927 | 20 | 20 | fits | 81,479 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 900,526 | 9.005 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 350,753 | 3.508 | 20 | 20 | fits | 80,534 | 121 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 315,182 | 3.152 | 20 | 200 | fits | 147,968 | 262 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 395,100 | 3.951 | 20 | 200 | fits | 80,534 | 121 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 316,106 | 3.161 | 20 | 20 | fits | 147,968 | 262 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 395,804 | 3.958 | 20 | 20 | fits | 80,534 | 121 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 171,778 | 1.718 | 20 | 24 | fits | 135,301 | 161 | 0.302 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 318,756 | 3.188 | 20 | 24 | fits | 147,968 | 262 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 318,690 | 3.187 | 20 | 50 | fits | 147,968 | 262 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 398,828 | 3.988 | 20 | 50 | fits | 80,534 | 121 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 480,241 | 4.802 | 20 | 20 | fits | 81,479 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 888,026 | 8.880 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 338,253 | 3.383 | 20 | 20 | fits | 80,534 | 121 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 302,682 | 3.027 | 20 | 200 | fits | 147,968 | 262 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 382,600 | 3.826 | 20 | 200 | fits | 80,534 | 121 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 303,606 | 3.036 | 20 | 20 | fits | 147,968 | 262 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 383,304 | 3.833 | 20 | 20 | fits | 80,534 | 121 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 159,278 | 1.593 | 20 | 24 | fits | 135,301 | 161 | 0.302 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 306,256 | 3.063 | 20 | 24 | fits | 147,968 | 262 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 306,190 | 3.062 | 20 | 50 | fits | 147,968 | 262 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 386,328 | 3.863 | 20 | 50 | fits | 80,534 | 121 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 467,741 | 4.677 | 20 | 20 | fits | 81,479 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 875,526 | 8.755 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 325,753 | 3.258 | 20 | 20 | fits | 80,534 | 121 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 290,182 | 2.902 | 20 | 200 | fits | 147,968 | 262 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 370,100 | 3.701 | 20 | 200 | fits | 80,534 | 121 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 291,106 | 2.911 | 20 | 20 | fits | 147,968 | 262 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 370,804 | 3.708 | 20 | 20 | fits | 80,534 | 121 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 146,778 | 1.468 | 20 | 24 | fits | 135,301 | 161 | 0.302 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 293,756 | 2.938 | 20 | 24 | fits | 147,968 | 262 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 293,690 | 2.937 | 20 | 50 | fits | 147,968 | 262 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 373,828 | 3.738 | 20 | 50 | fits | 80,534 | 121 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 455,241 | 4.552 | 20 | 20 | fits | 81,479 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 863,026 | 8.630 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 314,095 | 3.141 | 20 | 20 | fits | 93,983 | 168 | 0.431 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 265,436 | 2.654 | 20 | 200 | fits | 144,342 | 262 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 358,803 | 3.588 | 20 | 200 | fits | 93,983 | 168 | 0.431 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 266,360 | 2.664 | 20 | 20 | fits | 144,342 | 262 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 359,507 | 3.595 | 20 | 20 | fits | 93,983 | 168 | 0.431 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 125,658 | 1.257 | 20 | 24 | fits | 126,681 | 114 | 0.307 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 269,010 | 2.690 | 20 | 24 | fits | 144,342 | 262 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 268,944 | 2.689 | 20 | 50 | fits | 144,342 | 262 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 362,531 | 3.625 | 20 | 50 | fits | 93,983 | 168 | 0.431 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 444,112 | 4.441 | 20 | 20 | fits | 81,647 | 73 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 852,135 | 8.521 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 380,713 | 3.807 | 20 | 20 | fits | 83,079 | 109 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 350,080 | 3.501 | 20 | 200 | fits | 147,107 | 277 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 432,543 | 4.325 | 20 | 200 | fits | 83,079 | 109 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 351,004 | 3.510 | 20 | 20 | fits | 147,107 | 277 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 433,247 | 4.332 | 20 | 20 | fits | 83,079 | 109 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 207,537 | 2.075 | 20 | 24 | fits | 135,301 | 161 | 0.302 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 353,654 | 3.537 | 20 | 24 | fits | 147,107 | 277 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 353,588 | 3.536 | 20 | 50 | fits | 147,107 | 277 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 436,271 | 4.363 | 20 | 50 | fits | 83,079 | 109 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 517,698 | 5.177 | 20 | 20 | fits | 81,493 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 925,311 | 9.253 | 20 | 20 | fits | 51,506 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 321,646 | 3.216 | 20 | 20 | fits | 82,046 | 106 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 313,571 | 3.136 | 20 | 200 | fits | 143,095 | 276 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 395,001 | 3.950 | 20 | 200 | fits | 82,046 | 106 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 314,495 | 3.145 | 20 | 20 | fits | 143,095 | 276 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 395,705 | 3.957 | 20 | 20 | fits | 82,046 | 106 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 175,040 | 1.750 | 20 | 24 | fits | 136,531 | 161 | 0.308 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 317,145 | 3.171 | 20 | 24 | fits | 143,095 | 276 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 317,079 | 3.171 | 20 | 50 | fits | 143,095 | 276 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 398,729 | 3.987 | 20 | 50 | fits | 82,046 | 106 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 480,152 | 4.802 | 20 | 20 | fits | 81,489 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 893,034 | 8.930 | 20 | 20 | fits | 62,929 | 60 | 0.689 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 296,646 | 2.966 | 20 | 20 | fits | 82,046 | 106 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 288,571 | 2.886 | 20 | 200 | fits | 143,095 | 276 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 370,001 | 3.700 | 20 | 200 | fits | 82,046 | 106 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 289,495 | 2.895 | 20 | 20 | fits | 143,095 | 276 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 370,705 | 3.707 | 20 | 20 | fits | 82,046 | 106 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 150,040 | 1.500 | 20 | 24 | fits | 136,531 | 161 | 0.308 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 292,145 | 2.921 | 20 | 24 | fits | 143,095 | 276 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 292,079 | 2.921 | 20 | 50 | fits | 143,095 | 276 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 373,729 | 3.737 | 20 | 50 | fits | 82,046 | 106 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 455,152 | 4.552 | 20 | 20 | fits | 81,489 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 868,034 | 8.680 | 20 | 20 | fits | 62,929 | 60 | 0.689 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 289,288 | 2.893 | 20 | 20 | fits | 80,170 | 118 | 0.452 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 280,860 | 2.809 | 20 | 200 | fits | 144,186 | 261 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 360,414 | 3.604 | 20 | 200 | fits | 80,170 | 118 | 0.452 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 281,784 | 2.818 | 20 | 20 | fits | 144,186 | 261 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 361,118 | 3.611 | 20 | 20 | fits | 80,170 | 118 | 0.452 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 141,238 | 1.412 | 20 | 24 | fits | 135,678 | 161 | 0.303 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 284,434 | 2.844 | 20 | 24 | fits | 144,186 | 261 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 284,368 | 2.844 | 20 | 50 | fits | 144,186 | 261 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 364,142 | 3.641 | 20 | 50 | fits | 80,170 | 118 | 0.452 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 445,676 | 4.457 | 20 | 20 | fits | 81,600 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 858,729 | 8.587 | 20 | 20 | fits | 62,929 | 60 | 0.689 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 380,193 | 3.802 | 20 | 20 | fits | 79,486 | 118 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 347,422 | 3.474 | 20 | 200 | fits | 143,930 | 261 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 426,292 | 4.263 | 20 | 200 | fits | 79,486 | 118 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 348,346 | 3.483 | 20 | 20 | fits | 143,930 | 261 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 426,996 | 4.270 | 20 | 20 | fits | 79,486 | 118 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 208,056 | 2.081 | 20 | 24 | fits | 136,611 | 161 | 0.308 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 350,996 | 3.510 | 20 | 24 | fits | 143,930 | 261 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 350,930 | 3.509 | 20 | 50 | fits | 143,930 | 261 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 430,020 | 4.300 | 20 | 50 | fits | 79,486 | 118 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 511,567 | 5.116 | 20 | 20 | fits | 81,613 | 73 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 924,520 | 9.245 | 20 | 20 | fits | 62,773 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 355,193 | 3.552 | 20 | 20 | fits | 79,486 | 118 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 322,422 | 3.224 | 20 | 200 | fits | 143,930 | 261 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 401,292 | 4.013 | 20 | 200 | fits | 79,486 | 118 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 323,346 | 3.233 | 20 | 20 | fits | 143,930 | 261 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 401,996 | 4.020 | 20 | 20 | fits | 79,486 | 118 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 183,056 | 1.831 | 20 | 24 | fits | 136,611 | 161 | 0.308 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 325,996 | 3.260 | 20 | 24 | fits | 143,930 | 261 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 325,930 | 3.259 | 20 | 50 | fits | 143,930 | 261 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 405,020 | 4.050 | 20 | 50 | fits | 79,486 | 118 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 486,567 | 4.866 | 20 | 20 | fits | 81,613 | 73 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 899,520 | 8.995 | 20 | 20 | fits | 62,773 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 330,193 | 3.302 | 20 | 20 | fits | 79,486 | 118 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 297,422 | 2.974 | 20 | 200 | fits | 143,930 | 261 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 376,292 | 3.763 | 20 | 200 | fits | 79,486 | 118 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 298,346 | 2.983 | 20 | 20 | fits | 143,930 | 261 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 376,996 | 3.770 | 20 | 20 | fits | 79,486 | 118 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 158,056 | 1.581 | 20 | 24 | fits | 136,611 | 161 | 0.308 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 300,996 | 3.010 | 20 | 24 | fits | 143,930 | 261 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 300,930 | 3.009 | 20 | 50 | fits | 143,930 | 261 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 380,020 | 3.800 | 20 | 50 | fits | 79,486 | 118 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 461,567 | 4.616 | 20 | 20 | fits | 81,613 | 73 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 874,520 | 8.745 | 20 | 20 | fits | 62,773 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 323,540 | 3.235 | 20 | 20 | fits | 99,071 | 113 | 0.556 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 292,808 | 2.928 | 20 | 200 | fits | 148,317 | 279 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 391,263 | 3.913 | 20 | 200 | fits | 99,071 | 113 | 0.556 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 293,732 | 2.937 | 20 | 20 | fits | 148,317 | 279 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 391,967 | 3.920 | 20 | 20 | fits | 99,071 | 113 | 0.556 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 149,055 | 1.491 | 20 | 24 | fits | 135,583 | 161 | 0.302 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 296,382 | 2.964 | 20 | 24 | fits | 148,317 | 279 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 296,316 | 2.963 | 20 | 50 | fits | 148,317 | 279 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 394,991 | 3.950 | 20 | 50 | fits | 99,071 | 113 | 0.556 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 394,925 | 3.949 | 20 | 20 | fits | 99,071 | 113 | 0.556 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 871,754 | 8.718 | 20 | 20 | fits | 40,215 | 34 | 0.759 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 369,003 | 3.690 | 20 | 20 | fits | 81,435 | 106 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 354,160 | 3.542 | 20 | 200 | fits | 143,150 | 276 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 434,979 | 4.350 | 20 | 200 | fits | 81,435 | 106 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 355,084 | 3.551 | 20 | 20 | fits | 143,150 | 276 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 435,683 | 4.357 | 20 | 20 | fits | 81,435 | 106 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 215,574 | 2.156 | 20 | 24 | fits | 136,453 | 161 | 0.308 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 357,734 | 3.577 | 20 | 24 | fits | 143,150 | 276 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 357,668 | 3.577 | 20 | 50 | fits | 143,150 | 276 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 438,707 | 4.387 | 20 | 50 | fits | 81,435 | 106 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 520,273 | 5.203 | 20 | 20 | fits | 81,632 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 933,128 | 9.331 | 20 | 20 | fits | 62,778 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 377,633 | 3.776 | 20 | 20 | fits | 80,875 | 106 | 0.464 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 342,090 | 3.421 | 20 | 200 | fits | 147,995 | 279 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 422,349 | 4.223 | 20 | 200 | fits | 80,875 | 106 | 0.464 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 343,014 | 3.430 | 20 | 20 | fits | 147,995 | 279 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 423,053 | 4.231 | 20 | 20 | fits | 80,875 | 106 | 0.464 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 198,659 | 1.987 | 20 | 24 | fits | 135,194 | 161 | 0.297 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 345,664 | 3.457 | 20 | 24 | fits | 147,995 | 279 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 345,598 | 3.456 | 20 | 50 | fits | 147,995 | 279 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 426,077 | 4.261 | 20 | 50 | fits | 80,875 | 106 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 507,556 | 5.076 | 20 | 20 | fits | 81,545 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 915,311 | 9.153 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 365,133 | 3.651 | 20 | 20 | fits | 80,875 | 106 | 0.464 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 329,590 | 3.296 | 20 | 200 | fits | 147,995 | 279 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 409,849 | 4.098 | 20 | 200 | fits | 80,875 | 106 | 0.464 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 330,514 | 3.305 | 20 | 20 | fits | 147,995 | 279 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 410,553 | 4.106 | 20 | 20 | fits | 80,875 | 106 | 0.464 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 186,159 | 1.862 | 20 | 24 | fits | 135,194 | 161 | 0.297 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 333,164 | 3.332 | 20 | 24 | fits | 147,995 | 279 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 333,098 | 3.331 | 20 | 50 | fits | 147,995 | 279 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 413,577 | 4.136 | 20 | 50 | fits | 80,875 | 106 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 495,056 | 4.951 | 20 | 20 | fits | 81,545 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 902,811 | 9.028 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 352,633 | 3.526 | 20 | 20 | fits | 80,875 | 106 | 0.464 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 317,090 | 3.171 | 20 | 200 | fits | 147,995 | 279 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 397,349 | 3.973 | 20 | 200 | fits | 80,875 | 106 | 0.464 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 318,014 | 3.180 | 20 | 20 | fits | 147,995 | 279 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 398,053 | 3.981 | 20 | 20 | fits | 80,875 | 106 | 0.464 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 173,659 | 1.737 | 20 | 24 | fits | 135,194 | 161 | 0.297 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 320,664 | 3.207 | 20 | 24 | fits | 147,995 | 279 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 320,598 | 3.206 | 20 | 50 | fits | 147,995 | 279 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 401,077 | 4.011 | 20 | 50 | fits | 80,875 | 106 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 482,556 | 4.826 | 20 | 20 | fits | 81,545 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 890,311 | 8.903 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 340,133 | 3.401 | 20 | 20 | fits | 80,875 | 106 | 0.464 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 304,590 | 3.046 | 20 | 200 | fits | 147,995 | 279 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 384,849 | 3.848 | 20 | 200 | fits | 80,875 | 106 | 0.464 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 305,514 | 3.055 | 20 | 20 | fits | 147,995 | 279 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 385,553 | 3.856 | 20 | 20 | fits | 80,875 | 106 | 0.464 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 161,159 | 1.612 | 20 | 24 | fits | 135,194 | 161 | 0.297 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 308,164 | 3.082 | 20 | 24 | fits | 147,995 | 279 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 308,098 | 3.081 | 20 | 50 | fits | 147,995 | 279 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 388,577 | 3.886 | 20 | 50 | fits | 80,875 | 106 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 470,056 | 4.701 | 20 | 20 | fits | 81,545 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 877,811 | 8.778 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 327,633 | 3.276 | 20 | 20 | fits | 80,875 | 106 | 0.464 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 292,090 | 2.921 | 20 | 200 | fits | 147,995 | 279 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 372,349 | 3.723 | 20 | 200 | fits | 80,875 | 106 | 0.464 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 293,014 | 2.930 | 20 | 20 | fits | 147,995 | 279 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 373,053 | 3.731 | 20 | 20 | fits | 80,875 | 106 | 0.464 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 148,659 | 1.487 | 20 | 24 | fits | 135,194 | 161 | 0.297 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 295,664 | 2.957 | 20 | 24 | fits | 147,995 | 279 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 295,598 | 2.956 | 20 | 50 | fits | 147,995 | 279 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 376,077 | 3.761 | 20 | 50 | fits | 80,875 | 106 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 457,556 | 4.576 | 20 | 20 | fits | 81,545 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 865,311 | 8.653 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 315,133 | 3.151 | 20 | 20 | fits | 80,875 | 106 | 0.464 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 279,590 | 2.796 | 20 | 200 | fits | 147,995 | 279 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 359,849 | 3.598 | 20 | 200 | fits | 80,875 | 106 | 0.464 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 280,514 | 2.805 | 20 | 20 | fits | 147,995 | 279 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 360,553 | 3.606 | 20 | 20 | fits | 80,875 | 106 | 0.464 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 136,159 | 1.362 | 20 | 24 | fits | 135,194 | 161 | 0.297 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 283,164 | 2.832 | 20 | 24 | fits | 147,995 | 279 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 283,098 | 2.831 | 20 | 50 | fits | 147,995 | 279 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 363,577 | 3.636 | 20 | 50 | fits | 80,875 | 106 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 445,056 | 4.451 | 20 | 20 | fits | 81,545 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 852,811 | 8.528 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 383,267 | 3.833 | 20 | 20 | fits | 83,049 | 109 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 352,664 | 3.527 | 20 | 200 | fits | 146,579 | 277 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 435,097 | 4.351 | 20 | 200 | fits | 83,049 | 109 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 353,588 | 3.536 | 20 | 20 | fits | 146,579 | 277 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 435,801 | 4.358 | 20 | 20 | fits | 83,049 | 109 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 210,649 | 2.106 | 20 | 24 | fits | 135,115 | 161 | 0.297 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 356,238 | 3.562 | 20 | 24 | fits | 146,579 | 277 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 356,172 | 3.562 | 20 | 50 | fits | 146,579 | 277 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 438,825 | 4.388 | 20 | 50 | fits | 83,049 | 109 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 520,318 | 5.203 | 20 | 20 | fits | 81,559 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 928,149 | 9.281 | 20 | 20 | fits | 51,506 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 370,767 | 3.708 | 20 | 20 | fits | 83,049 | 109 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 340,164 | 3.402 | 20 | 200 | fits | 146,579 | 277 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 422,597 | 4.226 | 20 | 200 | fits | 83,049 | 109 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 341,088 | 3.411 | 20 | 20 | fits | 146,579 | 277 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 423,301 | 4.233 | 20 | 20 | fits | 83,049 | 109 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 198,149 | 1.981 | 20 | 24 | fits | 135,115 | 161 | 0.297 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 343,738 | 3.437 | 20 | 24 | fits | 146,579 | 277 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 343,672 | 3.437 | 20 | 50 | fits | 146,579 | 277 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 426,325 | 4.263 | 20 | 50 | fits | 83,049 | 109 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 507,818 | 5.078 | 20 | 20 | fits | 81,559 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 915,649 | 9.156 | 20 | 20 | fits | 51,506 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 279,715 | 2.797 | 20 | 20 | fits | 81,855 | 106 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 271,698 | 2.717 | 20 | 200 | fits | 143,926 | 281 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 352,937 | 3.529 | 20 | 200 | fits | 81,855 | 106 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 272,622 | 2.726 | 20 | 20 | fits | 143,926 | 281 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 353,641 | 3.536 | 20 | 20 | fits | 81,855 | 106 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 132,336 | 1.323 | 20 | 24 | fits | 134,406 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 275,272 | 2.753 | 20 | 24 | fits | 143,926 | 281 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 275,206 | 2.752 | 20 | 50 | fits | 143,926 | 281 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 356,665 | 3.567 | 20 | 50 | fits | 81,855 | 106 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 438,294 | 4.383 | 20 | 20 | fits | 81,695 | 73 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 846,008 | 8.460 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 314,736 | 3.147 | 20 | 20 | fits | 79,465 | 118 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 281,893 | 2.819 | 20 | 200 | fits | 143,893 | 261 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 360,742 | 3.607 | 20 | 200 | fits | 79,465 | 118 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 282,817 | 2.828 | 20 | 20 | fits | 143,893 | 261 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 361,446 | 3.614 | 20 | 20 | fits | 79,465 | 118 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 142,564 | 1.426 | 20 | 24 | fits | 134,406 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 285,467 | 2.855 | 20 | 24 | fits | 143,893 | 261 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 285,401 | 2.854 | 20 | 50 | fits | 143,893 | 261 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 364,470 | 3.645 | 20 | 50 | fits | 79,465 | 118 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 446,161 | 4.462 | 20 | 20 | fits | 81,757 | 73 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 853,793 | 8.538 | 20 | 20 | fits | 51,501 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 315,700 | 3.157 | 20 | 20 | fits | 99,123 | 113 | 0.557 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 285,002 | 2.850 | 20 | 200 | fits | 148,043 | 279 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 383,509 | 3.835 | 20 | 200 | fits | 99,123 | 113 | 0.557 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 285,926 | 2.859 | 20 | 20 | fits | 148,043 | 279 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 384,213 | 3.842 | 20 | 20 | fits | 99,123 | 113 | 0.557 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 141,523 | 1.415 | 20 | 24 | fits | 134,406 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 288,576 | 2.886 | 20 | 24 | fits | 148,043 | 279 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 288,510 | 2.885 | 20 | 50 | fits | 148,043 | 279 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 387,237 | 3.872 | 20 | 50 | fits | 99,123 | 113 | 0.557 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 387,171 | 3.872 | 20 | 20 | fits | 99,123 | 113 | 0.557 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 941,213 | 9.412 | 20 | 20 | fits | 40,936 | 35 | 0.770 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 293,863 | 2.939 | 20 | 20 | fits | 81,396 | 106 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 279,031 | 2.790 | 20 | 200 | fits | 143,113 | 276 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 359,811 | 3.598 | 20 | 200 | fits | 81,396 | 106 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 279,955 | 2.800 | 20 | 20 | fits | 143,113 | 276 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 360,515 | 3.605 | 20 | 20 | fits | 81,396 | 106 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 140,482 | 1.405 | 20 | 24 | fits | 134,406 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 282,605 | 2.826 | 20 | 24 | fits | 143,113 | 276 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 282,539 | 2.825 | 20 | 50 | fits | 143,113 | 276 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 363,539 | 3.635 | 20 | 50 | fits | 81,396 | 106 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 445,333 | 4.453 | 20 | 20 | fits | 81,860 | 73 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 935,323 | 9.353 | 20 | 20 | fits | 62,966 | 60 | 0.689 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 285,952 | 2.860 | 20 | 20 | fits | 81,924 | 106 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 277,935 | 2.779 | 20 | 200 | fits | 143,058 | 276 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 359,243 | 3.592 | 20 | 200 | fits | 81,924 | 106 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 278,859 | 2.789 | 20 | 20 | fits | 143,058 | 276 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 359,947 | 3.599 | 20 | 20 | fits | 81,924 | 106 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 139,441 | 1.394 | 20 | 24 | fits | 134,406 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 281,509 | 2.815 | 20 | 24 | fits | 143,058 | 276 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 281,443 | 2.814 | 20 | 50 | fits | 143,058 | 276 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 362,971 | 3.630 | 20 | 50 | fits | 81,924 | 106 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 444,600 | 4.446 | 20 | 20 | fits | 81,695 | 73 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 934,415 | 9.344 | 20 | 20 | fits | 62,759 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 286,076 | 2.861 | 20 | 20 | fits | 79,885 | 118 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 277,748 | 2.777 | 20 | 200 | fits | 143,912 | 261 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 357,017 | 3.570 | 20 | 200 | fits | 79,885 | 118 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 278,672 | 2.787 | 20 | 20 | fits | 143,912 | 261 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 357,721 | 3.577 | 20 | 20 | fits | 79,885 | 118 | 0.449 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 138,400 | 1.384 | 20 | 24 | fits | 134,406 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 281,322 | 2.813 | 20 | 24 | fits | 143,912 | 261 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 281,256 | 2.813 | 20 | 50 | fits | 143,912 | 261 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 360,745 | 3.607 | 20 | 50 | fits | 79,885 | 118 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 445,974 | 4.460 | 20 | 20 | fits | 85,295 | 79 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 929,756 | 9.298 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 315,528 | 3.155 | 20 | 20 | fits | 85,377 | 124 | 0.469 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 276,688 | 2.767 | 20 | 200 | fits | 143,893 | 261 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 361,449 | 3.614 | 20 | 200 | fits | 85,377 | 124 | 0.469 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 277,612 | 2.776 | 20 | 20 | fits | 143,893 | 261 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 362,153 | 3.622 | 20 | 20 | fits | 85,377 | 124 | 0.469 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 137,359 | 1.374 | 20 | 24 | fits | 134,406 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 280,262 | 2.803 | 20 | 24 | fits | 143,893 | 261 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 280,196 | 2.802 | 20 | 50 | fits | 143,893 | 261 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 365,177 | 3.652 | 20 | 50 | fits | 85,377 | 124 | 0.469 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 523,029 | 5.230 | 20 | 20 | fits | 81,352 | 74 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 930,809 | 9.308 | 20 | 20 | fits | 51,501 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 390,849 | 3.908 | 20 | 20 | fits | 80,582 | 121 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 279,065 | 2.791 | 20 | 200 | fits | 147,311 | 262 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 435,366 | 4.354 | 20 | 200 | fits | 80,582 | 121 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 279,989 | 2.800 | 20 | 20 | fits | 147,311 | 262 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 436,070 | 4.361 | 20 | 20 | fits | 80,582 | 121 | 0.430 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 136,318 | 1.363 | 20 | 24 | fits | 134,406 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 282,639 | 2.826 | 20 | 24 | fits | 147,311 | 262 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 282,573 | 2.826 | 20 | 50 | fits | 147,311 | 262 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 439,094 | 4.391 | 20 | 50 | fits | 80,582 | 121 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 520,767 | 5.208 | 20 | 20 | fits | 81,739 | 73 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 928,481 | 9.285 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 310,850 | 3.108 | 20 | 20 | fits | 79,465 | 118 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 278,007 | 2.780 | 20 | 200 | fits | 143,893 | 261 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 356,856 | 3.569 | 20 | 200 | fits | 79,465 | 118 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 278,931 | 2.789 | 20 | 20 | fits | 143,893 | 261 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 357,560 | 3.576 | 20 | 20 | fits | 79,465 | 118 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 138,678 | 1.387 | 20 | 24 | fits | 134,406 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 281,581 | 2.816 | 20 | 24 | fits | 143,893 | 261 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 281,515 | 2.815 | 20 | 50 | fits | 143,893 | 261 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 360,584 | 3.606 | 20 | 50 | fits | 79,465 | 118 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 442,275 | 4.423 | 20 | 20 | fits | 81,757 | 73 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 849,907 | 8.499 | 20 | 20 | fits | 51,501 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 311,814 | 3.118 | 20 | 20 | fits | 99,123 | 113 | 0.557 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 281,116 | 2.811 | 20 | 200 | fits | 148,043 | 279 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 379,623 | 3.796 | 20 | 200 | fits | 99,123 | 113 | 0.557 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 282,040 | 2.820 | 20 | 20 | fits | 148,043 | 279 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 380,327 | 3.803 | 20 | 20 | fits | 99,123 | 113 | 0.557 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 137,637 | 1.376 | 20 | 24 | fits | 134,406 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 284,690 | 2.847 | 20 | 24 | fits | 148,043 | 279 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 284,624 | 2.846 | 20 | 50 | fits | 148,043 | 279 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 383,351 | 3.834 | 20 | 50 | fits | 99,123 | 113 | 0.557 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 383,285 | 3.833 | 20 | 20 | fits | 99,123 | 113 | 0.557 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 859,476 | 8.595 | 20 | 20 | fits | 33,507 | 27 | 0.828 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 289,977 | 2.900 | 20 | 20 | fits | 81,396 | 106 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 275,145 | 2.751 | 20 | 200 | fits | 143,113 | 276 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 355,925 | 3.559 | 20 | 200 | fits | 81,396 | 106 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 276,069 | 2.761 | 20 | 20 | fits | 143,113 | 276 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 356,629 | 3.566 | 20 | 20 | fits | 81,396 | 106 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 136,596 | 1.366 | 20 | 24 | fits | 134,406 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 278,719 | 2.787 | 20 | 24 | fits | 143,113 | 276 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 278,653 | 2.787 | 20 | 50 | fits | 143,113 | 276 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 359,653 | 3.597 | 20 | 50 | fits | 81,396 | 106 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 441,447 | 4.414 | 20 | 20 | fits | 81,860 | 73 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 854,284 | 8.543 | 20 | 20 | fits | 62,948 | 60 | 0.689 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 282,066 | 2.821 | 20 | 20 | fits | 81,924 | 106 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 274,049 | 2.740 | 20 | 200 | fits | 143,058 | 276 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 355,357 | 3.554 | 20 | 200 | fits | 81,924 | 106 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 274,973 | 2.750 | 20 | 20 | fits | 143,058 | 276 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 356,061 | 3.561 | 20 | 20 | fits | 81,924 | 106 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 135,555 | 1.356 | 20 | 24 | fits | 134,406 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 277,623 | 2.776 | 20 | 24 | fits | 143,058 | 276 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 277,557 | 2.776 | 20 | 50 | fits | 143,058 | 276 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 359,085 | 3.591 | 20 | 50 | fits | 81,924 | 106 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 440,714 | 4.407 | 20 | 20 | fits | 81,695 | 73 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 853,567 | 8.536 | 20 | 20 | fits | 62,759 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 282,190 | 2.822 | 20 | 20 | fits | 79,885 | 118 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 273,862 | 2.739 | 20 | 200 | fits | 143,912 | 261 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 353,131 | 3.531 | 20 | 200 | fits | 79,885 | 118 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 274,786 | 2.748 | 20 | 20 | fits | 143,912 | 261 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 353,835 | 3.538 | 20 | 20 | fits | 79,885 | 118 | 0.449 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 134,514 | 1.345 | 20 | 24 | fits | 134,406 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 277,436 | 2.774 | 20 | 24 | fits | 143,912 | 261 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 277,370 | 2.774 | 20 | 50 | fits | 143,912 | 261 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 356,859 | 3.569 | 20 | 50 | fits | 79,885 | 118 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 438,440 | 4.384 | 20 | 20 | fits | 81,647 | 73 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 850,953 | 8.510 | 20 | 20 | fits | 62,759 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 305,802 | 3.058 | 20 | 20 | fits | 79,370 | 118 | 0.442 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 273,054 | 2.731 | 20 | 200 | fits | 144,761 | 266 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 351,808 | 3.518 | 20 | 200 | fits | 79,370 | 118 | 0.442 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 273,978 | 2.740 | 20 | 20 | fits | 144,761 | 266 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 352,512 | 3.525 | 20 | 20 | fits | 79,370 | 118 | 0.442 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 132,857 | 1.329 | 20 | 24 | fits | 134,406 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 276,628 | 2.766 | 20 | 24 | fits | 144,761 | 266 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 276,562 | 2.766 | 20 | 50 | fits | 144,761 | 266 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 355,536 | 3.555 | 20 | 50 | fits | 79,370 | 118 | 0.442 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 440,811 | 4.408 | 20 | 20 | fits | 85,341 | 79 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 848,390 | 8.484 | 20 | 20 | fits | 51,501 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 312,448 | 3.124 | 20 | 20 | fits | 86,351 | 127 | 0.456 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 271,372 | 2.714 | 20 | 200 | fits | 143,504 | 262 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 357,107 | 3.571 | 20 | 200 | fits | 86,351 | 127 | 0.456 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 272,296 | 2.723 | 20 | 20 | fits | 143,504 | 262 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 357,811 | 3.578 | 20 | 20 | fits | 86,351 | 127 | 0.456 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 132,432 | 1.324 | 20 | 24 | fits | 134,406 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 274,946 | 2.749 | 20 | 24 | fits | 143,504 | 262 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 274,880 | 2.749 | 20 | 50 | fits | 143,504 | 262 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 360,835 | 3.608 | 20 | 50 | fits | 86,351 | 127 | 0.456 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 442,458 | 4.425 | 20 | 20 | fits | 81,689 | 73 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 850,126 | 8.501 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 297,718 | 2.977 | 20 | 20 | fits | 92,989 | 153 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 264,282 | 2.643 | 20 | 200 | fits | 143,981 | 281 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 356,655 | 3.567 | 20 | 200 | fits | 92,989 | 153 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 265,206 | 2.652 | 20 | 20 | fits | 143,981 | 281 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 357,359 | 3.574 | 20 | 20 | fits | 92,989 | 153 | 0.409 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 124,865 | 1.249 | 20 | 24 | fits | 127,880 | 120 | 0.301 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 267,856 | 2.679 | 20 | 24 | fits | 143,981 | 281 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 267,790 | 2.678 | 20 | 50 | fits | 143,981 | 281 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 360,383 | 3.604 | 20 | 50 | fits | 92,989 | 153 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 441,849 | 4.418 | 20 | 20 | fits | 81,532 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 849,488 | 8.495 | 20 | 20 | fits | 51,506 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 307,056 | 3.071 | 20 | 20 | fits | 79,463 | 118 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 274,308 | 2.743 | 20 | 200 | fits | 143,893 | 261 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 353,155 | 3.532 | 20 | 200 | fits | 79,463 | 118 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 275,232 | 2.752 | 20 | 20 | fits | 143,893 | 261 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 353,859 | 3.539 | 20 | 20 | fits | 79,463 | 118 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 134,979 | 1.350 | 20 | 24 | fits | 134,404 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 277,882 | 2.779 | 20 | 24 | fits | 143,893 | 261 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 277,816 | 2.778 | 20 | 50 | fits | 143,893 | 261 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 356,883 | 3.569 | 20 | 50 | fits | 79,463 | 118 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 438,286 | 4.383 | 20 | 20 | fits | 81,469 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 845,821 | 8.458 | 20 | 20 | fits | 51,501 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 307,288 | 3.073 | 20 | 20 | fits | 80,456 | 121 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 271,795 | 2.718 | 20 | 200 | fits | 143,504 | 262 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 351,635 | 3.516 | 20 | 200 | fits | 80,456 | 121 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 272,719 | 2.727 | 20 | 20 | fits | 143,504 | 262 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 352,339 | 3.523 | 20 | 20 | fits | 80,456 | 121 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 132,855 | 1.329 | 20 | 24 | fits | 134,404 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 275,369 | 2.754 | 20 | 24 | fits | 143,504 | 262 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 275,303 | 2.753 | 20 | 50 | fits | 143,504 | 262 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 355,363 | 3.554 | 20 | 50 | fits | 80,456 | 121 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 436,785 | 4.368 | 20 | 20 | fits | 81,488 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 844,379 | 8.444 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 287,104 | 2.871 | 20 | 20 | fits | 81,489 | 106 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 272,272 | 2.723 | 20 | 200 | fits | 143,981 | 281 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 353,145 | 3.531 | 20 | 200 | fits | 81,489 | 106 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 273,196 | 2.732 | 20 | 20 | fits | 143,981 | 281 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 353,849 | 3.538 | 20 | 20 | fits | 81,489 | 106 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 132,855 | 1.329 | 20 | 24 | fits | 134,404 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 275,846 | 2.758 | 20 | 24 | fits | 143,981 | 281 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 275,780 | 2.758 | 20 | 50 | fits | 143,981 | 281 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 356,873 | 3.569 | 20 | 50 | fits | 81,489 | 106 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 438,368 | 4.384 | 20 | 20 | fits | 81,561 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 933,337 | 9.333 | 20 | 20 | fits | 64,505 | 61 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 280,376 | 2.804 | 20 | 20 | fits | 90,275 | 148 | 0.434 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 264,692 | 2.647 | 20 | 200 | fits | 143,926 | 281 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 354,351 | 3.544 | 20 | 200 | fits | 90,275 | 148 | 0.434 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 265,616 | 2.656 | 20 | 20 | fits | 143,926 | 281 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 355,055 | 3.551 | 20 | 20 | fits | 90,275 | 148 | 0.434 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 125,330 | 1.253 | 20 | 24 | fits | 127,878 | 120 | 0.300 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 268,266 | 2.683 | 20 | 24 | fits | 143,926 | 281 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 268,200 | 2.682 | 20 | 50 | fits | 143,926 | 281 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 358,079 | 3.581 | 20 | 50 | fits | 90,275 | 148 | 0.434 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 439,585 | 4.396 | 20 | 20 | fits | 81,572 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 934,985 | 9.350 | 20 | 20 | fits | 62,935 | 60 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 314,256 | 3.143 | 20 | 20 | fits | 79,558 | 118 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 281,413 | 2.814 | 20 | 200 | fits | 143,893 | 261 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 360,355 | 3.604 | 20 | 200 | fits | 79,558 | 118 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 282,337 | 2.823 | 20 | 20 | fits | 143,893 | 261 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 361,059 | 3.611 | 20 | 20 | fits | 79,558 | 118 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 142,084 | 1.421 | 20 | 24 | fits | 134,404 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 284,987 | 2.850 | 20 | 24 | fits | 143,893 | 261 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 284,921 | 2.849 | 20 | 50 | fits | 143,893 | 261 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 364,083 | 3.641 | 20 | 50 | fits | 79,558 | 118 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 445,486 | 4.455 | 20 | 20 | fits | 81,469 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 940,377 | 9.404 | 20 | 20 | fits | 62,773 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 315,220 | 3.152 | 20 | 20 | fits | 98,959 | 113 | 0.556 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 284,522 | 2.845 | 20 | 200 | fits | 148,043 | 279 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 382,865 | 3.829 | 20 | 200 | fits | 98,959 | 113 | 0.556 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 285,446 | 2.854 | 20 | 20 | fits | 148,043 | 279 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 383,569 | 3.836 | 20 | 20 | fits | 98,959 | 113 | 0.556 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 141,043 | 1.410 | 20 | 24 | fits | 134,404 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 288,096 | 2.881 | 20 | 24 | fits | 148,043 | 279 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 288,030 | 2.880 | 20 | 50 | fits | 148,043 | 279 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 386,593 | 3.866 | 20 | 50 | fits | 98,959 | 113 | 0.556 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 386,527 | 3.865 | 20 | 20 | fits | 98,959 | 113 | 0.556 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 943,468 | 9.435 | 20 | 20 | fits | 40,215 | 34 | 0.759 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 305,026 | 3.050 | 20 | 20 | fits | 86,281 | 112 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 278,551 | 2.786 | 20 | 200 | fits | 143,113 | 276 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 364,216 | 3.642 | 20 | 200 | fits | 86,281 | 112 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 279,475 | 2.795 | 20 | 20 | fits | 143,113 | 276 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 364,920 | 3.649 | 20 | 20 | fits | 86,281 | 112 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 140,002 | 1.400 | 20 | 24 | fits | 134,404 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 282,125 | 2.821 | 20 | 24 | fits | 143,113 | 276 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 282,059 | 2.821 | 20 | 50 | fits | 143,113 | 276 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 367,944 | 3.679 | 20 | 50 | fits | 86,281 | 112 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 531,126 | 5.311 | 20 | 20 | fits | 82,541 | 74 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 938,721 | 9.387 | 20 | 20 | fits | 51,506 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 391,807 | 3.918 | 20 | 20 | fits | 83,899 | 109 | 0.445 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 280,799 | 2.808 | 20 | 200 | fits | 146,402 | 277 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 444,671 | 4.447 | 20 | 200 | fits | 83,899 | 109 | 0.445 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 281,723 | 2.817 | 20 | 20 | fits | 146,402 | 277 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 445,375 | 4.454 | 20 | 20 | fits | 83,899 | 109 | 0.445 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 138,961 | 1.390 | 20 | 24 | fits | 134,404 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 284,373 | 2.844 | 20 | 24 | fits | 146,402 | 277 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 284,307 | 2.843 | 20 | 50 | fits | 146,402 | 277 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 448,399 | 4.484 | 20 | 50 | fits | 83,899 | 109 | 0.445 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 530,081 | 5.301 | 20 | 20 | fits | 81,748 | 73 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 937,797 | 9.378 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 294,702 | 2.947 | 20 | 20 | fits | 81,489 | 106 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 279,870 | 2.799 | 20 | 200 | fits | 143,113 | 276 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 360,743 | 3.607 | 20 | 200 | fits | 81,489 | 106 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 280,794 | 2.808 | 20 | 20 | fits | 143,113 | 276 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 361,447 | 3.614 | 20 | 20 | fits | 81,489 | 106 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 141,321 | 1.413 | 20 | 24 | fits | 134,404 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 283,444 | 2.834 | 20 | 24 | fits | 143,113 | 276 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 283,378 | 2.834 | 20 | 50 | fits | 143,113 | 276 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 364,471 | 3.645 | 20 | 50 | fits | 81,489 | 106 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 445,966 | 4.460 | 20 | 20 | fits | 81,561 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 853,494 | 8.535 | 20 | 20 | fits | 51,506 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 286,791 | 2.868 | 20 | 20 | fits | 81,906 | 106 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 278,774 | 2.788 | 20 | 200 | fits | 143,058 | 276 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 360,064 | 3.601 | 20 | 200 | fits | 81,906 | 106 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 279,698 | 2.797 | 20 | 20 | fits | 143,058 | 276 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 360,768 | 3.608 | 20 | 20 | fits | 81,906 | 106 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 140,280 | 1.403 | 20 | 24 | fits | 134,404 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 282,348 | 2.823 | 20 | 24 | fits | 143,058 | 276 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 282,282 | 2.823 | 20 | 50 | fits | 143,058 | 276 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 363,792 | 3.638 | 20 | 50 | fits | 81,906 | 106 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 445,214 | 4.452 | 20 | 20 | fits | 81,488 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 852,761 | 8.528 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 286,915 | 2.869 | 20 | 20 | fits | 79,936 | 118 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 278,587 | 2.786 | 20 | 200 | fits | 143,912 | 261 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 357,907 | 3.579 | 20 | 200 | fits | 79,936 | 118 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 279,511 | 2.795 | 20 | 20 | fits | 143,912 | 261 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 358,611 | 3.586 | 20 | 20 | fits | 79,936 | 118 | 0.449 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 139,239 | 1.392 | 20 | 24 | fits | 134,404 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 282,161 | 2.822 | 20 | 24 | fits | 143,912 | 261 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 282,095 | 2.821 | 20 | 50 | fits | 143,912 | 261 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 361,635 | 3.616 | 20 | 50 | fits | 79,936 | 118 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 443,020 | 4.430 | 20 | 20 | fits | 81,451 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 855,647 | 8.556 | 20 | 20 | fits | 62,929 | 60 | 0.689 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 310,370 | 3.104 | 20 | 20 | fits | 79,558 | 118 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 277,527 | 2.775 | 20 | 200 | fits | 143,893 | 261 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 356,469 | 3.565 | 20 | 200 | fits | 79,558 | 118 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 278,451 | 2.785 | 20 | 20 | fits | 143,893 | 261 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 357,173 | 3.572 | 20 | 20 | fits | 79,558 | 118 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 138,198 | 1.382 | 20 | 24 | fits | 134,404 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 281,101 | 2.811 | 20 | 24 | fits | 143,893 | 261 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 281,035 | 2.810 | 20 | 50 | fits | 143,893 | 261 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 360,197 | 3.602 | 20 | 50 | fits | 79,558 | 118 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 441,600 | 4.416 | 20 | 20 | fits | 81,469 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 854,273 | 8.543 | 20 | 20 | fits | 62,773 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 311,334 | 3.113 | 20 | 20 | fits | 98,959 | 113 | 0.556 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 280,636 | 2.806 | 20 | 200 | fits | 148,043 | 279 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 378,979 | 3.790 | 20 | 200 | fits | 98,959 | 113 | 0.556 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 281,560 | 2.816 | 20 | 20 | fits | 148,043 | 279 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 379,683 | 3.797 | 20 | 20 | fits | 98,959 | 113 | 0.556 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 137,157 | 1.372 | 20 | 24 | fits | 134,404 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 284,210 | 2.842 | 20 | 24 | fits | 148,043 | 279 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 284,144 | 2.841 | 20 | 50 | fits | 148,043 | 279 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 382,707 | 3.827 | 20 | 50 | fits | 98,959 | 113 | 0.556 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 382,641 | 3.826 | 20 | 20 | fits | 98,959 | 113 | 0.556 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 859,190 | 8.592 | 20 | 20 | fits | 40,215 | 34 | 0.759 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 289,497 | 2.895 | 20 | 20 | fits | 81,489 | 106 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 274,665 | 2.747 | 20 | 200 | fits | 143,113 | 276 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 355,538 | 3.555 | 20 | 200 | fits | 81,489 | 106 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 275,589 | 2.756 | 20 | 20 | fits | 143,113 | 276 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 356,242 | 3.562 | 20 | 20 | fits | 81,489 | 106 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 136,116 | 1.361 | 20 | 24 | fits | 134,404 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 278,239 | 2.782 | 20 | 24 | fits | 143,113 | 276 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 278,173 | 2.782 | 20 | 50 | fits | 143,113 | 276 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 359,266 | 3.593 | 20 | 50 | fits | 81,489 | 106 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 444,411 | 4.444 | 20 | 20 | fits | 85,211 | 79 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 851,985 | 8.520 | 20 | 20 | fits | 51,506 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 299,757 | 2.998 | 20 | 20 | fits | 86,726 | 112 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 273,569 | 2.736 | 20 | 200 | fits | 143,058 | 276 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 359,679 | 3.597 | 20 | 200 | fits | 86,726 | 112 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 274,493 | 2.745 | 20 | 20 | fits | 143,058 | 276 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 360,383 | 3.604 | 20 | 20 | fits | 86,726 | 112 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 135,075 | 1.351 | 20 | 24 | fits | 134,404 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 277,143 | 2.771 | 20 | 24 | fits | 143,058 | 276 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 277,077 | 2.771 | 20 | 50 | fits | 143,058 | 276 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 363,407 | 3.634 | 20 | 50 | fits | 86,726 | 112 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 444,771 | 4.448 | 20 | 20 | fits | 81,430 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 852,537 | 8.525 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 299,353 | 2.994 | 20 | 20 | fits | 85,525 | 124 | 0.472 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 273,071 | 2.731 | 20 | 200 | fits | 144,780 | 266 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 357,980 | 3.580 | 20 | 200 | fits | 85,525 | 124 | 0.472 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 273,995 | 2.740 | 20 | 20 | fits | 144,780 | 266 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 358,684 | 3.587 | 20 | 20 | fits | 85,525 | 124 | 0.472 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 132,855 | 1.329 | 20 | 24 | fits | 134,404 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 276,645 | 2.766 | 20 | 24 | fits | 144,780 | 266 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 276,579 | 2.766 | 20 | 50 | fits | 144,780 | 266 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 361,708 | 3.617 | 20 | 50 | fits | 85,525 | 124 | 0.472 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 443,181 | 4.432 | 20 | 20 | fits | 81,539 | 73 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 850,888 | 8.509 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 307,604 | 3.076 | 20 | 20 | fits | 88,931 | 163 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 263,997 | 2.640 | 20 | 200 | fits | 143,519 | 262 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 352,312 | 3.523 | 20 | 200 | fits | 88,931 | 163 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 264,921 | 2.649 | 20 | 20 | fits | 143,519 | 262 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 353,016 | 3.530 | 20 | 20 | fits | 88,931 | 163 | 0.421 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 125,042 | 1.250 | 20 | 24 | fits | 127,957 | 120 | 0.301 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 267,571 | 2.676 | 20 | 24 | fits | 143,519 | 262 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 267,505 | 2.675 | 20 | 50 | fits | 143,519 | 262 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 356,040 | 3.560 | 20 | 50 | fits | 88,931 | 163 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 437,689 | 4.377 | 20 | 20 | fits | 81,715 | 73 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 845,332 | 8.453 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 288,276 | 2.883 | 20 | 20 | fits | 81,987 | 106 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 280,289 | 2.803 | 20 | 200 | fits | 143,057 | 276 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 361,660 | 3.617 | 20 | 200 | fits | 81,987 | 106 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 281,213 | 2.812 | 20 | 20 | fits | 143,057 | 276 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 362,364 | 3.624 | 20 | 20 | fits | 81,987 | 106 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 141,796 | 1.418 | 20 | 24 | fits | 134,483 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 283,863 | 2.839 | 20 | 24 | fits | 143,057 | 276 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 283,797 | 2.838 | 20 | 50 | fits | 143,057 | 276 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 365,388 | 3.654 | 20 | 50 | fits | 81,987 | 106 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 446,810 | 4.468 | 20 | 20 | fits | 81,488 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 854,300 | 8.543 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 288,400 | 2.884 | 20 | 20 | fits | 79,948 | 118 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 280,102 | 2.801 | 20 | 200 | fits | 143,911 | 261 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 359,434 | 3.594 | 20 | 200 | fits | 79,948 | 118 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 281,026 | 2.810 | 20 | 20 | fits | 143,911 | 261 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 360,138 | 3.601 | 20 | 20 | fits | 79,948 | 118 | 0.449 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 140,755 | 1.408 | 20 | 24 | fits | 134,483 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 283,676 | 2.837 | 20 | 24 | fits | 143,911 | 261 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 283,610 | 2.836 | 20 | 50 | fits | 143,911 | 261 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 363,162 | 3.632 | 20 | 50 | fits | 79,948 | 118 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 444,547 | 4.445 | 20 | 20 | fits | 81,451 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 935,658 | 9.357 | 20 | 20 | fits | 63,765 | 61 | 0.699 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 311,760 | 3.118 | 20 | 20 | fits | 79,433 | 118 | 0.442 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 279,042 | 2.790 | 20 | 200 | fits | 143,892 | 261 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 357,859 | 3.579 | 20 | 200 | fits | 79,433 | 118 | 0.442 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 279,966 | 2.800 | 20 | 20 | fits | 143,892 | 261 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 358,563 | 3.586 | 20 | 20 | fits | 79,433 | 118 | 0.442 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 139,714 | 1.397 | 20 | 24 | fits | 134,483 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 282,616 | 2.826 | 20 | 24 | fits | 143,892 | 261 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 282,550 | 2.825 | 20 | 50 | fits | 143,892 | 261 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 361,587 | 3.616 | 20 | 50 | fits | 79,433 | 118 | 0.442 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 443,049 | 4.430 | 20 | 20 | fits | 81,528 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 934,312 | 9.343 | 20 | 20 | fits | 62,916 | 60 | 0.689 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 312,835 | 3.128 | 20 | 20 | fits | 99,084 | 113 | 0.556 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 282,167 | 2.822 | 20 | 200 | fits | 148,058 | 279 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 380,635 | 3.806 | 20 | 200 | fits | 99,084 | 113 | 0.556 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 283,091 | 2.831 | 20 | 20 | fits | 148,058 | 279 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 381,339 | 3.813 | 20 | 20 | fits | 99,084 | 113 | 0.556 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 138,673 | 1.387 | 20 | 24 | fits | 134,483 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 285,741 | 2.857 | 20 | 24 | fits | 148,058 | 279 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 285,675 | 2.857 | 20 | 50 | fits | 148,058 | 279 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 384,363 | 3.844 | 20 | 50 | fits | 99,084 | 113 | 0.556 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 384,297 | 3.843 | 20 | 20 | fits | 99,084 | 113 | 0.556 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 939,274 | 9.393 | 20 | 20 | fits | 40,215 | 34 | 0.759 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 290,982 | 2.910 | 20 | 20 | fits | 81,459 | 106 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 276,180 | 2.762 | 20 | 200 | fits | 143,112 | 276 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 357,023 | 3.570 | 20 | 200 | fits | 81,459 | 106 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 277,104 | 2.771 | 20 | 20 | fits | 143,112 | 276 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 357,727 | 3.577 | 20 | 20 | fits | 81,459 | 106 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 137,632 | 1.376 | 20 | 24 | fits | 134,483 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 279,754 | 2.798 | 20 | 24 | fits | 143,112 | 276 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 279,688 | 2.797 | 20 | 50 | fits | 143,112 | 276 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 360,751 | 3.608 | 20 | 50 | fits | 81,459 | 106 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 445,966 | 4.460 | 20 | 20 | fits | 85,281 | 79 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 930,986 | 9.310 | 20 | 20 | fits | 51,506 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 301,242 | 3.012 | 20 | 20 | fits | 86,696 | 112 | 0.447 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 275,084 | 2.751 | 20 | 200 | fits | 143,057 | 276 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 361,164 | 3.612 | 20 | 200 | fits | 86,696 | 112 | 0.447 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 276,008 | 2.760 | 20 | 20 | fits | 143,057 | 276 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 361,868 | 3.619 | 20 | 20 | fits | 86,696 | 112 | 0.447 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 136,591 | 1.366 | 20 | 24 | fits | 134,483 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 278,658 | 2.787 | 20 | 24 | fits | 143,057 | 276 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 278,592 | 2.786 | 20 | 50 | fits | 143,057 | 276 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 364,892 | 3.649 | 20 | 50 | fits | 86,696 | 112 | 0.447 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 523,830 | 5.238 | 20 | 20 | fits | 81,489 | 74 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 931,588 | 9.316 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 364,911 | 3.649 | 20 | 20 | fits | 79,913 | 118 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 279,511 | 2.795 | 20 | 200 | fits | 148,525 | 266 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 436,064 | 4.361 | 20 | 200 | fits | 79,913 | 118 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 280,435 | 2.804 | 20 | 20 | fits | 148,525 | 266 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 436,768 | 4.368 | 20 | 20 | fits | 79,913 | 118 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 135,550 | 1.355 | 20 | 24 | fits | 134,483 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 283,085 | 2.831 | 20 | 24 | fits | 148,525 | 266 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 283,019 | 2.830 | 20 | 50 | fits | 148,525 | 266 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 439,792 | 4.398 | 20 | 50 | fits | 79,913 | 118 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 521,097 | 5.211 | 20 | 20 | fits | 81,371 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 928,581 | 9.286 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 284,390 | 2.844 | 20 | 20 | fits | 81,987 | 106 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 276,403 | 2.764 | 20 | 200 | fits | 143,057 | 276 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 357,774 | 3.578 | 20 | 200 | fits | 81,987 | 106 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 277,327 | 2.773 | 20 | 20 | fits | 143,057 | 276 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 358,478 | 3.585 | 20 | 20 | fits | 81,987 | 106 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 137,910 | 1.379 | 20 | 24 | fits | 134,483 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 279,977 | 2.800 | 20 | 24 | fits | 143,057 | 276 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 279,911 | 2.799 | 20 | 50 | fits | 143,057 | 276 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 361,502 | 3.615 | 20 | 50 | fits | 81,987 | 106 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 442,924 | 4.429 | 20 | 20 | fits | 81,488 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 850,414 | 8.504 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 284,514 | 2.845 | 20 | 20 | fits | 79,948 | 118 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 276,216 | 2.762 | 20 | 200 | fits | 143,911 | 261 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 355,548 | 3.555 | 20 | 200 | fits | 79,948 | 118 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 277,140 | 2.771 | 20 | 20 | fits | 143,911 | 261 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 356,252 | 3.563 | 20 | 20 | fits | 79,948 | 118 | 0.449 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 136,869 | 1.369 | 20 | 24 | fits | 134,483 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 279,790 | 2.798 | 20 | 24 | fits | 143,911 | 261 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 279,724 | 2.797 | 20 | 50 | fits | 143,911 | 261 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 359,276 | 3.593 | 20 | 50 | fits | 79,948 | 118 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 440,661 | 4.407 | 20 | 20 | fits | 81,451 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 848,092 | 8.481 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 307,874 | 3.079 | 20 | 20 | fits | 79,433 | 118 | 0.442 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 275,156 | 2.752 | 20 | 200 | fits | 143,892 | 261 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 353,973 | 3.540 | 20 | 200 | fits | 79,433 | 118 | 0.442 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 276,080 | 2.761 | 20 | 20 | fits | 143,892 | 261 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 354,677 | 3.547 | 20 | 20 | fits | 79,433 | 118 | 0.442 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 135,828 | 1.358 | 20 | 24 | fits | 134,483 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 278,730 | 2.787 | 20 | 24 | fits | 143,892 | 261 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 278,664 | 2.787 | 20 | 50 | fits | 143,892 | 261 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 357,701 | 3.577 | 20 | 50 | fits | 79,433 | 118 | 0.442 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 439,163 | 4.392 | 20 | 20 | fits | 81,528 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 851,780 | 8.518 | 20 | 20 | fits | 62,943 | 60 | 0.689 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 308,949 | 3.089 | 20 | 20 | fits | 99,084 | 113 | 0.556 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 278,281 | 2.783 | 20 | 200 | fits | 148,058 | 279 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 376,749 | 3.767 | 20 | 200 | fits | 99,084 | 113 | 0.556 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 279,205 | 2.792 | 20 | 20 | fits | 148,058 | 279 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 377,453 | 3.775 | 20 | 20 | fits | 99,084 | 113 | 0.556 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 134,787 | 1.348 | 20 | 24 | fits | 134,483 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 281,855 | 2.819 | 20 | 24 | fits | 148,058 | 279 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 281,789 | 2.818 | 20 | 50 | fits | 148,058 | 279 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 380,477 | 3.805 | 20 | 50 | fits | 99,084 | 113 | 0.556 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 380,411 | 3.804 | 20 | 20 | fits | 99,084 | 113 | 0.556 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 857,213 | 8.572 | 20 | 20 | fits | 40,215 | 34 | 0.759 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 287,152 | 2.872 | 20 | 20 | fits | 81,459 | 106 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 272,350 | 2.724 | 20 | 200 | fits | 143,980 | 281 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 353,193 | 3.532 | 20 | 200 | fits | 81,459 | 106 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 273,274 | 2.733 | 20 | 20 | fits | 143,980 | 281 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 353,897 | 3.539 | 20 | 20 | fits | 81,459 | 106 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 132,934 | 1.329 | 20 | 24 | fits | 134,483 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 275,924 | 2.759 | 20 | 24 | fits | 143,980 | 281 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 275,858 | 2.759 | 20 | 50 | fits | 143,980 | 281 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 356,921 | 3.569 | 20 | 50 | fits | 81,459 | 106 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 438,486 | 4.385 | 20 | 20 | fits | 81,631 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 850,967 | 8.510 | 20 | 20 | fits | 62,778 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 280,053 | 2.801 | 20 | 20 | fits | 81,918 | 106 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 272,066 | 2.721 | 20 | 200 | fits | 143,925 | 281 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 353,368 | 3.534 | 20 | 200 | fits | 81,918 | 106 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 272,990 | 2.730 | 20 | 20 | fits | 143,925 | 281 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 354,072 | 3.541 | 20 | 20 | fits | 81,918 | 106 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 132,705 | 1.327 | 20 | 24 | fits | 134,483 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 275,640 | 2.756 | 20 | 24 | fits | 143,925 | 281 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 275,574 | 2.756 | 20 | 50 | fits | 143,925 | 281 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 357,096 | 3.571 | 20 | 50 | fits | 81,918 | 106 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 442,168 | 4.422 | 20 | 20 | fits | 85,138 | 79 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 849,704 | 8.497 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 298,659 | 2.987 | 20 | 20 | fits | 92,549 | 165 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 265,353 | 2.654 | 20 | 200 | fits | 144,779 | 266 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 357,286 | 3.573 | 20 | 200 | fits | 92,549 | 165 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 266,277 | 2.663 | 20 | 20 | fits | 144,779 | 266 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 357,990 | 3.580 | 20 | 20 | fits | 92,549 | 165 | 0.446 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 125,138 | 1.251 | 20 | 24 | fits | 127,957 | 120 | 0.301 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 268,927 | 2.689 | 20 | 24 | fits | 144,779 | 266 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 268,861 | 2.689 | 20 | 50 | fits | 144,779 | 266 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 361,014 | 3.610 | 20 | 50 | fits | 92,549 | 165 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 442,557 | 4.426 | 20 | 20 | fits | 81,609 | 73 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 850,141 | 8.501 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 320,087 | 3.201 | 20 | 20 | fits | 80,504 | 121 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 284,546 | 2.845 | 20 | 200 | fits | 147,218 | 262 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 364,434 | 3.644 | 20 | 200 | fits | 80,504 | 121 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 285,470 | 2.855 | 20 | 20 | fits | 147,218 | 262 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 365,138 | 3.651 | 20 | 20 | fits | 80,504 | 121 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 141,892 | 1.419 | 20 | 24 | fits | 134,483 | 161 | 0.285 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 288,120 | 2.881 | 20 | 24 | fits | 147,218 | 262 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 288,054 | 2.881 | 20 | 50 | fits | 147,218 | 262 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 368,162 | 3.682 | 20 | 50 | fits | 80,504 | 121 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 449,574 | 4.496 | 20 | 20 | fits | 81,478 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 857,167 | 8.572 | 20 | 20 | fits | 51,487 | 47 | 0.716 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 154,718 | 1.547 | 20 | 200 | fits | 155,658 | 255 | 0.445 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 222,179 | 2.222 | 20 | 20 | fits | 143,781 | 260 | 0.356 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 257,022 | 2.570 | 20 | 24 | fits | 81,026 | 71 | 0.550 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 182,704 | 1.827 | 20 | 50 | fits | 143,781 | 260 | 0.356 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 767,520 | 7.675 | 20 | 20 | fits | 51,794 | 47 | 0.722 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 162,664 | 1.627 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 154,718 | 1.547 | 20 | 200 | fits | 155,658 | 255 | 0.445 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 204,859 | 2.049 | 20 | 20 | fits | 145,536 | 266 | 0.358 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 254,630 | 2.546 | 20 | 24 | fits | 83,610 | 77 | 0.561 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 178,523 | 1.785 | 20 | 50 | fits | 83,417 | 101 | 0.695 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 790,492 | 7.905 | 20 | 20 | fits | 77,158 | 79 | 0.678 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 167,798 | 1.678 | 49 | 49 | fits | 0 | - | 0.000 |
| Talker Advertise RX for every input, bound | `srp.bound_advertise.if0` | 49,257 | 0.493 | 20 | 20 | fits | 49,323 | 25 | 0.869 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 13,368 | 0.134 | 20 | 20 | fits | 24,336 | 21 (35) | 0.800 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 6,487 | 0.065 | 20 | 20 | fits | 20,238 | 17 (14) | 0.824 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 7,565 | 0.076 | 20 | 20 | fits | 19,097 | 18 (14) | 0.804 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 10,445 | 0.104 | 20 | 20 | fits | 23,410 | 21 (35) | 0.779 |
| a registering record of the burst | `srp.register_burst.t0.r0.if0` | 102,168 | 1.022 | 20 | 20 | fits | 94,374 | 40 | 0.841 |
| a registering record of the burst | `srp.register_burst.t0.r1.if0` | 102,087 | 1.021 | 20 | 20 | fits | 94,374 | 40 | 0.841 |
| a registering record of the burst | `srp.register_burst.t0.r2.if0` | 102,006 | 1.020 | 20 | 20 | fits | 94,374 | 40 | 0.841 |
| our MRPDU after a registering triple (JoinTime wait) | `srp.register_tx.t0.if0` | 131,777 | 1.318 | 220 | 220 | fits | 43,894 | 4 | 0.887 |
| ACMP's last record of its burst at a registering triple | `acmp.register_burst.t0.if0` | 144,190 | 1.442 | 20 | 20 | fits | 116,244 | 119 | 0.408 |
| AECP's last record of its burst at a registering triple | `aecp.register_burst.t0.if0` | 175,245 | 1.752 | 20 | 24 | fits | 54,043 | 45 | 0.458 |
| a registering record of the burst | `srp.register_burst.t1.r0.if0` | 63,286 | 0.633 | 20 | 20 | fits | 61,646 | 36 | 0.846 |
| a registering record of the burst | `srp.register_burst.t1.r1.if0` | 63,205 | 0.632 | 20 | 20 | fits | 61,646 | 36 | 0.846 |
| a registering record of the burst | `srp.register_burst.t1.r2.if0` | 63,124 | 0.631 | 20 | 20 | fits | 61,646 | 36 | 0.846 |
| our MRPDU after a registering triple (JoinTime wait) | `srp.register_tx.t1.if0` | 7,670,363 | 76.704 | 220 | 220 | fits | 42,150 | 4 | 0.862 |
| ACMP's last record of its burst at a registering triple | `acmp.register_burst.t1.if0` | 234,861 | 2.349 | 20 | 20 | fits | 68,588 | 33 | 0.839 |
| AECP's last record of its burst at a registering triple | `aecp.register_burst.t1.if0` | 250,979 | 2.510 | 20 | 24 | fits | 54,050 | 45 | 0.458 |
| a registering record of the burst | `srp.register_burst.t2.r0.if0` | 85,465 | 0.855 | 20 | 20 | fits | 84,798 | 40 | 0.829 |
| a registering record of the burst | `srp.register_burst.t2.r1.if0` | 85,384 | 0.854 | 20 | 20 | fits | 84,798 | 40 | 0.829 |
| a registering record of the burst | `srp.register_burst.t2.r2.if0` | 85,303 | 0.853 | 20 | 20 | fits | 84,798 | 40 | 0.829 |
| our MRPDU after a registering triple (JoinTime wait) | `srp.register_tx.t2.if0` | 15,668,319 | 156.683 | 220 | 220 | fits | 41,994 | 4 | 0.865 |
| ACMP's last record of its burst at a registering triple | `acmp.register_burst.t2.if0` | 104,589 | 1.046 | 20 | 20 | fits | 124,929 | 141 | 0.381 |
| AECP's last record of its burst at a registering triple | `aecp.register_burst.t2.if0` | 291,637 | 2.916 | 20 | 24 | fits | 100,211 | 62 | 0.622 |
| LINK_UP | `adp.link_up.if0` | 3,199 | 0.032 | 20 | 200 | fits | 23,900 | 44 (12) | 0.714 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 11,592 | 0.116 | 20 | 200 | fits | 17,049 | 23 (39) | 0.628 |
| LINK_DOWN | `adp.link_down.if0` | 1,950 | 0.019 | 20 | 200 | fits | 19,234 | 23 (9) | 0.686 |
| LINK_UP | `adp.link_up.if0` | 3,199 | 0.032 | 20 | 200 | fits | 23,900 | 44 (12) | 0.714 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 11,592 | 0.116 | 20 | 200 | fits | 17,049 | 23 (39) | 0.628 |
| GM_CHANGE | `adp.gm_change.if0` | 2,147 | 0.021 | 20 | 200 | fits | 11,820 | 17 (11) | 0.400 |
| LINK_UP | `adp.link_up.if0` | 3,199 | 0.032 | 20 | 200 | fits | 23,900 | 44 (12) | 0.714 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 11,592 | 0.116 | 20 | 200 | fits | 17,049 | 23 (39) | 0.628 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,711 | 0.047 | 20 | 200 | fits | 13,245 | 16 (31) | 0.508 |
| LINK_UP | `adp.link_up.if0` | 3,199 | 0.032 | 20 | 200 | fits | 23,900 | 44 (12) | 0.714 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 11,592 | 0.116 | 20 | 200 | fits | 17,049 | 23 (39) | 0.628 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,711 | 0.047 | 20 | 200 | fits | 13,245 | 16 (31) | 0.508 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 47,536 | 0.475 | 20 | 20 | fits | 17,265 | 9 | 0.835 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 34,291 | 0.343 | 20 | 20 | fits | 34,357 | 21 | 0.851 |
| malformed MRPDU discard | `srp.malformed.if0` | 18,597 | 0.186 | 20 | 20 | fits | 18,663 | 21 | 0.688 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 57,551 | 0.576 | 220 | 220 | fits | 33,675 | 7 | 0.899 |
| an event behind 15 others | `backlog.event.if0` | 148,650 | 1.486 | 20 | 200 | fits | 46,150 | 78 | 0.557 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 352,028 | 3.520 | 20 | 20 | fits | 133,788 | 161 | 0.346 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 370,860 | 3.709 | 20 | 200 | fits | 133,788 | 161 | 0.346 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 370,244 | 3.702 | 20 | 200 | fits | 133,788 | 161 | 0.346 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 366,538 | 3.665 | 20 | 20 | fits | 133,788 | 161 | 0.346 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 365,702 | 3.657 | 20 | 20 | fits | 133,788 | 161 | 0.346 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 138,477 | 1.385 | 20 | 24 | fits | 139,368 | 164 | 0.307 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 235,400 | 2.354 | 20 | 24 | fits | 51,763 | 26 | 0.720 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 369,122 | 3.691 | 20 | 50 | fits | 133,788 | 161 | 0.346 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 368,726 | 3.687 | 20 | 50 | fits | 133,788 | 161 | 0.346 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 413,016 | 4.130 | 20 | 20 | fits | 41,980 | 165 | 0.180 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 485,331 | 4.853 | 20 | 20 | fits | 31,145 | 112 | 0.126 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 285,674 | 2.857 | 20 | 20 | fits | 97,850 | 110 | 0.571 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 277,657 | 2.777 | 20 | 200 | fits | 148,665 | 283 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 374,891 | 3.749 | 20 | 200 | fits | 97,850 | 110 | 0.571 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 278,581 | 2.786 | 20 | 20 | fits | 148,665 | 283 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 375,595 | 3.756 | 20 | 20 | fits | 97,850 | 110 | 0.571 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 133,556 | 1.336 | 20 | 24 | fits | 133,742 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 281,231 | 2.812 | 20 | 24 | fits | 148,665 | 283 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 281,165 | 2.812 | 20 | 50 | fits | 148,665 | 283 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 378,619 | 3.786 | 20 | 50 | fits | 97,850 | 110 | 0.571 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 378,553 | 3.786 | 20 | 20 | fits | 97,850 | 110 | 0.571 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 855,624 | 8.556 | 20 | 20 | fits | 40,210 | 34 | 0.759 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 10,707 | 0.107 | 20 | 20 | fits | 20,780 | 19 | 0.744 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 277,657 | 2.777 | 20 | 200 | fits | 148,665 | 283 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 23,251 | 0.233 | 20 | 200 | fits | 20,780 | 19 | 0.744 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 278,581 | 2.786 | 20 | 20 | fits | 148,665 | 283 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 366,653 | 3.667 | 20 | 20 | fits | 88,908 | 100 | 0.543 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 133,556 | 1.336 | 20 | 24 | fits | 133,742 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 281,231 | 2.812 | 20 | 24 | fits | 148,665 | 283 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 281,165 | 2.812 | 20 | 50 | fits | 148,665 | 283 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 369,677 | 3.697 | 20 | 50 | fits | 88,908 | 100 | 0.543 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 369,611 | 3.696 | 20 | 20 | fits | 88,908 | 100 | 0.543 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 827,473 | 8.275 | 20 | 20 | fits | 40,389 | 34 | 0.761 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,246,012 | 62.460 | 20 | 20 | MISS ceiling | 14,691 | 13 | 0.550 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,260,680 | 62.607 | 20 | 20 | MISS ceiling | 14,665 | 13 | 0.516 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,275,088 | 62.751 | 20 | 20 | MISS ceiling | 14,465 | 13 | 0.550 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,289,523 | 62.895 | 20 | 20 | MISS ceiling | 14,511 | 13 | 0.550 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,303,870 | 63.039 | 20 | 20 | MISS ceiling | 14,410 | 13 | 0.550 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 148,563 | 1.486 | 20 | 200 | fits | 147,147 | 231 | 0.407 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 241,124 | 2.411 | 20 | 200 | fits | 93,177 | 162 | 0.551 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 144,241 | 1.442 | 20 | 20 | fits | 147,147 | 231 | 0.407 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,174,031 | 61.740 | 20 | 20 | MISS ceiling | 25,391 | 15 | 0.702 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 147,881 | 1.479 | 20 | 24 | fits | 147,147 | 231 | 0.407 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,152,126 | 61.521 | 20 | 24 | MISS ceiling | 121,013 | 106 | 0.352 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 146,825 | 1.468 | 20 | 50 | fits | 147,147 | 231 | 0.407 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 239,606 | 2.396 | 20 | 50 | fits | 93,177 | 162 | 0.551 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 239,540 | 2.395 | 20 | 20 | fits | 93,177 | 162 | 0.551 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 698,362 | 6.984 | 20 | 20 | fits | 40,718 | 34 | 0.775 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,327 | 0.053 | 20 | 20 | fits | 18,127 | 13 (29) | 0.713 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,028 | 0.070 | 20 | 20 | fits | 20,160 | 19 (35) | 0.720 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 10,546 | 0.105 | 20 | 20 | fits | 23,510 | 21 (12) | 0.782 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 10,473 | 0.105 | 20 | 50 | fits | 23,900 | 44 | 0.714 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 8,486 | 0.085 | 20 | 50 | fits | 18,609 | 35 | 0.621 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 15,759 | 0.158 | 20 | 50 | fits | 18,228 | 35 | 0.602 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 17,393 | 0.174 | 20 | 50 | fits | 23,232 | 61 | 0.589 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 19,348 | 0.193 | 20 | 50 | fits | 23,232 | 61 | 0.589 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 8,746 | 0.087 | 20 | 50 | fits | 18,278 | 30 | 0.617 |
| set_name | `aecp_fanout.set_name.if0` | 41,781 | 0.418 | 20 | 24 | fits | 54,507 | 89 | 0.581 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 40,437 | 0.404 | 20 | 24 | fits | 48,897 | 78 | 0.611 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 35,932 | 0.359 | 20 | 24 | fits | 44,578 | 79 | 0.575 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 37,181 | 0.372 | 20 | 24 | fits | 43,752 | 78 | 0.567 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 48,878 | 0.489 | 20 | 24 | fits | 58,488 | 110 | 0.597 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 273,302 | 2.733 | 20 | 24 | fits | 54,263 | 109 | 0.565 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 346,175 | 3.462 | 20 | 24 | fits | 59,825 | 110 | 0.600 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 345,248 | 3.452 | 20 | 24 | fits | 58,658 | 109 | 0.598 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 334,366 | 3.344 | 20 | 24 | fits | 46,810 | 67 | 0.607 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 51,454 | 0.515 | 20 | 24 | fits | 59,687 | 77 | 0.622 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 355,902 | 3.559 | 20 | 24 | fits | 57,272 | 78 | 0.622 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 35,714 | 0.357 | 20 | 24 | fits | 44,501 | 78 | 0.575 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 38,884 | 0.389 | 20 | 24 | fits | 44,336 | 79 | 0.570 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 72,375 | 0.724 | 20 | 24 | fits | 35,673 | 59 | 0.490 |
| BIND_RX | `acmp.bind_rx.if0` | 18,482 | 0.185 | 20 | 20 | fits | 37,920 | 26 (77) | 0.794 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,506 | 0.095 | 20 | 20 | fits | 26,320 | 19 (32) | 0.825 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 11,191 | 0.112 | 20 | 20 | fits | 22,632 | 15 (47) | 0.762 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,282 | 0.133 | 20 | 20 | fits | 34,248 | 18 (50) | 0.834 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 11,514 | 0.115 | 20 | 20 | fits | 22,662 | 17 (48) | 0.734 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,439 | 0.094 | 20 | 20 | fits | 20,888 | 16 (48) | 0.670 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 8,865 | 0.089 | 20 | 20 | fits | 19,685 | 16 (48) | 0.637 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 8,889 | 0.089 | 20 | 20 | fits | 19,666 | 16 (48) | 0.637 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 10,904 | 0.109 | 20 | 24 | fits | 23,789 | 20 | 0.766 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 20,668 | 0.207 | 20 | 24 | fits | 27,883 | 20 | 0.707 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 15,926 | 0.159 | 20 | 24 | fits | 24,948 | 20 | 0.741 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 17,146 | 0.171 | 20 | 24 | fits | 24,281 | 20 | 0.732 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 16,035 | 0.160 | 20 | 24 | fits | 25,003 | 20 | 0.734 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 17,843 | 0.178 | 20 | 24 | fits | 24,829 | 20 | 0.735 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 17,111 | 0.171 | 20 | 24 | fits | 24,096 | 20 | 0.740 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 15,281 | 0.153 | 20 | 24 | fits | 24,091 | 20 | 0.751 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 16,745 | 0.167 | 20 | 24 | fits | 23,485 | 20 | 0.750 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 17,433 | 0.174 | 20 | 24 | fits | 26,442 | 21 | 0.653 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 16,644 | 0.166 | 20 | 24 | fits | 23,672 | 20 | 0.772 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 14,343 | 0.143 | 20 | 24 | fits | 23,364 | 20 | 0.767 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 17,045 | 0.170 | 20 | 24 | fits | 24,098 | 20 | 0.741 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 15,619 | 0.156 | 20 | 24 | fits | 24,584 | 20 | 0.738 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 15,020 | 0.150 | 20 | 24 | fits | 23,906 | 20 | 0.753 |
| get_configuration | `aecp.get_configuration.if0` | 15,027 | 0.150 | 20 | 24 | fits | 21,299 | 20 | 0.752 |
| entity_available | `aecp.entity_available.if0` | 12,815 | 0.128 | 20 | 24 | fits | 21,168 | 20 | 0.734 |
| get_name | `aecp.get_name.if0` | 17,142 | 0.171 | 20 | 24 | fits | 24,163 | 20 | 0.760 |
| get_counters | `aecp.get_counters.if0` | 17,894 | 0.179 | 20 | 24 | fits | 27,453 | 20 | 0.755 |
| get_avb_info | `aecp.get_avb_info.if0` | 18,213 | 0.182 | 20 | 24 | fits | 24,903 | 20 | 0.794 |
| get_as_path | `aecp.get_as_path.if0` | 20,923 | 0.209 | 20 | 24 | fits | 30,470 | 100 | 0.560 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 14,996 | 0.150 | 20 | 24 | fits | 21,727 | 20 | 0.760 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 14,405 | 0.144 | 20 | 24 | fits | 20,544 | 20 | 0.730 |
| set_name | `aecp.set_name.if0` | 21,422 | 0.214 | 20 | 24 | fits | 41,371 | 44 | 0.760 |
| lock_entity | `aecp.lock_entity.if0` | 21,070 | 0.211 | 20 | 24 | fits | 33,361 | 33 | 0.798 |
| unlock_entity | `aecp.unlock_entity.if0` | 19,177 | 0.192 | 20 | 24 | fits | 32,572 | 33 | 0.791 |
| Talker Advertise RX for every input, bound | `srp.register_advertise.if0` | 49,075 | 0.491 | 20 | 20 | fits | 49,141 | 25 | 0.867 |
| REBOOT, refused BAD_ARGUMENTS | `aecp_reboot.short.if0` | 9,414 | 0.094 | 20 | 24 | fits | 24,172 | 17 | 0.781 |
| REBOOT, refused NOT_SUPPORTED | `aecp_reboot.stream_input.if0` | 10,896 | 0.109 | 20 | 24 | fits | 24,143 | 17 | 0.780 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | `aecp_reboot.entity_1.if0` | 9,674 | 0.097 | 20 | 24 | fits | 24,234 | 17 | 0.781 |
| REBOOT, refused ENTITY_LOCKED | `aecp_reboot.locked.if0` | 11,111 | 0.111 | 20 | 24 | fits | 24,849 | 17 | 0.796 |
| REBOOT | `aecp_reboot.accepted.if0` | 32,075 | 0.321 | 20 | 24 | fits | 37,445 | 66 | 0.541 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 137,041 | 1.370 | 20 | 24 | fits | 150,373 | 137 | 0.323 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 337,689 | 3.377 | 20 | 24 | fits | 141,653 | 114 | 0.286 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 240,250 | 2.402 | 20 | 24 | fits | 36,893 | 17 | 0.644 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 393,613 | 3.936 | 20 | 24 | fits | 86,631 | 18 | 0.654 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 351,956 | 3.520 | 20 | 24 | fits | 96,674 | 17 | 0.654 |
| READ_DESCRIPTOR held for a token (#917) | `aecp.held.read_descriptor.if0` | 514,742 | 5.147 | 20 | 24 | fits | 26,995 | 17 | 0.718 |
| LINK_UP | `fixture.link_up.if0` | 3,199 | 0.032 | 20 | 200 | fits | 23,900 | 44 (12) | 0.714 |
| malformed MRPDU discard | `fixture.malformed.if0` | 18,797 | 0.188 | 20 | 20 | fits | 18,863 | 21 | 0.699 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 30,159 | 0.302 | 20 | 24 | fits | 42,571 | 43 | 0.775 |
| LINK_DOWN | `fixture.link_down.if0` | 2,457 | 0.025 | 20 | 200 | fits | 22,000 | 23 (9) | 0.752 |
| BIND_RX | `fixture.bind_rx.if0` | 19,101 | 0.191 | 20 | 20 | fits | 37,962 | 26 (77) | 0.796 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 12,766 | 0.128 | 20 | 20 | fits | 29,873 | 29 (35) | 0.764 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 15,395 | 0.154 | 20 | 20 | fits | 19,843 | 13 (29) | 0.765 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 76,907 | 0.769 | 20 | 200 | fits | 77,011 | 86 | 0.733 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 76,907 | 0.769 | 20 | 200 | fits | 77,011 | 86 | 0.733 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 76,633 | 0.766 | 20 | 20 | fits | 77,011 | 86 | 0.733 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 76,633 | 0.766 | 20 | 20 | fits | 77,011 | 86 | 0.733 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 76,841 | 0.768 | 20 | 24 | fits | 77,011 | 86 | 0.733 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 76,841 | 0.768 | 20 | 24 | fits | 77,011 | 86 | 0.733 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 76,775 | 0.768 | 20 | 50 | fits | 77,011 | 86 | 0.733 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 76,775 | 0.768 | 20 | 50 | fits | 77,011 | 86 | 0.733 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 76,709 | 0.767 | 20 | 20 | fits | 77,011 | 86 | 0.733 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 76,709 | 0.767 | 20 | 20 | fits | 77,011 | 86 | 0.733 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
