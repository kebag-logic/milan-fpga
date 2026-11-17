Round 3 CPU-budget 1x1/1if: complete row table, measured firmware byte-identical at 5f625090, rc 0
### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 92 paths and 7 of 950 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.196 (0.410) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.096 (0.224) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.078 (0.260) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.136 (0.473) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.105 (0.245) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.097 (0.223) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.106 (0.236) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.107 (0.247) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.099 (0.312) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.102 (0.443) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.201 (0.545) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.300 (0.589) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.188 (0.555) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.077 (0.327) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.200 (0.553) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.150 (0.385) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.051 (0.153) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.026 (0.163) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.027 (0.243) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.028 (0.265) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.125 (0.281) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.074 (0.383) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.084 (0.235) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.169 (0.474) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.134 (0.429) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.114 (0.272) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.156 (0.458) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.141 (0.341) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.076 (0.227) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.195 (0.505) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.110 (0.270) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.107 (0.267) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.149 (0.454) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.126 (0.286) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.146 (0.451) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.096 (0.255) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.155 (0.464) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.152 (0.457) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.157 (0.463) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.104 (0.265) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.112 (0.272) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.163 (0.470) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.154 (0.461) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.219 (0.516) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.222 (0.627) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.139 (0.440) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.224 (0.579) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.847 (3.118) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.497 (0.757) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.613 (0.896) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.555 (0.839) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.563 (0.823) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.541 (0.844) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.486 (3.768) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.552 (0.810) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 2.266 (2.560) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.221 (2.565) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.919 (4.263) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.462 (3.806) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.565 (1.870) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.034 (4.442) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-aged2-7.adp_available.if0` (backlog-adp@verify-aged2-7) | 4.412 (5.022) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.089 (0.436) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.572 (1.968) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.842 (62.969) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.521 (63.649) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.320 (0.448) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 2.948 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 1.520 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 2.666 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 1.854 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.078 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.236 (0.551) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.096 (0.211) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.112 (0.265) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.209 (0.551) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.141 (0.442) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 1.871 | fits | 0 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 3.944 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.006 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 3.988 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-7.service.adp.last.if0` (backlog-adp@verify-aged2-7) | 4.916 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.265 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.756 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 3.970 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-7.service.maap.last.if0` (backlog-adp@verify-aged2-7) | 4.953 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-5.service.srp.first.if0` (backlog-adp@program-aged2-5) | 5.976 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-6.service.srp.last.if0` (backlog-adp@program-aged2-6) | 9.788 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.804 (0.890) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.419 (0.420) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.194 (0.195) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.749 (0.826) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.108 | 11 | 149,220 (1.492) | yes | - |
| backlog-adp@blank-1 | 0 | 10.307 | 11 | 148,398 (1.484) | yes | - |
| backlog-adp@blank-2 | 0 | 10.142 | 10 | 148,398 (1.484) | yes | - |
| backlog-adp@blank-3 | 0 | 10.060 | 10 | 148,398 (1.484) | yes | - |
| backlog-adp@blank-4 | 0 | 10.010 | 9 | 145,998 (1.460) | yes | - |
| backlog-adp@blank-5 | 0 | 10.512 | 12 | 148,450 (1.484) | yes | - |
| backlog-adp@blank-6 | 0 | 10.108 | 10 | 148,514 (1.485) | yes | - |
| backlog-adp@blank-7 | 0 | 10.049 | 9 | 144,382 (1.444) | yes | - |
| backlog-adp@program-0 | 0 | 10.269 | 11 | 146,495 (1.465) | yes | - |
| backlog-adp@program-1 | 0 | 10.467 | 12 | 146,639 (1.466) | yes | - |
| backlog-adp@program-2 | 0 | 10.050 | 10 | 146,175 (1.462) | yes | - |
| backlog-adp@program-3 | 0 | 10.146 | 10 | 146,204 (1.462) | yes | - |
| backlog-adp@program-4 | 0 | 9.592 | 11 | 147,128 (1.471) | yes | - |
| backlog-adp@program-5 | 0 | 9.354 | 10 | 146,204 (1.462) | yes | - |
| backlog-adp@program-6 | 0 | 9.394 | 10 | 146,175 (1.462) | yes | - |
| backlog-adp@program-7 | 0 | 9.311 | 10 | 146,175 (1.462) | yes | - |
| backlog-adp@verify-0 | 0 | 10.589 | 11 | 147,042 (1.470) | yes | - |
| backlog-adp@verify-1 | 0 | 10.145 | 10 | 146,469 (1.465) | yes | - |
| backlog-adp@verify-2 | 0 | 10.042 | 10 | 146,469 (1.465) | yes | - |
| backlog-adp@verify-3 | 0 | 10.007 | 10 | 146,469 (1.465) | yes | - |
| backlog-adp@verify-4 | 0 | 10.519 | 12 | 146,902 (1.469) | yes | - |
| backlog-adp@verify-5 | 0 | 10.217 | 11 | 146,550 (1.466) | yes | - |
| backlog-adp@verify-6 | 0 | 10.057 | 10 | 146,254 (1.463) | yes | - |
| backlog-adp@verify-7 | 0 | 10.152 | 10 | 146,265 (1.463) | yes | - |
| backlog-adp@blank-aged2-0 | 1 | 11.471 | 12 | 146,608 (1.466) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 10.258 | 11 | 144,970 (1.450) | yes | - |
| backlog-adp@blank-aged2-2 | 1 | 10.011 | 9 | 146,119 (1.461) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 10.045 | 10 | 145,687 (1.457) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 10.043 | 10 | 145,687 (1.457) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 10.048 | 10 | 145,687 (1.457) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 10.082 | 10 | 145,692 (1.457) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 9.964 | 9 | 149,885 (1.499) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 11.744 | 12 | 147,129 (1.471) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 10.669 | 12 | 147,704 (1.477) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 10.736 | 12 | 147,704 (1.477) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 10.870 | 13 | 147,753 (1.478) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 10.769 | 12 | 147,754 (1.478) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 10.801 | 12 | 147,754 (1.478) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 10.815 | 11 | 147,754 (1.478) | yes | - |
| backlog-adp@blank-aged1-7 | 1 | 10.683 | 10 | 147,027 (1.470) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 10.580 | 12 | 146,776 (1.468) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 10.026 | 10 | 145,988 (1.460) | yes | - |
| backlog-adp@program-aged2-2 | 1 | 10.058 | 9 | 145,050 (1.450) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 10.098 | 10 | 145,806 (1.458) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 10.088 | 10 | 145,806 (1.458) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 10.125 | 10 | 145,806 (1.458) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 10.294 | 11 | 146,672 (1.467) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 10.059 | 9 | 144,686 (1.447) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 11.104 | 13 | 145,818 (1.458) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.502 | 12 | 146,672 (1.467) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 10.244 | 11 | 146,178 (1.462) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 10.156 | 10 | 145,731 (1.457) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 10.041 | 9 | 146,210 (1.462) | yes | - |
| backlog-adp@program-aged1-5 | 1 | 10.033 | 9 | 145,952 (1.460) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 10.067 | 10 | 145,751 (1.458) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 10.103 | 10 | 145,878 (1.459) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.042 | 10 | 146,110 (1.461) | yes | - |
| backlog-adp@verify-aged2-1 | 1 | 9.881 | 9 | 145,852 (1.459) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 10.009 | 10 | 145,614 (1.456) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 10.038 | 10 | 145,656 (1.457) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 10.312 | 12 | 146,746 (1.467) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 10.324 | 12 | 146,987 (1.470) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 10.121 | 10 | 145,752 (1.458) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 10.139 | 10 | 145,752 (1.458) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 11.200 | 12 | 146,987 (1.470) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 10.081 | 10 | 145,752 (1.458) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 10.120 | 10 | 145,752 (1.458) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 10.014 | 9 | 144,178 (1.442) | yes | - |
| backlog-adp@verify-aged1-4 | 1 | 9.981 | 9 | 146,200 (1.462) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 9.994 | 10 | 145,732 (1.457) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 10.425 | 12 | 145,840 (1.458) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 10.111 | 10 | 145,795 (1.458) | yes | - |
| backlog | 0 | 5.549 | 7 | 148,320 (1.483) | yes | - |
| backlog-adp | 0 | 9.238 | 10 | 146,385 (1.464) | yes | - |
| backlog-adp-refill | 0 | 40.736 | 25 | 146,385 (1.464) | yes | - |
| backlog-owed | 0 | 64.113 | 25 | 148,023 (1.480) | yes | - |
| fixture | 0 | 1.255 | 2 | 80,247 (0.802) | yes | - |

Composed maximum over the 4 backlog windows: 148,320 CPU cycles (1.483 ms), backlog.
Over the windows that released their whole load only: 148,320 (1.483 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3360 | 0 | 40,776 (0.408) | fits |
| save-second | 48513 | 0 | 49,122 (0.491) | fits |
| backlog-adp@blank-0 | 416 | 0 | 149,220 (1.492) | fits |
| backlog-adp@blank-1 | 416 | 0 | 148,398 (1.484) | fits |
| backlog-adp@blank-2 | 415 | 0 | 148,398 (1.484) | fits |
| backlog-adp@blank-3 | 415 | 0 | 148,398 (1.484) | fits |
| backlog-adp@blank-4 | 415 | 0 | 148,398 (1.484) | fits |
| backlog-adp@blank-5 | 417 | 0 | 148,450 (1.484) | fits |
| backlog-adp@blank-6 | 417 | 0 | 148,514 (1.485) | fits |
| backlog-adp@blank-7 | 417 | 0 | 148,514 (1.485) | fits |
| backlog-adp@program-0 | 519 | 0 | 146,495 (1.465) | fits |
| backlog-adp@program-1 | 520 | 0 | 146,639 (1.466) | fits |
| backlog-adp@program-2 | 520 | 0 | 146,175 (1.462) | fits |
| backlog-adp@program-3 | 520 | 0 | 146,204 (1.462) | fits |
| backlog-adp@program-4 | 522 | 0 | 147,128 (1.471) | fits |
| backlog-adp@program-5 | 523 | 0 | 146,204 (1.462) | fits |
| backlog-adp@program-6 | 523 | 0 | 146,175 (1.462) | fits |
| backlog-adp@program-7 | 523 | 0 | 146,175 (1.462) | fits |
| backlog-adp@verify-0 | 614 | 0 | 147,042 (1.470) | fits |
| backlog-adp@verify-1 | 613 | 0 | 146,469 (1.465) | fits |
| backlog-adp@verify-2 | 613 | 0 | 146,469 (1.465) | fits |
| backlog-adp@verify-3 | 613 | 0 | 146,469 (1.465) | fits |
| backlog-adp@verify-4 | 615 | 0 | 146,902 (1.469) | fits |
| backlog-adp@verify-5 | 615 | 0 | 146,550 (1.466) | fits |
| backlog-adp@verify-6 | 615 | 0 | 146,254 (1.463) | fits |
| backlog-adp@verify-7 | 615 | 0 | 146,265 (1.463) | fits |
| backlog-adp@blank-aged2-0 | 720 | 0 | 149,812 (1.498) | fits |
| backlog-adp@blank-aged2-1 | 725 | 0 | 149,771 (1.498) | fits |
| backlog-adp@blank-aged2-2 | 732 | 0 | 147,380 (1.474) | fits |
| backlog-adp@blank-aged2-3 | 739 | 0 | 145,687 (1.457) | fits |
| backlog-adp@blank-aged2-4 | 747 | 0 | 145,687 (1.457) | fits |
| backlog-adp@blank-aged2-5 | 755 | 0 | 145,687 (1.457) | fits |
| backlog-adp@blank-aged2-6 | 763 | 0 | 145,692 (1.457) | fits |
| backlog-adp@blank-aged2-7 | 770 | 0 | 149,885 (1.499) | fits |
| backlog-adp@blank-aged1-0 | 658 | 0 | 147,704 (1.477) | fits |
| backlog-adp@blank-aged1-1 | 665 | 0 | 147,704 (1.477) | fits |
| backlog-adp@blank-aged1-2 | 673 | 0 | 147,704 (1.477) | fits |
| backlog-adp@blank-aged1-3 | 682 | 0 | 147,753 (1.478) | fits |
| backlog-adp@blank-aged1-4 | 689 | 0 | 147,754 (1.478) | fits |
| backlog-adp@blank-aged1-5 | 697 | 0 | 147,754 (1.478) | fits |
| backlog-adp@blank-aged1-6 | 704 | 0 | 147,754 (1.478) | fits |
| backlog-adp@blank-aged1-7 | 711 | 0 | 147,734 (1.477) | fits |
| backlog-adp@program-aged2-0 | 818 | 0 | 146,776 (1.468) | fits |
| backlog-adp@program-aged2-1 | 824 | 0 | 145,988 (1.460) | fits |
| backlog-adp@program-aged2-2 | 831 | 0 | 145,806 (1.458) | fits |
| backlog-adp@program-aged2-3 | 839 | 0 | 145,806 (1.458) | fits |
| backlog-adp@program-aged2-4 | 847 | 0 | 145,806 (1.458) | fits |
| backlog-adp@program-aged2-5 | 855 | 0 | 145,806 (1.458) | fits |
| backlog-adp@program-aged2-6 | 864 | 0 | 146,672 (1.467) | fits |
| backlog-adp@program-aged2-7 | 870 | 0 | 152,585 (1.526) | fits |
| backlog-adp@program-aged1-0 | 756 | 0 | 145,818 (1.458) | fits |
| backlog-adp@program-aged1-1 | 763 | 0 | 146,672 (1.467) | fits |
| backlog-adp@program-aged1-2 | 770 | 0 | 146,178 (1.462) | fits |
| backlog-adp@program-aged1-3 | 777 | 0 | 145,731 (1.457) | fits |
| backlog-adp@program-aged1-4 | 784 | 0 | 146,210 (1.462) | fits |
| backlog-adp@program-aged1-5 | 792 | 0 | 145,952 (1.460) | fits |
| backlog-adp@program-aged1-6 | 800 | 0 | 145,751 (1.458) | fits |
| backlog-adp@program-aged1-7 | 808 | 0 | 145,878 (1.459) | fits |
| backlog-adp@verify-aged2-0 | 913 | 0 | 146,110 (1.461) | fits |
| backlog-adp@verify-aged2-1 | 920 | 0 | 145,852 (1.459) | fits |
| backlog-adp@verify-aged2-2 | 928 | 0 | 145,614 (1.456) | fits |
| backlog-adp@verify-aged2-3 | 936 | 0 | 145,656 (1.457) | fits |
| backlog-adp@verify-aged2-4 | 946 | 0 | 146,746 (1.467) | fits |
| backlog-adp@verify-aged2-5 | 954 | 0 | 146,987 (1.470) | fits |
| backlog-adp@verify-aged2-6 | 960 | 0 | 145,752 (1.458) | fits |
| backlog-adp@verify-aged2-7 | 968 | 0 | 145,752 (1.458) | fits |
| backlog-adp@verify-aged1-0 | 852 | 0 | 146,987 (1.470) | fits |
| backlog-adp@verify-aged1-1 | 858 | 0 | 145,752 (1.458) | fits |
| backlog-adp@verify-aged1-2 | 866 | 0 | 145,752 (1.458) | fits |
| backlog-adp@verify-aged1-3 | 873 | 0 | 149,720 (1.497) | fits |
| backlog-adp@verify-aged1-4 | 881 | 0 | 146,200 (1.462) | fits |
| backlog-adp@verify-aged1-5 | 889 | 0 | 145,732 (1.457) | fits |
| backlog-adp@verify-aged1-6 | 899 | 0 | 145,840 (1.458) | fits |
| backlog-adp@verify-aged1-7 | 905 | 0 | 145,795 (1.458) | fits |
| adp-advertise | 598 | 0 | 28,205 (0.282) | fits |
| save-held | 1418 | 0 | 152,969 (1.530) | fits |
| save-starved | 26127 | 0 | 152,969 (1.530) | fits |
| acmp-noresp | 1890 | 0 | 40,776 (0.408) | fits |
| save | 610 | 0 | 43,639 (0.436) | fits |
| srp | 290 | 0 | 51,450 (0.514) | fits |
| backlog | 286 | 0 | 148,320 (1.483) | fits |
| backlog-adp | 314 | 0 | 146,385 (1.464) | fits |
| backlog-adp-refill | 329 | 0 | 146,385 (1.464) | fits |
| backlog-owed | 310 | 0 | 148,023 (1.480) | fits |
| acmp-disc | 878 | 0 | 40,776 (0.408) | fits |
| maap | 182 | 0 | 28,205 (0.282) | fits |
| adp-link | 89 | 0 | 34,352 (0.344) | fits |
| adp-gm | 88 | 0 | 28,114 (0.281) | fits |
| adp-discover | 88 | 0 | 28,114 (0.281) | fits |
| control | 88 | 0 | 28,114 (0.281) | fits |
| aecp-fanout | 113 | 0 | 60,851 (0.609) | fits |
| acmp-cmd | 87 | 0 | 40,776 (0.408) | fits |
| aecp | 112 | 0 | 43,400 (0.434) | fits |
| aecp-largest-notice | 107 | 0 | 163,940 (1.639) | fits |
| datapath-events | 116 | 0 | 28,114 (0.281) | fits |
| fixture | 150 | 0 | 80,247 (0.802) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 8.654 (20) | 11.346 |
| backlog-adp@blank-aged2-1 | 2 | none | +8.697 ms, 76,790 (0.768 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 8.660 (20) | 11.340 |
| backlog-adp@blank-aged2-2 | 2 | none | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 9.505 (20) | 10.495 |
| backlog-adp@blank-aged2-3 | 2 | +6.433 ms, 76,710 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 9.541 (20) | 10.459 |
| backlog-adp@blank-aged2-4 | 2 | none | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 9.539 (20) | 10.461 |
| backlog-adp@blank-aged2-5 | 2 | none | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 9.544 (20) | 10.456 |
| backlog-adp@blank-aged2-6 | 2 | +4.331 ms, 77,153 (0.772 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 9.574 (20) | 10.426 |
| backlog-adp@blank-aged2-7 | 2 | +4.191 ms, 77,153 (0.772 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 9.457 (20) | 10.543 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 8.705 (20) | 11.295 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 8.799 (20) | 11.201 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 9.122 (20) | 10.878 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 9.601 (20) | 10.399 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 9.502 (20) | 10.498 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 9.535 (20) | 10.465 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 9.546 (20) | 10.454 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 9.414 (20) | 10.586 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 8.710 (20) | 11.290 |
| backlog-adp@program-aged2-1 | 2 | none | +8.883 ms, 80,500 (0.805 ms), issue | `backlog-adp@program-aged2-1.service.srp.last.if0` | 8.660 (20) | 11.340 |
| backlog-adp@program-aged2-2 | 2 | +8.074 ms, 80,567 (0.806 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 9.553 (20) | 10.447 |
| backlog-adp@program-aged2-3 | 2 | +6.529 ms, 80,522 (0.805 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 9.593 (20) | 10.407 |
| backlog-adp@program-aged2-4 | 2 | +5.727 ms, 80,567 (0.806 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 9.583 (20) | 10.417 |
| backlog-adp@program-aged2-5 | 2 | +4.332 ms, 80,600 (0.806 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 9.617 (20) | 10.383 |
| backlog-adp@program-aged2-6 | 2 | +4.323 ms, 80,547 (0.805 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 9.788 (20) | 10.212 |
| backlog-adp@program-aged2-7 | 2 | +4.087 ms, 80,547 (0.805 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 9.554 (20) | 10.446 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 8.690 (20) | 11.310 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 8.720 (20) | 11.280 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 8.926 (20) | 11.074 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 8.839 (20) | 11.161 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 8.724 (20) | 11.276 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 8.717 (20) | 11.283 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 8.751 (20) | 11.249 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 8.784 (20) | 11.216 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 8.677 (20) | 11.323 |
| backlog-adp@verify-aged2-1 | 2 | none | +8.774 ms, 77,456 (0.775 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 8.737 (20) | 11.263 |
| backlog-adp@verify-aged2-2 | 2 | +8.063 ms, 77,376 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 9.503 (20) | 10.497 |
| backlog-adp@verify-aged2-3 | 2 | +6.610 ms, 77,311 (0.773 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 9.530 (20) | 10.470 |
| backlog-adp@verify-aged2-4 | 2 | +5.794 ms, 77,311 (0.773 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 9.506 (20) | 10.494 |
| backlog-adp@verify-aged2-5 | 2 | +5.009 ms, 77,353 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 9.517 (20) | 10.483 |
| backlog-adp@verify-aged2-6 | 2 | +4.173 ms, 77,636 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 9.616 (20) | 10.384 |
| backlog-adp@verify-aged2-7 | 2 | +3.021 ms, 77,294 (0.773 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 9.634 (20) | 10.366 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 8.664 (20) | 11.336 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 8.809 (20) | 11.191 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 8.849 (20) | 11.151 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 8.742 (20) | 11.258 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 8.709 (20) | 11.291 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 8.719 (20) | 11.281 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 8.742 (20) | 11.258 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 8.837 (20) | 11.163 |

Least margin over the aged windows: 10.212 ms, `backlog-adp@program-aged2-6.service.srp.last.if0` at 9.788 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.406 | 6,070 | 102 | 2 | 30.894 | yes | within |
| save-held | 2019.189 | 4,070 | 102 | - | 14.417 | no | within |
| save-starved | 4049.088 | 4,070 | 102 | - | 31.020 | yes | within |
| save | 2019.678 | 4,070 | 102 | - | 10.763 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 96,424 (0.964) | 78,540 (0.785) |
| save-second | 520 | 79,932 (0.799) | 78,086 (0.781) |
| backlog-adp@blank-0 | 299 | 90,621 (0.906) | 76,150 (0.761) |
| backlog-adp@blank-1 | 299 | 91,131 (0.911) | 76,152 (0.762) |
| backlog-adp@blank-2 | 299 | 91,712 (0.917) | 76,288 (0.763) |
| backlog-adp@blank-3 | 299 | 91,867 (0.919) | 76,267 (0.763) |
| backlog-adp@blank-4 | 299 | 91,867 (0.919) | 76,267 (0.763) |
| backlog-adp@blank-5 | 299 | 91,776 (0.918) | 76,205 (0.762) |
| backlog-adp@blank-6 | 299 | 91,664 (0.917) | 76,240 (0.762) |
| backlog-adp@blank-7 | 299 | 91,664 (0.917) | 76,240 (0.762) |
| backlog-adp@program-0 | 328 | 96,012 (0.960) | 78,979 (0.790) |
| backlog-adp@program-1 | 328 | 96,204 (0.962) | 79,043 (0.790) |
| backlog-adp@program-2 | 328 | 96,048 (0.960) | 79,062 (0.791) |
| backlog-adp@program-3 | 328 | 96,048 (0.960) | 79,062 (0.791) |
| backlog-adp@program-4 | 329 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@program-5 | 329 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@program-6 | 329 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@program-7 | 329 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-0 | 355 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-1 | 355 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-2 | 355 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-3 | 355 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-4 | 355 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-5 | 355 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-6 | 355 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-7 | 355 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@blank-aged2-0 | 298 | 92,101 (0.921) | 76,501 (0.765) |
| backlog-adp@blank-aged2-1 | 297 | 76,790 (0.768) | 75,907 (0.759) |
| backlog-adp@blank-aged2-2 | 297 | 87,444 (0.874) | 76,169 (0.762) |
| backlog-adp@blank-aged2-3 | 297 | 76,710 (0.767) | 75,941 (0.759) |
| backlog-adp@blank-aged2-4 | 297 | 87,369 (0.874) | 76,169 (0.762) |
| backlog-adp@blank-aged2-5 | 297 | 87,358 (0.874) | 76,169 (0.762) |
| backlog-adp@blank-aged2-6 | 297 | 77,153 (0.772) | 75,858 (0.759) |
| backlog-adp@blank-aged2-7 | 297 | 77,153 (0.772) | 75,858 (0.759) |
| backlog-adp@blank-aged1-0 | 298 | 96,376 (0.964) | 76,464 (0.765) |
| backlog-adp@blank-aged1-1 | 297 | 96,873 (0.969) | 76,579 (0.766) |
| backlog-adp@blank-aged1-2 | 297 | 97,490 (0.975) | 76,526 (0.765) |
| backlog-adp@blank-aged1-3 | 297 | 92,187 (0.922) | 76,601 (0.766) |
| backlog-adp@blank-aged1-4 | 297 | 92,025 (0.920) | 76,601 (0.766) |
| backlog-adp@blank-aged1-5 | 297 | 91,946 (0.919) | 76,522 (0.765) |
| backlog-adp@blank-aged1-6 | 297 | 92,014 (0.920) | 76,568 (0.766) |
| backlog-adp@blank-aged1-7 | 297 | 92,073 (0.921) | 76,568 (0.766) |
| backlog-adp@program-aged2-0 | 327 | 96,012 (0.960) | 79,043 (0.790) |
| backlog-adp@program-aged2-1 | 326 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@program-aged2-2 | 326 | 96,012 (0.960) | 78,676 (0.787) |
| backlog-adp@program-aged2-3 | 326 | 96,012 (0.960) | 78,674 (0.787) |
| backlog-adp@program-aged2-4 | 326 | 96,012 (0.960) | 78,676 (0.787) |
| backlog-adp@program-aged2-5 | 326 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@program-aged2-6 | 326 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@program-aged2-7 | 326 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@program-aged1-0 | 327 | 96,012 (0.960) | 79,041 (0.790) |
| backlog-adp@program-aged1-1 | 326 | 96,012 (0.960) | 79,043 (0.790) |
| backlog-adp@program-aged1-2 | 326 | 96,012 (0.960) | 79,062 (0.791) |
| backlog-adp@program-aged1-3 | 326 | 96,012 (0.960) | 79,062 (0.791) |
| backlog-adp@program-aged1-4 | 326 | 96,012 (0.960) | 79,062 (0.791) |
| backlog-adp@program-aged1-5 | 326 | 96,012 (0.960) | 79,062 (0.791) |
| backlog-adp@program-aged1-6 | 326 | 96,012 (0.960) | 79,062 (0.791) |
| backlog-adp@program-aged1-7 | 326 | 96,012 (0.960) | 79,041 (0.790) |
| backlog-adp@verify-aged2-0 | 356 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-aged2-1 | 355 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-aged2-2 | 355 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-aged2-3 | 355 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-aged2-4 | 355 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-aged2-5 | 355 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-aged2-6 | 355 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-aged2-7 | 355 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-aged1-0 | 356 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-aged1-1 | 355 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-aged1-2 | 355 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-aged1-3 | 355 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-aged1-4 | 355 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-aged1-5 | 355 | 96,012 (0.960) | 78,555 (0.786) |
| backlog-adp@verify-aged1-6 | 355 | 100,508 (1.005) | 78,555 (0.786) |
| backlog-adp@verify-aged1-7 | 355 | 96,012 (0.960) | 78,555 (0.786) |
| adp-advertise | 577 | 21,517 (0.215) | 2,629 (0.026) |
| save-held | 722 | 95,436 (0.954) | 78,825 (0.788) |
| save-starved | 418 | 80,620 (0.806) | 78,396 (0.784) |
| acmp-noresp | 615 | 96,077 (0.961) | 78,505 (0.785) |
| save | 585 | 95,004 (0.950) | 78,372 (0.784) |
| srp | 271 | 21,490 (0.215) | 2,629 (0.026) |
| backlog | 265 | 21,490 (0.215) | 2,629 (0.026) |
| backlog-adp | 271 | 21,490 (0.215) | 2,673 (0.027) |
| backlog-adp-refill | 274 | 21,490 (0.215) | 2,673 (0.027) |
| backlog-owed | 276 | 21,490 (0.215) | 2,640 (0.026) |
| acmp-disc | 305 | 96,068 (0.961) | 78,507 (0.785) |
| maap | 169 | 21,336 (0.213) | 2,629 (0.026) |
| adp-link | 79 | 21,307 (0.213) | 2,629 (0.026) |
| adp-gm | 79 | 21,307 (0.213) | 2,629 (0.026) |
| adp-discover | 79 | 21,307 (0.213) | 2,629 (0.026) |
| control | 79 | 21,307 (0.213) | 2,629 (0.026) |
| aecp-fanout | 80 | 21,307 (0.213) | 2,629 (0.026) |
| acmp-cmd | 65 | 21,307 (0.213) | 2,629 (0.026) |
| aecp | 79 | 21,307 (0.213) | 2,629 (0.026) |
| aecp-largest-notice | 78 | 21,307 (0.213) | 2,629 (0.026) |
| datapath-events | 69 | 21,307 (0.213) | 2,629 (0.026) |
| fixture | 54 | 19,418 (0.194) | 2,629 (0.026) |

Longest pass that carries a step: 100,508 CPU cycles (1.005 ms), backlog-adp@verify-aged1-6; longest step: 79,062 (0.791 ms), backlog-adp@program-2.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 7,683 | 0.077 | 20 | 20 | fits | 32,674 | 19 (14) | 0.891 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 429,135 | 4.291 | 20 | 20 | fits | 111,898 | 163 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 368,114 | 3.681 | 20 | 200 | fits | 146,128 | 226 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 479,396 | 4.794 | 20 | 200 | fits | 111,898 | 163 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 369,038 | 3.690 | 20 | 20 | fits | 146,128 | 226 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 480,100 | 4.801 | 20 | 20 | fits | 111,898 | 163 | 0.384 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 226,550 | 2.265 | 20 | 24 | fits | 149,220 | 155 | 0.436 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 371,688 | 3.717 | 20 | 24 | fits | 146,128 | 226 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 371,622 | 3.716 | 20 | 50 | fits | 146,128 | 226 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 483,124 | 4.831 | 20 | 50 | fits | 111,898 | 163 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 569,126 | 5.691 | 20 | 20 | fits | 86,068 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 951,391 | 9.514 | 20 | 20 | fits | 59,171 | 24 | 0.613 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 356,859 | 3.569 | 20 | 20 | fits | 111,757 | 163 | 0.386 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 303,242 | 3.032 | 20 | 200 | fits | 146,153 | 226 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 414,383 | 4.144 | 20 | 200 | fits | 111,757 | 163 | 0.386 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 304,166 | 3.042 | 20 | 20 | fits | 146,153 | 226 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 415,087 | 4.151 | 20 | 20 | fits | 111,757 | 163 | 0.386 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 161,653 | 1.617 | 20 | 24 | fits | 148,398 | 155 | 0.432 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 306,816 | 3.068 | 20 | 24 | fits | 146,153 | 226 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 306,750 | 3.067 | 20 | 50 | fits | 146,153 | 226 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 418,111 | 4.181 | 20 | 50 | fits | 111,757 | 163 | 0.386 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 504,121 | 5.041 | 20 | 20 | fits | 86,076 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 886,349 | 8.863 | 20 | 20 | fits | 59,239 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 351,941 | 3.519 | 20 | 20 | fits | 111,198 | 163 | 0.381 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 298,304 | 2.983 | 20 | 200 | fits | 145,887 | 226 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 408,886 | 4.089 | 20 | 200 | fits | 111,198 | 163 | 0.381 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 299,228 | 2.992 | 20 | 20 | fits | 145,887 | 226 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 409,590 | 4.096 | 20 | 20 | fits | 111,198 | 163 | 0.381 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 156,981 | 1.570 | 20 | 24 | fits | 148,398 | 155 | 0.432 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 301,878 | 3.019 | 20 | 24 | fits | 145,887 | 226 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 301,812 | 3.018 | 20 | 50 | fits | 145,887 | 226 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 412,614 | 4.126 | 20 | 50 | fits | 111,198 | 163 | 0.381 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 492,825 | 4.928 | 20 | 20 | fits | 80,277 | 31 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 887,840 | 8.878 | 20 | 20 | fits | 69,423 | 28 | 0.575 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 369,048 | 3.690 | 20 | 20 | fits | 116,348 | 170 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 294,232 | 2.942 | 20 | 200 | fits | 146,487 | 227 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 419,834 | 4.198 | 20 | 200 | fits | 116,348 | 170 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 295,156 | 2.952 | 20 | 20 | fits | 146,487 | 227 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 420,538 | 4.205 | 20 | 20 | fits | 116,348 | 170 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 152,309 | 1.523 | 20 | 24 | fits | 148,398 | 155 | 0.432 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 297,806 | 2.978 | 20 | 24 | fits | 146,487 | 227 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 297,740 | 2.977 | 20 | 50 | fits | 146,487 | 227 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 423,562 | 4.236 | 20 | 50 | fits | 116,348 | 170 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 509,621 | 5.096 | 20 | 20 | fits | 86,125 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 879,336 | 8.793 | 20 | 20 | fits | 59,201 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 356,476 | 3.565 | 20 | 20 | fits | 116,003 | 170 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 289,071 | 2.891 | 20 | 200 | fits | 145,998 | 227 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 414,482 | 4.145 | 20 | 200 | fits | 116,003 | 170 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 289,995 | 2.900 | 20 | 20 | fits | 145,998 | 227 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 415,186 | 4.152 | 20 | 20 | fits | 116,003 | 170 | 0.422 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 147,637 | 1.476 | 20 | 24 | fits | 148,398 | 155 | 0.432 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 292,645 | 2.926 | 20 | 24 | fits | 145,998 | 227 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 292,579 | 2.926 | 20 | 50 | fits | 145,998 | 227 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 418,210 | 4.182 | 20 | 50 | fits | 116,003 | 170 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 504,353 | 5.044 | 20 | 20 | fits | 86,209 | 28 | 0.746 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 874,476 | 8.745 | 20 | 20 | fits | 59,201 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 363,869 | 3.639 | 20 | 20 | fits | 111,157 | 163 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 310,228 | 3.102 | 20 | 200 | fits | 147,540 | 231 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 420,769 | 4.208 | 20 | 200 | fits | 111,157 | 163 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 311,152 | 3.112 | 20 | 20 | fits | 147,540 | 231 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 421,473 | 4.215 | 20 | 20 | fits | 111,157 | 163 | 0.379 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 158,058 | 1.581 | 20 | 24 | fits | 148,450 | 156 | 0.433 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 313,802 | 3.138 | 20 | 24 | fits | 147,540 | 231 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 313,736 | 3.137 | 20 | 50 | fits | 147,540 | 231 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 424,497 | 4.245 | 20 | 50 | fits | 111,157 | 163 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 504,528 | 5.045 | 20 | 20 | fits | 80,097 | 30 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 878,573 | 8.786 | 20 | 20 | fits | 59,149 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 354,819 | 3.548 | 20 | 20 | fits | 119,218 | 169 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 293,985 | 2.940 | 20 | 200 | fits | 146,305 | 226 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 412,587 | 4.126 | 20 | 200 | fits | 119,218 | 169 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 294,909 | 2.949 | 20 | 20 | fits | 146,305 | 226 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 413,291 | 4.133 | 20 | 20 | fits | 119,218 | 169 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 152,244 | 1.522 | 20 | 24 | fits | 148,514 | 155 | 0.432 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 297,559 | 2.976 | 20 | 24 | fits | 146,305 | 226 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 297,493 | 2.975 | 20 | 50 | fits | 146,305 | 226 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 416,315 | 4.163 | 20 | 50 | fits | 119,218 | 169 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 502,355 | 5.024 | 20 | 20 | fits | 86,106 | 28 | 0.746 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 884,527 | 8.845 | 20 | 20 | fits | 59,459 | 24 | 0.624 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 349,931 | 3.499 | 20 | 20 | fits | 120,018 | 175 | 0.361 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 287,390 | 2.874 | 20 | 200 | fits | 144,382 | 220 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 406,792 | 4.068 | 20 | 200 | fits | 120,018 | 175 | 0.361 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 288,314 | 2.883 | 20 | 20 | fits | 144,382 | 220 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 407,496 | 4.075 | 20 | 20 | fits | 120,018 | 175 | 0.361 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 147,572 | 1.476 | 20 | 24 | fits | 148,514 | 155 | 0.432 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 290,964 | 2.910 | 20 | 24 | fits | 144,382 | 220 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 290,898 | 2.909 | 20 | 50 | fits | 144,382 | 220 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 410,520 | 4.105 | 20 | 50 | fits | 120,018 | 175 | 0.361 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 496,444 | 4.964 | 20 | 20 | fits | 85,990 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 878,577 | 8.786 | 20 | 20 | fits | 59,191 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 358,151 | 3.582 | 20 | 20 | fits | 112,322 | 164 | 0.387 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 297,130 | 2.971 | 20 | 200 | fits | 145,246 | 226 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 408,836 | 4.088 | 20 | 200 | fits | 112,322 | 164 | 0.387 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 298,054 | 2.981 | 20 | 20 | fits | 145,246 | 226 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 409,540 | 4.095 | 20 | 20 | fits | 112,322 | 164 | 0.387 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 156,448 | 1.564 | 20 | 24 | fits | 146,495 | 155 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 300,704 | 3.007 | 20 | 24 | fits | 145,246 | 226 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 300,638 | 3.006 | 20 | 50 | fits | 145,246 | 226 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 412,564 | 4.126 | 20 | 50 | fits | 112,322 | 164 | 0.387 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 501,739 | 5.017 | 20 | 20 | fits | 78,704 | 31 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 876,400 | 8.764 | 20 | 20 | fits | 59,239 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 360,005 | 3.600 | 20 | 20 | fits | 112,144 | 166 | 0.367 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 297,654 | 2.977 | 20 | 200 | fits | 145,776 | 227 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 409,182 | 4.092 | 20 | 200 | fits | 112,144 | 166 | 0.367 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 298,578 | 2.986 | 20 | 20 | fits | 145,776 | 227 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 409,886 | 4.099 | 20 | 20 | fits | 112,144 | 166 | 0.367 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 147,248 | 1.472 | 20 | 24 | fits | 146,639 | 156 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 301,228 | 3.012 | 20 | 24 | fits | 145,776 | 227 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 301,162 | 3.012 | 20 | 50 | fits | 145,776 | 227 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 412,910 | 4.129 | 20 | 50 | fits | 112,144 | 166 | 0.367 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 498,335 | 4.983 | 20 | 20 | fits | 85,491 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 868,227 | 8.682 | 20 | 20 | fits | 59,201 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 340,241 | 3.402 | 20 | 20 | fits | 111,061 | 163 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 286,741 | 2.867 | 20 | 200 | fits | 144,983 | 226 | 0.404 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 397,186 | 3.972 | 20 | 200 | fits | 111,061 | 163 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 287,665 | 2.877 | 20 | 20 | fits | 144,983 | 226 | 0.404 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 397,890 | 3.979 | 20 | 20 | fits | 111,061 | 163 | 0.379 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 146,322 | 1.463 | 20 | 24 | fits | 146,175 | 155 | 0.418 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 290,315 | 2.903 | 20 | 24 | fits | 144,983 | 226 | 0.404 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 290,249 | 2.902 | 20 | 50 | fits | 144,983 | 226 | 0.404 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 400,914 | 4.009 | 20 | 50 | fits | 111,061 | 163 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 480,316 | 4.803 | 20 | 20 | fits | 79,468 | 30 | 0.781 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 872,921 | 8.729 | 20 | 20 | fits | 69,691 | 28 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 346,446 | 3.464 | 20 | 20 | fits | 118,779 | 184 | 0.381 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 293,022 | 2.930 | 20 | 200 | fits | 145,538 | 209 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 411,185 | 4.112 | 20 | 200 | fits | 118,779 | 184 | 0.381 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 293,946 | 2.939 | 20 | 20 | fits | 145,538 | 209 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 411,889 | 4.119 | 20 | 20 | fits | 118,779 | 184 | 0.381 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 152,048 | 1.520 | 20 | 24 | fits | 146,204 | 155 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 296,596 | 2.966 | 20 | 24 | fits | 145,538 | 209 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 296,530 | 2.965 | 20 | 50 | fits | 145,538 | 209 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 414,913 | 4.149 | 20 | 50 | fits | 118,779 | 184 | 0.381 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 500,443 | 5.004 | 20 | 20 | fits | 85,596 | 29 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 882,438 | 8.824 | 20 | 20 | fits | 59,239 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 365,191 | 3.652 | 20 | 20 | fits | 116,348 | 170 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 290,366 | 2.904 | 20 | 200 | fits | 145,387 | 227 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 415,977 | 4.160 | 20 | 200 | fits | 116,348 | 170 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 291,290 | 2.913 | 20 | 20 | fits | 145,387 | 227 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 416,681 | 4.167 | 20 | 20 | fits | 116,348 | 170 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 149,543 | 1.495 | 20 | 24 | fits | 147,128 | 155 | 0.426 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 293,940 | 2.939 | 20 | 24 | fits | 145,387 | 227 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 293,874 | 2.939 | 20 | 50 | fits | 145,387 | 227 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 419,705 | 4.197 | 20 | 50 | fits | 116,348 | 170 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 505,023 | 5.050 | 20 | 20 | fits | 85,384 | 28 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 869,114 | 8.691 | 20 | 20 | fits | 49,017 | 20 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 352,432 | 3.524 | 20 | 20 | fits | 112,388 | 166 | 0.369 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 289,882 | 2.899 | 20 | 200 | fits | 143,922 | 222 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 401,654 | 4.017 | 20 | 200 | fits | 112,388 | 166 | 0.369 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 290,806 | 2.908 | 20 | 20 | fits | 143,922 | 222 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 402,358 | 4.024 | 20 | 20 | fits | 112,388 | 166 | 0.369 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 150,524 | 1.505 | 20 | 24 | fits | 146,204 | 155 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 293,456 | 2.935 | 20 | 24 | fits | 143,922 | 222 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 293,390 | 2.934 | 20 | 50 | fits | 143,922 | 222 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 405,382 | 4.054 | 20 | 50 | fits | 112,388 | 166 | 0.369 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 490,882 | 4.909 | 20 | 20 | fits | 85,566 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 878,792 | 8.788 | 20 | 20 | fits | 65,930 | 31 | 0.698 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 349,952 | 3.500 | 20 | 20 | fits | 111,455 | 163 | 0.381 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 296,594 | 2.966 | 20 | 200 | fits | 144,966 | 226 | 0.404 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 407,433 | 4.074 | 20 | 200 | fits | 111,455 | 163 | 0.381 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 297,518 | 2.975 | 20 | 20 | fits | 144,966 | 226 | 0.404 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 408,137 | 4.081 | 20 | 20 | fits | 111,455 | 163 | 0.381 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 156,192 | 1.562 | 20 | 24 | fits | 146,175 | 155 | 0.418 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 300,168 | 3.002 | 20 | 24 | fits | 144,966 | 226 | 0.404 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 300,102 | 3.001 | 20 | 50 | fits | 144,966 | 226 | 0.404 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 411,161 | 4.112 | 20 | 50 | fits | 111,455 | 163 | 0.381 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 490,819 | 4.908 | 20 | 20 | fits | 79,724 | 31 | 0.780 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 882,946 | 8.829 | 20 | 20 | fits | 69,423 | 28 | 0.575 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 355,552 | 3.556 | 20 | 20 | fits | 123,006 | 190 | 0.417 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 288,363 | 2.884 | 20 | 200 | fits | 146,079 | 210 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 420,835 | 4.208 | 20 | 200 | fits | 123,006 | 190 | 0.417 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 289,287 | 2.893 | 20 | 20 | fits | 146,079 | 210 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 421,539 | 4.215 | 20 | 20 | fits | 123,006 | 190 | 0.417 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 146,848 | 1.468 | 20 | 24 | fits | 146,175 | 155 | 0.418 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 291,937 | 2.919 | 20 | 24 | fits | 146,079 | 210 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 291,871 | 2.919 | 20 | 50 | fits | 146,079 | 210 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 424,563 | 4.246 | 20 | 50 | fits | 123,006 | 190 | 0.417 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 510,309 | 5.103 | 20 | 20 | fits | 85,812 | 28 | 0.747 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 874,413 | 8.744 | 20 | 20 | fits | 49,017 | 20 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 369,818 | 3.698 | 20 | 20 | fits | 110,942 | 163 | 0.377 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 316,392 | 3.164 | 20 | 200 | fits | 145,008 | 226 | 0.404 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 426,718 | 4.267 | 20 | 200 | fits | 110,942 | 163 | 0.377 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 317,316 | 3.173 | 20 | 20 | fits | 145,008 | 226 | 0.404 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 427,422 | 4.274 | 20 | 20 | fits | 110,942 | 163 | 0.377 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 175,948 | 1.759 | 20 | 24 | fits | 147,042 | 155 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 319,966 | 3.200 | 20 | 24 | fits | 145,008 | 226 | 0.404 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 319,900 | 3.199 | 20 | 50 | fits | 145,008 | 226 | 0.404 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 430,446 | 4.304 | 20 | 50 | fits | 110,942 | 163 | 0.377 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 516,332 | 5.163 | 20 | 20 | fits | 85,952 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 898,627 | 8.986 | 20 | 20 | fits | 59,171 | 24 | 0.613 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 350,675 | 3.507 | 20 | 20 | fits | 111,654 | 163 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 297,116 | 2.971 | 20 | 200 | fits | 145,285 | 226 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 408,154 | 4.082 | 20 | 200 | fits | 111,654 | 163 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 298,040 | 2.980 | 20 | 20 | fits | 145,285 | 226 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 408,858 | 4.089 | 20 | 20 | fits | 111,654 | 163 | 0.384 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 156,395 | 1.564 | 20 | 24 | fits | 146,469 | 155 | 0.421 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 300,690 | 3.007 | 20 | 24 | fits | 145,285 | 226 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 300,624 | 3.006 | 20 | 50 | fits | 145,285 | 226 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 411,882 | 4.119 | 20 | 50 | fits | 111,654 | 163 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 497,779 | 4.978 | 20 | 20 | fits | 85,963 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 887,280 | 8.873 | 20 | 20 | fits | 54,871 | 26 | 0.725 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 345,757 | 3.458 | 20 | 20 | fits | 111,519 | 164 | 0.382 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 292,178 | 2.922 | 20 | 200 | fits | 145,019 | 226 | 0.404 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 403,081 | 4.031 | 20 | 200 | fits | 111,519 | 164 | 0.382 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 293,102 | 2.931 | 20 | 20 | fits | 145,019 | 226 | 0.404 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 403,785 | 4.038 | 20 | 20 | fits | 111,519 | 164 | 0.382 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 151,723 | 1.517 | 20 | 24 | fits | 146,469 | 155 | 0.421 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 295,752 | 2.958 | 20 | 24 | fits | 145,019 | 226 | 0.404 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 295,686 | 2.957 | 20 | 50 | fits | 145,019 | 226 | 0.404 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 406,809 | 4.068 | 20 | 50 | fits | 111,519 | 164 | 0.382 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 496,517 | 4.965 | 20 | 20 | fits | 79,237 | 31 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 876,994 | 8.770 | 20 | 20 | fits | 69,494 | 28 | 0.577 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 362,917 | 3.629 | 20 | 20 | fits | 116,334 | 170 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 288,106 | 2.881 | 20 | 200 | fits | 145,619 | 227 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 413,703 | 4.137 | 20 | 200 | fits | 116,334 | 170 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 289,030 | 2.890 | 20 | 20 | fits | 145,619 | 227 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 414,407 | 4.144 | 20 | 20 | fits | 116,334 | 170 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 147,051 | 1.471 | 20 | 24 | fits | 146,469 | 155 | 0.421 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 291,680 | 2.917 | 20 | 24 | fits | 145,619 | 227 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 291,614 | 2.916 | 20 | 50 | fits | 145,619 | 227 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 417,431 | 4.174 | 20 | 50 | fits | 116,334 | 170 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 503,415 | 5.034 | 20 | 20 | fits | 86,050 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 873,216 | 8.732 | 20 | 20 | fits | 59,201 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 362,721 | 3.627 | 20 | 20 | fits | 111,772 | 163 | 0.385 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 309,089 | 3.091 | 20 | 200 | fits | 146,902 | 231 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 420,245 | 4.202 | 20 | 200 | fits | 111,772 | 163 | 0.385 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 310,013 | 3.100 | 20 | 20 | fits | 146,902 | 231 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 420,949 | 4.209 | 20 | 20 | fits | 111,772 | 163 | 0.385 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 157,557 | 1.576 | 20 | 24 | fits | 146,606 | 156 | 0.421 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 312,663 | 3.127 | 20 | 24 | fits | 146,902 | 231 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 312,597 | 3.126 | 20 | 50 | fits | 146,902 | 231 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 423,973 | 4.240 | 20 | 50 | fits | 111,772 | 163 | 0.385 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 503,961 | 5.040 | 20 | 20 | fits | 80,054 | 30 | 0.781 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 878,144 | 8.781 | 20 | 20 | fits | 59,201 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 365,192 | 3.652 | 20 | 20 | fits | 118,880 | 169 | 0.411 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 304,117 | 3.041 | 20 | 200 | fits | 145,006 | 226 | 0.404 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 422,381 | 4.224 | 20 | 200 | fits | 118,880 | 169 | 0.411 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 305,041 | 3.050 | 20 | 20 | fits | 145,006 | 226 | 0.404 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 423,085 | 4.231 | 20 | 20 | fits | 118,880 | 169 | 0.411 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 163,675 | 1.637 | 20 | 24 | fits | 146,550 | 156 | 0.421 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 307,691 | 3.077 | 20 | 24 | fits | 145,006 | 226 | 0.404 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 307,625 | 3.076 | 20 | 50 | fits | 145,006 | 226 | 0.404 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 426,109 | 4.261 | 20 | 50 | fits | 118,880 | 169 | 0.411 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 512,061 | 5.121 | 20 | 20 | fits | 86,018 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 894,310 | 8.943 | 20 | 20 | fits | 55,858 | 27 | 0.741 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 348,607 | 3.486 | 20 | 20 | fits | 119,340 | 169 | 0.414 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 287,651 | 2.877 | 20 | 200 | fits | 145,423 | 226 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 406,375 | 4.064 | 20 | 200 | fits | 119,340 | 169 | 0.414 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 288,575 | 2.886 | 20 | 20 | fits | 145,423 | 226 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 407,079 | 4.071 | 20 | 20 | fits | 119,340 | 169 | 0.414 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 146,792 | 1.468 | 20 | 24 | fits | 146,254 | 155 | 0.418 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 291,225 | 2.912 | 20 | 24 | fits | 145,423 | 226 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 291,159 | 2.912 | 20 | 50 | fits | 145,423 | 226 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 410,103 | 4.101 | 20 | 50 | fits | 119,340 | 169 | 0.414 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 496,030 | 4.960 | 20 | 20 | fits | 85,993 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 878,484 | 8.785 | 20 | 20 | fits | 59,507 | 24 | 0.624 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 351,017 | 3.510 | 20 | 20 | fits | 119,280 | 172 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 297,470 | 2.975 | 20 | 200 | fits | 144,862 | 224 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 416,134 | 4.161 | 20 | 200 | fits | 119,280 | 172 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 298,394 | 2.984 | 20 | 20 | fits | 144,862 | 224 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 416,838 | 4.168 | 20 | 20 | fits | 119,280 | 172 | 0.372 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 157,172 | 1.572 | 20 | 24 | fits | 146,265 | 155 | 0.418 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 301,044 | 3.010 | 20 | 24 | fits | 144,862 | 224 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 300,978 | 3.010 | 20 | 50 | fits | 144,862 | 224 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 419,862 | 4.199 | 20 | 50 | fits | 119,280 | 172 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 505,684 | 5.057 | 20 | 20 | fits | 85,888 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 888,064 | 8.881 | 20 | 20 | fits | 59,239 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 354,556 | 3.546 | 20 | 20 | fits | 116,966 | 175 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 285,861 | 2.859 | 20 | 200 | fits | 146,608 | 232 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 412,582 | 4.126 | 20 | 200 | fits | 116,966 | 175 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 286,785 | 2.868 | 20 | 20 | fits | 146,608 | 232 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 413,286 | 4.133 | 20 | 20 | fits | 116,966 | 175 | 0.422 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 143,817 | 1.438 | 20 | 24 | fits | 149,812 | 157 | 0.439 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 289,435 | 2.894 | 20 | 24 | fits | 146,608 | 232 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 289,369 | 2.894 | 20 | 50 | fits | 146,608 | 232 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 416,310 | 4.163 | 20 | 50 | fits | 116,966 | 175 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 501,605 | 5.016 | 20 | 20 | fits | 85,361 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 865,392 | 8.654 | 20 | 20 | fits | 48,977 | 20 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 357,126 | 3.571 | 20 | 20 | fits | 111,728 | 198 | 0.397 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 296,568 | 2.966 | 20 | 200 | fits | 144,970 | 234 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 407,680 | 4.077 | 20 | 200 | fits | 111,728 | 198 | 0.397 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 297,492 | 2.975 | 20 | 20 | fits | 144,970 | 234 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 408,384 | 4.084 | 20 | 20 | fits | 111,728 | 198 | 0.397 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 145,905 | 1.459 | 20 | 24 | fits | 149,771 | 121 | 0.427 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 300,142 | 3.001 | 20 | 24 | fits | 144,970 | 234 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 300,076 | 3.001 | 20 | 50 | fits | 144,970 | 234 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 411,408 | 4.114 | 20 | 50 | fits | 111,728 | 198 | 0.397 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 496,484 | 4.965 | 20 | 20 | fits | 85,142 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 865,971 | 8.660 | 20 | 20 | fits | 54,704 | 26 | 0.724 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 339,585 | 3.396 | 20 | 20 | fits | 114,508 | 169 | 0.403 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 283,339 | 2.833 | 20 | 200 | fits | 146,119 | 231 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 397,231 | 3.972 | 20 | 200 | fits | 114,508 | 169 | 0.403 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 284,263 | 2.843 | 20 | 20 | fits | 146,119 | 231 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 397,935 | 3.979 | 20 | 20 | fits | 114,508 | 169 | 0.403 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 141,784 | 1.418 | 20 | 24 | fits | 147,380 | 157 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 286,913 | 2.869 | 20 | 24 | fits | 146,119 | 231 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 286,847 | 2.868 | 20 | 50 | fits | 146,119 | 231 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 400,959 | 4.010 | 20 | 50 | fits | 114,508 | 169 | 0.403 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 486,161 | 4.862 | 20 | 20 | fits | 85,268 | 28 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 950,525 | 9.505 | 20 | 20 | fits | 66,424 | 31 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 348,307 | 3.483 | 20 | 20 | fits | 111,676 | 163 | 0.382 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 287,335 | 2.873 | 20 | 200 | fits | 145,308 | 226 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 398,395 | 3.984 | 20 | 200 | fits | 111,676 | 163 | 0.382 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 288,259 | 2.883 | 20 | 20 | fits | 145,308 | 226 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 399,099 | 3.991 | 20 | 20 | fits | 111,676 | 163 | 0.382 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 146,591 | 1.466 | 20 | 24 | fits | 145,687 | 152 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 290,909 | 2.909 | 20 | 24 | fits | 145,308 | 226 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 290,843 | 2.908 | 20 | 50 | fits | 145,308 | 226 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 402,123 | 4.021 | 20 | 50 | fits | 111,676 | 163 | 0.382 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 487,234 | 4.872 | 20 | 20 | fits | 85,177 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 954,107 | 9.541 | 20 | 20 | fits | 59,519 | 24 | 0.624 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 343,120 | 3.431 | 20 | 20 | fits | 111,235 | 163 | 0.381 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 289,793 | 2.898 | 20 | 200 | fits | 144,958 | 226 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 400,412 | 4.004 | 20 | 200 | fits | 111,235 | 163 | 0.381 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 290,717 | 2.907 | 20 | 20 | fits | 144,958 | 226 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 401,116 | 4.011 | 20 | 20 | fits | 111,235 | 163 | 0.381 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 149,399 | 1.494 | 20 | 24 | fits | 145,687 | 152 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 293,367 | 2.934 | 20 | 24 | fits | 144,958 | 226 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 293,301 | 2.933 | 20 | 50 | fits | 144,958 | 226 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 404,140 | 4.041 | 20 | 50 | fits | 111,235 | 163 | 0.381 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 489,259 | 4.893 | 20 | 20 | fits | 85,185 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 953,915 | 9.539 | 20 | 20 | fits | 69,329 | 28 | 0.575 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 354,130 | 3.541 | 20 | 20 | fits | 112,101 | 166 | 0.368 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 291,710 | 2.917 | 20 | 200 | fits | 144,067 | 222 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 403,195 | 4.032 | 20 | 200 | fits | 112,101 | 166 | 0.368 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 292,634 | 2.926 | 20 | 20 | fits | 144,067 | 222 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 403,899 | 4.039 | 20 | 20 | fits | 112,101 | 166 | 0.368 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 152,207 | 1.522 | 20 | 24 | fits | 145,687 | 152 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 295,284 | 2.953 | 20 | 24 | fits | 144,067 | 222 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 295,218 | 2.952 | 20 | 50 | fits | 144,067 | 222 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 406,923 | 4.069 | 20 | 50 | fits | 112,101 | 166 | 0.368 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 489,315 | 4.893 | 20 | 20 | fits | 82,458 | 37 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 954,438 | 9.544 | 20 | 20 | fits | 59,153 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 369,806 | 3.698 | 20 | 20 | fits | 122,516 | 176 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 296,143 | 2.961 | 20 | 200 | fits | 145,692 | 227 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 427,755 | 4.278 | 20 | 200 | fits | 122,516 | 176 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 297,067 | 2.971 | 20 | 20 | fits | 145,692 | 227 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 428,459 | 4.285 | 20 | 20 | fits | 122,516 | 176 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 155,015 | 1.550 | 20 | 24 | fits | 145,687 | 152 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 299,717 | 2.997 | 20 | 24 | fits | 145,692 | 227 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 299,651 | 2.997 | 20 | 50 | fits | 145,692 | 227 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 431,483 | 4.315 | 20 | 50 | fits | 122,516 | 176 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 593,649 | 5.936 | 20 | 20 | fits | 85,079 | 29 | 0.738 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 957,436 | 9.574 | 20 | 20 | fits | 48,977 | 20 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 363,968 | 3.640 | 20 | 20 | fits | 113,646 | 180 | 0.445 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 291,026 | 2.910 | 20 | 200 | fits | 149,885 | 252 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 413,768 | 4.138 | 20 | 200 | fits | 113,646 | 180 | 0.445 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 291,950 | 2.920 | 20 | 20 | fits | 149,885 | 252 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 414,472 | 4.145 | 20 | 20 | fits | 113,646 | 180 | 0.445 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 145,705 | 1.457 | 20 | 24 | fits | 149,545 | 120 | 0.426 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 294,600 | 2.946 | 20 | 24 | fits | 149,885 | 252 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 294,534 | 2.945 | 20 | 50 | fits | 149,885 | 252 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 417,496 | 4.175 | 20 | 50 | fits | 113,646 | 180 | 0.445 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 571,896 | 5.719 | 20 | 20 | fits | 77,313 | 30 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 945,711 | 9.457 | 20 | 20 | fits | 59,153 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 349,374 | 3.494 | 20 | 20 | fits | 111,799 | 163 | 0.381 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 288,407 | 2.884 | 20 | 200 | fits | 147,129 | 231 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 399,590 | 3.996 | 20 | 200 | fits | 111,799 | 163 | 0.381 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 289,331 | 2.893 | 20 | 20 | fits | 147,129 | 231 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 400,294 | 4.003 | 20 | 20 | fits | 111,799 | 163 | 0.381 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 145,842 | 1.458 | 20 | 24 | fits | 147,704 | 152 | 0.426 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 291,981 | 2.920 | 20 | 24 | fits | 147,129 | 231 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 291,915 | 2.919 | 20 | 50 | fits | 147,129 | 231 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 403,318 | 4.033 | 20 | 50 | fits | 111,799 | 163 | 0.381 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 488,982 | 4.890 | 20 | 20 | fits | 85,730 | 29 | 0.741 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 870,497 | 8.705 | 20 | 20 | fits | 59,191 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 342,594 | 3.426 | 20 | 20 | fits | 111,591 | 164 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 289,303 | 2.893 | 20 | 200 | fits | 146,033 | 226 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 400,278 | 4.003 | 20 | 200 | fits | 111,591 | 164 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 290,227 | 2.902 | 20 | 20 | fits | 146,033 | 226 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 400,982 | 4.010 | 20 | 20 | fits | 111,591 | 164 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 147,834 | 1.478 | 20 | 24 | fits | 147,704 | 152 | 0.426 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 292,877 | 2.929 | 20 | 24 | fits | 146,033 | 226 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 292,811 | 2.928 | 20 | 50 | fits | 146,033 | 226 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 404,006 | 4.040 | 20 | 50 | fits | 111,591 | 164 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 493,682 | 4.937 | 20 | 20 | fits | 79,125 | 31 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 879,861 | 8.799 | 20 | 20 | fits | 71,196 | 30 | 0.705 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 366,749 | 3.667 | 20 | 20 | fits | 116,679 | 173 | 0.411 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 290,299 | 2.903 | 20 | 200 | fits | 145,037 | 223 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 416,338 | 4.163 | 20 | 200 | fits | 116,679 | 173 | 0.411 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 291,223 | 2.912 | 20 | 20 | fits | 145,037 | 223 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 417,042 | 4.170 | 20 | 20 | fits | 116,679 | 173 | 0.411 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 149,826 | 1.498 | 20 | 24 | fits | 147,704 | 152 | 0.426 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 293,873 | 2.939 | 20 | 24 | fits | 145,037 | 223 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 293,807 | 2.938 | 20 | 50 | fits | 145,037 | 223 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 420,066 | 4.201 | 20 | 50 | fits | 116,679 | 173 | 0.411 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 505,741 | 5.057 | 20 | 20 | fits | 85,741 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 912,178 | 9.122 | 20 | 20 | fits | 62,608 | 25 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 357,879 | 3.579 | 20 | 20 | fits | 111,588 | 163 | 0.385 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 304,287 | 3.043 | 20 | 200 | fits | 147,753 | 231 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 415,259 | 4.153 | 20 | 200 | fits | 111,588 | 163 | 0.385 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 305,211 | 3.052 | 20 | 20 | fits | 147,753 | 231 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 415,963 | 4.160 | 20 | 20 | fits | 111,588 | 163 | 0.385 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 151,807 | 1.518 | 20 | 24 | fits | 147,693 | 153 | 0.427 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 307,861 | 3.079 | 20 | 24 | fits | 147,753 | 231 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 307,795 | 3.078 | 20 | 50 | fits | 147,753 | 231 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 418,987 | 4.190 | 20 | 50 | fits | 111,588 | 163 | 0.385 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 504,539 | 5.045 | 20 | 20 | fits | 85,618 | 28 | 0.742 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 960,102 | 9.601 | 20 | 20 | fits | 65,933 | 31 | 0.699 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 356,233 | 3.562 | 20 | 20 | fits | 111,993 | 166 | 0.367 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 293,966 | 2.940 | 20 | 200 | fits | 145,007 | 222 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 405,343 | 4.053 | 20 | 200 | fits | 111,993 | 166 | 0.367 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 294,890 | 2.949 | 20 | 20 | fits | 145,007 | 222 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 406,047 | 4.060 | 20 | 20 | fits | 111,993 | 166 | 0.367 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 153,523 | 1.535 | 20 | 24 | fits | 147,754 | 152 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 297,540 | 2.975 | 20 | 24 | fits | 145,007 | 222 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 297,474 | 2.975 | 20 | 50 | fits | 145,007 | 222 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 409,071 | 4.091 | 20 | 50 | fits | 111,993 | 166 | 0.367 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 494,699 | 4.947 | 20 | 20 | fits | 85,694 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 950,154 | 9.502 | 20 | 20 | fits | 69,625 | 28 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 351,471 | 3.515 | 20 | 20 | fits | 111,427 | 163 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 298,040 | 2.980 | 20 | 200 | fits | 146,273 | 226 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 408,851 | 4.089 | 20 | 200 | fits | 111,427 | 163 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 298,964 | 2.990 | 20 | 20 | fits | 146,273 | 226 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 409,555 | 4.096 | 20 | 20 | fits | 111,427 | 163 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 156,331 | 1.563 | 20 | 24 | fits | 147,754 | 152 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 301,614 | 3.016 | 20 | 24 | fits | 146,273 | 226 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 301,548 | 3.015 | 20 | 50 | fits | 146,273 | 226 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 412,579 | 4.126 | 20 | 50 | fits | 111,427 | 163 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 497,892 | 4.979 | 20 | 20 | fits | 85,379 | 30 | 0.791 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 953,470 | 9.535 | 20 | 20 | fits | 69,367 | 28 | 0.575 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 368,927 | 3.689 | 20 | 20 | fits | 127,317 | 169 | 0.455 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 300,582 | 3.006 | 20 | 200 | fits | 146,007 | 226 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 427,283 | 4.273 | 20 | 200 | fits | 127,317 | 169 | 0.455 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 301,506 | 3.015 | 20 | 20 | fits | 146,007 | 226 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 427,987 | 4.280 | 20 | 20 | fits | 127,317 | 169 | 0.455 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 159,139 | 1.591 | 20 | 24 | fits | 147,754 | 152 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 304,156 | 3.042 | 20 | 24 | fits | 146,007 | 226 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 304,090 | 3.041 | 20 | 50 | fits | 146,007 | 226 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 431,011 | 4.310 | 20 | 50 | fits | 127,317 | 169 | 0.455 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 542,932 | 5.429 | 20 | 20 | fits | 84,767 | 30 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 954,619 | 9.546 | 20 | 20 | fits | 59,191 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 356,868 | 3.569 | 20 | 20 | fits | 128,344 | 170 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 288,409 | 2.884 | 20 | 200 | fits | 147,027 | 231 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 416,137 | 4.161 | 20 | 200 | fits | 128,344 | 170 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 289,333 | 2.893 | 20 | 20 | fits | 147,027 | 231 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 416,841 | 4.168 | 20 | 20 | fits | 128,344 | 170 | 0.461 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 145,946 | 1.459 | 20 | 24 | fits | 147,734 | 152 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 291,983 | 2.920 | 20 | 24 | fits | 147,027 | 231 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 291,917 | 2.919 | 20 | 50 | fits | 147,027 | 231 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 419,865 | 4.199 | 20 | 50 | fits | 128,344 | 170 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 535,538 | 5.355 | 20 | 20 | fits | 78,183 | 31 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 941,420 | 9.414 | 20 | 20 | fits | 59,191 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 361,216 | 3.612 | 20 | 20 | fits | 111,004 | 163 | 0.377 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 307,728 | 3.077 | 20 | 200 | fits | 146,776 | 231 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 418,116 | 4.181 | 20 | 200 | fits | 111,004 | 163 | 0.377 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 308,652 | 3.087 | 20 | 20 | fits | 146,776 | 231 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 418,820 | 4.188 | 20 | 20 | fits | 111,004 | 163 | 0.377 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 156,377 | 1.564 | 20 | 24 | fits | 145,765 | 153 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 311,302 | 3.113 | 20 | 24 | fits | 146,776 | 231 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 311,236 | 3.112 | 20 | 50 | fits | 146,776 | 231 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 421,844 | 4.218 | 20 | 50 | fits | 111,004 | 163 | 0.377 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 506,979 | 5.070 | 20 | 20 | fits | 85,201 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 870,983 | 8.710 | 20 | 20 | fits | 49,017 | 20 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 337,336 | 3.373 | 20 | 20 | fits | 111,574 | 163 | 0.382 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 283,859 | 2.839 | 20 | 200 | fits | 145,988 | 231 | 0.404 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 394,817 | 3.948 | 20 | 200 | fits | 111,574 | 163 | 0.382 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 284,783 | 2.848 | 20 | 20 | fits | 145,988 | 231 | 0.404 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 395,521 | 3.955 | 20 | 20 | fits | 111,574 | 163 | 0.382 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 142,435 | 1.424 | 20 | 24 | fits | 145,806 | 152 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 287,433 | 2.874 | 20 | 24 | fits | 145,988 | 231 | 0.404 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 287,367 | 2.874 | 20 | 50 | fits | 145,988 | 231 | 0.404 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 398,545 | 3.985 | 20 | 50 | fits | 111,574 | 163 | 0.382 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 483,691 | 4.837 | 20 | 20 | fits | 85,212 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 865,958 | 8.660 | 20 | 20 | fits | 59,507 | 24 | 0.624 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 346,985 | 3.470 | 20 | 20 | fits | 112,327 | 166 | 0.369 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 284,496 | 2.845 | 20 | 200 | fits | 145,050 | 227 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 396,207 | 3.962 | 20 | 200 | fits | 112,327 | 166 | 0.369 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 285,420 | 2.854 | 20 | 20 | fits | 145,050 | 227 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 396,911 | 3.969 | 20 | 20 | fits | 112,327 | 166 | 0.369 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 144,010 | 1.440 | 20 | 24 | fits | 145,806 | 152 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 288,070 | 2.881 | 20 | 24 | fits | 145,050 | 227 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 288,004 | 2.880 | 20 | 50 | fits | 145,050 | 227 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 399,935 | 3.999 | 20 | 50 | fits | 112,327 | 166 | 0.369 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 485,081 | 4.851 | 20 | 20 | fits | 85,212 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 955,275 | 9.553 | 20 | 20 | fits | 71,107 | 29 | 0.606 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 342,705 | 3.427 | 20 | 20 | fits | 111,669 | 163 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 289,176 | 2.892 | 20 | 200 | fits | 145,433 | 226 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 400,229 | 4.002 | 20 | 200 | fits | 111,669 | 163 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 290,100 | 2.901 | 20 | 20 | fits | 145,433 | 226 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 400,933 | 4.009 | 20 | 20 | fits | 111,669 | 163 | 0.384 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 148,307 | 1.483 | 20 | 24 | fits | 145,806 | 152 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 292,750 | 2.928 | 20 | 24 | fits | 145,433 | 226 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 292,684 | 2.927 | 20 | 50 | fits | 145,433 | 226 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 403,957 | 4.040 | 20 | 50 | fits | 111,669 | 163 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 489,231 | 4.892 | 20 | 20 | fits | 85,340 | 29 | 0.741 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 959,259 | 9.593 | 20 | 20 | fits | 69,423 | 28 | 0.575 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 345,395 | 3.454 | 20 | 20 | fits | 111,534 | 164 | 0.382 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 291,846 | 2.918 | 20 | 200 | fits | 145,167 | 226 | 0.406 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 402,764 | 4.028 | 20 | 200 | fits | 111,534 | 164 | 0.382 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 292,770 | 2.928 | 20 | 20 | fits | 145,167 | 226 | 0.406 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 403,468 | 4.035 | 20 | 20 | fits | 111,534 | 164 | 0.382 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 151,243 | 1.512 | 20 | 24 | fits | 145,806 | 152 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 295,420 | 2.954 | 20 | 24 | fits | 145,167 | 226 | 0.406 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 295,354 | 2.954 | 20 | 50 | fits | 145,167 | 226 | 0.406 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 406,492 | 4.065 | 20 | 50 | fits | 111,534 | 164 | 0.382 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 495,403 | 4.954 | 20 | 20 | fits | 78,588 | 31 | 0.778 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 958,298 | 9.583 | 20 | 20 | fits | 69,423 | 28 | 0.575 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 376,985 | 3.770 | 20 | 20 | fits | 123,248 | 176 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 295,382 | 2.954 | 20 | 200 | fits | 145,767 | 227 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 427,815 | 4.278 | 20 | 200 | fits | 123,248 | 176 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 296,306 | 2.963 | 20 | 20 | fits | 145,767 | 227 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 428,519 | 4.285 | 20 | 20 | fits | 123,248 | 176 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 154,179 | 1.542 | 20 | 24 | fits | 145,806 | 152 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 298,956 | 2.990 | 20 | 24 | fits | 145,767 | 227 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 298,890 | 2.989 | 20 | 50 | fits | 145,767 | 227 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 431,543 | 4.315 | 20 | 50 | fits | 123,248 | 176 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 597,565 | 5.976 | 20 | 20 | fits | 85,488 | 29 | 0.737 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 961,709 | 9.617 | 20 | 20 | fits | 49,017 | 20 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 369,303 | 3.693 | 20 | 20 | fits | 119,093 | 169 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 308,461 | 3.085 | 20 | 200 | fits | 146,672 | 231 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 426,938 | 4.269 | 20 | 200 | fits | 119,093 | 169 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 309,385 | 3.094 | 20 | 20 | fits | 146,672 | 231 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 427,642 | 4.276 | 20 | 20 | fits | 119,093 | 169 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 157,214 | 1.572 | 20 | 24 | fits | 145,905 | 153 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 312,035 | 3.120 | 20 | 24 | fits | 146,672 | 231 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 311,969 | 3.120 | 20 | 50 | fits | 146,672 | 231 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 430,666 | 4.307 | 20 | 50 | fits | 119,093 | 169 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 596,656 | 5.967 | 20 | 20 | fits | 85,509 | 29 | 0.738 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 978,783 | 9.788 | 20 | 20 | fits | 55,608 | 27 | 0.738 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 338,316 | 3.383 | 20 | 20 | fits | 117,855 | 198 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 286,088 | 2.861 | 20 | 200 | fits | 144,686 | 233 | 0.400 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 403,327 | 4.033 | 20 | 200 | fits | 117,855 | 198 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 287,012 | 2.870 | 20 | 20 | fits | 144,686 | 233 | 0.400 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 404,031 | 4.040 | 20 | 20 | fits | 117,855 | 198 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 145,966 | 1.460 | 20 | 24 | fits | 152,585 | 131 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 289,662 | 2.897 | 20 | 24 | fits | 144,686 | 233 | 0.400 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 289,596 | 2.896 | 20 | 50 | fits | 144,686 | 233 | 0.400 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 407,055 | 4.071 | 20 | 50 | fits | 117,855 | 198 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 573,141 | 5.731 | 20 | 20 | fits | 85,605 | 28 | 0.742 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 955,437 | 9.554 | 20 | 20 | fits | 59,451 | 24 | 0.622 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 365,319 | 3.653 | 20 | 20 | fits | 116,419 | 170 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 290,301 | 2.903 | 20 | 200 | fits | 145,818 | 227 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 416,105 | 4.161 | 20 | 200 | fits | 116,419 | 170 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 291,225 | 2.912 | 20 | 20 | fits | 145,818 | 227 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 416,809 | 4.168 | 20 | 20 | fits | 116,419 | 170 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 149,047 | 1.490 | 20 | 24 | fits | 145,711 | 152 | 0.415 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 293,875 | 2.939 | 20 | 24 | fits | 145,818 | 227 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 293,809 | 2.938 | 20 | 50 | fits | 145,818 | 227 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 419,833 | 4.198 | 20 | 50 | fits | 116,419 | 170 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 505,005 | 5.050 | 20 | 20 | fits | 85,238 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 869,033 | 8.690 | 20 | 20 | fits | 49,017 | 20 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 355,907 | 3.559 | 20 | 20 | fits | 111,438 | 163 | 0.381 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 302,521 | 3.025 | 20 | 200 | fits | 146,672 | 231 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 413,343 | 4.133 | 20 | 200 | fits | 111,438 | 163 | 0.381 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 303,445 | 3.034 | 20 | 20 | fits | 146,672 | 231 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 414,047 | 4.140 | 20 | 20 | fits | 111,438 | 163 | 0.381 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 151,165 | 1.512 | 20 | 24 | fits | 145,837 | 153 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 306,095 | 3.061 | 20 | 24 | fits | 146,672 | 231 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 306,029 | 3.060 | 20 | 50 | fits | 146,672 | 231 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 417,071 | 4.171 | 20 | 50 | fits | 111,438 | 163 | 0.381 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 502,217 | 5.022 | 20 | 20 | fits | 85,212 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 872,038 | 8.720 | 20 | 20 | fits | 54,834 | 26 | 0.725 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 366,775 | 3.668 | 20 | 20 | fits | 112,312 | 166 | 0.369 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 304,301 | 3.043 | 20 | 200 | fits | 144,094 | 222 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 415,997 | 4.160 | 20 | 200 | fits | 112,312 | 166 | 0.369 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 305,225 | 3.052 | 20 | 20 | fits | 144,094 | 222 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 416,701 | 4.167 | 20 | 20 | fits | 112,312 | 166 | 0.369 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 164,771 | 1.648 | 20 | 24 | fits | 146,178 | 153 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 307,875 | 3.079 | 20 | 24 | fits | 144,094 | 222 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 307,809 | 3.078 | 20 | 50 | fits | 144,094 | 222 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 419,725 | 4.197 | 20 | 50 | fits | 112,312 | 166 | 0.369 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 504,789 | 5.048 | 20 | 20 | fits | 85,130 | 28 | 0.742 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 892,636 | 8.926 | 20 | 20 | fits | 65,853 | 31 | 0.698 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 349,486 | 3.495 | 20 | 20 | fits | 111,437 | 163 | 0.381 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 296,101 | 2.961 | 20 | 200 | fits | 145,216 | 226 | 0.406 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 406,922 | 4.069 | 20 | 200 | fits | 111,437 | 163 | 0.381 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 297,025 | 2.970 | 20 | 20 | fits | 145,216 | 226 | 0.406 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 407,626 | 4.076 | 20 | 20 | fits | 111,437 | 163 | 0.381 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 155,449 | 1.554 | 20 | 24 | fits | 145,731 | 152 | 0.415 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 299,675 | 2.997 | 20 | 24 | fits | 145,216 | 226 | 0.406 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 299,609 | 2.996 | 20 | 50 | fits | 145,216 | 226 | 0.406 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 410,650 | 4.106 | 20 | 50 | fits | 111,437 | 163 | 0.381 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 495,796 | 4.958 | 20 | 20 | fits | 85,212 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 883,919 | 8.839 | 20 | 20 | fits | 69,691 | 28 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 345,179 | 3.452 | 20 | 20 | fits | 111,997 | 163 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 284,059 | 2.841 | 20 | 200 | fits | 146,210 | 231 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 395,440 | 3.954 | 20 | 200 | fits | 111,997 | 163 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 284,983 | 2.850 | 20 | 20 | fits | 146,210 | 231 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 396,144 | 3.961 | 20 | 20 | fits | 111,997 | 163 | 0.384 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 142,413 | 1.424 | 20 | 24 | fits | 145,751 | 152 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 287,633 | 2.876 | 20 | 24 | fits | 146,210 | 231 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 287,567 | 2.876 | 20 | 50 | fits | 146,210 | 231 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 399,168 | 3.992 | 20 | 50 | fits | 111,997 | 163 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 484,306 | 4.843 | 20 | 20 | fits | 85,204 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 872,421 | 8.724 | 20 | 20 | fits | 69,423 | 28 | 0.575 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 338,829 | 3.388 | 20 | 20 | fits | 111,583 | 163 | 0.382 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 285,343 | 2.853 | 20 | 200 | fits | 145,952 | 231 | 0.404 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 396,310 | 3.963 | 20 | 200 | fits | 111,583 | 163 | 0.382 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 286,267 | 2.863 | 20 | 20 | fits | 145,952 | 231 | 0.404 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 397,014 | 3.970 | 20 | 20 | fits | 111,583 | 163 | 0.382 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 143,955 | 1.440 | 20 | 24 | fits | 145,751 | 152 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 288,917 | 2.889 | 20 | 24 | fits | 145,952 | 231 | 0.404 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 288,851 | 2.889 | 20 | 50 | fits | 145,952 | 231 | 0.404 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 400,038 | 4.000 | 20 | 50 | fits | 111,583 | 163 | 0.382 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 479,614 | 4.796 | 20 | 20 | fits | 79,642 | 31 | 0.780 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 871,659 | 8.717 | 20 | 20 | fits | 69,423 | 28 | 0.575 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 361,146 | 3.611 | 20 | 20 | fits | 123,072 | 179 | 0.403 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 287,897 | 2.879 | 20 | 200 | fits | 144,176 | 222 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 410,353 | 4.104 | 20 | 200 | fits | 123,072 | 179 | 0.403 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 288,821 | 2.888 | 20 | 20 | fits | 144,176 | 222 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 411,057 | 4.111 | 20 | 20 | fits | 123,072 | 179 | 0.403 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 148,285 | 1.483 | 20 | 24 | fits | 145,751 | 152 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 291,471 | 2.915 | 20 | 24 | fits | 144,176 | 222 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 291,405 | 2.914 | 20 | 50 | fits | 144,176 | 222 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 414,081 | 4.141 | 20 | 50 | fits | 123,072 | 179 | 0.403 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 510,574 | 5.106 | 20 | 20 | fits | 85,957 | 29 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 875,061 | 8.751 | 20 | 20 | fits | 49,055 | 20 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 359,794 | 3.598 | 20 | 20 | fits | 123,076 | 190 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 292,535 | 2.925 | 20 | 200 | fits | 145,878 | 210 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 425,077 | 4.251 | 20 | 200 | fits | 123,076 | 190 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 293,459 | 2.935 | 20 | 20 | fits | 145,878 | 210 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 425,781 | 4.258 | 20 | 20 | fits | 123,076 | 190 | 0.418 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 151,221 | 1.512 | 20 | 24 | fits | 145,751 | 152 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 296,109 | 2.961 | 20 | 24 | fits | 145,878 | 210 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 296,043 | 2.960 | 20 | 50 | fits | 145,878 | 210 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 428,805 | 4.288 | 20 | 50 | fits | 123,076 | 190 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 514,272 | 5.143 | 20 | 20 | fits | 85,533 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 878,376 | 8.784 | 20 | 20 | fits | 49,017 | 20 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 345,478 | 3.455 | 20 | 20 | fits | 112,055 | 163 | 0.385 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 284,300 | 2.843 | 20 | 200 | fits | 146,110 | 231 | 0.406 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 395,739 | 3.957 | 20 | 200 | fits | 112,055 | 163 | 0.385 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 285,224 | 2.852 | 20 | 20 | fits | 146,110 | 231 | 0.406 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 396,443 | 3.964 | 20 | 20 | fits | 112,055 | 163 | 0.385 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 142,754 | 1.428 | 20 | 24 | fits | 145,614 | 152 | 0.414 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 287,874 | 2.879 | 20 | 24 | fits | 146,110 | 231 | 0.406 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 287,808 | 2.878 | 20 | 50 | fits | 146,110 | 231 | 0.406 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 399,467 | 3.995 | 20 | 50 | fits | 112,055 | 163 | 0.385 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 485,221 | 4.852 | 20 | 20 | fits | 85,820 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 867,657 | 8.677 | 20 | 20 | fits | 59,239 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 338,725 | 3.387 | 20 | 20 | fits | 111,641 | 163 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 285,181 | 2.852 | 20 | 200 | fits | 145,852 | 231 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 396,206 | 3.962 | 20 | 200 | fits | 111,641 | 163 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 286,105 | 2.861 | 20 | 20 | fits | 145,852 | 231 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 396,910 | 3.969 | 20 | 20 | fits | 111,641 | 163 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 143,893 | 1.439 | 20 | 24 | fits | 145,614 | 152 | 0.414 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 288,755 | 2.888 | 20 | 24 | fits | 145,852 | 231 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 288,689 | 2.887 | 20 | 50 | fits | 145,852 | 231 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 399,934 | 3.999 | 20 | 50 | fits | 111,641 | 163 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 485,696 | 4.857 | 20 | 20 | fits | 85,828 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 873,653 | 8.737 | 20 | 20 | fits | 64,816 | 30 | 0.680 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 348,722 | 3.487 | 20 | 20 | fits | 112,812 | 167 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 286,172 | 2.862 | 20 | 200 | fits | 143,998 | 222 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 398,368 | 3.984 | 20 | 200 | fits | 112,812 | 167 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 287,096 | 2.871 | 20 | 20 | fits | 143,998 | 222 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 399,072 | 3.991 | 20 | 20 | fits | 112,812 | 167 | 0.372 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 146,738 | 1.467 | 20 | 24 | fits | 145,614 | 152 | 0.414 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 289,746 | 2.897 | 20 | 24 | fits | 143,998 | 222 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 289,680 | 2.897 | 20 | 50 | fits | 143,998 | 222 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 402,096 | 4.021 | 20 | 50 | fits | 112,812 | 167 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 491,679 | 4.917 | 20 | 20 | fits | 79,080 | 31 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 950,308 | 9.503 | 20 | 20 | fits | 70,334 | 29 | 0.592 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 357,103 | 3.571 | 20 | 20 | fits | 115,945 | 170 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 289,822 | 2.898 | 20 | 200 | fits | 145,656 | 227 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 415,152 | 4.152 | 20 | 200 | fits | 115,945 | 170 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 290,746 | 2.907 | 20 | 20 | fits | 145,656 | 227 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 415,856 | 4.159 | 20 | 20 | fits | 115,945 | 170 | 0.422 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 148,730 | 1.487 | 20 | 24 | fits | 145,614 | 152 | 0.414 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 293,396 | 2.934 | 20 | 24 | fits | 145,656 | 227 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 293,330 | 2.933 | 20 | 50 | fits | 145,656 | 227 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 418,880 | 4.189 | 20 | 50 | fits | 115,945 | 170 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 504,855 | 5.049 | 20 | 20 | fits | 86,041 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 952,958 | 9.530 | 20 | 20 | fits | 59,201 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 355,843 | 3.558 | 20 | 20 | fits | 111,004 | 163 | 0.377 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 302,355 | 3.024 | 20 | 200 | fits | 146,746 | 231 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 412,743 | 4.127 | 20 | 200 | fits | 111,004 | 163 | 0.377 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 303,279 | 3.033 | 20 | 20 | fits | 146,746 | 231 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 413,447 | 4.134 | 20 | 20 | fits | 111,004 | 163 | 0.377 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 150,866 | 1.509 | 20 | 24 | fits | 145,758 | 153 | 0.415 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 305,929 | 3.059 | 20 | 24 | fits | 146,746 | 231 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 305,863 | 3.059 | 20 | 50 | fits | 146,746 | 231 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 416,471 | 4.165 | 20 | 50 | fits | 111,004 | 163 | 0.377 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 502,330 | 5.023 | 20 | 20 | fits | 85,925 | 28 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 950,642 | 9.506 | 20 | 20 | fits | 59,293 | 25 | 0.614 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 365,367 | 3.654 | 20 | 20 | fits | 111,710 | 163 | 0.381 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 304,489 | 3.045 | 20 | 200 | fits | 146,987 | 231 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 415,583 | 4.156 | 20 | 200 | fits | 111,710 | 163 | 0.381 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 305,413 | 3.054 | 20 | 20 | fits | 146,987 | 231 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 416,287 | 4.163 | 20 | 20 | fits | 111,710 | 163 | 0.381 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 152,759 | 1.528 | 20 | 24 | fits | 145,659 | 153 | 0.415 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 308,063 | 3.081 | 20 | 24 | fits | 146,987 | 231 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 307,997 | 3.080 | 20 | 50 | fits | 146,987 | 231 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 419,311 | 4.193 | 20 | 50 | fits | 111,710 | 163 | 0.381 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 499,231 | 4.992 | 20 | 20 | fits | 79,986 | 30 | 0.781 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 951,712 | 9.517 | 20 | 20 | fits | 59,293 | 25 | 0.614 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 354,757 | 3.548 | 20 | 20 | fits | 118,766 | 169 | 0.410 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 293,796 | 2.938 | 20 | 200 | fits | 144,982 | 226 | 0.404 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 411,946 | 4.119 | 20 | 200 | fits | 118,766 | 169 | 0.410 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 294,720 | 2.947 | 20 | 20 | fits | 144,982 | 226 | 0.404 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 412,650 | 4.127 | 20 | 20 | fits | 118,766 | 169 | 0.410 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 153,378 | 1.534 | 20 | 24 | fits | 145,752 | 152 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 297,370 | 2.974 | 20 | 24 | fits | 144,982 | 226 | 0.404 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 297,304 | 2.973 | 20 | 50 | fits | 144,982 | 226 | 0.404 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 415,674 | 4.157 | 20 | 50 | fits | 118,766 | 169 | 0.410 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 578,893 | 5.789 | 20 | 20 | fits | 85,649 | 29 | 0.738 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 961,608 | 9.616 | 20 | 20 | fits | 59,239 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 441,161 | 4.412 | 20 | 20 | fits | 117,600 | 184 | 0.369 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 297,335 | 2.973 | 20 | 200 | fits | 145,585 | 209 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 491,613 | 4.916 | 20 | 200 | fits | 117,600 | 184 | 0.369 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 298,259 | 2.983 | 20 | 20 | fits | 145,585 | 209 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 492,317 | 4.923 | 20 | 20 | fits | 117,600 | 184 | 0.369 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 156,314 | 1.563 | 20 | 24 | fits | 145,752 | 152 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 300,909 | 3.009 | 20 | 24 | fits | 145,585 | 209 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 300,843 | 3.008 | 20 | 50 | fits | 145,585 | 209 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 495,341 | 4.953 | 20 | 50 | fits | 117,600 | 184 | 0.369 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 581,285 | 5.813 | 20 | 20 | fits | 86,010 | 29 | 0.741 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 963,403 | 9.634 | 20 | 20 | fits | 59,239 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 362,628 | 3.626 | 20 | 20 | fits | 111,710 | 163 | 0.381 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 301,750 | 3.018 | 20 | 200 | fits | 146,987 | 231 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 412,844 | 4.128 | 20 | 200 | fits | 111,710 | 163 | 0.381 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 302,674 | 3.027 | 20 | 20 | fits | 146,987 | 231 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 413,548 | 4.135 | 20 | 20 | fits | 111,710 | 163 | 0.381 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 150,103 | 1.501 | 20 | 24 | fits | 145,700 | 153 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 305,324 | 3.053 | 20 | 24 | fits | 146,987 | 231 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 305,258 | 3.053 | 20 | 50 | fits | 146,987 | 231 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 416,572 | 4.166 | 20 | 50 | fits | 111,710 | 163 | 0.381 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 502,434 | 5.024 | 20 | 20 | fits | 85,928 | 28 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 866,438 | 8.664 | 20 | 20 | fits | 49,017 | 20 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 346,392 | 3.464 | 20 | 20 | fits | 111,205 | 163 | 0.380 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 292,748 | 2.927 | 20 | 200 | fits | 145,065 | 226 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 403,337 | 4.033 | 20 | 200 | fits | 111,205 | 163 | 0.380 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 293,672 | 2.937 | 20 | 20 | fits | 145,065 | 226 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 404,041 | 4.040 | 20 | 20 | fits | 111,205 | 163 | 0.380 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 152,247 | 1.522 | 20 | 24 | fits | 145,752 | 152 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 296,322 | 2.963 | 20 | 24 | fits | 145,065 | 226 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 296,256 | 2.963 | 20 | 50 | fits | 145,065 | 226 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 407,065 | 4.071 | 20 | 50 | fits | 111,205 | 163 | 0.380 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 492,924 | 4.929 | 20 | 20 | fits | 85,925 | 28 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 880,858 | 8.809 | 20 | 20 | fits | 65,142 | 30 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 356,953 | 3.570 | 20 | 20 | fits | 111,905 | 163 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 295,925 | 2.959 | 20 | 200 | fits | 145,306 | 226 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 407,214 | 4.072 | 20 | 200 | fits | 111,905 | 163 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 296,849 | 2.968 | 20 | 20 | fits | 145,306 | 226 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 407,918 | 4.079 | 20 | 20 | fits | 111,905 | 163 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 155,183 | 1.552 | 20 | 24 | fits | 145,752 | 152 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 299,499 | 2.995 | 20 | 24 | fits | 145,306 | 226 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 299,433 | 2.994 | 20 | 50 | fits | 145,306 | 226 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 410,942 | 4.109 | 20 | 50 | fits | 111,905 | 163 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 496,804 | 4.968 | 20 | 20 | fits | 85,928 | 28 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 884,864 | 8.849 | 20 | 20 | fits | 69,494 | 28 | 0.577 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 332,075 | 3.321 | 20 | 20 | fits | 111,754 | 181 | 0.397 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 285,709 | 2.857 | 20 | 200 | fits | 144,178 | 248 | 0.393 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 396,847 | 3.968 | 20 | 200 | fits | 111,754 | 181 | 0.397 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 286,633 | 2.866 | 20 | 20 | fits | 144,178 | 248 | 0.393 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 397,551 | 3.976 | 20 | 20 | fits | 111,754 | 181 | 0.397 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 146,095 | 1.461 | 20 | 24 | fits | 149,720 | 120 | 0.426 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 289,283 | 2.893 | 20 | 24 | fits | 144,178 | 248 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 289,217 | 2.892 | 20 | 50 | fits | 144,178 | 248 | 0.393 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 400,575 | 4.006 | 20 | 50 | fits | 111,754 | 181 | 0.397 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 486,494 | 4.865 | 20 | 20 | fits | 85,985 | 29 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 874,198 | 8.742 | 20 | 20 | fits | 69,423 | 28 | 0.575 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 346,597 | 3.466 | 20 | 20 | fits | 112,281 | 164 | 0.385 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 285,572 | 2.856 | 20 | 200 | fits | 146,200 | 231 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 397,237 | 3.972 | 20 | 200 | fits | 112,281 | 164 | 0.385 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 286,496 | 2.865 | 20 | 20 | fits | 146,200 | 231 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 397,941 | 3.979 | 20 | 20 | fits | 112,281 | 164 | 0.385 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 143,936 | 1.439 | 20 | 24 | fits | 145,732 | 152 | 0.415 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 289,146 | 2.891 | 20 | 24 | fits | 146,200 | 231 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 289,080 | 2.891 | 20 | 50 | fits | 146,200 | 231 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 400,965 | 4.010 | 20 | 50 | fits | 112,281 | 164 | 0.385 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 490,334 | 4.903 | 20 | 20 | fits | 79,046 | 31 | 0.778 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 870,900 | 8.709 | 20 | 20 | fits | 69,423 | 28 | 0.575 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 356,063 | 3.561 | 20 | 20 | fits | 115,925 | 170 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 288,878 | 2.889 | 20 | 200 | fits | 145,463 | 227 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 414,069 | 4.141 | 20 | 200 | fits | 115,925 | 170 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 289,802 | 2.898 | 20 | 20 | fits | 145,463 | 227 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 414,773 | 4.148 | 20 | 20 | fits | 115,925 | 170 | 0.422 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 147,979 | 1.480 | 20 | 24 | fits | 145,732 | 152 | 0.415 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 292,452 | 2.925 | 20 | 24 | fits | 145,463 | 227 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 292,386 | 2.924 | 20 | 50 | fits | 145,463 | 227 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 417,797 | 4.178 | 20 | 50 | fits | 115,925 | 170 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 497,588 | 4.976 | 20 | 20 | fits | 79,857 | 30 | 0.780 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 871,921 | 8.719 | 20 | 20 | fits | 59,201 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 371,059 | 3.711 | 20 | 20 | fits | 119,825 | 172 | 0.400 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 301,270 | 3.013 | 20 | 200 | fits | 145,646 | 227 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 420,479 | 4.205 | 20 | 200 | fits | 119,825 | 172 | 0.400 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 302,194 | 3.022 | 20 | 20 | fits | 145,646 | 227 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 421,183 | 4.212 | 20 | 20 | fits | 119,825 | 172 | 0.400 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 151,023 | 1.510 | 20 | 24 | fits | 145,840 | 153 | 0.416 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 304,844 | 3.048 | 20 | 24 | fits | 145,646 | 227 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 304,778 | 3.048 | 20 | 50 | fits | 145,646 | 227 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 424,207 | 4.242 | 20 | 50 | fits | 119,825 | 172 | 0.400 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 510,134 | 5.101 | 20 | 20 | fits | 85,993 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 874,179 | 8.742 | 20 | 20 | fits | 49,017 | 20 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 347,023 | 3.470 | 20 | 20 | fits | 119,157 | 172 | 0.371 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 293,476 | 2.935 | 20 | 200 | fits | 144,823 | 224 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 412,017 | 4.120 | 20 | 200 | fits | 119,157 | 172 | 0.371 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 294,400 | 2.944 | 20 | 20 | fits | 144,823 | 224 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 412,721 | 4.127 | 20 | 20 | fits | 119,157 | 172 | 0.371 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 153,217 | 1.532 | 20 | 24 | fits | 145,795 | 152 | 0.415 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 297,050 | 2.970 | 20 | 24 | fits | 144,823 | 224 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 296,984 | 2.970 | 20 | 50 | fits | 144,823 | 224 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 415,745 | 4.157 | 20 | 50 | fits | 119,157 | 172 | 0.371 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 501,543 | 5.015 | 20 | 20 | fits | 85,864 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 883,716 | 8.837 | 20 | 20 | fits | 55,834 | 27 | 0.741 |
| LINK_UP | `adp.link_up.if0` | 2,790 | 0.028 | 20 | 200 | fits | 26,513 | 43 (11) | 0.727 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 7,415 | 0.074 | 20 | 200 | fits | 22,058 | 23 (39) | 0.740 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 12,458 | 0.125 | 20 | 200 | fits | 2,640 | 10 (11) | 0.556 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 152,029 | 1.520 | 20 | 200 | fits | 152,969 | 240 | 0.449 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 264,912 | 2.649 | 20 | 20 | fits | 60,638 | 27 | 0.701 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 229,619 | 2.296 | 20 | 24 | fits | 59,174 | 45 | 0.486 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 185,378 | 1.854 | 20 | 50 | fits | 92,961 | 91 | 0.632 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 781,261 | 7.813 | 20 | 20 | fits | 79,321 | 32 | 0.557 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 151,914 | 1.519 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 152,029 | 1.520 | 20 | 200 | fits | 152,969 | 240 | 0.449 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 294,824 | 2.948 | 20 | 20 | fits | 83,795 | 41 | 0.657 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 266,557 | 2.666 | 20 | 24 | fits | 79,903 | 55 | 0.596 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 171,554 | 1.716 | 20 | 50 | fits | 149,676 | 256 | 0.339 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 807,806 | 8.078 | 20 | 20 | fits | 82,545 | 38 | 0.599 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 187,123 | 1.871 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 10,638 | 0.106 | 20 | 20 | fits | 28,255 | 21 (35) | 0.817 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 18,759 | 0.188 | 20 | 20 | fits | 25,602 | 17 (14) | 0.860 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 19,976 | 0.200 | 20 | 20 | fits | 24,598 | 18 (14) | 0.854 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 10,241 | 0.102 | 20 | 20 | fits | 28,357 | 21 (35) | 0.817 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 74,878 | 0.749 | 20 | 20 | fits | 28,007 | 8 | 0.753 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 41,900 | 0.419 | 20 | 20 | fits | 41,966 | 12 | 0.894 |
| malformed MRPDU discard | `srp.malformed.if0` | 18,923 | 0.189 | 20 | 20 | fits | 18,989 | 12 | 0.714 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 80,442 | 0.804 | 220 | 220 | fits | 51,450 | 6 | 0.893 |
| an event behind 15 others | `backlog.event.if0` | 157,154 | 1.572 | 20 | 200 | fits | 49,964 | 78 | 0.567 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 403,438 | 4.034 | 20 | 20 | fits | 45,259 | 63 | 0.289 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 398,769 | 3.988 | 20 | 200 | fits | 148,320 | 159 | 0.366 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 398,153 | 3.982 | 20 | 200 | fits | 148,320 | 159 | 0.366 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 394,447 | 3.944 | 20 | 20 | fits | 148,320 | 159 | 0.366 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 438,870 | 4.389 | 20 | 20 | fits | 45,259 | 63 | 0.289 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 145,896 | 1.459 | 20 | 24 | fits | 146,787 | 158 | 0.429 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 397,097 | 3.971 | 20 | 24 | fits | 148,320 | 159 | 0.366 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 397,031 | 3.970 | 20 | 50 | fits | 148,320 | 159 | 0.366 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 396,635 | 3.966 | 20 | 50 | fits | 148,320 | 159 | 0.366 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 441,828 | 4.418 | 20 | 20 | fits | 45,259 | 63 | 0.289 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 506,291 | 5.063 | 20 | 20 | fits | 27,585 | 41 | 0.159 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 353,814 | 3.538 | 20 | 20 | fits | 115,682 | 170 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 286,710 | 2.867 | 20 | 200 | fits | 145,075 | 227 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 411,736 | 4.117 | 20 | 200 | fits | 115,682 | 170 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 287,634 | 2.876 | 20 | 20 | fits | 145,075 | 227 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 412,440 | 4.124 | 20 | 20 | fits | 115,682 | 170 | 0.421 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 146,199 | 1.462 | 20 | 24 | fits | 146,385 | 155 | 0.418 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 290,284 | 2.903 | 20 | 24 | fits | 145,075 | 227 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 290,218 | 2.902 | 20 | 50 | fits | 145,075 | 227 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 415,464 | 4.155 | 20 | 50 | fits | 115,682 | 170 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 501,235 | 5.012 | 20 | 20 | fits | 85,837 | 28 | 0.747 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 871,075 | 8.711 | 20 | 20 | fits | 59,196 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,931 | 0.089 | 20 | 20 | fits | 26,916 | 19 | 0.812 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 286,710 | 2.867 | 20 | 200 | fits | 145,075 | 227 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 26,978 | 0.270 | 20 | 200 | fits | 26,916 | 19 | 0.812 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 287,634 | 2.876 | 20 | 20 | fits | 145,075 | 227 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 402,042 | 4.020 | 20 | 20 | fits | 105,284 | 160 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 146,199 | 1.462 | 20 | 24 | fits | 146,385 | 155 | 0.418 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 290,284 | 2.903 | 20 | 24 | fits | 145,075 | 227 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 290,218 | 2.902 | 20 | 50 | fits | 145,075 | 227 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 405,066 | 4.051 | 20 | 50 | fits | 105,284 | 160 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 490,676 | 4.907 | 20 | 20 | fits | 85,676 | 28 | 0.749 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 860,678 | 8.607 | 20 | 20 | fits | 59,196 | 24 | 0.615 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,284,208 | 62.842 | 20 | 20 | MISS ceiling | 17,104 | 13 | 0.582 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,301,385 | 63.014 | 20 | 20 | MISS ceiling | 17,086 | 13 | 0.574 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,318,317 | 63.183 | 20 | 20 | MISS ceiling | 16,989 | 13 | 0.582 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,335,231 | 63.352 | 20 | 20 | MISS ceiling | 16,990 | 13 | 0.582 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,352,143 | 63.521 | 20 | 20 | MISS ceiling | 16,975 | 13 | 0.582 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 151,530 | 1.515 | 20 | 200 | fits | 148,023 | 208 | 0.443 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 239,416 | 2.394 | 20 | 200 | fits | 88,502 | 176 | 0.358 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 147,208 | 1.472 | 20 | 20 | fits | 148,023 | 208 | 0.443 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,200,622 | 62.006 | 20 | 20 | MISS ceiling | 28,506 | 15 | 0.714 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 150,848 | 1.508 | 20 | 24 | fits | 148,023 | 208 | 0.443 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,175,602 | 61.756 | 20 | 24 | MISS ceiling | 138,767 | 106 | 0.470 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 149,792 | 1.498 | 20 | 50 | fits | 148,023 | 208 | 0.443 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 237,898 | 2.379 | 20 | 50 | fits | 88,502 | 176 | 0.358 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 322,414 | 3.224 | 20 | 20 | fits | 84,582 | 28 | 0.737 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 696,368 | 6.964 | 20 | 20 | fits | 60,372 | 24 | 0.649 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 6,010 | 0.060 | 20 | 20 | fits | 23,527 | 13 (29) | 0.777 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,798 | 0.078 | 20 | 20 | fits | 26,002 | 19 (35) | 0.796 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 20,108 | 0.201 | 20 | 20 | fits | 28,624 | 21 (12) | 0.820 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 11,163 | 0.112 | 20 | 50 | fits | 26,513 | 43 | 0.727 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 9,361 | 0.094 | 20 | 50 | fits | 23,353 | 35 | 0.717 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 14,119 | 0.141 | 20 | 50 | fits | 23,260 | 35 | 0.715 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 20,927 | 0.209 | 20 | 50 | fits | 28,205 | 61 | 0.622 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 23,609 | 0.236 | 20 | 50 | fits | 28,205 | 61 | 0.622 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 9,648 | 0.096 | 20 | 50 | fits | 21,149 | 30 | 0.626 |
| LINK_UP | `adp.link_up.if0` | 2,790 | 0.028 | 20 | 200 | fits | 26,513 | 43 (11) | 0.727 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 7,415 | 0.074 | 20 | 200 | fits | 22,058 | 23 (39) | 0.740 |
| LINK_DOWN | `adp.link_down.if0` | 2,442 | 0.024 | 20 | 200 | fits | 22,868 | 23 (9) | 0.771 |
| LINK_UP | `adp.link_up.if0` | 2,790 | 0.028 | 20 | 200 | fits | 26,513 | 43 (11) | 0.727 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 7,415 | 0.074 | 20 | 200 | fits | 22,058 | 23 (39) | 0.740 |
| GM_CHANGE | `adp.gm_change.if0` | 2,583 | 0.026 | 20 | 200 | fits | 16,267 | 17 (11) | 0.759 |
| LINK_UP | `adp.link_up.if0` | 2,790 | 0.028 | 20 | 200 | fits | 26,513 | 43 (11) | 0.727 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 7,415 | 0.074 | 20 | 200 | fits | 22,058 | 23 (39) | 0.740 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 5,134 | 0.051 | 20 | 200 | fits | 15,265 | 16 (31) | 0.603 |
| LINK_UP | `adp.link_up.if0` | 2,790 | 0.028 | 20 | 200 | fits | 26,513 | 43 (11) | 0.727 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 7,415 | 0.074 | 20 | 200 | fits | 22,058 | 23 (39) | 0.740 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 5,134 | 0.051 | 20 | 200 | fits | 15,265 | 16 (31) | 0.603 |
| set_name | `aecp_fanout.set_name.if0` | 54,078 | 0.541 | 20 | 24 | fits | 60,851 | 88 | 0.572 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 55,499 | 0.555 | 20 | 24 | fits | 54,764 | 78 | 0.596 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 56,273 | 0.563 | 20 | 24 | fits | 53,193 | 78 | 0.565 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 49,764 | 0.498 | 20 | 24 | fits | 49,240 | 77 | 0.554 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 61,300 | 0.613 | 20 | 24 | fits | 59,296 | 66 | 0.626 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 284,671 | 2.847 | 20 | 24 | fits | 57,086 | 65 | 0.612 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 348,560 | 3.486 | 20 | 24 | fits | 51,383 | 67 | 0.573 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 49,719 | 0.497 | 20 | 24 | fits | 49,243 | 77 | 0.553 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 55,166 | 0.552 | 20 | 24 | fits | 49,459 | 78 | 0.553 |
| BIND_RX | `acmp.bind_rx.if0` | 18,982 | 0.190 | 20 | 20 | fits | 40,776 | 26 (77) | 0.797 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,854 | 0.099 | 20 | 20 | fits | 31,231 | 19 (32) | 0.833 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,499 | 0.105 | 20 | 20 | fits | 24,529 | 15 (47) | 0.745 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 14,957 | 0.150 | 20 | 20 | fits | 38,477 | 18 (50) | 0.838 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,699 | 0.107 | 20 | 20 | fits | 24,693 | 17 (48) | 0.729 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 10,566 | 0.106 | 20 | 20 | fits | 23,599 | 16 (48) | 0.694 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,572 | 0.096 | 20 | 20 | fits | 22,395 | 16 (48) | 0.681 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,735 | 0.097 | 20 | 20 | fits | 22,291 | 17 (48) | 0.669 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 21,861 | 0.219 | 20 | 24 | fits | 26,363 | 20 | 0.774 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 19,509 | 0.195 | 20 | 24 | fits | 31,245 | 20 | 0.709 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 11,014 | 0.110 | 20 | 24 | fits | 27,037 | 20 | 0.733 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 15,545 | 0.155 | 20 | 24 | fits | 27,063 | 20 | 0.732 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 11,150 | 0.112 | 20 | 24 | fits | 27,172 | 20 | 0.726 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 16,279 | 0.163 | 20 | 24 | fits | 27,687 | 20 | 0.735 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 15,398 | 0.154 | 20 | 24 | fits | 26,727 | 20 | 0.736 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 10,704 | 0.107 | 20 | 24 | fits | 26,736 | 20 | 0.743 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 14,881 | 0.149 | 20 | 24 | fits | 26,039 | 20 | 0.747 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 12,648 | 0.126 | 20 | 24 | fits | 28,633 | 21 | 0.650 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 14,559 | 0.146 | 20 | 24 | fits | 25,567 | 20 | 0.762 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 9,605 | 0.096 | 20 | 24 | fits | 25,520 | 20 | 0.754 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 15,153 | 0.152 | 20 | 24 | fits | 26,423 | 20 | 0.736 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 15,737 | 0.157 | 20 | 24 | fits | 27,085 | 20 | 0.738 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 10,442 | 0.104 | 20 | 24 | fits | 26,469 | 20 | 0.744 |
| get_configuration | `aecp.get_configuration.if0` | 13,383 | 0.134 | 20 | 24 | fits | 23,673 | 20 | 0.739 |
| entity_available | `aecp.entity_available.if0` | 8,364 | 0.084 | 20 | 24 | fits | 23,533 | 20 | 0.717 |
| get_name | `aecp.get_name.if0` | 15,603 | 0.156 | 20 | 24 | fits | 26,490 | 20 | 0.741 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 11,413 | 0.114 | 20 | 24 | fits | 27,151 | 27 | 0.702 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 16,944 | 0.169 | 20 | 24 | fits | 27,984 | 29 | 0.754 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 13,881 | 0.139 | 20 | 24 | fits | 24,606 | 20 | 0.753 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 7,580 | 0.076 | 20 | 24 | fits | 22,650 | 20 | 0.706 |
| set_name | `aecp.set_name.if0` | 22,190 | 0.222 | 20 | 24 | fits | 43,400 | 42 | 0.765 |
| lock_entity | `aecp.lock_entity.if0` | 14,087 | 0.141 | 20 | 24 | fits | 34,135 | 34 | 0.773 |
| unlock_entity | `aecp.unlock_entity.if0` | 22,413 | 0.224 | 20 | 24 | fits | 35,610 | 32 | 0.781 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 156,514 | 1.565 | 20 | 24 | fits | 163,940 | 91 | 0.328 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 226,600 | 2.266 | 20 | 24 | fits | 155,788 | 70 | 0.303 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 222,051 | 2.221 | 20 | 24 | fits | 39,376 | 17 | 0.678 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 391,933 | 3.919 | 20 | 24 | fits | 102,185 | 18 | 0.659 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 346,177 | 3.462 | 20 | 24 | fits | 111,394 | 17 | 0.668 |
| LINK_UP | `fixture.link_up.if0` | 2,790 | 0.028 | 20 | 200 | fits | 26,513 | 43 (11) | 0.727 |
| malformed MRPDU discard | `fixture.malformed.if0` | 19,427 | 0.194 | 20 | 20 | fits | 19,493 | 12 | 0.750 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 32,002 | 0.320 | 20 | 24 | fits | 44,800 | 42 | 0.779 |
| LINK_DOWN | `fixture.link_down.if0` | 2,688 | 0.027 | 20 | 200 | fits | 24,329 | 23 (9) | 0.787 |
| BIND_RX | `fixture.bind_rx.if0` | 19,594 | 0.196 | 20 | 20 | fits | 40,999 | 26 (77) | 0.804 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 29,955 | 0.300 | 20 | 20 | fits | 37,865 | 35 (35) | 0.780 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 13,636 | 0.136 | 20 | 20 | fits | 24,920 | 13 (29) | 0.814 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 80,143 | 0.801 | 20 | 200 | fits | 80,247 | 51 | 0.759 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 80,143 | 0.801 | 20 | 200 | fits | 80,247 | 51 | 0.759 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 79,869 | 0.799 | 20 | 20 | fits | 80,247 | 51 | 0.759 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 79,869 | 0.799 | 20 | 20 | fits | 80,247 | 51 | 0.759 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 80,077 | 0.801 | 20 | 24 | fits | 80,247 | 51 | 0.759 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 80,077 | 0.801 | 20 | 24 | fits | 80,247 | 51 | 0.759 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 80,011 | 0.800 | 20 | 50 | fits | 80,247 | 51 | 0.759 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 80,011 | 0.800 | 20 | 50 | fits | 80,247 | 51 | 0.759 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 79,945 | 0.799 | 20 | 20 | fits | 80,247 | 51 | 0.759 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 79,945 | 0.799 | 20 | 20 | fits | 80,247 | 51 | 0.759 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
