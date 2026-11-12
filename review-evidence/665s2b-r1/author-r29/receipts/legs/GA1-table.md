### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 87 paths and 7 of 945 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.184 (0.366) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.090 (0.193) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.082 (0.216) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.063 (0.326) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.103 (0.204) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.093 (0.189) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.093 (0.199) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.099 (0.212) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.089 (0.250) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.144 (0.416) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.166 (0.438) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.232 (0.505) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.131 (0.414) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.157 (0.483) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.055 (0.216) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.131 (0.318) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.046 (0.125) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.024 (0.125) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.025 (0.228) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.025 (0.225) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.026 (0.152) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.104 (0.346) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.133 (0.346) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.125 (0.239) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.085 (0.198) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.168 (0.388) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.108 (0.233) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.197 (0.284) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.077 (0.194) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.154 (0.272) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.161 (0.378) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.156 (0.374) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.103 (0.219) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.179 (0.397) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.100 (0.212) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.148 (0.363) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.097 (0.223) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.093 (0.219) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.151 (0.378) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.102 (0.223) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.154 (0.380) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.112 (0.231) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.108 (0.222) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.117 (0.226) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.274 (0.518) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.138 (0.353) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.194 (0.279) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 0.366 (0.473) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.466 (0.685) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.438 (0.670) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.429 (0.659) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.402 (0.615) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.414 (0.543) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.353 (0.455) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.413 (0.625) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.532 (5.275) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-aged1-5.adp_available.if0` (backlog-adp@blank-aged1-5) | 6.923 (7.214) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.059 (0.216) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.593 (2.224) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.824 (62.964) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.379 (63.522) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.279 (0.382) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 6.197 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 1.506 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 2.862 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 5.803 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 4.126 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.115 (0.371) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.099 (0.181) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.104 (0.225) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.095 (0.371) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.098 (0.334) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 1.176 | fits | 0 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.acmp.first.if0` (backlog-adp@verify-0) | 2.137 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.136 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.adp.first.if0` (backlog-adp@verify-0) | 2.128 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-5.service.adp.last.if0` (backlog-adp@program-aged2-5) | 7.301 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.aecp.first.if0` (backlog-adp@verify-0) | 2.173 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.923 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.maap.first.if0` (backlog-adp@verify-0) | 2.163 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-5.service.maap.last.if0` (backlog-adp@program-aged2-5) | 7.337 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-aged1-7.service.srp.first.if0` (backlog-adp@blank-aged1-7) | 6.464 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-4.service.srp.last.if0` (backlog-adp@verify-aged2-4) | 8.586 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.787 (1.165) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.384 (0.385) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.150 (0.150) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.768 (0.842) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 9.001 | 7 | 152,865 (1.529) | yes | - |
| backlog-adp@blank-1 | 0 | 8.332 | 7 | 152,865 (1.529) | yes | - |
| backlog-adp@blank-2 | 0 | 9.280 | 8 | 157,381 (1.574) | yes | - |
| backlog-adp@blank-3 | 0 | 9.357 | 8 | 151,146 (1.511) | yes | - |
| backlog-adp@blank-4 | 0 | 9.355 | 8 | 148,311 (1.483) | yes | - |
| backlog-adp@blank-5 | 0 | 9.167 | 7 | 153,218 (1.532) | yes | - |
| backlog-adp@blank-6 | 0 | 9.255 | 8 | 148,362 (1.484) | yes | - |
| backlog-adp@blank-7 | 0 | 9.296 | 8 | 150,946 (1.509) | yes | - |
| backlog-adp@program-0 | 0 | 8.320 | 7 | 148,248 (1.482) | yes | - |
| backlog-adp@program-1 | 0 | 9.293 | 8 | 157,199 (1.572) | yes | - |
| backlog-adp@program-2 | 0 | 9.278 | 8 | 157,980 (1.580) | yes | - |
| backlog-adp@program-3 | 0 | 9.330 | 8 | 152,497 (1.525) | yes | - |
| backlog-adp@program-4 | 0 | 8.347 | 7 | 148,108 (1.481) | yes | - |
| backlog-adp@program-5 | 0 | 8.475 | 8 | 147,834 (1.478) | yes | - |
| backlog-adp@program-6 | 0 | 8.477 | 7 | 157,692 (1.577) | yes | - |
| backlog-adp@program-7 | 0 | 8.578 | 8 | 152,295 (1.523) | yes | - |
| backlog-adp@verify-0 | 0 | 9.014 | 7 | 153,262 (1.533) | yes | - |
| backlog-adp@verify-1 | 0 | 8.343 | 7 | 153,262 (1.533) | yes | - |
| backlog-adp@verify-2 | 0 | 9.268 | 8 | 150,139 (1.501) | yes | - |
| backlog-adp@verify-3 | 0 | 9.391 | 8 | 146,784 (1.468) | yes | - |
| backlog-adp@verify-4 | 0 | 9.174 | 7 | 157,861 (1.579) | yes | - |
| backlog-adp@verify-5 | 0 | 9.040 | 6 | 153,273 (1.533) | yes | - |
| backlog-adp@verify-6 | 0 | 9.270 | 8 | 150,300 (1.503) | yes | - |
| backlog-adp@verify-7 | 0 | 9.329 | 8 | 152,524 (1.525) | yes | - |
| backlog-adp@blank-aged2-0 | 1 | 9.018 | 6 | 152,529 (1.525) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 10.392 | 10 | 151,436 (1.514) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 9.313 | 9 | 147,691 (1.477) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 9.320 | 8 | 145,951 (1.460) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 9.117 | 6 | 147,187 (1.472) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 9.118 | 6 | 151,521 (1.515) | yes | - |
| backlog-adp@blank-aged2-6 | 1 | 9.032 | 6 | 156,894 (1.569) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 9.112 | 7 | 156,078 (1.561) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 9.224 | 7 | 146,391 (1.464) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 10.872 | 8 | 151,500 (1.515) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 10.010 | 9 | 148,009 (1.480) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 10.057 | 10 | 157,312 (1.573) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 10.037 | 9 | 157,414 (1.574) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 9.886 | 8 | 155,575 (1.556) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 9.894 | 8 | 149,898 (1.499) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 9.989 | 7 | 154,138 (1.541) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 9.089 | 7 | 157,346 (1.573) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 9.438 | 8 | 152,089 (1.521) | yes | - |
| backlog-adp@program-aged2-2 | 1 | 9.104 | 7 | 156,868 (1.569) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 9.112 | 7 | 156,718 (1.567) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 9.335 | 8 | 147,605 (1.476) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 9.199 | 7 | 148,311 (1.483) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 9.456 | 9 | 152,978 (1.530) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 9.289 | 7 | 146,269 (1.463) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 9.119 | 7 | 148,209 (1.482) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 9.712 | 10 | 156,990 (1.570) | yes | - |
| backlog-adp@program-aged1-2 | 1 | 9.192 | 7 | 156,587 (1.566) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 9.348 | 8 | 156,430 (1.564) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 9.155 | 6 | 152,170 (1.522) | yes | - |
| backlog-adp@program-aged1-5 | 1 | 9.139 | 6 | 152,599 (1.526) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 9.174 | 7 | 147,950 (1.480) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 9.293 | 8 | 150,886 (1.509) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 9.135 | 8 | 148,370 (1.484) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 10.091 | 8 | 152,801 (1.528) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 9.179 | 8 | 156,803 (1.568) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 9.361 | 8 | 150,827 (1.508) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 9.247 | 7 | 148,866 (1.489) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 9.115 | 6 | 152,764 (1.528) | yes | - |
| backlog-adp@verify-aged2-6 | 1 | 9.235 | 7 | 151,339 (1.513) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 9.294 | 8 | 150,876 (1.509) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 9.061 | 7 | 157,011 (1.570) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 10.144 | 8 | 150,995 (1.510) | yes | - |
| backlog-adp@verify-aged1-2 | 1 | 9.168 | 7 | 156,563 (1.566) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 9.184 | 7 | 156,386 (1.564) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 9.304 | 8 | 147,645 (1.476) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 9.196 | 7 | 147,993 (1.480) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 9.469 | 9 | 153,173 (1.532) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 9.363 | 8 | 146,567 (1.466) | yes | - |
| backlog | 0 | 5.866 | 8 | 148,995 (1.490) | yes | - |
| backlog-adp | 0 | 8.536 | 8 | 146,259 (1.463) | yes | - |
| backlog-adp-refill | 0 | 40.550 | 22 | 149,347 (1.493) | yes | - |
| backlog-owed | 0 | 63.854 | 22 | 163,134 (1.631) | yes | - |
| fixture | 0 | 1.100 | 2 | 74,795 (0.748) | yes | - |

Composed maximum over the 4 backlog windows: 163,134 CPU cycles (1.631 ms), backlog-owed.
Over the windows that released their whole load only: 163,134 (1.631 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3597 | 0 | 61,769 (0.618) | fits |
| save-second | 66014 | 0 | 61,769 (0.618) | fits |
| backlog-adp@blank-0 | 408 | 0 | 152,865 (1.529) | fits |
| backlog-adp@blank-1 | 408 | 0 | 152,865 (1.529) | fits |
| backlog-adp@blank-2 | 409 | 0 | 157,381 (1.574) | fits |
| backlog-adp@blank-3 | 409 | 0 | 151,146 (1.511) | fits |
| backlog-adp@blank-4 | 409 | 0 | 148,311 (1.483) | fits |
| backlog-adp@blank-5 | 408 | 0 | 153,218 (1.532) | fits |
| backlog-adp@blank-6 | 411 | 0 | 148,362 (1.484) | fits |
| backlog-adp@blank-7 | 411 | 0 | 150,946 (1.509) | fits |
| backlog-adp@program-0 | 510 | 0 | 148,248 (1.482) | fits |
| backlog-adp@program-1 | 511 | 0 | 157,199 (1.572) | fits |
| backlog-adp@program-2 | 513 | 0 | 157,980 (1.580) | fits |
| backlog-adp@program-3 | 513 | 0 | 152,497 (1.525) | fits |
| backlog-adp@program-4 | 513 | 0 | 148,108 (1.481) | fits |
| backlog-adp@program-5 | 516 | 0 | 147,834 (1.478) | fits |
| backlog-adp@program-6 | 515 | 0 | 157,692 (1.577) | fits |
| backlog-adp@program-7 | 516 | 0 | 152,295 (1.523) | fits |
| backlog-adp@verify-0 | 605 | 0 | 153,262 (1.533) | fits |
| backlog-adp@verify-1 | 605 | 0 | 153,262 (1.533) | fits |
| backlog-adp@verify-2 | 606 | 0 | 150,139 (1.501) | fits |
| backlog-adp@verify-3 | 606 | 0 | 146,784 (1.468) | fits |
| backlog-adp@verify-4 | 605 | 0 | 157,861 (1.579) | fits |
| backlog-adp@verify-5 | 605 | 0 | 153,273 (1.533) | fits |
| backlog-adp@verify-6 | 608 | 0 | 150,300 (1.503) | fits |
| backlog-adp@verify-7 | 608 | 0 | 152,524 (1.525) | fits |
| backlog-adp@blank-aged2-0 | 829 | 0 | 152,529 (1.525) | fits |
| backlog-adp@blank-aged2-1 | 840 | 0 | 151,436 (1.514) | fits |
| backlog-adp@blank-aged2-2 | 850 | 0 | 147,691 (1.477) | fits |
| backlog-adp@blank-aged2-3 | 860 | 0 | 145,951 (1.460) | fits |
| backlog-adp@blank-aged2-4 | 869 | 0 | 148,660 (1.487) | fits |
| backlog-adp@blank-aged2-5 | 880 | 0 | 151,521 (1.515) | fits |
| backlog-adp@blank-aged2-6 | 891 | 0 | 156,894 (1.569) | fits |
| backlog-adp@blank-aged2-7 | 902 | 0 | 156,078 (1.561) | fits |
| backlog-adp@blank-aged1-0 | 746 | 0 | 146,391 (1.464) | fits |
| backlog-adp@blank-aged1-1 | 758 | 0 | 151,500 (1.515) | fits |
| backlog-adp@blank-aged1-2 | 769 | 0 | 148,009 (1.480) | fits |
| backlog-adp@blank-aged1-3 | 781 | 0 | 157,312 (1.573) | fits |
| backlog-adp@blank-aged1-4 | 791 | 0 | 157,414 (1.574) | fits |
| backlog-adp@blank-aged1-5 | 801 | 0 | 155,575 (1.556) | fits |
| backlog-adp@blank-aged1-6 | 812 | 0 | 149,898 (1.499) | fits |
| backlog-adp@blank-aged1-7 | 822 | 0 | 154,138 (1.541) | fits |
| backlog-adp@program-aged2-0 | 928 | 0 | 157,346 (1.573) | fits |
| backlog-adp@program-aged2-1 | 940 | 0 | 152,089 (1.521) | fits |
| backlog-adp@program-aged2-2 | 950 | 0 | 156,868 (1.569) | fits |
| backlog-adp@program-aged2-3 | 960 | 0 | 156,718 (1.567) | fits |
| backlog-adp@program-aged2-4 | 972 | 0 | 147,605 (1.476) | fits |
| backlog-adp@program-aged2-5 | 982 | 0 | 148,311 (1.483) | fits |
| backlog-adp@program-aged2-6 | 995 | 0 | 152,978 (1.530) | fits |
| backlog-adp@program-aged2-7 | 1004 | 0 | 146,269 (1.463) | fits |
| backlog-adp@program-aged1-0 | 841 | 0 | 148,209 (1.482) | fits |
| backlog-adp@program-aged1-1 | 855 | 0 | 156,990 (1.570) | fits |
| backlog-adp@program-aged1-2 | 864 | 0 | 156,587 (1.566) | fits |
| backlog-adp@program-aged1-3 | 875 | 0 | 156,430 (1.564) | fits |
| backlog-adp@program-aged1-4 | 884 | 0 | 156,430 (1.564) | fits |
| backlog-adp@program-aged1-5 | 895 | 0 | 152,599 (1.526) | fits |
| backlog-adp@program-aged1-6 | 906 | 0 | 147,950 (1.480) | fits |
| backlog-adp@program-aged1-7 | 918 | 0 | 150,886 (1.509) | fits |
| backlog-adp@verify-aged2-0 | 1023 | 0 | 148,370 (1.484) | fits |
| backlog-adp@verify-aged2-1 | 1034 | 0 | 152,801 (1.528) | fits |
| backlog-adp@verify-aged2-2 | 1045 | 0 | 156,803 (1.568) | fits |
| backlog-adp@verify-aged2-3 | 1056 | 0 | 150,827 (1.508) | fits |
| backlog-adp@verify-aged2-4 | 1066 | 0 | 148,866 (1.489) | fits |
| backlog-adp@verify-aged2-5 | 1076 | 0 | 152,764 (1.528) | fits |
| backlog-adp@verify-aged2-6 | 1088 | 0 | 151,339 (1.513) | fits |
| backlog-adp@verify-aged2-7 | 1099 | 0 | 150,876 (1.509) | fits |
| backlog-adp@verify-aged1-0 | 936 | 0 | 157,011 (1.570) | fits |
| backlog-adp@verify-aged1-1 | 948 | 0 | 150,995 (1.510) | fits |
| backlog-adp@verify-aged1-2 | 958 | 0 | 156,563 (1.566) | fits |
| backlog-adp@verify-aged1-3 | 968 | 0 | 156,386 (1.564) | fits |
| backlog-adp@verify-aged1-4 | 980 | 0 | 147,645 (1.476) | fits |
| backlog-adp@verify-aged1-5 | 990 | 0 | 147,993 (1.480) | fits |
| backlog-adp@verify-aged1-6 | 1003 | 0 | 153,173 (1.532) | fits |
| backlog-adp@verify-aged1-7 | 1013 | 0 | 146,567 (1.466) | fits |
| adp-advertise | 592 | 0 | 61,769 (0.618) | fits |
| save-held | 1221 | 0 | 152,339 (1.523) | fits |
| save-starved | 35542 | 0 | 153,897 (1.539) | fits |
| acmp-noresp | 2019 | 0 | 61,769 (0.618) | fits |
| save | 603 | 0 | 61,769 (0.618) | fits |
| srp | 285 | 0 | 83,547 (0.835) | fits |
| backlog | 283 | 0 | 148,995 (1.490) | fits |
| backlog-adp | 308 | 0 | 146,259 (1.463) | fits |
| backlog-adp-refill | 322 | 0 | 149,347 (1.493) | fits |
| backlog-owed | 303 | 0 | 163,134 (1.631) | fits |
| acmp-disc | 933 | 0 | 61,769 (0.618) | fits |
| maap | 176 | 0 | 61,769 (0.618) | fits |
| adp-link | 88 | 0 | 61,769 (0.618) | fits |
| adp-gm | 87 | 0 | 61,769 (0.618) | fits |
| adp-discover | 87 | 0 | 61,769 (0.618) | fits |
| control | 87 | 0 | 61,769 (0.618) | fits |
| aecp-fanout | 110 | 0 | 61,769 (0.618) | fits |
| acmp-cmd | 83 | 0 | 61,769 (0.618) | fits |
| aecp | 110 | 0 | 61,769 (0.618) | fits |
| fixture | 149 | 0 | 74,795 (0.748) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 7.889 (20) | 12.111 |
| backlog-adp@blank-aged2-1 | 2 | none | none | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 7.902 (20) | 12.098 |
| backlog-adp@blank-aged2-2 | 2 | none | none | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 7.908 (20) | 12.092 |
| backlog-adp@blank-aged2-3 | 2 | none | none | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 8.956 (20) | 11.044 |
| backlog-adp@blank-aged2-4 | 2 | +6.524 ms, 76,794 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 8.750 (20) | 11.250 |
| backlog-adp@blank-aged2-5 | 2 | +5.653 ms, 76,877 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 8.750 (20) | 11.250 |
| backlog-adp@blank-aged2-6 | 2 | +4.470 ms, 76,877 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 8.664 (20) | 11.336 |
| backlog-adp@blank-aged2-7 | 2 | none | none | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 8.745 (20) | 11.255 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 8.097 (20) | 11.903 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 7.931 (20) | 12.069 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 7.936 (20) | 12.064 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 8.690 (20) | 11.310 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 8.676 (20) | 11.324 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 8.754 (20) | 11.246 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 8.762 (20) | 11.238 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 8.862 (20) | 11.138 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 7.923 (20) | 12.078 |
| backlog-adp@program-aged2-1 | 2 | none | none | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 7.743 (20) | 12.257 |
| backlog-adp@program-aged2-2 | 2 | none | +8.051 ms, 79,624 (0.796 ms), issue | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 7.887 (20) | 12.113 |
| backlog-adp@program-aged2-3 | 2 | none | +8.049 ms, 80,085 (0.801 ms), issue | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 8.037 (20) | 11.963 |
| backlog-adp@program-aged2-4 | 2 | +6.489 ms, 80,024 (0.800 ms), issue | none | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 8.967 (20) | 11.033 |
| backlog-adp@program-aged2-5 | 2 | +5.085 ms, 79,901 (0.799 ms), issue | none | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 8.825 (20) | 11.175 |
| backlog-adp@program-aged2-6 | 2 | +4.500 ms, 80,061 (0.801 ms), issue | none | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 8.780 (20) | 11.220 |
| backlog-adp@program-aged2-7 | 2 | +4.280 ms, 80,015 (0.800 ms), issue | none | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 8.923 (20) | 11.077 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 7.947 (20) | 12.053 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 7.891 (20) | 12.109 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 7.758 (20) | 12.242 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 7.961 (20) | 12.039 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 7.989 (20) | 12.011 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 7.973 (20) | 12.027 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 8.003 (20) | 11.997 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 8.128 (20) | 11.872 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 7.772 (20) | 12.228 |
| backlog-adp@verify-aged2-1 | 2 | none | none | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 7.927 (20) | 12.073 |
| backlog-adp@verify-aged2-2 | 2 | none | +8.160 ms, 77,256 (0.773 ms), read-back | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 7.993 (20) | 12.007 |
| backlog-adp@verify-aged2-3 | 2 | +7.975 ms, 77,737 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 8.994 (20) | 11.006 |
| backlog-adp@verify-aged2-4 | 2 | +5.862 ms, 77,626 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 8.880 (20) | 11.120 |
| backlog-adp@verify-aged2-5 | 2 | +5.648 ms, 77,466 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 8.745 (20) | 11.255 |
| backlog-adp@verify-aged2-6 | 2 | +4.356 ms, 77,505 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 8.870 (20) | 11.130 |
| backlog-adp@verify-aged2-7 | 2 | +2.979 ms, 77,756 (0.778 ms), read-back | none | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 8.927 (20) | 11.073 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 7.923 (20) | 12.077 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 7.765 (20) | 12.235 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 7.885 (20) | 12.115 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 8.037 (20) | 11.963 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 8.164 (20) | 11.836 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 8.051 (20) | 11.949 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 7.986 (20) | 12.014 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 8.004 (20) | 11.996 |

Least margin over the aged windows: 11.006 ms, `backlog-adp@verify-aged2-3.service.aecp.last.if0` at 8.994 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6029.864 | 6,070 | 102 | 2 | 30.824 | yes | within |
| save-held | 2018.016 | 4,070 | 102 | - | 12.854 | no | within |
| save-starved | 4047.985 | 4,070 | 102 | - | 31.460 | yes | within |
| save | 2018.305 | 4,070 | 102 | - | 10.832 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 93,040 (0.930) | 78,665 (0.787) |
| save-second | 520 | 80,729 (0.807) | 77,956 (0.780) |
| backlog-adp@blank-0 | 298 | 86,591 (0.866) | 76,303 (0.763) |
| backlog-adp@blank-1 | 298 | 86,591 (0.866) | 76,303 (0.763) |
| backlog-adp@blank-2 | 299 | 87,474 (0.875) | 76,603 (0.766) |
| backlog-adp@blank-3 | 299 | 87,926 (0.879) | 76,767 (0.768) |
| backlog-adp@blank-4 | 299 | 88,076 (0.881) | 76,767 (0.768) |
| backlog-adp@blank-5 | 299 | 88,025 (0.880) | 76,670 (0.767) |
| backlog-adp@blank-6 | 299 | 87,191 (0.872) | 76,670 (0.767) |
| backlog-adp@blank-7 | 299 | 87,714 (0.877) | 76,735 (0.767) |
| backlog-adp@program-0 | 327 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@program-1 | 328 | 92,943 (0.929) | 79,192 (0.792) |
| backlog-adp@program-2 | 328 | 92,943 (0.929) | 79,086 (0.791) |
| backlog-adp@program-3 | 328 | 92,943 (0.929) | 79,192 (0.792) |
| backlog-adp@program-4 | 328 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@program-5 | 329 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@program-6 | 329 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@program-7 | 329 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-0 | 354 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-1 | 354 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-2 | 355 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-3 | 355 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-4 | 355 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-5 | 355 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-6 | 355 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-7 | 355 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@blank-aged2-0 | 297 | 87,947 (0.879) | 76,639 (0.766) |
| backlog-adp@blank-aged2-1 | 298 | 87,994 (0.880) | 76,639 (0.766) |
| backlog-adp@blank-aged2-2 | 297 | 84,329 (0.843) | 76,338 (0.763) |
| backlog-adp@blank-aged2-3 | 297 | 84,687 (0.847) | 76,369 (0.764) |
| backlog-adp@blank-aged2-4 | 297 | 76,794 (0.768) | 76,085 (0.761) |
| backlog-adp@blank-aged2-5 | 297 | 76,877 (0.769) | 76,043 (0.760) |
| backlog-adp@blank-aged2-6 | 297 | 76,877 (0.769) | 76,043 (0.760) |
| backlog-adp@blank-aged2-7 | 297 | 84,256 (0.843) | 76,404 (0.764) |
| backlog-adp@blank-aged1-0 | 297 | 87,790 (0.878) | 76,736 (0.767) |
| backlog-adp@blank-aged1-1 | 298 | 93,110 (0.931) | 76,639 (0.766) |
| backlog-adp@blank-aged1-2 | 297 | 93,492 (0.935) | 76,640 (0.766) |
| backlog-adp@blank-aged1-3 | 297 | 88,687 (0.887) | 76,456 (0.765) |
| backlog-adp@blank-aged1-4 | 297 | 87,172 (0.872) | 76,639 (0.766) |
| backlog-adp@blank-aged1-5 | 297 | 88,142 (0.881) | 76,639 (0.766) |
| backlog-adp@blank-aged1-6 | 297 | 88,123 (0.881) | 76,639 (0.766) |
| backlog-adp@blank-aged1-7 | 297 | 87,690 (0.877) | 76,639 (0.766) |
| backlog-adp@program-aged2-0 | 326 | 92,943 (0.929) | 79,095 (0.791) |
| backlog-adp@program-aged2-1 | 327 | 92,943 (0.929) | 79,086 (0.791) |
| backlog-adp@program-aged2-2 | 326 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@program-aged2-3 | 326 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@program-aged2-4 | 326 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@program-aged2-5 | 326 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@program-aged2-6 | 326 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@program-aged2-7 | 326 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@program-aged1-0 | 326 | 92,943 (0.929) | 79,014 (0.790) |
| backlog-adp@program-aged1-1 | 327 | 92,943 (0.929) | 79,095 (0.791) |
| backlog-adp@program-aged1-2 | 326 | 92,943 (0.929) | 78,841 (0.788) |
| backlog-adp@program-aged1-3 | 326 | 92,943 (0.929) | 79,086 (0.791) |
| backlog-adp@program-aged1-4 | 326 | 92,943 (0.929) | 79,095 (0.791) |
| backlog-adp@program-aged1-5 | 326 | 92,943 (0.929) | 79,095 (0.791) |
| backlog-adp@program-aged1-6 | 326 | 92,943 (0.929) | 79,014 (0.790) |
| backlog-adp@program-aged1-7 | 326 | 92,943 (0.929) | 79,192 (0.792) |
| backlog-adp@verify-aged2-0 | 355 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-aged2-1 | 356 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-aged2-2 | 355 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-aged2-3 | 355 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-aged2-4 | 355 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-aged2-5 | 355 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-aged2-6 | 355 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-aged2-7 | 355 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-aged1-0 | 355 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-aged1-1 | 356 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-aged1-2 | 355 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-aged1-3 | 355 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-aged1-4 | 355 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-aged1-5 | 355 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-aged1-6 | 355 | 92,943 (0.929) | 78,697 (0.787) |
| backlog-adp@verify-aged1-7 | 355 | 92,943 (0.929) | 78,697 (0.787) |
| adp-advertise | 578 | 18,847 (0.188) | 3,272 (0.033) |
| save-held | 722 | 92,267 (0.923) | 78,891 (0.789) |
| save-starved | 418 | 81,155 (0.812) | 78,640 (0.786) |
| acmp-noresp | 615 | 92,879 (0.929) | 78,665 (0.787) |
| save | 585 | 91,854 (0.919) | 78,593 (0.786) |
| srp | 271 | 18,847 (0.188) | 3,272 (0.033) |
| backlog | 265 | 18,847 (0.188) | 3,272 (0.033) |
| backlog-adp | 271 | 18,847 (0.188) | 3,456 (0.035) |
| backlog-adp-refill | 274 | 18,847 (0.188) | 3,280 (0.033) |
| backlog-owed | 276 | 18,847 (0.188) | 3,350 (0.034) |
| acmp-disc | 305 | 92,938 (0.929) | 78,665 (0.787) |
| maap | 166 | 18,847 (0.188) | 3,272 (0.033) |
| adp-link | 80 | 18,837 (0.188) | 3,272 (0.033) |
| adp-gm | 80 | 18,837 (0.188) | 3,272 (0.033) |
| adp-discover | 80 | 18,837 (0.188) | 3,272 (0.033) |
| control | 80 | 18,837 (0.188) | 3,272 (0.033) |
| aecp-fanout | 79 | 18,837 (0.188) | 3,272 (0.033) |
| acmp-cmd | 65 | 18,837 (0.188) | 3,272 (0.033) |
| aecp | 79 | 18,837 (0.188) | 3,272 (0.033) |
| fixture | 54 | 15,204 (0.152) | 3,272 (0.033) |

Longest pass that carries a step: 93,492 CPU cycles (0.935 ms), backlog-adp@blank-aged1-2; longest step: 79,192 (0.792 ms), backlog-adp@program-1.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 15,658 | 0.157 | 20 | 20 | fits | 28,243 | 19 (14) | 0.897 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 647,313 | 6.473 | 20 | 20 | fits | 146,424 | 168 | 0.550 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 211,543 | 2.115 | 20 | 200 | fits | 143,738 | 223 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 697,342 | 6.973 | 20 | 200 | fits | 146,424 | 168 | 0.550 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 212,455 | 2.125 | 20 | 20 | fits | 143,738 | 223 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 859,804 | 8.598 | 20 | 20 | fits | 152,865 | 124 | 0.511 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 216,040 | 2.160 | 20 | 24 | fits | 143,738 | 223 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 863,239 | 8.632 | 20 | 24 | fits | 152,865 | 124 | 0.511 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 215,000 | 2.150 | 20 | 50 | fits | 143,738 | 223 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 701,018 | 7.010 | 20 | 50 | fits | 146,424 | 168 | 0.550 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 356,351 | 3.564 | 20 | 20 | fits | 141,806 | 94 | 0.564 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 552,514 | 5.525 | 20 | 20 | fits | 82,142 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 580,333 | 5.803 | 20 | 20 | fits | 146,557 | 168 | 0.551 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 144,593 | 1.446 | 20 | 200 | fits | 143,601 | 223 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 630,402 | 6.304 | 20 | 200 | fits | 146,557 | 168 | 0.551 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 145,505 | 1.455 | 20 | 20 | fits | 143,601 | 223 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 792,864 | 7.929 | 20 | 20 | fits | 152,865 | 124 | 0.511 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 149,090 | 1.491 | 20 | 24 | fits | 143,601 | 223 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 796,299 | 7.963 | 20 | 24 | fits | 152,865 | 124 | 0.511 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 148,050 | 1.480 | 20 | 50 | fits | 143,601 | 223 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 634,078 | 6.341 | 20 | 50 | fits | 146,557 | 168 | 0.551 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 289,285 | 2.893 | 20 | 20 | fits | 141,690 | 94 | 0.563 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 485,441 | 4.854 | 20 | 20 | fits | 82,142 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 632,957 | 6.330 | 20 | 20 | fits | 146,922 | 167 | 0.556 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 159,235 | 1.592 | 20 | 200 | fits | 157,381 | 232 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 659,344 | 6.593 | 20 | 200 | fits | 146,922 | 167 | 0.556 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 160,147 | 1.601 | 20 | 20 | fits | 157,381 | 232 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 796,510 | 7.965 | 20 | 20 | fits | 136,470 | 111 | 0.503 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 163,732 | 1.637 | 20 | 24 | fits | 157,381 | 232 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 799,945 | 7.999 | 20 | 24 | fits | 136,470 | 111 | 0.503 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 162,692 | 1.627 | 20 | 50 | fits | 157,381 | 232 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 663,020 | 6.630 | 20 | 50 | fits | 146,922 | 167 | 0.556 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 304,114 | 3.041 | 20 | 20 | fits | 141,877 | 94 | 0.568 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 504,810 | 5.048 | 20 | 20 | fits | 86,741 | 43 | 0.515 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 611,889 | 6.119 | 20 | 20 | fits | 151,146 | 168 | 0.547 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 146,104 | 1.461 | 20 | 200 | fits | 143,388 | 223 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 652,065 | 6.521 | 20 | 200 | fits | 151,146 | 168 | 0.547 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 147,016 | 1.470 | 20 | 20 | fits | 143,388 | 223 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 794,442 | 7.944 | 20 | 20 | fits | 141,681 | 109 | 0.557 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 150,601 | 1.506 | 20 | 24 | fits | 143,388 | 223 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 822,599 | 8.226 | 20 | 24 | fits | 24,722 | 18 | 0.660 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 149,561 | 1.496 | 20 | 50 | fits | 143,388 | 223 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 655,741 | 6.557 | 20 | 50 | fits | 151,146 | 168 | 0.547 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 291,066 | 2.911 | 20 | 20 | fits | 141,960 | 94 | 0.568 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 502,515 | 5.025 | 20 | 20 | fits | 87,910 | 43 | 0.570 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 611,323 | 6.113 | 20 | 20 | fits | 148,311 | 165 | 0.581 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 146,689 | 1.467 | 20 | 200 | fits | 143,111 | 223 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 649,933 | 6.499 | 20 | 200 | fits | 148,311 | 165 | 0.581 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 147,601 | 1.476 | 20 | 20 | fits | 143,111 | 223 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 794,201 | 7.942 | 20 | 20 | fits | 143,572 | 111 | 0.514 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 151,186 | 1.512 | 20 | 24 | fits | 143,111 | 223 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 822,371 | 8.224 | 20 | 24 | fits | 24,735 | 18 | 0.658 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 150,146 | 1.501 | 20 | 50 | fits | 143,111 | 223 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 653,609 | 6.536 | 20 | 50 | fits | 148,311 | 165 | 0.581 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 291,617 | 2.916 | 20 | 20 | fits | 141,926 | 95 | 0.564 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 503,218 | 5.032 | 20 | 20 | fits | 82,622 | 36 | 0.473 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 282,019 | 2.820 | 20 | 20 | fits | 153,218 | 213 | 0.528 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 147,722 | 1.477 | 20 | 200 | fits | 143,282 | 224 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 308,773 | 3.088 | 20 | 200 | fits | 153,218 | 213 | 0.528 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 148,634 | 1.486 | 20 | 20 | fits | 143,282 | 224 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 800,104 | 8.001 | 20 | 20 | fits | 150,980 | 118 | 0.504 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 152,219 | 1.522 | 20 | 24 | fits | 143,282 | 224 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 803,539 | 8.035 | 20 | 24 | fits | 150,980 | 118 | 0.504 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 151,179 | 1.512 | 20 | 50 | fits | 143,282 | 224 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 312,449 | 3.124 | 20 | 50 | fits | 153,218 | 213 | 0.528 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 446,389 | 4.464 | 20 | 20 | fits | 134,005 | 52 | 0.594 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 650,024 | 6.500 | 20 | 20 | fits | 82,653 | 36 | 0.473 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 587,556 | 5.876 | 20 | 20 | fits | 146,664 | 167 | 0.553 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 144,709 | 1.447 | 20 | 200 | fits | 143,499 | 223 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 637,411 | 6.374 | 20 | 200 | fits | 146,664 | 167 | 0.553 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 145,621 | 1.456 | 20 | 20 | fits | 143,499 | 223 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 786,469 | 7.865 | 20 | 20 | fits | 148,362 | 119 | 0.488 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 149,206 | 1.492 | 20 | 24 | fits | 143,499 | 223 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 789,904 | 7.899 | 20 | 24 | fits | 148,362 | 119 | 0.488 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 148,166 | 1.482 | 20 | 50 | fits | 143,499 | 223 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 641,087 | 6.411 | 20 | 50 | fits | 146,664 | 167 | 0.553 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 289,486 | 2.895 | 20 | 20 | fits | 141,775 | 94 | 0.564 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 492,343 | 4.923 | 20 | 20 | fits | 82,492 | 36 | 0.469 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 271,437 | 2.714 | 20 | 20 | fits | 150,946 | 206 | 0.543 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 146,015 | 1.460 | 20 | 200 | fits | 143,943 | 223 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 296,352 | 2.964 | 20 | 200 | fits | 150,946 | 206 | 0.543 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 146,927 | 1.469 | 20 | 20 | fits | 143,943 | 223 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 788,535 | 7.885 | 20 | 20 | fits | 150,186 | 117 | 0.551 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 150,512 | 1.505 | 20 | 24 | fits | 143,943 | 223 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 816,890 | 8.169 | 20 | 24 | fits | 24,920 | 18 | 0.671 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 149,472 | 1.495 | 20 | 50 | fits | 143,943 | 223 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 300,028 | 3.000 | 20 | 50 | fits | 150,946 | 206 | 0.543 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 433,705 | 4.337 | 20 | 20 | fits | 133,742 | 52 | 0.591 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 629,975 | 6.300 | 20 | 20 | fits | 82,252 | 37 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 593,603 | 5.936 | 20 | 20 | fits | 146,723 | 168 | 0.552 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 140,540 | 1.405 | 20 | 200 | fits | 143,647 | 223 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 642,090 | 6.421 | 20 | 200 | fits | 146,723 | 168 | 0.552 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 141,452 | 1.415 | 20 | 20 | fits | 143,647 | 223 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 791,034 | 7.910 | 20 | 20 | fits | 148,248 | 118 | 0.487 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 145,037 | 1.450 | 20 | 24 | fits | 143,647 | 223 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 794,469 | 7.945 | 20 | 24 | fits | 148,248 | 118 | 0.487 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 143,997 | 1.440 | 20 | 50 | fits | 143,647 | 223 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 645,766 | 6.458 | 20 | 50 | fits | 146,723 | 168 | 0.552 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 285,407 | 2.854 | 20 | 20 | fits | 141,865 | 94 | 0.566 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 496,963 | 4.970 | 20 | 20 | fits | 88,074 | 43 | 0.572 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 259,242 | 2.592 | 20 | 20 | fits | 157,199 | 216 | 0.514 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 142,665 | 1.427 | 20 | 200 | fits | 144,048 | 223 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 299,255 | 2.993 | 20 | 200 | fits | 157,199 | 216 | 0.514 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 143,577 | 1.436 | 20 | 20 | fits | 144,048 | 223 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 783,892 | 7.839 | 20 | 20 | fits | 143,170 | 106 | 0.568 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 147,162 | 1.472 | 20 | 24 | fits | 144,048 | 223 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 812,236 | 8.122 | 20 | 24 | fits | 24,909 | 18 | 0.671 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 146,122 | 1.461 | 20 | 50 | fits | 144,048 | 223 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 302,931 | 3.029 | 20 | 50 | fits | 157,199 | 216 | 0.514 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 445,290 | 4.453 | 20 | 20 | fits | 134,392 | 52 | 0.600 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 641,622 | 6.416 | 20 | 20 | fits | 82,142 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 620,547 | 6.205 | 20 | 20 | fits | 146,876 | 166 | 0.555 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 153,823 | 1.538 | 20 | 200 | fits | 157,980 | 232 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 647,006 | 6.470 | 20 | 200 | fits | 146,876 | 166 | 0.555 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 154,735 | 1.547 | 20 | 20 | fits | 157,980 | 232 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 784,588 | 7.846 | 20 | 20 | fits | 136,886 | 112 | 0.506 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 158,320 | 1.583 | 20 | 24 | fits | 157,980 | 232 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 788,023 | 7.880 | 20 | 24 | fits | 136,886 | 112 | 0.506 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 157,280 | 1.573 | 20 | 50 | fits | 157,980 | 232 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 650,682 | 6.507 | 20 | 50 | fits | 146,876 | 166 | 0.555 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 298,698 | 2.987 | 20 | 20 | fits | 141,873 | 94 | 0.567 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 501,726 | 5.017 | 20 | 20 | fits | 89,045 | 42 | 0.539 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 253,066 | 2.531 | 20 | 20 | fits | 152,497 | 205 | 0.554 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 141,346 | 1.413 | 20 | 200 | fits | 143,779 | 223 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 293,234 | 2.932 | 20 | 200 | fits | 152,497 | 205 | 0.554 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 142,258 | 1.423 | 20 | 20 | fits | 143,779 | 223 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 787,892 | 7.879 | 20 | 20 | fits | 146,653 | 111 | 0.535 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 145,843 | 1.458 | 20 | 24 | fits | 143,779 | 223 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 815,891 | 8.159 | 20 | 24 | fits | 24,564 | 18 | 0.656 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 144,803 | 1.448 | 20 | 50 | fits | 143,779 | 223 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 296,910 | 2.969 | 20 | 50 | fits | 152,497 | 205 | 0.554 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 430,593 | 4.306 | 20 | 20 | fits | 133,748 | 52 | 0.590 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 642,139 | 6.421 | 20 | 20 | fits | 88,180 | 43 | 0.574 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 596,702 | 5.967 | 20 | 20 | fits | 146,376 | 168 | 0.550 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 143,741 | 1.437 | 20 | 200 | fits | 143,760 | 223 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 645,024 | 6.450 | 20 | 200 | fits | 146,376 | 168 | 0.550 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 144,653 | 1.447 | 20 | 20 | fits | 143,760 | 223 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 793,828 | 7.938 | 20 | 20 | fits | 148,108 | 118 | 0.486 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 148,238 | 1.482 | 20 | 24 | fits | 143,760 | 223 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 797,263 | 7.973 | 20 | 24 | fits | 148,108 | 118 | 0.486 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 147,198 | 1.472 | 20 | 50 | fits | 143,760 | 223 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 648,700 | 6.487 | 20 | 50 | fits | 146,376 | 168 | 0.550 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 288,591 | 2.886 | 20 | 20 | fits | 141,848 | 95 | 0.565 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 500,244 | 5.002 | 20 | 20 | fits | 82,622 | 36 | 0.473 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 577,614 | 5.776 | 20 | 20 | fits | 146,208 | 167 | 0.551 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 142,194 | 1.422 | 20 | 200 | fits | 143,601 | 223 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 627,361 | 6.274 | 20 | 200 | fits | 146,208 | 167 | 0.551 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 143,106 | 1.431 | 20 | 20 | fits | 143,601 | 223 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 775,891 | 7.759 | 20 | 20 | fits | 147,834 | 119 | 0.487 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 146,691 | 1.467 | 20 | 24 | fits | 143,601 | 223 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 779,326 | 7.793 | 20 | 24 | fits | 147,834 | 119 | 0.487 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 145,651 | 1.457 | 20 | 50 | fits | 143,601 | 223 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 631,037 | 6.310 | 20 | 50 | fits | 146,208 | 167 | 0.551 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 286,788 | 2.868 | 20 | 20 | fits | 141,592 | 94 | 0.563 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 482,749 | 4.827 | 20 | 20 | fits | 82,142 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 637,022 | 6.370 | 20 | 20 | fits | 150,192 | 173 | 0.566 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 158,009 | 1.580 | 20 | 200 | fits | 157,692 | 232 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 663,981 | 6.640 | 20 | 200 | fits | 150,192 | 173 | 0.566 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 158,921 | 1.589 | 20 | 20 | fits | 157,692 | 232 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 801,611 | 8.016 | 20 | 20 | fits | 136,934 | 111 | 0.507 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 162,506 | 1.625 | 20 | 24 | fits | 157,692 | 232 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 805,046 | 8.050 | 20 | 24 | fits | 136,934 | 111 | 0.507 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 161,466 | 1.615 | 20 | 50 | fits | 157,692 | 232 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 667,657 | 6.677 | 20 | 50 | fits | 150,192 | 173 | 0.566 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 302,982 | 3.030 | 20 | 20 | fits | 141,971 | 94 | 0.570 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 506,121 | 5.061 | 20 | 20 | fits | 89,155 | 43 | 0.539 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 257,123 | 2.571 | 20 | 20 | fits | 152,295 | 206 | 0.553 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 145,596 | 1.456 | 20 | 200 | fits | 143,555 | 223 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 297,282 | 2.973 | 20 | 200 | fits | 152,295 | 206 | 0.553 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 146,508 | 1.465 | 20 | 20 | fits | 143,555 | 223 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 787,780 | 7.878 | 20 | 20 | fits | 146,343 | 111 | 0.533 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 150,093 | 1.501 | 20 | 24 | fits | 143,555 | 223 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 815,724 | 8.157 | 20 | 24 | fits | 24,509 | 18 | 0.654 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 149,053 | 1.491 | 20 | 50 | fits | 143,555 | 223 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 300,958 | 3.010 | 20 | 50 | fits | 152,295 | 206 | 0.553 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 445,948 | 4.459 | 20 | 20 | fits | 136,754 | 58 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 642,337 | 6.423 | 20 | 20 | fits | 82,142 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 649,570 | 6.496 | 20 | 20 | fits | 145,820 | 169 | 0.546 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 212,807 | 2.128 | 20 | 200 | fits | 143,823 | 223 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 698,031 | 6.980 | 20 | 200 | fits | 145,820 | 169 | 0.546 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 213,719 | 2.137 | 20 | 20 | fits | 143,823 | 223 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 861,103 | 8.611 | 20 | 20 | fits | 153,262 | 125 | 0.513 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 217,304 | 2.173 | 20 | 24 | fits | 143,823 | 223 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 864,538 | 8.645 | 20 | 24 | fits | 153,262 | 125 | 0.513 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 216,264 | 2.163 | 20 | 50 | fits | 143,823 | 223 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 701,707 | 7.017 | 20 | 50 | fits | 145,820 | 169 | 0.546 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 357,840 | 3.578 | 20 | 20 | fits | 142,031 | 94 | 0.567 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 553,807 | 5.538 | 20 | 20 | fits | 82,142 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 582,440 | 5.824 | 20 | 20 | fits | 145,922 | 169 | 0.547 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 145,765 | 1.458 | 20 | 200 | fits | 143,686 | 223 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 630,910 | 6.309 | 20 | 200 | fits | 145,922 | 169 | 0.547 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 146,677 | 1.467 | 20 | 20 | fits | 143,686 | 223 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 793,982 | 7.940 | 20 | 20 | fits | 153,262 | 125 | 0.513 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 150,262 | 1.503 | 20 | 24 | fits | 143,686 | 223 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 797,417 | 7.974 | 20 | 24 | fits | 153,262 | 125 | 0.513 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 149,222 | 1.492 | 20 | 50 | fits | 143,686 | 223 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 634,586 | 6.346 | 20 | 50 | fits | 145,922 | 169 | 0.547 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 290,624 | 2.906 | 20 | 20 | fits | 141,857 | 94 | 0.565 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 486,584 | 4.866 | 20 | 20 | fits | 82,142 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 595,122 | 5.951 | 20 | 20 | fits | 150,139 | 174 | 0.566 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 146,634 | 1.466 | 20 | 200 | fits | 143,693 | 223 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 645,349 | 6.453 | 20 | 200 | fits | 150,139 | 174 | 0.566 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 147,546 | 1.475 | 20 | 20 | fits | 143,693 | 223 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 794,381 | 7.944 | 20 | 20 | fits | 148,336 | 118 | 0.487 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 151,131 | 1.511 | 20 | 24 | fits | 143,693 | 223 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 797,816 | 7.978 | 20 | 24 | fits | 148,336 | 118 | 0.487 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 150,091 | 1.501 | 20 | 50 | fits | 143,693 | 223 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 649,025 | 6.490 | 20 | 50 | fits | 150,139 | 174 | 0.566 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 291,450 | 2.914 | 20 | 20 | fits | 141,814 | 94 | 0.564 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 487,520 | 4.875 | 20 | 20 | fits | 82,252 | 37 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 600,502 | 6.005 | 20 | 20 | fits | 146,784 | 167 | 0.552 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 147,890 | 1.479 | 20 | 200 | fits | 144,087 | 223 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 650,524 | 6.505 | 20 | 200 | fits | 146,784 | 167 | 0.552 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 148,802 | 1.488 | 20 | 20 | fits | 144,087 | 223 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 797,166 | 7.972 | 20 | 20 | fits | 145,946 | 112 | 0.535 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 152,387 | 1.524 | 20 | 24 | fits | 144,087 | 223 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 825,377 | 8.254 | 20 | 24 | fits | 24,776 | 18 | 0.665 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 151,347 | 1.513 | 20 | 50 | fits | 144,087 | 223 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 654,200 | 6.542 | 20 | 50 | fits | 146,784 | 167 | 0.552 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 292,786 | 2.928 | 20 | 20 | fits | 141,894 | 94 | 0.565 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 505,336 | 5.053 | 20 | 20 | fits | 85,077 | 37 | 0.546 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 266,797 | 2.668 | 20 | 20 | fits | 143,417 | 208 | 0.525 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 162,526 | 1.625 | 20 | 200 | fits | 157,861 | 232 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 305,334 | 3.053 | 20 | 200 | fits | 143,417 | 208 | 0.525 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 163,438 | 1.634 | 20 | 20 | fits | 157,861 | 232 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 800,281 | 8.003 | 20 | 20 | fits | 146,396 | 110 | 0.532 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 167,023 | 1.670 | 20 | 24 | fits | 157,861 | 232 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 803,716 | 8.037 | 20 | 24 | fits | 146,396 | 110 | 0.532 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 165,983 | 1.660 | 20 | 50 | fits | 157,861 | 232 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 309,010 | 3.090 | 20 | 50 | fits | 143,417 | 208 | 0.525 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 451,549 | 4.515 | 20 | 20 | fits | 134,321 | 52 | 0.598 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 654,785 | 6.548 | 20 | 20 | fits | 89,046 | 42 | 0.538 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 256,326 | 2.563 | 20 | 20 | fits | 143,986 | 207 | 0.534 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 143,670 | 1.437 | 20 | 200 | fits | 149,585 | 187 | 0.524 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 295,219 | 2.952 | 20 | 200 | fits | 143,986 | 207 | 0.534 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 144,582 | 1.446 | 20 | 20 | fits | 149,585 | 187 | 0.524 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 449,188 | 4.492 | 20 | 20 | fits | 153,273 | 159 | 0.506 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 148,167 | 1.482 | 20 | 24 | fits | 149,585 | 187 | 0.524 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 452,623 | 4.526 | 20 | 24 | fits | 153,273 | 159 | 0.506 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 147,127 | 1.471 | 20 | 50 | fits | 149,585 | 187 | 0.524 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 298,895 | 2.989 | 20 | 50 | fits | 143,986 | 207 | 0.534 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 591,260 | 5.913 | 20 | 20 | fits | 139,157 | 58 | 0.606 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 787,640 | 7.876 | 20 | 20 | fits | 82,142 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 602,534 | 6.025 | 20 | 20 | fits | 150,300 | 168 | 0.543 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 145,918 | 1.459 | 20 | 200 | fits | 144,159 | 223 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 642,553 | 6.426 | 20 | 200 | fits | 150,300 | 168 | 0.543 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 146,830 | 1.468 | 20 | 20 | fits | 144,159 | 223 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 787,307 | 7.873 | 20 | 20 | fits | 144,058 | 114 | 0.512 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 150,415 | 1.504 | 20 | 24 | fits | 144,159 | 223 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 790,742 | 7.907 | 20 | 24 | fits | 144,058 | 114 | 0.512 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 149,375 | 1.494 | 20 | 50 | fits | 144,159 | 223 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 646,229 | 6.462 | 20 | 50 | fits | 150,300 | 168 | 0.543 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 290,673 | 2.907 | 20 | 20 | fits | 141,753 | 94 | 0.565 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 493,849 | 4.938 | 20 | 20 | fits | 82,534 | 36 | 0.469 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 258,147 | 2.581 | 20 | 20 | fits | 152,524 | 205 | 0.554 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 146,400 | 1.464 | 20 | 200 | fits | 143,779 | 223 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 298,315 | 2.983 | 20 | 200 | fits | 152,524 | 205 | 0.554 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 147,312 | 1.473 | 20 | 20 | fits | 143,779 | 223 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 790,930 | 7.909 | 20 | 20 | fits | 150,616 | 118 | 0.552 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 150,897 | 1.509 | 20 | 24 | fits | 143,779 | 223 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 819,283 | 8.193 | 20 | 24 | fits | 24,918 | 18 | 0.671 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 149,857 | 1.499 | 20 | 50 | fits | 143,779 | 223 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 301,991 | 3.020 | 20 | 50 | fits | 152,524 | 205 | 0.554 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 435,748 | 4.357 | 20 | 20 | fits | 133,822 | 52 | 0.590 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 631,915 | 6.319 | 20 | 20 | fits | 82,210 | 37 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 263,784 | 2.638 | 20 | 20 | fits | 152,529 | 214 | 0.523 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 138,408 | 1.384 | 20 | 200 | fits | 145,591 | 221 | 0.524 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 290,328 | 2.903 | 20 | 200 | fits | 152,529 | 214 | 0.523 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 139,320 | 1.393 | 20 | 20 | fits | 145,591 | 221 | 0.524 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 785,435 | 7.854 | 20 | 20 | fits | 150,731 | 118 | 0.504 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 142,905 | 1.429 | 20 | 24 | fits | 145,591 | 221 | 0.524 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 788,870 | 7.889 | 20 | 24 | fits | 150,731 | 118 | 0.504 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 141,865 | 1.419 | 20 | 50 | fits | 145,591 | 221 | 0.524 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 294,004 | 2.940 | 20 | 50 | fits | 152,529 | 214 | 0.523 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 439,512 | 4.395 | 20 | 20 | fits | 136,673 | 58 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 635,604 | 6.356 | 20 | 20 | fits | 82,078 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 253,538 | 2.535 | 20 | 20 | fits | 147,493 | 193 | 0.537 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 146,978 | 1.470 | 20 | 200 | fits | 150,361 | 243 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 302,632 | 3.026 | 20 | 200 | fits | 147,493 | 193 | 0.537 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 147,890 | 1.479 | 20 | 20 | fits | 150,361 | 243 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 786,777 | 7.868 | 20 | 20 | fits | 151,436 | 119 | 0.504 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 151,475 | 1.515 | 20 | 24 | fits | 150,361 | 243 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 790,212 | 7.902 | 20 | 24 | fits | 151,436 | 119 | 0.504 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 150,435 | 1.504 | 20 | 50 | fits | 150,361 | 243 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 306,308 | 3.063 | 20 | 50 | fits | 147,493 | 193 | 0.537 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 440,214 | 4.402 | 20 | 20 | fits | 133,971 | 52 | 0.596 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 636,241 | 6.362 | 20 | 20 | fits | 82,078 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 566,450 | 5.665 | 20 | 20 | fits | 144,912 | 165 | 0.552 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 155,394 | 1.554 | 20 | 200 | fits | 146,320 | 225 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 639,012 | 6.390 | 20 | 200 | fits | 144,912 | 165 | 0.552 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 156,306 | 1.563 | 20 | 20 | fits | 146,320 | 225 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 787,399 | 7.874 | 20 | 20 | fits | 147,691 | 118 | 0.483 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 159,891 | 1.599 | 20 | 24 | fits | 146,320 | 225 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 790,834 | 7.908 | 20 | 24 | fits | 147,691 | 118 | 0.483 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 158,851 | 1.589 | 20 | 50 | fits | 146,320 | 225 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 642,688 | 6.427 | 20 | 50 | fits | 144,912 | 165 | 0.552 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 299,855 | 2.999 | 20 | 20 | fits | 141,459 | 94 | 0.562 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 495,696 | 4.957 | 20 | 20 | fits | 82,078 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 558,792 | 5.588 | 20 | 20 | fits | 145,074 | 165 | 0.554 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 147,643 | 1.476 | 20 | 200 | fits | 145,710 | 224 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 631,397 | 6.314 | 20 | 200 | fits | 145,074 | 165 | 0.554 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 148,555 | 1.486 | 20 | 20 | fits | 145,710 | 224 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 778,044 | 7.780 | 20 | 20 | fits | 145,951 | 114 | 0.534 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 152,140 | 1.521 | 20 | 24 | fits | 145,710 | 224 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 895,625 | 8.956 | 20 | 24 | fits | 29,459 | 25 | 0.721 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 151,100 | 1.511 | 20 | 50 | fits | 145,710 | 224 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 635,073 | 6.351 | 20 | 50 | fits | 145,074 | 165 | 0.554 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 292,046 | 2.920 | 20 | 20 | fits | 141,401 | 94 | 0.561 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 487,919 | 4.879 | 20 | 20 | fits | 82,078 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 261,571 | 2.616 | 20 | 20 | fits | 147,187 | 196 | 0.521 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 140,683 | 1.407 | 20 | 200 | fits | 148,660 | 201 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 287,261 | 2.873 | 20 | 200 | fits | 147,187 | 196 | 0.521 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 141,595 | 1.416 | 20 | 20 | fits | 148,660 | 201 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 871,548 | 8.715 | 20 | 20 | fits | 146,978 | 113 | 0.534 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 145,180 | 1.452 | 20 | 24 | fits | 148,660 | 201 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 874,983 | 8.750 | 20 | 24 | fits | 146,978 | 113 | 0.534 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 144,140 | 1.441 | 20 | 50 | fits | 148,660 | 201 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 290,937 | 2.909 | 20 | 50 | fits | 147,187 | 196 | 0.521 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 432,887 | 4.329 | 20 | 20 | fits | 142,015 | 94 | 0.570 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 648,676 | 6.487 | 20 | 20 | fits | 92,429 | 49 | 0.576 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 239,403 | 2.394 | 20 | 20 | fits | 151,521 | 210 | 0.531 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 139,271 | 1.393 | 20 | 200 | fits | 145,649 | 224 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 290,183 | 2.902 | 20 | 200 | fits | 151,521 | 210 | 0.531 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 140,183 | 1.402 | 20 | 20 | fits | 145,649 | 224 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 871,580 | 8.716 | 20 | 20 | fits | 151,269 | 118 | 0.508 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 143,768 | 1.438 | 20 | 24 | fits | 145,649 | 224 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 875,015 | 8.750 | 20 | 24 | fits | 151,269 | 118 | 0.508 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 142,728 | 1.427 | 20 | 50 | fits | 145,649 | 224 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 293,859 | 2.939 | 20 | 50 | fits | 151,521 | 210 | 0.531 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 427,778 | 4.278 | 20 | 20 | fits | 133,984 | 53 | 0.596 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 721,211 | 7.212 | 20 | 20 | fits | 82,707 | 37 | 0.485 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 252,109 | 2.521 | 20 | 20 | fits | 156,894 | 216 | 0.515 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 136,346 | 1.363 | 20 | 200 | fits | 142,616 | 220 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 292,631 | 2.926 | 20 | 200 | fits | 156,894 | 216 | 0.515 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 137,258 | 1.373 | 20 | 20 | fits | 142,616 | 220 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 862,975 | 8.630 | 20 | 20 | fits | 145,365 | 111 | 0.528 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 140,843 | 1.408 | 20 | 24 | fits | 142,616 | 220 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 866,410 | 8.664 | 20 | 24 | fits | 145,365 | 111 | 0.528 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 139,803 | 1.398 | 20 | 50 | fits | 142,616 | 220 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 296,307 | 2.963 | 20 | 50 | fits | 156,894 | 216 | 0.515 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 445,332 | 4.453 | 20 | 20 | fits | 141,032 | 64 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 718,510 | 7.185 | 20 | 20 | fits | 82,136 | 36 | 0.459 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 265,962 | 2.660 | 20 | 20 | fits | 152,223 | 207 | 0.551 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 152,898 | 1.529 | 20 | 200 | fits | 156,078 | 229 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 304,512 | 3.045 | 20 | 200 | fits | 152,223 | 207 | 0.551 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 153,810 | 1.538 | 20 | 20 | fits | 156,078 | 229 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 871,102 | 8.711 | 20 | 20 | fits | 146,226 | 110 | 0.532 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 157,395 | 1.574 | 20 | 24 | fits | 156,078 | 229 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 874,537 | 8.745 | 20 | 24 | fits | 146,226 | 110 | 0.532 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 156,355 | 1.564 | 20 | 50 | fits | 156,078 | 229 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 308,188 | 3.082 | 20 | 50 | fits | 152,223 | 207 | 0.551 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 529,474 | 5.295 | 20 | 20 | fits | 137,095 | 58 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 725,776 | 7.258 | 20 | 20 | fits | 82,078 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 265,190 | 2.652 | 20 | 20 | fits | 146,391 | 210 | 0.517 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 138,198 | 1.382 | 20 | 200 | fits | 146,198 | 180 | 0.530 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 283,980 | 2.840 | 20 | 200 | fits | 146,391 | 210 | 0.517 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 139,110 | 1.391 | 20 | 20 | fits | 146,198 | 180 | 0.530 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 781,629 | 7.816 | 20 | 20 | fits | 141,696 | 106 | 0.556 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 142,695 | 1.427 | 20 | 24 | fits | 146,198 | 180 | 0.530 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 809,679 | 8.097 | 20 | 24 | fits | 24,615 | 18 | 0.658 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 141,655 | 1.417 | 20 | 50 | fits | 146,198 | 180 | 0.530 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 287,656 | 2.877 | 20 | 50 | fits | 146,391 | 210 | 0.517 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 429,674 | 4.297 | 20 | 20 | fits | 142,083 | 94 | 0.566 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 640,833 | 6.408 | 20 | 20 | fits | 87,672 | 43 | 0.569 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 210,063 | 2.101 | 20 | 20 | fits | 151,500 | 211 | 0.528 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 139,064 | 1.391 | 20 | 200 | fits | 145,377 | 224 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 289,955 | 2.900 | 20 | 200 | fits | 151,500 | 211 | 0.528 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 139,976 | 1.400 | 20 | 20 | fits | 145,377 | 224 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 789,654 | 7.897 | 20 | 20 | fits | 150,899 | 118 | 0.506 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 143,561 | 1.436 | 20 | 24 | fits | 145,377 | 224 | 0.501 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 793,089 | 7.931 | 20 | 24 | fits | 150,899 | 118 | 0.506 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 142,521 | 1.425 | 20 | 50 | fits | 145,377 | 224 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 293,631 | 2.936 | 20 | 50 | fits | 151,500 | 211 | 0.528 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 427,901 | 4.279 | 20 | 20 | fits | 134,335 | 53 | 0.597 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 639,655 | 6.397 | 20 | 20 | fits | 82,718 | 36 | 0.479 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 561,551 | 5.616 | 20 | 20 | fits | 146,237 | 164 | 0.564 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 140,754 | 1.408 | 20 | 200 | fits | 145,380 | 224 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 641,509 | 6.415 | 20 | 200 | fits | 146,237 | 164 | 0.564 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 141,666 | 1.417 | 20 | 20 | fits | 145,380 | 224 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 790,214 | 7.902 | 20 | 20 | fits | 148,009 | 118 | 0.486 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 145,251 | 1.453 | 20 | 24 | fits | 145,380 | 224 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 793,649 | 7.936 | 20 | 24 | fits | 148,009 | 118 | 0.486 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 144,211 | 1.442 | 20 | 50 | fits | 145,380 | 224 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 645,185 | 6.452 | 20 | 50 | fits | 146,237 | 164 | 0.564 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 285,517 | 2.855 | 20 | 20 | fits | 141,761 | 95 | 0.562 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 496,868 | 4.969 | 20 | 20 | fits | 82,558 | 36 | 0.473 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 274,241 | 2.742 | 20 | 20 | fits | 157,312 | 215 | 0.524 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 149,102 | 1.491 | 20 | 200 | fits | 152,041 | 228 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 314,646 | 3.146 | 20 | 200 | fits | 157,312 | 215 | 0.524 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 150,014 | 1.500 | 20 | 20 | fits | 152,041 | 228 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 865,573 | 8.656 | 20 | 20 | fits | 142,983 | 112 | 0.546 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 153,599 | 1.536 | 20 | 24 | fits | 152,041 | 228 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 869,008 | 8.690 | 20 | 24 | fits | 142,983 | 112 | 0.546 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 152,559 | 1.526 | 20 | 50 | fits | 152,041 | 228 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 318,322 | 3.183 | 20 | 50 | fits | 157,312 | 215 | 0.524 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 451,931 | 4.519 | 20 | 20 | fits | 133,674 | 52 | 0.590 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 662,754 | 6.628 | 20 | 20 | fits | 96,828 | 42 | 0.564 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 604,632 | 6.046 | 20 | 20 | fits | 157,414 | 164 | 0.590 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 149,897 | 1.499 | 20 | 200 | fits | 151,677 | 227 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 646,479 | 6.465 | 20 | 200 | fits | 157,414 | 164 | 0.590 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 150,809 | 1.508 | 20 | 20 | fits | 151,677 | 227 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 864,201 | 8.642 | 20 | 20 | fits | 154,903 | 119 | 0.527 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 154,394 | 1.544 | 20 | 24 | fits | 151,677 | 227 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 867,636 | 8.676 | 20 | 24 | fits | 154,903 | 119 | 0.527 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 153,354 | 1.534 | 20 | 50 | fits | 151,677 | 227 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 650,155 | 6.502 | 20 | 50 | fits | 157,414 | 164 | 0.590 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 294,744 | 2.947 | 20 | 20 | fits | 141,845 | 94 | 0.568 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 490,661 | 4.907 | 20 | 20 | fits | 82,078 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 692,297 | 6.923 | 20 | 20 | fits | 150,750 | 168 | 0.570 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 155,608 | 1.556 | 20 | 200 | fits | 155,575 | 229 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 720,856 | 7.209 | 20 | 200 | fits | 150,750 | 168 | 0.570 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 156,520 | 1.565 | 20 | 20 | fits | 155,575 | 229 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 872,014 | 8.720 | 20 | 20 | fits | 141,233 | 118 | 0.528 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 160,105 | 1.601 | 20 | 24 | fits | 155,575 | 229 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 875,449 | 8.754 | 20 | 24 | fits | 141,233 | 118 | 0.528 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 159,065 | 1.591 | 20 | 50 | fits | 155,575 | 229 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 724,532 | 7.245 | 20 | 50 | fits | 150,750 | 168 | 0.570 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 300,360 | 3.004 | 20 | 20 | fits | 141,750 | 94 | 0.567 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 510,903 | 5.109 | 20 | 20 | fits | 96,611 | 42 | 0.561 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 688,141 | 6.881 | 20 | 20 | fits | 145,197 | 149 | 0.557 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 151,514 | 1.515 | 20 | 200 | fits | 149,898 | 242 | 0.498 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 728,617 | 7.286 | 20 | 200 | fits | 145,197 | 149 | 0.557 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 152,426 | 1.524 | 20 | 20 | fits | 149,898 | 242 | 0.498 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 872,724 | 8.727 | 20 | 20 | fits | 143,411 | 113 | 0.509 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 156,011 | 1.560 | 20 | 24 | fits | 149,898 | 242 | 0.498 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 876,159 | 8.762 | 20 | 24 | fits | 143,411 | 113 | 0.509 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 154,971 | 1.550 | 20 | 50 | fits | 149,898 | 242 | 0.498 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 732,293 | 7.323 | 20 | 50 | fits | 145,197 | 149 | 0.557 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 296,302 | 2.963 | 20 | 20 | fits | 141,786 | 94 | 0.565 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 575,581 | 5.756 | 20 | 20 | fits | 90,011 | 44 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 264,077 | 2.641 | 20 | 20 | fits | 145,962 | 210 | 0.517 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 137,472 | 1.375 | 20 | 200 | fits | 145,766 | 180 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 282,825 | 2.828 | 20 | 200 | fits | 145,962 | 210 | 0.517 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 138,384 | 1.384 | 20 | 20 | fits | 145,766 | 180 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 437,659 | 4.377 | 20 | 20 | fits | 154,138 | 143 | 0.579 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 141,969 | 1.420 | 20 | 24 | fits | 145,766 | 180 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 886,187 | 8.862 | 20 | 24 | fits | 40,802 | 30 | 0.604 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 140,929 | 1.409 | 20 | 50 | fits | 145,766 | 180 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 286,501 | 2.865 | 20 | 50 | fits | 145,962 | 210 | 0.517 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 646,365 | 6.464 | 20 | 20 | fits | 136,632 | 58 | 0.609 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 842,850 | 8.428 | 20 | 20 | fits | 82,078 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 269,818 | 2.698 | 20 | 20 | fits | 157,346 | 215 | 0.520 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 145,245 | 1.452 | 20 | 200 | fits | 142,705 | 221 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 310,446 | 3.104 | 20 | 200 | fits | 157,346 | 215 | 0.520 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 146,157 | 1.462 | 20 | 20 | fits | 142,705 | 221 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 788,815 | 7.888 | 20 | 20 | fits | 145,624 | 111 | 0.526 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 149,742 | 1.497 | 20 | 24 | fits | 142,705 | 221 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 792,250 | 7.923 | 20 | 24 | fits | 145,624 | 111 | 0.526 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 148,702 | 1.487 | 20 | 50 | fits | 142,705 | 221 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 314,122 | 3.141 | 20 | 50 | fits | 157,346 | 215 | 0.520 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 447,912 | 4.479 | 20 | 20 | fits | 133,855 | 52 | 0.592 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 644,091 | 6.441 | 20 | 20 | fits | 82,142 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 260,517 | 2.605 | 20 | 20 | fits | 152,089 | 213 | 0.521 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 135,607 | 1.356 | 20 | 200 | fits | 142,486 | 220 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 287,087 | 2.871 | 20 | 200 | fits | 152,089 | 213 | 0.521 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 136,519 | 1.365 | 20 | 20 | fits | 142,486 | 220 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 770,853 | 7.709 | 20 | 20 | fits | 151,004 | 119 | 0.503 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 140,104 | 1.401 | 20 | 24 | fits | 142,486 | 220 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 774,288 | 7.743 | 20 | 24 | fits | 151,004 | 119 | 0.503 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 139,064 | 1.391 | 20 | 50 | fits | 142,486 | 220 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 290,763 | 2.908 | 20 | 50 | fits | 152,089 | 213 | 0.521 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 424,570 | 4.246 | 20 | 20 | fits | 133,872 | 52 | 0.595 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 620,749 | 6.207 | 20 | 20 | fits | 82,142 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 252,366 | 2.524 | 20 | 20 | fits | 156,868 | 215 | 0.515 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 136,627 | 1.366 | 20 | 200 | fits | 142,905 | 220 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 292,886 | 2.929 | 20 | 200 | fits | 156,868 | 215 | 0.515 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 137,539 | 1.375 | 20 | 20 | fits | 142,905 | 220 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 785,276 | 7.853 | 20 | 20 | fits | 150,292 | 118 | 0.549 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 141,124 | 1.411 | 20 | 24 | fits | 142,905 | 220 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 788,711 | 7.887 | 20 | 24 | fits | 150,292 | 118 | 0.549 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 140,084 | 1.401 | 20 | 50 | fits | 142,905 | 220 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 296,562 | 2.966 | 20 | 50 | fits | 156,868 | 215 | 0.515 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 430,352 | 4.304 | 20 | 20 | fits | 133,855 | 52 | 0.592 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 626,641 | 6.266 | 20 | 20 | fits | 82,252 | 37 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 625,250 | 6.253 | 20 | 20 | fits | 150,088 | 173 | 0.566 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 153,213 | 1.532 | 20 | 200 | fits | 156,718 | 229 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 651,971 | 6.520 | 20 | 200 | fits | 150,088 | 173 | 0.566 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 154,125 | 1.541 | 20 | 20 | fits | 156,718 | 229 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 800,276 | 8.003 | 20 | 20 | fits | 147,609 | 112 | 0.541 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 157,710 | 1.577 | 20 | 24 | fits | 156,718 | 229 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 803,711 | 8.037 | 20 | 24 | fits | 147,609 | 112 | 0.541 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 156,670 | 1.567 | 20 | 50 | fits | 156,718 | 229 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 655,647 | 6.556 | 20 | 50 | fits | 150,088 | 173 | 0.566 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 297,915 | 2.979 | 20 | 20 | fits | 141,700 | 94 | 0.566 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 494,215 | 4.942 | 20 | 20 | fits | 82,252 | 37 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 618,727 | 6.187 | 20 | 20 | fits | 147,605 | 165 | 0.579 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 141,059 | 1.411 | 20 | 200 | fits | 142,877 | 220 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 643,564 | 6.436 | 20 | 200 | fits | 147,605 | 165 | 0.579 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 141,971 | 1.420 | 20 | 20 | fits | 142,877 | 220 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 868,571 | 8.686 | 20 | 20 | fits | 144,287 | 113 | 0.514 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 145,556 | 1.456 | 20 | 24 | fits | 142,877 | 220 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 896,688 | 8.967 | 20 | 24 | fits | 24,682 | 18 | 0.660 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 144,516 | 1.445 | 20 | 50 | fits | 142,877 | 220 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 647,240 | 6.472 | 20 | 50 | fits | 147,605 | 165 | 0.579 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 285,975 | 2.860 | 20 | 20 | fits | 141,914 | 94 | 0.567 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 497,555 | 4.976 | 20 | 20 | fits | 88,053 | 43 | 0.572 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 681,382 | 6.814 | 20 | 20 | fits | 146,909 | 169 | 0.552 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 142,309 | 1.423 | 20 | 200 | fits | 142,440 | 220 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 730,065 | 7.301 | 20 | 200 | fits | 146,909 | 169 | 0.552 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 143,221 | 1.432 | 20 | 20 | fits | 142,440 | 220 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 879,072 | 8.791 | 20 | 20 | fits | 148,311 | 118 | 0.487 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 146,806 | 1.468 | 20 | 24 | fits | 142,440 | 220 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 882,507 | 8.825 | 20 | 24 | fits | 148,311 | 118 | 0.487 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 145,766 | 1.458 | 20 | 50 | fits | 142,440 | 220 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 733,741 | 7.337 | 20 | 50 | fits | 146,909 | 169 | 0.552 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 287,031 | 2.870 | 20 | 20 | fits | 141,720 | 95 | 0.563 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 504,851 | 5.049 | 20 | 20 | fits | 88,536 | 42 | 0.527 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 278,249 | 2.782 | 20 | 20 | fits | 152,978 | 213 | 0.528 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 144,194 | 1.442 | 20 | 200 | fits | 142,638 | 221 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 304,897 | 3.049 | 20 | 200 | fits | 152,978 | 213 | 0.528 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 145,106 | 1.451 | 20 | 20 | fits | 142,638 | 221 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 874,591 | 8.746 | 20 | 20 | fits | 150,569 | 118 | 0.504 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 148,691 | 1.487 | 20 | 24 | fits | 142,638 | 221 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 878,026 | 8.780 | 20 | 24 | fits | 150,569 | 118 | 0.504 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 147,651 | 1.477 | 20 | 50 | fits | 142,638 | 221 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 308,573 | 3.086 | 20 | 50 | fits | 152,978 | 213 | 0.528 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 448,337 | 4.483 | 20 | 20 | fits | 139,829 | 58 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 724,922 | 7.249 | 20 | 20 | fits | 82,206 | 36 | 0.459 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 261,744 | 2.617 | 20 | 20 | fits | 146,269 | 210 | 0.518 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 134,887 | 1.349 | 20 | 200 | fits | 142,982 | 179 | 0.530 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 280,547 | 2.805 | 20 | 200 | fits | 146,269 | 210 | 0.518 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 135,799 | 1.358 | 20 | 20 | fits | 142,982 | 179 | 0.530 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 423,442 | 4.234 | 20 | 20 | fits | 142,199 | 143 | 0.556 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 139,384 | 1.394 | 20 | 24 | fits | 142,982 | 179 | 0.530 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 892,272 | 8.923 | 20 | 24 | fits | 44,138 | 37 | 0.638 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 138,344 | 1.383 | 20 | 50 | fits | 142,982 | 179 | 0.530 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 284,223 | 2.842 | 20 | 50 | fits | 146,269 | 210 | 0.518 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 639,822 | 6.398 | 20 | 20 | fits | 133,450 | 52 | 0.591 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 836,153 | 8.362 | 20 | 20 | fits | 82,252 | 37 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 592,630 | 5.926 | 20 | 20 | fits | 146,922 | 167 | 0.555 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 140,843 | 1.408 | 20 | 200 | fits | 142,527 | 220 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 642,406 | 6.424 | 20 | 200 | fits | 146,922 | 167 | 0.555 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 141,755 | 1.418 | 20 | 20 | fits | 142,527 | 220 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 791,311 | 7.913 | 20 | 20 | fits | 148,209 | 118 | 0.487 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 145,340 | 1.453 | 20 | 24 | fits | 142,527 | 220 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 794,746 | 7.947 | 20 | 24 | fits | 148,209 | 118 | 0.487 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 144,300 | 1.443 | 20 | 50 | fits | 142,527 | 220 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 646,082 | 6.461 | 20 | 50 | fits | 146,922 | 167 | 0.555 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 285,470 | 2.855 | 20 | 20 | fits | 141,625 | 95 | 0.563 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 497,080 | 4.971 | 20 | 20 | fits | 82,564 | 36 | 0.471 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 267,391 | 2.674 | 20 | 20 | fits | 156,990 | 215 | 0.520 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 143,024 | 1.430 | 20 | 200 | fits | 143,021 | 221 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 307,791 | 3.078 | 20 | 200 | fits | 156,990 | 215 | 0.520 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 143,936 | 1.439 | 20 | 20 | fits | 143,021 | 221 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 785,653 | 7.857 | 20 | 20 | fits | 145,172 | 111 | 0.526 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 147,521 | 1.475 | 20 | 24 | fits | 143,021 | 221 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 789,088 | 7.891 | 20 | 24 | fits | 145,172 | 111 | 0.526 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 146,481 | 1.465 | 20 | 50 | fits | 143,021 | 221 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 311,467 | 3.115 | 20 | 50 | fits | 156,990 | 215 | 0.520 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 445,202 | 4.452 | 20 | 20 | fits | 133,800 | 52 | 0.594 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 641,381 | 6.414 | 20 | 20 | fits | 82,142 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 251,254 | 2.513 | 20 | 20 | fits | 156,587 | 215 | 0.514 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 135,638 | 1.356 | 20 | 200 | fits | 143,686 | 221 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 291,616 | 2.916 | 20 | 200 | fits | 156,587 | 215 | 0.514 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 136,550 | 1.365 | 20 | 20 | fits | 143,686 | 221 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 772,414 | 7.724 | 20 | 20 | fits | 145,342 | 111 | 0.526 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 140,135 | 1.401 | 20 | 24 | fits | 143,686 | 221 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 775,849 | 7.758 | 20 | 24 | fits | 145,342 | 111 | 0.526 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 139,095 | 1.391 | 20 | 50 | fits | 143,686 | 221 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 295,292 | 2.953 | 20 | 50 | fits | 156,587 | 215 | 0.514 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 431,903 | 4.319 | 20 | 20 | fits | 136,676 | 58 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 627,972 | 6.280 | 20 | 20 | fits | 82,142 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 618,537 | 6.185 | 20 | 20 | fits | 146,167 | 166 | 0.552 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 159,279 | 1.593 | 20 | 200 | fits | 156,430 | 229 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 644,839 | 6.448 | 20 | 200 | fits | 146,167 | 166 | 0.552 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 160,191 | 1.602 | 20 | 20 | fits | 156,430 | 229 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 792,690 | 7.927 | 20 | 20 | fits | 147,155 | 113 | 0.541 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 163,776 | 1.638 | 20 | 24 | fits | 156,430 | 229 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 796,125 | 7.961 | 20 | 24 | fits | 147,155 | 113 | 0.541 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 162,736 | 1.627 | 20 | 50 | fits | 156,430 | 229 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 648,515 | 6.485 | 20 | 50 | fits | 146,167 | 166 | 0.552 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 304,078 | 3.041 | 20 | 20 | fits | 141,797 | 94 | 0.568 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 500,268 | 5.003 | 20 | 20 | fits | 82,142 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 252,488 | 2.525 | 20 | 20 | fits | 152,170 | 215 | 0.521 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 149,449 | 1.494 | 20 | 200 | fits | 156,430 | 229 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 301,010 | 3.010 | 20 | 200 | fits | 152,170 | 215 | 0.521 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 150,361 | 1.504 | 20 | 20 | fits | 156,430 | 229 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 795,429 | 7.954 | 20 | 20 | fits | 139,256 | 111 | 0.523 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 153,946 | 1.539 | 20 | 24 | fits | 156,430 | 229 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 798,864 | 7.989 | 20 | 24 | fits | 139,256 | 111 | 0.523 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 152,906 | 1.529 | 20 | 50 | fits | 156,430 | 229 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 304,686 | 3.047 | 20 | 50 | fits | 152,170 | 215 | 0.521 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 438,474 | 4.385 | 20 | 20 | fits | 133,853 | 52 | 0.594 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 657,073 | 6.571 | 20 | 20 | fits | 87,961 | 43 | 0.567 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 238,263 | 2.383 | 20 | 20 | fits | 152,599 | 214 | 0.526 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 136,311 | 1.363 | 20 | 200 | fits | 142,589 | 220 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 288,301 | 2.883 | 20 | 200 | fits | 152,599 | 214 | 0.526 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 137,223 | 1.372 | 20 | 20 | fits | 142,589 | 220 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 793,897 | 7.939 | 20 | 20 | fits | 152,148 | 119 | 0.510 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 140,808 | 1.408 | 20 | 24 | fits | 142,589 | 220 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 797,332 | 7.973 | 20 | 24 | fits | 152,148 | 119 | 0.510 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 139,768 | 1.398 | 20 | 50 | fits | 142,589 | 220 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 291,977 | 2.920 | 20 | 50 | fits | 152,599 | 214 | 0.526 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 425,892 | 4.259 | 20 | 20 | fits | 133,980 | 53 | 0.595 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 642,649 | 6.426 | 20 | 20 | fits | 82,808 | 36 | 0.481 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 575,507 | 5.755 | 20 | 20 | fits | 145,646 | 165 | 0.558 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 142,272 | 1.423 | 20 | 200 | fits | 145,879 | 224 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 648,195 | 6.482 | 20 | 200 | fits | 145,646 | 165 | 0.558 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 143,184 | 1.432 | 20 | 20 | fits | 145,879 | 224 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 796,841 | 7.968 | 20 | 20 | fits | 147,950 | 118 | 0.484 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 146,769 | 1.468 | 20 | 24 | fits | 145,879 | 224 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 800,276 | 8.003 | 20 | 24 | fits | 147,950 | 118 | 0.484 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 145,729 | 1.457 | 20 | 50 | fits | 145,879 | 224 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 651,871 | 6.519 | 20 | 50 | fits | 145,646 | 165 | 0.558 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 286,816 | 2.868 | 20 | 20 | fits | 141,542 | 94 | 0.562 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 504,145 | 5.041 | 20 | 20 | fits | 85,134 | 37 | 0.547 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 253,779 | 2.538 | 20 | 20 | fits | 150,886 | 202 | 0.558 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 144,026 | 1.440 | 20 | 200 | fits | 145,946 | 224 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 294,303 | 2.943 | 20 | 200 | fits | 150,886 | 202 | 0.558 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 144,938 | 1.449 | 20 | 20 | fits | 145,946 | 224 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 784,891 | 7.849 | 20 | 20 | fits | 146,354 | 111 | 0.532 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 148,523 | 1.485 | 20 | 24 | fits | 145,946 | 224 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 812,835 | 8.128 | 20 | 24 | fits | 24,509 | 18 | 0.654 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 147,483 | 1.475 | 20 | 50 | fits | 145,946 | 224 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 297,979 | 2.980 | 20 | 50 | fits | 150,886 | 202 | 0.558 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 442,983 | 4.430 | 20 | 20 | fits | 136,846 | 58 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 639,437 | 6.394 | 20 | 20 | fits | 82,142 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 574,952 | 5.750 | 20 | 20 | fits | 146,406 | 167 | 0.552 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 139,187 | 1.392 | 20 | 200 | fits | 142,511 | 220 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 624,728 | 6.247 | 20 | 200 | fits | 146,406 | 167 | 0.552 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 140,099 | 1.401 | 20 | 20 | fits | 142,511 | 220 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 773,794 | 7.738 | 20 | 20 | fits | 148,370 | 119 | 0.488 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 143,684 | 1.437 | 20 | 24 | fits | 142,511 | 220 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 777,229 | 7.772 | 20 | 24 | fits | 148,370 | 119 | 0.488 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 142,644 | 1.426 | 20 | 50 | fits | 142,511 | 220 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 628,404 | 6.284 | 20 | 50 | fits | 146,406 | 167 | 0.552 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 283,916 | 2.839 | 20 | 20 | fits | 141,727 | 94 | 0.564 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 479,918 | 4.799 | 20 | 20 | fits | 82,142 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 576,862 | 5.769 | 20 | 20 | fits | 146,499 | 168 | 0.550 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 141,229 | 1.412 | 20 | 200 | fits | 142,866 | 220 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 626,798 | 6.268 | 20 | 200 | fits | 146,499 | 168 | 0.550 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 142,141 | 1.421 | 20 | 20 | fits | 142,866 | 220 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 789,252 | 7.893 | 20 | 20 | fits | 152,801 | 124 | 0.511 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 145,726 | 1.457 | 20 | 24 | fits | 142,866 | 220 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 792,687 | 7.927 | 20 | 24 | fits | 152,801 | 124 | 0.511 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 144,686 | 1.447 | 20 | 50 | fits | 142,866 | 220 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 630,474 | 6.305 | 20 | 50 | fits | 146,499 | 168 | 0.550 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 285,893 | 2.859 | 20 | 20 | fits | 141,662 | 94 | 0.563 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 481,895 | 4.819 | 20 | 20 | fits | 82,142 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 632,090 | 6.321 | 20 | 20 | fits | 147,064 | 166 | 0.556 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 156,853 | 1.569 | 20 | 200 | fits | 156,803 | 229 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 658,486 | 6.585 | 20 | 200 | fits | 147,064 | 166 | 0.556 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 157,765 | 1.578 | 20 | 20 | fits | 156,803 | 229 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 795,893 | 7.959 | 20 | 20 | fits | 136,711 | 111 | 0.505 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 161,350 | 1.613 | 20 | 24 | fits | 156,803 | 229 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 799,328 | 7.993 | 20 | 24 | fits | 136,711 | 111 | 0.505 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 160,310 | 1.603 | 20 | 50 | fits | 156,803 | 229 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 662,162 | 6.622 | 20 | 50 | fits | 147,064 | 166 | 0.556 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 301,724 | 3.017 | 20 | 20 | fits | 141,869 | 94 | 0.567 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 513,018 | 5.130 | 20 | 20 | fits | 87,876 | 43 | 0.570 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 610,494 | 6.105 | 20 | 20 | fits | 150,827 | 168 | 0.545 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 144,743 | 1.447 | 20 | 200 | fits | 143,006 | 220 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 650,592 | 6.506 | 20 | 200 | fits | 150,827 | 168 | 0.545 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 145,655 | 1.457 | 20 | 20 | fits | 143,006 | 220 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 792,915 | 7.929 | 20 | 20 | fits | 141,627 | 109 | 0.557 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 149,240 | 1.492 | 20 | 24 | fits | 143,006 | 220 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 899,446 | 8.994 | 20 | 24 | fits | 25,359 | 19 | 0.665 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 148,200 | 1.482 | 20 | 50 | fits | 143,006 | 220 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 654,268 | 6.543 | 20 | 50 | fits | 150,827 | 168 | 0.545 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 289,848 | 2.898 | 20 | 20 | fits | 142,103 | 95 | 0.567 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 501,361 | 5.014 | 20 | 20 | fits | 82,721 | 36 | 0.477 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 265,952 | 2.660 | 20 | 20 | fits | 146,525 | 211 | 0.518 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 138,829 | 1.388 | 20 | 200 | fits | 146,922 | 180 | 0.533 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 284,745 | 2.847 | 20 | 200 | fits | 146,525 | 211 | 0.518 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 139,741 | 1.397 | 20 | 20 | fits | 146,922 | 180 | 0.533 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 442,767 | 4.428 | 20 | 20 | fits | 148,866 | 152 | 0.536 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 143,326 | 1.433 | 20 | 24 | fits | 146,922 | 180 | 0.533 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 888,005 | 8.880 | 20 | 24 | fits | 26,864 | 18 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 142,286 | 1.423 | 20 | 50 | fits | 146,922 | 180 | 0.533 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 288,421 | 2.884 | 20 | 50 | fits | 146,525 | 211 | 0.518 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 584,560 | 5.846 | 20 | 20 | fits | 138,878 | 58 | 0.605 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 858,606 | 8.586 | 20 | 20 | fits | 82,200 | 36 | 0.459 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 220,046 | 2.200 | 20 | 20 | fits | 152,764 | 211 | 0.539 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 139,479 | 1.395 | 20 | 200 | fits | 145,885 | 225 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 300,020 | 3.000 | 20 | 200 | fits | 152,764 | 211 | 0.539 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 140,391 | 1.404 | 20 | 20 | fits | 145,885 | 225 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 871,067 | 8.711 | 20 | 20 | fits | 150,652 | 118 | 0.504 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 143,976 | 1.440 | 20 | 24 | fits | 145,885 | 225 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 874,502 | 8.745 | 20 | 24 | fits | 150,652 | 118 | 0.504 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 142,936 | 1.429 | 20 | 50 | fits | 145,885 | 225 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 303,696 | 3.037 | 20 | 50 | fits | 152,764 | 211 | 0.539 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 440,447 | 4.404 | 20 | 20 | fits | 136,816 | 58 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 721,315 | 7.213 | 20 | 20 | fits | 82,749 | 37 | 0.485 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 210,493 | 2.105 | 20 | 20 | fits | 151,339 | 211 | 0.528 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 139,681 | 1.397 | 20 | 200 | fits | 145,959 | 224 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 290,411 | 2.904 | 20 | 200 | fits | 151,339 | 211 | 0.528 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 140,593 | 1.406 | 20 | 20 | fits | 145,959 | 224 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 858,782 | 8.588 | 20 | 20 | fits | 142,066 | 114 | 0.543 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 144,178 | 1.442 | 20 | 24 | fits | 145,959 | 224 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 886,983 | 8.870 | 20 | 24 | fits | 24,766 | 18 | 0.667 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 143,138 | 1.431 | 20 | 50 | fits | 145,959 | 224 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 294,087 | 2.941 | 20 | 50 | fits | 151,339 | 211 | 0.528 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 433,953 | 4.340 | 20 | 20 | fits | 139,931 | 58 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 708,248 | 7.082 | 20 | 20 | fits | 82,403 | 37 | 0.464 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 252,013 | 2.520 | 20 | 20 | fits | 150,876 | 201 | 0.559 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 142,338 | 1.423 | 20 | 200 | fits | 145,898 | 224 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 292,605 | 2.926 | 20 | 200 | fits | 150,876 | 201 | 0.559 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 143,250 | 1.433 | 20 | 20 | fits | 145,898 | 224 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 864,718 | 8.647 | 20 | 20 | fits | 146,707 | 111 | 0.533 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 146,835 | 1.468 | 20 | 24 | fits | 145,898 | 224 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 892,717 | 8.927 | 20 | 24 | fits | 24,564 | 18 | 0.656 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 145,795 | 1.458 | 20 | 50 | fits | 145,898 | 224 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 296,281 | 2.963 | 20 | 50 | fits | 150,876 | 201 | 0.559 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 507,451 | 5.075 | 20 | 20 | fits | 133,479 | 52 | 0.588 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 718,911 | 7.189 | 20 | 20 | fits | 88,071 | 43 | 0.571 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 270,079 | 2.701 | 20 | 20 | fits | 157,011 | 215 | 0.520 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 145,749 | 1.457 | 20 | 200 | fits | 142,945 | 221 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 310,615 | 3.106 | 20 | 200 | fits | 157,011 | 215 | 0.520 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 146,661 | 1.467 | 20 | 20 | fits | 142,945 | 221 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 788,819 | 7.888 | 20 | 20 | fits | 145,172 | 111 | 0.526 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 150,246 | 1.502 | 20 | 24 | fits | 142,945 | 221 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 792,254 | 7.923 | 20 | 24 | fits | 145,172 | 111 | 0.526 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 149,206 | 1.492 | 20 | 50 | fits | 142,945 | 221 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 314,291 | 3.143 | 20 | 50 | fits | 157,011 | 215 | 0.520 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 448,247 | 4.482 | 20 | 20 | fits | 134,021 | 52 | 0.594 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 644,547 | 6.445 | 20 | 20 | fits | 82,142 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 238,735 | 2.387 | 20 | 20 | fits | 150,995 | 210 | 0.528 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 139,283 | 1.393 | 20 | 200 | fits | 145,898 | 224 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 289,669 | 2.897 | 20 | 200 | fits | 150,995 | 210 | 0.528 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 140,195 | 1.402 | 20 | 20 | fits | 145,898 | 224 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 773,031 | 7.730 | 20 | 20 | fits | 150,309 | 119 | 0.503 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 143,780 | 1.438 | 20 | 24 | fits | 145,898 | 224 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 776,466 | 7.765 | 20 | 24 | fits | 150,309 | 119 | 0.503 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 142,740 | 1.427 | 20 | 50 | fits | 145,898 | 224 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 293,345 | 2.933 | 20 | 50 | fits | 150,995 | 210 | 0.528 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 427,379 | 4.274 | 20 | 20 | fits | 134,099 | 52 | 0.596 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 623,622 | 6.236 | 20 | 20 | fits | 82,100 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 251,843 | 2.518 | 20 | 20 | fits | 156,563 | 215 | 0.514 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 136,387 | 1.364 | 20 | 200 | fits | 142,665 | 220 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 292,341 | 2.923 | 20 | 200 | fits | 156,563 | 215 | 0.514 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 137,299 | 1.373 | 20 | 20 | fits | 142,665 | 220 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 785,018 | 7.850 | 20 | 20 | fits | 150,292 | 118 | 0.549 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 140,884 | 1.409 | 20 | 24 | fits | 142,665 | 220 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 788,453 | 7.885 | 20 | 24 | fits | 150,292 | 118 | 0.549 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 139,844 | 1.398 | 20 | 50 | fits | 142,665 | 220 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 296,017 | 2.960 | 20 | 50 | fits | 156,563 | 215 | 0.514 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 429,973 | 4.300 | 20 | 20 | fits | 134,021 | 52 | 0.594 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 626,383 | 6.264 | 20 | 20 | fits | 82,252 | 37 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 625,257 | 6.253 | 20 | 20 | fits | 150,048 | 173 | 0.566 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 153,145 | 1.531 | 20 | 200 | fits | 156,386 | 229 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 651,978 | 6.520 | 20 | 200 | fits | 150,048 | 173 | 0.566 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 154,057 | 1.541 | 20 | 20 | fits | 156,386 | 229 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 800,289 | 8.003 | 20 | 20 | fits | 147,615 | 112 | 0.541 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 157,642 | 1.576 | 20 | 24 | fits | 156,386 | 229 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 803,724 | 8.037 | 20 | 24 | fits | 147,615 | 112 | 0.541 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 156,602 | 1.566 | 20 | 50 | fits | 156,386 | 229 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 655,654 | 6.557 | 20 | 50 | fits | 150,048 | 173 | 0.566 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 298,083 | 2.981 | 20 | 20 | fits | 141,936 | 94 | 0.568 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 494,262 | 4.943 | 20 | 20 | fits | 82,252 | 37 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 618,908 | 6.189 | 20 | 20 | fits | 147,645 | 165 | 0.579 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 141,085 | 1.411 | 20 | 200 | fits | 142,639 | 220 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 643,745 | 6.437 | 20 | 200 | fits | 147,645 | 165 | 0.579 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 141,997 | 1.420 | 20 | 20 | fits | 142,639 | 220 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 788,232 | 7.882 | 20 | 20 | fits | 143,791 | 112 | 0.511 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 145,582 | 1.456 | 20 | 24 | fits | 142,639 | 220 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 816,436 | 8.164 | 20 | 24 | fits | 24,769 | 18 | 0.660 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 144,542 | 1.445 | 20 | 50 | fits | 142,639 | 220 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 647,421 | 6.474 | 20 | 50 | fits | 147,645 | 165 | 0.579 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 286,237 | 2.862 | 20 | 20 | fits | 142,150 | 94 | 0.570 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 497,696 | 4.977 | 20 | 20 | fits | 88,053 | 43 | 0.572 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 580,054 | 5.801 | 20 | 20 | fits | 145,879 | 165 | 0.558 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 146,028 | 1.460 | 20 | 200 | fits | 145,895 | 224 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 652,962 | 6.530 | 20 | 200 | fits | 145,879 | 165 | 0.558 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 146,940 | 1.469 | 20 | 20 | fits | 145,895 | 224 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 801,651 | 8.017 | 20 | 20 | fits | 147,993 | 118 | 0.484 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 150,525 | 1.505 | 20 | 24 | fits | 145,895 | 224 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 805,086 | 8.051 | 20 | 24 | fits | 147,993 | 118 | 0.484 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 149,485 | 1.495 | 20 | 50 | fits | 145,895 | 224 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 656,638 | 6.566 | 20 | 50 | fits | 145,879 | 165 | 0.558 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 290,900 | 2.909 | 20 | 20 | fits | 141,870 | 95 | 0.563 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 508,679 | 5.087 | 20 | 20 | fits | 88,536 | 42 | 0.527 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 278,513 | 2.785 | 20 | 20 | fits | 153,173 | 213 | 0.528 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 144,218 | 1.442 | 20 | 200 | fits | 142,398 | 221 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 305,116 | 3.051 | 20 | 200 | fits | 153,173 | 213 | 0.528 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 145,130 | 1.451 | 20 | 20 | fits | 142,398 | 221 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 795,186 | 7.952 | 20 | 20 | fits | 151,110 | 118 | 0.505 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 148,715 | 1.487 | 20 | 24 | fits | 142,398 | 221 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 798,621 | 7.986 | 20 | 24 | fits | 151,110 | 118 | 0.505 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 147,675 | 1.477 | 20 | 50 | fits | 142,398 | 221 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 308,792 | 3.088 | 20 | 50 | fits | 153,173 | 213 | 0.528 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 448,695 | 4.487 | 20 | 20 | fits | 139,968 | 58 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 644,976 | 6.450 | 20 | 20 | fits | 82,142 | 36 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 262,593 | 2.626 | 20 | 20 | fits | 146,567 | 210 | 0.518 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 135,483 | 1.355 | 20 | 200 | fits | 143,314 | 179 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 281,441 | 2.814 | 20 | 200 | fits | 146,567 | 210 | 0.518 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 136,395 | 1.364 | 20 | 20 | fits | 143,314 | 179 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 424,668 | 4.247 | 20 | 20 | fits | 142,531 | 143 | 0.557 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 139,980 | 1.400 | 20 | 24 | fits | 143,314 | 179 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 800,361 | 8.004 | 20 | 24 | fits | 40,686 | 31 | 0.596 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 138,940 | 1.389 | 20 | 50 | fits | 143,314 | 179 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 285,117 | 2.851 | 20 | 50 | fits | 146,567 | 210 | 0.518 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 560,969 | 5.610 | 20 | 20 | fits | 133,386 | 52 | 0.586 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 757,140 | 7.571 | 20 | 20 | fits | 82,142 | 36 | 0.457 |
| LINK_UP | `adp.link_up.if0` | 2,514 | 0.025 | 20 | 200 | fits | 22,457 | 43 (11) | 0.727 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,431 | 0.104 | 20 | 200 | fits | 17,859 | 23 (39) | 0.732 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 2,605 | 0.026 | 20 | 200 | fits | 2,587 | 10 (11) | 0.538 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 150,555 | 1.506 | 20 | 200 | fits | 151,494 | 237 | 0.487 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 609,473 | 6.095 | 20 | 20 | fits | 143,944 | 149 | 0.497 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 272,620 | 2.726 | 20 | 24 | fits | 33,168 | 27 | 0.680 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 569,998 | 5.700 | 20 | 50 | fits | 143,944 | 149 | 0.497 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 404,029 | 4.040 | 20 | 20 | fits | 81,986 | 36 | 0.455 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 112,906 | 1.129 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 150,555 | 1.506 | 20 | 200 | fits | 151,494 | 237 | 0.487 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 619,741 | 6.197 | 20 | 20 | fits | 145,597 | 151 | 0.521 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 286,220 | 2.862 | 20 | 24 | fits | 33,557 | 33 | 0.650 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 580,266 | 5.803 | 20 | 50 | fits | 145,597 | 151 | 0.521 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 412,644 | 4.126 | 20 | 20 | fits | 84,677 | 42 | 0.496 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 117,574 | 1.176 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 12,112 | 0.121 | 20 | 20 | fits | 25,234 | 21 (35) | 0.828 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 13,127 | 0.131 | 20 | 20 | fits | 21,873 | 17 (14) | 0.872 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 5,512 | 0.055 | 20 | 20 | fits | 21,609 | 18 (14) | 0.867 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 14,402 | 0.144 | 20 | 20 | fits | 25,320 | 21 (35) | 0.828 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 76,756 | 0.768 | 20 | 20 | fits | 61,769 | 6 | 0.890 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 38,440 | 0.384 | 20 | 20 | fits | 38,505 | 12 | 0.899 |
| malformed MRPDU discard | `srp.malformed.if0` | 13,800 | 0.138 | 20 | 20 | fits | 13,865 | 12 | 0.586 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 78,740 | 0.787 | 220 | 220 | fits | 83,547 | 9 | 0.871 |
| an event behind 15 others | `backlog.event.if0` | 159,344 | 1.593 | 20 | 200 | fits | 73,435 | 109 | 0.538 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 453,196 | 4.532 | 20 | 20 | fits | 142,718 | 109 | 0.512 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 148,787 | 1.488 | 20 | 200 | fits | 148,995 | 226 | 0.513 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 304,720 | 3.047 | 20 | 200 | fits | 83,107 | 52 | 0.613 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 144,528 | 1.445 | 20 | 20 | fits | 148,995 | 226 | 0.513 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 522,197 | 5.222 | 20 | 20 | fits | 142,718 | 109 | 0.512 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 148,113 | 1.481 | 20 | 24 | fits | 148,995 | 226 | 0.513 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 550,139 | 5.501 | 20 | 24 | fits | 24,507 | 18 | 0.665 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 147,073 | 1.471 | 20 | 50 | fits | 148,995 | 226 | 0.513 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 303,225 | 3.032 | 20 | 50 | fits | 83,107 | 52 | 0.613 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 336,110 | 3.361 | 20 | 20 | fits | 29,423 | 53 | 0.243 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 380,379 | 3.804 | 20 | 20 | fits | 20,185 | 36 | 0.048 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 591,210 | 5.912 | 20 | 20 | fits | 146,259 | 168 | 0.550 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 138,291 | 1.383 | 20 | 200 | fits | 142,973 | 223 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 639,492 | 6.395 | 20 | 200 | fits | 146,259 | 168 | 0.550 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 139,203 | 1.392 | 20 | 20 | fits | 142,973 | 223 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 785,946 | 7.859 | 20 | 20 | fits | 145,758 | 113 | 0.532 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 142,788 | 1.428 | 20 | 24 | fits | 142,973 | 223 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 814,387 | 8.144 | 20 | 24 | fits | 25,006 | 18 | 0.671 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 141,748 | 1.417 | 20 | 50 | fits | 142,973 | 223 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 643,168 | 6.432 | 20 | 50 | fits | 146,259 | 168 | 0.550 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 283,330 | 2.833 | 20 | 20 | fits | 142,037 | 95 | 0.566 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 494,829 | 4.948 | 20 | 20 | fits | 82,617 | 36 | 0.473 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 5,858 | 0.059 | 20 | 20 | fits | 21,617 | 19 | 0.801 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 138,291 | 1.383 | 20 | 200 | fits | 142,973 | 223 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 19,321 | 0.193 | 20 | 200 | fits | 21,617 | 19 | 0.801 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 139,203 | 1.392 | 20 | 20 | fits | 142,973 | 223 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 789,342 | 7.893 | 20 | 20 | fits | 146,066 | 114 | 0.533 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 142,788 | 1.428 | 20 | 24 | fits | 142,973 | 223 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 792,777 | 7.928 | 20 | 24 | fits | 146,066 | 114 | 0.533 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 141,748 | 1.417 | 20 | 50 | fits | 142,973 | 223 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 646,256 | 6.463 | 20 | 50 | fits | 149,347 | 167 | 0.530 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 283,330 | 2.833 | 20 | 20 | fits | 142,037 | 95 | 0.566 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 494,829 | 4.948 | 20 | 20 | fits | 82,617 | 36 | 0.473 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,282,445 | 62.824 | 20 | 20 | MISS ceiling | 13,896 | 13 | 0.629 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,296,298 | 62.963 | 20 | 20 | MISS ceiling | 13,988 | 13 | 0.600 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,310,219 | 63.102 | 20 | 20 | MISS ceiling | 13,917 | 13 | 0.609 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,323,974 | 63.240 | 20 | 20 | MISS ceiling | 13,830 | 13 | 0.629 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,337,855 | 63.379 | 20 | 20 | MISS ceiling | 14,023 | 13 | 0.629 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 150,755 | 1.508 | 20 | 200 | fits | 150,713 | 217 | 0.516 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 601,667 | 6.017 | 20 | 200 | fits | 105,849 | 129 | 0.585 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 146,496 | 1.465 | 20 | 20 | fits | 150,713 | 217 | 0.516 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,213,557 | 62.136 | 20 | 20 | MISS ceiling | 24,741 | 15 | 0.759 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 150,081 | 1.501 | 20 | 24 | fits | 150,713 | 217 | 0.516 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,192,251 | 61.923 | 20 | 24 | MISS ceiling | 163,134 | 119 | 0.473 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 149,041 | 1.490 | 20 | 50 | fits | 150,713 | 217 | 0.516 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 600,172 | 6.002 | 20 | 50 | fits | 105,849 | 129 | 0.585 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 292,197 | 2.922 | 20 | 20 | fits | 143,611 | 95 | 0.580 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 492,243 | 4.922 | 20 | 20 | fits | 83,998 | 37 | 0.502 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,959 | 0.060 | 20 | 20 | fits | 19,542 | 13 (29) | 0.805 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 8,188 | 0.082 | 20 | 20 | fits | 21,570 | 19 (35) | 0.803 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 16,561 | 0.166 | 20 | 20 | fits | 25,493 | 21 (12) | 0.831 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 10,399 | 0.104 | 20 | 50 | fits | 22,457 | 43 | 0.727 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 9,775 | 0.098 | 20 | 50 | fits | 19,072 | 35 | 0.697 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 7,092 | 0.071 | 20 | 50 | fits | 18,822 | 35 | 0.692 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 9,478 | 0.095 | 20 | 50 | fits | 24,086 | 61 | 0.636 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 11,468 | 0.115 | 20 | 50 | fits | 24,086 | 61 | 0.636 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 9,863 | 0.099 | 20 | 50 | fits | 18,073 | 30 | 0.634 |
| LINK_UP | `adp.link_up.if0` | 2,514 | 0.025 | 20 | 200 | fits | 22,457 | 43 (11) | 0.727 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,431 | 0.104 | 20 | 200 | fits | 17,859 | 23 (39) | 0.732 |
| LINK_DOWN | `adp.link_down.if0` | 2,231 | 0.022 | 20 | 200 | fits | 21,378 | 23 (9) | 0.740 |
| LINK_UP | `adp.link_up.if0` | 2,514 | 0.025 | 20 | 200 | fits | 22,457 | 43 (11) | 0.727 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,431 | 0.104 | 20 | 200 | fits | 17,859 | 23 (39) | 0.732 |
| GM_CHANGE | `adp.gm_change.if0` | 2,364 | 0.024 | 20 | 200 | fits | 12,513 | 17 (11) | 0.703 |
| LINK_UP | `adp.link_up.if0` | 2,514 | 0.025 | 20 | 200 | fits | 22,457 | 43 (11) | 0.727 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,431 | 0.104 | 20 | 200 | fits | 17,859 | 23 (39) | 0.732 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,564 | 0.046 | 20 | 200 | fits | 12,526 | 16 (31) | 0.620 |
| LINK_UP | `adp.link_up.if0` | 2,514 | 0.025 | 20 | 200 | fits | 22,457 | 43 (11) | 0.727 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,431 | 0.104 | 20 | 200 | fits | 17,859 | 23 (39) | 0.732 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,564 | 0.046 | 20 | 200 | fits | 12,526 | 16 (31) | 0.620 |
| set_name | `aecp_fanout.set_name.if0` | 41,392 | 0.414 | 20 | 24 | fits | 54,291 | 88 | 0.544 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 42,866 | 0.429 | 20 | 24 | fits | 47,214 | 77 | 0.558 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 34,599 | 0.346 | 20 | 24 | fits | 43,455 | 78 | 0.511 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 40,205 | 0.402 | 20 | 24 | fits | 43,537 | 77 | 0.514 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 43,829 | 0.438 | 20 | 24 | fits | 48,941 | 66 | 0.588 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 36,602 | 0.366 | 20 | 24 | fits | 47,295 | 65 | 0.563 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 35,281 | 0.353 | 20 | 24 | fits | 45,531 | 66 | 0.556 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 46,554 | 0.466 | 20 | 24 | fits | 42,711 | 77 | 0.511 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 41,297 | 0.413 | 20 | 24 | fits | 43,222 | 78 | 0.514 |
| BIND_RX | `acmp.bind_rx.if0` | 18,382 | 0.184 | 20 | 20 | fits | 36,591 | 26 (77) | 0.798 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 8,920 | 0.089 | 20 | 20 | fits | 24,951 | 20 (32) | 0.819 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,290 | 0.103 | 20 | 20 | fits | 20,447 | 15 (47) | 0.762 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,087 | 0.131 | 20 | 20 | fits | 31,782 | 18 (50) | 0.828 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 9,881 | 0.099 | 20 | 20 | fits | 21,181 | 17 (48) | 0.757 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,287 | 0.093 | 20 | 20 | fits | 19,886 | 16 (48) | 0.727 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 8,964 | 0.090 | 20 | 20 | fits | 19,296 | 16 (48) | 0.722 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,309 | 0.093 | 20 | 20 | fits | 18,885 | 16 (48) | 0.711 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 11,699 | 0.117 | 20 | 24 | fits | 22,573 | 20 | 0.765 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 15,357 | 0.154 | 20 | 24 | fits | 27,244 | 20 | 0.701 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 16,071 | 0.161 | 20 | 24 | fits | 22,257 | 20 | 0.706 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 9,749 | 0.097 | 20 | 24 | fits | 22,254 | 20 | 0.713 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 15,373 | 0.154 | 20 | 24 | fits | 22,801 | 20 | 0.705 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 11,155 | 0.112 | 20 | 24 | fits | 23,099 | 20 | 0.716 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 10,826 | 0.108 | 20 | 24 | fits | 22,215 | 20 | 0.713 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 15,566 | 0.156 | 20 | 24 | fits | 22,204 | 20 | 0.722 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 10,333 | 0.103 | 20 | 24 | fits | 21,856 | 20 | 0.729 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 17,869 | 0.179 | 20 | 24 | fits | 24,430 | 21 | 0.614 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 10,005 | 0.100 | 20 | 24 | fits | 21,185 | 20 | 0.742 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 14,753 | 0.148 | 20 | 24 | fits | 20,882 | 20 | 0.727 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 9,332 | 0.093 | 20 | 24 | fits | 21,922 | 20 | 0.716 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 15,137 | 0.151 | 20 | 24 | fits | 22,598 | 20 | 0.710 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 10,230 | 0.102 | 20 | 24 | fits | 22,320 | 20 | 0.733 |
| get_configuration | `aecp.get_configuration.if0` | 8,485 | 0.085 | 20 | 24 | fits | 19,784 | 20 | 0.738 |
| entity_available | `aecp.entity_available.if0` | 13,255 | 0.133 | 20 | 24 | fits | 19,461 | 20 | 0.712 |
| get_name | `aecp.get_name.if0` | 10,816 | 0.108 | 20 | 24 | fits | 23,292 | 20 | 0.756 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 16,752 | 0.168 | 20 | 24 | fits | 23,538 | 27 | 0.709 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 12,488 | 0.125 | 20 | 24 | fits | 23,927 | 29 | 0.750 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 13,823 | 0.138 | 20 | 24 | fits | 19,697 | 20 | 0.734 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 7,655 | 0.077 | 20 | 24 | fits | 19,437 | 20 | 0.728 |
| set_name | `aecp.set_name.if0` | 27,437 | 0.274 | 20 | 24 | fits | 36,709 | 42 | 0.734 |
| lock_entity | `aecp.lock_entity.if0` | 19,660 | 0.197 | 20 | 24 | fits | 28,372 | 33 | 0.760 |
| unlock_entity | `aecp.unlock_entity.if0` | 19,427 | 0.194 | 20 | 24 | fits | 27,872 | 32 | 0.758 |
| LINK_UP | `fixture.link_up.if0` | 2,514 | 0.025 | 20 | 200 | fits | 22,457 | 43 (11) | 0.727 |
| malformed MRPDU discard | `fixture.malformed.if0` | 14,959 | 0.150 | 20 | 20 | fits | 15,024 | 12 | 0.697 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 27,885 | 0.279 | 20 | 24 | fits | 38,201 | 42 | 0.753 |
| LINK_DOWN | `fixture.link_down.if0` | 2,479 | 0.025 | 20 | 200 | fits | 22,802 | 23 (9) | 0.752 |
| BIND_RX | `fixture.bind_rx.if0` | 18,277 | 0.183 | 20 | 20 | fits | 36,110 | 26 (77) | 0.801 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 23,217 | 0.232 | 20 | 20 | fits | 33,747 | 35 (35) | 0.788 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 6,330 | 0.063 | 20 | 20 | fits | 20,379 | 13 (29) | 0.815 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 74,692 | 0.747 | 20 | 200 | fits | 74,795 | 51 | 0.757 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 74,692 | 0.747 | 20 | 200 | fits | 74,795 | 51 | 0.757 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 74,422 | 0.744 | 20 | 20 | fits | 74,795 | 51 | 0.757 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 74,422 | 0.744 | 20 | 20 | fits | 74,795 | 51 | 0.757 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 74,627 | 0.746 | 20 | 24 | fits | 74,795 | 51 | 0.757 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 74,627 | 0.746 | 20 | 24 | fits | 74,795 | 51 | 0.757 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 74,562 | 0.746 | 20 | 50 | fits | 74,795 | 51 | 0.757 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 74,562 | 0.746 | 20 | 50 | fits | 74,795 | 51 | 0.757 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 74,497 | 0.745 | 20 | 20 | fits | 74,795 | 51 | 0.757 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 74,497 | 0.745 | 20 | 20 | fits | 74,795 | 51 | 0.757 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
