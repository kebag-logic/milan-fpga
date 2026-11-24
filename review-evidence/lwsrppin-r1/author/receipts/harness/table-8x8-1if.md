### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 87 paths and 7 of 963 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.191 (0.429) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.084 (0.245) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.088 (0.295) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.171 (0.560) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.093 (0.258) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.090 (0.258) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.090 (0.252) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.092 (0.260) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.097 (0.328) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.193 (0.572) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.195 (0.593) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.216 (0.589) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.184 (0.568) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.203 (0.634) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.166 (0.566) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.144 (0.403) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.041 (0.178) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.019 (0.165) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.021 (0.309) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.021 (0.320) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.018 (0.019) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.082 (0.407) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.215 (0.558) | fits | 0 aecp | 1 | 0 |
| get_as_path, refused ENTITY_MISBEHAVING | 0 | `aecp.get_as_path.if0` (aecp) | 0.107 (0.283) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.211 (0.558) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.184 (0.535) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.255 (0.606) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.205 (0.552) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR held for a token (#917) | 0 | `aecp.held.read_descriptor.if0` (aecp-held) | 5.194 (5.371) | fits | 16 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.236 (0.678) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.177 (0.521) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.273 (0.622) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.206 (0.554) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.199 (0.543) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.236 (0.583) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.284 (0.637) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.199 (0.545) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.232 (0.580) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.236 (0.583) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.200 (0.548) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.242 (0.591) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.205 (0.552) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.239 (0.589) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.208 (0.555) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.235 (0.583) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.173 (0.522) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.304 (0.754) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.225 (0.576) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.244 (0.637) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.364 (0.674) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.542 (0.923) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.374 (0.680) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.595 (0.945) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.518 (0.837) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.511 (0.826) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.355 (4.725) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-0.adp_available.if0` (backlog-adp@verify-0) | 4.617 (6.118) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.157 (0.547) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.608 (2.057) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.201 (63.417) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.027 (64.245) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.324 (0.462) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 2.842 | fits | 11 acmp | 4 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 3.020 | fits | 7 adp | 4 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-flight.held.aecp.if0` (save-flight) | 3.701 | fits | 14 aecp | 4 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 2.571 | fits | 6 maap | 4 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 7.246 | fits | 31 srp | 4 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.144 (0.334) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.122 (0.278) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.144 (0.320) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.125 (0.334) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.182 (0.516) | fits | 0 events | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-burst.mrpdu.periodic.if0` (save-burst) | 1.682 | fits | 0 srp | 10 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.127 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.212 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.171 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 5.281 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.aecp.first.if0` (backlog-adp@verify-0) | 2.376 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.567 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.153 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.maap.last.if0` (backlog-adp@program-aged2-7) | 5.318 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-6.service.srp.first.if0` (backlog-adp@program-aged2-6) | 6.640 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-4.service.srp.last.if0` (backlog-adp@verify-aged2-4) | 8.923 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.731 (0.779) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.412 (0.412) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.222 (0.223) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.793 (0.868) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 10.935 | 7 | 149,057 (1.491) | yes | - |
| backlog-adp@blank-1 | 0 | 12.884 | 9 | 150,174 (1.502) | yes | - |
| backlog-adp@blank-2 | 0 | 12.759 | 9 | 150,174 (1.502) | yes | - |
| backlog-adp@blank-3 | 0 | 12.634 | 9 | 150,174 (1.502) | yes | - |
| backlog-adp@blank-4 | 0 | 12.509 | 9 | 150,174 (1.502) | yes | - |
| backlog-adp@blank-5 | 0 | 12.384 | 9 | 150,174 (1.502) | yes | - |
| backlog-adp@blank-6 | 0 | 12.259 | 9 | 150,174 (1.502) | yes | - |
| backlog-adp@blank-7 | 0 | 12.134 | 9 | 150,174 (1.502) | yes | - |
| backlog-adp@program-0 | 0 | 9.763 | 7 | 151,954 (1.520) | yes | - |
| backlog-adp@program-1 | 0 | 9.513 | 7 | 151,954 (1.520) | yes | - |
| backlog-adp@program-2 | 0 | 10.218 | 7 | 150,645 (1.506) | yes | - |
| backlog-adp@program-3 | 0 | 10.164 | 7 | 151,848 (1.518) | yes | - |
| backlog-adp@program-4 | 0 | 9.914 | 7 | 151,848 (1.518) | yes | - |
| backlog-adp@program-5 | 1 | 9.462 | 6 | 157,448 (1.574) | yes | - |
| backlog-adp@program-6 | 0 | 9.458 | 6 | 157,448 (1.574) | yes | - |
| backlog-adp@program-7 | 0 | 11.876 | 9 | 148,812 (1.488) | yes | - |
| backlog-adp@verify-0 | 0 | 13.781 | 9 | 148,688 (1.487) | yes | - |
| backlog-adp@verify-1 | 0 | 13.656 | 9 | 148,688 (1.487) | yes | - |
| backlog-adp@verify-2 | 0 | 13.531 | 9 | 148,688 (1.487) | yes | - |
| backlog-adp@verify-3 | 0 | 13.406 | 9 | 148,688 (1.487) | yes | - |
| backlog-adp@verify-4 | 0 | 13.281 | 9 | 148,688 (1.487) | yes | - |
| backlog-adp@verify-5 | 0 | 13.156 | 9 | 148,688 (1.487) | yes | - |
| backlog-adp@verify-6 | 0 | 13.031 | 9 | 148,688 (1.487) | yes | - |
| backlog-adp@verify-7 | 0 | 12.906 | 9 | 148,688 (1.487) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 12.859 | 8 | 153,734 (1.537) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 10.913 | 8 | 155,073 (1.551) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 10.831 | 7 | 155,980 (1.560) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 13.703 | 9 | 155,236 (1.552) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 12.778 | 9 | 157,659 (1.577) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 11.601 | 7 | 155,240 (1.552) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 11.612 | 7 | 155,995 (1.560) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 15.694 | 10 | 151,266 (1.513) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 12.957 | 9 | 155,240 (1.552) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 11.945 | 8 | 155,995 (1.560) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 10.899 | 7 | 155,240 (1.552) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 10.926 | 7 | 155,995 (1.560) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 10.766 | 6 | 149,288 (1.493) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 12.871 | 9 | 157,735 (1.577) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 11.053 | 9 | 154,124 (1.541) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 10.796 | 7 | 150,940 (1.509) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.849 | 9 | 147,873 (1.479) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 10.826 | 9 | 157,374 (1.574) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 10.155 | 7 | 148,523 (1.485) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 10.279 | 7 | 156,220 (1.562) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 10.284 | 7 | 155,465 (1.555) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 10.328 | 7 | 156,220 (1.562) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 10.314 | 7 | 154,325 (1.543) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 10.578 | 9 | 152,339 (1.523) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 10.238 | 7 | 156,220 (1.562) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.461 | 8 | 154,310 (1.543) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 10.743 | 9 | 147,800 (1.478) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 10.464 | 8 | 154,214 (1.542) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 10.210 | 6 | 157,114 (1.571) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 10.214 | 7 | 154,214 (1.542) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 10.216 | 7 | 148,579 (1.486) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 10.229 | 7 | 151,540 (1.515) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 12.848 | 8 | 156,220 (1.562) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 14.028 | 10 | 148,675 (1.487) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 11.961 | 9 | 157,784 (1.578) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 11.653 | 7 | 148,579 (1.486) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 11.731 | 7 | 156,276 (1.563) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 11.722 | 7 | 154,182 (1.542) | yes | - |
| backlog-adp@verify-aged2-6 | 1 | 11.576 | 6 | 157,114 (1.571) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 14.827 | 10 | 150,360 (1.504) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 12.962 | 8 | 154,214 (1.542) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 11.911 | 8 | 156,276 (1.563) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 10.881 | 7 | 154,366 (1.544) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 10.873 | 7 | 148,771 (1.488) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 13.016 | 9 | 157,696 (1.577) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 11.014 | 8 | 148,523 (1.485) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 10.931 | 7 | 156,220 (1.562) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 10.928 | 7 | 151,491 (1.515) | yes | - |
| backlog | 0 | 5.787 | 7 | 152,229 (1.522) | yes | - |
| backlog-adp | 0 | 8.602 | 7 | 154,859 (1.549) | yes | - |
| backlog-adp-refill | 0 | 40.869 | 21 | 154,859 (1.549) | yes | - |
| backlog-owed | 0 | 65.095 | 23 | 143,822 (1.438) | yes | - |
| fixture | 0 | 1.379 | 2 | 86,983 (0.870) | yes | - |

Composed maximum over the 4 backlog windows: 154,859 CPU cycles (1.549 ms), backlog-adp.
Over the windows that released their whole load only: 154,859 (1.549 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 150992 | 0 | 48,672 (0.487) | fits |
| save-burst | 2738 | 0 | 154,101 (1.541) | fits |
| save-held | 2916 | 0 | 163,158 (1.632) | fits |
| save-starved | 72547 | 0 | 163,158 (1.632) | fits |
| save-flight | 2501 | 0 | 163,158 (1.632) | fits |
| acmp-notk | 3604 | 0 | 110,183 (1.102) | fits |
| backlog-adp@blank-0 | 470 | 0 | 149,057 (1.491) | fits |
| backlog-adp@blank-1 | 472 | 0 | 150,174 (1.502) | fits |
| backlog-adp@blank-2 | 472 | 0 | 150,174 (1.502) | fits |
| backlog-adp@blank-3 | 472 | 0 | 150,174 (1.502) | fits |
| backlog-adp@blank-4 | 472 | 0 | 150,174 (1.502) | fits |
| backlog-adp@blank-5 | 472 | 0 | 150,174 (1.502) | fits |
| backlog-adp@blank-6 | 472 | 0 | 150,174 (1.502) | fits |
| backlog-adp@blank-7 | 472 | 0 | 150,174 (1.502) | fits |
| backlog-adp@program-0 | 504 | 0 | 151,954 (1.520) | fits |
| backlog-adp@program-1 | 504 | 0 | 151,954 (1.520) | fits |
| backlog-adp@program-2 | 504 | 0 | 150,645 (1.506) | fits |
| backlog-adp@program-3 | 504 | 0 | 151,848 (1.518) | fits |
| backlog-adp@program-4 | 504 | 0 | 151,848 (1.518) | fits |
| backlog-adp@program-5 | 504 | 0 | 157,448 (1.574) | fits |
| backlog-adp@program-6 | 504 | 0 | 157,448 (1.574) | fits |
| backlog-adp@program-7 | 507 | 0 | 148,812 (1.488) | fits |
| backlog-adp@verify-0 | 527 | 0 | 148,688 (1.487) | fits |
| backlog-adp@verify-1 | 527 | 0 | 148,688 (1.487) | fits |
| backlog-adp@verify-2 | 527 | 0 | 148,688 (1.487) | fits |
| backlog-adp@verify-3 | 527 | 0 | 148,688 (1.487) | fits |
| backlog-adp@verify-4 | 527 | 0 | 148,688 (1.487) | fits |
| backlog-adp@verify-5 | 527 | 0 | 148,688 (1.487) | fits |
| backlog-adp@verify-6 | 527 | 0 | 148,688 (1.487) | fits |
| backlog-adp@verify-7 | 527 | 0 | 148,688 (1.487) | fits |
| backlog-adp@blank-aged2-0 | 762 | 0 | 153,734 (1.537) | fits |
| backlog-adp@blank-aged2-1 | 770 | 0 | 155,073 (1.551) | fits |
| backlog-adp@blank-aged2-2 | 777 | 0 | 155,980 (1.560) | fits |
| backlog-adp@blank-aged2-3 | 786 | 0 | 155,236 (1.552) | fits |
| backlog-adp@blank-aged2-4 | 794 | 0 | 157,659 (1.577) | fits |
| backlog-adp@blank-aged2-5 | 800 | 0 | 155,240 (1.552) | fits |
| backlog-adp@blank-aged2-6 | 808 | 0 | 155,995 (1.560) | fits |
| backlog-adp@blank-aged2-7 | 819 | 0 | 151,266 (1.513) | fits |
| backlog-adp@blank-aged1-0 | 700 | 0 | 155,240 (1.552) | fits |
| backlog-adp@blank-aged1-1 | 707 | 0 | 155,995 (1.560) | fits |
| backlog-adp@blank-aged1-2 | 714 | 0 | 155,240 (1.552) | fits |
| backlog-adp@blank-aged1-3 | 722 | 0 | 155,995 (1.560) | fits |
| backlog-adp@blank-aged1-4 | 729 | 0 | 149,288 (1.493) | fits |
| backlog-adp@blank-aged1-5 | 739 | 0 | 157,735 (1.577) | fits |
| backlog-adp@blank-aged1-6 | 747 | 0 | 154,124 (1.541) | fits |
| backlog-adp@blank-aged1-7 | 753 | 0 | 150,940 (1.509) | fits |
| backlog-adp@program-aged2-0 | 780 | 0 | 147,873 (1.479) | fits |
| backlog-adp@program-aged2-1 | 788 | 0 | 157,374 (1.574) | fits |
| backlog-adp@program-aged2-2 | 794 | 0 | 148,523 (1.485) | fits |
| backlog-adp@program-aged2-3 | 801 | 0 | 156,220 (1.562) | fits |
| backlog-adp@program-aged2-4 | 809 | 0 | 155,465 (1.555) | fits |
| backlog-adp@program-aged2-5 | 817 | 0 | 156,220 (1.562) | fits |
| backlog-adp@program-aged2-6 | 825 | 0 | 154,325 (1.543) | fits |
| backlog-adp@program-aged2-7 | 835 | 0 | 152,339 (1.523) | fits |
| backlog-adp@program-aged1-0 | 715 | 0 | 156,220 (1.562) | fits |
| backlog-adp@program-aged1-1 | 724 | 0 | 154,310 (1.543) | fits |
| backlog-adp@program-aged1-2 | 733 | 0 | 147,800 (1.478) | fits |
| backlog-adp@program-aged1-3 | 740 | 0 | 154,214 (1.542) | fits |
| backlog-adp@program-aged1-4 | 746 | 0 | 157,114 (1.571) | fits |
| backlog-adp@program-aged1-5 | 754 | 0 | 154,214 (1.542) | fits |
| backlog-adp@program-aged1-6 | 762 | 0 | 148,579 (1.486) | fits |
| backlog-adp@program-aged1-7 | 770 | 0 | 151,540 (1.515) | fits |
| backlog-adp@verify-aged2-0 | 821 | 0 | 156,220 (1.562) | fits |
| backlog-adp@verify-aged2-1 | 831 | 0 | 148,675 (1.487) | fits |
| backlog-adp@verify-aged2-2 | 838 | 0 | 157,784 (1.578) | fits |
| backlog-adp@verify-aged2-3 | 844 | 0 | 148,579 (1.486) | fits |
| backlog-adp@verify-aged2-4 | 852 | 0 | 156,276 (1.563) | fits |
| backlog-adp@verify-aged2-5 | 860 | 0 | 154,182 (1.542) | fits |
| backlog-adp@verify-aged2-6 | 867 | 0 | 157,114 (1.571) | fits |
| backlog-adp@verify-aged2-7 | 878 | 0 | 150,360 (1.504) | fits |
| backlog-adp@verify-aged1-0 | 759 | 0 | 154,214 (1.542) | fits |
| backlog-adp@verify-aged1-1 | 766 | 0 | 156,276 (1.563) | fits |
| backlog-adp@verify-aged1-2 | 773 | 0 | 154,366 (1.544) | fits |
| backlog-adp@verify-aged1-3 | 781 | 0 | 148,771 (1.488) | fits |
| backlog-adp@verify-aged1-4 | 791 | 0 | 157,696 (1.577) | fits |
| backlog-adp@verify-aged1-5 | 798 | 0 | 148,523 (1.485) | fits |
| backlog-adp@verify-aged1-6 | 805 | 0 | 156,220 (1.562) | fits |
| backlog-adp@verify-aged1-7 | 813 | 0 | 151,491 (1.515) | fits |
| adp-advertise | 598 | 0 | 33,387 (0.334) | fits |
| acmp-noresp | 2021 | 0 | 110,114 (1.101) | fits |
| save | 610 | 0 | 81,183 (0.812) | fits |
| srp | 290 | 0 | 43,613 (0.436) | fits |
| backlog | 286 | 0 | 152,229 (1.522) | fits |
| backlog-adp | 309 | 0 | 154,859 (1.549) | fits |
| backlog-adp-refill | 323 | 0 | 154,859 (1.549) | fits |
| backlog-owed | 309 | 0 | 150,343 (1.503) | fits |
| acmp-disc | 936 | 0 | 110,114 (1.101) | fits |
| maap | 184 | 0 | 33,387 (0.334) | fits |
| adp-link | 89 | 0 | 42,988 (0.430) | fits |
| adp-gm | 88 | 0 | 32,023 (0.320) | fits |
| adp-discover | 88 | 0 | 32,023 (0.320) | fits |
| control | 88 | 0 | 32,023 (0.320) | fits |
| aecp-fanout | 110 | 0 | 57,466 (0.575) | fits |
| acmp-cmd | 88 | 0 | 42,885 (0.429) | fits |
| aecp | 114 | 0 | 44,655 (0.447) | fits |
| aecp-held | 105 | 0 | 35,724 (0.357) | fits |
| datapath-events | 119 | 0 | 32,023 (0.320) | fits |
| fixture | 161 | 0 | 86,983 (0.870) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 8.070 (20) | 11.930 |
| backlog-adp@blank-aged2-1 | 2 | none | +8.318 ms, 76,092 (0.761 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 8.085 (20) | 11.915 |
| backlog-adp@blank-aged2-2 | 2 | none | +8.221 ms, 76,563 (0.766 ms), read-back | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 8.183 (20) | 11.817 |
| backlog-adp@blank-aged2-3 | 2 | +7.248 ms, 76,713 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 8.817 (20) | 11.183 |
| backlog-adp@blank-aged2-4 | 2 | +5.962 ms, 76,713 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 8.798 (20) | 11.202 |
| backlog-adp@blank-aged2-5 | 2 | +5.845 ms, 76,713 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 8.823 (20) | 11.177 |
| backlog-adp@blank-aged2-6 | 2 | +4.367 ms, 76,468 (0.765 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 8.835 (20) | 11.165 |
| backlog-adp@blank-aged2-7 | 2 | +3.055 ms, 76,309 (0.763 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 8.804 (20) | 11.196 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 7.881 (20) | 12.119 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 8.063 (20) | 11.937 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 8.119 (20) | 11.881 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 8.145 (20) | 11.855 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 7.978 (20) | 12.022 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 7.970 (20) | 12.030 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 7.983 (20) | 12.017 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 8.014 (20) | 11.986 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 7.999 (20) | 12.001 |
| backlog-adp@program-aged2-1 | 2 | none | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 7.958 (20) | 12.042 |
| backlog-adp@program-aged2-2 | 2 | none | +8.165 ms, 80,813 (0.808 ms), issue | `backlog-adp@program-aged2-2.service.srp.last.if0` | 8.127 (20) | 11.873 |
| backlog-adp@program-aged2-3 | 2 | +7.250 ms, 80,873 (0.809 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 8.865 (20) | 11.135 |
| backlog-adp@program-aged2-4 | 2 | +5.899 ms, 80,814 (0.808 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 8.866 (20) | 11.134 |
| backlog-adp@program-aged2-5 | 2 | +5.943 ms, 80,814 (0.808 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 8.910 (20) | 11.090 |
| backlog-adp@program-aged2-6 | 2 | +4.535 ms, 80,784 (0.808 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 8.888 (20) | 11.112 |
| backlog-adp@program-aged2-7 | 2 | +3.188 ms, 80,703 (0.807 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 8.873 (20) | 11.127 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 8.067 (20) | 11.933 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 8.090 (20) | 11.910 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 8.061 (20) | 11.939 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 8.011 (20) | 11.989 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 8.040 (20) | 11.960 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 8.044 (20) | 11.956 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 8.042 (20) | 11.958 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 8.050 (20) | 11.950 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 8.011 (20) | 11.989 |
| backlog-adp@verify-aged2-1 | 2 | none | none | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 7.998 (20) | 12.002 |
| backlog-adp@verify-aged2-2 | 2 | none | +8.111 ms, 77,334 (0.773 ms), read-back | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 8.074 (20) | 11.926 |
| backlog-adp@verify-aged2-3 | 2 | +6.949 ms, 77,484 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 8.728 (20) | 11.272 |
| backlog-adp@verify-aged2-4 | 2 | +5.936 ms, 77,484 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 8.923 (20) | 11.077 |
| backlog-adp@verify-aged2-5 | 2 | +4.440 ms, 77,239 (0.772 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 8.916 (20) | 11.084 |
| backlog-adp@verify-aged2-6 | 2 | none | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 8.767 (20) | 11.233 |
| backlog-adp@verify-aged2-7 | 2 | none | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 8.772 (20) | 11.228 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 8.125 (20) | 11.875 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 7.992 (20) | 12.008 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 8.066 (20) | 11.934 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 8.057 (20) | 11.943 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 8.076 (20) | 11.924 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 7.920 (20) | 12.080 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 8.121 (20) | 11.879 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 8.119 (20) | 11.881 |

Least margin over the aged windows: 11.077 ms, `backlog-adp@verify-aged2-4.service.srp.last.if0` at 8.923 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 22829.538 | 22,870 | 382 | 2 | 31.388 | yes | within |
| save-held | 1325.445 | 12,470 | 382 | - | 42.044 | no | within |
| save-starved | 12447.867 | 12,470 | 382 | - | 32.858 | yes | within |
| save | 1290.277 | 12,470 | 382 | - | 98.970 | no | within |

Names from their response to durable (save_burst.py; #920, #665's ruling of 2026-11-15, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-burst | 107 | 1335.752 (0) | 5,000 | 7 | - | - | sequence 7, 0 missing | within |
| save-flight | 1 | 610.773 (0) | 5,000 | 2 | - | - | 59 steps (want 59), 22.567 ms | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1080 | 81,905 (0.819) | 78,661 (0.787) |
| save-burst | 4088 | 98,307 (0.983) | 78,265 (0.783) |
| save-held | 1912 | 95,008 (0.950) | 78,038 (0.780) |
| save-starved | 698 | 82,758 (0.828) | 78,964 (0.790) |
| save-flight | 2068 | 97,836 (0.978) | 78,075 (0.781) |
| acmp-notk | 1416 | 110,183 (1.102) | 77,973 (0.780) |
| backlog-adp@blank-0 | 381 | 93,258 (0.933) | 75,779 (0.758) |
| backlog-adp@blank-1 | 383 | 93,792 (0.938) | 75,779 (0.758) |
| backlog-adp@blank-2 | 383 | 93,792 (0.938) | 75,779 (0.758) |
| backlog-adp@blank-3 | 383 | 93,792 (0.938) | 75,779 (0.758) |
| backlog-adp@blank-4 | 383 | 93,792 (0.938) | 75,779 (0.758) |
| backlog-adp@blank-5 | 383 | 93,792 (0.938) | 75,779 (0.758) |
| backlog-adp@blank-6 | 383 | 93,792 (0.938) | 75,779 (0.758) |
| backlog-adp@blank-7 | 383 | 93,792 (0.938) | 75,779 (0.758) |
| backlog-adp@program-0 | 491 | 97,623 (0.976) | 77,906 (0.779) |
| backlog-adp@program-1 | 491 | 97,623 (0.976) | 77,906 (0.779) |
| backlog-adp@program-2 | 492 | 97,623 (0.976) | 78,523 (0.785) |
| backlog-adp@program-3 | 493 | 97,623 (0.976) | 77,906 (0.779) |
| backlog-adp@program-4 | 493 | 97,623 (0.976) | 77,906 (0.779) |
| backlog-adp@program-5 | 493 | 97,623 (0.976) | 77,906 (0.779) |
| backlog-adp@program-6 | 493 | 97,623 (0.976) | 77,906 (0.779) |
| backlog-adp@program-7 | 497 | 102,365 (1.024) | 78,552 (0.786) |
| backlog-adp@verify-0 | 600 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-1 | 600 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-2 | 600 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-3 | 600 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-4 | 600 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-5 | 600 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-6 | 600 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-7 | 600 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@blank-aged2-0 | 381 | 92,662 (0.927) | 75,938 (0.759) |
| backlog-adp@blank-aged2-1 | 379 | 92,500 (0.925) | 75,604 (0.756) |
| backlog-adp@blank-aged2-2 | 379 | 93,503 (0.935) | 75,729 (0.757) |
| backlog-adp@blank-aged2-3 | 382 | 93,581 (0.936) | 75,878 (0.759) |
| backlog-adp@blank-aged2-4 | 381 | 93,636 (0.936) | 75,878 (0.759) |
| backlog-adp@blank-aged2-5 | 380 | 92,406 (0.924) | 75,878 (0.759) |
| backlog-adp@blank-aged2-6 | 380 | 92,431 (0.924) | 75,694 (0.757) |
| backlog-adp@blank-aged2-7 | 384 | 93,546 (0.935) | 75,808 (0.758) |
| backlog-adp@blank-aged1-0 | 381 | 91,529 (0.915) | 75,903 (0.759) |
| backlog-adp@blank-aged1-1 | 380 | 92,645 (0.926) | 75,938 (0.759) |
| backlog-adp@blank-aged1-2 | 379 | 92,662 (0.927) | 75,938 (0.759) |
| backlog-adp@blank-aged1-3 | 379 | 92,685 (0.927) | 75,938 (0.759) |
| backlog-adp@blank-aged1-4 | 379 | 93,277 (0.933) | 75,938 (0.759) |
| backlog-adp@blank-aged1-5 | 381 | 93,713 (0.937) | 75,938 (0.759) |
| backlog-adp@blank-aged1-6 | 379 | 91,529 (0.915) | 75,903 (0.759) |
| backlog-adp@blank-aged1-7 | 379 | 92,809 (0.928) | 75,938 (0.759) |
| backlog-adp@program-aged2-0 | 491 | 102,487 (1.025) | 78,523 (0.785) |
| backlog-adp@program-aged2-1 | 489 | 97,623 (0.976) | 78,523 (0.785) |
| backlog-adp@program-aged2-2 | 488 | 97,623 (0.976) | 78,560 (0.786) |
| backlog-adp@program-aged2-3 | 489 | 97,623 (0.976) | 78,709 (0.787) |
| backlog-adp@program-aged2-4 | 489 | 97,623 (0.976) | 78,560 (0.786) |
| backlog-adp@program-aged2-5 | 489 | 97,623 (0.976) | 78,560 (0.786) |
| backlog-adp@program-aged2-6 | 489 | 97,623 (0.976) | 78,584 (0.786) |
| backlog-adp@program-aged2-7 | 489 | 97,623 (0.976) | 78,464 (0.785) |
| backlog-adp@program-aged1-0 | 488 | 97,623 (0.976) | 78,523 (0.785) |
| backlog-adp@program-aged1-1 | 488 | 97,623 (0.976) | 78,632 (0.786) |
| backlog-adp@program-aged1-2 | 489 | 97,623 (0.976) | 78,523 (0.785) |
| backlog-adp@program-aged1-3 | 488 | 97,623 (0.976) | 78,488 (0.785) |
| backlog-adp@program-aged1-4 | 488 | 97,623 (0.976) | 78,523 (0.785) |
| backlog-adp@program-aged1-5 | 488 | 97,623 (0.976) | 78,523 (0.785) |
| backlog-adp@program-aged1-6 | 488 | 97,623 (0.976) | 78,523 (0.785) |
| backlog-adp@program-aged1-7 | 488 | 97,623 (0.976) | 78,523 (0.785) |
| backlog-adp@verify-aged2-0 | 599 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-aged2-1 | 600 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-aged2-2 | 598 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-aged2-3 | 598 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-aged2-4 | 598 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-aged2-5 | 598 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-aged2-6 | 598 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-aged2-7 | 601 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-aged1-0 | 599 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-aged1-1 | 598 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-aged1-2 | 597 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-aged1-3 | 597 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-aged1-4 | 599 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-aged1-5 | 597 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-aged1-6 | 597 | 101,573 (1.016) | 78,114 (0.781) |
| backlog-adp@verify-aged1-7 | 597 | 101,573 (1.016) | 78,114 (0.781) |
| adp-advertise | 577 | 24,326 (0.243) | 2,791 (0.028) |
| acmp-noresp | 966 | 110,114 (1.101) | 78,525 (0.785) |
| save | 938 | 95,008 (0.950) | 77,762 (0.778) |
| srp | 271 | 24,326 (0.243) | 2,791 (0.028) |
| backlog | 265 | 24,326 (0.243) | 2,791 (0.028) |
| backlog-adp | 271 | 24,326 (0.243) | 2,791 (0.028) |
| backlog-adp-refill | 274 | 24,326 (0.243) | 2,791 (0.028) |
| backlog-owed | 277 | 24,326 (0.243) | 2,791 (0.028) |
| acmp-disc | 657 | 110,114 (1.101) | 78,114 (0.781) |
| maap | 171 | 24,286 (0.243) | 2,791 (0.028) |
| adp-link | 79 | 24,286 (0.243) | 2,791 (0.028) |
| adp-gm | 79 | 24,286 (0.243) | 2,791 (0.028) |
| adp-discover | 79 | 24,286 (0.243) | 2,791 (0.028) |
| control | 79 | 24,286 (0.243) | 2,791 (0.028) |
| aecp-fanout | 79 | 24,286 (0.243) | 2,791 (0.028) |
| acmp-cmd | 66 | 24,286 (0.243) | 2,791 (0.028) |
| aecp | 80 | 24,286 (0.243) | 2,791 (0.028) |
| aecp-held | 94 | 24,286 (0.243) | 2,791 (0.028) |
| datapath-events | 70 | 24,286 (0.243) | 2,791 (0.028) |
| fixture | 54 | 17,944 (0.179) | 2,355 (0.024) |

Longest pass that carries a step: 110,183 CPU cycles (1.102 ms), acmp-notk; longest step: 78,964 (0.790 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-burst.held.adp.if0` | 214,956 | 2.150 | 20 | 200 | fits | 131,313 | 211 | 0.364 |
| ACMP record, every channel at its refill rate, the longest | `save-burst.held.acmp.if0` | 278,737 | 2.787 | 20 | 20 | fits | 50,150 | 42 | 0.283 |
| AECP record, every channel at its refill rate, the longest | `save-burst.held.aecp.if0` | 288,100 | 2.881 | 20 | 24 | fits | 141,612 | 151 | 0.609 |
| MAAP record, every channel at its refill rate, the longest | `save-burst.held.maap.if0` | 189,112 | 1.891 | 20 | 50 | fits | 151,440 | 224 | 0.260 |
| SRP record, every channel at its refill rate, the longest | `save-burst.held.srp.if0` | 609,622 | 6.096 | 20 | 20 | fits | 132,009 | 58 | 0.628 |
| an MRPDU its join timer owes, the longest | `save-burst.mrpdu.join.if0` | 58,147 | 0.581 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-burst.mrpdu.leaveall.if0` | 58,147 | 0.581 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-burst.mrpdu.periodic.if0` | 168,159 | 1.682 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 301,985 | 3.020 | 20 | 200 | fits | 139,767 | 128 | 0.547 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 284,194 | 2.842 | 20 | 20 | fits | 50,082 | 42 | 0.285 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 284,842 | 2.848 | 20 | 24 | fits | 63,000 | 50 | 0.463 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 194,637 | 1.946 | 20 | 50 | fits | 151,927 | 225 | 0.262 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 714,985 | 7.150 | 20 | 20 | fits | 101,554 | 61 | 0.541 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 52,461 | 0.525 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 57,894 | 0.579 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 159,594 | 1.596 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 296,162 | 2.962 | 20 | 200 | fits | 133,944 | 130 | 0.570 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 236,048 | 2.360 | 20 | 20 | fits | 125,356 | 136 | 0.224 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 265,880 | 2.659 | 20 | 24 | fits | 111,484 | 71 | 0.530 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 236,550 | 2.365 | 20 | 50 | fits | 133,944 | 130 | 0.570 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 724,584 | 7.246 | 20 | 20 | fits | 111,484 | 71 | 0.530 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 52,011 | 0.520 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 49,178 | 0.492 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 161,028 | 1.610 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 301,985 | 3.020 | 20 | 200 | fits | 139,767 | 128 | 0.547 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 242,057 | 2.421 | 20 | 20 | fits | 49,997 | 42 | 0.276 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 370,121 | 3.701 | 20 | 24 | fits | 125,809 | 67 | 0.521 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 257,097 | 2.571 | 20 | 50 | fits | 125,372 | 202 | 0.326 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 704,748 | 7.047 | 20 | 20 | fits | 91,317 | 51 | 0.570 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 96,502 | 0.965 | 49 | 49 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 20,270 | 0.203 | 20 | 20 | fits | 36,261 | 19 (14) | 0.867 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 357,025 | 3.570 | 20 | 20 | fits | 135,264 | 167 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 297,226 | 2.972 | 20 | 200 | fits | 149,057 | 222 | 0.360 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 441,769 | 4.418 | 20 | 200 | fits | 135,264 | 167 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 298,150 | 2.982 | 20 | 20 | fits | 149,057 | 222 | 0.360 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 442,473 | 4.425 | 20 | 20 | fits | 135,264 | 167 | 0.379 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 152,733 | 1.527 | 20 | 24 | fits | 149,036 | 164 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 300,800 | 3.008 | 20 | 24 | fits | 149,057 | 222 | 0.360 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 300,734 | 3.007 | 20 | 50 | fits | 149,057 | 222 | 0.360 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 445,497 | 4.455 | 20 | 50 | fits | 135,264 | 167 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 572,911 | 5.729 | 20 | 20 | fits | 127,480 | 54 | 0.658 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 814,712 | 8.147 | 20 | 20 | fits | 109,787 | 49 | 0.518 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 455,657 | 4.557 | 20 | 20 | fits | 137,342 | 166 | 0.339 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 385,440 | 3.854 | 20 | 200 | fits | 150,174 | 226 | 0.363 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 522,166 | 5.222 | 20 | 200 | fits | 137,342 | 166 | 0.339 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 386,364 | 3.864 | 20 | 20 | fits | 150,174 | 226 | 0.363 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 522,870 | 5.229 | 20 | 20 | fits | 137,342 | 166 | 0.339 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 231,316 | 2.313 | 20 | 24 | fits | 149,203 | 165 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 389,014 | 3.890 | 20 | 24 | fits | 150,174 | 226 | 0.363 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 388,948 | 3.889 | 20 | 50 | fits | 150,174 | 226 | 0.363 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 525,894 | 5.259 | 20 | 50 | fits | 137,342 | 166 | 0.339 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 660,442 | 6.604 | 20 | 20 | fits | 130,698 | 53 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 889,230 | 8.892 | 20 | 20 | fits | 100,684 | 44 | 0.527 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 443,157 | 4.432 | 20 | 20 | fits | 137,342 | 166 | 0.339 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 372,940 | 3.729 | 20 | 200 | fits | 150,174 | 226 | 0.363 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 509,666 | 5.097 | 20 | 200 | fits | 137,342 | 166 | 0.339 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 373,864 | 3.739 | 20 | 20 | fits | 150,174 | 226 | 0.363 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 510,370 | 5.104 | 20 | 20 | fits | 137,342 | 166 | 0.339 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 218,816 | 2.188 | 20 | 24 | fits | 149,203 | 165 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 376,514 | 3.765 | 20 | 24 | fits | 150,174 | 226 | 0.363 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 376,448 | 3.764 | 20 | 50 | fits | 150,174 | 226 | 0.363 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 513,394 | 5.134 | 20 | 50 | fits | 137,342 | 166 | 0.339 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 647,942 | 6.479 | 20 | 20 | fits | 130,698 | 53 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 876,730 | 8.767 | 20 | 20 | fits | 100,684 | 44 | 0.527 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 430,657 | 4.307 | 20 | 20 | fits | 137,342 | 166 | 0.339 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 360,440 | 3.604 | 20 | 200 | fits | 150,174 | 226 | 0.363 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 497,166 | 4.972 | 20 | 200 | fits | 137,342 | 166 | 0.339 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 361,364 | 3.614 | 20 | 20 | fits | 150,174 | 226 | 0.363 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 497,870 | 4.979 | 20 | 20 | fits | 137,342 | 166 | 0.339 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 206,316 | 2.063 | 20 | 24 | fits | 149,203 | 165 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 364,014 | 3.640 | 20 | 24 | fits | 150,174 | 226 | 0.363 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 363,948 | 3.639 | 20 | 50 | fits | 150,174 | 226 | 0.363 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 500,894 | 5.009 | 20 | 50 | fits | 137,342 | 166 | 0.339 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 635,442 | 6.354 | 20 | 20 | fits | 130,698 | 53 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 864,230 | 8.642 | 20 | 20 | fits | 100,684 | 44 | 0.527 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 418,157 | 4.182 | 20 | 20 | fits | 137,342 | 166 | 0.339 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 347,940 | 3.479 | 20 | 200 | fits | 150,174 | 226 | 0.363 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 484,666 | 4.847 | 20 | 200 | fits | 137,342 | 166 | 0.339 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 348,864 | 3.489 | 20 | 20 | fits | 150,174 | 226 | 0.363 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 485,370 | 4.854 | 20 | 20 | fits | 137,342 | 166 | 0.339 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 193,816 | 1.938 | 20 | 24 | fits | 149,203 | 165 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 351,514 | 3.515 | 20 | 24 | fits | 150,174 | 226 | 0.363 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 351,448 | 3.514 | 20 | 50 | fits | 150,174 | 226 | 0.363 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 488,394 | 4.884 | 20 | 50 | fits | 137,342 | 166 | 0.339 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 622,942 | 6.229 | 20 | 20 | fits | 130,698 | 53 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 851,730 | 8.517 | 20 | 20 | fits | 100,684 | 44 | 0.527 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 405,657 | 4.057 | 20 | 20 | fits | 137,342 | 166 | 0.339 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 335,440 | 3.354 | 20 | 200 | fits | 150,174 | 226 | 0.363 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 472,166 | 4.722 | 20 | 200 | fits | 137,342 | 166 | 0.339 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 336,364 | 3.364 | 20 | 20 | fits | 150,174 | 226 | 0.363 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 472,870 | 4.729 | 20 | 20 | fits | 137,342 | 166 | 0.339 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 181,316 | 1.813 | 20 | 24 | fits | 149,203 | 165 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 339,014 | 3.390 | 20 | 24 | fits | 150,174 | 226 | 0.363 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 338,948 | 3.389 | 20 | 50 | fits | 150,174 | 226 | 0.363 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 475,894 | 4.759 | 20 | 50 | fits | 137,342 | 166 | 0.339 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 610,442 | 6.104 | 20 | 20 | fits | 130,698 | 53 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 839,230 | 8.392 | 20 | 20 | fits | 100,684 | 44 | 0.527 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 393,157 | 3.932 | 20 | 20 | fits | 137,342 | 166 | 0.339 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 322,940 | 3.229 | 20 | 200 | fits | 150,174 | 226 | 0.363 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 459,666 | 4.597 | 20 | 200 | fits | 137,342 | 166 | 0.339 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 323,864 | 3.239 | 20 | 20 | fits | 150,174 | 226 | 0.363 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 460,370 | 4.604 | 20 | 20 | fits | 137,342 | 166 | 0.339 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 168,816 | 1.688 | 20 | 24 | fits | 149,203 | 165 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 326,514 | 3.265 | 20 | 24 | fits | 150,174 | 226 | 0.363 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 326,448 | 3.264 | 20 | 50 | fits | 150,174 | 226 | 0.363 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 463,394 | 4.634 | 20 | 50 | fits | 137,342 | 166 | 0.339 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 597,942 | 5.979 | 20 | 20 | fits | 130,698 | 53 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 826,730 | 8.267 | 20 | 20 | fits | 100,684 | 44 | 0.527 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 380,657 | 3.807 | 20 | 20 | fits | 137,342 | 166 | 0.339 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 310,440 | 3.104 | 20 | 200 | fits | 150,174 | 226 | 0.363 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 447,166 | 4.472 | 20 | 200 | fits | 137,342 | 166 | 0.339 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 311,364 | 3.114 | 20 | 20 | fits | 150,174 | 226 | 0.363 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 447,870 | 4.479 | 20 | 20 | fits | 137,342 | 166 | 0.339 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 156,316 | 1.563 | 20 | 24 | fits | 149,203 | 165 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 314,014 | 3.140 | 20 | 24 | fits | 150,174 | 226 | 0.363 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 313,948 | 3.139 | 20 | 50 | fits | 150,174 | 226 | 0.363 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 450,894 | 4.509 | 20 | 50 | fits | 137,342 | 166 | 0.339 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 585,442 | 5.854 | 20 | 20 | fits | 130,698 | 53 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 814,230 | 8.142 | 20 | 20 | fits | 100,684 | 44 | 0.527 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 415,115 | 4.151 | 20 | 20 | fits | 135,833 | 169 | 0.364 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 329,129 | 3.291 | 20 | 200 | fits | 151,954 | 223 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 474,053 | 4.741 | 20 | 200 | fits | 135,833 | 169 | 0.364 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 330,053 | 3.301 | 20 | 20 | fits | 151,954 | 223 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 474,757 | 4.748 | 20 | 20 | fits | 135,833 | 169 | 0.364 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 181,739 | 1.817 | 20 | 24 | fits | 149,185 | 164 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 332,703 | 3.327 | 20 | 24 | fits | 151,954 | 223 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 332,637 | 3.326 | 20 | 50 | fits | 151,954 | 223 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 477,781 | 4.778 | 20 | 50 | fits | 135,833 | 169 | 0.364 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 608,714 | 6.087 | 20 | 20 | fits | 130,999 | 52 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 833,705 | 8.337 | 20 | 20 | fits | 100,606 | 44 | 0.527 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 390,115 | 3.901 | 20 | 20 | fits | 135,833 | 169 | 0.364 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 304,129 | 3.041 | 20 | 200 | fits | 151,954 | 223 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 449,053 | 4.491 | 20 | 200 | fits | 135,833 | 169 | 0.364 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 305,053 | 3.051 | 20 | 20 | fits | 151,954 | 223 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 449,757 | 4.498 | 20 | 20 | fits | 135,833 | 169 | 0.364 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 156,739 | 1.567 | 20 | 24 | fits | 149,185 | 164 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 307,703 | 3.077 | 20 | 24 | fits | 151,954 | 223 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 307,637 | 3.076 | 20 | 50 | fits | 151,954 | 223 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 452,781 | 4.528 | 20 | 50 | fits | 135,833 | 169 | 0.364 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 583,714 | 5.837 | 20 | 20 | fits | 130,999 | 52 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 808,705 | 8.087 | 20 | 20 | fits | 100,606 | 44 | 0.527 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 387,029 | 3.870 | 20 | 20 | fits | 137,390 | 172 | 0.359 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 298,497 | 2.985 | 20 | 200 | fits | 150,645 | 219 | 0.378 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 444,978 | 4.450 | 20 | 200 | fits | 137,390 | 172 | 0.359 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 299,421 | 2.994 | 20 | 20 | fits | 150,645 | 219 | 0.378 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 445,682 | 4.457 | 20 | 20 | fits | 137,390 | 172 | 0.359 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 152,416 | 1.524 | 20 | 24 | fits | 149,172 | 164 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 302,071 | 3.021 | 20 | 24 | fits | 150,645 | 219 | 0.378 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 302,005 | 3.020 | 20 | 50 | fits | 150,645 | 219 | 0.378 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 448,706 | 4.487 | 20 | 50 | fits | 137,390 | 172 | 0.359 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 579,468 | 5.795 | 20 | 20 | fits | 130,828 | 52 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 804,529 | 8.045 | 20 | 20 | fits | 100,608 | 44 | 0.527 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 448,188 | 4.482 | 20 | 20 | fits | 136,242 | 169 | 0.369 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 369,530 | 3.695 | 20 | 200 | fits | 151,848 | 223 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 514,588 | 5.146 | 20 | 200 | fits | 136,242 | 169 | 0.369 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 370,454 | 3.705 | 20 | 20 | fits | 151,848 | 223 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 515,292 | 5.153 | 20 | 20 | fits | 136,242 | 169 | 0.369 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 222,246 | 2.222 | 20 | 24 | fits | 149,199 | 164 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 373,104 | 3.731 | 20 | 24 | fits | 151,848 | 223 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 373,038 | 3.730 | 20 | 50 | fits | 151,848 | 223 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 518,316 | 5.183 | 20 | 50 | fits | 136,242 | 169 | 0.369 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 648,999 | 6.490 | 20 | 20 | fits | 130,749 | 52 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 874,042 | 8.740 | 20 | 20 | fits | 100,608 | 44 | 0.527 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 423,188 | 4.232 | 20 | 20 | fits | 136,242 | 169 | 0.369 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 344,530 | 3.445 | 20 | 200 | fits | 151,848 | 223 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 489,588 | 4.896 | 20 | 200 | fits | 136,242 | 169 | 0.369 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 345,454 | 3.455 | 20 | 20 | fits | 151,848 | 223 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 490,292 | 4.903 | 20 | 20 | fits | 136,242 | 169 | 0.369 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 197,246 | 1.972 | 20 | 24 | fits | 149,199 | 164 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 348,104 | 3.481 | 20 | 24 | fits | 151,848 | 223 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 348,038 | 3.480 | 20 | 50 | fits | 151,848 | 223 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 493,316 | 4.933 | 20 | 50 | fits | 136,242 | 169 | 0.369 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 623,999 | 6.240 | 20 | 20 | fits | 130,749 | 52 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 849,042 | 8.490 | 20 | 20 | fits | 100,608 | 44 | 0.527 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 372,545 | 3.725 | 20 | 20 | fits | 151,764 | 152 | 0.495 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 303,007 | 3.030 | 20 | 200 | fits | 157,448 | 245 | 0.353 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 463,843 | 4.638 | 20 | 200 | fits | 151,764 | 152 | 0.495 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 303,931 | 3.039 | 20 | 20 | fits | 157,448 | 245 | 0.353 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 464,547 | 4.645 | 20 | 20 | fits | 151,764 | 152 | 0.495 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 150,123 | 1.501 | 20 | 24 | fits | 151,717 | 164 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 306,581 | 3.066 | 20 | 24 | fits | 157,448 | 245 | 0.353 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 306,515 | 3.065 | 20 | 50 | fits | 157,448 | 245 | 0.353 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 467,571 | 4.676 | 20 | 50 | fits | 151,764 | 152 | 0.495 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 467,505 | 4.675 | 20 | 20 | fits | 151,764 | 152 | 0.495 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 803,955 | 8.040 | 20 | 20 | fits | 83,295 | 36 | 0.570 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 372,186 | 3.722 | 20 | 20 | fits | 151,764 | 152 | 0.495 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 302,648 | 3.026 | 20 | 200 | fits | 157,448 | 245 | 0.353 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 463,484 | 4.635 | 20 | 200 | fits | 151,764 | 152 | 0.495 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 303,572 | 3.036 | 20 | 20 | fits | 157,448 | 245 | 0.353 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 464,188 | 4.642 | 20 | 20 | fits | 151,764 | 152 | 0.495 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 149,764 | 1.498 | 20 | 24 | fits | 151,717 | 164 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 306,222 | 3.062 | 20 | 24 | fits | 157,448 | 245 | 0.353 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 306,156 | 3.062 | 20 | 50 | fits | 157,448 | 245 | 0.353 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 467,212 | 4.672 | 20 | 50 | fits | 151,764 | 152 | 0.495 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 467,146 | 4.671 | 20 | 20 | fits | 151,764 | 152 | 0.495 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 803,596 | 8.036 | 20 | 20 | fits | 83,295 | 36 | 0.570 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 377,606 | 3.776 | 20 | 20 | fits | 130,752 | 163 | 0.288 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 313,272 | 3.133 | 20 | 200 | fits | 148,034 | 222 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 443,408 | 4.434 | 20 | 200 | fits | 130,752 | 163 | 0.288 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 314,196 | 3.142 | 20 | 20 | fits | 148,034 | 222 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 444,112 | 4.441 | 20 | 20 | fits | 130,752 | 163 | 0.288 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 161,793 | 1.618 | 20 | 24 | fits | 148,812 | 165 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 316,846 | 3.168 | 20 | 24 | fits | 148,034 | 222 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 316,780 | 3.168 | 20 | 50 | fits | 148,034 | 222 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 447,136 | 4.471 | 20 | 50 | fits | 130,752 | 163 | 0.288 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 578,065 | 5.781 | 20 | 20 | fits | 130,995 | 52 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 802,989 | 8.030 | 20 | 20 | fits | 100,542 | 44 | 0.526 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 461,731 | 4.617 | 20 | 20 | fits | 130,554 | 163 | 0.287 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 389,365 | 3.894 | 20 | 200 | fits | 147,910 | 222 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 519,303 | 5.193 | 20 | 200 | fits | 130,554 | 163 | 0.287 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 390,289 | 3.903 | 20 | 20 | fits | 147,910 | 222 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 520,007 | 5.200 | 20 | 20 | fits | 130,554 | 163 | 0.287 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 237,573 | 2.376 | 20 | 24 | fits | 148,688 | 165 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 392,939 | 3.929 | 20 | 24 | fits | 147,910 | 222 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 392,873 | 3.929 | 20 | 50 | fits | 147,910 | 222 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 523,031 | 5.230 | 20 | 50 | fits | 130,554 | 163 | 0.287 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 653,922 | 6.539 | 20 | 20 | fits | 130,957 | 52 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 883,704 | 8.837 | 20 | 20 | fits | 100,538 | 44 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 449,231 | 4.492 | 20 | 20 | fits | 130,554 | 163 | 0.287 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 376,865 | 3.769 | 20 | 200 | fits | 147,910 | 222 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 506,803 | 5.068 | 20 | 200 | fits | 130,554 | 163 | 0.287 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 377,789 | 3.778 | 20 | 20 | fits | 147,910 | 222 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 507,507 | 5.075 | 20 | 20 | fits | 130,554 | 163 | 0.287 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 225,073 | 2.251 | 20 | 24 | fits | 148,688 | 165 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 380,439 | 3.804 | 20 | 24 | fits | 147,910 | 222 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 380,373 | 3.804 | 20 | 50 | fits | 147,910 | 222 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 510,531 | 5.105 | 20 | 50 | fits | 130,554 | 163 | 0.287 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 641,422 | 6.414 | 20 | 20 | fits | 130,957 | 52 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 871,204 | 8.712 | 20 | 20 | fits | 100,538 | 44 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 436,731 | 4.367 | 20 | 20 | fits | 130,554 | 163 | 0.287 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 364,365 | 3.644 | 20 | 200 | fits | 147,910 | 222 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 494,303 | 4.943 | 20 | 200 | fits | 130,554 | 163 | 0.287 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 365,289 | 3.653 | 20 | 20 | fits | 147,910 | 222 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 495,007 | 4.950 | 20 | 20 | fits | 130,554 | 163 | 0.287 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 212,573 | 2.126 | 20 | 24 | fits | 148,688 | 165 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 367,939 | 3.679 | 20 | 24 | fits | 147,910 | 222 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 367,873 | 3.679 | 20 | 50 | fits | 147,910 | 222 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 498,031 | 4.980 | 20 | 50 | fits | 130,554 | 163 | 0.287 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 628,922 | 6.289 | 20 | 20 | fits | 130,957 | 52 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 858,704 | 8.587 | 20 | 20 | fits | 100,538 | 44 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 424,231 | 4.242 | 20 | 20 | fits | 130,554 | 163 | 0.287 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 351,865 | 3.519 | 20 | 200 | fits | 147,910 | 222 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 481,803 | 4.818 | 20 | 200 | fits | 130,554 | 163 | 0.287 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 352,789 | 3.528 | 20 | 20 | fits | 147,910 | 222 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 482,507 | 4.825 | 20 | 20 | fits | 130,554 | 163 | 0.287 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 200,073 | 2.001 | 20 | 24 | fits | 148,688 | 165 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 355,439 | 3.554 | 20 | 24 | fits | 147,910 | 222 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 355,373 | 3.554 | 20 | 50 | fits | 147,910 | 222 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 485,531 | 4.855 | 20 | 50 | fits | 130,554 | 163 | 0.287 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 616,422 | 6.164 | 20 | 20 | fits | 130,957 | 52 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 846,204 | 8.462 | 20 | 20 | fits | 100,538 | 44 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 411,731 | 4.117 | 20 | 20 | fits | 130,554 | 163 | 0.287 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 339,365 | 3.394 | 20 | 200 | fits | 147,910 | 222 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 469,303 | 4.693 | 20 | 200 | fits | 130,554 | 163 | 0.287 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 340,289 | 3.403 | 20 | 20 | fits | 147,910 | 222 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 470,007 | 4.700 | 20 | 20 | fits | 130,554 | 163 | 0.287 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 187,573 | 1.876 | 20 | 24 | fits | 148,688 | 165 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 342,939 | 3.429 | 20 | 24 | fits | 147,910 | 222 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 342,873 | 3.429 | 20 | 50 | fits | 147,910 | 222 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 473,031 | 4.730 | 20 | 50 | fits | 130,554 | 163 | 0.287 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 603,922 | 6.039 | 20 | 20 | fits | 130,957 | 52 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 833,704 | 8.337 | 20 | 20 | fits | 100,538 | 44 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 399,231 | 3.992 | 20 | 20 | fits | 130,554 | 163 | 0.287 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 326,865 | 3.269 | 20 | 200 | fits | 147,910 | 222 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 456,803 | 4.568 | 20 | 200 | fits | 130,554 | 163 | 0.287 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 327,789 | 3.278 | 20 | 20 | fits | 147,910 | 222 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 457,507 | 4.575 | 20 | 20 | fits | 130,554 | 163 | 0.287 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 175,073 | 1.751 | 20 | 24 | fits | 148,688 | 165 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 330,439 | 3.304 | 20 | 24 | fits | 147,910 | 222 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 330,373 | 3.304 | 20 | 50 | fits | 147,910 | 222 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 460,531 | 4.605 | 20 | 50 | fits | 130,554 | 163 | 0.287 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 591,422 | 5.914 | 20 | 20 | fits | 130,957 | 52 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 821,204 | 8.212 | 20 | 20 | fits | 100,538 | 44 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 386,731 | 3.867 | 20 | 20 | fits | 130,554 | 163 | 0.287 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 314,365 | 3.144 | 20 | 200 | fits | 147,910 | 222 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 444,303 | 4.443 | 20 | 200 | fits | 130,554 | 163 | 0.287 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 315,289 | 3.153 | 20 | 20 | fits | 147,910 | 222 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 445,007 | 4.450 | 20 | 20 | fits | 130,554 | 163 | 0.287 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 162,573 | 1.626 | 20 | 24 | fits | 148,688 | 165 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 317,939 | 3.179 | 20 | 24 | fits | 147,910 | 222 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 317,873 | 3.179 | 20 | 50 | fits | 147,910 | 222 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 448,031 | 4.480 | 20 | 50 | fits | 130,554 | 163 | 0.287 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 578,922 | 5.789 | 20 | 20 | fits | 130,957 | 52 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 808,704 | 8.087 | 20 | 20 | fits | 100,538 | 44 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 374,231 | 3.742 | 20 | 20 | fits | 130,554 | 163 | 0.287 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 301,865 | 3.019 | 20 | 200 | fits | 147,910 | 222 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 431,803 | 4.318 | 20 | 200 | fits | 130,554 | 163 | 0.287 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 302,789 | 3.028 | 20 | 20 | fits | 147,910 | 222 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 432,507 | 4.325 | 20 | 20 | fits | 130,554 | 163 | 0.287 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 150,073 | 1.501 | 20 | 24 | fits | 148,688 | 165 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 305,439 | 3.054 | 20 | 24 | fits | 147,910 | 222 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 305,373 | 3.054 | 20 | 50 | fits | 147,910 | 222 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 435,531 | 4.355 | 20 | 50 | fits | 130,554 | 163 | 0.287 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 566,422 | 5.664 | 20 | 20 | fits | 130,957 | 52 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 796,204 | 7.962 | 20 | 20 | fits | 100,538 | 44 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 370,073 | 3.701 | 20 | 20 | fits | 147,748 | 158 | 0.462 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 304,638 | 3.046 | 20 | 200 | fits | 153,734 | 224 | 0.351 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 451,770 | 4.518 | 20 | 200 | fits | 147,748 | 158 | 0.462 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 305,562 | 3.056 | 20 | 20 | fits | 153,734 | 224 | 0.351 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 452,474 | 4.525 | 20 | 20 | fits | 147,748 | 158 | 0.462 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 155,468 | 1.555 | 20 | 24 | fits | 147,150 | 161 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 308,212 | 3.082 | 20 | 24 | fits | 153,734 | 224 | 0.351 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 308,146 | 3.081 | 20 | 50 | fits | 153,734 | 224 | 0.351 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 455,498 | 4.555 | 20 | 50 | fits | 147,748 | 158 | 0.462 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 455,432 | 4.554 | 20 | 20 | fits | 147,748 | 158 | 0.462 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 806,958 | 8.070 | 20 | 20 | fits | 83,555 | 36 | 0.578 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 354,345 | 3.543 | 20 | 20 | fits | 146,862 | 156 | 0.475 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 308,633 | 3.086 | 20 | 200 | fits | 155,073 | 228 | 0.345 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 454,879 | 4.549 | 20 | 200 | fits | 146,862 | 156 | 0.475 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 309,557 | 3.096 | 20 | 20 | fits | 155,073 | 228 | 0.345 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 455,583 | 4.556 | 20 | 20 | fits | 146,862 | 156 | 0.475 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 158,124 | 1.581 | 20 | 24 | fits | 147,150 | 161 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 312,207 | 3.122 | 20 | 24 | fits | 155,073 | 228 | 0.345 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 312,141 | 3.121 | 20 | 50 | fits | 155,073 | 228 | 0.345 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 458,607 | 4.586 | 20 | 50 | fits | 146,862 | 156 | 0.475 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 458,541 | 4.585 | 20 | 20 | fits | 146,862 | 156 | 0.475 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 808,491 | 8.085 | 20 | 20 | fits | 83,301 | 36 | 0.571 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 381,859 | 3.819 | 20 | 20 | fits | 151,972 | 153 | 0.495 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 312,196 | 3.122 | 20 | 200 | fits | 155,980 | 240 | 0.350 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 473,157 | 4.732 | 20 | 200 | fits | 151,972 | 153 | 0.495 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 313,120 | 3.131 | 20 | 20 | fits | 155,980 | 240 | 0.350 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 473,861 | 4.739 | 20 | 20 | fits | 151,972 | 153 | 0.495 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 160,780 | 1.608 | 20 | 24 | fits | 147,150 | 161 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 315,770 | 3.158 | 20 | 24 | fits | 155,980 | 240 | 0.350 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 315,704 | 3.157 | 20 | 50 | fits | 155,980 | 240 | 0.350 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 476,885 | 4.769 | 20 | 50 | fits | 151,972 | 153 | 0.495 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 476,819 | 4.768 | 20 | 20 | fits | 151,972 | 153 | 0.495 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 818,318 | 8.183 | 20 | 20 | fits | 88,254 | 42 | 0.601 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 357,571 | 3.576 | 20 | 20 | fits | 152,257 | 162 | 0.520 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 298,151 | 2.982 | 20 | 200 | fits | 155,236 | 229 | 0.346 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 459,195 | 4.592 | 20 | 200 | fits | 152,257 | 162 | 0.520 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 299,075 | 2.991 | 20 | 20 | fits | 155,236 | 229 | 0.346 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 459,899 | 4.599 | 20 | 20 | fits | 152,257 | 162 | 0.520 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 147,479 | 1.475 | 20 | 24 | fits | 147,150 | 161 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 301,725 | 3.017 | 20 | 24 | fits | 155,236 | 229 | 0.346 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 301,659 | 3.017 | 20 | 50 | fits | 155,236 | 229 | 0.346 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 462,923 | 4.629 | 20 | 50 | fits | 152,257 | 162 | 0.520 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 462,857 | 4.629 | 20 | 20 | fits | 152,257 | 162 | 0.520 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 881,678 | 8.817 | 20 | 20 | fits | 83,949 | 37 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 367,092 | 3.671 | 20 | 20 | fits | 146,739 | 146 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 311,181 | 3.112 | 20 | 200 | fits | 157,659 | 244 | 0.355 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 457,304 | 4.573 | 20 | 200 | fits | 146,739 | 146 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 312,105 | 3.121 | 20 | 20 | fits | 157,659 | 244 | 0.355 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 458,008 | 4.580 | 20 | 20 | fits | 146,739 | 146 | 0.451 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 150,162 | 1.502 | 20 | 24 | fits | 147,177 | 162 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 314,755 | 3.148 | 20 | 24 | fits | 157,659 | 244 | 0.355 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 314,689 | 3.147 | 20 | 50 | fits | 157,659 | 244 | 0.355 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 461,032 | 4.610 | 20 | 50 | fits | 146,739 | 146 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 460,966 | 4.610 | 20 | 20 | fits | 146,739 | 146 | 0.451 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 879,820 | 8.798 | 20 | 20 | fits | 83,351 | 36 | 0.573 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 345,166 | 3.452 | 20 | 20 | fits | 146,768 | 155 | 0.475 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 299,454 | 2.995 | 20 | 200 | fits | 155,240 | 228 | 0.346 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 445,606 | 4.456 | 20 | 200 | fits | 146,768 | 155 | 0.475 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 300,378 | 3.004 | 20 | 20 | fits | 155,240 | 228 | 0.346 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 446,310 | 4.463 | 20 | 20 | fits | 146,768 | 155 | 0.475 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 148,778 | 1.488 | 20 | 24 | fits | 147,036 | 161 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 303,028 | 3.030 | 20 | 24 | fits | 155,240 | 228 | 0.346 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 302,962 | 3.030 | 20 | 50 | fits | 155,240 | 228 | 0.346 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 449,334 | 4.493 | 20 | 50 | fits | 146,768 | 155 | 0.475 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 449,268 | 4.493 | 20 | 20 | fits | 146,768 | 155 | 0.475 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 882,347 | 8.823 | 20 | 20 | fits | 87,584 | 43 | 0.622 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 365,955 | 3.660 | 20 | 20 | fits | 129,106 | 148 | 0.342 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 302,865 | 3.029 | 20 | 200 | fits | 155,995 | 239 | 0.351 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 431,355 | 4.314 | 20 | 200 | fits | 129,106 | 148 | 0.342 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 303,789 | 3.038 | 20 | 20 | fits | 155,995 | 239 | 0.351 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 432,059 | 4.321 | 20 | 20 | fits | 129,106 | 148 | 0.342 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 151,434 | 1.514 | 20 | 24 | fits | 147,036 | 161 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 306,439 | 3.064 | 20 | 24 | fits | 155,995 | 239 | 0.351 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 306,373 | 3.064 | 20 | 50 | fits | 155,995 | 239 | 0.351 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 435,083 | 4.351 | 20 | 50 | fits | 129,106 | 148 | 0.342 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 643,019 | 6.430 | 20 | 20 | fits | 131,534 | 54 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 883,461 | 8.835 | 20 | 20 | fits | 100,928 | 44 | 0.535 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 449,918 | 4.499 | 20 | 20 | fits | 131,195 | 164 | 0.298 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 300,792 | 3.008 | 20 | 200 | fits | 151,266 | 222 | 0.366 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 507,680 | 5.077 | 20 | 200 | fits | 131,195 | 164 | 0.298 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 301,716 | 3.017 | 20 | 20 | fits | 151,266 | 222 | 0.366 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 508,384 | 5.084 | 20 | 20 | fits | 131,195 | 164 | 0.298 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 154,090 | 1.541 | 20 | 24 | fits | 147,036 | 161 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 304,366 | 3.044 | 20 | 24 | fits | 151,266 | 222 | 0.366 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 304,300 | 3.043 | 20 | 50 | fits | 151,266 | 222 | 0.366 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 511,408 | 5.114 | 20 | 50 | fits | 131,195 | 164 | 0.298 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 655,665 | 6.557 | 20 | 20 | fits | 134,586 | 59 | 0.645 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 880,365 | 8.804 | 20 | 20 | fits | 100,434 | 44 | 0.523 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 347,107 | 3.471 | 20 | 20 | fits | 146,768 | 155 | 0.475 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 301,395 | 3.014 | 20 | 200 | fits | 155,240 | 228 | 0.346 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 447,547 | 4.475 | 20 | 200 | fits | 146,768 | 155 | 0.475 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 302,319 | 3.023 | 20 | 20 | fits | 155,240 | 228 | 0.346 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 448,251 | 4.483 | 20 | 20 | fits | 146,768 | 155 | 0.475 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 150,719 | 1.507 | 20 | 24 | fits | 147,036 | 161 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 304,969 | 3.050 | 20 | 24 | fits | 155,240 | 228 | 0.346 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 304,903 | 3.049 | 20 | 50 | fits | 155,240 | 228 | 0.346 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 451,275 | 4.513 | 20 | 50 | fits | 146,768 | 155 | 0.475 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 451,209 | 4.512 | 20 | 20 | fits | 146,768 | 155 | 0.475 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 788,111 | 7.881 | 20 | 20 | fits | 83,438 | 37 | 0.569 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 360,985 | 3.610 | 20 | 20 | fits | 147,034 | 146 | 0.454 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 304,806 | 3.048 | 20 | 200 | fits | 155,995 | 239 | 0.351 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 451,224 | 4.512 | 20 | 200 | fits | 147,034 | 146 | 0.454 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 305,730 | 3.057 | 20 | 20 | fits | 155,995 | 239 | 0.351 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 451,928 | 4.519 | 20 | 20 | fits | 147,034 | 146 | 0.454 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 153,375 | 1.534 | 20 | 24 | fits | 147,036 | 161 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 308,380 | 3.084 | 20 | 24 | fits | 155,995 | 239 | 0.351 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 308,314 | 3.083 | 20 | 50 | fits | 155,995 | 239 | 0.351 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 454,952 | 4.550 | 20 | 50 | fits | 147,034 | 146 | 0.454 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 454,886 | 4.549 | 20 | 20 | fits | 147,034 | 146 | 0.454 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 806,350 | 8.063 | 20 | 20 | fits | 88,107 | 43 | 0.633 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 369,287 | 3.693 | 20 | 20 | fits | 146,141 | 155 | 0.469 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 306,707 | 3.067 | 20 | 200 | fits | 155,240 | 228 | 0.346 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 452,232 | 4.522 | 20 | 200 | fits | 146,141 | 155 | 0.469 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 307,631 | 3.076 | 20 | 20 | fits | 155,240 | 228 | 0.346 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 452,936 | 4.529 | 20 | 20 | fits | 146,141 | 155 | 0.469 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 156,031 | 1.560 | 20 | 24 | fits | 147,036 | 161 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 310,281 | 3.103 | 20 | 24 | fits | 155,240 | 228 | 0.346 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 310,215 | 3.102 | 20 | 50 | fits | 155,240 | 228 | 0.346 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 455,960 | 4.560 | 20 | 50 | fits | 146,141 | 155 | 0.469 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 455,894 | 4.559 | 20 | 20 | fits | 146,141 | 155 | 0.469 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 811,857 | 8.119 | 20 | 20 | fits | 87,944 | 42 | 0.596 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 365,974 | 3.660 | 20 | 20 | fits | 147,182 | 147 | 0.457 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 310,118 | 3.101 | 20 | 200 | fits | 155,995 | 239 | 0.351 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 456,684 | 4.567 | 20 | 200 | fits | 147,182 | 147 | 0.457 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 311,042 | 3.110 | 20 | 20 | fits | 155,995 | 239 | 0.351 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 457,388 | 4.574 | 20 | 20 | fits | 147,182 | 147 | 0.457 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 158,687 | 1.587 | 20 | 24 | fits | 147,036 | 161 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 313,692 | 3.137 | 20 | 24 | fits | 155,995 | 239 | 0.351 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 313,626 | 3.136 | 20 | 50 | fits | 155,995 | 239 | 0.351 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 460,412 | 4.604 | 20 | 50 | fits | 147,182 | 147 | 0.457 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 460,346 | 4.603 | 20 | 20 | fits | 147,182 | 147 | 0.457 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 814,536 | 8.145 | 20 | 20 | fits | 83,292 | 36 | 0.570 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 366,247 | 3.662 | 20 | 20 | fits | 134,635 | 166 | 0.371 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 290,110 | 2.901 | 20 | 200 | fits | 149,288 | 227 | 0.355 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 433,734 | 4.337 | 20 | 200 | fits | 134,635 | 166 | 0.371 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 291,034 | 2.910 | 20 | 20 | fits | 149,288 | 227 | 0.355 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 434,438 | 4.344 | 20 | 20 | fits | 134,635 | 166 | 0.371 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 145,386 | 1.454 | 20 | 24 | fits | 147,036 | 161 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 293,684 | 2.937 | 20 | 24 | fits | 149,288 | 227 | 0.355 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 293,618 | 2.936 | 20 | 50 | fits | 149,288 | 227 | 0.355 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 437,462 | 4.375 | 20 | 50 | fits | 134,635 | 166 | 0.371 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 572,877 | 5.729 | 20 | 20 | fits | 135,481 | 58 | 0.640 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 797,842 | 7.978 | 20 | 20 | fits | 100,568 | 44 | 0.526 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 371,624 | 3.716 | 20 | 20 | fits | 128,865 | 148 | 0.341 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 309,158 | 3.092 | 20 | 200 | fits | 157,735 | 244 | 0.356 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 437,407 | 4.374 | 20 | 200 | fits | 128,865 | 148 | 0.341 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 310,082 | 3.101 | 20 | 20 | fits | 157,735 | 244 | 0.356 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 438,111 | 4.381 | 20 | 20 | fits | 128,865 | 148 | 0.341 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 148,136 | 1.481 | 20 | 24 | fits | 147,130 | 162 | 0.375 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 312,732 | 3.127 | 20 | 24 | fits | 157,735 | 244 | 0.356 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 312,666 | 3.127 | 20 | 50 | fits | 157,735 | 244 | 0.356 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 441,135 | 4.411 | 20 | 50 | fits | 128,865 | 148 | 0.341 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 572,082 | 5.721 | 20 | 20 | fits | 131,013 | 52 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 797,006 | 7.970 | 20 | 20 | fits | 100,555 | 44 | 0.526 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 381,809 | 3.818 | 20 | 20 | fits | 130,463 | 160 | 0.366 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 308,854 | 3.089 | 20 | 200 | fits | 154,124 | 224 | 0.354 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 438,701 | 4.387 | 20 | 200 | fits | 130,463 | 160 | 0.366 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 309,778 | 3.098 | 20 | 20 | fits | 154,124 | 224 | 0.354 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 439,405 | 4.394 | 20 | 20 | fits | 130,463 | 160 | 0.366 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 159,294 | 1.593 | 20 | 24 | fits | 147,079 | 162 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 312,428 | 3.124 | 20 | 24 | fits | 154,124 | 224 | 0.354 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 312,362 | 3.124 | 20 | 50 | fits | 154,124 | 224 | 0.354 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 442,429 | 4.424 | 20 | 50 | fits | 130,463 | 160 | 0.366 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 573,283 | 5.733 | 20 | 20 | fits | 130,920 | 52 | 0.626 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 798,347 | 7.983 | 20 | 20 | fits | 100,743 | 45 | 0.527 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 360,848 | 3.608 | 20 | 20 | fits | 131,082 | 163 | 0.296 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 296,310 | 2.963 | 20 | 200 | fits | 150,940 | 222 | 0.365 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 426,776 | 4.268 | 20 | 200 | fits | 131,082 | 163 | 0.296 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 297,234 | 2.972 | 20 | 20 | fits | 150,940 | 222 | 0.365 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 427,480 | 4.275 | 20 | 20 | fits | 131,082 | 163 | 0.296 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 149,934 | 1.499 | 20 | 24 | fits | 147,150 | 161 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 299,884 | 2.999 | 20 | 24 | fits | 150,940 | 222 | 0.365 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 299,818 | 2.998 | 20 | 50 | fits | 150,940 | 222 | 0.365 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 430,504 | 4.305 | 20 | 50 | fits | 131,082 | 163 | 0.296 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 561,477 | 5.615 | 20 | 20 | fits | 131,039 | 52 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 801,450 | 8.014 | 20 | 20 | fits | 105,511 | 51 | 0.593 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 382,882 | 3.829 | 20 | 20 | fits | 130,543 | 163 | 0.288 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 310,543 | 3.105 | 20 | 200 | fits | 147,873 | 222 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 440,470 | 4.405 | 20 | 200 | fits | 130,543 | 163 | 0.288 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 311,467 | 3.115 | 20 | 20 | fits | 147,873 | 222 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 441,174 | 4.412 | 20 | 20 | fits | 130,543 | 163 | 0.288 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 159,280 | 1.593 | 20 | 24 | fits | 147,240 | 162 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 314,117 | 3.141 | 20 | 24 | fits | 147,873 | 222 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 314,051 | 3.141 | 20 | 50 | fits | 147,873 | 222 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 444,198 | 4.442 | 20 | 50 | fits | 130,543 | 163 | 0.288 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 574,996 | 5.750 | 20 | 20 | fits | 130,864 | 52 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 799,925 | 7.999 | 20 | 20 | fits | 100,560 | 44 | 0.526 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 364,745 | 3.647 | 20 | 20 | fits | 149,237 | 152 | 0.464 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 306,682 | 3.067 | 20 | 200 | fits | 157,374 | 244 | 0.356 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 455,303 | 4.553 | 20 | 200 | fits | 149,237 | 152 | 0.464 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 307,606 | 3.076 | 20 | 20 | fits | 157,374 | 244 | 0.356 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 456,007 | 4.560 | 20 | 20 | fits | 149,237 | 152 | 0.464 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 145,918 | 1.459 | 20 | 24 | fits | 147,179 | 162 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 310,256 | 3.103 | 20 | 24 | fits | 157,374 | 244 | 0.356 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 310,190 | 3.102 | 20 | 50 | fits | 157,374 | 244 | 0.356 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 459,031 | 4.590 | 20 | 50 | fits | 149,237 | 152 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 458,965 | 4.590 | 20 | 20 | fits | 149,237 | 152 | 0.464 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 795,836 | 7.958 | 20 | 20 | fits | 83,564 | 36 | 0.573 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 367,806 | 3.678 | 20 | 20 | fits | 129,868 | 160 | 0.303 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 304,936 | 3.049 | 20 | 200 | fits | 148,523 | 221 | 0.358 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 434,188 | 4.342 | 20 | 200 | fits | 129,868 | 160 | 0.303 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 305,860 | 3.059 | 20 | 20 | fits | 148,523 | 221 | 0.358 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 434,892 | 4.349 | 20 | 20 | fits | 129,868 | 160 | 0.303 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 160,977 | 1.610 | 20 | 24 | fits | 147,047 | 161 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 308,510 | 3.085 | 20 | 24 | fits | 148,523 | 221 | 0.358 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 308,444 | 3.084 | 20 | 50 | fits | 148,523 | 221 | 0.358 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 437,916 | 4.379 | 20 | 50 | fits | 129,868 | 160 | 0.303 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 568,918 | 5.689 | 20 | 20 | fits | 131,068 | 52 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 812,722 | 8.127 | 20 | 20 | fits | 109,276 | 57 | 0.594 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 355,511 | 3.555 | 20 | 20 | fits | 147,124 | 146 | 0.455 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 299,332 | 2.993 | 20 | 200 | fits | 156,220 | 239 | 0.353 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 445,840 | 4.458 | 20 | 200 | fits | 147,124 | 146 | 0.455 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 300,256 | 3.003 | 20 | 20 | fits | 156,220 | 239 | 0.353 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 446,544 | 4.465 | 20 | 20 | fits | 147,124 | 146 | 0.455 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 147,676 | 1.477 | 20 | 24 | fits | 147,047 | 161 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 302,906 | 3.029 | 20 | 24 | fits | 156,220 | 239 | 0.353 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 302,840 | 3.028 | 20 | 50 | fits | 156,220 | 239 | 0.353 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 449,568 | 4.496 | 20 | 50 | fits | 147,124 | 146 | 0.455 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 449,502 | 4.495 | 20 | 20 | fits | 147,124 | 146 | 0.455 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 886,466 | 8.865 | 20 | 20 | fits | 84,356 | 37 | 0.592 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 363,813 | 3.638 | 20 | 20 | fits | 146,325 | 156 | 0.470 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 301,233 | 3.012 | 20 | 200 | fits | 155,465 | 228 | 0.348 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 446,942 | 4.469 | 20 | 200 | fits | 146,325 | 156 | 0.470 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 302,157 | 3.022 | 20 | 20 | fits | 155,465 | 228 | 0.348 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 447,646 | 4.476 | 20 | 20 | fits | 146,325 | 156 | 0.470 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 150,332 | 1.503 | 20 | 24 | fits | 147,047 | 161 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 304,807 | 3.048 | 20 | 24 | fits | 155,465 | 228 | 0.348 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 304,741 | 3.047 | 20 | 50 | fits | 155,465 | 228 | 0.348 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 450,670 | 4.507 | 20 | 50 | fits | 146,325 | 156 | 0.470 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 450,604 | 4.506 | 20 | 20 | fits | 146,325 | 156 | 0.470 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 886,627 | 8.866 | 20 | 20 | fits | 92,171 | 40 | 0.549 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 360,500 | 3.605 | 20 | 20 | fits | 147,272 | 147 | 0.457 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 304,644 | 3.046 | 20 | 200 | fits | 156,220 | 239 | 0.353 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 451,300 | 4.513 | 20 | 200 | fits | 147,272 | 147 | 0.457 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 305,568 | 3.056 | 20 | 20 | fits | 156,220 | 239 | 0.353 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 452,004 | 4.520 | 20 | 20 | fits | 147,272 | 147 | 0.457 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 152,988 | 1.530 | 20 | 24 | fits | 147,047 | 161 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 308,218 | 3.082 | 20 | 24 | fits | 156,220 | 239 | 0.353 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 308,152 | 3.082 | 20 | 50 | fits | 156,220 | 239 | 0.353 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 455,028 | 4.550 | 20 | 50 | fits | 147,272 | 147 | 0.457 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 454,962 | 4.550 | 20 | 20 | fits | 147,272 | 147 | 0.457 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 890,967 | 8.910 | 20 | 20 | fits | 92,166 | 40 | 0.549 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 390,500 | 3.905 | 20 | 20 | fits | 133,948 | 167 | 0.401 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 305,405 | 3.054 | 20 | 200 | fits | 154,325 | 225 | 0.355 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 448,140 | 4.481 | 20 | 200 | fits | 133,948 | 167 | 0.401 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 306,329 | 3.063 | 20 | 20 | fits | 154,325 | 225 | 0.355 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 448,844 | 4.488 | 20 | 20 | fits | 133,948 | 167 | 0.401 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 155,644 | 1.556 | 20 | 24 | fits | 147,047 | 161 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 308,979 | 3.090 | 20 | 24 | fits | 154,325 | 225 | 0.355 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 308,913 | 3.089 | 20 | 50 | fits | 154,325 | 225 | 0.355 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 451,868 | 4.519 | 20 | 50 | fits | 133,948 | 167 | 0.401 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 663,962 | 6.640 | 20 | 20 | fits | 131,376 | 53 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 888,827 | 8.888 | 20 | 20 | fits | 100,482 | 44 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 461,708 | 4.617 | 20 | 20 | fits | 133,975 | 169 | 0.325 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 314,001 | 3.140 | 20 | 200 | fits | 152,339 | 222 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 528,063 | 5.281 | 20 | 200 | fits | 133,975 | 169 | 0.325 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 314,925 | 3.149 | 20 | 20 | fits | 152,339 | 222 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 528,767 | 5.288 | 20 | 20 | fits | 133,975 | 169 | 0.325 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 158,345 | 1.583 | 20 | 24 | fits | 147,092 | 162 | 0.375 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 317,575 | 3.176 | 20 | 24 | fits | 152,339 | 222 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 317,509 | 3.175 | 20 | 50 | fits | 152,339 | 222 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 531,791 | 5.318 | 20 | 50 | fits | 133,975 | 169 | 0.325 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 662,473 | 6.625 | 20 | 20 | fits | 130,748 | 52 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 887,288 | 8.873 | 20 | 20 | fits | 100,559 | 45 | 0.523 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 362,337 | 3.623 | 20 | 20 | fits | 147,272 | 147 | 0.457 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 306,481 | 3.065 | 20 | 200 | fits | 156,220 | 239 | 0.353 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 453,137 | 4.531 | 20 | 200 | fits | 147,272 | 147 | 0.457 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 307,405 | 3.074 | 20 | 20 | fits | 156,220 | 239 | 0.353 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 453,841 | 4.538 | 20 | 20 | fits | 147,272 | 147 | 0.457 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 154,825 | 1.548 | 20 | 24 | fits | 147,047 | 161 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 310,055 | 3.101 | 20 | 24 | fits | 156,220 | 239 | 0.353 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 309,989 | 3.100 | 20 | 50 | fits | 156,220 | 239 | 0.353 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 456,865 | 4.569 | 20 | 50 | fits | 147,272 | 147 | 0.457 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 456,799 | 4.568 | 20 | 20 | fits | 147,272 | 147 | 0.457 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 806,745 | 8.067 | 20 | 20 | fits | 83,314 | 36 | 0.571 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 386,062 | 3.861 | 20 | 20 | fits | 152,839 | 165 | 0.505 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 307,227 | 3.072 | 20 | 200 | fits | 154,310 | 225 | 0.355 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 468,853 | 4.689 | 20 | 200 | fits | 152,839 | 165 | 0.505 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 308,151 | 3.082 | 20 | 20 | fits | 154,310 | 225 | 0.355 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 469,557 | 4.696 | 20 | 20 | fits | 152,839 | 165 | 0.505 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 157,481 | 1.575 | 20 | 24 | fits | 147,047 | 161 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 310,801 | 3.108 | 20 | 24 | fits | 154,310 | 225 | 0.355 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 310,735 | 3.107 | 20 | 50 | fits | 154,310 | 225 | 0.355 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 472,581 | 4.726 | 20 | 50 | fits | 152,839 | 165 | 0.505 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 472,515 | 4.725 | 20 | 20 | fits | 152,839 | 165 | 0.505 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 809,029 | 8.090 | 20 | 20 | fits | 83,295 | 36 | 0.570 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 375,893 | 3.759 | 20 | 20 | fits | 130,898 | 163 | 0.293 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 311,495 | 3.115 | 20 | 200 | fits | 147,800 | 222 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 441,777 | 4.418 | 20 | 200 | fits | 130,898 | 163 | 0.293 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 312,419 | 3.124 | 20 | 20 | fits | 147,800 | 222 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 442,481 | 4.425 | 20 | 20 | fits | 130,898 | 163 | 0.293 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 160,200 | 1.602 | 20 | 24 | fits | 147,110 | 162 | 0.375 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 315,069 | 3.151 | 20 | 24 | fits | 147,800 | 222 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 315,003 | 3.150 | 20 | 50 | fits | 147,800 | 222 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 445,505 | 4.455 | 20 | 50 | fits | 130,898 | 163 | 0.293 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 576,303 | 5.763 | 20 | 20 | fits | 130,864 | 52 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 806,058 | 8.061 | 20 | 20 | fits | 105,373 | 50 | 0.556 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 374,085 | 3.741 | 20 | 20 | fits | 147,838 | 158 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 308,650 | 3.087 | 20 | 200 | fits | 154,214 | 224 | 0.356 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 455,872 | 4.559 | 20 | 200 | fits | 147,838 | 158 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 309,574 | 3.096 | 20 | 20 | fits | 154,214 | 224 | 0.356 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 456,576 | 4.566 | 20 | 20 | fits | 147,838 | 158 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 159,000 | 1.590 | 20 | 24 | fits | 147,161 | 161 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 312,224 | 3.122 | 20 | 24 | fits | 154,214 | 224 | 0.356 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 312,158 | 3.122 | 20 | 50 | fits | 154,214 | 224 | 0.356 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 459,600 | 4.596 | 20 | 50 | fits | 147,838 | 158 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 459,534 | 4.595 | 20 | 20 | fits | 147,838 | 158 | 0.463 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 801,139 | 8.011 | 20 | 20 | fits | 83,416 | 37 | 0.568 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 354,105 | 3.541 | 20 | 20 | fits | 147,178 | 146 | 0.457 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 298,249 | 2.982 | 20 | 200 | fits | 157,114 | 244 | 0.352 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 444,811 | 4.448 | 20 | 200 | fits | 147,178 | 146 | 0.457 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 299,173 | 2.992 | 20 | 20 | fits | 157,114 | 244 | 0.352 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 445,515 | 4.455 | 20 | 20 | fits | 147,178 | 146 | 0.457 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 145,699 | 1.457 | 20 | 24 | fits | 147,161 | 161 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 301,823 | 3.018 | 20 | 24 | fits | 157,114 | 244 | 0.352 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 301,757 | 3.018 | 20 | 50 | fits | 157,114 | 244 | 0.352 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 448,539 | 4.485 | 20 | 50 | fits | 147,178 | 146 | 0.457 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 448,473 | 4.485 | 20 | 20 | fits | 147,178 | 146 | 0.457 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 804,022 | 8.040 | 20 | 20 | fits | 87,624 | 43 | 0.624 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 363,440 | 3.634 | 20 | 20 | fits | 147,838 | 158 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 298,005 | 2.980 | 20 | 200 | fits | 154,214 | 224 | 0.356 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 445,227 | 4.452 | 20 | 200 | fits | 147,838 | 158 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 298,929 | 2.989 | 20 | 20 | fits | 154,214 | 224 | 0.356 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 445,931 | 4.459 | 20 | 20 | fits | 147,838 | 158 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 148,355 | 1.484 | 20 | 24 | fits | 147,161 | 161 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 301,579 | 3.016 | 20 | 24 | fits | 154,214 | 224 | 0.356 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 301,513 | 3.015 | 20 | 50 | fits | 154,214 | 224 | 0.356 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 448,955 | 4.490 | 20 | 50 | fits | 147,838 | 158 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 448,889 | 4.489 | 20 | 20 | fits | 147,838 | 158 | 0.463 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 804,443 | 8.044 | 20 | 20 | fits | 83,549 | 36 | 0.576 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 347,986 | 3.480 | 20 | 20 | fits | 137,345 | 167 | 0.345 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 295,026 | 2.950 | 20 | 200 | fits | 148,579 | 221 | 0.359 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 431,755 | 4.318 | 20 | 200 | fits | 137,345 | 167 | 0.345 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 295,950 | 2.959 | 20 | 20 | fits | 148,579 | 221 | 0.359 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 432,459 | 4.325 | 20 | 20 | fits | 137,345 | 167 | 0.345 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 151,011 | 1.510 | 20 | 24 | fits | 147,161 | 161 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 298,600 | 2.986 | 20 | 24 | fits | 148,579 | 221 | 0.359 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 298,534 | 2.985 | 20 | 50 | fits | 148,579 | 221 | 0.359 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 435,483 | 4.355 | 20 | 50 | fits | 137,345 | 167 | 0.345 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 579,299 | 5.793 | 20 | 20 | fits | 134,214 | 59 | 0.642 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 804,216 | 8.042 | 20 | 20 | fits | 100,542 | 44 | 0.526 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 379,323 | 3.793 | 20 | 20 | fits | 136,008 | 169 | 0.366 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 300,643 | 3.006 | 20 | 200 | fits | 151,540 | 223 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 445,623 | 4.456 | 20 | 200 | fits | 136,008 | 169 | 0.366 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 301,567 | 3.016 | 20 | 20 | fits | 151,540 | 223 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 446,327 | 4.463 | 20 | 20 | fits | 136,008 | 169 | 0.366 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 153,667 | 1.537 | 20 | 24 | fits | 147,161 | 161 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 304,217 | 3.042 | 20 | 24 | fits | 151,540 | 223 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 304,151 | 3.042 | 20 | 50 | fits | 151,540 | 223 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 449,351 | 4.494 | 20 | 50 | fits | 136,008 | 169 | 0.366 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 579,996 | 5.800 | 20 | 20 | fits | 130,711 | 52 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 805,013 | 8.050 | 20 | 20 | fits | 100,570 | 44 | 0.526 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 357,142 | 3.571 | 20 | 20 | fits | 147,199 | 147 | 0.454 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 300,963 | 3.010 | 20 | 200 | fits | 156,220 | 239 | 0.353 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 447,546 | 4.475 | 20 | 200 | fits | 147,199 | 147 | 0.454 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 301,887 | 3.019 | 20 | 20 | fits | 156,220 | 239 | 0.353 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 448,250 | 4.482 | 20 | 20 | fits | 147,199 | 147 | 0.454 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 149,307 | 1.493 | 20 | 24 | fits | 146,982 | 161 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 304,537 | 3.045 | 20 | 24 | fits | 156,220 | 239 | 0.353 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 304,471 | 3.045 | 20 | 50 | fits | 156,220 | 239 | 0.353 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 451,274 | 4.513 | 20 | 50 | fits | 147,199 | 147 | 0.454 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 451,208 | 4.512 | 20 | 20 | fits | 147,199 | 147 | 0.454 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 801,092 | 8.011 | 20 | 20 | fits | 83,301 | 36 | 0.571 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 372,582 | 3.726 | 20 | 20 | fits | 134,924 | 167 | 0.373 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 296,074 | 2.961 | 20 | 200 | fits | 148,675 | 222 | 0.358 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 439,987 | 4.400 | 20 | 200 | fits | 134,924 | 167 | 0.373 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 296,998 | 2.970 | 20 | 20 | fits | 148,675 | 222 | 0.358 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 440,691 | 4.407 | 20 | 20 | fits | 134,924 | 167 | 0.373 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 151,963 | 1.520 | 20 | 24 | fits | 146,982 | 161 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 299,648 | 2.996 | 20 | 24 | fits | 148,675 | 222 | 0.358 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 299,582 | 2.996 | 20 | 50 | fits | 148,675 | 222 | 0.358 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 443,715 | 4.437 | 20 | 50 | fits | 134,924 | 167 | 0.373 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 574,790 | 5.748 | 20 | 20 | fits | 131,141 | 52 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 799,755 | 7.998 | 20 | 20 | fits | 100,568 | 44 | 0.526 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 371,543 | 3.715 | 20 | 20 | fits | 146,954 | 146 | 0.455 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 315,931 | 3.159 | 20 | 200 | fits | 157,784 | 244 | 0.357 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 462,269 | 4.623 | 20 | 200 | fits | 146,954 | 146 | 0.455 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 316,855 | 3.169 | 20 | 20 | fits | 157,784 | 244 | 0.357 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 462,973 | 4.630 | 20 | 20 | fits | 146,954 | 146 | 0.455 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 154,691 | 1.547 | 20 | 24 | fits | 147,054 | 162 | 0.375 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 319,505 | 3.195 | 20 | 24 | fits | 157,784 | 244 | 0.357 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 319,439 | 3.194 | 20 | 50 | fits | 157,784 | 244 | 0.357 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 465,997 | 4.660 | 20 | 50 | fits | 146,954 | 146 | 0.455 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 465,931 | 4.659 | 20 | 20 | fits | 146,954 | 146 | 0.455 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 807,394 | 8.074 | 20 | 20 | fits | 88,139 | 42 | 0.599 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 360,783 | 3.608 | 20 | 20 | fits | 129,807 | 160 | 0.302 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 297,913 | 2.979 | 20 | 200 | fits | 148,579 | 221 | 0.359 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 427,104 | 4.271 | 20 | 200 | fits | 129,807 | 160 | 0.302 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 298,837 | 2.988 | 20 | 20 | fits | 148,579 | 221 | 0.359 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 427,808 | 4.278 | 20 | 20 | fits | 129,807 | 160 | 0.302 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 153,898 | 1.539 | 20 | 24 | fits | 147,027 | 161 | 0.375 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 301,487 | 3.015 | 20 | 24 | fits | 148,579 | 221 | 0.359 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 301,421 | 3.014 | 20 | 50 | fits | 148,579 | 221 | 0.359 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 430,832 | 4.308 | 20 | 50 | fits | 129,807 | 160 | 0.302 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 561,873 | 5.619 | 20 | 20 | fits | 131,107 | 52 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 872,759 | 8.728 | 20 | 20 | fits | 104,158 | 52 | 0.547 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 364,191 | 3.642 | 20 | 20 | fits | 147,159 | 146 | 0.457 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 308,335 | 3.083 | 20 | 200 | fits | 156,276 | 239 | 0.354 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 454,878 | 4.549 | 20 | 200 | fits | 147,159 | 146 | 0.457 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 309,259 | 3.093 | 20 | 20 | fits | 156,276 | 239 | 0.354 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 455,582 | 4.556 | 20 | 20 | fits | 147,159 | 146 | 0.457 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 156,623 | 1.566 | 20 | 24 | fits | 147,096 | 161 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 311,909 | 3.119 | 20 | 24 | fits | 156,276 | 239 | 0.354 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 311,843 | 3.118 | 20 | 50 | fits | 156,276 | 239 | 0.354 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 458,606 | 4.586 | 20 | 50 | fits | 147,159 | 146 | 0.457 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 458,540 | 4.585 | 20 | 20 | fits | 147,159 | 146 | 0.457 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 892,276 | 8.923 | 20 | 20 | fits | 85,345 | 37 | 0.618 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 381,757 | 3.818 | 20 | 20 | fits | 130,337 | 160 | 0.364 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 308,897 | 3.089 | 20 | 200 | fits | 154,182 | 224 | 0.355 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 438,618 | 4.386 | 20 | 200 | fits | 130,337 | 160 | 0.364 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 309,821 | 3.098 | 20 | 20 | fits | 154,182 | 224 | 0.355 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 439,322 | 4.393 | 20 | 20 | fits | 130,337 | 160 | 0.364 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 159,279 | 1.593 | 20 | 24 | fits | 147,096 | 161 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 312,471 | 3.125 | 20 | 24 | fits | 154,182 | 224 | 0.355 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 312,405 | 3.124 | 20 | 50 | fits | 154,182 | 224 | 0.355 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 442,346 | 4.423 | 20 | 50 | fits | 130,337 | 160 | 0.364 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 654,084 | 6.541 | 20 | 20 | fits | 134,565 | 60 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 891,620 | 8.916 | 20 | 20 | fits | 101,080 | 44 | 0.536 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 361,149 | 3.611 | 20 | 20 | fits | 129,109 | 149 | 0.343 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 298,501 | 2.985 | 20 | 200 | fits | 157,114 | 244 | 0.352 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 426,994 | 4.270 | 20 | 200 | fits | 129,109 | 149 | 0.343 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 299,425 | 2.994 | 20 | 20 | fits | 157,114 | 244 | 0.352 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 427,698 | 4.277 | 20 | 20 | fits | 129,109 | 149 | 0.343 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 145,951 | 1.460 | 20 | 24 | fits | 147,096 | 161 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 302,075 | 3.021 | 20 | 24 | fits | 157,114 | 244 | 0.352 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 302,009 | 3.020 | 20 | 50 | fits | 157,114 | 244 | 0.352 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 430,722 | 4.307 | 20 | 50 | fits | 129,109 | 149 | 0.343 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 651,811 | 6.518 | 20 | 20 | fits | 134,836 | 59 | 0.645 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 876,728 | 8.767 | 20 | 20 | fits | 100,555 | 44 | 0.526 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 459,904 | 4.599 | 20 | 20 | fits | 138,081 | 172 | 0.367 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 294,430 | 2.944 | 20 | 200 | fits | 150,360 | 219 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 517,987 | 5.180 | 20 | 200 | fits | 138,081 | 172 | 0.367 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 295,354 | 2.954 | 20 | 20 | fits | 150,360 | 219 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 518,691 | 5.187 | 20 | 20 | fits | 138,081 | 172 | 0.367 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 148,634 | 1.486 | 20 | 24 | fits | 147,096 | 161 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 298,004 | 2.980 | 20 | 24 | fits | 150,360 | 219 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 297,938 | 2.979 | 20 | 50 | fits | 150,360 | 219 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 521,715 | 5.217 | 20 | 50 | fits | 138,081 | 172 | 0.367 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 652,430 | 6.524 | 20 | 20 | fits | 130,781 | 52 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 877,239 | 8.772 | 20 | 20 | fits | 100,482 | 44 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 375,716 | 3.757 | 20 | 20 | fits | 147,819 | 158 | 0.462 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 310,281 | 3.103 | 20 | 200 | fits | 154,214 | 224 | 0.356 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 457,484 | 4.575 | 20 | 200 | fits | 147,819 | 158 | 0.462 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 311,205 | 3.112 | 20 | 20 | fits | 154,214 | 224 | 0.356 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 458,188 | 4.582 | 20 | 20 | fits | 147,819 | 158 | 0.462 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 160,631 | 1.606 | 20 | 24 | fits | 147,096 | 161 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 313,855 | 3.139 | 20 | 24 | fits | 154,214 | 224 | 0.356 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 313,789 | 3.138 | 20 | 50 | fits | 154,214 | 224 | 0.356 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 461,212 | 4.612 | 20 | 50 | fits | 147,819 | 158 | 0.462 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 461,146 | 4.611 | 20 | 20 | fits | 147,819 | 158 | 0.462 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 812,469 | 8.125 | 20 | 20 | fits | 83,519 | 36 | 0.576 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 354,898 | 3.549 | 20 | 20 | fits | 147,253 | 147 | 0.457 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 299,042 | 2.990 | 20 | 200 | fits | 156,276 | 239 | 0.354 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 445,679 | 4.457 | 20 | 200 | fits | 147,253 | 147 | 0.457 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 299,966 | 3.000 | 20 | 20 | fits | 156,276 | 239 | 0.354 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 446,383 | 4.464 | 20 | 20 | fits | 147,253 | 147 | 0.457 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 147,330 | 1.473 | 20 | 24 | fits | 147,096 | 161 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 302,616 | 3.026 | 20 | 24 | fits | 156,276 | 239 | 0.354 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 302,550 | 3.026 | 20 | 50 | fits | 156,276 | 239 | 0.354 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 449,407 | 4.494 | 20 | 50 | fits | 147,253 | 147 | 0.457 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 449,341 | 4.493 | 20 | 20 | fits | 147,253 | 147 | 0.457 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 799,203 | 7.992 | 20 | 20 | fits | 83,314 | 36 | 0.571 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 378,665 | 3.787 | 20 | 20 | fits | 152,878 | 165 | 0.505 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 299,788 | 2.998 | 20 | 200 | fits | 154,366 | 225 | 0.357 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 461,527 | 4.615 | 20 | 200 | fits | 152,878 | 165 | 0.505 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 300,712 | 3.007 | 20 | 20 | fits | 154,366 | 225 | 0.357 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 462,231 | 4.622 | 20 | 20 | fits | 152,878 | 165 | 0.505 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 149,986 | 1.500 | 20 | 24 | fits | 147,096 | 161 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 303,362 | 3.034 | 20 | 24 | fits | 154,366 | 225 | 0.357 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 303,296 | 3.033 | 20 | 50 | fits | 154,366 | 225 | 0.357 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 465,255 | 4.653 | 20 | 50 | fits | 152,878 | 165 | 0.505 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 465,189 | 4.652 | 20 | 20 | fits | 152,878 | 165 | 0.505 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 806,596 | 8.066 | 20 | 20 | fits | 88,254 | 42 | 0.601 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 356,438 | 3.564 | 20 | 20 | fits | 135,101 | 167 | 0.377 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 296,849 | 2.968 | 20 | 200 | fits | 148,771 | 222 | 0.360 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 441,013 | 4.410 | 20 | 200 | fits | 135,101 | 167 | 0.377 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 297,773 | 2.978 | 20 | 20 | fits | 148,771 | 222 | 0.360 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 441,717 | 4.417 | 20 | 20 | fits | 135,101 | 167 | 0.377 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 152,642 | 1.526 | 20 | 24 | fits | 147,096 | 161 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 300,423 | 3.004 | 20 | 24 | fits | 148,771 | 222 | 0.360 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 300,357 | 3.004 | 20 | 50 | fits | 148,771 | 222 | 0.360 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 444,741 | 4.447 | 20 | 50 | fits | 135,101 | 167 | 0.377 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 575,731 | 5.757 | 20 | 20 | fits | 131,056 | 52 | 0.626 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 805,672 | 8.057 | 20 | 20 | fits | 100,528 | 44 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 372,322 | 3.723 | 20 | 20 | fits | 146,810 | 146 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 316,411 | 3.164 | 20 | 200 | fits | 157,696 | 244 | 0.356 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 462,605 | 4.626 | 20 | 200 | fits | 146,810 | 146 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 317,335 | 3.173 | 20 | 20 | fits | 157,696 | 244 | 0.356 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 463,309 | 4.633 | 20 | 20 | fits | 146,810 | 146 | 0.451 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 155,325 | 1.553 | 20 | 24 | fits | 147,123 | 162 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 319,985 | 3.200 | 20 | 24 | fits | 157,696 | 244 | 0.356 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 319,919 | 3.199 | 20 | 50 | fits | 157,696 | 244 | 0.356 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 466,333 | 4.663 | 20 | 50 | fits | 146,810 | 146 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 466,267 | 4.663 | 20 | 20 | fits | 146,810 | 146 | 0.451 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 807,592 | 8.076 | 20 | 20 | fits | 83,295 | 36 | 0.570 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 344,379 | 3.444 | 20 | 20 | fits | 130,086 | 160 | 0.307 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 298,377 | 2.984 | 20 | 200 | fits | 148,523 | 221 | 0.358 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 427,847 | 4.278 | 20 | 200 | fits | 130,086 | 160 | 0.307 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 299,301 | 2.993 | 20 | 20 | fits | 148,523 | 221 | 0.358 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 428,551 | 4.286 | 20 | 20 | fits | 130,086 | 160 | 0.307 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 154,418 | 1.544 | 20 | 24 | fits | 146,982 | 161 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 301,951 | 3.020 | 20 | 24 | fits | 148,523 | 221 | 0.358 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 301,885 | 3.019 | 20 | 50 | fits | 148,523 | 221 | 0.358 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 431,575 | 4.316 | 20 | 50 | fits | 130,086 | 160 | 0.307 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 566,974 | 5.670 | 20 | 20 | fits | 135,465 | 58 | 0.639 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 792,019 | 7.920 | 20 | 20 | fits | 100,685 | 45 | 0.526 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 371,781 | 3.718 | 20 | 20 | fits | 129,067 | 148 | 0.341 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 308,730 | 3.087 | 20 | 200 | fits | 156,220 | 239 | 0.353 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 437,181 | 4.372 | 20 | 200 | fits | 129,067 | 148 | 0.341 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 309,654 | 3.097 | 20 | 20 | fits | 156,220 | 239 | 0.353 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 437,885 | 4.379 | 20 | 20 | fits | 129,067 | 148 | 0.341 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 157,074 | 1.571 | 20 | 24 | fits | 146,982 | 161 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 312,304 | 3.123 | 20 | 24 | fits | 156,220 | 239 | 0.353 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 312,238 | 3.122 | 20 | 50 | fits | 156,220 | 239 | 0.353 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 440,909 | 4.409 | 20 | 50 | fits | 129,067 | 148 | 0.341 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 572,058 | 5.721 | 20 | 20 | fits | 131,215 | 52 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 812,059 | 8.121 | 20 | 20 | fits | 105,473 | 51 | 0.592 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 379,278 | 3.793 | 20 | 20 | fits | 130,903 | 163 | 0.294 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 306,657 | 3.067 | 20 | 200 | fits | 151,491 | 222 | 0.367 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 436,944 | 4.369 | 20 | 200 | fits | 130,903 | 163 | 0.294 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 307,581 | 3.076 | 20 | 20 | fits | 151,491 | 222 | 0.367 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 437,648 | 4.376 | 20 | 20 | fits | 130,903 | 163 | 0.294 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 159,730 | 1.597 | 20 | 24 | fits | 146,982 | 161 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 310,231 | 3.102 | 20 | 24 | fits | 151,491 | 222 | 0.367 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 310,165 | 3.102 | 20 | 50 | fits | 151,491 | 222 | 0.367 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 440,672 | 4.407 | 20 | 50 | fits | 130,903 | 163 | 0.294 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 571,856 | 5.719 | 20 | 20 | fits | 131,250 | 53 | 0.626 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 811,906 | 8.119 | 20 | 20 | fits | 100,872 | 44 | 0.532 |
| LINK_UP | `adp.link_up.if0` | 2,119 | 0.021 | 20 | 200 | fits | 32,023 | 43 (11) | 0.676 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,151 | 0.082 | 20 | 200 | fits | 21,213 | 23 (39) | 0.578 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 1,824 | 0.018 | 20 | 200 | fits | 1,933 | 10 (11) | 0.368 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 21,573 | 0.216 | 20 | 20 | fits | 32,177 | 21 (35) | 0.780 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 18,398 | 0.184 | 20 | 20 | fits | 28,256 | 17 (14) | 0.816 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 16,632 | 0.166 | 20 | 20 | fits | 29,141 | 18 (14) | 0.820 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 19,332 | 0.193 | 20 | 20 | fits | 35,482 | 27 (35) | 0.750 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 79,288 | 0.793 | 20 | 20 | fits | 28,014 | 8 | 0.832 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 41,155 | 0.412 | 20 | 20 | fits | 41,221 | 12 | 0.883 |
| malformed MRPDU discard | `srp.malformed.if0` | 22,209 | 0.222 | 20 | 20 | fits | 22,275 | 12 | 0.717 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 73,061 | 0.731 | 220 | 220 | fits | 43,613 | 6 | 0.917 |
| an event behind 15 others | `backlog.event.if0` | 160,817 | 1.608 | 20 | 200 | fits | 53,446 | 78 | 0.502 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 435,474 | 4.355 | 20 | 20 | fits | 55,239 | 81 | 0.187 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 417,058 | 4.171 | 20 | 200 | fits | 150,204 | 130 | 0.266 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 416,442 | 4.164 | 20 | 200 | fits | 150,204 | 130 | 0.266 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 412,736 | 4.127 | 20 | 20 | fits | 150,204 | 130 | 0.266 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 467,139 | 4.671 | 20 | 20 | fits | 55,239 | 81 | 0.187 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 151,338 | 1.513 | 20 | 24 | fits | 152,229 | 167 | 0.388 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 265,182 | 2.652 | 20 | 24 | fits | 61,388 | 26 | 0.688 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 415,320 | 4.153 | 20 | 50 | fits | 150,204 | 130 | 0.266 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 414,924 | 4.149 | 20 | 50 | fits | 150,204 | 130 | 0.266 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 470,097 | 4.701 | 20 | 20 | fits | 55,239 | 81 | 0.187 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 525,436 | 5.254 | 20 | 20 | fits | 24,450 | 41 | 0.095 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 356,732 | 3.567 | 20 | 20 | fits | 151,819 | 162 | 0.521 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 297,841 | 2.978 | 20 | 200 | fits | 154,859 | 229 | 0.345 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 458,391 | 4.584 | 20 | 200 | fits | 151,819 | 162 | 0.521 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 298,765 | 2.988 | 20 | 20 | fits | 154,859 | 229 | 0.345 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 459,095 | 4.591 | 20 | 20 | fits | 151,819 | 162 | 0.521 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 147,546 | 1.475 | 20 | 24 | fits | 147,732 | 164 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 301,415 | 3.014 | 20 | 24 | fits | 154,859 | 229 | 0.345 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 301,349 | 3.013 | 20 | 50 | fits | 154,859 | 229 | 0.345 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 462,119 | 4.621 | 20 | 50 | fits | 151,819 | 162 | 0.521 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 462,053 | 4.621 | 20 | 20 | fits | 151,819 | 162 | 0.521 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 803,524 | 8.035 | 20 | 20 | fits | 83,268 | 36 | 0.568 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 15,718 | 0.157 | 20 | 20 | fits | 30,269 | 19 | 0.766 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 297,841 | 2.978 | 20 | 200 | fits | 154,859 | 229 | 0.345 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 36,745 | 0.367 | 20 | 200 | fits | 30,269 | 19 | 0.766 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 298,765 | 2.988 | 20 | 20 | fits | 154,859 | 229 | 0.345 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 445,317 | 4.453 | 20 | 20 | fits | 138,041 | 152 | 0.486 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 147,546 | 1.475 | 20 | 24 | fits | 147,732 | 164 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 301,415 | 3.014 | 20 | 24 | fits | 154,859 | 229 | 0.345 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 301,349 | 3.013 | 20 | 50 | fits | 154,859 | 229 | 0.345 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 448,341 | 4.483 | 20 | 50 | fits | 138,041 | 152 | 0.486 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 448,275 | 4.483 | 20 | 20 | fits | 138,041 | 152 | 0.486 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 788,827 | 7.888 | 20 | 20 | fits | 83,268 | 36 | 0.568 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,320,096 | 63.201 | 20 | 20 | MISS ceiling | 20,766 | 13 | 0.422 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,340,808 | 63.408 | 20 | 20 | MISS ceiling | 20,788 | 13 | 0.396 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,361,453 | 63.615 | 20 | 20 | MISS ceiling | 20,702 | 13 | 0.404 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,382,133 | 63.821 | 20 | 20 | MISS ceiling | 20,756 | 13 | 0.396 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,402,660 | 64.027 | 20 | 20 | MISS ceiling | 20,590 | 13 | 0.422 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 149,996 | 1.500 | 20 | 200 | fits | 150,343 | 200 | 0.421 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 293,202 | 2.932 | 20 | 200 | fits | 143,822 | 189 | 0.432 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 145,674 | 1.457 | 20 | 20 | fits | 150,343 | 200 | 0.421 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,221,232 | 62.212 | 20 | 20 | MISS ceiling | 33,955 | 15 | 0.648 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 149,314 | 1.493 | 20 | 24 | fits | 150,343 | 200 | 0.421 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,156,726 | 61.567 | 20 | 24 | MISS ceiling | 138,354 | 107 | 0.439 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 148,258 | 1.483 | 20 | 50 | fits | 150,343 | 200 | 0.421 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 291,684 | 2.917 | 20 | 50 | fits | 143,822 | 189 | 0.432 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 291,618 | 2.916 | 20 | 20 | fits | 143,822 | 189 | 0.432 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 629,918 | 6.299 | 20 | 20 | fits | 87,454 | 42 | 0.585 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,416 | 0.054 | 20 | 20 | fits | 25,454 | 13 (29) | 0.667 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 8,764 | 0.088 | 20 | 20 | fits | 29,454 | 19 (35) | 0.750 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 19,513 | 0.195 | 20 | 20 | fits | 32,626 | 21 (12) | 0.787 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 14,424 | 0.144 | 20 | 50 | fits | 32,023 | 43 | 0.676 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 18,230 | 0.182 | 20 | 50 | fits | 28,110 | 35 | 0.610 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 14,470 | 0.145 | 20 | 50 | fits | 28,262 | 35 | 0.614 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 12,479 | 0.125 | 20 | 50 | fits | 33,387 | 61 | 0.564 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 14,429 | 0.144 | 20 | 50 | fits | 33,387 | 61 | 0.564 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 12,218 | 0.122 | 20 | 50 | fits | 27,775 | 30 | 0.596 |
| LINK_UP | `adp.link_up.if0` | 2,119 | 0.021 | 20 | 200 | fits | 32,023 | 43 (11) | 0.676 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,151 | 0.082 | 20 | 200 | fits | 21,213 | 23 (39) | 0.578 |
| LINK_DOWN | `adp.link_down.if0` | 1,695 | 0.017 | 20 | 200 | fits | 29,439 | 23 (9) | 0.667 |
| LINK_UP | `adp.link_up.if0` | 2,119 | 0.021 | 20 | 200 | fits | 32,023 | 43 (11) | 0.676 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,151 | 0.082 | 20 | 200 | fits | 21,213 | 23 (39) | 0.578 |
| GM_CHANGE | `adp.gm_change.if0` | 1,888 | 0.019 | 20 | 200 | fits | 16,478 | 17 (11) | 0.323 |
| LINK_UP | `adp.link_up.if0` | 2,119 | 0.021 | 20 | 200 | fits | 32,023 | 43 (11) | 0.676 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,151 | 0.082 | 20 | 200 | fits | 21,213 | 23 (39) | 0.578 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,070 | 0.041 | 20 | 200 | fits | 17,842 | 16 (31) | 0.508 |
| LINK_UP | `adp.link_up.if0` | 2,119 | 0.021 | 20 | 200 | fits | 32,023 | 43 (11) | 0.676 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,151 | 0.082 | 20 | 200 | fits | 21,213 | 23 (39) | 0.578 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,070 | 0.041 | 20 | 200 | fits | 17,842 | 16 (31) | 0.508 |
| set_name | `aecp_fanout.set_name.if0` | 59,544 | 0.595 | 20 | 24 | fits | 57,466 | 89 | 0.547 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 54,181 | 0.542 | 20 | 24 | fits | 52,942 | 78 | 0.592 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 37,421 | 0.374 | 20 | 24 | fits | 47,518 | 79 | 0.551 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 36,455 | 0.365 | 20 | 24 | fits | 47,323 | 78 | 0.539 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 51,818 | 0.518 | 20 | 24 | fits | 50,437 | 67 | 0.579 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 36,401 | 0.364 | 20 | 24 | fits | 47,250 | 78 | 0.547 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 51,103 | 0.511 | 20 | 24 | fits | 46,498 | 79 | 0.526 |
| BIND_RX | `acmp.bind_rx.if0` | 19,079 | 0.191 | 20 | 20 | fits | 42,885 | 26 (77) | 0.759 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,705 | 0.097 | 20 | 20 | fits | 32,802 | 19 (32) | 0.810 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 9,289 | 0.093 | 20 | 20 | fits | 25,770 | 15 (47) | 0.676 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 14,382 | 0.144 | 20 | 20 | fits | 40,274 | 18 (50) | 0.822 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 9,163 | 0.092 | 20 | 20 | fits | 26,049 | 17 (48) | 0.657 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 8,966 | 0.090 | 20 | 20 | fits | 25,230 | 16 (48) | 0.593 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 8,352 | 0.084 | 20 | 20 | fits | 24,451 | 16 (48) | 0.575 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,014 | 0.090 | 20 | 20 | fits | 25,791 | 16 (48) | 0.679 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 17,340 | 0.173 | 20 | 24 | fits | 28,084 | 20 | 0.758 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 27,274 | 0.273 | 20 | 24 | fits | 31,371 | 20 | 0.674 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 20,616 | 0.206 | 20 | 24 | fits | 27,932 | 20 | 0.706 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 23,592 | 0.236 | 20 | 24 | fits | 27,478 | 20 | 0.699 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 23,877 | 0.239 | 20 | 24 | fits | 28,045 | 20 | 0.697 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 20,823 | 0.208 | 20 | 24 | fits | 28,139 | 20 | 0.699 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 23,540 | 0.235 | 20 | 24 | fits | 27,426 | 20 | 0.704 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 19,858 | 0.199 | 20 | 24 | fits | 27,015 | 20 | 0.712 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 23,610 | 0.236 | 20 | 24 | fits | 27,497 | 20 | 0.724 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 28,421 | 0.284 | 20 | 24 | fits | 33,166 | 21 | 0.626 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 19,852 | 0.199 | 20 | 24 | fits | 27,085 | 20 | 0.738 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 23,228 | 0.232 | 20 | 24 | fits | 27,115 | 20 | 0.743 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 19,970 | 0.200 | 20 | 24 | fits | 27,285 | 20 | 0.703 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 24,206 | 0.242 | 20 | 24 | fits | 28,251 | 20 | 0.710 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 20,457 | 0.205 | 20 | 24 | fits | 27,773 | 20 | 0.704 |
| get_configuration | `aecp.get_configuration.if0` | 18,446 | 0.184 | 20 | 24 | fits | 25,598 | 20 | 0.731 |
| entity_available | `aecp.entity_available.if0` | 21,507 | 0.215 | 20 | 24 | fits | 25,056 | 20 | 0.714 |
| get_name | `aecp.get_name.if0` | 20,509 | 0.205 | 20 | 24 | fits | 27,948 | 20 | 0.731 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 25,521 | 0.255 | 20 | 24 | fits | 29,102 | 26 | 0.701 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 21,118 | 0.211 | 20 | 24 | fits | 28,397 | 29 | 0.719 |
| get_as_path, refused ENTITY_MISBEHAVING | `aecp.get_as_path.if0` | 10,720 | 0.107 | 20 | 24 | fits | 28,344 | 28 | 0.740 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 22,524 | 0.225 | 20 | 24 | fits | 25,881 | 20 | 0.747 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 17,691 | 0.177 | 20 | 24 | fits | 24,693 | 20 | 0.708 |
| set_name | `aecp.set_name.if0` | 30,402 | 0.304 | 20 | 24 | fits | 44,655 | 43 | 0.742 |
| lock_entity | `aecp.lock_entity.if0` | 23,607 | 0.236 | 20 | 24 | fits | 35,289 | 34 | 0.768 |
| unlock_entity | `aecp.unlock_entity.if0` | 24,443 | 0.244 | 20 | 24 | fits | 35,180 | 33 | 0.779 |
| READ_DESCRIPTOR held for a token (#917) | `aecp.held.read_descriptor.if0` | 519,357 | 5.194 | 20 | 24 | fits | 31,760 | 17 | 0.699 |
| LINK_UP | `fixture.link_up.if0` | 2,119 | 0.021 | 20 | 200 | fits | 32,023 | 43 (11) | 0.676 |
| malformed MRPDU discard | `fixture.malformed.if0` | 22,229 | 0.222 | 20 | 20 | fits | 22,295 | 12 | 0.723 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 32,367 | 0.324 | 20 | 24 | fits | 46,165 | 43 | 0.759 |
| LINK_DOWN | `fixture.link_down.if0` | 2,062 | 0.021 | 20 | 200 | fits | 30,882 | 23 (9) | 0.713 |
| BIND_RX | `fixture.bind_rx.if0` | 18,409 | 0.184 | 20 | 20 | fits | 42,792 | 26 (77) | 0.766 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 11,064 | 0.111 | 20 | 20 | fits | 40,340 | 29 (35) | 0.757 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 17,106 | 0.171 | 20 | 20 | fits | 26,720 | 13 (29) | 0.737 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 86,879 | 0.869 | 20 | 200 | fits | 86,983 | 75 | 0.736 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 86,879 | 0.869 | 20 | 200 | fits | 86,983 | 75 | 0.736 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 86,605 | 0.866 | 20 | 20 | fits | 86,983 | 75 | 0.736 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 86,605 | 0.866 | 20 | 20 | fits | 86,983 | 75 | 0.736 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 86,813 | 0.868 | 20 | 24 | fits | 86,983 | 75 | 0.736 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 86,813 | 0.868 | 20 | 24 | fits | 86,983 | 75 | 0.736 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 86,747 | 0.867 | 20 | 50 | fits | 86,983 | 75 | 0.736 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 86,747 | 0.867 | 20 | 50 | fits | 86,983 | 75 | 0.736 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 86,681 | 0.867 | 20 | 20 | fits | 86,983 | 75 | 0.736 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 86,681 | 0.867 | 20 | 20 | fits | 86,983 | 75 | 0.736 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
