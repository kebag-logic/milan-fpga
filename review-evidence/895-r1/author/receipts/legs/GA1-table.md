### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 87 paths and 7 of 945 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.185 (0.370) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.087 (0.196) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.068 (0.210) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.132 (0.398) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.097 (0.206) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.091 (0.194) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.093 (0.205) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.100 (0.218) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.086 (0.252) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.209 (0.491) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.167 (0.450) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.187 (0.470) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.092 (0.387) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.068 (0.276) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.055 (0.212) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.126 (0.317) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.040 (0.131) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.022 (0.129) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.024 (0.220) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.024 (0.223) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.122 (0.258) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.122 (0.382) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.098 (0.332) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.186 (0.441) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.148 (0.397) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.132 (0.374) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.172 (0.424) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.190 (0.285) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.096 (0.345) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.209 (0.464) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.120 (0.361) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.121 (0.359) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.166 (0.417) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.143 (0.383) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.161 (0.413) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.111 (0.350) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.165 (0.420) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.167 (0.420) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.171 (0.424) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.118 (0.356) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.123 (0.366) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.130 (0.381) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.170 (0.421) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.210 (0.463) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.248 (0.385) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.145 (0.419) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.255 (0.489) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 0.370 (0.478) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.353 (0.439) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.437 (0.693) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.430 (0.685) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.355 (0.442) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.426 (0.551) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.480 (0.719) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.367 (0.603) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.449 (5.191) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-0.adp_available.if0` (backlog-adp@verify-0) | 6.504 (7.777) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.129 (0.413) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.611 (2.243) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.916 (63.155) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.490 (63.728) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.275 (0.384) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 5.220 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 1.520 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 2.554 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 4.825 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 3.984 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.180 (0.449) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.089 (0.180) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.103 (0.223) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.159 (0.449) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.168 (0.421) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 0.894 | fits | 0 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 2.192 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.205 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 2.183 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-6.service.adp.last.if0` (backlog-adp@program-aged2-6) | 7.215 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.228 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.985 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 2.218 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-6.service.maap.last.if0` (backlog-adp@program-aged2-6) | 7.251 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-7.service.srp.first.if0` (backlog-adp@verify-aged2-7) | 6.373 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-5.service.srp.last.if0` (backlog-adp@verify-aged2-5) | 8.468 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.713 (1.069) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.359 (0.360) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.159 (0.159) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.680 (0.742) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 8.976 | 8 | 154,300 (1.543) | yes | - |
| backlog-adp@blank-1 | 0 | 8.237 | 8 | 150,701 (1.507) | yes | - |
| backlog-adp@blank-2 | 0 | 9.065 | 8 | 150,990 (1.510) | yes | - |
| backlog-adp@blank-3 | 0 | 9.046 | 7 | 151,333 (1.513) | yes | - |
| backlog-adp@blank-4 | 0 | 9.086 | 7 | 154,184 (1.542) | yes | - |
| backlog-adp@blank-5 | 0 | 8.899 | 6 | 152,253 (1.523) | yes | - |
| backlog-adp@blank-6 | 0 | 8.909 | 7 | 155,892 (1.559) | yes | - |
| backlog-adp@blank-7 | 0 | 9.129 | 8 | 155,772 (1.558) | yes | - |
| backlog-adp@program-0 | 0 | 8.190 | 7 | 155,962 (1.560) | yes | - |
| backlog-adp@program-1 | 0 | 8.919 | 6 | 148,631 (1.486) | yes | - |
| backlog-adp@program-2 | 0 | 9.285 | 8 | 156,516 (1.565) | yes | - |
| backlog-adp@program-3 | 0 | 9.126 | 8 | 148,369 (1.484) | yes | - |
| backlog-adp@program-4 | 0 | 8.236 | 7 | 155,943 (1.559) | yes | - |
| backlog-adp@program-5 | 0 | 8.295 | 8 | 149,598 (1.496) | yes | - |
| backlog-adp@program-6 | 0 | 8.210 | 6 | 150,505 (1.505) | yes | - |
| backlog-adp@program-7 | 0 | 8.280 | 7 | 155,780 (1.558) | yes | - |
| backlog-adp@verify-0 | 0 | 8.788 | 8 | 156,731 (1.567) | yes | - |
| backlog-adp@verify-1 | 0 | 8.205 | 7 | 150,480 (1.505) | yes | - |
| backlog-adp@verify-2 | 0 | 9.010 | 8 | 157,311 (1.573) | yes | - |
| backlog-adp@verify-3 | 0 | 9.012 | 7 | 157,992 (1.580) | yes | - |
| backlog-adp@verify-4 | 0 | 9.052 | 7 | 155,958 (1.560) | yes | - |
| backlog-adp@verify-5 | 0 | 8.971 | 7 | 156,047 (1.560) | yes | - |
| backlog-adp@verify-6 | 1 | 9.159 | 7 | 150,328 (1.503) | yes | - |
| backlog-adp@verify-7 | 0 | 9.090 | 8 | 152,335 (1.523) | yes | - |
| backlog-adp@blank-aged2-0 | 1 | 8.869 | 6 | 155,457 (1.555) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 9.960 | 8 | 156,113 (1.561) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 9.536 | 10 | 152,492 (1.525) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 9.086 | 7 | 153,541 (1.535) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 8.974 | 6 | 152,115 (1.521) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 8.909 | 6 | 157,232 (1.572) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 8.900 | 6 | 157,232 (1.572) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 8.868 | 6 | 157,333 (1.573) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 8.857 | 6 | 155,161 (1.552) | yes | - |
| backlog-adp@blank-aged1-1 | 1 | 10.554 | 8 | 155,161 (1.552) | yes | - |
| backlog-adp@blank-aged1-2 | 1 | 9.632 | 8 | 155,255 (1.553) | yes | - |
| backlog-adp@blank-aged1-3 | 1 | 9.546 | 7 | 155,043 (1.550) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 10.065 | 10 | 155,745 (1.557) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 9.644 | 9 | 158,518 (1.585) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 9.522 | 8 | 155,679 (1.557) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 9.687 | 9 | 157,142 (1.571) | yes | - |
| backlog-adp@program-aged2-0 | 1 | 8.878 | 6 | 155,707 (1.557) | yes | - |
| backlog-adp@program-aged2-1 | 1 | 9.783 | 9 | 155,707 (1.557) | yes | - |
| backlog-adp@program-aged2-2 | 1 | 8.908 | 7 | 149,681 (1.497) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 8.877 | 7 | 155,918 (1.559) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 9.144 | 8 | 146,477 (1.465) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 8.986 | 7 | 156,387 (1.564) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 9.001 | 7 | 156,438 (1.564) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 9.375 | 10 | 149,604 (1.496) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 8.948 | 7 | 151,142 (1.511) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 9.280 | 8 | 150,777 (1.508) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 9.544 | 10 | 149,277 (1.493) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 9.157 | 8 | 157,227 (1.572) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 9.182 | 8 | 155,409 (1.554) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 9.016 | 7 | 157,502 (1.575) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 9.054 | 7 | 158,055 (1.581) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 9.041 | 7 | 155,409 (1.554) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 9.005 | 8 | 156,469 (1.565) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 9.940 | 8 | 156,579 (1.566) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 8.948 | 8 | 156,614 (1.566) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 8.934 | 7 | 157,368 (1.574) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 9.075 | 7 | 151,152 (1.512) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 8.896 | 6 | 151,977 (1.520) | yes | - |
| backlog-adp@verify-aged2-6 | 1 | 9.036 | 7 | 149,330 (1.493) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 9.096 | 7 | 146,838 (1.468) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 8.846 | 6 | 148,540 (1.485) | yes | - |
| backlog-adp@verify-aged1-1 | 1 | 10.253 | 9 | 148,540 (1.485) | yes | - |
| backlog-adp@verify-aged1-2 | 1 | 8.986 | 7 | 150,417 (1.504) | yes | - |
| backlog-adp@verify-aged1-3 | 1 | 8.922 | 6 | 150,417 (1.504) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 8.964 | 7 | 155,735 (1.557) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 8.927 | 7 | 157,994 (1.580) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 8.935 | 7 | 157,550 (1.575) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 9.318 | 9 | 155,885 (1.559) | yes | - |
| backlog | 0 | 5.836 | 8 | 150,565 (1.506) | yes | - |
| backlog-adp | 0 | 8.239 | 7 | 156,603 (1.566) | yes | - |
| backlog-adp-refill | 0 | 40.665 | 22 | 151,313 (1.513) | yes | - |
| backlog-owed | 0 | 64.008 | 22 | 161,050 (1.611) | yes | - |
| fixture | 0 | 1.109 | 2 | 72,325 (0.723) | yes | - |

Composed maximum over the 4 backlog windows: 161,050 CPU cycles (1.611 ms), backlog-owed.
Over the windows that released their whole load only: 161,050 (1.611 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3597 | 0 | 51,897 (0.519) | fits |
| save-second | 60468 | 0 | 51,897 (0.519) | fits |
| backlog-adp@blank-0 | 400 | 0 | 154,300 (1.543) | fits |
| backlog-adp@blank-1 | 400 | 0 | 150,701 (1.507) | fits |
| backlog-adp@blank-2 | 400 | 0 | 150,990 (1.510) | fits |
| backlog-adp@blank-3 | 399 | 0 | 151,333 (1.513) | fits |
| backlog-adp@blank-4 | 399 | 0 | 154,184 (1.542) | fits |
| backlog-adp@blank-5 | 399 | 0 | 155,937 (1.559) | fits |
| backlog-adp@blank-6 | 399 | 0 | 155,892 (1.559) | fits |
| backlog-adp@blank-7 | 402 | 0 | 155,772 (1.558) | fits |
| backlog-adp@program-0 | 494 | 0 | 155,962 (1.560) | fits |
| backlog-adp@program-1 | 494 | 0 | 148,631 (1.486) | fits |
| backlog-adp@program-2 | 497 | 0 | 156,516 (1.565) | fits |
| backlog-adp@program-3 | 497 | 0 | 148,369 (1.484) | fits |
| backlog-adp@program-4 | 497 | 0 | 155,943 (1.559) | fits |
| backlog-adp@program-5 | 498 | 0 | 149,598 (1.496) | fits |
| backlog-adp@program-6 | 499 | 0 | 150,505 (1.505) | fits |
| backlog-adp@program-7 | 499 | 0 | 155,780 (1.558) | fits |
| backlog-adp@verify-0 | 583 | 0 | 156,731 (1.567) | fits |
| backlog-adp@verify-1 | 583 | 0 | 150,480 (1.505) | fits |
| backlog-adp@verify-2 | 583 | 0 | 157,311 (1.573) | fits |
| backlog-adp@verify-3 | 582 | 0 | 157,992 (1.580) | fits |
| backlog-adp@verify-4 | 582 | 0 | 155,958 (1.560) | fits |
| backlog-adp@verify-5 | 582 | 0 | 156,047 (1.560) | fits |
| backlog-adp@verify-6 | 584 | 0 | 156,619 (1.566) | fits |
| backlog-adp@verify-7 | 585 | 0 | 152,335 (1.523) | fits |
| backlog-adp@blank-aged2-0 | 785 | 0 | 155,457 (1.555) | fits |
| backlog-adp@blank-aged2-1 | 795 | 0 | 156,113 (1.561) | fits |
| backlog-adp@blank-aged2-2 | 807 | 0 | 152,492 (1.525) | fits |
| backlog-adp@blank-aged2-3 | 814 | 0 | 153,541 (1.535) | fits |
| backlog-adp@blank-aged2-4 | 823 | 0 | 152,115 (1.521) | fits |
| backlog-adp@blank-aged2-5 | 833 | 0 | 157,232 (1.572) | fits |
| backlog-adp@blank-aged2-6 | 843 | 0 | 157,232 (1.572) | fits |
| backlog-adp@blank-aged2-7 | 853 | 0 | 157,333 (1.573) | fits |
| backlog-adp@blank-aged1-0 | 708 | 0 | 155,161 (1.552) | fits |
| backlog-adp@blank-aged1-1 | 720 | 0 | 155,161 (1.552) | fits |
| backlog-adp@blank-aged1-2 | 730 | 0 | 155,255 (1.553) | fits |
| backlog-adp@blank-aged1-3 | 739 | 0 | 155,043 (1.550) | fits |
| backlog-adp@blank-aged1-4 | 751 | 0 | 155,745 (1.557) | fits |
| backlog-adp@blank-aged1-5 | 760 | 0 | 158,518 (1.585) | fits |
| backlog-adp@blank-aged1-6 | 769 | 0 | 155,679 (1.557) | fits |
| backlog-adp@blank-aged1-7 | 780 | 0 | 157,142 (1.571) | fits |
| backlog-adp@program-aged2-0 | 876 | 0 | 155,707 (1.557) | fits |
| backlog-adp@program-aged2-1 | 889 | 0 | 155,707 (1.557) | fits |
| backlog-adp@program-aged2-2 | 897 | 0 | 149,681 (1.497) | fits |
| backlog-adp@program-aged2-3 | 906 | 0 | 155,918 (1.559) | fits |
| backlog-adp@program-aged2-4 | 917 | 0 | 146,477 (1.465) | fits |
| backlog-adp@program-aged2-5 | 926 | 0 | 156,387 (1.564) | fits |
| backlog-adp@program-aged2-6 | 936 | 0 | 156,438 (1.564) | fits |
| backlog-adp@program-aged2-7 | 949 | 0 | 149,604 (1.496) | fits |
| backlog-adp@program-aged1-0 | 797 | 0 | 151,142 (1.511) | fits |
| backlog-adp@program-aged1-1 | 808 | 0 | 150,777 (1.508) | fits |
| backlog-adp@program-aged1-2 | 820 | 0 | 149,277 (1.493) | fits |
| backlog-adp@program-aged1-3 | 828 | 0 | 157,227 (1.572) | fits |
| backlog-adp@program-aged1-4 | 838 | 0 | 155,409 (1.554) | fits |
| backlog-adp@program-aged1-5 | 847 | 0 | 157,502 (1.575) | fits |
| backlog-adp@program-aged1-6 | 857 | 0 | 158,055 (1.581) | fits |
| backlog-adp@program-aged1-7 | 867 | 0 | 155,409 (1.554) | fits |
| backlog-adp@verify-aged2-0 | 967 | 0 | 156,469 (1.565) | fits |
| backlog-adp@verify-aged2-1 | 977 | 0 | 156,579 (1.566) | fits |
| backlog-adp@verify-aged2-2 | 987 | 0 | 156,614 (1.566) | fits |
| backlog-adp@verify-aged2-3 | 996 | 0 | 157,368 (1.574) | fits |
| backlog-adp@verify-aged2-4 | 1006 | 0 | 151,152 (1.512) | fits |
| backlog-adp@verify-aged2-5 | 1015 | 0 | 151,977 (1.520) | fits |
| backlog-adp@verify-aged2-6 | 1027 | 0 | 149,330 (1.493) | fits |
| backlog-adp@verify-aged2-7 | 1036 | 0 | 148,695 (1.487) | fits |
| backlog-adp@verify-aged1-0 | 886 | 0 | 149,069 (1.491) | fits |
| backlog-adp@verify-aged1-1 | 899 | 0 | 149,110 (1.491) | fits |
| backlog-adp@verify-aged1-2 | 907 | 0 | 155,735 (1.557) | fits |
| backlog-adp@verify-aged1-3 | 916 | 0 | 155,735 (1.557) | fits |
| backlog-adp@verify-aged1-4 | 926 | 0 | 155,735 (1.557) | fits |
| backlog-adp@verify-aged1-5 | 936 | 0 | 157,994 (1.580) | fits |
| backlog-adp@verify-aged1-6 | 946 | 0 | 157,550 (1.575) | fits |
| backlog-adp@verify-aged1-7 | 958 | 0 | 155,885 (1.559) | fits |
| adp-advertise | 592 | 0 | 51,897 (0.519) | fits |
| save-held | 1212 | 0 | 152,914 (1.529) | fits |
| save-starved | 32747 | 0 | 152,914 (1.529) | fits |
| acmp-noresp | 2019 | 0 | 51,897 (0.519) | fits |
| save | 603 | 0 | 51,897 (0.519) | fits |
| srp | 285 | 0 | 73,050 (0.731) | fits |
| backlog | 283 | 0 | 150,565 (1.506) | fits |
| backlog-adp | 307 | 0 | 156,603 (1.566) | fits |
| backlog-adp-refill | 322 | 0 | 151,313 (1.513) | fits |
| backlog-owed | 303 | 0 | 161,050 (1.611) | fits |
| acmp-disc | 933 | 0 | 51,897 (0.519) | fits |
| maap | 176 | 0 | 51,897 (0.519) | fits |
| adp-link | 88 | 0 | 51,897 (0.519) | fits |
| adp-gm | 87 | 0 | 51,897 (0.519) | fits |
| adp-discover | 87 | 0 | 51,897 (0.519) | fits |
| control | 87 | 0 | 51,897 (0.519) | fits |
| aecp-fanout | 110 | 0 | 55,082 (0.551) | fits |
| acmp-cmd | 83 | 0 | 51,897 (0.519) | fits |
| aecp | 109 | 0 | 51,897 (0.519) | fits |
| fixture | 149 | 0 | 72,325 (0.723) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 7.709 (20) | 12.291 |
| backlog-adp@blank-aged2-1 | 2 | none | none | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 7.774 (20) | 12.226 |
| backlog-adp@blank-aged2-2 | 2 | none | +7.927 ms, 76,458 (0.765 ms), read-back | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 7.755 (20) | 12.245 |
| backlog-adp@blank-aged2-3 | 2 | none | none | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 7.689 (20) | 12.311 |
| backlog-adp@blank-aged2-4 | 2 | +6.235 ms, 76,611 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 8.470 (20) | 11.530 |
| backlog-adp@blank-aged2-5 | 2 | none | none | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 8.509 (20) | 11.491 |
| backlog-adp@blank-aged2-6 | 2 | none | none | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 8.498 (20) | 11.502 |
| backlog-adp@blank-aged2-7 | 2 | +4.450 ms, 76,723 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 8.466 (20) | 11.534 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 7.697 (20) | 12.303 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 7.701 (20) | 12.299 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 7.663 (20) | 12.337 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 7.815 (20) | 12.185 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 8.319 (20) | 11.681 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 8.249 (20) | 11.751 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 8.365 (20) | 11.635 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 8.527 (20) | 11.473 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 7.674 (20) | 12.326 |
| backlog-adp@program-aged2-1 | 2 | none | none | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 7.674 (20) | 12.326 |
| backlog-adp@program-aged2-2 | 2 | none | +7.841 ms, 79,942 (0.799 ms), issue | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 7.555 (20) | 12.445 |
| backlog-adp@program-aged2-3 | 2 | none | +7.801 ms, 80,291 (0.803 ms), issue | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 7.790 (20) | 12.210 |
| backlog-adp@program-aged2-4 | 2 | +6.259 ms, 80,397 (0.804 ms), issue | none | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 8.745 (20) | 11.255 |
| backlog-adp@program-aged2-5 | 2 | +4.888 ms, 80,072 (0.801 ms), issue | none | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 8.584 (20) | 11.416 |
| backlog-adp@program-aged2-6 | 2 | +4.110 ms, 80,078 (0.801 ms), issue | none | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 8.599 (20) | 11.401 |
| backlog-adp@program-aged2-7 | 2 | +3.072 ms, 80,436 (0.804 ms), issue | none | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 8.738 (20) | 11.262 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 7.746 (20) | 12.254 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 7.752 (20) | 12.248 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 7.736 (20) | 12.264 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 7.721 (20) | 12.279 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 7.744 (20) | 12.256 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 7.815 (20) | 12.185 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 7.851 (20) | 12.149 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 7.838 (20) | 12.162 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 7.603 (20) | 12.397 |
| backlog-adp@verify-aged2-1 | 2 | none | none | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 7.740 (20) | 12.260 |
| backlog-adp@verify-aged2-2 | 2 | none | +7.914 ms, 77,172 (0.772 ms), read-back | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 7.745 (20) | 12.255 |
| backlog-adp@verify-aged2-3 | 2 | none | +7.896 ms, 77,558 (0.776 ms), read-back | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 7.884 (20) | 12.116 |
| backlog-adp@verify-aged2-4 | 2 | +6.423 ms, 77,818 (0.778 ms), read-back | none | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 8.670 (20) | 11.330 |
| backlog-adp@verify-aged2-5 | 2 | +5.836 ms, 77,583 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 8.468 (20) | 11.532 |
| backlog-adp@verify-aged2-6 | 2 | +4.253 ms, 77,437 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 8.398 (20) | 11.602 |
| backlog-adp@verify-aged2-7 | 2 | +4.363 ms, 77,572 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 8.694 (20) | 11.306 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 7.679 (20) | 12.321 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 7.685 (20) | 12.315 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 7.555 (20) | 12.445 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 7.754 (20) | 12.246 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 7.799 (20) | 12.201 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 7.761 (20) | 12.239 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 7.769 (20) | 12.231 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 7.782 (20) | 12.218 |

Least margin over the aged windows: 11.255 ms, `backlog-adp@program-aged2-4.service.aecp.last.if0` at 8.745 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6029.890 | 6,070 | 102 | 2 | 30.858 | yes | within |
| save-held | 2018.171 | 4,070 | 102 | - | 12.622 | no | within |
| save-starved | 4047.994 | 4,070 | 102 | - | 31.251 | yes | within |
| save | 2018.473 | 4,070 | 102 | - | 10.788 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 92,252 (0.923) | 78,355 (0.784) |
| save-second | 520 | 80,047 (0.800) | 78,154 (0.782) |
| backlog-adp@blank-0 | 298 | 87,556 (0.876) | 75,973 (0.760) |
| backlog-adp@blank-1 | 298 | 87,556 (0.876) | 75,973 (0.760) |
| backlog-adp@blank-2 | 299 | 88,147 (0.881) | 76,270 (0.763) |
| backlog-adp@blank-3 | 299 | 89,039 (0.890) | 76,442 (0.764) |
| backlog-adp@blank-4 | 299 | 88,761 (0.888) | 76,451 (0.765) |
| backlog-adp@blank-5 | 299 | 88,958 (0.890) | 76,544 (0.765) |
| backlog-adp@blank-6 | 299 | 88,958 (0.890) | 76,544 (0.765) |
| backlog-adp@blank-7 | 299 | 88,173 (0.882) | 76,402 (0.764) |
| backlog-adp@program-0 | 327 | 91,781 (0.918) | 78,387 (0.784) |
| backlog-adp@program-1 | 328 | 93,049 (0.930) | 79,203 (0.792) |
| backlog-adp@program-2 | 328 | 92,817 (0.928) | 79,255 (0.793) |
| backlog-adp@program-3 | 328 | 92,400 (0.924) | 79,236 (0.792) |
| backlog-adp@program-4 | 328 | 91,781 (0.918) | 78,387 (0.784) |
| backlog-adp@program-5 | 329 | 91,781 (0.918) | 78,387 (0.784) |
| backlog-adp@program-6 | 329 | 91,781 (0.918) | 78,387 (0.784) |
| backlog-adp@program-7 | 329 | 91,781 (0.918) | 78,387 (0.784) |
| backlog-adp@verify-0 | 354 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-1 | 354 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-2 | 355 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-3 | 355 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-4 | 355 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-5 | 355 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-6 | 355 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-7 | 355 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@blank-aged2-0 | 297 | 88,900 (0.889) | 76,513 (0.765) |
| backlog-adp@blank-aged2-1 | 298 | 88,787 (0.888) | 76,420 (0.764) |
| backlog-adp@blank-aged2-2 | 297 | 76,458 (0.765) | 75,854 (0.759) |
| backlog-adp@blank-aged2-3 | 297 | 84,332 (0.843) | 76,395 (0.764) |
| backlog-adp@blank-aged2-4 | 297 | 76,611 (0.766) | 75,925 (0.759) |
| backlog-adp@blank-aged2-5 | 297 | 85,100 (0.851) | 76,325 (0.763) |
| backlog-adp@blank-aged2-6 | 297 | 84,995 (0.850) | 76,391 (0.764) |
| backlog-adp@blank-aged2-7 | 297 | 76,723 (0.767) | 75,991 (0.760) |
| backlog-adp@blank-aged1-0 | 297 | 88,753 (0.888) | 76,469 (0.765) |
| backlog-adp@blank-aged1-1 | 298 | 92,296 (0.923) | 76,513 (0.765) |
| backlog-adp@blank-aged1-2 | 297 | 92,855 (0.929) | 76,467 (0.765) |
| backlog-adp@blank-aged1-3 | 297 | 92,741 (0.927) | 76,467 (0.765) |
| backlog-adp@blank-aged1-4 | 297 | 88,950 (0.889) | 76,513 (0.765) |
| backlog-adp@blank-aged1-5 | 297 | 88,081 (0.881) | 76,310 (0.763) |
| backlog-adp@blank-aged1-6 | 297 | 88,556 (0.886) | 76,376 (0.764) |
| backlog-adp@blank-aged1-7 | 297 | 88,859 (0.889) | 76,566 (0.766) |
| backlog-adp@program-aged2-0 | 326 | 92,272 (0.923) | 79,227 (0.792) |
| backlog-adp@program-aged2-1 | 327 | 92,272 (0.923) | 79,227 (0.792) |
| backlog-adp@program-aged2-2 | 326 | 91,781 (0.918) | 78,624 (0.786) |
| backlog-adp@program-aged2-3 | 326 | 91,781 (0.918) | 78,729 (0.787) |
| backlog-adp@program-aged2-4 | 326 | 91,781 (0.918) | 78,737 (0.787) |
| backlog-adp@program-aged2-5 | 326 | 91,781 (0.918) | 78,513 (0.785) |
| backlog-adp@program-aged2-6 | 326 | 91,781 (0.918) | 78,513 (0.785) |
| backlog-adp@program-aged2-7 | 326 | 91,781 (0.918) | 78,776 (0.788) |
| backlog-adp@program-aged1-0 | 326 | 92,230 (0.922) | 79,255 (0.793) |
| backlog-adp@program-aged1-1 | 327 | 92,230 (0.922) | 79,255 (0.793) |
| backlog-adp@program-aged1-2 | 326 | 91,781 (0.918) | 79,154 (0.792) |
| backlog-adp@program-aged1-3 | 326 | 91,781 (0.918) | 79,112 (0.791) |
| backlog-adp@program-aged1-4 | 326 | 91,781 (0.918) | 79,121 (0.791) |
| backlog-adp@program-aged1-5 | 326 | 92,069 (0.921) | 79,211 (0.792) |
| backlog-adp@program-aged1-6 | 326 | 92,207 (0.922) | 79,255 (0.793) |
| backlog-adp@program-aged1-7 | 326 | 92,257 (0.923) | 79,227 (0.792) |
| backlog-adp@verify-aged2-0 | 355 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-aged2-1 | 356 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-aged2-2 | 355 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-aged2-3 | 355 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-aged2-4 | 355 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-aged2-5 | 355 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-aged2-6 | 355 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-aged2-7 | 355 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-aged1-0 | 355 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-aged1-1 | 356 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-aged1-2 | 355 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-aged1-3 | 355 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-aged1-4 | 355 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-aged1-5 | 355 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-aged1-6 | 355 | 92,974 (0.930) | 78,387 (0.784) |
| backlog-adp@verify-aged1-7 | 355 | 92,974 (0.930) | 78,387 (0.784) |
| adp-advertise | 578 | 17,958 (0.180) | 3,231 (0.032) |
| save-held | 722 | 91,760 (0.918) | 78,866 (0.789) |
| save-starved | 418 | 80,663 (0.807) | 78,644 (0.786) |
| acmp-noresp | 615 | 91,859 (0.919) | 78,355 (0.784) |
| save | 585 | 90,977 (0.910) | 78,403 (0.784) |
| srp | 271 | 17,958 (0.180) | 3,231 (0.032) |
| backlog | 265 | 17,958 (0.180) | 3,231 (0.032) |
| backlog-adp | 271 | 17,958 (0.180) | 3,242 (0.032) |
| backlog-adp-refill | 274 | 17,958 (0.180) | 3,242 (0.032) |
| backlog-owed | 276 | 17,958 (0.180) | 3,336 (0.033) |
| acmp-disc | 305 | 91,811 (0.918) | 78,355 (0.784) |
| maap | 166 | 17,958 (0.180) | 3,231 (0.032) |
| adp-link | 80 | 17,958 (0.180) | 3,231 (0.032) |
| adp-gm | 80 | 17,958 (0.180) | 3,231 (0.032) |
| adp-discover | 80 | 17,958 (0.180) | 3,231 (0.032) |
| control | 80 | 17,958 (0.180) | 3,231 (0.032) |
| aecp-fanout | 79 | 17,958 (0.180) | 3,231 (0.032) |
| acmp-cmd | 65 | 17,958 (0.180) | 3,231 (0.032) |
| aecp | 79 | 17,958 (0.180) | 3,231 (0.032) |
| fixture | 54 | 15,064 (0.151) | 3,231 (0.032) |

Longest pass that carries a step: 93,049 CPU cycles (0.930 ms), backlog-adp@program-1; longest step: 79,255 (0.793 ms), backlog-adp@program-2.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 6,793 | 0.068 | 20 | 20 | fits | 27,556 | 19 (14) | 0.894 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 610,822 | 6.108 | 20 | 20 | fits | 154,300 | 174 | 0.553 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 218,296 | 2.183 | 20 | 200 | fits | 145,941 | 227 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 694,982 | 6.950 | 20 | 200 | fits | 154,300 | 174 | 0.553 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 219,208 | 2.192 | 20 | 20 | fits | 145,941 | 227 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 830,312 | 8.303 | 20 | 20 | fits | 134,634 | 112 | 0.506 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 222,793 | 2.228 | 20 | 24 | fits | 145,941 | 227 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 833,747 | 8.337 | 20 | 24 | fits | 134,634 | 112 | 0.506 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 221,753 | 2.218 | 20 | 50 | fits | 145,941 | 227 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 698,658 | 6.987 | 20 | 50 | fits | 154,300 | 174 | 0.553 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 355,590 | 3.556 | 20 | 20 | fits | 134,292 | 94 | 0.604 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 542,278 | 5.423 | 20 | 20 | fits | 78,409 | 36 | 0.519 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 573,864 | 5.739 | 20 | 20 | fits | 150,701 | 156 | 0.563 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 148,260 | 1.483 | 20 | 200 | fits | 149,377 | 245 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 621,753 | 6.218 | 20 | 200 | fits | 150,701 | 156 | 0.563 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 149,172 | 1.492 | 20 | 20 | fits | 149,377 | 245 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 756,398 | 7.564 | 20 | 20 | fits | 133,949 | 112 | 0.500 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 152,757 | 1.528 | 20 | 24 | fits | 149,377 | 245 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 759,833 | 7.598 | 20 | 24 | fits | 133,949 | 112 | 0.500 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 151,717 | 1.517 | 20 | 50 | fits | 149,377 | 245 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 625,429 | 6.254 | 20 | 50 | fits | 150,701 | 156 | 0.563 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 285,895 | 2.859 | 20 | 20 | fits | 134,633 | 94 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 472,648 | 4.726 | 20 | 20 | fits | 78,412 | 36 | 0.519 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 576,304 | 5.763 | 20 | 20 | fits | 150,990 | 157 | 0.564 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 150,410 | 1.504 | 20 | 200 | fits | 149,377 | 245 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 624,192 | 6.242 | 20 | 200 | fits | 150,990 | 157 | 0.564 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 151,322 | 1.513 | 20 | 20 | fits | 149,377 | 245 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 771,797 | 7.718 | 20 | 20 | fits | 137,814 | 118 | 0.521 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 154,907 | 1.549 | 20 | 24 | fits | 149,377 | 245 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 775,232 | 7.752 | 20 | 24 | fits | 137,814 | 118 | 0.521 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 153,867 | 1.539 | 20 | 50 | fits | 149,377 | 245 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 627,868 | 6.279 | 20 | 50 | fits | 150,990 | 157 | 0.564 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 288,045 | 2.880 | 20 | 20 | fits | 134,633 | 94 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 474,798 | 4.748 | 20 | 20 | fits | 78,412 | 36 | 0.519 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 593,053 | 5.931 | 20 | 20 | fits | 151,333 | 156 | 0.566 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 152,560 | 1.526 | 20 | 200 | fits | 149,377 | 245 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 640,954 | 6.410 | 20 | 200 | fits | 151,333 | 156 | 0.566 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 153,472 | 1.535 | 20 | 20 | fits | 149,377 | 245 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 784,955 | 7.850 | 20 | 20 | fits | 143,305 | 115 | 0.530 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 157,057 | 1.571 | 20 | 24 | fits | 149,377 | 245 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 788,390 | 7.884 | 20 | 24 | fits | 143,305 | 115 | 0.530 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 156,017 | 1.560 | 20 | 50 | fits | 149,377 | 245 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 644,630 | 6.446 | 20 | 50 | fits | 151,333 | 156 | 0.566 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 290,195 | 2.902 | 20 | 20 | fits | 134,633 | 94 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 491,217 | 4.912 | 20 | 20 | fits | 83,343 | 43 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 606,238 | 6.062 | 20 | 20 | fits | 154,184 | 153 | 0.588 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 154,710 | 1.547 | 20 | 200 | fits | 149,377 | 245 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 646,120 | 6.461 | 20 | 200 | fits | 154,184 | 153 | 0.588 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 155,622 | 1.556 | 20 | 20 | fits | 149,377 | 245 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 789,218 | 7.892 | 20 | 20 | fits | 142,402 | 114 | 0.517 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 159,207 | 1.592 | 20 | 24 | fits | 149,377 | 245 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 792,653 | 7.927 | 20 | 24 | fits | 142,402 | 114 | 0.517 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 158,167 | 1.582 | 20 | 50 | fits | 149,377 | 245 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 649,796 | 6.498 | 20 | 50 | fits | 154,184 | 153 | 0.588 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 292,464 | 2.925 | 20 | 20 | fits | 134,752 | 95 | 0.606 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 493,532 | 4.935 | 20 | 20 | fits | 78,712 | 36 | 0.526 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 262,281 | 2.623 | 20 | 20 | fits | 152,253 | 215 | 0.539 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 150,705 | 1.507 | 20 | 200 | fits | 155,937 | 233 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 310,677 | 3.107 | 20 | 200 | fits | 152,253 | 215 | 0.539 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 151,617 | 1.516 | 20 | 20 | fits | 155,937 | 233 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 770,406 | 7.704 | 20 | 20 | fits | 137,383 | 111 | 0.526 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 155,202 | 1.552 | 20 | 24 | fits | 155,937 | 233 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 773,841 | 7.738 | 20 | 24 | fits | 137,383 | 111 | 0.526 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 154,162 | 1.542 | 20 | 50 | fits | 155,937 | 233 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 314,353 | 3.144 | 20 | 50 | fits | 152,253 | 215 | 0.539 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 440,671 | 4.407 | 20 | 20 | fits | 126,383 | 52 | 0.640 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 633,923 | 6.339 | 20 | 20 | fits | 78,458 | 36 | 0.521 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 264,339 | 2.643 | 20 | 20 | fits | 152,206 | 215 | 0.539 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 152,810 | 1.528 | 20 | 200 | fits | 155,892 | 233 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 312,735 | 3.127 | 20 | 200 | fits | 152,206 | 215 | 0.539 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 153,722 | 1.537 | 20 | 20 | fits | 155,892 | 233 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 771,361 | 7.714 | 20 | 20 | fits | 137,415 | 111 | 0.526 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 157,307 | 1.573 | 20 | 24 | fits | 155,892 | 233 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 774,796 | 7.748 | 20 | 24 | fits | 137,415 | 111 | 0.526 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 156,267 | 1.563 | 20 | 50 | fits | 155,892 | 233 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 316,411 | 3.164 | 20 | 50 | fits | 152,206 | 215 | 0.539 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 448,354 | 4.484 | 20 | 20 | fits | 132,008 | 58 | 0.656 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 634,846 | 6.348 | 20 | 20 | fits | 78,412 | 36 | 0.519 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 271,804 | 2.718 | 20 | 20 | fits | 149,817 | 206 | 0.559 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 160,947 | 1.609 | 20 | 200 | fits | 155,772 | 232 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 310,155 | 3.102 | 20 | 200 | fits | 149,817 | 206 | 0.559 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 161,859 | 1.619 | 20 | 20 | fits | 155,772 | 232 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 769,918 | 7.699 | 20 | 20 | fits | 144,277 | 111 | 0.539 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 165,444 | 1.654 | 20 | 24 | fits | 155,772 | 232 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 773,353 | 7.734 | 20 | 24 | fits | 144,277 | 111 | 0.539 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 164,404 | 1.644 | 20 | 50 | fits | 155,772 | 232 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 313,831 | 3.138 | 20 | 50 | fits | 149,817 | 206 | 0.559 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 439,960 | 4.400 | 20 | 20 | fits | 126,194 | 52 | 0.638 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 626,541 | 6.265 | 20 | 20 | fits | 78,353 | 36 | 0.517 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 602,494 | 6.025 | 20 | 20 | fits | 148,288 | 173 | 0.566 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 157,810 | 1.578 | 20 | 200 | fits | 155,962 | 232 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 629,022 | 6.290 | 20 | 200 | fits | 148,288 | 173 | 0.566 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 158,722 | 1.587 | 20 | 20 | fits | 155,962 | 232 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 775,316 | 7.753 | 20 | 20 | fits | 136,289 | 112 | 0.519 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 162,307 | 1.623 | 20 | 24 | fits | 155,962 | 232 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 778,751 | 7.788 | 20 | 24 | fits | 136,289 | 112 | 0.519 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 161,267 | 1.613 | 20 | 50 | fits | 155,962 | 232 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 632,698 | 6.327 | 20 | 50 | fits | 148,288 | 173 | 0.566 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 295,467 | 2.955 | 20 | 20 | fits | 134,655 | 94 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 482,330 | 4.823 | 20 | 20 | fits | 78,588 | 36 | 0.523 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 249,603 | 2.496 | 20 | 20 | fits | 148,631 | 195 | 0.528 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 141,605 | 1.416 | 20 | 200 | fits | 148,172 | 202 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 289,627 | 2.896 | 20 | 200 | fits | 148,631 | 195 | 0.528 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 142,517 | 1.425 | 20 | 20 | fits | 148,172 | 202 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 446,468 | 4.465 | 20 | 20 | fits | 148,047 | 154 | 0.541 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 146,102 | 1.461 | 20 | 24 | fits | 148,172 | 202 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 449,903 | 4.499 | 20 | 24 | fits | 148,047 | 154 | 0.541 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 145,062 | 1.451 | 20 | 50 | fits | 148,172 | 202 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 293,303 | 2.933 | 20 | 50 | fits | 148,631 | 195 | 0.528 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 575,083 | 5.751 | 20 | 20 | fits | 125,700 | 52 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 768,192 | 7.682 | 20 | 20 | fits | 84,846 | 42 | 0.585 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 579,138 | 5.791 | 20 | 20 | fits | 156,516 | 176 | 0.554 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 155,667 | 1.557 | 20 | 200 | fits | 151,990 | 230 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 641,191 | 6.412 | 20 | 200 | fits | 156,516 | 176 | 0.554 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 156,579 | 1.566 | 20 | 20 | fits | 151,990 | 230 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 767,341 | 7.673 | 20 | 20 | fits | 125,454 | 105 | 0.488 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 160,164 | 1.602 | 20 | 24 | fits | 151,990 | 230 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 770,776 | 7.708 | 20 | 24 | fits | 125,454 | 105 | 0.488 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 159,124 | 1.591 | 20 | 50 | fits | 151,990 | 230 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 644,867 | 6.449 | 20 | 50 | fits | 156,516 | 176 | 0.554 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 293,136 | 2.931 | 20 | 20 | fits | 134,467 | 94 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 486,271 | 4.863 | 20 | 20 | fits | 84,856 | 42 | 0.585 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 249,356 | 2.494 | 20 | 20 | fits | 148,369 | 201 | 0.564 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 141,540 | 1.415 | 20 | 200 | fits | 146,099 | 227 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 289,300 | 2.893 | 20 | 200 | fits | 148,369 | 201 | 0.564 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 142,452 | 1.425 | 20 | 20 | fits | 146,099 | 227 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 761,853 | 7.619 | 20 | 20 | fits | 148,129 | 118 | 0.548 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 146,037 | 1.460 | 20 | 24 | fits | 146,099 | 227 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 791,987 | 7.920 | 20 | 24 | fits | 26,699 | 18 | 0.733 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 144,997 | 1.450 | 20 | 50 | fits | 146,099 | 227 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 292,976 | 2.930 | 20 | 50 | fits | 148,369 | 201 | 0.564 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 418,811 | 4.188 | 20 | 20 | fits | 125,900 | 52 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 605,339 | 6.053 | 20 | 20 | fits | 78,466 | 37 | 0.516 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 560,187 | 5.602 | 20 | 20 | fits | 155,943 | 174 | 0.561 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 150,710 | 1.507 | 20 | 200 | fits | 146,177 | 227 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 644,795 | 6.448 | 20 | 200 | fits | 155,943 | 174 | 0.561 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 151,622 | 1.516 | 20 | 20 | fits | 146,177 | 227 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 779,965 | 7.800 | 20 | 20 | fits | 134,474 | 111 | 0.505 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 155,207 | 1.552 | 20 | 24 | fits | 146,177 | 227 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 783,400 | 7.834 | 20 | 24 | fits | 134,474 | 111 | 0.505 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 154,167 | 1.542 | 20 | 50 | fits | 146,177 | 227 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 648,471 | 6.485 | 20 | 50 | fits | 155,943 | 174 | 0.561 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 288,047 | 2.880 | 20 | 20 | fits | 134,335 | 94 | 0.605 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 490,448 | 4.904 | 20 | 20 | fits | 80,684 | 37 | 0.590 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 251,772 | 2.518 | 20 | 20 | fits | 147,099 | 193 | 0.550 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 145,837 | 1.458 | 20 | 200 | fits | 149,598 | 246 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 300,891 | 3.009 | 20 | 200 | fits | 147,099 | 193 | 0.550 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 146,749 | 1.467 | 20 | 20 | fits | 149,598 | 246 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 764,809 | 7.648 | 20 | 20 | fits | 148,230 | 119 | 0.501 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 150,334 | 1.503 | 20 | 24 | fits | 149,598 | 246 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 768,244 | 7.682 | 20 | 24 | fits | 148,230 | 119 | 0.501 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 149,294 | 1.493 | 20 | 50 | fits | 149,598 | 246 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 304,567 | 3.046 | 20 | 50 | fits | 147,099 | 193 | 0.550 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 430,904 | 4.309 | 20 | 20 | fits | 126,402 | 52 | 0.641 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 617,479 | 6.175 | 20 | 20 | fits | 78,350 | 36 | 0.517 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 243,253 | 2.433 | 20 | 20 | fits | 150,505 | 215 | 0.528 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 141,920 | 1.419 | 20 | 200 | fits | 148,017 | 186 | 0.532 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 291,816 | 2.918 | 20 | 200 | fits | 150,505 | 215 | 0.528 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 142,832 | 1.428 | 20 | 20 | fits | 148,017 | 186 | 0.532 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 772,030 | 7.720 | 20 | 20 | fits | 140,050 | 118 | 0.535 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 146,417 | 1.464 | 20 | 24 | fits | 148,017 | 186 | 0.532 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 775,465 | 7.755 | 20 | 24 | fits | 140,050 | 118 | 0.535 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 145,377 | 1.454 | 20 | 50 | fits | 148,017 | 186 | 0.532 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 295,492 | 2.955 | 20 | 50 | fits | 150,505 | 215 | 0.528 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 430,550 | 4.306 | 20 | 20 | fits | 135,123 | 94 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 623,363 | 6.234 | 20 | 20 | fits | 78,505 | 37 | 0.518 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 264,823 | 2.648 | 20 | 20 | fits | 149,800 | 206 | 0.558 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 153,983 | 1.540 | 20 | 200 | fits | 155,780 | 232 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 303,174 | 3.032 | 20 | 200 | fits | 149,800 | 206 | 0.558 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 154,895 | 1.549 | 20 | 20 | fits | 155,780 | 232 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 778,489 | 7.785 | 20 | 20 | fits | 145,124 | 110 | 0.541 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 158,480 | 1.585 | 20 | 24 | fits | 155,780 | 232 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 781,924 | 7.819 | 20 | 24 | fits | 145,124 | 110 | 0.541 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 157,440 | 1.574 | 20 | 50 | fits | 155,780 | 232 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 306,850 | 3.068 | 20 | 50 | fits | 149,800 | 206 | 0.558 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 432,903 | 4.329 | 20 | 20 | fits | 126,118 | 53 | 0.636 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 634,265 | 6.343 | 20 | 20 | fits | 78,752 | 36 | 0.528 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 650,386 | 6.504 | 20 | 20 | fits | 156,731 | 175 | 0.559 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 210,522 | 2.105 | 20 | 200 | fits | 155,926 | 232 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 689,698 | 6.897 | 20 | 200 | fits | 156,731 | 175 | 0.559 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 211,434 | 2.114 | 20 | 20 | fits | 155,926 | 232 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 811,480 | 8.115 | 20 | 20 | fits | 121,086 | 100 | 0.522 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 215,019 | 2.150 | 20 | 24 | fits | 155,926 | 232 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 814,915 | 8.149 | 20 | 24 | fits | 121,086 | 100 | 0.522 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 213,979 | 2.140 | 20 | 50 | fits | 155,926 | 232 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 693,374 | 6.934 | 20 | 50 | fits | 156,731 | 175 | 0.559 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 347,976 | 3.480 | 20 | 20 | fits | 134,452 | 94 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 534,563 | 5.346 | 20 | 20 | fits | 78,412 | 36 | 0.519 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 243,143 | 2.431 | 20 | 20 | fits | 150,480 | 215 | 0.528 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 141,835 | 1.418 | 20 | 200 | fits | 148,195 | 186 | 0.533 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 291,706 | 2.917 | 20 | 200 | fits | 150,480 | 215 | 0.528 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 142,747 | 1.427 | 20 | 20 | fits | 148,195 | 186 | 0.533 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 753,455 | 7.535 | 20 | 20 | fits | 137,384 | 112 | 0.525 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 146,332 | 1.463 | 20 | 24 | fits | 148,195 | 186 | 0.533 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 756,890 | 7.569 | 20 | 24 | fits | 137,384 | 112 | 0.525 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 145,292 | 1.453 | 20 | 50 | fits | 148,195 | 186 | 0.533 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 295,382 | 2.954 | 20 | 50 | fits | 150,480 | 215 | 0.528 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 430,470 | 4.305 | 20 | 20 | fits | 135,153 | 94 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 616,971 | 6.170 | 20 | 20 | fits | 78,412 | 36 | 0.519 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 592,523 | 5.925 | 20 | 20 | fits | 157,311 | 176 | 0.561 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 151,748 | 1.517 | 20 | 200 | fits | 155,958 | 232 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 631,799 | 6.318 | 20 | 200 | fits | 157,311 | 176 | 0.561 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 152,660 | 1.527 | 20 | 20 | fits | 155,958 | 232 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 765,717 | 7.657 | 20 | 20 | fits | 124,830 | 106 | 0.544 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 156,245 | 1.562 | 20 | 24 | fits | 155,958 | 232 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 769,152 | 7.692 | 20 | 24 | fits | 124,830 | 106 | 0.544 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 155,205 | 1.552 | 20 | 50 | fits | 155,958 | 232 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 635,475 | 6.355 | 20 | 50 | fits | 157,311 | 176 | 0.561 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 289,497 | 2.895 | 20 | 20 | fits | 134,747 | 94 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 476,084 | 4.761 | 20 | 20 | fits | 78,412 | 36 | 0.519 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 609,823 | 6.098 | 20 | 20 | fits | 157,992 | 175 | 0.565 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 153,898 | 1.539 | 20 | 200 | fits | 155,958 | 232 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 649,112 | 6.491 | 20 | 200 | fits | 157,992 | 175 | 0.565 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 154,810 | 1.548 | 20 | 20 | fits | 155,958 | 232 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 781,199 | 7.812 | 20 | 20 | fits | 131,391 | 107 | 0.550 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 158,395 | 1.584 | 20 | 24 | fits | 155,958 | 232 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 784,634 | 7.846 | 20 | 24 | fits | 131,391 | 107 | 0.550 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 157,355 | 1.574 | 20 | 50 | fits | 155,958 | 232 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 652,788 | 6.528 | 20 | 50 | fits | 157,992 | 175 | 0.565 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 291,647 | 2.916 | 20 | 20 | fits | 134,747 | 94 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 492,716 | 4.927 | 20 | 20 | fits | 83,556 | 43 | 0.607 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 623,165 | 6.232 | 20 | 20 | fits | 147,196 | 165 | 0.595 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 156,048 | 1.560 | 20 | 200 | fits | 155,958 | 232 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 640,877 | 6.409 | 20 | 200 | fits | 147,196 | 165 | 0.595 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 156,960 | 1.570 | 20 | 20 | fits | 155,958 | 232 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 785,107 | 7.851 | 20 | 20 | fits | 143,534 | 113 | 0.519 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 160,545 | 1.605 | 20 | 24 | fits | 155,958 | 232 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 788,542 | 7.885 | 20 | 24 | fits | 143,534 | 113 | 0.519 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 159,505 | 1.595 | 20 | 50 | fits | 155,958 | 232 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 644,553 | 6.446 | 20 | 50 | fits | 147,196 | 165 | 0.595 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 293,916 | 2.939 | 20 | 20 | fits | 134,866 | 95 | 0.609 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 495,277 | 4.953 | 20 | 20 | fits | 78,792 | 36 | 0.528 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 269,968 | 2.700 | 20 | 20 | fits | 152,210 | 215 | 0.539 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 158,287 | 1.583 | 20 | 200 | fits | 156,047 | 233 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 318,364 | 3.184 | 20 | 200 | fits | 152,210 | 215 | 0.539 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 159,199 | 1.592 | 20 | 20 | fits | 156,047 | 233 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 776,989 | 7.770 | 20 | 20 | fits | 137,415 | 111 | 0.526 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 162,784 | 1.628 | 20 | 24 | fits | 156,047 | 233 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 780,424 | 7.804 | 20 | 24 | fits | 137,415 | 111 | 0.526 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 161,744 | 1.617 | 20 | 50 | fits | 156,047 | 233 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 322,040 | 3.220 | 20 | 50 | fits | 152,210 | 215 | 0.539 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 453,816 | 4.538 | 20 | 20 | fits | 131,841 | 58 | 0.654 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 640,474 | 6.405 | 20 | 20 | fits | 78,412 | 36 | 0.519 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 251,792 | 2.518 | 20 | 20 | fits | 150,328 | 215 | 0.527 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 150,570 | 1.506 | 20 | 200 | fits | 156,619 | 232 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 300,289 | 3.003 | 20 | 200 | fits | 150,328 | 215 | 0.527 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 151,482 | 1.515 | 20 | 20 | fits | 156,619 | 232 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 758,771 | 7.588 | 20 | 20 | fits | 137,421 | 111 | 0.526 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 155,067 | 1.551 | 20 | 24 | fits | 156,619 | 232 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 762,206 | 7.622 | 20 | 24 | fits | 137,421 | 111 | 0.526 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 154,027 | 1.540 | 20 | 50 | fits | 156,619 | 232 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 303,965 | 3.040 | 20 | 50 | fits | 150,328 | 215 | 0.527 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 435,758 | 4.358 | 20 | 20 | fits | 131,858 | 58 | 0.654 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 622,250 | 6.223 | 20 | 20 | fits | 78,412 | 36 | 0.519 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 276,445 | 2.764 | 20 | 20 | fits | 149,774 | 206 | 0.557 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 152,171 | 1.522 | 20 | 200 | fits | 152,335 | 230 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 301,336 | 3.013 | 20 | 200 | fits | 149,774 | 206 | 0.557 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 153,083 | 1.531 | 20 | 20 | fits | 152,335 | 230 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 765,355 | 7.654 | 20 | 20 | fits | 148,350 | 118 | 0.504 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 156,668 | 1.567 | 20 | 24 | fits | 152,335 | 230 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 768,790 | 7.688 | 20 | 24 | fits | 148,350 | 118 | 0.504 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 155,628 | 1.556 | 20 | 50 | fits | 152,335 | 230 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 305,012 | 3.050 | 20 | 50 | fits | 149,774 | 206 | 0.557 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 431,461 | 4.315 | 20 | 20 | fits | 126,514 | 52 | 0.640 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 617,905 | 6.179 | 20 | 20 | fits | 78,350 | 36 | 0.517 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 261,545 | 2.615 | 20 | 20 | fits | 155,457 | 215 | 0.526 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 146,378 | 1.464 | 20 | 200 | fits | 153,166 | 228 | 0.528 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 301,226 | 3.012 | 20 | 200 | fits | 155,457 | 215 | 0.526 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 147,290 | 1.473 | 20 | 20 | fits | 153,166 | 228 | 0.528 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 767,485 | 7.675 | 20 | 20 | fits | 136,569 | 111 | 0.524 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 150,875 | 1.509 | 20 | 24 | fits | 153,166 | 228 | 0.528 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 770,920 | 7.709 | 20 | 24 | fits | 136,569 | 111 | 0.524 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 149,835 | 1.498 | 20 | 50 | fits | 153,166 | 228 | 0.528 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 304,902 | 3.049 | 20 | 50 | fits | 155,457 | 215 | 0.526 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 430,744 | 4.307 | 20 | 20 | fits | 125,907 | 53 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 631,816 | 6.318 | 20 | 20 | fits | 78,609 | 36 | 0.526 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 548,016 | 5.480 | 20 | 20 | fits | 156,113 | 173 | 0.567 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 146,922 | 1.469 | 20 | 200 | fits | 144,790 | 224 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 639,057 | 6.391 | 20 | 200 | fits | 156,113 | 173 | 0.567 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 147,834 | 1.478 | 20 | 20 | fits | 144,790 | 224 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 773,926 | 7.739 | 20 | 20 | fits | 134,173 | 111 | 0.505 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 151,419 | 1.514 | 20 | 24 | fits | 144,790 | 224 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 777,361 | 7.774 | 20 | 24 | fits | 134,173 | 111 | 0.505 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 150,379 | 1.504 | 20 | 50 | fits | 144,790 | 224 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 642,733 | 6.427 | 20 | 50 | fits | 156,113 | 173 | 0.567 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 283,753 | 2.838 | 20 | 20 | fits | 133,829 | 95 | 0.600 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 484,540 | 4.845 | 20 | 20 | fits | 78,480 | 36 | 0.523 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 257,748 | 2.577 | 20 | 20 | fits | 152,492 | 210 | 0.553 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 147,661 | 1.477 | 20 | 200 | fits | 144,949 | 225 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 308,644 | 3.086 | 20 | 200 | fits | 152,492 | 210 | 0.553 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 148,573 | 1.486 | 20 | 20 | fits | 144,949 | 225 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 772,051 | 7.721 | 20 | 20 | fits | 147,978 | 118 | 0.502 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 152,158 | 1.522 | 20 | 24 | fits | 144,949 | 225 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 775,486 | 7.755 | 20 | 24 | fits | 147,978 | 118 | 0.502 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 151,118 | 1.511 | 20 | 50 | fits | 144,949 | 225 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 312,320 | 3.123 | 20 | 50 | fits | 152,492 | 210 | 0.553 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 438,544 | 4.385 | 20 | 20 | fits | 126,289 | 52 | 0.641 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 624,973 | 6.250 | 20 | 20 | fits | 78,289 | 36 | 0.517 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 262,097 | 2.621 | 20 | 20 | fits | 152,030 | 217 | 0.525 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 136,658 | 1.367 | 20 | 200 | fits | 145,558 | 180 | 0.543 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 288,079 | 2.881 | 20 | 200 | fits | 152,030 | 217 | 0.525 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 137,570 | 1.376 | 20 | 20 | fits | 145,558 | 180 | 0.543 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 765,496 | 7.655 | 20 | 20 | fits | 153,541 | 122 | 0.551 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 141,155 | 1.412 | 20 | 24 | fits | 145,558 | 180 | 0.543 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 768,931 | 7.689 | 20 | 24 | fits | 153,541 | 122 | 0.551 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 140,115 | 1.401 | 20 | 50 | fits | 145,558 | 180 | 0.543 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 291,755 | 2.918 | 20 | 50 | fits | 152,030 | 217 | 0.525 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 426,477 | 4.265 | 20 | 20 | fits | 134,787 | 94 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 612,855 | 6.129 | 20 | 20 | fits | 78,345 | 36 | 0.519 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 262,938 | 2.629 | 20 | 20 | fits | 152,115 | 217 | 0.526 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 137,446 | 1.374 | 20 | 200 | fits | 145,506 | 180 | 0.543 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 288,952 | 2.890 | 20 | 200 | fits | 152,115 | 217 | 0.526 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 138,358 | 1.384 | 20 | 20 | fits | 145,506 | 180 | 0.543 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 843,609 | 8.436 | 20 | 20 | fits | 148,127 | 121 | 0.540 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 141,943 | 1.419 | 20 | 24 | fits | 145,506 | 180 | 0.543 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 847,044 | 8.470 | 20 | 24 | fits | 148,127 | 121 | 0.540 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 140,903 | 1.409 | 20 | 50 | fits | 145,506 | 180 | 0.543 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 292,628 | 2.926 | 20 | 50 | fits | 152,115 | 217 | 0.526 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 427,350 | 4.274 | 20 | 20 | fits | 134,787 | 94 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 619,771 | 6.198 | 20 | 20 | fits | 84,388 | 42 | 0.578 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 236,763 | 2.368 | 20 | 20 | fits | 157,232 | 202 | 0.535 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 141,089 | 1.411 | 20 | 200 | fits | 148,569 | 242 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 297,712 | 2.977 | 20 | 200 | fits | 157,232 | 202 | 0.535 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 142,001 | 1.420 | 20 | 20 | fits | 148,569 | 242 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 847,417 | 8.474 | 20 | 20 | fits | 137,176 | 111 | 0.526 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 145,586 | 1.456 | 20 | 24 | fits | 148,569 | 242 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 850,852 | 8.509 | 20 | 24 | fits | 137,176 | 111 | 0.526 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 144,546 | 1.445 | 20 | 50 | fits | 148,569 | 242 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 301,388 | 3.014 | 20 | 50 | fits | 157,232 | 202 | 0.535 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 427,598 | 4.276 | 20 | 20 | fits | 126,275 | 52 | 0.641 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 711,141 | 7.111 | 20 | 20 | fits | 83,804 | 43 | 0.612 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 237,343 | 2.373 | 20 | 20 | fits | 157,232 | 202 | 0.535 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 141,669 | 1.417 | 20 | 200 | fits | 148,569 | 242 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 298,292 | 2.983 | 20 | 200 | fits | 157,232 | 202 | 0.535 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 142,581 | 1.426 | 20 | 20 | fits | 148,569 | 242 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 846,388 | 8.464 | 20 | 20 | fits | 136,649 | 111 | 0.523 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 146,166 | 1.462 | 20 | 24 | fits | 148,569 | 242 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 849,823 | 8.498 | 20 | 24 | fits | 136,649 | 111 | 0.523 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 145,126 | 1.451 | 20 | 50 | fits | 148,569 | 242 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 301,968 | 3.020 | 20 | 50 | fits | 157,232 | 202 | 0.535 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 433,823 | 4.338 | 20 | 20 | fits | 131,920 | 59 | 0.656 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 710,639 | 7.106 | 20 | 20 | fits | 78,653 | 36 | 0.526 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 237,923 | 2.379 | 20 | 20 | fits | 157,333 | 203 | 0.535 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 142,249 | 1.422 | 20 | 200 | fits | 148,569 | 242 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 298,973 | 2.990 | 20 | 200 | fits | 157,333 | 203 | 0.535 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 143,161 | 1.432 | 20 | 20 | fits | 148,569 | 242 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 843,209 | 8.432 | 20 | 20 | fits | 136,895 | 111 | 0.524 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 146,746 | 1.467 | 20 | 24 | fits | 148,569 | 242 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 846,644 | 8.466 | 20 | 24 | fits | 136,895 | 111 | 0.524 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 145,706 | 1.457 | 20 | 50 | fits | 148,569 | 242 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 302,649 | 3.026 | 20 | 50 | fits | 157,333 | 203 | 0.535 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 443,318 | 4.433 | 20 | 20 | fits | 132,707 | 64 | 0.648 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 707,214 | 7.072 | 20 | 20 | fits | 78,451 | 36 | 0.521 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 259,421 | 2.594 | 20 | 20 | fits | 155,161 | 215 | 0.525 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 144,566 | 1.446 | 20 | 200 | fits | 151,235 | 227 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 299,118 | 2.991 | 20 | 200 | fits | 155,161 | 215 | 0.525 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 145,478 | 1.455 | 20 | 20 | fits | 151,235 | 227 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 766,310 | 7.663 | 20 | 20 | fits | 137,709 | 112 | 0.531 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 149,063 | 1.491 | 20 | 24 | fits | 151,235 | 227 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 769,745 | 7.697 | 20 | 24 | fits | 137,709 | 112 | 0.531 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 148,023 | 1.480 | 20 | 50 | fits | 151,235 | 227 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 302,794 | 3.028 | 20 | 50 | fits | 155,161 | 215 | 0.525 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 429,156 | 4.292 | 20 | 20 | fits | 126,427 | 52 | 0.641 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 620,070 | 6.201 | 20 | 20 | fits | 82,689 | 43 | 0.567 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 259,766 | 2.598 | 20 | 20 | fits | 155,161 | 215 | 0.525 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 144,911 | 1.449 | 20 | 200 | fits | 151,235 | 227 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 299,463 | 2.995 | 20 | 200 | fits | 155,161 | 215 | 0.525 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 145,823 | 1.458 | 20 | 20 | fits | 151,235 | 227 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 766,661 | 7.667 | 20 | 20 | fits | 136,723 | 111 | 0.524 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 149,408 | 1.494 | 20 | 24 | fits | 151,235 | 227 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 770,096 | 7.701 | 20 | 24 | fits | 136,723 | 111 | 0.524 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 148,368 | 1.484 | 20 | 50 | fits | 151,235 | 227 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 303,139 | 3.031 | 20 | 50 | fits | 155,161 | 215 | 0.525 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 429,620 | 4.296 | 20 | 20 | fits | 126,546 | 53 | 0.640 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 630,838 | 6.308 | 20 | 20 | fits | 78,772 | 36 | 0.530 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 259,766 | 2.598 | 20 | 20 | fits | 155,255 | 216 | 0.525 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 144,911 | 1.449 | 20 | 200 | fits | 151,235 | 227 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 299,557 | 2.996 | 20 | 200 | fits | 155,255 | 216 | 0.525 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 145,823 | 1.458 | 20 | 20 | fits | 151,235 | 227 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 762,880 | 7.629 | 20 | 20 | fits | 137,016 | 111 | 0.527 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 149,408 | 1.494 | 20 | 24 | fits | 151,235 | 227 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 766,315 | 7.663 | 20 | 24 | fits | 137,016 | 111 | 0.527 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 148,368 | 1.484 | 20 | 50 | fits | 151,235 | 227 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 303,233 | 3.032 | 20 | 50 | fits | 155,255 | 216 | 0.525 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 440,432 | 4.404 | 20 | 20 | fits | 129,068 | 58 | 0.650 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 626,764 | 6.268 | 20 | 20 | fits | 78,286 | 36 | 0.517 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 259,729 | 2.597 | 20 | 20 | fits | 155,043 | 216 | 0.525 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 144,911 | 1.449 | 20 | 200 | fits | 151,235 | 227 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 299,345 | 2.993 | 20 | 200 | fits | 155,043 | 216 | 0.525 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 145,823 | 1.458 | 20 | 20 | fits | 151,235 | 227 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 778,068 | 7.781 | 20 | 20 | fits | 152,419 | 113 | 0.555 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 149,408 | 1.494 | 20 | 24 | fits | 151,235 | 227 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 781,503 | 7.815 | 20 | 24 | fits | 152,419 | 113 | 0.555 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 148,368 | 1.484 | 20 | 50 | fits | 151,235 | 227 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 303,021 | 3.030 | 20 | 50 | fits | 155,043 | 216 | 0.525 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 440,217 | 4.402 | 20 | 20 | fits | 129,081 | 58 | 0.650 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 626,549 | 6.265 | 20 | 20 | fits | 78,286 | 36 | 0.517 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 271,497 | 2.715 | 20 | 20 | fits | 155,745 | 215 | 0.534 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 147,157 | 1.472 | 20 | 200 | fits | 151,186 | 228 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 311,472 | 3.115 | 20 | 200 | fits | 155,745 | 215 | 0.534 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 148,069 | 1.481 | 20 | 20 | fits | 151,186 | 228 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 828,503 | 8.285 | 20 | 20 | fits | 136,205 | 111 | 0.521 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 151,654 | 1.517 | 20 | 24 | fits | 151,186 | 228 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 831,938 | 8.319 | 20 | 24 | fits | 136,205 | 111 | 0.521 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 150,614 | 1.506 | 20 | 50 | fits | 151,186 | 228 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 315,148 | 3.151 | 20 | 50 | fits | 155,745 | 215 | 0.534 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 441,406 | 4.414 | 20 | 20 | fits | 126,323 | 52 | 0.641 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 693,198 | 6.932 | 20 | 20 | fits | 79,850 | 37 | 0.567 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 593,242 | 5.932 | 20 | 20 | fits | 158,518 | 174 | 0.572 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 141,187 | 1.412 | 20 | 200 | fits | 144,814 | 224 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 686,043 | 6.860 | 20 | 200 | fits | 158,518 | 174 | 0.572 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 142,099 | 1.421 | 20 | 20 | fits | 144,814 | 224 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 821,493 | 8.215 | 20 | 20 | fits | 134,754 | 112 | 0.508 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 145,684 | 1.457 | 20 | 24 | fits | 144,814 | 224 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 824,928 | 8.249 | 20 | 24 | fits | 134,754 | 112 | 0.508 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 144,644 | 1.446 | 20 | 50 | fits | 144,814 | 224 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 689,719 | 6.897 | 20 | 50 | fits | 158,518 | 174 | 0.572 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 278,636 | 2.786 | 20 | 20 | fits | 134,447 | 94 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 477,039 | 4.770 | 20 | 20 | fits | 90,153 | 42 | 0.601 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 594,154 | 5.942 | 20 | 20 | fits | 155,679 | 174 | 0.563 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 141,759 | 1.418 | 20 | 200 | fits | 144,822 | 224 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 685,063 | 6.851 | 20 | 200 | fits | 155,679 | 174 | 0.563 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 142,671 | 1.427 | 20 | 20 | fits | 144,822 | 224 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 833,076 | 8.331 | 20 | 20 | fits | 138,685 | 118 | 0.529 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 146,256 | 1.463 | 20 | 24 | fits | 144,822 | 224 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 836,511 | 8.365 | 20 | 24 | fits | 138,685 | 118 | 0.529 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 145,216 | 1.452 | 20 | 50 | fits | 144,822 | 224 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 688,739 | 6.887 | 20 | 50 | fits | 155,679 | 174 | 0.563 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 279,208 | 2.792 | 20 | 20 | fits | 134,447 | 94 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 530,980 | 5.310 | 20 | 20 | fits | 79,859 | 37 | 0.567 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 257,916 | 2.579 | 20 | 20 | fits | 157,142 | 201 | 0.586 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 142,339 | 1.423 | 20 | 200 | fits | 144,822 | 224 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 298,872 | 2.989 | 20 | 200 | fits | 157,142 | 201 | 0.586 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 143,251 | 1.433 | 20 | 20 | fits | 144,822 | 224 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 822,914 | 8.229 | 20 | 20 | fits | 144,660 | 111 | 0.539 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 146,836 | 1.468 | 20 | 24 | fits | 144,822 | 224 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 852,694 | 8.527 | 20 | 24 | fits | 26,345 | 18 | 0.725 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 145,796 | 1.458 | 20 | 50 | fits | 144,822 | 224 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 302,548 | 3.025 | 20 | 50 | fits | 157,142 | 201 | 0.586 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 477,758 | 4.778 | 20 | 20 | fits | 123,613 | 53 | 0.605 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 679,154 | 6.792 | 20 | 20 | fits | 78,489 | 36 | 0.523 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 269,118 | 2.691 | 20 | 20 | fits | 155,707 | 215 | 0.534 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 144,864 | 1.449 | 20 | 200 | fits | 151,188 | 228 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 309,157 | 3.092 | 20 | 200 | fits | 155,707 | 215 | 0.534 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 145,776 | 1.458 | 20 | 20 | fits | 151,188 | 228 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 763,966 | 7.640 | 20 | 20 | fits | 136,258 | 111 | 0.519 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 149,361 | 1.494 | 20 | 24 | fits | 151,188 | 228 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 767,401 | 7.674 | 20 | 24 | fits | 136,258 | 111 | 0.519 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 148,321 | 1.483 | 20 | 50 | fits | 151,188 | 228 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 312,833 | 3.128 | 20 | 50 | fits | 155,707 | 215 | 0.534 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 442,015 | 4.420 | 20 | 20 | fits | 129,247 | 58 | 0.649 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 628,608 | 6.286 | 20 | 20 | fits | 78,409 | 36 | 0.519 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 269,159 | 2.692 | 20 | 20 | fits | 155,707 | 215 | 0.534 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 144,905 | 1.449 | 20 | 200 | fits | 151,229 | 228 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 309,198 | 3.092 | 20 | 200 | fits | 155,707 | 215 | 0.534 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 145,817 | 1.458 | 20 | 20 | fits | 151,229 | 228 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 764,007 | 7.640 | 20 | 20 | fits | 136,258 | 111 | 0.519 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 149,402 | 1.494 | 20 | 24 | fits | 151,229 | 228 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 767,442 | 7.674 | 20 | 24 | fits | 136,258 | 111 | 0.519 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 148,362 | 1.484 | 20 | 50 | fits | 151,229 | 228 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 312,874 | 3.129 | 20 | 50 | fits | 155,707 | 215 | 0.534 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 442,056 | 4.421 | 20 | 20 | fits | 129,247 | 58 | 0.649 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 628,649 | 6.286 | 20 | 20 | fits | 78,409 | 36 | 0.519 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 237,932 | 2.379 | 20 | 20 | fits | 149,681 | 210 | 0.535 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 139,239 | 1.392 | 20 | 200 | fits | 145,563 | 224 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 288,311 | 2.883 | 20 | 200 | fits | 149,681 | 210 | 0.535 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 140,151 | 1.402 | 20 | 20 | fits | 145,563 | 224 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 752,018 | 7.520 | 20 | 20 | fits | 148,429 | 119 | 0.503 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 143,736 | 1.437 | 20 | 24 | fits | 145,563 | 224 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 755,453 | 7.555 | 20 | 24 | fits | 148,429 | 119 | 0.503 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 142,696 | 1.427 | 20 | 50 | fits | 145,563 | 224 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 291,987 | 2.920 | 20 | 50 | fits | 149,681 | 210 | 0.535 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 418,057 | 4.181 | 20 | 20 | fits | 126,135 | 52 | 0.637 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 604,489 | 6.045 | 20 | 20 | fits | 78,353 | 36 | 0.517 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 528,943 | 5.289 | 20 | 20 | fits | 155,918 | 174 | 0.562 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 141,403 | 1.414 | 20 | 200 | fits | 145,563 | 224 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 620,010 | 6.200 | 20 | 200 | fits | 155,918 | 174 | 0.562 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 142,315 | 1.423 | 20 | 20 | fits | 145,563 | 224 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 775,543 | 7.755 | 20 | 20 | fits | 146,348 | 121 | 0.540 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 145,900 | 1.459 | 20 | 24 | fits | 145,563 | 224 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 778,978 | 7.790 | 20 | 24 | fits | 146,348 | 121 | 0.540 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 144,860 | 1.449 | 20 | 50 | fits | 145,563 | 224 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 623,686 | 6.237 | 20 | 50 | fits | 155,918 | 174 | 0.562 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 278,755 | 2.788 | 20 | 20 | fits | 134,350 | 94 | 0.605 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 465,688 | 4.657 | 20 | 20 | fits | 78,585 | 36 | 0.523 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 552,077 | 5.521 | 20 | 20 | fits | 146,477 | 168 | 0.596 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 142,063 | 1.421 | 20 | 200 | fits | 145,563 | 224 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 620,642 | 6.206 | 20 | 200 | fits | 146,477 | 168 | 0.596 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 142,975 | 1.430 | 20 | 20 | fits | 145,563 | 224 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 844,537 | 8.445 | 20 | 20 | fits | 142,802 | 114 | 0.519 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 146,560 | 1.466 | 20 | 24 | fits | 145,563 | 224 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 874,514 | 8.745 | 20 | 24 | fits | 26,542 | 18 | 0.728 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 145,520 | 1.455 | 20 | 50 | fits | 145,563 | 224 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 624,318 | 6.243 | 20 | 50 | fits | 146,477 | 168 | 0.596 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 279,415 | 2.794 | 20 | 20 | fits | 134,350 | 94 | 0.605 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 466,461 | 4.665 | 20 | 20 | fits | 78,698 | 37 | 0.522 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 628,318 | 6.283 | 20 | 20 | fits | 156,387 | 174 | 0.565 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 142,723 | 1.427 | 20 | 200 | fits | 145,563 | 224 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 719,970 | 7.200 | 20 | 200 | fits | 156,387 | 174 | 0.565 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 143,635 | 1.436 | 20 | 20 | fits | 145,563 | 224 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 854,924 | 8.549 | 20 | 20 | fits | 134,258 | 111 | 0.504 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 147,220 | 1.472 | 20 | 24 | fits | 145,563 | 224 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 858,359 | 8.584 | 20 | 24 | fits | 134,258 | 111 | 0.504 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 146,180 | 1.462 | 20 | 50 | fits | 145,563 | 224 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 723,646 | 7.236 | 20 | 50 | fits | 156,387 | 174 | 0.565 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 280,075 | 2.801 | 20 | 20 | fits | 134,350 | 94 | 0.605 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 485,107 | 4.851 | 20 | 20 | fits | 87,346 | 49 | 0.604 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 630,087 | 6.301 | 20 | 20 | fits | 156,438 | 173 | 0.567 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 143,383 | 1.434 | 20 | 200 | fits | 145,563 | 224 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 721,461 | 7.215 | 20 | 200 | fits | 156,438 | 173 | 0.567 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 144,295 | 1.443 | 20 | 20 | fits | 145,563 | 224 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 856,492 | 8.565 | 20 | 20 | fits | 134,335 | 111 | 0.504 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 147,880 | 1.479 | 20 | 24 | fits | 145,563 | 224 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 859,927 | 8.599 | 20 | 24 | fits | 134,335 | 111 | 0.504 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 146,840 | 1.468 | 20 | 50 | fits | 145,563 | 224 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 725,137 | 7.251 | 20 | 50 | fits | 156,438 | 173 | 0.567 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 280,854 | 2.809 | 20 | 20 | fits | 134,469 | 95 | 0.605 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 566,619 | 5.666 | 20 | 20 | fits | 79,269 | 37 | 0.553 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 261,643 | 2.616 | 20 | 20 | fits | 149,604 | 201 | 0.571 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 144,202 | 1.442 | 20 | 200 | fits | 145,722 | 225 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 301,907 | 3.019 | 20 | 200 | fits | 149,604 | 201 | 0.571 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 145,114 | 1.451 | 20 | 20 | fits | 145,722 | 225 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 843,937 | 8.439 | 20 | 20 | fits | 143,972 | 111 | 0.531 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 148,699 | 1.487 | 20 | 24 | fits | 145,722 | 225 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 873,819 | 8.738 | 20 | 24 | fits | 26,447 | 19 | 0.723 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 147,659 | 1.477 | 20 | 50 | fits | 145,722 | 225 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 305,583 | 3.056 | 20 | 50 | fits | 149,604 | 201 | 0.571 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 514,218 | 5.142 | 20 | 20 | fits | 128,264 | 58 | 0.640 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 700,865 | 7.009 | 20 | 20 | fits | 78,412 | 36 | 0.519 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 588,971 | 5.890 | 20 | 20 | fits | 151,142 | 156 | 0.565 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 149,228 | 1.492 | 20 | 200 | fits | 149,120 | 242 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 636,872 | 6.369 | 20 | 200 | fits | 151,142 | 156 | 0.565 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 150,140 | 1.501 | 20 | 20 | fits | 149,120 | 242 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 771,158 | 7.712 | 20 | 20 | fits | 133,590 | 111 | 0.499 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 153,725 | 1.537 | 20 | 24 | fits | 149,120 | 242 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 774,593 | 7.746 | 20 | 24 | fits | 133,590 | 111 | 0.499 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 152,685 | 1.527 | 20 | 50 | fits | 149,120 | 242 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 640,548 | 6.405 | 20 | 50 | fits | 151,142 | 156 | 0.565 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 286,362 | 2.864 | 20 | 20 | fits | 134,132 | 94 | 0.602 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 487,326 | 4.873 | 20 | 20 | fits | 83,351 | 43 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 589,589 | 5.896 | 20 | 20 | fits | 150,777 | 156 | 0.563 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 149,888 | 1.499 | 20 | 200 | fits | 149,120 | 242 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 637,429 | 6.374 | 20 | 200 | fits | 150,777 | 156 | 0.563 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 150,800 | 1.508 | 20 | 20 | fits | 149,120 | 242 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 771,747 | 7.717 | 20 | 20 | fits | 133,622 | 111 | 0.499 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 154,385 | 1.544 | 20 | 24 | fits | 149,120 | 242 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 775,182 | 7.752 | 20 | 24 | fits | 133,622 | 111 | 0.499 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 153,345 | 1.533 | 20 | 50 | fits | 149,120 | 242 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 641,105 | 6.411 | 20 | 50 | fits | 150,777 | 156 | 0.563 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 287,141 | 2.871 | 20 | 20 | fits | 134,251 | 95 | 0.602 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 488,248 | 4.882 | 20 | 20 | fits | 78,712 | 36 | 0.526 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 256,981 | 2.570 | 20 | 20 | fits | 147,251 | 193 | 0.551 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 150,705 | 1.507 | 20 | 200 | fits | 149,277 | 243 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 306,100 | 3.061 | 20 | 200 | fits | 147,251 | 193 | 0.551 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 151,617 | 1.516 | 20 | 20 | fits | 149,277 | 243 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 770,158 | 7.702 | 20 | 20 | fits | 148,309 | 119 | 0.502 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 155,202 | 1.552 | 20 | 24 | fits | 149,277 | 243 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 773,593 | 7.736 | 20 | 24 | fits | 148,309 | 119 | 0.502 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 154,162 | 1.542 | 20 | 50 | fits | 149,277 | 243 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 309,776 | 3.098 | 20 | 50 | fits | 147,251 | 193 | 0.551 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 436,174 | 4.362 | 20 | 20 | fits | 126,463 | 52 | 0.641 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 622,749 | 6.227 | 20 | 20 | fits | 78,350 | 36 | 0.517 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 597,190 | 5.972 | 20 | 20 | fits | 157,227 | 175 | 0.561 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 156,222 | 1.562 | 20 | 200 | fits | 155,460 | 229 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 636,467 | 6.365 | 20 | 200 | fits | 157,227 | 175 | 0.561 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 157,134 | 1.571 | 20 | 20 | fits | 155,460 | 229 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 768,651 | 7.687 | 20 | 20 | fits | 131,488 | 108 | 0.550 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 160,719 | 1.607 | 20 | 24 | fits | 155,460 | 229 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 772,086 | 7.721 | 20 | 24 | fits | 131,488 | 108 | 0.550 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 159,679 | 1.597 | 20 | 50 | fits | 155,460 | 229 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 640,143 | 6.401 | 20 | 50 | fits | 157,227 | 175 | 0.561 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 293,897 | 2.939 | 20 | 20 | fits | 134,673 | 94 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 480,836 | 4.808 | 20 | 20 | fits | 78,588 | 36 | 0.523 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 608,948 | 6.089 | 20 | 20 | fits | 146,760 | 165 | 0.592 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 156,882 | 1.569 | 20 | 200 | fits | 155,409 | 229 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 626,660 | 6.267 | 20 | 200 | fits | 146,760 | 165 | 0.592 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 157,794 | 1.578 | 20 | 20 | fits | 155,409 | 229 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 770,950 | 7.710 | 20 | 20 | fits | 143,594 | 114 | 0.520 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 161,379 | 1.614 | 20 | 24 | fits | 155,409 | 229 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 774,385 | 7.744 | 20 | 24 | fits | 143,594 | 114 | 0.520 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 160,339 | 1.603 | 20 | 50 | fits | 155,409 | 229 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 630,336 | 6.303 | 20 | 50 | fits | 146,760 | 165 | 0.592 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 294,557 | 2.946 | 20 | 20 | fits | 134,673 | 94 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 481,496 | 4.815 | 20 | 20 | fits | 78,588 | 36 | 0.523 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 604,960 | 6.050 | 20 | 20 | fits | 157,502 | 176 | 0.561 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 157,542 | 1.575 | 20 | 200 | fits | 155,409 | 229 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 644,236 | 6.442 | 20 | 200 | fits | 157,502 | 176 | 0.561 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 158,454 | 1.585 | 20 | 20 | fits | 155,409 | 229 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 778,096 | 7.781 | 20 | 20 | fits | 124,772 | 106 | 0.543 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 162,039 | 1.620 | 20 | 24 | fits | 155,409 | 229 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 781,531 | 7.815 | 20 | 24 | fits | 124,772 | 106 | 0.543 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 160,999 | 1.610 | 20 | 50 | fits | 155,409 | 229 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 647,912 | 6.479 | 20 | 50 | fits | 157,502 | 176 | 0.561 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 295,217 | 2.952 | 20 | 20 | fits | 134,673 | 94 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 488,330 | 4.883 | 20 | 20 | fits | 84,762 | 42 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 620,469 | 6.205 | 20 | 20 | fits | 158,055 | 175 | 0.566 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 158,202 | 1.582 | 20 | 200 | fits | 155,409 | 229 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 659,758 | 6.598 | 20 | 200 | fits | 158,055 | 175 | 0.566 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 159,114 | 1.591 | 20 | 20 | fits | 155,409 | 229 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 781,658 | 7.817 | 20 | 20 | fits | 121,204 | 99 | 0.523 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 162,699 | 1.627 | 20 | 24 | fits | 155,409 | 229 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 785,093 | 7.851 | 20 | 24 | fits | 121,204 | 99 | 0.523 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 161,659 | 1.617 | 20 | 50 | fits | 155,409 | 229 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 663,434 | 6.634 | 20 | 50 | fits | 158,055 | 175 | 0.566 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 295,877 | 2.959 | 20 | 20 | fits | 134,673 | 94 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 503,299 | 5.033 | 20 | 20 | fits | 83,370 | 43 | 0.605 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 269,702 | 2.697 | 20 | 20 | fits | 149,904 | 207 | 0.558 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 158,862 | 1.589 | 20 | 200 | fits | 155,409 | 229 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 308,157 | 3.082 | 20 | 200 | fits | 149,904 | 207 | 0.558 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 159,774 | 1.598 | 20 | 20 | fits | 155,409 | 229 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 780,323 | 7.803 | 20 | 20 | fits | 145,364 | 110 | 0.543 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 163,359 | 1.634 | 20 | 24 | fits | 155,409 | 229 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 783,758 | 7.838 | 20 | 24 | fits | 145,364 | 110 | 0.543 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 162,319 | 1.623 | 20 | 50 | fits | 155,409 | 229 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 311,833 | 3.118 | 20 | 50 | fits | 149,904 | 207 | 0.558 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 449,292 | 4.493 | 20 | 20 | fits | 129,275 | 58 | 0.652 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 635,859 | 6.359 | 20 | 20 | fits | 78,353 | 36 | 0.517 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 568,617 | 5.686 | 20 | 20 | fits | 156,469 | 176 | 0.555 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 151,689 | 1.517 | 20 | 200 | fits | 151,152 | 227 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 630,670 | 6.307 | 20 | 200 | fits | 156,469 | 176 | 0.555 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 152,601 | 1.526 | 20 | 20 | fits | 151,152 | 227 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 756,840 | 7.568 | 20 | 20 | fits | 125,474 | 106 | 0.488 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 156,186 | 1.562 | 20 | 24 | fits | 151,152 | 227 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 760,275 | 7.603 | 20 | 24 | fits | 125,474 | 106 | 0.488 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 155,146 | 1.551 | 20 | 50 | fits | 151,152 | 227 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 634,346 | 6.343 | 20 | 50 | fits | 156,469 | 176 | 0.555 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 289,285 | 2.893 | 20 | 20 | fits | 134,594 | 94 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 475,797 | 4.758 | 20 | 20 | fits | 78,409 | 36 | 0.519 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 569,277 | 5.693 | 20 | 20 | fits | 156,579 | 177 | 0.554 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 152,349 | 1.523 | 20 | 200 | fits | 151,152 | 227 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 631,440 | 6.314 | 20 | 200 | fits | 156,579 | 177 | 0.554 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 153,261 | 1.533 | 20 | 20 | fits | 151,152 | 227 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 770,603 | 7.706 | 20 | 20 | fits | 129,978 | 112 | 0.517 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 156,846 | 1.568 | 20 | 24 | fits | 151,152 | 227 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 774,038 | 7.740 | 20 | 24 | fits | 129,978 | 112 | 0.517 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 155,806 | 1.558 | 20 | 50 | fits | 151,152 | 227 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 635,116 | 6.351 | 20 | 50 | fits | 156,579 | 177 | 0.554 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 289,945 | 2.899 | 20 | 20 | fits | 134,594 | 94 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 476,457 | 4.765 | 20 | 20 | fits | 78,409 | 36 | 0.519 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 570,092 | 5.701 | 20 | 20 | fits | 156,614 | 177 | 0.555 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 153,009 | 1.530 | 20 | 200 | fits | 151,152 | 227 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 632,135 | 6.321 | 20 | 200 | fits | 156,614 | 177 | 0.555 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 153,921 | 1.539 | 20 | 20 | fits | 151,152 | 227 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 771,095 | 7.711 | 20 | 20 | fits | 129,775 | 112 | 0.514 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 157,506 | 1.575 | 20 | 24 | fits | 151,152 | 227 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 774,530 | 7.745 | 20 | 24 | fits | 129,775 | 112 | 0.514 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 156,466 | 1.565 | 20 | 50 | fits | 151,152 | 227 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 635,811 | 6.358 | 20 | 50 | fits | 156,614 | 177 | 0.555 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 290,605 | 2.906 | 20 | 20 | fits | 134,594 | 94 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 477,117 | 4.771 | 20 | 20 | fits | 78,409 | 36 | 0.519 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 585,957 | 5.860 | 20 | 20 | fits | 157,368 | 176 | 0.559 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 153,669 | 1.537 | 20 | 200 | fits | 151,152 | 227 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 648,024 | 6.480 | 20 | 200 | fits | 157,368 | 176 | 0.559 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 154,581 | 1.546 | 20 | 20 | fits | 151,152 | 227 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 784,958 | 7.850 | 20 | 20 | fits | 136,238 | 113 | 0.523 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 158,166 | 1.582 | 20 | 24 | fits | 151,152 | 227 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 788,393 | 7.884 | 20 | 24 | fits | 136,238 | 113 | 0.523 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 157,126 | 1.571 | 20 | 50 | fits | 151,152 | 227 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 651,700 | 6.517 | 20 | 50 | fits | 157,368 | 176 | 0.559 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 291,265 | 2.913 | 20 | 20 | fits | 134,594 | 94 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 492,252 | 4.923 | 20 | 20 | fits | 83,368 | 43 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 597,564 | 5.976 | 20 | 20 | fits | 145,323 | 164 | 0.589 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 154,329 | 1.543 | 20 | 200 | fits | 151,152 | 227 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 637,055 | 6.371 | 20 | 200 | fits | 145,323 | 164 | 0.589 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 155,241 | 1.552 | 20 | 20 | fits | 151,152 | 227 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 863,596 | 8.636 | 20 | 20 | fits | 148,027 | 118 | 0.498 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 158,826 | 1.588 | 20 | 24 | fits | 151,152 | 227 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 867,031 | 8.670 | 20 | 24 | fits | 148,027 | 118 | 0.498 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 157,786 | 1.578 | 20 | 50 | fits | 151,152 | 227 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 640,731 | 6.407 | 20 | 50 | fits | 145,323 | 164 | 0.589 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 292,044 | 2.920 | 20 | 20 | fits | 134,713 | 95 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 493,328 | 4.933 | 20 | 20 | fits | 78,709 | 36 | 0.526 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 341,689 | 3.417 | 20 | 20 | fits | 146,981 | 156 | 0.538 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 139,783 | 1.398 | 20 | 200 | fits | 148,512 | 202 | 0.534 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 446,732 | 4.467 | 20 | 200 | fits | 146,981 | 156 | 0.538 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 140,695 | 1.407 | 20 | 20 | fits | 148,512 | 202 | 0.534 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 447,428 | 4.474 | 20 | 20 | fits | 146,981 | 156 | 0.538 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 144,280 | 1.443 | 20 | 24 | fits | 148,512 | 202 | 0.534 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 450,863 | 4.509 | 20 | 24 | fits | 146,981 | 156 | 0.538 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 143,240 | 1.432 | 20 | 50 | fits | 148,512 | 202 | 0.534 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 303,427 | 3.034 | 20 | 50 | fits | 151,977 | 195 | 0.533 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 581,891 | 5.819 | 20 | 20 | fits | 131,548 | 58 | 0.653 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 846,761 | 8.468 | 20 | 20 | fits | 78,575 | 36 | 0.523 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 237,028 | 2.370 | 20 | 20 | fits | 149,330 | 210 | 0.534 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 138,574 | 1.386 | 20 | 200 | fits | 146,503 | 225 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 287,295 | 2.873 | 20 | 200 | fits | 149,330 | 210 | 0.534 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 139,486 | 1.395 | 20 | 20 | fits | 146,503 | 225 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 836,363 | 8.364 | 20 | 20 | fits | 149,237 | 119 | 0.507 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 143,071 | 1.431 | 20 | 24 | fits | 146,503 | 225 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 839,798 | 8.398 | 20 | 24 | fits | 149,237 | 119 | 0.507 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 142,031 | 1.420 | 20 | 50 | fits | 146,503 | 225 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 290,971 | 2.910 | 20 | 50 | fits | 149,330 | 210 | 0.534 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 423,593 | 4.236 | 20 | 20 | fits | 132,687 | 64 | 0.647 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 688,026 | 6.880 | 20 | 20 | fits | 78,412 | 36 | 0.519 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 260,001 | 2.600 | 20 | 20 | fits | 146,838 | 196 | 0.535 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 139,876 | 1.399 | 20 | 200 | fits | 148,695 | 201 | 0.535 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 286,105 | 2.861 | 20 | 200 | fits | 146,838 | 196 | 0.535 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 140,788 | 1.408 | 20 | 20 | fits | 148,695 | 201 | 0.535 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 431,689 | 4.317 | 20 | 20 | fits | 144,888 | 147 | 0.536 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 144,373 | 1.444 | 20 | 24 | fits | 148,695 | 201 | 0.535 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 869,372 | 8.694 | 20 | 24 | fits | 28,546 | 18 | 0.752 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 143,333 | 1.433 | 20 | 50 | fits | 148,695 | 201 | 0.535 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 289,781 | 2.898 | 20 | 50 | fits | 146,838 | 196 | 0.535 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 637,320 | 6.373 | 20 | 20 | fits | 125,144 | 52 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 838,291 | 8.383 | 20 | 20 | fits | 83,492 | 43 | 0.606 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 247,962 | 2.480 | 20 | 20 | fits | 146,893 | 193 | 0.551 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 142,154 | 1.422 | 20 | 200 | fits | 149,069 | 243 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 297,081 | 2.971 | 20 | 200 | fits | 146,893 | 193 | 0.551 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 143,066 | 1.431 | 20 | 20 | fits | 149,069 | 243 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 764,432 | 7.644 | 20 | 20 | fits | 148,540 | 119 | 0.503 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 146,651 | 1.467 | 20 | 24 | fits | 149,069 | 243 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 767,867 | 7.679 | 20 | 24 | fits | 148,540 | 119 | 0.503 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 145,611 | 1.456 | 20 | 50 | fits | 149,069 | 243 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 300,757 | 3.008 | 20 | 50 | fits | 146,893 | 193 | 0.551 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 430,199 | 4.302 | 20 | 20 | fits | 129,507 | 58 | 0.650 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 616,792 | 6.168 | 20 | 20 | fits | 78,409 | 36 | 0.519 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 248,547 | 2.485 | 20 | 20 | fits | 146,846 | 193 | 0.551 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 142,786 | 1.428 | 20 | 200 | fits | 149,110 | 243 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 297,666 | 2.977 | 20 | 200 | fits | 146,846 | 193 | 0.551 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 143,698 | 1.437 | 20 | 20 | fits | 149,110 | 243 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 765,017 | 7.650 | 20 | 20 | fits | 148,540 | 119 | 0.503 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 147,283 | 1.473 | 20 | 24 | fits | 149,110 | 243 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 768,452 | 7.685 | 20 | 24 | fits | 148,540 | 119 | 0.503 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 146,243 | 1.462 | 20 | 50 | fits | 149,110 | 243 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 301,342 | 3.013 | 20 | 50 | fits | 146,846 | 193 | 0.551 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 430,784 | 4.308 | 20 | 20 | fits | 129,507 | 58 | 0.650 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 617,377 | 6.174 | 20 | 20 | fits | 78,409 | 36 | 0.519 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 250,656 | 2.507 | 20 | 20 | fits | 150,417 | 215 | 0.528 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 149,411 | 1.494 | 20 | 200 | fits | 155,735 | 229 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 299,219 | 2.992 | 20 | 200 | fits | 150,417 | 215 | 0.528 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 150,323 | 1.503 | 20 | 20 | fits | 155,735 | 229 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 752,063 | 7.521 | 20 | 20 | fits | 137,286 | 112 | 0.524 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 153,908 | 1.539 | 20 | 24 | fits | 155,735 | 229 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 755,498 | 7.555 | 20 | 24 | fits | 137,286 | 112 | 0.524 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 152,868 | 1.529 | 20 | 50 | fits | 155,735 | 229 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 302,895 | 3.029 | 20 | 50 | fits | 150,417 | 215 | 0.528 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 429,245 | 4.292 | 20 | 20 | fits | 126,415 | 52 | 0.639 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 615,677 | 6.157 | 20 | 20 | fits | 78,353 | 36 | 0.517 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 250,656 | 2.507 | 20 | 20 | fits | 150,417 | 215 | 0.528 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 149,411 | 1.494 | 20 | 200 | fits | 155,735 | 229 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 299,219 | 2.992 | 20 | 200 | fits | 150,417 | 215 | 0.528 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 150,323 | 1.503 | 20 | 20 | fits | 155,735 | 229 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 771,947 | 7.719 | 20 | 20 | fits | 147,540 | 119 | 0.548 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 153,908 | 1.539 | 20 | 24 | fits | 155,735 | 229 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 775,382 | 7.754 | 20 | 24 | fits | 147,540 | 119 | 0.548 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 152,868 | 1.529 | 20 | 50 | fits | 155,735 | 229 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 302,895 | 3.029 | 20 | 50 | fits | 150,417 | 215 | 0.528 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 429,245 | 4.292 | 20 | 20 | fits | 126,415 | 52 | 0.639 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 615,790 | 6.158 | 20 | 20 | fits | 78,466 | 37 | 0.516 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 614,344 | 6.143 | 20 | 20 | fits | 148,917 | 172 | 0.594 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 151,310 | 1.513 | 20 | 200 | fits | 155,735 | 229 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 632,252 | 6.323 | 20 | 200 | fits | 148,917 | 172 | 0.594 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 152,222 | 1.522 | 20 | 20 | fits | 155,735 | 229 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 776,481 | 7.765 | 20 | 20 | fits | 143,533 | 113 | 0.519 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 155,807 | 1.558 | 20 | 24 | fits | 155,735 | 229 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 779,916 | 7.799 | 20 | 24 | fits | 143,533 | 113 | 0.519 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 154,767 | 1.548 | 20 | 50 | fits | 155,735 | 229 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 635,928 | 6.359 | 20 | 50 | fits | 148,917 | 172 | 0.594 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 288,931 | 2.889 | 20 | 20 | fits | 134,619 | 94 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 475,631 | 4.756 | 20 | 20 | fits | 78,525 | 37 | 0.518 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 611,476 | 6.115 | 20 | 20 | fits | 157,994 | 175 | 0.565 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 151,970 | 1.520 | 20 | 200 | fits | 155,735 | 229 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 650,765 | 6.508 | 20 | 200 | fits | 157,994 | 175 | 0.565 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 152,882 | 1.529 | 20 | 20 | fits | 155,735 | 229 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 772,694 | 7.727 | 20 | 20 | fits | 121,233 | 99 | 0.523 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 156,467 | 1.565 | 20 | 24 | fits | 155,735 | 229 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 776,129 | 7.761 | 20 | 24 | fits | 121,233 | 99 | 0.523 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 155,427 | 1.554 | 20 | 50 | fits | 155,735 | 229 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 654,441 | 6.544 | 20 | 50 | fits | 157,994 | 175 | 0.565 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 289,591 | 2.896 | 20 | 20 | fits | 134,619 | 94 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 494,367 | 4.944 | 20 | 20 | fits | 87,263 | 49 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 612,162 | 6.122 | 20 | 20 | fits | 157,550 | 175 | 0.563 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 152,630 | 1.526 | 20 | 200 | fits | 155,735 | 229 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 651,451 | 6.515 | 20 | 200 | fits | 157,550 | 175 | 0.563 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 153,542 | 1.535 | 20 | 20 | fits | 155,735 | 229 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 773,441 | 7.734 | 20 | 20 | fits | 121,294 | 99 | 0.523 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 157,127 | 1.571 | 20 | 24 | fits | 155,735 | 229 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 776,876 | 7.769 | 20 | 24 | fits | 121,294 | 99 | 0.523 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 156,087 | 1.561 | 20 | 50 | fits | 155,735 | 229 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 655,127 | 6.551 | 20 | 50 | fits | 157,550 | 175 | 0.563 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 290,370 | 2.904 | 20 | 20 | fits | 134,738 | 95 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 495,497 | 4.955 | 20 | 20 | fits | 78,792 | 36 | 0.528 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 273,338 | 2.733 | 20 | 20 | fits | 150,413 | 206 | 0.562 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 153,440 | 1.534 | 20 | 200 | fits | 155,885 | 230 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 311,517 | 3.115 | 20 | 200 | fits | 150,413 | 206 | 0.562 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 154,352 | 1.544 | 20 | 20 | fits | 155,885 | 230 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 774,717 | 7.747 | 20 | 20 | fits | 144,438 | 110 | 0.536 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 157,937 | 1.579 | 20 | 24 | fits | 155,885 | 230 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 778,152 | 7.782 | 20 | 24 | fits | 144,438 | 110 | 0.536 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 156,897 | 1.569 | 20 | 50 | fits | 155,885 | 230 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 315,193 | 3.152 | 20 | 50 | fits | 150,413 | 206 | 0.562 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 444,504 | 4.445 | 20 | 20 | fits | 129,376 | 58 | 0.649 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 631,179 | 6.312 | 20 | 20 | fits | 78,412 | 36 | 0.519 |
| LINK_UP | `adp.link_up.if0` | 2,428 | 0.024 | 20 | 200 | fits | 22,299 | 43 (11) | 0.719 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,180 | 0.122 | 20 | 200 | fits | 18,795 | 23 (39) | 0.764 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 12,176 | 0.122 | 20 | 200 | fits | 2,535 | 10 (11) | 0.500 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 151,975 | 1.520 | 20 | 200 | fits | 152,914 | 246 | 0.434 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 510,380 | 5.104 | 20 | 20 | fits | 60,757 | 88 | 0.505 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 252,184 | 2.522 | 20 | 24 | fits | 94,268 | 79 | 0.467 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 470,905 | 4.709 | 20 | 50 | fits | 60,757 | 88 | 0.505 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 388,123 | 3.881 | 20 | 20 | fits | 78,702 | 36 | 0.528 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 84,164 | 0.842 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 151,975 | 1.520 | 20 | 200 | fits | 152,914 | 246 | 0.434 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 522,013 | 5.220 | 20 | 20 | fits | 64,105 | 94 | 0.538 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 255,423 | 2.554 | 20 | 24 | fits | 96,304 | 84 | 0.478 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 482,538 | 4.825 | 20 | 50 | fits | 64,105 | 94 | 0.538 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 398,395 | 3.984 | 20 | 20 | fits | 82,345 | 49 | 0.555 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 89,370 | 0.894 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 18,729 | 0.187 | 20 | 20 | fits | 24,697 | 21 (35) | 0.821 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 9,205 | 0.092 | 20 | 20 | fits | 21,958 | 17 (14) | 0.870 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 5,514 | 0.055 | 20 | 20 | fits | 21,227 | 18 (14) | 0.863 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 20,910 | 0.209 | 20 | 20 | fits | 24,694 | 21 (35) | 0.824 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 67,976 | 0.680 | 20 | 20 | fits | 51,897 | 6 | 0.879 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 35,923 | 0.359 | 20 | 20 | fits | 35,988 | 12 | 0.907 |
| malformed MRPDU discard | `srp.malformed.if0` | 15,285 | 0.153 | 20 | 20 | fits | 15,350 | 12 | 0.738 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 71,288 | 0.713 | 220 | 220 | fits | 73,050 | 9 | 0.872 |
| an event behind 15 others | `backlog.event.if0` | 161,051 | 1.611 | 20 | 200 | fits | 73,711 | 109 | 0.557 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 444,908 | 4.449 | 20 | 20 | fits | 142,399 | 112 | 0.520 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 150,357 | 1.504 | 20 | 200 | fits | 150,565 | 230 | 0.515 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 299,779 | 2.998 | 20 | 200 | fits | 76,320 | 49 | 0.675 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 146,098 | 1.461 | 20 | 20 | fits | 150,565 | 230 | 0.515 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 513,767 | 5.138 | 20 | 20 | fits | 142,399 | 112 | 0.520 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 149,683 | 1.497 | 20 | 24 | fits | 150,565 | 230 | 0.515 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 543,480 | 5.435 | 20 | 24 | fits | 26,278 | 18 | 0.728 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 148,643 | 1.486 | 20 | 50 | fits | 150,565 | 230 | 0.515 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 298,284 | 2.983 | 20 | 50 | fits | 76,320 | 49 | 0.675 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 328,864 | 3.289 | 20 | 20 | fits | 27,371 | 53 | 0.305 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 372,268 | 3.723 | 20 | 20 | fits | 20,164 | 36 | 0.216 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 578,885 | 5.789 | 20 | 20 | fits | 156,603 | 176 | 0.556 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 146,631 | 1.466 | 20 | 200 | fits | 151,313 | 230 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 640,693 | 6.407 | 20 | 200 | fits | 156,603 | 176 | 0.556 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 147,543 | 1.475 | 20 | 20 | fits | 151,313 | 230 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 777,743 | 7.777 | 20 | 20 | fits | 136,354 | 113 | 0.525 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 151,128 | 1.511 | 20 | 24 | fits | 151,313 | 230 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 781,178 | 7.812 | 20 | 24 | fits | 136,354 | 113 | 0.525 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 150,088 | 1.501 | 20 | 50 | fits | 151,313 | 230 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 644,369 | 6.444 | 20 | 50 | fits | 156,603 | 176 | 0.556 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 284,438 | 2.844 | 20 | 20 | fits | 134,805 | 95 | 0.609 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 485,686 | 4.857 | 20 | 20 | fits | 78,704 | 36 | 0.526 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 12,929 | 0.129 | 20 | 20 | fits | 21,507 | 19 | 0.789 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 146,631 | 1.466 | 20 | 200 | fits | 151,313 | 230 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 27,197 | 0.272 | 20 | 200 | fits | 21,507 | 19 | 0.789 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 147,543 | 1.475 | 20 | 20 | fits | 151,313 | 230 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 767,624 | 7.676 | 20 | 20 | fits | 135,662 | 113 | 0.522 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 151,128 | 1.511 | 20 | 24 | fits | 151,313 | 230 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 771,059 | 7.711 | 20 | 24 | fits | 135,662 | 113 | 0.522 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 150,088 | 1.501 | 20 | 50 | fits | 151,313 | 230 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 634,942 | 6.349 | 20 | 50 | fits | 147,176 | 166 | 0.540 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 284,438 | 2.844 | 20 | 20 | fits | 134,805 | 95 | 0.609 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 485,686 | 4.857 | 20 | 20 | fits | 78,704 | 36 | 0.526 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,291,589 | 62.916 | 20 | 20 | MISS ceiling | 14,480 | 13 | 0.615 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,306,009 | 63.060 | 20 | 20 | MISS ceiling | 14,495 | 13 | 0.615 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,320,345 | 63.203 | 20 | 20 | MISS ceiling | 14,392 | 13 | 0.615 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,334,720 | 63.347 | 20 | 20 | MISS ceiling | 14,450 | 13 | 0.606 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,348,956 | 63.490 | 20 | 20 | MISS ceiling | 14,299 | 13 | 0.625 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 154,676 | 1.547 | 20 | 200 | fits | 146,343 | 235 | 0.498 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 586,264 | 5.863 | 20 | 200 | fits | 105,774 | 114 | 0.569 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 150,417 | 1.504 | 20 | 20 | fits | 146,343 | 235 | 0.498 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,220,468 | 62.205 | 20 | 20 | MISS ceiling | 25,436 | 15 | 0.761 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 154,002 | 1.540 | 20 | 24 | fits | 146,343 | 235 | 0.498 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,198,467 | 61.985 | 20 | 24 | MISS ceiling | 161,050 | 120 | 0.468 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 152,962 | 1.530 | 20 | 50 | fits | 146,343 | 235 | 0.498 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 584,769 | 5.848 | 20 | 50 | fits | 105,774 | 114 | 0.569 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 287,762 | 2.878 | 20 | 20 | fits | 135,255 | 95 | 0.608 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 476,915 | 4.769 | 20 | 20 | fits | 79,517 | 37 | 0.537 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,033 | 0.050 | 20 | 20 | fits | 19,043 | 13 (29) | 0.775 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 6,797 | 0.068 | 20 | 20 | fits | 20,973 | 19 (35) | 0.782 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 16,695 | 0.167 | 20 | 20 | fits | 24,839 | 21 (12) | 0.825 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 10,258 | 0.103 | 20 | 50 | fits | 22,299 | 43 | 0.719 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 16,118 | 0.161 | 20 | 50 | fits | 19,840 | 35 | 0.715 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 16,797 | 0.168 | 20 | 50 | fits | 19,553 | 35 | 0.713 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 15,852 | 0.159 | 20 | 50 | fits | 24,183 | 61 | 0.638 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 18,004 | 0.180 | 20 | 50 | fits | 24,183 | 61 | 0.638 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 8,867 | 0.089 | 20 | 50 | fits | 18,010 | 30 | 0.649 |
| LINK_UP | `adp.link_up.if0` | 2,428 | 0.024 | 20 | 200 | fits | 22,299 | 43 (11) | 0.719 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,180 | 0.122 | 20 | 200 | fits | 18,795 | 23 (39) | 0.764 |
| LINK_DOWN | `adp.link_down.if0` | 2,003 | 0.020 | 20 | 200 | fits | 20,511 | 23 (9) | 0.779 |
| LINK_UP | `adp.link_up.if0` | 2,428 | 0.024 | 20 | 200 | fits | 22,299 | 43 (11) | 0.719 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,180 | 0.122 | 20 | 200 | fits | 18,795 | 23 (39) | 0.764 |
| GM_CHANGE | `adp.gm_change.if0` | 2,186 | 0.022 | 20 | 200 | fits | 12,938 | 17 (11) | 0.740 |
| LINK_UP | `adp.link_up.if0` | 2,428 | 0.024 | 20 | 200 | fits | 22,299 | 43 (11) | 0.719 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,180 | 0.122 | 20 | 200 | fits | 18,795 | 23 (39) | 0.764 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,030 | 0.040 | 20 | 200 | fits | 13,129 | 16 (31) | 0.636 |
| LINK_UP | `adp.link_up.if0` | 2,428 | 0.024 | 20 | 200 | fits | 22,299 | 43 (11) | 0.719 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,180 | 0.122 | 20 | 200 | fits | 18,795 | 23 (39) | 0.764 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,030 | 0.040 | 20 | 200 | fits | 13,129 | 16 (31) | 0.636 |
| set_name | `aecp_fanout.set_name.if0` | 42,569 | 0.426 | 20 | 24 | fits | 55,082 | 88 | 0.540 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 43,026 | 0.430 | 20 | 24 | fits | 48,726 | 77 | 0.577 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 35,549 | 0.355 | 20 | 24 | fits | 44,244 | 78 | 0.530 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 35,542 | 0.355 | 20 | 24 | fits | 44,195 | 77 | 0.534 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 43,711 | 0.437 | 20 | 24 | fits | 49,904 | 66 | 0.596 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 37,008 | 0.370 | 20 | 24 | fits | 47,777 | 65 | 0.561 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 47,981 | 0.480 | 20 | 24 | fits | 47,264 | 66 | 0.578 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 35,281 | 0.353 | 20 | 24 | fits | 43,933 | 77 | 0.537 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 36,690 | 0.367 | 20 | 24 | fits | 44,314 | 78 | 0.541 |
| BIND_RX | `acmp.bind_rx.if0` | 18,286 | 0.183 | 20 | 20 | fits | 37,002 | 26 (77) | 0.802 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 8,621 | 0.086 | 20 | 20 | fits | 25,223 | 20 (32) | 0.817 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 9,683 | 0.097 | 20 | 20 | fits | 20,557 | 15 (47) | 0.766 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 12,601 | 0.126 | 20 | 20 | fits | 31,707 | 18 (50) | 0.832 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 9,954 | 0.100 | 20 | 20 | fits | 21,767 | 17 (48) | 0.765 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,276 | 0.093 | 20 | 20 | fits | 20,488 | 16 (48) | 0.736 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 8,697 | 0.087 | 20 | 20 | fits | 19,552 | 16 (48) | 0.721 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,058 | 0.091 | 20 | 20 | fits | 19,423 | 16 (48) | 0.719 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 20,962 | 0.210 | 20 | 24 | fits | 24,245 | 20 | 0.805 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 20,901 | 0.209 | 20 | 24 | fits | 27,623 | 20 | 0.723 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 11,978 | 0.120 | 20 | 24 | fits | 23,227 | 20 | 0.739 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 16,519 | 0.165 | 20 | 24 | fits | 23,357 | 20 | 0.746 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 12,327 | 0.123 | 20 | 24 | fits | 23,655 | 20 | 0.733 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 13,037 | 0.130 | 20 | 24 | fits | 24,063 | 20 | 0.747 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 17,021 | 0.170 | 20 | 24 | fits | 23,357 | 20 | 0.750 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 12,087 | 0.121 | 20 | 24 | fits | 23,062 | 20 | 0.748 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 16,578 | 0.166 | 20 | 24 | fits | 22,902 | 20 | 0.762 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 14,295 | 0.143 | 20 | 24 | fits | 25,322 | 21 | 0.654 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 16,133 | 0.161 | 20 | 24 | fits | 22,437 | 20 | 0.783 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 11,053 | 0.111 | 20 | 24 | fits | 22,028 | 20 | 0.769 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 16,673 | 0.167 | 20 | 24 | fits | 23,240 | 20 | 0.754 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 17,143 | 0.171 | 20 | 24 | fits | 23,776 | 20 | 0.751 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 11,760 | 0.118 | 20 | 24 | fits | 22,816 | 20 | 0.748 |
| get_configuration | `aecp.get_configuration.if0` | 14,798 | 0.148 | 20 | 24 | fits | 20,997 | 20 | 0.774 |
| entity_available | `aecp.entity_available.if0` | 9,845 | 0.098 | 20 | 24 | fits | 20,300 | 20 | 0.762 |
| get_name | `aecp.get_name.if0` | 17,244 | 0.172 | 20 | 24 | fits | 23,705 | 20 | 0.783 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 13,206 | 0.132 | 20 | 24 | fits | 24,246 | 25 | 0.739 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 18,621 | 0.186 | 20 | 24 | fits | 25,004 | 29 | 0.773 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 14,501 | 0.145 | 20 | 24 | fits | 28,374 | 29 | 0.737 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 9,551 | 0.096 | 20 | 24 | fits | 19,926 | 20 | 0.739 |
| set_name | `aecp.set_name.if0` | 24,796 | 0.248 | 20 | 24 | fits | 38,466 | 42 | 0.748 |
| lock_entity | `aecp.lock_entity.if0` | 18,982 | 0.190 | 20 | 24 | fits | 28,493 | 33 | 0.773 |
| unlock_entity | `aecp.unlock_entity.if0` | 25,517 | 0.255 | 20 | 24 | fits | 28,743 | 32 | 0.782 |
| LINK_UP | `fixture.link_up.if0` | 2,428 | 0.024 | 20 | 200 | fits | 22,299 | 43 (11) | 0.719 |
| malformed MRPDU discard | `fixture.malformed.if0` | 15,871 | 0.159 | 20 | 20 | fits | 15,936 | 12 | 0.784 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 27,533 | 0.275 | 20 | 24 | fits | 38,440 | 42 | 0.746 |
| LINK_DOWN | `fixture.link_down.if0` | 2,395 | 0.024 | 20 | 200 | fits | 22,032 | 23 (9) | 0.781 |
| BIND_RX | `fixture.bind_rx.if0` | 18,485 | 0.185 | 20 | 20 | fits | 37,011 | 26 (77) | 0.807 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 18,482 | 0.185 | 20 | 20 | fits | 32,766 | 35 (35) | 0.770 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 13,195 | 0.132 | 20 | 20 | fits | 20,165 | 13 (29) | 0.798 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 72,222 | 0.722 | 20 | 200 | fits | 72,325 | 51 | 0.778 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 72,222 | 0.722 | 20 | 200 | fits | 72,325 | 51 | 0.778 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 71,952 | 0.720 | 20 | 20 | fits | 72,325 | 51 | 0.778 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 71,952 | 0.720 | 20 | 20 | fits | 72,325 | 51 | 0.778 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 72,157 | 0.722 | 20 | 24 | fits | 72,325 | 51 | 0.778 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 72,157 | 0.722 | 20 | 24 | fits | 72,325 | 51 | 0.778 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 72,092 | 0.721 | 20 | 50 | fits | 72,325 | 51 | 0.778 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 72,092 | 0.721 | 20 | 50 | fits | 72,325 | 51 | 0.778 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 72,027 | 0.720 | 20 | 20 | fits | 72,325 | 51 | 0.778 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 72,027 | 0.720 | 20 | 20 | fits | 72,325 | 51 | 0.778 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
