### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 94 paths and 7 of 964 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.190 (0.386) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.090 (0.209) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.081 (0.236) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.089 (0.381) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.107 (0.227) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.092 (0.208) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.098 (0.219) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.102 (0.228) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.100 (0.286) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.127 (0.463) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.181 (0.482) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.296 (0.570) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.125 (0.429) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.141 (0.491) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.113 (0.407) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.157 (0.372) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.050 (0.144) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.022 (0.128) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.023 (0.213) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.023 (0.233) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.083 (0.224) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.121 (0.377) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.123 (0.399) | fits | 0 aecp | 1 | 0 |
| get_as_path, refused ENTITY_MISBEHAVING | 0 | `aecp.get_as_path.if0` (aecp) | 0.193 (0.475) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.168 (0.464) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.149 (0.426) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.203 (0.491) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.183 (0.463) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR held for a token (#917) | 0 | `aecp.held.read_descriptor.if0` (aecp-held) | 5.180 (5.461) | fits | 16 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.232 (0.566) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.082 (0.226) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.218 (0.501) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.164 (0.450) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.157 (0.441) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.176 (0.457) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.179 (0.462) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.172 (0.453) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.163 (0.401) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.178 (0.461) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.152 (0.447) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.185 (0.467) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.153 (0.439) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.177 (0.418) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.161 (0.457) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.177 (0.456) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.109 (0.254) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.221 (0.602) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.132 (0.409) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.236 (0.570) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.561 (2.862) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.452 (0.718) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.618 (0.903) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.484 (0.759) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.490 (0.743) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.516 (0.814) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.286 (3.578) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.500 (0.756) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 3.083 (3.369) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.445 (2.776) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.692 (4.019) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.548 (3.867) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.399 (1.702) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.008 (4.334) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 4.539 (5.888) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.085 (0.394) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.554 (1.941) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.865 (63.116) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.519 (63.770) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.320 (0.442) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 1.944 | fits | 11 acmp | 4 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-burst.held.adp.if0` (save-burst) | 1.519 | fits | 7 adp | 4 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-flight.held.aecp.if0` (save-flight) | 2.935 | fits | 14 aecp | 4 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 2.396 | fits | 6 maap | 4 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 7.775 | fits | 31 srp | 4 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.124 (0.404) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.093 (0.194) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.099 (0.233) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.105 (0.404) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.196 (0.458) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.411 | fits | 0 srp | 4 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 3.918 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.063 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 3.961 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 5.041 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-7.service.aecp.first.if0` (backlog-adp@blank-7) | 2.284 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.823 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 3.944 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.maap.last.if0` (backlog-adp@program-aged2-7) | 5.078 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-6.service.srp.first.if0` (backlog-adp@verify-aged2-6) | 5.885 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-7.service.srp.last.if0` (backlog-adp@verify-aged2-7) | 9.526 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.776 (0.874) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.381 (0.382) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.180 (0.181) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.739 (0.825) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 14.144 | 12 | 145,788 (1.458) | yes | - |
| backlog-adp@blank-1 | 0 | 14.019 | 12 | 145,788 (1.458) | yes | - |
| backlog-adp@blank-2 | 0 | 13.894 | 12 | 145,788 (1.458) | yes | - |
| backlog-adp@blank-3 | 0 | 13.769 | 12 | 145,788 (1.458) | yes | - |
| backlog-adp@blank-4 | 0 | 13.644 | 12 | 145,788 (1.458) | yes | - |
| backlog-adp@blank-5 | 0 | 13.519 | 12 | 145,788 (1.458) | yes | - |
| backlog-adp@blank-6 | 0 | 13.394 | 12 | 145,788 (1.458) | yes | - |
| backlog-adp@blank-7 | 0 | 13.250 | 12 | 148,362 (1.484) | yes | - |
| backlog-adp@program-0 | 0 | 11.369 | 12 | 149,533 (1.495) | yes | - |
| backlog-adp@program-1 | 0 | 11.116 | 12 | 148,318 (1.483) | yes | - |
| backlog-adp@program-2 | 0 | 11.865 | 12 | 147,009 (1.470) | yes | - |
| backlog-adp@program-3 | 0 | 11.615 | 12 | 147,009 (1.470) | yes | - |
| backlog-adp@program-4 | 0 | 11.365 | 12 | 147,009 (1.470) | yes | - |
| backlog-adp@program-5 | 1 | 11.042 | 11 | 146,845 (1.468) | yes | - |
| backlog-adp@program-6 | 0 | 9.948 | 10 | 145,507 (1.455) | yes | - |
| backlog-adp@program-7 | 0 | 10.652 | 10 | 147,621 (1.476) | yes | - |
| backlog-adp@verify-0 | 0 | 12.375 | 12 | 149,599 (1.496) | yes | - |
| backlog-adp@verify-1 | 0 | 13.250 | 13 | 148,369 (1.484) | yes | - |
| backlog-adp@verify-2 | 0 | 13.125 | 13 | 148,369 (1.484) | yes | - |
| backlog-adp@verify-3 | 0 | 13.000 | 13 | 148,369 (1.484) | yes | - |
| backlog-adp@verify-4 | 0 | 12.875 | 13 | 148,369 (1.484) | yes | - |
| backlog-adp@verify-5 | 0 | 12.750 | 13 | 148,369 (1.484) | yes | - |
| backlog-adp@verify-6 | 0 | 12.625 | 13 | 148,369 (1.484) | yes | - |
| backlog-adp@verify-7 | 0 | 12.500 | 13 | 148,369 (1.484) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 13.162 | 12 | 149,747 (1.497) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 12.347 | 13 | 149,665 (1.497) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 12.047 | 10 | 147,711 (1.477) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 12.062 | 10 | 147,711 (1.477) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 11.966 | 9 | 147,254 (1.473) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 16.703 | 12 | 146,353 (1.464) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 15.071 | 12 | 146,522 (1.465) | yes | - |
| backlog-adp@blank-aged2-7 | 1 | 14.014 | 11 | 146,864 (1.469) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 15.073 | 13 | 145,528 (1.455) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 13.397 | 13 | 145,744 (1.457) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 12.375 | 12 | 147,042 (1.470) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 11.296 | 10 | 146,335 (1.463) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 11.191 | 9 | 148,421 (1.484) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 11.195 | 9 | 148,421 (1.484) | yes | - |
| backlog-adp@blank-aged1-6 | 1 | 11.188 | 9 | 148,421 (1.484) | yes | - |
| backlog-adp@blank-aged1-7 | 1 | 11.204 | 9 | 148,564 (1.486) | yes | - |
| backlog-adp@program-aged2-0 | 1 | 10.847 | 10 | 148,360 (1.484) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 10.586 | 11 | 147,723 (1.477) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 10.904 | 12 | 149,697 (1.497) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 10.738 | 10 | 147,650 (1.476) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 10.758 | 10 | 147,650 (1.476) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 10.759 | 10 | 147,650 (1.476) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 10.725 | 10 | 147,650 (1.476) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 10.734 | 10 | 145,311 (1.453) | yes | - |
| backlog-adp@program-aged1-0 | 1 | 10.891 | 10 | 146,305 (1.463) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.712 | 11 | 145,467 (1.455) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 10.612 | 10 | 145,467 (1.455) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 10.614 | 10 | 145,618 (1.456) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 11.054 | 12 | 147,074 (1.471) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 10.665 | 10 | 146,274 (1.463) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 10.707 | 10 | 146,274 (1.463) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 10.690 | 10 | 144,811 (1.448) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 13.200 | 12 | 149,767 (1.498) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 12.373 | 13 | 149,685 (1.497) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 12.083 | 10 | 145,361 (1.454) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 12.094 | 10 | 145,361 (1.454) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 12.090 | 10 | 145,361 (1.454) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 16.077 | 13 | 145,361 (1.454) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 15.251 | 13 | 145,521 (1.455) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 14.183 | 12 | 147,049 (1.470) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 15.119 | 13 | 146,262 (1.463) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 13.423 | 13 | 146,463 (1.465) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 12.391 | 12 | 148,331 (1.483) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 11.306 | 10 | 147,649 (1.476) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 11.328 | 10 | 147,649 (1.476) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 11.322 | 10 | 147,649 (1.476) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 11.319 | 10 | 147,649 (1.476) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 11.250 | 9 | 143,879 (1.439) | yes | - |
| backlog | 0 | 5.298 | 7 | 148,522 (1.485) | yes | - |
| backlog-adp | 0 | 8.941 | 10 | 147,419 (1.474) | yes | - |
| backlog-adp-refill | 0 | 40.660 | 24 | 147,419 (1.474) | yes | - |
| backlog-owed | 0 | 64.069 | 25 | 146,114 (1.461) | yes | - |
| fixture | 0 | 1.233 | 2 | 81,304 (0.813) | yes | - |

Composed maximum over the 4 backlog windows: 148,522 CPU cycles (1.485 ms), backlog.
Over the windows that released their whole load only: 148,522 (1.485 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-flight | 2992 | 0 | 152,756 (1.528) | fits |
| save-burst | 2737 | 0 | 152,756 (1.528) | fits |
| acmp-notk | 3607 | 0 | 96,143 (0.961) | fits |
| save-second | 60490 | 0 | 47,989 (0.480) | fits |
| backlog-adp@blank-0 | 470 | 0 | 145,788 (1.458) | fits |
| backlog-adp@blank-1 | 470 | 0 | 145,788 (1.458) | fits |
| backlog-adp@blank-2 | 470 | 0 | 145,788 (1.458) | fits |
| backlog-adp@blank-3 | 470 | 0 | 145,788 (1.458) | fits |
| backlog-adp@blank-4 | 470 | 0 | 145,788 (1.458) | fits |
| backlog-adp@blank-5 | 470 | 0 | 145,788 (1.458) | fits |
| backlog-adp@blank-6 | 470 | 0 | 145,788 (1.458) | fits |
| backlog-adp@blank-7 | 470 | 0 | 148,362 (1.484) | fits |
| backlog-adp@program-0 | 478 | 0 | 149,533 (1.495) | fits |
| backlog-adp@program-1 | 478 | 0 | 148,318 (1.483) | fits |
| backlog-adp@program-2 | 478 | 0 | 147,009 (1.470) | fits |
| backlog-adp@program-3 | 478 | 0 | 147,009 (1.470) | fits |
| backlog-adp@program-4 | 478 | 0 | 147,009 (1.470) | fits |
| backlog-adp@program-5 | 478 | 0 | 147,816 (1.478) | fits |
| backlog-adp@program-6 | 478 | 0 | 145,507 (1.455) | fits |
| backlog-adp@program-7 | 478 | 0 | 147,621 (1.476) | fits |
| backlog-adp@verify-0 | 484 | 0 | 149,599 (1.496) | fits |
| backlog-adp@verify-1 | 485 | 0 | 148,369 (1.484) | fits |
| backlog-adp@verify-2 | 485 | 0 | 148,369 (1.484) | fits |
| backlog-adp@verify-3 | 485 | 0 | 148,369 (1.484) | fits |
| backlog-adp@verify-4 | 485 | 0 | 148,369 (1.484) | fits |
| backlog-adp@verify-5 | 485 | 0 | 148,369 (1.484) | fits |
| backlog-adp@verify-6 | 485 | 0 | 148,369 (1.484) | fits |
| backlog-adp@verify-7 | 485 | 0 | 148,369 (1.484) | fits |
| backlog-adp@blank-aged2-0 | 813 | 0 | 149,747 (1.497) | fits |
| backlog-adp@blank-aged2-1 | 824 | 0 | 149,665 (1.497) | fits |
| backlog-adp@blank-aged2-2 | 831 | 0 | 147,711 (1.477) | fits |
| backlog-adp@blank-aged2-3 | 841 | 0 | 147,711 (1.477) | fits |
| backlog-adp@blank-aged2-4 | 850 | 0 | 150,537 (1.505) | fits |
| backlog-adp@blank-aged2-5 | 863 | 0 | 146,353 (1.464) | fits |
| backlog-adp@blank-aged2-6 | 873 | 0 | 146,522 (1.465) | fits |
| backlog-adp@blank-aged2-7 | 882 | 0 | 146,864 (1.469) | fits |
| backlog-adp@blank-aged1-0 | 735 | 0 | 145,528 (1.455) | fits |
| backlog-adp@blank-aged1-1 | 745 | 0 | 145,744 (1.457) | fits |
| backlog-adp@blank-aged1-2 | 754 | 0 | 147,042 (1.470) | fits |
| backlog-adp@blank-aged1-3 | 762 | 0 | 146,335 (1.463) | fits |
| backlog-adp@blank-aged1-4 | 771 | 0 | 148,421 (1.484) | fits |
| backlog-adp@blank-aged1-5 | 781 | 0 | 148,421 (1.484) | fits |
| backlog-adp@blank-aged1-6 | 791 | 0 | 148,421 (1.484) | fits |
| backlog-adp@blank-aged1-7 | 801 | 0 | 148,564 (1.486) | fits |
| backlog-adp@program-aged2-0 | 852 | 0 | 148,360 (1.484) | fits |
| backlog-adp@program-aged2-1 | 862 | 0 | 147,723 (1.477) | fits |
| backlog-adp@program-aged2-2 | 873 | 0 | 149,697 (1.497) | fits |
| backlog-adp@program-aged2-3 | 881 | 0 | 147,650 (1.476) | fits |
| backlog-adp@program-aged2-4 | 891 | 0 | 147,650 (1.476) | fits |
| backlog-adp@program-aged2-5 | 901 | 0 | 147,650 (1.476) | fits |
| backlog-adp@program-aged2-6 | 911 | 0 | 147,650 (1.476) | fits |
| backlog-adp@program-aged2-7 | 921 | 0 | 145,311 (1.453) | fits |
| backlog-adp@program-aged1-0 | 773 | 0 | 146,305 (1.463) | fits |
| backlog-adp@program-aged1-1 | 783 | 0 | 145,467 (1.455) | fits |
| backlog-adp@program-aged1-2 | 792 | 0 | 145,467 (1.455) | fits |
| backlog-adp@program-aged1-3 | 802 | 0 | 145,618 (1.456) | fits |
| backlog-adp@program-aged1-4 | 814 | 0 | 147,074 (1.471) | fits |
| backlog-adp@program-aged1-5 | 822 | 0 | 146,274 (1.463) | fits |
| backlog-adp@program-aged1-6 | 832 | 0 | 146,274 (1.463) | fits |
| backlog-adp@program-aged1-7 | 842 | 0 | 144,811 (1.448) | fits |
| backlog-adp@verify-aged2-0 | 793 | 0 | 149,767 (1.498) | fits |
| backlog-adp@verify-aged2-1 | 804 | 0 | 149,685 (1.497) | fits |
| backlog-adp@verify-aged2-2 | 811 | 0 | 145,361 (1.454) | fits |
| backlog-adp@verify-aged2-3 | 821 | 0 | 145,361 (1.454) | fits |
| backlog-adp@verify-aged2-4 | 831 | 0 | 145,361 (1.454) | fits |
| backlog-adp@verify-aged2-5 | 844 | 0 | 145,361 (1.454) | fits |
| backlog-adp@verify-aged2-6 | 854 | 0 | 145,521 (1.455) | fits |
| backlog-adp@verify-aged2-7 | 863 | 0 | 147,049 (1.470) | fits |
| backlog-adp@verify-aged1-0 | 715 | 0 | 146,262 (1.463) | fits |
| backlog-adp@verify-aged1-1 | 725 | 0 | 146,463 (1.465) | fits |
| backlog-adp@verify-aged1-2 | 734 | 0 | 148,331 (1.483) | fits |
| backlog-adp@verify-aged1-3 | 742 | 0 | 147,649 (1.476) | fits |
| backlog-adp@verify-aged1-4 | 752 | 0 | 147,649 (1.476) | fits |
| backlog-adp@verify-aged1-5 | 762 | 0 | 147,649 (1.476) | fits |
| backlog-adp@verify-aged1-6 | 772 | 0 | 147,649 (1.476) | fits |
| backlog-adp@verify-aged1-7 | 781 | 0 | 150,537 (1.505) | fits |
| adp-advertise | 599 | 0 | 30,170 (0.302) | fits |
| save-held | 1406 | 0 | 152,756 (1.528) | fits |
| save-starved | 32563 | 0 | 152,756 (1.528) | fits |
| acmp-noresp | 2027 | 0 | 47,988 (0.480) | fits |
| save | 610 | 0 | 43,888 (0.439) | fits |
| srp | 290 | 0 | 53,576 (0.536) | fits |
| backlog | 286 | 0 | 148,522 (1.485) | fits |
| backlog-adp | 312 | 0 | 147,419 (1.474) | fits |
| backlog-adp-refill | 326 | 0 | 147,419 (1.474) | fits |
| backlog-owed | 310 | 0 | 146,114 (1.461) | fits |
| acmp-disc | 938 | 0 | 47,990 (0.480) | fits |
| maap | 178 | 0 | 30,170 (0.302) | fits |
| adp-link | 90 | 0 | 32,915 (0.329) | fits |
| adp-gm | 89 | 0 | 30,170 (0.302) | fits |
| adp-discover | 89 | 0 | 30,170 (0.302) | fits |
| control | 89 | 0 | 30,170 (0.302) | fits |
| aecp-fanout | 111 | 0 | 66,952 (0.670) | fits |
| acmp-cmd | 87 | 0 | 38,594 (0.386) | fits |
| aecp | 113 | 0 | 43,411 (0.434) | fits |
| aecp-largest-notice | 106 | 0 | 145,593 (1.456) | fits |
| aecp-held | 109 | 0 | 38,542 (0.385) | fits |
| datapath-events | 119 | 0 | 30,170 (0.302) | fits |
| fixture | 160 | 0 | 81,304 (0.813) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 8.421 (20) | 11.579 |
| backlog-adp@blank-aged2-1 | 2 | none | +8.628 ms, 76,203 (0.762 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 8.426 (20) | 11.574 |
| backlog-adp@blank-aged2-2 | 2 | +8.049 ms, 76,635 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 9.357 (20) | 10.643 |
| backlog-adp@blank-aged2-3 | 2 | none | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 9.368 (20) | 10.632 |
| backlog-adp@blank-aged2-4 | 2 | +5.688 ms, 76,595 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 9.275 (20) | 10.725 |
| backlog-adp@blank-aged2-5 | 2 | +4.877 ms, 76,707 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 9.231 (20) | 10.769 |
| backlog-adp@blank-aged2-6 | 2 | +4.223 ms, 76,806 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 9.282 (20) | 10.718 |
| backlog-adp@blank-aged2-7 | 2 | +4.173 ms, 76,806 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 9.412 (20) | 10.588 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 8.470 (20) | 11.530 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 8.490 (20) | 11.510 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 8.494 (20) | 11.506 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 8.598 (20) | 11.402 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 8.494 (20) | 11.506 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 8.497 (20) | 11.503 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 8.490 (20) | 11.510 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 8.503 (20) | 11.497 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 8.422 (20) | 11.578 |
| backlog-adp@program-aged2-1 | 2 | none | +8.647 ms, 80,653 (0.807 ms), issue | `backlog-adp@program-aged2-1.service.srp.last.if0` | 8.446 (20) | 11.554 |
| backlog-adp@program-aged2-2 | 2 | +8.014 ms, 81,027 (0.810 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 9.274 (20) | 10.726 |
| backlog-adp@program-aged2-3 | 2 | +6.428 ms, 81,027 (0.810 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 9.393 (20) | 10.607 |
| backlog-adp@program-aged2-4 | 2 | +5.675 ms, 80,947 (0.809 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 9.414 (20) | 10.586 |
| backlog-adp@program-aged2-5 | 2 | +4.811 ms, 81,047 (0.810 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 9.414 (20) | 10.586 |
| backlog-adp@program-aged2-6 | 2 | none | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 9.379 (20) | 10.621 |
| backlog-adp@program-aged2-7 | 2 | none | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 9.385 (20) | 10.615 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 8.466 (20) | 11.534 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 8.470 (20) | 11.530 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 8.521 (20) | 11.479 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 8.518 (20) | 11.482 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 8.473 (20) | 11.527 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 8.574 (20) | 11.426 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 8.615 (20) | 11.385 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 8.599 (20) | 11.401 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 8.404 (20) | 11.596 |
| backlog-adp@verify-aged2-1 | 2 | none | +8.611 ms, 77,025 (0.770 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 8.409 (20) | 11.591 |
| backlog-adp@verify-aged2-2 | 2 | +8.040 ms, 77,486 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 9.359 (20) | 10.641 |
| backlog-adp@verify-aged2-3 | 2 | none | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 9.367 (20) | 10.633 |
| backlog-adp@verify-aged2-4 | 2 | +5.765 ms, 77,446 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 9.366 (20) | 10.634 |
| backlog-adp@verify-aged2-5 | 2 | +4.974 ms, 77,558 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 9.342 (20) | 10.658 |
| backlog-adp@verify-aged2-6 | 2 | +4.321 ms, 77,628 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 9.395 (20) | 10.605 |
| backlog-adp@verify-aged2-7 | 2 | +3.112 ms, 77,482 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 9.526 (20) | 10.474 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 8.440 (20) | 11.560 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 8.460 (20) | 11.540 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 8.469 (20) | 11.531 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 8.578 (20) | 11.422 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 8.601 (20) | 11.399 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 8.594 (20) | 11.406 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 8.591 (20) | 11.409 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 8.518 (20) | 11.482 |

Least margin over the aged windows: 10.474 ms, `backlog-adp@verify-aged2-7.service.srp.last.if0` at 9.526 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.363 | 6,070 | 102 | 2 | 30.823 | yes | within |
| save-held | 1085.584 | 4,070 | 102 | - | 20.680 | no | within |
| save-starved | 4048.221 | 4,070 | 102 | - | 31.244 | yes | within |
| save | 1077.111 | 4,070 | 102 | - | 24.673 | no | within |

Names from their response to durable (save_burst.py; #920, the ruling of #665 issuecomment-6899740728, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-flight | 1 | 149.906 (0) | 5,000 | 2 | - | - | 19 steps (want 19), 6.156 ms | within |
| save-burst | 39 | 1099.082 (0) | 5,000 | 1 | - | - | sequence 1, 0 missing | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-flight | 1554 | 93,341 (0.933) | 78,792 (0.788) |
| save-burst | 1479 | 91,739 (0.917) | 78,175 (0.782) |
| acmp-notk | 1158 | 96,143 (0.961) | 79,103 (0.791) |
| save-second | 520 | 79,996 (0.800) | 78,111 (0.781) |
| backlog-adp@blank-0 | 344 | 91,891 (0.919) | 76,076 (0.761) |
| backlog-adp@blank-1 | 344 | 91,891 (0.919) | 76,076 (0.761) |
| backlog-adp@blank-2 | 344 | 91,891 (0.919) | 76,076 (0.761) |
| backlog-adp@blank-3 | 344 | 91,891 (0.919) | 76,076 (0.761) |
| backlog-adp@blank-4 | 344 | 91,891 (0.919) | 76,076 (0.761) |
| backlog-adp@blank-5 | 344 | 91,891 (0.919) | 76,076 (0.761) |
| backlog-adp@blank-6 | 344 | 91,891 (0.919) | 76,076 (0.761) |
| backlog-adp@blank-7 | 344 | 91,891 (0.919) | 76,076 (0.761) |
| backlog-adp@program-0 | 373 | 101,206 (1.012) | 78,693 (0.787) |
| backlog-adp@program-1 | 373 | 102,714 (1.027) | 79,096 (0.791) |
| backlog-adp@program-2 | 374 | 96,544 (0.965) | 79,024 (0.790) |
| backlog-adp@program-3 | 374 | 96,544 (0.965) | 79,024 (0.790) |
| backlog-adp@program-4 | 374 | 96,544 (0.965) | 79,024 (0.790) |
| backlog-adp@program-5 | 374 | 96,544 (0.965) | 79,024 (0.790) |
| backlog-adp@program-6 | 373 | 92,914 (0.929) | 78,254 (0.783) |
| backlog-adp@program-7 | 374 | 94,523 (0.945) | 78,977 (0.790) |
| backlog-adp@verify-0 | 398 | 92,768 (0.928) | 78,254 (0.783) |
| backlog-adp@verify-1 | 399 | 93,087 (0.931) | 78,254 (0.783) |
| backlog-adp@verify-2 | 399 | 93,087 (0.931) | 78,254 (0.783) |
| backlog-adp@verify-3 | 399 | 93,087 (0.931) | 78,254 (0.783) |
| backlog-adp@verify-4 | 399 | 93,087 (0.931) | 78,254 (0.783) |
| backlog-adp@verify-5 | 399 | 93,087 (0.931) | 78,254 (0.783) |
| backlog-adp@verify-6 | 399 | 93,087 (0.931) | 78,254 (0.783) |
| backlog-adp@verify-7 | 399 | 93,087 (0.931) | 78,254 (0.783) |
| backlog-adp@blank-aged2-0 | 341 | 96,713 (0.967) | 76,300 (0.763) |
| backlog-adp@blank-aged2-1 | 340 | 91,871 (0.919) | 75,983 (0.760) |
| backlog-adp@blank-aged2-2 | 340 | 89,544 (0.895) | 75,712 (0.757) |
| backlog-adp@blank-aged2-3 | 340 | 89,903 (0.899) | 75,963 (0.760) |
| backlog-adp@blank-aged2-4 | 340 | 89,601 (0.896) | 75,744 (0.757) |
| backlog-adp@blank-aged2-5 | 345 | 96,086 (0.961) | 75,760 (0.758) |
| backlog-adp@blank-aged2-6 | 343 | 91,952 (0.920) | 75,983 (0.760) |
| backlog-adp@blank-aged2-7 | 342 | 89,999 (0.900) | 76,032 (0.760) |
| backlog-adp@blank-aged1-0 | 343 | 96,221 (0.962) | 76,300 (0.763) |
| backlog-adp@blank-aged1-1 | 341 | 91,964 (0.920) | 76,220 (0.762) |
| backlog-adp@blank-aged1-2 | 340 | 91,992 (0.920) | 76,300 (0.763) |
| backlog-adp@blank-aged1-3 | 339 | 90,315 (0.903) | 76,222 (0.762) |
| backlog-adp@blank-aged1-4 | 339 | 90,267 (0.903) | 76,300 (0.763) |
| backlog-adp@blank-aged1-5 | 339 | 90,299 (0.903) | 76,300 (0.763) |
| backlog-adp@blank-aged1-6 | 339 | 90,359 (0.904) | 76,300 (0.763) |
| backlog-adp@blank-aged1-7 | 339 | 90,641 (0.906) | 76,300 (0.763) |
| backlog-adp@program-aged2-0 | 369 | 94,421 (0.944) | 79,055 (0.791) |
| backlog-adp@program-aged2-1 | 368 | 92,489 (0.925) | 78,477 (0.785) |
| backlog-adp@program-aged2-2 | 369 | 92,824 (0.928) | 78,691 (0.787) |
| backlog-adp@program-aged2-3 | 369 | 92,955 (0.930) | 78,691 (0.787) |
| backlog-adp@program-aged2-4 | 369 | 93,002 (0.930) | 78,689 (0.787) |
| backlog-adp@program-aged2-5 | 369 | 93,002 (0.930) | 78,689 (0.787) |
| backlog-adp@program-aged2-6 | 369 | 92,955 (0.930) | 78,867 (0.789) |
| backlog-adp@program-aged2-7 | 369 | 92,993 (0.930) | 78,618 (0.786) |
| backlog-adp@program-aged1-0 | 369 | 94,361 (0.944) | 79,055 (0.791) |
| backlog-adp@program-aged1-1 | 368 | 93,270 (0.933) | 78,975 (0.790) |
| backlog-adp@program-aged1-2 | 368 | 94,421 (0.944) | 79,055 (0.791) |
| backlog-adp@program-aged1-3 | 368 | 94,703 (0.947) | 79,055 (0.791) |
| backlog-adp@program-aged1-4 | 369 | 94,812 (0.948) | 79,055 (0.791) |
| backlog-adp@program-aged1-5 | 368 | 94,377 (0.944) | 78,977 (0.790) |
| backlog-adp@program-aged1-6 | 368 | 94,339 (0.943) | 79,055 (0.791) |
| backlog-adp@program-aged1-7 | 368 | 94,379 (0.944) | 79,055 (0.791) |
| backlog-adp@verify-aged2-0 | 400 | 97,853 (0.979) | 78,254 (0.783) |
| backlog-adp@verify-aged2-1 | 399 | 93,017 (0.930) | 78,254 (0.783) |
| backlog-adp@verify-aged2-2 | 399 | 92,591 (0.926) | 78,254 (0.783) |
| backlog-adp@verify-aged2-3 | 399 | 92,591 (0.926) | 78,254 (0.783) |
| backlog-adp@verify-aged2-4 | 399 | 92,591 (0.926) | 78,254 (0.783) |
| backlog-adp@verify-aged2-5 | 403 | 92,914 (0.929) | 78,254 (0.783) |
| backlog-adp@verify-aged2-6 | 402 | 92,874 (0.929) | 78,254 (0.783) |
| backlog-adp@verify-aged2-7 | 401 | 92,591 (0.926) | 78,254 (0.783) |
| backlog-adp@verify-aged1-0 | 402 | 97,417 (0.974) | 78,254 (0.783) |
| backlog-adp@verify-aged1-1 | 400 | 92,998 (0.930) | 78,254 (0.783) |
| backlog-adp@verify-aged1-2 | 399 | 93,107 (0.931) | 78,254 (0.783) |
| backlog-adp@verify-aged1-3 | 398 | 92,591 (0.926) | 78,254 (0.783) |
| backlog-adp@verify-aged1-4 | 398 | 92,591 (0.926) | 78,254 (0.783) |
| backlog-adp@verify-aged1-5 | 398 | 92,591 (0.926) | 78,254 (0.783) |
| backlog-adp@verify-aged1-6 | 398 | 92,591 (0.926) | 78,254 (0.783) |
| backlog-adp@verify-aged1-7 | 398 | 92,591 (0.926) | 78,254 (0.783) |
| adp-advertise | 578 | 21,598 (0.216) | 2,394 (0.024) |
| save-held | 816 | 92,402 (0.924) | 78,177 (0.782) |
| save-starved | 418 | 80,985 (0.810) | 78,447 (0.784) |
| acmp-noresp | 708 | 95,914 (0.959) | 79,103 (0.791) |
| save | 680 | 91,729 (0.917) | 78,022 (0.780) |
| srp | 271 | 21,598 (0.216) | 2,394 (0.024) |
| backlog | 265 | 21,598 (0.216) | 2,394 (0.024) |
| backlog-adp | 271 | 21,598 (0.216) | 2,505 (0.025) |
| backlog-adp-refill | 274 | 21,598 (0.216) | 2,505 (0.025) |
| backlog-owed | 276 | 21,598 (0.216) | 2,554 (0.026) |
| acmp-disc | 398 | 95,914 (0.959) | 79,103 (0.791) |
| maap | 165 | 21,598 (0.216) | 2,394 (0.024) |
| adp-link | 80 | 21,598 (0.216) | 2,394 (0.024) |
| adp-gm | 80 | 21,598 (0.216) | 2,394 (0.024) |
| adp-discover | 80 | 21,598 (0.216) | 2,394 (0.024) |
| control | 80 | 21,598 (0.216) | 2,394 (0.024) |
| aecp-fanout | 80 | 21,598 (0.216) | 2,394 (0.024) |
| acmp-cmd | 65 | 21,598 (0.216) | 2,394 (0.024) |
| aecp | 80 | 21,598 (0.216) | 2,394 (0.024) |
| aecp-largest-notice | 78 | 21,598 (0.216) | 2,394 (0.024) |
| aecp-held | 98 | 21,598 (0.216) | 2,394 (0.024) |
| datapath-events | 70 | 21,598 (0.216) | 2,394 (0.024) |
| fixture | 54 | 15,346 (0.153) | 2,394 (0.024) |

Longest pass that carries a step: 102,714 CPU cycles (1.027 ms), backlog-adp@program-1; longest step: 79,103 (0.791 ms), acmp-notk.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 151,816 | 1.518 | 20 | 200 | fits | 152,756 | 271 | 0.373 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 179,509 | 1.795 | 20 | 20 | fits | 99,865 | 115 | 0.216 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 293,498 | 2.935 | 20 | 24 | fits | 78,471 | 48 | 0.576 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 239,557 | 2.396 | 20 | 50 | fits | 105,735 | 211 | 0.327 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 756,050 | 7.561 | 20 | 20 | fits | 72,331 | 34 | 0.678 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 84,499 | 0.845 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-burst.held.adp.if0` | 151,947 | 1.519 | 20 | 200 | fits | 152,756 | 271 | 0.373 |
| ACMP record, every channel at its refill rate, the longest | `save-burst.held.acmp.if0` | 190,521 | 1.905 | 20 | 20 | fits | 135,684 | 264 | 0.208 |
| AECP record, every channel at its refill rate, the longest | `save-burst.held.aecp.if0` | 142,403 | 1.424 | 20 | 24 | fits | 81,843 | 37 | 0.701 |
| MAAP record, every channel at its refill rate, the longest | `save-burst.held.maap.if0` | 179,241 | 1.792 | 20 | 50 | fits | 87,037 | 70 | 0.702 |
| SRP record, every channel at its refill rate, the longest | `save-burst.held.srp.if0` | 676,787 | 6.768 | 20 | 20 | fits | 28,203 | 12 | 0.820 |
| an MRPDU its periodic timer owes, the longest | `save-burst.mrpdu.periodic.if0` | 224,239 | 2.242 | 49 | 49 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 14,122 | 0.141 | 20 | 20 | fits | 28,877 | 19 (14) | 0.861 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 453,897 | 4.539 | 20 | 20 | fits | 119,953 | 205 | 0.328 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 368,751 | 3.688 | 20 | 200 | fits | 145,269 | 205 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 500,222 | 5.002 | 20 | 200 | fits | 119,953 | 205 | 0.328 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 369,675 | 3.697 | 20 | 20 | fits | 145,269 | 205 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 500,926 | 5.009 | 20 | 20 | fits | 119,953 | 205 | 0.328 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 228,046 | 2.280 | 20 | 24 | fits | 145,788 | 145 | 0.427 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 372,325 | 3.723 | 20 | 24 | fits | 145,269 | 205 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 372,259 | 3.723 | 20 | 50 | fits | 145,269 | 205 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 503,950 | 5.040 | 20 | 50 | fits | 119,953 | 205 | 0.328 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 584,479 | 5.845 | 20 | 20 | fits | 80,595 | 28 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 934,618 | 9.346 | 20 | 20 | fits | 47,486 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 441,397 | 4.414 | 20 | 20 | fits | 119,953 | 205 | 0.328 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 356,251 | 3.563 | 20 | 200 | fits | 145,269 | 205 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 487,722 | 4.877 | 20 | 200 | fits | 119,953 | 205 | 0.328 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 357,175 | 3.572 | 20 | 20 | fits | 145,269 | 205 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 488,426 | 4.884 | 20 | 20 | fits | 119,953 | 205 | 0.328 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 215,546 | 2.155 | 20 | 24 | fits | 145,788 | 145 | 0.427 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 359,825 | 3.598 | 20 | 24 | fits | 145,269 | 205 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 359,759 | 3.598 | 20 | 50 | fits | 145,269 | 205 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 491,450 | 4.915 | 20 | 50 | fits | 119,953 | 205 | 0.328 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 571,979 | 5.720 | 20 | 20 | fits | 80,595 | 28 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 922,118 | 9.221 | 20 | 20 | fits | 47,486 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 428,897 | 4.289 | 20 | 20 | fits | 119,953 | 205 | 0.328 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 343,751 | 3.438 | 20 | 200 | fits | 145,269 | 205 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 475,222 | 4.752 | 20 | 200 | fits | 119,953 | 205 | 0.328 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 344,675 | 3.447 | 20 | 20 | fits | 145,269 | 205 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 475,926 | 4.759 | 20 | 20 | fits | 119,953 | 205 | 0.328 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 203,046 | 2.030 | 20 | 24 | fits | 145,788 | 145 | 0.427 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 347,325 | 3.473 | 20 | 24 | fits | 145,269 | 205 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 347,259 | 3.473 | 20 | 50 | fits | 145,269 | 205 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 478,950 | 4.790 | 20 | 50 | fits | 119,953 | 205 | 0.328 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 559,479 | 5.595 | 20 | 20 | fits | 80,595 | 28 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 909,618 | 9.096 | 20 | 20 | fits | 47,486 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 416,397 | 4.164 | 20 | 20 | fits | 119,953 | 205 | 0.328 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 331,251 | 3.313 | 20 | 200 | fits | 145,269 | 205 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 462,722 | 4.627 | 20 | 200 | fits | 119,953 | 205 | 0.328 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 332,175 | 3.322 | 20 | 20 | fits | 145,269 | 205 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 463,426 | 4.634 | 20 | 20 | fits | 119,953 | 205 | 0.328 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 190,546 | 1.905 | 20 | 24 | fits | 145,788 | 145 | 0.427 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 334,825 | 3.348 | 20 | 24 | fits | 145,269 | 205 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 334,759 | 3.348 | 20 | 50 | fits | 145,269 | 205 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 466,450 | 4.665 | 20 | 50 | fits | 119,953 | 205 | 0.328 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 546,979 | 5.470 | 20 | 20 | fits | 80,595 | 28 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 897,118 | 8.971 | 20 | 20 | fits | 47,486 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 403,897 | 4.039 | 20 | 20 | fits | 119,953 | 205 | 0.328 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 318,751 | 3.188 | 20 | 200 | fits | 145,269 | 205 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 450,222 | 4.502 | 20 | 200 | fits | 119,953 | 205 | 0.328 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 319,675 | 3.197 | 20 | 20 | fits | 145,269 | 205 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 450,926 | 4.509 | 20 | 20 | fits | 119,953 | 205 | 0.328 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 178,046 | 1.780 | 20 | 24 | fits | 145,788 | 145 | 0.427 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 322,325 | 3.223 | 20 | 24 | fits | 145,269 | 205 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 322,259 | 3.223 | 20 | 50 | fits | 145,269 | 205 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 453,950 | 4.540 | 20 | 50 | fits | 119,953 | 205 | 0.328 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 534,479 | 5.345 | 20 | 20 | fits | 80,595 | 28 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 884,618 | 8.846 | 20 | 20 | fits | 47,486 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 391,397 | 3.914 | 20 | 20 | fits | 119,953 | 205 | 0.328 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 306,251 | 3.063 | 20 | 200 | fits | 145,269 | 205 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 437,722 | 4.377 | 20 | 200 | fits | 119,953 | 205 | 0.328 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 307,175 | 3.072 | 20 | 20 | fits | 145,269 | 205 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 438,426 | 4.384 | 20 | 20 | fits | 119,953 | 205 | 0.328 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 165,546 | 1.655 | 20 | 24 | fits | 145,788 | 145 | 0.427 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 309,825 | 3.098 | 20 | 24 | fits | 145,269 | 205 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 309,759 | 3.098 | 20 | 50 | fits | 145,269 | 205 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 441,450 | 4.415 | 20 | 50 | fits | 119,953 | 205 | 0.328 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 521,979 | 5.220 | 20 | 20 | fits | 80,595 | 28 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 872,118 | 8.721 | 20 | 20 | fits | 47,486 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 378,897 | 3.789 | 20 | 20 | fits | 119,953 | 205 | 0.328 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 293,751 | 2.938 | 20 | 200 | fits | 145,269 | 205 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 425,222 | 4.252 | 20 | 200 | fits | 119,953 | 205 | 0.328 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 294,675 | 2.947 | 20 | 20 | fits | 145,269 | 205 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 425,926 | 4.259 | 20 | 20 | fits | 119,953 | 205 | 0.328 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 153,046 | 1.530 | 20 | 24 | fits | 145,788 | 145 | 0.427 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 297,325 | 2.973 | 20 | 24 | fits | 145,269 | 205 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 297,259 | 2.973 | 20 | 50 | fits | 145,269 | 205 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 428,950 | 4.290 | 20 | 50 | fits | 119,953 | 205 | 0.328 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 509,479 | 5.095 | 20 | 20 | fits | 80,595 | 28 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 859,618 | 8.596 | 20 | 20 | fits | 47,486 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 446,306 | 4.463 | 20 | 20 | fits | 116,572 | 202 | 0.294 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 382,954 | 3.830 | 20 | 200 | fits | 148,362 | 208 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 498,910 | 4.989 | 20 | 200 | fits | 116,572 | 202 | 0.294 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 383,878 | 3.839 | 20 | 20 | fits | 148,362 | 208 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 499,614 | 4.996 | 20 | 20 | fits | 116,572 | 202 | 0.294 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 228,376 | 2.284 | 20 | 24 | fits | 145,886 | 146 | 0.427 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 386,528 | 3.865 | 20 | 24 | fits | 148,362 | 208 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 386,462 | 3.865 | 20 | 50 | fits | 148,362 | 208 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 502,638 | 5.026 | 20 | 50 | fits | 116,572 | 202 | 0.294 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 582,898 | 5.829 | 20 | 20 | fits | 80,326 | 28 | 0.757 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 933,110 | 9.331 | 20 | 20 | fits | 47,504 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 381,585 | 3.816 | 20 | 20 | fits | 105,712 | 184 | 0.295 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 323,123 | 3.231 | 20 | 200 | fits | 149,533 | 219 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 428,219 | 4.282 | 20 | 200 | fits | 105,712 | 184 | 0.295 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 324,047 | 3.240 | 20 | 20 | fits | 149,533 | 219 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 428,923 | 4.289 | 20 | 20 | fits | 105,712 | 184 | 0.295 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 167,317 | 1.673 | 20 | 24 | fits | 145,962 | 146 | 0.425 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 326,697 | 3.267 | 20 | 24 | fits | 149,533 | 219 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 326,631 | 3.266 | 20 | 50 | fits | 149,533 | 219 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 431,947 | 4.319 | 20 | 50 | fits | 105,712 | 184 | 0.295 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 512,340 | 5.123 | 20 | 20 | fits | 80,459 | 28 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 867,544 | 8.675 | 20 | 20 | fits | 47,499 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 375,791 | 3.758 | 20 | 20 | fits | 107,073 | 187 | 0.289 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 314,711 | 3.147 | 20 | 200 | fits | 148,318 | 215 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 421,168 | 4.212 | 20 | 200 | fits | 107,073 | 187 | 0.289 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 315,635 | 3.156 | 20 | 20 | fits | 148,318 | 215 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 421,872 | 4.219 | 20 | 20 | fits | 107,073 | 187 | 0.289 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 160,212 | 1.602 | 20 | 24 | fits | 145,721 | 146 | 0.427 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 318,285 | 3.183 | 20 | 24 | fits | 148,318 | 215 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 318,219 | 3.182 | 20 | 50 | fits | 148,318 | 215 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 424,896 | 4.249 | 20 | 50 | fits | 107,073 | 187 | 0.289 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 505,420 | 5.054 | 20 | 20 | fits | 80,590 | 28 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 860,601 | 8.606 | 20 | 20 | fits | 47,486 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 437,093 | 4.371 | 20 | 20 | fits | 108,888 | 175 | 0.275 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 381,154 | 3.812 | 20 | 200 | fits | 147,009 | 230 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 489,426 | 4.894 | 20 | 200 | fits | 108,888 | 175 | 0.275 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 382,078 | 3.821 | 20 | 20 | fits | 147,009 | 230 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 490,130 | 4.901 | 20 | 20 | fits | 108,888 | 175 | 0.275 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 227,872 | 2.279 | 20 | 24 | fits | 146,079 | 146 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 384,728 | 3.847 | 20 | 24 | fits | 147,009 | 230 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 384,662 | 3.847 | 20 | 50 | fits | 147,009 | 230 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 493,154 | 4.932 | 20 | 50 | fits | 108,888 | 175 | 0.275 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 568,553 | 5.686 | 20 | 20 | fits | 75,465 | 30 | 0.794 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 928,444 | 9.284 | 20 | 20 | fits | 57,145 | 24 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 412,093 | 4.121 | 20 | 20 | fits | 108,888 | 175 | 0.275 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 356,154 | 3.562 | 20 | 200 | fits | 147,009 | 230 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 464,426 | 4.644 | 20 | 200 | fits | 108,888 | 175 | 0.275 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 357,078 | 3.571 | 20 | 20 | fits | 147,009 | 230 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 465,130 | 4.651 | 20 | 20 | fits | 108,888 | 175 | 0.275 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 202,872 | 2.029 | 20 | 24 | fits | 146,079 | 146 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 359,728 | 3.597 | 20 | 24 | fits | 147,009 | 230 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 359,662 | 3.597 | 20 | 50 | fits | 147,009 | 230 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 468,154 | 4.682 | 20 | 50 | fits | 108,888 | 175 | 0.275 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 543,553 | 5.436 | 20 | 20 | fits | 75,465 | 30 | 0.794 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 903,444 | 9.034 | 20 | 20 | fits | 57,145 | 24 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 387,093 | 3.871 | 20 | 20 | fits | 108,888 | 175 | 0.275 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 331,154 | 3.312 | 20 | 200 | fits | 147,009 | 230 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 439,426 | 4.394 | 20 | 200 | fits | 108,888 | 175 | 0.275 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 332,078 | 3.321 | 20 | 20 | fits | 147,009 | 230 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 440,130 | 4.401 | 20 | 20 | fits | 108,888 | 175 | 0.275 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 177,872 | 1.779 | 20 | 24 | fits | 146,079 | 146 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 334,728 | 3.347 | 20 | 24 | fits | 147,009 | 230 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 334,662 | 3.347 | 20 | 50 | fits | 147,009 | 230 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 443,154 | 4.432 | 20 | 50 | fits | 108,888 | 175 | 0.275 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 518,553 | 5.186 | 20 | 20 | fits | 75,465 | 30 | 0.794 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 878,444 | 8.784 | 20 | 20 | fits | 57,145 | 24 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 354,819 | 3.548 | 20 | 20 | fits | 108,888 | 175 | 0.275 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 298,880 | 2.989 | 20 | 200 | fits | 146,845 | 230 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 407,152 | 4.072 | 20 | 200 | fits | 108,888 | 175 | 0.275 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 299,804 | 2.998 | 20 | 20 | fits | 146,845 | 230 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 407,856 | 4.079 | 20 | 20 | fits | 108,888 | 175 | 0.275 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 145,920 | 1.459 | 20 | 24 | fits | 147,816 | 146 | 0.427 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 302,454 | 3.025 | 20 | 24 | fits | 146,845 | 230 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 302,388 | 3.024 | 20 | 50 | fits | 146,845 | 230 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 410,880 | 4.109 | 20 | 50 | fits | 108,888 | 175 | 0.275 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 486,319 | 4.863 | 20 | 20 | fits | 75,505 | 30 | 0.795 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 846,210 | 8.462 | 20 | 20 | fits | 57,145 | 24 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 350,511 | 3.505 | 20 | 20 | fits | 109,321 | 175 | 0.285 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 294,578 | 2.946 | 20 | 200 | fits | 145,507 | 225 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 403,283 | 4.033 | 20 | 200 | fits | 109,321 | 175 | 0.285 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 295,502 | 2.955 | 20 | 20 | fits | 145,507 | 225 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 403,987 | 4.040 | 20 | 20 | fits | 109,321 | 175 | 0.285 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 153,635 | 1.536 | 20 | 24 | fits | 145,419 | 146 | 0.418 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 298,152 | 2.982 | 20 | 24 | fits | 145,507 | 225 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 298,086 | 2.981 | 20 | 50 | fits | 145,507 | 225 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 407,011 | 4.070 | 20 | 50 | fits | 109,321 | 175 | 0.285 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 482,422 | 4.824 | 20 | 20 | fits | 75,477 | 30 | 0.794 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 860,270 | 8.603 | 20 | 20 | fits | 62,652 | 31 | 0.721 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 340,726 | 3.407 | 20 | 20 | fits | 106,141 | 184 | 0.307 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 293,426 | 2.934 | 20 | 200 | fits | 147,621 | 214 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 398,951 | 3.990 | 20 | 200 | fits | 106,141 | 184 | 0.307 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 294,350 | 2.943 | 20 | 20 | fits | 147,621 | 214 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 399,655 | 3.997 | 20 | 20 | fits | 106,141 | 184 | 0.307 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 150,369 | 1.504 | 20 | 24 | fits | 145,856 | 145 | 0.429 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 297,000 | 2.970 | 20 | 24 | fits | 147,621 | 214 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 296,934 | 2.969 | 20 | 50 | fits | 147,621 | 214 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 402,679 | 4.027 | 20 | 50 | fits | 106,141 | 184 | 0.307 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 478,138 | 4.781 | 20 | 20 | fits | 75,525 | 30 | 0.795 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 855,869 | 8.559 | 20 | 20 | fits | 62,696 | 31 | 0.722 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 360,518 | 3.605 | 20 | 20 | fits | 105,809 | 184 | 0.297 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 302,022 | 3.020 | 20 | 200 | fits | 149,599 | 219 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 407,215 | 4.072 | 20 | 200 | fits | 105,809 | 184 | 0.297 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 302,946 | 3.029 | 20 | 20 | fits | 149,599 | 219 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 407,919 | 4.079 | 20 | 20 | fits | 105,809 | 184 | 0.297 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 146,180 | 1.462 | 20 | 24 | fits | 145,646 | 146 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 305,596 | 3.056 | 20 | 24 | fits | 149,599 | 219 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 305,530 | 3.055 | 20 | 50 | fits | 149,599 | 219 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 410,943 | 4.109 | 20 | 50 | fits | 105,809 | 184 | 0.297 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 491,311 | 4.913 | 20 | 20 | fits | 80,434 | 28 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 841,549 | 8.415 | 20 | 20 | fits | 47,499 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 437,819 | 4.378 | 20 | 20 | fits | 107,101 | 187 | 0.289 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 376,762 | 3.768 | 20 | 200 | fits | 148,369 | 215 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 483,247 | 4.832 | 20 | 200 | fits | 107,101 | 187 | 0.289 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 377,686 | 3.777 | 20 | 20 | fits | 148,369 | 215 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 483,951 | 4.840 | 20 | 20 | fits | 107,101 | 187 | 0.289 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 222,028 | 2.220 | 20 | 24 | fits | 145,337 | 146 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 380,336 | 3.803 | 20 | 24 | fits | 148,369 | 215 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 380,270 | 3.803 | 20 | 50 | fits | 148,369 | 215 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 486,975 | 4.870 | 20 | 50 | fits | 107,101 | 187 | 0.289 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 567,539 | 5.675 | 20 | 20 | fits | 80,630 | 28 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 917,754 | 9.178 | 20 | 20 | fits | 47,486 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 425,319 | 4.253 | 20 | 20 | fits | 107,101 | 187 | 0.289 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 364,262 | 3.643 | 20 | 200 | fits | 148,369 | 215 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 470,747 | 4.707 | 20 | 200 | fits | 107,101 | 187 | 0.289 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 365,186 | 3.652 | 20 | 20 | fits | 148,369 | 215 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 471,451 | 4.715 | 20 | 20 | fits | 107,101 | 187 | 0.289 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 209,528 | 2.095 | 20 | 24 | fits | 145,337 | 146 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 367,836 | 3.678 | 20 | 24 | fits | 148,369 | 215 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 367,770 | 3.678 | 20 | 50 | fits | 148,369 | 215 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 474,475 | 4.745 | 20 | 50 | fits | 107,101 | 187 | 0.289 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 555,039 | 5.550 | 20 | 20 | fits | 80,630 | 28 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 905,254 | 9.053 | 20 | 20 | fits | 47,486 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 412,819 | 4.128 | 20 | 20 | fits | 107,101 | 187 | 0.289 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 351,762 | 3.518 | 20 | 200 | fits | 148,369 | 215 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 458,247 | 4.582 | 20 | 200 | fits | 107,101 | 187 | 0.289 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 352,686 | 3.527 | 20 | 20 | fits | 148,369 | 215 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 458,951 | 4.590 | 20 | 20 | fits | 107,101 | 187 | 0.289 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 197,028 | 1.970 | 20 | 24 | fits | 145,337 | 146 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 355,336 | 3.553 | 20 | 24 | fits | 148,369 | 215 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 355,270 | 3.553 | 20 | 50 | fits | 148,369 | 215 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 461,975 | 4.620 | 20 | 50 | fits | 107,101 | 187 | 0.289 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 542,539 | 5.425 | 20 | 20 | fits | 80,630 | 28 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 892,754 | 8.928 | 20 | 20 | fits | 47,486 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 400,319 | 4.003 | 20 | 20 | fits | 107,101 | 187 | 0.289 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 339,262 | 3.393 | 20 | 200 | fits | 148,369 | 215 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 445,747 | 4.457 | 20 | 200 | fits | 107,101 | 187 | 0.289 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 340,186 | 3.402 | 20 | 20 | fits | 148,369 | 215 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 446,451 | 4.465 | 20 | 20 | fits | 107,101 | 187 | 0.289 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 184,528 | 1.845 | 20 | 24 | fits | 145,337 | 146 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 342,836 | 3.428 | 20 | 24 | fits | 148,369 | 215 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 342,770 | 3.428 | 20 | 50 | fits | 148,369 | 215 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 449,475 | 4.495 | 20 | 50 | fits | 107,101 | 187 | 0.289 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 530,039 | 5.300 | 20 | 20 | fits | 80,630 | 28 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 880,254 | 8.803 | 20 | 20 | fits | 47,486 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 387,819 | 3.878 | 20 | 20 | fits | 107,101 | 187 | 0.289 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 326,762 | 3.268 | 20 | 200 | fits | 148,369 | 215 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 433,247 | 4.332 | 20 | 200 | fits | 107,101 | 187 | 0.289 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 327,686 | 3.277 | 20 | 20 | fits | 148,369 | 215 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 433,951 | 4.340 | 20 | 20 | fits | 107,101 | 187 | 0.289 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 172,028 | 1.720 | 20 | 24 | fits | 145,337 | 146 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 330,336 | 3.303 | 20 | 24 | fits | 148,369 | 215 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 330,270 | 3.303 | 20 | 50 | fits | 148,369 | 215 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 436,975 | 4.370 | 20 | 50 | fits | 107,101 | 187 | 0.289 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 517,539 | 5.175 | 20 | 20 | fits | 80,630 | 28 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 867,754 | 8.678 | 20 | 20 | fits | 47,486 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 375,319 | 3.753 | 20 | 20 | fits | 107,101 | 187 | 0.289 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 314,262 | 3.143 | 20 | 200 | fits | 148,369 | 215 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 420,747 | 4.207 | 20 | 200 | fits | 107,101 | 187 | 0.289 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 315,186 | 3.152 | 20 | 20 | fits | 148,369 | 215 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 421,451 | 4.215 | 20 | 20 | fits | 107,101 | 187 | 0.289 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 159,528 | 1.595 | 20 | 24 | fits | 145,337 | 146 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 317,836 | 3.178 | 20 | 24 | fits | 148,369 | 215 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 317,770 | 3.178 | 20 | 50 | fits | 148,369 | 215 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 424,475 | 4.245 | 20 | 50 | fits | 107,101 | 187 | 0.289 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 505,039 | 5.050 | 20 | 20 | fits | 80,630 | 28 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 855,254 | 8.553 | 20 | 20 | fits | 47,486 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 362,819 | 3.628 | 20 | 20 | fits | 107,101 | 187 | 0.289 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 301,762 | 3.018 | 20 | 200 | fits | 148,369 | 215 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 408,247 | 4.082 | 20 | 200 | fits | 107,101 | 187 | 0.289 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 302,686 | 3.027 | 20 | 20 | fits | 148,369 | 215 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 408,951 | 4.090 | 20 | 20 | fits | 107,101 | 187 | 0.289 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 147,028 | 1.470 | 20 | 24 | fits | 145,337 | 146 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 305,336 | 3.053 | 20 | 24 | fits | 148,369 | 215 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 305,270 | 3.053 | 20 | 50 | fits | 148,369 | 215 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 411,975 | 4.120 | 20 | 50 | fits | 107,101 | 187 | 0.289 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 492,539 | 4.925 | 20 | 20 | fits | 80,630 | 28 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 842,754 | 8.428 | 20 | 20 | fits | 47,486 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 361,132 | 3.611 | 20 | 20 | fits | 105,787 | 184 | 0.296 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 302,658 | 3.027 | 20 | 200 | fits | 149,747 | 219 | 0.393 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 407,829 | 4.078 | 20 | 200 | fits | 105,787 | 184 | 0.296 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 303,582 | 3.036 | 20 | 20 | fits | 149,747 | 219 | 0.393 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 408,533 | 4.085 | 20 | 20 | fits | 105,787 | 184 | 0.296 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 147,402 | 1.474 | 20 | 24 | fits | 144,909 | 143 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 306,232 | 3.062 | 20 | 24 | fits | 149,747 | 219 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 306,166 | 3.062 | 20 | 50 | fits | 149,747 | 219 | 0.393 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 411,557 | 4.116 | 20 | 50 | fits | 105,787 | 184 | 0.296 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 491,857 | 4.919 | 20 | 20 | fits | 80,366 | 28 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 842,053 | 8.421 | 20 | 20 | fits | 47,499 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 361,587 | 3.616 | 20 | 20 | fits | 105,787 | 184 | 0.296 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 303,113 | 3.031 | 20 | 200 | fits | 149,665 | 219 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 408,284 | 4.083 | 20 | 200 | fits | 105,787 | 184 | 0.296 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 304,037 | 3.040 | 20 | 20 | fits | 149,665 | 219 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 408,988 | 4.090 | 20 | 20 | fits | 105,787 | 184 | 0.296 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 147,939 | 1.479 | 20 | 24 | fits | 144,886 | 143 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 306,687 | 3.067 | 20 | 24 | fits | 149,665 | 219 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 306,621 | 3.066 | 20 | 50 | fits | 149,665 | 219 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 412,012 | 4.120 | 20 | 50 | fits | 105,787 | 184 | 0.296 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 492,377 | 4.924 | 20 | 20 | fits | 80,431 | 28 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 842,573 | 8.426 | 20 | 20 | fits | 47,499 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 343,393 | 3.434 | 20 | 20 | fits | 105,984 | 184 | 0.304 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 296,275 | 2.963 | 20 | 200 | fits | 147,711 | 214 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 401,643 | 4.016 | 20 | 200 | fits | 105,984 | 184 | 0.304 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 297,199 | 2.972 | 20 | 20 | fits | 147,711 | 214 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 402,347 | 4.023 | 20 | 20 | fits | 105,984 | 184 | 0.304 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 153,128 | 1.531 | 20 | 24 | fits | 144,657 | 142 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 299,849 | 2.998 | 20 | 24 | fits | 147,711 | 214 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 299,783 | 2.998 | 20 | 50 | fits | 147,711 | 214 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 405,371 | 4.054 | 20 | 50 | fits | 105,984 | 184 | 0.304 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 485,916 | 4.859 | 20 | 20 | fits | 80,611 | 28 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 935,715 | 9.357 | 20 | 20 | fits | 57,883 | 25 | 0.687 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 343,953 | 3.440 | 20 | 20 | fits | 105,984 | 184 | 0.304 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 296,835 | 2.968 | 20 | 200 | fits | 147,711 | 214 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 402,203 | 4.022 | 20 | 200 | fits | 105,984 | 184 | 0.304 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 297,759 | 2.978 | 20 | 20 | fits | 147,711 | 214 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 402,907 | 4.029 | 20 | 20 | fits | 105,984 | 184 | 0.304 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 153,688 | 1.537 | 20 | 24 | fits | 144,657 | 142 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 300,409 | 3.004 | 20 | 24 | fits | 147,711 | 214 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 300,343 | 3.003 | 20 | 50 | fits | 147,711 | 214 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 405,931 | 4.059 | 20 | 50 | fits | 105,984 | 184 | 0.304 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 486,476 | 4.865 | 20 | 20 | fits | 80,611 | 28 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 936,836 | 9.368 | 20 | 20 | fits | 57,501 | 24 | 0.674 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 340,914 | 3.409 | 20 | 20 | fits | 104,426 | 184 | 0.324 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 290,262 | 2.903 | 20 | 200 | fits | 147,254 | 253 | 0.360 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 394,072 | 3.941 | 20 | 200 | fits | 104,426 | 184 | 0.324 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 291,186 | 2.912 | 20 | 20 | fits | 147,254 | 253 | 0.360 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 394,776 | 3.948 | 20 | 20 | fits | 104,426 | 184 | 0.324 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 147,572 | 1.476 | 20 | 24 | fits | 150,537 | 111 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 293,836 | 2.938 | 20 | 24 | fits | 147,254 | 253 | 0.360 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 293,770 | 2.938 | 20 | 50 | fits | 147,254 | 253 | 0.360 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 397,800 | 3.978 | 20 | 50 | fits | 104,426 | 184 | 0.324 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 478,383 | 4.784 | 20 | 20 | fits | 80,649 | 29 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 927,526 | 9.275 | 20 | 20 | fits | 57,091 | 24 | 0.668 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 339,782 | 3.398 | 20 | 20 | fits | 109,317 | 176 | 0.283 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 284,041 | 2.840 | 20 | 200 | fits | 146,353 | 230 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 392,742 | 3.927 | 20 | 200 | fits | 109,317 | 176 | 0.283 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 284,965 | 2.850 | 20 | 20 | fits | 146,353 | 230 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 393,446 | 3.934 | 20 | 20 | fits | 109,317 | 176 | 0.283 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 142,252 | 1.423 | 20 | 24 | fits | 144,657 | 142 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 287,615 | 2.876 | 20 | 24 | fits | 146,353 | 230 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 287,549 | 2.875 | 20 | 50 | fits | 146,353 | 230 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 396,470 | 3.965 | 20 | 50 | fits | 109,317 | 176 | 0.283 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 486,023 | 4.860 | 20 | 20 | fits | 77,757 | 37 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 923,124 | 9.231 | 20 | 20 | fits | 57,167 | 24 | 0.670 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 363,082 | 3.631 | 20 | 20 | fits | 120,766 | 187 | 0.365 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 284,770 | 2.848 | 20 | 200 | fits | 146,522 | 231 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 416,889 | 4.169 | 20 | 200 | fits | 120,766 | 187 | 0.365 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 285,694 | 2.857 | 20 | 20 | fits | 146,522 | 231 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 417,593 | 4.176 | 20 | 20 | fits | 120,766 | 187 | 0.365 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 142,812 | 1.428 | 20 | 24 | fits | 144,657 | 142 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 288,344 | 2.883 | 20 | 24 | fits | 146,522 | 231 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 288,278 | 2.883 | 20 | 50 | fits | 146,522 | 231 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 420,617 | 4.206 | 20 | 50 | fits | 120,766 | 187 | 0.365 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 577,597 | 5.776 | 20 | 20 | fits | 80,240 | 29 | 0.756 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 928,183 | 9.282 | 20 | 20 | fits | 47,568 | 20 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 358,822 | 3.588 | 20 | 20 | fits | 117,104 | 187 | 0.320 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 295,400 | 2.954 | 20 | 200 | fits | 146,864 | 230 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 411,888 | 4.119 | 20 | 200 | fits | 117,104 | 187 | 0.320 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 296,324 | 2.963 | 20 | 20 | fits | 146,864 | 230 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 412,592 | 4.126 | 20 | 20 | fits | 117,104 | 187 | 0.320 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 143,083 | 1.431 | 20 | 24 | fits | 144,739 | 143 | 0.418 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 298,974 | 2.990 | 20 | 24 | fits | 146,864 | 230 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 298,908 | 2.989 | 20 | 50 | fits | 146,864 | 230 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 415,616 | 4.156 | 20 | 50 | fits | 117,104 | 187 | 0.320 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 572,657 | 5.727 | 20 | 20 | fits | 80,301 | 29 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 941,177 | 9.412 | 20 | 20 | fits | 53,132 | 27 | 0.758 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 344,529 | 3.445 | 20 | 20 | fits | 108,987 | 176 | 0.275 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 288,654 | 2.887 | 20 | 200 | fits | 145,528 | 225 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 397,025 | 3.970 | 20 | 200 | fits | 108,987 | 176 | 0.275 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 289,578 | 2.896 | 20 | 20 | fits | 145,528 | 225 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 397,729 | 3.977 | 20 | 20 | fits | 108,987 | 176 | 0.275 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 147,690 | 1.477 | 20 | 24 | fits | 144,657 | 142 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 292,228 | 2.922 | 20 | 24 | fits | 145,528 | 225 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 292,162 | 2.922 | 20 | 50 | fits | 145,528 | 225 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 400,753 | 4.008 | 20 | 50 | fits | 108,987 | 176 | 0.275 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 496,240 | 4.962 | 20 | 20 | fits | 83,624 | 35 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 847,002 | 8.470 | 20 | 20 | fits | 47,586 | 20 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 361,346 | 3.613 | 20 | 20 | fits | 113,883 | 182 | 0.343 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 289,430 | 2.894 | 20 | 200 | fits | 145,744 | 226 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 414,666 | 4.147 | 20 | 200 | fits | 113,883 | 182 | 0.343 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 290,354 | 2.904 | 20 | 20 | fits | 145,744 | 226 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 415,370 | 4.154 | 20 | 20 | fits | 113,883 | 182 | 0.343 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 148,250 | 1.482 | 20 | 24 | fits | 144,657 | 142 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 293,004 | 2.930 | 20 | 24 | fits | 145,744 | 226 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 292,938 | 2.929 | 20 | 50 | fits | 145,744 | 226 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 418,394 | 4.184 | 20 | 50 | fits | 113,883 | 182 | 0.343 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 498,845 | 4.988 | 20 | 20 | fits | 80,517 | 28 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 848,984 | 8.490 | 20 | 20 | fits | 47,504 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 357,525 | 3.575 | 20 | 20 | fits | 109,015 | 175 | 0.277 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 301,574 | 3.016 | 20 | 200 | fits | 147,042 | 230 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 409,973 | 4.100 | 20 | 200 | fits | 109,015 | 175 | 0.277 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 302,498 | 3.025 | 20 | 20 | fits | 147,042 | 230 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 410,677 | 4.107 | 20 | 20 | fits | 109,015 | 175 | 0.277 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 148,910 | 1.489 | 20 | 24 | fits | 144,757 | 143 | 0.418 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 305,148 | 3.051 | 20 | 24 | fits | 147,042 | 230 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 305,082 | 3.051 | 20 | 50 | fits | 147,042 | 230 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 413,701 | 4.137 | 20 | 50 | fits | 109,015 | 175 | 0.277 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 494,142 | 4.941 | 20 | 20 | fits | 80,507 | 28 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 849,357 | 8.494 | 20 | 20 | fits | 47,581 | 20 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 357,055 | 3.571 | 20 | 20 | fits | 106,909 | 187 | 0.285 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 296,074 | 2.961 | 20 | 200 | fits | 146,335 | 210 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 402,367 | 4.024 | 20 | 200 | fits | 106,909 | 187 | 0.285 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 296,998 | 2.970 | 20 | 20 | fits | 146,335 | 210 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 403,071 | 4.031 | 20 | 20 | fits | 106,909 | 187 | 0.285 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 154,303 | 1.543 | 20 | 24 | fits | 144,782 | 142 | 0.418 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 299,648 | 2.996 | 20 | 24 | fits | 146,335 | 210 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 299,582 | 2.996 | 20 | 50 | fits | 146,335 | 210 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 406,095 | 4.061 | 20 | 50 | fits | 106,909 | 187 | 0.285 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 486,516 | 4.865 | 20 | 20 | fits | 80,487 | 28 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 859,813 | 8.598 | 20 | 20 | fits | 53,106 | 27 | 0.757 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 344,646 | 3.446 | 20 | 20 | fits | 105,634 | 184 | 0.293 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 286,261 | 2.863 | 20 | 200 | fits | 148,421 | 219 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 391,279 | 3.913 | 20 | 200 | fits | 105,634 | 184 | 0.293 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 287,185 | 2.872 | 20 | 20 | fits | 148,421 | 219 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 391,983 | 3.920 | 20 | 20 | fits | 105,634 | 184 | 0.293 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 142,404 | 1.424 | 20 | 24 | fits | 144,811 | 142 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 289,835 | 2.898 | 20 | 24 | fits | 148,421 | 219 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 289,769 | 2.898 | 20 | 50 | fits | 148,421 | 219 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 395,007 | 3.950 | 20 | 50 | fits | 105,634 | 184 | 0.293 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 475,433 | 4.754 | 20 | 20 | fits | 80,492 | 28 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 849,418 | 8.494 | 20 | 20 | fits | 48,116 | 20 | 0.722 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 345,206 | 3.452 | 20 | 20 | fits | 105,634 | 184 | 0.293 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 286,821 | 2.868 | 20 | 200 | fits | 148,421 | 219 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 391,839 | 3.918 | 20 | 200 | fits | 105,634 | 184 | 0.293 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 287,745 | 2.877 | 20 | 20 | fits | 148,421 | 219 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 392,543 | 3.925 | 20 | 20 | fits | 105,634 | 184 | 0.293 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 142,964 | 1.430 | 20 | 24 | fits | 144,811 | 142 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 290,395 | 2.904 | 20 | 24 | fits | 148,421 | 219 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 290,329 | 2.903 | 20 | 50 | fits | 148,421 | 219 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 395,567 | 3.956 | 20 | 50 | fits | 105,634 | 184 | 0.293 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 470,884 | 4.709 | 20 | 20 | fits | 75,383 | 30 | 0.794 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 849,717 | 8.497 | 20 | 20 | fits | 57,207 | 24 | 0.670 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 352,310 | 3.523 | 20 | 20 | fits | 112,840 | 191 | 0.340 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 287,012 | 2.870 | 20 | 200 | fits | 148,421 | 219 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 399,236 | 3.992 | 20 | 200 | fits | 112,840 | 191 | 0.340 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 287,936 | 2.879 | 20 | 20 | fits | 148,421 | 219 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 399,940 | 3.999 | 20 | 20 | fits | 112,840 | 191 | 0.340 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 143,155 | 1.432 | 20 | 24 | fits | 144,811 | 142 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 290,586 | 2.906 | 20 | 24 | fits | 148,421 | 219 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 290,520 | 2.905 | 20 | 50 | fits | 148,421 | 219 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 402,964 | 4.030 | 20 | 50 | fits | 112,840 | 191 | 0.340 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 498,372 | 4.984 | 20 | 20 | fits | 83,545 | 35 | 0.761 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 848,982 | 8.490 | 20 | 20 | fits | 47,581 | 20 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 368,600 | 3.686 | 20 | 20 | fits | 117,794 | 196 | 0.385 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 287,155 | 2.872 | 20 | 200 | fits | 148,564 | 220 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 416,120 | 4.161 | 20 | 200 | fits | 117,794 | 196 | 0.385 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 288,079 | 2.881 | 20 | 20 | fits | 148,564 | 220 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 416,824 | 4.168 | 20 | 20 | fits | 117,794 | 196 | 0.385 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 143,155 | 1.432 | 20 | 24 | fits | 144,811 | 142 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 290,729 | 2.907 | 20 | 24 | fits | 148,564 | 220 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 290,663 | 2.907 | 20 | 50 | fits | 148,564 | 220 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 419,848 | 4.198 | 20 | 50 | fits | 117,794 | 196 | 0.385 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 500,149 | 5.001 | 20 | 20 | fits | 80,367 | 28 | 0.757 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 850,295 | 8.503 | 20 | 20 | fits | 47,499 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 345,336 | 3.453 | 20 | 20 | fits | 105,746 | 185 | 0.294 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 286,951 | 2.870 | 20 | 200 | fits | 148,360 | 219 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 392,081 | 3.921 | 20 | 200 | fits | 105,746 | 185 | 0.294 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 287,875 | 2.879 | 20 | 20 | fits | 148,360 | 219 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 392,785 | 3.928 | 20 | 20 | fits | 105,746 | 185 | 0.294 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 143,155 | 1.432 | 20 | 24 | fits | 144,811 | 142 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 290,525 | 2.905 | 20 | 24 | fits | 148,360 | 219 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 290,459 | 2.905 | 20 | 50 | fits | 148,360 | 219 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 395,809 | 3.958 | 20 | 50 | fits | 105,746 | 185 | 0.294 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 491,427 | 4.914 | 20 | 20 | fits | 83,755 | 35 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 842,238 | 8.422 | 20 | 20 | fits | 47,581 | 20 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 362,565 | 3.626 | 20 | 20 | fits | 111,141 | 191 | 0.366 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 287,886 | 2.879 | 20 | 200 | fits | 147,723 | 215 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 410,198 | 4.102 | 20 | 200 | fits | 111,141 | 191 | 0.366 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 288,810 | 2.888 | 20 | 20 | fits | 147,723 | 215 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 410,902 | 4.109 | 20 | 20 | fits | 111,141 | 191 | 0.366 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 144,727 | 1.447 | 20 | 24 | fits | 144,811 | 142 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 291,460 | 2.915 | 20 | 24 | fits | 147,723 | 215 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 291,394 | 2.914 | 20 | 50 | fits | 147,723 | 215 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 413,926 | 4.139 | 20 | 50 | fits | 111,141 | 191 | 0.366 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 494,364 | 4.944 | 20 | 20 | fits | 80,504 | 28 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 844,552 | 8.446 | 20 | 20 | fits | 47,499 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 359,097 | 3.591 | 20 | 20 | fits | 105,787 | 184 | 0.296 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 300,623 | 3.006 | 20 | 200 | fits | 149,697 | 219 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 405,794 | 4.058 | 20 | 200 | fits | 105,787 | 184 | 0.296 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 301,547 | 3.015 | 20 | 20 | fits | 149,697 | 219 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 406,498 | 4.065 | 20 | 20 | fits | 105,787 | 184 | 0.296 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 145,387 | 1.454 | 20 | 24 | fits | 144,911 | 143 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 304,197 | 3.042 | 20 | 24 | fits | 149,697 | 219 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 304,131 | 3.041 | 20 | 50 | fits | 149,697 | 219 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 409,522 | 4.095 | 20 | 50 | fits | 105,787 | 184 | 0.296 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 489,947 | 4.899 | 20 | 20 | fits | 80,491 | 28 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 927,447 | 9.274 | 20 | 20 | fits | 48,784 | 22 | 0.729 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 340,631 | 3.406 | 20 | 20 | fits | 105,984 | 184 | 0.304 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 293,513 | 2.935 | 20 | 200 | fits | 147,650 | 214 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 398,881 | 3.989 | 20 | 200 | fits | 105,984 | 184 | 0.304 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 294,437 | 2.944 | 20 | 20 | fits | 147,650 | 214 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 399,585 | 3.996 | 20 | 20 | fits | 105,984 | 184 | 0.304 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 150,427 | 1.504 | 20 | 24 | fits | 144,629 | 142 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 297,087 | 2.971 | 20 | 24 | fits | 147,650 | 214 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 297,021 | 2.970 | 20 | 50 | fits | 147,650 | 214 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 402,609 | 4.026 | 20 | 50 | fits | 105,984 | 184 | 0.304 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 483,340 | 4.833 | 20 | 20 | fits | 80,797 | 28 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 939,324 | 9.393 | 20 | 20 | fits | 48,055 | 20 | 0.721 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 341,288 | 3.413 | 20 | 20 | fits | 105,984 | 184 | 0.304 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 294,170 | 2.942 | 20 | 200 | fits | 147,650 | 214 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 399,538 | 3.995 | 20 | 200 | fits | 105,984 | 184 | 0.304 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 295,094 | 2.951 | 20 | 20 | fits | 147,650 | 214 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 400,242 | 4.002 | 20 | 20 | fits | 105,984 | 184 | 0.304 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 151,084 | 1.511 | 20 | 24 | fits | 144,657 | 142 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 297,744 | 2.977 | 20 | 24 | fits | 147,650 | 214 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 297,678 | 2.977 | 20 | 50 | fits | 147,650 | 214 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 403,266 | 4.033 | 20 | 50 | fits | 105,984 | 184 | 0.304 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 483,997 | 4.840 | 20 | 20 | fits | 80,797 | 28 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 941,379 | 9.414 | 20 | 20 | fits | 47,818 | 20 | 0.714 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 341,848 | 3.418 | 20 | 20 | fits | 105,984 | 184 | 0.304 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 294,730 | 2.947 | 20 | 200 | fits | 147,650 | 214 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 400,098 | 4.001 | 20 | 200 | fits | 105,984 | 184 | 0.304 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 295,654 | 2.957 | 20 | 20 | fits | 147,650 | 214 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 400,802 | 4.008 | 20 | 20 | fits | 105,984 | 184 | 0.304 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 151,644 | 1.516 | 20 | 24 | fits | 144,657 | 142 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 298,304 | 2.983 | 20 | 24 | fits | 147,650 | 214 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 298,238 | 2.982 | 20 | 50 | fits | 147,650 | 214 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 403,826 | 4.038 | 20 | 50 | fits | 105,984 | 184 | 0.304 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 479,437 | 4.794 | 20 | 20 | fits | 75,677 | 30 | 0.796 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 941,408 | 9.414 | 20 | 20 | fits | 57,152 | 24 | 0.670 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 349,231 | 3.492 | 20 | 20 | fits | 113,100 | 191 | 0.347 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 295,290 | 2.953 | 20 | 200 | fits | 147,650 | 214 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 407,774 | 4.078 | 20 | 200 | fits | 113,100 | 191 | 0.347 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 296,214 | 2.962 | 20 | 20 | fits | 147,650 | 214 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 408,478 | 4.085 | 20 | 20 | fits | 113,100 | 191 | 0.347 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 152,204 | 1.522 | 20 | 24 | fits | 144,657 | 142 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 298,864 | 2.989 | 20 | 24 | fits | 147,650 | 214 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 298,798 | 2.988 | 20 | 50 | fits | 147,650 | 214 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 411,502 | 4.115 | 20 | 50 | fits | 113,100 | 191 | 0.347 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 587,270 | 5.873 | 20 | 20 | fits | 84,051 | 35 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 937,923 | 9.379 | 20 | 20 | fits | 47,568 | 20 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 449,790 | 4.498 | 20 | 20 | fits | 119,626 | 202 | 0.350 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 293,511 | 2.935 | 20 | 200 | fits | 145,311 | 209 | 0.406 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 504,080 | 5.041 | 20 | 200 | fits | 119,626 | 202 | 0.350 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 294,435 | 2.944 | 20 | 20 | fits | 145,311 | 209 | 0.406 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 504,784 | 5.048 | 20 | 20 | fits | 119,626 | 202 | 0.350 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 152,764 | 1.528 | 20 | 24 | fits | 144,657 | 142 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 297,085 | 2.971 | 20 | 24 | fits | 145,311 | 209 | 0.406 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 297,019 | 2.970 | 20 | 50 | fits | 145,311 | 209 | 0.406 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 507,808 | 5.078 | 20 | 50 | fits | 119,626 | 202 | 0.350 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 588,320 | 5.883 | 20 | 20 | fits | 80,578 | 28 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 938,460 | 9.385 | 20 | 20 | fits | 47,486 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 340,617 | 3.406 | 20 | 20 | fits | 108,875 | 175 | 0.274 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 284,742 | 2.847 | 20 | 200 | fits | 146,305 | 230 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 393,001 | 3.930 | 20 | 200 | fits | 108,875 | 175 | 0.274 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 285,666 | 2.857 | 20 | 20 | fits | 146,305 | 230 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 393,705 | 3.937 | 20 | 20 | fits | 108,875 | 175 | 0.274 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 143,001 | 1.430 | 20 | 24 | fits | 144,657 | 142 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 288,316 | 2.883 | 20 | 24 | fits | 146,305 | 230 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 288,250 | 2.882 | 20 | 50 | fits | 146,305 | 230 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 396,729 | 3.967 | 20 | 50 | fits | 108,875 | 175 | 0.274 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 477,229 | 4.772 | 20 | 20 | fits | 80,566 | 28 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 846,643 | 8.466 | 20 | 20 | fits | 47,571 | 20 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 341,791 | 3.418 | 20 | 20 | fits | 108,875 | 175 | 0.274 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 285,916 | 2.859 | 20 | 200 | fits | 145,467 | 225 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 394,175 | 3.942 | 20 | 200 | fits | 108,875 | 175 | 0.274 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 286,840 | 2.868 | 20 | 20 | fits | 145,467 | 225 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 394,879 | 3.949 | 20 | 20 | fits | 108,875 | 175 | 0.274 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 145,013 | 1.450 | 20 | 24 | fits | 144,657 | 142 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 289,490 | 2.895 | 20 | 24 | fits | 145,467 | 225 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 289,424 | 2.894 | 20 | 50 | fits | 145,467 | 225 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 397,903 | 3.979 | 20 | 50 | fits | 108,875 | 175 | 0.274 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 478,552 | 4.786 | 20 | 20 | fits | 80,715 | 29 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 847,037 | 8.470 | 20 | 20 | fits | 47,510 | 20 | 0.708 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 346,618 | 3.466 | 20 | 20 | fits | 113,025 | 182 | 0.301 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 286,476 | 2.865 | 20 | 200 | fits | 145,467 | 225 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 398,885 | 3.989 | 20 | 200 | fits | 113,025 | 182 | 0.301 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 287,400 | 2.874 | 20 | 20 | fits | 145,467 | 225 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 399,589 | 3.996 | 20 | 20 | fits | 113,025 | 182 | 0.301 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 145,573 | 1.456 | 20 | 24 | fits | 144,657 | 142 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 290,050 | 2.901 | 20 | 24 | fits | 145,467 | 225 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 289,984 | 2.900 | 20 | 50 | fits | 145,467 | 225 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 402,613 | 4.026 | 20 | 50 | fits | 113,025 | 182 | 0.301 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 496,006 | 4.960 | 20 | 20 | fits | 81,490 | 29 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 852,061 | 8.521 | 20 | 20 | fits | 47,676 | 20 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 359,079 | 3.591 | 20 | 20 | fits | 113,923 | 182 | 0.343 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 287,187 | 2.872 | 20 | 200 | fits | 145,618 | 226 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 412,463 | 4.125 | 20 | 200 | fits | 113,923 | 182 | 0.343 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 288,111 | 2.881 | 20 | 20 | fits | 145,618 | 226 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 413,167 | 4.132 | 20 | 20 | fits | 113,923 | 182 | 0.343 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 146,133 | 1.461 | 20 | 24 | fits | 144,657 | 142 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 290,761 | 2.908 | 20 | 24 | fits | 145,618 | 226 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 290,695 | 2.907 | 20 | 50 | fits | 145,618 | 226 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 416,191 | 4.162 | 20 | 50 | fits | 113,923 | 182 | 0.343 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 496,763 | 4.968 | 20 | 20 | fits | 80,638 | 28 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 851,750 | 8.518 | 20 | 20 | fits | 47,504 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 355,434 | 3.554 | 20 | 20 | fits | 109,015 | 175 | 0.277 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 299,483 | 2.995 | 20 | 200 | fits | 147,074 | 230 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 407,882 | 4.079 | 20 | 200 | fits | 109,015 | 175 | 0.277 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 300,407 | 3.004 | 20 | 20 | fits | 147,074 | 230 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 408,586 | 4.086 | 20 | 20 | fits | 109,015 | 175 | 0.277 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 146,757 | 1.468 | 20 | 24 | fits | 144,721 | 143 | 0.418 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 303,057 | 3.031 | 20 | 24 | fits | 147,074 | 230 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 302,991 | 3.030 | 20 | 50 | fits | 147,074 | 230 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 411,610 | 4.116 | 20 | 50 | fits | 109,015 | 175 | 0.277 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 492,111 | 4.921 | 20 | 20 | fits | 80,567 | 28 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 847,309 | 8.473 | 20 | 20 | fits | 47,504 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 354,916 | 3.549 | 20 | 20 | fits | 106,909 | 187 | 0.285 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 293,935 | 2.939 | 20 | 200 | fits | 146,274 | 210 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 400,228 | 4.002 | 20 | 200 | fits | 106,909 | 187 | 0.285 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 294,859 | 2.949 | 20 | 20 | fits | 146,274 | 210 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 400,932 | 4.009 | 20 | 20 | fits | 106,909 | 187 | 0.285 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 152,225 | 1.522 | 20 | 24 | fits | 144,811 | 142 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 297,509 | 2.975 | 20 | 24 | fits | 146,274 | 210 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 297,443 | 2.974 | 20 | 50 | fits | 146,274 | 210 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 403,956 | 4.040 | 20 | 50 | fits | 106,909 | 187 | 0.285 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 479,454 | 4.795 | 20 | 20 | fits | 75,564 | 30 | 0.795 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 857,359 | 8.574 | 20 | 20 | fits | 62,747 | 31 | 0.723 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 362,295 | 3.623 | 20 | 20 | fits | 113,911 | 193 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 294,495 | 2.945 | 20 | 200 | fits | 146,274 | 210 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 407,790 | 4.078 | 20 | 200 | fits | 113,911 | 193 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 295,419 | 2.954 | 20 | 20 | fits | 146,274 | 210 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 408,494 | 4.085 | 20 | 20 | fits | 113,911 | 193 | 0.333 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 152,785 | 1.528 | 20 | 24 | fits | 144,811 | 142 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 298,069 | 2.981 | 20 | 24 | fits | 146,274 | 210 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 298,003 | 2.980 | 20 | 50 | fits | 146,274 | 210 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 411,518 | 4.115 | 20 | 50 | fits | 113,911 | 193 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 492,069 | 4.921 | 20 | 20 | fits | 80,617 | 28 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 861,543 | 8.615 | 20 | 20 | fits | 47,949 | 20 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 361,571 | 3.616 | 20 | 20 | fits | 114,926 | 199 | 0.260 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 292,573 | 2.926 | 20 | 200 | fits | 143,792 | 204 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 406,883 | 4.069 | 20 | 200 | fits | 114,926 | 199 | 0.260 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 293,497 | 2.935 | 20 | 20 | fits | 143,792 | 204 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 407,587 | 4.076 | 20 | 20 | fits | 114,926 | 199 | 0.260 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 153,345 | 1.533 | 20 | 24 | fits | 144,811 | 142 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 296,147 | 2.961 | 20 | 24 | fits | 143,792 | 204 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 296,081 | 2.961 | 20 | 50 | fits | 143,792 | 204 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 410,611 | 4.106 | 20 | 50 | fits | 114,926 | 199 | 0.260 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 491,435 | 4.914 | 20 | 20 | fits | 80,890 | 29 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 859,920 | 8.599 | 20 | 20 | fits | 47,492 | 20 | 0.708 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 347,860 | 3.479 | 20 | 20 | fits | 106,175 | 184 | 0.308 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 300,564 | 3.006 | 20 | 200 | fits | 149,767 | 219 | 0.393 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 406,123 | 4.061 | 20 | 200 | fits | 106,175 | 184 | 0.308 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 301,488 | 3.015 | 20 | 20 | fits | 149,767 | 219 | 0.393 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 406,827 | 4.068 | 20 | 20 | fits | 106,175 | 184 | 0.308 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 145,143 | 1.451 | 20 | 24 | fits | 144,755 | 143 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 304,138 | 3.041 | 20 | 24 | fits | 149,767 | 219 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 304,072 | 3.041 | 20 | 50 | fits | 149,767 | 219 | 0.393 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 409,851 | 4.099 | 20 | 50 | fits | 106,175 | 184 | 0.308 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 490,458 | 4.905 | 20 | 20 | fits | 80,673 | 28 | 0.761 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 840,393 | 8.404 | 20 | 20 | fits | 47,486 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 348,315 | 3.483 | 20 | 20 | fits | 106,175 | 184 | 0.308 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 301,019 | 3.010 | 20 | 200 | fits | 149,685 | 219 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 406,578 | 4.066 | 20 | 200 | fits | 106,175 | 184 | 0.308 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 301,943 | 3.019 | 20 | 20 | fits | 149,685 | 219 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 407,282 | 4.073 | 20 | 20 | fits | 106,175 | 184 | 0.308 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 145,680 | 1.457 | 20 | 24 | fits | 144,732 | 143 | 0.418 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 304,593 | 3.046 | 20 | 24 | fits | 149,685 | 219 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 304,527 | 3.045 | 20 | 50 | fits | 149,685 | 219 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 410,306 | 4.103 | 20 | 50 | fits | 106,175 | 184 | 0.308 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 490,978 | 4.910 | 20 | 20 | fits | 80,738 | 28 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 840,913 | 8.409 | 20 | 20 | fits | 47,486 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 347,764 | 3.478 | 20 | 20 | fits | 109,191 | 175 | 0.282 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 291,934 | 2.919 | 20 | 200 | fits | 145,361 | 225 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 400,509 | 4.005 | 20 | 200 | fits | 109,191 | 175 | 0.282 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 292,858 | 2.929 | 20 | 20 | fits | 145,361 | 225 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 401,213 | 4.012 | 20 | 20 | fits | 109,191 | 175 | 0.282 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 151,137 | 1.511 | 20 | 24 | fits | 144,811 | 142 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 295,508 | 2.955 | 20 | 24 | fits | 145,361 | 225 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 295,442 | 2.954 | 20 | 50 | fits | 145,361 | 225 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 404,237 | 4.042 | 20 | 50 | fits | 109,191 | 175 | 0.282 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 484,804 | 4.848 | 20 | 20 | fits | 80,633 | 28 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 935,931 | 9.359 | 20 | 20 | fits | 58,151 | 25 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 348,324 | 3.483 | 20 | 20 | fits | 109,191 | 175 | 0.282 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 292,494 | 2.925 | 20 | 200 | fits | 145,361 | 225 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 401,069 | 4.011 | 20 | 200 | fits | 109,191 | 175 | 0.282 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 293,418 | 2.934 | 20 | 20 | fits | 145,361 | 225 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 401,773 | 4.018 | 20 | 20 | fits | 109,191 | 175 | 0.282 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 151,697 | 1.517 | 20 | 24 | fits | 144,811 | 142 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 296,068 | 2.961 | 20 | 24 | fits | 145,361 | 225 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 296,002 | 2.960 | 20 | 50 | fits | 145,361 | 225 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 404,797 | 4.048 | 20 | 50 | fits | 109,191 | 175 | 0.282 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 485,364 | 4.854 | 20 | 20 | fits | 80,633 | 28 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 936,703 | 9.367 | 20 | 20 | fits | 57,571 | 24 | 0.677 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 348,884 | 3.489 | 20 | 20 | fits | 109,191 | 175 | 0.282 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 293,054 | 2.931 | 20 | 200 | fits | 145,361 | 225 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 401,629 | 4.016 | 20 | 200 | fits | 109,191 | 175 | 0.282 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 293,978 | 2.940 | 20 | 20 | fits | 145,361 | 225 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 402,333 | 4.023 | 20 | 20 | fits | 109,191 | 175 | 0.282 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 152,257 | 1.523 | 20 | 24 | fits | 144,811 | 142 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 296,628 | 2.966 | 20 | 24 | fits | 145,361 | 225 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 296,562 | 2.966 | 20 | 50 | fits | 145,361 | 225 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 405,357 | 4.054 | 20 | 50 | fits | 109,191 | 175 | 0.282 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 486,073 | 4.861 | 20 | 20 | fits | 80,782 | 29 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 936,597 | 9.366 | 20 | 20 | fits | 57,161 | 24 | 0.671 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 349,444 | 3.494 | 20 | 20 | fits | 109,303 | 176 | 0.283 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 293,614 | 2.936 | 20 | 200 | fits | 145,361 | 225 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 402,301 | 4.023 | 20 | 200 | fits | 109,303 | 176 | 0.283 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 294,538 | 2.945 | 20 | 20 | fits | 145,361 | 225 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 403,005 | 4.030 | 20 | 20 | fits | 109,303 | 176 | 0.283 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 152,817 | 1.528 | 20 | 24 | fits | 144,811 | 142 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 297,188 | 2.972 | 20 | 24 | fits | 145,361 | 225 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 297,122 | 2.971 | 20 | 50 | fits | 145,361 | 225 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 406,029 | 4.060 | 20 | 50 | fits | 109,303 | 176 | 0.283 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 495,715 | 4.957 | 20 | 20 | fits | 77,890 | 37 | 0.788 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 934,241 | 9.342 | 20 | 20 | fits | 57,237 | 24 | 0.673 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 372,965 | 3.730 | 20 | 20 | fits | 121,070 | 188 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 294,334 | 2.943 | 20 | 200 | fits | 145,521 | 226 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 426,757 | 4.268 | 20 | 200 | fits | 121,070 | 188 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 295,258 | 2.953 | 20 | 20 | fits | 145,521 | 226 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 427,461 | 4.275 | 20 | 20 | fits | 121,070 | 188 | 0.372 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 153,377 | 1.534 | 20 | 24 | fits | 144,811 | 142 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 297,908 | 2.979 | 20 | 24 | fits | 145,521 | 226 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 297,842 | 2.978 | 20 | 50 | fits | 145,521 | 226 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 430,485 | 4.305 | 20 | 50 | fits | 121,070 | 188 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 588,491 | 5.885 | 20 | 20 | fits | 80,444 | 29 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 939,453 | 9.395 | 20 | 20 | fits | 47,638 | 20 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 447,087 | 4.471 | 20 | 20 | fits | 117,230 | 202 | 0.308 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 306,440 | 3.064 | 20 | 200 | fits | 147,049 | 208 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 500,536 | 5.005 | 20 | 200 | fits | 117,230 | 202 | 0.308 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 307,364 | 3.074 | 20 | 20 | fits | 147,049 | 208 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 501,240 | 5.012 | 20 | 20 | fits | 117,230 | 202 | 0.308 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 154,019 | 1.540 | 20 | 24 | fits | 144,893 | 143 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 310,014 | 3.100 | 20 | 24 | fits | 147,049 | 208 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 309,948 | 3.099 | 20 | 50 | fits | 147,049 | 208 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 504,264 | 5.043 | 20 | 50 | fits | 117,230 | 202 | 0.308 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 584,513 | 5.845 | 20 | 20 | fits | 80,315 | 28 | 0.757 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 952,559 | 9.526 | 20 | 20 | fits | 53,117 | 27 | 0.758 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 348,521 | 3.485 | 20 | 20 | fits | 107,015 | 188 | 0.287 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 287,495 | 2.875 | 20 | 200 | fits | 146,262 | 210 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 393,894 | 3.939 | 20 | 200 | fits | 107,015 | 188 | 0.287 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 288,419 | 2.884 | 20 | 20 | fits | 146,262 | 210 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 394,598 | 3.946 | 20 | 20 | fits | 107,015 | 188 | 0.287 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 145,797 | 1.458 | 20 | 24 | fits | 144,811 | 142 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 291,069 | 2.911 | 20 | 24 | fits | 146,262 | 210 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 291,003 | 2.910 | 20 | 50 | fits | 146,262 | 210 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 397,622 | 3.976 | 20 | 50 | fits | 107,015 | 188 | 0.287 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 493,175 | 4.932 | 20 | 20 | fits | 83,757 | 35 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 843,963 | 8.440 | 20 | 20 | fits | 47,568 | 20 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 365,297 | 3.653 | 20 | 20 | fits | 112,105 | 194 | 0.353 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 288,256 | 2.883 | 20 | 200 | fits | 146,463 | 211 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 411,532 | 4.115 | 20 | 200 | fits | 112,105 | 194 | 0.353 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 289,180 | 2.892 | 20 | 20 | fits | 146,463 | 211 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 412,236 | 4.122 | 20 | 20 | fits | 112,105 | 194 | 0.353 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 146,357 | 1.464 | 20 | 24 | fits | 144,811 | 142 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 291,830 | 2.918 | 20 | 24 | fits | 146,463 | 211 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 291,764 | 2.918 | 20 | 50 | fits | 146,463 | 211 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 415,260 | 4.153 | 20 | 50 | fits | 112,105 | 194 | 0.353 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 495,844 | 4.958 | 20 | 20 | fits | 80,650 | 28 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 846,009 | 8.460 | 20 | 20 | fits | 47,486 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 361,991 | 3.620 | 20 | 20 | fits | 107,043 | 187 | 0.289 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 300,889 | 3.009 | 20 | 200 | fits | 148,331 | 215 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 407,316 | 4.073 | 20 | 200 | fits | 107,043 | 187 | 0.289 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 301,813 | 3.018 | 20 | 20 | fits | 148,331 | 215 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 408,020 | 4.080 | 20 | 20 | fits | 107,043 | 187 | 0.289 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 147,017 | 1.470 | 20 | 24 | fits | 144,911 | 143 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 304,463 | 3.045 | 20 | 24 | fits | 148,331 | 215 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 304,397 | 3.044 | 20 | 50 | fits | 148,331 | 215 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 411,044 | 4.110 | 20 | 50 | fits | 107,043 | 187 | 0.289 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 491,618 | 4.916 | 20 | 20 | fits | 80,640 | 28 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 846,860 | 8.469 | 20 | 20 | fits | 47,563 | 20 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 353,559 | 3.536 | 20 | 20 | fits | 105,680 | 184 | 0.295 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 295,129 | 2.951 | 20 | 200 | fits | 147,649 | 214 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 400,193 | 4.002 | 20 | 200 | fits | 105,680 | 184 | 0.295 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 296,053 | 2.961 | 20 | 20 | fits | 147,649 | 214 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 400,897 | 4.009 | 20 | 20 | fits | 105,680 | 184 | 0.295 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 152,044 | 1.520 | 20 | 24 | fits | 144,629 | 142 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 298,703 | 2.987 | 20 | 24 | fits | 147,649 | 214 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 298,637 | 2.986 | 20 | 50 | fits | 147,649 | 214 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 403,921 | 4.039 | 20 | 50 | fits | 105,680 | 184 | 0.295 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 484,480 | 4.845 | 20 | 20 | fits | 80,625 | 28 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 857,826 | 8.578 | 20 | 20 | fits | 53,119 | 27 | 0.757 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 354,216 | 3.542 | 20 | 20 | fits | 105,680 | 184 | 0.295 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 295,786 | 2.958 | 20 | 200 | fits | 147,649 | 214 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 400,850 | 4.008 | 20 | 200 | fits | 105,680 | 184 | 0.295 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 296,710 | 2.967 | 20 | 20 | fits | 147,649 | 214 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 401,554 | 4.016 | 20 | 20 | fits | 105,680 | 184 | 0.295 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 152,701 | 1.527 | 20 | 24 | fits | 144,657 | 142 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 299,360 | 2.994 | 20 | 24 | fits | 147,649 | 214 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 299,294 | 2.993 | 20 | 50 | fits | 147,649 | 214 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 404,578 | 4.046 | 20 | 50 | fits | 105,680 | 184 | 0.295 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 485,137 | 4.851 | 20 | 20 | fits | 80,625 | 28 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 860,071 | 8.601 | 20 | 20 | fits | 47,910 | 20 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 354,776 | 3.548 | 20 | 20 | fits | 105,680 | 184 | 0.295 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 296,346 | 2.963 | 20 | 200 | fits | 147,649 | 214 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 401,410 | 4.014 | 20 | 200 | fits | 105,680 | 184 | 0.295 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 297,270 | 2.973 | 20 | 20 | fits | 147,649 | 214 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 402,114 | 4.021 | 20 | 20 | fits | 105,680 | 184 | 0.295 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 153,261 | 1.533 | 20 | 24 | fits | 144,657 | 142 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 299,920 | 2.999 | 20 | 24 | fits | 147,649 | 214 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 299,854 | 2.999 | 20 | 50 | fits | 147,649 | 214 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 405,138 | 4.051 | 20 | 50 | fits | 105,680 | 184 | 0.295 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 480,588 | 4.806 | 20 | 20 | fits | 75,516 | 30 | 0.795 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 859,447 | 8.594 | 20 | 20 | fits | 57,207 | 24 | 0.670 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 362,252 | 3.623 | 20 | 20 | fits | 112,940 | 191 | 0.344 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 296,906 | 2.969 | 20 | 200 | fits | 147,649 | 214 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 409,230 | 4.092 | 20 | 200 | fits | 112,940 | 191 | 0.344 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 297,830 | 2.978 | 20 | 20 | fits | 147,649 | 214 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 409,934 | 4.099 | 20 | 20 | fits | 112,940 | 191 | 0.344 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 153,821 | 1.538 | 20 | 24 | fits | 144,657 | 142 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 300,480 | 3.005 | 20 | 24 | fits | 147,649 | 214 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 300,414 | 3.004 | 20 | 50 | fits | 147,649 | 214 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 412,958 | 4.130 | 20 | 50 | fits | 112,940 | 191 | 0.344 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 508,499 | 5.085 | 20 | 20 | fits | 83,678 | 35 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 859,083 | 8.591 | 20 | 20 | fits | 47,581 | 20 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 349,300 | 3.493 | 20 | 20 | fits | 117,110 | 207 | 0.392 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 287,020 | 2.870 | 20 | 200 | fits | 143,879 | 236 | 0.363 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 415,483 | 4.155 | 20 | 200 | fits | 117,110 | 207 | 0.392 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 287,944 | 2.879 | 20 | 20 | fits | 143,879 | 236 | 0.363 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 416,187 | 4.162 | 20 | 20 | fits | 117,110 | 207 | 0.392 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 147,705 | 1.477 | 20 | 24 | fits | 150,537 | 111 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 290,594 | 2.906 | 20 | 24 | fits | 143,879 | 236 | 0.363 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 290,528 | 2.905 | 20 | 50 | fits | 143,879 | 236 | 0.363 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 419,211 | 4.192 | 20 | 50 | fits | 117,110 | 207 | 0.392 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 501,914 | 5.019 | 20 | 20 | fits | 82,769 | 34 | 0.756 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 851,847 | 8.518 | 20 | 20 | fits | 47,486 | 20 | 0.706 |
| LINK_UP | `adp.link_up.if0` | 2,332 | 0.023 | 20 | 200 | fits | 23,265 | 43 (11) | 0.659 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,055 | 0.121 | 20 | 200 | fits | 17,820 | 23 (39) | 0.583 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 8,288 | 0.083 | 20 | 200 | fits | 2,306 | 10 (11) | 0.368 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 151,816 | 1.518 | 20 | 200 | fits | 152,756 | 271 | 0.373 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 184,623 | 1.846 | 20 | 20 | fits | 135,908 | 264 | 0.211 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 228,652 | 2.287 | 20 | 24 | fits | 73,730 | 54 | 0.452 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 175,934 | 1.759 | 20 | 50 | fits | 83,730 | 65 | 0.677 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 761,404 | 7.614 | 20 | 20 | fits | 82,092 | 38 | 0.664 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 226,971 | 2.270 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 151,816 | 1.518 | 20 | 200 | fits | 152,756 | 271 | 0.373 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 194,443 | 1.944 | 20 | 20 | fits | 137,632 | 270 | 0.223 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 238,359 | 2.384 | 20 | 24 | fits | 75,727 | 60 | 0.461 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 178,825 | 1.788 | 20 | 50 | fits | 86,621 | 71 | 0.686 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 777,512 | 7.775 | 20 | 20 | fits | 82,525 | 44 | 0.639 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 241,093 | 2.411 | 49 | 49 | fits | 0 | - | 0.000 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 17,908 | 0.179 | 20 | 20 | fits | 27,108 | 21 (35) | 0.775 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 12,490 | 0.125 | 20 | 20 | fits | 22,197 | 17 (14) | 0.796 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 11,259 | 0.113 | 20 | 20 | fits | 21,745 | 18 (14) | 0.792 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 12,701 | 0.127 | 20 | 20 | fits | 27,141 | 21 (35) | 0.775 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 73,863 | 0.739 | 20 | 20 | fits | 30,170 | 8 | 0.849 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 38,088 | 0.381 | 20 | 20 | fits | 38,154 | 12 | 0.881 |
| malformed MRPDU discard | `srp.malformed.if0` | 18,016 | 0.180 | 20 | 20 | fits | 18,082 | 12 | 0.698 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 77,632 | 0.776 | 220 | 220 | fits | 53,576 | 6 | 0.923 |
| an event behind 15 others | `backlog.event.if0` | 155,388 | 1.554 | 20 | 200 | fits | 47,638 | 79 | 0.519 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 400,796 | 4.008 | 20 | 20 | fits | 37,046 | 63 | 0.249 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 396,107 | 3.961 | 20 | 200 | fits | 148,522 | 166 | 0.306 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 395,491 | 3.955 | 20 | 200 | fits | 148,522 | 166 | 0.306 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 391,785 | 3.918 | 20 | 20 | fits | 148,522 | 166 | 0.306 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 427,995 | 4.280 | 20 | 20 | fits | 37,046 | 63 | 0.249 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 145,558 | 1.456 | 20 | 24 | fits | 146,449 | 148 | 0.427 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 394,435 | 3.944 | 20 | 24 | fits | 148,522 | 166 | 0.306 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 394,369 | 3.944 | 20 | 50 | fits | 148,522 | 166 | 0.306 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 393,973 | 3.940 | 20 | 50 | fits | 148,522 | 166 | 0.306 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 430,953 | 4.310 | 20 | 20 | fits | 37,046 | 63 | 0.249 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 484,383 | 4.844 | 20 | 20 | fits | 21,963 | 41 | 0.095 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 334,973 | 3.350 | 20 | 20 | fits | 105,781 | 185 | 0.301 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 287,800 | 2.878 | 20 | 200 | fits | 147,419 | 214 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 392,965 | 3.930 | 20 | 200 | fits | 105,781 | 185 | 0.301 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 288,724 | 2.887 | 20 | 20 | fits | 147,419 | 214 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 393,669 | 3.937 | 20 | 20 | fits | 105,781 | 185 | 0.301 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 144,945 | 1.449 | 20 | 24 | fits | 145,131 | 145 | 0.418 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 291,374 | 2.914 | 20 | 24 | fits | 147,419 | 214 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 291,308 | 2.913 | 20 | 50 | fits | 147,419 | 214 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 396,693 | 3.967 | 20 | 50 | fits | 105,781 | 185 | 0.301 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 491,733 | 4.917 | 20 | 20 | fits | 83,137 | 35 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 846,824 | 8.468 | 20 | 20 | fits | 47,481 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,531 | 0.085 | 20 | 20 | fits | 24,227 | 19 | 0.763 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 287,800 | 2.878 | 20 | 200 | fits | 147,419 | 214 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 24,554 | 0.246 | 20 | 200 | fits | 24,227 | 19 | 0.763 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 288,724 | 2.887 | 20 | 20 | fits | 147,419 | 214 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 382,521 | 3.825 | 20 | 20 | fits | 94,633 | 175 | 0.200 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 144,945 | 1.449 | 20 | 24 | fits | 145,131 | 145 | 0.418 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 291,374 | 2.914 | 20 | 24 | fits | 147,419 | 214 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 291,308 | 2.913 | 20 | 50 | fits | 147,419 | 214 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 385,545 | 3.855 | 20 | 50 | fits | 94,633 | 175 | 0.200 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 480,383 | 4.804 | 20 | 20 | fits | 82,954 | 35 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 835,474 | 8.355 | 20 | 20 | fits | 47,481 | 20 | 0.706 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,286,452 | 62.865 | 20 | 20 | MISS ceiling | 16,468 | 13 | 0.458 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,302,936 | 63.029 | 20 | 20 | MISS ceiling | 16,481 | 13 | 0.431 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,319,257 | 63.193 | 20 | 20 | MISS ceiling | 16,378 | 13 | 0.440 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,335,572 | 63.356 | 20 | 20 | MISS ceiling | 16,391 | 13 | 0.440 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,351,866 | 63.519 | 20 | 20 | MISS ceiling | 16,445 | 13 | 0.458 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 150,959 | 1.510 | 20 | 200 | fits | 145,648 | 222 | 0.415 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 231,996 | 2.320 | 20 | 200 | fits | 81,653 | 164 | 0.272 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 146,637 | 1.466 | 20 | 20 | fits | 145,648 | 222 | 0.415 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,206,328 | 62.063 | 20 | 20 | MISS ceiling | 27,560 | 15 | 0.672 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 150,277 | 1.503 | 20 | 24 | fits | 145,648 | 222 | 0.415 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,182,254 | 61.823 | 20 | 24 | MISS ceiling | 146,114 | 106 | 0.438 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 149,221 | 1.492 | 20 | 50 | fits | 145,648 | 222 | 0.415 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 230,478 | 2.305 | 20 | 50 | fits | 81,653 | 164 | 0.272 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 309,363 | 3.094 | 20 | 20 | fits | 78,951 | 28 | 0.751 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 657,158 | 6.572 | 20 | 20 | fits | 46,127 | 20 | 0.678 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,588 | 0.056 | 20 | 20 | fits | 20,387 | 13 (29) | 0.658 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 8,107 | 0.081 | 20 | 20 | fits | 23,609 | 19 (35) | 0.740 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 18,110 | 0.181 | 20 | 20 | fits | 26,919 | 21 (12) | 0.769 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 9,891 | 0.099 | 20 | 50 | fits | 23,265 | 43 | 0.659 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 8,274 | 0.083 | 20 | 50 | fits | 20,329 | 35 | 0.610 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 19,604 | 0.196 | 20 | 50 | fits | 20,224 | 35 | 0.602 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 10,475 | 0.105 | 20 | 50 | fits | 25,041 | 61 | 0.555 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 12,437 | 0.124 | 20 | 50 | fits | 25,041 | 61 | 0.555 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 9,283 | 0.093 | 20 | 50 | fits | 19,428 | 30 | 0.588 |
| LINK_UP | `adp.link_up.if0` | 2,332 | 0.023 | 20 | 200 | fits | 23,265 | 43 (11) | 0.659 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,055 | 0.121 | 20 | 200 | fits | 17,820 | 23 (39) | 0.583 |
| LINK_DOWN | `adp.link_down.if0` | 1,991 | 0.020 | 20 | 200 | fits | 19,506 | 23 (9) | 0.675 |
| LINK_UP | `adp.link_up.if0` | 2,332 | 0.023 | 20 | 200 | fits | 23,265 | 43 (11) | 0.659 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,055 | 0.121 | 20 | 200 | fits | 17,820 | 23 (39) | 0.583 |
| GM_CHANGE | `adp.gm_change.if0` | 2,243 | 0.022 | 20 | 200 | fits | 12,832 | 17 (11) | 0.323 |
| LINK_UP | `adp.link_up.if0` | 2,332 | 0.023 | 20 | 200 | fits | 23,265 | 43 (11) | 0.659 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,055 | 0.121 | 20 | 200 | fits | 17,820 | 23 (39) | 0.583 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 5,043 | 0.050 | 20 | 200 | fits | 14,430 | 16 (31) | 0.517 |
| LINK_UP | `adp.link_up.if0` | 2,332 | 0.023 | 20 | 200 | fits | 23,265 | 43 (11) | 0.659 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,055 | 0.121 | 20 | 200 | fits | 17,820 | 23 (39) | 0.583 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 5,043 | 0.050 | 20 | 200 | fits | 14,430 | 16 (31) | 0.517 |
| set_name | `aecp_fanout.set_name.if0` | 51,601 | 0.516 | 20 | 24 | fits | 56,294 | 88 | 0.557 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 48,399 | 0.484 | 20 | 24 | fits | 51,071 | 77 | 0.597 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 49,040 | 0.490 | 20 | 24 | fits | 46,349 | 78 | 0.551 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 44,598 | 0.446 | 20 | 24 | fits | 45,009 | 78 | 0.515 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 61,751 | 0.618 | 20 | 24 | fits | 62,636 | 110 | 0.589 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 256,101 | 2.561 | 20 | 24 | fits | 66,952 | 124 | 0.586 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 328,586 | 3.286 | 20 | 24 | fits | 49,306 | 67 | 0.588 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 45,162 | 0.452 | 20 | 24 | fits | 45,912 | 77 | 0.531 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 50,028 | 0.500 | 20 | 24 | fits | 46,634 | 78 | 0.544 |
| BIND_RX | `acmp.bind_rx.if0` | 18,998 | 0.190 | 20 | 20 | fits | 38,594 | 26 (77) | 0.760 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,973 | 0.100 | 20 | 20 | fits | 28,625 | 19 (32) | 0.812 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,742 | 0.107 | 20 | 20 | fits | 22,725 | 15 (47) | 0.684 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 15,654 | 0.157 | 20 | 20 | fits | 37,174 | 18 (50) | 0.824 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,208 | 0.102 | 20 | 20 | fits | 22,824 | 17 (48) | 0.670 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,789 | 0.098 | 20 | 20 | fits | 21,881 | 16 (48) | 0.622 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,042 | 0.090 | 20 | 20 | fits | 20,887 | 16 (48) | 0.593 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,218 | 0.092 | 20 | 20 | fits | 20,760 | 16 (48) | 0.584 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 10,921 | 0.109 | 20 | 24 | fits | 25,448 | 20 | 0.752 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 21,825 | 0.218 | 20 | 24 | fits | 30,708 | 20 | 0.680 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 16,441 | 0.164 | 20 | 24 | fits | 27,651 | 20 | 0.709 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 17,827 | 0.178 | 20 | 24 | fits | 26,505 | 20 | 0.695 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 17,700 | 0.177 | 20 | 24 | fits | 27,997 | 20 | 0.706 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 16,134 | 0.161 | 20 | 24 | fits | 27,269 | 20 | 0.701 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 17,681 | 0.177 | 20 | 24 | fits | 26,158 | 20 | 0.699 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 15,684 | 0.157 | 20 | 24 | fits | 26,819 | 20 | 0.719 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 17,633 | 0.176 | 20 | 24 | fits | 25,999 | 20 | 0.713 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 17,885 | 0.179 | 20 | 24 | fits | 28,866 | 21 | 0.613 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 17,213 | 0.172 | 20 | 24 | fits | 25,734 | 20 | 0.733 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 16,275 | 0.163 | 20 | 24 | fits | 26,278 | 20 | 0.733 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 15,156 | 0.152 | 20 | 24 | fits | 26,213 | 20 | 0.700 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 18,511 | 0.185 | 20 | 24 | fits | 27,139 | 20 | 0.709 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 15,341 | 0.153 | 20 | 24 | fits | 26,484 | 20 | 0.717 |
| get_configuration | `aecp.get_configuration.if0` | 14,906 | 0.149 | 20 | 24 | fits | 22,993 | 20 | 0.721 |
| entity_available | `aecp.entity_available.if0` | 12,301 | 0.123 | 20 | 24 | fits | 22,833 | 20 | 0.700 |
| get_name | `aecp.get_name.if0` | 18,298 | 0.183 | 20 | 24 | fits | 26,941 | 20 | 0.728 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 20,321 | 0.203 | 20 | 24 | fits | 31,958 | 32 | 0.682 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 16,802 | 0.168 | 20 | 24 | fits | 27,993 | 29 | 0.726 |
| get_as_path, refused ENTITY_MISBEHAVING | `aecp.get_as_path.if0` | 19,310 | 0.193 | 20 | 24 | fits | 27,127 | 29 | 0.727 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 13,194 | 0.132 | 20 | 24 | fits | 23,854 | 20 | 0.732 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 8,223 | 0.082 | 20 | 24 | fits | 22,606 | 20 | 0.683 |
| set_name | `aecp.set_name.if0` | 22,065 | 0.221 | 20 | 24 | fits | 43,411 | 42 | 0.744 |
| lock_entity | `aecp.lock_entity.if0` | 23,195 | 0.232 | 20 | 24 | fits | 35,666 | 34 | 0.773 |
| unlock_entity | `aecp.unlock_entity.if0` | 23,580 | 0.236 | 20 | 24 | fits | 35,478 | 32 | 0.776 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 139,874 | 1.399 | 20 | 24 | fits | 145,593 | 136 | 0.314 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 308,324 | 3.083 | 20 | 24 | fits | 137,008 | 114 | 0.290 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 244,490 | 2.445 | 20 | 24 | fits | 45,384 | 18 | 0.665 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 369,150 | 3.692 | 20 | 24 | fits | 82,003 | 17 | 0.671 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 354,846 | 3.548 | 20 | 24 | fits | 92,058 | 17 | 0.672 |
| READ_DESCRIPTOR held for a token (#917) | `aecp.held.read_descriptor.if0` | 518,038 | 5.180 | 20 | 24 | fits | 30,268 | 17 | 0.698 |
| LINK_UP | `fixture.link_up.if0` | 2,332 | 0.023 | 20 | 200 | fits | 23,265 | 43 (11) | 0.659 |
| malformed MRPDU discard | `fixture.malformed.if0` | 17,692 | 0.177 | 20 | 20 | fits | 17,758 | 12 | 0.687 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 31,997 | 0.320 | 20 | 24 | fits | 44,215 | 42 | 0.755 |
| LINK_DOWN | `fixture.link_down.if0` | 2,298 | 0.023 | 20 | 200 | fits | 21,293 | 23 (9) | 0.730 |
| BIND_RX | `fixture.bind_rx.if0` | 18,433 | 0.184 | 20 | 20 | fits | 38,383 | 26 (77) | 0.764 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 29,647 | 0.296 | 20 | 20 | fits | 36,801 | 35 (35) | 0.754 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 8,904 | 0.089 | 20 | 20 | fits | 22,014 | 13 (29) | 0.737 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 81,200 | 0.812 | 20 | 200 | fits | 81,304 | 77 | 0.730 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 81,200 | 0.812 | 20 | 200 | fits | 81,304 | 77 | 0.730 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 80,926 | 0.809 | 20 | 20 | fits | 81,304 | 77 | 0.730 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 80,926 | 0.809 | 20 | 20 | fits | 81,304 | 77 | 0.730 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 81,134 | 0.811 | 20 | 24 | fits | 81,304 | 77 | 0.730 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 81,134 | 0.811 | 20 | 24 | fits | 81,304 | 77 | 0.730 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 81,068 | 0.811 | 20 | 50 | fits | 81,304 | 77 | 0.730 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 81,068 | 0.811 | 20 | 50 | fits | 81,304 | 77 | 0.730 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 81,002 | 0.810 | 20 | 20 | fits | 81,304 | 77 | 0.730 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 81,002 | 0.810 | 20 | 20 | fits | 81,304 | 77 | 0.730 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
