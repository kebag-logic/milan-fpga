### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 92 paths and 7 of 965 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.186 (0.403) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.091 (0.228) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.082 (0.255) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.155 (0.482) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.099 (0.242) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.092 (0.229) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.095 (0.235) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.100 (0.249) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.088 (0.309) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.225 (0.563) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.193 (0.530) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.198 (0.617) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.065 (0.410) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.139 (0.569) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.071 (0.399) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.127 (0.382) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.044 (0.160) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.022 (0.158) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.025 (0.269) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.026 (0.270) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.069 (0.218) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.125 (0.422) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.214 (0.514) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.228 (0.534) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.094 (0.243) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.122 (0.283) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.240 (0.545) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.157 (0.497) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.213 (0.510) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.163 (0.320) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.239 (0.543) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.235 (0.537) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.118 (0.417) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.235 (0.538) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.100 (0.259) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.121 (0.421) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.130 (0.430) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.232 (0.536) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.121 (0.274) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.208 (0.512) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.113 (0.275) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.217 (0.519) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.122 (0.421) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.181 (0.481) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.282 (0.679) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.101 (0.402) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.251 (0.597) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 1.951 (2.242) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.537 (0.825) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.499 (0.795) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.416 (0.548) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.536 (0.814) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.537 (0.855) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 2.321 (2.615) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.433 (0.696) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 2.300 (2.616) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 1.354 (1.696) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 2.811 (3.148) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 2.414 (2.752) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.361 (1.513) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.294 (4.678) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 4.633 (6.048) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.094 (0.425) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.709 (2.126) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.920 (63.070) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.625 (63.777) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.320 (0.463) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-burst.held.acmp.if0` (save-burst) | 2.376 | fits | 11 acmp | 4 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-burst.held.adp.if0` (save-burst) | 1.575 | fits | 7 adp | 4 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 2.994 | fits | 15 aecp | 4 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 2.367 | fits | 6 maap | 4 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.464 | fits | 31 srp | 4 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.165 (0.475) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.092 (0.215) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.114 (0.270) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.140 (0.475) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.149 (0.446) | fits | 0 events | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.759 | fits | 0 srp | 7 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.207 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.076 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.250 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 5.148 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@program-2.service.aecp.first.if0` (backlog-adp@program-2) | 2.371 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.835 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.233 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 5.186 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.srp.first.if0` (backlog-adp@blank-0) | 6.086 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-2.service.srp.last.if0` (backlog-adp@program-2) | 10.042 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.974 (1.086) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.438 (0.438) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.216 (0.217) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.887 (0.962) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 14.772 | 12 | 146,050 (1.460) | yes | - |
| backlog-adp@blank-1 | 0 | 14.647 | 12 | 146,050 (1.460) | yes | - |
| backlog-adp@blank-2 | 0 | 14.522 | 12 | 146,050 (1.460) | yes | - |
| backlog-adp@blank-3 | 0 | 14.397 | 12 | 146,050 (1.460) | yes | - |
| backlog-adp@blank-4 | 0 | 14.272 | 12 | 146,050 (1.460) | yes | - |
| backlog-adp@blank-5 | 0 | 14.147 | 12 | 146,050 (1.460) | yes | - |
| backlog-adp@blank-6 | 0 | 14.022 | 12 | 146,050 (1.460) | yes | - |
| backlog-adp@blank-7 | 0 | 13.897 | 12 | 146,050 (1.460) | yes | - |
| backlog-adp@program-0 | 0 | 11.879 | 12 | 145,117 (1.451) | yes | - |
| backlog-adp@program-1 | 0 | 11.629 | 12 | 145,117 (1.451) | yes | - |
| backlog-adp@program-2 | 0 | 11.417 | 10 | 144,630 (1.446) | yes | - |
| backlog-adp@program-3 | 1 | 10.458 | 9 | 144,514 (1.445) | yes | - |
| backlog-adp@program-4 | 1 | 10.458 | 9 | 144,514 (1.445) | yes | - |
| backlog-adp@program-5 | 1 | 10.458 | 9 | 144,514 (1.445) | yes | - |
| backlog-adp@program-6 | 0 | 10.571 | 10 | 143,281 (1.433) | yes | - |
| backlog-adp@program-7 | 0 | 11.287 | 10 | 143,358 (1.434) | yes | - |
| backlog-adp@verify-0 | 0 | 12.132 | 12 | 145,171 (1.452) | yes | - |
| backlog-adp@verify-1 | 0 | 12.927 | 12 | 145,216 (1.452) | yes | - |
| backlog-adp@verify-2 | 0 | 12.802 | 12 | 145,216 (1.452) | yes | - |
| backlog-adp@verify-3 | 0 | 12.677 | 12 | 145,216 (1.452) | yes | - |
| backlog-adp@verify-4 | 0 | 12.552 | 12 | 145,216 (1.452) | yes | - |
| backlog-adp@verify-5 | 1 | 12.064 | 11 | 145,100 (1.451) | yes | - |
| backlog-adp@verify-6 | 1 | 12.064 | 11 | 145,100 (1.451) | yes | - |
| backlog-adp@verify-7 | 1 | 12.064 | 11 | 145,100 (1.451) | yes | - |
| backlog-adp@blank-aged2-0 | 1 | 12.923 | 11 | 147,660 (1.477) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 12.905 | 12 | 144,082 (1.441) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 12.612 | 10 | 152,808 (1.528) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 12.573 | 10 | 152,808 (1.528) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 12.552 | 9 | 148,872 (1.489) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 12.628 | 10 | 143,514 (1.435) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 14.807 | 13 | 152,862 (1.529) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 13.772 | 12 | 144,553 (1.446) | yes | - |
| backlog-adp@blank-aged1-0 | 1 | 14.873 | 12 | 148,347 (1.483) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 13.919 | 12 | 152,808 (1.528) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 12.085 | 12 | 145,072 (1.451) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 11.811 | 10 | 144,462 (1.445) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 11.811 | 9 | 148,797 (1.488) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 11.884 | 10 | 143,449 (1.434) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 11.847 | 10 | 152,810 (1.528) | yes | - |
| backlog-adp@blank-aged1-7 | 1 | 13.918 | 11 | 149,015 (1.490) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 12.991 | 13 | 144,408 (1.444) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 12.484 | 12 | 143,854 (1.439) | yes | - |
| backlog-adp@program-aged2-2 | 1 | 11.370 | 10 | 143,940 (1.439) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 11.354 | 10 | 144,309 (1.443) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 11.307 | 10 | 143,505 (1.435) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 11.281 | 10 | 152,841 (1.528) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 11.219 | 9 | 148,342 (1.483) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 14.026 | 13 | 149,895 (1.499) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 11.578 | 11 | 144,333 (1.443) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 11.223 | 10 | 143,579 (1.436) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 11.158 | 9 | 148,033 (1.480) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 11.247 | 10 | 152,864 (1.529) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 11.658 | 12 | 144,433 (1.444) | yes | - |
| backlog-adp@program-aged1-5 | 1 | 11.191 | 9 | 145,690 (1.457) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 11.332 | 10 | 144,289 (1.443) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 11.256 | 10 | 149,697 (1.497) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 12.991 | 12 | 144,277 (1.443) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 12.844 | 12 | 145,074 (1.451) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 12.701 | 10 | 152,825 (1.528) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 12.663 | 10 | 152,825 (1.528) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 12.628 | 10 | 152,825 (1.528) | yes | - |
| backlog-adp@verify-aged2-5 | 1 | 16.643 | 12 | 144,718 (1.447) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 14.962 | 13 | 152,771 (1.528) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 13.877 | 12 | 144,675 (1.447) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 14.963 | 13 | 152,794 (1.528) | yes | - |
| backlog-adp@verify-aged1-1 | 1 | 13.859 | 11 | 148,997 (1.490) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 12.155 | 12 | 145,145 (1.451) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 11.904 | 10 | 144,438 (1.444) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 11.858 | 10 | 144,200 (1.442) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 11.825 | 9 | 144,796 (1.448) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 11.934 | 10 | 144,388 (1.444) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 14.015 | 12 | 145,186 (1.452) | yes | - |
| backlog | 0 | 5.765 | 7 | 157,324 (1.573) | yes | - |
| backlog-adp | 0 | 9.557 | 10 | 152,841 (1.528) | yes | - |
| backlog-adp-refill | 0 | 40.725 | 24 | 152,841 (1.528) | yes | - |
| backlog-owed | 0 | 64.241 | 25 | 149,450 (1.494) | yes | - |
| fixture | 0 | 1.281 | 2 | 82,174 (0.822) | yes | - |

Composed maximum over the 4 backlog windows: 157,324 CPU cycles (1.573 ms), backlog.
Over the windows that released their whole load only: 157,324 (1.573 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-flight | 2994 | 0 | 158,295 (1.583) | fits |
| save-burst | 2754 | 0 | 158,295 (1.583) | fits |
| acmp-notk | 3610 | 0 | 94,706 (0.947) | fits |
| save-second | 50165 | 0 | 49,946 (0.499) | fits |
| backlog-adp@blank-0 | 470 | 0 | 146,050 (1.460) | fits |
| backlog-adp@blank-1 | 470 | 0 | 146,050 (1.460) | fits |
| backlog-adp@blank-2 | 470 | 0 | 146,050 (1.460) | fits |
| backlog-adp@blank-3 | 470 | 0 | 146,050 (1.460) | fits |
| backlog-adp@blank-4 | 470 | 0 | 146,050 (1.460) | fits |
| backlog-adp@blank-5 | 470 | 0 | 146,050 (1.460) | fits |
| backlog-adp@blank-6 | 470 | 0 | 146,050 (1.460) | fits |
| backlog-adp@blank-7 | 470 | 0 | 146,050 (1.460) | fits |
| backlog-adp@program-0 | 478 | 0 | 145,117 (1.451) | fits |
| backlog-adp@program-1 | 478 | 0 | 145,117 (1.451) | fits |
| backlog-adp@program-2 | 477 | 0 | 144,630 (1.446) | fits |
| backlog-adp@program-3 | 477 | 0 | 144,514 (1.445) | fits |
| backlog-adp@program-4 | 477 | 0 | 144,514 (1.445) | fits |
| backlog-adp@program-5 | 477 | 0 | 144,514 (1.445) | fits |
| backlog-adp@program-6 | 478 | 0 | 143,281 (1.433) | fits |
| backlog-adp@program-7 | 478 | 0 | 143,358 (1.434) | fits |
| backlog-adp@verify-0 | 484 | 0 | 145,171 (1.452) | fits |
| backlog-adp@verify-1 | 484 | 0 | 145,216 (1.452) | fits |
| backlog-adp@verify-2 | 484 | 0 | 145,216 (1.452) | fits |
| backlog-adp@verify-3 | 484 | 0 | 145,216 (1.452) | fits |
| backlog-adp@verify-4 | 484 | 0 | 145,216 (1.452) | fits |
| backlog-adp@verify-5 | 484 | 0 | 145,100 (1.451) | fits |
| backlog-adp@verify-6 | 484 | 0 | 145,100 (1.451) | fits |
| backlog-adp@verify-7 | 484 | 0 | 145,100 (1.451) | fits |
| backlog-adp@blank-aged2-0 | 756 | 0 | 152,974 (1.530) | fits |
| backlog-adp@blank-aged2-1 | 765 | 0 | 144,082 (1.441) | fits |
| backlog-adp@blank-aged2-2 | 771 | 0 | 152,808 (1.528) | fits |
| backlog-adp@blank-aged2-3 | 779 | 0 | 152,808 (1.528) | fits |
| backlog-adp@blank-aged2-4 | 787 | 0 | 152,808 (1.528) | fits |
| backlog-adp@blank-aged2-5 | 796 | 0 | 143,514 (1.435) | fits |
| backlog-adp@blank-aged2-6 | 807 | 0 | 152,862 (1.529) | fits |
| backlog-adp@blank-aged2-7 | 814 | 0 | 144,553 (1.446) | fits |
| backlog-adp@blank-aged1-0 | 691 | 0 | 152,862 (1.529) | fits |
| backlog-adp@blank-aged1-1 | 699 | 0 | 152,808 (1.528) | fits |
| backlog-adp@blank-aged1-2 | 707 | 0 | 145,072 (1.451) | fits |
| backlog-adp@blank-aged1-3 | 713 | 0 | 144,462 (1.445) | fits |
| backlog-adp@blank-aged1-4 | 721 | 0 | 148,797 (1.488) | fits |
| backlog-adp@blank-aged1-5 | 730 | 0 | 143,449 (1.434) | fits |
| backlog-adp@blank-aged1-6 | 738 | 0 | 152,810 (1.528) | fits |
| backlog-adp@blank-aged1-7 | 748 | 0 | 152,810 (1.528) | fits |
| backlog-adp@program-aged2-0 | 790 | 0 | 144,408 (1.444) | fits |
| backlog-adp@program-aged2-1 | 797 | 0 | 143,854 (1.439) | fits |
| backlog-adp@program-aged2-2 | 804 | 0 | 143,940 (1.439) | fits |
| backlog-adp@program-aged2-3 | 812 | 0 | 144,309 (1.443) | fits |
| backlog-adp@program-aged2-4 | 820 | 0 | 143,505 (1.435) | fits |
| backlog-adp@program-aged2-5 | 828 | 0 | 152,841 (1.528) | fits |
| backlog-adp@program-aged2-6 | 836 | 0 | 152,841 (1.528) | fits |
| backlog-adp@program-aged2-7 | 848 | 0 | 149,895 (1.499) | fits |
| backlog-adp@program-aged1-0 | 722 | 0 | 144,333 (1.443) | fits |
| backlog-adp@program-aged1-1 | 729 | 0 | 143,579 (1.436) | fits |
| backlog-adp@program-aged1-2 | 737 | 0 | 152,810 (1.528) | fits |
| backlog-adp@program-aged1-3 | 746 | 0 | 152,864 (1.529) | fits |
| backlog-adp@program-aged1-4 | 756 | 0 | 144,433 (1.444) | fits |
| backlog-adp@program-aged1-5 | 762 | 0 | 145,690 (1.457) | fits |
| backlog-adp@program-aged1-6 | 771 | 0 | 144,289 (1.443) | fits |
| backlog-adp@program-aged1-7 | 779 | 0 | 149,697 (1.497) | fits |
| backlog-adp@verify-aged2-0 | 743 | 0 | 144,277 (1.443) | fits |
| backlog-adp@verify-aged2-1 | 751 | 0 | 145,074 (1.451) | fits |
| backlog-adp@verify-aged2-2 | 758 | 0 | 152,825 (1.528) | fits |
| backlog-adp@verify-aged2-3 | 766 | 0 | 152,825 (1.528) | fits |
| backlog-adp@verify-aged2-4 | 774 | 0 | 152,825 (1.528) | fits |
| backlog-adp@verify-aged2-5 | 785 | 0 | 144,718 (1.447) | fits |
| backlog-adp@verify-aged2-6 | 794 | 0 | 152,771 (1.528) | fits |
| backlog-adp@verify-aged2-7 | 801 | 0 | 144,675 (1.447) | fits |
| backlog-adp@verify-aged1-0 | 678 | 0 | 152,794 (1.528) | fits |
| backlog-adp@verify-aged1-1 | 685 | 0 | 152,794 (1.528) | fits |
| backlog-adp@verify-aged1-2 | 694 | 0 | 145,145 (1.451) | fits |
| backlog-adp@verify-aged1-3 | 700 | 0 | 144,438 (1.444) | fits |
| backlog-adp@verify-aged1-4 | 708 | 0 | 144,200 (1.442) | fits |
| backlog-adp@verify-aged1-5 | 716 | 0 | 144,796 (1.448) | fits |
| backlog-adp@verify-aged1-6 | 725 | 0 | 144,388 (1.444) | fits |
| backlog-adp@verify-aged1-7 | 735 | 0 | 145,186 (1.452) | fits |
| adp-advertise | 599 | 0 | 42,064 (0.421) | fits |
| save-held | 1406 | 0 | 158,295 (1.583) | fits |
| save-starved | 26856 | 0 | 158,295 (1.583) | fits |
| acmp-noresp | 2027 | 0 | 87,279 (0.873) | fits |
| save | 610 | 0 | 45,493 (0.455) | fits |
| srp | 290 | 0 | 69,452 (0.695) | fits |
| backlog | 286 | 0 | 157,324 (1.573) | fits |
| backlog-adp | 312 | 0 | 152,841 (1.528) | fits |
| backlog-adp-refill | 326 | 0 | 152,841 (1.528) | fits |
| backlog-owed | 310 | 0 | 149,450 (1.494) | fits |
| acmp-disc | 938 | 0 | 94,550 (0.946) | fits |
| maap | 176 | 0 | 42,064 (0.421) | fits |
| adp-link | 90 | 0 | 45,189 (0.452) | fits |
| adp-gm | 89 | 0 | 42,064 (0.421) | fits |
| adp-discover | 89 | 0 | 42,064 (0.421) | fits |
| control | 89 | 0 | 42,064 (0.421) | fits |
| aecp-fanout | 111 | 0 | 68,258 (0.683) | fits |
| acmp-cmd | 87 | 0 | 42,064 (0.421) | fits |
| aecp | 112 | 0 | 45,254 (0.453) | fits |
| aecp-largest-notice | 106 | 0 | 151,278 (1.513) | fits |
| datapath-events | 118 | 0 | 42,064 (0.421) | fits |
| fixture | 161 | 0 | 82,174 (0.822) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 8.959 (20) | 11.041 |
| backlog-adp@blank-aged2-1 | 2 | none | +9.155 ms, 76,672 (0.767 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 9.117 (20) | 10.883 |
| backlog-adp@blank-aged2-2 | 2 | +8.524 ms, 76,811 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 9.889 (20) | 10.111 |
| backlog-adp@blank-aged2-3 | 2 | +6.795 ms, 76,811 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 9.852 (20) | 10.148 |
| backlog-adp@blank-aged2-4 | 2 | +5.935 ms, 76,811 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 9.831 (20) | 10.169 |
| backlog-adp@blank-aged2-5 | 2 | +5.156 ms, 76,993 (0.770 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 9.904 (20) | 10.096 |
| backlog-adp@blank-aged2-6 | 2 | +4.347 ms, 76,643 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 9.871 (20) | 10.129 |
| backlog-adp@blank-aged2-7 | 2 | +2.945 ms, 76,310 (0.763 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 9.961 (20) | 10.039 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 8.997 (20) | 11.003 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 9.160 (20) | 10.840 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 9.081 (20) | 10.919 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 9.078 (20) | 10.922 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 9.080 (20) | 10.920 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 9.154 (20) | 10.846 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 9.112 (20) | 10.888 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 9.060 (20) | 10.940 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 9.078 (20) | 10.922 |
| backlog-adp@program-aged2-1 | 2 | none | +9.120 ms, 80,242 (0.802 ms), issue | `backlog-adp@program-aged2-1.service.srp.last.if0` | 9.083 (20) | 10.917 |
| backlog-adp@program-aged2-2 | 2 | +8.545 ms, 80,178 (0.802 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 9.875 (20) | 10.125 |
| backlog-adp@program-aged2-3 | 2 | +6.847 ms, 80,178 (0.802 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 9.987 (20) | 10.013 |
| backlog-adp@program-aged2-4 | 2 | +5.956 ms, 80,178 (0.802 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 9.940 (20) | 10.060 |
| backlog-adp@program-aged2-5 | 2 | +4.971 ms, 80,307 (0.803 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 9.913 (20) | 10.087 |
| backlog-adp@program-aged2-6 | 2 | none | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 9.847 (20) | 10.153 |
| backlog-adp@program-aged2-7 | 2 | none | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 9.916 (20) | 10.084 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 9.082 (20) | 10.918 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 9.111 (20) | 10.889 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 9.046 (20) | 10.954 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 9.134 (20) | 10.866 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 9.061 (20) | 10.939 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 9.079 (20) | 10.921 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 9.219 (20) | 10.781 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 9.143 (20) | 10.857 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 8.989 (20) | 11.011 |
| backlog-adp@verify-aged2-1 | 2 | none | +9.062 ms, 77,337 (0.773 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 9.024 (20) | 10.976 |
| backlog-adp@verify-aged2-2 | 2 | +8.577 ms, 77,476 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 9.949 (20) | 10.051 |
| backlog-adp@verify-aged2-3 | 2 | +6.847 ms, 77,476 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 9.911 (20) | 10.089 |
| backlog-adp@verify-aged2-4 | 2 | +5.973 ms, 77,476 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 9.876 (20) | 10.124 |
| backlog-adp@verify-aged2-5 | 2 | +5.064 ms, 77,658 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 9.819 (20) | 10.181 |
| backlog-adp@verify-aged2-6 | 2 | +4.398 ms, 77,244 (0.772 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 9.929 (20) | 10.071 |
| backlog-adp@verify-aged2-7 | 2 | +2.999 ms, 76,978 (0.770 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 10.024 (20) | 9.976 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 9.033 (20) | 10.967 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 9.057 (20) | 10.943 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 9.125 (20) | 10.875 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 9.146 (20) | 10.854 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 9.101 (20) | 10.899 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 9.068 (20) | 10.932 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 9.173 (20) | 10.827 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 9.111 (20) | 10.889 |

Least margin over the aged windows: 9.976 ms, `backlog-adp@verify-aged2-7.service.srp.last.if0` at 10.024 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.460 | 6,070 | 102 | 2 | 30.835 | yes | within |
| save-held | 1087.455 | 4,070 | 102 | - | 19.338 | no | within |
| save-starved | 4048.173 | 4,070 | 102 | - | 31.217 | yes | within |
| save | 1078.709 | 4,070 | 102 | - | 25.138 | no | within |

Names from their response to durable (save_burst.py; #920, the ruling of #665 issuecomment-6899740728, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-flight | 1 | 158.513 (0) | 5,000 | 2 | - | - | 19 steps (want 19), 6.431 ms | within |
| save-burst | 39 | 1101.746 (0) | 5,000 | 1 | - | - | sequence 1, 0 missing | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-flight | 1553 | 93,046 (0.930) | 77,722 (0.777) |
| save-burst | 1479 | 92,933 (0.929) | 77,828 (0.778) |
| acmp-notk | 1158 | 94,706 (0.947) | 77,669 (0.777) |
| save-second | 520 | 79,564 (0.796) | 77,579 (0.776) |
| backlog-adp@blank-0 | 344 | 96,003 (0.960) | 76,288 (0.763) |
| backlog-adp@blank-1 | 344 | 96,003 (0.960) | 76,288 (0.763) |
| backlog-adp@blank-2 | 344 | 96,003 (0.960) | 76,288 (0.763) |
| backlog-adp@blank-3 | 344 | 96,003 (0.960) | 76,288 (0.763) |
| backlog-adp@blank-4 | 344 | 96,003 (0.960) | 76,288 (0.763) |
| backlog-adp@blank-5 | 344 | 96,003 (0.960) | 76,288 (0.763) |
| backlog-adp@blank-6 | 344 | 96,003 (0.960) | 76,288 (0.763) |
| backlog-adp@blank-7 | 344 | 96,003 (0.960) | 76,288 (0.763) |
| backlog-adp@program-0 | 372 | 95,376 (0.954) | 77,838 (0.778) |
| backlog-adp@program-1 | 372 | 95,376 (0.954) | 77,838 (0.778) |
| backlog-adp@program-2 | 373 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@program-3 | 373 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@program-4 | 373 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@program-5 | 373 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@program-6 | 373 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@program-7 | 374 | 98,909 (0.989) | 78,820 (0.788) |
| backlog-adp@verify-0 | 397 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-1 | 398 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-2 | 398 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-3 | 398 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-4 | 398 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-5 | 398 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-6 | 398 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-7 | 398 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@blank-aged2-0 | 340 | 91,589 (0.916) | 76,224 (0.762) |
| backlog-adp@blank-aged2-1 | 340 | 91,569 (0.916) | 75,660 (0.757) |
| backlog-adp@blank-aged2-2 | 340 | 90,083 (0.901) | 75,725 (0.757) |
| backlog-adp@blank-aged2-3 | 340 | 90,088 (0.901) | 75,725 (0.757) |
| backlog-adp@blank-aged2-4 | 340 | 90,088 (0.901) | 75,725 (0.757) |
| backlog-adp@blank-aged2-5 | 340 | 90,445 (0.904) | 75,803 (0.758) |
| backlog-adp@blank-aged2-6 | 342 | 96,075 (0.961) | 75,871 (0.759) |
| backlog-adp@blank-aged2-7 | 341 | 91,164 (0.912) | 76,133 (0.761) |
| backlog-adp@blank-aged1-0 | 342 | 91,570 (0.916) | 76,220 (0.762) |
| backlog-adp@blank-aged1-1 | 341 | 96,067 (0.961) | 76,205 (0.762) |
| backlog-adp@blank-aged1-2 | 339 | 89,921 (0.899) | 76,125 (0.761) |
| backlog-adp@blank-aged1-3 | 339 | 91,316 (0.913) | 76,220 (0.762) |
| backlog-adp@blank-aged1-4 | 339 | 91,076 (0.911) | 76,220 (0.762) |
| backlog-adp@blank-aged1-5 | 339 | 91,076 (0.911) | 76,220 (0.762) |
| backlog-adp@blank-aged1-6 | 339 | 91,511 (0.915) | 76,220 (0.762) |
| backlog-adp@blank-aged1-7 | 341 | 91,636 (0.916) | 76,289 (0.763) |
| backlog-adp@program-aged2-0 | 371 | 94,953 (0.950) | 78,751 (0.788) |
| backlog-adp@program-aged2-1 | 370 | 95,572 (0.956) | 78,400 (0.784) |
| backlog-adp@program-aged2-2 | 369 | 93,763 (0.938) | 78,335 (0.783) |
| backlog-adp@program-aged2-3 | 369 | 93,536 (0.935) | 78,335 (0.783) |
| backlog-adp@program-aged2-4 | 369 | 93,607 (0.936) | 78,335 (0.783) |
| backlog-adp@program-aged2-5 | 369 | 93,666 (0.937) | 78,413 (0.784) |
| backlog-adp@program-aged2-6 | 369 | 93,560 (0.936) | 78,115 (0.781) |
| backlog-adp@program-aged2-7 | 373 | 93,639 (0.936) | 78,120 (0.781) |
| backlog-adp@program-aged1-0 | 369 | 94,594 (0.946) | 78,751 (0.788) |
| backlog-adp@program-aged1-1 | 368 | 94,651 (0.947) | 78,667 (0.787) |
| backlog-adp@program-aged1-2 | 368 | 94,888 (0.949) | 78,736 (0.787) |
| backlog-adp@program-aged1-3 | 368 | 94,854 (0.949) | 78,736 (0.787) |
| backlog-adp@program-aged1-4 | 369 | 94,789 (0.948) | 78,671 (0.787) |
| backlog-adp@program-aged1-5 | 368 | 94,552 (0.946) | 78,751 (0.788) |
| backlog-adp@program-aged1-6 | 368 | 94,518 (0.945) | 78,751 (0.788) |
| backlog-adp@program-aged1-7 | 368 | 94,594 (0.946) | 78,751 (0.788) |
| backlog-adp@verify-aged2-0 | 398 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-aged2-1 | 398 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-aged2-2 | 398 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-aged2-3 | 398 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-aged2-4 | 398 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-aged2-5 | 402 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-aged2-6 | 400 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-aged2-7 | 399 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-aged1-0 | 400 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-aged1-1 | 399 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-aged1-2 | 397 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-aged1-3 | 397 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-aged1-4 | 397 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-aged1-5 | 397 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-aged1-6 | 397 | 98,909 (0.989) | 77,706 (0.777) |
| backlog-adp@verify-aged1-7 | 399 | 98,909 (0.989) | 77,706 (0.777) |
| adp-advertise | 578 | 21,193 (0.212) | 2,071 (0.021) |
| save-held | 816 | 92,898 (0.929) | 77,886 (0.779) |
| save-starved | 418 | 80,189 (0.802) | 77,957 (0.780) |
| acmp-noresp | 708 | 93,448 (0.934) | 77,669 (0.777) |
| save | 679 | 92,886 (0.929) | 77,681 (0.777) |
| srp | 271 | 21,193 (0.212) | 2,071 (0.021) |
| backlog | 265 | 21,193 (0.212) | 2,071 (0.021) |
| backlog-adp | 271 | 21,193 (0.212) | 2,330 (0.023) |
| backlog-adp-refill | 274 | 21,193 (0.212) | 2,330 (0.023) |
| backlog-owed | 276 | 21,193 (0.212) | 2,299 (0.023) |
| acmp-disc | 398 | 94,550 (0.946) | 77,669 (0.777) |
| maap | 163 | 21,193 (0.212) | 2,071 (0.021) |
| adp-link | 80 | 21,193 (0.212) | 2,071 (0.021) |
| adp-gm | 80 | 21,193 (0.212) | 2,071 (0.021) |
| adp-discover | 80 | 21,193 (0.212) | 2,071 (0.021) |
| control | 80 | 21,193 (0.212) | 2,071 (0.021) |
| aecp-fanout | 80 | 23,270 (0.233) | 4,440 (0.044) |
| acmp-cmd | 65 | 21,193 (0.212) | 2,071 (0.021) |
| aecp | 79 | 21,193 (0.212) | 2,071 (0.021) |
| aecp-largest-notice | 78 | 21,193 (0.212) | 2,109 (0.021) |
| datapath-events | 70 | 21,193 (0.212) | 2,071 (0.021) |
| fixture | 54 | 15,848 (0.158) | 2,071 (0.021) |

Longest pass that carries a step: 98,909 CPU cycles (0.989 ms), backlog-adp@program-2; longest step: 78,820 (0.788 ms), backlog-adp@program-7.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 157,355 | 1.574 | 20 | 200 | fits | 158,295 | 250 | 0.480 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 224,911 | 2.249 | 20 | 20 | fits | 87,693 | 82 | 0.674 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 293,247 | 2.932 | 20 | 24 | fits | 79,188 | 43 | 0.575 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 236,723 | 2.367 | 20 | 50 | fits | 98,667 | 202 | 0.314 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 811,617 | 8.116 | 20 | 20 | fits | 74,507 | 28 | 0.592 |
| an MRPDU its join timer owes, the longest | `save-flight.mrpdu.join.if0` | 50,232 | 0.502 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-flight.mrpdu.leaveall.if0` | 46,765 | 0.468 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 105,303 | 1.053 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-burst.held.adp.if0` | 157,486 | 1.575 | 20 | 200 | fits | 158,295 | 250 | 0.480 |
| ACMP record, every channel at its refill rate, the longest | `save-burst.held.acmp.if0` | 237,574 | 2.376 | 20 | 20 | fits | 100,356 | 91 | 0.683 |
| AECP record, every channel at its refill rate, the longest | `save-burst.held.aecp.if0` | 119,051 | 1.191 | 20 | 24 | fits | 49,485 | 25 | 0.800 |
| MAAP record, every channel at its refill rate, the longest | `save-burst.held.maap.if0` | 198,099 | 1.981 | 20 | 50 | fits | 100,356 | 91 | 0.683 |
| SRP record, every channel at its refill rate, the longest | `save-burst.held.srp.if0` | 775,698 | 7.757 | 20 | 20 | fits | 64,902 | 28 | 0.831 |
| an MRPDU its join timer owes, the longest | `save-burst.mrpdu.join.if0` | 49,583 | 0.496 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-burst.mrpdu.periodic.if0` | 262,131 | 2.621 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 13,918 | 0.139 | 20 | 20 | fits | 32,888 | 19 (14) | 0.883 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 463,263 | 4.633 | 20 | 20 | fits | 134,457 | 224 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 372,282 | 3.723 | 20 | 200 | fits | 146,050 | 186 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 514,823 | 5.148 | 20 | 200 | fits | 134,457 | 224 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 373,206 | 3.732 | 20 | 20 | fits | 146,050 | 186 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 515,527 | 5.155 | 20 | 20 | fits | 134,457 | 224 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 230,796 | 2.308 | 20 | 24 | fits | 143,429 | 145 | 0.385 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 375,856 | 3.759 | 20 | 24 | fits | 146,050 | 186 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 375,790 | 3.758 | 20 | 50 | fits | 146,050 | 186 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 518,551 | 5.186 | 20 | 50 | fits | 134,457 | 224 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 608,603 | 6.086 | 20 | 20 | fits | 90,118 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 996,167 | 9.962 | 20 | 20 | fits | 52,177 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 450,763 | 4.508 | 20 | 20 | fits | 134,457 | 224 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 359,782 | 3.598 | 20 | 200 | fits | 146,050 | 186 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 502,323 | 5.023 | 20 | 200 | fits | 134,457 | 224 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 360,706 | 3.607 | 20 | 20 | fits | 146,050 | 186 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 503,027 | 5.030 | 20 | 20 | fits | 134,457 | 224 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 218,296 | 2.183 | 20 | 24 | fits | 143,429 | 145 | 0.385 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 363,356 | 3.634 | 20 | 24 | fits | 146,050 | 186 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 363,290 | 3.633 | 20 | 50 | fits | 146,050 | 186 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 506,051 | 5.061 | 20 | 50 | fits | 134,457 | 224 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 596,103 | 5.961 | 20 | 20 | fits | 90,118 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 983,667 | 9.837 | 20 | 20 | fits | 52,177 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 438,263 | 4.383 | 20 | 20 | fits | 134,457 | 224 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 347,282 | 3.473 | 20 | 200 | fits | 146,050 | 186 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 489,823 | 4.898 | 20 | 200 | fits | 134,457 | 224 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 348,206 | 3.482 | 20 | 20 | fits | 146,050 | 186 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 490,527 | 4.905 | 20 | 20 | fits | 134,457 | 224 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 205,796 | 2.058 | 20 | 24 | fits | 143,429 | 145 | 0.385 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 350,856 | 3.509 | 20 | 24 | fits | 146,050 | 186 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 350,790 | 3.508 | 20 | 50 | fits | 146,050 | 186 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 493,551 | 4.936 | 20 | 50 | fits | 134,457 | 224 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 583,603 | 5.836 | 20 | 20 | fits | 90,118 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 971,167 | 9.712 | 20 | 20 | fits | 52,177 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 425,763 | 4.258 | 20 | 20 | fits | 134,457 | 224 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 334,782 | 3.348 | 20 | 200 | fits | 146,050 | 186 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 477,323 | 4.773 | 20 | 200 | fits | 134,457 | 224 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 335,706 | 3.357 | 20 | 20 | fits | 146,050 | 186 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 478,027 | 4.780 | 20 | 20 | fits | 134,457 | 224 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 193,296 | 1.933 | 20 | 24 | fits | 143,429 | 145 | 0.385 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 338,356 | 3.384 | 20 | 24 | fits | 146,050 | 186 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 338,290 | 3.383 | 20 | 50 | fits | 146,050 | 186 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 481,051 | 4.811 | 20 | 50 | fits | 134,457 | 224 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 571,103 | 5.711 | 20 | 20 | fits | 90,118 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 958,667 | 9.587 | 20 | 20 | fits | 52,177 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 413,263 | 4.133 | 20 | 20 | fits | 134,457 | 224 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 322,282 | 3.223 | 20 | 200 | fits | 146,050 | 186 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 464,823 | 4.648 | 20 | 200 | fits | 134,457 | 224 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 323,206 | 3.232 | 20 | 20 | fits | 146,050 | 186 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 465,527 | 4.655 | 20 | 20 | fits | 134,457 | 224 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 180,796 | 1.808 | 20 | 24 | fits | 143,429 | 145 | 0.385 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 325,856 | 3.259 | 20 | 24 | fits | 146,050 | 186 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 325,790 | 3.258 | 20 | 50 | fits | 146,050 | 186 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 468,551 | 4.686 | 20 | 50 | fits | 134,457 | 224 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 558,603 | 5.586 | 20 | 20 | fits | 90,118 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 946,167 | 9.462 | 20 | 20 | fits | 52,177 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 400,763 | 4.008 | 20 | 20 | fits | 134,457 | 224 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 309,782 | 3.098 | 20 | 200 | fits | 146,050 | 186 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 452,323 | 4.523 | 20 | 200 | fits | 134,457 | 224 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 310,706 | 3.107 | 20 | 20 | fits | 146,050 | 186 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 453,027 | 4.530 | 20 | 20 | fits | 134,457 | 224 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 168,296 | 1.683 | 20 | 24 | fits | 143,429 | 145 | 0.385 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 313,356 | 3.134 | 20 | 24 | fits | 146,050 | 186 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 313,290 | 3.133 | 20 | 50 | fits | 146,050 | 186 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 456,051 | 4.561 | 20 | 50 | fits | 134,457 | 224 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 546,103 | 5.461 | 20 | 20 | fits | 90,118 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 933,667 | 9.337 | 20 | 20 | fits | 52,177 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 388,263 | 3.883 | 20 | 20 | fits | 134,457 | 224 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 297,282 | 2.973 | 20 | 200 | fits | 146,050 | 186 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 439,823 | 4.398 | 20 | 200 | fits | 134,457 | 224 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 298,206 | 2.982 | 20 | 20 | fits | 146,050 | 186 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 440,527 | 4.405 | 20 | 20 | fits | 134,457 | 224 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 155,796 | 1.558 | 20 | 24 | fits | 143,429 | 145 | 0.385 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 300,856 | 3.009 | 20 | 24 | fits | 146,050 | 186 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 300,790 | 3.008 | 20 | 50 | fits | 146,050 | 186 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 443,551 | 4.436 | 20 | 50 | fits | 134,457 | 224 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 533,603 | 5.336 | 20 | 20 | fits | 90,118 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 921,167 | 9.212 | 20 | 20 | fits | 52,177 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 375,763 | 3.758 | 20 | 20 | fits | 134,457 | 224 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 284,782 | 2.848 | 20 | 200 | fits | 146,050 | 186 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 427,323 | 4.273 | 20 | 200 | fits | 134,457 | 224 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 285,706 | 2.857 | 20 | 20 | fits | 146,050 | 186 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 428,027 | 4.280 | 20 | 20 | fits | 134,457 | 224 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 143,296 | 1.433 | 20 | 24 | fits | 143,429 | 145 | 0.385 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 288,356 | 2.884 | 20 | 24 | fits | 146,050 | 186 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 288,290 | 2.883 | 20 | 50 | fits | 146,050 | 186 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 431,051 | 4.311 | 20 | 50 | fits | 134,457 | 224 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 521,103 | 5.211 | 20 | 20 | fits | 90,118 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 908,667 | 9.087 | 20 | 20 | fits | 52,177 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 383,126 | 3.831 | 20 | 20 | fits | 124,877 | 196 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 317,147 | 3.171 | 20 | 200 | fits | 145,117 | 208 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 441,408 | 4.414 | 20 | 200 | fits | 124,877 | 196 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 318,071 | 3.181 | 20 | 20 | fits | 145,117 | 208 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 442,112 | 4.421 | 20 | 20 | fits | 124,877 | 196 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 168,720 | 1.687 | 20 | 24 | fits | 142,985 | 146 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 320,721 | 3.207 | 20 | 24 | fits | 145,117 | 208 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 320,655 | 3.207 | 20 | 50 | fits | 145,117 | 208 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 445,136 | 4.451 | 20 | 50 | fits | 124,877 | 196 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 534,778 | 5.348 | 20 | 20 | fits | 89,708 | 28 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 928,591 | 9.286 | 20 | 20 | fits | 52,177 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 358,126 | 3.581 | 20 | 20 | fits | 124,877 | 196 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 292,147 | 2.921 | 20 | 200 | fits | 145,117 | 208 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 416,408 | 4.164 | 20 | 200 | fits | 124,877 | 196 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 293,071 | 2.931 | 20 | 20 | fits | 145,117 | 208 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 417,112 | 4.171 | 20 | 20 | fits | 124,877 | 196 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 143,720 | 1.437 | 20 | 24 | fits | 142,985 | 146 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 295,721 | 2.957 | 20 | 24 | fits | 145,117 | 208 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 295,655 | 2.957 | 20 | 50 | fits | 145,117 | 208 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 420,136 | 4.201 | 20 | 50 | fits | 124,877 | 196 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 509,778 | 5.098 | 20 | 20 | fits | 89,708 | 28 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 903,591 | 9.036 | 20 | 20 | fits | 52,177 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 452,347 | 4.523 | 20 | 20 | fits | 125,386 | 199 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 377,174 | 3.772 | 20 | 200 | fits | 144,630 | 204 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 501,944 | 5.019 | 20 | 200 | fits | 125,386 | 199 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 378,098 | 3.781 | 20 | 20 | fits | 144,630 | 204 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 502,648 | 5.026 | 20 | 20 | fits | 125,386 | 199 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 237,108 | 2.371 | 20 | 24 | fits | 142,983 | 145 | 0.375 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 380,748 | 3.807 | 20 | 24 | fits | 144,630 | 204 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 380,682 | 3.807 | 20 | 50 | fits | 144,630 | 204 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 505,672 | 5.057 | 20 | 50 | fits | 125,386 | 199 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 590,742 | 5.907 | 20 | 20 | fits | 85,136 | 30 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 1,004,179 | 10.042 | 20 | 20 | fits | 63,443 | 24 | 0.622 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 356,348 | 3.563 | 20 | 20 | fits | 125,386 | 199 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 281,175 | 2.812 | 20 | 200 | fits | 144,514 | 204 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 405,945 | 4.059 | 20 | 200 | fits | 125,386 | 199 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 282,099 | 2.821 | 20 | 20 | fits | 144,514 | 204 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 406,649 | 4.066 | 20 | 20 | fits | 125,386 | 199 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 141,225 | 1.412 | 20 | 24 | fits | 143,047 | 145 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 284,749 | 2.847 | 20 | 24 | fits | 144,514 | 204 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 284,683 | 2.847 | 20 | 50 | fits | 144,514 | 204 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 409,673 | 4.097 | 20 | 50 | fits | 125,386 | 199 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 494,811 | 4.948 | 20 | 20 | fits | 85,204 | 30 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 908,248 | 9.082 | 20 | 20 | fits | 63,443 | 24 | 0.622 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 356,348 | 3.563 | 20 | 20 | fits | 125,386 | 199 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 281,175 | 2.812 | 20 | 200 | fits | 144,514 | 204 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 405,945 | 4.059 | 20 | 200 | fits | 125,386 | 199 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 282,099 | 2.821 | 20 | 20 | fits | 144,514 | 204 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 406,649 | 4.066 | 20 | 20 | fits | 125,386 | 199 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 141,225 | 1.412 | 20 | 24 | fits | 143,047 | 145 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 284,749 | 2.847 | 20 | 24 | fits | 144,514 | 204 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 284,683 | 2.847 | 20 | 50 | fits | 144,514 | 204 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 409,673 | 4.097 | 20 | 50 | fits | 125,386 | 199 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 494,811 | 4.948 | 20 | 20 | fits | 85,204 | 30 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 908,248 | 9.082 | 20 | 20 | fits | 63,443 | 24 | 0.622 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 356,348 | 3.563 | 20 | 20 | fits | 125,386 | 199 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 281,175 | 2.812 | 20 | 200 | fits | 144,514 | 204 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 405,945 | 4.059 | 20 | 200 | fits | 125,386 | 199 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 282,099 | 2.821 | 20 | 20 | fits | 144,514 | 204 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 406,649 | 4.066 | 20 | 20 | fits | 125,386 | 199 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 141,225 | 1.412 | 20 | 24 | fits | 143,047 | 145 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 284,749 | 2.847 | 20 | 24 | fits | 144,514 | 204 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 284,683 | 2.847 | 20 | 50 | fits | 144,514 | 204 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 409,673 | 4.097 | 20 | 50 | fits | 125,386 | 199 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 494,811 | 4.948 | 20 | 20 | fits | 85,204 | 30 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 908,248 | 9.082 | 20 | 20 | fits | 63,443 | 24 | 0.622 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 359,650 | 3.596 | 20 | 20 | fits | 124,728 | 196 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 293,102 | 2.931 | 20 | 200 | fits | 143,281 | 203 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 417,214 | 4.172 | 20 | 200 | fits | 124,728 | 196 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 294,026 | 2.940 | 20 | 20 | fits | 143,281 | 203 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 417,918 | 4.179 | 20 | 20 | fits | 124,728 | 196 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 154,385 | 1.544 | 20 | 24 | fits | 142,510 | 145 | 0.372 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 296,676 | 2.967 | 20 | 24 | fits | 143,281 | 203 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 296,610 | 2.966 | 20 | 50 | fits | 143,281 | 203 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 420,942 | 4.209 | 20 | 50 | fits | 124,728 | 196 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 506,050 | 5.061 | 20 | 20 | fits | 85,174 | 30 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 919,603 | 9.196 | 20 | 20 | fits | 63,443 | 24 | 0.622 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 360,668 | 3.607 | 20 | 20 | fits | 133,194 | 202 | 0.462 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 286,377 | 2.864 | 20 | 200 | fits | 143,358 | 203 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 418,955 | 4.190 | 20 | 200 | fits | 133,194 | 202 | 0.462 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 287,301 | 2.873 | 20 | 20 | fits | 143,358 | 203 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 419,659 | 4.197 | 20 | 20 | fits | 133,194 | 202 | 0.462 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 147,583 | 1.476 | 20 | 24 | fits | 142,701 | 145 | 0.381 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 289,951 | 2.900 | 20 | 24 | fits | 143,358 | 203 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 289,885 | 2.899 | 20 | 50 | fits | 143,358 | 203 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 422,683 | 4.227 | 20 | 50 | fits | 133,194 | 202 | 0.462 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 512,625 | 5.126 | 20 | 20 | fits | 90,008 | 28 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 917,041 | 9.170 | 20 | 20 | fits | 52,544 | 20 | 0.670 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 365,948 | 3.659 | 20 | 20 | fits | 125,050 | 196 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 299,879 | 2.999 | 20 | 200 | fits | 145,171 | 208 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 424,313 | 4.243 | 20 | 200 | fits | 125,050 | 196 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 300,803 | 3.008 | 20 | 20 | fits | 145,171 | 208 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 425,017 | 4.250 | 20 | 20 | fits | 125,050 | 196 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 151,390 | 1.514 | 20 | 24 | fits | 142,685 | 146 | 0.375 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 303,453 | 3.035 | 20 | 24 | fits | 145,171 | 208 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 303,387 | 3.034 | 20 | 50 | fits | 145,171 | 208 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 428,041 | 4.280 | 20 | 50 | fits | 125,050 | 196 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 517,829 | 5.178 | 20 | 20 | fits | 89,854 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 905,200 | 9.052 | 20 | 20 | fits | 52,275 | 21 | 0.658 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 450,826 | 4.508 | 20 | 20 | fits | 124,912 | 196 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 377,306 | 3.773 | 20 | 200 | fits | 145,216 | 208 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 501,602 | 5.016 | 20 | 200 | fits | 124,912 | 196 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 378,230 | 3.782 | 20 | 20 | fits | 145,216 | 208 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 502,306 | 5.023 | 20 | 20 | fits | 124,912 | 196 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 228,765 | 2.288 | 20 | 24 | fits | 142,881 | 146 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 380,880 | 3.809 | 20 | 24 | fits | 145,216 | 208 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 380,814 | 3.808 | 20 | 50 | fits | 145,216 | 208 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 505,330 | 5.053 | 20 | 50 | fits | 124,912 | 196 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 595,257 | 5.953 | 20 | 20 | fits | 89,993 | 28 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 989,273 | 9.893 | 20 | 20 | fits | 52,452 | 21 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 438,326 | 4.383 | 20 | 20 | fits | 124,912 | 196 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 364,806 | 3.648 | 20 | 200 | fits | 145,216 | 208 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 489,102 | 4.891 | 20 | 200 | fits | 124,912 | 196 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 365,730 | 3.657 | 20 | 20 | fits | 145,216 | 208 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 489,806 | 4.898 | 20 | 20 | fits | 124,912 | 196 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 216,265 | 2.163 | 20 | 24 | fits | 142,881 | 146 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 368,380 | 3.684 | 20 | 24 | fits | 145,216 | 208 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 368,314 | 3.683 | 20 | 50 | fits | 145,216 | 208 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 492,830 | 4.928 | 20 | 50 | fits | 124,912 | 196 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 582,757 | 5.828 | 20 | 20 | fits | 89,993 | 28 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 976,773 | 9.768 | 20 | 20 | fits | 52,452 | 21 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 425,826 | 4.258 | 20 | 20 | fits | 124,912 | 196 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 352,306 | 3.523 | 20 | 200 | fits | 145,216 | 208 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 476,602 | 4.766 | 20 | 200 | fits | 124,912 | 196 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 353,230 | 3.532 | 20 | 20 | fits | 145,216 | 208 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 477,306 | 4.773 | 20 | 20 | fits | 124,912 | 196 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 203,765 | 2.038 | 20 | 24 | fits | 142,881 | 146 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 355,880 | 3.559 | 20 | 24 | fits | 145,216 | 208 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 355,814 | 3.558 | 20 | 50 | fits | 145,216 | 208 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 480,330 | 4.803 | 20 | 50 | fits | 124,912 | 196 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 570,257 | 5.703 | 20 | 20 | fits | 89,993 | 28 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 964,273 | 9.643 | 20 | 20 | fits | 52,452 | 21 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 413,326 | 4.133 | 20 | 20 | fits | 124,912 | 196 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 339,806 | 3.398 | 20 | 200 | fits | 145,216 | 208 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 464,102 | 4.641 | 20 | 200 | fits | 124,912 | 196 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 340,730 | 3.407 | 20 | 20 | fits | 145,216 | 208 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 464,806 | 4.648 | 20 | 20 | fits | 124,912 | 196 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 191,265 | 1.913 | 20 | 24 | fits | 142,881 | 146 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 343,380 | 3.434 | 20 | 24 | fits | 145,216 | 208 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 343,314 | 3.433 | 20 | 50 | fits | 145,216 | 208 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 467,830 | 4.678 | 20 | 50 | fits | 124,912 | 196 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 557,757 | 5.578 | 20 | 20 | fits | 89,993 | 28 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 951,773 | 9.518 | 20 | 20 | fits | 52,452 | 21 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 364,510 | 3.645 | 20 | 20 | fits | 124,912 | 196 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 290,990 | 2.910 | 20 | 200 | fits | 145,100 | 208 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 415,286 | 4.153 | 20 | 200 | fits | 124,912 | 196 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 291,914 | 2.919 | 20 | 20 | fits | 145,100 | 208 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 415,990 | 4.160 | 20 | 20 | fits | 124,912 | 196 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 142,565 | 1.426 | 20 | 24 | fits | 144,102 | 146 | 0.381 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 294,564 | 2.946 | 20 | 24 | fits | 145,100 | 208 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 294,498 | 2.945 | 20 | 50 | fits | 145,100 | 208 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 419,014 | 4.190 | 20 | 50 | fits | 124,912 | 196 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 508,940 | 5.089 | 20 | 20 | fits | 89,992 | 28 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 902,924 | 9.029 | 20 | 20 | fits | 52,452 | 21 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 364,510 | 3.645 | 20 | 20 | fits | 124,912 | 196 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 290,990 | 2.910 | 20 | 200 | fits | 145,100 | 208 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 415,286 | 4.153 | 20 | 200 | fits | 124,912 | 196 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 291,914 | 2.919 | 20 | 20 | fits | 145,100 | 208 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 415,990 | 4.160 | 20 | 20 | fits | 124,912 | 196 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 142,565 | 1.426 | 20 | 24 | fits | 144,102 | 146 | 0.381 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 294,564 | 2.946 | 20 | 24 | fits | 145,100 | 208 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 294,498 | 2.945 | 20 | 50 | fits | 145,100 | 208 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 419,014 | 4.190 | 20 | 50 | fits | 124,912 | 196 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 508,940 | 5.089 | 20 | 20 | fits | 89,992 | 28 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 902,924 | 9.029 | 20 | 20 | fits | 52,452 | 21 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 364,510 | 3.645 | 20 | 20 | fits | 124,912 | 196 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 290,990 | 2.910 | 20 | 200 | fits | 145,100 | 208 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 415,286 | 4.153 | 20 | 200 | fits | 124,912 | 196 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 291,914 | 2.919 | 20 | 20 | fits | 145,100 | 208 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 415,990 | 4.160 | 20 | 20 | fits | 124,912 | 196 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 142,565 | 1.426 | 20 | 24 | fits | 144,102 | 146 | 0.381 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 294,564 | 2.946 | 20 | 24 | fits | 145,100 | 208 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 294,498 | 2.945 | 20 | 50 | fits | 145,100 | 208 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 419,014 | 4.190 | 20 | 50 | fits | 124,912 | 196 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 508,940 | 5.089 | 20 | 20 | fits | 89,992 | 28 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 902,924 | 9.029 | 20 | 20 | fits | 52,452 | 21 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 356,911 | 3.569 | 20 | 20 | fits | 113,331 | 169 | 0.473 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 302,000 | 3.020 | 20 | 200 | fits | 147,660 | 231 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 414,715 | 4.147 | 20 | 200 | fits | 113,331 | 169 | 0.473 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 302,924 | 3.029 | 20 | 20 | fits | 147,660 | 231 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 415,419 | 4.154 | 20 | 20 | fits | 113,331 | 169 | 0.473 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 151,218 | 1.512 | 20 | 24 | fits | 152,974 | 153 | 0.356 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 305,574 | 3.056 | 20 | 24 | fits | 147,660 | 231 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 305,508 | 3.055 | 20 | 50 | fits | 147,660 | 231 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 418,443 | 4.184 | 20 | 50 | fits | 113,331 | 169 | 0.473 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 508,574 | 5.086 | 20 | 20 | fits | 90,197 | 28 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 895,852 | 8.959 | 20 | 20 | fits | 52,177 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 375,000 | 3.750 | 20 | 20 | fits | 125,404 | 199 | 0.428 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 299,782 | 2.998 | 20 | 200 | fits | 144,082 | 204 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 424,570 | 4.246 | 20 | 200 | fits | 125,404 | 199 | 0.428 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 300,706 | 3.007 | 20 | 20 | fits | 144,082 | 204 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 425,274 | 4.253 | 20 | 20 | fits | 125,404 | 199 | 0.428 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 152,578 | 1.526 | 20 | 24 | fits | 142,219 | 143 | 0.365 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 303,356 | 3.034 | 20 | 24 | fits | 144,082 | 204 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 303,290 | 3.033 | 20 | 50 | fits | 144,082 | 204 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 428,298 | 4.283 | 20 | 50 | fits | 125,404 | 199 | 0.428 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 518,066 | 5.181 | 20 | 20 | fits | 89,834 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 911,746 | 9.117 | 20 | 20 | fits | 58,645 | 26 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 352,292 | 3.523 | 20 | 20 | fits | 110,481 | 163 | 0.466 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 300,693 | 3.007 | 20 | 200 | fits | 146,950 | 226 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 410,558 | 4.106 | 20 | 200 | fits | 110,481 | 163 | 0.466 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 301,617 | 3.016 | 20 | 20 | fits | 146,950 | 226 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 411,262 | 4.113 | 20 | 20 | fits | 110,481 | 163 | 0.466 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 158,307 | 1.583 | 20 | 24 | fits | 152,808 | 152 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 304,267 | 3.043 | 20 | 24 | fits | 146,950 | 226 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 304,201 | 3.042 | 20 | 50 | fits | 146,950 | 226 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 414,286 | 4.143 | 20 | 50 | fits | 110,481 | 163 | 0.466 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 504,051 | 5.041 | 20 | 20 | fits | 89,831 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 988,945 | 9.889 | 20 | 20 | fits | 63,440 | 25 | 0.617 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 356,542 | 3.565 | 20 | 20 | fits | 110,702 | 166 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 296,053 | 2.961 | 20 | 200 | fits | 146,390 | 222 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 406,139 | 4.061 | 20 | 200 | fits | 110,702 | 166 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 296,977 | 2.970 | 20 | 20 | fits | 146,390 | 222 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 406,843 | 4.068 | 20 | 20 | fits | 110,702 | 166 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 154,227 | 1.542 | 20 | 24 | fits | 152,808 | 152 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 299,627 | 2.996 | 20 | 24 | fits | 146,390 | 222 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 299,561 | 2.996 | 20 | 50 | fits | 146,390 | 222 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 409,867 | 4.099 | 20 | 50 | fits | 110,702 | 166 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 499,703 | 4.997 | 20 | 20 | fits | 89,902 | 28 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 985,177 | 9.852 | 20 | 20 | fits | 63,297 | 24 | 0.618 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 345,973 | 3.460 | 20 | 20 | fits | 110,443 | 163 | 0.465 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 294,455 | 2.945 | 20 | 200 | fits | 148,872 | 231 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 404,282 | 4.043 | 20 | 200 | fits | 110,443 | 163 | 0.465 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 295,379 | 2.954 | 20 | 20 | fits | 148,872 | 231 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 404,986 | 4.050 | 20 | 20 | fits | 110,443 | 163 | 0.465 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 150,147 | 1.501 | 20 | 24 | fits | 152,808 | 152 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 298,029 | 2.980 | 20 | 24 | fits | 148,872 | 231 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 297,963 | 2.980 | 20 | 50 | fits | 148,872 | 231 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 408,010 | 4.080 | 20 | 50 | fits | 110,443 | 163 | 0.465 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 497,953 | 4.980 | 20 | 20 | fits | 90,009 | 29 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 983,069 | 9.831 | 20 | 20 | fits | 63,099 | 24 | 0.611 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 355,138 | 3.551 | 20 | 20 | fits | 125,239 | 197 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 288,997 | 2.890 | 20 | 200 | fits | 143,514 | 203 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 413,620 | 4.136 | 20 | 200 | fits | 125,239 | 197 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 289,921 | 2.899 | 20 | 20 | fits | 143,514 | 203 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 414,324 | 4.143 | 20 | 20 | fits | 125,239 | 197 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 150,047 | 1.500 | 20 | 24 | fits | 141,673 | 142 | 0.365 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 292,571 | 2.926 | 20 | 24 | fits | 143,514 | 203 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 292,505 | 2.925 | 20 | 50 | fits | 143,514 | 203 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 417,348 | 4.173 | 20 | 50 | fits | 125,239 | 197 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 513,929 | 5.139 | 20 | 20 | fits | 87,922 | 37 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 990,365 | 9.904 | 20 | 20 | fits | 63,224 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 379,094 | 3.791 | 20 | 20 | fits | 122,220 | 179 | 0.481 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 299,268 | 2.993 | 20 | 200 | fits | 146,676 | 223 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 429,370 | 4.294 | 20 | 200 | fits | 122,220 | 179 | 0.481 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 300,192 | 3.002 | 20 | 20 | fits | 146,676 | 223 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 430,074 | 4.301 | 20 | 20 | fits | 122,220 | 179 | 0.481 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 157,156 | 1.572 | 20 | 24 | fits | 152,862 | 152 | 0.356 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 302,842 | 3.028 | 20 | 24 | fits | 146,676 | 223 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 302,776 | 3.028 | 20 | 50 | fits | 146,676 | 223 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 433,098 | 4.331 | 20 | 50 | fits | 122,220 | 179 | 0.481 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 599,518 | 5.995 | 20 | 20 | fits | 89,843 | 29 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 987,094 | 9.871 | 20 | 20 | fits | 52,177 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 434,836 | 4.348 | 20 | 20 | fits | 134,365 | 224 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 289,732 | 2.897 | 20 | 200 | fits | 144,553 | 185 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 499,791 | 4.998 | 20 | 200 | fits | 134,365 | 224 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 290,656 | 2.907 | 20 | 20 | fits | 144,553 | 185 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 500,495 | 5.005 | 20 | 20 | fits | 134,365 | 224 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 142,279 | 1.423 | 20 | 24 | fits | 142,065 | 143 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 293,306 | 2.933 | 20 | 24 | fits | 144,553 | 185 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 293,240 | 2.932 | 20 | 50 | fits | 144,553 | 185 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 503,519 | 5.035 | 20 | 50 | fits | 134,365 | 224 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 593,608 | 5.936 | 20 | 20 | fits | 90,155 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 996,102 | 9.961 | 20 | 20 | fits | 57,056 | 27 | 0.720 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 346,753 | 3.468 | 20 | 20 | fits | 110,287 | 164 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 294,889 | 2.949 | 20 | 200 | fits | 148,347 | 231 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 404,560 | 4.046 | 20 | 200 | fits | 110,287 | 164 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 295,813 | 2.958 | 20 | 20 | fits | 148,347 | 231 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 405,264 | 4.053 | 20 | 20 | fits | 110,287 | 164 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 151,106 | 1.511 | 20 | 24 | fits | 152,862 | 152 | 0.356 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 298,463 | 2.985 | 20 | 24 | fits | 148,347 | 231 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 298,397 | 2.984 | 20 | 50 | fits | 148,347 | 231 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 408,288 | 4.083 | 20 | 50 | fits | 110,287 | 164 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 500,435 | 5.004 | 20 | 20 | fits | 83,301 | 31 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 899,709 | 8.997 | 20 | 20 | fits | 63,224 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 377,810 | 3.778 | 20 | 20 | fits | 114,907 | 173 | 0.472 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 305,248 | 3.052 | 20 | 200 | fits | 146,716 | 223 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 428,222 | 4.282 | 20 | 200 | fits | 114,907 | 173 | 0.472 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 306,172 | 3.062 | 20 | 20 | fits | 146,716 | 223 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 428,926 | 4.289 | 20 | 20 | fits | 114,907 | 173 | 0.472 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 163,096 | 1.631 | 20 | 24 | fits | 152,808 | 152 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 308,822 | 3.088 | 20 | 24 | fits | 146,716 | 223 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 308,756 | 3.088 | 20 | 50 | fits | 146,716 | 223 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 431,950 | 4.319 | 20 | 50 | fits | 114,907 | 173 | 0.472 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 522,025 | 5.220 | 20 | 20 | fits | 90,141 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 915,963 | 9.160 | 20 | 20 | fits | 58,678 | 26 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 362,371 | 3.624 | 20 | 20 | fits | 124,988 | 196 | 0.442 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 296,337 | 2.963 | 20 | 200 | fits | 145,072 | 208 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 420,709 | 4.207 | 20 | 200 | fits | 124,988 | 196 | 0.442 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 297,261 | 2.973 | 20 | 20 | fits | 145,072 | 208 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 421,413 | 4.214 | 20 | 20 | fits | 124,988 | 196 | 0.442 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 148,143 | 1.481 | 20 | 24 | fits | 141,935 | 143 | 0.365 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 299,911 | 2.999 | 20 | 24 | fits | 145,072 | 208 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 299,845 | 2.998 | 20 | 50 | fits | 145,072 | 208 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 424,437 | 4.244 | 20 | 50 | fits | 124,988 | 196 | 0.442 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 514,134 | 5.141 | 20 | 20 | fits | 89,763 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 908,089 | 9.081 | 20 | 20 | fits | 52,452 | 21 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 348,114 | 3.481 | 20 | 20 | fits | 124,541 | 196 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 281,788 | 2.818 | 20 | 200 | fits | 144,462 | 203 | 0.423 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 405,713 | 4.057 | 20 | 200 | fits | 124,541 | 196 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 282,712 | 2.827 | 20 | 20 | fits | 144,462 | 203 | 0.423 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 406,417 | 4.064 | 20 | 20 | fits | 124,541 | 196 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 141,890 | 1.419 | 20 | 24 | fits | 141,679 | 142 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 285,362 | 2.854 | 20 | 24 | fits | 144,462 | 203 | 0.423 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 285,296 | 2.853 | 20 | 50 | fits | 144,462 | 203 | 0.423 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 409,441 | 4.094 | 20 | 50 | fits | 124,541 | 196 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 499,233 | 4.992 | 20 | 20 | fits | 89,858 | 28 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 907,840 | 9.078 | 20 | 20 | fits | 56,722 | 27 | 0.714 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 346,515 | 3.465 | 20 | 20 | fits | 122,132 | 205 | 0.458 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 283,471 | 2.835 | 20 | 200 | fits | 148,797 | 231 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 404,987 | 4.050 | 20 | 200 | fits | 122,132 | 205 | 0.458 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 284,395 | 2.844 | 20 | 20 | fits | 148,797 | 231 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 405,691 | 4.057 | 20 | 20 | fits | 122,132 | 205 | 0.458 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 139,238 | 1.392 | 20 | 24 | fits | 142,893 | 111 | 0.372 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 287,045 | 2.870 | 20 | 24 | fits | 148,797 | 231 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 286,979 | 2.870 | 20 | 50 | fits | 148,797 | 231 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 408,715 | 4.087 | 20 | 50 | fits | 122,132 | 205 | 0.458 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 498,689 | 4.987 | 20 | 20 | fits | 90,040 | 28 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 908,012 | 9.080 | 20 | 20 | fits | 52,451 | 20 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 354,027 | 3.540 | 20 | 20 | fits | 125,023 | 196 | 0.442 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 287,886 | 2.879 | 20 | 200 | fits | 143,449 | 203 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 412,293 | 4.123 | 20 | 200 | fits | 125,023 | 196 | 0.442 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 288,810 | 2.888 | 20 | 20 | fits | 143,449 | 203 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 412,997 | 4.130 | 20 | 20 | fits | 125,023 | 196 | 0.442 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 149,001 | 1.490 | 20 | 24 | fits | 141,621 | 142 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 291,460 | 2.915 | 20 | 24 | fits | 143,449 | 203 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 291,394 | 2.914 | 20 | 50 | fits | 143,449 | 203 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 416,021 | 4.160 | 20 | 50 | fits | 125,023 | 196 | 0.442 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 501,274 | 5.013 | 20 | 20 | fits | 85,319 | 30 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 915,408 | 9.154 | 20 | 20 | fits | 63,224 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 366,348 | 3.663 | 20 | 20 | fits | 118,976 | 173 | 0.471 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 297,871 | 2.979 | 20 | 200 | fits | 146,325 | 222 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 416,231 | 4.162 | 20 | 200 | fits | 118,976 | 173 | 0.471 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 298,795 | 2.988 | 20 | 20 | fits | 146,325 | 222 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 416,935 | 4.169 | 20 | 20 | fits | 118,976 | 173 | 0.471 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 156,110 | 1.561 | 20 | 24 | fits | 152,810 | 152 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 301,445 | 3.014 | 20 | 24 | fits | 146,325 | 222 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 301,379 | 3.014 | 20 | 50 | fits | 146,325 | 222 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 419,959 | 4.200 | 20 | 50 | fits | 118,976 | 173 | 0.471 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 511,780 | 5.118 | 20 | 20 | fits | 82,888 | 31 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 911,227 | 9.112 | 20 | 20 | fits | 63,224 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 365,724 | 3.657 | 20 | 20 | fits | 121,284 | 175 | 0.493 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 295,505 | 2.955 | 20 | 200 | fits | 149,015 | 232 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 424,634 | 4.246 | 20 | 200 | fits | 121,284 | 175 | 0.493 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 296,429 | 2.964 | 20 | 20 | fits | 149,015 | 232 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 425,338 | 4.253 | 20 | 20 | fits | 121,284 | 175 | 0.493 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 151,054 | 1.511 | 20 | 24 | fits | 152,810 | 152 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 299,079 | 2.991 | 20 | 24 | fits | 149,015 | 232 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 299,013 | 2.990 | 20 | 50 | fits | 149,015 | 232 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 428,362 | 4.284 | 20 | 50 | fits | 121,284 | 175 | 0.493 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 518,522 | 5.185 | 20 | 20 | fits | 90,226 | 28 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 905,959 | 9.060 | 20 | 20 | fits | 52,177 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 361,829 | 3.618 | 20 | 20 | fits | 125,063 | 197 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 288,318 | 2.883 | 20 | 200 | fits | 144,408 | 203 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 412,765 | 4.128 | 20 | 200 | fits | 125,063 | 197 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 289,242 | 2.892 | 20 | 20 | fits | 144,408 | 203 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 413,469 | 4.135 | 20 | 20 | fits | 125,063 | 197 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 148,474 | 1.485 | 20 | 24 | fits | 141,739 | 142 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 291,892 | 2.919 | 20 | 24 | fits | 144,408 | 203 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 291,826 | 2.918 | 20 | 50 | fits | 144,408 | 203 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 416,493 | 4.165 | 20 | 50 | fits | 125,063 | 197 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 508,483 | 5.085 | 20 | 20 | fits | 83,325 | 31 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 907,757 | 9.078 | 20 | 20 | fits | 63,224 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 361,372 | 3.614 | 20 | 20 | fits | 128,746 | 203 | 0.459 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 283,684 | 2.837 | 20 | 200 | fits | 143,854 | 204 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 420,431 | 4.204 | 20 | 200 | fits | 128,746 | 203 | 0.459 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 284,608 | 2.846 | 20 | 20 | fits | 143,854 | 204 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 421,135 | 4.211 | 20 | 20 | fits | 128,746 | 203 | 0.459 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 144,394 | 1.444 | 20 | 24 | fits | 141,739 | 142 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 287,258 | 2.873 | 20 | 24 | fits | 143,854 | 204 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 287,192 | 2.872 | 20 | 50 | fits | 143,854 | 204 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 424,159 | 4.242 | 20 | 50 | fits | 128,746 | 203 | 0.459 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 514,258 | 5.143 | 20 | 20 | fits | 90,165 | 28 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 908,262 | 9.083 | 20 | 20 | fits | 58,678 | 26 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 365,591 | 3.656 | 20 | 20 | fits | 128,750 | 205 | 0.442 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 287,323 | 2.873 | 20 | 200 | fits | 143,940 | 204 | 0.424 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 415,457 | 4.155 | 20 | 200 | fits | 128,750 | 205 | 0.442 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 288,247 | 2.882 | 20 | 20 | fits | 143,940 | 204 | 0.424 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 416,161 | 4.162 | 20 | 20 | fits | 128,750 | 205 | 0.442 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 140,261 | 1.403 | 20 | 24 | fits | 142,017 | 143 | 0.364 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 290,897 | 2.909 | 20 | 24 | fits | 143,940 | 204 | 0.424 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 290,831 | 2.908 | 20 | 50 | fits | 143,940 | 204 | 0.424 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 419,185 | 4.192 | 20 | 50 | fits | 128,750 | 205 | 0.442 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 509,234 | 5.092 | 20 | 20 | fits | 90,115 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 987,481 | 9.875 | 20 | 20 | fits | 56,552 | 28 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 356,205 | 3.562 | 20 | 20 | fits | 125,041 | 196 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 290,145 | 2.901 | 20 | 200 | fits | 144,309 | 203 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 414,570 | 4.146 | 20 | 200 | fits | 125,041 | 196 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 291,069 | 2.911 | 20 | 20 | fits | 144,309 | 203 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 415,274 | 4.153 | 20 | 20 | fits | 125,041 | 196 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 150,400 | 1.504 | 20 | 24 | fits | 141,648 | 142 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 293,719 | 2.937 | 20 | 24 | fits | 144,309 | 203 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 293,653 | 2.937 | 20 | 50 | fits | 144,309 | 203 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 418,298 | 4.183 | 20 | 50 | fits | 125,041 | 196 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 507,995 | 5.080 | 20 | 20 | fits | 89,763 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 998,719 | 9.987 | 20 | 20 | fits | 52,544 | 20 | 0.670 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 352,087 | 3.521 | 20 | 20 | fits | 124,826 | 196 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 285,468 | 2.855 | 20 | 200 | fits | 143,505 | 203 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 409,678 | 4.097 | 20 | 200 | fits | 124,826 | 196 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 286,392 | 2.864 | 20 | 20 | fits | 143,505 | 203 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 410,382 | 4.104 | 20 | 20 | fits | 124,826 | 196 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 146,527 | 1.465 | 20 | 24 | fits | 141,652 | 142 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 289,042 | 2.890 | 20 | 24 | fits | 143,505 | 203 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 288,976 | 2.890 | 20 | 50 | fits | 143,505 | 203 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 413,406 | 4.134 | 20 | 50 | fits | 124,826 | 196 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 503,174 | 5.032 | 20 | 20 | fits | 89,834 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 993,957 | 9.940 | 20 | 20 | fits | 52,385 | 20 | 0.665 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 355,564 | 3.556 | 20 | 20 | fits | 110,305 | 163 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 296,595 | 2.966 | 20 | 200 | fits | 147,523 | 226 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 406,284 | 4.063 | 20 | 200 | fits | 110,305 | 163 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 297,519 | 2.975 | 20 | 20 | fits | 147,523 | 226 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 406,988 | 4.070 | 20 | 20 | fits | 110,305 | 163 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 153,636 | 1.536 | 20 | 24 | fits | 152,841 | 152 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 300,169 | 3.002 | 20 | 24 | fits | 147,523 | 226 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 300,103 | 3.001 | 20 | 50 | fits | 147,523 | 226 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 410,012 | 4.100 | 20 | 50 | fits | 110,305 | 163 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 495,371 | 4.954 | 20 | 20 | fits | 85,425 | 30 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 991,315 | 9.913 | 20 | 20 | fits | 63,224 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 353,083 | 3.531 | 20 | 20 | fits | 118,839 | 170 | 0.487 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 293,334 | 2.933 | 20 | 200 | fits | 148,342 | 231 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 411,557 | 4.116 | 20 | 200 | fits | 118,839 | 170 | 0.487 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 294,258 | 2.943 | 20 | 20 | fits | 148,342 | 231 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 412,261 | 4.123 | 20 | 20 | fits | 118,839 | 170 | 0.487 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 149,556 | 1.496 | 20 | 24 | fits | 152,841 | 152 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 296,908 | 2.969 | 20 | 24 | fits | 148,342 | 231 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 296,842 | 2.968 | 20 | 50 | fits | 148,342 | 231 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 415,285 | 4.153 | 20 | 50 | fits | 118,839 | 170 | 0.487 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 586,028 | 5.860 | 20 | 20 | fits | 83,184 | 31 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 984,685 | 9.847 | 20 | 20 | fits | 63,016 | 24 | 0.609 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 452,121 | 4.521 | 20 | 20 | fits | 128,943 | 202 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 294,787 | 2.948 | 20 | 200 | fits | 149,895 | 209 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 510,527 | 5.105 | 20 | 200 | fits | 128,943 | 202 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 295,711 | 2.957 | 20 | 20 | fits | 149,895 | 209 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 511,231 | 5.112 | 20 | 20 | fits | 128,943 | 202 | 0.461 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 149,456 | 1.495 | 20 | 24 | fits | 141,706 | 142 | 0.364 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 298,361 | 2.984 | 20 | 24 | fits | 149,895 | 209 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 298,295 | 2.983 | 20 | 50 | fits | 149,895 | 209 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 514,255 | 5.143 | 20 | 50 | fits | 128,943 | 202 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 604,275 | 6.043 | 20 | 20 | fits | 90,086 | 28 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 991,553 | 9.916 | 20 | 20 | fits | 52,177 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 360,665 | 3.607 | 20 | 20 | fits | 124,847 | 196 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 287,154 | 2.872 | 20 | 200 | fits | 144,333 | 203 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 411,385 | 4.114 | 20 | 200 | fits | 124,847 | 196 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 288,078 | 2.881 | 20 | 20 | fits | 144,333 | 203 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 412,089 | 4.121 | 20 | 20 | fits | 124,847 | 196 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 147,385 | 1.474 | 20 | 24 | fits | 141,621 | 142 | 0.362 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 290,728 | 2.907 | 20 | 24 | fits | 144,333 | 203 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 290,662 | 2.907 | 20 | 50 | fits | 144,333 | 203 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 415,113 | 4.151 | 20 | 50 | fits | 124,847 | 196 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 504,881 | 5.049 | 20 | 20 | fits | 89,834 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 908,155 | 9.082 | 20 | 20 | fits | 52,385 | 20 | 0.665 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 348,461 | 3.485 | 20 | 20 | fits | 125,023 | 196 | 0.442 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 282,320 | 2.823 | 20 | 200 | fits | 143,579 | 203 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 406,727 | 4.067 | 20 | 200 | fits | 125,023 | 196 | 0.442 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 283,244 | 2.832 | 20 | 20 | fits | 143,579 | 203 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 407,431 | 4.074 | 20 | 20 | fits | 125,023 | 196 | 0.442 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 143,305 | 1.433 | 20 | 24 | fits | 141,621 | 142 | 0.362 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 285,894 | 2.859 | 20 | 24 | fits | 143,579 | 203 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 285,828 | 2.858 | 20 | 50 | fits | 143,579 | 203 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 410,455 | 4.105 | 20 | 50 | fits | 125,023 | 196 | 0.442 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 493,925 | 4.939 | 20 | 20 | fits | 83,536 | 31 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 911,116 | 9.111 | 20 | 20 | fits | 69,440 | 30 | 0.649 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 366,253 | 3.663 | 20 | 20 | fits | 114,791 | 172 | 0.473 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 293,883 | 2.939 | 20 | 200 | fits | 148,033 | 228 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 416,665 | 4.167 | 20 | 200 | fits | 114,791 | 172 | 0.473 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 294,807 | 2.948 | 20 | 20 | fits | 148,033 | 228 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 417,369 | 4.174 | 20 | 20 | fits | 114,791 | 172 | 0.473 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 150,414 | 1.504 | 20 | 24 | fits | 152,810 | 152 | 0.354 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 297,457 | 2.975 | 20 | 24 | fits | 148,033 | 228 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 297,391 | 2.974 | 20 | 50 | fits | 148,033 | 228 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 420,393 | 4.204 | 20 | 50 | fits | 114,791 | 172 | 0.473 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 510,468 | 5.105 | 20 | 20 | fits | 90,141 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 904,572 | 9.046 | 20 | 20 | fits | 52,277 | 20 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 374,366 | 3.744 | 20 | 20 | fits | 116,416 | 184 | 0.459 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 301,293 | 3.013 | 20 | 200 | fits | 144,354 | 210 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 425,629 | 4.256 | 20 | 200 | fits | 116,416 | 184 | 0.459 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 302,217 | 3.022 | 20 | 20 | fits | 144,354 | 210 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 426,333 | 4.263 | 20 | 20 | fits | 116,416 | 184 | 0.459 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 161,503 | 1.615 | 20 | 24 | fits | 152,864 | 152 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 304,867 | 3.049 | 20 | 24 | fits | 144,354 | 210 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 304,801 | 3.048 | 20 | 50 | fits | 144,354 | 210 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 429,357 | 4.294 | 20 | 50 | fits | 116,416 | 184 | 0.459 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 519,224 | 5.192 | 20 | 20 | fits | 89,933 | 28 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 913,382 | 9.134 | 20 | 20 | fits | 52,177 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 360,465 | 3.605 | 20 | 20 | fits | 125,063 | 196 | 0.442 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 294,257 | 2.943 | 20 | 200 | fits | 144,433 | 208 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 418,704 | 4.187 | 20 | 200 | fits | 125,063 | 196 | 0.442 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 295,181 | 2.952 | 20 | 20 | fits | 144,433 | 208 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 419,408 | 4.194 | 20 | 20 | fits | 125,063 | 196 | 0.442 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 146,702 | 1.467 | 20 | 24 | fits | 142,143 | 143 | 0.364 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 297,831 | 2.978 | 20 | 24 | fits | 144,433 | 208 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 297,765 | 2.978 | 20 | 50 | fits | 144,433 | 208 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 422,432 | 4.224 | 20 | 50 | fits | 125,063 | 196 | 0.442 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 512,255 | 5.123 | 20 | 20 | fits | 89,889 | 28 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 906,068 | 9.061 | 20 | 20 | fits | 52,177 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 354,651 | 3.547 | 20 | 20 | fits | 124,847 | 196 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 281,140 | 2.811 | 20 | 200 | fits | 145,690 | 208 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 405,371 | 4.054 | 20 | 200 | fits | 124,847 | 196 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 282,064 | 2.821 | 20 | 20 | fits | 145,690 | 208 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 406,075 | 4.061 | 20 | 20 | fits | 124,847 | 196 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 140,014 | 1.400 | 20 | 24 | fits | 141,770 | 142 | 0.364 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 284,714 | 2.847 | 20 | 24 | fits | 145,690 | 208 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 284,648 | 2.846 | 20 | 50 | fits | 145,690 | 208 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 409,099 | 4.091 | 20 | 50 | fits | 124,847 | 196 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 494,347 | 4.943 | 20 | 20 | fits | 85,314 | 30 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 907,874 | 9.079 | 20 | 20 | fits | 63,443 | 24 | 0.622 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 366,612 | 3.666 | 20 | 20 | fits | 133,246 | 202 | 0.462 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 292,283 | 2.923 | 20 | 200 | fits | 144,289 | 203 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 424,913 | 4.249 | 20 | 200 | fits | 133,246 | 202 | 0.462 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 293,207 | 2.932 | 20 | 20 | fits | 144,289 | 203 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 425,617 | 4.256 | 20 | 20 | fits | 133,246 | 202 | 0.462 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 152,558 | 1.526 | 20 | 24 | fits | 141,824 | 142 | 0.365 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 295,857 | 2.959 | 20 | 24 | fits | 144,289 | 203 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 295,791 | 2.958 | 20 | 50 | fits | 144,289 | 203 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 428,641 | 4.286 | 20 | 50 | fits | 133,246 | 202 | 0.462 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 518,645 | 5.186 | 20 | 20 | fits | 90,070 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 921,891 | 9.219 | 20 | 20 | fits | 52,385 | 20 | 0.665 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 360,090 | 3.601 | 20 | 20 | fits | 124,686 | 196 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 293,611 | 2.936 | 20 | 200 | fits | 149,697 | 208 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 417,681 | 4.177 | 20 | 200 | fits | 124,686 | 196 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 294,535 | 2.945 | 20 | 20 | fits | 149,697 | 208 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 418,385 | 4.184 | 20 | 20 | fits | 124,686 | 196 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 148,478 | 1.485 | 20 | 24 | fits | 141,824 | 142 | 0.365 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 297,185 | 2.972 | 20 | 24 | fits | 149,697 | 208 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 297,119 | 2.971 | 20 | 50 | fits | 149,697 | 208 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 421,409 | 4.214 | 20 | 50 | fits | 124,686 | 196 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 511,447 | 5.114 | 20 | 20 | fits | 90,104 | 29 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 914,251 | 9.143 | 20 | 20 | fits | 52,260 | 20 | 0.661 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 360,523 | 3.605 | 20 | 20 | fits | 124,866 | 196 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 293,837 | 2.938 | 20 | 200 | fits | 144,277 | 208 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 418,087 | 4.181 | 20 | 200 | fits | 124,866 | 196 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 294,761 | 2.948 | 20 | 20 | fits | 144,277 | 208 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 418,791 | 4.188 | 20 | 20 | fits | 124,866 | 196 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 146,438 | 1.464 | 20 | 24 | fits | 141,887 | 143 | 0.364 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 297,411 | 2.974 | 20 | 24 | fits | 144,277 | 208 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 297,345 | 2.973 | 20 | 50 | fits | 144,277 | 208 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 421,815 | 4.218 | 20 | 50 | fits | 124,866 | 196 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 511,731 | 5.117 | 20 | 20 | fits | 89,982 | 28 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 898,943 | 8.989 | 20 | 20 | fits | 52,177 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 364,454 | 3.645 | 20 | 20 | fits | 124,829 | 196 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 290,934 | 2.909 | 20 | 200 | fits | 145,074 | 208 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 415,147 | 4.151 | 20 | 200 | fits | 124,829 | 196 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 291,858 | 2.919 | 20 | 20 | fits | 145,074 | 208 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 415,851 | 4.159 | 20 | 20 | fits | 124,829 | 196 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 142,738 | 1.427 | 20 | 24 | fits | 142,267 | 143 | 0.364 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 294,508 | 2.945 | 20 | 24 | fits | 145,074 | 208 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 294,442 | 2.944 | 20 | 50 | fits | 145,074 | 208 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 418,875 | 4.189 | 20 | 50 | fits | 124,829 | 196 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 508,733 | 5.087 | 20 | 20 | fits | 89,924 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 902,413 | 9.024 | 20 | 20 | fits | 58,645 | 26 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 357,437 | 3.574 | 20 | 20 | fits | 110,410 | 163 | 0.465 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 305,909 | 3.059 | 20 | 200 | fits | 146,853 | 226 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 415,703 | 4.157 | 20 | 200 | fits | 110,410 | 163 | 0.465 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 306,833 | 3.068 | 20 | 20 | fits | 146,853 | 226 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 416,407 | 4.164 | 20 | 20 | fits | 110,410 | 163 | 0.465 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 163,620 | 1.636 | 20 | 24 | fits | 152,825 | 152 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 309,483 | 3.095 | 20 | 24 | fits | 146,853 | 226 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 309,417 | 3.094 | 20 | 50 | fits | 146,853 | 226 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 419,431 | 4.194 | 20 | 50 | fits | 110,410 | 163 | 0.465 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 509,218 | 5.092 | 20 | 20 | fits | 89,853 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 994,897 | 9.949 | 20 | 20 | fits | 63,519 | 25 | 0.617 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 361,635 | 3.616 | 20 | 20 | fits | 110,631 | 166 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 301,217 | 3.012 | 20 | 200 | fits | 146,241 | 222 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 411,232 | 4.112 | 20 | 200 | fits | 110,631 | 166 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 302,141 | 3.021 | 20 | 20 | fits | 146,241 | 222 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 411,936 | 4.119 | 20 | 20 | fits | 110,631 | 166 | 0.449 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 159,540 | 1.595 | 20 | 24 | fits | 152,825 | 152 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 304,791 | 3.048 | 20 | 24 | fits | 146,241 | 222 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 304,725 | 3.047 | 20 | 50 | fits | 146,241 | 222 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 414,960 | 4.150 | 20 | 50 | fits | 110,631 | 166 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 504,818 | 5.048 | 20 | 20 | fits | 89,924 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 991,077 | 9.911 | 20 | 20 | fits | 63,297 | 24 | 0.618 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 349,696 | 3.497 | 20 | 20 | fits | 110,372 | 163 | 0.465 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 298,249 | 2.982 | 20 | 200 | fits | 147,353 | 226 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 408,005 | 4.080 | 20 | 200 | fits | 110,372 | 163 | 0.465 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 299,173 | 2.992 | 20 | 20 | fits | 147,353 | 226 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 408,709 | 4.087 | 20 | 20 | fits | 110,372 | 163 | 0.465 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 155,460 | 1.555 | 20 | 24 | fits | 152,825 | 152 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 301,823 | 3.018 | 20 | 24 | fits | 147,353 | 226 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 301,757 | 3.018 | 20 | 50 | fits | 147,353 | 226 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 411,733 | 4.117 | 20 | 50 | fits | 110,372 | 163 | 0.465 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 501,698 | 5.017 | 20 | 20 | fits | 90,031 | 29 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 987,599 | 9.876 | 20 | 20 | fits | 63,099 | 24 | 0.611 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 346,582 | 3.466 | 20 | 20 | fits | 124,971 | 197 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 280,034 | 2.800 | 20 | 200 | fits | 144,718 | 208 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 404,389 | 4.044 | 20 | 200 | fits | 124,971 | 197 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 280,958 | 2.810 | 20 | 20 | fits | 144,718 | 208 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 405,093 | 4.051 | 20 | 20 | fits | 124,971 | 197 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 139,880 | 1.399 | 20 | 24 | fits | 141,636 | 142 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 283,608 | 2.836 | 20 | 24 | fits | 144,718 | 208 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 283,542 | 2.835 | 20 | 50 | fits | 144,718 | 208 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 408,117 | 4.081 | 20 | 50 | fits | 124,971 | 197 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 504,682 | 5.047 | 20 | 20 | fits | 88,051 | 37 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 981,862 | 9.819 | 20 | 20 | fits | 63,224 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 384,124 | 3.841 | 20 | 20 | fits | 122,163 | 179 | 0.480 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 304,362 | 3.044 | 20 | 200 | fits | 146,565 | 223 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 434,400 | 4.344 | 20 | 200 | fits | 122,163 | 179 | 0.480 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 305,286 | 3.053 | 20 | 20 | fits | 146,565 | 223 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 435,104 | 4.351 | 20 | 20 | fits | 122,163 | 179 | 0.480 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 162,361 | 1.624 | 20 | 24 | fits | 152,771 | 152 | 0.354 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 307,936 | 3.079 | 20 | 24 | fits | 146,565 | 223 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 307,870 | 3.079 | 20 | 50 | fits | 146,565 | 223 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 438,128 | 4.381 | 20 | 50 | fits | 122,163 | 179 | 0.480 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 605,289 | 6.053 | 20 | 20 | fits | 89,983 | 29 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 992,865 | 9.929 | 20 | 20 | fits | 52,177 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 441,001 | 4.410 | 20 | 20 | fits | 134,395 | 224 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 295,128 | 2.951 | 20 | 200 | fits | 144,675 | 185 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 505,885 | 5.059 | 20 | 200 | fits | 134,395 | 224 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 296,052 | 2.961 | 20 | 20 | fits | 144,675 | 185 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 506,589 | 5.066 | 20 | 20 | fits | 134,395 | 224 | 0.449 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 147,484 | 1.475 | 20 | 24 | fits | 141,974 | 143 | 0.364 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 298,702 | 2.987 | 20 | 24 | fits | 144,675 | 185 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 298,636 | 2.986 | 20 | 50 | fits | 144,675 | 185 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 509,613 | 5.096 | 20 | 50 | fits | 134,395 | 224 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 599,823 | 5.998 | 20 | 20 | fits | 90,276 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,002,358 | 10.024 | 20 | 20 | fits | 57,097 | 27 | 0.721 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 350,392 | 3.504 | 20 | 20 | fits | 110,216 | 164 | 0.462 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 298,599 | 2.986 | 20 | 200 | fits | 146,845 | 226 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 408,199 | 4.082 | 20 | 200 | fits | 110,216 | 164 | 0.462 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 299,523 | 2.995 | 20 | 20 | fits | 146,845 | 226 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 408,903 | 4.089 | 20 | 20 | fits | 110,216 | 164 | 0.462 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 156,318 | 1.563 | 20 | 24 | fits | 152,794 | 152 | 0.354 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 302,173 | 3.022 | 20 | 24 | fits | 146,845 | 226 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 302,107 | 3.021 | 20 | 50 | fits | 146,845 | 226 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 411,927 | 4.119 | 20 | 50 | fits | 110,216 | 164 | 0.462 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 504,061 | 5.041 | 20 | 20 | fits | 83,432 | 31 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 903,335 | 9.033 | 20 | 20 | fits | 63,224 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 366,223 | 3.662 | 20 | 20 | fits | 114,333 | 169 | 0.486 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 295,471 | 2.955 | 20 | 200 | fits | 148,997 | 232 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 417,758 | 4.178 | 20 | 200 | fits | 114,333 | 169 | 0.486 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 296,395 | 2.964 | 20 | 20 | fits | 148,997 | 232 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 418,462 | 4.185 | 20 | 20 | fits | 114,333 | 169 | 0.486 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 151,038 | 1.510 | 20 | 24 | fits | 152,794 | 152 | 0.354 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 299,045 | 2.990 | 20 | 24 | fits | 148,997 | 232 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 298,979 | 2.990 | 20 | 50 | fits | 148,997 | 232 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 421,486 | 4.215 | 20 | 50 | fits | 114,333 | 169 | 0.486 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 511,651 | 5.117 | 20 | 20 | fits | 90,231 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 905,655 | 9.057 | 20 | 20 | fits | 58,678 | 26 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 366,682 | 3.667 | 20 | 20 | fits | 125,023 | 196 | 0.442 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 300,613 | 3.006 | 20 | 200 | fits | 145,145 | 208 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 425,020 | 4.250 | 20 | 200 | fits | 125,023 | 196 | 0.442 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 301,537 | 3.015 | 20 | 20 | fits | 145,145 | 208 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 425,724 | 4.257 | 20 | 20 | fits | 125,023 | 196 | 0.442 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 152,346 | 1.523 | 20 | 24 | fits | 141,867 | 143 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 304,187 | 3.042 | 20 | 24 | fits | 145,145 | 208 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 304,121 | 3.041 | 20 | 50 | fits | 145,145 | 208 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 428,748 | 4.287 | 20 | 50 | fits | 125,023 | 196 | 0.442 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 518,603 | 5.186 | 20 | 20 | fits | 89,921 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 912,515 | 9.125 | 20 | 20 | fits | 52,309 | 21 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 353,351 | 3.534 | 20 | 20 | fits | 124,470 | 196 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 287,096 | 2.871 | 20 | 200 | fits | 144,438 | 203 | 0.423 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 410,950 | 4.109 | 20 | 200 | fits | 124,470 | 196 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 288,020 | 2.880 | 20 | 20 | fits | 144,438 | 203 | 0.423 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 411,654 | 4.117 | 20 | 20 | fits | 124,470 | 196 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 147,222 | 1.472 | 20 | 24 | fits | 141,810 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 290,670 | 2.907 | 20 | 24 | fits | 144,438 | 203 | 0.423 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 290,604 | 2.906 | 20 | 50 | fits | 144,438 | 203 | 0.423 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 414,678 | 4.147 | 20 | 50 | fits | 124,470 | 196 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 504,560 | 5.046 | 20 | 20 | fits | 89,948 | 28 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 914,643 | 9.146 | 20 | 20 | fits | 53,983 | 21 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 348,974 | 3.490 | 20 | 20 | fits | 124,914 | 196 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 282,985 | 2.830 | 20 | 200 | fits | 144,200 | 203 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 407,283 | 4.073 | 20 | 200 | fits | 124,914 | 196 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 283,909 | 2.839 | 20 | 20 | fits | 144,200 | 203 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 407,987 | 4.080 | 20 | 20 | fits | 124,914 | 196 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 143,349 | 1.433 | 20 | 24 | fits | 141,754 | 142 | 0.364 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 286,559 | 2.866 | 20 | 24 | fits | 144,200 | 203 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 286,493 | 2.865 | 20 | 50 | fits | 144,200 | 203 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 411,011 | 4.110 | 20 | 50 | fits | 124,914 | 196 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 500,822 | 5.008 | 20 | 20 | fits | 89,877 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 910,117 | 9.101 | 20 | 20 | fits | 52,419 | 20 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 346,049 | 3.460 | 20 | 20 | fits | 124,755 | 196 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 279,501 | 2.795 | 20 | 200 | fits | 144,796 | 208 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 403,640 | 4.036 | 20 | 200 | fits | 124,755 | 196 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 280,425 | 2.804 | 20 | 20 | fits | 144,796 | 208 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 404,344 | 4.043 | 20 | 20 | fits | 124,755 | 196 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 139,269 | 1.393 | 20 | 24 | fits | 141,754 | 142 | 0.364 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 283,075 | 2.831 | 20 | 24 | fits | 144,796 | 208 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 283,009 | 2.830 | 20 | 50 | fits | 144,796 | 208 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 407,368 | 4.074 | 20 | 50 | fits | 124,755 | 196 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 492,706 | 4.927 | 20 | 20 | fits | 85,404 | 30 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 906,817 | 9.068 | 20 | 20 | fits | 63,224 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 364,438 | 3.644 | 20 | 20 | fits | 132,809 | 203 | 0.458 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 290,074 | 2.901 | 20 | 200 | fits | 144,388 | 203 | 0.423 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 422,267 | 4.223 | 20 | 200 | fits | 132,809 | 203 | 0.458 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 290,998 | 2.910 | 20 | 20 | fits | 144,388 | 203 | 0.423 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 422,971 | 4.230 | 20 | 20 | fits | 132,809 | 203 | 0.458 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 150,250 | 1.502 | 20 | 24 | fits | 141,700 | 142 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 293,648 | 2.936 | 20 | 24 | fits | 144,388 | 203 | 0.423 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 293,582 | 2.936 | 20 | 50 | fits | 144,388 | 203 | 0.423 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 425,995 | 4.260 | 20 | 50 | fits | 132,809 | 203 | 0.458 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 517,834 | 5.178 | 20 | 20 | fits | 83,019 | 31 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 917,281 | 9.173 | 20 | 20 | fits | 63,224 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 364,483 | 3.645 | 20 | 20 | fits | 134,884 | 224 | 0.455 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 286,792 | 2.868 | 20 | 200 | fits | 145,186 | 186 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 429,640 | 4.296 | 20 | 200 | fits | 134,884 | 224 | 0.455 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 287,716 | 2.877 | 20 | 20 | fits | 145,186 | 186 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 430,344 | 4.303 | 20 | 20 | fits | 134,884 | 224 | 0.455 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 146,170 | 1.462 | 20 | 24 | fits | 141,700 | 142 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 290,366 | 2.904 | 20 | 24 | fits | 145,186 | 186 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 290,300 | 2.903 | 20 | 50 | fits | 145,186 | 186 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 433,368 | 4.334 | 20 | 50 | fits | 134,884 | 224 | 0.455 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 523,569 | 5.236 | 20 | 20 | fits | 90,267 | 28 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 911,072 | 9.111 | 20 | 20 | fits | 52,177 | 20 | 0.659 |
| LINK_UP | `adp.link_up.if0` | 2,553 | 0.026 | 20 | 200 | fits | 27,008 | 43 (11) | 0.736 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,544 | 0.125 | 20 | 200 | fits | 21,562 | 23 (39) | 0.721 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 6,926 | 0.069 | 20 | 200 | fits | 2,500 | 10 (11) | 0.538 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 157,355 | 1.574 | 20 | 200 | fits | 158,295 | 250 | 0.480 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 224,911 | 2.249 | 20 | 20 | fits | 87,693 | 82 | 0.674 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 278,512 | 2.785 | 20 | 24 | fits | 85,877 | 55 | 0.573 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 185,436 | 1.854 | 20 | 50 | fits | 87,693 | 82 | 0.674 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 822,164 | 8.222 | 20 | 20 | fits | 84,948 | 32 | 0.557 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 258,271 | 2.583 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 157,355 | 1.574 | 20 | 200 | fits | 158,295 | 250 | 0.480 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 228,165 | 2.282 | 20 | 20 | fits | 90,947 | 88 | 0.682 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 299,355 | 2.994 | 20 | 24 | fits | 87,629 | 61 | 0.570 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 188,690 | 1.887 | 20 | 50 | fits | 90,947 | 88 | 0.682 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 846,435 | 8.464 | 20 | 20 | fits | 88,376 | 38 | 0.583 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 275,880 | 2.759 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 9,820 | 0.098 | 20 | 20 | fits | 28,053 | 21 (35) | 0.816 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 6,476 | 0.065 | 20 | 20 | fits | 25,040 | 17 (14) | 0.856 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 7,058 | 0.071 | 20 | 20 | fits | 24,045 | 18 (14) | 0.846 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 22,507 | 0.225 | 20 | 20 | fits | 28,281 | 21 (35) | 0.819 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 88,711 | 0.887 | 20 | 20 | fits | 27,080 | 8 | 0.792 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 43,779 | 0.438 | 20 | 20 | fits | 43,845 | 12 | 0.882 |
| malformed MRPDU discard | `srp.malformed.if0` | 21,042 | 0.210 | 20 | 20 | fits | 21,108 | 12 | 0.678 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 97,392 | 0.974 | 220 | 220 | fits | 69,452 | 6 | 0.871 |
| an event behind 15 others | `backlog.event.if0` | 170,911 | 1.709 | 20 | 200 | fits | 55,242 | 78 | 0.543 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 429,435 | 4.294 | 20 | 20 | fits | 42,583 | 63 | 0.332 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 425,044 | 4.250 | 20 | 200 | fits | 145,518 | 159 | 0.423 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 424,428 | 4.244 | 20 | 200 | fits | 145,518 | 159 | 0.423 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 420,722 | 4.207 | 20 | 20 | fits | 145,518 | 159 | 0.423 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 462,469 | 4.625 | 20 | 20 | fits | 42,583 | 63 | 0.332 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 156,433 | 1.564 | 20 | 24 | fits | 157,324 | 158 | 0.374 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 423,372 | 4.234 | 20 | 24 | fits | 145,518 | 159 | 0.423 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 423,306 | 4.233 | 20 | 50 | fits | 145,518 | 159 | 0.423 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 422,910 | 4.229 | 20 | 50 | fits | 145,518 | 159 | 0.423 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 465,427 | 4.654 | 20 | 20 | fits | 42,583 | 63 | 0.332 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 527,654 | 5.277 | 20 | 20 | fits | 25,884 | 41 | 0.178 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 357,813 | 3.578 | 20 | 20 | fits | 114,015 | 170 | 0.485 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 294,971 | 2.950 | 20 | 200 | fits | 146,880 | 227 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 416,934 | 4.169 | 20 | 200 | fits | 114,015 | 170 | 0.485 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 295,895 | 2.959 | 20 | 20 | fits | 146,880 | 227 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 417,638 | 4.176 | 20 | 20 | fits | 114,015 | 170 | 0.485 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 152,655 | 1.527 | 20 | 24 | fits | 152,841 | 155 | 0.358 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 298,545 | 2.985 | 20 | 24 | fits | 146,880 | 227 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 298,479 | 2.985 | 20 | 50 | fits | 146,880 | 227 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 420,662 | 4.207 | 20 | 50 | fits | 114,015 | 170 | 0.485 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 510,477 | 5.105 | 20 | 20 | fits | 89,881 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 904,353 | 9.044 | 20 | 20 | fits | 52,204 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 9,379 | 0.094 | 20 | 20 | fits | 26,125 | 19 | 0.817 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 294,971 | 2.950 | 20 | 200 | fits | 146,880 | 227 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 26,868 | 0.269 | 20 | 200 | fits | 26,125 | 19 | 0.817 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 295,895 | 2.959 | 20 | 20 | fits | 146,880 | 227 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 407,289 | 4.073 | 20 | 20 | fits | 103,666 | 160 | 0.451 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 152,655 | 1.527 | 20 | 24 | fits | 152,841 | 155 | 0.358 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 298,545 | 2.985 | 20 | 24 | fits | 146,880 | 227 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 298,479 | 2.985 | 20 | 50 | fits | 146,880 | 227 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 410,313 | 4.103 | 20 | 50 | fits | 103,666 | 160 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 499,882 | 4.999 | 20 | 20 | fits | 89,635 | 28 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 893,786 | 8.938 | 20 | 20 | fits | 52,204 | 20 | 0.659 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,292,019 | 62.920 | 20 | 20 | MISS ceiling | 17,785 | 13 | 0.655 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,309,799 | 63.098 | 20 | 20 | MISS ceiling | 17,750 | 13 | 0.663 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,327,395 | 63.274 | 20 | 20 | MISS ceiling | 17,653 | 13 | 0.671 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,344,973 | 63.450 | 20 | 20 | MISS ceiling | 17,654 | 13 | 0.671 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,362,549 | 63.625 | 20 | 20 | MISS ceiling | 17,567 | 13 | 0.667 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 151,745 | 1.517 | 20 | 200 | fits | 149,450 | 222 | 0.427 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 241,808 | 2.418 | 20 | 200 | fits | 90,679 | 164 | 0.410 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 147,423 | 1.474 | 20 | 20 | fits | 149,450 | 222 | 0.427 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,207,572 | 62.076 | 20 | 20 | MISS ceiling | 27,573 | 15 | 0.747 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 151,063 | 1.511 | 20 | 24 | fits | 149,450 | 222 | 0.427 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,183,485 | 61.835 | 20 | 24 | MISS ceiling | 141,127 | 106 | 0.427 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 150,007 | 1.500 | 20 | 50 | fits | 149,450 | 222 | 0.427 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 240,290 | 2.403 | 20 | 50 | fits | 90,679 | 164 | 0.410 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 330,496 | 3.305 | 20 | 20 | fits | 90,272 | 28 | 0.732 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 726,072 | 7.261 | 20 | 20 | fits | 52,392 | 20 | 0.663 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,381 | 0.054 | 20 | 20 | fits | 22,692 | 13 (29) | 0.786 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 8,161 | 0.082 | 20 | 20 | fits | 25,535 | 19 (35) | 0.804 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 19,283 | 0.193 | 20 | 20 | fits | 28,091 | 21 (12) | 0.815 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 11,357 | 0.114 | 20 | 50 | fits | 27,008 | 43 | 0.736 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 14,946 | 0.149 | 20 | 50 | fits | 23,231 | 35 | 0.721 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 11,747 | 0.117 | 20 | 50 | fits | 22,985 | 35 | 0.719 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 14,022 | 0.140 | 20 | 50 | fits | 28,232 | 61 | 0.649 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 16,507 | 0.165 | 20 | 50 | fits | 28,232 | 61 | 0.649 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 9,185 | 0.092 | 20 | 50 | fits | 21,472 | 30 | 0.669 |
| LINK_UP | `adp.link_up.if0` | 2,553 | 0.026 | 20 | 200 | fits | 27,008 | 43 (11) | 0.736 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,544 | 0.125 | 20 | 200 | fits | 21,562 | 23 (39) | 0.721 |
| LINK_DOWN | `adp.link_down.if0` | 2,177 | 0.022 | 20 | 200 | fits | 25,209 | 23 (9) | 0.767 |
| LINK_UP | `adp.link_up.if0` | 2,553 | 0.026 | 20 | 200 | fits | 27,008 | 43 (11) | 0.736 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,544 | 0.125 | 20 | 200 | fits | 21,562 | 23 (39) | 0.721 |
| GM_CHANGE | `adp.gm_change.if0` | 2,166 | 0.022 | 20 | 200 | fits | 15,843 | 17 (11) | 0.700 |
| LINK_UP | `adp.link_up.if0` | 2,553 | 0.026 | 20 | 200 | fits | 27,008 | 43 (11) | 0.736 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,544 | 0.125 | 20 | 200 | fits | 21,562 | 23 (39) | 0.721 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,445 | 0.044 | 20 | 200 | fits | 15,970 | 16 (31) | 0.663 |
| LINK_UP | `adp.link_up.if0` | 2,553 | 0.026 | 20 | 200 | fits | 27,008 | 43 (11) | 0.736 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,544 | 0.125 | 20 | 200 | fits | 21,562 | 23 (39) | 0.721 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,445 | 0.044 | 20 | 200 | fits | 15,970 | 16 (31) | 0.663 |
| set_name | `aecp_fanout.set_name.if0` | 53,697 | 0.537 | 20 | 24 | fits | 68,258 | 95 | 0.580 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 41,608 | 0.416 | 20 | 24 | fits | 54,777 | 78 | 0.600 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 44,128 | 0.441 | 20 | 24 | fits | 50,365 | 79 | 0.566 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 53,625 | 0.536 | 20 | 24 | fits | 48,848 | 78 | 0.549 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 49,904 | 0.499 | 20 | 24 | fits | 60,462 | 66 | 0.645 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 195,064 | 1.951 | 20 | 24 | fits | 57,904 | 65 | 0.635 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 232,095 | 2.321 | 20 | 24 | fits | 58,120 | 73 | 0.602 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 53,664 | 0.537 | 20 | 24 | fits | 49,034 | 78 | 0.564 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 43,313 | 0.433 | 20 | 24 | fits | 48,634 | 79 | 0.550 |
| BIND_RX | `acmp.bind_rx.if0` | 18,044 | 0.180 | 20 | 20 | fits | 39,530 | 26 (77) | 0.795 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 8,788 | 0.088 | 20 | 20 | fits | 30,897 | 19 (32) | 0.835 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 9,896 | 0.099 | 20 | 20 | fits | 24,190 | 15 (47) | 0.769 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 12,688 | 0.127 | 20 | 20 | fits | 38,237 | 18 (50) | 0.838 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,016 | 0.100 | 20 | 20 | fits | 24,886 | 17 (48) | 0.764 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,453 | 0.095 | 20 | 20 | fits | 23,464 | 16 (48) | 0.739 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,136 | 0.091 | 20 | 20 | fits | 22,836 | 16 (48) | 0.732 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,225 | 0.092 | 20 | 20 | fits | 22,877 | 16 (48) | 0.734 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 18,086 | 0.181 | 20 | 24 | fits | 27,372 | 20 | 0.793 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 16,343 | 0.163 | 20 | 24 | fits | 32,036 | 20 | 0.729 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 23,943 | 0.239 | 20 | 24 | fits | 27,165 | 20 | 0.740 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 12,961 | 0.130 | 20 | 24 | fits | 26,784 | 20 | 0.740 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 11,300 | 0.113 | 20 | 24 | fits | 27,517 | 20 | 0.746 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 21,685 | 0.217 | 20 | 24 | fits | 27,075 | 20 | 0.736 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 12,182 | 0.122 | 20 | 24 | fits | 26,510 | 20 | 0.746 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 23,488 | 0.235 | 20 | 24 | fits | 26,533 | 20 | 0.751 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 11,755 | 0.118 | 20 | 24 | fits | 26,114 | 20 | 0.757 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 23,513 | 0.235 | 20 | 24 | fits | 28,976 | 21 | 0.660 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 10,019 | 0.100 | 20 | 24 | fits | 25,883 | 20 | 0.776 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 12,083 | 0.121 | 20 | 24 | fits | 26,027 | 20 | 0.775 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 23,228 | 0.232 | 20 | 24 | fits | 26,449 | 20 | 0.740 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 12,065 | 0.121 | 20 | 24 | fits | 27,351 | 20 | 0.747 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 20,799 | 0.208 | 20 | 24 | fits | 26,442 | 20 | 0.754 |
| get_configuration | `aecp.get_configuration.if0` | 9,372 | 0.094 | 20 | 24 | fits | 24,321 | 20 | 0.765 |
| entity_available | `aecp.entity_available.if0` | 21,412 | 0.214 | 20 | 24 | fits | 24,230 | 20 | 0.755 |
| get_name | `aecp.get_name.if0` | 23,973 | 0.240 | 20 | 24 | fits | 27,590 | 20 | 0.768 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 12,218 | 0.122 | 20 | 24 | fits | 28,294 | 27 | 0.742 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 22,839 | 0.228 | 20 | 24 | fits | 28,683 | 29 | 0.770 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 10,083 | 0.101 | 20 | 24 | fits | 25,076 | 20 | 0.780 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 21,340 | 0.213 | 20 | 24 | fits | 23,949 | 20 | 0.750 |
| set_name | `aecp.set_name.if0` | 28,199 | 0.282 | 20 | 24 | fits | 45,254 | 43 | 0.768 |
| lock_entity | `aecp.lock_entity.if0` | 15,729 | 0.157 | 20 | 24 | fits | 34,367 | 34 | 0.782 |
| unlock_entity | `aecp.unlock_entity.if0` | 25,116 | 0.251 | 20 | 24 | fits | 32,733 | 33 | 0.772 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 136,149 | 1.361 | 20 | 24 | fits | 151,278 | 99 | 0.348 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 229,967 | 2.300 | 20 | 24 | fits | 136,253 | 69 | 0.300 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 135,354 | 1.354 | 20 | 24 | fits | 40,401 | 18 | 0.697 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 281,085 | 2.811 | 20 | 24 | fits | 91,738 | 17 | 0.688 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 241,406 | 2.414 | 20 | 24 | fits | 93,743 | 17 | 0.698 |
| LINK_UP | `fixture.link_up.if0` | 2,553 | 0.026 | 20 | 200 | fits | 27,008 | 43 (11) | 0.736 |
| malformed MRPDU discard | `fixture.malformed.if0` | 21,602 | 0.216 | 20 | 20 | fits | 21,668 | 12 | 0.738 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 32,003 | 0.320 | 20 | 24 | fits | 46,279 | 43 | 0.771 |
| LINK_DOWN | `fixture.link_down.if0` | 2,515 | 0.025 | 20 | 200 | fits | 26,856 | 23 (9) | 0.784 |
| BIND_RX | `fixture.bind_rx.if0` | 18,627 | 0.186 | 20 | 20 | fits | 40,270 | 26 (77) | 0.800 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 19,842 | 0.198 | 20 | 20 | fits | 35,986 | 29 (35) | 0.796 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 15,452 | 0.155 | 20 | 20 | fits | 24,371 | 13 (29) | 0.823 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 82,070 | 0.821 | 20 | 200 | fits | 82,174 | 49 | 0.752 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 82,070 | 0.821 | 20 | 200 | fits | 82,174 | 49 | 0.752 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 81,796 | 0.818 | 20 | 20 | fits | 82,174 | 49 | 0.752 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 81,796 | 0.818 | 20 | 20 | fits | 82,174 | 49 | 0.752 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 82,004 | 0.820 | 20 | 24 | fits | 82,174 | 49 | 0.752 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 82,004 | 0.820 | 20 | 24 | fits | 82,174 | 49 | 0.752 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 81,938 | 0.819 | 20 | 50 | fits | 82,174 | 49 | 0.752 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 81,938 | 0.819 | 20 | 50 | fits | 82,174 | 49 | 0.752 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 81,872 | 0.819 | 20 | 20 | fits | 82,174 | 49 | 0.752 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 81,872 | 0.819 | 20 | 20 | fits | 82,174 | 49 | 0.752 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
