### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 81 paths and 6 of 405 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.212 (0.400) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.101 (0.231) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.060 (0.216) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.101 (0.332) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.111 (0.267) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.100 (0.231) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.112 (0.249) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.110 (0.250) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.067 (0.255) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.107 (0.264) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.179 (0.421) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.135 (0.536) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.104 (0.354) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.062 (0.370) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.127 (0.368) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.132 (0.356) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.031 (0.110) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.015 (0.095) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.021 (0.220) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.022 (0.553) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.088 (0.192) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.129 (0.317) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.188 (0.352) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.155 (0.325) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.176 (0.333) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.216 (0.378) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.167 (0.334) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.208 (0.390) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.149 (0.317) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.206 (0.372) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.200 (0.361) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.200 (0.381) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.153 (0.320) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.221 (0.384) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.150 (0.316) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.190 (0.351) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.159 (0.325) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.159 (0.325) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.204 (0.365) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.160 (0.328) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.209 (0.372) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.169 (0.337) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.139 (0.224) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.179 (0.345) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.361 (0.650) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 0.179 (0.339) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.150 (0.253) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 0.476 (0.736) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.422 (0.654) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.491 (0.794) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.520 (0.742) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.464 (0.652) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.578 (0.859) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.499 (0.697) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.478 (0.666) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.587 (3.914) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 3.571 (5.276) | fits | 7 adp | 25 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.085 (0.347) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 0.920 (1.499) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.051 (62.233) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.242 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.327 (0.498) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.154 (0.364) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.086 (0.160) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.108 (0.553) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.134 (0.364) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.124 (0.317) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.482 | fits | 0 acmp | 29 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 5.955 | fits | 11 acmp | 29 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.473 | fits | 0 adp | 29 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 4.436 | fits | 7 adp | 29 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.518 | fits | 0 aecp | 29 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.899 | MISS ceiling | 15 aecp | 29 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.508 | fits | 0 maap | 29 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 4.473 | fits | 6 maap | 29 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.884 | fits | 0 srp | 29 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.srp.last.if0` (backlog-adp@blank-0) | 11.167 | fits | 31 srp | 29 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.630 (0.725) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.351 (0.351) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.140 (0.141) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.828 (0.910) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 12.252 | 17 | 110,262 (1.103) | yes | - |
| backlog-adp@blank-1 | 0 | 11.707 | 18 | 110,297 (1.103) | yes | - |
| backlog-adp@blank-2 | 0 | 11.732 | 18 | 110,297 (1.103) | yes | - |
| backlog-adp@blank-3 | 0 | 11.878 | 18 | 110,419 (1.104) | yes | - |
| backlog-adp@blank-4 | 0 | 11.705 | 18 | 116,290 (1.163) | yes | - |
| backlog-adp@blank-5 | 0 | 11.729 | 18 | 112,513 (1.125) | yes | - |
| backlog-adp@blank-6 | 0 | 11.628 | 18 | 110,286 (1.103) | yes | - |
| backlog-adp@blank-7 | 0 | 13.494 | 20 | 121,844 (1.218) | yes | - |
| backlog-adp@program-0 | 0 | 11.714 | 18 | 109,916 (1.099) | yes | - |
| backlog-adp@program-1 | 0 | 11.847 | 18 | 107,231 (1.072) | yes | - |
| backlog-adp@program-2 | 0 | 11.703 | 18 | 109,916 (1.099) | yes | - |
| backlog-adp@program-3 | 0 | 11.963 | 19 | 101,040 (1.010) | yes | - |
| backlog-adp@program-4 | 0 | 11.029 | 18 | 109,831 (1.098) | yes | - |
| backlog-adp@program-5 | 0 | 11.017 | 18 | 109,831 (1.098) | yes | - |
| backlog-adp@program-6 | 0 | 10.908 | 18 | 109,879 (1.099) | yes | - |
| backlog-adp@program-7 | 0 | 11.106 | 19 | 111,556 (1.116) | yes | - |
| backlog-adp@verify-0 | 0 | 12.193 | 17 | 110,024 (1.100) | yes | - |
| backlog-adp@verify-1 | 0 | 11.652 | 18 | 110,023 (1.100) | yes | - |
| backlog-adp@verify-2 | 0 | 11.748 | 19 | 110,071 (1.101) | yes | - |
| backlog-adp@verify-3 | 0 | 11.901 | 19 | 110,071 (1.101) | yes | - |
| backlog-adp@verify-4 | 0 | 11.897 | 19 | 116,187 (1.162) | yes | - |
| backlog-adp@verify-5 | 0 | 11.762 | 18 | 112,193 (1.122) | yes | - |
| backlog-adp@verify-6 | 0 | 11.812 | 19 | 109,975 (1.100) | yes | - |
| backlog-adp@verify-7 | 0 | 12.623 | 19 | 105,582 (1.056) | yes | - |
| backlog | 0 | 6.778 | 19 | 82,472 (0.825) | yes | - |
| backlog-adp | 0 | 10.919 | 19 | 110,222 (1.102) | yes | - |
| backlog-adp-refill | 0 | 40.518 | 29 | 110,222 (1.102) | yes | - |
| backlog-owed | 0 | 360.292 | 64 | 107,165 (1.072) | yes | - |
| fixture | 0 | 1.032 | 2 | 74,976 (0.750) | yes | - |

Composed maximum over the 4 backlog windows: 110,222 CPU cycles (1.102 ms), backlog-adp.
Over the windows that released their whole load only: 110,222 (1.102 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 2736 | 0 | 121,651 (1.217) | fits |
| backlog-adp@blank-0 | 388 | 0 | 110,262 (1.103) | fits |
| backlog-adp@blank-1 | 389 | 0 | 110,297 (1.103) | fits |
| backlog-adp@blank-2 | 389 | 0 | 110,297 (1.103) | fits |
| backlog-adp@blank-3 | 390 | 0 | 110,419 (1.104) | fits |
| backlog-adp@blank-4 | 389 | 0 | 116,290 (1.163) | fits |
| backlog-adp@blank-5 | 389 | 0 | 112,513 (1.125) | fits |
| backlog-adp@blank-6 | 390 | 0 | 110,286 (1.103) | fits |
| backlog-adp@blank-7 | 392 | 0 | 121,844 (1.218) | fits |
| backlog-adp@program-0 | 467 | 0 | 121,112 (1.211) | fits |
| backlog-adp@program-1 | 467 | 0 | 121,112 (1.211) | fits |
| backlog-adp@program-2 | 468 | 0 | 121,112 (1.211) | fits |
| backlog-adp@program-3 | 469 | 0 | 121,112 (1.211) | fits |
| backlog-adp@program-4 | 469 | 0 | 121,112 (1.211) | fits |
| backlog-adp@program-5 | 470 | 0 | 121,112 (1.211) | fits |
| backlog-adp@program-6 | 470 | 0 | 121,112 (1.211) | fits |
| backlog-adp@program-7 | 471 | 0 | 121,112 (1.211) | fits |
| backlog-adp@verify-0 | 539 | 0 | 121,112 (1.211) | fits |
| backlog-adp@verify-1 | 540 | 0 | 121,112 (1.211) | fits |
| backlog-adp@verify-2 | 541 | 0 | 121,112 (1.211) | fits |
| backlog-adp@verify-3 | 541 | 0 | 121,112 (1.211) | fits |
| backlog-adp@verify-4 | 541 | 0 | 121,112 (1.211) | fits |
| backlog-adp@verify-5 | 540 | 0 | 121,112 (1.211) | fits |
| backlog-adp@verify-6 | 543 | 0 | 121,112 (1.211) | fits |
| backlog-adp@verify-7 | 543 | 0 | 121,112 (1.211) | fits |
| adp-advertise | 591 | 0 | 55,316 (0.553) | fits |
| acmp-noresp | 1561 | 0 | 121,127 (1.211) | fits |
| save | 602 | 0 | 120,515 (1.205) | fits |
| srp | 284 | 0 | 72,468 (0.725) | fits |
| backlog | 293 | 0 | 82,472 (0.825) | fits |
| backlog-adp | 314 | 0 | 110,222 (1.102) | fits |
| backlog-adp-refill | 324 | 0 | 110,222 (1.102) | fits |
| backlog-owed | 349 | 0 | 107,165 (1.072) | fits |
| acmp-disc | 742 | 0 | 121,036 (1.210) | fits |
| maap | 175 | 0 | 55,316 (0.553) | fits |
| adp-link | 87 | 0 | 55,316 (0.553) | fits |
| adp-gm | 86 | 0 | 55,316 (0.553) | fits |
| adp-discover | 86 | 0 | 55,316 (0.553) | fits |
| control | 86 | 0 | 55,316 (0.553) | fits |
| aecp-fanout | 109 | 0 | 73,866 (0.739) | fits |
| acmp-cmd | 80 | 0 | 55,316 (0.553) | fits |
| aecp | 108 | 0 | 55,316 (0.553) | fits |
| fixture | 119 | 0 | 74,976 (0.750) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 6,202 | 0.062 | 20 | 20 | fits | 27,404 | 20 (14) | 0.880 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 357,133 | 3.571 | 20 | 20 | fits | 94,573 | 81 | 0.642 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 147,310 | 1.473 | 20 | 200 | fits | 77,735 | 135 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 443,620 | 4.436 | 20 | 200 | fits | 94,573 | 81 | 0.642 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 148,222 | 1.482 | 20 | 20 | fits | 77,735 | 135 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 595,480 | 5.955 | 20 | 20 | fits | 74,930 | 44 | 0.663 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 151,807 | 1.518 | 20 | 24 | fits | 77,735 | 135 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 1,086,257 | 10.863 | 20 | 24 | fits | 47,587 | 29 | 0.728 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 150,767 | 1.508 | 20 | 50 | fits | 77,735 | 135 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 447,296 | 4.473 | 20 | 50 | fits | 94,573 | 81 | 0.642 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 260,574 | 2.606 | 18 | 18 | fits | 110,262 | 138 | 0.605 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,116,739 | 11.167 | 18 | 18 | fits | 33,017 | 19 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 286,480 | 2.865 | 20 | 20 | fits | 94,573 | 81 | 0.642 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 76,638 | 0.766 | 20 | 200 | fits | 76,969 | 135 | 0.494 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 372,967 | 3.730 | 20 | 200 | fits | 94,573 | 81 | 0.642 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 77,550 | 0.775 | 20 | 20 | fits | 76,969 | 135 | 0.494 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 524,827 | 5.248 | 20 | 20 | fits | 74,930 | 44 | 0.663 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 81,135 | 0.811 | 20 | 24 | fits | 76,969 | 135 | 0.494 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 1,008,105 | 10.081 | 20 | 24 | fits | 47,622 | 29 | 0.729 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 80,095 | 0.801 | 20 | 50 | fits | 76,969 | 135 | 0.494 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 376,643 | 3.766 | 20 | 50 | fits | 94,573 | 81 | 0.642 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 189,937 | 1.899 | 18 | 18 | fits | 110,297 | 138 | 0.605 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 1,062,393 | 10.624 | 18 | 18 | fits | 23,890 | 14 | 0.821 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 288,516 | 2.885 | 20 | 20 | fits | 94,573 | 81 | 0.642 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 78,674 | 0.787 | 20 | 200 | fits | 76,969 | 135 | 0.494 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 375,003 | 3.750 | 20 | 200 | fits | 94,573 | 81 | 0.642 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 79,586 | 0.796 | 20 | 20 | fits | 76,969 | 135 | 0.494 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 529,159 | 5.292 | 20 | 20 | fits | 78,861 | 50 | 0.692 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 83,171 | 0.832 | 20 | 24 | fits | 76,969 | 135 | 0.494 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 1,010,426 | 10.104 | 20 | 24 | fits | 47,495 | 29 | 0.726 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 82,131 | 0.821 | 20 | 50 | fits | 76,969 | 135 | 0.494 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 378,679 | 3.787 | 20 | 50 | fits | 94,573 | 81 | 0.642 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 191,973 | 1.920 | 18 | 18 | fits | 110,297 | 138 | 0.605 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 1,064,871 | 10.649 | 18 | 18 | fits | 24,054 | 14 | 0.823 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 322,770 | 3.228 | 20 | 20 | fits | 90,833 | 64 | 0.680 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 109,984 | 1.100 | 20 | 200 | fits | 77,512 | 137 | 0.495 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 403,027 | 4.030 | 20 | 200 | fits | 90,833 | 64 | 0.680 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 110,896 | 1.109 | 20 | 20 | fits | 77,512 | 137 | 0.495 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 554,499 | 5.545 | 20 | 20 | fits | 75,167 | 44 | 0.665 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 36,969 | 0.370 | 20 | 24 | fits | 37,805 | 63 | 0.560 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 989,064 | 9.891 | 20 | 24 | fits | 47,579 | 29 | 0.728 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 35,929 | 0.359 | 20 | 50 | fits | 37,805 | 63 | 0.560 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 315,870 | 3.159 | 20 | 50 | fits | 92,400 | 85 | 0.648 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 223,405 | 2.234 | 18 | 18 | fits | 110,419 | 138 | 0.605 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 1,051,241 | 10.512 | 18 | 18 | fits | 31,870 | 17 | 0.783 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 293,212 | 2.932 | 20 | 20 | fits | 95,070 | 81 | 0.646 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 73,672 | 0.737 | 20 | 200 | fits | 76,969 | 135 | 0.494 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 380,094 | 3.801 | 20 | 200 | fits | 95,070 | 81 | 0.646 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 74,584 | 0.746 | 20 | 20 | fits | 76,969 | 135 | 0.494 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 510,377 | 5.104 | 20 | 20 | fits | 53,045 | 35 | 0.619 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 78,169 | 0.782 | 20 | 24 | fits | 76,969 | 135 | 0.494 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 997,267 | 9.973 | 20 | 24 | fits | 53,701 | 40 | 0.741 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 77,129 | 0.771 | 20 | 50 | fits | 76,969 | 135 | 0.494 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 383,770 | 3.838 | 20 | 50 | fits | 95,070 | 81 | 0.646 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 192,964 | 1.930 | 18 | 18 | fits | 116,290 | 149 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 1,062,116 | 10.621 | 18 | 18 | fits | 31,742 | 17 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 293,822 | 2.938 | 20 | 20 | fits | 71,700 | 72 | 0.593 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 81,418 | 0.814 | 20 | 200 | fits | 82,679 | 146 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 357,364 | 3.574 | 20 | 200 | fits | 71,700 | 72 | 0.593 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 82,330 | 0.823 | 20 | 20 | fits | 82,679 | 146 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 512,794 | 5.128 | 20 | 20 | fits | 75,426 | 44 | 0.669 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 85,915 | 0.859 | 20 | 24 | fits | 82,679 | 146 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 1,001,962 | 10.020 | 20 | 24 | fits | 47,630 | 29 | 0.728 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 84,875 | 0.849 | 20 | 50 | fits | 82,679 | 146 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 361,040 | 3.610 | 20 | 50 | fits | 71,700 | 72 | 0.593 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 196,933 | 1.969 | 18 | 18 | fits | 112,513 | 143 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 1,064,570 | 10.646 | 18 | 18 | fits | 32,094 | 17 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 266,078 | 2.661 | 20 | 20 | fits | 97,788 | 87 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 75,837 | 0.758 | 20 | 200 | fits | 76,800 | 135 | 0.495 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 352,583 | 3.526 | 20 | 200 | fits | 97,788 | 87 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 76,749 | 0.767 | 20 | 20 | fits | 76,800 | 135 | 0.495 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 504,725 | 5.047 | 20 | 20 | fits | 74,872 | 44 | 0.663 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 80,334 | 0.803 | 20 | 24 | fits | 76,800 | 135 | 0.495 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 992,132 | 9.921 | 20 | 24 | fits | 47,486 | 29 | 0.727 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 79,294 | 0.793 | 20 | 50 | fits | 76,800 | 135 | 0.495 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 356,259 | 3.563 | 20 | 50 | fits | 97,788 | 87 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 189,125 | 1.891 | 18 | 18 | fits | 110,286 | 138 | 0.605 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 1,054,384 | 10.544 | 18 | 18 | fits | 31,734 | 17 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 266,157 | 2.662 | 20 | 20 | fits | 95,363 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 77,873 | 0.779 | 20 | 200 | fits | 76,800 | 135 | 0.495 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 353,270 | 3.533 | 20 | 200 | fits | 95,363 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 78,785 | 0.788 | 20 | 20 | fits | 76,800 | 135 | 0.495 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 505,268 | 5.053 | 20 | 20 | fits | 74,930 | 44 | 0.663 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 82,370 | 0.824 | 20 | 24 | fits | 76,800 | 135 | 0.495 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 992,969 | 9.930 | 20 | 24 | fits | 47,549 | 29 | 0.727 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 81,330 | 0.813 | 20 | 50 | fits | 76,800 | 135 | 0.495 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 356,946 | 3.569 | 20 | 50 | fits | 95,363 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 261,518 | 2.615 | 18 | 18 | fits | 105,841 | 102 | 0.636 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 1,055,221 | 10.552 | 18 | 18 | fits | 31,906 | 17 | 0.783 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 289,480 | 2.895 | 20 | 20 | fits | 94,573 | 81 | 0.642 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 79,995 | 0.800 | 20 | 200 | fits | 77,136 | 135 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 375,967 | 3.760 | 20 | 200 | fits | 94,573 | 81 | 0.642 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 80,907 | 0.809 | 20 | 20 | fits | 77,136 | 135 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 514,327 | 5.143 | 20 | 20 | fits | 77,895 | 50 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 84,492 | 0.845 | 20 | 24 | fits | 77,136 | 135 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 995,452 | 9.955 | 20 | 24 | fits | 47,529 | 29 | 0.728 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 83,452 | 0.835 | 20 | 50 | fits | 77,136 | 135 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 379,643 | 3.796 | 20 | 50 | fits | 94,573 | 81 | 0.642 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 192,913 | 1.929 | 18 | 18 | fits | 109,916 | 138 | 0.604 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 1,057,662 | 10.577 | 18 | 18 | fits | 31,786 | 17 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 285,975 | 2.860 | 20 | 20 | fits | 95,032 | 81 | 0.646 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 75,084 | 0.751 | 20 | 200 | fits | 77,136 | 135 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 372,729 | 3.727 | 20 | 200 | fits | 95,032 | 81 | 0.646 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 75,996 | 0.760 | 20 | 20 | fits | 77,136 | 135 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 524,727 | 5.247 | 20 | 20 | fits | 75,016 | 44 | 0.664 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 79,581 | 0.796 | 20 | 24 | fits | 77,136 | 135 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 1,008,638 | 10.086 | 20 | 24 | fits | 57,626 | 47 | 0.748 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 78,541 | 0.785 | 20 | 50 | fits | 77,136 | 135 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 376,405 | 3.764 | 20 | 50 | fits | 95,032 | 81 | 0.646 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 185,317 | 1.853 | 18 | 18 | fits | 107,231 | 145 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 1,070,906 | 10.709 | 18 | 18 | fits | 31,742 | 17 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 286,960 | 2.870 | 20 | 20 | fits | 94,573 | 81 | 0.642 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 77,475 | 0.775 | 20 | 200 | fits | 77,075 | 135 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 373,447 | 3.734 | 20 | 200 | fits | 94,573 | 81 | 0.642 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 78,387 | 0.784 | 20 | 20 | fits | 77,075 | 135 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 506,373 | 5.064 | 20 | 20 | fits | 78,265 | 50 | 0.671 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 81,972 | 0.820 | 20 | 24 | fits | 77,075 | 135 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 993,852 | 9.939 | 20 | 24 | fits | 47,569 | 29 | 0.727 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 80,932 | 0.809 | 20 | 50 | fits | 77,075 | 135 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 377,123 | 3.771 | 20 | 50 | fits | 94,573 | 81 | 0.642 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 190,393 | 1.904 | 18 | 18 | fits | 109,916 | 138 | 0.604 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 1,056,459 | 10.565 | 18 | 18 | fits | 32,110 | 17 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 277,132 | 2.771 | 20 | 20 | fits | 94,951 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 72,473 | 0.725 | 20 | 200 | fits | 77,075 | 135 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 363,850 | 3.639 | 20 | 200 | fits | 94,951 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 73,385 | 0.734 | 20 | 20 | fits | 77,075 | 135 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 526,979 | 5.270 | 20 | 20 | fits | 86,117 | 62 | 0.705 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 76,970 | 0.770 | 20 | 24 | fits | 77,075 | 135 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 1,003,854 | 10.039 | 20 | 24 | fits | 47,470 | 29 | 0.726 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 75,930 | 0.759 | 20 | 50 | fits | 77,075 | 135 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 367,526 | 3.675 | 20 | 50 | fits | 94,951 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 176,515 | 1.765 | 18 | 18 | fits | 101,040 | 134 | 0.599 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 1,058,051 | 10.581 | 18 | 18 | fits | 23,890 | 14 | 0.821 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 271,613 | 2.716 | 20 | 20 | fits | 97,374 | 87 | 0.653 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 77,099 | 0.771 | 20 | 200 | fits | 77,100 | 135 | 0.499 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 358,897 | 3.589 | 20 | 200 | fits | 97,374 | 87 | 0.653 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 78,011 | 0.780 | 20 | 20 | fits | 77,100 | 135 | 0.499 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 511,117 | 5.111 | 20 | 20 | fits | 74,934 | 44 | 0.663 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 81,596 | 0.816 | 20 | 24 | fits | 77,100 | 135 | 0.499 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 993,014 | 9.930 | 20 | 24 | fits | 47,544 | 29 | 0.727 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 80,556 | 0.806 | 20 | 50 | fits | 77,100 | 135 | 0.499 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 362,573 | 3.626 | 20 | 50 | fits | 97,374 | 87 | 0.653 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 189,932 | 1.899 | 18 | 18 | fits | 109,831 | 138 | 0.603 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 1,065,586 | 10.656 | 18 | 18 | fits | 31,914 | 17 | 0.783 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 288,945 | 2.889 | 20 | 20 | fits | 94,573 | 81 | 0.642 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 79,417 | 0.794 | 20 | 200 | fits | 77,075 | 135 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 375,432 | 3.754 | 20 | 200 | fits | 94,573 | 81 | 0.642 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 80,329 | 0.803 | 20 | 20 | fits | 77,075 | 135 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 527,292 | 5.273 | 20 | 20 | fits | 74,930 | 44 | 0.663 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 83,914 | 0.839 | 20 | 24 | fits | 77,075 | 135 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 1,010,035 | 10.100 | 20 | 24 | fits | 47,622 | 29 | 0.729 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 82,874 | 0.829 | 20 | 50 | fits | 77,075 | 135 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 379,108 | 3.791 | 20 | 50 | fits | 94,573 | 81 | 0.642 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 192,250 | 1.923 | 18 | 18 | fits | 109,831 | 138 | 0.603 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 1,064,323 | 10.643 | 18 | 18 | fits | 23,890 | 14 | 0.821 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 283,863 | 2.839 | 20 | 20 | fits | 94,573 | 81 | 0.642 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 74,415 | 0.744 | 20 | 200 | fits | 77,075 | 135 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 370,350 | 3.704 | 20 | 200 | fits | 94,573 | 81 | 0.642 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 75,327 | 0.753 | 20 | 20 | fits | 77,075 | 135 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 509,212 | 5.092 | 20 | 20 | fits | 84,201 | 61 | 0.687 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 78,912 | 0.789 | 20 | 24 | fits | 77,075 | 135 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 990,785 | 9.908 | 20 | 24 | fits | 47,550 | 29 | 0.727 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 77,872 | 0.779 | 20 | 50 | fits | 77,075 | 135 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 374,026 | 3.740 | 20 | 50 | fits | 94,573 | 81 | 0.642 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 187,296 | 1.873 | 18 | 18 | fits | 109,879 | 138 | 0.603 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 1,053,392 | 10.534 | 18 | 18 | fits | 31,982 | 17 | 0.783 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 274,825 | 2.748 | 20 | 20 | fits | 98,764 | 87 | 0.668 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 78,487 | 0.785 | 20 | 200 | fits | 77,075 | 135 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 363,072 | 3.631 | 20 | 200 | fits | 98,764 | 87 | 0.668 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 79,399 | 0.794 | 20 | 20 | fits | 77,075 | 135 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 515,616 | 5.156 | 20 | 20 | fits | 75,190 | 44 | 0.666 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 82,984 | 0.830 | 20 | 24 | fits | 77,075 | 135 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 993,591 | 9.936 | 20 | 24 | fits | 47,451 | 29 | 0.726 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 81,944 | 0.819 | 20 | 50 | fits | 77,075 | 135 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 366,748 | 3.667 | 20 | 50 | fits | 98,764 | 87 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 267,919 | 2.679 | 18 | 18 | fits | 111,556 | 113 | 0.650 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 1,062,471 | 10.625 | 18 | 18 | fits | 38,445 | 28 | 0.793 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 350,873 | 3.509 | 20 | 20 | fits | 94,573 | 81 | 0.642 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 141,264 | 1.413 | 20 | 200 | fits | 78,047 | 135 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 437,360 | 4.374 | 20 | 200 | fits | 94,573 | 81 | 0.642 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 142,176 | 1.422 | 20 | 20 | fits | 78,047 | 135 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 589,220 | 5.892 | 20 | 20 | fits | 74,930 | 44 | 0.663 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 145,761 | 1.458 | 20 | 24 | fits | 78,047 | 135 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 1,080,081 | 10.801 | 20 | 24 | fits | 47,587 | 29 | 0.728 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 144,721 | 1.447 | 20 | 50 | fits | 78,047 | 135 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 441,036 | 4.410 | 20 | 50 | fits | 94,573 | 81 | 0.642 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 254,290 | 2.543 | 18 | 18 | fits | 110,024 | 138 | 0.604 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,110,563 | 11.106 | 18 | 18 | fits | 33,017 | 19 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 289,486 | 2.895 | 20 | 20 | fits | 94,573 | 81 | 0.642 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 79,766 | 0.798 | 20 | 200 | fits | 77,400 | 135 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 375,973 | 3.760 | 20 | 200 | fits | 94,573 | 81 | 0.642 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 80,678 | 0.807 | 20 | 20 | fits | 77,400 | 135 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 527,833 | 5.278 | 20 | 20 | fits | 74,930 | 44 | 0.663 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 84,263 | 0.843 | 20 | 24 | fits | 77,400 | 135 | 0.501 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 994,288 | 9.943 | 20 | 24 | fits | 47,436 | 29 | 0.727 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 83,223 | 0.832 | 20 | 50 | fits | 77,400 | 135 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 379,649 | 3.796 | 20 | 50 | fits | 94,573 | 81 | 0.642 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 192,791 | 1.928 | 18 | 18 | fits | 110,023 | 138 | 0.603 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 1,056,498 | 10.565 | 18 | 18 | fits | 31,742 | 17 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 282,368 | 2.824 | 20 | 20 | fits | 94,573 | 81 | 0.642 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 72,728 | 0.727 | 20 | 200 | fits | 77,400 | 135 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 368,855 | 3.689 | 20 | 200 | fits | 94,573 | 81 | 0.642 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 73,640 | 0.736 | 20 | 20 | fits | 77,400 | 135 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 523,011 | 5.230 | 20 | 20 | fits | 78,861 | 50 | 0.692 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 77,225 | 0.772 | 20 | 24 | fits | 77,400 | 135 | 0.501 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 980,003 | 9.800 | 20 | 24 | fits | 47,393 | 29 | 0.726 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 76,185 | 0.762 | 20 | 50 | fits | 77,400 | 135 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 372,531 | 3.725 | 20 | 50 | fits | 94,573 | 81 | 0.642 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 185,801 | 1.858 | 18 | 18 | fits | 110,071 | 138 | 0.604 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 1,066,109 | 10.661 | 18 | 18 | fits | 23,987 | 14 | 0.822 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 284,404 | 2.844 | 20 | 20 | fits | 77,554 | 83 | 0.613 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 74,764 | 0.748 | 20 | 200 | fits | 77,400 | 135 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 353,872 | 3.539 | 20 | 200 | fits | 77,554 | 83 | 0.613 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 75,676 | 0.757 | 20 | 20 | fits | 77,400 | 135 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 508,880 | 5.089 | 20 | 20 | fits | 75,459 | 44 | 0.670 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 79,261 | 0.793 | 20 | 24 | fits | 77,400 | 135 | 0.501 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 991,014 | 9.910 | 20 | 24 | fits | 47,506 | 29 | 0.727 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 78,221 | 0.782 | 20 | 50 | fits | 77,400 | 135 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 357,548 | 3.575 | 20 | 50 | fits | 77,554 | 83 | 0.613 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 187,837 | 1.878 | 18 | 18 | fits | 110,071 | 138 | 0.604 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 1,053,621 | 10.536 | 18 | 18 | fits | 31,938 | 17 | 0.783 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 296,007 | 2.960 | 20 | 20 | fits | 94,944 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 76,800 | 0.768 | 20 | 200 | fits | 77,400 | 135 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 382,763 | 3.828 | 20 | 200 | fits | 94,944 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 77,712 | 0.777 | 20 | 20 | fits | 77,400 | 135 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 512,964 | 5.130 | 20 | 20 | fits | 53,045 | 35 | 0.619 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 81,297 | 0.813 | 20 | 24 | fits | 77,400 | 135 | 0.501 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 992,182 | 9.922 | 20 | 24 | fits | 45,932 | 36 | 0.759 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 80,257 | 0.803 | 20 | 50 | fits | 77,400 | 135 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 386,439 | 3.864 | 20 | 50 | fits | 94,944 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 195,989 | 1.960 | 18 | 18 | fits | 116,187 | 149 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 1,081,029 | 10.810 | 18 | 18 | fits | 23,823 | 14 | 0.819 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 296,636 | 2.966 | 20 | 20 | fits | 71,700 | 72 | 0.593 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 84,656 | 0.847 | 20 | 200 | fits | 83,220 | 146 | 0.526 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 360,178 | 3.602 | 20 | 200 | fits | 71,700 | 72 | 0.593 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 85,568 | 0.856 | 20 | 20 | fits | 83,220 | 146 | 0.526 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 515,608 | 5.156 | 20 | 20 | fits | 75,426 | 44 | 0.669 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 89,153 | 0.892 | 20 | 24 | fits | 83,220 | 146 | 0.526 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 1,004,873 | 10.049 | 20 | 24 | fits | 47,630 | 29 | 0.728 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 88,113 | 0.881 | 20 | 50 | fits | 83,220 | 146 | 0.526 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 363,854 | 3.639 | 20 | 50 | fits | 71,700 | 72 | 0.593 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 199,851 | 1.999 | 18 | 18 | fits | 112,193 | 143 | 0.609 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 1,067,480 | 10.675 | 18 | 18 | fits | 32,110 | 17 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 268,213 | 2.682 | 20 | 20 | fits | 97,688 | 87 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 78,181 | 0.782 | 20 | 200 | fits | 77,031 | 135 | 0.499 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 354,618 | 3.546 | 20 | 200 | fits | 97,688 | 87 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 79,093 | 0.791 | 20 | 20 | fits | 77,031 | 135 | 0.499 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 506,712 | 5.067 | 20 | 20 | fits | 74,848 | 44 | 0.663 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 82,678 | 0.827 | 20 | 24 | fits | 77,031 | 135 | 0.499 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 986,175 | 9.862 | 20 | 24 | fits | 47,622 | 29 | 0.729 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 81,638 | 0.816 | 20 | 50 | fits | 77,031 | 135 | 0.499 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 358,294 | 3.583 | 20 | 50 | fits | 97,688 | 87 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 191,158 | 1.912 | 18 | 18 | fits | 109,975 | 138 | 0.603 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 1,072,430 | 10.724 | 18 | 18 | fits | 23,987 | 14 | 0.822 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 268,238 | 2.682 | 20 | 20 | fits | 95,387 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 80,126 | 0.801 | 20 | 200 | fits | 77,031 | 135 | 0.499 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 355,310 | 3.553 | 20 | 200 | fits | 95,387 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 81,038 | 0.810 | 20 | 20 | fits | 77,031 | 135 | 0.499 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 507,308 | 5.073 | 20 | 20 | fits | 74,930 | 44 | 0.663 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 84,623 | 0.846 | 20 | 24 | fits | 77,031 | 135 | 0.499 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 994,898 | 9.949 | 20 | 24 | fits | 47,538 | 29 | 0.727 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 83,583 | 0.836 | 20 | 50 | fits | 77,031 | 135 | 0.499 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 358,986 | 3.590 | 20 | 50 | fits | 95,387 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 263,534 | 2.635 | 18 | 18 | fits | 105,582 | 102 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 1,057,166 | 10.572 | 18 | 18 | fits | 31,786 | 17 | 0.781 |
| LINK_UP | `adp.link_up.if0` | 2,155 | 0.022 | 20 | 200 | fits | 55,316 | 49 (11) | 0.748 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,888 | 0.129 | 20 | 200 | fits | 17,105 | 25 (39) | 0.608 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 8,845 | 0.088 | 20 | 200 | fits | 1,912 | 9 (11) | 0.450 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 10,234 | 0.102 | 20 | 20 | fits | 25,904 | 23 (35) | 0.763 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 10,383 | 0.104 | 20 | 20 | fits | 20,223 | 18 (14) | 0.839 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 12,708 | 0.127 | 20 | 20 | fits | 20,035 | 19 (14) | 0.826 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 10,686 | 0.107 | 20 | 20 | fits | 26,377 | 23 (35) | 0.776 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 82,801 | 0.828 | 18 | 18 | fits | 35,684 | 13 | 0.836 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 35,060 | 0.351 | 18 | 18 | fits | 35,125 | 14 | 0.887 |
| malformed MRPDU discard | `srp.malformed.if0` | 13,494 | 0.135 | 18 | 18 | fits | 13,559 | 14 | 0.644 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 62,978 | 0.630 | 218 | 218 | fits | 72,468 | 21 | 0.870 |
| an event behind 15 others | `backlog.event.if0` | 91,980 | 0.920 | 20 | 200 | fits | 67,440 | 104 | 0.497 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 358,657 | 3.587 | 20 | 20 | fits | 49,967 | 44 | 0.515 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 82,214 | 0.822 | 20 | 200 | fits | 82,422 | 138 | 0.511 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 289,939 | 2.899 | 20 | 200 | fits | 58,422 | 55 | 0.537 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 77,955 | 0.780 | 20 | 20 | fits | 82,422 | 138 | 0.511 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 386,149 | 3.861 | 20 | 20 | fits | 49,967 | 44 | 0.515 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 81,540 | 0.815 | 20 | 24 | fits | 82,422 | 138 | 0.511 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 621,782 | 6.218 | 20 | 24 | fits | 23,247 | 29 | 0.479 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 80,500 | 0.805 | 20 | 50 | fits | 82,422 | 138 | 0.511 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 288,444 | 2.884 | 20 | 50 | fits | 58,422 | 55 | 0.537 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 288,379 | 2.884 | 18 | 18 | fits | 58,422 | 55 | 0.537 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 649,478 | 6.495 | 18 | 18 | fits | 9,757 | 17 | 0.361 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 281,013 | 2.810 | 20 | 20 | fits | 77,607 | 83 | 0.612 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 71,378 | 0.714 | 20 | 200 | fits | 76,060 | 135 | 0.480 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 350,601 | 3.506 | 20 | 200 | fits | 77,607 | 83 | 0.612 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 72,290 | 0.723 | 20 | 20 | fits | 76,060 | 135 | 0.480 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 505,566 | 5.056 | 20 | 20 | fits | 75,454 | 44 | 0.670 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 75,875 | 0.759 | 20 | 24 | fits | 76,060 | 135 | 0.480 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 962,999 | 9.630 | 20 | 24 | fits | 47,545 | 29 | 0.727 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 74,835 | 0.748 | 20 | 50 | fits | 76,060 | 135 | 0.480 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 354,277 | 3.543 | 20 | 50 | fits | 77,607 | 83 | 0.612 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 184,602 | 1.846 | 18 | 18 | fits | 110,222 | 138 | 0.605 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,057,590 | 10.576 | 18 | 18 | fits | 31,994 | 17 | 0.784 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,458 | 0.085 | 20 | 20 | fits | 21,773 | 20 | 0.766 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 71,378 | 0.714 | 20 | 200 | fits | 76,060 | 135 | 0.480 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 23,953 | 0.240 | 20 | 200 | fits | 21,773 | 20 | 0.766 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 72,290 | 0.723 | 20 | 20 | fits | 76,060 | 135 | 0.480 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 495,352 | 4.954 | 20 | 20 | fits | 75,316 | 44 | 0.669 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 75,875 | 0.759 | 20 | 24 | fits | 76,060 | 135 | 0.480 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 967,991 | 9.680 | 20 | 24 | fits | 47,560 | 29 | 0.728 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 74,835 | 0.748 | 20 | 50 | fits | 76,060 | 135 | 0.480 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 344,492 | 3.445 | 20 | 50 | fits | 67,822 | 73 | 0.603 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 184,602 | 1.846 | 18 | 18 | fits | 110,222 | 138 | 0.605 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,055,302 | 10.553 | 18 | 18 | fits | 23,818 | 14 | 0.819 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,205,142 | 62.051 | 20 | 20 | MISS ceiling | 28,365 | 25 | 0.599 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,024,168 | 360.242 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,024,093 | 360.241 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,024,018 | 360.240 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,023,943 | 360.239 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 74,255 | 0.743 | 20 | 200 | fits | 72,523 | 129 | 0.485 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 351,879 | 3.519 | 20 | 200 | fits | 82,430 | 67 | 0.655 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 69,996 | 0.700 | 20 | 20 | fits | 72,523 | 129 | 0.485 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 470,797 | 4.708 | 20 | 20 | fits | 62,062 | 39 | 0.763 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 73,581 | 0.736 | 20 | 24 | fits | 72,523 | 129 | 0.485 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,289,919 | 62.899 | 20 | 24 | MISS ceiling | 21,872 | 21 | 0.577 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 72,541 | 0.725 | 20 | 50 | fits | 72,523 | 129 | 0.485 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 350,384 | 3.504 | 20 | 50 | fits | 82,430 | 67 | 0.655 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 179,251 | 1.793 | 18 | 18 | fits | 107,165 | 131 | 0.626 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 820,716 | 8.207 | 18 | 18 | fits | 31,647 | 20 | 0.770 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 4,380 | 0.044 | 20 | 20 | fits | 19,321 | 14 (29) | 0.748 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 5,964 | 0.060 | 20 | 20 | fits | 21,607 | 20 (35) | 0.768 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 17,918 | 0.179 | 20 | 20 | fits | 26,152 | 23 (12) | 0.768 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 10,808 | 0.108 | 20 | 50 | fits | 55,316 | 49 | 0.748 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 10,184 | 0.102 | 20 | 50 | fits | 17,532 | 37 | 0.655 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 12,414 | 0.124 | 20 | 50 | fits | 17,088 | 37 | 0.642 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 13,360 | 0.134 | 20 | 50 | fits | 23,442 | 64 | 0.588 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 15,395 | 0.154 | 20 | 50 | fits | 23,442 | 64 | 0.588 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 8,599 | 0.086 | 20 | 50 | fits | 16,026 | 32 | 0.569 |
| LINK_UP | `adp.link_up.if0` | 2,155 | 0.022 | 20 | 200 | fits | 55,316 | 49 (11) | 0.748 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,888 | 0.129 | 20 | 200 | fits | 17,105 | 25 (39) | 0.608 |
| LINK_DOWN | `adp.link_down.if0` | 1,730 | 0.017 | 20 | 200 | fits | 20,278 | 22 (9) | 0.769 |
| LINK_UP | `adp.link_up.if0` | 2,155 | 0.022 | 20 | 200 | fits | 55,316 | 49 (11) | 0.748 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,888 | 0.129 | 20 | 200 | fits | 17,105 | 25 (39) | 0.608 |
| GM_CHANGE | `adp.gm_change.if0` | 1,536 | 0.015 | 20 | 200 | fits | 9,546 | 18 (11) | 0.575 |
| LINK_UP | `adp.link_up.if0` | 2,155 | 0.022 | 20 | 200 | fits | 55,316 | 49 (11) | 0.748 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,888 | 0.129 | 20 | 200 | fits | 17,105 | 25 (39) | 0.608 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 3,124 | 0.031 | 20 | 200 | fits | 11,005 | 17 (31) | 0.589 |
| LINK_UP | `adp.link_up.if0` | 2,155 | 0.022 | 20 | 200 | fits | 55,316 | 49 (11) | 0.748 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,888 | 0.129 | 20 | 200 | fits | 17,105 | 25 (39) | 0.608 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 3,124 | 0.031 | 20 | 200 | fits | 11,005 | 17 (31) | 0.589 |
| set_name | `aecp_fanout.set_name.if0` | 57,831 | 0.578 | 20 | 24 | fits | 73,866 | 120 | 0.386 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 52,025 | 0.520 | 20 | 24 | fits | 57,698 | 110 | 0.428 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 41,598 | 0.416 | 20 | 24 | fits | 48,669 | 110 | 0.356 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 46,373 | 0.464 | 20 | 24 | fits | 48,790 | 110 | 0.361 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 49,142 | 0.491 | 20 | 24 | fits | 63,327 | 99 | 0.412 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 47,637 | 0.476 | 20 | 24 | fits | 61,854 | 99 | 0.410 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 49,858 | 0.499 | 20 | 24 | fits | 55,668 | 99 | 0.431 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 42,218 | 0.422 | 20 | 24 | fits | 49,150 | 110 | 0.344 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 47,785 | 0.478 | 20 | 24 | fits | 48,928 | 110 | 0.343 |
| BIND_RX | `acmp.bind_rx.if0` | 21,083 | 0.211 | 20 | 20 | fits | 40,857 | 29 (77) | 0.756 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 6,735 | 0.067 | 20 | 20 | fits | 25,456 | 20 (32) | 0.809 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 11,109 | 0.111 | 20 | 20 | fits | 26,723 | 17 (47) | 0.747 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,169 | 0.132 | 20 | 20 | fits | 35,584 | 20 (50) | 0.805 |
| PROBE_TX | `acmp.probe_tx.if0` | 10,999 | 0.110 | 20 | 20 | fits | 24,957 | 19 (48) | 0.716 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 11,225 | 0.112 | 20 | 20 | fits | 24,894 | 18 (48) | 0.711 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 10,121 | 0.101 | 20 | 20 | fits | 23,141 | 18 (48) | 0.672 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 9,985 | 0.100 | 20 | 20 | fits | 23,059 | 18 (48) | 0.672 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 17,932 | 0.179 | 20 | 24 | fits | 21,573 | 22 | 0.736 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 20,582 | 0.206 | 20 | 24 | fits | 24,608 | 22 | 0.663 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 20,034 | 0.200 | 20 | 24 | fits | 19,776 | 22 | 0.659 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 15,897 | 0.159 | 20 | 24 | fits | 19,848 | 22 | 0.635 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 20,915 | 0.209 | 20 | 24 | fits | 20,815 | 22 | 0.638 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 16,871 | 0.169 | 20 | 24 | fits | 21,126 | 22 | 0.657 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 13,894 | 0.139 | 20 | 24 | fits | 22,369 | 28 | 0.660 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 20,030 | 0.200 | 20 | 24 | fits | 19,870 | 22 | 0.662 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 15,315 | 0.153 | 20 | 24 | fits | 19,335 | 22 | 0.659 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 22,147 | 0.221 | 20 | 24 | fits | 21,979 | 22 | 0.534 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 14,966 | 0.150 | 20 | 24 | fits | 19,017 | 22 | 0.674 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 19,004 | 0.190 | 20 | 24 | fits | 18,665 | 22 | 0.647 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 15,910 | 0.159 | 20 | 24 | fits | 19,961 | 22 | 0.657 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 20,390 | 0.204 | 20 | 24 | fits | 20,111 | 22 | 0.647 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 15,986 | 0.160 | 20 | 24 | fits | 20,183 | 22 | 0.676 |
| get_configuration | `aecp.get_configuration.if0` | 17,630 | 0.176 | 20 | 24 | fits | 16,928 | 22 | 0.632 |
| entity_available | `aecp.entity_available.if0` | 18,801 | 0.188 | 20 | 24 | fits | 18,199 | 22 | 0.653 |
| get_name | `aecp.get_name.if0` | 16,650 | 0.167 | 20 | 24 | fits | 20,820 | 22 | 0.700 |
| get_counters | `aecp.get_counters.if0` | 21,597 | 0.216 | 20 | 24 | fits | 21,465 | 29 | 0.658 |
| get_avb_info | `aecp.get_avb_info.if0` | 15,490 | 0.155 | 20 | 24 | fits | 19,598 | 22 | 0.718 |
| unknown_command | `aecp.unknown_command.if0` | 17,902 | 0.179 | 20 | 24 | fits | 17,498 | 22 | 0.661 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 14,919 | 0.149 | 20 | 24 | fits | 18,593 | 22 | 0.688 |
| set_name | `aecp.set_name.if0` | 36,098 | 0.361 | 20 | 24 | fits | 48,620 | 45 | 0.689 |
| lock_entity | `aecp.lock_entity.if0` | 20,812 | 0.208 | 20 | 24 | fits | 27,733 | 35 | 0.716 |
| unlock_entity | `aecp.unlock_entity.if0` | 15,031 | 0.150 | 20 | 24 | fits | 25,328 | 34 | 0.661 |
| LINK_UP | `fixture.link_up.if0` | 2,155 | 0.022 | 20 | 200 | fits | 55,316 | 49 (11) | 0.748 |
| malformed MRPDU discard | `fixture.malformed.if0` | 14,014 | 0.140 | 18 | 18 | fits | 14,079 | 14 | 0.694 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 32,695 | 0.327 | 20 | 24 | fits | 49,792 | 45 | 0.706 |
| LINK_DOWN | `fixture.link_down.if0` | 2,052 | 0.021 | 20 | 200 | fits | 22,011 | 22 (9) | 0.797 |
| BIND_RX | `fixture.bind_rx.if0` | 21,182 | 0.212 | 20 | 20 | fits | 40,046 | 29 (77) | 0.751 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 13,513 | 0.135 | 20 | 20 | fits | 40,800 | 49 (35) | 0.715 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 10,121 | 0.101 | 20 | 20 | fits | 19,238 | 14 (29) | 0.761 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 74,873 | 0.749 | 20 | 200 | fits | 74,976 | 55 | 0.742 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 74,873 | 0.749 | 20 | 200 | fits | 74,976 | 55 | 0.742 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 74,603 | 0.746 | 20 | 20 | fits | 74,976 | 55 | 0.742 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 74,603 | 0.746 | 20 | 20 | fits | 74,976 | 55 | 0.742 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 74,808 | 0.748 | 20 | 24 | fits | 74,976 | 55 | 0.742 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 74,808 | 0.748 | 20 | 24 | fits | 74,976 | 55 | 0.742 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 74,743 | 0.747 | 20 | 50 | fits | 74,976 | 55 | 0.742 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 74,743 | 0.747 | 20 | 50 | fits | 74,976 | 55 | 0.742 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 74,678 | 0.747 | 18 | 18 | fits | 74,976 | 55 | 0.742 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 74,678 | 0.747 | 18 | 18 | fits | 74,976 | 55 | 0.742 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
