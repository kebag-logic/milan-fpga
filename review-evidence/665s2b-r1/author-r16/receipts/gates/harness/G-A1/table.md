### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 86 paths and 6 of 943 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.222 (0.395) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.102 (0.233) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.064 (0.212) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.092 (0.338) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.117 (0.261) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.102 (0.233) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.117 (0.253) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.112 (0.245) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.076 (0.248) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.112 (0.269) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.132 (0.377) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.228 (0.511) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.059 (0.318) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.142 (0.450) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.118 (0.362) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.138 (0.328) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.041 (0.111) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.024 (0.103) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.025 (0.221) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.025 (0.205) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.090 (0.203) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.151 (0.345) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.142 (0.195) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.153 (0.206) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.140 (0.286) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.189 (0.338) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.168 (0.230) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.201 (0.290) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.144 (0.198) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.208 (0.268) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.170 (0.320) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.184 (0.366) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.151 (0.207) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.186 (0.332) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.147 (0.201) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.155 (0.300) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.161 (0.215) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.157 (0.212) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.170 (0.318) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.160 (0.218) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.176 (0.324) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.170 (0.229) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.159 (0.304) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.213 (0.375) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.251 (0.462) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 0.145 (0.289) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.209 (0.393) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 0.485 (0.701) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.457 (0.667) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.490 (0.704) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.556 (0.774) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.533 (0.739) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.545 (0.782) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.512 (0.694) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.431 (0.503) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.782 (4.128) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-aged2-6.adp_available.if0` (backlog-adp@verify-aged2-6) | 4.567 (5.380) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.080 (0.327) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 0.969 (1.581) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.163 (62.343) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.251 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.272 (0.366) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 4.478 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.856 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 6.127 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 2.966 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.648 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.142 (0.362) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.092 (0.163) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.110 (0.205) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.123 (0.362) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.093 (0.296) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.acmp.first.if0` (backlog-adp@verify-0) | 1.520 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-6.service.acmp.last.if0` (backlog-adp@verify-aged2-6) | 6.794 | fits | 11 acmp | 77 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.adp.first.if0` (backlog-adp@verify-0) | 1.511 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-6.service.adp.last.if0` (backlog-adp@verify-aged2-6) | 5.369 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.aecp.first.if0` (backlog-adp@verify-0) | 1.556 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 63.032 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.maap.first.if0` (backlog-adp@verify-0) | 1.546 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.maap.last.if0` (backlog-adp@verify-0) | 4.609 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-aged1-6.service.srp.first.if0` (backlog-adp@verify-aged1-6) | 3.118 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-aged1-7.service.srp.last.if0` (backlog-adp@blank-aged1-7) | 12.229 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.788 (0.887) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.352 (0.352) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.135 (0.136) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 9.265 (9.350) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 12.655 | 20 | 114,428 (1.144) | yes | - |
| backlog-adp@blank-1 | 0 | 11.951 | 20 | 114,483 (1.145) | yes | - |
| backlog-adp@blank-2 | 0 | 12.004 | 20 | 114,483 (1.145) | yes | - |
| backlog-adp@blank-3 | 0 | 11.934 | 19 | 114,556 (1.146) | yes | - |
| backlog-adp@blank-4 | 0 | 11.957 | 20 | 105,442 (1.054) | yes | - |
| backlog-adp@blank-5 | 0 | 12.070 | 20 | 116,133 (1.161) | yes | - |
| backlog-adp@blank-6 | 0 | 12.168 | 21 | 114,283 (1.143) | yes | - |
| backlog-adp@blank-7 | 0 | 14.007 | 22 | 113,008 (1.130) | yes | - |
| backlog-adp@program-0 | 0 | 11.966 | 19 | 114,446 (1.144) | yes | - |
| backlog-adp@program-1 | 0 | 12.118 | 21 | 108,567 (1.086) | yes | - |
| backlog-adp@program-2 | 0 | 12.137 | 19 | 113,945 (1.139) | yes | - |
| backlog-adp@program-3 | 0 | 12.363 | 21 | 96,209 (0.962) | yes | - |
| backlog-adp@program-4 | 0 | 11.224 | 19 | 114,542 (1.145) | yes | - |
| backlog-adp@program-5 | 0 | 11.371 | 20 | 113,987 (1.140) | yes | - |
| backlog-adp@program-6 | 0 | 11.279 | 19 | 113,987 (1.140) | yes | - |
| backlog-adp@program-7 | 0 | 11.321 | 20 | 100,080 (1.001) | yes | - |
| backlog-adp@verify-0 | 0 | 12.704 | 20 | 114,551 (1.146) | yes | - |
| backlog-adp@verify-1 | 0 | 12.024 | 20 | 114,599 (1.146) | yes | - |
| backlog-adp@verify-2 | 0 | 12.032 | 21 | 114,526 (1.145) | yes | - |
| backlog-adp@verify-3 | 0 | 11.956 | 19 | 113,923 (1.139) | yes | - |
| backlog-adp@verify-4 | 0 | 12.007 | 20 | 105,511 (1.055) | yes | - |
| backlog-adp@verify-5 | 0 | 12.027 | 20 | 116,176 (1.162) | yes | - |
| backlog-adp@verify-6 | 0 | 12.212 | 21 | 114,025 (1.140) | yes | - |
| backlog-adp@verify-7 | 0 | 12.146 | 21 | 96,209 (0.962) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 12.576 | 20 | 114,091 (1.141) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 12.183 | 21 | 114,168 (1.142) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 12.112 | 20 | 114,168 (1.142) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 12.101 | 20 | 113,476 (1.135) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 12.137 | 20 | 113,476 (1.135) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 12.103 | 21 | 113,476 (1.135) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 13.114 | 21 | 113,476 (1.135) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 12.953 | 21 | 96,656 (0.967) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 13.001 | 21 | 121,055 (1.211) | yes | - |
| backlog-adp@blank-aged1-1 | 1 | 12.904 | 20 | 121,107 (1.211) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 12.895 | 20 | 121,069 (1.211) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 12.898 | 21 | 114,491 (1.145) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 12.955 | 21 | 114,407 (1.144) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 13.011 | 22 | 114,348 (1.143) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 13.850 | 22 | 121,317 (1.213) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 14.023 | 23 | 128,083 (1.281) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 12.185 | 20 | 114,424 (1.144) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 12.195 | 20 | 113,997 (1.140) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 12.116 | 19 | 115,364 (1.154) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 12.095 | 19 | 114,631 (1.146) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 12.223 | 21 | 113,275 (1.133) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 12.104 | 20 | 113,554 (1.136) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 12.397 | 21 | 113,554 (1.136) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 12.332 | 21 | 96,870 (0.969) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 12.194 | 21 | 114,320 (1.143) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 12.111 | 20 | 114,313 (1.143) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 12.030 | 19 | 113,704 (1.137) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 11.928 | 19 | 113,704 (1.137) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 11.991 | 19 | 113,704 (1.137) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 12.045 | 20 | 113,704 (1.137) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 12.379 | 20 | 113,704 (1.137) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 11.963 | 20 | 108,438 (1.084) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 12.034 | 20 | 114,358 (1.144) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 12.032 | 20 | 114,170 (1.142) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 11.944 | 19 | 113,634 (1.136) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 11.943 | 19 | 113,634 (1.136) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 12.010 | 19 | 113,634 (1.136) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 12.049 | 20 | 113,634 (1.136) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 13.150 | 21 | 113,634 (1.136) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 12.967 | 20 | 99,102 (0.991) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 12.079 | 20 | 114,165 (1.142) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 11.970 | 19 | 113,638 (1.136) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 11.907 | 19 | 113,638 (1.136) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 11.885 | 19 | 113,638 (1.136) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 11.999 | 20 | 113,638 (1.136) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 12.041 | 21 | 113,638 (1.136) | yes | - |
| backlog-adp@verify-aged1-6 | 1 | 13.492 | 23 | 89,877 (0.899) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 12.205 | 22 | 96,356 (0.964) | yes | - |
| backlog | 0 | 7.327 | 19 | 87,008 (0.870) | yes | - |
| backlog-adp | 0 | 11.191 | 20 | 114,378 (1.144) | yes | - |
| backlog-adp-refill | 0 | 40.519 | 35 | 114,378 (1.144) | yes | - |
| backlog-owed | 0 | 360.301 | 66 | 111,244 (1.112) | yes | - |
| fixture | 0 | 1.091 | 2 | 77,924 (0.779) | yes | - |

Composed maximum over the 4 backlog windows: 114,378 CPU cycles (1.144 ms), backlog-adp.
Over the windows that released their whole load only: 114,378 (1.144 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3609 | 0 | 113,914 (1.139) | fits |
| save-second | 81422 | 0 | 47,749 (0.477) | fits |
| backlog-adp@blank-0 | 425 | 0 | 114,428 (1.144) | fits |
| backlog-adp@blank-1 | 425 | 0 | 114,483 (1.145) | fits |
| backlog-adp@blank-2 | 425 | 0 | 114,483 (1.145) | fits |
| backlog-adp@blank-3 | 424 | 0 | 114,556 (1.146) | fits |
| backlog-adp@blank-4 | 425 | 0 | 105,442 (1.054) | fits |
| backlog-adp@blank-5 | 425 | 0 | 116,133 (1.161) | fits |
| backlog-adp@blank-6 | 428 | 0 | 114,283 (1.143) | fits |
| backlog-adp@blank-7 | 430 | 0 | 113,008 (1.130) | fits |
| backlog-adp@program-0 | 527 | 0 | 114,446 (1.144) | fits |
| backlog-adp@program-1 | 529 | 0 | 113,409 (1.134) | fits |
| backlog-adp@program-2 | 529 | 0 | 113,945 (1.139) | fits |
| backlog-adp@program-3 | 532 | 0 | 113,409 (1.134) | fits |
| backlog-adp@program-4 | 530 | 0 | 114,542 (1.145) | fits |
| backlog-adp@program-5 | 533 | 0 | 113,987 (1.140) | fits |
| backlog-adp@program-6 | 533 | 0 | 113,987 (1.140) | fits |
| backlog-adp@program-7 | 533 | 0 | 113,409 (1.134) | fits |
| backlog-adp@verify-0 | 623 | 0 | 114,551 (1.146) | fits |
| backlog-adp@verify-1 | 623 | 0 | 114,599 (1.146) | fits |
| backlog-adp@verify-2 | 624 | 0 | 114,526 (1.145) | fits |
| backlog-adp@verify-3 | 623 | 0 | 113,923 (1.139) | fits |
| backlog-adp@verify-4 | 623 | 0 | 113,409 (1.134) | fits |
| backlog-adp@verify-5 | 623 | 0 | 116,176 (1.162) | fits |
| backlog-adp@verify-6 | 626 | 0 | 114,025 (1.140) | fits |
| backlog-adp@verify-7 | 626 | 0 | 113,409 (1.134) | fits |
| backlog-adp@blank-aged2-0 | 932 | 0 | 114,091 (1.141) | fits |
| backlog-adp@blank-aged2-1 | 941 | 0 | 114,168 (1.142) | fits |
| backlog-adp@blank-aged2-2 | 953 | 0 | 114,168 (1.142) | fits |
| backlog-adp@blank-aged2-3 | 966 | 0 | 113,476 (1.135) | fits |
| backlog-adp@blank-aged2-4 | 979 | 0 | 113,476 (1.135) | fits |
| backlog-adp@blank-aged2-5 | 993 | 0 | 113,476 (1.135) | fits |
| backlog-adp@blank-aged2-6 | 1006 | 0 | 113,476 (1.135) | fits |
| backlog-adp@blank-aged2-7 | 1019 | 0 | 96,656 (0.967) | fits |
| backlog-adp@blank-aged1-0 | 833 | 0 | 121,055 (1.211) | fits |
| backlog-adp@blank-aged1-1 | 845 | 0 | 121,107 (1.211) | fits |
| backlog-adp@blank-aged1-2 | 858 | 0 | 121,069 (1.211) | fits |
| backlog-adp@blank-aged1-3 | 872 | 0 | 114,491 (1.145) | fits |
| backlog-adp@blank-aged1-4 | 885 | 0 | 114,407 (1.144) | fits |
| backlog-adp@blank-aged1-5 | 899 | 0 | 114,348 (1.143) | fits |
| backlog-adp@blank-aged1-6 | 912 | 0 | 121,317 (1.213) | fits |
| backlog-adp@blank-aged1-7 | 926 | 0 | 128,083 (1.281) | fits |
| backlog-adp@program-aged2-0 | 1030 | 0 | 114,424 (1.144) | fits |
| backlog-adp@program-aged2-1 | 1043 | 0 | 113,997 (1.140) | fits |
| backlog-adp@program-aged2-2 | 1055 | 0 | 115,364 (1.154) | fits |
| backlog-adp@program-aged2-3 | 1068 | 0 | 114,631 (1.146) | fits |
| backlog-adp@program-aged2-4 | 1083 | 0 | 113,409 (1.134) | fits |
| backlog-adp@program-aged2-5 | 1095 | 0 | 113,554 (1.136) | fits |
| backlog-adp@program-aged2-6 | 1109 | 0 | 113,554 (1.136) | fits |
| backlog-adp@program-aged2-7 | 1122 | 0 | 113,409 (1.134) | fits |
| backlog-adp@program-aged1-0 | 927 | 0 | 114,320 (1.143) | fits |
| backlog-adp@program-aged1-1 | 939 | 0 | 114,313 (1.143) | fits |
| backlog-adp@program-aged1-2 | 951 | 0 | 113,704 (1.137) | fits |
| backlog-adp@program-aged1-3 | 964 | 0 | 113,704 (1.137) | fits |
| backlog-adp@program-aged1-4 | 977 | 0 | 113,704 (1.137) | fits |
| backlog-adp@program-aged1-5 | 991 | 0 | 113,704 (1.137) | fits |
| backlog-adp@program-aged1-6 | 1004 | 0 | 113,704 (1.137) | fits |
| backlog-adp@program-aged1-7 | 1017 | 0 | 113,409 (1.134) | fits |
| backlog-adp@verify-aged2-0 | 1124 | 0 | 114,358 (1.144) | fits |
| backlog-adp@verify-aged2-1 | 1137 | 0 | 114,170 (1.142) | fits |
| backlog-adp@verify-aged2-2 | 1149 | 0 | 113,634 (1.136) | fits |
| backlog-adp@verify-aged2-3 | 1162 | 0 | 113,634 (1.136) | fits |
| backlog-adp@verify-aged2-4 | 1175 | 0 | 113,634 (1.136) | fits |
| backlog-adp@verify-aged2-5 | 1189 | 0 | 113,634 (1.136) | fits |
| backlog-adp@verify-aged2-6 | 1203 | 0 | 113,634 (1.136) | fits |
| backlog-adp@verify-aged2-7 | 1215 | 0 | 113,409 (1.134) | fits |
| backlog-adp@verify-aged1-0 | 1020 | 0 | 114,165 (1.142) | fits |
| backlog-adp@verify-aged1-1 | 1032 | 0 | 113,638 (1.136) | fits |
| backlog-adp@verify-aged1-2 | 1045 | 0 | 113,638 (1.136) | fits |
| backlog-adp@verify-aged1-3 | 1058 | 0 | 113,638 (1.136) | fits |
| backlog-adp@verify-aged1-4 | 1072 | 0 | 113,638 (1.136) | fits |
| backlog-adp@verify-aged1-5 | 1086 | 0 | 113,638 (1.136) | fits |
| backlog-adp@verify-aged1-6 | 1102 | 0 | 113,409 (1.134) | fits |
| backlog-adp@verify-aged1-7 | 1113 | 0 | 113,409 (1.134) | fits |
| adp-advertise | 599 | 0 | 46,666 (0.467) | fits |
| save-held | 3426 | 0 | 112,947 (1.129) | fits |
| save-starved | 42843 | 0 | 93,466 (0.935) | fits |
| acmp-noresp | 2027 | 0 | 113,264 (1.133) | fits |
| save | 610 | 0 | 111,735 (1.117) | fits |
| srp | 291 | 0 | 58,086 (0.581) | fits |
| backlog | 298 | 0 | 87,008 (0.870) | fits |
| backlog-adp | 323 | 0 | 114,378 (1.144) | fits |
| backlog-adp-refill | 338 | 0 | 114,378 (1.144) | fits |
| backlog-owed | 356 | 0 | 111,244 (1.112) | fits |
| acmp-disc | 936 | 0 | 113,362 (1.134) | fits |
| maap | 179 | 0 | 46,666 (0.467) | fits |
| adp-link | 90 | 0 | 46,481 (0.465) | fits |
| adp-gm | 89 | 0 | 46,481 (0.465) | fits |
| adp-discover | 89 | 0 | 46,481 (0.465) | fits |
| control | 89 | 0 | 46,481 (0.465) | fits |
| aecp-fanout | 112 | 0 | 61,270 (0.613) | fits |
| acmp-cmd | 85 | 0 | 46,481 (0.465) | fits |
| aecp | 111 | 0 | 46,481 (0.465) | fits |
| fixture | 159 | 0 | 77,924 (0.779) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | +9.854 ms, 77,586 (0.776 ms), read-back | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 11.647 (18) | 6.353 |
| backlog-adp@blank-aged2-1 | 2 | +8.769 ms, 77,649 (0.776 ms), read-back | none | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 11.652 (18) | 6.348 |
| backlog-adp@blank-aged2-2 | 2 | +7.425 ms, 77,649 (0.776 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 11.584 (18) | 6.416 |
| backlog-adp@blank-aged2-3 | 2 | +6.302 ms, 77,731 (0.777 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 11.569 (18) | 6.431 |
| backlog-adp@blank-aged2-4 | 2 | +5.225 ms, 77,815 (0.778 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 11.778 (18) | 6.222 |
| backlog-adp@blank-aged2-5 | 2 | +4.291 ms, 77,733 (0.777 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 11.746 (18) | 6.254 |
| backlog-adp@blank-aged2-6 | 2 | +2.696 ms, 77,733 (0.777 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 11.675 (18) | 6.325 |
| backlog-adp@blank-aged2-7 | 2 | +1.711 ms, 77,733 (0.777 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 11.840 (18) | 6.160 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 10.892 (18) | 7.108 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 10.796 (18) | 7.204 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 10.787 (18) | 7.213 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 10.868 (18) | 7.132 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 10.930 (18) | 7.070 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 10.982 (18) | 7.018 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 10.928 (18) | 7.072 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 12.229 (18) | 5.771 |
| backlog-adp@program-aged2-0 | 2 | +9.820 ms, 83,517 (0.835 ms), issue | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 11.660 (18) | 6.340 |
| backlog-adp@program-aged2-1 | 2 | +8.572 ms, 83,517 (0.835 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 11.667 (18) | 6.333 |
| backlog-adp@program-aged2-2 | 2 | +7.367 ms, 83,517 (0.835 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 11.587 (18) | 6.413 |
| backlog-adp@program-aged2-3 | 2 | +6.236 ms, 83,599 (0.836 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 11.563 (18) | 6.437 |
| backlog-adp@program-aged2-4 | 2 | +5.265 ms, 83,659 (0.837 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 11.867 (18) | 6.133 |
| backlog-adp@program-aged2-5 | 2 | +4.312 ms, 90,231 (0.902 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 11.748 (18) | 6.252 |
| backlog-adp@program-aged2-6 | 2 | +2.717 ms, 83,767 (0.838 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 11.756 (18) | 6.244 |
| backlog-adp@program-aged2-7 | 2 | +1.735 ms, 83,717 (0.837 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 11.923 (18) | 6.077 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 10.848 (18) | 7.152 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 10.767 (18) | 7.233 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 10.687 (18) | 7.313 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 10.751 (18) | 7.249 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 10.815 (18) | 7.185 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 10.868 (18) | 7.132 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 10.831 (18) | 7.169 |
| backlog-adp@program-aged1-7 | 1 | none | +10.911 ms, 83,104 (0.831 ms), issue | `backlog-adp@program-aged1-7.service.srp.last.if0` | 10.740 (18) | 7.260 |
| backlog-adp@verify-aged2-0 | 2 | +9.811 ms, 85,212 (0.852 ms), read-back | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 11.677 (18) | 6.323 |
| backlog-adp@verify-aged2-1 | 2 | +8.561 ms, 85,212 (0.852 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 11.674 (18) | 6.326 |
| backlog-adp@verify-aged2-2 | 2 | +7.343 ms, 85,212 (0.852 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 11.586 (18) | 6.414 |
| backlog-adp@verify-aged2-3 | 2 | +6.313 ms, 85,437 (0.854 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 11.584 (18) | 6.416 |
| backlog-adp@verify-aged2-4 | 2 | +5.238 ms, 85,433 (0.854 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 11.653 (18) | 6.347 |
| backlog-adp@verify-aged2-5 | 2 | +4.305 ms, 85,224 (0.852 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 11.694 (18) | 6.306 |
| backlog-adp@verify-aged2-6 | 2 | +2.709 ms, 85,119 (0.851 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 11.630 (18) | 6.370 |
| backlog-adp@verify-aged2-7 | 2 | +1.725 ms, 85,463 (0.855 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 11.675 (18) | 6.325 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 10.786 (18) | 7.214 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 10.678 (18) | 7.322 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 10.787 (18) | 7.213 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 10.764 (18) | 7.236 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 10.879 (18) | 7.121 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 10.922 (18) | 7.078 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 10.918 (18) | 7.082 |
| backlog-adp@verify-aged1-7 | 1 | none | +10.941 ms, 84,513 (0.845 ms), read-back | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 10.772 (18) | 7.228 |

Least margin over the aged windows: 5.771 ms, `backlog-adp@blank-aged1-7.service.srp.last.if0` at 12.229 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6029.841 | 6,070 | 102 | 2 | 30.948 | yes | within |
| save-held | 2018.151 | 4,070 | 102 | - | 14.206 | no | within |
| save-starved | 4048.118 | 4,070 | 102 | - | 31.043 | yes | within |
| save | 2018.418 | 4,070 | 102 | - | 10.950 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 113,914 (1.139) | 95,681 (0.957) |
| save-second | 520 | 96,376 (0.964) | 95,318 (0.953) |
| backlog-adp@blank-0 | 299 | 88,132 (0.881) | 76,128 (0.761) |
| backlog-adp@blank-1 | 299 | 88,238 (0.882) | 76,063 (0.761) |
| backlog-adp@blank-2 | 299 | 88,155 (0.882) | 76,060 (0.761) |
| backlog-adp@blank-3 | 299 | 88,155 (0.882) | 76,060 (0.761) |
| backlog-adp@blank-4 | 299 | 88,263 (0.883) | 76,063 (0.761) |
| backlog-adp@blank-5 | 299 | 88,069 (0.881) | 76,036 (0.760) |
| backlog-adp@blank-6 | 299 | 94,997 (0.950) | 76,183 (0.762) |
| backlog-adp@blank-7 | 300 | 113,008 (1.130) | 76,207 (0.762) |
| backlog-adp@program-0 | 328 | 113,409 (1.134) | 81,887 (0.819) |
| backlog-adp@program-1 | 328 | 113,409 (1.134) | 81,890 (0.819) |
| backlog-adp@program-2 | 328 | 113,409 (1.134) | 81,969 (0.820) |
| backlog-adp@program-3 | 329 | 113,409 (1.134) | 81,887 (0.819) |
| backlog-adp@program-4 | 329 | 113,409 (1.134) | 81,109 (0.811) |
| backlog-adp@program-5 | 329 | 113,409 (1.134) | 81,109 (0.811) |
| backlog-adp@program-6 | 329 | 113,409 (1.134) | 81,109 (0.811) |
| backlog-adp@program-7 | 329 | 113,409 (1.134) | 81,109 (0.811) |
| backlog-adp@verify-0 | 355 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-1 | 355 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-2 | 355 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-3 | 355 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-4 | 355 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-5 | 355 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-6 | 355 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-7 | 355 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@blank-aged2-0 | 297 | 77,586 (0.776) | 76,053 (0.761) |
| backlog-adp@blank-aged2-1 | 297 | 77,649 (0.776) | 76,116 (0.761) |
| backlog-adp@blank-aged2-2 | 297 | 77,649 (0.776) | 76,116 (0.761) |
| backlog-adp@blank-aged2-3 | 297 | 77,731 (0.777) | 76,116 (0.761) |
| backlog-adp@blank-aged2-4 | 297 | 77,815 (0.778) | 76,200 (0.762) |
| backlog-adp@blank-aged2-5 | 297 | 77,733 (0.777) | 76,200 (0.762) |
| backlog-adp@blank-aged2-6 | 298 | 85,777 (0.858) | 76,200 (0.762) |
| backlog-adp@blank-aged2-7 | 298 | 88,135 (0.881) | 76,200 (0.762) |
| backlog-adp@blank-aged1-0 | 297 | 121,055 (1.211) | 76,511 (0.765) |
| backlog-adp@blank-aged1-1 | 297 | 121,107 (1.211) | 76,511 (0.765) |
| backlog-adp@blank-aged1-2 | 297 | 121,069 (1.211) | 76,511 (0.765) |
| backlog-adp@blank-aged1-3 | 297 | 114,491 (1.145) | 76,367 (0.764) |
| backlog-adp@blank-aged1-4 | 297 | 114,407 (1.144) | 76,364 (0.764) |
| backlog-adp@blank-aged1-5 | 297 | 114,348 (1.143) | 76,364 (0.764) |
| backlog-adp@blank-aged1-6 | 298 | 121,317 (1.213) | 76,364 (0.764) |
| backlog-adp@blank-aged1-7 | 298 | 128,083 (1.281) | 76,364 (0.764) |
| backlog-adp@program-aged2-0 | 326 | 113,409 (1.134) | 81,759 (0.818) |
| backlog-adp@program-aged2-1 | 326 | 113,409 (1.134) | 81,759 (0.818) |
| backlog-adp@program-aged2-2 | 326 | 113,409 (1.134) | 81,759 (0.818) |
| backlog-adp@program-aged2-3 | 326 | 113,409 (1.134) | 81,759 (0.818) |
| backlog-adp@program-aged2-4 | 326 | 113,409 (1.134) | 81,843 (0.818) |
| backlog-adp@program-aged2-5 | 326 | 113,409 (1.134) | 81,843 (0.818) |
| backlog-adp@program-aged2-6 | 327 | 113,409 (1.134) | 81,843 (0.818) |
| backlog-adp@program-aged2-7 | 327 | 113,409 (1.134) | 81,843 (0.818) |
| backlog-adp@program-aged1-0 | 326 | 113,409 (1.134) | 81,802 (0.818) |
| backlog-adp@program-aged1-1 | 326 | 113,409 (1.134) | 81,822 (0.818) |
| backlog-adp@program-aged1-2 | 326 | 113,409 (1.134) | 81,825 (0.818) |
| backlog-adp@program-aged1-3 | 326 | 113,409 (1.134) | 81,743 (0.817) |
| backlog-adp@program-aged1-4 | 326 | 113,409 (1.134) | 81,743 (0.817) |
| backlog-adp@program-aged1-5 | 326 | 113,409 (1.134) | 81,743 (0.817) |
| backlog-adp@program-aged1-6 | 327 | 113,409 (1.134) | 81,743 (0.817) |
| backlog-adp@program-aged1-7 | 326 | 113,409 (1.134) | 81,514 (0.815) |
| backlog-adp@verify-aged2-0 | 355 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-aged2-1 | 355 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-aged2-2 | 355 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-aged2-3 | 355 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-aged2-4 | 355 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-aged2-5 | 355 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-aged2-6 | 356 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-aged2-7 | 356 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-aged1-0 | 355 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-aged1-1 | 355 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-aged1-2 | 355 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-aged1-3 | 355 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-aged1-4 | 355 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-aged1-5 | 355 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-aged1-6 | 356 | 113,409 (1.134) | 95,616 (0.956) |
| backlog-adp@verify-aged1-7 | 355 | 113,409 (1.134) | 95,616 (0.956) |
| adp-advertise | 578 | 46,481 (0.465) | 3,010 (0.030) |
| save-held | 722 | 112,947 (1.129) | 95,352 (0.954) |
| save-starved | 418 | 97,378 (0.974) | 96,212 (0.962) |
| acmp-noresp | 615 | 113,264 (1.133) | 95,616 (0.956) |
| save | 585 | 111,735 (1.117) | 95,352 (0.954) |
| srp | 272 | 46,481 (0.465) | 3,010 (0.030) |
| backlog | 265 | 46,481 (0.465) | 3,010 (0.030) |
| backlog-adp | 271 | 46,481 (0.465) | 3,010 (0.030) |
| backlog-adp-refill | 274 | 46,481 (0.465) | 3,010 (0.030) |
| backlog-owed | 306 | 46,481 (0.465) | 3,089 (0.031) |
| acmp-disc | 305 | 113,362 (1.134) | 95,616 (0.956) |
| maap | 166 | 46,481 (0.465) | 3,010 (0.030) |
| adp-link | 80 | 46,481 (0.465) | 2,943 (0.029) |
| adp-gm | 80 | 46,481 (0.465) | 2,943 (0.029) |
| adp-discover | 80 | 46,481 (0.465) | 2,943 (0.029) |
| control | 80 | 46,481 (0.465) | 2,943 (0.029) |
| aecp-fanout | 79 | 46,481 (0.465) | 2,943 (0.029) |
| acmp-cmd | 65 | 46,481 (0.465) | 2,943 (0.029) |
| aecp | 78 | 46,481 (0.465) | 2,943 (0.029) |
| fixture | 54 | 46,481 (0.465) | 2,857 (0.029) |

Longest pass that carries a step: 128,083 CPU cycles (1.281 ms), backlog-adp@blank-aged1-7; longest step: 96,212 (0.962 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 14,179 | 0.142 | 20 | 20 | fits | 27,401 | 20 (14) | 0.873 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 364,644 | 3.646 | 20 | 20 | fits | 96,985 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 146,526 | 1.465 | 20 | 200 | fits | 81,789 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 452,668 | 4.527 | 20 | 200 | fits | 96,985 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 147,438 | 1.474 | 20 | 20 | fits | 81,789 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 607,095 | 6.071 | 20 | 20 | fits | 76,519 | 44 | 0.678 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 151,023 | 1.510 | 20 | 24 | fits | 81,789 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 1,063,388 | 10.634 | 20 | 24 | fits | 47,666 | 30 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 149,983 | 1.500 | 20 | 50 | fits | 81,789 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 456,344 | 4.563 | 20 | 50 | fits | 96,985 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 263,956 | 2.640 | 18 | 18 | fits | 114,428 | 138 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,154,341 | 11.543 | 18 | 18 | fits | 22,349 | 14 | 0.789 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 295,972 | 2.960 | 20 | 20 | fits | 96,985 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 77,857 | 0.779 | 20 | 200 | fits | 81,603 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 383,996 | 3.840 | 20 | 200 | fits | 96,985 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 78,769 | 0.788 | 20 | 20 | fits | 81,603 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 538,423 | 5.384 | 20 | 20 | fits | 76,519 | 44 | 0.678 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 82,354 | 0.824 | 20 | 24 | fits | 81,603 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 1,003,363 | 10.034 | 20 | 24 | fits | 47,419 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 81,314 | 0.813 | 20 | 50 | fits | 81,603 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 387,672 | 3.877 | 20 | 50 | fits | 96,985 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 195,342 | 1.953 | 18 | 18 | fits | 114,483 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 1,083,797 | 10.838 | 18 | 18 | fits | 22,212 | 14 | 0.784 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 302,131 | 3.021 | 20 | 20 | fits | 96,985 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 84,016 | 0.840 | 20 | 200 | fits | 81,603 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 390,155 | 3.902 | 20 | 200 | fits | 96,985 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 84,928 | 0.849 | 20 | 20 | fits | 81,603 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 524,270 | 5.243 | 20 | 20 | fits | 78,504 | 51 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 88,513 | 0.885 | 20 | 24 | fits | 81,603 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 1,008,664 | 10.087 | 20 | 24 | fits | 47,461 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 87,473 | 0.875 | 20 | 50 | fits | 81,603 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 393,831 | 3.938 | 20 | 50 | fits | 96,985 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 201,501 | 2.015 | 18 | 18 | fits | 114,483 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 1,089,036 | 10.890 | 18 | 18 | fits | 22,256 | 14 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 303,171 | 3.032 | 20 | 20 | fits | 101,152 | 88 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 81,122 | 0.811 | 20 | 200 | fits | 81,743 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 391,501 | 3.915 | 20 | 200 | fits | 101,152 | 88 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 82,034 | 0.820 | 20 | 20 | fits | 81,743 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 546,686 | 5.467 | 20 | 20 | fits | 76,863 | 45 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 85,619 | 0.856 | 20 | 24 | fits | 81,743 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 1,031,367 | 10.314 | 20 | 24 | fits | 47,470 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 84,579 | 0.846 | 20 | 50 | fits | 81,743 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 395,177 | 3.952 | 20 | 50 | fits | 101,152 | 88 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 198,680 | 1.987 | 18 | 18 | fits | 114,556 | 138 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 1,082,128 | 10.821 | 18 | 18 | fits | 22,476 | 14 | 0.791 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 290,248 | 2.902 | 20 | 20 | fits | 97,200 | 82 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 77,857 | 0.779 | 20 | 200 | fits | 81,603 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 378,290 | 3.783 | 20 | 200 | fits | 97,200 | 82 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 78,769 | 0.788 | 20 | 20 | fits | 81,603 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 511,368 | 5.114 | 20 | 20 | fits | 54,852 | 36 | 0.636 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 82,354 | 0.824 | 20 | 24 | fits | 81,603 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 996,535 | 9.965 | 20 | 24 | fits | 47,495 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 81,314 | 0.813 | 20 | 50 | fits | 81,603 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 381,966 | 3.820 | 20 | 50 | fits | 97,200 | 82 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 186,301 | 1.863 | 18 | 18 | fits | 105,442 | 135 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 1,084,283 | 10.843 | 18 | 18 | fits | 29,618 | 17 | 0.718 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 304,399 | 3.044 | 20 | 20 | fits | 75,006 | 73 | 0.611 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 84,098 | 0.841 | 20 | 200 | fits | 81,685 | 136 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 370,168 | 3.702 | 20 | 200 | fits | 75,006 | 73 | 0.611 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 85,010 | 0.850 | 20 | 20 | fits | 81,685 | 136 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 583,716 | 5.837 | 20 | 20 | fits | 65,965 | 37 | 0.731 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 88,595 | 0.886 | 20 | 24 | fits | 81,685 | 136 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 1,015,272 | 10.153 | 20 | 24 | fits | 47,473 | 29 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 87,555 | 0.876 | 20 | 50 | fits | 81,685 | 136 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 373,844 | 3.738 | 20 | 50 | fits | 75,006 | 73 | 0.611 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 203,233 | 2.032 | 18 | 18 | fits | 116,133 | 144 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 1,095,861 | 10.959 | 18 | 18 | fits | 22,248 | 14 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 343,604 | 3.436 | 20 | 20 | fits | 87,889 | 55 | 0.689 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 78,986 | 0.790 | 20 | 200 | fits | 81,464 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 423,901 | 4.239 | 20 | 200 | fits | 87,889 | 55 | 0.689 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 79,898 | 0.799 | 20 | 20 | fits | 81,464 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 566,232 | 5.662 | 20 | 20 | fits | 64,944 | 37 | 0.723 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 83,483 | 0.835 | 20 | 24 | fits | 81,464 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 977,636 | 9.776 | 20 | 24 | fits | 47,505 | 30 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 82,443 | 0.824 | 20 | 50 | fits | 81,464 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 339,688 | 3.397 | 20 | 50 | fits | 70,457 | 62 | 0.701 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 196,271 | 1.963 | 18 | 18 | fits | 114,283 | 138 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 1,088,207 | 10.882 | 18 | 18 | fits | 22,312 | 15 | 0.777 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 388,438 | 3.884 | 20 | 20 | fits | 87,608 | 55 | 0.688 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 116,561 | 1.166 | 20 | 200 | fits | 81,967 | 137 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 468,454 | 4.685 | 20 | 200 | fits | 87,608 | 55 | 0.688 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 117,473 | 1.175 | 20 | 20 | fits | 81,967 | 137 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 610,898 | 6.109 | 20 | 20 | fits | 65,117 | 38 | 0.723 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 39,091 | 0.391 | 20 | 24 | fits | 40,197 | 63 | 0.549 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 998,324 | 9.983 | 20 | 24 | fits | 47,486 | 30 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 38,051 | 0.381 | 20 | 50 | fits | 40,197 | 63 | 0.549 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 304,339 | 3.043 | 20 | 50 | fits | 96,087 | 96 | 0.611 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 208,187 | 2.082 | 18 | 18 | fits | 88,624 | 103 | 0.689 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 1,089,070 | 10.891 | 18 | 18 | fits | 22,248 | 14 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 296,476 | 2.965 | 20 | 20 | fits | 96,865 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 78,425 | 0.784 | 20 | 200 | fits | 81,529 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 384,380 | 3.844 | 20 | 200 | fits | 96,865 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 79,337 | 0.793 | 20 | 20 | fits | 81,529 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 543,615 | 5.436 | 20 | 20 | fits | 76,945 | 45 | 0.678 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 82,922 | 0.829 | 20 | 24 | fits | 81,529 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 1,028,068 | 10.281 | 20 | 24 | fits | 47,336 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 81,882 | 0.819 | 20 | 50 | fits | 81,529 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 388,056 | 3.881 | 20 | 50 | fits | 96,865 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 195,873 | 1.959 | 18 | 18 | fits | 114,446 | 138 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 1,078,879 | 10.789 | 18 | 18 | fits | 22,461 | 14 | 0.791 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 278,180 | 2.782 | 20 | 20 | fits | 97,971 | 82 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 81,690 | 0.817 | 20 | 200 | fits | 81,669 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 366,800 | 3.668 | 20 | 200 | fits | 97,971 | 82 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 82,602 | 0.826 | 20 | 20 | fits | 81,669 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 521,723 | 5.217 | 20 | 20 | fits | 76,756 | 45 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 86,187 | 0.862 | 20 | 24 | fits | 81,669 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 983,947 | 9.839 | 20 | 24 | fits | 47,479 | 29 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 85,147 | 0.851 | 20 | 50 | fits | 81,669 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 370,476 | 3.705 | 20 | 50 | fits | 97,971 | 82 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 272,440 | 2.724 | 18 | 18 | fits | 108,567 | 103 | 0.646 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 1,093,844 | 10.938 | 18 | 18 | fits | 22,212 | 14 | 0.784 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 300,005 | 3.000 | 20 | 20 | fits | 96,865 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 82,399 | 0.824 | 20 | 200 | fits | 81,339 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 387,909 | 3.879 | 20 | 200 | fits | 96,865 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 83,311 | 0.833 | 20 | 20 | fits | 81,339 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 592,416 | 5.924 | 20 | 20 | fits | 65,077 | 37 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 86,896 | 0.869 | 20 | 24 | fits | 81,339 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 1,028,094 | 10.281 | 20 | 24 | fits | 47,444 | 30 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 85,856 | 0.859 | 20 | 50 | fits | 81,339 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 391,585 | 3.916 | 20 | 50 | fits | 96,865 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 199,346 | 1.993 | 18 | 18 | fits | 113,945 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 1,079,066 | 10.791 | 18 | 18 | fits | 22,421 | 15 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 339,251 | 3.393 | 20 | 20 | fits | 88,075 | 55 | 0.692 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 76,149 | 0.761 | 20 | 200 | fits | 81,339 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 419,734 | 4.197 | 20 | 200 | fits | 88,075 | 55 | 0.692 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 77,061 | 0.771 | 20 | 20 | fits | 81,339 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 541,805 | 5.418 | 20 | 20 | fits | 66,822 | 44 | 0.720 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 80,646 | 0.806 | 20 | 24 | fits | 81,339 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 981,306 | 9.813 | 20 | 24 | fits | 47,605 | 29 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 79,606 | 0.796 | 20 | 50 | fits | 81,339 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 335,335 | 3.353 | 20 | 50 | fits | 96,209 | 96 | 0.612 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 239,061 | 2.391 | 18 | 18 | fits | 80,966 | 62 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 1,091,281 | 10.913 | 18 | 18 | fits | 22,205 | 14 | 0.784 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 302,795 | 3.028 | 20 | 20 | fits | 97,101 | 82 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 80,311 | 0.803 | 20 | 200 | fits | 82,201 | 135 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 390,738 | 3.907 | 20 | 200 | fits | 97,101 | 82 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 81,223 | 0.812 | 20 | 20 | fits | 82,201 | 135 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 545,756 | 5.458 | 20 | 20 | fits | 76,834 | 45 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 84,808 | 0.848 | 20 | 24 | fits | 82,201 | 135 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 1,030,905 | 10.309 | 20 | 24 | fits | 47,336 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 83,768 | 0.838 | 20 | 50 | fits | 82,201 | 135 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 394,414 | 3.944 | 20 | 50 | fits | 97,101 | 82 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 197,855 | 1.979 | 18 | 18 | fits | 114,542 | 138 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 1,081,716 | 10.817 | 18 | 18 | fits | 22,461 | 14 | 0.791 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 300,331 | 3.003 | 20 | 20 | fits | 96,865 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 82,683 | 0.827 | 20 | 200 | fits | 81,382 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 388,235 | 3.882 | 20 | 200 | fits | 96,865 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 83,595 | 0.836 | 20 | 20 | fits | 81,382 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 542,665 | 5.427 | 20 | 20 | fits | 76,564 | 44 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 87,180 | 0.872 | 20 | 24 | fits | 81,382 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 998,471 | 9.985 | 20 | 24 | fits | 47,453 | 30 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 86,140 | 0.861 | 20 | 50 | fits | 81,382 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 391,911 | 3.919 | 20 | 50 | fits | 96,865 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 199,672 | 1.997 | 18 | 18 | fits | 113,987 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 1,079,319 | 10.793 | 18 | 18 | fits | 22,384 | 15 | 0.779 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 294,081 | 2.941 | 20 | 20 | fits | 96,865 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 76,433 | 0.764 | 20 | 200 | fits | 81,382 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 381,985 | 3.820 | 20 | 200 | fits | 96,865 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 77,345 | 0.773 | 20 | 20 | fits | 81,382 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 566,226 | 5.662 | 20 | 20 | fits | 67,803 | 44 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 80,930 | 0.809 | 20 | 24 | fits | 81,382 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 1,006,697 | 10.067 | 20 | 24 | fits | 47,686 | 29 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 79,890 | 0.799 | 20 | 50 | fits | 81,382 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 385,661 | 3.857 | 20 | 50 | fits | 96,865 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 193,422 | 1.934 | 18 | 18 | fits | 113,987 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 1,087,124 | 10.871 | 18 | 18 | fits | 22,256 | 14 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 347,191 | 3.472 | 20 | 20 | fits | 88,021 | 56 | 0.687 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 79,698 | 0.797 | 20 | 200 | fits | 81,522 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 427,344 | 4.273 | 20 | 200 | fits | 88,021 | 56 | 0.687 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 80,610 | 0.806 | 20 | 20 | fits | 81,522 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 570,214 | 5.702 | 20 | 20 | fits | 65,225 | 38 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 84,195 | 0.842 | 20 | 24 | fits | 81,522 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 1,010,829 | 10.108 | 20 | 24 | fits | 47,553 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 83,155 | 0.832 | 20 | 50 | fits | 81,522 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 342,999 | 3.430 | 20 | 50 | fits | 100,080 | 103 | 0.619 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 242,854 | 2.429 | 18 | 18 | fits | 81,041 | 62 | 0.733 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 1,091,201 | 10.912 | 18 | 18 | fits | 22,256 | 14 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 369,297 | 3.693 | 20 | 20 | fits | 96,865 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 151,107 | 1.511 | 20 | 200 | fits | 82,040 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 457,201 | 4.572 | 20 | 200 | fits | 96,865 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 152,019 | 1.520 | 20 | 20 | fits | 82,040 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 611,631 | 6.116 | 20 | 20 | fits | 76,564 | 44 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 155,604 | 1.556 | 20 | 24 | fits | 82,040 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 1,067,924 | 10.679 | 20 | 24 | fits | 47,666 | 30 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 154,564 | 1.546 | 20 | 50 | fits | 82,040 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 460,877 | 4.609 | 20 | 50 | fits | 96,865 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 268,660 | 2.687 | 18 | 18 | fits | 114,551 | 138 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,158,619 | 11.586 | 18 | 18 | fits | 22,212 | 14 | 0.784 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 300,476 | 3.005 | 20 | 20 | fits | 96,865 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 82,272 | 0.823 | 20 | 200 | fits | 81,768 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 388,380 | 3.884 | 20 | 200 | fits | 96,865 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 83,184 | 0.832 | 20 | 20 | fits | 81,768 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 542,810 | 5.428 | 20 | 20 | fits | 76,564 | 44 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 86,769 | 0.868 | 20 | 24 | fits | 81,768 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 1,009,749 | 10.097 | 20 | 24 | fits | 47,533 | 29 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 85,729 | 0.857 | 20 | 50 | fits | 81,768 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 392,056 | 3.921 | 20 | 50 | fits | 96,865 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 199,873 | 1.999 | 18 | 18 | fits | 114,599 | 138 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 1,090,392 | 10.904 | 18 | 18 | fits | 22,263 | 14 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 297,138 | 2.971 | 20 | 20 | fits | 96,865 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 79,007 | 0.790 | 20 | 200 | fits | 81,628 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 385,042 | 3.850 | 20 | 200 | fits | 96,865 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 79,919 | 0.799 | 20 | 20 | fits | 81,628 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 519,256 | 5.193 | 20 | 20 | fits | 78,549 | 51 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 83,504 | 0.835 | 20 | 24 | fits | 81,628 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 981,235 | 9.812 | 20 | 24 | fits | 47,486 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 82,464 | 0.825 | 20 | 50 | fits | 81,628 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 388,718 | 3.887 | 20 | 50 | fits | 96,865 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 196,535 | 1.965 | 18 | 18 | fits | 114,526 | 138 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 1,091,144 | 10.911 | 18 | 18 | fits | 22,212 | 14 | 0.784 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 323,124 | 3.231 | 20 | 20 | fits | 92,221 | 65 | 0.681 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 116,823 | 1.168 | 20 | 200 | fits | 82,044 | 137 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 403,974 | 4.040 | 20 | 200 | fits | 92,221 | 65 | 0.681 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 117,735 | 1.177 | 20 | 20 | fits | 82,044 | 137 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 558,693 | 5.587 | 20 | 20 | fits | 76,852 | 45 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 39,276 | 0.393 | 20 | 24 | fits | 40,525 | 63 | 0.559 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 995,873 | 9.959 | 20 | 24 | fits | 47,470 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 38,236 | 0.382 | 20 | 50 | fits | 40,525 | 63 | 0.559 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 315,429 | 3.154 | 20 | 50 | fits | 81,616 | 71 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 233,748 | 2.337 | 18 | 18 | fits | 113,923 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 1,083,600 | 10.836 | 18 | 18 | fits | 29,611 | 17 | 0.718 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 294,703 | 2.947 | 20 | 20 | fits | 97,077 | 82 | 0.648 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 82,272 | 0.823 | 20 | 200 | fits | 81,768 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 382,622 | 3.826 | 20 | 200 | fits | 97,077 | 82 | 0.648 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 83,184 | 0.832 | 20 | 20 | fits | 81,768 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 515,703 | 5.157 | 20 | 20 | fits | 54,897 | 36 | 0.637 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 86,769 | 0.868 | 20 | 24 | fits | 81,768 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 1,000,883 | 10.009 | 20 | 24 | fits | 47,495 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 85,729 | 0.857 | 20 | 50 | fits | 81,768 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 386,298 | 3.863 | 20 | 50 | fits | 97,077 | 82 | 0.648 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 190,785 | 1.908 | 18 | 18 | fits | 105,511 | 135 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 1,088,631 | 10.886 | 18 | 18 | fits | 29,618 | 17 | 0.718 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 299,406 | 2.994 | 20 | 20 | fits | 75,074 | 73 | 0.612 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 79,089 | 0.791 | 20 | 200 | fits | 81,710 | 136 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 365,243 | 3.652 | 20 | 200 | fits | 75,074 | 73 | 0.612 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 80,001 | 0.800 | 20 | 20 | fits | 81,710 | 136 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 578,931 | 5.789 | 20 | 20 | fits | 65,965 | 37 | 0.731 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 83,586 | 0.836 | 20 | 24 | fits | 81,710 | 136 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 1,010,487 | 10.105 | 20 | 24 | fits | 47,473 | 29 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 82,546 | 0.825 | 20 | 50 | fits | 81,710 | 136 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 368,919 | 3.689 | 20 | 50 | fits | 75,074 | 73 | 0.612 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 198,267 | 1.983 | 18 | 18 | fits | 116,176 | 144 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 1,090,847 | 10.908 | 18 | 18 | fits | 22,256 | 14 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 347,495 | 3.475 | 20 | 20 | fits | 87,847 | 55 | 0.689 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 83,048 | 0.830 | 20 | 200 | fits | 81,417 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 427,750 | 4.277 | 20 | 200 | fits | 87,847 | 55 | 0.689 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 83,960 | 0.840 | 20 | 20 | fits | 81,417 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 570,126 | 5.701 | 20 | 20 | fits | 64,944 | 37 | 0.723 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 87,545 | 0.875 | 20 | 24 | fits | 81,417 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 981,357 | 9.814 | 20 | 24 | fits | 47,453 | 30 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 86,505 | 0.865 | 20 | 50 | fits | 81,417 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 343,579 | 3.436 | 20 | 50 | fits | 70,438 | 62 | 0.702 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 200,075 | 2.001 | 18 | 18 | fits | 114,025 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 1,091,960 | 10.920 | 18 | 18 | fits | 22,320 | 15 | 0.777 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 343,428 | 3.434 | 20 | 20 | fits | 88,075 | 55 | 0.692 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 80,063 | 0.801 | 20 | 200 | fits | 81,557 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 423,911 | 4.239 | 20 | 200 | fits | 88,075 | 55 | 0.692 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 80,975 | 0.810 | 20 | 20 | fits | 81,557 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 566,263 | 5.663 | 20 | 20 | fits | 65,025 | 37 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 84,560 | 0.846 | 20 | 24 | fits | 81,557 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 992,400 | 9.924 | 20 | 24 | fits | 47,354 | 30 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 83,520 | 0.835 | 20 | 50 | fits | 81,557 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 339,512 | 3.395 | 20 | 50 | fits | 96,209 | 96 | 0.612 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 243,238 | 2.432 | 18 | 18 | fits | 81,081 | 62 | 0.733 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 1,090,516 | 10.905 | 18 | 18 | fits | 29,611 | 17 | 0.718 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 304,858 | 3.049 | 20 | 20 | fits | 97,100 | 82 | 0.648 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 86,570 | 0.866 | 20 | 200 | fits | 84,746 | 133 | 0.537 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 392,729 | 3.927 | 20 | 200 | fits | 97,100 | 82 | 0.648 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 87,482 | 0.875 | 20 | 20 | fits | 84,746 | 133 | 0.537 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 557,136 | 5.571 | 20 | 20 | fits | 76,898 | 44 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 91,067 | 0.911 | 20 | 24 | fits | 84,746 | 133 | 0.537 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 1,109,913 | 11.099 | 20 | 24 | fits | 48,076 | 29 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 90,027 | 0.900 | 20 | 50 | fits | 84,746 | 133 | 0.537 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 396,405 | 3.964 | 20 | 50 | fits | 97,100 | 82 | 0.648 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 203,663 | 2.037 | 18 | 18 | fits | 114,091 | 139 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 1,164,737 | 11.647 | 18 | 18 | fits | 26,461 | 21 | 0.795 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 307,709 | 3.077 | 20 | 20 | fits | 97,232 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 80,888 | 0.809 | 20 | 200 | fits | 81,483 | 133 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 396,159 | 3.962 | 20 | 200 | fits | 97,232 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 81,800 | 0.818 | 20 | 20 | fits | 81,483 | 133 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 550,876 | 5.509 | 20 | 20 | fits | 76,626 | 44 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 85,385 | 0.854 | 20 | 24 | fits | 81,483 | 133 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 1,077,023 | 10.770 | 20 | 24 | fits | 49,429 | 36 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 84,345 | 0.843 | 20 | 50 | fits | 81,483 | 133 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 399,835 | 3.998 | 20 | 50 | fits | 97,232 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 198,058 | 1.981 | 18 | 18 | fits | 114,168 | 139 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 1,165,247 | 11.652 | 18 | 18 | fits | 29,667 | 18 | 0.710 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 308,638 | 3.086 | 20 | 20 | fits | 96,844 | 81 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 81,611 | 0.816 | 20 | 200 | fits | 81,483 | 133 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 396,492 | 3.965 | 20 | 200 | fits | 96,844 | 81 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 82,523 | 0.825 | 20 | 20 | fits | 81,483 | 133 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 550,856 | 5.509 | 20 | 20 | fits | 76,626 | 44 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 86,108 | 0.861 | 20 | 24 | fits | 81,483 | 133 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 1,100,078 | 11.001 | 20 | 24 | fits | 47,580 | 30 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 85,068 | 0.851 | 20 | 50 | fits | 81,483 | 133 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 400,168 | 4.002 | 20 | 50 | fits | 96,844 | 81 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 198,781 | 1.988 | 18 | 18 | fits | 114,168 | 139 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,158,375 | 11.584 | 18 | 18 | fits | 29,761 | 18 | 0.714 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 298,573 | 2.986 | 20 | 20 | fits | 96,857 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 81,573 | 0.816 | 20 | 200 | fits | 80,676 | 132 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 386,477 | 3.865 | 20 | 200 | fits | 96,857 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 82,485 | 0.825 | 20 | 20 | fits | 80,676 | 132 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 540,891 | 5.409 | 20 | 20 | fits | 76,556 | 44 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 86,070 | 0.861 | 20 | 24 | fits | 80,676 | 132 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 1,068,952 | 10.690 | 20 | 24 | fits | 47,640 | 30 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 85,030 | 0.850 | 20 | 50 | fits | 80,676 | 132 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 390,153 | 3.902 | 20 | 50 | fits | 96,857 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 198,051 | 1.981 | 18 | 18 | fits | 113,476 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,156,937 | 11.569 | 18 | 18 | fits | 29,667 | 18 | 0.710 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 297,736 | 2.977 | 20 | 20 | fits | 96,857 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 80,736 | 0.807 | 20 | 200 | fits | 80,676 | 132 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 385,640 | 3.856 | 20 | 200 | fits | 96,857 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 81,648 | 0.816 | 20 | 20 | fits | 80,676 | 132 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 653,904 | 6.539 | 20 | 20 | fits | 58,170 | 34 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 85,233 | 0.852 | 20 | 24 | fits | 80,676 | 132 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 1,097,183 | 10.972 | 20 | 24 | fits | 47,506 | 29 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 84,193 | 0.842 | 20 | 50 | fits | 80,676 | 132 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 389,316 | 3.893 | 20 | 50 | fits | 96,857 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 197,214 | 1.972 | 18 | 18 | fits | 113,476 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,177,802 | 11.778 | 18 | 18 | fits | 22,255 | 14 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 296,899 | 2.969 | 20 | 20 | fits | 74,804 | 72 | 0.613 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 79,899 | 0.799 | 20 | 200 | fits | 80,676 | 132 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 362,750 | 3.627 | 20 | 200 | fits | 74,804 | 72 | 0.613 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 80,811 | 0.808 | 20 | 20 | fits | 80,676 | 132 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 624,291 | 6.243 | 20 | 20 | fits | 67,303 | 44 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 84,396 | 0.844 | 20 | 24 | fits | 80,676 | 132 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 1,064,677 | 10.647 | 20 | 24 | fits | 47,455 | 29 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 83,356 | 0.834 | 20 | 50 | fits | 80,676 | 132 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 366,426 | 3.664 | 20 | 50 | fits | 74,804 | 72 | 0.613 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 196,377 | 1.964 | 18 | 18 | fits | 113,476 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,174,565 | 11.746 | 18 | 18 | fits | 22,197 | 14 | 0.784 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 423,863 | 4.239 | 20 | 20 | fits | 89,828 | 62 | 0.688 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 79,062 | 0.791 | 20 | 200 | fits | 80,676 | 132 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 504,192 | 5.042 | 20 | 200 | fits | 89,828 | 62 | 0.688 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 79,974 | 0.800 | 20 | 20 | fits | 80,676 | 132 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 647,248 | 6.472 | 20 | 20 | fits | 65,210 | 38 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 83,559 | 0.836 | 20 | 24 | fits | 80,676 | 132 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 1,087,203 | 10.872 | 20 | 24 | fits | 47,464 | 29 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 82,519 | 0.825 | 20 | 50 | fits | 80,676 | 132 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 418,040 | 4.180 | 20 | 50 | fits | 72,369 | 88 | 0.536 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 195,540 | 1.955 | 18 | 18 | fits | 113,476 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,167,539 | 11.675 | 18 | 18 | fits | 22,248 | 14 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 421,361 | 4.214 | 20 | 20 | fits | 87,828 | 56 | 0.685 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 78,225 | 0.782 | 20 | 200 | fits | 80,676 | 132 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 501,329 | 5.013 | 20 | 200 | fits | 87,828 | 56 | 0.685 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 79,137 | 0.791 | 20 | 20 | fits | 80,676 | 132 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 644,111 | 6.441 | 20 | 20 | fits | 65,136 | 38 | 0.720 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 82,722 | 0.827 | 20 | 24 | fits | 80,676 | 132 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 1,076,744 | 10.767 | 20 | 24 | fits | 39,917 | 25 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 81,682 | 0.817 | 20 | 50 | fits | 80,676 | 132 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 417,177 | 4.172 | 20 | 50 | fits | 96,656 | 103 | 0.598 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 169,423 | 1.694 | 18 | 18 | fits | 88,196 | 103 | 0.688 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,184,016 | 11.840 | 18 | 18 | fits | 22,197 | 14 | 0.784 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 337,117 | 3.371 | 20 | 20 | fits | 89,308 | 58 | 0.675 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 116,410 | 1.164 | 20 | 200 | fits | 81,369 | 135 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 417,427 | 4.174 | 20 | 200 | fits | 89,308 | 58 | 0.675 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 117,322 | 1.173 | 20 | 20 | fits | 81,369 | 135 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 571,557 | 5.716 | 20 | 20 | fits | 76,578 | 44 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 39,538 | 0.395 | 20 | 24 | fits | 42,161 | 70 | 0.550 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 1,008,205 | 10.082 | 20 | 24 | fits | 53,465 | 37 | 0.761 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 38,498 | 0.385 | 20 | 50 | fits | 42,161 | 70 | 0.550 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 331,795 | 3.318 | 20 | 50 | fits | 89,145 | 74 | 0.640 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 233,697 | 2.337 | 18 | 18 | fits | 114,285 | 139 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 1,089,207 | 10.892 | 18 | 18 | fits | 22,377 | 15 | 0.779 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 301,304 | 3.013 | 20 | 20 | fits | 96,873 | 81 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 74,850 | 0.749 | 20 | 200 | fits | 81,247 | 133 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 389,216 | 3.892 | 20 | 200 | fits | 96,873 | 81 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 75,762 | 0.758 | 20 | 20 | fits | 81,247 | 133 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 543,717 | 5.437 | 20 | 20 | fits | 76,653 | 44 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 79,347 | 0.793 | 20 | 24 | fits | 81,247 | 133 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 1,028,556 | 10.286 | 20 | 24 | fits | 47,562 | 30 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 78,307 | 0.783 | 20 | 50 | fits | 81,247 | 133 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 392,892 | 3.929 | 20 | 50 | fits | 96,873 | 81 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 200,645 | 2.006 | 18 | 18 | fits | 115,108 | 143 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 1,079,570 | 10.796 | 18 | 18 | fits | 22,522 | 15 | 0.783 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 326,265 | 3.263 | 20 | 20 | fits | 89,374 | 58 | 0.675 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 115,493 | 1.155 | 20 | 200 | fits | 81,059 | 134 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 406,678 | 4.067 | 20 | 200 | fits | 89,374 | 58 | 0.675 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 116,405 | 1.164 | 20 | 20 | fits | 81,059 | 134 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 560,786 | 5.608 | 20 | 20 | fits | 76,502 | 44 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 38,931 | 0.389 | 20 | 24 | fits | 41,823 | 69 | 0.542 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 997,949 | 9.979 | 20 | 24 | fits | 47,502 | 30 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 37,891 | 0.379 | 20 | 50 | fits | 41,823 | 69 | 0.542 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 320,980 | 3.210 | 20 | 50 | fits | 88,901 | 74 | 0.639 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 232,014 | 2.320 | 18 | 18 | fits | 113,519 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 1,078,695 | 10.787 | 18 | 18 | fits | 22,377 | 15 | 0.779 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 299,453 | 2.995 | 20 | 20 | fits | 97,057 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 82,134 | 0.821 | 20 | 200 | fits | 80,697 | 132 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 387,479 | 3.875 | 20 | 200 | fits | 97,057 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 83,046 | 0.830 | 20 | 20 | fits | 80,697 | 132 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 541,892 | 5.419 | 20 | 20 | fits | 76,511 | 44 | 0.678 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 86,631 | 0.866 | 20 | 24 | fits | 80,697 | 132 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 1,028,444 | 10.284 | 20 | 24 | fits | 47,398 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 85,591 | 0.856 | 20 | 50 | fits | 80,697 | 132 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 391,155 | 3.912 | 20 | 50 | fits | 97,057 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 198,743 | 1.987 | 18 | 18 | fits | 113,607 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 1,086,756 | 10.868 | 18 | 18 | fits | 29,844 | 17 | 0.724 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 298,700 | 2.987 | 20 | 20 | fits | 96,977 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 81,401 | 0.814 | 20 | 200 | fits | 80,697 | 132 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 386,724 | 3.867 | 20 | 200 | fits | 96,977 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 82,313 | 0.823 | 20 | 20 | fits | 80,697 | 132 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 593,877 | 5.939 | 20 | 20 | fits | 65,578 | 38 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 85,898 | 0.859 | 20 | 24 | fits | 80,697 | 132 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 1,034,901 | 10.349 | 20 | 24 | fits | 47,545 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 84,858 | 0.849 | 20 | 50 | fits | 80,697 | 132 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 390,400 | 3.904 | 20 | 50 | fits | 96,977 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 198,074 | 1.981 | 18 | 18 | fits | 113,671 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 1,093,001 | 10.930 | 18 | 18 | fits | 29,823 | 17 | 0.724 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 297,824 | 2.978 | 20 | 20 | fits | 74,818 | 73 | 0.612 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 80,599 | 0.806 | 20 | 200 | fits | 80,681 | 132 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 363,689 | 3.637 | 20 | 200 | fits | 74,818 | 73 | 0.612 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 81,511 | 0.815 | 20 | 20 | fits | 80,681 | 132 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 577,366 | 5.774 | 20 | 20 | fits | 65,250 | 38 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 85,096 | 0.851 | 20 | 24 | fits | 80,681 | 132 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 1,017,886 | 10.179 | 20 | 24 | fits | 47,545 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 84,056 | 0.841 | 20 | 50 | fits | 80,681 | 132 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 367,365 | 3.674 | 20 | 50 | fits | 74,818 | 73 | 0.612 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 197,200 | 1.972 | 18 | 18 | fits | 113,599 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 1,098,234 | 10.982 | 18 | 18 | fits | 22,248 | 14 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 377,935 | 3.779 | 20 | 20 | fits | 88,157 | 56 | 0.689 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 79,754 | 0.798 | 20 | 200 | fits | 80,689 | 132 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 458,311 | 4.583 | 20 | 200 | fits | 88,157 | 56 | 0.689 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 80,666 | 0.807 | 20 | 20 | fits | 80,689 | 132 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 601,169 | 6.012 | 20 | 20 | fits | 65,217 | 38 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 84,251 | 0.843 | 20 | 24 | fits | 80,689 | 132 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 1,042,022 | 10.420 | 20 | 24 | fits | 47,545 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 83,211 | 0.832 | 20 | 50 | fits | 80,689 | 132 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 373,830 | 3.738 | 20 | 50 | fits | 94,482 | 97 | 0.591 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 196,355 | 1.964 | 18 | 18 | fits | 113,599 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 1,092,767 | 10.928 | 18 | 18 | fits | 22,468 | 14 | 0.791 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 363,650 | 3.636 | 20 | 20 | fits | 88,264 | 56 | 0.690 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 79,006 | 0.790 | 20 | 200 | fits | 80,778 | 133 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 444,054 | 4.441 | 20 | 200 | fits | 88,264 | 56 | 0.690 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 79,918 | 0.799 | 20 | 20 | fits | 80,778 | 133 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 596,324 | 5.963 | 20 | 20 | fits | 65,932 | 37 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 83,503 | 0.835 | 20 | 24 | fits | 80,778 | 133 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 1,028,567 | 10.286 | 20 | 24 | fits | 47,546 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 82,463 | 0.825 | 20 | 50 | fits | 80,778 | 133 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 359,466 | 3.595 | 20 | 50 | fits | 95,758 | 97 | 0.604 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 263,643 | 2.636 | 18 | 18 | fits | 108,827 | 103 | 0.648 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 1,222,861 | 12.229 | 18 | 18 | fits | 22,393 | 14 | 0.791 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 301,157 | 3.012 | 20 | 20 | fits | 97,133 | 82 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 82,548 | 0.825 | 20 | 200 | fits | 81,066 | 133 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 389,053 | 3.891 | 20 | 200 | fits | 97,133 | 82 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 83,460 | 0.835 | 20 | 20 | fits | 81,066 | 133 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 553,709 | 5.537 | 20 | 20 | fits | 76,906 | 44 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 87,045 | 0.870 | 20 | 24 | fits | 81,066 | 133 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 1,112,571 | 11.126 | 20 | 24 | fits | 48,196 | 29 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 86,005 | 0.860 | 20 | 50 | fits | 81,066 | 133 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 392,729 | 3.927 | 20 | 50 | fits | 97,133 | 82 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 199,974 | 2.000 | 18 | 18 | fits | 114,424 | 139 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 1,165,980 | 11.660 | 18 | 18 | fits | 24,885 | 21 | 0.782 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 336,692 | 3.367 | 20 | 20 | fits | 89,235 | 58 | 0.674 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 116,176 | 1.162 | 20 | 200 | fits | 81,516 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 416,929 | 4.169 | 20 | 200 | fits | 89,235 | 58 | 0.674 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 117,088 | 1.171 | 20 | 20 | fits | 81,516 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 570,936 | 5.709 | 20 | 20 | fits | 76,578 | 44 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 39,157 | 0.392 | 20 | 24 | fits | 41,939 | 70 | 0.545 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 1,078,304 | 10.783 | 20 | 24 | fits | 50,393 | 36 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 38,117 | 0.381 | 20 | 50 | fits | 41,939 | 70 | 0.545 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 331,370 | 3.314 | 20 | 50 | fits | 89,323 | 74 | 0.641 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 233,175 | 2.332 | 18 | 18 | fits | 113,997 | 139 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 1,166,707 | 11.667 | 18 | 18 | fits | 29,863 | 18 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 302,726 | 3.027 | 20 | 20 | fits | 96,943 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 74,614 | 0.746 | 20 | 200 | fits | 81,066 | 133 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 390,671 | 3.907 | 20 | 200 | fits | 96,943 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 75,526 | 0.755 | 20 | 20 | fits | 81,066 | 133 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 545,111 | 5.451 | 20 | 20 | fits | 76,634 | 44 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 79,111 | 0.791 | 20 | 24 | fits | 81,066 | 133 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 1,100,358 | 11.004 | 20 | 24 | fits | 47,588 | 30 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 78,071 | 0.781 | 20 | 50 | fits | 81,066 | 133 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 394,347 | 3.943 | 20 | 50 | fits | 96,943 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 192,980 | 1.930 | 18 | 18 | fits | 115,364 | 144 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,158,671 | 11.587 | 18 | 18 | fits | 29,769 | 18 | 0.714 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 291,999 | 2.920 | 20 | 20 | fits | 96,865 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 73,813 | 0.738 | 20 | 200 | fits | 80,605 | 132 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 379,903 | 3.799 | 20 | 200 | fits | 96,865 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 74,725 | 0.747 | 20 | 20 | fits | 80,605 | 132 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 534,333 | 5.343 | 20 | 20 | fits | 76,564 | 44 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 78,310 | 0.783 | 20 | 24 | fits | 80,605 | 132 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 1,068,303 | 10.683 | 20 | 24 | fits | 47,648 | 30 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 77,270 | 0.773 | 20 | 50 | fits | 80,605 | 132 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 383,579 | 3.836 | 20 | 50 | fits | 96,865 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 191,446 | 1.914 | 18 | 18 | fits | 114,631 | 143 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,156,312 | 11.563 | 18 | 18 | fits | 29,675 | 18 | 0.710 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 325,981 | 3.260 | 20 | 20 | fits | 89,301 | 58 | 0.675 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 115,382 | 1.154 | 20 | 200 | fits | 81,117 | 134 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 406,321 | 4.063 | 20 | 200 | fits | 89,301 | 58 | 0.675 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 116,294 | 1.163 | 20 | 20 | fits | 81,117 | 134 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 648,638 | 6.486 | 20 | 20 | fits | 43,038 | 29 | 0.698 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 38,762 | 0.388 | 20 | 24 | fits | 41,713 | 69 | 0.540 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 1,036,706 | 10.367 | 20 | 24 | fits | 47,554 | 30 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 37,722 | 0.377 | 20 | 50 | fits | 41,713 | 69 | 0.540 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 320,696 | 3.207 | 20 | 50 | fits | 88,972 | 74 | 0.639 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 231,659 | 2.317 | 18 | 18 | fits | 113,275 | 138 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,186,692 | 11.867 | 18 | 18 | fits | 22,212 | 14 | 0.784 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 299,092 | 2.991 | 20 | 20 | fits | 74,812 | 72 | 0.613 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 81,983 | 0.820 | 20 | 200 | fits | 80,605 | 132 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 364,943 | 3.649 | 20 | 200 | fits | 74,812 | 72 | 0.613 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 82,895 | 0.829 | 20 | 20 | fits | 80,605 | 132 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 663,180 | 6.632 | 20 | 20 | fits | 65,357 | 37 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 86,480 | 0.865 | 20 | 24 | fits | 80,605 | 132 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 1,094,393 | 10.944 | 20 | 24 | fits | 47,463 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 85,440 | 0.854 | 20 | 50 | fits | 80,605 | 132 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 368,619 | 3.686 | 20 | 50 | fits | 74,812 | 72 | 0.613 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 198,539 | 1.985 | 18 | 18 | fits | 113,554 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,174,776 | 11.748 | 18 | 18 | fits | 22,256 | 14 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 432,017 | 4.320 | 20 | 20 | fits | 89,870 | 62 | 0.688 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 81,250 | 0.812 | 20 | 200 | fits | 80,605 | 132 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 512,268 | 5.123 | 20 | 200 | fits | 89,870 | 62 | 0.688 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 82,162 | 0.822 | 20 | 20 | fits | 80,605 | 132 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 655,280 | 6.553 | 20 | 20 | fits | 65,218 | 38 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 85,747 | 0.857 | 20 | 24 | fits | 80,605 | 132 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 1,095,237 | 10.952 | 20 | 24 | fits | 47,472 | 29 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 84,707 | 0.847 | 20 | 50 | fits | 80,605 | 132 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 426,074 | 4.261 | 20 | 50 | fits | 72,202 | 88 | 0.536 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 197,806 | 1.978 | 18 | 18 | fits | 113,554 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,175,597 | 11.756 | 18 | 18 | fits | 22,256 | 14 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 429,838 | 4.298 | 20 | 20 | fits | 87,747 | 56 | 0.685 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 80,517 | 0.805 | 20 | 200 | fits | 80,605 | 132 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 509,717 | 5.097 | 20 | 200 | fits | 87,747 | 56 | 0.685 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 81,429 | 0.814 | 20 | 20 | fits | 80,605 | 132 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 652,455 | 6.525 | 20 | 20 | fits | 65,144 | 38 | 0.720 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 85,014 | 0.850 | 20 | 24 | fits | 80,605 | 132 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 1,085,090 | 10.851 | 20 | 24 | fits | 39,925 | 25 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 83,974 | 0.840 | 20 | 50 | fits | 80,605 | 132 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 425,646 | 4.256 | 20 | 50 | fits | 96,870 | 103 | 0.600 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 171,837 | 1.718 | 18 | 18 | fits | 88,318 | 103 | 0.691 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,192,284 | 11.923 | 18 | 18 | fits | 22,205 | 14 | 0.784 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 308,013 | 3.080 | 20 | 20 | fits | 96,943 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 80,945 | 0.809 | 20 | 200 | fits | 81,063 | 133 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 395,958 | 3.960 | 20 | 200 | fits | 96,943 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 81,857 | 0.819 | 20 | 20 | fits | 81,063 | 133 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 550,398 | 5.504 | 20 | 20 | fits | 76,634 | 44 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 85,442 | 0.854 | 20 | 24 | fits | 81,063 | 133 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 1,003,593 | 10.036 | 20 | 24 | fits | 44,588 | 37 | 0.724 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 84,402 | 0.844 | 20 | 50 | fits | 81,063 | 133 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 399,634 | 3.996 | 20 | 50 | fits | 96,943 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 198,267 | 1.983 | 18 | 18 | fits | 114,320 | 139 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 1,084,813 | 10.848 | 18 | 18 | fits | 22,384 | 15 | 0.779 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 307,502 | 3.075 | 20 | 20 | fits | 96,750 | 81 | 0.648 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 81,772 | 0.818 | 20 | 200 | fits | 81,063 | 133 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 395,291 | 3.953 | 20 | 200 | fits | 96,750 | 81 | 0.648 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 82,684 | 0.827 | 20 | 20 | fits | 81,063 | 133 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 549,731 | 5.497 | 20 | 20 | fits | 76,634 | 44 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 86,269 | 0.863 | 20 | 24 | fits | 81,063 | 133 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 1,018,341 | 10.183 | 20 | 24 | fits | 47,354 | 30 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 85,229 | 0.852 | 20 | 50 | fits | 81,063 | 133 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 398,967 | 3.990 | 20 | 50 | fits | 96,750 | 81 | 0.648 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 206,930 | 2.069 | 18 | 18 | fits | 114,313 | 138 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 1,076,654 | 10.767 | 18 | 18 | fits | 29,769 | 18 | 0.714 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 297,527 | 2.975 | 20 | 20 | fits | 96,865 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 80,268 | 0.803 | 20 | 200 | fits | 80,770 | 132 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 385,431 | 3.854 | 20 | 200 | fits | 96,865 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 81,180 | 0.812 | 20 | 20 | fits | 80,770 | 132 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 539,861 | 5.399 | 20 | 20 | fits | 76,564 | 44 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 84,765 | 0.848 | 20 | 24 | fits | 80,770 | 132 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 1,017,757 | 10.178 | 20 | 24 | fits | 47,361 | 30 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 83,725 | 0.837 | 20 | 50 | fits | 80,770 | 132 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 389,107 | 3.891 | 20 | 50 | fits | 96,865 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 196,974 | 1.970 | 18 | 18 | fits | 113,704 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 1,068,729 | 10.687 | 18 | 18 | fits | 22,421 | 15 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 296,794 | 2.968 | 20 | 20 | fits | 96,865 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 79,535 | 0.795 | 20 | 200 | fits | 80,770 | 132 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 384,698 | 3.847 | 20 | 200 | fits | 96,865 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 80,447 | 0.804 | 20 | 20 | fits | 80,770 | 132 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 539,128 | 5.391 | 20 | 20 | fits | 76,564 | 44 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 84,032 | 0.840 | 20 | 24 | fits | 80,770 | 132 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 1,016,900 | 10.169 | 20 | 24 | fits | 47,434 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 82,992 | 0.830 | 20 | 50 | fits | 80,770 | 132 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 388,374 | 3.884 | 20 | 50 | fits | 96,865 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 196,241 | 1.962 | 18 | 18 | fits | 113,704 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 1,075,108 | 10.751 | 18 | 18 | fits | 29,831 | 17 | 0.724 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 296,061 | 2.961 | 20 | 20 | fits | 96,865 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 78,802 | 0.788 | 20 | 200 | fits | 80,770 | 132 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 383,965 | 3.840 | 20 | 200 | fits | 96,865 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 79,714 | 0.797 | 20 | 20 | fits | 80,770 | 132 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 583,085 | 5.831 | 20 | 20 | fits | 65,317 | 38 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 83,299 | 0.833 | 20 | 24 | fits | 80,770 | 132 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 1,023,426 | 10.234 | 20 | 24 | fits | 47,544 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 82,259 | 0.823 | 20 | 50 | fits | 80,770 | 132 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 387,641 | 3.876 | 20 | 50 | fits | 96,865 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 195,508 | 1.955 | 18 | 18 | fits | 113,704 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 1,081,542 | 10.815 | 18 | 18 | fits | 29,831 | 17 | 0.724 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 295,328 | 2.953 | 20 | 20 | fits | 74,894 | 73 | 0.613 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 78,069 | 0.781 | 20 | 200 | fits | 80,770 | 132 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 361,261 | 3.613 | 20 | 200 | fits | 74,894 | 73 | 0.613 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 78,981 | 0.790 | 20 | 20 | fits | 80,770 | 132 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 566,552 | 5.666 | 20 | 20 | fits | 65,264 | 38 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 82,566 | 0.826 | 20 | 24 | fits | 80,770 | 132 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 1,006,462 | 10.065 | 20 | 24 | fits | 47,472 | 29 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 81,526 | 0.815 | 20 | 50 | fits | 80,770 | 132 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 364,937 | 3.649 | 20 | 50 | fits | 74,894 | 73 | 0.613 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 194,775 | 1.948 | 18 | 18 | fits | 113,704 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 1,086,822 | 10.868 | 18 | 18 | fits | 22,256 | 14 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 368,254 | 3.683 | 20 | 20 | fits | 88,197 | 56 | 0.689 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 77,336 | 0.773 | 20 | 200 | fits | 80,770 | 132 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 448,662 | 4.487 | 20 | 200 | fits | 88,197 | 56 | 0.689 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 78,248 | 0.782 | 20 | 20 | fits | 80,770 | 132 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 591,536 | 5.915 | 20 | 20 | fits | 65,225 | 38 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 81,833 | 0.818 | 20 | 24 | fits | 80,770 | 132 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 1,032,320 | 10.323 | 20 | 24 | fits | 47,553 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 80,793 | 0.808 | 20 | 50 | fits | 80,770 | 132 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 364,141 | 3.641 | 20 | 50 | fits | 94,577 | 97 | 0.593 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 194,042 | 1.940 | 18 | 18 | fits | 113,704 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 1,083,081 | 10.831 | 18 | 18 | fits | 22,476 | 14 | 0.791 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 350,947 | 3.509 | 20 | 20 | fits | 88,230 | 56 | 0.690 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 76,692 | 0.767 | 20 | 200 | fits | 80,859 | 133 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 431,309 | 4.313 | 20 | 200 | fits | 88,230 | 56 | 0.690 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 77,604 | 0.776 | 20 | 20 | fits | 80,859 | 133 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 583,570 | 5.836 | 20 | 20 | fits | 65,940 | 37 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 81,189 | 0.812 | 20 | 24 | fits | 80,859 | 133 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 1,015,885 | 10.159 | 20 | 24 | fits | 47,554 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 80,149 | 0.801 | 20 | 50 | fits | 80,859 | 133 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 346,755 | 3.468 | 20 | 50 | fits | 95,704 | 97 | 0.605 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 250,986 | 2.510 | 18 | 18 | fits | 108,438 | 103 | 0.647 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 1,074,001 | 10.740 | 18 | 18 | fits | 29,831 | 17 | 0.724 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 309,514 | 3.095 | 20 | 20 | fits | 97,331 | 81 | 0.653 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 82,607 | 0.826 | 20 | 200 | fits | 81,059 | 133 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 398,055 | 3.981 | 20 | 200 | fits | 97,331 | 81 | 0.653 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 83,519 | 0.835 | 20 | 20 | fits | 81,059 | 133 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 552,848 | 5.528 | 20 | 20 | fits | 76,634 | 44 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 87,104 | 0.871 | 20 | 24 | fits | 81,059 | 133 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 1,116,688 | 11.167 | 20 | 24 | fits | 51,551 | 35 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 86,064 | 0.861 | 20 | 50 | fits | 81,059 | 133 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 401,731 | 4.017 | 20 | 50 | fits | 97,331 | 81 | 0.653 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 199,967 | 2.000 | 18 | 18 | fits | 114,358 | 139 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 1,167,667 | 11.677 | 18 | 18 | fits | 22,476 | 14 | 0.791 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 335,442 | 3.354 | 20 | 20 | fits | 89,280 | 58 | 0.674 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 116,227 | 1.162 | 20 | 200 | fits | 81,501 | 135 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 415,761 | 4.158 | 20 | 200 | fits | 89,280 | 58 | 0.674 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 117,139 | 1.171 | 20 | 20 | fits | 81,501 | 135 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 569,758 | 5.698 | 20 | 20 | fits | 76,508 | 44 | 0.678 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 39,223 | 0.392 | 20 | 24 | fits | 41,939 | 70 | 0.545 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 1,087,005 | 10.870 | 20 | 24 | fits | 47,521 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 38,183 | 0.382 | 20 | 50 | fits | 41,939 | 70 | 0.545 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 330,157 | 3.302 | 20 | 50 | fits | 88,861 | 74 | 0.638 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 241,231 | 2.412 | 18 | 18 | fits | 114,170 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 1,167,377 | 11.674 | 18 | 18 | fits | 22,256 | 14 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 300,192 | 3.002 | 20 | 20 | fits | 96,865 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 82,952 | 0.830 | 20 | 200 | fits | 80,932 | 132 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 388,096 | 3.881 | 20 | 200 | fits | 96,865 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 83,864 | 0.839 | 20 | 20 | fits | 80,932 | 132 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 542,526 | 5.425 | 20 | 20 | fits | 76,564 | 44 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 87,449 | 0.874 | 20 | 24 | fits | 80,932 | 132 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 1,107,831 | 11.078 | 20 | 24 | fits | 47,530 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 86,409 | 0.864 | 20 | 50 | fits | 80,932 | 132 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 391,772 | 3.918 | 20 | 50 | fits | 96,865 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 199,588 | 1.996 | 18 | 18 | fits | 113,634 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,158,592 | 11.586 | 18 | 18 | fits | 22,476 | 14 | 0.791 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 299,696 | 2.997 | 20 | 20 | fits | 96,865 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 82,456 | 0.825 | 20 | 200 | fits | 80,878 | 132 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 387,600 | 3.876 | 20 | 200 | fits | 96,865 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 83,368 | 0.834 | 20 | 20 | fits | 80,878 | 132 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 542,030 | 5.420 | 20 | 20 | fits | 76,564 | 44 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 86,953 | 0.870 | 20 | 24 | fits | 80,878 | 132 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 1,100,313 | 11.003 | 20 | 24 | fits | 47,530 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 85,913 | 0.859 | 20 | 50 | fits | 80,878 | 132 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 391,276 | 3.913 | 20 | 50 | fits | 96,865 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 199,092 | 1.991 | 18 | 18 | fits | 113,634 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,158,429 | 11.584 | 18 | 18 | fits | 29,831 | 17 | 0.724 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 299,054 | 2.991 | 20 | 20 | fits | 96,865 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 81,814 | 0.818 | 20 | 200 | fits | 80,878 | 132 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 386,958 | 3.870 | 20 | 200 | fits | 96,865 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 82,726 | 0.827 | 20 | 20 | fits | 80,878 | 132 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 674,132 | 6.741 | 20 | 20 | fits | 69,523 | 43 | 0.742 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 86,311 | 0.863 | 20 | 24 | fits | 80,878 | 132 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 1,107,230 | 11.072 | 20 | 24 | fits | 47,614 | 29 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 85,271 | 0.853 | 20 | 50 | fits | 80,878 | 132 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 390,634 | 3.906 | 20 | 50 | fits | 96,865 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 198,450 | 1.984 | 18 | 18 | fits | 113,634 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,165,346 | 11.653 | 18 | 18 | fits | 29,831 | 17 | 0.724 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 298,321 | 2.983 | 20 | 20 | fits | 74,812 | 72 | 0.613 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 81,081 | 0.811 | 20 | 200 | fits | 80,878 | 132 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 364,172 | 3.642 | 20 | 200 | fits | 74,812 | 72 | 0.613 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 81,993 | 0.820 | 20 | 20 | fits | 80,878 | 132 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 657,717 | 6.577 | 20 | 20 | fits | 65,419 | 37 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 85,578 | 0.856 | 20 | 24 | fits | 80,878 | 132 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 1,088,990 | 10.890 | 20 | 24 | fits | 47,463 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 84,538 | 0.845 | 20 | 50 | fits | 80,878 | 132 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 367,848 | 3.678 | 20 | 50 | fits | 74,812 | 72 | 0.613 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 197,717 | 1.977 | 18 | 18 | fits | 113,634 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,169,373 | 11.694 | 18 | 18 | fits | 22,256 | 14 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 456,673 | 4.567 | 20 | 20 | fits | 87,924 | 55 | 0.691 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 80,348 | 0.803 | 20 | 200 | fits | 80,878 | 132 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 536,889 | 5.369 | 20 | 200 | fits | 87,924 | 55 | 0.691 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 81,260 | 0.813 | 20 | 20 | fits | 80,878 | 132 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 679,393 | 6.794 | 20 | 20 | fits | 65,025 | 37 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 84,845 | 0.848 | 20 | 24 | fits | 80,878 | 132 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 1,101,944 | 11.019 | 20 | 24 | fits | 39,870 | 26 | 0.732 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 83,805 | 0.838 | 20 | 50 | fits | 80,878 | 132 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 452,641 | 4.526 | 20 | 50 | fits | 98,188 | 102 | 0.614 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 196,984 | 1.970 | 18 | 18 | fits | 113,634 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,162,999 | 11.630 | 18 | 18 | fits | 29,833 | 18 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 454,042 | 4.540 | 20 | 20 | fits | 87,919 | 55 | 0.691 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 79,615 | 0.796 | 20 | 200 | fits | 80,878 | 132 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 534,369 | 5.344 | 20 | 200 | fits | 87,919 | 55 | 0.691 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 80,527 | 0.805 | 20 | 20 | fits | 80,878 | 132 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 676,799 | 6.768 | 20 | 20 | fits | 65,025 | 37 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 84,112 | 0.841 | 20 | 24 | fits | 80,878 | 132 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 1,108,931 | 11.089 | 20 | 24 | fits | 44,272 | 31 | 0.749 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 83,072 | 0.831 | 20 | 50 | fits | 80,878 | 132 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 450,126 | 4.501 | 20 | 50 | fits | 94,643 | 96 | 0.597 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 170,853 | 1.709 | 18 | 18 | fits | 88,236 | 103 | 0.690 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,167,481 | 11.675 | 18 | 18 | fits | 29,776 | 18 | 0.714 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 305,776 | 3.058 | 20 | 20 | fits | 96,750 | 81 | 0.648 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 80,265 | 0.803 | 20 | 200 | fits | 81,494 | 133 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 393,565 | 3.936 | 20 | 200 | fits | 96,750 | 81 | 0.648 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 81,177 | 0.812 | 20 | 20 | fits | 81,494 | 133 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 548,005 | 5.480 | 20 | 20 | fits | 76,634 | 44 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 84,762 | 0.848 | 20 | 24 | fits | 81,494 | 133 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 1,027,614 | 10.276 | 20 | 24 | fits | 47,575 | 30 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 83,722 | 0.837 | 20 | 50 | fits | 81,494 | 133 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 397,241 | 3.972 | 20 | 50 | fits | 96,750 | 81 | 0.648 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 205,265 | 2.053 | 18 | 18 | fits | 114,165 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 1,078,586 | 10.786 | 18 | 18 | fits | 22,421 | 15 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 296,240 | 2.962 | 20 | 20 | fits | 96,865 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 78,996 | 0.790 | 20 | 200 | fits | 80,653 | 132 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 384,144 | 3.841 | 20 | 200 | fits | 96,865 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 79,908 | 0.799 | 20 | 20 | fits | 80,653 | 132 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 538,574 | 5.386 | 20 | 20 | fits | 76,564 | 44 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 83,493 | 0.835 | 20 | 24 | fits | 80,653 | 132 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 1,016,823 | 10.168 | 20 | 24 | fits | 47,354 | 30 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 82,453 | 0.825 | 20 | 50 | fits | 80,653 | 132 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 387,820 | 3.878 | 20 | 50 | fits | 96,865 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 195,636 | 1.956 | 18 | 18 | fits | 113,638 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 1,067,781 | 10.678 | 18 | 18 | fits | 22,414 | 15 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 295,507 | 2.955 | 20 | 20 | fits | 96,865 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 78,263 | 0.783 | 20 | 200 | fits | 80,653 | 132 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 383,411 | 3.834 | 20 | 200 | fits | 96,865 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 79,175 | 0.792 | 20 | 20 | fits | 80,653 | 132 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 537,841 | 5.378 | 20 | 20 | fits | 76,564 | 44 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 82,760 | 0.828 | 20 | 24 | fits | 80,653 | 132 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 1,017,559 | 10.176 | 20 | 24 | fits | 47,361 | 30 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 81,720 | 0.817 | 20 | 50 | fits | 80,653 | 132 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 387,087 | 3.871 | 20 | 50 | fits | 96,865 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 194,903 | 1.949 | 18 | 18 | fits | 113,638 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 1,078,743 | 10.787 | 18 | 18 | fits | 22,631 | 14 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 294,774 | 2.948 | 20 | 20 | fits | 96,865 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 77,530 | 0.775 | 20 | 200 | fits | 80,653 | 132 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 382,678 | 3.827 | 20 | 200 | fits | 96,865 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 78,442 | 0.784 | 20 | 20 | fits | 80,653 | 132 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 541,781 | 5.418 | 20 | 20 | fits | 81,237 | 51 | 0.692 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 82,027 | 0.820 | 20 | 24 | fits | 80,653 | 132 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 1,018,312 | 10.183 | 20 | 24 | fits | 47,461 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 80,987 | 0.810 | 20 | 50 | fits | 80,653 | 132 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 386,354 | 3.864 | 20 | 50 | fits | 96,865 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 194,170 | 1.942 | 18 | 18 | fits | 113,638 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 1,076,428 | 10.764 | 18 | 18 | fits | 29,831 | 17 | 0.724 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 294,041 | 2.940 | 20 | 20 | fits | 74,901 | 73 | 0.613 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 76,797 | 0.768 | 20 | 200 | fits | 80,653 | 132 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 359,981 | 3.600 | 20 | 200 | fits | 74,901 | 73 | 0.613 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 77,709 | 0.777 | 20 | 20 | fits | 80,653 | 132 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 566,944 | 5.669 | 20 | 20 | fits | 65,248 | 38 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 81,294 | 0.813 | 20 | 24 | fits | 80,653 | 132 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 1,007,513 | 10.075 | 20 | 24 | fits | 47,553 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 80,254 | 0.803 | 20 | 50 | fits | 80,653 | 132 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 363,657 | 3.637 | 20 | 50 | fits | 74,901 | 73 | 0.613 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 193,437 | 1.934 | 18 | 18 | fits | 113,638 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 1,087,885 | 10.879 | 18 | 18 | fits | 22,256 | 14 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 273,115 | 2.731 | 20 | 20 | fits | 75,866 | 79 | 0.603 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 76,064 | 0.761 | 20 | 200 | fits | 80,653 | 132 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 338,043 | 3.380 | 20 | 200 | fits | 75,866 | 79 | 0.603 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 76,976 | 0.770 | 20 | 20 | fits | 80,653 | 132 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 542,310 | 5.423 | 20 | 20 | fits | 65,253 | 38 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 80,561 | 0.806 | 20 | 24 | fits | 80,653 | 132 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 982,257 | 9.823 | 20 | 24 | fits | 47,472 | 29 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 79,521 | 0.795 | 20 | 50 | fits | 80,653 | 132 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 341,719 | 3.417 | 20 | 50 | fits | 75,866 | 79 | 0.603 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 192,704 | 1.927 | 18 | 18 | fits | 113,638 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 1,092,177 | 10.922 | 18 | 18 | fits | 22,205 | 14 | 0.784 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 316,335 | 3.163 | 20 | 20 | fits | 89,877 | 56 | 0.703 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 74,453 | 0.745 | 20 | 200 | fits | 80,653 | 132 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 398,061 | 3.981 | 20 | 200 | fits | 89,877 | 56 | 0.703 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 75,365 | 0.754 | 20 | 20 | fits | 80,653 | 132 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 541,066 | 5.411 | 20 | 20 | fits | 65,225 | 38 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 78,950 | 0.789 | 20 | 24 | fits | 80,653 | 132 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 981,832 | 9.818 | 20 | 24 | fits | 47,553 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 77,910 | 0.779 | 20 | 50 | fits | 80,653 | 132 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 311,860 | 3.119 | 20 | 50 | fits | 81,395 | 63 | 0.734 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 311,795 | 3.118 | 18 | 18 | fits | 81,395 | 63 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 1,091,764 | 10.918 | 18 | 18 | fits | 22,205 | 14 | 0.784 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 372,863 | 3.729 | 20 | 20 | fits | 88,338 | 55 | 0.692 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 77,515 | 0.775 | 20 | 200 | fits | 80,987 | 133 | 0.502 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 453,931 | 4.539 | 20 | 200 | fits | 88,338 | 55 | 0.692 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 78,427 | 0.784 | 20 | 20 | fits | 80,987 | 133 | 0.502 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 596,563 | 5.966 | 20 | 20 | fits | 64,955 | 37 | 0.723 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 82,012 | 0.820 | 20 | 24 | fits | 80,987 | 133 | 0.502 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 1,026,572 | 10.266 | 20 | 24 | fits | 47,328 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 80,972 | 0.810 | 20 | 50 | fits | 80,987 | 133 | 0.502 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 360,355 | 3.604 | 20 | 50 | fits | 94,735 | 97 | 0.593 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 169,199 | 1.692 | 18 | 18 | fits | 88,682 | 104 | 0.690 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 1,077,223 | 10.772 | 18 | 18 | fits | 22,215 | 13 | 0.795 |
| LINK_UP | `adp.link_up.if0` | 2,550 | 0.025 | 20 | 200 | fits | 20,500 | 45 (11) | 0.676 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,057 | 0.151 | 20 | 200 | fits | 17,332 | 25 (39) | 0.608 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 9,022 | 0.090 | 20 | 200 | fits | 2,573 | 9 (11) | 0.560 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 277,767 | 2.778 | 20 | 200 | fits | 72,614 | 84 | 0.533 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 432,572 | 4.326 | 20 | 20 | fits | 55,743 | 32 | 0.665 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 551,772 | 5.518 | 20 | 24 | fits | 22,735 | 21 | 0.560 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 296,556 | 2.966 | 20 | 50 | fits | 63,076 | 55 | 0.617 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 848,597 | 8.486 | 18 | 18 | fits | 39,306 | 26 | 0.728 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 285,578 | 2.856 | 20 | 200 | fits | 75,471 | 90 | 0.558 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 447,816 | 4.478 | 20 | 20 | fits | 57,582 | 38 | 0.667 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 612,707 | 6.127 | 20 | 24 | fits | 25,521 | 27 | 0.608 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 292,110 | 2.921 | 20 | 50 | fits | 66,144 | 61 | 0.643 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 864,787 | 8.648 | 18 | 18 | fits | 49,613 | 35 | 0.715 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 12,629 | 0.126 | 20 | 20 | fits | 26,553 | 23 (35) | 0.774 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 5,947 | 0.059 | 20 | 20 | fits | 20,079 | 18 (14) | 0.828 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 11,845 | 0.118 | 20 | 20 | fits | 20,004 | 19 (14) | 0.817 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 11,247 | 0.112 | 20 | 20 | fits | 26,899 | 23 (35) | 0.783 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 926,541 | 9.265 | 18 | 18 | fits | 39,742 | 14 | 0.851 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 35,160 | 0.352 | 18 | 18 | fits | 35,225 | 14 | 0.889 |
| malformed MRPDU discard | `srp.malformed.if0` | 13,393 | 0.134 | 18 | 18 | fits | 13,458 | 14 | 0.586 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 78,787 | 0.788 | 218 | 218 | fits | 58,086 | 17 | 0.859 |
| an event behind 15 others | `backlog.event.if0` | 96,922 | 0.969 | 20 | 200 | fits | 71,656 | 104 | 0.520 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 378,221 | 3.782 | 20 | 20 | fits | 52,238 | 44 | 0.534 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 86,206 | 0.862 | 20 | 200 | fits | 86,414 | 138 | 0.522 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 306,609 | 3.066 | 20 | 200 | fits | 62,348 | 55 | 0.570 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 81,947 | 0.819 | 20 | 20 | fits | 86,414 | 138 | 0.522 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 407,473 | 4.075 | 20 | 20 | fits | 52,238 | 44 | 0.534 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 85,532 | 0.855 | 20 | 24 | fits | 86,414 | 138 | 0.522 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 669,540 | 6.695 | 20 | 24 | fits | 25,777 | 29 | 0.491 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 84,492 | 0.845 | 20 | 50 | fits | 86,414 | 138 | 0.522 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 305,114 | 3.051 | 20 | 50 | fits | 62,348 | 55 | 0.570 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 305,049 | 3.050 | 18 | 18 | fits | 62,348 | 55 | 0.570 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 699,790 | 6.998 | 18 | 18 | fits | 10,496 | 17 | 0.159 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 294,195 | 2.942 | 20 | 20 | fits | 74,821 | 73 | 0.612 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 76,079 | 0.761 | 20 | 200 | fits | 80,761 | 135 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 360,055 | 3.601 | 20 | 200 | fits | 74,821 | 73 | 0.612 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 76,991 | 0.770 | 20 | 20 | fits | 80,761 | 135 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 516,464 | 5.165 | 20 | 20 | fits | 76,798 | 45 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 80,576 | 0.806 | 20 | 24 | fits | 80,761 | 135 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 1,000,843 | 10.008 | 20 | 24 | fits | 47,465 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 79,536 | 0.795 | 20 | 50 | fits | 80,761 | 135 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 363,731 | 3.637 | 20 | 50 | fits | 74,821 | 73 | 0.612 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 193,459 | 1.935 | 18 | 18 | fits | 114,378 | 138 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,081,200 | 10.812 | 18 | 18 | fits | 22,251 | 14 | 0.786 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,024 | 0.080 | 20 | 20 | fits | 22,211 | 20 | 0.772 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 76,079 | 0.761 | 20 | 200 | fits | 80,761 | 135 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 23,069 | 0.231 | 20 | 200 | fits | 22,211 | 20 | 0.772 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 76,991 | 0.770 | 20 | 20 | fits | 80,761 | 135 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 506,196 | 5.062 | 20 | 20 | fits | 76,695 | 45 | 0.676 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 80,576 | 0.806 | 20 | 24 | fits | 80,761 | 135 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 968,151 | 9.682 | 20 | 24 | fits | 47,490 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 79,536 | 0.795 | 20 | 50 | fits | 80,761 | 135 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 353,665 | 3.537 | 20 | 50 | fits | 64,755 | 63 | 0.600 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 193,459 | 1.935 | 18 | 18 | fits | 114,378 | 138 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,080,254 | 10.803 | 18 | 18 | fits | 22,207 | 14 | 0.784 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,216,323 | 62.163 | 20 | 20 | MISS ceiling | 29,429 | 25 | 0.572 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,025,081 | 360.251 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,025,006 | 360.250 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,024,931 | 360.249 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,024,856 | 360.249 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 78,977 | 0.790 | 20 | 200 | fits | 77,340 | 129 | 0.511 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 366,342 | 3.663 | 20 | 200 | fits | 84,945 | 67 | 0.654 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 74,718 | 0.747 | 20 | 20 | fits | 77,340 | 129 | 0.511 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 506,915 | 5.069 | 20 | 20 | fits | 39,970 | 24 | 0.764 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 78,303 | 0.783 | 20 | 24 | fits | 77,340 | 129 | 0.511 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,303,169 | 63.032 | 20 | 24 | MISS ceiling | 22,729 | 21 | 0.560 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 77,263 | 0.773 | 20 | 50 | fits | 77,340 | 129 | 0.511 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 364,847 | 3.648 | 20 | 50 | fits | 84,945 | 67 | 0.654 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 188,052 | 1.881 | 18 | 18 | fits | 111,244 | 131 | 0.637 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 846,282 | 8.463 | 18 | 18 | fits | 30,741 | 20 | 0.716 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,149 | 0.051 | 20 | 20 | fits | 19,474 | 14 (29) | 0.742 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 6,390 | 0.064 | 20 | 20 | fits | 21,235 | 20 (35) | 0.758 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 13,235 | 0.132 | 20 | 20 | fits | 26,759 | 23 (12) | 0.780 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 11,042 | 0.110 | 20 | 50 | fits | 20,500 | 45 | 0.676 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 9,285 | 0.093 | 20 | 50 | fits | 17,670 | 37 | 0.629 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 7,892 | 0.079 | 20 | 50 | fits | 17,400 | 37 | 0.621 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 12,335 | 0.123 | 20 | 50 | fits | 23,675 | 64 | 0.574 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 14,167 | 0.142 | 20 | 50 | fits | 23,675 | 64 | 0.574 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 9,226 | 0.092 | 20 | 50 | fits | 16,332 | 32 | 0.517 |
| LINK_UP | `adp.link_up.if0` | 2,550 | 0.025 | 20 | 200 | fits | 20,500 | 45 (11) | 0.676 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,057 | 0.151 | 20 | 200 | fits | 17,332 | 25 (39) | 0.608 |
| LINK_DOWN | `adp.link_down.if0` | 2,183 | 0.022 | 20 | 200 | fits | 20,475 | 22 (9) | 0.745 |
| LINK_UP | `adp.link_up.if0` | 2,550 | 0.025 | 20 | 200 | fits | 20,500 | 45 (11) | 0.676 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,057 | 0.151 | 20 | 200 | fits | 17,332 | 25 (39) | 0.608 |
| GM_CHANGE | `adp.gm_change.if0` | 2,358 | 0.024 | 20 | 200 | fits | 10,344 | 18 (11) | 0.592 |
| LINK_UP | `adp.link_up.if0` | 2,550 | 0.025 | 20 | 200 | fits | 20,500 | 45 (11) | 0.676 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,057 | 0.151 | 20 | 200 | fits | 17,332 | 25 (39) | 0.608 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,056 | 0.041 | 20 | 200 | fits | 11,137 | 17 (31) | 0.562 |
| LINK_UP | `adp.link_up.if0` | 2,550 | 0.025 | 20 | 200 | fits | 20,500 | 45 (11) | 0.676 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,057 | 0.151 | 20 | 200 | fits | 17,332 | 25 (39) | 0.608 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,056 | 0.041 | 20 | 200 | fits | 11,137 | 17 (31) | 0.562 |
| set_name | `aecp_fanout.set_name.if0` | 54,483 | 0.545 | 20 | 24 | fits | 61,270 | 120 | 0.349 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 55,599 | 0.556 | 20 | 24 | fits | 54,361 | 110 | 0.386 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 45,618 | 0.456 | 20 | 24 | fits | 49,849 | 110 | 0.306 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 53,283 | 0.533 | 20 | 24 | fits | 50,899 | 110 | 0.336 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 48,952 | 0.490 | 20 | 24 | fits | 54,067 | 99 | 0.367 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 48,506 | 0.485 | 20 | 24 | fits | 53,475 | 99 | 0.365 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 51,238 | 0.512 | 20 | 24 | fits | 51,895 | 99 | 0.364 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 45,676 | 0.457 | 20 | 24 | fits | 50,024 | 110 | 0.314 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 43,054 | 0.431 | 20 | 24 | fits | 50,301 | 110 | 0.327 |
| BIND_RX | `acmp.bind_rx.if0` | 21,877 | 0.219 | 20 | 20 | fits | 38,882 | 29 (77) | 0.747 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 7,555 | 0.076 | 20 | 20 | fits | 24,766 | 20 (32) | 0.799 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 11,745 | 0.117 | 20 | 20 | fits | 26,061 | 17 (47) | 0.743 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,766 | 0.138 | 20 | 20 | fits | 32,780 | 20 (50) | 0.783 |
| PROBE_TX | `acmp.probe_tx.if0` | 11,150 | 0.112 | 20 | 20 | fits | 24,488 | 19 (48) | 0.685 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 11,725 | 0.117 | 20 | 20 | fits | 25,325 | 18 (48) | 0.725 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 10,207 | 0.102 | 20 | 20 | fits | 23,292 | 18 (48) | 0.658 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 10,188 | 0.102 | 20 | 20 | fits | 23,273 | 18 (48) | 0.658 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 21,289 | 0.213 | 20 | 24 | fits | 21,527 | 22 | 0.704 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 20,771 | 0.208 | 20 | 24 | fits | 26,793 | 22 | 0.677 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 16,950 | 0.170 | 20 | 24 | fits | 20,767 | 22 | 0.638 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 16,082 | 0.161 | 20 | 24 | fits | 21,547 | 22 | 0.655 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 17,554 | 0.176 | 20 | 24 | fits | 21,371 | 22 | 0.623 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 17,041 | 0.170 | 20 | 24 | fits | 22,920 | 22 | 0.680 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 15,859 | 0.159 | 20 | 24 | fits | 19,352 | 21 | 0.612 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 18,371 | 0.184 | 20 | 24 | fits | 22,109 | 22 | 0.698 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 15,097 | 0.151 | 20 | 24 | fits | 20,724 | 22 | 0.676 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 18,636 | 0.186 | 20 | 24 | fits | 22,208 | 22 | 0.507 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 14,727 | 0.147 | 20 | 24 | fits | 20,124 | 22 | 0.689 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 15,465 | 0.155 | 20 | 24 | fits | 18,958 | 22 | 0.628 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 15,657 | 0.157 | 20 | 24 | fits | 21,212 | 22 | 0.676 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 16,990 | 0.170 | 20 | 24 | fits | 20,728 | 22 | 0.638 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 16,003 | 0.160 | 20 | 24 | fits | 21,803 | 22 | 0.698 |
| get_configuration | `aecp.get_configuration.if0` | 14,033 | 0.140 | 20 | 24 | fits | 17,492 | 22 | 0.604 |
| entity_available | `aecp.entity_available.if0` | 14,194 | 0.142 | 20 | 24 | fits | 19,536 | 22 | 0.672 |
| get_name | `aecp.get_name.if0` | 16,843 | 0.168 | 20 | 24 | fits | 23,025 | 22 | 0.727 |
| get_counters | `aecp.get_counters.if0` | 18,868 | 0.189 | 20 | 24 | fits | 22,514 | 28 | 0.647 |
| get_avb_info | `aecp.get_avb_info.if0` | 15,308 | 0.153 | 20 | 24 | fits | 20,608 | 22 | 0.718 |
| unknown_command | `aecp.unknown_command.if0` | 14,466 | 0.145 | 20 | 24 | fits | 17,883 | 22 | 0.628 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 14,439 | 0.144 | 20 | 24 | fits | 19,795 | 22 | 0.698 |
| set_name | `aecp.set_name.if0` | 25,108 | 0.251 | 20 | 24 | fits | 35,120 | 45 | 0.653 |
| lock_entity | `aecp.lock_entity.if0` | 20,114 | 0.201 | 20 | 24 | fits | 29,032 | 35 | 0.709 |
| unlock_entity | `aecp.unlock_entity.if0` | 20,923 | 0.209 | 20 | 24 | fits | 26,915 | 35 | 0.654 |
| LINK_UP | `fixture.link_up.if0` | 2,550 | 0.025 | 20 | 200 | fits | 20,500 | 45 (11) | 0.676 |
| malformed MRPDU discard | `fixture.malformed.if0` | 13,496 | 0.135 | 18 | 18 | fits | 13,561 | 14 | 0.619 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 27,187 | 0.272 | 20 | 24 | fits | 36,583 | 45 | 0.684 |
| LINK_DOWN | `fixture.link_down.if0` | 2,507 | 0.025 | 20 | 200 | fits | 22,137 | 22 (9) | 0.769 |
| BIND_RX | `fixture.bind_rx.if0` | 22,247 | 0.222 | 20 | 20 | fits | 39,450 | 29 (77) | 0.751 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 22,750 | 0.228 | 20 | 20 | fits | 36,764 | 37 (35) | 0.738 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 9,188 | 0.092 | 20 | 20 | fits | 20,011 | 14 (29) | 0.760 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 77,821 | 0.778 | 20 | 200 | fits | 77,924 | 55 | 0.748 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 77,821 | 0.778 | 20 | 200 | fits | 77,924 | 55 | 0.748 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 77,551 | 0.776 | 20 | 20 | fits | 77,924 | 55 | 0.748 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 77,551 | 0.776 | 20 | 20 | fits | 77,924 | 55 | 0.748 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 77,756 | 0.778 | 20 | 24 | fits | 77,924 | 55 | 0.748 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 77,756 | 0.778 | 20 | 24 | fits | 77,924 | 55 | 0.748 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 77,691 | 0.777 | 20 | 50 | fits | 77,924 | 55 | 0.748 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 77,691 | 0.777 | 20 | 50 | fits | 77,924 | 55 | 0.748 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 77,626 | 0.776 | 18 | 18 | fits | 77,924 | 55 | 0.748 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 77,626 | 0.776 | 18 | 18 | fits | 77,924 | 55 | 0.748 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
