### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 92 paths and 7 of 950 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.195 (0.419) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.095 (0.239) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.072 (0.268) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.145 (0.527) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.107 (0.263) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.089 (0.239) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.100 (0.247) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.105 (0.262) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.095 (0.329) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.234 (0.601) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.197 (0.565) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.234 (0.697) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.065 (0.485) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.194 (0.641) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.138 (0.507) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.135 (0.396) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.051 (0.172) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.024 (0.180) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.029 (0.272) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.028 (0.277) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.091 (0.262) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.084 (0.422) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.222 (0.546) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.209 (0.534) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.221 (0.544) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.255 (0.585) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.199 (0.520) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.286 (0.662) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.094 (0.409) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.291 (0.628) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.202 (0.527) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.197 (0.520) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.240 (0.571) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.220 (0.541) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.238 (0.571) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.237 (0.569) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.246 (0.579) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.194 (0.517) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.249 (0.582) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.197 (0.523) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.248 (0.576) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.205 (0.544) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.246 (0.578) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.176 (0.502) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.265 (0.699) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.230 (0.559) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.249 (0.630) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 3.264 (3.588) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.494 (0.793) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.598 (0.925) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.523 (0.894) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.577 (0.873) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.590 (0.839) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.321 (3.635) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.500 (0.797) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 3.043 (3.386) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.043 (2.421) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.823 (4.192) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 2.967 (3.337) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.421 (1.675) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.221 (4.581) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 4.468 (5.111) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.168 (0.533) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.612 (2.050) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.917 (63.061) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.665 (63.811) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.316 (0.469) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 2.300 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 1.558 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 3.021 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 1.905 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 9.868 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.176 (0.522) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.096 (0.226) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.104 (0.277) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.153 (0.522) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.162 (0.498) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.738 | fits | 0 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.131 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.013 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.174 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 4.959 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.118 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.753 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.156 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.maap.last.if0` (backlog-adp@program-aged2-7) | 4.997 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-6.service.srp.first.if0` (backlog-adp@blank-aged2-6) | 5.889 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-1.service.srp.last.if0` (backlog-adp@blank-aged2-1) | 10.956 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.891 (0.984) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.452 (0.453) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.226 (0.226) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.785 (0.864) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.985 | 11 | 150,760 (1.508) | yes | - |
| backlog-adp@blank-1 | 0 | 11.395 | 11 | 148,169 (1.482) | yes | - |
| backlog-adp@blank-2 | 0 | 11.283 | 10 | 149,516 (1.495) | yes | - |
| backlog-adp@blank-3 | 0 | 11.804 | 13 | 148,366 (1.484) | yes | - |
| backlog-adp@blank-4 | 0 | 11.845 | 13 | 151,493 (1.515) | yes | - |
| backlog-adp@blank-5 | 0 | 11.515 | 13 | 149,585 (1.496) | yes | - |
| backlog-adp@blank-6 | 0 | 11.438 | 11 | 149,177 (1.492) | yes | - |
| backlog-adp@blank-7 | 0 | 13.202 | 14 | 148,865 (1.489) | yes | - |
| backlog-adp@program-0 | 0 | 11.446 | 11 | 149,489 (1.495) | yes | - |
| backlog-adp@program-1 | 0 | 11.538 | 12 | 150,780 (1.508) | yes | - |
| backlog-adp@program-2 | 0 | 11.334 | 11 | 150,707 (1.507) | yes | - |
| backlog-adp@program-3 | 0 | 12.035 | 12 | 147,765 (1.478) | yes | - |
| backlog-adp@program-4 | 0 | 10.654 | 11 | 149,794 (1.498) | yes | - |
| backlog-adp@program-5 | 0 | 10.613 | 11 | 150,641 (1.506) | yes | - |
| backlog-adp@program-6 | 0 | 10.554 | 10 | 149,577 (1.496) | yes | - |
| backlog-adp@program-7 | 0 | 11.073 | 13 | 148,029 (1.480) | yes | - |
| backlog-adp@verify-0 | 0 | 11.698 | 11 | 149,475 (1.495) | yes | - |
| backlog-adp@verify-1 | 0 | 11.447 | 11 | 148,277 (1.483) | yes | - |
| backlog-adp@verify-2 | 0 | 11.314 | 11 | 150,775 (1.508) | yes | - |
| backlog-adp@verify-3 | 0 | 11.851 | 13 | 148,474 (1.485) | yes | - |
| backlog-adp@verify-4 | 0 | 11.407 | 11 | 152,251 (1.523) | yes | - |
| backlog-adp@verify-5 | 1 | 11.296 | 10 | 149,464 (1.495) | yes | - |
| backlog-adp@verify-6 | 0 | 11.353 | 11 | 150,810 (1.508) | yes | - |
| backlog-adp@verify-7 | 0 | 12.507 | 12 | 148,804 (1.488) | yes | - |
| backlog-adp@blank-aged2-0 | 1 | 11.602 | 12 | 151,325 (1.513) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 11.495 | 12 | 149,193 (1.492) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 11.471 | 12 | 153,781 (1.538) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 11.308 | 11 | 150,646 (1.506) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 11.267 | 10 | 149,439 (1.494) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 11.344 | 11 | 150,646 (1.506) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 11.295 | 11 | 148,079 (1.481) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 12.690 | 14 | 148,837 (1.488) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 12.265 | 14 | 147,870 (1.479) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 12.558 | 15 | 150,603 (1.506) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 12.448 | 15 | 149,326 (1.493) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 12.088 | 13 | 152,016 (1.520) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 12.047 | 13 | 150,259 (1.503) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 12.000 | 13 | 147,668 (1.477) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 11.959 | 11 | 151,644 (1.516) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 12.572 | 15 | 149,738 (1.497) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.393 | 12 | 151,696 (1.517) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 11.397 | 11 | 147,884 (1.479) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 11.356 | 11 | 150,499 (1.505) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 11.312 | 10 | 150,568 (1.506) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 12.164 | 13 | 150,499 (1.505) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 11.641 | 13 | 149,472 (1.495) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 11.449 | 12 | 149,473 (1.495) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 11.697 | 12 | 148,893 (1.489) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 11.907 | 13 | 149,653 (1.497) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 11.528 | 12 | 150,748 (1.507) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 11.492 | 12 | 153,963 (1.540) | yes | - |
| backlog-adp@program-aged1-3 | 1 | 11.329 | 10 | 151,784 (1.518) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 11.450 | 11 | 147,809 (1.478) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 11.381 | 11 | 150,424 (1.504) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 11.320 | 11 | 149,133 (1.491) | yes | - |
| backlog-adp@program-aged1-7 | 1 | 11.856 | 12 | 149,380 (1.494) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.374 | 12 | 148,168 (1.482) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 11.353 | 11 | 150,816 (1.508) | yes | - |
| backlog-adp@verify-aged2-2 | 1 | 11.273 | 10 | 150,885 (1.509) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 11.722 | 13 | 151,163 (1.512) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 11.463 | 12 | 150,953 (1.510) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 11.415 | 12 | 149,405 (1.494) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 11.294 | 10 | 151,989 (1.520) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 12.354 | 12 | 148,586 (1.486) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 11.496 | 12 | 150,953 (1.510) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 11.325 | 11 | 148,080 (1.481) | yes | - |
| backlog-adp@verify-aged1-2 | 1 | 11.283 | 10 | 152,055 (1.521) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 11.405 | 11 | 148,164 (1.482) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 11.343 | 11 | 150,695 (1.507) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 11.702 | 13 | 149,668 (1.497) | yes | - |
| backlog-adp@verify-aged1-6 | 1 | 11.397 | 11 | 149,360 (1.494) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 12.501 | 12 | 149,076 (1.491) | yes | - |
| backlog | 0 | 5.685 | 7 | 151,768 (1.518) | yes | - |
| backlog-adp | 0 | 10.515 | 11 | 149,212 (1.492) | yes | - |
| backlog-adp-refill | 0 | 40.858 | 26 | 149,212 (1.492) | yes | - |
| backlog-owed | 0 | 64.324 | 26 | 148,431 (1.484) | yes | - |
| fixture | 0 | 1.318 | 2 | 81,717 (0.817) | yes | - |

Composed maximum over the 4 backlog windows: 151,768 CPU cycles (1.518 ms), backlog.
Over the windows that released their whole load only: 151,768 (1.518 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3609 | 0 | 41,273 (0.413) | fits |
| save-second | 44069 | 0 | 50,835 (0.508) | fits |
| backlog-adp@blank-0 | 416 | 0 | 150,760 (1.508) | fits |
| backlog-adp@blank-1 | 416 | 0 | 148,169 (1.482) | fits |
| backlog-adp@blank-2 | 416 | 0 | 151,219 (1.512) | fits |
| backlog-adp@blank-3 | 418 | 0 | 148,366 (1.484) | fits |
| backlog-adp@blank-4 | 418 | 0 | 151,493 (1.515) | fits |
| backlog-adp@blank-5 | 418 | 0 | 149,585 (1.496) | fits |
| backlog-adp@blank-6 | 418 | 0 | 149,177 (1.492) | fits |
| backlog-adp@blank-7 | 421 | 0 | 148,865 (1.489) | fits |
| backlog-adp@program-0 | 519 | 0 | 149,489 (1.495) | fits |
| backlog-adp@program-1 | 520 | 0 | 150,780 (1.508) | fits |
| backlog-adp@program-2 | 521 | 0 | 150,707 (1.507) | fits |
| backlog-adp@program-3 | 522 | 0 | 147,765 (1.478) | fits |
| backlog-adp@program-4 | 522 | 0 | 149,794 (1.498) | fits |
| backlog-adp@program-5 | 524 | 0 | 150,641 (1.506) | fits |
| backlog-adp@program-6 | 524 | 0 | 151,390 (1.514) | fits |
| backlog-adp@program-7 | 526 | 0 | 148,029 (1.480) | fits |
| backlog-adp@verify-0 | 614 | 0 | 149,475 (1.495) | fits |
| backlog-adp@verify-1 | 614 | 0 | 148,277 (1.483) | fits |
| backlog-adp@verify-2 | 614 | 0 | 150,775 (1.508) | fits |
| backlog-adp@verify-3 | 616 | 0 | 148,474 (1.485) | fits |
| backlog-adp@verify-4 | 615 | 0 | 152,251 (1.523) | fits |
| backlog-adp@verify-5 | 615 | 0 | 149,464 (1.495) | fits |
| backlog-adp@verify-6 | 616 | 0 | 150,810 (1.508) | fits |
| backlog-adp@verify-7 | 617 | 0 | 148,804 (1.488) | fits |
| backlog-adp@blank-aged2-0 | 697 | 0 | 151,325 (1.513) | fits |
| backlog-adp@blank-aged2-1 | 702 | 0 | 149,193 (1.492) | fits |
| backlog-adp@blank-aged2-2 | 709 | 0 | 153,781 (1.538) | fits |
| backlog-adp@blank-aged2-3 | 715 | 0 | 150,646 (1.506) | fits |
| backlog-adp@blank-aged2-4 | 722 | 0 | 149,439 (1.494) | fits |
| backlog-adp@blank-aged2-5 | 730 | 0 | 150,646 (1.506) | fits |
| backlog-adp@blank-aged2-6 | 737 | 0 | 148,079 (1.481) | fits |
| backlog-adp@blank-aged2-7 | 747 | 0 | 148,837 (1.488) | fits |
| backlog-adp@blank-aged1-0 | 641 | 0 | 147,870 (1.479) | fits |
| backlog-adp@blank-aged1-1 | 649 | 0 | 150,603 (1.506) | fits |
| backlog-adp@blank-aged1-2 | 656 | 0 | 149,326 (1.493) | fits |
| backlog-adp@blank-aged1-3 | 662 | 0 | 152,016 (1.520) | fits |
| backlog-adp@blank-aged1-4 | 669 | 0 | 150,259 (1.503) | fits |
| backlog-adp@blank-aged1-5 | 676 | 0 | 147,668 (1.477) | fits |
| backlog-adp@blank-aged1-6 | 682 | 0 | 151,644 (1.516) | fits |
| backlog-adp@blank-aged1-7 | 693 | 0 | 149,738 (1.497) | fits |
| backlog-adp@program-aged2-0 | 796 | 0 | 151,696 (1.517) | fits |
| backlog-adp@program-aged2-1 | 802 | 0 | 147,884 (1.479) | fits |
| backlog-adp@program-aged2-2 | 809 | 0 | 150,499 (1.505) | fits |
| backlog-adp@program-aged2-3 | 816 | 0 | 150,568 (1.506) | fits |
| backlog-adp@program-aged2-4 | 826 | 0 | 150,499 (1.505) | fits |
| backlog-adp@program-aged2-5 | 833 | 0 | 149,472 (1.495) | fits |
| backlog-adp@program-aged2-6 | 839 | 0 | 149,473 (1.495) | fits |
| backlog-adp@program-aged2-7 | 847 | 0 | 148,893 (1.489) | fits |
| backlog-adp@program-aged1-0 | 739 | 0 | 149,653 (1.497) | fits |
| backlog-adp@program-aged1-1 | 745 | 0 | 150,748 (1.507) | fits |
| backlog-adp@program-aged1-2 | 752 | 0 | 153,963 (1.540) | fits |
| backlog-adp@program-aged1-3 | 758 | 0 | 151,784 (1.518) | fits |
| backlog-adp@program-aged1-4 | 766 | 0 | 147,809 (1.478) | fits |
| backlog-adp@program-aged1-5 | 773 | 0 | 150,424 (1.504) | fits |
| backlog-adp@program-aged1-6 | 780 | 0 | 149,133 (1.491) | fits |
| backlog-adp@program-aged1-7 | 789 | 0 | 149,380 (1.494) | fits |
| backlog-adp@verify-aged2-0 | 893 | 0 | 148,168 (1.482) | fits |
| backlog-adp@verify-aged2-1 | 899 | 0 | 150,816 (1.508) | fits |
| backlog-adp@verify-aged2-2 | 906 | 0 | 150,885 (1.509) | fits |
| backlog-adp@verify-aged2-3 | 916 | 0 | 151,163 (1.512) | fits |
| backlog-adp@verify-aged2-4 | 922 | 0 | 150,953 (1.510) | fits |
| backlog-adp@verify-aged2-5 | 929 | 0 | 149,405 (1.494) | fits |
| backlog-adp@verify-aged2-6 | 935 | 0 | 151,989 (1.520) | fits |
| backlog-adp@verify-aged2-7 | 944 | 0 | 148,586 (1.486) | fits |
| backlog-adp@verify-aged1-0 | 835 | 0 | 150,953 (1.510) | fits |
| backlog-adp@verify-aged1-1 | 841 | 0 | 148,080 (1.481) | fits |
| backlog-adp@verify-aged1-2 | 848 | 0 | 152,055 (1.521) | fits |
| backlog-adp@verify-aged1-3 | 856 | 0 | 148,164 (1.482) | fits |
| backlog-adp@verify-aged1-4 | 863 | 0 | 150,695 (1.507) | fits |
| backlog-adp@verify-aged1-5 | 872 | 0 | 149,668 (1.497) | fits |
| backlog-adp@verify-aged1-6 | 878 | 0 | 149,360 (1.494) | fits |
| backlog-adp@verify-aged1-7 | 886 | 0 | 149,076 (1.491) | fits |
| adp-advertise | 598 | 0 | 30,345 (0.303) | fits |
| save-held | 1467 | 0 | 156,736 (1.567) | fits |
| save-starved | 23332 | 0 | 156,736 (1.567) | fits |
| acmp-noresp | 2023 | 0 | 41,273 (0.413) | fits |
| save | 610 | 0 | 45,232 (0.452) | fits |
| srp | 290 | 0 | 56,000 (0.560) | fits |
| backlog | 286 | 0 | 151,768 (1.518) | fits |
| backlog-adp | 314 | 0 | 149,212 (1.492) | fits |
| backlog-adp-refill | 329 | 0 | 149,212 (1.492) | fits |
| backlog-owed | 311 | 0 | 148,431 (1.484) | fits |
| acmp-disc | 937 | 0 | 41,273 (0.413) | fits |
| maap | 182 | 0 | 30,345 (0.303) | fits |
| adp-link | 89 | 0 | 39,951 (0.400) | fits |
| adp-gm | 88 | 0 | 30,345 (0.303) | fits |
| adp-discover | 88 | 0 | 30,345 (0.303) | fits |
| control | 88 | 0 | 30,345 (0.303) | fits |
| aecp-fanout | 113 | 0 | 63,569 (0.636) | fits |
| acmp-cmd | 85 | 0 | 41,273 (0.413) | fits |
| aecp | 111 | 0 | 44,791 (0.448) | fits |
| aecp-largest-notice | 107 | 0 | 147,151 (1.472) | fits |
| datapath-events | 116 | 0 | 30,345 (0.303) | fits |
| fixture | 151 | 0 | 81,717 (0.817) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | +10.001 ms, 77,332 (0.773 ms), read-back | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 9.964 (20) | 10.036 |
| backlog-adp@blank-aged2-1 | 2 | none | none | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 10.956 (20) | 9.044 |
| backlog-adp@blank-aged2-2 | 2 | none | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 10.934 (20) | 9.066 |
| backlog-adp@blank-aged2-3 | 2 | +6.560 ms, 77,338 (0.773 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 10.770 (20) | 9.230 |
| backlog-adp@blank-aged2-4 | 2 | none | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 10.728 (20) | 9.272 |
| backlog-adp@blank-aged2-5 | 2 | none | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 10.805 (20) | 9.195 |
| backlog-adp@blank-aged2-6 | 2 | none | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 10.754 (20) | 9.246 |
| backlog-adp@blank-aged2-7 | 2 | none | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 10.708 (20) | 9.292 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 10.020 (20) | 9.980 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 10.424 (20) | 9.576 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 10.662 (20) | 9.338 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 10.792 (20) | 9.208 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 10.750 (20) | 9.250 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 10.703 (20) | 9.297 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 10.655 (20) | 9.345 |
| backlog-adp@blank-aged1-7 | 1 | none | +10.983 ms, 77,014 (0.770 ms), read-back | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 10.731 (20) | 9.269 |
| backlog-adp@program-aged2-0 | 2 | none | +10.237 ms, 80,810 (0.808 ms), issue | `backlog-adp@program-aged2-0.service.srp.last.if0` | 9.842 (20) | 10.158 |
| backlog-adp@program-aged2-1 | 2 | +9.228 ms, 80,832 (0.808 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 10.857 (20) | 9.143 |
| backlog-adp@program-aged2-2 | 2 | +8.330 ms, 80,832 (0.808 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 10.816 (20) | 9.184 |
| backlog-adp@program-aged2-3 | 2 | +6.570 ms, 80,832 (0.808 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 10.772 (20) | 9.228 |
| backlog-adp@program-aged2-4 | 2 | +5.938 ms, 80,867 (0.809 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 10.874 (20) | 9.126 |
| backlog-adp@program-aged2-5 | 2 | +5.008 ms, 81,187 (0.812 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 10.795 (20) | 9.205 |
| backlog-adp@program-aged2-6 | 2 | +4.233 ms, 80,564 (0.806 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 10.911 (20) | 9.089 |
| backlog-adp@program-aged2-7 | 2 | +3.043 ms, 80,386 (0.804 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 10.899 (20) | 9.101 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 9.882 (20) | 10.118 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 10.184 (20) | 9.816 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 10.149 (20) | 9.851 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 9.985 (20) | 10.015 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 10.106 (20) | 9.894 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 10.037 (20) | 9.963 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 9.977 (20) | 10.023 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 9.947 (20) | 10.053 |
| backlog-adp@verify-aged2-0 | 2 | none | +10.256 ms, 77,563 (0.776 ms), read-back | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 10.005 (20) | 9.995 |
| backlog-adp@verify-aged2-1 | 2 | +9.213 ms, 77,655 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 10.812 (20) | 9.188 |
| backlog-adp@verify-aged2-2 | 2 | +8.398 ms, 77,738 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 10.732 (20) | 9.268 |
| backlog-adp@verify-aged2-3 | 2 | +6.825 ms, 77,825 (0.778 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 10.877 (20) | 9.123 |
| backlog-adp@verify-aged2-4 | 2 | +5.863 ms, 77,694 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 10.923 (20) | 9.077 |
| backlog-adp@verify-aged2-5 | 2 | +4.946 ms, 77,870 (0.779 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 10.876 (20) | 9.124 |
| backlog-adp@verify-aged2-6 | 2 | +4.095 ms, 77,745 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 10.754 (20) | 9.246 |
| backlog-adp@verify-aged2-7 | 2 | +3.010 ms, 77,522 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 10.844 (20) | 9.156 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 10.068 (20) | 9.932 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 10.022 (20) | 9.978 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 9.981 (20) | 10.019 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 10.102 (20) | 9.898 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 10.040 (20) | 9.960 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 9.970 (20) | 10.030 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 10.094 (20) | 9.906 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 10.075 (20) | 9.925 |

Least margin over the aged windows: 9.044 ms, `backlog-adp@blank-aged2-1.service.srp.last.if0` at 10.956 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.390 | 6,070 | 102 | 2 | 30.898 | yes | within |
| save-held | 2019.253 | 4,070 | 102 | - | 15.658 | no | within |
| save-starved | 4049.078 | 4,070 | 102 | - | 31.201 | yes | within |
| save | 2019.587 | 4,070 | 102 | - | 10.937 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 97,564 (0.976) | 78,523 (0.785) |
| save-second | 520 | 80,279 (0.803) | 78,195 (0.782) |
| backlog-adp@blank-0 | 299 | 92,868 (0.929) | 76,797 (0.768) |
| backlog-adp@blank-1 | 299 | 92,869 (0.929) | 76,797 (0.768) |
| backlog-adp@blank-2 | 299 | 92,859 (0.929) | 76,797 (0.768) |
| backlog-adp@blank-3 | 299 | 93,204 (0.932) | 76,797 (0.768) |
| backlog-adp@blank-4 | 299 | 93,372 (0.934) | 76,749 (0.767) |
| backlog-adp@blank-5 | 299 | 91,817 (0.918) | 76,722 (0.767) |
| backlog-adp@blank-6 | 299 | 92,822 (0.928) | 76,749 (0.767) |
| backlog-adp@blank-7 | 300 | 97,381 (0.974) | 76,749 (0.767) |
| backlog-adp@program-0 | 328 | 97,010 (0.970) | 79,266 (0.793) |
| backlog-adp@program-1 | 328 | 99,060 (0.991) | 79,307 (0.793) |
| backlog-adp@program-2 | 328 | 97,008 (0.970) | 79,314 (0.793) |
| backlog-adp@program-3 | 329 | 97,008 (0.970) | 79,314 (0.793) |
| backlog-adp@program-4 | 329 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@program-5 | 329 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@program-6 | 329 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@program-7 | 329 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-0 | 355 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-1 | 355 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-2 | 355 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-3 | 355 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-4 | 355 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-5 | 355 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-6 | 355 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-7 | 356 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@blank-aged2-0 | 297 | 77,332 (0.773) | 76,232 (0.762) |
| backlog-adp@blank-aged2-1 | 297 | 86,472 (0.865) | 76,460 (0.765) |
| backlog-adp@blank-aged2-2 | 297 | 86,576 (0.866) | 76,460 (0.765) |
| backlog-adp@blank-aged2-3 | 297 | 77,338 (0.773) | 76,232 (0.762) |
| backlog-adp@blank-aged2-4 | 297 | 86,353 (0.864) | 76,478 (0.765) |
| backlog-adp@blank-aged2-5 | 297 | 86,443 (0.864) | 76,395 (0.764) |
| backlog-adp@blank-aged2-6 | 297 | 85,527 (0.855) | 76,249 (0.762) |
| backlog-adp@blank-aged2-7 | 298 | 92,546 (0.925) | 76,593 (0.766) |
| backlog-adp@blank-aged1-0 | 297 | 97,854 (0.979) | 76,593 (0.766) |
| backlog-adp@blank-aged1-1 | 297 | 97,978 (0.980) | 76,643 (0.766) |
| backlog-adp@blank-aged1-2 | 297 | 93,566 (0.936) | 76,723 (0.767) |
| backlog-adp@blank-aged1-3 | 297 | 92,739 (0.927) | 76,768 (0.768) |
| backlog-adp@blank-aged1-4 | 297 | 92,819 (0.928) | 76,750 (0.767) |
| backlog-adp@blank-aged1-5 | 297 | 92,830 (0.928) | 76,750 (0.767) |
| backlog-adp@blank-aged1-6 | 297 | 93,031 (0.930) | 76,750 (0.767) |
| backlog-adp@blank-aged1-7 | 297 | 77,014 (0.770) | 76,068 (0.761) |
| backlog-adp@program-aged2-0 | 326 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@program-aged2-1 | 326 | 97,008 (0.970) | 78,843 (0.788) |
| backlog-adp@program-aged2-2 | 326 | 97,008 (0.970) | 78,843 (0.788) |
| backlog-adp@program-aged2-3 | 326 | 97,008 (0.970) | 78,843 (0.788) |
| backlog-adp@program-aged2-4 | 326 | 97,008 (0.970) | 78,795 (0.788) |
| backlog-adp@program-aged2-5 | 326 | 97,008 (0.970) | 78,917 (0.789) |
| backlog-adp@program-aged2-6 | 326 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@program-aged2-7 | 327 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@program-aged1-0 | 326 | 97,008 (0.970) | 79,237 (0.792) |
| backlog-adp@program-aged1-1 | 326 | 97,008 (0.970) | 79,287 (0.793) |
| backlog-adp@program-aged1-2 | 326 | 97,008 (0.970) | 79,332 (0.793) |
| backlog-adp@program-aged1-3 | 326 | 97,008 (0.970) | 79,314 (0.793) |
| backlog-adp@program-aged1-4 | 326 | 97,008 (0.970) | 79,314 (0.793) |
| backlog-adp@program-aged1-5 | 326 | 97,008 (0.970) | 79,314 (0.793) |
| backlog-adp@program-aged1-6 | 326 | 97,008 (0.970) | 79,314 (0.793) |
| backlog-adp@program-aged1-7 | 327 | 97,008 (0.970) | 79,314 (0.793) |
| backlog-adp@verify-aged2-0 | 355 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-aged2-1 | 355 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-aged2-2 | 355 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-aged2-3 | 355 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-aged2-4 | 355 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-aged2-5 | 355 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-aged2-6 | 355 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-aged2-7 | 356 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-aged1-0 | 355 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-aged1-1 | 355 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-aged1-2 | 355 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-aged1-3 | 355 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-aged1-4 | 355 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-aged1-5 | 355 | 100,454 (1.005) | 78,650 (0.786) |
| backlog-adp@verify-aged1-6 | 355 | 97,008 (0.970) | 78,650 (0.786) |
| backlog-adp@verify-aged1-7 | 356 | 97,008 (0.970) | 78,650 (0.786) |
| adp-advertise | 577 | 22,804 (0.228) | 2,786 (0.028) |
| save-held | 722 | 95,943 (0.959) | 79,034 (0.790) |
| save-starved | 418 | 81,231 (0.812) | 78,635 (0.786) |
| acmp-noresp | 615 | 96,841 (0.968) | 78,523 (0.785) |
| save | 585 | 95,959 (0.960) | 78,523 (0.785) |
| srp | 271 | 22,787 (0.228) | 2,786 (0.028) |
| backlog | 265 | 22,787 (0.228) | 2,786 (0.028) |
| backlog-adp | 271 | 22,787 (0.228) | 2,894 (0.029) |
| backlog-adp-refill | 274 | 22,787 (0.228) | 2,894 (0.029) |
| backlog-owed | 276 | 22,787 (0.228) | 2,786 (0.028) |
| acmp-disc | 305 | 96,899 (0.969) | 78,523 (0.785) |
| maap | 169 | 22,763 (0.228) | 2,786 (0.028) |
| adp-link | 79 | 22,750 (0.228) | 2,786 (0.028) |
| adp-gm | 79 | 22,750 (0.228) | 2,786 (0.028) |
| adp-discover | 79 | 22,750 (0.228) | 2,786 (0.028) |
| control | 79 | 22,750 (0.228) | 2,786 (0.028) |
| aecp-fanout | 80 | 23,934 (0.239) | 4,349 (0.043) |
| acmp-cmd | 65 | 22,750 (0.228) | 2,786 (0.028) |
| aecp | 79 | 22,750 (0.228) | 2,786 (0.028) |
| aecp-largest-notice | 78 | 22,750 (0.228) | 2,786 (0.028) |
| datapath-events | 69 | 22,750 (0.228) | 2,786 (0.028) |
| fixture | 54 | 20,956 (0.210) | 2,817 (0.028) |

Longest pass that carries a step: 100,454 CPU cycles (1.005 ms), backlog-adp@verify-aged1-5; longest step: 79,332 (0.793 ms), backlog-adp@program-aged1-2.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 19,447 | 0.194 | 20 | 20 | fits | 35,699 | 19 (14) | 0.895 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 405,174 | 4.052 | 20 | 20 | fits | 109,638 | 184 | 0.397 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 358,027 | 3.580 | 20 | 200 | fits | 150,760 | 214 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 467,049 | 4.670 | 20 | 200 | fits | 109,638 | 184 | 0.397 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 358,951 | 3.590 | 20 | 20 | fits | 150,760 | 214 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 467,753 | 4.678 | 20 | 20 | fits | 109,638 | 184 | 0.397 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 211,831 | 2.118 | 20 | 24 | fits | 144,124 | 145 | 0.403 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 361,601 | 3.616 | 20 | 24 | fits | 150,760 | 214 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 361,535 | 3.615 | 20 | 50 | fits | 150,760 | 214 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 470,777 | 4.708 | 20 | 50 | fits | 109,638 | 184 | 0.397 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 557,062 | 5.571 | 20 | 20 | fits | 86,351 | 24 | 0.780 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,068,738 | 10.687 | 20 | 20 | fits | 80,241 | 30 | 0.710 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 352,179 | 3.522 | 20 | 20 | fits | 112,161 | 175 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 296,046 | 2.960 | 20 | 200 | fits | 148,169 | 225 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 407,591 | 4.076 | 20 | 200 | fits | 112,161 | 175 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 296,970 | 2.970 | 20 | 20 | fits | 148,169 | 225 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 408,295 | 4.083 | 20 | 20 | fits | 112,161 | 175 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 152,441 | 1.524 | 20 | 24 | fits | 143,694 | 145 | 0.399 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 299,620 | 2.996 | 20 | 24 | fits | 148,169 | 225 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 299,554 | 2.996 | 20 | 50 | fits | 148,169 | 225 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 411,319 | 4.113 | 20 | 50 | fits | 112,161 | 175 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 497,808 | 4.978 | 20 | 20 | fits | 86,555 | 24 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 1,009,690 | 10.097 | 20 | 20 | fits | 86,041 | 28 | 0.607 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 346,986 | 3.470 | 20 | 20 | fits | 102,196 | 172 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 294,522 | 2.945 | 20 | 200 | fits | 149,516 | 258 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 396,102 | 3.961 | 20 | 200 | fits | 102,196 | 172 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 295,446 | 2.954 | 20 | 20 | fits | 149,516 | 258 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 396,806 | 3.968 | 20 | 20 | fits | 102,196 | 172 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 149,570 | 1.496 | 20 | 24 | fits | 151,219 | 114 | 0.375 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 298,096 | 2.981 | 20 | 24 | fits | 149,516 | 258 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 298,030 | 2.980 | 20 | 50 | fits | 149,516 | 258 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 399,830 | 3.998 | 20 | 50 | fits | 102,196 | 172 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 490,739 | 4.907 | 20 | 20 | fits | 90,975 | 31 | 0.783 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 998,455 | 9.985 | 20 | 20 | fits | 73,407 | 24 | 0.646 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 361,298 | 3.613 | 20 | 20 | fits | 116,941 | 182 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 291,765 | 2.918 | 20 | 200 | fits | 148,366 | 226 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 417,530 | 4.175 | 20 | 200 | fits | 116,941 | 182 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 292,689 | 2.927 | 20 | 20 | fits | 148,366 | 226 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 418,234 | 4.182 | 20 | 20 | fits | 116,941 | 182 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 147,963 | 1.480 | 20 | 24 | fits | 143,636 | 145 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 295,339 | 2.953 | 20 | 24 | fits | 148,366 | 226 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 295,273 | 2.953 | 20 | 50 | fits | 148,366 | 226 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 421,258 | 4.213 | 20 | 50 | fits | 116,941 | 182 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 507,642 | 5.076 | 20 | 20 | fits | 86,450 | 24 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 1,002,767 | 10.028 | 20 | 20 | fits | 73,283 | 24 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 372,645 | 3.726 | 20 | 20 | fits | 111,153 | 187 | 0.399 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 300,868 | 3.009 | 20 | 200 | fits | 151,493 | 216 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 420,869 | 4.209 | 20 | 200 | fits | 111,153 | 187 | 0.399 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 301,792 | 3.018 | 20 | 20 | fits | 151,493 | 216 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 421,573 | 4.216 | 20 | 20 | fits | 111,153 | 187 | 0.399 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 153,939 | 1.539 | 20 | 24 | fits | 143,636 | 145 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 304,442 | 3.044 | 20 | 24 | fits | 151,493 | 216 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 304,376 | 3.044 | 20 | 50 | fits | 151,493 | 216 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 424,597 | 4.246 | 20 | 50 | fits | 111,153 | 187 | 0.399 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 511,050 | 5.111 | 20 | 20 | fits | 86,519 | 24 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 1,006,263 | 10.063 | 20 | 20 | fits | 73,195 | 24 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 353,663 | 3.537 | 20 | 20 | fits | 112,295 | 175 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 297,474 | 2.975 | 20 | 200 | fits | 149,585 | 230 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 409,153 | 4.092 | 20 | 200 | fits | 112,295 | 175 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 298,398 | 2.984 | 20 | 20 | fits | 149,585 | 230 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 409,857 | 4.099 | 20 | 20 | fits | 112,295 | 175 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 143,751 | 1.438 | 20 | 24 | fits | 143,844 | 146 | 0.400 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 301,048 | 3.010 | 20 | 24 | fits | 149,585 | 230 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 300,982 | 3.010 | 20 | 50 | fits | 149,585 | 230 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 412,881 | 4.129 | 20 | 50 | fits | 112,295 | 175 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 491,886 | 4.919 | 20 | 20 | fits | 79,071 | 26 | 0.822 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 991,405 | 9.914 | 20 | 20 | fits | 73,122 | 25 | 0.638 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 371,264 | 3.713 | 20 | 20 | fits | 117,746 | 193 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 302,242 | 3.022 | 20 | 200 | fits | 149,177 | 210 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 419,372 | 4.194 | 20 | 200 | fits | 117,746 | 193 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 303,166 | 3.032 | 20 | 20 | fits | 149,177 | 210 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 420,076 | 4.201 | 20 | 20 | fits | 117,746 | 193 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 157,629 | 1.576 | 20 | 24 | fits | 143,750 | 145 | 0.400 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 305,816 | 3.058 | 20 | 24 | fits | 149,177 | 210 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 305,750 | 3.058 | 20 | 50 | fits | 149,177 | 210 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 423,100 | 4.231 | 20 | 50 | fits | 117,746 | 193 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 509,593 | 5.096 | 20 | 20 | fits | 86,559 | 24 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 1,014,097 | 10.141 | 20 | 20 | fits | 73,265 | 24 | 0.644 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 352,410 | 3.524 | 20 | 20 | fits | 117,205 | 196 | 0.375 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 291,582 | 2.916 | 20 | 200 | fits | 148,865 | 208 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 408,171 | 4.082 | 20 | 200 | fits | 117,205 | 196 | 0.375 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 292,506 | 2.925 | 20 | 20 | fits | 148,865 | 208 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 408,875 | 4.089 | 20 | 20 | fits | 117,205 | 196 | 0.375 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 147,281 | 1.473 | 20 | 24 | fits | 143,798 | 145 | 0.401 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 295,156 | 2.952 | 20 | 24 | fits | 148,865 | 208 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 295,090 | 2.951 | 20 | 50 | fits | 148,865 | 208 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 411,899 | 4.119 | 20 | 50 | fits | 117,205 | 196 | 0.375 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 498,368 | 4.984 | 20 | 20 | fits | 86,535 | 24 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 1,002,966 | 10.030 | 20 | 20 | fits | 73,359 | 24 | 0.646 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 363,311 | 3.633 | 20 | 20 | fits | 109,707 | 188 | 0.380 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 302,195 | 3.022 | 20 | 200 | fits | 149,489 | 210 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 411,286 | 4.113 | 20 | 200 | fits | 109,707 | 188 | 0.380 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 303,119 | 3.031 | 20 | 20 | fits | 149,489 | 210 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 411,990 | 4.120 | 20 | 20 | fits | 109,707 | 188 | 0.380 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 157,270 | 1.573 | 20 | 24 | fits | 143,611 | 145 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 305,769 | 3.058 | 20 | 24 | fits | 149,489 | 210 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 305,703 | 3.057 | 20 | 50 | fits | 149,489 | 210 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 415,014 | 4.150 | 20 | 50 | fits | 109,707 | 188 | 0.380 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 514,072 | 5.141 | 20 | 20 | fits | 89,523 | 31 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 1,009,699 | 10.097 | 20 | 20 | fits | 67,537 | 26 | 0.750 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 369,364 | 3.694 | 20 | 20 | fits | 109,587 | 187 | 0.378 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 308,142 | 3.081 | 20 | 200 | fits | 150,780 | 215 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 417,113 | 4.171 | 20 | 200 | fits | 109,587 | 187 | 0.378 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 309,066 | 3.091 | 20 | 20 | fits | 150,780 | 215 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 417,817 | 4.178 | 20 | 20 | fits | 109,587 | 187 | 0.378 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 153,120 | 1.531 | 20 | 24 | fits | 143,881 | 146 | 0.400 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 311,716 | 3.117 | 20 | 24 | fits | 150,780 | 215 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 311,650 | 3.116 | 20 | 50 | fits | 150,780 | 215 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 420,841 | 4.208 | 20 | 50 | fits | 109,587 | 187 | 0.378 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 506,668 | 5.067 | 20 | 20 | fits | 85,893 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 1,006,389 | 10.064 | 20 | 20 | fits | 78,064 | 31 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 350,789 | 3.508 | 20 | 20 | fits | 108,733 | 184 | 0.385 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 291,731 | 2.917 | 20 | 200 | fits | 150,707 | 214 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 399,848 | 3.998 | 20 | 200 | fits | 108,733 | 184 | 0.385 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 292,655 | 2.927 | 20 | 20 | fits | 150,707 | 214 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 400,552 | 4.006 | 20 | 20 | fits | 108,733 | 184 | 0.385 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 145,588 | 1.456 | 20 | 24 | fits | 143,975 | 145 | 0.401 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 295,305 | 2.953 | 20 | 24 | fits | 150,707 | 214 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 295,239 | 2.952 | 20 | 50 | fits | 150,707 | 214 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 403,576 | 4.036 | 20 | 50 | fits | 108,733 | 184 | 0.385 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 481,888 | 4.819 | 20 | 20 | fits | 78,378 | 26 | 0.818 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 998,634 | 9.986 | 20 | 20 | fits | 85,886 | 28 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 370,028 | 3.700 | 20 | 20 | fits | 117,619 | 199 | 0.361 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 300,741 | 3.007 | 20 | 200 | fits | 147,765 | 204 | 0.442 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 417,744 | 4.177 | 20 | 200 | fits | 117,619 | 199 | 0.361 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 301,665 | 3.017 | 20 | 20 | fits | 147,765 | 204 | 0.442 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 418,448 | 4.184 | 20 | 20 | fits | 117,619 | 199 | 0.361 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 157,540 | 1.575 | 20 | 24 | fits | 143,975 | 145 | 0.401 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 304,315 | 3.043 | 20 | 24 | fits | 147,765 | 204 | 0.442 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 304,249 | 3.042 | 20 | 50 | fits | 147,765 | 204 | 0.442 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 421,472 | 4.215 | 20 | 50 | fits | 117,619 | 199 | 0.361 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 511,712 | 5.117 | 20 | 20 | fits | 90,306 | 31 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 1,011,113 | 10.111 | 20 | 20 | fits | 60,187 | 20 | 0.692 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 373,845 | 3.738 | 20 | 20 | fits | 114,344 | 194 | 0.413 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 299,255 | 2.993 | 20 | 200 | fits | 149,794 | 211 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 422,235 | 4.222 | 20 | 200 | fits | 114,344 | 194 | 0.413 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 300,179 | 3.002 | 20 | 20 | fits | 149,794 | 211 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 422,939 | 4.229 | 20 | 20 | fits | 114,344 | 194 | 0.413 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 154,025 | 1.540 | 20 | 24 | fits | 143,507 | 145 | 0.397 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 302,829 | 3.028 | 20 | 24 | fits | 149,794 | 211 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 302,763 | 3.028 | 20 | 50 | fits | 149,794 | 211 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 425,963 | 4.260 | 20 | 50 | fits | 114,344 | 194 | 0.413 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 511,717 | 5.117 | 20 | 20 | fits | 85,820 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 1,005,819 | 10.058 | 20 | 20 | fits | 67,477 | 26 | 0.748 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 351,950 | 3.519 | 20 | 20 | fits | 108,778 | 184 | 0.386 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 292,892 | 2.929 | 20 | 200 | fits | 150,641 | 214 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 401,054 | 4.011 | 20 | 200 | fits | 108,778 | 184 | 0.386 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 293,816 | 2.938 | 20 | 20 | fits | 150,641 | 214 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 401,758 | 4.018 | 20 | 20 | fits | 108,778 | 184 | 0.386 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 146,815 | 1.468 | 20 | 24 | fits | 144,049 | 145 | 0.402 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 296,466 | 2.965 | 20 | 24 | fits | 150,641 | 214 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 296,400 | 2.964 | 20 | 50 | fits | 150,641 | 214 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 404,782 | 4.048 | 20 | 50 | fits | 108,778 | 184 | 0.386 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 490,609 | 4.906 | 20 | 20 | fits | 85,893 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 1,002,020 | 10.020 | 20 | 20 | fits | 85,886 | 28 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 347,188 | 3.472 | 20 | 20 | fits | 102,216 | 172 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 294,749 | 2.947 | 20 | 200 | fits | 149,577 | 258 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 396,349 | 3.963 | 20 | 200 | fits | 102,216 | 172 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 295,673 | 2.957 | 20 | 20 | fits | 149,577 | 258 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 397,053 | 3.971 | 20 | 20 | fits | 102,216 | 172 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 149,736 | 1.497 | 20 | 24 | fits | 151,390 | 114 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 298,323 | 2.983 | 20 | 24 | fits | 149,577 | 258 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 298,257 | 2.983 | 20 | 50 | fits | 149,577 | 258 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 400,077 | 4.001 | 20 | 50 | fits | 102,216 | 172 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 478,516 | 4.785 | 20 | 20 | fits | 78,505 | 26 | 0.818 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 996,218 | 9.962 | 20 | 20 | fits | 85,797 | 28 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 380,614 | 3.806 | 20 | 20 | fits | 122,510 | 205 | 0.397 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 297,798 | 2.978 | 20 | 200 | fits | 148,029 | 205 | 0.442 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 429,095 | 4.291 | 20 | 200 | fits | 122,510 | 205 | 0.397 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 298,722 | 2.987 | 20 | 20 | fits | 148,029 | 205 | 0.442 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 429,799 | 4.298 | 20 | 20 | fits | 122,510 | 205 | 0.397 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 154,333 | 1.543 | 20 | 24 | fits | 144,035 | 145 | 0.402 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 301,372 | 3.014 | 20 | 24 | fits | 148,029 | 205 | 0.442 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 301,306 | 3.013 | 20 | 50 | fits | 148,029 | 205 | 0.442 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 432,823 | 4.328 | 20 | 50 | fits | 122,510 | 205 | 0.397 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 518,571 | 5.186 | 20 | 20 | fits | 85,814 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 1,005,259 | 10.053 | 20 | 20 | fits | 60,063 | 20 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 390,648 | 3.906 | 20 | 20 | fits | 109,566 | 187 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 329,459 | 3.295 | 20 | 200 | fits | 149,475 | 210 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 438,409 | 4.384 | 20 | 200 | fits | 109,566 | 187 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 330,383 | 3.304 | 20 | 20 | fits | 149,475 | 210 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 439,113 | 4.391 | 20 | 20 | fits | 109,566 | 187 | 0.379 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 184,548 | 1.845 | 20 | 24 | fits | 144,082 | 145 | 0.402 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 333,033 | 3.330 | 20 | 24 | fits | 149,475 | 210 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 332,967 | 3.330 | 20 | 50 | fits | 149,475 | 210 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 442,137 | 4.421 | 20 | 50 | fits | 109,566 | 187 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 527,970 | 5.280 | 20 | 20 | fits | 85,899 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,039,606 | 10.396 | 20 | 20 | fits | 80,164 | 30 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 357,135 | 3.571 | 20 | 20 | fits | 111,413 | 175 | 0.373 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 301,332 | 3.013 | 20 | 200 | fits | 148,277 | 225 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 412,129 | 4.121 | 20 | 200 | fits | 111,413 | 175 | 0.373 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 302,256 | 3.023 | 20 | 20 | fits | 148,277 | 225 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 412,833 | 4.128 | 20 | 20 | fits | 111,413 | 175 | 0.373 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 157,619 | 1.576 | 20 | 24 | fits | 143,627 | 145 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 304,906 | 3.049 | 20 | 24 | fits | 148,277 | 225 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 304,840 | 3.048 | 20 | 50 | fits | 148,277 | 225 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 415,857 | 4.159 | 20 | 50 | fits | 111,413 | 175 | 0.373 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 501,849 | 5.018 | 20 | 20 | fits | 86,058 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 1,014,434 | 10.144 | 20 | 20 | fits | 86,265 | 28 | 0.612 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 340,493 | 3.405 | 20 | 20 | fits | 109,867 | 185 | 0.399 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 293,376 | 2.934 | 20 | 200 | fits | 150,775 | 214 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 402,627 | 4.026 | 20 | 200 | fits | 109,867 | 185 | 0.399 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 294,300 | 2.943 | 20 | 20 | fits | 150,775 | 214 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 403,331 | 4.033 | 20 | 20 | fits | 109,867 | 185 | 0.399 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 147,165 | 1.472 | 20 | 24 | fits | 143,569 | 145 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 296,950 | 2.970 | 20 | 24 | fits | 150,775 | 214 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 296,884 | 2.969 | 20 | 50 | fits | 150,775 | 214 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 406,355 | 4.064 | 20 | 50 | fits | 109,867 | 185 | 0.399 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 505,578 | 5.056 | 20 | 20 | fits | 89,688 | 31 | 0.778 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 1,001,093 | 10.011 | 20 | 20 | fits | 73,227 | 24 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 366,538 | 3.665 | 20 | 20 | fits | 116,464 | 182 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 297,051 | 2.971 | 20 | 200 | fits | 148,474 | 226 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 422,216 | 4.222 | 20 | 200 | fits | 116,464 | 182 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 297,975 | 2.980 | 20 | 20 | fits | 148,474 | 226 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 422,920 | 4.229 | 20 | 20 | fits | 116,464 | 182 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 153,141 | 1.531 | 20 | 24 | fits | 143,569 | 145 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 300,625 | 3.006 | 20 | 24 | fits | 148,474 | 226 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 300,559 | 3.006 | 20 | 50 | fits | 148,474 | 226 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 425,944 | 4.259 | 20 | 50 | fits | 116,464 | 182 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 511,831 | 5.118 | 20 | 20 | fits | 85,953 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 1,006,956 | 10.070 | 20 | 20 | fits | 73,283 | 24 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 346,817 | 3.468 | 20 | 20 | fits | 109,829 | 184 | 0.398 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 299,512 | 2.995 | 20 | 200 | fits | 152,251 | 219 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 408,725 | 4.087 | 20 | 200 | fits | 109,829 | 184 | 0.398 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 300,436 | 3.004 | 20 | 20 | fits | 152,251 | 219 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 409,429 | 4.094 | 20 | 20 | fits | 109,829 | 184 | 0.398 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 143,025 | 1.430 | 20 | 24 | fits | 143,849 | 146 | 0.399 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 303,086 | 3.031 | 20 | 24 | fits | 152,251 | 219 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 303,020 | 3.030 | 20 | 50 | fits | 152,251 | 219 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 412,453 | 4.125 | 20 | 50 | fits | 109,829 | 184 | 0.398 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 498,400 | 4.984 | 20 | 20 | fits | 86,013 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 997,729 | 9.977 | 20 | 20 | fits | 78,064 | 31 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 350,397 | 3.504 | 20 | 20 | fits | 119,587 | 181 | 0.407 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 286,693 | 2.867 | 20 | 200 | fits | 149,464 | 230 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 405,664 | 4.057 | 20 | 200 | fits | 119,587 | 181 | 0.407 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 287,617 | 2.876 | 20 | 20 | fits | 149,464 | 230 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 406,368 | 4.064 | 20 | 20 | fits | 119,587 | 181 | 0.407 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 141,793 | 1.418 | 20 | 24 | fits | 144,021 | 145 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 290,267 | 2.903 | 20 | 24 | fits | 149,464 | 230 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 290,201 | 2.902 | 20 | 50 | fits | 149,464 | 230 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 409,392 | 4.094 | 20 | 50 | fits | 119,587 | 181 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 495,477 | 4.955 | 20 | 20 | fits | 86,151 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 999,463 | 9.995 | 20 | 20 | fits | 73,845 | 24 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 348,096 | 3.481 | 20 | 20 | fits | 117,515 | 190 | 0.427 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 293,303 | 2.933 | 20 | 200 | fits | 150,810 | 214 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 410,202 | 4.102 | 20 | 200 | fits | 117,515 | 190 | 0.427 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 294,227 | 2.942 | 20 | 20 | fits | 150,810 | 214 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 410,906 | 4.109 | 20 | 20 | fits | 117,515 | 190 | 0.427 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 147,057 | 1.471 | 20 | 24 | fits | 143,755 | 145 | 0.400 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 296,877 | 2.969 | 20 | 24 | fits | 150,810 | 214 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 296,811 | 2.968 | 20 | 50 | fits | 150,810 | 214 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 413,930 | 4.139 | 20 | 50 | fits | 117,515 | 190 | 0.427 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 500,037 | 5.000 | 20 | 20 | fits | 86,173 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 1,005,035 | 10.050 | 20 | 20 | fits | 73,144 | 24 | 0.641 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 358,327 | 3.583 | 20 | 20 | fits | 116,619 | 196 | 0.368 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 297,273 | 2.973 | 20 | 200 | fits | 148,804 | 208 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 413,276 | 4.133 | 20 | 200 | fits | 116,619 | 196 | 0.368 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 298,197 | 2.982 | 20 | 20 | fits | 148,804 | 208 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 413,980 | 4.140 | 20 | 20 | fits | 116,619 | 196 | 0.368 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 153,033 | 1.530 | 20 | 24 | fits | 143,755 | 145 | 0.400 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 300,847 | 3.008 | 20 | 24 | fits | 148,804 | 208 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 300,781 | 3.008 | 20 | 50 | fits | 148,804 | 208 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 417,004 | 4.170 | 20 | 50 | fits | 116,619 | 196 | 0.368 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 503,028 | 5.030 | 20 | 20 | fits | 86,090 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 1,007,923 | 10.079 | 20 | 20 | fits | 73,407 | 24 | 0.646 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 364,440 | 3.644 | 20 | 20 | fits | 116,214 | 199 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 287,575 | 2.876 | 20 | 200 | fits | 151,325 | 216 | 0.424 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 412,839 | 4.128 | 20 | 200 | fits | 116,214 | 199 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 288,499 | 2.885 | 20 | 20 | fits | 151,325 | 216 | 0.424 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 413,543 | 4.135 | 20 | 20 | fits | 116,214 | 199 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 140,814 | 1.408 | 20 | 24 | fits | 146,747 | 147 | 0.417 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 291,149 | 2.911 | 20 | 24 | fits | 151,325 | 216 | 0.424 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 291,083 | 2.911 | 20 | 50 | fits | 151,325 | 216 | 0.424 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 416,567 | 4.166 | 20 | 50 | fits | 116,214 | 199 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 502,441 | 5.024 | 20 | 20 | fits | 85,940 | 24 | 0.780 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 996,362 | 9.964 | 20 | 20 | fits | 67,598 | 26 | 0.751 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 364,389 | 3.644 | 20 | 20 | fits | 111,490 | 175 | 0.375 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 308,331 | 3.083 | 20 | 200 | fits | 149,193 | 230 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 419,205 | 4.192 | 20 | 200 | fits | 111,490 | 175 | 0.375 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 309,255 | 3.093 | 20 | 20 | fits | 149,193 | 230 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 419,909 | 4.199 | 20 | 20 | fits | 111,490 | 175 | 0.375 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 154,174 | 1.542 | 20 | 24 | fits | 143,319 | 143 | 0.396 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 311,905 | 3.119 | 20 | 24 | fits | 149,193 | 230 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 311,839 | 3.118 | 20 | 50 | fits | 149,193 | 230 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 422,933 | 4.229 | 20 | 50 | fits | 111,490 | 175 | 0.375 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 508,539 | 5.085 | 20 | 20 | fits | 85,672 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 1,095,589 | 10.956 | 20 | 20 | fits | 79,333 | 31 | 0.722 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 348,131 | 3.481 | 20 | 20 | fits | 103,100 | 160 | 0.408 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 314,452 | 3.145 | 20 | 200 | fits | 146,623 | 230 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 416,936 | 4.169 | 20 | 200 | fits | 103,100 | 160 | 0.408 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 315,376 | 3.154 | 20 | 20 | fits | 146,623 | 230 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 417,640 | 4.176 | 20 | 20 | fits | 103,100 | 160 | 0.408 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 172,393 | 1.724 | 20 | 24 | fits | 153,781 | 153 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 318,026 | 3.180 | 20 | 24 | fits | 146,623 | 230 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 317,960 | 3.180 | 20 | 50 | fits | 146,623 | 230 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 420,664 | 4.207 | 20 | 50 | fits | 103,100 | 160 | 0.408 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 506,225 | 5.062 | 20 | 20 | fits | 85,627 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,093,390 | 10.934 | 20 | 20 | fits | 86,028 | 28 | 0.609 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 350,265 | 3.503 | 20 | 20 | fits | 108,687 | 184 | 0.387 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 291,099 | 2.911 | 20 | 200 | fits | 150,646 | 214 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 399,170 | 3.992 | 20 | 200 | fits | 108,687 | 184 | 0.387 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 292,023 | 2.920 | 20 | 20 | fits | 150,646 | 214 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 399,874 | 3.999 | 20 | 20 | fits | 108,687 | 184 | 0.387 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 145,017 | 1.450 | 20 | 24 | fits | 143,331 | 142 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 294,673 | 2.947 | 20 | 24 | fits | 150,646 | 214 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 294,607 | 2.946 | 20 | 50 | fits | 150,646 | 214 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 402,898 | 4.029 | 20 | 50 | fits | 108,687 | 184 | 0.387 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 488,421 | 4.884 | 20 | 20 | fits | 85,589 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,076,994 | 10.770 | 20 | 20 | fits | 85,658 | 28 | 0.598 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 341,222 | 3.412 | 20 | 20 | fits | 111,379 | 175 | 0.374 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 285,246 | 2.852 | 20 | 200 | fits | 149,439 | 230 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 396,009 | 3.960 | 20 | 200 | fits | 111,379 | 175 | 0.374 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 286,170 | 2.862 | 20 | 20 | fits | 149,439 | 230 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 396,713 | 3.967 | 20 | 20 | fits | 111,379 | 175 | 0.374 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 140,371 | 1.404 | 20 | 24 | fits | 143,264 | 142 | 0.405 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 288,820 | 2.888 | 20 | 24 | fits | 149,439 | 230 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 288,754 | 2.888 | 20 | 50 | fits | 149,439 | 230 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 399,737 | 3.997 | 20 | 50 | fits | 111,379 | 175 | 0.374 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 485,266 | 4.853 | 20 | 20 | fits | 85,595 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,072,828 | 10.728 | 20 | 20 | fits | 85,913 | 28 | 0.604 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 358,243 | 3.582 | 20 | 20 | fits | 108,687 | 184 | 0.387 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 299,077 | 2.991 | 20 | 200 | fits | 150,646 | 214 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 407,148 | 4.071 | 20 | 200 | fits | 108,687 | 184 | 0.387 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 300,001 | 3.000 | 20 | 20 | fits | 150,646 | 214 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 407,852 | 4.079 | 20 | 20 | fits | 108,687 | 184 | 0.387 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 152,995 | 1.530 | 20 | 24 | fits | 143,264 | 142 | 0.405 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 302,651 | 3.027 | 20 | 24 | fits | 150,646 | 214 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 302,585 | 3.026 | 20 | 50 | fits | 150,646 | 214 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 410,876 | 4.109 | 20 | 50 | fits | 108,687 | 184 | 0.387 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 492,122 | 4.921 | 20 | 20 | fits | 81,312 | 33 | 0.805 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,080,462 | 10.805 | 20 | 20 | fits | 73,107 | 24 | 0.641 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 358,632 | 3.586 | 20 | 20 | fits | 121,898 | 188 | 0.407 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 291,998 | 2.920 | 20 | 200 | fits | 148,079 | 225 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 413,280 | 4.133 | 20 | 200 | fits | 121,898 | 188 | 0.407 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 292,922 | 2.929 | 20 | 20 | fits | 148,079 | 225 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 413,984 | 4.140 | 20 | 20 | fits | 121,898 | 188 | 0.407 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 148,483 | 1.485 | 20 | 24 | fits | 143,331 | 142 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 295,572 | 2.956 | 20 | 24 | fits | 148,079 | 225 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 295,506 | 2.955 | 20 | 50 | fits | 148,079 | 225 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 417,008 | 4.170 | 20 | 50 | fits | 121,898 | 188 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 588,857 | 5.889 | 20 | 20 | fits | 86,388 | 25 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,075,408 | 10.754 | 20 | 20 | fits | 60,078 | 20 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 438,549 | 4.385 | 20 | 20 | fits | 122,118 | 202 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 288,110 | 2.881 | 20 | 200 | fits | 148,837 | 209 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 494,951 | 4.950 | 20 | 200 | fits | 122,118 | 202 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 289,034 | 2.890 | 20 | 20 | fits | 148,837 | 209 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 495,655 | 4.957 | 20 | 20 | fits | 122,118 | 202 | 0.409 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 143,837 | 1.438 | 20 | 24 | fits | 143,264 | 142 | 0.405 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 291,684 | 2.917 | 20 | 24 | fits | 148,837 | 209 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 291,618 | 2.916 | 20 | 50 | fits | 148,837 | 209 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 498,679 | 4.987 | 20 | 50 | fits | 122,118 | 202 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 584,393 | 5.844 | 20 | 20 | fits | 85,780 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,070,836 | 10.708 | 20 | 20 | fits | 60,038 | 20 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 352,218 | 3.522 | 20 | 20 | fits | 111,496 | 175 | 0.374 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 296,216 | 2.962 | 20 | 200 | fits | 147,870 | 225 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 407,096 | 4.071 | 20 | 200 | fits | 111,496 | 175 | 0.374 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 297,140 | 2.971 | 20 | 20 | fits | 147,870 | 225 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 407,800 | 4.078 | 20 | 20 | fits | 111,496 | 175 | 0.374 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 152,910 | 1.529 | 20 | 24 | fits | 143,432 | 142 | 0.407 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 299,790 | 2.998 | 20 | 24 | fits | 147,870 | 225 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 299,724 | 2.997 | 20 | 50 | fits | 147,870 | 225 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 410,824 | 4.108 | 20 | 50 | fits | 111,496 | 175 | 0.374 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 497,220 | 4.972 | 20 | 20 | fits | 86,462 | 25 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 1,001,998 | 10.020 | 20 | 20 | fits | 73,359 | 24 | 0.646 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 341,529 | 3.415 | 20 | 20 | fits | 109,649 | 185 | 0.399 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 294,354 | 2.944 | 20 | 200 | fits | 150,603 | 214 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 403,387 | 4.034 | 20 | 200 | fits | 109,649 | 185 | 0.399 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 295,278 | 2.953 | 20 | 20 | fits | 150,603 | 214 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 404,091 | 4.041 | 20 | 20 | fits | 109,649 | 185 | 0.399 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 148,315 | 1.483 | 20 | 24 | fits | 143,437 | 142 | 0.407 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 297,928 | 2.979 | 20 | 24 | fits | 150,603 | 214 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 297,862 | 2.979 | 20 | 50 | fits | 150,603 | 214 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 407,115 | 4.071 | 20 | 50 | fits | 109,649 | 185 | 0.399 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 506,854 | 5.069 | 20 | 20 | fits | 90,164 | 31 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 1,042,357 | 10.424 | 20 | 20 | fits | 75,224 | 25 | 0.705 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 363,344 | 3.633 | 20 | 20 | fits | 114,479 | 194 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 288,472 | 2.885 | 20 | 200 | fits | 149,326 | 211 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 411,758 | 4.118 | 20 | 200 | fits | 114,479 | 194 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 289,396 | 2.894 | 20 | 20 | fits | 149,326 | 211 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 412,462 | 4.125 | 20 | 20 | fits | 114,479 | 194 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 143,710 | 1.437 | 20 | 24 | fits | 143,432 | 142 | 0.407 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 292,046 | 2.920 | 20 | 24 | fits | 149,326 | 211 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 291,980 | 2.920 | 20 | 50 | fits | 149,326 | 211 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 415,486 | 4.155 | 20 | 50 | fits | 114,479 | 194 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 501,822 | 5.018 | 20 | 20 | fits | 86,402 | 24 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 1,066,250 | 10.662 | 20 | 20 | fits | 74,023 | 25 | 0.681 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 352,484 | 3.525 | 20 | 20 | fits | 112,078 | 189 | 0.408 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 296,592 | 2.966 | 20 | 200 | fits | 152,016 | 254 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 408,054 | 4.081 | 20 | 200 | fits | 112,078 | 189 | 0.408 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 297,516 | 2.975 | 20 | 20 | fits | 152,016 | 254 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 408,758 | 4.088 | 20 | 20 | fits | 112,078 | 189 | 0.408 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 140,387 | 1.404 | 20 | 24 | fits | 144,709 | 112 | 0.418 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 300,166 | 3.002 | 20 | 24 | fits | 152,016 | 254 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 300,100 | 3.001 | 20 | 50 | fits | 152,016 | 254 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 411,782 | 4.118 | 20 | 50 | fits | 112,078 | 189 | 0.408 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 498,074 | 4.981 | 20 | 20 | fits | 86,358 | 24 | 0.780 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 1,079,172 | 10.792 | 20 | 20 | fits | 86,312 | 28 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 354,528 | 3.545 | 20 | 20 | fits | 108,567 | 184 | 0.386 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 295,482 | 2.955 | 20 | 200 | fits | 150,259 | 214 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 403,433 | 4.034 | 20 | 200 | fits | 108,567 | 184 | 0.386 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 296,406 | 2.964 | 20 | 20 | fits | 150,259 | 214 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 404,137 | 4.041 | 20 | 20 | fits | 108,567 | 184 | 0.386 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 149,787 | 1.498 | 20 | 24 | fits | 143,352 | 142 | 0.407 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 299,056 | 2.991 | 20 | 24 | fits | 150,259 | 214 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 298,990 | 2.990 | 20 | 50 | fits | 150,259 | 214 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 407,161 | 4.072 | 20 | 50 | fits | 108,567 | 184 | 0.386 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 493,443 | 4.934 | 20 | 20 | fits | 86,348 | 24 | 0.781 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 1,074,988 | 10.750 | 20 | 20 | fits | 85,830 | 28 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 344,027 | 3.440 | 20 | 20 | fits | 111,246 | 175 | 0.374 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 288,184 | 2.882 | 20 | 200 | fits | 147,668 | 225 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 398,814 | 3.988 | 20 | 200 | fits | 111,246 | 175 | 0.374 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 289,108 | 2.891 | 20 | 20 | fits | 147,668 | 225 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 399,518 | 3.995 | 20 | 20 | fits | 111,246 | 175 | 0.374 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 145,080 | 1.451 | 20 | 24 | fits | 143,357 | 142 | 0.407 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 291,758 | 2.918 | 20 | 24 | fits | 147,668 | 225 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 291,692 | 2.917 | 20 | 50 | fits | 147,668 | 225 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 402,542 | 4.025 | 20 | 50 | fits | 111,246 | 175 | 0.374 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 487,019 | 4.870 | 20 | 20 | fits | 84,543 | 26 | 0.832 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 1,070,316 | 10.703 | 20 | 20 | fits | 85,741 | 28 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 349,487 | 3.495 | 20 | 20 | fits | 126,058 | 190 | 0.465 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 287,443 | 2.874 | 20 | 200 | fits | 151,644 | 219 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 412,885 | 4.129 | 20 | 200 | fits | 126,058 | 190 | 0.465 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 288,367 | 2.884 | 20 | 20 | fits | 151,644 | 219 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 413,589 | 4.136 | 20 | 20 | fits | 126,058 | 190 | 0.465 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 140,363 | 1.404 | 20 | 24 | fits | 143,352 | 142 | 0.407 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 291,017 | 2.910 | 20 | 24 | fits | 151,644 | 219 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 290,951 | 2.910 | 20 | 50 | fits | 151,644 | 219 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 416,613 | 4.166 | 20 | 50 | fits | 126,058 | 190 | 0.465 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 531,088 | 5.311 | 20 | 20 | fits | 85,468 | 26 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 1,065,545 | 10.655 | 20 | 20 | fits | 73,214 | 24 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 367,371 | 3.674 | 20 | 20 | fits | 125,003 | 209 | 0.357 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 298,009 | 2.980 | 20 | 200 | fits | 149,738 | 197 | 0.471 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 422,396 | 4.224 | 20 | 200 | fits | 125,003 | 209 | 0.357 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 298,933 | 2.989 | 20 | 20 | fits | 149,738 | 197 | 0.471 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 423,100 | 4.231 | 20 | 20 | fits | 125,003 | 209 | 0.357 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 152,835 | 1.528 | 20 | 24 | fits | 143,352 | 142 | 0.407 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 301,583 | 3.016 | 20 | 24 | fits | 149,738 | 197 | 0.471 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 301,517 | 3.015 | 20 | 50 | fits | 149,738 | 197 | 0.471 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 426,124 | 4.261 | 20 | 50 | fits | 125,003 | 209 | 0.357 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 554,024 | 5.540 | 20 | 20 | fits | 89,985 | 31 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 1,073,087 | 10.731 | 20 | 20 | fits | 60,170 | 20 | 0.692 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 358,980 | 3.590 | 20 | 20 | fits | 111,996 | 190 | 0.402 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 296,858 | 2.969 | 20 | 200 | fits | 151,696 | 219 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 408,238 | 4.082 | 20 | 200 | fits | 111,996 | 190 | 0.402 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 297,782 | 2.978 | 20 | 20 | fits | 151,696 | 219 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 408,942 | 4.089 | 20 | 20 | fits | 111,996 | 190 | 0.402 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 140,853 | 1.409 | 20 | 24 | fits | 143,700 | 143 | 0.408 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 300,432 | 3.004 | 20 | 24 | fits | 151,696 | 219 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 300,366 | 3.004 | 20 | 50 | fits | 151,696 | 219 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 411,966 | 4.120 | 20 | 50 | fits | 111,996 | 190 | 0.402 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 497,512 | 4.975 | 20 | 20 | fits | 85,612 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 984,182 | 9.842 | 20 | 20 | fits | 60,133 | 21 | 0.686 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 349,720 | 3.497 | 20 | 20 | fits | 111,429 | 175 | 0.373 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 293,830 | 2.938 | 20 | 200 | fits | 147,884 | 225 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 404,643 | 4.046 | 20 | 200 | fits | 111,429 | 175 | 0.373 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 294,754 | 2.948 | 20 | 20 | fits | 147,884 | 225 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 405,347 | 4.053 | 20 | 20 | fits | 111,429 | 175 | 0.373 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 150,510 | 1.505 | 20 | 24 | fits | 143,494 | 142 | 0.407 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 297,404 | 2.974 | 20 | 24 | fits | 147,884 | 225 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 297,338 | 2.973 | 20 | 50 | fits | 147,884 | 225 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 408,371 | 4.084 | 20 | 50 | fits | 111,429 | 175 | 0.373 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 493,956 | 4.940 | 20 | 20 | fits | 85,651 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 1,085,656 | 10.857 | 20 | 20 | fits | 85,731 | 29 | 0.609 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 338,954 | 3.390 | 20 | 20 | fits | 109,669 | 184 | 0.397 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 291,750 | 2.917 | 20 | 200 | fits | 150,499 | 214 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 400,803 | 4.008 | 20 | 200 | fits | 109,669 | 184 | 0.397 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 292,674 | 2.927 | 20 | 20 | fits | 150,499 | 214 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 401,507 | 4.015 | 20 | 20 | fits | 109,669 | 184 | 0.397 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 145,815 | 1.458 | 20 | 24 | fits | 143,427 | 142 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 295,324 | 2.953 | 20 | 24 | fits | 150,499 | 214 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 295,258 | 2.953 | 20 | 50 | fits | 150,499 | 214 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 404,531 | 4.045 | 20 | 50 | fits | 109,669 | 184 | 0.397 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 490,077 | 4.901 | 20 | 20 | fits | 85,612 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,081,629 | 10.816 | 20 | 20 | fits | 85,838 | 28 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 348,542 | 3.485 | 20 | 20 | fits | 109,590 | 187 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 287,258 | 2.873 | 20 | 200 | fits | 150,568 | 215 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 396,232 | 3.962 | 20 | 200 | fits | 109,590 | 187 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 288,182 | 2.882 | 20 | 20 | fits | 150,568 | 215 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 396,936 | 3.969 | 20 | 20 | fits | 109,590 | 187 | 0.379 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 141,254 | 1.413 | 20 | 24 | fits | 143,494 | 142 | 0.407 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 290,832 | 2.908 | 20 | 24 | fits | 150,568 | 215 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 290,766 | 2.908 | 20 | 50 | fits | 150,568 | 215 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 399,960 | 4.000 | 20 | 50 | fits | 109,590 | 187 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 485,673 | 4.857 | 20 | 20 | fits | 85,779 | 25 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,077,177 | 10.772 | 20 | 20 | fits | 85,786 | 28 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 346,961 | 3.470 | 20 | 20 | fits | 109,883 | 185 | 0.399 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 299,757 | 2.998 | 20 | 200 | fits | 150,499 | 214 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 409,024 | 4.090 | 20 | 200 | fits | 109,883 | 185 | 0.399 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 300,681 | 3.007 | 20 | 20 | fits | 150,499 | 214 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 409,728 | 4.097 | 20 | 20 | fits | 109,883 | 185 | 0.399 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 153,822 | 1.538 | 20 | 24 | fits | 143,494 | 142 | 0.407 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 303,331 | 3.033 | 20 | 24 | fits | 150,499 | 214 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 303,265 | 3.033 | 20 | 50 | fits | 150,499 | 214 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 412,752 | 4.128 | 20 | 50 | fits | 109,883 | 185 | 0.399 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 511,770 | 5.118 | 20 | 20 | fits | 89,519 | 31 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,087,398 | 10.874 | 20 | 20 | fits | 73,227 | 24 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 368,621 | 3.686 | 20 | 20 | fits | 114,433 | 194 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 294,035 | 2.940 | 20 | 200 | fits | 149,472 | 211 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 417,147 | 4.171 | 20 | 200 | fits | 114,433 | 194 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 294,959 | 2.950 | 20 | 20 | fits | 149,472 | 211 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 417,851 | 4.179 | 20 | 20 | fits | 114,433 | 194 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 149,127 | 1.491 | 20 | 24 | fits | 143,427 | 142 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 297,609 | 2.976 | 20 | 24 | fits | 149,472 | 211 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 297,543 | 2.975 | 20 | 50 | fits | 149,472 | 211 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 420,875 | 4.209 | 20 | 50 | fits | 114,433 | 194 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 499,054 | 4.991 | 20 | 20 | fits | 78,245 | 26 | 0.817 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,079,521 | 10.795 | 20 | 20 | fits | 73,182 | 25 | 0.638 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 362,220 | 3.622 | 20 | 20 | fits | 120,069 | 181 | 0.413 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 298,529 | 2.985 | 20 | 200 | fits | 149,473 | 230 | 0.406 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 417,982 | 4.180 | 20 | 200 | fits | 120,069 | 181 | 0.413 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 299,453 | 2.995 | 20 | 20 | fits | 149,473 | 230 | 0.406 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 418,686 | 4.187 | 20 | 20 | fits | 120,069 | 181 | 0.413 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 144,875 | 1.449 | 20 | 24 | fits | 143,803 | 143 | 0.409 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 302,103 | 3.021 | 20 | 24 | fits | 149,473 | 230 | 0.406 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 302,037 | 3.020 | 20 | 50 | fits | 149,473 | 230 | 0.406 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 421,710 | 4.217 | 20 | 50 | fits | 120,069 | 181 | 0.413 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 587,451 | 5.875 | 20 | 20 | fits | 85,243 | 25 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,091,108 | 10.911 | 20 | 20 | fits | 73,793 | 24 | 0.657 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 446,800 | 4.468 | 20 | 20 | fits | 116,641 | 196 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 299,536 | 2.995 | 20 | 200 | fits | 148,893 | 208 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 495,947 | 4.959 | 20 | 200 | fits | 116,641 | 196 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 300,460 | 3.005 | 20 | 20 | fits | 148,893 | 208 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 496,651 | 4.967 | 20 | 20 | fits | 116,641 | 196 | 0.372 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 155,207 | 1.552 | 20 | 24 | fits | 143,483 | 142 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 303,110 | 3.031 | 20 | 24 | fits | 148,893 | 208 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 303,044 | 3.030 | 20 | 50 | fits | 148,893 | 208 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 499,675 | 4.997 | 20 | 50 | fits | 116,641 | 196 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 585,519 | 5.855 | 20 | 20 | fits | 85,910 | 24 | 0.778 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,089,944 | 10.899 | 20 | 20 | fits | 73,347 | 24 | 0.644 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 355,977 | 3.560 | 20 | 20 | fits | 116,793 | 181 | 0.413 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 286,494 | 2.865 | 20 | 200 | fits | 149,653 | 231 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 412,175 | 4.122 | 20 | 200 | fits | 116,793 | 181 | 0.413 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 287,418 | 2.874 | 20 | 20 | fits | 149,653 | 231 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 412,879 | 4.129 | 20 | 20 | fits | 116,793 | 181 | 0.413 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 141,405 | 1.414 | 20 | 24 | fits | 143,552 | 142 | 0.408 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 290,068 | 2.901 | 20 | 24 | fits | 149,653 | 231 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 290,002 | 2.900 | 20 | 50 | fits | 149,653 | 231 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 415,903 | 4.159 | 20 | 50 | fits | 116,793 | 181 | 0.413 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 501,520 | 5.015 | 20 | 20 | fits | 85,683 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 988,219 | 9.882 | 20 | 20 | fits | 60,074 | 20 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 370,685 | 3.707 | 20 | 20 | fits | 109,641 | 187 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 309,379 | 3.094 | 20 | 200 | fits | 150,748 | 215 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 418,404 | 4.184 | 20 | 200 | fits | 109,641 | 187 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 310,303 | 3.103 | 20 | 20 | fits | 150,748 | 215 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 419,108 | 4.191 | 20 | 20 | fits | 109,641 | 187 | 0.379 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 154,322 | 1.543 | 20 | 24 | fits | 143,901 | 143 | 0.409 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 312,953 | 3.130 | 20 | 24 | fits | 150,748 | 215 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 312,887 | 3.129 | 20 | 50 | fits | 150,748 | 215 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 422,132 | 4.221 | 20 | 50 | fits | 109,641 | 187 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 507,602 | 5.076 | 20 | 20 | fits | 85,536 | 24 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 1,018,360 | 10.184 | 20 | 20 | fits | 78,823 | 31 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 358,933 | 3.589 | 20 | 20 | fits | 98,610 | 142 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 316,425 | 3.164 | 20 | 200 | fits | 150,352 | 248 | 0.401 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 414,419 | 4.144 | 20 | 200 | fits | 98,610 | 142 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 317,349 | 3.173 | 20 | 20 | fits | 150,352 | 248 | 0.401 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 415,123 | 4.151 | 20 | 20 | fits | 98,610 | 142 | 0.406 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 170,637 | 1.706 | 20 | 24 | fits | 153,963 | 153 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 319,999 | 3.200 | 20 | 24 | fits | 150,352 | 248 | 0.401 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 319,933 | 3.199 | 20 | 50 | fits | 150,352 | 248 | 0.401 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 418,147 | 4.181 | 20 | 50 | fits | 98,610 | 142 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 503,815 | 5.038 | 20 | 20 | fits | 85,734 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 1,014,885 | 10.149 | 20 | 20 | fits | 86,150 | 28 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 335,893 | 3.359 | 20 | 20 | fits | 109,792 | 184 | 0.398 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 288,521 | 2.885 | 20 | 200 | fits | 151,784 | 219 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 397,697 | 3.977 | 20 | 200 | fits | 109,792 | 184 | 0.398 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 289,445 | 2.894 | 20 | 20 | fits | 151,784 | 219 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 398,401 | 3.984 | 20 | 20 | fits | 109,792 | 184 | 0.398 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 141,301 | 1.413 | 20 | 24 | fits | 143,427 | 142 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 292,095 | 2.921 | 20 | 24 | fits | 151,784 | 219 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 292,029 | 2.920 | 20 | 50 | fits | 151,784 | 219 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 401,425 | 4.014 | 20 | 50 | fits | 109,792 | 184 | 0.398 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 486,965 | 4.870 | 20 | 20 | fits | 85,606 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 998,525 | 9.985 | 20 | 20 | fits | 85,878 | 28 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 354,891 | 3.549 | 20 | 20 | fits | 111,471 | 175 | 0.373 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 298,914 | 2.989 | 20 | 200 | fits | 147,809 | 225 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 409,769 | 4.098 | 20 | 200 | fits | 111,471 | 175 | 0.373 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 299,838 | 2.998 | 20 | 20 | fits | 147,809 | 225 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 410,473 | 4.105 | 20 | 20 | fits | 111,471 | 175 | 0.373 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 155,669 | 1.557 | 20 | 24 | fits | 143,427 | 142 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 302,488 | 3.025 | 20 | 24 | fits | 147,809 | 225 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 302,422 | 3.024 | 20 | 50 | fits | 147,809 | 225 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 413,497 | 4.135 | 20 | 50 | fits | 111,471 | 175 | 0.373 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 499,082 | 4.991 | 20 | 20 | fits | 85,651 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 1,010,585 | 10.106 | 20 | 20 | fits | 85,969 | 28 | 0.604 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 344,259 | 3.443 | 20 | 20 | fits | 109,711 | 184 | 0.397 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 296,968 | 2.970 | 20 | 200 | fits | 150,424 | 214 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 406,063 | 4.061 | 20 | 200 | fits | 109,711 | 184 | 0.397 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 297,892 | 2.979 | 20 | 20 | fits | 150,424 | 214 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 406,767 | 4.068 | 20 | 20 | fits | 109,711 | 184 | 0.397 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 151,108 | 1.511 | 20 | 24 | fits | 143,494 | 142 | 0.407 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 300,542 | 3.005 | 20 | 24 | fits | 150,424 | 214 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 300,476 | 3.005 | 20 | 50 | fits | 150,424 | 214 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 409,791 | 4.098 | 20 | 50 | fits | 109,711 | 184 | 0.397 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 491,104 | 4.911 | 20 | 20 | fits | 81,379 | 33 | 0.803 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 1,003,690 | 10.037 | 20 | 20 | fits | 73,227 | 24 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 363,181 | 3.632 | 20 | 20 | fits | 120,423 | 200 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 290,982 | 2.910 | 20 | 200 | fits | 149,133 | 210 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 410,789 | 4.108 | 20 | 200 | fits | 120,423 | 200 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 291,906 | 2.919 | 20 | 20 | fits | 149,133 | 210 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 411,493 | 4.115 | 20 | 20 | fits | 120,423 | 200 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 146,413 | 1.464 | 20 | 24 | fits | 143,427 | 142 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 294,556 | 2.946 | 20 | 24 | fits | 149,133 | 210 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 294,490 | 2.945 | 20 | 50 | fits | 149,133 | 210 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 414,517 | 4.145 | 20 | 50 | fits | 120,423 | 200 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 510,307 | 5.103 | 20 | 20 | fits | 86,292 | 25 | 0.778 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 997,724 | 9.977 | 20 | 20 | fits | 60,187 | 20 | 0.692 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 362,272 | 3.623 | 20 | 20 | fits | 123,814 | 187 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 286,184 | 2.862 | 20 | 200 | fits | 149,380 | 231 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 418,554 | 4.186 | 20 | 200 | fits | 123,814 | 187 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 287,108 | 2.871 | 20 | 20 | fits | 149,380 | 231 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 419,258 | 4.193 | 20 | 20 | fits | 123,814 | 187 | 0.430 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 141,368 | 1.414 | 20 | 24 | fits | 143,494 | 142 | 0.407 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 289,758 | 2.898 | 20 | 24 | fits | 149,380 | 231 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 289,692 | 2.897 | 20 | 50 | fits | 149,380 | 231 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 422,282 | 4.223 | 20 | 50 | fits | 123,814 | 187 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 508,036 | 5.080 | 20 | 20 | fits | 85,820 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 994,694 | 9.947 | 20 | 20 | fits | 60,074 | 20 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 351,225 | 3.512 | 20 | 20 | fits | 111,429 | 175 | 0.373 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 295,335 | 2.953 | 20 | 200 | fits | 148,168 | 225 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 406,148 | 4.061 | 20 | 200 | fits | 111,429 | 175 | 0.373 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 296,259 | 2.963 | 20 | 20 | fits | 148,168 | 225 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 406,852 | 4.069 | 20 | 20 | fits | 111,429 | 175 | 0.373 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 151,731 | 1.517 | 20 | 24 | fits | 143,367 | 142 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 298,909 | 2.989 | 20 | 24 | fits | 148,168 | 225 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 298,843 | 2.988 | 20 | 50 | fits | 148,168 | 225 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 409,876 | 4.099 | 20 | 50 | fits | 111,429 | 175 | 0.373 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 495,735 | 4.957 | 20 | 20 | fits | 85,925 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 1,000,458 | 10.005 | 20 | 20 | fits | 73,407 | 24 | 0.646 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 340,564 | 3.406 | 20 | 20 | fits | 109,669 | 184 | 0.397 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 293,360 | 2.934 | 20 | 200 | fits | 150,816 | 214 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 402,413 | 4.024 | 20 | 200 | fits | 109,669 | 184 | 0.397 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 294,284 | 2.943 | 20 | 20 | fits | 150,816 | 214 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 403,117 | 4.031 | 20 | 20 | fits | 109,669 | 184 | 0.397 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 147,108 | 1.471 | 20 | 24 | fits | 143,372 | 142 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 296,934 | 2.969 | 20 | 24 | fits | 150,816 | 214 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 296,868 | 2.969 | 20 | 50 | fits | 150,816 | 214 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 406,141 | 4.061 | 20 | 50 | fits | 109,669 | 184 | 0.397 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 491,961 | 4.920 | 20 | 20 | fits | 85,886 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 1,081,231 | 10.812 | 20 | 20 | fits | 86,066 | 29 | 0.611 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 348,846 | 3.488 | 20 | 20 | fits | 109,804 | 188 | 0.381 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 287,562 | 2.876 | 20 | 200 | fits | 150,885 | 215 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 396,750 | 3.967 | 20 | 200 | fits | 109,804 | 188 | 0.381 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 288,486 | 2.885 | 20 | 20 | fits | 150,885 | 215 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 397,454 | 3.975 | 20 | 20 | fits | 109,804 | 188 | 0.381 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 141,241 | 1.412 | 20 | 24 | fits | 143,367 | 142 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 291,136 | 2.911 | 20 | 24 | fits | 150,885 | 215 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 291,070 | 2.911 | 20 | 50 | fits | 150,885 | 215 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 400,478 | 4.005 | 20 | 50 | fits | 109,804 | 188 | 0.381 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 499,810 | 4.998 | 20 | 20 | fits | 89,741 | 31 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,073,174 | 10.732 | 20 | 20 | fits | 73,249 | 24 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 362,594 | 3.626 | 20 | 20 | fits | 114,529 | 191 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 301,642 | 3.016 | 20 | 200 | fits | 151,163 | 215 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 425,059 | 4.251 | 20 | 200 | fits | 114,529 | 191 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 302,566 | 3.026 | 20 | 20 | fits | 151,163 | 215 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 425,763 | 4.258 | 20 | 20 | fits | 114,529 | 191 | 0.430 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 155,043 | 1.550 | 20 | 24 | fits | 143,367 | 142 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 305,216 | 3.052 | 20 | 24 | fits | 151,163 | 215 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 305,150 | 3.051 | 20 | 50 | fits | 151,163 | 215 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 428,787 | 4.288 | 20 | 50 | fits | 114,529 | 191 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 514,652 | 5.147 | 20 | 20 | fits | 85,931 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,087,657 | 10.877 | 20 | 20 | fits | 73,357 | 25 | 0.641 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 367,219 | 3.672 | 20 | 20 | fits | 109,641 | 187 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 305,913 | 3.059 | 20 | 200 | fits | 150,953 | 215 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 414,938 | 4.149 | 20 | 200 | fits | 109,641 | 187 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 306,837 | 3.068 | 20 | 20 | fits | 150,953 | 215 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 415,642 | 4.156 | 20 | 20 | fits | 109,641 | 187 | 0.379 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 150,586 | 1.506 | 20 | 24 | fits | 143,538 | 143 | 0.407 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 309,487 | 3.095 | 20 | 24 | fits | 150,953 | 215 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 309,421 | 3.094 | 20 | 50 | fits | 150,953 | 215 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 418,666 | 4.187 | 20 | 50 | fits | 109,641 | 187 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 504,384 | 5.044 | 20 | 20 | fits | 85,784 | 24 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,092,310 | 10.923 | 20 | 20 | fits | 78,797 | 31 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 355,423 | 3.554 | 20 | 20 | fits | 112,143 | 175 | 0.381 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 299,311 | 2.993 | 20 | 200 | fits | 149,405 | 230 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 410,838 | 4.108 | 20 | 200 | fits | 112,143 | 175 | 0.381 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 300,235 | 3.002 | 20 | 20 | fits | 149,405 | 230 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 411,542 | 4.115 | 20 | 20 | fits | 112,143 | 175 | 0.381 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 145,597 | 1.456 | 20 | 24 | fits | 143,177 | 143 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 302,885 | 3.029 | 20 | 24 | fits | 149,405 | 230 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 302,819 | 3.028 | 20 | 50 | fits | 149,405 | 230 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 414,566 | 4.146 | 20 | 50 | fits | 112,143 | 175 | 0.381 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 492,892 | 4.929 | 20 | 20 | fits | 78,392 | 26 | 0.816 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,087,593 | 10.876 | 20 | 20 | fits | 87,699 | 29 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 342,097 | 3.421 | 20 | 20 | fits | 117,699 | 190 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 287,049 | 2.870 | 20 | 200 | fits | 151,989 | 219 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 404,132 | 4.041 | 20 | 200 | fits | 117,699 | 190 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 287,973 | 2.880 | 20 | 20 | fits | 151,989 | 219 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 404,836 | 4.048 | 20 | 20 | fits | 117,699 | 190 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 139,624 | 1.396 | 20 | 24 | fits | 143,367 | 142 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 290,623 | 2.906 | 20 | 24 | fits | 151,989 | 219 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 290,557 | 2.906 | 20 | 50 | fits | 151,989 | 219 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 407,860 | 4.079 | 20 | 50 | fits | 117,699 | 190 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 571,081 | 5.711 | 20 | 20 | fits | 85,542 | 25 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,075,432 | 10.754 | 20 | 20 | fits | 73,399 | 24 | 0.646 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 434,396 | 4.344 | 20 | 20 | fits | 116,513 | 196 | 0.369 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 296,214 | 2.962 | 20 | 200 | fits | 148,586 | 208 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 489,633 | 4.896 | 20 | 200 | fits | 116,513 | 196 | 0.369 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 297,138 | 2.971 | 20 | 20 | fits | 148,586 | 208 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 490,337 | 4.903 | 20 | 20 | fits | 116,513 | 196 | 0.369 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 152,192 | 1.522 | 20 | 24 | fits | 143,367 | 142 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 299,788 | 2.998 | 20 | 24 | fits | 148,586 | 208 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 299,722 | 2.997 | 20 | 50 | fits | 148,586 | 208 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 493,361 | 4.934 | 20 | 50 | fits | 116,513 | 196 | 0.369 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 579,473 | 5.795 | 20 | 20 | fits | 86,178 | 25 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,084,388 | 10.844 | 20 | 20 | fits | 73,407 | 24 | 0.646 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 371,542 | 3.715 | 20 | 20 | fits | 109,641 | 187 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 310,236 | 3.102 | 20 | 200 | fits | 150,953 | 215 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 419,261 | 4.193 | 20 | 200 | fits | 109,641 | 187 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 311,160 | 3.112 | 20 | 20 | fits | 150,953 | 215 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 419,965 | 4.200 | 20 | 20 | fits | 109,641 | 187 | 0.379 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 155,025 | 1.550 | 20 | 24 | fits | 143,631 | 143 | 0.407 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 313,810 | 3.138 | 20 | 24 | fits | 150,953 | 215 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 313,744 | 3.137 | 20 | 50 | fits | 150,953 | 215 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 422,989 | 4.230 | 20 | 50 | fits | 109,641 | 187 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 508,707 | 5.087 | 20 | 20 | fits | 85,784 | 24 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 1,006,818 | 10.068 | 20 | 20 | fits | 70,714 | 33 | 0.738 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 346,921 | 3.469 | 20 | 20 | fits | 111,471 | 175 | 0.373 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 290,944 | 2.909 | 20 | 200 | fits | 148,080 | 225 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 401,799 | 4.018 | 20 | 200 | fits | 111,471 | 175 | 0.373 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 291,868 | 2.919 | 20 | 20 | fits | 148,080 | 225 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 402,503 | 4.025 | 20 | 20 | fits | 111,471 | 175 | 0.373 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 147,428 | 1.474 | 20 | 24 | fits | 143,367 | 142 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 294,518 | 2.945 | 20 | 24 | fits | 148,080 | 225 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 294,452 | 2.945 | 20 | 50 | fits | 148,080 | 225 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 405,527 | 4.055 | 20 | 50 | fits | 111,471 | 175 | 0.373 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 491,360 | 4.914 | 20 | 20 | fits | 85,899 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 1,002,182 | 10.022 | 20 | 20 | fits | 85,753 | 28 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 336,109 | 3.361 | 20 | 20 | fits | 109,792 | 184 | 0.398 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 288,737 | 2.887 | 20 | 200 | fits | 152,055 | 219 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 397,913 | 3.979 | 20 | 200 | fits | 109,792 | 184 | 0.398 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 289,661 | 2.897 | 20 | 20 | fits | 152,055 | 219 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 398,617 | 3.986 | 20 | 20 | fits | 109,792 | 184 | 0.398 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 141,246 | 1.412 | 20 | 24 | fits | 143,372 | 142 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 292,311 | 2.923 | 20 | 24 | fits | 152,055 | 219 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 292,245 | 2.922 | 20 | 50 | fits | 152,055 | 219 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 401,641 | 4.016 | 20 | 50 | fits | 109,792 | 184 | 0.398 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 487,435 | 4.874 | 20 | 20 | fits | 85,860 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 998,060 | 9.981 | 20 | 20 | fits | 85,789 | 28 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 354,950 | 3.550 | 20 | 20 | fits | 111,471 | 175 | 0.373 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 298,973 | 2.990 | 20 | 200 | fits | 148,164 | 225 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 409,828 | 4.098 | 20 | 200 | fits | 111,471 | 175 | 0.373 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 299,897 | 2.999 | 20 | 20 | fits | 148,164 | 225 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 410,532 | 4.105 | 20 | 20 | fits | 111,471 | 175 | 0.373 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 155,373 | 1.554 | 20 | 24 | fits | 143,372 | 142 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 302,547 | 3.025 | 20 | 24 | fits | 148,164 | 225 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 302,481 | 3.025 | 20 | 50 | fits | 148,164 | 225 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 413,556 | 4.136 | 20 | 50 | fits | 111,471 | 175 | 0.373 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 499,523 | 4.995 | 20 | 20 | fits | 86,033 | 25 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 1,010,191 | 10.102 | 20 | 20 | fits | 85,797 | 28 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 344,162 | 3.442 | 20 | 20 | fits | 109,925 | 185 | 0.399 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 296,871 | 2.969 | 20 | 200 | fits | 150,695 | 214 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 406,180 | 4.062 | 20 | 200 | fits | 109,925 | 185 | 0.399 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 297,795 | 2.978 | 20 | 20 | fits | 150,695 | 214 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 406,884 | 4.069 | 20 | 20 | fits | 109,925 | 185 | 0.399 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 150,740 | 1.507 | 20 | 24 | fits | 143,367 | 142 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 300,445 | 3.004 | 20 | 24 | fits | 150,695 | 214 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 300,379 | 3.004 | 20 | 50 | fits | 150,695 | 214 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 409,908 | 4.099 | 20 | 50 | fits | 109,925 | 185 | 0.399 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 509,060 | 5.091 | 20 | 20 | fits | 89,732 | 31 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 1,003,957 | 10.040 | 20 | 20 | fits | 73,227 | 24 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 365,803 | 3.658 | 20 | 20 | fits | 114,461 | 194 | 0.413 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 291,221 | 2.912 | 20 | 200 | fits | 149,668 | 211 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 414,238 | 4.142 | 20 | 200 | fits | 114,461 | 194 | 0.413 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 292,145 | 2.921 | 20 | 20 | fits | 149,668 | 211 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 414,942 | 4.149 | 20 | 20 | fits | 114,461 | 194 | 0.413 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 146,117 | 1.461 | 20 | 24 | fits | 143,372 | 142 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 294,795 | 2.948 | 20 | 24 | fits | 149,668 | 211 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 294,729 | 2.947 | 20 | 50 | fits | 149,668 | 211 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 417,966 | 4.180 | 20 | 50 | fits | 114,461 | 194 | 0.413 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 496,393 | 4.964 | 20 | 20 | fits | 78,493 | 26 | 0.817 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 996,997 | 9.970 | 20 | 20 | fits | 73,272 | 24 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 360,910 | 3.609 | 20 | 20 | fits | 122,165 | 187 | 0.417 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 295,049 | 2.950 | 20 | 200 | fits | 149,360 | 230 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 416,598 | 4.166 | 20 | 200 | fits | 122,165 | 187 | 0.417 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 295,973 | 2.960 | 20 | 20 | fits | 149,360 | 230 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 417,302 | 4.173 | 20 | 20 | fits | 122,165 | 187 | 0.417 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 141,559 | 1.416 | 20 | 24 | fits | 143,685 | 143 | 0.407 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 298,623 | 2.986 | 20 | 24 | fits | 149,360 | 230 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 298,557 | 2.986 | 20 | 50 | fits | 149,360 | 230 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 420,326 | 4.203 | 20 | 50 | fits | 122,165 | 187 | 0.417 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 506,186 | 5.062 | 20 | 20 | fits | 85,926 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 1,009,433 | 10.094 | 20 | 20 | fits | 66,291 | 27 | 0.755 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 364,384 | 3.644 | 20 | 20 | fits | 117,075 | 196 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 296,709 | 2.967 | 20 | 200 | fits | 149,076 | 208 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 413,168 | 4.132 | 20 | 200 | fits | 117,075 | 196 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 297,633 | 2.976 | 20 | 20 | fits | 149,076 | 208 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 413,872 | 4.139 | 20 | 20 | fits | 117,075 | 196 | 0.372 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 152,197 | 1.522 | 20 | 24 | fits | 143,428 | 142 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 300,283 | 3.003 | 20 | 24 | fits | 149,076 | 208 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 300,217 | 3.002 | 20 | 50 | fits | 149,076 | 208 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 416,896 | 4.169 | 20 | 50 | fits | 117,075 | 196 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 502,761 | 5.028 | 20 | 20 | fits | 85,931 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 1,007,516 | 10.075 | 20 | 20 | fits | 73,347 | 24 | 0.648 |
| LINK_UP | `adp.link_up.if0` | 2,795 | 0.028 | 20 | 200 | fits | 27,707 | 43 (11) | 0.749 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,382 | 0.084 | 20 | 200 | fits | 23,408 | 23 (39) | 0.755 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 9,125 | 0.091 | 20 | 200 | fits | 2,681 | 10 (11) | 0.556 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 155,796 | 1.558 | 20 | 200 | fits | 156,736 | 272 | 0.455 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 229,950 | 2.300 | 20 | 20 | fits | 94,291 | 65 | 0.689 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 302,056 | 3.021 | 20 | 24 | fits | 82,274 | 49 | 0.575 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 190,475 | 1.905 | 20 | 50 | fits | 94,291 | 65 | 0.689 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 911,494 | 9.115 | 20 | 20 | fits | 85,857 | 28 | 0.605 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 246,589 | 2.466 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 155,796 | 1.558 | 20 | 200 | fits | 156,736 | 272 | 0.455 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 194,762 | 1.948 | 20 | 20 | fits | 143,885 | 269 | 0.341 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 288,746 | 2.887 | 20 | 24 | fits | 85,678 | 55 | 0.595 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 179,908 | 1.799 | 20 | 50 | fits | 83,724 | 67 | 0.711 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 986,757 | 9.868 | 20 | 20 | fits | 64,155 | 26 | 0.728 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 273,845 | 2.738 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 9,939 | 0.099 | 20 | 20 | fits | 32,748 | 28 (35) | 0.802 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 6,532 | 0.065 | 20 | 20 | fits | 29,935 | 24 (14) | 0.837 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 13,842 | 0.138 | 20 | 20 | fits | 29,400 | 24 (14) | 0.845 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 23,402 | 0.234 | 20 | 20 | fits | 30,146 | 21 (35) | 0.826 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 78,464 | 0.785 | 20 | 20 | fits | 28,326 | 8 | 0.753 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 45,222 | 0.452 | 20 | 20 | fits | 45,288 | 12 | 0.895 |
| malformed MRPDU discard | `srp.malformed.if0` | 22,129 | 0.221 | 20 | 20 | fits | 22,195 | 12 | 0.714 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 89,051 | 0.891 | 220 | 220 | fits | 56,000 | 6 | 0.897 |
| an event behind 15 others | `backlog.event.if0` | 161,163 | 1.612 | 20 | 200 | fits | 57,646 | 79 | 0.587 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 422,103 | 4.221 | 20 | 20 | fits | 40,500 | 63 | 0.329 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 417,385 | 4.174 | 20 | 200 | fits | 151,768 | 168 | 0.392 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 416,769 | 4.168 | 20 | 200 | fits | 151,768 | 168 | 0.392 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 413,063 | 4.131 | 20 | 20 | fits | 151,768 | 168 | 0.392 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 452,727 | 4.527 | 20 | 20 | fits | 40,500 | 63 | 0.329 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 146,431 | 1.464 | 20 | 24 | fits | 147,322 | 148 | 0.411 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 415,713 | 4.157 | 20 | 24 | fits | 151,768 | 168 | 0.392 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 415,647 | 4.156 | 20 | 50 | fits | 151,768 | 168 | 0.392 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 415,251 | 4.153 | 20 | 50 | fits | 151,768 | 168 | 0.392 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 455,685 | 4.557 | 20 | 20 | fits | 40,500 | 63 | 0.329 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 515,438 | 5.154 | 20 | 20 | fits | 24,419 | 41 | 0.158 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 362,402 | 3.624 | 20 | 20 | fits | 114,313 | 194 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 287,926 | 2.879 | 20 | 200 | fits | 149,212 | 211 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 410,842 | 4.108 | 20 | 200 | fits | 114,313 | 194 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 288,850 | 2.889 | 20 | 20 | fits | 149,212 | 211 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 411,546 | 4.115 | 20 | 20 | fits | 114,313 | 194 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 143,278 | 1.433 | 20 | 24 | fits | 143,464 | 145 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 291,500 | 2.915 | 20 | 24 | fits | 149,212 | 211 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 291,434 | 2.914 | 20 | 50 | fits | 149,212 | 211 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 414,570 | 4.146 | 20 | 50 | fits | 114,313 | 194 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 500,491 | 5.005 | 20 | 20 | fits | 85,987 | 24 | 0.780 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 995,567 | 9.956 | 20 | 20 | fits | 73,267 | 24 | 0.642 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 16,781 | 0.168 | 20 | 20 | fits | 27,500 | 19 | 0.816 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 287,926 | 2.879 | 20 | 200 | fits | 149,212 | 211 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 35,667 | 0.357 | 20 | 200 | fits | 27,500 | 19 | 0.816 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 288,850 | 2.889 | 20 | 20 | fits | 149,212 | 211 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 402,736 | 4.027 | 20 | 20 | fits | 105,503 | 184 | 0.384 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 143,278 | 1.433 | 20 | 24 | fits | 143,464 | 145 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 291,500 | 2.915 | 20 | 24 | fits | 149,212 | 211 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 291,434 | 2.914 | 20 | 50 | fits | 149,212 | 211 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 405,760 | 4.058 | 20 | 50 | fits | 105,503 | 184 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 491,288 | 4.913 | 20 | 20 | fits | 85,594 | 24 | 0.780 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 986,430 | 9.864 | 20 | 20 | fits | 73,267 | 24 | 0.642 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,291,737 | 62.917 | 20 | 20 | MISS ceiling | 18,756 | 13 | 0.616 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,310,491 | 63.105 | 20 | 20 | MISS ceiling | 18,830 | 13 | 0.600 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,329,248 | 63.292 | 20 | 20 | MISS ceiling | 18,814 | 13 | 0.600 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,347,917 | 63.479 | 20 | 20 | MISS ceiling | 18,745 | 13 | 0.608 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,366,507 | 63.665 | 20 | 20 | MISS ceiling | 18,652 | 13 | 0.625 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 151,915 | 1.519 | 20 | 200 | fits | 148,431 | 222 | 0.425 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 238,715 | 2.387 | 20 | 200 | fits | 87,416 | 164 | 0.361 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 147,593 | 1.476 | 20 | 20 | fits | 148,431 | 222 | 0.425 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,201,260 | 62.013 | 20 | 20 | MISS ceiling | 29,449 | 15 | 0.756 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 151,233 | 1.512 | 20 | 24 | fits | 148,431 | 222 | 0.425 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,175,297 | 61.753 | 20 | 24 | MISS ceiling | 142,285 | 106 | 0.429 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 150,177 | 1.502 | 20 | 50 | fits | 148,431 | 222 | 0.425 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 237,197 | 2.372 | 20 | 50 | fits | 87,416 | 164 | 0.361 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 322,213 | 3.222 | 20 | 20 | fits | 85,082 | 24 | 0.764 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 816,970 | 8.170 | 20 | 20 | fits | 73,204 | 24 | 0.635 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,919 | 0.059 | 20 | 20 | fits | 24,883 | 13 (29) | 0.807 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,248 | 0.072 | 20 | 20 | fits | 26,783 | 19 (35) | 0.806 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 19,721 | 0.197 | 20 | 20 | fits | 30,223 | 21 (12) | 0.829 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 10,448 | 0.104 | 20 | 50 | fits | 27,707 | 43 | 0.749 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 13,562 | 0.136 | 20 | 50 | fits | 24,444 | 35 | 0.735 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 16,158 | 0.162 | 20 | 50 | fits | 24,295 | 35 | 0.737 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 15,326 | 0.153 | 20 | 50 | fits | 28,800 | 61 | 0.652 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 17,565 | 0.176 | 20 | 50 | fits | 28,800 | 61 | 0.652 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 9,561 | 0.096 | 20 | 50 | fits | 22,593 | 30 | 0.650 |
| LINK_UP | `adp.link_up.if0` | 2,795 | 0.028 | 20 | 200 | fits | 27,707 | 43 (11) | 0.749 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,382 | 0.084 | 20 | 200 | fits | 23,408 | 23 (39) | 0.755 |
| LINK_DOWN | `adp.link_down.if0` | 2,472 | 0.025 | 20 | 200 | fits | 25,252 | 23 (9) | 0.786 |
| LINK_UP | `adp.link_up.if0` | 2,795 | 0.028 | 20 | 200 | fits | 27,707 | 43 (11) | 0.749 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,382 | 0.084 | 20 | 200 | fits | 23,408 | 23 (39) | 0.755 |
| GM_CHANGE | `adp.gm_change.if0` | 2,448 | 0.024 | 20 | 200 | fits | 18,011 | 17 (11) | 0.759 |
| LINK_UP | `adp.link_up.if0` | 2,795 | 0.028 | 20 | 200 | fits | 27,707 | 43 (11) | 0.749 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,382 | 0.084 | 20 | 200 | fits | 23,408 | 23 (39) | 0.755 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 5,066 | 0.051 | 20 | 200 | fits | 17,161 | 16 (31) | 0.642 |
| LINK_UP | `adp.link_up.if0` | 2,795 | 0.028 | 20 | 200 | fits | 27,707 | 43 (11) | 0.749 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,382 | 0.084 | 20 | 200 | fits | 23,408 | 23 (39) | 0.755 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 5,066 | 0.051 | 20 | 200 | fits | 17,161 | 16 (31) | 0.642 |
| set_name | `aecp_fanout.set_name.if0` | 59,033 | 0.590 | 20 | 24 | fits | 63,569 | 89 | 0.589 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 52,279 | 0.523 | 20 | 24 | fits | 56,788 | 78 | 0.602 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 57,730 | 0.577 | 20 | 24 | fits | 55,028 | 79 | 0.568 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 50,042 | 0.500 | 20 | 24 | fits | 51,920 | 78 | 0.561 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 59,788 | 0.598 | 20 | 24 | fits | 60,391 | 66 | 0.632 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 326,433 | 3.264 | 20 | 24 | fits | 58,143 | 65 | 0.629 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 332,057 | 3.321 | 20 | 24 | fits | 53,344 | 67 | 0.590 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 49,422 | 0.494 | 20 | 24 | fits | 51,334 | 78 | 0.562 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 50,013 | 0.500 | 20 | 24 | fits | 51,643 | 79 | 0.561 |
| BIND_RX | `acmp.bind_rx.if0` | 18,781 | 0.188 | 20 | 20 | fits | 41,273 | 26 (77) | 0.796 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,531 | 0.095 | 20 | 20 | fits | 32,927 | 19 (32) | 0.832 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,682 | 0.107 | 20 | 20 | fits | 26,324 | 15 (47) | 0.782 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,509 | 0.135 | 20 | 20 | fits | 39,622 | 18 (50) | 0.828 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,453 | 0.105 | 20 | 20 | fits | 26,179 | 17 (48) | 0.761 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 10,020 | 0.100 | 20 | 20 | fits | 24,673 | 16 (48) | 0.718 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,487 | 0.095 | 20 | 20 | fits | 23,933 | 16 (48) | 0.713 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 8,881 | 0.089 | 20 | 20 | fits | 23,942 | 16 (48) | 0.715 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 17,586 | 0.176 | 20 | 24 | fits | 28,466 | 20 | 0.785 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 29,054 | 0.291 | 20 | 24 | fits | 32,847 | 20 | 0.723 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 20,204 | 0.202 | 20 | 24 | fits | 28,339 | 20 | 0.746 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 24,552 | 0.246 | 20 | 24 | fits | 27,948 | 20 | 0.739 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 24,766 | 0.248 | 20 | 24 | fits | 33,424 | 26 | 0.745 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 20,479 | 0.205 | 20 | 24 | fits | 28,529 | 20 | 0.743 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 24,644 | 0.246 | 20 | 24 | fits | 27,473 | 20 | 0.743 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 19,715 | 0.197 | 20 | 24 | fits | 27,765 | 20 | 0.757 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 24,008 | 0.240 | 20 | 24 | fits | 27,009 | 20 | 0.756 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 21,973 | 0.220 | 20 | 24 | fits | 29,850 | 21 | 0.656 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 23,770 | 0.238 | 20 | 24 | fits | 26,723 | 20 | 0.772 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 23,711 | 0.237 | 20 | 24 | fits | 27,000 | 20 | 0.772 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 19,431 | 0.194 | 20 | 24 | fits | 27,481 | 20 | 0.741 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 24,940 | 0.249 | 20 | 24 | fits | 28,267 | 20 | 0.747 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 19,740 | 0.197 | 20 | 24 | fits | 27,956 | 20 | 0.757 |
| get_configuration | `aecp.get_configuration.if0` | 22,101 | 0.221 | 20 | 24 | fits | 24,485 | 20 | 0.741 |
| entity_available | `aecp.entity_available.if0` | 22,160 | 0.222 | 20 | 24 | fits | 24,752 | 20 | 0.742 |
| get_name | `aecp.get_name.if0` | 19,851 | 0.199 | 20 | 24 | fits | 27,893 | 20 | 0.754 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 25,502 | 0.255 | 20 | 24 | fits | 28,516 | 27 | 0.730 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 20,932 | 0.209 | 20 | 24 | fits | 28,969 | 29 | 0.764 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 22,986 | 0.230 | 20 | 24 | fits | 25,771 | 20 | 0.770 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 9,372 | 0.094 | 20 | 24 | fits | 24,448 | 20 | 0.736 |
| set_name | `aecp.set_name.if0` | 26,511 | 0.265 | 20 | 24 | fits | 44,791 | 43 | 0.766 |
| lock_entity | `aecp.lock_entity.if0` | 28,621 | 0.286 | 20 | 24 | fits | 36,129 | 34 | 0.783 |
| unlock_entity | `aecp.unlock_entity.if0` | 24,933 | 0.249 | 20 | 24 | fits | 37,560 | 33 | 0.787 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 142,114 | 1.421 | 20 | 24 | fits | 147,151 | 92 | 0.339 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 304,292 | 3.043 | 20 | 24 | fits | 136,693 | 70 | 0.306 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 204,285 | 2.043 | 20 | 24 | fits | 41,418 | 17 | 0.686 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 382,285 | 3.823 | 20 | 24 | fits | 91,808 | 18 | 0.665 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 296,677 | 2.967 | 20 | 24 | fits | 93,601 | 17 | 0.673 |
| LINK_UP | `fixture.link_up.if0` | 2,795 | 0.028 | 20 | 200 | fits | 27,707 | 43 (11) | 0.749 |
| malformed MRPDU discard | `fixture.malformed.if0` | 22,578 | 0.226 | 20 | 20 | fits | 22,644 | 12 | 0.750 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 31,559 | 0.316 | 20 | 24 | fits | 46,940 | 43 | 0.785 |
| LINK_DOWN | `fixture.link_down.if0` | 2,882 | 0.029 | 20 | 200 | fits | 27,198 | 23 (9) | 0.804 |
| BIND_RX | `fixture.bind_rx.if0` | 19,520 | 0.195 | 20 | 20 | fits | 41,919 | 26 (77) | 0.806 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 23,367 | 0.234 | 20 | 20 | fits | 36,859 | 29 (35) | 0.790 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 14,468 | 0.145 | 20 | 20 | fits | 25,776 | 13 (29) | 0.826 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 81,613 | 0.816 | 20 | 200 | fits | 81,717 | 51 | 0.757 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 81,613 | 0.816 | 20 | 200 | fits | 81,717 | 51 | 0.757 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 81,339 | 0.813 | 20 | 20 | fits | 81,717 | 51 | 0.757 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 81,339 | 0.813 | 20 | 20 | fits | 81,717 | 51 | 0.757 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 81,547 | 0.815 | 20 | 24 | fits | 81,717 | 51 | 0.757 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 81,547 | 0.815 | 20 | 24 | fits | 81,717 | 51 | 0.757 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 81,481 | 0.815 | 20 | 50 | fits | 81,717 | 51 | 0.757 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 81,481 | 0.815 | 20 | 50 | fits | 81,717 | 51 | 0.757 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 81,415 | 0.814 | 20 | 20 | fits | 81,717 | 51 | 0.757 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 81,415 | 0.814 | 20 | 20 | fits | 81,717 | 51 | 0.757 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
