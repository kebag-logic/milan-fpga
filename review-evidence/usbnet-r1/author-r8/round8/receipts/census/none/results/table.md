### arty-1x1

Clock: CPU 80 MHz on sys, the product's split CPU clock, bus 80 MHz.

4 of 99 paths and 7 of 973 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.210 (0.421) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.101 (0.209) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.093 (0.261) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.089 (0.370) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.109 (0.228) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.101 (0.207) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.107 (0.220) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.119 (0.243) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.112 (0.293) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.196 (0.480) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.113 (0.394) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.280 (0.595) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.155 (0.472) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.116 (0.479) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.159 (0.451) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.141 (0.377) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.052 (0.132) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.023 (0.112) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.026 (0.246) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.036 (0.249) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.061 (0.175) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.080 (0.298) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.108 (0.349) | fits | 0 aecp | 1 | 0 |
| get_as_path, refused ENTITY_MISBEHAVING | 0 | `aecp.get_as_path.if0` (aecp) | 0.145 (0.392) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.116 (0.255) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.083 (0.218) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.158 (0.410) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.111 (0.247) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR held for a token (#917) | 0 | `aecp.held.read_descriptor.if0` (aecp-held) | 5.220 (5.466) | fits | 16 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.149 (0.343) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.112 (0.356) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.176 (0.425) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.117 (0.257) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.106 (0.245) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.135 (0.381) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.167 (0.307) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.129 (0.375) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.095 (0.235) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (156 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.142 (0.390) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i15.c0.if0` (aecp) | 0.133 (0.380) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t23.i0.c0.if0` (aecp) | 0.107 (0.246) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.145 (0.393) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.135 (0.382) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.118 (0.258) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i0.c0.if0` (aecp) | 0.138 (0.387) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.112 (0.254) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.164 (0.409) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.217 (0.591) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.084 (0.221) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.210 (0.518) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 3.590 (3.929) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.434 (0.713) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.647 (0.957) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.509 (0.802) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.437 (0.713) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.510 (0.825) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 4.320 (4.638) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.481 (0.731) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 3.951 (4.253) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 3.191 (3.521) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 4.720 (5.051) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 4.601 (4.931) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.784 (2.059) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.296 (4.661) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 4.838 (5.401) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.165 (0.468) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.606 (2.006) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.720 (62.862) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.286 (63.432) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.332 (0.480) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-burst.held.acmp.if0` (save-burst) | 3.743 | fits | 11 acmp | 4 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-burst.held.adp.if0` (save-burst) | 1.533 | fits | 7 adp | 4 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-flight.held.aecp.if0` (save-flight) | 3.605 | fits | 14 aecp | 4 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 2.411 | fits | 6 maap | 4 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 9.573 | fits | 31 srp | 4 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.119 (0.258) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.095 (0.189) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.126 (0.249) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.095 (0.258) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.157 (0.381) | fits | 0 events | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-held.mrpdu.periodic.if0` (save-held) | 2.642 | fits | 0 srp | 8 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.053 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 61.993 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.107 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 5.356 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@program-4.service.aecp.first.if0` (backlog-adp@program-4) | 2.515 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.036 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.086 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.maap.last.if0` (backlog-adp@program-aged2-7) | 5.402 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-7.service.srp.first.if0` (backlog-adp@program-aged2-7) | 6.715 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-3.service.srp.last.if0` (backlog-adp@program-aged2-3) | 11.530 | fits | 31 srp | 77 | 0 |
| Talker Advertise RX for every input, bound | 0 | `srp.bound_advertise.if0` (srp-bound) | 0.774 (0.775) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.811 (1.286) | fits | 0 srp | 1 | 0 |
| Talker Advertise RX for every input, no binding (kept) | 0 | `srp.kept_advertise.if0` (srp-kept) | 0.577 (0.578) | fits | 0 srp | 1 | 0 |
| Talker Failed RX for every input, no binding (kept) | 0 | `srp.kept_failed.if0` (srp-kept) | 0.572 (0.573) | fits | 0 srp | 1 | 0 |
| Talker RX at the bound after a freed block (count) | 0 | `srp.kept_recount.if0` (srp-kept) | 0.538 (0.539) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.417 (0.418) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.176 (0.177) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.848 (0.936) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 14.954 | 13 | 120,404 (1.505) | yes | - |
| backlog-adp@blank-1 | 0 | 14.829 | 13 | 120,404 (1.505) | yes | - |
| backlog-adp@blank-2 | 0 | 14.704 | 13 | 120,404 (1.505) | yes | - |
| backlog-adp@blank-3 | 0 | 14.579 | 13 | 120,404 (1.505) | yes | - |
| backlog-adp@blank-4 | 0 | 14.454 | 13 | 120,404 (1.505) | yes | - |
| backlog-adp@blank-5 | 0 | 14.329 | 13 | 120,404 (1.505) | yes | - |
| backlog-adp@blank-6 | 0 | 14.074 | 12 | 119,470 (1.493) | yes | - |
| backlog-adp@blank-7 | 0 | 13.949 | 12 | 119,470 (1.493) | yes | - |
| backlog-adp@program-0 | 1 | 11.857 | 9 | 119,227 (1.490) | yes | - |
| backlog-adp@program-1 | 1 | 11.857 | 9 | 119,227 (1.490) | yes | - |
| backlog-adp@program-2 | 1 | 11.857 | 9 | 119,227 (1.490) | yes | - |
| backlog-adp@program-3 | 0 | 11.702 | 9 | 119,608 (1.495) | yes | - |
| backlog-adp@program-4 | 0 | 14.141 | 10 | 119,575 (1.495) | yes | - |
| backlog-adp@program-5 | 0 | 13.891 | 10 | 119,575 (1.495) | yes | - |
| backlog-adp@program-6 | 0 | 13.641 | 10 | 119,575 (1.495) | yes | - |
| backlog-adp@program-7 | 0 | 13.391 | 10 | 119,575 (1.495) | yes | - |
| backlog-adp@verify-0 | 0 | 13.763 | 11 | 119,133 (1.489) | yes | - |
| backlog-adp@verify-1 | 0 | 13.638 | 11 | 119,133 (1.489) | yes | - |
| backlog-adp@verify-2 | 0 | 13.513 | 11 | 119,133 (1.489) | yes | - |
| backlog-adp@verify-3 | 0 | 13.388 | 11 | 119,133 (1.489) | yes | - |
| backlog-adp@verify-4 | 0 | 13.263 | 11 | 119,133 (1.489) | yes | - |
| backlog-adp@verify-5 | 0 | 13.138 | 11 | 119,133 (1.489) | yes | - |
| backlog-adp@verify-6 | 0 | 13.124 | 10 | 118,606 (1.483) | yes | - |
| backlog-adp@verify-7 | 0 | 13.761 | 11 | 119,198 (1.490) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 12.975 | 11 | 118,231 (1.478) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 13.702 | 10 | 118,285 (1.479) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 13.756 | 10 | 119,502 (1.494) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 15.665 | 12 | 118,046 (1.476) | yes | - |
| backlog-adp@blank-aged2-4 | 1 | 14.768 | 11 | 115,963 (1.450) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 13.933 | 11 | 119,701 (1.496) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 14.835 | 12 | 118,221 (1.478) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 13.768 | 10 | 118,407 (1.480) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 13.982 | 12 | 119,638 (1.495) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 13.108 | 11 | 118,164 (1.477) | yes | - |
| backlog-adp@blank-aged1-2 | 1 | 12.930 | 9 | 116,150 (1.452) | yes | - |
| backlog-adp@blank-aged1-3 | 1 | 12.929 | 9 | 115,950 (1.449) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 12.964 | 10 | 118,206 (1.478) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 15.801 | 13 | 119,489 (1.494) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 15.116 | 13 | 118,735 (1.484) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 13.965 | 11 | 119,625 (1.495) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 12.742 | 10 | 119,473 (1.493) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 14.408 | 12 | 117,919 (1.474) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 13.007 | 10 | 116,124 (1.452) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 13.034 | 11 | 118,076 (1.476) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 12.898 | 10 | 119,489 (1.494) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 12.860 | 10 | 119,489 (1.494) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 15.908 | 13 | 118,219 (1.478) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 14.476 | 12 | 119,379 (1.492) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 12.777 | 10 | 119,460 (1.493) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 12.775 | 9 | 118,104 (1.476) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 12.597 | 9 | 118,177 (1.477) | yes | - |
| backlog-adp@program-aged1-3 | 1 | 13.036 | 10 | 115,661 (1.446) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 12.956 | 11 | 118,132 (1.477) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 12.896 | 11 | 118,152 (1.477) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 12.630 | 9 | 117,967 (1.475) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 13.076 | 10 | 119,057 (1.488) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 13.913 | 11 | 120,343 (1.504) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 13.914 | 11 | 118,312 (1.479) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 13.845 | 11 | 118,380 (1.480) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 13.722 | 10 | 117,967 (1.475) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 13.599 | 9 | 119,442 (1.493) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 16.705 | 13 | 119,442 (1.493) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 15.856 | 12 | 117,526 (1.469) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 14.954 | 12 | 119,376 (1.492) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 13.007 | 10 | 119,413 (1.493) | yes | - |
| backlog-adp@verify-aged1-1 | 1 | 15.750 | 11 | 115,874 (1.448) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 14.150 | 12 | 118,368 (1.480) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 13.133 | 11 | 118,207 (1.478) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 12.986 | 10 | 119,429 (1.493) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 12.953 | 9 | 120,267 (1.503) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 16.005 | 13 | 118,167 (1.477) | yes | - |
| backlog-adp@verify-aged1-7 | 1 | 14.920 | 11 | 118,975 (1.487) | yes | - |
| backlog | 0 | 5.516 | 7 | 119,822 (1.498) | yes | - |
| backlog-adp | 0 | 10.724 | 10 | 119,108 (1.489) | yes | - |
| backlog-adp-refill | 0 | 40.697 | 24 | 119,108 (1.489) | yes | - |
| backlog-owed | 0 | 63.760 | 24 | 116,720 (1.459) | yes | - |
| fixture | 0 | 1.273 | 2 | 72,720 (0.909) | yes | - |

Composed maximum over the 4 backlog windows: 119,822 CPU cycles (1.498 ms), backlog.
Over the windows that released their whole load only: 119,822 (1.498 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 160,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-kept | 1889 | 0 | 56,110 (0.701) | fits |
| save-flight | 2836 | 0 | 123,450 (1.543) | fits |
| save-burst | 2514 | 0 | 123,450 (1.543) | fits |
| acmp-notk | 3346 | 0 | 75,608 (0.945) | fits |
| adp-advertise | 748 | 0 | 54,957 (0.687) | fits |
| save-second | 60456 | 0 | 54,957 (0.687) | fits |
| backlog-adp@blank-0 | 338 | 0 | 120,404 (1.505) | fits |
| backlog-adp@blank-1 | 338 | 0 | 120,404 (1.505) | fits |
| backlog-adp@blank-2 | 338 | 0 | 120,404 (1.505) | fits |
| backlog-adp@blank-3 | 338 | 0 | 120,404 (1.505) | fits |
| backlog-adp@blank-4 | 338 | 0 | 120,404 (1.505) | fits |
| backlog-adp@blank-5 | 338 | 0 | 120,404 (1.505) | fits |
| backlog-adp@blank-6 | 337 | 0 | 119,470 (1.493) | fits |
| backlog-adp@blank-7 | 337 | 0 | 119,470 (1.493) | fits |
| backlog-adp@program-0 | 342 | 0 | 120,200 (1.502) | fits |
| backlog-adp@program-1 | 342 | 0 | 120,200 (1.502) | fits |
| backlog-adp@program-2 | 342 | 0 | 120,200 (1.502) | fits |
| backlog-adp@program-3 | 342 | 0 | 119,608 (1.495) | fits |
| backlog-adp@program-4 | 343 | 0 | 119,575 (1.495) | fits |
| backlog-adp@program-5 | 343 | 0 | 119,575 (1.495) | fits |
| backlog-adp@program-6 | 343 | 0 | 119,575 (1.495) | fits |
| backlog-adp@program-7 | 343 | 0 | 119,575 (1.495) | fits |
| backlog-adp@verify-0 | 348 | 0 | 119,133 (1.489) | fits |
| backlog-adp@verify-1 | 348 | 0 | 119,133 (1.489) | fits |
| backlog-adp@verify-2 | 348 | 0 | 119,133 (1.489) | fits |
| backlog-adp@verify-3 | 348 | 0 | 119,133 (1.489) | fits |
| backlog-adp@verify-4 | 348 | 0 | 119,133 (1.489) | fits |
| backlog-adp@verify-5 | 348 | 0 | 119,133 (1.489) | fits |
| backlog-adp@verify-6 | 348 | 0 | 120,330 (1.504) | fits |
| backlog-adp@verify-7 | 348 | 0 | 119,198 (1.490) | fits |
| backlog-adp@blank-aged2-0 | 737 | 0 | 118,231 (1.478) | fits |
| backlog-adp@blank-aged2-1 | 747 | 0 | 118,285 (1.479) | fits |
| backlog-adp@blank-aged2-2 | 759 | 0 | 119,502 (1.494) | fits |
| backlog-adp@blank-aged2-3 | 772 | 0 | 118,046 (1.476) | fits |
| backlog-adp@blank-aged2-4 | 783 | 0 | 118,046 (1.476) | fits |
| backlog-adp@blank-aged2-5 | 794 | 0 | 119,701 (1.496) | fits |
| backlog-adp@blank-aged2-6 | 806 | 0 | 118,221 (1.478) | fits |
| backlog-adp@blank-aged2-7 | 815 | 0 | 118,407 (1.480) | fits |
| backlog-adp@blank-aged1-0 | 648 | 0 | 119,638 (1.495) | fits |
| backlog-adp@blank-aged1-1 | 658 | 0 | 118,164 (1.477) | fits |
| backlog-adp@blank-aged1-2 | 669 | 0 | 119,489 (1.494) | fits |
| backlog-adp@blank-aged1-3 | 679 | 0 | 118,140 (1.477) | fits |
| backlog-adp@blank-aged1-4 | 691 | 0 | 118,206 (1.478) | fits |
| backlog-adp@blank-aged1-5 | 705 | 0 | 119,489 (1.494) | fits |
| backlog-adp@blank-aged1-6 | 717 | 0 | 118,735 (1.484) | fits |
| backlog-adp@blank-aged1-7 | 726 | 0 | 119,625 (1.495) | fits |
| backlog-adp@program-aged2-0 | 748 | 0 | 119,473 (1.493) | fits |
| backlog-adp@program-aged2-1 | 761 | 0 | 117,919 (1.474) | fits |
| backlog-adp@program-aged2-2 | 771 | 0 | 117,919 (1.474) | fits |
| backlog-adp@program-aged2-3 | 783 | 0 | 118,076 (1.476) | fits |
| backlog-adp@program-aged2-4 | 793 | 0 | 119,489 (1.494) | fits |
| backlog-adp@program-aged2-5 | 804 | 0 | 119,489 (1.494) | fits |
| backlog-adp@program-aged2-6 | 819 | 0 | 118,219 (1.478) | fits |
| backlog-adp@program-aged2-7 | 829 | 0 | 119,379 (1.492) | fits |
| backlog-adp@program-aged1-0 | 657 | 0 | 119,460 (1.493) | fits |
| backlog-adp@program-aged1-1 | 668 | 0 | 121,621 (1.520) | fits |
| backlog-adp@program-aged1-2 | 679 | 0 | 118,177 (1.477) | fits |
| backlog-adp@program-aged1-3 | 692 | 0 | 118,040 (1.476) | fits |
| backlog-adp@program-aged1-4 | 704 | 0 | 118,132 (1.477) | fits |
| backlog-adp@program-aged1-5 | 715 | 0 | 118,152 (1.477) | fits |
| backlog-adp@program-aged1-6 | 724 | 0 | 117,967 (1.475) | fits |
| backlog-adp@program-aged1-7 | 737 | 0 | 119,057 (1.488) | fits |
| backlog-adp@verify-aged2-0 | 701 | 0 | 120,343 (1.504) | fits |
| backlog-adp@verify-aged2-1 | 712 | 0 | 118,312 (1.479) | fits |
| backlog-adp@verify-aged2-2 | 723 | 0 | 118,380 (1.480) | fits |
| backlog-adp@verify-aged2-3 | 733 | 0 | 117,967 (1.475) | fits |
| backlog-adp@verify-aged2-4 | 744 | 0 | 119,442 (1.493) | fits |
| backlog-adp@verify-aged2-5 | 759 | 0 | 119,442 (1.493) | fits |
| backlog-adp@verify-aged2-6 | 770 | 0 | 117,967 (1.475) | fits |
| backlog-adp@verify-aged2-7 | 781 | 0 | 119,376 (1.492) | fits |
| backlog-adp@verify-aged1-0 | 609 | 0 | 119,413 (1.493) | fits |
| backlog-adp@verify-aged1-1 | 622 | 0 | 118,050 (1.476) | fits |
| backlog-adp@verify-aged1-2 | 634 | 0 | 118,368 (1.480) | fits |
| backlog-adp@verify-aged1-3 | 644 | 0 | 118,207 (1.478) | fits |
| backlog-adp@verify-aged1-4 | 654 | 0 | 119,429 (1.493) | fits |
| backlog-adp@verify-aged1-5 | 665 | 0 | 120,267 (1.503) | fits |
| backlog-adp@verify-aged1-6 | 680 | 0 | 118,167 (1.477) | fits |
| backlog-adp@verify-aged1-7 | 690 | 0 | 118,975 (1.487) | fits |
| srp-bound | 1227 | 0 | 62,009 (0.775) | fits |
| acmp-noresp | 1881 | 0 | 75,531 (0.944) | fits |
| save-held | 1187 | 0 | 123,450 (1.543) | fits |
| save-starved | 32475 | 0 | 123,450 (1.543) | fits |
| save-bind | 1656 | 0 | 94,198 (1.177) | fits |
| save | 602 | 0 | 54,957 (0.687) | fits |
| adp-link | 246 | 0 | 54,957 (0.687) | fits |
| adp-gm | 245 | 0 | 54,957 (0.687) | fits |
| adp-discover | 245 | 0 | 54,957 (0.687) | fits |
| control | 245 | 0 | 54,957 (0.687) | fits |
| srp | 285 | 0 | 74,298 (0.929) | fits |
| save-bind-in-capture | 843 | 0 | 54,957 (0.687) | fits |
| save-bind-in-seal | 841 | 0 | 63,368 (0.792) | fits |
| save-bind-in-erase | 879 | 0 | 75,330 (0.942) | fits |
| save-bind-in-erase-late | 851 | 0 | 54,957 (0.687) | fits |
| save-bind-in-blank | 849 | 0 | 77,916 (0.974) | fits |
| save-bind-in-blank-late | 852 | 0 | 77,867 (0.973) | fits |
| save-bind-in-program | 901 | 0 | 94,070 (1.176) | fits |
| save-bind-in-program-late | 853 | 0 | 95,387 (1.192) | fits |
| save-bind-in-verify | 856 | 0 | 94,067 (1.176) | fits |
| save-bind-in-verify-late | 851 | 0 | 78,989 (0.987) | fits |
| save-bind-burst | 1617 | 0 | 95,148 (1.189) | fits |
| backlog | 282 | 0 | 119,822 (1.498) | fits |
| backlog-adp | 310 | 0 | 119,108 (1.489) | fits |
| backlog-adp-refill | 324 | 0 | 119,108 (1.489) | fits |
| backlog-owed | 305 | 0 | 116,720 (1.459) | fits |
| acmp-disc | 874 | 0 | 74,257 (0.928) | fits |
| maap | 174 | 0 | 54,957 (0.687) | fits |
| aecp-fanout | 109 | 0 | 58,847 (0.736) | fits |
| acmp-cmd | 83 | 0 | 54,957 (0.687) | fits |
| aecp | 112 | 0 | 54,957 (0.687) | fits |
| aecp-largest-notice | 104 | 0 | 129,587 (1.620) | fits |
| aecp-held | 106 | 0 | 54,957 (0.687) | fits |
| datapath-events | 115 | 0 | 54,957 (0.687) | fits |
| fixture | 152 | 0 | 72,720 (0.909) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | +10.497 ms, 60,408 (0.755 ms), read-back | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 10.450 (20) | 9.550 |
| backlog-adp@blank-aged2-1 | 2 | +10.062 ms, 60,408 (0.755 ms), read-back | none | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 11.098 (20) | 8.902 |
| backlog-adp@blank-aged2-2 | 2 | +8.934 ms, 60,408 (0.755 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 11.150 (20) | 8.850 |
| backlog-adp@blank-aged2-3 | 2 | +6.779 ms, 60,408 (0.755 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 11.090 (20) | 8.910 |
| backlog-adp@blank-aged2-4 | 2 | +5.505 ms, 60,525 (0.757 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 11.032 (20) | 8.968 |
| backlog-adp@blank-aged2-5 | 2 | +4.580 ms, 60,376 (0.755 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 11.319 (20) | 8.681 |
| backlog-adp@blank-aged2-6 | 2 | +4.508 ms, 60,163 (0.752 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 11.234 (20) | 8.766 |
| backlog-adp@blank-aged2-7 | 2 | +2.970 ms, 60,007 (0.750 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 11.157 (20) | 8.843 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 10.142 (20) | 9.858 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 10.495 (20) | 9.505 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 10.315 (20) | 9.685 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 10.316 (20) | 9.684 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 10.351 (20) | 9.649 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 10.281 (20) | 9.719 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 10.374 (20) | 9.626 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 10.171 (20) | 9.829 |
| backlog-adp@program-aged2-0 | 2 | none | +10.435 ms, 80,607 (1.008 ms), issue | `backlog-adp@program-aged2-0.service.srp.last.if0` | 10.388 (20) | 9.612 |
| backlog-adp@program-aged2-1 | 2 | +10.053 ms, 80,528 (1.007 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 11.346 (20) | 8.654 |
| backlog-adp@program-aged2-2 | 2 | +8.833 ms, 80,528 (1.007 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 11.347 (20) | 8.653 |
| backlog-adp@program-aged2-3 | 2 | +6.763 ms, 80,607 (1.008 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 11.530 (20) | 8.470 |
| backlog-adp@program-aged2-4 | 2 | +6.625 ms, 80,607 (1.008 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 11.393 (20) | 8.607 |
| backlog-adp@program-aged2-5 | 2 | +5.365 ms, 80,645 (1.008 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 11.355 (20) | 8.645 |
| backlog-adp@program-aged2-6 | 2 | +4.424 ms, 80,159 (1.002 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 11.424 (20) | 8.576 |
| backlog-adp@program-aged2-7 | 2 | +2.992 ms, 80,075 (1.001 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 11.409 (20) | 8.591 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 10.336 (20) | 9.664 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 10.331 (20) | 9.669 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 10.153 (20) | 9.847 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 10.140 (20) | 9.860 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 10.515 (20) | 9.485 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 10.454 (20) | 9.546 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 10.185 (20) | 9.815 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 10.326 (20) | 9.674 |
| backlog-adp@verify-aged2-0 | 2 | none | +10.275 ms, 60,512 (0.756 ms), read-back | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 10.066 (20) | 9.934 |
| backlog-adp@verify-aged2-1 | 2 | none | none | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 11.267 (20) | 8.733 |
| backlog-adp@verify-aged2-2 | 2 | none | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 11.196 (20) | 8.804 |
| backlog-adp@verify-aged2-3 | 2 | none | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 11.074 (20) | 8.926 |
| backlog-adp@verify-aged2-4 | 2 | +6.809 ms, 60,865 (0.761 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 10.954 (20) | 9.046 |
| backlog-adp@verify-aged2-5 | 2 | +5.542 ms, 60,982 (0.762 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 11.059 (20) | 8.941 |
| backlog-adp@verify-aged2-6 | 2 | none | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 11.054 (20) | 8.946 |
| backlog-adp@verify-aged2-7 | 2 | none | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 11.158 (20) | 8.842 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 10.360 (20) | 9.640 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 10.290 (20) | 9.710 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 10.360 (20) | 9.640 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 10.486 (20) | 9.514 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 10.339 (20) | 9.661 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 10.306 (20) | 9.694 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 10.364 (20) | 9.636 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 10.131 (20) | 9.869 |

Least margin over the aged windows: 8.470 ms, `backlog-adp@program-aged2-3.service.srp.last.if0` at 11.530 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 4769.955 | 4,810 | 81 | 2 | 31.027 | yes | within |
| save-held | 1071.112 | 3,440 | 81 | - | 8.949 | no | within |
| save-starved | 3418.842 | 3,440 | 81 | - | 31.585 | yes | within |
| save | 1061.984 | 3,440 | 81 | - | 18.199 | no | within |

Names from their response to durable (save_burst.py; #920, #665's ruling of 2026-11-15, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-flight | 1 | 117.325 (0) | 5,000 | 2 | - | - | 16 steps (want 16), 7.264 ms | within |
| save-burst | 29 | 1077.628 (0) | 5,000 | 1 | - | - | sequence 1, 0 missing | within |

Binding changes from their response to durable (bind_save.py; the binding class's 100 ms window, Milan v1.2 5.5.3.5.3 and 5.3.8.3), with the part's erase of 120 ms and page program of 0.5 ms modelled:

| Group | Command | Sink | Durable, ms | Target ms | Saves | Erases | Verdict |
|---|---|---:|---:|---:|---:|---:|---|
| save-bind | BIND_RX | 0 | 288.781 | 800 | 4 | 4 | within |
| save-bind | STOP_STREAMING | 0 | 288.356 | 800 | 4 | 4 | within |
| save-bind | START_STREAMING | 0 | 288.458 | 800 | 4 | 4 | within |
| save-bind | UNBIND_RX | 0 | 288.775 | 800 | 4 | 4 | within |
| save-bind-in-capture | BIND_RX | 0 | 369.158 | 400 | 2 | 2 | within |
| save-bind-in-seal | BIND_RX | 0 | 367.559 | 400 | 2 | 2 | within |
| save-bind-in-erase | BIND_RX | 0 | 355.523 | 400 | 2 | 2 | within |
| save-bind-in-erase-late | BIND_RX | 0 | 305.755 | 400 | 2 | 2 | within |
| save-bind-in-blank | BIND_RX | 0 | 283.599 | 400 | 2 | 2 | within |
| save-bind-in-blank-late | BIND_RX | 0 | 288.275 | 400 | 2 | 2 | within |
| save-bind-in-program | BIND_RX | 0 | 286.176 | 400 | 2 | 2 | within |
| save-bind-in-program-late | BIND_RX | 0 | 282.694 | 400 | 2 | 2 | within |
| save-bind-in-verify | BIND_RX | 0 | 288.761 | 400 | 2 | 2 | within |
| save-bind-in-verify-late | BIND_RX | 0 | 283.385 | 400 | 2 | 2 | within |
| save-bind-burst | UNBIND_RX | 0 | 239.557 | 400 | 4 | 4 | within |
| save-bind-burst | UNBIND_RX | 1 | 230.051 | 400 | 4 | 4 | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-kept | 1844 | 16,167 (0.202) | 2,554 (0.032) |
| save-flight | 1515 | 87,567 (1.095) | 77,944 (0.974) |
| save-burst | 1423 | 87,605 (1.095) | 77,962 (0.975) |
| acmp-notk | 1139 | 88,799 (1.110) | 77,913 (0.974) |
| adp-advertise | 732 | 15,780 (0.197) | 2,413 (0.030) |
| save-second | 478 | 80,365 (1.005) | 78,221 (0.978) |
| backlog-adp@blank-0 | 300 | 68,382 (0.855) | 59,725 (0.747) |
| backlog-adp@blank-1 | 300 | 68,382 (0.855) | 59,725 (0.747) |
| backlog-adp@blank-2 | 300 | 68,382 (0.855) | 59,725 (0.747) |
| backlog-adp@blank-3 | 300 | 68,382 (0.855) | 59,725 (0.747) |
| backlog-adp@blank-4 | 300 | 68,382 (0.855) | 59,725 (0.747) |
| backlog-adp@blank-5 | 300 | 68,382 (0.855) | 59,725 (0.747) |
| backlog-adp@blank-6 | 300 | 68,508 (0.856) | 59,725 (0.747) |
| backlog-adp@blank-7 | 300 | 68,508 (0.856) | 59,725 (0.747) |
| backlog-adp@program-0 | 322 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@program-1 | 322 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@program-2 | 322 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@program-3 | 322 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@program-4 | 326 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@program-5 | 326 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@program-6 | 326 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@program-7 | 326 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-0 | 343 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-1 | 343 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-2 | 343 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-3 | 343 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-4 | 343 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-5 | 343 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-6 | 343 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-7 | 344 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@blank-aged2-0 | 296 | 70,147 (0.877) | 59,546 (0.744) |
| backlog-adp@blank-aged2-1 | 297 | 69,259 (0.866) | 59,546 (0.744) |
| backlog-adp@blank-aged2-2 | 297 | 69,325 (0.867) | 59,546 (0.744) |
| backlog-adp@blank-aged2-3 | 299 | 70,508 (0.881) | 59,546 (0.744) |
| backlog-adp@blank-aged2-4 | 298 | 70,522 (0.882) | 59,546 (0.744) |
| backlog-adp@blank-aged2-5 | 297 | 69,848 (0.873) | 59,828 (0.748) |
| backlog-adp@blank-aged2-6 | 298 | 69,745 (0.872) | 59,828 (0.748) |
| backlog-adp@blank-aged2-7 | 297 | 69,687 (0.871) | 59,809 (0.748) |
| backlog-adp@blank-aged1-0 | 297 | 76,549 (0.957) | 59,968 (0.750) |
| backlog-adp@blank-aged1-1 | 296 | 69,804 (0.873) | 59,968 (0.750) |
| backlog-adp@blank-aged1-2 | 296 | 69,898 (0.874) | 59,968 (0.750) |
| backlog-adp@blank-aged1-3 | 296 | 69,866 (0.873) | 59,968 (0.750) |
| backlog-adp@blank-aged1-4 | 296 | 69,871 (0.873) | 59,968 (0.750) |
| backlog-adp@blank-aged1-5 | 299 | 74,686 (0.934) | 59,968 (0.750) |
| backlog-adp@blank-aged1-6 | 298 | 70,495 (0.881) | 59,968 (0.750) |
| backlog-adp@blank-aged1-7 | 297 | 70,487 (0.881) | 59,968 (0.750) |
| backlog-adp@program-aged2-0 | 319 | 88,124 (1.102) | 78,567 (0.982) |
| backlog-adp@program-aged2-1 | 322 | 88,321 (1.104) | 78,567 (0.982) |
| backlog-adp@program-aged2-2 | 320 | 88,360 (1.105) | 78,567 (0.982) |
| backlog-adp@program-aged2-3 | 320 | 88,319 (1.104) | 78,567 (0.982) |
| backlog-adp@program-aged2-4 | 320 | 88,364 (1.105) | 78,567 (0.982) |
| backlog-adp@program-aged2-5 | 320 | 88,364 (1.105) | 78,567 (0.982) |
| backlog-adp@program-aged2-6 | 324 | 88,377 (1.105) | 78,425 (0.980) |
| backlog-adp@program-aged2-7 | 322 | 88,322 (1.104) | 78,242 (0.978) |
| backlog-adp@program-aged1-0 | 319 | 89,738 (1.122) | 78,735 (0.984) |
| backlog-adp@program-aged1-1 | 319 | 89,814 (1.123) | 78,735 (0.984) |
| backlog-adp@program-aged1-2 | 319 | 89,825 (1.123) | 78,735 (0.984) |
| backlog-adp@program-aged1-3 | 320 | 90,335 (1.129) | 78,735 (0.984) |
| backlog-adp@program-aged1-4 | 319 | 89,709 (1.121) | 78,735 (0.984) |
| backlog-adp@program-aged1-5 | 319 | 89,696 (1.121) | 78,735 (0.984) |
| backlog-adp@program-aged1-6 | 319 | 90,056 (1.126) | 78,735 (0.984) |
| backlog-adp@program-aged1-7 | 320 | 89,763 (1.122) | 78,735 (0.984) |
| backlog-adp@verify-aged2-0 | 344 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-aged2-1 | 344 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-aged2-2 | 344 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-aged2-3 | 344 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-aged2-4 | 344 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-aged2-5 | 347 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-aged2-6 | 346 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-aged2-7 | 345 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-aged1-0 | 343 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-aged1-1 | 346 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-aged1-2 | 344 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-aged1-3 | 343 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-aged1-4 | 343 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-aged1-5 | 343 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-aged1-6 | 346 | 94,371 (1.180) | 77,913 (0.974) |
| backlog-adp@verify-aged1-7 | 345 | 94,371 (1.180) | 77,913 (0.974) |
| srp-bound | 636 | 89,345 (1.117) | 77,913 (0.974) |
| acmp-noresp | 689 | 88,722 (1.109) | 77,913 (0.974) |
| save-held | 733 | 87,523 (1.094) | 77,953 (0.974) |
| save-starved | 397 | 80,418 (1.005) | 78,296 (0.979) |
| save-bind | 3758 | 94,198 (1.177) | 77,913 (0.974) |
| save | 660 | 87,523 (1.094) | 77,685 (0.971) |
| adp-link | 234 | 15,780 (0.197) | 2,413 (0.030) |
| adp-gm | 234 | 15,780 (0.197) | 2,413 (0.030) |
| adp-discover | 234 | 15,780 (0.197) | 2,413 (0.030) |
| control | 234 | 15,780 (0.197) | 2,413 (0.030) |
| srp | 271 | 15,780 (0.197) | 2,413 (0.030) |
| save-bind-in-capture | 1968 | 88,606 (1.108) | 77,913 (0.974) |
| save-bind-in-seal | 1968 | 88,609 (1.108) | 77,913 (0.974) |
| save-bind-in-erase | 1965 | 88,513 (1.106) | 77,834 (0.973) |
| save-bind-in-erase-late | 2012 | 88,513 (1.106) | 77,913 (0.974) |
| save-bind-in-blank | 2067 | 88,655 (1.108) | 77,834 (0.973) |
| save-bind-in-blank-late | 2067 | 88,582 (1.107) | 78,052 (0.976) |
| save-bind-in-program | 2063 | 94,070 (1.176) | 77,841 (0.973) |
| save-bind-in-program-late | 2071 | 95,387 (1.192) | 77,931 (0.974) |
| save-bind-in-verify | 2075 | 94,067 (1.176) | 77,841 (0.973) |
| save-bind-in-verify-late | 2078 | 88,467 (1.106) | 77,799 (0.972) |
| save-bind-burst | 3260 | 95,148 (1.189) | 78,161 (0.977) |
| backlog | 265 | 15,780 (0.197) | 2,413 (0.030) |
| backlog-adp | 271 | 15,780 (0.197) | 2,413 (0.030) |
| backlog-adp-refill | 274 | 15,780 (0.197) | 2,413 (0.030) |
| backlog-owed | 276 | 15,780 (0.197) | 2,413 (0.030) |
| acmp-disc | 380 | 88,655 (1.108) | 77,913 (0.974) |
| maap | 165 | 15,677 (0.196) | 2,413 (0.030) |
| aecp-fanout | 80 | 15,677 (0.196) | 2,413 (0.030) |
| acmp-cmd | 65 | 15,677 (0.196) | 2,413 (0.030) |
| aecp | 80 | 15,677 (0.196) | 2,413 (0.030) |
| aecp-largest-notice | 78 | 15,677 (0.196) | 2,413 (0.030) |
| aecp-held | 98 | 15,677 (0.196) | 2,413 (0.030) |
| datapath-events | 69 | 15,677 (0.196) | 2,413 (0.030) |
| fixture | 130 | 89,001 (1.113) | 77,834 (0.973) |

Longest pass that carries a step: 95,387 CPU cycles (1.192 ms), save-bind-in-program-late; longest step: 78,735 (0.984 ms), backlog-adp@program-aged1-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| Talker Advertise RX for every input, no binding (kept) | `srp.kept_advertise.if0` | 46,199 | 0.577 | 20 | 20 | fits | 46,265 | 12 | 0.890 |
| Talker RX at the bound after a freed block (count) | `srp.kept_recount.if0` | 43,027 | 0.538 | 20 | 20 | fits | 43,093 | 12 | 0.886 |
| Talker Failed RX for every input, no binding (kept) | `srp.kept_failed.if0` | 45,750 | 0.572 | 20 | 20 | fits | 45,816 | 12 | 0.892 |
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 122,510 | 1.531 | 20 | 200 | fits | 123,450 | 221 | 0.399 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 183,721 | 2.297 | 20 | 20 | fits | 93,162 | 115 | 0.206 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 288,385 | 3.605 | 20 | 24 | fits | 88,868 | 56 | 0.535 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 192,868 | 2.411 | 20 | 50 | fits | 89,638 | 211 | 0.294 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 743,274 | 9.291 | 20 | 20 | fits | 24,863 | 12 | 0.796 |
| an MRPDU its join timer owes, the longest | `save-flight.mrpdu.join.if0` | 37,637 | 0.470 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-flight.mrpdu.leaveall.if0` | 39,412 | 0.493 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 72,236 | 0.903 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-burst.held.adp.if0` | 122,641 | 1.533 | 20 | 200 | fits | 123,450 | 221 | 0.399 |
| ACMP record, every channel at its refill rate, the longest | `save-burst.held.acmp.if0` | 299,435 | 3.743 | 20 | 20 | fits | 91,865 | 39 | 0.652 |
| AECP record, every channel at its refill rate, the longest | `save-burst.held.aecp.if0` | 168,961 | 2.112 | 20 | 24 | fits | 95,607 | 38 | 0.740 |
| MAAP record, every channel at its refill rate, the longest | `save-burst.held.maap.if0` | 176,095 | 2.201 | 20 | 50 | fits | 117,799 | 252 | 0.210 |
| SRP record, every channel at its refill rate, the longest | `save-burst.held.srp.if0` | 700,066 | 8.751 | 20 | 20 | fits | 95,312 | 38 | 0.738 |
| an MRPDU its join timer owes, the longest | `save-burst.mrpdu.join.if0` | 153,050 | 1.913 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-burst.mrpdu.leaveall.if0` | 187,440 | 2.343 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-burst.mrpdu.periodic.if0` | 208,893 | 2.611 | 49 | 49 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 9,266 | 0.116 | 20 | 20 | fits | 25,502 | 19 (14) | 0.881 |
| LINK_UP | `adp.link_up.if0` | 2,890 | 0.036 | 20 | 200 | fits | 19,889 | 44 (12) | 0.673 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 6,368 | 0.080 | 20 | 200 | fits | 14,117 | 23 (39) | 0.607 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 4,875 | 0.061 | 20 | 200 | fits | 2,003 | 10 (11) | 0.400 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 357,462 | 4.468 | 20 | 20 | fits | 120,404 | 229 | 0.309 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 288,369 | 3.605 | 20 | 200 | fits | 115,662 | 179 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 418,219 | 5.228 | 20 | 200 | fits | 120,404 | 229 | 0.309 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 289,293 | 3.616 | 20 | 20 | fits | 115,662 | 179 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 418,923 | 5.237 | 20 | 20 | fits | 120,404 | 229 | 0.309 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 177,271 | 2.216 | 20 | 24 | fits | 119,387 | 145 | 0.349 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 291,943 | 3.649 | 20 | 24 | fits | 115,662 | 179 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 291,877 | 3.648 | 20 | 50 | fits | 115,662 | 179 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 421,947 | 5.274 | 20 | 50 | fits | 120,404 | 229 | 0.309 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 515,463 | 6.443 | 20 | 20 | fits | 93,582 | 32 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 886,032 | 11.075 | 20 | 20 | fits | 25,413 | 13 | 0.793 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 347,462 | 4.343 | 20 | 20 | fits | 120,404 | 229 | 0.309 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 278,369 | 3.480 | 20 | 200 | fits | 115,662 | 179 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 408,219 | 5.103 | 20 | 200 | fits | 120,404 | 229 | 0.309 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 279,293 | 3.491 | 20 | 20 | fits | 115,662 | 179 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 408,923 | 5.112 | 20 | 20 | fits | 120,404 | 229 | 0.309 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 167,271 | 2.091 | 20 | 24 | fits | 119,387 | 145 | 0.349 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 281,943 | 3.524 | 20 | 24 | fits | 115,662 | 179 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 281,877 | 3.523 | 20 | 50 | fits | 115,662 | 179 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 411,947 | 5.149 | 20 | 50 | fits | 120,404 | 229 | 0.309 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 505,463 | 6.318 | 20 | 20 | fits | 93,582 | 32 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 876,032 | 10.950 | 20 | 20 | fits | 25,413 | 13 | 0.793 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 337,462 | 4.218 | 20 | 20 | fits | 120,404 | 229 | 0.309 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 268,369 | 3.355 | 20 | 200 | fits | 115,662 | 179 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 398,219 | 4.978 | 20 | 200 | fits | 120,404 | 229 | 0.309 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 269,293 | 3.366 | 20 | 20 | fits | 115,662 | 179 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 398,923 | 4.987 | 20 | 20 | fits | 120,404 | 229 | 0.309 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 157,271 | 1.966 | 20 | 24 | fits | 119,387 | 145 | 0.349 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 271,943 | 3.399 | 20 | 24 | fits | 115,662 | 179 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 271,877 | 3.398 | 20 | 50 | fits | 115,662 | 179 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 401,947 | 5.024 | 20 | 50 | fits | 120,404 | 229 | 0.309 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 495,463 | 6.193 | 20 | 20 | fits | 93,582 | 32 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 866,032 | 10.825 | 20 | 20 | fits | 25,413 | 13 | 0.793 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 327,462 | 4.093 | 20 | 20 | fits | 120,404 | 229 | 0.309 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 258,369 | 3.230 | 20 | 200 | fits | 115,662 | 179 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 388,219 | 4.853 | 20 | 200 | fits | 120,404 | 229 | 0.309 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 259,293 | 3.241 | 20 | 20 | fits | 115,662 | 179 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 388,923 | 4.862 | 20 | 20 | fits | 120,404 | 229 | 0.309 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 147,271 | 1.841 | 20 | 24 | fits | 119,387 | 145 | 0.349 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 261,943 | 3.274 | 20 | 24 | fits | 115,662 | 179 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 261,877 | 3.273 | 20 | 50 | fits | 115,662 | 179 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 391,947 | 4.899 | 20 | 50 | fits | 120,404 | 229 | 0.309 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 485,463 | 6.068 | 20 | 20 | fits | 93,582 | 32 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 856,032 | 10.700 | 20 | 20 | fits | 25,413 | 13 | 0.793 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 317,462 | 3.968 | 20 | 20 | fits | 120,404 | 229 | 0.309 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 248,369 | 3.105 | 20 | 200 | fits | 115,662 | 179 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 378,219 | 4.728 | 20 | 200 | fits | 120,404 | 229 | 0.309 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 249,293 | 3.116 | 20 | 20 | fits | 115,662 | 179 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 378,923 | 4.737 | 20 | 20 | fits | 120,404 | 229 | 0.309 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 137,271 | 1.716 | 20 | 24 | fits | 119,387 | 145 | 0.349 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 251,943 | 3.149 | 20 | 24 | fits | 115,662 | 179 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 251,877 | 3.148 | 20 | 50 | fits | 115,662 | 179 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 381,947 | 4.774 | 20 | 50 | fits | 120,404 | 229 | 0.309 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 475,463 | 5.943 | 20 | 20 | fits | 93,582 | 32 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 846,032 | 10.575 | 20 | 20 | fits | 25,413 | 13 | 0.793 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 307,462 | 3.843 | 20 | 20 | fits | 120,404 | 229 | 0.309 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 238,369 | 2.980 | 20 | 200 | fits | 115,662 | 179 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 368,219 | 4.603 | 20 | 200 | fits | 120,404 | 229 | 0.309 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 239,293 | 2.991 | 20 | 20 | fits | 115,662 | 179 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 368,923 | 4.612 | 20 | 20 | fits | 120,404 | 229 | 0.309 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 127,271 | 1.591 | 20 | 24 | fits | 119,387 | 145 | 0.349 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 241,943 | 3.024 | 20 | 24 | fits | 115,662 | 179 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 241,877 | 3.023 | 20 | 50 | fits | 115,662 | 179 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 371,947 | 4.649 | 20 | 50 | fits | 120,404 | 229 | 0.309 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 465,463 | 5.818 | 20 | 20 | fits | 93,582 | 32 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 836,032 | 10.450 | 20 | 20 | fits | 25,413 | 13 | 0.793 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 373,263 | 4.666 | 20 | 20 | fits | 117,437 | 228 | 0.268 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 305,486 | 3.819 | 20 | 200 | fits | 116,185 | 178 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 422,307 | 5.279 | 20 | 200 | fits | 117,437 | 228 | 0.268 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 306,410 | 3.830 | 20 | 20 | fits | 116,185 | 178 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 423,011 | 5.288 | 20 | 20 | fits | 117,437 | 228 | 0.268 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 184,938 | 2.312 | 20 | 24 | fits | 119,470 | 146 | 0.349 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 309,060 | 3.863 | 20 | 24 | fits | 116,185 | 178 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 308,994 | 3.862 | 20 | 50 | fits | 116,185 | 178 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 426,035 | 5.325 | 20 | 50 | fits | 117,437 | 228 | 0.268 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 519,705 | 6.496 | 20 | 20 | fits | 93,736 | 32 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 906,226 | 11.328 | 20 | 20 | fits | 30,754 | 19 | 0.832 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 363,263 | 4.541 | 20 | 20 | fits | 117,437 | 228 | 0.268 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 295,486 | 3.694 | 20 | 200 | fits | 116,185 | 178 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 412,307 | 5.154 | 20 | 200 | fits | 117,437 | 228 | 0.268 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 296,410 | 3.705 | 20 | 20 | fits | 116,185 | 178 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 413,011 | 5.163 | 20 | 20 | fits | 117,437 | 228 | 0.268 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 174,938 | 2.187 | 20 | 24 | fits | 119,470 | 146 | 0.349 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 299,060 | 3.738 | 20 | 24 | fits | 116,185 | 178 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 298,994 | 3.737 | 20 | 50 | fits | 116,185 | 178 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 416,035 | 5.200 | 20 | 50 | fits | 117,437 | 228 | 0.268 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 509,705 | 6.371 | 20 | 20 | fits | 93,736 | 32 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 896,226 | 11.203 | 20 | 20 | fits | 30,754 | 19 | 0.832 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 302,881 | 3.786 | 20 | 20 | fits | 112,411 | 205 | 0.299 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 233,007 | 2.913 | 20 | 200 | fits | 119,227 | 204 | 0.364 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 344,802 | 4.310 | 20 | 200 | fits | 112,411 | 205 | 0.299 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 233,931 | 2.924 | 20 | 20 | fits | 119,227 | 204 | 0.364 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 345,506 | 4.319 | 20 | 20 | fits | 112,411 | 205 | 0.299 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 118,344 | 1.479 | 20 | 24 | fits | 120,200 | 145 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 236,581 | 2.957 | 20 | 24 | fits | 119,227 | 204 | 0.364 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 236,515 | 2.956 | 20 | 50 | fits | 119,227 | 204 | 0.364 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 348,530 | 4.357 | 20 | 50 | fits | 112,411 | 205 | 0.299 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 441,909 | 5.524 | 20 | 20 | fits | 93,445 | 32 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 827,511 | 10.344 | 20 | 20 | fits | 25,336 | 12 | 0.799 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 302,881 | 3.786 | 20 | 20 | fits | 112,411 | 205 | 0.299 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 233,007 | 2.913 | 20 | 200 | fits | 119,227 | 204 | 0.364 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 344,802 | 4.310 | 20 | 200 | fits | 112,411 | 205 | 0.299 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 233,931 | 2.924 | 20 | 20 | fits | 119,227 | 204 | 0.364 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 345,506 | 4.319 | 20 | 20 | fits | 112,411 | 205 | 0.299 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 118,344 | 1.479 | 20 | 24 | fits | 120,200 | 145 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 236,581 | 2.957 | 20 | 24 | fits | 119,227 | 204 | 0.364 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 236,515 | 2.956 | 20 | 50 | fits | 119,227 | 204 | 0.364 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 348,530 | 4.357 | 20 | 50 | fits | 112,411 | 205 | 0.299 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 441,909 | 5.524 | 20 | 20 | fits | 93,445 | 32 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 827,511 | 10.344 | 20 | 20 | fits | 25,336 | 12 | 0.799 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 302,881 | 3.786 | 20 | 20 | fits | 112,411 | 205 | 0.299 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 233,007 | 2.913 | 20 | 200 | fits | 119,227 | 204 | 0.364 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 344,802 | 4.310 | 20 | 200 | fits | 112,411 | 205 | 0.299 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 233,931 | 2.924 | 20 | 20 | fits | 119,227 | 204 | 0.364 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 345,506 | 4.319 | 20 | 20 | fits | 112,411 | 205 | 0.299 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 118,344 | 1.479 | 20 | 24 | fits | 120,200 | 145 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 236,581 | 2.957 | 20 | 24 | fits | 119,227 | 204 | 0.364 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 236,515 | 2.956 | 20 | 50 | fits | 119,227 | 204 | 0.364 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 348,530 | 4.357 | 20 | 50 | fits | 112,411 | 205 | 0.299 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 441,909 | 5.524 | 20 | 20 | fits | 93,445 | 32 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 827,511 | 10.344 | 20 | 20 | fits | 25,336 | 12 | 0.799 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 296,571 | 3.707 | 20 | 20 | fits | 111,704 | 202 | 0.310 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 234,364 | 2.930 | 20 | 200 | fits | 119,608 | 203 | 0.361 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 345,452 | 4.318 | 20 | 200 | fits | 111,704 | 202 | 0.310 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 235,288 | 2.941 | 20 | 20 | fits | 119,608 | 203 | 0.361 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 346,156 | 4.327 | 20 | 20 | fits | 111,704 | 202 | 0.310 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 119,320 | 1.492 | 20 | 24 | fits | 118,507 | 145 | 0.340 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 237,938 | 2.974 | 20 | 24 | fits | 119,608 | 203 | 0.361 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 237,872 | 2.973 | 20 | 50 | fits | 119,608 | 203 | 0.361 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 349,180 | 4.365 | 20 | 50 | fits | 111,704 | 202 | 0.310 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 442,781 | 5.535 | 20 | 20 | fits | 93,667 | 32 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 814,839 | 10.185 | 20 | 20 | fits | 95,323 | 36 | 0.632 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 367,344 | 4.592 | 20 | 20 | fits | 115,641 | 223 | 0.261 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 312,173 | 3.902 | 20 | 200 | fits | 115,558 | 178 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 427,198 | 5.340 | 20 | 200 | fits | 115,641 | 223 | 0.261 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 313,097 | 3.914 | 20 | 20 | fits | 115,558 | 178 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 427,902 | 5.349 | 20 | 20 | fits | 115,641 | 223 | 0.261 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 201,179 | 2.515 | 20 | 24 | fits | 119,575 | 145 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 315,747 | 3.947 | 20 | 24 | fits | 115,558 | 178 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 315,681 | 3.946 | 20 | 50 | fits | 115,558 | 178 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 430,926 | 5.387 | 20 | 50 | fits | 115,641 | 223 | 0.261 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 524,529 | 6.557 | 20 | 20 | fits | 93,669 | 33 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 897,447 | 11.218 | 20 | 20 | fits | 95,434 | 36 | 0.631 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 347,344 | 4.342 | 20 | 20 | fits | 115,641 | 223 | 0.261 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 292,173 | 3.652 | 20 | 200 | fits | 115,558 | 178 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 407,198 | 5.090 | 20 | 200 | fits | 115,641 | 223 | 0.261 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 293,097 | 3.664 | 20 | 20 | fits | 115,558 | 178 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 407,902 | 5.099 | 20 | 20 | fits | 115,641 | 223 | 0.261 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 181,179 | 2.265 | 20 | 24 | fits | 119,575 | 145 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 295,747 | 3.697 | 20 | 24 | fits | 115,558 | 178 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 295,681 | 3.696 | 20 | 50 | fits | 115,558 | 178 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 410,926 | 5.137 | 20 | 50 | fits | 115,641 | 223 | 0.261 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 504,529 | 6.307 | 20 | 20 | fits | 93,669 | 33 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 877,447 | 10.968 | 20 | 20 | fits | 95,434 | 36 | 0.631 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 327,344 | 4.092 | 20 | 20 | fits | 115,641 | 223 | 0.261 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 272,173 | 3.402 | 20 | 200 | fits | 115,558 | 178 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 387,198 | 4.840 | 20 | 200 | fits | 115,641 | 223 | 0.261 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 273,097 | 3.414 | 20 | 20 | fits | 115,558 | 178 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 387,902 | 4.849 | 20 | 20 | fits | 115,641 | 223 | 0.261 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 161,179 | 2.015 | 20 | 24 | fits | 119,575 | 145 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 275,747 | 3.447 | 20 | 24 | fits | 115,558 | 178 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 275,681 | 3.446 | 20 | 50 | fits | 115,558 | 178 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 390,926 | 4.887 | 20 | 50 | fits | 115,641 | 223 | 0.261 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 484,529 | 6.057 | 20 | 20 | fits | 93,669 | 33 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 857,447 | 10.718 | 20 | 20 | fits | 95,434 | 36 | 0.631 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 307,344 | 3.842 | 20 | 20 | fits | 115,641 | 223 | 0.261 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 252,173 | 3.152 | 20 | 200 | fits | 115,558 | 178 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 367,198 | 4.590 | 20 | 200 | fits | 115,641 | 223 | 0.261 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 253,097 | 3.164 | 20 | 20 | fits | 115,558 | 178 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 367,902 | 4.599 | 20 | 20 | fits | 115,641 | 223 | 0.261 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 141,179 | 1.765 | 20 | 24 | fits | 119,575 | 145 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 255,747 | 3.197 | 20 | 24 | fits | 115,558 | 178 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 255,681 | 3.196 | 20 | 50 | fits | 115,558 | 178 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 370,926 | 4.637 | 20 | 50 | fits | 115,641 | 223 | 0.261 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 464,529 | 5.807 | 20 | 20 | fits | 93,669 | 33 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 837,447 | 10.468 | 20 | 20 | fits | 95,434 | 36 | 0.631 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 366,620 | 4.583 | 20 | 20 | fits | 110,318 | 221 | 0.260 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 298,593 | 3.732 | 20 | 200 | fits | 115,837 | 181 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 408,295 | 5.104 | 20 | 200 | fits | 110,318 | 221 | 0.260 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 299,517 | 3.744 | 20 | 20 | fits | 115,837 | 181 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 408,999 | 5.112 | 20 | 20 | fits | 110,318 | 221 | 0.260 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 178,273 | 2.228 | 20 | 24 | fits | 119,133 | 146 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 302,167 | 3.777 | 20 | 24 | fits | 115,837 | 181 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 302,101 | 3.776 | 20 | 50 | fits | 115,837 | 181 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 412,023 | 5.150 | 20 | 50 | fits | 110,318 | 221 | 0.260 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 505,580 | 6.320 | 20 | 20 | fits | 93,623 | 32 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 867,247 | 10.841 | 20 | 20 | fits | 88,802 | 39 | 0.668 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 356,620 | 4.458 | 20 | 20 | fits | 110,318 | 221 | 0.260 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 288,593 | 3.607 | 20 | 200 | fits | 115,837 | 181 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 398,295 | 4.979 | 20 | 200 | fits | 110,318 | 221 | 0.260 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 289,517 | 3.619 | 20 | 20 | fits | 115,837 | 181 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 398,999 | 4.987 | 20 | 20 | fits | 110,318 | 221 | 0.260 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 168,273 | 2.103 | 20 | 24 | fits | 119,133 | 146 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 292,167 | 3.652 | 20 | 24 | fits | 115,837 | 181 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 292,101 | 3.651 | 20 | 50 | fits | 115,837 | 181 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 402,023 | 5.025 | 20 | 50 | fits | 110,318 | 221 | 0.260 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 495,580 | 6.195 | 20 | 20 | fits | 93,623 | 32 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 857,247 | 10.716 | 20 | 20 | fits | 88,802 | 39 | 0.668 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 346,620 | 4.333 | 20 | 20 | fits | 110,318 | 221 | 0.260 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 278,593 | 3.482 | 20 | 200 | fits | 115,837 | 181 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 388,295 | 4.854 | 20 | 200 | fits | 110,318 | 221 | 0.260 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 279,517 | 3.494 | 20 | 20 | fits | 115,837 | 181 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 388,999 | 4.862 | 20 | 20 | fits | 110,318 | 221 | 0.260 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 158,273 | 1.978 | 20 | 24 | fits | 119,133 | 146 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 282,167 | 3.527 | 20 | 24 | fits | 115,837 | 181 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 282,101 | 3.526 | 20 | 50 | fits | 115,837 | 181 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 392,023 | 4.900 | 20 | 50 | fits | 110,318 | 221 | 0.260 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 485,580 | 6.070 | 20 | 20 | fits | 93,623 | 32 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 847,247 | 10.591 | 20 | 20 | fits | 88,802 | 39 | 0.668 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 336,620 | 4.208 | 20 | 20 | fits | 110,318 | 221 | 0.260 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 268,593 | 3.357 | 20 | 200 | fits | 115,837 | 181 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 378,295 | 4.729 | 20 | 200 | fits | 110,318 | 221 | 0.260 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 269,517 | 3.369 | 20 | 20 | fits | 115,837 | 181 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 378,999 | 4.737 | 20 | 20 | fits | 110,318 | 221 | 0.260 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 148,273 | 1.853 | 20 | 24 | fits | 119,133 | 146 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 272,167 | 3.402 | 20 | 24 | fits | 115,837 | 181 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 272,101 | 3.401 | 20 | 50 | fits | 115,837 | 181 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 382,023 | 4.775 | 20 | 50 | fits | 110,318 | 221 | 0.260 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 475,580 | 5.945 | 20 | 20 | fits | 93,623 | 32 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 837,247 | 10.466 | 20 | 20 | fits | 88,802 | 39 | 0.668 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 326,620 | 4.083 | 20 | 20 | fits | 110,318 | 221 | 0.260 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 258,593 | 3.232 | 20 | 200 | fits | 115,837 | 181 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 368,295 | 4.604 | 20 | 200 | fits | 110,318 | 221 | 0.260 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 259,517 | 3.244 | 20 | 20 | fits | 115,837 | 181 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 368,999 | 4.612 | 20 | 20 | fits | 110,318 | 221 | 0.260 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 138,273 | 1.728 | 20 | 24 | fits | 119,133 | 146 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 262,167 | 3.277 | 20 | 24 | fits | 115,837 | 181 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 262,101 | 3.276 | 20 | 50 | fits | 115,837 | 181 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 372,023 | 4.650 | 20 | 50 | fits | 110,318 | 221 | 0.260 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 465,580 | 5.820 | 20 | 20 | fits | 93,623 | 32 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 827,247 | 10.341 | 20 | 20 | fits | 88,802 | 39 | 0.668 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 316,620 | 3.958 | 20 | 20 | fits | 110,318 | 221 | 0.260 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 248,593 | 3.107 | 20 | 200 | fits | 115,837 | 181 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 358,295 | 4.479 | 20 | 200 | fits | 110,318 | 221 | 0.260 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 249,517 | 3.119 | 20 | 20 | fits | 115,837 | 181 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 358,999 | 4.487 | 20 | 20 | fits | 110,318 | 221 | 0.260 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 128,273 | 1.603 | 20 | 24 | fits | 119,133 | 146 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 252,167 | 3.152 | 20 | 24 | fits | 115,837 | 181 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 252,101 | 3.151 | 20 | 50 | fits | 115,837 | 181 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 362,023 | 4.525 | 20 | 50 | fits | 110,318 | 221 | 0.260 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 455,580 | 5.695 | 20 | 20 | fits | 93,623 | 32 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 817,247 | 10.216 | 20 | 20 | fits | 88,802 | 39 | 0.668 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 307,298 | 3.841 | 20 | 20 | fits | 107,314 | 234 | 0.296 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 242,674 | 3.033 | 20 | 200 | fits | 118,606 | 209 | 0.360 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 349,372 | 4.367 | 20 | 200 | fits | 107,314 | 234 | 0.296 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 243,598 | 3.045 | 20 | 20 | fits | 118,606 | 209 | 0.360 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 350,076 | 4.376 | 20 | 20 | fits | 107,314 | 234 | 0.296 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 119,470 | 1.493 | 20 | 24 | fits | 120,330 | 106 | 0.344 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 246,248 | 3.078 | 20 | 24 | fits | 118,606 | 209 | 0.360 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 246,182 | 3.077 | 20 | 50 | fits | 118,606 | 209 | 0.360 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 353,100 | 4.414 | 20 | 50 | fits | 107,314 | 234 | 0.296 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 446,837 | 5.585 | 20 | 20 | fits | 93,803 | 32 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 838,222 | 10.478 | 20 | 20 | fits | 30,493 | 19 | 0.829 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 352,675 | 4.408 | 20 | 20 | fits | 111,342 | 205 | 0.252 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 297,208 | 3.715 | 20 | 200 | fits | 116,166 | 201 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 407,934 | 5.099 | 20 | 200 | fits | 111,342 | 205 | 0.252 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 298,132 | 3.727 | 20 | 20 | fits | 116,166 | 201 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 408,638 | 5.108 | 20 | 20 | fits | 111,342 | 205 | 0.252 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 176,559 | 2.207 | 20 | 24 | fits | 119,198 | 146 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 300,782 | 3.760 | 20 | 24 | fits | 116,166 | 201 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 300,716 | 3.759 | 20 | 50 | fits | 116,166 | 201 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 411,662 | 5.146 | 20 | 50 | fits | 111,342 | 205 | 0.252 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 505,115 | 6.314 | 20 | 20 | fits | 93,519 | 32 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 866,881 | 10.836 | 20 | 20 | fits | 95,544 | 37 | 0.630 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 307,445 | 3.843 | 20 | 20 | fits | 110,397 | 221 | 0.261 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 239,339 | 2.992 | 20 | 200 | fits | 115,855 | 181 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 349,120 | 4.364 | 20 | 200 | fits | 110,397 | 221 | 0.261 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 240,263 | 3.003 | 20 | 20 | fits | 115,855 | 181 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 349,824 | 4.373 | 20 | 20 | fits | 110,397 | 221 | 0.261 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 118,968 | 1.487 | 20 | 24 | fits | 118,231 | 143 | 0.340 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 242,913 | 3.036 | 20 | 24 | fits | 115,855 | 181 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 242,847 | 3.036 | 20 | 50 | fits | 115,855 | 181 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 352,848 | 4.411 | 20 | 50 | fits | 110,397 | 221 | 0.261 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 446,499 | 5.581 | 20 | 20 | fits | 93,717 | 32 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 836,032 | 10.450 | 20 | 20 | fits | 33,920 | 25 | 0.816 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 296,955 | 3.712 | 20 | 20 | fits | 106,013 | 199 | 0.268 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 233,212 | 2.915 | 20 | 200 | fits | 118,285 | 199 | 0.363 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 338,609 | 4.233 | 20 | 200 | fits | 106,013 | 199 | 0.268 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 234,136 | 2.927 | 20 | 20 | fits | 118,285 | 199 | 0.363 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 339,313 | 4.241 | 20 | 20 | fits | 106,013 | 199 | 0.268 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 119,491 | 1.494 | 20 | 24 | fits | 118,046 | 142 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 236,786 | 2.960 | 20 | 24 | fits | 118,285 | 199 | 0.363 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 236,720 | 2.959 | 20 | 50 | fits | 118,285 | 199 | 0.363 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 342,337 | 4.279 | 20 | 50 | fits | 106,013 | 199 | 0.268 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 435,856 | 5.448 | 20 | 20 | fits | 93,585 | 32 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 887,845 | 11.098 | 20 | 20 | fits | 26,235 | 13 | 0.814 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 294,523 | 3.682 | 20 | 20 | fits | 104,916 | 196 | 0.274 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 239,393 | 2.992 | 20 | 200 | fits | 119,502 | 203 | 0.359 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 343,693 | 4.296 | 20 | 200 | fits | 104,916 | 196 | 0.274 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 240,317 | 3.004 | 20 | 20 | fits | 119,502 | 203 | 0.359 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 344,397 | 4.305 | 20 | 20 | fits | 104,916 | 196 | 0.274 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 124,455 | 1.556 | 20 | 24 | fits | 118,046 | 142 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 242,967 | 3.037 | 20 | 24 | fits | 119,502 | 203 | 0.359 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 242,901 | 3.036 | 20 | 50 | fits | 119,502 | 203 | 0.359 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 347,421 | 4.343 | 20 | 50 | fits | 104,916 | 196 | 0.274 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 440,999 | 5.512 | 20 | 20 | fits | 93,644 | 32 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 892,031 | 11.150 | 20 | 20 | fits | 25,396 | 12 | 0.800 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 286,315 | 3.579 | 20 | 20 | fits | 109,547 | 218 | 0.270 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 231,233 | 2.890 | 20 | 200 | fits | 115,125 | 180 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 340,164 | 4.252 | 20 | 200 | fits | 109,547 | 218 | 0.270 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 232,157 | 2.902 | 20 | 20 | fits | 115,125 | 180 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 340,868 | 4.261 | 20 | 20 | fits | 109,547 | 218 | 0.270 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 120,672 | 1.508 | 20 | 24 | fits | 118,046 | 142 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 234,807 | 2.935 | 20 | 24 | fits | 115,125 | 180 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 234,741 | 2.934 | 20 | 50 | fits | 115,125 | 180 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 343,892 | 4.299 | 20 | 50 | fits | 109,547 | 218 | 0.270 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 437,507 | 5.469 | 20 | 20 | fits | 93,681 | 33 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 887,162 | 11.090 | 20 | 20 | fits | 25,303 | 12 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 293,450 | 3.668 | 20 | 20 | fits | 108,891 | 219 | 0.258 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 228,189 | 2.852 | 20 | 200 | fits | 115,963 | 185 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 336,464 | 4.206 | 20 | 200 | fits | 108,891 | 219 | 0.258 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 229,113 | 2.864 | 20 | 20 | fits | 115,963 | 185 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 337,168 | 4.215 | 20 | 20 | fits | 108,891 | 219 | 0.258 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 116,790 | 1.460 | 20 | 24 | fits | 118,046 | 142 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 231,763 | 2.897 | 20 | 24 | fits | 115,963 | 185 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 231,697 | 2.896 | 20 | 50 | fits | 115,963 | 185 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 340,192 | 4.252 | 20 | 50 | fits | 108,891 | 219 | 0.258 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 438,683 | 5.484 | 20 | 20 | fits | 88,275 | 41 | 0.753 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 882,536 | 11.032 | 20 | 20 | fits | 48,886 | 20 | 0.708 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 311,631 | 3.895 | 20 | 20 | fits | 114,793 | 209 | 0.331 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 236,990 | 2.962 | 20 | 200 | fits | 119,701 | 204 | 0.360 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 361,009 | 4.513 | 20 | 200 | fits | 114,793 | 209 | 0.331 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 237,914 | 2.974 | 20 | 20 | fits | 119,701 | 204 | 0.360 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 361,713 | 4.521 | 20 | 20 | fits | 114,793 | 209 | 0.331 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 121,853 | 1.523 | 20 | 24 | fits | 118,046 | 142 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 240,564 | 3.007 | 20 | 24 | fits | 119,701 | 204 | 0.360 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 240,498 | 3.006 | 20 | 50 | fits | 119,701 | 204 | 0.360 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 364,737 | 4.559 | 20 | 50 | fits | 114,793 | 209 | 0.331 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 518,795 | 6.485 | 20 | 20 | fits | 93,748 | 33 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 905,543 | 11.319 | 20 | 20 | fits | 31,026 | 19 | 0.835 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 299,811 | 3.748 | 20 | 20 | fits | 117,398 | 207 | 0.293 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 238,507 | 2.981 | 20 | 200 | fits | 116,105 | 201 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 355,289 | 4.441 | 20 | 200 | fits | 117,398 | 207 | 0.293 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 239,431 | 2.993 | 20 | 20 | fits | 116,105 | 201 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 355,993 | 4.450 | 20 | 20 | fits | 117,398 | 207 | 0.293 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 118,245 | 1.478 | 20 | 24 | fits | 118,221 | 143 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 242,081 | 3.026 | 20 | 24 | fits | 116,105 | 201 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 242,015 | 3.025 | 20 | 50 | fits | 116,105 | 201 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 359,017 | 4.488 | 20 | 50 | fits | 117,398 | 207 | 0.293 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 512,801 | 6.410 | 20 | 20 | fits | 93,687 | 33 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 898,698 | 11.234 | 20 | 20 | fits | 25,357 | 12 | 0.803 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 355,990 | 4.450 | 20 | 20 | fits | 112,761 | 208 | 0.263 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 232,895 | 2.911 | 20 | 200 | fits | 118,407 | 197 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 405,047 | 5.063 | 20 | 200 | fits | 112,761 | 208 | 0.263 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 233,819 | 2.923 | 20 | 20 | fits | 118,407 | 197 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 405,751 | 5.072 | 20 | 20 | fits | 112,761 | 208 | 0.263 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 119,052 | 1.488 | 20 | 24 | fits | 117,971 | 142 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 236,469 | 2.956 | 20 | 24 | fits | 118,407 | 197 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 236,403 | 2.955 | 20 | 50 | fits | 118,407 | 197 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 408,775 | 5.110 | 20 | 50 | fits | 112,761 | 208 | 0.263 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 502,370 | 6.280 | 20 | 20 | fits | 93,661 | 32 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 892,583 | 11.157 | 20 | 20 | fits | 29,598 | 18 | 0.805 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 307,990 | 3.850 | 20 | 20 | fits | 109,972 | 203 | 0.328 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 238,149 | 2.977 | 20 | 200 | fits | 119,638 | 204 | 0.359 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 357,366 | 4.467 | 20 | 200 | fits | 109,972 | 203 | 0.328 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 239,073 | 2.988 | 20 | 20 | fits | 119,638 | 204 | 0.359 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 358,070 | 4.476 | 20 | 20 | fits | 109,972 | 203 | 0.328 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 123,075 | 1.538 | 20 | 24 | fits | 117,971 | 142 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 241,723 | 3.022 | 20 | 24 | fits | 119,638 | 204 | 0.359 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 241,657 | 3.021 | 20 | 50 | fits | 119,638 | 204 | 0.359 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 361,094 | 4.514 | 20 | 50 | fits | 109,972 | 203 | 0.328 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 454,581 | 5.682 | 20 | 20 | fits | 93,553 | 32 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 811,341 | 10.142 | 20 | 20 | fits | 83,774 | 32 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 295,023 | 3.688 | 20 | 20 | fits | 111,622 | 205 | 0.257 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 240,018 | 3.000 | 20 | 200 | fits | 116,108 | 201 | 0.374 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 351,024 | 4.388 | 20 | 200 | fits | 111,622 | 205 | 0.257 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 240,942 | 3.012 | 20 | 20 | fits | 116,108 | 201 | 0.374 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 351,728 | 4.397 | 20 | 20 | fits | 111,622 | 205 | 0.257 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 119,485 | 1.494 | 20 | 24 | fits | 118,164 | 143 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 243,592 | 3.045 | 20 | 24 | fits | 116,108 | 201 | 0.374 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 243,526 | 3.044 | 20 | 50 | fits | 116,108 | 201 | 0.374 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 354,752 | 4.434 | 20 | 50 | fits | 111,622 | 205 | 0.257 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 448,423 | 5.605 | 20 | 20 | fits | 93,737 | 32 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 839,608 | 10.495 | 20 | 20 | fits | 30,474 | 19 | 0.829 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 283,408 | 3.543 | 20 | 20 | fits | 109,506 | 218 | 0.269 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 228,366 | 2.855 | 20 | 200 | fits | 116,150 | 185 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 337,256 | 4.216 | 20 | 200 | fits | 109,506 | 218 | 0.269 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 229,290 | 2.866 | 20 | 20 | fits | 116,150 | 185 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 337,960 | 4.224 | 20 | 20 | fits | 109,506 | 218 | 0.269 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 116,780 | 1.460 | 20 | 24 | fits | 119,489 | 147 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 231,940 | 2.899 | 20 | 24 | fits | 116,150 | 185 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 231,874 | 2.898 | 20 | 50 | fits | 116,150 | 185 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 340,984 | 4.262 | 20 | 50 | fits | 109,506 | 218 | 0.269 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 434,515 | 5.431 | 20 | 20 | fits | 93,597 | 32 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 825,164 | 10.315 | 20 | 20 | fits | 25,325 | 12 | 0.800 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 283,286 | 3.541 | 20 | 20 | fits | 109,480 | 218 | 0.268 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 228,270 | 2.853 | 20 | 200 | fits | 115,950 | 185 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 337,134 | 4.214 | 20 | 200 | fits | 109,480 | 218 | 0.268 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 229,194 | 2.865 | 20 | 20 | fits | 115,950 | 185 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 337,838 | 4.223 | 20 | 20 | fits | 109,480 | 218 | 0.268 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 116,884 | 1.461 | 20 | 24 | fits | 118,140 | 142 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 231,844 | 2.898 | 20 | 24 | fits | 115,950 | 185 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 231,778 | 2.897 | 20 | 50 | fits | 115,950 | 185 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 340,862 | 4.261 | 20 | 50 | fits | 109,480 | 218 | 0.268 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 434,393 | 5.430 | 20 | 20 | fits | 93,597 | 32 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 825,280 | 10.316 | 20 | 20 | fits | 25,336 | 12 | 0.799 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 299,758 | 3.747 | 20 | 20 | fits | 105,931 | 199 | 0.266 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 236,096 | 2.951 | 20 | 200 | fits | 118,206 | 199 | 0.363 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 341,411 | 4.268 | 20 | 200 | fits | 105,931 | 199 | 0.266 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 237,020 | 2.963 | 20 | 20 | fits | 118,206 | 199 | 0.363 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 342,115 | 4.276 | 20 | 20 | fits | 105,931 | 199 | 0.266 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 122,454 | 1.531 | 20 | 24 | fits | 118,140 | 142 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 239,670 | 2.996 | 20 | 24 | fits | 118,206 | 199 | 0.363 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 239,604 | 2.995 | 20 | 50 | fits | 118,206 | 199 | 0.363 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 345,139 | 4.314 | 20 | 50 | fits | 105,931 | 199 | 0.266 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 438,703 | 5.484 | 20 | 20 | fits | 93,630 | 33 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 828,083 | 10.351 | 20 | 20 | fits | 25,303 | 12 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 289,440 | 3.618 | 20 | 20 | fits | 105,039 | 197 | 0.275 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 233,596 | 2.920 | 20 | 200 | fits | 119,489 | 203 | 0.359 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 338,019 | 4.225 | 20 | 200 | fits | 105,039 | 197 | 0.275 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 234,520 | 2.932 | 20 | 20 | fits | 119,489 | 203 | 0.359 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 338,723 | 4.234 | 20 | 20 | fits | 105,039 | 197 | 0.275 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 118,671 | 1.483 | 20 | 24 | fits | 118,140 | 142 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 237,170 | 2.965 | 20 | 24 | fits | 119,489 | 203 | 0.359 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 237,104 | 2.964 | 20 | 50 | fits | 119,489 | 203 | 0.359 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 341,747 | 4.272 | 20 | 50 | fits | 105,039 | 197 | 0.275 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 440,124 | 5.502 | 20 | 20 | fits | 88,161 | 41 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 822,445 | 10.281 | 20 | 20 | fits | 25,321 | 12 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 308,352 | 3.854 | 20 | 20 | fits | 118,735 | 227 | 0.331 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 234,288 | 2.929 | 20 | 200 | fits | 115,217 | 181 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 362,343 | 4.529 | 20 | 200 | fits | 118,735 | 227 | 0.331 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 235,212 | 2.940 | 20 | 20 | fits | 115,217 | 181 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 363,047 | 4.538 | 20 | 20 | fits | 118,735 | 227 | 0.331 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 123,635 | 1.545 | 20 | 24 | fits | 118,140 | 142 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 237,862 | 2.973 | 20 | 24 | fits | 115,217 | 181 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 237,796 | 2.972 | 20 | 50 | fits | 115,217 | 181 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 366,071 | 4.576 | 20 | 50 | fits | 118,735 | 227 | 0.331 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 459,463 | 5.743 | 20 | 20 | fits | 93,458 | 32 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 829,922 | 10.374 | 20 | 20 | fits | 25,303 | 12 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 310,092 | 3.876 | 20 | 20 | fits | 119,625 | 228 | 0.302 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 230,625 | 2.883 | 20 | 200 | fits | 115,337 | 179 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 359,637 | 4.495 | 20 | 200 | fits | 119,625 | 228 | 0.302 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 231,549 | 2.894 | 20 | 20 | fits | 115,337 | 179 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 360,341 | 4.504 | 20 | 20 | fits | 119,625 | 228 | 0.302 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 119,852 | 1.498 | 20 | 24 | fits | 118,140 | 142 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 234,199 | 2.927 | 20 | 24 | fits | 115,337 | 179 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 234,133 | 2.927 | 20 | 50 | fits | 115,337 | 179 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 363,365 | 4.542 | 20 | 50 | fits | 119,625 | 228 | 0.302 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 456,945 | 5.712 | 20 | 20 | fits | 93,646 | 32 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 813,643 | 10.171 | 20 | 20 | fits | 95,434 | 36 | 0.631 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 293,923 | 3.674 | 20 | 20 | fits | 104,980 | 196 | 0.275 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 238,793 | 2.985 | 20 | 200 | fits | 119,473 | 203 | 0.358 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 343,157 | 4.289 | 20 | 200 | fits | 104,980 | 196 | 0.275 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 239,717 | 2.996 | 20 | 20 | fits | 119,473 | 203 | 0.358 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 343,861 | 4.298 | 20 | 20 | fits | 104,980 | 196 | 0.275 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 123,884 | 1.549 | 20 | 24 | fits | 117,919 | 142 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 242,367 | 3.030 | 20 | 24 | fits | 119,473 | 203 | 0.358 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 242,301 | 3.029 | 20 | 50 | fits | 119,473 | 203 | 0.358 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 346,885 | 4.336 | 20 | 50 | fits | 104,980 | 196 | 0.275 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 440,484 | 5.506 | 20 | 20 | fits | 93,665 | 33 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 831,065 | 10.388 | 20 | 20 | fits | 29,510 | 18 | 0.803 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 285,715 | 3.571 | 20 | 20 | fits | 109,721 | 219 | 0.271 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 230,633 | 2.883 | 20 | 200 | fits | 115,096 | 180 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 339,738 | 4.247 | 20 | 200 | fits | 109,721 | 219 | 0.271 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 231,557 | 2.894 | 20 | 20 | fits | 115,096 | 180 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 340,442 | 4.256 | 20 | 20 | fits | 109,721 | 219 | 0.271 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 120,101 | 1.501 | 20 | 24 | fits | 117,919 | 142 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 234,207 | 2.928 | 20 | 24 | fits | 115,096 | 180 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 234,141 | 2.927 | 20 | 50 | fits | 115,096 | 180 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 343,466 | 4.293 | 20 | 50 | fits | 109,721 | 219 | 0.271 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 450,567 | 5.632 | 20 | 20 | fits | 96,885 | 39 | 0.737 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 907,675 | 11.346 | 20 | 20 | fits | 26,654 | 13 | 0.819 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 307,376 | 3.842 | 20 | 20 | fits | 114,092 | 224 | 0.317 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 227,878 | 2.848 | 20 | 200 | fits | 116,124 | 186 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 351,196 | 4.390 | 20 | 200 | fits | 114,092 | 224 | 0.317 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 228,802 | 2.860 | 20 | 20 | fits | 116,124 | 186 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 351,900 | 4.399 | 20 | 20 | fits | 114,092 | 224 | 0.317 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 116,318 | 1.454 | 20 | 24 | fits | 117,919 | 142 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 231,452 | 2.893 | 20 | 24 | fits | 116,124 | 186 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 231,386 | 2.892 | 20 | 50 | fits | 116,124 | 186 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 354,924 | 4.437 | 20 | 50 | fits | 114,092 | 224 | 0.317 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 448,476 | 5.606 | 20 | 20 | fits | 93,618 | 32 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 907,770 | 11.347 | 20 | 20 | fits | 39,984 | 23 | 0.739 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 297,439 | 3.718 | 20 | 20 | fits | 111,451 | 205 | 0.254 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 241,990 | 3.025 | 20 | 200 | fits | 116,037 | 201 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 352,825 | 4.410 | 20 | 200 | fits | 111,451 | 205 | 0.254 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 242,914 | 3.036 | 20 | 20 | fits | 116,037 | 201 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 353,529 | 4.419 | 20 | 20 | fits | 111,451 | 205 | 0.254 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 121,439 | 1.518 | 20 | 24 | fits | 118,076 | 143 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 245,564 | 3.070 | 20 | 24 | fits | 116,037 | 201 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 245,498 | 3.069 | 20 | 50 | fits | 116,037 | 201 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 356,553 | 4.457 | 20 | 50 | fits | 111,451 | 205 | 0.254 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 450,048 | 5.626 | 20 | 20 | fits | 93,561 | 32 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 922,429 | 11.530 | 20 | 20 | fits | 25,354 | 12 | 0.799 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 293,186 | 3.665 | 20 | 20 | fits | 104,987 | 196 | 0.275 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 237,342 | 2.967 | 20 | 200 | fits | 119,489 | 203 | 0.359 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 341,713 | 4.271 | 20 | 200 | fits | 104,987 | 196 | 0.275 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 238,266 | 2.978 | 20 | 20 | fits | 119,489 | 203 | 0.359 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 342,417 | 4.280 | 20 | 20 | fits | 104,987 | 196 | 0.275 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 122,417 | 1.530 | 20 | 24 | fits | 118,219 | 142 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 240,916 | 3.011 | 20 | 24 | fits | 119,489 | 203 | 0.359 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 240,850 | 3.011 | 20 | 50 | fits | 119,489 | 203 | 0.359 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 345,441 | 4.318 | 20 | 50 | fits | 104,987 | 196 | 0.275 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 438,973 | 5.487 | 20 | 20 | fits | 93,598 | 32 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 911,453 | 11.393 | 20 | 20 | fits | 37,133 | 16 | 0.746 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 288,608 | 3.608 | 20 | 20 | fits | 104,871 | 196 | 0.272 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 233,559 | 2.919 | 20 | 200 | fits | 119,489 | 203 | 0.359 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 337,814 | 4.223 | 20 | 200 | fits | 104,871 | 196 | 0.272 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 234,483 | 2.931 | 20 | 20 | fits | 119,489 | 203 | 0.359 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 338,518 | 4.231 | 20 | 20 | fits | 104,871 | 196 | 0.272 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 118,634 | 1.483 | 20 | 24 | fits | 118,219 | 142 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 237,133 | 2.964 | 20 | 24 | fits | 119,489 | 203 | 0.359 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 237,067 | 2.963 | 20 | 50 | fits | 119,489 | 203 | 0.359 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 341,542 | 4.269 | 20 | 50 | fits | 104,871 | 196 | 0.272 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 427,518 | 5.344 | 20 | 20 | fits | 86,042 | 34 | 0.754 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 908,416 | 11.355 | 20 | 20 | fits | 48,873 | 20 | 0.708 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 305,925 | 3.824 | 20 | 20 | fits | 115,062 | 222 | 0.296 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 234,146 | 2.927 | 20 | 200 | fits | 115,112 | 180 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 348,592 | 4.357 | 20 | 200 | fits | 115,062 | 222 | 0.296 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 235,070 | 2.938 | 20 | 20 | fits | 115,112 | 180 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 349,296 | 4.366 | 20 | 20 | fits | 115,062 | 222 | 0.296 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 123,598 | 1.545 | 20 | 24 | fits | 118,219 | 142 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 237,720 | 2.971 | 20 | 24 | fits | 115,112 | 180 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 237,654 | 2.971 | 20 | 50 | fits | 115,112 | 180 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 352,320 | 4.404 | 20 | 50 | fits | 115,062 | 222 | 0.296 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 518,107 | 6.476 | 20 | 20 | fits | 85,694 | 36 | 0.749 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 913,938 | 11.424 | 20 | 20 | fits | 48,886 | 20 | 0.708 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 387,053 | 4.838 | 20 | 20 | fits | 114,379 | 227 | 0.297 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 234,630 | 2.933 | 20 | 200 | fits | 119,379 | 181 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 428,468 | 5.356 | 20 | 200 | fits | 114,379 | 227 | 0.297 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 235,554 | 2.944 | 20 | 20 | fits | 119,379 | 181 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 429,172 | 5.365 | 20 | 20 | fits | 114,379 | 227 | 0.297 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 119,815 | 1.498 | 20 | 24 | fits | 118,219 | 142 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 238,204 | 2.978 | 20 | 24 | fits | 119,379 | 181 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 238,138 | 2.977 | 20 | 50 | fits | 119,379 | 181 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 432,196 | 5.402 | 20 | 50 | fits | 114,379 | 227 | 0.297 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 537,226 | 6.715 | 20 | 20 | fits | 94,655 | 33 | 0.738 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 912,719 | 11.409 | 20 | 20 | fits | 30,297 | 18 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 289,768 | 3.622 | 20 | 20 | fits | 104,871 | 196 | 0.272 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 234,719 | 2.934 | 20 | 200 | fits | 119,460 | 203 | 0.359 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 338,974 | 4.237 | 20 | 200 | fits | 104,871 | 196 | 0.272 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 235,643 | 2.946 | 20 | 20 | fits | 119,460 | 203 | 0.359 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 339,678 | 4.246 | 20 | 20 | fits | 104,871 | 196 | 0.272 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 119,823 | 1.498 | 20 | 24 | fits | 118,040 | 142 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 238,293 | 2.979 | 20 | 24 | fits | 119,460 | 203 | 0.359 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 238,227 | 2.978 | 20 | 50 | fits | 119,460 | 203 | 0.359 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 342,702 | 4.284 | 20 | 50 | fits | 104,871 | 196 | 0.272 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 436,256 | 5.453 | 20 | 20 | fits | 93,620 | 32 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 826,885 | 10.336 | 20 | 20 | fits | 29,510 | 18 | 0.803 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 283,923 | 3.549 | 20 | 20 | fits | 105,624 | 226 | 0.305 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 233,161 | 2.915 | 20 | 200 | fits | 118,104 | 209 | 0.347 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 338,169 | 4.227 | 20 | 200 | fits | 105,624 | 226 | 0.305 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 234,085 | 2.926 | 20 | 20 | fits | 118,104 | 209 | 0.347 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 338,873 | 4.236 | 20 | 20 | fits | 105,624 | 226 | 0.305 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 119,621 | 1.495 | 20 | 24 | fits | 121,621 | 111 | 0.346 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 236,735 | 2.959 | 20 | 24 | fits | 118,104 | 209 | 0.347 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 236,669 | 2.958 | 20 | 50 | fits | 118,104 | 209 | 0.347 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 341,897 | 4.274 | 20 | 50 | fits | 105,624 | 226 | 0.305 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 435,672 | 5.446 | 20 | 20 | fits | 93,841 | 33 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 826,507 | 10.331 | 20 | 20 | fits | 25,389 | 12 | 0.799 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 298,279 | 3.728 | 20 | 20 | fits | 106,105 | 200 | 0.268 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 234,617 | 2.933 | 20 | 200 | fits | 118,177 | 199 | 0.362 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 340,106 | 4.251 | 20 | 200 | fits | 106,105 | 200 | 0.268 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 235,541 | 2.944 | 20 | 20 | fits | 118,177 | 199 | 0.362 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 340,810 | 4.260 | 20 | 20 | fits | 106,105 | 200 | 0.268 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 121,004 | 1.513 | 20 | 24 | fits | 118,040 | 142 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 238,191 | 2.977 | 20 | 24 | fits | 118,177 | 199 | 0.362 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 238,125 | 2.977 | 20 | 50 | fits | 118,177 | 199 | 0.362 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 343,834 | 4.298 | 20 | 50 | fits | 106,105 | 200 | 0.268 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 450,770 | 5.635 | 20 | 20 | fits | 96,720 | 39 | 0.736 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 812,203 | 10.153 | 20 | 20 | fits | 95,447 | 36 | 0.631 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 296,668 | 3.708 | 20 | 20 | fits | 115,661 | 209 | 0.309 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 227,234 | 2.840 | 20 | 200 | fits | 115,014 | 202 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 352,301 | 4.404 | 20 | 200 | fits | 115,661 | 209 | 0.309 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 228,158 | 2.852 | 20 | 20 | fits | 115,014 | 202 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 353,005 | 4.413 | 20 | 20 | fits | 115,661 | 209 | 0.309 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 116,784 | 1.460 | 20 | 24 | fits | 118,040 | 142 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 230,808 | 2.885 | 20 | 24 | fits | 115,014 | 202 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 230,742 | 2.884 | 20 | 50 | fits | 115,014 | 202 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 356,029 | 4.450 | 20 | 50 | fits | 115,661 | 209 | 0.309 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 449,558 | 5.619 | 20 | 20 | fits | 93,595 | 32 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 811,204 | 10.140 | 20 | 20 | fits | 95,434 | 36 | 0.631 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 298,926 | 3.737 | 20 | 20 | fits | 109,569 | 218 | 0.268 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 243,970 | 3.050 | 20 | 200 | fits | 117,158 | 185 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 352,923 | 4.412 | 20 | 200 | fits | 109,569 | 218 | 0.268 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 244,894 | 3.061 | 20 | 20 | fits | 117,158 | 185 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 353,627 | 4.420 | 20 | 20 | fits | 109,569 | 218 | 0.268 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 122,277 | 1.528 | 20 | 24 | fits | 118,132 | 143 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 247,544 | 3.094 | 20 | 24 | fits | 117,158 | 185 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 247,478 | 3.093 | 20 | 50 | fits | 117,158 | 185 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 356,651 | 4.458 | 20 | 50 | fits | 109,569 | 218 | 0.268 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 442,708 | 5.534 | 20 | 20 | fits | 86,123 | 34 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 841,163 | 10.515 | 20 | 20 | fits | 30,571 | 19 | 0.831 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 305,293 | 3.816 | 20 | 20 | fits | 108,773 | 218 | 0.256 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 240,188 | 3.002 | 20 | 200 | fits | 117,158 | 185 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 348,345 | 4.354 | 20 | 200 | fits | 108,773 | 218 | 0.256 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 241,112 | 3.014 | 20 | 20 | fits | 117,158 | 185 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 349,049 | 4.363 | 20 | 20 | fits | 108,773 | 218 | 0.256 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 118,514 | 1.481 | 20 | 24 | fits | 118,152 | 143 | 0.339 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 243,762 | 3.047 | 20 | 24 | fits | 117,158 | 185 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 243,696 | 3.046 | 20 | 50 | fits | 117,158 | 185 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 352,073 | 4.401 | 20 | 50 | fits | 108,773 | 218 | 0.256 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 438,042 | 5.476 | 20 | 20 | fits | 86,035 | 34 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 836,352 | 10.454 | 20 | 20 | fits | 30,584 | 19 | 0.831 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 302,283 | 3.779 | 20 | 20 | fits | 115,064 | 222 | 0.296 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 230,504 | 2.881 | 20 | 200 | fits | 115,125 | 180 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 344,952 | 4.312 | 20 | 200 | fits | 115,064 | 222 | 0.296 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 231,428 | 2.893 | 20 | 20 | fits | 115,125 | 180 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 345,656 | 4.321 | 20 | 20 | fits | 115,064 | 222 | 0.296 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 119,943 | 1.499 | 20 | 24 | fits | 117,967 | 142 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 234,078 | 2.926 | 20 | 24 | fits | 115,125 | 180 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 234,012 | 2.925 | 20 | 50 | fits | 115,125 | 180 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 348,680 | 4.359 | 20 | 50 | fits | 115,064 | 222 | 0.296 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 442,060 | 5.526 | 20 | 20 | fits | 93,446 | 32 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 814,803 | 10.185 | 20 | 20 | fits | 95,293 | 36 | 0.632 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 300,640 | 3.758 | 20 | 20 | fits | 112,588 | 205 | 0.301 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 230,653 | 2.883 | 20 | 200 | fits | 119,057 | 204 | 0.360 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 342,625 | 4.283 | 20 | 200 | fits | 112,588 | 205 | 0.301 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 231,577 | 2.895 | 20 | 20 | fits | 119,057 | 204 | 0.360 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 343,329 | 4.292 | 20 | 20 | fits | 112,588 | 205 | 0.301 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 116,160 | 1.452 | 20 | 24 | fits | 117,967 | 142 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 234,227 | 2.928 | 20 | 24 | fits | 119,057 | 204 | 0.360 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 234,161 | 2.927 | 20 | 50 | fits | 119,057 | 204 | 0.360 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 346,353 | 4.329 | 20 | 50 | fits | 112,588 | 205 | 0.301 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 439,774 | 5.497 | 20 | 20 | fits | 93,487 | 32 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 826,045 | 10.326 | 20 | 20 | fits | 25,303 | 12 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 302,154 | 3.777 | 20 | 20 | fits | 109,885 | 202 | 0.329 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 232,354 | 2.904 | 20 | 200 | fits | 120,343 | 209 | 0.356 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 351,559 | 4.394 | 20 | 200 | fits | 109,885 | 202 | 0.329 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 233,278 | 2.916 | 20 | 20 | fits | 120,343 | 209 | 0.356 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 352,263 | 4.403 | 20 | 20 | fits | 109,885 | 202 | 0.329 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 116,575 | 1.457 | 20 | 24 | fits | 118,119 | 142 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 235,928 | 2.949 | 20 | 24 | fits | 120,343 | 209 | 0.356 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 235,862 | 2.948 | 20 | 50 | fits | 120,343 | 209 | 0.356 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 355,287 | 4.441 | 20 | 50 | fits | 109,885 | 202 | 0.329 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 448,680 | 5.609 | 20 | 20 | fits | 93,459 | 32 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 805,309 | 10.066 | 20 | 20 | fits | 95,434 | 36 | 0.631 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 298,302 | 3.729 | 20 | 20 | fits | 109,511 | 218 | 0.267 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 243,346 | 3.042 | 20 | 200 | fits | 117,098 | 185 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 352,241 | 4.403 | 20 | 200 | fits | 109,511 | 218 | 0.267 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 244,270 | 3.053 | 20 | 20 | fits | 117,098 | 185 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 352,945 | 4.412 | 20 | 20 | fits | 109,511 | 218 | 0.267 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 121,732 | 1.522 | 20 | 24 | fits | 118,312 | 143 | 0.339 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 246,920 | 3.087 | 20 | 24 | fits | 117,098 | 185 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 246,854 | 3.086 | 20 | 50 | fits | 117,098 | 185 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 355,969 | 4.450 | 20 | 50 | fits | 109,511 | 218 | 0.267 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 449,525 | 5.619 | 20 | 20 | fits | 93,622 | 32 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 901,342 | 11.267 | 20 | 20 | fits | 30,892 | 19 | 0.834 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 304,331 | 3.804 | 20 | 20 | fits | 108,862 | 218 | 0.260 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 238,989 | 2.987 | 20 | 200 | fits | 115,334 | 180 | 0.376 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 347,235 | 4.340 | 20 | 200 | fits | 108,862 | 218 | 0.260 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 239,913 | 2.999 | 20 | 20 | fits | 115,334 | 180 | 0.376 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 347,939 | 4.349 | 20 | 20 | fits | 108,862 | 218 | 0.260 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 128,219 | 1.603 | 20 | 24 | fits | 118,380 | 143 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 242,563 | 3.032 | 20 | 24 | fits | 115,334 | 180 | 0.376 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 242,497 | 3.031 | 20 | 50 | fits | 115,334 | 180 | 0.376 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 350,963 | 4.387 | 20 | 50 | fits | 108,862 | 218 | 0.260 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 444,460 | 5.556 | 20 | 20 | fits | 93,563 | 32 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 895,668 | 11.196 | 20 | 20 | fits | 25,543 | 12 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 294,857 | 3.686 | 20 | 20 | fits | 108,781 | 218 | 0.258 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 229,596 | 2.870 | 20 | 200 | fits | 115,065 | 180 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 337,761 | 4.222 | 20 | 200 | fits | 108,781 | 218 | 0.258 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 230,520 | 2.881 | 20 | 20 | fits | 115,065 | 180 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 338,465 | 4.231 | 20 | 20 | fits | 108,781 | 218 | 0.258 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 119,095 | 1.489 | 20 | 24 | fits | 117,967 | 142 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 233,170 | 2.915 | 20 | 24 | fits | 115,065 | 180 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 233,104 | 2.914 | 20 | 50 | fits | 115,065 | 180 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 341,489 | 4.269 | 20 | 50 | fits | 108,781 | 218 | 0.258 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 434,934 | 5.437 | 20 | 20 | fits | 93,511 | 32 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 885,954 | 11.074 | 20 | 20 | fits | 25,349 | 12 | 0.799 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 294,862 | 3.686 | 20 | 20 | fits | 105,011 | 196 | 0.276 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 238,937 | 2.987 | 20 | 200 | fits | 119,442 | 203 | 0.358 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 343,332 | 4.292 | 20 | 200 | fits | 105,011 | 196 | 0.276 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 239,861 | 2.998 | 20 | 20 | fits | 119,442 | 203 | 0.358 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 344,036 | 4.300 | 20 | 20 | fits | 105,011 | 196 | 0.276 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 124,059 | 1.551 | 20 | 24 | fits | 117,967 | 142 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 242,511 | 3.031 | 20 | 24 | fits | 119,442 | 203 | 0.358 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 242,445 | 3.031 | 20 | 50 | fits | 119,442 | 203 | 0.358 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 347,060 | 4.338 | 20 | 50 | fits | 105,011 | 196 | 0.276 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 440,556 | 5.507 | 20 | 20 | fits | 93,562 | 33 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 876,280 | 10.954 | 20 | 20 | fits | 95,434 | 36 | 0.631 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 290,284 | 3.629 | 20 | 20 | fits | 105,026 | 197 | 0.275 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 235,154 | 2.939 | 20 | 200 | fits | 119,442 | 203 | 0.358 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 339,564 | 4.245 | 20 | 200 | fits | 105,026 | 197 | 0.275 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 236,078 | 2.951 | 20 | 20 | fits | 119,442 | 203 | 0.358 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 340,268 | 4.253 | 20 | 20 | fits | 105,026 | 197 | 0.275 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 120,276 | 1.503 | 20 | 24 | fits | 117,967 | 142 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 238,728 | 2.984 | 20 | 24 | fits | 119,442 | 203 | 0.358 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 238,662 | 2.983 | 20 | 50 | fits | 119,442 | 203 | 0.358 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 343,292 | 4.291 | 20 | 50 | fits | 105,026 | 197 | 0.275 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 441,652 | 5.521 | 20 | 20 | fits | 88,144 | 41 | 0.751 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 884,704 | 11.059 | 20 | 20 | fits | 25,303 | 12 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 291,586 | 3.645 | 20 | 20 | fits | 117,526 | 227 | 0.308 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 227,832 | 2.848 | 20 | 200 | fits | 115,903 | 185 | 0.369 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 344,742 | 4.309 | 20 | 200 | fits | 117,526 | 227 | 0.308 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 228,756 | 2.859 | 20 | 20 | fits | 115,903 | 185 | 0.369 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 345,446 | 4.318 | 20 | 20 | fits | 117,526 | 227 | 0.308 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 116,493 | 1.456 | 20 | 24 | fits | 117,967 | 142 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 231,406 | 2.893 | 20 | 24 | fits | 115,903 | 185 | 0.369 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 231,340 | 2.892 | 20 | 50 | fits | 115,903 | 185 | 0.369 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 348,470 | 4.356 | 20 | 50 | fits | 117,526 | 227 | 0.308 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 513,779 | 6.422 | 20 | 20 | fits | 95,034 | 33 | 0.742 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 884,357 | 11.054 | 20 | 20 | fits | 25,358 | 12 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 378,316 | 4.729 | 20 | 20 | fits | 114,986 | 226 | 0.318 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 236,269 | 2.953 | 20 | 200 | fits | 119,376 | 182 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 420,264 | 5.253 | 20 | 200 | fits | 114,986 | 226 | 0.318 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 237,193 | 2.965 | 20 | 20 | fits | 119,376 | 182 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 420,968 | 5.262 | 20 | 20 | fits | 114,986 | 226 | 0.318 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 121,457 | 1.518 | 20 | 24 | fits | 117,967 | 142 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 239,843 | 2.998 | 20 | 24 | fits | 119,376 | 182 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 239,777 | 2.997 | 20 | 50 | fits | 119,376 | 182 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 423,992 | 5.300 | 20 | 50 | fits | 114,986 | 226 | 0.318 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 517,269 | 6.466 | 20 | 20 | fits | 93,343 | 32 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 892,605 | 11.158 | 20 | 20 | fits | 30,165 | 18 | 0.816 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 291,604 | 3.645 | 20 | 20 | fits | 104,916 | 196 | 0.274 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 236,474 | 2.956 | 20 | 200 | fits | 119,413 | 203 | 0.357 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 340,774 | 4.260 | 20 | 200 | fits | 104,916 | 196 | 0.274 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 237,398 | 2.967 | 20 | 20 | fits | 119,413 | 203 | 0.357 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 341,478 | 4.268 | 20 | 20 | fits | 104,916 | 196 | 0.274 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 121,625 | 1.520 | 20 | 24 | fits | 118,050 | 142 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 240,048 | 3.001 | 20 | 24 | fits | 119,413 | 203 | 0.357 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 239,982 | 3.000 | 20 | 50 | fits | 119,413 | 203 | 0.357 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 344,502 | 4.306 | 20 | 50 | fits | 104,916 | 196 | 0.274 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 438,098 | 5.476 | 20 | 20 | fits | 93,662 | 33 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 828,811 | 10.360 | 20 | 20 | fits | 29,510 | 18 | 0.803 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 283,186 | 3.540 | 20 | 20 | fits | 109,657 | 219 | 0.270 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 228,104 | 2.851 | 20 | 200 | fits | 115,874 | 185 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 337,145 | 4.214 | 20 | 200 | fits | 109,657 | 219 | 0.270 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 229,028 | 2.863 | 20 | 20 | fits | 115,874 | 185 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 337,849 | 4.223 | 20 | 20 | fits | 109,657 | 219 | 0.270 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 116,794 | 1.460 | 20 | 24 | fits | 118,050 | 142 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 231,678 | 2.896 | 20 | 24 | fits | 115,874 | 185 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 231,612 | 2.895 | 20 | 50 | fits | 115,874 | 185 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 340,873 | 4.261 | 20 | 50 | fits | 109,657 | 219 | 0.270 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 447,932 | 5.599 | 20 | 20 | fits | 96,843 | 39 | 0.737 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 823,161 | 10.290 | 20 | 20 | fits | 25,303 | 12 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 313,964 | 3.925 | 20 | 20 | fits | 110,688 | 206 | 0.317 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 236,610 | 2.958 | 20 | 200 | fits | 118,368 | 200 | 0.363 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 356,524 | 4.457 | 20 | 200 | fits | 110,688 | 206 | 0.317 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 237,534 | 2.969 | 20 | 20 | fits | 118,368 | 200 | 0.363 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 357,228 | 4.465 | 20 | 20 | fits | 110,688 | 206 | 0.317 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 122,806 | 1.535 | 20 | 24 | fits | 118,050 | 142 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 240,184 | 3.002 | 20 | 24 | fits | 118,368 | 200 | 0.363 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 240,118 | 3.001 | 20 | 50 | fits | 118,368 | 200 | 0.363 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 360,252 | 4.503 | 20 | 50 | fits | 110,688 | 206 | 0.317 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 453,774 | 5.672 | 20 | 20 | fits | 93,588 | 32 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 828,775 | 10.360 | 20 | 20 | fits | 25,303 | 12 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 295,159 | 3.689 | 20 | 20 | fits | 111,393 | 205 | 0.253 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 239,710 | 2.996 | 20 | 200 | fits | 116,016 | 201 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 350,487 | 4.381 | 20 | 200 | fits | 111,393 | 205 | 0.253 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 240,634 | 3.008 | 20 | 20 | fits | 116,016 | 201 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 351,191 | 4.390 | 20 | 20 | fits | 111,393 | 205 | 0.253 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 119,180 | 1.490 | 20 | 24 | fits | 118,207 | 143 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 243,284 | 3.041 | 20 | 24 | fits | 116,016 | 201 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 243,218 | 3.040 | 20 | 50 | fits | 116,016 | 201 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 354,215 | 4.428 | 20 | 50 | fits | 111,393 | 205 | 0.253 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 447,668 | 5.596 | 20 | 20 | fits | 93,519 | 32 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 838,897 | 10.486 | 20 | 20 | fits | 25,329 | 12 | 0.801 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 290,909 | 3.636 | 20 | 20 | fits | 104,929 | 196 | 0.274 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 235,065 | 2.938 | 20 | 200 | fits | 119,429 | 203 | 0.359 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 339,378 | 4.242 | 20 | 200 | fits | 104,929 | 196 | 0.274 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 235,989 | 2.950 | 20 | 20 | fits | 119,429 | 203 | 0.359 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 340,082 | 4.251 | 20 | 20 | fits | 104,929 | 196 | 0.274 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 120,200 | 1.502 | 20 | 24 | fits | 118,167 | 142 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 238,639 | 2.983 | 20 | 24 | fits | 119,429 | 203 | 0.359 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 238,573 | 2.982 | 20 | 50 | fits | 119,429 | 203 | 0.359 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 343,106 | 4.289 | 20 | 50 | fits | 104,929 | 196 | 0.274 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 436,557 | 5.457 | 20 | 20 | fits | 93,517 | 32 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 827,128 | 10.339 | 20 | 20 | fits | 25,354 | 12 | 0.799 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 287,169 | 3.590 | 20 | 20 | fits | 104,807 | 196 | 0.271 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 232,120 | 2.901 | 20 | 200 | fits | 120,267 | 208 | 0.357 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 336,311 | 4.204 | 20 | 200 | fits | 104,807 | 196 | 0.271 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 233,044 | 2.913 | 20 | 20 | fits | 120,267 | 208 | 0.357 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 337,015 | 4.213 | 20 | 20 | fits | 104,807 | 196 | 0.271 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 116,417 | 1.455 | 20 | 24 | fits | 118,167 | 142 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 235,694 | 2.946 | 20 | 24 | fits | 120,267 | 208 | 0.357 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 235,628 | 2.945 | 20 | 50 | fits | 120,267 | 208 | 0.357 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 340,039 | 4.250 | 20 | 50 | fits | 104,807 | 196 | 0.271 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 425,934 | 5.324 | 20 | 20 | fits | 85,961 | 34 | 0.753 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 824,497 | 10.306 | 20 | 20 | fits | 25,303 | 12 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 303,582 | 3.795 | 20 | 20 | fits | 114,932 | 222 | 0.295 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 231,869 | 2.898 | 20 | 200 | fits | 115,052 | 180 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 346,185 | 4.327 | 20 | 200 | fits | 114,932 | 222 | 0.295 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 232,793 | 2.910 | 20 | 20 | fits | 115,052 | 180 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 346,889 | 4.336 | 20 | 20 | fits | 114,932 | 222 | 0.295 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 121,381 | 1.517 | 20 | 24 | fits | 118,167 | 142 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 235,443 | 2.943 | 20 | 24 | fits | 115,052 | 180 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 235,377 | 2.942 | 20 | 50 | fits | 115,052 | 180 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 349,913 | 4.374 | 20 | 50 | fits | 114,932 | 222 | 0.295 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 443,295 | 5.541 | 20 | 20 | fits | 93,448 | 33 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 829,096 | 10.364 | 20 | 20 | fits | 25,316 | 12 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 301,228 | 3.765 | 20 | 20 | fits | 112,551 | 206 | 0.300 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 231,322 | 2.892 | 20 | 200 | fits | 118,975 | 204 | 0.360 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 343,257 | 4.291 | 20 | 200 | fits | 112,551 | 206 | 0.300 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 232,246 | 2.903 | 20 | 20 | fits | 118,975 | 204 | 0.360 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 343,961 | 4.300 | 20 | 20 | fits | 112,551 | 206 | 0.300 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 116,911 | 1.461 | 20 | 24 | fits | 118,167 | 142 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 234,896 | 2.936 | 20 | 24 | fits | 118,975 | 204 | 0.360 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 234,830 | 2.935 | 20 | 50 | fits | 118,975 | 204 | 0.360 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 346,985 | 4.337 | 20 | 50 | fits | 112,551 | 206 | 0.300 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 453,856 | 5.673 | 20 | 20 | fits | 96,655 | 39 | 0.736 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 810,474 | 10.131 | 20 | 20 | fits | 95,447 | 36 | 0.631 |
| Talker Advertise RX for every input, bound | `srp.bound_advertise.if0` | 61,943 | 0.774 | 20 | 20 | fits | 62,009 | 15 | 0.911 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 12,448 | 0.156 | 20 | 20 | fits | 22,992 | 21 (35) | 0.805 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 12,426 | 0.155 | 20 | 20 | fits | 19,377 | 17 (14) | 0.842 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 12,757 | 0.159 | 20 | 20 | fits | 18,023 | 18 (14) | 0.817 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 15,708 | 0.196 | 20 | 20 | fits | 21,820 | 21 (35) | 0.787 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 122,510 | 1.531 | 20 | 200 | fits | 123,450 | 221 | 0.399 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 299,331 | 3.742 | 20 | 20 | fits | 91,924 | 39 | 0.652 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 250,076 | 3.126 | 20 | 24 | fits | 57,669 | 54 | 0.396 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 175,932 | 2.199 | 20 | 50 | fits | 117,715 | 250 | 0.210 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 752,861 | 9.411 | 20 | 20 | fits | 36,642 | 16 | 0.743 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 211,399 | 2.642 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 122,510 | 1.531 | 20 | 200 | fits | 123,450 | 221 | 0.399 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 280,147 | 3.502 | 20 | 20 | fits | 89,755 | 50 | 0.624 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 270,814 | 3.385 | 20 | 24 | fits | 88,253 | 68 | 0.503 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 158,917 | 1.986 | 20 | 50 | fits | 112,903 | 249 | 0.235 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 765,870 | 9.573 | 20 | 20 | fits | 61,705 | 30 | 0.678 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 198,161 | 2.477 | 49 | 49 | fits | 0 | - | 0.000 |
| LINK_UP | `adp.link_up.if0` | 2,890 | 0.036 | 20 | 200 | fits | 19,889 | 44 (12) | 0.673 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 6,368 | 0.080 | 20 | 200 | fits | 14,117 | 23 (39) | 0.607 |
| LINK_DOWN | `adp.link_down.if0` | 1,699 | 0.021 | 20 | 200 | fits | 18,048 | 23 (9) | 0.671 |
| LINK_UP | `adp.link_up.if0` | 2,890 | 0.036 | 20 | 200 | fits | 19,889 | 44 (12) | 0.673 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 6,368 | 0.080 | 20 | 200 | fits | 14,117 | 23 (39) | 0.607 |
| GM_CHANGE | `adp.gm_change.if0` | 1,828 | 0.023 | 20 | 200 | fits | 8,991 | 17 (11) | 0.344 |
| LINK_UP | `adp.link_up.if0` | 2,890 | 0.036 | 20 | 200 | fits | 19,889 | 44 (12) | 0.673 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 6,368 | 0.080 | 20 | 200 | fits | 14,117 | 23 (39) | 0.607 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,187 | 0.052 | 20 | 200 | fits | 10,520 | 16 (31) | 0.525 |
| LINK_UP | `adp.link_up.if0` | 2,890 | 0.036 | 20 | 200 | fits | 19,889 | 44 (12) | 0.673 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 6,368 | 0.080 | 20 | 200 | fits | 14,117 | 23 (39) | 0.607 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,187 | 0.052 | 20 | 200 | fits | 10,520 | 16 (31) | 0.525 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 67,813 | 0.848 | 20 | 20 | fits | 54,957 | 6 | 0.881 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 33,393 | 0.417 | 20 | 20 | fits | 33,459 | 12 | 0.873 |
| malformed MRPDU discard | `srp.malformed.if0` | 13,303 | 0.166 | 20 | 20 | fits | 13,369 | 12 | 0.649 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 64,870 | 0.811 | 220 | 220 | fits | 74,298 | 9 | 0.862 |
| an event behind 15 others | `backlog.event.if0` | 128,452 | 1.606 | 20 | 200 | fits | 40,676 | 79 | 0.503 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 343,659 | 4.296 | 20 | 20 | fits | 44,062 | 81 | 0.193 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 328,593 | 4.107 | 20 | 200 | fits | 117,656 | 148 | 0.306 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 327,977 | 4.100 | 20 | 200 | fits | 117,656 | 148 | 0.306 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 324,271 | 4.053 | 20 | 20 | fits | 117,656 | 148 | 0.306 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 367,497 | 4.594 | 20 | 20 | fits | 44,062 | 81 | 0.193 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 118,946 | 1.487 | 20 | 24 | fits | 119,822 | 148 | 0.355 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 326,921 | 4.087 | 20 | 24 | fits | 117,656 | 148 | 0.306 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 326,855 | 4.086 | 20 | 50 | fits | 117,656 | 148 | 0.306 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 326,459 | 4.081 | 20 | 50 | fits | 117,656 | 148 | 0.306 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 370,455 | 4.631 | 20 | 20 | fits | 44,062 | 81 | 0.193 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 409,536 | 5.119 | 20 | 20 | fits | 17,223 | 40 | 0.093 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 288,232 | 3.603 | 20 | 20 | fits | 104,592 | 197 | 0.272 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 233,432 | 2.918 | 20 | 200 | fits | 119,108 | 203 | 0.357 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 337,408 | 4.218 | 20 | 200 | fits | 104,592 | 197 | 0.272 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 234,356 | 2.929 | 20 | 20 | fits | 119,108 | 203 | 0.357 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 338,112 | 4.226 | 20 | 20 | fits | 104,592 | 197 | 0.272 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 118,888 | 1.486 | 20 | 24 | fits | 119,059 | 145 | 0.342 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 237,006 | 2.963 | 20 | 24 | fits | 119,108 | 203 | 0.357 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 236,940 | 2.962 | 20 | 50 | fits | 119,108 | 203 | 0.357 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 341,136 | 4.264 | 20 | 50 | fits | 104,592 | 197 | 0.272 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 448,100 | 5.601 | 20 | 20 | fits | 96,689 | 39 | 0.737 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 822,855 | 10.286 | 20 | 20 | fits | 25,298 | 12 | 0.797 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 13,215 | 0.165 | 20 | 20 | fits | 20,962 | 19 | 0.797 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 233,432 | 2.918 | 20 | 200 | fits | 119,108 | 203 | 0.357 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 26,911 | 0.336 | 20 | 200 | fits | 20,962 | 19 | 0.797 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 234,356 | 2.929 | 20 | 20 | fits | 119,108 | 203 | 0.357 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 327,705 | 4.096 | 20 | 20 | fits | 94,185 | 187 | 0.185 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 118,888 | 1.486 | 20 | 24 | fits | 119,059 | 145 | 0.342 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 237,006 | 2.963 | 20 | 24 | fits | 119,108 | 203 | 0.357 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 236,940 | 2.962 | 20 | 50 | fits | 119,108 | 203 | 0.357 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 330,729 | 4.134 | 20 | 50 | fits | 94,185 | 187 | 0.185 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 437,441 | 5.468 | 20 | 20 | fits | 96,441 | 39 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 812,207 | 10.153 | 20 | 20 | fits | 25,298 | 12 | 0.797 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 5,017,585 | 62.720 | 20 | 20 | MISS ceiling | 11,455 | 13 | 0.442 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 5,028,977 | 62.862 | 20 | 20 | MISS ceiling | 11,468 | 13 | 0.442 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 5,040,293 | 63.004 | 20 | 20 | MISS ceiling | 11,373 | 13 | 0.460 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 5,051,599 | 63.145 | 20 | 20 | MISS ceiling | 11,382 | 13 | 0.451 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 5,062,889 | 63.286 | 20 | 20 | MISS ceiling | 11,353 | 13 | 0.451 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 117,160 | 1.464 | 20 | 200 | fits | 116,354 | 196 | 0.397 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 221,117 | 2.764 | 20 | 200 | fits | 104,573 | 192 | 0.414 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 112,838 | 1.410 | 20 | 20 | fits | 116,354 | 196 | 0.397 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 4,959,422 | 61.993 | 20 | 20 | MISS ceiling | 116,720 | 107 | 0.373 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 116,478 | 1.456 | 20 | 24 | fits | 116,354 | 196 | 0.397 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 4,962,908 | 62.036 | 20 | 24 | MISS ceiling | 116,720 | 107 | 0.373 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 115,422 | 1.443 | 20 | 50 | fits | 116,354 | 196 | 0.397 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 219,599 | 2.745 | 20 | 50 | fits | 104,573 | 192 | 0.414 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 219,533 | 2.744 | 20 | 20 | fits | 104,573 | 192 | 0.414 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 648,574 | 8.107 | 20 | 20 | fits | 70,974 | 28 | 0.644 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,131 | 0.064 | 20 | 20 | fits | 16,893 | 13 (29) | 0.725 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,411 | 0.093 | 20 | 20 | fits | 20,856 | 19 (35) | 0.791 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 9,007 | 0.113 | 20 | 20 | fits | 21,771 | 21 (12) | 0.787 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 10,041 | 0.126 | 20 | 50 | fits | 19,889 | 44 | 0.673 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 12,538 | 0.157 | 20 | 50 | fits | 15,646 | 35 | 0.621 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 11,206 | 0.140 | 20 | 50 | fits | 15,628 | 35 | 0.625 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 7,582 | 0.095 | 20 | 50 | fits | 20,678 | 61 | 0.570 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 9,532 | 0.119 | 20 | 50 | fits | 20,678 | 61 | 0.570 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 7,637 | 0.095 | 20 | 50 | fits | 15,091 | 30 | 0.587 |
| set_name | `aecp_fanout.set_name.if0` | 40,791 | 0.510 | 20 | 24 | fits | 50,654 | 89 | 0.562 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 40,757 | 0.509 | 20 | 24 | fits | 46,572 | 79 | 0.602 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 34,935 | 0.437 | 20 | 24 | fits | 39,879 | 78 | 0.543 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 34,822 | 0.435 | 20 | 24 | fits | 39,644 | 79 | 0.538 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 51,800 | 0.647 | 20 | 24 | fits | 58,847 | 109 | 0.591 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 287,196 | 3.590 | 20 | 24 | fits | 53,824 | 110 | 0.576 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 345,635 | 4.320 | 20 | 24 | fits | 44,095 | 66 | 0.600 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 34,692 | 0.434 | 20 | 24 | fits | 39,957 | 79 | 0.545 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 38,446 | 0.481 | 20 | 24 | fits | 40,156 | 78 | 0.552 |
| BIND_RX | `acmp.bind_rx.if0` | 16,805 | 0.210 | 20 | 20 | fits | 33,704 | 26 (77) | 0.772 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 8,936 | 0.112 | 20 | 20 | fits | 23,412 | 19 (32) | 0.814 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 8,744 | 0.109 | 20 | 20 | fits | 18,273 | 15 (47) | 0.704 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 11,311 | 0.141 | 20 | 20 | fits | 30,157 | 19 (50) | 0.796 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 9,507 | 0.119 | 20 | 20 | fits | 19,412 | 17 (48) | 0.727 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 8,542 | 0.107 | 20 | 20 | fits | 17,614 | 16 (48) | 0.645 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 8,090 | 0.101 | 20 | 20 | fits | 16,688 | 16 (48) | 0.620 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 8,092 | 0.101 | 20 | 20 | fits | 16,589 | 16 (48) | 0.612 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 13,125 | 0.164 | 20 | 24 | fits | 20,629 | 20 | 0.752 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 14,100 | 0.176 | 20 | 24 | fits | 23,733 | 20 | 0.672 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 9,320 | 0.117 | 20 | 24 | fits | 20,573 | 20 | 0.706 |
| READ_DESCRIPTOR (156 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 11,390 | 0.142 | 20 | 24 | fits | 20,310 | 20 | 0.690 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 9,415 | 0.118 | 20 | 24 | fits | 20,664 | 20 | 0.697 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i0.c0.if0` | 11,056 | 0.138 | 20 | 24 | fits | 19,923 | 20 | 0.699 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 8,929 | 0.112 | 20 | 24 | fits | 20,343 | 20 | 0.704 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 8,494 | 0.106 | 20 | 24 | fits | 19,569 | 20 | 0.718 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 10,814 | 0.135 | 20 | 24 | fits | 19,754 | 20 | 0.722 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 13,346 | 0.167 | 20 | 24 | fits | 24,595 | 21 | 0.617 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 10,283 | 0.129 | 20 | 24 | fits | 19,139 | 20 | 0.737 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 7,626 | 0.095 | 20 | 24 | fits | 18,796 | 20 | 0.731 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i15.c0.if0` | 10,672 | 0.133 | 20 | 24 | fits | 19,686 | 20 | 0.711 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t23.i0.c0.if0` | 8,553 | 0.107 | 20 | 24 | fits | 19,644 | 20 | 0.716 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 11,624 | 0.145 | 20 | 24 | fits | 20,559 | 20 | 0.708 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 10,805 | 0.135 | 20 | 24 | fits | 19,754 | 20 | 0.720 |
| get_configuration | `aecp.get_configuration.if0` | 6,674 | 0.083 | 20 | 24 | fits | 17,479 | 20 | 0.713 |
| entity_available | `aecp.entity_available.if0` | 8,633 | 0.108 | 20 | 24 | fits | 17,265 | 20 | 0.705 |
| get_name | `aecp.get_name.if0` | 8,862 | 0.111 | 20 | 24 | fits | 19,755 | 20 | 0.727 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 12,655 | 0.158 | 20 | 24 | fits | 21,522 | 26 | 0.706 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 9,319 | 0.116 | 20 | 24 | fits | 20,404 | 29 | 0.716 |
| get_as_path, refused ENTITY_MISBEHAVING | `aecp.get_as_path.if0` | 11,608 | 0.145 | 20 | 24 | fits | 19,837 | 28 | 0.725 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 6,712 | 0.084 | 20 | 24 | fits | 17,675 | 20 | 0.723 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 8,988 | 0.112 | 20 | 24 | fits | 17,078 | 20 | 0.705 |
| set_name | `aecp.set_name.if0` | 17,328 | 0.217 | 20 | 24 | fits | 36,889 | 44 | 0.755 |
| lock_entity | `aecp.lock_entity.if0` | 11,896 | 0.149 | 20 | 24 | fits | 27,407 | 33 | 0.769 |
| unlock_entity | `aecp.unlock_entity.if0` | 16,838 | 0.210 | 20 | 24 | fits | 27,897 | 33 | 0.780 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 142,702 | 1.784 | 20 | 24 | fits | 20,195 | 15 | 0.478 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 316,108 | 3.951 | 20 | 24 | fits | 127,072 | 114 | 0.289 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 255,257 | 3.191 | 20 | 24 | fits | 35,359 | 18 | 0.668 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 377,590 | 4.720 | 20 | 24 | fits | 70,109 | 17 | 0.662 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 368,115 | 4.601 | 20 | 24 | fits | 82,546 | 17 | 0.662 |
| READ_DESCRIPTOR held for a token (#917) | `aecp.held.read_descriptor.if0` | 417,570 | 5.220 | 20 | 24 | fits | 24,174 | 17 | 0.698 |
| LINK_UP | `fixture.link_up.if0` | 2,890 | 0.036 | 20 | 200 | fits | 19,889 | 44 (12) | 0.673 |
| malformed MRPDU discard | `fixture.malformed.if0` | 14,059 | 0.176 | 20 | 20 | fits | 14,125 | 12 | 0.690 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 26,579 | 0.332 | 20 | 24 | fits | 38,386 | 43 | 0.769 |
| LINK_DOWN | `fixture.link_down.if0` | 2,060 | 0.026 | 20 | 200 | fits | 19,664 | 23 (9) | 0.722 |
| BIND_RX | `fixture.bind_rx.if0` | 16,292 | 0.204 | 20 | 20 | fits | 33,548 | 26 (77) | 0.768 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 22,385 | 0.280 | 20 | 20 | fits | 31,828 | 35 (35) | 0.779 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 7,124 | 0.089 | 20 | 20 | fits | 18,470 | 13 (29) | 0.783 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 72,618 | 0.908 | 20 | 200 | fits | 72,720 | 75 | 0.724 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 72,618 | 0.908 | 20 | 200 | fits | 72,720 | 75 | 0.724 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 72,344 | 0.904 | 20 | 20 | fits | 72,720 | 75 | 0.724 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 72,344 | 0.904 | 20 | 20 | fits | 72,720 | 75 | 0.724 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 72,552 | 0.907 | 20 | 24 | fits | 72,720 | 75 | 0.724 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 72,552 | 0.907 | 20 | 24 | fits | 72,720 | 75 | 0.724 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 72,486 | 0.906 | 20 | 50 | fits | 72,720 | 75 | 0.724 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 72,486 | 0.906 | 20 | 50 | fits | 72,720 | 75 | 0.724 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 72,420 | 0.905 | 20 | 20 | fits | 72,720 | 75 | 0.724 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 72,420 | 0.905 | 20 | 20 | fits | 72,720 | 75 | 0.724 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
