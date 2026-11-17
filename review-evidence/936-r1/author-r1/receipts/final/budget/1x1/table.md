Original file: <scratch>/budget/final/1x1/table.md
Original size: 188809 bytes
Original sha256: a86ad09a3a522051a775e27f3e24c0d8dbf929197421aa7f84bcd9c31a6ee7d0

TRUNCATED at 177879 of 188809 bytes (the original is kept in scratch, its sha256 above)

### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 92 paths and 7 of 950 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.186 (0.413) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.091 (0.230) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.072 (0.260) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.183 (0.534) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.102 (0.256) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.091 (0.230) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.094 (0.238) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.102 (0.253) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.092 (0.314) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.108 (0.467) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.245 (0.604) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.246 (0.528) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.124 (0.496) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.173 (0.625) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.255 (0.492) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.123 (0.379) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.047 (0.163) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.025 (0.175) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.029 (0.255) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.029 (0.270) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.018 (0.029) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.154 (0.485) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.110 (0.416) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.149 (0.467) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.154 (0.468) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.189 (0.512) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.181 (0.505) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.208 (0.542) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.192 (0.500) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.224 (0.554) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.140 (0.460) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.135 (0.451) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.171 (0.492) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.158 (0.472) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.169 (0.491) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.171 (0.493) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.177 (0.500) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.131 (0.445) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.181 (0.506) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.133 (0.453) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.140 (0.458) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.143 (0.467) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.179 (0.499) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.116 (0.275) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.249 (0.677) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.165 (0.484) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.247 (0.633) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.557 (2.873) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.488 (0.776) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.592 (0.909) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.465 (0.779) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.563 (0.844) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.502 (0.836) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.152 (3.464) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.489 (0.770) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 3.146 (3.467) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.137 (2.507) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.735 (4.097) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.046 (3.407) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.325 (1.657) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.261 (4.625) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-aged2-7.adp_available.if0` (backlog-adp@blank-aged2-7) | 4.673 (5.286) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.096 (0.458) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.668 (2.097) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.041 (63.336) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.784 (64.079) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.321 (0.466) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 2.159 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 1.518 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 2.964 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 1.313 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 9.973 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.160 (0.494) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.087 (0.213) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.105 (0.270) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.134 (0.494) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.185 (0.506) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.628 | fits | 0 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.177 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.145 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.220 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.adp.last.if0` (backlog-adp@blank-aged2-7) | 5.173 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.268 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.887 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.203 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.maap.last.if0` (backlog-adp@blank-aged2-7) | 5.211 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-5.service.srp.first.if0` (backlog-adp@program-aged2-5) | 6.099 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-5.service.srp.last.if0` (backlog-adp@program-aged2-5) | 11.172 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.874 (0.976) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.450 (0.451) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.209 (0.210) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.761 (0.838) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 12.215 | 11 | 150,255 (1.503) | yes | - |
| backlog-adp@blank-1 | 0 | 11.444 | 11 | 149,775 (1.498) | yes | - |
| backlog-adp@blank-2 | 0 | 11.448 | 11 | 149,775 (1.498) | yes | - |
| backlog-adp@blank-3 | 0 | 11.952 | 13 | 149,775 (1.498) | yes | - |
| backlog-adp@blank-4 | 0 | 11.972 | 13 | 149,775 (1.498) | yes | - |
| backlog-adp@blank-5 | 0 | 11.656 | 12 | 149,781 (1.498) | yes | - |
| backlog-adp@blank-6 | 0 | 11.534 | 11 | 149,854 (1.499) | yes | - |
| backlog-adp@blank-7 | 0 | 13.364 | 14 | 149,854 (1.499) | yes | - |
| backlog-adp@program-0 | 0 | 11.502 | 11 | 149,887 (1.499) | yes | - |
| backlog-adp@program-1 | 0 | 11.703 | 12 | 149,965 (1.500) | yes | - |
| backlog-adp@program-2 | 0 | 11.556 | 11 | 149,828 (1.498) | yes | - |
| backlog-adp@program-3 | 0 | 12.036 | 11 | 148,036 (1.480) | yes | - |
| backlog-adp@program-4 | 0 | 10.773 | 11 | 150,072 (1.501) | yes | - |
| backlog-adp@program-5 | 0 | 10.777 | 11 | 149,877 (1.499) | yes | - |
| backlog-adp@program-6 | 0 | 10.820 | 11 | 149,877 (1.499) | yes | - |
| backlog-adp@program-7 | 0 | 11.145 | 13 | 149,878 (1.499) | yes | - |
| backlog-adp@verify-0 | 0 | 11.816 | 11 | 150,540 (1.505) | yes | - |
| backlog-adp@verify-1 | 0 | 11.493 | 11 | 149,888 (1.499) | yes | - |
| backlog-adp@verify-2 | 0 | 11.501 | 11 | 149,888 (1.499) | yes | - |
| backlog-adp@verify-3 | 0 | 11.953 | 13 | 149,888 (1.499) | yes | - |
| backlog-adp@verify-4 | 0 | 11.529 | 11 | 148,088 (1.481) | yes | - |
| backlog-adp@verify-5 | 1 | 11.452 | 10 | 147,113 (1.471) | yes | - |
| backlog-adp@verify-6 | 0 | 11.583 | 11 | 149,827 (1.498) | yes | - |
| backlog-adp@verify-7 | 0 | 12.571 | 12 | 149,828 (1.498) | yes | - |
| backlog-adp@blank-aged2-0 | 1 | 11.715 | 12 | 146,277 (1.463) | yes | - |
| backlog-adp@blank-aged2-1 | 1 | 11.547 | 11 | 146,386 (1.464) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 11.655 | 12 | 148,909 (1.489) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 11.480 | 11 | 148,919 (1.489) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 11.390 | 10 | 146,635 (1.466) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 11.476 | 11 | 148,681 (1.487) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 11.393 | 11 | 148,919 (1.489) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 12.934 | 14 | 148,919 (1.489) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 12.103 | 13 | 148,747 (1.487) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 12.954 | 15 | 148,747 (1.487) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 12.454 | 15 | 148,985 (1.490) | yes | - |
| backlog-adp@blank-aged1-3 | 1 | 12.227 | 13 | 146,759 (1.468) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 12.215 | 13 | 148,969 (1.490) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 12.120 | 13 | 148,667 (1.487) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 13.754 | 15 | 148,667 (1.487) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 12.185 | 13 | 148,905 (1.489) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.513 | 12 | 149,104 (1.491) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 11.492 | 11 | 148,860 (1.489) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 11.605 | 11 | 148,860 (1.489) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 11.535 | 11 | 149,098 (1.491) | yes | - |
| backlog-adp@program-aged2-4 | 1 | 12.176 | 12 | 146,802 (1.468) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 11.706 | 12 | 148,860 (1.489) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 11.620 | 12 | 149,149 (1.491) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 11.856 | 12 | 149,243 (1.492) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 11.932 | 13 | 149,098 (1.491) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 11.588 | 12 | 148,929 (1.489) | yes | - |
| backlog-adp@program-aged1-2 | 1 | 11.477 | 10 | 146,306 (1.463) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 11.509 | 11 | 148,860 (1.489) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 11.451 | 10 | 147,258 (1.473) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 11.517 | 11 | 149,098 (1.491) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 11.448 | 11 | 148,860 (1.489) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 12.114 | 13 | 148,860 (1.489) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.368 | 11 | 149,098 (1.491) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 11.454 | 11 | 148,860 (1.489) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 11.536 | 11 | 148,860 (1.489) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 11.775 | 13 | 149,098 (1.491) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 11.570 | 11 | 147,098 (1.471) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 11.652 | 12 | 149,005 (1.490) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 11.463 | 11 | 148,860 (1.489) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 12.536 | 12 | 148,860 (1.489) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 11.567 | 12 | 148,866 (1.489) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 11.419 | 10 | 146,736 (1.467) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 11.534 | 11 | 148,860 (1.489) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 11.448 | 11 | 149,098 (1.491) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 12.221 | 13 | 149,098 (1.491) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 11.773 | 13 | 148,860 (1.489) | yes | - |
| backlog-adp@verify-aged1-6 | 1 | 11.557 | 11 | 147,627 (1.476) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 12.640 | 12 | 149,217 (1.492) | yes | - |
| backlog | 0 | 5.718 | 7 | 152,871 (1.529) | yes | - |
| backlog-adp | 0 | 10.665 | 11 | 149,429 (1.494) | yes | - |
| backlog-adp-refill | 0 | 40.780 | 26 | 149,429 (1.494) | yes | - |
| backlog-owed | 0 | 64.446 | 26 | 148,994 (1.490) | yes | - |
| fixture | 0 | 1.315 | 2 | 81,673 (0.817) | yes | - |

Composed maximum over the 4 backlog windows: 152,871 CPU cycles (1.529 ms), backlog.
Over the windows that released their whole load only: 152,871 (1.529 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3609 | 0 | 40,350 (0.404) | fits |
| save-second | 44737 | 0 | 50,677 (0.507) | fits |
| backlog-adp@blank-0 | 416 | 0 | 150,255 (1.503) | fits |
| backlog-adp@blank-1 | 416 | 0 | 149,775 (1.498) | fits |
| backlog-adp@blank-2 | 416 | 0 | 149,775 (1.498) | fits |
| backlog-adp@blank-3 | 418 | 0 | 149,775 (1.498) | fits |
| backlog-adp@blank-4 | 418 | 0 | 149,775 (1.498) | fits |
| backlog-adp@blank-5 | 417 | 0 | 149,781 (1.498) | fits |
| backlog-adp@blank-6 | 418 | 0 | 149,854 (1.499) | fits |
| backlog-adp@blank-7 | 421 | 0 | 149,854 (1.499) | fits |
| backlog-adp@program-0 | 519 | 0 | 149,887 (1.499) | fits |
| backlog-adp@program-1 | 520 | 0 | 149,965 (1.500) | fits |
| backlog-adp@program-2 | 521 | 0 | 149,828 (1.498) | fits |
| backlog-adp@program-3 | 522 | 0 | 149,827 (1.498) | fits |
| backlog-adp@program-4 | 522 | 0 | 150,072 (1.501) | fits |
| backlog-adp@program-5 | 524 | 0 | 149,877 (1.499) | fits |
| backlog-adp@program-6 | 524 | 0 | 149,877 (1.499) | fits |
| backlog-adp@program-7 | 526 | 0 | 149,878 (1.499) | fits |
| backlog-adp@verify-0 | 614 | 0 | 150,540 (1.505) | fits |
| backlog-adp@verify-1 | 614 | 0 | 149,888 (1.499) | fits |
| backlog-adp@verify-2 | 614 | 0 | 149,888 (1.499) | fits |
| backlog-adp@verify-3 | 616 | 0 | 149,888 (1.499) | fits |
| backlog-adp@verify-4 | 615 | 0 | 149,967 (1.500) | fits |
| backlog-adp@verify-5 | 615 | 0 | 150,436 (1.504) | fits |
| backlog-adp@verify-6 | 616 | 0 | 149,827 (1.498) | fits |
| backlog-adp@verify-7 | 617 | 0 | 149,828 (1.498) | fits |
| backlog-adp@blank-aged2-0 | 702 | 0 | 152,657 (1.527) | fits |
| backlog-adp@blank-aged2-1 | 706 | 0 | 149,062 (1.491) | fits |
| backlog-adp@blank-aged2-2 | 714 | 0 | 148,909 (1.489) | fits |
| backlog-adp@blank-aged2-3 | 720 | 0 | 148,919 (1.489) | fits |
| backlog-adp@blank-aged2-4 | 727 | 0 | 148,681 (1.487) | fits |
| backlog-adp@blank-aged2-5 | 735 | 0 | 148,681 (1.487) | fits |
| backlog-adp@blank-aged2-6 | 742 | 0 | 148,919 (1.489) | fits |
| backlog-adp@blank-aged2-7 | 753 | 0 | 148,919 (1.489) | fits |
| backlog-adp@blank-aged1-0 | 643 | 0 | 148,747 (1.487) | fits |
| backlog-adp@blank-aged1-1 | 653 | 0 | 148,747 (1.487) | fits |
| backlog-adp@blank-aged1-2 | 660 | 0 | 148,985 (1.490) | fits |
| backlog-adp@blank-aged1-3 | 666 | 0 | 148,696 (1.487) | fits |
| backlog-adp@blank-aged1-4 | 673 | 0 | 148,969 (1.490) | fits |
| backlog-adp@blank-aged1-5 | 680 | 0 | 148,667 (1.487) | fits |
| backlog-adp@blank-aged1-6 | 690 | 0 | 148,667 (1.487) | fits |
| backlog-adp@blank-aged1-7 | 695 | 0 | 148,905 (1.489) | fits |
| backlog-adp@program-aged2-0 | 800 | 0 | 149,104 (1.491) | fits |
| backlog-adp@program-aged2-1 | 806 | 0 | 148,860 (1.489) | fits |
| backlog-adp@program-aged2-2 | 814 | 0 | 148,860 (1.489) | fits |
| backlog-adp@program-aged2-3 | 821 | 0 | 149,098 (1.491) | fits |
| backlog-adp@program-aged2-4 | 830 | 0 | 148,860 (1.489) | fits |
| backlog-adp@program-aged2-5 | 837 | 0 | 148,860 (1.489) | fits |
| backlog-adp@program-aged2-6 | 844 | 0 | 149,149 (1.491) | fits |
| backlog-adp@program-aged2-7 | 852 | 0 | 149,243 (1.492) | fits |
| backlog-adp@program-aged1-0 | 742 | 0 | 149,098 (1.491) | fits |
| backlog-adp@program-aged1-1 | 748 | 0 | 148,929 (1.489) | fits |
| backlog-adp@program-aged1-2 | 755 | 0 | 151,226 (1.512) | fits |
| backlog-adp@program-aged1-3 | 762 | 0 | 148,860 (1.489) | fits |
| backlog-adp@program-aged1-4 | 769 | 0 | 149,098 (1.491) | fits |
| backlog-adp@program-aged1-5 | 777 | 0 | 149,098 (1.491) | fits |
| backlog-adp@program-aged1-6 | 784 | 0 | 148,860 (1.489) | fits |
| backlog-adp@program-aged1-7 | 794 | 0 | 148,860 (1.489) | fits |
| backlog-adp@verify-aged2-0 | 896 | 0 | 149,098 (1.491) | fits |
| backlog-adp@verify-aged2-1 | 903 | 0 | 148,860 (1.489) | fits |
| backlog-adp@verify-aged2-2 | 911 | 0 | 148,860 (1.489) | fits |
| backlog-adp@verify-aged2-3 | 920 | 0 | 149,098 (1.491) | fits |
| backlog-adp@verify-aged2-4 | 926 | 0 | 148,947 (1.489) | fits |
| backlog-adp@verify-aged2-5 | 934 | 0 | 149,005 (1.490) | fits |
| backlog-adp@verify-aged2-6 | 940 | 0 | 148,860 (1.489) | fits |
| backlog-adp@verify-aged2-7 | 949 | 0 | 148,860 (1.489) | fits |
| backlog-adp@verify-aged1-0 | 838 | 0 | 148,866 (1.489) | fits |
| backlog-adp@verify-aged1-1 | 844 | 0 | 148,860 (1.489) | fits |
| backlog-adp@verify-aged1-2 | 852 | 0 | 148,860 (1.489) | fits |
| backlog-adp@verify-aged1-3 | 859 | 0 | 149,098 (1.491) | fits |
| backlog-adp@verify-aged1-4 | 869 | 0 | 149,098 (1.491) | fits |
| backlog-adp@verify-aged1-5 | 876 | 0 | 148,860 (1.489) | fits |
| backlog-adp@verify-aged1-6 | 882 | 0 | 149,149 (1.491) | fits |
| backlog-adp@verify-aged1-7 | 890 | 0 | 149,217 (1.492) | fits |
| adp-advertise | 598 | 0 | 29,100 (0.291) | fits |
| save-held | 1471 | 0 | 152,690 (1.527) | fits |
| save-starved | 23583 | 0 | 152,690 (1.527) | fits |
| acmp-noresp | 2023 | 0 | 40,350 (0.404) | fits |
| save | 610 | 0 | 45,181 (0.452) | fits |
| srp | 290 | 0 | 56,849 (0.568) | fits |
| backlog | 286 | 0 | 152,871 (1.529) | fits |
| backlog-adp | 315 | 0 | 149,429 (1.494) | fits |
| backlog-adp-refill | 330 | 0 | 149,429 (1.494) | fits |
| backlog-owed | 311 | 0 | 148,994 (1.490) | fits |
| acmp-disc | 937 | 0 | 40,350 (0.404) | fits |
| maap | 182 | 0 | 29,100 (0.291) | fits |
| adp-link | 89 | 0 | 39,375 (0.394) | fits |
| adp-gm | 88 | 0 | 28,867 (0.289) | fits |
| adp-discover | 88 | 0 | 28,867 (0.289) | fits |
| control | 88 | 0 | 28,867 (0.289) | fits |
| aecp-fanout | 113 | 0 | 62,340 (0.623) | fits |
| acmp-cmd | 85 | 0 | 40,350 (0.404) | fits |
| aecp | 112 | 0 | 44,458 (0.445) | fits |
| aecp-largest-notice | 107 | 0 | 144,843 (1.448) | fits |
| datapath-events | 116 | 0 | 28,867 (0.289) | fits |
| fixture | 151 | 0 | 81,673 (0.817) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 10.130 (20) | 9.870 |
| backlog-adp@blank-aged2-1 | 2 | none | none | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 11.011 (20) | 8.989 |
| backlog-adp@blank-aged2-2 | 2 | +7.751 ms, 76,458 (0.765 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 11.125 (20) | 8.875 |
| backlog-adp@blank-aged2-3 | 2 | +6.713 ms, 76,392 (0.764 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 10.949 (20) | 9.051 |
| backlog-adp@blank-aged2-4 | 2 | none | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 10.857 (20) | 9.143 |
| backlog-adp@blank-aged2-5 | 2 | none | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 10.946 (20) | 9.054 |
| backlog-adp@blank-aged2-6 | 2 | none | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 10.862 (20) | 9.138 |
| backlog-adp@blank-aged2-7 | 2 | none | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 10.983 (20) | 9.017 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 10.205 (20) | 9.795 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 10.600 (20) | 9.400 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 10.858 (20) | 9.142 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 10.946 (20) | 9.054 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 10.933 (20) | 9.067 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 10.837 (20) | 9.163 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 10.915 (20) | 9.085 |
| backlog-adp@blank-aged1-7 | 1 | none | +11.078 ms, 76,441 (0.764 ms), read-back | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 10.830 (20) | 9.170 |
| backlog-adp@program-aged2-0 | 2 | none | +10.356 ms, 80,557 (0.806 ms), issue | `backlog-adp@program-aged2-0.service.srp.last.if0` | 10.319 (20) | 9.681 |
| backlog-adp@program-aged2-1 | 2 | +9.318 ms, 80,530 (0.805 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 10.959 (20) | 9.041 |
| backlog-adp@program-aged2-2 | 2 | +7.700 ms, 80,530 (0.805 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 11.073 (20) | 8.927 |
| backlog-adp@program-aged2-3 | 2 | +6.766 ms, 80,413 (0.804 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 11.002 (20) | 8.998 |
| backlog-adp@program-aged2-4 | 2 | +5.941 ms, 80,496 (0.805 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 10.912 (20) | 9.088 |
| backlog-adp@program-aged2-5 | 2 | +4.440 ms, 80,195 (0.802 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 11.172 (20) | 8.828 |
| backlog-adp@program-aged2-6 | 2 | +4.354 ms, 80,195 (0.802 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 11.090 (20) | 8.910 |
| backlog-adp@program-aged2-7 | 2 | +3.095 ms, 79,966 (0.800 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 11.078 (20) | 8.922 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 10.187 (20) | 9.813 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 10.254 (20) | 9.746 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 10.147 (20) | 9.853 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 10.180 (20) | 9.820 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 10.120 (20) | 9.880 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 10.188 (20) | 9.812 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 10.119 (20) | 9.881 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 10.230 (20) | 9.770 |
| backlog-adp@verify-aged2-0 | 2 | none | +10.248 ms, 77,324 (0.773 ms), read-back | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 10.211 (20) | 9.789 |
| backlog-adp@verify-aged2-1 | 2 | +9.312 ms, 77,324 (0.773 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 10.922 (20) | 9.078 |
| backlog-adp@verify-aged2-2 | 2 | +7.794 ms, 77,407 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 11.004 (20) | 8.996 |
| backlog-adp@verify-aged2-3 | 2 | +6.872 ms, 77,324 (0.773 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 10.946 (20) | 9.054 |
| backlog-adp@verify-aged2-4 | 2 | +5.936 ms, 77,207 (0.772 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 11.035 (20) | 8.965 |
| backlog-adp@verify-aged2-5 | 2 | +4.407 ms, 77,704 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 11.122 (20) | 8.878 |
| backlog-adp@verify-aged2-6 | 2 | +4.220 ms, 77,704 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 10.933 (20) | 9.067 |
| backlog-adp@verify-aged2-7 | 2 | +3.085 ms, 77,455 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 11.041 (20) | 8.959 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 10.272 (20) | 9.728 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 10.127 (20) | 9.873 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 10.241 (20) | 9.759 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 10.154 (20) | 9.846 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 10.196 (20) | 9.804 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 10.170 (20) | 9.830 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 10.262 (20) | 9.738 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 10.231 (20) | 9.769 |

Least margin over the aged windows: 8.828 ms, `backlog-adp@program-aged2-5.service.srp.last.if0` at 11.172 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.365 | 6,070 | 102 | 2 | 30.783 | yes | within |
| save-held | 2019.257 | 4,070 | 102 | - | 15.622 | no | within |
| save-starved | 4049.196 | 4,070 | 102 | - | 31.231 | yes | within |
| save | 2019.552 | 4,070 | 102 | - | 10.818 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 96,136 (0.961) | 78,214 (0.782) |
| save-second | 520 | 80,024 (0.800) | 77,945 (0.779) |
| backlog-adp@blank-0 | 299 | 92,358 (0.924) | 76,029 (0.760) |
| backlog-adp@blank-1 | 299 | 92,089 (0.921) | 76,029 (0.760) |
| backlog-adp@blank-2 | 299 | 92,166 (0.922) | 76,029 (0.760) |
| backlog-adp@blank-3 | 299 | 92,401 (0.924) | 76,029 (0.760) |
| backlog-adp@blank-4 | 299 | 92,280 (0.923) | 75,981 (0.760) |
| backlog-adp@blank-5 | 299 | 92,385 (0.924) | 76,114 (0.761) |
| backlog-adp@blank-6 | 299 | 92,050 (0.920) | 76,032 (0.760) |
| backlog-adp@blank-7 | 300 | 95,500 (0.955) | 76,032 (0.760) |
| backlog-adp@program-0 | 328 | 96,596 (0.966) | 78,710 (0.787) |
| backlog-adp@program-1 | 328 | 96,531 (0.965) | 78,679 (0.787) |
| backlog-adp@program-2 | 328 | 96,316 (0.963) | 78,679 (0.787) |
| backlog-adp@program-3 | 329 | 96,207 (0.962) | 78,679 (0.787) |
| backlog-adp@program-4 | 329 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@program-5 | 329 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@program-6 | 329 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@program-7 | 329 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-0 | 355 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-1 | 355 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-2 | 355 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-3 | 355 | 99,484 (0.995) | 78,247 (0.782) |
| backlog-adp@verify-4 | 355 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-5 | 355 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-6 | 355 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-7 | 356 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@blank-aged2-0 | 297 | 85,343 (0.853) | 75,573 (0.756) |
| backlog-adp@blank-aged2-1 | 297 | 85,389 (0.854) | 75,573 (0.756) |
| backlog-adp@blank-aged2-2 | 297 | 76,458 (0.765) | 75,410 (0.754) |
| backlog-adp@blank-aged2-3 | 297 | 76,392 (0.764) | 75,344 (0.753) |
| backlog-adp@blank-aged2-4 | 297 | 85,355 (0.854) | 75,507 (0.755) |
| backlog-adp@blank-aged2-5 | 297 | 85,497 (0.855) | 75,589 (0.756) |
| backlog-adp@blank-aged2-6 | 297 | 84,505 (0.845) | 75,574 (0.756) |
| backlog-adp@blank-aged2-7 | 298 | 91,535 (0.915) | 75,816 (0.758) |
| backlog-adp@blank-aged1-0 | 297 | 96,123 (0.961) | 75,878 (0.759) |
| backlog-adp@blank-aged1-1 | 297 | 96,640 (0.966) | 75,931 (0.759) |
| backlog-adp@blank-aged1-2 | 297 | 93,833 (0.938) | 76,183 (0.762) |
| backlog-adp@blank-aged1-3 | 297 | 92,010 (0.920) | 76,033 (0.760) |
| backlog-adp@blank-aged1-4 | 297 | 92,010 (0.920) | 76,033 (0.760) |
| backlog-adp@blank-aged1-5 | 297 | 92,087 (0.921) | 76,033 (0.760) |
| backlog-adp@blank-aged1-6 | 298 | 91,978 (0.920) | 76,033 (0.760) |
| backlog-adp@blank-aged1-7 | 297 | 76,441 (0.764) | 75,406 (0.754) |
| backlog-adp@program-aged2-0 | 326 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@program-aged2-1 | 326 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@program-aged2-2 | 326 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@program-aged2-3 | 326 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@program-aged2-4 | 326 | 95,251 (0.953) | 78,266 (0.783) |
| backlog-adp@program-aged2-5 | 326 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@program-aged2-6 | 326 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@program-aged2-7 | 327 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@program-aged1-0 | 326 | 102,254 (1.023) | 78,661 (0.787) |
| backlog-adp@program-aged1-1 | 326 | 96,225 (0.962) | 78,679 (0.787) |
| backlog-adp@program-aged1-2 | 326 | 96,019 (0.960) | 78,744 (0.787) |
| backlog-adp@program-aged1-3 | 326 | 95,954 (0.960) | 78,679 (0.787) |
| backlog-adp@program-aged1-4 | 326 | 96,031 (0.960) | 78,679 (0.787) |
| backlog-adp@program-aged1-5 | 326 | 95,922 (0.959) | 78,679 (0.787) |
| backlog-adp@program-aged1-6 | 326 | 95,922 (0.959) | 78,679 (0.787) |
| backlog-adp@program-aged1-7 | 327 | 96,276 (0.963) | 78,679 (0.787) |
| backlog-adp@verify-aged2-0 | 355 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-aged2-1 | 355 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-aged2-2 | 355 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-aged2-3 | 355 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-aged2-4 | 355 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-aged2-5 | 355 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-aged2-6 | 355 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-aged2-7 | 356 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-aged1-0 | 355 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-aged1-1 | 355 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-aged1-2 | 355 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-aged1-3 | 355 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-aged1-4 | 355 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-aged1-5 | 355 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-aged1-6 | 355 | 95,251 (0.953) | 78,247 (0.782) |
| backlog-adp@verify-aged1-7 | 356 | 95,251 (0.953) | 78,247 (0.782) |
| adp-advertise | 577 | 21,430 (0.214) | 2,573 (0.026) |
| save-held | 722 | 95,401 (0.954) | 78,369 (0.784) |
| save-starved | 418 | 80,653 (0.807) | 77,946 (0.779) |
| acmp-noresp | 615 | 95,194 (0.952) | 78,199 (0.782) |
| save | 585 | 94,626 (0.946) | 78,177 (0.782) |
| srp | 271 | 21,430 (0.214) | 2,573 (0.026) |
| backlog | 265 | 21,430 (0.214) | 2,573 (0.026) |
| backlog-adp | 271 | 21,430 (0.214) | 2,573 (0.026) |
| backlog-adp-refill | 274 | 21,430 (0.214) | 2,573 (0.026) |
| backlog-owed | 276 | 21,430 (0.214) | 2,573 (0.026) |
| acmp-disc | 305 | 95,194 (0.952) | 78,199 (0.782) |
| maap | 169 | 21,430 (0.214) | 2,573 (0.026) |
| adp-link | 79 | 21,430 (0.214) | 2,573 (0.026) |
| adp-gm | 79 | 21,430 (0.214) | 2,573 (0.026) |
| adp-discover | 79 | 21,430 (0.214) | 2,573 (0.026) |
| control | 79 | 21,430 (0.214) | 2,573 (0.026) |
| aecp-fanout | 80 | 21,430 (0.214) | 2,573 (0.026) |
| acmp-cmd | 65 | 21,430 (0.214) | 2,573 (0.026) |
| aecp | 79 | 21,430 (0.214) | 2,573 (0.026) |
| aecp-largest-notice | 78 | 21,430 (0.214) | 2,573 (0.026) |
| datapath-events | 69 | 21,430 (0.214) | 2,573 (0.026) |
| fixture | 54 | 19,907 (0.199) | 2,573 (0.026) |

Longest pass that carries a step: 102,254 CPU cycles (1.023 ms), backlog-adp@program-aged1-0; longest step: 78,744 (0.787 ms), backlog-adp@program-aged1-2.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 17,259 | 0.173 | 20 | 20 | fits | 34,316 | 19 (14) | 0.888 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 430,361 | 4.304 | 20 | 20 | fits | 119,055 | 196 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 367,983 | 3.680 | 20 | 200 | fits | 145,711 | 203 | 0.445 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 486,422 | 4.864 | 20 | 200 | fits | 119,055 | 196 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 368,907 | 3.689 | 20 | 20 | fits | 145,711 | 203 | 0.445 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 487,126 | 4.871 | 20 | 20 | fits | 119,055 | 196 | 0.384 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 226,836 | 2.268 | 20 | 24 | fits | 150,255 | 145 | 0.458 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 371,557 | 3.716 | 20 | 24 | fits | 145,711 | 203 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 371,491 | 3.715 | 20 | 50 | fits | 145,711 | 203 | 0.445 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 490,150 | 4.902 | 20 | 50 | fits | 119,055 | 196 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 578,168 | 5.782 | 20 | 20 | fits | 88,084 | 24 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,092,760 | 10.928 | 20 | 20 | fits | 80,293 | 30 | 0.675 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 361,417 | 3.614 | 20 | 20 | fits | 119,645 | 199 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 290,498 | 2.905 | 20 | 200 | fits | 145,380 | 199 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 409,527 | 4.095 | 20 | 200 | fits | 119,645 | 199 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 291,422 | 2.914 | 20 | 20 | fits | 145,380 | 199 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 410,231 | 4.102 | 20 | 20 | fits | 119,645 | 199 | 0.372 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 149,682 | 1.497 | 20 | 24 | fits | 149,775 | 145 | 0.457 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 294,072 | 2.941 | 20 | 24 | fits | 145,380 | 199 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 294,006 | 2.940 | 20 | 50 | fits | 145,380 | 199 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 413,255 | 4.133 | 20 | 50 | fits | 119,645 | 199 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 501,309 | 5.013 | 20 | 20 | fits | 88,120 | 24 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 1,016,002 | 10.160 | 20 | 20 | fits | 86,664 | 28 | 0.567 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 357,339 | 3.573 | 20 | 20 | fits | 119,393 | 197 | 0.386 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 295,081 | 2.951 | 20 | 200 | fits | 146,635 | 203 | 0.452 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 413,858 | 4.139 | 20 | 200 | fits | 119,393 | 197 | 0.386 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 296,005 | 2.960 | 20 | 20 | fits | 146,635 | 203 | 0.452 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 414,562 | 4.146 | 20 | 20 | fits | 119,393 | 197 | 0.386 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 153,010 | 1.530 | 20 | 24 | fits | 149,775 | 145 | 0.457 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 298,655 | 2.987 | 20 | 24 | fits | 146,635 | 203 | 0.452 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 298,589 | 2.986 | 20 | 50 | fits | 146,635 | 203 | 0.452 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 417,586 | 4.176 | 20 | 50 | fits | 119,393 | 197 | 0.386 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 504,799 | 5.048 | 20 | 20 | fits | 78,322 | 27 | 0.812 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 1,016,335 | 10.163 | 20 | 20 | fits | 86,454 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 373,661 | 3.737 | 20 | 20 | fits | 123,502 | 203 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 298,182 | 2.982 | 20 | 200 | fits | 146,408 | 204 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 429,900 | 4.299 | 20 | 200 | fits | 123,502 | 203 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 299,106 | 2.991 | 20 | 20 | fits | 146,408 | 204 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 430,604 | 4.306 | 20 | 20 | fits | 123,502 | 203 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 156,338 | 1.563 | 20 | 24 | fits | 149,775 | 145 | 0.457 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 301,756 | 3.018 | 20 | 24 | fits | 146,408 | 204 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 301,690 | 3.017 | 20 | 50 | fits | 146,408 | 204 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 433,628 | 4.336 | 20 | 50 | fits | 123,502 | 203 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 521,682 | 5.217 | 20 | 20 | fits | 88,120 | 24 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 1,020,111 | 10.201 | 20 | 20 | fits | 73,260 | 24 | 0.601 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 382,859 | 3.829 | 20 | 20 | fits | 119,993 | 196 | 0.393 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 303,983 | 3.040 | 20 | 200 | fits | 148,881 | 209 | 0.451 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 432,228 | 4.322 | 20 | 200 | fits | 119,993 | 196 | 0.393 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 304,907 | 3.049 | 20 | 20 | fits | 148,881 | 209 | 0.451 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 432,932 | 4.329 | 20 | 20 | fits | 119,993 | 196 | 0.393 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 159,666 | 1.597 | 20 | 24 | fits | 149,775 | 145 | 0.457 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 307,557 | 3.076 | 20 | 24 | fits | 148,881 | 209 | 0.451 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 307,491 | 3.075 | 20 | 50 | fits | 148,881 | 209 | 0.451 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 435,956 | 4.360 | 20 | 50 | fits | 119,993 | 196 | 0.393 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 524,103 | 5.241 | 20 | 20 | fits | 88,213 | 24 | 0.780 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 1,022,407 | 10.224 | 20 | 20 | fits | 73,313 | 24 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 376,779 | 3.768 | 20 | 20 | fits | 119,127 | 196 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 314,211 | 3.142 | 20 | 200 | fits | 147,613 | 208 | 0.452 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 432,722 | 4.327 | 20 | 200 | fits | 119,127 | 196 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 315,135 | 3.151 | 20 | 20 | fits | 147,613 | 208 | 0.452 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 433,426 | 4.334 | 20 | 20 | fits | 119,127 | 196 | 0.384 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 163,000 | 1.630 | 20 | 24 | fits | 149,781 | 146 | 0.457 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 317,785 | 3.178 | 20 | 24 | fits | 147,613 | 208 | 0.452 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 317,719 | 3.177 | 20 | 50 | fits | 147,613 | 208 | 0.452 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 436,450 | 4.364 | 20 | 50 | fits | 119,127 | 196 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 516,389 | 5.164 | 20 | 20 | fits | 80,005 | 26 | 0.817 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 1,036,915 | 10.369 | 20 | 20 | fits | 79,441 | 31 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 376,461 | 3.765 | 20 | 20 | fits | 127,131 | 202 | 0.411 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 299,259 | 2.993 | 20 | 200 | fits | 146,294 | 203 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 425,774 | 4.258 | 20 | 200 | fits | 127,131 | 202 | 0.411 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 300,183 | 3.002 | 20 | 20 | fits | 146,294 | 203 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 426,478 | 4.265 | 20 | 20 | fits | 127,131 | 202 | 0.411 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 157,529 | 1.575 | 20 | 24 | fits | 149,854 | 145 | 0.457 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 302,833 | 3.028 | 20 | 24 | fits | 146,294 | 203 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 302,767 | 3.028 | 20 | 50 | fits | 146,294 | 203 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 429,502 | 4.295 | 20 | 50 | fits | 127,131 | 202 | 0.411 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 517,766 | 5.178 | 20 | 20 | fits | 88,330 | 24 | 0.781 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 1,025,108 | 10.251 | 20 | 20 | fits | 73,212 | 24 | 0.601 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 372,765 | 3.728 | 20 | 20 | fits | 127,676 | 208 | 0.373 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 301,753 | 3.018 | 20 | 200 | fits | 145,460 | 197 | 0.466 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 428,813 | 4.288 | 20 | 200 | fits | 127,676 | 208 | 0.373 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 302,677 | 3.027 | 20 | 20 | fits | 145,460 | 197 | 0.466 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 429,517 | 4.295 | 20 | 20 | fits | 127,676 | 208 | 0.373 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 160,857 | 1.609 | 20 | 24 | fits | 149,854 | 145 | 0.457 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 305,327 | 3.053 | 20 | 24 | fits | 145,460 | 197 | 0.466 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 305,261 | 3.053 | 20 | 50 | fits | 145,460 | 197 | 0.466 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 432,541 | 4.325 | 20 | 50 | fits | 127,676 | 208 | 0.373 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 520,484 | 5.205 | 20 | 20 | fits | 88,009 | 24 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 1,027,824 | 10.278 | 20 | 20 | fits | 73,212 | 24 | 0.601 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 357,785 | 3.578 | 20 | 20 | fits | 119,449 | 197 | 0.387 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 295,471 | 2.955 | 20 | 200 | fits | 146,340 | 203 | 0.453 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 414,304 | 4.143 | 20 | 200 | fits | 119,449 | 197 | 0.387 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 296,395 | 2.964 | 20 | 20 | fits | 146,340 | 203 | 0.453 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 415,008 | 4.150 | 20 | 20 | fits | 119,449 | 197 | 0.387 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 153,695 | 1.537 | 20 | 24 | fits | 149,887 | 145 | 0.458 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 299,045 | 2.990 | 20 | 24 | fits | 146,340 | 203 | 0.453 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 298,979 | 2.990 | 20 | 50 | fits | 146,340 | 203 | 0.453 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 418,032 | 4.180 | 20 | 50 | fits | 119,449 | 197 | 0.387 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 518,193 | 5.182 | 20 | 20 | fits | 91,176 | 31 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 1,016,249 | 10.162 | 20 | 20 | fits | 67,180 | 26 | 0.721 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 381,989 | 3.820 | 20 | 20 | fits | 119,378 | 196 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 312,308 | 3.123 | 20 | 200 | fits | 148,050 | 208 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 431,070 | 4.311 | 20 | 200 | fits | 119,378 | 196 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 313,232 | 3.132 | 20 | 20 | fits | 148,050 | 208 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 431,774 | 4.318 | 20 | 20 | fits | 119,378 | 196 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 160,429 | 1.604 | 20 | 24 | fits | 149,965 | 146 | 0.458 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 315,882 | 3.159 | 20 | 24 | fits | 148,050 | 208 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 315,816 | 3.158 | 20 | 50 | fits | 148,050 | 208 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 434,798 | 4.348 | 20 | 50 | fits | 119,378 | 196 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 521,940 | 5.219 | 20 | 20 | fits | 87,208 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 1,036,557 | 10.366 | 20 | 20 | fits | 79,417 | 31 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 369,098 | 3.691 | 20 | 20 | fits | 119,190 | 196 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 299,678 | 2.997 | 20 | 200 | fits | 146,223 | 203 | 0.453 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 418,252 | 4.183 | 20 | 200 | fits | 119,190 | 196 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 300,602 | 3.006 | 20 | 20 | fits | 146,223 | 203 | 0.453 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 418,956 | 4.190 | 20 | 20 | fits | 119,190 | 196 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 158,019 | 1.580 | 20 | 24 | fits | 149,828 | 145 | 0.457 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 303,252 | 3.033 | 20 | 24 | fits | 146,223 | 203 | 0.453 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 303,186 | 3.032 | 20 | 50 | fits | 146,223 | 203 | 0.453 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 421,980 | 4.220 | 20 | 50 | fits | 119,190 | 196 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 501,183 | 5.012 | 20 | 20 | fits | 79,269 | 26 | 0.814 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 1,021,965 | 10.220 | 20 | 20 | fits | 86,454 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 367,163 | 3.672 | 20 | 20 | fits | 124,929 | 218 | 0.376 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 292,105 | 2.921 | 20 | 200 | fits | 148,036 | 185 | 0.475 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 416,418 | 4.164 | 20 | 200 | fits | 124,929 | 218 | 0.376 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 293,029 | 2.930 | 20 | 20 | fits | 148,036 | 185 | 0.475 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 417,122 | 4.171 | 20 | 20 | fits | 124,929 | 218 | 0.376 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 148,633 | 1.486 | 20 | 24 | fits | 149,827 | 145 | 0.458 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 295,679 | 2.957 | 20 | 24 | fits | 148,036 | 185 | 0.475 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 295,613 | 2.956 | 20 | 50 | fits | 148,036 | 185 | 0.475 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 420,146 | 4.201 | 20 | 50 | fits | 124,929 | 218 | 0.376 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 507,461 | 5.075 | 20 | 20 | fits | 87,381 | 25 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 1,014,493 | 10.145 | 20 | 20 | fits | 73,337 | 24 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 381,082 | 3.811 | 20 | 20 | fits | 124,327 | 206 | 0.404 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 297,068 | 2.971 | 20 | 200 | fits | 145,147 | 200 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 429,736 | 4.297 | 20 | 200 | fits | 124,327 | 206 | 0.404 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 297,992 | 2.980 | 20 | 20 | fits | 145,147 | 200 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 430,440 | 4.304 | 20 | 20 | fits | 124,327 | 206 | 0.404 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 156,485 | 1.565 | 20 | 24 | fits | 150,072 | 145 | 0.456 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 300,642 | 3.006 | 20 | 24 | fits | 145,147 | 200 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 300,576 | 3.006 | 20 | 50 | fits | 145,147 | 200 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 433,464 | 4.335 | 20 | 50 | fits | 124,327 | 206 | 0.404 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 520,707 | 5.207 | 20 | 20 | fits | 87,309 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 1,018,746 | 10.187 | 20 | 20 | fits | 67,368 | 26 | 0.725 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 358,931 | 3.589 | 20 | 20 | fits | 118,737 | 196 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 296,278 | 2.963 | 20 | 200 | fits | 145,712 | 203 | 0.449 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 414,399 | 4.144 | 20 | 200 | fits | 118,737 | 196 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 297,202 | 2.972 | 20 | 20 | fits | 145,712 | 203 | 0.449 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 415,103 | 4.151 | 20 | 20 | fits | 118,737 | 196 | 0.379 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 155,130 | 1.551 | 20 | 24 | fits | 149,877 | 145 | 0.458 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 299,852 | 2.999 | 20 | 24 | fits | 145,712 | 203 | 0.449 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 299,786 | 2.998 | 20 | 50 | fits | 145,712 | 203 | 0.449 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 418,127 | 4.181 | 20 | 50 | fits | 118,737 | 196 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 505,258 | 5.053 | 20 | 20 | fits | 87,197 | 24 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 1,019,786 | 10.198 | 20 | 20 | fits | 86,454 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 365,401 | 3.654 | 20 | 20 | fits | 119,015 | 196 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 302,613 | 3.026 | 20 | 200 | fits | 145,391 | 203 | 0.446 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 421,012 | 4.210 | 20 | 200 | fits | 119,015 | 196 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 303,537 | 3.035 | 20 | 20 | fits | 145,391 | 203 | 0.446 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 421,716 | 4.217 | 20 | 20 | fits | 119,015 | 196 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 161,786 | 1.618 | 20 | 24 | fits | 149,877 | 145 | 0.458 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 306,187 | 3.062 | 20 | 24 | fits | 145,391 | 203 | 0.446 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 306,121 | 3.061 | 20 | 50 | fits | 145,391 | 203 | 0.446 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 424,740 | 4.247 | 20 | 50 | fits | 119,015 | 196 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 503,904 | 5.039 | 20 | 20 | fits | 79,230 | 27 | 0.811 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 1,024,375 | 10.244 | 20 | 20 | fits | 86,531 | 28 | 0.560 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 376,949 | 3.769 | 20 | 20 | fits | 131,583 | 214 | 0.397 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 293,419 | 2.934 | 20 | 200 | fits | 145,581 | 198 | 0.469 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 433,331 | 4.333 | 20 | 200 | fits | 131,583 | 214 | 0.397 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 294,343 | 2.943 | 20 | 20 | fits | 145,581 | 198 | 0.469 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 434,035 | 4.340 | 20 | 20 | fits | 131,583 | 214 | 0.397 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 152,402 | 1.524 | 20 | 24 | fits | 149,878 | 145 | 0.458 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 296,993 | 2.970 | 20 | 24 | fits | 145,581 | 198 | 0.469 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 296,927 | 2.969 | 20 | 50 | fits | 145,581 | 198 | 0.469 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 437,059 | 4.371 | 20 | 50 | fits | 131,583 | 214 | 0.397 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 524,273 | 5.243 | 20 | 20 | fits | 87,280 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 1,015,018 | 10.150 | 20 | 20 | fits | 59,802 | 20 | 0.655 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 395,077 | 3.951 | 20 | 20 | fits | 119,222 | 196 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 325,670 | 3.257 | 20 | 200 | fits | 146,078 | 203 | 0.451 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 444,276 | 4.443 | 20 | 200 | fits | 119,222 | 196 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 326,594 | 3.266 | 20 | 20 | fits | 146,078 | 203 | 0.451 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 444,980 | 4.450 | 20 | 20 | fits | 119,222 | 196 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 184,156 | 1.842 | 20 | 24 | fits | 150,540 | 145 | 0.460 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 329,244 | 3.292 | 20 | 24 | fits | 146,078 | 203 | 0.451 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 329,178 | 3.292 | 20 | 50 | fits | 146,078 | 203 | 0.451 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 448,004 | 4.480 | 20 | 50 | fits | 119,222 | 196 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 535,464 | 5.355 | 20 | 20 | fits | 87,526 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,051,975 | 10.520 | 20 | 20 | fits | 80,519 | 30 | 0.679 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 359,086 | 3.591 | 20 | 20 | fits | 118,737 | 196 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 296,433 | 2.964 | 20 | 200 | fits | 145,861 | 203 | 0.449 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 414,554 | 4.146 | 20 | 200 | fits | 118,737 | 196 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 297,357 | 2.974 | 20 | 20 | fits | 145,861 | 203 | 0.449 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 415,258 | 4.153 | 20 | 20 | fits | 118,737 | 196 | 0.379 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 155,136 | 1.551 | 20 | 24 | fits | 149,888 | 145 | 0.458 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 300,007 | 3.000 | 20 | 24 | fits | 145,861 | 203 | 0.449 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 299,941 | 2.999 | 20 | 50 | fits | 145,861 | 203 | 0.449 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 418,282 | 4.183 | 20 | 50 | fits | 118,737 | 196 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 505,878 | 5.059 | 20 | 20 | fits | 87,662 | 25 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 1,020,090 | 10.201 | 20 | 20 | fits | 86,720 | 28 | 0.569 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 362,176 | 3.622 | 20 | 20 | fits | 119,436 | 197 | 0.387 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 299,875 | 2.999 | 20 | 200 | fits | 145,975 | 203 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 418,695 | 4.187 | 20 | 200 | fits | 119,436 | 197 | 0.387 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 300,799 | 3.008 | 20 | 20 | fits | 145,975 | 203 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 419,399 | 4.194 | 20 | 20 | fits | 119,436 | 197 | 0.387 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 158,464 | 1.585 | 20 | 24 | fits | 149,888 | 145 | 0.458 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 303,449 | 3.034 | 20 | 24 | fits | 145,975 | 203 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 303,383 | 3.034 | 20 | 50 | fits | 145,975 | 203 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 422,423 | 4.224 | 20 | 50 | fits | 119,436 | 197 | 0.387 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 522,561 | 5.226 | 20 | 20 | fits | 91,330 | 31 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 1,020,909 | 10.209 | 20 | 20 | fits | 73,337 | 24 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 378,643 | 3.786 | 20 | 20 | fits | 123,549 | 203 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 303,032 | 3.030 | 20 | 200 | fits | 145,804 | 204 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 434,798 | 4.348 | 20 | 200 | fits | 123,549 | 203 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 303,956 | 3.040 | 20 | 20 | fits | 145,804 | 204 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 435,502 | 4.355 | 20 | 20 | fits | 123,549 | 203 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 161,792 | 1.618 | 20 | 24 | fits | 149,888 | 145 | 0.458 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 306,606 | 3.066 | 20 | 24 | fits | 145,804 | 204 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 306,540 | 3.065 | 20 | 50 | fits | 145,804 | 204 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 438,526 | 4.385 | 20 | 50 | fits | 123,549 | 203 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 525,984 | 5.260 | 20 | 20 | fits | 87,524 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 1,024,226 | 10.242 | 20 | 20 | fits | 73,260 | 24 | 0.601 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 363,524 | 3.635 | 20 | 20 | fits | 119,240 | 196 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 300,981 | 3.010 | 20 | 200 | fits | 148,088 | 208 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 419,605 | 4.196 | 20 | 200 | fits | 119,240 | 196 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 301,905 | 3.019 | 20 | 20 | fits | 148,088 | 208 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 420,309 | 4.203 | 20 | 20 | fits | 119,240 | 196 | 0.384 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 149,158 | 1.492 | 20 | 24 | fits | 149,967 | 146 | 0.457 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 304,555 | 3.046 | 20 | 24 | fits | 148,088 | 208 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 304,489 | 3.045 | 20 | 50 | fits | 148,088 | 208 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 423,333 | 4.233 | 20 | 50 | fits | 119,240 | 196 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 502,655 | 5.027 | 20 | 20 | fits | 79,388 | 26 | 0.813 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 1,023,277 | 10.233 | 20 | 20 | fits | 79,489 | 31 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 361,326 | 3.613 | 20 | 20 | fits | 127,024 | 202 | 0.411 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 290,743 | 2.907 | 20 | 200 | fits | 147,113 | 208 | 0.447 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 417,151 | 4.172 | 20 | 200 | fits | 127,024 | 202 | 0.411 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 291,667 | 2.917 | 20 | 20 | fits | 147,113 | 208 | 0.447 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 417,855 | 4.179 | 20 | 20 | fits | 127,024 | 202 | 0.411 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 148,194 | 1.482 | 20 | 24 | fits | 150,436 | 145 | 0.462 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 294,317 | 2.943 | 20 | 24 | fits | 147,113 | 208 | 0.447 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 294,251 | 2.943 | 20 | 50 | fits | 147,113 | 208 | 0.447 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 420,879 | 4.209 | 20 | 50 | fits | 127,024 | 202 | 0.411 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 508,583 | 5.086 | 20 | 20 | fits | 87,770 | 24 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 1,016,149 | 10.161 | 20 | 20 | fits | 73,628 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 381,374 | 3.814 | 20 | 20 | fits | 124,929 | 218 | 0.376 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 306,316 | 3.063 | 20 | 200 | fits | 148,036 | 185 | 0.475 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 430,629 | 4.306 | 20 | 200 | fits | 124,929 | 218 | 0.376 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 307,240 | 3.072 | 20 | 20 | fits | 148,036 | 185 | 0.475 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 431,333 | 4.313 | 20 | 20 | fits | 124,929 | 218 | 0.376 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 162,844 | 1.628 | 20 | 24 | fits | 149,827 | 145 | 0.458 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 309,890 | 3.099 | 20 | 24 | fits | 148,036 | 185 | 0.475 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 309,824 | 3.098 | 20 | 50 | fits | 148,036 | 185 | 0.475 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 434,357 | 4.344 | 20 | 50 | fits | 124,929 | 218 | 0.376 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 521,659 | 5.217 | 20 | 20 | fits | 87,368 | 24 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 1,029,164 | 10.292 | 20 | 20 | fits | 73,337 | 24 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 361,925 | 3.619 | 20 | 20 | fits | 127,111 | 208 | 0.367 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 291,060 | 2.911 | 20 | 200 | fits | 145,492 | 197 | 0.469 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 417,555 | 4.176 | 20 | 200 | fits | 127,111 | 208 | 0.367 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 291,984 | 2.920 | 20 | 20 | fits | 145,492 | 197 | 0.469 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 418,259 | 4.183 | 20 | 20 | fits | 127,111 | 208 | 0.367 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 150,132 | 1.501 | 20 | 24 | fits | 149,828 | 145 | 0.457 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 294,634 | 2.946 | 20 | 24 | fits | 145,492 | 197 | 0.469 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 294,568 | 2.946 | 20 | 50 | fits | 145,492 | 197 | 0.469 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 421,283 | 4.213 | 20 | 50 | fits | 127,111 | 208 | 0.367 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 508,712 | 5.087 | 20 | 20 | fits | 87,495 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 1,016,205 | 10.162 | 20 | 20 | fits | 73,260 | 24 | 0.601 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 375,545 | 3.755 | 20 | 20 | fits | 124,035 | 205 | 0.404 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 291,376 | 2.914 | 20 | 200 | fits | 146,277 | 205 | 0.453 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 424,166 | 4.242 | 20 | 200 | fits | 124,035 | 205 | 0.404 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 292,300 | 2.923 | 20 | 20 | fits | 146,277 | 205 | 0.453 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 424,870 | 4.249 | 20 | 20 | fits | 124,035 | 205 | 0.404 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 149,663 | 1.497 | 20 | 24 | fits | 152,657 | 147 | 0.477 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 294,950 | 2.950 | 20 | 24 | fits | 146,277 | 205 | 0.453 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 294,884 | 2.949 | 20 | 50 | fits | 146,277 | 205 | 0.453 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 427,894 | 4.279 | 20 | 50 | fits | 124,035 | 205 | 0.404 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 515,075 | 5.151 | 20 | 20 | fits | 87,247 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 1,012,977 | 10.130 | 20 | 20 | fits | 67,463 | 27 | 0.724 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 372,159 | 3.722 | 20 | 20 | fits | 122,919 | 205 | 0.390 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 298,182 | 2.982 | 20 | 200 | fits | 146,386 | 204 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 420,485 | 4.205 | 20 | 200 | fits | 122,919 | 205 | 0.390 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 299,106 | 2.991 | 20 | 20 | fits | 146,386 | 204 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 421,189 | 4.212 | 20 | 20 | fits | 122,919 | 205 | 0.390 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 147,126 | 1.471 | 20 | 24 | fits | 149,062 | 143 | 0.455 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 301,756 | 3.018 | 20 | 24 | fits | 146,386 | 204 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 301,690 | 3.017 | 20 | 50 | fits | 146,386 | 204 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 424,213 | 4.242 | 20 | 50 | fits | 122,919 | 205 | 0.390 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 511,254 | 5.113 | 20 | 20 | fits | 87,107 | 24 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 1,101,105 | 11.011 | 20 | 20 | fits | 79,727 | 31 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 373,176 | 3.732 | 20 | 20 | fits | 118,753 | 196 | 0.381 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 311,050 | 3.111 | 20 | 200 | fits | 145,607 | 203 | 0.447 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 429,187 | 4.292 | 20 | 200 | fits | 118,753 | 196 | 0.381 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 311,974 | 3.120 | 20 | 20 | fits | 145,607 | 203 | 0.447 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 429,891 | 4.299 | 20 | 20 | fits | 118,753 | 196 | 0.381 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 170,007 | 1.700 | 20 | 24 | fits | 148,909 | 143 | 0.456 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 314,624 | 3.146 | 20 | 24 | fits | 145,607 | 203 | 0.447 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 314,558 | 3.146 | 20 | 50 | fits | 145,607 | 203 | 0.447 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 432,915 | 4.329 | 20 | 50 | fits | 118,753 | 196 | 0.381 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 519,998 | 5.200 | 20 | 20 | fits | 87,149 | 24 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,112,464 | 11.125 | 20 | 20 | fits | 86,689 | 28 | 0.571 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 362,453 | 3.625 | 20 | 20 | fits | 119,182 | 196 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 293,008 | 2.930 | 20 | 200 | fits | 145,780 | 203 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 411,574 | 4.116 | 20 | 200 | fits | 119,182 | 196 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 293,932 | 2.939 | 20 | 20 | fits | 145,780 | 203 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 412,278 | 4.123 | 20 | 20 | fits | 119,182 | 196 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 151,792 | 1.518 | 20 | 24 | fits | 148,919 | 142 | 0.454 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 296,582 | 2.966 | 20 | 24 | fits | 145,780 | 203 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 296,516 | 2.965 | 20 | 50 | fits | 145,780 | 203 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 415,302 | 4.153 | 20 | 50 | fits | 119,182 | 196 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 502,441 | 5.024 | 20 | 20 | fits | 87,205 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,094,926 | 10.949 | 20 | 20 | fits | 86,475 | 28 | 0.560 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 349,854 | 3.499 | 20 | 20 | fits | 118,744 | 196 | 0.382 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 287,156 | 2.872 | 20 | 200 | fits | 146,635 | 208 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 405,284 | 4.053 | 20 | 200 | fits | 118,744 | 196 | 0.382 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 288,080 | 2.881 | 20 | 20 | fits | 146,635 | 208 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 405,988 | 4.060 | 20 | 20 | fits | 118,744 | 196 | 0.382 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 145,085 | 1.451 | 20 | 24 | fits | 148,681 | 142 | 0.452 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 290,730 | 2.907 | 20 | 24 | fits | 146,635 | 208 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 290,664 | 2.907 | 20 | 50 | fits | 146,635 | 208 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 409,012 | 4.090 | 20 | 50 | fits | 118,744 | 196 | 0.382 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 496,101 | 4.961 | 20 | 20 | fits | 87,155 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,085,749 | 10.857 | 20 | 20 | fits | 86,398 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 366,210 | 3.662 | 20 | 20 | fits | 119,182 | 196 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 296,765 | 2.968 | 20 | 200 | fits | 145,780 | 203 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 415,331 | 4.153 | 20 | 200 | fits | 119,182 | 196 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 297,689 | 2.977 | 20 | 20 | fits | 145,780 | 203 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 416,035 | 4.160 | 20 | 20 | fits | 119,182 | 196 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 155,549 | 1.555 | 20 | 24 | fits | 148,681 | 142 | 0.452 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 300,339 | 3.003 | 20 | 24 | fits | 145,780 | 203 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 300,273 | 3.003 | 20 | 50 | fits | 145,780 | 203 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 419,059 | 4.191 | 20 | 50 | fits | 119,182 | 196 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 501,921 | 5.019 | 20 | 20 | fits | 82,928 | 33 | 0.805 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,094,595 | 10.946 | 20 | 20 | fits | 73,289 | 24 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 363,965 | 3.640 | 20 | 20 | fits | 129,972 | 209 | 0.411 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 290,029 | 2.900 | 20 | 200 | fits | 145,275 | 203 | 0.446 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 419,385 | 4.194 | 20 | 200 | fits | 129,972 | 209 | 0.411 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 290,953 | 2.910 | 20 | 20 | fits | 145,275 | 203 | 0.446 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 420,089 | 4.201 | 20 | 20 | fits | 129,972 | 209 | 0.411 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 149,318 | 1.493 | 20 | 24 | fits | 148,919 | 142 | 0.454 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 293,603 | 2.936 | 20 | 24 | fits | 145,275 | 203 | 0.446 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 293,537 | 2.935 | 20 | 50 | fits | 145,275 | 203 | 0.446 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 423,113 | 4.231 | 20 | 50 | fits | 129,972 | 209 | 0.411 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 595,884 | 5.959 | 20 | 20 | fits | 88,332 | 25 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,086,216 | 10.862 | 20 | 20 | fits | 59,762 | 20 | 0.655 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 467,320 | 4.673 | 20 | 20 | fits | 129,910 | 224 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 303,678 | 3.037 | 20 | 200 | fits | 148,460 | 186 | 0.479 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 517,339 | 5.173 | 20 | 200 | fits | 129,910 | 224 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 304,602 | 3.046 | 20 | 20 | fits | 148,460 | 186 | 0.479 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 518,043 | 5.180 | 20 | 20 | fits | 129,910 | 224 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 159,782 | 1.598 | 20 | 24 | fits | 148,919 | 142 | 0.454 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 307,252 | 3.073 | 20 | 24 | fits | 148,460 | 186 | 0.479 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 307,186 | 3.072 | 20 | 50 | fits | 148,460 | 186 | 0.479 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 521,067 | 5.211 | 20 | 50 | fits | 129,910 | 224 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 608,189 | 6.082 | 20 | 20 | fits | 87,188 | 24 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,098,289 | 10.983 | 20 | 20 | fits | 59,762 | 20 | 0.655 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 360,431 | 3.604 | 20 | 20 | fits | 119,239 | 196 | 0.382 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 290,962 | 2.910 | 20 | 200 | fits | 146,057 | 203 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 409,585 | 4.096 | 20 | 200 | fits | 119,239 | 196 | 0.382 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 291,886 | 2.919 | 20 | 20 | fits | 146,057 | 203 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 410,289 | 4.103 | 20 | 20 | fits | 119,239 | 196 | 0.382 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 149,469 | 1.495 | 20 | 24 | fits | 148,747 | 142 | 0.451 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 294,536 | 2.945 | 20 | 24 | fits | 146,057 | 203 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 294,470 | 2.945 | 20 | 50 | fits | 146,057 | 203 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 413,313 | 4.133 | 20 | 50 | fits | 119,239 | 196 | 0.382 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 501,314 | 5.013 | 20 | 20 | fits | 88,067 | 25 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 1,020,536 | 10.205 | 20 | 20 | fits | 85,848 | 30 | 0.704 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 363,303 | 3.633 | 20 | 20 | fits | 119,135 | 197 | 0.386 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 300,976 | 3.010 | 20 | 200 | fits | 145,479 | 203 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 419,495 | 4.195 | 20 | 200 | fits | 119,135 | 197 | 0.386 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 301,900 | 3.019 | 20 | 20 | fits | 145,479 | 203 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 420,199 | 4.202 | 20 | 20 | fits | 119,135 | 197 | 0.386 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 160,061 | 1.601 | 20 | 24 | fits | 148,747 | 142 | 0.451 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 304,550 | 3.046 | 20 | 24 | fits | 145,479 | 203 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 304,484 | 3.045 | 20 | 50 | fits | 145,479 | 203 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 423,223 | 4.232 | 20 | 50 | fits | 119,135 | 197 | 0.386 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 510,385 | 5.104 | 20 | 20 | fits | 78,214 | 27 | 0.812 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 1,059,997 | 10.600 | 20 | 20 | fits | 89,668 | 29 | 0.646 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 377,432 | 3.774 | 20 | 20 | fits | 123,450 | 203 | 0.410 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 295,471 | 2.955 | 20 | 200 | fits | 146,093 | 204 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 427,126 | 4.271 | 20 | 200 | fits | 123,450 | 203 | 0.410 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 296,395 | 2.964 | 20 | 20 | fits | 146,093 | 204 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 427,830 | 4.278 | 20 | 20 | fits | 123,450 | 203 | 0.410 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 153,942 | 1.539 | 20 | 24 | fits | 148,985 | 142 | 0.453 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 299,045 | 2.990 | 20 | 24 | fits | 146,093 | 204 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 298,979 | 2.990 | 20 | 50 | fits | 146,093 | 204 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 430,854 | 4.309 | 20 | 50 | fits | 123,450 | 203 | 0.410 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 518,753 | 5.188 | 20 | 20 | fits | 87,965 | 24 | 0.778 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 1,085,801 | 10.858 | 20 | 20 | fits | 73,465 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 363,164 | 3.632 | 20 | 20 | fits | 122,023 | 202 | 0.398 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 297,510 | 2.975 | 20 | 200 | fits | 146,759 | 208 | 0.447 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 418,917 | 4.189 | 20 | 200 | fits | 122,023 | 202 | 0.398 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 298,434 | 2.984 | 20 | 20 | fits | 146,759 | 208 | 0.447 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 419,621 | 4.196 | 20 | 20 | fits | 122,023 | 202 | 0.398 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 146,752 | 1.468 | 20 | 24 | fits | 148,696 | 143 | 0.451 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 301,084 | 3.011 | 20 | 24 | fits | 146,759 | 208 | 0.447 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 301,018 | 3.010 | 20 | 50 | fits | 146,759 | 208 | 0.447 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 422,645 | 4.226 | 20 | 50 | fits | 122,023 | 202 | 0.398 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 510,498 | 5.105 | 20 | 20 | fits | 87,919 | 24 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 1,094,631 | 10.946 | 20 | 20 | fits | 86,870 | 28 | 0.577 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 360,436 | 3.604 | 20 | 20 | fits | 118,970 | 196 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 298,137 | 2.981 | 20 | 200 | fits | 145,973 | 203 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 416,491 | 4.165 | 20 | 200 | fits | 118,970 | 196 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 299,061 | 2.991 | 20 | 20 | fits | 145,973 | 203 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 417,195 | 4.172 | 20 | 20 | fits | 118,970 | 196 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 156,728 | 1.567 | 20 | 24 | fits | 148,969 | 142 | 0.453 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 301,711 | 3.017 | 20 | 24 | fits | 145,973 | 203 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 301,645 | 3.016 | 20 | 50 | fits | 145,973 | 203 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 420,219 | 4.202 | 20 | 50 | fits | 118,970 | 196 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 508,048 | 5.080 | 20 | 20 | fits | 87,895 | 24 | 0.778 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 1,093,296 | 10.933 | 20 | 20 | fits | 86,551 | 28 | 0.565 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 353,916 | 3.539 | 20 | 20 | fits | 118,467 | 196 | 0.378 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 291,397 | 2.914 | 20 | 200 | fits | 145,940 | 203 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 409,248 | 4.092 | 20 | 200 | fits | 118,467 | 196 | 0.378 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 292,321 | 2.923 | 20 | 20 | fits | 145,940 | 203 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 409,952 | 4.100 | 20 | 20 | fits | 118,467 | 196 | 0.378 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 150,021 | 1.500 | 20 | 24 | fits | 148,667 | 142 | 0.451 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 294,971 | 2.950 | 20 | 24 | fits | 145,940 | 203 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 294,905 | 2.949 | 20 | 50 | fits | 145,940 | 203 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 412,976 | 4.130 | 20 | 50 | fits | 118,467 | 196 | 0.378 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 497,254 | 4.973 | 20 | 20 | fits | 84,344 | 26 | 0.825 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 1,083,737 | 10.837 | 20 | 20 | fits | 86,398 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 378,478 | 3.785 | 20 | 20 | fits | 134,524 | 202 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 301,894 | 3.019 | 20 | 200 | fits | 145,973 | 203 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 435,802 | 4.358 | 20 | 200 | fits | 134,524 | 202 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 302,818 | 3.028 | 20 | 20 | fits | 145,973 | 203 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 436,506 | 4.365 | 20 | 20 | fits | 134,524 | 202 | 0.446 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 160,485 | 1.605 | 20 | 24 | fits | 148,667 | 142 | 0.451 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 305,468 | 3.055 | 20 | 24 | fits | 145,973 | 203 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 305,402 | 3.054 | 20 | 50 | fits | 145,973 | 203 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 439,530 | 4.395 | 20 | 50 | fits | 134,524 | 202 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 554,549 | 5.545 | 20 | 20 | fits | 87,313 | 26 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 1,091,483 | 10.915 | 20 | 20 | fits | 73,289 | 24 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 380,595 | 3.806 | 20 | 20 | fits | 134,022 | 234 | 0.360 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 295,514 | 2.955 | 20 | 200 | fits | 145,824 | 170 | 0.526 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 428,920 | 4.289 | 20 | 200 | fits | 134,022 | 234 | 0.360 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 296,438 | 2.964 | 20 | 20 | fits | 145,824 | 170 | 0.526 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 429,624 | 4.296 | 20 | 20 | fits | 134,022 | 234 | 0.360 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 154,254 | 1.543 | 20 | 24 | fits | 148,905 | 142 | 0.453 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 299,088 | 2.991 | 20 | 24 | fits | 145,824 | 170 | 0.526 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 299,022 | 2.990 | 20 | 50 | fits | 145,824 | 170 | 0.526 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 432,648 | 4.326 | 20 | 50 | fits | 134,022 | 234 | 0.360 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 547,319 | 5.473 | 20 | 20 | fits | 78,402 | 27 | 0.818 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 1,082,993 | 10.830 | 20 | 20 | fits | 73,289 | 24 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 379,332 | 3.793 | 20 | 20 | fits | 119,444 | 196 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 309,630 | 3.096 | 20 | 200 | fits | 147,739 | 208 | 0.451 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 428,458 | 4.285 | 20 | 200 | fits | 119,444 | 196 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 310,554 | 3.106 | 20 | 20 | fits | 147,739 | 208 | 0.451 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 429,162 | 4.292 | 20 | 20 | fits | 119,444 | 196 | 0.384 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 157,876 | 1.579 | 20 | 24 | fits | 149,104 | 143 | 0.454 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 313,204 | 3.132 | 20 | 24 | fits | 147,739 | 208 | 0.451 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 313,138 | 3.131 | 20 | 50 | fits | 147,739 | 208 | 0.451 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 432,186 | 4.322 | 20 | 50 | fits | 119,444 | 196 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 519,245 | 5.192 | 20 | 20 | fits | 87,125 | 24 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 1,031,877 | 10.319 | 20 | 20 | fits | 71,816 | 33 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 354,073 | 3.541 | 20 | 20 | fits | 118,647 | 196 | 0.378 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 291,426 | 2.914 | 20 | 200 | fits | 145,956 | 203 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 409,457 | 4.095 | 20 | 200 | fits | 118,647 | 196 | 0.378 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 292,350 | 2.924 | 20 | 20 | fits | 145,956 | 203 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 410,161 | 4.102 | 20 | 20 | fits | 118,647 | 196 | 0.378 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 150,034 | 1.500 | 20 | 24 | fits | 148,860 | 142 | 0.452 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 295,000 | 2.950 | 20 | 24 | fits | 145,956 | 203 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 294,934 | 2.949 | 20 | 50 | fits | 145,956 | 203 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 413,185 | 4.132 | 20 | 50 | fits | 118,647 | 196 | 0.378 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 500,222 | 5.002 | 20 | 20 | fits | 87,103 | 24 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 1,095,916 | 10.959 | 20 | 20 | fits | 87,354 | 29 | 0.580 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 364,470 | 3.645 | 20 | 20 | fits | 119,150 | 196 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 302,051 | 3.021 | 20 | 200 | fits | 145,989 | 203 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 420,585 | 4.206 | 20 | 200 | fits | 119,150 | 196 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 302,975 | 3.030 | 20 | 20 | fits | 145,989 | 203 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 421,289 | 4.213 | 20 | 20 | fits | 119,150 | 196 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 160,626 | 1.606 | 20 | 24 | fits | 148,860 | 142 | 0.452 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 305,625 | 3.056 | 20 | 24 | fits | 145,989 | 203 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 305,559 | 3.056 | 20 | 50 | fits | 145,989 | 203 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 424,313 | 4.243 | 20 | 50 | fits | 119,150 | 196 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 511,350 | 5.114 | 20 | 20 | fits | 87,103 | 24 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,107,292 | 11.073 | 20 | 20 | fits | 86,531 | 28 | 0.560 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 358,546 | 3.585 | 20 | 20 | fits | 118,647 | 196 | 0.378 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 295,899 | 2.959 | 20 | 200 | fits | 145,956 | 203 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 413,930 | 4.139 | 20 | 200 | fits | 118,647 | 196 | 0.378 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 296,823 | 2.968 | 20 | 20 | fits | 145,956 | 203 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 414,634 | 4.146 | 20 | 20 | fits | 118,647 | 196 | 0.378 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 154,507 | 1.545 | 20 | 24 | fits | 149,098 | 142 | 0.454 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 299,473 | 2.995 | 20 | 24 | fits | 145,956 | 203 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 299,407 | 2.994 | 20 | 50 | fits | 145,956 | 203 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 417,658 | 4.177 | 20 | 50 | fits | 118,647 | 196 | 0.378 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 504,917 | 5.049 | 20 | 20 | fits | 87,325 | 25 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,100,163 | 11.002 | 20 | 20 | fits | 86,454 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 351,636 | 3.516 | 20 | 20 | fits | 119,395 | 197 | 0.387 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 289,154 | 2.892 | 20 | 200 | fits | 146,802 | 208 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 407,933 | 4.079 | 20 | 200 | fits | 119,395 | 197 | 0.387 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 290,078 | 2.901 | 20 | 20 | fits | 146,802 | 208 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 408,637 | 4.086 | 20 | 20 | fits | 119,395 | 197 | 0.387 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 146,916 | 1.469 | 20 | 24 | fits | 148,860 | 142 | 0.452 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 292,728 | 2.927 | 20 | 24 | fits | 146,802 | 208 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 292,662 | 2.927 | 20 | 50 | fits | 146,802 | 208 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 411,661 | 4.117 | 20 | 50 | fits | 119,395 | 197 | 0.387 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 511,584 | 5.116 | 20 | 20 | fits | 91,206 | 31 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,091,207 | 10.912 | 20 | 20 | fits | 73,337 | 24 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 389,923 | 3.899 | 20 | 20 | fits | 131,728 | 212 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 298,901 | 2.989 | 20 | 200 | fits | 144,961 | 200 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 438,673 | 4.387 | 20 | 200 | fits | 131,728 | 212 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 299,825 | 2.998 | 20 | 20 | fits | 144,961 | 200 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 439,377 | 4.394 | 20 | 20 | fits | 131,728 | 212 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 158,504 | 1.585 | 20 | 24 | fits | 148,860 | 142 | 0.452 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 302,475 | 3.025 | 20 | 24 | fits | 144,961 | 200 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 302,409 | 3.024 | 20 | 50 | fits | 144,961 | 200 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 442,401 | 4.424 | 20 | 50 | fits | 131,728 | 212 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 609,902 | 6.099 | 20 | 20 | fits | 87,372 | 25 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,117,182 | 11.172 | 20 | 20 | fits | 66,415 | 27 | 0.735 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 373,803 | 3.738 | 20 | 20 | fits | 127,110 | 202 | 0.413 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 303,523 | 3.035 | 20 | 200 | fits | 147,210 | 208 | 0.449 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 430,017 | 4.300 | 20 | 200 | fits | 127,110 | 202 | 0.413 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 304,447 | 3.044 | 20 | 20 | fits | 147,210 | 208 | 0.449 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 430,721 | 4.307 | 20 | 20 | fits | 127,110 | 202 | 0.413 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 152,436 | 1.524 | 20 | 24 | fits | 149,149 | 143 | 0.454 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 307,097 | 3.071 | 20 | 24 | fits | 147,210 | 208 | 0.449 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 307,031 | 3.070 | 20 | 50 | fits | 147,210 | 208 | 0.449 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 433,745 | 4.337 | 20 | 50 | fits | 127,110 | 202 | 0.413 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 601,139 | 6.011 | 20 | 20 | fits | 87,265 | 25 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,108,995 | 11.090 | 20 | 20 | fits | 73,628 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 459,556 | 4.596 | 20 | 20 | fits | 125,049 | 218 | 0.378 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 304,747 | 3.047 | 20 | 200 | fits | 148,113 | 185 | 0.475 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 509,146 | 5.091 | 20 | 200 | fits | 125,049 | 218 | 0.378 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 305,671 | 3.057 | 20 | 20 | fits | 148,113 | 185 | 0.475 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 509,850 | 5.098 | 20 | 20 | fits | 125,049 | 218 | 0.378 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 161,198 | 1.612 | 20 | 24 | fits | 149,243 | 142 | 0.455 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 308,321 | 3.083 | 20 | 24 | fits | 148,113 | 185 | 0.475 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 308,255 | 3.083 | 20 | 50 | fits | 148,113 | 185 | 0.475 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 512,874 | 5.129 | 20 | 50 | fits | 125,049 | 218 | 0.378 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 600,156 | 6.002 | 20 | 20 | fits | 87,348 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,107,782 | 11.078 | 20 | 20 | fits | 73,337 | 24 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 373,322 | 3.733 | 20 | 20 | fits | 123,672 | 203 | 0.413 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 297,704 | 2.977 | 20 | 200 | fits | 145,802 | 204 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 429,640 | 4.296 | 20 | 200 | fits | 123,672 | 203 | 0.413 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 298,628 | 2.986 | 20 | 20 | fits | 145,802 | 204 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 430,344 | 4.303 | 20 | 20 | fits | 123,672 | 203 | 0.413 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 156,466 | 1.565 | 20 | 24 | fits | 149,098 | 142 | 0.454 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 301,278 | 3.013 | 20 | 24 | fits | 145,802 | 204 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 301,212 | 3.012 | 20 | 50 | fits | 145,802 | 204 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 433,368 | 4.334 | 20 | 50 | fits | 123,672 | 203 | 0.413 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 520,667 | 5.207 | 20 | 20 | fits | 87,365 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 1,018,712 | 10.187 | 20 | 20 | fits | 67,301 | 26 | 0.723 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 364,105 | 3.641 | 20 | 20 | fits | 119,193 | 196 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 301,609 | 3.016 | 20 | 200 | fits | 147,654 | 208 | 0.451 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 420,186 | 4.202 | 20 | 200 | fits | 119,193 | 196 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 302,533 | 3.025 | 20 | 20 | fits | 147,654 | 208 | 0.451 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 420,890 | 4.209 | 20 | 20 | fits | 119,193 | 196 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 149,940 | 1.499 | 20 | 24 | fits | 148,929 | 143 | 0.453 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 305,183 | 3.052 | 20 | 24 | fits | 147,654 | 208 | 0.451 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 305,117 | 3.051 | 20 | 50 | fits | 147,654 | 208 | 0.451 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 423,914 | 4.239 | 20 | 50 | fits | 119,193 | 196 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 511,075 | 5.111 | 20 | 20 | fits | 87,227 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 1,025,442 | 10.254 | 20 | 20 | fits | 79,439 | 31 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 360,823 | 3.608 | 20 | 20 | fits | 122,792 | 205 | 0.388 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 286,936 | 2.869 | 20 | 200 | fits | 146,306 | 204 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 409,112 | 4.091 | 20 | 200 | fits | 122,792 | 205 | 0.388 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 287,860 | 2.879 | 20 | 20 | fits | 146,306 | 204 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 409,816 | 4.098 | 20 | 20 | fits | 122,792 | 205 | 0.388 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 145,194 | 1.452 | 20 | 24 | fits | 151,226 | 147 | 0.459 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 290,510 | 2.905 | 20 | 24 | fits | 146,306 | 204 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 290,444 | 2.904 | 20 | 50 | fits | 146,306 | 204 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 412,840 | 4.128 | 20 | 50 | fits | 122,792 | 205 | 0.388 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 499,993 | 5.000 | 20 | 20 | fits | 87,219 | 24 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 1,014,744 | 10.147 | 20 | 20 | fits | 86,822 | 28 | 0.573 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 354,500 | 3.545 | 20 | 20 | fits | 118,982 | 196 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 292,066 | 2.921 | 20 | 200 | fits | 145,376 | 203 | 0.446 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 410,432 | 4.104 | 20 | 200 | fits | 118,982 | 196 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 292,990 | 2.930 | 20 | 20 | fits | 145,376 | 203 | 0.446 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 411,136 | 4.111 | 20 | 20 | fits | 118,982 | 196 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 151,254 | 1.513 | 20 | 24 | fits | 148,860 | 142 | 0.452 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 295,640 | 2.956 | 20 | 24 | fits | 145,376 | 203 | 0.446 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 295,574 | 2.956 | 20 | 50 | fits | 145,376 | 203 | 0.446 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 414,160 | 4.142 | 20 | 50 | fits | 118,982 | 196 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 501,402 | 5.014 | 20 | 20 | fits | 87,308 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 1,017,973 | 10.180 | 20 | 20 | fits | 86,531 | 28 | 0.560 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 357,402 | 3.574 | 20 | 20 | fits | 119,259 | 196 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 287,829 | 2.878 | 20 | 200 | fits | 147,258 | 208 | 0.447 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 406,472 | 4.065 | 20 | 200 | fits | 119,259 | 196 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 288,753 | 2.888 | 20 | 20 | fits | 147,258 | 208 | 0.447 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 407,176 | 4.072 | 20 | 20 | fits | 119,259 | 196 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 145,135 | 1.451 | 20 | 24 | fits | 149,098 | 142 | 0.454 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 291,403 | 2.914 | 20 | 24 | fits | 147,258 | 208 | 0.447 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 291,337 | 2.913 | 20 | 50 | fits | 147,258 | 208 | 0.447 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 410,200 | 4.102 | 20 | 50 | fits | 119,259 | 196 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 497,293 | 4.973 | 20 | 20 | fits | 87,159 | 24 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 1,011,962 | 10.120 | 20 | 20 | fits | 86,454 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 358,973 | 3.590 | 20 | 20 | fits | 118,982 | 196 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 296,539 | 2.965 | 20 | 200 | fits | 145,376 | 203 | 0.446 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 414,905 | 4.149 | 20 | 200 | fits | 118,982 | 196 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 297,463 | 2.975 | 20 | 20 | fits | 145,376 | 203 | 0.446 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 415,609 | 4.156 | 20 | 20 | fits | 118,982 | 196 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 155,727 | 1.557 | 20 | 24 | fits | 149,098 | 142 | 0.454 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 300,113 | 3.001 | 20 | 24 | fits | 145,376 | 203 | 0.446 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 300,047 | 3.000 | 20 | 50 | fits | 145,376 | 203 | 0.446 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 418,633 | 4.186 | 20 | 50 | fits | 118,982 | 196 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 501,547 | 5.015 | 20 | 20 | fits | 82,980 | 33 | 0.805 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 1,018,850 | 10.188 | 20 | 20 | fits | 73,337 | 24 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 371,326 | 3.713 | 20 | 20 | fits | 130,436 | 209 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 290,466 | 2.905 | 20 | 200 | fits | 145,898 | 203 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 420,286 | 4.203 | 20 | 200 | fits | 130,436 | 209 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 291,390 | 2.914 | 20 | 20 | fits | 145,898 | 203 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 420,990 | 4.210 | 20 | 20 | fits | 130,436 | 209 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 149,132 | 1.491 | 20 | 24 | fits | 148,860 | 142 | 0.452 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 294,040 | 2.940 | 20 | 24 | fits | 145,898 | 203 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 293,974 | 2.940 | 20 | 50 | fits | 145,898 | 203 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 424,014 | 4.240 | 20 | 50 | fits | 130,436 | 209 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 521,142 | 5.211 | 20 | 20 | fits | 88,165 | 25 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 1,011,855 | 10.119 | 20 | 20 | fits | 59,802 | 20 | 0.655 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 384,617 | 3.846 | 20 | 20 | fits | 132,045 | 214 | 0.401 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 301,029 | 3.010 | 20 | 200 | fits | 145,869 | 198 | 0.471 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 441,338 | 4.413 | 20 | 200 | fits | 132,045 | 214 | 0.401 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 301,953 | 3.020 | 20 | 20 | fits | 145,869 | 198 | 0.471 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 442,042 | 4.420 | 20 | 20 | fits | 132,045 | 214 | 0.401 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 159,724 | 1.597 | 20 | 24 | fits | 148,860 | 142 | 0.452 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 304,603 | 3.046 | 20 | 24 | fits | 145,869 | 198 | 0.471 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 304,537 | 3.045 | 20 | 50 | fits | 145,869 | 198 | 0.471 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 445,066 | 4.451 | 20 | 50 | fits | 132,045 | 214 | 0.401 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 532,346 | 5.323 | 20 | 20 | fits | 87,346 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 1,022,959 | 10.230 | 20 | 20 | fits | 59,802 | 20 | 0.655 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 359,477 | 3.595 | 20 | 20 | fits | 119,105 | 196 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 297,058 | 2.971 | 20 | 200 | fits | 146,068 | 203 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 415,547 | 4.155 | 20 | 200 | fits | 119,105 | 196 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 297,982 | 2.980 | 20 | 20 | fits | 146,068 | 203 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 416,251 | 4.163 | 20 | 20 | fits | 119,105 | 196 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 155,554 | 1.556 | 20 | 24 | fits | 149,098 | 142 | 0.454 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 300,632 | 3.006 | 20 | 24 | fits | 146,068 | 203 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 300,566 | 3.006 | 20 | 50 | fits | 146,068 | 203 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 419,275 | 4.193 | 20 | 50 | fits | 119,105 | 196 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 506,585 | 5.066 | 20 | 20 | fits | 87,376 | 24 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 1,021,079 | 10.211 | 20 | 20 | fits | 80,341 | 30 | 0.676 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 360,245 | 3.602 | 20 | 20 | fits | 119,553 | 199 | 0.371 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 289,289 | 2.893 | 20 | 200 | fits | 144,894 | 199 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 408,226 | 4.082 | 20 | 200 | fits | 119,553 | 199 | 0.371 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 290,213 | 2.902 | 20 | 20 | fits | 144,894 | 199 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 408,930 | 4.089 | 20 | 20 | fits | 119,553 | 199 | 0.371 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 148,959 | 1.490 | 20 | 24 | fits | 148,860 | 142 | 0.452 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 292,863 | 2.929 | 20 | 24 | fits | 144,894 | 199 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 292,797 | 2.928 | 20 | 50 | fits | 144,894 | 199 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 411,954 | 4.120 | 20 | 50 | fits | 119,553 | 199 | 0.371 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 499,358 | 4.994 | 20 | 20 | fits | 87,470 | 24 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 1,092,174 | 10.922 | 20 | 20 | fits | 87,357 | 29 | 0.578 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 363,474 | 3.635 | 20 | 20 | fits | 119,425 | 197 | 0.385 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 301,055 | 3.011 | 20 | 200 | fits | 146,068 | 203 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 419,864 | 4.199 | 20 | 200 | fits | 119,425 | 197 | 0.385 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 301,979 | 3.020 | 20 | 20 | fits | 146,068 | 203 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 420,568 | 4.206 | 20 | 20 | fits | 119,425 | 197 | 0.385 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 159,551 | 1.596 | 20 | 24 | fits | 148,860 | 142 | 0.452 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 304,629 | 3.046 | 20 | 24 | fits | 146,068 | 203 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 304,563 | 3.046 | 20 | 50 | fits | 146,068 | 203 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 423,592 | 4.236 | 20 | 50 | fits | 119,425 | 197 | 0.385 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 523,813 | 5.238 | 20 | 20 | fits | 91,300 | 31 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,100,375 | 11.004 | 20 | 20 | fits | 73,337 | 24 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 378,014 | 3.780 | 20 | 20 | fits | 124,584 | 206 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 294,026 | 2.940 | 20 | 200 | fits | 145,158 | 200 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 426,831 | 4.268 | 20 | 200 | fits | 124,584 | 206 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 294,950 | 2.950 | 20 | 20 | fits | 145,158 | 200 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 427,535 | 4.275 | 20 | 20 | fits | 124,584 | 206 | 0.406 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 153,432 | 1.534 | 20 | 24 | fits | 149,098 | 142 | 0.454 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 297,600 | 2.976 | 20 | 24 | fits | 145,158 | 200 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 297,534 | 2.975 | 20 | 50 | fits | 145,158 | 200 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 430,559 | 4.306 | 20 | 50 | fits | 124,584 | 206 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 518,095 | 5.181 | 20 | 20 | fits | 87,602 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,094,646 | 10.946 | 20 | 20 | fits | 73,427 | 25 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 363,597 | 3.636 | 20 | 20 | fits | 122,515 | 202 | 0.403 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 298,037 | 2.980 | 20 | 200 | fits | 147,098 | 208 | 0.449 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 419,936 | 4.199 | 20 | 200 | fits | 122,515 | 202 | 0.403 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 298,961 | 2.990 | 20 | 20 | fits | 147,098 | 208 | 0.449 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 420,640 | 4.206 | 20 | 20 | fits | 122,515 | 202 | 0.403 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 146,924 | 1.469 | 20 | 24 | fits | 148,947 | 143 | 0.453 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 301,611 | 3.016 | 20 | 24 | fits | 147,098 | 208 | 0.449 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 301,545 | 3.015 | 20 | 50 | fits | 147,098 | 208 | 0.449 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 423,664 | 4.237 | 20 | 50 | fits | 122,515 | 202 | 0.403 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 511,073 | 5.111 | 20 | 20 | fits | 87,475 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,103,469 | 11.035 | 20 | 20 | fits | 79,377 | 31 | 0.687 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 387,075 | 3.871 | 20 | 20 | fits | 127,759 | 205 | 0.402 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 308,178 | 3.082 | 20 | 200 | fits | 146,589 | 204 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 435,321 | 4.353 | 20 | 200 | fits | 127,759 | 205 | 0.402 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 309,102 | 3.091 | 20 | 20 | fits | 146,589 | 204 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 436,025 | 4.360 | 20 | 20 | fits | 127,759 | 205 | 0.402 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 157,574 | 1.576 | 20 | 24 | fits | 149,005 | 143 | 0.453 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 311,752 | 3.118 | 20 | 24 | fits | 146,589 | 204 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 311,686 | 3.117 | 20 | 50 | fits | 146,589 | 204 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 439,049 | 4.390 | 20 | 50 | fits | 127,759 | 205 | 0.402 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 604,335 | 6.043 | 20 | 20 | fits | 87,648 | 25 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,112,185 | 11.122 | 20 | 20 | fits | 73,628 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 360,827 | 3.608 | 20 | 20 | fits | 126,871 | 202 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 290,358 | 2.904 | 20 | 200 | fits | 145,393 | 203 | 0.446 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 416,613 | 4.166 | 20 | 200 | fits | 126,871 | 202 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 291,282 | 2.913 | 20 | 20 | fits | 145,393 | 203 | 0.446 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 417,317 | 4.173 | 20 | 20 | fits | 126,871 | 202 | 0.409 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 149,529 | 1.495 | 20 | 24 | fits | 148,860 | 142 | 0.452 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 293,932 | 2.939 | 20 | 24 | fits | 145,393 | 203 | 0.446 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 293,866 | 2.939 | 20 | 50 | fits | 145,393 | 203 | 0.446 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 420,341 | 4.203 | 20 | 50 | fits | 126,871 | 202 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 585,606 | 5.856 | 20 | 20 | fits | 87,627 | 25 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,093,259 | 10.933 | 20 | 20 | fits | 73,337 | 24 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 455,930 | 4.559 | 20 | 20 | fits | 125,003 | 218 | 0.376 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 303,728 | 3.037 | 20 | 200 | fits | 148,171 | 185 | 0.476 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 505,570 | 5.056 | 20 | 200 | fits | 125,003 | 218 | 0.376 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 304,652 | 3.047 | 20 | 20 | fits | 148,171 | 185 | 0.476 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 506,274 | 5.063 | 20 | 20 | fits | 125,003 | 218 | 0.376 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 160,121 | 1.601 | 20 | 24 | fits | 148,860 | 142 | 0.452 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 307,302 | 3.073 | 20 | 24 | fits | 148,171 | 185 | 0.476 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 307,236 | 3.072 | 20 | 50 | fits | 148,171 | 185 | 0.476 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 509,298 | 5.093 | 20 | 50 | fits | 125,003 | 218 | 0.376 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 597,025 | 5.970 | 20 | 20 | fits | 87,793 | 25 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,104,126 | 11.041 | 20 | 20 | fits | 73,337 | 24 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 367,969 | 3.680 | 20 | 20 | fits | 118,953 | 196 | 0.381 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 305,170 | 3.052 | 20 | 200 | fits | 147,183 | 208 | 0.449 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 423,507 | 4.235 | 20 | 200 | fits | 118,953 | 196 | 0.381 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 306,094 | 3.061 | 20 | 20 | fits | 147,183 | 208 | 0.449 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 424,211 | 4.242 | 20 | 20 | fits | 118,953 | 196 | 0.381 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 153,972 | 1.540 | 20 | 24 | fits | 148,866 | 143 | 0.453 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 308,744 | 3.087 | 20 | 24 | fits | 147,183 | 208 | 0.449 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 308,678 | 3.087 | 20 | 50 | fits | 147,183 | 208 | 0.449 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 427,235 | 4.272 | 20 | 50 | fits | 118,953 | 196 | 0.381 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 514,705 | 5.147 | 20 | 20 | fits | 87,536 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 1,027,203 | 10.272 | 20 | 20 | fits | 71,749 | 33 | 0.743 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 350,974 | 3.510 | 20 | 20 | fits | 119,075 | 196 | 0.385 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 288,492 | 2.885 | 20 | 200 | fits | 146,736 | 208 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 406,951 | 4.070 | 20 | 200 | fits | 119,075 | 196 | 0.385 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 289,416 | 2.894 | 20 | 20 | fits | 146,736 | 208 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 407,655 | 4.077 | 20 | 20 | fits | 119,075 | 196 | 0.385 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 146,320 | 1.463 | 20 | 24 | fits | 148,860 | 142 | 0.452 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 292,066 | 2.921 | 20 | 24 | fits | 146,736 | 208 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 292,000 | 2.920 | 20 | 50 | fits | 146,736 | 208 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 410,679 | 4.107 | 20 | 50 | fits | 119,075 | 196 | 0.385 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 498,194 | 4.982 | 20 | 20 | fits | 87,581 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 1,012,660 | 10.127 | 20 | 20 | fits | 86,675 | 28 | 0.567 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 360,885 | 3.609 | 20 | 20 | fits | 118,647 | 196 | 0.378 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 298,238 | 2.982 | 20 | 200 | fits | 145,890 | 203 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 416,269 | 4.163 | 20 | 200 | fits | 118,647 | 196 | 0.378 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 299,162 | 2.992 | 20 | 20 | fits | 145,890 | 203 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 416,973 | 4.170 | 20 | 20 | fits | 118,647 | 196 | 0.378 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 156,912 | 1.569 | 20 | 24 | fits | 148,860 | 142 | 0.452 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 301,812 | 3.018 | 20 | 24 | fits | 145,890 | 203 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 301,746 | 3.017 | 20 | 50 | fits | 145,890 | 203 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 419,997 | 4.200 | 20 | 50 | fits | 118,647 | 196 | 0.378 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 507,465 | 5.075 | 20 | 20 | fits | 87,534 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 1,024,077 | 10.241 | 20 | 20 | fits | 86,454 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 354,039 | 3.540 | 20 | 20 | fits | 119,027 | 196 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 291,605 | 2.916 | 20 | 200 | fits | 145,376 | 203 | 0.446 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 410,016 | 4.100 | 20 | 200 | fits | 119,027 | 196 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 292,529 | 2.925 | 20 | 20 | fits | 145,376 | 203 | 0.446 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 410,720 | 4.107 | 20 | 20 | fits | 119,027 | 196 | 0.384 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 150,793 | 1.508 | 20 | 24 | fits | 149,098 | 142 | 0.454 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 295,179 | 2.952 | 20 | 24 | fits | 145,376 | 203 | 0.446 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 295,113 | 2.951 | 20 | 50 | fits | 145,376 | 203 | 0.446 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 413,744 | 4.137 | 20 | 50 | fits | 119,027 | 196 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 501,293 | 5.013 | 20 | 20 | fits | 87,615 | 25 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 1,015,424 | 10.154 | 20 | 20 | fits | 86,454 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 365,358 | 3.654 | 20 | 20 | fits | 118,967 | 197 | 0.381 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 302,711 | 3.027 | 20 | 200 | fits | 145,890 | 203 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 421,062 | 4.211 | 20 | 200 | fits | 118,967 | 197 | 0.381 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 303,635 | 3.036 | 20 | 20 | fits | 145,890 | 203 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 421,766 | 4.218 | 20 | 20 | fits | 118,967 | 197 | 0.381 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 161,385 | 1.614 | 20 | 24 | fits | 149,098 | 142 | 0.454 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 306,285 | 3.063 | 20 | 24 | fits | 145,890 | 203 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 306,219 | 3.062 | 20 | 50 | fits | 145,890 | 203 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 424,790 | 4.248 | 20 | 50 | fits | 118,967 | 197 | 0.381 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 515,462 | 5.155 | 20 | 20 | fits | 82,088 | 33 | 0.805 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 1,019,609 | 10.196 | 20 | 20 | fits | 73,337 | 24 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 378,276 | 3.783 | 20 | 20 | fits | 131,125 | 209 | 0.434 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 295,748 | 2.957 | 20 | 200 | fits | 145,522 | 204 | 0.447 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 434,960 | 4.350 | 20 | 200 | fits | 131,125 | 209 | 0.434 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 296,672 | 2.967 | 20 | 20 | fits | 145,522 | 204 | 0.447 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 435,664 | 4.357 | 20 | 20 | fits | 131,125 | 209 | 0.434 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 154,790 | 1.548 | 20 | 24 | fits | 148,860 | 142 | 0.452 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 299,322 | 2.993 | 20 | 24 | fits | 145,522 | 204 | 0.447 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 299,256 | 2.993 | 20 | 50 | fits | 145,522 | 204 | 0.447 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 438,688 | 4.387 | 20 | 50 | fits | 131,125 | 209 | 0.434 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 526,381 | 5.264 | 20 | 20 | fits | 87,759 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 1,016,994 | 10.170 | 20 | 20 | fits | 59,802 | 20 | 0.655 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 378,166 | 3.782 | 20 | 20 | fits | 129,388 | 208 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 298,709 | 2.987 | 20 | 200 | fits | 147,627 | 208 | 0.451 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 427,481 | 4.275 | 20 | 200 | fits | 129,388 | 208 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 299,633 | 2.996 | 20 | 20 | fits | 147,627 | 208 | 0.451 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 428,185 | 4.282 | 20 | 20 | fits | 129,388 | 208 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 147,205 | 1.472 | 20 | 24 | fits | 149,149 | 143 | 0.454 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 302,283 | 3.023 | 20 | 24 | fits | 147,627 | 208 | 0.451 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 302,217 | 3.022 | 20 | 50 | fits | 147,627 | 208 | 0.451 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 431,209 | 4.312 | 20 | 50 | fits | 129,388 | 208 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 518,825 | 5.188 | 20 | 20 | fits | 87,682 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 1,026,162 | 10.262 | 20 | 20 | fits | 66,415 | 27 | 0.735 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 369,075 | 3.691 | 20 | 20 | fits | 126,948 | 208 | 0.365 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 298,289 | 2.983 | 20 | 200 | fits | 145,623 | 197 | 0.469 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 424,621 | 4.246 | 20 | 200 | fits | 126,948 | 208 | 0.365 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 299,213 | 2.992 | 20 | 20 | fits | 145,623 | 197 | 0.469 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 425,325 | 4.253 | 20 | 20 | fits | 126,948 | 208 | 0.365 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 157,230 | 1.572 | 20 | 24 | fits | 149,217 | 142 | 0.455 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 301,863 | 3.019 | 20 | 24 | fits | 145,623 | 197 | 0.469 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 301,797 | 3.018 | 20 | 50 | fits | 145,623 | 197 | 0.469 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 428,349 | 4.283 | 20 | 50 | fits | 126,948 | 208 | 0.365 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 515,789 | 5.158 | 20 | 20 | fits | 87,506 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 1,023,085 | 10.231 | 20 | 20 | fits | 73,260 | 24 | 0.601 |
| LINK_UP | `adp.link_up.if0` | 2,925 | 0.029 | 20 | 200 | fits | 26,957 | 43 (11) | 0.722 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,388 | 0.154 | 20 | 200 | fits | 23,321 | 23 (39) | 0.748 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 1,785 | 0.018 | 20 | 200 | fits | 2,865 | 10 (11) | 0.538 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 151,750 | 1.518 | 20 | 200 | fits | 152,690 | 251 | 0.460 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 215,902 | 2.159 | 20 | 20 | fits | 84,289 | 82 | 0.664 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 296,411 | 2.964 | 20 | 24 | fits | 75,616 | 54 | 0.490 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 123,590 | 1.236 | 20 | 50 | fits | 30,134 | 37 | 0.644 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 939,255 | 9.393 | 20 | 20 | fits | 46,321 | 16 | 0.724 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 234,254 | 2.343 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 151,750 | 1.518 | 20 | 200 | fits | 152,690 | 251 | 0.460 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 199,109 | 1.991 | 20 | 20 | fits | 147,966 | 267 | 0.357 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 285,370 | 2.854 | 20 | 24 | fits | 78,925 | 60 | 0.516 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 131,266 | 1.313 | 20 | 50 | fits | 33,212 | 43 | 0.667 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 997,302 | 9.973 | 20 | 20 | fits | 63,507 | 26 | 0.692 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 262,781 | 2.628 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 24,560 | 0.246 | 20 | 20 | fits | 32,433 | 27 (35) | 0.813 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 12,374 | 0.124 | 20 | 20 | fits | 29,387 | 23 (14) | 0.841 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 25,549 | 0.255 | 20 | 20 | fits | 28,838 | 24 (14) | 0.840 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 10,834 | 0.108 | 20 | 20 | fits | 29,808 | 21 (35) | 0.823 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 76,078 | 0.761 | 20 | 20 | fits | 28,025 | 8 | 0.762 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 44,993 | 0.450 | 20 | 20 | fits | 45,059 | 12 | 0.892 |
| malformed MRPDU discard | `srp.malformed.if0` | 20,424 | 0.204 | 20 | 20 | fits | 20,490 | 12 | 0.693 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 87,362 | 0.874 | 220 | 220 | fits | 56,849 | 6 | 0.923 |
| an event behind 15 others | `backlog.event.if0` | 166,826 | 1.668 | 20 | 200 | fits | 56,818 | 79 | 0.577 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 426,110 | 4.261 | 20 | 20 | fits | 40,298 | 63 | 0.323 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 422,014 | 4.220 | 20 | 200 | fits | 151,958 | 167 | 0.398 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 421,398 | 4.214 | 20 | 200 | fits | 151,958 | 167 | 0.398 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 417,692 | 4.177 | 20 | 20 | fits | 151,958 | 167 | 0.398 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 457,154 | 4.572 | 20 | 20 | fits | 40,298 | 63 | 0.323 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 151,980 | 1.520 | 20 | 24 | fits | 152,871 | 148 | 0.462 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 420,342 | 4.203 | 20 | 24 | fits | 151,958 | 167 | 0.398 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 420,276 | 4.203 | 20 | 50 | fits | 151,958 | 167 | 0.398 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 419,880 | 4.199 | 20 | 50 | fits | 151,958 | 167 | 0.398 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 460,112 | 4.601 | 20 | 20 | fits | 40,298 | 63 | 0.323 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 518,984 | 5.190 | 20 | 20 | fits | 24,719 | 41 | 0.162 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 373,284 | 3.733 | 20 | 20 | fits | 123,887 | 206 | 0.402 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 289,913 | 2.899 | 20 | 200 | fits | 145,234 | 200 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 422,012 | 4.220 | 20 | 200 | fits | 123,887 | 206 | 0.402 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 290,837 | 2.908 | 20 | 20 | fits | 145,234 | 200 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 422,716 | 4.227 | 20 | 20 | fits | 123,887 | 206 | 0.402 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 149,243 | 1.492 | 20 | 24 | fits | 149,429 | 145 | 0.455 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 293,487 | 2.935 | 20 | 24 | fits | 145,234 | 200 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 293,421 | 2.934 | 20 | 50 | fits | 145,234 | 200 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 425,740 | 4.257 | 20 | 50 | fits | 123,887 | 206 | 0.402 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 513,242 | 5.132 | 20 | 20 | fits | 87,568 | 24 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,011,420 | 10.114 | 20 | 20 | fits | 73,255 | 24 | 0.601 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 9,630 | 0.096 | 20 | 20 | fits | 26,755 | 19 | 0.804 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 289,913 | 2.899 | 20 | 200 | fits | 145,234 | 200 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 28,861 | 0.289 | 20 | 200 | fits | 26,755 | 19 | 0.804 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 290,837 | 2.908 | 20 | 20 | fits | 145,234 | 200 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 413,322 | 4.133 | 20 | 20 | fits | 114,493 | 196 | 0.367 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 149,243 | 1.492 | 20 | 24 | fits | 149,429 | 145 | 0.455 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 293,487 | 2.935 | 20 | 24 | fits | 145,234 | 200 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 293,421 | 2.934 | 20 | 50 | fits | 145,234 | 200 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 416,346 | 4.163 | 20 | 50 | fits | 114,493 | 196 | 0.367 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 503,600 | 5.036 | 20 | 20 | fits | 87,320 | 24 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,001,539 | 10.015 | 20 | 20 | fits | 73,255 | 24 | 0.601 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,304,098 | 63.041 | 20 | 20 | MISS ceiling | 18,657 | 13 | 0.622 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,322,755 | 63.228 | 20 | 20 | MISS ceiling | 18,714 | 13 | 0.605 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,341,324 | 63.413 | 20 | 20 | MISS ceiling | 18,645 | 13 | 0.613 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,359,885 | 63.599 | 20 | 20 | MISS ceiling | 18,637 | 13 | 0.622 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,378,447 | 63.784 | 20 | 20 | MISS ceiling | 18,629 | 13 | 0.622 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 155,100 | 1.551 | 20 | 200 | fits | 147,584 | 200 | 0.475 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 250,684 | 2.507 | 20 | 200 | fits | 96,200 | 185 | 0.373 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 150,778 | 1.508 | 20 | 20 | fits | 147,584 | 200 | 0.475 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,214,475 | 62.145 | 20 | 20 | MISS ceiling | 29,267 | 15 | 0.750 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 154,418 | 1.544 | 20 | 24 | fits | 147,584 | 200 | 0.475 |
