### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 98 paths and 7 of 974 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.191 (0.441) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.090 (0.237) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.106 (0.306) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.103 (1.255) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.104 (0.254) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.079 (0.236) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.098 (0.247) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.100 (0.255) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.106 (0.325) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.153 (0.514) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.151 (0.503) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.778 (2.034) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.100 (0.459) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.180 (0.594) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.141 (0.490) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.155 (0.414) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.052 (0.168) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.021 (0.152) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.022 (0.300) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.022 (0.287) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.160 (0.322) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.222 (0.524) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.174 (0.493) | fits | 0 aecp | 1 | 0 |
| get_as_path, refused ENTITY_MISBEHAVING | 0 | `aecp.get_as_path.if0` (aecp) | 0.217 (0.543) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.178 (0.501) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.146 (0.463) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.217 (0.545) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.172 (0.493) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR held for a token (#917) | 0 | `aecp.held.read_descriptor.if0` (aecp-held) | 5.349 (5.681) | fits | 16 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.210 (0.633) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.141 (0.460) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.325 (0.651) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.169 (0.496) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.158 (0.480) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.197 (0.518) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.238 (0.565) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.160 (0.484) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.191 (0.513) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.162 (0.489) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i79.c0.if0` (aecp) | 0.162 (0.485) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.199 (0.520) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.164 (0.488) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.195 (0.519) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.169 (0.491) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.197 (0.518) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.135 (0.456) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.277 (0.717) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.188 (0.509) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.196 (0.577) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 3.032 (3.364) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.494 (0.797) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.483 (0.835) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.412 (0.792) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.432 (0.719) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.471 (0.817) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.115 (3.436) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.385 (0.702) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 3.263 (3.610) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.501 (2.905) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.455 (3.857) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.052 (3.440) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.315 (1.668) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.033 (6.252) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-6.adp_available.if0` (backlog-adp@program-aged2-6) | 6.510 (6.946) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.161 (0.554) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.649 (2.260) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.984 (64.293) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.762 (65.065) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.335 (0.483) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-burst.held.acmp.if0` (save-burst) | 2.908 | fits | 11 acmp | 4 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 3.017 | fits | 7 adp | 4 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-flight.held.aecp.if0` (save-flight) | 5.594 | fits | 14 aecp | 4 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 4.205 | fits | 6 maap | 4 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 9.849 | fits | 31 srp | 4 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.193 (0.520) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.123 (0.257) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.126 (0.287) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.171 (0.520) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.221 (0.527) | fits | 0 events | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-burst.mrpdu.periodic.if0` (save-burst) | 3.130 | fits | 0 srp | 10 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-1.service.acmp.first.if0` (backlog-adp@blank-1) | 5.320 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 63.003 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-1.service.adp.first.if0` (backlog-adp@blank-1) | 5.311 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-7.service.adp.last.if0` (backlog-adp@verify-aged2-7) | 6.907 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-3.service.aecp.first.if0` (backlog-adp@verify-3) | 2.338 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 63.038 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-1.service.maap.first.if0` (backlog-adp@blank-1) | 5.346 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-7.service.maap.last.if0` (backlog-adp@verify-aged2-7) | 6.944 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-5.service.srp.first.if0` (backlog-adp@program-aged2-5) | 8.320 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-3.service.srp.last.if0` (backlog-adp@verify-aged2-3) | 11.483 | fits | 31 srp | 77 | 0 |
| Talker Advertise RX for every input, bound | 0 | `srp.bound_advertise.if0` (srp-bound) | 2.504 (3.484) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.725 (0.784) | fits | 0 srp | 1 | 0 |
| Talker Advertise RX for every input, no binding (kept) | 0 | `srp.kept_advertise.if0` (srp-kept) | 1.533 (1.533) | fits | 0 srp | 1 | 0 |
| Talker Failed RX for every input, no binding (kept) | 0 | `srp.kept_failed.if0` (srp-kept) | 1.583 (1.583) | fits | 0 srp | 1 | 0 |
| Talker RX at the bound after a freed block (count) | 0 | `srp.kept_recount.if0` (srp-kept) | 0.911 (0.912) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.408 (0.409) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.218 (0.218) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.759 (0.829) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 14.416 | 11 | 153,637 (1.536) | yes | - |
| backlog-adp@blank-1 | 0 | 17.178 | 12 | 155,084 (1.551) | yes | - |
| backlog-adp@blank-2 | 0 | 17.053 | 12 | 155,084 (1.551) | yes | - |
| backlog-adp@blank-3 | 0 | 16.928 | 12 | 155,084 (1.551) | yes | - |
| backlog-adp@blank-4 | 0 | 16.803 | 12 | 155,084 (1.551) | yes | - |
| backlog-adp@blank-5 | 0 | 16.678 | 12 | 155,084 (1.551) | yes | - |
| backlog-adp@blank-6 | 0 | 16.553 | 12 | 155,084 (1.551) | yes | - |
| backlog-adp@blank-7 | 0 | 16.428 | 12 | 155,084 (1.551) | yes | - |
| backlog-adp@program-0 | 0 | 12.426 | 9 | 154,932 (1.549) | yes | - |
| backlog-adp@program-1 | 0 | 12.176 | 9 | 154,932 (1.549) | yes | - |
| backlog-adp@program-2 | 0 | 11.926 | 9 | 154,932 (1.549) | yes | - |
| backlog-adp@program-3 | 0 | 12.648 | 8 | 149,699 (1.497) | yes | - |
| backlog-adp@program-4 | 0 | 12.581 | 9 | 149,765 (1.498) | yes | - |
| backlog-adp@program-5 | 0 | 12.331 | 9 | 149,765 (1.498) | yes | - |
| backlog-adp@program-6 | 0 | 12.081 | 9 | 149,765 (1.498) | yes | - |
| backlog-adp@program-7 | 0 | 12.768 | 9 | 152,733 (1.527) | yes | - |
| backlog-adp@verify-0 | 1 | 15.414 | 10 | 149,996 (1.500) | yes | - |
| backlog-adp@verify-1 | 1 | 15.414 | 10 | 149,996 (1.500) | yes | - |
| backlog-adp@verify-2 | 0 | 15.429 | 11 | 150,365 (1.504) | yes | - |
| backlog-adp@verify-3 | 0 | 16.242 | 11 | 151,864 (1.519) | yes | - |
| backlog-adp@verify-4 | 0 | 16.117 | 11 | 151,864 (1.519) | yes | - |
| backlog-adp@verify-5 | 0 | 15.992 | 11 | 151,864 (1.519) | yes | - |
| backlog-adp@verify-6 | 0 | 15.867 | 11 | 151,864 (1.519) | yes | - |
| backlog-adp@verify-7 | 0 | 15.742 | 11 | 151,864 (1.519) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 13.084 | 9 | 153,568 (1.536) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 16.184 | 11 | 154,015 (1.540) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 15.261 | 11 | 151,689 (1.517) | yes | - |
| backlog-adp@blank-aged2-3 | 1 | 14.131 | 9 | 153,720 (1.537) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 14.229 | 10 | 152,544 (1.525) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 16.171 | 11 | 154,511 (1.545) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 15.211 | 10 | 155,263 (1.553) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 14.101 | 9 | 149,968 (1.500) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 13.310 | 10 | 153,574 (1.536) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 13.317 | 9 | 150,076 (1.501) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 13.239 | 9 | 155,096 (1.551) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 13.178 | 8 | 155,608 (1.556) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 17.417 | 12 | 150,137 (1.501) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 13.508 | 11 | 153,580 (1.536) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 15.446 | 11 | 154,500 (1.545) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 14.349 | 10 | 149,919 (1.499) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 12.693 | 10 | 149,965 (1.500) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 12.710 | 9 | 153,872 (1.539) | yes | - |
| backlog-adp@program-aged2-2 | 1 | 12.690 | 8 | 150,008 (1.500) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 12.771 | 9 | 155,034 (1.550) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 14.168 | 11 | 150,407 (1.504) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 12.808 | 9 | 154,636 (1.546) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 14.213 | 11 | 148,055 (1.481) | yes | - |
| backlog-adp@program-aged2-7 | 1 | 12.736 | 8 | 156,303 (1.563) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 12.935 | 11 | 154,978 (1.550) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 12.748 | 10 | 153,878 (1.539) | yes | - |
| backlog-adp@program-aged1-2 | 1 | 12.625 | 8 | 151,878 (1.519) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 12.683 | 9 | 153,630 (1.536) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 12.645 | 9 | 154,787 (1.548) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 12.743 | 9 | 150,175 (1.502) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 14.247 | 12 | 154,590 (1.546) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 13.110 | 10 | 154,843 (1.548) | yes | - |
| backlog-adp@verify-aged2-0 | 1 | 15.280 | 10 | 152,407 (1.524) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 15.282 | 11 | 150,587 (1.506) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 14.301 | 10 | 156,088 (1.561) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 14.277 | 10 | 150,276 (1.503) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 14.093 | 9 | 152,600 (1.526) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 16.209 | 10 | 154,338 (1.543) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 17.344 | 12 | 150,588 (1.506) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 16.196 | 11 | 157,096 (1.571) | yes | - |
| backlog-adp@verify-aged1-0 | 1 | 13.865 | 10 | 153,392 (1.534) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 16.987 | 13 | 153,839 (1.538) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 15.142 | 13 | 151,513 (1.515) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 14.146 | 12 | 154,882 (1.549) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 14.108 | 12 | 150,233 (1.502) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 16.087 | 13 | 151,013 (1.510) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 15.103 | 11 | 154,498 (1.545) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 13.852 | 11 | 156,314 (1.563) | yes | - |
| backlog | 0 | 7.750 | 8 | 175,333 (1.753) | yes | - |
| backlog-adp | 0 | 11.283 | 11 | 153,614 (1.536) | yes | - |
| backlog-adp-refill | 0 | 40.834 | 22 | 152,698 (1.527) | yes | - |
| backlog-owed | 0 | 65.406 | 23 | 171,589 (1.716) | yes | - |
| fixture | 0 | 1.440 | 2 | 95,749 (0.957) | yes | - |

Composed maximum over the 4 backlog windows: 175,333 CPU cycles (1.753 ms), backlog.
Over the windows that released their whole load only: 175,333 (1.753 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 167748 | 0 | 50,461 (0.505) | fits |
| srp-kept | 1906 | 0 | 158,334 (1.583) | fits |
| save-burst | 2849 | 0 | 163,828 (1.638) | fits |
| save-held | 3079 | 0 | 163,828 (1.638) | fits |
| save-starved | 77433 | 0 | 163,828 (1.638) | fits |
| save-flight | 2628 | 0 | 163,828 (1.638) | fits |
| acmp-notk | 3356 | 0 | 114,323 (1.143) | fits |
| srp-bound | 5747 | 1 | 212,037 (2.120) | OVER the share |
| backlog-adp@blank-0 | 345 | 0 | 153,637 (1.536) | fits |
| backlog-adp@blank-1 | 346 | 0 | 155,084 (1.551) | fits |
| backlog-adp@blank-2 | 346 | 0 | 155,084 (1.551) | fits |
| backlog-adp@blank-3 | 346 | 0 | 155,084 (1.551) | fits |
| backlog-adp@blank-4 | 346 | 0 | 155,084 (1.551) | fits |
| backlog-adp@blank-5 | 346 | 0 | 155,084 (1.551) | fits |
| backlog-adp@blank-6 | 346 | 0 | 155,084 (1.551) | fits |
| backlog-adp@blank-7 | 346 | 0 | 155,084 (1.551) | fits |
| backlog-adp@program-0 | 382 | 0 | 154,932 (1.549) | fits |
| backlog-adp@program-1 | 382 | 0 | 154,932 (1.549) | fits |
| backlog-adp@program-2 | 382 | 0 | 154,932 (1.549) | fits |
| backlog-adp@program-3 | 382 | 0 | 149,699 (1.497) | fits |
| backlog-adp@program-4 | 382 | 0 | 149,765 (1.498) | fits |
| backlog-adp@program-5 | 382 | 0 | 149,765 (1.498) | fits |
| backlog-adp@program-6 | 382 | 0 | 149,765 (1.498) | fits |
| backlog-adp@program-7 | 382 | 0 | 152,733 (1.527) | fits |
| backlog-adp@verify-0 | 406 | 0 | 152,818 (1.528) | fits |
| backlog-adp@verify-1 | 406 | 0 | 152,818 (1.528) | fits |
| backlog-adp@verify-2 | 407 | 0 | 150,365 (1.504) | fits |
| backlog-adp@verify-3 | 407 | 0 | 151,864 (1.519) | fits |
| backlog-adp@verify-4 | 407 | 0 | 151,864 (1.519) | fits |
| backlog-adp@verify-5 | 407 | 0 | 151,864 (1.519) | fits |
| backlog-adp@verify-6 | 407 | 0 | 151,864 (1.519) | fits |
| backlog-adp@verify-7 | 407 | 0 | 151,864 (1.519) | fits |
| backlog-adp@blank-aged2-0 | 651 | 0 | 153,568 (1.536) | fits |
| backlog-adp@blank-aged2-1 | 662 | 0 | 154,015 (1.540) | fits |
| backlog-adp@blank-aged2-2 | 670 | 0 | 151,689 (1.517) | fits |
| backlog-adp@blank-aged2-3 | 677 | 0 | 153,720 (1.537) | fits |
| backlog-adp@blank-aged2-4 | 686 | 0 | 152,544 (1.525) | fits |
| backlog-adp@blank-aged2-5 | 695 | 0 | 154,511 (1.545) | fits |
| backlog-adp@blank-aged2-6 | 703 | 0 | 155,263 (1.553) | fits |
| backlog-adp@blank-aged2-7 | 710 | 0 | 149,968 (1.500) | fits |
| backlog-adp@blank-aged1-0 | 585 | 0 | 153,574 (1.536) | fits |
| backlog-adp@blank-aged1-1 | 593 | 0 | 150,076 (1.501) | fits |
| backlog-adp@blank-aged1-2 | 601 | 0 | 155,096 (1.551) | fits |
| backlog-adp@blank-aged1-3 | 609 | 0 | 160,951 (1.610) | fits |
| backlog-adp@blank-aged1-4 | 621 | 0 | 150,137 (1.501) | fits |
| backlog-adp@blank-aged1-5 | 628 | 0 | 153,580 (1.536) | fits |
| backlog-adp@blank-aged1-6 | 637 | 0 | 154,500 (1.545) | fits |
| backlog-adp@blank-aged1-7 | 644 | 0 | 149,919 (1.499) | fits |
| backlog-adp@program-aged2-0 | 708 | 0 | 149,965 (1.500) | fits |
| backlog-adp@program-aged2-1 | 715 | 0 | 153,872 (1.539) | fits |
| backlog-adp@program-aged2-2 | 723 | 0 | 150,008 (1.500) | fits |
| backlog-adp@program-aged2-3 | 732 | 0 | 155,034 (1.550) | fits |
| backlog-adp@program-aged2-4 | 742 | 0 | 150,407 (1.504) | fits |
| backlog-adp@program-aged2-5 | 749 | 0 | 160,951 (1.610) | fits |
| backlog-adp@program-aged2-6 | 759 | 0 | 148,055 (1.481) | fits |
| backlog-adp@program-aged2-7 | 765 | 0 | 156,303 (1.563) | fits |
| backlog-adp@program-aged1-0 | 642 | 0 | 154,978 (1.550) | fits |
| backlog-adp@program-aged1-1 | 649 | 0 | 153,878 (1.539) | fits |
| backlog-adp@program-aged1-2 | 657 | 0 | 151,878 (1.519) | fits |
| backlog-adp@program-aged1-3 | 665 | 0 | 153,630 (1.536) | fits |
| backlog-adp@program-aged1-4 | 673 | 0 | 154,787 (1.548) | fits |
| backlog-adp@program-aged1-5 | 682 | 0 | 150,175 (1.502) | fits |
| backlog-adp@program-aged1-6 | 693 | 0 | 154,590 (1.546) | fits |
| backlog-adp@program-aged1-7 | 700 | 0 | 154,843 (1.548) | fits |
| backlog-adp@verify-aged2-0 | 672 | 0 | 152,688 (1.527) | fits |
| backlog-adp@verify-aged2-1 | 679 | 0 | 150,587 (1.506) | fits |
| backlog-adp@verify-aged2-2 | 687 | 0 | 156,088 (1.561) | fits |
| backlog-adp@verify-aged2-3 | 695 | 0 | 150,276 (1.503) | fits |
| backlog-adp@verify-aged2-4 | 702 | 0 | 152,600 (1.526) | fits |
| backlog-adp@verify-aged2-5 | 712 | 0 | 154,338 (1.543) | fits |
| backlog-adp@verify-aged2-6 | 722 | 0 | 150,588 (1.506) | fits |
| backlog-adp@verify-aged2-7 | 729 | 0 | 157,096 (1.571) | fits |
| backlog-adp@verify-aged1-0 | 606 | 0 | 153,392 (1.534) | fits |
| backlog-adp@verify-aged1-1 | 617 | 0 | 153,839 (1.538) | fits |
| backlog-adp@verify-aged1-2 | 625 | 0 | 151,513 (1.515) | fits |
| backlog-adp@verify-aged1-3 | 633 | 0 | 154,882 (1.549) | fits |
| backlog-adp@verify-aged1-4 | 641 | 0 | 150,233 (1.502) | fits |
| backlog-adp@verify-aged1-5 | 650 | 0 | 151,013 (1.510) | fits |
| backlog-adp@verify-aged1-6 | 657 | 0 | 154,498 (1.545) | fits |
| backlog-adp@verify-aged1-7 | 665 | 0 | 156,314 (1.563) | fits |
| adp-advertise | 599 | 0 | 30,275 (0.303) | fits |
| acmp-noresp | 1886 | 0 | 113,738 (1.137) | fits |
| save-bind | 1664 | 0 | 114,024 (1.140) | fits |
| save | 608 | 0 | 85,132 (0.851) | fits |
| srp | 289 | 0 | 44,079 (0.441) | fits |
| save-bind-in-capture | 843 | 0 | 113,802 (1.138) | fits |
| save-bind-in-seal | 845 | 0 | 113,623 (1.136) | fits |
| save-bind-in-erase | 846 | 0 | 113,753 (1.138) | fits |
| save-bind-in-erase-late | 853 | 0 | 113,802 (1.138) | fits |
| save-bind-in-blank | 909 | 0 | 113,753 (1.138) | fits |
| save-bind-in-blank-late | 871 | 0 | 114,088 (1.141) | fits |
| save-bind-in-program | 917 | 0 | 114,165 (1.142) | fits |
| save-bind-in-program-late | 927 | 0 | 113,712 (1.137) | fits |
| save-bind-in-verify | 875 | 0 | 113,702 (1.137) | fits |
| save-bind-in-verify-late | 935 | 0 | 113,797 (1.138) | fits |
| save-bind-burst | 5327 | 0 | 115,805 (1.158) | fits |
| backlog | 286 | 0 | 175,333 (1.753) | fits |
| backlog-adp | 312 | 0 | 153,614 (1.536) | fits |
| backlog-adp-refill | 323 | 0 | 152,698 (1.527) | fits |
| backlog-owed | 307 | 0 | 171,589 (1.716) | fits |
| acmp-disc | 879 | 0 | 114,110 (1.141) | fits |
| maap | 174 | 0 | 30,275 (0.303) | fits |
| adp-link | 91 | 0 | 41,364 (0.414) | fits |
| adp-gm | 90 | 0 | 28,684 (0.287) | fits |
| adp-discover | 90 | 0 | 28,684 (0.287) | fits |
| control | 90 | 0 | 28,684 (0.287) | fits |
| aecp-fanout | 111 | 0 | 62,400 (0.624) | fits |
| acmp-cmd | 87 | 0 | 43,371 (0.434) | fits |
| aecp | 113 | 0 | 46,451 (0.465) | fits |
| aecp-largest-notice | 105 | 0 | 145,230 (1.452) | fits |
| aecp-held | 103 | 0 | 43,842 (0.438) | fits |
| datapath-events | 117 | 0 | 28,684 (0.287) | fits |
| fixture | 153 | 0 | 101,229 (1.012) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | +10.486 ms, 76,922 (0.769 ms), read-back | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 10.449 (20) | 9.551 |
| backlog-adp@blank-aged2-1 | 2 | +10.076 ms, 76,923 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 11.326 (20) | 8.674 |
| backlog-adp@blank-aged2-2 | 2 | +8.730 ms, 76,863 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 11.299 (20) | 8.701 |
| backlog-adp@blank-aged2-3 | 2 | +7.417 ms, 77,197 (0.772 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 11.364 (20) | 8.636 |
| backlog-adp@blank-aged2-4 | 2 | +6.162 ms, 76,903 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 11.463 (20) | 8.537 |
| backlog-adp@blank-aged2-5 | 2 | +6.121 ms, 76,872 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 11.421 (20) | 8.579 |
| backlog-adp@blank-aged2-6 | 2 | +4.528 ms, 76,807 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 11.363 (20) | 8.637 |
| backlog-adp@blank-aged2-7 | 2 | +3.038 ms, 76,356 (0.764 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 11.329 (20) | 8.671 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 10.541 (20) | 9.459 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 10.548 (20) | 9.452 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 10.465 (20) | 9.535 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 10.406 (20) | 9.594 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 10.554 (20) | 9.446 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 10.447 (20) | 9.553 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 10.693 (20) | 9.307 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 10.499 (20) | 9.501 |
| backlog-adp@program-aged2-0 | 2 | none | +10.713 ms, 80,801 (0.808 ms), issue | `backlog-adp@program-aged2-0.service.srp.last.if0` | 10.676 (20) | 9.324 |
| backlog-adp@program-aged2-1 | 2 | +10.017 ms, 80,702 (0.807 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 11.310 (20) | 8.690 |
| backlog-adp@program-aged2-2 | 2 | +8.577 ms, 80,819 (0.808 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 11.293 (20) | 8.707 |
| backlog-adp@program-aged2-3 | 2 | +7.526 ms, 81,163 (0.812 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 11.364 (20) | 8.636 |
| backlog-adp@program-aged2-4 | 2 | +6.049 ms, 80,804 (0.808 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 11.323 (20) | 8.677 |
| backlog-adp@program-aged2-5 | 2 | +6.168 ms, 80,804 (0.808 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 11.404 (20) | 8.596 |
| backlog-adp@program-aged2-6 | 2 | +4.583 ms, 80,647 (0.806 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 11.481 (20) | 8.519 |
| backlog-adp@program-aged2-7 | 2 | +4.406 ms, 80,574 (0.806 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 11.335 (20) | 8.665 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 10.494 (20) | 9.506 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 10.591 (20) | 9.409 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 10.469 (20) | 9.531 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 10.527 (20) | 9.473 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 10.488 (20) | 9.512 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 10.585 (20) | 9.415 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 10.472 (20) | 9.528 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 10.418 (20) | 9.582 |
| backlog-adp@verify-aged2-0 | 2 | none | +10.534 ms, 77,665 (0.777 ms), read-back | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 10.496 (20) | 9.504 |
| backlog-adp@verify-aged2-1 | 2 | +10.025 ms, 77,666 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 11.284 (20) | 8.716 |
| backlog-adp@verify-aged2-2 | 2 | +8.738 ms, 77,628 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 11.218 (20) | 8.782 |
| backlog-adp@verify-aged2-3 | 2 | +7.418 ms, 78,012 (0.780 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 11.483 (20) | 8.517 |
| backlog-adp@verify-aged2-4 | 2 | +5.991 ms, 77,747 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 11.299 (20) | 8.701 |
| backlog-adp@verify-aged2-5 | 2 | +6.099 ms, 77,716 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 11.412 (20) | 8.588 |
| backlog-adp@verify-aged2-6 | 2 | +4.464 ms, 77,600 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 11.337 (20) | 8.663 |
| backlog-adp@verify-aged2-7 | 2 | +2.982 ms, 77,136 (0.771 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 11.280 (20) | 8.720 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 10.474 (20) | 9.526 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 10.854 (20) | 9.146 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 11.126 (20) | 8.874 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 11.346 (20) | 8.654 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 11.308 (20) | 8.692 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 11.283 (20) | 8.717 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 11.209 (20) | 8.791 |
| backlog-adp@verify-aged1-7 | 1 | none | +11.219 ms, 77,658 (0.777 ms), read-back | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 11.182 (20) | 8.818 |

Least margin over the aged windows: 8.517 ms, `backlog-adp@verify-aged2-3.service.srp.last.if0` at 11.483 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 23789.761 | 23,830 | 398 | 2 | 30.873 | yes | within |
| save-held | 1344.318 | 12,950 | 398 | - | 32.699 | no | within |
| save-starved | 12927.097 | 12,950 | 398 | - | 33.043 | yes | within |
| save | 1298.777 | 12,950 | 398 | - | 102.341 | no | within |

Names from their response to durable (save_burst.py; #920, #665's ruling of 2026-11-15, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-burst | 115 | 1353.998 (0) | 5,000 | 8 | - | - | sequence 8, 0 missing | within |
| save-flight | 1 | 650.995 (0) | 5,000 | 2 | - | - | 61 steps (want 61), 24.957 ms | within |

Binding changes from their response to durable (bind_save.py; the binding class's 100 ms window, Milan v1.2 5.5.3.5.3 and 5.3.8.3), with the part's erase of 120 ms and page program of 0.5 ms modelled:

| Group | Command | Sink | Durable, ms | Target ms | Saves | Erases | Verdict |
|---|---|---:|---:|---:|---:|---:|---|
| save-bind | BIND_RX | 0 | 550.477 | 800 | 4 | 4 | within |
| save-bind | STOP_STREAMING | 0 | 549.97 | 800 | 4 | 4 | within |
| save-bind | START_STREAMING | 0 | 550.481 | 800 | 4 | 4 | within |
| save-bind | UNBIND_RX | 0 | 550.417 | 800 | 4 | 4 | within |
| save-bind-in-capture | BIND_RX | 0 | 891.169 | 950 | 2 | 2 | within |
| save-bind-in-seal | BIND_RX | 0 | 880.349 | 950 | 2 | 2 | within |
| save-bind-in-erase | BIND_RX | 0 | 870.845 | 950 | 2 | 2 | within |
| save-bind-in-erase-late | BIND_RX | 0 | 810.709 | 950 | 2 | 2 | within |
| save-bind-in-blank | BIND_RX | 0 | 750.094 | 950 | 2 | 2 | within |
| save-bind-in-blank-late | BIND_RX | 0 | 650.089 | 950 | 2 | 2 | within |
| save-bind-in-program | BIND_RX | 0 | 649.101 | 950 | 2 | 2 | within |
| save-bind-in-program-late | BIND_RX | 0 | 558.193 | 950 | 2 | 2 | within |
| save-bind-in-verify | BIND_RX | 0 | 553.369 | 950 | 2 | 2 | within |
| save-bind-in-verify-late | BIND_RX | 0 | 552.76 | 950 | 2 | 2 | within |
| save-bind-burst | BIND_RX | 1 | 646.392 | 950 | 2 | 2 | within |
| save-bind-burst | BIND_RX | 2 | 637.148 | 950 | 2 | 2 | within |
| save-bind-burst | BIND_RX | 3 | 626.699 | 950 | 2 | 2 | within |
| save-bind-burst | BIND_RX | 4 | 616.649 | 950 | 2 | 2 | within |
| save-bind-burst | BIND_RX | 5 | 607.244 | 950 | 2 | 2 | within |
| save-bind-burst | BIND_RX | 6 | 596.839 | 950 | 2 | 2 | within |
| save-bind-burst | BIND_RX | 7 | 586.566 | 950 | 2 | 2 | within |
| save-bind-burst | BIND_RX | 8 | 576.35 | 950 | 2 | 2 | within |
| save-bind-burst | UNBIND_RX | 0 | 567.193 | 950 | 2 | 2 | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1112 | 81,934 (0.819) | 78,567 (0.786) |
| srp-kept | 1844 | 23,901 (0.239) | 2,984 (0.030) |
| save-burst | 4585 | 102,764 (1.028) | 78,997 (0.790) |
| save-held | 1974 | 95,044 (0.950) | 78,286 (0.783) |
| save-starved | 714 | 81,554 (0.816) | 78,597 (0.786) |
| save-flight | 2096 | 95,041 (0.950) | 78,329 (0.783) |
| acmp-notk | 1431 | 114,323 (1.143) | 78,511 (0.785) |
| srp-bound | 3605 | 114,456 (1.145) | 79,312 (0.793) |
| backlog-adp@blank-0 | 344 | 100,446 (1.004) | 76,858 (0.769) |
| backlog-adp@blank-1 | 347 | 100,342 (1.003) | 76,858 (0.769) |
| backlog-adp@blank-2 | 347 | 100,342 (1.003) | 76,858 (0.769) |
| backlog-adp@blank-3 | 347 | 100,342 (1.003) | 76,858 (0.769) |
| backlog-adp@blank-4 | 347 | 100,342 (1.003) | 76,858 (0.769) |
| backlog-adp@blank-5 | 347 | 100,342 (1.003) | 76,858 (0.769) |
| backlog-adp@blank-6 | 347 | 100,342 (1.003) | 76,858 (0.769) |
| backlog-adp@blank-7 | 347 | 100,342 (1.003) | 76,858 (0.769) |
| backlog-adp@program-0 | 458 | 94,692 (0.947) | 78,198 (0.782) |
| backlog-adp@program-1 | 458 | 94,692 (0.947) | 78,198 (0.782) |
| backlog-adp@program-2 | 458 | 94,692 (0.947) | 78,198 (0.782) |
| backlog-adp@program-3 | 459 | 96,112 (0.961) | 79,120 (0.791) |
| backlog-adp@program-4 | 460 | 94,692 (0.947) | 78,198 (0.782) |
| backlog-adp@program-5 | 460 | 94,692 (0.947) | 78,198 (0.782) |
| backlog-adp@program-6 | 460 | 94,692 (0.947) | 78,198 (0.782) |
| backlog-adp@program-7 | 461 | 96,317 (0.963) | 79,036 (0.790) |
| backlog-adp@verify-0 | 570 | 95,526 (0.955) | 78,198 (0.782) |
| backlog-adp@verify-1 | 570 | 95,526 (0.955) | 78,198 (0.782) |
| backlog-adp@verify-2 | 570 | 95,526 (0.955) | 78,198 (0.782) |
| backlog-adp@verify-3 | 571 | 95,526 (0.955) | 78,198 (0.782) |
| backlog-adp@verify-4 | 571 | 95,526 (0.955) | 78,198 (0.782) |
| backlog-adp@verify-5 | 571 | 95,526 (0.955) | 78,198 (0.782) |
| backlog-adp@verify-6 | 571 | 95,526 (0.955) | 78,198 (0.782) |
| backlog-adp@verify-7 | 571 | 95,526 (0.955) | 78,198 (0.782) |
| backlog-adp@blank-aged2-0 | 341 | 92,537 (0.925) | 76,055 (0.761) |
| backlog-adp@blank-aged2-1 | 344 | 93,468 (0.935) | 76,214 (0.762) |
| backlog-adp@blank-aged2-2 | 343 | 93,211 (0.932) | 76,214 (0.762) |
| backlog-adp@blank-aged2-3 | 342 | 92,331 (0.923) | 76,441 (0.764) |
| backlog-adp@blank-aged2-4 | 342 | 92,210 (0.922) | 76,441 (0.764) |
| backlog-adp@blank-aged2-5 | 344 | 92,288 (0.923) | 76,441 (0.764) |
| backlog-adp@blank-aged2-6 | 343 | 92,286 (0.923) | 76,482 (0.765) |
| backlog-adp@blank-aged2-7 | 342 | 92,652 (0.927) | 76,464 (0.765) |
| backlog-adp@blank-aged1-0 | 341 | 92,582 (0.926) | 76,692 (0.767) |
| backlog-adp@blank-aged1-1 | 341 | 92,513 (0.925) | 76,692 (0.767) |
| backlog-adp@blank-aged1-2 | 341 | 92,876 (0.929) | 76,692 (0.767) |
| backlog-adp@blank-aged1-3 | 341 | 92,632 (0.926) | 76,692 (0.767) |
| backlog-adp@blank-aged1-4 | 345 | 93,327 (0.933) | 76,692 (0.767) |
| backlog-adp@blank-aged1-5 | 341 | 91,142 (0.911) | 76,611 (0.766) |
| backlog-adp@blank-aged1-6 | 343 | 92,582 (0.926) | 76,692 (0.767) |
| backlog-adp@blank-aged1-7 | 342 | 92,539 (0.925) | 76,692 (0.767) |
| backlog-adp@program-aged2-0 | 455 | 94,692 (0.947) | 78,532 (0.785) |
| backlog-adp@program-aged2-1 | 456 | 94,731 (0.947) | 78,532 (0.785) |
| backlog-adp@program-aged2-2 | 456 | 94,692 (0.947) | 78,532 (0.785) |
| backlog-adp@program-aged2-3 | 456 | 94,817 (0.948) | 78,672 (0.787) |
| backlog-adp@program-aged2-4 | 458 | 94,692 (0.947) | 78,628 (0.786) |
| backlog-adp@program-aged2-5 | 456 | 94,772 (0.948) | 78,628 (0.786) |
| backlog-adp@program-aged2-6 | 458 | 94,812 (0.948) | 78,378 (0.784) |
| backlog-adp@program-aged2-7 | 456 | 94,692 (0.947) | 78,242 (0.782) |
| backlog-adp@program-aged1-0 | 455 | 94,972 (0.950) | 79,018 (0.790) |
| backlog-adp@program-aged1-1 | 455 | 96,391 (0.964) | 79,120 (0.791) |
| backlog-adp@program-aged1-2 | 455 | 96,343 (0.963) | 79,036 (0.790) |
| backlog-adp@program-aged1-3 | 455 | 96,384 (0.964) | 79,120 (0.791) |
| backlog-adp@program-aged1-4 | 455 | 96,768 (0.968) | 79,120 (0.791) |
| backlog-adp@program-aged1-5 | 455 | 96,941 (0.969) | 79,120 (0.791) |
| backlog-adp@program-aged1-6 | 457 | 96,942 (0.969) | 79,120 (0.791) |
| backlog-adp@program-aged1-7 | 456 | 96,959 (0.970) | 79,120 (0.791) |
| backlog-adp@verify-aged2-0 | 570 | 95,526 (0.955) | 78,198 (0.782) |
| backlog-adp@verify-aged2-1 | 570 | 95,526 (0.955) | 78,198 (0.782) |
| backlog-adp@verify-aged2-2 | 569 | 95,526 (0.955) | 78,198 (0.782) |
| backlog-adp@verify-aged2-3 | 569 | 95,526 (0.955) | 78,198 (0.782) |
| backlog-adp@verify-aged2-4 | 569 | 95,526 (0.955) | 78,198 (0.782) |
| backlog-adp@verify-aged2-5 | 571 | 95,526 (0.955) | 78,198 (0.782) |
| backlog-adp@verify-aged2-6 | 572 | 95,526 (0.955) | 78,198 (0.782) |
| backlog-adp@verify-aged2-7 | 571 | 95,526 (0.955) | 78,198 (0.782) |
| backlog-adp@verify-aged1-0 | 568 | 99,425 (0.994) | 78,198 (0.782) |
| backlog-adp@verify-aged1-1 | 571 | 99,476 (0.995) | 78,198 (0.782) |
| backlog-adp@verify-aged1-2 | 569 | 95,526 (0.955) | 78,198 (0.782) |
| backlog-adp@verify-aged1-3 | 568 | 95,526 (0.955) | 78,198 (0.782) |
| backlog-adp@verify-aged1-4 | 568 | 95,526 (0.955) | 78,198 (0.782) |
| backlog-adp@verify-aged1-5 | 570 | 95,526 (0.955) | 78,198 (0.782) |
| backlog-adp@verify-aged1-6 | 569 | 95,526 (0.955) | 78,198 (0.782) |
| backlog-adp@verify-aged1-7 | 568 | 95,526 (0.955) | 78,198 (0.782) |
| adp-advertise | 579 | 23,226 (0.232) | 2,844 (0.028) |
| acmp-noresp | 981 | 113,738 (1.137) | 78,650 (0.786) |
| save-bind | 4705 | 114,024 (1.140) | 78,650 (0.786) |
| save | 953 | 95,041 (0.950) | 78,094 (0.781) |
| srp | 271 | 23,226 (0.232) | 2,844 (0.028) |
| save-bind-in-capture | 2446 | 113,802 (1.138) | 78,650 (0.786) |
| save-bind-in-seal | 2446 | 113,623 (1.136) | 78,650 (0.786) |
| save-bind-in-erase | 2445 | 113,753 (1.138) | 78,650 (0.786) |
| save-bind-in-erase-late | 2469 | 113,802 (1.138) | 78,650 (0.786) |
| save-bind-in-blank | 2490 | 113,753 (1.138) | 78,681 (0.787) |
| save-bind-in-blank-late | 2507 | 114,088 (1.141) | 78,650 (0.786) |
| save-bind-in-program | 2501 | 114,165 (1.142) | 78,650 (0.786) |
| save-bind-in-program-late | 2510 | 113,712 (1.137) | 78,647 (0.786) |
| save-bind-in-verify | 2520 | 113,702 (1.137) | 78,647 (0.786) |
| save-bind-in-verify-late | 2526 | 113,797 (1.138) | 78,647 (0.786) |
| save-bind-burst | 1927 | 115,805 (1.158) | 79,101 (0.791) |
| backlog | 266 | 23,226 (0.232) | 2,844 (0.028) |
| backlog-adp | 271 | 23,226 (0.232) | 2,844 (0.028) |
| backlog-adp-refill | 274 | 23,226 (0.232) | 2,844 (0.028) |
| backlog-owed | 277 | 23,226 (0.232) | 3,043 (0.030) |
| acmp-disc | 672 | 114,110 (1.141) | 78,500 (0.785) |
| maap | 162 | 22,945 (0.229) | 2,844 (0.028) |
| adp-link | 82 | 22,945 (0.229) | 2,844 (0.028) |
| adp-gm | 82 | 22,945 (0.229) | 2,844 (0.028) |
| adp-discover | 82 | 22,945 (0.229) | 2,844 (0.028) |
| control | 82 | 22,945 (0.229) | 2,844 (0.028) |
| aecp-fanout | 80 | 22,945 (0.229) | 2,844 (0.028) |
| acmp-cmd | 66 | 22,945 (0.229) | 2,844 (0.028) |
| aecp | 80 | 22,945 (0.229) | 2,844 (0.028) |
| aecp-largest-notice | 78 | 22,945 (0.229) | 2,844 (0.028) |
| aecp-held | 94 | 22,945 (0.229) | 2,844 (0.028) |
| datapath-events | 70 | 22,945 (0.229) | 2,844 (0.028) |
| fixture | 378 | 101,229 (1.012) | 78,737 (0.787) |

Longest pass that carries a step: 115,805 CPU cycles (1.158 ms), save-bind-burst; longest step: 79,312 (0.793 ms), srp-bound.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| Talker Advertise RX for every input, no binding (kept) | `srp.kept_advertise.if0` | 153,256 | 1.533 | 20 | 20 | fits | 153,322 | 12 | 0.936 |
| Talker RX at the bound after a freed block (count) | `srp.kept_recount.if0` | 91,118 | 0.911 | 20 | 20 | fits | 91,184 | 12 | 0.893 |
| Talker Failed RX for every input, no binding (kept) | `srp.kept_failed.if0` | 158,266 | 1.583 | 20 | 20 | fits | 158,334 | 12 | 0.940 |
| ADP record, every channel at its refill rate, the longest | `save-burst.held.adp.if0` | 299,582 | 2.996 | 20 | 200 | fits | 136,563 | 134 | 0.558 |
| ACMP record, every channel at its refill rate, the longest | `save-burst.held.acmp.if0` | 290,831 | 2.908 | 20 | 20 | fits | 63,586 | 51 | 0.244 |
| AECP record, every channel at its refill rate, the longest | `save-burst.held.aecp.if0` | 192,813 | 1.928 | 20 | 24 | fits | 94,152 | 40 | 0.769 |
| MAAP record, every channel at its refill rate, the longest | `save-burst.held.maap.if0` | 239,839 | 2.398 | 20 | 50 | fits | 136,563 | 134 | 0.558 |
| SRP record, every channel at its refill rate, the longest | `save-burst.held.srp.if0` | 707,491 | 7.075 | 20 | 20 | fits | 81,398 | 41 | 0.749 |
| an MRPDU its join timer owes, the longest | `save-burst.mrpdu.join.if0` | 53,075 | 0.531 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-burst.mrpdu.leaveall.if0` | 49,975 | 0.500 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-burst.mrpdu.periodic.if0` | 313,020 | 3.130 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 298,878 | 2.989 | 20 | 200 | fits | 135,990 | 129 | 0.533 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 268,687 | 2.687 | 20 | 20 | fits | 63,560 | 51 | 0.247 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 454,002 | 4.540 | 20 | 24 | fits | 57,415 | 27 | 0.517 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 239,266 | 2.393 | 20 | 50 | fits | 135,990 | 129 | 0.533 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 971,005 | 9.710 | 20 | 20 | fits | 51,249 | 20 | 0.723 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 51,241 | 0.512 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 52,672 | 0.527 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 289,786 | 2.898 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 301,718 | 3.017 | 20 | 200 | fits | 138,830 | 135 | 0.548 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 251,890 | 2.519 | 20 | 20 | fits | 138,049 | 121 | 0.235 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 480,177 | 4.802 | 20 | 24 | fits | 58,938 | 32 | 0.518 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 242,106 | 2.421 | 20 | 50 | fits | 138,830 | 135 | 0.548 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 984,936 | 9.849 | 20 | 20 | fits | 63,339 | 30 | 0.700 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 51,213 | 0.512 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 49,425 | 0.494 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 307,633 | 3.076 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 298,878 | 2.989 | 20 | 200 | fits | 135,990 | 129 | 0.533 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 269,850 | 2.699 | 20 | 20 | fits | 64,174 | 51 | 0.272 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 559,372 | 5.594 | 20 | 24 | fits | 125,034 | 49 | 0.643 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 420,539 | 4.205 | 20 | 50 | fits | 115,068 | 184 | 0.308 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 951,268 | 9.513 | 20 | 20 | fits | 31,024 | 12 | 0.811 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 80,907 | 0.809 | 49 | 49 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 17,982 | 0.180 | 20 | 20 | fits | 34,927 | 19 (14) | 0.869 |
| Talker Advertise RX for every input, bound | `srp.bound_advertise.if0` | 250,415 | 2.504 | 20 | 20 | fits | 212,037 | 40 | 0.897 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 567,487 | 5.675 | 20 | 20 | fits | 153,637 | 205 | 0.306 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 454,467 | 4.545 | 20 | 200 | fits | 152,563 | 122 | 0.452 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 607,488 | 6.075 | 20 | 200 | fits | 153,637 | 205 | 0.306 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 455,391 | 4.554 | 20 | 20 | fits | 152,563 | 122 | 0.452 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 742,590 | 7.426 | 20 | 20 | fits | 134,398 | 57 | 0.673 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 151,971 | 1.520 | 20 | 24 | fits | 149,961 | 109 | 0.440 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 458,041 | 4.580 | 20 | 24 | fits | 152,563 | 122 | 0.452 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 457,975 | 4.580 | 20 | 50 | fits | 152,563 | 122 | 0.452 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 611,216 | 6.112 | 20 | 50 | fits | 153,637 | 205 | 0.306 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 745,548 | 7.455 | 20 | 20 | fits | 134,398 | 57 | 0.673 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,048,394 | 10.484 | 20 | 20 | fits | 40,651 | 16 | 0.747 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 635,673 | 6.357 | 20 | 20 | fits | 155,084 | 208 | 0.256 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 531,054 | 5.311 | 20 | 200 | fits | 151,294 | 121 | 0.482 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 685,522 | 6.855 | 20 | 200 | fits | 155,084 | 208 | 0.256 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 531,978 | 5.320 | 20 | 20 | fits | 151,294 | 121 | 0.482 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 820,381 | 8.204 | 20 | 20 | fits | 134,155 | 57 | 0.672 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 229,761 | 2.298 | 20 | 24 | fits | 149,961 | 109 | 0.441 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 534,628 | 5.346 | 20 | 24 | fits | 151,294 | 121 | 0.482 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 534,562 | 5.346 | 20 | 50 | fits | 151,294 | 121 | 0.482 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 689,250 | 6.893 | 20 | 50 | fits | 155,084 | 208 | 0.256 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 823,339 | 8.233 | 20 | 20 | fits | 134,155 | 57 | 0.672 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 1,126,173 | 11.262 | 20 | 20 | fits | 40,664 | 16 | 0.747 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 623,173 | 6.232 | 20 | 20 | fits | 155,084 | 208 | 0.256 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 518,554 | 5.186 | 20 | 200 | fits | 151,294 | 121 | 0.482 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 673,022 | 6.730 | 20 | 200 | fits | 155,084 | 208 | 0.256 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 519,478 | 5.195 | 20 | 20 | fits | 151,294 | 121 | 0.482 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 807,881 | 8.079 | 20 | 20 | fits | 134,155 | 57 | 0.672 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 217,261 | 2.173 | 20 | 24 | fits | 149,961 | 109 | 0.441 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 522,128 | 5.221 | 20 | 24 | fits | 151,294 | 121 | 0.482 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 522,062 | 5.221 | 20 | 50 | fits | 151,294 | 121 | 0.482 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 676,750 | 6.768 | 20 | 50 | fits | 155,084 | 208 | 0.256 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 810,839 | 8.108 | 20 | 20 | fits | 134,155 | 57 | 0.672 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 1,113,673 | 11.137 | 20 | 20 | fits | 40,664 | 16 | 0.747 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 610,673 | 6.107 | 20 | 20 | fits | 155,084 | 208 | 0.256 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 506,054 | 5.061 | 20 | 200 | fits | 151,294 | 121 | 0.482 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 660,522 | 6.605 | 20 | 200 | fits | 155,084 | 208 | 0.256 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 506,978 | 5.070 | 20 | 20 | fits | 151,294 | 121 | 0.482 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 795,381 | 7.954 | 20 | 20 | fits | 134,155 | 57 | 0.672 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 204,761 | 2.048 | 20 | 24 | fits | 149,961 | 109 | 0.441 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 509,628 | 5.096 | 20 | 24 | fits | 151,294 | 121 | 0.482 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 509,562 | 5.096 | 20 | 50 | fits | 151,294 | 121 | 0.482 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 664,250 | 6.643 | 20 | 50 | fits | 155,084 | 208 | 0.256 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 798,339 | 7.983 | 20 | 20 | fits | 134,155 | 57 | 0.672 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 1,101,173 | 11.012 | 20 | 20 | fits | 40,664 | 16 | 0.747 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 598,173 | 5.982 | 20 | 20 | fits | 155,084 | 208 | 0.256 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 493,554 | 4.936 | 20 | 200 | fits | 151,294 | 121 | 0.482 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 648,022 | 6.480 | 20 | 200 | fits | 155,084 | 208 | 0.256 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 494,478 | 4.945 | 20 | 20 | fits | 151,294 | 121 | 0.482 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 782,881 | 7.829 | 20 | 20 | fits | 134,155 | 57 | 0.672 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 192,261 | 1.923 | 20 | 24 | fits | 149,961 | 109 | 0.441 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 497,128 | 4.971 | 20 | 24 | fits | 151,294 | 121 | 0.482 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 497,062 | 4.971 | 20 | 50 | fits | 151,294 | 121 | 0.482 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 651,750 | 6.518 | 20 | 50 | fits | 155,084 | 208 | 0.256 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 785,839 | 7.858 | 20 | 20 | fits | 134,155 | 57 | 0.672 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 1,088,673 | 10.887 | 20 | 20 | fits | 40,664 | 16 | 0.747 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 585,673 | 5.857 | 20 | 20 | fits | 155,084 | 208 | 0.256 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 481,054 | 4.811 | 20 | 200 | fits | 151,294 | 121 | 0.482 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 635,522 | 6.355 | 20 | 200 | fits | 155,084 | 208 | 0.256 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 481,978 | 4.820 | 20 | 20 | fits | 151,294 | 121 | 0.482 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 770,381 | 7.704 | 20 | 20 | fits | 134,155 | 57 | 0.672 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 179,761 | 1.798 | 20 | 24 | fits | 149,961 | 109 | 0.441 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 484,628 | 4.846 | 20 | 24 | fits | 151,294 | 121 | 0.482 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 484,562 | 4.846 | 20 | 50 | fits | 151,294 | 121 | 0.482 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 639,250 | 6.393 | 20 | 50 | fits | 155,084 | 208 | 0.256 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 773,339 | 7.733 | 20 | 20 | fits | 134,155 | 57 | 0.672 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 1,076,173 | 10.762 | 20 | 20 | fits | 40,664 | 16 | 0.747 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 573,173 | 5.732 | 20 | 20 | fits | 155,084 | 208 | 0.256 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 468,554 | 4.686 | 20 | 200 | fits | 151,294 | 121 | 0.482 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 623,022 | 6.230 | 20 | 200 | fits | 155,084 | 208 | 0.256 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 469,478 | 4.695 | 20 | 20 | fits | 151,294 | 121 | 0.482 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 757,881 | 7.579 | 20 | 20 | fits | 134,155 | 57 | 0.672 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 167,261 | 1.673 | 20 | 24 | fits | 149,961 | 109 | 0.441 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 472,128 | 4.721 | 20 | 24 | fits | 151,294 | 121 | 0.482 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 472,062 | 4.721 | 20 | 50 | fits | 151,294 | 121 | 0.482 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 626,750 | 6.268 | 20 | 50 | fits | 155,084 | 208 | 0.256 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 760,839 | 7.608 | 20 | 20 | fits | 134,155 | 57 | 0.672 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 1,063,673 | 10.637 | 20 | 20 | fits | 40,664 | 16 | 0.747 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 560,673 | 5.607 | 20 | 20 | fits | 155,084 | 208 | 0.256 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 456,054 | 4.561 | 20 | 200 | fits | 151,294 | 121 | 0.482 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 610,522 | 6.105 | 20 | 200 | fits | 155,084 | 208 | 0.256 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 456,978 | 4.570 | 20 | 20 | fits | 151,294 | 121 | 0.482 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 745,381 | 7.454 | 20 | 20 | fits | 134,155 | 57 | 0.672 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 154,761 | 1.548 | 20 | 24 | fits | 149,961 | 109 | 0.441 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 459,628 | 4.596 | 20 | 24 | fits | 151,294 | 121 | 0.482 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 459,562 | 4.596 | 20 | 50 | fits | 151,294 | 121 | 0.482 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 614,250 | 6.143 | 20 | 50 | fits | 155,084 | 208 | 0.256 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 748,339 | 7.483 | 20 | 20 | fits | 134,155 | 57 | 0.672 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 1,051,173 | 10.512 | 20 | 20 | fits | 40,664 | 16 | 0.747 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 597,632 | 5.976 | 20 | 20 | fits | 154,932 | 209 | 0.253 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 492,894 | 4.929 | 20 | 200 | fits | 148,743 | 115 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 647,210 | 6.472 | 20 | 200 | fits | 154,932 | 209 | 0.253 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 493,818 | 4.938 | 20 | 20 | fits | 148,743 | 115 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 780,851 | 7.809 | 20 | 20 | fits | 132,937 | 56 | 0.717 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 203,850 | 2.038 | 20 | 24 | fits | 149,493 | 109 | 0.432 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 496,468 | 4.965 | 20 | 24 | fits | 148,743 | 115 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 496,402 | 4.964 | 20 | 50 | fits | 148,743 | 115 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 650,938 | 6.509 | 20 | 50 | fits | 154,932 | 209 | 0.253 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 783,809 | 7.838 | 20 | 20 | fits | 132,937 | 56 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 1,102,383 | 11.024 | 20 | 20 | fits | 50,735 | 20 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 572,632 | 5.726 | 20 | 20 | fits | 154,932 | 209 | 0.253 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 467,894 | 4.679 | 20 | 200 | fits | 148,743 | 115 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 622,210 | 6.222 | 20 | 200 | fits | 154,932 | 209 | 0.253 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 468,818 | 4.688 | 20 | 20 | fits | 148,743 | 115 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 755,851 | 7.559 | 20 | 20 | fits | 132,937 | 56 | 0.717 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 178,850 | 1.788 | 20 | 24 | fits | 149,493 | 109 | 0.432 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 471,468 | 4.715 | 20 | 24 | fits | 148,743 | 115 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 471,402 | 4.714 | 20 | 50 | fits | 148,743 | 115 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 625,938 | 6.259 | 20 | 50 | fits | 154,932 | 209 | 0.253 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 758,809 | 7.588 | 20 | 20 | fits | 132,937 | 56 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 1,077,383 | 10.774 | 20 | 20 | fits | 50,735 | 20 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 547,632 | 5.476 | 20 | 20 | fits | 154,932 | 209 | 0.253 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 442,894 | 4.429 | 20 | 200 | fits | 148,743 | 115 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 597,210 | 5.972 | 20 | 200 | fits | 154,932 | 209 | 0.253 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 443,818 | 4.438 | 20 | 20 | fits | 148,743 | 115 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 730,851 | 7.309 | 20 | 20 | fits | 132,937 | 56 | 0.717 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 153,850 | 1.538 | 20 | 24 | fits | 149,493 | 109 | 0.432 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 446,468 | 4.465 | 20 | 24 | fits | 148,743 | 115 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 446,402 | 4.464 | 20 | 50 | fits | 148,743 | 115 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 600,938 | 6.009 | 20 | 50 | fits | 154,932 | 209 | 0.253 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 733,809 | 7.338 | 20 | 20 | fits | 132,937 | 56 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 1,052,383 | 10.524 | 20 | 20 | fits | 50,735 | 20 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 534,793 | 5.348 | 20 | 20 | fits | 146,729 | 188 | 0.256 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 438,954 | 4.390 | 20 | 200 | fits | 149,699 | 131 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 585,067 | 5.851 | 20 | 200 | fits | 146,729 | 188 | 0.256 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 439,878 | 4.399 | 20 | 20 | fits | 149,699 | 131 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 718,309 | 7.183 | 20 | 20 | fits | 132,538 | 62 | 0.687 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 148,903 | 1.489 | 20 | 24 | fits | 149,344 | 109 | 0.435 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 442,528 | 4.425 | 20 | 24 | fits | 149,699 | 131 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 442,462 | 4.425 | 20 | 50 | fits | 149,699 | 131 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 588,795 | 5.888 | 20 | 50 | fits | 146,729 | 188 | 0.256 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 721,267 | 7.213 | 20 | 20 | fits | 132,538 | 62 | 0.687 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 1,049,963 | 10.500 | 20 | 20 | fits | 60,892 | 24 | 0.686 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 603,384 | 6.034 | 20 | 20 | fits | 146,953 | 188 | 0.261 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 508,193 | 5.082 | 20 | 200 | fits | 149,765 | 131 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 654,530 | 6.545 | 20 | 200 | fits | 146,953 | 188 | 0.261 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 509,117 | 5.091 | 20 | 20 | fits | 149,765 | 131 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 801,678 | 8.017 | 20 | 20 | fits | 135,872 | 68 | 0.698 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 218,127 | 2.181 | 20 | 24 | fits | 149,461 | 109 | 0.433 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 511,767 | 5.118 | 20 | 24 | fits | 149,765 | 131 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 511,701 | 5.117 | 20 | 50 | fits | 149,765 | 131 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 658,258 | 6.583 | 20 | 50 | fits | 146,953 | 188 | 0.261 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 804,636 | 8.046 | 20 | 20 | fits | 135,872 | 68 | 0.698 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 1,117,857 | 11.179 | 20 | 20 | fits | 50,794 | 20 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 578,384 | 5.784 | 20 | 20 | fits | 146,953 | 188 | 0.261 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 483,193 | 4.832 | 20 | 200 | fits | 149,765 | 131 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 629,530 | 6.295 | 20 | 200 | fits | 146,953 | 188 | 0.261 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 484,117 | 4.841 | 20 | 20 | fits | 149,765 | 131 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 776,678 | 7.767 | 20 | 20 | fits | 135,872 | 68 | 0.698 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 193,127 | 1.931 | 20 | 24 | fits | 149,461 | 109 | 0.433 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 486,767 | 4.868 | 20 | 24 | fits | 149,765 | 131 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 486,701 | 4.867 | 20 | 50 | fits | 149,765 | 131 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 633,258 | 6.333 | 20 | 50 | fits | 146,953 | 188 | 0.261 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 779,636 | 7.796 | 20 | 20 | fits | 135,872 | 68 | 0.698 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 1,092,857 | 10.929 | 20 | 20 | fits | 50,794 | 20 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 553,384 | 5.534 | 20 | 20 | fits | 146,953 | 188 | 0.261 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 458,193 | 4.582 | 20 | 200 | fits | 149,765 | 131 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 604,530 | 6.045 | 20 | 200 | fits | 146,953 | 188 | 0.261 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 459,117 | 4.591 | 20 | 20 | fits | 149,765 | 131 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 751,678 | 7.517 | 20 | 20 | fits | 135,872 | 68 | 0.698 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 168,127 | 1.681 | 20 | 24 | fits | 149,461 | 109 | 0.433 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 461,767 | 4.618 | 20 | 24 | fits | 149,765 | 131 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 461,701 | 4.617 | 20 | 50 | fits | 149,765 | 131 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 608,258 | 6.083 | 20 | 50 | fits | 146,953 | 188 | 0.261 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 754,636 | 7.546 | 20 | 20 | fits | 135,872 | 68 | 0.698 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 1,067,857 | 10.679 | 20 | 20 | fits | 50,794 | 20 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 545,941 | 5.459 | 20 | 20 | fits | 152,733 | 202 | 0.314 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 453,345 | 4.533 | 20 | 200 | fits | 150,024 | 119 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 605,462 | 6.055 | 20 | 200 | fits | 152,733 | 202 | 0.314 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 454,269 | 4.543 | 20 | 20 | fits | 150,024 | 119 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 745,639 | 7.456 | 20 | 20 | fits | 128,870 | 60 | 0.706 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 162,969 | 1.630 | 20 | 24 | fits | 149,344 | 109 | 0.435 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 456,919 | 4.569 | 20 | 24 | fits | 150,024 | 119 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 456,853 | 4.569 | 20 | 50 | fits | 150,024 | 119 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 609,190 | 6.092 | 20 | 50 | fits | 152,733 | 202 | 0.314 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 748,597 | 7.486 | 20 | 20 | fits | 128,870 | 60 | 0.706 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 1,061,811 | 10.618 | 20 | 20 | fits | 50,812 | 20 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 559,856 | 5.599 | 20 | 20 | fits | 149,656 | 202 | 0.349 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 443,133 | 4.431 | 20 | 200 | fits | 149,996 | 120 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 602,710 | 6.027 | 20 | 200 | fits | 149,656 | 202 | 0.349 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 444,057 | 4.441 | 20 | 20 | fits | 149,996 | 120 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 737,974 | 7.380 | 20 | 20 | fits | 134,560 | 57 | 0.675 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 151,487 | 1.515 | 20 | 24 | fits | 152,818 | 109 | 0.441 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 446,707 | 4.467 | 20 | 24 | fits | 149,996 | 120 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 446,641 | 4.466 | 20 | 50 | fits | 149,996 | 120 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 606,438 | 6.064 | 20 | 50 | fits | 149,656 | 202 | 0.349 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 740,932 | 7.409 | 20 | 20 | fits | 134,560 | 57 | 0.675 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,049,297 | 10.493 | 20 | 20 | fits | 45,975 | 22 | 0.777 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 559,856 | 5.599 | 20 | 20 | fits | 149,656 | 202 | 0.349 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 443,133 | 4.431 | 20 | 200 | fits | 149,996 | 120 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 602,710 | 6.027 | 20 | 200 | fits | 149,656 | 202 | 0.349 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 444,057 | 4.441 | 20 | 20 | fits | 149,996 | 120 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 737,974 | 7.380 | 20 | 20 | fits | 134,560 | 57 | 0.675 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 151,487 | 1.515 | 20 | 24 | fits | 152,818 | 109 | 0.441 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 446,707 | 4.467 | 20 | 24 | fits | 149,996 | 120 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 446,641 | 4.466 | 20 | 50 | fits | 149,996 | 120 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 606,438 | 6.064 | 20 | 50 | fits | 149,656 | 202 | 0.349 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 740,932 | 7.409 | 20 | 20 | fits | 134,560 | 57 | 0.675 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 1,049,297 | 10.493 | 20 | 20 | fits | 45,975 | 22 | 0.777 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 563,762 | 5.638 | 20 | 20 | fits | 150,365 | 206 | 0.336 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 444,043 | 4.440 | 20 | 200 | fits | 148,827 | 116 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 604,407 | 6.044 | 20 | 200 | fits | 150,365 | 206 | 0.336 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 444,967 | 4.450 | 20 | 20 | fits | 148,827 | 116 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 739,560 | 7.396 | 20 | 20 | fits | 134,449 | 57 | 0.674 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 154,883 | 1.549 | 20 | 24 | fits | 148,884 | 109 | 0.427 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 447,617 | 4.476 | 20 | 24 | fits | 148,827 | 116 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 447,551 | 4.476 | 20 | 50 | fits | 148,827 | 116 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 608,135 | 6.081 | 20 | 50 | fits | 150,365 | 206 | 0.336 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 742,518 | 7.425 | 20 | 20 | fits | 134,449 | 57 | 0.674 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 1,050,772 | 10.508 | 20 | 20 | fits | 45,987 | 22 | 0.776 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 635,276 | 6.353 | 20 | 20 | fits | 151,864 | 193 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 523,985 | 5.240 | 20 | 200 | fits | 149,917 | 132 | 0.432 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 686,004 | 6.860 | 20 | 200 | fits | 151,864 | 193 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 524,909 | 5.249 | 20 | 20 | fits | 149,917 | 132 | 0.432 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 821,021 | 8.210 | 20 | 20 | fits | 134,313 | 57 | 0.673 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 233,767 | 2.338 | 20 | 24 | fits | 149,200 | 109 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 527,559 | 5.276 | 20 | 24 | fits | 149,917 | 132 | 0.432 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 527,493 | 5.275 | 20 | 50 | fits | 149,917 | 132 | 0.432 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 689,732 | 6.897 | 20 | 50 | fits | 151,864 | 193 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 823,979 | 8.240 | 20 | 20 | fits | 134,313 | 57 | 0.673 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 1,132,392 | 11.324 | 20 | 20 | fits | 50,843 | 20 | 0.714 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 622,776 | 6.228 | 20 | 20 | fits | 151,864 | 193 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 511,485 | 5.115 | 20 | 200 | fits | 149,917 | 132 | 0.432 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 673,504 | 6.735 | 20 | 200 | fits | 151,864 | 193 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 512,409 | 5.124 | 20 | 20 | fits | 149,917 | 132 | 0.432 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 808,521 | 8.085 | 20 | 20 | fits | 134,313 | 57 | 0.673 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 221,267 | 2.213 | 20 | 24 | fits | 149,200 | 109 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 515,059 | 5.151 | 20 | 24 | fits | 149,917 | 132 | 0.432 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 514,993 | 5.150 | 20 | 50 | fits | 149,917 | 132 | 0.432 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 677,232 | 6.772 | 20 | 50 | fits | 151,864 | 193 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 811,479 | 8.115 | 20 | 20 | fits | 134,313 | 57 | 0.673 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 1,119,892 | 11.199 | 20 | 20 | fits | 50,843 | 20 | 0.714 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 610,276 | 6.103 | 20 | 20 | fits | 151,864 | 193 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 498,985 | 4.990 | 20 | 200 | fits | 149,917 | 132 | 0.432 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 661,004 | 6.610 | 20 | 200 | fits | 151,864 | 193 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 499,909 | 4.999 | 20 | 20 | fits | 149,917 | 132 | 0.432 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 796,021 | 7.960 | 20 | 20 | fits | 134,313 | 57 | 0.673 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 208,767 | 2.088 | 20 | 24 | fits | 149,200 | 109 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 502,559 | 5.026 | 20 | 24 | fits | 149,917 | 132 | 0.432 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 502,493 | 5.025 | 20 | 50 | fits | 149,917 | 132 | 0.432 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 664,732 | 6.647 | 20 | 50 | fits | 151,864 | 193 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 798,979 | 7.990 | 20 | 20 | fits | 134,313 | 57 | 0.673 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 1,107,392 | 11.074 | 20 | 20 | fits | 50,843 | 20 | 0.714 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 597,776 | 5.978 | 20 | 20 | fits | 151,864 | 193 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 486,485 | 4.865 | 20 | 200 | fits | 149,917 | 132 | 0.432 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 648,504 | 6.485 | 20 | 200 | fits | 151,864 | 193 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 487,409 | 4.874 | 20 | 20 | fits | 149,917 | 132 | 0.432 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 783,521 | 7.835 | 20 | 20 | fits | 134,313 | 57 | 0.673 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 196,267 | 1.963 | 20 | 24 | fits | 149,200 | 109 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 490,059 | 4.901 | 20 | 24 | fits | 149,917 | 132 | 0.432 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 489,993 | 4.900 | 20 | 50 | fits | 149,917 | 132 | 0.432 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 652,232 | 6.522 | 20 | 50 | fits | 151,864 | 193 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 786,479 | 7.865 | 20 | 20 | fits | 134,313 | 57 | 0.673 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 1,094,892 | 10.949 | 20 | 20 | fits | 50,843 | 20 | 0.714 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 585,276 | 5.853 | 20 | 20 | fits | 151,864 | 193 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 473,985 | 4.740 | 20 | 200 | fits | 149,917 | 132 | 0.432 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 636,004 | 6.360 | 20 | 200 | fits | 151,864 | 193 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 474,909 | 4.749 | 20 | 20 | fits | 149,917 | 132 | 0.432 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 771,021 | 7.710 | 20 | 20 | fits | 134,313 | 57 | 0.673 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 183,767 | 1.838 | 20 | 24 | fits | 149,200 | 109 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 477,559 | 4.776 | 20 | 24 | fits | 149,917 | 132 | 0.432 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 477,493 | 4.775 | 20 | 50 | fits | 149,917 | 132 | 0.432 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 639,732 | 6.397 | 20 | 50 | fits | 151,864 | 193 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 773,979 | 7.740 | 20 | 20 | fits | 134,313 | 57 | 0.673 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 1,082,392 | 10.824 | 20 | 20 | fits | 50,843 | 20 | 0.714 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 541,370 | 5.414 | 20 | 20 | fits | 153,568 | 204 | 0.258 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 439,909 | 4.399 | 20 | 200 | fits | 150,224 | 119 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 592,861 | 5.929 | 20 | 200 | fits | 153,568 | 204 | 0.258 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 440,833 | 4.408 | 20 | 20 | fits | 150,224 | 119 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 728,753 | 7.288 | 20 | 20 | fits | 135,188 | 52 | 0.706 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 149,371 | 1.494 | 20 | 24 | fits | 148,045 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 443,483 | 4.435 | 20 | 24 | fits | 150,224 | 119 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 443,417 | 4.434 | 20 | 50 | fits | 150,224 | 119 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 596,589 | 5.966 | 20 | 50 | fits | 153,568 | 204 | 0.258 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 731,711 | 7.317 | 20 | 20 | fits | 135,188 | 52 | 0.706 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 1,044,870 | 10.449 | 20 | 20 | fits | 45,179 | 22 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 533,330 | 5.333 | 20 | 20 | fits | 154,015 | 206 | 0.262 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 449,308 | 4.493 | 20 | 200 | fits | 150,321 | 119 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 602,707 | 6.027 | 20 | 200 | fits | 154,015 | 206 | 0.262 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 450,232 | 4.502 | 20 | 20 | fits | 150,321 | 119 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 743,526 | 7.435 | 20 | 20 | fits | 129,512 | 54 | 0.738 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 158,673 | 1.587 | 20 | 24 | fits | 148,045 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 452,882 | 4.529 | 20 | 24 | fits | 150,321 | 119 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 452,816 | 4.528 | 20 | 50 | fits | 150,321 | 119 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 606,435 | 6.064 | 20 | 50 | fits | 154,015 | 206 | 0.262 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 746,484 | 7.465 | 20 | 20 | fits | 129,512 | 54 | 0.738 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 1,132,558 | 11.326 | 20 | 20 | fits | 51,832 | 21 | 0.731 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 554,641 | 5.546 | 20 | 20 | fits | 151,689 | 193 | 0.330 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 443,478 | 4.435 | 20 | 200 | fits | 150,050 | 132 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 605,393 | 6.054 | 20 | 200 | fits | 151,689 | 193 | 0.330 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 444,402 | 4.444 | 20 | 20 | fits | 150,050 | 132 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 740,503 | 7.405 | 20 | 20 | fits | 134,406 | 57 | 0.674 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 153,114 | 1.531 | 20 | 24 | fits | 148,045 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 447,052 | 4.471 | 20 | 24 | fits | 150,050 | 132 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 446,986 | 4.470 | 20 | 50 | fits | 150,050 | 132 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 609,121 | 6.091 | 20 | 50 | fits | 151,689 | 193 | 0.330 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 743,461 | 7.435 | 20 | 20 | fits | 134,406 | 57 | 0.674 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,129,898 | 11.299 | 20 | 20 | fits | 50,884 | 20 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 551,705 | 5.517 | 20 | 20 | fits | 153,720 | 204 | 0.260 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 450,232 | 4.502 | 20 | 200 | fits | 153,210 | 125 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 603,336 | 6.033 | 20 | 200 | fits | 153,720 | 204 | 0.260 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 451,156 | 4.512 | 20 | 20 | fits | 153,210 | 125 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 737,025 | 7.370 | 20 | 20 | fits | 132,985 | 55 | 0.719 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 146,508 | 1.465 | 20 | 24 | fits | 148,045 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 453,806 | 4.538 | 20 | 24 | fits | 153,210 | 125 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 453,740 | 4.537 | 20 | 50 | fits | 153,210 | 125 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 607,064 | 6.071 | 20 | 50 | fits | 153,720 | 204 | 0.260 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 739,983 | 7.400 | 20 | 20 | fits | 132,985 | 55 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,136,420 | 11.364 | 20 | 20 | fits | 45,442 | 23 | 0.806 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 551,352 | 5.514 | 20 | 20 | fits | 152,544 | 201 | 0.312 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 458,926 | 4.589 | 20 | 200 | fits | 150,261 | 119 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 610,854 | 6.109 | 20 | 200 | fits | 152,544 | 201 | 0.312 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 459,850 | 4.598 | 20 | 20 | fits | 150,261 | 119 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 823,943 | 8.239 | 20 | 20 | fits | 135,482 | 58 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 156,806 | 1.568 | 20 | 24 | fits | 148,073 | 107 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 462,500 | 4.625 | 20 | 24 | fits | 150,261 | 119 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 462,434 | 4.624 | 20 | 50 | fits | 150,261 | 119 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 614,582 | 6.146 | 20 | 50 | fits | 152,544 | 201 | 0.312 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 826,901 | 8.269 | 20 | 20 | fits | 135,482 | 58 | 0.679 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,146,297 | 11.463 | 20 | 20 | fits | 51,061 | 20 | 0.718 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 556,807 | 5.568 | 20 | 20 | fits | 154,511 | 192 | 0.292 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 452,865 | 4.529 | 20 | 200 | fits | 149,839 | 131 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 606,760 | 6.068 | 20 | 200 | fits | 154,511 | 192 | 0.292 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 453,789 | 4.538 | 20 | 20 | fits | 149,839 | 131 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 819,739 | 8.197 | 20 | 20 | fits | 135,403 | 58 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 151,162 | 1.512 | 20 | 24 | fits | 147,988 | 107 | 0.418 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 456,439 | 4.564 | 20 | 24 | fits | 149,839 | 131 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 456,373 | 4.564 | 20 | 50 | fits | 149,839 | 131 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 610,488 | 6.105 | 20 | 50 | fits | 154,511 | 192 | 0.292 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 822,697 | 8.227 | 20 | 20 | fits | 135,403 | 58 | 0.680 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,142,104 | 11.421 | 20 | 20 | fits | 51,057 | 20 | 0.718 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 638,136 | 6.381 | 20 | 20 | fits | 155,263 | 207 | 0.266 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 448,078 | 4.481 | 20 | 200 | fits | 148,031 | 114 | 0.469 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 679,532 | 6.795 | 20 | 200 | fits | 155,263 | 207 | 0.266 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 449,002 | 4.490 | 20 | 20 | fits | 148,031 | 114 | 0.469 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 814,879 | 8.149 | 20 | 20 | fits | 134,643 | 58 | 0.674 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 159,740 | 1.597 | 20 | 24 | fits | 148,045 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 451,652 | 4.517 | 20 | 24 | fits | 148,031 | 114 | 0.469 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 451,586 | 4.516 | 20 | 50 | fits | 148,031 | 114 | 0.469 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 683,260 | 6.833 | 20 | 50 | fits | 155,263 | 207 | 0.266 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 817,837 | 8.178 | 20 | 20 | fits | 134,643 | 58 | 0.674 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,136,307 | 11.363 | 20 | 20 | fits | 50,656 | 20 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 620,517 | 6.205 | 20 | 20 | fits | 147,002 | 188 | 0.262 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 525,339 | 5.253 | 20 | 200 | fits | 149,968 | 131 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 671,725 | 6.717 | 20 | 200 | fits | 147,002 | 188 | 0.262 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 526,263 | 5.263 | 20 | 20 | fits | 149,968 | 131 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 811,671 | 8.117 | 20 | 20 | fits | 128,670 | 60 | 0.705 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 154,102 | 1.541 | 20 | 24 | fits | 148,045 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 528,913 | 5.289 | 20 | 24 | fits | 149,968 | 131 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 528,847 | 5.288 | 20 | 50 | fits | 149,968 | 131 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 675,453 | 6.755 | 20 | 50 | fits | 147,002 | 188 | 0.262 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 814,629 | 8.146 | 20 | 20 | fits | 128,670 | 60 | 0.705 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,132,898 | 11.329 | 20 | 20 | fits | 55,972 | 26 | 0.742 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 551,467 | 5.515 | 20 | 20 | fits | 153,574 | 204 | 0.258 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 450,062 | 4.501 | 20 | 200 | fits | 150,164 | 119 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 603,020 | 6.030 | 20 | 200 | fits | 153,574 | 204 | 0.258 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 450,986 | 4.510 | 20 | 20 | fits | 150,164 | 119 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 738,630 | 7.386 | 20 | 20 | fits | 134,906 | 51 | 0.705 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 148,039 | 1.480 | 20 | 24 | fits | 148,101 | 107 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 453,636 | 4.536 | 20 | 24 | fits | 150,164 | 119 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 453,570 | 4.536 | 20 | 50 | fits | 150,164 | 119 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 606,748 | 6.067 | 20 | 50 | fits | 153,574 | 204 | 0.258 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 741,588 | 7.416 | 20 | 20 | fits | 134,906 | 51 | 0.705 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 1,054,102 | 10.541 | 20 | 20 | fits | 39,485 | 25 | 0.833 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 542,065 | 5.421 | 20 | 20 | fits | 146,859 | 187 | 0.262 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 446,887 | 4.469 | 20 | 200 | fits | 150,076 | 131 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 593,130 | 5.931 | 20 | 200 | fits | 146,859 | 187 | 0.262 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 447,811 | 4.478 | 20 | 20 | fits | 150,076 | 131 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 728,293 | 7.283 | 20 | 20 | fits | 134,459 | 58 | 0.675 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 156,504 | 1.565 | 20 | 24 | fits | 148,045 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 450,461 | 4.505 | 20 | 24 | fits | 150,076 | 131 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 450,395 | 4.504 | 20 | 50 | fits | 150,076 | 131 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 596,858 | 5.969 | 20 | 50 | fits | 146,859 | 187 | 0.262 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 731,251 | 7.313 | 20 | 20 | fits | 134,459 | 58 | 0.675 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 1,054,848 | 10.548 | 20 | 20 | fits | 60,904 | 24 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 544,962 | 5.450 | 20 | 20 | fits | 155,096 | 210 | 0.254 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 440,342 | 4.403 | 20 | 200 | fits | 149,090 | 115 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 594,822 | 5.948 | 20 | 200 | fits | 155,096 | 210 | 0.254 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 441,266 | 4.413 | 20 | 20 | fits | 149,090 | 115 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 735,439 | 7.354 | 20 | 20 | fits | 129,341 | 54 | 0.735 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 150,945 | 1.509 | 20 | 24 | fits | 148,045 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 443,916 | 4.439 | 20 | 24 | fits | 149,090 | 115 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 443,850 | 4.439 | 20 | 50 | fits | 149,090 | 115 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 598,550 | 5.986 | 20 | 50 | fits | 155,096 | 210 | 0.254 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 738,397 | 7.384 | 20 | 20 | fits | 129,341 | 54 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 1,046,499 | 10.465 | 20 | 20 | fits | 50,795 | 20 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 530,565 | 5.306 | 20 | 20 | fits | 155,608 | 193 | 0.263 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 446,457 | 4.465 | 20 | 200 | fits | 146,945 | 175 | 0.400 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 601,449 | 6.014 | 20 | 200 | fits | 155,608 | 193 | 0.263 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 447,381 | 4.474 | 20 | 20 | fits | 146,945 | 175 | 0.400 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 602,153 | 6.022 | 20 | 20 | fits | 155,608 | 193 | 0.263 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 158,213 | 1.582 | 20 | 24 | fits | 160,951 | 74 | 0.438 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 450,031 | 4.500 | 20 | 24 | fits | 146,945 | 175 | 0.400 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 449,965 | 4.500 | 20 | 50 | fits | 146,945 | 175 | 0.400 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 605,177 | 6.052 | 20 | 50 | fits | 155,608 | 193 | 0.263 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 748,003 | 7.480 | 20 | 20 | fits | 132,289 | 57 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 1,040,643 | 10.406 | 20 | 20 | fits | 30,430 | 12 | 0.798 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 562,777 | 5.628 | 20 | 20 | fits | 149,441 | 190 | 0.363 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 445,053 | 4.451 | 20 | 200 | fits | 150,137 | 132 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 604,720 | 6.047 | 20 | 200 | fits | 149,441 | 190 | 0.363 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 445,977 | 4.460 | 20 | 20 | fits | 150,137 | 132 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 739,391 | 7.394 | 20 | 20 | fits | 133,967 | 62 | 0.641 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 154,609 | 1.546 | 20 | 24 | fits | 148,045 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 448,627 | 4.486 | 20 | 24 | fits | 150,137 | 132 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 448,561 | 4.486 | 20 | 50 | fits | 150,137 | 132 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 608,448 | 6.084 | 20 | 50 | fits | 149,441 | 190 | 0.363 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 742,349 | 7.423 | 20 | 20 | fits | 133,967 | 62 | 0.641 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 1,055,388 | 10.554 | 20 | 20 | fits | 50,794 | 20 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 563,786 | 5.638 | 20 | 20 | fits | 153,580 | 205 | 0.305 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 450,761 | 4.508 | 20 | 200 | fits | 152,441 | 122 | 0.451 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 603,725 | 6.037 | 20 | 200 | fits | 153,580 | 205 | 0.305 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 451,685 | 4.517 | 20 | 20 | fits | 152,441 | 122 | 0.451 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 738,827 | 7.388 | 20 | 20 | fits | 134,398 | 57 | 0.673 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 149,050 | 1.490 | 20 | 24 | fits | 148,045 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 454,335 | 4.543 | 20 | 24 | fits | 152,441 | 122 | 0.451 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 454,269 | 4.543 | 20 | 50 | fits | 152,441 | 122 | 0.451 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 607,453 | 6.075 | 20 | 50 | fits | 153,580 | 205 | 0.305 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 741,785 | 7.418 | 20 | 20 | fits | 134,398 | 57 | 0.673 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 1,044,743 | 10.447 | 20 | 20 | fits | 40,728 | 17 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 571,036 | 5.710 | 20 | 20 | fits | 154,500 | 206 | 0.253 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 458,406 | 4.584 | 20 | 200 | fits | 148,267 | 114 | 0.470 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 612,290 | 6.123 | 20 | 200 | fits | 154,500 | 206 | 0.253 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 459,330 | 4.593 | 20 | 20 | fits | 148,267 | 114 | 0.470 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 747,417 | 7.474 | 20 | 20 | fits | 134,423 | 57 | 0.674 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 158,362 | 1.584 | 20 | 24 | fits | 148,055 | 107 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 461,980 | 4.620 | 20 | 24 | fits | 148,267 | 114 | 0.470 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 461,914 | 4.619 | 20 | 50 | fits | 148,267 | 114 | 0.470 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 616,018 | 6.160 | 20 | 50 | fits | 154,500 | 206 | 0.253 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 750,375 | 7.504 | 20 | 20 | fits | 134,423 | 57 | 0.674 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 1,069,260 | 10.693 | 20 | 20 | fits | 45,789 | 23 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 542,350 | 5.423 | 20 | 20 | fits | 146,736 | 188 | 0.256 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 446,581 | 4.466 | 20 | 200 | fits | 149,919 | 131 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 592,701 | 5.927 | 20 | 200 | fits | 146,736 | 188 | 0.256 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 447,505 | 4.475 | 20 | 20 | fits | 149,919 | 131 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 727,993 | 7.280 | 20 | 20 | fits | 134,588 | 57 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 151,800 | 1.518 | 20 | 24 | fits | 148,079 | 106 | 0.422 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 450,155 | 4.502 | 20 | 24 | fits | 149,919 | 131 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 450,089 | 4.501 | 20 | 50 | fits | 149,919 | 131 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 596,429 | 5.964 | 20 | 50 | fits | 146,736 | 188 | 0.256 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 730,951 | 7.310 | 20 | 20 | fits | 134,588 | 57 | 0.677 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 1,049,857 | 10.499 | 20 | 20 | fits | 50,924 | 20 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 556,286 | 5.563 | 20 | 20 | fits | 146,731 | 188 | 0.256 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 460,522 | 4.605 | 20 | 200 | fits | 149,965 | 131 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 606,637 | 6.066 | 20 | 200 | fits | 146,731 | 188 | 0.256 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 461,446 | 4.614 | 20 | 20 | fits | 149,965 | 131 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 741,537 | 7.415 | 20 | 20 | fits | 134,196 | 57 | 0.672 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 158,623 | 1.586 | 20 | 24 | fits | 148,049 | 107 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 464,096 | 4.641 | 20 | 24 | fits | 149,965 | 131 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 464,030 | 4.640 | 20 | 50 | fits | 149,965 | 131 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 610,365 | 6.104 | 20 | 50 | fits | 146,731 | 188 | 0.256 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 744,495 | 7.445 | 20 | 20 | fits | 134,196 | 57 | 0.672 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 1,067,577 | 10.676 | 20 | 20 | fits | 50,031 | 29 | 0.799 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 527,416 | 5.274 | 20 | 20 | fits | 153,872 | 205 | 0.262 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 443,394 | 4.434 | 20 | 200 | fits | 150,352 | 119 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 596,650 | 5.966 | 20 | 200 | fits | 153,872 | 205 | 0.262 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 444,318 | 4.443 | 20 | 20 | fits | 150,352 | 119 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 732,491 | 7.325 | 20 | 20 | fits | 135,137 | 52 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 152,728 | 1.527 | 20 | 24 | fits | 148,045 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 446,968 | 4.470 | 20 | 24 | fits | 150,352 | 119 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 446,902 | 4.469 | 20 | 50 | fits | 150,352 | 119 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 600,378 | 6.004 | 20 | 50 | fits | 153,872 | 205 | 0.262 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 735,449 | 7.354 | 20 | 20 | fits | 135,137 | 52 | 0.707 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 1,130,976 | 11.310 | 20 | 20 | fits | 52,327 | 21 | 0.736 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 533,692 | 5.337 | 20 | 20 | fits | 146,776 | 188 | 0.258 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 437,883 | 4.379 | 20 | 200 | fits | 150,008 | 131 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 584,043 | 5.840 | 20 | 200 | fits | 146,776 | 188 | 0.258 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 438,807 | 4.388 | 20 | 20 | fits | 150,008 | 131 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 712,096 | 7.121 | 20 | 20 | fits | 127,349 | 60 | 0.687 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 146,508 | 1.465 | 20 | 24 | fits | 148,045 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 441,457 | 4.415 | 20 | 24 | fits | 150,008 | 131 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 441,391 | 4.414 | 20 | 50 | fits | 150,008 | 131 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 587,771 | 5.878 | 20 | 50 | fits | 146,776 | 188 | 0.258 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 715,054 | 7.151 | 20 | 20 | fits | 127,349 | 60 | 0.687 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,129,274 | 11.293 | 20 | 20 | fits | 61,083 | 24 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 550,493 | 5.505 | 20 | 20 | fits | 155,034 | 210 | 0.253 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 445,873 | 4.459 | 20 | 200 | fits | 149,088 | 115 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 600,291 | 6.003 | 20 | 200 | fits | 155,034 | 210 | 0.253 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 446,797 | 4.468 | 20 | 20 | fits | 149,088 | 115 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 747,949 | 7.479 | 20 | 20 | fits | 136,382 | 62 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 156,471 | 1.565 | 20 | 24 | fits | 148,045 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 449,447 | 4.494 | 20 | 24 | fits | 149,088 | 115 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 449,381 | 4.494 | 20 | 50 | fits | 149,088 | 115 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 604,019 | 6.040 | 20 | 50 | fits | 155,034 | 210 | 0.253 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 750,907 | 7.509 | 20 | 20 | fits | 136,382 | 62 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,136,440 | 11.364 | 20 | 20 | fits | 40,651 | 16 | 0.747 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 548,375 | 5.484 | 20 | 20 | fits | 147,837 | 201 | 0.381 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 441,554 | 4.416 | 20 | 200 | fits | 150,407 | 120 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 599,523 | 5.995 | 20 | 200 | fits | 147,837 | 201 | 0.381 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 442,478 | 4.425 | 20 | 20 | fits | 150,407 | 120 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 816,290 | 8.163 | 20 | 20 | fits | 135,259 | 63 | 0.647 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 150,833 | 1.508 | 20 | 24 | fits | 148,045 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 445,128 | 4.451 | 20 | 24 | fits | 150,407 | 120 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 445,062 | 4.451 | 20 | 50 | fits | 150,407 | 120 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 603,251 | 6.033 | 20 | 50 | fits | 147,837 | 201 | 0.381 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 819,248 | 8.192 | 20 | 20 | fits | 135,259 | 63 | 0.647 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,132,283 | 11.323 | 20 | 20 | fits | 50,774 | 20 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 551,333 | 5.513 | 20 | 20 | fits | 154,636 | 190 | 0.315 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 457,376 | 4.574 | 20 | 200 | fits | 148,927 | 180 | 0.406 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 611,396 | 6.114 | 20 | 200 | fits | 154,636 | 190 | 0.315 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 458,300 | 4.583 | 20 | 20 | fits | 148,927 | 180 | 0.406 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 829,073 | 8.291 | 20 | 20 | fits | 136,169 | 52 | 0.710 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 158,180 | 1.582 | 20 | 24 | fits | 160,951 | 74 | 0.438 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 460,950 | 4.609 | 20 | 24 | fits | 148,927 | 180 | 0.406 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 460,884 | 4.609 | 20 | 50 | fits | 148,927 | 180 | 0.406 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 615,124 | 6.151 | 20 | 50 | fits | 154,636 | 190 | 0.315 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 832,031 | 8.320 | 20 | 20 | fits | 136,169 | 52 | 0.710 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,140,436 | 11.404 | 20 | 20 | fits | 35,276 | 19 | 0.844 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 651,003 | 6.510 | 20 | 20 | fits | 147,503 | 203 | 0.281 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 453,501 | 4.535 | 20 | 200 | fits | 147,160 | 110 | 0.482 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 681,035 | 6.810 | 20 | 200 | fits | 147,503 | 203 | 0.281 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 454,425 | 4.544 | 20 | 20 | fits | 147,160 | 110 | 0.482 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 815,949 | 8.159 | 20 | 20 | fits | 134,210 | 62 | 0.643 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 154,586 | 1.546 | 20 | 24 | fits | 148,055 | 107 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 457,075 | 4.571 | 20 | 24 | fits | 147,160 | 110 | 0.482 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 457,009 | 4.570 | 20 | 50 | fits | 147,160 | 110 | 0.482 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 684,763 | 6.848 | 20 | 50 | fits | 147,503 | 203 | 0.281 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 818,907 | 8.189 | 20 | 20 | fits | 134,210 | 62 | 0.643 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,148,073 | 11.481 | 20 | 20 | fits | 61,055 | 24 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 621,194 | 6.212 | 20 | 20 | fits | 156,303 | 208 | 0.276 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 435,888 | 4.359 | 20 | 200 | fits | 148,044 | 114 | 0.470 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 672,149 | 6.721 | 20 | 200 | fits | 156,303 | 208 | 0.276 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 436,812 | 4.368 | 20 | 20 | fits | 148,044 | 114 | 0.470 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 807,286 | 8.073 | 20 | 20 | fits | 134,433 | 58 | 0.675 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 146,542 | 1.465 | 20 | 24 | fits | 148,079 | 106 | 0.422 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 439,462 | 4.395 | 20 | 24 | fits | 148,044 | 114 | 0.470 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 439,396 | 4.394 | 20 | 50 | fits | 148,044 | 114 | 0.470 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 675,877 | 6.759 | 20 | 50 | fits | 156,303 | 208 | 0.276 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 810,244 | 8.102 | 20 | 20 | fits | 134,433 | 58 | 0.675 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,133,549 | 11.335 | 20 | 20 | fits | 55,464 | 26 | 0.734 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 563,138 | 5.631 | 20 | 20 | fits | 154,978 | 209 | 0.254 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 458,571 | 4.586 | 20 | 200 | fits | 152,439 | 122 | 0.451 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 612,933 | 6.129 | 20 | 200 | fits | 154,978 | 209 | 0.254 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 459,495 | 4.595 | 20 | 20 | fits | 152,439 | 122 | 0.451 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 748,393 | 7.484 | 20 | 20 | fits | 134,756 | 51 | 0.704 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 156,625 | 1.566 | 20 | 24 | fits | 148,045 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 462,145 | 4.621 | 20 | 24 | fits | 152,439 | 122 | 0.451 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 462,079 | 4.621 | 20 | 50 | fits | 152,439 | 122 | 0.451 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 616,661 | 6.167 | 20 | 50 | fits | 154,978 | 209 | 0.254 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 751,351 | 7.514 | 20 | 20 | fits | 134,756 | 51 | 0.704 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 1,049,438 | 10.494 | 20 | 20 | fits | 35,884 | 19 | 0.816 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 537,257 | 5.373 | 20 | 20 | fits | 153,878 | 205 | 0.262 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 453,291 | 4.533 | 20 | 200 | fits | 150,362 | 119 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 606,553 | 6.066 | 20 | 200 | fits | 153,878 | 205 | 0.262 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 454,215 | 4.542 | 20 | 20 | fits | 150,362 | 119 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 742,090 | 7.421 | 20 | 20 | fits | 134,833 | 51 | 0.705 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 151,070 | 1.511 | 20 | 24 | fits | 148,128 | 107 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 456,865 | 4.569 | 20 | 24 | fits | 150,362 | 119 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 456,799 | 4.568 | 20 | 50 | fits | 150,362 | 119 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 610,281 | 6.103 | 20 | 50 | fits | 153,878 | 205 | 0.262 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 745,048 | 7.450 | 20 | 20 | fits | 134,833 | 51 | 0.705 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 1,059,063 | 10.591 | 20 | 20 | fits | 45,658 | 23 | 0.807 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 534,050 | 5.340 | 20 | 20 | fits | 146,849 | 188 | 0.259 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 438,230 | 4.382 | 20 | 200 | fits | 151,878 | 137 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 584,463 | 5.845 | 20 | 200 | fits | 146,849 | 188 | 0.259 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 439,154 | 4.392 | 20 | 20 | fits | 151,878 | 137 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 719,415 | 7.194 | 20 | 20 | fits | 134,248 | 57 | 0.674 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 145,118 | 1.451 | 20 | 24 | fits | 149,724 | 111 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 441,804 | 4.418 | 20 | 24 | fits | 151,878 | 137 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 441,738 | 4.417 | 20 | 50 | fits | 151,878 | 137 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 588,191 | 5.882 | 20 | 50 | fits | 146,849 | 188 | 0.259 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 722,373 | 7.224 | 20 | 20 | fits | 134,248 | 57 | 0.674 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 1,046,886 | 10.469 | 20 | 20 | fits | 61,144 | 24 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 545,825 | 5.458 | 20 | 20 | fits | 153,630 | 204 | 0.259 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 444,364 | 4.444 | 20 | 200 | fits | 150,358 | 119 | 0.430 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 597,378 | 5.974 | 20 | 200 | fits | 153,630 | 204 | 0.259 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 445,288 | 4.453 | 20 | 20 | fits | 150,358 | 119 | 0.430 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 731,090 | 7.311 | 20 | 20 | fits | 133,008 | 56 | 0.719 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 153,699 | 1.537 | 20 | 24 | fits | 148,045 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 447,938 | 4.479 | 20 | 24 | fits | 150,358 | 119 | 0.430 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 447,872 | 4.479 | 20 | 50 | fits | 150,358 | 119 | 0.430 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 601,106 | 6.011 | 20 | 50 | fits | 153,630 | 204 | 0.259 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 734,048 | 7.340 | 20 | 20 | fits | 133,008 | 56 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 1,052,673 | 10.527 | 20 | 20 | fits | 50,656 | 20 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 542,047 | 5.420 | 20 | 20 | fits | 154,787 | 192 | 0.298 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 438,545 | 4.385 | 20 | 200 | fits | 150,177 | 131 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 592,716 | 5.927 | 20 | 200 | fits | 154,787 | 192 | 0.298 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 439,469 | 4.395 | 20 | 20 | fits | 150,177 | 131 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 732,734 | 7.327 | 20 | 20 | fits | 128,572 | 60 | 0.706 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 148,061 | 1.481 | 20 | 24 | fits | 148,045 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 442,119 | 4.421 | 20 | 24 | fits | 150,177 | 131 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 442,053 | 4.421 | 20 | 50 | fits | 150,177 | 131 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 596,444 | 5.964 | 20 | 50 | fits | 154,787 | 192 | 0.298 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 735,692 | 7.357 | 20 | 20 | fits | 128,572 | 60 | 0.706 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 1,048,833 | 10.488 | 20 | 20 | fits | 50,794 | 20 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 566,811 | 5.668 | 20 | 20 | fits | 149,669 | 190 | 0.363 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 447,924 | 4.479 | 20 | 200 | fits | 150,175 | 132 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 607,819 | 6.078 | 20 | 200 | fits | 149,669 | 190 | 0.363 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 448,848 | 4.488 | 20 | 20 | fits | 150,175 | 132 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 742,588 | 7.426 | 20 | 20 | fits | 134,065 | 62 | 0.642 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 157,442 | 1.574 | 20 | 24 | fits | 148,045 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 451,498 | 4.515 | 20 | 24 | fits | 150,175 | 132 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 451,432 | 4.514 | 20 | 50 | fits | 150,175 | 132 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 611,547 | 6.115 | 20 | 50 | fits | 149,669 | 190 | 0.363 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 745,546 | 7.455 | 20 | 20 | fits | 134,065 | 62 | 0.642 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 1,058,507 | 10.585 | 20 | 20 | fits | 50,808 | 20 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 565,045 | 5.650 | 20 | 20 | fits | 154,590 | 206 | 0.254 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 452,403 | 4.524 | 20 | 200 | fits | 151,302 | 121 | 0.483 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 606,377 | 6.064 | 20 | 200 | fits | 154,590 | 206 | 0.254 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 453,327 | 4.533 | 20 | 20 | fits | 151,302 | 121 | 0.483 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 741,361 | 7.414 | 20 | 20 | fits | 134,280 | 57 | 0.672 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 151,804 | 1.518 | 20 | 24 | fits | 148,045 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 455,977 | 4.560 | 20 | 24 | fits | 151,302 | 121 | 0.483 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 455,911 | 4.559 | 20 | 50 | fits | 151,302 | 121 | 0.483 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 610,105 | 6.101 | 20 | 50 | fits | 154,590 | 206 | 0.254 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 744,319 | 7.443 | 20 | 20 | fits | 134,280 | 57 | 0.672 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 1,047,156 | 10.472 | 20 | 20 | fits | 40,572 | 16 | 0.747 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 550,475 | 5.505 | 20 | 20 | fits | 154,843 | 207 | 0.255 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 446,948 | 4.469 | 20 | 200 | fits | 150,456 | 120 | 0.476 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 601,175 | 6.012 | 20 | 200 | fits | 154,843 | 207 | 0.255 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 447,872 | 4.479 | 20 | 20 | fits | 150,456 | 120 | 0.476 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 735,973 | 7.360 | 20 | 20 | fits | 134,094 | 57 | 0.673 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 146,166 | 1.462 | 20 | 24 | fits | 148,045 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 450,522 | 4.505 | 20 | 24 | fits | 150,456 | 120 | 0.476 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 450,456 | 4.505 | 20 | 50 | fits | 150,456 | 120 | 0.476 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 604,903 | 6.049 | 20 | 50 | fits | 154,843 | 207 | 0.255 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 738,931 | 7.389 | 20 | 20 | fits | 134,094 | 57 | 0.673 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 1,041,843 | 10.418 | 20 | 20 | fits | 40,650 | 16 | 0.747 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 551,360 | 5.514 | 20 | 20 | fits | 151,595 | 192 | 0.335 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 441,189 | 4.412 | 20 | 200 | fits | 152,407 | 138 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 602,923 | 6.029 | 20 | 200 | fits | 151,595 | 192 | 0.335 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 442,113 | 4.421 | 20 | 20 | fits | 152,407 | 138 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 737,776 | 7.378 | 20 | 20 | fits | 134,149 | 57 | 0.675 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 147,029 | 1.470 | 20 | 24 | fits | 152,688 | 111 | 0.462 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 444,763 | 4.448 | 20 | 24 | fits | 152,407 | 138 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 444,697 | 4.447 | 20 | 50 | fits | 152,407 | 138 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 606,651 | 6.067 | 20 | 50 | fits | 151,595 | 192 | 0.335 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 740,734 | 7.407 | 20 | 20 | fits | 134,149 | 57 | 0.675 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 1,049,646 | 10.496 | 20 | 20 | fits | 46,264 | 22 | 0.780 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 559,507 | 5.595 | 20 | 20 | fits | 149,832 | 203 | 0.348 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 443,063 | 4.431 | 20 | 200 | fits | 150,587 | 120 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 602,940 | 6.029 | 20 | 200 | fits | 149,832 | 203 | 0.348 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 443,987 | 4.440 | 20 | 20 | fits | 150,587 | 120 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 738,055 | 7.381 | 20 | 20 | fits | 134,411 | 57 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 152,013 | 1.520 | 20 | 24 | fits | 148,484 | 106 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 446,637 | 4.466 | 20 | 24 | fits | 150,587 | 120 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 446,571 | 4.466 | 20 | 50 | fits | 150,587 | 120 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 606,668 | 6.067 | 20 | 50 | fits | 149,832 | 203 | 0.348 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 741,013 | 7.410 | 20 | 20 | fits | 134,411 | 57 | 0.677 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 1,128,396 | 11.284 | 20 | 20 | fits | 51,956 | 21 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 545,295 | 5.453 | 20 | 20 | fits | 156,088 | 195 | 0.249 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 450,365 | 4.504 | 20 | 200 | fits | 153,149 | 137 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 605,837 | 6.058 | 20 | 200 | fits | 156,088 | 195 | 0.249 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 451,289 | 4.513 | 20 | 20 | fits | 153,149 | 137 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 741,105 | 7.411 | 20 | 20 | fits | 134,564 | 51 | 0.706 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 146,247 | 1.462 | 20 | 24 | fits | 148,484 | 106 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 453,939 | 4.539 | 20 | 24 | fits | 153,149 | 137 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 453,873 | 4.539 | 20 | 50 | fits | 153,149 | 137 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 609,565 | 6.096 | 20 | 50 | fits | 156,088 | 195 | 0.249 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 744,063 | 7.441 | 20 | 20 | fits | 134,564 | 51 | 0.706 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,121,838 | 11.218 | 20 | 20 | fits | 40,985 | 17 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 553,770 | 5.538 | 20 | 20 | fits | 146,712 | 188 | 0.258 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 458,128 | 4.581 | 20 | 200 | fits | 150,276 | 131 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 604,224 | 6.042 | 20 | 200 | fits | 146,712 | 188 | 0.258 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 459,052 | 4.591 | 20 | 20 | fits | 150,276 | 131 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 737,094 | 7.371 | 20 | 20 | fits | 132,166 | 61 | 0.688 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 155,540 | 1.555 | 20 | 24 | fits | 148,540 | 107 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 461,702 | 4.617 | 20 | 24 | fits | 150,276 | 131 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 461,636 | 4.616 | 20 | 50 | fits | 150,276 | 131 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 607,952 | 6.080 | 20 | 50 | fits | 146,712 | 188 | 0.258 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 740,052 | 7.401 | 20 | 20 | fits | 132,166 | 61 | 0.688 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,148,331 | 11.483 | 20 | 20 | fits | 61,132 | 24 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 534,366 | 5.344 | 20 | 20 | fits | 152,600 | 201 | 0.317 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 441,766 | 4.418 | 20 | 200 | fits | 150,483 | 119 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 593,750 | 5.938 | 20 | 200 | fits | 152,600 | 201 | 0.317 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 442,690 | 4.427 | 20 | 20 | fits | 150,483 | 119 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 807,634 | 8.076 | 20 | 20 | fits | 135,433 | 59 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 150,769 | 1.508 | 20 | 24 | fits | 148,283 | 106 | 0.421 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 445,340 | 4.453 | 20 | 24 | fits | 150,483 | 119 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 445,274 | 4.453 | 20 | 50 | fits | 150,483 | 119 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 597,478 | 5.975 | 20 | 50 | fits | 152,600 | 201 | 0.317 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 810,592 | 8.106 | 20 | 20 | fits | 135,433 | 59 | 0.679 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,129,912 | 11.299 | 20 | 20 | fits | 51,009 | 20 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 553,931 | 5.539 | 20 | 20 | fits | 154,338 | 191 | 0.295 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 450,768 | 4.508 | 20 | 200 | fits | 150,327 | 131 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 604,490 | 6.045 | 20 | 200 | fits | 154,338 | 191 | 0.295 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 451,692 | 4.517 | 20 | 20 | fits | 150,327 | 131 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 810,917 | 8.109 | 20 | 20 | fits | 128,007 | 61 | 0.690 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 159,927 | 1.599 | 20 | 24 | fits | 148,283 | 106 | 0.421 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 454,342 | 4.543 | 20 | 24 | fits | 150,327 | 131 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 454,276 | 4.543 | 20 | 50 | fits | 150,327 | 131 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 608,218 | 6.082 | 20 | 50 | fits | 154,338 | 191 | 0.295 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 813,875 | 8.139 | 20 | 20 | fits | 128,007 | 61 | 0.690 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,141,245 | 11.412 | 20 | 20 | fits | 61,127 | 24 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 638,846 | 6.388 | 20 | 20 | fits | 150,588 | 210 | 0.301 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 441,672 | 4.417 | 20 | 200 | fits | 146,918 | 110 | 0.479 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 669,244 | 6.692 | 20 | 200 | fits | 150,588 | 210 | 0.301 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 442,596 | 4.426 | 20 | 20 | fits | 146,918 | 110 | 0.479 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 817,196 | 8.172 | 20 | 20 | fits | 136,607 | 63 | 0.669 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 154,240 | 1.542 | 20 | 24 | fits | 148,283 | 106 | 0.421 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 445,246 | 4.452 | 20 | 24 | fits | 146,918 | 110 | 0.479 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 445,180 | 4.452 | 20 | 50 | fits | 146,918 | 110 | 0.479 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 672,972 | 6.730 | 20 | 50 | fits | 150,588 | 210 | 0.301 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 820,154 | 8.202 | 20 | 20 | fits | 136,607 | 63 | 0.669 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,133,738 | 11.337 | 20 | 20 | fits | 50,992 | 20 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 620,412 | 6.204 | 20 | 20 | fits | 157,096 | 206 | 0.325 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 523,571 | 5.236 | 20 | 200 | fits | 152,990 | 126 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 690,712 | 6.907 | 20 | 200 | fits | 157,096 | 206 | 0.325 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 524,495 | 5.245 | 20 | 20 | fits | 152,990 | 126 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 826,484 | 8.265 | 20 | 20 | fits | 135,068 | 51 | 0.709 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 148,474 | 1.485 | 20 | 24 | fits | 148,283 | 106 | 0.421 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 527,145 | 5.271 | 20 | 24 | fits | 152,990 | 126 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 527,079 | 5.271 | 20 | 50 | fits | 152,990 | 126 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 694,440 | 6.944 | 20 | 50 | fits | 157,096 | 206 | 0.325 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 829,442 | 8.294 | 20 | 20 | fits | 135,068 | 51 | 0.709 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,128,007 | 11.280 | 20 | 20 | fits | 35,992 | 18 | 0.822 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 539,294 | 5.393 | 20 | 20 | fits | 153,392 | 204 | 0.258 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 437,913 | 4.379 | 20 | 200 | fits | 150,126 | 119 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 590,689 | 5.907 | 20 | 200 | fits | 153,392 | 204 | 0.258 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 438,837 | 4.388 | 20 | 20 | fits | 150,126 | 119 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 726,563 | 7.266 | 20 | 20 | fits | 135,170 | 52 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 146,468 | 1.465 | 20 | 24 | fits | 147,997 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 441,487 | 4.415 | 20 | 24 | fits | 150,126 | 119 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 441,421 | 4.414 | 20 | 50 | fits | 150,126 | 119 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 594,417 | 5.944 | 20 | 50 | fits | 153,392 | 204 | 0.258 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 729,521 | 7.295 | 20 | 20 | fits | 135,170 | 52 | 0.707 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 1,047,426 | 10.474 | 20 | 20 | fits | 49,948 | 22 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 530,564 | 5.306 | 20 | 20 | fits | 153,839 | 206 | 0.262 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 446,606 | 4.466 | 20 | 200 | fits | 150,223 | 119 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 599,829 | 5.998 | 20 | 200 | fits | 153,839 | 206 | 0.262 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 447,530 | 4.475 | 20 | 20 | fits | 150,223 | 119 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 740,622 | 7.406 | 20 | 20 | fits | 129,502 | 54 | 0.738 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 156,117 | 1.561 | 20 | 24 | fits | 147,997 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 450,180 | 4.502 | 20 | 24 | fits | 150,223 | 119 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 450,114 | 4.501 | 20 | 50 | fits | 150,223 | 119 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 603,557 | 6.036 | 20 | 50 | fits | 153,839 | 206 | 0.262 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 743,580 | 7.436 | 20 | 20 | fits | 129,502 | 54 | 0.738 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 1,085,397 | 10.854 | 20 | 20 | fits | 54,003 | 21 | 0.763 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 551,779 | 5.518 | 20 | 20 | fits | 151,513 | 193 | 0.330 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 440,728 | 4.407 | 20 | 200 | fits | 150,032 | 132 | 0.432 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 602,451 | 6.025 | 20 | 200 | fits | 151,513 | 193 | 0.330 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 441,652 | 4.417 | 20 | 20 | fits | 150,032 | 132 | 0.432 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 737,527 | 7.375 | 20 | 20 | fits | 134,372 | 57 | 0.674 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 150,430 | 1.504 | 20 | 24 | fits | 147,997 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 444,302 | 4.443 | 20 | 24 | fits | 150,032 | 132 | 0.432 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 444,236 | 4.442 | 20 | 50 | fits | 150,032 | 132 | 0.432 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 606,179 | 6.062 | 20 | 50 | fits | 151,513 | 193 | 0.330 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 740,485 | 7.405 | 20 | 20 | fits | 134,372 | 57 | 0.674 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 1,112,567 | 11.126 | 20 | 20 | fits | 53,297 | 21 | 0.757 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 565,887 | 5.659 | 20 | 20 | fits | 154,882 | 209 | 0.255 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 461,336 | 4.613 | 20 | 200 | fits | 152,360 | 122 | 0.451 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 615,602 | 6.156 | 20 | 200 | fits | 154,882 | 209 | 0.255 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 462,260 | 4.623 | 20 | 20 | fits | 152,360 | 122 | 0.451 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 743,262 | 7.433 | 20 | 20 | fits | 126,956 | 51 | 0.741 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 159,588 | 1.596 | 20 | 24 | fits | 147,997 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 464,910 | 4.649 | 20 | 24 | fits | 152,360 | 122 | 0.451 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 464,844 | 4.648 | 20 | 50 | fits | 152,360 | 122 | 0.451 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 619,330 | 6.193 | 20 | 50 | fits | 154,882 | 209 | 0.255 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 746,220 | 7.462 | 20 | 20 | fits | 126,956 | 51 | 0.741 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 1,134,633 | 11.346 | 20 | 20 | fits | 56,190 | 27 | 0.778 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 554,276 | 5.543 | 20 | 20 | fits | 148,989 | 192 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 455,878 | 4.559 | 20 | 200 | fits | 150,233 | 119 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 604,251 | 6.043 | 20 | 200 | fits | 148,989 | 192 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 456,802 | 4.568 | 20 | 20 | fits | 150,233 | 119 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 738,901 | 7.389 | 20 | 20 | fits | 133,946 | 62 | 0.642 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 153,850 | 1.538 | 20 | 24 | fits | 148,025 | 107 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 459,452 | 4.595 | 20 | 24 | fits | 150,233 | 119 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 459,386 | 4.594 | 20 | 50 | fits | 150,233 | 119 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 607,979 | 6.080 | 20 | 50 | fits | 148,989 | 192 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 741,859 | 7.419 | 20 | 20 | fits | 133,946 | 62 | 0.642 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 1,130,783 | 11.308 | 20 | 20 | fits | 56,481 | 27 | 0.782 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 559,809 | 5.598 | 20 | 20 | fits | 151,013 | 183 | 0.363 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 449,769 | 4.498 | 20 | 200 | fits | 149,891 | 131 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 600,166 | 6.002 | 20 | 200 | fits | 151,013 | 183 | 0.363 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 450,693 | 4.507 | 20 | 20 | fits | 149,891 | 131 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 734,920 | 7.349 | 20 | 20 | fits | 134,050 | 62 | 0.645 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 148,078 | 1.481 | 20 | 24 | fits | 147,940 | 107 | 0.418 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 453,343 | 4.533 | 20 | 24 | fits | 149,891 | 131 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 453,277 | 4.533 | 20 | 50 | fits | 149,891 | 131 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 603,894 | 6.039 | 20 | 50 | fits | 151,013 | 183 | 0.363 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 737,878 | 7.379 | 20 | 20 | fits | 134,050 | 62 | 0.645 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 1,128,290 | 11.283 | 20 | 20 | fits | 64,122 | 25 | 0.752 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 563,550 | 5.636 | 20 | 20 | fits | 154,498 | 206 | 0.256 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 450,925 | 4.509 | 20 | 200 | fits | 153,667 | 114 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 604,807 | 6.048 | 20 | 200 | fits | 154,498 | 206 | 0.256 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 451,849 | 4.518 | 20 | 20 | fits | 153,667 | 114 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 740,049 | 7.400 | 20 | 20 | fits | 134,538 | 58 | 0.676 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 156,999 | 1.570 | 20 | 24 | fits | 147,997 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 454,499 | 4.545 | 20 | 24 | fits | 153,667 | 114 | 0.501 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 454,433 | 4.544 | 20 | 50 | fits | 153,667 | 114 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 608,535 | 6.085 | 20 | 50 | fits | 154,498 | 206 | 0.256 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 743,007 | 7.430 | 20 | 20 | fits | 134,538 | 58 | 0.676 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 1,120,897 | 11.209 | 20 | 20 | fits | 51,488 | 20 | 0.726 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 546,971 | 5.470 | 20 | 20 | fits | 156,314 | 196 | 0.253 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 451,759 | 4.518 | 20 | 200 | fits | 149,919 | 131 | 0.432 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 607,457 | 6.075 | 20 | 200 | fits | 156,314 | 196 | 0.253 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 452,683 | 4.527 | 20 | 20 | fits | 149,919 | 131 | 0.432 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 747,842 | 7.478 | 20 | 20 | fits | 129,125 | 54 | 0.736 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 151,233 | 1.512 | 20 | 24 | fits | 147,997 | 106 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 455,333 | 4.553 | 20 | 24 | fits | 149,919 | 131 | 0.432 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 455,267 | 4.553 | 20 | 50 | fits | 149,919 | 131 | 0.432 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 611,185 | 6.112 | 20 | 50 | fits | 156,314 | 196 | 0.253 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 750,800 | 7.508 | 20 | 20 | fits | 129,125 | 54 | 0.736 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 1,118,155 | 11.182 | 20 | 20 | fits | 46,315 | 22 | 0.782 |
| LINK_UP | `adp.link_up.if0` | 2,213 | 0.022 | 20 | 200 | fits | 28,684 | 43 (11) | 0.671 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 22,238 | 0.222 | 20 | 200 | fits | 23,686 | 29 (39) | 0.543 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 16,041 | 0.160 | 20 | 200 | fits | 5,192 | 16 (11) | 0.250 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 22,897 | 0.229 | 20 | 20 | fits | 32,215 | 21 (35) | 0.794 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 9,953 | 0.100 | 20 | 20 | fits | 28,736 | 17 (14) | 0.816 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 14,066 | 0.141 | 20 | 20 | fits | 26,415 | 18 (14) | 0.812 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 15,347 | 0.153 | 20 | 20 | fits | 30,130 | 21 (35) | 0.764 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 75,868 | 0.759 | 20 | 20 | fits | 27,296 | 8 | 0.832 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 40,805 | 0.408 | 20 | 20 | fits | 40,871 | 12 | 0.882 |
| malformed MRPDU discard | `srp.malformed.if0` | 21,782 | 0.218 | 20 | 20 | fits | 21,848 | 12 | 0.690 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 72,508 | 0.725 | 220 | 220 | fits | 44,079 | 6 | 0.897 |
| an event behind 15 others | `backlog.event.if0` | 164,912 | 1.649 | 20 | 200 | fits | 71,315 | 78 | 0.508 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 603,264 | 6.033 | 20 | 20 | fits | 144,523 | 129 | 0.145 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 480,445 | 4.804 | 20 | 200 | fits | 175,333 | 91 | 0.469 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 624,352 | 6.244 | 20 | 200 | fits | 144,523 | 129 | 0.145 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 476,123 | 4.761 | 20 | 20 | fits | 175,333 | 91 | 0.469 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 619,810 | 6.198 | 20 | 20 | fits | 144,523 | 129 | 0.145 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 153,838 | 1.538 | 20 | 24 | fits | 154,729 | 112 | 0.443 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 478,773 | 4.788 | 20 | 24 | fits | 175,333 | 91 | 0.469 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 478,707 | 4.787 | 20 | 50 | fits | 175,333 | 91 | 0.469 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 622,834 | 6.228 | 20 | 50 | fits | 144,523 | 129 | 0.145 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 656,535 | 6.565 | 20 | 20 | fits | 33,767 | 56 | 0.115 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 722,762 | 7.228 | 20 | 20 | fits | 31,466 | 47 | 0.211 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 553,850 | 5.538 | 20 | 20 | fits | 153,614 | 191 | 0.291 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 451,234 | 4.512 | 20 | 200 | fits | 152,698 | 138 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 604,232 | 6.042 | 20 | 200 | fits | 153,614 | 191 | 0.291 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 452,158 | 4.522 | 20 | 20 | fits | 152,698 | 138 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 739,204 | 7.392 | 20 | 20 | fits | 134,268 | 57 | 0.674 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 148,298 | 1.483 | 20 | 24 | fits | 148,484 | 109 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 454,808 | 4.548 | 20 | 24 | fits | 152,698 | 138 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 454,742 | 4.547 | 20 | 50 | fits | 152,698 | 138 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 607,960 | 6.080 | 20 | 50 | fits | 153,614 | 191 | 0.291 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 742,162 | 7.422 | 20 | 20 | fits | 134,268 | 57 | 0.674 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,045,198 | 10.452 | 20 | 20 | fits | 40,722 | 17 | 0.744 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 16,084 | 0.161 | 20 | 20 | fits | 29,590 | 19 | 0.771 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 451,234 | 4.512 | 20 | 200 | fits | 152,698 | 138 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 35,712 | 0.357 | 20 | 200 | fits | 29,590 | 19 | 0.771 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 452,158 | 4.522 | 20 | 20 | fits | 152,698 | 138 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 736,629 | 7.366 | 20 | 20 | fits | 134,455 | 51 | 0.701 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 148,298 | 1.483 | 20 | 24 | fits | 148,484 | 109 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 454,808 | 4.548 | 20 | 24 | fits | 152,698 | 138 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 454,742 | 4.547 | 20 | 50 | fits | 152,698 | 138 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 605,198 | 6.052 | 20 | 50 | fits | 150,852 | 191 | 0.208 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 739,587 | 7.396 | 20 | 20 | fits | 134,455 | 51 | 0.701 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,034,101 | 10.341 | 20 | 20 | fits | 32,241 | 17 | 0.731 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,398,379 | 63.984 | 20 | 20 | MISS ceiling | 20,167 | 13 | 0.525 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,418,346 | 64.183 | 20 | 20 | MISS ceiling | 19,447 | 13 | 0.434 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,437,609 | 64.376 | 20 | 20 | MISS ceiling | 19,339 | 13 | 0.460 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,456,875 | 64.569 | 20 | 20 | MISS ceiling | 19,342 | 13 | 0.460 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,476,166 | 64.762 | 20 | 20 | MISS ceiling | 19,354 | 13 | 0.451 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 310,639 | 3.106 | 20 | 200 | fits | 151,824 | 252 | 0.234 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 440,161 | 4.402 | 20 | 200 | fits | 130,138 | 59 | 0.638 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 306,317 | 3.063 | 20 | 20 | fits | 151,824 | 252 | 0.234 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,300,340 | 63.003 | 20 | 20 | MISS ceiling | 92,715 | 42 | 0.518 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 158,133 | 1.581 | 20 | 24 | fits | 145,932 | 107 | 0.425 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,303,826 | 63.038 | 20 | 24 | MISS ceiling | 92,715 | 42 | 0.518 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 308,901 | 3.089 | 20 | 50 | fits | 151,824 | 252 | 0.234 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 308,505 | 3.085 | 20 | 50 | fits | 151,824 | 252 | 0.234 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 438,577 | 4.386 | 20 | 20 | fits | 130,138 | 59 | 0.638 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 760,470 | 7.605 | 20 | 20 | fits | 62,063 | 24 | 0.707 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 6,851 | 0.069 | 20 | 20 | fits | 25,228 | 13 (29) | 0.679 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 10,613 | 0.106 | 20 | 20 | fits | 30,640 | 19 (35) | 0.779 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 15,128 | 0.151 | 20 | 20 | fits | 30,600 | 21 (12) | 0.778 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 12,637 | 0.126 | 20 | 50 | fits | 28,684 | 43 | 0.671 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 22,085 | 0.221 | 20 | 50 | fits | 25,406 | 35 | 0.610 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 11,517 | 0.115 | 20 | 50 | fits | 25,348 | 35 | 0.610 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 17,101 | 0.171 | 20 | 50 | fits | 30,275 | 61 | 0.558 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 19,279 | 0.193 | 20 | 50 | fits | 30,275 | 61 | 0.558 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 12,312 | 0.123 | 20 | 50 | fits | 25,707 | 30 | 0.592 |
| LINK_UP | `adp.link_up.if0` | 2,213 | 0.022 | 20 | 200 | fits | 28,684 | 43 (11) | 0.671 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 22,238 | 0.222 | 20 | 200 | fits | 23,686 | 29 (39) | 0.543 |
| LINK_DOWN | `adp.link_down.if0` | 1,854 | 0.019 | 20 | 200 | fits | 27,916 | 23 (9) | 0.686 |
| LINK_UP | `adp.link_up.if0` | 2,213 | 0.022 | 20 | 200 | fits | 28,684 | 43 (11) | 0.671 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 22,238 | 0.222 | 20 | 200 | fits | 23,686 | 29 (39) | 0.543 |
| GM_CHANGE | `adp.gm_change.if0` | 2,066 | 0.021 | 20 | 200 | fits | 15,233 | 17 (11) | 0.344 |
| LINK_UP | `adp.link_up.if0` | 2,213 | 0.022 | 20 | 200 | fits | 28,684 | 43 (11) | 0.671 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 22,238 | 0.222 | 20 | 200 | fits | 23,686 | 29 (39) | 0.543 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 5,176 | 0.052 | 20 | 200 | fits | 16,756 | 16 (31) | 0.532 |
| LINK_UP | `adp.link_up.if0` | 2,213 | 0.022 | 20 | 200 | fits | 28,684 | 43 (11) | 0.671 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 22,238 | 0.222 | 20 | 200 | fits | 23,686 | 29 (39) | 0.543 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 5,176 | 0.052 | 20 | 200 | fits | 16,756 | 16 (31) | 0.532 |
| set_name | `aecp_fanout.set_name.if0` | 47,065 | 0.471 | 20 | 24 | fits | 59,688 | 89 | 0.557 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 41,240 | 0.412 | 20 | 24 | fits | 53,742 | 78 | 0.584 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 43,216 | 0.432 | 20 | 24 | fits | 48,192 | 79 | 0.540 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 40,989 | 0.410 | 20 | 24 | fits | 47,148 | 78 | 0.532 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 48,290 | 0.483 | 20 | 24 | fits | 62,400 | 110 | 0.577 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 303,194 | 3.032 | 20 | 24 | fits | 60,428 | 110 | 0.574 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 311,542 | 3.115 | 20 | 24 | fits | 50,860 | 67 | 0.588 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 49,398 | 0.494 | 20 | 24 | fits | 59,068 | 99 | 0.571 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 38,482 | 0.385 | 20 | 24 | fits | 47,045 | 79 | 0.533 |
| BIND_RX | `acmp.bind_rx.if0` | 18,785 | 0.188 | 20 | 20 | fits | 43,371 | 26 (77) | 0.758 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 10,636 | 0.106 | 20 | 20 | fits | 32,523 | 19 (32) | 0.799 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,402 | 0.104 | 20 | 20 | fits | 25,376 | 15 (47) | 0.684 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 15,481 | 0.155 | 20 | 20 | fits | 41,360 | 18 (50) | 0.814 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 9,990 | 0.100 | 20 | 20 | fits | 25,532 | 17 (48) | 0.625 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,811 | 0.098 | 20 | 20 | fits | 24,706 | 16 (48) | 0.587 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 8,965 | 0.090 | 20 | 20 | fits | 23,672 | 16 (48) | 0.573 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 7,927 | 0.079 | 20 | 20 | fits | 23,620 | 17 (48) | 0.567 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 13,475 | 0.135 | 20 | 24 | fits | 26,783 | 20 | 0.745 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 32,517 | 0.325 | 20 | 24 | fits | 39,679 | 20 | 0.665 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 16,863 | 0.169 | 20 | 24 | fits | 27,079 | 20 | 0.691 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 16,225 | 0.162 | 20 | 24 | fits | 26,073 | 20 | 0.678 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 19,544 | 0.195 | 20 | 24 | fits | 26,459 | 20 | 0.678 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 16,872 | 0.169 | 20 | 24 | fits | 26,791 | 20 | 0.680 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 19,695 | 0.197 | 20 | 24 | fits | 26,232 | 20 | 0.683 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 15,839 | 0.158 | 20 | 24 | fits | 25,766 | 20 | 0.693 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 19,701 | 0.197 | 20 | 24 | fits | 26,232 | 20 | 0.703 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 23,830 | 0.238 | 20 | 24 | fits | 31,136 | 21 | 0.602 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 16,016 | 0.160 | 20 | 24 | fits | 26,016 | 20 | 0.719 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 19,145 | 0.191 | 20 | 24 | fits | 25,913 | 20 | 0.723 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i79.c0.if0` | 16,244 | 0.162 | 20 | 24 | fits | 26,092 | 20 | 0.683 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 19,897 | 0.199 | 20 | 24 | fits | 26,507 | 20 | 0.689 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 16,358 | 0.164 | 20 | 24 | fits | 26,279 | 20 | 0.685 |
| get_configuration | `aecp.get_configuration.if0` | 14,572 | 0.146 | 20 | 24 | fits | 24,056 | 20 | 0.701 |
| entity_available | `aecp.entity_available.if0` | 17,439 | 0.174 | 20 | 24 | fits | 23,965 | 20 | 0.688 |
| get_name | `aecp.get_name.if0` | 17,152 | 0.172 | 20 | 24 | fits | 27,128 | 20 | 0.713 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 21,661 | 0.217 | 20 | 24 | fits | 28,638 | 26 | 0.697 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 17,820 | 0.178 | 20 | 24 | fits | 27,875 | 29 | 0.711 |
| get_as_path, refused ENTITY_MISBEHAVING | `aecp.get_as_path.if0` | 21,717 | 0.217 | 20 | 24 | fits | 27,761 | 29 | 0.717 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 18,785 | 0.188 | 20 | 24 | fits | 24,475 | 20 | 0.714 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 14,120 | 0.141 | 20 | 24 | fits | 23,671 | 20 | 0.680 |
| set_name | `aecp.set_name.if0` | 27,730 | 0.277 | 20 | 24 | fits | 46,451 | 43 | 0.747 |
| lock_entity | `aecp.lock_entity.if0` | 21,005 | 0.210 | 20 | 24 | fits | 35,225 | 34 | 0.756 |
| unlock_entity | `aecp.unlock_entity.if0` | 19,582 | 0.196 | 20 | 24 | fits | 36,463 | 33 | 0.770 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 131,518 | 1.315 | 20 | 24 | fits | 145,230 | 137 | 0.315 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 326,262 | 3.263 | 20 | 24 | fits | 135,273 | 114 | 0.289 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 250,138 | 2.501 | 20 | 24 | fits | 52,530 | 24 | 0.665 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 345,454 | 3.455 | 20 | 24 | fits | 78,766 | 17 | 0.651 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 305,216 | 3.052 | 20 | 24 | fits | 89,664 | 17 | 0.651 |
| READ_DESCRIPTOR held for a token (#917) | `aecp.held.read_descriptor.if0` | 534,911 | 5.349 | 20 | 24 | fits | 43,842 | 23 | 0.668 |
| LINK_UP | `fixture.link_up.if0` | 2,213 | 0.022 | 20 | 200 | fits | 28,684 | 43 (11) | 0.671 |
| malformed MRPDU discard | `fixture.malformed.if0` | 21,558 | 0.216 | 20 | 20 | fits | 21,624 | 12 | 0.705 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 33,451 | 0.335 | 20 | 24 | fits | 48,347 | 43 | 0.767 |
| LINK_DOWN | `fixture.link_down.if0` | 2,164 | 0.022 | 20 | 200 | fits | 29,968 | 23 (9) | 0.738 |
| BIND_RX | `fixture.bind_rx.if0` | 19,064 | 0.191 | 20 | 20 | fits | 44,100 | 26 (77) | 0.757 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 77,769 | 0.778 | 20 | 20 | fits | 44,887 | 38 (35) | 0.769 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 10,278 | 0.103 | 20 | 20 | fits | 29,469 | 13 (29) | 0.785 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 95,645 | 0.956 | 20 | 200 | fits | 95,749 | 77 | 0.726 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 95,645 | 0.956 | 20 | 200 | fits | 95,749 | 77 | 0.726 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 95,371 | 0.954 | 20 | 20 | fits | 95,749 | 77 | 0.726 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 95,371 | 0.954 | 20 | 20 | fits | 95,749 | 77 | 0.726 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 95,579 | 0.956 | 20 | 24 | fits | 95,749 | 77 | 0.726 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 95,579 | 0.956 | 20 | 24 | fits | 95,749 | 77 | 0.726 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 95,513 | 0.955 | 20 | 50 | fits | 95,749 | 77 | 0.726 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 95,513 | 0.955 | 20 | 50 | fits | 95,749 | 77 | 0.726 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 95,447 | 0.954 | 20 | 20 | fits | 95,749 | 77 | 0.726 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 95,447 | 0.954 | 20 | 20 | fits | 95,749 | 77 | 0.726 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `srp-bound`: wait quiet TIMEOUT
- `srp-bound`: wait quiet TIMEOUT
- `srp-bound`: wait quiet TIMEOUT
- `srp-bound`: wait quiet TIMEOUT
- `srp-bound`: wait quiet TIMEOUT
- `srp-bound`: wait quiet TIMEOUT
- `srp-bound`: wait quiet TIMEOUT
