### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 92 paths and 7 of 965 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.194 (0.421) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.090 (0.239) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.077 (0.263) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.156 (0.537) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.109 (0.264) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.090 (0.239) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.095 (0.248) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.111 (0.266) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.103 (0.330) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.106 (0.475) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.172 (0.561) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.218 (0.544) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.130 (0.508) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.142 (0.589) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.173 (0.502) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.139 (0.395) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.046 (0.171) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.024 (0.178) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.026 (0.274) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.026 (0.283) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.089 (0.260) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.166 (0.505) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.127 (0.457) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.275 (0.598) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.127 (0.455) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.158 (0.489) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.264 (0.588) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.189 (0.562) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.201 (0.527) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.197 (0.534) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.270 (0.593) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.264 (0.588) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.147 (0.479) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.287 (0.612) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.254 (0.587) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.141 (0.474) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.151 (0.484) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.259 (0.585) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.154 (0.491) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.259 (0.586) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.316 (0.651) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.272 (0.609) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.150 (0.482) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.243 (0.571) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.327 (0.760) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.135 (0.464) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.145 (0.350) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 3.103 (3.425) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.497 (0.795) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.615 (0.937) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.520 (0.890) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.556 (0.846) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.603 (0.839) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.328 (3.563) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.508 (0.801) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 3.068 (3.400) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.049 (2.427) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.665 (4.036) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 2.983 (3.354) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.446 (1.685) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.296 (4.675) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 4.757 (5.366) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.080 (0.448) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.659 (2.101) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.115 (63.311) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.866 (64.065) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.318 (0.464) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-burst.held.acmp.if0` (save-burst) | 2.352 | fits | 11 acmp | 4 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-burst.held.adp.if0` (save-burst) | 1.558 | fits | 7 adp | 4 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 2.906 | fits | 15 aecp | 4 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 2.505 | fits | 6 maap | 4 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 10.016 | fits | 31 srp | 4 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.191 (0.540) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.102 (0.233) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.109 (0.283) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.166 (0.540) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.119 (0.453) | fits | 0 events | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.688 | fits | 0 srp | 7 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.154 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.204 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.197 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 5.262 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-4.service.aecp.first.if0` (backlog-adp@verify-4) | 2.367 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.938 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.180 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.maap.last.if0` (backlog-adp@program-aged2-7) | 5.299 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-7.service.srp.first.if0` (backlog-adp@program-aged2-7) | 6.171 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-1.service.srp.last.if0` (backlog-adp@blank-1) | 11.192 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.901 (0.991) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.459 (0.459) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.234 (0.234) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.781 (0.858) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 13.356 | 13 | 151,590 (1.516) | yes | - |
| backlog-adp@blank-1 | 0 | 13.978 | 12 | 150,636 (1.506) | yes | - |
| backlog-adp@blank-2 | 0 | 13.853 | 12 | 150,636 (1.506) | yes | - |
| backlog-adp@blank-3 | 1 | 13.099 | 11 | 148,955 (1.490) | yes | - |
| backlog-adp@blank-4 | 1 | 13.099 | 11 | 148,955 (1.490) | yes | - |
| backlog-adp@blank-5 | 1 | 13.099 | 11 | 148,955 (1.490) | yes | - |
| backlog-adp@blank-6 | 1 | 13.099 | 11 | 148,955 (1.490) | yes | - |
| backlog-adp@blank-7 | 1 | 13.099 | 11 | 148,955 (1.490) | yes | - |
| backlog-adp@program-0 | 0 | 12.172 | 11 | 150,387 (1.504) | yes | - |
| backlog-adp@program-1 | 0 | 11.922 | 11 | 150,387 (1.504) | yes | - |
| backlog-adp@program-2 | 0 | 11.672 | 11 | 150,387 (1.504) | yes | - |
| backlog-adp@program-3 | 0 | 12.381 | 11 | 150,145 (1.501) | yes | - |
| backlog-adp@program-4 | 0 | 15.129 | 14 | 150,466 (1.505) | yes | - |
| backlog-adp@program-5 | 0 | 14.879 | 14 | 150,466 (1.505) | yes | - |
| backlog-adp@program-6 | 0 | 14.629 | 14 | 150,466 (1.505) | yes | - |
| backlog-adp@program-7 | 0 | 14.355 | 14 | 150,072 (1.501) | yes | - |
| backlog-adp@verify-0 | 0 | 13.434 | 11 | 150,240 (1.502) | yes | - |
| backlog-adp@verify-1 | 0 | 13.309 | 11 | 150,240 (1.502) | yes | - |
| backlog-adp@verify-2 | 0 | 13.184 | 11 | 150,240 (1.502) | yes | - |
| backlog-adp@verify-3 | 0 | 13.059 | 11 | 150,240 (1.502) | yes | - |
| backlog-adp@verify-4 | 0 | 13.854 | 11 | 150,167 (1.502) | yes | - |
| backlog-adp@verify-5 | 0 | 13.729 | 11 | 150,167 (1.502) | yes | - |
| backlog-adp@verify-6 | 0 | 13.604 | 11 | 150,167 (1.502) | yes | - |
| backlog-adp@verify-7 | 0 | 13.479 | 11 | 150,167 (1.502) | yes | - |
| backlog-adp@blank-aged2-0 | 1 | 12.916 | 11 | 150,115 (1.501) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 13.815 | 11 | 149,040 (1.490) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 13.778 | 11 | 149,202 (1.492) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 15.861 | 13 | 149,040 (1.490) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 14.878 | 12 | 149,162 (1.492) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 13.957 | 12 | 149,202 (1.492) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 14.998 | 13 | 150,128 (1.501) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 13.931 | 11 | 149,282 (1.493) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 14.231 | 13 | 149,089 (1.491) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 13.135 | 12 | 150,290 (1.503) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 13.101 | 12 | 149,482 (1.495) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 12.955 | 10 | 149,174 (1.492) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 13.054 | 11 | 149,349 (1.493) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 16.155 | 14 | 149,187 (1.492) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 15.311 | 14 | 149,349 (1.493) | yes | - |
| backlog-adp@blank-aged1-7 | 1 | 14.188 | 12 | 149,393 (1.494) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 12.770 | 13 | 149,293 (1.493) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 12.519 | 12 | 150,008 (1.500) | yes | - |
| backlog-adp@program-aged2-2 | 1 | 12.418 | 10 | 149,778 (1.498) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 12.460 | 11 | 149,184 (1.492) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 12.441 | 11 | 149,346 (1.493) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 12.383 | 11 | 149,184 (1.492) | yes | - |
| backlog-adp@program-aged2-6 | 1 | 15.157 | 13 | 149,123 (1.491) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 14.095 | 14 | 149,468 (1.495) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 12.363 | 11 | 149,021 (1.490) | yes | - |
| backlog-adp@program-aged1-1 | 1 | 12.289 | 10 | 149,558 (1.496) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 12.950 | 13 | 149,104 (1.491) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 12.523 | 12 | 150,355 (1.504) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 12.332 | 11 | 149,131 (1.491) | yes | - |
| backlog-adp@program-aged1-5 | 1 | 12.297 | 10 | 149,063 (1.491) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 12.453 | 11 | 149,293 (1.493) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 14.043 | 14 | 149,131 (1.491) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 12.931 | 11 | 149,293 (1.493) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 13.811 | 11 | 149,131 (1.491) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 14.957 | 13 | 149,293 (1.493) | yes | - |
| backlog-adp@verify-aged2-3 | 1 | 14.021 | 12 | 149,899 (1.499) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 13.963 | 12 | 150,064 (1.501) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 13.953 | 12 | 150,421 (1.504) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 14.888 | 12 | 149,346 (1.493) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 13.933 | 11 | 149,353 (1.494) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 13.055 | 11 | 148,753 (1.488) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 13.020 | 11 | 149,146 (1.491) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 12.983 | 11 | 148,984 (1.490) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 12.941 | 10 | 149,422 (1.494) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 15.142 | 13 | 149,146 (1.491) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 13.284 | 13 | 148,984 (1.490) | yes | - |
| backlog-adp@verify-aged1-6 | 1 | 15.134 | 12 | 150,434 (1.504) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 14.192 | 12 | 149,177 (1.492) | yes | - |
| backlog | 0 | 5.807 | 7 | 151,943 (1.519) | yes | - |
| backlog-adp | 0 | 10.994 | 13 | 149,552 (1.496) | yes | - |
| backlog-adp-refill | 0 | 40.776 | 25 | 149,552 (1.496) | yes | - |
| backlog-owed | 0 | 64.533 | 25 | 147,528 (1.475) | yes | - |
| fixture | 0 | 1.334 | 2 | 83,490 (0.835) | yes | - |

Composed maximum over the 4 backlog windows: 151,943 CPU cycles (1.519 ms), backlog.
Over the windows that released their whole load only: 151,943 (1.519 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-flight | 3131 | 0 | 156,656 (1.567) | fits |
| save-burst | 2916 | 0 | 156,656 (1.567) | fits |
| acmp-notk | 3609 | 0 | 98,757 (0.988) | fits |
| save-second | 43978 | 0 | 50,411 (0.504) | fits |
| backlog-adp@blank-0 | 484 | 0 | 151,590 (1.516) | fits |
| backlog-adp@blank-1 | 483 | 0 | 150,636 (1.506) | fits |
| backlog-adp@blank-2 | 483 | 0 | 150,636 (1.506) | fits |
| backlog-adp@blank-3 | 483 | 0 | 154,259 (1.543) | fits |
| backlog-adp@blank-4 | 483 | 0 | 154,259 (1.543) | fits |
| backlog-adp@blank-5 | 483 | 0 | 154,259 (1.543) | fits |
| backlog-adp@blank-6 | 483 | 0 | 154,259 (1.543) | fits |
| backlog-adp@blank-7 | 483 | 0 | 154,259 (1.543) | fits |
| backlog-adp@program-0 | 493 | 0 | 150,387 (1.504) | fits |
| backlog-adp@program-1 | 493 | 0 | 150,387 (1.504) | fits |
| backlog-adp@program-2 | 493 | 0 | 150,387 (1.504) | fits |
| backlog-adp@program-3 | 493 | 0 | 150,145 (1.501) | fits |
| backlog-adp@program-4 | 496 | 0 | 150,466 (1.505) | fits |
| backlog-adp@program-5 | 496 | 0 | 150,466 (1.505) | fits |
| backlog-adp@program-6 | 496 | 0 | 150,466 (1.505) | fits |
| backlog-adp@program-7 | 496 | 0 | 150,072 (1.501) | fits |
| backlog-adp@verify-0 | 499 | 0 | 150,240 (1.502) | fits |
| backlog-adp@verify-1 | 499 | 0 | 150,240 (1.502) | fits |
| backlog-adp@verify-2 | 499 | 0 | 150,240 (1.502) | fits |
| backlog-adp@verify-3 | 499 | 0 | 150,240 (1.502) | fits |
| backlog-adp@verify-4 | 499 | 0 | 150,167 (1.502) | fits |
| backlog-adp@verify-5 | 499 | 0 | 150,167 (1.502) | fits |
| backlog-adp@verify-6 | 499 | 0 | 150,167 (1.502) | fits |
| backlog-adp@verify-7 | 499 | 0 | 150,167 (1.502) | fits |
| backlog-adp@blank-aged2-0 | 730 | 0 | 150,115 (1.501) | fits |
| backlog-adp@blank-aged2-1 | 737 | 0 | 149,040 (1.490) | fits |
| backlog-adp@blank-aged2-2 | 744 | 0 | 149,202 (1.492) | fits |
| backlog-adp@blank-aged2-3 | 753 | 0 | 149,040 (1.490) | fits |
| backlog-adp@blank-aged2-4 | 760 | 0 | 149,202 (1.492) | fits |
| backlog-adp@blank-aged2-5 | 767 | 0 | 149,202 (1.492) | fits |
| backlog-adp@blank-aged2-6 | 775 | 0 | 150,128 (1.501) | fits |
| backlog-adp@blank-aged2-7 | 781 | 0 | 150,780 (1.508) | fits |
| backlog-adp@blank-aged1-0 | 674 | 0 | 149,089 (1.491) | fits |
| backlog-adp@blank-aged1-1 | 680 | 0 | 150,290 (1.503) | fits |
| backlog-adp@blank-aged1-2 | 687 | 0 | 149,482 (1.495) | fits |
| backlog-adp@blank-aged1-3 | 693 | 0 | 149,349 (1.493) | fits |
| backlog-adp@blank-aged1-4 | 701 | 0 | 149,349 (1.493) | fits |
| backlog-adp@blank-aged1-5 | 711 | 0 | 149,187 (1.492) | fits |
| backlog-adp@blank-aged1-6 | 718 | 0 | 149,349 (1.493) | fits |
| backlog-adp@blank-aged1-7 | 724 | 0 | 149,393 (1.494) | fits |
| backlog-adp@program-aged2-0 | 757 | 0 | 149,293 (1.493) | fits |
| backlog-adp@program-aged2-1 | 763 | 0 | 150,008 (1.500) | fits |
| backlog-adp@program-aged2-2 | 770 | 0 | 151,052 (1.511) | fits |
| backlog-adp@program-aged2-3 | 777 | 0 | 149,184 (1.492) | fits |
| backlog-adp@program-aged2-4 | 784 | 0 | 149,346 (1.493) | fits |
| backlog-adp@program-aged2-5 | 791 | 0 | 149,184 (1.492) | fits |
| backlog-adp@program-aged2-6 | 801 | 0 | 149,346 (1.493) | fits |
| backlog-adp@program-aged2-7 | 809 | 0 | 149,468 (1.495) | fits |
| backlog-adp@program-aged1-0 | 697 | 0 | 149,021 (1.490) | fits |
| backlog-adp@program-aged1-1 | 704 | 0 | 149,558 (1.496) | fits |
| backlog-adp@program-aged1-2 | 714 | 0 | 149,104 (1.491) | fits |
| backlog-adp@program-aged1-3 | 720 | 0 | 150,355 (1.504) | fits |
| backlog-adp@program-aged1-4 | 726 | 0 | 149,131 (1.491) | fits |
| backlog-adp@program-aged1-5 | 733 | 0 | 149,293 (1.493) | fits |
| backlog-adp@program-aged1-6 | 741 | 0 | 149,293 (1.493) | fits |
| backlog-adp@program-aged1-7 | 751 | 0 | 149,131 (1.491) | fits |
| backlog-adp@verify-aged2-0 | 772 | 0 | 149,293 (1.493) | fits |
| backlog-adp@verify-aged2-1 | 779 | 0 | 149,131 (1.491) | fits |
| backlog-adp@verify-aged2-2 | 788 | 0 | 149,293 (1.493) | fits |
| backlog-adp@verify-aged2-3 | 795 | 0 | 149,899 (1.499) | fits |
| backlog-adp@verify-aged2-4 | 802 | 0 | 150,064 (1.501) | fits |
| backlog-adp@verify-aged2-5 | 809 | 0 | 150,421 (1.504) | fits |
| backlog-adp@verify-aged2-6 | 816 | 0 | 149,346 (1.493) | fits |
| backlog-adp@verify-aged2-7 | 823 | 0 | 149,353 (1.494) | fits |
| backlog-adp@verify-aged1-0 | 714 | 0 | 149,056 (1.491) | fits |
| backlog-adp@verify-aged1-1 | 721 | 0 | 149,146 (1.491) | fits |
| backlog-adp@verify-aged1-2 | 728 | 0 | 148,984 (1.490) | fits |
| backlog-adp@verify-aged1-3 | 735 | 0 | 149,422 (1.494) | fits |
| backlog-adp@verify-aged1-4 | 745 | 0 | 149,146 (1.491) | fits |
| backlog-adp@verify-aged1-5 | 752 | 0 | 148,984 (1.490) | fits |
| backlog-adp@verify-aged1-6 | 759 | 0 | 150,434 (1.504) | fits |
| backlog-adp@verify-aged1-7 | 766 | 0 | 149,177 (1.492) | fits |
| adp-advertise | 598 | 0 | 29,874 (0.299) | fits |
| save-held | 1467 | 0 | 156,656 (1.567) | fits |
| save-starved | 23117 | 0 | 156,656 (1.567) | fits |
| acmp-noresp | 2023 | 0 | 50,440 (0.504) | fits |
| save | 610 | 0 | 44,974 (0.450) | fits |
| srp | 290 | 0 | 56,882 (0.569) | fits |
| backlog | 286 | 0 | 151,943 (1.519) | fits |
| backlog-adp | 317 | 0 | 149,552 (1.496) | fits |
| backlog-adp-refill | 329 | 0 | 149,552 (1.496) | fits |
| backlog-owed | 311 | 0 | 147,528 (1.475) | fits |
| acmp-disc | 937 | 0 | 98,431 (0.984) | fits |
| maap | 182 | 0 | 29,874 (0.299) | fits |
| adp-link | 89 | 0 | 40,422 (0.404) | fits |
| adp-gm | 88 | 0 | 29,678 (0.297) | fits |
| adp-discover | 88 | 0 | 29,678 (0.297) | fits |
| control | 88 | 0 | 29,678 (0.297) | fits |
| aecp-fanout | 113 | 0 | 63,200 (0.632) | fits |
| acmp-cmd | 85 | 0 | 41,200 (0.412) | fits |
| aecp | 110 | 0 | 44,065 (0.441) | fits |
| aecp-largest-notice | 107 | 0 | 147,796 (1.478) | fits |
| datapath-events | 116 | 0 | 29,678 (0.297) | fits |
| fixture | 151 | 0 | 83,490 (0.835) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | +10.306 ms, 76,924 (0.769 ms), read-back | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 10.268 (20) | 9.732 |
| backlog-adp@blank-aged2-1 | 2 | +9.435 ms, 76,879 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 11.030 (20) | 8.970 |
| backlog-adp@blank-aged2-2 | 2 | +7.680 ms, 76,879 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 10.994 (20) | 9.006 |
| backlog-adp@blank-aged2-3 | 2 | +6.776 ms, 76,986 (0.770 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 10.955 (20) | 9.045 |
| backlog-adp@blank-aged2-4 | 2 | +5.967 ms, 76,879 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 10.881 (20) | 9.119 |
| backlog-adp@blank-aged2-5 | 2 | +4.493 ms, 76,940 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 11.174 (20) | 8.826 |
| backlog-adp@blank-aged2-6 | 2 | +4.419 ms, 76,858 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 11.100 (20) | 8.900 |
| backlog-adp@blank-aged2-7 | 2 | +4.255 ms, 76,923 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 10.949 (20) | 9.051 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 10.271 (20) | 9.729 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 10.347 (20) | 9.653 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 10.314 (20) | 9.686 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 10.167 (20) | 9.833 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 10.267 (20) | 9.733 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 10.177 (20) | 9.823 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 10.185 (20) | 9.815 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 10.132 (20) | 9.868 |
| backlog-adp@program-aged2-0 | 2 | none | +10.270 ms, 80,692 (0.807 ms), issue | `backlog-adp@program-aged2-0.service.srp.last.if0` | 10.232 (20) | 9.768 |
| backlog-adp@program-aged2-1 | 2 | none | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 11.107 (20) | 8.893 |
| backlog-adp@program-aged2-2 | 2 | +7.597 ms, 80,591 (0.806 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 11.006 (20) | 8.994 |
| backlog-adp@program-aged2-3 | 2 | none | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 11.048 (20) | 8.952 |
| backlog-adp@program-aged2-4 | 2 | none | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 11.027 (20) | 8.973 |
| backlog-adp@program-aged2-5 | 2 | none | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 10.971 (20) | 9.029 |
| backlog-adp@program-aged2-6 | 2 | none | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 10.933 (20) | 9.067 |
| backlog-adp@program-aged2-7 | 2 | none | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 11.067 (20) | 8.933 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 10.204 (20) | 9.796 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 10.130 (20) | 9.870 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 10.274 (20) | 9.726 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 10.364 (20) | 9.636 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 10.173 (20) | 9.827 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 10.137 (20) | 9.863 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 10.294 (20) | 9.706 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 10.222 (20) | 9.778 |
| backlog-adp@verify-aged2-0 | 2 | none | +10.304 ms, 77,477 (0.775 ms), read-back | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 10.266 (20) | 9.734 |
| backlog-adp@verify-aged2-1 | 2 | +9.408 ms, 77,370 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 11.007 (20) | 8.993 |
| backlog-adp@verify-aged2-2 | 2 | +7.735 ms, 77,370 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 10.932 (20) | 9.068 |
| backlog-adp@verify-aged2-3 | 2 | +6.863 ms, 77,477 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 10.921 (20) | 9.079 |
| backlog-adp@verify-aged2-4 | 2 | +5.203 ms, 77,548 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 11.158 (20) | 8.842 |
| backlog-adp@verify-aged2-5 | 2 | +4.465 ms, 77,364 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 11.150 (20) | 8.850 |
| backlog-adp@verify-aged2-6 | 2 | +4.281 ms, 77,364 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 10.962 (20) | 9.038 |
| backlog-adp@verify-aged2-7 | 2 | +4.246 ms, 77,364 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 10.929 (20) | 9.071 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 10.130 (20) | 9.870 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 10.215 (20) | 9.785 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 10.178 (20) | 9.822 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 10.135 (20) | 9.865 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 10.195 (20) | 9.805 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 10.181 (20) | 9.819 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 10.293 (20) | 9.707 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 10.267 (20) | 9.733 |

Least margin over the aged windows: 8.826 ms, `backlog-adp@blank-aged2-5.service.srp.last.if0` at 11.174 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.340 | 6,070 | 102 | 2 | 30.865 | yes | within |
| save-held | 1097.164 | 4,070 | 102 | - | 17.213 | no | within |
| save-starved | 4049.108 | 4,070 | 102 | - | 31.292 | yes | within |
| save | 1081.825 | 4,070 | 102 | - | 26.002 | no | within |

Names from their response to durable (save_burst.py; #920, the ruling of #665 issuecomment-6899740728, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-flight | 1 | 165.045 (0) | 5,000 | 2 | - | - | 19 steps (want 19), 7.939 ms | within |
| save-burst | 39 | 1107.785 (0) | 5,000 | 1 | - | - | sequence 1, 0 missing | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-flight | 1552 | 94,464 (0.945) | 78,131 (0.781) |
| save-burst | 1479 | 94,319 (0.943) | 77,837 (0.778) |
| acmp-notk | 1158 | 98,757 (0.988) | 77,779 (0.778) |
| save-second | 520 | 79,900 (0.799) | 77,850 (0.778) |
| backlog-adp@blank-0 | 341 | 91,745 (0.917) | 75,954 (0.760) |
| backlog-adp@blank-1 | 342 | 92,674 (0.927) | 76,188 (0.762) |
| backlog-adp@blank-2 | 342 | 92,674 (0.927) | 76,188 (0.762) |
| backlog-adp@blank-3 | 342 | 92,674 (0.927) | 76,188 (0.762) |
| backlog-adp@blank-4 | 342 | 92,674 (0.927) | 76,188 (0.762) |
| backlog-adp@blank-5 | 342 | 92,674 (0.927) | 76,188 (0.762) |
| backlog-adp@blank-6 | 342 | 92,674 (0.927) | 76,188 (0.762) |
| backlog-adp@blank-7 | 342 | 92,674 (0.927) | 76,188 (0.762) |
| backlog-adp@program-0 | 371 | 95,200 (0.952) | 77,837 (0.778) |
| backlog-adp@program-1 | 371 | 95,200 (0.952) | 77,837 (0.778) |
| backlog-adp@program-2 | 371 | 95,200 (0.952) | 77,837 (0.778) |
| backlog-adp@program-3 | 372 | 96,670 (0.967) | 78,823 (0.788) |
| backlog-adp@program-4 | 377 | 95,135 (0.951) | 77,837 (0.778) |
| backlog-adp@program-5 | 377 | 95,135 (0.951) | 77,837 (0.778) |
| backlog-adp@program-6 | 377 | 95,135 (0.951) | 77,837 (0.778) |
| backlog-adp@program-7 | 377 | 96,638 (0.966) | 78,823 (0.788) |
| backlog-adp@verify-0 | 397 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@verify-1 | 397 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@verify-2 | 397 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@verify-3 | 397 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@verify-4 | 398 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@verify-5 | 398 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@verify-6 | 398 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@verify-7 | 398 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@blank-aged2-0 | 339 | 93,034 (0.930) | 75,825 (0.758) |
| backlog-adp@blank-aged2-1 | 340 | 92,468 (0.925) | 75,799 (0.758) |
| backlog-adp@blank-aged2-2 | 340 | 92,382 (0.924) | 75,799 (0.758) |
| backlog-adp@blank-aged2-3 | 342 | 93,290 (0.933) | 75,863 (0.759) |
| backlog-adp@blank-aged2-4 | 341 | 93,449 (0.934) | 75,799 (0.758) |
| backlog-adp@blank-aged2-5 | 340 | 92,388 (0.924) | 75,902 (0.759) |
| backlog-adp@blank-aged2-6 | 341 | 92,355 (0.924) | 75,902 (0.759) |
| backlog-adp@blank-aged2-7 | 340 | 91,571 (0.916) | 75,686 (0.757) |
| backlog-adp@blank-aged1-0 | 340 | 99,806 (0.998) | 76,578 (0.766) |
| backlog-adp@blank-aged1-1 | 339 | 92,853 (0.929) | 76,333 (0.763) |
| backlog-adp@blank-aged1-2 | 339 | 92,849 (0.928) | 76,333 (0.763) |
| backlog-adp@blank-aged1-3 | 339 | 92,916 (0.929) | 76,333 (0.763) |
| backlog-adp@blank-aged1-4 | 339 | 92,916 (0.929) | 76,333 (0.763) |
| backlog-adp@blank-aged1-5 | 342 | 97,551 (0.976) | 76,333 (0.763) |
| backlog-adp@blank-aged1-6 | 341 | 93,640 (0.936) | 76,333 (0.763) |
| backlog-adp@blank-aged1-7 | 340 | 93,661 (0.937) | 76,333 (0.763) |
| backlog-adp@program-aged2-0 | 369 | 95,008 (0.950) | 78,497 (0.785) |
| backlog-adp@program-aged2-1 | 369 | 95,202 (0.952) | 78,604 (0.786) |
| backlog-adp@program-aged2-2 | 369 | 95,231 (0.952) | 78,433 (0.784) |
| backlog-adp@program-aged2-3 | 369 | 95,231 (0.952) | 78,668 (0.787) |
| backlog-adp@program-aged2-4 | 369 | 95,269 (0.953) | 78,604 (0.786) |
| backlog-adp@program-aged2-5 | 369 | 95,269 (0.953) | 78,670 (0.787) |
| backlog-adp@program-aged2-6 | 373 | 95,268 (0.953) | 78,046 (0.780) |
| backlog-adp@program-aged2-7 | 371 | 101,602 (1.016) | 77,965 (0.780) |
| backlog-adp@program-aged1-0 | 368 | 96,405 (0.964) | 78,825 (0.788) |
| backlog-adp@program-aged1-1 | 368 | 96,429 (0.964) | 78,823 (0.788) |
| backlog-adp@program-aged1-2 | 369 | 96,607 (0.966) | 78,823 (0.788) |
| backlog-adp@program-aged1-3 | 368 | 96,533 (0.965) | 78,823 (0.788) |
| backlog-adp@program-aged1-4 | 368 | 96,459 (0.965) | 78,823 (0.788) |
| backlog-adp@program-aged1-5 | 368 | 96,459 (0.965) | 78,823 (0.788) |
| backlog-adp@program-aged1-6 | 368 | 96,396 (0.964) | 78,823 (0.788) |
| backlog-adp@program-aged1-7 | 370 | 96,838 (0.968) | 78,823 (0.788) |
| backlog-adp@verify-aged2-0 | 397 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@verify-aged2-1 | 398 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@verify-aged2-2 | 399 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@verify-aged2-3 | 398 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@verify-aged2-4 | 398 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@verify-aged2-5 | 398 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@verify-aged2-6 | 399 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@verify-aged2-7 | 398 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@verify-aged1-0 | 397 | 95,092 (0.951) | 77,867 (0.779) |
| backlog-adp@verify-aged1-1 | 397 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@verify-aged1-2 | 397 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@verify-aged1-3 | 397 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@verify-aged1-4 | 399 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@verify-aged1-5 | 397 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@verify-aged1-6 | 399 | 94,789 (0.948) | 77,867 (0.779) |
| backlog-adp@verify-aged1-7 | 398 | 94,789 (0.948) | 77,867 (0.779) |
| adp-advertise | 577 | 22,325 (0.223) | 2,328 (0.023) |
| save-held | 815 | 94,464 (0.945) | 78,052 (0.781) |
| save-starved | 418 | 80,886 (0.809) | 78,414 (0.784) |
| acmp-noresp | 708 | 96,748 (0.967) | 77,940 (0.779) |
| save | 679 | 94,319 (0.943) | 77,902 (0.779) |
| srp | 271 | 22,237 (0.222) | 2,328 (0.023) |
| backlog | 265 | 22,237 (0.222) | 2,328 (0.023) |
| backlog-adp | 271 | 22,237 (0.222) | 2,419 (0.024) |
| backlog-adp-refill | 274 | 22,237 (0.222) | 2,534 (0.025) |
| backlog-owed | 276 | 22,237 (0.222) | 2,506 (0.025) |
| acmp-disc | 398 | 98,431 (0.984) | 77,940 (0.779) |
| maap | 169 | 22,232 (0.222) | 2,328 (0.023) |
| adp-link | 79 | 22,232 (0.222) | 2,328 (0.023) |
| adp-gm | 79 | 22,232 (0.222) | 2,328 (0.023) |
| adp-discover | 79 | 22,232 (0.222) | 2,328 (0.023) |
| control | 79 | 22,232 (0.222) | 2,328 (0.023) |
| aecp-fanout | 80 | 23,447 (0.234) | 4,305 (0.043) |
| acmp-cmd | 65 | 22,232 (0.222) | 2,328 (0.023) |
| aecp | 79 | 22,232 (0.222) | 2,333 (0.023) |
| aecp-largest-notice | 78 | 22,232 (0.222) | 2,328 (0.023) |
| datapath-events | 69 | 22,232 (0.222) | 2,328 (0.023) |
| fixture | 54 | 18,149 (0.181) | 2,348 (0.023) |

Longest pass that carries a step: 101,602 CPU cycles (1.016 ms), backlog-adp@program-aged2-7; longest step: 78,825 (0.788 ms), backlog-adp@program-aged1-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 155,716 | 1.557 | 20 | 200 | fits | 156,656 | 250 | 0.467 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 222,105 | 2.221 | 20 | 20 | fits | 86,526 | 82 | 0.667 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 290,316 | 2.903 | 20 | 24 | fits | 64,228 | 44 | 0.500 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 250,535 | 2.505 | 20 | 50 | fits | 112,991 | 211 | 0.323 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 936,401 | 9.364 | 20 | 20 | fits | 33,993 | 12 | 0.827 |
| an MRPDU its join timer owes, the longest | `save-flight.mrpdu.join.if0` | 55,477 | 0.555 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-flight.mrpdu.leaveall.if0` | 56,448 | 0.564 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 220,201 | 2.202 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-burst.held.adp.if0` | 155,847 | 1.558 | 20 | 200 | fits | 156,656 | 250 | 0.467 |
| ACMP record, every channel at its refill rate, the longest | `save-burst.held.acmp.if0` | 235,192 | 2.352 | 20 | 20 | fits | 99,613 | 91 | 0.684 |
| AECP record, every channel at its refill rate, the longest | `save-burst.held.aecp.if0` | 171,984 | 1.720 | 20 | 24 | fits | 88,253 | 30 | 0.795 |
| MAAP record, every channel at its refill rate, the longest | `save-burst.held.maap.if0` | 195,717 | 1.957 | 20 | 50 | fits | 99,613 | 91 | 0.684 |
| SRP record, every channel at its refill rate, the longest | `save-burst.held.srp.if0` | 871,463 | 8.715 | 20 | 20 | fits | 81,813 | 32 | 0.736 |
| an MRPDU its join timer owes, the longest | `save-burst.mrpdu.join.if0` | 57,748 | 0.577 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-burst.mrpdu.periodic.if0` | 245,974 | 2.460 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 14,177 | 0.142 | 20 | 20 | fits | 35,658 | 19 (14) | 0.895 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 390,336 | 3.903 | 20 | 20 | fits | 130,708 | 224 | 0.387 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 310,128 | 3.101 | 20 | 200 | fits | 151,590 | 185 | 0.472 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 440,220 | 4.402 | 20 | 200 | fits | 130,708 | 224 | 0.387 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 311,052 | 3.111 | 20 | 20 | fits | 151,590 | 185 | 0.472 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 440,924 | 4.409 | 20 | 20 | fits | 130,708 | 224 | 0.387 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 154,215 | 1.542 | 20 | 24 | fits | 150,635 | 146 | 0.435 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 313,702 | 3.137 | 20 | 24 | fits | 151,590 | 185 | 0.472 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 313,636 | 3.136 | 20 | 50 | fits | 151,590 | 185 | 0.472 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 443,948 | 4.439 | 20 | 50 | fits | 130,708 | 224 | 0.387 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 531,168 | 5.312 | 20 | 20 | fits | 87,286 | 24 | 0.791 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,037,153 | 10.372 | 20 | 20 | fits | 66,607 | 27 | 0.763 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 469,457 | 4.695 | 20 | 20 | fits | 131,089 | 227 | 0.378 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 387,393 | 3.874 | 20 | 200 | fits | 150,302 | 181 | 0.477 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 517,866 | 5.179 | 20 | 200 | fits | 131,089 | 227 | 0.378 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 388,317 | 3.883 | 20 | 20 | fits | 150,302 | 181 | 0.477 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 518,570 | 5.186 | 20 | 20 | fits | 131,089 | 227 | 0.378 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 232,768 | 2.328 | 20 | 24 | fits | 150,636 | 146 | 0.436 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 390,967 | 3.910 | 20 | 24 | fits | 150,302 | 181 | 0.477 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 390,901 | 3.909 | 20 | 50 | fits | 150,302 | 181 | 0.477 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 521,594 | 5.216 | 20 | 50 | fits | 131,089 | 227 | 0.378 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 608,822 | 6.088 | 20 | 20 | fits | 87,294 | 24 | 0.791 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 1,119,189 | 11.192 | 20 | 20 | fits | 70,989 | 33 | 0.758 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 456,957 | 4.570 | 20 | 20 | fits | 131,089 | 227 | 0.378 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 374,893 | 3.749 | 20 | 200 | fits | 150,302 | 181 | 0.477 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 505,366 | 5.054 | 20 | 200 | fits | 131,089 | 227 | 0.378 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 375,817 | 3.758 | 20 | 20 | fits | 150,302 | 181 | 0.477 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 506,070 | 5.061 | 20 | 20 | fits | 131,089 | 227 | 0.378 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 220,268 | 2.203 | 20 | 24 | fits | 150,636 | 146 | 0.436 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 378,467 | 3.785 | 20 | 24 | fits | 150,302 | 181 | 0.477 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 378,401 | 3.784 | 20 | 50 | fits | 150,302 | 181 | 0.477 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 509,094 | 5.091 | 20 | 50 | fits | 131,089 | 227 | 0.378 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 596,322 | 5.963 | 20 | 20 | fits | 87,294 | 24 | 0.791 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 1,106,689 | 11.067 | 20 | 20 | fits | 70,989 | 33 | 0.758 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 381,576 | 3.816 | 20 | 20 | fits | 124,776 | 205 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 305,796 | 3.058 | 20 | 200 | fits | 148,955 | 204 | 0.445 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 429,956 | 4.300 | 20 | 200 | fits | 124,776 | 205 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 306,720 | 3.067 | 20 | 20 | fits | 148,955 | 204 | 0.445 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 430,660 | 4.307 | 20 | 20 | fits | 124,776 | 205 | 0.384 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 152,478 | 1.525 | 20 | 24 | fits | 154,259 | 146 | 0.443 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 309,370 | 3.094 | 20 | 24 | fits | 148,955 | 204 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 309,304 | 3.093 | 20 | 50 | fits | 148,955 | 204 | 0.445 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 433,684 | 4.337 | 20 | 50 | fits | 124,776 | 205 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 520,957 | 5.210 | 20 | 20 | fits | 87,339 | 24 | 0.791 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 1,031,324 | 10.313 | 20 | 20 | fits | 70,989 | 33 | 0.758 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 381,576 | 3.816 | 20 | 20 | fits | 124,776 | 205 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 305,796 | 3.058 | 20 | 200 | fits | 148,955 | 204 | 0.445 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 429,956 | 4.300 | 20 | 200 | fits | 124,776 | 205 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 306,720 | 3.067 | 20 | 20 | fits | 148,955 | 204 | 0.445 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 430,660 | 4.307 | 20 | 20 | fits | 124,776 | 205 | 0.384 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 152,478 | 1.525 | 20 | 24 | fits | 154,259 | 146 | 0.443 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 309,370 | 3.094 | 20 | 24 | fits | 148,955 | 204 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 309,304 | 3.093 | 20 | 50 | fits | 148,955 | 204 | 0.445 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 433,684 | 4.337 | 20 | 50 | fits | 124,776 | 205 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 520,957 | 5.210 | 20 | 20 | fits | 87,339 | 24 | 0.791 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 1,031,324 | 10.313 | 20 | 20 | fits | 70,989 | 33 | 0.758 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 381,576 | 3.816 | 20 | 20 | fits | 124,776 | 205 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 305,796 | 3.058 | 20 | 200 | fits | 148,955 | 204 | 0.445 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 429,956 | 4.300 | 20 | 200 | fits | 124,776 | 205 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 306,720 | 3.067 | 20 | 20 | fits | 148,955 | 204 | 0.445 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 430,660 | 4.307 | 20 | 20 | fits | 124,776 | 205 | 0.384 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 152,478 | 1.525 | 20 | 24 | fits | 154,259 | 146 | 0.443 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 309,370 | 3.094 | 20 | 24 | fits | 148,955 | 204 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 309,304 | 3.093 | 20 | 50 | fits | 148,955 | 204 | 0.445 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 433,684 | 4.337 | 20 | 50 | fits | 124,776 | 205 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 520,957 | 5.210 | 20 | 20 | fits | 87,339 | 24 | 0.791 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 1,031,324 | 10.313 | 20 | 20 | fits | 70,989 | 33 | 0.758 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 381,576 | 3.816 | 20 | 20 | fits | 124,776 | 205 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 305,796 | 3.058 | 20 | 200 | fits | 148,955 | 204 | 0.445 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 429,956 | 4.300 | 20 | 200 | fits | 124,776 | 205 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 306,720 | 3.067 | 20 | 20 | fits | 148,955 | 204 | 0.445 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 430,660 | 4.307 | 20 | 20 | fits | 124,776 | 205 | 0.384 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 152,478 | 1.525 | 20 | 24 | fits | 154,259 | 146 | 0.443 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 309,370 | 3.094 | 20 | 24 | fits | 148,955 | 204 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 309,304 | 3.093 | 20 | 50 | fits | 148,955 | 204 | 0.445 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 433,684 | 4.337 | 20 | 50 | fits | 124,776 | 205 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 520,957 | 5.210 | 20 | 20 | fits | 87,339 | 24 | 0.791 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 1,031,324 | 10.313 | 20 | 20 | fits | 70,989 | 33 | 0.758 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 381,576 | 3.816 | 20 | 20 | fits | 124,776 | 205 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 305,796 | 3.058 | 20 | 200 | fits | 148,955 | 204 | 0.445 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 429,956 | 4.300 | 20 | 200 | fits | 124,776 | 205 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 306,720 | 3.067 | 20 | 20 | fits | 148,955 | 204 | 0.445 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 430,660 | 4.307 | 20 | 20 | fits | 124,776 | 205 | 0.384 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 152,478 | 1.525 | 20 | 24 | fits | 154,259 | 146 | 0.443 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 309,370 | 3.094 | 20 | 24 | fits | 148,955 | 204 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 309,304 | 3.093 | 20 | 50 | fits | 148,955 | 204 | 0.445 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 433,684 | 4.337 | 20 | 50 | fits | 124,776 | 205 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 520,957 | 5.210 | 20 | 20 | fits | 87,339 | 24 | 0.791 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 1,031,324 | 10.313 | 20 | 20 | fits | 70,989 | 33 | 0.758 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 422,965 | 4.230 | 20 | 20 | fits | 129,137 | 202 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 350,153 | 3.502 | 20 | 200 | fits | 148,464 | 203 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 478,674 | 4.787 | 20 | 200 | fits | 129,137 | 202 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 351,077 | 3.511 | 20 | 20 | fits | 148,464 | 203 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 479,378 | 4.794 | 20 | 20 | fits | 129,137 | 202 | 0.409 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 206,253 | 2.063 | 20 | 24 | fits | 150,387 | 145 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 353,727 | 3.537 | 20 | 24 | fits | 148,464 | 203 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 353,661 | 3.537 | 20 | 50 | fits | 148,464 | 203 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 482,402 | 4.824 | 20 | 50 | fits | 129,137 | 202 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 569,952 | 5.700 | 20 | 20 | fits | 87,616 | 24 | 0.794 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 1,075,979 | 10.760 | 20 | 20 | fits | 73,457 | 24 | 0.653 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 397,965 | 3.980 | 20 | 20 | fits | 129,137 | 202 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 325,153 | 3.252 | 20 | 200 | fits | 148,464 | 203 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 453,674 | 4.537 | 20 | 200 | fits | 129,137 | 202 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 326,077 | 3.261 | 20 | 20 | fits | 148,464 | 203 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 454,378 | 4.544 | 20 | 20 | fits | 129,137 | 202 | 0.409 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 181,253 | 1.813 | 20 | 24 | fits | 150,387 | 145 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 328,727 | 3.287 | 20 | 24 | fits | 148,464 | 203 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 328,661 | 3.287 | 20 | 50 | fits | 148,464 | 203 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 457,402 | 4.574 | 20 | 50 | fits | 129,137 | 202 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 544,952 | 5.450 | 20 | 20 | fits | 87,616 | 24 | 0.794 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 1,050,979 | 10.510 | 20 | 20 | fits | 73,457 | 24 | 0.653 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 372,965 | 3.730 | 20 | 20 | fits | 129,137 | 202 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 300,153 | 3.002 | 20 | 200 | fits | 148,464 | 203 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 428,674 | 4.287 | 20 | 200 | fits | 129,137 | 202 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 301,077 | 3.011 | 20 | 20 | fits | 148,464 | 203 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 429,378 | 4.294 | 20 | 20 | fits | 129,137 | 202 | 0.409 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 156,253 | 1.563 | 20 | 24 | fits | 150,387 | 145 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 303,727 | 3.037 | 20 | 24 | fits | 148,464 | 203 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 303,661 | 3.037 | 20 | 50 | fits | 148,464 | 203 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 432,402 | 4.324 | 20 | 50 | fits | 129,137 | 202 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 519,952 | 5.200 | 20 | 20 | fits | 87,616 | 24 | 0.794 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 1,025,979 | 10.260 | 20 | 20 | fits | 73,457 | 24 | 0.653 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 367,857 | 3.679 | 20 | 20 | fits | 129,952 | 202 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 295,330 | 2.953 | 20 | 200 | fits | 148,357 | 203 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 424,666 | 4.247 | 20 | 200 | fits | 129,952 | 202 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 296,254 | 2.963 | 20 | 20 | fits | 148,357 | 203 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 425,370 | 4.254 | 20 | 20 | fits | 129,952 | 202 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 151,537 | 1.515 | 20 | 24 | fits | 150,145 | 145 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 298,904 | 2.989 | 20 | 24 | fits | 148,357 | 203 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 298,838 | 2.988 | 20 | 50 | fits | 148,357 | 203 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 428,394 | 4.284 | 20 | 50 | fits | 129,952 | 202 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 515,955 | 5.160 | 20 | 20 | fits | 87,627 | 24 | 0.794 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 1,021,982 | 10.220 | 20 | 20 | fits | 73,457 | 24 | 0.653 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 431,229 | 4.312 | 20 | 20 | fits | 128,498 | 218 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 366,529 | 3.665 | 20 | 200 | fits | 149,734 | 185 | 0.465 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 494,411 | 4.944 | 20 | 200 | fits | 128,498 | 218 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 367,453 | 3.675 | 20 | 20 | fits | 149,734 | 185 | 0.465 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 495,115 | 4.951 | 20 | 20 | fits | 128,498 | 218 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 221,359 | 2.214 | 20 | 24 | fits | 150,466 | 145 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 370,103 | 3.701 | 20 | 24 | fits | 149,734 | 185 | 0.465 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 370,037 | 3.700 | 20 | 50 | fits | 149,734 | 185 | 0.465 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 498,139 | 4.981 | 20 | 50 | fits | 128,498 | 218 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 585,724 | 5.857 | 20 | 20 | fits | 87,651 | 25 | 0.792 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 1,091,068 | 10.911 | 20 | 20 | fits | 73,376 | 24 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 406,229 | 4.062 | 20 | 20 | fits | 128,498 | 218 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 341,529 | 3.415 | 20 | 200 | fits | 149,734 | 185 | 0.465 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 469,411 | 4.694 | 20 | 200 | fits | 128,498 | 218 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 342,453 | 3.425 | 20 | 20 | fits | 149,734 | 185 | 0.465 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 470,115 | 4.701 | 20 | 20 | fits | 128,498 | 218 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 196,359 | 1.964 | 20 | 24 | fits | 150,466 | 145 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 345,103 | 3.451 | 20 | 24 | fits | 149,734 | 185 | 0.465 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 345,037 | 3.450 | 20 | 50 | fits | 149,734 | 185 | 0.465 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 473,139 | 4.731 | 20 | 50 | fits | 128,498 | 218 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 560,724 | 5.607 | 20 | 20 | fits | 87,651 | 25 | 0.792 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 1,066,068 | 10.661 | 20 | 20 | fits | 73,376 | 24 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 381,229 | 3.812 | 20 | 20 | fits | 128,498 | 218 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 316,529 | 3.165 | 20 | 200 | fits | 149,734 | 185 | 0.465 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 444,411 | 4.444 | 20 | 200 | fits | 128,498 | 218 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 317,453 | 3.175 | 20 | 20 | fits | 149,734 | 185 | 0.465 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 445,115 | 4.451 | 20 | 20 | fits | 128,498 | 218 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 171,359 | 1.714 | 20 | 24 | fits | 150,466 | 145 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 320,103 | 3.201 | 20 | 24 | fits | 149,734 | 185 | 0.465 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 320,037 | 3.200 | 20 | 50 | fits | 149,734 | 185 | 0.465 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 448,139 | 4.481 | 20 | 50 | fits | 128,498 | 218 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 535,724 | 5.357 | 20 | 20 | fits | 87,651 | 25 | 0.792 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 1,041,068 | 10.411 | 20 | 20 | fits | 73,376 | 24 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 389,111 | 3.891 | 20 | 20 | fits | 127,820 | 219 | 0.374 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 311,599 | 3.116 | 20 | 200 | fits | 149,672 | 185 | 0.464 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 438,803 | 4.388 | 20 | 200 | fits | 127,820 | 219 | 0.374 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 312,523 | 3.125 | 20 | 20 | fits | 149,672 | 185 | 0.464 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 439,507 | 4.395 | 20 | 20 | fits | 127,820 | 219 | 0.374 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 166,491 | 1.665 | 20 | 24 | fits | 150,072 | 145 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 315,173 | 3.152 | 20 | 24 | fits | 149,672 | 185 | 0.464 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 315,107 | 3.151 | 20 | 50 | fits | 149,672 | 185 | 0.464 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 442,531 | 4.425 | 20 | 50 | fits | 127,820 | 219 | 0.374 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 542,859 | 5.429 | 20 | 20 | fits | 90,712 | 31 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 1,032,823 | 10.328 | 20 | 20 | fits | 60,451 | 20 | 0.701 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 403,776 | 4.038 | 20 | 20 | fits | 120,462 | 196 | 0.370 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 339,334 | 3.393 | 20 | 200 | fits | 148,436 | 203 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 459,180 | 4.592 | 20 | 200 | fits | 120,462 | 196 | 0.370 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 340,258 | 3.403 | 20 | 20 | fits | 148,436 | 203 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 459,884 | 4.599 | 20 | 20 | fits | 120,462 | 196 | 0.370 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 195,462 | 1.955 | 20 | 24 | fits | 150,240 | 145 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 342,908 | 3.429 | 20 | 24 | fits | 148,436 | 203 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 342,842 | 3.428 | 20 | 50 | fits | 148,436 | 203 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 462,908 | 4.629 | 20 | 50 | fits | 120,462 | 196 | 0.370 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 550,483 | 5.505 | 20 | 20 | fits | 87,641 | 24 | 0.794 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,062,836 | 10.628 | 20 | 20 | fits | 86,006 | 28 | 0.612 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 391,276 | 3.913 | 20 | 20 | fits | 120,462 | 196 | 0.370 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 326,834 | 3.268 | 20 | 200 | fits | 148,436 | 203 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 446,680 | 4.467 | 20 | 200 | fits | 120,462 | 196 | 0.370 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 327,758 | 3.278 | 20 | 20 | fits | 148,436 | 203 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 447,384 | 4.474 | 20 | 20 | fits | 120,462 | 196 | 0.370 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 182,962 | 1.830 | 20 | 24 | fits | 150,240 | 145 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 330,408 | 3.304 | 20 | 24 | fits | 148,436 | 203 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 330,342 | 3.303 | 20 | 50 | fits | 148,436 | 203 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 450,408 | 4.504 | 20 | 50 | fits | 120,462 | 196 | 0.370 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 537,983 | 5.380 | 20 | 20 | fits | 87,641 | 24 | 0.794 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 1,050,336 | 10.503 | 20 | 20 | fits | 86,006 | 28 | 0.612 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 378,776 | 3.788 | 20 | 20 | fits | 120,462 | 196 | 0.370 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 314,334 | 3.143 | 20 | 200 | fits | 148,436 | 203 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 434,180 | 4.342 | 20 | 200 | fits | 120,462 | 196 | 0.370 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 315,258 | 3.153 | 20 | 20 | fits | 148,436 | 203 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 434,884 | 4.349 | 20 | 20 | fits | 120,462 | 196 | 0.370 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 170,462 | 1.705 | 20 | 24 | fits | 150,240 | 145 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 317,908 | 3.179 | 20 | 24 | fits | 148,436 | 203 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 317,842 | 3.178 | 20 | 50 | fits | 148,436 | 203 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 437,908 | 4.379 | 20 | 50 | fits | 120,462 | 196 | 0.370 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 525,483 | 5.255 | 20 | 20 | fits | 87,641 | 24 | 0.794 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 1,037,836 | 10.378 | 20 | 20 | fits | 86,006 | 28 | 0.612 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 366,276 | 3.663 | 20 | 20 | fits | 120,462 | 196 | 0.370 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 301,834 | 3.018 | 20 | 200 | fits | 148,436 | 203 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 421,680 | 4.217 | 20 | 200 | fits | 120,462 | 196 | 0.370 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 302,758 | 3.028 | 20 | 20 | fits | 148,436 | 203 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 422,384 | 4.224 | 20 | 20 | fits | 120,462 | 196 | 0.370 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 157,962 | 1.580 | 20 | 24 | fits | 150,240 | 145 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 305,408 | 3.054 | 20 | 24 | fits | 148,436 | 203 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 305,342 | 3.053 | 20 | 50 | fits | 148,436 | 203 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 425,408 | 4.254 | 20 | 50 | fits | 120,462 | 196 | 0.370 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 512,983 | 5.130 | 20 | 20 | fits | 87,641 | 24 | 0.794 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 1,025,336 | 10.253 | 20 | 20 | fits | 86,006 | 28 | 0.612 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 444,907 | 4.449 | 20 | 20 | fits | 121,159 | 196 | 0.377 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 380,530 | 3.805 | 20 | 200 | fits | 148,382 | 203 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 501,073 | 5.011 | 20 | 200 | fits | 121,159 | 196 | 0.377 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 381,454 | 3.815 | 20 | 20 | fits | 148,382 | 203 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 501,777 | 5.018 | 20 | 20 | fits | 121,159 | 196 | 0.377 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 236,712 | 2.367 | 20 | 24 | fits | 150,167 | 145 | 0.429 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 384,104 | 3.841 | 20 | 24 | fits | 148,382 | 203 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 384,038 | 3.840 | 20 | 50 | fits | 148,382 | 203 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 504,801 | 5.048 | 20 | 50 | fits | 121,159 | 196 | 0.377 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 592,517 | 5.925 | 20 | 20 | fits | 87,782 | 25 | 0.793 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 1,104,636 | 11.046 | 20 | 20 | fits | 85,925 | 28 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 432,407 | 4.324 | 20 | 20 | fits | 121,159 | 196 | 0.377 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 368,030 | 3.680 | 20 | 200 | fits | 148,382 | 203 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 488,573 | 4.886 | 20 | 200 | fits | 121,159 | 196 | 0.377 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 368,954 | 3.690 | 20 | 20 | fits | 148,382 | 203 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 489,277 | 4.893 | 20 | 20 | fits | 121,159 | 196 | 0.377 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 224,212 | 2.242 | 20 | 24 | fits | 150,167 | 145 | 0.429 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 371,604 | 3.716 | 20 | 24 | fits | 148,382 | 203 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 371,538 | 3.715 | 20 | 50 | fits | 148,382 | 203 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 492,301 | 4.923 | 20 | 50 | fits | 121,159 | 196 | 0.377 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 580,017 | 5.800 | 20 | 20 | fits | 87,782 | 25 | 0.793 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 1,092,136 | 10.921 | 20 | 20 | fits | 85,925 | 28 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 419,907 | 4.199 | 20 | 20 | fits | 121,159 | 196 | 0.377 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 355,530 | 3.555 | 20 | 200 | fits | 148,382 | 203 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 476,073 | 4.761 | 20 | 200 | fits | 121,159 | 196 | 0.377 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 356,454 | 3.565 | 20 | 20 | fits | 148,382 | 203 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 476,777 | 4.768 | 20 | 20 | fits | 121,159 | 196 | 0.377 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 211,712 | 2.117 | 20 | 24 | fits | 150,167 | 145 | 0.429 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 359,104 | 3.591 | 20 | 24 | fits | 148,382 | 203 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 359,038 | 3.590 | 20 | 50 | fits | 148,382 | 203 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 479,801 | 4.798 | 20 | 50 | fits | 121,159 | 196 | 0.377 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 567,517 | 5.675 | 20 | 20 | fits | 87,782 | 25 | 0.793 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 1,079,636 | 10.796 | 20 | 20 | fits | 85,925 | 28 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 407,407 | 4.074 | 20 | 20 | fits | 121,159 | 196 | 0.377 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 343,030 | 3.430 | 20 | 200 | fits | 148,382 | 203 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 463,573 | 4.636 | 20 | 200 | fits | 121,159 | 196 | 0.377 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 343,954 | 3.440 | 20 | 20 | fits | 148,382 | 203 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 464,277 | 4.643 | 20 | 20 | fits | 121,159 | 196 | 0.377 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 199,212 | 1.992 | 20 | 24 | fits | 150,167 | 145 | 0.429 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 346,604 | 3.466 | 20 | 24 | fits | 148,382 | 203 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 346,538 | 3.465 | 20 | 50 | fits | 148,382 | 203 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 467,301 | 4.673 | 20 | 50 | fits | 121,159 | 196 | 0.377 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 555,017 | 5.550 | 20 | 20 | fits | 87,782 | 25 | 0.793 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 1,067,136 | 10.671 | 20 | 20 | fits | 85,925 | 28 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 368,552 | 3.686 | 20 | 20 | fits | 124,633 | 202 | 0.395 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 301,305 | 3.013 | 20 | 200 | fits | 150,115 | 208 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 425,322 | 4.253 | 20 | 200 | fits | 124,633 | 202 | 0.395 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 302,229 | 3.022 | 20 | 20 | fits | 150,115 | 208 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 426,026 | 4.260 | 20 | 20 | fits | 124,633 | 202 | 0.395 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 147,215 | 1.472 | 20 | 24 | fits | 149,324 | 143 | 0.426 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 304,879 | 3.049 | 20 | 24 | fits | 150,115 | 208 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 304,813 | 3.048 | 20 | 50 | fits | 150,115 | 208 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 429,050 | 4.290 | 20 | 50 | fits | 124,633 | 202 | 0.395 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 516,347 | 5.163 | 20 | 20 | fits | 87,363 | 24 | 0.793 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 1,026,818 | 10.268 | 20 | 20 | fits | 71,060 | 33 | 0.759 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 374,189 | 3.742 | 20 | 20 | fits | 121,261 | 199 | 0.363 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 301,564 | 3.016 | 20 | 200 | fits | 146,659 | 199 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 422,209 | 4.222 | 20 | 200 | fits | 121,261 | 199 | 0.363 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 302,488 | 3.025 | 20 | 20 | fits | 146,659 | 199 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 422,913 | 4.229 | 20 | 20 | fits | 121,261 | 199 | 0.363 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 159,469 | 1.595 | 20 | 24 | fits | 149,040 | 142 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 305,138 | 3.051 | 20 | 24 | fits | 146,659 | 199 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 305,072 | 3.051 | 20 | 50 | fits | 146,659 | 199 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 425,937 | 4.259 | 20 | 50 | fits | 121,261 | 199 | 0.363 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 513,641 | 5.136 | 20 | 20 | fits | 87,770 | 24 | 0.796 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 1,103,040 | 11.030 | 20 | 20 | fits | 86,389 | 29 | 0.625 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 362,609 | 3.626 | 20 | 20 | fits | 121,175 | 196 | 0.378 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 298,216 | 2.982 | 20 | 200 | fits | 147,748 | 203 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 418,775 | 4.188 | 20 | 200 | fits | 121,175 | 196 | 0.378 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 299,140 | 2.991 | 20 | 20 | fits | 147,748 | 203 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 419,479 | 4.195 | 20 | 20 | fits | 121,175 | 196 | 0.378 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 155,032 | 1.550 | 20 | 24 | fits | 149,202 | 142 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 301,790 | 3.018 | 20 | 24 | fits | 147,748 | 203 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 301,724 | 3.017 | 20 | 50 | fits | 147,748 | 203 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 422,503 | 4.225 | 20 | 50 | fits | 121,175 | 196 | 0.378 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 510,118 | 5.101 | 20 | 20 | fits | 87,681 | 24 | 0.795 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,099,434 | 10.994 | 20 | 20 | fits | 85,925 | 28 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 365,239 | 3.652 | 20 | 20 | fits | 120,917 | 196 | 0.374 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 294,026 | 2.940 | 20 | 200 | fits | 148,223 | 203 | 0.438 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 414,327 | 4.143 | 20 | 200 | fits | 120,917 | 196 | 0.374 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 294,950 | 2.950 | 20 | 20 | fits | 148,223 | 203 | 0.438 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 415,031 | 4.150 | 20 | 20 | fits | 120,917 | 196 | 0.374 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 150,367 | 1.504 | 20 | 24 | fits | 149,040 | 142 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 297,600 | 2.976 | 20 | 24 | fits | 148,223 | 203 | 0.438 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 297,534 | 2.975 | 20 | 50 | fits | 148,223 | 203 | 0.438 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 418,055 | 4.181 | 20 | 50 | fits | 120,917 | 196 | 0.374 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 505,854 | 5.059 | 20 | 20 | fits | 87,865 | 25 | 0.794 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,095,499 | 10.955 | 20 | 20 | fits | 86,006 | 28 | 0.612 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 354,989 | 3.550 | 20 | 20 | fits | 120,649 | 197 | 0.371 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 290,528 | 2.905 | 20 | 200 | fits | 149,162 | 208 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 410,561 | 4.106 | 20 | 200 | fits | 120,649 | 197 | 0.371 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 291,452 | 2.915 | 20 | 20 | fits | 149,162 | 208 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 411,265 | 4.113 | 20 | 20 | fits | 120,649 | 197 | 0.371 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 145,930 | 1.459 | 20 | 24 | fits | 149,202 | 142 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 294,102 | 2.941 | 20 | 24 | fits | 149,162 | 208 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 294,036 | 2.940 | 20 | 50 | fits | 149,162 | 208 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 414,289 | 4.143 | 20 | 50 | fits | 120,649 | 197 | 0.371 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 514,405 | 5.144 | 20 | 20 | fits | 90,762 | 31 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,088,079 | 10.881 | 20 | 20 | fits | 73,487 | 24 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 394,016 | 3.940 | 20 | 20 | fits | 133,260 | 209 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 302,344 | 3.023 | 20 | 200 | fits | 148,322 | 204 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 443,892 | 4.439 | 20 | 200 | fits | 133,260 | 209 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 303,268 | 3.033 | 20 | 20 | fits | 148,322 | 204 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 444,596 | 4.446 | 20 | 20 | fits | 133,260 | 209 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 158,586 | 1.586 | 20 | 24 | fits | 149,202 | 142 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 305,918 | 3.059 | 20 | 24 | fits | 148,322 | 204 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 305,852 | 3.059 | 20 | 50 | fits | 148,322 | 204 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 447,620 | 4.476 | 20 | 50 | fits | 133,260 | 209 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 611,311 | 6.113 | 20 | 20 | fits | 86,817 | 25 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,117,376 | 11.174 | 20 | 20 | fits | 66,739 | 27 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 380,849 | 3.808 | 20 | 20 | fits | 129,253 | 202 | 0.410 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 307,921 | 3.079 | 20 | 200 | fits | 150,128 | 208 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 436,558 | 4.366 | 20 | 200 | fits | 129,253 | 202 | 0.410 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 308,845 | 3.088 | 20 | 20 | fits | 150,128 | 208 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 437,262 | 4.373 | 20 | 20 | fits | 129,253 | 202 | 0.410 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 154,045 | 1.540 | 20 | 24 | fits | 149,164 | 143 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 311,495 | 3.115 | 20 | 24 | fits | 150,128 | 208 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 311,429 | 3.114 | 20 | 50 | fits | 150,128 | 208 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 440,286 | 4.403 | 20 | 50 | fits | 129,253 | 202 | 0.410 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 604,171 | 6.042 | 20 | 20 | fits | 87,093 | 25 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,109,964 | 11.100 | 20 | 20 | fits | 73,508 | 24 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 363,516 | 3.635 | 20 | 20 | fits | 131,560 | 208 | 0.416 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 289,228 | 2.892 | 20 | 200 | fits | 149,282 | 208 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 420,172 | 4.202 | 20 | 200 | fits | 131,560 | 208 | 0.416 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 290,152 | 2.902 | 20 | 20 | fits | 149,282 | 208 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 420,876 | 4.209 | 20 | 20 | fits | 131,560 | 208 | 0.416 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 144,510 | 1.445 | 20 | 24 | fits | 150,780 | 147 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 292,802 | 2.928 | 20 | 24 | fits | 149,282 | 208 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 292,736 | 2.927 | 20 | 50 | fits | 149,282 | 208 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 423,900 | 4.239 | 20 | 50 | fits | 131,560 | 208 | 0.416 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 587,713 | 5.877 | 20 | 20 | fits | 86,956 | 25 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,094,867 | 10.949 | 20 | 20 | fits | 73,390 | 24 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 382,431 | 3.824 | 20 | 20 | fits | 126,130 | 203 | 0.407 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 304,839 | 3.048 | 20 | 200 | fits | 147,986 | 204 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 439,455 | 4.395 | 20 | 200 | fits | 126,130 | 203 | 0.407 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 305,763 | 3.058 | 20 | 20 | fits | 147,986 | 204 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 440,159 | 4.402 | 20 | 20 | fits | 126,130 | 203 | 0.407 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 161,417 | 1.614 | 20 | 24 | fits | 149,089 | 142 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 308,413 | 3.084 | 20 | 24 | fits | 147,986 | 204 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 308,347 | 3.083 | 20 | 50 | fits | 147,986 | 204 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 443,183 | 4.432 | 20 | 50 | fits | 126,130 | 203 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 530,263 | 5.303 | 20 | 20 | fits | 87,146 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 1,027,137 | 10.271 | 20 | 20 | fits | 67,688 | 26 | 0.758 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 382,600 | 3.826 | 20 | 20 | fits | 120,870 | 196 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 311,434 | 3.114 | 20 | 200 | fits | 150,290 | 208 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 431,688 | 4.317 | 20 | 200 | fits | 120,870 | 196 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 312,358 | 3.124 | 20 | 20 | fits | 150,290 | 208 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 432,392 | 4.324 | 20 | 20 | fits | 120,870 | 196 | 0.372 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 157,265 | 1.573 | 20 | 24 | fits | 149,140 | 143 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 315,008 | 3.150 | 20 | 24 | fits | 150,290 | 208 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 314,942 | 3.149 | 20 | 50 | fits | 150,290 | 208 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 435,416 | 4.354 | 20 | 50 | fits | 120,870 | 196 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 522,880 | 5.229 | 20 | 20 | fits | 87,530 | 24 | 0.794 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 1,034,745 | 10.347 | 20 | 20 | fits | 78,585 | 31 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 372,191 | 3.722 | 20 | 20 | fits | 120,476 | 196 | 0.371 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 307,735 | 3.077 | 20 | 200 | fits | 148,225 | 203 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 427,595 | 4.276 | 20 | 200 | fits | 120,476 | 196 | 0.371 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 308,659 | 3.087 | 20 | 20 | fits | 148,225 | 203 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 428,299 | 4.283 | 20 | 20 | fits | 120,476 | 196 | 0.371 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 164,074 | 1.641 | 20 | 24 | fits | 149,482 | 143 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 311,309 | 3.113 | 20 | 24 | fits | 148,225 | 203 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 311,243 | 3.112 | 20 | 50 | fits | 148,225 | 203 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 431,323 | 4.313 | 20 | 50 | fits | 120,476 | 196 | 0.371 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 518,934 | 5.189 | 20 | 20 | fits | 87,677 | 24 | 0.795 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 1,031,353 | 10.314 | 20 | 20 | fits | 86,129 | 28 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 355,868 | 3.559 | 20 | 20 | fits | 121,232 | 196 | 0.378 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 291,418 | 2.914 | 20 | 200 | fits | 149,174 | 208 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 412,034 | 4.120 | 20 | 200 | fits | 121,232 | 196 | 0.378 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 292,342 | 2.923 | 20 | 20 | fits | 149,174 | 208 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 412,738 | 4.127 | 20 | 20 | fits | 121,232 | 196 | 0.378 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 146,808 | 1.468 | 20 | 24 | fits | 149,349 | 142 | 0.426 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 294,992 | 2.950 | 20 | 24 | fits | 149,174 | 208 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 294,926 | 2.949 | 20 | 50 | fits | 149,174 | 208 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 415,762 | 4.158 | 20 | 50 | fits | 121,232 | 196 | 0.378 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 503,350 | 5.034 | 20 | 20 | fits | 87,654 | 24 | 0.795 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 1,016,687 | 10.167 | 20 | 20 | fits | 85,858 | 28 | 0.609 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 375,081 | 3.751 | 20 | 20 | fits | 121,287 | 199 | 0.364 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 302,430 | 3.024 | 20 | 200 | fits | 146,674 | 199 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 423,101 | 4.231 | 20 | 200 | fits | 121,287 | 199 | 0.364 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 303,354 | 3.034 | 20 | 20 | fits | 146,674 | 199 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 423,805 | 4.238 | 20 | 20 | fits | 121,287 | 199 | 0.364 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 160,320 | 1.603 | 20 | 24 | fits | 149,349 | 142 | 0.426 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 306,004 | 3.060 | 20 | 24 | fits | 146,674 | 199 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 305,938 | 3.059 | 20 | 50 | fits | 146,674 | 199 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 426,829 | 4.268 | 20 | 50 | fits | 121,287 | 199 | 0.364 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 514,417 | 5.144 | 20 | 20 | fits | 87,654 | 24 | 0.795 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 1,026,651 | 10.267 | 20 | 20 | fits | 85,925 | 28 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 364,072 | 3.641 | 20 | 20 | fits | 121,317 | 197 | 0.378 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 299,705 | 2.997 | 20 | 200 | fits | 147,865 | 203 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 420,406 | 4.204 | 20 | 200 | fits | 121,317 | 197 | 0.378 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 300,629 | 3.006 | 20 | 20 | fits | 147,865 | 203 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 421,110 | 4.211 | 20 | 20 | fits | 121,317 | 197 | 0.378 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 156,404 | 1.564 | 20 | 24 | fits | 149,187 | 142 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 303,279 | 3.033 | 20 | 24 | fits | 147,865 | 203 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 303,213 | 3.032 | 20 | 50 | fits | 147,865 | 203 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 424,134 | 4.241 | 20 | 50 | fits | 121,317 | 197 | 0.378 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 515,067 | 5.151 | 20 | 20 | fits | 81,579 | 33 | 0.815 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 1,017,734 | 10.177 | 20 | 20 | fits | 73,487 | 24 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 388,347 | 3.883 | 20 | 20 | fits | 133,461 | 209 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 296,558 | 2.966 | 20 | 200 | fits | 148,406 | 204 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 438,307 | 4.383 | 20 | 200 | fits | 133,461 | 209 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 297,482 | 2.975 | 20 | 20 | fits | 148,406 | 204 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 439,011 | 4.390 | 20 | 20 | fits | 133,461 | 209 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 152,716 | 1.527 | 20 | 24 | fits | 149,349 | 142 | 0.426 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 300,132 | 3.001 | 20 | 24 | fits | 148,406 | 204 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 300,066 | 3.001 | 20 | 50 | fits | 148,406 | 204 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 442,035 | 4.420 | 20 | 50 | fits | 133,461 | 209 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 529,163 | 5.292 | 20 | 20 | fits | 87,194 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 1,018,523 | 10.185 | 20 | 20 | fits | 60,370 | 20 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 376,873 | 3.769 | 20 | 20 | fits | 132,837 | 208 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 291,925 | 2.919 | 20 | 200 | fits | 149,393 | 209 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 433,106 | 4.331 | 20 | 200 | fits | 132,837 | 208 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 292,849 | 2.928 | 20 | 20 | fits | 149,393 | 209 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 433,810 | 4.338 | 20 | 20 | fits | 132,837 | 208 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 147,096 | 1.471 | 20 | 24 | fits | 149,187 | 142 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 295,499 | 2.955 | 20 | 24 | fits | 149,393 | 209 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 295,433 | 2.954 | 20 | 50 | fits | 149,393 | 209 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 436,834 | 4.368 | 20 | 50 | fits | 132,837 | 208 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 523,890 | 5.239 | 20 | 20 | fits | 87,122 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 1,013,203 | 10.132 | 20 | 20 | fits | 60,370 | 20 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 385,585 | 3.856 | 20 | 20 | fits | 125,920 | 203 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 301,092 | 3.011 | 20 | 200 | fits | 148,432 | 204 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 435,442 | 4.354 | 20 | 200 | fits | 125,920 | 203 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 302,016 | 3.020 | 20 | 20 | fits | 148,432 | 204 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 436,146 | 4.361 | 20 | 20 | fits | 125,920 | 203 | 0.406 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 157,224 | 1.572 | 20 | 24 | fits | 149,293 | 142 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 304,666 | 3.047 | 20 | 24 | fits | 148,432 | 204 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 304,600 | 3.046 | 20 | 50 | fits | 148,432 | 204 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 439,170 | 4.392 | 20 | 50 | fits | 125,920 | 203 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 526,373 | 5.264 | 20 | 20 | fits | 87,269 | 24 | 0.791 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 1,023,247 | 10.232 | 20 | 20 | fits | 67,688 | 26 | 0.758 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 371,950 | 3.720 | 20 | 20 | fits | 120,633 | 196 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 307,337 | 3.073 | 20 | 200 | fits | 150,008 | 208 | 0.439 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 427,354 | 4.274 | 20 | 200 | fits | 120,633 | 196 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 308,261 | 3.083 | 20 | 20 | fits | 150,008 | 208 | 0.439 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 428,058 | 4.281 | 20 | 20 | fits | 120,633 | 196 | 0.372 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 153,450 | 1.534 | 20 | 24 | fits | 149,273 | 143 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 310,911 | 3.109 | 20 | 24 | fits | 150,008 | 208 | 0.439 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 310,845 | 3.108 | 20 | 50 | fits | 150,008 | 208 | 0.439 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 431,082 | 4.311 | 20 | 50 | fits | 120,633 | 196 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 518,543 | 5.185 | 20 | 20 | fits | 87,527 | 24 | 0.794 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 1,110,665 | 11.107 | 20 | 20 | fits | 79,864 | 31 | 0.732 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 357,460 | 3.575 | 20 | 20 | fits | 121,357 | 196 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 293,012 | 2.930 | 20 | 200 | fits | 149,778 | 208 | 0.438 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 413,753 | 4.138 | 20 | 200 | fits | 121,357 | 196 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 293,936 | 2.939 | 20 | 20 | fits | 149,778 | 208 | 0.438 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 414,457 | 4.145 | 20 | 20 | fits | 121,357 | 196 | 0.379 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 147,798 | 1.478 | 20 | 24 | fits | 151,052 | 147 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 296,586 | 2.966 | 20 | 24 | fits | 149,778 | 208 | 0.438 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 296,520 | 2.965 | 20 | 50 | fits | 149,778 | 208 | 0.438 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 417,481 | 4.175 | 20 | 50 | fits | 121,357 | 196 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 505,125 | 5.051 | 20 | 20 | fits | 87,710 | 24 | 0.796 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,100,559 | 11.006 | 20 | 20 | fits | 86,074 | 28 | 0.614 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 373,893 | 3.739 | 20 | 20 | fits | 121,298 | 199 | 0.364 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 301,231 | 3.012 | 20 | 200 | fits | 146,673 | 199 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 421,913 | 4.219 | 20 | 200 | fits | 121,298 | 199 | 0.364 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 302,155 | 3.022 | 20 | 20 | fits | 146,673 | 199 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 422,617 | 4.226 | 20 | 20 | fits | 121,298 | 199 | 0.364 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 159,122 | 1.591 | 20 | 24 | fits | 149,184 | 142 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 304,805 | 3.048 | 20 | 24 | fits | 146,673 | 199 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 304,739 | 3.047 | 20 | 50 | fits | 146,673 | 199 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 425,641 | 4.256 | 20 | 50 | fits | 121,298 | 199 | 0.364 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 513,160 | 5.132 | 20 | 20 | fits | 87,585 | 24 | 0.794 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,104,780 | 11.048 | 20 | 20 | fits | 85,925 | 28 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 362,955 | 3.630 | 20 | 20 | fits | 121,158 | 196 | 0.378 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 298,579 | 2.986 | 20 | 200 | fits | 147,709 | 203 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 419,121 | 4.191 | 20 | 200 | fits | 121,158 | 196 | 0.378 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 299,503 | 2.995 | 20 | 20 | fits | 147,709 | 203 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 419,825 | 4.198 | 20 | 20 | fits | 121,158 | 196 | 0.378 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 155,434 | 1.554 | 20 | 24 | fits | 149,346 | 142 | 0.426 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 302,153 | 3.022 | 20 | 24 | fits | 147,709 | 203 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 302,087 | 3.021 | 20 | 50 | fits | 147,709 | 203 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 422,849 | 4.228 | 20 | 50 | fits | 121,158 | 196 | 0.378 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 510,306 | 5.103 | 20 | 20 | fits | 87,523 | 24 | 0.793 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,102,734 | 11.027 | 20 | 20 | fits | 85,925 | 28 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 366,441 | 3.664 | 20 | 20 | fits | 120,954 | 196 | 0.375 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 295,191 | 2.952 | 20 | 200 | fits | 148,237 | 203 | 0.438 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 415,529 | 4.155 | 20 | 200 | fits | 120,954 | 196 | 0.375 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 296,115 | 2.961 | 20 | 20 | fits | 148,237 | 203 | 0.438 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 416,233 | 4.162 | 20 | 20 | fits | 120,954 | 196 | 0.375 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 151,518 | 1.515 | 20 | 24 | fits | 149,184 | 142 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 298,765 | 2.988 | 20 | 24 | fits | 148,237 | 203 | 0.438 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 298,699 | 2.987 | 20 | 50 | fits | 148,237 | 203 | 0.438 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 419,257 | 4.193 | 20 | 50 | fits | 120,954 | 196 | 0.375 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 502,458 | 5.025 | 20 | 20 | fits | 83,267 | 33 | 0.821 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,097,102 | 10.971 | 20 | 20 | fits | 73,376 | 24 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 368,014 | 3.680 | 20 | 20 | fits | 132,659 | 209 | 0.416 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 291,725 | 2.917 | 20 | 200 | fits | 149,123 | 208 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 423,768 | 4.238 | 20 | 200 | fits | 132,659 | 209 | 0.416 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 292,649 | 2.926 | 20 | 20 | fits | 149,123 | 208 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 424,472 | 4.245 | 20 | 20 | fits | 132,659 | 209 | 0.416 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 147,166 | 1.472 | 20 | 24 | fits | 149,346 | 142 | 0.426 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 295,299 | 2.953 | 20 | 24 | fits | 149,123 | 208 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 295,233 | 2.952 | 20 | 50 | fits | 149,123 | 208 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 427,496 | 4.275 | 20 | 50 | fits | 132,659 | 209 | 0.416 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 603,820 | 6.038 | 20 | 20 | fits | 88,262 | 25 | 0.795 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,093,260 | 10.933 | 20 | 20 | fits | 60,370 | 20 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 475,709 | 4.757 | 20 | 20 | fits | 132,880 | 224 | 0.405 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 306,246 | 3.062 | 20 | 200 | fits | 149,468 | 186 | 0.463 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 526,166 | 5.262 | 20 | 200 | fits | 132,880 | 224 | 0.405 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 307,170 | 3.072 | 20 | 20 | fits | 149,468 | 186 | 0.463 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 526,870 | 5.269 | 20 | 20 | fits | 132,880 | 224 | 0.405 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 161,342 | 1.613 | 20 | 24 | fits | 149,346 | 142 | 0.426 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 309,820 | 3.098 | 20 | 24 | fits | 149,468 | 186 | 0.463 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 309,754 | 3.098 | 20 | 50 | fits | 149,468 | 186 | 0.463 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 529,894 | 5.299 | 20 | 50 | fits | 132,880 | 224 | 0.405 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 617,145 | 6.171 | 20 | 20 | fits | 87,317 | 24 | 0.792 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,106,701 | 11.067 | 20 | 20 | fits | 60,370 | 20 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 360,455 | 3.605 | 20 | 20 | fits | 121,132 | 196 | 0.377 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 296,105 | 2.961 | 20 | 200 | fits | 147,730 | 203 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 416,621 | 4.166 | 20 | 200 | fits | 121,132 | 196 | 0.377 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 297,029 | 2.970 | 20 | 20 | fits | 147,730 | 203 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 417,325 | 4.173 | 20 | 20 | fits | 121,132 | 196 | 0.377 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 152,939 | 1.529 | 20 | 24 | fits | 149,021 | 142 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 299,679 | 2.997 | 20 | 24 | fits | 147,730 | 203 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 299,613 | 2.996 | 20 | 50 | fits | 147,730 | 203 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 420,349 | 4.203 | 20 | 50 | fits | 121,132 | 196 | 0.377 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 508,138 | 5.081 | 20 | 20 | fits | 87,855 | 25 | 0.794 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 1,020,393 | 10.204 | 20 | 20 | fits | 79,961 | 30 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 363,251 | 3.633 | 20 | 20 | fits | 121,205 | 197 | 0.377 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 291,918 | 2.919 | 20 | 200 | fits | 149,558 | 208 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 412,507 | 4.125 | 20 | 200 | fits | 121,205 | 197 | 0.377 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 292,842 | 2.928 | 20 | 20 | fits | 149,558 | 208 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 413,211 | 4.132 | 20 | 20 | fits | 121,205 | 197 | 0.377 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 146,924 | 1.469 | 20 | 24 | fits | 149,104 | 142 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 295,492 | 2.955 | 20 | 24 | fits | 149,558 | 208 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 295,426 | 2.954 | 20 | 50 | fits | 149,558 | 208 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 416,235 | 4.162 | 20 | 50 | fits | 121,205 | 197 | 0.377 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 516,385 | 5.164 | 20 | 20 | fits | 90,718 | 31 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 1,013,009 | 10.130 | 20 | 20 | fits | 73,586 | 24 | 0.657 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 382,768 | 3.828 | 20 | 20 | fits | 126,167 | 203 | 0.408 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 305,139 | 3.051 | 20 | 200 | fits | 147,839 | 204 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 439,792 | 4.398 | 20 | 200 | fits | 126,167 | 203 | 0.408 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 306,063 | 3.061 | 20 | 20 | fits | 147,839 | 204 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 440,496 | 4.405 | 20 | 20 | fits | 126,167 | 203 | 0.408 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 161,864 | 1.619 | 20 | 24 | fits | 149,104 | 142 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 308,713 | 3.087 | 20 | 24 | fits | 147,839 | 204 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 308,647 | 3.086 | 20 | 50 | fits | 147,839 | 204 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 443,520 | 4.435 | 20 | 50 | fits | 126,167 | 203 | 0.408 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 530,600 | 5.306 | 20 | 20 | fits | 87,146 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 1,027,369 | 10.274 | 20 | 20 | fits | 73,487 | 24 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 383,104 | 3.831 | 20 | 20 | fits | 120,907 | 196 | 0.373 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 311,901 | 3.119 | 20 | 200 | fits | 150,355 | 208 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 432,192 | 4.322 | 20 | 200 | fits | 120,907 | 196 | 0.373 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 312,825 | 3.128 | 20 | 20 | fits | 150,355 | 208 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 432,896 | 4.329 | 20 | 20 | fits | 120,907 | 196 | 0.373 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 157,667 | 1.577 | 20 | 24 | fits | 149,039 | 143 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 315,475 | 3.155 | 20 | 24 | fits | 150,355 | 208 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 315,409 | 3.154 | 20 | 50 | fits | 150,355 | 208 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 435,920 | 4.359 | 20 | 50 | fits | 120,907 | 196 | 0.373 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 523,384 | 5.234 | 20 | 20 | fits | 87,530 | 24 | 0.794 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 1,036,352 | 10.364 | 20 | 20 | fits | 88,024 | 29 | 0.658 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 365,893 | 3.659 | 20 | 20 | fits | 121,298 | 199 | 0.364 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 293,231 | 2.932 | 20 | 200 | fits | 146,667 | 199 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 413,913 | 4.139 | 20 | 200 | fits | 121,298 | 199 | 0.364 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 294,155 | 2.942 | 20 | 20 | fits | 146,667 | 199 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 414,617 | 4.146 | 20 | 20 | fits | 121,298 | 199 | 0.364 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 151,128 | 1.511 | 20 | 24 | fits | 149,131 | 142 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 296,805 | 2.968 | 20 | 24 | fits | 146,667 | 199 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 296,739 | 2.967 | 20 | 50 | fits | 146,667 | 199 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 417,641 | 4.176 | 20 | 50 | fits | 121,298 | 199 | 0.364 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 505,318 | 5.053 | 20 | 20 | fits | 87,743 | 24 | 0.796 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 1,017,339 | 10.173 | 20 | 20 | fits | 85,947 | 28 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 356,045 | 3.560 | 20 | 20 | fits | 121,215 | 196 | 0.378 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 291,612 | 2.916 | 20 | 200 | fits | 149,063 | 208 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 412,211 | 4.122 | 20 | 200 | fits | 121,215 | 196 | 0.378 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 292,536 | 2.925 | 20 | 20 | fits | 149,063 | 208 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 412,915 | 4.129 | 20 | 20 | fits | 121,215 | 196 | 0.378 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 147,113 | 1.471 | 20 | 24 | fits | 149,293 | 142 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 295,186 | 2.952 | 20 | 24 | fits | 149,063 | 208 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 295,120 | 2.951 | 20 | 50 | fits | 149,063 | 208 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 415,939 | 4.159 | 20 | 50 | fits | 121,215 | 196 | 0.378 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 495,659 | 4.957 | 20 | 20 | fits | 79,786 | 26 | 0.831 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 1,013,740 | 10.137 | 20 | 20 | fits | 85,925 | 28 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 383,953 | 3.840 | 20 | 20 | fits | 130,146 | 205 | 0.404 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 303,004 | 3.030 | 20 | 200 | fits | 146,616 | 199 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 432,534 | 4.325 | 20 | 200 | fits | 130,146 | 205 | 0.404 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 303,928 | 3.039 | 20 | 20 | fits | 146,616 | 199 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 433,238 | 4.332 | 20 | 20 | fits | 130,146 | 205 | 0.404 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 160,952 | 1.610 | 20 | 24 | fits | 149,293 | 142 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 306,578 | 3.066 | 20 | 24 | fits | 146,616 | 199 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 306,512 | 3.065 | 20 | 50 | fits | 146,616 | 199 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 436,262 | 4.363 | 20 | 50 | fits | 130,146 | 205 | 0.404 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 523,928 | 5.239 | 20 | 20 | fits | 87,732 | 25 | 0.793 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 1,029,430 | 10.294 | 20 | 20 | fits | 73,457 | 24 | 0.653 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 372,798 | 3.728 | 20 | 20 | fits | 129,728 | 209 | 0.367 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 299,666 | 2.997 | 20 | 200 | fits | 147,194 | 197 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 428,778 | 4.288 | 20 | 200 | fits | 129,728 | 209 | 0.367 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 300,590 | 3.006 | 20 | 20 | fits | 147,194 | 197 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 429,482 | 4.295 | 20 | 20 | fits | 129,728 | 209 | 0.367 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 157,036 | 1.570 | 20 | 24 | fits | 149,131 | 142 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 303,240 | 3.032 | 20 | 24 | fits | 147,194 | 197 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 303,174 | 3.032 | 20 | 50 | fits | 147,194 | 197 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 432,506 | 4.325 | 20 | 50 | fits | 129,728 | 209 | 0.367 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 532,713 | 5.327 | 20 | 20 | fits | 90,775 | 31 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 1,022,178 | 10.222 | 20 | 20 | fits | 60,370 | 20 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 366,948 | 3.669 | 20 | 20 | fits | 121,173 | 196 | 0.377 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 302,557 | 3.026 | 20 | 200 | fits | 147,949 | 203 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 423,114 | 4.231 | 20 | 200 | fits | 121,173 | 196 | 0.377 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 303,481 | 3.035 | 20 | 20 | fits | 147,949 | 203 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 423,818 | 4.238 | 20 | 20 | fits | 121,173 | 196 | 0.377 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 159,172 | 1.592 | 20 | 24 | fits | 149,293 | 142 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 306,131 | 3.061 | 20 | 24 | fits | 147,949 | 203 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 306,065 | 3.061 | 20 | 50 | fits | 147,949 | 203 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 426,842 | 4.268 | 20 | 50 | fits | 121,173 | 196 | 0.377 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 514,474 | 5.145 | 20 | 20 | fits | 87,698 | 24 | 0.796 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 1,026,619 | 10.266 | 20 | 20 | fits | 79,931 | 30 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 370,277 | 3.703 | 20 | 20 | fits | 120,980 | 196 | 0.376 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 299,001 | 2.990 | 20 | 200 | fits | 148,309 | 203 | 0.439 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 419,365 | 4.194 | 20 | 200 | fits | 120,980 | 196 | 0.376 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 299,925 | 2.999 | 20 | 20 | fits | 148,309 | 203 | 0.439 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 420,069 | 4.201 | 20 | 20 | fits | 120,980 | 196 | 0.376 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 155,256 | 1.553 | 20 | 24 | fits | 149,131 | 142 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 302,575 | 3.026 | 20 | 24 | fits | 148,309 | 203 | 0.439 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 302,509 | 3.025 | 20 | 50 | fits | 148,309 | 203 | 0.439 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 423,093 | 4.231 | 20 | 50 | fits | 120,980 | 196 | 0.376 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 510,628 | 5.106 | 20 | 20 | fits | 87,601 | 24 | 0.795 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 1,100,677 | 11.007 | 20 | 20 | fits | 86,219 | 29 | 0.619 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 359,409 | 3.594 | 20 | 20 | fits | 120,590 | 197 | 0.371 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 295,007 | 2.950 | 20 | 200 | fits | 148,003 | 203 | 0.438 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 414,981 | 4.150 | 20 | 200 | fits | 120,590 | 197 | 0.371 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 295,931 | 2.959 | 20 | 20 | fits | 148,003 | 203 | 0.438 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 415,685 | 4.157 | 20 | 20 | fits | 120,590 | 197 | 0.371 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 151,568 | 1.516 | 20 | 24 | fits | 149,293 | 142 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 298,581 | 2.986 | 20 | 24 | fits | 148,003 | 203 | 0.438 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 298,515 | 2.985 | 20 | 50 | fits | 148,003 | 203 | 0.438 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 418,709 | 4.187 | 20 | 50 | fits | 120,590 | 197 | 0.371 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 518,943 | 5.189 | 20 | 20 | fits | 90,802 | 31 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,093,157 | 10.932 | 20 | 20 | fits | 73,487 | 24 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 369,690 | 3.697 | 20 | 20 | fits | 125,969 | 202 | 0.407 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 292,375 | 2.924 | 20 | 200 | fits | 149,899 | 209 | 0.438 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 426,774 | 4.268 | 20 | 200 | fits | 125,969 | 202 | 0.407 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 293,299 | 2.933 | 20 | 20 | fits | 149,899 | 209 | 0.438 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 427,478 | 4.275 | 20 | 20 | fits | 125,969 | 202 | 0.407 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 147,040 | 1.470 | 20 | 24 | fits | 149,131 | 142 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 295,949 | 2.959 | 20 | 24 | fits | 149,899 | 209 | 0.438 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 295,883 | 2.959 | 20 | 50 | fits | 149,899 | 209 | 0.438 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 430,502 | 4.305 | 20 | 50 | fits | 125,969 | 202 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 517,735 | 5.177 | 20 | 20 | fits | 87,299 | 24 | 0.792 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,092,072 | 10.921 | 20 | 20 | fits | 73,581 | 25 | 0.653 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 379,884 | 3.799 | 20 | 20 | fits | 120,646 | 196 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 315,258 | 3.153 | 20 | 200 | fits | 150,064 | 208 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 435,288 | 4.353 | 20 | 200 | fits | 120,646 | 196 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 316,182 | 3.162 | 20 | 20 | fits | 150,064 | 208 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 435,992 | 4.360 | 20 | 20 | fits | 120,646 | 196 | 0.372 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 161,315 | 1.613 | 20 | 24 | fits | 149,282 | 143 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 318,832 | 3.188 | 20 | 24 | fits | 150,064 | 208 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 318,766 | 3.188 | 20 | 50 | fits | 150,064 | 208 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 439,016 | 4.390 | 20 | 50 | fits | 120,646 | 196 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 518,637 | 5.186 | 20 | 20 | fits | 79,687 | 26 | 0.830 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,115,798 | 11.158 | 20 | 20 | fits | 88,167 | 29 | 0.662 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 384,446 | 3.844 | 20 | 20 | fits | 129,771 | 202 | 0.413 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 311,942 | 3.119 | 20 | 200 | fits | 150,421 | 208 | 0.442 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 441,097 | 4.411 | 20 | 200 | fits | 129,771 | 202 | 0.413 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 312,866 | 3.129 | 20 | 20 | fits | 150,421 | 208 | 0.442 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 441,801 | 4.418 | 20 | 20 | fits | 129,771 | 202 | 0.413 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 157,546 | 1.575 | 20 | 24 | fits | 149,363 | 143 | 0.426 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 315,516 | 3.155 | 20 | 24 | fits | 150,421 | 208 | 0.442 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 315,450 | 3.155 | 20 | 50 | fits | 150,421 | 208 | 0.442 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 444,825 | 4.448 | 20 | 50 | fits | 129,771 | 202 | 0.413 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 609,135 | 6.091 | 20 | 20 | fits | 87,012 | 25 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,114,961 | 11.150 | 20 | 20 | fits | 73,508 | 24 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 373,130 | 3.731 | 20 | 20 | fits | 129,720 | 202 | 0.413 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 293,646 | 2.936 | 20 | 200 | fits | 148,432 | 203 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 422,750 | 4.228 | 20 | 200 | fits | 129,720 | 202 | 0.413 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 294,570 | 2.946 | 20 | 20 | fits | 148,432 | 203 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 423,454 | 4.235 | 20 | 20 | fits | 129,720 | 202 | 0.413 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 149,778 | 1.498 | 20 | 24 | fits | 149,346 | 142 | 0.426 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 297,220 | 2.972 | 20 | 24 | fits | 148,432 | 203 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 297,154 | 2.972 | 20 | 50 | fits | 148,432 | 203 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 426,478 | 4.265 | 20 | 50 | fits | 129,720 | 202 | 0.413 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 590,722 | 5.907 | 20 | 20 | fits | 86,946 | 25 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,096,172 | 10.962 | 20 | 20 | fits | 73,376 | 24 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 363,556 | 3.636 | 20 | 20 | fits | 129,230 | 202 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 290,651 | 2.907 | 20 | 200 | fits | 149,353 | 208 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 419,265 | 4.193 | 20 | 200 | fits | 129,230 | 202 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 291,575 | 2.916 | 20 | 20 | fits | 149,353 | 208 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 419,969 | 4.200 | 20 | 20 | fits | 129,230 | 202 | 0.409 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 145,862 | 1.459 | 20 | 24 | fits | 149,184 | 142 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 294,225 | 2.942 | 20 | 24 | fits | 149,353 | 208 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 294,159 | 2.942 | 20 | 50 | fits | 149,353 | 208 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 422,993 | 4.230 | 20 | 50 | fits | 129,230 | 202 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 587,307 | 5.873 | 20 | 20 | fits | 87,016 | 26 | 0.783 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,092,878 | 10.929 | 20 | 20 | fits | 73,457 | 24 | 0.653 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 373,619 | 3.736 | 20 | 20 | fits | 124,732 | 205 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 297,883 | 2.979 | 20 | 200 | fits | 148,753 | 204 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 421,999 | 4.220 | 20 | 200 | fits | 124,732 | 205 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 298,807 | 2.988 | 20 | 20 | fits | 148,753 | 204 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 422,703 | 4.227 | 20 | 20 | fits | 124,732 | 205 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 145,288 | 1.453 | 20 | 24 | fits | 149,056 | 143 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 301,457 | 3.015 | 20 | 24 | fits | 148,753 | 204 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 301,391 | 3.014 | 20 | 50 | fits | 148,753 | 204 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 425,727 | 4.257 | 20 | 50 | fits | 124,732 | 205 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 513,002 | 5.130 | 20 | 20 | fits | 87,341 | 24 | 0.792 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 1,012,982 | 10.130 | 20 | 20 | fits | 70,894 | 33 | 0.746 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 362,025 | 3.620 | 20 | 20 | fits | 121,173 | 196 | 0.377 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 297,634 | 2.976 | 20 | 200 | fits | 148,008 | 203 | 0.438 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 418,191 | 4.182 | 20 | 200 | fits | 121,173 | 196 | 0.377 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 298,558 | 2.986 | 20 | 20 | fits | 148,008 | 203 | 0.438 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 418,895 | 4.189 | 20 | 20 | fits | 121,173 | 196 | 0.377 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 154,190 | 1.542 | 20 | 24 | fits | 149,146 | 142 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 301,208 | 3.012 | 20 | 24 | fits | 148,008 | 203 | 0.438 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 301,142 | 3.011 | 20 | 50 | fits | 148,008 | 203 | 0.438 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 421,919 | 4.219 | 20 | 50 | fits | 121,173 | 196 | 0.377 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 509,465 | 5.095 | 20 | 20 | fits | 87,612 | 24 | 0.794 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 1,021,480 | 10.215 | 20 | 20 | fits | 86,024 | 28 | 0.614 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 364,600 | 3.646 | 20 | 20 | fits | 120,980 | 196 | 0.376 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 293,324 | 2.933 | 20 | 200 | fits | 148,363 | 203 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 413,688 | 4.137 | 20 | 200 | fits | 120,980 | 196 | 0.376 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 294,248 | 2.942 | 20 | 20 | fits | 148,363 | 203 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 414,392 | 4.144 | 20 | 20 | fits | 120,980 | 196 | 0.376 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 149,525 | 1.495 | 20 | 24 | fits | 148,984 | 142 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 296,898 | 2.969 | 20 | 24 | fits | 148,363 | 203 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 296,832 | 2.968 | 20 | 50 | fits | 148,363 | 203 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 417,416 | 4.174 | 20 | 50 | fits | 120,980 | 196 | 0.376 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 504,838 | 5.048 | 20 | 20 | fits | 87,488 | 24 | 0.793 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 1,017,803 | 10.178 | 20 | 20 | fits | 86,014 | 28 | 0.612 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 354,429 | 3.544 | 20 | 20 | fits | 120,503 | 196 | 0.370 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 289,946 | 2.899 | 20 | 200 | fits | 149,422 | 208 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 409,833 | 4.098 | 20 | 200 | fits | 120,503 | 196 | 0.370 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 290,870 | 2.909 | 20 | 20 | fits | 149,422 | 208 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 410,537 | 4.105 | 20 | 20 | fits | 120,503 | 196 | 0.370 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 145,088 | 1.451 | 20 | 24 | fits | 149,146 | 142 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 293,520 | 2.935 | 20 | 24 | fits | 149,422 | 208 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 293,454 | 2.935 | 20 | 50 | fits | 149,422 | 208 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 413,561 | 4.136 | 20 | 50 | fits | 120,503 | 196 | 0.370 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 501,226 | 5.012 | 20 | 20 | fits | 87,731 | 25 | 0.792 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 1,013,535 | 10.135 | 20 | 20 | fits | 86,006 | 28 | 0.612 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 372,862 | 3.729 | 20 | 20 | fits | 121,122 | 197 | 0.376 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 301,612 | 3.016 | 20 | 200 | fits | 148,432 | 203 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 422,118 | 4.221 | 20 | 200 | fits | 121,122 | 197 | 0.376 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 302,536 | 3.025 | 20 | 20 | fits | 148,432 | 203 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 422,822 | 4.228 | 20 | 20 | fits | 121,122 | 197 | 0.376 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 157,744 | 1.577 | 20 | 24 | fits | 149,146 | 142 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 305,186 | 3.052 | 20 | 24 | fits | 148,432 | 203 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 305,120 | 3.051 | 20 | 50 | fits | 148,432 | 203 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 425,846 | 4.258 | 20 | 50 | fits | 121,122 | 197 | 0.376 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 516,833 | 5.168 | 20 | 20 | fits | 81,633 | 33 | 0.816 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 1,019,533 | 10.195 | 20 | 20 | fits | 73,487 | 24 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 381,668 | 3.817 | 20 | 20 | fits | 132,983 | 209 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 296,658 | 2.967 | 20 | 200 | fits | 148,143 | 204 | 0.439 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 437,985 | 4.380 | 20 | 200 | fits | 132,983 | 209 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 297,582 | 2.976 | 20 | 20 | fits | 148,143 | 204 | 0.439 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 438,689 | 4.387 | 20 | 20 | fits | 132,983 | 209 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 153,079 | 1.531 | 20 | 24 | fits | 148,984 | 142 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 300,232 | 3.002 | 20 | 24 | fits | 148,143 | 204 | 0.439 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 300,166 | 3.002 | 20 | 50 | fits | 148,143 | 204 | 0.439 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 441,713 | 4.417 | 20 | 50 | fits | 132,983 | 209 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 528,680 | 5.287 | 20 | 20 | fits | 87,033 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 1,018,134 | 10.181 | 20 | 20 | fits | 60,464 | 21 | 0.697 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 375,424 | 3.754 | 20 | 20 | fits | 131,578 | 208 | 0.414 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 301,362 | 3.014 | 20 | 200 | fits | 150,434 | 208 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 432,324 | 4.323 | 20 | 200 | fits | 131,578 | 208 | 0.414 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 302,286 | 3.023 | 20 | 20 | fits | 150,434 | 208 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 433,028 | 4.330 | 20 | 20 | fits | 131,578 | 208 | 0.414 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 147,090 | 1.471 | 20 | 24 | fits | 149,270 | 143 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 304,936 | 3.049 | 20 | 24 | fits | 150,434 | 208 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 304,870 | 3.049 | 20 | 50 | fits | 150,434 | 208 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 436,052 | 4.361 | 20 | 50 | fits | 131,578 | 208 | 0.414 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 523,309 | 5.233 | 20 | 20 | fits | 87,323 | 24 | 0.792 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 1,029,327 | 10.293 | 20 | 20 | fits | 66,607 | 27 | 0.763 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 381,550 | 3.816 | 20 | 20 | fits | 127,788 | 221 | 0.361 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 302,427 | 3.024 | 20 | 200 | fits | 147,946 | 181 | 0.466 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 429,599 | 4.296 | 20 | 200 | fits | 127,788 | 221 | 0.361 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 303,351 | 3.034 | 20 | 20 | fits | 147,946 | 181 | 0.466 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 430,303 | 4.303 | 20 | 20 | fits | 127,788 | 221 | 0.361 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 159,045 | 1.590 | 20 | 24 | fits | 149,177 | 142 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 306,001 | 3.060 | 20 | 24 | fits | 147,946 | 181 | 0.466 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 305,935 | 3.059 | 20 | 50 | fits | 147,946 | 181 | 0.466 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 433,327 | 4.333 | 20 | 50 | fits | 127,788 | 221 | 0.361 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 520,897 | 5.209 | 20 | 20 | fits | 87,636 | 24 | 0.795 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 1,026,700 | 10.267 | 20 | 20 | fits | 73,398 | 24 | 0.651 |
| LINK_UP | `adp.link_up.if0` | 2,623 | 0.026 | 20 | 200 | fits | 28,298 | 43 (11) | 0.736 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 16,581 | 0.166 | 20 | 200 | fits | 23,607 | 23 (39) | 0.750 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 8,915 | 0.089 | 20 | 200 | fits | 2,638 | 10 (11) | 0.571 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 155,716 | 1.557 | 20 | 200 | fits | 156,656 | 250 | 0.467 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 189,951 | 1.900 | 20 | 20 | fits | 105,910 | 115 | 0.361 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 290,570 | 2.906 | 20 | 24 | fits | 75,337 | 54 | 0.473 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 182,630 | 1.826 | 20 | 50 | fits | 86,526 | 82 | 0.667 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 941,935 | 9.419 | 20 | 20 | fits | 47,346 | 16 | 0.761 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 240,141 | 2.401 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 155,716 | 1.557 | 20 | 200 | fits | 156,656 | 250 | 0.467 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 203,917 | 2.039 | 20 | 20 | fits | 150,628 | 266 | 0.347 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 279,866 | 2.799 | 20 | 24 | fits | 78,747 | 60 | 0.501 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 186,095 | 1.861 | 20 | 50 | fits | 89,991 | 88 | 0.680 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 1,001,567 | 10.016 | 20 | 20 | fits | 64,248 | 26 | 0.736 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 268,832 | 2.688 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 21,815 | 0.218 | 20 | 20 | fits | 32,988 | 27 (35) | 0.816 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 12,972 | 0.130 | 20 | 20 | fits | 29,671 | 23 (14) | 0.843 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 17,267 | 0.173 | 20 | 20 | fits | 28,934 | 24 (14) | 0.841 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 10,650 | 0.106 | 20 | 20 | fits | 29,928 | 21 (35) | 0.823 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 78,097 | 0.781 | 20 | 20 | fits | 27,867 | 8 | 0.750 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 45,877 | 0.459 | 20 | 20 | fits | 45,943 | 12 | 0.899 |
| malformed MRPDU discard | `srp.malformed.if0` | 22,584 | 0.226 | 20 | 20 | fits | 22,650 | 12 | 0.740 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 90,121 | 0.901 | 220 | 220 | fits | 56,882 | 6 | 0.894 |
| an event behind 15 others | `backlog.event.if0` | 165,874 | 1.659 | 20 | 200 | fits | 58,177 | 79 | 0.577 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 429,592 | 4.296 | 20 | 20 | fits | 47,572 | 72 | 0.316 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 419,723 | 4.197 | 20 | 200 | fits | 148,207 | 159 | 0.408 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 419,107 | 4.191 | 20 | 200 | fits | 148,207 | 159 | 0.408 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 415,401 | 4.154 | 20 | 20 | fits | 148,207 | 159 | 0.408 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 462,137 | 4.621 | 20 | 20 | fits | 47,572 | 72 | 0.316 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 151,052 | 1.511 | 20 | 24 | fits | 151,943 | 148 | 0.439 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 418,051 | 4.181 | 20 | 24 | fits | 148,207 | 159 | 0.408 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 417,985 | 4.180 | 20 | 50 | fits | 148,207 | 159 | 0.408 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 417,589 | 4.176 | 20 | 50 | fits | 148,207 | 159 | 0.408 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 465,095 | 4.651 | 20 | 20 | fits | 47,572 | 72 | 0.316 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 526,385 | 5.264 | 20 | 20 | fits | 25,074 | 41 | 0.182 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 378,005 | 3.780 | 20 | 20 | fits | 126,935 | 206 | 0.403 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 291,528 | 2.915 | 20 | 200 | fits | 146,726 | 200 | 0.439 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 426,855 | 4.269 | 20 | 200 | fits | 126,935 | 206 | 0.403 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 292,452 | 2.925 | 20 | 20 | fits | 146,726 | 200 | 0.439 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 427,559 | 4.276 | 20 | 20 | fits | 126,935 | 206 | 0.403 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 149,366 | 1.494 | 20 | 24 | fits | 149,552 | 145 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 295,102 | 2.951 | 20 | 24 | fits | 146,726 | 200 | 0.439 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 295,036 | 2.950 | 20 | 50 | fits | 146,726 | 200 | 0.439 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 430,583 | 4.306 | 20 | 50 | fits | 126,935 | 206 | 0.403 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 517,346 | 5.173 | 20 | 20 | fits | 86,829 | 24 | 0.791 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,014,072 | 10.141 | 20 | 20 | fits | 73,576 | 25 | 0.653 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 7,977 | 0.080 | 20 | 20 | fits | 27,123 | 19 | 0.802 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 291,528 | 2.915 | 20 | 200 | fits | 146,726 | 200 | 0.439 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 27,263 | 0.273 | 20 | 200 | fits | 27,123 | 19 | 0.802 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 292,452 | 2.925 | 20 | 20 | fits | 146,726 | 200 | 0.439 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 418,534 | 4.185 | 20 | 20 | fits | 117,910 | 196 | 0.377 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 149,366 | 1.494 | 20 | 24 | fits | 149,552 | 145 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 295,102 | 2.951 | 20 | 24 | fits | 146,726 | 200 | 0.439 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 295,036 | 2.950 | 20 | 50 | fits | 146,726 | 200 | 0.439 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 421,558 | 4.216 | 20 | 50 | fits | 117,910 | 196 | 0.377 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 507,812 | 5.078 | 20 | 20 | fits | 86,320 | 24 | 0.788 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,004,832 | 10.048 | 20 | 20 | fits | 73,482 | 24 | 0.654 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,311,460 | 63.115 | 20 | 20 | MISS ceiling | 18,941 | 13 | 0.654 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,330,313 | 63.303 | 20 | 20 | MISS ceiling | 18,929 | 13 | 0.630 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,349,169 | 63.492 | 20 | 20 | MISS ceiling | 18,913 | 13 | 0.630 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,367,937 | 63.679 | 20 | 20 | MISS ceiling | 18,844 | 13 | 0.637 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,386,626 | 63.866 | 20 | 20 | MISS ceiling | 18,752 | 13 | 0.654 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 130,387 | 1.304 | 20 | 200 | fits | 131,805 | 239 | 0.350 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 129,771 | 1.298 | 20 | 200 | fits | 131,805 | 239 | 0.350 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 126,065 | 1.261 | 20 | 20 | fits | 131,805 | 239 | 0.350 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,220,400 | 62.204 | 20 | 20 | MISS ceiling | 30,119 | 15 | 0.768 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 232,425 | 2.324 | 20 | 24 | fits | 102,720 | 107 | 0.502 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,193,767 | 61.938 | 20 | 24 | MISS ceiling | 147,528 | 106 | 0.462 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 128,649 | 1.286 | 20 | 50 | fits | 131,805 | 239 | 0.350 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 128,253 | 1.283 | 20 | 50 | fits | 131,805 | 239 | 0.350 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 315,623 | 3.156 | 20 | 20 | fits | 84,716 | 62 | 0.738 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 828,694 | 8.287 | 20 | 20 | fits | 86,765 | 28 | 0.627 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 6,514 | 0.065 | 20 | 20 | fits | 24,917 | 13 (29) | 0.794 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,653 | 0.077 | 20 | 20 | fits | 26,265 | 19 (35) | 0.788 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 17,250 | 0.172 | 20 | 20 | fits | 29,975 | 21 (12) | 0.821 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 10,919 | 0.109 | 20 | 50 | fits | 28,298 | 43 | 0.736 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 8,735 | 0.087 | 20 | 50 | fits | 25,173 | 35 | 0.721 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 11,940 | 0.119 | 20 | 50 | fits | 24,953 | 35 | 0.723 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 16,553 | 0.166 | 20 | 50 | fits | 29,874 | 61 | 0.631 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 19,129 | 0.191 | 20 | 50 | fits | 29,874 | 61 | 0.631 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 10,166 | 0.102 | 20 | 50 | fits | 23,268 | 30 | 0.656 |
| LINK_UP | `adp.link_up.if0` | 2,623 | 0.026 | 20 | 200 | fits | 28,298 | 43 (11) | 0.736 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 16,581 | 0.166 | 20 | 200 | fits | 23,607 | 23 (39) | 0.750 |
| LINK_DOWN | `adp.link_down.if0` | 2,340 | 0.023 | 20 | 200 | fits | 25,628 | 23 (9) | 0.777 |
| LINK_UP | `adp.link_up.if0` | 2,623 | 0.026 | 20 | 200 | fits | 28,298 | 43 (11) | 0.736 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 16,581 | 0.166 | 20 | 200 | fits | 23,607 | 23 (39) | 0.750 |
| GM_CHANGE | `adp.gm_change.if0` | 2,392 | 0.024 | 20 | 200 | fits | 17,842 | 17 (11) | 0.747 |
| LINK_UP | `adp.link_up.if0` | 2,623 | 0.026 | 20 | 200 | fits | 28,298 | 43 (11) | 0.736 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 16,581 | 0.166 | 20 | 200 | fits | 23,607 | 23 (39) | 0.750 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,554 | 0.046 | 20 | 200 | fits | 17,086 | 16 (31) | 0.628 |
| LINK_UP | `adp.link_up.if0` | 2,623 | 0.026 | 20 | 200 | fits | 28,298 | 43 (11) | 0.736 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 16,581 | 0.166 | 20 | 200 | fits | 23,607 | 23 (39) | 0.750 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,554 | 0.046 | 20 | 200 | fits | 17,086 | 16 (31) | 0.628 |
| set_name | `aecp_fanout.set_name.if0` | 60,345 | 0.603 | 20 | 24 | fits | 63,200 | 89 | 0.588 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 51,977 | 0.520 | 20 | 24 | fits | 55,872 | 78 | 0.606 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 55,579 | 0.556 | 20 | 24 | fits | 51,406 | 79 | 0.568 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 50,127 | 0.501 | 20 | 24 | fits | 50,341 | 78 | 0.555 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 61,531 | 0.615 | 20 | 24 | fits | 60,529 | 66 | 0.628 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 310,251 | 3.103 | 20 | 24 | fits | 59,105 | 65 | 0.632 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 332,791 | 3.328 | 20 | 24 | fits | 54,212 | 67 | 0.596 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 49,740 | 0.497 | 20 | 24 | fits | 50,446 | 78 | 0.564 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 50,843 | 0.508 | 20 | 24 | fits | 50,684 | 79 | 0.566 |
| BIND_RX | `acmp.bind_rx.if0` | 19,106 | 0.191 | 20 | 20 | fits | 41,200 | 26 (77) | 0.793 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 10,283 | 0.103 | 20 | 20 | fits | 32,967 | 19 (32) | 0.837 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,864 | 0.109 | 20 | 20 | fits | 26,365 | 15 (47) | 0.783 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,870 | 0.139 | 20 | 20 | fits | 39,468 | 18 (50) | 0.832 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 11,051 | 0.111 | 20 | 20 | fits | 26,566 | 17 (48) | 0.765 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,503 | 0.095 | 20 | 20 | fits | 24,775 | 16 (48) | 0.718 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 8,960 | 0.090 | 20 | 20 | fits | 23,878 | 16 (48) | 0.713 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,010 | 0.090 | 20 | 20 | fits | 23,885 | 16 (48) | 0.713 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 24,341 | 0.243 | 20 | 24 | fits | 29,134 | 20 | 0.792 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 19,736 | 0.197 | 20 | 24 | fits | 32,916 | 20 | 0.724 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 26,973 | 0.270 | 20 | 24 | fits | 28,502 | 20 | 0.738 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 15,098 | 0.151 | 20 | 24 | fits | 28,085 | 20 | 0.734 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 31,567 | 0.316 | 20 | 24 | fits | 34,338 | 26 | 0.749 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 27,152 | 0.272 | 20 | 24 | fits | 28,986 | 20 | 0.739 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 14,980 | 0.150 | 20 | 24 | fits | 27,777 | 20 | 0.738 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 26,377 | 0.264 | 20 | 24 | fits | 28,046 | 20 | 0.751 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 14,750 | 0.147 | 20 | 24 | fits | 27,416 | 20 | 0.753 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 28,697 | 0.287 | 20 | 24 | fits | 30,512 | 21 | 0.654 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 25,353 | 0.254 | 20 | 24 | fits | 27,309 | 20 | 0.772 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 14,074 | 0.141 | 20 | 24 | fits | 27,465 | 20 | 0.770 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 25,932 | 0.259 | 20 | 24 | fits | 27,820 | 20 | 0.737 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 15,434 | 0.154 | 20 | 24 | fits | 28,888 | 20 | 0.747 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 25,930 | 0.259 | 20 | 24 | fits | 27,840 | 20 | 0.751 |
| get_configuration | `aecp.get_configuration.if0` | 12,712 | 0.127 | 20 | 24 | fits | 25,298 | 20 | 0.753 |
| entity_available | `aecp.entity_available.if0` | 12,676 | 0.127 | 20 | 24 | fits | 25,431 | 20 | 0.750 |
| get_name | `aecp.get_name.if0` | 26,385 | 0.264 | 20 | 24 | fits | 28,031 | 20 | 0.749 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 15,783 | 0.158 | 20 | 24 | fits | 28,849 | 27 | 0.718 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 27,488 | 0.275 | 20 | 24 | fits | 29,000 | 29 | 0.751 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 13,505 | 0.135 | 20 | 24 | fits | 26,072 | 20 | 0.769 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 20,066 | 0.201 | 20 | 24 | fits | 30,145 | 26 | 0.747 |
| set_name | `aecp.set_name.if0` | 32,663 | 0.327 | 20 | 24 | fits | 44,065 | 43 | 0.763 |
| lock_entity | `aecp.lock_entity.if0` | 18,928 | 0.189 | 20 | 24 | fits | 36,006 | 34 | 0.789 |
| unlock_entity | `aecp.unlock_entity.if0` | 14,515 | 0.145 | 20 | 24 | fits | 34,998 | 33 | 0.785 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 144,565 | 1.446 | 20 | 24 | fits | 147,796 | 93 | 0.336 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 306,805 | 3.068 | 20 | 24 | fits | 139,178 | 69 | 0.305 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 204,942 | 2.049 | 20 | 24 | fits | 42,458 | 18 | 0.692 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 366,513 | 3.665 | 20 | 24 | fits | 93,801 | 17 | 0.669 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 298,310 | 2.983 | 20 | 24 | fits | 95,714 | 17 | 0.680 |
| LINK_UP | `fixture.link_up.if0` | 2,623 | 0.026 | 20 | 200 | fits | 28,298 | 43 (11) | 0.736 |
| malformed MRPDU discard | `fixture.malformed.if0` | 23,384 | 0.234 | 20 | 20 | fits | 23,450 | 12 | 0.776 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 31,811 | 0.318 | 20 | 24 | fits | 46,377 | 43 | 0.783 |
| LINK_DOWN | `fixture.link_down.if0` | 2,597 | 0.026 | 20 | 200 | fits | 27,428 | 23 (9) | 0.791 |
| BIND_RX | `fixture.bind_rx.if0` | 19,429 | 0.194 | 20 | 20 | fits | 42,136 | 26 (77) | 0.804 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 11,088 | 0.111 | 20 | 20 | fits | 36,768 | 29 (35) | 0.785 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 15,645 | 0.156 | 20 | 20 | fits | 25,799 | 13 (29) | 0.813 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 83,386 | 0.834 | 20 | 200 | fits | 83,490 | 51 | 0.766 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 83,386 | 0.834 | 20 | 200 | fits | 83,490 | 51 | 0.766 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 83,112 | 0.831 | 20 | 20 | fits | 83,490 | 51 | 0.766 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 83,112 | 0.831 | 20 | 20 | fits | 83,490 | 51 | 0.766 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 83,320 | 0.833 | 20 | 24 | fits | 83,490 | 51 | 0.766 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 83,320 | 0.833 | 20 | 24 | fits | 83,490 | 51 | 0.766 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 83,254 | 0.833 | 20 | 50 | fits | 83,490 | 51 | 0.766 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 83,254 | 0.833 | 20 | 50 | fits | 83,490 | 51 | 0.766 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 83,188 | 0.832 | 20 | 20 | fits | 83,490 | 51 | 0.766 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 83,188 | 0.832 | 20 | 20 | fits | 83,490 | 51 | 0.766 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
