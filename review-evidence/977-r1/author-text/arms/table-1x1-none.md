### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 117 paths and 7 of 987 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.192 (0.381) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.089 (0.204) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.077 (0.200) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.146 (0.436) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.108 (0.222) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.092 (0.204) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.102 (0.212) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.113 (0.228) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.099 (0.270) | fits | 0 acmp | 1 | 0 |
| ACMP's last record of its burst at a registering triple | 0 | `acmp.register_burst.t0.if0` (srp-register-burst) | 1.419 (2.526) | fits | 11 acmp | 1 | 0 |
| ACMP's last record of its burst at a registering triple | 0 | `acmp.register_burst.t1.if0` (srp-register-burst) | 2.413 (3.162) | fits | 11 acmp | 1 | 0 |
| ACMP's last record of its burst at a registering triple | 0 | `acmp.register_burst.t2.if0` (srp-register-burst) | 1.120 (1.415) | fits | 11 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.163 (0.427) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.169 (0.432) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.182 (0.458) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.111 (0.430) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.083 (0.419) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.151 (0.412) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.133 (0.346) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.049 (0.131) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.022 (0.120) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.024 (0.221) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.033 (0.237) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.125 (0.245) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.085 (0.314) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.127 (0.369) | fits | 0 aecp | 1 | 0 |
| get_as_path, refused ENTITY_MISBEHAVING | 0 | `aecp.get_as_path.if0` (aecp) | 0.158 (0.412) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.195 (0.454) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.153 (0.397) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.170 (0.427) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.174 (0.424) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR held for a token (#917) | 0 | `aecp.held.read_descriptor.if0` (aecp-held) | 5.183 (5.428) | fits | 16 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.217 (0.525) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.146 (0.388) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.208 (0.459) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.158 (0.408) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.153 (0.401) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.170 (0.421) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.174 (0.422) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.168 (0.420) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.142 (0.391) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.174 (0.427) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.174 (0.425) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.155 (0.404) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.150 (0.401) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.160 (0.408) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.181 (0.432) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.172 (0.422) | fits | 0 aecp | 1 | 0 |
| AECP's last record of its burst at a registering triple | 0 | `aecp.register_burst.t0.if0` (srp-register-burst) | 1.798 (2.062) | fits | 15 aecp | 1 | 0 |
| AECP's last record of its burst at a registering triple | 0 | `aecp.register_burst.t1.if0` (srp-register-burst) | 2.610 (3.158) | fits | 15 aecp | 1 | 0 |
| AECP's last record of its burst at a registering triple | 0 | `aecp.register_burst.t2.if0` (srp-register-burst) | 3.002 (3.346) | fits | 15 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.109 (0.239) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.215 (0.566) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.155 (0.400) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.193 (0.515) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.734 (3.014) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.379 (0.608) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.494 (0.749) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.415 (0.661) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.371 (0.599) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.410 (0.678) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.359 (3.602) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.362 (0.614) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 3.388 (3.636) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.406 (2.709) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.940 (4.245) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.526 (3.830) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.370 (1.503) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.518 (3.706) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-7.adp_available.if0` (backlog-adp@blank-7) | 4.043 (5.365) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.068 (0.210) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.486 (1.855) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.528 (62.641) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.106 (63.222) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.299 (0.424) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-flight.held.acmp.if0` (save-flight) | 2.252 | fits | 11 acmp | 4 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-burst.held.adp.if0` (save-burst) | 1.539 | fits | 7 adp | 4 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 2.613 | fits | 15 aecp | 4 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 2.037 | fits | 6 maap | 4 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.140 | fits | 31 srp | 4 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.134 (0.384) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.093 (0.181) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.104 (0.237) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.114 (0.384) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.145 (0.377) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 1.688 | fits | 0 srp | 4 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 3.661 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 61.808 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 3.704 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 4.533 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@program-7.service.aecp.first.if0` (backlog-adp@program-7) | 2.161 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.589 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 3.687 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 4.571 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-6.service.srp.first.if0` (backlog-adp@program-aged2-6) | 5.487 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-4.service.srp.last.if0` (backlog-adp@program-aged2-4) | 9.455 | fits | 31 srp | 77 | 0 |
| Talker Advertise RX for every input, bound | 0 | `srp.bound_advertise.if0` (srp-bound) | 0.501 (0.502) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.575 (0.649) | fits | 0 srp | 1 | 0 |
| Talker Advertise RX for every input, no binding (kept) | 0 | `srp.kept_advertise.if0` (srp-kept) | 0.443 (0.444) | fits | 0 srp | 1 | 0 |
| Talker Failed RX for every input, no binding (kept) | 0 | `srp.kept_failed.if0` (srp-kept) | 0.452 (0.453) | fits | 0 srp | 1 | 0 |
| Talker RX at the bound after a freed block (count) | 0 | `srp.kept_recount.if0` (srp-kept) | 0.414 (0.415) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.346 (0.347) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.188 (0.189) | fits | 0 srp | 2 | 0 |
| Talker Advertise RX for every input, bound | 0 | `srp.register_advertise.if0` (srp-register) | 0.499 (0.500) | fits | 0 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t0.r0.if0` (srp-register-burst) | 1.017 (1.145) | fits | 0 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t0.r1.if0` (srp-register-burst) | 1.016 (1.144) | fits | 1 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t0.r2.if0` (srp-register-burst) | 1.015 (1.143) | fits | 2 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t1.r0.if0` (srp-register-burst) | 0.711 (0.840) | fits | 0 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t1.r1.if0` (srp-register-burst) | 0.710 (0.839) | fits | 1 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t1.r2.if0` (srp-register-burst) | 0.710 (0.838) | fits | 2 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t2.r0.if0` (srp-register-burst) | 0.915 (1.043) | fits | 0 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t2.r1.if0` (srp-register-burst) | 0.914 (1.042) | fits | 1 srp | 1 | 0 |
| a registering record of the burst | 0 | `srp.register_burst.t2.r2.if0` (srp-register-burst) | 0.913 (1.042) | fits | 2 srp | 1 | 0 |
| our MRPDU after a registering triple (JoinTime wait) | 0 | `srp.register_tx.t0.if0` (srp-register-burst) | 1.311 (1.562) | fits | 2 srp | 1 | 0 |
| our MRPDU after a registering triple (JoinTime wait) | 0 | `srp.register_tx.t1.if0` (srp-register-burst) | 76.703 (76.985) | fits | 2 srp | 1 | 0 |
| our MRPDU after a registering triple (JoinTime wait) | 0 | `srp.register_tx.t2.if0` (srp-register-burst) | 156.757 (157.037) | fits | 2 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.463 (0.543) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.999 | 10 | 144,365 (1.444) | yes | - |
| backlog-adp@blank-1 | 0 | 11.874 | 10 | 144,365 (1.444) | yes | - |
| backlog-adp@blank-2 | 0 | 11.749 | 10 | 144,365 (1.444) | yes | - |
| backlog-adp@blank-3 | 0 | 11.624 | 10 | 144,365 (1.444) | yes | - |
| backlog-adp@blank-4 | 0 | 11.499 | 10 | 144,365 (1.444) | yes | - |
| backlog-adp@blank-5 | 0 | 11.374 | 10 | 144,365 (1.444) | yes | - |
| backlog-adp@blank-6 | 0 | 11.249 | 10 | 144,365 (1.444) | yes | - |
| backlog-adp@blank-7 | 0 | 14.093 | 13 | 143,003 (1.430) | yes | - |
| backlog-adp@program-0 | 0 | 11.251 | 12 | 146,306 (1.463) | yes | - |
| backlog-adp@program-1 | 0 | 10.995 | 12 | 146,301 (1.463) | yes | - |
| backlog-adp@program-2 | 0 | 11.694 | 12 | 145,025 (1.450) | yes | - |
| backlog-adp@program-3 | 0 | 11.444 | 12 | 145,025 (1.450) | yes | - |
| backlog-adp@program-4 | 1 | 10.979 | 11 | 144,788 (1.448) | yes | - |
| backlog-adp@program-5 | 0 | 10.070 | 11 | 144,095 (1.441) | yes | - |
| backlog-adp@program-6 | 0 | 10.755 | 10 | 143,973 (1.440) | yes | - |
| backlog-adp@program-7 | 0 | 10.653 | 10 | 144,510 (1.445) | yes | - |
| backlog-adp@verify-0 | 0 | 14.058 | 13 | 144,774 (1.448) | yes | - |
| backlog-adp@verify-1 | 0 | 13.933 | 13 | 144,774 (1.448) | yes | - |
| backlog-adp@verify-2 | 0 | 13.808 | 13 | 144,774 (1.448) | yes | - |
| backlog-adp@verify-3 | 0 | 13.683 | 13 | 144,774 (1.448) | yes | - |
| backlog-adp@verify-4 | 0 | 13.558 | 13 | 144,774 (1.448) | yes | - |
| backlog-adp@verify-5 | 0 | 13.433 | 13 | 144,774 (1.448) | yes | - |
| backlog-adp@verify-6 | 0 | 13.201 | 12 | 144,768 (1.448) | yes | - |
| backlog-adp@verify-7 | 0 | 13.076 | 12 | 144,768 (1.448) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 12.405 | 12 | 144,125 (1.441) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 11.285 | 11 | 144,001 (1.440) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 12.062 | 10 | 144,670 (1.447) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 12.074 | 10 | 144,651 (1.447) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 11.983 | 9 | 145,519 (1.455) | yes | - |
| backlog-adp@blank-aged2-5 | 1 | 13.091 | 11 | 144,566 (1.446) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 12.232 | 12 | 144,350 (1.444) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 13.947 | 11 | 147,776 (1.478) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 13.318 | 13 | 144,169 (1.442) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 12.422 | 13 | 146,364 (1.464) | yes | - |
| backlog-adp@blank-aged1-2 | 1 | 11.253 | 9 | 145,563 (1.456) | yes | - |
| backlog-adp@blank-aged1-3 | 1 | 11.229 | 9 | 145,604 (1.456) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 11.237 | 10 | 144,717 (1.447) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 11.247 | 10 | 143,612 (1.436) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 11.266 | 10 | 144,122 (1.441) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 11.288 | 10 | 147,867 (1.479) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 12.250 | 13 | 144,233 (1.442) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 11.069 | 13 | 144,344 (1.443) | yes | - |
| backlog-adp@program-aged2-2 | 1 | 10.697 | 9 | 143,552 (1.436) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 10.711 | 10 | 143,944 (1.439) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 10.741 | 10 | 144,613 (1.446) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 10.720 | 10 | 144,594 (1.446) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 10.729 | 10 | 143,473 (1.435) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 10.656 | 9 | 144,491 (1.445) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 10.963 | 11 | 143,999 (1.440) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.681 | 10 | 143,354 (1.434) | yes | - |
| backlog-adp@program-aged1-2 | 1 | 10.599 | 9 | 143,627 (1.436) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 10.954 | 12 | 146,307 (1.463) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 10.684 | 10 | 144,679 (1.447) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 10.614 | 9 | 145,547 (1.455) | yes | - |
| backlog-adp@program-aged1-6 | 1 | 10.633 | 9 | 145,528 (1.455) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 10.633 | 10 | 148,438 (1.484) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 12.413 | 12 | 145,113 (1.451) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 11.277 | 11 | 144,661 (1.447) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 12.083 | 10 | 143,540 (1.435) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 12.117 | 10 | 144,066 (1.441) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 12.115 | 10 | 144,011 (1.440) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 13.161 | 11 | 143,694 (1.437) | yes | - |
| backlog-adp@verify-aged2-6 | 1 | 12.258 | 11 | 146,031 (1.460) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 13.992 | 11 | 143,484 (1.435) | yes | - |
| backlog-adp@verify-aged1-0 | 1 | 13.335 | 12 | 145,697 (1.457) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 12.440 | 13 | 145,167 (1.452) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 11.413 | 11 | 144,034 (1.440) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 11.257 | 9 | 144,356 (1.444) | yes | - |
| backlog-adp@verify-aged1-4 | 1 | 11.269 | 9 | 143,353 (1.434) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 11.279 | 10 | 143,943 (1.439) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 11.275 | 10 | 144,612 (1.446) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 11.294 | 10 | 143,606 (1.436) | yes | - |
| backlog | 0 | 5.240 | 7 | 139,223 (1.392) | yes | - |
| backlog-adp | 0 | 8.968 | 10 | 144,285 (1.443) | yes | - |
| backlog-adp-refill | 0 | 40.554 | 25 | 144,285 (1.443) | yes | - |
| backlog-owed | 0 | 63.582 | 25 | 147,371 (1.474) | yes | - |
| fixture | 0 | 1.134 | 2 | 76,996 (0.770) | yes | - |

Composed maximum over the 4 backlog windows: 147,371 CPU cycles (1.474 ms), backlog-owed.
Over the windows that released their whole load only: 147,371 (1.474 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-kept | 1909 | 0 | 45,276 (0.453) | fits |
| save-flight | 2988 | 0 | 154,717 (1.547) | fits |
| save-burst | 2742 | 0 | 154,717 (1.547) | fits |
| acmp-notk | 3356 | 0 | 95,390 (0.954) | fits |
| save-second | 66029 | 0 | 44,382 (0.444) | fits |
| adp-advertise | 880 | 0 | 23,744 (0.237) | fits |
| backlog-adp@blank-0 | 480 | 0 | 144,365 (1.444) | fits |
| backlog-adp@blank-1 | 480 | 0 | 144,365 (1.444) | fits |
| backlog-adp@blank-2 | 480 | 0 | 144,365 (1.444) | fits |
| backlog-adp@blank-3 | 480 | 0 | 144,365 (1.444) | fits |
| backlog-adp@blank-4 | 480 | 0 | 144,365 (1.444) | fits |
| backlog-adp@blank-5 | 480 | 0 | 144,365 (1.444) | fits |
| backlog-adp@blank-6 | 480 | 0 | 144,365 (1.444) | fits |
| backlog-adp@blank-7 | 483 | 0 | 143,003 (1.430) | fits |
| backlog-adp@program-0 | 491 | 0 | 146,306 (1.463) | fits |
| backlog-adp@program-1 | 491 | 0 | 146,301 (1.463) | fits |
| backlog-adp@program-2 | 491 | 0 | 145,025 (1.450) | fits |
| backlog-adp@program-3 | 491 | 0 | 145,025 (1.450) | fits |
| backlog-adp@program-4 | 491 | 0 | 144,788 (1.448) | fits |
| backlog-adp@program-5 | 491 | 0 | 144,095 (1.441) | fits |
| backlog-adp@program-6 | 491 | 0 | 143,973 (1.440) | fits |
| backlog-adp@program-7 | 491 | 0 | 144,510 (1.445) | fits |
| backlog-adp@verify-0 | 497 | 0 | 144,774 (1.448) | fits |
| backlog-adp@verify-1 | 497 | 0 | 144,774 (1.448) | fits |
| backlog-adp@verify-2 | 497 | 0 | 144,774 (1.448) | fits |
| backlog-adp@verify-3 | 497 | 0 | 144,774 (1.448) | fits |
| backlog-adp@verify-4 | 497 | 0 | 144,774 (1.448) | fits |
| backlog-adp@verify-5 | 497 | 0 | 144,774 (1.448) | fits |
| backlog-adp@verify-6 | 496 | 0 | 144,768 (1.448) | fits |
| backlog-adp@verify-7 | 496 | 0 | 144,768 (1.448) | fits |
| backlog-adp@blank-aged2-0 | 861 | 0 | 144,125 (1.441) | fits |
| backlog-adp@blank-aged2-1 | 870 | 0 | 144,001 (1.440) | fits |
| backlog-adp@blank-aged2-2 | 880 | 0 | 144,670 (1.447) | fits |
| backlog-adp@blank-aged2-3 | 891 | 0 | 144,651 (1.447) | fits |
| backlog-adp@blank-aged2-4 | 901 | 0 | 145,519 (1.455) | fits |
| backlog-adp@blank-aged2-5 | 914 | 0 | 144,566 (1.446) | fits |
| backlog-adp@blank-aged2-6 | 925 | 0 | 144,350 (1.444) | fits |
| backlog-adp@blank-aged2-7 | 935 | 0 | 147,776 (1.478) | fits |
| backlog-adp@blank-aged1-0 | 775 | 0 | 144,169 (1.442) | fits |
| backlog-adp@blank-aged1-1 | 786 | 0 | 146,364 (1.464) | fits |
| backlog-adp@blank-aged1-2 | 794 | 0 | 145,563 (1.456) | fits |
| backlog-adp@blank-aged1-3 | 804 | 0 | 145,604 (1.456) | fits |
| backlog-adp@blank-aged1-4 | 815 | 0 | 144,717 (1.447) | fits |
| backlog-adp@blank-aged1-5 | 826 | 0 | 143,612 (1.436) | fits |
| backlog-adp@blank-aged1-6 | 837 | 0 | 144,122 (1.441) | fits |
| backlog-adp@blank-aged1-7 | 848 | 0 | 147,867 (1.479) | fits |
| backlog-adp@program-aged2-0 | 910 | 0 | 144,233 (1.442) | fits |
| backlog-adp@program-aged2-1 | 921 | 0 | 144,344 (1.443) | fits |
| backlog-adp@program-aged2-2 | 929 | 0 | 143,552 (1.436) | fits |
| backlog-adp@program-aged2-3 | 939 | 0 | 143,944 (1.439) | fits |
| backlog-adp@program-aged2-4 | 950 | 0 | 144,613 (1.446) | fits |
| backlog-adp@program-aged2-5 | 961 | 0 | 144,594 (1.446) | fits |
| backlog-adp@program-aged2-6 | 972 | 0 | 143,473 (1.435) | fits |
| backlog-adp@program-aged2-7 | 982 | 0 | 144,491 (1.445) | fits |
| backlog-adp@program-aged1-0 | 822 | 0 | 143,999 (1.440) | fits |
| backlog-adp@program-aged1-1 | 832 | 0 | 143,354 (1.434) | fits |
| backlog-adp@program-aged1-2 | 842 | 0 | 143,627 (1.436) | fits |
| backlog-adp@program-aged1-3 | 855 | 0 | 146,307 (1.463) | fits |
| backlog-adp@program-aged1-4 | 864 | 0 | 144,679 (1.447) | fits |
| backlog-adp@program-aged1-5 | 874 | 0 | 145,547 (1.455) | fits |
| backlog-adp@program-aged1-6 | 885 | 0 | 145,528 (1.455) | fits |
| backlog-adp@program-aged1-7 | 896 | 0 | 148,438 (1.484) | fits |
| backlog-adp@verify-aged2-0 | 849 | 0 | 145,113 (1.451) | fits |
| backlog-adp@verify-aged2-1 | 858 | 0 | 144,661 (1.447) | fits |
| backlog-adp@verify-aged2-2 | 868 | 0 | 143,540 (1.435) | fits |
| backlog-adp@verify-aged2-3 | 879 | 0 | 144,066 (1.441) | fits |
| backlog-adp@verify-aged2-4 | 890 | 0 | 144,011 (1.440) | fits |
| backlog-adp@verify-aged2-5 | 902 | 0 | 143,694 (1.437) | fits |
| backlog-adp@verify-aged2-6 | 913 | 0 | 146,031 (1.460) | fits |
| backlog-adp@verify-aged2-7 | 923 | 0 | 143,484 (1.435) | fits |
| backlog-adp@verify-aged1-0 | 763 | 0 | 145,697 (1.457) | fits |
| backlog-adp@verify-aged1-1 | 774 | 0 | 145,167 (1.452) | fits |
| backlog-adp@verify-aged1-2 | 783 | 0 | 144,034 (1.440) | fits |
| backlog-adp@verify-aged1-3 | 792 | 0 | 144,356 (1.444) | fits |
| backlog-adp@verify-aged1-4 | 803 | 0 | 143,353 (1.434) | fits |
| backlog-adp@verify-aged1-5 | 814 | 0 | 143,943 (1.439) | fits |
| backlog-adp@verify-aged1-6 | 825 | 0 | 144,612 (1.446) | fits |
| backlog-adp@verify-aged1-7 | 836 | 0 | 143,606 (1.436) | fits |
| save-held | 1402 | 0 | 154,717 (1.547) | fits |
| save-starved | 35314 | 0 | 154,717 (1.547) | fits |
| srp-bound | 1233 | 0 | 98,272 (0.983) | fits |
| acmp-noresp | 1889 | 0 | 94,641 (0.946) | fits |
| save | 609 | 0 | 40,413 (0.404) | fits |
| srp-register-burst | 2105 | 0 | 144,970 (1.450) | fits |
| adp-link | 373 | 0 | 30,723 (0.307) | fits |
| adp-gm | 372 | 0 | 23,744 (0.237) | fits |
| adp-discover | 372 | 0 | 23,744 (0.237) | fits |
| control | 372 | 0 | 23,744 (0.237) | fits |
| srp | 289 | 0 | 34,667 (0.347) | fits |
| backlog | 285 | 0 | 139,223 (1.392) | fits |
| backlog-adp | 313 | 0 | 144,285 (1.443) | fits |
| backlog-adp-refill | 328 | 0 | 144,285 (1.443) | fits |
| backlog-owed | 309 | 0 | 147,371 (1.474) | fits |
| acmp-disc | 877 | 0 | 94,649 (0.946) | fits |
| maap | 177 | 0 | 23,744 (0.237) | fits |
| aecp-fanout | 112 | 0 | 58,876 (0.589) | fits |
| acmp-cmd | 85 | 0 | 37,636 (0.376) | fits |
| aecp | 112 | 0 | 40,858 (0.409) | fits |
| srp-register | 395 | 0 | 49,981 (0.500) | fits |
| aecp-largest-notice | 106 | 0 | 150,315 (1.503) | fits |
| aecp-held | 108 | 0 | 30,855 (0.309) | fits |
| datapath-events | 117 | 0 | 23,744 (0.237) | fits |
| fixture | 161 | 0 | 76,996 (0.770) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 8.493 (20) | 11.507 |
| backlog-adp@blank-aged2-1 | 2 | none | +8.778 ms, 76,316 (0.763 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 8.596 (20) | 11.404 |
| backlog-adp@blank-aged2-2 | 2 | +7.929 ms, 76,652 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 9.415 (20) | 10.585 |
| backlog-adp@blank-aged2-3 | 2 | +7.080 ms, 76,652 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 9.428 (20) | 10.572 |
| backlog-adp@blank-aged2-4 | 2 | +5.370 ms, 76,652 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 9.331 (20) | 10.669 |
| backlog-adp@blank-aged2-5 | 2 | +4.600 ms, 76,652 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 9.309 (20) | 10.691 |
| backlog-adp@blank-aged2-6 | 2 | +3.793 ms, 76,594 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 9.315 (20) | 10.685 |
| backlog-adp@blank-aged2-7 | 2 | +2.915 ms, 76,484 (0.765 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 9.445 (20) | 10.555 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 8.537 (20) | 11.463 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 8.505 (20) | 11.495 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 8.462 (20) | 11.538 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 8.580 (20) | 11.420 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 8.588 (20) | 11.412 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 8.599 (20) | 11.401 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 8.611 (20) | 11.389 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 8.630 (20) | 11.370 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 8.571 (20) | 11.429 |
| backlog-adp@program-aged2-1 | 2 | none | +8.741 ms, 80,486 (0.805 ms), issue | `backlog-adp@program-aged2-1.service.srp.last.if0` | 8.554 (20) | 11.446 |
| backlog-adp@program-aged2-2 | 2 | none | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 9.411 (20) | 10.589 |
| backlog-adp@program-aged2-3 | 2 | none | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 9.427 (20) | 10.573 |
| backlog-adp@program-aged2-4 | 2 | +5.270 ms, 80,624 (0.806 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 9.455 (20) | 10.545 |
| backlog-adp@program-aged2-5 | 2 | none | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 9.437 (20) | 10.563 |
| backlog-adp@program-aged2-6 | 2 | none | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 9.442 (20) | 10.558 |
| backlog-adp@program-aged2-7 | 2 | +3.789 ms, 80,793 (0.808 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 9.366 (20) | 10.634 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 8.635 (20) | 11.365 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 8.517 (20) | 11.483 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 8.562 (20) | 11.438 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 8.534 (20) | 11.466 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 8.652 (20) | 11.348 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 8.582 (20) | 11.418 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 8.601 (20) | 11.399 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 8.601 (20) | 11.399 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 8.549 (20) | 11.451 |
| backlog-adp@verify-aged2-1 | 2 | none | +8.741 ms, 77,245 (0.772 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 8.559 (20) | 11.441 |
| backlog-adp@verify-aged2-2 | 2 | +7.904 ms, 77,581 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 9.402 (20) | 10.598 |
| backlog-adp@verify-aged2-3 | 2 | +7.076 ms, 77,581 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 9.437 (20) | 10.563 |
| backlog-adp@verify-aged2-4 | 2 | +5.454 ms, 77,581 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 9.429 (20) | 10.571 |
| backlog-adp@verify-aged2-5 | 2 | +4.610 ms, 77,581 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 9.331 (20) | 10.669 |
| backlog-adp@verify-aged2-6 | 2 | +3.774 ms, 77,579 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 9.307 (20) | 10.693 |
| backlog-adp@verify-aged2-7 | 2 | +2.856 ms, 77,418 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 9.435 (20) | 10.565 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 8.499 (20) | 11.501 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 8.479 (20) | 11.521 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 8.732 (20) | 11.268 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 8.577 (20) | 11.423 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 8.590 (20) | 11.410 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 8.601 (20) | 11.399 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 8.589 (20) | 11.411 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 8.605 (20) | 11.395 |

Least margin over the aged windows: 10.545 ms, `backlog-adp@program-aged2-4.service.srp.last.if0` at 9.455 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.403 | 6,070 | 102 | 2 | 30.823 | yes | within |
| save-held | 1084.952 | 4,070 | 102 | - | 21.218 | no | within |
| save-starved | 4049.131 | 4,070 | 102 | - | 31.262 | yes | within |
| save | 1076.272 | 4,070 | 102 | - | 24.122 | no | within |

Names from their response to durable (save_burst.py; #920, #665's ruling of 2026-11-15, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-flight | 1 | 146.887 (0) | 5,000 | 2 | - | - | 19 steps (want 19), 5.938 ms | within |
| save-burst | 39 | 1098.659 (0) | 5,000 | 1 | - | - | sequence 1, 0 missing | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-kept | 1844 | 18,760 (0.188) | 2,258 (0.023) |
| save-flight | 1554 | 91,760 (0.918) | 78,523 (0.785) |
| save-burst | 1480 | 90,039 (0.900) | 77,702 (0.777) |
| acmp-notk | 1159 | 95,390 (0.954) | 78,327 (0.783) |
| save-second | 520 | 79,922 (0.799) | 77,832 (0.778) |
| adp-advertise | 853 | 18,532 (0.185) | 2,258 (0.023) |
| backlog-adp@blank-0 | 342 | 88,824 (0.888) | 75,918 (0.759) |
| backlog-adp@blank-1 | 342 | 88,824 (0.888) | 75,918 (0.759) |
| backlog-adp@blank-2 | 342 | 88,824 (0.888) | 75,918 (0.759) |
| backlog-adp@blank-3 | 342 | 88,824 (0.888) | 75,918 (0.759) |
| backlog-adp@blank-4 | 342 | 88,824 (0.888) | 75,918 (0.759) |
| backlog-adp@blank-5 | 342 | 88,824 (0.888) | 75,918 (0.759) |
| backlog-adp@blank-6 | 342 | 88,824 (0.888) | 75,918 (0.759) |
| backlog-adp@blank-7 | 345 | 90,051 (0.901) | 75,918 (0.759) |
| backlog-adp@program-0 | 373 | 98,579 (0.986) | 78,275 (0.783) |
| backlog-adp@program-1 | 373 | 100,624 (1.006) | 78,645 (0.786) |
| backlog-adp@program-2 | 374 | 94,346 (0.943) | 78,360 (0.784) |
| backlog-adp@program-3 | 374 | 94,346 (0.943) | 78,360 (0.784) |
| backlog-adp@program-4 | 374 | 94,346 (0.943) | 78,360 (0.784) |
| backlog-adp@program-5 | 373 | 90,458 (0.905) | 77,930 (0.779) |
| backlog-adp@program-6 | 374 | 92,644 (0.926) | 78,569 (0.786) |
| backlog-adp@program-7 | 375 | 90,446 (0.904) | 77,930 (0.779) |
| backlog-adp@verify-0 | 400 | 91,351 (0.914) | 77,930 (0.779) |
| backlog-adp@verify-1 | 400 | 91,351 (0.914) | 77,930 (0.779) |
| backlog-adp@verify-2 | 400 | 91,351 (0.914) | 77,930 (0.779) |
| backlog-adp@verify-3 | 400 | 91,351 (0.914) | 77,930 (0.779) |
| backlog-adp@verify-4 | 400 | 91,351 (0.914) | 77,930 (0.779) |
| backlog-adp@verify-5 | 400 | 91,351 (0.914) | 77,930 (0.779) |
| backlog-adp@verify-6 | 400 | 90,999 (0.910) | 77,930 (0.779) |
| backlog-adp@verify-7 | 400 | 90,999 (0.910) | 77,930 (0.779) |
| backlog-adp@blank-aged2-0 | 340 | 86,881 (0.869) | 76,138 (0.761) |
| backlog-adp@blank-aged2-1 | 339 | 88,149 (0.881) | 75,706 (0.757) |
| backlog-adp@blank-aged2-2 | 340 | 88,388 (0.884) | 75,758 (0.758) |
| backlog-adp@blank-aged2-3 | 340 | 88,322 (0.883) | 75,758 (0.758) |
| backlog-adp@blank-aged2-4 | 340 | 88,430 (0.884) | 75,758 (0.758) |
| backlog-adp@blank-aged2-5 | 341 | 89,951 (0.900) | 75,768 (0.758) |
| backlog-adp@blank-aged2-6 | 340 | 86,549 (0.865) | 75,806 (0.758) |
| backlog-adp@blank-aged2-7 | 342 | 88,269 (0.883) | 75,824 (0.758) |
| backlog-adp@blank-aged1-0 | 341 | 89,988 (0.900) | 76,207 (0.762) |
| backlog-adp@blank-aged1-1 | 340 | 90,072 (0.901) | 76,138 (0.761) |
| backlog-adp@blank-aged1-2 | 339 | 91,517 (0.915) | 76,254 (0.763) |
| backlog-adp@blank-aged1-3 | 339 | 88,615 (0.886) | 76,156 (0.762) |
| backlog-adp@blank-aged1-4 | 339 | 88,601 (0.886) | 76,156 (0.762) |
| backlog-adp@blank-aged1-5 | 339 | 88,536 (0.885) | 76,156 (0.762) |
| backlog-adp@blank-aged1-6 | 339 | 88,738 (0.887) | 76,207 (0.762) |
| backlog-adp@blank-aged1-7 | 339 | 89,098 (0.891) | 76,207 (0.762) |
| backlog-adp@program-aged2-0 | 371 | 93,125 (0.931) | 78,620 (0.786) |
| backlog-adp@program-aged2-1 | 369 | 90,638 (0.906) | 78,263 (0.783) |
| backlog-adp@program-aged2-2 | 369 | 90,678 (0.907) | 78,405 (0.784) |
| backlog-adp@program-aged2-3 | 369 | 90,762 (0.908) | 78,405 (0.784) |
| backlog-adp@program-aged2-4 | 369 | 90,734 (0.907) | 78,234 (0.782) |
| backlog-adp@program-aged2-5 | 369 | 90,764 (0.908) | 78,479 (0.785) |
| backlog-adp@program-aged2-6 | 369 | 90,859 (0.909) | 78,503 (0.785) |
| backlog-adp@program-aged2-7 | 369 | 90,948 (0.909) | 78,332 (0.783) |
| backlog-adp@program-aged1-0 | 369 | 92,543 (0.925) | 78,569 (0.786) |
| backlog-adp@program-aged1-1 | 368 | 91,357 (0.914) | 78,551 (0.786) |
| backlog-adp@program-aged1-2 | 368 | 92,990 (0.930) | 78,569 (0.786) |
| backlog-adp@program-aged1-3 | 369 | 100,758 (1.008) | 78,645 (0.786) |
| backlog-adp@program-aged1-4 | 368 | 92,593 (0.926) | 78,569 (0.786) |
| backlog-adp@program-aged1-5 | 368 | 92,557 (0.926) | 78,569 (0.786) |
| backlog-adp@program-aged1-6 | 368 | 92,543 (0.925) | 78,569 (0.786) |
| backlog-adp@program-aged1-7 | 368 | 92,565 (0.926) | 78,620 (0.786) |
| backlog-adp@verify-aged2-0 | 399 | 91,130 (0.911) | 77,930 (0.779) |
| backlog-adp@verify-aged2-1 | 398 | 90,446 (0.904) | 77,930 (0.779) |
| backlog-adp@verify-aged2-2 | 399 | 90,446 (0.904) | 77,930 (0.779) |
| backlog-adp@verify-aged2-3 | 399 | 90,446 (0.904) | 77,930 (0.779) |
| backlog-adp@verify-aged2-4 | 399 | 90,446 (0.904) | 77,930 (0.779) |
| backlog-adp@verify-aged2-5 | 400 | 91,041 (0.910) | 77,930 (0.779) |
| backlog-adp@verify-aged2-6 | 399 | 90,446 (0.904) | 77,930 (0.779) |
| backlog-adp@verify-aged2-7 | 401 | 90,446 (0.904) | 77,930 (0.779) |
| backlog-adp@verify-aged1-0 | 400 | 90,919 (0.909) | 77,930 (0.779) |
| backlog-adp@verify-aged1-1 | 399 | 91,213 (0.912) | 77,930 (0.779) |
| backlog-adp@verify-aged1-2 | 398 | 90,446 (0.904) | 77,930 (0.779) |
| backlog-adp@verify-aged1-3 | 398 | 90,446 (0.904) | 77,930 (0.779) |
| backlog-adp@verify-aged1-4 | 398 | 90,446 (0.904) | 77,930 (0.779) |
| backlog-adp@verify-aged1-5 | 398 | 90,446 (0.904) | 77,930 (0.779) |
| backlog-adp@verify-aged1-6 | 398 | 90,446 (0.904) | 77,930 (0.779) |
| backlog-adp@verify-aged1-7 | 398 | 90,446 (0.904) | 77,930 (0.779) |
| save-held | 816 | 90,201 (0.902) | 78,024 (0.780) |
| save-starved | 418 | 80,757 (0.808) | 78,405 (0.784) |
| srp-bound | 582 | 98,272 (0.983) | 78,240 (0.782) |
| acmp-noresp | 709 | 94,641 (0.946) | 78,327 (0.783) |
| save | 680 | 90,039 (0.900) | 77,708 (0.777) |
| srp-register-burst | 496 | 98,086 (0.981) | 78,221 (0.782) |
| adp-link | 355 | 18,532 (0.185) | 2,258 (0.023) |
| adp-gm | 355 | 18,532 (0.185) | 2,258 (0.023) |
| adp-discover | 355 | 18,532 (0.185) | 2,258 (0.023) |
| control | 355 | 18,532 (0.185) | 2,258 (0.023) |
| srp | 271 | 18,532 (0.185) | 2,258 (0.023) |
| backlog | 265 | 18,532 (0.185) | 2,258 (0.023) |
| backlog-adp | 271 | 18,532 (0.185) | 2,258 (0.023) |
| backlog-adp-refill | 274 | 18,532 (0.185) | 2,258 (0.023) |
| backlog-owed | 276 | 18,532 (0.185) | 2,258 (0.023) |
| acmp-disc | 399 | 94,649 (0.946) | 78,327 (0.783) |
| maap | 165 | 18,532 (0.185) | 2,258 (0.023) |
| aecp-fanout | 80 | 18,325 (0.183) | 2,258 (0.023) |
| acmp-cmd | 65 | 18,325 (0.183) | 2,258 (0.023) |
| aecp | 79 | 18,325 (0.183) | 2,258 (0.023) |
| srp-register | 138 | 20,355 (0.204) | 2,258 (0.023) |
| aecp-largest-notice | 78 | 18,325 (0.183) | 2,258 (0.023) |
| aecp-held | 98 | 18,325 (0.183) | 2,258 (0.023) |
| datapath-events | 69 | 18,325 (0.183) | 2,258 (0.023) |
| fixture | 54 | 13,051 (0.131) | 2,258 (0.023) |

Longest pass that carries a step: 100,758 CPU cycles (1.008 ms), backlog-adp@program-aged1-3; longest step: 78,645 (0.786 ms), backlog-adp@program-1.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| Talker Advertise RX for every input, no binding (kept) | `srp.kept_advertise.if0` | 44,348 | 0.443 | 20 | 20 | fits | 44,414 | 25 | 0.859 |
| Talker RX at the bound after a freed block (count) | `srp.kept_recount.if0` | 41,398 | 0.414 | 20 | 20 | fits | 41,464 | 25 | 0.857 |
| Talker Failed RX for every input, no binding (kept) | `srp.kept_failed.if0` | 45,210 | 0.452 | 20 | 20 | fits | 45,276 | 23 | 0.869 |
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 150,168 | 1.502 | 20 | 200 | fits | 71,844 | 203 | 0.297 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 225,242 | 2.252 | 20 | 20 | fits | 91,602 | 108 | 0.664 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 250,917 | 2.509 | 20 | 24 | fits | 43,889 | 35 | 0.500 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 203,667 | 2.037 | 20 | 50 | fits | 91,566 | 202 | 0.359 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 763,147 | 7.631 | 20 | 20 | fits | 41,057 | 34 | 0.766 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 50,138 | 0.501 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-burst.held.adp.if0` | 153,908 | 1.539 | 20 | 200 | fits | 154,717 | 255 | 0.441 |
| ACMP record, every channel at its refill rate, the longest | `save-burst.held.acmp.if0` | 181,390 | 1.814 | 20 | 20 | fits | 102,435 | 115 | 0.282 |
| AECP record, every channel at its refill rate, the longest | `save-burst.held.aecp.if0` | 169,788 | 1.698 | 20 | 24 | fits | 88,257 | 70 | 0.747 |
| MAAP record, every channel at its refill rate, the longest | `save-burst.held.maap.if0` | 184,683 | 1.847 | 20 | 50 | fits | 90,518 | 104 | 0.690 |
| SRP record, every channel at its refill rate, the longest | `save-burst.held.srp.if0` | 696,590 | 6.966 | 20 | 20 | fits | 89,263 | 84 | 0.705 |
| an MRPDU its periodic timer owes, the longest | `save-burst.mrpdu.periodic.if0` | 156,364 | 1.564 | 49 | 49 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 8,336 | 0.083 | 20 | 20 | fits | 27,552 | 19 (14) | 0.880 |
| LINK_UP | `adp.link_up.if0` | 3,264 | 0.033 | 20 | 200 | fits | 23,744 | 44 (12) | 0.716 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,547 | 0.085 | 20 | 200 | fits | 17,160 | 23 (39) | 0.628 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 12,545 | 0.125 | 20 | 200 | fits | 2,416 | 10 (11) | 0.429 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 374,135 | 3.741 | 20 | 20 | fits | 90,772 | 133 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 353,141 | 3.531 | 20 | 200 | fits | 144,365 | 260 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 453,340 | 4.533 | 20 | 200 | fits | 90,772 | 133 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 354,065 | 3.541 | 20 | 20 | fits | 144,365 | 260 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 454,044 | 4.540 | 20 | 20 | fits | 90,772 | 133 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 213,340 | 2.133 | 20 | 24 | fits | 137,696 | 161 | 0.292 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 356,715 | 3.567 | 20 | 24 | fits | 144,365 | 260 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 356,649 | 3.566 | 20 | 50 | fits | 144,365 | 260 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 457,068 | 4.571 | 20 | 50 | fits | 90,772 | 133 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 539,306 | 5.393 | 20 | 20 | fits | 82,304 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 934,313 | 9.343 | 20 | 20 | fits | 52,184 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 361,635 | 3.616 | 20 | 20 | fits | 90,772 | 133 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 340,641 | 3.406 | 20 | 200 | fits | 144,365 | 260 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 440,840 | 4.408 | 20 | 200 | fits | 90,772 | 133 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 341,565 | 3.416 | 20 | 20 | fits | 144,365 | 260 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 441,544 | 4.415 | 20 | 20 | fits | 90,772 | 133 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 200,840 | 2.008 | 20 | 24 | fits | 137,696 | 161 | 0.292 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 344,215 | 3.442 | 20 | 24 | fits | 144,365 | 260 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 344,149 | 3.441 | 20 | 50 | fits | 144,365 | 260 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 444,568 | 4.446 | 20 | 50 | fits | 90,772 | 133 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 526,806 | 5.268 | 20 | 20 | fits | 82,304 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 921,813 | 9.218 | 20 | 20 | fits | 52,184 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 349,135 | 3.491 | 20 | 20 | fits | 90,772 | 133 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 328,141 | 3.281 | 20 | 200 | fits | 144,365 | 260 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 428,340 | 4.283 | 20 | 200 | fits | 90,772 | 133 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 329,065 | 3.291 | 20 | 20 | fits | 144,365 | 260 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 429,044 | 4.290 | 20 | 20 | fits | 90,772 | 133 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 188,340 | 1.883 | 20 | 24 | fits | 137,696 | 161 | 0.292 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 331,715 | 3.317 | 20 | 24 | fits | 144,365 | 260 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 331,649 | 3.316 | 20 | 50 | fits | 144,365 | 260 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 432,068 | 4.321 | 20 | 50 | fits | 90,772 | 133 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 514,306 | 5.143 | 20 | 20 | fits | 82,304 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 909,313 | 9.093 | 20 | 20 | fits | 52,184 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 336,635 | 3.366 | 20 | 20 | fits | 90,772 | 133 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 315,641 | 3.156 | 20 | 200 | fits | 144,365 | 260 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 415,840 | 4.158 | 20 | 200 | fits | 90,772 | 133 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 316,565 | 3.166 | 20 | 20 | fits | 144,365 | 260 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 416,544 | 4.165 | 20 | 20 | fits | 90,772 | 133 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 175,840 | 1.758 | 20 | 24 | fits | 137,696 | 161 | 0.292 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 319,215 | 3.192 | 20 | 24 | fits | 144,365 | 260 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 319,149 | 3.191 | 20 | 50 | fits | 144,365 | 260 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 419,568 | 4.196 | 20 | 50 | fits | 90,772 | 133 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 501,806 | 5.018 | 20 | 20 | fits | 82,304 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 896,813 | 8.968 | 20 | 20 | fits | 52,184 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 324,135 | 3.241 | 20 | 20 | fits | 90,772 | 133 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 303,141 | 3.031 | 20 | 200 | fits | 144,365 | 260 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 403,340 | 4.033 | 20 | 200 | fits | 90,772 | 133 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 304,065 | 3.041 | 20 | 20 | fits | 144,365 | 260 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 404,044 | 4.040 | 20 | 20 | fits | 90,772 | 133 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 163,340 | 1.633 | 20 | 24 | fits | 137,696 | 161 | 0.292 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 306,715 | 3.067 | 20 | 24 | fits | 144,365 | 260 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 306,649 | 3.066 | 20 | 50 | fits | 144,365 | 260 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 407,068 | 4.071 | 20 | 50 | fits | 90,772 | 133 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 489,306 | 4.893 | 20 | 20 | fits | 82,304 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 884,313 | 8.843 | 20 | 20 | fits | 52,184 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 311,635 | 3.116 | 20 | 20 | fits | 90,772 | 133 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 290,641 | 2.906 | 20 | 200 | fits | 144,365 | 260 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 390,840 | 3.908 | 20 | 200 | fits | 90,772 | 133 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 291,565 | 2.916 | 20 | 20 | fits | 144,365 | 260 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 391,544 | 3.915 | 20 | 20 | fits | 90,772 | 133 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 150,840 | 1.508 | 20 | 24 | fits | 137,696 | 161 | 0.292 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 294,215 | 2.942 | 20 | 24 | fits | 144,365 | 260 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 294,149 | 2.941 | 20 | 50 | fits | 144,365 | 260 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 394,568 | 3.946 | 20 | 50 | fits | 90,772 | 133 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 476,806 | 4.768 | 20 | 20 | fits | 82,304 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 871,813 | 8.718 | 20 | 20 | fits | 52,184 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 299,135 | 2.991 | 20 | 20 | fits | 90,772 | 133 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 278,141 | 2.781 | 20 | 200 | fits | 144,365 | 260 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 378,340 | 3.783 | 20 | 200 | fits | 90,772 | 133 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 279,065 | 2.791 | 20 | 20 | fits | 144,365 | 260 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 379,044 | 3.790 | 20 | 20 | fits | 90,772 | 133 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 138,340 | 1.383 | 20 | 24 | fits | 137,696 | 161 | 0.292 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 281,715 | 2.817 | 20 | 24 | fits | 144,365 | 260 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 281,649 | 2.816 | 20 | 50 | fits | 144,365 | 260 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 382,068 | 3.821 | 20 | 50 | fits | 90,772 | 133 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 464,306 | 4.643 | 20 | 20 | fits | 82,304 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 859,313 | 8.593 | 20 | 20 | fits | 52,184 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 404,293 | 4.043 | 20 | 20 | fits | 90,809 | 136 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 359,674 | 3.597 | 20 | 200 | fits | 143,003 | 255 | 0.406 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 449,867 | 4.499 | 20 | 200 | fits | 90,809 | 136 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 360,598 | 3.606 | 20 | 20 | fits | 143,003 | 255 | 0.406 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 450,571 | 4.506 | 20 | 20 | fits | 90,809 | 136 | 0.430 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 212,216 | 2.122 | 20 | 24 | fits | 137,817 | 162 | 0.292 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 363,248 | 3.632 | 20 | 24 | fits | 143,003 | 255 | 0.406 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 363,182 | 3.632 | 20 | 50 | fits | 143,003 | 255 | 0.406 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 453,595 | 4.536 | 20 | 50 | fits | 90,809 | 136 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 535,711 | 5.357 | 20 | 20 | fits | 82,182 | 73 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 930,876 | 9.309 | 20 | 20 | fits | 52,198 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 311,360 | 3.114 | 20 | 20 | fits | 79,804 | 118 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 302,961 | 3.030 | 20 | 200 | fits | 146,306 | 266 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 382,149 | 3.821 | 20 | 200 | fits | 79,804 | 118 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 303,885 | 3.039 | 20 | 20 | fits | 146,306 | 266 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 382,853 | 3.829 | 20 | 20 | fits | 79,804 | 118 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 152,265 | 1.523 | 20 | 24 | fits | 138,723 | 162 | 0.297 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 306,535 | 3.065 | 20 | 24 | fits | 146,306 | 266 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 306,469 | 3.065 | 20 | 50 | fits | 146,306 | 266 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 385,877 | 3.859 | 20 | 50 | fits | 79,804 | 118 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 468,146 | 4.681 | 20 | 20 | fits | 82,335 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 867,901 | 8.679 | 20 | 20 | fits | 63,610 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 326,495 | 3.265 | 20 | 20 | fits | 79,313 | 118 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 293,795 | 2.938 | 20 | 200 | fits | 146,301 | 266 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 372,492 | 3.725 | 20 | 200 | fits | 79,313 | 118 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 294,719 | 2.947 | 20 | 20 | fits | 146,301 | 266 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 373,196 | 3.732 | 20 | 20 | fits | 79,313 | 118 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 143,021 | 1.430 | 20 | 24 | fits | 138,134 | 162 | 0.298 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 297,369 | 2.974 | 20 | 24 | fits | 146,301 | 266 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 297,303 | 2.973 | 20 | 50 | fits | 146,301 | 266 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 376,220 | 3.762 | 20 | 50 | fits | 79,313 | 118 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 458,549 | 4.585 | 20 | 20 | fits | 82,395 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 858,276 | 8.583 | 20 | 20 | fits | 63,624 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 393,715 | 3.937 | 20 | 20 | fits | 80,517 | 121 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 358,059 | 3.581 | 20 | 200 | fits | 145,025 | 262 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 437,960 | 4.380 | 20 | 200 | fits | 80,517 | 121 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 358,983 | 3.590 | 20 | 20 | fits | 145,025 | 262 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 438,664 | 4.387 | 20 | 20 | fits | 80,517 | 121 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 208,644 | 2.086 | 20 | 24 | fits | 138,740 | 162 | 0.297 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 361,633 | 3.616 | 20 | 24 | fits | 145,025 | 262 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 361,567 | 3.616 | 20 | 50 | fits | 145,025 | 262 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 441,688 | 4.417 | 20 | 50 | fits | 80,517 | 121 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 524,013 | 5.240 | 20 | 20 | fits | 82,391 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 923,872 | 9.239 | 20 | 20 | fits | 63,610 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 368,715 | 3.687 | 20 | 20 | fits | 80,517 | 121 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 333,059 | 3.331 | 20 | 200 | fits | 145,025 | 262 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 412,960 | 4.130 | 20 | 200 | fits | 80,517 | 121 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 333,983 | 3.340 | 20 | 20 | fits | 145,025 | 262 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 413,664 | 4.137 | 20 | 20 | fits | 80,517 | 121 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 183,644 | 1.836 | 20 | 24 | fits | 138,740 | 162 | 0.297 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 336,633 | 3.366 | 20 | 24 | fits | 145,025 | 262 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 336,567 | 3.366 | 20 | 50 | fits | 145,025 | 262 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 416,688 | 4.167 | 20 | 50 | fits | 80,517 | 121 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 499,013 | 4.990 | 20 | 20 | fits | 82,391 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 898,872 | 8.989 | 20 | 20 | fits | 63,610 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 322,351 | 3.224 | 20 | 20 | fits | 80,510 | 121 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 286,637 | 2.866 | 20 | 200 | fits | 144,788 | 262 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 366,531 | 3.665 | 20 | 200 | fits | 80,510 | 121 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 287,561 | 2.876 | 20 | 20 | fits | 144,788 | 262 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 367,235 | 3.672 | 20 | 20 | fits | 80,510 | 121 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 137,595 | 1.376 | 20 | 24 | fits | 139,564 | 162 | 0.294 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 290,211 | 2.902 | 20 | 24 | fits | 144,788 | 262 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 290,145 | 2.901 | 20 | 50 | fits | 144,788 | 262 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 370,259 | 3.703 | 20 | 50 | fits | 80,510 | 121 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 452,585 | 4.526 | 20 | 20 | fits | 82,392 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 852,449 | 8.524 | 20 | 20 | fits | 63,611 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 310,768 | 3.108 | 20 | 20 | fits | 81,317 | 106 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 295,996 | 2.960 | 20 | 200 | fits | 144,095 | 276 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 376,697 | 3.767 | 20 | 200 | fits | 81,317 | 106 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 296,920 | 2.969 | 20 | 20 | fits | 144,095 | 276 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 377,401 | 3.774 | 20 | 20 | fits | 81,317 | 106 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 156,465 | 1.565 | 20 | 24 | fits | 138,268 | 162 | 0.295 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 299,570 | 2.996 | 20 | 24 | fits | 144,095 | 276 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 299,504 | 2.995 | 20 | 50 | fits | 144,095 | 276 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 380,425 | 3.804 | 20 | 50 | fits | 81,317 | 106 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 462,675 | 4.627 | 20 | 20 | fits | 82,316 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 878,967 | 8.790 | 20 | 20 | fits | 68,835 | 67 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 297,519 | 2.975 | 20 | 20 | fits | 81,741 | 106 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 289,655 | 2.897 | 20 | 200 | fits | 143,973 | 276 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 370,780 | 3.708 | 20 | 200 | fits | 81,741 | 106 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 290,579 | 2.906 | 20 | 20 | fits | 143,973 | 276 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 371,484 | 3.715 | 20 | 20 | fits | 81,741 | 106 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 150,246 | 1.502 | 20 | 24 | fits | 138,127 | 161 | 0.300 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 293,229 | 2.932 | 20 | 24 | fits | 143,973 | 276 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 293,163 | 2.932 | 20 | 50 | fits | 143,973 | 276 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 374,508 | 3.745 | 20 | 50 | fits | 81,741 | 106 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 456,629 | 4.566 | 20 | 20 | fits | 82,187 | 73 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 872,816 | 8.728 | 20 | 20 | fits | 68,934 | 67 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 364,360 | 3.644 | 20 | 20 | fits | 79,882 | 118 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 356,045 | 3.560 | 20 | 200 | fits | 144,510 | 261 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 435,311 | 4.353 | 20 | 200 | fits | 79,882 | 118 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 356,969 | 3.570 | 20 | 20 | fits | 144,510 | 261 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 436,015 | 4.360 | 20 | 20 | fits | 79,882 | 118 | 0.446 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 216,099 | 2.161 | 20 | 24 | fits | 138,745 | 161 | 0.302 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 359,619 | 3.596 | 20 | 24 | fits | 144,510 | 261 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 359,553 | 3.596 | 20 | 50 | fits | 144,510 | 261 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 439,039 | 4.390 | 20 | 50 | fits | 79,882 | 118 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 525,117 | 5.251 | 20 | 20 | fits | 86,144 | 79 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 937,426 | 9.374 | 20 | 20 | fits | 64,168 | 60 | 0.694 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 361,645 | 3.616 | 20 | 20 | fits | 89,229 | 133 | 0.435 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 351,827 | 3.518 | 20 | 200 | fits | 144,774 | 259 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 440,440 | 4.404 | 20 | 200 | fits | 89,229 | 133 | 0.435 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 352,751 | 3.528 | 20 | 20 | fits | 144,774 | 259 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 441,144 | 4.411 | 20 | 20 | fits | 89,229 | 133 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 202,734 | 2.027 | 20 | 24 | fits | 138,328 | 162 | 0.298 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 355,401 | 3.554 | 20 | 24 | fits | 144,774 | 259 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 355,335 | 3.553 | 20 | 50 | fits | 144,774 | 259 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 444,168 | 4.442 | 20 | 50 | fits | 89,229 | 133 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 526,320 | 5.263 | 20 | 20 | fits | 82,218 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 921,359 | 9.214 | 20 | 20 | fits | 52,184 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 349,145 | 3.491 | 20 | 20 | fits | 89,229 | 133 | 0.435 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 339,327 | 3.393 | 20 | 200 | fits | 144,774 | 259 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 427,940 | 4.279 | 20 | 200 | fits | 89,229 | 133 | 0.435 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 340,251 | 3.403 | 20 | 20 | fits | 144,774 | 259 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 428,644 | 4.286 | 20 | 20 | fits | 89,229 | 133 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 190,234 | 1.902 | 20 | 24 | fits | 138,328 | 162 | 0.298 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 342,901 | 3.429 | 20 | 24 | fits | 144,774 | 259 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 342,835 | 3.428 | 20 | 50 | fits | 144,774 | 259 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 431,668 | 4.317 | 20 | 50 | fits | 89,229 | 133 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 513,820 | 5.138 | 20 | 20 | fits | 82,218 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 908,859 | 9.089 | 20 | 20 | fits | 52,184 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 336,645 | 3.366 | 20 | 20 | fits | 89,229 | 133 | 0.435 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 326,827 | 3.268 | 20 | 200 | fits | 144,774 | 259 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 415,440 | 4.154 | 20 | 200 | fits | 89,229 | 133 | 0.435 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 327,751 | 3.278 | 20 | 20 | fits | 144,774 | 259 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 416,144 | 4.161 | 20 | 20 | fits | 89,229 | 133 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 177,734 | 1.777 | 20 | 24 | fits | 138,328 | 162 | 0.298 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 330,401 | 3.304 | 20 | 24 | fits | 144,774 | 259 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 330,335 | 3.303 | 20 | 50 | fits | 144,774 | 259 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 419,168 | 4.192 | 20 | 50 | fits | 89,229 | 133 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 501,320 | 5.013 | 20 | 20 | fits | 82,218 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 896,359 | 8.964 | 20 | 20 | fits | 52,184 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 324,145 | 3.241 | 20 | 20 | fits | 89,229 | 133 | 0.435 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 314,327 | 3.143 | 20 | 200 | fits | 144,774 | 259 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 402,940 | 4.029 | 20 | 200 | fits | 89,229 | 133 | 0.435 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 315,251 | 3.153 | 20 | 20 | fits | 144,774 | 259 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 403,644 | 4.036 | 20 | 20 | fits | 89,229 | 133 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 165,234 | 1.652 | 20 | 24 | fits | 138,328 | 162 | 0.298 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 317,901 | 3.179 | 20 | 24 | fits | 144,774 | 259 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 317,835 | 3.178 | 20 | 50 | fits | 144,774 | 259 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 406,668 | 4.067 | 20 | 50 | fits | 89,229 | 133 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 488,820 | 4.888 | 20 | 20 | fits | 82,218 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 883,859 | 8.839 | 20 | 20 | fits | 52,184 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 311,645 | 3.116 | 20 | 20 | fits | 89,229 | 133 | 0.435 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 301,827 | 3.018 | 20 | 200 | fits | 144,774 | 259 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 390,440 | 3.904 | 20 | 200 | fits | 89,229 | 133 | 0.435 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 302,751 | 3.028 | 20 | 20 | fits | 144,774 | 259 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 391,144 | 3.911 | 20 | 20 | fits | 89,229 | 133 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 152,734 | 1.527 | 20 | 24 | fits | 138,328 | 162 | 0.298 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 305,401 | 3.054 | 20 | 24 | fits | 144,774 | 259 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 305,335 | 3.053 | 20 | 50 | fits | 144,774 | 259 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 394,168 | 3.942 | 20 | 50 | fits | 89,229 | 133 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 476,320 | 4.763 | 20 | 20 | fits | 82,218 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 871,359 | 8.714 | 20 | 20 | fits | 52,184 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 299,145 | 2.991 | 20 | 20 | fits | 89,229 | 133 | 0.435 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 289,327 | 2.893 | 20 | 200 | fits | 144,774 | 259 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 377,940 | 3.779 | 20 | 200 | fits | 89,229 | 133 | 0.435 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 290,251 | 2.903 | 20 | 20 | fits | 144,774 | 259 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 378,644 | 3.786 | 20 | 20 | fits | 89,229 | 133 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 140,234 | 1.402 | 20 | 24 | fits | 138,328 | 162 | 0.298 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 292,901 | 2.929 | 20 | 24 | fits | 144,774 | 259 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 292,835 | 2.928 | 20 | 50 | fits | 144,774 | 259 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 381,668 | 3.817 | 20 | 50 | fits | 89,229 | 133 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 463,820 | 4.638 | 20 | 20 | fits | 82,218 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 858,859 | 8.589 | 20 | 20 | fits | 52,184 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 399,415 | 3.994 | 20 | 20 | fits | 89,243 | 133 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 364,311 | 3.643 | 20 | 200 | fits | 144,768 | 259 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 452,938 | 4.529 | 20 | 200 | fits | 89,243 | 133 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 365,235 | 3.652 | 20 | 20 | fits | 144,768 | 259 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 453,642 | 4.536 | 20 | 20 | fits | 89,243 | 133 | 0.432 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 215,174 | 2.152 | 20 | 24 | fits | 138,168 | 162 | 0.298 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 367,885 | 3.679 | 20 | 24 | fits | 144,768 | 259 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 367,819 | 3.678 | 20 | 50 | fits | 144,768 | 259 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 456,666 | 4.567 | 20 | 50 | fits | 89,243 | 133 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 538,842 | 5.388 | 20 | 20 | fits | 82,242 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 933,848 | 9.338 | 20 | 20 | fits | 52,198 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 386,915 | 3.869 | 20 | 20 | fits | 89,243 | 133 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 351,811 | 3.518 | 20 | 200 | fits | 144,768 | 259 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 440,438 | 4.404 | 20 | 200 | fits | 89,243 | 133 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 352,735 | 3.527 | 20 | 20 | fits | 144,768 | 259 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 441,142 | 4.411 | 20 | 20 | fits | 89,243 | 133 | 0.432 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 202,674 | 2.027 | 20 | 24 | fits | 138,168 | 162 | 0.298 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 355,385 | 3.554 | 20 | 24 | fits | 144,768 | 259 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 355,319 | 3.553 | 20 | 50 | fits | 144,768 | 259 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 444,166 | 4.442 | 20 | 50 | fits | 89,243 | 133 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 526,342 | 5.263 | 20 | 20 | fits | 82,242 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 921,348 | 9.213 | 20 | 20 | fits | 52,198 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 315,711 | 3.157 | 20 | 20 | fits | 85,767 | 115 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 283,228 | 2.832 | 20 | 200 | fits | 144,125 | 277 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 368,379 | 3.684 | 20 | 200 | fits | 85,767 | 115 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 284,152 | 2.842 | 20 | 20 | fits | 144,125 | 277 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 369,083 | 3.691 | 20 | 20 | fits | 85,767 | 115 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 135,162 | 1.352 | 20 | 24 | fits | 137,205 | 162 | 0.282 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 286,802 | 2.868 | 20 | 24 | fits | 144,125 | 277 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 286,736 | 2.867 | 20 | 50 | fits | 144,125 | 277 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 372,107 | 3.721 | 20 | 50 | fits | 85,767 | 115 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 454,214 | 4.542 | 20 | 20 | fits | 82,173 | 73 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 849,348 | 8.493 | 20 | 20 | fits | 52,338 | 48 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 288,187 | 2.882 | 20 | 20 | fits | 81,741 | 106 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 280,323 | 2.803 | 20 | 200 | fits | 144,001 | 276 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 361,448 | 3.614 | 20 | 200 | fits | 81,741 | 106 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 281,247 | 2.812 | 20 | 20 | fits | 144,001 | 276 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 362,152 | 3.622 | 20 | 20 | fits | 81,741 | 106 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 140,886 | 1.409 | 20 | 24 | fits | 137,076 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 283,897 | 2.839 | 20 | 24 | fits | 144,001 | 276 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 283,831 | 2.838 | 20 | 50 | fits | 144,001 | 276 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 365,176 | 3.652 | 20 | 50 | fits | 81,741 | 106 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 447,247 | 4.472 | 20 | 20 | fits | 82,137 | 73 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 859,644 | 8.596 | 20 | 20 | fits | 58,104 | 54 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 290,939 | 2.909 | 20 | 20 | fits | 79,823 | 118 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 282,712 | 2.827 | 20 | 200 | fits | 144,670 | 261 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 361,919 | 3.619 | 20 | 200 | fits | 79,823 | 118 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 283,636 | 2.836 | 20 | 20 | fits | 144,670 | 261 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 362,623 | 3.626 | 20 | 20 | fits | 79,823 | 118 | 0.446 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 142,606 | 1.426 | 20 | 24 | fits | 137,076 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 286,286 | 2.863 | 20 | 24 | fits | 144,670 | 261 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 286,220 | 2.862 | 20 | 50 | fits | 144,670 | 261 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 365,647 | 3.656 | 20 | 50 | fits | 79,823 | 118 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 447,670 | 4.477 | 20 | 20 | fits | 82,089 | 73 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 941,528 | 9.415 | 20 | 20 | fits | 75,725 | 74 | 0.674 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 317,153 | 3.172 | 20 | 20 | fits | 79,288 | 118 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 284,413 | 2.844 | 20 | 200 | fits | 144,651 | 261 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 363,085 | 3.631 | 20 | 200 | fits | 79,288 | 118 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 285,337 | 2.853 | 20 | 20 | fits | 144,651 | 261 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 363,789 | 3.638 | 20 | 20 | fits | 79,288 | 118 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 144,326 | 1.443 | 20 | 24 | fits | 137,076 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 287,987 | 2.880 | 20 | 24 | fits | 144,651 | 261 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 287,921 | 2.879 | 20 | 50 | fits | 144,651 | 261 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 366,813 | 3.668 | 20 | 50 | fits | 79,288 | 118 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 448,946 | 4.489 | 20 | 20 | fits | 82,199 | 73 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 942,817 | 9.428 | 20 | 20 | fits | 75,104 | 73 | 0.664 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 309,858 | 3.099 | 20 | 20 | fits | 87,950 | 161 | 0.434 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 268,955 | 2.690 | 20 | 200 | fits | 145,519 | 266 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 356,289 | 3.563 | 20 | 200 | fits | 87,950 | 161 | 0.434 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 269,879 | 2.699 | 20 | 20 | fits | 145,519 | 266 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 356,993 | 3.570 | 20 | 20 | fits | 87,950 | 161 | 0.434 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 128,000 | 1.280 | 20 | 24 | fits | 130,550 | 120 | 0.296 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 272,529 | 2.725 | 20 | 24 | fits | 145,519 | 266 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 272,463 | 2.725 | 20 | 50 | fits | 145,519 | 266 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 360,017 | 3.600 | 20 | 50 | fits | 87,950 | 161 | 0.434 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 456,502 | 4.565 | 20 | 20 | fits | 86,371 | 80 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 933,143 | 9.331 | 20 | 20 | fits | 63,624 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 323,538 | 3.235 | 20 | 20 | fits | 84,427 | 127 | 0.469 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 275,450 | 2.755 | 20 | 200 | fits | 144,566 | 263 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 368,611 | 3.686 | 20 | 200 | fits | 84,427 | 127 | 0.469 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 276,374 | 2.764 | 20 | 20 | fits | 144,566 | 263 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 369,315 | 3.693 | 20 | 20 | fits | 84,427 | 127 | 0.469 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 135,448 | 1.354 | 20 | 24 | fits | 137,076 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 279,024 | 2.790 | 20 | 24 | fits | 144,566 | 263 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 278,958 | 2.790 | 20 | 50 | fits | 144,566 | 263 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 372,339 | 3.723 | 20 | 50 | fits | 84,427 | 127 | 0.469 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 458,311 | 4.583 | 20 | 20 | fits | 86,038 | 79 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 930,865 | 9.309 | 20 | 20 | fits | 52,183 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 322,136 | 3.221 | 20 | 20 | fits | 88,375 | 115 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 286,222 | 2.862 | 20 | 200 | fits | 144,350 | 277 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 373,981 | 3.740 | 20 | 200 | fits | 88,375 | 115 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 287,146 | 2.871 | 20 | 20 | fits | 144,350 | 277 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 374,685 | 3.747 | 20 | 20 | fits | 88,375 | 115 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 138,087 | 1.381 | 20 | 24 | fits | 137,197 | 162 | 0.282 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 289,796 | 2.898 | 20 | 24 | fits | 144,350 | 277 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 289,730 | 2.897 | 20 | 50 | fits | 144,350 | 277 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 377,709 | 3.777 | 20 | 50 | fits | 88,375 | 115 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 536,260 | 5.363 | 20 | 20 | fits | 82,023 | 74 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 931,503 | 9.315 | 20 | 20 | fits | 52,357 | 48 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 393,972 | 3.940 | 20 | 20 | fits | 82,935 | 109 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 286,779 | 2.868 | 20 | 200 | fits | 147,776 | 277 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 445,582 | 4.456 | 20 | 200 | fits | 82,935 | 109 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 287,703 | 2.877 | 20 | 20 | fits | 147,776 | 277 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 446,286 | 4.463 | 20 | 20 | fits | 82,935 | 109 | 0.421 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 143,567 | 1.436 | 20 | 24 | fits | 137,058 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 290,353 | 2.904 | 20 | 24 | fits | 147,776 | 277 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 290,287 | 2.903 | 20 | 50 | fits | 147,776 | 277 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 449,310 | 4.493 | 20 | 50 | fits | 82,935 | 109 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 531,600 | 5.316 | 20 | 20 | fits | 82,356 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 944,544 | 9.445 | 20 | 20 | fits | 64,195 | 60 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 298,422 | 2.984 | 20 | 20 | fits | 85,919 | 113 | 0.478 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 277,649 | 2.776 | 20 | 200 | fits | 144,169 | 277 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 372,554 | 3.726 | 20 | 200 | fits | 85,919 | 113 | 0.478 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 278,573 | 2.786 | 20 | 20 | fits | 144,169 | 277 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 373,258 | 3.733 | 20 | 20 | fits | 85,919 | 113 | 0.478 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 138,044 | 1.380 | 20 | 24 | fits | 137,147 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 281,223 | 2.812 | 20 | 24 | fits | 144,169 | 277 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 281,157 | 2.812 | 20 | 50 | fits | 144,169 | 277 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 376,282 | 3.763 | 20 | 50 | fits | 85,919 | 113 | 0.478 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 458,552 | 4.586 | 20 | 20 | fits | 82,336 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 853,673 | 8.537 | 20 | 20 | fits | 52,184 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 298,482 | 2.985 | 20 | 20 | fits | 79,968 | 118 | 0.447 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 290,194 | 2.902 | 20 | 200 | fits | 146,364 | 266 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 369,546 | 3.695 | 20 | 200 | fits | 79,968 | 118 | 0.447 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 291,118 | 2.911 | 20 | 20 | fits | 146,364 | 266 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 370,250 | 3.703 | 20 | 20 | fits | 79,968 | 118 | 0.447 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 139,903 | 1.399 | 20 | 24 | fits | 137,286 | 162 | 0.282 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 293,768 | 2.938 | 20 | 24 | fits | 146,364 | 266 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 293,702 | 2.937 | 20 | 50 | fits | 146,364 | 266 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 373,274 | 3.733 | 20 | 50 | fits | 79,968 | 118 | 0.447 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 455,381 | 4.554 | 20 | 20 | fits | 82,173 | 73 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 850,509 | 8.505 | 20 | 20 | fits | 52,183 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 286,000 | 2.860 | 20 | 20 | fits | 82,516 | 124 | 0.468 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 275,650 | 2.756 | 20 | 200 | fits | 145,563 | 266 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 357,550 | 3.575 | 20 | 200 | fits | 82,516 | 124 | 0.468 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 276,574 | 2.766 | 20 | 20 | fits | 145,563 | 266 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 358,254 | 3.583 | 20 | 20 | fits | 82,516 | 124 | 0.468 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 134,651 | 1.347 | 20 | 24 | fits | 139,939 | 166 | 0.292 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 279,224 | 2.792 | 20 | 24 | fits | 145,563 | 266 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 279,158 | 2.792 | 20 | 50 | fits | 145,563 | 266 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 361,278 | 3.613 | 20 | 50 | fits | 82,516 | 124 | 0.468 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 443,227 | 4.432 | 20 | 20 | fits | 82,015 | 73 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 846,171 | 8.462 | 20 | 20 | fits | 66,939 | 67 | 0.684 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 284,697 | 2.847 | 20 | 20 | fits | 79,765 | 118 | 0.445 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 276,470 | 2.765 | 20 | 200 | fits | 145,604 | 266 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 355,619 | 3.556 | 20 | 200 | fits | 79,765 | 118 | 0.445 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 277,394 | 2.774 | 20 | 20 | fits | 145,604 | 266 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 356,323 | 3.563 | 20 | 20 | fits | 79,765 | 118 | 0.445 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 135,430 | 1.354 | 20 | 24 | fits | 137,058 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 280,044 | 2.800 | 20 | 24 | fits | 145,604 | 266 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 279,978 | 2.800 | 20 | 50 | fits | 145,604 | 266 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 359,347 | 3.593 | 20 | 50 | fits | 79,765 | 118 | 0.445 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 441,416 | 4.414 | 20 | 20 | fits | 82,135 | 73 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 857,973 | 8.580 | 20 | 20 | fits | 75,463 | 73 | 0.668 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 310,346 | 3.103 | 20 | 20 | fits | 79,230 | 118 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 277,664 | 2.777 | 20 | 200 | fits | 144,717 | 261 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 356,278 | 3.563 | 20 | 200 | fits | 79,230 | 118 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 278,588 | 2.786 | 20 | 20 | fits | 144,717 | 261 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 356,982 | 3.570 | 20 | 20 | fits | 79,230 | 118 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 137,511 | 1.375 | 20 | 24 | fits | 137,058 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 281,238 | 2.812 | 20 | 24 | fits | 144,717 | 261 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 281,172 | 2.812 | 20 | 50 | fits | 144,717 | 261 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 360,006 | 3.600 | 20 | 50 | fits | 79,230 | 118 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 442,152 | 4.422 | 20 | 20 | fits | 82,212 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 858,850 | 8.588 | 20 | 20 | fits | 75,135 | 73 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 313,717 | 3.137 | 20 | 20 | fits | 80,234 | 121 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 278,279 | 2.783 | 20 | 200 | fits | 143,612 | 257 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 357,897 | 3.579 | 20 | 200 | fits | 80,234 | 121 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 279,203 | 2.792 | 20 | 20 | fits | 143,612 | 257 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 358,601 | 3.586 | 20 | 20 | fits | 80,234 | 121 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 139,231 | 1.392 | 20 | 24 | fits | 137,058 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 281,853 | 2.819 | 20 | 24 | fits | 143,612 | 257 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 281,787 | 2.818 | 20 | 50 | fits | 143,612 | 257 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 361,625 | 3.616 | 20 | 50 | fits | 80,234 | 121 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 447,750 | 4.478 | 20 | 20 | fits | 86,191 | 80 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 859,914 | 8.599 | 20 | 20 | fits | 63,610 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 309,762 | 3.098 | 20 | 20 | fits | 88,486 | 119 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 280,509 | 2.805 | 20 | 200 | fits | 144,122 | 276 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 368,379 | 3.684 | 20 | 200 | fits | 88,486 | 119 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 281,433 | 2.814 | 20 | 20 | fits | 144,122 | 276 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 369,083 | 3.691 | 20 | 20 | fits | 88,486 | 119 | 0.430 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 140,951 | 1.410 | 20 | 24 | fits | 137,058 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 284,083 | 2.841 | 20 | 24 | fits | 144,122 | 276 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 284,017 | 2.840 | 20 | 50 | fits | 144,122 | 276 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 372,107 | 3.721 | 20 | 50 | fits | 88,486 | 119 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 465,655 | 4.657 | 20 | 20 | fits | 83,434 | 74 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 861,064 | 8.611 | 20 | 20 | fits | 52,202 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 329,025 | 3.290 | 20 | 20 | fits | 87,208 | 115 | 0.470 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 285,974 | 2.860 | 20 | 200 | fits | 147,867 | 278 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 382,168 | 3.822 | 20 | 200 | fits | 87,208 | 115 | 0.470 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 286,898 | 2.869 | 20 | 20 | fits | 147,867 | 278 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 382,872 | 3.829 | 20 | 20 | fits | 87,208 | 115 | 0.470 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 142,671 | 1.427 | 20 | 24 | fits | 137,058 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 289,548 | 2.895 | 20 | 24 | fits | 147,867 | 278 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 289,482 | 2.895 | 20 | 50 | fits | 147,867 | 278 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 385,896 | 3.859 | 20 | 50 | fits | 87,208 | 115 | 0.470 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 467,983 | 4.680 | 20 | 20 | fits | 82,153 | 73 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 862,992 | 8.630 | 20 | 20 | fits | 52,183 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 308,961 | 3.090 | 20 | 20 | fits | 85,841 | 113 | 0.471 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 281,304 | 2.813 | 20 | 200 | fits | 144,233 | 277 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 376,131 | 3.761 | 20 | 200 | fits | 85,841 | 113 | 0.471 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 282,228 | 2.822 | 20 | 20 | fits | 144,233 | 277 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 376,835 | 3.768 | 20 | 20 | fits | 85,841 | 113 | 0.471 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 141,635 | 1.416 | 20 | 24 | fits | 137,190 | 161 | 0.282 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 284,878 | 2.849 | 20 | 24 | fits | 144,233 | 277 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 284,812 | 2.848 | 20 | 50 | fits | 144,233 | 277 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 379,859 | 3.799 | 20 | 50 | fits | 85,841 | 113 | 0.471 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 462,166 | 4.622 | 20 | 20 | fits | 82,373 | 73 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 857,106 | 8.571 | 20 | 20 | fits | 52,203 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 322,037 | 3.220 | 20 | 20 | fits | 83,200 | 109 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 291,779 | 2.918 | 20 | 200 | fits | 144,344 | 277 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 374,363 | 3.744 | 20 | 200 | fits | 83,200 | 109 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 292,703 | 2.927 | 20 | 20 | fits | 144,344 | 277 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 375,067 | 3.751 | 20 | 20 | fits | 83,200 | 109 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 143,494 | 1.435 | 20 | 24 | fits | 137,329 | 162 | 0.282 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 295,353 | 2.954 | 20 | 24 | fits | 144,344 | 277 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 295,287 | 2.953 | 20 | 50 | fits | 144,344 | 277 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 378,091 | 3.781 | 20 | 50 | fits | 83,200 | 109 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 460,333 | 4.603 | 20 | 20 | fits | 82,308 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 855,381 | 8.554 | 20 | 20 | fits | 52,184 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 306,343 | 3.063 | 20 | 20 | fits | 85,862 | 115 | 0.447 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 273,700 | 2.737 | 20 | 200 | fits | 143,552 | 277 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 358,946 | 3.589 | 20 | 200 | fits | 85,862 | 115 | 0.447 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 274,624 | 2.746 | 20 | 20 | fits | 143,552 | 277 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 359,650 | 3.596 | 20 | 20 | fits | 85,862 | 115 | 0.447 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 134,712 | 1.347 | 20 | 24 | fits | 140,000 | 166 | 0.293 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 277,274 | 2.773 | 20 | 24 | fits | 143,552 | 277 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 277,208 | 2.772 | 20 | 50 | fits | 143,552 | 277 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 362,674 | 3.627 | 20 | 50 | fits | 85,862 | 115 | 0.447 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 444,756 | 4.448 | 20 | 20 | fits | 82,148 | 73 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 941,142 | 9.411 | 20 | 20 | fits | 69,626 | 67 | 0.718 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 286,599 | 2.866 | 20 | 20 | fits | 81,810 | 106 | 0.434 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 278,735 | 2.787 | 20 | 200 | fits | 143,944 | 276 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 359,929 | 3.599 | 20 | 200 | fits | 81,810 | 106 | 0.434 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 279,659 | 2.797 | 20 | 20 | fits | 143,944 | 276 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 360,633 | 3.606 | 20 | 20 | fits | 81,810 | 106 | 0.434 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 139,355 | 1.394 | 20 | 24 | fits | 137,137 | 161 | 0.282 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 282,309 | 2.823 | 20 | 24 | fits | 143,944 | 276 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 282,243 | 2.822 | 20 | 50 | fits | 143,944 | 276 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 363,657 | 3.637 | 20 | 50 | fits | 81,810 | 106 | 0.434 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 445,777 | 4.458 | 20 | 20 | fits | 82,186 | 73 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 942,677 | 9.427 | 20 | 20 | fits | 75,544 | 73 | 0.668 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 289,351 | 2.894 | 20 | 20 | fits | 79,823 | 118 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 281,124 | 2.811 | 20 | 200 | fits | 144,613 | 261 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 360,331 | 3.603 | 20 | 200 | fits | 79,823 | 118 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 282,048 | 2.820 | 20 | 20 | fits | 144,613 | 261 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 361,035 | 3.610 | 20 | 20 | fits | 79,823 | 118 | 0.446 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 141,075 | 1.411 | 20 | 24 | fits | 137,137 | 161 | 0.282 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 284,698 | 2.847 | 20 | 24 | fits | 144,613 | 261 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 284,632 | 2.846 | 20 | 50 | fits | 144,613 | 261 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 364,059 | 3.641 | 20 | 50 | fits | 79,823 | 118 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 446,131 | 4.461 | 20 | 20 | fits | 82,138 | 73 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 945,549 | 9.455 | 20 | 20 | fits | 86,246 | 86 | 0.644 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 315,470 | 3.155 | 20 | 20 | fits | 79,193 | 118 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 282,825 | 2.828 | 20 | 200 | fits | 144,594 | 261 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 361,402 | 3.614 | 20 | 200 | fits | 79,193 | 118 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 283,749 | 2.837 | 20 | 20 | fits | 144,594 | 261 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 362,106 | 3.621 | 20 | 20 | fits | 79,193 | 118 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 142,795 | 1.428 | 20 | 24 | fits | 137,137 | 161 | 0.282 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 286,399 | 2.864 | 20 | 24 | fits | 144,594 | 261 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 286,333 | 2.863 | 20 | 50 | fits | 144,594 | 261 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 365,130 | 3.651 | 20 | 50 | fits | 79,193 | 118 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 451,345 | 4.513 | 20 | 20 | fits | 86,281 | 80 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 943,742 | 9.437 | 20 | 20 | fits | 63,624 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 327,175 | 3.272 | 20 | 20 | fits | 88,546 | 134 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 283,424 | 2.834 | 20 | 200 | fits | 143,473 | 257 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 371,354 | 3.714 | 20 | 200 | fits | 88,546 | 134 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 284,348 | 2.843 | 20 | 20 | fits | 143,473 | 257 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 372,058 | 3.721 | 20 | 20 | fits | 88,546 | 134 | 0.449 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 144,515 | 1.445 | 20 | 24 | fits | 137,137 | 161 | 0.282 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 286,998 | 2.870 | 20 | 24 | fits | 143,473 | 257 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 286,932 | 2.869 | 20 | 50 | fits | 143,473 | 257 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 375,082 | 3.751 | 20 | 50 | fits | 88,546 | 134 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 548,654 | 5.487 | 20 | 20 | fits | 83,823 | 74 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 944,174 | 9.442 | 20 | 20 | fits | 52,183 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 328,555 | 3.286 | 20 | 20 | fits | 90,193 | 133 | 0.482 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 274,642 | 2.746 | 20 | 200 | fits | 144,491 | 263 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 373,569 | 3.736 | 20 | 200 | fits | 90,193 | 133 | 0.482 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 275,566 | 2.756 | 20 | 20 | fits | 144,491 | 263 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 374,273 | 3.743 | 20 | 20 | fits | 90,193 | 133 | 0.482 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 134,715 | 1.347 | 20 | 24 | fits | 137,137 | 161 | 0.282 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 278,216 | 2.782 | 20 | 24 | fits | 144,491 | 263 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 278,150 | 2.781 | 20 | 50 | fits | 144,491 | 263 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 377,297 | 3.773 | 20 | 50 | fits | 90,193 | 133 | 0.482 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 541,323 | 5.413 | 20 | 20 | fits | 83,299 | 74 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 936,556 | 9.366 | 20 | 20 | fits | 52,184 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 298,822 | 2.988 | 20 | 20 | fits | 81,334 | 106 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 284,091 | 2.841 | 20 | 200 | fits | 143,999 | 276 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 364,809 | 3.648 | 20 | 200 | fits | 81,334 | 106 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 285,015 | 2.850 | 20 | 20 | fits | 143,999 | 276 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 365,513 | 3.655 | 20 | 20 | fits | 81,334 | 106 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 144,656 | 1.447 | 20 | 24 | fits | 137,208 | 161 | 0.282 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 287,665 | 2.877 | 20 | 24 | fits | 143,999 | 276 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 287,599 | 2.876 | 20 | 50 | fits | 143,999 | 276 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 368,537 | 3.685 | 20 | 50 | fits | 81,334 | 106 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 450,904 | 4.509 | 20 | 20 | fits | 82,433 | 74 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 863,470 | 8.635 | 20 | 20 | fits | 63,629 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 304,282 | 3.043 | 20 | 20 | fits | 83,083 | 110 | 0.417 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 273,646 | 2.736 | 20 | 200 | fits | 143,354 | 277 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 356,113 | 3.561 | 20 | 200 | fits | 83,083 | 110 | 0.417 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 274,570 | 2.746 | 20 | 20 | fits | 143,354 | 277 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 356,817 | 3.568 | 20 | 20 | fits | 83,083 | 110 | 0.417 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 134,856 | 1.349 | 20 | 24 | fits | 137,208 | 161 | 0.282 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 277,220 | 2.772 | 20 | 24 | fits | 143,354 | 277 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 277,154 | 2.772 | 20 | 50 | fits | 143,354 | 277 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 359,841 | 3.598 | 20 | 50 | fits | 83,083 | 110 | 0.417 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 456,072 | 4.561 | 20 | 20 | fits | 86,147 | 80 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 851,722 | 8.517 | 20 | 20 | fits | 52,202 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 317,694 | 3.177 | 20 | 20 | fits | 87,086 | 115 | 0.469 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 274,643 | 2.746 | 20 | 200 | fits | 143,627 | 278 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 370,715 | 3.707 | 20 | 200 | fits | 87,086 | 115 | 0.469 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 275,567 | 2.756 | 20 | 20 | fits | 143,627 | 278 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 371,419 | 3.714 | 20 | 20 | fits | 87,086 | 115 | 0.469 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 135,580 | 1.356 | 20 | 24 | fits | 137,208 | 161 | 0.282 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 278,217 | 2.782 | 20 | 24 | fits | 143,627 | 278 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 278,151 | 2.782 | 20 | 50 | fits | 143,627 | 278 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 374,443 | 3.744 | 20 | 50 | fits | 87,086 | 115 | 0.469 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 456,494 | 4.565 | 20 | 20 | fits | 82,117 | 73 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 856,152 | 8.562 | 20 | 20 | fits | 63,790 | 60 | 0.689 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 296,849 | 2.968 | 20 | 20 | fits | 79,968 | 118 | 0.447 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 288,561 | 2.886 | 20 | 200 | fits | 146,307 | 266 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 367,913 | 3.679 | 20 | 200 | fits | 79,968 | 118 | 0.447 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 289,485 | 2.895 | 20 | 20 | fits | 146,307 | 266 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 368,617 | 3.686 | 20 | 20 | fits | 79,968 | 118 | 0.447 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 138,390 | 1.384 | 20 | 24 | fits | 137,302 | 162 | 0.282 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 292,135 | 2.921 | 20 | 24 | fits | 146,307 | 266 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 292,069 | 2.921 | 20 | 50 | fits | 146,307 | 266 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 371,641 | 3.716 | 20 | 50 | fits | 79,968 | 118 | 0.447 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 453,699 | 4.537 | 20 | 20 | fits | 82,124 | 73 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 853,392 | 8.534 | 20 | 20 | fits | 63,611 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 292,402 | 2.924 | 20 | 20 | fits | 79,765 | 118 | 0.445 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 284,175 | 2.842 | 20 | 200 | fits | 144,679 | 261 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 363,324 | 3.633 | 20 | 200 | fits | 79,765 | 118 | 0.445 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 285,099 | 2.851 | 20 | 20 | fits | 144,679 | 261 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 364,028 | 3.640 | 20 | 20 | fits | 79,765 | 118 | 0.445 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 144,060 | 1.441 | 20 | 24 | fits | 137,119 | 161 | 0.282 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 287,749 | 2.877 | 20 | 24 | fits | 144,679 | 261 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 287,683 | 2.877 | 20 | 50 | fits | 144,679 | 261 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 367,052 | 3.671 | 20 | 50 | fits | 79,765 | 118 | 0.445 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 449,070 | 4.491 | 20 | 20 | fits | 82,084 | 73 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 865,184 | 8.652 | 20 | 20 | fits | 68,865 | 67 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 284,637 | 2.846 | 20 | 20 | fits | 88,057 | 160 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 268,717 | 2.687 | 20 | 200 | fits | 145,547 | 266 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 356,158 | 3.562 | 20 | 200 | fits | 88,057 | 160 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 269,641 | 2.696 | 20 | 20 | fits | 145,547 | 266 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 356,862 | 3.569 | 20 | 20 | fits | 88,057 | 160 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 127,734 | 1.277 | 20 | 24 | fits | 130,593 | 120 | 0.297 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 272,291 | 2.723 | 20 | 24 | fits | 145,547 | 266 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 272,225 | 2.722 | 20 | 50 | fits | 145,547 | 266 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 359,886 | 3.599 | 20 | 50 | fits | 88,057 | 160 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 445,651 | 4.457 | 20 | 20 | fits | 85,831 | 79 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 858,215 | 8.582 | 20 | 20 | fits | 63,694 | 60 | 0.686 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 315,657 | 3.157 | 20 | 20 | fits | 85,646 | 124 | 0.468 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 276,455 | 2.765 | 20 | 200 | fits | 145,528 | 266 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 361,485 | 3.615 | 20 | 200 | fits | 85,646 | 124 | 0.468 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 277,379 | 2.774 | 20 | 20 | fits | 145,528 | 266 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 362,189 | 3.622 | 20 | 20 | fits | 85,646 | 124 | 0.468 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 135,491 | 1.355 | 20 | 24 | fits | 137,119 | 161 | 0.282 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 280,029 | 2.800 | 20 | 24 | fits | 145,528 | 266 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 279,963 | 2.800 | 20 | 50 | fits | 145,528 | 266 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 365,213 | 3.652 | 20 | 50 | fits | 85,646 | 124 | 0.468 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 447,308 | 4.473 | 20 | 20 | fits | 82,161 | 73 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 860,137 | 8.601 | 20 | 20 | fits | 63,624 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 317,090 | 3.171 | 20 | 20 | fits | 80,312 | 121 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 281,574 | 2.816 | 20 | 200 | fits | 148,438 | 262 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 361,270 | 3.613 | 20 | 200 | fits | 80,312 | 121 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 282,498 | 2.825 | 20 | 20 | fits | 148,438 | 262 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 361,974 | 3.620 | 20 | 20 | fits | 80,312 | 121 | 0.421 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 137,700 | 1.377 | 20 | 24 | fits | 137,119 | 161 | 0.282 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 285,148 | 2.851 | 20 | 24 | fits | 148,438 | 262 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 285,082 | 2.851 | 20 | 50 | fits | 148,438 | 262 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 364,998 | 3.650 | 20 | 50 | fits | 80,312 | 121 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 450,483 | 4.505 | 20 | 20 | fits | 85,551 | 80 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 860,051 | 8.601 | 20 | 20 | fits | 63,610 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 329,504 | 3.295 | 20 | 20 | fits | 80,534 | 121 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 293,831 | 2.938 | 20 | 200 | fits | 145,113 | 262 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 373,749 | 3.737 | 20 | 200 | fits | 80,534 | 121 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 294,755 | 2.948 | 20 | 20 | fits | 145,113 | 262 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 374,453 | 3.745 | 20 | 20 | fits | 80,534 | 121 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 144,854 | 1.449 | 20 | 24 | fits | 137,214 | 162 | 0.282 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 297,405 | 2.974 | 20 | 24 | fits | 145,113 | 262 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 297,339 | 2.973 | 20 | 50 | fits | 145,113 | 262 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 377,477 | 3.775 | 20 | 50 | fits | 80,534 | 121 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 459,691 | 4.597 | 20 | 20 | fits | 82,280 | 73 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 854,900 | 8.549 | 20 | 20 | fits | 52,183 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 311,715 | 3.117 | 20 | 20 | fits | 79,135 | 118 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 279,128 | 2.791 | 20 | 200 | fits | 144,661 | 261 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 357,647 | 3.576 | 20 | 200 | fits | 79,135 | 118 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 280,052 | 2.801 | 20 | 20 | fits | 144,661 | 261 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 358,351 | 3.584 | 20 | 20 | fits | 79,135 | 118 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 139,031 | 1.390 | 20 | 24 | fits | 137,058 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 282,702 | 2.827 | 20 | 24 | fits | 144,661 | 261 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 282,636 | 2.826 | 20 | 50 | fits | 144,661 | 261 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 361,375 | 3.614 | 20 | 50 | fits | 79,135 | 118 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 443,521 | 4.435 | 20 | 20 | fits | 82,212 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 855,940 | 8.559 | 20 | 20 | fits | 58,118 | 54 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 315,165 | 3.152 | 20 | 20 | fits | 80,234 | 121 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 279,727 | 2.797 | 20 | 200 | fits | 143,540 | 257 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 359,345 | 3.593 | 20 | 200 | fits | 80,234 | 121 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 280,651 | 2.807 | 20 | 20 | fits | 143,540 | 257 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 360,049 | 3.600 | 20 | 20 | fits | 80,234 | 121 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 140,751 | 1.408 | 20 | 24 | fits | 137,058 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 283,301 | 2.833 | 20 | 24 | fits | 143,540 | 257 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 283,235 | 2.832 | 20 | 50 | fits | 143,540 | 257 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 363,073 | 3.631 | 20 | 50 | fits | 80,234 | 121 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 445,165 | 4.452 | 20 | 20 | fits | 82,158 | 73 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 940,245 | 9.402 | 20 | 20 | fits | 75,991 | 74 | 0.675 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 296,704 | 2.967 | 20 | 20 | fits | 81,276 | 106 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 281,973 | 2.820 | 20 | 200 | fits | 144,066 | 276 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 362,633 | 3.626 | 20 | 200 | fits | 81,276 | 106 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 282,897 | 2.829 | 20 | 20 | fits | 144,066 | 276 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 363,337 | 3.633 | 20 | 20 | fits | 81,276 | 106 | 0.418 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 142,471 | 1.425 | 20 | 24 | fits | 137,058 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 285,547 | 2.855 | 20 | 24 | fits | 144,066 | 276 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 285,481 | 2.855 | 20 | 50 | fits | 144,066 | 276 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 366,361 | 3.664 | 20 | 50 | fits | 81,276 | 106 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 448,537 | 4.485 | 20 | 20 | fits | 82,242 | 73 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 943,663 | 9.437 | 20 | 20 | fits | 75,109 | 73 | 0.664 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 291,502 | 2.915 | 20 | 20 | fits | 81,851 | 107 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 283,638 | 2.836 | 20 | 200 | fits | 144,011 | 276 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 364,873 | 3.649 | 20 | 200 | fits | 81,851 | 107 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 284,562 | 2.846 | 20 | 20 | fits | 144,011 | 276 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 365,577 | 3.656 | 20 | 20 | fits | 81,851 | 107 | 0.432 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 144,191 | 1.442 | 20 | 24 | fits | 137,058 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 287,212 | 2.872 | 20 | 24 | fits | 144,011 | 276 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 287,146 | 2.871 | 20 | 50 | fits | 144,011 | 276 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 368,601 | 3.686 | 20 | 50 | fits | 81,851 | 107 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 464,815 | 4.648 | 20 | 20 | fits | 86,188 | 80 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 942,932 | 9.429 | 20 | 20 | fits | 63,610 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 316,704 | 3.167 | 20 | 20 | fits | 93,922 | 156 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 266,995 | 2.670 | 20 | 200 | fits | 143,694 | 278 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 369,722 | 3.697 | 20 | 200 | fits | 93,922 | 156 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 267,919 | 2.679 | 20 | 20 | fits | 143,694 | 278 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 370,426 | 3.704 | 20 | 20 | fits | 93,922 | 156 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 127,865 | 1.279 | 20 | 24 | fits | 130,532 | 120 | 0.296 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 270,569 | 2.706 | 20 | 24 | fits | 143,694 | 278 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 270,503 | 2.705 | 20 | 50 | fits | 143,694 | 278 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 373,450 | 3.735 | 20 | 50 | fits | 93,922 | 156 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 459,325 | 4.593 | 20 | 20 | fits | 85,941 | 79 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 933,050 | 9.331 | 20 | 20 | fits | 52,183 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 313,567 | 3.136 | 20 | 20 | fits | 87,180 | 130 | 0.465 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 285,444 | 2.854 | 20 | 200 | fits | 146,031 | 266 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 372,008 | 3.720 | 20 | 200 | fits | 87,180 | 130 | 0.465 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 286,368 | 2.864 | 20 | 20 | fits | 146,031 | 266 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 372,712 | 3.727 | 20 | 20 | fits | 87,180 | 130 | 0.465 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 135,551 | 1.356 | 20 | 24 | fits | 137,179 | 162 | 0.282 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 289,018 | 2.890 | 20 | 24 | fits | 146,031 | 266 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 288,952 | 2.890 | 20 | 50 | fits | 146,031 | 266 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 375,736 | 3.757 | 20 | 50 | fits | 87,180 | 130 | 0.465 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 535,643 | 5.356 | 20 | 20 | fits | 82,394 | 74 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 930,688 | 9.307 | 20 | 20 | fits | 52,338 | 48 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 366,188 | 3.662 | 20 | 20 | fits | 86,995 | 127 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 280,883 | 2.809 | 20 | 200 | fits | 143,484 | 259 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 444,680 | 4.447 | 20 | 200 | fits | 86,995 | 127 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 281,807 | 2.818 | 20 | 20 | fits | 143,484 | 259 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 445,384 | 4.454 | 20 | 20 | fits | 86,995 | 127 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 141,963 | 1.420 | 20 | 24 | fits | 137,135 | 161 | 0.284 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 284,457 | 2.845 | 20 | 24 | fits | 143,484 | 259 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 284,391 | 2.844 | 20 | 50 | fits | 143,484 | 259 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 448,408 | 4.484 | 20 | 50 | fits | 86,995 | 127 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 530,572 | 5.306 | 20 | 20 | fits | 82,230 | 73 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 943,463 | 9.435 | 20 | 20 | fits | 64,226 | 60 | 0.695 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 322,275 | 3.223 | 20 | 20 | fits | 83,332 | 124 | 0.483 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 276,634 | 2.766 | 20 | 200 | fits | 145,697 | 267 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 368,934 | 3.689 | 20 | 200 | fits | 83,332 | 124 | 0.483 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 277,558 | 2.776 | 20 | 20 | fits | 145,697 | 267 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 369,638 | 3.696 | 20 | 20 | fits | 83,332 | 124 | 0.483 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 135,501 | 1.355 | 20 | 24 | fits | 137,129 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 280,208 | 2.802 | 20 | 24 | fits | 145,697 | 267 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 280,142 | 2.801 | 20 | 50 | fits | 145,697 | 267 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 372,662 | 3.727 | 20 | 50 | fits | 83,332 | 124 | 0.483 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 454,888 | 4.549 | 20 | 20 | fits | 82,292 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 849,887 | 8.499 | 20 | 20 | fits | 52,198 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 322,489 | 3.225 | 20 | 20 | fits | 80,476 | 121 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 286,874 | 2.869 | 20 | 200 | fits | 145,167 | 262 | 0.393 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 366,734 | 3.667 | 20 | 200 | fits | 80,476 | 121 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 287,798 | 2.878 | 20 | 20 | fits | 145,167 | 262 | 0.393 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 367,438 | 3.674 | 20 | 20 | fits | 80,476 | 121 | 0.422 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 137,766 | 1.378 | 20 | 24 | fits | 137,277 | 162 | 0.282 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 290,448 | 2.904 | 20 | 24 | fits | 145,167 | 262 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 290,382 | 2.904 | 20 | 50 | fits | 145,167 | 262 | 0.393 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 370,462 | 3.705 | 20 | 50 | fits | 80,476 | 121 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 452,737 | 4.527 | 20 | 20 | fits | 82,341 | 73 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 847,876 | 8.479 | 20 | 20 | fits | 52,183 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 305,245 | 3.052 | 20 | 20 | fits | 81,317 | 106 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 290,473 | 2.905 | 20 | 200 | fits | 144,034 | 276 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 371,174 | 3.712 | 20 | 200 | fits | 81,317 | 106 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 291,397 | 2.914 | 20 | 20 | fits | 144,034 | 276 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 371,878 | 3.719 | 20 | 20 | fits | 81,317 | 106 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 151,003 | 1.510 | 20 | 24 | fits | 138,169 | 162 | 0.293 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 294,047 | 2.940 | 20 | 24 | fits | 144,034 | 276 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 293,981 | 2.940 | 20 | 50 | fits | 144,034 | 276 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 374,902 | 3.749 | 20 | 50 | fits | 81,317 | 106 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 457,101 | 4.571 | 20 | 20 | fits | 82,265 | 73 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 873,172 | 8.732 | 20 | 20 | fits | 68,907 | 67 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 310,915 | 3.109 | 20 | 20 | fits | 88,815 | 163 | 0.417 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 267,238 | 2.672 | 20 | 200 | fits | 144,356 | 262 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 355,437 | 3.554 | 20 | 200 | fits | 88,815 | 163 | 0.417 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 268,162 | 2.682 | 20 | 20 | fits | 144,356 | 262 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 356,141 | 3.561 | 20 | 20 | fits | 88,815 | 163 | 0.417 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 127,446 | 1.274 | 20 | 24 | fits | 130,550 | 120 | 0.296 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 270,812 | 2.708 | 20 | 24 | fits | 144,356 | 262 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 270,746 | 2.707 | 20 | 50 | fits | 144,356 | 262 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 359,165 | 3.592 | 20 | 50 | fits | 88,815 | 163 | 0.417 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 441,244 | 4.412 | 20 | 20 | fits | 82,145 | 73 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 857,721 | 8.577 | 20 | 20 | fits | 75,463 | 73 | 0.668 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 304,873 | 3.049 | 20 | 20 | fits | 82,915 | 109 | 0.417 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 274,237 | 2.742 | 20 | 200 | fits | 143,353 | 277 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 356,536 | 3.565 | 20 | 200 | fits | 82,915 | 109 | 0.417 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 275,161 | 2.752 | 20 | 20 | fits | 143,353 | 277 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 357,240 | 3.572 | 20 | 20 | fits | 82,915 | 109 | 0.417 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 135,448 | 1.354 | 20 | 24 | fits | 137,076 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 277,811 | 2.778 | 20 | 24 | fits | 143,353 | 277 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 277,745 | 2.777 | 20 | 50 | fits | 143,353 | 277 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 360,264 | 3.603 | 20 | 50 | fits | 82,915 | 109 | 0.417 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 442,335 | 4.423 | 20 | 20 | fits | 82,137 | 73 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 858,959 | 8.590 | 20 | 20 | fits | 75,140 | 73 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 284,655 | 2.847 | 20 | 20 | fits | 81,741 | 106 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 276,791 | 2.768 | 20 | 200 | fits | 143,943 | 276 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 357,916 | 3.579 | 20 | 200 | fits | 81,741 | 106 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 277,715 | 2.777 | 20 | 20 | fits | 143,943 | 276 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 358,620 | 3.586 | 20 | 20 | fits | 81,741 | 106 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 137,412 | 1.374 | 20 | 24 | fits | 137,076 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 280,365 | 2.804 | 20 | 24 | fits | 143,943 | 276 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 280,299 | 2.803 | 20 | 50 | fits | 143,943 | 276 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 361,644 | 3.616 | 20 | 50 | fits | 81,741 | 106 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 447,748 | 4.477 | 20 | 20 | fits | 86,170 | 80 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 860,065 | 8.601 | 20 | 20 | fits | 63,610 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 308,072 | 3.081 | 20 | 20 | fits | 87,529 | 131 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 279,180 | 2.792 | 20 | 200 | fits | 144,612 | 261 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 366,093 | 3.661 | 20 | 200 | fits | 87,529 | 131 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 280,104 | 2.801 | 20 | 20 | fits | 144,612 | 261 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 366,797 | 3.668 | 20 | 20 | fits | 87,529 | 131 | 0.461 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 139,132 | 1.391 | 20 | 24 | fits | 137,076 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 282,754 | 2.828 | 20 | 24 | fits | 144,612 | 261 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 282,688 | 2.827 | 20 | 50 | fits | 144,612 | 261 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 369,821 | 3.698 | 20 | 50 | fits | 87,529 | 131 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 463,410 | 4.634 | 20 | 20 | fits | 83,475 | 74 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 858,908 | 8.589 | 20 | 20 | fits | 52,183 | 47 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 325,706 | 3.257 | 20 | 20 | fits | 90,682 | 133 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 279,894 | 2.799 | 20 | 200 | fits | 143,606 | 260 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 379,615 | 3.796 | 20 | 200 | fits | 90,682 | 133 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 280,818 | 2.808 | 20 | 20 | fits | 143,606 | 260 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 380,319 | 3.803 | 20 | 20 | fits | 90,682 | 133 | 0.460 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 140,852 | 1.409 | 20 | 24 | fits | 137,076 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 283,468 | 2.835 | 20 | 24 | fits | 143,606 | 260 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 283,402 | 2.834 | 20 | 50 | fits | 143,606 | 260 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 383,343 | 3.833 | 20 | 50 | fits | 90,682 | 133 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 465,461 | 4.655 | 20 | 20 | fits | 82,184 | 73 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 860,503 | 8.605 | 20 | 20 | fits | 52,197 | 47 | 0.716 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 153,777 | 1.538 | 20 | 200 | fits | 154,717 | 255 | 0.441 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 225,242 | 2.252 | 20 | 20 | fits | 91,602 | 108 | 0.664 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 261,317 | 2.613 | 20 | 24 | fits | 81,512 | 71 | 0.550 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 185,767 | 1.858 | 20 | 50 | fits | 91,602 | 108 | 0.664 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 772,421 | 7.724 | 20 | 20 | fits | 52,400 | 47 | 0.722 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 150,280 | 1.503 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 153,777 | 1.538 | 20 | 200 | fits | 154,717 | 255 | 0.441 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 197,811 | 1.978 | 20 | 20 | fits | 145,529 | 265 | 0.359 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 217,413 | 2.174 | 20 | 24 | fits | 54,755 | 51 | 0.445 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 177,650 | 1.776 | 20 | 50 | fits | 83,485 | 101 | 0.688 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 814,019 | 8.140 | 20 | 20 | fits | 33,637 | 33 | 0.788 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 168,790 | 1.688 | 49 | 49 | fits | 0 | - | 0.000 |
| Talker Advertise RX for every input, bound | `srp.bound_advertise.if0` | 50,106 | 0.501 | 20 | 20 | fits | 50,172 | 25 | 0.871 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 18,190 | 0.182 | 20 | 20 | fits | 24,319 | 21 (35) | 0.799 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 11,050 | 0.111 | 20 | 20 | fits | 20,787 | 17 (14) | 0.835 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 15,070 | 0.151 | 20 | 20 | fits | 19,248 | 18 (14) | 0.805 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 16,289 | 0.163 | 20 | 20 | fits | 24,222 | 21 (35) | 0.795 |
| a registering record of the burst | `srp.register_burst.t0.r0.if0` | 101,657 | 1.017 | 20 | 20 | fits | 94,386 | 40 | 0.848 |
| a registering record of the burst | `srp.register_burst.t0.r1.if0` | 101,576 | 1.016 | 20 | 20 | fits | 94,386 | 40 | 0.848 |
| a registering record of the burst | `srp.register_burst.t0.r2.if0` | 101,495 | 1.015 | 20 | 20 | fits | 94,386 | 40 | 0.848 |
| our MRPDU after a registering triple (JoinTime wait) | `srp.register_tx.t0.if0` | 131,109 | 1.311 | 220 | 220 | fits | 41,921 | 4 | 0.885 |
| ACMP's last record of its burst at a registering triple | `acmp.register_burst.t0.if0` | 141,880 | 1.419 | 20 | 20 | fits | 116,267 | 119 | 0.403 |
| AECP's last record of its burst at a registering triple | `aecp.register_burst.t0.if0` | 179,755 | 1.798 | 20 | 24 | fits | 55,580 | 45 | 0.458 |
| a registering record of the burst | `srp.register_burst.t1.r0.if0` | 71,117 | 0.711 | 20 | 20 | fits | 62,259 | 36 | 0.849 |
| a registering record of the burst | `srp.register_burst.t1.r1.if0` | 71,036 | 0.710 | 20 | 20 | fits | 62,259 | 36 | 0.849 |
| a registering record of the burst | `srp.register_burst.t1.r2.if0` | 70,955 | 0.710 | 20 | 20 | fits | 62,259 | 36 | 0.849 |
| our MRPDU after a registering triple (JoinTime wait) | `srp.register_tx.t1.if0` | 7,670,321 | 76.703 | 220 | 220 | fits | 38,987 | 4 | 0.861 |
| ACMP's last record of its burst at a registering triple | `acmp.register_burst.t1.if0` | 241,330 | 2.413 | 20 | 20 | fits | 73,795 | 39 | 0.771 |
| AECP's last record of its burst at a registering triple | `aecp.register_burst.t1.if0` | 261,046 | 2.610 | 20 | 24 | fits | 59,250 | 54 | 0.476 |
| a registering record of the burst | `srp.register_burst.t2.r0.if0` | 91,460 | 0.915 | 20 | 20 | fits | 85,184 | 40 | 0.833 |
| a registering record of the burst | `srp.register_burst.t2.r1.if0` | 91,379 | 0.914 | 20 | 20 | fits | 85,184 | 40 | 0.833 |
| a registering record of the burst | `srp.register_burst.t2.r2.if0` | 91,298 | 0.913 | 20 | 20 | fits | 85,184 | 40 | 0.833 |
| our MRPDU after a registering triple (JoinTime wait) | `srp.register_tx.t2.if0` | 15,675,731 | 156.757 | 220 | 220 | fits | 38,669 | 4 | 0.859 |
| ACMP's last record of its burst at a registering triple | `acmp.register_burst.t2.if0` | 111,962 | 1.120 | 20 | 20 | fits | 125,660 | 141 | 0.378 |
| AECP's last record of its burst at a registering triple | `aecp.register_burst.t2.if0` | 300,185 | 3.002 | 20 | 24 | fits | 61,738 | 62 | 0.499 |
| LINK_UP | `adp.link_up.if0` | 3,264 | 0.033 | 20 | 200 | fits | 23,744 | 44 (12) | 0.716 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,547 | 0.085 | 20 | 200 | fits | 17,160 | 23 (39) | 0.628 |
| LINK_DOWN | `adp.link_down.if0` | 2,015 | 0.020 | 20 | 200 | fits | 19,385 | 23 (9) | 0.686 |
| LINK_UP | `adp.link_up.if0` | 3,264 | 0.033 | 20 | 200 | fits | 23,744 | 44 (12) | 0.716 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,547 | 0.085 | 20 | 200 | fits | 17,160 | 23 (39) | 0.628 |
| GM_CHANGE | `adp.gm_change.if0` | 2,212 | 0.022 | 20 | 200 | fits | 11,964 | 17 (11) | 0.400 |
| LINK_UP | `adp.link_up.if0` | 3,264 | 0.033 | 20 | 200 | fits | 23,744 | 44 (12) | 0.716 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,547 | 0.085 | 20 | 200 | fits | 17,160 | 23 (39) | 0.628 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,886 | 0.049 | 20 | 200 | fits | 13,094 | 16 (31) | 0.508 |
| LINK_UP | `adp.link_up.if0` | 3,264 | 0.033 | 20 | 200 | fits | 23,744 | 44 (12) | 0.716 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,547 | 0.085 | 20 | 200 | fits | 17,160 | 23 (39) | 0.628 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,886 | 0.049 | 20 | 200 | fits | 13,094 | 16 (31) | 0.508 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 46,299 | 0.463 | 20 | 20 | fits | 16,526 | 9 | 0.836 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 34,601 | 0.346 | 20 | 20 | fits | 34,667 | 21 | 0.850 |
| malformed MRPDU discard | `srp.malformed.if0` | 18,773 | 0.188 | 20 | 20 | fits | 18,839 | 21 | 0.688 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 57,543 | 0.575 | 220 | 220 | fits | 33,016 | 7 | 0.896 |
| an event behind 15 others | `backlog.event.if0` | 148,647 | 1.486 | 20 | 200 | fits | 46,231 | 78 | 0.557 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 351,800 | 3.518 | 20 | 20 | fits | 133,723 | 161 | 0.344 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 370,414 | 3.704 | 20 | 200 | fits | 133,723 | 161 | 0.344 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 369,798 | 3.698 | 20 | 200 | fits | 133,723 | 161 | 0.344 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 366,092 | 3.661 | 20 | 20 | fits | 133,723 | 161 | 0.344 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 365,256 | 3.653 | 20 | 20 | fits | 133,723 | 161 | 0.344 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 138,332 | 1.383 | 20 | 24 | fits | 139,223 | 164 | 0.307 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 235,019 | 2.350 | 20 | 24 | fits | 51,446 | 26 | 0.724 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 368,676 | 3.687 | 20 | 50 | fits | 133,723 | 161 | 0.344 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 368,280 | 3.683 | 20 | 50 | fits | 133,723 | 161 | 0.344 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 412,388 | 4.124 | 20 | 20 | fits | 41,818 | 165 | 0.178 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 484,551 | 4.846 | 20 | 20 | fits | 31,145 | 112 | 0.126 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 284,461 | 2.845 | 20 | 20 | fits | 79,425 | 119 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 276,449 | 2.764 | 20 | 200 | fits | 144,285 | 261 | 0.378 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 355,258 | 3.553 | 20 | 200 | fits | 79,425 | 119 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 277,373 | 2.774 | 20 | 20 | fits | 144,285 | 261 | 0.378 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 355,962 | 3.560 | 20 | 20 | fits | 79,425 | 119 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 136,728 | 1.367 | 20 | 24 | fits | 136,914 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 280,023 | 2.800 | 20 | 24 | fits | 144,285 | 261 | 0.378 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 279,957 | 2.800 | 20 | 50 | fits | 144,285 | 261 | 0.378 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 358,986 | 3.590 | 20 | 50 | fits | 79,425 | 119 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 455,594 | 4.556 | 20 | 20 | fits | 86,525 | 80 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 855,329 | 8.553 | 20 | 20 | fits | 63,605 | 60 | 0.685 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 6,817 | 0.068 | 20 | 20 | fits | 20,994 | 19 | 0.742 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 276,449 | 2.764 | 20 | 200 | fits | 144,285 | 261 | 0.378 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 20,348 | 0.203 | 20 | 200 | fits | 20,994 | 19 | 0.742 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 277,373 | 2.774 | 20 | 20 | fits | 144,285 | 261 | 0.378 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 370,913 | 3.709 | 20 | 20 | fits | 94,376 | 122 | 0.521 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 136,728 | 1.367 | 20 | 24 | fits | 136,914 | 161 | 0.281 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 280,023 | 2.800 | 20 | 24 | fits | 144,285 | 261 | 0.378 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 279,957 | 2.800 | 20 | 50 | fits | 144,285 | 261 | 0.378 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 373,937 | 3.739 | 20 | 50 | fits | 94,376 | 122 | 0.521 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 373,871 | 3.739 | 20 | 20 | fits | 94,376 | 122 | 0.521 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 853,977 | 8.540 | 20 | 20 | fits | 52,181 | 47 | 0.716 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,252,757 | 62.528 | 20 | 20 | MISS ceiling | 14,691 | 13 | 0.550 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,267,425 | 62.674 | 20 | 20 | MISS ceiling | 14,665 | 13 | 0.516 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,281,833 | 62.818 | 20 | 20 | MISS ceiling | 14,465 | 13 | 0.550 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,296,268 | 62.963 | 20 | 20 | MISS ceiling | 14,511 | 13 | 0.550 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,310,615 | 63.106 | 20 | 20 | MISS ceiling | 14,410 | 13 | 0.550 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 149,946 | 1.499 | 20 | 200 | fits | 147,371 | 231 | 0.407 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 242,948 | 2.429 | 20 | 200 | fits | 93,618 | 162 | 0.551 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 145,624 | 1.456 | 20 | 20 | fits | 147,371 | 231 | 0.407 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,180,776 | 61.808 | 20 | 20 | MISS ceiling | 25,391 | 15 | 0.702 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 149,264 | 1.493 | 20 | 24 | fits | 147,371 | 231 | 0.407 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,158,871 | 61.589 | 20 | 24 | MISS ceiling | 120,949 | 106 | 0.352 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 148,208 | 1.482 | 20 | 50 | fits | 147,371 | 231 | 0.407 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 241,430 | 2.414 | 20 | 50 | fits | 93,618 | 162 | 0.551 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 241,364 | 2.414 | 20 | 20 | fits | 93,618 | 162 | 0.551 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 704,918 | 7.049 | 20 | 20 | fits | 40,994 | 34 | 0.773 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,391 | 0.054 | 20 | 20 | fits | 18,278 | 13 (29) | 0.722 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,691 | 0.077 | 20 | 20 | fits | 20,043 | 19 (35) | 0.720 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 16,864 | 0.169 | 20 | 20 | fits | 24,344 | 21 (12) | 0.799 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 10,400 | 0.104 | 20 | 50 | fits | 23,744 | 44 | 0.716 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 14,502 | 0.145 | 20 | 50 | fits | 18,569 | 35 | 0.610 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 9,492 | 0.095 | 20 | 50 | fits | 18,437 | 35 | 0.606 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 11,417 | 0.114 | 20 | 50 | fits | 23,376 | 61 | 0.589 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 13,372 | 0.134 | 20 | 50 | fits | 23,376 | 61 | 0.589 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 9,282 | 0.093 | 20 | 50 | fits | 18,056 | 30 | 0.613 |
| set_name | `aecp_fanout.set_name.if0` | 40,999 | 0.410 | 20 | 24 | fits | 53,873 | 89 | 0.577 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 41,488 | 0.415 | 20 | 24 | fits | 49,537 | 78 | 0.620 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 36,244 | 0.362 | 20 | 24 | fits | 44,746 | 79 | 0.574 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 37,109 | 0.371 | 20 | 24 | fits | 43,626 | 78 | 0.565 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 49,435 | 0.494 | 20 | 24 | fits | 58,876 | 110 | 0.600 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 273,406 | 2.734 | 20 | 24 | fits | 54,390 | 109 | 0.569 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 335,865 | 3.359 | 20 | 24 | fits | 47,866 | 67 | 0.618 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 37,946 | 0.379 | 20 | 24 | fits | 44,590 | 78 | 0.578 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 36,238 | 0.362 | 20 | 24 | fits | 43,699 | 79 | 0.562 |
| BIND_RX | `acmp.bind_rx.if0` | 18,375 | 0.184 | 20 | 20 | fits | 37,636 | 26 (77) | 0.794 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,871 | 0.099 | 20 | 20 | fits | 26,951 | 19 (32) | 0.833 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,761 | 0.108 | 20 | 20 | fits | 22,166 | 15 (47) | 0.739 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,271 | 0.133 | 20 | 20 | fits | 34,629 | 19 (50) | 0.831 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 11,271 | 0.113 | 20 | 20 | fits | 22,817 | 17 (48) | 0.732 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 10,168 | 0.102 | 20 | 20 | fits | 21,176 | 16 (48) | 0.678 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 8,872 | 0.089 | 20 | 20 | fits | 20,390 | 16 (48) | 0.664 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,179 | 0.092 | 20 | 20 | fits | 20,371 | 16 (48) | 0.664 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 10,866 | 0.109 | 20 | 24 | fits | 23,912 | 20 | 0.772 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 20,757 | 0.208 | 20 | 24 | fits | 27,705 | 20 | 0.702 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 15,843 | 0.158 | 20 | 24 | fits | 24,957 | 20 | 0.741 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 17,429 | 0.174 | 20 | 24 | fits | 24,391 | 20 | 0.734 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 15,952 | 0.160 | 20 | 24 | fits | 25,012 | 20 | 0.734 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 18,126 | 0.181 | 20 | 24 | fits | 24,902 | 20 | 0.735 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 17,250 | 0.172 | 20 | 24 | fits | 24,104 | 20 | 0.740 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 15,342 | 0.153 | 20 | 24 | fits | 24,323 | 20 | 0.751 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 17,028 | 0.170 | 20 | 24 | fits | 23,637 | 20 | 0.750 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 17,402 | 0.174 | 20 | 24 | fits | 26,424 | 21 | 0.653 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 16,777 | 0.168 | 20 | 24 | fits | 23,358 | 20 | 0.772 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 14,246 | 0.142 | 20 | 24 | fits | 23,280 | 20 | 0.767 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 17,407 | 0.174 | 20 | 24 | fits | 24,171 | 20 | 0.741 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 15,536 | 0.155 | 20 | 24 | fits | 24,593 | 20 | 0.738 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 15,001 | 0.150 | 20 | 24 | fits | 23,993 | 20 | 0.753 |
| get_configuration | `aecp.get_configuration.if0` | 15,310 | 0.153 | 20 | 24 | fits | 21,386 | 20 | 0.752 |
| entity_available | `aecp.entity_available.if0` | 12,732 | 0.127 | 20 | 24 | fits | 21,191 | 20 | 0.734 |
| get_name | `aecp.get_name.if0` | 17,384 | 0.174 | 20 | 24 | fits | 24,162 | 20 | 0.759 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 16,959 | 0.170 | 20 | 24 | fits | 26,961 | 26 | 0.748 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 19,527 | 0.195 | 20 | 24 | fits | 26,582 | 28 | 0.775 |
| get_as_path, refused ENTITY_MISBEHAVING | `aecp.get_as_path.if0` | 15,841 | 0.158 | 20 | 24 | fits | 25,277 | 28 | 0.768 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 15,472 | 0.155 | 20 | 24 | fits | 21,594 | 20 | 0.757 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 14,628 | 0.146 | 20 | 24 | fits | 20,558 | 20 | 0.730 |
| set_name | `aecp.set_name.if0` | 21,461 | 0.215 | 20 | 24 | fits | 40,858 | 43 | 0.759 |
| lock_entity | `aecp.lock_entity.if0` | 21,724 | 0.217 | 20 | 24 | fits | 33,658 | 34 | 0.795 |
| unlock_entity | `aecp.unlock_entity.if0` | 19,332 | 0.193 | 20 | 24 | fits | 32,507 | 33 | 0.789 |
| Talker Advertise RX for every input, bound | `srp.register_advertise.if0` | 49,915 | 0.499 | 20 | 20 | fits | 49,981 | 25 | 0.868 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 136,961 | 1.370 | 20 | 24 | fits | 150,315 | 137 | 0.323 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 338,758 | 3.388 | 20 | 24 | fits | 142,865 | 114 | 0.290 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 240,575 | 2.406 | 20 | 24 | fits | 36,994 | 17 | 0.644 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 394,025 | 3.940 | 20 | 24 | fits | 86,820 | 18 | 0.656 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 352,649 | 3.526 | 20 | 24 | fits | 97,080 | 17 | 0.656 |
| READ_DESCRIPTOR held for a token (#917) | `aecp.held.read_descriptor.if0` | 518,261 | 5.183 | 20 | 24 | fits | 26,963 | 17 | 0.718 |
| LINK_UP | `fixture.link_up.if0` | 3,264 | 0.033 | 20 | 200 | fits | 23,744 | 44 (12) | 0.716 |
| malformed MRPDU discard | `fixture.malformed.if0` | 18,797 | 0.188 | 20 | 20 | fits | 18,863 | 21 | 0.696 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 29,880 | 0.299 | 20 | 24 | fits | 42,388 | 43 | 0.774 |
| LINK_DOWN | `fixture.link_down.if0` | 2,402 | 0.024 | 20 | 200 | fits | 22,098 | 23 (9) | 0.748 |
| BIND_RX | `fixture.bind_rx.if0` | 19,188 | 0.192 | 20 | 20 | fits | 38,101 | 26 (77) | 0.796 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 16,795 | 0.168 | 20 | 20 | fits | 30,095 | 29 (35) | 0.767 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 14,592 | 0.146 | 20 | 20 | fits | 19,930 | 13 (29) | 0.769 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 76,892 | 0.769 | 20 | 200 | fits | 76,996 | 86 | 0.730 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 76,892 | 0.769 | 20 | 200 | fits | 76,996 | 86 | 0.730 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 76,618 | 0.766 | 20 | 20 | fits | 76,996 | 86 | 0.730 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 76,618 | 0.766 | 20 | 20 | fits | 76,996 | 86 | 0.730 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 76,826 | 0.768 | 20 | 24 | fits | 76,996 | 86 | 0.730 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 76,826 | 0.768 | 20 | 24 | fits | 76,996 | 86 | 0.730 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 76,760 | 0.768 | 20 | 50 | fits | 76,996 | 86 | 0.730 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 76,760 | 0.768 | 20 | 50 | fits | 76,996 | 86 | 0.730 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 76,694 | 0.767 | 20 | 20 | fits | 76,996 | 86 | 0.730 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 76,694 | 0.767 | 20 | 20 | fits | 76,996 | 86 | 0.730 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
