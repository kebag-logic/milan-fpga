### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 98 paths and 7 of 968 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.183 (0.379) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.085 (0.201) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.091 (0.248) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.105 (0.405) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.101 (0.214) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.084 (0.199) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.088 (0.209) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.107 (0.228) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.092 (0.276) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.107 (0.378) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.208 (0.483) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.171 (0.448) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.128 (0.438) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.100 (0.425) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.160 (0.427) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.127 (0.341) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.050 (0.133) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.020 (0.116) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.023 (0.210) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.022 (0.221) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.043 (0.168) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.131 (0.365) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.171 (0.424) | fits | 0 aecp | 1 | 0 |
| get_as_path, refused ENTITY_MISBEHAVING | 0 | `aecp.get_as_path.if0` (aecp) | 0.113 (0.253) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.207 (0.472) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.189 (0.440) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.209 (0.472) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.213 (0.470) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR held for a token (#917) | 0 | `aecp.held.read_descriptor.if0` (aecp-held) | 5.203 (5.463) | fits | 16 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.147 (0.339) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.136 (0.379) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.244 (0.506) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.198 (0.461) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.193 (0.452) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.204 (0.460) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.213 (0.473) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.200 (0.457) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.204 (0.469) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.207 (0.465) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.188 (0.457) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.214 (0.472) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.188 (0.449) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.206 (0.371) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.196 (0.466) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.206 (0.462) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.151 (0.406) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.261 (0.629) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.174 (0.430) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.232 (0.560) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 3.179 (3.479) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.377 (0.644) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.536 (0.816) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.446 (0.714) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.422 (0.653) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.447 (0.731) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 2.825 (3.079) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.426 (0.662) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 2.706 (2.981) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.417 (2.728) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.866 (4.173) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.485 (3.793) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.309 (1.599) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.522 (3.727) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 4.142 (4.697) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.083 (0.371) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.559 (1.913) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.602 (62.835) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.215 (63.445) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.312 (0.443) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 2.087 | fits | 11 acmp | 4 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-burst.held.adp.if0` (save-burst) | 1.539 | fits | 7 adp | 4 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-flight.held.aecp.if0` (save-flight) | 2.618 | fits | 14 aecp | 4 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 2.116 | fits | 6 maap | 4 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 7.602 | fits | 31 srp | 4 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.202 (0.454) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.083 (0.187) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.096 (0.221) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.182 (0.454) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.161 (0.417) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.468 | fits | 0 srp | 4 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@program-6.service.acmp.first.if0` (backlog-adp@program-6) | 3.838 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 61.862 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@program-6.service.adp.first.if0` (backlog-adp@program-6) | 3.829 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-6.service.adp.last.if0` (backlog-adp@program-6) | 4.840 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@program-6.service.aecp.first.if0` (backlog-adp@program-6) | 2.292 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.645 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@program-6.service.maap.first.if0` (backlog-adp@program-6) | 3.864 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-6.service.maap.last.if0` (backlog-adp@program-6) | 4.878 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-6.service.srp.first.if0` (backlog-adp@blank-aged2-6) | 5.539 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-3.service.srp.last.if0` (backlog-adp@program-aged2-3) | 9.238 | fits | 31 srp | 77 | 0 |
| Talker Advertise RX for every input, bound | 0 | `srp.bound_advertise.if0` (srp-bound) | 0.646 (0.646) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.719 (0.809) | fits | 0 srp | 1 | 0 |
| Talker Advertise RX for every input, no binding (kept) | 0 | `srp.kept_advertise.if0` (srp-kept) | 0.487 (0.488) | fits | 0 srp | 1 | 0 |
| Talker Failed RX for every input, no binding (kept) | 0 | `srp.kept_failed.if0` (srp-kept) | 0.517 (0.518) | fits | 0 srp | 1 | 0 |
| Talker RX at the bound after a freed block (count) | 0 | `srp.kept_recount.if0` (srp-kept) | 0.466 (0.467) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.350 (0.351) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.170 (0.170) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.694 (0.777) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.750 | 10 | 146,500 (1.465) | yes | - |
| backlog-adp@blank-1 | 0 | 11.625 | 10 | 146,500 (1.465) | yes | - |
| backlog-adp@blank-2 | 0 | 11.500 | 10 | 146,500 (1.465) | yes | - |
| backlog-adp@blank-3 | 0 | 11.375 | 10 | 146,500 (1.465) | yes | - |
| backlog-adp@blank-4 | 0 | 11.250 | 10 | 146,500 (1.465) | yes | - |
| backlog-adp@blank-5 | 0 | 11.125 | 10 | 146,500 (1.465) | yes | - |
| backlog-adp@blank-6 | 0 | 11.000 | 10 | 146,500 (1.465) | yes | - |
| backlog-adp@blank-7 | 0 | 14.732 | 13 | 147,943 (1.479) | yes | - |
| backlog-adp@program-0 | 0 | 9.755 | 10 | 147,627 (1.476) | yes | - |
| backlog-adp@program-1 | 0 | 10.429 | 10 | 147,684 (1.477) | yes | - |
| backlog-adp@program-2 | 0 | 11.653 | 12 | 146,842 (1.468) | yes | - |
| backlog-adp@program-3 | 0 | 11.403 | 12 | 146,842 (1.468) | yes | - |
| backlog-adp@program-4 | 0 | 11.153 | 12 | 146,842 (1.468) | yes | - |
| backlog-adp@program-5 | 0 | 10.903 | 11 | 143,961 (1.440) | yes | - |
| backlog-adp@program-6 | 0 | 11.748 | 12 | 148,039 (1.480) | yes | - |
| backlog-adp@program-7 | 0 | 11.498 | 12 | 148,039 (1.480) | yes | - |
| backlog-adp@verify-0 | 0 | 13.722 | 12 | 147,008 (1.470) | yes | - |
| backlog-adp@verify-1 | 0 | 13.597 | 12 | 147,008 (1.470) | yes | - |
| backlog-adp@verify-2 | 0 | 13.472 | 12 | 147,008 (1.470) | yes | - |
| backlog-adp@verify-3 | 0 | 13.347 | 12 | 147,008 (1.470) | yes | - |
| backlog-adp@verify-4 | 0 | 13.222 | 12 | 147,008 (1.470) | yes | - |
| backlog-adp@verify-5 | 0 | 13.097 | 12 | 147,008 (1.470) | yes | - |
| backlog-adp@verify-6 | 0 | 12.950 | 12 | 147,177 (1.472) | yes | - |
| backlog-adp@verify-7 | 1 | 12.128 | 11 | 148,411 (1.484) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 12.891 | 12 | 144,989 (1.450) | yes | - |
| backlog-adp@blank-aged2-1 | 1 | 12.046 | 12 | 147,528 (1.475) | yes | - |
| backlog-adp@blank-aged2-2 | 1 | 11.720 | 9 | 146,969 (1.470) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 11.808 | 10 | 147,332 (1.473) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 11.774 | 10 | 147,210 (1.472) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 11.730 | 10 | 147,192 (1.472) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 14.795 | 13 | 147,375 (1.474) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 13.771 | 12 | 145,601 (1.456) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 14.813 | 13 | 146,131 (1.461) | yes | - |
| backlog-adp@blank-aged1-1 | 1 | 13.010 | 12 | 148,222 (1.482) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 12.093 | 12 | 145,028 (1.450) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 11.053 | 10 | 147,208 (1.472) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 11.030 | 10 | 147,190 (1.472) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 10.978 | 10 | 146,129 (1.461) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 11.037 | 10 | 147,330 (1.473) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 10.957 | 10 | 146,087 (1.461) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.567 | 11 | 147,360 (1.474) | yes | - |
| backlog-adp@program-aged2-1 | 1 | 10.303 | 10 | 143,114 (1.431) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 10.635 | 11 | 149,011 (1.490) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 10.543 | 10 | 147,430 (1.474) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 10.508 | 10 | 147,417 (1.474) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 10.471 | 10 | 147,295 (1.473) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 10.509 | 10 | 146,214 (1.462) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 10.421 | 10 | 145,038 (1.450) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 11.576 | 11 | 147,277 (1.473) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.456 | 11 | 146,214 (1.462) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 10.401 | 10 | 147,505 (1.475) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 10.361 | 10 | 147,356 (1.474) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 11.751 | 12 | 144,992 (1.450) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 10.386 | 10 | 147,342 (1.473) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 10.437 | 10 | 147,495 (1.475) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 10.397 | 10 | 144,954 (1.450) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 13.035 | 12 | 148,693 (1.487) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 12.105 | 13 | 145,069 (1.451) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 11.833 | 10 | 147,362 (1.474) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 11.800 | 10 | 147,344 (1.473) | yes | - |
| backlog-adp@verify-aged2-4 | 1 | 11.767 | 9 | 147,121 (1.471) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 11.838 | 10 | 147,484 (1.475) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 14.822 | 13 | 147,456 (1.475) | yes | - |
| backlog-adp@verify-aged2-7 | 1 | 13.853 | 12 | 143,505 (1.435) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 14.943 | 13 | 147,362 (1.474) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 13.115 | 13 | 147,447 (1.474) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 12.089 | 12 | 147,825 (1.478) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 11.017 | 10 | 146,150 (1.462) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 10.999 | 9 | 148,239 (1.482) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 11.069 | 10 | 147,266 (1.473) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 11.004 | 10 | 147,248 (1.472) | yes | - |
| backlog-adp@verify-aged1-7 | 1 | 10.956 | 9 | 147,175 (1.472) | yes | - |
| backlog | 0 | 4.869 | 7 | 146,982 (1.470) | yes | - |
| backlog-adp | 0 | 8.722 | 10 | 146,795 (1.468) | yes | - |
| backlog-adp-refill | 0 | 40.602 | 24 | 146,795 (1.468) | yes | - |
| backlog-owed | 0 | 63.719 | 25 | 147,483 (1.475) | yes | - |
| fixture | 0 | 1.152 | 2 | 77,591 (0.776) | yes | - |

Composed maximum over the 4 backlog windows: 147,483 CPU cycles (1.475 ms), backlog-owed.
Over the windows that released their whole load only: 147,483 (1.475 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-kept | 1908 | 0 | 51,789 (0.518) | fits |
| save-flight | 2981 | 0 | 154,693 (1.547) | fits |
| save-burst | 2737 | 0 | 154,693 (1.547) | fits |
| acmp-notk | 3606 | 0 | 46,725 (0.467) | fits |
| save-second | 68898 | 0 | 46,456 (0.465) | fits |
| backlog-adp@blank-0 | 336 | 0 | 146,500 (1.465) | fits |
| backlog-adp@blank-1 | 336 | 0 | 146,500 (1.465) | fits |
| backlog-adp@blank-2 | 336 | 0 | 146,500 (1.465) | fits |
| backlog-adp@blank-3 | 336 | 0 | 146,500 (1.465) | fits |
| backlog-adp@blank-4 | 336 | 0 | 146,500 (1.465) | fits |
| backlog-adp@blank-5 | 336 | 0 | 146,500 (1.465) | fits |
| backlog-adp@blank-6 | 336 | 0 | 146,500 (1.465) | fits |
| backlog-adp@blank-7 | 339 | 0 | 147,943 (1.479) | fits |
| backlog-adp@program-0 | 344 | 0 | 147,627 (1.476) | fits |
| backlog-adp@program-1 | 344 | 0 | 147,684 (1.477) | fits |
| backlog-adp@program-2 | 346 | 0 | 146,842 (1.468) | fits |
| backlog-adp@program-3 | 346 | 0 | 146,842 (1.468) | fits |
| backlog-adp@program-4 | 346 | 0 | 146,842 (1.468) | fits |
| backlog-adp@program-5 | 346 | 0 | 146,842 (1.468) | fits |
| backlog-adp@program-6 | 346 | 0 | 148,039 (1.480) | fits |
| backlog-adp@program-7 | 346 | 0 | 148,039 (1.480) | fits |
| backlog-adp@verify-0 | 351 | 0 | 147,008 (1.470) | fits |
| backlog-adp@verify-1 | 351 | 0 | 147,008 (1.470) | fits |
| backlog-adp@verify-2 | 351 | 0 | 147,008 (1.470) | fits |
| backlog-adp@verify-3 | 351 | 0 | 147,008 (1.470) | fits |
| backlog-adp@verify-4 | 351 | 0 | 147,008 (1.470) | fits |
| backlog-adp@verify-5 | 351 | 0 | 147,008 (1.470) | fits |
| backlog-adp@verify-6 | 351 | 0 | 147,177 (1.472) | fits |
| backlog-adp@verify-7 | 351 | 0 | 149,063 (1.491) | fits |
| backlog-adp@blank-aged2-0 | 734 | 0 | 144,989 (1.450) | fits |
| backlog-adp@blank-aged2-1 | 746 | 0 | 147,528 (1.475) | fits |
| backlog-adp@blank-aged2-2 | 754 | 0 | 146,969 (1.470) | fits |
| backlog-adp@blank-aged2-3 | 766 | 0 | 147,332 (1.473) | fits |
| backlog-adp@blank-aged2-4 | 777 | 0 | 147,210 (1.472) | fits |
| backlog-adp@blank-aged2-5 | 788 | 0 | 147,192 (1.472) | fits |
| backlog-adp@blank-aged2-6 | 803 | 0 | 147,375 (1.474) | fits |
| backlog-adp@blank-aged2-7 | 813 | 0 | 145,601 (1.456) | fits |
| backlog-adp@blank-aged1-0 | 645 | 0 | 146,131 (1.461) | fits |
| backlog-adp@blank-aged1-1 | 656 | 0 | 148,222 (1.482) | fits |
| backlog-adp@blank-aged1-2 | 667 | 0 | 145,028 (1.450) | fits |
| backlog-adp@blank-aged1-3 | 676 | 0 | 147,208 (1.472) | fits |
| backlog-adp@blank-aged1-4 | 687 | 0 | 147,190 (1.472) | fits |
| backlog-adp@blank-aged1-5 | 698 | 0 | 146,129 (1.461) | fits |
| backlog-adp@blank-aged1-6 | 710 | 0 | 147,330 (1.473) | fits |
| backlog-adp@blank-aged1-7 | 721 | 0 | 146,087 (1.461) | fits |
| backlog-adp@program-aged2-0 | 782 | 0 | 147,360 (1.474) | fits |
| backlog-adp@program-aged2-1 | 793 | 0 | 144,954 (1.450) | fits |
| backlog-adp@program-aged2-2 | 805 | 0 | 149,011 (1.490) | fits |
| backlog-adp@program-aged2-3 | 815 | 0 | 147,430 (1.474) | fits |
| backlog-adp@program-aged2-4 | 826 | 0 | 147,417 (1.474) | fits |
| backlog-adp@program-aged2-5 | 837 | 0 | 147,295 (1.473) | fits |
| backlog-adp@program-aged2-6 | 849 | 0 | 146,214 (1.462) | fits |
| backlog-adp@program-aged2-7 | 860 | 0 | 145,038 (1.450) | fits |
| backlog-adp@program-aged1-0 | 692 | 0 | 147,277 (1.473) | fits |
| backlog-adp@program-aged1-1 | 703 | 0 | 146,214 (1.462) | fits |
| backlog-adp@program-aged1-2 | 714 | 0 | 147,505 (1.475) | fits |
| backlog-adp@program-aged1-3 | 725 | 0 | 147,356 (1.474) | fits |
| backlog-adp@program-aged1-4 | 738 | 0 | 144,992 (1.450) | fits |
| backlog-adp@program-aged1-5 | 747 | 0 | 147,342 (1.473) | fits |
| backlog-adp@program-aged1-6 | 759 | 0 | 147,495 (1.475) | fits |
| backlog-adp@program-aged1-7 | 770 | 0 | 144,954 (1.450) | fits |
| backlog-adp@verify-aged2-0 | 718 | 0 | 148,693 (1.487) | fits |
| backlog-adp@verify-aged2-1 | 730 | 0 | 145,069 (1.451) | fits |
| backlog-adp@verify-aged2-2 | 738 | 0 | 147,362 (1.474) | fits |
| backlog-adp@verify-aged2-3 | 749 | 0 | 147,344 (1.473) | fits |
| backlog-adp@verify-aged2-4 | 760 | 0 | 147,121 (1.471) | fits |
| backlog-adp@verify-aged2-5 | 772 | 0 | 147,484 (1.475) | fits |
| backlog-adp@verify-aged2-6 | 786 | 0 | 147,456 (1.475) | fits |
| backlog-adp@verify-aged2-7 | 797 | 0 | 144,990 (1.450) | fits |
| backlog-adp@verify-aged1-0 | 629 | 0 | 147,362 (1.474) | fits |
| backlog-adp@verify-aged1-1 | 640 | 0 | 147,447 (1.474) | fits |
| backlog-adp@verify-aged1-2 | 650 | 0 | 147,825 (1.478) | fits |
| backlog-adp@verify-aged1-3 | 659 | 0 | 146,150 (1.462) | fits |
| backlog-adp@verify-aged1-4 | 670 | 0 | 148,239 (1.482) | fits |
| backlog-adp@verify-aged1-5 | 682 | 0 | 147,266 (1.473) | fits |
| backlog-adp@verify-aged1-6 | 693 | 0 | 147,248 (1.472) | fits |
| backlog-adp@verify-aged1-7 | 704 | 0 | 147,175 (1.472) | fits |
| adp-advertise | 599 | 0 | 28,411 (0.284) | fits |
| save-held | 1409 | 0 | 154,693 (1.547) | fits |
| save-starved | 37087 | 0 | 154,693 (1.547) | fits |
| srp-bound | 1225 | 0 | 99,011 (0.990) | fits |
| acmp-noresp | 2026 | 0 | 46,388 (0.464) | fits |
| save-bind | 1787 | 0 | 46,388 (0.464) | fits |
| save | 610 | 0 | 42,861 (0.429) | fits |
| srp | 290 | 0 | 49,010 (0.490) | fits |
| save-bind-in-capture | 894 | 0 | 94,332 (0.943) | fits |
| save-bind-in-seal | 896 | 0 | 94,718 (0.947) | fits |
| save-bind-in-erase | 895 | 0 | 95,426 (0.954) | fits |
| save-bind-in-erase-late | 902 | 0 | 94,568 (0.946) | fits |
| save-bind-in-blank | 857 | 0 | 97,833 (0.978) | fits |
| save-bind-in-blank-late | 910 | 0 | 97,833 (0.978) | fits |
| save-bind-in-program | 858 | 0 | 46,133 (0.461) | fits |
| save-bind-in-program-late | 861 | 0 | 95,345 (0.953) | fits |
| save-bind-in-verify | 909 | 0 | 98,455 (0.985) | fits |
| save-bind-in-verify-late | 860 | 0 | 98,781 (0.988) | fits |
| save-bind-burst | 1743 | 0 | 98,772 (0.988) | fits |
| backlog | 286 | 0 | 146,982 (1.470) | fits |
| backlog-adp | 312 | 0 | 146,795 (1.468) | fits |
| backlog-adp-refill | 326 | 0 | 146,795 (1.468) | fits |
| backlog-owed | 310 | 0 | 147,483 (1.475) | fits |
| acmp-disc | 939 | 0 | 46,594 (0.466) | fits |
| maap | 178 | 0 | 28,411 (0.284) | fits |
| adp-link | 90 | 0 | 32,079 (0.321) | fits |
| adp-gm | 89 | 0 | 28,411 (0.284) | fits |
| adp-discover | 89 | 0 | 28,411 (0.284) | fits |
| control | 89 | 0 | 28,411 (0.284) | fits |
| aecp-fanout | 111 | 0 | 61,412 (0.614) | fits |
| acmp-cmd | 85 | 0 | 37,474 (0.375) | fits |
| aecp | 113 | 0 | 42,525 (0.425) | fits |
| aecp-largest-notice | 106 | 0 | 142,621 (1.426) | fits |
| aecp-held | 109 | 0 | 30,541 (0.305) | fits |
| datapath-events | 119 | 0 | 28,411 (0.284) | fits |
| fixture | 154 | 0 | 95,244 (0.952) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 8.194 (20) | 11.806 |
| backlog-adp@blank-aged2-1 | 2 | none | +8.390 ms, 76,371 (0.764 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 8.204 (20) | 11.796 |
| backlog-adp@blank-aged2-2 | 2 | +8.064 ms, 76,709 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 9.068 (20) | 10.932 |
| backlog-adp@blank-aged2-3 | 2 | +7.366 ms, 76,669 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 9.153 (20) | 10.847 |
| backlog-adp@blank-aged2-4 | 2 | +5.768 ms, 76,709 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 9.120 (20) | 10.880 |
| backlog-adp@blank-aged2-5 | 2 | +4.834 ms, 76,558 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 9.074 (20) | 10.926 |
| backlog-adp@blank-aged2-6 | 2 | +3.979 ms, 76,729 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 9.123 (20) | 10.877 |
| backlog-adp@blank-aged2-7 | 2 | +3.044 ms, 76,652 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 9.095 (20) | 10.905 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 8.288 (20) | 11.712 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 8.211 (20) | 11.789 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 8.290 (20) | 11.710 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 8.394 (20) | 11.606 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 8.372 (20) | 11.628 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 8.320 (20) | 11.680 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 8.379 (20) | 11.621 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 8.294 (20) | 11.706 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 8.300 (20) | 11.700 |
| backlog-adp@program-aged2-1 | 2 | none | +8.396 ms, 80,676 (0.807 ms), issue | `backlog-adp@program-aged2-1.service.srp.last.if0` | 8.209 (20) | 11.791 |
| backlog-adp@program-aged2-2 | 2 | +8.095 ms, 80,902 (0.809 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 9.186 (20) | 10.814 |
| backlog-adp@program-aged2-3 | 2 | +7.206 ms, 80,902 (0.809 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 9.238 (20) | 10.762 |
| backlog-adp@program-aged2-4 | 2 | +5.609 ms, 80,902 (0.809 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 9.206 (20) | 10.794 |
| backlog-adp@program-aged2-5 | 2 | +4.789 ms, 80,737 (0.807 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 9.169 (20) | 10.831 |
| backlog-adp@program-aged2-6 | 2 | +3.815 ms, 80,963 (0.810 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 9.205 (20) | 10.795 |
| backlog-adp@program-aged2-7 | 2 | none | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 9.113 (20) | 10.887 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 8.311 (20) | 11.689 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 8.272 (20) | 11.728 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 8.346 (20) | 11.654 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 8.307 (20) | 11.693 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 8.223 (20) | 11.777 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 8.335 (20) | 11.665 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 8.386 (20) | 11.614 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 8.346 (20) | 11.654 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 8.282 (20) | 11.718 |
| backlog-adp@verify-aged2-1 | 2 | none | +8.407 ms, 77,311 (0.773 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 8.219 (20) | 11.781 |
| backlog-adp@verify-aged2-2 | 2 | +8.138 ms, 77,649 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 9.149 (20) | 10.851 |
| backlog-adp@verify-aged2-3 | 2 | +7.318 ms, 77,609 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 9.114 (20) | 10.886 |
| backlog-adp@verify-aged2-4 | 2 | +5.721 ms, 77,649 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 9.081 (20) | 10.919 |
| backlog-adp@verify-aged2-5 | 2 | +4.903 ms, 77,498 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 9.152 (20) | 10.848 |
| backlog-adp@verify-aged2-6 | 2 | +3.931 ms, 77,873 (0.779 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 9.089 (20) | 10.911 |
| backlog-adp@verify-aged2-7 | 2 | +3.849 ms, 77,873 (0.779 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 9.006 (20) | 10.994 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 8.344 (20) | 11.656 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 8.262 (20) | 11.738 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 8.246 (20) | 11.754 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 8.328 (20) | 11.672 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 8.313 (20) | 11.687 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 8.380 (20) | 11.620 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 8.317 (20) | 11.683 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 8.263 (20) | 11.737 |

Least margin over the aged windows: 10.762 ms, `backlog-adp@program-aged2-3.service.srp.last.if0` at 9.238 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.414 | 6,070 | 102 | 2 | 30.796 | yes | within |
| save-held | 1084.160 | 4,070 | 102 | - | 22.175 | no | within |
| save-starved | 4048.223 | 4,070 | 102 | - | 31.357 | yes | within |
| save | 1075.874 | 4,070 | 102 | - | 24.210 | no | within |

Names from their response to durable (save_burst.py; #920, #665's ruling of 2026-11-15, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-flight | 1 | 147.073 (0) | 5,000 | 2 | - | - | 19 steps (want 19), 5.946 ms | within |
| save-burst | 39 | 1097.438 (0) | 5,000 | 1 | - | - | sequence 1, 0 missing | within |

Binding changes from their response to durable (bind_save.py; the binding class's 100 ms window, Milan v1.2 5.5.3.5.3 and 5.3.8.3), with the part's erase of 120 ms and page program of 0.5 ms modelled:

| Group | Command | Sink | Durable, ms | Target ms | Saves | Erases | Verdict |
|---|---|---:|---:|---:|---:|---:|---|
| save-bind | BIND_RX | 0 | 304.506 | 800 | 4 | 4 | within |
| save-bind | STOP_STREAMING | 0 | 304.212 | 800 | 4 | 4 | within |
| save-bind | START_STREAMING | 0 | 304.189 | 800 | 4 | 4 | within |
| save-bind | UNBIND_RX | 0 | 304.535 | 800 | 4 | 4 | within |
| save-bind-in-capture | BIND_RX | 0 | 394.959 | 450 | 2 | 2 | within |
| save-bind-in-seal | BIND_RX | 0 | 392.866 | 450 | 2 | 2 | within |
| save-bind-in-erase | BIND_RX | 0 | 391.169 | 450 | 2 | 2 | within |
| save-bind-in-erase-late | BIND_RX | 0 | 330.538 | 450 | 2 | 2 | within |
| save-bind-in-blank | BIND_RX | 0 | 298.809 | 450 | 2 | 2 | within |
| save-bind-in-blank-late | BIND_RX | 0 | 298.591 | 450 | 2 | 2 | within |
| save-bind-in-program | BIND_RX | 0 | 305.495 | 450 | 2 | 2 | within |
| save-bind-in-program-late | BIND_RX | 0 | 298.517 | 450 | 2 | 2 | within |
| save-bind-in-verify | BIND_RX | 0 | 305.254 | 450 | 2 | 2 | within |
| save-bind-in-verify-late | BIND_RX | 0 | 303.246 | 450 | 2 | 2 | within |
| save-bind-burst | UNBIND_RX | 0 | 306.463 | 450 | 4 | 4 | within |
| save-bind-burst | UNBIND_RX | 1 | 296.522 | 450 | 4 | 4 | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-kept | 1844 | 18,738 (0.187) | 2,553 (0.026) |
| save-flight | 1554 | 92,005 (0.920) | 78,771 (0.788) |
| save-burst | 1480 | 90,761 (0.908) | 77,990 (0.780) |
| acmp-notk | 1159 | 94,049 (0.940) | 78,461 (0.785) |
| save-second | 520 | 79,963 (0.800) | 78,148 (0.781) |
| backlog-adp@blank-0 | 302 | 89,114 (0.891) | 76,076 (0.761) |
| backlog-adp@blank-1 | 302 | 89,114 (0.891) | 76,076 (0.761) |
| backlog-adp@blank-2 | 302 | 89,114 (0.891) | 76,076 (0.761) |
| backlog-adp@blank-3 | 302 | 89,114 (0.891) | 76,076 (0.761) |
| backlog-adp@blank-4 | 302 | 89,114 (0.891) | 76,076 (0.761) |
| backlog-adp@blank-5 | 302 | 89,114 (0.891) | 76,076 (0.761) |
| backlog-adp@blank-6 | 302 | 89,114 (0.891) | 76,076 (0.761) |
| backlog-adp@blank-7 | 306 | 89,698 (0.897) | 76,076 (0.761) |
| backlog-adp@program-0 | 331 | 91,366 (0.914) | 78,131 (0.781) |
| backlog-adp@program-1 | 332 | 93,281 (0.933) | 78,891 (0.789) |
| backlog-adp@program-2 | 335 | 91,471 (0.915) | 78,131 (0.781) |
| backlog-adp@program-3 | 335 | 91,471 (0.915) | 78,131 (0.781) |
| backlog-adp@program-4 | 335 | 91,471 (0.915) | 78,131 (0.781) |
| backlog-adp@program-5 | 335 | 91,471 (0.915) | 78,131 (0.781) |
| backlog-adp@program-6 | 337 | 91,489 (0.915) | 78,131 (0.781) |
| backlog-adp@program-7 | 337 | 91,489 (0.915) | 78,131 (0.781) |
| backlog-adp@verify-0 | 360 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-1 | 360 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-2 | 360 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-3 | 360 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-4 | 360 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-5 | 360 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-6 | 360 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-7 | 360 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@blank-aged2-0 | 301 | 89,641 (0.896) | 76,235 (0.762) |
| backlog-adp@blank-aged2-1 | 300 | 89,759 (0.898) | 75,772 (0.758) |
| backlog-adp@blank-aged2-2 | 300 | 88,214 (0.882) | 75,858 (0.759) |
| backlog-adp@blank-aged2-3 | 300 | 88,471 (0.885) | 75,856 (0.759) |
| backlog-adp@blank-aged2-4 | 300 | 88,438 (0.884) | 75,858 (0.759) |
| backlog-adp@blank-aged2-5 | 300 | 88,425 (0.884) | 75,913 (0.759) |
| backlog-adp@blank-aged2-6 | 303 | 89,622 (0.896) | 75,908 (0.759) |
| backlog-adp@blank-aged2-7 | 302 | 91,276 (0.913) | 75,896 (0.759) |
| backlog-adp@blank-aged1-0 | 303 | 89,664 (0.897) | 76,235 (0.762) |
| backlog-adp@blank-aged1-1 | 301 | 89,589 (0.896) | 76,149 (0.761) |
| backlog-adp@blank-aged1-2 | 300 | 89,723 (0.897) | 76,235 (0.762) |
| backlog-adp@blank-aged1-3 | 299 | 88,827 (0.888) | 76,233 (0.762) |
| backlog-adp@blank-aged1-4 | 299 | 88,873 (0.889) | 76,235 (0.762) |
| backlog-adp@blank-aged1-5 | 299 | 88,844 (0.888) | 76,235 (0.762) |
| backlog-adp@blank-aged1-6 | 299 | 88,746 (0.887) | 76,235 (0.762) |
| backlog-adp@blank-aged1-7 | 299 | 89,135 (0.891) | 76,235 (0.762) |
| backlog-adp@program-aged2-0 | 330 | 92,720 (0.927) | 78,891 (0.789) |
| backlog-adp@program-aged2-1 | 328 | 91,244 (0.912) | 78,681 (0.787) |
| backlog-adp@program-aged2-2 | 329 | 91,655 (0.917) | 78,658 (0.787) |
| backlog-adp@program-aged2-3 | 329 | 91,670 (0.917) | 78,658 (0.787) |
| backlog-adp@program-aged2-4 | 329 | 91,432 (0.914) | 78,658 (0.787) |
| backlog-adp@program-aged2-5 | 329 | 91,432 (0.914) | 78,590 (0.786) |
| backlog-adp@program-aged2-6 | 329 | 91,452 (0.915) | 78,682 (0.787) |
| backlog-adp@program-aged2-7 | 329 | 91,541 (0.915) | 78,747 (0.787) |
| backlog-adp@program-aged1-0 | 330 | 92,643 (0.926) | 78,891 (0.789) |
| backlog-adp@program-aged1-1 | 328 | 91,605 (0.916) | 78,914 (0.789) |
| backlog-adp@program-aged1-2 | 328 | 93,242 (0.932) | 78,891 (0.789) |
| backlog-adp@program-aged1-3 | 328 | 93,230 (0.932) | 78,891 (0.789) |
| backlog-adp@program-aged1-4 | 331 | 99,412 (0.994) | 78,891 (0.789) |
| backlog-adp@program-aged1-5 | 328 | 92,880 (0.929) | 78,889 (0.789) |
| backlog-adp@program-aged1-6 | 328 | 92,841 (0.928) | 78,891 (0.789) |
| backlog-adp@program-aged1-7 | 328 | 92,867 (0.929) | 78,891 (0.789) |
| backlog-adp@verify-aged2-0 | 360 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-aged2-1 | 359 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-aged2-2 | 359 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-aged2-3 | 359 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-aged2-4 | 359 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-aged2-5 | 359 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-aged2-6 | 362 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-aged2-7 | 361 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-aged1-0 | 362 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-aged1-1 | 360 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-aged1-2 | 359 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-aged1-3 | 358 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-aged1-4 | 358 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-aged1-5 | 358 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-aged1-6 | 358 | 91,444 (0.914) | 78,131 (0.781) |
| backlog-adp@verify-aged1-7 | 358 | 91,444 (0.914) | 78,131 (0.781) |
| adp-advertise | 578 | 18,269 (0.183) | 2,553 (0.026) |
| save-held | 816 | 90,852 (0.909) | 78,074 (0.781) |
| save-starved | 418 | 80,792 (0.808) | 78,479 (0.785) |
| srp-bound | 675 | 99,011 (0.990) | 78,461 (0.785) |
| acmp-noresp | 709 | 93,972 (0.940) | 78,461 (0.785) |
| save-bind | 3935 | 93,943 (0.939) | 78,458 (0.785) |
| save | 680 | 90,705 (0.907) | 77,844 (0.778) |
| srp | 271 | 18,269 (0.183) | 2,553 (0.026) |
| save-bind-in-capture | 2059 | 94,332 (0.943) | 78,131 (0.781) |
| save-bind-in-seal | 2052 | 94,718 (0.947) | 78,131 (0.781) |
| save-bind-in-erase | 2055 | 95,426 (0.954) | 78,261 (0.783) |
| save-bind-in-erase-late | 2076 | 94,568 (0.946) | 78,261 (0.783) |
| save-bind-in-blank | 2107 | 97,833 (0.978) | 78,210 (0.782) |
| save-bind-in-blank-late | 2112 | 97,833 (0.978) | 78,261 (0.783) |
| save-bind-in-program | 2106 | 93,168 (0.932) | 78,210 (0.782) |
| save-bind-in-program-late | 2113 | 95,345 (0.953) | 78,543 (0.785) |
| save-bind-in-verify | 2121 | 98,455 (0.985) | 78,410 (0.784) |
| save-bind-in-verify-late | 2123 | 98,781 (0.988) | 78,210 (0.782) |
| save-bind-burst | 3463 | 98,772 (0.988) | 78,756 (0.788) |
| backlog | 265 | 18,269 (0.183) | 2,553 (0.026) |
| backlog-adp | 271 | 18,269 (0.183) | 2,553 (0.026) |
| backlog-adp-refill | 274 | 18,269 (0.183) | 2,553 (0.026) |
| backlog-owed | 276 | 18,269 (0.183) | 2,569 (0.026) |
| acmp-disc | 399 | 91,317 (0.913) | 78,261 (0.783) |
| maap | 165 | 18,233 (0.182) | 2,553 (0.026) |
| adp-link | 80 | 18,126 (0.181) | 2,553 (0.026) |
| adp-gm | 80 | 18,126 (0.181) | 2,553 (0.026) |
| adp-discover | 80 | 18,126 (0.181) | 2,553 (0.026) |
| control | 80 | 18,126 (0.181) | 2,553 (0.026) |
| aecp-fanout | 80 | 18,126 (0.181) | 2,553 (0.026) |
| acmp-cmd | 65 | 18,126 (0.181) | 2,553 (0.026) |
| aecp | 80 | 18,126 (0.181) | 2,553 (0.026) |
| aecp-largest-notice | 78 | 18,126 (0.181) | 2,553 (0.026) |
| aecp-held | 98 | 18,126 (0.181) | 2,553 (0.026) |
| datapath-events | 70 | 18,126 (0.181) | 2,553 (0.026) |
| fixture | 149 | 95,244 (0.952) | 78,131 (0.781) |

Longest pass that carries a step: 99,412 CPU cycles (0.994 ms), backlog-adp@program-aged1-4; longest step: 78,914 (0.789 ms), backlog-adp@program-aged1-1.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| Talker Advertise RX for every input, no binding (kept) | `srp.kept_advertise.if0` | 48,701 | 0.487 | 20 | 20 | fits | 48,767 | 12 | 0.895 |
| Talker RX at the bound after a freed block (count) | `srp.kept_recount.if0` | 46,619 | 0.466 | 20 | 20 | fits | 46,685 | 12 | 0.893 |
| Talker Failed RX for every input, no binding (kept) | `srp.kept_failed.if0` | 51,723 | 0.517 | 20 | 20 | fits | 51,789 | 12 | 0.901 |
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 152,214 | 1.522 | 20 | 200 | fits | 68,786 | 203 | 0.176 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 190,866 | 1.909 | 20 | 20 | fits | 139,087 | 264 | 0.209 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 261,797 | 2.618 | 20 | 24 | fits | 44,901 | 35 | 0.495 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 211,575 | 2.116 | 20 | 50 | fits | 91,349 | 202 | 0.323 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 734,414 | 7.344 | 20 | 20 | fits | 41,111 | 22 | 0.781 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 75,764 | 0.758 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-burst.held.adp.if0` | 153,884 | 1.539 | 20 | 200 | fits | 154,693 | 260 | 0.370 |
| ACMP record, every channel at its refill rate, the longest | `save-burst.held.acmp.if0` | 198,048 | 1.980 | 20 | 20 | fits | 138,395 | 264 | 0.203 |
| AECP record, every channel at its refill rate, the longest | `save-burst.held.aecp.if0` | 115,684 | 1.157 | 20 | 24 | fits | 45,730 | 27 | 0.808 |
| MAAP record, every channel at its refill rate, the longest | `save-burst.held.maap.if0` | 189,416 | 1.894 | 20 | 50 | fits | 95,275 | 86 | 0.699 |
| SRP record, every channel at its refill rate, the longest | `save-burst.held.srp.if0` | 666,835 | 6.668 | 20 | 20 | fits | 84,181 | 39 | 0.722 |
| an MRPDU its periodic timer owes, the longest | `save-burst.mrpdu.periodic.if0` | 240,725 | 2.407 | 49 | 49 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 9,968 | 0.100 | 20 | 20 | fits | 27,925 | 19 (14) | 0.867 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 410,728 | 4.107 | 20 | 20 | fits | 89,387 | 115 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 365,760 | 3.658 | 20 | 200 | fits | 145,973 | 278 | 0.330 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 466,166 | 4.662 | 20 | 200 | fits | 89,387 | 115 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 366,684 | 3.667 | 20 | 20 | fits | 145,973 | 278 | 0.330 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 466,870 | 4.669 | 20 | 20 | fits | 89,387 | 115 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 224,351 | 2.244 | 20 | 24 | fits | 146,500 | 164 | 0.404 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 369,334 | 3.693 | 20 | 24 | fits | 145,973 | 278 | 0.330 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 369,268 | 3.693 | 20 | 50 | fits | 145,973 | 278 | 0.330 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 469,894 | 4.699 | 20 | 50 | fits | 89,387 | 115 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 550,388 | 5.504 | 20 | 20 | fits | 80,560 | 28 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 908,925 | 9.089 | 20 | 20 | fits | 47,159 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 398,228 | 3.982 | 20 | 20 | fits | 89,387 | 115 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 353,260 | 3.533 | 20 | 200 | fits | 145,973 | 278 | 0.330 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 453,666 | 4.537 | 20 | 200 | fits | 89,387 | 115 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 354,184 | 3.542 | 20 | 20 | fits | 145,973 | 278 | 0.330 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 454,370 | 4.544 | 20 | 20 | fits | 89,387 | 115 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 211,851 | 2.119 | 20 | 24 | fits | 146,500 | 164 | 0.404 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 356,834 | 3.568 | 20 | 24 | fits | 145,973 | 278 | 0.330 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 356,768 | 3.568 | 20 | 50 | fits | 145,973 | 278 | 0.330 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 457,394 | 4.574 | 20 | 50 | fits | 89,387 | 115 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 537,888 | 5.379 | 20 | 20 | fits | 80,560 | 28 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 896,425 | 8.964 | 20 | 20 | fits | 47,159 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 385,728 | 3.857 | 20 | 20 | fits | 89,387 | 115 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 340,760 | 3.408 | 20 | 200 | fits | 145,973 | 278 | 0.330 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 441,166 | 4.412 | 20 | 200 | fits | 89,387 | 115 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 341,684 | 3.417 | 20 | 20 | fits | 145,973 | 278 | 0.330 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 441,870 | 4.419 | 20 | 20 | fits | 89,387 | 115 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 199,351 | 1.994 | 20 | 24 | fits | 146,500 | 164 | 0.404 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 344,334 | 3.443 | 20 | 24 | fits | 145,973 | 278 | 0.330 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 344,268 | 3.443 | 20 | 50 | fits | 145,973 | 278 | 0.330 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 444,894 | 4.449 | 20 | 50 | fits | 89,387 | 115 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 525,388 | 5.254 | 20 | 20 | fits | 80,560 | 28 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 883,925 | 8.839 | 20 | 20 | fits | 47,159 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 373,228 | 3.732 | 20 | 20 | fits | 89,387 | 115 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 328,260 | 3.283 | 20 | 200 | fits | 145,973 | 278 | 0.330 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 428,666 | 4.287 | 20 | 200 | fits | 89,387 | 115 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 329,184 | 3.292 | 20 | 20 | fits | 145,973 | 278 | 0.330 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 429,370 | 4.294 | 20 | 20 | fits | 89,387 | 115 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 186,851 | 1.869 | 20 | 24 | fits | 146,500 | 164 | 0.404 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 331,834 | 3.318 | 20 | 24 | fits | 145,973 | 278 | 0.330 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 331,768 | 3.318 | 20 | 50 | fits | 145,973 | 278 | 0.330 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 432,394 | 4.324 | 20 | 50 | fits | 89,387 | 115 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 512,888 | 5.129 | 20 | 20 | fits | 80,560 | 28 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 871,425 | 8.714 | 20 | 20 | fits | 47,159 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 360,728 | 3.607 | 20 | 20 | fits | 89,387 | 115 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 315,760 | 3.158 | 20 | 200 | fits | 145,973 | 278 | 0.330 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 416,166 | 4.162 | 20 | 200 | fits | 89,387 | 115 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 316,684 | 3.167 | 20 | 20 | fits | 145,973 | 278 | 0.330 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 416,870 | 4.169 | 20 | 20 | fits | 89,387 | 115 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 174,351 | 1.744 | 20 | 24 | fits | 146,500 | 164 | 0.404 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 319,334 | 3.193 | 20 | 24 | fits | 145,973 | 278 | 0.330 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 319,268 | 3.193 | 20 | 50 | fits | 145,973 | 278 | 0.330 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 419,894 | 4.199 | 20 | 50 | fits | 89,387 | 115 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 500,388 | 5.004 | 20 | 20 | fits | 80,560 | 28 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 858,925 | 8.589 | 20 | 20 | fits | 47,159 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 348,228 | 3.482 | 20 | 20 | fits | 89,387 | 115 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 303,260 | 3.033 | 20 | 200 | fits | 145,973 | 278 | 0.330 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 403,666 | 4.037 | 20 | 200 | fits | 89,387 | 115 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 304,184 | 3.042 | 20 | 20 | fits | 145,973 | 278 | 0.330 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 404,370 | 4.044 | 20 | 20 | fits | 89,387 | 115 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 161,851 | 1.619 | 20 | 24 | fits | 146,500 | 164 | 0.404 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 306,834 | 3.068 | 20 | 24 | fits | 145,973 | 278 | 0.330 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 306,768 | 3.068 | 20 | 50 | fits | 145,973 | 278 | 0.330 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 407,394 | 4.074 | 20 | 50 | fits | 89,387 | 115 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 487,888 | 4.879 | 20 | 20 | fits | 80,560 | 28 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 846,425 | 8.464 | 20 | 20 | fits | 47,159 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 335,728 | 3.357 | 20 | 20 | fits | 89,387 | 115 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 290,760 | 2.908 | 20 | 200 | fits | 145,973 | 278 | 0.330 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 391,166 | 3.912 | 20 | 200 | fits | 89,387 | 115 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 291,684 | 2.917 | 20 | 20 | fits | 145,973 | 278 | 0.330 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 391,870 | 3.919 | 20 | 20 | fits | 89,387 | 115 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 149,351 | 1.494 | 20 | 24 | fits | 146,500 | 164 | 0.404 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 294,334 | 2.943 | 20 | 24 | fits | 145,973 | 278 | 0.330 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 294,268 | 2.943 | 20 | 50 | fits | 145,973 | 278 | 0.330 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 394,894 | 3.949 | 20 | 50 | fits | 89,387 | 115 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 475,388 | 4.754 | 20 | 20 | fits | 80,560 | 28 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 833,925 | 8.339 | 20 | 20 | fits | 47,159 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 389,627 | 3.896 | 20 | 20 | fits | 85,628 | 124 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 366,887 | 3.669 | 20 | 200 | fits | 147,943 | 267 | 0.327 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 463,372 | 4.634 | 20 | 200 | fits | 85,628 | 124 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 367,811 | 3.678 | 20 | 20 | fits | 147,943 | 267 | 0.327 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 464,076 | 4.641 | 20 | 20 | fits | 85,628 | 124 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 223,508 | 2.235 | 20 | 24 | fits | 146,500 | 164 | 0.404 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 370,461 | 3.705 | 20 | 24 | fits | 147,943 | 267 | 0.327 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 370,395 | 3.704 | 20 | 50 | fits | 147,943 | 267 | 0.327 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 467,100 | 4.671 | 20 | 50 | fits | 85,628 | 124 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 547,774 | 5.478 | 20 | 20 | fits | 80,740 | 28 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 906,248 | 9.062 | 20 | 20 | fits | 47,159 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 335,822 | 3.358 | 20 | 20 | fits | 80,916 | 104 | 0.471 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 306,121 | 3.061 | 20 | 200 | fits | 147,627 | 284 | 0.309 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 397,802 | 3.978 | 20 | 200 | fits | 80,916 | 104 | 0.471 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 307,045 | 3.070 | 20 | 20 | fits | 147,627 | 284 | 0.309 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 398,506 | 3.985 | 20 | 20 | fits | 80,916 | 104 | 0.471 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 163,058 | 1.631 | 20 | 24 | fits | 146,630 | 164 | 0.402 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 309,695 | 3.097 | 20 | 24 | fits | 147,627 | 284 | 0.309 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 309,629 | 3.096 | 20 | 50 | fits | 147,627 | 284 | 0.309 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 401,530 | 4.015 | 20 | 50 | fits | 80,916 | 104 | 0.471 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 481,898 | 4.819 | 20 | 20 | fits | 80,434 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 844,884 | 8.449 | 20 | 20 | fits | 47,176 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 321,049 | 3.210 | 20 | 20 | fits | 81,005 | 104 | 0.480 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 298,067 | 2.981 | 20 | 200 | fits | 147,684 | 284 | 0.310 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 389,837 | 3.898 | 20 | 200 | fits | 81,005 | 104 | 0.480 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 298,991 | 2.990 | 20 | 20 | fits | 147,684 | 284 | 0.310 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 390,541 | 3.905 | 20 | 20 | fits | 81,005 | 104 | 0.480 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 154,947 | 1.549 | 20 | 24 | fits | 146,521 | 164 | 0.402 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 301,641 | 3.016 | 20 | 24 | fits | 147,684 | 284 | 0.310 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 301,575 | 3.016 | 20 | 50 | fits | 147,684 | 284 | 0.310 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 393,565 | 3.936 | 20 | 50 | fits | 81,005 | 104 | 0.480 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 474,120 | 4.741 | 20 | 20 | fits | 80,621 | 28 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 837,173 | 8.372 | 20 | 20 | fits | 47,157 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 380,055 | 3.801 | 20 | 20 | fits | 81,033 | 118 | 0.378 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 370,999 | 3.710 | 20 | 200 | fits | 143,961 | 266 | 0.326 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 451,416 | 4.514 | 20 | 200 | fits | 81,033 | 118 | 0.378 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 371,923 | 3.719 | 20 | 20 | fits | 143,961 | 266 | 0.326 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 452,120 | 4.521 | 20 | 20 | fits | 81,033 | 118 | 0.378 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 221,371 | 2.214 | 20 | 24 | fits | 146,842 | 165 | 0.402 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 374,573 | 3.746 | 20 | 24 | fits | 143,961 | 266 | 0.326 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 374,507 | 3.745 | 20 | 50 | fits | 143,961 | 266 | 0.326 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 455,144 | 4.551 | 20 | 50 | fits | 81,033 | 118 | 0.378 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 535,590 | 5.356 | 20 | 20 | fits | 80,512 | 28 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 898,831 | 8.988 | 20 | 20 | fits | 47,157 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 355,055 | 3.551 | 20 | 20 | fits | 81,033 | 118 | 0.378 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 345,999 | 3.460 | 20 | 200 | fits | 143,961 | 266 | 0.326 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 426,416 | 4.264 | 20 | 200 | fits | 81,033 | 118 | 0.378 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 346,923 | 3.469 | 20 | 20 | fits | 143,961 | 266 | 0.326 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 427,120 | 4.271 | 20 | 20 | fits | 81,033 | 118 | 0.378 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 196,371 | 1.964 | 20 | 24 | fits | 146,842 | 165 | 0.402 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 349,573 | 3.496 | 20 | 24 | fits | 143,961 | 266 | 0.326 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 349,507 | 3.495 | 20 | 50 | fits | 143,961 | 266 | 0.326 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 430,144 | 4.301 | 20 | 50 | fits | 81,033 | 118 | 0.378 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 510,590 | 5.106 | 20 | 20 | fits | 80,512 | 28 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 873,831 | 8.738 | 20 | 20 | fits | 47,157 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 330,055 | 3.301 | 20 | 20 | fits | 81,033 | 118 | 0.378 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 320,999 | 3.210 | 20 | 200 | fits | 143,961 | 266 | 0.326 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 401,416 | 4.014 | 20 | 200 | fits | 81,033 | 118 | 0.378 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 321,923 | 3.219 | 20 | 20 | fits | 143,961 | 266 | 0.326 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 402,120 | 4.021 | 20 | 20 | fits | 81,033 | 118 | 0.378 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 171,371 | 1.714 | 20 | 24 | fits | 146,842 | 165 | 0.402 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 324,573 | 3.246 | 20 | 24 | fits | 143,961 | 266 | 0.326 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 324,507 | 3.245 | 20 | 50 | fits | 143,961 | 266 | 0.326 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 405,144 | 4.051 | 20 | 50 | fits | 81,033 | 118 | 0.378 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 485,590 | 4.856 | 20 | 20 | fits | 80,512 | 28 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 848,831 | 8.488 | 20 | 20 | fits | 47,157 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 305,055 | 3.051 | 20 | 20 | fits | 81,033 | 118 | 0.378 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 295,999 | 2.960 | 20 | 200 | fits | 143,961 | 266 | 0.326 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 376,416 | 3.764 | 20 | 200 | fits | 81,033 | 118 | 0.378 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 296,923 | 2.969 | 20 | 20 | fits | 143,961 | 266 | 0.326 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 377,120 | 3.771 | 20 | 20 | fits | 81,033 | 118 | 0.378 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 146,371 | 1.464 | 20 | 24 | fits | 146,842 | 165 | 0.402 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 299,573 | 2.996 | 20 | 24 | fits | 143,961 | 266 | 0.326 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 299,507 | 2.995 | 20 | 50 | fits | 143,961 | 266 | 0.326 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 380,144 | 3.801 | 20 | 50 | fits | 81,033 | 118 | 0.378 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 460,590 | 4.606 | 20 | 20 | fits | 80,512 | 28 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 823,831 | 8.238 | 20 | 20 | fits | 47,157 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 412,735 | 4.127 | 20 | 20 | fits | 101,734 | 104 | 0.524 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 382,917 | 3.829 | 20 | 200 | fits | 148,039 | 284 | 0.324 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 484,035 | 4.840 | 20 | 200 | fits | 101,734 | 104 | 0.524 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 383,841 | 3.838 | 20 | 20 | fits | 148,039 | 284 | 0.324 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 484,739 | 4.847 | 20 | 20 | fits | 101,734 | 104 | 0.524 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 229,211 | 2.292 | 20 | 24 | fits | 146,659 | 165 | 0.402 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 386,491 | 3.865 | 20 | 24 | fits | 148,039 | 284 | 0.324 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 386,425 | 3.864 | 20 | 50 | fits | 148,039 | 284 | 0.324 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 487,763 | 4.878 | 20 | 50 | fits | 101,734 | 104 | 0.524 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 487,697 | 4.877 | 20 | 20 | fits | 101,734 | 104 | 0.524 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 908,913 | 9.089 | 20 | 20 | fits | 26,062 | 12 | 0.803 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 387,735 | 3.877 | 20 | 20 | fits | 101,734 | 104 | 0.524 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 357,917 | 3.579 | 20 | 200 | fits | 148,039 | 284 | 0.324 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 459,035 | 4.590 | 20 | 200 | fits | 101,734 | 104 | 0.524 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 358,841 | 3.588 | 20 | 20 | fits | 148,039 | 284 | 0.324 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 459,739 | 4.597 | 20 | 20 | fits | 101,734 | 104 | 0.524 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 204,211 | 2.042 | 20 | 24 | fits | 146,659 | 165 | 0.402 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 361,491 | 3.615 | 20 | 24 | fits | 148,039 | 284 | 0.324 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 361,425 | 3.614 | 20 | 50 | fits | 148,039 | 284 | 0.324 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 462,763 | 4.628 | 20 | 50 | fits | 101,734 | 104 | 0.524 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 462,697 | 4.627 | 20 | 20 | fits | 101,734 | 104 | 0.524 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 883,913 | 8.839 | 20 | 20 | fits | 26,062 | 12 | 0.803 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 400,496 | 4.005 | 20 | 20 | fits | 89,061 | 115 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 354,996 | 3.550 | 20 | 200 | fits | 144,828 | 278 | 0.322 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 455,075 | 4.551 | 20 | 200 | fits | 89,061 | 115 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 355,920 | 3.559 | 20 | 20 | fits | 144,828 | 278 | 0.322 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 455,779 | 4.558 | 20 | 20 | fits | 89,061 | 115 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 214,732 | 2.147 | 20 | 24 | fits | 147,008 | 164 | 0.408 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 358,570 | 3.586 | 20 | 24 | fits | 144,828 | 278 | 0.322 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 358,504 | 3.585 | 20 | 50 | fits | 144,828 | 278 | 0.322 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 458,803 | 4.588 | 20 | 50 | fits | 89,061 | 115 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 539,054 | 5.391 | 20 | 20 | fits | 80,317 | 28 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 897,291 | 8.973 | 20 | 20 | fits | 47,176 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 387,996 | 3.880 | 20 | 20 | fits | 89,061 | 115 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 342,496 | 3.425 | 20 | 200 | fits | 144,828 | 278 | 0.322 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 442,575 | 4.426 | 20 | 200 | fits | 89,061 | 115 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 343,420 | 3.434 | 20 | 20 | fits | 144,828 | 278 | 0.322 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 443,279 | 4.433 | 20 | 20 | fits | 89,061 | 115 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 202,232 | 2.022 | 20 | 24 | fits | 147,008 | 164 | 0.408 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 346,070 | 3.461 | 20 | 24 | fits | 144,828 | 278 | 0.322 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 346,004 | 3.460 | 20 | 50 | fits | 144,828 | 278 | 0.322 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 446,303 | 4.463 | 20 | 50 | fits | 89,061 | 115 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 526,554 | 5.266 | 20 | 20 | fits | 80,317 | 28 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 884,791 | 8.848 | 20 | 20 | fits | 47,176 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 375,496 | 3.755 | 20 | 20 | fits | 89,061 | 115 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 329,996 | 3.300 | 20 | 200 | fits | 144,828 | 278 | 0.322 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 430,075 | 4.301 | 20 | 200 | fits | 89,061 | 115 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 330,920 | 3.309 | 20 | 20 | fits | 144,828 | 278 | 0.322 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 430,779 | 4.308 | 20 | 20 | fits | 89,061 | 115 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 189,732 | 1.897 | 20 | 24 | fits | 147,008 | 164 | 0.408 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 333,570 | 3.336 | 20 | 24 | fits | 144,828 | 278 | 0.322 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 333,504 | 3.335 | 20 | 50 | fits | 144,828 | 278 | 0.322 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 433,803 | 4.338 | 20 | 50 | fits | 89,061 | 115 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 514,054 | 5.141 | 20 | 20 | fits | 80,317 | 28 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 872,291 | 8.723 | 20 | 20 | fits | 47,176 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 362,996 | 3.630 | 20 | 20 | fits | 89,061 | 115 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 317,496 | 3.175 | 20 | 200 | fits | 144,828 | 278 | 0.322 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 417,575 | 4.176 | 20 | 200 | fits | 89,061 | 115 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 318,420 | 3.184 | 20 | 20 | fits | 144,828 | 278 | 0.322 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 418,279 | 4.183 | 20 | 20 | fits | 89,061 | 115 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 177,232 | 1.772 | 20 | 24 | fits | 147,008 | 164 | 0.408 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 321,070 | 3.211 | 20 | 24 | fits | 144,828 | 278 | 0.322 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 321,004 | 3.210 | 20 | 50 | fits | 144,828 | 278 | 0.322 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 421,303 | 4.213 | 20 | 50 | fits | 89,061 | 115 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 501,554 | 5.016 | 20 | 20 | fits | 80,317 | 28 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 859,791 | 8.598 | 20 | 20 | fits | 47,176 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 350,496 | 3.505 | 20 | 20 | fits | 89,061 | 115 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 304,996 | 3.050 | 20 | 200 | fits | 144,828 | 278 | 0.322 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 405,075 | 4.051 | 20 | 200 | fits | 89,061 | 115 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 305,920 | 3.059 | 20 | 20 | fits | 144,828 | 278 | 0.322 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 405,779 | 4.058 | 20 | 20 | fits | 89,061 | 115 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 164,732 | 1.647 | 20 | 24 | fits | 147,008 | 164 | 0.408 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 308,570 | 3.086 | 20 | 24 | fits | 144,828 | 278 | 0.322 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 308,504 | 3.085 | 20 | 50 | fits | 144,828 | 278 | 0.322 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 408,803 | 4.088 | 20 | 50 | fits | 89,061 | 115 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 489,054 | 4.891 | 20 | 20 | fits | 80,317 | 28 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 847,291 | 8.473 | 20 | 20 | fits | 47,176 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 337,996 | 3.380 | 20 | 20 | fits | 89,061 | 115 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 292,496 | 2.925 | 20 | 200 | fits | 144,828 | 278 | 0.322 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 392,575 | 3.926 | 20 | 200 | fits | 89,061 | 115 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 293,420 | 2.934 | 20 | 20 | fits | 144,828 | 278 | 0.322 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 393,279 | 3.933 | 20 | 20 | fits | 89,061 | 115 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 152,232 | 1.522 | 20 | 24 | fits | 147,008 | 164 | 0.408 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 296,070 | 2.961 | 20 | 24 | fits | 144,828 | 278 | 0.322 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 296,004 | 2.960 | 20 | 50 | fits | 144,828 | 278 | 0.322 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 396,303 | 3.963 | 20 | 50 | fits | 89,061 | 115 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 476,554 | 4.766 | 20 | 20 | fits | 80,317 | 28 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 834,791 | 8.348 | 20 | 20 | fits | 47,176 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 410,821 | 4.108 | 20 | 20 | fits | 87,078 | 115 | 0.386 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 379,075 | 3.791 | 20 | 200 | fits | 145,802 | 277 | 0.333 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 465,537 | 4.655 | 20 | 200 | fits | 87,078 | 115 | 0.386 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 379,999 | 3.800 | 20 | 20 | fits | 145,802 | 277 | 0.333 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 466,241 | 4.662 | 20 | 20 | fits | 87,078 | 115 | 0.386 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 227,502 | 2.275 | 20 | 24 | fits | 147,177 | 165 | 0.408 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 382,649 | 3.826 | 20 | 24 | fits | 145,802 | 277 | 0.333 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 382,583 | 3.826 | 20 | 50 | fits | 145,802 | 277 | 0.333 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 469,265 | 4.693 | 20 | 50 | fits | 87,078 | 115 | 0.386 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 549,658 | 5.497 | 20 | 20 | fits | 80,459 | 28 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 907,792 | 9.078 | 20 | 20 | fits | 47,157 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 312,776 | 3.128 | 20 | 20 | fits | 103,761 | 107 | 0.559 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 301,836 | 3.018 | 20 | 200 | fits | 148,411 | 288 | 0.316 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 404,981 | 4.050 | 20 | 200 | fits | 103,761 | 107 | 0.559 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 302,760 | 3.028 | 20 | 20 | fits | 148,411 | 288 | 0.316 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 405,685 | 4.057 | 20 | 20 | fits | 103,761 | 107 | 0.559 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 147,488 | 1.475 | 20 | 24 | fits | 149,063 | 165 | 0.410 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 305,410 | 3.054 | 20 | 24 | fits | 148,411 | 288 | 0.316 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 305,344 | 3.053 | 20 | 50 | fits | 148,411 | 288 | 0.316 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 408,709 | 4.087 | 20 | 50 | fits | 103,761 | 107 | 0.559 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 408,643 | 4.086 | 20 | 20 | fits | 103,761 | 107 | 0.559 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 825,289 | 8.253 | 20 | 20 | fits | 26,061 | 12 | 0.803 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 329,032 | 3.290 | 20 | 20 | fits | 80,380 | 118 | 0.368 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 296,846 | 2.968 | 20 | 200 | fits | 143,760 | 266 | 0.324 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 376,610 | 3.766 | 20 | 200 | fits | 80,380 | 118 | 0.368 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 297,770 | 2.978 | 20 | 20 | fits | 143,760 | 266 | 0.324 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 377,314 | 3.773 | 20 | 20 | fits | 80,380 | 118 | 0.368 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 147,578 | 1.476 | 20 | 24 | fits | 144,989 | 162 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 300,420 | 3.004 | 20 | 24 | fits | 143,760 | 266 | 0.324 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 300,354 | 3.004 | 20 | 50 | fits | 143,760 | 266 | 0.324 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 380,338 | 3.803 | 20 | 50 | fits | 80,380 | 118 | 0.368 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 460,822 | 4.608 | 20 | 20 | fits | 80,550 | 28 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 819,379 | 8.194 | 20 | 20 | fits | 47,171 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 328,514 | 3.285 | 20 | 20 | fits | 104,026 | 110 | 0.534 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 296,590 | 2.966 | 20 | 200 | fits | 147,528 | 284 | 0.321 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 400,000 | 4.000 | 20 | 200 | fits | 104,026 | 110 | 0.534 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 297,514 | 2.975 | 20 | 20 | fits | 147,528 | 284 | 0.321 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 400,704 | 4.007 | 20 | 20 | fits | 104,026 | 110 | 0.534 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 143,554 | 1.436 | 20 | 24 | fits | 144,890 | 162 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 300,164 | 3.002 | 20 | 24 | fits | 147,528 | 284 | 0.321 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 300,098 | 3.001 | 20 | 50 | fits | 147,528 | 284 | 0.321 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 403,728 | 4.037 | 20 | 50 | fits | 104,026 | 110 | 0.534 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 403,662 | 4.037 | 20 | 20 | fits | 104,026 | 110 | 0.534 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 820,381 | 8.204 | 20 | 20 | fits | 26,062 | 12 | 0.803 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 316,055 | 3.161 | 20 | 20 | fits | 101,681 | 104 | 0.523 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 286,107 | 2.861 | 20 | 200 | fits | 146,969 | 284 | 0.309 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 387,172 | 3.872 | 20 | 200 | fits | 101,681 | 104 | 0.523 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 287,031 | 2.870 | 20 | 20 | fits | 146,969 | 284 | 0.309 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 387,876 | 3.879 | 20 | 20 | fits | 101,681 | 104 | 0.523 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 143,702 | 1.437 | 20 | 24 | fits | 145,038 | 161 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 289,681 | 2.897 | 20 | 24 | fits | 146,969 | 284 | 0.309 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 289,615 | 2.896 | 20 | 50 | fits | 146,969 | 284 | 0.309 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 390,900 | 3.909 | 20 | 50 | fits | 101,681 | 104 | 0.523 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 390,834 | 3.908 | 20 | 20 | fits | 101,681 | 104 | 0.523 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 906,824 | 9.068 | 20 | 20 | fits | 27,482 | 13 | 0.825 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 303,863 | 3.039 | 20 | 20 | fits | 101,131 | 101 | 0.548 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 294,826 | 2.948 | 20 | 200 | fits | 147,332 | 283 | 0.308 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 395,341 | 3.953 | 20 | 200 | fits | 101,131 | 101 | 0.548 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 295,750 | 2.958 | 20 | 20 | fits | 147,332 | 283 | 0.308 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 396,045 | 3.960 | 20 | 20 | fits | 101,131 | 101 | 0.548 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 152,058 | 1.521 | 20 | 24 | fits | 145,038 | 161 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 298,400 | 2.984 | 20 | 24 | fits | 147,332 | 283 | 0.308 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 298,334 | 2.983 | 20 | 50 | fits | 147,332 | 283 | 0.308 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 399,069 | 3.991 | 20 | 50 | fits | 101,131 | 101 | 0.548 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 399,003 | 3.990 | 20 | 20 | fits | 101,131 | 101 | 0.548 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 915,329 | 9.153 | 20 | 20 | fits | 26,155 | 12 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 300,138 | 3.001 | 20 | 20 | fits | 101,303 | 101 | 0.549 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 291,144 | 2.911 | 20 | 200 | fits | 147,210 | 283 | 0.304 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 391,831 | 3.918 | 20 | 200 | fits | 101,303 | 101 | 0.549 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 292,068 | 2.921 | 20 | 20 | fits | 147,210 | 283 | 0.304 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 392,535 | 3.925 | 20 | 20 | fits | 101,303 | 101 | 0.549 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 148,498 | 1.485 | 20 | 24 | fits | 145,038 | 161 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 294,718 | 2.947 | 20 | 24 | fits | 147,210 | 283 | 0.304 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 294,652 | 2.947 | 20 | 50 | fits | 147,210 | 283 | 0.304 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 395,559 | 3.956 | 20 | 50 | fits | 101,303 | 101 | 0.549 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 395,493 | 3.955 | 20 | 20 | fits | 101,303 | 101 | 0.549 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 911,965 | 9.120 | 20 | 20 | fits | 26,148 | 12 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 315,401 | 3.154 | 20 | 20 | fits | 101,102 | 102 | 0.546 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 287,566 | 2.876 | 20 | 200 | fits | 147,192 | 283 | 0.304 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 388,052 | 3.881 | 20 | 200 | fits | 101,102 | 102 | 0.546 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 288,490 | 2.885 | 20 | 20 | fits | 147,192 | 283 | 0.304 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 388,756 | 3.888 | 20 | 20 | fits | 101,102 | 102 | 0.546 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 144,938 | 1.449 | 20 | 24 | fits | 145,038 | 161 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 291,140 | 2.911 | 20 | 24 | fits | 147,192 | 283 | 0.304 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 291,074 | 2.911 | 20 | 50 | fits | 147,192 | 283 | 0.304 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 391,780 | 3.918 | 20 | 50 | fits | 101,102 | 102 | 0.546 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 391,714 | 3.917 | 20 | 20 | fits | 101,102 | 102 | 0.546 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 907,418 | 9.074 | 20 | 20 | fits | 36,707 | 16 | 0.753 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 337,892 | 3.379 | 20 | 20 | fits | 86,533 | 110 | 0.483 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 295,229 | 2.952 | 20 | 200 | fits | 147,375 | 284 | 0.307 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 392,527 | 3.925 | 20 | 200 | fits | 86,533 | 110 | 0.483 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 296,153 | 2.962 | 20 | 20 | fits | 147,375 | 284 | 0.307 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 393,231 | 3.932 | 20 | 20 | fits | 86,533 | 110 | 0.483 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 152,418 | 1.524 | 20 | 24 | fits | 145,038 | 161 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 298,803 | 2.988 | 20 | 24 | fits | 147,375 | 284 | 0.307 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 298,737 | 2.987 | 20 | 50 | fits | 147,375 | 284 | 0.307 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 396,255 | 3.963 | 20 | 50 | fits | 86,533 | 110 | 0.483 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 553,908 | 5.539 | 20 | 20 | fits | 80,990 | 29 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 912,322 | 9.123 | 20 | 20 | fits | 47,178 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 408,137 | 4.081 | 20 | 20 | fits | 87,433 | 115 | 0.396 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 299,665 | 2.997 | 20 | 200 | fits | 145,601 | 277 | 0.334 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 463,134 | 4.631 | 20 | 200 | fits | 87,433 | 115 | 0.396 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 300,589 | 3.006 | 20 | 20 | fits | 145,601 | 277 | 0.334 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 463,838 | 4.638 | 20 | 20 | fits | 87,433 | 115 | 0.396 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 148,830 | 1.488 | 20 | 24 | fits | 145,010 | 162 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 303,239 | 3.032 | 20 | 24 | fits | 145,601 | 277 | 0.334 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 303,173 | 3.032 | 20 | 50 | fits | 145,601 | 277 | 0.334 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 466,862 | 4.669 | 20 | 50 | fits | 87,433 | 115 | 0.396 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 547,176 | 5.472 | 20 | 20 | fits | 80,380 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 909,480 | 9.095 | 20 | 20 | fits | 51,299 | 27 | 0.731 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 319,525 | 3.195 | 20 | 20 | fits | 101,775 | 105 | 0.523 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 289,577 | 2.896 | 20 | 200 | fits | 146,131 | 279 | 0.311 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 390,736 | 3.907 | 20 | 200 | fits | 101,775 | 105 | 0.523 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 290,501 | 2.905 | 20 | 20 | fits | 146,131 | 279 | 0.311 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 391,440 | 3.914 | 20 | 20 | fits | 101,775 | 105 | 0.523 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 148,010 | 1.480 | 20 | 24 | fits | 145,038 | 161 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 293,151 | 2.932 | 20 | 24 | fits | 146,131 | 279 | 0.311 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 293,085 | 2.931 | 20 | 50 | fits | 146,131 | 279 | 0.311 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 394,464 | 3.945 | 20 | 50 | fits | 101,775 | 105 | 0.523 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 394,398 | 3.944 | 20 | 20 | fits | 101,775 | 105 | 0.523 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 828,830 | 8.288 | 20 | 20 | fits | 26,062 | 12 | 0.803 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 316,741 | 3.167 | 20 | 20 | fits | 80,539 | 103 | 0.470 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 287,360 | 2.874 | 20 | 200 | fits | 148,222 | 289 | 0.306 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 378,664 | 3.787 | 20 | 200 | fits | 80,539 | 103 | 0.470 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 288,284 | 2.883 | 20 | 20 | fits | 148,222 | 289 | 0.306 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 379,368 | 3.794 | 20 | 20 | fits | 80,539 | 103 | 0.470 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 143,702 | 1.437 | 20 | 24 | fits | 145,038 | 161 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 290,934 | 2.909 | 20 | 24 | fits | 148,222 | 289 | 0.306 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 290,868 | 2.909 | 20 | 50 | fits | 148,222 | 289 | 0.306 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 382,392 | 3.824 | 20 | 50 | fits | 80,539 | 103 | 0.470 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 462,646 | 4.626 | 20 | 20 | fits | 80,320 | 28 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 821,053 | 8.211 | 20 | 20 | fits | 47,178 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 310,139 | 3.101 | 20 | 20 | fits | 80,973 | 118 | 0.378 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 301,145 | 3.011 | 20 | 200 | fits | 143,783 | 266 | 0.324 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 381,502 | 3.815 | 20 | 200 | fits | 80,973 | 118 | 0.378 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 302,069 | 3.021 | 20 | 20 | fits | 143,783 | 266 | 0.324 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 382,206 | 3.822 | 20 | 20 | fits | 80,973 | 118 | 0.378 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 151,920 | 1.519 | 20 | 24 | fits | 145,028 | 162 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 304,719 | 3.047 | 20 | 24 | fits | 143,783 | 266 | 0.324 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 304,653 | 3.047 | 20 | 50 | fits | 143,783 | 266 | 0.324 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 385,230 | 3.852 | 20 | 50 | fits | 80,973 | 118 | 0.378 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 465,662 | 4.657 | 20 | 20 | fits | 80,498 | 28 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 828,973 | 8.290 | 20 | 20 | fits | 47,201 | 20 | 0.718 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 303,982 | 3.040 | 20 | 20 | fits | 101,397 | 101 | 0.551 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 294,988 | 2.950 | 20 | 200 | fits | 147,208 | 283 | 0.305 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 395,769 | 3.958 | 20 | 200 | fits | 101,397 | 101 | 0.551 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 295,912 | 2.959 | 20 | 20 | fits | 147,208 | 283 | 0.305 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 396,473 | 3.965 | 20 | 20 | fits | 101,397 | 101 | 0.551 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 152,344 | 1.523 | 20 | 24 | fits | 144,954 | 161 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 298,562 | 2.986 | 20 | 24 | fits | 147,208 | 283 | 0.305 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 298,496 | 2.985 | 20 | 50 | fits | 147,208 | 283 | 0.305 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 399,497 | 3.995 | 20 | 50 | fits | 101,397 | 101 | 0.551 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 399,431 | 3.994 | 20 | 20 | fits | 101,397 | 101 | 0.551 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 839,372 | 8.394 | 20 | 20 | fits | 32,571 | 19 | 0.846 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 319,245 | 3.192 | 20 | 20 | fits | 101,072 | 101 | 0.547 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 291,410 | 2.914 | 20 | 200 | fits | 147,190 | 283 | 0.305 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 391,866 | 3.919 | 20 | 200 | fits | 101,072 | 101 | 0.547 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 292,334 | 2.923 | 20 | 20 | fits | 147,190 | 283 | 0.305 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 392,570 | 3.926 | 20 | 20 | fits | 101,072 | 101 | 0.547 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 148,784 | 1.488 | 20 | 24 | fits | 144,954 | 161 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 294,984 | 2.950 | 20 | 24 | fits | 147,190 | 283 | 0.305 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 294,918 | 2.949 | 20 | 50 | fits | 147,190 | 283 | 0.305 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 395,594 | 3.956 | 20 | 50 | fits | 101,072 | 101 | 0.547 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 395,528 | 3.955 | 20 | 20 | fits | 101,072 | 101 | 0.547 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 837,170 | 8.372 | 20 | 20 | fits | 26,347 | 12 | 0.809 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 316,737 | 3.167 | 20 | 20 | fits | 101,775 | 104 | 0.524 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 286,789 | 2.868 | 20 | 200 | fits | 146,129 | 279 | 0.311 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 387,948 | 3.879 | 20 | 200 | fits | 101,775 | 104 | 0.524 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 287,713 | 2.877 | 20 | 20 | fits | 146,129 | 279 | 0.311 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 388,652 | 3.887 | 20 | 20 | fits | 101,775 | 104 | 0.524 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 145,224 | 1.452 | 20 | 24 | fits | 144,954 | 161 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 290,363 | 2.904 | 20 | 24 | fits | 146,129 | 279 | 0.311 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 290,297 | 2.903 | 20 | 50 | fits | 146,129 | 279 | 0.311 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 391,676 | 3.917 | 20 | 50 | fits | 101,775 | 104 | 0.524 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 391,610 | 3.916 | 20 | 20 | fits | 101,775 | 104 | 0.524 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 831,979 | 8.320 | 20 | 20 | fits | 26,149 | 12 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 322,040 | 3.220 | 20 | 20 | fits | 81,804 | 103 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 295,470 | 2.955 | 20 | 200 | fits | 147,330 | 283 | 0.308 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 376,658 | 3.767 | 20 | 200 | fits | 81,804 | 103 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 296,394 | 2.964 | 20 | 20 | fits | 147,330 | 283 | 0.308 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 377,362 | 3.774 | 20 | 20 | fits | 81,804 | 103 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 152,704 | 1.527 | 20 | 24 | fits | 144,954 | 161 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 299,044 | 2.990 | 20 | 24 | fits | 147,330 | 283 | 0.308 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 298,978 | 2.990 | 20 | 50 | fits | 147,330 | 283 | 0.308 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 380,386 | 3.804 | 20 | 50 | fits | 81,804 | 103 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 461,246 | 4.612 | 20 | 20 | fits | 80,926 | 29 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 837,858 | 8.379 | 20 | 20 | fits | 47,157 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 313,043 | 3.130 | 20 | 20 | fits | 85,375 | 124 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 290,667 | 2.907 | 20 | 200 | fits | 146,087 | 267 | 0.316 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 386,674 | 3.867 | 20 | 200 | fits | 85,375 | 124 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 291,591 | 2.916 | 20 | 20 | fits | 146,087 | 267 | 0.316 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 387,378 | 3.874 | 20 | 20 | fits | 85,375 | 124 | 0.451 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 149,144 | 1.491 | 20 | 24 | fits | 144,954 | 161 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 294,241 | 2.942 | 20 | 24 | fits | 146,087 | 267 | 0.316 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 294,175 | 2.942 | 20 | 50 | fits | 146,087 | 267 | 0.316 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 390,402 | 3.904 | 20 | 50 | fits | 85,375 | 124 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 470,892 | 4.709 | 20 | 20 | fits | 80,556 | 28 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 829,398 | 8.294 | 20 | 20 | fits | 47,157 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 299,951 | 3.000 | 20 | 20 | fits | 101,363 | 102 | 0.548 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 290,957 | 2.910 | 20 | 200 | fits | 147,360 | 283 | 0.307 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 391,704 | 3.917 | 20 | 200 | fits | 101,363 | 102 | 0.548 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 291,881 | 2.919 | 20 | 20 | fits | 147,360 | 283 | 0.307 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 392,408 | 3.924 | 20 | 20 | fits | 101,363 | 102 | 0.548 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 148,161 | 1.482 | 20 | 24 | fits | 144,954 | 161 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 294,531 | 2.945 | 20 | 24 | fits | 147,360 | 283 | 0.307 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 294,465 | 2.945 | 20 | 50 | fits | 147,360 | 283 | 0.307 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 395,432 | 3.954 | 20 | 50 | fits | 101,363 | 102 | 0.548 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 395,366 | 3.954 | 20 | 20 | fits | 101,363 | 102 | 0.548 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 830,031 | 8.300 | 20 | 20 | fits | 26,061 | 12 | 0.803 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 329,583 | 3.296 | 20 | 20 | fits | 85,413 | 124 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 282,168 | 2.822 | 20 | 200 | fits | 143,114 | 267 | 0.314 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 378,194 | 3.782 | 20 | 200 | fits | 85,413 | 124 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 283,092 | 2.831 | 20 | 20 | fits | 143,114 | 267 | 0.314 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 378,898 | 3.789 | 20 | 20 | fits | 85,413 | 124 | 0.449 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 143,618 | 1.436 | 20 | 24 | fits | 144,954 | 161 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 285,742 | 2.857 | 20 | 24 | fits | 143,114 | 267 | 0.314 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 285,676 | 2.857 | 20 | 50 | fits | 143,114 | 267 | 0.314 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 381,922 | 3.819 | 20 | 50 | fits | 85,413 | 124 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 462,412 | 4.624 | 20 | 20 | fits | 80,556 | 28 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 820,918 | 8.209 | 20 | 20 | fits | 47,171 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 321,559 | 3.216 | 20 | 20 | fits | 100,914 | 101 | 0.542 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 306,590 | 3.066 | 20 | 200 | fits | 149,011 | 288 | 0.318 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 406,888 | 4.069 | 20 | 200 | fits | 100,914 | 101 | 0.542 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 307,514 | 3.075 | 20 | 20 | fits | 149,011 | 288 | 0.318 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 407,592 | 4.076 | 20 | 20 | fits | 100,914 | 101 | 0.542 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 152,071 | 1.521 | 20 | 24 | fits | 144,944 | 162 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 310,164 | 3.102 | 20 | 24 | fits | 149,011 | 288 | 0.318 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 310,098 | 3.101 | 20 | 50 | fits | 149,011 | 288 | 0.318 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 410,616 | 4.106 | 20 | 50 | fits | 100,914 | 101 | 0.542 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 410,550 | 4.106 | 20 | 20 | fits | 100,914 | 101 | 0.542 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 918,609 | 9.186 | 20 | 20 | fits | 31,925 | 20 | 0.814 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 310,530 | 3.105 | 20 | 20 | fits | 100,925 | 101 | 0.541 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 295,561 | 2.956 | 20 | 200 | fits | 147,430 | 283 | 0.309 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 395,870 | 3.959 | 20 | 200 | fits | 100,925 | 101 | 0.541 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 296,485 | 2.965 | 20 | 20 | fits | 147,430 | 283 | 0.309 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 396,574 | 3.966 | 20 | 20 | fits | 100,925 | 101 | 0.541 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 152,695 | 1.527 | 20 | 24 | fits | 145,038 | 161 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 299,135 | 2.991 | 20 | 24 | fits | 147,430 | 283 | 0.309 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 299,069 | 2.991 | 20 | 50 | fits | 147,430 | 283 | 0.309 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 399,598 | 3.996 | 20 | 50 | fits | 100,925 | 101 | 0.541 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 399,532 | 3.995 | 20 | 20 | fits | 100,925 | 101 | 0.541 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 923,753 | 9.238 | 20 | 20 | fits | 30,239 | 13 | 0.857 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 301,087 | 3.011 | 20 | 20 | fits | 101,065 | 101 | 0.547 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 291,988 | 2.920 | 20 | 200 | fits | 147,417 | 283 | 0.309 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 392,437 | 3.924 | 20 | 200 | fits | 101,065 | 101 | 0.547 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 292,912 | 2.929 | 20 | 20 | fits | 147,417 | 283 | 0.309 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 393,141 | 3.931 | 20 | 20 | fits | 101,065 | 101 | 0.547 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 149,135 | 1.491 | 20 | 24 | fits | 145,038 | 161 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 295,562 | 2.956 | 20 | 24 | fits | 147,417 | 283 | 0.309 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 295,496 | 2.955 | 20 | 50 | fits | 147,417 | 283 | 0.309 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 396,165 | 3.962 | 20 | 50 | fits | 101,065 | 101 | 0.547 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 396,099 | 3.961 | 20 | 20 | fits | 101,065 | 101 | 0.547 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 920,599 | 9.206 | 20 | 20 | fits | 26,148 | 12 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 297,362 | 2.974 | 20 | 20 | fits | 101,237 | 101 | 0.548 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 288,306 | 2.883 | 20 | 200 | fits | 147,295 | 283 | 0.305 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 388,927 | 3.889 | 20 | 200 | fits | 101,237 | 101 | 0.548 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 289,230 | 2.892 | 20 | 20 | fits | 147,295 | 283 | 0.305 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 389,631 | 3.896 | 20 | 20 | fits | 101,237 | 101 | 0.548 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 145,575 | 1.456 | 20 | 24 | fits | 145,038 | 161 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 291,880 | 2.919 | 20 | 24 | fits | 147,295 | 283 | 0.305 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 291,814 | 2.918 | 20 | 50 | fits | 147,295 | 283 | 0.305 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 392,655 | 3.927 | 20 | 50 | fits | 101,237 | 101 | 0.548 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 392,589 | 3.926 | 20 | 20 | fits | 101,237 | 101 | 0.548 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 916,877 | 9.169 | 20 | 20 | fits | 26,237 | 12 | 0.806 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 329,760 | 3.298 | 20 | 20 | fits | 82,080 | 106 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 294,705 | 2.947 | 20 | 200 | fits | 146,214 | 279 | 0.311 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 376,169 | 3.762 | 20 | 200 | fits | 82,080 | 106 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 295,629 | 2.956 | 20 | 20 | fits | 146,214 | 279 | 0.311 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 376,873 | 3.769 | 20 | 20 | fits | 82,080 | 106 | 0.406 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 153,055 | 1.531 | 20 | 24 | fits | 145,038 | 161 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 298,279 | 2.983 | 20 | 24 | fits | 146,214 | 279 | 0.311 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 298,213 | 2.982 | 20 | 50 | fits | 146,214 | 279 | 0.311 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 379,897 | 3.799 | 20 | 50 | fits | 82,080 | 106 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 545,449 | 5.454 | 20 | 20 | fits | 84,655 | 36 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 920,488 | 9.205 | 20 | 20 | fits | 47,245 | 20 | 0.718 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 414,239 | 4.142 | 20 | 20 | fits | 89,445 | 115 | 0.435 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 289,335 | 2.893 | 20 | 200 | fits | 144,404 | 278 | 0.322 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 469,005 | 4.690 | 20 | 200 | fits | 89,445 | 115 | 0.435 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 290,259 | 2.903 | 20 | 20 | fits | 144,404 | 278 | 0.322 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 469,709 | 4.697 | 20 | 20 | fits | 89,445 | 115 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 149,495 | 1.495 | 20 | 24 | fits | 145,038 | 161 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 292,909 | 2.929 | 20 | 24 | fits | 144,404 | 278 | 0.322 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 292,843 | 2.928 | 20 | 50 | fits | 144,404 | 278 | 0.322 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 472,733 | 4.727 | 20 | 50 | fits | 89,445 | 115 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 553,091 | 5.531 | 20 | 20 | fits | 80,424 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 911,340 | 9.113 | 20 | 20 | fits | 47,178 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 319,210 | 3.192 | 20 | 20 | fits | 100,930 | 101 | 0.545 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 291,327 | 2.913 | 20 | 200 | fits | 147,277 | 283 | 0.305 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 391,641 | 3.916 | 20 | 200 | fits | 100,930 | 101 | 0.545 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 292,251 | 2.923 | 20 | 20 | fits | 147,277 | 283 | 0.305 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 392,345 | 3.923 | 20 | 20 | fits | 100,930 | 101 | 0.545 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 148,614 | 1.486 | 20 | 24 | fits | 145,038 | 161 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 294,901 | 2.949 | 20 | 24 | fits | 147,277 | 283 | 0.305 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 294,835 | 2.948 | 20 | 50 | fits | 147,277 | 283 | 0.305 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 395,369 | 3.954 | 20 | 50 | fits | 100,930 | 101 | 0.545 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 395,303 | 3.953 | 20 | 20 | fits | 100,930 | 101 | 0.545 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 831,078 | 8.311 | 20 | 20 | fits | 26,075 | 12 | 0.803 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 316,700 | 3.167 | 20 | 20 | fits | 101,686 | 104 | 0.522 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 286,704 | 2.867 | 20 | 200 | fits | 146,214 | 279 | 0.311 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 387,774 | 3.878 | 20 | 200 | fits | 101,686 | 104 | 0.522 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 287,628 | 2.876 | 20 | 20 | fits | 146,214 | 279 | 0.311 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 388,478 | 3.885 | 20 | 20 | fits | 101,686 | 104 | 0.522 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 145,054 | 1.451 | 20 | 24 | fits | 145,038 | 161 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 290,278 | 2.903 | 20 | 24 | fits | 146,214 | 279 | 0.311 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 290,212 | 2.902 | 20 | 50 | fits | 146,214 | 279 | 0.311 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 391,502 | 3.915 | 20 | 50 | fits | 101,686 | 104 | 0.522 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 391,436 | 3.914 | 20 | 20 | fits | 101,686 | 104 | 0.522 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 827,221 | 8.272 | 20 | 20 | fits | 26,149 | 12 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 318,459 | 3.185 | 20 | 20 | fits | 80,900 | 104 | 0.479 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 295,475 | 2.955 | 20 | 200 | fits | 147,505 | 284 | 0.309 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 387,140 | 3.871 | 20 | 200 | fits | 80,900 | 104 | 0.479 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 296,399 | 2.964 | 20 | 20 | fits | 147,505 | 284 | 0.309 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 387,844 | 3.878 | 20 | 20 | fits | 80,900 | 104 | 0.479 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 152,534 | 1.525 | 20 | 24 | fits | 145,038 | 161 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 299,049 | 2.990 | 20 | 24 | fits | 147,505 | 284 | 0.309 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 298,983 | 2.990 | 20 | 50 | fits | 147,505 | 284 | 0.309 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 390,868 | 3.909 | 20 | 50 | fits | 80,900 | 104 | 0.479 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 471,423 | 4.714 | 20 | 20 | fits | 80,621 | 28 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 834,635 | 8.346 | 20 | 20 | fits | 47,201 | 20 | 0.718 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 314,610 | 3.146 | 20 | 20 | fits | 80,734 | 104 | 0.474 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 291,766 | 2.918 | 20 | 200 | fits | 147,356 | 284 | 0.305 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 383,341 | 3.833 | 20 | 200 | fits | 80,734 | 104 | 0.474 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 292,690 | 2.927 | 20 | 20 | fits | 147,356 | 284 | 0.305 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 384,045 | 3.840 | 20 | 20 | fits | 80,734 | 104 | 0.474 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 148,974 | 1.490 | 20 | 24 | fits | 145,038 | 161 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 295,340 | 2.953 | 20 | 24 | fits | 147,356 | 284 | 0.305 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 295,274 | 2.953 | 20 | 50 | fits | 147,356 | 284 | 0.305 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 387,069 | 3.871 | 20 | 50 | fits | 80,734 | 104 | 0.474 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 467,507 | 4.675 | 20 | 20 | fits | 80,504 | 28 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 830,668 | 8.307 | 20 | 20 | fits | 47,157 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 326,935 | 3.269 | 20 | 20 | fits | 80,514 | 118 | 0.370 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 294,701 | 2.947 | 20 | 200 | fits | 143,891 | 266 | 0.324 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 374,599 | 3.746 | 20 | 200 | fits | 80,514 | 118 | 0.370 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 295,625 | 2.956 | 20 | 20 | fits | 143,891 | 266 | 0.324 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 375,303 | 3.753 | 20 | 20 | fits | 80,514 | 118 | 0.370 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 145,368 | 1.454 | 20 | 24 | fits | 144,992 | 162 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 298,275 | 2.983 | 20 | 24 | fits | 143,891 | 266 | 0.324 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 298,209 | 2.982 | 20 | 50 | fits | 143,891 | 266 | 0.324 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 378,327 | 3.783 | 20 | 50 | fits | 80,514 | 118 | 0.370 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 458,874 | 4.589 | 20 | 20 | fits | 80,613 | 28 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 822,345 | 8.223 | 20 | 20 | fits | 47,171 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 316,453 | 3.165 | 20 | 20 | fits | 100,944 | 101 | 0.545 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 288,620 | 2.886 | 20 | 200 | fits | 147,342 | 283 | 0.307 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 388,948 | 3.889 | 20 | 200 | fits | 100,944 | 101 | 0.545 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 289,544 | 2.895 | 20 | 20 | fits | 147,342 | 283 | 0.307 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 389,652 | 3.897 | 20 | 20 | fits | 100,944 | 101 | 0.545 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 145,842 | 1.458 | 20 | 24 | fits | 144,954 | 161 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 292,194 | 2.922 | 20 | 24 | fits | 147,342 | 283 | 0.307 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 292,128 | 2.921 | 20 | 50 | fits | 147,342 | 283 | 0.307 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 392,676 | 3.927 | 20 | 50 | fits | 100,944 | 101 | 0.545 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 392,610 | 3.926 | 20 | 20 | fits | 100,944 | 101 | 0.545 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 833,507 | 8.335 | 20 | 20 | fits | 30,246 | 13 | 0.859 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 323,570 | 3.236 | 20 | 20 | fits | 81,802 | 103 | 0.436 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 296,253 | 2.963 | 20 | 200 | fits | 147,495 | 283 | 0.310 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 377,439 | 3.774 | 20 | 200 | fits | 81,802 | 103 | 0.436 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 297,177 | 2.972 | 20 | 20 | fits | 147,495 | 283 | 0.310 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 378,143 | 3.781 | 20 | 20 | fits | 81,802 | 103 | 0.436 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 153,322 | 1.533 | 20 | 24 | fits | 144,954 | 161 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 299,827 | 2.998 | 20 | 24 | fits | 147,495 | 283 | 0.310 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 299,761 | 2.998 | 20 | 50 | fits | 147,495 | 283 | 0.310 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 381,167 | 3.812 | 20 | 50 | fits | 81,802 | 103 | 0.436 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 461,743 | 4.617 | 20 | 20 | fits | 80,642 | 28 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 838,561 | 8.386 | 20 | 20 | fits | 47,176 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 319,109 | 3.191 | 20 | 20 | fits | 84,618 | 109 | 0.364 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 289,566 | 2.896 | 20 | 200 | fits | 144,368 | 277 | 0.324 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 373,568 | 3.736 | 20 | 200 | fits | 84,618 | 109 | 0.364 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 290,490 | 2.905 | 20 | 20 | fits | 144,368 | 277 | 0.324 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 374,272 | 3.743 | 20 | 20 | fits | 84,618 | 109 | 0.364 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 149,762 | 1.498 | 20 | 24 | fits | 144,954 | 161 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 293,140 | 2.931 | 20 | 24 | fits | 144,368 | 277 | 0.324 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 293,074 | 2.931 | 20 | 50 | fits | 144,368 | 277 | 0.324 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 377,296 | 3.773 | 20 | 50 | fits | 84,618 | 109 | 0.364 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 457,582 | 4.576 | 20 | 20 | fits | 80,352 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 834,574 | 8.346 | 20 | 20 | fits | 47,244 | 20 | 0.718 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 316,481 | 3.165 | 20 | 20 | fits | 101,168 | 101 | 0.549 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 307,444 | 3.074 | 20 | 200 | fits | 148,693 | 288 | 0.315 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 407,996 | 4.080 | 20 | 200 | fits | 101,168 | 101 | 0.549 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 308,368 | 3.084 | 20 | 20 | fits | 148,693 | 288 | 0.315 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 408,700 | 4.087 | 20 | 20 | fits | 101,168 | 101 | 0.549 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 153,267 | 1.533 | 20 | 24 | fits | 145,137 | 162 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 311,018 | 3.110 | 20 | 24 | fits | 148,693 | 288 | 0.315 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 310,952 | 3.110 | 20 | 50 | fits | 148,693 | 288 | 0.315 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 411,724 | 4.117 | 20 | 50 | fits | 101,168 | 101 | 0.549 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 411,658 | 4.117 | 20 | 20 | fits | 101,168 | 101 | 0.549 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 828,157 | 8.282 | 20 | 20 | fits | 26,063 | 12 | 0.803 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 307,883 | 3.079 | 20 | 20 | fits | 81,043 | 118 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 298,889 | 2.989 | 20 | 200 | fits | 143,766 | 266 | 0.324 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 379,316 | 3.793 | 20 | 200 | fits | 81,043 | 118 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 299,813 | 2.998 | 20 | 20 | fits | 143,766 | 266 | 0.324 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 380,020 | 3.800 | 20 | 20 | fits | 81,043 | 118 | 0.379 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 149,639 | 1.496 | 20 | 24 | fits | 145,069 | 162 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 302,463 | 3.025 | 20 | 24 | fits | 143,766 | 266 | 0.324 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 302,397 | 3.024 | 20 | 50 | fits | 143,766 | 266 | 0.324 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 383,044 | 3.830 | 20 | 50 | fits | 81,043 | 118 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 463,394 | 4.634 | 20 | 20 | fits | 80,416 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 821,862 | 8.219 | 20 | 20 | fits | 47,159 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 302,793 | 3.028 | 20 | 20 | fits | 101,434 | 101 | 0.551 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 293,799 | 2.938 | 20 | 200 | fits | 147,362 | 283 | 0.306 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 394,617 | 3.946 | 20 | 200 | fits | 101,434 | 101 | 0.551 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 294,723 | 2.947 | 20 | 20 | fits | 147,362 | 283 | 0.306 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 395,321 | 3.953 | 20 | 20 | fits | 101,434 | 101 | 0.551 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 151,001 | 1.510 | 20 | 24 | fits | 144,954 | 161 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 297,373 | 2.974 | 20 | 24 | fits | 147,362 | 283 | 0.306 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 297,307 | 2.973 | 20 | 50 | fits | 147,362 | 283 | 0.306 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 398,345 | 3.983 | 20 | 50 | fits | 101,434 | 101 | 0.551 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 398,279 | 3.983 | 20 | 20 | fits | 101,434 | 101 | 0.551 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 914,927 | 9.149 | 20 | 20 | fits | 27,224 | 13 | 0.817 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 318,104 | 3.181 | 20 | 20 | fits | 101,117 | 101 | 0.548 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 290,221 | 2.902 | 20 | 200 | fits | 147,344 | 283 | 0.306 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 390,722 | 3.907 | 20 | 200 | fits | 101,117 | 101 | 0.548 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 291,145 | 2.911 | 20 | 20 | fits | 147,344 | 283 | 0.306 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 391,426 | 3.914 | 20 | 20 | fits | 101,117 | 101 | 0.548 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 147,441 | 1.474 | 20 | 24 | fits | 144,954 | 161 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 293,795 | 2.938 | 20 | 24 | fits | 147,344 | 283 | 0.306 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 293,729 | 2.937 | 20 | 50 | fits | 147,344 | 283 | 0.306 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 394,450 | 3.945 | 20 | 50 | fits | 101,117 | 101 | 0.548 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 394,384 | 3.944 | 20 | 20 | fits | 101,117 | 101 | 0.548 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 911,411 | 9.114 | 20 | 20 | fits | 26,251 | 12 | 0.806 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 316,171 | 3.162 | 20 | 20 | fits | 101,790 | 104 | 0.524 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 286,175 | 2.862 | 20 | 200 | fits | 147,121 | 284 | 0.311 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 387,349 | 3.873 | 20 | 200 | fits | 101,790 | 104 | 0.524 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 287,099 | 2.871 | 20 | 20 | fits | 147,121 | 284 | 0.311 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 388,053 | 3.881 | 20 | 20 | fits | 101,790 | 104 | 0.524 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 143,618 | 1.436 | 20 | 24 | fits | 144,954 | 161 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 289,749 | 2.897 | 20 | 24 | fits | 147,121 | 284 | 0.311 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 289,683 | 2.897 | 20 | 50 | fits | 147,121 | 284 | 0.311 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 391,077 | 3.911 | 20 | 50 | fits | 101,790 | 104 | 0.524 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 391,011 | 3.910 | 20 | 20 | fits | 101,790 | 104 | 0.524 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 908,143 | 9.081 | 20 | 20 | fits | 26,149 | 12 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 303,318 | 3.033 | 20 | 20 | fits | 101,356 | 102 | 0.549 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 294,281 | 2.943 | 20 | 200 | fits | 147,484 | 283 | 0.310 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 395,021 | 3.950 | 20 | 200 | fits | 101,356 | 102 | 0.549 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 295,205 | 2.952 | 20 | 20 | fits | 147,484 | 283 | 0.310 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 395,725 | 3.957 | 20 | 20 | fits | 101,356 | 102 | 0.549 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 151,361 | 1.514 | 20 | 24 | fits | 144,954 | 161 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 297,855 | 2.979 | 20 | 24 | fits | 147,484 | 283 | 0.310 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 297,789 | 2.978 | 20 | 50 | fits | 147,484 | 283 | 0.310 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 398,749 | 3.987 | 20 | 50 | fits | 101,356 | 102 | 0.549 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 398,683 | 3.987 | 20 | 20 | fits | 101,356 | 102 | 0.549 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 915,193 | 9.152 | 20 | 20 | fits | 36,693 | 16 | 0.753 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 332,376 | 3.324 | 20 | 20 | fits | 86,275 | 110 | 0.482 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 290,693 | 2.907 | 20 | 200 | fits | 147,456 | 284 | 0.306 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 387,743 | 3.877 | 20 | 200 | fits | 86,275 | 110 | 0.482 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 291,617 | 2.916 | 20 | 20 | fits | 147,456 | 284 | 0.306 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 388,447 | 3.884 | 20 | 20 | fits | 86,275 | 110 | 0.482 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 147,801 | 1.478 | 20 | 24 | fits | 144,954 | 161 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 294,267 | 2.943 | 20 | 24 | fits | 147,456 | 284 | 0.306 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 294,201 | 2.942 | 20 | 50 | fits | 147,456 | 284 | 0.306 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 391,471 | 3.915 | 20 | 50 | fits | 86,275 | 110 | 0.482 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 550,272 | 5.503 | 20 | 20 | fits | 80,994 | 29 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 908,867 | 9.089 | 20 | 20 | fits | 47,157 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 331,703 | 3.317 | 20 | 20 | fits | 87,664 | 130 | 0.411 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 292,501 | 2.925 | 20 | 200 | fits | 143,505 | 266 | 0.324 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 379,549 | 3.795 | 20 | 200 | fits | 87,664 | 130 | 0.411 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 293,425 | 2.934 | 20 | 20 | fits | 143,505 | 266 | 0.324 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 380,253 | 3.803 | 20 | 20 | fits | 87,664 | 130 | 0.411 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 143,654 | 1.437 | 20 | 24 | fits | 144,990 | 162 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 296,075 | 2.961 | 20 | 24 | fits | 143,505 | 266 | 0.324 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 296,009 | 2.960 | 20 | 50 | fits | 143,505 | 266 | 0.324 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 383,277 | 3.833 | 20 | 50 | fits | 87,664 | 130 | 0.411 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 542,079 | 5.421 | 20 | 20 | fits | 80,995 | 29 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 900,618 | 9.006 | 20 | 20 | fits | 47,263 | 21 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 304,270 | 3.043 | 20 | 20 | fits | 101,528 | 102 | 0.550 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 295,276 | 2.953 | 20 | 200 | fits | 147,362 | 283 | 0.306 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 396,188 | 3.962 | 20 | 200 | fits | 101,528 | 102 | 0.550 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 296,200 | 2.962 | 20 | 20 | fits | 147,362 | 283 | 0.306 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 396,892 | 3.969 | 20 | 20 | fits | 101,528 | 102 | 0.550 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 152,478 | 1.525 | 20 | 24 | fits | 144,954 | 161 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 298,850 | 2.989 | 20 | 24 | fits | 147,362 | 283 | 0.306 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 298,784 | 2.988 | 20 | 50 | fits | 147,362 | 283 | 0.306 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 399,916 | 3.999 | 20 | 50 | fits | 101,528 | 102 | 0.550 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 399,850 | 3.998 | 20 | 20 | fits | 101,528 | 102 | 0.550 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 834,369 | 8.344 | 20 | 20 | fits | 26,061 | 12 | 0.803 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 334,992 | 3.350 | 20 | 20 | fits | 81,157 | 104 | 0.478 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 291,801 | 2.918 | 20 | 200 | fits | 147,447 | 284 | 0.306 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 383,733 | 3.837 | 20 | 200 | fits | 81,157 | 104 | 0.478 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 292,725 | 2.927 | 20 | 20 | fits | 147,447 | 284 | 0.306 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 384,437 | 3.844 | 20 | 20 | fits | 81,157 | 104 | 0.478 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 148,918 | 1.489 | 20 | 24 | fits | 144,954 | 161 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 295,375 | 2.954 | 20 | 24 | fits | 147,447 | 284 | 0.306 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 295,309 | 2.953 | 20 | 50 | fits | 147,447 | 284 | 0.306 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 387,461 | 3.875 | 20 | 50 | fits | 81,157 | 104 | 0.478 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 467,642 | 4.676 | 20 | 20 | fits | 80,247 | 28 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 826,167 | 8.262 | 20 | 20 | fits | 47,171 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 328,662 | 3.287 | 20 | 20 | fits | 101,574 | 104 | 0.522 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 298,844 | 2.988 | 20 | 200 | fits | 147,825 | 284 | 0.321 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 399,802 | 3.998 | 20 | 200 | fits | 101,574 | 104 | 0.522 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 299,768 | 2.998 | 20 | 20 | fits | 147,825 | 284 | 0.321 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 400,506 | 4.005 | 20 | 20 | fits | 101,574 | 104 | 0.522 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 145,421 | 1.454 | 20 | 24 | fits | 145,017 | 162 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 302,418 | 3.024 | 20 | 24 | fits | 147,825 | 284 | 0.321 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 302,352 | 3.024 | 20 | 50 | fits | 147,825 | 284 | 0.321 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 403,530 | 4.035 | 20 | 50 | fits | 101,574 | 104 | 0.522 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 403,464 | 4.035 | 20 | 20 | fits | 101,574 | 104 | 0.522 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 824,588 | 8.246 | 20 | 20 | fits | 26,137 | 12 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 318,344 | 3.183 | 20 | 20 | fits | 101,652 | 104 | 0.522 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 288,392 | 2.884 | 20 | 200 | fits | 146,150 | 279 | 0.311 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 389,428 | 3.894 | 20 | 200 | fits | 101,652 | 104 | 0.522 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 289,316 | 2.893 | 20 | 20 | fits | 146,150 | 279 | 0.311 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 390,132 | 3.901 | 20 | 20 | fits | 101,652 | 104 | 0.522 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 146,806 | 1.468 | 20 | 24 | fits | 144,975 | 161 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 291,966 | 2.920 | 20 | 24 | fits | 146,150 | 279 | 0.311 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 291,900 | 2.919 | 20 | 50 | fits | 146,150 | 279 | 0.311 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 393,156 | 3.932 | 20 | 50 | fits | 101,652 | 104 | 0.522 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 393,090 | 3.931 | 20 | 20 | fits | 101,652 | 104 | 0.522 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 832,805 | 8.328 | 20 | 20 | fits | 32,597 | 19 | 0.846 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 301,999 | 3.020 | 20 | 20 | fits | 100,923 | 101 | 0.542 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 287,044 | 2.870 | 20 | 200 | fits | 148,239 | 288 | 0.307 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 387,351 | 3.874 | 20 | 200 | fits | 100,923 | 101 | 0.542 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 287,968 | 2.880 | 20 | 20 | fits | 148,239 | 288 | 0.307 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 388,055 | 3.881 | 20 | 20 | fits | 100,923 | 101 | 0.542 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 143,369 | 1.434 | 20 | 24 | fits | 145,038 | 161 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 290,618 | 2.906 | 20 | 24 | fits | 148,239 | 288 | 0.307 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 290,552 | 2.906 | 20 | 50 | fits | 148,239 | 288 | 0.307 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 391,079 | 3.911 | 20 | 50 | fits | 100,923 | 101 | 0.542 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 391,013 | 3.910 | 20 | 20 | fits | 100,923 | 101 | 0.542 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 831,256 | 8.313 | 20 | 20 | fits | 26,363 | 12 | 0.808 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 302,545 | 3.025 | 20 | 20 | fits | 101,257 | 101 | 0.549 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 293,551 | 2.936 | 20 | 200 | fits | 147,266 | 283 | 0.305 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 394,192 | 3.942 | 20 | 200 | fits | 101,257 | 101 | 0.549 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 294,475 | 2.945 | 20 | 20 | fits | 147,266 | 283 | 0.305 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 394,896 | 3.949 | 20 | 20 | fits | 101,257 | 101 | 0.549 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 150,849 | 1.508 | 20 | 24 | fits | 145,038 | 161 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 297,125 | 2.971 | 20 | 24 | fits | 147,266 | 283 | 0.305 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 297,059 | 2.971 | 20 | 50 | fits | 147,266 | 283 | 0.305 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 397,920 | 3.979 | 20 | 50 | fits | 101,257 | 101 | 0.549 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 397,854 | 3.979 | 20 | 20 | fits | 101,257 | 101 | 0.549 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 838,037 | 8.380 | 20 | 20 | fits | 26,148 | 12 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 323,297 | 3.233 | 20 | 20 | fits | 81,461 | 103 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 289,973 | 2.900 | 20 | 200 | fits | 147,248 | 283 | 0.305 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 370,818 | 3.708 | 20 | 200 | fits | 81,461 | 103 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 290,897 | 2.909 | 20 | 20 | fits | 147,248 | 283 | 0.305 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 371,522 | 3.715 | 20 | 20 | fits | 81,461 | 103 | 0.430 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 147,289 | 1.473 | 20 | 24 | fits | 145,038 | 161 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 293,547 | 2.935 | 20 | 24 | fits | 147,248 | 283 | 0.305 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 293,481 | 2.935 | 20 | 50 | fits | 147,248 | 283 | 0.305 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 374,546 | 3.745 | 20 | 50 | fits | 81,461 | 103 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 455,174 | 4.552 | 20 | 20 | fits | 80,694 | 29 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 831,692 | 8.317 | 20 | 20 | fits | 47,171 | 20 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 336,670 | 3.367 | 20 | 20 | fits | 86,767 | 112 | 0.462 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 286,313 | 2.863 | 20 | 200 | fits | 147,175 | 285 | 0.310 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 383,921 | 3.839 | 20 | 200 | fits | 86,767 | 112 | 0.462 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 287,237 | 2.872 | 20 | 20 | fits | 147,175 | 285 | 0.310 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 384,625 | 3.846 | 20 | 20 | fits | 86,767 | 112 | 0.462 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 143,702 | 1.437 | 20 | 24 | fits | 145,038 | 161 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 289,887 | 2.899 | 20 | 24 | fits | 147,175 | 285 | 0.310 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 289,821 | 2.898 | 20 | 50 | fits | 147,175 | 285 | 0.310 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 387,649 | 3.876 | 20 | 50 | fits | 86,767 | 112 | 0.462 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 468,044 | 4.680 | 20 | 20 | fits | 80,461 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 826,344 | 8.263 | 20 | 20 | fits | 47,160 | 20 | 0.717 |
| LINK_UP | `adp.link_up.if0` | 2,235 | 0.022 | 20 | 200 | fits | 22,110 | 43 (11) | 0.654 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 13,079 | 0.131 | 20 | 200 | fits | 17,230 | 23 (39) | 0.553 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 4,272 | 0.043 | 20 | 200 | fits | 2,137 | 10 (11) | 0.333 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 153,753 | 1.538 | 20 | 200 | fits | 154,693 | 260 | 0.370 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 201,039 | 2.010 | 20 | 20 | fits | 139,463 | 264 | 0.213 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 225,819 | 2.258 | 20 | 24 | fits | 55,034 | 45 | 0.469 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 186,349 | 1.863 | 20 | 50 | fits | 92,208 | 81 | 0.664 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 744,303 | 7.443 | 20 | 20 | fits | 51,538 | 26 | 0.747 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 239,100 | 2.391 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 153,753 | 1.538 | 20 | 200 | fits | 154,693 | 260 | 0.370 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 208,746 | 2.087 | 20 | 20 | fits | 140,823 | 270 | 0.220 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 220,138 | 2.201 | 20 | 24 | fits | 56,359 | 51 | 0.469 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 178,943 | 1.789 | 20 | 50 | fits | 84,802 | 83 | 0.683 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 760,188 | 7.602 | 20 | 20 | fits | 62,514 | 36 | 0.704 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 246,803 | 2.468 | 49 | 49 | fits | 0 | - | 0.000 |
| Talker Advertise RX for every input, bound | `srp.bound_advertise.if0` | 64,580 | 0.646 | 20 | 20 | fits | 64,646 | 15 | 0.912 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 17,075 | 0.171 | 20 | 20 | fits | 25,835 | 21 (35) | 0.788 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 12,826 | 0.128 | 20 | 20 | fits | 21,990 | 17 (14) | 0.825 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 15,976 | 0.160 | 20 | 20 | fits | 20,526 | 18 (14) | 0.805 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 10,673 | 0.107 | 20 | 20 | fits | 24,806 | 21 (35) | 0.764 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 69,364 | 0.694 | 20 | 20 | fits | 28,411 | 8 | 0.835 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 35,040 | 0.350 | 20 | 20 | fits | 35,106 | 12 | 0.876 |
| malformed MRPDU discard | `srp.malformed.if0` | 16,969 | 0.170 | 20 | 20 | fits | 17,035 | 12 | 0.700 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 71,892 | 0.719 | 220 | 220 | fits | 49,010 | 6 | 0.917 |
| an event behind 15 others | `backlog.event.if0` | 155,931 | 1.559 | 20 | 200 | fits | 44,342 | 78 | 0.505 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 352,187 | 3.522 | 20 | 20 | fits | 131,099 | 161 | 0.224 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 372,472 | 3.725 | 20 | 200 | fits | 131,099 | 161 | 0.224 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 371,856 | 3.719 | 20 | 200 | fits | 131,099 | 161 | 0.224 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 368,150 | 3.682 | 20 | 20 | fits | 131,099 | 161 | 0.224 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 367,314 | 3.673 | 20 | 20 | fits | 131,099 | 161 | 0.224 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 146,091 | 1.461 | 20 | 24 | fits | 146,982 | 167 | 0.406 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 239,701 | 2.397 | 20 | 24 | fits | 50,258 | 26 | 0.684 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 370,734 | 3.707 | 20 | 50 | fits | 131,099 | 161 | 0.224 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 370,338 | 3.703 | 20 | 50 | fits | 131,099 | 161 | 0.224 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 399,689 | 3.997 | 20 | 20 | fits | 26,993 | 57 | 0.119 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 446,238 | 4.462 | 20 | 20 | fits | 21,144 | 40 | 0.070 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 302,017 | 3.020 | 20 | 20 | fits | 100,486 | 102 | 0.540 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 287,431 | 2.874 | 20 | 200 | fits | 146,795 | 283 | 0.304 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 387,301 | 3.873 | 20 | 200 | fits | 100,486 | 102 | 0.540 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 288,355 | 2.884 | 20 | 20 | fits | 146,795 | 283 | 0.304 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 388,005 | 3.880 | 20 | 20 | fits | 100,486 | 102 | 0.540 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 145,200 | 1.452 | 20 | 24 | fits | 145,386 | 164 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 291,005 | 2.910 | 20 | 24 | fits | 146,795 | 283 | 0.304 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 290,939 | 2.909 | 20 | 50 | fits | 146,795 | 283 | 0.304 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 391,029 | 3.910 | 20 | 50 | fits | 100,486 | 102 | 0.540 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 390,963 | 3.910 | 20 | 20 | fits | 100,486 | 102 | 0.540 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 829,429 | 8.294 | 20 | 20 | fits | 26,075 | 12 | 0.803 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,328 | 0.083 | 20 | 20 | fits | 23,520 | 19 | 0.766 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 287,431 | 2.874 | 20 | 200 | fits | 146,795 | 283 | 0.304 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 23,748 | 0.237 | 20 | 200 | fits | 23,520 | 19 | 0.766 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 288,355 | 2.884 | 20 | 20 | fits | 146,795 | 283 | 0.304 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 377,729 | 3.777 | 20 | 20 | fits | 90,210 | 92 | 0.501 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 145,200 | 1.452 | 20 | 24 | fits | 145,386 | 164 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 291,005 | 2.910 | 20 | 24 | fits | 146,795 | 283 | 0.304 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 290,939 | 2.909 | 20 | 50 | fits | 146,795 | 283 | 0.304 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 380,753 | 3.808 | 20 | 50 | fits | 90,210 | 92 | 0.501 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 380,687 | 3.807 | 20 | 20 | fits | 90,210 | 92 | 0.501 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 818,906 | 8.189 | 20 | 20 | fits | 26,075 | 12 | 0.803 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,260,184 | 62.602 | 20 | 20 | MISS ceiling | 15,525 | 13 | 0.435 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,275,749 | 62.757 | 20 | 20 | MISS ceiling | 15,423 | 13 | 0.408 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,290,987 | 62.910 | 20 | 20 | MISS ceiling | 15,295 | 13 | 0.425 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,306,215 | 63.062 | 20 | 20 | MISS ceiling | 15,304 | 13 | 0.417 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,321,464 | 63.215 | 20 | 20 | MISS ceiling | 15,312 | 13 | 0.417 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 152,929 | 1.529 | 20 | 200 | fits | 147,483 | 234 | 0.388 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 243,992 | 2.440 | 20 | 200 | fits | 91,679 | 153 | 0.494 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 148,607 | 1.486 | 20 | 20 | fits | 147,483 | 234 | 0.388 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,186,158 | 61.862 | 20 | 20 | MISS ceiling | 25,136 | 15 | 0.634 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 152,247 | 1.522 | 20 | 24 | fits | 147,483 | 234 | 0.388 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,164,508 | 61.645 | 20 | 24 | MISS ceiling | 126,738 | 106 | 0.430 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 151,191 | 1.512 | 20 | 50 | fits | 147,483 | 234 | 0.388 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 242,474 | 2.425 | 20 | 50 | fits | 91,679 | 153 | 0.494 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 242,408 | 2.424 | 20 | 20 | fits | 91,679 | 153 | 0.494 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 670,619 | 6.706 | 20 | 20 | fits | 27,288 | 12 | 0.826 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,628 | 0.056 | 20 | 20 | fits | 19,489 | 13 (29) | 0.662 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 9,067 | 0.091 | 20 | 20 | fits | 24,761 | 19 (35) | 0.791 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 20,826 | 0.208 | 20 | 20 | fits | 25,220 | 21 (12) | 0.777 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 9,577 | 0.096 | 20 | 50 | fits | 22,110 | 43 | 0.654 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 16,053 | 0.161 | 20 | 50 | fits | 19,014 | 35 | 0.602 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 13,654 | 0.137 | 20 | 50 | fits | 18,753 | 35 | 0.594 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 18,200 | 0.182 | 20 | 50 | fits | 23,458 | 61 | 0.542 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 20,150 | 0.202 | 20 | 50 | fits | 23,458 | 61 | 0.542 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 8,324 | 0.083 | 20 | 50 | fits | 18,749 | 30 | 0.591 |
| LINK_UP | `adp.link_up.if0` | 2,235 | 0.022 | 20 | 200 | fits | 22,110 | 43 (11) | 0.654 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 13,079 | 0.131 | 20 | 200 | fits | 17,230 | 23 (39) | 0.553 |
| LINK_DOWN | `adp.link_down.if0` | 1,954 | 0.020 | 20 | 200 | fits | 19,133 | 23 (9) | 0.679 |
| LINK_UP | `adp.link_up.if0` | 2,235 | 0.022 | 20 | 200 | fits | 22,110 | 43 (11) | 0.654 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 13,079 | 0.131 | 20 | 200 | fits | 17,230 | 23 (39) | 0.553 |
| GM_CHANGE | `adp.gm_change.if0` | 2,031 | 0.020 | 20 | 200 | fits | 11,641 | 17 (11) | 0.250 |
| LINK_UP | `adp.link_up.if0` | 2,235 | 0.022 | 20 | 200 | fits | 22,110 | 43 (11) | 0.654 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 13,079 | 0.131 | 20 | 200 | fits | 17,230 | 23 (39) | 0.553 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,965 | 0.050 | 20 | 200 | fits | 13,279 | 16 (31) | 0.517 |
| LINK_UP | `adp.link_up.if0` | 2,235 | 0.022 | 20 | 200 | fits | 22,110 | 43 (11) | 0.654 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 13,079 | 0.131 | 20 | 200 | fits | 17,230 | 23 (39) | 0.553 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,965 | 0.050 | 20 | 200 | fits | 13,279 | 16 (31) | 0.517 |
| set_name | `aecp_fanout.set_name.if0` | 44,660 | 0.447 | 20 | 24 | fits | 55,433 | 89 | 0.560 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 44,565 | 0.446 | 20 | 24 | fits | 50,738 | 78 | 0.592 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 42,182 | 0.422 | 20 | 24 | fits | 45,217 | 79 | 0.546 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 37,243 | 0.372 | 20 | 24 | fits | 42,807 | 78 | 0.514 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 53,626 | 0.536 | 20 | 24 | fits | 61,412 | 110 | 0.595 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 317,894 | 3.179 | 20 | 24 | fits | 59,380 | 110 | 0.585 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 282,477 | 2.825 | 20 | 24 | fits | 52,338 | 73 | 0.598 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 37,703 | 0.377 | 20 | 24 | fits | 43,858 | 78 | 0.532 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 42,586 | 0.426 | 20 | 24 | fits | 44,580 | 79 | 0.549 |
| BIND_RX | `acmp.bind_rx.if0` | 18,080 | 0.181 | 20 | 20 | fits | 37,474 | 26 (77) | 0.755 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,215 | 0.092 | 20 | 20 | fits | 27,565 | 19 (32) | 0.799 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,135 | 0.101 | 20 | 20 | fits | 21,422 | 15 (47) | 0.678 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 12,664 | 0.127 | 20 | 20 | fits | 34,133 | 19 (50) | 0.771 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,715 | 0.107 | 20 | 20 | fits | 22,808 | 17 (48) | 0.698 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 8,769 | 0.088 | 20 | 20 | fits | 20,886 | 16 (48) | 0.591 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 8,472 | 0.085 | 20 | 20 | fits | 20,103 | 16 (48) | 0.578 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 8,398 | 0.084 | 20 | 20 | fits | 19,909 | 16 (48) | 0.568 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 15,105 | 0.151 | 20 | 24 | fits | 24,687 | 20 | 0.750 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 24,418 | 0.244 | 20 | 24 | fits | 28,267 | 20 | 0.676 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 19,771 | 0.198 | 20 | 24 | fits | 25,086 | 20 | 0.709 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 20,715 | 0.207 | 20 | 24 | fits | 24,332 | 20 | 0.693 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 20,590 | 0.206 | 20 | 24 | fits | 25,227 | 20 | 0.695 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 19,625 | 0.196 | 20 | 24 | fits | 24,861 | 20 | 0.699 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 20,598 | 0.206 | 20 | 24 | fits | 23,957 | 20 | 0.699 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 19,256 | 0.193 | 20 | 24 | fits | 24,434 | 20 | 0.717 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 20,439 | 0.204 | 20 | 24 | fits | 23,582 | 20 | 0.711 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 21,312 | 0.213 | 20 | 24 | fits | 26,457 | 21 | 0.609 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 19,959 | 0.200 | 20 | 24 | fits | 23,336 | 20 | 0.731 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 20,447 | 0.204 | 20 | 24 | fits | 26,101 | 26 | 0.701 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 18,754 | 0.188 | 20 | 24 | fits | 23,975 | 20 | 0.698 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 21,386 | 0.214 | 20 | 24 | fits | 24,875 | 20 | 0.707 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 18,765 | 0.188 | 20 | 24 | fits | 24,019 | 20 | 0.717 |
| get_configuration | `aecp.get_configuration.if0` | 18,908 | 0.189 | 20 | 24 | fits | 21,846 | 20 | 0.709 |
| entity_available | `aecp.entity_available.if0` | 17,064 | 0.171 | 20 | 24 | fits | 21,780 | 20 | 0.695 |
| get_name | `aecp.get_name.if0` | 21,346 | 0.213 | 20 | 24 | fits | 24,835 | 20 | 0.730 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 20,886 | 0.209 | 20 | 24 | fits | 26,575 | 26 | 0.708 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 20,651 | 0.207 | 20 | 24 | fits | 25,833 | 29 | 0.721 |
| get_as_path, refused ENTITY_MISBEHAVING | `aecp.get_as_path.if0` | 11,340 | 0.113 | 20 | 24 | fits | 25,274 | 29 | 0.721 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 17,399 | 0.174 | 20 | 24 | fits | 22,408 | 20 | 0.723 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 13,624 | 0.136 | 20 | 24 | fits | 21,212 | 20 | 0.691 |
| set_name | `aecp.set_name.if0` | 26,087 | 0.261 | 20 | 24 | fits | 42,525 | 43 | 0.743 |
| lock_entity | `aecp.lock_entity.if0` | 14,720 | 0.147 | 20 | 24 | fits | 33,911 | 34 | 0.779 |
| unlock_entity | `aecp.unlock_entity.if0` | 23,162 | 0.232 | 20 | 24 | fits | 32,428 | 33 | 0.764 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 130,897 | 1.309 | 20 | 24 | fits | 142,621 | 137 | 0.314 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 270,605 | 2.706 | 20 | 24 | fits | 136,209 | 115 | 0.299 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 241,700 | 2.417 | 20 | 24 | fits | 40,340 | 17 | 0.668 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 386,599 | 3.866 | 20 | 24 | fits | 78,930 | 18 | 0.672 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 348,539 | 3.485 | 20 | 24 | fits | 88,836 | 17 | 0.672 |
| READ_DESCRIPTOR held for a token (#917) | `aecp.held.read_descriptor.if0` | 520,342 | 5.203 | 20 | 24 | fits | 27,930 | 17 | 0.700 |
| LINK_UP | `fixture.link_up.if0` | 2,235 | 0.022 | 20 | 200 | fits | 22,110 | 43 (11) | 0.654 |
| malformed MRPDU discard | `fixture.malformed.if0` | 16,962 | 0.170 | 20 | 20 | fits | 17,028 | 12 | 0.700 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 31,168 | 0.312 | 20 | 24 | fits | 44,265 | 43 | 0.771 |
| LINK_DOWN | `fixture.link_down.if0` | 2,326 | 0.023 | 20 | 200 | fits | 21,049 | 23 (9) | 0.727 |
| BIND_RX | `fixture.bind_rx.if0` | 18,283 | 0.183 | 20 | 20 | fits | 37,868 | 26 (77) | 0.753 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 13,753 | 0.138 | 20 | 20 | fits | 33,763 | 29 (35) | 0.768 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 10,522 | 0.105 | 20 | 20 | fits | 21,131 | 13 (29) | 0.748 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 77,487 | 0.775 | 20 | 200 | fits | 77,591 | 77 | 0.728 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 77,487 | 0.775 | 20 | 200 | fits | 77,591 | 77 | 0.728 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 77,213 | 0.772 | 20 | 20 | fits | 77,591 | 77 | 0.728 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 77,213 | 0.772 | 20 | 20 | fits | 77,591 | 77 | 0.728 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 77,421 | 0.774 | 20 | 24 | fits | 77,591 | 77 | 0.728 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 77,421 | 0.774 | 20 | 24 | fits | 77,591 | 77 | 0.728 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 77,355 | 0.774 | 20 | 50 | fits | 77,591 | 77 | 0.728 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 77,355 | 0.774 | 20 | 50 | fits | 77,591 | 77 | 0.728 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 77,289 | 0.773 | 20 | 20 | fits | 77,591 | 77 | 0.728 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 77,289 | 0.773 | 20 | 20 | fits | 77,591 | 77 | 0.728 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
