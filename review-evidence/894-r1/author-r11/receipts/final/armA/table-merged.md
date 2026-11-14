### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 92 paths and 7 of 950 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.191 (0.407) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.088 (0.223) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.074 (0.249) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.076 (0.396) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.106 (0.237) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.090 (0.223) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.098 (0.228) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.105 (0.247) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.094 (0.307) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.197 (0.537) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.163 (0.489) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.127 (0.527) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.181 (0.520) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.186 (0.605) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.153 (0.477) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.134 (0.385) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.049 (0.157) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.024 (0.156) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.026 (0.266) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.025 (0.258) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.058 (0.205) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.150 (0.441) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.165 (0.449) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.203 (0.495) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.220 (0.508) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.256 (0.550) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.245 (0.540) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.217 (0.597) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.166 (0.453) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.284 (0.580) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.188 (0.479) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.187 (0.477) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.098 (0.256) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.211 (0.500) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.099 (0.254) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.236 (0.528) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.106 (0.266) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.186 (0.477) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.248 (0.543) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.187 (0.478) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.249 (0.544) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.193 (0.483) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.106 (0.261) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.160 (0.452) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.266 (0.650) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.091 (0.248) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.237 (0.579) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.013 (2.297) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.470 (0.759) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.607 (0.895) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.507 (0.798) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.563 (0.823) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.548 (0.854) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 2.350 (2.653) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.530 (0.792) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 1.600 (1.891) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 1.396 (1.730) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 2.825 (3.156) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 2.457 (2.800) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.381 (1.683) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.287 (4.690) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-aged2-7.adp_available.if0` (backlog-adp@blank-aged2-7) | 4.520 (5.170) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.205 (0.544) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.692 (2.095) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.811 (62.958) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.497 (63.645) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.321 (0.456) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 3.044 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 1.523 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 2.975 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 1.882 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.813 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.171 (0.478) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.097 (0.203) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.105 (0.258) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.147 (0.478) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.150 (0.437) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-held.mrpdu.periodic.if0` (save-held) | 2.478 | fits | 0 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.191 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 61.986 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.234 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.adp.last.if0` (backlog-adp@blank-aged2-7) | 5.033 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.354 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.740 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.217 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.maap.last.if0` (backlog-adp@blank-aged2-7) | 5.071 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-6.service.srp.first.if0` (backlog-adp@program-aged2-6) | 5.930 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-5.service.srp.last.if0` (backlog-adp@verify-aged2-5) | 10.122 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.981 (1.094) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.449 (0.450) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.216 (0.216) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.879 (0.956) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.364 | 11 | 149,774 (1.498) | yes | - |
| backlog-adp@blank-1 | 0 | 10.419 | 10 | 149,664 (1.497) | yes | - |
| backlog-adp@blank-2 | 0 | 10.460 | 10 | 149,731 (1.497) | yes | - |
| backlog-adp@blank-3 | 0 | 10.459 | 10 | 149,664 (1.497) | yes | - |
| backlog-adp@blank-4 | 0 | 10.487 | 10 | 149,731 (1.497) | yes | - |
| backlog-adp@blank-5 | 0 | 10.725 | 12 | 149,895 (1.499) | yes | - |
| backlog-adp@blank-6 | 0 | 10.644 | 12 | 149,729 (1.497) | yes | - |
| backlog-adp@blank-7 | 0 | 10.394 | 9 | 144,460 (1.445) | yes | - |
| backlog-adp@program-0 | 0 | 10.680 | 11 | 149,755 (1.498) | yes | - |
| backlog-adp@program-1 | 0 | 11.007 | 12 | 149,688 (1.497) | yes | - |
| backlog-adp@program-2 | 0 | 10.471 | 10 | 148,628 (1.486) | yes | - |
| backlog-adp@program-3 | 0 | 10.579 | 10 | 149,616 (1.496) | yes | - |
| backlog-adp@program-4 | 0 | 9.786 | 11 | 149,728 (1.497) | yes | - |
| backlog-adp@program-5 | 0 | 10.057 | 12 | 149,691 (1.497) | yes | - |
| backlog-adp@program-6 | 0 | 9.758 | 10 | 149,598 (1.496) | yes | - |
| backlog-adp@program-7 | 0 | 9.783 | 10 | 149,598 (1.496) | yes | - |
| backlog-adp@verify-0 | 0 | 10.867 | 11 | 149,599 (1.496) | yes | - |
| backlog-adp@verify-1 | 0 | 10.499 | 10 | 149,547 (1.495) | yes | - |
| backlog-adp@verify-2 | 0 | 10.381 | 9 | 144,659 (1.447) | yes | - |
| backlog-adp@verify-3 | 0 | 10.388 | 10 | 149,480 (1.495) | yes | - |
| backlog-adp@verify-4 | 0 | 10.927 | 12 | 149,547 (1.495) | yes | - |
| backlog-adp@verify-5 | 0 | 10.686 | 12 | 149,599 (1.496) | yes | - |
| backlog-adp@verify-6 | 0 | 10.438 | 10 | 149,633 (1.496) | yes | - |
| backlog-adp@verify-7 | 0 | 10.464 | 10 | 149,566 (1.496) | yes | - |
| backlog-adp@blank-aged2-0 | 1 | 10.405 | 10 | 146,689 (1.467) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 10.890 | 11 | 146,268 (1.463) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 10.584 | 11 | 150,009 (1.500) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 10.444 | 10 | 149,340 (1.493) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 10.428 | 10 | 149,278 (1.493) | yes | - |
| backlog-adp@blank-aged2-5 | 1 | 10.389 | 9 | 147,165 (1.472) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 10.463 | 10 | 149,423 (1.494) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 10.429 | 10 | 149,423 (1.494) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 12.266 | 12 | 147,597 (1.476) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 11.303 | 12 | 149,567 (1.496) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 11.705 | 14 | 149,567 (1.496) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 11.630 | 14 | 149,567 (1.496) | yes | - |
| backlog-adp@blank-aged1-4 | 1 | 11.433 | 13 | 145,784 (1.458) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 11.306 | 12 | 149,270 (1.493) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 11.303 | 12 | 149,270 (1.493) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 12.325 | 12 | 149,419 (1.494) | yes | - |
| backlog-adp@program-aged2-0 | 1 | 10.809 | 11 | 144,791 (1.448) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 10.737 | 12 | 149,730 (1.497) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 10.470 | 10 | 149,549 (1.495) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 10.446 | 10 | 149,549 (1.495) | yes | - |
| backlog-adp@program-aged2-4 | 1 | 10.416 | 9 | 147,147 (1.471) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 10.487 | 10 | 149,560 (1.496) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 10.486 | 10 | 149,560 (1.496) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 10.573 | 11 | 149,661 (1.497) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 10.809 | 11 | 149,710 (1.497) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.895 | 12 | 149,710 (1.497) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 10.670 | 12 | 149,829 (1.498) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 10.419 | 9 | 147,659 (1.477) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 10.533 | 10 | 149,618 (1.496) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 10.475 | 10 | 149,618 (1.496) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 10.445 | 10 | 149,618 (1.496) | yes | - |
| backlog-adp@program-aged1-7 | 1 | 10.402 | 9 | 147,370 (1.474) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.420 | 10 | 147,659 (1.477) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 10.370 | 10 | 149,551 (1.496) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 10.476 | 10 | 149,551 (1.496) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 10.406 | 10 | 149,551 (1.496) | yes | - |
| backlog-adp@verify-aged2-4 | 1 | 11.033 | 11 | 147,370 (1.474) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 10.602 | 11 | 149,688 (1.497) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 10.582 | 11 | 148,078 (1.481) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 10.433 | 10 | 149,560 (1.496) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 11.576 | 12 | 149,856 (1.499) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 10.675 | 12 | 149,766 (1.498) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 10.379 | 10 | 149,627 (1.496) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 10.368 | 9 | 147,636 (1.476) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 10.471 | 10 | 149,482 (1.495) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 10.393 | 10 | 149,482 (1.495) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 10.397 | 10 | 149,482 (1.495) | yes | - |
| backlog-adp@verify-aged1-7 | 1 | 10.603 | 11 | 146,235 (1.462) | yes | - |
| backlog | 0 | 5.800 | 7 | 155,697 (1.557) | yes | - |
| backlog-adp | 0 | 9.611 | 10 | 149,687 (1.497) | yes | - |
| backlog-adp-refill | 0 | 40.812 | 24 | 149,687 (1.497) | yes | - |
| backlog-owed | 0 | 64.080 | 25 | 149,023 (1.490) | yes | - |
| fixture | 0 | 1.260 | 2 | 82,191 (0.822) | yes | - |

Composed maximum over the 4 backlog windows: 155,697 CPU cycles (1.557 ms), backlog.
Over the windows that released their whole load only: 155,697 (1.557 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3610 | 0 | 42,084 (0.421) | fits |
| save-second | 49912 | 0 | 49,142 (0.491) | fits |
| backlog-adp@blank-0 | 407 | 0 | 149,774 (1.498) | fits |
| backlog-adp@blank-1 | 406 | 0 | 149,664 (1.497) | fits |
| backlog-adp@blank-2 | 406 | 0 | 149,731 (1.497) | fits |
| backlog-adp@blank-3 | 406 | 0 | 149,664 (1.497) | fits |
| backlog-adp@blank-4 | 406 | 0 | 149,731 (1.497) | fits |
| backlog-adp@blank-5 | 408 | 0 | 149,895 (1.499) | fits |
| backlog-adp@blank-6 | 408 | 0 | 149,729 (1.497) | fits |
| backlog-adp@blank-7 | 408 | 0 | 149,495 (1.495) | fits |
| backlog-adp@program-0 | 503 | 0 | 149,755 (1.498) | fits |
| backlog-adp@program-1 | 504 | 0 | 149,688 (1.497) | fits |
| backlog-adp@program-2 | 504 | 0 | 148,628 (1.486) | fits |
| backlog-adp@program-3 | 504 | 0 | 149,616 (1.496) | fits |
| backlog-adp@program-4 | 506 | 0 | 149,728 (1.497) | fits |
| backlog-adp@program-5 | 507 | 0 | 149,691 (1.497) | fits |
| backlog-adp@program-6 | 507 | 0 | 149,598 (1.496) | fits |
| backlog-adp@program-7 | 507 | 0 | 149,598 (1.496) | fits |
| backlog-adp@verify-0 | 591 | 0 | 149,599 (1.496) | fits |
| backlog-adp@verify-1 | 590 | 0 | 149,547 (1.495) | fits |
| backlog-adp@verify-2 | 590 | 0 | 149,547 (1.495) | fits |
| backlog-adp@verify-3 | 590 | 0 | 149,480 (1.495) | fits |
| backlog-adp@verify-4 | 592 | 0 | 149,547 (1.495) | fits |
| backlog-adp@verify-5 | 592 | 0 | 149,599 (1.496) | fits |
| backlog-adp@verify-6 | 592 | 0 | 149,633 (1.496) | fits |
| backlog-adp@verify-7 | 592 | 0 | 149,566 (1.496) | fits |
| backlog-adp@blank-aged2-0 | 726 | 0 | 154,639 (1.546) | fits |
| backlog-adp@blank-aged2-1 | 732 | 0 | 150,035 (1.500) | fits |
| backlog-adp@blank-aged2-2 | 740 | 0 | 150,009 (1.500) | fits |
| backlog-adp@blank-aged2-3 | 747 | 0 | 149,340 (1.493) | fits |
| backlog-adp@blank-aged2-4 | 755 | 0 | 149,278 (1.493) | fits |
| backlog-adp@blank-aged2-5 | 763 | 0 | 149,278 (1.493) | fits |
| backlog-adp@blank-aged2-6 | 772 | 0 | 149,423 (1.494) | fits |
| backlog-adp@blank-aged2-7 | 780 | 0 | 149,423 (1.494) | fits |
| backlog-adp@blank-aged1-0 | 663 | 0 | 149,578 (1.496) | fits |
| backlog-adp@blank-aged1-1 | 671 | 0 | 149,567 (1.496) | fits |
| backlog-adp@blank-aged1-2 | 681 | 0 | 149,567 (1.496) | fits |
| backlog-adp@blank-aged1-3 | 689 | 0 | 149,567 (1.496) | fits |
| backlog-adp@blank-aged1-4 | 697 | 0 | 149,558 (1.496) | fits |
| backlog-adp@blank-aged1-5 | 704 | 0 | 149,270 (1.493) | fits |
| backlog-adp@blank-aged1-6 | 712 | 0 | 149,270 (1.493) | fits |
| backlog-adp@blank-aged1-7 | 720 | 0 | 149,419 (1.494) | fits |
| backlog-adp@program-aged2-0 | 818 | 0 | 149,971 (1.500) | fits |
| backlog-adp@program-aged2-1 | 827 | 0 | 149,730 (1.497) | fits |
| backlog-adp@program-aged2-2 | 833 | 0 | 149,549 (1.495) | fits |
| backlog-adp@program-aged2-3 | 841 | 0 | 149,549 (1.495) | fits |
| backlog-adp@program-aged2-4 | 849 | 0 | 149,549 (1.495) | fits |
| backlog-adp@program-aged2-5 | 858 | 0 | 149,560 (1.496) | fits |
| backlog-adp@program-aged2-6 | 866 | 0 | 149,560 (1.496) | fits |
| backlog-adp@program-aged2-7 | 875 | 0 | 149,661 (1.497) | fits |
| backlog-adp@program-aged1-0 | 752 | 0 | 149,710 (1.497) | fits |
| backlog-adp@program-aged1-1 | 761 | 0 | 149,710 (1.497) | fits |
| backlog-adp@program-aged1-2 | 769 | 0 | 149,829 (1.498) | fits |
| backlog-adp@program-aged1-3 | 775 | 0 | 149,535 (1.495) | fits |
| backlog-adp@program-aged1-4 | 784 | 0 | 149,618 (1.496) | fits |
| backlog-adp@program-aged1-5 | 792 | 0 | 149,618 (1.496) | fits |
| backlog-adp@program-aged1-6 | 800 | 0 | 149,618 (1.496) | fits |
| backlog-adp@program-aged1-7 | 808 | 0 | 149,618 (1.496) | fits |
| backlog-adp@verify-aged2-0 | 907 | 0 | 149,540 (1.495) | fits |
| backlog-adp@verify-aged2-1 | 915 | 0 | 149,551 (1.496) | fits |
| backlog-adp@verify-aged2-2 | 923 | 0 | 149,551 (1.496) | fits |
| backlog-adp@verify-aged2-3 | 931 | 0 | 149,551 (1.496) | fits |
| backlog-adp@verify-aged2-4 | 941 | 0 | 149,551 (1.496) | fits |
| backlog-adp@verify-aged2-5 | 949 | 0 | 149,688 (1.497) | fits |
| backlog-adp@verify-aged2-6 | 957 | 0 | 148,078 (1.481) | fits |
| backlog-adp@verify-aged2-7 | 964 | 0 | 149,560 (1.496) | fits |
| backlog-adp@verify-aged1-0 | 843 | 0 | 149,856 (1.499) | fits |
| backlog-adp@verify-aged1-1 | 851 | 0 | 149,766 (1.498) | fits |
| backlog-adp@verify-aged1-2 | 857 | 0 | 149,627 (1.496) | fits |
| backlog-adp@verify-aged1-3 | 865 | 0 | 149,627 (1.496) | fits |
| backlog-adp@verify-aged1-4 | 874 | 0 | 149,482 (1.495) | fits |
| backlog-adp@verify-aged1-5 | 882 | 0 | 149,482 (1.495) | fits |
| backlog-adp@verify-aged1-6 | 890 | 0 | 149,482 (1.495) | fits |
| backlog-adp@verify-aged1-7 | 900 | 0 | 149,583 (1.496) | fits |
| adp-advertise | 599 | 0 | 41,610 (0.416) | fits |
| save-held | 1409 | 0 | 153,247 (1.532) | fits |
| save-starved | 26664 | 0 | 153,247 (1.532) | fits |
| acmp-noresp | 2027 | 0 | 41,610 (0.416) | fits |
| save | 610 | 0 | 44,302 (0.443) | fits |
| srp | 290 | 0 | 68,972 (0.690) | fits |
| backlog | 286 | 0 | 155,697 (1.557) | fits |
| backlog-adp | 312 | 0 | 149,687 (1.497) | fits |
| backlog-adp-refill | 326 | 0 | 149,687 (1.497) | fits |
| backlog-owed | 310 | 0 | 149,023 (1.490) | fits |
| acmp-disc | 938 | 0 | 41,610 (0.416) | fits |
| maap | 176 | 0 | 41,610 (0.416) | fits |
| adp-link | 90 | 0 | 45,332 (0.453) | fits |
| adp-gm | 89 | 0 | 41,610 (0.416) | fits |
| adp-discover | 89 | 0 | 41,610 (0.416) | fits |
| control | 89 | 0 | 41,610 (0.416) | fits |
| aecp-fanout | 112 | 0 | 61,692 (0.617) | fits |
| acmp-cmd | 87 | 0 | 41,610 (0.416) | fits |
| aecp | 112 | 0 | 43,260 (0.433) | fits |
| aecp-largest-notice | 106 | 0 | 144,997 (1.450) | fits |
| datapath-events | 118 | 0 | 41,610 (0.416) | fits |
| fixture | 161 | 0 | 82,191 (0.822) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | +9.336 ms, 76,470 (0.765 ms), read-back | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 9.100 (20) | 10.900 |
| backlog-adp@blank-aged2-1 | 2 | none | +9.160 ms, 76,566 (0.766 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 9.122 (20) | 10.878 |
| backlog-adp@blank-aged2-2 | 2 | +8.468 ms, 76,566 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 9.994 (20) | 10.006 |
| backlog-adp@blank-aged2-3 | 2 | +6.605 ms, 76,566 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 9.964 (20) | 10.036 |
| backlog-adp@blank-aged2-4 | 2 | +5.719 ms, 76,566 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 9.948 (20) | 10.052 |
| backlog-adp@blank-aged2-5 | 2 | +4.923 ms, 76,797 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 9.910 (20) | 10.090 |
| backlog-adp@blank-aged2-6 | 2 | none | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 9.980 (20) | 10.020 |
| backlog-adp@blank-aged2-7 | 2 | none | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 9.948 (20) | 10.052 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 9.074 (20) | 10.926 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 9.324 (20) | 10.676 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 9.703 (20) | 10.297 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 9.975 (20) | 10.025 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 9.925 (20) | 10.075 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 10.072 (20) | 9.928 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 10.070 (20) | 9.930 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 10.016 (20) | 9.984 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 9.016 (20) | 10.984 |
| backlog-adp@program-aged2-1 | 2 | none | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 9.195 (20) | 10.805 |
| backlog-adp@program-aged2-2 | 2 | +8.462 ms, 80,258 (0.803 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 9.990 (20) | 10.010 |
| backlog-adp@program-aged2-3 | 2 | +6.714 ms, 80,258 (0.803 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 9.965 (20) | 10.035 |
| backlog-adp@program-aged2-4 | 2 | +5.821 ms, 80,258 (0.803 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 9.935 (20) | 10.065 |
| backlog-adp@program-aged2-5 | 2 | +5.139 ms, 80,489 (0.805 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 10.005 (20) | 9.995 |
| backlog-adp@program-aged2-6 | 2 | +4.334 ms, 80,000 (0.800 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 10.003 (20) | 9.997 |
| backlog-adp@program-aged2-7 | 2 | +3.045 ms, 80,095 (0.801 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 10.092 (20) | 9.908 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 9.152 (20) | 10.848 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 9.202 (20) | 10.798 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 9.121 (20) | 10.879 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 9.137 (20) | 10.863 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 9.251 (20) | 10.749 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 9.196 (20) | 10.804 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 9.160 (20) | 10.840 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 9.117 (20) | 10.883 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 9.099 (20) | 10.901 |
| backlog-adp@verify-aged2-1 | 2 | none | +9.289 ms, 77,277 (0.773 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 9.252 (20) | 10.748 |
| backlog-adp@verify-aged2-2 | 2 | +8.394 ms, 77,277 (0.773 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 9.995 (20) | 10.005 |
| backlog-adp@verify-aged2-3 | 2 | +6.709 ms, 77,277 (0.773 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 9.924 (20) | 10.076 |
| backlog-adp@verify-aged2-4 | 2 | +5.817 ms, 77,277 (0.773 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 9.894 (20) | 10.106 |
| backlog-adp@verify-aged2-5 | 2 | +4.330 ms, 77,211 (0.772 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 10.122 (20) | 9.878 |
| backlog-adp@verify-aged2-6 | 2 | +4.308 ms, 77,211 (0.772 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 10.102 (20) | 9.898 |
| backlog-adp@verify-aged2-7 | 2 | +2.962 ms, 77,117 (0.771 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 9.954 (20) | 10.046 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 9.109 (20) | 10.891 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 9.155 (20) | 10.845 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 9.139 (20) | 10.861 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 9.128 (20) | 10.872 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 9.232 (20) | 10.768 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 9.150 (20) | 10.850 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 9.152 (20) | 10.848 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 9.090 (20) | 10.910 |

Least margin over the aged windows: 9.878 ms, `backlog-adp@verify-aged2-5.service.srp.last.if0` at 10.122 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.259 | 6,070 | 102 | 2 | 30.838 | yes | within |
| save-held | 2018.230 | 4,070 | 102 | - | 15.559 | no | within |
| save-starved | 4048.152 | 4,070 | 102 | - | 31.128 | yes | within |
| save | 2018.611 | 4,070 | 102 | - | 10.911 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 95,411 (0.954) | 77,763 (0.778) |
| save-second | 520 | 79,676 (0.797) | 77,571 (0.776) |
| backlog-adp@blank-0 | 299 | 90,117 (0.901) | 75,823 (0.758) |
| backlog-adp@blank-1 | 299 | 91,135 (0.911) | 75,918 (0.759) |
| backlog-adp@blank-2 | 299 | 90,993 (0.910) | 75,918 (0.759) |
| backlog-adp@blank-3 | 299 | 90,916 (0.909) | 75,918 (0.759) |
| backlog-adp@blank-4 | 299 | 91,019 (0.910) | 75,918 (0.759) |
| backlog-adp@blank-5 | 299 | 91,095 (0.911) | 75,994 (0.760) |
| backlog-adp@blank-6 | 299 | 91,287 (0.913) | 75,847 (0.758) |
| backlog-adp@blank-7 | 299 | 90,850 (0.908) | 75,934 (0.759) |
| backlog-adp@program-0 | 328 | 95,261 (0.953) | 78,440 (0.784) |
| backlog-adp@program-1 | 328 | 95,261 (0.953) | 78,535 (0.785) |
| backlog-adp@program-2 | 328 | 95,261 (0.953) | 78,586 (0.786) |
| backlog-adp@program-3 | 328 | 95,261 (0.953) | 78,599 (0.786) |
| backlog-adp@program-4 | 329 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@program-5 | 329 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@program-6 | 329 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@program-7 | 329 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-0 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-1 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-2 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-3 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-4 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-5 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-6 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-7 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@blank-aged2-0 | 297 | 76,470 (0.765) | 75,392 (0.754) |
| backlog-adp@blank-aged2-1 | 297 | 76,566 (0.766) | 75,487 (0.755) |
| backlog-adp@blank-aged2-2 | 297 | 76,566 (0.766) | 75,487 (0.755) |
| backlog-adp@blank-aged2-3 | 297 | 76,566 (0.766) | 75,487 (0.755) |
| backlog-adp@blank-aged2-4 | 297 | 76,566 (0.766) | 75,487 (0.755) |
| backlog-adp@blank-aged2-5 | 297 | 76,797 (0.768) | 75,628 (0.756) |
| backlog-adp@blank-aged2-6 | 297 | 84,102 (0.841) | 75,584 (0.756) |
| backlog-adp@blank-aged2-7 | 297 | 84,243 (0.842) | 75,536 (0.755) |
| backlog-adp@blank-aged1-0 | 298 | 95,454 (0.955) | 75,935 (0.759) |
| backlog-adp@blank-aged1-1 | 297 | 96,054 (0.961) | 75,963 (0.760) |
| backlog-adp@blank-aged1-2 | 297 | 97,094 (0.971) | 76,037 (0.760) |
| backlog-adp@blank-aged1-3 | 297 | 91,224 (0.912) | 75,884 (0.759) |
| backlog-adp@blank-aged1-4 | 297 | 89,798 (0.898) | 75,816 (0.758) |
| backlog-adp@blank-aged1-5 | 297 | 90,959 (0.910) | 75,935 (0.759) |
| backlog-adp@blank-aged1-6 | 297 | 90,801 (0.908) | 75,935 (0.759) |
| backlog-adp@blank-aged1-7 | 298 | 90,838 (0.908) | 76,025 (0.760) |
| backlog-adp@program-aged2-0 | 327 | 95,261 (0.953) | 78,822 (0.788) |
| backlog-adp@program-aged2-1 | 326 | 95,261 (0.953) | 78,450 (0.784) |
| backlog-adp@program-aged2-2 | 326 | 95,261 (0.953) | 78,279 (0.783) |
| backlog-adp@program-aged2-3 | 326 | 95,261 (0.953) | 78,279 (0.783) |
| backlog-adp@program-aged2-4 | 326 | 95,261 (0.953) | 78,279 (0.783) |
| backlog-adp@program-aged2-5 | 326 | 95,261 (0.953) | 78,420 (0.784) |
| backlog-adp@program-aged2-6 | 326 | 95,261 (0.953) | 78,121 (0.781) |
| backlog-adp@program-aged2-7 | 326 | 95,261 (0.953) | 78,089 (0.781) |
| backlog-adp@program-aged1-0 | 327 | 95,261 (0.953) | 78,689 (0.787) |
| backlog-adp@program-aged1-1 | 326 | 95,261 (0.953) | 78,535 (0.785) |
| backlog-adp@program-aged1-2 | 326 | 95,261 (0.953) | 78,454 (0.785) |
| backlog-adp@program-aged1-3 | 326 | 95,261 (0.953) | 78,586 (0.786) |
| backlog-adp@program-aged1-4 | 326 | 95,261 (0.953) | 78,586 (0.786) |
| backlog-adp@program-aged1-5 | 326 | 95,261 (0.953) | 78,586 (0.786) |
| backlog-adp@program-aged1-6 | 326 | 95,261 (0.953) | 78,676 (0.787) |
| backlog-adp@program-aged1-7 | 326 | 95,261 (0.953) | 78,809 (0.788) |
| backlog-adp@verify-aged2-0 | 356 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-aged2-1 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-aged2-2 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-aged2-3 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-aged2-4 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-aged2-5 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-aged2-6 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-aged2-7 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-aged1-0 | 356 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-aged1-1 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-aged1-2 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-aged1-3 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-aged1-4 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-aged1-5 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-aged1-6 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| backlog-adp@verify-aged1-7 | 355 | 95,261 (0.953) | 77,835 (0.778) |
| adp-advertise | 578 | 20,701 (0.207) | 1,900 (0.019) |
| save-held | 722 | 94,360 (0.944) | 78,515 (0.785) |
| save-starved | 418 | 80,590 (0.806) | 77,991 (0.780) |
| acmp-noresp | 615 | 95,097 (0.951) | 77,763 (0.778) |
| save | 585 | 94,311 (0.943) | 77,744 (0.777) |
| srp | 271 | 20,701 (0.207) | 1,978 (0.020) |
| backlog | 265 | 20,701 (0.207) | 1,900 (0.019) |
| backlog-adp | 271 | 20,701 (0.207) | 2,163 (0.022) |
| backlog-adp-refill | 274 | 20,701 (0.207) | 2,163 (0.022) |
| backlog-owed | 276 | 20,701 (0.207) | 2,213 (0.022) |
| acmp-disc | 305 | 95,229 (0.952) | 77,763 (0.778) |
| maap | 163 | 20,701 (0.207) | 1,900 (0.019) |
| adp-link | 80 | 20,701 (0.207) | 1,900 (0.019) |
| adp-gm | 80 | 20,701 (0.207) | 1,900 (0.019) |
| adp-discover | 80 | 20,701 (0.207) | 1,900 (0.019) |
| control | 80 | 20,701 (0.207) | 1,900 (0.019) |
| aecp-fanout | 80 | 20,701 (0.207) | 1,900 (0.019) |
| acmp-cmd | 65 | 20,701 (0.207) | 1,900 (0.019) |
| aecp | 79 | 20,701 (0.207) | 1,900 (0.019) |
| aecp-largest-notice | 78 | 20,701 (0.207) | 1,900 (0.019) |
| datapath-events | 70 | 20,701 (0.207) | 1,900 (0.019) |
| fixture | 54 | 15,454 (0.155) | 1,900 (0.019) |

Longest pass that carries a step: 97,094 CPU cycles (0.971 ms), backlog-adp@blank-aged1-2; longest step: 78,822 (0.788 ms), backlog-adp@program-aged2-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 18,617 | 0.186 | 20 | 20 | fits | 32,648 | 19 (14) | 0.880 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 428,830 | 4.288 | 20 | 20 | fits | 111,120 | 163 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 376,596 | 3.766 | 20 | 200 | fits | 145,793 | 226 | 0.376 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 487,100 | 4.871 | 20 | 200 | fits | 111,120 | 163 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 377,520 | 3.775 | 20 | 20 | fits | 145,793 | 226 | 0.376 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 487,804 | 4.878 | 20 | 20 | fits | 111,120 | 163 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 235,367 | 2.354 | 20 | 24 | fits | 149,774 | 155 | 0.334 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 380,170 | 3.802 | 20 | 24 | fits | 145,793 | 226 | 0.376 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 380,104 | 3.801 | 20 | 50 | fits | 145,793 | 226 | 0.376 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 490,828 | 4.908 | 20 | 50 | fits | 111,120 | 163 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 571,789 | 5.718 | 20 | 20 | fits | 81,027 | 24 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 994,761 | 9.948 | 20 | 20 | fits | 75,754 | 28 | 0.568 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 354,787 | 3.548 | 20 | 20 | fits | 111,775 | 166 | 0.405 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 293,262 | 2.933 | 20 | 200 | fits | 144,665 | 222 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 404,421 | 4.044 | 20 | 200 | fits | 111,775 | 166 | 0.405 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 294,186 | 2.942 | 20 | 20 | fits | 144,665 | 222 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 405,125 | 4.051 | 20 | 20 | fits | 111,775 | 166 | 0.405 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 153,161 | 1.532 | 20 | 24 | fits | 149,664 | 155 | 0.333 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 296,836 | 2.968 | 20 | 24 | fits | 144,665 | 222 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 296,770 | 2.968 | 20 | 50 | fits | 144,665 | 222 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 408,149 | 4.081 | 20 | 50 | fits | 111,775 | 166 | 0.405 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 489,086 | 4.891 | 20 | 20 | fits | 81,003 | 24 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 918,233 | 9.182 | 20 | 20 | fits | 81,616 | 34 | 0.609 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 357,423 | 3.574 | 20 | 20 | fits | 110,972 | 163 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 297,755 | 2.978 | 20 | 200 | fits | 146,282 | 226 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 408,111 | 4.081 | 20 | 200 | fits | 110,972 | 163 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 298,679 | 2.987 | 20 | 20 | fits | 146,282 | 226 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 408,815 | 4.088 | 20 | 20 | fits | 110,972 | 163 | 0.418 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 156,037 | 1.560 | 20 | 24 | fits | 149,731 | 155 | 0.334 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 301,329 | 3.013 | 20 | 24 | fits | 146,282 | 226 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 301,263 | 3.013 | 20 | 50 | fits | 146,282 | 226 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 411,839 | 4.118 | 20 | 50 | fits | 110,972 | 163 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 492,857 | 4.929 | 20 | 20 | fits | 81,084 | 24 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 922,361 | 9.224 | 20 | 20 | fits | 86,456 | 32 | 0.531 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 352,824 | 3.528 | 20 | 20 | fits | 111,432 | 164 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 300,509 | 3.005 | 20 | 200 | fits | 146,294 | 226 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 411,325 | 4.113 | 20 | 200 | fits | 111,432 | 164 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 301,433 | 3.014 | 20 | 20 | fits | 146,294 | 226 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 412,029 | 4.120 | 20 | 20 | fits | 111,432 | 164 | 0.421 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 158,779 | 1.588 | 20 | 24 | fits | 149,664 | 155 | 0.333 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 304,083 | 3.041 | 20 | 24 | fits | 146,294 | 226 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 304,017 | 3.040 | 20 | 50 | fits | 146,294 | 226 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 415,053 | 4.151 | 20 | 50 | fits | 111,432 | 164 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 508,052 | 5.081 | 20 | 20 | fits | 84,856 | 31 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 922,386 | 9.224 | 20 | 20 | fits | 75,478 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 366,745 | 3.667 | 20 | 20 | fits | 114,625 | 170 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 303,073 | 3.031 | 20 | 200 | fits | 145,982 | 227 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 425,535 | 4.255 | 20 | 200 | fits | 114,625 | 170 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 303,997 | 3.040 | 20 | 20 | fits | 145,982 | 227 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 426,239 | 4.262 | 20 | 20 | fits | 114,625 | 170 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 161,655 | 1.617 | 20 | 24 | fits | 149,731 | 155 | 0.334 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 306,647 | 3.066 | 20 | 24 | fits | 145,982 | 227 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 306,581 | 3.066 | 20 | 50 | fits | 145,982 | 227 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 429,263 | 4.293 | 20 | 50 | fits | 114,625 | 170 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 510,451 | 5.105 | 20 | 20 | fits | 81,254 | 24 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 925,174 | 9.252 | 20 | 20 | fits | 75,478 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 360,080 | 3.601 | 20 | 20 | fits | 111,686 | 166 | 0.404 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 298,639 | 2.986 | 20 | 200 | fits | 145,210 | 227 | 0.378 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 409,709 | 4.097 | 20 | 200 | fits | 111,686 | 166 | 0.404 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 299,563 | 2.996 | 20 | 20 | fits | 145,210 | 227 | 0.378 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 410,413 | 4.104 | 20 | 20 | fits | 111,686 | 166 | 0.404 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 150,427 | 1.504 | 20 | 24 | fits | 149,895 | 156 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 302,213 | 3.022 | 20 | 24 | fits | 145,210 | 227 | 0.378 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 302,147 | 3.021 | 20 | 50 | fits | 145,210 | 227 | 0.378 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 413,437 | 4.134 | 20 | 50 | fits | 111,686 | 166 | 0.404 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 500,665 | 5.007 | 20 | 20 | fits | 87,294 | 30 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 907,958 | 9.080 | 20 | 20 | fits | 64,371 | 24 | 0.599 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 370,490 | 3.705 | 20 | 20 | fits | 119,062 | 169 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 302,876 | 3.029 | 20 | 200 | fits | 146,804 | 231 | 0.374 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 421,322 | 4.213 | 20 | 200 | fits | 119,062 | 169 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 303,800 | 3.038 | 20 | 20 | fits | 146,804 | 231 | 0.374 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 422,026 | 4.220 | 20 | 20 | fits | 119,062 | 169 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 153,070 | 1.531 | 20 | 24 | fits | 149,729 | 156 | 0.334 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 306,450 | 3.064 | 20 | 24 | fits | 146,804 | 231 | 0.374 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 306,384 | 3.064 | 20 | 50 | fits | 146,804 | 231 | 0.374 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 425,050 | 4.250 | 20 | 50 | fits | 119,062 | 169 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 506,009 | 5.060 | 20 | 20 | fits | 81,025 | 24 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 913,001 | 9.130 | 20 | 20 | fits | 64,307 | 24 | 0.599 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 350,384 | 3.504 | 20 | 20 | fits | 120,586 | 175 | 0.407 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 288,492 | 2.885 | 20 | 200 | fits | 144,460 | 220 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 408,462 | 4.085 | 20 | 200 | fits | 120,586 | 175 | 0.407 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 289,416 | 2.894 | 20 | 20 | fits | 144,460 | 220 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 409,166 | 4.092 | 20 | 20 | fits | 120,586 | 175 | 0.407 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 148,596 | 1.486 | 20 | 24 | fits | 149,495 | 155 | 0.332 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 292,066 | 2.921 | 20 | 24 | fits | 144,460 | 220 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 292,000 | 2.920 | 20 | 50 | fits | 144,460 | 220 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 412,190 | 4.122 | 20 | 50 | fits | 120,586 | 175 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 493,081 | 4.931 | 20 | 20 | fits | 80,957 | 24 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 915,841 | 9.158 | 20 | 20 | fits | 75,698 | 28 | 0.568 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 363,868 | 3.639 | 20 | 20 | fits | 111,805 | 166 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 302,389 | 3.024 | 20 | 200 | fits | 144,738 | 222 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 413,578 | 4.136 | 20 | 200 | fits | 111,805 | 166 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 303,313 | 3.033 | 20 | 20 | fits | 144,738 | 222 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 414,282 | 4.143 | 20 | 20 | fits | 111,805 | 166 | 0.406 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 162,215 | 1.622 | 20 | 24 | fits | 149,755 | 155 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 305,963 | 3.060 | 20 | 24 | fits | 144,738 | 222 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 305,897 | 3.059 | 20 | 50 | fits | 144,738 | 222 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 417,306 | 4.173 | 20 | 50 | fits | 111,805 | 166 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 498,060 | 4.981 | 20 | 20 | fits | 80,820 | 25 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 920,979 | 9.210 | 20 | 20 | fits | 75,478 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 358,549 | 3.585 | 20 | 20 | fits | 114,514 | 170 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 295,056 | 2.951 | 20 | 200 | fits | 146,055 | 227 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 417,339 | 4.173 | 20 | 200 | fits | 114,514 | 170 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 295,980 | 2.960 | 20 | 20 | fits | 146,055 | 227 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 418,043 | 4.180 | 20 | 20 | fits | 114,514 | 170 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 153,565 | 1.536 | 20 | 24 | fits | 149,688 | 155 | 0.334 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 298,630 | 2.986 | 20 | 24 | fits | 146,055 | 227 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 298,564 | 2.986 | 20 | 50 | fits | 146,055 | 227 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 421,067 | 4.211 | 20 | 50 | fits | 114,514 | 170 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 501,910 | 5.019 | 20 | 20 | fits | 80,909 | 24 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 916,611 | 9.166 | 20 | 20 | fits | 75,478 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 354,513 | 3.545 | 20 | 20 | fits | 110,845 | 163 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 294,891 | 2.949 | 20 | 200 | fits | 146,242 | 226 | 0.378 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 405,120 | 4.051 | 20 | 200 | fits | 110,845 | 163 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 295,815 | 2.958 | 20 | 20 | fits | 146,242 | 226 | 0.378 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 405,824 | 4.058 | 20 | 20 | fits | 110,845 | 163 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 153,213 | 1.532 | 20 | 24 | fits | 148,628 | 156 | 0.328 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 298,465 | 2.985 | 20 | 24 | fits | 146,242 | 226 | 0.378 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 298,399 | 2.984 | 20 | 50 | fits | 146,242 | 226 | 0.378 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 408,848 | 4.088 | 20 | 50 | fits | 110,845 | 163 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 495,904 | 4.959 | 20 | 20 | fits | 87,122 | 30 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 918,460 | 9.185 | 20 | 20 | fits | 69,564 | 31 | 0.675 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 363,694 | 3.637 | 20 | 20 | fits | 120,548 | 175 | 0.405 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 301,848 | 3.018 | 20 | 200 | fits | 144,728 | 220 | 0.393 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 421,780 | 4.218 | 20 | 200 | fits | 120,548 | 175 | 0.405 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 302,772 | 3.028 | 20 | 20 | fits | 144,728 | 220 | 0.393 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 422,484 | 4.225 | 20 | 20 | fits | 120,548 | 175 | 0.405 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 161,684 | 1.617 | 20 | 24 | fits | 149,616 | 155 | 0.333 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 305,422 | 3.054 | 20 | 24 | fits | 144,728 | 220 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 305,356 | 3.054 | 20 | 50 | fits | 144,728 | 220 | 0.393 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 425,508 | 4.255 | 20 | 50 | fits | 120,548 | 175 | 0.405 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 506,000 | 5.060 | 20 | 20 | fits | 80,558 | 24 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 929,080 | 9.291 | 20 | 20 | fits | 75,478 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 355,609 | 3.556 | 20 | 20 | fits | 114,534 | 170 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 292,095 | 2.921 | 20 | 200 | fits | 146,533 | 227 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 414,442 | 4.144 | 20 | 200 | fits | 114,534 | 170 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 293,019 | 2.930 | 20 | 20 | fits | 146,533 | 227 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 415,146 | 4.151 | 20 | 20 | fits | 114,534 | 170 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 150,126 | 1.501 | 20 | 24 | fits | 149,728 | 155 | 0.332 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 295,669 | 2.957 | 20 | 24 | fits | 146,533 | 227 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 295,603 | 2.956 | 20 | 50 | fits | 146,533 | 227 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 418,170 | 4.182 | 20 | 50 | fits | 114,534 | 170 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 499,070 | 4.991 | 20 | 20 | fits | 80,966 | 24 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 906,203 | 9.062 | 20 | 20 | fits | 64,371 | 24 | 0.599 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 358,231 | 3.582 | 20 | 20 | fits | 110,328 | 163 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 306,296 | 3.063 | 20 | 200 | fits | 146,303 | 231 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 416,008 | 4.160 | 20 | 200 | fits | 110,328 | 163 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 307,220 | 3.072 | 20 | 20 | fits | 146,303 | 231 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 416,712 | 4.167 | 20 | 20 | fits | 110,328 | 163 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 157,046 | 1.570 | 20 | 24 | fits | 149,691 | 156 | 0.334 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 309,870 | 3.099 | 20 | 24 | fits | 146,303 | 231 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 309,804 | 3.098 | 20 | 50 | fits | 146,303 | 231 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 419,736 | 4.197 | 20 | 50 | fits | 110,328 | 163 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 500,442 | 5.004 | 20 | 20 | fits | 80,772 | 24 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 915,041 | 9.150 | 20 | 20 | fits | 75,478 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 349,586 | 3.496 | 20 | 20 | fits | 111,248 | 163 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 297,317 | 2.973 | 20 | 200 | fits | 146,311 | 226 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 407,949 | 4.079 | 20 | 200 | fits | 111,248 | 163 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 298,241 | 2.982 | 20 | 20 | fits | 146,311 | 226 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 408,653 | 4.087 | 20 | 20 | fits | 111,248 | 163 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 155,570 | 1.556 | 20 | 24 | fits | 149,598 | 155 | 0.333 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 300,891 | 3.009 | 20 | 24 | fits | 146,311 | 226 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 300,825 | 3.008 | 20 | 50 | fits | 146,311 | 226 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 411,677 | 4.117 | 20 | 50 | fits | 111,248 | 163 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 498,695 | 4.987 | 20 | 20 | fits | 87,084 | 30 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 922,928 | 9.229 | 20 | 20 | fits | 75,478 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 362,684 | 3.627 | 20 | 20 | fits | 120,024 | 176 | 0.401 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 301,132 | 3.011 | 20 | 200 | fits | 144,508 | 220 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 420,540 | 4.205 | 20 | 200 | fits | 120,024 | 176 | 0.401 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 302,056 | 3.021 | 20 | 20 | fits | 144,508 | 220 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 421,244 | 4.212 | 20 | 20 | fits | 120,024 | 176 | 0.401 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 161,188 | 1.612 | 20 | 24 | fits | 149,598 | 155 | 0.333 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 304,706 | 3.047 | 20 | 24 | fits | 144,508 | 220 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 304,640 | 3.046 | 20 | 50 | fits | 144,508 | 220 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 424,268 | 4.243 | 20 | 50 | fits | 120,024 | 176 | 0.401 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 517,178 | 5.172 | 20 | 20 | fits | 84,645 | 31 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 924,512 | 9.245 | 20 | 20 | fits | 64,371 | 24 | 0.599 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 386,997 | 3.870 | 20 | 20 | fits | 111,805 | 166 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 325,518 | 3.255 | 20 | 200 | fits | 144,659 | 222 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 436,707 | 4.367 | 20 | 200 | fits | 111,805 | 166 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 326,442 | 3.264 | 20 | 20 | fits | 144,659 | 222 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 437,411 | 4.374 | 20 | 20 | fits | 111,805 | 166 | 0.406 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 185,423 | 1.854 | 20 | 24 | fits | 149,599 | 155 | 0.333 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 329,092 | 3.291 | 20 | 24 | fits | 144,659 | 222 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 329,026 | 3.290 | 20 | 50 | fits | 144,659 | 222 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 440,435 | 4.404 | 20 | 50 | fits | 111,805 | 166 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 521,383 | 5.214 | 20 | 20 | fits | 81,014 | 24 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 944,446 | 9.444 | 20 | 20 | fits | 75,754 | 28 | 0.568 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 353,420 | 3.534 | 20 | 20 | fits | 111,150 | 163 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 301,232 | 3.012 | 20 | 200 | fits | 145,787 | 226 | 0.376 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 411,766 | 4.118 | 20 | 200 | fits | 111,150 | 163 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 302,156 | 3.022 | 20 | 20 | fits | 145,787 | 226 | 0.376 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 412,470 | 4.125 | 20 | 20 | fits | 111,150 | 163 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 160,009 | 1.600 | 20 | 24 | fits | 149,547 | 155 | 0.333 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 304,806 | 3.048 | 20 | 24 | fits | 145,787 | 226 | 0.376 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 304,740 | 3.047 | 20 | 50 | fits | 145,787 | 226 | 0.376 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 415,494 | 4.155 | 20 | 50 | fits | 111,150 | 163 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 496,466 | 4.965 | 20 | 20 | fits | 81,038 | 24 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 925,662 | 9.257 | 20 | 20 | fits | 81,616 | 34 | 0.609 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 350,191 | 3.502 | 20 | 20 | fits | 111,805 | 166 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 288,712 | 2.887 | 20 | 200 | fits | 144,659 | 222 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 399,901 | 3.999 | 20 | 200 | fits | 111,805 | 166 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 289,636 | 2.896 | 20 | 20 | fits | 144,659 | 222 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 400,605 | 4.006 | 20 | 20 | fits | 111,805 | 166 | 0.406 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 148,617 | 1.486 | 20 | 24 | fits | 149,547 | 155 | 0.333 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 292,286 | 2.923 | 20 | 24 | fits | 144,659 | 222 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 292,220 | 2.922 | 20 | 50 | fits | 144,659 | 222 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 403,629 | 4.036 | 20 | 50 | fits | 111,805 | 166 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 484,793 | 4.848 | 20 | 20 | fits | 81,230 | 25 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 914,026 | 9.140 | 20 | 20 | fits | 86,394 | 32 | 0.529 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 352,693 | 3.527 | 20 | 20 | fits | 111,080 | 164 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 293,071 | 2.931 | 20 | 200 | fits | 146,276 | 226 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 403,535 | 4.035 | 20 | 200 | fits | 111,080 | 164 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 293,995 | 2.940 | 20 | 20 | fits | 146,276 | 226 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 404,239 | 4.042 | 20 | 20 | fits | 111,080 | 164 | 0.418 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 151,359 | 1.514 | 20 | 24 | fits | 149,480 | 155 | 0.332 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 296,645 | 2.966 | 20 | 24 | fits | 146,276 | 226 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 296,579 | 2.966 | 20 | 50 | fits | 146,276 | 226 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 407,263 | 4.073 | 20 | 50 | fits | 111,080 | 164 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 500,374 | 5.004 | 20 | 20 | fits | 84,900 | 31 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 914,558 | 9.146 | 20 | 20 | fits | 75,478 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 359,730 | 3.597 | 20 | 20 | fits | 114,494 | 170 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 296,148 | 2.961 | 20 | 200 | fits | 146,477 | 227 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 418,523 | 4.185 | 20 | 200 | fits | 114,494 | 170 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 297,072 | 2.971 | 20 | 20 | fits | 146,477 | 227 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 419,227 | 4.192 | 20 | 20 | fits | 114,494 | 170 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 154,235 | 1.542 | 20 | 24 | fits | 149,547 | 155 | 0.333 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 299,722 | 2.997 | 20 | 24 | fits | 146,477 | 227 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 299,656 | 2.997 | 20 | 50 | fits | 146,477 | 227 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 422,251 | 4.223 | 20 | 50 | fits | 114,494 | 170 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 509,478 | 5.095 | 20 | 20 | fits | 87,293 | 30 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 916,756 | 9.168 | 20 | 20 | fits | 64,371 | 24 | 0.599 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 366,752 | 3.668 | 20 | 20 | fits | 119,325 | 169 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 306,533 | 3.065 | 20 | 200 | fits | 146,509 | 231 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 425,242 | 4.252 | 20 | 200 | fits | 119,325 | 169 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 307,457 | 3.075 | 20 | 20 | fits | 146,509 | 231 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 425,946 | 4.259 | 20 | 20 | fits | 119,325 | 169 | 0.446 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 157,096 | 1.571 | 20 | 24 | fits | 149,599 | 156 | 0.333 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 310,107 | 3.101 | 20 | 24 | fits | 146,509 | 231 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 310,041 | 3.100 | 20 | 50 | fits | 146,509 | 231 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 428,970 | 4.290 | 20 | 50 | fits | 119,325 | 169 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 509,916 | 5.099 | 20 | 20 | fits | 81,012 | 24 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 917,218 | 9.172 | 20 | 20 | fits | 64,540 | 25 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 362,427 | 3.624 | 20 | 20 | fits | 120,188 | 172 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 292,707 | 2.927 | 20 | 200 | fits | 144,682 | 222 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 412,279 | 4.123 | 20 | 200 | fits | 120,188 | 172 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 293,631 | 2.936 | 20 | 20 | fits | 144,682 | 222 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 412,983 | 4.130 | 20 | 20 | fits | 120,188 | 172 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 152,589 | 1.526 | 20 | 24 | fits | 149,633 | 155 | 0.333 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 296,281 | 2.963 | 20 | 24 | fits | 144,682 | 222 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 296,215 | 2.962 | 20 | 50 | fits | 144,682 | 222 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 416,007 | 4.160 | 20 | 50 | fits | 120,188 | 172 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 496,875 | 4.969 | 20 | 20 | fits | 80,934 | 24 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 919,759 | 9.198 | 20 | 20 | fits | 69,988 | 31 | 0.681 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 363,635 | 3.636 | 20 | 20 | fits | 116,530 | 184 | 0.404 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 298,541 | 2.985 | 20 | 200 | fits | 147,774 | 209 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 414,455 | 4.145 | 20 | 200 | fits | 116,530 | 184 | 0.404 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 299,465 | 2.995 | 20 | 20 | fits | 147,774 | 209 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 415,159 | 4.152 | 20 | 20 | fits | 116,530 | 184 | 0.404 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 155,331 | 1.553 | 20 | 24 | fits | 149,566 | 155 | 0.332 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 302,115 | 3.021 | 20 | 24 | fits | 147,774 | 209 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 302,049 | 3.020 | 20 | 50 | fits | 147,774 | 209 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 418,183 | 4.182 | 20 | 50 | fits | 116,530 | 184 | 0.404 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 499,135 | 4.991 | 20 | 20 | fits | 81,018 | 24 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 922,231 | 9.222 | 20 | 20 | fits | 75,478 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 359,566 | 3.596 | 20 | 20 | fits | 115,780 | 173 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 293,836 | 2.938 | 20 | 200 | fits | 146,689 | 227 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 409,000 | 4.090 | 20 | 200 | fits | 115,780 | 173 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 294,760 | 2.948 | 20 | 20 | fits | 146,689 | 227 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 409,704 | 4.097 | 20 | 20 | fits | 115,780 | 173 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 151,711 | 1.517 | 20 | 24 | fits | 154,639 | 157 | 0.364 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 297,410 | 2.974 | 20 | 24 | fits | 146,689 | 227 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 297,344 | 2.973 | 20 | 50 | fits | 146,689 | 227 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 412,728 | 4.127 | 20 | 50 | fits | 115,780 | 173 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 503,159 | 5.032 | 20 | 20 | fits | 81,245 | 25 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 910,044 | 9.100 | 20 | 20 | fits | 64,323 | 24 | 0.599 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 363,638 | 3.636 | 20 | 20 | fits | 115,491 | 172 | 0.431 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 289,321 | 2.893 | 20 | 200 | fits | 146,268 | 228 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 413,640 | 4.136 | 20 | 200 | fits | 115,491 | 172 | 0.431 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 290,245 | 2.902 | 20 | 20 | fits | 146,268 | 228 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 414,344 | 4.143 | 20 | 20 | fits | 115,491 | 172 | 0.431 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 147,617 | 1.476 | 20 | 24 | fits | 150,035 | 152 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 292,895 | 2.929 | 20 | 24 | fits | 146,268 | 228 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 292,829 | 2.928 | 20 | 50 | fits | 146,268 | 228 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 417,368 | 4.174 | 20 | 50 | fits | 115,491 | 172 | 0.431 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 497,890 | 4.979 | 20 | 20 | fits | 80,588 | 24 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 912,213 | 9.122 | 20 | 20 | fits | 71,772 | 30 | 0.664 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 369,591 | 3.696 | 20 | 20 | fits | 110,518 | 163 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 310,189 | 3.102 | 20 | 200 | fits | 147,118 | 231 | 0.378 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 420,091 | 4.201 | 20 | 200 | fits | 110,518 | 163 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 311,113 | 3.111 | 20 | 20 | fits | 147,118 | 231 | 0.378 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 420,795 | 4.208 | 20 | 20 | fits | 110,518 | 163 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 159,166 | 1.592 | 20 | 24 | fits | 150,009 | 153 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 313,763 | 3.138 | 20 | 24 | fits | 147,118 | 231 | 0.378 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 313,697 | 3.137 | 20 | 50 | fits | 147,118 | 231 | 0.378 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 423,819 | 4.238 | 20 | 50 | fits | 110,518 | 163 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 504,404 | 5.044 | 20 | 20 | fits | 80,651 | 24 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 999,441 | 9.994 | 20 | 20 | fits | 79,817 | 36 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 348,351 | 3.484 | 20 | 20 | fits | 110,274 | 163 | 0.413 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 296,360 | 2.964 | 20 | 200 | fits | 145,809 | 226 | 0.378 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 406,018 | 4.060 | 20 | 200 | fits | 110,274 | 163 | 0.413 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 297,284 | 2.973 | 20 | 20 | fits | 145,809 | 226 | 0.378 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 406,722 | 4.067 | 20 | 20 | fits | 110,274 | 163 | 0.413 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 155,115 | 1.551 | 20 | 24 | fits | 149,340 | 152 | 0.330 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 299,934 | 2.999 | 20 | 24 | fits | 145,809 | 226 | 0.378 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 299,868 | 2.999 | 20 | 50 | fits | 145,809 | 226 | 0.378 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 409,746 | 4.097 | 20 | 50 | fits | 110,274 | 163 | 0.413 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 490,247 | 4.902 | 20 | 20 | fits | 80,567 | 24 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 996,448 | 9.964 | 20 | 20 | fits | 86,377 | 32 | 0.533 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 352,932 | 3.529 | 20 | 20 | fits | 110,708 | 163 | 0.417 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 293,366 | 2.934 | 20 | 200 | fits | 146,354 | 226 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 403,458 | 4.035 | 20 | 200 | fits | 110,708 | 163 | 0.417 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 294,290 | 2.943 | 20 | 20 | fits | 146,354 | 226 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 404,162 | 4.042 | 20 | 20 | fits | 110,708 | 163 | 0.417 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 151,576 | 1.516 | 20 | 24 | fits | 149,278 | 152 | 0.329 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 296,940 | 2.969 | 20 | 24 | fits | 146,354 | 226 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 296,874 | 2.969 | 20 | 50 | fits | 146,354 | 226 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 407,186 | 4.072 | 20 | 50 | fits | 110,708 | 163 | 0.417 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 487,708 | 4.877 | 20 | 20 | fits | 80,588 | 24 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 994,836 | 9.948 | 20 | 20 | fits | 86,099 | 32 | 0.521 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 342,025 | 3.420 | 20 | 20 | fits | 110,966 | 163 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 289,877 | 2.899 | 20 | 200 | fits | 147,165 | 231 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 400,227 | 4.002 | 20 | 200 | fits | 110,966 | 163 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 290,801 | 2.908 | 20 | 20 | fits | 147,165 | 231 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 400,931 | 4.009 | 20 | 20 | fits | 110,966 | 163 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 147,276 | 1.473 | 20 | 24 | fits | 149,278 | 152 | 0.329 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 293,451 | 2.935 | 20 | 24 | fits | 147,165 | 231 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 293,385 | 2.934 | 20 | 50 | fits | 147,165 | 231 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 403,955 | 4.040 | 20 | 50 | fits | 110,966 | 163 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 490,641 | 4.906 | 20 | 20 | fits | 86,752 | 30 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 991,033 | 9.910 | 20 | 20 | fits | 75,422 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 360,996 | 3.610 | 20 | 20 | fits | 118,726 | 170 | 0.442 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 300,941 | 3.009 | 20 | 200 | fits | 145,809 | 226 | 0.378 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 419,051 | 4.191 | 20 | 200 | fits | 118,726 | 170 | 0.442 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 301,865 | 3.019 | 20 | 20 | fits | 145,809 | 226 | 0.378 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 419,755 | 4.198 | 20 | 20 | fits | 118,726 | 170 | 0.442 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 159,696 | 1.597 | 20 | 24 | fits | 149,423 | 152 | 0.331 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 304,515 | 3.045 | 20 | 24 | fits | 145,809 | 226 | 0.378 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 304,449 | 3.044 | 20 | 50 | fits | 145,809 | 226 | 0.378 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 422,779 | 4.228 | 20 | 50 | fits | 118,726 | 170 | 0.442 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 591,020 | 5.910 | 20 | 20 | fits | 84,205 | 31 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 998,050 | 9.980 | 20 | 20 | fits | 64,323 | 24 | 0.599 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 451,982 | 4.520 | 20 | 20 | fits | 120,123 | 190 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 299,589 | 2.996 | 20 | 200 | fits | 148,057 | 210 | 0.402 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 503,339 | 5.033 | 20 | 200 | fits | 120,123 | 190 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 300,513 | 3.005 | 20 | 20 | fits | 148,057 | 210 | 0.402 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 504,043 | 5.040 | 20 | 20 | fits | 120,123 | 190 | 0.432 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 156,096 | 1.561 | 20 | 24 | fits | 149,423 | 152 | 0.331 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 303,163 | 3.032 | 20 | 24 | fits | 148,057 | 210 | 0.402 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 303,097 | 3.031 | 20 | 50 | fits | 148,057 | 210 | 0.402 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 507,067 | 5.071 | 20 | 50 | fits | 120,123 | 190 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 587,932 | 5.879 | 20 | 20 | fits | 80,931 | 24 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 994,761 | 9.948 | 20 | 20 | fits | 64,323 | 24 | 0.599 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 341,806 | 3.418 | 20 | 20 | fits | 111,265 | 163 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 289,491 | 2.895 | 20 | 200 | fits | 147,597 | 231 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 400,140 | 4.001 | 20 | 200 | fits | 111,265 | 163 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 290,415 | 2.904 | 20 | 20 | fits | 147,597 | 231 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 400,844 | 4.008 | 20 | 20 | fits | 111,265 | 163 | 0.421 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 146,458 | 1.465 | 20 | 24 | fits | 149,578 | 152 | 0.332 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 293,065 | 2.931 | 20 | 24 | fits | 147,597 | 231 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 292,999 | 2.930 | 20 | 50 | fits | 147,597 | 231 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 403,868 | 4.039 | 20 | 50 | fits | 111,265 | 163 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 484,877 | 4.849 | 20 | 20 | fits | 81,075 | 24 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 907,408 | 9.074 | 20 | 20 | fits | 75,422 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 351,512 | 3.515 | 20 | 20 | fits | 111,110 | 163 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 299,278 | 2.993 | 20 | 200 | fits | 145,676 | 226 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 409,772 | 4.098 | 20 | 200 | fits | 111,110 | 163 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 300,202 | 3.002 | 20 | 20 | fits | 145,676 | 226 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 410,476 | 4.105 | 20 | 20 | fits | 111,110 | 163 | 0.421 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 158,166 | 1.582 | 20 | 24 | fits | 149,567 | 152 | 0.332 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 302,852 | 3.029 | 20 | 24 | fits | 145,676 | 226 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 302,786 | 3.028 | 20 | 50 | fits | 145,676 | 226 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 413,500 | 4.135 | 20 | 50 | fits | 111,110 | 163 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 499,071 | 4.991 | 20 | 20 | fits | 85,637 | 31 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 932,396 | 9.324 | 20 | 20 | fits | 79,155 | 30 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 368,268 | 3.683 | 20 | 20 | fits | 115,404 | 173 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 294,904 | 2.949 | 20 | 200 | fits | 144,774 | 223 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 418,270 | 4.183 | 20 | 200 | fits | 115,404 | 173 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 295,828 | 2.958 | 20 | 20 | fits | 144,774 | 223 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 418,974 | 4.190 | 20 | 20 | fits | 115,404 | 173 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 154,694 | 1.547 | 20 | 24 | fits | 149,567 | 152 | 0.332 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 298,478 | 2.985 | 20 | 24 | fits | 144,774 | 223 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 298,412 | 2.984 | 20 | 50 | fits | 144,774 | 223 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 421,998 | 4.220 | 20 | 50 | fits | 115,404 | 173 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 503,060 | 5.031 | 20 | 20 | fits | 81,128 | 24 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 970,281 | 9.703 | 20 | 20 | fits | 89,228 | 33 | 0.608 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 356,015 | 3.560 | 20 | 20 | fits | 111,164 | 163 | 0.427 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 295,198 | 2.952 | 20 | 200 | fits | 148,540 | 232 | 0.378 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 414,340 | 4.143 | 20 | 200 | fits | 111,164 | 163 | 0.427 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 296,122 | 2.961 | 20 | 20 | fits | 148,540 | 232 | 0.378 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 415,044 | 4.150 | 20 | 20 | fits | 111,164 | 163 | 0.427 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 151,222 | 1.512 | 20 | 24 | fits | 149,567 | 152 | 0.332 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 298,772 | 2.988 | 20 | 24 | fits | 148,540 | 232 | 0.378 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 298,706 | 2.987 | 20 | 50 | fits | 148,540 | 232 | 0.378 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 418,068 | 4.181 | 20 | 50 | fits | 111,164 | 163 | 0.427 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 499,062 | 4.991 | 20 | 20 | fits | 81,060 | 24 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 997,532 | 9.975 | 20 | 20 | fits | 86,398 | 32 | 0.535 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 351,156 | 3.512 | 20 | 20 | fits | 113,433 | 169 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 296,242 | 2.962 | 20 | 200 | fits | 145,784 | 231 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 409,059 | 4.091 | 20 | 200 | fits | 113,433 | 169 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 297,166 | 2.972 | 20 | 20 | fits | 145,784 | 231 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 409,763 | 4.098 | 20 | 20 | fits | 113,433 | 169 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 147,548 | 1.475 | 20 | 24 | fits | 149,558 | 153 | 0.333 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 299,816 | 2.998 | 20 | 24 | fits | 145,784 | 231 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 299,750 | 2.998 | 20 | 50 | fits | 145,784 | 231 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 412,787 | 4.128 | 20 | 50 | fits | 113,433 | 169 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 493,945 | 4.939 | 20 | 20 | fits | 81,224 | 24 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 992,504 | 9.925 | 20 | 20 | fits | 86,268 | 33 | 0.523 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 358,664 | 3.587 | 20 | 20 | fits | 110,788 | 163 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 299,052 | 2.991 | 20 | 200 | fits | 146,034 | 226 | 0.378 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 409,224 | 4.092 | 20 | 200 | fits | 110,788 | 163 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 299,976 | 3.000 | 20 | 20 | fits | 146,034 | 226 | 0.378 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 409,928 | 4.099 | 20 | 20 | fits | 110,788 | 163 | 0.418 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 157,582 | 1.576 | 20 | 24 | fits | 149,270 | 152 | 0.329 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 302,626 | 3.026 | 20 | 24 | fits | 146,034 | 226 | 0.378 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 302,560 | 3.026 | 20 | 50 | fits | 146,034 | 226 | 0.378 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 412,952 | 4.130 | 20 | 50 | fits | 110,788 | 163 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 497,682 | 4.977 | 20 | 20 | fits | 84,796 | 26 | 0.817 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 1,007,247 | 10.072 | 20 | 20 | fits | 86,099 | 32 | 0.521 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 365,915 | 3.659 | 20 | 20 | fits | 131,862 | 169 | 0.480 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 294,903 | 2.949 | 20 | 200 | fits | 145,485 | 226 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 426,149 | 4.261 | 20 | 200 | fits | 131,862 | 169 | 0.480 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 295,827 | 2.958 | 20 | 20 | fits | 145,485 | 226 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 426,853 | 4.269 | 20 | 20 | fits | 131,862 | 169 | 0.480 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 153,982 | 1.540 | 20 | 24 | fits | 149,270 | 152 | 0.329 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 298,477 | 2.985 | 20 | 24 | fits | 145,485 | 226 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 298,411 | 2.984 | 20 | 50 | fits | 145,485 | 226 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 429,877 | 4.299 | 20 | 50 | fits | 131,862 | 169 | 0.480 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 552,106 | 5.521 | 20 | 20 | fits | 81,178 | 25 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 1,007,015 | 10.070 | 20 | 20 | fits | 75,422 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 372,070 | 3.721 | 20 | 20 | fits | 127,127 | 199 | 0.385 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 295,237 | 2.952 | 20 | 200 | fits | 149,419 | 194 | 0.449 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 421,748 | 4.217 | 20 | 200 | fits | 127,127 | 199 | 0.385 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 296,161 | 2.962 | 20 | 20 | fits | 149,419 | 194 | 0.449 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 422,452 | 4.225 | 20 | 20 | fits | 127,127 | 199 | 0.385 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 150,382 | 1.504 | 20 | 24 | fits | 149,270 | 152 | 0.329 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 298,811 | 2.988 | 20 | 24 | fits | 149,419 | 194 | 0.449 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 298,745 | 2.987 | 20 | 50 | fits | 149,419 | 194 | 0.449 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 425,476 | 4.255 | 20 | 50 | fits | 127,127 | 199 | 0.385 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 552,123 | 5.521 | 20 | 20 | fits | 85,451 | 32 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 1,001,589 | 10.016 | 20 | 20 | fits | 64,323 | 24 | 0.599 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 360,003 | 3.600 | 20 | 20 | fits | 114,902 | 172 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 295,699 | 2.957 | 20 | 200 | fits | 144,791 | 227 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 409,985 | 4.100 | 20 | 200 | fits | 114,902 | 172 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 296,623 | 2.966 | 20 | 20 | fits | 144,791 | 227 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 410,689 | 4.107 | 20 | 20 | fits | 114,902 | 172 | 0.418 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 147,961 | 1.480 | 20 | 24 | fits | 149,971 | 153 | 0.333 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 299,273 | 2.993 | 20 | 24 | fits | 144,791 | 227 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 299,207 | 2.992 | 20 | 50 | fits | 144,791 | 227 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 413,713 | 4.137 | 20 | 50 | fits | 114,902 | 172 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 494,460 | 4.945 | 20 | 20 | fits | 80,813 | 24 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 901,593 | 9.016 | 20 | 20 | fits | 64,371 | 24 | 0.599 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 369,813 | 3.698 | 20 | 20 | fits | 110,702 | 163 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 310,355 | 3.104 | 20 | 200 | fits | 146,759 | 231 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 420,441 | 4.204 | 20 | 200 | fits | 110,702 | 163 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 311,279 | 3.113 | 20 | 20 | fits | 146,759 | 231 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 421,145 | 4.211 | 20 | 20 | fits | 110,702 | 163 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 160,649 | 1.606 | 20 | 24 | fits | 149,730 | 153 | 0.332 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 313,929 | 3.139 | 20 | 24 | fits | 146,759 | 231 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 313,863 | 3.139 | 20 | 50 | fits | 146,759 | 231 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 424,169 | 4.242 | 20 | 50 | fits | 110,702 | 163 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 504,896 | 5.049 | 20 | 20 | fits | 80,793 | 24 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 919,465 | 9.195 | 20 | 20 | fits | 71,805 | 31 | 0.660 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 348,356 | 3.484 | 20 | 20 | fits | 110,458 | 163 | 0.413 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 296,317 | 2.963 | 20 | 200 | fits | 145,791 | 226 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 406,159 | 4.062 | 20 | 200 | fits | 110,458 | 163 | 0.413 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 297,241 | 2.972 | 20 | 20 | fits | 145,791 | 226 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 406,863 | 4.069 | 20 | 20 | fits | 110,458 | 163 | 0.413 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 155,090 | 1.551 | 20 | 24 | fits | 149,549 | 152 | 0.330 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 299,891 | 2.999 | 20 | 24 | fits | 145,791 | 226 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 299,825 | 2.998 | 20 | 50 | fits | 145,791 | 226 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 409,887 | 4.099 | 20 | 50 | fits | 110,458 | 163 | 0.413 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 490,476 | 4.905 | 20 | 20 | fits | 80,655 | 24 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 998,958 | 9.990 | 20 | 20 | fits | 76,257 | 29 | 0.575 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 352,952 | 3.530 | 20 | 20 | fits | 110,892 | 163 | 0.417 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 293,330 | 2.933 | 20 | 200 | fits | 146,276 | 226 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 403,606 | 4.036 | 20 | 200 | fits | 110,892 | 163 | 0.417 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 294,254 | 2.943 | 20 | 20 | fits | 146,276 | 226 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 404,310 | 4.043 | 20 | 20 | fits | 110,892 | 163 | 0.417 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 151,618 | 1.516 | 20 | 24 | fits | 149,549 | 152 | 0.330 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 296,904 | 2.969 | 20 | 24 | fits | 146,276 | 226 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 296,838 | 2.968 | 20 | 50 | fits | 146,276 | 226 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 407,334 | 4.073 | 20 | 50 | fits | 110,892 | 163 | 0.417 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 487,944 | 4.879 | 20 | 20 | fits | 80,676 | 24 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 996,532 | 9.965 | 20 | 20 | fits | 75,478 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 342,310 | 3.423 | 20 | 20 | fits | 111,150 | 163 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 290,122 | 2.901 | 20 | 200 | fits | 147,147 | 231 | 0.374 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 400,656 | 4.007 | 20 | 200 | fits | 111,150 | 163 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 291,046 | 2.910 | 20 | 20 | fits | 147,147 | 231 | 0.374 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 401,360 | 4.014 | 20 | 20 | fits | 111,150 | 163 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 147,539 | 1.475 | 20 | 24 | fits | 149,549 | 152 | 0.330 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 293,696 | 2.937 | 20 | 24 | fits | 147,147 | 231 | 0.374 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 293,630 | 2.936 | 20 | 50 | fits | 147,147 | 231 | 0.374 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 404,384 | 4.044 | 20 | 50 | fits | 111,150 | 163 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 485,153 | 4.852 | 20 | 20 | fits | 80,835 | 25 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 993,504 | 9.935 | 20 | 20 | fits | 75,478 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 353,142 | 3.531 | 20 | 20 | fits | 110,646 | 164 | 0.414 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 301,103 | 3.011 | 20 | 200 | fits | 145,791 | 226 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 411,133 | 4.111 | 20 | 200 | fits | 110,646 | 164 | 0.414 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 302,027 | 3.020 | 20 | 20 | fits | 145,791 | 226 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 411,837 | 4.118 | 20 | 20 | fits | 110,646 | 164 | 0.414 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 159,876 | 1.599 | 20 | 24 | fits | 149,560 | 152 | 0.330 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 304,677 | 3.047 | 20 | 24 | fits | 145,791 | 226 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 304,611 | 3.046 | 20 | 50 | fits | 145,791 | 226 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 414,861 | 4.149 | 20 | 50 | fits | 110,646 | 164 | 0.414 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 512,207 | 5.122 | 20 | 20 | fits | 89,113 | 37 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,000,511 | 10.005 | 20 | 20 | fits | 64,371 | 24 | 0.599 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 377,090 | 3.771 | 20 | 20 | fits | 121,893 | 176 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 298,278 | 2.983 | 20 | 200 | fits | 146,438 | 227 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 428,074 | 4.281 | 20 | 200 | fits | 121,893 | 176 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 299,202 | 2.992 | 20 | 20 | fits | 146,438 | 227 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 428,778 | 4.288 | 20 | 20 | fits | 121,893 | 176 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 156,404 | 1.564 | 20 | 24 | fits | 149,560 | 152 | 0.330 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 301,852 | 3.019 | 20 | 24 | fits | 146,438 | 227 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 301,786 | 3.018 | 20 | 50 | fits | 146,438 | 227 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 431,802 | 4.318 | 20 | 50 | fits | 121,893 | 176 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 592,955 | 5.930 | 20 | 20 | fits | 81,219 | 25 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,000,269 | 10.003 | 20 | 20 | fits | 64,371 | 24 | 0.599 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 443,563 | 4.436 | 20 | 20 | fits | 122,801 | 181 | 0.413 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 299,787 | 2.998 | 20 | 200 | fits | 143,881 | 220 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 502,067 | 5.021 | 20 | 200 | fits | 122,801 | 181 | 0.413 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 300,711 | 3.007 | 20 | 20 | fits | 143,881 | 220 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 502,771 | 5.028 | 20 | 20 | fits | 122,801 | 181 | 0.413 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 153,033 | 1.530 | 20 | 24 | fits | 149,661 | 153 | 0.331 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 303,361 | 3.034 | 20 | 24 | fits | 143,881 | 220 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 303,295 | 3.033 | 20 | 50 | fits | 143,881 | 220 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 505,795 | 5.058 | 20 | 50 | fits | 122,801 | 181 | 0.413 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 586,550 | 5.865 | 20 | 20 | fits | 80,821 | 24 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,009,239 | 10.092 | 20 | 20 | fits | 69,770 | 31 | 0.679 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 353,220 | 3.532 | 20 | 20 | fits | 110,646 | 164 | 0.414 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 301,181 | 3.012 | 20 | 200 | fits | 145,870 | 226 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 411,211 | 4.112 | 20 | 200 | fits | 110,646 | 164 | 0.414 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 302,105 | 3.021 | 20 | 20 | fits | 145,870 | 226 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 411,915 | 4.119 | 20 | 20 | fits | 110,646 | 164 | 0.414 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 159,875 | 1.599 | 20 | 24 | fits | 149,710 | 152 | 0.331 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 304,755 | 3.048 | 20 | 24 | fits | 145,870 | 226 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 304,689 | 3.047 | 20 | 50 | fits | 145,870 | 226 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 414,939 | 4.149 | 20 | 50 | fits | 110,646 | 164 | 0.414 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 507,768 | 5.078 | 20 | 20 | fits | 84,496 | 31 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 915,163 | 9.152 | 20 | 20 | fits | 64,371 | 24 | 0.599 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 369,780 | 3.698 | 20 | 20 | fits | 114,604 | 170 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 298,374 | 2.984 | 20 | 200 | fits | 146,535 | 227 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 420,948 | 4.209 | 20 | 200 | fits | 114,604 | 170 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 299,298 | 2.993 | 20 | 20 | fits | 146,535 | 227 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 421,652 | 4.217 | 20 | 20 | fits | 114,604 | 170 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 156,403 | 1.564 | 20 | 24 | fits | 149,710 | 152 | 0.331 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 301,948 | 3.019 | 20 | 24 | fits | 146,535 | 227 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 301,882 | 3.019 | 20 | 50 | fits | 146,535 | 227 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 424,676 | 4.247 | 20 | 50 | fits | 114,604 | 170 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 505,607 | 5.056 | 20 | 20 | fits | 80,997 | 24 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 920,177 | 9.202 | 20 | 20 | fits | 71,808 | 30 | 0.664 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 354,572 | 3.546 | 20 | 20 | fits | 110,954 | 163 | 0.417 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 302,533 | 3.025 | 20 | 200 | fits | 146,509 | 231 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 412,871 | 4.129 | 20 | 200 | fits | 110,954 | 163 | 0.417 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 303,457 | 3.035 | 20 | 20 | fits | 146,509 | 231 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 413,575 | 4.136 | 20 | 20 | fits | 110,954 | 163 | 0.417 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 153,050 | 1.530 | 20 | 24 | fits | 149,829 | 153 | 0.333 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 306,107 | 3.061 | 20 | 24 | fits | 146,509 | 231 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 306,041 | 3.060 | 20 | 50 | fits | 146,509 | 231 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 416,599 | 4.166 | 20 | 50 | fits | 110,954 | 163 | 0.417 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 497,283 | 4.973 | 20 | 20 | fits | 80,750 | 24 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 912,136 | 9.121 | 20 | 20 | fits | 75,940 | 29 | 0.569 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 349,280 | 3.493 | 20 | 20 | fits | 110,845 | 163 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 289,658 | 2.897 | 20 | 200 | fits | 147,659 | 231 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 399,887 | 3.999 | 20 | 200 | fits | 110,845 | 163 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 290,582 | 2.906 | 20 | 20 | fits | 147,659 | 231 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 400,591 | 4.006 | 20 | 20 | fits | 110,845 | 163 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 146,563 | 1.466 | 20 | 24 | fits | 149,535 | 152 | 0.329 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 293,232 | 2.932 | 20 | 24 | fits | 147,659 | 231 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 293,166 | 2.932 | 20 | 50 | fits | 147,659 | 231 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 403,615 | 4.036 | 20 | 50 | fits | 110,845 | 163 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 484,279 | 4.843 | 20 | 20 | fits | 80,730 | 24 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 913,699 | 9.137 | 20 | 20 | fits | 80,103 | 35 | 0.635 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 352,597 | 3.526 | 20 | 20 | fits | 111,227 | 163 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 300,328 | 3.003 | 20 | 200 | fits | 146,311 | 226 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 410,939 | 4.109 | 20 | 200 | fits | 111,227 | 163 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 301,252 | 3.013 | 20 | 20 | fits | 146,311 | 226 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 411,643 | 4.116 | 20 | 20 | fits | 111,227 | 163 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 158,581 | 1.586 | 20 | 24 | fits | 149,618 | 152 | 0.330 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 303,902 | 3.039 | 20 | 24 | fits | 146,311 | 226 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 303,836 | 3.038 | 20 | 50 | fits | 146,311 | 226 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 414,667 | 4.147 | 20 | 50 | fits | 111,227 | 163 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 495,399 | 4.954 | 20 | 20 | fits | 80,798 | 24 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 925,070 | 9.251 | 20 | 20 | fits | 86,163 | 32 | 0.521 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 348,398 | 3.484 | 20 | 20 | fits | 110,411 | 163 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 296,359 | 2.964 | 20 | 200 | fits | 145,814 | 226 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 406,154 | 4.062 | 20 | 200 | fits | 110,411 | 163 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 297,283 | 2.973 | 20 | 20 | fits | 145,814 | 226 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 406,858 | 4.069 | 20 | 20 | fits | 110,411 | 163 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 155,109 | 1.551 | 20 | 24 | fits | 149,618 | 152 | 0.330 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 299,933 | 2.999 | 20 | 24 | fits | 145,814 | 226 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 299,867 | 2.999 | 20 | 50 | fits | 145,814 | 226 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 409,882 | 4.099 | 20 | 50 | fits | 110,411 | 163 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 496,896 | 4.969 | 20 | 20 | fits | 87,080 | 30 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 919,593 | 9.196 | 20 | 20 | fits | 75,478 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 360,935 | 3.609 | 20 | 20 | fits | 119,172 | 170 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 293,372 | 2.934 | 20 | 200 | fits | 146,299 | 226 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 411,928 | 4.119 | 20 | 200 | fits | 119,172 | 170 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 294,296 | 2.943 | 20 | 20 | fits | 146,299 | 226 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 412,632 | 4.126 | 20 | 20 | fits | 119,172 | 170 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 151,637 | 1.516 | 20 | 24 | fits | 149,618 | 152 | 0.330 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 296,946 | 2.969 | 20 | 24 | fits | 146,299 | 226 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 296,880 | 2.969 | 20 | 50 | fits | 146,299 | 226 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 415,656 | 4.157 | 20 | 50 | fits | 119,172 | 170 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 508,666 | 5.087 | 20 | 20 | fits | 84,363 | 31 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 916,000 | 9.160 | 20 | 20 | fits | 64,371 | 24 | 0.599 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 361,478 | 3.615 | 20 | 20 | fits | 121,813 | 175 | 0.454 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 290,414 | 2.904 | 20 | 200 | fits | 147,370 | 232 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 420,086 | 4.201 | 20 | 200 | fits | 121,813 | 175 | 0.454 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 291,338 | 2.913 | 20 | 20 | fits | 147,370 | 232 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 420,790 | 4.208 | 20 | 20 | fits | 121,813 | 175 | 0.454 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 147,608 | 1.476 | 20 | 24 | fits | 149,618 | 152 | 0.330 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 293,988 | 2.940 | 20 | 24 | fits | 147,370 | 232 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 293,922 | 2.939 | 20 | 50 | fits | 147,370 | 232 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 423,814 | 4.238 | 20 | 50 | fits | 121,813 | 175 | 0.454 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 504,526 | 5.045 | 20 | 20 | fits | 80,778 | 24 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 911,659 | 9.117 | 20 | 20 | fits | 64,371 | 24 | 0.599 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 349,929 | 3.499 | 20 | 20 | fits | 110,845 | 163 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 290,307 | 2.903 | 20 | 200 | fits | 147,659 | 231 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 400,536 | 4.005 | 20 | 200 | fits | 110,845 | 163 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 291,231 | 2.912 | 20 | 20 | fits | 147,659 | 231 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 401,240 | 4.012 | 20 | 20 | fits | 110,845 | 163 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 147,212 | 1.472 | 20 | 24 | fits | 149,540 | 152 | 0.329 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 293,881 | 2.939 | 20 | 24 | fits | 147,659 | 231 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 293,815 | 2.938 | 20 | 50 | fits | 147,659 | 231 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 404,264 | 4.043 | 20 | 50 | fits | 110,845 | 163 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 485,216 | 4.852 | 20 | 20 | fits | 81,018 | 24 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 909,893 | 9.099 | 20 | 20 | fits | 77,729 | 29 | 0.625 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 352,958 | 3.530 | 20 | 20 | fits | 111,227 | 163 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 300,689 | 3.007 | 20 | 200 | fits | 146,311 | 226 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 411,300 | 4.113 | 20 | 200 | fits | 111,227 | 163 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 301,613 | 3.016 | 20 | 20 | fits | 146,311 | 226 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 412,004 | 4.120 | 20 | 20 | fits | 111,227 | 163 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 158,942 | 1.589 | 20 | 24 | fits | 149,551 | 152 | 0.329 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 304,263 | 3.043 | 20 | 24 | fits | 146,311 | 226 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 304,197 | 3.042 | 20 | 50 | fits | 146,311 | 226 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 415,028 | 4.150 | 20 | 50 | fits | 111,227 | 163 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 496,048 | 4.960 | 20 | 20 | fits | 81,086 | 24 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 925,181 | 9.252 | 20 | 20 | fits | 81,616 | 34 | 0.609 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 348,759 | 3.488 | 20 | 20 | fits | 110,411 | 163 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 296,720 | 2.967 | 20 | 200 | fits | 145,814 | 226 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 406,515 | 4.065 | 20 | 200 | fits | 110,411 | 163 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 297,644 | 2.976 | 20 | 20 | fits | 145,814 | 226 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 407,219 | 4.072 | 20 | 20 | fits | 110,411 | 163 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 155,470 | 1.555 | 20 | 24 | fits | 149,551 | 152 | 0.329 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 300,294 | 3.003 | 20 | 24 | fits | 145,814 | 226 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 300,228 | 3.002 | 20 | 50 | fits | 145,814 | 226 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 410,243 | 4.102 | 20 | 50 | fits | 110,411 | 163 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 491,242 | 4.912 | 20 | 20 | fits | 81,065 | 24 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 999,453 | 9.995 | 20 | 20 | fits | 86,551 | 33 | 0.531 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 353,355 | 3.534 | 20 | 20 | fits | 111,033 | 164 | 0.417 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 293,733 | 2.937 | 20 | 200 | fits | 146,299 | 226 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 404,150 | 4.042 | 20 | 200 | fits | 111,033 | 164 | 0.417 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 294,657 | 2.947 | 20 | 20 | fits | 146,299 | 226 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 404,854 | 4.049 | 20 | 20 | fits | 111,033 | 164 | 0.417 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 151,998 | 1.520 | 20 | 24 | fits | 149,551 | 152 | 0.329 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 297,307 | 2.973 | 20 | 24 | fits | 146,299 | 226 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 297,241 | 2.972 | 20 | 50 | fits | 146,299 | 226 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 407,878 | 4.079 | 20 | 50 | fits | 111,033 | 164 | 0.417 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 501,017 | 5.010 | 20 | 20 | fits | 84,954 | 31 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 992,399 | 9.924 | 20 | 20 | fits | 75,400 | 28 | 0.556 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 353,766 | 3.538 | 20 | 20 | fits | 114,358 | 169 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 290,347 | 2.903 | 20 | 200 | fits | 147,370 | 232 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 412,516 | 4.125 | 20 | 200 | fits | 114,358 | 169 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 291,271 | 2.913 | 20 | 20 | fits | 147,370 | 232 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 413,220 | 4.132 | 20 | 20 | fits | 114,358 | 169 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 147,541 | 1.475 | 20 | 24 | fits | 149,551 | 152 | 0.329 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 293,921 | 2.939 | 20 | 24 | fits | 147,370 | 232 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 293,855 | 2.939 | 20 | 50 | fits | 147,370 | 232 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 416,244 | 4.162 | 20 | 50 | fits | 114,358 | 169 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 497,375 | 4.974 | 20 | 20 | fits | 81,197 | 24 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 989,427 | 9.894 | 20 | 20 | fits | 75,478 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 369,670 | 3.697 | 20 | 20 | fits | 118,770 | 169 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 309,484 | 3.095 | 20 | 200 | fits | 146,277 | 231 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 427,638 | 4.276 | 20 | 200 | fits | 118,770 | 169 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 310,408 | 3.104 | 20 | 20 | fits | 146,277 | 231 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 428,342 | 4.283 | 20 | 20 | fits | 118,770 | 169 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 160,382 | 1.604 | 20 | 24 | fits | 149,688 | 153 | 0.330 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 313,058 | 3.131 | 20 | 24 | fits | 146,277 | 231 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 312,992 | 3.130 | 20 | 50 | fits | 146,277 | 231 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 431,366 | 4.314 | 20 | 50 | fits | 118,770 | 169 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 589,534 | 5.895 | 20 | 20 | fits | 81,023 | 25 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,012,155 | 10.122 | 20 | 20 | fits | 69,781 | 31 | 0.679 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 374,630 | 3.746 | 20 | 20 | fits | 119,085 | 169 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 306,978 | 3.070 | 20 | 200 | fits | 146,242 | 226 | 0.378 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 425,447 | 4.254 | 20 | 200 | fits | 119,085 | 169 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 307,902 | 3.079 | 20 | 20 | fits | 146,242 | 226 | 0.378 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 426,151 | 4.262 | 20 | 20 | fits | 119,085 | 169 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 165,300 | 1.653 | 20 | 24 | fits | 148,078 | 153 | 0.324 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 310,552 | 3.106 | 20 | 24 | fits | 146,242 | 226 | 0.378 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 310,486 | 3.105 | 20 | 50 | fits | 146,242 | 226 | 0.378 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 429,175 | 4.292 | 20 | 50 | fits | 119,085 | 169 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 587,411 | 5.874 | 20 | 20 | fits | 81,091 | 25 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,010,228 | 10.102 | 20 | 20 | fits | 75,754 | 28 | 0.568 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 429,866 | 4.299 | 20 | 20 | fits | 119,639 | 175 | 0.400 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 291,496 | 2.915 | 20 | 200 | fits | 144,485 | 220 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 487,636 | 4.876 | 20 | 200 | fits | 119,639 | 175 | 0.400 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 292,420 | 2.924 | 20 | 20 | fits | 144,485 | 220 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 488,340 | 4.883 | 20 | 20 | fits | 119,639 | 175 | 0.400 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 151,575 | 1.516 | 20 | 24 | fits | 149,560 | 152 | 0.330 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 295,070 | 2.951 | 20 | 24 | fits | 144,485 | 220 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 295,004 | 2.950 | 20 | 50 | fits | 144,485 | 220 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 491,364 | 4.914 | 20 | 50 | fits | 119,639 | 175 | 0.400 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 572,302 | 5.723 | 20 | 20 | fits | 81,004 | 24 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 995,375 | 9.954 | 20 | 20 | fits | 75,478 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 361,240 | 3.612 | 20 | 20 | fits | 110,328 | 163 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 309,305 | 3.093 | 20 | 200 | fits | 146,277 | 231 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 419,017 | 4.190 | 20 | 200 | fits | 110,328 | 163 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 310,229 | 3.102 | 20 | 20 | fits | 146,277 | 231 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 419,721 | 4.197 | 20 | 20 | fits | 110,328 | 163 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 160,129 | 1.601 | 20 | 24 | fits | 149,856 | 153 | 0.332 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 312,879 | 3.129 | 20 | 24 | fits | 146,277 | 231 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 312,813 | 3.128 | 20 | 50 | fits | 146,277 | 231 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 422,745 | 4.227 | 20 | 50 | fits | 110,328 | 163 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 503,807 | 5.038 | 20 | 20 | fits | 81,128 | 24 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 910,942 | 9.109 | 20 | 20 | fits | 64,371 | 24 | 0.599 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 365,683 | 3.657 | 20 | 20 | fits | 110,702 | 163 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 306,225 | 3.062 | 20 | 200 | fits | 146,759 | 231 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 416,311 | 4.163 | 20 | 200 | fits | 110,702 | 163 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 307,149 | 3.071 | 20 | 20 | fits | 146,759 | 231 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 417,015 | 4.170 | 20 | 20 | fits | 110,702 | 163 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 156,567 | 1.566 | 20 | 24 | fits | 149,766 | 153 | 0.332 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 309,799 | 3.098 | 20 | 24 | fits | 146,759 | 231 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 309,733 | 3.097 | 20 | 50 | fits | 146,759 | 231 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 420,039 | 4.200 | 20 | 50 | fits | 110,702 | 163 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 501,122 | 5.011 | 20 | 20 | fits | 81,149 | 24 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 915,490 | 9.155 | 20 | 20 | fits | 71,627 | 30 | 0.660 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 343,769 | 3.438 | 20 | 20 | fits | 110,458 | 163 | 0.413 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 291,730 | 2.917 | 20 | 200 | fits | 145,791 | 226 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 401,572 | 4.016 | 20 | 200 | fits | 110,458 | 163 | 0.413 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 292,654 | 2.927 | 20 | 20 | fits | 145,791 | 226 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 402,276 | 4.023 | 20 | 20 | fits | 110,458 | 163 | 0.413 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 150,503 | 1.505 | 20 | 24 | fits | 149,627 | 152 | 0.331 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 295,304 | 2.953 | 20 | 24 | fits | 145,791 | 226 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 295,238 | 2.952 | 20 | 50 | fits | 145,791 | 226 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 405,300 | 4.053 | 20 | 50 | fits | 110,458 | 163 | 0.413 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 486,245 | 4.862 | 20 | 20 | fits | 81,011 | 24 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 913,882 | 9.139 | 20 | 20 | fits | 75,693 | 28 | 0.566 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 349,725 | 3.497 | 20 | 20 | fits | 110,892 | 163 | 0.417 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 290,103 | 2.901 | 20 | 200 | fits | 147,636 | 231 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 400,379 | 4.004 | 20 | 200 | fits | 110,892 | 163 | 0.417 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 291,027 | 2.910 | 20 | 20 | fits | 147,636 | 231 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 401,083 | 4.011 | 20 | 20 | fits | 110,892 | 163 | 0.417 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 147,031 | 1.470 | 20 | 24 | fits | 149,627 | 152 | 0.331 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 293,677 | 2.937 | 20 | 24 | fits | 147,636 | 231 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 293,611 | 2.936 | 20 | 50 | fits | 147,636 | 231 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 404,107 | 4.041 | 20 | 50 | fits | 110,892 | 163 | 0.417 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 485,073 | 4.851 | 20 | 20 | fits | 81,032 | 24 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 912,790 | 9.128 | 20 | 20 | fits | 75,478 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 352,598 | 3.526 | 20 | 20 | fits | 111,274 | 163 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 300,329 | 3.003 | 20 | 200 | fits | 146,288 | 226 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 410,987 | 4.110 | 20 | 200 | fits | 111,274 | 163 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 301,253 | 3.013 | 20 | 20 | fits | 146,288 | 226 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 411,691 | 4.117 | 20 | 20 | fits | 111,274 | 163 | 0.421 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 158,605 | 1.586 | 20 | 24 | fits | 149,482 | 152 | 0.329 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 303,903 | 3.039 | 20 | 24 | fits | 146,288 | 226 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 303,837 | 3.038 | 20 | 50 | fits | 146,288 | 226 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 414,715 | 4.147 | 20 | 50 | fits | 111,274 | 163 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 495,829 | 4.958 | 20 | 20 | fits | 81,180 | 25 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 923,185 | 9.232 | 20 | 20 | fits | 75,478 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 348,399 | 3.484 | 20 | 20 | fits | 110,646 | 164 | 0.414 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 296,360 | 2.964 | 20 | 200 | fits | 145,791 | 226 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 406,390 | 4.064 | 20 | 200 | fits | 110,646 | 164 | 0.414 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 297,284 | 2.973 | 20 | 20 | fits | 145,791 | 226 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 407,094 | 4.071 | 20 | 20 | fits | 110,646 | 164 | 0.414 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 155,133 | 1.551 | 20 | 24 | fits | 149,482 | 152 | 0.329 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 299,934 | 2.999 | 20 | 24 | fits | 145,791 | 226 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 299,868 | 2.999 | 20 | 50 | fits | 145,791 | 226 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 410,118 | 4.101 | 20 | 50 | fits | 110,646 | 164 | 0.414 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 507,636 | 5.076 | 20 | 20 | fits | 89,401 | 37 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 914,970 | 9.150 | 20 | 20 | fits | 64,371 | 24 | 0.599 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 372,299 | 3.723 | 20 | 20 | fits | 121,933 | 176 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 293,535 | 2.935 | 20 | 200 | fits | 146,438 | 227 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 423,323 | 4.233 | 20 | 200 | fits | 121,933 | 176 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 294,459 | 2.945 | 20 | 20 | fits | 146,438 | 227 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 424,027 | 4.240 | 20 | 20 | fits | 121,933 | 176 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 151,661 | 1.517 | 20 | 24 | fits | 149,482 | 152 | 0.329 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 297,109 | 2.971 | 20 | 24 | fits | 146,438 | 227 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 297,043 | 2.970 | 20 | 50 | fits | 146,438 | 227 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 427,051 | 4.271 | 20 | 50 | fits | 121,933 | 176 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 508,108 | 5.081 | 20 | 20 | fits | 81,123 | 24 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 915,241 | 9.152 | 20 | 20 | fits | 64,371 | 24 | 0.599 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 358,470 | 3.585 | 20 | 20 | fits | 120,970 | 175 | 0.442 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 296,633 | 2.966 | 20 | 200 | fits | 146,235 | 231 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 416,987 | 4.170 | 20 | 200 | fits | 120,970 | 175 | 0.442 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 297,557 | 2.976 | 20 | 20 | fits | 146,235 | 231 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 417,691 | 4.177 | 20 | 20 | fits | 120,970 | 175 | 0.442 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 147,573 | 1.476 | 20 | 24 | fits | 149,583 | 153 | 0.330 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 300,207 | 3.002 | 20 | 24 | fits | 146,235 | 231 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 300,141 | 3.001 | 20 | 50 | fits | 146,235 | 231 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 420,715 | 4.207 | 20 | 50 | fits | 120,970 | 175 | 0.442 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 501,661 | 5.017 | 20 | 20 | fits | 81,012 | 24 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 908,963 | 9.090 | 20 | 20 | fits | 64,540 | 25 | 0.600 |
| LINK_UP | `adp.link_up.if0` | 2,540 | 0.025 | 20 | 200 | fits | 25,773 | 43 (11) | 0.717 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,033 | 0.150 | 20 | 200 | fits | 21,240 | 23 (39) | 0.714 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 5,810 | 0.058 | 20 | 200 | fits | 2,558 | 10 (11) | 0.556 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 152,307 | 1.523 | 20 | 200 | fits | 153,247 | 241 | 0.457 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 227,688 | 2.277 | 20 | 20 | fits | 95,518 | 91 | 0.627 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 287,387 | 2.874 | 20 | 24 | fits | 86,712 | 55 | 0.569 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 188,213 | 1.882 | 20 | 50 | fits | 95,518 | 91 | 0.627 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 832,877 | 8.329 | 20 | 20 | fits | 86,786 | 32 | 0.548 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 247,762 | 2.478 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 152,307 | 1.523 | 20 | 200 | fits | 153,247 | 241 | 0.457 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 304,429 | 3.044 | 20 | 20 | fits | 88,766 | 41 | 0.639 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 297,546 | 2.975 | 20 | 24 | fits | 87,970 | 61 | 0.557 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 176,188 | 1.762 | 20 | 50 | fits | 145,670 | 257 | 0.357 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 881,329 | 8.813 | 20 | 20 | fits | 45,405 | 22 | 0.730 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 245,947 | 2.459 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 12,573 | 0.126 | 20 | 20 | fits | 26,925 | 21 (35) | 0.801 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 18,121 | 0.181 | 20 | 20 | fits | 24,590 | 17 (14) | 0.853 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 15,256 | 0.153 | 20 | 20 | fits | 23,815 | 18 (14) | 0.846 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 19,720 | 0.197 | 20 | 20 | fits | 27,464 | 21 (35) | 0.809 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 87,889 | 0.879 | 20 | 20 | fits | 28,177 | 8 | 0.819 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 44,887 | 0.449 | 20 | 20 | fits | 44,953 | 12 | 0.887 |
| malformed MRPDU discard | `srp.malformed.if0` | 20,861 | 0.209 | 20 | 20 | fits | 20,927 | 12 | 0.674 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 98,097 | 0.981 | 220 | 220 | fits | 68,972 | 6 | 0.873 |
| an event behind 15 others | `backlog.event.if0` | 169,159 | 1.692 | 20 | 200 | fits | 53,798 | 78 | 0.522 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 428,676 | 4.287 | 20 | 20 | fits | 45,331 | 63 | 0.325 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 423,429 | 4.234 | 20 | 200 | fits | 147,596 | 157 | 0.394 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 422,813 | 4.228 | 20 | 200 | fits | 147,596 | 157 | 0.394 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 419,107 | 4.191 | 20 | 20 | fits | 147,596 | 157 | 0.394 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 463,602 | 4.636 | 20 | 20 | fits | 45,331 | 63 | 0.325 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 154,806 | 1.548 | 20 | 24 | fits | 155,697 | 158 | 0.348 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 421,757 | 4.218 | 20 | 24 | fits | 147,596 | 157 | 0.394 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 421,691 | 4.217 | 20 | 50 | fits | 147,596 | 157 | 0.394 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 421,295 | 4.213 | 20 | 50 | fits | 147,596 | 157 | 0.394 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 466,560 | 4.666 | 20 | 20 | fits | 45,331 | 63 | 0.325 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 533,528 | 5.335 | 20 | 20 | fits | 27,481 | 41 | 0.173 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 353,766 | 3.538 | 20 | 20 | fits | 114,301 | 170 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 290,298 | 2.903 | 20 | 200 | fits | 145,361 | 227 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 412,425 | 4.124 | 20 | 200 | fits | 114,301 | 170 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 291,222 | 2.912 | 20 | 20 | fits | 145,361 | 227 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 413,129 | 4.131 | 20 | 20 | fits | 114,301 | 170 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 149,501 | 1.495 | 20 | 24 | fits | 149,687 | 155 | 0.332 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 293,872 | 2.939 | 20 | 24 | fits | 145,361 | 227 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 293,806 | 2.938 | 20 | 50 | fits | 145,361 | 227 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 416,153 | 4.162 | 20 | 50 | fits | 114,301 | 170 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 496,891 | 4.969 | 20 | 20 | fits | 80,804 | 24 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 911,589 | 9.116 | 20 | 20 | fits | 75,473 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 20,470 | 0.205 | 20 | 20 | fits | 25,654 | 19 | 0.800 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 290,298 | 2.903 | 20 | 200 | fits | 145,361 | 227 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 37,637 | 0.376 | 20 | 200 | fits | 25,654 | 19 | 0.800 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 291,222 | 2.912 | 20 | 20 | fits | 145,361 | 227 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 402,971 | 4.030 | 20 | 20 | fits | 104,143 | 160 | 0.401 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 149,501 | 1.495 | 20 | 24 | fits | 149,687 | 155 | 0.332 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 293,872 | 2.939 | 20 | 24 | fits | 145,361 | 227 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 293,806 | 2.938 | 20 | 50 | fits | 145,361 | 227 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 405,995 | 4.060 | 20 | 50 | fits | 104,143 | 160 | 0.401 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 486,308 | 4.863 | 20 | 20 | fits | 80,379 | 24 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 900,546 | 9.005 | 20 | 20 | fits | 75,473 | 28 | 0.558 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,281,148 | 62.811 | 20 | 20 | MISS ceiling | 17,268 | 13 | 0.615 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,298,352 | 62.984 | 20 | 20 | MISS ceiling | 17,280 | 13 | 0.623 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,315,478 | 63.155 | 20 | 20 | MISS ceiling | 17,183 | 13 | 0.632 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,332,578 | 63.326 | 20 | 20 | MISS ceiling | 17,176 | 13 | 0.632 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,349,684 | 63.497 | 20 | 20 | MISS ceiling | 17,097 | 13 | 0.627 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 151,255 | 1.513 | 20 | 200 | fits | 149,023 | 222 | 0.395 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 243,386 | 2.434 | 20 | 200 | fits | 92,747 | 164 | 0.381 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 146,933 | 1.469 | 20 | 20 | fits | 149,023 | 222 | 0.395 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,198,577 | 61.986 | 20 | 20 | MISS ceiling | 28,058 | 15 | 0.744 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 150,573 | 1.506 | 20 | 24 | fits | 149,023 | 222 | 0.395 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,174,005 | 61.740 | 20 | 24 | MISS ceiling | 138,856 | 106 | 0.396 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 149,517 | 1.495 | 20 | 50 | fits | 149,023 | 222 | 0.395 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 241,868 | 2.419 | 20 | 50 | fits | 92,747 | 164 | 0.381 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 322,904 | 3.229 | 20 | 20 | fits | 81,102 | 24 | 0.768 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 741,271 | 7.413 | 20 | 20 | fits | 76,231 | 28 | 0.568 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,987 | 0.060 | 20 | 20 | fits | 22,553 | 13 (29) | 0.767 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,443 | 0.074 | 20 | 20 | fits | 24,891 | 19 (35) | 0.787 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 16,345 | 0.163 | 20 | 20 | fits | 27,129 | 21 (12) | 0.804 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 10,512 | 0.105 | 20 | 50 | fits | 25,773 | 43 | 0.717 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 13,583 | 0.136 | 20 | 50 | fits | 22,111 | 35 | 0.691 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 15,022 | 0.150 | 20 | 50 | fits | 21,902 | 35 | 0.688 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 14,722 | 0.147 | 20 | 50 | fits | 27,700 | 61 | 0.641 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 17,109 | 0.171 | 20 | 50 | fits | 27,700 | 61 | 0.641 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 9,671 | 0.097 | 20 | 50 | fits | 20,330 | 30 | 0.602 |
| LINK_UP | `adp.link_up.if0` | 2,540 | 0.025 | 20 | 200 | fits | 25,773 | 43 (11) | 0.717 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,033 | 0.150 | 20 | 200 | fits | 21,240 | 23 (39) | 0.714 |
| LINK_DOWN | `adp.link_down.if0` | 2,177 | 0.022 | 20 | 200 | fits | 24,646 | 23 (9) | 0.767 |
| LINK_UP | `adp.link_up.if0` | 2,540 | 0.025 | 20 | 200 | fits | 25,773 | 43 (11) | 0.717 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,033 | 0.150 | 20 | 200 | fits | 21,240 | 23 (39) | 0.714 |
| GM_CHANGE | `adp.gm_change.if0` | 2,379 | 0.024 | 20 | 200 | fits | 15,551 | 17 (11) | 0.687 |
| LINK_UP | `adp.link_up.if0` | 2,540 | 0.025 | 20 | 200 | fits | 25,773 | 43 (11) | 0.717 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,033 | 0.150 | 20 | 200 | fits | 21,240 | 23 (39) | 0.714 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,913 | 0.049 | 20 | 200 | fits | 15,687 | 16 (31) | 0.633 |
| LINK_UP | `adp.link_up.if0` | 2,540 | 0.025 | 20 | 200 | fits | 25,773 | 43 (11) | 0.717 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,033 | 0.150 | 20 | 200 | fits | 21,240 | 23 (39) | 0.714 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,913 | 0.049 | 20 | 200 | fits | 15,687 | 16 (31) | 0.633 |
| set_name | `aecp_fanout.set_name.if0` | 54,790 | 0.548 | 20 | 24 | fits | 61,692 | 88 | 0.569 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 50,654 | 0.507 | 20 | 24 | fits | 55,411 | 77 | 0.598 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 56,300 | 0.563 | 20 | 24 | fits | 53,563 | 78 | 0.563 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 47,019 | 0.470 | 20 | 24 | fits | 49,283 | 77 | 0.533 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 60,692 | 0.607 | 20 | 24 | fits | 60,481 | 66 | 0.638 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 201,281 | 2.013 | 20 | 24 | fits | 57,869 | 65 | 0.628 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 235,043 | 2.350 | 20 | 24 | fits | 59,386 | 73 | 0.609 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 47,004 | 0.470 | 20 | 24 | fits | 49,251 | 77 | 0.551 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 53,027 | 0.530 | 20 | 24 | fits | 48,976 | 78 | 0.540 |
| BIND_RX | `acmp.bind_rx.if0` | 17,995 | 0.180 | 20 | 20 | fits | 39,315 | 26 (77) | 0.791 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,441 | 0.094 | 20 | 20 | fits | 30,682 | 19 (32) | 0.827 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,650 | 0.106 | 20 | 20 | fits | 23,706 | 15 (47) | 0.752 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,378 | 0.134 | 20 | 20 | fits | 38,541 | 18 (50) | 0.838 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,545 | 0.105 | 20 | 20 | fits | 24,703 | 17 (48) | 0.756 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,779 | 0.098 | 20 | 20 | fits | 22,769 | 16 (48) | 0.701 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 8,786 | 0.088 | 20 | 20 | fits | 22,305 | 16 (48) | 0.701 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,028 | 0.090 | 20 | 20 | fits | 22,286 | 16 (48) | 0.701 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 16,030 | 0.160 | 20 | 24 | fits | 27,234 | 20 | 0.788 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 28,449 | 0.284 | 20 | 24 | fits | 31,043 | 20 | 0.721 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 18,802 | 0.188 | 20 | 24 | fits | 26,238 | 20 | 0.725 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 10,609 | 0.106 | 20 | 24 | fits | 26,572 | 20 | 0.732 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 24,912 | 0.249 | 20 | 24 | fits | 27,339 | 20 | 0.736 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 19,321 | 0.193 | 20 | 24 | fits | 26,570 | 20 | 0.719 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 10,595 | 0.106 | 20 | 24 | fits | 26,107 | 20 | 0.733 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 18,719 | 0.187 | 20 | 24 | fits | 26,077 | 20 | 0.740 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 9,815 | 0.098 | 20 | 24 | fits | 25,630 | 20 | 0.749 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 21,104 | 0.211 | 20 | 24 | fits | 28,237 | 21 | 0.640 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 9,888 | 0.099 | 20 | 24 | fits | 25,382 | 20 | 0.766 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 23,622 | 0.236 | 20 | 24 | fits | 25,767 | 20 | 0.767 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 18,599 | 0.186 | 20 | 24 | fits | 25,911 | 20 | 0.726 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 24,829 | 0.248 | 20 | 24 | fits | 27,289 | 20 | 0.740 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 18,658 | 0.187 | 20 | 24 | fits | 26,102 | 20 | 0.740 |
| get_configuration | `aecp.get_configuration.if0` | 22,039 | 0.220 | 20 | 24 | fits | 23,868 | 20 | 0.755 |
| entity_available | `aecp.entity_available.if0` | 16,528 | 0.165 | 20 | 24 | fits | 23,342 | 20 | 0.732 |
| get_name | `aecp.get_name.if0` | 24,452 | 0.245 | 20 | 24 | fits | 26,942 | 20 | 0.766 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 25,620 | 0.256 | 20 | 24 | fits | 27,978 | 27 | 0.737 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 20,256 | 0.203 | 20 | 24 | fits | 27,680 | 29 | 0.752 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 9,117 | 0.091 | 20 | 24 | fits | 24,758 | 20 | 0.772 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 16,644 | 0.166 | 20 | 24 | fits | 23,533 | 20 | 0.739 |
| set_name | `aecp.set_name.if0` | 26,584 | 0.266 | 20 | 24 | fits | 43,260 | 42 | 0.757 |
| lock_entity | `aecp.lock_entity.if0` | 21,668 | 0.217 | 20 | 24 | fits | 33,503 | 33 | 0.763 |
| unlock_entity | `aecp.unlock_entity.if0` | 23,727 | 0.237 | 20 | 24 | fits | 34,725 | 32 | 0.778 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 138,091 | 1.381 | 20 | 24 | fits | 144,997 | 91 | 0.326 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 159,961 | 1.600 | 20 | 24 | fits | 137,757 | 70 | 0.308 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 139,622 | 1.396 | 20 | 24 | fits | 40,300 | 17 | 0.687 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 282,512 | 2.825 | 20 | 24 | fits | 91,724 | 18 | 0.670 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 245,736 | 2.457 | 20 | 24 | fits | 101,688 | 32 | 0.678 |
| LINK_UP | `fixture.link_up.if0` | 2,540 | 0.025 | 20 | 200 | fits | 25,773 | 43 (11) | 0.717 |
| malformed MRPDU discard | `fixture.malformed.if0` | 21,572 | 0.216 | 20 | 20 | fits | 21,638 | 12 | 0.738 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 32,093 | 0.321 | 20 | 24 | fits | 45,621 | 42 | 0.774 |
| LINK_DOWN | `fixture.link_down.if0` | 2,576 | 0.026 | 20 | 200 | fits | 26,629 | 23 (9) | 0.786 |
| BIND_RX | `fixture.bind_rx.if0` | 19,062 | 0.191 | 20 | 20 | fits | 40,715 | 26 (77) | 0.802 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 12,690 | 0.127 | 20 | 20 | fits | 34,479 | 29 (35) | 0.776 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 7,563 | 0.076 | 20 | 20 | fits | 23,959 | 13 (29) | 0.806 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 82,087 | 0.821 | 20 | 200 | fits | 82,191 | 49 | 0.748 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 82,087 | 0.821 | 20 | 200 | fits | 82,191 | 49 | 0.748 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 81,813 | 0.818 | 20 | 20 | fits | 82,191 | 49 | 0.748 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 81,813 | 0.818 | 20 | 20 | fits | 82,191 | 49 | 0.748 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 82,021 | 0.820 | 20 | 24 | fits | 82,191 | 49 | 0.748 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 82,021 | 0.820 | 20 | 24 | fits | 82,191 | 49 | 0.748 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 81,955 | 0.820 | 20 | 50 | fits | 82,191 | 49 | 0.748 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 81,955 | 0.820 | 20 | 50 | fits | 82,191 | 49 | 0.748 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 81,889 | 0.819 | 20 | 20 | fits | 82,191 | 49 | 0.748 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 81,889 | 0.819 | 20 | 20 | fits | 82,191 | 49 | 0.748 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
