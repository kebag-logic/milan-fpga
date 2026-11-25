### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 98 paths and 7 of 974 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.192 (0.435) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.085 (0.240) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.096 (0.288) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.082 (0.433) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.094 (0.253) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.086 (0.240) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.092 (0.252) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.106 (0.260) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.112 (0.327) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.199 (0.557) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.255 (0.613) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.296 (0.634) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.189 (0.553) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.166 (0.578) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.150 (0.500) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.158 (0.409) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.050 (0.168) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.021 (0.151) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.022 (0.297) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.021 (0.283) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.148 (0.307) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.197 (0.494) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.122 (0.441) | fits | 0 aecp | 1 | 0 |
| get_as_path, refused ENTITY_MISBEHAVING | 0 | `aecp.get_as_path.if0` (aecp) | 0.163 (0.485) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.123 (0.450) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.125 (0.440) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.163 (0.491) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.121 (0.445) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR held for a token (#917) | 0 | `aecp.held.read_descriptor.if0` (aecp-held) | 5.278 (5.609) | fits | 16 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.157 (0.577) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.126 (0.445) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.270 (0.595) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.118 (0.446) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.108 (0.432) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.144 (0.466) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.189 (0.525) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.111 (0.445) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.139 (0.460) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.112 (0.439) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i79.c0.if0` (aecp) | 0.112 (0.437) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.146 (0.467) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.113 (0.438) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.143 (0.465) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.120 (0.443) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.144 (0.464) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.231 (0.551) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.224 (0.659) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.096 (0.417) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.284 (0.666) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.793 (3.113) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.436 (0.746) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.605 (0.942) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.547 (0.910) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.538 (0.822) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.598 (0.941) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.217 (3.530) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.515 (0.830) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 2.360 (2.692) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.386 (2.800) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.591 (3.982) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.350 (3.739) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.439 (1.785) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.049 (6.266) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-6.adp_available.if0` (backlog-adp@program-aged2-6) | 6.443 (6.978) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.183 (0.555) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.655 (2.266) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 64.100 (64.252) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.864 (65.019) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.338 (0.486) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-flight.held.acmp.if0` (save-flight) | 2.880 | fits | 11 acmp | 4 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-flight.held.adp.if0` (save-flight) | 5.083 | fits | 7 adp | 4 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-flight.held.aecp.if0` (save-flight) | 5.464 | fits | 14 aecp | 4 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 4.235 | fits | 6 maap | 4 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 9.842 | fits | 31 srp | 4 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.271 (0.594) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.125 (0.257) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.128 (0.283) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.248 (0.594) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.144 (0.446) | fits | 0 events | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-burst.mrpdu.periodic.if0` (save-burst) | 3.205 | fits | 0 srp | 10 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-1.service.acmp.first.if0` (backlog-adp@blank-1) | 5.332 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 63.130 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-1.service.adp.first.if0` (backlog-adp@blank-1) | 5.323 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-7.service.adp.last.if0` (backlog-adp@verify-aged2-7) | 6.939 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-4.service.aecp.first.if0` (backlog-adp@verify-4) | 2.322 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.848 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-1.service.maap.first.if0` (backlog-adp@blank-1) | 5.358 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-7.service.maap.last.if0` (backlog-adp@verify-aged2-7) | 6.976 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-7.service.srp.first.if0` (backlog-adp@verify-aged2-7) | 8.324 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-6.service.srp.last.if0` (backlog-adp@program-aged2-6) | 11.535 | fits | 31 srp | 77 | 0 |
| Talker Advertise RX for every input, bound | 0 | `srp.bound_advertise.if0` (srp-bound) | 3.009 (3.957) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.723 (0.780) | fits | 0 srp | 1 | 0 |
| Talker Advertise RX for every input, no binding (kept) | 0 | `srp.kept_advertise.if0` (srp-kept) | 1.542 (1.543) | fits | 0 srp | 1 | 0 |
| Talker Failed RX for every input, no binding (kept) | 0 | `srp.kept_failed.if0` (srp-kept) | 1.584 (1.585) | fits | 0 srp | 1 | 0 |
| Talker RX at the bound after a freed block (count) | 0 | `srp.kept_recount.if0` (srp-kept) | 0.910 (0.911) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.403 (0.404) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.214 (0.215) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.760 (0.829) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 14.537 | 11 | 152,853 (1.529) | yes | - |
| backlog-adp@blank-1 | 0 | 17.331 | 12 | 151,975 (1.520) | yes | - |
| backlog-adp@blank-2 | 0 | 17.206 | 12 | 151,975 (1.520) | yes | - |
| backlog-adp@blank-3 | 0 | 17.081 | 12 | 151,975 (1.520) | yes | - |
| backlog-adp@blank-4 | 0 | 16.956 | 12 | 151,975 (1.520) | yes | - |
| backlog-adp@blank-5 | 0 | 16.831 | 12 | 151,975 (1.520) | yes | - |
| backlog-adp@blank-6 | 0 | 16.706 | 12 | 151,975 (1.520) | yes | - |
| backlog-adp@blank-7 | 0 | 16.581 | 12 | 151,975 (1.520) | yes | - |
| backlog-adp@program-0 | 1 | 12.010 | 9 | 155,119 (1.551) | yes | - |
| backlog-adp@program-1 | 1 | 12.010 | 9 | 155,119 (1.551) | yes | - |
| backlog-adp@program-2 | 0 | 11.959 | 9 | 150,228 (1.502) | yes | - |
| backlog-adp@program-3 | 0 | 12.691 | 9 | 150,816 (1.508) | yes | - |
| backlog-adp@program-4 | 0 | 12.685 | 9 | 150,592 (1.506) | yes | - |
| backlog-adp@program-5 | 0 | 12.435 | 9 | 150,592 (1.506) | yes | - |
| backlog-adp@program-6 | 0 | 12.185 | 9 | 150,592 (1.506) | yes | - |
| backlog-adp@program-7 | 0 | 12.850 | 9 | 155,327 (1.553) | yes | - |
| backlog-adp@verify-0 | 1 | 13.321 | 8 | 154,952 (1.550) | yes | - |
| backlog-adp@verify-1 | 1 | 13.321 | 8 | 154,952 (1.550) | yes | - |
| backlog-adp@verify-2 | 1 | 13.321 | 8 | 154,952 (1.550) | yes | - |
| backlog-adp@verify-3 | 0 | 13.330 | 9 | 149,690 (1.497) | yes | - |
| backlog-adp@verify-4 | 0 | 16.216 | 11 | 153,118 (1.531) | yes | - |
| backlog-adp@verify-5 | 0 | 16.091 | 11 | 153,118 (1.531) | yes | - |
| backlog-adp@verify-6 | 0 | 15.966 | 11 | 153,118 (1.531) | yes | - |
| backlog-adp@verify-7 | 0 | 15.841 | 11 | 153,118 (1.531) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 13.180 | 9 | 155,389 (1.554) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 16.131 | 11 | 150,672 (1.507) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 15.298 | 11 | 152,231 (1.522) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 14.180 | 10 | 155,304 (1.553) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 14.273 | 10 | 156,051 (1.561) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 16.172 | 11 | 155,534 (1.555) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 15.228 | 10 | 148,330 (1.483) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 14.108 | 9 | 150,917 (1.509) | yes | - |
| backlog-adp@blank-aged1-0 | 1 | 13.366 | 9 | 152,464 (1.525) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 13.314 | 9 | 149,892 (1.499) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 13.245 | 9 | 155,421 (1.554) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 13.358 | 9 | 150,832 (1.508) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 17.364 | 12 | 149,919 (1.499) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 13.492 | 10 | 156,336 (1.563) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 15.396 | 11 | 149,109 (1.491) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 13.397 | 10 | 149,947 (1.499) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 12.673 | 10 | 150,641 (1.506) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 12.687 | 8 | 155,011 (1.550) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 12.759 | 9 | 155,451 (1.555) | yes | - |
| backlog-adp@program-aged2-3 | 1 | 12.733 | 8 | 150,855 (1.509) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 14.244 | 11 | 150,002 (1.500) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 12.857 | 10 | 154,165 (1.542) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 14.260 | 11 | 149,041 (1.490) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 12.737 | 9 | 154,967 (1.550) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 12.873 | 10 | 152,033 (1.520) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 12.802 | 10 | 155,046 (1.550) | yes | - |
| backlog-adp@program-aged1-2 | 1 | 12.657 | 8 | 152,733 (1.527) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 12.738 | 9 | 149,892 (1.499) | yes | - |
| backlog-adp@program-aged1-4 | 1 | 12.660 | 8 | 154,103 (1.541) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 12.755 | 9 | 150,862 (1.509) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 14.259 | 12 | 149,665 (1.497) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 13.158 | 11 | 154,924 (1.549) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 16.210 | 11 | 152,998 (1.530) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 15.259 | 10 | 151,064 (1.511) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 14.251 | 10 | 155,389 (1.554) | yes | - |
| backlog-adp@verify-aged2-3 | 1 | 14.231 | 9 | 152,578 (1.526) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 14.154 | 9 | 153,698 (1.537) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 18.235 | 12 | 155,941 (1.559) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 17.395 | 12 | 151,818 (1.518) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 16.235 | 11 | 158,254 (1.583) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 13.257 | 8 | 154,985 (1.550) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 13.337 | 9 | 155,425 (1.554) | yes | - |
| backlog-adp@verify-aged1-2 | 1 | 15.416 | 10 | 153,062 (1.531) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 14.506 | 11 | 152,379 (1.524) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 13.423 | 10 | 154,092 (1.541) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 13.507 | 10 | 149,027 (1.490) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 15.308 | 10 | 156,198 (1.562) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 17.435 | 12 | 155,363 (1.554) | yes | - |
| backlog | 0 | 7.769 | 8 | 175,919 (1.759) | yes | - |
| backlog-adp | 0 | 11.179 | 10 | 155,010 (1.550) | yes | - |
| backlog-adp-refill | 0 | 40.858 | 21 | 152,732 (1.527) | yes | - |
| backlog-owed | 0 | 65.503 | 24 | 174,737 (1.747) | yes | - |
| fixture | 0 | 1.429 | 2 | 95,594 (0.956) | yes | - |

Composed maximum over the 4 backlog windows: 175,919 CPU cycles (1.759 ms), backlog.
Over the windows that released their whole load only: 175,919 (1.759 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 169450 | 0 | 50,979 (0.510) | fits |
| srp-kept | 1906 | 0 | 158,477 (1.585) | fits |
| save-burst | 2838 | 0 | 163,523 (1.635) | fits |
| save-held | 3070 | 0 | 163,523 (1.635) | fits |
| save-starved | 78181 | 0 | 163,523 (1.635) | fits |
| save-flight | 2639 | 0 | 163,523 (1.635) | fits |
| acmp-notk | 3356 | 0 | 114,581 (1.146) | fits |
| srp-bound | 5820 | 1 | 210,174 (2.102) | OVER the share |
| backlog-adp@blank-0 | 487 | 0 | 152,853 (1.529) | fits |
| backlog-adp@blank-1 | 488 | 0 | 151,975 (1.520) | fits |
| backlog-adp@blank-2 | 488 | 0 | 151,975 (1.520) | fits |
| backlog-adp@blank-3 | 488 | 0 | 151,975 (1.520) | fits |
| backlog-adp@blank-4 | 488 | 0 | 151,975 (1.520) | fits |
| backlog-adp@blank-5 | 488 | 0 | 151,975 (1.520) | fits |
| backlog-adp@blank-6 | 488 | 0 | 151,975 (1.520) | fits |
| backlog-adp@blank-7 | 488 | 0 | 151,975 (1.520) | fits |
| backlog-adp@program-0 | 523 | 0 | 155,119 (1.551) | fits |
| backlog-adp@program-1 | 523 | 0 | 155,119 (1.551) | fits |
| backlog-adp@program-2 | 524 | 0 | 150,228 (1.502) | fits |
| backlog-adp@program-3 | 524 | 0 | 150,816 (1.508) | fits |
| backlog-adp@program-4 | 524 | 0 | 150,592 (1.506) | fits |
| backlog-adp@program-5 | 524 | 0 | 150,592 (1.506) | fits |
| backlog-adp@program-6 | 524 | 0 | 150,592 (1.506) | fits |
| backlog-adp@program-7 | 524 | 0 | 155,327 (1.553) | fits |
| backlog-adp@verify-0 | 546 | 0 | 154,952 (1.550) | fits |
| backlog-adp@verify-1 | 546 | 0 | 154,952 (1.550) | fits |
| backlog-adp@verify-2 | 546 | 0 | 154,952 (1.550) | fits |
| backlog-adp@verify-3 | 547 | 0 | 149,690 (1.497) | fits |
| backlog-adp@verify-4 | 549 | 0 | 153,118 (1.531) | fits |
| backlog-adp@verify-5 | 549 | 0 | 153,118 (1.531) | fits |
| backlog-adp@verify-6 | 549 | 0 | 153,118 (1.531) | fits |
| backlog-adp@verify-7 | 549 | 0 | 153,118 (1.531) | fits |
| backlog-adp@blank-aged2-0 | 797 | 0 | 155,389 (1.554) | fits |
| backlog-adp@blank-aged2-1 | 807 | 0 | 150,672 (1.507) | fits |
| backlog-adp@blank-aged2-2 | 816 | 0 | 152,231 (1.522) | fits |
| backlog-adp@blank-aged2-3 | 823 | 0 | 155,304 (1.553) | fits |
| backlog-adp@blank-aged2-4 | 832 | 0 | 156,051 (1.561) | fits |
| backlog-adp@blank-aged2-5 | 841 | 0 | 155,534 (1.555) | fits |
| backlog-adp@blank-aged2-6 | 849 | 0 | 148,330 (1.483) | fits |
| backlog-adp@blank-aged2-7 | 856 | 0 | 150,917 (1.509) | fits |
| backlog-adp@blank-aged1-0 | 730 | 0 | 152,464 (1.525) | fits |
| backlog-adp@blank-aged1-1 | 738 | 0 | 149,892 (1.499) | fits |
| backlog-adp@blank-aged1-2 | 746 | 0 | 155,421 (1.554) | fits |
| backlog-adp@blank-aged1-3 | 755 | 0 | 150,832 (1.508) | fits |
| backlog-adp@blank-aged1-4 | 766 | 0 | 149,919 (1.499) | fits |
| backlog-adp@blank-aged1-5 | 773 | 0 | 156,336 (1.563) | fits |
| backlog-adp@blank-aged1-6 | 782 | 0 | 149,109 (1.491) | fits |
| backlog-adp@blank-aged1-7 | 790 | 0 | 149,947 (1.499) | fits |
| backlog-adp@program-aged2-0 | 856 | 0 | 150,641 (1.506) | fits |
| backlog-adp@program-aged2-1 | 863 | 0 | 155,011 (1.550) | fits |
| backlog-adp@program-aged2-2 | 872 | 0 | 155,451 (1.555) | fits |
| backlog-adp@program-aged2-3 | 880 | 0 | 150,855 (1.509) | fits |
| backlog-adp@program-aged2-4 | 891 | 0 | 150,002 (1.500) | fits |
| backlog-adp@program-aged2-5 | 898 | 0 | 154,165 (1.542) | fits |
| backlog-adp@program-aged2-6 | 908 | 0 | 149,041 (1.490) | fits |
| backlog-adp@program-aged2-7 | 914 | 0 | 154,967 (1.550) | fits |
| backlog-adp@program-aged1-0 | 789 | 0 | 152,033 (1.520) | fits |
| backlog-adp@program-aged1-1 | 797 | 0 | 155,046 (1.550) | fits |
| backlog-adp@program-aged1-2 | 805 | 0 | 152,733 (1.527) | fits |
| backlog-adp@program-aged1-3 | 813 | 0 | 149,892 (1.499) | fits |
| backlog-adp@program-aged1-4 | 821 | 0 | 154,103 (1.541) | fits |
| backlog-adp@program-aged1-5 | 830 | 0 | 150,862 (1.509) | fits |
| backlog-adp@program-aged1-6 | 841 | 0 | 149,665 (1.497) | fits |
| backlog-adp@program-aged1-7 | 849 | 0 | 154,924 (1.549) | fits |
| backlog-adp@verify-aged2-0 | 821 | 0 | 152,998 (1.530) | fits |
| backlog-adp@verify-aged2-1 | 829 | 0 | 151,064 (1.511) | fits |
| backlog-adp@verify-aged2-2 | 837 | 0 | 155,389 (1.554) | fits |
| backlog-adp@verify-aged2-3 | 845 | 0 | 152,578 (1.526) | fits |
| backlog-adp@verify-aged2-4 | 853 | 0 | 153,698 (1.537) | fits |
| backlog-adp@verify-aged2-5 | 864 | 0 | 155,941 (1.559) | fits |
| backlog-adp@verify-aged2-6 | 873 | 0 | 151,818 (1.518) | fits |
| backlog-adp@verify-aged2-7 | 880 | 0 | 158,254 (1.583) | fits |
| backlog-adp@verify-aged1-0 | 751 | 0 | 154,985 (1.550) | fits |
| backlog-adp@verify-aged1-1 | 760 | 0 | 155,425 (1.554) | fits |
| backlog-adp@verify-aged1-2 | 770 | 0 | 153,062 (1.531) | fits |
| backlog-adp@verify-aged1-3 | 779 | 0 | 152,379 (1.524) | fits |
| backlog-adp@verify-aged1-4 | 786 | 0 | 154,092 (1.541) | fits |
| backlog-adp@verify-aged1-5 | 795 | 0 | 149,027 (1.490) | fits |
| backlog-adp@verify-aged1-6 | 803 | 0 | 156,198 (1.562) | fits |
| backlog-adp@verify-aged1-7 | 814 | 0 | 155,363 (1.554) | fits |
| adp-advertise | 599 | 0 | 30,979 (0.310) | fits |
| acmp-noresp | 1886 | 0 | 114,276 (1.143) | fits |
| save | 608 | 0 | 85,419 (0.854) | fits |
| srp | 289 | 0 | 44,043 (0.440) | fits |
| backlog | 286 | 0 | 175,919 (1.759) | fits |
| backlog-adp | 311 | 0 | 155,010 (1.550) | fits |
| backlog-adp-refill | 322 | 0 | 152,732 (1.527) | fits |
| backlog-owed | 308 | 0 | 174,737 (1.747) | fits |
| acmp-disc | 877 | 0 | 114,138 (1.141) | fits |
| maap | 174 | 0 | 30,979 (0.310) | fits |
| adp-link | 91 | 0 | 41,478 (0.415) | fits |
| adp-gm | 90 | 0 | 28,323 (0.283) | fits |
| adp-discover | 90 | 0 | 28,323 (0.283) | fits |
| control | 90 | 0 | 28,323 (0.283) | fits |
| aecp-fanout | 112 | 0 | 60,896 (0.609) | fits |
| acmp-cmd | 87 | 0 | 43,463 (0.435) | fits |
| aecp | 112 | 0 | 46,411 (0.464) | fits |
| aecp-largest-notice | 105 | 0 | 145,005 (1.450) | fits |
| aecp-held | 103 | 0 | 44,139 (0.441) | fits |
| datapath-events | 117 | 0 | 28,323 (0.283) | fits |
| fixture | 150 | 0 | 95,594 (0.956) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | +10.585 ms, 76,888 (0.769 ms), read-back | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 10.547 (20) | 9.453 |
| backlog-adp@blank-aged2-1 | 2 | +9.924 ms, 76,889 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 11.272 (20) | 8.728 |
| backlog-adp@blank-aged2-2 | 2 | +8.770 ms, 76,829 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 11.337 (20) | 8.663 |
| backlog-adp@blank-aged2-3 | 2 | +7.453 ms, 77,163 (0.772 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 11.420 (20) | 8.580 |
| backlog-adp@blank-aged2-4 | 2 | +6.208 ms, 76,752 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 11.511 (20) | 8.489 |
| backlog-adp@blank-aged2-5 | 2 | +6.126 ms, 76,752 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 11.431 (20) | 8.569 |
| backlog-adp@blank-aged2-6 | 2 | +4.525 ms, 76,663 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 11.387 (20) | 8.613 |
| backlog-adp@blank-aged2-7 | 2 | +3.019 ms, 76,445 (0.764 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 11.340 (20) | 8.660 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 10.603 (20) | 9.397 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 10.551 (20) | 9.449 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 10.476 (20) | 9.524 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 10.587 (20) | 9.413 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 10.508 (20) | 9.492 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 10.585 (20) | 9.415 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 10.654 (20) | 9.346 |
| backlog-adp@blank-aged1-7 | 1 | none | +10.812 ms, 76,572 (0.766 ms), read-back | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 10.588 (20) | 9.412 |
| backlog-adp@program-aged2-0 | 2 | none | +10.691 ms, 81,271 (0.813 ms), issue | `backlog-adp@program-aged2-0.service.srp.last.if0` | 10.653 (20) | 9.347 |
| backlog-adp@program-aged2-1 | 2 | +9.997 ms, 81,111 (0.811 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 11.290 (20) | 8.710 |
| backlog-adp@program-aged2-2 | 2 | +8.744 ms, 81,172 (0.812 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 11.358 (20) | 8.642 |
| backlog-adp@program-aged2-3 | 2 | +7.383 ms, 81,506 (0.815 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 11.329 (20) | 8.671 |
| backlog-adp@program-aged2-4 | 2 | +6.109 ms, 81,114 (0.811 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 11.389 (20) | 8.611 |
| backlog-adp@program-aged2-5 | 2 | +6.109 ms, 81,114 (0.811 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 11.457 (20) | 8.543 |
| backlog-adp@program-aged2-6 | 2 | +4.620 ms, 80,882 (0.809 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 11.535 (20) | 8.465 |
| backlog-adp@program-aged2-7 | 2 | +2.993 ms, 80,221 (0.802 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 11.333 (20) | 8.667 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 10.428 (20) | 9.572 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 10.648 (20) | 9.352 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 10.503 (20) | 9.497 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 10.583 (20) | 9.417 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 10.501 (20) | 9.499 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 10.594 (20) | 9.406 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 10.473 (20) | 9.527 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 10.512 (20) | 9.488 |
| backlog-adp@verify-aged2-0 | 2 | none | +10.585 ms, 77,763 (0.778 ms), read-back | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 10.548 (20) | 9.452 |
| backlog-adp@verify-aged2-1 | 2 | +10.001 ms, 77,764 (0.778 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 11.256 (20) | 8.744 |
| backlog-adp@verify-aged2-2 | 2 | +8.811 ms, 77,704 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 11.317 (20) | 8.683 |
| backlog-adp@verify-aged2-3 | 2 | +7.360 ms, 78,038 (0.780 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 11.438 (20) | 8.562 |
| backlog-adp@verify-aged2-4 | 2 | +6.057 ms, 77,627 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 11.361 (20) | 8.639 |
| backlog-adp@verify-aged2-5 | 2 | +6.009 ms, 77,627 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 11.326 (20) | 8.674 |
| backlog-adp@verify-aged2-6 | 2 | +4.509 ms, 77,563 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 11.387 (20) | 8.613 |
| backlog-adp@verify-aged2-7 | 2 | +2.998 ms, 77,201 (0.772 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 11.314 (20) | 8.686 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 10.461 (20) | 9.539 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 10.534 (20) | 9.466 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 10.494 (20) | 9.506 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 10.535 (20) | 9.465 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 10.628 (20) | 9.372 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 10.712 (20) | 9.288 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 10.513 (20) | 9.487 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 10.553 (20) | 9.447 |

Least margin over the aged windows: 8.465 ms, `backlog-adp@program-aged2-6.service.srp.last.if0` at 11.535 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 23789.788 | 23,830 | 398 | 2 | 30.872 | yes | within |
| save-held | 1344.148 | 12,950 | 398 | - | 32.516 | no | within |
| save-starved | 12927.107 | 12,950 | 398 | - | 34.137 | yes | within |
| save | 1298.196 | 12,950 | 398 | - | 102.086 | no | within |

Names from their response to durable (save_burst.py; #920, #665's ruling of 2026-11-15, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-burst | 115 | 1353.293 (0) | 5,000 | 8 | - | - | sequence 8, 0 missing | within |
| save-flight | 1 | 649.961 (0) | 5,000 | 2 | - | - | 61 steps (want 61), 24.554 ms | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1112 | 82,079 (0.821) | 78,826 (0.788) |
| srp-kept | 1844 | 24,103 (0.241) | 3,035 (0.030) |
| save-burst | 4585 | 102,161 (1.022) | 79,119 (0.791) |
| save-held | 1974 | 95,001 (0.950) | 78,534 (0.785) |
| save-starved | 714 | 81,558 (0.816) | 78,740 (0.787) |
| save-flight | 2096 | 95,080 (0.951) | 78,622 (0.786) |
| acmp-notk | 1431 | 114,581 (1.146) | 78,661 (0.787) |
| srp-bound | 2867 | 119,979 (1.200) | 79,513 (0.795) |
| backlog-adp@blank-0 | 384 | 100,516 (1.005) | 76,893 (0.769) |
| backlog-adp@blank-1 | 387 | 93,417 (0.934) | 76,499 (0.765) |
| backlog-adp@blank-2 | 387 | 93,417 (0.934) | 76,499 (0.765) |
| backlog-adp@blank-3 | 387 | 93,417 (0.934) | 76,499 (0.765) |
| backlog-adp@blank-4 | 387 | 93,417 (0.934) | 76,499 (0.765) |
| backlog-adp@blank-5 | 387 | 93,417 (0.934) | 76,499 (0.765) |
| backlog-adp@blank-6 | 387 | 93,417 (0.934) | 76,499 (0.765) |
| backlog-adp@blank-7 | 387 | 93,417 (0.934) | 76,499 (0.765) |
| backlog-adp@program-0 | 498 | 97,309 (0.973) | 78,737 (0.787) |
| backlog-adp@program-1 | 498 | 97,309 (0.973) | 78,737 (0.787) |
| backlog-adp@program-2 | 498 | 97,309 (0.973) | 78,737 (0.787) |
| backlog-adp@program-3 | 499 | 97,309 (0.973) | 79,335 (0.793) |
| backlog-adp@program-4 | 500 | 97,309 (0.973) | 78,737 (0.787) |
| backlog-adp@program-5 | 500 | 97,309 (0.973) | 78,737 (0.787) |
| backlog-adp@program-6 | 500 | 97,309 (0.973) | 78,737 (0.787) |
| backlog-adp@program-7 | 501 | 97,309 (0.973) | 79,335 (0.793) |
| backlog-adp@verify-0 | 608 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@verify-1 | 608 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@verify-2 | 608 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@verify-3 | 608 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@verify-4 | 611 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@verify-5 | 611 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@verify-6 | 611 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@verify-7 | 611 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@blank-aged2-0 | 381 | 92,592 (0.926) | 76,021 (0.760) |
| backlog-adp@blank-aged2-1 | 384 | 93,496 (0.935) | 76,096 (0.761) |
| backlog-adp@blank-aged2-2 | 383 | 93,456 (0.935) | 76,096 (0.761) |
| backlog-adp@blank-aged2-3 | 382 | 91,987 (0.920) | 76,451 (0.765) |
| backlog-adp@blank-aged2-4 | 382 | 92,194 (0.922) | 76,451 (0.765) |
| backlog-adp@blank-aged2-5 | 384 | 92,190 (0.922) | 76,451 (0.765) |
| backlog-adp@blank-aged2-6 | 383 | 92,120 (0.921) | 76,517 (0.765) |
| backlog-adp@blank-aged2-7 | 382 | 92,636 (0.926) | 76,499 (0.765) |
| backlog-adp@blank-aged1-0 | 381 | 92,344 (0.923) | 76,658 (0.767) |
| backlog-adp@blank-aged1-1 | 381 | 92,276 (0.923) | 76,658 (0.767) |
| backlog-adp@blank-aged1-2 | 381 | 92,640 (0.926) | 76,658 (0.767) |
| backlog-adp@blank-aged1-3 | 381 | 92,813 (0.928) | 76,658 (0.767) |
| backlog-adp@blank-aged1-4 | 385 | 93,534 (0.935) | 76,658 (0.767) |
| backlog-adp@blank-aged1-5 | 381 | 95,386 (0.954) | 76,712 (0.767) |
| backlog-adp@blank-aged1-6 | 383 | 92,290 (0.923) | 76,658 (0.767) |
| backlog-adp@blank-aged1-7 | 381 | 91,849 (0.918) | 75,940 (0.759) |
| backlog-adp@program-aged2-0 | 495 | 97,309 (0.973) | 78,794 (0.788) |
| backlog-adp@program-aged2-1 | 496 | 97,309 (0.973) | 78,794 (0.788) |
| backlog-adp@program-aged2-2 | 496 | 97,309 (0.973) | 78,794 (0.788) |
| backlog-adp@program-aged2-3 | 496 | 97,309 (0.973) | 78,884 (0.789) |
| backlog-adp@program-aged2-4 | 498 | 97,309 (0.973) | 78,942 (0.789) |
| backlog-adp@program-aged2-5 | 496 | 97,309 (0.973) | 78,942 (0.789) |
| backlog-adp@program-aged2-6 | 498 | 97,309 (0.973) | 78,737 (0.787) |
| backlog-adp@program-aged2-7 | 496 | 97,309 (0.973) | 78,737 (0.787) |
| backlog-adp@program-aged1-0 | 495 | 97,309 (0.973) | 79,427 (0.794) |
| backlog-adp@program-aged1-1 | 495 | 97,309 (0.973) | 79,335 (0.793) |
| backlog-adp@program-aged1-2 | 495 | 97,309 (0.973) | 79,335 (0.793) |
| backlog-adp@program-aged1-3 | 495 | 97,309 (0.973) | 79,335 (0.793) |
| backlog-adp@program-aged1-4 | 495 | 97,309 (0.973) | 79,335 (0.793) |
| backlog-adp@program-aged1-5 | 495 | 97,309 (0.973) | 79,335 (0.793) |
| backlog-adp@program-aged1-6 | 497 | 97,309 (0.973) | 79,335 (0.793) |
| backlog-adp@program-aged1-7 | 496 | 104,634 (1.046) | 79,657 (0.797) |
| backlog-adp@verify-aged2-0 | 611 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@verify-aged2-1 | 610 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@verify-aged2-2 | 609 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@verify-aged2-3 | 609 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@verify-aged2-4 | 609 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@verify-aged2-5 | 613 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@verify-aged2-6 | 612 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@verify-aged2-7 | 611 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@verify-aged1-0 | 608 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@verify-aged1-1 | 608 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@verify-aged1-2 | 610 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@verify-aged1-3 | 609 | 101,721 (1.017) | 78,914 (0.789) |
| backlog-adp@verify-aged1-4 | 608 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@verify-aged1-5 | 608 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@verify-aged1-6 | 610 | 101,067 (1.011) | 78,914 (0.789) |
| backlog-adp@verify-aged1-7 | 612 | 101,067 (1.011) | 78,914 (0.789) |
| adp-advertise | 579 | 23,540 (0.235) | 2,974 (0.030) |
| acmp-noresp | 981 | 114,276 (1.143) | 78,734 (0.787) |
| save | 953 | 95,002 (0.950) | 78,428 (0.784) |
| srp | 271 | 23,540 (0.235) | 2,974 (0.030) |
| backlog | 266 | 23,540 (0.235) | 2,974 (0.030) |
| backlog-adp | 271 | 23,540 (0.235) | 2,974 (0.030) |
| backlog-adp-refill | 274 | 23,540 (0.235) | 2,974 (0.030) |
| backlog-owed | 277 | 23,540 (0.235) | 2,974 (0.030) |
| acmp-disc | 672 | 114,138 (1.141) | 78,734 (0.787) |
| maap | 162 | 23,230 (0.232) | 2,974 (0.030) |
| adp-link | 82 | 23,230 (0.232) | 2,974 (0.030) |
| adp-gm | 82 | 23,230 (0.232) | 2,974 (0.030) |
| adp-discover | 82 | 23,230 (0.232) | 2,974 (0.030) |
| control | 82 | 23,230 (0.232) | 2,974 (0.030) |
| aecp-fanout | 80 | 23,230 (0.232) | 2,974 (0.030) |
| acmp-cmd | 66 | 23,230 (0.232) | 2,974 (0.030) |
| aecp | 80 | 23,230 (0.232) | 2,974 (0.030) |
| aecp-largest-notice | 78 | 23,230 (0.232) | 2,974 (0.030) |
| aecp-held | 94 | 23,230 (0.232) | 2,974 (0.030) |
| datapath-events | 70 | 23,230 (0.232) | 2,974 (0.030) |
| fixture | 54 | 17,241 (0.172) | 2,668 (0.027) |

Longest pass that carries a step: 119,979 CPU cycles (1.200 ms), srp-bound; longest step: 79,657 (0.797 ms), backlog-adp@program-aged1-7.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| Talker Advertise RX for every input, no binding (kept) | `srp.kept_advertise.if0` | 154,192 | 1.542 | 20 | 20 | fits | 154,258 | 12 | 0.939 |
| Talker RX at the bound after a freed block (count) | `srp.kept_recount.if0` | 91,007 | 0.910 | 20 | 20 | fits | 91,073 | 12 | 0.897 |
| Talker Failed RX for every input, no binding (kept) | `srp.kept_failed.if0` | 158,409 | 1.584 | 20 | 20 | fits | 158,477 | 12 | 0.941 |
| ADP record, every channel at its refill rate, the longest | `save-burst.held.adp.if0` | 299,047 | 2.990 | 20 | 200 | fits | 136,333 | 134 | 0.561 |
| ACMP record, every channel at its refill rate, the longest | `save-burst.held.acmp.if0` | 263,348 | 2.633 | 20 | 20 | fits | 63,521 | 51 | 0.253 |
| AECP record, every channel at its refill rate, the longest | `save-burst.held.aecp.if0` | 204,604 | 2.046 | 20 | 24 | fits | 81,528 | 39 | 0.732 |
| MAAP record, every channel at its refill rate, the longest | `save-burst.held.maap.if0` | 191,189 | 1.912 | 20 | 50 | fits | 94,907 | 175 | 0.237 |
| SRP record, every channel at its refill rate, the longest | `save-burst.held.srp.if0` | 704,044 | 7.040 | 20 | 20 | fits | 81,030 | 41 | 0.747 |
| an MRPDU its join timer owes, the longest | `save-burst.mrpdu.join.if0` | 48,992 | 0.490 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-burst.mrpdu.leaveall.if0` | 51,319 | 0.513 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-burst.mrpdu.periodic.if0` | 320,500 | 3.205 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 297,557 | 2.976 | 20 | 200 | fits | 134,974 | 129 | 0.527 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 270,753 | 2.708 | 20 | 20 | fits | 63,245 | 51 | 0.240 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 466,946 | 4.669 | 20 | 24 | fits | 57,663 | 27 | 0.528 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 237,945 | 2.379 | 20 | 50 | fits | 134,974 | 129 | 0.527 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 970,245 | 9.702 | 20 | 20 | fits | 50,787 | 20 | 0.720 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 54,166 | 0.542 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 54,166 | 0.542 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 284,595 | 2.846 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 300,593 | 3.006 | 20 | 200 | fits | 138,010 | 135 | 0.541 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 252,989 | 2.530 | 20 | 20 | fits | 136,214 | 121 | 0.228 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 480,284 | 4.803 | 20 | 24 | fits | 79,489 | 41 | 0.481 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 240,981 | 2.410 | 20 | 50 | fits | 138,010 | 135 | 0.541 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 984,180 | 9.842 | 20 | 20 | fits | 83,430 | 38 | 0.665 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 54,348 | 0.543 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 54,348 | 0.543 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 297,635 | 2.976 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 508,255 | 5.083 | 20 | 200 | fits | 126,241 | 83 | 0.497 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 287,983 | 2.880 | 20 | 20 | fits | 63,592 | 51 | 0.253 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 546,442 | 5.464 | 20 | 24 | fits | 125,303 | 49 | 0.647 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 423,484 | 4.235 | 20 | 50 | fits | 117,074 | 184 | 0.315 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 950,102 | 9.501 | 20 | 20 | fits | 30,063 | 12 | 0.798 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 81,461 | 0.815 | 49 | 49 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 16,571 | 0.166 | 20 | 20 | fits | 34,929 | 19 (14) | 0.869 |
| Talker Advertise RX for every input, bound | `srp.bound_advertise.if0` | 300,867 | 3.009 | 20 | 20 | fits | 210,174 | 40 | 0.897 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 570,387 | 5.704 | 20 | 20 | fits | 146,764 | 198 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 455,430 | 4.554 | 20 | 200 | fits | 152,853 | 122 | 0.459 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 601,578 | 6.016 | 20 | 200 | fits | 146,764 | 198 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 456,354 | 4.564 | 20 | 20 | fits | 152,853 | 122 | 0.459 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 735,612 | 7.356 | 20 | 20 | fits | 133,330 | 62 | 0.637 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 152,375 | 1.524 | 20 | 24 | fits | 150,240 | 109 | 0.445 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 459,004 | 4.590 | 20 | 24 | fits | 152,853 | 122 | 0.459 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 458,938 | 4.589 | 20 | 50 | fits | 152,853 | 122 | 0.459 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 605,306 | 6.053 | 20 | 50 | fits | 146,764 | 198 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 738,570 | 7.386 | 20 | 20 | fits | 133,330 | 62 | 0.637 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,060,847 | 10.608 | 20 | 20 | fits | 50,883 | 20 | 0.718 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 638,637 | 6.386 | 20 | 20 | fits | 147,544 | 200 | 0.280 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 532,257 | 5.323 | 20 | 200 | fits | 151,975 | 121 | 0.489 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 679,185 | 6.792 | 20 | 200 | fits | 147,544 | 200 | 0.280 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 533,181 | 5.332 | 20 | 20 | fits | 151,975 | 121 | 0.489 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 812,726 | 8.127 | 20 | 20 | fits | 132,837 | 62 | 0.634 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 230,116 | 2.301 | 20 | 24 | fits | 150,240 | 109 | 0.446 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 535,831 | 5.358 | 20 | 24 | fits | 151,975 | 121 | 0.489 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 535,765 | 5.358 | 20 | 50 | fits | 151,975 | 121 | 0.489 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 682,913 | 6.829 | 20 | 50 | fits | 147,544 | 200 | 0.280 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 815,684 | 8.157 | 20 | 20 | fits | 132,837 | 62 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 1,137,857 | 11.379 | 20 | 20 | fits | 50,896 | 20 | 0.718 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 626,137 | 6.261 | 20 | 20 | fits | 147,544 | 200 | 0.280 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 519,757 | 5.198 | 20 | 200 | fits | 151,975 | 121 | 0.489 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 666,685 | 6.667 | 20 | 200 | fits | 147,544 | 200 | 0.280 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 520,681 | 5.207 | 20 | 20 | fits | 151,975 | 121 | 0.489 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 800,226 | 8.002 | 20 | 20 | fits | 132,837 | 62 | 0.634 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 217,616 | 2.176 | 20 | 24 | fits | 150,240 | 109 | 0.446 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 523,331 | 5.233 | 20 | 24 | fits | 151,975 | 121 | 0.489 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 523,265 | 5.233 | 20 | 50 | fits | 151,975 | 121 | 0.489 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 670,413 | 6.704 | 20 | 50 | fits | 147,544 | 200 | 0.280 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 803,184 | 8.032 | 20 | 20 | fits | 132,837 | 62 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 1,125,357 | 11.254 | 20 | 20 | fits | 50,896 | 20 | 0.718 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 613,637 | 6.136 | 20 | 20 | fits | 147,544 | 200 | 0.280 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 507,257 | 5.073 | 20 | 200 | fits | 151,975 | 121 | 0.489 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 654,185 | 6.542 | 20 | 200 | fits | 147,544 | 200 | 0.280 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 508,181 | 5.082 | 20 | 20 | fits | 151,975 | 121 | 0.489 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 787,726 | 7.877 | 20 | 20 | fits | 132,837 | 62 | 0.634 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 205,116 | 2.051 | 20 | 24 | fits | 150,240 | 109 | 0.446 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 510,831 | 5.108 | 20 | 24 | fits | 151,975 | 121 | 0.489 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 510,765 | 5.108 | 20 | 50 | fits | 151,975 | 121 | 0.489 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 657,913 | 6.579 | 20 | 50 | fits | 147,544 | 200 | 0.280 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 790,684 | 7.907 | 20 | 20 | fits | 132,837 | 62 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 1,112,857 | 11.129 | 20 | 20 | fits | 50,896 | 20 | 0.718 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 601,137 | 6.011 | 20 | 20 | fits | 147,544 | 200 | 0.280 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 494,757 | 4.948 | 20 | 200 | fits | 151,975 | 121 | 0.489 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 641,685 | 6.417 | 20 | 200 | fits | 147,544 | 200 | 0.280 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 495,681 | 4.957 | 20 | 20 | fits | 151,975 | 121 | 0.489 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 775,226 | 7.752 | 20 | 20 | fits | 132,837 | 62 | 0.634 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 192,616 | 1.926 | 20 | 24 | fits | 150,240 | 109 | 0.446 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 498,331 | 4.983 | 20 | 24 | fits | 151,975 | 121 | 0.489 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 498,265 | 4.983 | 20 | 50 | fits | 151,975 | 121 | 0.489 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 645,413 | 6.454 | 20 | 50 | fits | 147,544 | 200 | 0.280 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 778,184 | 7.782 | 20 | 20 | fits | 132,837 | 62 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 1,100,357 | 11.004 | 20 | 20 | fits | 50,896 | 20 | 0.718 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 588,637 | 5.886 | 20 | 20 | fits | 147,544 | 200 | 0.280 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 482,257 | 4.823 | 20 | 200 | fits | 151,975 | 121 | 0.489 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 629,185 | 6.292 | 20 | 200 | fits | 147,544 | 200 | 0.280 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 483,181 | 4.832 | 20 | 20 | fits | 151,975 | 121 | 0.489 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 762,726 | 7.627 | 20 | 20 | fits | 132,837 | 62 | 0.634 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 180,116 | 1.801 | 20 | 24 | fits | 150,240 | 109 | 0.446 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 485,831 | 4.858 | 20 | 24 | fits | 151,975 | 121 | 0.489 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 485,765 | 4.858 | 20 | 50 | fits | 151,975 | 121 | 0.489 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 632,913 | 6.329 | 20 | 50 | fits | 147,544 | 200 | 0.280 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 765,684 | 7.657 | 20 | 20 | fits | 132,837 | 62 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 1,087,857 | 10.879 | 20 | 20 | fits | 50,896 | 20 | 0.718 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 576,137 | 5.761 | 20 | 20 | fits | 147,544 | 200 | 0.280 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 469,757 | 4.698 | 20 | 200 | fits | 151,975 | 121 | 0.489 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 616,685 | 6.167 | 20 | 200 | fits | 147,544 | 200 | 0.280 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 470,681 | 4.707 | 20 | 20 | fits | 151,975 | 121 | 0.489 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 750,226 | 7.502 | 20 | 20 | fits | 132,837 | 62 | 0.634 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 167,616 | 1.676 | 20 | 24 | fits | 150,240 | 109 | 0.446 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 473,331 | 4.733 | 20 | 24 | fits | 151,975 | 121 | 0.489 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 473,265 | 4.733 | 20 | 50 | fits | 151,975 | 121 | 0.489 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 620,413 | 6.204 | 20 | 50 | fits | 147,544 | 200 | 0.280 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 753,184 | 7.532 | 20 | 20 | fits | 132,837 | 62 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 1,075,357 | 10.754 | 20 | 20 | fits | 50,896 | 20 | 0.718 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 563,637 | 5.636 | 20 | 20 | fits | 147,544 | 200 | 0.280 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 457,257 | 4.573 | 20 | 200 | fits | 151,975 | 121 | 0.489 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 604,185 | 6.042 | 20 | 200 | fits | 147,544 | 200 | 0.280 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 458,181 | 4.582 | 20 | 20 | fits | 151,975 | 121 | 0.489 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 737,726 | 7.377 | 20 | 20 | fits | 132,837 | 62 | 0.634 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 155,116 | 1.551 | 20 | 24 | fits | 150,240 | 109 | 0.446 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 460,831 | 4.608 | 20 | 24 | fits | 151,975 | 121 | 0.489 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 460,765 | 4.608 | 20 | 50 | fits | 151,975 | 121 | 0.489 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 607,913 | 6.079 | 20 | 50 | fits | 147,544 | 200 | 0.280 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 740,684 | 7.407 | 20 | 20 | fits | 132,837 | 62 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 1,062,857 | 10.629 | 20 | 20 | fits | 50,896 | 20 | 0.718 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 556,093 | 5.561 | 20 | 20 | fits | 155,119 | 204 | 0.265 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 453,149 | 4.531 | 20 | 200 | fits | 150,941 | 119 | 0.432 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 607,652 | 6.077 | 20 | 200 | fits | 155,119 | 204 | 0.265 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 454,073 | 4.541 | 20 | 20 | fits | 150,941 | 119 | 0.432 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 742,526 | 7.425 | 20 | 20 | fits | 134,170 | 51 | 0.701 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 149,659 | 1.497 | 20 | 24 | fits | 151,253 | 110 | 0.445 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 456,723 | 4.567 | 20 | 24 | fits | 150,941 | 119 | 0.432 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 456,657 | 4.567 | 20 | 50 | fits | 150,941 | 119 | 0.432 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 611,380 | 6.114 | 20 | 50 | fits | 155,119 | 204 | 0.265 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 745,484 | 7.455 | 20 | 20 | fits | 134,170 | 51 | 0.701 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 1,060,802 | 10.608 | 20 | 20 | fits | 45,689 | 23 | 0.802 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 556,093 | 5.561 | 20 | 20 | fits | 155,119 | 204 | 0.265 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 453,149 | 4.531 | 20 | 200 | fits | 150,941 | 119 | 0.432 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 607,652 | 6.077 | 20 | 200 | fits | 155,119 | 204 | 0.265 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 454,073 | 4.541 | 20 | 20 | fits | 150,941 | 119 | 0.432 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 742,526 | 7.425 | 20 | 20 | fits | 134,170 | 51 | 0.701 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 149,659 | 1.497 | 20 | 24 | fits | 151,253 | 110 | 0.445 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 456,723 | 4.567 | 20 | 24 | fits | 150,941 | 119 | 0.432 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 456,657 | 4.567 | 20 | 50 | fits | 150,941 | 119 | 0.432 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 611,380 | 6.114 | 20 | 50 | fits | 155,119 | 204 | 0.265 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 745,484 | 7.455 | 20 | 20 | fits | 134,170 | 51 | 0.701 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 1,060,802 | 10.608 | 20 | 20 | fits | 45,689 | 23 | 0.802 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 552,970 | 5.530 | 20 | 20 | fits | 147,139 | 200 | 0.274 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 446,848 | 4.468 | 20 | 200 | fits | 150,228 | 115 | 0.446 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 593,371 | 5.934 | 20 | 200 | fits | 147,139 | 200 | 0.274 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 447,772 | 4.478 | 20 | 20 | fits | 150,228 | 115 | 0.446 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 727,662 | 7.277 | 20 | 20 | fits | 133,587 | 57 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 155,709 | 1.557 | 20 | 24 | fits | 149,752 | 110 | 0.439 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 450,422 | 4.504 | 20 | 24 | fits | 150,228 | 115 | 0.446 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 450,356 | 4.504 | 20 | 50 | fits | 150,228 | 115 | 0.446 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 597,099 | 5.971 | 20 | 50 | fits | 147,139 | 200 | 0.274 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 730,620 | 7.306 | 20 | 20 | fits | 133,587 | 57 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 1,056,038 | 10.560 | 20 | 20 | fits | 61,038 | 24 | 0.694 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 543,188 | 5.432 | 20 | 20 | fits | 147,876 | 186 | 0.270 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 446,023 | 4.460 | 20 | 200 | fits | 150,816 | 131 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 593,283 | 5.933 | 20 | 200 | fits | 147,876 | 186 | 0.270 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 446,947 | 4.469 | 20 | 20 | fits | 150,816 | 131 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 727,611 | 7.276 | 20 | 20 | fits | 133,624 | 58 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 154,203 | 1.542 | 20 | 24 | fits | 150,413 | 109 | 0.451 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 449,597 | 4.496 | 20 | 24 | fits | 150,816 | 131 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 449,531 | 4.495 | 20 | 50 | fits | 150,816 | 131 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 597,011 | 5.970 | 20 | 50 | fits | 147,876 | 186 | 0.270 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 730,569 | 7.306 | 20 | 20 | fits | 133,624 | 58 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 1,054,512 | 10.545 | 20 | 20 | fits | 50,516 | 20 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 611,693 | 6.117 | 20 | 20 | fits | 147,876 | 186 | 0.271 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 515,463 | 5.155 | 20 | 200 | fits | 150,592 | 131 | 0.438 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 662,723 | 6.627 | 20 | 200 | fits | 147,876 | 186 | 0.271 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 516,387 | 5.164 | 20 | 20 | fits | 150,592 | 131 | 0.438 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 795,319 | 7.953 | 20 | 20 | fits | 131,892 | 62 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 223,851 | 2.239 | 20 | 24 | fits | 150,354 | 109 | 0.444 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 519,037 | 5.190 | 20 | 24 | fits | 150,592 | 131 | 0.438 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 518,971 | 5.190 | 20 | 50 | fits | 150,592 | 131 | 0.438 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 666,451 | 6.665 | 20 | 50 | fits | 147,876 | 186 | 0.271 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 798,277 | 7.983 | 20 | 20 | fits | 131,892 | 62 | 0.682 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 1,128,361 | 11.284 | 20 | 20 | fits | 60,712 | 24 | 0.686 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 586,693 | 5.867 | 20 | 20 | fits | 147,876 | 186 | 0.271 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 490,463 | 4.905 | 20 | 200 | fits | 150,592 | 131 | 0.438 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 637,723 | 6.377 | 20 | 200 | fits | 147,876 | 186 | 0.271 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 491,387 | 4.914 | 20 | 20 | fits | 150,592 | 131 | 0.438 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 770,319 | 7.703 | 20 | 20 | fits | 131,892 | 62 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 198,851 | 1.989 | 20 | 24 | fits | 150,354 | 109 | 0.444 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 494,037 | 4.940 | 20 | 24 | fits | 150,592 | 131 | 0.438 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 493,971 | 4.940 | 20 | 50 | fits | 150,592 | 131 | 0.438 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 641,451 | 6.415 | 20 | 50 | fits | 147,876 | 186 | 0.271 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 773,277 | 7.733 | 20 | 20 | fits | 131,892 | 62 | 0.682 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 1,103,361 | 11.034 | 20 | 20 | fits | 60,712 | 24 | 0.686 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 561,693 | 5.617 | 20 | 20 | fits | 147,876 | 186 | 0.271 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 465,463 | 4.655 | 20 | 200 | fits | 150,592 | 131 | 0.438 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 612,723 | 6.127 | 20 | 200 | fits | 147,876 | 186 | 0.271 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 466,387 | 4.664 | 20 | 20 | fits | 150,592 | 131 | 0.438 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 745,319 | 7.453 | 20 | 20 | fits | 131,892 | 62 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 173,851 | 1.739 | 20 | 24 | fits | 150,354 | 109 | 0.444 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 469,037 | 4.690 | 20 | 24 | fits | 150,592 | 131 | 0.438 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 468,971 | 4.690 | 20 | 50 | fits | 150,592 | 131 | 0.438 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 616,451 | 6.165 | 20 | 50 | fits | 147,876 | 186 | 0.271 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 748,277 | 7.483 | 20 | 20 | fits | 131,892 | 62 | 0.682 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 1,078,361 | 10.784 | 20 | 20 | fits | 60,712 | 24 | 0.686 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 545,845 | 5.458 | 20 | 20 | fits | 155,327 | 206 | 0.267 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 460,779 | 4.608 | 20 | 200 | fits | 151,142 | 119 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 615,490 | 6.155 | 20 | 200 | fits | 155,327 | 206 | 0.267 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 461,703 | 4.617 | 20 | 20 | fits | 151,142 | 119 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 762,708 | 7.627 | 20 | 20 | fits | 136,014 | 62 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 168,633 | 1.686 | 20 | 24 | fits | 150,239 | 109 | 0.447 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 464,353 | 4.644 | 20 | 24 | fits | 151,142 | 119 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 464,287 | 4.643 | 20 | 50 | fits | 151,142 | 119 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 619,218 | 6.192 | 20 | 50 | fits | 155,327 | 206 | 0.267 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 765,666 | 7.657 | 20 | 20 | fits | 136,014 | 62 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 1,069,717 | 10.697 | 20 | 20 | fits | 40,361 | 16 | 0.746 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 547,557 | 5.476 | 20 | 20 | fits | 154,952 | 205 | 0.261 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 444,874 | 4.449 | 20 | 200 | fits | 150,793 | 119 | 0.430 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 599,210 | 5.992 | 20 | 200 | fits | 154,952 | 205 | 0.261 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 445,798 | 4.458 | 20 | 20 | fits | 150,793 | 119 | 0.430 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 739,559 | 7.396 | 20 | 20 | fits | 129,145 | 54 | 0.735 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 152,113 | 1.521 | 20 | 24 | fits | 153,523 | 109 | 0.452 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 448,448 | 4.484 | 20 | 24 | fits | 150,793 | 119 | 0.430 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 448,382 | 4.484 | 20 | 50 | fits | 150,793 | 119 | 0.430 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 602,938 | 6.029 | 20 | 50 | fits | 154,952 | 205 | 0.261 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 742,517 | 7.425 | 20 | 20 | fits | 129,145 | 54 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,051,770 | 10.518 | 20 | 20 | fits | 45,577 | 22 | 0.775 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 547,557 | 5.476 | 20 | 20 | fits | 154,952 | 205 | 0.261 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 444,874 | 4.449 | 20 | 200 | fits | 150,793 | 119 | 0.430 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 599,210 | 5.992 | 20 | 200 | fits | 154,952 | 205 | 0.261 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 445,798 | 4.458 | 20 | 20 | fits | 150,793 | 119 | 0.430 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 739,559 | 7.396 | 20 | 20 | fits | 129,145 | 54 | 0.735 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 152,113 | 1.521 | 20 | 24 | fits | 153,523 | 109 | 0.452 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 448,448 | 4.484 | 20 | 24 | fits | 150,793 | 119 | 0.430 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 448,382 | 4.484 | 20 | 50 | fits | 150,793 | 119 | 0.430 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 602,938 | 6.029 | 20 | 50 | fits | 154,952 | 205 | 0.261 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 742,517 | 7.425 | 20 | 20 | fits | 129,145 | 54 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 1,051,770 | 10.518 | 20 | 20 | fits | 45,577 | 22 | 0.775 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 547,557 | 5.476 | 20 | 20 | fits | 154,952 | 205 | 0.261 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 444,874 | 4.449 | 20 | 200 | fits | 150,793 | 119 | 0.430 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 599,210 | 5.992 | 20 | 200 | fits | 154,952 | 205 | 0.261 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 445,798 | 4.458 | 20 | 20 | fits | 150,793 | 119 | 0.430 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 739,559 | 7.396 | 20 | 20 | fits | 129,145 | 54 | 0.735 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 152,113 | 1.521 | 20 | 24 | fits | 153,523 | 109 | 0.452 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 448,448 | 4.484 | 20 | 24 | fits | 150,793 | 119 | 0.430 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 448,382 | 4.484 | 20 | 50 | fits | 150,793 | 119 | 0.430 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 602,938 | 6.029 | 20 | 50 | fits | 154,952 | 205 | 0.261 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 742,517 | 7.425 | 20 | 20 | fits | 129,145 | 54 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 1,051,770 | 10.518 | 20 | 20 | fits | 45,577 | 22 | 0.775 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 550,072 | 5.501 | 20 | 20 | fits | 147,292 | 201 | 0.275 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 443,968 | 4.440 | 20 | 200 | fits | 149,690 | 115 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 590,644 | 5.906 | 20 | 200 | fits | 147,292 | 201 | 0.275 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 444,892 | 4.449 | 20 | 20 | fits | 149,690 | 115 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 730,167 | 7.302 | 20 | 20 | fits | 128,319 | 60 | 0.703 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 153,327 | 1.533 | 20 | 24 | fits | 149,324 | 109 | 0.434 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 447,542 | 4.475 | 20 | 24 | fits | 149,690 | 115 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 447,476 | 4.475 | 20 | 50 | fits | 149,690 | 115 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 594,372 | 5.944 | 20 | 50 | fits | 147,292 | 201 | 0.275 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 733,125 | 7.331 | 20 | 20 | fits | 128,319 | 60 | 0.703 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 1,052,661 | 10.527 | 20 | 20 | fits | 56,161 | 26 | 0.747 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 635,819 | 6.358 | 20 | 20 | fits | 153,118 | 193 | 0.338 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 523,891 | 5.239 | 20 | 200 | fits | 150,737 | 132 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 687,086 | 6.871 | 20 | 200 | fits | 153,118 | 193 | 0.338 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 524,815 | 5.248 | 20 | 20 | fits | 150,737 | 132 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 821,403 | 8.214 | 20 | 20 | fits | 133,613 | 57 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 232,189 | 2.322 | 20 | 24 | fits | 149,693 | 109 | 0.435 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 527,465 | 5.275 | 20 | 24 | fits | 150,737 | 132 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 527,399 | 5.274 | 20 | 50 | fits | 150,737 | 132 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 690,814 | 6.908 | 20 | 50 | fits | 153,118 | 193 | 0.338 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 824,361 | 8.244 | 20 | 20 | fits | 133,613 | 57 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 1,133,771 | 11.338 | 20 | 20 | fits | 50,645 | 20 | 0.714 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 623,319 | 6.233 | 20 | 20 | fits | 153,118 | 193 | 0.338 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 511,391 | 5.114 | 20 | 200 | fits | 150,737 | 132 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 674,586 | 6.746 | 20 | 200 | fits | 153,118 | 193 | 0.338 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 512,315 | 5.123 | 20 | 20 | fits | 150,737 | 132 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 808,903 | 8.089 | 20 | 20 | fits | 133,613 | 57 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 219,689 | 2.197 | 20 | 24 | fits | 149,693 | 109 | 0.435 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 514,965 | 5.150 | 20 | 24 | fits | 150,737 | 132 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 514,899 | 5.149 | 20 | 50 | fits | 150,737 | 132 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 678,314 | 6.783 | 20 | 50 | fits | 153,118 | 193 | 0.338 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 811,861 | 8.119 | 20 | 20 | fits | 133,613 | 57 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 1,121,271 | 11.213 | 20 | 20 | fits | 50,645 | 20 | 0.714 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 610,819 | 6.108 | 20 | 20 | fits | 153,118 | 193 | 0.338 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 498,891 | 4.989 | 20 | 200 | fits | 150,737 | 132 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 662,086 | 6.621 | 20 | 200 | fits | 153,118 | 193 | 0.338 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 499,815 | 4.998 | 20 | 20 | fits | 150,737 | 132 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 796,403 | 7.964 | 20 | 20 | fits | 133,613 | 57 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 207,189 | 2.072 | 20 | 24 | fits | 149,693 | 109 | 0.435 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 502,465 | 5.025 | 20 | 24 | fits | 150,737 | 132 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 502,399 | 5.024 | 20 | 50 | fits | 150,737 | 132 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 665,814 | 6.658 | 20 | 50 | fits | 153,118 | 193 | 0.338 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 799,361 | 7.994 | 20 | 20 | fits | 133,613 | 57 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 1,108,771 | 11.088 | 20 | 20 | fits | 50,645 | 20 | 0.714 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 598,319 | 5.983 | 20 | 20 | fits | 153,118 | 193 | 0.338 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 486,391 | 4.864 | 20 | 200 | fits | 150,737 | 132 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 649,586 | 6.496 | 20 | 200 | fits | 153,118 | 193 | 0.338 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 487,315 | 4.873 | 20 | 20 | fits | 150,737 | 132 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 783,903 | 7.839 | 20 | 20 | fits | 133,613 | 57 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 194,689 | 1.947 | 20 | 24 | fits | 149,693 | 109 | 0.435 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 489,965 | 4.900 | 20 | 24 | fits | 150,737 | 132 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 489,899 | 4.899 | 20 | 50 | fits | 150,737 | 132 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 653,314 | 6.533 | 20 | 50 | fits | 153,118 | 193 | 0.338 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 786,861 | 7.869 | 20 | 20 | fits | 133,613 | 57 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 1,096,271 | 10.963 | 20 | 20 | fits | 50,645 | 20 | 0.714 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 532,334 | 5.323 | 20 | 20 | fits | 155,389 | 205 | 0.269 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 447,081 | 4.471 | 20 | 200 | fits | 150,998 | 119 | 0.432 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 601,854 | 6.019 | 20 | 200 | fits | 155,389 | 205 | 0.269 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 448,005 | 4.480 | 20 | 20 | fits | 150,998 | 119 | 0.432 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 736,856 | 7.369 | 20 | 20 | fits | 134,298 | 52 | 0.700 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 155,181 | 1.552 | 20 | 24 | fits | 148,369 | 106 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 450,655 | 4.507 | 20 | 24 | fits | 150,998 | 119 | 0.432 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 450,589 | 4.506 | 20 | 50 | fits | 150,998 | 119 | 0.432 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 605,582 | 6.056 | 20 | 50 | fits | 155,389 | 205 | 0.269 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 739,814 | 7.398 | 20 | 20 | fits | 134,298 | 52 | 0.700 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 1,054,706 | 10.547 | 20 | 20 | fits | 45,226 | 22 | 0.762 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 537,379 | 5.374 | 20 | 20 | fits | 148,149 | 187 | 0.273 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 440,004 | 4.400 | 20 | 200 | fits | 150,672 | 131 | 0.438 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 587,537 | 5.875 | 20 | 200 | fits | 148,149 | 187 | 0.273 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 440,928 | 4.409 | 20 | 20 | fits | 150,672 | 131 | 0.438 |
| ACMP record released under the compose

[... table.md: 194,497 bytes in full, sha256 465744a42463210efde08df249e762a6656d3f9b19c341f82db2e15bb9aafd26; the middle 14,497 bytes are cut here, the first and last 90,000 kept ...]

 ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 727,265 | 7.273 | 20 | 20 | fits | 133,804 | 58 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 155,008 | 1.550 | 20 | 24 | fits | 148,306 | 106 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 449,640 | 4.496 | 20 | 24 | fits | 149,892 | 115 | 0.442 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 449,574 | 4.496 | 20 | 50 | fits | 149,892 | 115 | 0.442 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 596,485 | 5.965 | 20 | 50 | fits | 147,307 | 200 | 0.277 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 730,223 | 7.302 | 20 | 20 | fits | 133,804 | 58 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 1,055,054 | 10.551 | 20 | 20 | fits | 60,764 | 24 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 525,689 | 5.257 | 20 | 20 | fits | 155,421 | 206 | 0.269 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 440,436 | 4.404 | 20 | 200 | fits | 151,092 | 119 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 595,241 | 5.952 | 20 | 200 | fits | 155,421 | 206 | 0.269 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 441,360 | 4.414 | 20 | 20 | fits | 151,092 | 119 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 735,170 | 7.352 | 20 | 20 | fits | 128,846 | 54 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 148,178 | 1.482 | 20 | 24 | fits | 148,306 | 106 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 444,010 | 4.440 | 20 | 24 | fits | 151,092 | 119 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 443,944 | 4.439 | 20 | 50 | fits | 151,092 | 119 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 598,969 | 5.990 | 20 | 50 | fits | 155,421 | 206 | 0.269 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 738,128 | 7.381 | 20 | 20 | fits | 128,846 | 54 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 1,047,573 | 10.476 | 20 | 20 | fits | 50,580 | 20 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 544,552 | 5.446 | 20 | 20 | fits | 148,062 | 187 | 0.273 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 448,137 | 4.481 | 20 | 200 | fits | 150,832 | 131 | 0.438 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 595,583 | 5.956 | 20 | 200 | fits | 148,062 | 187 | 0.273 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 449,061 | 4.491 | 20 | 20 | fits | 150,832 | 131 | 0.438 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 741,652 | 7.417 | 20 | 20 | fits | 134,986 | 68 | 0.695 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 156,139 | 1.561 | 20 | 24 | fits | 148,306 | 106 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 451,711 | 4.517 | 20 | 24 | fits | 150,832 | 131 | 0.438 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 451,645 | 4.516 | 20 | 50 | fits | 150,832 | 131 | 0.438 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 599,311 | 5.993 | 20 | 50 | fits | 148,062 | 187 | 0.273 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 744,610 | 7.446 | 20 | 20 | fits | 134,986 | 68 | 0.695 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 1,058,749 | 10.587 | 20 | 20 | fits | 50,580 | 20 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 568,179 | 5.682 | 20 | 20 | fits | 149,620 | 203 | 0.370 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 440,473 | 4.405 | 20 | 200 | fits | 149,919 | 116 | 0.442 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 599,669 | 5.997 | 20 | 200 | fits | 149,620 | 203 | 0.370 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 441,397 | 4.414 | 20 | 20 | fits | 149,919 | 116 | 0.442 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 733,970 | 7.340 | 20 | 20 | fits | 133,597 | 62 | 0.640 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 149,388 | 1.494 | 20 | 24 | fits | 148,306 | 106 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 444,047 | 4.440 | 20 | 24 | fits | 149,919 | 116 | 0.442 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 443,981 | 4.440 | 20 | 50 | fits | 149,919 | 116 | 0.442 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 603,397 | 6.034 | 20 | 50 | fits | 149,620 | 203 | 0.370 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 736,928 | 7.369 | 20 | 20 | fits | 133,597 | 62 | 0.640 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 1,050,777 | 10.508 | 20 | 20 | fits | 50,581 | 20 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 572,290 | 5.723 | 20 | 20 | fits | 156,336 | 206 | 0.263 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 458,166 | 4.582 | 20 | 200 | fits | 150,784 | 121 | 0.485 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 613,886 | 6.139 | 20 | 200 | fits | 156,336 | 206 | 0.263 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 459,090 | 4.591 | 20 | 20 | fits | 150,784 | 121 | 0.485 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 748,199 | 7.482 | 20 | 20 | fits | 133,609 | 57 | 0.667 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 157,349 | 1.573 | 20 | 24 | fits | 148,306 | 106 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 461,740 | 4.617 | 20 | 24 | fits | 150,784 | 121 | 0.485 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 461,674 | 4.617 | 20 | 50 | fits | 150,784 | 121 | 0.485 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 617,614 | 6.176 | 20 | 50 | fits | 156,336 | 206 | 0.263 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 751,157 | 7.512 | 20 | 20 | fits | 133,609 | 57 | 0.667 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 1,058,527 | 10.585 | 20 | 20 | fits | 43,611 | 23 | 0.745 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 556,477 | 5.565 | 20 | 20 | fits | 147,318 | 200 | 0.275 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 451,464 | 4.515 | 20 | 200 | fits | 149,109 | 114 | 0.476 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 598,166 | 5.982 | 20 | 200 | fits | 147,318 | 200 | 0.275 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 452,388 | 4.524 | 20 | 20 | fits | 149,109 | 114 | 0.476 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 731,696 | 7.317 | 20 | 20 | fits | 132,826 | 62 | 0.635 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 150,529 | 1.505 | 20 | 24 | fits | 148,316 | 107 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 455,038 | 4.550 | 20 | 24 | fits | 149,109 | 114 | 0.476 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 454,972 | 4.550 | 20 | 50 | fits | 149,109 | 114 | 0.476 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 601,894 | 6.019 | 20 | 50 | fits | 147,318 | 200 | 0.275 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 734,654 | 7.347 | 20 | 20 | fits | 132,826 | 62 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 1,065,408 | 10.654 | 20 | 20 | fits | 56,218 | 27 | 0.774 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 560,227 | 5.602 | 20 | 20 | fits | 147,323 | 200 | 0.277 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 453,967 | 4.540 | 20 | 200 | fits | 149,725 | 115 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 600,674 | 6.007 | 20 | 200 | fits | 147,323 | 200 | 0.277 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 454,891 | 4.549 | 20 | 20 | fits | 149,725 | 115 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 735,060 | 7.351 | 20 | 20 | fits | 133,682 | 57 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 158,859 | 1.589 | 20 | 24 | fits | 148,397 | 106 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 457,541 | 4.575 | 20 | 24 | fits | 149,725 | 115 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 457,475 | 4.575 | 20 | 50 | fits | 149,725 | 115 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 604,402 | 6.044 | 20 | 50 | fits | 147,323 | 200 | 0.277 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 738,018 | 7.380 | 20 | 20 | fits | 133,682 | 57 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 1,058,815 | 10.588 | 20 | 20 | fits | 50,971 | 20 | 0.722 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 552,679 | 5.527 | 20 | 20 | fits | 148,097 | 186 | 0.274 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 456,228 | 4.562 | 20 | 200 | fits | 150,641 | 131 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 603,709 | 6.037 | 20 | 200 | fits | 148,097 | 186 | 0.274 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 457,152 | 4.572 | 20 | 20 | fits | 150,641 | 131 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 737,852 | 7.379 | 20 | 20 | fits | 133,439 | 57 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 153,489 | 1.535 | 20 | 24 | fits | 148,289 | 107 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 459,802 | 4.598 | 20 | 24 | fits | 150,641 | 131 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 459,736 | 4.597 | 20 | 50 | fits | 150,641 | 131 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 607,437 | 6.074 | 20 | 50 | fits | 148,097 | 186 | 0.274 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 740,810 | 7.408 | 20 | 20 | fits | 133,439 | 57 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 1,065,301 | 10.653 | 20 | 20 | fits | 49,956 | 29 | 0.796 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 542,016 | 5.420 | 20 | 20 | fits | 155,011 | 204 | 0.264 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 439,180 | 4.392 | 20 | 200 | fits | 151,084 | 119 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 593,575 | 5.936 | 20 | 200 | fits | 155,011 | 204 | 0.264 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 440,104 | 4.401 | 20 | 20 | fits | 151,084 | 119 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 728,639 | 7.286 | 20 | 20 | fits | 134,360 | 52 | 0.700 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 146,167 | 1.462 | 20 | 24 | fits | 148,369 | 106 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 442,754 | 4.428 | 20 | 24 | fits | 151,084 | 119 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 442,688 | 4.427 | 20 | 50 | fits | 151,084 | 119 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 597,303 | 5.973 | 20 | 50 | fits | 155,011 | 204 | 0.264 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 731,597 | 7.316 | 20 | 20 | fits | 134,360 | 52 | 0.700 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 1,129,043 | 11.290 | 20 | 20 | fits | 52,014 | 21 | 0.735 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 531,432 | 5.314 | 20 | 20 | fits | 155,451 | 206 | 0.270 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 446,242 | 4.462 | 20 | 200 | fits | 151,181 | 119 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 601,077 | 6.011 | 20 | 200 | fits | 155,451 | 206 | 0.270 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 447,166 | 4.472 | 20 | 20 | fits | 151,181 | 119 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 740,992 | 7.410 | 20 | 20 | fits | 128,832 | 54 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 154,128 | 1.541 | 20 | 24 | fits | 148,369 | 106 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 449,816 | 4.498 | 20 | 24 | fits | 151,181 | 119 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 449,750 | 4.497 | 20 | 50 | fits | 151,181 | 119 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 604,805 | 6.048 | 20 | 50 | fits | 155,451 | 206 | 0.270 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 743,950 | 7.439 | 20 | 20 | fits | 128,832 | 54 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,135,752 | 11.358 | 20 | 20 | fits | 50,325 | 20 | 0.708 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 536,925 | 5.369 | 20 | 20 | fits | 148,114 | 187 | 0.273 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 439,616 | 4.396 | 20 | 200 | fits | 150,855 | 131 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 587,114 | 5.871 | 20 | 200 | fits | 148,114 | 187 | 0.273 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 440,540 | 4.405 | 20 | 20 | fits | 150,855 | 131 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 733,640 | 7.336 | 20 | 20 | fits | 135,279 | 68 | 0.697 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 146,832 | 1.468 | 20 | 24 | fits | 148,369 | 106 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 443,190 | 4.432 | 20 | 24 | fits | 150,855 | 131 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 443,124 | 4.431 | 20 | 50 | fits | 150,855 | 131 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 590,842 | 5.908 | 20 | 50 | fits | 148,114 | 187 | 0.273 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 736,598 | 7.366 | 20 | 20 | fits | 135,279 | 68 | 0.697 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,132,916 | 11.329 | 20 | 20 | fits | 50,594 | 20 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 573,964 | 5.740 | 20 | 20 | fits | 149,649 | 203 | 0.370 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 446,273 | 4.463 | 20 | 200 | fits | 150,002 | 116 | 0.443 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 605,549 | 6.055 | 20 | 200 | fits | 149,649 | 203 | 0.370 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 447,197 | 4.472 | 20 | 20 | fits | 150,002 | 116 | 0.443 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 821,954 | 8.220 | 20 | 20 | fits | 134,587 | 63 | 0.647 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 155,338 | 1.553 | 20 | 24 | fits | 148,369 | 106 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 449,847 | 4.498 | 20 | 24 | fits | 150,002 | 116 | 0.443 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 449,781 | 4.498 | 20 | 50 | fits | 150,002 | 116 | 0.443 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 609,277 | 6.093 | 20 | 50 | fits | 149,649 | 203 | 0.370 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 824,912 | 8.249 | 20 | 20 | fits | 134,587 | 63 | 0.647 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,138,855 | 11.389 | 20 | 20 | fits | 50,527 | 20 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 545,523 | 5.455 | 20 | 20 | fits | 154,165 | 201 | 0.322 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 452,017 | 4.520 | 20 | 200 | fits | 153,709 | 126 | 0.445 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 605,566 | 6.056 | 20 | 200 | fits | 154,165 | 201 | 0.322 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 452,941 | 4.529 | 20 | 20 | fits | 153,709 | 126 | 0.445 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 822,205 | 8.222 | 20 | 20 | fits | 134,821 | 58 | 0.676 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 148,508 | 1.485 | 20 | 24 | fits | 148,369 | 106 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 455,591 | 4.556 | 20 | 24 | fits | 153,709 | 126 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 455,525 | 4.555 | 20 | 50 | fits | 153,709 | 126 | 0.445 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 609,294 | 6.093 | 20 | 50 | fits | 154,165 | 201 | 0.322 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 825,163 | 8.252 | 20 | 20 | fits | 134,821 | 58 | 0.676 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,145,697 | 11.457 | 20 | 20 | fits | 45,818 | 23 | 0.802 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 644,295 | 6.443 | 20 | 20 | fits | 148,457 | 200 | 0.298 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 457,258 | 4.573 | 20 | 200 | fits | 149,041 | 114 | 0.475 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 685,981 | 6.860 | 20 | 200 | fits | 148,457 | 200 | 0.298 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 458,182 | 4.582 | 20 | 20 | fits | 149,041 | 114 | 0.475 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 819,497 | 8.195 | 20 | 20 | fits | 132,812 | 62 | 0.634 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 156,479 | 1.565 | 20 | 24 | fits | 148,379 | 107 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 460,832 | 4.608 | 20 | 24 | fits | 149,041 | 114 | 0.475 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 460,766 | 4.608 | 20 | 50 | fits | 149,041 | 114 | 0.475 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 689,709 | 6.897 | 20 | 50 | fits | 148,457 | 200 | 0.298 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 822,455 | 8.225 | 20 | 20 | fits | 132,812 | 62 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,153,511 | 11.535 | 20 | 20 | fits | 61,162 | 24 | 0.696 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 628,995 | 6.290 | 20 | 20 | fits | 154,967 | 204 | 0.263 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 526,141 | 5.261 | 20 | 200 | fits | 151,407 | 119 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 680,492 | 6.805 | 20 | 200 | fits | 154,967 | 204 | 0.263 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 527,065 | 5.271 | 20 | 20 | fits | 151,407 | 119 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 815,564 | 8.156 | 20 | 20 | fits | 134,368 | 52 | 0.700 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 148,881 | 1.489 | 20 | 24 | fits | 148,406 | 106 | 0.429 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 529,715 | 5.297 | 20 | 24 | fits | 151,407 | 119 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 529,649 | 5.296 | 20 | 50 | fits | 151,407 | 119 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 684,220 | 6.842 | 20 | 50 | fits | 154,967 | 204 | 0.263 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 818,522 | 8.185 | 20 | 20 | fits | 134,368 | 52 | 0.700 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,133,263 | 11.333 | 20 | 20 | fits | 45,050 | 22 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 555,643 | 5.556 | 20 | 20 | fits | 147,011 | 200 | 0.274 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 449,587 | 4.496 | 20 | 200 | fits | 152,033 | 121 | 0.452 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 595,982 | 5.960 | 20 | 200 | fits | 147,011 | 200 | 0.274 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 450,511 | 4.505 | 20 | 20 | fits | 152,033 | 121 | 0.452 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 730,283 | 7.303 | 20 | 20 | fits | 133,597 | 57 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 146,484 | 1.465 | 20 | 24 | fits | 148,369 | 106 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 453,161 | 4.532 | 20 | 24 | fits | 152,033 | 121 | 0.452 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 453,095 | 4.531 | 20 | 50 | fits | 152,033 | 121 | 0.452 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 599,710 | 5.997 | 20 | 50 | fits | 147,011 | 200 | 0.274 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 733,241 | 7.332 | 20 | 20 | fits | 133,597 | 57 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 1,042,762 | 10.428 | 20 | 20 | fits | 45,840 | 23 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 560,076 | 5.601 | 20 | 20 | fits | 155,046 | 204 | 0.263 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 457,143 | 4.571 | 20 | 200 | fits | 150,706 | 119 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 611,573 | 6.116 | 20 | 200 | fits | 155,046 | 204 | 0.263 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 458,067 | 4.581 | 20 | 20 | fits | 150,706 | 119 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 746,519 | 7.465 | 20 | 20 | fits | 134,242 | 51 | 0.701 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 154,464 | 1.545 | 20 | 24 | fits | 148,388 | 107 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 460,717 | 4.607 | 20 | 24 | fits | 150,706 | 119 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 460,651 | 4.607 | 20 | 50 | fits | 150,706 | 119 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 615,301 | 6.153 | 20 | 50 | fits | 155,046 | 204 | 0.263 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 749,477 | 7.495 | 20 | 20 | fits | 134,242 | 51 | 0.701 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 1,064,815 | 10.648 | 20 | 20 | fits | 45,710 | 23 | 0.802 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 536,205 | 5.362 | 20 | 20 | fits | 147,942 | 186 | 0.272 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 439,847 | 4.398 | 20 | 200 | fits | 152,733 | 137 | 0.443 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 587,173 | 5.872 | 20 | 200 | fits | 147,942 | 186 | 0.272 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 440,771 | 4.408 | 20 | 20 | fits | 152,733 | 137 | 0.443 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 721,450 | 7.215 | 20 | 20 | fits | 133,573 | 57 | 0.669 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 145,229 | 1.452 | 20 | 24 | fits | 149,973 | 111 | 0.427 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 443,421 | 4.434 | 20 | 24 | fits | 152,733 | 137 | 0.443 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 443,355 | 4.434 | 20 | 50 | fits | 152,733 | 137 | 0.443 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 590,901 | 5.909 | 20 | 50 | fits | 147,942 | 186 | 0.272 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 724,408 | 7.244 | 20 | 20 | fits | 133,573 | 57 | 0.669 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 1,050,337 | 10.503 | 20 | 20 | fits | 61,162 | 24 | 0.696 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 552,252 | 5.523 | 20 | 20 | fits | 147,272 | 200 | 0.277 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 446,012 | 4.460 | 20 | 200 | fits | 149,892 | 115 | 0.442 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 592,668 | 5.927 | 20 | 200 | fits | 147,272 | 200 | 0.277 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 446,936 | 4.469 | 20 | 20 | fits | 149,892 | 115 | 0.442 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 725,237 | 7.252 | 20 | 20 | fits | 131,865 | 62 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 154,923 | 1.549 | 20 | 24 | fits | 148,306 | 106 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 449,586 | 4.496 | 20 | 24 | fits | 149,892 | 115 | 0.442 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 449,520 | 4.495 | 20 | 50 | fits | 149,892 | 115 | 0.442 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 596,396 | 5.964 | 20 | 50 | fits | 147,272 | 200 | 0.277 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 728,195 | 7.282 | 20 | 20 | fits | 131,865 | 62 | 0.681 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 1,058,288 | 10.583 | 20 | 20 | fits | 60,713 | 24 | 0.686 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 533,547 | 5.335 | 20 | 20 | fits | 154,103 | 202 | 0.320 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 440,054 | 4.401 | 20 | 200 | fits | 151,092 | 119 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 593,541 | 5.935 | 20 | 200 | fits | 154,103 | 202 | 0.320 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 440,978 | 4.410 | 20 | 20 | fits | 151,092 | 119 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 733,071 | 7.331 | 20 | 20 | fits | 128,447 | 60 | 0.705 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 146,769 | 1.468 | 20 | 24 | fits | 148,306 | 106 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 443,628 | 4.436 | 20 | 24 | fits | 151,092 | 119 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 443,562 | 4.436 | 20 | 50 | fits | 151,092 | 119 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 597,269 | 5.973 | 20 | 50 | fits | 154,103 | 202 | 0.320 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 736,029 | 7.360 | 20 | 20 | fits | 128,447 | 60 | 0.705 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 1,050,117 | 10.501 | 20 | 20 | fits | 50,598 | 20 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 566,085 | 5.661 | 20 | 20 | fits | 150,232 | 189 | 0.367 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 448,113 | 4.481 | 20 | 200 | fits | 150,862 | 132 | 0.438 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 608,301 | 6.083 | 20 | 200 | fits | 150,232 | 189 | 0.367 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 449,037 | 4.490 | 20 | 20 | fits | 150,862 | 132 | 0.438 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 742,226 | 7.422 | 20 | 20 | fits | 133,221 | 62 | 0.639 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 156,054 | 1.561 | 20 | 24 | fits | 148,306 | 106 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 451,687 | 4.517 | 20 | 24 | fits | 150,862 | 132 | 0.438 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 451,621 | 4.516 | 20 | 50 | fits | 150,862 | 132 | 0.438 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 612,029 | 6.120 | 20 | 50 | fits | 150,232 | 189 | 0.367 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 745,184 | 7.452 | 20 | 20 | fits | 133,221 | 62 | 0.639 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 1,059,384 | 10.594 | 20 | 20 | fits | 50,580 | 20 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 566,041 | 5.660 | 20 | 20 | fits | 147,952 | 202 | 0.270 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 449,059 | 4.491 | 20 | 200 | fits | 149,665 | 117 | 0.496 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 596,395 | 5.964 | 20 | 200 | fits | 147,952 | 202 | 0.270 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 449,983 | 4.500 | 20 | 20 | fits | 149,665 | 117 | 0.496 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 730,201 | 7.302 | 20 | 20 | fits | 133,102 | 62 | 0.635 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 149,303 | 1.493 | 20 | 24 | fits | 148,306 | 106 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 452,633 | 4.526 | 20 | 24 | fits | 149,665 | 117 | 0.496 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 452,567 | 4.526 | 20 | 50 | fits | 149,665 | 117 | 0.496 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 600,123 | 6.001 | 20 | 50 | fits | 147,952 | 202 | 0.270 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 733,159 | 7.332 | 20 | 20 | fits | 133,102 | 62 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 1,047,285 | 10.473 | 20 | 20 | fits | 50,581 | 20 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 568,069 | 5.681 | 20 | 20 | fits | 154,924 | 204 | 0.263 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 465,320 | 4.653 | 20 | 200 | fits | 153,153 | 125 | 0.443 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 619,628 | 6.196 | 20 | 200 | fits | 154,924 | 204 | 0.263 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 466,244 | 4.662 | 20 | 20 | fits | 153,153 | 125 | 0.443 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 754,640 | 7.546 | 20 | 20 | fits | 134,308 | 51 | 0.701 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 157,264 | 1.573 | 20 | 24 | fits | 148,306 | 106 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 468,894 | 4.689 | 20 | 24 | fits | 153,153 | 125 | 0.443 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 468,828 | 4.688 | 20 | 50 | fits | 153,153 | 125 | 0.443 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 623,356 | 6.234 | 20 | 50 | fits | 154,924 | 204 | 0.263 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 757,598 | 7.576 | 20 | 20 | fits | 134,308 | 51 | 0.701 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 1,051,212 | 10.512 | 20 | 20 | fits | 29,968 | 12 | 0.794 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 556,695 | 5.567 | 20 | 20 | fits | 152,998 | 193 | 0.336 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 445,027 | 4.450 | 20 | 200 | fits | 150,847 | 132 | 0.438 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 607,981 | 6.080 | 20 | 200 | fits | 152,998 | 193 | 0.336 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 445,951 | 4.460 | 20 | 20 | fits | 150,847 | 132 | 0.438 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 742,538 | 7.425 | 20 | 20 | fits | 133,853 | 57 | 0.670 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 153,247 | 1.532 | 20 | 24 | fits | 148,367 | 106 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 448,601 | 4.486 | 20 | 24 | fits | 150,847 | 132 | 0.438 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 448,535 | 4.485 | 20 | 50 | fits | 150,847 | 132 | 0.438 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 611,709 | 6.117 | 20 | 50 | fits | 152,998 | 193 | 0.336 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 745,496 | 7.455 | 20 | 20 | fits | 133,853 | 57 | 0.670 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 1,054,761 | 10.548 | 20 | 20 | fits | 45,917 | 22 | 0.778 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 556,469 | 5.565 | 20 | 20 | fits | 150,688 | 202 | 0.350 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 439,410 | 4.394 | 20 | 200 | fits | 151,064 | 120 | 0.432 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 599,725 | 5.997 | 20 | 200 | fits | 150,688 | 202 | 0.350 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 440,334 | 4.403 | 20 | 20 | fits | 151,064 | 120 | 0.432 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 734,460 | 7.345 | 20 | 20 | fits | 134,031 | 57 | 0.670 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 146,417 | 1.464 | 20 | 24 | fits | 148,367 | 106 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 442,984 | 4.430 | 20 | 24 | fits | 151,064 | 120 | 0.432 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 442,918 | 4.429 | 20 | 50 | fits | 151,064 | 120 | 0.432 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 603,453 | 6.035 | 20 | 50 | fits | 150,688 | 202 | 0.350 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 737,418 | 7.374 | 20 | 20 | fits | 134,031 | 57 | 0.670 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 1,125,562 | 11.256 | 20 | 20 | fits | 51,484 | 21 | 0.725 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 543,356 | 5.434 | 20 | 20 | fits | 155,389 | 205 | 0.269 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 458,134 | 4.581 | 20 | 200 | fits | 153,709 | 126 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 612,907 | 6.129 | 20 | 200 | fits | 155,389 | 205 | 0.269 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 459,058 | 4.591 | 20 | 20 | fits | 153,709 | 126 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 747,913 | 7.479 | 20 | 20 | fits | 134,302 | 51 | 0.701 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 154,378 | 1.544 | 20 | 24 | fits | 148,367 | 106 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 461,708 | 4.617 | 20 | 24 | fits | 153,709 | 126 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 461,642 | 4.616 | 20 | 50 | fits | 153,709 | 126 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 616,635 | 6.166 | 20 | 50 | fits | 155,389 | 205 | 0.269 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 750,871 | 7.509 | 20 | 20 | fits | 134,302 | 51 | 0.701 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,131,719 | 11.317 | 20 | 20 | fits | 43,224 | 23 | 0.734 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 548,811 | 5.488 | 20 | 20 | fits | 148,095 | 186 | 0.273 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 451,427 | 4.514 | 20 | 200 | fits | 152,578 | 137 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 598,906 | 5.989 | 20 | 200 | fits | 148,095 | 186 | 0.273 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 452,351 | 4.524 | 20 | 20 | fits | 152,578 | 137 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 731,381 | 7.314 | 20 | 20 | fits | 131,771 | 61 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 146,831 | 1.468 | 20 | 24 | fits | 148,368 | 107 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 455,001 | 4.550 | 20 | 24 | fits | 152,578 | 137 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 454,935 | 4.549 | 20 | 50 | fits | 152,578 | 137 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 602,634 | 6.026 | 20 | 50 | fits | 148,095 | 186 | 0.273 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 734,339 | 7.343 | 20 | 20 | fits | 131,771 | 61 | 0.681 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,143,800 | 11.438 | 20 | 20 | fits | 61,170 | 24 | 0.696 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 558,337 | 5.583 | 20 | 20 | fits | 153,698 | 200 | 0.315 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 447,225 | 4.472 | 20 | 200 | fits | 151,074 | 119 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 600,307 | 6.003 | 20 | 200 | fits | 153,698 | 200 | 0.315 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 448,149 | 4.481 | 20 | 20 | fits | 151,074 | 119 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 813,171 | 8.132 | 20 | 20 | fits | 134,533 | 59 | 0.670 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 154,954 | 1.550 | 20 | 24 | fits | 148,308 | 106 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 450,799 | 4.508 | 20 | 24 | fits | 151,074 | 119 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 450,733 | 4.507 | 20 | 50 | fits | 151,074 | 119 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 604,035 | 6.040 | 20 | 50 | fits | 153,698 | 200 | 0.315 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 816,129 | 8.161 | 20 | 20 | fits | 134,533 | 59 | 0.670 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,136,089 | 11.361 | 20 | 20 | fits | 50,502 | 20 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 544,562 | 5.446 | 20 | 20 | fits | 155,941 | 191 | 0.304 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 440,232 | 4.402 | 20 | 200 | fits | 150,911 | 131 | 0.439 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 595,557 | 5.956 | 20 | 200 | fits | 155,941 | 191 | 0.304 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 441,156 | 4.412 | 20 | 20 | fits | 150,911 | 131 | 0.439 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 801,790 | 8.018 | 20 | 20 | fits | 127,902 | 61 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 148,124 | 1.481 | 20 | 24 | fits | 148,308 | 106 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 443,806 | 4.438 | 20 | 24 | fits | 150,911 | 131 | 0.439 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 443,740 | 4.437 | 20 | 50 | fits | 150,911 | 131 | 0.439 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 599,285 | 5.993 | 20 | 50 | fits | 155,941 | 191 | 0.304 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 804,748 | 8.047 | 20 | 20 | fits | 127,902 | 61 | 0.685 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,132,618 | 11.326 | 20 | 20 | fits | 60,772 | 24 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 634,151 | 6.342 | 20 | 20 | fits | 151,818 | 207 | 0.314 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 446,127 | 4.461 | 20 | 200 | fits | 148,766 | 114 | 0.473 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 674,892 | 6.749 | 20 | 200 | fits | 151,818 | 207 | 0.314 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 447,051 | 4.471 | 20 | 20 | fits | 148,766 | 114 | 0.473 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 821,913 | 8.219 | 20 | 20 | fits | 135,780 | 63 | 0.667 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 156,164 | 1.562 | 20 | 24 | fits | 148,308 | 106 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 449,701 | 4.497 | 20 | 24 | fits | 148,766 | 114 | 0.473 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 449,635 | 4.496 | 20 | 50 | fits | 148,766 | 114 | 0.473 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 678,620 | 6.786 | 20 | 50 | fits | 151,818 | 207 | 0.314 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 824,871 | 8.249 | 20 | 20 | fits | 135,780 | 63 | 0.667 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,138,740 | 11.387 | 20 | 20 | fits | 50,594 | 20 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 640,970 | 6.410 | 20 | 20 | fits | 158,254 | 205 | 0.328 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 525,760 | 5.258 | 20 | 200 | fits | 153,496 | 126 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 693,911 | 6.939 | 20 | 200 | fits | 158,254 | 205 | 0.328 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 526,684 | 5.267 | 20 | 20 | fits | 153,496 | 126 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 829,440 | 8.294 | 20 | 20 | fits | 134,825 | 51 | 0.705 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 149,334 | 1.493 | 20 | 24 | fits | 148,308 | 106 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 529,334 | 5.293 | 20 | 24 | fits | 153,496 | 126 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 529,268 | 5.293 | 20 | 50 | fits | 153,496 | 126 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 697,639 | 6.976 | 20 | 50 | fits | 158,254 | 205 | 0.328 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 832,398 | 8.324 | 20 | 20 | fits | 134,825 | 51 | 0.705 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,131,367 | 11.314 | 20 | 20 | fits | 35,589 | 18 | 0.820 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 541,811 | 5.418 | 20 | 20 | fits | 154,985 | 204 | 0.263 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 439,001 | 4.390 | 20 | 200 | fits | 150,891 | 119 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 593,370 | 5.934 | 20 | 200 | fits | 154,985 | 204 | 0.263 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 439,925 | 4.399 | 20 | 20 | fits | 150,891 | 119 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 728,440 | 7.284 | 20 | 20 | fits | 134,366 | 52 | 0.700 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 145,917 | 1.459 | 20 | 24 | fits | 148,308 | 106 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 442,575 | 4.426 | 20 | 24 | fits | 150,891 | 119 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 442,509 | 4.425 | 20 | 50 | fits | 150,891 | 119 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 597,098 | 5.971 | 20 | 50 | fits | 154,985 | 204 | 0.263 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 731,398 | 7.314 | 20 | 20 | fits | 134,366 | 52 | 0.700 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 1,046,056 | 10.461 | 20 | 20 | fits | 45,129 | 22 | 0.762 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 531,227 | 5.312 | 20 | 20 | fits | 155,425 | 206 | 0.269 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 446,063 | 4.461 | 20 | 200 | fits | 150,988 | 119 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 600,872 | 6.009 | 20 | 200 | fits | 155,425 | 206 | 0.269 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 446,987 | 4.470 | 20 | 20 | fits | 150,988 | 119 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 740,990 | 7.410 | 20 | 20 | fits | 129,035 | 54 | 0.735 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 153,878 | 1.539 | 20 | 24 | fits | 148,308 | 106 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 449,637 | 4.496 | 20 | 24 | fits | 150,988 | 119 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 449,571 | 4.496 | 20 | 50 | fits | 150,988 | 119 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 604,600 | 6.046 | 20 | 50 | fits | 155,425 | 206 | 0.269 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 743,948 | 7.439 | 20 | 20 | fits | 129,035 | 54 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 1,053,439 | 10.534 | 20 | 20 | fits | 50,582 | 20 | 0.714 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 551,333 | 5.513 | 20 | 20 | fits | 153,062 | 193 | 0.336 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 439,665 | 4.397 | 20 | 200 | fits | 150,701 | 132 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 602,683 | 6.027 | 20 | 200 | fits | 153,062 | 193 | 0.336 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 440,589 | 4.406 | 20 | 20 | fits | 150,701 | 132 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 737,240 | 7.372 | 20 | 20 | fits | 133,853 | 57 | 0.670 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 146,771 | 1.468 | 20 | 24 | fits | 148,308 | 106 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 443,239 | 4.432 | 20 | 24 | fits | 150,701 | 132 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 443,173 | 4.432 | 20 | 50 | fits | 150,701 | 132 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 606,411 | 6.064 | 20 | 50 | fits | 153,062 | 193 | 0.336 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 740,198 | 7.402 | 20 | 20 | fits | 133,853 | 57 | 0.670 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 1,049,429 | 10.494 | 20 | 20 | fits | 50,576 | 20 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 563,989 | 5.640 | 20 | 20 | fits | 147,130 | 200 | 0.275 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 457,814 | 4.578 | 20 | 200 | fits | 152,379 | 122 | 0.452 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 604,328 | 6.043 | 20 | 200 | fits | 147,130 | 200 | 0.275 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 458,738 | 4.587 | 20 | 20 | fits | 152,379 | 122 | 0.452 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 736,648 | 7.366 | 20 | 20 | fits | 131,616 | 61 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 155,088 | 1.551 | 20 | 24 | fits | 148,308 | 106 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 461,388 | 4.614 | 20 | 24 | fits | 152,379 | 122 | 0.452 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 461,322 | 4.613 | 20 | 50 | fits | 152,379 | 122 | 0.452 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 608,056 | 6.081 | 20 | 50 | fits | 147,130 | 200 | 0.275 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 739,606 | 7.396 | 20 | 20 | fits | 131,616 | 61 | 0.679 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 1,053,545 | 10.535 | 20 | 20 | fits | 50,581 | 20 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 544,959 | 5.450 | 20 | 20 | fits | 154,092 | 201 | 0.317 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 451,383 | 4.514 | 20 | 200 | fits | 150,915 | 119 | 0.430 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 604,859 | 6.049 | 20 | 200 | fits | 154,092 | 201 | 0.317 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 452,307 | 4.523 | 20 | 20 | fits | 150,915 | 119 | 0.430 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 739,263 | 7.393 | 20 | 20 | fits | 133,700 | 57 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 148,286 | 1.483 | 20 | 24 | fits | 148,336 | 107 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 454,957 | 4.550 | 20 | 24 | fits | 150,915 | 119 | 0.430 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 454,891 | 4.549 | 20 | 50 | fits | 150,915 | 119 | 0.430 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 608,587 | 6.086 | 20 | 50 | fits | 154,092 | 201 | 0.317 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 742,221 | 7.422 | 20 | 20 | fits | 133,700 | 57 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 1,062,807 | 10.628 | 20 | 20 | fits | 46,102 | 23 | 0.806 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 562,429 | 5.624 | 20 | 20 | fits | 147,261 | 200 | 0.274 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 457,442 | 4.574 | 20 | 200 | fits | 149,027 | 114 | 0.475 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 604,087 | 6.041 | 20 | 200 | fits | 147,261 | 200 | 0.274 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 458,366 | 4.584 | 20 | 20 | fits | 149,027 | 114 | 0.475 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 737,712 | 7.377 | 20 | 20 | fits | 132,921 | 62 | 0.636 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 156,233 | 1.562 | 20 | 24 | fits | 148,322 | 107 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 461,016 | 4.610 | 20 | 24 | fits | 149,027 | 114 | 0.475 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 460,950 | 4.609 | 20 | 50 | fits | 149,027 | 114 | 0.475 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 607,815 | 6.078 | 20 | 50 | fits | 147,261 | 200 | 0.274 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 740,670 | 7.407 | 20 | 20 | fits | 132,921 | 62 | 0.636 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 1,071,218 | 10.712 | 20 | 20 | fits | 56,199 | 27 | 0.773 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 552,382 | 5.524 | 20 | 20 | fits | 156,198 | 206 | 0.261 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 438,365 | 4.384 | 20 | 200 | fits | 148,467 | 114 | 0.475 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 593,947 | 5.939 | 20 | 200 | fits | 156,198 | 206 | 0.261 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 439,289 | 4.393 | 20 | 20 | fits | 148,467 | 114 | 0.475 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 728,341 | 7.283 | 20 | 20 | fits | 133,690 | 58 | 0.667 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 148,965 | 1.490 | 20 | 24 | fits | 148,367 | 106 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 441,939 | 4.419 | 20 | 24 | fits | 148,467 | 114 | 0.475 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 441,873 | 4.419 | 20 | 50 | fits | 148,467 | 114 | 0.475 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 597,675 | 5.977 | 20 | 50 | fits | 156,198 | 206 | 0.261 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 731,299 | 7.313 | 20 | 20 | fits | 133,690 | 58 | 0.667 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 1,051,338 | 10.513 | 20 | 20 | fits | 50,442 | 20 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 538,676 | 5.387 | 20 | 20 | fits | 155,363 | 206 | 0.268 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 453,512 | 4.535 | 20 | 200 | fits | 151,121 | 119 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 608,259 | 6.083 | 20 | 200 | fits | 155,363 | 206 | 0.268 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 454,436 | 4.544 | 20 | 20 | fits | 151,121 | 119 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 748,304 | 7.483 | 20 | 20 | fits | 128,962 | 54 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 156,926 | 1.569 | 20 | 24 | fits | 148,367 | 106 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 457,086 | 4.571 | 20 | 24 | fits | 151,121 | 119 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 457,020 | 4.570 | 20 | 50 | fits | 151,121 | 119 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 611,987 | 6.120 | 20 | 50 | fits | 155,363 | 206 | 0.268 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 751,262 | 7.513 | 20 | 20 | fits | 128,962 | 54 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 1,055,288 | 10.553 | 20 | 20 | fits | 40,361 | 16 | 0.746 |
| LINK_UP | `adp.link_up.if0` | 2,142 | 0.021 | 20 | 200 | fits | 28,323 | 43 (11) | 0.662 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 19,669 | 0.197 | 20 | 200 | fits | 23,228 | 29 (39) | 0.538 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 14,845 | 0.148 | 20 | 200 | fits | 5,188 | 16 (11) | 0.280 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 18,664 | 0.187 | 20 | 20 | fits | 30,493 | 21 (35) | 0.769 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 18,902 | 0.189 | 20 | 20 | fits | 27,421 | 17 (14) | 0.807 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 14,986 | 0.150 | 20 | 20 | fits | 27,138 | 18 (14) | 0.805 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 19,891 | 0.199 | 20 | 20 | fits | 30,041 | 21 (35) | 0.750 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 76,034 | 0.760 | 20 | 20 | fits | 27,492 | 8 | 0.833 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 40,313 | 0.403 | 20 | 20 | fits | 40,379 | 12 | 0.877 |
| malformed MRPDU discard | `srp.malformed.if0` | 21,393 | 0.214 | 20 | 20 | fits | 21,459 | 12 | 0.675 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 72,349 | 0.723 | 220 | 220 | fits | 44,043 | 6 | 0.896 |
| an event behind 15 others | `backlog.event.if0` | 165,478 | 1.655 | 20 | 200 | fits | 71,230 | 78 | 0.498 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 604,911 | 6.049 | 20 | 20 | fits | 144,500 | 128 | 0.144 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 481,875 | 4.819 | 20 | 200 | fits | 175,919 | 91 | 0.477 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 625,759 | 6.258 | 20 | 200 | fits | 144,500 | 128 | 0.144 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 477,553 | 4.776 | 20 | 20 | fits | 175,919 | 91 | 0.477 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 621,217 | 6.212 | 20 | 20 | fits | 144,500 | 128 | 0.144 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 154,485 | 1.545 | 20 | 24 | fits | 155,376 | 112 | 0.455 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 480,203 | 4.802 | 20 | 24 | fits | 175,919 | 91 | 0.477 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 480,137 | 4.801 | 20 | 50 | fits | 175,919 | 91 | 0.477 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 624,241 | 6.242 | 20 | 50 | fits | 144,500 | 128 | 0.144 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 658,111 | 6.581 | 20 | 20 | fits | 33,936 | 56 | 0.118 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 724,670 | 7.247 | 20 | 20 | fits | 31,629 | 47 | 0.211 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 555,936 | 5.559 | 20 | 20 | fits | 155,010 | 192 | 0.299 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 451,605 | 4.516 | 20 | 200 | fits | 152,732 | 138 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 605,999 | 6.060 | 20 | 200 | fits | 155,010 | 192 | 0.299 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 452,529 | 4.525 | 20 | 20 | fits | 152,732 | 138 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 740,553 | 7.406 | 20 | 20 | fits | 133,850 | 57 | 0.671 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 148,759 | 1.488 | 20 | 24 | fits | 148,945 | 109 | 0.434 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 455,179 | 4.552 | 20 | 24 | fits | 152,732 | 138 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 455,113 | 4.551 | 20 | 50 | fits | 152,732 | 138 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 609,727 | 6.097 | 20 | 50 | fits | 155,010 | 192 | 0.299 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 743,511 | 7.435 | 20 | 20 | fits | 133,850 | 57 | 0.671 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,050,833 | 10.508 | 20 | 20 | fits | 43,775 | 23 | 0.748 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 18,319 | 0.183 | 20 | 20 | fits | 30,282 | 19 | 0.780 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 451,605 | 4.516 | 20 | 200 | fits | 152,732 | 138 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 38,819 | 0.388 | 20 | 200 | fits | 30,282 | 19 | 0.780 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 452,529 | 4.525 | 20 | 20 | fits | 152,732 | 138 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 737,427 | 7.374 | 20 | 20 | fits | 134,328 | 51 | 0.701 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 148,759 | 1.488 | 20 | 24 | fits | 148,945 | 109 | 0.434 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 455,179 | 4.552 | 20 | 24 | fits | 152,732 | 138 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 455,113 | 4.551 | 20 | 50 | fits | 152,732 | 138 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 606,123 | 6.061 | 20 | 50 | fits | 151,406 | 192 | 0.210 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 740,385 | 7.404 | 20 | 20 | fits | 134,328 | 51 | 0.701 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,038,920 | 10.389 | 20 | 20 | fits | 35,178 | 23 | 0.737 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,409,994 | 64.100 | 20 | 20 | MISS ceiling | 19,260 | 13 | 0.451 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,429,245 | 64.292 | 20 | 20 | MISS ceiling | 19,258 | 13 | 0.412 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,448,319 | 64.483 | 20 | 20 | MISS ceiling | 19,150 | 13 | 0.438 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,467,393 | 64.674 | 20 | 20 | MISS ceiling | 19,150 | 13 | 0.438 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,486,397 | 64.864 | 20 | 20 | MISS ceiling | 19,067 | 13 | 0.429 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 302,896 | 3.029 | 20 | 200 | fits | 152,597 | 238 | 0.231 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 431,442 | 4.314 | 20 | 200 | fits | 129,162 | 72 | 0.649 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 298,574 | 2.986 | 20 | 20 | fits | 152,597 | 238 | 0.231 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,312,992 | 63.130 | 20 | 20 | MISS ceiling | 31,715 | 15 | 0.649 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 149,617 | 1.496 | 20 | 24 | fits | 146,518 | 107 | 0.438 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,284,763 | 62.848 | 20 | 24 | MISS ceiling | 92,905 | 41 | 0.528 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 301,158 | 3.012 | 20 | 50 | fits | 152,597 | 238 | 0.231 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 429,924 | 4.299 | 20 | 50 | fits | 129,162 | 72 | 0.649 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 429,858 | 4.299 | 20 | 20 | fits | 129,162 | 72 | 0.649 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 750,301 | 7.503 | 20 | 20 | fits | 61,101 | 24 | 0.693 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 7,240 | 0.072 | 20 | 20 | fits | 25,194 | 13 (29) | 0.654 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 9,557 | 0.096 | 20 | 20 | fits | 28,781 | 19 (35) | 0.754 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 25,519 | 0.255 | 20 | 20 | fits | 30,300 | 21 (12) | 0.764 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 12,783 | 0.128 | 20 | 50 | fits | 28,323 | 43 | 0.662 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 13,894 | 0.139 | 20 | 50 | fits | 25,001 | 35 | 0.602 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 14,432 | 0.144 | 20 | 50 | fits | 25,271 | 35 | 0.621 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 24,839 | 0.248 | 20 | 50 | fits | 30,979 | 61 | 0.564 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 27,058 | 0.271 | 20 | 50 | fits | 30,979 | 61 | 0.564 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 12,489 | 0.125 | 20 | 50 | fits | 25,733 | 30 | 0.596 |
| LINK_UP | `adp.link_up.if0` | 2,142 | 0.021 | 20 | 200 | fits | 28,323 | 43 (11) | 0.662 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 19,669 | 0.197 | 20 | 200 | fits | 23,228 | 29 (39) | 0.538 |
| LINK_DOWN | `adp.link_down.if0` | 1,770 | 0.018 | 20 | 200 | fits | 27,542 | 23 (9) | 0.686 |
| LINK_UP | `adp.link_up.if0` | 2,142 | 0.021 | 20 | 200 | fits | 28,323 | 43 (11) | 0.662 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 19,669 | 0.197 | 20 | 200 | fits | 23,228 | 29 (39) | 0.538 |
| GM_CHANGE | `adp.gm_change.if0` | 2,083 | 0.021 | 20 | 200 | fits | 15,059 | 17 (11) | 0.323 |
| LINK_UP | `adp.link_up.if0` | 2,142 | 0.021 | 20 | 200 | fits | 28,323 | 43 (11) | 0.662 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 19,669 | 0.197 | 20 | 200 | fits | 23,228 | 29 (39) | 0.538 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 5,020 | 0.050 | 20 | 200 | fits | 16,771 | 16 (31) | 0.517 |
| LINK_UP | `adp.link_up.if0` | 2,142 | 0.021 | 20 | 200 | fits | 28,323 | 43 (11) | 0.662 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 19,669 | 0.197 | 20 | 200 | fits | 23,228 | 29 (39) | 0.538 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 5,020 | 0.050 | 20 | 200 | fits | 16,771 | 16 (31) | 0.517 |
| set_name | `aecp_fanout.set_name.if0` | 59,804 | 0.598 | 20 | 24 | fits | 60,096 | 89 | 0.560 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 54,721 | 0.547 | 20 | 24 | fits | 53,824 | 78 | 0.594 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 38,851 | 0.389 | 20 | 24 | fits | 48,931 | 79 | 0.552 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 53,829 | 0.538 | 20 | 24 | fits | 47,647 | 78 | 0.538 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 60,484 | 0.605 | 20 | 24 | fits | 60,896 | 109 | 0.578 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 279,293 | 2.793 | 20 | 24 | fits | 59,577 | 110 | 0.578 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 321,688 | 3.217 | 20 | 24 | fits | 50,451 | 67 | 0.590 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 43,628 | 0.436 | 20 | 24 | fits | 48,460 | 78 | 0.556 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 51,498 | 0.515 | 20 | 24 | fits | 47,284 | 79 | 0.533 |
| BIND_RX | `acmp.bind_rx.if0` | 19,158 | 0.192 | 20 | 20 | fits | 43,463 | 26 (77) | 0.754 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 11,178 | 0.112 | 20 | 20 | fits | 32,729 | 19 (32) | 0.804 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 9,445 | 0.094 | 20 | 20 | fits | 25,275 | 15 (47) | 0.673 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 15,763 | 0.158 | 20 | 20 | fits | 40,922 | 18 (50) | 0.822 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,560 | 0.106 | 20 | 20 | fits | 25,986 | 17 (48) | 0.645 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,169 | 0.092 | 20 | 20 | fits | 25,167 | 16 (48) | 0.604 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 8,512 | 0.085 | 20 | 20 | fits | 23,964 | 16 (48) | 0.591 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 8,622 | 0.086 | 20 | 20 | fits | 24,007 | 17 (48) | 0.585 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 23,118 | 0.231 | 20 | 24 | fits | 27,472 | 20 | 0.753 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 27,048 | 0.270 | 20 | 24 | fits | 40,076 | 20 | 0.676 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 11,808 | 0.118 | 20 | 24 | fits | 27,470 | 20 | 0.704 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 11,153 | 0.112 | 20 | 24 | fits | 26,820 | 20 | 0.695 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 14,288 | 0.143 | 20 | 24 | fits | 26,984 | 20 | 0.693 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 12,046 | 0.120 | 20 | 24 | fits | 27,405 | 20 | 0.695 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 14,440 | 0.144 | 20 | 24 | fits | 26,885 | 20 | 0.700 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 10,773 | 0.108 | 20 | 24 | fits | 26,362 | 20 | 0.710 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 14,359 | 0.144 | 20 | 24 | fits | 26,956 | 20 | 0.720 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 18,913 | 0.189 | 20 | 24 | fits | 35,741 | 27 | 0.603 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 11,094 | 0.111 | 20 | 24 | fits | 26,598 | 20 | 0.736 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 13,882 | 0.139 | 20 | 24 | fits | 26,558 | 20 | 0.740 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i79.c0.if0` | 11,178 | 0.112 | 20 | 24 | fits | 26,688 | 20 | 0.701 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 14,571 | 0.146 | 20 | 24 | fits | 27,247 | 20 | 0.706 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 11,294 | 0.113 | 20 | 24 | fits | 26,877 | 20 | 0.702 |
| get_configuration | `aecp.get_configuration.if0` | 12,521 | 0.125 | 20 | 24 | fits | 24,555 | 20 | 0.710 |
| entity_available | `aecp.entity_available.if0` | 12,247 | 0.122 | 20 | 24 | fits | 24,702 | 20 | 0.710 |
| get_name | `aecp.get_name.if0` | 12,132 | 0.121 | 20 | 24 | fits | 27,779 | 20 | 0.729 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 16,269 | 0.163 | 20 | 24 | fits | 29,127 | 25 | 0.714 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 12,326 | 0.123 | 20 | 24 | fits | 28,106 | 29 | 0.722 |
| get_as_path, refused ENTITY_MISBEHAVING | `aecp.get_as_path.if0` | 16,268 | 0.163 | 20 | 24 | fits | 27,878 | 29 | 0.720 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 9,593 | 0.096 | 20 | 24 | fits | 24,952 | 20 | 0.721 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 12,605 | 0.126 | 20 | 24 | fits | 23,991 | 20 | 0.689 |
| set_name | `aecp.set_name.if0` | 22,412 | 0.224 | 20 | 24 | fits | 46,411 | 43 | 0.745 |
| lock_entity | `aecp.lock_entity.if0` | 15,695 | 0.157 | 20 | 24 | fits | 35,848 | 34 | 0.764 |
| unlock_entity | `aecp.unlock_entity.if0` | 28,413 | 0.284 | 20 | 24 | fits | 36,610 | 33 | 0.774 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 143,937 | 1.439 | 20 | 24 | fits | 145,005 | 136 | 0.311 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 235,987 | 2.360 | 20 | 24 | fits | 138,775 | 120 | 0.293 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 238,644 | 2.386 | 20 | 24 | fits | 47,060 | 18 | 0.660 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 359,120 | 3.591 | 20 | 24 | fits | 79,359 | 17 | 0.652 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 335,046 | 3.350 | 20 | 24 | fits | 90,055 | 17 | 0.652 |
| READ_DESCRIPTOR held for a token (#917) | `aecp.held.read_descriptor.if0` | 527,826 | 5.278 | 20 | 24 | fits | 44,139 | 23 | 0.679 |
| LINK_UP | `fixture.link_up.if0` | 2,142 | 0.021 | 20 | 200 | fits | 28,323 | 43 (11) | 0.662 |
| malformed MRPDU discard | `fixture.malformed.if0` | 21,290 | 0.213 | 20 | 20 | fits | 21,356 | 12 | 0.687 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 33,841 | 0.338 | 20 | 24 | fits | 48,650 | 43 | 0.772 |
| LINK_DOWN | `fixture.link_down.if0` | 2,156 | 0.022 | 20 | 200 | fits | 29,743 | 23 (9) | 0.735 |
| BIND_RX | `fixture.bind_rx.if0` | 19,048 | 0.190 | 20 | 20 | fits | 42,976 | 26 (77) | 0.762 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 29,602 | 0.296 | 20 | 20 | fits | 42,091 | 35 (35) | 0.760 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 8,167 | 0.082 | 20 | 20 | fits | 27,015 | 13 (29) | 0.743 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 95,490 | 0.955 | 20 | 200 | fits | 95,594 | 77 | 0.724 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 95,490 | 0.955 | 20 | 200 | fits | 95,594 | 77 | 0.724 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 95,216 | 0.952 | 20 | 20 | fits | 95,594 | 77 | 0.724 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 95,216 | 0.952 | 20 | 20 | fits | 95,594 | 77 | 0.724 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 95,424 | 0.954 | 20 | 24 | fits | 95,594 | 77 | 0.724 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 95,424 | 0.954 | 20 | 24 | fits | 95,594 | 77 | 0.724 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 95,358 | 0.954 | 20 | 50 | fits | 95,594 | 77 | 0.724 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 95,358 | 0.954 | 20 | 50 | fits | 95,594 | 77 | 0.724 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 95,292 | 0.953 | 20 | 20 | fits | 95,594 | 77 | 0.724 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 95,292 | 0.953 | 20 | 20 | fits | 95,594 | 77 | 0.724 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `srp-bound`: wait quiet TIMEOUT
- `srp-bound`: wait quiet TIMEOUT
- `srp-bound`: wait quiet TIMEOUT
- `srp-bound`: wait quiet TIMEOUT
- `srp-bound`: wait quiet TIMEOUT
- `srp-bound`: wait quiet TIMEOUT
- `srp-bound`: wait quiet TIMEOUT
- `srp-bound`: wait quiet TIMEOUT
