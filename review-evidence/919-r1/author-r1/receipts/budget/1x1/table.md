### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 92 paths and 7 of 950 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.190 (0.400) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.096 (0.230) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.075 (0.251) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.186 (0.512) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.103 (0.240) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.096 (0.230) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.098 (0.235) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.103 (0.254) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.095 (0.317) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.096 (0.286) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.110 (0.438) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.205 (0.537) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.051 (0.247) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.134 (0.537) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.096 (0.420) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.130 (0.389) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.044 (0.159) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.026 (0.160) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.028 (0.272) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.027 (0.262) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.033 (0.179) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.084 (0.373) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.157 (0.440) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.190 (0.482) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.211 (0.496) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.241 (0.534) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.181 (0.476) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.268 (0.601) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.158 (0.444) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.275 (0.567) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.179 (0.468) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.178 (0.467) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.225 (0.513) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.201 (0.490) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.224 (0.512) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.224 (0.512) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.232 (0.522) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.176 (0.465) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.237 (0.528) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.177 (0.468) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.237 (0.527) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.184 (0.472) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.231 (0.519) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.150 (0.441) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.264 (0.647) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.212 (0.501) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.220 (0.576) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.004 (2.286) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.473 (0.763) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.606 (0.891) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.507 (0.795) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.560 (0.818) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.550 (0.850) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 2.334 (2.632) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.525 (0.783) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 1.447 (1.737) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 1.391 (1.731) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 2.813 (3.145) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 2.449 (2.788) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.385 (1.685) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.224 (4.605) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 4.415 (5.115) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.139 (0.485) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.672 (2.081) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.731 (62.995) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.424 (63.687) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.321 (0.453) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 2.309 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 1.542 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 2.818 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 1.584 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.285 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.224 (0.530) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.089 (0.204) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.109 (0.262) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.203 (0.530) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.200 (0.491) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.604 | fits | 0 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.137 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 61.893 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.181 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 4.999 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.187 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.646 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.163 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.maap.last.if0` (backlog-adp@program-aged2-7) | 5.036 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-6.service.srp.first.if0` (backlog-adp@blank-aged2-6) | 5.941 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.srp.last.if0` (backlog-adp@program-aged2-7) | 9.948 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.978 (1.092) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.435 (0.436) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.209 (0.210) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.887 (0.959) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.035 | 11 | 148,934 (1.489) | yes | - |
| backlog-adp@blank-1 | 0 | 10.251 | 10 | 148,758 (1.488) | yes | - |
| backlog-adp@blank-2 | 0 | 10.301 | 10 | 148,662 (1.487) | yes | - |
| backlog-adp@blank-3 | 0 | 10.185 | 9 | 143,725 (1.437) | yes | - |
| backlog-adp@blank-4 | 0 | 10.245 | 10 | 148,758 (1.488) | yes | - |
| backlog-adp@blank-5 | 0 | 10.679 | 12 | 148,814 (1.488) | yes | - |
| backlog-adp@blank-6 | 0 | 10.562 | 12 | 148,760 (1.488) | yes | - |
| backlog-adp@blank-7 | 0 | 10.258 | 10 | 148,603 (1.486) | yes | - |
| backlog-adp@program-0 | 0 | 10.427 | 11 | 148,700 (1.487) | yes | - |
| backlog-adp@program-1 | 0 | 10.265 | 10 | 148,796 (1.488) | yes | - |
| backlog-adp@program-2 | 0 | 10.305 | 10 | 149,264 (1.493) | yes | - |
| backlog-adp@program-3 | 0 | 10.291 | 10 | 148,647 (1.486) | yes | - |
| backlog-adp@program-4 | 0 | 9.693 | 11 | 148,521 (1.485) | yes | - |
| backlog-adp@program-5 | 0 | 10.019 | 12 | 148,565 (1.486) | yes | - |
| backlog-adp@program-6 | 0 | 9.586 | 10 | 148,433 (1.484) | yes | - |
| backlog-adp@program-7 | 0 | 9.540 | 10 | 148,529 (1.485) | yes | - |
| backlog-adp@verify-0 | 0 | 10.752 | 11 | 148,774 (1.488) | yes | - |
| backlog-adp@verify-1 | 0 | 10.261 | 10 | 148,656 (1.487) | yes | - |
| backlog-adp@verify-2 | 0 | 10.309 | 10 | 148,560 (1.486) | yes | - |
| backlog-adp@verify-3 | 0 | 10.194 | 10 | 148,560 (1.486) | yes | - |
| backlog-adp@verify-4 | 0 | 10.916 | 12 | 148,656 (1.487) | yes | - |
| backlog-adp@verify-5 | 0 | 10.560 | 12 | 148,694 (1.487) | yes | - |
| backlog-adp@verify-6 | 0 | 10.319 | 10 | 148,647 (1.486) | yes | - |
| backlog-adp@verify-7 | 0 | 10.230 | 10 | 148,647 (1.486) | yes | - |
| backlog-adp@blank-aged2-0 | 1 | 10.216 | 10 | 144,567 (1.446) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 10.829 | 12 | 148,725 (1.487) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 10.388 | 11 | 148,859 (1.489) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 10.245 | 10 | 148,240 (1.482) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 10.224 | 10 | 148,086 (1.481) | yes | - |
| backlog-adp@blank-aged2-5 | 1 | 10.190 | 9 | 144,498 (1.445) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 10.291 | 10 | 148,144 (1.481) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 10.275 | 10 | 148,144 (1.481) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 12.149 | 13 | 147,957 (1.480) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 11.046 | 12 | 149,409 (1.494) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 11.071 | 11 | 144,974 (1.450) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 11.552 | 14 | 148,015 (1.480) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 11.326 | 14 | 148,035 (1.480) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 11.080 | 12 | 147,986 (1.480) | yes | - |
| backlog-adp@blank-aged1-6 | 1 | 11.069 | 11 | 144,182 (1.442) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 12.125 | 11 | 144,750 (1.448) | yes | - |
| backlog-adp@program-aged2-0 | 1 | 10.654 | 11 | 144,703 (1.447) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 10.480 | 11 | 144,343 (1.443) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 10.318 | 10 | 149,190 (1.492) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 10.295 | 10 | 148,155 (1.482) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 10.272 | 10 | 149,516 (1.495) | yes | - |
| backlog-adp@program-aged2-5 | 1 | 10.193 | 9 | 143,768 (1.438) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 10.212 | 9 | 145,006 (1.450) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 10.441 | 11 | 150,087 (1.501) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 10.568 | 11 | 149,320 (1.493) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.902 | 12 | 148,155 (1.482) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 10.471 | 11 | 144,114 (1.441) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 10.339 | 10 | 148,159 (1.482) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 10.313 | 10 | 148,088 (1.481) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 10.276 | 10 | 149,350 (1.494) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 10.246 | 10 | 148,088 (1.481) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 10.226 | 9 | 144,818 (1.448) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.243 | 11 | 148,349 (1.483) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 10.077 | 9 | 144,862 (1.449) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 10.328 | 10 | 149,554 (1.496) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 10.265 | 10 | 148,291 (1.483) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 10.244 | 10 | 148,291 (1.483) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 10.425 | 12 | 148,454 (1.485) | yes | - |
| backlog-adp@verify-aged2-6 | 1 | 10.235 | 9 | 144,982 (1.450) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 10.335 | 10 | 148,358 (1.484) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 11.360 | 12 | 148,524 (1.485) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 10.585 | 12 | 148,458 (1.485) | yes | - |
| backlog-adp@verify-aged1-2 | 1 | 10.194 | 9 | 144,642 (1.446) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 10.309 | 10 | 149,227 (1.492) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 10.281 | 10 | 148,358 (1.484) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 10.229 | 10 | 149,553 (1.496) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 10.222 | 10 | 148,358 (1.484) | yes | - |
| backlog-adp@verify-aged1-7 | 1 | 10.437 | 11 | 144,407 (1.444) | yes | - |
| backlog | 0 | 5.669 | 7 | 152,231 (1.522) | yes | - |
| backlog-adp | 0 | 9.446 | 10 | 148,406 (1.484) | yes | - |
| backlog-adp-refill | 0 | 40.758 | 24 | 148,406 (1.484) | yes | - |
| backlog-owed | 0 | 64.005 | 25 | 145,993 (1.460) | yes | - |
| fixture | 0 | 1.257 | 2 | 82,265 (0.823) | yes | - |

Composed maximum over the 4 backlog windows: 152,231 CPU cycles (1.522 ms), backlog.
Over the windows that released their whole load only: 152,231 (1.522 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3610 | 0 | 42,250 (0.422) | fits |
| save-second | 50226 | 0 | 49,812 (0.498) | fits |
| backlog-adp@blank-0 | 407 | 0 | 148,934 (1.489) | fits |
| backlog-adp@blank-1 | 406 | 0 | 148,758 (1.488) | fits |
| backlog-adp@blank-2 | 406 | 0 | 148,662 (1.487) | fits |
| backlog-adp@blank-3 | 406 | 0 | 148,662 (1.487) | fits |
| backlog-adp@blank-4 | 406 | 0 | 148,758 (1.488) | fits |
| backlog-adp@blank-5 | 408 | 0 | 148,814 (1.488) | fits |
| backlog-adp@blank-6 | 408 | 0 | 148,760 (1.488) | fits |
| backlog-adp@blank-7 | 408 | 0 | 148,603 (1.486) | fits |
| backlog-adp@program-0 | 503 | 0 | 148,700 (1.487) | fits |
| backlog-adp@program-1 | 502 | 0 | 148,796 (1.488) | fits |
| backlog-adp@program-2 | 504 | 0 | 149,264 (1.493) | fits |
| backlog-adp@program-3 | 504 | 0 | 148,647 (1.486) | fits |
| backlog-adp@program-4 | 506 | 0 | 148,521 (1.485) | fits |
| backlog-adp@program-5 | 507 | 0 | 148,565 (1.486) | fits |
| backlog-adp@program-6 | 507 | 0 | 148,433 (1.484) | fits |
| backlog-adp@program-7 | 507 | 0 | 148,529 (1.485) | fits |
| backlog-adp@verify-0 | 591 | 0 | 148,774 (1.488) | fits |
| backlog-adp@verify-1 | 590 | 0 | 148,656 (1.487) | fits |
| backlog-adp@verify-2 | 590 | 0 | 148,560 (1.486) | fits |
| backlog-adp@verify-3 | 590 | 0 | 148,560 (1.486) | fits |
| backlog-adp@verify-4 | 592 | 0 | 148,656 (1.487) | fits |
| backlog-adp@verify-5 | 592 | 0 | 148,694 (1.487) | fits |
| backlog-adp@verify-6 | 592 | 0 | 148,647 (1.486) | fits |
| backlog-adp@verify-7 | 592 | 0 | 148,647 (1.486) | fits |
| backlog-adp@blank-aged2-0 | 724 | 0 | 153,448 (1.534) | fits |
| backlog-adp@blank-aged2-1 | 730 | 0 | 148,725 (1.487) | fits |
| backlog-adp@blank-aged2-2 | 737 | 0 | 148,859 (1.489) | fits |
| backlog-adp@blank-aged2-3 | 744 | 0 | 148,240 (1.482) | fits |
| backlog-adp@blank-aged2-4 | 752 | 0 | 148,086 (1.481) | fits |
| backlog-adp@blank-aged2-5 | 760 | 0 | 148,086 (1.481) | fits |
| backlog-adp@blank-aged2-6 | 769 | 0 | 148,144 (1.481) | fits |
| backlog-adp@blank-aged2-7 | 777 | 0 | 148,144 (1.481) | fits |
| backlog-adp@blank-aged1-0 | 661 | 0 | 147,957 (1.480) | fits |
| backlog-adp@blank-aged1-1 | 668 | 0 | 149,409 (1.494) | fits |
| backlog-adp@blank-aged1-2 | 676 | 0 | 147,957 (1.480) | fits |
| backlog-adp@blank-aged1-3 | 687 | 0 | 148,015 (1.480) | fits |
| backlog-adp@blank-aged1-4 | 695 | 0 | 148,035 (1.480) | fits |
| backlog-adp@blank-aged1-5 | 701 | 0 | 147,986 (1.480) | fits |
| backlog-adp@blank-aged1-6 | 709 | 0 | 147,986 (1.480) | fits |
| backlog-adp@blank-aged1-7 | 717 | 0 | 147,986 (1.480) | fits |
| backlog-adp@program-aged2-0 | 816 | 0 | 148,263 (1.483) | fits |
| backlog-adp@program-aged2-1 | 824 | 0 | 148,197 (1.482) | fits |
| backlog-adp@program-aged2-2 | 831 | 0 | 149,190 (1.492) | fits |
| backlog-adp@program-aged2-3 | 839 | 0 | 148,155 (1.482) | fits |
| backlog-adp@program-aged2-4 | 847 | 0 | 149,516 (1.495) | fits |
| backlog-adp@program-aged2-5 | 855 | 0 | 148,155 (1.482) | fits |
| backlog-adp@program-aged2-6 | 863 | 0 | 148,155 (1.482) | fits |
| backlog-adp@program-aged2-7 | 873 | 0 | 150,087 (1.501) | fits |
| backlog-adp@program-aged1-0 | 750 | 0 | 149,320 (1.493) | fits |
| backlog-adp@program-aged1-1 | 759 | 0 | 148,155 (1.482) | fits |
| backlog-adp@program-aged1-2 | 767 | 0 | 148,295 (1.483) | fits |
| backlog-adp@program-aged1-3 | 774 | 0 | 148,159 (1.482) | fits |
| backlog-adp@program-aged1-4 | 782 | 0 | 148,088 (1.481) | fits |
| backlog-adp@program-aged1-5 | 790 | 0 | 149,350 (1.494) | fits |
| backlog-adp@program-aged1-6 | 798 | 0 | 148,088 (1.481) | fits |
| backlog-adp@program-aged1-7 | 806 | 0 | 148,088 (1.481) | fits |
| backlog-adp@verify-aged2-0 | 905 | 0 | 148,349 (1.483) | fits |
| backlog-adp@verify-aged2-1 | 912 | 0 | 148,349 (1.483) | fits |
| backlog-adp@verify-aged2-2 | 921 | 0 | 149,554 (1.496) | fits |
| backlog-adp@verify-aged2-3 | 929 | 0 | 148,291 (1.483) | fits |
| backlog-adp@verify-aged2-4 | 937 | 0 | 148,291 (1.483) | fits |
| backlog-adp@verify-aged2-5 | 947 | 0 | 148,454 (1.485) | fits |
| backlog-adp@verify-aged2-6 | 954 | 0 | 149,406 (1.494) | fits |
| backlog-adp@verify-aged2-7 | 962 | 0 | 148,358 (1.484) | fits |
| backlog-adp@verify-aged1-0 | 841 | 0 | 148,524 (1.485) | fits |
| backlog-adp@verify-aged1-1 | 849 | 0 | 148,458 (1.485) | fits |
| backlog-adp@verify-aged1-2 | 855 | 0 | 148,300 (1.483) | fits |
| backlog-adp@verify-aged1-3 | 864 | 0 | 149,227 (1.492) | fits |
| backlog-adp@verify-aged1-4 | 872 | 0 | 148,358 (1.484) | fits |
| backlog-adp@verify-aged1-5 | 880 | 0 | 149,553 (1.496) | fits |
| backlog-adp@verify-aged1-6 | 888 | 0 | 148,358 (1.484) | fits |
| backlog-adp@verify-aged1-7 | 898 | 0 | 148,480 (1.485) | fits |
| adp-advertise | 599 | 0 | 41,913 (0.419) | fits |
| save-held | 1401 | 0 | 155,175 (1.552) | fits |
| save-starved | 26949 | 0 | 155,175 (1.552) | fits |
| acmp-noresp | 2027 | 0 | 41,913 (0.419) | fits |
| save | 610 | 0 | 44,444 (0.444) | fits |
| srp | 290 | 0 | 69,635 (0.696) | fits |
| backlog | 286 | 0 | 152,231 (1.522) | fits |
| backlog-adp | 312 | 0 | 148,406 (1.484) | fits |
| backlog-adp-refill | 326 | 0 | 148,406 (1.484) | fits |
| backlog-owed | 310 | 0 | 145,993 (1.460) | fits |
| acmp-disc | 938 | 0 | 41,913 (0.419) | fits |
| maap | 176 | 0 | 41,913 (0.419) | fits |
| adp-link | 90 | 0 | 45,822 (0.458) | fits |
| adp-gm | 89 | 0 | 41,913 (0.419) | fits |
| adp-discover | 89 | 0 | 41,913 (0.419) | fits |
| control | 89 | 0 | 41,913 (0.419) | fits |
| aecp-fanout | 112 | 0 | 62,329 (0.623) | fits |
| acmp-cmd | 87 | 0 | 41,913 (0.419) | fits |
| aecp | 112 | 0 | 43,443 (0.434) | fits |
| aecp-largest-notice | 106 | 0 | 146,287 (1.463) | fits |
| datapath-events | 118 | 0 | 41,913 (0.419) | fits |
| fixture | 161 | 0 | 82,265 (0.823) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | +9.141 ms, 76,447 (0.764 ms), read-back | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 8.906 (20) | 11.094 |
| backlog-adp@blank-aged2-1 | 2 | none | +9.086 ms, 76,549 (0.765 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 9.048 (20) | 10.952 |
| backlog-adp@blank-aged2-2 | 2 | +8.494 ms, 76,549 (0.765 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 9.786 (20) | 10.214 |
| backlog-adp@blank-aged2-3 | 2 | +6.678 ms, 76,549 (0.765 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 9.761 (20) | 10.239 |
| backlog-adp@blank-aged2-4 | 2 | +5.815 ms, 76,549 (0.765 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 9.742 (20) | 10.258 |
| backlog-adp@blank-aged2-5 | 2 | +4.831 ms, 76,820 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 9.707 (20) | 10.293 |
| backlog-adp@blank-aged2-6 | 2 | none | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 9.804 (20) | 10.196 |
| backlog-adp@blank-aged2-7 | 2 | none | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 9.785 (20) | 10.215 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 8.922 (20) | 11.078 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 9.043 (20) | 10.957 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 9.470 (20) | 10.530 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 9.872 (20) | 10.128 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 9.803 (20) | 10.197 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 9.835 (20) | 10.165 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 9.823 (20) | 10.177 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 9.802 (20) | 10.198 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 8.836 (20) | 11.164 |
| backlog-adp@program-aged2-1 | 2 | none | +8.932 ms, 80,239 (0.802 ms), issue | `backlog-adp@program-aged2-1.service.srp.last.if0` | 8.894 (20) | 11.106 |
| backlog-adp@program-aged2-2 | 2 | +8.428 ms, 80,215 (0.802 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 9.828 (20) | 10.172 |
| backlog-adp@program-aged2-3 | 2 | +6.724 ms, 80,215 (0.802 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 9.807 (20) | 10.193 |
| backlog-adp@program-aged2-4 | 2 | +5.864 ms, 80,215 (0.802 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 9.785 (20) | 10.215 |
| backlog-adp@program-aged2-5 | 2 | +4.944 ms, 80,551 (0.806 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 9.704 (20) | 10.296 |
| backlog-adp@program-aged2-6 | 2 | +4.176 ms, 80,128 (0.801 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 9.722 (20) | 10.278 |
| backlog-adp@program-aged2-7 | 2 | +3.144 ms, 79,984 (0.800 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 9.948 (20) | 10.052 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 8.895 (20) | 11.105 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 8.944 (20) | 11.056 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 8.905 (20) | 11.095 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 9.046 (20) | 10.954 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 9.025 (20) | 10.975 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 8.988 (20) | 11.012 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 8.951 (20) | 11.049 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 8.929 (20) | 11.071 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 8.905 (20) | 11.095 |
| backlog-adp@verify-aged2-1 | 2 | none | +8.991 ms, 77,237 (0.772 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 8.954 (20) | 11.046 |
| backlog-adp@verify-aged2-2 | 2 | +8.582 ms, 77,237 (0.772 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 9.839 (20) | 10.161 |
| backlog-adp@verify-aged2-3 | 2 | +6.733 ms, 77,237 (0.772 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 9.776 (20) | 10.224 |
| backlog-adp@verify-aged2-4 | 2 | +5.982 ms, 77,237 (0.772 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 9.754 (20) | 10.246 |
| backlog-adp@verify-aged2-5 | 2 | +4.942 ms, 77,508 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 9.667 (20) | 10.333 |
| backlog-adp@verify-aged2-6 | 2 | +4.077 ms, 77,285 (0.773 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 9.749 (20) | 10.251 |
| backlog-adp@verify-aged2-7 | 2 | +3.012 ms, 76,916 (0.769 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 9.849 (20) | 10.151 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 8.873 (20) | 11.127 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 8.910 (20) | 11.090 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 8.944 (20) | 11.056 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 9.060 (20) | 10.940 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 9.032 (20) | 10.968 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 8.976 (20) | 11.024 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 8.967 (20) | 11.033 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 8.912 (20) | 11.088 |

Least margin over the aged windows: 10.052 ms, `backlog-adp@program-aged2-7.service.srp.last.if0` at 9.948 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.421 | 6,070 | 102 | 2 | 30.800 | yes | within |
| save-held | 2018.297 | 4,070 | 102 | - | 15.341 | no | within |
| save-starved | 4048.220 | 4,070 | 102 | - | 31.086 | yes | within |
| save | 2018.633 | 4,070 | 102 | - | 10.902 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 95,969 (0.960) | 77,913 (0.779) |
| save-second | 520 | 79,609 (0.796) | 77,463 (0.775) |
| backlog-adp@blank-0 | 299 | 90,442 (0.904) | 76,111 (0.761) |
| backlog-adp@blank-1 | 299 | 91,244 (0.912) | 76,195 (0.762) |
| backlog-adp@blank-2 | 299 | 91,217 (0.912) | 76,195 (0.762) |
| backlog-adp@blank-3 | 299 | 91,314 (0.913) | 76,197 (0.762) |
| backlog-adp@blank-4 | 299 | 91,349 (0.913) | 76,195 (0.762) |
| backlog-adp@blank-5 | 299 | 91,362 (0.914) | 76,241 (0.762) |
| backlog-adp@blank-6 | 299 | 97,775 (0.978) | 76,310 (0.763) |
| backlog-adp@blank-7 | 299 | 91,016 (0.910) | 76,178 (0.762) |
| backlog-adp@program-0 | 328 | 95,479 (0.955) | 78,587 (0.786) |
| backlog-adp@program-1 | 328 | 95,479 (0.955) | 78,671 (0.787) |
| backlog-adp@program-2 | 328 | 95,479 (0.955) | 78,722 (0.787) |
| backlog-adp@program-3 | 328 | 95,479 (0.955) | 78,702 (0.787) |
| backlog-adp@program-4 | 329 | 95,479 (0.955) | 77,961 (0.780) |
| backlog-adp@program-5 | 329 | 95,479 (0.955) | 77,961 (0.780) |
| backlog-adp@program-6 | 329 | 95,479 (0.955) | 77,961 (0.780) |
| backlog-adp@program-7 | 329 | 95,479 (0.955) | 77,961 (0.780) |
| backlog-adp@verify-0 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-1 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-2 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-3 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-4 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-5 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-6 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-7 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@blank-aged2-0 | 297 | 76,447 (0.764) | 75,541 (0.755) |
| backlog-adp@blank-aged2-1 | 297 | 76,549 (0.765) | 75,625 (0.756) |
| backlog-adp@blank-aged2-2 | 297 | 76,549 (0.765) | 75,625 (0.756) |
| backlog-adp@blank-aged2-3 | 297 | 76,549 (0.765) | 75,625 (0.756) |
| backlog-adp@blank-aged2-4 | 297 | 76,549 (0.765) | 75,625 (0.756) |
| backlog-adp@blank-aged2-5 | 297 | 76,820 (0.768) | 75,813 (0.758) |
| backlog-adp@blank-aged2-6 | 297 | 84,290 (0.843) | 75,550 (0.755) |
| backlog-adp@blank-aged2-7 | 297 | 84,112 (0.841) | 75,550 (0.755) |
| backlog-adp@blank-aged1-0 | 298 | 96,370 (0.964) | 76,179 (0.762) |
| backlog-adp@blank-aged1-1 | 297 | 96,742 (0.967) | 76,285 (0.763) |
| backlog-adp@blank-aged1-2 | 297 | 97,336 (0.973) | 76,285 (0.763) |
| backlog-adp@blank-aged1-3 | 297 | 91,562 (0.916) | 76,220 (0.762) |
| backlog-adp@blank-aged1-4 | 297 | 89,889 (0.899) | 76,097 (0.761) |
| backlog-adp@blank-aged1-5 | 297 | 91,035 (0.910) | 76,179 (0.762) |
| backlog-adp@blank-aged1-6 | 297 | 91,035 (0.910) | 76,179 (0.762) |
| backlog-adp@blank-aged1-7 | 298 | 91,082 (0.911) | 76,179 (0.762) |
| backlog-adp@program-aged2-0 | 327 | 95,479 (0.955) | 78,860 (0.789) |
| backlog-adp@program-aged2-1 | 326 | 95,479 (0.955) | 78,336 (0.783) |
| backlog-adp@program-aged2-2 | 326 | 95,479 (0.955) | 78,252 (0.783) |
| backlog-adp@program-aged2-3 | 326 | 95,479 (0.955) | 78,252 (0.783) |
| backlog-adp@program-aged2-4 | 326 | 95,479 (0.955) | 78,252 (0.783) |
| backlog-adp@program-aged2-5 | 326 | 95,479 (0.955) | 78,460 (0.785) |
| backlog-adp@program-aged2-6 | 326 | 95,479 (0.955) | 78,005 (0.780) |
| backlog-adp@program-aged2-7 | 326 | 95,479 (0.955) | 77,974 (0.780) |
| backlog-adp@program-aged1-0 | 327 | 95,479 (0.955) | 78,860 (0.789) |
| backlog-adp@program-aged1-1 | 326 | 95,479 (0.955) | 78,671 (0.787) |
| backlog-adp@program-aged1-2 | 326 | 95,593 (0.956) | 78,598 (0.786) |
| backlog-adp@program-aged1-3 | 326 | 95,479 (0.955) | 78,671 (0.787) |
| backlog-adp@program-aged1-4 | 326 | 95,479 (0.955) | 78,671 (0.787) |
| backlog-adp@program-aged1-5 | 326 | 95,479 (0.955) | 78,722 (0.787) |
| backlog-adp@program-aged1-6 | 326 | 95,479 (0.955) | 78,860 (0.789) |
| backlog-adp@program-aged1-7 | 326 | 95,479 (0.955) | 78,860 (0.789) |
| backlog-adp@verify-aged2-0 | 356 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-aged2-1 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-aged2-2 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-aged2-3 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-aged2-4 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-aged2-5 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-aged2-6 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-aged2-7 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-aged1-0 | 356 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-aged1-1 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-aged1-2 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-aged1-3 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-aged1-4 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-aged1-5 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-aged1-6 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| backlog-adp@verify-aged1-7 | 355 | 95,479 (0.955) | 77,963 (0.780) |
| adp-advertise | 578 | 21,130 (0.211) | 2,097 (0.021) |
| save-held | 722 | 94,378 (0.944) | 78,312 (0.783) |
| save-starved | 418 | 80,250 (0.802) | 77,883 (0.779) |
| acmp-noresp | 615 | 95,484 (0.955) | 77,978 (0.780) |
| save | 585 | 94,620 (0.946) | 77,633 (0.776) |
| srp | 271 | 21,130 (0.211) | 2,097 (0.021) |
| backlog | 265 | 21,130 (0.211) | 2,097 (0.021) |
| backlog-adp | 271 | 21,130 (0.211) | 2,395 (0.024) |
| backlog-adp-refill | 274 | 21,130 (0.211) | 2,395 (0.024) |
| backlog-owed | 276 | 21,130 (0.211) | 2,160 (0.022) |
| acmp-disc | 305 | 95,583 (0.956) | 77,901 (0.779) |
| maap | 163 | 21,130 (0.211) | 2,097 (0.021) |
| adp-link | 80 | 21,130 (0.211) | 2,097 (0.021) |
| adp-gm | 80 | 21,130 (0.211) | 2,097 (0.021) |
| adp-discover | 80 | 21,130 (0.211) | 2,097 (0.021) |
| control | 80 | 21,130 (0.211) | 2,097 (0.021) |
| aecp-fanout | 80 | 21,130 (0.211) | 2,097 (0.021) |
| acmp-cmd | 65 | 21,130 (0.211) | 2,097 (0.021) |
| aecp | 79 | 21,130 (0.211) | 2,097 (0.021) |
| aecp-largest-notice | 78 | 21,130 (0.211) | 2,097 (0.021) |
| datapath-events | 70 | 21,130 (0.211) | 2,097 (0.021) |
| fixture | 54 | 15,701 (0.157) | 1,984 (0.020) |

Longest pass that carries a step: 97,775 CPU cycles (0.978 ms), backlog-adp@blank-6; longest step: 78,860 (0.789 ms), backlog-adp@program-aged2-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 13,401 | 0.134 | 20 | 20 | fits | 33,270 | 19 (14) | 0.881 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 414,746 | 4.147 | 20 | 20 | fits | 108,360 | 163 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 357,602 | 3.576 | 20 | 200 | fits | 143,422 | 226 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 465,346 | 4.653 | 20 | 200 | fits | 108,360 | 163 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 358,526 | 3.585 | 20 | 20 | fits | 143,422 | 226 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 466,050 | 4.660 | 20 | 20 | fits | 108,360 | 163 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 218,744 | 2.187 | 20 | 24 | fits | 148,934 | 155 | 0.348 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 361,176 | 3.612 | 20 | 24 | fits | 143,422 | 226 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 361,110 | 3.611 | 20 | 50 | fits | 143,422 | 226 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 469,074 | 4.691 | 20 | 50 | fits | 108,360 | 163 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 558,850 | 5.588 | 20 | 20 | fits | 89,842 | 28 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 960,564 | 9.606 | 20 | 20 | fits | 52,637 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 340,503 | 3.405 | 20 | 20 | fits | 108,458 | 163 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 290,844 | 2.908 | 20 | 200 | fits | 143,419 | 226 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 398,686 | 3.987 | 20 | 200 | fits | 108,458 | 163 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 291,768 | 2.918 | 20 | 20 | fits | 143,419 | 226 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 399,390 | 3.994 | 20 | 20 | fits | 108,458 | 163 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 151,989 | 1.520 | 20 | 24 | fits | 148,758 | 155 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 294,418 | 2.944 | 20 | 24 | fits | 143,419 | 226 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 294,352 | 2.944 | 20 | 50 | fits | 143,419 | 226 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 402,414 | 4.024 | 20 | 50 | fits | 108,458 | 163 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 492,147 | 4.921 | 20 | 20 | fits | 89,799 | 28 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 900,571 | 9.006 | 20 | 20 | fits | 58,680 | 26 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 345,732 | 3.457 | 20 | 20 | fits | 108,355 | 163 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 296,009 | 2.960 | 20 | 200 | fits | 143,144 | 226 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 403,748 | 4.037 | 20 | 200 | fits | 108,355 | 163 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 296,933 | 2.969 | 20 | 20 | fits | 143,144 | 226 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 404,452 | 4.045 | 20 | 20 | fits | 108,355 | 163 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 157,429 | 1.574 | 20 | 24 | fits | 148,662 | 155 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 299,583 | 2.996 | 20 | 24 | fits | 143,144 | 226 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 299,517 | 2.995 | 20 | 50 | fits | 143,144 | 226 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 407,476 | 4.075 | 20 | 50 | fits | 108,355 | 163 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 497,277 | 4.973 | 20 | 20 | fits | 89,867 | 28 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 905,560 | 9.056 | 20 | 20 | fits | 52,332 | 20 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 337,376 | 3.374 | 20 | 20 | fits | 107,986 | 164 | 0.435 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 287,622 | 2.876 | 20 | 200 | fits | 143,725 | 226 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 394,992 | 3.950 | 20 | 200 | fits | 107,986 | 164 | 0.435 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 288,546 | 2.885 | 20 | 20 | fits | 143,725 | 226 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 395,696 | 3.957 | 20 | 20 | fits | 107,986 | 164 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 148,461 | 1.485 | 20 | 24 | fits | 148,662 | 155 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 291,196 | 2.912 | 20 | 24 | fits | 143,725 | 226 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 291,130 | 2.911 | 20 | 50 | fits | 143,725 | 226 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 398,720 | 3.987 | 20 | 50 | fits | 107,986 | 164 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 489,743 | 4.897 | 20 | 20 | fits | 82,705 | 31 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 893,906 | 8.939 | 20 | 20 | fits | 62,917 | 24 | 0.586 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 362,008 | 3.620 | 20 | 20 | fits | 112,157 | 170 | 0.459 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 293,167 | 2.932 | 20 | 200 | fits | 143,638 | 227 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 413,028 | 4.130 | 20 | 200 | fits | 112,157 | 170 | 0.459 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 294,091 | 2.941 | 20 | 20 | fits | 143,638 | 227 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 413,732 | 4.137 | 20 | 20 | fits | 112,157 | 170 | 0.459 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 154,093 | 1.541 | 20 | 24 | fits | 148,758 | 155 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 296,741 | 2.967 | 20 | 24 | fits | 143,638 | 227 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 296,675 | 2.967 | 20 | 50 | fits | 143,638 | 227 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 416,756 | 4.168 | 20 | 50 | fits | 112,157 | 170 | 0.459 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 506,928 | 5.069 | 20 | 20 | fits | 90,238 | 28 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 899,748 | 8.997 | 20 | 20 | fits | 52,149 | 20 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 356,806 | 3.568 | 20 | 20 | fits | 108,625 | 163 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 307,016 | 3.070 | 20 | 200 | fits | 144,636 | 231 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 415,025 | 4.150 | 20 | 200 | fits | 108,625 | 163 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 307,940 | 3.079 | 20 | 20 | fits | 144,636 | 231 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 415,729 | 4.157 | 20 | 20 | fits | 108,625 | 163 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 159,685 | 1.597 | 20 | 24 | fits | 148,814 | 156 | 0.346 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 310,590 | 3.106 | 20 | 24 | fits | 144,636 | 231 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 310,524 | 3.105 | 20 | 50 | fits | 144,636 | 231 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 418,753 | 4.188 | 20 | 50 | fits | 108,625 | 163 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 504,194 | 5.042 | 20 | 20 | fits | 85,507 | 30 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 900,838 | 9.008 | 20 | 20 | fits | 62,837 | 24 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 356,051 | 3.561 | 20 | 20 | fits | 116,578 | 169 | 0.462 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 297,452 | 2.975 | 20 | 200 | fits | 144,094 | 231 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 413,414 | 4.134 | 20 | 200 | fits | 116,578 | 169 | 0.462 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 298,376 | 2.984 | 20 | 20 | fits | 144,094 | 231 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 414,118 | 4.141 | 20 | 20 | fits | 116,578 | 169 | 0.462 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 150,663 | 1.507 | 20 | 24 | fits | 148,760 | 156 | 0.346 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 301,026 | 3.010 | 20 | 24 | fits | 144,094 | 231 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 300,960 | 3.010 | 20 | 50 | fits | 144,094 | 231 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 417,142 | 4.171 | 20 | 50 | fits | 116,578 | 169 | 0.462 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 507,120 | 5.071 | 20 | 20 | fits | 90,044 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 893,060 | 8.931 | 20 | 20 | fits | 52,093 | 20 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 355,692 | 3.557 | 20 | 20 | fits | 113,867 | 184 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 293,330 | 2.933 | 20 | 200 | fits | 144,991 | 209 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 406,581 | 4.066 | 20 | 200 | fits | 113,867 | 184 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 294,254 | 2.943 | 20 | 20 | fits | 144,991 | 209 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 407,285 | 4.073 | 20 | 20 | fits | 113,867 | 184 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 152,903 | 1.529 | 20 | 24 | fits | 148,603 | 155 | 0.344 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 296,904 | 2.969 | 20 | 24 | fits | 144,991 | 209 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 296,838 | 2.968 | 20 | 50 | fits | 144,991 | 209 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 410,309 | 4.103 | 20 | 50 | fits | 113,867 | 184 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 500,090 | 5.001 | 20 | 20 | fits | 89,847 | 28 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 901,463 | 9.015 | 20 | 20 | fits | 52,597 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 341,981 | 3.420 | 20 | 20 | fits | 108,435 | 163 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 292,338 | 2.923 | 20 | 200 | fits | 143,179 | 226 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 400,157 | 4.002 | 20 | 200 | fits | 108,435 | 163 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 293,262 | 2.933 | 20 | 20 | fits | 143,179 | 226 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 400,861 | 4.009 | 20 | 20 | fits | 108,435 | 163 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 153,723 | 1.537 | 20 | 24 | fits | 148,700 | 155 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 295,912 | 2.959 | 20 | 24 | fits | 143,179 | 226 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 295,846 | 2.958 | 20 | 50 | fits | 143,179 | 226 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 403,885 | 4.039 | 20 | 50 | fits | 108,435 | 163 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 493,369 | 4.934 | 20 | 20 | fits | 89,550 | 29 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 894,663 | 8.947 | 20 | 20 | fits | 52,147 | 20 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 358,560 | 3.586 | 20 | 20 | fits | 112,272 | 170 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 289,479 | 2.895 | 20 | 200 | fits | 143,656 | 227 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 409,616 | 4.096 | 20 | 200 | fits | 112,272 | 170 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 290,403 | 2.904 | 20 | 20 | fits | 143,656 | 227 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 410,320 | 4.103 | 20 | 20 | fits | 112,272 | 170 | 0.460 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 150,387 | 1.504 | 20 | 24 | fits | 148,796 | 155 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 293,053 | 2.931 | 20 | 24 | fits | 143,656 | 227 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 292,987 | 2.930 | 20 | 50 | fits | 143,656 | 227 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 413,344 | 4.133 | 20 | 50 | fits | 112,272 | 170 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 503,102 | 5.031 | 20 | 20 | fits | 89,824 | 28 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 896,542 | 8.965 | 20 | 20 | fits | 52,227 | 20 | 0.644 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 343,077 | 3.431 | 20 | 20 | fits | 102,086 | 142 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 298,761 | 2.988 | 20 | 200 | fits | 149,264 | 248 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 400,231 | 4.002 | 20 | 200 | fits | 102,086 | 142 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 299,685 | 2.997 | 20 | 20 | fits | 149,264 | 248 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 400,935 | 4.009 | 20 | 20 | fits | 102,086 | 142 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 154,061 | 1.541 | 20 | 24 | fits | 148,860 | 155 | 0.342 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 302,335 | 3.023 | 20 | 24 | fits | 149,264 | 248 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 302,269 | 3.023 | 20 | 50 | fits | 149,264 | 248 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 403,959 | 4.040 | 20 | 50 | fits | 102,086 | 142 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 488,699 | 4.887 | 20 | 20 | fits | 84,806 | 30 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 900,627 | 9.006 | 20 | 20 | fits | 68,228 | 31 | 0.672 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 340,503 | 3.405 | 20 | 20 | fits | 114,556 | 184 | 0.434 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 290,976 | 2.910 | 20 | 200 | fits | 145,024 | 209 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 404,916 | 4.049 | 20 | 200 | fits | 114,556 | 184 | 0.434 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 291,900 | 2.919 | 20 | 20 | fits | 145,024 | 209 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 405,620 | 4.056 | 20 | 20 | fits | 114,556 | 184 | 0.434 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 150,516 | 1.505 | 20 | 24 | fits | 148,647 | 155 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 294,550 | 2.946 | 20 | 24 | fits | 145,024 | 209 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 294,484 | 2.945 | 20 | 50 | fits | 145,024 | 209 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 408,644 | 4.086 | 20 | 50 | fits | 114,556 | 184 | 0.434 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 497,820 | 4.978 | 20 | 20 | fits | 89,242 | 28 | 0.714 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 899,526 | 8.995 | 20 | 20 | fits | 52,147 | 20 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 358,593 | 3.586 | 20 | 20 | fits | 111,899 | 170 | 0.459 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 296,854 | 2.969 | 20 | 200 | fits | 144,009 | 227 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 416,504 | 4.165 | 20 | 200 | fits | 111,899 | 170 | 0.459 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 297,778 | 2.978 | 20 | 20 | fits | 144,009 | 227 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 417,208 | 4.172 | 20 | 20 | fits | 111,899 | 170 | 0.459 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 157,409 | 1.574 | 20 | 24 | fits | 148,521 | 155 | 0.344 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 300,428 | 3.004 | 20 | 24 | fits | 144,009 | 227 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 300,362 | 3.004 | 20 | 50 | fits | 144,009 | 227 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 420,232 | 4.202 | 20 | 50 | fits | 111,899 | 170 | 0.459 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 509,990 | 5.100 | 20 | 20 | fits | 89,824 | 28 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 896,038 | 8.960 | 20 | 20 | fits | 52,149 | 20 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 350,786 | 3.508 | 20 | 20 | fits | 108,602 | 163 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 301,012 | 3.010 | 20 | 200 | fits | 144,388 | 231 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 408,998 | 4.090 | 20 | 200 | fits | 108,602 | 163 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 301,936 | 3.019 | 20 | 20 | fits | 144,388 | 231 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 409,702 | 4.097 | 20 | 20 | fits | 108,602 | 163 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 153,968 | 1.540 | 20 | 24 | fits | 148,565 | 156 | 0.344 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 304,586 | 3.046 | 20 | 24 | fits | 144,388 | 231 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 304,520 | 3.045 | 20 | 50 | fits | 144,388 | 231 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 412,726 | 4.127 | 20 | 50 | fits | 108,602 | 163 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 502,033 | 5.020 | 20 | 20 | fits | 89,373 | 28 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 895,200 | 8.952 | 20 | 20 | fits | 52,227 | 20 | 0.644 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 353,119 | 3.531 | 20 | 20 | fits | 108,290 | 163 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 296,055 | 2.961 | 20 | 200 | fits | 143,401 | 226 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 403,729 | 4.037 | 20 | 200 | fits | 108,290 | 163 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 296,979 | 2.970 | 20 | 20 | fits | 143,401 | 226 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 404,433 | 4.044 | 20 | 20 | fits | 108,290 | 163 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 157,218 | 1.572 | 20 | 24 | fits | 148,433 | 155 | 0.343 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 299,629 | 2.996 | 20 | 24 | fits | 143,401 | 226 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 299,563 | 2.996 | 20 | 50 | fits | 143,401 | 226 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 407,457 | 4.075 | 20 | 50 | fits | 108,290 | 163 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 492,268 | 4.923 | 20 | 20 | fits | 84,877 | 30 | 0.761 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 904,890 | 9.049 | 20 | 20 | fits | 62,986 | 24 | 0.589 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 342,739 | 3.427 | 20 | 20 | fits | 115,737 | 173 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 292,856 | 2.929 | 20 | 200 | fits | 143,538 | 224 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 407,977 | 4.080 | 20 | 200 | fits | 115,737 | 173 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 293,780 | 2.938 | 20 | 20 | fits | 143,538 | 224 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 408,681 | 4.087 | 20 | 20 | fits | 115,737 | 173 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 153,882 | 1.539 | 20 | 24 | fits | 148,529 | 155 | 0.344 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 296,430 | 2.964 | 20 | 24 | fits | 143,538 | 224 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 296,364 | 2.964 | 20 | 50 | fits | 143,538 | 224 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 411,705 | 4.117 | 20 | 50 | fits | 115,737 | 173 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 513,152 | 5.132 | 20 | 20 | fits | 92,901 | 35 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 899,604 | 8.996 | 20 | 20 | fits | 52,149 | 20 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 378,539 | 3.785 | 20 | 20 | fits | 108,435 | 163 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 328,896 | 3.289 | 20 | 200 | fits | 143,142 | 226 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 436,715 | 4.367 | 20 | 200 | fits | 108,435 | 163 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 329,820 | 3.298 | 20 | 20 | fits | 143,142 | 226 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 437,419 | 4.374 | 20 | 20 | fits | 108,435 | 163 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 190,318 | 1.903 | 20 | 24 | fits | 148,774 | 155 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 332,470 | 3.325 | 20 | 24 | fits | 143,142 | 226 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 332,404 | 3.324 | 20 | 50 | fits | 143,142 | 226 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 440,443 | 4.404 | 20 | 50 | fits | 108,435 | 163 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 530,070 | 5.301 | 20 | 20 | fits | 89,693 | 28 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 931,784 | 9.318 | 20 | 20 | fits | 52,637 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 341,016 | 3.410 | 20 | 20 | fits | 108,414 | 163 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 291,437 | 2.914 | 20 | 200 | fits | 143,427 | 226 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 399,235 | 3.992 | 20 | 200 | fits | 108,414 | 163 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 292,361 | 2.924 | 20 | 20 | fits | 143,427 | 226 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 399,939 | 3.999 | 20 | 20 | fits | 108,414 | 163 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 152,574 | 1.526 | 20 | 24 | fits | 148,656 | 155 | 0.346 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 295,011 | 2.950 | 20 | 24 | fits | 143,427 | 226 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 294,945 | 2.949 | 20 | 50 | fits | 143,427 | 226 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 402,963 | 4.030 | 20 | 50 | fits | 108,414 | 163 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 492,590 | 4.926 | 20 | 20 | fits | 89,693 | 28 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 901,014 | 9.010 | 20 | 20 | fits | 58,680 | 26 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 346,245 | 3.462 | 20 | 20 | fits | 108,311 | 163 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 296,602 | 2.966 | 20 | 200 | fits | 143,152 | 226 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 404,297 | 4.043 | 20 | 200 | fits | 108,311 | 163 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 297,526 | 2.975 | 20 | 20 | fits | 143,152 | 226 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 405,001 | 4.050 | 20 | 20 | fits | 108,311 | 163 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 158,014 | 1.580 | 20 | 24 | fits | 148,560 | 155 | 0.344 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 300,176 | 3.002 | 20 | 24 | fits | 143,152 | 226 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 300,110 | 3.001 | 20 | 50 | fits | 143,152 | 226 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 408,025 | 4.080 | 20 | 50 | fits | 108,311 | 163 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 497,761 | 4.978 | 20 | 20 | fits | 89,802 | 29 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 905,857 | 9.059 | 20 | 20 | fits | 52,227 | 20 | 0.644 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 337,889 | 3.379 | 20 | 20 | fits | 107,942 | 164 | 0.435 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 288,215 | 2.882 | 20 | 200 | fits | 143,733 | 226 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 395,541 | 3.955 | 20 | 200 | fits | 107,942 | 164 | 0.435 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 289,139 | 2.891 | 20 | 20 | fits | 143,733 | 226 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 396,245 | 3.962 | 20 | 20 | fits | 107,942 | 164 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 149,046 | 1.490 | 20 | 24 | fits | 148,560 | 155 | 0.344 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 291,789 | 2.918 | 20 | 24 | fits | 143,733 | 226 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 291,723 | 2.917 | 20 | 50 | fits | 143,733 | 226 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 399,269 | 3.993 | 20 | 50 | fits | 107,942 | 164 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 490,098 | 4.901 | 20 | 20 | fits | 82,531 | 31 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 894,217 | 8.942 | 20 | 20 | fits | 62,839 | 24 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 362,648 | 3.626 | 20 | 20 | fits | 112,193 | 170 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 293,760 | 2.938 | 20 | 200 | fits | 143,646 | 227 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 413,704 | 4.137 | 20 | 200 | fits | 112,193 | 170 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 294,684 | 2.947 | 20 | 20 | fits | 143,646 | 227 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 414,408 | 4.144 | 20 | 20 | fits | 112,193 | 170 | 0.460 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 154,678 | 1.547 | 20 | 24 | fits | 148,656 | 155 | 0.346 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 297,334 | 2.973 | 20 | 24 | fits | 143,646 | 227 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 297,268 | 2.973 | 20 | 50 | fits | 143,646 | 227 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 417,432 | 4.174 | 20 | 50 | fits | 112,193 | 170 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 502,760 | 5.028 | 20 | 20 | fits | 85,394 | 30 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 899,531 | 8.995 | 20 | 20 | fits | 62,837 | 24 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 365,379 | 3.654 | 20 | 20 | fits | 116,764 | 169 | 0.464 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 307,590 | 3.076 | 20 | 200 | fits | 144,643 | 231 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 423,738 | 4.237 | 20 | 200 | fits | 116,764 | 169 | 0.464 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 308,514 | 3.085 | 20 | 20 | fits | 144,643 | 231 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 424,442 | 4.244 | 20 | 20 | fits | 116,764 | 169 | 0.464 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 160,252 | 1.603 | 20 | 24 | fits | 148,694 | 156 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 311,164 | 3.112 | 20 | 24 | fits | 144,643 | 231 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 311,098 | 3.111 | 20 | 50 | fits | 144,643 | 231 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 427,466 | 4.275 | 20 | 50 | fits | 116,764 | 169 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 517,307 | 5.173 | 20 | 20 | fits | 89,907 | 28 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 903,487 | 9.035 | 20 | 20 | fits | 52,326 | 21 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 347,047 | 3.470 | 20 | 20 | fits | 115,452 | 172 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 297,164 | 2.972 | 20 | 200 | fits | 143,565 | 224 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 412,000 | 4.120 | 20 | 200 | fits | 115,452 | 172 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 298,088 | 2.981 | 20 | 20 | fits | 143,565 | 224 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 412,704 | 4.127 | 20 | 20 | fits | 115,452 | 172 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 158,163 | 1.582 | 20 | 24 | fits | 148,647 | 155 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 300,738 | 3.007 | 20 | 24 | fits | 143,565 | 224 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 300,672 | 3.007 | 20 | 50 | fits | 143,565 | 224 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 415,728 | 4.157 | 20 | 50 | fits | 115,452 | 172 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 505,267 | 5.053 | 20 | 20 | fits | 89,605 | 28 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 906,542 | 9.065 | 20 | 20 | fits | 57,693 | 27 | 0.720 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 351,940 | 3.519 | 20 | 20 | fits | 113,797 | 184 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 289,658 | 2.897 | 20 | 200 | fits | 145,027 | 209 | 0.404 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 402,839 | 4.028 | 20 | 200 | fits | 113,797 | 184 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 290,582 | 2.906 | 20 | 20 | fits | 145,027 | 209 | 0.404 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 403,543 | 4.035 | 20 | 20 | fits | 113,797 | 184 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 149,195 | 1.492 | 20 | 24 | fits | 148,647 | 155 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 293,232 | 2.932 | 20 | 24 | fits | 145,027 | 209 | 0.404 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 293,166 | 2.932 | 20 | 50 | fits | 145,027 | 209 | 0.404 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 406,567 | 4.066 | 20 | 50 | fits | 113,797 | 184 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 496,174 | 4.962 | 20 | 20 | fits | 89,673 | 28 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 898,139 | 8.981 | 20 | 20 | fits | 52,296 | 20 | 0.646 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 361,593 | 3.616 | 20 | 20 | fits | 112,578 | 172 | 0.452 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 290,374 | 2.904 | 20 | 200 | fits | 144,567 | 228 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 411,479 | 4.115 | 20 | 200 | fits | 112,578 | 172 | 0.452 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 291,298 | 2.913 | 20 | 20 | fits | 144,567 | 228 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 412,183 | 4.122 | 20 | 20 | fits | 112,578 | 172 | 0.452 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 150,371 | 1.504 | 20 | 24 | fits | 153,448 | 157 | 0.375 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 293,948 | 2.939 | 20 | 24 | fits | 144,567 | 228 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 293,882 | 2.939 | 20 | 50 | fits | 144,567 | 228 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 415,207 | 4.152 | 20 | 50 | fits | 112,578 | 172 | 0.452 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 504,826 | 5.048 | 20 | 20 | fits | 89,685 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 890,633 | 8.906 | 20 | 20 | fits | 52,109 | 20 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 360,948 | 3.609 | 20 | 20 | fits | 111,779 | 170 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 298,417 | 2.984 | 20 | 200 | fits | 143,991 | 227 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 418,723 | 4.187 | 20 | 200 | fits | 111,779 | 170 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 299,341 | 2.993 | 20 | 20 | fits | 143,991 | 227 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 419,427 | 4.194 | 20 | 20 | fits | 111,779 | 170 | 0.460 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 158,990 | 1.590 | 20 | 24 | fits | 148,725 | 152 | 0.343 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 301,991 | 3.020 | 20 | 24 | fits | 143,991 | 227 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 301,925 | 3.019 | 20 | 50 | fits | 143,991 | 227 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 422,451 | 4.225 | 20 | 50 | fits | 111,779 | 170 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 512,061 | 5.121 | 20 | 20 | fits | 89,676 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 904,843 | 9.048 | 20 | 20 | fits | 59,139 | 26 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 354,475 | 3.545 | 20 | 20 | fits | 108,397 | 163 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 304,805 | 3.048 | 20 | 200 | fits | 144,777 | 231 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 412,586 | 4.126 | 20 | 200 | fits | 108,397 | 163 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 305,729 | 3.057 | 20 | 20 | fits | 144,777 | 231 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 413,290 | 4.133 | 20 | 20 | fits | 108,397 | 163 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 156,108 | 1.561 | 20 | 24 | fits | 148,859 | 153 | 0.344 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 308,379 | 3.084 | 20 | 24 | fits | 144,777 | 231 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 308,313 | 3.083 | 20 | 50 | fits | 144,777 | 231 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 416,314 | 4.163 | 20 | 50 | fits | 108,397 | 163 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 505,194 | 5.052 | 20 | 20 | fits | 88,946 | 28 | 0.712 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 978,647 | 9.786 | 20 | 20 | fits | 56,468 | 28 | 0.660 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 341,437 | 3.414 | 20 | 20 | fits | 107,447 | 163 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 291,811 | 2.918 | 20 | 200 | fits | 143,711 | 226 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 398,642 | 3.986 | 20 | 200 | fits | 107,447 | 163 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 292,735 | 2.927 | 20 | 20 | fits | 143,711 | 226 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 399,346 | 3.993 | 20 | 20 | fits | 107,447 | 163 | 0.432 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 152,664 | 1.527 | 20 | 24 | fits | 148,240 | 152 | 0.339 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 295,385 | 2.954 | 20 | 24 | fits | 143,711 | 226 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 295,319 | 2.953 | 20 | 50 | fits | 143,711 | 226 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 402,370 | 4.024 | 20 | 50 | fits | 107,447 | 163 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 491,258 | 4.913 | 20 | 20 | fits | 88,954 | 28 | 0.713 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 976,094 | 9.761 | 20 | 20 | fits | 52,656 | 20 | 0.661 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 338,191 | 3.382 | 20 | 20 | fits | 108,204 | 163 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 288,652 | 2.887 | 20 | 200 | fits | 143,453 | 226 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 396,240 | 3.962 | 20 | 200 | fits | 108,204 | 163 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 289,576 | 2.896 | 20 | 20 | fits | 143,453 | 226 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 396,944 | 3.969 | 20 | 20 | fits | 108,204 | 163 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 149,763 | 1.498 | 20 | 24 | fits | 148,086 | 152 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 292,226 | 2.922 | 20 | 24 | fits | 143,453 | 226 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 292,160 | 2.922 | 20 | 50 | fits | 143,453 | 226 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 399,968 | 4.000 | 20 | 50 | fits | 108,204 | 163 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 488,813 | 4.888 | 20 | 20 | fits | 88,911 | 28 | 0.712 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 974,157 | 9.742 | 20 | 20 | fits | 52,125 | 20 | 0.644 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 335,925 | 3.359 | 20 | 20 | fits | 107,621 | 163 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 285,938 | 2.859 | 20 | 200 | fits | 144,498 | 231 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 392,943 | 3.929 | 20 | 200 | fits | 107,621 | 163 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 286,862 | 2.869 | 20 | 20 | fits | 144,498 | 231 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 393,647 | 3.936 | 20 | 20 | fits | 107,621 | 163 | 0.432 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 146,004 | 1.460 | 20 | 24 | fits | 148,086 | 152 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 289,512 | 2.895 | 20 | 24 | fits | 144,498 | 231 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 289,446 | 2.894 | 20 | 50 | fits | 144,498 | 231 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 396,671 | 3.967 | 20 | 50 | fits | 107,621 | 163 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 481,404 | 4.814 | 20 | 20 | fits | 84,799 | 30 | 0.761 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 970,731 | 9.707 | 20 | 20 | fits | 62,736 | 24 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 355,985 | 3.560 | 20 | 20 | fits | 116,094 | 170 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 298,133 | 2.981 | 20 | 200 | fits | 143,660 | 226 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 413,611 | 4.136 | 20 | 200 | fits | 116,094 | 170 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 299,057 | 2.991 | 20 | 20 | fits | 143,660 | 226 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 414,315 | 4.143 | 20 | 20 | fits | 116,094 | 170 | 0.460 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 159,037 | 1.590 | 20 | 24 | fits | 148,144 | 152 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 301,707 | 3.017 | 20 | 24 | fits | 143,660 | 226 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 301,641 | 3.016 | 20 | 50 | fits | 143,660 | 226 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 417,339 | 4.173 | 20 | 50 | fits | 116,094 | 170 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 594,145 | 5.941 | 20 | 20 | fits | 92,582 | 35 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 980,383 | 9.804 | 20 | 20 | fits | 52,109 | 20 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 434,563 | 4.346 | 20 | 20 | fits | 118,936 | 190 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 296,878 | 2.969 | 20 | 200 | fits | 145,421 | 210 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 499,310 | 4.993 | 20 | 200 | fits | 118,936 | 190 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 297,802 | 2.978 | 20 | 20 | fits | 145,421 | 210 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 500,014 | 5.000 | 20 | 20 | fits | 118,936 | 190 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 156,021 | 1.560 | 20 | 24 | fits | 148,144 | 152 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 300,452 | 3.005 | 20 | 24 | fits | 145,421 | 210 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 300,386 | 3.004 | 20 | 50 | fits | 145,421 | 210 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 503,038 | 5.030 | 20 | 50 | fits | 118,936 | 190 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 592,743 | 5.927 | 20 | 20 | fits | 89,771 | 28 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 978,495 | 9.785 | 20 | 20 | fits | 52,109 | 20 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 339,299 | 3.393 | 20 | 20 | fits | 108,458 | 163 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 289,640 | 2.896 | 20 | 200 | fits | 143,352 | 226 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 397,482 | 3.975 | 20 | 200 | fits | 108,458 | 163 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 290,564 | 2.906 | 20 | 20 | fits | 143,352 | 226 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 398,186 | 3.982 | 20 | 20 | fits | 108,458 | 163 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 150,852 | 1.509 | 20 | 24 | fits | 147,957 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 293,214 | 2.932 | 20 | 24 | fits | 143,352 | 226 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 293,148 | 2.931 | 20 | 50 | fits | 143,352 | 226 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 401,210 | 4.012 | 20 | 50 | fits | 108,458 | 163 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 490,880 | 4.909 | 20 | 20 | fits | 89,736 | 28 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 892,224 | 8.922 | 20 | 20 | fits | 52,107 | 20 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 337,205 | 3.372 | 20 | 20 | fits | 102,156 | 142 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 292,809 | 2.928 | 20 | 200 | fits | 149,409 | 248 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 394,349 | 3.943 | 20 | 200 | fits | 102,156 | 142 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 293,733 | 2.937 | 20 | 20 | fits | 149,409 | 248 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 395,053 | 3.951 | 20 | 20 | fits | 102,156 | 142 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 147,964 | 1.480 | 20 | 24 | fits | 147,957 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 296,383 | 2.964 | 20 | 24 | fits | 149,409 | 248 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 296,317 | 2.963 | 20 | 50 | fits | 149,409 | 248 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 398,077 | 3.981 | 20 | 50 | fits | 102,156 | 142 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 488,016 | 4.880 | 20 | 20 | fits | 90,005 | 29 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 904,311 | 9.043 | 20 | 20 | fits | 67,420 | 26 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 347,077 | 3.471 | 20 | 20 | fits | 112,638 | 170 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 285,486 | 2.855 | 20 | 200 | fits | 144,974 | 231 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 397,508 | 3.975 | 20 | 200 | fits | 112,638 | 170 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 286,410 | 2.864 | 20 | 20 | fits | 144,974 | 231 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 398,212 | 3.982 | 20 | 20 | fits | 112,638 | 170 | 0.451 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 145,076 | 1.451 | 20 | 24 | fits | 147,957 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 289,060 | 2.891 | 20 | 24 | fits | 144,974 | 231 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 288,994 | 2.890 | 20 | 50 | fits | 144,974 | 231 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 401,236 | 4.012 | 20 | 50 | fits | 112,638 | 170 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 500,052 | 5.001 | 20 | 20 | fits | 90,177 | 29 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 947,000 | 9.470 | 20 | 20 | fits | 65,659 | 25 | 0.676 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 357,264 | 3.573 | 20 | 20 | fits | 108,993 | 163 | 0.447 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 298,729 | 2.987 | 20 | 200 | fits | 145,783 | 232 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 415,606 | 4.156 | 20 | 200 | fits | 108,993 | 163 | 0.447 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 299,653 | 2.997 | 20 | 20 | fits | 145,783 | 232 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 416,310 | 4.163 | 20 | 20 | fits | 108,993 | 163 | 0.447 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 157,510 | 1.575 | 20 | 24 | fits | 148,015 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 302,303 | 3.023 | 20 | 24 | fits | 145,783 | 232 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 302,237 | 3.022 | 20 | 50 | fits | 145,783 | 232 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 419,334 | 4.193 | 20 | 50 | fits | 108,993 | 163 | 0.447 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 509,240 | 5.092 | 20 | 20 | fits | 89,972 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 987,190 | 9.872 | 20 | 20 | fits | 63,467 | 24 | 0.611 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 351,622 | 3.516 | 20 | 20 | fits | 107,858 | 163 | 0.434 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 301,424 | 3.014 | 20 | 200 | fits | 144,112 | 231 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 408,666 | 4.087 | 20 | 200 | fits | 107,858 | 163 | 0.434 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 302,348 | 3.023 | 20 | 20 | fits | 144,112 | 231 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 409,370 | 4.094 | 20 | 20 | fits | 107,858 | 163 | 0.434 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 154,642 | 1.546 | 20 | 24 | fits | 148,035 | 153 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 304,998 | 3.050 | 20 | 24 | fits | 144,112 | 231 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 304,932 | 3.049 | 20 | 50 | fits | 144,112 | 231 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 412,394 | 4.124 | 20 | 50 | fits | 107,858 | 163 | 0.434 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 502,182 | 5.022 | 20 | 20 | fits | 89,854 | 28 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 980,348 | 9.803 | 20 | 20 | fits | 63,039 | 25 | 0.588 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 338,925 | 3.389 | 20 | 20 | fits | 108,274 | 163 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 289,306 | 2.893 | 20 | 200 | fits | 143,137 | 226 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 396,964 | 3.970 | 20 | 200 | fits | 108,274 | 163 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 290,230 | 2.902 | 20 | 20 | fits | 143,137 | 226 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 397,668 | 3.977 | 20 | 20 | fits | 108,274 | 163 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 150,733 | 1.507 | 20 | 24 | fits | 147,986 | 152 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 292,880 | 2.929 | 20 | 24 | fits | 143,137 | 226 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 292,814 | 2.928 | 20 | 50 | fits | 143,137 | 226 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 400,692 | 4.007 | 20 | 50 | fits | 108,274 | 163 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 484,002 | 4.840 | 20 | 20 | fits | 83,376 | 26 | 0.809 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 983,545 | 9.835 | 20 | 20 | fits | 73,620 | 28 | 0.541 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 354,966 | 3.550 | 20 | 20 | fits | 129,212 | 169 | 0.494 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 285,522 | 2.855 | 20 | 200 | fits | 144,182 | 231 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 414,118 | 4.141 | 20 | 200 | fits | 129,212 | 169 | 0.494 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 286,446 | 2.864 | 20 | 20 | fits | 144,182 | 231 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 414,822 | 4.148 | 20 | 20 | fits | 129,212 | 169 | 0.494 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 145,904 | 1.459 | 20 | 24 | fits | 147,986 | 152 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 289,096 | 2.891 | 20 | 24 | fits | 144,182 | 231 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 289,030 | 2.890 | 20 | 50 | fits | 144,182 | 231 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 417,846 | 4.178 | 20 | 50 | fits | 129,212 | 169 | 0.494 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 549,224 | 5.492 | 20 | 20 | fits | 89,617 | 29 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 982,332 | 9.823 | 20 | 20 | fits | 52,107 | 20 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 361,097 | 3.611 | 20 | 20 | fits | 129,363 | 169 | 0.495 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 284,887 | 2.849 | 20 | 200 | fits | 144,750 | 231 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 413,634 | 4.136 | 20 | 200 | fits | 129,363 | 169 | 0.495 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 285,811 | 2.858 | 20 | 20 | fits | 144,750 | 231 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 414,338 | 4.143 | 20 | 20 | fits | 129,363 | 169 | 0.495 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 144,701 | 1.447 | 20 | 24 | fits | 147,986 | 152 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 288,461 | 2.885 | 20 | 24 | fits | 144,750 | 231 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 288,395 | 2.884 | 20 | 50 | fits | 144,750 | 231 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 417,362 | 4.174 | 20 | 50 | fits | 129,363 | 169 | 0.495 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 548,896 | 5.489 | 20 | 20 | fits | 89,773 | 30 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 980,246 | 9.802 | 20 | 20 | fits | 52,107 | 20 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 346,405 | 3.464 | 20 | 20 | fits | 111,094 | 169 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 293,562 | 2.936 | 20 | 200 | fits | 144,703 | 231 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 404,040 | 4.040 | 20 | 200 | fits | 111,094 | 169 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 294,486 | 2.945 | 20 | 20 | fits | 144,703 | 231 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 404,744 | 4.047 | 20 | 20 | fits | 111,094 | 169 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 146,173 | 1.462 | 20 | 24 | fits | 148,263 | 153 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 297,136 | 2.971 | 20 | 24 | fits | 144,703 | 231 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 297,070 | 2.971 | 20 | 50 | fits | 144,703 | 231 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 407,768 | 4.078 | 20 | 50 | fits | 111,094 | 169 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 497,569 | 4.976 | 20 | 20 | fits | 89,867 | 28 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 883,617 | 8.836 | 20 | 20 | fits | 52,149 | 20 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 344,216 | 3.442 | 20 | 20 | fits | 111,851 | 169 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 291,468 | 2.915 | 20 | 200 | fits | 144,343 | 231 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 402,703 | 4.027 | 20 | 200 | fits | 111,851 | 169 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 292,392 | 2.924 | 20 | 20 | fits | 144,343 | 231 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 403,407 | 4.034 | 20 | 20 | fits | 111,851 | 169 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 144,439 | 1.444 | 20 | 24 | fits | 148,197 | 153 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 295,042 | 2.950 | 20 | 24 | fits | 144,343 | 231 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 294,976 | 2.950 | 20 | 50 | fits | 144,343 | 231 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 406,431 | 4.064 | 20 | 50 | fits | 111,851 | 169 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 496,189 | 4.962 | 20 | 20 | fits | 89,824 | 28 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 889,423 | 8.894 | 20 | 20 | fits | 59,335 | 26 | 0.694 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 345,061 | 3.451 | 20 | 20 | fits | 102,112 | 142 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 300,745 | 3.007 | 20 | 200 | fits | 149,190 | 248 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 402,241 | 4.022 | 20 | 200 | fits | 102,112 | 142 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 301,669 | 3.017 | 20 | 20 | fits | 149,190 | 248 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 402,945 | 4.029 | 20 | 20 | fits | 102,112 | 142 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 156,119 | 1.561 | 20 | 24 | fits | 148,155 | 152 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 304,319 | 3.043 | 20 | 24 | fits | 149,190 | 248 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 304,253 | 3.043 | 20 | 50 | fits | 149,190 | 248 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 405,969 | 4.060 | 20 | 50 | fits | 102,112 | 142 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 495,188 | 4.952 | 20 | 20 | fits | 89,285 | 28 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 982,761 | 9.828 | 20 | 20 | fits | 63,537 | 25 | 0.606 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 349,007 | 3.490 | 20 | 20 | fits | 108,316 | 163 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 291,943 | 2.919 | 20 | 200 | fits | 143,276 | 226 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 399,643 | 3.996 | 20 | 200 | fits | 108,316 | 163 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 292,867 | 2.929 | 20 | 20 | fits | 143,276 | 226 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 400,347 | 4.003 | 20 | 20 | fits | 108,316 | 163 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 153,231 | 1.532 | 20 | 24 | fits | 148,155 | 152 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 295,517 | 2.955 | 20 | 24 | fits | 143,276 | 226 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 295,451 | 2.955 | 20 | 50 | fits | 143,276 | 226 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 403,371 | 4.034 | 20 | 50 | fits | 108,316 | 163 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 492,590 | 4.926 | 20 | 20 | fits | 89,285 | 28 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 980,735 | 9.807 | 20 | 20 | fits | 62,898 | 24 | 0.586 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 339,757 | 3.398 | 20 | 20 | fits | 102,907 | 142 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 295,295 | 2.953 | 20 | 200 | fits | 149,516 | 248 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 397,586 | 3.976 | 20 | 200 | fits | 102,907 | 142 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 296,219 | 2.962 | 20 | 20 | fits | 149,516 | 248 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 398,290 | 3.983 | 20 | 20 | fits | 102,907 | 142 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 150,343 | 1.503 | 20 | 24 | fits | 148,155 | 152 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 298,869 | 2.989 | 20 | 24 | fits | 149,516 | 248 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 298,803 | 2.988 | 20 | 50 | fits | 149,516 | 248 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 401,314 | 4.013 | 20 | 50 | fits | 102,907 | 142 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 490,667 | 4.907 | 20 | 20 | fits | 89,419 | 29 | 0.714 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 978,467 | 9.785 | 20 | 20 | fits | 62,837 | 24 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 343,813 | 3.438 | 20 | 20 | fits | 108,966 | 167 | 0.428 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 285,269 | 2.853 | 20 | 200 | fits | 143,768 | 227 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 393,619 | 3.936 | 20 | 200 | fits | 108,966 | 167 | 0.428 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 286,193 | 2.862 | 20 | 20 | fits | 143,768 | 227 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 394,323 | 3.943 | 20 | 20 | fits | 108,966 | 167 | 0.428 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 146,065 | 1.461 | 20 | 24 | fits | 148,155 | 152 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 288,843 | 2.888 | 20 | 24 | fits | 143,768 | 227 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 288,777 | 2.888 | 20 | 50 | fits | 143,768 | 227 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 397,347 | 3.973 | 20 | 50 | fits | 108,966 | 167 | 0.428 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 492,685 | 4.927 | 20 | 20 | fits | 86,984 | 37 | 0.753 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 970,440 | 9.704 | 20 | 20 | fits | 62,839 | 24 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 353,729 | 3.537 | 20 | 20 | fits | 119,424 | 175 | 0.470 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 285,009 | 2.850 | 20 | 200 | fits | 145,006 | 232 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 412,240 | 4.122 | 20 | 200 | fits | 119,424 | 175 | 0.470 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 285,933 | 2.859 | 20 | 20 | fits | 145,006 | 232 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 412,944 | 4.129 | 20 | 20 | fits | 119,424 | 175 | 0.470 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 144,567 | 1.446 | 20 | 24 | fits | 148,155 | 152 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 288,583 | 2.886 | 20 | 24 | fits | 145,006 | 232 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 288,517 | 2.885 | 20 | 50 | fits | 145,006 | 232 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 415,968 | 4.160 | 20 | 50 | fits | 119,424 | 175 | 0.470 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 585,605 | 5.856 | 20 | 20 | fits | 89,575 | 29 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 972,214 | 9.722 | 20 | 20 | fits | 52,149 | 20 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 441,461 | 4.415 | 20 | 20 | fits | 110,861 | 169 | 0.445 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 309,628 | 3.096 | 20 | 200 | fits | 150,087 | 231 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 499,857 | 4.999 | 20 | 200 | fits | 110,861 | 169 | 0.445 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 310,552 | 3.106 | 20 | 20 | fits | 150,087 | 231 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 500,561 | 5.006 | 20 | 20 | fits | 110,861 | 169 | 0.445 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 157,001 | 1.570 | 20 | 24 | fits | 148,213 | 153 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 313,202 | 3.132 | 20 | 24 | fits | 150,087 | 231 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 313,136 | 3.131 | 20 | 50 | fits | 150,087 | 231 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 503,585 | 5.036 | 20 | 50 | fits | 110,861 | 169 | 0.445 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 593,323 | 5.933 | 20 | 20 | fits | 89,804 | 28 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 994,835 | 9.948 | 20 | 20 | fits | 57,688 | 27 | 0.721 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 340,347 | 3.403 | 20 | 20 | fits | 102,397 | 143 | 0.445 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 296,031 | 2.960 | 20 | 200 | fits | 149,320 | 248 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 397,812 | 3.978 | 20 | 200 | fits | 102,397 | 143 | 0.445 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 296,955 | 2.970 | 20 | 20 | fits | 149,320 | 248 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 398,516 | 3.985 | 20 | 20 | fits | 102,397 | 143 | 0.445 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 151,275 | 1.513 | 20 | 24 | fits | 148,155 | 152 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 299,605 | 2.996 | 20 | 24 | fits | 149,320 | 248 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 299,539 | 2.995 | 20 | 50 | fits | 149,320 | 248 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 401,540 | 4.015 | 20 | 50 | fits | 102,397 | 143 | 0.445 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 503,035 | 5.030 | 20 | 20 | fits | 92,901 | 35 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 889,487 | 8.895 | 20 | 20 | fits | 52,149 | 20 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 356,644 | 3.566 | 20 | 20 | fits | 112,336 | 170 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 287,418 | 2.874 | 20 | 200 | fits | 143,595 | 227 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 407,700 | 4.077 | 20 | 200 | fits | 112,336 | 170 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 288,342 | 2.883 | 20 | 20 | fits | 143,595 | 227 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 408,404 | 4.084 | 20 | 20 | fits | 112,336 | 170 | 0.461 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 148,387 | 1.484 | 20 | 24 | fits | 148,155 | 152 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 290,992 | 2.910 | 20 | 24 | fits | 143,595 | 227 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 290,926 | 2.909 | 20 | 50 | fits | 143,595 | 227 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 411,428 | 4.114 | 20 | 50 | fits | 112,336 | 170 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 501,186 | 5.012 | 20 | 20 | fits | 89,824 | 28 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 894,420 | 8.944 | 20 | 20 | fits | 59,335 | 26 | 0.694 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 345,251 | 3.453 | 20 | 20 | fits | 111,872 | 169 | 0.454 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 292,439 | 2.924 | 20 | 200 | fits | 144,114 | 231 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 403,695 | 4.037 | 20 | 200 | fits | 111,872 | 169 | 0.454 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 293,363 | 2.934 | 20 | 20 | fits | 144,114 | 231 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 404,399 | 4.044 | 20 | 20 | fits | 111,872 | 169 | 0.454 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 145,639 | 1.456 | 20 | 24 | fits | 148,295 | 153 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 296,013 | 2.960 | 20 | 24 | fits | 144,114 | 231 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 295,947 | 2.959 | 20 | 50 | fits | 144,114 | 231 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 407,423 | 4.074 | 20 | 50 | fits | 111,872 | 169 | 0.454 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 497,181 | 4.972 | 20 | 20 | fits | 89,824 | 28 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 890,466 | 8.905 | 20 | 20 | fits | 52,332 | 20 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 346,062 | 3.461 | 20 | 20 | fits | 107,631 | 163 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 296,388 | 2.964 | 20 | 200 | fits | 143,653 | 226 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 403,403 | 4.034 | 20 | 200 | fits | 107,631 | 163 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 297,312 | 2.973 | 20 | 20 | fits | 143,653 | 226 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 404,107 | 4.041 | 20 | 20 | fits | 107,631 | 163 | 0.432 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 157,299 | 1.573 | 20 | 24 | fits | 148,159 | 152 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 299,962 | 3.000 | 20 | 24 | fits | 143,653 | 226 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 299,896 | 2.999 | 20 | 50 | fits | 143,653 | 226 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 407,131 | 4.071 | 20 | 50 | fits | 107,631 | 163 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 496,418 | 4.964 | 20 | 20 | fits | 89,353 | 28 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 904,586 | 9.046 | 20 | 20 | fits | 57,412 | 27 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 342,834 | 3.428 | 20 | 20 | fits | 108,388 | 163 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 293,255 | 2.933 | 20 | 200 | fits | 143,293 | 226 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 401,027 | 4.010 | 20 | 200 | fits | 108,388 | 163 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 294,179 | 2.942 | 20 | 20 | fits | 143,293 | 226 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 401,731 | 4.017 | 20 | 20 | fits | 108,388 | 163 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 154,526 | 1.545 | 20 | 24 | fits | 148,088 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 296,829 | 2.968 | 20 | 24 | fits | 143,293 | 226 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 296,763 | 2.968 | 20 | 50 | fits | 143,293 | 226 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 404,755 | 4.048 | 20 | 50 | fits | 108,388 | 163 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 493,999 | 4.940 | 20 | 20 | fits | 89,310 | 28 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 902,531 | 9.025 | 20 | 20 | fits | 52,296 | 20 | 0.646 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 340,740 | 3.407 | 20 | 20 | fits | 102,086 | 142 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 296,424 | 2.964 | 20 | 200 | fits | 149,350 | 248 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 397,894 | 3.979 | 20 | 200 | fits | 102,086 | 142 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 297,348 | 2.973 | 20 | 20 | fits | 149,350 | 248 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 398,598 | 3.986 | 20 | 20 | fits | 102,086 | 142 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 151,638 | 1.516 | 20 | 24 | fits | 148,088 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 299,998 | 3.000 | 20 | 24 | fits | 149,350 | 248 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 299,932 | 2.999 | 20 | 50 | fits | 149,350 | 248 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 401,622 | 4.016 | 20 | 50 | fits | 102,086 | 142 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 486,430 | 4.864 | 20 | 20 | fits | 84,874 | 30 | 0.761 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 898,795 | 8.988 | 20 | 20 | fits | 62,837 | 24 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 352,499 | 3.525 | 20 | 20 | fits | 116,558 | 170 | 0.462 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 287,509 | 2.875 | 20 | 200 | fits | 143,323 | 226 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 403,451 | 4.035 | 20 | 200 | fits | 116,558 | 170 | 0.462 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 288,433 | 2.884 | 20 | 20 | fits | 143,323 | 226 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 404,155 | 4.042 | 20 | 20 | fits | 116,558 | 170 | 0.462 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 148,750 | 1.488 | 20 | 24 | fits | 148,088 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 291,083 | 2.911 | 20 | 24 | fits | 143,323 | 226 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 291,017 | 2.910 | 20 | 50 | fits | 143,323 | 226 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 407,179 | 4.072 | 20 | 50 | fits | 116,558 | 170 | 0.462 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 508,545 | 5.085 | 20 | 20 | fits | 92,626 | 35 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 895,079 | 8.951 | 20 | 20 | fits | 52,149 | 20 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 354,966 | 3.550 | 20 | 20 | fits | 119,627 | 175 | 0.472 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 286,116 | 2.861 | 20 | 200 | fits | 144,818 | 232 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 413,482 | 4.135 | 20 | 200 | fits | 119,627 | 175 | 0.472 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 287,040 | 2.870 | 20 | 20 | fits | 144,818 | 232 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 414,186 | 4.142 | 20 | 20 | fits | 119,627 | 175 | 0.472 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 145,862 | 1.459 | 20 | 24 | fits | 148,088 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 289,690 | 2.897 | 20 | 24 | fits | 144,818 | 232 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 289,624 | 2.896 | 20 | 50 | fits | 144,818 | 232 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 417,210 | 4.172 | 20 | 50 | fits | 119,627 | 175 | 0.472 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 506,819 | 5.068 | 20 | 20 | fits | 89,675 | 28 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 892,867 | 8.929 | 20 | 20 | fits | 52,149 | 20 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 337,392 | 3.374 | 20 | 20 | fits | 107,631 | 163 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 287,718 | 2.877 | 20 | 200 | fits | 143,639 | 226 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 394,733 | 3.947 | 20 | 200 | fits | 107,631 | 163 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 288,642 | 2.886 | 20 | 20 | fits | 143,639 | 226 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 395,437 | 3.954 | 20 | 20 | fits | 107,631 | 163 | 0.432 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 148,643 | 1.486 | 20 | 24 | fits | 148,349 | 152 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 291,292 | 2.913 | 20 | 24 | fits | 143,639 | 226 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 291,226 | 2.912 | 20 | 50 | fits | 143,639 | 226 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 398,461 | 3.985 | 20 | 50 | fits | 107,631 | 163 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 488,000 | 4.880 | 20 | 20 | fits | 89,605 | 28 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 890,548 | 8.905 | 20 | 20 | fits | 54,011 | 21 | 0.702 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 335,632 | 3.356 | 20 | 20 | fits | 108,388 | 163 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 286,053 | 2.861 | 20 | 200 | fits | 144,862 | 231 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 393,825 | 3.938 | 20 | 200 | fits | 108,388 | 163 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 286,977 | 2.870 | 20 | 20 | fits | 144,862 | 231 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 394,529 | 3.945 | 20 | 20 | fits | 108,388 | 163 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 145,755 | 1.458 | 20 | 24 | fits | 148,349 | 152 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 289,627 | 2.896 | 20 | 24 | fits | 144,862 | 231 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 289,561 | 2.896 | 20 | 50 | fits | 144,862 | 231 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 397,553 | 3.976 | 20 | 50 | fits | 108,388 | 163 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 487,049 | 4.870 | 20 | 20 | fits | 89,562 | 28 | 0.714 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 895,398 | 8.954 | 20 | 20 | fits | 58,680 | 26 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 347,525 | 3.475 | 20 | 20 | fits | 103,005 | 142 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 303,063 | 3.031 | 20 | 200 | fits | 149,554 | 248 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 405,452 | 4.055 | 20 | 200 | fits | 103,005 | 142 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 303,987 | 3.040 | 20 | 20 | fits | 149,554 | 248 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 406,156 | 4.062 | 20 | 20 | fits | 103,005 | 142 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 158,073 | 1.581 | 20 | 24 | fits | 148,291 | 152 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 306,637 | 3.066 | 20 | 24 | fits | 149,554 | 248 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 306,571 | 3.066 | 20 | 50 | fits | 149,554 | 248 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 409,180 | 4.092 | 20 | 50 | fits | 103,005 | 142 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 498,921 | 4.989 | 20 | 20 | fits | 89,807 | 29 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 983,915 | 9.839 | 20 | 20 | fits | 52,233 | 21 | 0.644 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 343,985 | 3.440 | 20 | 20 | fits | 107,916 | 164 | 0.434 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 294,311 | 2.943 | 20 | 200 | fits | 143,690 | 226 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 401,611 | 4.016 | 20 | 200 | fits | 107,916 | 164 | 0.434 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 295,235 | 2.952 | 20 | 20 | fits | 143,690 | 226 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 402,315 | 4.023 | 20 | 20 | fits | 107,916 | 164 | 0.434 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 155,185 | 1.552 | 20 | 24 | fits | 148,291 | 152 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 297,885 | 2.979 | 20 | 24 | fits | 143,690 | 226 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 297,819 | 2.978 | 20 | 50 | fits | 143,690 | 226 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 405,339 | 4.053 | 20 | 50 | fits | 107,916 | 164 | 0.434 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 496,244 | 4.962 | 20 | 20 | fits | 82,531 | 31 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 977,605 | 9.776 | 20 | 20 | fits | 62,839 | 24 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 352,695 | 3.527 | 20 | 20 | fits | 112,312 | 170 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 291,263 | 2.913 | 20 | 200 | fits | 143,530 | 227 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 411,334 | 4.113 | 20 | 200 | fits | 112,312 | 170 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 292,187 | 2.922 | 20 | 20 | fits | 143,530 | 227 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 412,038 | 4.120 | 20 | 20 | fits | 112,312 | 170 | 0.460 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 152,297 | 1.523 | 20 | 24 | fits | 148,291 | 152 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 294,837 | 2.948 | 20 | 24 | fits | 143,530 | 227 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 294,771 | 2.948 | 20 | 50 | fits | 143,530 | 227 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 415,062 | 4.151 | 20 | 50 | fits | 112,312 | 170 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 505,183 | 5.052 | 20 | 20 | fits | 90,187 | 28 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 975,402 | 9.754 | 20 | 20 | fits | 52,149 | 20 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 346,391 | 3.464 | 20 | 20 | fits | 107,998 | 163 | 0.434 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 296,225 | 2.962 | 20 | 200 | fits | 144,113 | 231 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 403,607 | 4.036 | 20 | 200 | fits | 107,998 | 163 | 0.434 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 297,149 | 2.971 | 20 | 20 | fits | 144,113 | 231 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 404,311 | 4.043 | 20 | 20 | fits | 107,998 | 163 | 0.434 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 149,572 | 1.496 | 20 | 24 | fits | 148,454 | 153 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 299,799 | 2.998 | 20 | 24 | fits | 144,113 | 231 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 299,733 | 2.997 | 20 | 50 | fits | 144,113 | 231 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 407,335 | 4.073 | 20 | 50 | fits | 107,998 | 163 | 0.434 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 492,534 | 4.925 | 20 | 20 | fits | 85,265 | 30 | 0.761 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 966,672 | 9.667 | 20 | 20 | fits | 63,014 | 25 | 0.586 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 351,505 | 3.515 | 20 | 20 | fits | 118,351 | 175 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 284,563 | 2.846 | 20 | 200 | fits | 144,982 | 231 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 402,298 | 4.023 | 20 | 200 | fits | 118,351 | 175 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 285,487 | 2.855 | 20 | 20 | fits | 144,982 | 231 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 403,002 | 4.030 | 20 | 20 | fits | 118,351 | 175 | 0.460 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 144,145 | 1.441 | 20 | 24 | fits | 149,406 | 157 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 288,137 | 2.881 | 20 | 24 | fits | 144,982 | 231 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 288,071 | 2.881 | 20 | 50 | fits | 144,982 | 231 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 406,026 | 4.060 | 20 | 50 | fits | 118,351 | 175 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 572,900 | 5.729 | 20 | 20 | fits | 89,655 | 29 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 974,872 | 9.749 | 20 | 20 | fits | 52,637 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 422,833 | 4.228 | 20 | 20 | fits | 116,114 | 172 | 0.434 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 296,452 | 2.965 | 20 | 200 | fits | 143,675 | 224 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 488,866 | 4.889 | 20 | 200 | fits | 116,114 | 172 | 0.434 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 297,376 | 2.974 | 20 | 20 | fits | 143,675 | 224 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 489,570 | 4.896 | 20 | 20 | fits | 116,114 | 172 | 0.434 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 157,341 | 1.573 | 20 | 24 | fits | 148,358 | 152 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 300,026 | 3.000 | 20 | 24 | fits | 143,675 | 224 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 299,960 | 3.000 | 20 | 50 | fits | 143,675 | 224 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 492,594 | 4.926 | 20 | 50 | fits | 116,114 | 172 | 0.434 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 582,055 | 5.821 | 20 | 20 | fits | 89,527 | 28 | 0.713 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 984,915 | 9.849 | 20 | 20 | fits | 52,165 | 20 | 0.644 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 349,980 | 3.500 | 20 | 20 | fits | 108,602 | 163 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 300,206 | 3.002 | 20 | 200 | fits | 144,280 | 231 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 408,192 | 4.082 | 20 | 200 | fits | 108,602 | 163 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 301,130 | 3.011 | 20 | 20 | fits | 144,280 | 231 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 408,896 | 4.089 | 20 | 20 | fits | 108,602 | 163 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 153,240 | 1.532 | 20 | 24 | fits | 148,524 | 153 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 303,780 | 3.038 | 20 | 24 | fits | 144,280 | 231 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 303,714 | 3.037 | 20 | 50 | fits | 144,280 | 231 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 411,920 | 4.119 | 20 | 50 | fits | 108,602 | 163 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 501,479 | 5.015 | 20 | 20 | fits | 89,625 | 28 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 887,317 | 8.873 | 20 | 20 | fits | 52,149 | 20 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 355,219 | 3.552 | 20 | 20 | fits | 108,848 | 166 | 0.427 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 296,544 | 2.965 | 20 | 200 | fits | 143,572 | 227 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 404,776 | 4.048 | 20 | 200 | fits | 108,848 | 166 | 0.427 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 297,468 | 2.975 | 20 | 20 | fits | 143,572 | 227 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 405,480 | 4.055 | 20 | 20 | fits | 108,848 | 166 | 0.427 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 150,286 | 1.503 | 20 | 24 | fits | 148,458 | 153 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 300,118 | 3.001 | 20 | 24 | fits | 143,572 | 227 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 300,052 | 3.001 | 20 | 50 | fits | 143,572 | 227 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 408,504 | 4.085 | 20 | 50 | fits | 108,848 | 166 | 0.427 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 498,038 | 4.980 | 20 | 20 | fits | 89,600 | 28 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 890,999 | 8.910 | 20 | 20 | fits | 59,272 | 26 | 0.692 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 335,931 | 3.359 | 20 | 20 | fits | 108,311 | 163 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 286,288 | 2.863 | 20 | 200 | fits | 144,642 | 231 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 393,983 | 3.940 | 20 | 200 | fits | 108,311 | 163 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 287,212 | 2.872 | 20 | 20 | fits | 144,642 | 231 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 394,687 | 3.947 | 20 | 20 | fits | 108,311 | 163 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 146,210 | 1.462 | 20 | 24 | fits | 148,300 | 152 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 289,862 | 2.899 | 20 | 24 | fits | 144,642 | 231 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 289,796 | 2.898 | 20 | 50 | fits | 144,642 | 231 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 397,711 | 3.977 | 20 | 50 | fits | 108,311 | 163 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 487,275 | 4.873 | 20 | 20 | fits | 89,630 | 28 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 894,423 | 8.944 | 20 | 20 | fits | 63,327 | 24 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 348,336 | 3.483 | 20 | 20 | fits | 102,112 | 142 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 304,020 | 3.040 | 20 | 200 | fits | 149,227 | 248 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 405,516 | 4.055 | 20 | 200 | fits | 102,112 | 142 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 304,944 | 3.049 | 20 | 20 | fits | 149,227 | 248 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 406,220 | 4.062 | 20 | 20 | fits | 102,112 | 142 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 159,357 | 1.594 | 20 | 24 | fits | 148,358 | 152 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 307,594 | 3.076 | 20 | 24 | fits | 149,227 | 248 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 307,528 | 3.075 | 20 | 50 | fits | 149,227 | 248 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 409,244 | 4.092 | 20 | 50 | fits | 102,112 | 142 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 498,783 | 4.988 | 20 | 20 | fits | 89,605 | 28 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 905,998 | 9.060 | 20 | 20 | fits | 62,837 | 24 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 352,282 | 3.523 | 20 | 20 | fits | 108,316 | 163 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 295,218 | 2.952 | 20 | 200 | fits | 143,313 | 226 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 402,918 | 4.029 | 20 | 200 | fits | 108,316 | 163 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 296,142 | 2.961 | 20 | 20 | fits | 143,313 | 226 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 403,622 | 4.036 | 20 | 20 | fits | 108,316 | 163 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 156,469 | 1.565 | 20 | 24 | fits | 148,358 | 152 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 298,792 | 2.988 | 20 | 24 | fits | 143,313 | 226 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 298,726 | 2.987 | 20 | 50 | fits | 143,313 | 226 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 406,646 | 4.066 | 20 | 50 | fits | 108,316 | 163 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 496,362 | 4.964 | 20 | 20 | fits | 89,782 | 29 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 903,232 | 9.032 | 20 | 20 | fits | 62,837 | 24 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 343,032 | 3.430 | 20 | 20 | fits | 103,192 | 143 | 0.454 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 298,570 | 2.986 | 20 | 200 | fits | 149,553 | 248 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 401,146 | 4.011 | 20 | 200 | fits | 103,192 | 143 | 0.454 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 299,494 | 2.995 | 20 | 20 | fits | 149,553 | 248 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 401,850 | 4.019 | 20 | 20 | fits | 103,192 | 143 | 0.454 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 153,581 | 1.536 | 20 | 24 | fits | 148,358 | 152 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 302,144 | 3.021 | 20 | 24 | fits | 149,553 | 248 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 302,078 | 3.021 | 20 | 50 | fits | 149,553 | 248 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 404,874 | 4.049 | 20 | 50 | fits | 103,192 | 143 | 0.454 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 500,441 | 5.004 | 20 | 20 | fits | 87,261 | 37 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 897,573 | 8.976 | 20 | 20 | fits | 62,839 | 24 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 359,155 | 3.592 | 20 | 20 | fits | 119,369 | 176 | 0.469 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 289,889 | 2.899 | 20 | 200 | fits | 143,760 | 227 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 417,017 | 4.170 | 20 | 200 | fits | 119,369 | 176 | 0.469 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 290,813 | 2.908 | 20 | 20 | fits | 143,760 | 227 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 417,721 | 4.177 | 20 | 20 | fits | 119,369 | 176 | 0.469 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 150,693 | 1.507 | 20 | 24 | fits | 148,358 | 152 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 293,463 | 2.935 | 20 | 24 | fits | 143,760 | 227 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 293,397 | 2.934 | 20 | 50 | fits | 143,760 | 227 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 420,745 | 4.207 | 20 | 50 | fits | 119,369 | 176 | 0.469 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 510,631 | 5.106 | 20 | 20 | fits | 89,952 | 28 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 896,679 | 8.967 | 20 | 20 | fits | 52,149 | 20 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 352,967 | 3.530 | 20 | 20 | fits | 118,672 | 175 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 293,337 | 2.933 | 20 | 200 | fits | 144,407 | 231 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 411,393 | 4.114 | 20 | 200 | fits | 118,672 | 175 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 294,261 | 2.943 | 20 | 20 | fits | 144,407 | 231 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 412,097 | 4.121 | 20 | 20 | fits | 118,672 | 175 | 0.461 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 146,390 | 1.464 | 20 | 24 | fits | 148,480 | 153 | 0.339 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 296,911 | 2.969 | 20 | 24 | fits | 144,407 | 231 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 296,845 | 2.968 | 20 | 50 | fits | 144,407 | 231 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 415,121 | 4.151 | 20 | 50 | fits | 118,672 | 175 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 505,007 | 5.050 | 20 | 20 | fits | 89,952 | 28 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 891,232 | 8.912 | 20 | 20 | fits | 52,326 | 21 | 0.642 |
| LINK_UP | `adp.link_up.if0` | 2,725 | 0.027 | 20 | 200 | fits | 26,236 | 43 (11) | 0.719 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,363 | 0.084 | 20 | 200 | fits | 21,449 | 23 (39) | 0.714 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 3,341 | 0.033 | 20 | 200 | fits | 2,811 | 10 (11) | 0.586 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 154,235 | 1.542 | 20 | 200 | fits | 155,175 | 249 | 0.465 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 230,942 | 2.309 | 20 | 20 | fits | 96,844 | 86 | 0.647 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 275,393 | 2.754 | 20 | 24 | fits | 86,441 | 53 | 0.502 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 158,415 | 1.584 | 20 | 50 | fits | 88,219 | 183 | 0.343 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 804,215 | 8.042 | 20 | 20 | fits | 70,118 | 30 | 0.652 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 239,096 | 2.391 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 154,235 | 1.542 | 20 | 200 | fits | 155,175 | 249 | 0.465 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 222,820 | 2.228 | 20 | 20 | fits | 88,722 | 88 | 0.672 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 281,806 | 2.818 | 20 | 24 | fits | 84,540 | 61 | 0.540 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 157,377 | 1.574 | 20 | 50 | fits | 91,533 | 189 | 0.369 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 828,533 | 8.285 | 20 | 20 | fits | 88,023 | 38 | 0.562 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 260,424 | 2.604 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 20,466 | 0.205 | 20 | 20 | fits | 28,205 | 21 (35) | 0.816 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 5,077 | 0.051 | 20 | 20 | fits | 24,711 | 17 (14) | 0.848 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 9,649 | 0.096 | 20 | 20 | fits | 24,165 | 18 (14) | 0.843 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 9,559 | 0.096 | 20 | 20 | fits | 28,600 | 21 (35) | 0.822 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 88,679 | 0.887 | 20 | 20 | fits | 27,729 | 8 | 0.815 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 43,525 | 0.435 | 20 | 20 | fits | 43,591 | 12 | 0.882 |
| malformed MRPDU discard | `srp.malformed.if0` | 20,419 | 0.204 | 20 | 20 | fits | 20,485 | 12 | 0.646 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 97,779 | 0.978 | 220 | 220 | fits | 69,635 | 6 | 0.880 |
| an event behind 15 others | `backlog.event.if0` | 167,238 | 1.672 | 20 | 200 | fits | 55,856 | 78 | 0.543 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 422,388 | 4.224 | 20 | 20 | fits | 42,257 | 63 | 0.321 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 418,064 | 4.181 | 20 | 200 | fits | 143,701 | 160 | 0.407 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 417,448 | 4.174 | 20 | 200 | fits | 143,701 | 160 | 0.407 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 413,742 | 4.137 | 20 | 20 | fits | 143,701 | 160 | 0.407 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 455,163 | 4.552 | 20 | 20 | fits | 42,257 | 63 | 0.321 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 151,340 | 1.513 | 20 | 24 | fits | 152,231 | 158 | 0.344 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 416,392 | 4.164 | 20 | 24 | fits | 143,701 | 160 | 0.407 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 416,326 | 4.163 | 20 | 50 | fits | 143,701 | 160 | 0.407 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 415,930 | 4.159 | 20 | 50 | fits | 143,701 | 160 | 0.407 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 458,121 | 4.581 | 20 | 20 | fits | 42,257 | 63 | 0.321 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 520,729 | 5.207 | 20 | 20 | fits | 25,763 | 41 | 0.178 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 341,111 | 3.411 | 20 | 20 | fits | 112,953 | 170 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 286,861 | 2.869 | 20 | 200 | fits | 143,205 | 226 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 399,198 | 3.992 | 20 | 200 | fits | 112,953 | 170 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 287,785 | 2.878 | 20 | 20 | fits | 143,205 | 226 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 399,902 | 3.999 | 20 | 20 | fits | 112,953 | 170 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 148,220 | 1.482 | 20 | 24 | fits | 148,406 | 155 | 0.340 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 290,435 | 2.904 | 20 | 24 | fits | 143,205 | 226 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 290,369 | 2.904 | 20 | 50 | fits | 143,205 | 226 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 402,926 | 4.029 | 20 | 50 | fits | 112,953 | 170 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 500,998 | 5.010 | 20 | 20 | fits | 89,694 | 29 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 894,094 | 8.941 | 20 | 20 | fits | 52,144 | 20 | 0.642 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 13,937 | 0.139 | 20 | 20 | fits | 25,779 | 19 | 0.804 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 286,861 | 2.869 | 20 | 200 | fits | 143,205 | 226 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 31,608 | 0.316 | 20 | 200 | fits | 25,779 | 19 | 0.804 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 287,785 | 2.878 | 20 | 20 | fits | 143,205 | 226 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 389,905 | 3.899 | 20 | 20 | fits | 102,956 | 160 | 0.417 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 148,220 | 1.482 | 20 | 24 | fits | 148,406 | 155 | 0.340 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 290,435 | 2.904 | 20 | 24 | fits | 143,205 | 226 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 290,369 | 2.904 | 20 | 50 | fits | 143,205 | 226 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 392,929 | 3.929 | 20 | 50 | fits | 102,956 | 160 | 0.417 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 490,689 | 4.907 | 20 | 20 | fits | 89,391 | 29 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 883,740 | 8.837 | 20 | 20 | fits | 52,144 | 20 | 0.642 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,273,099 | 62.731 | 20 | 20 | MISS ceiling | 17,418 | 13 | 0.610 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,290,550 | 62.906 | 20 | 20 | MISS ceiling | 17,527 | 14 | 0.615 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,307,872 | 63.079 | 20 | 20 | MISS ceiling | 17,379 | 13 | 0.632 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,325,119 | 63.251 | 20 | 20 | MISS ceiling | 17,323 | 13 | 0.627 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,342,364 | 63.424 | 20 | 20 | MISS ceiling | 17,308 | 13 | 0.627 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 155,448 | 1.554 | 20 | 200 | fits | 145,993 | 222 | 0.402 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 245,809 | 2.458 | 20 | 200 | fits | 90,977 | 164 | 0.385 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 151,126 | 1.511 | 20 | 20 | fits | 145,993 | 222 | 0.402 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,189,345 | 61.893 | 20 | 20 | MISS ceiling | 28,193 | 15 | 0.751 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 154,766 | 1.548 | 20 | 24 | fits | 145,993 | 222 | 0.402 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,164,638 | 61.646 | 20 | 24 | MISS ceiling | 133,860 | 106 | 0.393 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 153,710 | 1.537 | 20 | 50 | fits | 145,993 | 222 | 0.402 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 244,291 | 2.443 | 20 | 50 | fits | 90,977 | 164 | 0.385 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 333,745 | 3.337 | 20 | 20 | fits | 89,520 | 28 | 0.722 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 729,612 | 7.296 | 20 | 20 | fits | 52,632 | 20 | 0.652 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,912 | 0.059 | 20 | 20 | fits | 22,957 | 13 (29) | 0.791 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,541 | 0.075 | 20 | 20 | fits | 25,061 | 19 (35) | 0.790 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 10,980 | 0.110 | 20 | 20 | fits | 27,635 | 21 (12) | 0.806 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 10,855 | 0.109 | 20 | 50 | fits | 26,236 | 43 | 0.719 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 19,979 | 0.200 | 20 | 50 | fits | 22,861 | 35 | 0.707 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 15,445 | 0.154 | 20 | 50 | fits | 22,670 | 35 | 0.707 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 20,250 | 0.203 | 20 | 50 | fits | 27,694 | 61 | 0.639 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 22,414 | 0.224 | 20 | 50 | fits | 27,694 | 61 | 0.639 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 8,859 | 0.089 | 20 | 50 | fits | 20,374 | 30 | 0.626 |
| LINK_UP | `adp.link_up.if0` | 2,725 | 0.027 | 20 | 200 | fits | 26,236 | 43 (11) | 0.719 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,363 | 0.084 | 20 | 200 | fits | 21,449 | 23 (39) | 0.714 |
| LINK_DOWN | `adp.link_down.if0` | 2,366 | 0.024 | 20 | 200 | fits | 24,737 | 23 (9) | 0.750 |
| LINK_UP | `adp.link_up.if0` | 2,725 | 0.027 | 20 | 200 | fits | 26,236 | 43 (11) | 0.719 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,363 | 0.084 | 20 | 200 | fits | 21,449 | 23 (39) | 0.714 |
| GM_CHANGE | `adp.gm_change.if0` | 2,570 | 0.026 | 20 | 200 | fits | 15,953 | 17 (11) | 0.700 |
| LINK_UP | `adp.link_up.if0` | 2,725 | 0.027 | 20 | 200 | fits | 26,236 | 43 (11) | 0.719 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,363 | 0.084 | 20 | 200 | fits | 21,449 | 23 (39) | 0.714 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,398 | 0.044 | 20 | 200 | fits | 15,873 | 16 (31) | 0.659 |
| LINK_UP | `adp.link_up.if0` | 2,725 | 0.027 | 20 | 200 | fits | 26,236 | 43 (11) | 0.719 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,363 | 0.084 | 20 | 200 | fits | 21,449 | 23 (39) | 0.714 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,398 | 0.044 | 20 | 200 | fits | 15,873 | 16 (31) | 0.659 |
| set_name | `aecp_fanout.set_name.if0` | 54,972 | 0.550 | 20 | 24 | fits | 62,329 | 89 | 0.565 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 50,687 | 0.507 | 20 | 24 | fits | 55,798 | 78 | 0.599 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 55,996 | 0.560 | 20 | 24 | fits | 53,927 | 79 | 0.565 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 46,935 | 0.469 | 20 | 24 | fits | 49,661 | 78 | 0.537 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 60,639 | 0.606 | 20 | 24 | fits | 61,222 | 66 | 0.641 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 200,422 | 2.004 | 20 | 24 | fits | 58,027 | 65 | 0.627 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 233,384 | 2.334 | 20 | 24 | fits | 58,442 | 73 | 0.596 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 47,307 | 0.473 | 20 | 24 | fits | 50,149 | 78 | 0.559 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 52,483 | 0.525 | 20 | 24 | fits | 49,472 | 79 | 0.539 |
| BIND_RX | `acmp.bind_rx.if0` | 18,380 | 0.184 | 20 | 20 | fits | 39,037 | 26 (77) | 0.789 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,523 | 0.095 | 20 | 20 | fits | 31,700 | 19 (32) | 0.839 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,271 | 0.103 | 20 | 20 | fits | 23,988 | 15 (47) | 0.757 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,010 | 0.130 | 20 | 20 | fits | 38,876 | 18 (50) | 0.842 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,327 | 0.103 | 20 | 20 | fits | 25,358 | 17 (48) | 0.764 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,779 | 0.098 | 20 | 20 | fits | 23,542 | 16 (48) | 0.727 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,581 | 0.096 | 20 | 20 | fits | 23,004 | 16 (48) | 0.725 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,610 | 0.096 | 20 | 20 | fits | 22,985 | 16 (48) | 0.725 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 14,960 | 0.150 | 20 | 24 | fits | 27,177 | 20 | 0.790 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 27,497 | 0.275 | 20 | 24 | fits | 30,949 | 20 | 0.720 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 17,867 | 0.179 | 20 | 24 | fits | 26,086 | 20 | 0.728 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 23,157 | 0.232 | 20 | 24 | fits | 26,093 | 20 | 0.730 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 23,696 | 0.237 | 20 | 24 | fits | 26,767 | 20 | 0.733 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 18,386 | 0.184 | 20 | 24 | fits | 26,509 | 20 | 0.724 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 23,119 | 0.231 | 20 | 24 | fits | 25,704 | 20 | 0.733 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 17,844 | 0.178 | 20 | 24 | fits | 25,984 | 20 | 0.741 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 22,500 | 0.225 | 20 | 24 | fits | 25,243 | 20 | 0.746 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 20,102 | 0.201 | 20 | 24 | fits | 28,205 | 21 | 0.646 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 22,370 | 0.224 | 20 | 24 | fits | 24,973 | 20 | 0.763 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 22,418 | 0.224 | 20 | 24 | fits | 25,288 | 20 | 0.763 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 17,616 | 0.176 | 20 | 24 | fits | 25,711 | 20 | 0.728 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 23,664 | 0.237 | 20 | 24 | fits | 26,752 | 20 | 0.737 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 17,735 | 0.177 | 20 | 24 | fits | 26,034 | 20 | 0.741 |
| get_configuration | `aecp.get_configuration.if0` | 21,072 | 0.211 | 20 | 24 | fits | 23,537 | 20 | 0.750 |
| entity_available | `aecp.entity_available.if0` | 15,650 | 0.157 | 20 | 24 | fits | 23,309 | 20 | 0.735 |
| get_name | `aecp.get_name.if0` | 18,116 | 0.181 | 20 | 24 | fits | 26,709 | 20 | 0.765 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 24,075 | 0.241 | 20 | 24 | fits | 27,564 | 25 | 0.740 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 18,957 | 0.190 | 20 | 24 | fits | 27,299 | 27 | 0.763 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 21,220 | 0.212 | 20 | 24 | fits | 24,305 | 20 | 0.766 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 15,788 | 0.158 | 20 | 24 | fits | 23,695 | 20 | 0.747 |
| set_name | `aecp.set_name.if0` | 26,379 | 0.264 | 20 | 24 | fits | 43,443 | 43 | 0.754 |
| lock_entity | `aecp.lock_entity.if0` | 26,837 | 0.268 | 20 | 24 | fits | 33,887 | 34 | 0.770 |
| unlock_entity | `aecp.unlock_entity.if0` | 22,029 | 0.220 | 20 | 24 | fits | 33,802 | 33 | 0.757 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 138,546 | 1.385 | 20 | 24 | fits | 146,287 | 92 | 0.332 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 144,717 | 1.447 | 20 | 24 | fits | 138,722 | 69 | 0.313 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 139,094 | 1.391 | 20 | 24 | fits | 41,543 | 17 | 0.702 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 281,327 | 2.813 | 20 | 24 | fits | 92,248 | 18 | 0.679 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 244,909 | 2.449 | 20 | 24 | fits | 101,937 | 32 | 0.684 |
| LINK_UP | `fixture.link_up.if0` | 2,725 | 0.027 | 20 | 200 | fits | 26,236 | 43 (11) | 0.719 |
| malformed MRPDU discard | `fixture.malformed.if0` | 20,905 | 0.209 | 20 | 20 | fits | 20,971 | 12 | 0.710 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 32,068 | 0.321 | 20 | 24 | fits | 45,346 | 43 | 0.770 |
| LINK_DOWN | `fixture.link_down.if0` | 2,751 | 0.028 | 20 | 200 | fits | 27,246 | 23 (9) | 0.787 |
| BIND_RX | `fixture.bind_rx.if0` | 19,014 | 0.190 | 20 | 20 | fits | 39,955 | 26 (77) | 0.799 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 9,683 | 0.097 | 20 | 20 | fits | 35,995 | 29 (35) | 0.796 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 18,581 | 0.186 | 20 | 20 | fits | 24,560 | 13 (29) | 0.819 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 82,161 | 0.822 | 20 | 200 | fits | 82,265 | 49 | 0.753 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 82,161 | 0.822 | 20 | 200 | fits | 82,265 | 49 | 0.753 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 81,887 | 0.819 | 20 | 20 | fits | 82,265 | 49 | 0.753 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 81,887 | 0.819 | 20 | 20 | fits | 82,265 | 49 | 0.753 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 82,095 | 0.821 | 20 | 24 | fits | 82,265 | 49 | 0.753 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 82,095 | 0.821 | 20 | 24 | fits | 82,265 | 49 | 0.753 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 82,029 | 0.820 | 20 | 50 | fits | 82,265 | 49 | 0.753 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 82,029 | 0.820 | 20 | 50 | fits | 82,265 | 49 | 0.753 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 81,963 | 0.820 | 20 | 20 | fits | 82,265 | 49 | 0.753 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 81,963 | 0.820 | 20 | 20 | fits | 82,265 | 49 | 0.753 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
