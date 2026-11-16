### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 92 paths and 7 of 950 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.195 (0.414) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.090 (0.245) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.081 (0.266) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.196 (0.548) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.105 (0.262) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.090 (0.243) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.093 (0.253) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.107 (0.267) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.095 (0.320) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.246 (0.605) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.127 (0.490) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.191 (0.534) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.160 (0.496) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.179 (0.609) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.135 (0.494) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.129 (0.382) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.046 (0.172) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.024 (0.177) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.026 (0.265) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.026 (0.271) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.095 (0.260) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.095 (0.424) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.275 (0.591) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.269 (0.588) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.118 (0.433) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.151 (0.469) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.256 (0.587) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.188 (0.549) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.159 (0.465) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.192 (0.519) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.259 (0.580) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.255 (0.573) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.143 (0.464) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.277 (0.594) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.134 (0.456) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.135 (0.456) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.151 (0.474) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.252 (0.569) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.152 (0.474) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.255 (0.576) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.262 (0.580) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.263 (0.590) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.141 (0.462) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.249 (0.563) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.216 (0.640) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.128 (0.444) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.159 (0.369) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.670 (2.995) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.405 (0.509) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.507 (0.833) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.440 (0.572) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.481 (0.771) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.520 (0.860) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.254 (3.581) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.453 (0.743) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 3.165 (3.511) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.173 (2.553) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.834 (4.205) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.069 (3.432) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.348 (1.515) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.992 (4.215) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 4.371 (5.084) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.156 (0.522) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.702 (2.127) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.905 (63.201) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.652 (63.948) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.317 (0.464) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 2.310 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 1.577 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 2.998 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 1.915 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 9.921 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.158 (0.498) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.095 (0.224) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.100 (0.271) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.136 (0.498) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.094 (0.417) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.655 | fits | 0 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.169 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.002 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.213 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 4.944 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.303 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.736 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.195 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.maap.last.if0` (backlog-adp@program-aged2-7) | 4.981 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-5.service.srp.first.if0` (backlog-adp@verify-aged2-5) | 5.953 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-5.service.srp.last.if0` (backlog-adp@verify-aged2-5) | 10.976 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.904 (0.996) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.449 (0.450) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.218 (0.219) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.774 (0.856) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 12.017 | 11 | 152,921 (1.529) | yes | - |
| backlog-adp@blank-1 | 0 | 11.266 | 11 | 152,439 (1.524) | yes | - |
| backlog-adp@blank-2 | 0 | 11.288 | 11 | 152,439 (1.524) | yes | - |
| backlog-adp@blank-3 | 0 | 11.788 | 13 | 152,439 (1.524) | yes | - |
| backlog-adp@blank-4 | 0 | 11.808 | 13 | 152,439 (1.524) | yes | - |
| backlog-adp@blank-5 | 0 | 11.493 | 13 | 152,583 (1.526) | yes | - |
| backlog-adp@blank-6 | 0 | 11.380 | 11 | 152,355 (1.524) | yes | - |
| backlog-adp@blank-7 | 0 | 13.117 | 13 | 149,918 (1.499) | yes | - |
| backlog-adp@program-0 | 0 | 11.381 | 11 | 152,898 (1.529) | yes | - |
| backlog-adp@program-1 | 0 | 11.457 | 12 | 153,086 (1.531) | yes | - |
| backlog-adp@program-2 | 0 | 11.300 | 11 | 152,454 (1.525) | yes | - |
| backlog-adp@program-3 | 0 | 11.958 | 12 | 152,454 (1.525) | yes | - |
| backlog-adp@program-4 | 0 | 10.543 | 11 | 153,491 (1.535) | yes | - |
| backlog-adp@program-5 | 0 | 10.544 | 11 | 152,542 (1.525) | yes | - |
| backlog-adp@program-6 | 0 | 10.613 | 11 | 152,542 (1.525) | yes | - |
| backlog-adp@program-7 | 0 | 11.092 | 13 | 152,575 (1.526) | yes | - |
| backlog-adp@verify-0 | 0 | 11.647 | 11 | 153,133 (1.531) | yes | - |
| backlog-adp@verify-1 | 0 | 11.385 | 11 | 152,733 (1.527) | yes | - |
| backlog-adp@verify-2 | 0 | 11.225 | 11 | 152,700 (1.527) | yes | - |
| backlog-adp@verify-3 | 0 | 11.740 | 13 | 152,700 (1.527) | yes | - |
| backlog-adp@verify-4 | 0 | 11.438 | 12 | 152,846 (1.528) | yes | - |
| backlog-adp@verify-5 | 0 | 11.327 | 11 | 147,388 (1.474) | yes | - |
| backlog-adp@verify-6 | 0 | 11.377 | 11 | 152,613 (1.526) | yes | - |
| backlog-adp@verify-7 | 0 | 12.357 | 11 | 149,366 (1.494) | yes | - |
| backlog-adp@blank-aged2-0 | 1 | 11.562 | 12 | 150,663 (1.507) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 11.369 | 11 | 147,070 (1.471) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 11.436 | 12 | 151,586 (1.516) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 11.276 | 11 | 152,026 (1.520) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 11.210 | 10 | 151,258 (1.513) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 11.372 | 11 | 152,073 (1.521) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 11.680 | 13 | 152,026 (1.520) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 12.638 | 14 | 152,073 (1.521) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 12.120 | 14 | 152,156 (1.522) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 12.120 | 13 | 152,156 (1.522) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 12.440 | 15 | 152,109 (1.521) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 12.106 | 14 | 152,223 (1.522) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 12.095 | 13 | 152,005 (1.520) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 12.032 | 13 | 152,052 (1.521) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 11.977 | 12 | 152,005 (1.520) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 12.413 | 14 | 146,830 (1.468) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.363 | 13 | 152,427 (1.524) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 11.392 | 11 | 152,255 (1.523) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 11.335 | 11 | 152,302 (1.523) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 11.307 | 11 | 152,255 (1.523) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 11.384 | 11 | 152,255 (1.523) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 11.502 | 12 | 152,302 (1.523) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 11.437 | 12 | 152,432 (1.524) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 11.645 | 12 | 152,160 (1.522) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 11.894 | 14 | 152,255 (1.523) | yes | - |
| backlog-adp@program-aged1-1 | 1 | 11.403 | 11 | 149,994 (1.500) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 11.372 | 11 | 146,653 (1.467) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 11.314 | 11 | 152,286 (1.523) | yes | - |
| backlog-adp@program-aged1-4 | 1 | 11.292 | 10 | 149,846 (1.498) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 11.413 | 11 | 152,239 (1.522) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 11.801 | 13 | 152,286 (1.523) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 11.839 | 13 | 152,239 (1.522) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.263 | 12 | 152,135 (1.521) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 11.262 | 10 | 146,582 (1.466) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 11.324 | 11 | 152,182 (1.522) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 11.598 | 13 | 152,135 (1.521) | yes | - |
| backlog-adp@verify-aged2-4 | 1 | 11.362 | 11 | 151,495 (1.515) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 11.506 | 12 | 152,298 (1.523) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 11.317 | 11 | 152,364 (1.524) | yes | - |
| backlog-adp@verify-aged2-7 | 1 | 12.228 | 11 | 149,802 (1.498) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 11.450 | 12 | 152,267 (1.523) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 11.266 | 11 | 152,317 (1.523) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 11.249 | 10 | 146,555 (1.466) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 11.340 | 11 | 152,364 (1.524) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 11.269 | 11 | 152,317 (1.523) | yes | - |
| backlog-adp@verify-aged1-5 | 1 | 11.633 | 12 | 151,414 (1.514) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 11.498 | 12 | 152,532 (1.525) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 12.390 | 12 | 152,056 (1.521) | yes | - |
| backlog | 0 | 5.629 | 7 | 156,321 (1.563) | yes | - |
| backlog-adp | 0 | 10.469 | 11 | 152,335 (1.523) | yes | - |
| backlog-adp-refill | 0 | 40.846 | 26 | 152,335 (1.523) | yes | - |
| backlog-owed | 0 | 64.307 | 26 | 149,154 (1.492) | yes | - |
| fixture | 0 | 1.308 | 2 | 81,156 (0.812) | yes | - |

Composed maximum over the 4 backlog windows: 156,321 CPU cycles (1.563 ms), backlog.
Over the windows that released their whole load only: 156,321 (1.563 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3609 | 0 | 41,470 (0.415) | fits |
| save-second | 44401 | 0 | 50,275 (0.503) | fits |
| backlog-adp@blank-0 | 416 | 0 | 152,921 (1.529) | fits |
| backlog-adp@blank-1 | 416 | 0 | 152,439 (1.524) | fits |
| backlog-adp@blank-2 | 416 | 0 | 152,439 (1.524) | fits |
| backlog-adp@blank-3 | 418 | 0 | 152,439 (1.524) | fits |
| backlog-adp@blank-4 | 418 | 0 | 152,439 (1.524) | fits |
| backlog-adp@blank-5 | 418 | 0 | 152,583 (1.526) | fits |
| backlog-adp@blank-6 | 418 | 0 | 152,355 (1.524) | fits |
| backlog-adp@blank-7 | 421 | 0 | 152,322 (1.523) | fits |
| backlog-adp@program-0 | 519 | 0 | 152,898 (1.529) | fits |
| backlog-adp@program-1 | 520 | 0 | 153,086 (1.531) | fits |
| backlog-adp@program-2 | 521 | 0 | 152,454 (1.525) | fits |
| backlog-adp@program-3 | 522 | 0 | 152,454 (1.525) | fits |
| backlog-adp@program-4 | 522 | 0 | 153,491 (1.535) | fits |
| backlog-adp@program-5 | 524 | 0 | 152,542 (1.525) | fits |
| backlog-adp@program-6 | 524 | 0 | 152,542 (1.525) | fits |
| backlog-adp@program-7 | 526 | 0 | 152,575 (1.526) | fits |
| backlog-adp@verify-0 | 614 | 0 | 153,133 (1.531) | fits |
| backlog-adp@verify-1 | 614 | 0 | 152,733 (1.527) | fits |
| backlog-adp@verify-2 | 614 | 0 | 152,700 (1.527) | fits |
| backlog-adp@verify-3 | 616 | 0 | 152,700 (1.527) | fits |
| backlog-adp@verify-4 | 615 | 0 | 152,846 (1.528) | fits |
| backlog-adp@verify-5 | 615 | 0 | 147,388 (1.474) | fits |
| backlog-adp@verify-6 | 616 | 0 | 152,613 (1.526) | fits |
| backlog-adp@verify-7 | 617 | 0 | 152,580 (1.526) | fits |
| backlog-adp@blank-aged2-0 | 699 | 0 | 150,663 (1.507) | fits |
| backlog-adp@blank-aged2-1 | 703 | 0 | 152,451 (1.525) | fits |
| backlog-adp@blank-aged2-2 | 711 | 0 | 151,586 (1.516) | fits |
| backlog-adp@blank-aged2-3 | 717 | 0 | 152,026 (1.520) | fits |
| backlog-adp@blank-aged2-4 | 724 | 0 | 152,073 (1.521) | fits |
| backlog-adp@blank-aged2-5 | 732 | 0 | 152,073 (1.521) | fits |
| backlog-adp@blank-aged2-6 | 741 | 0 | 152,026 (1.520) | fits |
| backlog-adp@blank-aged2-7 | 749 | 0 | 152,073 (1.521) | fits |
| backlog-adp@blank-aged1-0 | 642 | 0 | 152,156 (1.522) | fits |
| backlog-adp@blank-aged1-1 | 649 | 0 | 152,156 (1.522) | fits |
| backlog-adp@blank-aged1-2 | 658 | 0 | 152,109 (1.521) | fits |
| backlog-adp@blank-aged1-3 | 664 | 0 | 152,223 (1.522) | fits |
| backlog-adp@blank-aged1-4 | 671 | 0 | 152,005 (1.520) | fits |
| backlog-adp@blank-aged1-5 | 678 | 0 | 152,052 (1.521) | fits |
| backlog-adp@blank-aged1-6 | 684 | 0 | 152,005 (1.520) | fits |
| backlog-adp@blank-aged1-7 | 694 | 0 | 152,494 (1.525) | fits |
| backlog-adp@program-aged2-0 | 797 | 0 | 152,427 (1.524) | fits |
| backlog-adp@program-aged2-1 | 803 | 0 | 152,255 (1.523) | fits |
| backlog-adp@program-aged2-2 | 810 | 0 | 152,302 (1.523) | fits |
| backlog-adp@program-aged2-3 | 817 | 0 | 152,255 (1.523) | fits |
| backlog-adp@program-aged2-4 | 825 | 0 | 152,255 (1.523) | fits |
| backlog-adp@program-aged2-5 | 833 | 0 | 152,302 (1.523) | fits |
| backlog-adp@program-aged2-6 | 840 | 0 | 152,432 (1.524) | fits |
| backlog-adp@program-aged2-7 | 848 | 0 | 152,160 (1.522) | fits |
| backlog-adp@program-aged1-0 | 740 | 0 | 152,255 (1.523) | fits |
| backlog-adp@program-aged1-1 | 745 | 0 | 152,506 (1.525) | fits |
| backlog-adp@program-aged1-2 | 752 | 0 | 153,320 (1.533) | fits |
| backlog-adp@program-aged1-3 | 759 | 0 | 152,286 (1.523) | fits |
| backlog-adp@program-aged1-4 | 766 | 0 | 152,239 (1.522) | fits |
| backlog-adp@program-aged1-5 | 774 | 0 | 152,239 (1.522) | fits |
| backlog-adp@program-aged1-6 | 783 | 0 | 152,286 (1.523) | fits |
| backlog-adp@program-aged1-7 | 790 | 0 | 152,239 (1.522) | fits |
| backlog-adp@verify-aged2-0 | 894 | 0 | 152,135 (1.521) | fits |
| backlog-adp@verify-aged2-1 | 900 | 0 | 152,182 (1.522) | fits |
| backlog-adp@verify-aged2-2 | 908 | 0 | 152,182 (1.522) | fits |
| backlog-adp@verify-aged2-3 | 917 | 0 | 152,135 (1.521) | fits |
| backlog-adp@verify-aged2-4 | 923 | 0 | 152,346 (1.523) | fits |
| backlog-adp@verify-aged2-5 | 931 | 0 | 152,298 (1.523) | fits |
| backlog-adp@verify-aged2-6 | 937 | 0 | 152,364 (1.524) | fits |
| backlog-adp@verify-aged2-7 | 945 | 0 | 152,317 (1.523) | fits |
| backlog-adp@verify-aged1-0 | 836 | 0 | 152,267 (1.523) | fits |
| backlog-adp@verify-aged1-1 | 842 | 0 | 152,317 (1.523) | fits |
| backlog-adp@verify-aged1-2 | 849 | 0 | 152,364 (1.524) | fits |
| backlog-adp@verify-aged1-3 | 857 | 0 | 152,364 (1.524) | fits |
| backlog-adp@verify-aged1-4 | 864 | 0 | 152,317 (1.523) | fits |
| backlog-adp@verify-aged1-5 | 873 | 0 | 152,364 (1.524) | fits |
| backlog-adp@verify-aged1-6 | 880 | 0 | 152,532 (1.525) | fits |
| backlog-adp@verify-aged1-7 | 887 | 0 | 152,056 (1.521) | fits |
| adp-advertise | 598 | 0 | 30,305 (0.303) | fits |
| save-held | 1467 | 0 | 158,615 (1.586) | fits |
| save-starved | 23468 | 0 | 158,615 (1.586) | fits |
| acmp-noresp | 2023 | 0 | 41,470 (0.415) | fits |
| save | 610 | 0 | 45,514 (0.455) | fits |
| srp | 290 | 0 | 57,083 (0.571) | fits |
| backlog | 286 | 0 | 156,321 (1.563) | fits |
| backlog-adp | 315 | 0 | 152,335 (1.523) | fits |
| backlog-adp-refill | 330 | 0 | 152,335 (1.523) | fits |
| backlog-owed | 311 | 0 | 149,154 (1.492) | fits |
| acmp-disc | 937 | 0 | 41,470 (0.415) | fits |
| maap | 182 | 0 | 30,305 (0.303) | fits |
| adp-link | 89 | 0 | 39,548 (0.395) | fits |
| adp-gm | 88 | 0 | 30,305 (0.303) | fits |
| adp-discover | 88 | 0 | 30,305 (0.303) | fits |
| control | 88 | 0 | 30,305 (0.303) | fits |
| aecp-fanout | 112 | 0 | 67,866 (0.679) | fits |
| acmp-cmd | 85 | 0 | 41,470 (0.415) | fits |
| aecp | 111 | 0 | 44,645 (0.446) | fits |
| aecp-largest-notice | 105 | 0 | 151,514 (1.515) | fits |
| datapath-events | 116 | 0 | 30,305 (0.303) | fits |
| fixture | 151 | 0 | 81,156 (0.812) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | +9.981 ms, 76,849 (0.768 ms), read-back | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 9.943 (20) | 10.057 |
| backlog-adp@blank-aged2-1 | 2 | +9.209 ms, 76,849 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 10.711 (20) | 9.289 |
| backlog-adp@blank-aged2-2 | 2 | none | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 10.906 (20) | 9.094 |
| backlog-adp@blank-aged2-3 | 2 | +6.554 ms, 76,849 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 10.745 (20) | 9.255 |
| backlog-adp@blank-aged2-4 | 2 | none | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 10.679 (20) | 9.321 |
| backlog-adp@blank-aged2-5 | 2 | +4.200 ms, 77,111 (0.771 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 10.842 (20) | 9.158 |
| backlog-adp@blank-aged2-6 | 2 | +4.263 ms, 77,111 (0.771 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 10.729 (20) | 9.271 |
| backlog-adp@blank-aged2-7 | 2 | none | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 10.689 (20) | 9.311 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 9.888 (20) | 10.112 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 10.473 (20) | 9.527 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 10.729 (20) | 9.271 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 10.820 (20) | 9.180 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 10.809 (20) | 9.191 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 10.746 (20) | 9.254 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 10.689 (20) | 9.311 |
| backlog-adp@blank-aged1-7 | 1 | none | +10.840 ms, 76,651 (0.767 ms), read-back | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 10.597 (20) | 9.403 |
| backlog-adp@program-aged2-0 | 2 | none | +10.215 ms, 80,351 (0.804 ms), issue | `backlog-adp@program-aged2-0.service.srp.last.if0` | 9.828 (20) | 10.172 |
| backlog-adp@program-aged2-1 | 2 | +9.226 ms, 80,828 (0.808 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 10.856 (20) | 9.144 |
| backlog-adp@program-aged2-2 | 2 | +8.309 ms, 80,828 (0.808 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 10.801 (20) | 9.199 |
| backlog-adp@program-aged2-3 | 2 | +6.563 ms, 80,828 (0.808 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 10.773 (20) | 9.227 |
| backlog-adp@program-aged2-4 | 2 | +5.910 ms, 80,828 (0.808 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 10.851 (20) | 9.149 |
| backlog-adp@program-aged2-5 | 2 | +4.306 ms, 80,640 (0.806 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 10.969 (20) | 9.031 |
| backlog-adp@program-aged2-6 | 2 | +4.239 ms, 80,558 (0.806 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 10.906 (20) | 9.094 |
| backlog-adp@program-aged2-7 | 2 | +3.142 ms, 80,286 (0.803 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 10.869 (20) | 9.131 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 9.897 (20) | 10.103 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 9.942 (20) | 10.058 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 10.033 (20) | 9.967 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 9.976 (20) | 10.024 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 9.954 (20) | 10.046 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 10.073 (20) | 9.927 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 10.000 (20) | 10.000 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 9.944 (20) | 10.056 |
| backlog-adp@verify-aged2-0 | 2 | none | +10.151 ms, 77,343 (0.773 ms), read-back | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 9.910 (20) | 10.090 |
| backlog-adp@verify-aged2-1 | 2 | +9.132 ms, 77,541 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 10.727 (20) | 9.273 |
| backlog-adp@verify-aged2-2 | 2 | +8.461 ms, 77,541 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 10.791 (20) | 9.209 |
| backlog-adp@verify-aged2-3 | 2 | +6.724 ms, 77,541 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 10.771 (20) | 9.229 |
| backlog-adp@verify-aged2-4 | 2 | +5.776 ms, 77,375 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 10.828 (20) | 9.172 |
| backlog-adp@verify-aged2-5 | 2 | +4.338 ms, 77,749 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 10.976 (20) | 9.024 |
| backlog-adp@verify-aged2-6 | 2 | +4.140 ms, 77,749 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 10.786 (20) | 9.214 |
| backlog-adp@verify-aged2-7 | 2 | +4.088 ms, 77,749 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 10.739 (20) | 9.261 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 10.031 (20) | 9.969 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 9.971 (20) | 10.029 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 9.954 (20) | 10.046 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 10.045 (20) | 9.955 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 9.974 (20) | 10.026 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 9.916 (20) | 10.084 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 10.203 (20) | 9.797 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 9.983 (20) | 10.017 |

Least margin over the aged windows: 9.024 ms, `backlog-adp@verify-aged2-5.service.srp.last.if0` at 10.976 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.359 | 6,070 | 102 | 2 | 30.861 | yes | within |
| save-held | 2019.304 | 4,070 | 102 | - | 15.519 | no | within |
| save-starved | 4049.131 | 4,070 | 102 | - | 31.117 | yes | within |
| save | 2019.618 | 4,070 | 102 | - | 10.875 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 97,734 (0.977) | 78,205 (0.782) |
| save-second | 520 | 80,198 (0.802) | 77,905 (0.779) |
| backlog-adp@blank-0 | 299 | 92,604 (0.926) | 76,292 (0.763) |
| backlog-adp@blank-1 | 299 | 92,481 (0.925) | 76,290 (0.763) |
| backlog-adp@blank-2 | 299 | 92,481 (0.925) | 76,290 (0.763) |
| backlog-adp@blank-3 | 299 | 92,834 (0.928) | 76,290 (0.763) |
| backlog-adp@blank-4 | 299 | 92,973 (0.930) | 76,234 (0.762) |
| backlog-adp@blank-5 | 299 | 91,558 (0.916) | 76,192 (0.762) |
| backlog-adp@blank-6 | 299 | 92,327 (0.923) | 76,242 (0.762) |
| backlog-adp@blank-7 | 300 | 97,347 (0.973) | 76,242 (0.762) |
| backlog-adp@program-0 | 328 | 96,998 (0.970) | 78,946 (0.789) |
| backlog-adp@program-1 | 328 | 98,661 (0.987) | 78,829 (0.788) |
| backlog-adp@program-2 | 328 | 96,998 (0.970) | 78,944 (0.789) |
| backlog-adp@program-3 | 329 | 96,998 (0.970) | 78,944 (0.789) |
| backlog-adp@program-4 | 329 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@program-5 | 329 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@program-6 | 329 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@program-7 | 329 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-0 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-1 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-2 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-3 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-4 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-5 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-6 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-7 | 356 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@blank-aged2-0 | 297 | 76,849 (0.768) | 75,671 (0.757) |
| backlog-adp@blank-aged2-1 | 297 | 76,849 (0.768) | 75,671 (0.757) |
| backlog-adp@blank-aged2-2 | 297 | 85,954 (0.860) | 75,913 (0.759) |
| backlog-adp@blank-aged2-3 | 297 | 76,849 (0.768) | 75,671 (0.757) |
| backlog-adp@blank-aged2-4 | 297 | 86,037 (0.860) | 75,913 (0.759) |
| backlog-adp@blank-aged2-5 | 297 | 77,111 (0.771) | 75,726 (0.757) |
| backlog-adp@blank-aged2-6 | 297 | 77,111 (0.771) | 75,726 (0.757) |
| backlog-adp@blank-aged2-7 | 298 | 92,077 (0.921) | 75,995 (0.760) |
| backlog-adp@blank-aged1-0 | 297 | 97,939 (0.979) | 76,126 (0.761) |
| backlog-adp@blank-aged1-1 | 297 | 98,135 (0.981) | 76,146 (0.761) |
| backlog-adp@blank-aged1-2 | 297 | 99,620 (0.996) | 76,530 (0.765) |
| backlog-adp@blank-aged1-3 | 297 | 92,315 (0.923) | 76,243 (0.762) |
| backlog-adp@blank-aged1-4 | 297 | 92,374 (0.924) | 76,243 (0.762) |
| backlog-adp@blank-aged1-5 | 297 | 92,374 (0.924) | 76,243 (0.762) |
| backlog-adp@blank-aged1-6 | 297 | 92,463 (0.925) | 76,243 (0.762) |
| backlog-adp@blank-aged1-7 | 297 | 76,651 (0.767) | 75,555 (0.756) |
| backlog-adp@program-aged2-0 | 326 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@program-aged2-1 | 326 | 96,998 (0.970) | 78,500 (0.785) |
| backlog-adp@program-aged2-2 | 326 | 96,998 (0.970) | 78,500 (0.785) |
| backlog-adp@program-aged2-3 | 326 | 96,998 (0.970) | 78,500 (0.785) |
| backlog-adp@program-aged2-4 | 326 | 96,998 (0.970) | 78,500 (0.785) |
| backlog-adp@program-aged2-5 | 326 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@program-aged2-6 | 326 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@program-aged2-7 | 327 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@program-aged1-0 | 326 | 96,998 (0.970) | 78,830 (0.788) |
| backlog-adp@program-aged1-1 | 326 | 98,379 (0.984) | 78,829 (0.788) |
| backlog-adp@program-aged1-2 | 326 | 96,998 (0.970) | 78,944 (0.789) |
| backlog-adp@program-aged1-3 | 326 | 96,998 (0.970) | 78,944 (0.789) |
| backlog-adp@program-aged1-4 | 326 | 96,998 (0.970) | 78,944 (0.789) |
| backlog-adp@program-aged1-5 | 326 | 96,998 (0.970) | 78,944 (0.789) |
| backlog-adp@program-aged1-6 | 326 | 96,998 (0.970) | 78,944 (0.789) |
| backlog-adp@program-aged1-7 | 327 | 96,998 (0.970) | 78,944 (0.789) |
| backlog-adp@verify-aged2-0 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged2-1 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged2-2 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged2-3 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged2-4 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged2-5 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged2-6 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged2-7 | 356 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged1-0 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged1-1 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged1-2 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged1-3 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged1-4 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged1-5 | 355 | 100,110 (1.001) | 78,341 (0.783) |
| backlog-adp@verify-aged1-6 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged1-7 | 356 | 96,998 (0.970) | 78,341 (0.783) |
| adp-advertise | 577 | 22,507 (0.225) | 2,414 (0.024) |
| save-held | 722 | 95,696 (0.957) | 78,773 (0.788) |
| save-starved | 418 | 80,927 (0.809) | 78,361 (0.784) |
| acmp-noresp | 615 | 97,311 (0.973) | 78,205 (0.782) |
| save | 585 | 96,547 (0.965) | 78,190 (0.782) |
| srp | 271 | 22,507 (0.225) | 2,414 (0.024) |
| backlog | 265 | 22,507 (0.225) | 2,414 (0.024) |
| backlog-adp | 271 | 22,507 (0.225) | 2,414 (0.024) |
| backlog-adp-refill | 274 | 22,507 (0.225) | 2,414 (0.024) |
| backlog-owed | 276 | 22,507 (0.225) | 2,414 (0.024) |
| acmp-disc | 305 | 97,227 (0.972) | 78,205 (0.782) |
| maap | 169 | 22,437 (0.224) | 2,414 (0.024) |
| adp-link | 79 | 22,267 (0.223) | 2,414 (0.024) |
| adp-gm | 79 | 22,267 (0.223) | 2,414 (0.024) |
| adp-discover | 79 | 22,267 (0.223) | 2,414 (0.024) |
| control | 79 | 22,267 (0.223) | 2,414 (0.024) |
| aecp-fanout | 80 | 23,660 (0.237) | 3,978 (0.040) |
| acmp-cmd | 65 | 22,267 (0.223) | 2,414 (0.024) |
| aecp | 79 | 22,267 (0.223) | 2,414 (0.024) |
| aecp-largest-notice | 78 | 22,267 (0.223) | 2,414 (0.024) |
| datapath-events | 69 | 22,267 (0.223) | 2,414 (0.024) |
| fixture | 54 | 20,164 (0.202) | 2,414 (0.024) |

Longest pass that carries a step: 100,110 CPU cycles (1.001 ms), backlog-adp@verify-aged1-5; longest step: 78,946 (0.789 ms), backlog-adp@program-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 17,863 | 0.179 | 20 | 20 | fits | 33,906 | 19 (14) | 0.887 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 422,956 | 4.230 | 20 | 20 | fits | 97,380 | 151 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 377,027 | 3.770 | 20 | 200 | fits | 151,282 | 237 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 473,791 | 4.738 | 20 | 200 | fits | 97,380 | 151 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 377,951 | 3.780 | 20 | 20 | fits | 151,282 | 237 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 474,495 | 4.745 | 20 | 20 | fits | 97,380 | 151 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 230,309 | 2.303 | 20 | 24 | fits | 152,921 | 155 | 0.372 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 380,601 | 3.806 | 20 | 24 | fits | 151,282 | 237 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 380,535 | 3.805 | 20 | 50 | fits | 151,282 | 237 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 477,519 | 4.775 | 20 | 50 | fits | 97,380 | 151 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 564,152 | 5.642 | 20 | 20 | fits | 86,699 | 24 | 0.793 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,072,710 | 10.727 | 20 | 20 | fits | 78,989 | 30 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 340,604 | 3.406 | 20 | 20 | fits | 101,449 | 142 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 297,370 | 2.974 | 20 | 200 | fits | 148,480 | 248 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 398,203 | 3.982 | 20 | 200 | fits | 101,449 | 142 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 298,294 | 2.983 | 20 | 20 | fits | 148,480 | 248 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 398,907 | 3.989 | 20 | 20 | fits | 101,449 | 142 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 153,454 | 1.535 | 20 | 24 | fits | 152,439 | 155 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 300,944 | 3.009 | 20 | 24 | fits | 148,480 | 248 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 300,878 | 3.009 | 20 | 50 | fits | 148,480 | 248 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 401,931 | 4.019 | 20 | 50 | fits | 101,449 | 142 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 488,531 | 4.885 | 20 | 20 | fits | 86,666 | 24 | 0.793 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 997,676 | 9.977 | 20 | 20 | fits | 85,977 | 28 | 0.646 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 350,732 | 3.507 | 20 | 20 | fits | 98,328 | 154 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 302,697 | 3.027 | 20 | 200 | fits | 149,935 | 233 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 400,409 | 4.004 | 20 | 200 | fits | 98,328 | 154 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 303,621 | 3.036 | 20 | 20 | fits | 149,935 | 233 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 401,113 | 4.011 | 20 | 20 | fits | 98,328 | 154 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 157,326 | 1.573 | 20 | 24 | fits | 152,439 | 155 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 306,271 | 3.063 | 20 | 24 | fits | 149,935 | 233 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 306,205 | 3.062 | 20 | 50 | fits | 149,935 | 233 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 404,137 | 4.041 | 20 | 50 | fits | 98,328 | 154 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 490,932 | 4.909 | 20 | 20 | fits | 86,861 | 25 | 0.792 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 999,926 | 9.999 | 20 | 20 | fits | 85,624 | 28 | 0.639 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 355,634 | 3.556 | 20 | 20 | fits | 103,403 | 158 | 0.488 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 308,007 | 3.080 | 20 | 200 | fits | 151,373 | 238 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 420,236 | 4.202 | 20 | 200 | fits | 103,403 | 158 | 0.488 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 308,931 | 3.089 | 20 | 20 | fits | 151,373 | 238 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 420,940 | 4.209 | 20 | 20 | fits | 103,403 | 158 | 0.488 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 161,198 | 1.612 | 20 | 24 | fits | 152,439 | 155 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 311,581 | 3.116 | 20 | 24 | fits | 151,373 | 238 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 311,515 | 3.115 | 20 | 50 | fits | 151,373 | 238 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 423,964 | 4.240 | 20 | 50 | fits | 103,403 | 158 | 0.488 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 510,425 | 5.104 | 20 | 20 | fits | 86,527 | 24 | 0.791 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 1,003,634 | 10.036 | 20 | 20 | fits | 73,137 | 24 | 0.673 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 364,659 | 3.647 | 20 | 20 | fits | 102,163 | 142 | 0.452 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 311,252 | 3.113 | 20 | 200 | fits | 150,746 | 254 | 0.378 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 422,220 | 4.222 | 20 | 200 | fits | 102,163 | 142 | 0.452 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 312,176 | 3.122 | 20 | 20 | fits | 150,746 | 254 | 0.378 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 422,924 | 4.229 | 20 | 20 | fits | 102,163 | 142 | 0.452 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 165,070 | 1.651 | 20 | 24 | fits | 152,439 | 155 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 314,826 | 3.148 | 20 | 24 | fits | 150,746 | 254 | 0.378 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 314,760 | 3.148 | 20 | 50 | fits | 150,746 | 254 | 0.378 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 425,948 | 4.259 | 20 | 50 | fits | 102,163 | 142 | 0.452 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 512,480 | 5.125 | 20 | 20 | fits | 86,598 | 24 | 0.793 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 1,005,422 | 10.054 | 20 | 20 | fits | 73,054 | 24 | 0.671 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 338,321 | 3.383 | 20 | 20 | fits | 105,502 | 160 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 304,330 | 3.043 | 20 | 200 | fits | 146,998 | 235 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 409,216 | 4.092 | 20 | 200 | fits | 105,502 | 160 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 305,254 | 3.053 | 20 | 20 | fits | 146,998 | 235 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 409,920 | 4.099 | 20 | 20 | fits | 105,502 | 160 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 152,977 | 1.530 | 20 | 24 | fits | 152,583 | 156 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 307,904 | 3.079 | 20 | 24 | fits | 146,998 | 235 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 307,838 | 3.078 | 20 | 50 | fits | 146,998 | 235 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 412,944 | 4.129 | 20 | 50 | fits | 105,502 | 160 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 491,557 | 4.916 | 20 | 20 | fits | 78,679 | 26 | 0.825 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 990,873 | 9.909 | 20 | 20 | fits | 73,134 | 25 | 0.670 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 359,206 | 3.592 | 20 | 20 | fits | 108,841 | 148 | 0.472 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 308,450 | 3.084 | 20 | 200 | fits | 148,403 | 248 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 416,675 | 4.167 | 20 | 200 | fits | 108,841 | 148 | 0.472 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 309,374 | 3.094 | 20 | 20 | fits | 148,403 | 248 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 417,379 | 4.174 | 20 | 20 | fits | 108,841 | 148 | 0.472 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 164,611 | 1.646 | 20 | 24 | fits | 152,355 | 155 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 312,024 | 3.120 | 20 | 24 | fits | 148,403 | 248 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 311,958 | 3.120 | 20 | 50 | fits | 148,403 | 248 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 420,403 | 4.204 | 20 | 50 | fits | 108,841 | 148 | 0.472 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 507,106 | 5.071 | 20 | 20 | fits | 86,769 | 24 | 0.794 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 1,009,369 | 10.094 | 20 | 20 | fits | 73,275 | 24 | 0.684 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 345,377 | 3.454 | 20 | 20 | fits | 106,465 | 163 | 0.435 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 297,436 | 2.974 | 20 | 200 | fits | 149,918 | 231 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 403,285 | 4.033 | 20 | 200 | fits | 106,465 | 163 | 0.435 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 298,360 | 2.984 | 20 | 20 | fits | 149,918 | 231 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 403,989 | 4.040 | 20 | 20 | fits | 106,465 | 163 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 152,082 | 1.521 | 20 | 24 | fits | 152,322 | 155 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 301,010 | 3.010 | 20 | 24 | fits | 149,918 | 231 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 300,944 | 3.009 | 20 | 50 | fits | 149,918 | 231 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 407,013 | 4.070 | 20 | 50 | fits | 106,465 | 163 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 493,582 | 4.936 | 20 | 20 | fits | 86,635 | 24 | 0.793 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 996,065 | 9.961 | 20 | 20 | fits | 73,292 | 24 | 0.684 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 357,510 | 3.575 | 20 | 20 | fits | 97,367 | 152 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 311,633 | 3.116 | 20 | 200 | fits | 151,412 | 237 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 408,384 | 4.084 | 20 | 200 | fits | 97,367 | 152 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 312,557 | 3.126 | 20 | 20 | fits | 151,412 | 237 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 409,088 | 4.091 | 20 | 20 | fits | 97,367 | 152 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 164,785 | 1.648 | 20 | 24 | fits | 152,898 | 155 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 315,207 | 3.152 | 20 | 24 | fits | 151,412 | 237 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 315,141 | 3.151 | 20 | 50 | fits | 151,412 | 237 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 412,112 | 4.121 | 20 | 50 | fits | 97,367 | 152 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 510,696 | 5.107 | 20 | 20 | fits | 88,998 | 31 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 1,003,674 | 10.037 | 20 | 20 | fits | 66,643 | 26 | 0.754 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 354,332 | 3.543 | 20 | 20 | fits | 105,005 | 160 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 308,087 | 3.081 | 20 | 200 | fits | 147,124 | 235 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 412,476 | 4.125 | 20 | 200 | fits | 105,005 | 160 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 309,011 | 3.090 | 20 | 20 | fits | 147,124 | 235 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 413,180 | 4.132 | 20 | 20 | fits | 105,005 | 160 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 156,608 | 1.566 | 20 | 24 | fits | 153,086 | 156 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 311,661 | 3.117 | 20 | 24 | fits | 147,124 | 235 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 311,595 | 3.116 | 20 | 50 | fits | 147,124 | 235 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 416,204 | 4.162 | 20 | 50 | fits | 105,005 | 160 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 502,277 | 5.023 | 20 | 20 | fits | 86,139 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 999,208 | 9.992 | 20 | 20 | fits | 76,948 | 31 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 347,900 | 3.479 | 20 | 20 | fits | 97,252 | 151 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 302,023 | 3.020 | 20 | 200 | fits | 151,214 | 237 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 398,659 | 3.987 | 20 | 200 | fits | 97,252 | 151 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 302,947 | 3.029 | 20 | 20 | fits | 151,214 | 237 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 399,363 | 3.994 | 20 | 20 | fits | 97,252 | 151 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 155,373 | 1.554 | 20 | 24 | fits | 152,454 | 155 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 305,597 | 3.056 | 20 | 24 | fits | 151,214 | 237 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 305,531 | 3.055 | 20 | 50 | fits | 151,214 | 237 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 402,387 | 4.024 | 20 | 50 | fits | 97,252 | 151 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 480,619 | 4.806 | 20 | 20 | fits | 78,298 | 26 | 0.824 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 995,769 | 9.958 | 20 | 20 | fits | 85,819 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 362,967 | 3.630 | 20 | 20 | fits | 106,679 | 166 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 306,504 | 3.065 | 20 | 200 | fits | 148,543 | 227 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 412,567 | 4.126 | 20 | 200 | fits | 106,679 | 166 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 307,428 | 3.074 | 20 | 20 | fits | 148,543 | 227 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 413,271 | 4.133 | 20 | 20 | fits | 106,679 | 166 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 162,525 | 1.625 | 20 | 24 | fits | 152,454 | 155 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 310,078 | 3.101 | 20 | 24 | fits | 148,543 | 227 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 310,012 | 3.100 | 20 | 50 | fits | 148,543 | 227 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 416,295 | 4.163 | 20 | 50 | fits | 106,679 | 166 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 502,697 | 5.027 | 20 | 20 | fits | 86,468 | 25 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 1,005,771 | 10.058 | 20 | 20 | fits | 73,340 | 24 | 0.684 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 362,530 | 3.625 | 20 | 20 | fits | 102,959 | 161 | 0.464 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 301,164 | 3.012 | 20 | 200 | fits | 150,273 | 234 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 413,006 | 4.130 | 20 | 200 | fits | 102,959 | 161 | 0.464 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 302,088 | 3.021 | 20 | 20 | fits | 150,273 | 234 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 413,710 | 4.137 | 20 | 20 | fits | 102,959 | 161 | 0.464 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 155,455 | 1.555 | 20 | 24 | fits | 153,491 | 155 | 0.375 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 304,738 | 3.047 | 20 | 24 | fits | 150,273 | 234 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 304,672 | 3.047 | 20 | 50 | fits | 150,273 | 234 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 416,734 | 4.167 | 20 | 50 | fits | 102,959 | 161 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 502,816 | 5.028 | 20 | 20 | fits | 86,148 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 995,746 | 9.957 | 20 | 20 | fits | 66,722 | 26 | 0.755 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 347,791 | 3.478 | 20 | 20 | fits | 98,276 | 154 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 299,808 | 2.998 | 20 | 200 | fits | 149,841 | 233 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 397,468 | 3.975 | 20 | 200 | fits | 98,276 | 154 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 300,732 | 3.007 | 20 | 20 | fits | 149,841 | 233 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 398,172 | 3.982 | 20 | 20 | fits | 98,276 | 154 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 154,531 | 1.545 | 20 | 24 | fits | 152,542 | 155 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 303,382 | 3.034 | 20 | 24 | fits | 149,841 | 233 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 303,316 | 3.033 | 20 | 50 | fits | 149,841 | 233 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 401,196 | 4.012 | 20 | 50 | fits | 98,276 | 154 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 487,521 | 4.875 | 20 | 20 | fits | 86,391 | 24 | 0.793 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 996,440 | 9.964 | 20 | 20 | fits | 85,819 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 348,170 | 3.482 | 20 | 20 | fits | 100,553 | 142 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 305,369 | 3.054 | 20 | 200 | fits | 148,250 | 248 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 405,306 | 4.053 | 20 | 200 | fits | 100,553 | 142 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 306,293 | 3.063 | 20 | 20 | fits | 148,250 | 248 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 406,010 | 4.060 | 20 | 20 | fits | 100,553 | 142 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 161,683 | 1.617 | 20 | 24 | fits | 152,542 | 155 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 308,943 | 3.089 | 20 | 24 | fits | 148,250 | 248 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 308,877 | 3.089 | 20 | 50 | fits | 148,250 | 248 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 409,034 | 4.090 | 20 | 50 | fits | 100,553 | 142 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 487,395 | 4.874 | 20 | 20 | fits | 78,427 | 27 | 0.822 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 1,003,332 | 10.033 | 20 | 20 | fits | 85,836 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 358,880 | 3.589 | 20 | 20 | fits | 110,323 | 169 | 0.454 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 297,629 | 2.976 | 20 | 200 | fits | 149,397 | 232 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 416,898 | 4.169 | 20 | 200 | fits | 110,323 | 169 | 0.454 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 298,553 | 2.986 | 20 | 20 | fits | 149,397 | 232 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 417,602 | 4.176 | 20 | 20 | fits | 110,323 | 169 | 0.454 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 152,796 | 1.528 | 20 | 24 | fits | 152,575 | 155 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 301,203 | 3.012 | 20 | 24 | fits | 149,397 | 232 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 301,137 | 3.011 | 20 | 50 | fits | 149,397 | 232 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 420,626 | 4.206 | 20 | 50 | fits | 110,323 | 169 | 0.454 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 506,613 | 5.066 | 20 | 20 | fits | 86,053 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 992,758 | 9.928 | 20 | 20 | fits | 60,102 | 20 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 386,748 | 3.867 | 20 | 20 | fits | 98,276 | 154 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 338,765 | 3.388 | 20 | 200 | fits | 150,062 | 233 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 436,425 | 4.364 | 20 | 200 | fits | 98,276 | 154 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 339,689 | 3.397 | 20 | 20 | fits | 150,062 | 233 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 437,129 | 4.371 | 20 | 20 | fits | 98,276 | 154 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 193,267 | 1.933 | 20 | 24 | fits | 153,133 | 155 | 0.372 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 342,339 | 3.423 | 20 | 24 | fits | 150,062 | 233 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 342,273 | 3.423 | 20 | 50 | fits | 150,062 | 233 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 440,153 | 4.402 | 20 | 50 | fits | 98,276 | 154 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 526,506 | 5.265 | 20 | 20 | fits | 86,419 | 24 | 0.791 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,035,088 | 10.351 | 20 | 20 | fits | 78,989 | 30 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 351,613 | 3.516 | 20 | 20 | fits | 100,553 | 142 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 308,812 | 3.088 | 20 | 200 | fits | 148,552 | 248 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 408,749 | 4.087 | 20 | 200 | fits | 100,553 | 142 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 309,736 | 3.097 | 20 | 20 | fits | 148,552 | 248 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 409,453 | 4.095 | 20 | 20 | fits | 100,553 | 142 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 164,824 | 1.648 | 20 | 24 | fits | 152,733 | 155 | 0.372 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 312,386 | 3.124 | 20 | 24 | fits | 148,552 | 248 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 312,320 | 3.123 | 20 | 50 | fits | 148,552 | 248 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 412,477 | 4.125 | 20 | 50 | fits | 100,553 | 142 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 498,763 | 4.988 | 20 | 20 | fits | 86,352 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 1,008,763 | 10.088 | 20 | 20 | fits | 85,930 | 28 | 0.644 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 333,529 | 3.335 | 20 | 20 | fits | 98,545 | 152 | 0.459 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 299,327 | 2.993 | 20 | 200 | fits | 151,337 | 237 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 397,256 | 3.973 | 20 | 200 | fits | 98,545 | 152 | 0.459 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 300,251 | 3.003 | 20 | 20 | fits | 151,337 | 237 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 397,960 | 3.980 | 20 | 20 | fits | 98,545 | 152 | 0.459 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 152,554 | 1.526 | 20 | 24 | fits | 152,700 | 155 | 0.372 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 302,901 | 3.029 | 20 | 24 | fits | 151,337 | 237 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 302,835 | 3.028 | 20 | 50 | fits | 151,337 | 237 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 400,984 | 4.010 | 20 | 50 | fits | 98,545 | 152 | 0.459 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 499,707 | 4.997 | 20 | 20 | fits | 89,137 | 31 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 993,025 | 9.930 | 20 | 20 | fits | 73,137 | 24 | 0.673 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 356,948 | 3.569 | 20 | 20 | fits | 105,444 | 149 | 0.467 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 300,577 | 3.006 | 20 | 200 | fits | 148,715 | 249 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 414,865 | 4.149 | 20 | 200 | fits | 105,444 | 149 | 0.467 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 301,501 | 3.015 | 20 | 20 | fits | 148,715 | 249 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 415,569 | 4.156 | 20 | 20 | fits | 105,444 | 149 | 0.467 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 156,426 | 1.564 | 20 | 24 | fits | 152,700 | 155 | 0.372 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 304,151 | 3.042 | 20 | 24 | fits | 148,715 | 249 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 304,085 | 3.041 | 20 | 50 | fits | 148,715 | 249 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 418,593 | 4.186 | 20 | 50 | fits | 105,444 | 149 | 0.467 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 504,667 | 5.047 | 20 | 20 | fits | 86,140 | 24 | 0.788 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 997,917 | 9.979 | 20 | 20 | fits | 73,137 | 24 | 0.673 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 358,200 | 3.582 | 20 | 20 | fits | 105,005 | 160 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 311,955 | 3.120 | 20 | 200 | fits | 147,156 | 235 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 416,344 | 4.163 | 20 | 200 | fits | 105,005 | 160 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 312,879 | 3.129 | 20 | 20 | fits | 147,156 | 235 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 417,048 | 4.170 | 20 | 20 | fits | 105,005 | 160 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 160,444 | 1.604 | 20 | 24 | fits | 152,846 | 156 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 315,529 | 3.155 | 20 | 24 | fits | 147,156 | 235 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 315,463 | 3.155 | 20 | 50 | fits | 147,156 | 235 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 420,072 | 4.201 | 20 | 50 | fits | 105,005 | 160 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 498,312 | 4.983 | 20 | 20 | fits | 78,306 | 26 | 0.822 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 1,001,591 | 10.016 | 20 | 20 | fits | 77,035 | 31 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 354,225 | 3.542 | 20 | 20 | fits | 122,104 | 181 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 290,033 | 2.900 | 20 | 200 | fits | 147,388 | 230 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 411,521 | 4.115 | 20 | 200 | fits | 122,104 | 181 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 290,957 | 2.910 | 20 | 20 | fits | 147,388 | 230 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 412,225 | 4.122 | 20 | 20 | fits | 122,104 | 181 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 138,371 | 1.384 | 20 | 24 | fits | 143,010 | 146 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 293,607 | 2.936 | 20 | 24 | fits | 147,388 | 230 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 293,541 | 2.935 | 20 | 50 | fits | 147,388 | 230 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 415,249 | 4.152 | 20 | 50 | fits | 122,104 | 181 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 501,509 | 5.015 | 20 | 20 | fits | 86,326 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 1,003,170 | 10.032 | 20 | 20 | fits | 65,546 | 27 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 364,219 | 3.642 | 20 | 20 | fits | 105,863 | 163 | 0.427 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 309,611 | 3.096 | 20 | 200 | fits | 149,985 | 231 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 414,858 | 4.149 | 20 | 200 | fits | 105,863 | 163 | 0.427 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 310,535 | 3.105 | 20 | 20 | fits | 149,985 | 231 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 415,562 | 4.156 | 20 | 20 | fits | 105,863 | 163 | 0.427 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 164,190 | 1.642 | 20 | 24 | fits | 152,613 | 155 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 313,185 | 3.132 | 20 | 24 | fits | 149,985 | 231 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 313,119 | 3.131 | 20 | 50 | fits | 149,985 | 231 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 418,586 | 4.186 | 20 | 50 | fits | 105,863 | 163 | 0.427 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 504,752 | 5.048 | 20 | 20 | fits | 86,232 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 1,008,137 | 10.081 | 20 | 20 | fits | 73,293 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 344,553 | 3.446 | 20 | 20 | fits | 105,842 | 163 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 296,463 | 2.965 | 20 | 200 | fits | 149,366 | 231 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 401,689 | 4.017 | 20 | 200 | fits | 105,842 | 163 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 297,387 | 2.974 | 20 | 20 | fits | 149,366 | 231 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 402,393 | 4.024 | 20 | 20 | fits | 105,842 | 163 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 151,661 | 1.517 | 20 | 24 | fits | 152,580 | 155 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 300,037 | 3.000 | 20 | 24 | fits | 149,366 | 231 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 299,971 | 3.000 | 20 | 50 | fits | 149,366 | 231 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 405,417 | 4.054 | 20 | 50 | fits | 105,842 | 163 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 491,672 | 4.917 | 20 | 20 | fits | 86,321 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 994,992 | 9.950 | 20 | 20 | fits | 73,340 | 24 | 0.684 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 360,590 | 3.606 | 20 | 20 | fits | 117,430 | 196 | 0.447 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 285,254 | 2.853 | 20 | 200 | fits | 150,663 | 220 | 0.402 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 412,125 | 4.121 | 20 | 200 | fits | 117,430 | 196 | 0.447 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 286,178 | 2.862 | 20 | 20 | fits | 150,663 | 220 | 0.402 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 412,829 | 4.128 | 20 | 20 | fits | 117,430 | 196 | 0.447 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 139,155 | 1.392 | 20 | 24 | fits | 145,416 | 147 | 0.412 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 288,828 | 2.888 | 20 | 24 | fits | 150,663 | 220 | 0.402 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 288,762 | 2.888 | 20 | 50 | fits | 150,663 | 220 | 0.402 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 415,853 | 4.159 | 20 | 50 | fits | 117,430 | 196 | 0.447 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 501,964 | 5.020 | 20 | 20 | fits | 86,177 | 24 | 0.791 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 994,316 | 9.943 | 20 | 20 | fits | 66,624 | 26 | 0.754 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 349,928 | 3.499 | 20 | 20 | fits | 107,746 | 166 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 301,139 | 3.011 | 20 | 200 | fits | 147,070 | 235 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 408,269 | 4.083 | 20 | 200 | fits | 107,746 | 166 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 302,063 | 3.021 | 20 | 20 | fits | 147,070 | 235 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 408,973 | 4.090 | 20 | 20 | fits | 107,746 | 166 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 148,875 | 1.489 | 20 | 24 | fits | 152,451 | 153 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 304,713 | 3.047 | 20 | 24 | fits | 147,070 | 235 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 304,647 | 3.046 | 20 | 50 | fits | 147,070 | 235 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 411,997 | 4.120 | 20 | 50 | fits | 107,746 | 166 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 497,975 | 4.980 | 20 | 20 | fits | 86,044 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 1,071,082 | 10.711 | 20 | 20 | fits | 77,055 | 32 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 359,530 | 3.595 | 20 | 20 | fits | 101,345 | 142 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 316,256 | 3.163 | 20 | 200 | fits | 148,242 | 248 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 416,985 | 4.170 | 20 | 200 | fits | 101,345 | 142 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 317,180 | 3.172 | 20 | 20 | fits | 148,242 | 248 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 417,689 | 4.177 | 20 | 20 | fits | 101,345 | 142 | 0.449 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 172,578 | 1.726 | 20 | 24 | fits | 151,586 | 153 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 319,830 | 3.198 | 20 | 24 | fits | 148,242 | 248 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 319,764 | 3.198 | 20 | 50 | fits | 148,242 | 248 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 420,713 | 4.207 | 20 | 50 | fits | 101,345 | 142 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 506,623 | 5.066 | 20 | 20 | fits | 85,976 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,090,590 | 10.906 | 20 | 20 | fits | 86,029 | 28 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 335,872 | 3.359 | 20 | 20 | fits | 98,397 | 151 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 301,512 | 3.015 | 20 | 200 | fits | 151,163 | 237 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 399,293 | 3.993 | 20 | 200 | fits | 98,397 | 151 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 302,436 | 3.024 | 20 | 20 | fits | 151,163 | 237 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 399,997 | 4.000 | 20 | 20 | fits | 98,397 | 151 | 0.460 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 154,913 | 1.549 | 20 | 24 | fits | 152,026 | 152 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 305,086 | 3.051 | 20 | 24 | fits | 151,163 | 237 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 305,020 | 3.050 | 20 | 50 | fits | 151,163 | 237 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 403,021 | 4.030 | 20 | 50 | fits | 98,397 | 151 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 488,935 | 4.889 | 20 | 20 | fits | 85,980 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,074,516 | 10.745 | 20 | 20 | fits | 85,529 | 28 | 0.637 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 344,621 | 3.446 | 20 | 20 | fits | 98,118 | 154 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 296,634 | 2.966 | 20 | 200 | fits | 151,258 | 238 | 0.393 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 394,136 | 3.941 | 20 | 200 | fits | 98,118 | 154 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 297,558 | 2.976 | 20 | 20 | fits | 151,258 | 238 | 0.393 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 394,840 | 3.948 | 20 | 20 | fits | 98,118 | 154 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 149,940 | 1.499 | 20 | 24 | fits | 152,073 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 300,208 | 3.002 | 20 | 24 | fits | 151,258 | 238 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 300,142 | 3.001 | 20 | 50 | fits | 151,258 | 238 | 0.393 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 397,864 | 3.979 | 20 | 50 | fits | 98,118 | 154 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 483,861 | 4.839 | 20 | 20 | fits | 86,063 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,067,891 | 10.679 | 20 | 20 | fits | 85,529 | 28 | 0.637 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 350,782 | 3.508 | 20 | 20 | fits | 106,559 | 157 | 0.492 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 308,735 | 3.087 | 20 | 200 | fits | 151,239 | 237 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 414,678 | 4.147 | 20 | 200 | fits | 106,559 | 157 | 0.492 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 309,659 | 3.097 | 20 | 20 | fits | 151,239 | 237 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 415,382 | 4.154 | 20 | 20 | fits | 106,559 | 157 | 0.492 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 162,060 | 1.621 | 20 | 24 | fits | 152,073 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 312,309 | 3.123 | 20 | 24 | fits | 151,239 | 237 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 312,243 | 3.122 | 20 | 50 | fits | 151,239 | 237 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 418,406 | 4.184 | 20 | 50 | fits | 106,559 | 157 | 0.492 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 585,000 | 5.850 | 20 | 20 | fits | 89,549 | 32 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,084,199 | 10.842 | 20 | 20 | fits | 60,264 | 20 | 0.723 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 370,575 | 3.706 | 20 | 20 | fits | 109,787 | 167 | 0.479 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 302,414 | 3.024 | 20 | 200 | fits | 149,985 | 234 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 420,891 | 4.209 | 20 | 200 | fits | 109,787 | 167 | 0.479 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 303,338 | 3.033 | 20 | 20 | fits | 149,985 | 234 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 421,595 | 4.216 | 20 | 20 | fits | 109,787 | 167 | 0.479 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 156,993 | 1.570 | 20 | 24 | fits | 152,026 | 152 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 305,988 | 3.060 | 20 | 24 | fits | 149,985 | 234 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 305,922 | 3.059 | 20 | 50 | fits | 149,985 | 234 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 424,619 | 4.246 | 20 | 50 | fits | 109,787 | 167 | 0.479 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 586,790 | 5.868 | 20 | 20 | fits | 85,126 | 25 | 0.781 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,072,928 | 10.729 | 20 | 20 | fits | 60,109 | 20 | 0.714 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 434,945 | 4.349 | 20 | 20 | fits | 111,361 | 169 | 0.466 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 297,351 | 2.974 | 20 | 200 | fits | 149,895 | 232 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 493,418 | 4.934 | 20 | 200 | fits | 111,361 | 169 | 0.466 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 298,275 | 2.983 | 20 | 20 | fits | 149,895 | 232 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 494,122 | 4.941 | 20 | 20 | fits | 111,361 | 169 | 0.466 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 152,020 | 1.520 | 20 | 24 | fits | 152,073 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 300,925 | 3.009 | 20 | 24 | fits | 149,895 | 232 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 300,859 | 3.009 | 20 | 50 | fits | 149,895 | 232 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 497,146 | 4.971 | 20 | 50 | fits | 111,361 | 169 | 0.466 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 583,116 | 5.831 | 20 | 20 | fits | 86,036 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,068,941 | 10.689 | 20 | 20 | fits | 60,062 | 20 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 344,658 | 3.447 | 20 | 20 | fits | 97,427 | 151 | 0.445 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 298,729 | 2.987 | 20 | 200 | fits | 151,212 | 237 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 395,540 | 3.955 | 20 | 200 | fits | 97,427 | 151 | 0.445 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 299,653 | 2.997 | 20 | 20 | fits | 151,212 | 237 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 396,244 | 3.962 | 20 | 20 | fits | 97,427 | 151 | 0.445 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 152,081 | 1.521 | 20 | 24 | fits | 152,156 | 152 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 302,303 | 3.023 | 20 | 24 | fits | 151,212 | 237 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 302,237 | 3.022 | 20 | 50 | fits | 151,212 | 237 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 399,268 | 3.993 | 20 | 50 | fits | 97,427 | 151 | 0.445 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 485,833 | 4.858 | 20 | 20 | fits | 86,631 | 25 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 988,840 | 9.888 | 20 | 20 | fits | 73,292 | 24 | 0.684 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 355,612 | 3.556 | 20 | 20 | fits | 105,248 | 149 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 308,125 | 3.081 | 20 | 200 | fits | 148,360 | 248 | 0.378 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 412,757 | 4.128 | 20 | 200 | fits | 105,248 | 149 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 309,049 | 3.090 | 20 | 20 | fits | 148,360 | 248 | 0.378 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 413,461 | 4.135 | 20 | 20 | fits | 105,248 | 149 | 0.461 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 164,329 | 1.643 | 20 | 24 | fits | 152,156 | 152 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 311,699 | 3.117 | 20 | 24 | fits | 148,360 | 248 | 0.378 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 311,633 | 3.116 | 20 | 50 | fits | 148,360 | 248 | 0.378 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 416,485 | 4.165 | 20 | 50 | fits | 105,248 | 149 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 512,827 | 5.128 | 20 | 20 | fits | 86,670 | 25 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 1,047,251 | 10.473 | 20 | 20 | fits | 76,305 | 25 | 0.735 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 365,594 | 3.656 | 20 | 20 | fits | 102,201 | 158 | 0.476 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 306,104 | 3.061 | 20 | 200 | fits | 151,294 | 238 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 417,199 | 4.172 | 20 | 200 | fits | 102,201 | 158 | 0.476 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 307,028 | 3.070 | 20 | 20 | fits | 151,294 | 238 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 417,903 | 4.179 | 20 | 20 | fits | 102,201 | 158 | 0.476 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 159,374 | 1.594 | 20 | 24 | fits | 152,109 | 152 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 309,678 | 3.097 | 20 | 24 | fits | 151,294 | 238 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 309,612 | 3.096 | 20 | 50 | fits | 151,294 | 238 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 420,927 | 4.209 | 20 | 50 | fits | 102,201 | 158 | 0.476 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 507,269 | 5.073 | 20 | 20 | fits | 86,408 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 1,072,853 | 10.729 | 20 | 20 | fits | 74,726 | 25 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 351,815 | 3.518 | 20 | 20 | fits | 100,253 | 142 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 309,005 | 3.090 | 20 | 200 | fits | 150,085 | 253 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 408,642 | 4.086 | 20 | 200 | fits | 100,253 | 142 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 309,929 | 3.099 | 20 | 20 | fits | 150,085 | 253 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 409,346 | 4.093 | 20 | 20 | fits | 100,253 | 142 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 154,580 | 1.546 | 20 | 24 | fits | 152,223 | 153 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 312,579 | 3.126 | 20 | 24 | fits | 150,085 | 253 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 312,513 | 3.125 | 20 | 50 | fits | 150,085 | 253 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 412,370 | 4.124 | 20 | 50 | fits | 100,253 | 142 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 498,922 | 4.989 | 20 | 20 | fits | 86,618 | 24 | 0.793 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 1,082,043 | 10.820 | 20 | 20 | fits | 86,686 | 28 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 343,665 | 3.437 | 20 | 20 | fits | 98,392 | 151 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 309,305 | 3.093 | 20 | 200 | fits | 151,036 | 237 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 407,081 | 4.071 | 20 | 200 | fits | 98,392 | 151 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 310,229 | 3.102 | 20 | 20 | fits | 151,036 | 237 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 407,785 | 4.078 | 20 | 20 | fits | 98,392 | 151 | 0.460 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 162,833 | 1.628 | 20 | 24 | fits | 152,005 | 152 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 312,879 | 3.129 | 20 | 24 | fits | 151,036 | 237 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 312,813 | 3.128 | 20 | 50 | fits | 151,036 | 237 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 410,809 | 4.108 | 20 | 50 | fits | 98,392 | 151 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 497,305 | 4.973 | 20 | 20 | fits | 86,562 | 24 | 0.793 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 1,080,872 | 10.809 | 20 | 20 | fits | 86,087 | 28 | 0.656 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 351,054 | 3.511 | 20 | 20 | fits | 98,118 | 154 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 303,067 | 3.031 | 20 | 200 | fits | 149,771 | 233 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 400,569 | 4.006 | 20 | 200 | fits | 98,118 | 154 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 303,991 | 3.040 | 20 | 20 | fits | 149,771 | 233 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 401,273 | 4.013 | 20 | 20 | fits | 98,118 | 154 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 157,860 | 1.579 | 20 | 24 | fits | 152,052 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 306,641 | 3.066 | 20 | 24 | fits | 149,771 | 233 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 306,575 | 3.066 | 20 | 50 | fits | 149,771 | 233 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 404,297 | 4.043 | 20 | 50 | fits | 98,118 | 154 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 488,848 | 4.888 | 20 | 20 | fits | 84,617 | 26 | 0.838 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 1,074,586 | 10.746 | 20 | 20 | fits | 86,065 | 28 | 0.655 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 354,327 | 3.543 | 20 | 20 | fits | 117,938 | 148 | 0.513 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 296,466 | 2.965 | 20 | 200 | fits | 148,237 | 248 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 413,788 | 4.138 | 20 | 200 | fits | 117,938 | 148 | 0.513 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 297,390 | 2.974 | 20 | 20 | fits | 148,237 | 248 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 414,492 | 4.145 | 20 | 20 | fits | 117,938 | 148 | 0.513 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 152,793 | 1.528 | 20 | 24 | fits | 152,005 | 152 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 300,040 | 3.000 | 20 | 24 | fits | 148,237 | 248 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 299,974 | 3.000 | 20 | 50 | fits | 148,237 | 248 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 417,516 | 4.175 | 20 | 50 | fits | 117,938 | 148 | 0.513 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 532,949 | 5.329 | 20 | 20 | fits | 86,301 | 26 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 1,068,865 | 10.689 | 20 | 20 | fits | 73,530 | 24 | 0.686 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 357,040 | 3.570 | 20 | 20 | fits | 119,796 | 178 | 0.511 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 290,528 | 2.905 | 20 | 200 | fits | 146,830 | 255 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 409,708 | 4.097 | 20 | 200 | fits | 119,796 | 178 | 0.511 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 291,452 | 2.915 | 20 | 20 | fits | 146,830 | 255 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 410,412 | 4.104 | 20 | 20 | fits | 119,796 | 178 | 0.511 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 148,262 | 1.483 | 20 | 24 | fits | 152,494 | 120 | 0.375 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 294,102 | 2.941 | 20 | 24 | fits | 146,830 | 255 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 294,036 | 2.940 | 20 | 50 | fits | 146,830 | 255 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 413,436 | 4.134 | 20 | 50 | fits | 119,796 | 178 | 0.511 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 540,999 | 5.410 | 20 | 20 | fits | 89,456 | 30 | 0.793 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 1,059,652 | 10.597 | 20 | 20 | fits | 60,071 | 20 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 349,711 | 3.497 | 20 | 20 | fits | 100,385 | 142 | 0.436 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 306,905 | 3.069 | 20 | 200 | fits | 150,258 | 253 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 406,674 | 4.067 | 20 | 200 | fits | 100,385 | 142 | 0.436 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 307,829 | 3.078 | 20 | 20 | fits | 150,258 | 253 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 407,378 | 4.074 | 20 | 20 | fits | 100,385 | 142 | 0.436 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 152,291 | 1.523 | 20 | 24 | fits | 152,427 | 153 | 0.371 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 310,479 | 3.105 | 20 | 24 | fits | 150,258 | 253 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 310,413 | 3.104 | 20 | 50 | fits | 150,258 | 253 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 410,402 | 4.104 | 20 | 50 | fits | 100,385 | 142 | 0.436 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 496,551 | 4.966 | 20 | 20 | fits | 86,215 | 24 | 0.791 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 982,788 | 9.828 | 20 | 20 | fits | 60,194 | 21 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 342,923 | 3.429 | 20 | 20 | fits | 98,340 | 151 | 0.458 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 308,721 | 3.087 | 20 | 200 | fits | 151,176 | 237 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 406,445 | 4.064 | 20 | 200 | fits | 98,340 | 151 | 0.458 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 309,645 | 3.096 | 20 | 20 | fits | 151,176 | 237 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 407,149 | 4.071 | 20 | 20 | fits | 98,340 | 151 | 0.458 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 162,109 | 1.621 | 20 | 24 | fits | 152,255 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 312,295 | 3.123 | 20 | 24 | fits | 151,176 | 237 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 312,229 | 3.122 | 20 | 50 | fits | 151,176 | 237 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 410,173 | 4.102 | 20 | 50 | fits | 98,340 | 151 | 0.458 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 496,266 | 4.963 | 20 | 20 | fits | 86,159 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 1,085,639 | 10.856 | 20 | 20 | fits | 85,953 | 29 | 0.660 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 350,578 | 3.506 | 20 | 20 | fits | 98,226 | 154 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 302,595 | 3.026 | 20 | 200 | fits | 149,911 | 233 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 400,205 | 4.002 | 20 | 200 | fits | 98,226 | 154 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 303,519 | 3.035 | 20 | 20 | fits | 149,911 | 233 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 400,909 | 4.009 | 20 | 20 | fits | 98,226 | 154 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 157,248 | 1.572 | 20 | 24 | fits | 152,302 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 306,169 | 3.062 | 20 | 24 | fits | 149,911 | 233 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 306,103 | 3.061 | 20 | 50 | fits | 149,911 | 233 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 403,933 | 4.039 | 20 | 50 | fits | 98,226 | 154 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 490,109 | 4.901 | 20 | 20 | fits | 86,242 | 24 | 0.791 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,080,127 | 10.801 | 20 | 20 | fits | 86,091 | 28 | 0.656 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 339,268 | 3.393 | 20 | 20 | fits | 101,308 | 142 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 296,125 | 2.961 | 20 | 200 | fits | 148,396 | 248 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 396,817 | 3.968 | 20 | 200 | fits | 101,308 | 142 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 297,049 | 2.970 | 20 | 20 | fits | 148,396 | 248 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 397,521 | 3.975 | 20 | 20 | fits | 101,308 | 142 | 0.446 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 152,293 | 1.523 | 20 | 24 | fits | 152,255 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 299,699 | 2.997 | 20 | 24 | fits | 148,396 | 248 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 299,633 | 2.996 | 20 | 50 | fits | 148,396 | 248 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 400,545 | 4.005 | 20 | 50 | fits | 101,308 | 142 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 486,782 | 4.868 | 20 | 20 | fits | 86,303 | 25 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,077,272 | 10.773 | 20 | 20 | fits | 85,845 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 357,795 | 3.578 | 20 | 20 | fits | 98,341 | 155 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 309,812 | 3.098 | 20 | 200 | fits | 149,835 | 233 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 407,537 | 4.075 | 20 | 200 | fits | 98,341 | 155 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 310,736 | 3.107 | 20 | 20 | fits | 149,835 | 233 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 408,241 | 4.082 | 20 | 20 | fits | 98,341 | 155 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 164,541 | 1.645 | 20 | 24 | fits | 152,255 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 313,386 | 3.134 | 20 | 24 | fits | 149,835 | 233 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 313,320 | 3.133 | 20 | 50 | fits | 149,835 | 233 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 411,265 | 4.113 | 20 | 50 | fits | 98,341 | 155 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 509,907 | 5.099 | 20 | 20 | fits | 89,085 | 31 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,085,109 | 10.851 | 20 | 20 | fits | 73,349 | 24 | 0.684 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 366,824 | 3.668 | 20 | 20 | fits | 112,803 | 155 | 0.487 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 303,753 | 3.038 | 20 | 200 | fits | 148,637 | 249 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 425,251 | 4.253 | 20 | 200 | fits | 112,803 | 155 | 0.487 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 304,677 | 3.047 | 20 | 20 | fits | 148,637 | 249 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 425,955 | 4.260 | 20 | 20 | fits | 112,803 | 155 | 0.487 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 159,680 | 1.597 | 20 | 24 | fits | 152,302 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 307,327 | 3.073 | 20 | 24 | fits | 148,637 | 249 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 307,261 | 3.073 | 20 | 50 | fits | 148,637 | 249 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 428,979 | 4.290 | 20 | 50 | fits | 112,803 | 155 | 0.487 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 594,768 | 5.948 | 20 | 20 | fits | 85,215 | 25 | 0.781 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,096,895 | 10.969 | 20 | 20 | fits | 65,598 | 27 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 360,110 | 3.601 | 20 | 20 | fits | 113,016 | 166 | 0.467 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 306,117 | 3.061 | 20 | 200 | fits | 147,052 | 235 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 418,517 | 4.185 | 20 | 200 | fits | 113,016 | 166 | 0.467 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 307,041 | 3.070 | 20 | 20 | fits | 147,052 | 235 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 419,221 | 4.192 | 20 | 20 | fits | 113,016 | 166 | 0.467 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 154,902 | 1.549 | 20 | 24 | fits | 152,432 | 153 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 309,691 | 3.097 | 20 | 24 | fits | 147,052 | 235 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 309,625 | 3.096 | 20 | 50 | fits | 147,052 | 235 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 422,245 | 4.222 | 20 | 50 | fits | 113,016 | 166 | 0.467 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 588,209 | 5.882 | 20 | 20 | fits | 85,472 | 25 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,090,632 | 10.906 | 20 | 20 | fits | 73,543 | 24 | 0.692 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 437,117 | 4.371 | 20 | 20 | fits | 105,241 | 163 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 309,464 | 3.095 | 20 | 200 | fits | 149,462 | 231 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 494,375 | 4.944 | 20 | 200 | fits | 105,241 | 163 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 310,388 | 3.104 | 20 | 20 | fits | 149,462 | 231 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 495,079 | 4.951 | 20 | 20 | fits | 105,241 | 163 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 164,566 | 1.646 | 20 | 24 | fits | 152,160 | 152 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 313,038 | 3.130 | 20 | 24 | fits | 149,462 | 231 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 312,972 | 3.130 | 20 | 50 | fits | 149,462 | 231 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 498,103 | 4.981 | 20 | 50 | fits | 105,241 | 163 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 584,391 | 5.844 | 20 | 20 | fits | 86,354 | 24 | 0.791 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,086,867 | 10.869 | 20 | 20 | fits | 73,323 | 24 | 0.684 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 362,062 | 3.621 | 20 | 20 | fits | 102,301 | 158 | 0.475 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 302,470 | 3.025 | 20 | 200 | fits | 151,393 | 238 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 413,719 | 4.137 | 20 | 200 | fits | 102,301 | 158 | 0.475 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 303,394 | 3.034 | 20 | 20 | fits | 151,393 | 238 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 414,423 | 4.144 | 20 | 20 | fits | 102,301 | 158 | 0.475 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 155,641 | 1.556 | 20 | 24 | fits | 152,255 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 306,044 | 3.060 | 20 | 24 | fits | 151,393 | 238 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 305,978 | 3.060 | 20 | 50 | fits | 151,393 | 238 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 417,447 | 4.174 | 20 | 50 | fits | 102,301 | 158 | 0.475 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 503,386 | 5.034 | 20 | 20 | fits | 86,005 | 24 | 0.788 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 989,708 | 9.897 | 20 | 20 | fits | 60,149 | 20 | 0.714 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 350,200 | 3.502 | 20 | 20 | fits | 103,395 | 148 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 304,717 | 3.047 | 20 | 200 | fits | 149,994 | 253 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 407,496 | 4.075 | 20 | 200 | fits | 103,395 | 148 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 305,641 | 3.056 | 20 | 20 | fits | 149,994 | 253 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 408,200 | 4.082 | 20 | 20 | fits | 103,395 | 148 | 0.451 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 150,367 | 1.504 | 20 | 24 | fits | 152,506 | 153 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 308,291 | 3.083 | 20 | 24 | fits | 149,994 | 253 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 308,225 | 3.082 | 20 | 50 | fits | 149,994 | 253 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 411,224 | 4.112 | 20 | 50 | fits | 103,395 | 148 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 497,409 | 4.974 | 20 | 20 | fits | 86,251 | 24 | 0.791 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 994,243 | 9.942 | 20 | 20 | fits | 77,317 | 31 | 0.696 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 334,338 | 3.343 | 20 | 20 | fits | 108,339 | 166 | 0.457 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 297,875 | 2.979 | 20 | 200 | fits | 146,653 | 235 | 0.393 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 405,598 | 4.056 | 20 | 200 | fits | 108,339 | 166 | 0.457 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 298,799 | 2.988 | 20 | 20 | fits | 146,653 | 235 | 0.393 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 406,302 | 4.063 | 20 | 20 | fits | 108,339 | 166 | 0.457 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 146,890 | 1.469 | 20 | 24 | fits | 153,320 | 153 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 301,449 | 3.014 | 20 | 24 | fits | 146,653 | 235 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 301,383 | 3.014 | 20 | 50 | fits | 146,653 | 235 | 0.393 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 409,326 | 4.093 | 20 | 50 | fits | 108,339 | 166 | 0.457 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 495,471 | 4.955 | 20 | 20 | fits | 86,211 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 1,003,285 | 10.033 | 20 | 20 | fits | 77,839 | 31 | 0.726 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 349,153 | 3.492 | 20 | 20 | fits | 98,226 | 154 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 301,170 | 3.012 | 20 | 200 | fits | 149,849 | 233 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 398,780 | 3.988 | 20 | 200 | fits | 98,226 | 154 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 302,094 | 3.021 | 20 | 20 | fits | 149,849 | 233 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 399,484 | 3.995 | 20 | 20 | fits | 98,226 | 154 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 155,885 | 1.559 | 20 | 24 | fits | 152,286 | 152 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 304,744 | 3.047 | 20 | 24 | fits | 149,849 | 233 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 304,678 | 3.047 | 20 | 50 | fits | 149,849 | 233 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 402,508 | 4.025 | 20 | 50 | fits | 98,226 | 154 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 488,684 | 4.887 | 20 | 20 | fits | 86,242 | 24 | 0.791 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 997,558 | 9.976 | 20 | 20 | fits | 85,819 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 338,525 | 3.385 | 20 | 20 | fits | 101,308 | 142 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 295,382 | 2.954 | 20 | 200 | fits | 149,846 | 253 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 396,074 | 3.961 | 20 | 200 | fits | 101,308 | 142 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 296,306 | 2.963 | 20 | 20 | fits | 149,846 | 253 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 396,778 | 3.968 | 20 | 20 | fits | 101,308 | 142 | 0.446 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 150,100 | 1.501 | 20 | 24 | fits | 152,239 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 298,956 | 2.990 | 20 | 24 | fits | 149,846 | 253 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 298,890 | 2.989 | 20 | 50 | fits | 149,846 | 253 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 399,802 | 3.998 | 20 | 50 | fits | 101,308 | 142 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 485,911 | 4.859 | 20 | 20 | fits | 86,175 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 995,441 | 9.954 | 20 | 20 | fits | 85,836 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 364,165 | 3.642 | 20 | 20 | fits | 106,125 | 160 | 0.467 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 308,539 | 3.085 | 20 | 200 | fits | 149,925 | 233 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 414,048 | 4.140 | 20 | 200 | fits | 106,125 | 160 | 0.467 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 309,463 | 3.095 | 20 | 20 | fits | 149,925 | 233 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 414,752 | 4.148 | 20 | 20 | fits | 106,125 | 160 | 0.467 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 163,178 | 1.632 | 20 | 24 | fits | 152,239 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 312,113 | 3.121 | 20 | 24 | fits | 149,925 | 233 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 312,047 | 3.120 | 20 | 50 | fits | 149,925 | 233 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 417,776 | 4.178 | 20 | 50 | fits | 106,125 | 160 | 0.467 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 508,014 | 5.080 | 20 | 20 | fits | 90,304 | 31 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 1,007,330 | 10.073 | 20 | 20 | fits | 60,257 | 20 | 0.721 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 365,403 | 3.654 | 20 | 20 | fits | 112,809 | 155 | 0.485 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 302,326 | 3.023 | 20 | 200 | fits | 148,573 | 249 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 423,830 | 4.238 | 20 | 200 | fits | 112,809 | 155 | 0.485 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 303,250 | 3.033 | 20 | 20 | fits | 148,573 | 249 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 424,534 | 4.245 | 20 | 20 | fits | 112,809 | 155 | 0.485 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 158,317 | 1.583 | 20 | 24 | fits | 152,286 | 152 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 305,900 | 3.059 | 20 | 24 | fits | 148,573 | 249 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 305,834 | 3.058 | 20 | 50 | fits | 148,573 | 249 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 427,558 | 4.276 | 20 | 50 | fits | 112,809 | 155 | 0.485 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 513,660 | 5.137 | 20 | 20 | fits | 86,168 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 999,982 | 10.000 | 20 | 20 | fits | 60,149 | 20 | 0.714 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 367,030 | 3.670 | 20 | 20 | fits | 110,603 | 169 | 0.456 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 298,968 | 2.990 | 20 | 200 | fits | 150,170 | 232 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 418,497 | 4.185 | 20 | 200 | fits | 110,603 | 169 | 0.456 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 299,892 | 2.999 | 20 | 20 | fits | 150,170 | 232 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 419,201 | 4.192 | 20 | 20 | fits | 110,603 | 169 | 0.456 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 153,362 | 1.534 | 20 | 24 | fits | 152,239 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 302,542 | 3.025 | 20 | 24 | fits | 150,170 | 232 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 302,476 | 3.025 | 20 | 50 | fits | 150,170 | 232 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 422,225 | 4.222 | 20 | 50 | fits | 110,603 | 169 | 0.456 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 508,212 | 5.082 | 20 | 20 | fits | 86,053 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 994,357 | 9.944 | 20 | 20 | fits | 60,102 | 20 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 341,031 | 3.410 | 20 | 20 | fits | 100,573 | 142 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 298,160 | 2.982 | 20 | 200 | fits | 148,545 | 248 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 398,117 | 3.981 | 20 | 200 | fits | 100,573 | 142 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 299,084 | 2.991 | 20 | 20 | fits | 148,545 | 248 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 398,821 | 3.988 | 20 | 20 | fits | 100,573 | 142 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 154,179 | 1.542 | 20 | 24 | fits | 152,135 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 301,734 | 3.017 | 20 | 24 | fits | 148,545 | 248 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 301,668 | 3.017 | 20 | 50 | fits | 148,545 | 248 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 401,845 | 4.018 | 20 | 50 | fits | 100,573 | 142 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 487,971 | 4.880 | 20 | 20 | fits | 86,192 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 990,980 | 9.910 | 20 | 20 | fits | 73,340 | 24 | 0.684 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 325,339 | 3.253 | 20 | 20 | fits | 105,699 | 160 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 291,336 | 2.913 | 20 | 200 | fits | 146,582 | 235 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 396,419 | 3.964 | 20 | 200 | fits | 105,699 | 160 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 292,260 | 2.923 | 20 | 20 | fits | 146,582 | 235 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 397,123 | 3.971 | 20 | 20 | fits | 105,699 | 160 | 0.446 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 149,318 | 1.493 | 20 | 24 | fits | 152,182 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 294,910 | 2.949 | 20 | 24 | fits | 146,582 | 235 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 294,844 | 2.948 | 20 | 50 | fits | 146,582 | 235 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 400,147 | 4.001 | 20 | 50 | fits | 105,699 | 160 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 486,313 | 4.863 | 20 | 20 | fits | 86,232 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 1,072,707 | 10.727 | 20 | 20 | fits | 85,748 | 29 | 0.653 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 348,342 | 3.483 | 20 | 20 | fits | 100,688 | 143 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 305,471 | 3.055 | 20 | 200 | fits | 148,469 | 248 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 405,543 | 4.055 | 20 | 200 | fits | 100,688 | 143 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 306,395 | 3.064 | 20 | 20 | fits | 148,469 | 248 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 406,247 | 4.062 | 20 | 20 | fits | 100,688 | 143 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 161,566 | 1.616 | 20 | 24 | fits | 152,182 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 309,045 | 3.090 | 20 | 24 | fits | 148,469 | 248 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 308,979 | 3.090 | 20 | 50 | fits | 148,469 | 248 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 409,271 | 4.093 | 20 | 50 | fits | 100,688 | 143 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 508,197 | 5.082 | 20 | 20 | fits | 89,200 | 31 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,079,127 | 10.791 | 20 | 20 | fits | 73,476 | 24 | 0.686 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 351,378 | 3.514 | 20 | 20 | fits | 103,474 | 158 | 0.489 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 303,543 | 3.035 | 20 | 200 | fits | 151,496 | 238 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 415,965 | 4.160 | 20 | 200 | fits | 103,474 | 158 | 0.489 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 304,467 | 3.045 | 20 | 20 | fits | 151,496 | 238 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 416,669 | 4.167 | 20 | 20 | fits | 103,474 | 158 | 0.489 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 156,611 | 1.566 | 20 | 24 | fits | 152,135 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 307,117 | 3.071 | 20 | 24 | fits | 151,496 | 238 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 307,051 | 3.071 | 20 | 50 | fits | 151,496 | 238 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 419,693 | 4.197 | 20 | 50 | fits | 103,474 | 158 | 0.489 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 505,720 | 5.057 | 20 | 20 | fits | 86,093 | 24 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,077,135 | 10.771 | 20 | 20 | fits | 73,432 | 25 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 356,850 | 3.568 | 20 | 20 | fits | 101,245 | 160 | 0.452 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 306,058 | 3.061 | 20 | 200 | fits | 151,495 | 238 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 406,687 | 4.067 | 20 | 200 | fits | 101,245 | 160 | 0.452 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 306,982 | 3.070 | 20 | 20 | fits | 151,495 | 238 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 407,391 | 4.074 | 20 | 20 | fits | 101,245 | 160 | 0.452 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 150,207 | 1.502 | 20 | 24 | fits | 152,346 | 153 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 309,632 | 3.096 | 20 | 24 | fits | 151,495 | 238 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 309,566 | 3.096 | 20 | 50 | fits | 151,495 | 238 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 410,415 | 4.104 | 20 | 50 | fits | 101,245 | 160 | 0.452 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 496,715 | 4.967 | 20 | 20 | fits | 86,366 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,082,836 | 10.828 | 20 | 20 | fits | 77,894 | 31 | 0.724 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 357,179 | 3.572 | 20 | 20 | fits | 113,527 | 166 | 0.474 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 315,535 | 3.155 | 20 | 200 | fits | 147,065 | 235 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 428,446 | 4.284 | 20 | 200 | fits | 113,527 | 166 | 0.474 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 316,459 | 3.165 | 20 | 20 | fits | 147,065 | 235 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 429,150 | 4.292 | 20 | 20 | fits | 113,527 | 166 | 0.474 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 164,114 | 1.641 | 20 | 24 | fits | 152,298 | 153 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 319,109 | 3.191 | 20 | 24 | fits | 147,065 | 235 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 319,043 | 3.190 | 20 | 50 | fits | 147,065 | 235 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 432,174 | 4.322 | 20 | 50 | fits | 113,527 | 166 | 0.474 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 595,325 | 5.953 | 20 | 20 | fits | 85,468 | 25 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,097,555 | 10.976 | 20 | 20 | fits | 73,608 | 24 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 357,425 | 3.574 | 20 | 20 | fits | 105,453 | 157 | 0.477 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 303,797 | 3.038 | 20 | 200 | fits | 151,347 | 237 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 408,634 | 4.086 | 20 | 200 | fits | 105,453 | 157 | 0.477 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 304,721 | 3.047 | 20 | 20 | fits | 151,347 | 237 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 409,338 | 4.093 | 20 | 20 | fits | 105,453 | 157 | 0.477 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 157,014 | 1.570 | 20 | 24 | fits | 152,364 | 152 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 307,371 | 3.074 | 20 | 24 | fits | 151,347 | 237 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 307,305 | 3.073 | 20 | 50 | fits | 151,347 | 237 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 412,362 | 4.124 | 20 | 50 | fits | 105,453 | 157 | 0.477 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 575,553 | 5.756 | 20 | 20 | fits | 85,508 | 25 | 0.783 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,078,567 | 10.786 | 20 | 20 | fits | 73,340 | 24 | 0.684 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 346,061 | 3.461 | 20 | 20 | fits | 108,680 | 148 | 0.471 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 295,416 | 2.954 | 20 | 200 | fits | 149,802 | 253 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 403,480 | 4.035 | 20 | 200 | fits | 108,680 | 148 | 0.471 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 296,340 | 2.963 | 20 | 20 | fits | 149,802 | 253 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 404,184 | 4.042 | 20 | 20 | fits | 108,680 | 148 | 0.471 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 150,178 | 1.502 | 20 | 24 | fits | 152,317 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 298,990 | 2.990 | 20 | 24 | fits | 149,802 | 253 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 298,924 | 2.989 | 20 | 50 | fits | 149,802 | 253 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 407,208 | 4.072 | 20 | 50 | fits | 108,680 | 148 | 0.471 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 570,527 | 5.705 | 20 | 20 | fits | 85,636 | 26 | 0.781 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,073,851 | 10.739 | 20 | 20 | fits | 73,340 | 24 | 0.684 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 367,445 | 3.674 | 20 | 20 | fits | 98,235 | 154 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 319,330 | 3.193 | 20 | 200 | fits | 151,759 | 238 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 416,949 | 4.169 | 20 | 200 | fits | 98,235 | 154 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 320,254 | 3.203 | 20 | 20 | fits | 151,759 | 238 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 417,653 | 4.177 | 20 | 20 | fits | 98,235 | 154 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 163,215 | 1.632 | 20 | 24 | fits | 152,267 | 153 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 322,904 | 3.229 | 20 | 24 | fits | 151,759 | 238 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 322,838 | 3.228 | 20 | 50 | fits | 151,759 | 238 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 420,677 | 4.207 | 20 | 50 | fits | 98,235 | 154 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 506,941 | 5.069 | 20 | 20 | fits | 86,330 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 1,003,067 | 10.031 | 20 | 20 | fits | 70,124 | 33 | 0.745 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 341,407 | 3.414 | 20 | 20 | fits | 100,573 | 142 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 298,536 | 2.985 | 20 | 200 | fits | 148,518 | 248 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 398,493 | 3.985 | 20 | 200 | fits | 100,573 | 142 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 299,460 | 2.995 | 20 | 20 | fits | 148,518 | 248 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 399,197 | 3.992 | 20 | 20 | fits | 100,573 | 142 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 154,582 | 1.546 | 20 | 24 | fits | 152,317 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 302,110 | 3.021 | 20 | 24 | fits | 148,518 | 248 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 302,044 | 3.020 | 20 | 50 | fits | 148,518 | 248 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 402,221 | 4.022 | 20 | 50 | fits | 100,573 | 142 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 488,378 | 4.884 | 20 | 20 | fits | 86,223 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 997,073 | 9.971 | 20 | 20 | fits | 86,040 | 28 | 0.647 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 325,715 | 3.257 | 20 | 20 | fits | 105,699 | 160 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 291,712 | 2.917 | 20 | 200 | fits | 146,555 | 235 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 396,795 | 3.968 | 20 | 200 | fits | 105,699 | 160 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 292,636 | 2.926 | 20 | 20 | fits | 146,555 | 235 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 397,499 | 3.975 | 20 | 20 | fits | 105,699 | 160 | 0.446 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 149,721 | 1.497 | 20 | 24 | fits | 152,364 | 152 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 295,286 | 2.953 | 20 | 24 | fits | 146,555 | 235 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 295,220 | 2.952 | 20 | 50 | fits | 146,555 | 235 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 400,523 | 4.005 | 20 | 50 | fits | 105,699 | 160 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 486,720 | 4.867 | 20 | 20 | fits | 86,263 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 995,391 | 9.954 | 20 | 20 | fits | 85,585 | 28 | 0.637 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 348,718 | 3.487 | 20 | 20 | fits | 100,573 | 142 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 305,847 | 3.058 | 20 | 200 | fits | 148,442 | 248 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 405,804 | 4.058 | 20 | 200 | fits | 100,573 | 142 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 306,771 | 3.068 | 20 | 20 | fits | 148,442 | 248 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 406,508 | 4.065 | 20 | 20 | fits | 100,573 | 142 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 161,969 | 1.620 | 20 | 24 | fits | 152,364 | 152 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 309,421 | 3.094 | 20 | 24 | fits | 148,442 | 248 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 309,355 | 3.094 | 20 | 50 | fits | 148,442 | 248 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 409,532 | 4.095 | 20 | 50 | fits | 100,573 | 142 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 495,817 | 4.958 | 20 | 20 | fits | 86,351 | 25 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 1,004,462 | 10.045 | 20 | 20 | fits | 85,585 | 28 | 0.637 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 338,080 | 3.381 | 20 | 20 | fits | 98,582 | 152 | 0.459 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 303,756 | 3.038 | 20 | 200 | fits | 151,306 | 237 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 401,722 | 4.017 | 20 | 200 | fits | 98,582 | 152 | 0.459 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 304,680 | 3.047 | 20 | 20 | fits | 151,306 | 237 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 402,426 | 4.024 | 20 | 20 | fits | 98,582 | 152 | 0.459 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 157,014 | 1.570 | 20 | 24 | fits | 152,317 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 307,330 | 3.073 | 20 | 24 | fits | 151,306 | 237 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 307,264 | 3.073 | 20 | 50 | fits | 151,306 | 237 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 405,450 | 4.054 | 20 | 50 | fits | 98,582 | 152 | 0.459 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 504,092 | 5.041 | 20 | 20 | fits | 89,205 | 31 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 997,410 | 9.974 | 20 | 20 | fits | 73,137 | 24 | 0.673 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 365,154 | 3.652 | 20 | 20 | fits | 109,728 | 166 | 0.479 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 297,075 | 2.971 | 20 | 200 | fits | 151,414 | 239 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 415,582 | 4.156 | 20 | 200 | fits | 109,728 | 166 | 0.479 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 297,999 | 2.980 | 20 | 20 | fits | 151,414 | 239 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 416,286 | 4.163 | 20 | 20 | fits | 109,728 | 166 | 0.479 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 150,225 | 1.502 | 20 | 24 | fits | 152,364 | 152 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 300,649 | 3.006 | 20 | 24 | fits | 151,414 | 239 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 300,583 | 3.006 | 20 | 50 | fits | 151,414 | 239 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 419,310 | 4.193 | 20 | 50 | fits | 109,728 | 166 | 0.479 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 505,412 | 5.054 | 20 | 20 | fits | 86,168 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 991,557 | 9.916 | 20 | 20 | fits | 60,102 | 20 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 357,441 | 3.574 | 20 | 20 | fits | 113,527 | 166 | 0.474 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 315,797 | 3.158 | 20 | 200 | fits | 147,065 | 235 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 428,708 | 4.287 | 20 | 200 | fits | 113,527 | 166 | 0.474 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 316,721 | 3.167 | 20 | 20 | fits | 147,065 | 235 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 429,412 | 4.294 | 20 | 20 | fits | 113,527 | 166 | 0.474 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 164,569 | 1.646 | 20 | 24 | fits | 152,532 | 153 | 0.371 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 319,371 | 3.194 | 20 | 24 | fits | 147,065 | 235 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 319,305 | 3.193 | 20 | 50 | fits | 147,065 | 235 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 432,436 | 4.324 | 20 | 50 | fits | 113,527 | 166 | 0.474 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 518,696 | 5.187 | 20 | 20 | fits | 86,326 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 1,020,294 | 10.203 | 20 | 20 | fits | 65,483 | 27 | 0.762 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 355,545 | 3.555 | 20 | 20 | fits | 105,910 | 163 | 0.428 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 300,937 | 3.009 | 20 | 200 | fits | 150,072 | 231 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 406,231 | 4.062 | 20 | 200 | fits | 105,910 | 163 | 0.428 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 301,861 | 3.019 | 20 | 20 | fits | 150,072 | 231 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 406,935 | 4.069 | 20 | 20 | fits | 105,910 | 163 | 0.428 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 155,429 | 1.554 | 20 | 24 | fits | 152,056 | 152 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 304,511 | 3.045 | 20 | 24 | fits | 150,072 | 231 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 304,445 | 3.044 | 20 | 50 | fits | 150,072 | 231 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 409,959 | 4.100 | 20 | 50 | fits | 105,910 | 163 | 0.428 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 496,174 | 4.962 | 20 | 20 | fits | 86,281 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 998,343 | 9.983 | 20 | 20 | fits | 73,608 | 24 | 0.693 |
| LINK_UP | `adp.link_up.if0` | 2,571 | 0.026 | 20 | 200 | fits | 27,119 | 43 (11) | 0.739 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 9,524 | 0.095 | 20 | 200 | fits | 23,107 | 23 (39) | 0.753 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 9,457 | 0.095 | 20 | 200 | fits | 2,669 | 10 (11) | 0.571 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 157,675 | 1.577 | 20 | 200 | fits | 158,615 | 273 | 0.454 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 230,978 | 2.310 | 20 | 20 | fits | 93,440 | 65 | 0.693 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 299,827 | 2.998 | 20 | 24 | fits | 81,359 | 48 | 0.567 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 191,503 | 1.915 | 20 | 50 | fits | 93,440 | 65 | 0.693 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 911,858 | 9.119 | 20 | 20 | fits | 86,315 | 28 | 0.651 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 229,289 | 2.293 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 157,675 | 1.577 | 20 | 200 | fits | 158,615 | 273 | 0.454 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 201,220 | 2.012 | 20 | 20 | fits | 145,683 | 267 | 0.365 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 286,904 | 2.869 | 20 | 24 | fits | 84,819 | 55 | 0.585 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 129,362 | 1.294 | 20 | 50 | fits | 33,558 | 43 | 0.681 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 992,122 | 9.921 | 20 | 20 | fits | 51,108 | 22 | 0.788 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 265,495 | 2.655 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 19,112 | 0.191 | 20 | 20 | fits | 32,511 | 27 (35) | 0.812 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 15,969 | 0.160 | 20 | 20 | fits | 28,769 | 23 (14) | 0.838 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 13,492 | 0.135 | 20 | 20 | fits | 28,587 | 24 (14) | 0.841 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 24,584 | 0.246 | 20 | 20 | fits | 29,331 | 21 (35) | 0.812 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 77,429 | 0.774 | 20 | 20 | fits | 28,178 | 8 | 0.760 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 44,919 | 0.449 | 20 | 20 | fits | 44,985 | 12 | 0.896 |
| malformed MRPDU discard | `srp.malformed.if0` | 21,239 | 0.212 | 20 | 20 | fits | 21,305 | 12 | 0.691 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 90,436 | 0.904 | 220 | 220 | fits | 57,083 | 6 | 0.901 |
| an event behind 15 others | `backlog.event.if0` | 170,222 | 1.702 | 20 | 200 | fits | 56,368 | 78 | 0.575 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 399,244 | 3.992 | 20 | 20 | fits | 148,870 | 167 | 0.396 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 421,260 | 4.213 | 20 | 200 | fits | 148,870 | 167 | 0.396 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 420,644 | 4.206 | 20 | 200 | fits | 148,870 | 167 | 0.396 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 416,938 | 4.169 | 20 | 20 | fits | 148,870 | 167 | 0.396 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 416,102 | 4.161 | 20 | 20 | fits | 148,870 | 167 | 0.396 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 155,430 | 1.554 | 20 | 24 | fits | 156,321 | 158 | 0.381 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 419,588 | 4.196 | 20 | 24 | fits | 148,870 | 167 | 0.396 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 419,522 | 4.195 | 20 | 50 | fits | 148,870 | 167 | 0.396 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 419,126 | 4.191 | 20 | 50 | fits | 148,870 | 167 | 0.396 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 450,436 | 4.504 | 20 | 20 | fits | 31,376 | 56 | 0.228 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 510,619 | 5.106 | 20 | 20 | fits | 24,668 | 41 | 0.192 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 358,627 | 3.586 | 20 | 20 | fits | 102,804 | 161 | 0.464 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 297,517 | 2.975 | 20 | 200 | fits | 149,932 | 234 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 409,062 | 4.091 | 20 | 200 | fits | 102,804 | 161 | 0.464 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 298,441 | 2.984 | 20 | 20 | fits | 149,932 | 234 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 409,766 | 4.098 | 20 | 20 | fits | 102,804 | 161 | 0.464 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 152,149 | 1.521 | 20 | 24 | fits | 152,335 | 155 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 301,091 | 3.011 | 20 | 24 | fits | 149,932 | 234 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 301,025 | 3.010 | 20 | 50 | fits | 149,932 | 234 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 412,790 | 4.128 | 20 | 50 | fits | 102,804 | 161 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 499,004 | 4.990 | 20 | 20 | fits | 86,280 | 24 | 0.792 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 992,224 | 9.922 | 20 | 20 | fits | 73,132 | 24 | 0.673 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 15,632 | 0.156 | 20 | 20 | fits | 27,557 | 19 | 0.821 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 297,517 | 2.975 | 20 | 200 | fits | 149,932 | 234 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 35,156 | 0.352 | 20 | 200 | fits | 27,557 | 19 | 0.821 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 298,441 | 2.984 | 20 | 20 | fits | 149,932 | 234 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 400,263 | 4.003 | 20 | 20 | fits | 93,301 | 151 | 0.430 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 152,149 | 1.521 | 20 | 24 | fits | 152,335 | 155 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 301,091 | 3.011 | 20 | 24 | fits | 149,932 | 234 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 301,025 | 3.010 | 20 | 50 | fits | 149,932 | 234 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 403,287 | 4.033 | 20 | 50 | fits | 93,301 | 151 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 489,065 | 4.891 | 20 | 20 | fits | 85,844 | 24 | 0.791 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 982,244 | 9.822 | 20 | 20 | fits | 73,132 | 24 | 0.673 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,290,483 | 62.905 | 20 | 20 | MISS ceiling | 18,812 | 14 | 0.637 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,309,229 | 63.092 | 20 | 20 | MISS ceiling | 18,822 | 13 | 0.630 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,327,978 | 63.280 | 20 | 20 | MISS ceiling | 18,806 | 13 | 0.630 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,346,639 | 63.466 | 20 | 20 | MISS ceiling | 18,737 | 13 | 0.637 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,365,221 | 63.652 | 20 | 20 | MISS ceiling | 18,645 | 13 | 0.654 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 160,211 | 1.602 | 20 | 200 | fits | 149,154 | 204 | 0.437 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 246,865 | 2.469 | 20 | 200 | fits | 87,270 | 179 | 0.395 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 155,889 | 1.559 | 20 | 20 | fits | 149,154 | 204 | 0.437 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,200,208 | 62.002 | 20 | 20 | MISS ceiling | 30,113 | 15 | 0.781 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 159,529 | 1.595 | 20 | 24 | fits | 149,154 | 204 | 0.437 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,173,581 | 61.736 | 20 | 24 | MISS ceiling | 141,054 | 106 | 0.415 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 158,473 | 1.585 | 20 | 50 | fits | 149,154 | 204 | 0.437 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 245,347 | 2.453 | 20 | 50 | fits | 87,270 | 179 | 0.395 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 331,191 | 3.312 | 20 | 20 | fits | 85,910 | 24 | 0.787 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 826,591 | 8.266 | 20 | 20 | fits | 73,553 | 24 | 0.673 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,929 | 0.059 | 20 | 20 | fits | 24,688 | 13 (29) | 0.809 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 8,148 | 0.081 | 20 | 20 | fits | 26,592 | 19 (35) | 0.808 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 12,734 | 0.127 | 20 | 20 | fits | 29,727 | 21 (12) | 0.822 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 10,038 | 0.100 | 20 | 50 | fits | 27,119 | 43 | 0.739 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 9,371 | 0.094 | 20 | 50 | fits | 23,534 | 35 | 0.719 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 7,311 | 0.073 | 20 | 50 | fits | 23,515 | 35 | 0.723 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 13,559 | 0.136 | 20 | 50 | fits | 28,584 | 61 | 0.649 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 15,764 | 0.158 | 20 | 50 | fits | 28,584 | 61 | 0.649 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 9,538 | 0.095 | 20 | 50 | fits | 22,353 | 30 | 0.661 |
| LINK_UP | `adp.link_up.if0` | 2,571 | 0.026 | 20 | 200 | fits | 27,119 | 43 (11) | 0.739 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 9,524 | 0.095 | 20 | 200 | fits | 23,107 | 23 (39) | 0.753 |
| LINK_DOWN | `adp.link_down.if0` | 2,352 | 0.024 | 20 | 200 | fits | 24,885 | 23 (9) | 0.787 |
| LINK_UP | `adp.link_up.if0` | 2,571 | 0.026 | 20 | 200 | fits | 27,119 | 43 (11) | 0.739 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 9,524 | 0.095 | 20 | 200 | fits | 23,107 | 23 (39) | 0.753 |
| GM_CHANGE | `adp.gm_change.if0` | 2,371 | 0.024 | 20 | 200 | fits | 17,717 | 17 (11) | 0.759 |
| LINK_UP | `adp.link_up.if0` | 2,571 | 0.026 | 20 | 200 | fits | 27,119 | 43 (11) | 0.739 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 9,524 | 0.095 | 20 | 200 | fits | 23,107 | 23 (39) | 0.753 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,616 | 0.046 | 20 | 200 | fits | 17,250 | 16 (31) | 0.667 |
| LINK_UP | `adp.link_up.if0` | 2,571 | 0.026 | 20 | 200 | fits | 27,119 | 43 (11) | 0.739 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 9,524 | 0.095 | 20 | 200 | fits | 23,107 | 23 (39) | 0.753 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,616 | 0.046 | 20 | 200 | fits | 17,250 | 16 (31) | 0.667 |
| set_name | `aecp_fanout.set_name.if0` | 52,028 | 0.520 | 20 | 24 | fits | 67,866 | 95 | 0.596 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 43,991 | 0.440 | 20 | 24 | fits | 57,203 | 78 | 0.607 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 48,131 | 0.481 | 20 | 24 | fits | 54,975 | 79 | 0.567 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 40,928 | 0.409 | 20 | 24 | fits | 51,498 | 78 | 0.558 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 50,661 | 0.507 | 20 | 24 | fits | 61,126 | 66 | 0.642 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 267,027 | 2.670 | 20 | 24 | fits | 59,166 | 65 | 0.641 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 325,444 | 3.254 | 20 | 24 | fits | 54,632 | 67 | 0.603 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 40,461 | 0.405 | 20 | 24 | fits | 50,904 | 78 | 0.556 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 45,319 | 0.453 | 20 | 24 | fits | 50,939 | 79 | 0.553 |
| BIND_RX | `acmp.bind_rx.if0` | 19,035 | 0.190 | 20 | 20 | fits | 41,470 | 26 (77) | 0.798 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,493 | 0.095 | 20 | 20 | fits | 31,952 | 19 (32) | 0.835 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,544 | 0.105 | 20 | 20 | fits | 26,236 | 15 (47) | 0.783 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 12,858 | 0.129 | 20 | 20 | fits | 38,179 | 18 (50) | 0.825 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,702 | 0.107 | 20 | 20 | fits | 26,682 | 17 (48) | 0.775 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,342 | 0.093 | 20 | 20 | fits | 25,296 | 16 (48) | 0.747 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,004 | 0.090 | 20 | 20 | fits | 24,460 | 16 (48) | 0.739 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 8,957 | 0.090 | 20 | 20 | fits | 24,311 | 16 (48) | 0.736 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 24,885 | 0.249 | 20 | 24 | fits | 27,993 | 20 | 0.776 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 19,218 | 0.192 | 20 | 24 | fits | 32,606 | 20 | 0.721 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 25,939 | 0.259 | 20 | 24 | fits | 27,588 | 20 | 0.734 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 15,103 | 0.151 | 20 | 24 | fits | 27,456 | 20 | 0.729 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 26,191 | 0.262 | 20 | 24 | fits | 27,741 | 20 | 0.726 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 26,259 | 0.263 | 20 | 24 | fits | 27,818 | 20 | 0.733 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 14,072 | 0.141 | 20 | 24 | fits | 26,739 | 20 | 0.729 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 25,532 | 0.255 | 20 | 24 | fits | 27,003 | 20 | 0.744 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 14,318 | 0.143 | 20 | 24 | fits | 26,387 | 20 | 0.746 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 27,710 | 0.277 | 20 | 24 | fits | 29,095 | 21 | 0.641 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 13,435 | 0.134 | 20 | 24 | fits | 26,088 | 20 | 0.762 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 13,516 | 0.135 | 20 | 24 | fits | 26,418 | 20 | 0.764 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 25,239 | 0.252 | 20 | 24 | fits | 26,624 | 20 | 0.727 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 15,156 | 0.152 | 20 | 24 | fits | 27,770 | 20 | 0.740 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 25,469 | 0.255 | 20 | 24 | fits | 27,108 | 20 | 0.744 |
| get_configuration | `aecp.get_configuration.if0` | 11,771 | 0.118 | 20 | 24 | fits | 24,044 | 20 | 0.736 |
| entity_available | `aecp.entity_available.if0` | 27,505 | 0.275 | 20 | 24 | fits | 28,898 | 26 | 0.731 |
| get_name | `aecp.get_name.if0` | 25,639 | 0.256 | 20 | 24 | fits | 27,284 | 20 | 0.747 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 15,098 | 0.151 | 20 | 24 | fits | 27,668 | 27 | 0.715 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 26,863 | 0.269 | 20 | 24 | fits | 28,601 | 29 | 0.758 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 12,759 | 0.128 | 20 | 24 | fits | 24,890 | 20 | 0.753 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 15,935 | 0.159 | 20 | 24 | fits | 24,058 | 20 | 0.727 |
| set_name | `aecp.set_name.if0` | 21,639 | 0.216 | 20 | 24 | fits | 44,645 | 43 | 0.765 |
| lock_entity | `aecp.lock_entity.if0` | 18,759 | 0.188 | 20 | 24 | fits | 35,606 | 34 | 0.779 |
| unlock_entity | `aecp.unlock_entity.if0` | 15,914 | 0.159 | 20 | 24 | fits | 36,897 | 33 | 0.779 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 134,819 | 1.348 | 20 | 24 | fits | 151,514 | 98 | 0.346 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 316,510 | 3.165 | 20 | 24 | fits | 137,980 | 70 | 0.313 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 217,337 | 2.173 | 20 | 24 | fits | 42,242 | 17 | 0.698 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 383,383 | 3.834 | 20 | 24 | fits | 100,249 | 33 | 0.683 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 306,906 | 3.069 | 20 | 24 | fits | 93,278 | 17 | 0.667 |
| LINK_UP | `fixture.link_up.if0` | 2,571 | 0.026 | 20 | 200 | fits | 27,119 | 43 (11) | 0.739 |
| malformed MRPDU discard | `fixture.malformed.if0` | 21,785 | 0.218 | 20 | 20 | fits | 21,851 | 12 | 0.735 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 31,707 | 0.317 | 20 | 24 | fits | 46,401 | 43 | 0.781 |
| LINK_DOWN | `fixture.link_down.if0` | 2,648 | 0.026 | 20 | 200 | fits | 26,482 | 23 (9) | 0.794 |
| BIND_RX | `fixture.bind_rx.if0` | 19,508 | 0.195 | 20 | 20 | fits | 41,432 | 26 (77) | 0.800 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 13,902 | 0.139 | 20 | 20 | fits | 36,762 | 29 (35) | 0.789 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 19,599 | 0.196 | 20 | 20 | fits | 25,207 | 13 (29) | 0.818 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 81,052 | 0.811 | 20 | 200 | fits | 81,156 | 49 | 0.757 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 81,052 | 0.811 | 20 | 200 | fits | 81,156 | 49 | 0.757 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 80,778 | 0.808 | 20 | 20 | fits | 81,156 | 49 | 0.757 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 80,778 | 0.808 | 20 | 20 | fits | 81,156 | 49 | 0.757 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 80,986 | 0.810 | 20 | 24 | fits | 81,156 | 49 | 0.757 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 80,986 | 0.810 | 20 | 24 | fits | 81,156 | 49 | 0.757 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 80,920 | 0.809 | 20 | 50 | fits | 81,156 | 49 | 0.757 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 80,920 | 0.809 | 20 | 50 | fits | 81,156 | 49 | 0.757 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 80,854 | 0.809 | 20 | 20 | fits | 81,156 | 49 | 0.757 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 80,854 | 0.809 | 20 | 20 | fits | 81,156 | 49 | 0.757 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
