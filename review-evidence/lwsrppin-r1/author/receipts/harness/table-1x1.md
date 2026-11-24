### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 94 paths and 7 of 964 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.188 (0.388) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.092 (0.208) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.076 (0.232) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.068 (0.363) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.105 (0.221) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.091 (0.205) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.096 (0.216) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.102 (0.226) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.098 (0.280) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.110 (0.443) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.099 (0.268) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.240 (0.567) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.125 (0.463) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.161 (0.513) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.134 (0.460) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.145 (0.367) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.050 (0.143) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.021 (0.126) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.022 (0.217) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.024 (0.241) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.058 (0.203) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.062 (0.323) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.173 (0.452) | fits | 0 aecp | 1 | 0 |
| get_as_path, refused ENTITY_MISBEHAVING | 0 | `aecp.get_as_path.if0` (aecp) | 0.240 (0.522) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.215 (0.495) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.196 (0.475) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.249 (0.539) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.202 (0.485) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR held for a token (#917) | 0 | `aecp.held.read_descriptor.if0` (aecp-held) | 5.210 (5.492) | fits | 16 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.234 (0.619) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.128 (0.395) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.265 (0.549) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.209 (0.493) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.202 (0.481) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.223 (0.504) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.225 (0.504) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.219 (0.501) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.220 (0.501) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.226 (0.509) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.196 (0.476) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.233 (0.515) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.199 (0.483) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.235 (0.518) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.206 (0.488) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.223 (0.504) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.156 (0.437) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.295 (0.680) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.179 (0.457) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.151 (0.349) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.601 (2.911) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.491 (0.758) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.511 (0.798) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.523 (0.811) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.483 (0.750) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.553 (0.851) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.356 (3.654) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.389 (0.643) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 2.690 (2.984) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.504 (2.841) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.758 (4.087) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.458 (3.777) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.437 (1.742) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.007 (4.329) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 4.508 (5.094) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.170 (0.514) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.541 (1.933) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.805 (62.970) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.465 (63.632) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.329 (0.451) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-burst.held.acmp.if0` (save-burst) | 2.203 | fits | 11 acmp | 4 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-burst.held.adp.if0` (save-burst) | 1.526 | fits | 7 adp | 4 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-flight.held.aecp.if0` (save-flight) | 2.874 | fits | 14 aecp | 4 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 2.408 | fits | 6 maap | 4 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 7.801 | fits | 31 srp | 4 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.187 (0.472) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.087 (0.195) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.102 (0.241) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.167 (0.472) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.157 (0.447) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.318 | fits | 0 srp | 4 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 3.917 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.002 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 3.960 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-7.service.adp.last.if0` (backlog-adp@blank-7) | 4.995 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-7.service.aecp.first.if0` (backlog-adp@blank-7) | 2.291 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.766 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 3.943 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-7.service.maap.last.if0` (backlog-adp@blank-7) | 5.032 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-7.service.srp.first.if0` (backlog-adp@blank-7) | 5.835 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-4.service.srp.last.if0` (backlog-adp@program-aged2-4) | 9.358 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.766 (0.863) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.393 (0.394) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.180 (0.181) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.737 (0.822) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.839 | 9 | 145,058 (1.451) | yes | - |
| backlog-adp@blank-1 | 0 | 11.714 | 9 | 145,058 (1.451) | yes | - |
| backlog-adp@blank-2 | 0 | 11.589 | 9 | 145,058 (1.451) | yes | - |
| backlog-adp@blank-3 | 0 | 11.464 | 9 | 145,058 (1.451) | yes | - |
| backlog-adp@blank-4 | 0 | 11.339 | 9 | 145,058 (1.451) | yes | - |
| backlog-adp@blank-5 | 0 | 11.214 | 9 | 145,058 (1.451) | yes | - |
| backlog-adp@blank-6 | 0 | 11.089 | 9 | 145,058 (1.451) | yes | - |
| backlog-adp@blank-7 | 0 | 14.950 | 12 | 145,078 (1.451) | yes | - |
| backlog-adp@program-0 | 0 | 11.211 | 11 | 147,457 (1.475) | yes | - |
| backlog-adp@program-1 | 0 | 10.975 | 11 | 146,579 (1.466) | yes | - |
| backlog-adp@program-2 | 0 | 11.834 | 11 | 146,439 (1.464) | yes | - |
| backlog-adp@program-3 | 0 | 11.584 | 11 | 146,439 (1.464) | yes | - |
| backlog-adp@program-4 | 1 | 10.995 | 10 | 146,289 (1.463) | yes | - |
| backlog-adp@program-5 | 1 | 10.995 | 10 | 146,289 (1.463) | yes | - |
| backlog-adp@program-6 | 0 | 9.724 | 10 | 146,993 (1.470) | yes | - |
| backlog-adp@program-7 | 0 | 10.428 | 9 | 146,856 (1.469) | yes | - |
| backlog-adp@verify-0 | 0 | 12.982 | 11 | 147,595 (1.476) | yes | - |
| backlog-adp@verify-1 | 0 | 13.878 | 12 | 146,519 (1.465) | yes | - |
| backlog-adp@verify-2 | 0 | 13.753 | 12 | 146,519 (1.465) | yes | - |
| backlog-adp@verify-3 | 0 | 13.628 | 12 | 146,519 (1.465) | yes | - |
| backlog-adp@verify-4 | 0 | 13.503 | 12 | 146,519 (1.465) | yes | - |
| backlog-adp@verify-5 | 0 | 13.378 | 12 | 146,519 (1.465) | yes | - |
| backlog-adp@verify-6 | 0 | 13.253 | 12 | 146,519 (1.465) | yes | - |
| backlog-adp@verify-7 | 0 | 13.128 | 12 | 146,519 (1.465) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 13.047 | 11 | 147,291 (1.473) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 12.165 | 12 | 147,218 (1.472) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 10.834 | 8 | 147,499 (1.475) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 11.719 | 8 | 148,539 (1.485) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 11.815 | 9 | 146,661 (1.467) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 11.793 | 9 | 146,661 (1.467) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 14.932 | 12 | 146,824 (1.468) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 13.974 | 12 | 145,356 (1.454) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 14.971 | 12 | 144,586 (1.446) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 13.222 | 12 | 144,785 (1.448) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 12.161 | 11 | 146,161 (1.462) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 11.064 | 9 | 148,513 (1.485) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 11.228 | 10 | 145,322 (1.453) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 11.037 | 9 | 145,322 (1.453) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 11.045 | 9 | 145,322 (1.453) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 11.045 | 9 | 143,903 (1.439) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.656 | 10 | 145,310 (1.453) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 10.437 | 10 | 145,509 (1.455) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 10.737 | 11 | 147,235 (1.472) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 10.701 | 10 | 146,649 (1.466) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 10.705 | 10 | 146,649 (1.466) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 10.694 | 10 | 146,649 (1.466) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 10.492 | 9 | 146,649 (1.466) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 10.476 | 9 | 143,923 (1.439) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 11.681 | 10 | 144,574 (1.446) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.558 | 10 | 144,574 (1.446) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 10.434 | 9 | 144,574 (1.446) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 10.431 | 9 | 144,719 (1.447) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 11.720 | 11 | 146,211 (1.462) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 10.428 | 9 | 145,310 (1.453) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 10.454 | 9 | 145,310 (1.453) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 10.433 | 9 | 143,739 (1.437) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 13.077 | 11 | 146,428 (1.464) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 12.182 | 12 | 146,355 (1.464) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 10.957 | 9 | 144,725 (1.447) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 12.023 | 10 | 144,725 (1.447) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 11.843 | 9 | 144,725 (1.447) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 11.820 | 9 | 144,725 (1.447) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 14.980 | 12 | 144,888 (1.449) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 14.005 | 12 | 145,335 (1.453) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 14.995 | 12 | 146,809 (1.468) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 13.234 | 12 | 147,008 (1.470) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 12.161 | 11 | 148,734 (1.487) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 11.172 | 10 | 144,751 (1.448) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 11.238 | 10 | 144,751 (1.448) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 11.048 | 9 | 144,751 (1.448) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 11.050 | 9 | 144,751 (1.448) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 11.041 | 9 | 143,918 (1.439) | yes | - |
| backlog | 0 | 5.294 | 7 | 148,751 (1.488) | yes | - |
| backlog-adp | 0 | 8.712 | 9 | 145,174 (1.452) | yes | - |
| backlog-adp-refill | 0 | 40.742 | 23 | 145,174 (1.452) | yes | - |
| backlog-owed | 0 | 64.018 | 23 | 145,609 (1.456) | yes | - |
| fixture | 0 | 1.244 | 2 | 81,763 (0.818) | yes | - |

Composed maximum over the 4 backlog windows: 148,751 CPU cycles (1.488 ms), backlog.
Over the windows that released their whole load only: 148,751 (1.488 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-flight | 2826 | 0 | 153,382 (1.534) | fits |
| save-burst | 2577 | 0 | 153,382 (1.534) | fits |
| acmp-notk | 3608 | 0 | 96,853 (0.969) | fits |
| save-second | 61118 | 0 | 46,950 (0.469) | fits |
| backlog-adp@blank-0 | 467 | 0 | 145,058 (1.451) | fits |
| backlog-adp@blank-1 | 467 | 0 | 145,058 (1.451) | fits |
| backlog-adp@blank-2 | 467 | 0 | 145,058 (1.451) | fits |
| backlog-adp@blank-3 | 467 | 0 | 145,058 (1.451) | fits |
| backlog-adp@blank-4 | 467 | 0 | 145,058 (1.451) | fits |
| backlog-adp@blank-5 | 467 | 0 | 145,058 (1.451) | fits |
| backlog-adp@blank-6 | 467 | 0 | 145,058 (1.451) | fits |
| backlog-adp@blank-7 | 470 | 0 | 145,078 (1.451) | fits |
| backlog-adp@program-0 | 477 | 0 | 147,457 (1.475) | fits |
| backlog-adp@program-1 | 477 | 0 | 146,579 (1.466) | fits |
| backlog-adp@program-2 | 477 | 0 | 146,439 (1.464) | fits |
| backlog-adp@program-3 | 477 | 0 | 146,439 (1.464) | fits |
| backlog-adp@program-4 | 477 | 0 | 146,331 (1.463) | fits |
| backlog-adp@program-5 | 477 | 0 | 146,331 (1.463) | fits |
| backlog-adp@program-6 | 477 | 0 | 146,993 (1.470) | fits |
| backlog-adp@program-7 | 477 | 0 | 146,856 (1.469) | fits |
| backlog-adp@verify-0 | 483 | 0 | 147,595 (1.476) | fits |
| backlog-adp@verify-1 | 484 | 0 | 146,519 (1.465) | fits |
| backlog-adp@verify-2 | 484 | 0 | 146,519 (1.465) | fits |
| backlog-adp@verify-3 | 484 | 0 | 146,519 (1.465) | fits |
| backlog-adp@verify-4 | 484 | 0 | 146,519 (1.465) | fits |
| backlog-adp@verify-5 | 484 | 0 | 146,519 (1.465) | fits |
| backlog-adp@verify-6 | 484 | 0 | 146,519 (1.465) | fits |
| backlog-adp@verify-7 | 484 | 0 | 146,519 (1.465) | fits |
| backlog-adp@blank-aged2-0 | 817 | 0 | 147,291 (1.473) | fits |
| backlog-adp@blank-aged2-1 | 828 | 0 | 147,218 (1.472) | fits |
| backlog-adp@blank-aged2-2 | 834 | 0 | 147,499 (1.475) | fits |
| backlog-adp@blank-aged2-3 | 844 | 0 | 148,539 (1.485) | fits |
| backlog-adp@blank-aged2-4 | 855 | 0 | 146,661 (1.467) | fits |
| backlog-adp@blank-aged2-5 | 865 | 0 | 146,661 (1.467) | fits |
| backlog-adp@blank-aged2-6 | 878 | 0 | 146,824 (1.468) | fits |
| backlog-adp@blank-aged2-7 | 888 | 0 | 145,356 (1.454) | fits |
| backlog-adp@blank-aged1-0 | 738 | 0 | 144,586 (1.446) | fits |
| backlog-adp@blank-aged1-1 | 748 | 0 | 144,785 (1.448) | fits |
| backlog-adp@blank-aged1-2 | 757 | 0 | 146,161 (1.462) | fits |
| backlog-adp@blank-aged1-3 | 765 | 0 | 148,538 (1.485) | fits |
| backlog-adp@blank-aged1-4 | 776 | 0 | 145,322 (1.453) | fits |
| backlog-adp@blank-aged1-5 | 785 | 0 | 145,322 (1.453) | fits |
| backlog-adp@blank-aged1-6 | 795 | 0 | 145,322 (1.453) | fits |
| backlog-adp@blank-aged1-7 | 805 | 0 | 143,903 (1.439) | fits |
| backlog-adp@program-aged2-0 | 856 | 0 | 145,310 (1.453) | fits |
| backlog-adp@program-aged2-1 | 866 | 0 | 145,509 (1.455) | fits |
| backlog-adp@program-aged2-2 | 877 | 0 | 147,235 (1.472) | fits |
| backlog-adp@program-aged2-3 | 886 | 0 | 146,649 (1.466) | fits |
| backlog-adp@program-aged2-4 | 896 | 0 | 146,649 (1.466) | fits |
| backlog-adp@program-aged2-5 | 906 | 0 | 146,649 (1.466) | fits |
| backlog-adp@program-aged2-6 | 915 | 0 | 146,649 (1.466) | fits |
| backlog-adp@program-aged2-7 | 925 | 0 | 143,923 (1.439) | fits |
| backlog-adp@program-aged1-0 | 776 | 0 | 144,574 (1.446) | fits |
| backlog-adp@program-aged1-1 | 786 | 0 | 144,574 (1.446) | fits |
| backlog-adp@program-aged1-2 | 795 | 0 | 144,574 (1.446) | fits |
| backlog-adp@program-aged1-3 | 805 | 0 | 144,719 (1.447) | fits |
| backlog-adp@program-aged1-4 | 817 | 0 | 146,211 (1.462) | fits |
| backlog-adp@program-aged1-5 | 825 | 0 | 145,310 (1.453) | fits |
| backlog-adp@program-aged1-6 | 835 | 0 | 145,310 (1.453) | fits |
| backlog-adp@program-aged1-7 | 845 | 0 | 143,739 (1.437) | fits |
| backlog-adp@verify-aged2-0 | 795 | 0 | 146,428 (1.464) | fits |
| backlog-adp@verify-aged2-1 | 806 | 0 | 146,355 (1.464) | fits |
| backlog-adp@verify-aged2-2 | 813 | 0 | 144,725 (1.447) | fits |
| backlog-adp@verify-aged2-3 | 824 | 0 | 144,725 (1.447) | fits |
| backlog-adp@verify-aged2-4 | 833 | 0 | 144,725 (1.447) | fits |
| backlog-adp@verify-aged2-5 | 843 | 0 | 144,725 (1.447) | fits |
| backlog-adp@verify-aged2-6 | 856 | 0 | 144,888 (1.449) | fits |
| backlog-adp@verify-aged2-7 | 866 | 0 | 145,335 (1.453) | fits |
| backlog-adp@verify-aged1-0 | 716 | 0 | 146,809 (1.468) | fits |
| backlog-adp@verify-aged1-1 | 726 | 0 | 147,008 (1.470) | fits |
| backlog-adp@verify-aged1-2 | 735 | 0 | 148,734 (1.487) | fits |
| backlog-adp@verify-aged1-3 | 744 | 0 | 144,751 (1.448) | fits |
| backlog-adp@verify-aged1-4 | 754 | 0 | 144,751 (1.448) | fits |
| backlog-adp@verify-aged1-5 | 763 | 0 | 144,751 (1.448) | fits |
| backlog-adp@verify-aged1-6 | 773 | 0 | 144,751 (1.448) | fits |
| backlog-adp@verify-aged1-7 | 783 | 0 | 143,918 (1.439) | fits |
| adp-advertise | 599 | 0 | 29,488 (0.295) | fits |
| save-held | 1339 | 0 | 153,382 (1.534) | fits |
| save-starved | 32928 | 0 | 153,382 (1.534) | fits |
| acmp-noresp | 2027 | 0 | 96,712 (0.967) | fits |
| save | 610 | 0 | 43,667 (0.437) | fits |
| srp | 290 | 0 | 53,555 (0.536) | fits |
| backlog | 286 | 0 | 148,751 (1.488) | fits |
| backlog-adp | 311 | 0 | 145,174 (1.452) | fits |
| backlog-adp-refill | 325 | 0 | 145,174 (1.452) | fits |
| backlog-owed | 309 | 0 | 146,011 (1.460) | fits |
| acmp-disc | 938 | 0 | 96,776 (0.968) | fits |
| maap | 178 | 0 | 29,488 (0.295) | fits |
| adp-link | 90 | 0 | 33,817 (0.338) | fits |
| adp-gm | 89 | 0 | 29,488 (0.295) | fits |
| adp-discover | 89 | 0 | 29,488 (0.295) | fits |
| control | 89 | 0 | 29,488 (0.295) | fits |
| aecp-fanout | 113 | 0 | 62,893 (0.629) | fits |
| acmp-cmd | 87 | 0 | 38,357 (0.384) | fits |
| aecp | 113 | 0 | 46,449 (0.464) | fits |
| aecp-largest-notice | 107 | 0 | 145,571 (1.456) | fits |
| aecp-held | 109 | 0 | 38,533 (0.385) | fits |
| datapath-events | 119 | 0 | 29,488 (0.295) | fits |
| fixture | 160 | 0 | 81,763 (0.818) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 8.243 (20) | 11.757 |
| backlog-adp@blank-aged2-1 | 2 | none | +8.435 ms, 76,598 (0.766 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 8.235 (20) | 11.765 |
| backlog-adp@blank-aged2-2 | 2 | none | +8.274 ms, 76,909 (0.769 ms), read-back | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 8.236 (20) | 11.764 |
| backlog-adp@blank-aged2-3 | 2 | +7.429 ms, 76,909 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 9.021 (20) | 10.979 |
| backlog-adp@blank-aged2-4 | 2 | +5.814 ms, 76,939 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 9.116 (20) | 10.884 |
| backlog-adp@blank-aged2-5 | 2 | +5.026 ms, 77,104 (0.771 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 9.094 (20) | 10.906 |
| backlog-adp@blank-aged2-6 | 2 | +4.260 ms, 76,917 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 9.126 (20) | 10.874 |
| backlog-adp@blank-aged2-7 | 2 | +3.046 ms, 76,681 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 9.070 (20) | 10.930 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 8.293 (20) | 11.707 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 8.303 (20) | 11.697 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 8.275 (20) | 11.725 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 8.076 (20) | 11.924 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 8.526 (20) | 11.474 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 8.334 (20) | 11.666 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 8.340 (20) | 11.660 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 8.335 (20) | 11.665 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 8.282 (20) | 11.718 |
| backlog-adp@program-aged2-1 | 2 | none | +8.492 ms, 80,772 (0.808 ms), issue | `backlog-adp@program-aged2-1.service.srp.last.if0` | 8.290 (20) | 11.710 |
| backlog-adp@program-aged2-2 | 2 | none | +8.304 ms, 81,026 (0.810 ms), issue | `backlog-adp@program-aged2-2.service.srp.last.if0` | 8.266 (20) | 11.734 |
| backlog-adp@program-aged2-3 | 2 | +6.499 ms, 81,026 (0.810 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 9.353 (20) | 10.647 |
| backlog-adp@program-aged2-4 | 2 | +5.639 ms, 80,966 (0.810 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 9.358 (20) | 10.642 |
| backlog-adp@program-aged2-5 | 2 | +4.866 ms, 81,214 (0.812 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 9.348 (20) | 10.652 |
| backlog-adp@program-aged2-6 | 2 | none | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 9.142 (20) | 10.858 |
| backlog-adp@program-aged2-7 | 2 | none | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 9.123 (20) | 10.877 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 8.310 (20) | 11.690 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 8.306 (20) | 11.694 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 8.334 (20) | 11.666 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 8.329 (20) | 11.671 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 8.261 (20) | 11.739 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 8.328 (20) | 11.672 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 8.355 (20) | 11.645 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 8.335 (20) | 11.665 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 8.223 (20) | 11.777 |
| backlog-adp@verify-aged2-1 | 2 | none | +8.414 ms, 77,458 (0.775 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 8.215 (20) | 11.785 |
| backlog-adp@verify-aged2-2 | 2 | none | +8.368 ms, 77,769 (0.778 ms), read-back | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 8.331 (20) | 11.669 |
| backlog-adp@verify-aged2-3 | 2 | none | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 9.294 (20) | 10.706 |
| backlog-adp@verify-aged2-4 | 2 | +5.797 ms, 77,828 (0.778 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 9.112 (20) | 10.888 |
| backlog-adp@verify-aged2-5 | 2 | +5.008 ms, 77,993 (0.780 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 9.090 (20) | 10.910 |
| backlog-adp@verify-aged2-6 | 2 | +4.241 ms, 77,777 (0.778 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 9.114 (20) | 10.886 |
| backlog-adp@verify-aged2-7 | 2 | +3.016 ms, 77,534 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 9.048 (20) | 10.952 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 8.249 (20) | 11.751 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 8.263 (20) | 11.737 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 8.237 (20) | 11.763 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 8.155 (20) | 11.845 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 8.507 (20) | 11.493 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 8.315 (20) | 11.685 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 8.316 (20) | 11.684 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 8.303 (20) | 11.697 |

Least margin over the aged windows: 10.642 ms, `backlog-adp@program-aged2-4.service.srp.last.if0` at 9.358 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.358 | 6,070 | 102 | 2 | 30.830 | yes | within |
| save-held | 1085.929 | 4,070 | 102 | - | 20.770 | no | within |
| save-starved | 4048.291 | 4,070 | 102 | - | 31.214 | yes | within |
| save | 1077.554 | 4,070 | 102 | - | 24.827 | no | within |

Names from their response to durable (save_burst.py; #920, #665's ruling of 2026-11-15, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-flight | 1 | 150.364 (0) | 5,000 | 2 | - | - | 19 steps (want 19), 6.244 ms | within |
| save-burst | 39 | 1099.236 (0) | 5,000 | 1 | - | - | sequence 1, 0 missing | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-flight | 1554 | 92,735 (0.927) | 78,316 (0.783) |
| save-burst | 1479 | 92,153 (0.922) | 78,484 (0.785) |
| acmp-notk | 1158 | 96,853 (0.969) | 78,938 (0.789) |
| save-second | 520 | 80,409 (0.804) | 78,472 (0.785) |
| backlog-adp@blank-0 | 342 | 90,586 (0.906) | 76,317 (0.763) |
| backlog-adp@blank-1 | 342 | 90,586 (0.906) | 76,317 (0.763) |
| backlog-adp@blank-2 | 342 | 90,586 (0.906) | 76,317 (0.763) |
| backlog-adp@blank-3 | 342 | 90,586 (0.906) | 76,317 (0.763) |
| backlog-adp@blank-4 | 342 | 90,586 (0.906) | 76,317 (0.763) |
| backlog-adp@blank-5 | 342 | 90,586 (0.906) | 76,317 (0.763) |
| backlog-adp@blank-6 | 342 | 90,586 (0.906) | 76,317 (0.763) |
| backlog-adp@blank-7 | 346 | 91,866 (0.919) | 76,317 (0.763) |
| backlog-adp@program-0 | 373 | 93,135 (0.931) | 78,484 (0.785) |
| backlog-adp@program-1 | 373 | 94,984 (0.950) | 79,115 (0.791) |
| backlog-adp@program-2 | 375 | 93,057 (0.931) | 78,484 (0.785) |
| backlog-adp@program-3 | 375 | 93,057 (0.931) | 78,484 (0.785) |
| backlog-adp@program-4 | 375 | 93,057 (0.931) | 78,484 (0.785) |
| backlog-adp@program-5 | 375 | 93,057 (0.931) | 78,484 (0.785) |
| backlog-adp@program-6 | 373 | 92,895 (0.929) | 78,484 (0.785) |
| backlog-adp@program-7 | 374 | 94,639 (0.946) | 79,115 (0.791) |
| backlog-adp@verify-0 | 399 | 97,331 (0.973) | 78,484 (0.785) |
| backlog-adp@verify-1 | 400 | 97,870 (0.979) | 78,484 (0.785) |
| backlog-adp@verify-2 | 400 | 97,870 (0.979) | 78,484 (0.785) |
| backlog-adp@verify-3 | 400 | 97,870 (0.979) | 78,484 (0.785) |
| backlog-adp@verify-4 | 400 | 97,870 (0.979) | 78,484 (0.785) |
| backlog-adp@verify-5 | 400 | 97,870 (0.979) | 78,484 (0.785) |
| backlog-adp@verify-6 | 400 | 97,870 (0.979) | 78,484 (0.785) |
| backlog-adp@verify-7 | 400 | 97,870 (0.979) | 78,484 (0.785) |
| backlog-adp@blank-aged2-0 | 341 | 91,885 (0.919) | 76,606 (0.766) |
| backlog-adp@blank-aged2-1 | 340 | 91,892 (0.919) | 76,052 (0.761) |
| backlog-adp@blank-aged2-2 | 339 | 90,986 (0.910) | 75,924 (0.759) |
| backlog-adp@blank-aged2-3 | 340 | 89,833 (0.898) | 76,032 (0.760) |
| backlog-adp@blank-aged2-4 | 340 | 89,876 (0.899) | 76,159 (0.762) |
| backlog-adp@blank-aged2-5 | 340 | 89,896 (0.899) | 76,074 (0.761) |
| backlog-adp@blank-aged2-6 | 343 | 91,821 (0.918) | 76,074 (0.761) |
| backlog-adp@blank-aged2-7 | 342 | 88,884 (0.889) | 76,332 (0.763) |
| backlog-adp@blank-aged1-0 | 343 | 91,831 (0.918) | 76,606 (0.766) |
| backlog-adp@blank-aged1-1 | 341 | 91,866 (0.919) | 76,604 (0.766) |
| backlog-adp@blank-aged1-2 | 340 | 91,902 (0.919) | 76,606 (0.766) |
| backlog-adp@blank-aged1-3 | 339 | 89,156 (0.892) | 76,604 (0.766) |
| backlog-adp@blank-aged1-4 | 339 | 90,145 (0.901) | 76,604 (0.766) |
| backlog-adp@blank-aged1-5 | 339 | 90,323 (0.903) | 76,606 (0.766) |
| backlog-adp@blank-aged1-6 | 339 | 90,428 (0.904) | 76,606 (0.766) |
| backlog-adp@blank-aged1-7 | 339 | 90,875 (0.909) | 76,606 (0.766) |
| backlog-adp@program-aged2-0 | 370 | 94,271 (0.943) | 79,067 (0.791) |
| backlog-adp@program-aged2-1 | 368 | 92,646 (0.926) | 78,693 (0.787) |
| backlog-adp@program-aged2-2 | 369 | 92,652 (0.927) | 78,624 (0.786) |
| backlog-adp@program-aged2-3 | 369 | 93,128 (0.931) | 78,624 (0.786) |
| backlog-adp@program-aged2-4 | 369 | 93,036 (0.930) | 78,624 (0.786) |
| backlog-adp@program-aged2-5 | 369 | 93,102 (0.931) | 78,624 (0.786) |
| backlog-adp@program-aged2-6 | 369 | 93,225 (0.932) | 78,883 (0.789) |
| backlog-adp@program-aged2-7 | 369 | 93,059 (0.931) | 78,825 (0.788) |
| backlog-adp@program-aged1-0 | 370 | 94,232 (0.942) | 79,115 (0.791) |
| backlog-adp@program-aged1-1 | 368 | 93,330 (0.933) | 79,184 (0.792) |
| backlog-adp@program-aged1-2 | 368 | 94,270 (0.943) | 79,067 (0.791) |
| backlog-adp@program-aged1-3 | 368 | 94,784 (0.948) | 79,067 (0.791) |
| backlog-adp@program-aged1-4 | 370 | 94,764 (0.948) | 79,115 (0.791) |
| backlog-adp@program-aged1-5 | 368 | 94,367 (0.944) | 79,067 (0.791) |
| backlog-adp@program-aged1-6 | 368 | 94,166 (0.942) | 79,067 (0.791) |
| backlog-adp@program-aged1-7 | 368 | 94,106 (0.941) | 79,067 (0.791) |
| backlog-adp@verify-aged2-0 | 400 | 92,976 (0.930) | 78,484 (0.785) |
| backlog-adp@verify-aged2-1 | 399 | 93,015 (0.930) | 78,484 (0.785) |
| backlog-adp@verify-aged2-2 | 398 | 92,864 (0.929) | 78,484 (0.785) |
| backlog-adp@verify-aged2-3 | 399 | 92,864 (0.929) | 78,484 (0.785) |
| backlog-adp@verify-aged2-4 | 399 | 92,864 (0.929) | 78,484 (0.785) |
| backlog-adp@verify-aged2-5 | 399 | 92,864 (0.929) | 78,484 (0.785) |
| backlog-adp@verify-aged2-6 | 402 | 92,864 (0.929) | 78,484 (0.785) |
| backlog-adp@verify-aged2-7 | 401 | 92,864 (0.929) | 78,484 (0.785) |
| backlog-adp@verify-aged1-0 | 402 | 92,967 (0.930) | 78,484 (0.785) |
| backlog-adp@verify-aged1-1 | 400 | 92,957 (0.930) | 78,484 (0.785) |
| backlog-adp@verify-aged1-2 | 399 | 93,025 (0.930) | 78,484 (0.785) |
| backlog-adp@verify-aged1-3 | 398 | 92,864 (0.929) | 78,484 (0.785) |
| backlog-adp@verify-aged1-4 | 398 | 92,864 (0.929) | 78,484 (0.785) |
| backlog-adp@verify-aged1-5 | 398 | 92,864 (0.929) | 78,484 (0.785) |
| backlog-adp@verify-aged1-6 | 398 | 92,864 (0.929) | 78,484 (0.785) |
| backlog-adp@verify-aged1-7 | 398 | 92,864 (0.929) | 78,484 (0.785) |
| adp-advertise | 578 | 21,260 (0.213) | 2,866 (0.029) |
| save-held | 816 | 93,041 (0.930) | 78,633 (0.786) |
| save-starved | 418 | 81,026 (0.810) | 78,609 (0.786) |
| acmp-noresp | 708 | 96,712 (0.967) | 78,890 (0.789) |
| save | 680 | 92,169 (0.922) | 78,526 (0.785) |
| srp | 271 | 21,260 (0.213) | 2,866 (0.029) |
| backlog | 265 | 21,260 (0.213) | 2,866 (0.029) |
| backlog-adp | 271 | 21,260 (0.213) | 2,866 (0.029) |
| backlog-adp-refill | 274 | 21,260 (0.213) | 2,866 (0.029) |
| backlog-owed | 276 | 21,260 (0.213) | 2,866 (0.029) |
| acmp-disc | 398 | 96,776 (0.968) | 78,890 (0.789) |
| maap | 165 | 21,260 (0.213) | 2,866 (0.029) |
| adp-link | 80 | 21,260 (0.213) | 2,866 (0.029) |
| adp-gm | 80 | 21,260 (0.213) | 2,866 (0.029) |
| adp-discover | 80 | 21,260 (0.213) | 2,866 (0.029) |
| control | 80 | 21,260 (0.213) | 2,866 (0.029) |
| aecp-fanout | 80 | 21,260 (0.213) | 2,866 (0.029) |
| acmp-cmd | 65 | 21,260 (0.213) | 2,866 (0.029) |
| aecp | 80 | 21,260 (0.213) | 3,907 (0.039) |
| aecp-largest-notice | 78 | 21,260 (0.213) | 2,866 (0.029) |
| aecp-held | 98 | 21,260 (0.213) | 2,866 (0.029) |
| datapath-events | 70 | 21,260 (0.213) | 2,866 (0.029) |
| fixture | 54 | 15,497 (0.155) | 2,866 (0.029) |

Longest pass that carries a step: 97,870 CPU cycles (0.979 ms), backlog-adp@verify-1; longest step: 79,184 (0.792 ms), backlog-adp@program-aged1-1.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 152,442 | 1.524 | 20 | 200 | fits | 153,382 | 273 | 0.370 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 196,166 | 1.962 | 20 | 20 | fits | 136,599 | 264 | 0.205 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 287,360 | 2.874 | 20 | 24 | fits | 62,430 | 44 | 0.454 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 240,792 | 2.408 | 20 | 50 | fits | 106,939 | 211 | 0.319 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 754,886 | 7.549 | 20 | 20 | fits | 42,526 | 22 | 0.768 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 81,795 | 0.818 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-burst.held.adp.if0` | 152,573 | 1.526 | 20 | 200 | fits | 153,382 | 273 | 0.370 |
| ACMP record, every channel at its refill rate, the longest | `save-burst.held.acmp.if0` | 220,305 | 2.203 | 20 | 20 | fits | 88,000 | 70 | 0.704 |
| AECP record, every channel at its refill rate, the longest | `save-burst.held.aecp.if0` | 100,096 | 1.001 | 20 | 24 | fits | 38,463 | 18 | 0.805 |
| MAAP record, every channel at its refill rate, the longest | `save-burst.held.maap.if0` | 180,830 | 1.808 | 20 | 50 | fits | 88,000 | 70 | 0.704 |
| SRP record, every channel at its refill rate, the longest | `save-burst.held.srp.if0` | 658,955 | 6.590 | 20 | 20 | fits | 73,758 | 35 | 0.717 |
| an MRPDU its periodic timer owes, the longest | `save-burst.mrpdu.periodic.if0` | 210,141 | 2.101 | 49 | 49 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 16,078 | 0.161 | 20 | 20 | fits | 28,915 | 19 (14) | 0.866 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 445,281 | 4.453 | 20 | 20 | fits | 118,600 | 202 | 0.330 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 368,805 | 3.688 | 20 | 200 | fits | 145,058 | 209 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 498,506 | 4.985 | 20 | 200 | fits | 118,600 | 202 | 0.330 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 369,729 | 3.697 | 20 | 20 | fits | 145,058 | 209 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 499,210 | 4.992 | 20 | 20 | fits | 118,600 | 202 | 0.330 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 228,311 | 2.283 | 20 | 24 | fits | 143,940 | 145 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 372,379 | 3.724 | 20 | 24 | fits | 145,058 | 209 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 372,313 | 3.723 | 20 | 50 | fits | 145,058 | 209 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 502,234 | 5.022 | 20 | 50 | fits | 118,600 | 202 | 0.330 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 582,504 | 5.825 | 20 | 20 | fits | 80,336 | 28 | 0.748 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 913,266 | 9.133 | 20 | 20 | fits | 76,245 | 32 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 432,781 | 4.328 | 20 | 20 | fits | 118,600 | 202 | 0.330 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 356,305 | 3.563 | 20 | 200 | fits | 145,058 | 209 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 486,006 | 4.860 | 20 | 200 | fits | 118,600 | 202 | 0.330 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 357,229 | 3.572 | 20 | 20 | fits | 145,058 | 209 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 486,710 | 4.867 | 20 | 20 | fits | 118,600 | 202 | 0.330 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 215,811 | 2.158 | 20 | 24 | fits | 143,940 | 145 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 359,879 | 3.599 | 20 | 24 | fits | 145,058 | 209 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 359,813 | 3.598 | 20 | 50 | fits | 145,058 | 209 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 489,734 | 4.897 | 20 | 50 | fits | 118,600 | 202 | 0.330 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 570,004 | 5.700 | 20 | 20 | fits | 80,336 | 28 | 0.748 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 900,766 | 9.008 | 20 | 20 | fits | 76,245 | 32 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 420,281 | 4.203 | 20 | 20 | fits | 118,600 | 202 | 0.330 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 343,805 | 3.438 | 20 | 200 | fits | 145,058 | 209 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 473,506 | 4.735 | 20 | 200 | fits | 118,600 | 202 | 0.330 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 344,729 | 3.447 | 20 | 20 | fits | 145,058 | 209 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 474,210 | 4.742 | 20 | 20 | fits | 118,600 | 202 | 0.330 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 203,311 | 2.033 | 20 | 24 | fits | 143,940 | 145 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 347,379 | 3.474 | 20 | 24 | fits | 145,058 | 209 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 347,313 | 3.473 | 20 | 50 | fits | 145,058 | 209 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 477,234 | 4.772 | 20 | 50 | fits | 118,600 | 202 | 0.330 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 557,504 | 5.575 | 20 | 20 | fits | 80,336 | 28 | 0.748 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 888,266 | 8.883 | 20 | 20 | fits | 76,245 | 32 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 407,781 | 4.078 | 20 | 20 | fits | 118,600 | 202 | 0.330 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 331,305 | 3.313 | 20 | 200 | fits | 145,058 | 209 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 461,006 | 4.610 | 20 | 200 | fits | 118,600 | 202 | 0.330 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 332,229 | 3.322 | 20 | 20 | fits | 145,058 | 209 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 461,710 | 4.617 | 20 | 20 | fits | 118,600 | 202 | 0.330 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 190,811 | 1.908 | 20 | 24 | fits | 143,940 | 145 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 334,879 | 3.349 | 20 | 24 | fits | 145,058 | 209 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 334,813 | 3.348 | 20 | 50 | fits | 145,058 | 209 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 464,734 | 4.647 | 20 | 50 | fits | 118,600 | 202 | 0.330 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 545,004 | 5.450 | 20 | 20 | fits | 80,336 | 28 | 0.748 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 875,766 | 8.758 | 20 | 20 | fits | 76,245 | 32 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 395,281 | 3.953 | 20 | 20 | fits | 118,600 | 202 | 0.330 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 318,805 | 3.188 | 20 | 200 | fits | 145,058 | 209 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 448,506 | 4.485 | 20 | 200 | fits | 118,600 | 202 | 0.330 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 319,729 | 3.197 | 20 | 20 | fits | 145,058 | 209 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 449,210 | 4.492 | 20 | 20 | fits | 118,600 | 202 | 0.330 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 178,311 | 1.783 | 20 | 24 | fits | 143,940 | 145 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 322,379 | 3.224 | 20 | 24 | fits | 145,058 | 209 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 322,313 | 3.223 | 20 | 50 | fits | 145,058 | 209 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 452,234 | 4.522 | 20 | 50 | fits | 118,600 | 202 | 0.330 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 532,504 | 5.325 | 20 | 20 | fits | 80,336 | 28 | 0.748 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 863,266 | 8.633 | 20 | 20 | fits | 76,245 | 32 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 382,781 | 3.828 | 20 | 20 | fits | 118,600 | 202 | 0.330 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 306,305 | 3.063 | 20 | 200 | fits | 145,058 | 209 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 436,006 | 4.360 | 20 | 200 | fits | 118,600 | 202 | 0.330 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 307,229 | 3.072 | 20 | 20 | fits | 145,058 | 209 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 436,710 | 4.367 | 20 | 20 | fits | 118,600 | 202 | 0.330 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 165,811 | 1.658 | 20 | 24 | fits | 143,940 | 145 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 309,879 | 3.099 | 20 | 24 | fits | 145,058 | 209 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 309,813 | 3.098 | 20 | 50 | fits | 145,058 | 209 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 439,734 | 4.397 | 20 | 50 | fits | 118,600 | 202 | 0.330 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 520,004 | 5.200 | 20 | 20 | fits | 80,336 | 28 | 0.748 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 850,766 | 8.508 | 20 | 20 | fits | 76,245 | 32 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 370,281 | 3.703 | 20 | 20 | fits | 118,600 | 202 | 0.330 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 293,805 | 2.938 | 20 | 200 | fits | 145,058 | 209 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 423,506 | 4.235 | 20 | 200 | fits | 118,600 | 202 | 0.330 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 294,729 | 2.947 | 20 | 20 | fits | 145,058 | 209 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 424,210 | 4.242 | 20 | 20 | fits | 118,600 | 202 | 0.330 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 153,311 | 1.533 | 20 | 24 | fits | 143,940 | 145 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 297,379 | 2.974 | 20 | 24 | fits | 145,058 | 209 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 297,313 | 2.973 | 20 | 50 | fits | 145,058 | 209 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 427,234 | 4.272 | 20 | 50 | fits | 118,600 | 202 | 0.330 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 507,504 | 5.075 | 20 | 20 | fits | 80,336 | 28 | 0.748 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 838,266 | 8.383 | 20 | 20 | fits | 76,245 | 32 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 445,672 | 4.457 | 20 | 20 | fits | 118,767 | 202 | 0.332 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 369,591 | 3.696 | 20 | 200 | fits | 145,078 | 209 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 499,459 | 4.995 | 20 | 200 | fits | 118,767 | 202 | 0.332 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 370,515 | 3.705 | 20 | 20 | fits | 145,078 | 209 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 500,163 | 5.002 | 20 | 20 | fits | 118,767 | 202 | 0.332 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 229,077 | 2.291 | 20 | 24 | fits | 143,940 | 145 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 373,165 | 3.732 | 20 | 24 | fits | 145,078 | 209 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 373,099 | 3.731 | 20 | 50 | fits | 145,078 | 209 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 503,187 | 5.032 | 20 | 50 | fits | 118,767 | 202 | 0.332 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 583,499 | 5.835 | 20 | 20 | fits | 80,378 | 28 | 0.748 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 914,398 | 9.144 | 20 | 20 | fits | 76,245 | 32 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 381,041 | 3.810 | 20 | 20 | fits | 106,370 | 187 | 0.268 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 320,119 | 3.201 | 20 | 200 | fits | 147,457 | 215 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 425,873 | 4.259 | 20 | 200 | fits | 106,370 | 187 | 0.268 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 321,043 | 3.210 | 20 | 20 | fits | 147,457 | 215 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 426,577 | 4.266 | 20 | 20 | fits | 106,370 | 187 | 0.268 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 167,080 | 1.671 | 20 | 24 | fits | 144,403 | 146 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 323,693 | 3.237 | 20 | 24 | fits | 147,457 | 215 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 323,627 | 3.236 | 20 | 50 | fits | 147,457 | 215 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 429,601 | 4.296 | 20 | 50 | fits | 106,370 | 187 | 0.268 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 509,633 | 5.096 | 20 | 20 | fits | 80,098 | 28 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 844,205 | 8.442 | 20 | 20 | fits | 85,319 | 36 | 0.557 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 367,863 | 3.679 | 20 | 20 | fits | 108,384 | 175 | 0.262 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 312,224 | 3.122 | 20 | 200 | fits | 146,579 | 230 | 0.374 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 419,992 | 4.200 | 20 | 200 | fits | 108,384 | 175 | 0.262 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 313,148 | 3.131 | 20 | 20 | fits | 146,579 | 230 | 0.374 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 420,696 | 4.207 | 20 | 20 | fits | 108,384 | 175 | 0.262 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 160,147 | 1.601 | 20 | 24 | fits | 144,019 | 146 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 315,798 | 3.158 | 20 | 24 | fits | 146,579 | 230 | 0.374 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 315,732 | 3.157 | 20 | 50 | fits | 146,579 | 230 | 0.374 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 423,720 | 4.237 | 20 | 50 | fits | 108,384 | 175 | 0.262 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 503,836 | 5.038 | 20 | 20 | fits | 80,182 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 838,622 | 8.386 | 20 | 20 | fits | 85,319 | 36 | 0.557 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 435,900 | 4.359 | 20 | 20 | fits | 108,528 | 175 | 0.265 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 380,407 | 3.804 | 20 | 200 | fits | 146,439 | 230 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 488,319 | 4.883 | 20 | 200 | fits | 108,528 | 175 | 0.265 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 381,331 | 3.813 | 20 | 20 | fits | 146,439 | 230 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 489,023 | 4.890 | 20 | 20 | fits | 108,528 | 175 | 0.265 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 228,386 | 2.284 | 20 | 24 | fits | 144,679 | 146 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 383,981 | 3.840 | 20 | 24 | fits | 146,439 | 230 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 383,915 | 3.839 | 20 | 50 | fits | 146,439 | 230 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 492,047 | 4.920 | 20 | 50 | fits | 108,528 | 175 | 0.265 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 576,163 | 5.762 | 20 | 20 | fits | 84,182 | 34 | 0.750 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 906,620 | 9.066 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 410,900 | 4.109 | 20 | 20 | fits | 108,528 | 175 | 0.265 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 355,407 | 3.554 | 20 | 200 | fits | 146,439 | 230 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 463,319 | 4.633 | 20 | 200 | fits | 108,528 | 175 | 0.265 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 356,331 | 3.563 | 20 | 20 | fits | 146,439 | 230 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 464,023 | 4.640 | 20 | 20 | fits | 108,528 | 175 | 0.265 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 203,386 | 2.034 | 20 | 24 | fits | 144,679 | 146 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 358,981 | 3.590 | 20 | 24 | fits | 146,439 | 230 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 358,915 | 3.589 | 20 | 50 | fits | 146,439 | 230 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 467,047 | 4.670 | 20 | 50 | fits | 108,528 | 175 | 0.265 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 551,163 | 5.512 | 20 | 20 | fits | 84,182 | 34 | 0.750 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 881,620 | 8.816 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 351,853 | 3.519 | 20 | 20 | fits | 108,438 | 175 | 0.264 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 296,450 | 2.965 | 20 | 200 | fits | 146,289 | 230 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 404,272 | 4.043 | 20 | 200 | fits | 108,438 | 175 | 0.264 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 297,374 | 2.974 | 20 | 20 | fits | 146,289 | 230 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 404,976 | 4.050 | 20 | 20 | fits | 108,438 | 175 | 0.264 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 144,497 | 1.445 | 20 | 24 | fits | 146,331 | 146 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 300,024 | 3.000 | 20 | 24 | fits | 146,289 | 230 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 299,958 | 3.000 | 20 | 50 | fits | 146,289 | 230 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 408,000 | 4.080 | 20 | 50 | fits | 108,438 | 175 | 0.264 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 492,116 | 4.921 | 20 | 20 | fits | 84,182 | 34 | 0.750 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 822,710 | 8.227 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 351,853 | 3.519 | 20 | 20 | fits | 108,438 | 175 | 0.264 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 296,450 | 2.965 | 20 | 200 | fits | 146,289 | 230 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 404,272 | 4.043 | 20 | 200 | fits | 108,438 | 175 | 0.264 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 297,374 | 2.974 | 20 | 20 | fits | 146,289 | 230 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 404,976 | 4.050 | 20 | 20 | fits | 108,438 | 175 | 0.264 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 144,497 | 1.445 | 20 | 24 | fits | 146,331 | 146 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 300,024 | 3.000 | 20 | 24 | fits | 146,289 | 230 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 299,958 | 3.000 | 20 | 50 | fits | 146,289 | 230 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 408,000 | 4.080 | 20 | 50 | fits | 108,438 | 175 | 0.264 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 492,116 | 4.921 | 20 | 20 | fits | 84,182 | 34 | 0.750 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 822,710 | 8.227 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 343,243 | 3.432 | 20 | 20 | fits | 105,497 | 184 | 0.286 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 296,345 | 2.963 | 20 | 200 | fits | 146,993 | 214 | 0.364 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 401,226 | 4.012 | 20 | 200 | fits | 105,497 | 184 | 0.286 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 297,269 | 2.973 | 20 | 20 | fits | 146,993 | 214 | 0.364 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 401,930 | 4.019 | 20 | 20 | fits | 105,497 | 184 | 0.286 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 153,916 | 1.539 | 20 | 24 | fits | 144,040 | 146 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 299,919 | 2.999 | 20 | 24 | fits | 146,993 | 214 | 0.364 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 299,853 | 2.999 | 20 | 50 | fits | 146,993 | 214 | 0.364 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 404,954 | 4.050 | 20 | 50 | fits | 105,497 | 184 | 0.286 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 489,218 | 4.892 | 20 | 20 | fits | 84,330 | 34 | 0.753 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 822,474 | 8.225 | 20 | 20 | fits | 78,840 | 39 | 0.587 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 350,516 | 3.505 | 20 | 20 | fits | 105,336 | 184 | 0.281 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 292,050 | 2.921 | 20 | 200 | fits | 146,856 | 214 | 0.364 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 396,770 | 3.968 | 20 | 200 | fits | 105,336 | 184 | 0.281 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 292,974 | 2.930 | 20 | 20 | fits | 146,856 | 214 | 0.364 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 397,474 | 3.975 | 20 | 20 | fits | 105,336 | 184 | 0.281 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 149,758 | 1.498 | 20 | 24 | fits | 143,947 | 145 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 295,624 | 2.956 | 20 | 24 | fits | 146,856 | 214 | 0.364 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 295,558 | 2.956 | 20 | 50 | fits | 146,856 | 214 | 0.364 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 400,498 | 4.005 | 20 | 50 | fits | 105,336 | 184 | 0.281 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 484,739 | 4.847 | 20 | 20 | fits | 84,307 | 34 | 0.753 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 832,441 | 8.324 | 20 | 20 | fits | 80,902 | 39 | 0.656 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 359,543 | 3.595 | 20 | 20 | fits | 106,597 | 187 | 0.273 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 298,394 | 2.984 | 20 | 200 | fits | 147,595 | 215 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 404,375 | 4.044 | 20 | 200 | fits | 106,597 | 187 | 0.273 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 299,318 | 2.993 | 20 | 20 | fits | 147,595 | 215 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 405,079 | 4.051 | 20 | 20 | fits | 106,597 | 187 | 0.273 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 145,153 | 1.452 | 20 | 24 | fits | 143,669 | 146 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 301,968 | 3.020 | 20 | 24 | fits | 147,595 | 215 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 301,902 | 3.019 | 20 | 50 | fits | 147,595 | 215 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 408,103 | 4.081 | 20 | 50 | fits | 106,597 | 187 | 0.273 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 488,135 | 4.881 | 20 | 20 | fits | 80,098 | 28 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 818,643 | 8.186 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 429,517 | 4.295 | 20 | 20 | fits | 108,376 | 175 | 0.262 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 373,817 | 3.738 | 20 | 200 | fits | 146,519 | 230 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 481,577 | 4.816 | 20 | 200 | fits | 108,376 | 175 | 0.262 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 374,741 | 3.747 | 20 | 20 | fits | 146,519 | 230 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 482,281 | 4.823 | 20 | 20 | fits | 108,376 | 175 | 0.262 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 221,569 | 2.216 | 20 | 24 | fits | 143,495 | 146 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 377,391 | 3.774 | 20 | 24 | fits | 146,519 | 230 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 377,325 | 3.773 | 20 | 50 | fits | 146,519 | 230 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 485,305 | 4.853 | 20 | 50 | fits | 108,376 | 175 | 0.262 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 565,421 | 5.654 | 20 | 20 | fits | 80,182 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 896,045 | 8.960 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 417,017 | 4.170 | 20 | 20 | fits | 108,376 | 175 | 0.262 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 361,317 | 3.613 | 20 | 200 | fits | 146,519 | 230 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 469,077 | 4.691 | 20 | 200 | fits | 108,376 | 175 | 0.262 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 362,241 | 3.622 | 20 | 20 | fits | 146,519 | 230 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 469,781 | 4.698 | 20 | 20 | fits | 108,376 | 175 | 0.262 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 209,069 | 2.091 | 20 | 24 | fits | 143,495 | 146 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 364,891 | 3.649 | 20 | 24 | fits | 146,519 | 230 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 364,825 | 3.648 | 20 | 50 | fits | 146,519 | 230 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 472,805 | 4.728 | 20 | 50 | fits | 108,376 | 175 | 0.262 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 552,921 | 5.529 | 20 | 20 | fits | 80,182 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 883,545 | 8.835 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 404,517 | 4.045 | 20 | 20 | fits | 108,376 | 175 | 0.262 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 348,817 | 3.488 | 20 | 200 | fits | 146,519 | 230 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 456,577 | 4.566 | 20 | 200 | fits | 108,376 | 175 | 0.262 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 349,741 | 3.497 | 20 | 20 | fits | 146,519 | 230 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 457,281 | 4.573 | 20 | 20 | fits | 108,376 | 175 | 0.262 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 196,569 | 1.966 | 20 | 24 | fits | 143,495 | 146 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 352,391 | 3.524 | 20 | 24 | fits | 146,519 | 230 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 352,325 | 3.523 | 20 | 50 | fits | 146,519 | 230 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 460,305 | 4.603 | 20 | 50 | fits | 108,376 | 175 | 0.262 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 540,421 | 5.404 | 20 | 20 | fits | 80,182 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 871,045 | 8.710 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 392,017 | 3.920 | 20 | 20 | fits | 108,376 | 175 | 0.262 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 336,317 | 3.363 | 20 | 200 | fits | 146,519 | 230 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 444,077 | 4.441 | 20 | 200 | fits | 108,376 | 175 | 0.262 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 337,241 | 3.372 | 20 | 20 | fits | 146,519 | 230 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 444,781 | 4.448 | 20 | 20 | fits | 108,376 | 175 | 0.262 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 184,069 | 1.841 | 20 | 24 | fits | 143,495 | 146 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 339,891 | 3.399 | 20 | 24 | fits | 146,519 | 230 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 339,825 | 3.398 | 20 | 50 | fits | 146,519 | 230 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 447,805 | 4.478 | 20 | 50 | fits | 108,376 | 175 | 0.262 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 527,921 | 5.279 | 20 | 20 | fits | 80,182 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 858,545 | 8.585 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 379,517 | 3.795 | 20 | 20 | fits | 108,376 | 175 | 0.262 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 323,817 | 3.238 | 20 | 200 | fits | 146,519 | 230 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 431,577 | 4.316 | 20 | 200 | fits | 108,376 | 175 | 0.262 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 324,741 | 3.247 | 20 | 20 | fits | 146,519 | 230 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 432,281 | 4.323 | 20 | 20 | fits | 108,376 | 175 | 0.262 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 171,569 | 1.716 | 20 | 24 | fits | 143,495 | 146 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 327,391 | 3.274 | 20 | 24 | fits | 146,519 | 230 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 327,325 | 3.273 | 20 | 50 | fits | 146,519 | 230 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 435,305 | 4.353 | 20 | 50 | fits | 108,376 | 175 | 0.262 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 515,421 | 5.154 | 20 | 20 | fits | 80,182 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 846,045 | 8.460 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 367,017 | 3.670 | 20 | 20 | fits | 108,376 | 175 | 0.262 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 311,317 | 3.113 | 20 | 200 | fits | 146,519 | 230 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 419,077 | 4.191 | 20 | 200 | fits | 108,376 | 175 | 0.262 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 312,241 | 3.122 | 20 | 20 | fits | 146,519 | 230 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 419,781 | 4.198 | 20 | 20 | fits | 108,376 | 175 | 0.262 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 159,069 | 1.591 | 20 | 24 | fits | 143,495 | 146 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 314,891 | 3.149 | 20 | 24 | fits | 146,519 | 230 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 314,825 | 3.148 | 20 | 50 | fits | 146,519 | 230 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 422,805 | 4.228 | 20 | 50 | fits | 108,376 | 175 | 0.262 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 502,921 | 5.029 | 20 | 20 | fits | 80,182 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 833,545 | 8.335 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 354,517 | 3.545 | 20 | 20 | fits | 108,376 | 175 | 0.262 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 298,817 | 2.988 | 20 | 200 | fits | 146,519 | 230 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 406,577 | 4.066 | 20 | 200 | fits | 108,376 | 175 | 0.262 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 299,741 | 2.997 | 20 | 20 | fits | 146,519 | 230 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 407,281 | 4.073 | 20 | 20 | fits | 108,376 | 175 | 0.262 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 146,569 | 1.466 | 20 | 24 | fits | 143,495 | 146 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 302,391 | 3.024 | 20 | 24 | fits | 146,519 | 230 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 302,325 | 3.023 | 20 | 50 | fits | 146,519 | 230 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 410,305 | 4.103 | 20 | 50 | fits | 108,376 | 175 | 0.262 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 490,421 | 4.904 | 20 | 20 | fits | 80,182 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 821,045 | 8.210 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 365,215 | 3.652 | 20 | 20 | fits | 106,485 | 187 | 0.269 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 304,178 | 3.042 | 20 | 200 | fits | 147,291 | 215 | 0.376 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 410,047 | 4.100 | 20 | 200 | fits | 106,485 | 187 | 0.269 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 305,102 | 3.051 | 20 | 20 | fits | 147,291 | 215 | 0.376 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 410,751 | 4.108 | 20 | 20 | fits | 106,485 | 187 | 0.269 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 151,566 | 1.516 | 20 | 24 | fits | 142,990 | 143 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 307,752 | 3.078 | 20 | 24 | fits | 147,291 | 215 | 0.376 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 307,686 | 3.077 | 20 | 50 | fits | 147,291 | 215 | 0.376 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 413,775 | 4.138 | 20 | 50 | fits | 106,485 | 187 | 0.269 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 493,773 | 4.938 | 20 | 20 | fits | 80,064 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 824,281 | 8.243 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 364,419 | 3.644 | 20 | 20 | fits | 106,485 | 187 | 0.269 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 303,382 | 3.034 | 20 | 200 | fits | 147,218 | 215 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 409,251 | 4.093 | 20 | 200 | fits | 106,485 | 187 | 0.269 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 304,306 | 3.043 | 20 | 20 | fits | 147,218 | 215 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 409,955 | 4.100 | 20 | 20 | fits | 106,485 | 187 | 0.269 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 150,843 | 1.508 | 20 | 24 | fits | 142,987 | 143 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 306,956 | 3.070 | 20 | 24 | fits | 147,218 | 215 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 306,890 | 3.069 | 20 | 50 | fits | 147,218 | 215 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 412,979 | 4.130 | 20 | 50 | fits | 106,485 | 187 | 0.269 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 492,977 | 4.930 | 20 | 20 | fits | 80,064 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 823,485 | 8.235 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 330,313 | 3.303 | 20 | 20 | fits | 105,551 | 184 | 0.287 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 283,371 | 2.834 | 20 | 200 | fits | 147,499 | 219 | 0.360 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 388,306 | 3.883 | 20 | 200 | fits | 105,551 | 184 | 0.287 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 284,295 | 2.843 | 20 | 20 | fits | 147,499 | 219 | 0.360 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 389,010 | 3.890 | 20 | 20 | fits | 105,551 | 184 | 0.287 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 140,436 | 1.404 | 20 | 24 | fits | 142,552 | 142 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 286,945 | 2.869 | 20 | 24 | fits | 147,499 | 219 | 0.360 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 286,879 | 2.869 | 20 | 50 | fits | 147,499 | 219 | 0.360 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 392,034 | 3.920 | 20 | 50 | fits | 105,551 | 184 | 0.287 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 472,168 | 4.722 | 20 | 20 | fits | 80,200 | 28 | 0.746 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 823,634 | 8.236 | 20 | 20 | fits | 84,620 | 45 | 0.656 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 331,058 | 3.311 | 20 | 20 | fits | 100,388 | 193 | 0.331 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 289,415 | 2.894 | 20 | 200 | fits | 148,539 | 242 | 0.337 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 389,187 | 3.892 | 20 | 200 | fits | 100,388 | 193 | 0.331 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 290,339 | 2.903 | 20 | 20 | fits | 148,539 | 242 | 0.337 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 389,891 | 3.899 | 20 | 20 | fits | 100,388 | 193 | 0.331 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 145,440 | 1.454 | 20 | 24 | fits | 148,276 | 111 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 292,989 | 2.930 | 20 | 24 | fits | 148,539 | 242 | 0.337 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 292,923 | 2.929 | 20 | 50 | fits | 148,539 | 242 | 0.337 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 392,915 | 3.929 | 20 | 50 | fits | 100,388 | 193 | 0.331 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 473,002 | 4.730 | 20 | 20 | fits | 80,153 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 902,115 | 9.021 | 20 | 20 | fits | 86,094 | 37 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 351,875 | 3.519 | 20 | 20 | fits | 105,224 | 184 | 0.277 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 293,521 | 2.935 | 20 | 200 | fits | 146,661 | 214 | 0.362 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 398,129 | 3.981 | 20 | 200 | fits | 105,224 | 184 | 0.277 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 294,445 | 2.944 | 20 | 20 | fits | 146,661 | 214 | 0.362 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 398,833 | 3.988 | 20 | 20 | fits | 105,224 | 184 | 0.277 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 151,424 | 1.514 | 20 | 24 | fits | 142,552 | 142 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 297,095 | 2.971 | 20 | 24 | fits | 146,661 | 214 | 0.362 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 297,029 | 2.970 | 20 | 50 | fits | 146,661 | 214 | 0.362 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 401,857 | 4.019 | 20 | 50 | fits | 105,224 | 184 | 0.277 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 482,094 | 4.821 | 20 | 20 | fits | 80,303 | 29 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 911,632 | 9.116 | 20 | 20 | fits | 85,319 | 36 | 0.557 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 351,155 | 3.512 | 20 | 20 | fits | 105,328 | 185 | 0.278 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 292,801 | 2.928 | 20 | 200 | fits | 146,661 | 214 | 0.362 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 397,513 | 3.975 | 20 | 200 | fits | 105,328 | 185 | 0.278 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 293,725 | 2.937 | 20 | 20 | fits | 146,661 | 214 | 0.362 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 398,217 | 3.982 | 20 | 20 | fits | 105,328 | 185 | 0.278 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 150,704 | 1.507 | 20 | 24 | fits | 142,552 | 142 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 296,375 | 2.964 | 20 | 24 | fits | 146,661 | 214 | 0.362 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 296,309 | 2.963 | 20 | 50 | fits | 146,661 | 214 | 0.362 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 401,241 | 4.012 | 20 | 50 | fits | 105,328 | 185 | 0.278 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 500,864 | 5.009 | 20 | 20 | fits | 87,962 | 41 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 909,372 | 9.094 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 373,334 | 3.733 | 20 | 20 | fits | 117,323 | 197 | 0.373 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 292,244 | 2.922 | 20 | 200 | fits | 146,824 | 215 | 0.363 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 420,665 | 4.207 | 20 | 200 | fits | 117,323 | 197 | 0.373 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 293,168 | 2.932 | 20 | 20 | fits | 146,824 | 215 | 0.363 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 421,369 | 4.214 | 20 | 20 | fits | 117,323 | 197 | 0.373 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 149,984 | 1.500 | 20 | 24 | fits | 142,552 | 142 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 295,818 | 2.958 | 20 | 24 | fits | 146,824 | 215 | 0.363 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 295,752 | 2.958 | 20 | 50 | fits | 146,824 | 215 | 0.363 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 424,393 | 4.244 | 20 | 50 | fits | 117,323 | 197 | 0.373 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 581,602 | 5.816 | 20 | 20 | fits | 80,358 | 29 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 912,614 | 9.126 | 20 | 20 | fits | 76,245 | 32 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 446,158 | 4.462 | 20 | 20 | fits | 116,688 | 202 | 0.287 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 299,889 | 2.999 | 20 | 200 | fits | 145,356 | 208 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 492,642 | 4.926 | 20 | 200 | fits | 116,688 | 202 | 0.287 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 300,813 | 3.008 | 20 | 20 | fits | 145,356 | 208 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 493,346 | 4.933 | 20 | 20 | fits | 116,688 | 202 | 0.287 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 149,340 | 1.493 | 20 | 24 | fits | 142,628 | 143 | 0.379 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 303,463 | 3.035 | 20 | 24 | fits | 145,356 | 208 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 303,397 | 3.034 | 20 | 50 | fits | 145,356 | 208 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 496,370 | 4.964 | 20 | 50 | fits | 116,688 | 202 | 0.287 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 576,360 | 5.764 | 20 | 20 | fits | 80,056 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 907,037 | 9.070 | 20 | 20 | fits | 76,331 | 33 | 0.581 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 346,809 | 3.468 | 20 | 20 | fits | 108,444 | 176 | 0.261 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 291,164 | 2.912 | 20 | 200 | fits | 144,586 | 225 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 398,992 | 3.990 | 20 | 200 | fits | 108,444 | 176 | 0.261 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 292,088 | 2.921 | 20 | 20 | fits | 144,586 | 225 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 399,696 | 3.997 | 20 | 20 | fits | 108,444 | 176 | 0.261 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 151,142 | 1.511 | 20 | 24 | fits | 142,552 | 142 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 294,738 | 2.947 | 20 | 24 | fits | 144,586 | 225 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 294,672 | 2.947 | 20 | 50 | fits | 144,586 | 225 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 402,720 | 4.027 | 20 | 50 | fits | 108,444 | 176 | 0.261 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 498,532 | 4.985 | 20 | 20 | fits | 84,151 | 35 | 0.757 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 829,331 | 8.293 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 362,479 | 3.625 | 20 | 20 | fits | 113,753 | 182 | 0.340 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 290,643 | 2.906 | 20 | 200 | fits | 144,785 | 226 | 0.369 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 415,547 | 4.155 | 20 | 200 | fits | 113,753 | 182 | 0.340 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 291,567 | 2.916 | 20 | 20 | fits | 144,785 | 226 | 0.369 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 416,251 | 4.163 | 20 | 20 | fits | 113,753 | 182 | 0.340 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 150,422 | 1.504 | 20 | 24 | fits | 142,552 | 142 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 294,217 | 2.942 | 20 | 24 | fits | 144,785 | 226 | 0.369 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 294,151 | 2.942 | 20 | 50 | fits | 144,785 | 226 | 0.369 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 419,275 | 4.193 | 20 | 50 | fits | 113,753 | 182 | 0.340 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 499,379 | 4.994 | 20 | 20 | fits | 80,170 | 28 | 0.746 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 830,278 | 8.303 | 20 | 20 | fits | 76,245 | 32 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 356,948 | 3.569 | 20 | 20 | fits | 108,367 | 175 | 0.259 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 301,326 | 3.013 | 20 | 200 | fits | 146,161 | 230 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 409,077 | 4.091 | 20 | 200 | fits | 108,367 | 175 | 0.259 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 302,250 | 3.022 | 20 | 20 | fits | 146,161 | 230 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 409,781 | 4.098 | 20 | 20 | fits | 108,367 | 175 | 0.259 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 149,796 | 1.498 | 20 | 24 | fits | 142,646 | 143 | 0.379 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 304,900 | 3.049 | 20 | 24 | fits | 146,161 | 230 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 304,834 | 3.048 | 20 | 50 | fits | 146,161 | 230 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 412,805 | 4.128 | 20 | 50 | fits | 108,367 | 175 | 0.259 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 492,887 | 4.929 | 20 | 20 | fits | 80,148 | 28 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 827,468 | 8.275 | 20 | 20 | fits | 80,145 | 38 | 0.617 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 342,749 | 3.427 | 20 | 20 | fits | 100,174 | 193 | 0.323 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 289,632 | 2.896 | 20 | 200 | fits | 148,513 | 242 | 0.336 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 389,190 | 3.892 | 20 | 200 | fits | 100,174 | 193 | 0.323 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 290,556 | 2.906 | 20 | 20 | fits | 148,513 | 242 | 0.336 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 389,894 | 3.899 | 20 | 20 | fits | 100,174 | 193 | 0.323 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 145,683 | 1.457 | 20 | 24 | fits | 148,538 | 111 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 293,206 | 2.932 | 20 | 24 | fits | 148,513 | 242 | 0.336 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 293,140 | 2.931 | 20 | 50 | fits | 148,513 | 242 | 0.336 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 392,918 | 3.929 | 20 | 50 | fits | 100,174 | 193 | 0.323 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 473,012 | 4.730 | 20 | 20 | fits | 80,160 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 807,649 | 8.076 | 20 | 20 | fits | 85,496 | 37 | 0.556 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 353,573 | 3.536 | 20 | 20 | fits | 106,549 | 187 | 0.272 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 292,542 | 2.925 | 20 | 200 | fits | 145,322 | 210 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 398,475 | 3.985 | 20 | 200 | fits | 106,549 | 187 | 0.272 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 293,466 | 2.935 | 20 | 20 | fits | 145,322 | 210 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 399,179 | 3.992 | 20 | 20 | fits | 106,549 | 187 | 0.272 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 151,784 | 1.518 | 20 | 24 | fits | 142,898 | 142 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 296,116 | 2.961 | 20 | 24 | fits | 145,322 | 210 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 296,050 | 2.961 | 20 | 50 | fits | 145,322 | 210 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 402,203 | 4.022 | 20 | 50 | fits | 106,549 | 187 | 0.272 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 482,171 | 4.822 | 20 | 20 | fits | 80,034 | 28 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 852,566 | 8.526 | 20 | 20 | fits | 27,743 | 12 | 0.806 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 352,853 | 3.529 | 20 | 20 | fits | 106,549 | 187 | 0.272 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 291,822 | 2.918 | 20 | 200 | fits | 145,322 | 210 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 397,755 | 3.978 | 20 | 200 | fits | 106,549 | 187 | 0.272 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 292,746 | 2.927 | 20 | 20 | fits | 145,322 | 210 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 398,459 | 3.985 | 20 | 20 | fits | 106,549 | 187 | 0.272 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 151,064 | 1.511 | 20 | 24 | fits | 142,898 | 142 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 295,396 | 2.954 | 20 | 24 | fits | 145,322 | 210 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 295,330 | 2.953 | 20 | 50 | fits | 145,322 | 210 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 401,483 | 4.015 | 20 | 50 | fits | 106,549 | 187 | 0.272 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 485,564 | 4.856 | 20 | 20 | fits | 84,147 | 34 | 0.751 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 833,365 | 8.334 | 20 | 20 | fits | 85,319 | 36 | 0.557 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 358,946 | 3.589 | 20 | 20 | fits | 113,598 | 194 | 0.317 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 291,102 | 2.911 | 20 | 200 | fits | 145,322 | 210 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 404,084 | 4.041 | 20 | 200 | fits | 113,598 | 194 | 0.317 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 292,026 | 2.920 | 20 | 20 | fits | 145,322 | 210 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 404,788 | 4.048 | 20 | 20 | fits | 113,598 | 194 | 0.317 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 150,344 | 1.503 | 20 | 24 | fits | 142,898 | 142 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 294,676 | 2.947 | 20 | 24 | fits | 145,322 | 210 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 294,610 | 2.946 | 20 | 50 | fits | 145,322 | 210 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 407,812 | 4.078 | 20 | 50 | fits | 113,598 | 194 | 0.317 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 503,418 | 5.034 | 20 | 20 | fits | 83,945 | 35 | 0.755 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 834,029 | 8.340 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 365,604 | 3.656 | 20 | 20 | fits | 118,642 | 202 | 0.331 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 288,963 | 2.890 | 20 | 200 | fits | 143,903 | 209 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 418,756 | 4.188 | 20 | 200 | fits | 118,642 | 202 | 0.331 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 289,887 | 2.899 | 20 | 20 | fits | 143,903 | 209 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 419,460 | 4.195 | 20 | 20 | fits | 118,642 | 202 | 0.331 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 149,624 | 1.496 | 20 | 24 | fits | 142,898 | 142 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 292,537 | 2.925 | 20 | 24 | fits | 143,903 | 209 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 292,471 | 2.925 | 20 | 50 | fits | 143,903 | 209 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 422,484 | 4.225 | 20 | 50 | fits | 118,642 | 202 | 0.331 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 502,547 | 5.025 | 20 | 20 | fits | 80,129 | 28 | 0.746 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 833,508 | 8.335 | 20 | 20 | fits | 76,245 | 32 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 353,008 | 3.530 | 20 | 20 | fits | 106,721 | 188 | 0.273 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 291,909 | 2.919 | 20 | 200 | fits | 145,310 | 210 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 398,014 | 3.980 | 20 | 200 | fits | 106,721 | 188 | 0.273 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 292,833 | 2.928 | 20 | 20 | fits | 145,310 | 210 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 398,718 | 3.987 | 20 | 20 | fits | 106,721 | 188 | 0.273 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 151,163 | 1.512 | 20 | 24 | fits | 142,898 | 142 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 295,483 | 2.955 | 20 | 24 | fits | 145,310 | 210 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 295,417 | 2.954 | 20 | 50 | fits | 145,310 | 210 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 401,742 | 4.017 | 20 | 50 | fits | 106,721 | 188 | 0.273 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 497,552 | 4.976 | 20 | 20 | fits | 84,149 | 35 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 828,163 | 8.282 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 368,128 | 3.681 | 20 | 20 | fits | 111,805 | 194 | 0.346 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 291,388 | 2.914 | 20 | 200 | fits | 145,509 | 211 | 0.369 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 414,227 | 4.142 | 20 | 200 | fits | 111,805 | 194 | 0.346 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 292,312 | 2.923 | 20 | 20 | fits | 145,509 | 211 | 0.369 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 414,931 | 4.149 | 20 | 20 | fits | 111,805 | 194 | 0.346 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 150,443 | 1.504 | 20 | 24 | fits | 142,898 | 142 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 294,962 | 2.950 | 20 | 24 | fits | 145,509 | 211 | 0.369 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 294,896 | 2.949 | 20 | 50 | fits | 145,509 | 211 | 0.369 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 417,955 | 4.180 | 20 | 50 | fits | 111,805 | 194 | 0.346 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 498,225 | 4.982 | 20 | 20 | fits | 80,336 | 28 | 0.748 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 829,005 | 8.290 | 20 | 20 | fits | 76,245 | 32 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 363,478 | 3.635 | 20 | 20 | fits | 106,553 | 187 | 0.271 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 302,373 | 3.024 | 20 | 200 | fits | 147,235 | 215 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 408,310 | 4.083 | 20 | 200 | fits | 106,553 | 187 | 0.271 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 303,297 | 3.033 | 20 | 20 | fits | 147,235 | 215 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 409,014 | 4.090 | 20 | 20 | fits | 106,553 | 187 | 0.271 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 149,817 | 1.498 | 20 | 24 | fits | 142,992 | 143 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 305,947 | 3.059 | 20 | 24 | fits | 147,235 | 215 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 305,881 | 3.059 | 20 | 50 | fits | 147,235 | 215 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 412,038 | 4.120 | 20 | 50 | fits | 106,553 | 187 | 0.271 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 492,070 | 4.921 | 20 | 20 | fits | 80,098 | 28 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 826,633 | 8.266 | 20 | 20 | fits | 80,243 | 38 | 0.618 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 352,142 | 3.521 | 20 | 20 | fits | 105,292 | 184 | 0.279 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 293,720 | 2.937 | 20 | 200 | fits | 146,649 | 214 | 0.362 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 398,396 | 3.984 | 20 | 200 | fits | 105,292 | 184 | 0.279 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 294,644 | 2.946 | 20 | 20 | fits | 146,649 | 214 | 0.362 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 399,100 | 3.991 | 20 | 20 | fits | 105,292 | 184 | 0.279 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 151,635 | 1.516 | 20 | 24 | fits | 142,552 | 142 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 297,294 | 2.973 | 20 | 24 | fits | 146,649 | 214 | 0.362 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 297,228 | 2.972 | 20 | 50 | fits | 146,649 | 214 | 0.362 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 402,124 | 4.021 | 20 | 50 | fits | 105,292 | 184 | 0.279 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 482,252 | 4.823 | 20 | 20 | fits | 80,194 | 28 | 0.746 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 935,297 | 9.353 | 20 | 20 | fits | 28,077 | 12 | 0.814 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 351,422 | 3.514 | 20 | 20 | fits | 105,292 | 184 | 0.279 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 293,000 | 2.930 | 20 | 200 | fits | 146,649 | 214 | 0.362 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 397,676 | 3.977 | 20 | 200 | fits | 105,292 | 184 | 0.279 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 293,924 | 2.939 | 20 | 20 | fits | 146,649 | 214 | 0.362 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 398,380 | 3.984 | 20 | 20 | fits | 105,292 | 184 | 0.279 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 150,915 | 1.509 | 20 | 24 | fits | 142,552 | 142 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 296,574 | 2.966 | 20 | 24 | fits | 146,649 | 214 | 0.362 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 296,508 | 2.965 | 20 | 50 | fits | 146,649 | 214 | 0.362 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 401,404 | 4.014 | 20 | 50 | fits | 105,292 | 184 | 0.279 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 481,532 | 4.815 | 20 | 20 | fits | 80,194 | 28 | 0.746 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 935,784 | 9.358 | 20 | 20 | fits | 37,545 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 350,702 | 3.507 | 20 | 20 | fits | 105,292 | 184 | 0.279 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 292,280 | 2.923 | 20 | 200 | fits | 146,649 | 214 | 0.362 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 396,956 | 3.970 | 20 | 200 | fits | 105,292 | 184 | 0.279 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 293,204 | 2.932 | 20 | 20 | fits | 146,649 | 214 | 0.362 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 397,660 | 3.977 | 20 | 20 | fits | 105,292 | 184 | 0.279 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 150,195 | 1.502 | 20 | 24 | fits | 142,552 | 142 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 295,854 | 2.959 | 20 | 24 | fits | 146,649 | 214 | 0.362 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 295,788 | 2.958 | 20 | 50 | fits | 146,649 | 214 | 0.362 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 400,684 | 4.007 | 20 | 50 | fits | 105,292 | 184 | 0.279 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 484,925 | 4.849 | 20 | 20 | fits | 84,307 | 34 | 0.753 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 934,832 | 9.348 | 20 | 20 | fits | 27,672 | 12 | 0.806 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 356,701 | 3.567 | 20 | 20 | fits | 112,196 | 191 | 0.319 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 291,560 | 2.916 | 20 | 200 | fits | 146,649 | 214 | 0.362 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 403,140 | 4.031 | 20 | 200 | fits | 112,196 | 191 | 0.319 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 292,484 | 2.925 | 20 | 20 | fits | 146,649 | 214 | 0.362 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 403,844 | 4.038 | 20 | 20 | fits | 112,196 | 191 | 0.319 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 149,475 | 1.495 | 20 | 24 | fits | 142,552 | 142 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 295,134 | 2.951 | 20 | 24 | fits | 146,649 | 214 | 0.362 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 295,068 | 2.951 | 20 | 50 | fits | 146,649 | 214 | 0.362 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 406,868 | 4.069 | 20 | 50 | fits | 112,196 | 191 | 0.319 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 582,877 | 5.829 | 20 | 20 | fits | 84,434 | 35 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 914,185 | 9.142 | 20 | 20 | fits | 76,245 | 32 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 450,834 | 4.508 | 20 | 20 | fits | 119,298 | 202 | 0.338 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 288,114 | 2.881 | 20 | 200 | fits | 143,923 | 209 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 498,030 | 4.980 | 20 | 200 | fits | 119,298 | 202 | 0.338 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 289,038 | 2.890 | 20 | 20 | fits | 143,923 | 209 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 498,734 | 4.987 | 20 | 20 | fits | 119,298 | 202 | 0.338 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 148,755 | 1.488 | 20 | 24 | fits | 142,552 | 142 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 291,688 | 2.917 | 20 | 24 | fits | 143,923 | 209 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 291,622 | 2.916 | 20 | 50 | fits | 143,923 | 209 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 501,758 | 5.018 | 20 | 50 | fits | 119,298 | 202 | 0.338 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 581,781 | 5.818 | 20 | 20 | fits | 80,089 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 912,315 | 9.123 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 346,719 | 3.467 | 20 | 20 | fits | 108,408 | 175 | 0.262 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 291,006 | 2.910 | 20 | 200 | fits | 144,574 | 225 | 0.367 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 398,798 | 3.988 | 20 | 200 | fits | 108,408 | 175 | 0.262 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 291,930 | 2.919 | 20 | 20 | fits | 144,574 | 225 | 0.367 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 399,502 | 3.995 | 20 | 20 | fits | 108,408 | 175 | 0.262 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 150,996 | 1.510 | 20 | 24 | fits | 142,552 | 142 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 294,580 | 2.946 | 20 | 24 | fits | 144,574 | 225 | 0.367 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 294,514 | 2.945 | 20 | 50 | fits | 144,574 | 225 | 0.367 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 402,526 | 4.025 | 20 | 50 | fits | 108,408 | 175 | 0.262 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 482,654 | 4.827 | 20 | 20 | fits | 80,194 | 28 | 0.746 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 831,046 | 8.310 | 20 | 20 | fits | 85,319 | 36 | 0.557 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 345,999 | 3.460 | 20 | 20 | fits | 108,408 | 175 | 0.262 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 290,286 | 2.903 | 20 | 200 | fits | 144,574 | 225 | 0.367 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 398,078 | 3.981 | 20 | 200 | fits | 108,408 | 175 | 0.262 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 291,210 | 2.912 | 20 | 20 | fits | 144,574 | 225 | 0.367 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 398,782 | 3.988 | 20 | 20 | fits | 108,408 | 175 | 0.262 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 150,276 | 1.503 | 20 | 24 | fits | 142,552 | 142 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 293,860 | 2.939 | 20 | 24 | fits | 144,574 | 225 | 0.367 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 293,794 | 2.938 | 20 | 50 | fits | 144,574 | 225 | 0.367 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 401,806 | 4.018 | 20 | 50 | fits | 108,408 | 175 | 0.262 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 482,077 | 4.821 | 20 | 20 | fits | 80,337 | 29 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 830,640 | 8.306 | 20 | 20 | fits | 85,319 | 36 | 0.557 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 349,080 | 3.491 | 20 | 20 | fits | 111,987 | 182 | 0.283 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 289,566 | 2.896 | 20 | 200 | fits | 144,574 | 225 | 0.367 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 400,937 | 4.009 | 20 | 200 | fits | 111,987 | 182 | 0.283 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 290,490 | 2.905 | 20 | 20 | fits | 144,574 | 225 | 0.367 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 401,641 | 4.016 | 20 | 20 | fits | 111,987 | 182 | 0.283 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 149,556 | 1.496 | 20 | 24 | fits | 142,552 | 142 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 293,140 | 2.931 | 20 | 24 | fits | 144,574 | 225 | 0.367 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 293,074 | 2.931 | 20 | 50 | fits | 144,574 | 225 | 0.367 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 404,665 | 4.047 | 20 | 50 | fits | 111,987 | 182 | 0.283 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 498,153 | 4.982 | 20 | 20 | fits | 81,796 | 29 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 833,427 | 8.334 | 20 | 20 | fits | 80,649 | 38 | 0.625 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 360,827 | 3.608 | 20 | 20 | fits | 113,697 | 182 | 0.339 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 288,991 | 2.890 | 20 | 200 | fits | 144,719 | 226 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 413,839 | 4.138 | 20 | 200 | fits | 113,697 | 182 | 0.339 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 289,915 | 2.899 | 20 | 20 | fits | 144,719 | 226 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 414,543 | 4.145 | 20 | 20 | fits | 113,697 | 182 | 0.339 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 148,836 | 1.488 | 20 | 24 | fits | 142,552 | 142 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 292,565 | 2.926 | 20 | 24 | fits | 144,719 | 226 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 292,499 | 2.925 | 20 | 50 | fits | 144,719 | 226 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 417,567 | 4.176 | 20 | 50 | fits | 113,697 | 182 | 0.339 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 497,705 | 4.977 | 20 | 20 | fits | 80,204 | 28 | 0.746 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 832,912 | 8.329 | 20 | 20 | fits | 85,376 | 36 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 355,444 | 3.554 | 20 | 20 | fits | 108,435 | 175 | 0.261 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 299,754 | 2.998 | 20 | 200 | fits | 146,211 | 230 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 407,573 | 4.076 | 20 | 200 | fits | 108,435 | 175 | 0.261 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 300,678 | 3.007 | 20 | 20 | fits | 146,211 | 230 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 408,277 | 4.083 | 20 | 20 | fits | 108,435 | 175 | 0.261 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 148,174 | 1.482 | 20 | 24 | fits | 142,610 | 143 | 0.379 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 303,328 | 3.033 | 20 | 24 | fits | 146,211 | 230 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 303,262 | 3.033 | 20 | 50 | fits | 146,211 | 230 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 411,301 | 4.113 | 20 | 50 | fits | 108,435 | 175 | 0.261 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 491,417 | 4.914 | 20 | 20 | fits | 80,182 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 826,105 | 8.261 | 20 | 20 | fits | 85,319 | 36 | 0.557 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 352,598 | 3.526 | 20 | 20 | fits | 106,617 | 187 | 0.273 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 291,499 | 2.915 | 20 | 200 | fits | 145,310 | 210 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 397,500 | 3.975 | 20 | 200 | fits | 106,617 | 187 | 0.273 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 292,423 | 2.924 | 20 | 20 | fits | 145,310 | 210 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 398,204 | 3.982 | 20 | 20 | fits | 106,617 | 187 | 0.273 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 150,753 | 1.508 | 20 | 24 | fits | 142,898 | 142 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 295,073 | 2.951 | 20 | 24 | fits | 145,310 | 210 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 295,007 | 2.950 | 20 | 50 | fits | 145,310 | 210 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 401,228 | 4.012 | 20 | 50 | fits | 106,617 | 187 | 0.273 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 485,343 | 4.853 | 20 | 20 | fits | 84,181 | 34 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 832,775 | 8.328 | 20 | 20 | fits | 80,748 | 39 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 358,563 | 3.586 | 20 | 20 | fits | 113,434 | 193 | 0.315 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 290,779 | 2.908 | 20 | 200 | fits | 145,310 | 210 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 403,597 | 4.036 | 20 | 200 | fits | 113,434 | 193 | 0.315 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 291,703 | 2.917 | 20 | 20 | fits | 145,310 | 210 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 404,301 | 4.043 | 20 | 20 | fits | 113,434 | 193 | 0.315 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 150,033 | 1.500 | 20 | 24 | fits | 142,898 | 142 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 294,353 | 2.944 | 20 | 24 | fits | 145,310 | 210 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 294,287 | 2.943 | 20 | 50 | fits | 145,310 | 210 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 407,325 | 4.073 | 20 | 50 | fits | 113,434 | 193 | 0.315 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 487,376 | 4.874 | 20 | 20 | fits | 80,117 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 835,548 | 8.355 | 20 | 20 | fits | 85,679 | 36 | 0.567 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 349,119 | 3.491 | 20 | 20 | fits | 113,226 | 196 | 0.250 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 288,488 | 2.885 | 20 | 200 | fits | 143,739 | 208 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 401,098 | 4.011 | 20 | 200 | fits | 113,226 | 196 | 0.250 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 289,412 | 2.894 | 20 | 20 | fits | 143,739 | 208 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 401,802 | 4.018 | 20 | 20 | fits | 113,226 | 196 | 0.250 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 149,313 | 1.493 | 20 | 24 | fits | 142,898 | 142 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 292,062 | 2.921 | 20 | 24 | fits | 143,739 | 208 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 291,996 | 2.920 | 20 | 50 | fits | 143,739 | 208 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 404,826 | 4.048 | 20 | 50 | fits | 113,226 | 196 | 0.250 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 485,097 | 4.851 | 20 | 20 | fits | 80,337 | 29 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 833,509 | 8.335 | 20 | 20 | fits | 85,319 | 36 | 0.557 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 355,587 | 3.556 | 20 | 20 | fits | 108,783 | 175 | 0.269 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 299,908 | 2.999 | 20 | 200 | fits | 146,428 | 230 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 408,075 | 4.081 | 20 | 200 | fits | 108,783 | 175 | 0.269 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 300,832 | 3.008 | 20 | 20 | fits | 146,428 | 230 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 408,779 | 4.088 | 20 | 20 | fits | 108,783 | 175 | 0.269 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 148,111 | 1.481 | 20 | 24 | fits | 142,644 | 143 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 303,482 | 3.035 | 20 | 24 | fits | 146,428 | 230 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 303,416 | 3.034 | 20 | 50 | fits | 146,428 | 230 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 411,803 | 4.118 | 20 | 50 | fits | 108,783 | 175 | 0.269 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 491,793 | 4.918 | 20 | 20 | fits | 80,056 | 28 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 822,283 | 8.223 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 354,791 | 3.548 | 20 | 20 | fits | 108,783 | 175 | 0.269 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 299,112 | 2.991 | 20 | 200 | fits | 146,355 | 230 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 407,279 | 4.073 | 20 | 200 | fits | 108,783 | 175 | 0.269 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 300,036 | 3.000 | 20 | 20 | fits | 146,355 | 230 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 407,983 | 4.080 | 20 | 20 | fits | 108,783 | 175 | 0.269 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 147,388 | 1.474 | 20 | 24 | fits | 142,641 | 143 | 0.379 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 302,686 | 3.027 | 20 | 24 | fits | 146,355 | 230 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 302,620 | 3.026 | 20 | 50 | fits | 146,355 | 230 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 411,007 | 4.110 | 20 | 50 | fits | 108,783 | 175 | 0.269 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 490,997 | 4.910 | 20 | 20 | fits | 80,056 | 28 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 821,487 | 8.215 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 345,799 | 3.458 | 20 | 20 | fits | 108,430 | 175 | 0.263 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 290,064 | 2.901 | 20 | 200 | fits | 144,725 | 225 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 397,878 | 3.979 | 20 | 200 | fits | 108,430 | 175 | 0.263 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 290,988 | 2.910 | 20 | 20 | fits | 144,725 | 225 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 398,582 | 3.986 | 20 | 20 | fits | 108,430 | 175 | 0.263 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 149,903 | 1.499 | 20 | 24 | fits | 142,898 | 142 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 293,638 | 2.936 | 20 | 24 | fits | 144,725 | 225 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 293,572 | 2.936 | 20 | 50 | fits | 144,725 | 225 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 401,606 | 4.016 | 20 | 50 | fits | 108,430 | 175 | 0.263 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 481,734 | 4.817 | 20 | 20 | fits | 80,194 | 28 | 0.746 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 833,098 | 8.331 | 20 | 20 | fits | 84,531 | 45 | 0.655 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 345,079 | 3.451 | 20 | 20 | fits | 108,430 | 175 | 0.263 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 289,344 | 2.893 | 20 | 200 | fits | 144,725 | 225 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 397,158 | 3.972 | 20 | 200 | fits | 108,430 | 175 | 0.263 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 290,268 | 2.903 | 20 | 20 | fits | 144,725 | 225 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 397,862 | 3.979 | 20 | 20 | fits | 108,430 | 175 | 0.263 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 149,183 | 1.492 | 20 | 24 | fits | 142,898 | 142 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 292,918 | 2.929 | 20 | 24 | fits | 144,725 | 225 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 292,852 | 2.929 | 20 | 50 | fits | 144,725 | 225 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 400,886 | 4.009 | 20 | 50 | fits | 108,430 | 175 | 0.263 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 481,014 | 4.810 | 20 | 20 | fits | 80,194 | 28 | 0.746 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 929,372 | 9.294 | 20 | 20 | fits | 27,826 | 12 | 0.808 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 344,359 | 3.444 | 20 | 20 | fits | 108,430 | 175 | 0.263 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 288,624 | 2.886 | 20 | 200 | fits | 144,725 | 225 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 396,438 | 3.964 | 20 | 200 | fits | 108,430 | 175 | 0.263 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 289,548 | 2.895 | 20 | 20 | fits | 144,725 | 225 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 397,142 | 3.971 | 20 | 20 | fits | 108,430 | 175 | 0.263 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 148,463 | 1.485 | 20 | 24 | fits | 142,898 | 142 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 292,198 | 2.922 | 20 | 24 | fits | 144,725 | 225 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 292,132 | 2.921 | 20 | 50 | fits | 144,725 | 225 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 400,166 | 4.002 | 20 | 50 | fits | 108,430 | 175 | 0.263 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 480,437 | 4.804 | 20 | 20 | fits | 80,337 | 29 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 911,205 | 9.112 | 20 | 20 | fits | 85,389 | 36 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 343,639 | 3.436 | 20 | 20 | fits | 108,534 | 176 | 0.264 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 287,904 | 2.879 | 20 | 200 | fits | 144,725 | 225 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 395,822 | 3.958 | 20 | 200 | fits | 108,534 | 176 | 0.264 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 288,828 | 2.888 | 20 | 20 | fits | 144,725 | 225 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 396,526 | 3.965 | 20 | 20 | fits | 108,534 | 176 | 0.264 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 147,743 | 1.477 | 20 | 24 | fits | 142,898 | 142 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 291,478 | 2.915 | 20 | 24 | fits | 144,725 | 225 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 291,412 | 2.914 | 20 | 50 | fits | 144,725 | 225 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 399,550 | 3.995 | 20 | 50 | fits | 108,534 | 176 | 0.264 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 499,118 | 4.991 | 20 | 20 | fits | 87,907 | 41 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 908,960 | 9.090 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 365,705 | 3.657 | 20 | 20 | fits | 120,270 | 188 | 0.358 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 287,347 | 2.873 | 20 | 200 | fits | 144,888 | 226 | 0.369 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 418,768 | 4.188 | 20 | 200 | fits | 120,270 | 188 | 0.358 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 288,271 | 2.883 | 20 | 20 | fits | 144,888 | 226 | 0.369 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 419,472 | 4.195 | 20 | 20 | fits | 120,270 | 188 | 0.358 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 147,023 | 1.470 | 20 | 24 | fits | 142,898 | 142 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 290,921 | 2.909 | 20 | 24 | fits | 144,888 | 226 | 0.369 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 290,855 | 2.909 | 20 | 50 | fits | 144,888 | 226 | 0.369 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 422,496 | 4.225 | 20 | 50 | fits | 120,270 | 188 | 0.358 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 580,479 | 5.805 | 20 | 20 | fits | 80,272 | 29 | 0.746 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 911,378 | 9.114 | 20 | 20 | fits | 76,245 | 32 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 437,925 | 4.379 | 20 | 20 | fits | 116,645 | 202 | 0.289 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 296,859 | 2.969 | 20 | 200 | fits | 145,335 | 208 | 0.393 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 490,422 | 4.904 | 20 | 200 | fits | 116,645 | 202 | 0.289 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 297,783 | 2.978 | 20 | 20 | fits | 145,335 | 208 | 0.393 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 491,126 | 4.911 | 20 | 20 | fits | 116,645 | 202 | 0.289 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 146,379 | 1.464 | 20 | 24 | fits | 142,974 | 143 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 300,433 | 3.004 | 20 | 24 | fits | 145,335 | 208 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 300,367 | 3.004 | 20 | 50 | fits | 145,335 | 208 | 0.393 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 494,150 | 4.941 | 20 | 50 | fits | 116,645 | 202 | 0.289 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 574,085 | 5.741 | 20 | 20 | fits | 80,001 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 904,762 | 9.048 | 20 | 20 | fits | 76,331 | 33 | 0.581 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 336,517 | 3.365 | 20 | 20 | fits | 105,745 | 185 | 0.290 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 289,485 | 2.895 | 20 | 200 | fits | 146,809 | 214 | 0.362 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 394,614 | 3.946 | 20 | 200 | fits | 105,745 | 185 | 0.290 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 290,409 | 2.904 | 20 | 20 | fits | 146,809 | 214 | 0.362 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 395,318 | 3.953 | 20 | 20 | fits | 105,745 | 185 | 0.290 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 147,240 | 1.472 | 20 | 24 | fits | 142,898 | 142 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 293,059 | 2.931 | 20 | 24 | fits | 146,809 | 214 | 0.362 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 292,993 | 2.930 | 20 | 50 | fits | 146,809 | 214 | 0.362 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 398,342 | 3.983 | 20 | 50 | fits | 105,745 | 185 | 0.290 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 494,088 | 4.941 | 20 | 20 | fits | 84,045 | 35 | 0.757 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 824,854 | 8.249 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 352,158 | 3.522 | 20 | 20 | fits | 111,206 | 191 | 0.364 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 288,964 | 2.890 | 20 | 200 | fits | 147,008 | 215 | 0.363 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 411,268 | 4.113 | 20 | 200 | fits | 111,206 | 191 | 0.364 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 289,888 | 2.899 | 20 | 20 | fits | 147,008 | 215 | 0.363 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 411,972 | 4.120 | 20 | 20 | fits | 111,206 | 191 | 0.364 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 146,520 | 1.465 | 20 | 24 | fits | 142,898 | 142 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 292,538 | 2.925 | 20 | 24 | fits | 147,008 | 215 | 0.363 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 292,472 | 2.925 | 20 | 50 | fits | 147,008 | 215 | 0.363 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 414,996 | 4.150 | 20 | 50 | fits | 111,206 | 191 | 0.364 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 495,348 | 4.953 | 20 | 20 | fits | 80,418 | 28 | 0.749 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 826,260 | 8.263 | 20 | 20 | fits | 76,245 | 32 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 346,991 | 3.470 | 20 | 20 | fits | 105,711 | 184 | 0.290 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 299,949 | 2.999 | 20 | 200 | fits | 148,734 | 219 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 405,044 | 4.050 | 20 | 200 | fits | 105,711 | 184 | 0.290 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 300,873 | 3.009 | 20 | 20 | fits | 148,734 | 219 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 405,748 | 4.057 | 20 | 20 | fits | 105,711 | 184 | 0.290 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 145,894 | 1.459 | 20 | 24 | fits | 142,992 | 143 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 303,523 | 3.035 | 20 | 24 | fits | 148,734 | 219 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 303,457 | 3.035 | 20 | 50 | fits | 148,734 | 219 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 408,772 | 4.088 | 20 | 50 | fits | 105,711 | 184 | 0.290 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 488,970 | 4.890 | 20 | 20 | fits | 80,264 | 28 | 0.746 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 823,662 | 8.237 | 20 | 20 | fits | 80,243 | 38 | 0.618 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 344,850 | 3.449 | 20 | 20 | fits | 108,648 | 175 | 0.268 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 289,152 | 2.892 | 20 | 200 | fits | 144,751 | 225 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 397,184 | 3.972 | 20 | 200 | fits | 108,648 | 175 | 0.268 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 290,076 | 2.901 | 20 | 20 | fits | 144,751 | 225 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 397,888 | 3.979 | 20 | 20 | fits | 108,648 | 175 | 0.268 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 148,965 | 1.490 | 20 | 24 | fits | 142,468 | 142 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 292,726 | 2.927 | 20 | 24 | fits | 144,751 | 225 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 292,660 | 2.927 | 20 | 50 | fits | 144,751 | 225 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 400,912 | 4.009 | 20 | 50 | fits | 108,648 | 175 | 0.268 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 480,914 | 4.809 | 20 | 20 | fits | 80,068 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 815,518 | 8.155 | 20 | 20 | fits | 85,462 | 37 | 0.556 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 344,214 | 3.442 | 20 | 20 | fits | 108,648 | 175 | 0.268 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 288,516 | 2.885 | 20 | 200 | fits | 144,751 | 225 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 396,548 | 3.965 | 20 | 200 | fits | 108,648 | 175 | 0.268 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 289,440 | 2.894 | 20 | 20 | fits | 144,751 | 225 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 397,252 | 3.973 | 20 | 20 | fits | 108,648 | 175 | 0.268 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 148,329 | 1.483 | 20 | 24 | fits | 142,552 | 142 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 292,090 | 2.921 | 20 | 24 | fits | 144,751 | 225 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 292,024 | 2.920 | 20 | 50 | fits | 144,751 | 225 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 400,276 | 4.003 | 20 | 50 | fits | 108,648 | 175 | 0.268 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 480,278 | 4.803 | 20 | 20 | fits | 80,068 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 850,744 | 8.507 | 20 | 20 | fits | 27,743 | 12 | 0.806 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 343,494 | 3.435 | 20 | 20 | fits | 108,648 | 175 | 0.268 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 287,796 | 2.878 | 20 | 200 | fits | 144,751 | 225 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 395,828 | 3.958 | 20 | 200 | fits | 108,648 | 175 | 0.268 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 288,720 | 2.887 | 20 | 20 | fits | 144,751 | 225 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 396,532 | 3.965 | 20 | 20 | fits | 108,648 | 175 | 0.268 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 147,609 | 1.476 | 20 | 24 | fits | 142,552 | 142 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 291,370 | 2.914 | 20 | 24 | fits | 144,751 | 225 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 291,304 | 2.913 | 20 | 50 | fits | 144,751 | 225 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 399,556 | 3.996 | 20 | 50 | fits | 108,648 | 175 | 0.268 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 483,671 | 4.837 | 20 | 20 | fits | 84,181 | 34 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 831,543 | 8.315 | 20 | 20 | fits | 85,319 | 36 | 0.557 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 349,108 | 3.491 | 20 | 20 | fits | 115,138 | 182 | 0.300 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 287,076 | 2.871 | 20 | 200 | fits | 144,751 | 225 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 401,598 | 4.016 | 20 | 200 | fits | 115,138 | 182 | 0.300 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 288,000 | 2.880 | 20 | 20 | fits | 144,751 | 225 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 402,302 | 4.023 | 20 | 20 | fits | 115,138 | 182 | 0.300 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 146,889 | 1.469 | 20 | 24 | fits | 142,552 | 142 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 290,650 | 2.906 | 20 | 24 | fits | 144,751 | 225 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 290,584 | 2.906 | 20 | 50 | fits | 144,751 | 225 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 405,326 | 4.053 | 20 | 50 | fits | 115,138 | 182 | 0.300 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 501,006 | 5.010 | 20 | 20 | fits | 84,019 | 35 | 0.756 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 831,599 | 8.316 | 20 | 20 | fits | 76,188 | 32 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 361,712 | 3.617 | 20 | 20 | fits | 118,922 | 202 | 0.335 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 285,523 | 2.855 | 20 | 200 | fits | 143,918 | 209 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 415,479 | 4.155 | 20 | 200 | fits | 118,922 | 202 | 0.335 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 286,447 | 2.864 | 20 | 20 | fits | 143,918 | 209 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 416,183 | 4.162 | 20 | 20 | fits | 118,922 | 202 | 0.335 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 146,169 | 1.462 | 20 | 24 | fits | 142,552 | 142 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 289,097 | 2.891 | 20 | 24 | fits | 143,918 | 209 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 289,031 | 2.890 | 20 | 50 | fits | 143,918 | 209 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 419,207 | 4.192 | 20 | 50 | fits | 118,922 | 202 | 0.335 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 499,380 | 4.994 | 20 | 20 | fits | 80,239 | 28 | 0.746 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 830,323 | 8.303 | 20 | 20 | fits | 76,245 | 32 | 0.584 |
| LINK_UP | `adp.link_up.if0` | 2,385 | 0.024 | 20 | 200 | fits | 24,119 | 43 (11) | 0.678 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 6,239 | 0.062 | 20 | 200 | fits | 17,701 | 23 (39) | 0.593 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 5,792 | 0.058 | 20 | 200 | fits | 2,110 | 10 (11) | 0.368 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 152,442 | 1.524 | 20 | 200 | fits | 153,382 | 273 | 0.370 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 203,786 | 2.038 | 20 | 20 | fits | 136,452 | 264 | 0.204 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 265,477 | 2.655 | 20 | 24 | fits | 89,897 | 58 | 0.528 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 164,311 | 1.643 | 20 | 50 | fits | 136,452 | 264 | 0.204 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 766,707 | 7.667 | 20 | 20 | fits | 42,526 | 22 | 0.768 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 209,080 | 2.091 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 152,442 | 1.524 | 20 | 200 | fits | 153,382 | 273 | 0.370 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 190,757 | 1.908 | 20 | 20 | fits | 137,888 | 270 | 0.214 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 234,425 | 2.344 | 20 | 24 | fits | 76,014 | 60 | 0.436 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 179,798 | 1.798 | 20 | 50 | fits | 86,968 | 71 | 0.677 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 780,085 | 7.801 | 20 | 20 | fits | 71,756 | 40 | 0.624 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 231,797 | 2.318 | 49 | 49 | fits | 0 | - | 0.000 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 20,135 | 0.201 | 20 | 20 | fits | 27,124 | 21 (35) | 0.787 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 12,539 | 0.125 | 20 | 20 | fits | 22,441 | 17 (14) | 0.812 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 13,367 | 0.134 | 20 | 20 | fits | 22,082 | 18 (14) | 0.810 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 11,031 | 0.110 | 20 | 20 | fits | 26,877 | 21 (35) | 0.779 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 73,703 | 0.737 | 20 | 20 | fits | 29,488 | 8 | 0.824 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 39,297 | 0.393 | 20 | 20 | fits | 39,363 | 12 | 0.886 |
| malformed MRPDU discard | `srp.malformed.if0` | 17,614 | 0.176 | 20 | 20 | fits | 17,680 | 12 | 0.691 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 76,613 | 0.766 | 220 | 220 | fits | 53,555 | 6 | 0.920 |
| an event behind 15 others | `backlog.event.if0` | 154,138 | 1.541 | 20 | 200 | fits | 47,942 | 79 | 0.516 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 400,721 | 4.007 | 20 | 20 | fits | 36,679 | 63 | 0.227 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 396,048 | 3.960 | 20 | 200 | fits | 148,751 | 166 | 0.295 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 395,432 | 3.954 | 20 | 200 | fits | 148,751 | 166 | 0.295 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 391,726 | 3.917 | 20 | 20 | fits | 148,751 | 166 | 0.295 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 427,569 | 4.276 | 20 | 20 | fits | 36,679 | 63 | 0.227 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 144,424 | 1.444 | 20 | 24 | fits | 145,315 | 148 | 0.401 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 394,376 | 3.944 | 20 | 24 | fits | 148,751 | 166 | 0.295 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 394,310 | 3.943 | 20 | 50 | fits | 148,751 | 166 | 0.295 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 393,914 | 3.939 | 20 | 50 | fits | 148,751 | 166 | 0.295 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 430,527 | 4.305 | 20 | 20 | fits | 36,679 | 63 | 0.227 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 483,755 | 4.838 | 20 | 20 | fits | 21,934 | 41 | 0.083 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 344,539 | 3.445 | 20 | 20 | fits | 106,494 | 188 | 0.272 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 283,618 | 2.836 | 20 | 200 | fits | 145,174 | 210 | 0.365 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 389,496 | 3.895 | 20 | 200 | fits | 106,494 | 188 | 0.272 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 284,542 | 2.845 | 20 | 20 | fits | 145,174 | 210 | 0.365 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 390,200 | 3.902 | 20 | 20 | fits | 106,494 | 188 | 0.272 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 143,008 | 1.430 | 20 | 24 | fits | 143,194 | 145 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 287,192 | 2.872 | 20 | 24 | fits | 145,174 | 210 | 0.365 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 287,126 | 2.871 | 20 | 50 | fits | 145,174 | 210 | 0.365 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 393,224 | 3.932 | 20 | 50 | fits | 106,494 | 188 | 0.272 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 489,104 | 4.891 | 20 | 20 | fits | 84,219 | 35 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 823,720 | 8.237 | 20 | 20 | fits | 85,314 | 36 | 0.557 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 16,989 | 0.170 | 20 | 20 | fits | 23,988 | 19 | 0.748 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 283,618 | 2.836 | 20 | 200 | fits | 145,174 | 210 | 0.365 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 32,885 | 0.329 | 20 | 200 | fits | 23,988 | 19 | 0.748 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 284,542 | 2.845 | 20 | 20 | fits | 145,174 | 210 | 0.365 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 379,574 | 3.796 | 20 | 20 | fits | 95,868 | 178 | 0.184 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 143,008 | 1.430 | 20 | 24 | fits | 143,194 | 145 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 287,192 | 2.872 | 20 | 24 | fits | 145,174 | 210 | 0.365 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 287,126 | 2.871 | 20 | 50 | fits | 145,174 | 210 | 0.365 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 382,598 | 3.826 | 20 | 50 | fits | 95,868 | 178 | 0.184 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 478,418 | 4.784 | 20 | 20 | fits | 83,865 | 35 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 812,963 | 8.130 | 20 | 20 | fits | 85,314 | 36 | 0.557 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,280,535 | 62.805 | 20 | 20 | MISS ceiling | 16,777 | 14 | 0.472 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,297,193 | 62.972 | 20 | 20 | MISS ceiling | 16,639 | 13 | 0.442 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,313,686 | 63.137 | 20 | 20 | MISS ceiling | 16,513 | 13 | 0.449 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,330,200 | 63.302 | 20 | 20 | MISS ceiling | 16,590 | 13 | 0.423 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,346,541 | 63.465 | 20 | 20 | MISS ceiling | 16,404 | 13 | 0.449 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 145,499 | 1.455 | 20 | 200 | fits | 146,011 | 208 | 0.393 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 223,073 | 2.231 | 20 | 200 | fits | 78,190 | 176 | 0.241 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 141,177 | 1.412 | 20 | 20 | fits | 146,011 | 208 | 0.393 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,200,219 | 62.002 | 20 | 20 | MISS ceiling | 27,081 | 15 | 0.652 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 144,817 | 1.448 | 20 | 24 | fits | 146,011 | 208 | 0.393 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,176,624 | 61.766 | 20 | 24 | MISS ceiling | 145,609 | 106 | 0.410 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 143,761 | 1.438 | 20 | 50 | fits | 146,011 | 208 | 0.393 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 221,555 | 2.216 | 20 | 50 | fits | 78,190 | 176 | 0.241 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 300,469 | 3.005 | 20 | 20 | fits | 78,980 | 28 | 0.734 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 631,638 | 6.316 | 20 | 20 | fits | 84,534 | 36 | 0.537 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,674 | 0.057 | 20 | 20 | fits | 20,390 | 13 (29) | 0.649 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,633 | 0.076 | 20 | 20 | fits | 23,216 | 19 (35) | 0.731 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 9,893 | 0.099 | 20 | 20 | fits | 26,833 | 21 (12) | 0.779 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 10,189 | 0.102 | 20 | 50 | fits | 24,119 | 43 | 0.678 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 15,705 | 0.157 | 20 | 50 | fits | 19,994 | 35 | 0.598 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 14,414 | 0.144 | 20 | 50 | fits | 19,978 | 35 | 0.598 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 16,708 | 0.167 | 20 | 50 | fits | 24,977 | 61 | 0.555 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 18,664 | 0.187 | 20 | 50 | fits | 24,977 | 61 | 0.555 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 8,699 | 0.087 | 20 | 50 | fits | 19,498 | 30 | 0.596 |
| LINK_UP | `adp.link_up.if0` | 2,385 | 0.024 | 20 | 200 | fits | 24,119 | 43 (11) | 0.678 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 6,239 | 0.062 | 20 | 200 | fits | 17,701 | 23 (39) | 0.593 |
| LINK_DOWN | `adp.link_down.if0` | 1,933 | 0.019 | 20 | 200 | fits | 19,657 | 23 (9) | 0.671 |
| LINK_UP | `adp.link_up.if0` | 2,385 | 0.024 | 20 | 200 | fits | 24,119 | 43 (11) | 0.678 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 6,239 | 0.062 | 20 | 200 | fits | 17,701 | 23 (39) | 0.593 |
| GM_CHANGE | `adp.gm_change.if0` | 2,130 | 0.021 | 20 | 200 | fits | 12,585 | 17 (11) | 0.323 |
| LINK_UP | `adp.link_up.if0` | 2,385 | 0.024 | 20 | 200 | fits | 24,119 | 43 (11) | 0.678 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 6,239 | 0.062 | 20 | 200 | fits | 17,701 | 23 (39) | 0.593 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,984 | 0.050 | 20 | 200 | fits | 14,259 | 16 (31) | 0.517 |
| LINK_UP | `adp.link_up.if0` | 2,385 | 0.024 | 20 | 200 | fits | 24,119 | 43 (11) | 0.678 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 6,239 | 0.062 | 20 | 200 | fits | 17,701 | 23 (39) | 0.593 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,984 | 0.050 | 20 | 200 | fits | 14,259 | 16 (31) | 0.517 |
| set_name | `aecp_fanout.set_name.if0` | 55,290 | 0.553 | 20 | 24 | fits | 56,043 | 89 | 0.550 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 52,330 | 0.523 | 20 | 24 | fits | 51,041 | 78 | 0.581 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 37,445 | 0.374 | 20 | 24 | fits | 45,876 | 79 | 0.535 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 48,340 | 0.483 | 20 | 24 | fits | 44,710 | 78 | 0.505 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 51,061 | 0.511 | 20 | 24 | fits | 62,893 | 110 | 0.584 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 260,113 | 2.601 | 20 | 24 | fits | 60,774 | 109 | 0.572 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 335,617 | 3.356 | 20 | 24 | fits | 49,742 | 67 | 0.578 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 49,105 | 0.491 | 20 | 24 | fits | 45,479 | 78 | 0.515 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 38,938 | 0.389 | 20 | 24 | fits | 46,161 | 79 | 0.532 |
| BIND_RX | `acmp.bind_rx.if0` | 18,711 | 0.187 | 20 | 20 | fits | 38,357 | 26 (77) | 0.756 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,818 | 0.098 | 20 | 20 | fits | 28,014 | 19 (32) | 0.806 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,532 | 0.105 | 20 | 20 | fits | 22,056 | 15 (47) | 0.664 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 14,476 | 0.145 | 20 | 20 | fits | 36,683 | 18 (50) | 0.821 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,237 | 0.102 | 20 | 20 | fits | 22,637 | 17 (48) | 0.661 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,648 | 0.096 | 20 | 20 | fits | 21,582 | 16 (48) | 0.593 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,180 | 0.092 | 20 | 20 | fits | 20,759 | 16 (48) | 0.584 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,079 | 0.091 | 20 | 20 | fits | 20,549 | 16 (48) | 0.575 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 15,646 | 0.156 | 20 | 24 | fits | 25,663 | 20 | 0.743 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 26,508 | 0.265 | 20 | 24 | fits | 30,239 | 20 | 0.657 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 20,902 | 0.209 | 20 | 24 | fits | 27,024 | 20 | 0.678 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 22,598 | 0.226 | 20 | 24 | fits | 26,315 | 20 | 0.669 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 23,476 | 0.235 | 20 | 24 | fits | 27,219 | 20 | 0.676 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 20,563 | 0.206 | 20 | 24 | fits | 26,685 | 20 | 0.669 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 22,304 | 0.223 | 20 | 24 | fits | 25,705 | 20 | 0.671 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 20,154 | 0.202 | 20 | 24 | fits | 26,276 | 20 | 0.688 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 22,272 | 0.223 | 20 | 24 | fits | 25,594 | 20 | 0.686 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 22,455 | 0.225 | 20 | 24 | fits | 28,504 | 21 | 0.581 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 21,852 | 0.219 | 20 | 24 | fits | 25,329 | 20 | 0.707 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 21,982 | 0.220 | 20 | 24 | fits | 25,459 | 20 | 0.707 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 19,572 | 0.196 | 20 | 24 | fits | 25,618 | 20 | 0.671 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 23,261 | 0.233 | 20 | 24 | fits | 26,732 | 20 | 0.678 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 19,919 | 0.199 | 20 | 24 | fits | 26,049 | 20 | 0.688 |
| get_configuration | `aecp.get_configuration.if0` | 19,577 | 0.196 | 20 | 24 | fits | 22,895 | 20 | 0.698 |
| entity_available | `aecp.entity_available.if0` | 17,251 | 0.173 | 20 | 24 | fits | 23,225 | 20 | 0.691 |
| get_name | `aecp.get_name.if0` | 20,193 | 0.202 | 20 | 24 | fits | 26,417 | 20 | 0.711 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 24,861 | 0.249 | 20 | 24 | fits | 28,698 | 26 | 0.695 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 21,524 | 0.215 | 20 | 24 | fits | 27,585 | 29 | 0.706 |
| get_as_path, refused ENTITY_MISBEHAVING | `aecp.get_as_path.if0` | 24,007 | 0.240 | 20 | 24 | fits | 26,676 | 29 | 0.708 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 17,888 | 0.179 | 20 | 24 | fits | 23,923 | 20 | 0.710 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 12,824 | 0.128 | 20 | 24 | fits | 22,894 | 20 | 0.678 |
| set_name | `aecp.set_name.if0` | 29,472 | 0.295 | 20 | 24 | fits | 46,449 | 49 | 0.718 |
| lock_entity | `aecp.lock_entity.if0` | 23,448 | 0.234 | 20 | 24 | fits | 34,662 | 34 | 0.753 |
| unlock_entity | `aecp.unlock_entity.if0` | 15,081 | 0.151 | 20 | 24 | fits | 34,864 | 33 | 0.762 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 143,730 | 1.437 | 20 | 24 | fits | 145,571 | 137 | 0.312 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 269,038 | 2.690 | 20 | 24 | fits | 137,635 | 114 | 0.287 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 250,426 | 2.504 | 20 | 24 | fits | 45,542 | 18 | 0.658 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 375,832 | 3.758 | 20 | 24 | fits | 82,074 | 17 | 0.663 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 345,797 | 3.458 | 20 | 24 | fits | 91,871 | 17 | 0.661 |
| READ_DESCRIPTOR held for a token (#917) | `aecp.held.read_descriptor.if0` | 521,005 | 5.210 | 20 | 24 | fits | 30,031 | 17 | 0.686 |
| LINK_UP | `fixture.link_up.if0` | 2,385 | 0.024 | 20 | 200 | fits | 24,119 | 43 (11) | 0.678 |
| malformed MRPDU discard | `fixture.malformed.if0` | 17,992 | 0.180 | 20 | 20 | fits | 18,058 | 12 | 0.714 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 32,865 | 0.329 | 20 | 24 | fits | 45,055 | 43 | 0.757 |
| LINK_DOWN | `fixture.link_down.if0` | 2,244 | 0.022 | 20 | 200 | fits | 21,671 | 23 (9) | 0.733 |
| BIND_RX | `fixture.bind_rx.if0` | 18,762 | 0.188 | 20 | 20 | fits | 38,750 | 26 (77) | 0.764 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 23,956 | 0.240 | 20 | 20 | fits | 36,613 | 35 (35) | 0.760 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 6,789 | 0.068 | 20 | 20 | fits | 21,678 | 13 (29) | 0.720 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 81,659 | 0.817 | 20 | 200 | fits | 81,763 | 77 | 0.733 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 81,659 | 0.817 | 20 | 200 | fits | 81,763 | 77 | 0.733 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 81,385 | 0.814 | 20 | 20 | fits | 81,763 | 77 | 0.733 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 81,385 | 0.814 | 20 | 20 | fits | 81,763 | 77 | 0.733 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 81,593 | 0.816 | 20 | 24 | fits | 81,763 | 77 | 0.733 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 81,593 | 0.816 | 20 | 24 | fits | 81,763 | 77 | 0.733 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 81,527 | 0.815 | 20 | 50 | fits | 81,763 | 77 | 0.733 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 81,527 | 0.815 | 20 | 50 | fits | 81,763 | 77 | 0.733 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 81,461 | 0.815 | 20 | 20 | fits | 81,763 | 77 | 0.733 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 81,461 | 0.815 | 20 | 20 | fits | 81,763 | 77 | 0.733 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
