### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 98 paths and 7 of 968 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.181 (0.373) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.086 (0.202) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.081 (0.226) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.159 (0.430) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.102 (0.214) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.088 (0.200) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.092 (0.210) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.104 (0.231) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.094 (0.273) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.174 (0.449) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.135 (0.414) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.207 (0.589) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.053 (0.334) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.138 (0.467) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.126 (0.397) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.119 (0.332) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.043 (0.133) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.020 (0.116) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.025 (0.211) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.023 (0.224) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.119 (0.245) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.152 (0.387) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.171 (0.420) | fits | 0 aecp | 1 | 0 |
| get_as_path, refused ENTITY_MISBEHAVING | 0 | `aecp.get_as_path.if0` (aecp) | 0.115 (0.252) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.208 (0.470) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.190 (0.439) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.212 (0.470) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.214 (0.469) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR held for a token (#917) | 0 | `aecp.held.read_descriptor.if0` (aecp-held) | 5.142 (5.397) | fits | 16 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.149 (0.334) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.137 (0.375) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.246 (0.505) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.197 (0.451) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.191 (0.445) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.206 (0.458) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.213 (0.465) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.201 (0.454) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.180 (0.434) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.208 (0.463) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.188 (0.446) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.213 (0.468) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.187 (0.441) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.203 (0.365) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.196 (0.461) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.207 (0.460) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.148 (0.400) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.259 (0.623) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.169 (0.418) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.232 (0.551) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 3.170 (3.463) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.378 (0.646) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.526 (0.798) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.438 (0.700) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.418 (0.652) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.439 (0.720) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.424 (3.674) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.420 (0.656) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 2.698 (2.969) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.418 (2.729) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.730 (4.036) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.620 (3.927) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.304 (1.589) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.528 (3.721) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-7.adp_available.if0` (backlog-adp@blank-7) | 4.154 (5.502) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.077 (0.234) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.554 (1.911) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.555 (62.788) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.168 (63.274) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.307 (0.437) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 2.013 | fits | 11 acmp | 4 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-burst.held.adp.if0` (save-burst) | 1.537 | fits | 7 adp | 4 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-flight.held.aecp.if0` (save-flight) | 2.861 | fits | 14 aecp | 4 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 2.085 | fits | 6 maap | 4 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 7.510 | fits | 31 srp | 4 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.138 (0.392) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.090 (0.188) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.098 (0.224) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.119 (0.392) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.155 (0.415) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.345 | fits | 0 srp | 4 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@program-6.service.acmp.first.if0` (backlog-adp@program-6) | 3.780 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 61.813 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@program-6.service.adp.first.if0` (backlog-adp@program-6) | 3.771 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 4.678 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@program-6.service.aecp.first.if0` (backlog-adp@program-6) | 2.270 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.598 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@program-6.service.maap.first.if0` (backlog-adp@program-6) | 3.806 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.maap.last.if0` (backlog-adp@program-aged2-7) | 4.715 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-6.service.srp.first.if0` (backlog-adp@blank-aged2-6) | 5.531 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-3.service.srp.last.if0` (backlog-adp@program-aged2-3) | 9.092 | fits | 31 srp | 77 | 0 |
| Talker Advertise RX for every input, bound | 0 | `srp.bound_advertise.if0` (srp-bound) | 0.643 (0.644) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.714 (0.807) | fits | 0 srp | 1 | 0 |
| Talker Advertise RX for every input, no binding (kept) | 0 | `srp.kept_advertise.if0` (srp-kept) | 0.490 (0.491) | fits | 0 srp | 1 | 0 |
| Talker Failed RX for every input, no binding (kept) | 0 | `srp.kept_failed.if0` (srp-kept) | 0.522 (0.523) | fits | 0 srp | 1 | 0 |
| Talker RX at the bound after a freed block (count) | 0 | `srp.kept_recount.if0` (srp-kept) | 0.469 (0.470) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.350 (0.351) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.168 (0.169) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.695 (0.778) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.615 | 10 | 148,115 (1.481) | yes | - |
| backlog-adp@blank-1 | 0 | 11.490 | 10 | 148,115 (1.481) | yes | - |
| backlog-adp@blank-2 | 0 | 11.365 | 10 | 148,115 (1.481) | yes | - |
| backlog-adp@blank-3 | 0 | 11.240 | 10 | 148,115 (1.481) | yes | - |
| backlog-adp@blank-4 | 0 | 11.115 | 10 | 148,115 (1.481) | yes | - |
| backlog-adp@blank-5 | 0 | 10.990 | 10 | 148,115 (1.481) | yes | - |
| backlog-adp@blank-6 | 0 | 10.865 | 10 | 148,115 (1.481) | yes | - |
| backlog-adp@blank-7 | 0 | 14.599 | 13 | 146,945 (1.469) | yes | - |
| backlog-adp@program-0 | 0 | 9.649 | 10 | 146,142 (1.461) | yes | - |
| backlog-adp@program-1 | 0 | 10.297 | 10 | 146,018 (1.460) | yes | - |
| backlog-adp@program-2 | 0 | 11.510 | 12 | 146,336 (1.463) | yes | - |
| backlog-adp@program-3 | 0 | 11.260 | 12 | 146,336 (1.463) | yes | - |
| backlog-adp@program-4 | 0 | 11.010 | 12 | 146,336 (1.463) | yes | - |
| backlog-adp@program-5 | 0 | 10.775 | 11 | 145,286 (1.453) | yes | - |
| backlog-adp@program-6 | 0 | 11.576 | 12 | 146,182 (1.462) | yes | - |
| backlog-adp@program-7 | 0 | 11.326 | 12 | 146,182 (1.462) | yes | - |
| backlog-adp@verify-0 | 0 | 13.592 | 12 | 147,423 (1.474) | yes | - |
| backlog-adp@verify-1 | 0 | 13.467 | 12 | 147,423 (1.474) | yes | - |
| backlog-adp@verify-2 | 0 | 13.342 | 12 | 147,423 (1.474) | yes | - |
| backlog-adp@verify-3 | 0 | 13.217 | 12 | 147,423 (1.474) | yes | - |
| backlog-adp@verify-4 | 0 | 13.092 | 12 | 147,423 (1.474) | yes | - |
| backlog-adp@verify-5 | 0 | 12.967 | 12 | 147,423 (1.474) | yes | - |
| backlog-adp@verify-6 | 0 | 13.916 | 13 | 145,160 (1.452) | yes | - |
| backlog-adp@verify-7 | 0 | 12.754 | 12 | 145,665 (1.457) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 12.759 | 12 | 145,402 (1.454) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 11.987 | 12 | 144,048 (1.440) | yes | - |
| backlog-adp@blank-aged2-2 | 1 | 11.599 | 9 | 148,283 (1.483) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 11.666 | 10 | 148,358 (1.484) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 11.599 | 10 | 144,086 (1.441) | yes | - |
| backlog-adp@blank-aged2-5 | 1 | 11.534 | 9 | 144,245 (1.442) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 14.618 | 13 | 148,381 (1.484) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 13.720 | 13 | 146,390 (1.464) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 14.687 | 13 | 147,418 (1.474) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 13.739 | 12 | 143,498 (1.435) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 11.959 | 12 | 145,455 (1.455) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 10.888 | 10 | 144,134 (1.441) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 10.855 | 10 | 144,134 (1.441) | yes | - |
| backlog-adp@blank-aged1-5 | 1 | 10.846 | 9 | 148,160 (1.482) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 10.920 | 10 | 148,235 (1.482) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 10.835 | 10 | 146,671 (1.467) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 10.154 | 10 | 144,134 (1.441) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 10.184 | 10 | 144,152 (1.442) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 10.548 | 12 | 144,202 (1.442) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 10.387 | 10 | 148,263 (1.483) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 10.348 | 10 | 148,250 (1.482) | yes | - |
| backlog-adp@program-aged2-5 | 1 | 10.290 | 9 | 144,155 (1.442) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 10.368 | 10 | 147,280 (1.473) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 10.290 | 10 | 144,671 (1.447) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 10.188 | 10 | 144,086 (1.441) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.322 | 10 | 148,205 (1.482) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 10.275 | 10 | 148,329 (1.483) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 10.239 | 10 | 144,086 (1.441) | yes | - |
| backlog-adp@program-aged1-4 | 1 | 10.161 | 9 | 145,141 (1.451) | yes | - |
| backlog-adp@program-aged1-5 | 1 | 10.195 | 9 | 144,124 (1.441) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 10.304 | 10 | 148,250 (1.482) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 10.258 | 10 | 144,626 (1.446) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 12.885 | 12 | 145,471 (1.455) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 12.816 | 13 | 145,514 (1.455) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 10.804 | 10 | 144,134 (1.441) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 11.681 | 10 | 147,317 (1.473) | yes | - |
| backlog-adp@verify-aged2-4 | 1 | 11.631 | 9 | 143,318 (1.433) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 11.654 | 10 | 144,134 (1.441) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 14.665 | 13 | 144,134 (1.441) | yes | - |
| backlog-adp@verify-aged2-7 | 1 | 13.734 | 12 | 144,031 (1.440) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 14.773 | 13 | 144,134 (1.441) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 13.855 | 13 | 147,409 (1.474) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 11.954 | 12 | 144,271 (1.443) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 10.907 | 10 | 148,283 (1.483) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 10.867 | 9 | 143,318 (1.433) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 10.908 | 10 | 144,086 (1.441) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 10.899 | 10 | 147,330 (1.473) | yes | - |
| backlog-adp@verify-aged1-7 | 1 | 10.862 | 9 | 143,410 (1.434) | yes | - |
| backlog | 0 | 4.861 | 7 | 146,453 (1.465) | yes | - |
| backlog-adp | 0 | 8.618 | 10 | 147,938 (1.479) | yes | - |
| backlog-adp-refill | 0 | 40.596 | 24 | 147,938 (1.479) | yes | - |
| backlog-owed | 0 | 63.671 | 25 | 147,381 (1.474) | yes | - |
| fixture | 0 | 1.151 | 2 | 77,793 (0.778) | yes | - |

Composed maximum over the 4 backlog windows: 147,938 CPU cycles (1.479 ms), backlog-adp.
Over the windows that released their whole load only: 147,938 (1.479 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-kept | 1908 | 0 | 52,254 (0.523) | fits |
| save-flight | 2984 | 0 | 154,510 (1.545) | fits |
| save-burst | 2740 | 0 | 154,510 (1.545) | fits |
| acmp-notk | 3606 | 0 | 94,935 (0.949) | fits |
| save-second | 68900 | 0 | 45,529 (0.455) | fits |
| backlog-adp@blank-0 | 468 | 0 | 148,115 (1.481) | fits |
| backlog-adp@blank-1 | 468 | 0 | 148,115 (1.481) | fits |
| backlog-adp@blank-2 | 468 | 0 | 148,115 (1.481) | fits |
| backlog-adp@blank-3 | 468 | 0 | 148,115 (1.481) | fits |
| backlog-adp@blank-4 | 468 | 0 | 148,115 (1.481) | fits |
| backlog-adp@blank-5 | 468 | 0 | 148,115 (1.481) | fits |
| backlog-adp@blank-6 | 468 | 0 | 148,115 (1.481) | fits |
| backlog-adp@blank-7 | 471 | 0 | 146,945 (1.469) | fits |
| backlog-adp@program-0 | 476 | 0 | 146,142 (1.461) | fits |
| backlog-adp@program-1 | 476 | 0 | 146,018 (1.460) | fits |
| backlog-adp@program-2 | 478 | 0 | 146,336 (1.463) | fits |
| backlog-adp@program-3 | 478 | 0 | 146,336 (1.463) | fits |
| backlog-adp@program-4 | 478 | 0 | 146,336 (1.463) | fits |
| backlog-adp@program-5 | 478 | 0 | 145,286 (1.453) | fits |
| backlog-adp@program-6 | 478 | 0 | 146,182 (1.462) | fits |
| backlog-adp@program-7 | 478 | 0 | 146,182 (1.462) | fits |
| backlog-adp@verify-0 | 483 | 0 | 147,423 (1.474) | fits |
| backlog-adp@verify-1 | 483 | 0 | 147,423 (1.474) | fits |
| backlog-adp@verify-2 | 483 | 0 | 147,423 (1.474) | fits |
| backlog-adp@verify-3 | 483 | 0 | 147,423 (1.474) | fits |
| backlog-adp@verify-4 | 483 | 0 | 147,423 (1.474) | fits |
| backlog-adp@verify-5 | 483 | 0 | 147,423 (1.474) | fits |
| backlog-adp@verify-6 | 485 | 0 | 145,160 (1.452) | fits |
| backlog-adp@verify-7 | 484 | 0 | 145,665 (1.457) | fits |
| backlog-adp@blank-aged2-0 | 864 | 0 | 145,402 (1.454) | fits |
| backlog-adp@blank-aged2-1 | 876 | 0 | 144,070 (1.441) | fits |
| backlog-adp@blank-aged2-2 | 884 | 0 | 148,283 (1.483) | fits |
| backlog-adp@blank-aged2-3 | 896 | 0 | 148,358 (1.484) | fits |
| backlog-adp@blank-aged2-4 | 907 | 0 | 144,086 (1.441) | fits |
| backlog-adp@blank-aged2-5 | 918 | 0 | 144,245 (1.442) | fits |
| backlog-adp@blank-aged2-6 | 933 | 0 | 148,381 (1.484) | fits |
| backlog-adp@blank-aged2-7 | 944 | 0 | 146,390 (1.464) | fits |
| backlog-adp@blank-aged1-0 | 775 | 0 | 147,418 (1.474) | fits |
| backlog-adp@blank-aged1-1 | 786 | 0 | 144,086 (1.441) | fits |
| backlog-adp@blank-aged1-2 | 797 | 0 | 145,455 (1.455) | fits |
| backlog-adp@blank-aged1-3 | 806 | 0 | 144,134 (1.441) | fits |
| backlog-adp@blank-aged1-4 | 817 | 0 | 144,134 (1.441) | fits |
| backlog-adp@blank-aged1-5 | 828 | 0 | 148,160 (1.482) | fits |
| backlog-adp@blank-aged1-6 | 840 | 0 | 148,235 (1.482) | fits |
| backlog-adp@blank-aged1-7 | 851 | 0 | 146,671 (1.467) | fits |
| backlog-adp@program-aged2-0 | 911 | 0 | 144,134 (1.441) | fits |
| backlog-adp@program-aged2-1 | 923 | 0 | 144,152 (1.442) | fits |
| backlog-adp@program-aged2-2 | 936 | 0 | 144,202 (1.442) | fits |
| backlog-adp@program-aged2-3 | 945 | 0 | 148,263 (1.483) | fits |
| backlog-adp@program-aged2-4 | 956 | 0 | 148,250 (1.482) | fits |
| backlog-adp@program-aged2-5 | 967 | 0 | 144,155 (1.442) | fits |
| backlog-adp@program-aged2-6 | 979 | 0 | 147,280 (1.473) | fits |
| backlog-adp@program-aged2-7 | 990 | 0 | 144,671 (1.447) | fits |
| backlog-adp@program-aged1-0 | 821 | 0 | 144,086 (1.441) | fits |
| backlog-adp@program-aged1-1 | 833 | 0 | 148,205 (1.482) | fits |
| backlog-adp@program-aged1-2 | 844 | 0 | 148,329 (1.483) | fits |
| backlog-adp@program-aged1-3 | 855 | 0 | 144,086 (1.441) | fits |
| backlog-adp@program-aged1-4 | 866 | 0 | 145,141 (1.451) | fits |
| backlog-adp@program-aged1-5 | 877 | 0 | 144,134 (1.441) | fits |
| backlog-adp@program-aged1-6 | 889 | 0 | 148,250 (1.482) | fits |
| backlog-adp@program-aged1-7 | 900 | 0 | 144,626 (1.446) | fits |
| backlog-adp@verify-aged2-0 | 849 | 0 | 145,471 (1.455) | fits |
| backlog-adp@verify-aged2-1 | 861 | 0 | 145,514 (1.455) | fits |
| backlog-adp@verify-aged2-2 | 869 | 0 | 144,134 (1.441) | fits |
| backlog-adp@verify-aged2-3 | 880 | 0 | 147,317 (1.473) | fits |
| backlog-adp@verify-aged2-4 | 891 | 0 | 144,134 (1.441) | fits |
| backlog-adp@verify-aged2-5 | 903 | 0 | 144,134 (1.441) | fits |
| backlog-adp@verify-aged2-6 | 917 | 0 | 144,134 (1.441) | fits |
| backlog-adp@verify-aged2-7 | 928 | 0 | 144,170 (1.442) | fits |
| backlog-adp@verify-aged1-0 | 760 | 0 | 144,134 (1.441) | fits |
| backlog-adp@verify-aged1-1 | 771 | 0 | 147,409 (1.474) | fits |
| backlog-adp@verify-aged1-2 | 781 | 0 | 144,271 (1.443) | fits |
| backlog-adp@verify-aged1-3 | 790 | 0 | 148,283 (1.483) | fits |
| backlog-adp@verify-aged1-4 | 801 | 0 | 144,086 (1.441) | fits |
| backlog-adp@verify-aged1-5 | 813 | 0 | 144,086 (1.441) | fits |
| backlog-adp@verify-aged1-6 | 824 | 0 | 147,330 (1.473) | fits |
| backlog-adp@verify-aged1-7 | 835 | 0 | 144,086 (1.441) | fits |
| adp-advertise | 599 | 0 | 28,356 (0.284) | fits |
| save-held | 1406 | 0 | 154,510 (1.545) | fits |
| save-starved | 37166 | 0 | 154,510 (1.545) | fits |
| srp-bound | 1225 | 0 | 98,026 (0.980) | fits |
| acmp-noresp | 2026 | 0 | 94,509 (0.945) | fits |
| save | 610 | 0 | 42,060 (0.421) | fits |
| srp | 290 | 0 | 49,321 (0.493) | fits |
| backlog | 286 | 0 | 146,453 (1.465) | fits |
| backlog-adp | 312 | 0 | 147,938 (1.479) | fits |
| backlog-adp-refill | 326 | 0 | 147,938 (1.479) | fits |
| backlog-owed | 310 | 0 | 147,381 (1.474) | fits |
| acmp-disc | 937 | 0 | 93,621 (0.936) | fits |
| maap | 178 | 0 | 28,356 (0.284) | fits |
| adp-link | 90 | 0 | 31,579 (0.316) | fits |
| adp-gm | 89 | 0 | 28,356 (0.284) | fits |
| adp-discover | 89 | 0 | 28,356 (0.284) | fits |
| control | 89 | 0 | 28,356 (0.284) | fits |
| aecp-fanout | 112 | 0 | 59,848 (0.598) | fits |
| acmp-cmd | 85 | 0 | 36,701 (0.367) | fits |
| aecp | 114 | 0 | 42,113 (0.421) | fits |
| aecp-largest-notice | 107 | 0 | 142,061 (1.421) | fits |
| aecp-held | 109 | 0 | 30,333 (0.303) | fits |
| datapath-events | 119 | 0 | 28,356 (0.284) | fits |
| fixture | 151 | 0 | 77,793 (0.778) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 8.059 (20) | 11.941 |
| backlog-adp@blank-aged2-1 | 2 | none | none | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 8.050 (20) | 11.950 |
| backlog-adp@blank-aged2-2 | 2 | +7.961 ms, 76,553 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 8.947 (20) | 11.053 |
| backlog-adp@blank-aged2-3 | 2 | +7.271 ms, 76,553 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 9.015 (20) | 10.985 |
| backlog-adp@blank-aged2-4 | 2 | +5.488 ms, 76,491 (0.765 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 8.949 (20) | 11.051 |
| backlog-adp@blank-aged2-5 | 2 | +4.653 ms, 76,808 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 8.881 (20) | 11.119 |
| backlog-adp@blank-aged2-6 | 2 | +3.976 ms, 76,898 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 9.002 (20) | 10.998 |
| backlog-adp@blank-aged2-7 | 2 | +3.030 ms, 76,564 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 8.926 (20) | 11.074 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 8.166 (20) | 11.834 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 8.111 (20) | 11.889 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 8.160 (20) | 11.840 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 8.083 (20) | 11.917 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 8.199 (20) | 11.801 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 8.190 (20) | 11.810 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 8.263 (20) | 11.737 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 8.172 (20) | 11.828 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 8.106 (20) | 11.894 |
| backlog-adp@program-aged2-1 | 2 | none | +8.281 ms, 80,333 (0.803 ms), issue | `backlog-adp@program-aged2-1.service.srp.last.if0` | 8.094 (20) | 11.906 |
| backlog-adp@program-aged2-2 | 2 | +7.741 ms, 80,711 (0.807 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 8.987 (20) | 11.013 |
| backlog-adp@program-aged2-3 | 2 | +7.099 ms, 80,711 (0.807 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 9.092 (20) | 10.908 |
| backlog-adp@program-aged2-4 | 2 | +5.549 ms, 80,711 (0.807 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 9.052 (20) | 10.948 |
| backlog-adp@program-aged2-5 | 2 | +4.508 ms, 80,800 (0.808 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 8.992 (20) | 11.008 |
| backlog-adp@program-aged2-6 | 2 | +3.800 ms, 80,782 (0.808 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 9.071 (20) | 10.929 |
| backlog-adp@program-aged2-7 | 2 | none | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 8.984 (20) | 11.016 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 8.144 (20) | 11.856 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 8.148 (20) | 11.852 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 8.223 (20) | 11.777 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 8.186 (20) | 11.814 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 8.108 (20) | 11.892 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 8.150 (20) | 11.850 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 8.258 (20) | 11.742 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 8.211 (20) | 11.789 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 8.130 (20) | 11.870 |
| backlog-adp@verify-aged2-1 | 2 | none | +8.279 ms, 77,269 (0.773 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 8.091 (20) | 11.909 |
| backlog-adp@verify-aged2-2 | 2 | none | +8.250 ms, 77,485 (0.775 ms), read-back | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 8.213 (20) | 11.787 |
| backlog-adp@verify-aged2-3 | 2 | +7.238 ms, 77,486 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 8.993 (20) | 11.007 |
| backlog-adp@verify-aged2-4 | 2 | +5.471 ms, 77,424 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 8.946 (20) | 11.054 |
| backlog-adp@verify-aged2-5 | 2 | +4.726 ms, 77,741 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 8.965 (20) | 11.035 |
| backlog-adp@verify-aged2-6 | 2 | +3.943 ms, 77,831 (0.778 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 8.977 (20) | 11.023 |
| backlog-adp@verify-aged2-7 | 2 | +3.851 ms, 77,831 (0.778 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 8.883 (20) | 11.117 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 8.167 (20) | 11.833 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 8.162 (20) | 11.838 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 8.113 (20) | 11.887 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 8.219 (20) | 11.781 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 8.180 (20) | 11.820 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 8.222 (20) | 11.778 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 8.212 (20) | 11.788 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 8.168 (20) | 11.832 |

Least margin over the aged windows: 10.908 ms, `backlog-adp@program-aged2-3.service.srp.last.if0` at 9.092 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.384 | 6,070 | 102 | 2 | 30.766 | yes | within |
| save-held | 1084.026 | 4,070 | 102 | - | 22.179 | no | within |
| save-starved | 4048.241 | 4,070 | 102 | - | 31.313 | yes | within |
| save | 1075.754 | 4,070 | 102 | - | 24.214 | no | within |

Names from their response to durable (save_burst.py; #920, #665's ruling of 2026-11-15, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-flight | 1 | 146.789 (0) | 5,000 | 2 | - | - | 19 steps (want 19), 5.944 ms | within |
| save-burst | 39 | 1097.264 (0) | 5,000 | 1 | - | - | sequence 1, 0 missing | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-kept | 1844 | 18,872 (0.189) | 2,610 (0.026) |
| save-flight | 1554 | 91,674 (0.917) | 78,578 (0.786) |
| save-burst | 1480 | 90,387 (0.904) | 78,058 (0.781) |
| acmp-notk | 1159 | 94,935 (0.949) | 78,155 (0.782) |
| save-second | 520 | 79,904 (0.799) | 78,102 (0.781) |
| backlog-adp@blank-0 | 342 | 88,902 (0.889) | 76,009 (0.760) |
| backlog-adp@blank-1 | 342 | 88,902 (0.889) | 76,009 (0.760) |
| backlog-adp@blank-2 | 342 | 88,902 (0.889) | 76,009 (0.760) |
| backlog-adp@blank-3 | 342 | 88,902 (0.889) | 76,009 (0.760) |
| backlog-adp@blank-4 | 342 | 88,902 (0.889) | 76,009 (0.760) |
| backlog-adp@blank-5 | 342 | 88,902 (0.889) | 76,009 (0.760) |
| backlog-adp@blank-6 | 342 | 88,902 (0.889) | 76,009 (0.760) |
| backlog-adp@blank-7 | 346 | 89,871 (0.899) | 76,009 (0.760) |
| backlog-adp@program-0 | 371 | 91,412 (0.914) | 78,086 (0.781) |
| backlog-adp@program-1 | 372 | 93,346 (0.933) | 78,765 (0.788) |
| backlog-adp@program-2 | 375 | 91,473 (0.915) | 78,086 (0.781) |
| backlog-adp@program-3 | 375 | 91,473 (0.915) | 78,086 (0.781) |
| backlog-adp@program-4 | 375 | 91,473 (0.915) | 78,086 (0.781) |
| backlog-adp@program-5 | 375 | 91,473 (0.915) | 78,086 (0.781) |
| backlog-adp@program-6 | 377 | 91,285 (0.913) | 78,086 (0.781) |
| backlog-adp@program-7 | 377 | 91,285 (0.913) | 78,086 (0.781) |
| backlog-adp@verify-0 | 400 | 91,167 (0.912) | 78,086 (0.781) |
| backlog-adp@verify-1 | 400 | 91,167 (0.912) | 78,086 (0.781) |
| backlog-adp@verify-2 | 400 | 91,167 (0.912) | 78,086 (0.781) |
| backlog-adp@verify-3 | 400 | 91,167 (0.912) | 78,086 (0.781) |
| backlog-adp@verify-4 | 400 | 91,167 (0.912) | 78,086 (0.781) |
| backlog-adp@verify-5 | 400 | 91,167 (0.912) | 78,086 (0.781) |
| backlog-adp@verify-6 | 401 | 91,167 (0.912) | 78,086 (0.781) |
| backlog-adp@verify-7 | 400 | 91,167 (0.912) | 78,086 (0.781) |
| backlog-adp@blank-aged2-0 | 341 | 89,902 (0.899) | 76,233 (0.762) |
| backlog-adp@blank-aged2-1 | 340 | 89,902 (0.899) | 76,233 (0.762) |
| backlog-adp@blank-aged2-2 | 340 | 88,228 (0.882) | 75,823 (0.758) |
| backlog-adp@blank-aged2-3 | 340 | 88,256 (0.883) | 75,823 (0.758) |
| backlog-adp@blank-aged2-4 | 340 | 88,118 (0.881) | 75,821 (0.758) |
| backlog-adp@blank-aged2-5 | 340 | 88,391 (0.884) | 75,823 (0.758) |
| backlog-adp@blank-aged2-6 | 343 | 95,122 (0.951) | 75,913 (0.759) |
| backlog-adp@blank-aged2-7 | 342 | 87,286 (0.873) | 76,028 (0.760) |
| backlog-adp@blank-aged1-0 | 343 | 89,824 (0.898) | 76,233 (0.762) |
| backlog-adp@blank-aged1-1 | 342 | 95,172 (0.952) | 76,147 (0.761) |
| backlog-adp@blank-aged1-2 | 340 | 89,985 (0.900) | 76,233 (0.762) |
| backlog-adp@blank-aged1-3 | 339 | 91,476 (0.915) | 76,098 (0.761) |
| backlog-adp@blank-aged1-4 | 339 | 88,718 (0.887) | 76,233 (0.762) |
| backlog-adp@blank-aged1-5 | 339 | 88,736 (0.887) | 76,233 (0.762) |
| backlog-adp@blank-aged1-6 | 339 | 88,717 (0.887) | 76,233 (0.762) |
| backlog-adp@blank-aged1-7 | 339 | 89,291 (0.893) | 76,233 (0.762) |
| backlog-adp@program-aged2-0 | 368 | 92,872 (0.929) | 78,704 (0.787) |
| backlog-adp@program-aged2-1 | 368 | 91,112 (0.911) | 78,352 (0.784) |
| backlog-adp@program-aged2-2 | 369 | 91,071 (0.911) | 78,499 (0.785) |
| backlog-adp@program-aged2-3 | 369 | 91,061 (0.911) | 78,499 (0.785) |
| backlog-adp@program-aged2-4 | 369 | 91,056 (0.911) | 78,499 (0.785) |
| backlog-adp@program-aged2-5 | 369 | 91,265 (0.913) | 78,499 (0.785) |
| backlog-adp@program-aged2-6 | 369 | 91,176 (0.912) | 78,495 (0.785) |
| backlog-adp@program-aged2-7 | 369 | 91,356 (0.914) | 78,605 (0.786) |
| backlog-adp@program-aged1-0 | 368 | 92,571 (0.926) | 78,704 (0.787) |
| backlog-adp@program-aged1-1 | 368 | 91,393 (0.914) | 78,618 (0.786) |
| backlog-adp@program-aged1-2 | 368 | 93,130 (0.931) | 78,704 (0.787) |
| backlog-adp@program-aged1-3 | 368 | 93,294 (0.933) | 78,765 (0.788) |
| backlog-adp@program-aged1-4 | 368 | 93,199 (0.932) | 78,765 (0.788) |
| backlog-adp@program-aged1-5 | 368 | 92,637 (0.926) | 78,671 (0.787) |
| backlog-adp@program-aged1-6 | 368 | 92,722 (0.927) | 78,704 (0.787) |
| backlog-adp@program-aged1-7 | 368 | 92,722 (0.927) | 78,704 (0.787) |
| backlog-adp@verify-aged2-0 | 400 | 91,167 (0.912) | 78,086 (0.781) |
| backlog-adp@verify-aged2-1 | 400 | 98,631 (0.986) | 78,086 (0.781) |
| backlog-adp@verify-aged2-2 | 398 | 91,167 (0.912) | 78,086 (0.781) |
| backlog-adp@verify-aged2-3 | 399 | 91,167 (0.912) | 78,086 (0.781) |
| backlog-adp@verify-aged2-4 | 399 | 91,167 (0.912) | 78,086 (0.781) |
| backlog-adp@verify-aged2-5 | 399 | 91,167 (0.912) | 78,086 (0.781) |
| backlog-adp@verify-aged2-6 | 402 | 96,568 (0.966) | 78,086 (0.781) |
| backlog-adp@verify-aged2-7 | 401 | 91,167 (0.912) | 78,086 (0.781) |
| backlog-adp@verify-aged1-0 | 402 | 91,167 (0.912) | 78,086 (0.781) |
| backlog-adp@verify-aged1-1 | 401 | 96,404 (0.964) | 78,086 (0.781) |
| backlog-adp@verify-aged1-2 | 399 | 91,167 (0.912) | 78,086 (0.781) |
| backlog-adp@verify-aged1-3 | 398 | 91,167 (0.912) | 78,086 (0.781) |
| backlog-adp@verify-aged1-4 | 398 | 91,167 (0.912) | 78,086 (0.781) |
| backlog-adp@verify-aged1-5 | 398 | 91,167 (0.912) | 78,086 (0.781) |
| backlog-adp@verify-aged1-6 | 398 | 91,167 (0.912) | 78,086 (0.781) |
| backlog-adp@verify-aged1-7 | 398 | 91,167 (0.912) | 78,086 (0.781) |
| adp-advertise | 578 | 18,711 (0.187) | 2,610 (0.026) |
| save-held | 816 | 90,498 (0.905) | 78,119 (0.781) |
| save-starved | 418 | 80,568 (0.806) | 78,238 (0.782) |
| srp-bound | 582 | 98,026 (0.980) | 78,252 (0.783) |
| acmp-noresp | 709 | 94,509 (0.945) | 78,155 (0.782) |
| save | 680 | 90,314 (0.903) | 77,824 (0.778) |
| srp | 271 | 18,711 (0.187) | 2,610 (0.026) |
| backlog | 265 | 18,711 (0.187) | 2,610 (0.026) |
| backlog-adp | 271 | 18,711 (0.187) | 2,610 (0.026) |
| backlog-adp-refill | 274 | 18,711 (0.187) | 2,610 (0.026) |
| backlog-owed | 276 | 18,711 (0.187) | 2,610 (0.026) |
| acmp-disc | 399 | 93,621 (0.936) | 78,155 (0.782) |
| maap | 165 | 18,519 (0.185) | 2,610 (0.026) |
| adp-link | 80 | 18,519 (0.185) | 2,610 (0.026) |
| adp-gm | 80 | 18,519 (0.185) | 2,610 (0.026) |
| adp-discover | 80 | 18,519 (0.185) | 2,610 (0.026) |
| control | 80 | 18,519 (0.185) | 2,610 (0.026) |
| aecp-fanout | 80 | 18,519 (0.185) | 2,610 (0.026) |
| acmp-cmd | 65 | 18,519 (0.185) | 2,610 (0.026) |
| aecp | 80 | 18,519 (0.185) | 2,610 (0.026) |
| aecp-largest-notice | 78 | 18,519 (0.185) | 2,610 (0.026) |
| aecp-held | 98 | 18,519 (0.185) | 2,610 (0.026) |
| datapath-events | 70 | 18,519 (0.185) | 2,610 (0.026) |
| fixture | 54 | 13,943 (0.139) | 2,610 (0.026) |

Longest pass that carries a step: 98,631 CPU cycles (0.986 ms), backlog-adp@verify-aged2-1; longest step: 78,765 (0.788 ms), backlog-adp@program-1.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| Talker Advertise RX for every input, no binding (kept) | `srp.kept_advertise.if0` | 48,986 | 0.490 | 20 | 20 | fits | 49,052 | 12 | 0.892 |
| Talker RX at the bound after a freed block (count) | `srp.kept_recount.if0` | 46,924 | 0.469 | 20 | 20 | fits | 46,990 | 12 | 0.892 |
| Talker Failed RX for every input, no binding (kept) | `srp.kept_failed.if0` | 52,188 | 0.522 | 20 | 20 | fits | 52,254 | 12 | 0.898 |
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 153,570 | 1.536 | 20 | 200 | fits | 154,510 | 259 | 0.366 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 188,755 | 1.888 | 20 | 20 | fits | 139,028 | 264 | 0.202 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 286,141 | 2.861 | 20 | 24 | fits | 80,817 | 47 | 0.587 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 208,494 | 2.085 | 20 | 50 | fits | 91,563 | 202 | 0.319 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 724,297 | 7.243 | 20 | 20 | fits | 40,877 | 22 | 0.779 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 76,210 | 0.762 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-burst.held.adp.if0` | 153,701 | 1.537 | 20 | 200 | fits | 154,510 | 259 | 0.366 |
| ACMP record, every channel at its refill rate, the longest | `save-burst.held.acmp.if0` | 187,088 | 1.871 | 20 | 20 | fits | 139,203 | 264 | 0.204 |
| AECP record, every channel at its refill rate, the longest | `save-burst.held.aecp.if0` | 150,480 | 1.505 | 20 | 24 | fits | 84,226 | 34 | 0.758 |
| MAAP record, every channel at its refill rate, the longest | `save-burst.held.maap.if0` | 188,510 | 1.885 | 20 | 50 | fits | 94,552 | 86 | 0.693 |
| SRP record, every channel at its refill rate, the longest | `save-burst.held.srp.if0` | 656,275 | 6.563 | 20 | 20 | fits | 72,838 | 35 | 0.731 |
| an MRPDU its periodic timer owes, the longest | `save-burst.mrpdu.periodic.if0` | 226,110 | 2.261 | 49 | 49 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 13,814 | 0.138 | 20 | 20 | fits | 27,938 | 19 (14) | 0.866 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 415,249 | 4.152 | 20 | 20 | fits | 86,499 | 124 | 0.455 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 366,905 | 3.669 | 20 | 200 | fits | 148,115 | 267 | 0.325 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 464,483 | 4.645 | 20 | 200 | fits | 86,499 | 124 | 0.455 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 367,829 | 3.678 | 20 | 20 | fits | 148,115 | 267 | 0.325 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 465,187 | 4.652 | 20 | 20 | fits | 86,499 | 124 | 0.455 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 223,354 | 2.234 | 20 | 24 | fits | 146,165 | 164 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 370,479 | 3.705 | 20 | 24 | fits | 148,115 | 267 | 0.325 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 370,413 | 3.704 | 20 | 50 | fits | 148,115 | 267 | 0.325 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 468,211 | 4.682 | 20 | 50 | fits | 86,499 | 124 | 0.455 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 548,099 | 5.481 | 20 | 20 | fits | 79,954 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 895,524 | 8.955 | 20 | 20 | fits | 45,593 | 20 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 402,749 | 4.027 | 20 | 20 | fits | 86,499 | 124 | 0.455 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 354,405 | 3.544 | 20 | 200 | fits | 148,115 | 267 | 0.325 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 451,983 | 4.520 | 20 | 200 | fits | 86,499 | 124 | 0.455 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 355,329 | 3.553 | 20 | 20 | fits | 148,115 | 267 | 0.325 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 452,687 | 4.527 | 20 | 20 | fits | 86,499 | 124 | 0.455 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 210,854 | 2.109 | 20 | 24 | fits | 146,165 | 164 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 357,979 | 3.580 | 20 | 24 | fits | 148,115 | 267 | 0.325 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 357,913 | 3.579 | 20 | 50 | fits | 148,115 | 267 | 0.325 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 455,711 | 4.557 | 20 | 50 | fits | 86,499 | 124 | 0.455 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 535,599 | 5.356 | 20 | 20 | fits | 79,954 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 883,024 | 8.830 | 20 | 20 | fits | 45,593 | 20 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 390,249 | 3.902 | 20 | 20 | fits | 86,499 | 124 | 0.455 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 341,905 | 3.419 | 20 | 200 | fits | 148,115 | 267 | 0.325 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 439,483 | 4.395 | 20 | 200 | fits | 86,499 | 124 | 0.455 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 342,829 | 3.428 | 20 | 20 | fits | 148,115 | 267 | 0.325 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 440,187 | 4.402 | 20 | 20 | fits | 86,499 | 124 | 0.455 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 198,354 | 1.984 | 20 | 24 | fits | 146,165 | 164 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 345,479 | 3.455 | 20 | 24 | fits | 148,115 | 267 | 0.325 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 345,413 | 3.454 | 20 | 50 | fits | 148,115 | 267 | 0.325 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 443,211 | 4.432 | 20 | 50 | fits | 86,499 | 124 | 0.455 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 523,099 | 5.231 | 20 | 20 | fits | 79,954 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 870,524 | 8.705 | 20 | 20 | fits | 45,593 | 20 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 377,749 | 3.777 | 20 | 20 | fits | 86,499 | 124 | 0.455 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 329,405 | 3.294 | 20 | 200 | fits | 148,115 | 267 | 0.325 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 426,983 | 4.270 | 20 | 200 | fits | 86,499 | 124 | 0.455 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 330,329 | 3.303 | 20 | 20 | fits | 148,115 | 267 | 0.325 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 427,687 | 4.277 | 20 | 20 | fits | 86,499 | 124 | 0.455 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 185,854 | 1.859 | 20 | 24 | fits | 146,165 | 164 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 332,979 | 3.330 | 20 | 24 | fits | 148,115 | 267 | 0.325 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 332,913 | 3.329 | 20 | 50 | fits | 148,115 | 267 | 0.325 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 430,711 | 4.307 | 20 | 50 | fits | 86,499 | 124 | 0.455 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 510,599 | 5.106 | 20 | 20 | fits | 79,954 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 858,024 | 8.580 | 20 | 20 | fits | 45,593 | 20 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 365,249 | 3.652 | 20 | 20 | fits | 86,499 | 124 | 0.455 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 316,905 | 3.169 | 20 | 200 | fits | 148,115 | 267 | 0.325 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 414,483 | 4.145 | 20 | 200 | fits | 86,499 | 124 | 0.455 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 317,829 | 3.178 | 20 | 20 | fits | 148,115 | 267 | 0.325 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 415,187 | 4.152 | 20 | 20 | fits | 86,499 | 124 | 0.455 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 173,354 | 1.734 | 20 | 24 | fits | 146,165 | 164 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 320,479 | 3.205 | 20 | 24 | fits | 148,115 | 267 | 0.325 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 320,413 | 3.204 | 20 | 50 | fits | 148,115 | 267 | 0.325 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 418,211 | 4.182 | 20 | 50 | fits | 86,499 | 124 | 0.455 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 498,099 | 4.981 | 20 | 20 | fits | 79,954 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 845,524 | 8.455 | 20 | 20 | fits | 45,593 | 20 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 352,749 | 3.527 | 20 | 20 | fits | 86,499 | 124 | 0.455 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 304,405 | 3.044 | 20 | 200 | fits | 148,115 | 267 | 0.325 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 401,983 | 4.020 | 20 | 200 | fits | 86,499 | 124 | 0.455 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 305,329 | 3.053 | 20 | 20 | fits | 148,115 | 267 | 0.325 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 402,687 | 4.027 | 20 | 20 | fits | 86,499 | 124 | 0.455 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 160,854 | 1.609 | 20 | 24 | fits | 146,165 | 164 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 307,979 | 3.080 | 20 | 24 | fits | 148,115 | 267 | 0.325 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 307,913 | 3.079 | 20 | 50 | fits | 148,115 | 267 | 0.325 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 405,711 | 4.057 | 20 | 50 | fits | 86,499 | 124 | 0.455 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 485,599 | 4.856 | 20 | 20 | fits | 79,954 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 833,024 | 8.330 | 20 | 20 | fits | 45,593 | 20 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 340,249 | 3.402 | 20 | 20 | fits | 86,499 | 124 | 0.455 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 291,905 | 2.919 | 20 | 200 | fits | 148,115 | 267 | 0.325 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 389,483 | 3.895 | 20 | 200 | fits | 86,499 | 124 | 0.455 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 292,829 | 2.928 | 20 | 20 | fits | 148,115 | 267 | 0.325 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 390,187 | 3.902 | 20 | 20 | fits | 86,499 | 124 | 0.455 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 148,354 | 1.484 | 20 | 24 | fits | 146,165 | 164 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 295,479 | 2.955 | 20 | 24 | fits | 148,115 | 267 | 0.325 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 295,413 | 2.954 | 20 | 50 | fits | 148,115 | 267 | 0.325 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 393,211 | 3.932 | 20 | 50 | fits | 86,499 | 124 | 0.455 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 473,099 | 4.731 | 20 | 20 | fits | 79,954 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 820,524 | 8.205 | 20 | 20 | fits | 45,593 | 20 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 415,372 | 4.154 | 20 | 20 | fits | 87,110 | 127 | 0.436 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 364,770 | 3.648 | 20 | 200 | fits | 146,945 | 263 | 0.330 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 462,959 | 4.630 | 20 | 200 | fits | 87,110 | 127 | 0.436 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 365,694 | 3.657 | 20 | 20 | fits | 146,945 | 263 | 0.330 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 463,663 | 4.637 | 20 | 20 | fits | 87,110 | 127 | 0.436 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 222,389 | 2.224 | 20 | 24 | fits | 146,165 | 164 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 368,344 | 3.683 | 20 | 24 | fits | 146,945 | 263 | 0.330 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 368,278 | 3.683 | 20 | 50 | fits | 146,945 | 263 | 0.330 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 466,687 | 4.667 | 20 | 50 | fits | 87,110 | 127 | 0.436 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 546,520 | 5.465 | 20 | 20 | fits | 79,899 | 28 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 893,265 | 8.933 | 20 | 20 | fits | 45,444 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 323,851 | 3.239 | 20 | 20 | fits | 86,695 | 125 | 0.456 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 300,855 | 3.009 | 20 | 200 | fits | 143,665 | 262 | 0.322 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 398,434 | 3.984 | 20 | 200 | fits | 86,695 | 125 | 0.456 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 301,779 | 3.018 | 20 | 20 | fits | 143,665 | 262 | 0.322 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 399,138 | 3.991 | 20 | 20 | fits | 86,695 | 125 | 0.456 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 161,754 | 1.618 | 20 | 24 | fits | 146,142 | 164 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 304,429 | 3.044 | 20 | 24 | fits | 143,665 | 262 | 0.322 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 304,363 | 3.044 | 20 | 50 | fits | 143,665 | 262 | 0.322 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 402,162 | 4.022 | 20 | 50 | fits | 86,695 | 125 | 0.456 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 482,139 | 4.821 | 20 | 20 | fits | 80,043 | 28 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 834,246 | 8.342 | 20 | 20 | fits | 45,443 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 338,795 | 3.388 | 20 | 20 | fits | 83,303 | 118 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 293,897 | 2.939 | 20 | 200 | fits | 144,945 | 267 | 0.312 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 388,005 | 3.880 | 20 | 200 | fits | 83,303 | 118 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 294,821 | 2.948 | 20 | 20 | fits | 144,945 | 267 | 0.312 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 388,709 | 3.887 | 20 | 20 | fits | 83,303 | 118 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 153,516 | 1.535 | 20 | 24 | fits | 146,018 | 164 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 297,471 | 2.975 | 20 | 24 | fits | 144,945 | 267 | 0.312 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 297,405 | 2.974 | 20 | 50 | fits | 144,945 | 267 | 0.312 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 391,733 | 3.917 | 20 | 50 | fits | 83,303 | 118 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 471,825 | 4.718 | 20 | 20 | fits | 80,158 | 28 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 823,921 | 8.239 | 20 | 20 | fits | 45,485 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 404,055 | 4.041 | 20 | 20 | fits | 81,151 | 121 | 0.343 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 369,473 | 3.695 | 20 | 200 | fits | 144,265 | 262 | 0.336 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 450,008 | 4.500 | 20 | 200 | fits | 81,151 | 121 | 0.343 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 370,397 | 3.704 | 20 | 20 | fits | 144,265 | 262 | 0.336 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 450,712 | 4.507 | 20 | 20 | fits | 81,151 | 121 | 0.343 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 219,611 | 2.196 | 20 | 24 | fits | 146,336 | 165 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 373,047 | 3.730 | 20 | 24 | fits | 144,265 | 262 | 0.336 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 372,981 | 3.730 | 20 | 50 | fits | 144,265 | 262 | 0.336 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 453,736 | 4.537 | 20 | 50 | fits | 81,151 | 121 | 0.343 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 533,575 | 5.336 | 20 | 20 | fits | 79,905 | 28 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 885,403 | 8.854 | 20 | 20 | fits | 45,444 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 379,055 | 3.791 | 20 | 20 | fits | 81,151 | 121 | 0.343 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 344,473 | 3.445 | 20 | 200 | fits | 144,265 | 262 | 0.336 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 425,008 | 4.250 | 20 | 200 | fits | 81,151 | 121 | 0.343 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 345,397 | 3.454 | 20 | 20 | fits | 144,265 | 262 | 0.336 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 425,712 | 4.257 | 20 | 20 | fits | 81,151 | 121 | 0.343 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 194,611 | 1.946 | 20 | 24 | fits | 146,336 | 165 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 348,047 | 3.480 | 20 | 24 | fits | 144,265 | 262 | 0.336 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 347,981 | 3.480 | 20 | 50 | fits | 144,265 | 262 | 0.336 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 428,736 | 4.287 | 20 | 50 | fits | 81,151 | 121 | 0.343 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 508,575 | 5.086 | 20 | 20 | fits | 79,905 | 28 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 860,403 | 8.604 | 20 | 20 | fits | 45,444 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 354,055 | 3.541 | 20 | 20 | fits | 81,151 | 121 | 0.343 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 319,473 | 3.195 | 20 | 200 | fits | 144,265 | 262 | 0.336 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 400,008 | 4.000 | 20 | 200 | fits | 81,151 | 121 | 0.343 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 320,397 | 3.204 | 20 | 20 | fits | 144,265 | 262 | 0.336 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 400,712 | 4.007 | 20 | 20 | fits | 81,151 | 121 | 0.343 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 169,611 | 1.696 | 20 | 24 | fits | 146,336 | 165 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 323,047 | 3.230 | 20 | 24 | fits | 144,265 | 262 | 0.336 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 322,981 | 3.230 | 20 | 50 | fits | 144,265 | 262 | 0.336 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 403,736 | 4.037 | 20 | 50 | fits | 81,151 | 121 | 0.343 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 483,575 | 4.836 | 20 | 20 | fits | 79,905 | 28 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 835,403 | 8.354 | 20 | 20 | fits | 45,444 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 330,083 | 3.301 | 20 | 20 | fits | 90,577 | 168 | 0.347 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 286,453 | 2.865 | 20 | 200 | fits | 145,286 | 266 | 0.343 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 376,414 | 3.764 | 20 | 200 | fits | 90,577 | 168 | 0.347 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 287,377 | 2.874 | 20 | 20 | fits | 145,286 | 266 | 0.343 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 377,118 | 3.771 | 20 | 20 | fits | 90,577 | 168 | 0.347 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 135,606 | 1.356 | 20 | 24 | fits | 137,331 | 115 | 0.397 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 290,027 | 2.900 | 20 | 24 | fits | 145,286 | 266 | 0.343 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 289,961 | 2.900 | 20 | 50 | fits | 145,286 | 266 | 0.343 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 380,142 | 3.801 | 20 | 50 | fits | 90,577 | 168 | 0.347 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 460,013 | 4.600 | 20 | 20 | fits | 79,937 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 811,908 | 8.119 | 20 | 20 | fits | 45,444 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 385,838 | 3.858 | 20 | 20 | fits | 82,500 | 106 | 0.356 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 377,107 | 3.771 | 20 | 200 | fits | 144,438 | 281 | 0.329 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 458,991 | 4.590 | 20 | 200 | fits | 82,500 | 106 | 0.356 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 378,031 | 3.780 | 20 | 20 | fits | 144,438 | 281 | 0.329 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 459,695 | 4.597 | 20 | 20 | fits | 82,500 | 106 | 0.356 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 227,039 | 2.270 | 20 | 24 | fits | 146,182 | 165 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 380,681 | 3.807 | 20 | 24 | fits | 144,438 | 281 | 0.329 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 380,615 | 3.806 | 20 | 50 | fits | 144,438 | 281 | 0.329 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 462,719 | 4.627 | 20 | 50 | fits | 82,500 | 106 | 0.356 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 545,828 | 5.458 | 20 | 20 | fits | 83,175 | 34 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 892,485 | 8.925 | 20 | 20 | fits | 45,443 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 360,838 | 3.608 | 20 | 20 | fits | 82,500 | 106 | 0.356 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 352,107 | 3.521 | 20 | 200 | fits | 144,438 | 281 | 0.329 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 433,991 | 4.340 | 20 | 200 | fits | 82,500 | 106 | 0.356 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 353,031 | 3.530 | 20 | 20 | fits | 144,438 | 281 | 0.329 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 434,695 | 4.347 | 20 | 20 | fits | 82,500 | 106 | 0.356 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 202,039 | 2.020 | 20 | 24 | fits | 146,182 | 165 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 355,681 | 3.557 | 20 | 24 | fits | 144,438 | 281 | 0.329 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 355,615 | 3.556 | 20 | 50 | fits | 144,438 | 281 | 0.329 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 437,719 | 4.377 | 20 | 50 | fits | 82,500 | 106 | 0.356 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 520,828 | 5.208 | 20 | 20 | fits | 83,175 | 34 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 867,485 | 8.675 | 20 | 20 | fits | 45,443 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 379,127 | 3.791 | 20 | 20 | fits | 86,216 | 124 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 356,326 | 3.563 | 20 | 200 | fits | 147,423 | 267 | 0.320 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 453,553 | 4.536 | 20 | 200 | fits | 86,216 | 124 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 357,250 | 3.572 | 20 | 20 | fits | 147,423 | 267 | 0.320 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 454,257 | 4.543 | 20 | 20 | fits | 86,216 | 124 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 213,467 | 2.135 | 20 | 24 | fits | 146,074 | 164 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 359,900 | 3.599 | 20 | 24 | fits | 147,423 | 267 | 0.320 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 359,834 | 3.598 | 20 | 50 | fits | 147,423 | 267 | 0.320 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 457,281 | 4.573 | 20 | 50 | fits | 86,216 | 124 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 537,276 | 5.373 | 20 | 20 | fits | 80,061 | 28 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 884,021 | 8.840 | 20 | 20 | fits | 45,443 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 366,627 | 3.666 | 20 | 20 | fits | 86,216 | 124 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 343,826 | 3.438 | 20 | 200 | fits | 147,423 | 267 | 0.320 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 441,053 | 4.411 | 20 | 200 | fits | 86,216 | 124 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 344,750 | 3.447 | 20 | 20 | fits | 147,423 | 267 | 0.320 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 441,757 | 4.418 | 20 | 20 | fits | 86,216 | 124 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 200,967 | 2.010 | 20 | 24 | fits | 146,074 | 164 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 347,400 | 3.474 | 20 | 24 | fits | 147,423 | 267 | 0.320 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 347,334 | 3.473 | 20 | 50 | fits | 147,423 | 267 | 0.320 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 444,781 | 4.448 | 20 | 50 | fits | 86,216 | 124 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 524,776 | 5.248 | 20 | 20 | fits | 80,061 | 28 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 871,521 | 8.715 | 20 | 20 | fits | 45,443 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 354,127 | 3.541 | 20 | 20 | fits | 86,216 | 124 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 331,326 | 3.313 | 20 | 200 | fits | 147,423 | 267 | 0.320 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 428,553 | 4.286 | 20 | 200 | fits | 86,216 | 124 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 332,250 | 3.322 | 20 | 20 | fits | 147,423 | 267 | 0.320 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 429,257 | 4.293 | 20 | 20 | fits | 86,216 | 124 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 188,467 | 1.885 | 20 | 24 | fits | 146,074 | 164 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 334,900 | 3.349 | 20 | 24 | fits | 147,423 | 267 | 0.320 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 334,834 | 3.348 | 20 | 50 | fits | 147,423 | 267 | 0.320 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 432,281 | 4.323 | 20 | 50 | fits | 86,216 | 124 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 512,276 | 5.123 | 20 | 20 | fits | 80,061 | 28 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 859,021 | 8.590 | 20 | 20 | fits | 45,443 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 341,627 | 3.416 | 20 | 20 | fits | 86,216 | 124 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 318,826 | 3.188 | 20 | 200 | fits | 147,423 | 267 | 0.320 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 416,053 | 4.161 | 20 | 200 | fits | 86,216 | 124 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 319,750 | 3.197 | 20 | 20 | fits | 147,423 | 267 | 0.320 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 416,757 | 4.168 | 20 | 20 | fits | 86,216 | 124 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 175,967 | 1.760 | 20 | 24 | fits | 146,074 | 164 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 322,400 | 3.224 | 20 | 24 | fits | 147,423 | 267 | 0.320 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 322,334 | 3.223 | 20 | 50 | fits | 147,423 | 267 | 0.320 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 419,781 | 4.198 | 20 | 50 | fits | 86,216 | 124 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 499,776 | 4.998 | 20 | 20 | fits | 80,061 | 28 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 846,521 | 8.465 | 20 | 20 | fits | 45,443 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 329,127 | 3.291 | 20 | 20 | fits | 86,216 | 124 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 306,326 | 3.063 | 20 | 200 | fits | 147,423 | 267 | 0.320 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 403,553 | 4.036 | 20 | 200 | fits | 86,216 | 124 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 307,250 | 3.072 | 20 | 20 | fits | 147,423 | 267 | 0.320 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 404,257 | 4.043 | 20 | 20 | fits | 86,216 | 124 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 163,467 | 1.635 | 20 | 24 | fits | 146,074 | 164 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 309,900 | 3.099 | 20 | 24 | fits | 147,423 | 267 | 0.320 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 309,834 | 3.098 | 20 | 50 | fits | 147,423 | 267 | 0.320 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 407,281 | 4.073 | 20 | 50 | fits | 86,216 | 124 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 487,276 | 4.873 | 20 | 20 | fits | 80,061 | 28 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 834,021 | 8.340 | 20 | 20 | fits | 45,443 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 316,627 | 3.166 | 20 | 20 | fits | 86,216 | 124 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 293,826 | 2.938 | 20 | 200 | fits | 147,423 | 267 | 0.320 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 391,053 | 3.911 | 20 | 200 | fits | 86,216 | 124 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 294,750 | 2.947 | 20 | 20 | fits | 147,423 | 267 | 0.320 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 391,757 | 3.918 | 20 | 20 | fits | 86,216 | 124 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 150,967 | 1.510 | 20 | 24 | fits | 146,074 | 164 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 297,400 | 2.974 | 20 | 24 | fits | 147,423 | 267 | 0.320 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 297,334 | 2.973 | 20 | 50 | fits | 147,423 | 267 | 0.320 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 394,781 | 3.948 | 20 | 50 | fits | 86,216 | 124 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 474,776 | 4.748 | 20 | 20 | fits | 80,061 | 28 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 821,521 | 8.215 | 20 | 20 | fits | 45,443 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 338,778 | 3.388 | 20 | 20 | fits | 86,800 | 125 | 0.456 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 290,060 | 2.901 | 20 | 200 | fits | 143,400 | 262 | 0.320 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 387,902 | 3.879 | 20 | 200 | fits | 86,800 | 125 | 0.456 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 290,984 | 2.910 | 20 | 20 | fits | 143,400 | 262 | 0.320 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 388,606 | 3.886 | 20 | 20 | fits | 86,800 | 125 | 0.456 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 151,224 | 1.512 | 20 | 24 | fits | 145,160 | 164 | 0.381 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 293,634 | 2.936 | 20 | 24 | fits | 143,400 | 262 | 0.320 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 293,568 | 2.936 | 20 | 50 | fits | 143,400 | 262 | 0.320 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 391,630 | 3.916 | 20 | 50 | fits | 86,800 | 125 | 0.456 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 471,586 | 4.716 | 20 | 20 | fits | 80,022 | 28 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 818,528 | 8.185 | 20 | 20 | fits | 45,457 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 411,066 | 4.111 | 20 | 20 | fits | 81,303 | 121 | 0.347 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 376,373 | 3.764 | 20 | 200 | fits | 144,035 | 262 | 0.335 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 457,060 | 4.571 | 20 | 200 | fits | 81,303 | 121 | 0.347 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 377,297 | 3.773 | 20 | 20 | fits | 144,035 | 262 | 0.335 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 457,764 | 4.578 | 20 | 20 | fits | 81,303 | 121 | 0.347 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 226,688 | 2.267 | 20 | 24 | fits | 145,665 | 165 | 0.385 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 379,947 | 3.799 | 20 | 24 | fits | 144,035 | 262 | 0.335 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 379,881 | 3.799 | 20 | 50 | fits | 144,035 | 262 | 0.335 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 460,788 | 4.608 | 20 | 50 | fits | 81,303 | 121 | 0.347 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 540,662 | 5.407 | 20 | 20 | fits | 79,940 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 887,441 | 8.874 | 20 | 20 | fits | 45,444 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 328,387 | 3.284 | 20 | 20 | fits | 80,033 | 118 | 0.355 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 296,361 | 2.964 | 20 | 200 | fits | 145,402 | 266 | 0.331 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 375,778 | 3.758 | 20 | 200 | fits | 80,033 | 118 | 0.355 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 297,285 | 2.973 | 20 | 20 | fits | 145,402 | 266 | 0.331 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 376,482 | 3.765 | 20 | 20 | fits | 80,033 | 118 | 0.355 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 145,984 | 1.460 | 20 | 24 | fits | 144,169 | 162 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 299,935 | 2.999 | 20 | 24 | fits | 145,402 | 266 | 0.331 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 299,869 | 2.999 | 20 | 50 | fits | 145,402 | 266 | 0.331 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 379,506 | 3.795 | 20 | 50 | fits | 80,033 | 118 | 0.355 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 459,351 | 4.594 | 20 | 20 | fits | 79,911 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 805,884 | 8.059 | 20 | 20 | fits | 45,457 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 328,482 | 3.285 | 20 | 20 | fits | 83,935 | 127 | 0.368 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 291,348 | 2.913 | 20 | 200 | fits | 144,048 | 262 | 0.337 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 374,667 | 3.747 | 20 | 200 | fits | 83,935 | 127 | 0.368 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 292,272 | 2.923 | 20 | 20 | fits | 144,048 | 262 | 0.337 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 375,371 | 3.754 | 20 | 20 | fits | 83,935 | 127 | 0.368 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 142,325 | 1.423 | 20 | 24 | fits | 144,070 | 162 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 294,922 | 2.949 | 20 | 24 | fits | 144,048 | 262 | 0.337 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 294,856 | 2.949 | 20 | 50 | fits | 144,048 | 262 | 0.337 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 378,395 | 3.784 | 20 | 50 | fits | 83,935 | 127 | 0.368 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 458,308 | 4.583 | 20 | 20 | fits | 79,979 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 805,030 | 8.050 | 20 | 20 | fits | 45,444 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 316,161 | 3.162 | 20 | 20 | fits | 102,339 | 104 | 0.525 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 286,469 | 2.865 | 20 | 200 | fits | 148,283 | 284 | 0.315 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 388,192 | 3.882 | 20 | 200 | fits | 102,339 | 104 | 0.525 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 287,393 | 2.874 | 20 | 20 | fits | 148,283 | 284 | 0.315 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 388,896 | 3.889 | 20 | 20 | fits | 102,339 | 104 | 0.525 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 142,750 | 1.427 | 20 | 24 | fits | 144,086 | 161 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 290,043 | 2.900 | 20 | 24 | fits | 148,283 | 284 | 0.315 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 289,977 | 2.900 | 20 | 50 | fits | 148,283 | 284 | 0.315 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 391,920 | 3.919 | 20 | 50 | fits | 102,339 | 104 | 0.525 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 391,854 | 3.919 | 20 | 20 | fits | 102,339 | 104 | 0.525 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 894,688 | 8.947 | 20 | 20 | fits | 25,779 | 13 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 302,999 | 3.030 | 20 | 20 | fits | 101,217 | 101 | 0.

[... table.md: 192,770 bytes in full, sha256 549ca2a65ca11fe28d214cbc7efc4cdf57cd730cd358732579c6735da62dab0b; the middle 12,770 bytes are cut here, the first and last 90,000 kept ...]

ervice.adp.first.if0` | 300,596 | 3.006 | 20 | 200 | fits | 145,455 | 266 | 0.332 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 380,193 | 3.802 | 20 | 200 | fits | 80,213 | 118 | 0.361 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 301,520 | 3.015 | 20 | 20 | fits | 145,455 | 266 | 0.332 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 380,897 | 3.809 | 20 | 20 | fits | 80,213 | 118 | 0.361 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 150,166 | 1.502 | 20 | 24 | fits | 144,140 | 162 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 304,170 | 3.042 | 20 | 24 | fits | 145,455 | 266 | 0.332 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 304,104 | 3.041 | 20 | 50 | fits | 145,455 | 266 | 0.332 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 383,921 | 3.839 | 20 | 50 | fits | 80,213 | 118 | 0.361 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 464,004 | 4.640 | 20 | 20 | fits | 80,149 | 28 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 815,969 | 8.160 | 20 | 20 | fits | 45,565 | 20 | 0.695 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 298,246 | 2.982 | 20 | 20 | fits | 80,194 | 118 | 0.359 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 289,431 | 2.894 | 20 | 200 | fits | 143,245 | 261 | 0.319 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 369,009 | 3.690 | 20 | 200 | fits | 80,194 | 118 | 0.359 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 290,355 | 2.904 | 20 | 20 | fits | 143,245 | 261 | 0.319 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 369,713 | 3.697 | 20 | 20 | fits | 80,194 | 118 | 0.359 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 150,750 | 1.508 | 20 | 24 | fits | 144,134 | 161 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 293,005 | 2.930 | 20 | 24 | fits | 143,245 | 261 | 0.319 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 292,939 | 2.929 | 20 | 50 | fits | 143,245 | 261 | 0.319 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 372,737 | 3.727 | 20 | 50 | fits | 80,194 | 118 | 0.359 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 452,741 | 4.527 | 20 | 20 | fits | 80,070 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 808,314 | 8.083 | 20 | 20 | fits | 49,003 | 27 | 0.696 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 317,942 | 3.179 | 20 | 20 | fits | 80,119 | 118 | 0.357 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 285,853 | 2.859 | 20 | 200 | fits | 143,227 | 261 | 0.319 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 365,356 | 3.654 | 20 | 200 | fits | 80,119 | 118 | 0.357 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 286,777 | 2.868 | 20 | 20 | fits | 143,227 | 261 | 0.319 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 366,060 | 3.661 | 20 | 20 | fits | 80,119 | 118 | 0.357 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 147,190 | 1.472 | 20 | 24 | fits | 144,134 | 161 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 289,427 | 2.894 | 20 | 24 | fits | 143,227 | 261 | 0.319 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 289,361 | 2.894 | 20 | 50 | fits | 143,227 | 261 | 0.319 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 369,084 | 3.691 | 20 | 50 | fits | 80,119 | 118 | 0.357 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 448,989 | 4.490 | 20 | 20 | fits | 79,971 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 819,903 | 8.199 | 20 | 20 | fits | 45,702 | 20 | 0.701 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 316,109 | 3.161 | 20 | 20 | fits | 102,275 | 104 | 0.524 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 286,394 | 2.864 | 20 | 200 | fits | 148,160 | 284 | 0.313 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 388,053 | 3.881 | 20 | 200 | fits | 102,275 | 104 | 0.524 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 287,318 | 2.873 | 20 | 20 | fits | 148,160 | 284 | 0.313 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 388,757 | 3.888 | 20 | 20 | fits | 102,275 | 104 | 0.524 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 142,798 | 1.428 | 20 | 24 | fits | 144,134 | 161 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 289,968 | 2.900 | 20 | 24 | fits | 148,160 | 284 | 0.313 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 289,902 | 2.899 | 20 | 50 | fits | 148,160 | 284 | 0.313 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 391,781 | 3.918 | 20 | 50 | fits | 102,275 | 104 | 0.524 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 391,715 | 3.917 | 20 | 20 | fits | 102,275 | 104 | 0.524 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 819,032 | 8.190 | 20 | 20 | fits | 24,984 | 12 | 0.778 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 321,377 | 3.214 | 20 | 20 | fits | 81,797 | 103 | 0.431 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 294,781 | 2.948 | 20 | 200 | fits | 148,235 | 283 | 0.310 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 375,962 | 3.760 | 20 | 200 | fits | 81,797 | 103 | 0.431 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 295,705 | 2.957 | 20 | 20 | fits | 148,235 | 283 | 0.310 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 376,666 | 3.767 | 20 | 20 | fits | 81,797 | 103 | 0.431 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 151,110 | 1.511 | 20 | 24 | fits | 144,134 | 161 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 298,355 | 2.984 | 20 | 24 | fits | 148,235 | 283 | 0.310 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 298,289 | 2.983 | 20 | 50 | fits | 148,235 | 283 | 0.310 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 379,690 | 3.797 | 20 | 50 | fits | 81,797 | 103 | 0.431 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 459,901 | 4.599 | 20 | 20 | fits | 80,277 | 29 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 826,326 | 8.263 | 20 | 20 | fits | 45,441 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 312,300 | 3.123 | 20 | 20 | fits | 86,238 | 124 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 289,657 | 2.897 | 20 | 200 | fits | 146,671 | 267 | 0.317 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 386,748 | 3.867 | 20 | 200 | fits | 86,238 | 124 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 290,581 | 2.906 | 20 | 20 | fits | 146,671 | 267 | 0.317 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 387,452 | 3.875 | 20 | 20 | fits | 86,238 | 124 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 147,550 | 1.476 | 20 | 24 | fits | 144,134 | 161 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 293,231 | 2.932 | 20 | 24 | fits | 146,671 | 267 | 0.317 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 293,165 | 2.932 | 20 | 50 | fits | 146,671 | 267 | 0.317 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 390,476 | 3.905 | 20 | 50 | fits | 86,238 | 124 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 470,463 | 4.705 | 20 | 20 | fits | 80,053 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 817,155 | 8.172 | 20 | 20 | fits | 45,471 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 293,186 | 2.932 | 20 | 20 | fits | 80,309 | 119 | 0.361 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 284,371 | 2.844 | 20 | 200 | fits | 143,247 | 261 | 0.319 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 364,064 | 3.641 | 20 | 200 | fits | 80,309 | 119 | 0.361 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 285,295 | 2.853 | 20 | 20 | fits | 143,247 | 261 | 0.319 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 364,768 | 3.648 | 20 | 20 | fits | 80,309 | 119 | 0.361 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 145,688 | 1.457 | 20 | 24 | fits | 144,134 | 161 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 287,945 | 2.879 | 20 | 24 | fits | 143,247 | 261 | 0.319 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 287,879 | 2.879 | 20 | 50 | fits | 143,247 | 261 | 0.319 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 367,792 | 3.678 | 20 | 50 | fits | 80,309 | 119 | 0.361 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 463,321 | 4.633 | 20 | 20 | fits | 84,299 | 35 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 810,634 | 8.106 | 20 | 20 | fits | 45,471 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 329,860 | 3.299 | 20 | 20 | fits | 86,326 | 124 | 0.452 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 281,716 | 2.817 | 20 | 200 | fits | 144,152 | 267 | 0.317 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 378,926 | 3.789 | 20 | 200 | fits | 86,326 | 124 | 0.452 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 282,640 | 2.826 | 20 | 20 | fits | 144,152 | 267 | 0.317 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 379,630 | 3.796 | 20 | 20 | fits | 86,326 | 124 | 0.452 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 142,128 | 1.421 | 20 | 24 | fits | 144,134 | 161 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 285,290 | 2.853 | 20 | 24 | fits | 144,152 | 267 | 0.317 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 285,224 | 2.852 | 20 | 50 | fits | 144,152 | 267 | 0.317 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 382,654 | 3.827 | 20 | 50 | fits | 86,326 | 124 | 0.452 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 462,608 | 4.626 | 20 | 20 | fits | 80,020 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 809,353 | 8.094 | 20 | 20 | fits | 45,457 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 313,336 | 3.133 | 20 | 20 | fits | 82,384 | 106 | 0.352 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 298,775 | 2.988 | 20 | 200 | fits | 144,202 | 281 | 0.326 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 380,543 | 3.805 | 20 | 200 | fits | 82,384 | 106 | 0.352 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 299,699 | 2.997 | 20 | 20 | fits | 144,202 | 281 | 0.326 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 381,247 | 3.812 | 20 | 20 | fits | 82,384 | 106 | 0.352 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 149,598 | 1.496 | 20 | 24 | fits | 144,124 | 162 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 302,349 | 3.023 | 20 | 24 | fits | 144,202 | 281 | 0.326 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 302,283 | 3.023 | 20 | 50 | fits | 144,202 | 281 | 0.326 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 384,271 | 3.843 | 20 | 50 | fits | 82,384 | 106 | 0.352 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 464,032 | 4.640 | 20 | 20 | fits | 79,827 | 28 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 898,692 | 8.987 | 20 | 20 | fits | 47,592 | 22 | 0.722 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 308,546 | 3.085 | 20 | 20 | fits | 101,159 | 101 | 0.539 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 293,785 | 2.938 | 20 | 200 | fits | 148,263 | 283 | 0.310 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 394,328 | 3.943 | 20 | 200 | fits | 101,159 | 101 | 0.539 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 294,709 | 2.947 | 20 | 20 | fits | 148,263 | 283 | 0.310 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 395,032 | 3.950 | 20 | 20 | fits | 101,159 | 101 | 0.539 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 150,086 | 1.501 | 20 | 24 | fits | 144,086 | 161 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 297,359 | 2.974 | 20 | 24 | fits | 148,263 | 283 | 0.310 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 297,293 | 2.973 | 20 | 50 | fits | 148,263 | 283 | 0.310 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 398,056 | 3.981 | 20 | 50 | fits | 101,159 | 101 | 0.539 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 397,990 | 3.980 | 20 | 20 | fits | 101,159 | 101 | 0.539 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 909,187 | 9.092 | 20 | 20 | fits | 29,289 | 13 | 0.847 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 299,070 | 2.991 | 20 | 20 | fits | 101,132 | 101 | 0.541 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 290,212 | 2.902 | 20 | 200 | fits | 148,250 | 283 | 0.310 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 390,728 | 3.907 | 20 | 200 | fits | 101,132 | 101 | 0.541 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 291,136 | 2.911 | 20 | 20 | fits | 148,250 | 283 | 0.310 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 391,432 | 3.914 | 20 | 20 | fits | 101,132 | 101 | 0.541 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 146,526 | 1.465 | 20 | 24 | fits | 144,086 | 161 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 293,786 | 2.938 | 20 | 24 | fits | 148,250 | 283 | 0.310 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 293,720 | 2.937 | 20 | 50 | fits | 148,250 | 283 | 0.310 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 394,456 | 3.945 | 20 | 50 | fits | 101,132 | 101 | 0.541 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 394,390 | 3.944 | 20 | 20 | fits | 101,132 | 101 | 0.541 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 905,205 | 9.052 | 20 | 20 | fits | 25,011 | 12 | 0.778 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 291,156 | 2.912 | 20 | 20 | fits | 80,203 | 118 | 0.359 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 282,341 | 2.823 | 20 | 200 | fits | 144,155 | 266 | 0.318 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 361,928 | 3.619 | 20 | 200 | fits | 80,203 | 118 | 0.359 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 283,265 | 2.833 | 20 | 20 | fits | 144,155 | 266 | 0.318 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 362,632 | 3.626 | 20 | 20 | fits | 80,203 | 118 | 0.359 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 142,750 | 1.427 | 20 | 24 | fits | 144,086 | 161 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 285,915 | 2.859 | 20 | 24 | fits | 144,155 | 266 | 0.318 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 285,849 | 2.858 | 20 | 50 | fits | 144,155 | 266 | 0.318 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 365,656 | 3.657 | 20 | 50 | fits | 80,203 | 118 | 0.359 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 449,050 | 4.490 | 20 | 20 | fits | 83,460 | 34 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 899,212 | 8.992 | 20 | 20 | fits | 45,441 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 328,229 | 3.282 | 20 | 20 | fits | 82,040 | 106 | 0.404 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 293,162 | 2.932 | 20 | 200 | fits | 147,280 | 279 | 0.315 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 374,586 | 3.746 | 20 | 200 | fits | 82,040 | 106 | 0.404 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 294,086 | 2.941 | 20 | 20 | fits | 147,280 | 279 | 0.315 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 375,290 | 3.753 | 20 | 20 | fits | 82,040 | 106 | 0.404 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 150,446 | 1.504 | 20 | 24 | fits | 144,086 | 161 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 296,736 | 2.967 | 20 | 24 | fits | 147,280 | 279 | 0.315 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 296,670 | 2.967 | 20 | 50 | fits | 147,280 | 279 | 0.315 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 378,314 | 3.783 | 20 | 50 | fits | 82,040 | 106 | 0.404 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 543,805 | 5.438 | 20 | 20 | fits | 84,775 | 36 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 907,118 | 9.071 | 20 | 20 | fits | 45,442 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 412,644 | 4.126 | 20 | 20 | fits | 90,403 | 115 | 0.445 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 286,993 | 2.870 | 20 | 200 | fits | 144,671 | 278 | 0.319 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 467,805 | 4.678 | 20 | 200 | fits | 90,403 | 115 | 0.445 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 287,917 | 2.879 | 20 | 20 | fits | 144,671 | 278 | 0.319 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 468,509 | 4.685 | 20 | 20 | fits | 90,403 | 115 | 0.445 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 146,886 | 1.469 | 20 | 24 | fits | 144,086 | 161 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 290,567 | 2.906 | 20 | 24 | fits | 144,671 | 278 | 0.319 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 290,501 | 2.905 | 20 | 50 | fits | 144,671 | 278 | 0.319 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 471,533 | 4.715 | 20 | 50 | fits | 90,403 | 115 | 0.445 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 551,724 | 5.517 | 20 | 20 | fits | 80,257 | 28 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 898,416 | 8.984 | 20 | 20 | fits | 45,490 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 316,771 | 3.168 | 20 | 20 | fits | 80,169 | 118 | 0.358 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 284,673 | 2.847 | 20 | 200 | fits | 143,242 | 261 | 0.319 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 364,226 | 3.642 | 20 | 200 | fits | 80,169 | 118 | 0.358 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 285,597 | 2.856 | 20 | 20 | fits | 143,242 | 261 | 0.319 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 364,930 | 3.649 | 20 | 20 | fits | 80,169 | 118 | 0.358 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 145,995 | 1.460 | 20 | 24 | fits | 144,086 | 161 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 288,247 | 2.882 | 20 | 24 | fits | 143,242 | 261 | 0.319 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 288,181 | 2.882 | 20 | 50 | fits | 143,242 | 261 | 0.319 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 367,954 | 3.680 | 20 | 50 | fits | 80,169 | 118 | 0.358 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 447,788 | 4.478 | 20 | 20 | fits | 79,900 | 28 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 814,361 | 8.144 | 20 | 20 | fits | 45,526 | 20 | 0.692 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 315,800 | 3.158 | 20 | 20 | fits | 102,254 | 104 | 0.524 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 286,076 | 2.861 | 20 | 200 | fits | 148,205 | 284 | 0.314 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 387,714 | 3.877 | 20 | 200 | fits | 102,254 | 104 | 0.524 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 287,000 | 2.870 | 20 | 20 | fits | 148,205 | 284 | 0.314 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 388,418 | 3.884 | 20 | 20 | fits | 102,254 | 104 | 0.524 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 142,435 | 1.424 | 20 | 24 | fits | 144,086 | 161 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 289,650 | 2.897 | 20 | 24 | fits | 148,205 | 284 | 0.314 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 289,584 | 2.896 | 20 | 50 | fits | 148,205 | 284 | 0.314 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 391,442 | 3.914 | 20 | 50 | fits | 102,254 | 104 | 0.524 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 391,376 | 3.914 | 20 | 20 | fits | 102,254 | 104 | 0.524 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 814,753 | 8.148 | 20 | 20 | fits | 25,012 | 12 | 0.778 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 316,743 | 3.167 | 20 | 20 | fits | 81,789 | 104 | 0.480 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 293,680 | 2.937 | 20 | 200 | fits | 148,329 | 284 | 0.310 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 386,377 | 3.864 | 20 | 200 | fits | 81,789 | 104 | 0.480 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 294,604 | 2.946 | 20 | 20 | fits | 148,329 | 284 | 0.310 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 387,081 | 3.871 | 20 | 20 | fits | 81,789 | 104 | 0.480 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 149,915 | 1.499 | 20 | 24 | fits | 144,086 | 161 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 297,254 | 2.973 | 20 | 24 | fits | 148,329 | 284 | 0.310 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 297,188 | 2.972 | 20 | 50 | fits | 148,329 | 284 | 0.310 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 390,105 | 3.901 | 20 | 50 | fits | 81,789 | 104 | 0.480 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 470,168 | 4.702 | 20 | 20 | fits | 80,129 | 28 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 822,309 | 8.223 | 20 | 20 | fits | 45,593 | 20 | 0.695 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 308,118 | 3.081 | 20 | 20 | fits | 86,681 | 125 | 0.456 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 285,122 | 2.851 | 20 | 200 | fits | 143,331 | 262 | 0.320 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 382,687 | 3.827 | 20 | 200 | fits | 86,681 | 125 | 0.456 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 286,046 | 2.860 | 20 | 20 | fits | 143,331 | 262 | 0.320 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 383,391 | 3.834 | 20 | 20 | fits | 86,681 | 125 | 0.456 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 146,355 | 1.464 | 20 | 24 | fits | 144,086 | 161 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 288,696 | 2.887 | 20 | 24 | fits | 143,331 | 262 | 0.320 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 288,630 | 2.886 | 20 | 50 | fits | 143,331 | 262 | 0.320 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 386,415 | 3.864 | 20 | 50 | fits | 86,681 | 125 | 0.456 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 466,526 | 4.665 | 20 | 20 | fits | 80,177 | 28 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 818,551 | 8.186 | 20 | 20 | fits | 45,471 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 327,438 | 3.274 | 20 | 20 | fits | 82,875 | 124 | 0.380 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 292,884 | 2.929 | 20 | 200 | fits | 145,141 | 266 | 0.331 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 375,143 | 3.751 | 20 | 200 | fits | 82,875 | 124 | 0.380 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 293,808 | 2.938 | 20 | 20 | fits | 145,141 | 266 | 0.331 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 375,847 | 3.758 | 20 | 20 | fits | 82,875 | 124 | 0.380 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 142,768 | 1.428 | 20 | 24 | fits | 144,104 | 162 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 296,458 | 2.965 | 20 | 24 | fits | 145,141 | 266 | 0.331 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 296,392 | 2.964 | 20 | 50 | fits | 145,141 | 266 | 0.331 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 378,871 | 3.789 | 20 | 50 | fits | 82,875 | 124 | 0.380 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 458,861 | 4.589 | 20 | 20 | fits | 80,056 | 28 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 810,836 | 8.108 | 20 | 20 | fits | 45,457 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 314,479 | 3.145 | 20 | 20 | fits | 80,151 | 118 | 0.358 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 282,358 | 2.824 | 20 | 200 | fits | 144,124 | 266 | 0.318 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 361,893 | 3.619 | 20 | 200 | fits | 80,151 | 118 | 0.358 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 283,282 | 2.833 | 20 | 20 | fits | 144,124 | 266 | 0.318 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 362,597 | 3.626 | 20 | 20 | fits | 80,151 | 118 | 0.358 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 142,798 | 1.428 | 20 | 24 | fits | 144,134 | 161 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 285,932 | 2.859 | 20 | 24 | fits | 144,124 | 266 | 0.318 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 285,866 | 2.859 | 20 | 50 | fits | 144,124 | 266 | 0.318 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 365,621 | 3.656 | 20 | 50 | fits | 80,151 | 118 | 0.358 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 449,066 | 4.491 | 20 | 20 | fits | 83,511 | 34 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 815,030 | 8.150 | 20 | 20 | fits | 52,882 | 27 | 0.765 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 321,723 | 3.217 | 20 | 20 | fits | 81,454 | 103 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 294,535 | 2.945 | 20 | 200 | fits | 148,250 | 283 | 0.310 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 375,373 | 3.754 | 20 | 200 | fits | 81,454 | 103 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 295,459 | 2.955 | 20 | 20 | fits | 148,250 | 283 | 0.310 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 376,077 | 3.761 | 20 | 20 | fits | 81,454 | 103 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 150,849 | 1.508 | 20 | 24 | fits | 144,134 | 161 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 298,109 | 2.981 | 20 | 24 | fits | 148,250 | 283 | 0.310 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 298,043 | 2.980 | 20 | 50 | fits | 148,250 | 283 | 0.310 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 379,101 | 3.791 | 20 | 50 | fits | 81,454 | 103 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 459,198 | 4.592 | 20 | 20 | fits | 80,163 | 28 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 825,799 | 8.258 | 20 | 20 | fits | 45,559 | 20 | 0.692 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 316,532 | 3.165 | 20 | 20 | fits | 84,021 | 109 | 0.350 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 287,351 | 2.874 | 20 | 200 | fits | 144,626 | 277 | 0.319 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 370,756 | 3.708 | 20 | 200 | fits | 84,021 | 109 | 0.350 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 288,275 | 2.883 | 20 | 20 | fits | 144,626 | 277 | 0.319 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 371,460 | 3.715 | 20 | 20 | fits | 84,021 | 109 | 0.350 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 147,289 | 1.473 | 20 | 24 | fits | 144,134 | 161 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 290,925 | 2.909 | 20 | 24 | fits | 144,626 | 277 | 0.319 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 290,859 | 2.909 | 20 | 50 | fits | 144,626 | 277 | 0.319 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 374,484 | 3.745 | 20 | 50 | fits | 84,021 | 109 | 0.350 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 454,543 | 4.545 | 20 | 20 | fits | 80,125 | 28 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 821,126 | 8.211 | 20 | 20 | fits | 45,469 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 311,756 | 3.118 | 20 | 20 | fits | 80,336 | 118 | 0.365 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 303,001 | 3.030 | 20 | 200 | fits | 145,471 | 266 | 0.332 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 382,721 | 3.827 | 20 | 200 | fits | 80,336 | 118 | 0.365 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 303,925 | 3.039 | 20 | 20 | fits | 145,471 | 266 | 0.332 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 383,425 | 3.834 | 20 | 20 | fits | 80,336 | 118 | 0.365 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 152,588 | 1.526 | 20 | 24 | fits | 144,185 | 162 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 306,575 | 3.066 | 20 | 24 | fits | 145,471 | 266 | 0.332 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 306,509 | 3.065 | 20 | 50 | fits | 145,471 | 266 | 0.332 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 386,449 | 3.864 | 20 | 50 | fits | 80,336 | 118 | 0.365 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 466,516 | 4.665 | 20 | 20 | fits | 80,133 | 28 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 813,049 | 8.130 | 20 | 20 | fits | 45,443 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 331,476 | 3.315 | 20 | 20 | fits | 80,198 | 118 | 0.361 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 299,367 | 2.994 | 20 | 200 | fits | 145,514 | 266 | 0.333 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 378,949 | 3.789 | 20 | 200 | fits | 80,198 | 118 | 0.361 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 300,291 | 3.003 | 20 | 20 | fits | 145,514 | 266 | 0.333 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 379,653 | 3.797 | 20 | 20 | fits | 80,198 | 118 | 0.361 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 148,911 | 1.489 | 20 | 24 | fits | 144,068 | 162 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 302,941 | 3.029 | 20 | 24 | fits | 145,514 | 266 | 0.333 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 302,875 | 3.029 | 20 | 50 | fits | 145,514 | 266 | 0.333 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 382,677 | 3.827 | 20 | 50 | fits | 80,198 | 118 | 0.361 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 462,559 | 4.626 | 20 | 20 | fits | 79,948 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 809,092 | 8.091 | 20 | 20 | fits | 45,457 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 321,249 | 3.212 | 20 | 20 | fits | 80,294 | 118 | 0.359 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 289,100 | 2.891 | 20 | 200 | fits | 143,249 | 261 | 0.319 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 368,778 | 3.688 | 20 | 200 | fits | 80,294 | 118 | 0.359 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 290,024 | 2.900 | 20 | 20 | fits | 143,249 | 261 | 0.319 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 369,482 | 3.695 | 20 | 20 | fits | 80,294 | 118 | 0.359 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 150,415 | 1.504 | 20 | 24 | fits | 144,134 | 161 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 292,674 | 2.927 | 20 | 24 | fits | 143,249 | 261 | 0.319 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 292,608 | 2.926 | 20 | 50 | fits | 143,249 | 261 | 0.319 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 372,506 | 3.725 | 20 | 50 | fits | 80,294 | 118 | 0.359 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 452,443 | 4.524 | 20 | 20 | fits | 80,003 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 821,258 | 8.213 | 20 | 20 | fits | 55,668 | 33 | 0.759 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 319,383 | 3.194 | 20 | 20 | fits | 102,456 | 104 | 0.527 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 289,608 | 2.896 | 20 | 200 | fits | 147,317 | 279 | 0.316 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 391,448 | 3.914 | 20 | 200 | fits | 102,456 | 104 | 0.527 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 290,532 | 2.905 | 20 | 20 | fits | 147,317 | 279 | 0.316 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 392,152 | 3.922 | 20 | 20 | fits | 102,456 | 104 | 0.527 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 146,855 | 1.469 | 20 | 24 | fits | 144,134 | 161 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 293,182 | 2.932 | 20 | 24 | fits | 147,317 | 279 | 0.316 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 293,116 | 2.931 | 20 | 50 | fits | 147,317 | 279 | 0.316 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 395,176 | 3.952 | 20 | 50 | fits | 102,456 | 104 | 0.527 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 395,110 | 3.951 | 20 | 20 | fits | 102,456 | 104 | 0.527 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 899,259 | 8.993 | 20 | 20 | fits | 25,130 | 12 | 0.783 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 296,160 | 2.962 | 20 | 20 | fits | 82,530 | 106 | 0.352 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 281,552 | 2.816 | 20 | 200 | fits | 143,318 | 281 | 0.315 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 363,466 | 3.635 | 20 | 200 | fits | 82,530 | 106 | 0.352 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 282,476 | 2.825 | 20 | 20 | fits | 143,318 | 281 | 0.315 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 364,170 | 3.642 | 20 | 20 | fits | 82,530 | 106 | 0.352 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 142,798 | 1.428 | 20 | 24 | fits | 144,134 | 161 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 285,126 | 2.851 | 20 | 24 | fits | 143,318 | 281 | 0.315 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 285,060 | 2.851 | 20 | 50 | fits | 143,318 | 281 | 0.315 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 367,194 | 3.672 | 20 | 50 | fits | 82,530 | 106 | 0.352 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 447,209 | 4.472 | 20 | 20 | fits | 80,081 | 29 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 894,565 | 8.946 | 20 | 20 | fits | 45,460 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 298,293 | 2.983 | 20 | 20 | fits | 80,492 | 119 | 0.364 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 289,478 | 2.895 | 20 | 200 | fits | 143,267 | 261 | 0.319 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 369,354 | 3.694 | 20 | 200 | fits | 80,492 | 119 | 0.364 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 290,402 | 2.904 | 20 | 20 | fits | 143,267 | 261 | 0.319 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 370,058 | 3.701 | 20 | 20 | fits | 80,492 | 119 | 0.364 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 150,775 | 1.508 | 20 | 24 | fits | 144,134 | 161 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 293,052 | 2.931 | 20 | 24 | fits | 143,267 | 261 | 0.319 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 292,986 | 2.930 | 20 | 50 | fits | 143,267 | 261 | 0.319 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 373,082 | 3.731 | 20 | 50 | fits | 80,492 | 119 | 0.364 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 470,932 | 4.709 | 20 | 20 | fits | 86,620 | 41 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 896,517 | 8.965 | 20 | 20 | fits | 45,469 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 339,729 | 3.397 | 20 | 20 | fits | 92,086 | 131 | 0.466 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 285,983 | 2.860 | 20 | 200 | fits | 143,332 | 262 | 0.320 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 388,953 | 3.890 | 20 | 200 | fits | 92,086 | 131 | 0.466 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 286,907 | 2.869 | 20 | 20 | fits | 143,332 | 262 | 0.320 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 389,657 | 3.897 | 20 | 20 | fits | 92,086 | 131 | 0.466 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 147,215 | 1.472 | 20 | 24 | fits | 144,134 | 161 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 289,557 | 2.896 | 20 | 24 | fits | 143,332 | 262 | 0.320 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 289,491 | 2.895 | 20 | 50 | fits | 143,332 | 262 | 0.320 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 392,681 | 3.927 | 20 | 50 | fits | 92,086 | 131 | 0.466 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 550,583 | 5.506 | 20 | 20 | fits | 80,137 | 29 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 897,670 | 8.977 | 20 | 20 | fits | 45,457 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 333,462 | 3.335 | 20 | 20 | fits | 88,767 | 133 | 0.396 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 291,601 | 2.916 | 20 | 200 | fits | 144,031 | 262 | 0.337 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 379,752 | 3.798 | 20 | 200 | fits | 88,767 | 133 | 0.396 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 292,525 | 2.925 | 20 | 20 | fits | 144,031 | 262 | 0.337 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 380,456 | 3.805 | 20 | 20 | fits | 88,767 | 133 | 0.396 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 142,834 | 1.428 | 20 | 24 | fits | 144,170 | 162 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 295,175 | 2.952 | 20 | 24 | fits | 144,031 | 262 | 0.337 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 295,109 | 2.951 | 20 | 50 | fits | 144,031 | 262 | 0.337 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 383,480 | 3.835 | 20 | 50 | fits | 88,767 | 133 | 0.396 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 541,276 | 5.413 | 20 | 20 | fits | 80,031 | 29 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 888,251 | 8.883 | 20 | 20 | fits | 45,521 | 21 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 322,814 | 3.228 | 20 | 20 | fits | 80,377 | 119 | 0.360 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 290,665 | 2.907 | 20 | 200 | fits | 143,249 | 261 | 0.319 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 370,426 | 3.704 | 20 | 200 | fits | 80,377 | 119 | 0.360 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 291,589 | 2.916 | 20 | 20 | fits | 143,249 | 261 | 0.319 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 371,130 | 3.711 | 20 | 20 | fits | 80,377 | 119 | 0.360 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 151,980 | 1.520 | 20 | 24 | fits | 144,134 | 161 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 294,239 | 2.942 | 20 | 24 | fits | 143,249 | 261 | 0.319 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 294,173 | 2.942 | 20 | 50 | fits | 143,249 | 261 | 0.319 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 374,154 | 3.742 | 20 | 50 | fits | 80,377 | 119 | 0.360 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 469,545 | 4.695 | 20 | 20 | fits | 84,128 | 35 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 816,721 | 8.167 | 20 | 20 | fits | 45,485 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 337,298 | 3.373 | 20 | 20 | fits | 82,701 | 107 | 0.462 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 291,265 | 2.913 | 20 | 200 | fits | 147,409 | 280 | 0.316 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 384,943 | 3.849 | 20 | 200 | fits | 82,701 | 107 | 0.462 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 292,189 | 2.922 | 20 | 20 | fits | 147,409 | 280 | 0.316 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 385,647 | 3.856 | 20 | 20 | fits | 82,701 | 107 | 0.462 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 148,420 | 1.484 | 20 | 24 | fits | 144,134 | 161 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 294,839 | 2.948 | 20 | 24 | fits | 147,409 | 280 | 0.316 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 294,773 | 2.948 | 20 | 50 | fits | 147,409 | 280 | 0.316 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 388,671 | 3.887 | 20 | 50 | fits | 82,701 | 107 | 0.462 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 468,569 | 4.686 | 20 | 20 | fits | 79,964 | 28 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 816,191 | 8.162 | 20 | 20 | fits | 45,580 | 20 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 308,748 | 3.087 | 20 | 20 | fits | 82,435 | 106 | 0.354 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 294,136 | 2.941 | 20 | 200 | fits | 144,271 | 281 | 0.327 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 375,955 | 3.760 | 20 | 200 | fits | 82,435 | 106 | 0.354 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 295,060 | 2.951 | 20 | 20 | fits | 144,271 | 281 | 0.327 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 376,659 | 3.767 | 20 | 20 | fits | 82,435 | 106 | 0.354 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 144,923 | 1.449 | 20 | 24 | fits | 144,197 | 162 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 297,710 | 2.977 | 20 | 24 | fits | 144,271 | 281 | 0.327 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 297,644 | 2.976 | 20 | 50 | fits | 144,271 | 281 | 0.327 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 379,683 | 3.797 | 20 | 50 | fits | 82,435 | 106 | 0.354 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 459,375 | 4.594 | 20 | 20 | fits | 79,758 | 28 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 811,316 | 8.113 | 20 | 20 | fits | 45,584 | 20 | 0.695 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 304,664 | 3.047 | 20 | 20 | fits | 101,258 | 101 | 0.540 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 289,852 | 2.899 | 20 | 200 | fits | 148,283 | 283 | 0.310 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 390,494 | 3.905 | 20 | 200 | fits | 101,258 | 101 | 0.540 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 290,776 | 2.908 | 20 | 20 | fits | 148,283 | 283 | 0.310 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 391,198 | 3.912 | 20 | 20 | fits | 101,258 | 101 | 0.540 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 146,133 | 1.461 | 20 | 24 | fits | 144,065 | 161 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 293,426 | 2.934 | 20 | 24 | fits | 148,283 | 283 | 0.310 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 293,360 | 2.934 | 20 | 50 | fits | 148,283 | 283 | 0.310 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 394,222 | 3.942 | 20 | 50 | fits | 101,258 | 101 | 0.540 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 394,156 | 3.942 | 20 | 20 | fits | 101,258 | 101 | 0.540 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 821,897 | 8.219 | 20 | 20 | fits | 31,821 | 19 | 0.837 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 290,302 | 2.903 | 20 | 20 | fits | 82,860 | 106 | 0.363 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 281,444 | 2.814 | 20 | 200 | fits | 143,318 | 281 | 0.315 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 363,688 | 3.637 | 20 | 200 | fits | 82,860 | 106 | 0.363 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 282,368 | 2.824 | 20 | 20 | fits | 143,318 | 281 | 0.315 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 364,392 | 3.644 | 20 | 20 | fits | 82,860 | 106 | 0.363 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 142,690 | 1.427 | 20 | 24 | fits | 144,086 | 161 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 285,018 | 2.850 | 20 | 24 | fits | 143,318 | 281 | 0.315 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 284,952 | 2.850 | 20 | 50 | fits | 143,318 | 281 | 0.315 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 367,416 | 3.674 | 20 | 50 | fits | 82,860 | 106 | 0.363 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 447,215 | 4.472 | 20 | 20 | fits | 79,865 | 28 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 818,041 | 8.180 | 20 | 20 | fits | 45,571 | 20 | 0.698 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 321,017 | 3.210 | 20 | 20 | fits | 80,335 | 118 | 0.361 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 288,868 | 2.889 | 20 | 200 | fits | 143,262 | 261 | 0.319 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 368,587 | 3.686 | 20 | 200 | fits | 80,335 | 118 | 0.361 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 289,792 | 2.898 | 20 | 20 | fits | 143,262 | 261 | 0.319 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 369,291 | 3.693 | 20 | 20 | fits | 80,335 | 118 | 0.361 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 150,170 | 1.502 | 20 | 24 | fits | 144,086 | 161 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 292,442 | 2.924 | 20 | 24 | fits | 143,262 | 261 | 0.319 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 292,376 | 2.924 | 20 | 50 | fits | 143,262 | 261 | 0.319 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 372,315 | 3.723 | 20 | 50 | fits | 80,335 | 118 | 0.361 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 455,574 | 4.556 | 20 | 20 | fits | 83,325 | 34 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 822,181 | 8.222 | 20 | 20 | fits | 45,455 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 324,494 | 3.245 | 20 | 20 | fits | 82,162 | 106 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 289,376 | 2.894 | 20 | 200 | fits | 147,330 | 279 | 0.316 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 370,922 | 3.709 | 20 | 200 | fits | 82,162 | 106 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 290,300 | 2.903 | 20 | 20 | fits | 147,330 | 279 | 0.316 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 371,626 | 3.716 | 20 | 20 | fits | 82,162 | 106 | 0.406 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 146,610 | 1.466 | 20 | 24 | fits | 144,086 | 161 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 292,950 | 2.929 | 20 | 24 | fits | 147,330 | 279 | 0.316 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 292,884 | 2.929 | 20 | 50 | fits | 147,330 | 279 | 0.316 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 374,650 | 3.747 | 20 | 50 | fits | 82,162 | 106 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 454,799 | 4.548 | 20 | 20 | fits | 80,215 | 29 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 821,246 | 8.212 | 20 | 20 | fits | 45,442 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 323,657 | 3.237 | 20 | 20 | fits | 93,206 | 118 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 281,596 | 2.816 | 20 | 200 | fits | 143,410 | 282 | 0.316 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 385,779 | 3.858 | 20 | 200 | fits | 93,206 | 118 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 282,520 | 2.825 | 20 | 20 | fits | 143,410 | 282 | 0.316 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 386,483 | 3.865 | 20 | 20 | fits | 93,206 | 118 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 142,750 | 1.427 | 20 | 24 | fits | 144,086 | 161 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 285,170 | 2.852 | 20 | 24 | fits | 143,410 | 282 | 0.316 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 285,104 | 2.851 | 20 | 50 | fits | 143,410 | 282 | 0.316 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 389,507 | 3.895 | 20 | 50 | fits | 93,206 | 118 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 469,511 | 4.695 | 20 | 20 | fits | 80,070 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 816,816 | 8.168 | 20 | 20 | fits | 45,626 | 20 | 0.693 |
| LINK_UP | `adp.link_up.if0` | 2,319 | 0.023 | 20 | 200 | fits | 22,423 | 43 (11) | 0.667 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,167 | 0.152 | 20 | 200 | fits | 17,269 | 23 (39) | 0.558 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 11,929 | 0.119 | 20 | 200 | fits | 2,139 | 10 (11) | 0.333 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 153,570 | 1.536 | 20 | 200 | fits | 154,510 | 259 | 0.366 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 189,024 | 1.890 | 20 | 20 | fits | 139,638 | 264 | 0.208 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 217,474 | 2.175 | 20 | 24 | fits | 55,963 | 45 | 0.476 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 186,066 | 1.861 | 20 | 50 | fits | 92,108 | 81 | 0.667 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 734,726 | 7.347 | 20 | 20 | fits | 51,113 | 26 | 0.744 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 221,435 | 2.214 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 153,570 | 1.536 | 20 | 200 | fits | 154,510 | 259 | 0.366 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 201,251 | 2.013 | 20 | 20 | fits | 141,082 | 267 | 0.226 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 205,363 | 2.054 | 20 | 24 | fits | 56,915 | 51 | 0.467 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 178,578 | 1.786 | 20 | 50 | fits | 84,620 | 83 | 0.683 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 750,973 | 7.510 | 20 | 20 | fits | 61,369 | 36 | 0.695 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 234,478 | 2.345 | 49 | 49 | fits | 0 | - | 0.000 |
| Talker Advertise RX for every input, bound | `srp.bound_advertise.if0` | 64,336 | 0.643 | 20 | 20 | fits | 64,402 | 15 | 0.909 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 15,911 | 0.159 | 20 | 20 | fits | 25,162 | 21 (35) | 0.772 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 5,254 | 0.053 | 20 | 20 | fits | 21,115 | 17 (14) | 0.804 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 12,585 | 0.126 | 20 | 20 | fits | 20,847 | 18 (14) | 0.807 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 17,430 | 0.174 | 20 | 20 | fits | 24,995 | 21 (35) | 0.766 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 69,479 | 0.695 | 20 | 20 | fits | 28,356 | 8 | 0.832 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 34,997 | 0.350 | 20 | 20 | fits | 35,063 | 12 | 0.874 |
| malformed MRPDU discard | `srp.malformed.if0` | 16,654 | 0.167 | 20 | 20 | fits | 16,720 | 12 | 0.671 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 71,411 | 0.714 | 220 | 220 | fits | 49,321 | 6 | 0.917 |
| an event behind 15 others | `backlog.event.if0` | 155,354 | 1.554 | 20 | 200 | fits | 44,684 | 78 | 0.503 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 352,786 | 3.528 | 20 | 20 | fits | 130,915 | 161 | 0.221 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 371,880 | 3.719 | 20 | 200 | fits | 130,915 | 161 | 0.221 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 371,264 | 3.713 | 20 | 200 | fits | 130,915 | 161 | 0.221 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 367,558 | 3.676 | 20 | 20 | fits | 130,915 | 161 | 0.221 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 366,722 | 3.667 | 20 | 20 | fits | 130,915 | 161 | 0.221 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 145,562 | 1.456 | 20 | 24 | fits | 146,453 | 167 | 0.391 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 239,293 | 2.393 | 20 | 24 | fits | 50,037 | 26 | 0.682 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 370,142 | 3.701 | 20 | 50 | fits | 130,915 | 161 | 0.221 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 369,746 | 3.697 | 20 | 50 | fits | 130,915 | 161 | 0.221 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 399,063 | 3.991 | 20 | 20 | fits | 26,909 | 57 | 0.112 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 445,336 | 4.453 | 20 | 20 | fits | 20,939 | 40 | 0.045 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 297,013 | 2.970 | 20 | 20 | fits | 100,677 | 102 | 0.540 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 288,299 | 2.883 | 20 | 200 | fits | 147,938 | 283 | 0.308 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 388,360 | 3.884 | 20 | 200 | fits | 100,677 | 102 | 0.540 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 289,223 | 2.892 | 20 | 20 | fits | 147,938 | 283 | 0.308 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 389,064 | 3.891 | 20 | 20 | fits | 100,677 | 102 | 0.540 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 144,925 | 1.449 | 20 | 24 | fits | 145,111 | 164 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 291,873 | 2.919 | 20 | 24 | fits | 147,938 | 283 | 0.308 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 291,807 | 2.918 | 20 | 50 | fits | 147,938 | 283 | 0.308 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 392,088 | 3.921 | 20 | 50 | fits | 100,677 | 102 | 0.540 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 392,022 | 3.920 | 20 | 20 | fits | 100,677 | 102 | 0.540 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 818,845 | 8.188 | 20 | 20 | fits | 24,978 | 12 | 0.778 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 7,710 | 0.077 | 20 | 20 | fits | 23,371 | 19 | 0.763 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 288,299 | 2.883 | 20 | 200 | fits | 147,938 | 283 | 0.308 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 23,277 | 0.233 | 20 | 200 | fits | 23,371 | 19 | 0.763 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 289,223 | 2.892 | 20 | 20 | fits | 147,938 | 283 | 0.308 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 378,709 | 3.787 | 20 | 20 | fits | 90,322 | 92 | 0.498 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 144,925 | 1.449 | 20 | 24 | fits | 145,111 | 164 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 291,873 | 2.919 | 20 | 24 | fits | 147,938 | 283 | 0.308 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 291,807 | 2.918 | 20 | 50 | fits | 147,938 | 283 | 0.308 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 381,733 | 3.817 | 20 | 50 | fits | 90,322 | 92 | 0.498 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 381,667 | 3.817 | 20 | 20 | fits | 90,322 | 92 | 0.498 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 808,376 | 8.084 | 20 | 20 | fits | 24,978 | 12 | 0.778 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,255,463 | 62.555 | 20 | 20 | MISS ceiling | 15,560 | 13 | 0.417 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,271,017 | 62.710 | 20 | 20 | MISS ceiling | 15,412 | 13 | 0.400 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,286,275 | 62.863 | 20 | 20 | MISS ceiling | 15,315 | 13 | 0.408 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,301,515 | 63.015 | 20 | 20 | MISS ceiling | 15,316 | 13 | 0.408 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,316,753 | 63.168 | 20 | 20 | MISS ceiling | 15,301 | 13 | 0.408 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 152,343 | 1.523 | 20 | 200 | fits | 147,381 | 252 | 0.371 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 244,350 | 2.443 | 20 | 200 | fits | 92,623 | 138 | 0.488 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 148,021 | 1.480 | 20 | 20 | fits | 147,381 | 252 | 0.371 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,181,322 | 61.813 | 20 | 20 | MISS ceiling | 25,042 | 15 | 0.627 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 151,661 | 1.517 | 20 | 24 | fits | 147,381 | 252 | 0.371 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,159,766 | 61.598 | 20 | 24 | MISS ceiling | 127,729 | 106 | 0.425 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 150,605 | 1.506 | 20 | 50 | fits | 147,381 | 252 | 0.371 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 242,832 | 2.428 | 20 | 50 | fits | 92,623 | 138 | 0.488 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 242,766 | 2.428 | 20 | 20 | fits | 92,623 | 138 | 0.488 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 657,046 | 6.570 | 20 | 20 | fits | 25,906 | 12 | 0.800 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,544 | 0.055 | 20 | 20 | fits | 19,176 | 13 (29) | 0.645 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 8,050 | 0.081 | 20 | 20 | fits | 22,571 | 19 (35) | 0.742 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 13,468 | 0.135 | 20 | 20 | fits | 25,659 | 21 (12) | 0.783 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 9,762 | 0.098 | 20 | 50 | fits | 22,423 | 43 | 0.667 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 15,520 | 0.155 | 20 | 50 | fits | 19,020 | 35 | 0.602 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 10,546 | 0.105 | 20 | 50 | fits | 18,908 | 35 | 0.594 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 11,918 | 0.119 | 20 | 50 | fits | 23,350 | 61 | 0.539 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 13,840 | 0.138 | 20 | 50 | fits | 23,350 | 61 | 0.539 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 8,990 | 0.090 | 20 | 50 | fits | 18,784 | 30 | 0.602 |
| LINK_UP | `adp.link_up.if0` | 2,319 | 0.023 | 20 | 200 | fits | 22,423 | 43 (11) | 0.667 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,167 | 0.152 | 20 | 200 | fits | 17,269 | 23 (39) | 0.558 |
| LINK_DOWN | `adp.link_down.if0` | 1,941 | 0.019 | 20 | 200 | fits | 19,092 | 23 (9) | 0.667 |
| LINK_UP | `adp.link_up.if0` | 2,319 | 0.023 | 20 | 200 | fits | 22,423 | 43 (11) | 0.667 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,167 | 0.152 | 20 | 200 | fits | 17,269 | 23 (39) | 0.558 |
| GM_CHANGE | `adp.gm_change.if0` | 2,027 | 0.020 | 20 | 200 | fits | 11,637 | 17 (11) | 0.250 |
| LINK_UP | `adp.link_up.if0` | 2,319 | 0.023 | 20 | 200 | fits | 22,423 | 43 (11) | 0.667 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,167 | 0.152 | 20 | 200 | fits | 17,269 | 23 (39) | 0.558 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,275 | 0.043 | 20 | 200 | fits | 13,298 | 16 (31) | 0.517 |
| LINK_UP | `adp.link_up.if0` | 2,319 | 0.023 | 20 | 200 | fits | 22,423 | 43 (11) | 0.667 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,167 | 0.152 | 20 | 200 | fits | 17,269 | 23 (39) | 0.558 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,275 | 0.043 | 20 | 200 | fits | 13,298 | 16 (31) | 0.517 |
| set_name | `aecp_fanout.set_name.if0` | 43,948 | 0.439 | 20 | 24 | fits | 54,766 | 89 | 0.551 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 43,758 | 0.438 | 20 | 24 | fits | 49,536 | 78 | 0.583 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 41,844 | 0.418 | 20 | 24 | fits | 45,161 | 79 | 0.548 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 36,919 | 0.369 | 20 | 24 | fits | 42,680 | 78 | 0.514 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 52,573 | 0.526 | 20 | 24 | fits | 59,848 | 110 | 0.580 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 316,992 | 3.170 | 20 | 24 | fits | 57,907 | 110 | 0.571 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 342,396 | 3.424 | 20 | 24 | fits | 51,642 | 73 | 0.590 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 37,837 | 0.378 | 20 | 24 | fits | 43,956 | 78 | 0.533 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 41,967 | 0.420 | 20 | 24 | fits | 44,143 | 79 | 0.538 |
| BIND_RX | `acmp.bind_rx.if0` | 17,108 | 0.171 | 20 | 20 | fits | 36,701 | 26 (77) | 0.741 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,388 | 0.094 | 20 | 20 | fits | 27,268 | 19 (32) | 0.788 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,244 | 0.102 | 20 | 20 | fits | 21,449 | 15 (47) | 0.667 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 11,947 | 0.119 | 20 | 20 | fits | 33,178 | 19 (50) | 0.770 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,426 | 0.104 | 20 | 20 | fits | 23,061 | 17 (48) | 0.698 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,176 | 0.092 | 20 | 20 | fits | 21,032 | 16 (48) | 0.582 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 8,647 | 0.086 | 20 | 20 | fits | 20,236 | 16 (48) | 0.568 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 8,760 | 0.088 | 20 | 20 | fits | 20,010 | 16 (48) | 0.558 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 14,808 | 0.148 | 20 | 24 | fits | 24,022 | 20 | 0.734 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 24,620 | 0.246 | 20 | 24 | fits | 27,929 | 20 | 0.663 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 19,664 | 0.197 | 20 | 24 | fits | 24,437 | 20 | 0.685 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 20,839 | 0.208 | 20 | 24 | fits | 23,698 | 20 | 0.664 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 20,252 | 0.203 | 20 | 24 | fits | 24,652 | 20 | 0.673 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 19,558 | 0.196 | 20 | 24 | fits | 24,253 | 20 | 0.673 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 20,722 | 0.207 | 20 | 24 | fits | 23,322 | 20 | 0.671 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 19,117 | 0.191 | 20 | 24 | fits | 23,831 | 20 | 0.692 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 20,563 | 0.206 | 20 | 24 | fits | 22,948 | 20 | 0.683 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 21,290 | 0.213 | 20 | 24 | fits | 25,893 | 21 | 0.579 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 20,083 | 0.201 | 20 | 24 | fits | 22,702 | 20 | 0.704 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 18,027 | 0.180 | 20 | 24 | fits | 22,785 | 20 | 0.699 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 18,836 | 0.188 | 20 | 24 | fits | 23,515 | 20 | 0.674 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 21,287 | 0.213 | 20 | 24 | fits | 24,254 | 20 | 0.682 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 18,659 | 0.187 | 20 | 24 | fits | 23,371 | 20 | 0.690 |
| get_configuration | `aecp.get_configuration.if0` | 18,978 | 0.190 | 20 | 24 | fits | 21,327 | 20 | 0.691 |
| entity_available | `aecp.entity_available.if0` | 17,126 | 0.171 | 20 | 24 | fits | 21,537 | 20 | 0.680 |
| get_name | `aecp.get_name.if0` | 21,433 | 0.214 | 20 | 24 | fits | 24,333 | 20 | 0.712 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 21,207 | 0.212 | 20 | 24 | fits | 26,434 | 26 | 0.694 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 20,813 | 0.208 | 20 | 24 | fits | 25,585 | 29 | 0.708 |
| get_as_path, refused ENTITY_MISBEHAVING | `aecp.get_as_path.if0` | 11,505 | 0.115 | 20 | 24 | fits | 25,177 | 29 | 0.725 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 16,923 | 0.169 | 20 | 24 | fits | 21,471 | 20 | 0.705 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 13,720 | 0.137 | 20 | 24 | fits | 20,433 | 20 | 0.655 |
| set_name | `aecp.set_name.if0` | 25,873 | 0.259 | 20 | 24 | fits | 42,113 | 43 | 0.739 |
| lock_entity | `aecp.lock_entity.if0` | 14,883 | 0.149 | 20 | 24 | fits | 33,432 | 34 | 0.768 |
| unlock_entity | `aecp.unlock_entity.if0` | 23,172 | 0.232 | 20 | 24 | fits | 31,994 | 33 | 0.744 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 130,372 | 1.304 | 20 | 24 | fits | 142,061 | 137 | 0.308 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 269,844 | 2.698 | 20 | 24 | fits | 134,945 | 114 | 0.293 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 241,812 | 2.418 | 20 | 24 | fits | 40,244 | 18 | 0.661 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 372,969 | 3.730 | 20 | 24 | fits | 78,520 | 17 | 0.665 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 362,032 | 3.620 | 20 | 24 | fits | 88,535 | 17 | 0.665 |
| READ_DESCRIPTOR held for a token (#917) | `aecp.held.read_descriptor.if0` | 514,195 | 5.142 | 20 | 24 | fits | 27,506 | 17 | 0.685 |
| LINK_UP | `fixture.link_up.if0` | 2,319 | 0.023 | 20 | 200 | fits | 22,423 | 43 (11) | 0.667 |
| malformed MRPDU discard | `fixture.malformed.if0` | 16,797 | 0.168 | 20 | 20 | fits | 16,863 | 12 | 0.682 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 30,702 | 0.307 | 20 | 24 | fits | 43,683 | 43 | 0.764 |
| LINK_DOWN | `fixture.link_down.if0` | 2,454 | 0.025 | 20 | 200 | fits | 21,113 | 23 (9) | 0.719 |
| BIND_RX | `fixture.bind_rx.if0` | 18,083 | 0.181 | 20 | 20 | fits | 37,304 | 26 (77) | 0.750 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 20,682 | 0.207 | 20 | 20 | fits | 32,942 | 29 (35) | 0.754 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 15,895 | 0.159 | 20 | 20 | fits | 20,907 | 13 (29) | 0.726 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 77,689 | 0.777 | 20 | 200 | fits | 77,793 | 77 | 0.725 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 77,689 | 0.777 | 20 | 200 | fits | 77,793 | 77 | 0.725 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 77,415 | 0.774 | 20 | 20 | fits | 77,793 | 77 | 0.725 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 77,415 | 0.774 | 20 | 20 | fits | 77,793 | 77 | 0.725 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 77,623 | 0.776 | 20 | 24 | fits | 77,793 | 77 | 0.725 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 77,623 | 0.776 | 20 | 24 | fits | 77,793 | 77 | 0.725 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 77,557 | 0.776 | 20 | 50 | fits | 77,793 | 77 | 0.725 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 77,557 | 0.776 | 20 | 50 | fits | 77,793 | 77 | 0.725 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 77,491 | 0.775 | 20 | 20 | fits | 77,793 | 77 | 0.725 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 77,491 | 0.775 | 20 | 20 | fits | 77,793 | 77 | 0.725 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
