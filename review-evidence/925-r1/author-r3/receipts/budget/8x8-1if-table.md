Round 3 CPU-budget 8x8/1if row table; measured firmware byte-identical at 5f625090
### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 85 paths and 7 of 947 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.205 (0.493) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.096 (0.306) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.100 (0.355) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.085 (0.328) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.104 (0.326) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.094 (0.304) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.162 (0.397) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.108 (0.322) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.105 (0.371) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.365 (0.843) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.168 (0.642) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.314 (0.883) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.111 (0.599) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.102 (0.637) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.186 (0.689) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.146 (0.456) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.047 (0.230) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.023 (0.229) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.027 (0.378) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.028 (0.377) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.078 (0.303) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.191 (0.634) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.233 (0.670) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.132 (0.565) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.179 (0.608) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.211 (0.645) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.254 (0.696) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.233 (0.753) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.231 (0.669) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.293 (0.741) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.206 (0.641) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.197 (0.631) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.203 (0.648) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.301 (0.751) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.198 (0.632) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.250 (0.694) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.258 (0.702) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.250 (0.694) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.205 (0.641) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.259 (0.706) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.254 (0.699) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.207 (0.641) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.253 (0.697) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.183 (0.622) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.317 (0.862) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.183 (0.611) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.298 (0.781) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.620 (0.988) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.456 (0.844) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.629 (0.991) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.669 (1.089) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.455 (0.842) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.435 (0.799) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.875 (5.181) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 4.871 (5.493) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.269 (0.766) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.646 (2.161) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.520 (63.948) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.582 (65.001) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.353 (0.503) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 3.228 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.782 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 3.155 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 2.833 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 9.045 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.209 (0.656) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.142 (0.332) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.162 (0.377) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.191 (0.656) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.284 (0.717) | fits | 0 events | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.624 | fits | 0 srp | 6 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.329 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.336 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.372 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 5.488 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.aecp.first.if0` (backlog-adp@verify-0) | 2.329 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.973 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.355 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.maap.last.if0` (backlog-adp@program-aged2-7) | 5.525 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-6.service.srp.first.if0` (backlog-adp@program-aged2-6) | 6.503 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-5.service.srp.last.if0` (backlog-adp@verify-aged2-5) | 10.515 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.805 (0.852) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.469 (0.470) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.271 (0.271) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.842 (0.912) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.720 | 10 | 156,437 (1.564) | yes | - |
| backlog-adp@blank-1 | 0 | 10.899 | 10 | 155,789 (1.558) | yes | - |
| backlog-adp@blank-2 | 0 | 10.953 | 10 | 155,800 (1.558) | yes | - |
| backlog-adp@blank-3 | 0 | 11.004 | 10 | 156,400 (1.564) | yes | - |
| backlog-adp@blank-4 | 0 | 11.645 | 12 | 160,682 (1.607) | yes | - |
| backlog-adp@blank-5 | 0 | 11.160 | 11 | 156,857 (1.569) | yes | - |
| backlog-adp@blank-6 | 1 | 10.909 | 9 | 155,091 (1.551) | yes | - |
| backlog-adp@blank-7 | 0 | 10.912 | 10 | 158,408 (1.584) | yes | - |
| backlog-adp@program-0 | 0 | 10.979 | 10 | 156,602 (1.566) | yes | - |
| backlog-adp@program-1 | 0 | 11.517 | 12 | 159,886 (1.599) | yes | - |
| backlog-adp@program-2 | 0 | 10.674 | 9 | 161,662 (1.617) | yes | - |
| backlog-adp@program-3 | 0 | 11.079 | 10 | 158,300 (1.583) | yes | - |
| backlog-adp@program-4 | 0 | 10.281 | 10 | 159,891 (1.599) | yes | - |
| backlog-adp@program-5 | 0 | 10.342 | 10 | 156,112 (1.561) | yes | - |
| backlog-adp@program-6 | 0 | 10.279 | 10 | 156,437 (1.564) | yes | - |
| backlog-adp@program-7 | 0 | 10.364 | 10 | 156,772 (1.568) | yes | - |
| backlog-adp@verify-0 | 0 | 11.731 | 10 | 156,268 (1.563) | yes | - |
| backlog-adp@verify-1 | 0 | 10.908 | 10 | 155,719 (1.557) | yes | - |
| backlog-adp@verify-2 | 0 | 10.969 | 10 | 156,066 (1.561) | yes | - |
| backlog-adp@verify-3 | 0 | 11.020 | 10 | 156,679 (1.567) | yes | - |
| backlog-adp@verify-4 | 0 | 11.398 | 11 | 160,455 (1.605) | yes | - |
| backlog-adp@verify-5 | 0 | 11.068 | 11 | 155,530 (1.555) | yes | - |
| backlog-adp@verify-6 | 0 | 11.079 | 10 | 154,437 (1.544) | yes | - |
| backlog-adp@verify-7 | 0 | 12.376 | 11 | 157,288 (1.573) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 11.862 | 10 | 155,913 (1.559) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 11.123 | 10 | 160,830 (1.608) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 11.076 | 11 | 156,076 (1.561) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 10.950 | 10 | 155,638 (1.556) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 11.058 | 10 | 156,041 (1.560) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 10.938 | 10 | 161,702 (1.617) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 11.001 | 10 | 155,360 (1.554) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 12.419 | 11 | 158,563 (1.586) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 11.139 | 11 | 155,638 (1.556) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 10.775 | 9 | 161,731 (1.617) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 11.875 | 12 | 160,129 (1.601) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 11.754 | 12 | 158,340 (1.583) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 11.132 | 11 | 156,786 (1.568) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 10.893 | 10 | 156,244 (1.562) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 10.992 | 10 | 154,989 (1.550) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 12.317 | 10 | 160,312 (1.603) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.357 | 11 | 156,776 (1.568) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 11.109 | 11 | 156,837 (1.568) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 10.959 | 10 | 156,295 (1.563) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 11.052 | 10 | 156,263 (1.563) | yes | - |
| backlog-adp@program-aged2-4 | 1 | 10.920 | 9 | 156,551 (1.566) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 11.008 | 10 | 155,964 (1.560) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 11.885 | 12 | 157,804 (1.578) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 11.658 | 12 | 158,747 (1.587) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 11.286 | 10 | 156,551 (1.566) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 11.533 | 12 | 160,462 (1.605) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 11.178 | 11 | 157,498 (1.575) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 11.054 | 10 | 155,676 (1.557) | yes | - |
| backlog-adp@program-aged1-4 | 1 | 10.926 | 9 | 155,676 (1.557) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 11.012 | 10 | 155,689 (1.557) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 10.858 | 9 | 161,684 (1.617) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 11.768 | 11 | 160,201 (1.602) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.042 | 11 | 156,263 (1.563) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 10.937 | 10 | 156,263 (1.563) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 11.027 | 10 | 155,676 (1.557) | yes | - |
| backlog-adp@verify-aged2-3 | 1 | 10.878 | 9 | 155,964 (1.560) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 11.461 | 11 | 159,581 (1.596) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 11.217 | 11 | 155,275 (1.553) | yes | - |
| backlog-adp@verify-aged2-6 | 1 | 10.908 | 9 | 154,822 (1.548) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 12.415 | 11 | 157,850 (1.579) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 11.908 | 11 | 157,498 (1.575) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 11.101 | 11 | 156,127 (1.561) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 10.708 | 9 | 161,500 (1.615) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 10.842 | 9 | 155,689 (1.557) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 10.933 | 10 | 156,380 (1.564) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 11.045 | 10 | 157,085 (1.571) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 11.882 | 12 | 158,613 (1.586) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 12.343 | 12 | 159,982 (1.600) | yes | - |
| backlog | 0 | 6.822 | 8 | 155,790 (1.558) | yes | - |
| backlog-adp | 0 | 9.868 | 9 | 162,023 (1.620) | yes | - |
| backlog-adp-refill | 0 | 41.193 | 23 | 162,023 (1.620) | yes | - |
| backlog-owed | 0 | 65.486 | 24 | 153,876 (1.539) | yes | - |
| fixture | 0 | 1.562 | 2 | 89,774 (0.898) | yes | - |

Composed maximum over the 4 backlog windows: 162,023 CPU cycles (1.620 ms), backlog-adp.
Over the windows that released their whole load only: 162,023 (1.620 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 107628 | 0 | 55,174 (0.552) | fits |
| save-held | 3297 | 0 | 160,234 (1.602) | fits |
| save-starved | 51402 | 0 | 160,876 (1.609) | fits |
| acmp-notk | 3607 | 0 | 49,254 (0.493) | fits |
| backlog-adp@blank-0 | 538 | 0 | 156,437 (1.564) | fits |
| backlog-adp@blank-1 | 538 | 0 | 155,789 (1.558) | fits |
| backlog-adp@blank-2 | 538 | 0 | 155,800 (1.558) | fits |
| backlog-adp@blank-3 | 538 | 0 | 156,400 (1.564) | fits |
| backlog-adp@blank-4 | 540 | 0 | 160,682 (1.607) | fits |
| backlog-adp@blank-5 | 539 | 0 | 156,857 (1.569) | fits |
| backlog-adp@blank-6 | 539 | 0 | 155,091 (1.551) | fits |
| backlog-adp@blank-7 | 540 | 0 | 158,408 (1.584) | fits |
| backlog-adp@program-0 | 894 | 0 | 156,602 (1.566) | fits |
| backlog-adp@program-1 | 896 | 0 | 159,886 (1.599) | fits |
| backlog-adp@program-2 | 895 | 0 | 161,662 (1.617) | fits |
| backlog-adp@program-3 | 896 | 0 | 158,300 (1.583) | fits |
| backlog-adp@program-4 | 897 | 0 | 159,891 (1.599) | fits |
| backlog-adp@program-5 | 898 | 0 | 156,112 (1.561) | fits |
| backlog-adp@program-6 | 899 | 0 | 156,437 (1.564) | fits |
| backlog-adp@program-7 | 899 | 0 | 156,772 (1.568) | fits |
| backlog-adp@verify-0 | 1244 | 0 | 156,268 (1.563) | fits |
| backlog-adp@verify-1 | 1244 | 0 | 155,719 (1.557) | fits |
| backlog-adp@verify-2 | 1244 | 0 | 156,066 (1.561) | fits |
| backlog-adp@verify-3 | 1244 | 0 | 156,679 (1.567) | fits |
| backlog-adp@verify-4 | 1245 | 0 | 160,455 (1.605) | fits |
| backlog-adp@verify-5 | 1245 | 0 | 155,530 (1.555) | fits |
| backlog-adp@verify-6 | 1246 | 0 | 154,437 (1.544) | fits |
| backlog-adp@verify-7 | 1247 | 0 | 157,288 (1.573) | fits |
| backlog-adp@blank-aged2-0 | 753 | 0 | 155,913 (1.559) | fits |
| backlog-adp@blank-aged2-1 | 759 | 0 | 160,830 (1.608) | fits |
| backlog-adp@blank-aged2-2 | 765 | 0 | 156,076 (1.561) | fits |
| backlog-adp@blank-aged2-3 | 770 | 0 | 155,638 (1.556) | fits |
| backlog-adp@blank-aged2-4 | 776 | 0 | 156,041 (1.560) | fits |
| backlog-adp@blank-aged2-5 | 781 | 0 | 161,702 (1.617) | fits |
| backlog-adp@blank-aged2-6 | 787 | 0 | 155,360 (1.554) | fits |
| backlog-adp@blank-aged2-7 | 794 | 0 | 158,563 (1.586) | fits |
| backlog-adp@blank-aged1-0 | 709 | 0 | 155,638 (1.556) | fits |
| backlog-adp@blank-aged1-1 | 713 | 0 | 161,731 (1.617) | fits |
| backlog-adp@blank-aged1-2 | 721 | 0 | 160,129 (1.601) | fits |
| backlog-adp@blank-aged1-3 | 727 | 0 | 158,340 (1.583) | fits |
| backlog-adp@blank-aged1-4 | 731 | 0 | 156,786 (1.568) | fits |
| backlog-adp@blank-aged1-5 | 736 | 0 | 156,244 (1.562) | fits |
| backlog-adp@blank-aged1-6 | 742 | 0 | 154,989 (1.550) | fits |
| backlog-adp@blank-aged1-7 | 748 | 0 | 160,312 (1.603) | fits |
| backlog-adp@program-aged2-0 | 1107 | 0 | 156,776 (1.568) | fits |
| backlog-adp@program-aged2-1 | 1112 | 0 | 156,837 (1.568) | fits |
| backlog-adp@program-aged2-2 | 1117 | 0 | 156,295 (1.563) | fits |
| backlog-adp@program-aged2-3 | 1123 | 0 | 156,263 (1.563) | fits |
| backlog-adp@program-aged2-4 | 1128 | 0 | 156,551 (1.566) | fits |
| backlog-adp@program-aged2-5 | 1134 | 0 | 155,964 (1.560) | fits |
| backlog-adp@program-aged2-6 | 1142 | 0 | 157,804 (1.578) | fits |
| backlog-adp@program-aged2-7 | 1147 | 0 | 158,747 (1.587) | fits |
| backlog-adp@program-aged1-0 | 1061 | 0 | 156,551 (1.566) | fits |
| backlog-adp@program-aged1-1 | 1068 | 0 | 160,462 (1.605) | fits |
| backlog-adp@program-aged1-2 | 1073 | 0 | 157,498 (1.575) | fits |
| backlog-adp@program-aged1-3 | 1078 | 0 | 155,676 (1.557) | fits |
| backlog-adp@program-aged1-4 | 1083 | 0 | 155,676 (1.557) | fits |
| backlog-adp@program-aged1-5 | 1089 | 0 | 155,689 (1.557) | fits |
| backlog-adp@program-aged1-6 | 1094 | 0 | 161,684 (1.617) | fits |
| backlog-adp@program-aged1-7 | 1101 | 0 | 160,201 (1.602) | fits |
| backlog-adp@verify-aged2-0 | 1460 | 0 | 156,263 (1.563) | fits |
| backlog-adp@verify-aged2-1 | 1464 | 0 | 156,263 (1.563) | fits |
| backlog-adp@verify-aged2-2 | 1470 | 0 | 155,676 (1.557) | fits |
| backlog-adp@verify-aged2-3 | 1475 | 0 | 155,964 (1.560) | fits |
| backlog-adp@verify-aged2-4 | 1482 | 0 | 159,581 (1.596) | fits |
| backlog-adp@verify-aged2-5 | 1488 | 0 | 155,275 (1.553) | fits |
| backlog-adp@verify-aged2-6 | 1493 | 0 | 154,822 (1.548) | fits |
| backlog-adp@verify-aged2-7 | 1499 | 0 | 157,850 (1.579) | fits |
| backlog-adp@verify-aged1-0 | 1414 | 0 | 157,498 (1.575) | fits |
| backlog-adp@verify-aged1-1 | 1420 | 0 | 156,127 (1.561) | fits |
| backlog-adp@verify-aged1-2 | 1424 | 0 | 161,500 (1.615) | fits |
| backlog-adp@verify-aged1-3 | 1430 | 0 | 155,689 (1.557) | fits |
| backlog-adp@verify-aged1-4 | 1436 | 0 | 156,380 (1.564) | fits |
| backlog-adp@verify-aged1-5 | 1442 | 0 | 157,085 (1.571) | fits |
| backlog-adp@verify-aged1-6 | 1449 | 0 | 158,613 (1.586) | fits |
| backlog-adp@verify-aged1-7 | 1455 | 0 | 159,982 (1.600) | fits |
| adp-advertise | 598 | 0 | 38,886 (0.389) | fits |
| acmp-noresp | 2022 | 0 | 49,254 (0.493) | fits |
| save | 610 | 0 | 50,069 (0.501) | fits |
| srp | 290 | 0 | 47,003 (0.470) | fits |
| backlog | 287 | 0 | 155,790 (1.558) | fits |
| backlog-adp | 311 | 0 | 162,023 (1.620) | fits |
| backlog-adp-refill | 325 | 0 | 162,023 (1.620) | fits |
| backlog-owed | 309 | 0 | 153,876 (1.539) | fits |
| acmp-disc | 936 | 0 | 49,254 (0.493) | fits |
| maap | 187 | 0 | 38,886 (0.389) | fits |
| adp-link | 89 | 0 | 47,012 (0.470) | fits |
| adp-gm | 88 | 0 | 37,741 (0.377) | fits |
| adp-discover | 88 | 0 | 37,741 (0.377) | fits |
| control | 88 | 0 | 37,741 (0.377) | fits |
| aecp-fanout | 110 | 0 | 63,319 (0.633) | fits |
| acmp-cmd | 87 | 0 | 49,254 (0.493) | fits |
| aecp | 113 | 0 | 49,274 (0.493) | fits |
| datapath-events | 114 | 0 | 37,741 (0.377) | fits |
| fixture | 151 | 0 | 89,774 (0.898) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 9.173 (20) | 10.827 |
| backlog-adp@blank-aged2-1 | 2 | none | +9.141 ms, 76,542 (0.765 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 9.104 (20) | 10.896 |
| backlog-adp@blank-aged2-2 | 2 | +8.234 ms, 76,542 (0.765 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 10.375 (20) | 9.625 |
| backlog-adp@blank-aged2-3 | 2 | +7.223 ms, 76,542 (0.765 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 10.250 (20) | 9.750 |
| backlog-adp@blank-aged2-4 | 2 | +5.635 ms, 76,728 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 10.356 (20) | 9.644 |
| backlog-adp@blank-aged2-5 | 2 | +4.668 ms, 76,590 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 10.236 (20) | 9.764 |
| backlog-adp@blank-aged2-6 | 2 | none | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 10.295 (20) | 9.705 |
| backlog-adp@blank-aged2-7 | 2 | +4.670 ms, 76,726 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 10.168 (20) | 9.832 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 9.427 (20) | 10.573 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 9.311 (20) | 10.689 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 9.441 (20) | 10.559 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 9.535 (20) | 10.465 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 9.136 (20) | 10.864 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 9.433 (20) | 10.567 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 9.532 (20) | 10.468 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 9.413 (20) | 10.587 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 9.226 (20) | 10.774 |
| backlog-adp@program-aged2-1 | 2 | +9.107 ms, 80,868 (0.809 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 10.279 (20) | 9.721 |
| backlog-adp@program-aged2-2 | 2 | +8.233 ms, 80,764 (0.808 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 10.257 (20) | 9.743 |
| backlog-adp@program-aged2-3 | 2 | +7.437 ms, 80,758 (0.808 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 10.349 (20) | 9.651 |
| backlog-adp@program-aged2-4 | 2 | +5.526 ms, 81,048 (0.810 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 10.215 (20) | 9.785 |
| backlog-adp@program-aged2-5 | 2 | +5.614 ms, 81,048 (0.810 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 10.304 (20) | 9.696 |
| backlog-adp@program-aged2-6 | 2 | +4.851 ms, 80,712 (0.807 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 10.381 (20) | 9.619 |
| backlog-adp@program-aged2-7 | 2 | +3.147 ms, 80,743 (0.807 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 10.428 (20) | 9.572 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 9.253 (20) | 10.747 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 9.443 (20) | 10.557 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 9.668 (20) | 10.332 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 9.543 (20) | 10.457 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 9.414 (20) | 10.586 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 9.501 (20) | 10.499 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 9.342 (20) | 10.658 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 9.190 (20) | 10.810 |
| backlog-adp@verify-aged2-0 | 2 | none | +9.813 ms, 77,028 (0.770 ms), read-back | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 9.519 (20) | 10.481 |
| backlog-adp@verify-aged2-1 | 2 | +9.053 ms, 77,241 (0.772 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 10.234 (20) | 9.766 |
| backlog-adp@verify-aged2-2 | 2 | +8.255 ms, 77,241 (0.772 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 10.325 (20) | 9.675 |
| backlog-adp@verify-aged2-3 | 2 | +7.308 ms, 77,241 (0.772 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 10.173 (20) | 9.827 |
| backlog-adp@verify-aged2-4 | 2 | +5.704 ms, 77,453 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 9.998 (20) | 10.002 |
| backlog-adp@verify-aged2-5 | 2 | +4.845 ms, 77,425 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 10.515 (20) | 9.485 |
| backlog-adp@verify-aged2-6 | 2 | +4.542 ms, 77,399 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 10.207 (20) | 9.793 |
| backlog-adp@verify-aged2-7 | 2 | +3.115 ms, 77,397 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 10.254 (20) | 9.746 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 9.055 (20) | 10.945 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 9.507 (20) | 10.493 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 9.238 (20) | 10.762 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 9.374 (20) | 10.626 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 9.462 (20) | 10.538 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 9.573 (20) | 10.427 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 9.436 (20) | 10.564 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 9.273 (20) | 10.727 |

Least margin over the aged windows: 9.485 ms, `backlog-adp@verify-aged2-5.service.srp.last.if0` at 10.515 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 22829.558 | 22,870 | 382 | 2 | 31.309 | yes | within |
| save-held | 4818.186 | 12,470 | 382 | - | 15.671 | no | within |
| save-starved | 12448.003 | 12,470 | 382 | - | 32.526 | yes | within |
| save | 4818.745 | 12,470 | 382 | - | 10.878 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1080 | 81,117 (0.811) | 77,888 (0.779) |
| save-held | 1562 | 103,459 (1.035) | 78,489 (0.785) |
| save-starved | 698 | 81,922 (0.819) | 78,531 (0.785) |
| acmp-notk | 1065 | 111,096 (1.111) | 78,630 (0.786) |
| backlog-adp@blank-0 | 339 | 97,982 (0.980) | 75,964 (0.760) |
| backlog-adp@blank-1 | 339 | 97,982 (0.980) | 75,964 (0.760) |
| backlog-adp@blank-2 | 339 | 97,917 (0.979) | 75,964 (0.760) |
| backlog-adp@blank-3 | 339 | 98,191 (0.982) | 75,964 (0.760) |
| backlog-adp@blank-4 | 339 | 98,249 (0.982) | 75,964 (0.760) |
| backlog-adp@blank-5 | 339 | 105,671 (1.057) | 76,264 (0.763) |
| backlog-adp@blank-6 | 339 | 97,879 (0.979) | 75,964 (0.760) |
| backlog-adp@blank-7 | 339 | 97,917 (0.979) | 75,964 (0.760) |
| backlog-adp@program-0 | 448 | 103,065 (1.031) | 78,686 (0.787) |
| backlog-adp@program-1 | 448 | 103,065 (1.031) | 78,822 (0.788) |
| backlog-adp@program-2 | 448 | 103,065 (1.031) | 78,822 (0.788) |
| backlog-adp@program-3 | 448 | 103,065 (1.031) | 78,822 (0.788) |
| backlog-adp@program-4 | 449 | 103,065 (1.031) | 78,369 (0.784) |
| backlog-adp@program-5 | 449 | 103,065 (1.031) | 78,369 (0.784) |
| backlog-adp@program-6 | 449 | 103,065 (1.031) | 78,369 (0.784) |
| backlog-adp@program-7 | 449 | 103,065 (1.031) | 78,369 (0.784) |
| backlog-adp@verify-0 | 555 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-1 | 555 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-2 | 555 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-3 | 555 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-4 | 555 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-5 | 555 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-6 | 555 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-7 | 556 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@blank-aged2-0 | 338 | 98,532 (0.985) | 76,123 (0.761) |
| backlog-adp@blank-aged2-1 | 337 | 82,190 (0.822) | 75,680 (0.757) |
| backlog-adp@blank-aged2-2 | 337 | 82,190 (0.822) | 75,680 (0.757) |
| backlog-adp@blank-aged2-3 | 337 | 82,190 (0.822) | 75,680 (0.757) |
| backlog-adp@blank-aged2-4 | 337 | 82,190 (0.822) | 75,680 (0.757) |
| backlog-adp@blank-aged2-5 | 337 | 82,190 (0.822) | 75,618 (0.756) |
| backlog-adp@blank-aged2-6 | 337 | 85,715 (0.857) | 75,789 (0.758) |
| backlog-adp@blank-aged2-7 | 338 | 96,799 (0.968) | 75,754 (0.758) |
| backlog-adp@blank-aged1-0 | 337 | 97,458 (0.975) | 75,987 (0.760) |
| backlog-adp@blank-aged1-1 | 337 | 98,414 (0.984) | 76,123 (0.761) |
| backlog-adp@blank-aged1-2 | 337 | 98,408 (0.984) | 76,123 (0.761) |
| backlog-adp@blank-aged1-3 | 337 | 98,408 (0.984) | 76,123 (0.761) |
| backlog-adp@blank-aged1-4 | 337 | 105,746 (1.057) | 76,423 (0.764) |
| backlog-adp@blank-aged1-5 | 337 | 98,076 (0.981) | 76,123 (0.761) |
| backlog-adp@blank-aged1-6 | 337 | 98,076 (0.981) | 76,123 (0.761) |
| backlog-adp@blank-aged1-7 | 338 | 98,076 (0.981) | 76,123 (0.761) |
| backlog-adp@program-aged2-0 | 447 | 109,620 (1.096) | 78,934 (0.789) |
| backlog-adp@program-aged2-1 | 446 | 103,065 (1.031) | 78,609 (0.786) |
| backlog-adp@program-aged2-2 | 446 | 103,065 (1.031) | 78,607 (0.786) |
| backlog-adp@program-aged2-3 | 446 | 103,065 (1.031) | 78,607 (0.786) |
| backlog-adp@program-aged2-4 | 446 | 103,065 (1.031) | 78,609 (0.786) |
| backlog-adp@program-aged2-5 | 446 | 103,065 (1.031) | 78,609 (0.786) |
| backlog-adp@program-aged2-6 | 446 | 103,065 (1.031) | 78,369 (0.784) |
| backlog-adp@program-aged2-7 | 447 | 103,065 (1.031) | 78,438 (0.784) |
| backlog-adp@program-aged1-0 | 447 | 103,065 (1.031) | 78,822 (0.788) |
| backlog-adp@program-aged1-1 | 446 | 103,065 (1.031) | 78,822 (0.788) |
| backlog-adp@program-aged1-2 | 446 | 103,065 (1.031) | 78,822 (0.788) |
| backlog-adp@program-aged1-3 | 446 | 103,065 (1.031) | 78,822 (0.788) |
| backlog-adp@program-aged1-4 | 446 | 103,065 (1.031) | 78,822 (0.788) |
| backlog-adp@program-aged1-5 | 446 | 103,065 (1.031) | 78,822 (0.788) |
| backlog-adp@program-aged1-6 | 446 | 103,065 (1.031) | 78,822 (0.788) |
| backlog-adp@program-aged1-7 | 447 | 103,065 (1.031) | 78,822 (0.788) |
| backlog-adp@verify-aged2-0 | 555 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-aged2-1 | 555 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-aged2-2 | 555 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-aged2-3 | 555 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-aged2-4 | 555 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-aged2-5 | 555 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-aged2-6 | 555 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-aged2-7 | 556 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-aged1-0 | 556 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-aged1-1 | 555 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-aged1-2 | 555 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-aged1-3 | 555 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-aged1-4 | 555 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-aged1-5 | 555 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-aged1-6 | 555 | 107,044 (1.070) | 78,674 (0.787) |
| backlog-adp@verify-aged1-7 | 556 | 107,044 (1.070) | 78,674 (0.787) |
| adp-advertise | 577 | 29,032 (0.290) | 2,296 (0.023) |
| acmp-noresp | 615 | 110,922 (1.109) | 78,595 (0.786) |
| save | 585 | 102,907 (1.029) | 78,029 (0.780) |
| srp | 271 | 29,032 (0.290) | 2,296 (0.023) |
| backlog | 265 | 29,032 (0.290) | 2,296 (0.023) |
| backlog-adp | 271 | 29,032 (0.290) | 2,453 (0.025) |
| backlog-adp-refill | 274 | 29,032 (0.290) | 2,453 (0.025) |
| backlog-owed | 277 | 29,032 (0.290) | 2,348 (0.023) |
| acmp-disc | 306 | 110,922 (1.109) | 75,630 (0.756) |
| maap | 174 | 28,778 (0.288) | 2,296 (0.023) |
| adp-link | 79 | 28,778 (0.288) | 2,296 (0.023) |
| adp-gm | 79 | 28,778 (0.288) | 2,296 (0.023) |
| adp-discover | 79 | 28,778 (0.288) | 2,296 (0.023) |
| control | 79 | 28,778 (0.288) | 2,296 (0.023) |
| aecp-fanout | 79 | 28,778 (0.288) | 2,327 (0.023) |
| acmp-cmd | 66 | 28,778 (0.288) | 2,323 (0.023) |
| aecp | 80 | 28,778 (0.288) | 2,296 (0.023) |
| datapath-events | 70 | 28,778 (0.288) | 2,296 (0.023) |
| fixture | 54 | 23,671 (0.237) | 2,296 (0.023) |

Longest pass that carries a step: 111,096 CPU cycles (1.111 ms), acmp-notk; longest step: 78,934 (0.789 ms), backlog-adp@program-aged2-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 275,245 | 2.752 | 20 | 200 | fits | 116,381 | 142 | 0.415 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 255,108 | 2.551 | 20 | 20 | fits | 116,381 | 142 | 0.415 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 302,403 | 3.024 | 20 | 24 | fits | 88,015 | 54 | 0.599 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 215,633 | 2.156 | 20 | 50 | fits | 116,381 | 142 | 0.415 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 853,656 | 8.537 | 20 | 20 | fits | 70,851 | 28 | 0.593 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 132,543 | 1.325 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 179,313 | 1.793 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 226,515 | 2.265 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 278,186 | 2.782 | 20 | 200 | fits | 119,322 | 148 | 0.439 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 322,758 | 3.228 | 20 | 20 | fits | 96,772 | 83 | 0.548 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 315,503 | 3.155 | 20 | 24 | fits | 89,524 | 61 | 0.594 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 283,283 | 2.833 | 20 | 50 | fits | 96,772 | 83 | 0.548 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 904,504 | 9.045 | 20 | 20 | fits | 46,861 | 22 | 0.761 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 127,529 | 1.275 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 189,163 | 1.892 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 262,353 | 2.624 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 10,165 | 0.102 | 20 | 20 | fits | 41,369 | 19 (14) | 0.892 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 472,499 | 4.725 | 20 | 20 | fits | 156,437 | 183 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 378,800 | 3.788 | 20 | 200 | fits | 150,979 | 193 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 534,621 | 5.346 | 20 | 200 | fits | 156,437 | 183 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 379,724 | 3.797 | 20 | 20 | fits | 150,979 | 193 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 621,360 | 6.214 | 20 | 20 | fits | 86,035 | 31 | 0.742 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 232,385 | 2.324 | 20 | 24 | fits | 150,973 | 155 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 382,374 | 3.824 | 20 | 24 | fits | 150,979 | 193 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 382,308 | 3.823 | 20 | 50 | fits | 150,979 | 193 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 538,349 | 5.383 | 20 | 50 | fits | 156,437 | 183 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 624,318 | 6.243 | 20 | 20 | fits | 86,035 | 31 | 0.742 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,026,101 | 10.261 | 20 | 20 | fits | 41,232 | 18 | 0.837 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 390,861 | 3.909 | 20 | 20 | fits | 155,789 | 184 | 0.370 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 297,229 | 2.972 | 20 | 200 | fits | 150,795 | 193 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 452,402 | 4.524 | 20 | 200 | fits | 155,789 | 184 | 0.370 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 298,153 | 2.982 | 20 | 20 | fits | 150,795 | 193 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 539,243 | 5.392 | 20 | 20 | fits | 86,137 | 31 | 0.743 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 150,998 | 1.510 | 20 | 24 | fits | 150,424 | 155 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 300,803 | 3.008 | 20 | 24 | fits | 150,795 | 193 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 300,737 | 3.007 | 20 | 50 | fits | 150,795 | 193 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 456,130 | 4.561 | 20 | 50 | fits | 155,789 | 184 | 0.370 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 542,201 | 5.422 | 20 | 20 | fits | 86,137 | 31 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 944,050 | 9.441 | 20 | 20 | fits | 41,254 | 18 | 0.837 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 396,357 | 3.964 | 20 | 20 | fits | 155,800 | 184 | 0.371 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 302,762 | 3.028 | 20 | 200 | fits | 150,522 | 193 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 457,946 | 4.579 | 20 | 200 | fits | 155,800 | 184 | 0.371 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 303,686 | 3.037 | 20 | 20 | fits | 150,522 | 193 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 544,795 | 5.448 | 20 | 20 | fits | 86,145 | 32 | 0.740 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 156,804 | 1.568 | 20 | 24 | fits | 150,424 | 155 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 306,336 | 3.063 | 20 | 24 | fits | 150,522 | 193 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 306,270 | 3.063 | 20 | 50 | fits | 150,522 | 193 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 461,674 | 4.617 | 20 | 50 | fits | 155,800 | 184 | 0.371 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 547,753 | 5.478 | 20 | 20 | fits | 86,145 | 32 | 0.740 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 949,521 | 9.495 | 20 | 20 | fits | 44,139 | 16 | 0.738 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 401,971 | 4.020 | 20 | 20 | fits | 156,400 | 184 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 308,554 | 3.086 | 20 | 200 | fits | 150,508 | 193 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 464,338 | 4.643 | 20 | 200 | fits | 156,400 | 184 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 309,478 | 3.095 | 20 | 20 | fits | 150,508 | 193 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 565,238 | 5.652 | 20 | 20 | fits | 90,412 | 38 | 0.757 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 162,610 | 1.626 | 20 | 24 | fits | 150,424 | 155 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 312,128 | 3.121 | 20 | 24 | fits | 150,508 | 193 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 312,062 | 3.121 | 20 | 50 | fits | 150,508 | 193 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 468,066 | 4.681 | 20 | 50 | fits | 156,400 | 184 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 568,196 | 5.682 | 20 | 20 | fits | 90,412 | 38 | 0.757 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 954,299 | 9.543 | 20 | 20 | fits | 34,985 | 12 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 422,232 | 4.222 | 20 | 20 | fits | 160,682 | 190 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 314,961 | 3.150 | 20 | 200 | fits | 151,109 | 194 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 484,505 | 4.845 | 20 | 200 | fits | 160,682 | 190 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 315,885 | 3.159 | 20 | 20 | fits | 151,109 | 194 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 569,323 | 5.693 | 20 | 20 | fits | 84,114 | 35 | 0.766 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 168,416 | 1.684 | 20 | 24 | fits | 150,424 | 155 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 318,535 | 3.185 | 20 | 24 | fits | 151,109 | 194 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 318,469 | 3.185 | 20 | 50 | fits | 151,109 | 194 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 488,233 | 4.882 | 20 | 50 | fits | 160,682 | 190 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 572,281 | 5.723 | 20 | 20 | fits | 84,114 | 35 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 960,640 | 9.606 | 20 | 20 | fits | 35,051 | 12 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 404,176 | 4.042 | 20 | 20 | fits | 156,857 | 183 | 0.385 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 310,165 | 3.102 | 20 | 200 | fits | 153,737 | 198 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 466,406 | 4.664 | 20 | 200 | fits | 156,857 | 183 | 0.385 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 311,089 | 3.111 | 20 | 20 | fits | 153,737 | 198 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 560,141 | 5.601 | 20 | 20 | fits | 93,031 | 39 | 0.740 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 152,484 | 1.525 | 20 | 24 | fits | 150,487 | 156 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 313,739 | 3.137 | 20 | 24 | fits | 153,737 | 198 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 313,673 | 3.137 | 20 | 50 | fits | 153,737 | 198 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 470,134 | 4.701 | 20 | 50 | fits | 156,857 | 183 | 0.385 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 563,099 | 5.631 | 20 | 20 | fits | 93,031 | 39 | 0.740 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 916,393 | 9.164 | 20 | 20 | fits | 88,524 | 36 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 406,804 | 4.068 | 20 | 20 | fits | 155,091 | 178 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 296,536 | 2.965 | 20 | 200 | fits | 151,670 | 198 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 451,011 | 4.510 | 20 | 200 | fits | 155,091 | 178 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 297,460 | 2.975 | 20 | 20 | fits | 151,670 | 198 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 537,563 | 5.376 | 20 | 20 | fits | 85,848 | 37 | 0.709 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 149,430 | 1.494 | 20 | 24 | fits | 151,337 | 155 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 300,110 | 3.001 | 20 | 24 | fits | 151,670 | 198 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 300,044 | 3.000 | 20 | 50 | fits | 151,670 | 198 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 454,739 | 4.547 | 20 | 50 | fits | 155,091 | 178 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 540,521 | 5.405 | 20 | 20 | fits | 85,848 | 37 | 0.709 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 945,093 | 9.451 | 20 | 20 | fits | 44,179 | 16 | 0.743 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 406,694 | 4.067 | 20 | 20 | fits | 156,392 | 182 | 0.380 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 304,337 | 3.043 | 20 | 200 | fits | 158,408 | 198 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 460,113 | 4.601 | 20 | 200 | fits | 156,392 | 182 | 0.380 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 305,261 | 3.053 | 20 | 20 | fits | 158,408 | 198 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 546,913 | 5.469 | 20 | 20 | fits | 86,096 | 31 | 0.742 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 150,493 | 1.505 | 20 | 24 | fits | 150,380 | 155 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 307,911 | 3.079 | 20 | 24 | fits | 158,408 | 198 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 307,845 | 3.078 | 20 | 50 | fits | 158,408 | 198 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 463,841 | 4.638 | 20 | 50 | fits | 156,392 | 182 | 0.380 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 549,871 | 5.499 | 20 | 20 | fits | 86,096 | 31 | 0.742 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 945,383 | 9.454 | 20 | 20 | fits | 35,051 | 12 | 0.812 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 411,347 | 4.113 | 20 | 20 | fits | 156,602 | 183 | 0.382 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 309,003 | 3.090 | 20 | 200 | fits | 150,820 | 193 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 464,989 | 4.650 | 20 | 200 | fits | 156,602 | 183 | 0.382 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 309,927 | 3.099 | 20 | 20 | fits | 150,820 | 193 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 565,321 | 5.653 | 20 | 20 | fits | 89,864 | 38 | 0.754 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 162,747 | 1.627 | 20 | 24 | fits | 150,366 | 155 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 312,577 | 3.126 | 20 | 24 | fits | 150,820 | 193 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 312,511 | 3.125 | 20 | 50 | fits | 150,820 | 193 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 468,717 | 4.687 | 20 | 50 | fits | 156,602 | 183 | 0.382 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 568,279 | 5.683 | 20 | 20 | fits | 89,864 | 38 | 0.754 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 921,168 | 9.212 | 20 | 20 | fits | 88,547 | 36 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 406,049 | 4.060 | 20 | 20 | fits | 159,886 | 191 | 0.398 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 299,044 | 2.990 | 20 | 200 | fits | 151,142 | 194 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 467,690 | 4.677 | 20 | 200 | fits | 159,886 | 191 | 0.398 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 299,968 | 3.000 | 20 | 20 | fits | 151,142 | 194 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 554,369 | 5.544 | 20 | 20 | fits | 85,975 | 31 | 0.742 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 152,466 | 1.525 | 20 | 24 | fits | 150,274 | 155 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 302,618 | 3.026 | 20 | 24 | fits | 151,142 | 194 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 302,552 | 3.026 | 20 | 50 | fits | 151,142 | 194 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 471,418 | 4.714 | 20 | 50 | fits | 159,886 | 191 | 0.398 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 557,327 | 5.573 | 20 | 20 | fits | 85,975 | 31 | 0.742 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 942,820 | 9.428 | 20 | 20 | fits | 35,051 | 12 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 390,980 | 3.910 | 20 | 20 | fits | 154,223 | 172 | 0.367 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 307,940 | 3.079 | 20 | 200 | fits | 161,662 | 215 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 461,547 | 4.615 | 20 | 200 | fits | 154,223 | 172 | 0.367 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 308,864 | 3.089 | 20 | 20 | fits | 161,662 | 215 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 462,251 | 4.623 | 20 | 20 | fits | 154,223 | 172 | 0.367 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 150,842 | 1.508 | 20 | 24 | fits | 150,767 | 155 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 311,514 | 3.115 | 20 | 24 | fits | 161,662 | 215 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 311,448 | 3.114 | 20 | 50 | fits | 161,662 | 215 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 465,275 | 4.653 | 20 | 50 | fits | 154,223 | 172 | 0.367 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 556,365 | 5.564 | 20 | 20 | fits | 91,156 | 34 | 0.753 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 916,267 | 9.163 | 20 | 20 | fits | 85,341 | 39 | 0.640 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 410,022 | 4.100 | 20 | 20 | fits | 156,515 | 183 | 0.380 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 316,310 | 3.163 | 20 | 200 | fits | 158,300 | 198 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 472,209 | 4.722 | 20 | 200 | fits | 156,515 | 183 | 0.380 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 317,234 | 3.172 | 20 | 20 | fits | 158,300 | 198 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 558,812 | 5.588 | 20 | 20 | fits | 85,899 | 32 | 0.739 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 162,574 | 1.626 | 20 | 24 | fits | 150,455 | 155 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 319,884 | 3.199 | 20 | 24 | fits | 158,300 | 198 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 319,818 | 3.198 | 20 | 50 | fits | 158,300 | 198 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 475,937 | 4.759 | 20 | 50 | fits | 156,515 | 183 | 0.380 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 561,770 | 5.618 | 20 | 20 | fits | 85,899 | 32 | 0.739 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 956,837 | 9.568 | 20 | 20 | fits | 35,051 | 12 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 422,822 | 4.228 | 20 | 20 | fits | 159,891 | 191 | 0.398 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 315,763 | 3.158 | 20 | 200 | fits | 150,660 | 194 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 484,594 | 4.846 | 20 | 200 | fits | 159,891 | 191 | 0.398 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 316,687 | 3.167 | 20 | 20 | fits | 150,660 | 194 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 571,350 | 5.713 | 20 | 20 | fits | 86,052 | 31 | 0.742 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 169,667 | 1.697 | 20 | 24 | fits | 150,413 | 155 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 319,337 | 3.193 | 20 | 24 | fits | 150,660 | 194 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 319,271 | 3.193 | 20 | 50 | fits | 150,660 | 194 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 488,322 | 4.883 | 20 | 50 | fits | 159,891 | 191 | 0.398 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 574,308 | 5.743 | 20 | 20 | fits | 86,052 | 31 | 0.742 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 926,948 | 9.269 | 20 | 20 | fits | 88,374 | 36 | 0.520 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 405,761 | 4.058 | 20 | 20 | fits | 156,112 | 183 | 0.376 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 312,344 | 3.123 | 20 | 200 | fits | 151,262 | 198 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 467,840 | 4.678 | 20 | 200 | fits | 156,112 | 183 | 0.376 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 313,268 | 3.133 | 20 | 20 | fits | 151,262 | 198 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 554,384 | 5.544 | 20 | 20 | fits | 85,840 | 31 | 0.740 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 165,646 | 1.656 | 20 | 24 | fits | 150,989 | 155 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 315,918 | 3.159 | 20 | 24 | fits | 151,262 | 198 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 315,852 | 3.159 | 20 | 50 | fits | 151,262 | 198 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 471,568 | 4.716 | 20 | 50 | fits | 156,112 | 183 | 0.376 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 557,342 | 5.573 | 20 | 20 | fits | 85,840 | 31 | 0.740 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 958,648 | 9.586 | 20 | 20 | fits | 44,205 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 397,704 | 3.977 | 20 | 20 | fits | 156,437 | 183 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 304,005 | 3.040 | 20 | 200 | fits | 150,904 | 193 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 459,826 | 4.598 | 20 | 200 | fits | 156,437 | 183 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 304,929 | 3.049 | 20 | 20 | fits | 150,904 | 193 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 553,049 | 5.530 | 20 | 20 | fits | 92,519 | 39 | 0.737 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 157,665 | 1.577 | 20 | 24 | fits | 150,395 | 155 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 307,579 | 3.076 | 20 | 24 | fits | 150,904 | 193 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 307,513 | 3.075 | 20 | 50 | fits | 150,904 | 193 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 463,554 | 4.636 | 20 | 50 | fits | 156,437 | 183 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 556,007 | 5.560 | 20 | 20 | fits | 92,519 | 39 | 0.737 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 952,275 | 9.523 | 20 | 20 | fits | 43,931 | 16 | 0.734 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 439,158 | 4.392 | 20 | 20 | fits | 152,472 | 184 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 321,485 | 3.215 | 20 | 200 | fits | 156,772 | 195 | 0.438 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 482,979 | 4.830 | 20 | 200 | fits | 152,472 | 184 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 322,409 | 3.224 | 20 | 20 | fits | 156,772 | 195 | 0.438 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 569,640 | 5.696 | 20 | 20 | fits | 85,957 | 37 | 0.711 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 169,277 | 1.693 | 20 | 24 | fits | 150,395 | 155 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 325,059 | 3.251 | 20 | 24 | fits | 156,772 | 195 | 0.438 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 324,993 | 3.250 | 20 | 50 | fits | 156,772 | 195 | 0.438 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 486,707 | 4.867 | 20 | 50 | fits | 152,472 | 184 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 572,598 | 5.726 | 20 | 20 | fits | 85,957 | 37 | 0.711 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 960,274 | 9.603 | 20 | 20 | fits | 34,901 | 12 | 0.808 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 481,541 | 4.815 | 20 | 20 | fits | 156,268 | 182 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 379,243 | 3.792 | 20 | 200 | fits | 150,860 | 193 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 534,895 | 5.349 | 20 | 200 | fits | 156,268 | 182 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 380,167 | 3.802 | 20 | 20 | fits | 150,860 | 193 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 621,439 | 6.214 | 20 | 20 | fits | 85,840 | 31 | 0.739 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 232,947 | 2.329 | 20 | 24 | fits | 150,944 | 155 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 382,817 | 3.828 | 20 | 24 | fits | 150,860 | 193 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 382,751 | 3.828 | 20 | 50 | fits | 150,860 | 193 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 538,623 | 5.386 | 20 | 50 | fits | 156,268 | 182 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 624,397 | 6.244 | 20 | 20 | fits | 85,840 | 31 | 0.739 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,026,224 | 10.262 | 20 | 20 | fits | 41,232 | 18 | 0.837 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 390,998 | 3.910 | 20 | 20 | fits | 155,719 | 184 | 0.370 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 297,484 | 2.975 | 20 | 200 | fits | 150,339 | 193 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 452,587 | 4.526 | 20 | 200 | fits | 155,719 | 184 | 0.370 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 298,408 | 2.984 | 20 | 20 | fits | 150,339 | 193 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 539,047 | 5.390 | 20 | 20 | fits | 85,756 | 31 | 0.738 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 151,709 | 1.517 | 20 | 24 | fits | 150,521 | 155 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 301,058 | 3.011 | 20 | 24 | fits | 150,339 | 193 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 300,992 | 3.010 | 20 | 50 | fits | 150,339 | 193 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 456,315 | 4.563 | 20 | 50 | fits | 155,719 | 184 | 0.370 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 542,005 | 5.420 | 20 | 20 | fits | 85,756 | 31 | 0.738 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 943,930 | 9.439 | 20 | 20 | fits | 44,099 | 16 | 0.738 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 396,647 | 3.966 | 20 | 20 | fits | 156,066 | 183 | 0.375 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 303,276 | 3.033 | 20 | 200 | fits | 150,325 | 193 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 458,726 | 4.587 | 20 | 200 | fits | 156,066 | 183 | 0.375 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 304,200 | 3.042 | 20 | 20 | fits | 150,325 | 193 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 545,445 | 5.454 | 20 | 20 | fits | 86,015 | 32 | 0.738 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 157,515 | 1.575 | 20 | 24 | fits | 150,521 | 155 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 306,850 | 3.068 | 20 | 24 | fits | 150,325 | 193 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 306,784 | 3.068 | 20 | 50 | fits | 150,325 | 193 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 462,454 | 4.625 | 20 | 50 | fits | 156,066 | 183 | 0.375 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 548,403 | 5.484 | 20 | 20 | fits | 86,015 | 32 | 0.738 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 950,127 | 9.501 | 20 | 20 | fits | 44,139 | 16 | 0.738 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 403,175 | 4.032 | 20 | 20 | fits | 156,679 | 184 | 0.381 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 309,522 | 3.095 | 20 | 200 | fits | 150,765 | 193 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 465,585 | 4.656 | 20 | 200 | fits | 156,679 | 184 | 0.381 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 310,446 | 3.104 | 20 | 20 | fits | 150,765 | 193 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 566,144 | 5.661 | 20 | 20 | fits | 90,145 | 38 | 0.754 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 163,321 | 1.633 | 20 | 24 | fits | 150,521 | 155 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 313,096 | 3.131 | 20 | 24 | fits | 150,765 | 193 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 313,030 | 3.130 | 20 | 50 | fits | 150,765 | 193 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 469,313 | 4.693 | 20 | 50 | fits | 156,679 | 184 | 0.381 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 569,102 | 5.691 | 20 | 20 | fits | 90,145 | 38 | 0.754 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 954,843 | 9.548 | 20 | 20 | fits | 34,985 | 12 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 431,186 | 4.312 | 20 | 20 | fits | 160,455 | 189 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 315,558 | 3.156 | 20 | 200 | fits | 150,995 | 194 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 484,774 | 4.848 | 20 | 200 | fits | 160,455 | 189 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 316,482 | 3.165 | 20 | 20 | fits | 150,995 | 194 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 578,411 | 5.784 | 20 | 20 | fits | 92,933 | 39 | 0.739 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 169,127 | 1.691 | 20 | 24 | fits | 150,521 | 155 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 319,132 | 3.191 | 20 | 24 | fits | 150,995 | 194 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 319,066 | 3.191 | 20 | 50 | fits | 150,995 | 194 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 488,502 | 4.885 | 20 | 50 | fits | 160,455 | 189 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 581,369 | 5.814 | 20 | 20 | fits | 92,933 | 39 | 0.739 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 934,677 | 9.347 | 20 | 20 | fits | 88,524 | 36 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 421,380 | 4.214 | 20 | 20 | fits | 155,530 | 178 | 0.428 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 310,781 | 3.108 | 20 | 200 | fits | 153,670 | 198 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 465,695 | 4.657 | 20 | 200 | fits | 155,530 | 178 | 0.428 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 311,705 | 3.117 | 20 | 20 | fits | 153,670 | 198 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 552,405 | 5.524 | 20 | 20 | fits | 86,006 | 37 | 0.709 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 153,251 | 1.533 | 20 | 24 | fits | 150,640 | 156 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 314,355 | 3.144 | 20 | 24 | fits | 153,670 | 198 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 314,289 | 3.143 | 20 | 50 | fits | 153,670 | 198 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 469,423 | 4.694 | 20 | 50 | fits | 155,530 | 178 | 0.428 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 555,363 | 5.554 | 20 | 20 | fits | 86,006 | 37 | 0.709 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 947,426 | 9.474 | 20 | 20 | fits | 38,747 | 19 | 0.814 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 414,803 | 4.148 | 20 | 20 | fits | 154,437 | 180 | 0.413 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 313,325 | 3.133 | 20 | 200 | fits | 150,909 | 193 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 467,146 | 4.671 | 20 | 200 | fits | 154,437 | 180 | 0.413 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 314,249 | 3.142 | 20 | 20 | fits | 150,909 | 193 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 553,566 | 5.536 | 20 | 20 | fits | 85,716 | 37 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 166,980 | 1.670 | 20 | 24 | fits | 150,624 | 155 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 316,899 | 3.169 | 20 | 24 | fits | 150,909 | 193 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 316,833 | 3.168 | 20 | 50 | fits | 150,909 | 193 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 470,874 | 4.709 | 20 | 50 | fits | 154,437 | 180 | 0.413 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 556,524 | 5.565 | 20 | 20 | fits | 85,716 | 37 | 0.707 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 961,096 | 9.611 | 20 | 20 | fits | 44,179 | 16 | 0.743 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 407,436 | 4.074 | 20 | 20 | fits | 157,288 | 187 | 0.365 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 303,392 | 3.034 | 20 | 200 | fits | 156,680 | 194 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 460,064 | 4.601 | 20 | 200 | fits | 157,288 | 187 | 0.365 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 304,316 | 3.043 | 20 | 20 | fits | 156,680 | 194 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 547,008 | 5.470 | 20 | 20 | fits | 86,240 | 31 | 0.743 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 151,276 | 1.513 | 20 | 24 | fits | 150,629 | 155 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 306,966 | 3.070 | 20 | 24 | fits | 156,680 | 194 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 306,900 | 3.069 | 20 | 50 | fits | 156,680 | 194 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 463,792 | 4.638 | 20 | 50 | fits | 157,288 | 187 | 0.365 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 549,966 | 5.500 | 20 | 20 | fits | 86,240 | 31 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 945,523 | 9.455 | 20 | 20 | fits | 35,051 | 12 | 0.812 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 397,971 | 3.980 | 20 | 20 | fits | 155,913 | 185 | 0.371 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 304,425 | 3.044 | 20 | 200 | fits | 150,465 | 193 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 459,722 | 4.597 | 20 | 200 | fits | 155,913 | 185 | 0.371 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 305,349 | 3.053 | 20 | 20 | fits | 150,465 | 193 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 560,866 | 5.609 | 20 | 20 | fits | 90,573 | 38 | 0.758 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 158,524 | 1.585 | 20 | 24 | fits | 149,177 | 152 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 307,999 | 3.080 | 20 | 24 | fits | 150,465 | 193 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 307,933 | 3.079 | 20 | 50 | fits | 150,465 | 193 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 463,450 | 4.635 | 20 | 50 | fits | 155,913 | 185 | 0.371 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 563,824 | 5.638 | 20 | 20 | fits | 90,573 | 38 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 917,313 | 9.173 | 20 | 20 | fits | 88,697 | 36 | 0.527 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 408,635 | 4.086 | 20 | 20 | fits | 156,027 | 210 | 0.395 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 305,245 | 3.052 | 20 | 200 | fits | 160,830 | 219 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 470,263 | 4.703 | 20 | 200 | fits | 156,027 | 210 | 0.395 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 306,169 | 3.062 | 20 | 20 | fits | 160,830 | 219 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 470,967 | 4.710 | 20 | 20 | fits | 156,027 | 210 | 0.395 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 148,979 | 1.490 | 20 | 24 | fits | 152,622 | 120 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 308,819 | 3.088 | 20 | 24 | fits | 160,830 | 219 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 308,753 | 3.088 | 20 | 50 | fits | 160,830 | 219 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 473,991 | 4.740 | 20 | 50 | fits | 156,027 | 210 | 0.395 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 560,376 | 5.604 | 20 | 20 | fits | 86,451 | 28 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 910,394 | 9.104 | 20 | 20 | fits | 85,881 | 38 | 0.621 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 405,974 | 4.060 | 20 | 20 | fits | 156,076 | 184 | 0.375 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 312,133 | 3.121 | 20 | 200 | fits | 153,178 | 198 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 467,593 | 4.676 | 20 | 200 | fits | 156,076 | 184 | 0.375 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 313,057 | 3.131 | 20 | 20 | fits | 153,178 | 198 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 554,786 | 5.548 | 20 | 20 | fits | 86,489 | 31 | 0.744 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 155,049 | 1.550 | 20 | 24 | fits | 149,280 | 153 | 0.381 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 315,707 | 3.157 | 20 | 24 | fits | 153,178 | 198 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 315,641 | 3.156 | 20 | 50 | fits | 153,178 | 198 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 471,321 | 4.713 | 20 | 50 | fits | 156,076 | 184 | 0.375 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 557,744 | 5.577 | 20 | 20 | fits | 86,489 | 31 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,037,465 | 10.375 | 20 | 20 | fits | 47,146 | 17 | 0.794 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 393,897 | 3.939 | 20 | 20 | fits | 155,638 | 184 | 0.370 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 300,386 | 3.004 | 20 | 200 | fits | 150,382 | 193 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 455,408 | 4.554 | 20 | 200 | fits | 155,638 | 184 | 0.370 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 301,310 | 3.013 | 20 | 20 | fits | 150,382 | 193 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 542,389 | 5.424 | 20 | 20 | fits | 86,277 | 31 | 0.743 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 154,568 | 1.546 | 20 | 24 | fits | 149,136 | 152 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 303,960 | 3.040 | 20 | 24 | fits | 150,382 | 193 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 303,894 | 3.039 | 20 | 50 | fits | 150,382 | 193 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 459,136 | 4.591 | 20 | 50 | fits | 155,638 | 184 | 0.370 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 545,347 | 5.453 | 20 | 20 | fits | 86,277 | 31 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,024,959 | 10.250 | 20 | 20 | fits | 44,106 | 16 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 403,028 | 4.030 | 20 | 20 | fits | 156,041 | 183 | 0.376 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 309,604 | 3.096 | 20 | 200 | fits | 150,368 | 193 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 465,029 | 4.650 | 20 | 200 | fits | 156,041 | 183 | 0.376 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 310,528 | 3.105 | 20 | 20 | fits | 150,368 | 193 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 558,848 | 5.588 | 20 | 20 | fits | 93,115 | 39 | 0.740 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 163,800 | 1.638 | 20 | 24 | fits | 149,044 | 152 | 0.379 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 313,178 | 3.132 | 20 | 24 | fits | 150,368 | 193 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 313,112 | 3.131 | 20 | 50 | fits | 150,368 | 193 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 468,757 | 4.688 | 20 | 50 | fits | 156,041 | 183 | 0.376 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 561,806 | 5.618 | 20 | 20 | fits | 93,115 | 39 | 0.740 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,035,644 | 10.356 | 20 | 20 | fits | 43,931 | 16 | 0.734 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 399,594 | 3.996 | 20 | 20 | fits | 153,988 | 168 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 308,111 | 3.081 | 20 | 200 | fits | 161,702 | 215 | 0.393 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 461,483 | 4.615 | 20 | 200 | fits | 153,988 | 168 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 309,035 | 3.090 | 20 | 20 | fits | 161,702 | 215 | 0.393 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 628,411 | 6.284 | 20 | 20 | fits | 89,634 | 39 | 0.739 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 150,973 | 1.510 | 20 | 24 | fits | 149,207 | 152 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 311,685 | 3.117 | 20 | 24 | fits | 161,702 | 215 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 311,619 | 3.116 | 20 | 50 | fits | 161,702 | 215 | 0.393 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 465,211 | 4.652 | 20 | 50 | fits | 153,988 | 168 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 631,369 | 6.314 | 20 | 20 | fits | 89,634 | 39 | 0.739 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,023,620 | 10.236 | 20 | 20 | fits | 35,051 | 12 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 407,903 | 4.079 | 20 | 20 | fits | 155,360 | 180 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 306,346 | 3.063 | 20 | 200 | fits | 150,525 | 193 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 461,090 | 4.611 | 20 | 200 | fits | 155,360 | 180 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 307,270 | 3.073 | 20 | 20 | fits | 150,525 | 193 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 638,013 | 6.380 | 20 | 20 | fits | 90,504 | 44 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 160,385 | 1.604 | 20 | 24 | fits | 149,207 | 152 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 309,920 | 3.099 | 20 | 24 | fits | 150,525 | 193 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 309,854 | 3.099 | 20 | 50 | fits | 150,525 | 193 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 464,818 | 4.648 | 20 | 50 | fits | 155,360 | 180 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 640,971 | 6.410 | 20 | 20 | fits | 90,504 | 44 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,029,542 | 10.295 | 20 | 20 | fits | 34,985 | 12 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 408,598 | 4.086 | 20 | 20 | fits | 158,563 | 185 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 294,532 | 2.945 | 20 | 200 | fits | 151,864 | 199 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 461,675 | 4.617 | 20 | 200 | fits | 158,563 | 185 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 295,456 | 2.955 | 20 | 20 | fits | 151,864 | 199 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 625,306 | 6.253 | 20 | 20 | fits | 86,201 | 38 | 0.708 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 147,232 | 1.472 | 20 | 24 | fits | 149,044 | 152 | 0.379 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 298,106 | 2.981 | 20 | 24 | fits | 151,864 | 199 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 298,040 | 2.980 | 20 | 50 | fits | 151,864 | 199 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 465,403 | 4.654 | 20 | 50 | fits | 158,563 | 185 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 628,264 | 6.283 | 20 | 20 | fits | 86,201 | 38 | 0.708 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,016,751 | 10.168 | 20 | 20 | fits | 35,051 | 12 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 395,968 | 3.960 | 20 | 20 | fits | 155,638 | 184 | 0.370 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 302,457 | 3.025 | 20 | 200 | fits | 150,128 | 193 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 457,479 | 4.575 | 20 | 200 | fits | 155,638 | 184 | 0.370 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 303,381 | 3.034 | 20 | 20 | fits | 150,128 | 193 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 544,666 | 5.447 | 20 | 20 | fits | 86,483 | 32 | 0.743 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 156,893 | 1.569 | 20 | 24 | fits | 149,207 | 152 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 306,031 | 3.060 | 20 | 24 | fits | 150,128 | 193 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 305,965 | 3.060 | 20 | 50 | fits | 150,128 | 193 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 461,207 | 4.612 | 20 | 50 | fits | 155,638 | 184 | 0.370 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 547,624 | 5.476 | 20 | 20 | fits | 86,483 | 32 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 942,691 | 9.427 | 20 | 20 | fits | 35,051 | 12 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 407,095 | 4.071 | 20 | 20 | fits | 155,355 | 172 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 323,472 | 3.235 | 20 | 200 | fits | 161,731 | 215 | 0.393 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 478,211 | 4.782 | 20 | 200 | fits | 155,355 | 172 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 324,396 | 3.244 | 20 | 20 | fits | 161,731 | 215 | 0.393 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 478,915 | 4.789 | 20 | 20 | fits | 155,355 | 172 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 166,305 | 1.663 | 20 | 24 | fits | 149,207 | 152 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 327,046 | 3.270 | 20 | 24 | fits | 161,731 | 215 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 326,980 | 3.270 | 20 | 50 | fits | 161,731 | 215 | 0.393 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 481,939 | 4.819 | 20 | 50 | fits | 155,355 | 172 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 581,020 | 5.810 | 20 | 20 | fits | 89,253 | 35 | 0.748 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 931,122 | 9.311 | 20 | 20 | fits | 86,238 | 38 | 0.627 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 406,095 | 4.061 | 20 | 20 | fits | 160,129 | 190 | 0.404 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 299,088 | 2.991 | 20 | 200 | fits | 150,500 | 194 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 468,247 | 4.682 | 20 | 200 | fits | 160,129 | 190 | 0.404 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 300,012 | 3.000 | 20 | 20 | fits | 150,500 | 194 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 555,495 | 5.555 | 20 | 20 | fits | 86,544 | 31 | 0.745 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 153,152 | 1.532 | 20 | 24 | fits | 149,044 | 152 | 0.379 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 302,662 | 3.027 | 20 | 24 | fits | 150,500 | 194 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 302,596 | 3.026 | 20 | 50 | fits | 150,500 | 194 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 471,975 | 4.720 | 20 | 50 | fits | 160,129 | 190 | 0.404 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 558,453 | 5.585 | 20 | 20 | fits | 86,544 | 31 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 944,109 | 9.441 | 20 | 20 | fits | 35,086 | 12 | 0.812 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 415,411 | 4.154 | 20 | 20 | fits | 158,340 | 183 | 0.401 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 310,427 | 3.104 | 20 | 200 | fits | 152,427 | 199 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 477,672 | 4.777 | 20 | 200 | fits | 158,340 | 183 | 0.401 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 311,351 | 3.114 | 20 | 20 | fits | 152,427 | 199 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 564,968 | 5.650 | 20 | 20 | fits | 86,592 | 31 | 0.745 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 162,564 | 1.626 | 20 | 24 | fits | 149,044 | 152 | 0.379 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 314,001 | 3.140 | 20 | 24 | fits | 152,427 | 199 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 313,935 | 3.139 | 20 | 50 | fits | 152,427 | 199 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 481,400 | 4.814 | 20 | 50 | fits | 158,340 | 183 | 0.401 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 567,926 | 5.679 | 20 | 20 | fits | 86,592 | 31 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 953,457 | 9.535 | 20 | 20 | fits | 35,051 | 12 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 401,403 | 4.014 | 20 | 20 | fits | 156,786 | 183 | 0.385 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 307,385 | 3.074 | 20 | 200 | fits | 153,504 | 198 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 463,555 | 4.636 | 20 | 200 | fits | 156,786 | 183 | 0.385 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 308,309 | 3.083 | 20 | 20 | fits | 153,504 | 198 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 557,308 | 5.573 | 20 | 20 | fits | 93,049 | 39 | 0.740 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 149,958 | 1.500 | 20 | 24 | fits | 149,428 | 153 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 310,959 | 3.110 | 20 | 24 | fits | 153,504 | 198 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 310,893 | 3.109 | 20 | 50 | fits | 153,504 | 198 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 467,283 | 4.673 | 20 | 50 | fits | 156,786 | 183 | 0.385 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 560,266 | 5.603 | 20 | 20 | fits | 93,049 | 39 | 0.740 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 913,560 | 9.136 | 20 | 20 | fits | 88,524 | 36 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 388,941 | 3.889 | 20 | 20 | fits | 156,244 | 183 | 0.377 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 295,357 | 2.954 | 20 | 200 | fits | 150,808 | 193 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 450,985 | 4.510 | 20 | 200 | fits | 156,244 | 183 | 0.377 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 296,281 | 2.963 | 20 | 20 | fits | 150,808 | 193 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 544,732 | 5.447 | 20 | 20 | fits | 93,043 | 39 | 0.740 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 149,113 | 1.491 | 20 | 24 | fits | 149,014 | 152 | 0.379 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 298,931 | 2.989 | 20 | 24 | fits | 150,808 | 193 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 298,865 | 2.989 | 20 | 50 | fits | 150,808 | 193 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 454,713 | 4.547 | 20 | 50 | fits | 156,244 | 183 | 0.377 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 547,690 | 5.477 | 20 | 20 | fits | 93,043 | 39 | 0.740 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 943,315 | 9.433 | 20 | 20 | fits | 35,051 | 12 | 0.812 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 414,999 | 4.150 | 20 | 20 | fits | 154,989 | 178 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 304,755 | 3.048 | 20 | 200 | fits | 150,794 | 193 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 459,128 | 4.591 | 20 | 200 | fits | 154,989 | 178 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 305,679 | 3.057 | 20 | 20 | fits | 150,794 | 193 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 545,777 | 5.458 | 20 | 20 | fits | 85,945 | 37 | 0.710 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 158,525 | 1.585 | 20 | 24 | fits | 149,014 | 152 | 0.379 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 308,329 | 3.083 | 20 | 24 | fits | 150,794 | 193 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 308,263 | 3.083 | 20 | 50 | fits | 150,794 | 193 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 462,856 | 4.629 | 20 | 50 | fits | 154,989 | 178 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 548,735 | 5.487 | 20 | 20 | fits | 85,945 | 37 | 0.710 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 953,217 | 9.532 | 20 | 20 | fits | 43,931 | 16 | 0.734 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 402,544 | 4.025 | 20 | 20 | fits | 160,312 | 217 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 296,435 | 2.964 | 20 | 200 | fits | 151,693 | 200 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 456,131 | 4.561 | 20 | 200 | fits | 160,312 | 217 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 297,359 | 2.974 | 20 | 20 | fits | 151,693 | 200 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 546,315 | 5.463 | 20 | 20 | fits | 89,480 | 38 | 0.743 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 149,306 | 1.493 | 20 | 24 | fits | 152,785 | 120 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 300,009 | 3.000 | 20 | 24 | fits | 151,693 | 200 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 299,943 | 2.999 | 20 | 50 | fits | 151,693 | 200 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 459,859 | 4.599 | 20 | 50 | fits | 160,312 | 217 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 549,273 | 5.493 | 20 | 20 | fits | 89,480 | 38 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 941,280 | 9.413 | 20 | 20 | fits | 35,051 | 12 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 418,223 | 4.182 | 20 | 20 | fits | 156,776 | 183 | 0.385 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 324,215 | 3.242 | 20 | 200 | fits | 153,469 | 198 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 480,375 | 4.804 | 20 | 200 | fits | 156,776 | 183 | 0.385 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 325,139 | 3.251 | 20 | 20 | fits | 153,469 | 198 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 567,007 | 5.670 | 20 | 20 | fits | 85,928 | 31 | 0.740 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 166,881 | 1.669 | 20 | 24 | fits | 149,472 | 153 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 327,789 | 3.278 | 20 | 24 | fits | 153,469 | 198 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 327,723 | 3.277 | 20 | 50 | fits | 153,469 | 198 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 484,103 | 4.841 | 20 | 50 | fits | 156,776 | 183 | 0.385 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 569,965 | 5.700 | 20 | 20 | fits | 85,928 | 31 | 0.740 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 922,560 | 9.226 | 20 | 20 | fits | 88,374 | 36 | 0.520 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 405,113 | 4.051 | 20 | 20 | fits | 156,837 | 183 | 0.385 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 311,044 | 3.110 | 20 | 200 | fits | 153,448 | 198 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 467,265 | 4.673 | 20 | 200 | fits | 156,837 | 183 | 0.385 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 311,968 | 3.120 | 20 | 20 | fits | 153,448 | 198 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 553,897 | 5.539 | 20 | 20 | fits | 85,928 | 31 | 0.740 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 153,814 | 1.538 | 20 | 24 | fits | 149,610 | 153 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 314,618 | 3.146 | 20 | 24 | fits | 153,448 | 198 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 314,552 | 3.146 | 20 | 50 | fits | 153,448 | 198 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 470,993 | 4.710 | 20 | 50 | fits | 156,837 | 183 | 0.385 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 556,855 | 5.569 | 20 | 20 | fits | 85,928 | 31 | 0.740 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 1,027,878 | 10.279 | 20 | 20 | fits | 40,053 | 20 | 0.822 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 392,694 | 3.927 | 20 | 20 | fits | 156,295 | 183 | 0.378 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 299,059 | 2.991 | 20 | 200 | fits | 150,436 | 193 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 454,738 | 4.547 | 20 | 200 | fits | 156,295 | 183 | 0.378 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 299,983 | 3.000 | 20 | 20 | fits | 150,436 | 193 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 541,074 | 5.411 | 20 | 20 | fits | 85,632 | 31 | 0.738 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 153,187 | 1.532 | 20 | 24 | fits | 149,545 | 152 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 302,633 | 3.026 | 20 | 24 | fits | 150,436 | 193 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 302,567 | 3.026 | 20 | 50 | fits | 150,436 | 193 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 458,466 | 4.585 | 20 | 50 | fits | 156,295 | 183 | 0.378 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 544,032 | 5.440 | 20 | 20 | fits | 85,632 | 31 | 0.738 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,025,704 | 10.257 | 20 | 20 | fits | 35,328 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 410,570 | 4.106 | 20 | 20 | fits | 156,263 | 182 | 0.380 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 308,199 | 3.082 | 20 | 200 | fits | 150,422 | 193 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 463,846 | 4.638 | 20 | 200 | fits | 156,263 | 182 | 0.380 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 309,123 | 3.091 | 20 | 20 | fits | 150,422 | 193 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 550,120 | 5.501 | 20 | 20 | fits | 85,570 | 31 | 0.738 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 162,341 | 1.623 | 20 | 24 | fits | 149,545 | 152 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 311,773 | 3.118 | 20 | 24 | fits | 150,422 | 193 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 311,707 | 3.117 | 20 | 50 | fits | 150,422 | 193 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 467,574 | 4.676 | 20 | 50 | fits | 156,263 | 182 | 0.380 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 553,078 | 5.531 | 20 | 20 | fits | 85,570 | 31 | 0.738 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,034,916 | 10.349 | 20 | 20 | fits | 34,985 | 12 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 397,124 | 3.971 | 20 | 20 | fits | 156,551 | 183 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 294,753 | 2.948 | 20 | 200 | fits | 151,648 | 198 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 450,688 | 4.507 | 20 | 200 | fits | 156,551 | 183 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 295,677 | 2.957 | 20 | 20 | fits | 151,648 | 198 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 547,907 | 5.479 | 20 | 20 | fits | 87,033 | 42 | 0.770 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 147,669 | 1.477 | 20 | 24 | fits | 149,382 | 152 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 298,327 | 2.983 | 20 | 24 | fits | 151,648 | 198 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 298,261 | 2.983 | 20 | 50 | fits | 151,648 | 198 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 454,416 | 4.544 | 20 | 50 | fits | 156,551 | 183 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 550,865 | 5.509 | 20 | 20 | fits | 87,033 | 42 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,021,525 | 10.215 | 20 | 20 | fits | 34,985 | 12 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 397,831 | 3.978 | 20 | 20 | fits | 155,964 | 185 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 304,234 | 3.042 | 20 | 200 | fits | 150,671 | 193 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 459,582 | 4.596 | 20 | 200 | fits | 155,964 | 185 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 305,158 | 3.052 | 20 | 20 | fits | 150,671 | 193 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 556,782 | 5.568 | 20 | 20 | fits | 87,041 | 42 | 0.771 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 158,127 | 1.581 | 20 | 24 | fits | 149,382 | 152 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 307,808 | 3.078 | 20 | 24 | fits | 150,671 | 193 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 307,742 | 3.077 | 20 | 50 | fits | 150,671 | 193 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 463,310 | 4.633 | 20 | 50 | fits | 155,964 | 185 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 559,740 | 5.597 | 20 | 20 | fits | 87,041 | 42 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,030,355 | 10.304 | 20 | 20 | fits | 34,985 | 12 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 427,228 | 4.272 | 20 | 20 | fits | 157,804 | 187 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 313,259 | 3.133 | 20 | 200 | fits | 150,542 | 194 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 479,721 | 4.797 | 20 | 200 | fits | 157,804 | 187 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 314,183 | 3.142 | 20 | 20 | fits | 150,542 | 194 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 647,359 | 6.474 | 20 | 20 | fits | 86,222 | 38 | 0.708 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 167,281 | 1.673 | 20 | 24 | fits | 149,382 | 152 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 316,833 | 3.168 | 20 | 24 | fits | 150,542 | 194 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 316,767 | 3.168 | 20 | 50 | fits | 150,542 | 194 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 483,449 | 4.834 | 20 | 50 | fits | 157,804 | 187 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 650,317 | 6.503 | 20 | 20 | fits | 86,222 | 38 | 0.708 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,038,129 | 10.381 | 20 | 20 | fits | 34,901 | 12 | 0.808 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 487,083 | 4.871 | 20 | 20 | fits | 158,747 | 189 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 309,910 | 3.099 | 20 | 200 | fits | 151,682 | 191 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 548,784 | 5.488 | 20 | 200 | fits | 158,747 | 189 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 310,834 | 3.108 | 20 | 20 | fits | 151,682 | 191 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 635,683 | 6.357 | 20 | 20 | fits | 86,195 | 37 | 0.713 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 154,478 | 1.545 | 20 | 24 | fits | 149,784 | 153 | 0.385 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 313,484 | 3.135 | 20 | 24 | fits | 151,682 | 191 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 313,418 | 3.134 | 20 | 50 | fits | 151,682 | 191 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 552,512 | 5.525 | 20 | 50 | fits | 158,747 | 189 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 638,641 | 6.386 | 20 | 20 | fits | 86,195 | 37 | 0.713 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,042,776 | 10.428 | 20 | 20 | fits | 44,205 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 415,337 | 4.153 | 20 | 20 | fits | 156,551 | 183 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 312,966 | 3.130 | 20 | 200 | fits | 150,506 | 193 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 468,901 | 4.689 | 20 | 200 | fits | 156,551 | 183 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 313,890 | 3.139 | 20 | 20 | fits | 150,506 | 193 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 569,430 | 5.694 | 20 | 20 | fits | 89,978 | 38 | 0.754 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 167,024 | 1.670 | 20 | 24 | fits | 149,545 | 152 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 316,540 | 3.165 | 20 | 24 | fits | 150,506 | 193 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 316,474 | 3.165 | 20 | 50 | fits | 150,506 | 193 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 472,629 | 4.726 | 20 | 50 | fits | 156,551 | 183 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 572,388 | 5.724 | 20 | 20 | fits | 89,978 | 38 | 0.754 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 925,277 | 9.253 | 20 | 20 | fits | 88,547 | 36 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 415,872 | 4.159 | 20 | 20 | fits | 160,462 | 189 | 0.410 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 300,062 | 3.001 | 20 | 200 | fits | 150,970 | 194 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 469,382 | 4.694 | 20 | 200 | fits | 160,462 | 189 | 0.410 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 300,986 | 3.010 | 20 | 20 | fits | 150,970 | 194 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 556,037 | 5.560 | 20 | 20 | fits | 85,951 | 31 | 0.741 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 153,656 | 1.537 | 20 | 24 | fits | 149,382 | 152 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 303,636 | 3.036 | 20 | 24 | fits | 150,970 | 194 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 303,570 | 3.036 | 20 | 50 | fits | 150,970 | 194 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 473,110 | 4.731 | 20 | 50 | fits | 160,462 | 189 | 0.410 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 558,995 | 5.590 | 20 | 20 | fits | 85,951 | 31 | 0.741 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 944,250 | 9.443 | 20 | 20 | fits | 35,153 | 12 | 0.815 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 423,178 | 4.232 | 20 | 20 | fits | 157,498 | 187 | 0.369 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 318,889 | 3.189 | 20 | 200 | fits | 151,945 | 194 | 0.430 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 475,771 | 4.758 | 20 | 200 | fits | 157,498 | 187 | 0.369 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 319,813 | 3.198 | 20 | 20 | fits | 151,945 | 194 | 0.430 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 562,589 | 5.626 | 20 | 20 | fits | 86,114 | 31 | 0.742 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 163,067 | 1.631 | 20 | 24 | fits | 149,639 | 153 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 322,463 | 3.225 | 20 | 24 | fits | 151,945 | 194 | 0.430 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 322,397 | 3.224 | 20 | 50 | fits | 151,945 | 194 | 0.430 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 479,499 | 4.795 | 20 | 50 | fits | 157,498 | 187 | 0.369 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 565,547 | 5.655 | 20 | 20 | fits | 86,114 | 31 | 0.742 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 966,776 | 9.668 | 20 | 20 | fits | 40,668 | 19 | 0.848 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 401,882 | 4.019 | 20 | 20 | fits | 155,676 | 184 | 0.369 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 308,285 | 3.083 | 20 | 200 | fits | 150,637 | 193 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 463,345 | 4.633 | 20 | 200 | fits | 155,676 | 184 | 0.369 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 309,209 | 3.092 | 20 | 20 | fits | 150,637 | 193 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 549,951 | 5.500 | 20 | 20 | fits | 85,902 | 31 | 0.741 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 162,212 | 1.622 | 20 | 24 | fits | 149,336 | 152 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 311,859 | 3.119 | 20 | 24 | fits | 150,637 | 193 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 311,793 | 3.118 | 20 | 50 | fits | 150,637 | 193 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 467,073 | 4.671 | 20 | 50 | fits | 155,676 | 184 | 0.369 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 552,909 | 5.529 | 20 | 20 | fits | 85,902 | 31 | 0.741 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 954,304 | 9.543 | 20 | 20 | fits | 44,205 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 387,976 | 3.880 | 20 | 20 | fits | 155,676 | 184 | 0.369 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 294,379 | 2.944 | 20 | 200 | fits | 151,249 | 198 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 449,439 | 4.494 | 20 | 200 | fits | 155,676 | 184 | 0.369 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 295,303 | 2.953 | 20 | 20 | fits | 151,249 | 198 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 542,564 | 5.426 | 20 | 20 | fits | 92,421 | 39 | 0.736 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 147,694 | 1.477 | 20 | 24 | fits | 149,407 | 152 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 297,953 | 2.980 | 20 | 24 | fits | 151,249 | 198 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 297,887 | 2.979 | 20 | 50 | fits | 151,249 | 198 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 453,167 | 4.532 | 20 | 50 | fits | 155,676 | 184 | 0.369 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 545,522 | 5.455 | 20 | 20 | fits | 92,421 | 39 | 0.736 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 941,402 | 9.414 | 20 | 20 | fits | 44,021 | 16 | 0.738 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 397,277 | 3.973 | 20 | 20 | fits | 155,689 | 184 | 0.370 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 303,715 | 3.037 | 20 | 200 | fits | 150,081 | 193 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 458,788 | 4.588 | 20 | 200 | fits | 155,689 | 184 | 0.370 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 304,639 | 3.046 | 20 | 20 | fits | 150,081 | 193 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 552,020 | 5.520 | 20 | 20 | fits | 92,528 | 40 | 0.735 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 158,198 | 1.582 | 20 | 24 | fits | 149,407 | 152 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 307,289 | 3.073 | 20 | 24 | fits | 150,081 | 193 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 307,223 | 3.072 | 20 | 50 | fits | 150,081 | 193 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 462,516 | 4.625 | 20 | 50 | fits | 155,689 | 184 | 0.370 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 554,978 | 5.550 | 20 | 20 | fits | 92,528 | 40 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 950,067 | 9.501 | 20 | 20 | fits | 35,051 | 12 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 416,006 | 4.160 | 20 | 20 | fits | 154,327 | 169 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 324,472 | 3.245 | 20 | 200 | fits | 161,684 | 215 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 478,183 | 4.782 | 20 | 200 | fits | 154,327 | 169 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 325,396 | 3.254 | 20 | 20 | fits | 161,684 | 215 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 578,359 | 5.784 | 20 | 20 | fits | 89,625 | 38 | 0.753 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 167,352 | 1.674 | 20 | 24 | fits | 149,407 | 152 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 328,046 | 3.280 | 20 | 24 | fits | 161,684 | 215 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 327,980 | 3.280 | 20 | 50 | fits | 161,684 | 215 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 481,911 | 4.819 | 20 | 50 | fits | 154,327 | 169 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 581,317 | 5.813 | 20 | 20 | fits | 89,625 | 38 | 0.753 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 934,206 | 9.342 | 20 | 20 | fits | 88,547 | 36 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 414,456 | 4.145 | 20 | 20 | fits | 160,201 | 189 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 307,325 | 3.073 | 20 | 200 | fits | 157,905 | 199 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 476,673 | 4.767 | 20 | 200 | fits | 160,201 | 189 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 308,249 | 3.082 | 20 | 20 | fits | 157,905 | 199 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 563,481 | 5.635 | 20 | 20 | fits | 86,104 | 31 | 0.742 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 153,984 | 1.540 | 20 | 24 | fits | 149,244 | 152 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 310,899 | 3.109 | 20 | 24 | fits | 157,905 | 199 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 310,833 | 3.108 | 20 | 50 | fits | 157,905 | 199 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 480,401 | 4.804 | 20 | 50 | fits | 160,201 | 189 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 566,439 | 5.664 | 20 | 20 | fits | 86,104 | 31 | 0.742 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 919,034 | 9.190 | 20 | 20 | fits | 88,374 | 36 | 0.520 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 413,386 | 4.134 | 20 | 20 | fits | 156,263 | 182 | 0.380 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 311,015 | 3.110 | 20 | 200 | fits | 150,706 | 193 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 466,662 | 4.667 | 20 | 200 | fits | 156,263 | 182 | 0.380 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 311,939 | 3.119 | 20 | 20 | fits | 150,706 | 193 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 553,455 | 5.535 | 20 | 20 | fits | 86,089 | 31 | 0.741 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 164,873 | 1.649 | 20 | 24 | fits | 149,207 | 152 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 314,589 | 3.146 | 20 | 24 | fits | 150,706 | 193 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 314,523 | 3.145 | 20 | 50 | fits | 150,706 | 193 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 470,390 | 4.704 | 20 | 50 | fits | 156,263 | 182 | 0.380 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 556,413 | 5.564 | 20 | 20 | fits | 86,089 | 31 | 0.741 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 951,860 | 9.519 | 20 | 20 | fits | 35,233 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 400,761 | 4.008 | 20 | 20 | fits | 156,263 | 182 | 0.380 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 298,390 | 2.984 | 20 | 200 | fits | 151,234 | 193 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 454,037 | 4.540 | 20 | 200 | fits | 156,263 | 182 | 0.380 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 299,314 | 2.993 | 20 | 20 | fits | 151,234 | 193 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 540,914 | 5.409 | 20 | 20 | fits | 86,173 | 31 | 0.742 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 151,720 | 1.517 | 20 | 24 | fits | 149,044 | 152 | 0.379 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 301,964 | 3.020 | 20 | 24 | fits | 151,234 | 193 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 301,898 | 3.019 | 20 | 50 | fits | 151,234 | 193 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 457,765 | 4.578 | 20 | 50 | fits | 156,263 | 182 | 0.380 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 543,872 | 5.439 | 20 | 20 | fits | 86,173 | 31 | 0.742 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 1,023,388 | 10.234 | 20 | 20 | fits | 44,627 | 17 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 401,260 | 4.013 | 20 | 20 | fits | 155,676 | 184 | 0.369 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 307,663 | 3.077 | 20 | 200 | fits | 151,095 | 193 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 462,723 | 4.627 | 20 | 200 | fits | 155,676 | 184 | 0.369 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 308,587 | 3.086 | 20 | 20 | fits | 151,095 | 193 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 549,976 | 5.500 | 20 | 20 | fits | 86,549 | 32 | 0.743 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 161,132 | 1.611 | 20 | 24 | fits | 149,044 | 152 | 0.379 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 311,237 | 3.112 | 20 | 24 | fits | 151,095 | 193 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 311,171 | 3.112 | 20 | 50 | fits | 151,095 | 193 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 466,451 | 4.665 | 20 | 50 | fits | 155,676 | 184 | 0.369 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 552,934 | 5.529 | 20 | 20 | fits | 86,549 | 32 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,032,488 | 10.325 | 20 | 20 | fits | 44,245 | 16 | 0.741 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 387,932 | 3.879 | 20 | 20 | fits | 155,964 | 185 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 294,335 | 2.943 | 20 | 200 | fits | 151,405 | 198 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 449,683 | 4.497 | 20 | 200 | fits | 155,964 | 185 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 295,259 | 2.953 | 20 | 20 | fits | 151,405 | 198 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 550,392 | 5.504 | 20 | 20 | fits | 90,239 | 38 | 0.755 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 147,494 | 1.475 | 20 | 24 | fits | 149,207 | 152 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 297,909 | 2.979 | 20 | 24 | fits | 151,405 | 198 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 297,843 | 2.978 | 20 | 50 | fits | 151,405 | 198 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 453,411 | 4.534 | 20 | 50 | fits | 155,964 | 185 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 553,350 | 5.534 | 20 | 20 | fits | 90,239 | 38 | 0.755 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,017,328 | 10.173 | 20 | 20 | fits | 34,985 | 12 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 410,507 | 4.105 | 20 | 20 | fits | 159,581 | 191 | 0.397 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 303,608 | 3.036 | 20 | 200 | fits | 150,455 | 194 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 472,118 | 4.721 | 20 | 200 | fits | 159,581 | 191 | 0.397 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 304,532 | 3.045 | 20 | 20 | fits | 150,455 | 194 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 565,730 | 5.657 | 20 | 20 | fits | 92,908 | 39 | 0.738 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 157,717 | 1.577 | 20 | 24 | fits | 149,207 | 152 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 307,182 | 3.072 | 20 | 24 | fits | 150,455 | 194 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 307,116 | 3.071 | 20 | 50 | fits | 150,455 | 194 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 475,846 | 4.758 | 20 | 50 | fits | 159,581 | 191 | 0.397 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 568,688 | 5.687 | 20 | 20 | fits | 92,908 | 39 | 0.738 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 999,750 | 9.998 | 20 | 20 | fits | 88,524 | 36 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 426,184 | 4.262 | 20 | 20 | fits | 155,275 | 179 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 324,487 | 3.245 | 20 | 200 | fits | 153,206 | 198 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 479,146 | 4.791 | 20 | 200 | fits | 155,275 | 179 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 325,411 | 3.254 | 20 | 20 | fits | 153,206 | 198 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 643,461 | 6.435 | 20 | 20 | fits | 86,186 | 38 | 0.706 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 167,404 | 1.674 | 20 | 24 | fits | 149,482 | 153 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 328,061 | 3.281 | 20 | 24 | fits | 153,206 | 198 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 327,995 | 3.280 | 20 | 50 | fits | 153,206 | 198 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 482,874 | 4.829 | 20 | 50 | fits | 155,275 | 179 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 646,419 | 6.464 | 20 | 20 | fits | 86,186 | 38 | 0.706 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,051,546 | 10.515 | 20 | 20 | fits | 46,887 | 17 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 396,002 | 3.960 | 20 | 20 | fits | 154,822 | 179 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 294,650 | 2.946 | 20 | 200 | fits | 151,324 | 198 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 448,856 | 4.489 | 20 | 200 | fits | 154,822 | 179 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 295,574 | 2.956 | 20 | 20 | fits | 151,324 | 198 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 612,874 | 6.129 | 20 | 20 | fits | 85,915 | 38 | 0.704 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 147,890 | 1.479 | 20 | 24 | fits | 151,381 | 157 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 298,224 | 2.982 | 20 | 24 | fits | 151,324 | 198 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 298,158 | 2.982 | 20 | 50 | fits | 151,324 | 198 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 452,584 | 4.526 | 20 | 50 | fits | 154,822 | 179 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 615,832 | 6.158 | 20 | 20 | fits | 85,915 | 38 | 0.704 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,020,660 | 10.207 | 20 | 20 | fits | 44,104 | 16 | 0.738 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 477,739 | 4.777 | 20 | 20 | fits | 156,247 | 183 | 0.375 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 306,777 | 3.068 | 20 | 200 | fits | 157,850 | 198 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 539,805 | 5.398 | 20 | 200 | fits | 156,247 | 183 | 0.375 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 307,701 | 3.077 | 20 | 20 | fits | 157,850 | 198 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 626,814 | 6.268 | 20 | 20 | fits | 86,305 | 31 | 0.743 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 153,491 | 1.535 | 20 | 24 | fits | 148,906 | 152 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 310,351 | 3.104 | 20 | 24 | fits | 157,850 | 198 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 310,285 | 3.103 | 20 | 50 | fits | 157,850 | 198 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 543,533 | 5.435 | 20 | 50 | fits | 156,247 | 183 | 0.375 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 629,772 | 6.298 | 20 | 20 | fits | 86,305 | 31 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,025,351 | 10.254 | 20 | 20 | fits | 34,985 | 12 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 409,526 | 4.095 | 20 | 20 | fits | 157,498 | 187 | 0.369 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 305,237 | 3.052 | 20 | 200 | fits | 151,902 | 194 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 462,119 | 4.621 | 20 | 200 | fits | 157,498 | 187 | 0.369 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 306,161 | 3.062 | 20 | 20 | fits | 151,902 | 194 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 549,299 | 5.493 | 20 | 20 | fits | 86,476 | 31 | 0.743 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 149,400 | 1.494 | 20 | 24 | fits | 149,463 | 153 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 308,811 | 3.088 | 20 | 24 | fits | 151,902 | 194 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 308,745 | 3.087 | 20 | 50 | fits | 151,902 | 194 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 465,847 | 4.658 | 20 | 50 | fits | 157,498 | 187 | 0.369 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 552,257 | 5.523 | 20 | 20 | fits | 86,476 | 31 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 905,483 | 9.055 | 20 | 20 | fits | 88,524 | 36 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 409,869 | 4.099 | 20 | 20 | fits | 156,127 | 184 | 0.376 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 315,977 | 3.160 | 20 | 200 | fits | 153,191 | 198 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 471,488 | 4.715 | 20 | 200 | fits | 156,127 | 184 | 0.376 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 316,901 | 3.169 | 20 | 20 | fits | 153,191 | 198 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 558,548 | 5.585 | 20 | 20 | fits | 86,356 | 31 | 0.742 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 158,851 | 1.589 | 20 | 24 | fits | 149,502 | 153 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 319,551 | 3.196 | 20 | 24 | fits | 153,191 | 198 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 319,485 | 3.195 | 20 | 50 | fits | 153,191 | 198 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 475,216 | 4.752 | 20 | 50 | fits | 156,127 | 184 | 0.376 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 561,506 | 5.615 | 20 | 20 | fits | 86,356 | 31 | 0.742 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 950,693 | 9.507 | 20 | 20 | fits | 38,649 | 19 | 0.813 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 399,505 | 3.995 | 20 | 20 | fits | 154,231 | 172 | 0.367 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 316,379 | 3.164 | 20 | 200 | fits | 161,500 | 215 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 469,994 | 4.700 | 20 | 200 | fits | 154,231 | 172 | 0.367 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 317,303 | 3.173 | 20 | 20 | fits | 161,500 | 215 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 470,698 | 4.707 | 20 | 20 | fits | 154,231 | 172 | 0.367 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 159,443 | 1.594 | 20 | 24 | fits | 149,161 | 152 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 319,953 | 3.200 | 20 | 24 | fits | 161,500 | 215 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 319,887 | 3.199 | 20 | 50 | fits | 161,500 | 215 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 473,722 | 4.737 | 20 | 50 | fits | 154,231 | 172 | 0.367 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 559,625 | 5.596 | 20 | 20 | fits | 85,969 | 28 | 0.740 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 923,785 | 9.238 | 20 | 20 | fits | 88,905 | 36 | 0.536 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 386,558 | 3.866 | 20 | 20 | fits | 155,689 | 184 | 0.370 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 292,996 | 2.930 | 20 | 200 | fits | 151,270 | 198 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 448,069 | 4.481 | 20 | 200 | fits | 155,689 | 184 | 0.370 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 293,920 | 2.939 | 20 | 20 | fits | 151,270 | 198 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 534,838 | 5.348 | 20 | 20 | fits | 86,065 | 31 | 0.740 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 146,290 | 1.463 | 20 | 24 | fits | 148,998 | 152 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 296,570 | 2.966 | 20 | 24 | fits | 151,270 | 198 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 296,504 | 2.965 | 20 | 50 | fits | 151,270 | 198 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 451,797 | 4.518 | 20 | 50 | fits | 155,689 | 184 | 0.370 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 537,796 | 5.378 | 20 | 20 | fits | 86,065 | 31 | 0.740 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 937,365 | 9.374 | 20 | 20 | fits | 34,985 | 12 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 395,031 | 3.950 | 20 | 20 | fits | 156,380 | 184 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 301,556 | 3.016 | 20 | 200 | fits | 150,418 | 193 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 457,320 | 4.573 | 20 | 200 | fits | 156,380 | 184 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 302,480 | 3.025 | 20 | 20 | fits | 150,418 | 193 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 554,712 | 5.547 | 20 | 20 | fits | 87,287 | 42 | 0.771 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 155,702 | 1.557 | 20 | 24 | fits | 148,998 | 152 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 305,130 | 3.051 | 20 | 24 | fits | 150,418 | 193 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 305,064 | 3.051 | 20 | 50 | fits | 150,418 | 193 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 461,048 | 4.610 | 20 | 50 | fits | 156,380 | 184 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 557,670 | 5.577 | 20 | 20 | fits | 87,287 | 42 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 946,167 | 9.462 | 20 | 20 | fits | 34,985 | 12 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 415,433 | 4.154 | 20 | 20 | fits | 157,085 | 186 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 311,408 | 3.114 | 20 | 200 | fits | 150,858 | 193 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 467,877 | 4.679 | 20 | 200 | fits | 157,085 | 186 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 312,332 | 3.123 | 20 | 20 | fits | 150,858 | 193 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 565,791 | 5.658 | 20 | 20 | fits | 87,417 | 38 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 165,114 | 1.651 | 20 | 24 | fits | 148,998 | 152 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 314,982 | 3.150 | 20 | 24 | fits | 150,858 | 193 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 314,916 | 3.149 | 20 | 50 | fits | 150,858 | 193 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 471,605 | 4.716 | 20 | 50 | fits | 157,085 | 186 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 568,749 | 5.687 | 20 | 20 | fits | 87,417 | 38 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 957,316 | 9.573 | 20 | 20 | fits | 34,985 | 12 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 412,323 | 4.123 | 20 | 20 | fits | 158,613 | 186 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 298,308 | 2.983 | 20 | 200 | fits | 150,585 | 194 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 465,400 | 4.654 | 20 | 200 | fits | 158,613 | 186 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 299,232 | 2.992 | 20 | 20 | fits | 150,585 | 194 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 552,310 | 5.523 | 20 | 20 | fits | 86,206 | 37 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 152,287 | 1.523 | 20 | 24 | fits | 149,161 | 152 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 301,882 | 3.019 | 20 | 24 | fits | 150,585 | 194 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 301,816 | 3.018 | 20 | 50 | fits | 150,585 | 194 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 469,128 | 4.691 | 20 | 50 | fits | 158,613 | 186 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 555,268 | 5.553 | 20 | 20 | fits | 86,206 | 37 | 0.712 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 943,649 | 9.436 | 20 | 20 | fits | 35,051 | 12 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 430,641 | 4.306 | 20 | 20 | fits | 159,112 | 188 | 0.396 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 325,633 | 3.256 | 20 | 200 | fits | 159,982 | 198 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 484,129 | 4.841 | 20 | 200 | fits | 159,112 | 188 | 0.396 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 326,557 | 3.266 | 20 | 20 | fits | 159,982 | 198 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 571,128 | 5.711 | 20 | 20 | fits | 86,295 | 31 | 0.742 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 161,938 | 1.619 | 20 | 24 | fits | 149,400 | 153 | 0.381 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 329,207 | 3.292 | 20 | 24 | fits | 159,982 | 198 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 329,141 | 3.291 | 20 | 50 | fits | 159,982 | 198 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 487,857 | 4.879 | 20 | 50 | fits | 159,112 | 188 | 0.396 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 574,086 | 5.741 | 20 | 20 | fits | 86,295 | 31 | 0.742 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 927,267 | 9.273 | 20 | 20 | fits | 88,524 | 36 | 0.524 |
| LINK_UP | `adp.link_up.if0` | 2,776 | 0.028 | 20 | 200 | fits | 37,741 | 43 (11) | 0.733 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 19,134 | 0.191 | 20 | 200 | fits | 28,557 | 23 (39) | 0.765 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 7,836 | 0.078 | 20 | 200 | fits | 2,546 | 10 (11) | 0.538 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 16,998 | 0.170 | 20 | 20 | fits | 37,143 | 21 (35) | 0.836 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 11,135 | 0.111 | 20 | 20 | fits | 33,620 | 17 (14) | 0.865 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 18,553 | 0.186 | 20 | 20 | fits | 33,669 | 18 (14) | 0.855 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 36,471 | 0.365 | 20 | 20 | fits | 41,436 | 27 (35) | 0.815 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 84,179 | 0.842 | 20 | 20 | fits | 26,416 | 8 | 0.776 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 46,937 | 0.469 | 20 | 20 | fits | 47,003 | 12 | 0.892 |
| malformed MRPDU discard | `srp.malformed.if0` | 26,603 | 0.266 | 20 | 20 | fits | 26,669 | 12 | 0.720 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 80,499 | 0.805 | 220 | 220 | fits | 42,473 | 6 | 0.913 |
| an event behind 15 others | `backlog.event.if0` | 164,576 | 1.646 | 20 | 200 | fits | 61,760 | 78 | 0.564 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 487,527 | 4.875 | 20 | 20 | fits | 80,693 | 75 | 0.354 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 437,195 | 4.372 | 20 | 200 | fits | 155,790 | 109 | 0.429 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 517,272 | 5.173 | 20 | 200 | fits | 80,693 | 75 | 0.354 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 432,873 | 4.329 | 20 | 20 | fits | 155,790 | 109 | 0.429 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 512,730 | 5.127 | 20 | 20 | fits | 80,693 | 75 | 0.354 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 153,472 | 1.535 | 20 | 24 | fits | 154,363 | 158 | 0.401 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 435,523 | 4.355 | 20 | 24 | fits | 155,790 | 109 | 0.429 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 435,457 | 4.355 | 20 | 50 | fits | 155,790 | 109 | 0.429 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 435,061 | 4.351 | 20 | 50 | fits | 155,790 | 109 | 0.429 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 515,688 | 5.157 | 20 | 20 | fits | 80,693 | 75 | 0.354 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 612,974 | 6.130 | 20 | 20 | fits | 27,207 | 32 | 0.252 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 404,054 | 4.041 | 20 | 20 | fits | 158,529 | 178 | 0.410 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 307,763 | 3.078 | 20 | 200 | fits | 162,023 | 216 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 475,107 | 4.751 | 20 | 200 | fits | 158,529 | 178 | 0.410 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 308,687 | 3.087 | 20 | 20 | fits | 162,023 | 216 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 475,811 | 4.758 | 20 | 20 | fits | 158,529 | 178 | 0.410 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 150,304 | 1.503 | 20 | 24 | fits | 150,490 | 155 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 311,337 | 3.113 | 20 | 24 | fits | 162,023 | 216 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 311,271 | 3.113 | 20 | 50 | fits | 162,023 | 216 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 478,835 | 4.788 | 20 | 50 | fits | 158,529 | 178 | 0.410 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 570,285 | 5.703 | 20 | 20 | fits | 91,516 | 34 | 0.755 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 914,460 | 9.145 | 20 | 20 | fits | 79,710 | 32 | 0.553 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 26,902 | 0.269 | 20 | 20 | fits | 36,942 | 19 | 0.817 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 307,763 | 3.078 | 20 | 200 | fits | 162,023 | 216 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 53,210 | 0.532 | 20 | 200 | fits | 36,942 | 19 | 0.817 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 308,687 | 3.087 | 20 | 20 | fits | 162,023 | 216 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 463,859 | 4.639 | 20 | 20 | fits | 146,577 | 172 | 0.373 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 150,304 | 1.503 | 20 | 24 | fits | 150,490 | 155 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 311,337 | 3.113 | 20 | 24 | fits | 162,023 | 216 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 311,271 | 3.113 | 20 | 50 | fits | 162,023 | 216 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 466,883 | 4.669 | 20 | 50 | fits | 146,577 | 172 | 0.373 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 557,599 | 5.576 | 20 | 20 | fits | 90,782 | 34 | 0.751 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 901,774 | 9.018 | 20 | 20 | fits | 79,710 | 32 | 0.553 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,351,964 | 63.520 | 20 | 20 | MISS ceiling | 25,488 | 13 | 0.606 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,377,525 | 63.775 | 20 | 20 | MISS ceiling | 25,493 | 13 | 0.597 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,402,864 | 64.029 | 20 | 20 | MISS ceiling | 25,396 | 13 | 0.606 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,428,185 | 64.282 | 20 | 20 | MISS ceiling | 25,397 | 13 | 0.606 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,458,199 | 64.582 | 20 | 20 | MISS ceiling | 29,302 | 18 | 0.718 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 167,300 | 1.673 | 20 | 200 | fits | 153,876 | 177 | 0.454 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 311,647 | 3.116 | 20 | 200 | fits | 144,963 | 207 | 0.355 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 162,978 | 1.630 | 20 | 20 | fits | 153,876 | 177 | 0.454 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,233,609 | 62.336 | 20 | 20 | MISS ceiling | 39,824 | 15 | 0.747 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 166,618 | 1.666 | 20 | 24 | fits | 153,876 | 177 | 0.454 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,197,271 | 61.973 | 20 | 24 | MISS ceiling | 148,506 | 106 | 0.432 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 165,562 | 1.656 | 20 | 50 | fits | 153,876 | 177 | 0.454 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 310,129 | 3.101 | 20 | 50 | fits | 144,963 | 207 | 0.355 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 395,736 | 3.957 | 20 | 20 | fits | 85,673 | 28 | 0.735 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 749,340 | 7.493 | 20 | 20 | fits | 89,568 | 36 | 0.544 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 8,526 | 0.085 | 20 | 20 | fits | 32,780 | 13 (29) | 0.813 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 10,038 | 0.100 | 20 | 20 | fits | 35,521 | 19 (35) | 0.807 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 16,816 | 0.168 | 20 | 20 | fits | 37,293 | 21 (12) | 0.834 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 16,156 | 0.162 | 20 | 50 | fits | 37,741 | 43 | 0.733 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 27,970 | 0.280 | 20 | 50 | fits | 35,062 | 35 | 0.731 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 28,384 | 0.284 | 20 | 50 | fits | 34,748 | 35 | 0.723 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 19,064 | 0.191 | 20 | 50 | fits | 38,886 | 61 | 0.620 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 20,946 | 0.209 | 20 | 50 | fits | 38,886 | 61 | 0.620 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 14,159 | 0.142 | 20 | 50 | fits | 33,217 | 30 | 0.659 |
| LINK_UP | `adp.link_up.if0` | 2,776 | 0.028 | 20 | 200 | fits | 37,741 | 43 (11) | 0.733 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 19,134 | 0.191 | 20 | 200 | fits | 28,557 | 23 (39) | 0.765 |
| LINK_DOWN | `adp.link_down.if0` | 2,246 | 0.022 | 20 | 200 | fits | 36,227 | 23 (9) | 0.779 |
| LINK_UP | `adp.link_up.if0` | 2,776 | 0.028 | 20 | 200 | fits | 37,741 | 43 (11) | 0.733 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 19,134 | 0.191 | 20 | 200 | fits | 28,557 | 23 (39) | 0.765 |
| GM_CHANGE | `adp.gm_change.if0` | 2,316 | 0.023 | 20 | 200 | fits | 22,948 | 17 (11) | 0.761 |
| LINK_UP | `adp.link_up.if0` | 2,776 | 0.028 | 20 | 200 | fits | 37,741 | 43 (11) | 0.733 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 19,134 | 0.191 | 20 | 200 | fits | 28,557 | 23 (39) | 0.765 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,671 | 0.047 | 20 | 200 | fits | 22,966 | 16 (31) | 0.670 |
| LINK_UP | `adp.link_up.if0` | 2,776 | 0.028 | 20 | 200 | fits | 37,741 | 43 (11) | 0.733 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 19,134 | 0.191 | 20 | 200 | fits | 28,557 | 23 (39) | 0.765 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,671 | 0.047 | 20 | 200 | fits | 22,966 | 16 (31) | 0.670 |
| set_name | `aecp_fanout.set_name.if0` | 66,903 | 0.669 | 20 | 24 | fits | 63,319 | 89 | 0.576 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 45,635 | 0.456 | 20 | 24 | fits | 57,905 | 78 | 0.584 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 62,851 | 0.629 | 20 | 24 | fits | 53,554 | 79 | 0.545 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 45,619 | 0.456 | 20 | 24 | fits | 53,617 | 78 | 0.558 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 45,509 | 0.455 | 20 | 24 | fits | 57,866 | 67 | 0.576 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 62,047 | 0.620 | 20 | 24 | fits | 53,204 | 78 | 0.545 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 43,519 | 0.435 | 20 | 24 | fits | 52,930 | 79 | 0.545 |
| BIND_RX | `acmp.bind_rx.if0` | 20,410 | 0.204 | 20 | 20 | fits | 49,254 | 26 (77) | 0.792 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 10,494 | 0.105 | 20 | 20 | fits | 37,123 | 19 (32) | 0.828 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,437 | 0.104 | 20 | 20 | fits | 32,582 | 15 (47) | 0.770 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 14,644 | 0.146 | 20 | 20 | fits | 45,555 | 18 (50) | 0.819 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,757 | 0.108 | 20 | 20 | fits | 32,192 | 17 (48) | 0.730 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 16,196 | 0.162 | 20 | 20 | fits | 39,709 | 24 (48) | 0.741 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,591 | 0.096 | 20 | 20 | fits | 30,578 | 16 (48) | 0.702 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,387 | 0.094 | 20 | 20 | fits | 30,387 | 16 (48) | 0.695 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 18,281 | 0.183 | 20 | 24 | fits | 33,089 | 20 | 0.776 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 29,297 | 0.293 | 20 | 24 | fits | 36,869 | 20 | 0.701 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 20,631 | 0.206 | 20 | 24 | fits | 33,172 | 20 | 0.721 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 25,752 | 0.258 | 20 | 24 | fits | 33,136 | 20 | 0.718 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 25,383 | 0.254 | 20 | 24 | fits | 32,902 | 20 | 0.715 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 20,674 | 0.207 | 20 | 24 | fits | 33,264 | 20 | 0.718 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 25,300 | 0.253 | 20 | 24 | fits | 32,608 | 20 | 0.721 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 19,735 | 0.197 | 20 | 24 | fits | 32,084 | 20 | 0.726 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 20,324 | 0.203 | 20 | 24 | fits | 32,996 | 20 | 0.741 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 30,088 | 0.301 | 20 | 24 | fits | 38,116 | 21 | 0.655 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 19,818 | 0.198 | 20 | 24 | fits | 32,293 | 20 | 0.756 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 25,002 | 0.250 | 20 | 24 | fits | 32,201 | 20 | 0.759 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 25,001 | 0.250 | 20 | 24 | fits | 32,694 | 20 | 0.724 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 20,456 | 0.205 | 20 | 24 | fits | 33,127 | 20 | 0.721 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 25,921 | 0.259 | 20 | 24 | fits | 33,611 | 20 | 0.729 |
| get_configuration | `aecp.get_configuration.if0` | 17,938 | 0.179 | 20 | 24 | fits | 29,781 | 20 | 0.718 |
| entity_available | `aecp.entity_available.if0` | 23,304 | 0.233 | 20 | 24 | fits | 29,993 | 20 | 0.713 |
| get_name | `aecp.get_name.if0` | 25,407 | 0.254 | 20 | 24 | fits | 32,548 | 20 | 0.738 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 21,117 | 0.211 | 20 | 24 | fits | 33,513 | 27 | 0.694 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 13,249 | 0.132 | 20 | 24 | fits | 34,125 | 29 | 0.755 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 18,292 | 0.183 | 20 | 24 | fits | 30,185 | 20 | 0.745 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 23,105 | 0.231 | 20 | 24 | fits | 29,514 | 20 | 0.718 |
| set_name | `aecp.set_name.if0` | 31,666 | 0.317 | 20 | 24 | fits | 49,274 | 43 | 0.758 |
| lock_entity | `aecp.lock_entity.if0` | 23,295 | 0.233 | 20 | 24 | fits | 39,875 | 34 | 0.767 |
| unlock_entity | `aecp.unlock_entity.if0` | 29,817 | 0.298 | 20 | 24 | fits | 40,539 | 33 | 0.776 |
| LINK_UP | `fixture.link_up.if0` | 2,776 | 0.028 | 20 | 200 | fits | 37,741 | 43 (11) | 0.733 |
| malformed MRPDU discard | `fixture.malformed.if0` | 27,059 | 0.271 | 20 | 20 | fits | 27,125 | 12 | 0.759 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 35,340 | 0.353 | 20 | 24 | fits | 50,312 | 43 | 0.769 |
| LINK_DOWN | `fixture.link_down.if0` | 2,675 | 0.027 | 20 | 200 | fits | 37,789 | 23 (9) | 0.792 |
| BIND_RX | `fixture.bind_rx.if0` | 20,504 | 0.205 | 20 | 20 | fits | 49,299 | 26 (77) | 0.799 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 31,430 | 0.314 | 20 | 20 | fits | 46,401 | 29 (35) | 0.797 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 7,315 | 0.073 | 20 | 20 | fits | 33,843 | 13 (29) | 0.828 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 89,670 | 0.897 | 20 | 200 | fits | 89,774 | 51 | 0.755 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 89,670 | 0.897 | 20 | 200 | fits | 89,774 | 51 | 0.755 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 89,396 | 0.894 | 20 | 20 | fits | 89,774 | 51 | 0.755 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 89,396 | 0.894 | 20 | 20 | fits | 89,774 | 51 | 0.755 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 89,604 | 0.896 | 20 | 24 | fits | 89,774 | 51 | 0.755 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 89,604 | 0.896 | 20 | 24 | fits | 89,774 | 51 | 0.755 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 89,538 | 0.895 | 20 | 50 | fits | 89,774 | 51 | 0.755 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 89,538 | 0.895 | 20 | 50 | fits | 89,774 | 51 | 0.755 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 89,472 | 0.895 | 20 | 20 | fits | 89,774 | 51 | 0.755 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 89,472 | 0.895 | 20 | 20 | fits | 89,774 | 51 | 0.755 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
