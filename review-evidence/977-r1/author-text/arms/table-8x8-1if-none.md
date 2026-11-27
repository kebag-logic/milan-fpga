### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 117 paths and 7 of 993 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.208 (0.463) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.095 (0.253) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.085 (0.275) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.119 (0.478) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.104 (0.279) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.095 (0.253) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.103 (0.265) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.115 (0.284) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.100 (0.330) | fits | 0 acmp | 1 | 0 |
| ACMP's last record of its burst at a registering triple | 0 | `acmp.register_burst.t0.if0` (srp-register-burst) | 3.400 (4.144) | fits | 11 acmp | 1 | 0 |
| ACMP's last record of its burst at a registering triple | 0 | `acmp.register_burst.t1.if0` (srp-register-burst) | 3.854 (4.800) | fits | 11 acmp | 1 | 0 |
| ACMP's last record of its burst at a registering triple | 0 | `acmp.register_burst.t2.if0` (srp-register-burst) | 1.367 (2.495) | fits | 11 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.261 (0.629) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.219 (0.600) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.266 (0.565) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.270 (0.525) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.210 (0.638) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.183 (0.523) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.144 (0.424) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.052 (0.181) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.023 (0.164) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.024 (0.332) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.032 (0.312) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.139 (0.313) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.150 (0.477) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.188 (0.534) | fits | 0 aecp | 1 | 0 |
| get_as_path, refused ENTITY_MISBEHAVING | 0 | `aecp.get_as_path.if0` (aecp) | 0.222 (0.579) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.193 (0.545) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.160 (0.509) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.232 (0.591) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.185 (0.524) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR held for a token (#917) | 0 | `aecp.held.read_descriptor.if0` (aecp-held) | 5.341 (5.689) | fits | 16 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.221 (0.685) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.149 (0.481) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.342 (0.693) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.185 (0.529) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.176 (0.516) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.210 (0.559) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.253 (0.604) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.177 (0.520) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.206 (0.555) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.213 (0.564) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i79.c0.if0` (aecp) | 0.179 (0.518) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.215 (0.564) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.181 (0.522) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.213 (0.564) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.186 (0.528) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.213 (0.563) | fits | 0 aecp | 1 | 0 |
| AECP's last record of its burst at a registering triple | 0 | `aecp.register_burst.t0.if0` (srp-register-burst) | 4.494 (6.021) | fits | 15 aecp | 1 | 0 |
| AECP's last record of its burst at a registering triple | 0 | `aecp.register_burst.t1.if0` (srp-register-burst) | 5.551 (5.984) | fits | 15 aecp | 1 | 0 |
| AECP's last record of its burst at a registering triple | 0 | `aecp.register_burst.t2.if0` (srp-register-burst) | 5.591 (5.945) | fits | 15 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.146 (0.493) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.286 (0.768) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.189 (0.537) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.261 (0.671) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.384 (2.736) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.488 (0.805) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.570 (0.944) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.503 (0.906) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.498 (0.815) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.552 (0.933) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.253 (3.598) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.472 (0.807) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 2.404 (2.761) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.133 (2.583) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.611 (4.033) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.348 (3.768) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.400 (1.780) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.177 (6.413) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-aged2-7.adp_available.if0` (backlog-adp@blank-aged2-7) | 6.589 (7.175) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.157 (0.553) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.689 (2.339) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 64.103 (64.412) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.930 (65.251) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.354 (0.515) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 3.061 | fits | 11 acmp | 4 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-burst.held.adp.if0` (save-burst) | 3.079 | fits | 7 adp | 4 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-flight.held.aecp.if0` (save-flight) | 5.748 | fits | 14 aecp | 4 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 4.306 | fits | 6 maap | 4 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 10.236 | fits | 31 srp | 4 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.197 (0.545) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.115 (0.260) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.138 (0.312) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.177 (0.545) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.216 (0.543) | fits | 0 events | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-burst.mrpdu.periodic.if0` (save-burst) | 3.172 | fits | 0 srp | 10 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@program-7.service.acmp.first.if0` (backlog-adp@program-7) | 5.605 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 63.082 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@program-7.service.adp.first.if0` (backlog-adp@program-7) | 5.595 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-7.service.adp.last.if0` (backlog-adp@program-7) | 7.112 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@program-7.service.aecp.first.if0` (backlog-adp@program-7) | 2.455 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 63.117 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@program-7.service.maap.first.if0` (backlog-adp@program-7) | 5.630 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-7.service.maap.last.if0` (backlog-adp@program-7) | 7.149 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-7.service.srp.first.if0` (backlog-adp@program-7) | 8.519 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-1.service.srp.last.if0` (backlog-adp@blank-1) | 11.896 | fits | 31 srp | 77 | 0 |
| Talker Advertise RX for every input, bound | 0 | `srp.bound_advertise.if0` (srp-bound) | 1.257 (2.189) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.640 (0.705) | fits | 0 srp | 1 | 0 |
| Talker Advertise RX for every input, no binding (kept) | 0 | `srp.kept_advertise.if0` (srp-kept) | 0.966 (0.967) | fits | 0 srp | 1 | 0 |
| Talker Failed RX for every input, no binding (kept) | 0 | `srp.kept_failed.if0` (srp-kept) | 0.909 (0.910) | fits | 0 srp | 1 | 0 |
| Talker RX at the bound after a freed block (count) | 0 | `srp.kept_recount.if0` (srp-kept) | 0.639 (0.640) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.408 (0.409) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.246 (0.247) | fits | 0 srp | 2 | 0 |
| Talker Advertise RX for every input, bound | 0 | `srp.register_advertise.if0` (srp-register) | 1.033 (1.033) | fits | 0 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t0.r0.if0` (srp-register-burst) | 1.626 (2.156) | fits | 0 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t0.r1.if0` (srp-register-burst) | 1.625 (2.156) | fits | 1 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t0.r2.if0` (srp-register-burst) | 1.624 (2.156) | fits | 2 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t1.r0.if0` (srp-register-burst) | 1.744 (2.788) | fits | 0 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t1.r1.if0` (srp-register-burst) | 1.743 (2.787) | fits | 1 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t1.r2.if0` (srp-register-burst) | 1.742 (2.786) | fits | 2 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t2.r0.if0` (srp-register-burst) | 1.111 (1.345) | fits | 0 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t2.r1.if0` (srp-register-burst) | 1.110 (1.344) | fits | 1 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t2.r2.if0` (srp-register-burst) | 1.109 (1.343) | fits | 2 srp | 1 | 0 |
| our MRPDU after a registering triple (JoinTime wait) | 0 | `srp.register_tx.t0.if0` (srp-register-burst) | 5.005 (5.700) | fits | 2 srp | 1 | 0 |
| our MRPDU after a registering triple (JoinTime wait) | 0 | `srp.register_tx.t1.if0` (srp-register-burst) | 76.741 (78.417) | fits | 2 srp | 1 | 0 |
| our MRPDU after a registering triple (JoinTime wait) | 0 | `srp.register_tx.t2.if0` (srp-register-burst) | 156.299 (157.013) | fits | 2 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.536 (0.606) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 15.947 | 11 | 154,027 (1.540) | yes | - |
| backlog-adp@blank-1 | 0 | 15.815 | 11 | 153,595 (1.536) | yes | - |
| backlog-adp@blank-2 | 0 | 15.690 | 11 | 153,595 (1.536) | yes | - |
| backlog-adp@blank-3 | 0 | 15.565 | 11 | 153,595 (1.536) | yes | - |
| backlog-adp@blank-4 | 0 | 15.440 | 11 | 153,595 (1.536) | yes | - |
| backlog-adp@blank-5 | 0 | 15.315 | 11 | 153,595 (1.536) | yes | - |
| backlog-adp@blank-6 | 1 | 14.947 | 10 | 153,647 (1.536) | yes | - |
| backlog-adp@blank-7 | 1 | 14.947 | 10 | 153,647 (1.536) | yes | - |
| backlog-adp@program-0 | 0 | 13.823 | 11 | 154,148 (1.541) | yes | - |
| backlog-adp@program-1 | 0 | 13.573 | 11 | 154,148 (1.541) | yes | - |
| backlog-adp@program-2 | 0 | 13.354 | 11 | 155,143 (1.551) | yes | - |
| backlog-adp@program-3 | 0 | 14.680 | 12 | 154,124 (1.541) | yes | - |
| backlog-adp@program-4 | 0 | 14.430 | 12 | 154,124 (1.541) | yes | - |
| backlog-adp@program-5 | 0 | 14.180 | 12 | 154,124 (1.541) | yes | - |
| backlog-adp@program-6 | 0 | 13.930 | 12 | 154,124 (1.541) | yes | - |
| backlog-adp@program-7 | 0 | 13.476 | 11 | 155,591 (1.556) | yes | - |
| backlog-adp@verify-0 | 0 | 13.995 | 9 | 153,851 (1.539) | yes | - |
| backlog-adp@verify-1 | 0 | 13.870 | 9 | 153,851 (1.539) | yes | - |
| backlog-adp@verify-2 | 0 | 13.745 | 9 | 153,851 (1.539) | yes | - |
| backlog-adp@verify-3 | 0 | 14.554 | 9 | 153,851 (1.539) | yes | - |
| backlog-adp@verify-4 | 0 | 14.429 | 9 | 153,851 (1.539) | yes | - |
| backlog-adp@verify-5 | 0 | 14.304 | 9 | 153,851 (1.539) | yes | - |
| backlog-adp@verify-6 | 0 | 14.179 | 9 | 153,851 (1.539) | yes | - |
| backlog-adp@verify-7 | 0 | 14.054 | 9 | 153,851 (1.539) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 13.587 | 9 | 154,191 (1.542) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 15.648 | 10 | 153,585 (1.536) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 14.528 | 10 | 154,356 (1.544) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 14.541 | 10 | 155,546 (1.555) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 14.590 | 10 | 153,826 (1.538) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 16.511 | 10 | 153,851 (1.539) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 18.670 | 12 | 154,495 (1.545) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 15.798 | 11 | 156,803 (1.568) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 13.649 | 9 | 153,851 (1.539) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 13.698 | 9 | 153,703 (1.537) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 13.710 | 9 | 153,907 (1.539) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 15.942 | 11 | 153,632 (1.536) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 13.903 | 10 | 155,402 (1.554) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 13.760 | 10 | 153,582 (1.536) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 14.885 | 11 | 154,954 (1.550) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 13.706 | 10 | 154,059 (1.541) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 12.936 | 9 | 153,644 (1.536) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 13.176 | 9 | 153,851 (1.539) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 13.060 | 8 | 153,736 (1.537) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 13.418 | 11 | 156,803 (1.568) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 13.247 | 10 | 155,527 (1.555) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 13.253 | 10 | 150,937 (1.509) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 13.466 | 11 | 155,178 (1.552) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 13.186 | 9 | 154,223 (1.542) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 13.127 | 10 | 153,957 (1.540) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 13.158 | 10 | 154,200 (1.542) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 13.053 | 9 | 154,009 (1.540) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 13.102 | 9 | 153,851 (1.539) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 13.163 | 9 | 156,170 (1.562) | yes | - |
| backlog-adp@program-aged1-5 | 1 | 14.697 | 10 | 154,606 (1.546) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 13.515 | 11 | 154,046 (1.540) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 13.170 | 11 | 155,516 (1.555) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 13.722 | 10 | 153,790 (1.538) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 14.515 | 9 | 155,535 (1.555) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 14.413 | 9 | 154,009 (1.540) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 18.621 | 12 | 153,795 (1.538) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 17.817 | 12 | 156,170 (1.562) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 16.898 | 12 | 154,665 (1.547) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 14.849 | 11 | 154,419 (1.544) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 14.587 | 9 | 152,604 (1.526) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 15.872 | 11 | 156,803 (1.568) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 13.844 | 10 | 155,527 (1.555) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 13.859 | 10 | 153,957 (1.540) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 13.801 | 9 | 154,059 (1.541) | yes | - |
| backlog-adp@verify-aged1-4 | 1 | 13.657 | 8 | 153,907 (1.539) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 13.696 | 9 | 153,558 (1.536) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 15.877 | 11 | 150,796 (1.508) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 13.855 | 11 | 155,346 (1.553) | yes | - |
| backlog | 0 | 8.433 | 8 | 178,932 (1.789) | yes | - |
| backlog-adp | 0 | 11.834 | 11 | 154,999 (1.550) | yes | - |
| backlog-adp-refill | 0 | 40.856 | 23 | 154,999 (1.550) | yes | - |
| backlog-owed | 0 | 65.612 | 23 | 176,211 (1.762) | yes | - |
| fixture | 0 | 1.476 | 2 | 96,492 (0.965) | yes | - |

Composed maximum over the 4 backlog windows: 178,932 CPU cycles (1.789 ms), backlog.
Over the windows that released their whole load only: 178,932 (1.789 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 157210 | 0 | 53,580 (0.536) | fits |
| srp-kept | 1909 | 0 | 96,659 (0.967) | fits |
| save-burst | 2974 | 0 | 164,593 (1.646) | fits |
| save-held | 3167 | 0 | 165,465 (1.655) | fits |
| save-starved | 72266 | 0 | 165,531 (1.655) | fits |
| save-flight | 2726 | 0 | 165,800 (1.658) | fits |
| acmp-notk | 3356 | 0 | 116,842 (1.168) | fits |
| srp-bound | 5943 | 0 | 123,254 (1.233) | fits |
| adp-advertise | 741 | 0 | 31,162 (0.312) | fits |
| backlog-adp@blank-0 | 473 | 0 | 154,027 (1.540) | fits |
| backlog-adp@blank-1 | 473 | 0 | 153,595 (1.536) | fits |
| backlog-adp@blank-2 | 473 | 0 | 153,595 (1.536) | fits |
| backlog-adp@blank-3 | 473 | 0 | 153,595 (1.536) | fits |
| backlog-adp@blank-4 | 473 | 0 | 153,595 (1.536) | fits |
| backlog-adp@blank-5 | 473 | 0 | 153,595 (1.536) | fits |
| backlog-adp@blank-6 | 473 | 0 | 153,647 (1.536) | fits |
| backlog-adp@blank-7 | 473 | 0 | 153,647 (1.536) | fits |
| backlog-adp@program-0 | 510 | 0 | 154,148 (1.541) | fits |
| backlog-adp@program-1 | 510 | 0 | 154,148 (1.541) | fits |
| backlog-adp@program-2 | 510 | 0 | 155,143 (1.551) | fits |
| backlog-adp@program-3 | 511 | 0 | 154,124 (1.541) | fits |
| backlog-adp@program-4 | 511 | 0 | 154,124 (1.541) | fits |
| backlog-adp@program-5 | 511 | 0 | 154,124 (1.541) | fits |
| backlog-adp@program-6 | 511 | 0 | 154,124 (1.541) | fits |
| backlog-adp@program-7 | 510 | 0 | 155,591 (1.556) | fits |
| backlog-adp@verify-0 | 531 | 0 | 153,851 (1.539) | fits |
| backlog-adp@verify-1 | 531 | 0 | 153,851 (1.539) | fits |
| backlog-adp@verify-2 | 531 | 0 | 153,851 (1.539) | fits |
| backlog-adp@verify-3 | 531 | 0 | 153,851 (1.539) | fits |
| backlog-adp@verify-4 | 531 | 0 | 153,851 (1.539) | fits |
| backlog-adp@verify-5 | 531 | 0 | 153,851 (1.539) | fits |
| backlog-adp@verify-6 | 531 | 0 | 153,851 (1.539) | fits |
| backlog-adp@verify-7 | 531 | 0 | 153,851 (1.539) | fits |
| backlog-adp@blank-aged2-0 | 754 | 0 | 154,191 (1.542) | fits |
| backlog-adp@blank-aged2-1 | 763 | 0 | 153,585 (1.536) | fits |
| backlog-adp@blank-aged2-2 | 770 | 0 | 154,356 (1.544) | fits |
| backlog-adp@blank-aged2-3 | 778 | 0 | 155,546 (1.555) | fits |
| backlog-adp@blank-aged2-4 | 786 | 0 | 153,826 (1.538) | fits |
| backlog-adp@blank-aged2-5 | 794 | 0 | 153,851 (1.539) | fits |
| backlog-adp@blank-aged2-6 | 804 | 0 | 154,495 (1.545) | fits |
| backlog-adp@blank-aged2-7 | 811 | 0 | 156,803 (1.568) | fits |
| backlog-adp@blank-aged1-0 | 691 | 0 | 153,851 (1.539) | fits |
| backlog-adp@blank-aged1-1 | 699 | 0 | 153,703 (1.537) | fits |
| backlog-adp@blank-aged1-2 | 707 | 0 | 153,907 (1.539) | fits |
| backlog-adp@blank-aged1-3 | 717 | 0 | 153,632 (1.536) | fits |
| backlog-adp@blank-aged1-4 | 724 | 0 | 155,402 (1.554) | fits |
| backlog-adp@blank-aged1-5 | 731 | 0 | 153,582 (1.536) | fits |
| backlog-adp@blank-aged1-6 | 740 | 0 | 154,954 (1.550) | fits |
| backlog-adp@blank-aged1-7 | 747 | 0 | 154,059 (1.541) | fits |
| backlog-adp@program-aged2-0 | 795 | 0 | 153,644 (1.536) | fits |
| backlog-adp@program-aged2-1 | 803 | 0 | 153,851 (1.539) | fits |
| backlog-adp@program-aged2-2 | 810 | 0 | 153,736 (1.537) | fits |
| backlog-adp@program-aged2-3 | 820 | 0 | 156,803 (1.568) | fits |
| backlog-adp@program-aged2-4 | 827 | 0 | 155,527 (1.555) | fits |
| backlog-adp@program-aged2-5 | 835 | 0 | 150,937 (1.509) | fits |
| backlog-adp@program-aged2-6 | 844 | 0 | 155,178 (1.552) | fits |
| backlog-adp@program-aged2-7 | 850 | 0 | 154,223 (1.542) | fits |
| backlog-adp@program-aged1-0 | 733 | 0 | 153,957 (1.540) | fits |
| backlog-adp@program-aged1-1 | 741 | 0 | 154,200 (1.542) | fits |
| backlog-adp@program-aged1-2 | 748 | 0 | 154,009 (1.540) | fits |
| backlog-adp@program-aged1-3 | 756 | 0 | 153,851 (1.539) | fits |
| backlog-adp@program-aged1-4 | 764 | 0 | 156,170 (1.562) | fits |
| backlog-adp@program-aged1-5 | 773 | 0 | 154,606 (1.546) | fits |
| backlog-adp@program-aged1-6 | 781 | 0 | 154,046 (1.540) | fits |
| backlog-adp@program-aged1-7 | 789 | 0 | 155,516 (1.555) | fits |
| backlog-adp@verify-aged2-0 | 816 | 0 | 153,790 (1.538) | fits |
| backlog-adp@verify-aged2-1 | 823 | 0 | 155,535 (1.555) | fits |
| backlog-adp@verify-aged2-2 | 830 | 0 | 154,009 (1.540) | fits |
| backlog-adp@verify-aged2-3 | 841 | 0 | 153,795 (1.538) | fits |
| backlog-adp@verify-aged2-4 | 849 | 0 | 156,170 (1.562) | fits |
| backlog-adp@verify-aged2-5 | 857 | 0 | 154,665 (1.547) | fits |
| backlog-adp@verify-aged2-6 | 864 | 0 | 154,419 (1.544) | fits |
| backlog-adp@verify-aged2-7 | 870 | 0 | 164,751 (1.648) | fits |
| backlog-adp@verify-aged1-0 | 754 | 0 | 156,803 (1.568) | fits |
| backlog-adp@verify-aged1-1 | 761 | 0 | 155,527 (1.555) | fits |
| backlog-adp@verify-aged1-2 | 769 | 0 | 153,957 (1.540) | fits |
| backlog-adp@verify-aged1-3 | 776 | 0 | 154,059 (1.541) | fits |
| backlog-adp@verify-aged1-4 | 783 | 0 | 153,907 (1.539) | fits |
| backlog-adp@verify-aged1-5 | 791 | 0 | 153,558 (1.536) | fits |
| backlog-adp@verify-aged1-6 | 801 | 0 | 150,796 (1.508) | fits |
| backlog-adp@verify-aged1-7 | 809 | 0 | 155,346 (1.553) | fits |
| acmp-noresp | 1880 | 0 | 116,255 (1.163) | fits |
| save | 608 | 0 | 87,667 (0.877) | fits |
| srp-register-burst | 4037 | 0 | 162,374 (1.624) | fits |
| adp-link | 234 | 0 | 42,975 (0.430) | fits |
| adp-gm | 233 | 0 | 31,162 (0.312) | fits |
| adp-discover | 233 | 0 | 31,162 (0.312) | fits |
| control | 233 | 0 | 31,162 (0.312) | fits |
| srp | 289 | 0 | 40,898 (0.409) | fits |
| backlog | 286 | 0 | 178,932 (1.789) | fits |
| backlog-adp | 312 | 0 | 154,999 (1.550) | fits |
| backlog-adp-refill | 324 | 0 | 154,999 (1.550) | fits |
| backlog-owed | 307 | 0 | 176,211 (1.762) | fits |
| acmp-disc | 876 | 0 | 116,329 (1.163) | fits |
| srp-register | 1883 | 0 | 118,137 (1.181) | fits |
| maap | 183 | 0 | 31,162 (0.312) | fits |
| aecp-fanout | 111 | 0 | 65,541 (0.655) | fits |
| acmp-cmd | 87 | 0 | 46,175 (0.462) | fits |
| aecp | 113 | 0 | 50,200 (0.502) | fits |
| aecp-largest-notice | 104 | 0 | 149,311 (1.493) | fits |
| aecp-held | 103 | 0 | 41,958 (0.420) | fits |
| datapath-events | 119 | 0 | 31,162 (0.312) | fits |
| fixture | 161 | 0 | 96,492 (0.965) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | +10.940 ms, 77,172 (0.772 ms), read-back | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 10.902 (20) | 9.098 |
| backlog-adp@blank-aged2-1 | 2 | +10.163 ms, 77,172 (0.772 ms), read-back | none | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 11.578 (20) | 8.422 |
| backlog-adp@blank-aged2-2 | 2 | +8.807 ms, 77,172 (0.772 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 11.559 (20) | 8.441 |
| backlog-adp@blank-aged2-3 | 2 | +7.527 ms, 77,418 (0.774 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 11.723 (20) | 8.277 |
| backlog-adp@blank-aged2-4 | 2 | +6.220 ms, 76,881 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 11.772 (20) | 8.228 |
| backlog-adp@blank-aged2-5 | 2 | +6.126 ms, 76,881 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 11.673 (20) | 8.327 |
| backlog-adp@blank-aged2-6 | 2 | +4.609 ms, 76,905 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 11.705 (20) | 8.295 |
| backlog-adp@blank-aged2-7 | 2 | +3.160 ms, 76,638 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 11.732 (20) | 8.268 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 10.830 (20) | 9.170 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 10.879 (20) | 9.121 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 10.880 (20) | 9.120 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 10.945 (20) | 9.055 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 10.761 (20) | 9.239 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 10.938 (20) | 9.062 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 10.963 (20) | 9.037 |
| backlog-adp@blank-aged1-7 | 1 | none | +11.086 ms, 76,640 (0.766 ms), read-back | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 10.848 (20) | 9.152 |
| backlog-adp@program-aged2-0 | 2 | none | +10.928 ms, 80,928 (0.809 ms), issue | `backlog-adp@program-aged2-0.service.srp.last.if0` | 10.890 (20) | 9.110 |
| backlog-adp@program-aged2-1 | 2 | +10.277 ms, 81,081 (0.811 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 11.735 (20) | 8.265 |
| backlog-adp@program-aged2-2 | 2 | +8.842 ms, 81,075 (0.811 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 11.613 (20) | 8.387 |
| backlog-adp@program-aged2-3 | 2 | +7.559 ms, 81,321 (0.813 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 11.646 (20) | 8.354 |
| backlog-adp@program-aged2-4 | 2 | +6.203 ms, 80,772 (0.808 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 11.802 (20) | 8.198 |
| backlog-adp@program-aged2-5 | 2 | +4.650 ms, 81,006 (0.810 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 11.806 (20) | 8.194 |
| backlog-adp@program-aged2-6 | 2 | +4.705 ms, 81,006 (0.810 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 11.840 (20) | 8.160 |
| backlog-adp@program-aged2-7 | 2 | +3.140 ms, 80,070 (0.801 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 11.736 (20) | 8.264 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 10.930 (20) | 9.070 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 10.964 (20) | 9.036 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 10.856 (20) | 9.144 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 10.897 (20) | 9.103 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 10.958 (20) | 9.042 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 10.806 (20) | 9.194 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 10.794 (20) | 9.206 |
| backlog-adp@program-aged1-7 | 1 | none | +11.174 ms, 80,806 (0.808 ms), issue | `backlog-adp@program-aged1-7.service.srp.last.if0` | 10.936 (20) | 9.064 |
| backlog-adp@verify-aged2-0 | 2 | none | +11.057 ms, 77,806 (0.778 ms), read-back | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 11.020 (20) | 8.980 |
| backlog-adp@verify-aged2-1 | 2 | none | none | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 11.673 (20) | 8.327 |
| backlog-adp@verify-aged2-2 | 2 | +8.842 ms, 77,806 (0.778 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 11.571 (20) | 8.429 |
| backlog-adp@verify-aged2-3 | 2 | +7.561 ms, 78,077 (0.781 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 11.611 (20) | 8.389 |
| backlog-adp@verify-aged2-4 | 2 | +6.262 ms, 77,722 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 11.673 (20) | 8.327 |
| backlog-adp@verify-aged2-5 | 2 | +6.272 ms, 77,722 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 11.682 (20) | 8.318 |
| backlog-adp@verify-aged2-6 | 2 | +4.723 ms, 77,600 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 11.823 (20) | 8.177 |
| backlog-adp@verify-aged2-7 | 2 | +4.697 ms, 77,600 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 11.741 (20) | 8.259 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 10.851 (20) | 9.149 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 10.998 (20) | 9.002 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 11.012 (20) | 8.988 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 10.955 (20) | 9.045 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 10.812 (20) | 9.188 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 10.844 (20) | 9.156 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 10.857 (20) | 9.143 |
| backlog-adp@verify-aged1-7 | 1 | none | +11.210 ms, 77,400 (0.774 ms), read-back | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 10.797 (20) | 9.203 |

Least margin over the aged windows: 8.160 ms, `backlog-adp@program-aged2-6.service.srp.last.if0` at 11.840 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 23789.603 | 23,830 | 398 | 2 | 30.927 | yes | within |
| save-held | 1358.172 | 12,950 | 398 | - | 32.845 | no | within |
| save-starved | 12927.551 | 12,950 | 398 | - | 35.254 | yes | within |
| save | 1305.420 | 12,950 | 398 | - | 104.503 | no | within |

Names from their response to durable (save_burst.py; #920, #665's ruling of 2026-11-15, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-burst | 115 | 1365.075 (0) | 5,000 | 7 | - | - | sequence 7, 0 missing | within |
| save-flight | 1 | 674.812 (0) | 5,000 | 2 | - | - | 61 steps (want 61), 28.031 ms | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1112 | 82,701 (0.827) | 78,609 (0.786) |
| srp-kept | 1844 | 23,926 (0.239) | 2,982 (0.030) |
| save-burst | 4214 | 106,085 (1.061) | 79,200 (0.792) |
| save-held | 1972 | 98,754 (0.988) | 79,057 (0.791) |
| save-starved | 714 | 82,488 (0.825) | 78,699 (0.787) |
| save-flight | 2094 | 98,122 (0.981) | 79,064 (0.791) |
| acmp-notk | 1430 | 116,842 (1.168) | 78,906 (0.789) |
| srp-bound | 2508 | 123,254 (1.233) | 79,074 (0.791) |
| adp-advertise | 717 | 23,568 (0.236) | 2,982 (0.030) |
| backlog-adp@blank-0 | 385 | 93,896 (0.939) | 76,671 (0.767) |
| backlog-adp@blank-1 | 385 | 93,915 (0.939) | 76,671 (0.767) |
| backlog-adp@blank-2 | 385 | 93,915 (0.939) | 76,671 (0.767) |
| backlog-adp@blank-3 | 385 | 93,915 (0.939) | 76,671 (0.767) |
| backlog-adp@blank-4 | 385 | 93,915 (0.939) | 76,671 (0.767) |
| backlog-adp@blank-5 | 385 | 93,915 (0.939) | 76,671 (0.767) |
| backlog-adp@blank-6 | 385 | 93,915 (0.939) | 76,671 (0.767) |
| backlog-adp@blank-7 | 385 | 93,915 (0.939) | 76,671 (0.767) |
| backlog-adp@program-0 | 499 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@program-1 | 499 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@program-2 | 499 | 98,491 (0.985) | 79,301 (0.793) |
| backlog-adp@program-3 | 502 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@program-4 | 502 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@program-5 | 502 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@program-6 | 502 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@program-7 | 502 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@verify-0 | 608 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@verify-1 | 608 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@verify-2 | 608 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@verify-3 | 609 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@verify-4 | 609 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@verify-5 | 609 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@verify-6 | 609 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@verify-7 | 609 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@blank-aged2-0 | 381 | 95,317 (0.953) | 76,178 (0.762) |
| backlog-adp@blank-aged2-1 | 383 | 95,974 (0.960) | 76,545 (0.765) |
| backlog-adp@blank-aged2-2 | 382 | 97,187 (0.972) | 76,670 (0.767) |
| backlog-adp@blank-aged2-3 | 382 | 93,939 (0.939) | 76,535 (0.765) |
| backlog-adp@blank-aged2-4 | 382 | 93,862 (0.939) | 76,535 (0.765) |
| backlog-adp@blank-aged2-5 | 384 | 93,862 (0.939) | 76,535 (0.765) |
| backlog-adp@blank-aged2-6 | 386 | 99,722 (0.997) | 76,855 (0.769) |
| backlog-adp@blank-aged2-7 | 383 | 95,872 (0.959) | 76,770 (0.768) |
| backlog-adp@blank-aged1-0 | 381 | 94,152 (0.942) | 76,828 (0.768) |
| backlog-adp@blank-aged1-1 | 381 | 94,203 (0.942) | 76,830 (0.768) |
| backlog-adp@blank-aged1-2 | 381 | 94,658 (0.947) | 76,931 (0.769) |
| backlog-adp@blank-aged1-3 | 383 | 96,011 (0.960) | 77,014 (0.770) |
| backlog-adp@blank-aged1-4 | 381 | 92,533 (0.925) | 76,815 (0.768) |
| backlog-adp@blank-aged1-5 | 381 | 94,307 (0.943) | 76,830 (0.768) |
| backlog-adp@blank-aged1-6 | 382 | 94,221 (0.942) | 76,830 (0.768) |
| backlog-adp@blank-aged1-7 | 381 | 93,326 (0.933) | 76,042 (0.760) |
| backlog-adp@program-aged2-0 | 495 | 98,491 (0.985) | 78,646 (0.786) |
| backlog-adp@program-aged2-1 | 496 | 98,491 (0.985) | 78,774 (0.788) |
| backlog-adp@program-aged2-2 | 496 | 98,491 (0.985) | 78,713 (0.787) |
| backlog-adp@program-aged2-3 | 496 | 98,491 (0.985) | 78,796 (0.788) |
| backlog-adp@program-aged2-4 | 496 | 98,491 (0.985) | 78,822 (0.788) |
| backlog-adp@program-aged2-5 | 496 | 98,491 (0.985) | 78,721 (0.787) |
| backlog-adp@program-aged2-6 | 496 | 98,491 (0.985) | 78,721 (0.787) |
| backlog-adp@program-aged2-7 | 496 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@program-aged1-0 | 495 | 98,491 (0.985) | 79,381 (0.794) |
| backlog-adp@program-aged1-1 | 495 | 98,491 (0.985) | 79,383 (0.794) |
| backlog-adp@program-aged1-2 | 495 | 98,491 (0.985) | 79,383 (0.794) |
| backlog-adp@program-aged1-3 | 495 | 98,771 (0.988) | 79,399 (0.794) |
| backlog-adp@program-aged1-4 | 495 | 98,786 (0.988) | 79,399 (0.794) |
| backlog-adp@program-aged1-5 | 498 | 103,415 (1.034) | 79,399 (0.794) |
| backlog-adp@program-aged1-6 | 496 | 106,503 (1.065) | 79,453 (0.795) |
| backlog-adp@program-aged1-7 | 495 | 98,491 (0.985) | 78,739 (0.787) |
| backlog-adp@verify-aged2-0 | 608 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@verify-aged2-1 | 609 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@verify-aged2-2 | 609 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@verify-aged2-3 | 613 | 100,498 (1.005) | 78,380 (0.784) |
| backlog-adp@verify-aged2-4 | 612 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@verify-aged2-5 | 611 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@verify-aged2-6 | 609 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@verify-aged2-7 | 609 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@verify-aged1-0 | 610 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@verify-aged1-1 | 608 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@verify-aged1-2 | 608 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@verify-aged1-3 | 608 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@verify-aged1-4 | 608 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@verify-aged1-5 | 608 | 98,491 (0.985) | 78,380 (0.784) |
| backlog-adp@verify-aged1-6 | 610 | 100,837 (1.008) | 78,380 (0.784) |
| backlog-adp@verify-aged1-7 | 608 | 98,491 (0.985) | 78,380 (0.784) |
| acmp-noresp | 981 | 116,255 (1.163) | 78,517 (0.785) |
| save | 953 | 96,826 (0.968) | 78,424 (0.784) |
| srp-register-burst | 686 | 119,436 (1.194) | 79,219 (0.792) |
| adp-link | 219 | 23,568 (0.236) | 2,982 (0.030) |
| adp-gm | 219 | 23,568 (0.236) | 2,982 (0.030) |
| adp-discover | 219 | 23,568 (0.236) | 2,982 (0.030) |
| control | 219 | 23,568 (0.236) | 2,982 (0.030) |
| srp | 271 | 23,568 (0.236) | 2,982 (0.030) |
| backlog | 266 | 23,568 (0.236) | 2,982 (0.030) |
| backlog-adp | 271 | 23,568 (0.236) | 3,215 (0.032) |
| backlog-adp-refill | 274 | 23,568 (0.236) | 3,193 (0.032) |
| backlog-owed | 277 | 23,568 (0.236) | 3,184 (0.032) |
| acmp-disc | 672 | 116,329 (1.163) | 78,517 (0.785) |
| srp-register | 454 | 118,137 (1.181) | 78,841 (0.788) |
| maap | 172 | 23,523 (0.235) | 2,982 (0.030) |
| aecp-fanout | 80 | 23,523 (0.235) | 3,087 (0.031) |
| acmp-cmd | 66 | 23,523 (0.235) | 3,065 (0.031) |
| aecp | 80 | 23,523 (0.235) | 2,982 (0.030) |
| aecp-largest-notice | 78 | 23,523 (0.235) | 3,287 (0.033) |
| aecp-held | 93 | 23,523 (0.235) | 2,982 (0.030) |
| datapath-events | 70 | 23,523 (0.235) | 2,982 (0.030) |
| fixture | 54 | 18,648 (0.186) | 3,065 (0.031) |

Longest pass that carries a step: 123,254 CPU cycles (1.233 ms), srp-bound; longest step: 79,453 (0.795 ms), backlog-adp@program-aged1-6.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| Talker Advertise RX for every input, no binding (kept) | `srp.kept_advertise.if0` | 96,593 | 0.966 | 20 | 20 | fits | 96,659 | 25 | 0.873 |
| Talker RX at the bound after a freed block (count) | `srp.kept_recount.if0` | 63,886 | 0.639 | 20 | 20 | fits | 63,952 | 25 | 0.854 |
| Talker Failed RX for every input, no binding (kept) | `srp.kept_failed.if0` | 90,927 | 0.909 | 20 | 20 | fits | 90,995 | 23 | 0.884 |
| ADP record, every channel at its refill rate, the longest | `save-burst.held.adp.if0` | 307,851 | 3.079 | 20 | 200 | fits | 72,555 | 64 | 0.296 |
| ACMP record, every channel at its refill rate, the longest | `save-burst.held.acmp.if0` | 287,583 | 2.876 | 20 | 20 | fits | 72,555 | 64 | 0.296 |
| AECP record, every channel at its refill rate, the longest | `save-burst.held.aecp.if0` | 240,605 | 2.406 | 20 | 24 | fits | 112,253 | 92 | 0.691 |
| MAAP record, every channel at its refill rate, the longest | `save-burst.held.maap.if0` | 238,075 | 2.381 | 20 | 50 | fits | 134,034 | 143 | 0.582 |
| SRP record, every channel at its refill rate, the longest | `save-burst.held.srp.if0` | 732,190 | 7.322 | 20 | 20 | fits | 103,278 | 97 | 0.673 |
| an MRPDU its join timer owes, the longest | `save-burst.mrpdu.join.if0` | 42,292 | 0.423 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-burst.mrpdu.leaveall.if0` | 41,443 | 0.414 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-burst.mrpdu.periodic.if0` | 317,159 | 3.172 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 297,442 | 2.974 | 20 | 200 | fits | 133,789 | 147 | 0.556 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 306,105 | 3.061 | 20 | 20 | fits | 91,560 | 77 | 0.534 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 470,132 | 4.701 | 20 | 24 | fits | 82,150 | 36 | 0.513 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 237,830 | 2.378 | 20 | 50 | fits | 133,789 | 147 | 0.556 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 1,010,834 | 10.108 | 20 | 20 | fits | 88,862 | 86 | 0.630 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 43,953 | 0.440 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 43,953 | 0.440 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 294,033 | 2.940 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 299,923 | 2.999 | 20 | 200 | fits | 136,270 | 153 | 0.565 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 279,786 | 2.798 | 20 | 20 | fits | 136,270 | 153 | 0.565 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 485,262 | 4.853 | 20 | 24 | fits | 85,505 | 51 | 0.501 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 240,311 | 2.403 | 20 | 50 | fits | 136,270 | 153 | 0.565 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 1,023,569 | 10.236 | 20 | 20 | fits | 90,956 | 92 | 0.635 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 39,654 | 0.397 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 36,023 | 0.360 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 254,837 | 2.548 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 197,402 | 1.974 | 20 | 200 | fits | 105,458 | 203 | 0.313 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 295,543 | 2.955 | 20 | 20 | fits | 92,006 | 77 | 0.540 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 574,755 | 5.748 | 20 | 24 | fits | 133,660 | 121 | 0.608 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 430,600 | 4.306 | 20 | 50 | fits | 114,366 | 184 | 0.395 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 990,068 | 9.901 | 20 | 20 | fits | 67,608 | 60 | 0.679 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 139,053 | 1.391 | 49 | 49 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 21,046 | 0.210 | 20 | 20 | fits | 34,873 | 19 (14) | 0.872 |
| Talker Advertise RX for every input, bound | `srp.bound_advertise.if0` | 125,679 | 1.257 | 20 | 20 | fits | 106,225 | 32 | 0.878 |
| LINK_UP | `adp.link_up.if0` | 3,245 | 0.032 | 20 | 200 | fits | 31,162 | 44 (12) | 0.711 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,050 | 0.150 | 20 | 200 | fits | 21,634 | 23 (39) | 0.604 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 13,936 | 0.139 | 20 | 200 | fits | 2,362 | 10 (11) | 0.400 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 572,859 | 5.729 | 20 | 20 | fits | 154,027 | 208 | 0.365 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 466,858 | 4.669 | 20 | 200 | fits | 152,133 | 114 | 0.485 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 620,269 | 6.203 | 20 | 200 | fits | 154,027 | 208 | 0.365 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 467,782 | 4.678 | 20 | 20 | fits | 152,133 | 114 | 0.485 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 756,479 | 7.565 | 20 | 20 | fits | 135,506 | 129 | 0.615 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 158,111 | 1.581 | 20 | 24 | fits | 151,683 | 110 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 470,432 | 4.704 | 20 | 24 | fits | 152,133 | 114 | 0.485 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 470,366 | 4.704 | 20 | 50 | fits | 152,133 | 114 | 0.485 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 623,997 | 6.240 | 20 | 50 | fits | 154,027 | 208 | 0.365 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 759,437 | 7.594 | 20 | 20 | fits | 135,506 | 129 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,110,673 | 11.107 | 20 | 20 | fits | 67,464 | 60 | 0.675 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 651,021 | 6.510 | 20 | 20 | fits | 153,595 | 207 | 0.363 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 546,322 | 5.463 | 20 | 200 | fits | 152,254 | 114 | 0.485 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 699,301 | 6.993 | 20 | 200 | fits | 153,595 | 207 | 0.363 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 547,246 | 5.472 | 20 | 20 | fits | 152,254 | 114 | 0.485 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 835,353 | 8.354 | 20 | 20 | fits | 135,348 | 129 | 0.613 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 237,454 | 2.375 | 20 | 24 | fits | 151,619 | 110 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 549,896 | 5.499 | 20 | 24 | fits | 152,254 | 114 | 0.485 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 549,830 | 5.498 | 20 | 50 | fits | 152,254 | 114 | 0.485 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 703,029 | 7.030 | 20 | 50 | fits | 153,595 | 207 | 0.363 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 838,311 | 8.383 | 20 | 20 | fits | 135,348 | 129 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 1,189,596 | 11.896 | 20 | 20 | fits | 67,499 | 60 | 0.676 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 638,521 | 6.385 | 20 | 20 | fits | 153,595 | 207 | 0.363 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 533,822 | 5.338 | 20 | 200 | fits | 152,254 | 114 | 0.485 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 686,801 | 6.868 | 20 | 200 | fits | 153,595 | 207 | 0.363 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 534,746 | 5.347 | 20 | 20 | fits | 152,254 | 114 | 0.485 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 822,853 | 8.229 | 20 | 20 | fits | 135,348 | 129 | 0.613 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 224,954 | 2.250 | 20 | 24 | fits | 151,619 | 110 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 537,396 | 5.374 | 20 | 24 | fits | 152,254 | 114 | 0.485 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 537,330 | 5.373 | 20 | 50 | fits | 152,254 | 114 | 0.485 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 690,529 | 6.905 | 20 | 50 | fits | 153,595 | 207 | 0.363 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 825,811 | 8.258 | 20 | 20 | fits | 135,348 | 129 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 1,177,096 | 11.771 | 20 | 20 | fits | 67,499 | 60 | 0.676 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 626,021 | 6.260 | 20 | 20 | fits | 153,595 | 207 | 0.363 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 521,322 | 5.213 | 20 | 200 | fits | 152,254 | 114 | 0.485 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 674,301 | 6.743 | 20 | 200 | fits | 153,595 | 207 | 0.363 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 522,246 | 5.222 | 20 | 20 | fits | 152,254 | 114 | 0.485 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 810,353 | 8.104 | 20 | 20 | fits | 135,348 | 129 | 0.613 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 212,454 | 2.125 | 20 | 24 | fits | 151,619 | 110 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 524,896 | 5.249 | 20 | 24 | fits | 152,254 | 114 | 0.485 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 524,830 | 5.248 | 20 | 50 | fits | 152,254 | 114 | 0.485 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 678,029 | 6.780 | 20 | 50 | fits | 153,595 | 207 | 0.363 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 813,311 | 8.133 | 20 | 20 | fits | 135,348 | 129 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 1,164,596 | 11.646 | 20 | 20 | fits | 67,499 | 60 | 0.676 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 613,521 | 6.135 | 20 | 20 | fits | 153,595 | 207 | 0.363 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 508,822 | 5.088 | 20 | 200 | fits | 152,254 | 114 | 0.485 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 661,801 | 6.618 | 20 | 200 | fits | 153,595 | 207 | 0.363 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 509,746 | 5.097 | 20 | 20 | fits | 152,254 | 114 | 0.485 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 797,853 | 7.979 | 20 | 20 | fits | 135,348 | 129 | 0.613 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 199,954 | 2.000 | 20 | 24 | fits | 151,619 | 110 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 512,396 | 5.124 | 20 | 24 | fits | 152,254 | 114 | 0.485 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 512,330 | 5.123 | 20 | 50 | fits | 152,254 | 114 | 0.485 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 665,529 | 6.655 | 20 | 50 | fits | 153,595 | 207 | 0.363 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 800,811 | 8.008 | 20 | 20 | fits | 135,348 | 129 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 1,152,096 | 11.521 | 20 | 20 | fits | 67,499 | 60 | 0.676 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 601,021 | 6.010 | 20 | 20 | fits | 153,595 | 207 | 0.363 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 496,322 | 4.963 | 20 | 200 | fits | 152,254 | 114 | 0.485 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 649,301 | 6.493 | 20 | 200 | fits | 153,595 | 207 | 0.363 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 497,246 | 4.972 | 20 | 20 | fits | 152,254 | 114 | 0.485 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 785,353 | 7.854 | 20 | 20 | fits | 135,348 | 129 | 0.613 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 187,454 | 1.875 | 20 | 24 | fits | 151,619 | 110 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 499,896 | 4.999 | 20 | 24 | fits | 152,254 | 114 | 0.485 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 499,830 | 4.998 | 20 | 50 | fits | 152,254 | 114 | 0.485 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 653,029 | 6.530 | 20 | 50 | fits | 153,595 | 207 | 0.363 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 788,311 | 7.883 | 20 | 20 | fits | 135,348 | 129 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 1,139,596 | 11.396 | 20 | 20 | fits | 67,499 | 60 | 0.676 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 564,253 | 5.643 | 20 | 20 | fits | 153,647 | 207 | 0.364 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 459,554 | 4.596 | 20 | 200 | fits | 152,254 | 114 | 0.485 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 612,585 | 6.126 | 20 | 200 | fits | 153,647 | 207 | 0.364 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 460,478 | 4.605 | 20 | 20 | fits | 152,254 | 114 | 0.485 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 748,637 | 7.486 | 20 | 20 | fits | 135,348 | 129 | 0.613 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 151,083 | 1.511 | 20 | 24 | fits | 152,629 | 110 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 463,128 | 4.631 | 20 | 24 | fits | 152,254 | 114 | 0.485 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 463,062 | 4.631 | 20 | 50 | fits | 152,254 | 114 | 0.485 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 616,313 | 6.163 | 20 | 50 | fits | 153,647 | 207 | 0.364 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 751,595 | 7.516 | 20 | 20 | fits | 135,348 | 129 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 1,102,880 | 11.029 | 20 | 20 | fits | 67,499 | 60 | 0.676 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 564,253 | 5.643 | 20 | 20 | fits | 153,647 | 207 | 0.364 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 459,554 | 4.596 | 20 | 200 | fits | 152,254 | 114 | 0.485 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 612,585 | 6.126 | 20 | 200 | fits | 153,647 | 207 | 0.364 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 460,478 | 4.605 | 20 | 20 | fits | 152,254 | 114 | 0.485 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 748,637 | 7.486 | 20 | 20 | fits | 135,348 | 129 | 0.613 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 151,083 | 1.511 | 20 | 24 | fits | 152,629 | 110 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 463,128 | 4.631 | 20 | 24 | fits | 152,254 | 114 | 0.485 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 463,062 | 4.631 | 20 | 50 | fits | 152,254 | 114 | 0.485 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 616,313 | 6.163 | 20 | 50 | fits | 153,647 | 207 | 0.364 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 751,595 | 7.516 | 20 | 20 | fits | 135,348 | 129 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 1,102,880 | 11.029 | 20 | 20 | fits | 67,499 | 60 | 0.676 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 607,320 | 6.073 | 20 | 20 | fits | 154,148 | 206 | 0.373 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 493,113 | 4.931 | 20 | 200 | fits | 152,103 | 121 | 0.479 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 646,645 | 6.466 | 20 | 200 | fits | 154,148 | 206 | 0.373 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 494,037 | 4.940 | 20 | 20 | fits | 152,103 | 121 | 0.479 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 782,886 | 7.829 | 20 | 20 | fits | 135,537 | 129 | 0.614 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 187,056 | 1.871 | 20 | 24 | fits | 152,253 | 109 | 0.408 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 496,687 | 4.967 | 20 | 24 | fits | 152,103 | 121 | 0.479 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 496,621 | 4.966 | 20 | 50 | fits | 152,103 | 121 | 0.479 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 650,373 | 6.504 | 20 | 50 | fits | 154,148 | 206 | 0.373 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 785,844 | 7.858 | 20 | 20 | fits | 135,537 | 129 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 1,113,988 | 11.140 | 20 | 20 | fits | 67,475 | 60 | 0.675 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 582,320 | 5.823 | 20 | 20 | fits | 154,148 | 206 | 0.373 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 468,113 | 4.681 | 20 | 200 | fits | 152,103 | 121 | 0.479 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 621,645 | 6.216 | 20 | 200 | fits | 154,148 | 206 | 0.373 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 469,037 | 4.690 | 20 | 20 | fits | 152,103 | 121 | 0.479 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 757,886 | 7.579 | 20 | 20 | fits | 135,537 | 129 | 0.614 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 162,056 | 1.621 | 20 | 24 | fits | 152,253 | 109 | 0.408 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 471,687 | 4.717 | 20 | 24 | fits | 152,103 | 121 | 0.479 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 471,621 | 4.716 | 20 | 50 | fits | 152,103 | 121 | 0.479 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 625,373 | 6.254 | 20 | 50 | fits | 154,148 | 206 | 0.373 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 760,844 | 7.608 | 20 | 20 | fits | 135,537 | 129 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 1,088,988 | 10.890 | 20 | 20 | fits | 67,475 | 60 | 0.675 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 578,539 | 5.785 | 20 | 20 | fits | 155,143 | 211 | 0.366 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 462,205 | 4.622 | 20 | 200 | fits | 149,942 | 117 | 0.484 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 616,732 | 6.167 | 20 | 200 | fits | 155,143 | 211 | 0.366 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 463,129 | 4.631 | 20 | 20 | fits | 149,942 | 117 | 0.484 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 753,204 | 7.532 | 20 | 20 | fits | 135,768 | 129 | 0.617 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 158,309 | 1.583 | 20 | 24 | fits | 152,214 | 109 | 0.410 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 465,779 | 4.658 | 20 | 24 | fits | 149,942 | 117 | 0.484 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 465,713 | 4.657 | 20 | 50 | fits | 149,942 | 117 | 0.484 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 620,460 | 6.205 | 20 | 50 | fits | 155,143 | 211 | 0.366 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 756,162 | 7.562 | 20 | 20 | fits | 135,768 | 129 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 1,084,377 | 10.844 | 20 | 20 | fits | 67,565 | 61 | 0.674 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 641,652 | 6.417 | 20 | 20 | fits | 154,124 | 208 | 0.366 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 535,501 | 5.355 | 20 | 200 | fits | 152,925 | 121 | 0.486 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 689,009 | 6.890 | 20 | 200 | fits | 154,124 | 208 | 0.366 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 536,425 | 5.364 | 20 | 20 | fits | 152,925 | 121 | 0.486 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 825,346 | 8.253 | 20 | 20 | fits | 135,633 | 129 | 0.615 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 228,667 | 2.287 | 20 | 24 | fits | 152,253 | 109 | 0.408 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 539,075 | 5.391 | 20 | 24 | fits | 152,925 | 121 | 0.486 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 539,009 | 5.390 | 20 | 50 | fits | 152,925 | 121 | 0.486 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 692,737 | 6.927 | 20 | 50 | fits | 154,124 | 208 | 0.366 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 828,304 | 8.283 | 20 | 20 | fits | 135,633 | 129 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 1,156,496 | 11.565 | 20 | 20 | fits | 67,579 | 61 | 0.674 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 616,652 | 6.167 | 20 | 20 | fits | 154,124 | 208 | 0.366 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 510,501 | 5.105 | 20 | 200 | fits | 152,925 | 121 | 0.486 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 664,009 | 6.640 | 20 | 200 | fits | 154,124 | 208 | 0.366 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 511,425 | 5.114 | 20 | 20 | fits | 152,925 | 121 | 0.486 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 800,346 | 8.003 | 20 | 20 | fits | 135,633 | 129 | 0.615 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 203,667 | 2.037 | 20 | 24 | fits | 152,253 | 109 | 0.408 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 514,075 | 5.141 | 20 | 24 | fits | 152,925 | 121 | 0.486 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 514,009 | 5.140 | 20 | 50 | fits | 152,925 | 121 | 0.486 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 667,737 | 6.677 | 20 | 50 | fits | 154,124 | 208 | 0.366 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 803,304 | 8.033 | 20 | 20 | fits | 135,633 | 129 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 1,131,496 | 11.315 | 20 | 20 | fits | 67,579 | 61 | 0.674 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 591,652 | 5.917 | 20 | 20 | fits | 154,124 | 208 | 0.366 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 485,501 | 4.855 | 20 | 200 | fits | 152,925 | 121 | 0.486 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 639,009 | 6.390 | 20 | 200 | fits | 154,124 | 208 | 0.366 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 486,425 | 4.864 | 20 | 20 | fits | 152,925 | 121 | 0.486 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 775,346 | 7.753 | 20 | 20 | fits | 135,633 | 129 | 0.615 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 178,667 | 1.787 | 20 | 24 | fits | 152,253 | 109 | 0.408 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 489,075 | 4.891 | 20 | 24 | fits | 152,925 | 121 | 0.486 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 489,009 | 4.890 | 20 | 50 | fits | 152,925 | 121 | 0.486 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 642,737 | 6.427 | 20 | 50 | fits | 154,124 | 208 | 0.366 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 778,304 | 7.783 | 20 | 20 | fits | 135,633 | 129 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 1,106,496 | 11.065 | 20 | 20 | fits | 67,579 | 61 | 0.674 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 566,652 | 5.667 | 20 | 20 | fits | 154,124 | 208 | 0.366 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 460,501 | 4.605 | 20 | 200 | fits | 152,925 | 121 | 0.486 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 614,009 | 6.140 | 20 | 200 | fits | 154,124 | 208 | 0.366 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 461,425 | 4.614 | 20 | 20 | fits | 152,925 | 121 | 0.486 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 750,346 | 7.503 | 20 | 20 | fits | 135,633 | 129 | 0.615 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 153,667 | 1.537 | 20 | 24 | fits | 152,253 | 109 | 0.408 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 464,075 | 4.641 | 20 | 24 | fits | 152,925 | 121 | 0.486 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 464,009 | 4.640 | 20 | 50 | fits | 152,925 | 121 | 0.486 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 617,737 | 6.177 | 20 | 50 | fits | 154,124 | 208 | 0.366 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 753,304 | 7.533 | 20 | 20 | fits | 135,633 | 129 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 1,081,496 | 10.815 | 20 | 20 | fits | 67,579 | 61 | 0.674 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 644,650 | 6.447 | 20 | 20 | fits | 152,288 | 205 | 0.365 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 559,533 | 5.595 | 20 | 200 | fits | 155,591 | 125 | 0.446 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 711,205 | 7.112 | 20 | 200 | fits | 152,288 | 205 | 0.365 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 560,457 | 5.605 | 20 | 20 | fits | 155,591 | 125 | 0.446 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 848,942 | 8.489 | 20 | 20 | fits | 137,033 | 132 | 0.632 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 245,487 | 2.455 | 20 | 24 | fits | 152,397 | 110 | 0.409 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 563,107 | 5.631 | 20 | 24 | fits | 155,591 | 125 | 0.446 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 563,041 | 5.630 | 20 | 50 | fits | 155,591 | 125 | 0.446 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 714,933 | 7.149 | 20 | 50 | fits | 152,288 | 205 | 0.365 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 851,900 | 8.519 | 20 | 20 | fits | 137,033 | 132 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 1,184,995 | 11.850 | 20 | 20 | fits | 56,952 | 47 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 574,697 | 5.747 | 20 | 20 | fits | 151,116 | 201 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 482,079 | 4.821 | 20 | 200 | fits | 153,851 | 119 | 0.445 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 632,579 | 6.326 | 20 | 200 | fits | 151,116 | 201 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 483,003 | 4.830 | 20 | 20 | fits | 153,851 | 119 | 0.445 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 768,633 | 7.686 | 20 | 20 | fits | 135,350 | 130 | 0.613 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 183,765 | 1.838 | 20 | 24 | fits | 152,235 | 109 | 0.405 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 485,653 | 4.857 | 20 | 24 | fits | 153,851 | 119 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 485,587 | 4.856 | 20 | 50 | fits | 153,851 | 119 | 0.445 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 636,307 | 6.363 | 20 | 50 | fits | 151,116 | 201 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 771,591 | 7.716 | 20 | 20 | fits | 135,350 | 130 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,114,913 | 11.149 | 20 | 20 | fits | 67,251 | 60 | 0.672 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 562,197 | 5.622 | 20 | 20 | fits | 151,116 | 201 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 469,579 | 4.696 | 20 | 200 | fits | 153,851 | 119 | 0.445 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 620,079 | 6.201 | 20 | 200 | fits | 151,116 | 201 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 470,503 | 4.705 | 20 | 20 | fits | 153,851 | 119 | 0.445 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 756,133 | 7.561 | 20 | 20 | fits | 135,350 | 130 | 0.613 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 171,265 | 1.713 | 20 | 24 | fits | 152,235 | 109 | 0.405 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 473,153 | 4.732 | 20 | 24 | fits | 153,851 | 119 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 473,087 | 4.731 | 20 | 50 | fits | 153,851 | 119 | 0.445 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 623,807 | 6.238 | 20 | 50 | fits | 151,116 | 201 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 759,091 | 7.591 | 20 | 20 | fits | 135,350 | 130 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 1,102,413 | 11.024 | 20 | 20 | fits | 67,251 | 60 | 0.672 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 549,697 | 5.497 | 20 | 20 | fits | 151,116 | 201 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 457,079 | 4.571 | 20 | 200 | fits | 153,851 | 119 | 0.445 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 607,579 | 6.076 | 20 | 200 | fits | 151,116 | 201 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 458,003 | 4.580 | 20 | 20 | fits | 153,851 | 119 | 0.445 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 743,633 | 7.436 | 20 | 20 | fits | 135,350 | 130 | 0.613 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 158,765 | 1.588 | 20 | 24 | fits | 152,235 | 109 | 0.405 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 460,653 | 4.607 | 20 | 24 | fits | 153,851 | 119 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 460,587 | 4.606 | 20 | 50 | fits | 153,851 | 119 | 0.445 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 611,307 | 6.113 | 20 | 50 | fits | 151,116 | 201 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 746,591 | 7.466 | 20 | 20 | fits | 135,350 | 130 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 1,089,913 | 10.899 | 20 | 20 | fits | 67,251 | 60 | 0.672 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 647,577 | 6.476 | 20 | 20 | fits | 151,267 | 201 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 537,337 | 5.373 | 20 | 200 | fits | 153,851 | 119 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 687,988 | 6.880 | 20 | 200 | fits | 151,267 | 201 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 538,261 | 5.383 | 20 | 20 | fits | 153,851 | 119 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 828,301 | 8.283 | 20 | 20 | fits | 128,740 | 123 | 0.644 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 239,023 | 2.390 | 20 | 24 | fits | 152,027 | 109 | 0.403 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 540,911 | 5.409 | 20 | 24 | fits | 153,851 | 119 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 540,845 | 5.408 | 20 | 50 | fits | 153,851 | 119 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 691,716 | 6.917 | 20 | 50 | fits | 151,267 | 201 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 831,259 | 8.313 | 20 | 20 | fits | 128,740 | 123 | 0.644 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 1,170,146 | 11.701 | 20 | 20 | fits | 78,102 | 73 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 635,077 | 6.351 | 20 | 20 | fits | 151,267 | 201 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 524,837 | 5.248 | 20 | 200 | fits | 153,851 | 119 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 675,488 | 6.755 | 20 | 200 | fits | 151,267 | 201 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 525,761 | 5.258 | 20 | 20 | fits | 153,851 | 119 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 815,801 | 8.158 | 20 | 20 | fits | 128,740 | 123 | 0.644 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 226,523 | 2.265 | 20 | 24 | fits | 152,027 | 109 | 0.403 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 528,411 | 5.284 | 20 | 24 | fits | 153,851 | 119 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 528,345 | 5.283 | 20 | 50 | fits | 153,851 | 119 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 679,216 | 6.792 | 20 | 50 | fits | 151,267 | 201 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 818,759 | 8.188 | 20 | 20 | fits | 128,740 | 123 | 0.644 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 1,157,646 | 11.576 | 20 | 20 | fits | 78,102 | 73 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 622,577 | 6.226 | 20 | 20 | fits | 151,267 | 201 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 512,337 | 5.123 | 20 | 200 | fits | 153,851 | 119 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 662,988 | 6.630 | 20 | 200 | fits | 151,267 | 201 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 513,261 | 5.133 | 20 | 20 | fits | 153,851 | 119 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 803,301 | 8.033 | 20 | 20 | fits | 128,740 | 123 | 0.644 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 214,023 | 2.140 | 20 | 24 | fits | 152,027 | 109 | 0.403 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 515,911 | 5.159 | 20 | 24 | fits | 153,851 | 119 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 515,845 | 5.158 | 20 | 50 | fits | 153,851 | 119 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 666,716 | 6.667 | 20 | 50 | fits | 151,267 | 201 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 806,259 | 8.063 | 20 | 20 | fits | 128,740 | 123 | 0.644 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 1,145,146 | 11.451 | 20 | 20 | fits | 78,102 | 73 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 610,077 | 6.101 | 20 | 20 | fits | 151,267 | 201 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 499,837 | 4.998 | 20 | 200 | fits | 153,851 | 119 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 650,488 | 6.505 | 20 | 200 | fits | 151,267 | 201 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 500,761 | 5.008 | 20 | 20 | fits | 153,851 | 119 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 790,801 | 7.908 | 20 | 20 | fits | 128,740 | 123 | 0.644 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 201,523 | 2.015 | 20 | 24 | fits | 152,027 | 109 | 0.403 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 503,411 | 5.034 | 20 | 24 | fits | 153,851 | 119 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 503,345 | 5.033 | 20 | 50 | fits | 153,851 | 119 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 654,216 | 6.542 | 20 | 50 | fits | 151,267 | 201 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 793,759 | 7.938 | 20 | 20 | fits | 128,740 | 123 | 0.644 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 1,132,646 | 11.326 | 20 | 20 | fits | 78,102 | 73 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 597,577 | 5.976 | 20 | 20 | fits | 151,267 | 201 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 487,337 | 4.873 | 20 | 200 | fits | 153,851 | 119 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 637,988 | 6.380 | 20 | 200 | fits | 151,267 | 201 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 488,261 | 4.883 | 20 | 20 | fits | 153,851 | 119 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 778,301 | 7.783 | 20 | 20 | fits | 128,740 | 123 | 0.644 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 189,023 | 1.890 | 20 | 24 | fits | 152,027 | 109 | 0.403 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 490,911 | 4.909 | 20 | 24 | fits | 153,851 | 119 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 490,845 | 4.908 | 20 | 50 | fits | 153,851 | 119 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 641,716 | 6.417 | 20 | 50 | fits | 151,267 | 201 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 781,259 | 7.813 | 20 | 20 | fits | 128,740 | 123 | 0.644 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 1,120,146 | 11.201 | 20 | 20 | fits | 78,102 | 73 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 564,027 | 5.640 | 20 | 20 | fits | 154,191 | 210 | 0.367 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 458,006 | 4.580 | 20 | 200 | fits | 151,951 | 115 | 0.451 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 611,581 | 6.116 | 20 | 200 | fits | 154,191 | 210 | 0.367 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 458,930 | 4.589 | 20 | 20 | fits | 151,951 | 115 | 0.451 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 753,728 | 7.537 | 20 | 20 | fits | 130,541 | 126 | 0.664 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 161,631 | 1.616 | 20 | 24 | fits | 150,711 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 461,580 | 4.616 | 20 | 24 | fits | 151,951 | 115 | 0.451 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 461,514 | 4.615 | 20 | 50 | fits | 151,951 | 115 | 0.451 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 615,309 | 6.153 | 20 | 50 | fits | 154,191 | 210 | 0.367 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 756,686 | 7.567 | 20 | 20 | fits | 130,541 | 126 | 0.664 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 1,090,212 | 10.902 | 20 | 20 | fits | 72,666 | 66 | 0.697 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 557,684 | 5.577 | 20 | 20 | fits | 149,259 | 194 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 447,029 | 4.470 | 20 | 200 | fits | 153,585 | 132 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 606,780 | 6.068 | 20 | 200 | fits | 149,259 | 194 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 447,953 | 4.480 | 20 | 20 | fits | 153,585 | 132 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 743,264 | 7.433 | 20 | 20 | fits | 135,780 | 129 | 0.615 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 148,155 | 1.482 | 20 | 24 | fits | 150,711 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 450,603 | 4.506 | 20 | 24 | fits | 153,585 | 132 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 450,537 | 4.505 | 20 | 50 | fits | 153,585 | 132 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 610,508 | 6.105 | 20 | 50 | fits | 149,259 | 194 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 746,222 | 7.462 | 20 | 20 | fits | 135,780 | 129 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 1,157,789 | 11.578 | 20 | 20 | fits | 68,097 | 61 | 0.686 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 564,321 | 5.643 | 20 | 20 | fits | 154,356 | 209 | 0.370 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 457,901 | 4.579 | 20 | 200 | fits | 153,703 | 122 | 0.458 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 611,641 | 6.116 | 20 | 200 | fits | 154,356 | 209 | 0.370 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 458,825 | 4.588 | 20 | 20 | fits | 153,703 | 122 | 0.458 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 749,629 | 7.496 | 20 | 20 | fits | 137,284 | 132 | 0.635 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 150,611 | 1.506 | 20 | 24 | fits | 150,711 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 461,475 | 4.615 | 20 | 24 | fits | 153,703 | 122 | 0.458 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 461,409 | 4.614 | 20 | 50 | fits | 153,703 | 122 | 0.458 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 615,369 | 6.154 | 20 | 50 | fits | 154,356 | 209 | 0.370 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 752,587 | 7.526 | 20 | 20 | fits | 137,284 | 132 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,155,913 | 11.559 | 20 | 20 | fits | 70,381 | 67 | 0.673 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 547,528 | 5.475 | 20 | 20 | fits | 152,411 | 205 | 0.367 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 462,146 | 4.621 | 20 | 200 | fits | 155,546 | 126 | 0.452 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 613,941 | 6.139 | 20 | 200 | fits | 152,411 | 205 | 0.367 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 463,070 | 4.631 | 20 | 20 | fits | 155,546 | 126 | 0.452 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 748,005 | 7.480 | 20 | 20 | fits | 133,360 | 127 | 0.648 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 153,067 | 1.531 | 20 | 24 | fits | 150,711 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 465,720 | 4.657 | 20 | 24 | fits | 155,546 | 126 | 0.452 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 465,654 | 4.657 | 20 | 50 | fits | 155,546 | 126 | 0.452 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 617,669 | 6.177 | 20 | 50 | fits | 152,411 | 205 | 0.367 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 750,963 | 7.510 | 20 | 20 | fits | 133,360 | 127 | 0.648 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,172,344 | 11.723 | 20 | 20 | fits | 71,508 | 67 | 0.702 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 569,002 | 5.690 | 20 | 20 | fits | 152,373 | 192 | 0.393 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 464,922 | 4.649 | 20 | 200 | fits | 153,826 | 131 | 0.458 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 616,679 | 6.167 | 20 | 200 | fits | 152,373 | 192 | 0.393 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 465,846 | 4.658 | 20 | 20 | fits | 153,826 | 131 | 0.458 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 830,198 | 8.302 | 20 | 20 | fits | 135,934 | 130 | 0.620 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 155,570 | 1.556 | 20 | 24 | fits | 150,758 | 107 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 468,496 | 4.685 | 20 | 24 | fits | 153,826 | 131 | 0.458 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 468,430 | 4.684 | 20 | 50 | fits | 153,826 | 131 | 0.458 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 620,407 | 6.204 | 20 | 50 | fits | 152,373 | 192 | 0.393 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 833,156 | 8.332 | 20 | 20 | fits | 135,934 | 130 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,177,182 | 11.772 | 20 | 20 | fits | 67,688 | 60 | 0.679 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 549,368 | 5.494 | 20 | 20 | fits | 151,187 | 201 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 456,679 | 4.567 | 20 | 200 | fits | 153,851 | 119 | 0.445 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 607,250 | 6.072 | 20 | 200 | fits | 151,187 | 201 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 457,603 | 4.576 | 20 | 20 | fits | 153,851 | 119 | 0.445 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 820,547 | 8.205 | 20 | 20 | fits | 135,712 | 131 | 0.618 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 158,390 | 1.584 | 20 | 24 | fits | 150,740 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 460,253 | 4.603 | 20 | 24 | fits | 153,851 | 119 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 460,187 | 4.602 | 20 | 50 | fits | 153,851 | 119 | 0.445 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 610,978 | 6.110 | 20 | 50 | fits | 151,187 | 201 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 823,505 | 8.235 | 20 | 20 | fits | 135,712 | 131 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,167,271 | 11.673 | 20 | 20 | fits | 67,430 | 60 | 0.674 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 639,055 | 6.391 | 20 | 20 | fits | 154,495 | 210 | 0.374 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 456,179 | 4.562 | 20 | 200 | fits | 150,895 | 114 | 0.480 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 686,963 | 6.870 | 20 | 200 | fits | 154,495 | 210 | 0.374 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 457,103 | 4.571 | 20 | 20 | fits | 150,895 | 114 | 0.480 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 827,835 | 8.278 | 20 | 20 | fits | 129,152 | 123 | 0.647 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 160,846 | 1.608 | 20 | 24 | fits | 150,740 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 459,753 | 4.598 | 20 | 24 | fits | 150,895 | 114 | 0.480 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 459,687 | 4.597 | 20 | 50 | fits | 150,895 | 114 | 0.480 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 690,691 | 6.907 | 20 | 50 | fits | 154,495 | 210 | 0.374 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 830,793 | 8.308 | 20 | 20 | fits | 129,152 | 123 | 0.647 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,170,482 | 11.705 | 20 | 20 | fits | 78,295 | 73 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 658,912 | 6.589 | 20 | 20 | fits | 156,803 | 211 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 541,832 | 5.418 | 20 | 200 | fits | 153,934 | 120 | 0.451 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 708,959 | 7.090 | 20 | 200 | fits | 156,803 | 211 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 542,756 | 5.428 | 20 | 20 | fits | 153,934 | 120 | 0.451 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 847,218 | 8.472 | 20 | 20 | fits | 137,555 | 132 | 0.636 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 163,302 | 1.633 | 20 | 24 | fits | 150,740 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 545,406 | 5.454 | 20 | 24 | fits | 153,934 | 120 | 0.451 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 545,340 | 5.453 | 20 | 50 | fits | 153,934 | 120 | 0.451 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 712,687 | 7.127 | 20 | 50 | fits | 156,803 | 211 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 850,176 | 8.502 | 20 | 20 | fits | 137,555 | 132 | 0.636 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,173,218 | 11.732 | 20 | 20 | fits | 62,382 | 53 | 0.734 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 538,243 | 5.382 | 20 | 20 | fits | 152,064 | 205 | 0.363 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 453,260 | 4.533 | 20 | 200 | fits | 153,851 | 119 | 0.445 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 604,708 | 6.047 | 20 | 200 | fits | 152,064 | 205 | 0.363 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 454,184 | 4.542 | 20 | 20 | fits | 153,851 | 119 | 0.445 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 742,528 | 7.425 | 20 | 20 | fits | 137,116 | 133 | 0.631 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 154,971 | 1.550 | 20 | 24 | fits | 150,740 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 456,834 | 4.568 | 20 | 24 | fits | 153,851 | 119 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 456,768 | 4.568 | 20 | 50 | fits | 153,851 | 119 | 0.445 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 608,436 | 6.084 | 20 | 50 | fits | 152,064 | 205 | 0.363 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 745,486 | 7.455 | 20 | 20 | fits | 137,116 | 133 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 1,083,035 | 10.830 | 20 | 20 | fits | 61,459 | 53 | 0.723 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 551,655 | 5.517 | 20 | 20 | fits | 153,703 | 196 | 0.349 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 455,342 | 4.553 | 20 | 200 | fits | 153,477 | 131 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 608,429 | 6.084 | 20 | 200 | fits | 153,703 | 196 | 0.349 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 456,266 | 4.563 | 20 | 20 | fits | 153,477 | 131 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 738,667 | 7.387 | 20 | 20 | fits | 129,534 | 126 | 0.648 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 157,427 | 1.574 | 20 | 24 | fits | 150,740 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 458,916 | 4.589 | 20 | 24 | fits | 153,477 | 131 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 458,850 | 4.588 | 20 | 50 | fits | 153,477 | 131 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 612,157 | 6.122 | 20 | 50 | fits | 153,703 | 196 | 0.349 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 741,625 | 7.416 | 20 | 20 | fits | 129,534 | 126 | 0.648 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 1,087,852 | 10.879 | 20 | 20 | fits | 67,333 | 60 | 0.674 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 560,834 | 5.608 | 20 | 20 | fits | 152,329 | 205 | 0.371 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 458,228 | 4.582 | 20 | 200 | fits | 153,907 | 119 | 0.445 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 609,941 | 6.099 | 20 | 200 | fits | 152,329 | 205 | 0.371 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 459,152 | 4.592 | 20 | 20 | fits | 153,907 | 119 | 0.445 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 751,762 | 7.518 | 20 | 20 | fits | 130,324 | 126 | 0.662 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 159,883 | 1.599 | 20 | 24 | fits | 150,740 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 461,802 | 4.618 | 20 | 24 | fits | 153,907 | 119 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 461,736 | 4.617 | 20 | 50 | fits | 153,907 | 119 | 0.445 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 613,669 | 6.137 | 20 | 50 | fits | 152,329 | 205 | 0.371 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 754,720 | 7.547 | 20 | 20 | fits | 130,324 | 126 | 0.662 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 1,088,037 | 10.880 | 20 | 20 | fits | 67,310 | 60 | 0.673 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 570,917 | 5.709 | 20 | 20 | fits | 149,303 | 194 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 460,409 | 4.604 | 20 | 200 | fits | 153,632 | 132 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 620,103 | 6.201 | 20 | 200 | fits | 149,303 | 194 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 461,333 | 4.613 | 20 | 20 | fits | 153,632 | 132 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 753,102 | 7.531 | 20 | 20 | fits | 132,295 | 124 | 0.628 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 162,339 | 1.623 | 20 | 24 | fits | 150,740 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 463,983 | 4.640 | 20 | 24 | fits | 153,632 | 132 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 463,917 | 4.639 | 20 | 50 | fits | 153,632 | 132 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 623,831 | 6.238 | 20 | 50 | fits | 149,303 | 194 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 756,060 | 7.561 | 20 | 20 | fits | 132,295 | 124 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 1,094,505 | 10.945 | 20 | 20 | fits | 77,937 | 73 | 0.646 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 569,061 | 5.691 | 20 | 20 | fits | 151,230 | 200 | 0.416 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 458,713 | 4.587 | 20 | 200 | fits | 155,402 | 125 | 0.451 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 609,327 | 6.093 | 20 | 200 | fits | 151,230 | 200 | 0.416 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 459,637 | 4.596 | 20 | 20 | fits | 155,402 | 125 | 0.451 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 745,390 | 7.454 | 20 | 20 | fits | 135,359 | 129 | 0.612 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 148,863 | 1.489 | 20 | 24 | fits | 150,740 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 462,287 | 4.623 | 20 | 24 | fits | 155,402 | 125 | 0.451 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 462,221 | 4.622 | 20 | 50 | fits | 155,402 | 125 | 0.451 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 613,055 | 6.131 | 20 | 50 | fits | 151,230 | 200 | 0.416 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 748,348 | 7.483 | 20 | 20 | fits | 135,359 | 129 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 1,076,129 | 10.761 | 20 | 20 | fits | 67,400 | 61 | 0.672 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 562,852 | 5.629 | 20 | 20 | fits | 153,582 | 207 | 0.363 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 458,153 | 4.582 | 20 | 200 | fits | 151,211 | 114 | 0.481 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 611,119 | 6.111 | 20 | 200 | fits | 153,582 | 207 | 0.363 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 459,077 | 4.591 | 20 | 20 | fits | 151,211 | 114 | 0.481 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 747,187 | 7.472 | 20 | 20 | fits | 135,364 | 129 | 0.613 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 151,402 | 1.514 | 20 | 24 | fits | 150,823 | 107 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 461,727 | 4.617 | 20 | 24 | fits | 151,211 | 114 | 0.481 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 461,661 | 4.617 | 20 | 50 | fits | 151,211 | 114 | 0.481 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 614,847 | 6.148 | 20 | 50 | fits | 153,582 | 207 | 0.363 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 750,145 | 7.501 | 20 | 20 | fits | 135,364 | 129 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 1,093,754 | 10.938 | 20 | 20 | fits | 71,530 | 67 | 0.702 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 574,975 | 5.750 | 20 | 20 | fits | 154,954 | 211 | 0.363 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 458,974 | 4.590 | 20 | 200 | fits | 148,520 | 110 | 0.480 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 613,312 | 6.133 | 20 | 200 | fits | 154,954 | 211 | 0.363 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 459,898 | 4.599 | 20 | 20 | fits | 148,520 | 110 | 0.480 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 749,673 | 7.497 | 20 | 20 | fits | 135,657 | 129 | 0.616 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 165,849 | 1.658 | 20 | 24 | fits | 152,001 | 107 | 0.404 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 462,548 | 4.625 | 20 | 24 | fits | 148,520 | 110 | 0.480 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 462,482 | 4.625 | 20 | 50 | fits | 148,520 | 110 | 0.480 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 617,040 | 6.170 | 20 | 50 | fits | 154,954 | 211 | 0.363 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 752,631 | 7.526 | 20 | 20 | fits | 135,657 | 129 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 1,096,271 | 10.963 | 20 | 20 | fits | 67,485 | 60 | 0.676 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 554,379 | 5.544 | 20 | 20 | fits | 154,059 | 195 | 0.351 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 458,010 | 4.580 | 20 | 200 | fits | 153,482 | 131 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 611,453 | 6.115 | 20 | 200 | fits | 154,059 | 195 | 0.351 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 458,934 | 4.589 | 20 | 20 | fits | 153,482 | 131 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 749,158 | 7.492 | 20 | 20 | fits | 137,001 | 133 | 0.631 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 156,584 | 1.566 | 20 | 24 | fits | 150,711 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 461,584 | 4.616 | 20 | 24 | fits | 153,482 | 131 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 461,518 | 4.615 | 20 | 50 | fits | 153,482 | 131 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 615,181 | 6.152 | 20 | 50 | fits | 154,059 | 195 | 0.351 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 752,116 | 7.521 | 20 | 20 | fits | 137,001 | 133 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 1,084,805 | 10.848 | 20 | 20 | fits | 56,605 | 47 | 0.707 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 553,791 | 5.538 | 20 | 20 | fits | 153,644 | 196 | 0.348 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 457,478 | 4.575 | 20 | 200 | fits | 153,441 | 131 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 610,506 | 6.105 | 20 | 200 | fits | 153,644 | 196 | 0.348 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 458,402 | 4.584 | 20 | 20 | fits | 153,441 | 131 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 748,369 | 7.484 | 20 | 20 | fits | 137,159 | 133 | 0.632 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 159,655 | 1.597 | 20 | 24 | fits | 150,646 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 461,052 | 4.611 | 20 | 24 | fits | 153,441 | 131 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 460,986 | 4.610 | 20 | 50 | fits | 153,441 | 131 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 614,234 | 6.142 | 20 | 50 | fits | 153,644 | 196 | 0.348 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 751,327 | 7.513 | 20 | 20 | fits | 137,159 | 133 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 1,089,009 | 10.890 | 20 | 20 | fits | 61,454 | 53 | 0.723 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 562,950 | 5.630 | 20 | 20 | fits | 152,327 | 204 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 460,344 | 4.603 | 20 | 200 | fits | 153,851 | 119 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 612,055 | 6.121 | 20 | 200 | fits | 152,327 | 204 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 461,268 | 4.613 | 20 | 20 | fits | 153,851 | 119 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 742,296 | 7.423 | 20 | 20 | fits | 129,537 | 126 | 0.647 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 162,111 | 1.621 | 20 | 24 | fits | 150,646 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 463,918 | 4.639 | 20 | 24 | fits | 153,851 | 119 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 463,852 | 4.639 | 20 | 50 | fits | 153,851 | 119 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 615,783 | 6.158 | 20 | 50 | fits | 152,327 | 204 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 745,254 | 7.453 | 20 | 20 | fits | 129,537 | 126 | 0.647 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 1,173,537 | 11.735 | 20 | 20 | fits | 68,539 | 61 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 543,636 | 5.436 | 20 | 20 | fits | 153,736 | 197 | 0.348 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 447,323 | 4.473 | 20 | 200 | fits | 153,441 | 131 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 600,443 | 6.004 | 20 | 200 | fits | 153,736 | 197 | 0.348 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 448,247 | 4.482 | 20 | 20 | fits | 153,441 | 131 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 742,539 | 7.425 | 20 | 20 | fits | 130,490 | 126 | 0.663 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 148,635 | 1.486 | 20 | 24 | fits | 150,646 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 450,897 | 4.509 | 20 | 24 | fits | 153,441 | 131 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 450,831 | 4.508 | 20 | 50 | fits | 153,441 | 131 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 604,171 | 6.042 | 20 | 50 | fits | 153,736 | 197 | 0.348 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 745,497 | 7.455 | 20 | 20 | fits | 130,490 | 126 | 0.663 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,161,313 | 11.613 | 20 | 20 | fits | 67,684 | 60 | 0.677 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 566,453 | 5.665 | 20 | 20 | fits | 156,803 | 211 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 449,418 | 4.494 | 20 | 200 | fits | 153,945 | 120 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 616,500 | 6.165 | 20 | 200 | fits | 156,803 | 211 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 450,342 | 4.503 | 20 | 20 | fits | 153,945 | 120 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 751,192 | 7.512 | 20 | 20 | fits | 133,988 | 127 | 0.650 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 151,091 | 1.511 | 20 | 24 | fits | 150,646 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 452,992 | 4.530 | 20 | 24 | fits | 153,945 | 120 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 452,926 | 4.529 | 20 | 50 | fits | 153,945 | 120 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 620,228 | 6.202 | 20 | 50 | fits | 156,803 | 211 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 754,150 | 7.542 | 20 | 20 | fits | 133,988 | 127 | 0.650 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,164,592 | 11.646 | 20 | 20 | fits | 67,475 | 60 | 0.675 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 566,773 | 5.668 | 20 | 20 | fits | 152,916 | 191 | 0.397 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 462,601 | 4.626 | 20 | 200 | fits | 155,527 | 138 | 0.461 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 614,901 | 6.149 | 20 | 200 | fits | 152,916 | 191 | 0.397 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 463,525 | 4.635 | 20 | 20 | fits | 155,527 | 138 | 0.461 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 832,963 | 8.330 | 20 | 20 | fits | 136,586 | 130 | 0.622 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 153,547 | 1.535 | 20 | 24 | fits | 150,646 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 466,175 | 4.662 | 20 | 24 | fits | 155,527 | 138 | 0.461 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 466,109 | 4.661 | 20 | 50 | fits | 155,527 | 138 | 0.461 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 618,629 | 6.186 | 20 | 50 | fits | 152,916 | 191 | 0.397 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 835,921 | 8.359 | 20 | 20 | fits | 136,586 | 130 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,180,190 | 11.802 | 20 | 20 | fits | 71,601 | 67 | 0.703 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 658,589 | 6.586 | 20 | 20 | fits | 147,924 | 205 | 0.399 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 460,293 | 4.603 | 20 | 200 | fits | 148,763 | 110 | 0.483 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 688,607 | 6.886 | 20 | 200 | fits | 147,924 | 205 | 0.399 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 461,217 | 4.612 | 20 | 20 | fits | 148,763 | 110 | 0.483 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 823,383 | 8.234 | 20 | 20 | fits | 134,072 | 125 | 0.596 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 156,086 | 1.561 | 20 | 24 | fits | 150,729 | 107 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 463,867 | 4.639 | 20 | 24 | fits | 148,763 | 110 | 0.483 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 463,801 | 4.638 | 20 | 50 | fits | 148,763 | 110 | 0.483 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 692,335 | 6.923 | 20 | 50 | fits | 147,924 | 205 | 0.399 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 826,341 | 8.263 | 20 | 20 | fits | 134,072 | 125 | 0.596 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,180,605 | 11.806 | 20 | 20 | fits | 78,120 | 73 | 0.649 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 652,601 | 6.526 | 20 | 20 | fits | 155,178 | 208 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 465,726 | 4.657 | 20 | 200 | fits | 150,459 | 114 | 0.473 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 701,294 | 7.013 | 20 | 200 | fits | 155,178 | 208 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 466,650 | 4.667 | 20 | 20 | fits | 150,459 | 114 | 0.473 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 837,745 | 8.377 | 20 | 20 | fits | 135,747 | 130 | 0.616 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 170,614 | 1.706 | 20 | 24 | fits | 151,988 | 107 | 0.405 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 469,300 | 4.693 | 20 | 24 | fits | 150,459 | 114 | 0.473 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 469,234 | 4.692 | 20 | 50 | fits | 150,459 | 114 | 0.473 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 705,022 | 7.050 | 20 | 50 | fits | 155,178 | 208 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 840,703 | 8.407 | 20 | 20 | fits | 135,747 | 130 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,183,957 | 11.840 | 20 | 20 | fits | 67,251 | 60 | 0.672 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 647,679 | 6.477 | 20 | 20 | fits | 154,223 | 210 | 0.367 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 541,626 | 5.416 | 20 | 200 | fits | 152,314 | 115 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 695,233 | 6.952 | 20 | 200 | fits | 154,223 | 210 | 0.367 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 542,550 | 5.426 | 20 | 20 | fits | 152,314 | 115 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 837,434 | 8.374 | 20 | 20 | fits | 130,541 | 126 | 0.664 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 161,326 | 1.613 | 20 | 24 | fits | 150,675 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 545,200 | 5.452 | 20 | 24 | fits | 152,314 | 115 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 545,134 | 5.451 | 20 | 50 | fits | 152,314 | 115 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 698,961 | 6.990 | 20 | 50 | fits | 154,223 | 210 | 0.367 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 840,392 | 8.404 | 20 | 20 | fits | 130,541 | 126 | 0.664 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,173,631 | 11.736 | 20 | 20 | fits | 72,564 | 66 | 0.697 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 567,867 | 5.679 | 20 | 20 | fits | 153,957 | 209 | 0.365 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 461,846 | 4.618 | 20 | 200 | fits | 152,370 | 115 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 615,187 | 6.152 | 20 | 200 | fits | 153,957 | 209 | 0.365 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 462,770 | 4.628 | 20 | 20 | fits | 152,370 | 115 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 753,092 | 7.531 | 20 | 20 | fits | 137,201 | 132 | 0.634 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 153,954 | 1.540 | 20 | 24 | fits | 150,738 | 107 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 465,420 | 4.654 | 20 | 24 | fits | 152,370 | 115 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 465,354 | 4.654 | 20 | 50 | fits | 152,370 | 115 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 618,915 | 6.189 | 20 | 50 | fits | 153,957 | 209 | 0.365 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 756,050 | 7.561 | 20 | 20 | fits | 137,201 | 132 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 1,093,003 | 10.930 | 20 | 20 | fits | 64,904 | 60 | 0.733 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 551,061 | 5.511 | 20 | 20 | fits | 152,012 | 205 | 0.362 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 466,078 | 4.661 | 20 | 200 | fits | 154,200 | 119 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 617,474 | 6.175 | 20 | 200 | fits | 152,012 | 205 | 0.362 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 467,002 | 4.670 | 20 | 20 | fits | 154,200 | 119 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 755,211 | 7.552 | 20 | 20 | fits | 137,033 | 132 | 0.632 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 156,356 | 1.564 | 20 | 24 | fits | 150,684 | 107 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 469,652 | 4.697 | 20 | 24 | fits | 154,200 | 119 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 469,586 | 4.696 | 20 | 50 | fits | 154,200 | 119 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 621,202 | 6.212 | 20 | 50 | fits | 152,012 | 205 | 0.362 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 758,169 | 7.582 | 20 | 20 | fits | 137,033 | 132 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 1,096,361 | 10.964 | 20 | 20 | fits | 60,485 | 54 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 560,798 | 5.608 | 20 | 20 | fits | 154,009 | 209 | 0.366 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 454,777 | 4.548 | 20 | 200 | fits | 152,007 | 115 | 0.452 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 608,170 | 6.082 | 20 | 200 | fits | 154,009 | 209 | 0.366 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 455,701 | 4.557 | 20 | 20 | fits | 152,007 | 115 | 0.452 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 746,240 | 7.462 | 20 | 20 | fits | 137,366 | 133 | 0.635 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 158,374 | 1.584 | 20 | 24 | fits | 150,675 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 458,351 | 4.584 | 20 | 24 | fits | 152,007 | 115 | 0.452 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 458,285 | 4.583 | 20 | 50 | fits | 152,007 | 115 | 0.452 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 611,898 | 6.119 | 20 | 50 | fits | 154,009 | 209 | 0.366 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 749,198 | 7.492 | 20 | 20 | fits | 137,366 | 133 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 1,085,616 | 10.856 | 20 | 20 | fits | 67,232 | 60 | 0.672 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 544,060 | 5.441 | 20 | 20 | fits | 152,156 | 206 | 0.363 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 459,077 | 4.591 | 20 | 200 | fits | 153,851 | 119 | 0.445 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 610,617 | 6.106 | 20 | 200 | fits | 152,156 | 206 | 0.363 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 460,001 | 4.600 | 20 | 20 | fits | 153,851 | 119 | 0.445 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 758,434 | 7.584 | 20 | 20 | fits | 136,320 | 134 | 0.655 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 160,830 | 1.608 | 20 | 24 | fits | 150,675 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 462,651 | 4.627 | 20 | 24 | fits | 153,851 | 119 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 462,585 | 4.626 | 20 | 50 | fits | 153,851 | 119 | 0.445 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 614,345 | 6.143 | 20 | 50 | fits | 152,156 | 206 | 0.363 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 761,392 | 7.614 | 20 | 20 | fits | 136,320 | 134 | 0.655 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 1,089,726 | 10.897 | 20 | 20 | fits | 67,494 | 60 | 0.675 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 579,425 | 5.794 | 20 | 20 | fits | 156,170 | 199 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 461,282 | 4.613 | 20 | 200 | fits | 153,600 | 132 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 627,843 | 6.278 | 20 | 200 | fits | 156,170 | 199 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 462,206 | 4.622 | 20 | 20 | fits | 153,600 | 132 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 764,663 | 7.647 | 20 | 20 | fits | 136,116 | 129 | 0.618 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 163,286 | 1.633 | 20 | 24 | fits | 150,675 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 464,856 | 4.649 | 20 | 24 | fits | 153,600 | 132 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 464,790 | 4.648 | 20 | 50 | fits | 153,600 | 132 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 631,571 | 6.316 | 20 | 50 | fits | 156,170 | 199 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 767,621 | 7.676 | 20 | 20 | fits | 136,116 | 129 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 1,095,800 | 10.958 | 20 | 20 | fits | 67,489 | 60 | 0.675 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 554,394 | 5.544 | 20 | 20 | fits | 154,606 | 208 | 0.436 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 448,170 | 4.482 | 20 | 200 | fits | 153,927 | 120 | 0.445 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 612,870 | 6.129 | 20 | 200 | fits | 154,606 | 208 | 0.436 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 449,094 | 4.491 | 20 | 20 | fits | 153,927 | 120 | 0.445 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 749,417 | 7.494 | 20 | 20 | fits | 135,843 | 129 | 0.618 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 148,982 | 1.490 | 20 | 24 | fits | 150,675 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 451,744 | 4.517 | 20 | 24 | fits | 153,927 | 120 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 451,678 | 4.517 | 20 | 50 | fits | 153,927 | 120 | 0.445 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 616,598 | 6.166 | 20 | 50 | fits | 154,606 | 208 | 0.436 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 752,375 | 7.524 | 20 | 20 | fits | 135,843 | 129 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 1,080,563 | 10.806 | 20 | 20 | fits | 67,494 | 60 | 0.675 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 564,671 | 5.647 | 20 | 20 | fits | 154,046 | 208 | 0.366 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 458,546 | 4.585 | 20 | 200 | fits | 152,679 | 121 | 0.483 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 611,976 | 6.120 | 20 | 200 | fits | 154,046 | 208 | 0.366 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 459,470 | 4.595 | 20 | 20 | fits | 152,679 | 121 | 0.483 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 748,313 | 7.483 | 20 | 20 | fits | 135,633 | 129 | 0.615 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 152,266 | 1.523 | 20 | 24 | fits | 150,675 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 462,120 | 4.621 | 20 | 24 | fits | 152,679 | 121 | 0.483 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 462,054 | 4.621 | 20 | 50 | fits | 152,679 | 121 | 0.483 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 615,704 | 6.157 | 20 | 50 | fits | 154,046 | 208 | 0.366 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 751,271 | 7.513 | 20 | 20 | fits | 135,633 | 129 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 1,079,373 | 10.794 | 20 | 20 | fits | 67,489 | 60 | 0.675 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 571,114 | 5.711 | 20 | 20 | fits | 152,409 | 204 | 0.373 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 468,374 | 4.684 | 20 | 200 | fits | 155,516 | 125 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 620,167 | 6.202 | 20 | 200 | fits | 152,409 | 204 | 0.373 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 469,298 | 4.693 | 20 | 20 | fits | 155,516 | 125 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 757,703 | 7.577 | 20 | 20 | fits | 136,832 | 132 | 0.631 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 154,787 | 1.548 | 20 | 24 | fits | 150,740 | 107 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 471,948 | 4.719 | 20 | 24 | fits | 155,516 | 125 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 471,882 | 4.719 | 20 | 50 | fits | 155,516 | 125 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 623,895 | 6.239 | 20 | 50 | fits | 152,409 | 204 | 0.373 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 760,661 | 7.607 | 20 | 20 | fits | 136,832 | 132 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 1,093,627 | 10.936 | 20 | 20 | fits | 56,817 | 47 | 0.710 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 567,526 | 5.675 | 20 | 20 | fits | 153,592 | 196 | 0.347 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 471,213 | 4.712 | 20 | 200 | fits | 153,790 | 131 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 624,189 | 6.242 | 20 | 200 | fits | 153,592 | 196 | 0.347 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 472,137 | 4.721 | 20 | 20 | fits | 153,790 | 131 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 761,962 | 7.620 | 20 | 20 | fits | 137,069 | 132 | 0.633 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 162,057 | 1.621 | 20 | 24 | fits | 150,738 | 107 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 474,787 | 4.748 | 20 | 24 | fits | 153,790 | 131 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 474,721 | 4.747 | 20 | 50 | fits | 153,790 | 131 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 627,917 | 6.279 | 20 | 50 | fits | 153,592 | 196 | 0.347 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 764,920 | 7.649 | 20 | 20 | fits | 137,069 | 132 | 0.633 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 1,101,973 | 11.020 | 20 | 20 | fits | 64,918 | 60 | 0.733 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 544,276 | 5.443 | 20 | 20 | fits | 152,146 | 205 | 0.363 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 459,159 | 4.592 | 20 | 200 | fits | 155,535 | 125 | 0.445 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 610,689 | 6.107 | 20 | 200 | fits | 152,146 | 205 | 0.363 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 460,083 | 4.601 | 20 | 20 | fits | 155,535 | 125 | 0.445 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 748,426 | 7.484 | 20 | 20 | fits | 137,033 | 132 | 0.632 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 148,536 | 1.485 | 20 | 24 | fits | 150,693 | 107 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 462,733 | 4.627 | 20 | 24 | fits | 155,535 | 125 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 462,667 | 4.627 | 20 | 50 | fits | 155,535 | 125 | 0.445 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 614,417 | 6.144 | 20 | 50 | fits | 152,146 | 205 | 0.363 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 751,384 | 7.514 | 20 | 20 | fits | 137,033 | 132 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 1,167,304 | 11.673 | 20 | 20 | fits | 61,021 | 54 | 0.736 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 553,791 | 5.538 | 20 | 20 | fits | 154,009 | 209 | 0.366 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 447,770 | 4.478 | 20 | 200 | fits | 151,951 | 115 | 0.451 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 601,163 | 6.012 | 20 | 200 | fits | 154,009 | 209 | 0.366 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 448,694 | 4.487 | 20 | 20 | fits | 151,951 | 115 | 0.451 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 739,233 | 7.392 | 20 | 20 | fits | 137,366 | 133 | 0.635 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 151,356 | 1.514 | 20 | 24 | fits | 150,675 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 451,344 | 4.513 | 20 | 24 | fits | 151,951 | 115 | 0.451 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 451,278 | 4.513 | 20 | 50 | fits | 151,951 | 115 | 0.451 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 604,891 | 6.049 | 20 | 50 | fits | 154,009 | 209 | 0.366 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 742,191 | 7.422 | 20 | 20 | fits | 137,366 | 133 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,157,057 | 11.571 | 20 | 20 | fits | 67,233 | 60 | 0.673 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 537,053 | 5.371 | 20 | 20 | fits | 152,156 | 206 | 0.363 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 452,070 | 4.521 | 20 | 200 | fits | 153,795 | 119 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 603,610 | 6.036 | 20 | 200 | fits | 152,156 | 206 | 0.363 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 452,994 | 4.530 | 20 | 20 | fits | 153,795 | 119 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 751,427 | 7.514 | 20 | 20 | fits | 136,320 | 134 | 0.655 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 153,812 | 1.538 | 20 | 24 | fits | 150,675 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 455,644 | 4.556 | 20 | 24 | fits | 153,795 | 119 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 455,578 | 4.556 | 20 | 50 | fits | 153,795 | 119 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 607,338 | 6.073 | 20 | 50 | fits | 152,156 | 206 | 0.363 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 754,385 | 7.544 | 20 | 20 | fits | 136,320 | 134 | 0.655 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,161,102 | 11.611 | 20 | 20 | fits | 67,494 | 60 | 0.675 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 572,418 | 5.724 | 20 | 20 | fits | 156,170 | 199 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 454,275 | 4.543 | 20 | 200 | fits | 153,544 | 132 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 620,836 | 6.208 | 20 | 200 | fits | 156,170 | 199 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 455,199 | 4.552 | 20 | 20 | fits | 153,544 | 132 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 835,912 | 8.359 | 20 | 20 | fits | 136,650 | 130 | 0.624 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 156,268 | 1.563 | 20 | 24 | fits | 150,675 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 457,849 | 4.578 | 20 | 24 | fits | 153,544 | 132 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 457,783 | 4.578 | 20 | 50 | fits | 153,544 | 132 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 624,564 | 6.246 | 20 | 50 | fits | 156,170 | 199 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 838,870 | 8.389 | 20 | 20 | fits | 136,650 | 130 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,167,349 | 11.673 | 20 | 20 | fits | 67,489 | 60 | 0.675 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 580,961 | 5.810 | 20 | 20 | fits | 154,665 | 207 | 0.442 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 457,114 | 4.571 | 20 | 200 | fits | 153,927 | 120 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 621,873 | 6.219 | 20 | 200 | fits | 154,665 | 207 | 0.442 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 458,038 | 4.580 | 20 | 20 | fits | 153,927 | 120 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 836,738 | 8.367 | 20 | 20 | fits | 136,439 | 130 | 0.621 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 158,724 | 1.587 | 20 | 24 | fits | 150,675 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 460,688 | 4.607 | 20 | 24 | fits | 153,927 | 120 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 460,622 | 4.606 | 20 | 50 | fits | 153,927 | 120 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 625,601 | 6.256 | 20 | 50 | fits | 154,665 | 207 | 0.442 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 839,696 | 8.397 | 20 | 20 | fits | 136,439 | 130 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,168,184 | 11.682 | 20 | 20 | fits | 67,475 | 60 | 0.675 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 650,435 | 6.504 | 20 | 20 | fits | 154,419 | 208 | 0.374 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 467,561 | 4.676 | 20 | 200 | fits | 152,800 | 121 | 0.484 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 698,964 | 6.990 | 20 | 200 | fits | 154,419 | 208 | 0.374 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 468,485 | 4.685 | 20 | 20 | fits | 152,800 | 121 | 0.484 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 835,451 | 8.355 | 20 | 20 | fits | 135,783 | 129 | 0.616 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 161,180 | 1.612 | 20 | 24 | fits | 150,675 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 471,135 | 4.711 | 20 | 24 | fits | 152,800 | 121 | 0.484 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 471,069 | 4.711 | 20 | 50 | fits | 152,800 | 121 | 0.484 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 702,692 | 7.027 | 20 | 50 | fits | 154,419 | 208 | 0.374 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 838,409 | 8.384 | 20 | 20 | fits | 135,783 | 129 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,182,297 | 11.823 | 20 | 20 | fits | 71,582 | 67 | 0.702 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 645,314 | 6.453 | 20 | 20 | fits | 152,604 | 204 | 0.378 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 464,974 | 4.650 | 20 | 200 | fits | 148,045 | 157 | 0.449 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 694,562 | 6.946 | 20 | 200 | fits | 152,604 | 204 | 0.378 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 465,898 | 4.659 | 20 | 20 | fits | 148,045 | 157 | 0.449 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 832,234 | 8.322 | 20 | 20 | fits | 136,968 | 132 | 0.632 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 161,780 | 1.618 | 20 | 24 | fits | 164,751 | 75 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 468,548 | 4.685 | 20 | 24 | fits | 148,045 | 157 | 0.449 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 468,482 | 4.685 | 20 | 50 | fits | 148,045 | 157 | 0.449 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 698,290 | 6.983 | 20 | 50 | fits | 152,604 | 204 | 0.378 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 835,192 | 8.352 | 20 | 20 | fits | 136,968 | 132 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,174,061 | 11.741 | 20 | 20 | fits | 63,261 | 54 | 0.741 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 570,739 | 5.707 | 20 | 20 | fits | 156,803 | 211 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 453,704 | 4.537 | 20 | 200 | fits | 153,936 | 120 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 620,786 | 6.208 | 20 | 200 | fits | 156,803 | 211 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 454,628 | 4.546 | 20 | 20 | fits | 153,936 | 120 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 758,914 | 7.589 | 20 | 20 | fits | 137,424 | 132 | 0.634 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 155,305 | 1.553 | 20 | 24 | fits | 150,675 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 457,278 | 4.573 | 20 | 24 | fits | 153,936 | 120 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 457,212 | 4.572 | 20 | 50 | fits | 153,936 | 120 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 624,514 | 6.245 | 20 | 50 | fits | 156,803 | 211 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 761,872 | 7.619 | 20 | 20 | fits | 137,424 | 132 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 1,085,056 | 10.851 | 20 | 20 | fits | 62,382 | 53 | 0.734 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 563,580 | 5.636 | 20 | 20 | fits | 154,331 | 195 | 0.354 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 466,887 | 4.669 | 20 | 200 | fits | 155,527 | 138 | 0.461 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 620,602 | 6.206 | 20 | 200 | fits | 154,331 | 195 | 0.354 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 467,811 | 4.678 | 20 | 20 | fits | 155,527 | 138 | 0.461 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 758,300 | 7.583 | 20 | 20 | fits | 136,994 | 132 | 0.632 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 157,761 | 1.578 | 20 | 24 | fits | 150,675 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 470,461 | 4.705 | 20 | 24 | fits | 155,527 | 138 | 0.461 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 470,395 | 4.704 | 20 | 50 | fits | 155,527 | 138 | 0.461 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 624,330 | 6.243 | 20 | 50 | fits | 154,331 | 195 | 0.354 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 761,258 | 7.613 | 20 | 20 | fits | 136,994 | 132 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 1,099,842 | 10.998 | 20 | 20 | fits | 60,548 | 54 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 573,987 | 5.740 | 20 | 20 | fits | 153,957 | 209 | 0.365 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 467,966 | 4.680 | 20 | 200 | fits | 152,295 | 115 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 621,307 | 6.213 | 20 | 200 | fits | 153,957 | 209 | 0.365 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 468,890 | 4.689 | 20 | 20 | fits | 152,295 | 115 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 759,130 | 7.591 | 20 | 20 | fits | 137,119 | 132 | 0.634 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 160,291 | 1.603 | 20 | 24 | fits | 150,749 | 107 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 471,540 | 4.715 | 20 | 24 | fits | 152,295 | 115 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 471,474 | 4.715 | 20 | 50 | fits | 152,295 | 115 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 625,035 | 6.250 | 20 | 50 | fits | 153,957 | 209 | 0.365 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 762,088 | 7.621 | 20 | 20 | fits | 137,119 | 132 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 1,101,217 | 11.012 | 20 | 20 | fits | 68,911 | 61 | 0.695 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 557,428 | 5.574 | 20 | 20 | fits | 154,059 | 195 | 0.351 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 461,059 | 4.611 | 20 | 200 | fits | 153,558 | 131 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 614,502 | 6.145 | 20 | 200 | fits | 154,059 | 195 | 0.351 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 461,983 | 4.620 | 20 | 20 | fits | 153,558 | 131 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 748,577 | 7.486 | 20 | 20 | fits | 133,371 | 127 | 0.646 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 163,052 | 1.631 | 20 | 24 | fits | 150,845 | 106 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 464,633 | 4.646 | 20 | 24 | fits | 153,558 | 131 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 464,567 | 4.646 | 20 | 50 | fits | 153,558 | 131 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 618,230 | 6.182 | 20 | 50 | fits | 154,059 | 195 | 0.351 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 751,535 | 7.515 | 20 | 20 | fits | 133,371 | 127 | 0.646 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 1,095,466 | 10.955 | 20 | 20 | fits | 67,486 | 60 | 0.676 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 558,485 | 5.585 | 20 | 20 | fits | 151,245 | 200 | 0.416 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 448,174 | 4.482 | 20 | 200 | fits | 153,907 | 119 | 0.445 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 598,803 | 5.988 | 20 | 200 | fits | 151,245 | 200 | 0.416 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 449,098 | 4.491 | 20 | 20 | fits | 153,907 | 119 | 0.445 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 734,874 | 7.349 | 20 | 20 | fits | 135,367 | 130 | 0.611 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 148,953 | 1.490 | 20 | 24 | fits | 150,646 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 451,748 | 4.517 | 20 | 24 | fits | 153,907 | 119 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 451,682 | 4.517 | 20 | 50 | fits | 153,907 | 119 | 0.445 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 602,531 | 6.025 | 20 | 50 | fits | 151,245 | 200 | 0.416 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 737,832 | 7.378 | 20 | 20 | fits | 135,367 | 130 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 1,081,154 | 10.812 | 20 | 20 | fits | 67,232 | 60 | 0.672 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 553,986 | 5.540 | 20 | 20 | fits | 152,862 | 192 | 0.395 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 450,013 | 4.500 | 20 | 200 | fits | 153,558 | 131 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 602,259 | 6.023 | 20 | 200 | fits | 152,862 | 192 | 0.395 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 450,937 | 4.509 | 20 | 20 | fits | 153,558 | 131 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 742,477 | 7.425 | 20 | 20 | fits | 128,621 | 123 | 0.643 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 152,006 | 1.520 | 20 | 24 | fits | 150,646 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 453,587 | 4.536 | 20 | 24 | fits | 153,558 | 131 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 453,521 | 4.535 | 20 | 50 | fits | 153,558 | 131 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 605,987 | 6.060 | 20 | 50 | fits | 152,862 | 192 | 0.395 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 745,435 | 7.454 | 20 | 20 | fits | 128,621 | 123 | 0.643 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 1,084,360 | 10.844 | 20 | 20 | fits | 78,102 | 73 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 578,392 | 5.784 | 20 | 20 | fits | 150,796 | 209 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 447,381 | 4.474 | 20 | 200 | fits | 148,470 | 111 | 0.480 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 608,669 | 6.087 | 20 | 200 | fits | 150,796 | 209 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 448,305 | 4.483 | 20 | 20 | fits | 148,470 | 111 | 0.480 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 743,972 | 7.440 | 20 | 20 | fits | 134,599 | 125 | 0.600 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 154,462 | 1.545 | 20 | 24 | fits | 150,646 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 450,955 | 4.510 | 20 | 24 | fits | 148,470 | 111 | 0.480 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 450,889 | 4.509 | 20 | 50 | fits | 148,470 | 111 | 0.480 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 612,397 | 6.124 | 20 | 50 | fits | 150,796 | 209 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 746,930 | 7.469 | 20 | 20 | fits | 134,599 | 125 | 0.600 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 1,085,746 | 10.857 | 20 | 20 | fits | 78,102 | 73 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 554,769 | 5.548 | 20 | 20 | fits | 152,411 | 205 | 0.367 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 469,387 | 4.694 | 20 | 200 | fits | 155,346 | 125 | 0.451 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 621,182 | 6.212 | 20 | 200 | fits | 152,411 | 205 | 0.367 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 470,311 | 4.703 | 20 | 20 | fits | 155,346 | 125 | 0.451 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 759,084 | 7.591 | 20 | 20 | fits | 137,198 | 132 | 0.633 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 156,918 | 1.569 | 20 | 24 | fits | 150,646 | 106 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 472,961 | 4.730 | 20 | 24 | fits | 155,346 | 125 | 0.451 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 472,895 | 4.729 | 20 | 50 | fits | 155,346 | 125 | 0.451 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 624,910 | 6.249 | 20 | 50 | fits | 152,411 | 205 | 0.367 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 762,042 | 7.620 | 20 | 20 | fits | 137,198 | 132 | 0.633 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 1,079,733 | 10.797 | 20 | 20 | fits | 56,957 | 48 | 0.709 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 26,598 | 0.266 | 20 | 20 | fits | 34,025 | 27 (35) | 0.799 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 27,034 | 0.270 | 20 | 20 | fits | 30,001 | 23 (14) | 0.812 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 18,314 | 0.183 | 20 | 20 | fits | 29,707 | 24 (14) | 0.804 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 26,050 | 0.261 | 20 | 20 | fits | 33,892 | 27 (35) | 0.765 |
| a registering record of the burst | `srp.register_burst.t0.r0.if0` | 162,597 | 1.626 | 20 | 20 | fits | 112,785 | 47 | 0.848 |
| a registering record of the burst | `srp.register_burst.t0.r1.if0` | 162,514 | 1.625 | 20 | 20 | fits | 112,785 | 47 | 0.848 |
| a registering record of the burst | `srp.register_burst.t0.r2.if0` | 162,433 | 1.624 | 20 | 20 | fits | 112,785 | 47 | 0.848 |
| our MRPDU after a registering triple (JoinTime wait) | `srp.register_tx.t0.if0` | 500,459 | 5.005 | 220 | 220 | fits | 52,748 | 5 | 0.876 |
| ACMP's last record of its burst at a registering triple | `acmp.register_burst.t0.if0` | 340,004 | 3.400 | 20 | 20 | fits | 44,674 | 34 | 0.674 |
| AECP's last record of its burst at a registering triple | `aecp.register_burst.t0.if0` | 449,358 | 4.494 | 20 | 24 | fits | 138,907 | 100 | 0.332 |
| a registering record of the burst | `srp.register_burst.t1.r0.if0` | 174,398 | 1.744 | 20 | 20 | fits | 144,500 | 32 | 0.877 |
| a registering record of the burst | `srp.register_burst.t1.r1.if0` | 174,317 | 1.743 | 20 | 20 | fits | 144,500 | 32 | 0.877 |
| a registering record of the burst | `srp.register_burst.t1.r2.if0` | 174,234 | 1.742 | 20 | 20 | fits | 144,500 | 32 | 0.877 |
| our MRPDU after a registering triple (JoinTime wait) | `srp.register_tx.t1.if0` | 7,674,095 | 76.741 | 220 | 220 | fits | 138,225 | 8 | 0.735 |
| ACMP's last record of its burst at a registering triple | `acmp.register_burst.t1.if0` | 385,426 | 3.854 | 20 | 20 | fits | 107,206 | 122 | 0.402 |
| AECP's last record of its burst at a registering triple | `aecp.register_burst.t1.if0` | 555,106 | 5.551 | 20 | 24 | fits | 122,004 | 70 | 0.478 |
| a registering record of the burst | `srp.register_burst.t2.r0.if0` | 111,077 | 1.111 | 20 | 20 | fits | 100,183 | 38 | 0.804 |
| a registering record of the burst | `srp.register_burst.t2.r1.if0` | 110,996 | 1.110 | 20 | 20 | fits | 100,183 | 38 | 0.804 |
| a registering record of the burst | `srp.register_burst.t2.r2.if0` | 110,913 | 1.109 | 20 | 20 | fits | 100,183 | 38 | 0.804 |
| our MRPDU after a registering triple (JoinTime wait) | `srp.register_tx.t2.if0` | 15,629,854 | 156.299 | 220 | 220 | fits | 121,239 | 4 | 0.748 |
| ACMP's last record of its burst at a registering triple | `acmp.register_burst.t2.if0` | 136,693 | 1.367 | 20 | 20 | fits | 149,282 | 148 | 0.277 |
| AECP's last record of its burst at a registering triple | `aecp.register_burst.t2.if0` | 559,119 | 5.591 | 20 | 24 | fits | 118,584 | 66 | 0.478 |
| LINK_UP | `adp.link_up.if0` | 3,245 | 0.032 | 20 | 200 | fits | 31,162 | 44 (12) | 0.711 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,050 | 0.150 | 20 | 200 | fits | 21,634 | 23 (39) | 0.604 |
| LINK_DOWN | `adp.link_down.if0` | 2,014 | 0.020 | 20 | 200 | fits | 31,038 | 23 (9) | 0.667 |
| LINK_UP | `adp.link_up.if0` | 3,245 | 0.032 | 20 | 200 | fits | 31,162 | 44 (12) | 0.711 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,050 | 0.150 | 20 | 200 | fits | 21,634 | 23 (39) | 0.604 |
| GM_CHANGE | `adp.gm_change.if0` | 2,265 | 0.023 | 20 | 200 | fits | 16,365 | 17 (11) | 0.400 |
| LINK_UP | `adp.link_up.if0` | 3,245 | 0.032 | 20 | 200 | fits | 31,162 | 44 (12) | 0.711 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,050 | 0.150 | 20 | 200 | fits | 21,634 | 23 (39) | 0.604 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 5,195 | 0.052 | 20 | 200 | fits | 18,150 | 16 (31) | 0.562 |
| LINK_UP | `adp.link_up.if0` | 3,245 | 0.032 | 20 | 200 | fits | 31,162 | 44 (12) | 0.711 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,050 | 0.150 | 20 | 200 | fits | 21,634 | 23 (39) | 0.604 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 5,195 | 0.052 | 20 | 200 | fits | 18,150 | 16 (31) | 0.562 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 53,588 | 0.536 | 20 | 20 | fits | 15,020 | 9 | 0.849 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 40,832 | 0.408 | 20 | 20 | fits | 40,898 | 21 | 0.852 |
| malformed MRPDU discard | `srp.malformed.if0` | 24,490 | 0.245 | 20 | 20 | fits | 24,556 | 21 | 0.704 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 64,003 | 0.640 | 220 | 220 | fits | 34,588 | 7 | 0.919 |
| an event behind 15 others | `backlog.event.if0` | 168,879 | 1.689 | 20 | 200 | fits | 74,299 | 78 | 0.553 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 617,651 | 6.177 | 20 | 20 | fits | 144,134 | 131 | 0.270 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 496,924 | 4.969 | 20 | 200 | fits | 178,932 | 91 | 0.458 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 640,442 | 6.404 | 20 | 200 | fits | 144,134 | 131 | 0.270 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 492,602 | 4.926 | 20 | 20 | fits | 178,932 | 91 | 0.458 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 635,900 | 6.359 | 20 | 20 | fits | 144,134 | 131 | 0.270 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 158,677 | 1.587 | 20 | 24 | fits | 159,568 | 112 | 0.420 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 495,252 | 4.953 | 20 | 24 | fits | 178,932 | 91 | 0.458 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 495,186 | 4.952 | 20 | 50 | fits | 178,932 | 91 | 0.458 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 638,924 | 6.389 | 20 | 50 | fits | 144,134 | 131 | 0.270 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 692,453 | 6.925 | 20 | 20 | fits | 50,934 | 165 | 0.172 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 787,502 | 7.875 | 20 | 20 | fits | 44,032 | 118 | 0.199 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 551,691 | 5.517 | 20 | 20 | fits | 150,485 | 201 | 0.410 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 459,519 | 4.595 | 20 | 200 | fits | 154,999 | 126 | 0.449 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 609,388 | 6.094 | 20 | 200 | fits | 150,485 | 201 | 0.410 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 460,443 | 4.604 | 20 | 20 | fits | 154,999 | 126 | 0.449 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 745,279 | 7.453 | 20 | 20 | fits | 135,187 | 129 | 0.612 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 150,770 | 1.508 | 20 | 24 | fits | 150,956 | 109 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 463,093 | 4.631 | 20 | 24 | fits | 154,999 | 126 | 0.449 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 463,027 | 4.630 | 20 | 50 | fits | 154,999 | 126 | 0.449 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 613,116 | 6.131 | 20 | 50 | fits | 150,485 | 201 | 0.410 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 748,237 | 7.482 | 20 | 20 | fits | 135,187 | 129 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,076,079 | 10.761 | 20 | 20 | fits | 67,324 | 60 | 0.673 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 15,719 | 0.157 | 20 | 20 | fits | 28,178 | 19 | 0.748 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 459,519 | 4.595 | 20 | 200 | fits | 154,999 | 126 | 0.449 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 34,670 | 0.347 | 20 | 200 | fits | 28,178 | 19 | 0.748 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 460,443 | 4.604 | 20 | 20 | fits | 154,999 | 126 | 0.449 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 744,993 | 7.450 | 20 | 20 | fits | 137,029 | 132 | 0.627 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 150,770 | 1.508 | 20 | 24 | fits | 150,956 | 109 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 463,093 | 4.631 | 20 | 24 | fits | 154,999 | 126 | 0.449 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 463,027 | 4.630 | 20 | 50 | fits | 154,999 | 126 | 0.449 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 610,988 | 6.110 | 20 | 50 | fits | 148,357 | 201 | 0.354 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 747,951 | 7.480 | 20 | 20 | fits | 137,029 | 132 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,067,319 | 10.673 | 20 | 20 | fits | 58,718 | 51 | 0.686 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,410,278 | 64.103 | 20 | 20 | MISS ceiling | 23,029 | 18 | 0.659 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,429,627 | 64.296 | 20 | 20 | MISS ceiling | 22,567 | 13 | 0.558 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,452,165 | 64.522 | 20 | 20 | MISS ceiling | 21,022 | 13 | 0.583 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,472,814 | 64.728 | 20 | 20 | MISS ceiling | 20,359 | 13 | 0.541 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,493,027 | 64.930 | 20 | 20 | MISS ceiling | 20,276 | 13 | 0.550 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 309,781 | 3.098 | 20 | 200 | fits | 153,472 | 234 | 0.391 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 443,486 | 4.435 | 20 | 200 | fits | 134,321 | 138 | 0.611 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 305,459 | 3.055 | 20 | 20 | fits | 153,472 | 234 | 0.391 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,308,171 | 63.082 | 20 | 20 | MISS ceiling | 96,215 | 42 | 0.538 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 155,627 | 1.556 | 20 | 24 | fits | 149,430 | 107 | 0.420 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,311,657 | 63.117 | 20 | 24 | MISS ceiling | 96,215 | 42 | 0.538 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 308,043 | 3.080 | 20 | 50 | fits | 153,472 | 234 | 0.391 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 441,968 | 4.420 | 20 | 50 | fits | 134,321 | 138 | 0.611 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 441,902 | 4.419 | 20 | 20 | fits | 134,321 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 788,370 | 7.884 | 20 | 20 | fits | 78,987 | 73 | 0.664 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 7,998 | 0.080 | 20 | 20 | fits | 26,260 | 13 (29) | 0.764 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 8,521 | 0.085 | 20 | 20 | fits | 27,507 | 19 (35) | 0.737 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 21,901 | 0.219 | 20 | 20 | fits | 31,172 | 21 (12) | 0.797 |
| Talker Advertise RX for every input, bound | `srp.register_advertise.if0` | 103,259 | 1.033 | 20 | 20 | fits | 103,325 | 25 | 0.887 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 13,825 | 0.138 | 20 | 50 | fits | 31,162 | 44 | 0.711 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 21,641 | 0.216 | 20 | 50 | fits | 25,899 | 35 | 0.610 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 12,848 | 0.128 | 20 | 50 | fits | 28,349 | 41 | 0.554 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 17,749 | 0.177 | 20 | 50 | fits | 30,754 | 61 | 0.564 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 19,671 | 0.197 | 20 | 50 | fits | 30,754 | 61 | 0.564 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 11,544 | 0.115 | 20 | 50 | fits | 25,969 | 30 | 0.617 |
| set_name | `aecp_fanout.set_name.if0` | 55,193 | 0.552 | 20 | 24 | fits | 64,192 | 89 | 0.589 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 50,348 | 0.503 | 20 | 24 | fits | 58,177 | 78 | 0.625 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 49,784 | 0.498 | 20 | 24 | fits | 51,716 | 79 | 0.588 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 48,545 | 0.485 | 20 | 24 | fits | 50,845 | 78 | 0.583 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 57,015 | 0.570 | 20 | 24 | fits | 65,541 | 110 | 0.600 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 238,375 | 2.384 | 20 | 24 | fits | 61,567 | 109 | 0.574 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 325,259 | 3.253 | 20 | 24 | fits | 55,322 | 67 | 0.626 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 48,829 | 0.488 | 20 | 24 | fits | 51,516 | 78 | 0.592 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 47,205 | 0.472 | 20 | 24 | fits | 51,212 | 79 | 0.580 |
| BIND_RX | `acmp.bind_rx.if0` | 19,991 | 0.200 | 20 | 20 | fits | 46,175 | 26 (77) | 0.800 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 10,019 | 0.100 | 20 | 20 | fits | 33,043 | 19 (32) | 0.836 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,374 | 0.104 | 20 | 20 | fits | 27,912 | 15 (47) | 0.775 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 14,413 | 0.144 | 20 | 20 | fits | 42,352 | 19 (50) | 0.835 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 11,450 | 0.115 | 20 | 20 | fits | 28,361 | 17 (48) | 0.755 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 10,288 | 0.103 | 20 | 20 | fits | 26,530 | 16 (48) | 0.684 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,458 | 0.095 | 20 | 20 | fits | 25,324 | 16 (48) | 0.667 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,498 | 0.095 | 20 | 20 | fits | 25,316 | 16 (48) | 0.667 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 14,573 | 0.146 | 20 | 24 | fits | 29,084 | 20 | 0.775 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 34,151 | 0.342 | 20 | 24 | fits | 42,675 | 20 | 0.723 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 18,487 | 0.185 | 20 | 24 | fits | 30,190 | 20 | 0.750 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 21,320 | 0.213 | 20 | 24 | fits | 29,750 | 20 | 0.740 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 21,336 | 0.213 | 20 | 24 | fits | 29,755 | 20 | 0.741 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 18,646 | 0.186 | 20 | 24 | fits | 30,148 | 20 | 0.741 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 21,341 | 0.213 | 20 | 24 | fits | 29,540 | 20 | 0.744 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 17,625 | 0.176 | 20 | 24 | fits | 28,929 | 20 | 0.754 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 21,000 | 0.210 | 20 | 24 | fits | 29,089 | 20 | 0.759 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 25,316 | 0.253 | 20 | 24 | fits | 34,065 | 21 | 0.668 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 17,687 | 0.177 | 20 | 24 | fits | 29,341 | 20 | 0.780 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 20,619 | 0.206 | 20 | 24 | fits | 28,885 | 20 | 0.777 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i79.c0.if0` | 17,918 | 0.179 | 20 | 24 | fits | 29,170 | 20 | 0.743 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 21,513 | 0.215 | 20 | 24 | fits | 29,812 | 20 | 0.749 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 18,120 | 0.181 | 20 | 24 | fits | 29,557 | 20 | 0.746 |
| get_configuration | `aecp.get_configuration.if0` | 16,016 | 0.160 | 20 | 24 | fits | 27,361 | 20 | 0.769 |
| entity_available | `aecp.entity_available.if0` | 18,810 | 0.188 | 20 | 24 | fits | 26,796 | 20 | 0.748 |
| get_name | `aecp.get_name.if0` | 18,529 | 0.185 | 20 | 24 | fits | 29,933 | 20 | 0.760 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 23,208 | 0.232 | 20 | 24 | fits | 32,062 | 26 | 0.756 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 19,327 | 0.193 | 20 | 24 | fits | 31,366 | 28 | 0.776 |
| get_as_path, refused ENTITY_MISBEHAVING | `aecp.get_as_path.if0` | 22,212 | 0.222 | 20 | 24 | fits | 31,124 | 28 | 0.784 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 18,910 | 0.189 | 20 | 24 | fits | 27,062 | 20 | 0.769 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 14,859 | 0.149 | 20 | 24 | fits | 25,565 | 20 | 0.730 |
| set_name | `aecp.set_name.if0` | 28,604 | 0.286 | 20 | 24 | fits | 50,200 | 43 | 0.769 |
| lock_entity | `aecp.lock_entity.if0` | 22,116 | 0.221 | 20 | 24 | fits | 39,559 | 34 | 0.805 |
| unlock_entity | `aecp.unlock_entity.if0` | 26,050 | 0.261 | 20 | 24 | fits | 39,148 | 33 | 0.802 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 140,000 | 1.400 | 20 | 24 | fits | 149,311 | 137 | 0.321 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 240,420 | 2.404 | 20 | 24 | fits | 141,124 | 119 | 0.283 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 213,337 | 2.133 | 20 | 24 | fits | 47,305 | 18 | 0.651 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 361,074 | 3.611 | 20 | 24 | fits | 79,833 | 17 | 0.652 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 334,761 | 3.348 | 20 | 24 | fits | 90,908 | 17 | 0.649 |
| READ_DESCRIPTOR held for a token (#917) | `aecp.held.read_descriptor.if0` | 534,126 | 5.341 | 20 | 24 | fits | 41,958 | 17 | 0.731 |
| LINK_UP | `fixture.link_up.if0` | 3,245 | 0.032 | 20 | 200 | fits | 31,162 | 44 (12) | 0.711 |
| malformed MRPDU discard | `fixture.malformed.if0` | 24,625 | 0.246 | 20 | 20 | fits | 24,691 | 21 | 0.712 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 35,389 | 0.354 | 20 | 24 | fits | 51,479 | 43 | 0.782 |
| LINK_DOWN | `fixture.link_down.if0` | 2,390 | 0.024 | 20 | 200 | fits | 33,239 | 23 (9) | 0.735 |
| BIND_RX | `fixture.bind_rx.if0` | 20,769 | 0.208 | 20 | 20 | fits | 46,302 | 26 (77) | 0.808 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 11,229 | 0.112 | 20 | 20 | fits | 38,628 | 29 (35) | 0.771 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 11,929 | 0.119 | 20 | 20 | fits | 26,861 | 13 (29) | 0.775 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 96,388 | 0.964 | 20 | 200 | fits | 96,492 | 84 | 0.735 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 96,388 | 0.964 | 20 | 200 | fits | 96,492 | 84 | 0.735 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 96,114 | 0.961 | 20 | 20 | fits | 96,492 | 84 | 0.735 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 96,114 | 0.961 | 20 | 20 | fits | 96,492 | 84 | 0.735 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 96,322 | 0.963 | 20 | 24 | fits | 96,492 | 84 | 0.735 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 96,322 | 0.963 | 20 | 24 | fits | 96,492 | 84 | 0.735 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 96,256 | 0.963 | 20 | 50 | fits | 96,492 | 84 | 0.735 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 96,256 | 0.963 | 20 | 50 | fits | 96,492 | 84 | 0.735 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 96,190 | 0.962 | 20 | 20 | fits | 96,492 | 84 | 0.735 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 96,190 | 0.962 | 20 | 20 | fits | 96,492 | 84 | 0.735 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `srp-bound`: wait quiet TIMEOUT
- `srp-bound`: wait quiet TIMEOUT
- `srp-bound`: wait quiet TIMEOUT
- `srp-bound`: wait quiet TIMEOUT
- `srp-bound`: wait quiet TIMEOUT
- `srp-bound`: wait quiet TIMEOUT
- `srp-bound`: wait quiet TIMEOUT
- `srp-bound`: wait quiet TIMEOUT
- `srp-register`: wait quiet TIMEOUT
