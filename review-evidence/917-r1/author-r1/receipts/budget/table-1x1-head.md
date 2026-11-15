### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 87 paths and 7 of 945 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.198 (0.392) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.096 (0.220) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.077 (0.237) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.062 (0.216) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.106 (0.232) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.099 (0.216) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.099 (0.227) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.105 (0.237) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.093 (0.298) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.096 (0.283) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.204 (0.518) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.206 (0.484) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.148 (0.451) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.132 (0.542) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.194 (0.450) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.133 (0.376) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.046 (0.146) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.024 (0.150) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.025 (0.247) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.025 (0.253) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.023 (0.025) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.101 (0.373) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.083 (0.219) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.176 (0.436) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.143 (0.392) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.112 (0.256) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.164 (0.423) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.283 (0.565) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.079 (0.217) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.208 (0.463) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.110 (0.250) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.110 (0.246) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.150 (0.411) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.130 (0.266) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.153 (0.403) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.094 (0.232) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.160 (0.414) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.155 (0.410) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.155 (0.418) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.105 (0.243) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.106 (0.251) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.119 (0.255) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.158 (0.414) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.200 (0.458) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.229 (0.406) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.139 (0.398) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.230 (0.472) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 0.479 (0.766) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.367 (0.459) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.403 (0.526) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.390 (0.505) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.458 (0.714) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.547 (0.841) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.444 (0.701) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.466 (0.721) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.831 (5.558) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-6.adp_available.if0` (backlog-adp@program-aged2-6) | 8.607 (9.682) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.087 (0.389) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.697 (2.360) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.949 (63.194) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.585 (63.829) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.277 (0.411) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 7.157 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 1.519 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 3.448 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 6.762 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 4.979 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.157 (0.442) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.102 (0.202) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.102 (0.253) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.135 (0.442) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.188 (0.459) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 1.868 | fits | 0 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 2.138 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.179 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 2.129 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-6.service.adp.last.if0` (backlog-adp@program-aged2-6) | 9.651 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.174 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.948 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 2.164 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-3.service.maap.last.if0` (backlog-adp@verify-3) | 8.955 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-6.service.srp.first.if0` (backlog-adp@verify-aged2-6) | 6.707 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-4.service.srp.last.if0` (backlog-adp@verify-aged2-4) | 9.521 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.965 (1.349) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.431 (0.431) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.197 (0.198) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.837 (0.913) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.071 | 9 | 154,430 (1.544) | yes | - |
| backlog-adp@blank-1 | 0 | 10.250 | 8 | 154,514 (1.545) | yes | - |
| backlog-adp@blank-2 | 0 | 10.388 | 8 | 154,959 (1.550) | yes | - |
| backlog-adp@blank-3 | 0 | 10.336 | 8 | 154,808 (1.548) | yes | - |
| backlog-adp@blank-4 | 0 | 10.177 | 7 | 153,061 (1.531) | yes | - |
| backlog-adp@blank-5 | 0 | 10.646 | 10 | 153,705 (1.537) | yes | - |
| backlog-adp@blank-6 | 0 | 10.229 | 8 | 154,435 (1.544) | yes | - |
| backlog-adp@blank-7 | 0 | 10.371 | 8 | 153,118 (1.531) | yes | - |
| backlog-adp@program-0 | 0 | 10.292 | 8 | 153,827 (1.538) | yes | - |
| backlog-adp@program-1 | 0 | 10.751 | 10 | 154,708 (1.547) | yes | - |
| backlog-adp@program-2 | 0 | 10.317 | 8 | 154,013 (1.540) | yes | - |
| backlog-adp@program-3 | 0 | 10.388 | 8 | 153,422 (1.534) | yes | - |
| backlog-adp@program-4 | 0 | 9.622 | 8 | 153,963 (1.540) | yes | - |
| backlog-adp@program-5 | 0 | 9.565 | 8 | 153,935 (1.539) | yes | - |
| backlog-adp@program-6 | 0 | 9.402 | 7 | 153,865 (1.539) | yes | - |
| backlog-adp@program-7 | 0 | 9.622 | 8 | 155,825 (1.558) | yes | - |
| backlog-adp@verify-0 | 0 | 10.712 | 9 | 154,490 (1.545) | yes | - |
| backlog-adp@verify-1 | 0 | 10.248 | 8 | 154,215 (1.542) | yes | - |
| backlog-adp@verify-2 | 0 | 10.310 | 8 | 155,252 (1.553) | yes | - |
| backlog-adp@verify-3 | 0 | 10.415 | 8 | 154,808 (1.548) | yes | - |
| backlog-adp@verify-4 | 0 | 10.636 | 10 | 153,311 (1.533) | yes | - |
| backlog-adp@verify-5 | 1 | 10.215 | 7 | 149,375 (1.494) | yes | - |
| backlog-adp@verify-6 | 0 | 10.073 | 6 | 154,381 (1.544) | yes | - |
| backlog-adp@verify-7 | 0 | 10.335 | 8 | 153,511 (1.535) | yes | - |
| backlog-adp@blank-aged2-0 | 1 | 11.458 | 10 | 150,131 (1.501) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 10.453 | 9 | 150,076 (1.501) | yes | - |
| backlog-adp@blank-aged2-2 | 1 | 10.235 | 7 | 149,019 (1.490) | yes | - |
| backlog-adp@blank-aged2-3 | 1 | 10.198 | 7 | 153,700 (1.537) | yes | - |
| backlog-adp@blank-aged2-4 | 1 | 10.210 | 7 | 152,442 (1.524) | yes | - |
| backlog-adp@blank-aged2-5 | 1 | 10.203 | 7 | 153,235 (1.532) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 10.074 | 7 | 153,995 (1.540) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 10.197 | 8 | 147,656 (1.477) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 11.962 | 9 | 154,125 (1.541) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 11.074 | 9 | 154,048 (1.540) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 11.549 | 11 | 154,172 (1.542) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 11.146 | 10 | 153,398 (1.534) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 10.898 | 8 | 154,166 (1.542) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 11.032 | 9 | 154,005 (1.540) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 10.888 | 8 | 154,047 (1.540) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 12.160 | 10 | 153,047 (1.530) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 10.635 | 10 | 153,124 (1.531) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 10.105 | 8 | 153,501 (1.535) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 10.290 | 8 | 153,504 (1.535) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 10.301 | 8 | 154,623 (1.546) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 10.124 | 7 | 153,837 (1.538) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 10.121 | 7 | 153,869 (1.539) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 10.356 | 9 | 156,501 (1.565) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 10.301 | 8 | 153,278 (1.533) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 11.021 | 10 | 154,071 (1.541) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.655 | 10 | 153,248 (1.532) | yes | - |
| backlog-adp@program-aged1-2 | 1 | 10.287 | 7 | 153,527 (1.535) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 10.383 | 8 | 153,462 (1.535) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 10.188 | 7 | 155,447 (1.554) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 10.190 | 7 | 153,635 (1.536) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 10.205 | 7 | 153,777 (1.538) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 10.295 | 7 | 152,488 (1.525) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.157 | 8 | 154,254 (1.543) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 10.138 | 8 | 154,129 (1.541) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 10.381 | 8 | 153,960 (1.540) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 10.391 | 8 | 154,155 (1.542) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 10.254 | 7 | 153,423 (1.534) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 10.423 | 9 | 150,216 (1.502) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 10.300 | 7 | 153,381 (1.534) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 10.300 | 7 | 153,092 (1.531) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 11.333 | 10 | 153,436 (1.534) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 10.199 | 8 | 154,039 (1.540) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 10.268 | 8 | 154,000 (1.540) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 10.283 | 8 | 154,770 (1.548) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 10.109 | 7 | 154,357 (1.544) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 10.096 | 7 | 154,442 (1.544) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 10.341 | 9 | 156,167 (1.562) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 10.267 | 8 | 153,500 (1.535) | yes | - |
| backlog | 0 | 6.221 | 8 | 155,766 (1.558) | yes | - |
| backlog-adp | 0 | 9.545 | 8 | 154,682 (1.547) | yes | - |
| backlog-adp-refill | 0 | 40.660 | 22 | 154,682 (1.547) | yes | - |
| backlog-owed | 0 | 64.132 | 22 | 158,371 (1.584) | yes | - |
| fixture | 0 | 1.219 | 2 | 81,638 (0.816) | yes | - |

Composed maximum over the 4 backlog windows: 158,371 CPU cycles (1.584 ms), backlog-owed.
Over the windows that released their whole load only: 158,371 (1.584 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3597 | 0 | 66,772 (0.668) | fits |
| save-second | 54440 | 0 | 66,016 (0.660) | fits |
| backlog-adp@blank-0 | 409 | 0 | 154,430 (1.544) | fits |
| backlog-adp@blank-1 | 408 | 0 | 154,514 (1.545) | fits |
| backlog-adp@blank-2 | 408 | 0 | 154,959 (1.550) | fits |
| backlog-adp@blank-3 | 408 | 0 | 154,808 (1.548) | fits |
| backlog-adp@blank-4 | 408 | 0 | 153,061 (1.531) | fits |
| backlog-adp@blank-5 | 410 | 0 | 153,705 (1.537) | fits |
| backlog-adp@blank-6 | 410 | 0 | 154,435 (1.544) | fits |
| backlog-adp@blank-7 | 410 | 0 | 153,118 (1.531) | fits |
| backlog-adp@program-0 | 510 | 0 | 153,827 (1.538) | fits |
| backlog-adp@program-1 | 512 | 0 | 154,708 (1.547) | fits |
| backlog-adp@program-2 | 512 | 0 | 154,013 (1.540) | fits |
| backlog-adp@program-3 | 512 | 0 | 153,422 (1.534) | fits |
| backlog-adp@program-4 | 514 | 0 | 153,963 (1.540) | fits |
| backlog-adp@program-5 | 515 | 0 | 153,935 (1.539) | fits |
| backlog-adp@program-6 | 514 | 0 | 153,865 (1.539) | fits |
| backlog-adp@program-7 | 515 | 0 | 155,825 (1.558) | fits |
| backlog-adp@verify-0 | 606 | 0 | 154,490 (1.545) | fits |
| backlog-adp@verify-1 | 605 | 0 | 154,215 (1.542) | fits |
| backlog-adp@verify-2 | 605 | 0 | 155,252 (1.553) | fits |
| backlog-adp@verify-3 | 605 | 0 | 154,808 (1.548) | fits |
| backlog-adp@verify-4 | 607 | 0 | 153,311 (1.533) | fits |
| backlog-adp@verify-5 | 606 | 0 | 151,213 (1.512) | fits |
| backlog-adp@verify-6 | 606 | 0 | 154,381 (1.544) | fits |
| backlog-adp@verify-7 | 607 | 0 | 153,511 (1.535) | fits |
| backlog-adp@blank-aged2-0 | 756 | 0 | 153,227 (1.532) | fits |
| backlog-adp@blank-aged2-1 | 761 | 0 | 150,076 (1.501) | fits |
| backlog-adp@blank-aged2-2 | 769 | 0 | 149,909 (1.499) | fits |
| backlog-adp@blank-aged2-3 | 777 | 0 | 153,700 (1.537) | fits |
| backlog-adp@blank-aged2-4 | 786 | 0 | 152,442 (1.524) | fits |
| backlog-adp@blank-aged2-5 | 795 | 0 | 153,235 (1.532) | fits |
| backlog-adp@blank-aged2-6 | 803 | 0 | 153,995 (1.540) | fits |
| backlog-adp@blank-aged2-7 | 813 | 0 | 147,656 (1.477) | fits |
| backlog-adp@blank-aged1-0 | 685 | 0 | 154,125 (1.541) | fits |
| backlog-adp@blank-aged1-1 | 694 | 0 | 154,048 (1.540) | fits |
| backlog-adp@blank-aged1-2 | 705 | 0 | 154,172 (1.542) | fits |
| backlog-adp@blank-aged1-3 | 713 | 0 | 153,398 (1.534) | fits |
| backlog-adp@blank-aged1-4 | 720 | 0 | 154,166 (1.542) | fits |
| backlog-adp@blank-aged1-5 | 730 | 0 | 154,005 (1.540) | fits |
| backlog-adp@blank-aged1-6 | 738 | 0 | 154,047 (1.540) | fits |
| backlog-adp@blank-aged1-7 | 749 | 0 | 153,047 (1.530) | fits |
| backlog-adp@program-aged2-0 | 854 | 0 | 153,124 (1.531) | fits |
| backlog-adp@program-aged2-1 | 861 | 0 | 153,501 (1.535) | fits |
| backlog-adp@program-aged2-2 | 870 | 0 | 153,504 (1.535) | fits |
| backlog-adp@program-aged2-3 | 879 | 0 | 154,623 (1.546) | fits |
| backlog-adp@program-aged2-4 | 887 | 0 | 153,837 (1.538) | fits |
| backlog-adp@program-aged2-5 | 896 | 0 | 153,869 (1.539) | fits |
| backlog-adp@program-aged2-6 | 907 | 0 | 156,501 (1.565) | fits |
| backlog-adp@program-aged2-7 | 915 | 0 | 153,278 (1.533) | fits |
| backlog-adp@program-aged1-0 | 783 | 0 | 154,071 (1.541) | fits |
| backlog-adp@program-aged1-1 | 792 | 0 | 153,248 (1.532) | fits |
| backlog-adp@program-aged1-2 | 799 | 0 | 153,527 (1.535) | fits |
| backlog-adp@program-aged1-3 | 808 | 0 | 153,462 (1.535) | fits |
| backlog-adp@program-aged1-4 | 816 | 0 | 155,447 (1.554) | fits |
| backlog-adp@program-aged1-5 | 825 | 0 | 153,635 (1.536) | fits |
| backlog-adp@program-aged1-6 | 834 | 0 | 153,777 (1.538) | fits |
| backlog-adp@program-aged1-7 | 843 | 0 | 152,488 (1.525) | fits |
| backlog-adp@verify-aged2-0 | 949 | 0 | 154,254 (1.543) | fits |
| backlog-adp@verify-aged2-1 | 958 | 0 | 154,129 (1.541) | fits |
| backlog-adp@verify-aged2-2 | 967 | 0 | 153,960 (1.540) | fits |
| backlog-adp@verify-aged2-3 | 976 | 0 | 154,155 (1.542) | fits |
| backlog-adp@verify-aged2-4 | 984 | 0 | 153,423 (1.534) | fits |
| backlog-adp@verify-aged2-5 | 995 | 0 | 150,216 (1.502) | fits |
| backlog-adp@verify-aged2-6 | 1002 | 0 | 153,381 (1.534) | fits |
| backlog-adp@verify-aged2-7 | 1011 | 0 | 153,092 (1.531) | fits |
| backlog-adp@verify-aged1-0 | 879 | 0 | 153,436 (1.534) | fits |
| backlog-adp@verify-aged1-1 | 886 | 0 | 154,039 (1.540) | fits |
| backlog-adp@verify-aged1-2 | 895 | 0 | 154,000 (1.540) | fits |
| backlog-adp@verify-aged1-3 | 904 | 0 | 154,770 (1.548) | fits |
| backlog-adp@verify-aged1-4 | 912 | 0 | 154,357 (1.544) | fits |
| backlog-adp@verify-aged1-5 | 921 | 0 | 154,442 (1.544) | fits |
| backlog-adp@verify-aged1-6 | 932 | 0 | 156,167 (1.562) | fits |
| backlog-adp@verify-aged1-7 | 940 | 0 | 153,500 (1.535) | fits |
| adp-advertise | 591 | 0 | 66,016 (0.660) | fits |
| save-held | 1195 | 0 | 156,913 (1.569) | fits |
| save-starved | 29035 | 0 | 156,296 (1.563) | fits |
| acmp-noresp | 2015 | 0 | 66,016 (0.660) | fits |
| save | 602 | 0 | 66,016 (0.660) | fits |
| srp | 284 | 0 | 96,033 (0.960) | fits |
| backlog | 282 | 0 | 155,766 (1.558) | fits |
| backlog-adp | 307 | 0 | 154,682 (1.547) | fits |
| backlog-adp-refill | 321 | 0 | 154,682 (1.547) | fits |
| backlog-owed | 302 | 0 | 158,371 (1.584) | fits |
| acmp-disc | 932 | 0 | 66,016 (0.660) | fits |
| maap | 172 | 0 | 66,016 (0.660) | fits |
| adp-link | 87 | 0 | 66,016 (0.660) | fits |
| adp-gm | 86 | 0 | 66,016 (0.660) | fits |
| adp-discover | 86 | 0 | 66,016 (0.660) | fits |
| control | 86 | 0 | 66,016 (0.660) | fits |
| aecp-fanout | 109 | 0 | 66,016 (0.660) | fits |
| acmp-cmd | 82 | 0 | 66,016 (0.660) | fits |
| aecp | 109 | 0 | 66,016 (0.660) | fits |
| fixture | 150 | 0 | 81,638 (0.816) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 8.972 (20) | 11.028 |
| backlog-adp@blank-aged2-1 | 2 | none | +9.030 ms, 75,901 (0.759 ms), read-back | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 9.018 (20) | 10.982 |
| backlog-adp@blank-aged2-2 | 2 | none | none | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 9.823 (20) | 10.177 |
| backlog-adp@blank-aged2-3 | 2 | none | none | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 9.780 (20) | 10.220 |
| backlog-adp@blank-aged2-4 | 2 | none | none | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 9.794 (20) | 10.206 |
| backlog-adp@blank-aged2-5 | 2 | +6.067 ms, 76,065 (0.761 ms), read-back | none | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 9.787 (20) | 10.213 |
| backlog-adp@blank-aged2-6 | 2 | +4.592 ms, 76,065 (0.761 ms), read-back | none | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 9.656 (20) | 10.344 |
| backlog-adp@blank-aged2-7 | 2 | none | none | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 9.781 (20) | 10.219 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 8.861 (20) | 11.139 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 8.866 (20) | 11.134 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 9.983 (20) | 10.017 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 9.976 (20) | 10.024 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 9.724 (20) | 10.276 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 9.862 (20) | 10.138 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 9.716 (20) | 10.284 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 9.929 (20) | 10.071 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 8.924 (20) | 11.076 |
| backlog-adp@program-aged2-1 | 2 | none | +9.028 ms, 79,347 (0.793 ms), issue | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 8.724 (20) | 11.276 |
| backlog-adp@program-aged2-2 | 2 | +8.810 ms, 79,619 (0.796 ms), issue | none | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 9.872 (20) | 10.128 |
| backlog-adp@program-aged2-3 | 2 | +7.393 ms, 79,714 (0.797 ms), issue | none | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 9.885 (20) | 10.115 |
| backlog-adp@program-aged2-4 | 2 | +5.965 ms, 79,782 (0.798 ms), issue | none | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 9.705 (20) | 10.295 |
| backlog-adp@program-aged2-5 | 2 | +4.601 ms, 79,782 (0.798 ms), issue | none | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 9.702 (20) | 10.298 |
| backlog-adp@program-aged2-6 | 2 | +4.622 ms, 79,999 (0.800 ms), issue | none | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 9.693 (20) | 10.307 |
| backlog-adp@program-aged2-7 | 2 | +2.976 ms, 79,572 (0.796 ms), issue | none | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 9.884 (20) | 10.116 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 8.923 (20) | 11.077 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 9.093 (20) | 10.907 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 9.070 (20) | 10.930 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 9.164 (20) | 10.836 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 8.968 (20) | 11.032 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 8.969 (20) | 11.031 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 8.980 (20) | 11.020 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 9.078 (20) | 10.922 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 8.909 (20) | 11.091 |
| backlog-adp@verify-aged2-1 | 2 | none | +9.098 ms, 76,437 (0.764 ms), read-back | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 8.899 (20) | 11.101 |
| backlog-adp@verify-aged2-2 | 2 | +8.931 ms, 76,794 (0.768 ms), read-back | none | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 9.964 (20) | 10.036 |
| backlog-adp@verify-aged2-3 | 2 | +7.514 ms, 76,889 (0.769 ms), read-back | none | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 9.975 (20) | 10.025 |
| backlog-adp@verify-aged2-4 | 2 | +6.073 ms, 76,884 (0.769 ms), read-back | none | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 9.838 (20) | 10.162 |
| backlog-adp@verify-aged2-5 | 2 | +4.674 ms, 76,926 (0.769 ms), read-back | none | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 10.008 (20) | 9.992 |
| backlog-adp@verify-aged2-6 | 2 | +4.423 ms, 76,747 (0.767 ms), read-back | none | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 9.885 (20) | 10.115 |
| backlog-adp@verify-aged2-7 | 2 | +4.421 ms, 76,652 (0.767 ms), read-back | none | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 9.885 (20) | 10.115 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 8.951 (20) | 11.049 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 8.839 (20) | 11.161 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 9.090 (20) | 10.910 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 9.103 (20) | 10.897 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 8.929 (20) | 11.071 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 8.916 (20) | 11.084 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 8.896 (20) | 11.104 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 9.091 (20) | 10.909 |

Least margin over the aged windows: 9.992 ms, `backlog-adp@verify-aged2-5.service.aecp.last.if0` at 10.008 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.307 | 6,070 | 102 | 2 | 30.845 | yes | within |
| save-held | 2018.773 | 4,070 | 102 | - | 14.283 | no | within |
| save-starved | 4048.763 | 4,070 | 102 | - | 31.712 | yes | within |
| save | 2019.133 | 4,070 | 102 | - | 10.873 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 93,707 (0.937) | 77,812 (0.778) |
| save-second | 520 | 79,480 (0.795) | 77,510 (0.775) |
| backlog-adp@blank-0 | 299 | 88,269 (0.883) | 75,487 (0.755) |
| backlog-adp@blank-1 | 299 | 88,587 (0.886) | 75,432 (0.754) |
| backlog-adp@blank-2 | 299 | 88,960 (0.890) | 75,737 (0.757) |
| backlog-adp@blank-3 | 299 | 88,997 (0.890) | 75,749 (0.757) |
| backlog-adp@blank-4 | 299 | 88,857 (0.889) | 75,737 (0.757) |
| backlog-adp@blank-5 | 299 | 88,992 (0.890) | 75,673 (0.757) |
| backlog-adp@blank-6 | 299 | 88,847 (0.888) | 75,717 (0.757) |
| backlog-adp@blank-7 | 299 | 88,911 (0.889) | 75,686 (0.757) |
| backlog-adp@program-0 | 328 | 93,201 (0.932) | 78,137 (0.781) |
| backlog-adp@program-1 | 328 | 93,201 (0.932) | 78,573 (0.786) |
| backlog-adp@program-2 | 328 | 93,201 (0.932) | 78,573 (0.786) |
| backlog-adp@program-3 | 328 | 93,201 (0.932) | 78,368 (0.784) |
| backlog-adp@program-4 | 329 | 93,201 (0.932) | 77,772 (0.778) |
| backlog-adp@program-5 | 329 | 93,201 (0.932) | 77,772 (0.778) |
| backlog-adp@program-6 | 329 | 93,201 (0.932) | 77,772 (0.778) |
| backlog-adp@program-7 | 329 | 93,201 (0.932) | 77,772 (0.778) |
| backlog-adp@verify-0 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-1 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-2 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-3 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-4 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-5 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-6 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-7 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@blank-aged2-0 | 298 | 89,357 (0.894) | 75,857 (0.759) |
| backlog-adp@blank-aged2-1 | 297 | 75,901 (0.759) | 75,177 (0.752) |
| backlog-adp@blank-aged2-2 | 297 | 83,930 (0.839) | 75,340 (0.753) |
| backlog-adp@blank-aged2-3 | 297 | 84,538 (0.845) | 75,441 (0.754) |
| backlog-adp@blank-aged2-4 | 297 | 84,596 (0.846) | 75,441 (0.754) |
| backlog-adp@blank-aged2-5 | 297 | 76,065 (0.761) | 75,278 (0.753) |
| backlog-adp@blank-aged2-6 | 297 | 76,065 (0.761) | 75,278 (0.753) |
| backlog-adp@blank-aged2-7 | 297 | 83,631 (0.836) | 75,210 (0.752) |
| backlog-adp@blank-aged1-0 | 298 | 93,912 (0.939) | 75,603 (0.756) |
| backlog-adp@blank-aged1-1 | 297 | 94,182 (0.942) | 75,641 (0.756) |
| backlog-adp@blank-aged1-2 | 297 | 88,965 (0.890) | 75,547 (0.755) |
| backlog-adp@blank-aged1-3 | 297 | 88,677 (0.887) | 75,706 (0.757) |
| backlog-adp@blank-aged1-4 | 297 | 89,026 (0.890) | 75,464 (0.755) |
| backlog-adp@blank-aged1-5 | 297 | 88,784 (0.888) | 75,718 (0.757) |
| backlog-adp@blank-aged1-6 | 297 | 88,904 (0.889) | 75,464 (0.755) |
| backlog-adp@blank-aged1-7 | 298 | 88,781 (0.888) | 75,603 (0.756) |
| backlog-adp@program-aged2-0 | 327 | 93,201 (0.932) | 78,712 (0.787) |
| backlog-adp@program-aged2-1 | 326 | 93,201 (0.932) | 77,905 (0.779) |
| backlog-adp@program-aged2-2 | 326 | 93,201 (0.932) | 77,934 (0.779) |
| backlog-adp@program-aged2-3 | 326 | 93,201 (0.932) | 77,946 (0.779) |
| backlog-adp@program-aged2-4 | 326 | 93,201 (0.932) | 78,114 (0.781) |
| backlog-adp@program-aged2-5 | 326 | 93,201 (0.932) | 78,114 (0.781) |
| backlog-adp@program-aged2-6 | 326 | 93,201 (0.932) | 78,442 (0.784) |
| backlog-adp@program-aged2-7 | 326 | 93,201 (0.932) | 77,804 (0.778) |
| backlog-adp@program-aged1-0 | 327 | 93,201 (0.932) | 78,368 (0.784) |
| backlog-adp@program-aged1-1 | 326 | 97,853 (0.979) | 78,125 (0.781) |
| backlog-adp@program-aged1-2 | 326 | 93,201 (0.932) | 78,403 (0.784) |
| backlog-adp@program-aged1-3 | 326 | 93,201 (0.932) | 78,573 (0.786) |
| backlog-adp@program-aged1-4 | 326 | 93,201 (0.932) | 78,229 (0.782) |
| backlog-adp@program-aged1-5 | 326 | 93,201 (0.932) | 78,229 (0.782) |
| backlog-adp@program-aged1-6 | 326 | 93,201 (0.932) | 78,229 (0.782) |
| backlog-adp@program-aged1-7 | 326 | 93,201 (0.932) | 78,368 (0.784) |
| backlog-adp@verify-aged2-0 | 356 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-aged2-1 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-aged2-2 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-aged2-3 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-aged2-4 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-aged2-5 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-aged2-6 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-aged2-7 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-aged1-0 | 356 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-aged1-1 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-aged1-2 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-aged1-3 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-aged1-4 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-aged1-5 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-aged1-6 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| backlog-adp@verify-aged1-7 | 355 | 93,201 (0.932) | 77,812 (0.778) |
| adp-advertise | 578 | 19,237 (0.192) | 1,867 (0.019) |
| save-held | 722 | 93,322 (0.933) | 78,082 (0.781) |
| save-starved | 418 | 80,000 (0.800) | 77,840 (0.778) |
| acmp-noresp | 615 | 93,258 (0.933) | 77,812 (0.778) |
| save | 585 | 92,825 (0.928) | 77,776 (0.778) |
| srp | 271 | 19,237 (0.192) | 1,867 (0.019) |
| backlog | 265 | 19,237 (0.192) | 1,867 (0.019) |
| backlog-adp | 271 | 19,237 (0.192) | 2,389 (0.024) |
| backlog-adp-refill | 274 | 19,237 (0.192) | 2,154 (0.022) |
| backlog-owed | 276 | 19,237 (0.192) | 2,005 (0.020) |
| acmp-disc | 305 | 93,323 (0.933) | 77,812 (0.778) |
| maap | 163 | 19,237 (0.192) | 1,867 (0.019) |
| adp-link | 80 | 19,100 (0.191) | 1,867 (0.019) |
| adp-gm | 80 | 19,100 (0.191) | 1,867 (0.019) |
| adp-discover | 80 | 19,100 (0.191) | 1,867 (0.019) |
| control | 80 | 19,100 (0.191) | 1,867 (0.019) |
| aecp-fanout | 79 | 19,100 (0.191) | 2,053 (0.021) |
| acmp-cmd | 65 | 19,100 (0.191) | 1,867 (0.019) |
| aecp | 79 | 19,100 (0.191) | 1,867 (0.019) |
| fixture | 54 | 14,608 (0.146) | 1,985 (0.020) |

Longest pass that carries a step: 97,853 CPU cycles (0.979 ms), backlog-adp@program-aged1-1; longest step: 78,712 (0.787 ms), backlog-adp@program-aged2-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 13,229 | 0.132 | 20 | 20 | fits | 33,365 | 19 (14) | 0.898 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 736,023 | 7.360 | 20 | 20 | fits | 146,005 | 181 | 0.557 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 212,867 | 2.129 | 20 | 200 | fits | 144,543 | 201 | 0.526 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 783,825 | 7.838 | 20 | 200 | fits | 146,005 | 181 | 0.557 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 213,791 | 2.138 | 20 | 20 | fits | 144,543 | 201 | 0.526 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 941,157 | 9.412 | 20 | 20 | fits | 147,990 | 118 | 0.536 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 217,431 | 2.174 | 20 | 24 | fits | 144,543 | 201 | 0.526 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 971,974 | 9.720 | 20 | 24 | fits | 27,331 | 18 | 0.681 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 216,375 | 2.164 | 20 | 50 | fits | 144,543 | 201 | 0.526 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 787,553 | 7.876 | 20 | 50 | fits | 146,005 | 181 | 0.557 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 370,343 | 3.703 | 20 | 20 | fits | 154,430 | 86 | 0.598 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 639,436 | 6.394 | 20 | 20 | fits | 124,874 | 44 | 0.444 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 684,047 | 6.840 | 20 | 20 | fits | 149,072 | 187 | 0.565 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 141,243 | 1.412 | 20 | 200 | fits | 144,181 | 201 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 724,938 | 7.249 | 20 | 200 | fits | 149,072 | 187 | 0.565 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 142,167 | 1.422 | 20 | 20 | fits | 144,181 | 201 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 868,500 | 8.685 | 20 | 20 | fits | 142,858 | 112 | 0.516 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 145,807 | 1.458 | 20 | 24 | fits | 144,181 | 201 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 907,992 | 9.080 | 20 | 24 | fits | 36,006 | 27 | 0.680 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 144,751 | 1.448 | 20 | 50 | fits | 144,181 | 201 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 728,666 | 7.287 | 20 | 50 | fits | 149,072 | 187 | 0.565 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 298,803 | 2.988 | 20 | 20 | fits | 154,514 | 86 | 0.599 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 568,076 | 5.681 | 20 | 20 | fits | 125,108 | 45 | 0.448 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 694,395 | 6.944 | 20 | 20 | fits | 145,243 | 180 | 0.554 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 149,233 | 1.492 | 20 | 200 | fits | 144,181 | 201 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 734,988 | 7.350 | 20 | 200 | fits | 145,243 | 180 | 0.554 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 150,157 | 1.502 | 20 | 20 | fits | 144,181 | 201 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 890,651 | 8.907 | 20 | 20 | fits | 154,959 | 119 | 0.540 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 153,797 | 1.538 | 20 | 24 | fits | 144,181 | 201 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 921,576 | 9.216 | 20 | 24 | fits | 27,439 | 18 | 0.683 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 152,741 | 1.527 | 20 | 50 | fits | 144,181 | 201 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 738,716 | 7.387 | 20 | 50 | fits | 145,243 | 180 | 0.554 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 306,793 | 3.068 | 20 | 20 | fits | 154,514 | 86 | 0.599 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 591,361 | 5.914 | 20 | 20 | fits | 130,585 | 51 | 0.534 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 716,434 | 7.164 | 20 | 20 | fits | 151,022 | 165 | 0.583 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 149,906 | 1.499 | 20 | 200 | fits | 150,163 | 223 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 742,150 | 7.421 | 20 | 200 | fits | 151,022 | 165 | 0.583 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 150,830 | 1.508 | 20 | 20 | fits | 150,163 | 223 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 885,475 | 8.855 | 20 | 20 | fits | 142,621 | 113 | 0.510 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 154,470 | 1.545 | 20 | 24 | fits | 150,163 | 223 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 916,217 | 9.162 | 20 | 24 | fits | 27,256 | 18 | 0.675 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 153,414 | 1.534 | 20 | 50 | fits | 150,163 | 223 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 745,878 | 7.459 | 20 | 50 | fits | 151,022 | 165 | 0.583 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 307,760 | 3.078 | 20 | 20 | fits | 154,808 | 87 | 0.599 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 592,744 | 5.927 | 20 | 20 | fits | 125,144 | 44 | 0.454 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 255,077 | 2.551 | 20 | 20 | fits | 149,249 | 207 | 0.529 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 145,959 | 1.460 | 20 | 200 | fits | 151,525 | 186 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 294,592 | 2.946 | 20 | 200 | fits | 149,249 | 207 | 0.529 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 146,883 | 1.469 | 20 | 20 | fits | 151,525 | 186 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 447,484 | 4.475 | 20 | 20 | fits | 143,823 | 146 | 0.525 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 150,523 | 1.505 | 20 | 24 | fits | 151,525 | 186 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 900,506 | 9.005 | 20 | 24 | fits | 28,468 | 18 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 149,467 | 1.495 | 20 | 50 | fits | 151,525 | 186 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 298,320 | 2.983 | 20 | 50 | fits | 149,249 | 207 | 0.529 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 603,503 | 6.035 | 20 | 20 | fits | 153,061 | 48 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 869,464 | 8.695 | 20 | 20 | fits | 124,656 | 44 | 0.440 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 270,352 | 2.704 | 20 | 20 | fits | 149,771 | 206 | 0.534 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 151,822 | 1.518 | 20 | 200 | fits | 149,398 | 224 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 310,031 | 3.100 | 20 | 200 | fits | 149,771 | 206 | 0.534 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 152,746 | 1.527 | 20 | 20 | fits | 149,398 | 224 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 878,210 | 8.782 | 20 | 20 | fits | 145,448 | 109 | 0.533 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 156,386 | 1.564 | 20 | 24 | fits | 149,398 | 224 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 908,683 | 9.087 | 20 | 24 | fits | 26,987 | 18 | 0.673 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 155,330 | 1.553 | 20 | 50 | fits | 149,398 | 224 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 313,759 | 3.138 | 20 | 50 | fits | 149,771 | 206 | 0.534 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 467,398 | 4.674 | 20 | 20 | fits | 153,705 | 48 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 733,674 | 7.337 | 20 | 20 | fits | 124,630 | 44 | 0.438 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 669,914 | 6.699 | 20 | 20 | fits | 145,847 | 181 | 0.557 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 139,324 | 1.393 | 20 | 200 | fits | 143,942 | 201 | 0.523 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 717,726 | 7.177 | 20 | 200 | fits | 145,847 | 181 | 0.557 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 140,248 | 1.402 | 20 | 20 | fits | 143,942 | 201 | 0.523 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 874,778 | 8.748 | 20 | 20 | fits | 147,710 | 118 | 0.536 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 143,888 | 1.439 | 20 | 24 | fits | 143,942 | 201 | 0.523 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 905,743 | 9.057 | 20 | 24 | fits | 27,479 | 18 | 0.686 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 142,832 | 1.428 | 20 | 50 | fits | 143,942 | 201 | 0.523 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 721,454 | 7.215 | 20 | 50 | fits | 145,847 | 181 | 0.557 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 296,805 | 2.968 | 20 | 20 | fits | 154,435 | 86 | 0.598 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 573,495 | 5.735 | 20 | 20 | fits | 135,540 | 48 | 0.424 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 733,397 | 7.334 | 20 | 20 | fits | 149,924 | 132 | 0.567 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 147,314 | 1.473 | 20 | 200 | fits | 143,942 | 201 | 0.523 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 875,279 | 8.753 | 20 | 200 | fits | 149,924 | 132 | 0.567 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 148,238 | 1.482 | 20 | 20 | fits | 143,942 | 201 | 0.523 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 875,983 | 8.760 | 20 | 20 | fits | 149,924 | 132 | 0.567 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 151,878 | 1.519 | 20 | 24 | fits | 143,942 | 201 | 0.523 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 919,940 | 9.199 | 20 | 24 | fits | 40,471 | 30 | 0.575 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 150,822 | 1.508 | 20 | 50 | fits | 143,942 | 201 | 0.523 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 879,007 | 8.790 | 20 | 50 | fits | 149,924 | 132 | 0.567 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 453,371 | 4.534 | 20 | 20 | fits | 153,118 | 48 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 726,971 | 7.270 | 20 | 20 | fits | 119,826 | 47 | 0.555 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 709,889 | 7.099 | 20 | 20 | fits | 147,101 | 166 | 0.554 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 149,140 | 1.491 | 20 | 200 | fits | 149,238 | 223 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 736,262 | 7.363 | 20 | 200 | fits | 147,101 | 166 | 0.554 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 150,064 | 1.501 | 20 | 20 | fits | 149,238 | 223 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 884,969 | 8.850 | 20 | 20 | fits | 148,003 | 116 | 0.501 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 153,704 | 1.537 | 20 | 24 | fits | 149,238 | 223 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 888,455 | 8.885 | 20 | 24 | fits | 148,003 | 116 | 0.501 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 152,648 | 1.526 | 20 | 50 | fits | 149,238 | 223 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 739,990 | 7.400 | 20 | 50 | fits | 147,101 | 166 | 0.554 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 306,013 | 3.060 | 20 | 20 | fits | 153,827 | 86 | 0.596 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 590,777 | 5.908 | 20 | 20 | fits | 130,642 | 51 | 0.535 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 767,376 | 7.674 | 20 | 20 | fits | 154,708 | 116 | 0.590 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 152,220 | 1.522 | 20 | 200 | fits | 149,637 | 220 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 881,626 | 8.816 | 20 | 200 | fits | 154,708 | 116 | 0.590 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 153,144 | 1.531 | 20 | 20 | fits | 149,637 | 220 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 882,330 | 8.823 | 20 | 20 | fits | 154,708 | 116 | 0.590 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 156,784 | 1.568 | 20 | 24 | fits | 149,637 | 220 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 913,732 | 9.137 | 20 | 24 | fits | 27,916 | 18 | 0.697 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 155,728 | 1.557 | 20 | 50 | fits | 149,637 | 220 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 318,160 | 3.182 | 20 | 50 | fits | 154,121 | 208 | 0.501 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 470,614 | 4.706 | 20 | 20 | fits | 152,520 | 48 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 728,534 | 7.285 | 20 | 20 | fits | 113,886 | 40 | 0.458 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 680,531 | 6.805 | 20 | 20 | fits | 145,137 | 181 | 0.553 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 143,789 | 1.438 | 20 | 200 | fits | 144,323 | 201 | 0.526 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 721,222 | 7.212 | 20 | 200 | fits | 145,137 | 181 | 0.553 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 144,713 | 1.447 | 20 | 20 | fits | 144,323 | 201 | 0.526 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 878,361 | 8.784 | 20 | 20 | fits | 147,857 | 118 | 0.535 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 148,353 | 1.484 | 20 | 24 | fits | 144,323 | 201 | 0.526 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 909,115 | 9.091 | 20 | 24 | fits | 27,268 | 18 | 0.679 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 147,297 | 1.473 | 20 | 50 | fits | 144,323 | 201 | 0.526 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 724,950 | 7.250 | 20 | 50 | fits | 145,137 | 181 | 0.553 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 300,848 | 3.008 | 20 | 20 | fits | 154,013 | 86 | 0.597 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 577,701 | 5.777 | 20 | 20 | fits | 132,620 | 50 | 0.499 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 271,583 | 2.716 | 20 | 20 | fits | 146,114 | 196 | 0.560 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 152,850 | 1.528 | 20 | 200 | fits | 150,703 | 223 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 298,348 | 2.983 | 20 | 200 | fits | 146,114 | 196 | 0.560 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 153,774 | 1.538 | 20 | 20 | fits | 150,703 | 223 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 872,850 | 8.729 | 20 | 20 | fits | 144,184 | 112 | 0.522 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 157,414 | 1.574 | 20 | 24 | fits | 150,703 | 223 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 916,377 | 9.164 | 20 | 24 | fits | 40,041 | 30 | 0.561 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 156,358 | 1.564 | 20 | 50 | fits | 150,703 | 223 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 302,076 | 3.021 | 20 | 50 | fits | 146,114 | 196 | 0.560 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 455,432 | 4.554 | 20 | 20 | fits | 153,422 | 49 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 729,578 | 7.296 | 20 | 20 | fits | 114,234 | 40 | 0.471 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 343,440 | 3.434 | 20 | 20 | fits | 153,963 | 155 | 0.545 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 138,597 | 1.386 | 20 | 200 | fits | 145,185 | 177 | 0.537 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 451,063 | 4.511 | 20 | 200 | fits | 153,963 | 155 | 0.545 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 139,521 | 1.395 | 20 | 20 | fits | 145,185 | 177 | 0.537 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 451,767 | 4.518 | 20 | 20 | fits | 153,963 | 155 | 0.545 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 143,161 | 1.432 | 20 | 24 | fits | 145,185 | 177 | 0.537 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 897,185 | 8.972 | 20 | 24 | fits | 28,768 | 18 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 142,105 | 1.421 | 20 | 50 | fits | 145,185 | 177 | 0.537 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 291,623 | 2.916 | 20 | 50 | fits | 149,914 | 207 | 0.508 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 607,778 | 6.078 | 20 | 20 | fits | 153,053 | 48 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 865,843 | 8.658 | 20 | 20 | fits | 113,964 | 40 | 0.460 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 682,913 | 6.829 | 20 | 20 | fits | 152,522 | 168 | 0.549 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 146,602 | 1.466 | 20 | 200 | fits | 150,530 | 223 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 723,645 | 7.236 | 20 | 200 | fits | 152,522 | 168 | 0.549 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 147,526 | 1.475 | 20 | 20 | fits | 150,530 | 223 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 869,151 | 8.692 | 20 | 20 | fits | 144,802 | 115 | 0.552 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 151,166 | 1.512 | 20 | 24 | fits | 150,530 | 223 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 909,507 | 9.095 | 20 | 24 | fits | 28,035 | 19 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 150,110 | 1.501 | 20 | 50 | fits | 150,530 | 223 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 727,373 | 7.274 | 20 | 50 | fits | 152,522 | 168 | 0.549 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 303,583 | 3.036 | 20 | 20 | fits | 153,935 | 86 | 0.596 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 572,739 | 5.727 | 20 | 20 | fits | 124,874 | 44 | 0.444 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 714,085 | 7.141 | 20 | 20 | fits | 151,156 | 173 | 0.564 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 147,772 | 1.478 | 20 | 200 | fits | 149,019 | 223 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 740,787 | 7.408 | 20 | 200 | fits | 151,156 | 173 | 0.564 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 148,696 | 1.487 | 20 | 20 | fits | 149,019 | 223 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 889,519 | 8.895 | 20 | 20 | fits | 148,028 | 116 | 0.501 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 152,336 | 1.523 | 20 | 24 | fits | 149,019 | 223 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 893,005 | 8.930 | 20 | 24 | fits | 148,028 | 116 | 0.501 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 151,280 | 1.513 | 20 | 50 | fits | 149,019 | 223 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 744,515 | 7.445 | 20 | 50 | fits | 151,156 | 173 | 0.564 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 304,683 | 3.047 | 20 | 20 | fits | 153,865 | 86 | 0.596 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 581,819 | 5.818 | 20 | 20 | fits | 132,854 | 51 | 0.501 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 778,319 | 7.783 | 20 | 20 | fits | 155,825 | 121 | 0.556 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 150,843 | 1.508 | 20 | 200 | fits | 149,409 | 219 | 0.524 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 882,712 | 8.827 | 20 | 200 | fits | 155,825 | 121 | 0.556 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 151,767 | 1.518 | 20 | 20 | fits | 149,409 | 219 | 0.524 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 883,416 | 8.834 | 20 | 20 | fits | 155,825 | 121 | 0.556 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 155,407 | 1.554 | 20 | 24 | fits | 149,409 | 219 | 0.524 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 914,747 | 9.147 | 20 | 24 | fits | 27,845 | 18 | 0.695 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 154,351 | 1.544 | 20 | 50 | fits | 149,409 | 219 | 0.524 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 304,676 | 3.047 | 20 | 50 | fits | 150,721 | 200 | 0.535 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 459,367 | 4.594 | 20 | 20 | fits | 145,777 | 50 | 0.646 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 728,503 | 7.285 | 20 | 20 | fits | 124,796 | 44 | 0.442 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 706,690 | 7.067 | 20 | 20 | fits | 145,212 | 181 | 0.553 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 176,905 | 1.769 | 20 | 200 | fits | 144,773 | 201 | 0.528 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 747,198 | 7.472 | 20 | 200 | fits | 145,212 | 181 | 0.553 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 177,829 | 1.778 | 20 | 20 | fits | 144,773 | 201 | 0.528 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 904,337 | 9.043 | 20 | 20 | fits | 147,857 | 118 | 0.535 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 181,469 | 1.815 | 20 | 24 | fits | 144,773 | 201 | 0.528 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 935,091 | 9.351 | 20 | 24 | fits | 27,268 | 18 | 0.679 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 180,413 | 1.804 | 20 | 50 | fits | 144,773 | 201 | 0.528 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 750,926 | 7.509 | 20 | 50 | fits | 145,212 | 181 | 0.553 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 334,441 | 3.344 | 20 | 20 | fits | 154,490 | 86 | 0.598 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 603,602 | 6.036 | 20 | 20 | fits | 124,874 | 44 | 0.444 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 711,368 | 7.114 | 20 | 20 | fits | 153,077 | 177 | 0.561 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 150,312 | 1.503 | 20 | 200 | fits | 149,527 | 219 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 737,713 | 7.377 | 20 | 200 | fits | 153,077 | 177 | 0.561 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 151,236 | 1.512 | 20 | 20 | fits | 149,527 | 219 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 884,977 | 8.850 | 20 | 20 | fits | 146,560 | 117 | 0.492 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 154,876 | 1.549 | 20 | 24 | fits | 149,527 | 219 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 888,463 | 8.885 | 20 | 24 | fits | 146,560 | 117 | 0.492 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 153,820 | 1.538 | 20 | 50 | fits | 149,527 | 219 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 741,441 | 7.414 | 20 | 50 | fits | 153,077 | 177 | 0.561 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 307,573 | 3.076 | 20 | 20 | fits | 154,215 | 86 | 0.594 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 576,846 | 5.768 | 20 | 20 | fits | 125,108 | 45 | 0.448 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 678,747 | 6.787 | 20 | 20 | fits | 146,006 | 180 | 0.558 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 139,951 | 1.400 | 20 | 200 | fits | 144,520 | 201 | 0.527 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 726,583 | 7.266 | 20 | 200 | fits | 146,006 | 180 | 0.558 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 140,875 | 1.409 | 20 | 20 | fits | 144,520 | 201 | 0.527 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 882,539 | 8.825 | 20 | 20 | fits | 155,252 | 119 | 0.542 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 144,515 | 1.445 | 20 | 24 | fits | 144,520 | 201 | 0.527 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 913,171 | 9.132 | 20 | 24 | fits | 27,146 | 18 | 0.675 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 143,459 | 1.435 | 20 | 50 | fits | 144,520 | 201 | 0.527 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 730,311 | 7.303 | 20 | 50 | fits | 146,006 | 180 | 0.558 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 297,571 | 2.976 | 20 | 20 | fits | 154,574 | 86 | 0.599 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 582,193 | 5.822 | 20 | 20 | fits | 130,571 | 51 | 0.534 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 699,791 | 6.998 | 20 | 20 | fits | 151,928 | 164 | 0.588 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 147,891 | 1.479 | 20 | 200 | fits | 144,520 | 201 | 0.527 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 740,836 | 7.408 | 20 | 200 | fits | 151,928 | 164 | 0.588 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 148,815 | 1.488 | 20 | 20 | fits | 144,520 | 201 | 0.527 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 892,496 | 8.925 | 20 | 20 | fits | 150,956 | 133 | 0.522 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 152,455 | 1.525 | 20 | 24 | fits | 144,520 | 201 | 0.527 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 923,417 | 9.234 | 20 | 24 | fits | 27,435 | 18 | 0.683 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 151,399 | 1.514 | 20 | 50 | fits | 144,520 | 201 | 0.527 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 895,520 | 8.955 | 20 | 50 | fits | 150,956 | 133 | 0.522 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 305,745 | 3.057 | 20 | 20 | fits | 154,808 | 87 | 0.600 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 590,524 | 5.905 | 20 | 20 | fits | 125,144 | 44 | 0.454 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 260,018 | 2.600 | 20 | 20 | fits | 150,250 | 205 | 0.537 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 142,598 | 1.426 | 20 | 200 | fits | 144,581 | 202 | 0.527 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 300,856 | 3.009 | 20 | 200 | fits | 150,250 | 205 | 0.537 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 143,522 | 1.435 | 20 | 20 | fits | 144,581 | 202 | 0.527 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 876,048 | 8.760 | 20 | 20 | fits | 153,029 | 133 | 0.537 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 147,162 | 1.472 | 20 | 24 | fits | 144,581 | 202 | 0.527 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 906,832 | 9.068 | 20 | 24 | fits | 27,298 | 18 | 0.683 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 146,106 | 1.461 | 20 | 50 | fits | 144,581 | 202 | 0.527 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 879,072 | 8.791 | 20 | 50 | fits | 153,029 | 133 | 0.537 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 457,829 | 4.578 | 20 | 20 | fits | 153,311 | 48 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 723,931 | 7.239 | 20 | 20 | fits | 124,630 | 44 | 0.438 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 252,779 | 2.528 | 20 | 20 | fits | 149,347 | 205 | 0.531 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 144,849 | 1.448 | 20 | 200 | fits | 151,213 | 223 | 0.524 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 293,580 | 2.936 | 20 | 200 | fits | 149,347 | 205 | 0.531 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 145,773 | 1.458 | 20 | 20 | fits | 151,213 | 223 | 0.524 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 859,717 | 8.597 | 20 | 20 | fits | 145,030 | 113 | 0.529 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 149,413 | 1.494 | 20 | 24 | fits | 151,213 | 223 | 0.524 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 903,799 | 9.038 | 20 | 24 | fits | 31,725 | 25 | 0.722 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 148,357 | 1.484 | 20 | 50 | fits | 151,213 | 223 | 0.524 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 297,308 | 2.973 | 20 | 50 | fits | 149,347 | 205 | 0.531 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 446,617 | 4.466 | 20 | 20 | fits | 149,375 | 50 | 0.643 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 715,599 | 7.156 | 20 | 20 | fits | 124,874 | 44 | 0.444 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 697,853 | 6.979 | 20 | 20 | fits | 147,689 | 167 | 0.555 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 144,017 | 1.440 | 20 | 200 | fits | 149,164 | 223 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 724,275 | 7.243 | 20 | 200 | fits | 147,689 | 167 | 0.555 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 144,941 | 1.449 | 20 | 20 | fits | 149,164 | 223 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 885,821 | 8.858 | 20 | 20 | fits | 151,974 | 123 | 0.514 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 148,581 | 1.486 | 20 | 24 | fits | 149,164 | 223 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 889,307 | 8.893 | 20 | 24 | fits | 151,974 | 123 | 0.514 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 147,525 | 1.475 | 20 | 50 | fits | 149,164 | 223 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 728,003 | 7.280 | 20 | 50 | fits | 147,689 | 167 | 0.555 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 301,444 | 3.014 | 20 | 20 | fits | 154,381 | 86 | 0.597 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 578,202 | 5.782 | 20 | 20 | fits | 135,540 | 48 | 0.424 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 271,074 | 2.711 | 20 | 20 | fits | 145,452 | 197 | 0.556 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 151,957 | 1.520 | 20 | 200 | fits | 149,164 | 223 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 296,793 | 2.968 | 20 | 200 | fits | 145,452 | 197 | 0.556 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 152,881 | 1.529 | 20 | 20 | fits | 149,164 | 223 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 872,398 | 8.724 | 20 | 20 | fits | 145,497 | 109 | 0.533 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 156,521 | 1.565 | 20 | 24 | fits | 149,164 | 223 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 915,676 | 9.157 | 20 | 24 | fits | 39,792 | 30 | 0.554 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 155,465 | 1.555 | 20 | 50 | fits | 149,164 | 223 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 300,521 | 3.005 | 20 | 50 | fits | 145,452 | 197 | 0.556 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 453,966 | 4.540 | 20 | 20 | fits | 153,511 | 48 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 727,813 | 7.278 | 20 | 20 | fits | 119,983 | 47 | 0.557 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 254,455 | 2.545 | 20 | 20 | fits | 150,131 | 206 | 0.533 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 145,927 | 1.459 | 20 | 200 | fits | 153,227 | 221 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 295,442 | 2.954 | 20 | 200 | fits | 150,131 | 206 | 0.533 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 146,851 | 1.469 | 20 | 20 | fits | 153,227 | 221 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 866,371 | 8.664 | 20 | 20 | fits | 144,846 | 112 | 0.529 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 150,491 | 1.505 | 20 | 24 | fits | 153,227 | 221 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 897,245 | 8.972 | 20 | 24 | fits | 27,388 | 18 | 0.683 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 149,435 | 1.494 | 20 | 50 | fits | 153,227 | 221 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 299,170 | 2.992 | 20 | 50 | fits | 150,131 | 206 | 0.533 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 453,397 | 4.534 | 20 | 20 | fits | 145,572 | 50 | 0.639 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 722,437 | 7.224 | 20 | 20 | fits | 124,794 | 44 | 0.444 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 260,433 | 2.604 | 20 | 20 | fits | 150,076 | 205 | 0.538 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 142,545 | 1.425 | 20 | 200 | fits | 149,325 | 221 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 301,133 | 3.011 | 20 | 200 | fits | 150,076 | 205 | 0.538 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 143,469 | 1.435 | 20 | 20 | fits | 149,325 | 221 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 862,378 | 8.624 | 20 | 20 | fits | 144,471 | 111 | 0.531 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 147,109 | 1.471 | 20 | 24 | fits | 149,325 | 221 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 901,836 | 9.018 | 20 | 24 | fits | 35,972 | 27 | 0.683 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 146,053 | 1.461 | 20 | 50 | fits | 149,325 | 221 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 304,861 | 3.049 | 20 | 50 | fits | 150,076 | 205 | 0.538 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 450,046 | 4.500 | 20 | 20 | fits | 145,251 | 50 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 718,819 | 7.188 | 20 | 20 | fits | 124,794 | 44 | 0.444 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 248,706 | 2.487 | 20 | 20 | fits | 149,019 | 205 | 0.530 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 140,966 | 1.410 | 20 | 200 | fits | 149,909 | 221 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 289,369 | 2.894 | 20 | 200 | fits | 149,019 | 205 | 0.530 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 141,890 | 1.419 | 20 | 20 | fits | 149,909 | 221 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 849,937 | 8.499 | 20 | 20 | fits | 143,418 | 109 | 0.565 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 145,530 | 1.455 | 20 | 24 | fits | 149,909 | 221 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 982,282 | 9.823 | 20 | 24 | fits | 44,929 | 37 | 0.617 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 144,474 | 1.445 | 20 | 50 | fits | 149,909 | 221 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 293,097 | 2.931 | 20 | 50 | fits | 149,019 | 205 | 0.530 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 438,617 | 4.386 | 20 | 20 | fits | 145,586 | 50 | 0.639 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 707,431 | 7.074 | 20 | 20 | fits | 124,794 | 44 | 0.444 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 855,417 | 8.554 | 20 | 20 | fits | 146,237 | 116 | 0.580 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 141,528 | 1.415 | 20 | 200 | fits | 147,700 | 216 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 946,028 | 9.460 | 20 | 200 | fits | 146,237 | 116 | 0.580 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 142,452 | 1.425 | 20 | 20 | fits | 147,700 | 216 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 946,732 | 9.467 | 20 | 20 | fits | 146,237 | 116 | 0.580 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 146,092 | 1.461 | 20 | 24 | fits | 147,700 | 216 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 978,048 | 9.780 | 20 | 24 | fits | 27,830 | 18 | 0.695 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 145,036 | 1.450 | 20 | 50 | fits | 147,700 | 216 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 298,340 | 2.983 | 20 | 50 | fits | 153,700 | 208 | 0.494 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 450,656 | 4.507 | 20 | 20 | fits | 152,382 | 48 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 716,869 | 7.169 | 20 | 20 | fits | 122,088 | 47 | 0.523 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 273,871 | 2.739 | 20 | 20 | fits | 149,195 | 206 | 0.531 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 142,888 | 1.429 | 20 | 200 | fits | 149,060 | 220 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 291,467 | 2.915 | 20 | 200 | fits | 149,195 | 206 | 0.531 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 143,812 | 1.438 | 20 | 20 | fits | 149,060 | 220 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 948,695 | 9.487 | 20 | 20 | fits | 145,173 | 111 | 0.533 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 147,452 | 1.475 | 20 | 24 | fits | 149,060 | 220 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 979,382 | 9.794 | 20 | 24 | fits | 27,201 | 18 | 0.677 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 146,396 | 1.464 | 20 | 50 | fits | 149,060 | 220 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 295,195 | 2.952 | 20 | 50 | fits | 149,195 | 206 | 0.531 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 447,571 | 4.476 | 20 | 20 | fits | 152,442 | 48 | 0.599 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 804,434 | 8.044 | 20 | 20 | fits | 130,685 | 51 | 0.531 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 250,610 | 2.506 | 20 | 20 | fits | 149,260 | 205 | 0.530 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 142,671 | 1.427 | 20 | 200 | fits | 148,843 | 220 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 291,315 | 2.913 | 20 | 200 | fits | 149,260 | 205 | 0.530 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 143,595 | 1.436 | 20 | 20 | fits | 148,843 | 220 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 947,970 | 9.480 | 20 | 20 | fits | 144,744 | 111 | 0.530 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 147,235 | 1.472 | 20 | 24 | fits | 148,843 | 220 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 978,661 | 9.787 | 20 | 24 | fits | 27,205 | 18 | 0.679 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 146,179 | 1.462 | 20 | 50 | fits | 148,843 | 220 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 295,043 | 2.950 | 20 | 50 | fits | 149,260 | 205 | 0.530 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 448,212 | 4.482 | 20 | 20 | fits | 153,235 | 49 | 0.609 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 804,138 | 8.041 | 20 | 20 | fits | 125,122 | 45 | 0.451 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 778,088 | 7.781 | 20 | 20 | fits | 152,764 | 168 | 0.550 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 144,020 | 1.440 | 20 | 200 | fits | 148,562 | 220 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 818,726 | 8.187 | 20 | 200 | fits | 152,764 | 168 | 0.550 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 144,944 | 1.449 | 20 | 20 | fits | 148,562 | 220 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 962,127 | 9.621 | 20 | 20 | fits | 142,697 | 113 | 0.512 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 148,584 | 1.486 | 20 | 24 | fits | 148,562 | 220 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 965,613 | 9.656 | 20 | 24 | fits | 142,697 | 113 | 0.512 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 147,528 | 1.475 | 20 | 50 | fits | 148,562 | 220 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 822,454 | 8.225 | 20 | 50 | fits | 152,764 | 168 | 0.550 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 301,061 | 3.011 | 20 | 20 | fits | 153,995 | 87 | 0.597 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 667,578 | 6.676 | 20 | 20 | fits | 136,024 | 49 | 0.437 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 262,535 | 2.625 | 20 | 20 | fits | 145,362 | 198 | 0.556 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 143,403 | 1.434 | 20 | 200 | fits | 147,656 | 220 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 288,149 | 2.881 | 20 | 200 | fits | 145,362 | 198 | 0.556 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 144,327 | 1.443 | 20 | 20 | fits | 147,656 | 220 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 934,924 | 9.349 | 20 | 20 | fits | 145,678 | 109 | 0.534 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 147,967 | 1.480 | 20 | 24 | fits | 147,656 | 220 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 978,095 | 9.781 | 20 | 24 | fits | 39,685 | 30 | 0.554 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 146,911 | 1.469 | 20 | 50 | fits | 147,656 | 220 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 291,877 | 2.919 | 20 | 50 | fits | 145,362 | 198 | 0.556 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 521,139 | 5.211 | 20 | 20 | fits | 145,697 | 50 | 0.641 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 790,158 | 7.902 | 20 | 20 | fits | 124,794 | 44 | 0.444 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 709,623 | 7.096 | 20 | 20 | fits | 148,952 | 170 | 0.551 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 146,298 | 1.463 | 20 | 200 | fits | 147,678 | 216 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 735,465 | 7.355 | 20 | 200 | fits | 148,952 | 170 | 0.551 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 147,222 | 1.472 | 20 | 20 | fits | 147,678 | 216 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 882,585 | 8.826 | 20 | 20 | fits | 146,416 | 117 | 0.493 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 150,862 | 1.509 | 20 | 24 | fits | 147,678 | 216 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 886,071 | 8.861 | 20 | 24 | fits | 146,416 | 117 | 0.493 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 149,806 | 1.498 | 20 | 50 | fits | 147,678 | 216 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 739,193 | 7.392 | 20 | 50 | fits | 148,952 | 170 | 0.551 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 303,469 | 3.035 | 20 | 20 | fits | 154,125 | 86 | 0.593 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 588,129 | 5.881 | 20 | 20 | fits | 130,665 | 51 | 0.536 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 686,016 | 6.860 | 20 | 20 | fits | 148,032 | 167 | 0.558 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 147,942 | 1.479 | 20 | 200 | fits | 148,961 | 220 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 735,926 | 7.359 | 20 | 200 | fits | 148,032 | 167 | 0.558 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 148,866 | 1.489 | 20 | 20 | fits | 148,961 | 220 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 883,107 | 8.831 | 20 | 20 | fits | 146,477 | 118 | 0.493 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 152,506 | 1.525 | 20 | 24 | fits | 148,961 | 220 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 886,593 | 8.866 | 20 | 24 | fits | 146,477 | 118 | 0.493 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 151,450 | 1.514 | 20 | 50 | fits | 148,961 | 220 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 739,654 | 7.397 | 20 | 50 | fits | 148,032 | 167 | 0.558 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 305,036 | 3.050 | 20 | 20 | fits | 154,048 | 86 | 0.592 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 589,510 | 5.895 | 20 | 20 | fits | 130,570 | 51 | 0.535 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 686,837 | 6.868 | 20 | 20 | fits | 147,059 | 168 | 0.551 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 148,142 | 1.481 | 20 | 200 | fits | 148,800 | 220 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 735,432 | 7.354 | 20 | 200 | fits | 147,059 | 168 | 0.551 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 149,066 | 1.491 | 20 | 20 | fits | 148,800 | 220 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 881,558 | 8.816 | 20 | 20 | fits | 145,422 | 101 | 0.573 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 152,706 | 1.527 | 20 | 24 | fits | 148,800 | 220 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 998,314 | 9.983 | 20 | 24 | fits | 46,217 | 31 | 0.651 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 151,650 | 1.516 | 20 | 50 | fits | 148,800 | 220 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 739,160 | 7.392 | 20 | 50 | fits | 147,059 | 168 | 0.551 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 305,360 | 3.054 | 20 | 20 | fits | 154,172 | 87 | 0.593 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 589,989 | 5.900 | 20 | 20 | fits | 125,070 | 44 | 0.456 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 265,047 | 2.650 | 20 | 20 | fits | 149,750 | 205 | 0.536 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 148,119 | 1.481 | 20 | 200 | fits | 148,416 | 221 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 305,870 | 3.059 | 20 | 200 | fits | 149,750 | 205 | 0.536 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 149,043 | 1.490 | 20 | 20 | fits | 148,416 | 221 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 952,744 | 9.527 | 20 | 20 | fits | 150,010 | 114 | 0.549 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 152,683 | 1.527 | 20 | 24 | fits | 148,416 | 221 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 997,622 | 9.976 | 20 | 24 | fits | 32,040 | 25 | 0.729 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 151,627 | 1.516 | 20 | 50 | fits | 148,416 | 221 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 309,598 | 3.096 | 20 | 50 | fits | 149,750 | 205 | 0.536 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 462,930 | 4.629 | 20 | 20 | fits | 153,398 | 48 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 737,893 | 7.379 | 20 | 20 | fits | 130,855 | 46 | 0.546 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 778,751 | 7.788 | 20 | 20 | fits | 153,363 | 172 | 0.564 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 147,466 | 1.475 | 20 | 200 | fits | 147,571 | 216 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 807,372 | 8.074 | 20 | 200 | fits | 153,363 | 172 | 0.564 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 148,390 | 1.484 | 20 | 20 | fits | 147,571 | 216 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 968,935 | 9.689 | 20 | 20 | fits | 151,555 | 124 | 0.513 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 152,030 | 1.520 | 20 | 24 | fits | 147,571 | 216 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 972,421 | 9.724 | 20 | 24 | fits | 151,555 | 124 | 0.513 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 150,974 | 1.510 | 20 | 50 | fits | 147,571 | 216 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 811,100 | 8.111 | 20 | 50 | fits | 153,363 | 172 | 0.564 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 304,678 | 3.047 | 20 | 20 | fits | 154,166 | 86 | 0.594 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 590,005 | 5.900 | 20 | 20 | fits | 141,287 | 50 | 0.519 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 759,037 | 7.590 | 20 | 20 | fits | 146,595 | 167 | 0.577 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 148,956 | 1.490 | 20 | 200 | fits | 148,804 | 220 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 802,013 | 8.020 | 20 | 200 | fits | 146,595 | 167 | 0.577 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 149,880 | 1.499 | 20 | 20 | fits | 148,804 | 220 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 955,463 | 9.555 | 20 | 20 | fits | 143,872 | 112 | 0.525 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 153,520 | 1.535 | 20 | 24 | fits | 148,804 | 220 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 986,182 | 9.862 | 20 | 24 | fits | 27,233 | 18 | 0.679 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 152,464 | 1.525 | 20 | 50 | fits | 148,804 | 220 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 805,741 | 8.057 | 20 | 50 | fits | 146,595 | 167 | 0.577 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 306,007 | 3.060 | 20 | 20 | fits | 154,005 | 86 | 0.592 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 591,414 | 5.914 | 20 | 20 | fits | 141,367 | 50 | 0.520 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 772,173 | 7.722 | 20 | 20 | fits | 148,073 | 169 | 0.558 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 149,142 | 1.491 | 20 | 200 | fits | 148,701 | 220 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 821,101 | 8.211 | 20 | 200 | fits | 148,073 | 169 | 0.558 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 150,066 | 1.501 | 20 | 20 | fits | 148,701 | 220 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 968,124 | 9.681 | 20 | 20 | fits | 146,319 | 118 | 0.491 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 153,706 | 1.537 | 20 | 24 | fits | 148,701 | 220 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 971,610 | 9.716 | 20 | 24 | fits | 146,319 | 118 | 0.491 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 152,650 | 1.526 | 20 | 50 | fits | 148,701 | 220 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 824,829 | 8.248 | 20 | 50 | fits | 148,073 | 169 | 0.558 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 306,235 | 3.062 | 20 | 20 | fits | 154,047 | 86 | 0.593 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 664,786 | 6.648 | 20 | 20 | fits | 143,105 | 56 | 0.529 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 278,603 | 2.786 | 20 | 20 | fits | 151,784 | 189 | 0.584 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 149,025 | 1.490 | 20 | 200 | fits | 148,295 | 220 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 300,193 | 3.002 | 20 | 200 | fits | 151,784 | 189 | 0.584 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 149,949 | 1.499 | 20 | 20 | fits | 148,295 | 220 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 949,282 | 9.493 | 20 | 20 | fits | 153,047 | 118 | 0.530 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 153,589 | 1.536 | 20 | 24 | fits | 148,295 | 220 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 992,923 | 9.929 | 20 | 24 | fits | 40,155 | 30 | 0.565 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 152,533 | 1.525 | 20 | 50 | fits | 148,295 | 220 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 303,921 | 3.039 | 20 | 50 | fits | 151,784 | 189 | 0.584 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 515,234 | 5.152 | 20 | 20 | fits | 145,737 | 51 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 797,147 | 7.971 | 20 | 20 | fits | 125,034 | 44 | 0.451 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 262,343 | 2.623 | 20 | 20 | fits | 150,089 | 205 | 0.537 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 144,936 | 1.449 | 20 | 200 | fits | 149,446 | 221 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 303,134 | 3.031 | 20 | 200 | fits | 150,089 | 205 | 0.537 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 145,860 | 1.459 | 20 | 20 | fits | 149,446 | 221 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 861,489 | 8.615 | 20 | 20 | fits | 144,415 | 112 | 0.526 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 149,500 | 1.495 | 20 | 24 | fits | 149,446 | 221 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 892,438 | 8.924 | 20 | 24 | fits | 27,463 | 18 | 0.683 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 148,444 | 1.484 | 20 | 50 | fits | 149,446 | 221 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 306,862 | 3.069 | 20 | 50 | fits | 150,089 | 205 | 0.537 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 459,920 | 4.599 | 20 | 20 | fits | 153,124 | 48 | 0.609 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 717,986 | 7.180 | 20 | 20 | fits | 113,964 | 40 | 0.460 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 690,740 | 6.907 | 20 | 20 | fits | 148,960 | 170 | 0.549 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 143,862 | 1.439 | 20 | 200 | fits | 148,139 | 216 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 716,755 | 7.168 | 20 | 200 | fits | 148,960 | 170 | 0.549 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 144,786 | 1.448 | 20 | 20 | fits | 148,139 | 216 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 868,915 | 8.689 | 20 | 20 | fits | 151,456 | 124 | 0.504 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 148,426 | 1.484 | 20 | 24 | fits | 148,139 | 216 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 872,401 | 8.724 | 20 | 24 | fits | 151,456 | 124 | 0.504 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 147,370 | 1.474 | 20 | 50 | fits | 148,139 | 216 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 720,483 | 7.205 | 20 | 50 | fits | 148,960 | 170 | 0.549 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 300,409 | 3.004 | 20 | 20 | fits | 153,501 | 86 | 0.591 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 569,411 | 5.694 | 20 | 20 | fits | 124,874 | 44 | 0.444 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 667,675 | 6.677 | 20 | 20 | fits | 148,343 | 168 | 0.558 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 145,527 | 1.455 | 20 | 200 | fits | 149,443 | 220 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 717,806 | 7.178 | 20 | 200 | fits | 148,343 | 168 | 0.558 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 146,451 | 1.465 | 20 | 20 | fits | 149,443 | 220 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 876,308 | 8.763 | 20 | 20 | fits | 149,096 | 120 | 0.543 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 150,091 | 1.501 | 20 | 24 | fits | 149,443 | 220 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 987,157 | 9.872 | 20 | 24 | fits | 27,744 | 19 | 0.677 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 149,035 | 1.490 | 20 | 50 | fits | 149,443 | 220 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 721,534 | 7.215 | 20 | 50 | fits | 148,343 | 168 | 0.558 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 302,077 | 3.021 | 20 | 20 | fits | 153,504 | 86 | 0.591 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 571,079 | 5.711 | 20 | 20 | fits | 124,874 | 44 | 0.444 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 693,848 | 6.938 | 20 | 20 | fits | 154,623 | 172 | 0.593 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 145,727 | 1.457 | 20 | 200 | fits | 149,282 | 220 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 733,884 | 7.339 | 20 | 200 | fits | 154,623 | 172 | 0.593 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 146,651 | 1.467 | 20 | 20 | fits | 149,282 | 220 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 957,741 | 9.577 | 20 | 20 | fits | 143,439 | 113 | 0.515 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 150,291 | 1.503 | 20 | 24 | fits | 149,282 | 220 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 988,483 | 9.885 | 20 | 24 | fits | 27,256 | 18 | 0.675 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 149,235 | 1.492 | 20 | 50 | fits | 149,282 | 220 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 737,612 | 7.376 | 20 | 50 | fits | 154,623 | 172 | 0.593 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 302,235 | 3.022 | 20 | 20 | fits | 153,462 | 86 | 0.590 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 571,471 | 5.715 | 20 | 20 | fits | 125,108 | 45 | 0.448 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 782,684 | 7.827 | 20 | 20 | fits | 152,592 | 169 | 0.548 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 146,062 | 1.461 | 20 | 200 | fits | 149,256 | 220 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 823,478 | 8.235 | 20 | 200 | fits | 152,592 | 169 | 0.548 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 146,986 | 1.470 | 20 | 20 | fits | 149,256 | 220 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 967,035 | 9.670 | 20 | 20 | fits | 142,853 | 113 | 0.512 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 150,626 | 1.506 | 20 | 24 | fits | 149,256 | 220 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 970,521 | 9.705 | 20 | 24 | fits | 142,853 | 113 | 0.512 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 149,570 | 1.496 | 20 | 50 | fits | 149,256 | 220 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 827,206 | 8.272 | 20 | 50 | fits | 152,592 | 169 | 0.548 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 302,945 | 3.029 | 20 | 20 | fits | 153,837 | 86 | 0.594 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 592,720 | 5.927 | 20 | 20 | fits | 135,876 | 57 | 0.537 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 791,683 | 7.917 | 20 | 20 | fits | 147,237 | 166 | 0.554 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 145,317 | 1.453 | 20 | 200 | fits | 148,150 | 220 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 818,056 | 8.181 | 20 | 200 | fits | 147,237 | 166 | 0.554 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 146,241 | 1.462 | 20 | 20 | fits | 148,150 | 220 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 966,747 | 9.667 | 20 | 20 | fits | 147,987 | 116 | 0.500 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 149,881 | 1.499 | 20 | 24 | fits | 148,150 | 220 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 970,233 | 9.702 | 20 | 24 | fits | 147,987 | 116 | 0.500 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 148,825 | 1.488 | 20 | 50 | fits | 148,150 | 220 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 821,784 | 8.218 | 20 | 50 | fits | 147,237 | 166 | 0.554 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 302,232 | 3.022 | 20 | 20 | fits | 153,869 | 87 | 0.594 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 672,435 | 6.724 | 20 | 20 | fits | 136,328 | 49 | 0.442 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 860,668 | 8.607 | 20 | 20 | fits | 156,501 | 123 | 0.559 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 145,993 | 1.460 | 20 | 200 | fits | 148,465 | 217 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 965,104 | 9.651 | 20 | 200 | fits | 156,501 | 123 | 0.559 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 146,917 | 1.469 | 20 | 20 | fits | 148,465 | 217 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 965,808 | 9.658 | 20 | 20 | fits | 156,501 | 123 | 0.559 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 150,557 | 1.506 | 20 | 24 | fits | 148,465 | 217 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 969,294 | 9.693 | 20 | 24 | fits | 156,501 | 123 | 0.559 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 149,501 | 1.495 | 20 | 50 | fits | 148,465 | 217 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 311,832 | 3.118 | 20 | 50 | fits | 154,073 | 208 | 0.500 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 460,546 | 4.605 | 20 | 20 | fits | 148,780 | 50 | 0.644 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 810,219 | 8.102 | 20 | 20 | fits | 124,857 | 44 | 0.444 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 265,513 | 2.655 | 20 | 20 | fits | 146,060 | 196 | 0.560 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 146,794 | 1.468 | 20 | 200 | fits | 149,267 | 220 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 292,238 | 2.922 | 20 | 200 | fits | 146,060 | 196 | 0.560 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 147,718 | 1.477 | 20 | 20 | fits | 149,267 | 220 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 944,937 | 9.449 | 20 | 20 | fits | 149,584 | 118 | 0.549 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 151,358 | 1.514 | 20 | 24 | fits | 149,267 | 220 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 988,361 | 9.884 | 20 | 24 | fits | 39,938 | 30 | 0.561 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 150,302 | 1.503 | 20 | 50 | fits | 149,267 | 220 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 295,966 | 2.960 | 20 | 50 | fits | 146,060 | 196 | 0.560 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 528,750 | 5.287 | 20 | 20 | fits | 153,278 | 48 | 0.606 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 786,963 | 7.870 | 20 | 20 | fits | 114,198 | 41 | 0.464 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 704,396 | 7.044 | 20 | 20 | fits | 152,670 | 168 | 0.550 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 152,437 | 1.524 | 20 | 200 | fits | 149,335 | 220 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 745,225 | 7.452 | 20 | 200 | fits | 152,670 | 168 | 0.550 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 153,361 | 1.534 | 20 | 20 | fits | 149,335 | 220 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 888,826 | 8.888 | 20 | 20 | fits | 142,897 | 113 | 0.512 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 157,001 | 1.570 | 20 | 24 | fits | 149,335 | 220 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 892,312 | 8.923 | 20 | 24 | fits | 142,897 | 113 | 0.512 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 155,945 | 1.559 | 20 | 50 | fits | 149,335 | 220 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 748,953 | 7.490 | 20 | 50 | fits | 152,670 | 168 | 0.550 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 309,554 | 3.096 | 20 | 20 | fits | 154,071 | 87 | 0.595 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 594,171 | 5.942 | 20 | 20 | fits | 125,144 | 44 | 0.454 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 270,409 | 2.704 | 20 | 20 | fits | 149,540 | 206 | 0.533 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 152,025 | 1.520 | 20 | 200 | fits | 148,562 | 221 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 310,006 | 3.100 | 20 | 200 | fits | 149,540 | 206 | 0.533 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 152,949 | 1.529 | 20 | 20 | fits | 148,562 | 221 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 869,524 | 8.695 | 20 | 20 | fits | 145,454 | 109 | 0.533 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 156,589 | 1.566 | 20 | 24 | fits | 148,562 | 221 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 909,258 | 9.093 | 20 | 24 | fits | 36,248 | 27 | 0.688 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 155,533 | 1.555 | 20 | 50 | fits | 148,562 | 221 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 313,734 | 3.137 | 20 | 50 | fits | 149,540 | 206 | 0.533 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 466,916 | 4.669 | 20 | 20 | fits | 153,248 | 48 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 724,982 | 7.250 | 20 | 20 | fits | 113,964 | 40 | 0.460 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 709,952 | 7.100 | 20 | 20 | fits | 153,527 | 118 | 0.581 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 135,167 | 1.352 | 20 | 200 | fits | 143,968 | 199 | 0.527 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 849,733 | 8.497 | 20 | 200 | fits | 153,527 | 118 | 0.581 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 136,091 | 1.361 | 20 | 20 | fits | 143,968 | 199 | 0.527 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 850,437 | 8.504 | 20 | 20 | fits | 153,527 | 118 | 0.581 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 139,731 | 1.397 | 20 | 24 | fits | 143,968 | 199 | 0.527 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 907,006 | 9.070 | 20 | 24 | fits | 44,548 | 37 | 0.614 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 138,675 | 1.387 | 20 | 50 | fits | 143,968 | 199 | 0.527 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 283,726 | 2.837 | 20 | 50 | fits | 145,447 | 216 | 0.505 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 428,746 | 4.287 | 20 | 20 | fits | 145,086 | 50 | 0.637 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 697,822 | 6.978 | 20 | 20 | fits | 124,796 | 44 | 0.442 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 688,559 | 6.886 | 20 | 20 | fits | 152,247 | 166 | 0.588 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 152,531 | 1.525 | 20 | 200 | fits | 149,238 | 220 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 728,672 | 7.287 | 20 | 200 | fits | 152,247 | 166 | 0.588 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 153,455 | 1.535 | 20 | 20 | fits | 149,238 | 220 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 885,567 | 8.856 | 20 | 20 | fits | 147,698 | 118 | 0.533 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 157,095 | 1.571 | 20 | 24 | fits | 149,238 | 220 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 916,400 | 9.164 | 20 | 24 | fits | 27,347 | 18 | 0.681 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 156,039 | 1.560 | 20 | 50 | fits | 149,238 | 220 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 732,400 | 7.324 | 20 | 50 | fits | 152,247 | 166 | 0.588 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 309,039 | 3.090 | 20 | 20 | fits | 153,462 | 86 | 0.590 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 578,041 | 5.780 | 20 | 20 | fits | 124,874 | 44 | 0.444 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 708,908 | 7.089 | 20 | 20 | fits | 155,447 | 175 | 0.557 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 152,793 | 1.528 | 20 | 200 | fits | 149,139 | 220 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 749,872 | 7.499 | 20 | 200 | fits | 155,447 | 175 | 0.557 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 153,717 | 1.537 | 20 | 20 | fits | 149,139 | 220 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 893,342 | 8.933 | 20 | 20 | fits | 142,766 | 113 | 0.510 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 157,357 | 1.574 | 20 | 24 | fits | 149,139 | 220 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 896,828 | 8.968 | 20 | 24 | fits | 142,766 | 113 | 0.510 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 156,301 | 1.563 | 20 | 50 | fits | 149,139 | 220 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 753,600 | 7.536 | 20 | 50 | fits | 155,447 | 175 | 0.557 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 309,700 | 3.097 | 20 | 20 | fits | 153,861 | 86 | 0.596 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 586,635 | 5.866 | 20 | 20 | fits | 132,854 | 51 | 0.501 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 718,363 | 7.184 | 20 | 20 | fits | 147,096 | 166 | 0.554 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 152,121 | 1.521 | 20 | 200 | fits | 148,106 | 220 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 744,763 | 7.448 | 20 | 200 | fits | 147,096 | 166 | 0.554 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 153,045 | 1.530 | 20 | 20 | fits | 148,106 | 220 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 893,454 | 8.935 | 20 | 20 | fits | 147,987 | 116 | 0.500 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 156,685 | 1.567 | 20 | 24 | fits | 148,106 | 220 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 896,940 | 8.969 | 20 | 24 | fits | 147,987 | 116 | 0.500 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 155,629 | 1.556 | 20 | 50 | fits | 148,106 | 220 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 748,491 | 7.485 | 20 | 50 | fits | 147,096 | 166 | 0.554 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 308,802 | 3.088 | 20 | 20 | fits | 153,635 | 86 | 0.593 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 599,283 | 5.993 | 20 | 20 | fits | 136,513 | 57 | 0.539 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 721,171 | 7.212 | 20 | 20 | fits | 149,038 | 170 | 0.550 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 152,500 | 1.525 | 20 | 200 | fits | 148,124 | 216 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 747,186 | 7.472 | 20 | 200 | fits | 149,038 | 170 | 0.550 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 153,424 | 1.534 | 20 | 20 | fits | 148,124 | 216 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 894,522 | 8.945 | 20 | 20 | fits | 146,632 | 117 | 0.492 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 157,064 | 1.571 | 20 | 24 | fits | 148,124 | 216 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 898,008 | 8.980 | 20 | 24 | fits | 146,632 | 117 | 0.492 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 156,008 | 1.560 | 20 | 50 | fits | 148,124 | 216 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 750,914 | 7.509 | 20 | 50 | fits | 149,038 | 170 | 0.550 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 309,323 | 3.093 | 20 | 20 | fits | 153,777 | 87 | 0.593 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 599,764 | 5.998 | 20 | 20 | fits | 135,756 | 48 | 0.433 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 270,080 | 2.701 | 20 | 20 | fits | 152,488 | 211 | 0.524 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 136,877 | 1.369 | 20 | 200 | fits | 146,069 | 179 | 0.536 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 288,749 | 2.887 | 20 | 200 | fits | 152,488 | 211 | 0.524 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 137,801 | 1.378 | 20 | 20 | fits | 146,069 | 179 | 0.536 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 446,774 | 4.468 | 20 | 20 | fits | 148,796 | 141 | 0.568 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 141,441 | 1.414 | 20 | 24 | fits | 146,069 | 179 | 0.536 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 907,766 | 9.078 | 20 | 24 | fits | 41,652 | 30 | 0.596 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 140,385 | 1.404 | 20 | 50 | fits | 146,069 | 179 | 0.536 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 292,477 | 2.925 | 20 | 50 | fits | 152,488 | 211 | 0.524 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 594,490 | 5.945 | 20 | 20 | fits | 144,758 | 50 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 863,540 | 8.635 | 20 | 20 | fits | 124,874 | 44 | 0.444 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 689,421 | 6.894 | 20 | 20 | fits | 152,664 | 169 | 0.550 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 152,666 | 1.527 | 20 | 200 | fits | 149,343 | 220 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 730,170 | 7.302 | 20 | 200 | fits | 152,664 | 169 | 0.550 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 153,590 | 1.536 | 20 | 20 | fits | 149,343 | 220 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 887,415 | 8.874 | 20 | 20 | fits | 148,048 | 120 | 0.532 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 157,230 | 1.572 | 20 | 24 | fits | 149,343 | 220 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 890,901 | 8.909 | 20 | 24 | fits | 148,048 | 120 | 0.532 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 156,174 | 1.562 | 20 | 50 | fits | 149,343 | 220 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 733,898 | 7.339 | 20 | 50 | fits | 152,664 | 169 | 0.550 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 309,966 | 3.100 | 20 | 20 | fits | 154,254 | 86 | 0.594 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 579,122 | 5.791 | 20 | 20 | fits | 124,874 | 44 | 0.444 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 710,943 | 7.109 | 20 | 20 | fits | 151,350 | 173 | 0.565 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 151,871 | 1.519 | 20 | 200 | fits | 148,232 | 220 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 737,645 | 7.376 | 20 | 200 | fits | 151,350 | 173 | 0.565 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 152,795 | 1.528 | 20 | 20 | fits | 148,232 | 220 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 886,375 | 8.864 | 20 | 20 | fits | 148,026 | 116 | 0.500 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 156,435 | 1.564 | 20 | 24 | fits | 148,232 | 220 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 889,861 | 8.899 | 20 | 24 | fits | 148,026 | 116 | 0.500 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 155,379 | 1.554 | 20 | 50 | fits | 148,232 | 220 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 741,373 | 7.414 | 20 | 50 | fits | 151,350 | 173 | 0.565 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 309,046 | 3.090 | 20 | 20 | fits | 154,129 | 86 | 0.595 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 578,483 | 5.785 | 20 | 20 | fits | 125,108 | 45 | 0.448 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 715,649 | 7.156 | 20 | 20 | fits | 149,170 | 170 | 0.551 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 152,204 | 1.522 | 20 | 200 | fits | 148,249 | 216 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 741,629 | 7.416 | 20 | 200 | fits | 149,170 | 170 | 0.551 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 153,128 | 1.531 | 20 | 20 | fits | 148,249 | 216 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 888,414 | 8.884 | 20 | 20 | fits | 146,081 | 112 | 0.537 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 156,768 | 1.568 | 20 | 24 | fits | 148,249 | 216 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 996,359 | 9.964 | 20 | 24 | fits | 27,665 | 19 | 0.673 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 155,712 | 1.557 | 20 | 50 | fits | 148,249 | 216 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 745,357 | 7.454 | 20 | 50 | fits | 149,170 | 170 | 0.551 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 309,210 | 3.092 | 20 | 20 | fits | 153,960 | 86 | 0.591 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 594,075 | 5.941 | 20 | 20 | fits | 130,718 | 51 | 0.536 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 705,079 | 7.051 | 20 | 20 | fits | 151,850 | 164 | 0.588 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 153,735 | 1.537 | 20 | 200 | fits | 149,464 | 220 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 746,046 | 7.460 | 20 | 200 | fits | 151,850 | 164 | 0.588 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 154,659 | 1.547 | 20 | 20 | fits | 149,464 | 220 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 966,833 | 9.668 | 20 | 20 | fits | 143,194 | 112 | 0.515 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 158,299 | 1.583 | 20 | 24 | fits | 149,464 | 220 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 997,512 | 9.975 | 20 | 24 | fits | 27,193 | 18 | 0.677 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 157,243 | 1.572 | 20 | 50 | fits | 149,464 | 220 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 749,774 | 7.498 | 20 | 50 | fits | 151,850 | 164 | 0.588 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 310,936 | 3.109 | 20 | 20 | fits | 154,155 | 87 | 0.592 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 595,812 | 5.958 | 20 | 20 | fits | 125,150 | 44 | 0.456 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 272,318 | 2.723 | 20 | 20 | fits | 152,328 | 211 | 0.523 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 139,319 | 1.393 | 20 | 200 | fits | 148,656 | 180 | 0.536 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 291,031 | 2.910 | 20 | 200 | fits | 152,328 | 211 | 0.523 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 140,243 | 1.402 | 20 | 20 | fits | 148,656 | 180 | 0.536 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 453,916 | 4.539 | 20 | 20 | fits | 153,423 | 152 | 0.535 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 143,883 | 1.439 | 20 | 24 | fits | 148,656 | 180 | 0.536 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 983,766 | 9.838 | 20 | 24 | fits | 29,062 | 18 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 142,827 | 1.428 | 20 | 50 | fits | 148,656 | 180 | 0.536 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 294,759 | 2.948 | 20 | 50 | fits | 152,328 | 211 | 0.523 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 605,630 | 6.056 | 20 | 20 | fits | 148,756 | 50 | 0.636 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 952,130 | 9.521 | 20 | 20 | fits | 124,934 | 44 | 0.446 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 271,795 | 2.718 | 20 | 20 | fits | 150,216 | 205 | 0.538 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 154,401 | 1.544 | 20 | 200 | fits | 149,498 | 221 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 312,668 | 3.127 | 20 | 200 | fits | 150,216 | 205 | 0.538 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 155,325 | 1.553 | 20 | 20 | fits | 149,498 | 221 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 956,640 | 9.566 | 20 | 20 | fits | 145,388 | 113 | 0.530 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 158,965 | 1.590 | 20 | 24 | fits | 149,498 | 221 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 1,000,839 | 10.008 | 20 | 24 | fits | 31,878 | 25 | 0.725 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 157,909 | 1.579 | 20 | 50 | fits | 149,498 | 221 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 316,396 | 3.164 | 20 | 50 | fits | 150,216 | 205 | 0.538 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 465,740 | 4.657 | 20 | 20 | fits | 149,410 | 50 | 0.643 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 812,164 | 8.122 | 20 | 20 | fits | 124,934 | 44 | 0.446 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 325,745 | 3.257 | 20 | 20 | fits | 150,499 | 144 | 0.578 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 137,396 | 1.374 | 20 | 200 | fits | 146,235 | 179 | 0.536 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 436,891 | 4.369 | 20 | 200 | fits | 150,499 | 144 | 0.578 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 138,320 | 1.383 | 20 | 20 | fits | 146,235 | 179 | 0.536 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 437,595 | 4.376 | 20 | 20 | fits | 150,499 | 144 | 0.578 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 141,960 | 1.420 | 20 | 24 | fits | 146,235 | 179 | 0.536 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 988,523 | 9.885 | 20 | 24 | fits | 41,594 | 30 | 0.589 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 140,904 | 1.409 | 20 | 50 | fits | 146,235 | 179 | 0.536 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 290,120 | 2.901 | 20 | 50 | fits | 149,612 | 206 | 0.506 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 670,681 | 6.707 | 20 | 20 | fits | 153,381 | 48 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 944,355 | 9.444 | 20 | 20 | fits | 119,715 | 47 | 0.554 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 270,309 | 2.703 | 20 | 20 | fits | 152,131 | 210 | 0.522 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 137,520 | 1.375 | 20 | 200 | fits | 146,043 | 179 | 0.536 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 289,035 | 2.890 | 20 | 200 | fits | 152,131 | 210 | 0.522 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 138,444 | 1.384 | 20 | 20 | fits | 146,043 | 179 | 0.536 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 437,467 | 4.375 | 20 | 20 | fits | 147,728 | 141 | 0.556 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 142,084 | 1.421 | 20 | 24 | fits | 146,043 | 179 | 0.536 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 988,492 | 9.885 | 20 | 24 | fits | 41,725 | 30 | 0.592 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 141,028 | 1.410 | 20 | 50 | fits | 146,043 | 179 | 0.536 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 292,763 | 2.928 | 20 | 50 | fits | 152,131 | 210 | 0.522 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 670,169 | 6.702 | 20 | 20 | fits | 153,092 | 49 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 944,193 | 9.442 | 20 | 20 | fits | 114,240 | 40 | 0.473 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 264,601 | 2.646 | 20 | 20 | fits | 150,171 | 205 | 0.537 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 147,252 | 1.473 | 20 | 200 | fits | 149,498 | 221 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 305,474 | 3.055 | 20 | 200 | fits | 150,171 | 205 | 0.537 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 148,176 | 1.482 | 20 | 20 | fits | 149,498 | 221 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 864,141 | 8.641 | 20 | 20 | fits | 144,415 | 112 | 0.526 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 151,816 | 1.518 | 20 | 24 | fits | 149,498 | 221 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 895,090 | 8.951 | 20 | 24 | fits | 27,463 | 18 | 0.683 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 150,760 | 1.508 | 20 | 50 | fits | 149,498 | 221 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 309,202 | 3.092 | 20 | 50 | fits | 150,171 | 205 | 0.537 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 462,572 | 4.626 | 20 | 20 | fits | 153,436 | 48 | 0.609 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 720,638 | 7.206 | 20 | 20 | fits | 113,964 | 40 | 0.460 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 692,790 | 6.928 | 20 | 20 | fits | 149,197 | 171 | 0.550 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 145,287 | 1.453 | 20 | 200 | fits | 148,137 | 216 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 719,107 | 7.191 | 20 | 200 | fits | 149,197 | 171 | 0.550 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 146,211 | 1.462 | 20 | 20 | fits | 148,137 | 216 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 880,427 | 8.804 | 20 | 20 | fits | 151,712 | 124 | 0.512 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 149,851 | 1.499 | 20 | 24 | fits | 148,137 | 216 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 883,913 | 8.839 | 20 | 24 | fits | 151,712 | 124 | 0.512 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 148,795 | 1.488 | 20 | 50 | fits | 148,137 | 216 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 722,835 | 7.228 | 20 | 50 | fits | 149,197 | 171 | 0.550 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 302,372 | 3.024 | 20 | 20 | fits | 154,039 | 86 | 0.592 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 571,526 | 5.715 | 20 | 20 | fits | 124,874 | 44 | 0.444 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 669,549 | 6.695 | 20 | 20 | fits | 148,364 | 168 | 0.558 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 146,818 | 1.468 | 20 | 200 | fits | 149,352 | 220 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 719,766 | 7.198 | 20 | 200 | fits | 148,364 | 168 | 0.558 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 147,742 | 1.477 | 20 | 20 | fits | 149,352 | 220 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 878,274 | 8.783 | 20 | 20 | fits | 149,018 | 120 | 0.543 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 151,382 | 1.514 | 20 | 24 | fits | 149,352 | 220 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 908,987 | 9.090 | 20 | 24 | fits | 27,227 | 18 | 0.681 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 150,326 | 1.503 | 20 | 50 | fits | 149,352 | 220 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 723,494 | 7.235 | 20 | 50 | fits | 148,364 | 168 | 0.558 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 303,864 | 3.039 | 20 | 20 | fits | 154,000 | 86 | 0.591 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 573,018 | 5.730 | 20 | 20 | fits | 124,874 | 44 | 0.444 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 695,938 | 6.959 | 20 | 20 | fits | 154,770 | 172 | 0.593 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 147,062 | 1.471 | 20 | 200 | fits | 149,280 | 220 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 736,056 | 7.361 | 20 | 200 | fits | 154,770 | 172 | 0.593 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 147,986 | 1.480 | 20 | 20 | fits | 149,280 | 220 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 879,546 | 8.795 | 20 | 20 | fits | 142,786 | 111 | 0.515 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 151,626 | 1.516 | 20 | 24 | fits | 149,280 | 220 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 910,303 | 9.103 | 20 | 24 | fits | 27,271 | 18 | 0.677 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 150,570 | 1.506 | 20 | 50 | fits | 149,280 | 220 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 739,784 | 7.398 | 20 | 50 | fits | 154,770 | 172 | 0.593 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 304,108 | 3.041 | 20 | 20 | fits | 154,000 | 86 | 0.591 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 573,496 | 5.735 | 20 | 20 | fits | 125,108 | 45 | 0.448 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 704,893 | 7.049 | 20 | 20 | fits | 152,904 | 168 | 0.552 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 147,245 | 1.472 | 20 | 200 | fits | 149,147 | 220 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 745,804 | 7.458 | 20 | 200 | fits | 152,904 | 168 | 0.552 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 148,169 | 1.482 | 20 | 20 | fits | 149,147 | 220 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 889,405 | 8.894 | 20 | 20 | fits | 142,897 | 113 | 0.512 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 151,809 | 1.518 | 20 | 24 | fits | 149,147 | 220 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 892,891 | 8.929 | 20 | 24 | fits | 142,897 | 113 | 0.512 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 150,753 | 1.508 | 20 | 50 | fits | 149,147 | 220 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 749,532 | 7.495 | 20 | 50 | fits | 152,904 | 168 | 0.552 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 304,648 | 3.046 | 20 | 20 | fits | 154,357 | 86 | 0.596 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 594,516 | 5.945 | 20 | 20 | fits | 135,817 | 57 | 0.536 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 712,940 | 7.129 | 20 | 20 | fits | 147,064 | 166 | 0.553 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 146,526 | 1.465 | 20 | 200 | fits | 148,112 | 220 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 739,430 | 7.394 | 20 | 200 | fits | 147,064 | 166 | 0.553 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 147,450 | 1.474 | 20 | 20 | fits | 148,112 | 220 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 888,121 | 8.881 | 20 | 20 | fits | 147,987 | 116 | 0.500 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 151,090 | 1.511 | 20 | 24 | fits | 148,112 | 220 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 891,607 | 8.916 | 20 | 24 | fits | 147,987 | 116 | 0.500 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 150,034 | 1.500 | 20 | 50 | fits | 148,112 | 220 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 743,158 | 7.432 | 20 | 50 | fits | 147,064 | 166 | 0.553 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 304,014 | 3.040 | 20 | 20 | fits | 154,442 | 87 | 0.597 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 593,982 | 5.940 | 20 | 20 | fits | 135,866 | 48 | 0.434 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 781,179 | 7.812 | 20 | 20 | fits | 156,167 | 122 | 0.557 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 147,104 | 1.471 | 20 | 200 | fits | 148,374 | 217 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 885,447 | 8.854 | 20 | 200 | fits | 156,167 | 122 | 0.557 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 148,028 | 1.480 | 20 | 20 | fits | 148,374 | 217 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 886,151 | 8.862 | 20 | 20 | fits | 156,167 | 122 | 0.557 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 151,668 | 1.517 | 20 | 24 | fits | 148,374 | 217 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 889,637 | 8.896 | 20 | 24 | fits | 156,167 | 122 | 0.557 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 150,612 | 1.506 | 20 | 50 | fits | 148,374 | 217 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 312,842 | 3.128 | 20 | 50 | fits | 154,030 | 208 | 0.500 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 462,019 | 4.620 | 20 | 20 | fits | 149,243 | 50 | 0.644 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 730,896 | 7.309 | 20 | 20 | fits | 124,796 | 44 | 0.442 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 266,593 | 2.666 | 20 | 20 | fits | 146,063 | 196 | 0.560 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 147,953 | 1.480 | 20 | 200 | fits | 149,264 | 220 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 293,400 | 2.934 | 20 | 200 | fits | 146,063 | 196 | 0.560 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 148,877 | 1.489 | 20 | 20 | fits | 149,264 | 220 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 852,314 | 8.523 | 20 | 20 | fits | 144,598 | 112 | 0.528 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 152,517 | 1.525 | 20 | 24 | fits | 149,264 | 220 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 909,136 | 9.091 | 20 | 24 | fits | 44,448 | 37 | 0.613 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 151,461 | 1.515 | 20 | 50 | fits | 149,264 | 220 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 297,128 | 2.971 | 20 | 50 | fits | 146,063 | 196 | 0.560 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 450,562 | 4.506 | 20 | 20 | fits | 153,500 | 48 | 0.609 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 708,628 | 7.086 | 20 | 20 | fits | 113,964 | 40 | 0.460 |
| LINK_UP | `adp.link_up.if0` | 2,521 | 0.025 | 20 | 200 | fits | 25,318 | 43 (11) | 0.727 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,069 | 0.101 | 20 | 200 | fits | 20,316 | 23 (39) | 0.710 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 2,289 | 0.023 | 20 | 200 | fits | 2,508 | 10 (11) | 0.520 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 151,934 | 1.519 | 20 | 200 | fits | 152,874 | 239 | 0.487 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 703,197 | 7.032 | 20 | 20 | fits | 153,620 | 145 | 0.542 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 328,570 | 3.286 | 20 | 24 | fits | 145,577 | 123 | 0.422 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 663,722 | 6.637 | 20 | 50 | fits | 153,620 | 145 | 0.542 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 488,077 | 4.881 | 20 | 20 | fits | 113,920 | 40 | 0.462 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 177,561 | 1.776 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 151,934 | 1.519 | 20 | 200 | fits | 152,874 | 239 | 0.487 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 715,664 | 7.157 | 20 | 20 | fits | 156,296 | 151 | 0.544 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 344,776 | 3.448 | 20 | 24 | fits | 149,316 | 129 | 0.436 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 676,189 | 6.762 | 20 | 50 | fits | 156,296 | 151 | 0.544 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 497,868 | 4.979 | 20 | 20 | fits | 127,807 | 50 | 0.470 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 186,803 | 1.868 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 20,568 | 0.206 | 20 | 20 | fits | 30,077 | 27 (35) | 0.816 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 14,755 | 0.148 | 20 | 20 | fits | 26,831 | 23 (14) | 0.849 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 19,402 | 0.194 | 20 | 20 | fits | 26,660 | 24 (14) | 0.846 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 9,577 | 0.096 | 20 | 20 | fits | 28,257 | 21 (35) | 0.835 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 83,710 | 0.837 | 20 | 20 | fits | 66,016 | 6 | 0.888 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 43,073 | 0.431 | 20 | 20 | fits | 43,139 | 12 | 0.901 |
| malformed MRPDU discard | `srp.malformed.if0` | 18,935 | 0.189 | 20 | 20 | fits | 19,001 | 12 | 0.631 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 96,458 | 0.965 | 220 | 220 | fits | 96,033 | 9 | 0.871 |
| an event behind 15 others | `backlog.event.if0` | 169,686 | 1.697 | 20 | 200 | fits | 80,222 | 109 | 0.529 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 483,136 | 4.831 | 20 | 20 | fits | 142,264 | 111 | 0.516 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 155,557 | 1.556 | 20 | 200 | fits | 155,766 | 226 | 0.515 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 325,364 | 3.254 | 20 | 200 | fits | 90,201 | 52 | 0.635 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 151,235 | 1.512 | 20 | 20 | fits | 155,766 | 226 | 0.515 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 550,462 | 5.505 | 20 | 20 | fits | 142,264 | 111 | 0.516 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 154,875 | 1.549 | 20 | 24 | fits | 155,766 | 226 | 0.515 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 580,866 | 5.809 | 20 | 24 | fits | 26,918 | 18 | 0.673 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 153,819 | 1.538 | 20 | 50 | fits | 155,766 | 226 | 0.515 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 323,846 | 3.238 | 20 | 50 | fits | 90,201 | 52 | 0.635 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 359,839 | 3.598 | 20 | 20 | fits | 31,640 | 53 | 0.217 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 409,110 | 4.091 | 20 | 20 | fits | 22,590 | 36 | 0.073 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 718,675 | 7.187 | 20 | 20 | fits | 151,927 | 165 | 0.588 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 143,851 | 1.439 | 20 | 200 | fits | 148,601 | 223 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 736,622 | 7.366 | 20 | 200 | fits | 151,927 | 165 | 0.588 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 144,775 | 1.448 | 20 | 20 | fits | 148,601 | 223 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 880,546 | 8.805 | 20 | 20 | fits | 143,220 | 111 | 0.515 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 148,415 | 1.484 | 20 | 24 | fits | 148,601 | 223 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 910,919 | 9.109 | 20 | 24 | fits | 26,887 | 18 | 0.667 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 147,359 | 1.474 | 20 | 50 | fits | 148,601 | 223 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 740,350 | 7.404 | 20 | 50 | fits | 151,927 | 165 | 0.588 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 301,579 | 3.016 | 20 | 20 | fits | 154,682 | 87 | 0.603 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 586,311 | 5.863 | 20 | 20 | fits | 125,061 | 44 | 0.453 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,681 | 0.087 | 20 | 20 | fits | 24,468 | 19 | 0.809 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 143,851 | 1.439 | 20 | 200 | fits | 148,601 | 223 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 24,852 | 0.249 | 20 | 200 | fits | 24,468 | 19 | 0.809 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 144,775 | 1.448 | 20 | 20 | fits | 148,601 | 223 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 883,726 | 8.837 | 20 | 20 | fits | 147,362 | 116 | 0.495 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 148,415 | 1.484 | 20 | 24 | fits | 148,601 | 223 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 887,212 | 8.872 | 20 | 24 | fits | 147,362 | 116 | 0.495 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 147,359 | 1.474 | 20 | 50 | fits | 148,601 | 223 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 739,388 | 7.394 | 20 | 50 | fits | 150,965 | 162 | 0.569 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 301,579 | 3.016 | 20 | 20 | fits | 154,682 | 87 | 0.603 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 586,311 | 5.863 | 20 | 20 | fits | 125,061 | 44 | 0.453 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,294,936 | 62.949 | 20 | 20 | MISS ceiling | 15,880 | 13 | 0.635 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,310,817 | 63.108 | 20 | 20 | MISS ceiling | 16,017 | 13 | 0.606 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,326,759 | 63.268 | 20 | 20 | MISS ceiling | 15,939 | 13 | 0.615 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,342,614 | 63.426 | 20 | 20 | MISS ceiling | 15,931 | 13 | 0.625 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,358,470 | 63.585 | 20 | 20 | MISS ceiling | 15,927 | 13 | 0.625 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 153,085 | 1.531 | 20 | 200 | fits | 146,774 | 209 | 0.520 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 702,104 | 7.021 | 20 | 200 | fits | 118,888 | 138 | 0.574 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 148,763 | 1.488 | 20 | 20 | fits | 146,774 | 209 | 0.520 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,217,946 | 62.179 | 20 | 20 | MISS ceiling | 26,589 | 15 | 0.762 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 152,403 | 1.524 | 20 | 24 | fits | 146,774 | 209 | 0.520 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,194,843 | 61.948 | 20 | 24 | MISS ceiling | 158,371 | 119 | 0.468 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 151,347 | 1.513 | 20 | 50 | fits | 146,774 | 209 | 0.520 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 700,586 | 7.006 | 20 | 50 | fits | 118,888 | 138 | 0.574 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 306,555 | 3.066 | 20 | 20 | fits | 155,670 | 87 | 0.603 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 579,586 | 5.796 | 20 | 20 | fits | 126,840 | 45 | 0.484 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 6,151 | 0.062 | 20 | 20 | fits | 21,649 | 13 (29) | 0.797 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,688 | 0.077 | 20 | 20 | fits | 23,664 | 19 (35) | 0.797 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 20,360 | 0.204 | 20 | 20 | fits | 27,844 | 21 (12) | 0.831 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 10,206 | 0.102 | 20 | 50 | fits | 25,318 | 43 | 0.727 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 12,845 | 0.128 | 20 | 50 | fits | 25,725 | 41 | 0.661 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 18,830 | 0.188 | 20 | 50 | fits | 21,961 | 35 | 0.702 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 13,491 | 0.135 | 20 | 50 | fits | 26,814 | 61 | 0.632 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 15,658 | 0.157 | 20 | 50 | fits | 26,814 | 61 | 0.632 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 10,209 | 0.102 | 20 | 50 | fits | 20,217 | 30 | 0.637 |
| LINK_UP | `adp.link_up.if0` | 2,521 | 0.025 | 20 | 200 | fits | 25,318 | 43 (11) | 0.727 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,069 | 0.101 | 20 | 200 | fits | 20,316 | 23 (39) | 0.710 |
| LINK_DOWN | `adp.link_down.if0` | 2,232 | 0.022 | 20 | 200 | fits | 23,230 | 23 (9) | 0.740 |
| LINK_UP | `adp.link_up.if0` | 2,521 | 0.025 | 20 | 200 | fits | 25,318 | 43 (11) | 0.727 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,069 | 0.101 | 20 | 200 | fits | 20,316 | 23 (39) | 0.710 |
| GM_CHANGE | `adp.gm_change.if0` | 2,369 | 0.024 | 20 | 200 | fits | 15,010 | 17 (11) | 0.708 |
| LINK_UP | `adp.link_up.if0` | 2,521 | 0.025 | 20 | 200 | fits | 25,318 | 43 (11) | 0.727 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,069 | 0.101 | 20 | 200 | fits | 20,316 | 23 (39) | 0.710 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,601 | 0.046 | 20 | 200 | fits | 14,567 | 16 (31) | 0.625 |
| LINK_UP | `adp.link_up.if0` | 2,521 | 0.025 | 20 | 200 | fits | 25,318 | 43 (11) | 0.727 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,069 | 0.101 | 20 | 200 | fits | 20,316 | 23 (39) | 0.710 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,601 | 0.046 | 20 | 200 | fits | 14,567 | 16 (31) | 0.625 |
| set_name | `aecp_fanout.set_name.if0` | 54,656 | 0.547 | 20 | 24 | fits | 57,760 | 88 | 0.543 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 39,014 | 0.390 | 20 | 24 | fits | 50,523 | 77 | 0.560 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 37,019 | 0.370 | 20 | 24 | fits | 46,599 | 78 | 0.525 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 45,798 | 0.458 | 20 | 24 | fits | 45,621 | 77 | 0.511 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 40,288 | 0.403 | 20 | 24 | fits | 52,643 | 66 | 0.589 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 47,881 | 0.479 | 20 | 24 | fits | 50,531 | 65 | 0.563 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 44,365 | 0.444 | 20 | 24 | fits | 49,165 | 66 | 0.570 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 36,725 | 0.367 | 20 | 24 | fits | 45,858 | 77 | 0.520 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 46,568 | 0.466 | 20 | 24 | fits | 45,381 | 78 | 0.509 |
| BIND_RX | `acmp.bind_rx.if0` | 18,524 | 0.185 | 20 | 20 | fits | 38,973 | 26 (77) | 0.798 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,257 | 0.093 | 20 | 20 | fits | 29,759 | 20 (32) | 0.827 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,605 | 0.106 | 20 | 20 | fits | 23,245 | 15 (47) | 0.767 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,279 | 0.133 | 20 | 20 | fits | 37,593 | 18 (50) | 0.838 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,462 | 0.105 | 20 | 20 | fits | 23,745 | 17 (48) | 0.762 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,909 | 0.099 | 20 | 20 | fits | 22,681 | 16 (48) | 0.741 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,638 | 0.096 | 20 | 20 | fits | 22,038 | 16 (48) | 0.731 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,909 | 0.099 | 20 | 20 | fits | 21,606 | 16 (48) | 0.720 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 19,950 | 0.200 | 20 | 24 | fits | 24,923 | 20 | 0.772 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 20,817 | 0.208 | 20 | 24 | fits | 29,502 | 20 | 0.699 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 11,014 | 0.110 | 20 | 24 | fits | 25,018 | 20 | 0.712 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 16,014 | 0.160 | 20 | 24 | fits | 24,777 | 20 | 0.713 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 10,595 | 0.106 | 20 | 24 | fits | 25,106 | 20 | 0.704 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 11,871 | 0.119 | 20 | 24 | fits | 25,526 | 20 | 0.717 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 15,827 | 0.158 | 20 | 24 | fits | 24,634 | 20 | 0.716 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 10,957 | 0.110 | 20 | 24 | fits | 24,629 | 20 | 0.723 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 14,970 | 0.150 | 20 | 24 | fits | 24,294 | 20 | 0.732 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 13,005 | 0.130 | 20 | 24 | fits | 26,605 | 21 | 0.613 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 15,282 | 0.153 | 20 | 24 | fits | 23,460 | 20 | 0.747 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 9,416 | 0.094 | 20 | 24 | fits | 23,249 | 20 | 0.736 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 15,533 | 0.155 | 20 | 24 | fits | 24,422 | 20 | 0.721 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 15,451 | 0.155 | 20 | 24 | fits | 25,119 | 20 | 0.722 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 10,527 | 0.105 | 20 | 24 | fits | 24,268 | 20 | 0.725 |
| get_configuration | `aecp.get_configuration.if0` | 14,307 | 0.143 | 20 | 24 | fits | 22,454 | 20 | 0.747 |
| entity_available | `aecp.entity_available.if0` | 8,326 | 0.083 | 20 | 24 | fits | 21,907 | 20 | 0.720 |
| get_name | `aecp.get_name.if0` | 16,443 | 0.164 | 20 | 24 | fits | 25,584 | 20 | 0.757 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 11,167 | 0.112 | 20 | 24 | fits | 25,617 | 27 | 0.705 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 17,569 | 0.176 | 20 | 24 | fits | 26,398 | 29 | 0.751 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 13,925 | 0.139 | 20 | 24 | fits | 22,420 | 20 | 0.745 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 7,858 | 0.079 | 20 | 24 | fits | 21,722 | 20 | 0.718 |
| set_name | `aecp.set_name.if0` | 22,897 | 0.229 | 20 | 24 | fits | 40,647 | 42 | 0.743 |
| lock_entity | `aecp.lock_entity.if0` | 28,255 | 0.283 | 20 | 24 | fits | 29,991 | 33 | 0.748 |
| unlock_entity | `aecp.unlock_entity.if0` | 23,024 | 0.230 | 20 | 24 | fits | 30,635 | 32 | 0.764 |
| LINK_UP | `fixture.link_up.if0` | 2,521 | 0.025 | 20 | 200 | fits | 25,318 | 43 (11) | 0.727 |
| malformed MRPDU discard | `fixture.malformed.if0` | 19,717 | 0.197 | 20 | 20 | fits | 19,783 | 12 | 0.729 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 27,714 | 0.277 | 20 | 24 | fits | 41,120 | 42 | 0.745 |
| LINK_DOWN | `fixture.link_down.if0` | 2,498 | 0.025 | 20 | 200 | fits | 24,750 | 23 (9) | 0.757 |
| BIND_RX | `fixture.bind_rx.if0` | 19,759 | 0.198 | 20 | 20 | fits | 39,187 | 26 (77) | 0.800 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 17,201 | 0.172 | 20 | 20 | fits | 34,522 | 29 (35) | 0.798 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 5,459 | 0.055 | 20 | 20 | fits | 22,492 | 13 (29) | 0.812 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 81,534 | 0.815 | 20 | 200 | fits | 81,638 | 51 | 0.758 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 81,534 | 0.815 | 20 | 200 | fits | 81,638 | 51 | 0.758 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 81,260 | 0.813 | 20 | 20 | fits | 81,638 | 51 | 0.758 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 81,260 | 0.813 | 20 | 20 | fits | 81,638 | 51 | 0.758 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 81,468 | 0.815 | 20 | 24 | fits | 81,638 | 51 | 0.758 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 81,468 | 0.815 | 20 | 24 | fits | 81,638 | 51 | 0.758 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 81,402 | 0.814 | 20 | 50 | fits | 81,638 | 51 | 0.758 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 81,402 | 0.814 | 20 | 50 | fits | 81,638 | 51 | 0.758 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 81,336 | 0.813 | 20 | 20 | fits | 81,638 | 51 | 0.758 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 81,336 | 0.813 | 20 | 20 | fits | 81,638 | 51 | 0.758 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
