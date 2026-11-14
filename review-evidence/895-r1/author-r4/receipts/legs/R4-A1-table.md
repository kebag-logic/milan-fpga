### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 92 paths and 7 of 950 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.191 (0.421) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.090 (0.243) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.085 (0.270) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.120 (0.468) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.103 (0.253) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.093 (0.243) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.094 (0.251) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.104 (0.257) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.097 (0.331) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.141 (0.511) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.118 (0.464) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.210 (0.635) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.167 (0.523) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.162 (0.586) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.207 (0.552) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.140 (0.405) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.051 (0.168) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.025 (0.164) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.029 (0.261) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.028 (0.267) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.022 (0.027) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.106 (0.421) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.103 (0.426) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.226 (0.550) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.235 (0.558) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.121 (0.295) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.239 (0.561) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.306 (0.677) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.194 (0.508) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.278 (0.606) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.241 (0.564) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.238 (0.559) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.249 (0.575) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.304 (0.630) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.202 (0.535) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.118 (0.444) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.256 (0.584) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.208 (0.528) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.130 (0.458) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.211 (0.533) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.130 (0.459) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.217 (0.537) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.115 (0.278) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.192 (0.511) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.212 (0.627) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.109 (0.433) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.292 (0.674) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.387 (2.691) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.530 (0.820) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.690 (1.009) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.595 (0.935) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.566 (0.857) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.480 (0.815) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 2.255 (2.553) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.446 (0.729) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 1.371 (1.689) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 1.257 (1.627) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 2.789 (3.154) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 2.357 (2.721) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.359 (1.519) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.236 (4.615) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 4.545 (5.101) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.082 (0.273) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.615 (2.034) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.983 (63.275) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.714 (64.007) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.318 (0.463) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 2.933 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 1.531 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 3.064 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 1.821 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 10.158 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.217 (0.543) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.092 (0.220) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.109 (0.267) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.194 (0.543) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.194 (0.502) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 3.000 | fits | 0 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.089 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.096 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.132 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 5.072 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.325 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.829 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.115 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.maap.last.if0` (backlog-adp@program-aged2-7) | 5.109 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-7.service.srp.first.if0` (backlog-adp@program-aged2-7) | 6.004 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.srp.last.if0` (backlog-adp@program-aged2-7) | 11.257 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.923 (1.018) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.453 (0.454) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.224 (0.225) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.774 (0.858) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 12.465 | 11 | 151,879 (1.519) | yes | - |
| backlog-adp@blank-1 | 0 | 11.701 | 11 | 149,612 (1.496) | yes | - |
| backlog-adp@blank-2 | 0 | 11.723 | 11 | 150,877 (1.509) | yes | - |
| backlog-adp@blank-3 | 0 | 11.572 | 11 | 149,532 (1.495) | yes | - |
| backlog-adp@blank-4 | 0 | 12.042 | 13 | 151,198 (1.512) | yes | - |
| backlog-adp@blank-5 | 0 | 11.753 | 12 | 147,446 (1.474) | yes | - |
| backlog-adp@blank-6 | 0 | 11.789 | 12 | 150,982 (1.510) | yes | - |
| backlog-adp@blank-7 | 0 | 13.499 | 14 | 150,664 (1.507) | yes | - |
| backlog-adp@program-0 | 0 | 11.757 | 11 | 150,753 (1.508) | yes | - |
| backlog-adp@program-1 | 0 | 11.910 | 13 | 151,281 (1.513) | yes | - |
| backlog-adp@program-2 | 0 | 11.759 | 11 | 149,559 (1.496) | yes | - |
| backlog-adp@program-3 | 0 | 12.059 | 12 | 150,234 (1.502) | yes | - |
| backlog-adp@program-4 | 0 | 11.522 | 13 | 150,152 (1.502) | yes | - |
| backlog-adp@program-5 | 0 | 10.981 | 11 | 151,220 (1.512) | yes | - |
| backlog-adp@program-6 | 0 | 10.983 | 11 | 151,953 (1.520) | yes | - |
| backlog-adp@program-7 | 0 | 10.864 | 10 | 150,927 (1.509) | yes | - |
| backlog-adp@verify-0 | 0 | 11.973 | 11 | 149,635 (1.496) | yes | - |
| backlog-adp@verify-1 | 0 | 11.685 | 11 | 149,484 (1.495) | yes | - |
| backlog-adp@verify-2 | 0 | 11.695 | 11 | 150,749 (1.507) | yes | - |
| backlog-adp@verify-3 | 0 | 12.158 | 13 | 151,857 (1.519) | yes | - |
| backlog-adp@verify-4 | 0 | 11.820 | 12 | 151,103 (1.511) | yes | - |
| backlog-adp@verify-5 | 0 | 11.750 | 12 | 147,484 (1.475) | yes | - |
| backlog-adp@verify-6 | 0 | 11.712 | 11 | 150,242 (1.502) | yes | - |
| backlog-adp@verify-7 | 0 | 11.932 | 12 | 150,833 (1.508) | yes | - |
| backlog-adp@blank-aged2-0 | 1 | 11.435 | 10 | 151,266 (1.513) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 11.762 | 12 | 149,831 (1.498) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 11.749 | 12 | 152,544 (1.525) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 11.690 | 11 | 149,526 (1.495) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 11.710 | 11 | 150,791 (1.508) | yes | - |
| backlog-adp@blank-aged2-5 | 1 | 11.584 | 10 | 150,816 (1.508) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 11.569 | 11 | 150,732 (1.507) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 13.006 | 14 | 151,437 (1.514) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 12.400 | 13 | 152,146 (1.521) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 12.887 | 14 | 152,148 (1.521) | yes | - |
| backlog-adp@blank-aged1-2 | 1 | 12.750 | 14 | 147,136 (1.471) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 12.581 | 15 | 149,607 (1.496) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 12.479 | 14 | 147,333 (1.473) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 12.349 | 13 | 149,432 (1.494) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 13.483 | 14 | 151,777 (1.518) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 12.315 | 12 | 150,840 (1.508) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.886 | 12 | 152,482 (1.525) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 11.748 | 12 | 147,587 (1.476) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 11.628 | 11 | 150,796 (1.508) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 11.668 | 11 | 151,904 (1.519) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 11.703 | 11 | 149,545 (1.495) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 11.691 | 11 | 151,890 (1.519) | yes | - |
| backlog-adp@program-aged2-6 | 1 | 11.888 | 12 | 151,172 (1.512) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 12.024 | 13 | 146,413 (1.464) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 12.182 | 13 | 152,045 (1.520) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 11.945 | 13 | 149,880 (1.499) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 11.804 | 12 | 152,519 (1.525) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 11.743 | 11 | 149,607 (1.496) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 11.637 | 10 | 147,156 (1.472) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 11.632 | 11 | 149,548 (1.495) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 11.636 | 11 | 150,813 (1.508) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 12.213 | 13 | 151,262 (1.513) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.457 | 11 | 150,955 (1.510) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 11.657 | 11 | 152,063 (1.521) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 11.695 | 11 | 149,704 (1.497) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 12.416 | 13 | 152,049 (1.520) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 11.861 | 12 | 151,361 (1.514) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 11.722 | 12 | 147,570 (1.476) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 11.770 | 12 | 149,586 (1.496) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 12.629 | 12 | 150,896 (1.509) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 11.729 | 12 | 152,744 (1.527) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 11.809 | 12 | 147,660 (1.477) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 11.691 | 11 | 150,879 (1.509) | yes | - |
| backlog-adp@verify-aged1-3 | 1 | 11.567 | 10 | 151,022 (1.510) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 11.587 | 11 | 150,938 (1.509) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 11.580 | 11 | 152,046 (1.520) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 13.357 | 14 | 149,863 (1.499) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 12.938 | 13 | 146,548 (1.465) | yes | - |
| backlog | 0 | 5.709 | 7 | 148,936 (1.489) | yes | - |
| backlog-adp | 0 | 11.560 | 13 | 149,779 (1.498) | yes | - |
| backlog-adp-refill | 0 | 40.759 | 25 | 149,779 (1.498) | yes | - |
| backlog-owed | 0 | 64.357 | 26 | 150,864 (1.509) | yes | - |
| fixture | 0 | 1.311 | 2 | 82,042 (0.820) | yes | - |

Composed maximum over the 4 backlog windows: 150,864 CPU cycles (1.509 ms), backlog-owed.
Over the windows that released their whole load only: 150,864 (1.509 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3609 | 0 | 41,749 (0.417) | fits |
| save-second | 47489 | 0 | 49,538 (0.495) | fits |
| backlog-adp@blank-0 | 406 | 0 | 151,879 (1.519) | fits |
| backlog-adp@blank-1 | 406 | 0 | 149,612 (1.496) | fits |
| backlog-adp@blank-2 | 406 | 0 | 150,877 (1.509) | fits |
| backlog-adp@blank-3 | 406 | 0 | 149,532 (1.495) | fits |
| backlog-adp@blank-4 | 408 | 0 | 151,198 (1.512) | fits |
| backlog-adp@blank-5 | 407 | 0 | 147,446 (1.474) | fits |
| backlog-adp@blank-6 | 407 | 0 | 150,982 (1.510) | fits |
| backlog-adp@blank-7 | 411 | 0 | 150,664 (1.507) | fits |
| backlog-adp@program-0 | 502 | 0 | 150,753 (1.508) | fits |
| backlog-adp@program-1 | 504 | 0 | 151,281 (1.513) | fits |
| backlog-adp@program-2 | 504 | 0 | 149,559 (1.496) | fits |
| backlog-adp@program-3 | 505 | 0 | 150,234 (1.502) | fits |
| backlog-adp@program-4 | 507 | 0 | 150,152 (1.502) | fits |
| backlog-adp@program-5 | 506 | 0 | 151,220 (1.512) | fits |
| backlog-adp@program-6 | 507 | 0 | 151,953 (1.520) | fits |
| backlog-adp@program-7 | 507 | 0 | 150,927 (1.509) | fits |
| backlog-adp@verify-0 | 590 | 0 | 149,635 (1.496) | fits |
| backlog-adp@verify-1 | 590 | 0 | 149,484 (1.495) | fits |
| backlog-adp@verify-2 | 590 | 0 | 150,749 (1.507) | fits |
| backlog-adp@verify-3 | 592 | 0 | 151,857 (1.519) | fits |
| backlog-adp@verify-4 | 592 | 0 | 151,103 (1.511) | fits |
| backlog-adp@verify-5 | 591 | 0 | 147,484 (1.475) | fits |
| backlog-adp@verify-6 | 592 | 0 | 150,242 (1.502) | fits |
| backlog-adp@verify-7 | 593 | 0 | 150,833 (1.508) | fits |
| backlog-adp@blank-aged2-0 | 708 | 0 | 151,266 (1.513) | fits |
| backlog-adp@blank-aged2-1 | 715 | 0 | 149,831 (1.498) | fits |
| backlog-adp@blank-aged2-2 | 723 | 0 | 152,544 (1.525) | fits |
| backlog-adp@blank-aged2-3 | 730 | 0 | 149,526 (1.495) | fits |
| backlog-adp@blank-aged2-4 | 738 | 0 | 150,791 (1.508) | fits |
| backlog-adp@blank-aged2-5 | 745 | 0 | 150,816 (1.508) | fits |
| backlog-adp@blank-aged2-6 | 753 | 0 | 150,732 (1.507) | fits |
| backlog-adp@blank-aged2-7 | 764 | 0 | 151,437 (1.514) | fits |
| backlog-adp@blank-aged1-0 | 649 | 0 | 152,146 (1.521) | fits |
| backlog-adp@blank-aged1-1 | 658 | 0 | 152,148 (1.521) | fits |
| backlog-adp@blank-aged1-2 | 666 | 0 | 147,136 (1.471) | fits |
| backlog-adp@blank-aged1-3 | 674 | 0 | 149,607 (1.496) | fits |
| backlog-adp@blank-aged1-4 | 681 | 0 | 147,333 (1.473) | fits |
| backlog-adp@blank-aged1-5 | 688 | 0 | 149,432 (1.494) | fits |
| backlog-adp@blank-aged1-6 | 697 | 0 | 151,777 (1.518) | fits |
| backlog-adp@blank-aged1-7 | 703 | 0 | 150,840 (1.508) | fits |
| backlog-adp@program-aged2-0 | 801 | 0 | 152,482 (1.525) | fits |
| backlog-adp@program-aged2-1 | 808 | 0 | 147,587 (1.476) | fits |
| backlog-adp@program-aged2-2 | 815 | 0 | 150,796 (1.508) | fits |
| backlog-adp@program-aged2-3 | 823 | 0 | 151,904 (1.519) | fits |
| backlog-adp@program-aged2-4 | 831 | 0 | 149,545 (1.495) | fits |
| backlog-adp@program-aged2-5 | 839 | 0 | 151,890 (1.519) | fits |
| backlog-adp@program-aged2-6 | 848 | 0 | 151,172 (1.512) | fits |
| backlog-adp@program-aged2-7 | 856 | 0 | 146,413 (1.464) | fits |
| backlog-adp@program-aged1-0 | 739 | 0 | 152,045 (1.520) | fits |
| backlog-adp@program-aged1-1 | 747 | 0 | 149,880 (1.499) | fits |
| backlog-adp@program-aged1-2 | 754 | 0 | 152,519 (1.525) | fits |
| backlog-adp@program-aged1-3 | 761 | 0 | 149,607 (1.496) | fits |
| backlog-adp@program-aged1-4 | 768 | 0 | 147,156 (1.472) | fits |
| backlog-adp@program-aged1-5 | 776 | 0 | 149,548 (1.495) | fits |
| backlog-adp@program-aged1-6 | 784 | 0 | 150,813 (1.508) | fits |
| backlog-adp@program-aged1-7 | 794 | 0 | 151,262 (1.513) | fits |
| backlog-adp@verify-aged2-0 | 890 | 0 | 150,955 (1.510) | fits |
| backlog-adp@verify-aged2-1 | 898 | 0 | 152,063 (1.521) | fits |
| backlog-adp@verify-aged2-2 | 906 | 0 | 149,704 (1.497) | fits |
| backlog-adp@verify-aged2-3 | 916 | 0 | 152,049 (1.520) | fits |
| backlog-adp@verify-aged2-4 | 923 | 0 | 151,361 (1.514) | fits |
| backlog-adp@verify-aged2-5 | 930 | 0 | 147,570 (1.476) | fits |
| backlog-adp@verify-aged2-6 | 938 | 0 | 149,586 (1.496) | fits |
| backlog-adp@verify-aged2-7 | 946 | 0 | 150,896 (1.509) | fits |
| backlog-adp@verify-aged1-0 | 829 | 0 | 152,744 (1.527) | fits |
| backlog-adp@verify-aged1-1 | 837 | 0 | 147,660 (1.477) | fits |
| backlog-adp@verify-aged1-2 | 844 | 0 | 150,879 (1.509) | fits |
| backlog-adp@verify-aged1-3 | 851 | 0 | 151,022 (1.510) | fits |
| backlog-adp@verify-aged1-4 | 859 | 0 | 150,938 (1.509) | fits |
| backlog-adp@verify-aged1-5 | 867 | 0 | 152,046 (1.520) | fits |
| backlog-adp@verify-aged1-6 | 878 | 0 | 149,863 (1.499) | fits |
| backlog-adp@verify-aged1-7 | 885 | 0 | 146,548 (1.465) | fits |
| adp-advertise | 598 | 0 | 30,217 (0.302) | fits |
| save-held | 1453 | 0 | 154,047 (1.540) | fits |
| save-starved | 25020 | 0 | 154,047 (1.540) | fits |
| acmp-noresp | 2026 | 0 | 41,749 (0.417) | fits |
| save | 609 | 0 | 45,103 (0.451) | fits |
| srp | 289 | 0 | 59,146 (0.591) | fits |
| backlog | 285 | 0 | 148,936 (1.489) | fits |
| backlog-adp | 314 | 0 | 149,779 (1.498) | fits |
| backlog-adp-refill | 326 | 0 | 149,779 (1.498) | fits |
| backlog-owed | 310 | 0 | 150,864 (1.509) | fits |
| acmp-disc | 938 | 0 | 41,749 (0.417) | fits |
| maap | 175 | 0 | 30,217 (0.302) | fits |
| adp-link | 89 | 0 | 38,796 (0.388) | fits |
| adp-gm | 88 | 0 | 30,217 (0.302) | fits |
| adp-discover | 88 | 0 | 30,217 (0.302) | fits |
| control | 88 | 0 | 30,217 (0.302) | fits |
| aecp-fanout | 112 | 0 | 66,940 (0.669) | fits |
| acmp-cmd | 87 | 0 | 41,749 (0.417) | fits |
| aecp | 110 | 0 | 45,421 (0.454) | fits |
| aecp-largest-notice | 106 | 0 | 151,879 (1.519) | fits |
| datapath-events | 117 | 0 | 30,217 (0.302) | fits |
| fixture | 161 | 0 | 82,042 (0.820) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | +10.328 ms, 76,740 (0.767 ms), read-back | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 10.291 (20) | 9.709 |
| backlog-adp@blank-aged2-1 | 2 | +9.569 ms, 76,740 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 11.108 (20) | 8.892 |
| backlog-adp@blank-aged2-2 | 2 | +7.780 ms, 76,740 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 11.223 (20) | 8.777 |
| backlog-adp@blank-aged2-3 | 2 | +6.823 ms, 76,740 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 11.165 (20) | 8.835 |
| backlog-adp@blank-aged2-4 | 2 | +5.945 ms, 76,740 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 11.186 (20) | 8.814 |
| backlog-adp@blank-aged2-5 | 2 | +5.053 ms, 76,748 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 11.060 (20) | 8.940 |
| backlog-adp@blank-aged2-6 | 2 | none | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 11.042 (20) | 8.958 |
| backlog-adp@blank-aged2-7 | 2 | none | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 11.081 (20) | 8.919 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 10.452 (20) | 9.548 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 10.680 (20) | 9.320 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 11.008 (20) | 8.992 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 11.006 (20) | 8.994 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 11.199 (20) | 8.801 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 11.070 (20) | 8.930 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 11.108 (20) | 8.892 |
| backlog-adp@blank-aged1-7 | 1 | none | +11.213 ms, 76,581 (0.766 ms), read-back | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 10.977 (20) | 9.023 |
| backlog-adp@program-aged2-0 | 2 | none | +10.279 ms, 80,622 (0.806 ms), issue | `backlog-adp@program-aged2-0.service.srp.last.if0` | 10.242 (20) | 9.758 |
| backlog-adp@program-aged2-1 | 2 | none | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 11.219 (20) | 8.781 |
| backlog-adp@program-aged2-2 | 2 | +8.673 ms, 80,622 (0.806 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 11.101 (20) | 8.899 |
| backlog-adp@program-aged2-3 | 2 | +6.928 ms, 80,622 (0.806 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 11.141 (20) | 8.859 |
| backlog-adp@program-aged2-4 | 2 | +6.067 ms, 80,622 (0.806 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 11.176 (20) | 8.824 |
| backlog-adp@program-aged2-5 | 2 | +5.152 ms, 80,667 (0.807 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 11.165 (20) | 8.835 |
| backlog-adp@program-aged2-6 | 2 | +4.304 ms, 80,450 (0.804 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 11.068 (20) | 8.932 |
| backlog-adp@program-aged2-7 | 2 | +3.023 ms, 80,518 (0.805 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 11.257 (20) | 8.743 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 10.289 (20) | 9.711 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 10.329 (20) | 9.671 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 10.479 (20) | 9.521 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 10.419 (20) | 9.581 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 10.313 (20) | 9.687 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 10.309 (20) | 9.691 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 10.308 (20) | 9.692 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 10.340 (20) | 9.660 |
| backlog-adp@verify-aged2-0 | 2 | none | +10.344 ms, 77,376 (0.774 ms), read-back | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 10.307 (20) | 9.693 |
| backlog-adp@verify-aged2-1 | 2 | +9.491 ms, 77,376 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 11.129 (20) | 8.871 |
| backlog-adp@verify-aged2-2 | 2 | +7.739 ms, 77,376 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 11.168 (20) | 8.832 |
| backlog-adp@verify-aged2-3 | 2 | +6.971 ms, 77,339 (0.773 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 11.157 (20) | 8.843 |
| backlog-adp@verify-aged2-4 | 2 | +5.961 ms, 77,376 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 11.040 (20) | 8.960 |
| backlog-adp@verify-aged2-5 | 2 | +5.188 ms, 77,421 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 11.196 (20) | 8.804 |
| backlog-adp@verify-aged2-6 | 2 | +4.338 ms, 77,579 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 11.245 (20) | 8.755 |
| backlog-adp@verify-aged2-7 | 2 | +3.021 ms, 77,684 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 11.151 (20) | 8.849 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 10.443 (20) | 9.557 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 10.521 (20) | 9.479 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 10.408 (20) | 9.592 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 10.285 (20) | 9.715 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 10.304 (20) | 9.696 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 10.296 (20) | 9.704 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 10.346 (20) | 9.654 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 10.546 (20) | 9.454 |

Least margin over the aged windows: 8.743 ms, `backlog-adp@program-aged2-7.service.srp.last.if0` at 11.257 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.327 | 6,070 | 102 | 2 | 30.862 | yes | within |
| save-held | 2018.397 | 4,070 | 102 | - | 16.618 | no | within |
| save-starved | 4048.248 | 4,070 | 102 | - | 31.518 | yes | within |
| save | 2018.681 | 4,070 | 102 | - | 10.785 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 96,656 (0.967) | 78,945 (0.789) |
| save-second | 520 | 80,218 (0.802) | 77,908 (0.779) |
| backlog-adp@blank-0 | 299 | 91,749 (0.917) | 76,305 (0.763) |
| backlog-adp@blank-1 | 299 | 91,618 (0.916) | 76,260 (0.763) |
| backlog-adp@blank-2 | 299 | 91,618 (0.916) | 76,260 (0.763) |
| backlog-adp@blank-3 | 299 | 91,794 (0.918) | 76,260 (0.763) |
| backlog-adp@blank-4 | 299 | 92,006 (0.920) | 76,313 (0.763) |
| backlog-adp@blank-5 | 299 | 91,856 (0.919) | 76,278 (0.763) |
| backlog-adp@blank-6 | 299 | 91,906 (0.919) | 76,290 (0.763) |
| backlog-adp@blank-7 | 300 | 96,529 (0.965) | 76,290 (0.763) |
| backlog-adp@program-0 | 328 | 96,240 (0.962) | 79,118 (0.791) |
| backlog-adp@program-1 | 328 | 97,636 (0.976) | 79,091 (0.791) |
| backlog-adp@program-2 | 328 | 95,995 (0.960) | 79,139 (0.791) |
| backlog-adp@program-3 | 329 | 96,042 (0.960) | 79,151 (0.792) |
| backlog-adp@program-4 | 329 | 95,995 (0.960) | 78,805 (0.788) |
| backlog-adp@program-5 | 329 | 95,995 (0.960) | 78,805 (0.788) |
| backlog-adp@program-6 | 329 | 95,995 (0.960) | 78,805 (0.788) |
| backlog-adp@program-7 | 329 | 95,995 (0.960) | 78,805 (0.788) |
| backlog-adp@verify-0 | 355 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-1 | 355 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-2 | 355 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-3 | 355 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-4 | 355 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-5 | 355 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-6 | 355 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-7 | 355 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@blank-aged2-0 | 297 | 76,740 (0.767) | 75,573 (0.756) |
| backlog-adp@blank-aged2-1 | 297 | 76,740 (0.767) | 75,573 (0.756) |
| backlog-adp@blank-aged2-2 | 297 | 76,740 (0.767) | 75,573 (0.756) |
| backlog-adp@blank-aged2-3 | 297 | 76,740 (0.767) | 75,573 (0.756) |
| backlog-adp@blank-aged2-4 | 297 | 76,740 (0.767) | 75,573 (0.756) |
| backlog-adp@blank-aged2-5 | 297 | 76,748 (0.767) | 75,573 (0.756) |
| backlog-adp@blank-aged2-6 | 297 | 84,817 (0.848) | 75,731 (0.757) |
| backlog-adp@blank-aged2-7 | 298 | 91,615 (0.916) | 76,258 (0.763) |
| backlog-adp@blank-aged1-0 | 297 | 97,195 (0.972) | 76,285 (0.763) |
| backlog-adp@blank-aged1-1 | 297 | 97,528 (0.975) | 76,285 (0.763) |
| backlog-adp@blank-aged1-2 | 297 | 92,009 (0.920) | 76,282 (0.763) |
| backlog-adp@blank-aged1-3 | 297 | 90,967 (0.910) | 76,202 (0.762) |
| backlog-adp@blank-aged1-4 | 297 | 91,866 (0.919) | 76,291 (0.763) |
| backlog-adp@blank-aged1-5 | 297 | 91,771 (0.918) | 76,291 (0.763) |
| backlog-adp@blank-aged1-6 | 298 | 91,695 (0.917) | 76,291 (0.763) |
| backlog-adp@blank-aged1-7 | 297 | 76,581 (0.766) | 75,533 (0.755) |
| backlog-adp@program-aged2-0 | 326 | 95,995 (0.960) | 78,768 (0.788) |
| backlog-adp@program-aged2-1 | 326 | 95,995 (0.960) | 78,768 (0.788) |
| backlog-adp@program-aged2-2 | 326 | 95,995 (0.960) | 78,768 (0.788) |
| backlog-adp@program-aged2-3 | 326 | 95,995 (0.960) | 78,768 (0.788) |
| backlog-adp@program-aged2-4 | 326 | 95,995 (0.960) | 78,768 (0.788) |
| backlog-adp@program-aged2-5 | 326 | 95,995 (0.960) | 78,768 (0.788) |
| backlog-adp@program-aged2-6 | 326 | 95,995 (0.960) | 78,768 (0.788) |
| backlog-adp@program-aged2-7 | 327 | 95,995 (0.960) | 78,768 (0.788) |
| backlog-adp@program-aged1-0 | 326 | 95,995 (0.960) | 79,039 (0.790) |
| backlog-adp@program-aged1-1 | 326 | 95,995 (0.960) | 78,892 (0.789) |
| backlog-adp@program-aged1-2 | 326 | 95,995 (0.960) | 79,060 (0.791) |
| backlog-adp@program-aged1-3 | 326 | 95,995 (0.960) | 79,060 (0.791) |
| backlog-adp@program-aged1-4 | 326 | 95,995 (0.960) | 79,060 (0.791) |
| backlog-adp@program-aged1-5 | 326 | 95,995 (0.960) | 79,060 (0.791) |
| backlog-adp@program-aged1-6 | 326 | 95,995 (0.960) | 79,072 (0.791) |
| backlog-adp@program-aged1-7 | 327 | 95,995 (0.960) | 79,129 (0.791) |
| backlog-adp@verify-aged2-0 | 355 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-aged2-1 | 355 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-aged2-2 | 355 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-aged2-3 | 355 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-aged2-4 | 355 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-aged2-5 | 355 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-aged2-6 | 355 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-aged2-7 | 356 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-aged1-0 | 355 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-aged1-1 | 355 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-aged1-2 | 355 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-aged1-3 | 355 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-aged1-4 | 355 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-aged1-5 | 355 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-aged1-6 | 356 | 97,057 (0.971) | 78,879 (0.789) |
| backlog-adp@verify-aged1-7 | 356 | 97,057 (0.971) | 78,879 (0.789) |
| adp-advertise | 578 | 22,280 (0.223) | 2,788 (0.028) |
| save-held | 722 | 95,427 (0.954) | 78,901 (0.789) |
| save-starved | 418 | 80,983 (0.810) | 78,325 (0.783) |
| acmp-noresp | 615 | 96,023 (0.960) | 78,879 (0.789) |
| save | 585 | 95,302 (0.953) | 78,426 (0.784) |
| srp | 271 | 22,280 (0.223) | 2,788 (0.028) |
| backlog | 265 | 22,280 (0.223) | 2,788 (0.028) |
| backlog-adp | 271 | 22,280 (0.223) | 2,788 (0.028) |
| backlog-adp-refill | 274 | 22,280 (0.223) | 2,788 (0.028) |
| backlog-owed | 276 | 22,280 (0.223) | 2,788 (0.028) |
| acmp-disc | 306 | 95,953 (0.960) | 78,879 (0.789) |
| maap | 163 | 22,280 (0.223) | 2,788 (0.028) |
| adp-link | 80 | 22,280 (0.223) | 2,788 (0.028) |
| adp-gm | 80 | 22,280 (0.223) | 2,788 (0.028) |
| adp-discover | 80 | 22,280 (0.223) | 2,788 (0.028) |
| control | 80 | 22,280 (0.223) | 2,788 (0.028) |
| aecp-fanout | 80 | 22,280 (0.223) | 2,788 (0.028) |
| acmp-cmd | 66 | 22,280 (0.223) | 2,788 (0.028) |
| aecp | 79 | 22,280 (0.223) | 2,788 (0.028) |
| aecp-largest-notice | 78 | 22,280 (0.223) | 2,788 (0.028) |
| datapath-events | 70 | 22,280 (0.223) | 2,788 (0.028) |
| fixture | 54 | 17,244 (0.172) | 2,788 (0.028) |

Longest pass that carries a step: 97,636 CPU cycles (0.976 ms), backlog-adp@program-1; longest step: 79,151 (0.792 ms), backlog-adp@program-3.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 16,166 | 0.162 | 20 | 20 | fits | 33,657 | 19 (14) | 0.883 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 440,156 | 4.402 | 20 | 20 | fits | 113,859 | 184 | 0.417 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 379,848 | 3.798 | 20 | 200 | fits | 151,879 | 214 | 0.400 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 493,091 | 4.931 | 20 | 200 | fits | 113,859 | 184 | 0.417 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 380,772 | 3.808 | 20 | 20 | fits | 151,879 | 214 | 0.400 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 493,795 | 4.938 | 20 | 20 | fits | 113,859 | 184 | 0.417 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 232,533 | 2.325 | 20 | 24 | fits | 145,062 | 145 | 0.385 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 383,422 | 3.834 | 20 | 24 | fits | 151,879 | 214 | 0.400 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 383,356 | 3.834 | 20 | 50 | fits | 151,879 | 214 | 0.400 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 496,819 | 4.968 | 20 | 50 | fits | 113,859 | 184 | 0.417 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 586,416 | 5.864 | 20 | 20 | fits | 89,663 | 24 | 0.809 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,118,526 | 11.185 | 20 | 20 | fits | 82,533 | 30 | 0.734 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 357,976 | 3.580 | 20 | 20 | fits | 117,504 | 175 | 0.408 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 300,829 | 3.008 | 20 | 200 | fits | 149,612 | 225 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 417,717 | 4.177 | 20 | 200 | fits | 117,504 | 175 | 0.408 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 301,753 | 3.018 | 20 | 20 | fits | 149,612 | 225 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 418,421 | 4.184 | 20 | 20 | fits | 117,504 | 175 | 0.408 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 155,781 | 1.558 | 20 | 24 | fits | 144,980 | 145 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 304,403 | 3.044 | 20 | 24 | fits | 149,612 | 225 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 304,337 | 3.043 | 20 | 50 | fits | 149,612 | 225 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 421,445 | 4.214 | 20 | 50 | fits | 117,504 | 175 | 0.408 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 511,098 | 5.111 | 20 | 20 | fits | 89,719 | 24 | 0.809 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 1,042,313 | 10.423 | 20 | 20 | fits | 89,620 | 28 | 0.662 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 367,933 | 3.679 | 20 | 20 | fits | 114,724 | 187 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 304,958 | 3.050 | 20 | 200 | fits | 150,877 | 210 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 419,066 | 4.191 | 20 | 200 | fits | 114,724 | 187 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 305,882 | 3.059 | 20 | 20 | fits | 150,877 | 210 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 419,770 | 4.198 | 20 | 20 | fits | 114,724 | 187 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 158,645 | 1.586 | 20 | 24 | fits | 144,980 | 145 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 308,532 | 3.085 | 20 | 24 | fits | 150,877 | 210 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 308,466 | 3.085 | 20 | 50 | fits | 150,877 | 210 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 422,794 | 4.228 | 20 | 50 | fits | 114,724 | 187 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 512,391 | 5.124 | 20 | 20 | fits | 89,663 | 24 | 0.809 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 1,044,417 | 10.444 | 20 | 20 | fits | 89,420 | 28 | 0.658 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 347,641 | 3.476 | 20 | 20 | fits | 117,910 | 176 | 0.411 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 290,494 | 2.905 | 20 | 200 | fits | 149,532 | 225 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 407,788 | 4.078 | 20 | 200 | fits | 117,910 | 176 | 0.411 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 291,418 | 2.914 | 20 | 20 | fits | 149,532 | 225 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 408,492 | 4.085 | 20 | 20 | fits | 117,910 | 176 | 0.411 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 145,526 | 1.455 | 20 | 24 | fits | 144,980 | 145 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 294,068 | 2.941 | 20 | 24 | fits | 149,532 | 225 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 294,002 | 2.940 | 20 | 50 | fits | 149,532 | 225 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 411,516 | 4.115 | 20 | 50 | fits | 117,910 | 176 | 0.411 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 513,654 | 5.137 | 20 | 20 | fits | 93,042 | 31 | 0.804 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 1,029,293 | 10.293 | 20 | 20 | fits | 76,323 | 24 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 370,128 | 3.701 | 20 | 20 | fits | 117,891 | 194 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 295,024 | 2.950 | 20 | 200 | fits | 151,198 | 211 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 421,314 | 4.213 | 20 | 200 | fits | 117,891 | 194 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 295,948 | 2.959 | 20 | 20 | fits | 151,198 | 211 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 422,018 | 4.220 | 20 | 20 | fits | 117,891 | 194 | 0.422 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 148,390 | 1.484 | 20 | 24 | fits | 144,980 | 145 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 298,598 | 2.986 | 20 | 24 | fits | 151,198 | 211 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 298,532 | 2.985 | 20 | 50 | fits | 151,198 | 211 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 425,042 | 4.250 | 20 | 50 | fits | 117,891 | 194 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 514,671 | 5.147 | 20 | 20 | fits | 89,695 | 24 | 0.809 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 1,030,123 | 10.301 | 20 | 20 | fits | 76,323 | 24 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 350,680 | 3.507 | 20 | 20 | fits | 122,327 | 193 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 302,686 | 3.027 | 20 | 200 | fits | 147,446 | 212 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 424,397 | 4.244 | 20 | 200 | fits | 122,327 | 193 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 303,610 | 3.036 | 20 | 20 | fits | 147,446 | 212 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 425,101 | 4.251 | 20 | 20 | fits | 122,327 | 193 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 151,420 | 1.514 | 20 | 24 | fits | 145,146 | 146 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 306,260 | 3.063 | 20 | 24 | fits | 147,446 | 212 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 306,194 | 3.062 | 20 | 50 | fits | 147,446 | 212 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 428,125 | 4.281 | 20 | 50 | fits | 122,327 | 193 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 509,207 | 5.092 | 20 | 20 | fits | 81,148 | 26 | 0.838 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 1,047,266 | 10.473 | 20 | 20 | fits | 81,926 | 31 | 0.752 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 373,990 | 3.740 | 20 | 20 | fits | 124,362 | 181 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 308,996 | 3.090 | 20 | 200 | fits | 150,982 | 230 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 432,742 | 4.327 | 20 | 200 | fits | 124,362 | 181 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 309,920 | 3.099 | 20 | 20 | fits | 150,982 | 230 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 433,446 | 4.334 | 20 | 20 | fits | 124,362 | 181 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 154,194 | 1.542 | 20 | 24 | fits | 145,056 | 146 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 312,570 | 3.126 | 20 | 24 | fits | 150,982 | 230 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 312,504 | 3.125 | 20 | 50 | fits | 150,982 | 230 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 436,470 | 4.365 | 20 | 50 | fits | 124,362 | 181 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 526,144 | 5.261 | 20 | 20 | fits | 89,740 | 24 | 0.809 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 1,050,849 | 10.508 | 20 | 20 | fits | 68,835 | 27 | 0.785 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 356,392 | 3.564 | 20 | 20 | fits | 122,769 | 196 | 0.399 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 294,129 | 2.941 | 20 | 200 | fits | 150,664 | 208 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 416,282 | 4.163 | 20 | 200 | fits | 122,769 | 196 | 0.399 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 295,053 | 2.951 | 20 | 20 | fits | 150,664 | 208 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 416,986 | 4.170 | 20 | 20 | fits | 122,769 | 196 | 0.399 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 148,029 | 1.480 | 20 | 24 | fits | 144,867 | 145 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 297,703 | 2.977 | 20 | 24 | fits | 150,664 | 208 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 297,637 | 2.976 | 20 | 50 | fits | 150,664 | 208 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 420,010 | 4.200 | 20 | 50 | fits | 122,769 | 196 | 0.399 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 509,709 | 5.097 | 20 | 20 | fits | 89,765 | 24 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 1,035,497 | 10.355 | 20 | 20 | fits | 76,340 | 24 | 0.696 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 367,142 | 3.671 | 20 | 20 | fits | 114,598 | 187 | 0.410 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 304,176 | 3.042 | 20 | 200 | fits | 150,753 | 210 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 418,158 | 4.182 | 20 | 200 | fits | 114,598 | 187 | 0.410 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 305,100 | 3.051 | 20 | 20 | fits | 150,753 | 210 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 418,862 | 4.189 | 20 | 20 | fits | 114,598 | 187 | 0.410 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 157,987 | 1.580 | 20 | 24 | fits | 145,246 | 145 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 307,750 | 3.078 | 20 | 24 | fits | 150,753 | 210 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 307,684 | 3.077 | 20 | 50 | fits | 150,753 | 210 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 421,886 | 4.219 | 20 | 50 | fits | 114,598 | 187 | 0.410 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 511,470 | 5.115 | 20 | 20 | fits | 89,650 | 25 | 0.809 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 1,042,477 | 10.425 | 20 | 20 | fits | 82,296 | 30 | 0.732 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 368,579 | 3.686 | 20 | 20 | fits | 117,975 | 194 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 293,234 | 2.932 | 20 | 200 | fits | 151,281 | 211 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 419,765 | 4.198 | 20 | 200 | fits | 117,975 | 194 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 294,158 | 2.942 | 20 | 20 | fits | 151,281 | 211 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 420,469 | 4.205 | 20 | 20 | fits | 117,975 | 194 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 146,517 | 1.465 | 20 | 24 | fits | 145,246 | 145 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 296,808 | 2.968 | 20 | 24 | fits | 151,281 | 211 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 296,742 | 2.967 | 20 | 50 | fits | 151,281 | 211 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 423,493 | 4.235 | 20 | 50 | fits | 117,975 | 194 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 512,984 | 5.130 | 20 | 20 | fits | 89,557 | 24 | 0.811 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 1,028,403 | 10.284 | 20 | 20 | fits | 76,323 | 24 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 361,184 | 3.612 | 20 | 20 | fits | 117,009 | 175 | 0.404 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 303,767 | 3.038 | 20 | 200 | fits | 149,559 | 225 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 420,160 | 4.202 | 20 | 200 | fits | 117,009 | 175 | 0.404 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 304,691 | 3.047 | 20 | 20 | fits | 149,559 | 225 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 420,864 | 4.209 | 20 | 20 | fits | 117,009 | 175 | 0.404 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 158,772 | 1.588 | 20 | 24 | fits | 145,487 | 145 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 307,341 | 3.073 | 20 | 24 | fits | 149,559 | 225 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 307,275 | 3.073 | 20 | 50 | fits | 149,559 | 225 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 423,888 | 4.239 | 20 | 50 | fits | 117,009 | 175 | 0.404 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 518,154 | 5.182 | 20 | 20 | fits | 94,332 | 30 | 0.809 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 1,042,861 | 10.429 | 20 | 20 | fits | 76,378 | 24 | 0.696 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 356,014 | 3.560 | 20 | 20 | fits | 122,581 | 196 | 0.402 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 292,937 | 2.929 | 20 | 200 | fits | 150,234 | 208 | 0.424 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 414,902 | 4.149 | 20 | 200 | fits | 122,581 | 196 | 0.402 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 293,861 | 2.939 | 20 | 20 | fits | 150,234 | 208 | 0.424 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 415,606 | 4.156 | 20 | 20 | fits | 122,581 | 196 | 0.402 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 147,267 | 1.473 | 20 | 24 | fits | 145,198 | 145 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 296,511 | 2.965 | 20 | 24 | fits | 150,234 | 208 | 0.424 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 296,445 | 2.964 | 20 | 50 | fits | 150,234 | 208 | 0.424 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 418,630 | 4.186 | 20 | 50 | fits | 122,581 | 196 | 0.402 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 508,109 | 5.081 | 20 | 20 | fits | 89,545 | 24 | 0.811 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 1,032,971 | 10.330 | 20 | 20 | fits | 76,311 | 24 | 0.694 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 369,786 | 3.698 | 20 | 20 | fits | 121,236 | 182 | 0.427 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 299,955 | 3.000 | 20 | 200 | fits | 150,152 | 226 | 0.400 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 429,580 | 4.296 | 20 | 200 | fits | 121,236 | 182 | 0.427 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 300,879 | 3.009 | 20 | 20 | fits | 150,152 | 226 | 0.400 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 430,284 | 4.303 | 20 | 20 | fits | 121,236 | 182 | 0.427 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 154,367 | 1.544 | 20 | 24 | fits | 145,279 | 145 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 303,529 | 3.035 | 20 | 24 | fits | 150,152 | 226 | 0.400 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 303,463 | 3.035 | 20 | 50 | fits | 150,152 | 226 | 0.400 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 433,308 | 4.333 | 20 | 50 | fits | 121,236 | 182 | 0.427 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 522,550 | 5.226 | 20 | 20 | fits | 89,308 | 24 | 0.809 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 1,037,075 | 10.371 | 20 | 20 | fits | 76,429 | 24 | 0.696 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 356,848 | 3.568 | 20 | 20 | fits | 117,806 | 175 | 0.410 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 299,367 | 2.994 | 20 | 200 | fits | 151,220 | 230 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 416,557 | 4.166 | 20 | 200 | fits | 117,806 | 175 | 0.410 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 300,291 | 3.003 | 20 | 20 | fits | 151,220 | 230 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 417,261 | 4.173 | 20 | 20 | fits | 117,806 | 175 | 0.410 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 144,189 | 1.442 | 20 | 24 | fits | 145,364 | 146 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 302,941 | 3.029 | 20 | 24 | fits | 151,220 | 230 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 302,875 | 3.029 | 20 | 50 | fits | 151,220 | 230 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 420,285 | 4.203 | 20 | 50 | fits | 117,806 | 175 | 0.410 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 509,707 | 5.097 | 20 | 20 | fits | 89,488 | 24 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 1,040,262 | 10.403 | 20 | 20 | fits | 81,816 | 31 | 0.748 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 351,626 | 3.516 | 20 | 20 | fits | 114,442 | 184 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 303,691 | 3.037 | 20 | 200 | fits | 151,953 | 214 | 0.402 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 417,517 | 4.175 | 20 | 200 | fits | 114,442 | 184 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 304,615 | 3.046 | 20 | 20 | fits | 151,953 | 214 | 0.402 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 418,221 | 4.182 | 20 | 20 | fits | 114,442 | 184 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 156,302 | 1.563 | 20 | 24 | fits | 145,194 | 145 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 307,265 | 3.073 | 20 | 24 | fits | 151,953 | 214 | 0.402 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 307,199 | 3.072 | 20 | 50 | fits | 151,953 | 214 | 0.402 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 421,245 | 4.212 | 20 | 50 | fits | 114,442 | 184 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 515,605 | 5.156 | 20 | 20 | fits | 94,426 | 30 | 0.809 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 1,040,704 | 10.407 | 20 | 20 | fits | 76,311 | 24 | 0.694 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 353,660 | 3.537 | 20 | 20 | fits | 123,424 | 197 | 0.404 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 291,195 | 2.912 | 20 | 200 | fits | 150,927 | 208 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 414,003 | 4.140 | 20 | 200 | fits | 123,424 | 197 | 0.404 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 292,119 | 2.921 | 20 | 20 | fits | 150,927 | 208 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 414,707 | 4.147 | 20 | 20 | fits | 123,424 | 197 | 0.404 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 144,832 | 1.448 | 20 | 24 | fits | 145,194 | 145 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 294,769 | 2.948 | 20 | 24 | fits | 150,927 | 208 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 294,703 | 2.947 | 20 | 50 | fits | 150,927 | 208 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 417,731 | 4.177 | 20 | 50 | fits | 123,424 | 197 | 0.404 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 519,932 | 5.199 | 20 | 20 | fits | 92,915 | 31 | 0.806 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 1,028,520 | 10.285 | 20 | 20 | fits | 62,500 | 20 | 0.731 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 385,514 | 3.855 | 20 | 20 | fits | 117,023 | 175 | 0.404 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 328,097 | 3.281 | 20 | 200 | fits | 149,635 | 225 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 444,504 | 4.445 | 20 | 200 | fits | 117,023 | 175 | 0.404 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 329,021 | 3.290 | 20 | 20 | fits | 149,635 | 225 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 445,208 | 4.452 | 20 | 20 | fits | 117,023 | 175 | 0.404 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 183,026 | 1.830 | 20 | 24 | fits | 145,217 | 145 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 331,671 | 3.317 | 20 | 24 | fits | 149,635 | 225 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 331,605 | 3.316 | 20 | 50 | fits | 149,635 | 225 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 448,232 | 4.482 | 20 | 50 | fits | 117,023 | 175 | 0.404 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 538,001 | 5.380 | 20 | 20 | fits | 89,835 | 24 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,068,804 | 10.688 | 20 | 20 | fits | 82,246 | 30 | 0.732 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 355,863 | 3.559 | 20 | 20 | fits | 117,370 | 175 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 298,733 | 2.987 | 20 | 200 | fits | 149,484 | 225 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 415,487 | 4.155 | 20 | 200 | fits | 117,370 | 175 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 299,657 | 2.997 | 20 | 20 | fits | 149,484 | 225 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 416,191 | 4.162 | 20 | 20 | fits | 117,370 | 175 | 0.406 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 153,813 | 1.538 | 20 | 24 | fits | 145,114 | 145 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 302,307 | 3.023 | 20 | 24 | fits | 149,484 | 225 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 302,241 | 3.022 | 20 | 50 | fits | 149,484 | 225 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 419,215 | 4.192 | 20 | 50 | fits | 117,370 | 175 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 508,984 | 5.090 | 20 | 20 | fits | 89,835 | 24 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 1,040,119 | 10.401 | 20 | 20 | fits | 89,681 | 28 | 0.664 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 365,180 | 3.652 | 20 | 20 | fits | 114,598 | 187 | 0.410 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 302,214 | 3.022 | 20 | 200 | fits | 150,749 | 210 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 416,196 | 4.162 | 20 | 200 | fits | 114,598 | 187 | 0.410 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 303,138 | 3.031 | 20 | 20 | fits | 150,749 | 210 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 416,900 | 4.169 | 20 | 20 | fits | 114,598 | 187 | 0.410 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 156,029 | 1.560 | 20 | 24 | fits | 145,114 | 145 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 305,788 | 3.058 | 20 | 24 | fits | 150,749 | 210 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 305,722 | 3.057 | 20 | 50 | fits | 150,749 | 210 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 419,924 | 4.199 | 20 | 50 | fits | 114,598 | 187 | 0.410 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 509,762 | 5.098 | 20 | 20 | fits | 89,904 | 25 | 0.808 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 1,041,001 | 10.410 | 20 | 20 | fits | 89,480 | 28 | 0.658 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 353,411 | 3.534 | 20 | 20 | fits | 114,833 | 185 | 0.427 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 305,538 | 3.055 | 20 | 200 | fits | 151,857 | 214 | 0.400 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 419,755 | 4.198 | 20 | 200 | fits | 114,833 | 185 | 0.427 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 306,462 | 3.065 | 20 | 20 | fits | 151,857 | 214 | 0.400 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 420,459 | 4.205 | 20 | 20 | fits | 114,833 | 185 | 0.427 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 158,245 | 1.582 | 20 | 24 | fits | 145,114 | 145 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 309,112 | 3.091 | 20 | 24 | fits | 151,857 | 214 | 0.400 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 309,046 | 3.090 | 20 | 50 | fits | 151,857 | 214 | 0.400 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 423,483 | 4.235 | 20 | 50 | fits | 114,833 | 185 | 0.427 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 525,901 | 5.259 | 20 | 20 | fits | 93,165 | 31 | 0.806 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 1,041,523 | 10.415 | 20 | 20 | fits | 76,323 | 24 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 366,406 | 3.664 | 20 | 20 | fits | 117,939 | 194 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 291,098 | 2.911 | 20 | 200 | fits | 151,103 | 211 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 417,592 | 4.176 | 20 | 200 | fits | 117,939 | 194 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 292,022 | 2.920 | 20 | 20 | fits | 151,103 | 211 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 418,296 | 4.183 | 20 | 20 | fits | 117,939 | 194 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 144,559 | 1.446 | 20 | 24 | fits | 145,114 | 145 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 294,672 | 2.947 | 20 | 24 | fits | 151,103 | 211 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 294,606 | 2.946 | 20 | 50 | fits | 151,103 | 211 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 421,320 | 4.213 | 20 | 50 | fits | 117,939 | 194 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 515,941 | 5.159 | 20 | 20 | fits | 94,687 | 30 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 1,024,198 | 10.242 | 20 | 20 | fits | 62,592 | 21 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 354,043 | 3.540 | 20 | 20 | fits | 130,067 | 199 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 298,260 | 2.983 | 20 | 200 | fits | 147,484 | 212 | 0.400 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 427,711 | 4.277 | 20 | 200 | fits | 130,067 | 199 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 299,184 | 2.992 | 20 | 20 | fits | 147,484 | 212 | 0.400 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 428,415 | 4.284 | 20 | 20 | fits | 130,067 | 199 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 146,905 | 1.469 | 20 | 24 | fits | 145,244 | 146 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 301,834 | 3.018 | 20 | 24 | fits | 147,484 | 212 | 0.400 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 301,768 | 3.018 | 20 | 50 | fits | 147,484 | 212 | 0.400 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 431,439 | 4.314 | 20 | 50 | fits | 130,067 | 199 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 521,262 | 5.213 | 20 | 20 | fits | 89,889 | 24 | 0.811 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 1,046,242 | 10.462 | 20 | 20 | fits | 68,898 | 27 | 0.785 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 365,220 | 3.652 | 20 | 20 | fits | 122,693 | 196 | 0.403 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 302,148 | 3.021 | 20 | 200 | fits | 150,242 | 208 | 0.424 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 424,225 | 4.242 | 20 | 200 | fits | 122,693 | 196 | 0.403 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 303,072 | 3.031 | 20 | 20 | fits | 150,242 | 208 | 0.424 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 424,929 | 4.249 | 20 | 20 | fits | 122,693 | 196 | 0.403 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 156,470 | 1.565 | 20 | 24 | fits | 145,222 | 145 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 305,722 | 3.057 | 20 | 24 | fits | 150,242 | 208 | 0.424 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 305,656 | 3.057 | 20 | 50 | fits | 150,242 | 208 | 0.424 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 427,953 | 4.280 | 20 | 50 | fits | 122,693 | 196 | 0.403 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 517,710 | 5.177 | 20 | 20 | fits | 89,823 | 24 | 0.811 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 1,042,736 | 10.427 | 20 | 20 | fits | 76,378 | 24 | 0.696 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 374,726 | 3.747 | 20 | 20 | fits | 122,664 | 196 | 0.398 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 305,188 | 3.052 | 20 | 200 | fits | 150,833 | 208 | 0.430 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 427,236 | 4.272 | 20 | 200 | fits | 122,664 | 196 | 0.398 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 306,112 | 3.061 | 20 | 20 | fits | 150,833 | 208 | 0.430 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 427,940 | 4.279 | 20 | 20 | fits | 122,664 | 196 | 0.398 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 158,919 | 1.589 | 20 | 24 | fits | 145,198 | 145 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 308,762 | 3.088 | 20 | 24 | fits | 150,833 | 208 | 0.430 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 308,696 | 3.087 | 20 | 50 | fits | 150,833 | 208 | 0.430 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 430,964 | 4.310 | 20 | 50 | fits | 122,664 | 196 | 0.398 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 520,846 | 5.208 | 20 | 20 | fits | 89,948 | 24 | 0.811 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 1,045,775 | 10.458 | 20 | 20 | fits | 76,311 | 24 | 0.694 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 349,673 | 3.497 | 20 | 20 | fits | 119,619 | 182 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 289,797 | 2.898 | 20 | 200 | fits | 151,266 | 230 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 408,800 | 4.088 | 20 | 200 | fits | 119,619 | 182 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 290,721 | 2.907 | 20 | 20 | fits | 151,266 | 230 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 409,504 | 4.095 | 20 | 20 | fits | 119,619 | 182 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 143,095 | 1.431 | 20 | 24 | fits | 149,409 | 147 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 293,371 | 2.934 | 20 | 24 | fits | 151,266 | 230 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 293,305 | 2.933 | 20 | 50 | fits | 151,266 | 230 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 412,528 | 4.125 | 20 | 50 | fits | 119,619 | 182 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 514,551 | 5.146 | 20 | 20 | fits | 92,441 | 31 | 0.805 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 1,029,090 | 10.291 | 20 | 20 | fits | 69,105 | 26 | 0.769 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 362,850 | 3.628 | 20 | 20 | fits | 120,950 | 182 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 292,577 | 2.926 | 20 | 200 | fits | 149,831 | 226 | 0.400 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 422,562 | 4.226 | 20 | 200 | fits | 120,950 | 182 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 293,501 | 2.935 | 20 | 20 | fits | 149,831 | 226 | 0.400 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 423,266 | 4.233 | 20 | 20 | fits | 120,950 | 182 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 147,310 | 1.473 | 20 | 24 | fits | 144,784 | 142 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 296,151 | 2.962 | 20 | 24 | fits | 149,831 | 226 | 0.400 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 296,085 | 2.961 | 20 | 50 | fits | 149,831 | 226 | 0.400 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 426,290 | 4.263 | 20 | 50 | fits | 120,950 | 182 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 515,344 | 5.153 | 20 | 20 | fits | 89,120 | 24 | 0.807 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 1,110,831 | 11.108 | 20 | 20 | fits | 80,967 | 32 | 0.722 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 370,738 | 3.707 | 20 | 20 | fits | 114,688 | 187 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 307,785 | 3.078 | 20 | 200 | fits | 152,544 | 215 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 421,857 | 4.219 | 20 | 200 | fits | 114,688 | 187 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 308,709 | 3.087 | 20 | 20 | fits | 152,544 | 215 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 422,561 | 4.226 | 20 | 20 | fits | 114,688 | 187 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 150,497 | 1.505 | 20 | 24 | fits | 144,963 | 143 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 311,359 | 3.114 | 20 | 24 | fits | 152,544 | 215 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 311,293 | 3.113 | 20 | 50 | fits | 152,544 | 215 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 425,585 | 4.256 | 20 | 50 | fits | 114,688 | 187 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 514,659 | 5.147 | 20 | 20 | fits | 89,140 | 24 | 0.807 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,122,302 | 11.223 | 20 | 20 | fits | 89,785 | 28 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 355,723 | 3.557 | 20 | 20 | fits | 117,230 | 175 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 298,645 | 2.986 | 20 | 200 | fits | 149,526 | 225 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 415,259 | 4.153 | 20 | 200 | fits | 117,230 | 175 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 299,569 | 2.996 | 20 | 20 | fits | 149,526 | 225 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 415,963 | 4.160 | 20 | 20 | fits | 117,230 | 175 | 0.406 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 153,683 | 1.537 | 20 | 24 | fits | 144,716 | 142 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 302,219 | 3.022 | 20 | 24 | fits | 149,526 | 225 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 302,153 | 3.022 | 20 | 50 | fits | 149,526 | 225 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 418,987 | 4.190 | 20 | 50 | fits | 117,230 | 175 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 508,278 | 5.083 | 20 | 20 | fits | 89,357 | 24 | 0.809 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,116,485 | 11.165 | 20 | 20 | fits | 89,433 | 28 | 0.658 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 365,864 | 3.659 | 20 | 20 | fits | 114,474 | 187 | 0.410 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 302,966 | 3.030 | 20 | 200 | fits | 150,791 | 210 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 416,824 | 4.168 | 20 | 200 | fits | 114,474 | 187 | 0.410 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 303,890 | 3.039 | 20 | 20 | fits | 150,791 | 210 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 417,528 | 4.175 | 20 | 20 | fits | 114,474 | 187 | 0.410 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 156,739 | 1.567 | 20 | 24 | fits | 144,772 | 142 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 306,540 | 3.065 | 20 | 24 | fits | 150,791 | 210 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 306,474 | 3.065 | 20 | 50 | fits | 150,791 | 210 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 420,552 | 4.206 | 20 | 50 | fits | 114,474 | 187 | 0.410 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 509,787 | 5.098 | 20 | 20 | fits | 89,301 | 24 | 0.809 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,118,582 | 11.186 | 20 | 20 | fits | 89,374 | 28 | 0.658 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 346,077 | 3.461 | 20 | 20 | fits | 117,283 | 175 | 0.407 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 288,946 | 2.889 | 20 | 200 | fits | 150,816 | 230 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 405,613 | 4.056 | 20 | 200 | fits | 117,283 | 175 | 0.407 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 289,870 | 2.899 | 20 | 20 | fits | 150,816 | 230 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 406,317 | 4.063 | 20 | 20 | fits | 117,283 | 175 | 0.407 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 142,694 | 1.427 | 20 | 24 | fits | 144,772 | 142 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 292,520 | 2.925 | 20 | 24 | fits | 150,816 | 230 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 292,454 | 2.925 | 20 | 50 | fits | 150,816 | 230 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 409,341 | 4.093 | 20 | 50 | fits | 117,283 | 175 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 503,561 | 5.036 | 20 | 20 | fits | 94,286 | 30 | 0.808 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,105,966 | 11.060 | 20 | 20 | fits | 76,273 | 24 | 0.694 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 363,554 | 3.636 | 20 | 20 | fits | 122,429 | 194 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 292,922 | 2.929 | 20 | 200 | fits | 150,732 | 210 | 0.406 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 414,735 | 4.147 | 20 | 200 | fits | 122,429 | 194 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 293,846 | 2.938 | 20 | 20 | fits | 150,732 | 210 | 0.406 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 415,439 | 4.154 | 20 | 20 | fits | 122,429 | 194 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 146,754 | 1.468 | 20 | 24 | fits | 144,772 | 142 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 296,496 | 2.965 | 20 | 24 | fits | 150,732 | 210 | 0.406 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 296,430 | 2.964 | 20 | 50 | fits | 150,732 | 210 | 0.406 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 418,463 | 4.185 | 20 | 50 | fits | 122,429 | 194 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 596,041 | 5.960 | 20 | 20 | fits | 92,827 | 31 | 0.804 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,104,221 | 11.042 | 20 | 20 | fits | 62,460 | 20 | 0.731 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 447,075 | 4.471 | 20 | 20 | fits | 126,245 | 202 | 0.416 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 296,635 | 2.966 | 20 | 200 | fits | 151,437 | 209 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 506,955 | 5.070 | 20 | 200 | fits | 126,245 | 202 | 0.416 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 297,559 | 2.976 | 20 | 20 | fits | 151,437 | 209 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 507,659 | 5.077 | 20 | 20 | fits | 126,245 | 202 | 0.416 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 149,762 | 1.498 | 20 | 24 | fits | 144,772 | 142 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 300,209 | 3.002 | 20 | 24 | fits | 151,437 | 209 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 300,143 | 3.001 | 20 | 50 | fits | 151,437 | 209 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 510,683 | 5.107 | 20 | 50 | fits | 126,245 | 202 | 0.416 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 600,129 | 6.001 | 20 | 20 | fits | 89,512 | 24 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,108,061 | 11.081 | 20 | 20 | fits | 62,460 | 20 | 0.731 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 349,791 | 3.498 | 20 | 20 | fits | 114,456 | 184 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 301,901 | 3.019 | 20 | 200 | fits | 152,146 | 214 | 0.402 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 415,741 | 4.157 | 20 | 200 | fits | 114,456 | 184 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 302,825 | 3.028 | 20 | 20 | fits | 152,146 | 214 | 0.402 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 416,445 | 4.164 | 20 | 20 | fits | 114,456 | 184 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 154,319 | 1.543 | 20 | 24 | fits | 144,452 | 142 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 305,475 | 3.055 | 20 | 24 | fits | 152,146 | 214 | 0.402 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 305,409 | 3.054 | 20 | 50 | fits | 152,146 | 214 | 0.402 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 419,469 | 4.195 | 20 | 50 | fits | 114,456 | 184 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 508,941 | 5.089 | 20 | 20 | fits | 89,538 | 24 | 0.807 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 1,045,239 | 10.452 | 20 | 20 | fits | 87,852 | 30 | 0.746 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 351,759 | 3.518 | 20 | 20 | fits | 114,834 | 187 | 0.413 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 288,784 | 2.888 | 20 | 200 | fits | 152,148 | 215 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 403,002 | 4.030 | 20 | 200 | fits | 114,834 | 187 | 0.413 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 289,708 | 2.897 | 20 | 20 | fits | 152,148 | 215 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 403,706 | 4.037 | 20 | 20 | fits | 114,834 | 187 | 0.413 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 141,200 | 1.412 | 20 | 24 | fits | 144,452 | 142 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 292,358 | 2.924 | 20 | 24 | fits | 152,148 | 215 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 292,292 | 2.923 | 20 | 50 | fits | 152,148 | 215 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 406,730 | 4.067 | 20 | 50 | fits | 114,834 | 187 | 0.413 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 496,222 | 4.962 | 20 | 20 | fits | 89,558 | 25 | 0.806 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 1,067,986 | 10.680 | 20 | 20 | fits | 92,340 | 29 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 336,988 | 3.370 | 20 | 20 | fits | 125,647 | 200 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 284,867 | 2.849 | 20 | 200 | fits | 147,136 | 212 | 0.400 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 409,898 | 4.099 | 20 | 200 | fits | 125,647 | 200 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 285,791 | 2.858 | 20 | 20 | fits | 147,136 | 212 | 0.400 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 410,602 | 4.106 | 20 | 20 | fits | 125,647 | 200 | 0.418 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 142,295 | 1.423 | 20 | 24 | fits | 144,452 | 142 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 288,441 | 2.884 | 20 | 24 | fits | 147,136 | 212 | 0.400 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 288,375 | 2.884 | 20 | 50 | fits | 147,136 | 212 | 0.400 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 413,626 | 4.136 | 20 | 50 | fits | 125,647 | 200 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 512,951 | 5.130 | 20 | 20 | fits | 90,125 | 25 | 0.807 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 1,100,808 | 11.008 | 20 | 20 | fits | 76,652 | 24 | 0.704 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 361,387 | 3.614 | 20 | 20 | fits | 120,155 | 182 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 291,971 | 2.920 | 20 | 200 | fits | 149,607 | 226 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 420,356 | 4.204 | 20 | 200 | fits | 120,155 | 182 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 292,895 | 2.929 | 20 | 20 | fits | 149,607 | 226 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 421,060 | 4.211 | 20 | 20 | fits | 120,155 | 182 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 146,928 | 1.469 | 20 | 24 | fits | 144,452 | 142 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 295,545 | 2.955 | 20 | 24 | fits | 149,607 | 226 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 295,479 | 2.955 | 20 | 50 | fits | 149,607 | 226 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 424,084 | 4.241 | 20 | 50 | fits | 120,155 | 182 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 513,416 | 5.134 | 20 | 20 | fits | 89,398 | 24 | 0.806 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 1,100,606 | 11.006 | 20 | 20 | fits | 76,424 | 25 | 0.694 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 361,418 | 3.614 | 20 | 20 | fits | 121,880 | 193 | 0.407 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 300,797 | 3.008 | 20 | 200 | fits | 147,333 | 212 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 422,061 | 4.221 | 20 | 200 | fits | 121,880 | 193 | 0.407 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 301,721 | 3.017 | 20 | 20 | fits | 147,333 | 212 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 422,765 | 4.228 | 20 | 20 | fits | 121,880 | 193 | 0.407 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 149,850 | 1.498 | 20 | 24 | fits | 144,510 | 143 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 304,371 | 3.044 | 20 | 24 | fits | 147,333 | 212 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 304,305 | 3.043 | 20 | 50 | fits | 147,333 | 212 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 425,789 | 4.258 | 20 | 50 | fits | 121,880 | 193 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 515,279 | 5.153 | 20 | 20 | fits | 89,556 | 24 | 0.808 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 1,119,910 | 11.199 | 20 | 20 | fits | 91,424 | 29 | 0.694 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 353,862 | 3.539 | 20 | 20 | fits | 116,836 | 175 | 0.405 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 296,565 | 2.966 | 20 | 200 | fits | 149,432 | 225 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 412,785 | 4.128 | 20 | 200 | fits | 116,836 | 175 | 0.405 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 297,489 | 2.975 | 20 | 20 | fits | 149,432 | 225 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 413,489 | 4.135 | 20 | 20 | fits | 116,836 | 175 | 0.405 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 151,697 | 1.517 | 20 | 24 | fits | 144,333 | 142 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 300,139 | 3.001 | 20 | 24 | fits | 149,432 | 225 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 300,073 | 3.001 | 20 | 50 | fits | 149,432 | 225 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 416,513 | 4.165 | 20 | 50 | fits | 116,836 | 175 | 0.405 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 502,556 | 5.026 | 20 | 20 | fits | 86,109 | 26 | 0.842 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 1,106,992 | 11.070 | 20 | 20 | fits | 89,366 | 28 | 0.657 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 377,377 | 3.774 | 20 | 20 | fits | 130,227 | 190 | 0.477 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 301,918 | 3.019 | 20 | 200 | fits | 151,777 | 214 | 0.401 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 431,529 | 4.315 | 20 | 200 | fits | 130,227 | 190 | 0.477 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 302,842 | 3.028 | 20 | 20 | fits | 151,777 | 214 | 0.401 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 432,233 | 4.322 | 20 | 20 | fits | 130,227 | 190 | 0.477 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 154,705 | 1.547 | 20 | 24 | fits | 144,333 | 142 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 305,492 | 3.055 | 20 | 24 | fits | 151,777 | 214 | 0.401 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 305,426 | 3.054 | 20 | 50 | fits | 151,777 | 214 | 0.401 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 435,257 | 4.353 | 20 | 50 | fits | 130,227 | 190 | 0.477 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 553,895 | 5.539 | 20 | 20 | fits | 89,587 | 25 | 0.806 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 1,110,829 | 11.108 | 20 | 20 | fits | 76,265 | 24 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 360,155 | 3.602 | 20 | 20 | fits | 132,961 | 181 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 287,988 | 2.880 | 20 | 200 | fits | 150,840 | 230 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 420,333 | 4.203 | 20 | 200 | fits | 132,961 | 181 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 288,912 | 2.889 | 20 | 20 | fits | 150,840 | 230 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 421,037 | 4.210 | 20 | 20 | fits | 132,961 | 181 | 0.461 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 141,712 | 1.417 | 20 | 24 | fits | 144,333 | 142 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 291,562 | 2.916 | 20 | 24 | fits | 150,840 | 230 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 291,496 | 2.915 | 20 | 50 | fits | 150,840 | 230 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 424,061 | 4.241 | 20 | 50 | fits | 132,961 | 181 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 542,637 | 5.426 | 20 | 20 | fits | 89,536 | 26 | 0.803 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 1,097,726 | 10.977 | 20 | 20 | fits | 76,174 | 24 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 365,620 | 3.656 | 20 | 20 | fits | 117,748 | 193 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 290,588 | 2.906 | 20 | 200 | fits | 152,482 | 216 | 0.406 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 416,738 | 4.167 | 20 | 200 | fits | 117,748 | 193 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 291,512 | 2.915 | 20 | 20 | fits | 152,482 | 216 | 0.406 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 417,442 | 4.174 | 20 | 20 | fits | 117,748 | 193 | 0.422 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 142,670 | 1.427 | 20 | 24 | fits | 145,102 | 142 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 294,162 | 2.942 | 20 | 24 | fits | 152,482 | 216 | 0.406 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 294,096 | 2.941 | 20 | 50 | fits | 152,482 | 216 | 0.406 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 420,466 | 4.205 | 20 | 50 | fits | 117,748 | 193 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 509,853 | 5.099 | 20 | 20 | fits | 89,453 | 24 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 1,024,185 | 10.242 | 20 | 20 | fits | 69,304 | 26 | 0.769 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 345,056 | 3.451 | 20 | 20 | fits | 122,375 | 193 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 297,014 | 2.970 | 20 | 200 | fits | 147,587 | 212 | 0.401 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 418,773 | 4.188 | 20 | 200 | fits | 122,375 | 193 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 297,938 | 2.979 | 20 | 20 | fits | 147,587 | 212 | 0.401 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 419,477 | 4.195 | 20 | 20 | fits | 122,375 | 193 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 145,662 | 1.457 | 20 | 24 | fits | 145,230 | 143 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 300,588 | 3.006 | 20 | 24 | fits | 147,587 | 212 | 0.401 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 300,522 | 3.005 | 20 | 50 | fits | 147,587 | 212 | 0.401 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 422,501 | 4.225 | 20 | 50 | fits | 122,375 | 193 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 511,925 | 5.119 | 20 | 20 | fits | 89,490 | 24 | 0.811 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 1,121,867 | 11.219 | 20 | 20 | fits | 82,331 | 31 | 0.755 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 356,839 | 3.568 | 20 | 20 | fits | 114,705 | 187 | 0.411 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 293,869 | 2.939 | 20 | 200 | fits | 150,796 | 210 | 0.406 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 407,958 | 4.080 | 20 | 200 | fits | 114,705 | 187 | 0.411 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 294,793 | 2.948 | 20 | 20 | fits | 150,796 | 210 | 0.406 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 408,662 | 4.087 | 20 | 20 | fits | 114,705 | 187 | 0.411 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 147,637 | 1.476 | 20 | 24 | fits | 144,999 | 142 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 297,443 | 2.974 | 20 | 24 | fits | 150,796 | 210 | 0.406 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 297,377 | 2.974 | 20 | 50 | fits | 150,796 | 210 | 0.406 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 411,686 | 4.117 | 20 | 50 | fits | 114,705 | 187 | 0.411 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 501,000 | 5.010 | 20 | 20 | fits | 89,380 | 24 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,110,131 | 11.101 | 20 | 20 | fits | 76,350 | 24 | 0.696 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 345,998 | 3.460 | 20 | 20 | fits | 114,448 | 184 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 298,113 | 2.981 | 20 | 200 | fits | 151,904 | 214 | 0.402 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 411,945 | 4.119 | 20 | 200 | fits | 114,448 | 184 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 299,037 | 2.990 | 20 | 20 | fits | 151,904 | 214 | 0.402 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 412,649 | 4.126 | 20 | 20 | fits | 114,448 | 184 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 150,773 | 1.508 | 20 | 24 | fits | 144,999 | 142 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 301,687 | 3.017 | 20 | 24 | fits | 151,904 | 214 | 0.402 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 301,621 | 3.016 | 20 | 50 | fits | 151,904 | 214 | 0.402 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 415,673 | 4.157 | 20 | 50 | fits | 114,448 | 184 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 504,987 | 5.050 | 20 | 20 | fits | 89,380 | 24 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,114,137 | 11.141 | 20 | 20 | fits | 76,166 | 24 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 356,254 | 3.563 | 20 | 20 | fits | 116,956 | 175 | 0.403 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 298,890 | 2.989 | 20 | 200 | fits | 149,545 | 225 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 415,230 | 4.152 | 20 | 200 | fits | 116,956 | 175 | 0.403 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 299,814 | 2.998 | 20 | 20 | fits | 149,545 | 225 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 415,934 | 4.159 | 20 | 20 | fits | 116,956 | 175 | 0.403 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 153,909 | 1.539 | 20 | 24 | fits | 144,999 | 142 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 302,464 | 3.025 | 20 | 24 | fits | 149,545 | 225 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 302,398 | 3.024 | 20 | 50 | fits | 149,545 | 225 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 418,958 | 4.190 | 20 | 50 | fits | 116,956 | 175 | 0.403 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 508,453 | 5.085 | 20 | 20 | fits | 89,561 | 25 | 0.808 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,117,590 | 11.176 | 20 | 20 | fits | 76,166 | 24 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 364,674 | 3.647 | 20 | 20 | fits | 114,199 | 185 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 304,371 | 3.044 | 20 | 200 | fits | 151,890 | 214 | 0.402 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 417,954 | 4.180 | 20 | 200 | fits | 114,199 | 185 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 305,295 | 3.053 | 20 | 20 | fits | 151,890 | 214 | 0.402 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 418,658 | 4.187 | 20 | 20 | fits | 114,199 | 185 | 0.418 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 157,045 | 1.570 | 20 | 24 | fits | 144,999 | 142 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 307,945 | 3.079 | 20 | 24 | fits | 151,890 | 214 | 0.402 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 307,879 | 3.079 | 20 | 50 | fits | 151,890 | 214 | 0.402 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 421,682 | 4.217 | 20 | 50 | fits | 114,199 | 185 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 513,483 | 5.135 | 20 | 20 | fits | 82,764 | 33 | 0.824 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,116,467 | 11.165 | 20 | 20 | fits | 76,311 | 24 | 0.694 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 365,952 | 3.660 | 20 | 20 | fits | 127,239 | 187 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 289,521 | 2.895 | 20 | 200 | fits | 151,172 | 231 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 425,000 | 4.250 | 20 | 200 | fits | 127,239 | 187 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 290,445 | 2.904 | 20 | 20 | fits | 151,172 | 231 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 425,704 | 4.257 | 20 | 20 | fits | 127,239 | 187 | 0.430 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 142,913 | 1.429 | 20 | 24 | fits | 144,999 | 142 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 293,095 | 2.931 | 20 | 24 | fits | 151,172 | 231 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 293,029 | 2.930 | 20 | 50 | fits | 151,172 | 231 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 428,728 | 4.287 | 20 | 50 | fits | 127,239 | 187 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 598,159 | 5.982 | 20 | 20 | fits | 89,047 | 25 | 0.802 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,106,765 | 11.068 | 20 | 20 | fits | 62,642 | 21 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 454,463 | 4.545 | 20 | 20 | fits | 129,752 | 224 | 0.391 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 297,560 | 2.976 | 20 | 200 | fits | 146,413 | 185 | 0.443 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 507,214 | 5.072 | 20 | 200 | fits | 129,752 | 224 | 0.391 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 298,484 | 2.985 | 20 | 20 | fits | 146,413 | 185 | 0.443 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 507,918 | 5.079 | 20 | 20 | fits | 129,752 | 224 | 0.391 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 147,461 | 1.475 | 20 | 24 | fits | 145,160 | 143 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 301,134 | 3.011 | 20 | 24 | fits | 146,413 | 185 | 0.443 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 301,068 | 3.011 | 20 | 50 | fits | 146,413 | 185 | 0.443 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 510,942 | 5.109 | 20 | 50 | fits | 129,752 | 224 | 0.391 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 600,358 | 6.004 | 20 | 20 | fits | 89,482 | 24 | 0.811 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,125,671 | 11.257 | 20 | 20 | fits | 76,497 | 24 | 0.698 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 355,163 | 3.552 | 20 | 20 | fits | 114,199 | 185 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 294,860 | 2.949 | 20 | 200 | fits | 152,045 | 214 | 0.402 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 408,443 | 4.084 | 20 | 200 | fits | 114,199 | 185 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 295,784 | 2.958 | 20 | 20 | fits | 152,045 | 214 | 0.402 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 409,147 | 4.091 | 20 | 20 | fits | 114,199 | 185 | 0.418 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 147,379 | 1.474 | 20 | 24 | fits | 144,999 | 142 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 298,434 | 2.984 | 20 | 24 | fits | 152,045 | 214 | 0.402 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 298,368 | 2.984 | 20 | 50 | fits | 152,045 | 214 | 0.402 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 412,171 | 4.122 | 20 | 50 | fits | 114,199 | 185 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 514,241 | 5.142 | 20 | 20 | fits | 92,921 | 31 | 0.807 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 1,028,941 | 10.289 | 20 | 20 | fits | 69,264 | 26 | 0.769 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 365,459 | 3.655 | 20 | 20 | fits | 121,145 | 182 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 295,831 | 2.958 | 20 | 200 | fits | 149,880 | 226 | 0.400 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 425,300 | 4.253 | 20 | 200 | fits | 121,145 | 182 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 296,755 | 2.968 | 20 | 20 | fits | 149,880 | 226 | 0.400 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 426,004 | 4.260 | 20 | 20 | fits | 121,145 | 182 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 150,515 | 1.505 | 20 | 24 | fits | 144,999 | 142 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 299,405 | 2.994 | 20 | 24 | fits | 149,880 | 226 | 0.400 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 299,339 | 2.993 | 20 | 50 | fits | 149,880 | 226 | 0.400 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 429,028 | 4.290 | 20 | 50 | fits | 121,145 | 182 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 518,314 | 5.183 | 20 | 20 | fits | 89,352 | 24 | 0.809 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 1,032,933 | 10.329 | 20 | 20 | fits | 76,523 | 25 | 0.694 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 373,056 | 3.731 | 20 | 20 | fits | 114,742 | 187 | 0.411 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 310,031 | 3.100 | 20 | 200 | fits | 152,519 | 215 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 424,157 | 4.242 | 20 | 200 | fits | 114,742 | 187 | 0.411 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 310,955 | 3.110 | 20 | 20 | fits | 152,519 | 215 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 424,861 | 4.249 | 20 | 20 | fits | 114,742 | 187 | 0.411 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 153,830 | 1.538 | 20 | 24 | fits | 145,178 | 143 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 313,605 | 3.136 | 20 | 24 | fits | 152,519 | 215 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 313,539 | 3.135 | 20 | 50 | fits | 152,519 | 215 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 427,885 | 4.279 | 20 | 50 | fits | 114,742 | 187 | 0.411 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 517,295 | 5.173 | 20 | 20 | fits | 89,476 | 24 | 0.811 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 1,047,854 | 10.479 | 20 | 20 | fits | 81,816 | 31 | 0.748 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 357,933 | 3.579 | 20 | 20 | fits | 117,526 | 175 | 0.408 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 300,791 | 3.008 | 20 | 200 | fits | 149,607 | 225 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 417,701 | 4.177 | 20 | 200 | fits | 117,526 | 175 | 0.408 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 301,715 | 3.017 | 20 | 20 | fits | 149,607 | 225 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 418,405 | 4.184 | 20 | 20 | fits | 117,526 | 175 | 0.408 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 155,748 | 1.557 | 20 | 24 | fits | 144,892 | 142 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 304,365 | 3.044 | 20 | 24 | fits | 149,607 | 225 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 304,299 | 3.043 | 20 | 50 | fits | 149,607 | 225 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 421,429 | 4.214 | 20 | 50 | fits | 117,526 | 175 | 0.408 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 510,843 | 5.108 | 20 | 20 | fits | 89,480 | 24 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 1,041,943 | 10.419 | 20 | 20 | fits | 89,487 | 28 | 0.660 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 346,019 | 3.460 | 20 | 20 | fits | 121,852 | 193 | 0.405 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 285,507 | 2.855 | 20 | 200 | fits | 147,156 | 212 | 0.402 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 406,743 | 4.067 | 20 | 200 | fits | 121,852 | 193 | 0.405 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 286,431 | 2.864 | 20 | 20 | fits | 147,156 | 212 | 0.402 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 407,447 | 4.074 | 20 | 20 | fits | 121,852 | 193 | 0.405 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 142,915 | 1.429 | 20 | 24 | fits | 145,031 | 142 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 289,081 | 2.891 | 20 | 24 | fits | 147,156 | 212 | 0.402 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 289,015 | 2.890 | 20 | 50 | fits | 147,156 | 212 | 0.402 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 410,471 | 4.105 | 20 | 50 | fits | 121,852 | 193 | 0.405 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 499,887 | 4.999 | 20 | 20 | fits | 89,482 | 24 | 0.811 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 1,031,336 | 10.313 | 20 | 20 | fits | 89,420 | 28 | 0.658 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 348,230 | 3.482 | 20 | 20 | fits | 117,579 | 175 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 291,035 | 2.910 | 20 | 200 | fits | 149,548 | 225 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 407,998 | 4.080 | 20 | 200 | fits | 117,579 | 175 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 291,959 | 2.920 | 20 | 20 | fits | 149,548 | 225 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 408,702 | 4.087 | 20 | 20 | fits | 117,579 | 175 | 0.409 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 146,051 | 1.461 | 20 | 24 | fits | 145,031 | 142 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 294,609 | 2.946 | 20 | 24 | fits | 149,548 | 225 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 294,543 | 2.945 | 20 | 50 | fits | 149,548 | 225 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 411,726 | 4.117 | 20 | 50 | fits | 117,579 | 175 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 505,992 | 5.060 | 20 | 20 | fits | 94,332 | 30 | 0.809 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 1,030,894 | 10.309 | 20 | 20 | fits | 76,311 | 24 | 0.694 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 366,160 | 3.662 | 20 | 20 | fits | 122,680 | 194 | 0.434 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 295,436 | 2.954 | 20 | 200 | fits | 150,813 | 210 | 0.406 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 417,500 | 4.175 | 20 | 200 | fits | 122,680 | 194 | 0.434 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 296,360 | 2.964 | 20 | 20 | fits | 150,813 | 210 | 0.406 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 418,204 | 4.182 | 20 | 20 | fits | 122,680 | 194 | 0.434 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 149,187 | 1.492 | 20 | 24 | fits | 145,031 | 142 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 299,010 | 2.990 | 20 | 24 | fits | 150,813 | 210 | 0.406 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 298,944 | 2.989 | 20 | 50 | fits | 150,813 | 210 | 0.406 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 421,228 | 4.212 | 20 | 50 | fits | 122,680 | 194 | 0.434 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 523,120 | 5.231 | 20 | 20 | fits | 92,778 | 31 | 0.806 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 1,030,842 | 10.308 | 20 | 20 | fits | 62,355 | 20 | 0.728 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 373,514 | 3.735 | 20 | 20 | fits | 126,193 | 202 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 299,021 | 2.990 | 20 | 200 | fits | 151,262 | 209 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 433,538 | 4.335 | 20 | 200 | fits | 126,193 | 202 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 299,945 | 2.999 | 20 | 20 | fits | 151,262 | 209 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 434,242 | 4.342 | 20 | 20 | fits | 126,193 | 202 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 152,323 | 1.523 | 20 | 24 | fits | 145,031 | 142 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 302,595 | 3.026 | 20 | 24 | fits | 151,262 | 209 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 302,529 | 3.025 | 20 | 50 | fits | 151,262 | 209 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 437,266 | 4.373 | 20 | 50 | fits | 126,193 | 202 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 526,595 | 5.266 | 20 | 20 | fits | 89,395 | 24 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 1,033,974 | 10.340 | 20 | 20 | fits | 62,355 | 20 | 0.728 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 355,674 | 3.557 | 20 | 20 | fits | 114,758 | 187 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 292,651 | 2.927 | 20 | 200 | fits | 150,955 | 210 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 406,793 | 4.068 | 20 | 200 | fits | 114,758 | 187 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 293,575 | 2.936 | 20 | 20 | fits | 150,955 | 210 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 407,497 | 4.075 | 20 | 20 | fits | 114,758 | 187 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 146,260 | 1.463 | 20 | 24 | fits | 145,035 | 142 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 296,225 | 2.962 | 20 | 24 | fits | 150,955 | 210 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 296,159 | 2.962 | 20 | 50 | fits | 150,955 | 210 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 410,521 | 4.105 | 20 | 50 | fits | 114,758 | 187 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 500,133 | 5.001 | 20 | 20 | fits | 89,678 | 24 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 1,030,679 | 10.307 | 20 | 20 | fits | 82,325 | 30 | 0.733 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 344,833 | 3.448 | 20 | 20 | fits | 114,501 | 184 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 296,895 | 2.969 | 20 | 200 | fits | 152,063 | 214 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 410,780 | 4.108 | 20 | 200 | fits | 114,501 | 184 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 297,819 | 2.978 | 20 | 20 | fits | 152,063 | 214 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 411,484 | 4.115 | 20 | 20 | fits | 114,501 | 184 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 149,396 | 1.494 | 20 | 24 | fits | 145,035 | 142 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 300,469 | 3.005 | 20 | 24 | fits | 152,063 | 214 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 300,403 | 3.004 | 20 | 50 | fits | 152,063 | 214 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 414,508 | 4.145 | 20 | 50 | fits | 114,501 | 184 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 504,120 | 5.041 | 20 | 20 | fits | 89,678 | 24 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 1,112,929 | 11.129 | 20 | 20 | fits | 90,207 | 29 | 0.664 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 355,089 | 3.551 | 20 | 20 | fits | 117,009 | 175 | 0.404 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 297,672 | 2.977 | 20 | 200 | fits | 149,704 | 225 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 414,065 | 4.141 | 20 | 200 | fits | 117,009 | 175 | 0.404 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 298,596 | 2.986 | 20 | 20 | fits | 149,704 | 225 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 414,769 | 4.148 | 20 | 20 | fits | 117,009 | 175 | 0.404 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 152,532 | 1.525 | 20 | 24 | fits | 145,035 | 142 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 301,246 | 3.012 | 20 | 24 | fits | 149,704 | 225 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 301,180 | 3.012 | 20 | 50 | fits | 149,704 | 225 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 417,793 | 4.178 | 20 | 50 | fits | 117,009 | 175 | 0.404 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 507,586 | 5.076 | 20 | 20 | fits | 89,859 | 25 | 0.808 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,116,794 | 11.168 | 20 | 20 | fits | 89,420 | 28 | 0.658 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 363,509 | 3.635 | 20 | 20 | fits | 114,252 | 185 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 303,153 | 3.032 | 20 | 200 | fits | 152,049 | 214 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 416,789 | 4.168 | 20 | 200 | fits | 114,252 | 185 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 304,077 | 3.041 | 20 | 20 | fits | 152,049 | 214 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 417,493 | 4.175 | 20 | 20 | fits | 114,252 | 185 | 0.418 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 155,668 | 1.557 | 20 | 24 | fits | 145,035 | 142 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 306,727 | 3.067 | 20 | 24 | fits | 152,049 | 214 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 306,661 | 3.067 | 20 | 50 | fits | 152,049 | 214 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 420,517 | 4.205 | 20 | 50 | fits | 114,252 | 185 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 522,795 | 5.228 | 20 | 20 | fits | 93,241 | 31 | 0.807 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,115,669 | 11.157 | 20 | 20 | fits | 76,168 | 24 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 359,084 | 3.591 | 20 | 20 | fits | 120,235 | 181 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 289,584 | 2.896 | 20 | 200 | fits | 151,361 | 231 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 418,059 | 4.181 | 20 | 200 | fits | 120,235 | 181 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 290,508 | 2.905 | 20 | 20 | fits | 151,361 | 231 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 418,763 | 4.188 | 20 | 20 | fits | 120,235 | 181 | 0.418 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 142,787 | 1.428 | 20 | 24 | fits | 145,035 | 142 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 293,158 | 2.932 | 20 | 24 | fits | 151,361 | 231 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 293,092 | 2.931 | 20 | 50 | fits | 151,361 | 231 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 421,787 | 4.218 | 20 | 50 | fits | 120,235 | 181 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 511,368 | 5.114 | 20 | 20 | fits | 89,647 | 24 | 0.809 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,103,999 | 11.040 | 20 | 20 | fits | 76,262 | 25 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 358,018 | 3.580 | 20 | 20 | fits | 122,053 | 193 | 0.407 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 297,293 | 2.973 | 20 | 200 | fits | 147,570 | 212 | 0.401 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 418,730 | 4.187 | 20 | 200 | fits | 122,053 | 193 | 0.407 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 298,217 | 2.982 | 20 | 20 | fits | 147,570 | 212 | 0.401 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 419,434 | 4.194 | 20 | 20 | fits | 122,053 | 193 | 0.407 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 146,120 | 1.461 | 20 | 24 | fits | 145,232 | 143 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 300,867 | 3.009 | 20 | 24 | fits | 147,570 | 212 | 0.401 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 300,801 | 3.008 | 20 | 50 | fits | 147,570 | 212 | 0.401 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 422,458 | 4.225 | 20 | 50 | fits | 122,053 | 193 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 517,054 | 5.171 | 20 | 20 | fits | 94,662 | 30 | 0.809 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,119,622 | 11.196 | 20 | 20 | fits | 76,732 | 24 | 0.702 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 369,002 | 3.690 | 20 | 20 | fits | 125,061 | 181 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 303,977 | 3.040 | 20 | 200 | fits | 149,586 | 225 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 428,422 | 4.284 | 20 | 200 | fits | 125,061 | 181 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 304,901 | 3.049 | 20 | 20 | fits | 149,586 | 225 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 429,126 | 4.291 | 20 | 20 | fits | 125,061 | 181 | 0.430 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 158,955 | 1.590 | 20 | 24 | fits | 144,317 | 143 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 307,551 | 3.076 | 20 | 24 | fits | 149,586 | 225 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 307,485 | 3.075 | 20 | 50 | fits | 149,586 | 225 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 432,150 | 4.322 | 20 | 50 | fits | 125,061 | 181 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 599,491 | 5.995 | 20 | 20 | fits | 89,828 | 25 | 0.805 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,124,462 | 11.245 | 20 | 20 | fits | 76,378 | 24 | 0.696 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 444,287 | 4.443 | 20 | 20 | fits | 122,557 | 196 | 0.398 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 297,385 | 2.974 | 20 | 200 | fits | 150,896 | 208 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 497,010 | 4.970 | 20 | 200 | fits | 122,557 | 196 | 0.398 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 298,309 | 2.983 | 20 | 20 | fits | 150,896 | 208 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 497,714 | 4.977 | 20 | 20 | fits | 122,557 | 196 | 0.398 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 151,053 | 1.511 | 20 | 24 | fits | 144,995 | 142 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 300,959 | 3.010 | 20 | 24 | fits | 150,896 | 208 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 300,893 | 3.009 | 20 | 50 | fits | 150,896 | 208 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 500,738 | 5.007 | 20 | 50 | fits | 122,557 | 196 | 0.398 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 590,362 | 5.904 | 20 | 20 | fits | 89,690 | 24 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,115,148 | 11.151 | 20 | 20 | fits | 76,311 | 24 | 0.694 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 371,639 | 3.716 | 20 | 20 | fits | 114,789 | 187 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 308,614 | 3.086 | 20 | 200 | fits | 152,744 | 215 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 422,787 | 4.228 | 20 | 200 | fits | 114,789 | 187 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 309,538 | 3.095 | 20 | 20 | fits | 152,744 | 215 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 423,491 | 4.235 | 20 | 20 | fits | 114,789 | 187 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 152,109 | 1.521 | 20 | 24 | fits | 145,272 | 143 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 312,188 | 3.122 | 20 | 24 | fits | 152,744 | 215 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 312,122 | 3.121 | 20 | 50 | fits | 152,744 | 215 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 426,515 | 4.265 | 20 | 50 | fits | 114,789 | 187 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 516,135 | 5.161 | 20 | 20 | fits | 89,686 | 24 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 1,044,310 | 10.443 | 20 | 20 | fits | 72,925 | 33 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 354,398 | 3.544 | 20 | 20 | fits | 122,375 | 193 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 306,356 | 3.064 | 20 | 200 | fits | 147,660 | 212 | 0.402 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 428,115 | 4.281 | 20 | 200 | fits | 122,375 | 193 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 307,280 | 3.073 | 20 | 20 | fits | 147,660 | 212 | 0.402 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 428,819 | 4.288 | 20 | 20 | fits | 122,375 | 193 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 154,935 | 1.549 | 20 | 24 | fits | 145,234 | 143 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 309,930 | 3.099 | 20 | 24 | fits | 147,660 | 212 | 0.402 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 309,864 | 3.099 | 20 | 50 | fits | 147,660 | 212 | 0.402 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 431,843 | 4.318 | 20 | 50 | fits | 122,375 | 193 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 521,521 | 5.215 | 20 | 20 | fits | 89,744 | 24 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 1,052,146 | 10.521 | 20 | 20 | fits | 81,814 | 31 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 366,228 | 3.662 | 20 | 20 | fits | 114,799 | 187 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 303,205 | 3.032 | 20 | 200 | fits | 150,879 | 210 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 417,388 | 4.174 | 20 | 200 | fits | 114,799 | 187 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 304,129 | 3.041 | 20 | 20 | fits | 150,879 | 210 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 418,092 | 4.181 | 20 | 20 | fits | 114,799 | 187 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 156,890 | 1.569 | 20 | 24 | fits | 144,995 | 142 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 306,779 | 3.068 | 20 | 24 | fits | 150,879 | 210 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 306,713 | 3.067 | 20 | 50 | fits | 150,879 | 210 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 421,116 | 4.211 | 20 | 50 | fits | 114,799 | 187 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 510,684 | 5.107 | 20 | 20 | fits | 89,634 | 24 | 0.809 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 1,040,786 | 10.408 | 20 | 20 | fits | 76,388 | 24 | 0.696 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 346,509 | 3.465 | 20 | 20 | fits | 117,526 | 175 | 0.408 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 289,367 | 2.894 | 20 | 200 | fits | 151,022 | 230 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 406,277 | 4.063 | 20 | 200 | fits | 117,526 | 175 | 0.408 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 290,291 | 2.903 | 20 | 20 | fits | 151,022 | 230 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 406,981 | 4.070 | 20 | 20 | fits | 117,526 | 175 | 0.408 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 142,909 | 1.429 | 20 | 24 | fits | 144,995 | 142 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 292,941 | 2.929 | 20 | 24 | fits | 151,022 | 230 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 292,875 | 2.929 | 20 | 50 | fits | 151,022 | 230 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 410,005 | 4.100 | 20 | 50 | fits | 117,526 | 175 | 0.408 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 499,629 | 4.996 | 20 | 20 | fits | 89,690 | 24 | 0.809 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 1,028,455 | 10.285 | 20 | 20 | fits | 76,311 | 24 | 0.694 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 356,489 | 3.565 | 20 | 20 | fits | 114,746 | 187 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 293,519 | 2.935 | 20 | 200 | fits | 150,938 | 210 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 407,649 | 4.076 | 20 | 200 | fits | 114,746 | 187 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 294,443 | 2.944 | 20 | 20 | fits | 150,938 | 210 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 408,353 | 4.084 | 20 | 20 | fits | 114,746 | 187 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 147,145 | 1.471 | 20 | 24 | fits | 144,995 | 142 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 297,093 | 2.971 | 20 | 24 | fits | 150,938 | 210 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 297,027 | 2.970 | 20 | 50 | fits | 150,938 | 210 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 411,377 | 4.114 | 20 | 50 | fits | 114,746 | 187 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 501,070 | 5.011 | 20 | 20 | fits | 89,759 | 25 | 0.807 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 1,030,358 | 10.304 | 20 | 20 | fits | 76,361 | 24 | 0.694 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 345,648 | 3.456 | 20 | 20 | fits | 114,774 | 185 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 297,763 | 2.978 | 20 | 200 | fits | 152,046 | 214 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 411,921 | 4.119 | 20 | 200 | fits | 114,774 | 185 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 298,687 | 2.987 | 20 | 20 | fits | 152,046 | 214 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 412,625 | 4.126 | 20 | 20 | fits | 114,774 | 185 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 150,281 | 1.503 | 20 | 24 | fits | 144,995 | 142 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 301,337 | 3.013 | 20 | 24 | fits | 152,046 | 214 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 301,271 | 3.013 | 20 | 50 | fits | 152,046 | 214 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 415,649 | 4.156 | 20 | 50 | fits | 114,774 | 185 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 507,846 | 5.078 | 20 | 20 | fits | 83,081 | 33 | 0.824 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 1,029,617 | 10.296 | 20 | 20 | fits | 76,226 | 24 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 375,336 | 3.753 | 20 | 20 | fits | 127,428 | 188 | 0.431 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 298,716 | 2.987 | 20 | 200 | fits | 149,863 | 226 | 0.400 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 434,384 | 4.344 | 20 | 200 | fits | 127,428 | 188 | 0.431 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 299,640 | 2.996 | 20 | 20 | fits | 149,863 | 226 | 0.400 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 435,088 | 4.351 | 20 | 20 | fits | 127,428 | 188 | 0.431 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 153,417 | 1.534 | 20 | 24 | fits | 144,995 | 142 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 302,290 | 3.023 | 20 | 24 | fits | 149,863 | 226 | 0.400 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 302,224 | 3.022 | 20 | 50 | fits | 149,863 | 226 | 0.400 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 438,112 | 4.381 | 20 | 50 | fits | 127,428 | 188 | 0.431 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 527,497 | 5.275 | 20 | 20 | fits | 89,451 | 24 | 0.807 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 1,034,590 | 10.346 | 20 | 20 | fits | 62,353 | 20 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 384,079 | 3.841 | 20 | 20 | fits | 130,506 | 224 | 0.399 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 306,856 | 3.069 | 20 | 200 | fits | 146,548 | 185 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 436,746 | 4.367 | 20 | 200 | fits | 130,506 | 224 | 0.399 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 307,780 | 3.078 | 20 | 20 | fits | 146,548 | 185 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 437,450 | 4.375 | 20 | 20 | fits | 130,506 | 224 | 0.399 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 156,705 | 1.567 | 20 | 24 | fits | 145,147 | 143 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 310,430 | 3.104 | 20 | 24 | fits | 146,548 | 185 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 310,364 | 3.104 | 20 | 50 | fits | 146,548 | 185 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 440,474 | 4.405 | 20 | 50 | fits | 130,506 | 224 | 0.399 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 530,152 | 5.302 | 20 | 20 | fits | 89,744 | 24 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 1,054,557 | 10.546 | 20 | 20 | fits | 76,710 | 24 | 0.702 |
| LINK_UP | `adp.link_up.if0` | 2,846 | 0.028 | 20 | 200 | fits | 26,682 | 43 (11) | 0.722 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,622 | 0.106 | 20 | 200 | fits | 22,124 | 23 (39) | 0.739 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 2,204 | 0.022 | 20 | 200 | fits | 2,727 | 10 (11) | 0.520 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 153,107 | 1.531 | 20 | 200 | fits | 154,047 | 250 | 0.464 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 218,717 | 2.187 | 20 | 20 | fits | 85,747 | 82 | 0.680 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 306,434 | 3.064 | 20 | 24 | fits | 81,276 | 60 | 0.504 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 165,625 | 1.656 | 20 | 50 | fits | 84,320 | 179 | 0.379 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 956,730 | 9.567 | 20 | 20 | fits | 34,618 | 12 | 0.837 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 259,195 | 2.592 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 153,107 | 1.531 | 20 | 200 | fits | 154,047 | 250 | 0.464 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 293,279 | 2.933 | 20 | 20 | fits | 88,905 | 37 | 0.723 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 301,299 | 3.013 | 20 | 24 | fits | 82,777 | 66 | 0.499 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 182,052 | 1.821 | 20 | 50 | fits | 88,557 | 88 | 0.685 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 1,015,793 | 10.158 | 20 | 20 | fits | 66,505 | 26 | 0.761 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 299,979 | 3.000 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 13,678 | 0.137 | 20 | 20 | fits | 28,908 | 21 (35) | 0.811 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 16,674 | 0.167 | 20 | 20 | fits | 25,311 | 17 (14) | 0.849 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 20,706 | 0.207 | 20 | 20 | fits | 24,596 | 18 (14) | 0.841 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 14,080 | 0.141 | 20 | 20 | fits | 28,874 | 21 (35) | 0.806 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 77,403 | 0.774 | 20 | 20 | fits | 28,870 | 8 | 0.819 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 45,331 | 0.453 | 20 | 20 | fits | 45,397 | 12 | 0.900 |
| malformed MRPDU discard | `srp.malformed.if0` | 21,956 | 0.220 | 20 | 20 | fits | 22,022 | 12 | 0.742 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 92,346 | 0.923 | 220 | 220 | fits | 59,146 | 6 | 0.904 |
| an event behind 15 others | `backlog.event.if0` | 161,462 | 1.615 | 20 | 200 | fits | 55,169 | 79 | 0.544 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 423,570 | 4.236 | 20 | 20 | fits | 48,138 | 72 | 0.369 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 413,190 | 4.132 | 20 | 200 | fits | 148,936 | 159 | 0.408 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 412,574 | 4.126 | 20 | 200 | fits | 148,936 | 159 | 0.408 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 408,868 | 4.089 | 20 | 20 | fits | 148,936 | 159 | 0.408 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 456,170 | 4.562 | 20 | 20 | fits | 48,138 | 72 | 0.369 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 147,311 | 1.473 | 20 | 24 | fits | 148,202 | 148 | 0.399 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 411,518 | 4.115 | 20 | 24 | fits | 148,936 | 159 | 0.408 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 411,452 | 4.115 | 20 | 50 | fits | 148,936 | 159 | 0.408 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 411,056 | 4.111 | 20 | 50 | fits | 148,936 | 159 | 0.408 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 459,128 | 4.591 | 20 | 20 | fits | 48,138 | 72 | 0.369 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 519,562 | 5.196 | 20 | 20 | fits | 24,737 | 41 | 0.230 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 359,364 | 3.594 | 20 | 20 | fits | 121,226 | 182 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 289,797 | 2.898 | 20 | 200 | fits | 149,779 | 226 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 419,299 | 4.193 | 20 | 200 | fits | 121,226 | 182 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 290,721 | 2.907 | 20 | 20 | fits | 149,779 | 226 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 420,003 | 4.200 | 20 | 20 | fits | 121,226 | 182 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 144,582 | 1.446 | 20 | 24 | fits | 144,768 | 145 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 293,371 | 2.934 | 20 | 24 | fits | 149,779 | 226 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 293,305 | 2.933 | 20 | 50 | fits | 149,779 | 226 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 423,027 | 4.230 | 20 | 50 | fits | 121,226 | 182 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 512,576 | 5.126 | 20 | 20 | fits | 89,615 | 24 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,028,029 | 10.280 | 20 | 20 | fits | 76,318 | 24 | 0.693 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,246 | 0.082 | 20 | 20 | fits | 27,346 | 19 | 0.820 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 289,797 | 2.898 | 20 | 200 | fits | 149,779 | 226 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 26,911 | 0.269 | 20 | 200 | fits | 27,346 | 19 | 0.820 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 290,721 | 2.907 | 20 | 20 | fits | 149,779 | 226 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 410,788 | 4.108 | 20 | 20 | fits | 112,011 | 172 | 0.392 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 144,582 | 1.446 | 20 | 24 | fits | 144,768 | 145 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 293,371 | 2.934 | 20 | 24 | fits | 149,779 | 226 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 293,305 | 2.933 | 20 | 50 | fits | 149,779 | 226 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 413,812 | 4.138 | 20 | 50 | fits | 112,011 | 172 | 0.392 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 502,919 | 5.029 | 20 | 20 | fits | 89,173 | 24 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,018,356 | 10.184 | 20 | 20 | fits | 76,316 | 24 | 0.694 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,298,261 | 62.983 | 20 | 20 | MISS ceiling | 18,375 | 13 | 0.633 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,316,615 | 63.166 | 20 | 20 | MISS ceiling | 18,430 | 13 | 0.625 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,334,958 | 63.350 | 20 | 20 | MISS ceiling | 18,400 | 13 | 0.625 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,353,214 | 63.532 | 20 | 20 | MISS ceiling | 18,332 | 13 | 0.633 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,371,423 | 63.714 | 20 | 20 | MISS ceiling | 18,272 | 13 | 0.641 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 157,002 | 1.570 | 20 | 200 | fits | 150,864 | 222 | 0.423 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 246,607 | 2.466 | 20 | 200 | fits | 90,221 | 164 | 0.373 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 152,680 | 1.527 | 20 | 20 | fits | 150,864 | 222 | 0.423 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,209,618 | 62.096 | 20 | 20 | MISS ceiling | 30,199 | 15 | 0.782 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 156,320 | 1.563 | 20 | 24 | fits | 150,864 | 222 | 0.423 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,182,905 | 61.829 | 20 | 24 | MISS ceiling | 145,809 | 106 | 0.431 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 155,264 | 1.553 | 20 | 50 | fits | 150,864 | 222 | 0.423 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 245,089 | 2.451 | 20 | 50 | fits | 90,221 | 164 | 0.373 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 333,948 | 3.339 | 20 | 20 | fits | 88,925 | 24 | 0.804 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 848,729 | 8.487 | 20 | 20 | fits | 76,214 | 24 | 0.679 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 6,225 | 0.062 | 20 | 20 | fits | 24,781 | 13 (29) | 0.810 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 8,537 | 0.085 | 20 | 20 | fits | 27,012 | 19 (35) | 0.815 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 11,807 | 0.118 | 20 | 20 | fits | 28,872 | 21 (12) | 0.809 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 10,926 | 0.109 | 20 | 50 | fits | 26,682 | 43 | 0.722 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 19,390 | 0.194 | 20 | 50 | fits | 26,276 | 41 | 0.674 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 19,189 | 0.192 | 20 | 50 | fits | 22,897 | 35 | 0.698 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 19,442 | 0.194 | 20 | 50 | fits | 28,044 | 61 | 0.622 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 21,694 | 0.217 | 20 | 50 | fits | 28,044 | 61 | 0.622 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 9,210 | 0.092 | 20 | 50 | fits | 22,034 | 30 | 0.664 |
| LINK_UP | `adp.link_up.if0` | 2,846 | 0.028 | 20 | 200 | fits | 26,682 | 43 (11) | 0.722 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,622 | 0.106 | 20 | 200 | fits | 22,124 | 23 (39) | 0.739 |
| LINK_DOWN | `adp.link_down.if0` | 2,418 | 0.024 | 20 | 200 | fits | 23,867 | 23 (9) | 0.775 |
| LINK_UP | `adp.link_up.if0` | 2,846 | 0.028 | 20 | 200 | fits | 26,682 | 43 (11) | 0.722 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,622 | 0.106 | 20 | 200 | fits | 22,124 | 23 (39) | 0.739 |
| GM_CHANGE | `adp.gm_change.if0` | 2,536 | 0.025 | 20 | 200 | fits | 16,407 | 17 (11) | 0.696 |
| LINK_UP | `adp.link_up.if0` | 2,846 | 0.028 | 20 | 200 | fits | 26,682 | 43 (11) | 0.722 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,622 | 0.106 | 20 | 200 | fits | 22,124 | 23 (39) | 0.739 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 5,087 | 0.051 | 20 | 200 | fits | 16,805 | 16 (31) | 0.659 |
| LINK_UP | `adp.link_up.if0` | 2,846 | 0.028 | 20 | 200 | fits | 26,682 | 43 (11) | 0.722 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,622 | 0.106 | 20 | 200 | fits | 22,124 | 23 (39) | 0.739 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 5,087 | 0.051 | 20 | 200 | fits | 16,805 | 16 (31) | 0.659 |
| set_name | `aecp_fanout.set_name.if0` | 47,982 | 0.480 | 20 | 24 | fits | 63,175 | 89 | 0.600 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 59,540 | 0.595 | 20 | 24 | fits | 56,183 | 78 | 0.610 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 45,716 | 0.457 | 20 | 24 | fits | 55,421 | 79 | 0.578 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 56,623 | 0.566 | 20 | 24 | fits | 51,296 | 78 | 0.566 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 69,041 | 0.690 | 20 | 24 | fits | 66,940 | 66 | 0.653 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 238,744 | 2.387 | 20 | 24 | fits | 61,723 | 65 | 0.649 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 225,467 | 2.255 | 20 | 24 | fits | 54,648 | 67 | 0.613 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 52,963 | 0.530 | 20 | 24 | fits | 51,999 | 78 | 0.578 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 44,575 | 0.446 | 20 | 24 | fits | 51,754 | 79 | 0.574 |
| BIND_RX | `acmp.bind_rx.if0` | 18,494 | 0.185 | 20 | 20 | fits | 41,749 | 26 (77) | 0.803 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,676 | 0.097 | 20 | 20 | fits | 33,122 | 19 (32) | 0.842 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,282 | 0.103 | 20 | 20 | fits | 25,315 | 15 (47) | 0.774 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,997 | 0.140 | 20 | 20 | fits | 40,487 | 18 (50) | 0.847 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,361 | 0.104 | 20 | 20 | fits | 25,677 | 17 (48) | 0.767 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,444 | 0.094 | 20 | 20 | fits | 25,062 | 16 (48) | 0.760 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,007 | 0.090 | 20 | 20 | fits | 24,350 | 16 (48) | 0.755 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,321 | 0.093 | 20 | 20 | fits | 24,330 | 16 (48) | 0.755 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 19,216 | 0.192 | 20 | 24 | fits | 28,317 | 20 | 0.799 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 27,832 | 0.278 | 20 | 24 | fits | 32,589 | 20 | 0.739 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 24,130 | 0.241 | 20 | 24 | fits | 28,587 | 20 | 0.761 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 25,568 | 0.256 | 20 | 24 | fits | 28,458 | 20 | 0.758 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 13,031 | 0.130 | 20 | 24 | fits | 28,918 | 20 | 0.762 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 21,676 | 0.217 | 20 | 24 | fits | 28,567 | 20 | 0.755 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 11,452 | 0.115 | 20 | 24 | fits | 27,773 | 20 | 0.761 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 23,778 | 0.238 | 20 | 24 | fits | 28,077 | 20 | 0.772 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 24,896 | 0.249 | 20 | 24 | fits | 27,453 | 20 | 0.775 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 30,427 | 0.304 | 20 | 24 | fits | 35,126 | 27 | 0.678 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 20,226 | 0.202 | 20 | 24 | fits | 26,902 | 20 | 0.785 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 11,815 | 0.118 | 20 | 24 | fits | 27,251 | 20 | 0.789 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 20,781 | 0.208 | 20 | 24 | fits | 27,536 | 20 | 0.756 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 12,973 | 0.130 | 20 | 24 | fits | 28,935 | 20 | 0.765 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 21,086 | 0.211 | 20 | 24 | fits | 28,060 | 20 | 0.772 |
| get_configuration | `aecp.get_configuration.if0` | 23,451 | 0.235 | 20 | 24 | fits | 25,763 | 20 | 0.786 |
| entity_available | `aecp.entity_available.if0` | 10,296 | 0.103 | 20 | 24 | fits | 25,497 | 20 | 0.773 |
| get_name | `aecp.get_name.if0` | 23,940 | 0.239 | 20 | 24 | fits | 28,298 | 20 | 0.777 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 12,140 | 0.121 | 20 | 24 | fits | 29,456 | 25 | 0.762 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 22,625 | 0.226 | 20 | 24 | fits | 29,558 | 27 | 0.786 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 10,948 | 0.109 | 20 | 24 | fits | 26,232 | 20 | 0.792 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 19,375 | 0.194 | 20 | 24 | fits | 24,985 | 20 | 0.764 |
| set_name | `aecp.set_name.if0` | 21,162 | 0.212 | 20 | 24 | fits | 45,421 | 43 | 0.782 |
| lock_entity | `aecp.lock_entity.if0` | 30,612 | 0.306 | 20 | 24 | fits | 37,218 | 34 | 0.806 |
| unlock_entity | `aecp.unlock_entity.if0` | 29,240 | 0.292 | 20 | 24 | fits | 37,594 | 33 | 0.798 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 135,874 | 1.359 | 20 | 24 | fits | 151,879 | 92 | 0.338 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 137,091 | 1.371 | 20 | 24 | fits | 139,902 | 70 | 0.312 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 125,700 | 1.257 | 20 | 24 | fits | 44,968 | 17 | 0.704 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 278,883 | 2.789 | 20 | 24 | fits | 95,696 | 18 | 0.688 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 235,717 | 2.357 | 20 | 24 | fits | 97,321 | 17 | 0.693 |
| LINK_UP | `fixture.link_up.if0` | 2,846 | 0.028 | 20 | 200 | fits | 26,682 | 43 (11) | 0.722 |
| malformed MRPDU discard | `fixture.malformed.if0` | 22,394 | 0.224 | 20 | 20 | fits | 22,460 | 12 | 0.771 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 31,812 | 0.318 | 20 | 24 | fits | 46,270 | 43 | 0.788 |
| LINK_DOWN | `fixture.link_down.if0` | 2,940 | 0.029 | 20 | 200 | fits | 26,119 | 23 (9) | 0.791 |
| BIND_RX | `fixture.bind_rx.if0` | 19,064 | 0.191 | 20 | 20 | fits | 42,077 | 26 (77) | 0.810 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 20,991 | 0.210 | 20 | 20 | fits | 36,302 | 29 (35) | 0.785 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 11,978 | 0.120 | 20 | 20 | fits | 26,030 | 13 (29) | 0.834 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 81,938 | 0.819 | 20 | 200 | fits | 82,042 | 51 | 0.769 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 81,938 | 0.819 | 20 | 200 | fits | 82,042 | 51 | 0.769 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 81,664 | 0.817 | 20 | 20 | fits | 82,042 | 51 | 0.769 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 81,664 | 0.817 | 20 | 20 | fits | 82,042 | 51 | 0.769 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 81,872 | 0.819 | 20 | 24 | fits | 82,042 | 51 | 0.769 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 81,872 | 0.819 | 20 | 24 | fits | 82,042 | 51 | 0.769 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 81,806 | 0.818 | 20 | 50 | fits | 82,042 | 51 | 0.769 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 81,806 | 0.818 | 20 | 50 | fits | 82,042 | 51 | 0.769 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 81,740 | 0.817 | 20 | 20 | fits | 82,042 | 51 | 0.769 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 81,740 | 0.817 | 20 | 20 | fits | 82,042 | 51 | 0.769 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
