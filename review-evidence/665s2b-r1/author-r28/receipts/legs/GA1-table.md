### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 87 paths and 6 of 945 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.226 (0.407) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.119 (0.236) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.063 (0.212) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.057 (0.202) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.127 (0.268) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.108 (0.236) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.122 (0.250) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.126 (0.257) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.082 (0.256) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.132 (0.402) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.164 (0.419) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.239 (0.513) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.135 (0.404) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.086 (0.413) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.106 (0.365) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.145 (0.341) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.049 (0.110) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.021 (0.107) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.027 (0.223) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.024 (0.221) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.049 (0.161) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.169 (0.382) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.172 (0.370) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.163 (0.374) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.127 (0.327) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.210 (0.411) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.150 (0.359) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.226 (0.417) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.123 (0.329) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.183 (0.397) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.196 (0.395) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.193 (0.394) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.142 (0.349) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.209 (0.413) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.135 (0.345) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.177 (0.384) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.148 (0.351) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.137 (0.350) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.196 (0.393) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.147 (0.352) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.198 (0.401) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.153 (0.361) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.148 (0.354) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.150 (0.367) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.308 (0.538) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.172 (0.378) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.234 (0.437) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 0.457 (0.677) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.427 (0.637) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.469 (0.694) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.395 (0.479) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.435 (0.649) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.494 (0.722) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.353 (0.455) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.379 (0.579) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.911 (5.512) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 7.746 (9.344) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.112 (0.385) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.711 (2.432) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.601 (62.836) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.264 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.268 (0.361) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 7.533 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 6.271 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 3.136 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 5.675 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 5.199 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.140 (0.367) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.107 (0.178) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.114 (0.221) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.119 (0.367) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.169 (0.379) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 0.882 | fits | 0 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 2.226 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@program-aged2-4.service.acmp.last.if0` (backlog-adp@program-aged2-4) | 9.532 | fits | 11 acmp | 77 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 2.217 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-4.service.adp.last.if0` (backlog-adp@program-aged2-4) | 8.576 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.262 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.772 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 2.251 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-4.service.maap.last.if0` (backlog-adp@program-aged2-4) | 8.613 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-7.service.srp.first.if0` (backlog-adp@blank-aged2-7) | 6.627 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.srp.last.if0` (backlog-adp@blank-aged2-7) | 8.461 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.803 (1.166) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.358 (0.358) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.141 (0.142) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.780 (0.851) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 9.654 | 8 | 155,635 (1.556) | yes | - |
| backlog-adp@blank-1 | 0 | 9.800 | 9 | 155,685 (1.557) | yes | - |
| backlog-adp@blank-2 | 0 | 9.785 | 8 | 152,156 (1.522) | yes | - |
| backlog-adp@blank-3 | 0 | 9.805 | 8 | 156,160 (1.562) | yes | - |
| backlog-adp@blank-4 | 0 | 9.879 | 8 | 152,267 (1.523) | yes | - |
| backlog-adp@blank-5 | 0 | 10.079 | 10 | 151,049 (1.510) | yes | - |
| backlog-adp@blank-6 | 0 | 9.746 | 8 | 153,661 (1.537) | yes | - |
| backlog-adp@blank-7 | 0 | 9.784 | 8 | 151,876 (1.519) | yes | - |
| backlog-adp@program-0 | 0 | 8.982 | 8 | 156,419 (1.564) | yes | - |
| backlog-adp@program-1 | 0 | 10.145 | 10 | 148,841 (1.488) | yes | - |
| backlog-adp@program-2 | 0 | 9.799 | 7 | 151,849 (1.518) | yes | - |
| backlog-adp@program-3 | 0 | 9.834 | 7 | 144,709 (1.447) | yes | - |
| backlog-adp@program-4 | 0 | 8.928 | 8 | 156,596 (1.566) | yes | - |
| backlog-adp@program-5 | 0 | 9.004 | 7 | 155,549 (1.555) | yes | - |
| backlog-adp@program-6 | 0 | 9.098 | 8 | 155,792 (1.558) | yes | - |
| backlog-adp@program-7 | 0 | 9.088 | 8 | 150,314 (1.503) | yes | - |
| backlog-adp@verify-0 | 0 | 9.591 | 8 | 154,080 (1.541) | yes | - |
| backlog-adp@verify-1 | 0 | 9.834 | 9 | 153,935 (1.539) | yes | - |
| backlog-adp@verify-2 | 0 | 9.759 | 8 | 153,109 (1.531) | yes | - |
| backlog-adp@verify-3 | 0 | 9.830 | 8 | 154,054 (1.541) | yes | - |
| backlog-adp@verify-4 | 0 | 9.886 | 8 | 152,297 (1.523) | yes | - |
| backlog-adp@verify-5 | 0 | 10.108 | 10 | 150,202 (1.502) | yes | - |
| backlog-adp@verify-6 | 0 | 9.686 | 8 | 156,078 (1.561) | yes | - |
| backlog-adp@verify-7 | 0 | 9.804 | 8 | 148,726 (1.487) | yes | - |
| backlog-adp@blank-aged2-0 | 1 | 10.953 | 10 | 156,766 (1.568) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 10.038 | 10 | 149,679 (1.497) | yes | - |
| backlog-adp@blank-aged2-2 | 1 | 9.801 | 8 | 146,362 (1.464) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 9.807 | 8 | 153,857 (1.539) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 9.812 | 8 | 151,619 (1.516) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 9.712 | 8 | 154,895 (1.549) | yes | - |
| backlog-adp@blank-aged2-6 | 1 | 9.656 | 7 | 156,415 (1.564) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 9.789 | 7 | 152,115 (1.521) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 11.407 | 9 | 156,654 (1.567) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 10.657 | 10 | 156,048 (1.560) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 10.906 | 11 | 150,771 (1.508) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 10.755 | 11 | 151,791 (1.518) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 10.599 | 9 | 150,110 (1.501) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 10.467 | 9 | 153,243 (1.532) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 10.431 | 9 | 152,979 (1.530) | yes | - |
| backlog-adp@blank-aged1-7 | 1 | 10.405 | 7 | 155,893 (1.559) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 10.073 | 9 | 156,765 (1.568) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 9.706 | 8 | 146,735 (1.467) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 9.654 | 7 | 155,910 (1.559) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 9.845 | 7 | 149,083 (1.491) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 9.897 | 8 | 153,916 (1.539) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 9.800 | 8 | 151,476 (1.515) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 10.001 | 10 | 150,096 (1.501) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 9.815 | 8 | 148,023 (1.480) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 9.980 | 9 | 150,907 (1.509) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.116 | 10 | 147,400 (1.474) | yes | - |
| backlog-adp@program-aged1-2 | 1 | 9.841 | 8 | 155,873 (1.559) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 9.809 | 8 | 156,212 (1.562) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 9.869 | 8 | 155,852 (1.559) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 9.745 | 8 | 151,612 (1.516) | yes | - |
| backlog-adp@program-aged1-6 | 1 | 9.709 | 7 | 146,835 (1.468) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 9.752 | 7 | 149,208 (1.492) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 10.676 | 9 | 156,574 (1.566) | yes | - |
| backlog-adp@verify-aged2-1 | 1 | 9.709 | 8 | 156,137 (1.561) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 9.679 | 7 | 146,746 (1.467) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 9.872 | 8 | 151,479 (1.515) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 9.976 | 10 | 150,049 (1.500) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 9.955 | 10 | 152,986 (1.530) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 9.771 | 8 | 151,608 (1.516) | yes | - |
| backlog-adp@verify-aged2-7 | 1 | 9.767 | 7 | 146,597 (1.466) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 10.729 | 9 | 148,102 (1.481) | yes | - |
| backlog-adp@verify-aged1-1 | 1 | 9.747 | 8 | 156,617 (1.566) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 9.775 | 7 | 154,504 (1.545) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 9.830 | 8 | 152,279 (1.523) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 9.894 | 8 | 151,622 (1.516) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 9.774 | 8 | 156,476 (1.565) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 10.031 | 10 | 156,647 (1.566) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 9.873 | 9 | 151,419 (1.514) | yes | - |
| backlog | 0 | 6.328 | 8 | 160,618 (1.606) | yes | - |
| backlog-adp | 0 | 9.045 | 8 | 149,907 (1.499) | yes | - |
| backlog-adp-refill | 0 | 40.576 | 22 | 153,063 (1.531) | yes | - |
| backlog-owed | 0 | 360.314 | 50 | 153,927 (1.539) | yes | - |
| fixture | 0 | 1.109 | 2 | 79,044 (0.790) | yes | - |

Composed maximum over the 4 backlog windows: 160,618 CPU cycles (1.606 ms), backlog.
Over the windows that released their whole load only: 160,618 (1.606 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3597 | 0 | 63,046 (0.630) | fits |
| save-second | 74342 | 0 | 63,046 (0.630) | fits |
| backlog-adp@blank-0 | 409 | 0 | 155,635 (1.556) | fits |
| backlog-adp@blank-1 | 410 | 0 | 155,685 (1.557) | fits |
| backlog-adp@blank-2 | 409 | 0 | 152,156 (1.522) | fits |
| backlog-adp@blank-3 | 409 | 0 | 156,160 (1.562) | fits |
| backlog-adp@blank-4 | 409 | 0 | 152,267 (1.523) | fits |
| backlog-adp@blank-5 | 411 | 0 | 151,049 (1.510) | fits |
| backlog-adp@blank-6 | 411 | 0 | 153,661 (1.537) | fits |
| backlog-adp@blank-7 | 411 | 0 | 151,876 (1.519) | fits |
| backlog-adp@program-0 | 511 | 0 | 156,419 (1.564) | fits |
| backlog-adp@program-1 | 513 | 0 | 148,841 (1.488) | fits |
| backlog-adp@program-2 | 513 | 0 | 153,385 (1.534) | fits |
| backlog-adp@program-3 | 513 | 0 | 151,926 (1.519) | fits |
| backlog-adp@program-4 | 514 | 0 | 156,596 (1.566) | fits |
| backlog-adp@program-5 | 516 | 0 | 155,549 (1.555) | fits |
| backlog-adp@program-6 | 516 | 0 | 155,792 (1.558) | fits |
| backlog-adp@program-7 | 516 | 0 | 150,314 (1.503) | fits |
| backlog-adp@verify-0 | 606 | 0 | 154,080 (1.541) | fits |
| backlog-adp@verify-1 | 607 | 0 | 153,935 (1.539) | fits |
| backlog-adp@verify-2 | 606 | 0 | 153,109 (1.531) | fits |
| backlog-adp@verify-3 | 606 | 0 | 154,054 (1.541) | fits |
| backlog-adp@verify-4 | 606 | 0 | 152,297 (1.523) | fits |
| backlog-adp@verify-5 | 608 | 0 | 150,202 (1.502) | fits |
| backlog-adp@verify-6 | 608 | 0 | 156,078 (1.561) | fits |
| backlog-adp@verify-7 | 608 | 0 | 148,726 (1.487) | fits |
| backlog-adp@blank-aged2-0 | 883 | 0 | 156,766 (1.568) | fits |
| backlog-adp@blank-aged2-1 | 892 | 0 | 149,679 (1.497) | fits |
| backlog-adp@blank-aged2-2 | 903 | 0 | 151,837 (1.518) | fits |
| backlog-adp@blank-aged2-3 | 914 | 0 | 153,857 (1.539) | fits |
| backlog-adp@blank-aged2-4 | 926 | 0 | 151,619 (1.516) | fits |
| backlog-adp@blank-aged2-5 | 938 | 0 | 154,895 (1.549) | fits |
| backlog-adp@blank-aged2-6 | 950 | 0 | 156,415 (1.564) | fits |
| backlog-adp@blank-aged2-7 | 962 | 0 | 153,922 (1.539) | fits |
| backlog-adp@blank-aged1-0 | 789 | 0 | 156,654 (1.567) | fits |
| backlog-adp@blank-aged1-1 | 802 | 0 | 156,048 (1.560) | fits |
| backlog-adp@blank-aged1-2 | 815 | 0 | 150,771 (1.508) | fits |
| backlog-adp@blank-aged1-3 | 827 | 0 | 151,791 (1.518) | fits |
| backlog-adp@blank-aged1-4 | 837 | 0 | 150,110 (1.501) | fits |
| backlog-adp@blank-aged1-5 | 849 | 0 | 153,243 (1.532) | fits |
| backlog-adp@blank-aged1-6 | 861 | 0 | 152,979 (1.530) | fits |
| backlog-adp@blank-aged1-7 | 872 | 0 | 155,893 (1.559) | fits |
| backlog-adp@program-aged2-0 | 982 | 0 | 156,765 (1.568) | fits |
| backlog-adp@program-aged2-1 | 993 | 0 | 151,476 (1.515) | fits |
| backlog-adp@program-aged2-2 | 1004 | 0 | 155,910 (1.559) | fits |
| backlog-adp@program-aged2-3 | 1016 | 0 | 154,024 (1.540) | fits |
| backlog-adp@program-aged2-4 | 1029 | 0 | 153,916 (1.539) | fits |
| backlog-adp@program-aged2-5 | 1041 | 0 | 151,476 (1.515) | fits |
| backlog-adp@program-aged2-6 | 1055 | 0 | 150,096 (1.501) | fits |
| backlog-adp@program-aged2-7 | 1065 | 0 | 148,023 (1.480) | fits |
| backlog-adp@program-aged1-0 | 884 | 0 | 150,907 (1.509) | fits |
| backlog-adp@program-aged1-1 | 898 | 0 | 151,662 (1.517) | fits |
| backlog-adp@program-aged1-2 | 909 | 0 | 155,873 (1.559) | fits |
| backlog-adp@program-aged1-3 | 920 | 0 | 156,212 (1.562) | fits |
| backlog-adp@program-aged1-4 | 932 | 0 | 155,852 (1.559) | fits |
| backlog-adp@program-aged1-5 | 944 | 0 | 151,612 (1.516) | fits |
| backlog-adp@program-aged1-6 | 956 | 0 | 151,506 (1.515) | fits |
| backlog-adp@program-aged1-7 | 968 | 0 | 149,208 (1.492) | fits |
| backlog-adp@verify-aged2-0 | 1074 | 0 | 156,574 (1.566) | fits |
| backlog-adp@verify-aged2-1 | 1086 | 0 | 156,137 (1.561) | fits |
| backlog-adp@verify-aged2-2 | 1097 | 0 | 149,928 (1.499) | fits |
| backlog-adp@verify-aged2-3 | 1110 | 0 | 151,479 (1.515) | fits |
| backlog-adp@verify-aged2-4 | 1124 | 0 | 150,049 (1.500) | fits |
| backlog-adp@verify-aged2-5 | 1136 | 0 | 152,986 (1.530) | fits |
| backlog-adp@verify-aged2-6 | 1146 | 0 | 151,608 (1.516) | fits |
| backlog-adp@verify-aged2-7 | 1158 | 0 | 150,055 (1.501) | fits |
| backlog-adp@verify-aged1-0 | 978 | 0 | 148,412 (1.484) | fits |
| backlog-adp@verify-aged1-1 | 989 | 0 | 156,617 (1.566) | fits |
| backlog-adp@verify-aged1-2 | 1000 | 0 | 154,504 (1.545) | fits |
| backlog-adp@verify-aged1-3 | 1013 | 0 | 152,279 (1.523) | fits |
| backlog-adp@verify-aged1-4 | 1025 | 0 | 151,622 (1.516) | fits |
| backlog-adp@verify-aged1-5 | 1037 | 0 | 156,476 (1.565) | fits |
| backlog-adp@verify-aged1-6 | 1051 | 0 | 156,647 (1.566) | fits |
| backlog-adp@verify-aged1-7 | 1062 | 0 | 151,419 (1.514) | fits |
| adp-advertise | 592 | 0 | 63,046 (0.630) | fits |
| save-held | 1279 | 0 | 154,676 (1.547) | fits |
| save-starved | 39678 | 0 | 154,676 (1.547) | fits |
| acmp-noresp | 2019 | 0 | 63,046 (0.630) | fits |
| save | 603 | 0 | 63,046 (0.630) | fits |
| srp | 285 | 0 | 86,175 (0.862) | fits |
| backlog | 283 | 0 | 160,618 (1.606) | fits |
| backlog-adp | 308 | 0 | 149,907 (1.499) | fits |
| backlog-adp-refill | 322 | 0 | 153,063 (1.531) | fits |
| backlog-owed | 332 | 0 | 153,927 (1.539) | fits |
| acmp-disc | 931 | 0 | 63,046 (0.630) | fits |
| maap | 176 | 0 | 63,046 (0.630) | fits |
| adp-link | 88 | 0 | 63,046 (0.630) | fits |
| adp-gm | 87 | 0 | 63,046 (0.630) | fits |
| adp-discover | 87 | 0 | 63,046 (0.630) | fits |
| control | 87 | 0 | 63,046 (0.630) | fits |
| aecp-fanout | 110 | 0 | 63,046 (0.630) | fits |
| acmp-cmd | 83 | 0 | 63,046 (0.630) | fits |
| aecp | 110 | 0 | 63,046 (0.630) | fits |
| fixture | 149 | 0 | 79,044 (0.790) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 8.576 (20) | 11.424 |
| backlog-adp@blank-aged2-1 | 2 | none | +8.747 ms, 76,606 (0.766 ms), read-back | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 8.591 (20) | 11.409 |
| backlog-adp@blank-aged2-2 | 2 | none | none | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 8.507 (20) | 11.493 |
| backlog-adp@blank-aged2-3 | 2 | none | none | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 9.479 (20) | 10.521 |
| backlog-adp@blank-aged2-4 | 2 | none | none | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 9.486 (20) | 10.514 |
| backlog-adp@blank-aged2-5 | 2 | none | none | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 9.387 (20) | 10.613 |
| backlog-adp@blank-aged2-6 | 2 | +4.386 ms, 77,185 (0.772 ms), read-back | none | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 9.331 (20) | 10.669 |
| backlog-adp@blank-aged2-7 | 2 | +4.597 ms, 77,156 (0.772 ms), read-back | none | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 9.458 (20) | 10.542 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 8.545 (20) | 11.455 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 8.656 (20) | 11.344 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 8.819 (20) | 11.181 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 9.453 (20) | 10.547 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 9.511 (20) | 10.489 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 9.379 (20) | 10.621 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 9.348 (20) | 10.652 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 9.317 (20) | 10.683 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 8.547 (20) | 11.453 |
| backlog-adp@program-aged2-1 | 2 | none | +8.684 ms, 79,924 (0.799 ms), issue | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 8.533 (20) | 11.467 |
| backlog-adp@program-aged2-2 | 2 | none | +8.623 ms, 80,081 (0.801 ms), issue | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 8.611 (20) | 11.389 |
| backlog-adp@program-aged2-3 | 2 | +7.766 ms, 80,336 (0.803 ms), issue | none | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 9.514 (20) | 10.486 |
| backlog-adp@program-aged2-4 | 2 | +6.398 ms, 80,341 (0.803 ms), issue | none | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 9.566 (20) | 10.434 |
| backlog-adp@program-aged2-5 | 2 | +4.952 ms, 80,137 (0.801 ms), issue | none | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 9.475 (20) | 10.525 |
| backlog-adp@program-aged2-6 | 2 | +4.401 ms, 80,280 (0.803 ms), issue | none | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 9.460 (20) | 10.540 |
| backlog-adp@program-aged2-7 | 2 | +2.959 ms, 80,198 (0.802 ms), issue | none | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 9.487 (20) | 10.513 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 8.574 (20) | 11.426 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 8.540 (20) | 11.460 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 8.506 (20) | 11.494 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 8.685 (20) | 11.315 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 8.743 (20) | 11.257 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 8.613 (20) | 11.387 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 8.583 (20) | 11.417 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 8.622 (20) | 11.378 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 8.587 (20) | 11.413 |
| backlog-adp@verify-aged2-1 | 2 | none | +8.721 ms, 77,267 (0.773 ms), read-back | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 8.573 (20) | 11.427 |
| backlog-adp@verify-aged2-2 | 2 | none | +8.682 ms, 77,572 (0.776 ms), read-back | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 8.670 (20) | 11.330 |
| backlog-adp@verify-aged2-3 | 2 | +7.845 ms, 77,688 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 9.548 (20) | 10.452 |
| backlog-adp@verify-aged2-4 | 2 | +6.264 ms, 77,430 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 9.437 (20) | 10.563 |
| backlog-adp@verify-aged2-5 | 2 | +5.394 ms, 77,506 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 9.418 (20) | 10.582 |
| backlog-adp@verify-aged2-6 | 2 | +4.012 ms, 77,506 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 9.447 (20) | 10.553 |
| backlog-adp@verify-aged2-7 | 2 | +4.247 ms, 77,573 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 9.438 (20) | 10.562 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 8.510 (20) | 11.490 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 8.524 (20) | 11.476 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 8.683 (20) | 11.317 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 8.734 (20) | 11.266 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 8.801 (20) | 11.199 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 8.675 (20) | 11.325 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 8.613 (20) | 11.387 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 8.564 (20) | 11.436 |

Least margin over the aged windows: 10.434 ms, `backlog-adp@program-aged2-4.service.aecp.last.if0` at 9.566 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6029.789 | 6,070 | 102 | 2 | 30.824 | yes | within |
| save-held | 2018.114 | 4,070 | 102 | - | 12.642 | no | within |
| save-starved | 4048.077 | 4,070 | 102 | - | 31.754 | yes | within |
| save | 2018.426 | 4,070 | 102 | - | 10.807 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 91,986 (0.920) | 78,253 (0.783) |
| save-second | 520 | 80,594 (0.806) | 78,008 (0.780) |
| backlog-adp@blank-0 | 298 | 84,794 (0.848) | 75,534 (0.755) |
| backlog-adp@blank-1 | 299 | 86,025 (0.860) | 76,161 (0.762) |
| backlog-adp@blank-2 | 299 | 86,473 (0.865) | 76,161 (0.762) |
| backlog-adp@blank-3 | 299 | 86,717 (0.867) | 76,164 (0.762) |
| backlog-adp@blank-4 | 299 | 86,803 (0.868) | 76,226 (0.762) |
| backlog-adp@blank-5 | 299 | 87,023 (0.870) | 76,226 (0.762) |
| backlog-adp@blank-6 | 299 | 86,489 (0.865) | 76,189 (0.762) |
| backlog-adp@blank-7 | 299 | 87,025 (0.870) | 76,194 (0.762) |
| backlog-adp@program-0 | 327 | 91,450 (0.914) | 78,179 (0.782) |
| backlog-adp@program-1 | 328 | 91,450 (0.914) | 78,716 (0.787) |
| backlog-adp@program-2 | 328 | 91,450 (0.914) | 78,778 (0.788) |
| backlog-adp@program-3 | 328 | 91,450 (0.914) | 78,778 (0.788) |
| backlog-adp@program-4 | 328 | 91,450 (0.914) | 78,179 (0.782) |
| backlog-adp@program-5 | 329 | 91,450 (0.914) | 78,179 (0.782) |
| backlog-adp@program-6 | 329 | 91,450 (0.914) | 78,179 (0.782) |
| backlog-adp@program-7 | 329 | 91,450 (0.914) | 78,179 (0.782) |
| backlog-adp@verify-0 | 354 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-1 | 355 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-2 | 355 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-3 | 355 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-4 | 355 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-5 | 355 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-6 | 355 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-7 | 355 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@blank-aged2-0 | 298 | 86,837 (0.868) | 76,260 (0.763) |
| backlog-adp@blank-aged2-1 | 297 | 76,606 (0.766) | 75,986 (0.760) |
| backlog-adp@blank-aged2-2 | 297 | 85,100 (0.851) | 76,372 (0.764) |
| backlog-adp@blank-aged2-3 | 297 | 85,692 (0.857) | 76,420 (0.764) |
| backlog-adp@blank-aged2-4 | 297 | 85,566 (0.856) | 76,420 (0.764) |
| backlog-adp@blank-aged2-5 | 297 | 85,788 (0.858) | 76,524 (0.765) |
| backlog-adp@blank-aged2-6 | 297 | 77,185 (0.772) | 76,282 (0.763) |
| backlog-adp@blank-aged2-7 | 297 | 77,156 (0.772) | 76,034 (0.760) |
| backlog-adp@blank-aged1-0 | 298 | 91,314 (0.913) | 76,253 (0.763) |
| backlog-adp@blank-aged1-1 | 297 | 91,855 (0.919) | 76,542 (0.765) |
| backlog-adp@blank-aged1-2 | 297 | 92,073 (0.921) | 76,545 (0.765) |
| backlog-adp@blank-aged1-3 | 297 | 85,858 (0.859) | 76,325 (0.763) |
| backlog-adp@blank-aged1-4 | 297 | 87,056 (0.871) | 76,260 (0.763) |
| backlog-adp@blank-aged1-5 | 297 | 87,104 (0.871) | 76,260 (0.763) |
| backlog-adp@blank-aged1-6 | 297 | 86,717 (0.867) | 76,260 (0.763) |
| backlog-adp@blank-aged1-7 | 297 | 87,209 (0.872) | 76,260 (0.763) |
| backlog-adp@program-aged2-0 | 327 | 91,450 (0.914) | 78,778 (0.788) |
| backlog-adp@program-aged2-1 | 326 | 91,450 (0.914) | 78,496 (0.785) |
| backlog-adp@program-aged2-2 | 326 | 91,450 (0.914) | 78,499 (0.785) |
| backlog-adp@program-aged2-3 | 326 | 91,450 (0.914) | 78,606 (0.786) |
| backlog-adp@program-aged2-4 | 326 | 91,450 (0.914) | 78,609 (0.786) |
| backlog-adp@program-aged2-5 | 326 | 91,450 (0.914) | 78,777 (0.788) |
| backlog-adp@program-aged2-6 | 326 | 91,450 (0.914) | 78,856 (0.789) |
| backlog-adp@program-aged2-7 | 326 | 91,450 (0.914) | 78,467 (0.785) |
| backlog-adp@program-aged1-0 | 327 | 91,450 (0.914) | 78,778 (0.788) |
| backlog-adp@program-aged1-1 | 326 | 91,450 (0.914) | 78,713 (0.787) |
| backlog-adp@program-aged1-2 | 326 | 91,450 (0.914) | 78,716 (0.787) |
| backlog-adp@program-aged1-3 | 326 | 91,450 (0.914) | 78,778 (0.788) |
| backlog-adp@program-aged1-4 | 326 | 91,450 (0.914) | 78,778 (0.788) |
| backlog-adp@program-aged1-5 | 326 | 91,450 (0.914) | 78,778 (0.788) |
| backlog-adp@program-aged1-6 | 326 | 91,450 (0.914) | 78,778 (0.788) |
| backlog-adp@program-aged1-7 | 326 | 91,450 (0.914) | 78,778 (0.788) |
| backlog-adp@verify-aged2-0 | 356 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-aged2-1 | 355 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-aged2-2 | 355 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-aged2-3 | 355 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-aged2-4 | 355 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-aged2-5 | 355 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-aged2-6 | 355 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-aged2-7 | 355 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-aged1-0 | 356 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-aged1-1 | 355 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-aged1-2 | 355 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-aged1-3 | 355 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-aged1-4 | 355 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-aged1-5 | 355 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-aged1-6 | 355 | 91,450 (0.914) | 78,193 (0.782) |
| backlog-adp@verify-aged1-7 | 355 | 91,450 (0.914) | 78,193 (0.782) |
| adp-advertise | 578 | 17,566 (0.176) | 3,074 (0.031) |
| save-held | 722 | 90,832 (0.908) | 78,570 (0.786) |
| save-starved | 418 | 81,743 (0.817) | 78,767 (0.788) |
| acmp-noresp | 615 | 91,543 (0.915) | 78,193 (0.782) |
| save | 585 | 90,658 (0.907) | 78,054 (0.781) |
| srp | 271 | 17,566 (0.176) | 3,074 (0.031) |
| backlog | 265 | 17,566 (0.176) | 3,074 (0.031) |
| backlog-adp | 271 | 17,566 (0.176) | 3,074 (0.031) |
| backlog-adp-refill | 274 | 17,566 (0.176) | 3,074 (0.031) |
| backlog-owed | 306 | 17,590 (0.176) | 3,074 (0.031) |
| acmp-disc | 305 | 91,421 (0.914) | 78,193 (0.782) |
| maap | 166 | 17,566 (0.176) | 3,074 (0.031) |
| adp-link | 80 | 17,566 (0.176) | 3,059 (0.031) |
| adp-gm | 80 | 17,566 (0.176) | 3,059 (0.031) |
| adp-discover | 80 | 17,566 (0.176) | 3,059 (0.031) |
| control | 80 | 17,566 (0.176) | 3,059 (0.031) |
| aecp-fanout | 79 | 17,566 (0.176) | 3,059 (0.031) |
| acmp-cmd | 65 | 17,566 (0.176) | 3,059 (0.031) |
| aecp | 79 | 17,566 (0.176) | 3,059 (0.031) |
| fixture | 54 | 13,825 (0.138) | 2,913 (0.029) |

Longest pass that carries a step: 92,073 CPU cycles (0.921 ms), backlog-adp@blank-aged1-2; longest step: 78,856 (0.789 ms), backlog-adp@program-aged2-6.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 8,600 | 0.086 | 20 | 20 | fits | 29,240 | 19 (14) | 0.889 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 774,597 | 7.746 | 20 | 20 | fits | 145,603 | 114 | 0.550 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 221,654 | 2.217 | 20 | 200 | fits | 150,964 | 188 | 0.495 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 849,789 | 8.498 | 20 | 200 | fits | 145,603 | 114 | 0.550 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 222,566 | 2.226 | 20 | 20 | fits | 150,964 | 188 | 0.495 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 850,485 | 8.505 | 20 | 20 | fits | 145,603 | 114 | 0.550 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 226,151 | 2.262 | 20 | 24 | fits | 150,964 | 188 | 0.495 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 932,806 | 9.328 | 20 | 24 | fits | 78,886 | 66 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 225,111 | 2.251 | 20 | 50 | fits | 150,964 | 188 | 0.495 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 853,465 | 8.535 | 20 | 50 | fits | 145,603 | 114 | 0.550 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 358,082 | 3.581 | 20 | 20 | fits | 133,426 | 94 | 0.545 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 541,186 | 5.412 | 20 | 20 | fits | 76,687 | 36 | 0.421 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 700,135 | 7.001 | 20 | 20 | fits | 145,667 | 114 | 0.550 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 147,078 | 1.471 | 20 | 200 | fits | 150,891 | 188 | 0.495 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 775,327 | 7.753 | 20 | 200 | fits | 145,667 | 114 | 0.550 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 147,990 | 1.480 | 20 | 20 | fits | 150,891 | 188 | 0.495 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 776,023 | 7.760 | 20 | 20 | fits | 145,667 | 114 | 0.550 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 151,575 | 1.516 | 20 | 24 | fits | 150,891 | 188 | 0.495 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 858,344 | 8.583 | 20 | 24 | fits | 78,886 | 66 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 150,535 | 1.505 | 20 | 50 | fits | 150,891 | 188 | 0.495 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 779,003 | 7.790 | 20 | 50 | fits | 145,667 | 114 | 0.550 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 283,506 | 2.835 | 20 | 20 | fits | 133,426 | 94 | 0.545 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 466,610 | 4.666 | 20 | 20 | fits | 76,687 | 36 | 0.421 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 610,003 | 6.100 | 20 | 20 | fits | 147,479 | 171 | 0.524 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 153,850 | 1.538 | 20 | 200 | fits | 152,156 | 192 | 0.488 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 629,045 | 6.290 | 20 | 200 | fits | 147,479 | 171 | 0.524 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 154,762 | 1.548 | 20 | 20 | fits | 152,156 | 192 | 0.488 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 779,997 | 7.800 | 20 | 20 | fits | 150,256 | 93 | 0.482 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 158,347 | 1.583 | 20 | 24 | fits | 152,156 | 192 | 0.488 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 870,384 | 8.704 | 20 | 24 | fits | 86,952 | 75 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 157,307 | 1.573 | 20 | 50 | fits | 152,156 | 192 | 0.488 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 632,721 | 6.327 | 20 | 50 | fits | 147,479 | 171 | 0.524 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 290,278 | 2.903 | 20 | 20 | fits | 133,426 | 94 | 0.545 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 473,483 | 4.735 | 20 | 20 | fits | 76,788 | 37 | 0.424 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 686,051 | 6.861 | 20 | 20 | fits | 152,442 | 113 | 0.559 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 147,942 | 1.479 | 20 | 200 | fits | 150,780 | 188 | 0.494 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 789,118 | 7.891 | 20 | 200 | fits | 152,442 | 113 | 0.559 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 148,854 | 1.489 | 20 | 20 | fits | 150,780 | 188 | 0.494 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 789,814 | 7.898 | 20 | 20 | fits | 152,442 | 113 | 0.559 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 152,439 | 1.524 | 20 | 24 | fits | 150,780 | 188 | 0.494 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 871,991 | 8.720 | 20 | 24 | fits | 78,742 | 66 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 151,399 | 1.514 | 20 | 50 | fits | 150,780 | 188 | 0.494 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 792,794 | 7.928 | 20 | 50 | fits | 152,442 | 113 | 0.559 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 284,370 | 2.844 | 20 | 20 | fits | 133,426 | 94 | 0.545 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 482,112 | 4.821 | 20 | 20 | fits | 81,467 | 43 | 0.526 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 641,458 | 6.415 | 20 | 20 | fits | 147,418 | 94 | 0.506 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 154,936 | 1.549 | 20 | 200 | fits | 152,267 | 192 | 0.489 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 781,705 | 7.817 | 20 | 200 | fits | 147,418 | 94 | 0.506 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 155,848 | 1.558 | 20 | 20 | fits | 152,267 | 192 | 0.489 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 782,401 | 7.824 | 20 | 20 | fits | 147,418 | 94 | 0.506 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 159,433 | 1.594 | 20 | 24 | fits | 152,267 | 192 | 0.489 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 879,395 | 8.794 | 20 | 24 | fits | 93,559 | 79 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 158,393 | 1.584 | 20 | 50 | fits | 152,267 | 192 | 0.489 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 637,963 | 6.380 | 20 | 50 | fits | 146,532 | 159 | 0.538 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 291,460 | 2.915 | 20 | 20 | fits | 133,522 | 95 | 0.546 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 489,351 | 4.894 | 20 | 20 | fits | 76,986 | 36 | 0.433 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 692,588 | 6.926 | 20 | 20 | fits | 145,421 | 110 | 0.544 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 149,186 | 1.492 | 20 | 200 | fits | 151,049 | 189 | 0.495 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 767,355 | 7.674 | 20 | 200 | fits | 145,421 | 110 | 0.544 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 150,098 | 1.501 | 20 | 20 | fits | 151,049 | 189 | 0.495 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 863,273 | 8.633 | 20 | 20 | fits | 95,222 | 73 | 0.454 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 153,683 | 1.537 | 20 | 24 | fits | 151,049 | 189 | 0.495 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 866,708 | 8.667 | 20 | 24 | fits | 95,222 | 73 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 152,643 | 1.526 | 20 | 50 | fits | 151,049 | 189 | 0.495 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 771,031 | 7.710 | 20 | 50 | fits | 145,421 | 110 | 0.544 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 433,423 | 4.334 | 20 | 20 | fits | 124,868 | 52 | 0.566 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 623,530 | 6.235 | 20 | 20 | fits | 77,025 | 36 | 0.431 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 629,401 | 6.294 | 20 | 20 | fits | 147,521 | 97 | 0.501 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 144,553 | 1.446 | 20 | 200 | fits | 143,262 | 203 | 0.474 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 769,837 | 7.698 | 20 | 200 | fits | 147,521 | 97 | 0.501 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 145,465 | 1.455 | 20 | 20 | fits | 143,262 | 203 | 0.474 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 770,533 | 7.705 | 20 | 20 | fits | 147,521 | 97 | 0.501 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 149,050 | 1.490 | 20 | 24 | fits | 143,262 | 203 | 0.474 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 866,475 | 8.665 | 20 | 24 | fits | 83,202 | 73 | 0.451 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 148,010 | 1.480 | 20 | 50 | fits | 143,262 | 203 | 0.474 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 625,992 | 6.260 | 20 | 50 | fits | 153,661 | 152 | 0.490 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 280,529 | 2.805 | 20 | 20 | fits | 132,974 | 94 | 0.542 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 470,251 | 4.703 | 20 | 20 | fits | 76,803 | 36 | 0.424 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 619,596 | 6.196 | 20 | 20 | fits | 147,652 | 114 | 0.562 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 148,635 | 1.486 | 20 | 200 | fits | 151,876 | 192 | 0.487 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 757,049 | 7.570 | 20 | 200 | fits | 147,652 | 114 | 0.562 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 149,547 | 1.495 | 20 | 20 | fits | 151,876 | 192 | 0.487 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 866,280 | 8.663 | 20 | 20 | fits | 108,535 | 86 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 153,132 | 1.531 | 20 | 24 | fits | 151,876 | 192 | 0.487 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 869,715 | 8.697 | 20 | 24 | fits | 108,535 | 86 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 152,092 | 1.521 | 20 | 50 | fits | 151,876 | 192 | 0.487 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 760,725 | 7.607 | 20 | 50 | fits | 147,652 | 114 | 0.562 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 418,343 | 4.183 | 20 | 20 | fits | 124,685 | 52 | 0.562 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 601,311 | 6.013 | 20 | 20 | fits | 76,714 | 37 | 0.422 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 677,488 | 6.775 | 20 | 20 | fits | 156,419 | 121 | 0.498 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 150,590 | 1.506 | 20 | 200 | fits | 148,833 | 190 | 0.486 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 793,203 | 7.932 | 20 | 200 | fits | 156,419 | 121 | 0.498 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 151,502 | 1.515 | 20 | 20 | fits | 148,833 | 190 | 0.486 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 861,710 | 8.617 | 20 | 20 | fits | 67,811 | 49 | 0.531 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 155,087 | 1.551 | 20 | 24 | fits | 148,833 | 190 | 0.486 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 865,145 | 8.651 | 20 | 24 | fits | 67,811 | 49 | 0.531 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 154,047 | 1.540 | 20 | 50 | fits | 148,833 | 190 | 0.486 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 796,879 | 7.969 | 20 | 50 | fits | 156,419 | 121 | 0.498 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 286,638 | 2.866 | 20 | 20 | fits | 133,046 | 94 | 0.542 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 473,686 | 4.737 | 20 | 20 | fits | 80,631 | 43 | 0.471 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 645,579 | 6.456 | 20 | 20 | fits | 148,236 | 95 | 0.514 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 151,573 | 1.516 | 20 | 200 | fits | 148,841 | 191 | 0.485 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 760,411 | 7.604 | 20 | 200 | fits | 148,236 | 95 | 0.514 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 152,485 | 1.525 | 20 | 20 | fits | 148,841 | 191 | 0.485 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 866,167 | 8.662 | 20 | 20 | fits | 105,060 | 76 | 0.523 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 156,070 | 1.561 | 20 | 24 | fits | 148,841 | 191 | 0.485 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 869,602 | 8.696 | 20 | 24 | fits | 105,060 | 76 | 0.523 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 155,030 | 1.550 | 20 | 50 | fits | 148,841 | 191 | 0.485 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 305,986 | 3.060 | 20 | 50 | fits | 142,649 | 204 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 430,501 | 4.305 | 20 | 20 | fits | 124,580 | 52 | 0.564 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 613,771 | 6.138 | 20 | 20 | fits | 76,835 | 36 | 0.426 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 626,932 | 6.269 | 20 | 20 | fits | 151,849 | 99 | 0.522 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 147,498 | 1.475 | 20 | 200 | fits | 153,385 | 168 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 770,733 | 7.707 | 20 | 200 | fits | 151,849 | 99 | 0.522 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 148,410 | 1.484 | 20 | 20 | fits | 153,385 | 168 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 771,429 | 7.714 | 20 | 20 | fits | 151,849 | 99 | 0.522 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 151,995 | 1.520 | 20 | 24 | fits | 153,385 | 168 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 867,432 | 8.674 | 20 | 24 | fits | 83,209 | 73 | 0.449 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 150,955 | 1.510 | 20 | 50 | fits | 153,385 | 168 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 298,036 | 2.980 | 20 | 50 | fits | 147,471 | 185 | 0.483 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 430,720 | 4.307 | 20 | 20 | fits | 132,749 | 94 | 0.539 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 620,480 | 6.205 | 20 | 20 | fits | 76,803 | 36 | 0.424 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 619,176 | 6.192 | 20 | 20 | fits | 144,709 | 107 | 0.551 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 147,014 | 1.470 | 20 | 200 | fits | 151,926 | 192 | 0.489 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 756,903 | 7.569 | 20 | 200 | fits | 144,709 | 107 | 0.551 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 147,926 | 1.479 | 20 | 20 | fits | 151,926 | 192 | 0.489 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 866,910 | 8.669 | 20 | 20 | fits | 109,311 | 86 | 0.442 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 151,511 | 1.515 | 20 | 24 | fits | 151,926 | 192 | 0.489 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 870,345 | 8.703 | 20 | 24 | fits | 109,311 | 86 | 0.442 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 150,471 | 1.505 | 20 | 50 | fits | 151,926 | 192 | 0.489 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 760,579 | 7.606 | 20 | 50 | fits | 144,709 | 107 | 0.551 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 416,380 | 4.164 | 20 | 20 | fits | 124,476 | 52 | 0.560 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 613,790 | 6.138 | 20 | 20 | fits | 81,325 | 43 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 672,118 | 6.721 | 20 | 20 | fits | 156,596 | 121 | 0.499 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 144,386 | 1.444 | 20 | 200 | fits | 148,493 | 190 | 0.482 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 787,799 | 7.878 | 20 | 200 | fits | 156,596 | 121 | 0.499 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 145,298 | 1.453 | 20 | 20 | fits | 148,493 | 190 | 0.482 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 856,304 | 8.563 | 20 | 20 | fits | 67,809 | 49 | 0.531 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 148,883 | 1.489 | 20 | 24 | fits | 148,493 | 190 | 0.482 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 859,739 | 8.597 | 20 | 24 | fits | 67,809 | 49 | 0.531 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 147,843 | 1.478 | 20 | 50 | fits | 148,493 | 190 | 0.482 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 791,475 | 7.915 | 20 | 50 | fits | 156,596 | 121 | 0.499 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 280,580 | 2.806 | 20 | 20 | fits | 133,192 | 95 | 0.543 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 478,072 | 4.781 | 20 | 20 | fits | 76,986 | 36 | 0.433 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 685,453 | 6.855 | 20 | 20 | fits | 141,886 | 111 | 0.528 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 145,455 | 1.455 | 20 | 200 | fits | 150,314 | 188 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 760,540 | 7.605 | 20 | 200 | fits | 141,886 | 111 | 0.528 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 146,367 | 1.464 | 20 | 20 | fits | 150,314 | 188 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 761,236 | 7.612 | 20 | 20 | fits | 141,886 | 111 | 0.528 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 149,952 | 1.500 | 20 | 24 | fits | 150,314 | 188 | 0.493 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 862,830 | 8.628 | 20 | 24 | fits | 89,298 | 82 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 148,912 | 1.489 | 20 | 50 | fits | 150,314 | 188 | 0.493 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 764,216 | 7.642 | 20 | 50 | fits | 141,886 | 111 | 0.528 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 281,597 | 2.816 | 20 | 20 | fits | 133,140 | 94 | 0.546 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 464,701 | 4.647 | 20 | 20 | fits | 76,687 | 36 | 0.421 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 700,184 | 7.002 | 20 | 20 | fits | 145,218 | 113 | 0.550 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 146,443 | 1.464 | 20 | 200 | fits | 150,327 | 188 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 775,101 | 7.751 | 20 | 200 | fits | 145,218 | 113 | 0.550 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 147,355 | 1.474 | 20 | 20 | fits | 150,327 | 188 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 775,797 | 7.758 | 20 | 20 | fits | 145,218 | 113 | 0.550 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 150,940 | 1.509 | 20 | 24 | fits | 150,327 | 188 | 0.493 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 872,088 | 8.721 | 20 | 24 | fits | 92,856 | 79 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 149,900 | 1.499 | 20 | 50 | fits | 150,327 | 188 | 0.493 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 778,777 | 7.788 | 20 | 50 | fits | 145,218 | 113 | 0.550 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 282,585 | 2.826 | 20 | 20 | fits | 133,140 | 94 | 0.546 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 465,689 | 4.657 | 20 | 20 | fits | 76,687 | 36 | 0.421 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 682,614 | 6.826 | 20 | 20 | fits | 145,948 | 109 | 0.549 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 147,405 | 1.474 | 20 | 200 | fits | 150,314 | 188 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 757,525 | 7.575 | 20 | 200 | fits | 145,948 | 109 | 0.549 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 148,317 | 1.483 | 20 | 20 | fits | 150,314 | 188 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 867,223 | 8.672 | 20 | 20 | fits | 109,002 | 86 | 0.431 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 151,902 | 1.519 | 20 | 24 | fits | 150,314 | 188 | 0.493 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 870,658 | 8.707 | 20 | 24 | fits | 109,002 | 86 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 150,862 | 1.509 | 20 | 50 | fits | 150,314 | 188 | 0.493 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 761,201 | 7.612 | 20 | 50 | fits | 145,948 | 109 | 0.549 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 429,967 | 4.300 | 20 | 20 | fits | 127,294 | 58 | 0.584 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 613,173 | 6.132 | 20 | 20 | fits | 76,712 | 36 | 0.421 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 738,904 | 7.389 | 20 | 20 | fits | 145,684 | 119 | 0.533 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 214,396 | 2.144 | 20 | 200 | fits | 149,069 | 190 | 0.486 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 840,825 | 8.408 | 20 | 200 | fits | 145,684 | 119 | 0.533 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 215,308 | 2.153 | 20 | 20 | fits | 149,069 | 190 | 0.486 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 922,689 | 9.227 | 20 | 20 | fits | 81,168 | 61 | 0.483 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 218,893 | 2.189 | 20 | 24 | fits | 149,069 | 190 | 0.486 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 926,124 | 9.261 | 20 | 24 | fits | 81,168 | 61 | 0.483 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 217,853 | 2.179 | 20 | 50 | fits | 149,069 | 190 | 0.486 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 844,501 | 8.445 | 20 | 50 | fits | 145,684 | 119 | 0.533 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 350,592 | 3.506 | 20 | 20 | fits | 133,194 | 94 | 0.542 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 533,696 | 5.337 | 20 | 20 | fits | 76,687 | 36 | 0.421 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 635,944 | 6.359 | 20 | 20 | fits | 150,887 | 103 | 0.517 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 144,701 | 1.447 | 20 | 200 | fits | 143,516 | 203 | 0.477 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 776,977 | 7.770 | 20 | 200 | fits | 150,887 | 103 | 0.517 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 145,613 | 1.456 | 20 | 20 | fits | 143,516 | 203 | 0.477 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 777,673 | 7.777 | 20 | 20 | fits | 150,887 | 103 | 0.517 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 149,198 | 1.492 | 20 | 24 | fits | 143,516 | 203 | 0.477 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 860,844 | 8.608 | 20 | 24 | fits | 79,736 | 66 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 148,158 | 1.482 | 20 | 50 | fits | 143,516 | 203 | 0.477 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 619,958 | 6.200 | 20 | 50 | fits | 153,935 | 153 | 0.491 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 280,877 | 2.809 | 20 | 20 | fits | 133,174 | 94 | 0.542 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 463,943 | 4.639 | 20 | 20 | fits | 76,687 | 36 | 0.421 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 597,672 | 5.977 | 20 | 20 | fits | 153,109 | 156 | 0.531 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 148,963 | 1.490 | 20 | 200 | fits | 152,310 | 192 | 0.491 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 629,790 | 6.298 | 20 | 200 | fits | 153,109 | 156 | 0.531 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 149,875 | 1.499 | 20 | 20 | fits | 152,310 | 192 | 0.491 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 776,490 | 7.765 | 20 | 20 | fits | 146,004 | 109 | 0.495 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 153,460 | 1.535 | 20 | 24 | fits | 152,310 | 192 | 0.491 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 866,709 | 8.667 | 20 | 24 | fits | 86,784 | 75 | 0.423 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 152,420 | 1.524 | 20 | 50 | fits | 152,310 | 192 | 0.491 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 779,470 | 7.795 | 20 | 50 | fits | 146,004 | 109 | 0.495 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 285,393 | 2.854 | 20 | 20 | fits | 133,428 | 94 | 0.546 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 468,598 | 4.686 | 20 | 20 | fits | 76,788 | 37 | 0.424 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 643,181 | 6.432 | 20 | 20 | fits | 142,695 | 94 | 0.544 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 145,630 | 1.456 | 20 | 200 | fits | 143,470 | 203 | 0.477 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 774,291 | 7.743 | 20 | 200 | fits | 142,695 | 94 | 0.544 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 146,542 | 1.465 | 20 | 20 | fits | 143,470 | 203 | 0.477 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 869,952 | 8.700 | 20 | 20 | fits | 94,965 | 73 | 0.458 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 150,127 | 1.501 | 20 | 24 | fits | 143,470 | 203 | 0.477 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 873,387 | 8.734 | 20 | 24 | fits | 94,965 | 73 | 0.458 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 149,087 | 1.491 | 20 | 50 | fits | 143,470 | 203 | 0.477 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 635,272 | 6.353 | 20 | 50 | fits | 154,054 | 152 | 0.492 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 281,806 | 2.818 | 20 | 20 | fits | 133,174 | 94 | 0.542 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 479,138 | 4.791 | 20 | 20 | fits | 81,316 | 43 | 0.523 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 614,216 | 6.142 | 20 | 20 | fits | 150,749 | 148 | 0.566 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 149,925 | 1.499 | 20 | 200 | fits | 152,297 | 192 | 0.491 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 633,574 | 6.336 | 20 | 200 | fits | 150,749 | 148 | 0.566 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 150,837 | 1.508 | 20 | 20 | fits | 152,297 | 192 | 0.491 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 782,575 | 7.826 | 20 | 20 | fits | 148,305 | 105 | 0.514 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 154,422 | 1.544 | 20 | 24 | fits | 152,297 | 192 | 0.491 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 879,189 | 8.792 | 20 | 24 | fits | 93,179 | 79 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 153,382 | 1.534 | 20 | 50 | fits | 152,297 | 192 | 0.491 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 785,555 | 7.856 | 20 | 50 | fits | 148,305 | 105 | 0.514 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 286,451 | 2.865 | 20 | 20 | fits | 133,524 | 95 | 0.546 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 484,421 | 4.844 | 20 | 20 | fits | 76,986 | 36 | 0.433 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 629,000 | 6.290 | 20 | 20 | fits | 149,447 | 95 | 0.519 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 146,805 | 1.468 | 20 | 200 | fits | 143,670 | 204 | 0.477 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 771,479 | 7.715 | 20 | 200 | fits | 149,447 | 95 | 0.519 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 147,717 | 1.477 | 20 | 20 | fits | 143,670 | 204 | 0.477 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 772,175 | 7.722 | 20 | 20 | fits | 149,447 | 95 | 0.519 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 151,302 | 1.513 | 20 | 24 | fits | 143,670 | 204 | 0.477 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 868,977 | 8.690 | 20 | 24 | fits | 93,367 | 79 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 150,262 | 1.503 | 20 | 50 | fits | 143,670 | 204 | 0.477 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 308,868 | 3.089 | 20 | 50 | fits | 150,202 | 189 | 0.486 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 433,483 | 4.335 | 20 | 20 | fits | 124,680 | 52 | 0.565 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 623,628 | 6.236 | 20 | 20 | fits | 77,025 | 36 | 0.431 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 597,420 | 5.974 | 20 | 20 | fits | 156,078 | 171 | 0.499 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 148,158 | 1.482 | 20 | 200 | fits | 152,030 | 192 | 0.490 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 628,583 | 6.286 | 20 | 200 | fits | 156,078 | 171 | 0.499 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 149,070 | 1.491 | 20 | 20 | fits | 152,030 | 192 | 0.490 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 778,660 | 7.787 | 20 | 20 | fits | 149,381 | 100 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 152,655 | 1.527 | 20 | 24 | fits | 152,030 | 192 | 0.490 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 859,533 | 8.595 | 20 | 24 | fits | 68,568 | 61 | 0.470 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 151,615 | 1.516 | 20 | 50 | fits | 152,030 | 192 | 0.490 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 632,259 | 6.323 | 20 | 50 | fits | 156,078 | 171 | 0.499 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 284,341 | 2.843 | 20 | 20 | fits | 133,181 | 94 | 0.545 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 474,101 | 4.741 | 20 | 20 | fits | 76,803 | 36 | 0.424 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 657,054 | 6.571 | 20 | 20 | fits | 147,671 | 118 | 0.549 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 150,361 | 1.504 | 20 | 200 | fits | 148,726 | 190 | 0.484 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 759,588 | 7.596 | 20 | 200 | fits | 147,671 | 118 | 0.549 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 151,273 | 1.513 | 20 | 20 | fits | 148,726 | 190 | 0.484 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 867,174 | 8.672 | 20 | 20 | fits | 106,890 | 80 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 154,858 | 1.549 | 20 | 24 | fits | 148,726 | 190 | 0.484 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 870,609 | 8.706 | 20 | 24 | fits | 106,890 | 80 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 153,818 | 1.538 | 20 | 50 | fits | 148,726 | 190 | 0.484 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 763,264 | 7.633 | 20 | 50 | fits | 147,671 | 118 | 0.549 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 421,141 | 4.211 | 20 | 20 | fits | 124,748 | 52 | 0.564 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 604,109 | 6.041 | 20 | 20 | fits | 76,714 | 37 | 0.422 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 272,240 | 2.722 | 20 | 20 | fits | 156,766 | 197 | 0.497 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 148,044 | 1.480 | 20 | 200 | fits | 155,077 | 190 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 304,201 | 3.042 | 20 | 200 | fits | 156,766 | 197 | 0.497 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 148,956 | 1.490 | 20 | 20 | fits | 155,077 | 190 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 775,533 | 7.755 | 20 | 20 | fits | 148,715 | 109 | 0.518 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 152,541 | 1.525 | 20 | 24 | fits | 155,077 | 190 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 857,613 | 8.576 | 20 | 24 | fits | 78,645 | 66 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 151,501 | 1.515 | 20 | 50 | fits | 155,077 | 190 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 778,513 | 7.785 | 20 | 50 | fits | 148,715 | 109 | 0.518 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 444,250 | 4.442 | 20 | 20 | fits | 127,049 | 58 | 0.584 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 627,718 | 6.277 | 20 | 20 | fits | 76,872 | 36 | 0.431 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 313,470 | 3.135 | 20 | 20 | fits | 149,573 | 155 | 0.509 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 139,758 | 1.398 | 20 | 200 | fits | 147,625 | 150 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 448,272 | 4.483 | 20 | 200 | fits | 149,573 | 155 | 0.509 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 140,670 | 1.407 | 20 | 20 | fits | 147,625 | 150 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 855,642 | 8.556 | 20 | 20 | fits | 97,001 | 73 | 0.484 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 144,255 | 1.443 | 20 | 24 | fits | 147,625 | 150 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 859,077 | 8.591 | 20 | 24 | fits | 97,001 | 73 | 0.484 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 143,215 | 1.432 | 20 | 50 | fits | 147,625 | 150 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 451,948 | 4.519 | 20 | 50 | fits | 149,573 | 155 | 0.509 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 576,382 | 5.764 | 20 | 20 | fits | 124,499 | 52 | 0.566 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 759,541 | 7.595 | 20 | 20 | fits | 76,771 | 36 | 0.426 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 608,427 | 6.084 | 20 | 20 | fits | 143,570 | 107 | 0.545 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 144,137 | 1.441 | 20 | 200 | fits | 151,837 | 190 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 745,311 | 7.453 | 20 | 200 | fits | 143,570 | 107 | 0.545 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 145,049 | 1.450 | 20 | 20 | fits | 151,837 | 190 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 746,007 | 7.460 | 20 | 20 | fits | 143,570 | 107 | 0.545 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 148,634 | 1.486 | 20 | 24 | fits | 151,837 | 190 | 0.493 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 850,703 | 8.507 | 20 | 24 | fits | 101,261 | 89 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 147,594 | 1.476 | 20 | 50 | fits | 151,837 | 190 | 0.493 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 748,987 | 7.490 | 20 | 50 | fits | 143,570 | 107 | 0.545 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 420,344 | 4.203 | 20 | 20 | fits | 126,843 | 58 | 0.576 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 603,337 | 6.033 | 20 | 20 | fits | 76,623 | 36 | 0.421 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 685,176 | 6.852 | 20 | 20 | fits | 152,899 | 119 | 0.542 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 149,249 | 1.492 | 20 | 200 | fits | 147,920 | 187 | 0.488 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 772,605 | 7.726 | 20 | 200 | fits | 152,899 | 119 | 0.542 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 150,161 | 1.502 | 20 | 20 | fits | 147,920 | 187 | 0.488 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 944,501 | 9.445 | 20 | 20 | fits | 85,508 | 68 | 0.521 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 153,746 | 1.537 | 20 | 24 | fits | 147,920 | 187 | 0.488 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 947,936 | 9.479 | 20 | 24 | fits | 85,508 | 68 | 0.521 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 152,706 | 1.527 | 20 | 50 | fits | 147,920 | 187 | 0.488 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 776,281 | 7.763 | 20 | 50 | fits | 152,899 | 119 | 0.542 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 284,452 | 2.845 | 20 | 20 | fits | 132,201 | 94 | 0.549 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 467,445 | 4.674 | 20 | 20 | fits | 76,623 | 36 | 0.421 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 709,318 | 7.093 | 20 | 20 | fits | 151,619 | 101 | 0.526 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 150,457 | 1.505 | 20 | 200 | fits | 151,332 | 189 | 0.498 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 851,102 | 8.511 | 20 | 200 | fits | 151,619 | 101 | 0.526 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 151,369 | 1.514 | 20 | 20 | fits | 151,332 | 189 | 0.498 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 851,798 | 8.518 | 20 | 20 | fits | 151,619 | 101 | 0.526 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 154,954 | 1.550 | 20 | 24 | fits | 151,332 | 189 | 0.498 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 948,626 | 9.486 | 20 | 24 | fits | 93,393 | 79 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 153,914 | 1.539 | 20 | 50 | fits | 151,332 | 189 | 0.498 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 617,593 | 6.176 | 20 | 50 | fits | 146,694 | 160 | 0.538 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 285,826 | 2.858 | 20 | 20 | fits | 132,367 | 94 | 0.551 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 468,819 | 4.688 | 20 | 20 | fits | 76,623 | 36 | 0.421 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 767,347 | 7.673 | 20 | 20 | fits | 154,895 | 119 | 0.509 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 146,568 | 1.466 | 20 | 200 | fits | 149,647 | 185 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 855,730 | 8.557 | 20 | 200 | fits | 154,895 | 119 | 0.509 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 147,480 | 1.475 | 20 | 20 | fits | 149,647 | 185 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 856,426 | 8.564 | 20 | 20 | fits | 154,895 | 119 | 0.509 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 151,065 | 1.511 | 20 | 24 | fits | 149,647 | 185 | 0.501 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 938,677 | 9.387 | 20 | 24 | fits | 78,816 | 66 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 150,025 | 1.500 | 20 | 50 | fits | 149,647 | 185 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 859,406 | 8.594 | 20 | 50 | fits | 154,895 | 119 | 0.509 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 281,937 | 2.819 | 20 | 20 | fits | 132,367 | 94 | 0.551 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 471,515 | 4.715 | 20 | 20 | fits | 83,208 | 43 | 0.498 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 261,209 | 2.612 | 20 | 20 | fits | 156,415 | 197 | 0.495 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 137,303 | 1.373 | 20 | 200 | fits | 143,340 | 204 | 0.472 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 293,109 | 2.931 | 20 | 200 | fits | 156,415 | 197 | 0.495 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 138,215 | 1.382 | 20 | 20 | fits | 143,340 | 204 | 0.472 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 851,239 | 8.512 | 20 | 20 | fits | 154,043 | 94 | 0.508 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 141,800 | 1.418 | 20 | 24 | fits | 143,340 | 204 | 0.472 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 933,107 | 9.331 | 20 | 24 | fits | 78,433 | 66 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 140,760 | 1.408 | 20 | 50 | fits | 143,340 | 204 | 0.472 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 296,785 | 2.968 | 20 | 50 | fits | 156,415 | 197 | 0.495 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 436,878 | 4.369 | 20 | 20 | fits | 131,232 | 64 | 0.584 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 698,096 | 6.981 | 20 | 20 | fits | 76,819 | 36 | 0.429 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 367,168 | 3.672 | 20 | 20 | fits | 152,115 | 138 | 0.538 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 146,435 | 1.464 | 20 | 200 | fits | 153,922 | 170 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 454,452 | 4.545 | 20 | 200 | fits | 152,115 | 138 | 0.538 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 147,347 | 1.473 | 20 | 20 | fits | 153,922 | 170 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 942,335 | 9.423 | 20 | 20 | fits | 97,128 | 73 | 0.486 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 150,932 | 1.509 | 20 | 24 | fits | 153,922 | 170 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 945,770 | 9.458 | 20 | 24 | fits | 97,128 | 73 | 0.486 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 149,892 | 1.499 | 20 | 50 | fits | 153,922 | 170 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 296,639 | 2.966 | 20 | 50 | fits | 147,137 | 186 | 0.487 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 662,740 | 6.627 | 20 | 20 | fits | 127,521 | 58 | 0.583 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 846,107 | 8.461 | 20 | 20 | fits | 76,845 | 36 | 0.429 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 261,282 | 2.613 | 20 | 20 | fits | 156,654 | 196 | 0.489 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 137,126 | 1.371 | 20 | 200 | fits | 144,070 | 204 | 0.467 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 293,171 | 2.932 | 20 | 200 | fits | 156,654 | 196 | 0.489 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 138,038 | 1.380 | 20 | 20 | fits | 144,070 | 204 | 0.467 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 772,325 | 7.723 | 20 | 20 | fits | 153,875 | 94 | 0.510 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 141,623 | 1.416 | 20 | 24 | fits | 144,070 | 204 | 0.467 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 854,475 | 8.545 | 20 | 24 | fits | 78,715 | 66 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 140,583 | 1.406 | 20 | 50 | fits | 144,070 | 204 | 0.467 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 296,847 | 2.968 | 20 | 50 | fits | 156,654 | 196 | 0.489 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 421,867 | 4.219 | 20 | 20 | fits | 125,085 | 52 | 0.567 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 619,350 | 6.194 | 20 | 20 | fits | 81,488 | 43 | 0.527 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 707,602 | 7.076 | 20 | 20 | fits | 141,760 | 110 | 0.529 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 152,213 | 1.522 | 20 | 200 | fits | 150,257 | 185 | 0.494 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 782,632 | 7.826 | 20 | 200 | fits | 141,760 | 110 | 0.529 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 153,125 | 1.531 | 20 | 20 | fits | 150,257 | 185 | 0.494 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 783,328 | 7.833 | 20 | 20 | fits | 141,760 | 110 | 0.529 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 156,710 | 1.567 | 20 | 24 | fits | 150,257 | 185 | 0.494 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 865,617 | 8.656 | 20 | 24 | fits | 78,854 | 66 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 155,670 | 1.557 | 20 | 50 | fits | 150,257 | 185 | 0.494 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 786,308 | 7.863 | 20 | 50 | fits | 141,760 | 110 | 0.529 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 288,785 | 2.888 | 20 | 20 | fits | 133,570 | 94 | 0.548 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 486,420 | 4.864 | 20 | 20 | fits | 81,424 | 43 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 608,447 | 6.084 | 20 | 20 | fits | 149,189 | 152 | 0.509 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 144,626 | 1.446 | 20 | 200 | fits | 144,070 | 204 | 0.467 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 625,949 | 6.259 | 20 | 200 | fits | 149,189 | 152 | 0.509 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 145,538 | 1.455 | 20 | 20 | fits | 144,070 | 204 | 0.467 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 878,416 | 8.784 | 20 | 20 | fits | 101,000 | 69 | 0.556 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 149,123 | 1.491 | 20 | 24 | fits | 144,070 | 204 | 0.467 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 881,851 | 8.819 | 20 | 24 | fits | 101,000 | 69 | 0.556 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 148,083 | 1.481 | 20 | 50 | fits | 144,070 | 204 | 0.467 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 629,625 | 6.296 | 20 | 50 | fits | 149,189 | 152 | 0.509 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 280,997 | 2.810 | 20 | 20 | fits | 133,369 | 95 | 0.544 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 478,356 | 4.784 | 20 | 20 | fits | 76,922 | 36 | 0.433 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 636,229 | 6.362 | 20 | 20 | fits | 151,016 | 104 | 0.594 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 150,947 | 1.509 | 20 | 200 | fits | 151,791 | 190 | 0.489 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 768,108 | 7.681 | 20 | 200 | fits | 151,016 | 104 | 0.594 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 151,859 | 1.519 | 20 | 20 | fits | 151,791 | 190 | 0.489 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 768,804 | 7.688 | 20 | 20 | fits | 151,016 | 104 | 0.594 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 155,444 | 1.554 | 20 | 24 | fits | 151,791 | 190 | 0.489 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 945,305 | 9.453 | 20 | 24 | fits | 110,799 | 93 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 154,404 | 1.544 | 20 | 50 | fits | 151,791 | 190 | 0.489 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 771,784 | 7.718 | 20 | 50 | fits | 151,016 | 104 | 0.594 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 435,570 | 4.356 | 20 | 20 | fits | 124,670 | 52 | 0.565 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 618,688 | 6.187 | 20 | 20 | fits | 76,771 | 36 | 0.426 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 747,758 | 7.478 | 20 | 20 | fits | 148,572 | 111 | 0.558 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 149,821 | 1.498 | 20 | 200 | fits | 150,110 | 185 | 0.494 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 824,796 | 8.248 | 20 | 200 | fits | 148,572 | 111 | 0.558 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 150,733 | 1.507 | 20 | 20 | fits | 150,110 | 185 | 0.494 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 947,638 | 9.476 | 20 | 20 | fits | 112,849 | 93 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 154,318 | 1.543 | 20 | 24 | fits | 150,110 | 185 | 0.494 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 951,073 | 9.511 | 20 | 24 | fits | 112,849 | 93 | 0.463 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 153,278 | 1.533 | 20 | 50 | fits | 150,110 | 185 | 0.494 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 828,472 | 8.285 | 20 | 50 | fits | 148,572 | 111 | 0.558 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 285,989 | 2.860 | 20 | 20 | fits | 133,166 | 94 | 0.546 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 468,941 | 4.689 | 20 | 20 | fits | 76,623 | 36 | 0.421 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 668,047 | 6.680 | 20 | 20 | fits | 153,243 | 154 | 0.528 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 142,141 | 1.421 | 20 | 200 | fits | 143,867 | 204 | 0.466 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 687,736 | 6.877 | 20 | 200 | fits | 153,243 | 154 | 0.528 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 143,053 | 1.431 | 20 | 20 | fits | 143,867 | 204 | 0.466 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 934,511 | 9.345 | 20 | 20 | fits | 93,893 | 73 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 146,638 | 1.466 | 20 | 24 | fits | 143,867 | 204 | 0.466 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 937,946 | 9.379 | 20 | 24 | fits | 93,893 | 73 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 145,598 | 1.456 | 20 | 50 | fits | 143,867 | 204 | 0.466 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 691,412 | 6.914 | 20 | 50 | fits | 153,243 | 154 | 0.528 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 278,012 | 2.780 | 20 | 20 | fits | 132,869 | 94 | 0.542 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 474,324 | 4.743 | 20 | 20 | fits | 90,021 | 42 | 0.521 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 674,185 | 6.742 | 20 | 20 | fits | 152,979 | 156 | 0.533 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 148,293 | 1.483 | 20 | 200 | fits | 151,531 | 189 | 0.489 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 706,396 | 7.064 | 20 | 200 | fits | 152,979 | 156 | 0.533 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 149,205 | 1.492 | 20 | 20 | fits | 151,531 | 189 | 0.489 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 852,890 | 8.529 | 20 | 20 | fits | 145,798 | 109 | 0.496 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 152,790 | 1.528 | 20 | 24 | fits | 151,531 | 189 | 0.489 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 934,834 | 9.348 | 20 | 24 | fits | 78,509 | 66 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 151,750 | 1.518 | 20 | 50 | fits | 151,531 | 189 | 0.489 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 855,870 | 8.559 | 20 | 50 | fits | 145,798 | 109 | 0.496 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 284,461 | 2.845 | 20 | 20 | fits | 133,166 | 94 | 0.546 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 545,101 | 5.451 | 20 | 20 | fits | 79,448 | 38 | 0.514 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 731,306 | 7.313 | 20 | 20 | fits | 149,252 | 96 | 0.521 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 142,097 | 1.421 | 20 | 200 | fits | 148,134 | 187 | 0.481 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 846,350 | 8.463 | 20 | 200 | fits | 149,252 | 96 | 0.521 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 143,009 | 1.430 | 20 | 20 | fits | 148,134 | 187 | 0.481 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 928,216 | 9.282 | 20 | 20 | fits | 81,170 | 61 | 0.487 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 146,594 | 1.466 | 20 | 24 | fits | 148,134 | 187 | 0.481 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 931,651 | 9.317 | 20 | 24 | fits | 81,170 | 61 | 0.487 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 145,554 | 1.456 | 20 | 50 | fits | 148,134 | 187 | 0.481 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 301,057 | 3.011 | 20 | 50 | fits | 155,893 | 211 | 0.465 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 437,628 | 4.376 | 20 | 20 | fits | 136,636 | 59 | 0.594 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 698,694 | 6.987 | 20 | 20 | fits | 77,112 | 36 | 0.440 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 278,772 | 2.788 | 20 | 20 | fits | 156,765 | 196 | 0.500 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 145,131 | 1.451 | 20 | 200 | fits | 151,825 | 190 | 0.498 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 310,873 | 3.109 | 20 | 200 | fits | 156,765 | 196 | 0.500 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 146,043 | 1.460 | 20 | 20 | fits | 151,825 | 190 | 0.498 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 772,587 | 7.726 | 20 | 20 | fits | 147,935 | 109 | 0.513 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 149,628 | 1.496 | 20 | 24 | fits | 151,825 | 190 | 0.498 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 854,721 | 8.547 | 20 | 24 | fits | 78,699 | 66 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 148,588 | 1.486 | 20 | 50 | fits | 151,825 | 190 | 0.498 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 775,567 | 7.756 | 20 | 50 | fits | 147,935 | 109 | 0.513 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 442,042 | 4.420 | 20 | 20 | fits | 127,558 | 58 | 0.582 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 625,552 | 6.256 | 20 | 20 | fits | 76,909 | 36 | 0.429 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 607,173 | 6.072 | 20 | 20 | fits | 143,712 | 108 | 0.545 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 145,225 | 1.452 | 20 | 200 | fits | 151,476 | 189 | 0.496 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 744,191 | 7.442 | 20 | 200 | fits | 143,712 | 108 | 0.545 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 146,137 | 1.461 | 20 | 20 | fits | 151,476 | 189 | 0.496 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 744,887 | 7.449 | 20 | 20 | fits | 143,712 | 108 | 0.545 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 149,722 | 1.497 | 20 | 24 | fits | 151,476 | 189 | 0.496 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 853,289 | 8.533 | 20 | 24 | fits | 96,074 | 86 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 148,682 | 1.487 | 20 | 50 | fits | 151,476 | 189 | 0.496 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 747,867 | 7.479 | 20 | 50 | fits | 143,712 | 108 | 0.545 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 419,211 | 4.192 | 20 | 20 | fits | 124,249 | 52 | 0.559 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 602,075 | 6.021 | 20 | 20 | fits | 76,613 | 36 | 0.419 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 651,135 | 6.511 | 20 | 20 | fits | 151,910 | 103 | 0.530 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 140,855 | 1.409 | 20 | 200 | fits | 147,990 | 187 | 0.488 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 767,084 | 7.671 | 20 | 200 | fits | 151,910 | 103 | 0.530 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 141,767 | 1.418 | 20 | 20 | fits | 147,990 | 187 | 0.488 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 857,682 | 8.577 | 20 | 20 | fits | 89,902 | 69 | 0.514 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 145,352 | 1.454 | 20 | 24 | fits | 147,990 | 187 | 0.488 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 861,117 | 8.611 | 20 | 24 | fits | 89,902 | 69 | 0.514 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 144,312 | 1.443 | 20 | 50 | fits | 147,990 | 187 | 0.488 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 299,832 | 2.998 | 20 | 50 | fits | 155,910 | 211 | 0.472 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 424,190 | 4.242 | 20 | 20 | fits | 124,423 | 52 | 0.563 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 607,155 | 6.072 | 20 | 20 | fits | 76,714 | 37 | 0.420 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 637,607 | 6.376 | 20 | 20 | fits | 144,612 | 93 | 0.558 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 146,005 | 1.460 | 20 | 200 | fits | 154,024 | 170 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 771,312 | 7.713 | 20 | 200 | fits | 144,612 | 93 | 0.558 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 146,917 | 1.469 | 20 | 20 | fits | 154,024 | 170 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 948,014 | 9.480 | 20 | 20 | fits | 95,670 | 74 | 0.466 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 150,502 | 1.505 | 20 | 24 | fits | 154,024 | 170 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 951,449 | 9.514 | 20 | 24 | fits | 95,670 | 74 | 0.466 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 149,462 | 1.495 | 20 | 50 | fits | 154,024 | 170 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 298,155 | 2.982 | 20 | 50 | fits | 149,083 | 189 | 0.486 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 430,690 | 4.307 | 20 | 20 | fits | 132,600 | 94 | 0.547 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 628,296 | 6.283 | 20 | 20 | fits | 81,395 | 43 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 756,573 | 7.566 | 20 | 20 | fits | 142,817 | 113 | 0.519 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 149,430 | 1.494 | 20 | 200 | fits | 147,990 | 187 | 0.488 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 857,625 | 8.576 | 20 | 200 | fits | 142,817 | 113 | 0.519 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 150,342 | 1.503 | 20 | 20 | fits | 147,990 | 187 | 0.488 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 953,155 | 9.532 | 20 | 20 | fits | 94,834 | 73 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 153,927 | 1.539 | 20 | 24 | fits | 147,990 | 187 | 0.488 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 956,590 | 9.566 | 20 | 24 | fits | 94,834 | 73 | 0.453 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 152,887 | 1.529 | 20 | 50 | fits | 147,990 | 187 | 0.488 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 861,301 | 8.613 | 20 | 50 | fits | 142,817 | 113 | 0.519 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 284,880 | 2.849 | 20 | 20 | fits | 132,448 | 94 | 0.547 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 482,147 | 4.821 | 20 | 20 | fits | 81,323 | 43 | 0.523 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 695,400 | 6.954 | 20 | 20 | fits | 144,156 | 165 | 0.509 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 152,032 | 1.520 | 20 | 200 | fits | 151,476 | 189 | 0.496 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 714,194 | 7.142 | 20 | 200 | fits | 144,156 | 165 | 0.509 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 152,944 | 1.529 | 20 | 20 | fits | 151,476 | 189 | 0.496 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 865,488 | 8.655 | 20 | 20 | fits | 150,598 | 93 | 0.484 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 156,529 | 1.565 | 20 | 24 | fits | 151,476 | 189 | 0.496 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 947,468 | 9.475 | 20 | 24 | fits | 78,545 | 66 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 155,489 | 1.555 | 20 | 50 | fits | 151,476 | 189 | 0.496 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 717,870 | 7.179 | 20 | 50 | fits | 144,156 | 165 | 0.509 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 287,863 | 2.879 | 20 | 20 | fits | 132,829 | 95 | 0.550 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 491,497 | 4.915 | 20 | 20 | fits | 82,793 | 42 | 0.495 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 771,951 | 7.720 | 20 | 20 | fits | 145,257 | 110 | 0.544 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 149,768 | 1.498 | 20 | 200 | fits | 150,096 | 186 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 846,632 | 8.466 | 20 | 200 | fits | 145,257 | 110 | 0.544 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 150,680 | 1.507 | 20 | 20 | fits | 150,096 | 186 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 942,584 | 9.426 | 20 | 20 | fits | 95,256 | 74 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 154,265 | 1.543 | 20 | 24 | fits | 150,096 | 186 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 946,019 | 9.460 | 20 | 24 | fits | 95,256 | 74 | 0.453 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 153,225 | 1.532 | 20 | 50 | fits | 150,096 | 186 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 850,308 | 8.503 | 20 | 50 | fits | 145,257 | 110 | 0.544 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 438,449 | 4.384 | 20 | 20 | fits | 130,086 | 58 | 0.583 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 702,971 | 7.030 | 20 | 20 | fits | 76,943 | 36 | 0.431 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 722,244 | 7.222 | 20 | 20 | fits | 144,785 | 112 | 0.536 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 148,312 | 1.483 | 20 | 200 | fits | 148,023 | 187 | 0.480 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 824,605 | 8.246 | 20 | 200 | fits | 144,785 | 112 | 0.536 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 149,224 | 1.492 | 20 | 20 | fits | 148,023 | 187 | 0.480 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 945,259 | 9.453 | 20 | 20 | fits | 110,653 | 87 | 0.473 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 152,809 | 1.528 | 20 | 24 | fits | 148,023 | 187 | 0.480 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 948,694 | 9.487 | 20 | 24 | fits | 110,653 | 87 | 0.473 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 151,769 | 1.518 | 20 | 50 | fits | 148,023 | 187 | 0.480 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 828,281 | 8.283 | 20 | 50 | fits | 144,785 | 112 | 0.536 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 498,561 | 4.986 | 20 | 20 | fits | 124,112 | 52 | 0.559 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 681,416 | 6.814 | 20 | 20 | fits | 76,613 | 36 | 0.419 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 603,500 | 6.035 | 20 | 20 | fits | 149,272 | 152 | 0.508 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 140,094 | 1.401 | 20 | 200 | fits | 143,941 | 204 | 0.476 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 621,042 | 6.210 | 20 | 200 | fits | 149,272 | 152 | 0.508 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 141,006 | 1.410 | 20 | 20 | fits | 143,941 | 204 | 0.476 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 853,928 | 8.539 | 20 | 20 | fits | 81,283 | 61 | 0.489 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 144,591 | 1.446 | 20 | 24 | fits | 143,941 | 204 | 0.476 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 857,363 | 8.574 | 20 | 24 | fits | 81,283 | 61 | 0.489 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 143,551 | 1.436 | 20 | 50 | fits | 143,941 | 204 | 0.476 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 624,718 | 6.247 | 20 | 50 | fits | 149,272 | 152 | 0.508 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 275,975 | 2.760 | 20 | 20 | fits | 132,879 | 95 | 0.548 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 473,366 | 4.734 | 20 | 20 | fits | 76,986 | 36 | 0.433 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 620,604 | 6.206 | 20 | 20 | fits | 143,125 | 107 | 0.542 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 145,239 | 1.452 | 20 | 200 | fits | 151,662 | 190 | 0.498 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 757,035 | 7.570 | 20 | 200 | fits | 143,125 | 107 | 0.542 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 146,151 | 1.462 | 20 | 20 | fits | 151,662 | 190 | 0.498 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 757,731 | 7.577 | 20 | 20 | fits | 143,125 | 107 | 0.542 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 149,736 | 1.497 | 20 | 24 | fits | 151,662 | 190 | 0.498 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 853,967 | 8.540 | 20 | 24 | fits | 92,801 | 79 | 0.378 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 148,696 | 1.487 | 20 | 50 | fits | 151,662 | 190 | 0.498 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 760,711 | 7.607 | 20 | 50 | fits | 143,125 | 107 | 0.542 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 431,996 | 4.320 | 20 | 20 | fits | 126,898 | 58 | 0.575 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 615,506 | 6.155 | 20 | 20 | fits | 76,909 | 36 | 0.429 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 641,098 | 6.411 | 20 | 20 | fits | 148,865 | 96 | 0.516 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 142,135 | 1.421 | 20 | 200 | fits | 148,505 | 188 | 0.484 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 756,255 | 7.563 | 20 | 200 | fits | 148,865 | 96 | 0.516 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 143,047 | 1.430 | 20 | 20 | fits | 148,505 | 188 | 0.484 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 847,192 | 8.472 | 20 | 20 | fits | 90,241 | 70 | 0.514 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 146,632 | 1.466 | 20 | 24 | fits | 148,505 | 188 | 0.484 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 850,627 | 8.506 | 20 | 24 | fits | 90,241 | 70 | 0.514 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 145,592 | 1.456 | 20 | 50 | fits | 148,505 | 188 | 0.484 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 301,075 | 3.011 | 20 | 50 | fits | 155,873 | 211 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 425,716 | 4.257 | 20 | 20 | fits | 124,706 | 52 | 0.565 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 608,986 | 6.090 | 20 | 20 | fits | 76,835 | 36 | 0.426 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 594,843 | 5.948 | 20 | 20 | fits | 156,212 | 171 | 0.500 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 152,589 | 1.526 | 20 | 200 | fits | 151,506 | 189 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 626,074 | 6.261 | 20 | 200 | fits | 156,212 | 171 | 0.500 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 153,501 | 1.535 | 20 | 20 | fits | 151,506 | 189 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 774,042 | 7.740 | 20 | 20 | fits | 147,272 | 96 | 0.508 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 157,086 | 1.571 | 20 | 24 | fits | 151,506 | 189 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 868,497 | 8.685 | 20 | 24 | fits | 81,929 | 73 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 156,046 | 1.560 | 20 | 50 | fits | 151,506 | 189 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 629,750 | 6.298 | 20 | 50 | fits | 156,212 | 171 | 0.500 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 288,354 | 2.884 | 20 | 20 | fits | 132,763 | 94 | 0.551 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 471,458 | 4.715 | 20 | 20 | fits | 76,687 | 36 | 0.421 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 702,352 | 7.024 | 20 | 20 | fits | 145,218 | 113 | 0.550 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 148,928 | 1.489 | 20 | 200 | fits | 149,953 | 185 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 777,269 | 7.773 | 20 | 200 | fits | 145,218 | 113 | 0.550 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 149,840 | 1.498 | 20 | 20 | fits | 149,953 | 185 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 777,965 | 7.780 | 20 | 20 | fits | 145,218 | 113 | 0.550 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 153,425 | 1.534 | 20 | 24 | fits | 149,953 | 185 | 0.501 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 874,256 | 8.743 | 20 | 24 | fits | 92,856 | 79 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 152,385 | 1.524 | 20 | 50 | fits | 149,953 | 185 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 780,945 | 7.809 | 20 | 50 | fits | 145,218 | 113 | 0.550 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 284,693 | 2.847 | 20 | 20 | fits | 132,763 | 94 | 0.551 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 467,797 | 4.678 | 20 | 20 | fits | 76,687 | 36 | 0.421 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 607,385 | 6.074 | 20 | 20 | fits | 151,612 | 159 | 0.517 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 140,581 | 1.406 | 20 | 200 | fits | 143,714 | 204 | 0.474 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 625,285 | 6.253 | 20 | 200 | fits | 151,612 | 159 | 0.517 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 141,493 | 1.415 | 20 | 20 | fits | 143,714 | 204 | 0.474 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 857,844 | 8.578 | 20 | 20 | fits | 81,285 | 61 | 0.489 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 145,078 | 1.451 | 20 | 24 | fits | 143,714 | 204 | 0.474 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 861,279 | 8.613 | 20 | 24 | fits | 81,285 | 61 | 0.489 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 144,038 | 1.440 | 20 | 50 | fits | 143,714 | 204 | 0.474 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 628,961 | 6.290 | 20 | 50 | fits | 151,612 | 159 | 0.517 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 276,050 | 2.760 | 20 | 20 | fits | 132,467 | 94 | 0.546 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 465,778 | 4.658 | 20 | 20 | fits | 83,349 | 43 | 0.500 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 624,007 | 6.240 | 20 | 20 | fits | 143,997 | 107 | 0.546 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 145,461 | 1.455 | 20 | 200 | fits | 151,506 | 189 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 761,337 | 7.613 | 20 | 200 | fits | 143,997 | 107 | 0.546 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 146,373 | 1.464 | 20 | 20 | fits | 151,506 | 189 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 762,033 | 7.620 | 20 | 20 | fits | 143,997 | 107 | 0.546 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 149,958 | 1.500 | 20 | 24 | fits | 151,506 | 189 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 858,264 | 8.583 | 20 | 24 | fits | 92,796 | 79 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 148,918 | 1.489 | 20 | 50 | fits | 151,506 | 189 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 765,013 | 7.650 | 20 | 50 | fits | 143,997 | 107 | 0.546 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 435,688 | 4.357 | 20 | 20 | fits | 131,172 | 64 | 0.581 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 618,936 | 6.189 | 20 | 20 | fits | 76,712 | 36 | 0.421 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 316,601 | 3.166 | 20 | 20 | fits | 149,208 | 134 | 0.526 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 141,365 | 1.414 | 20 | 200 | fits | 148,714 | 168 | 0.490 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 447,350 | 4.473 | 20 | 200 | fits | 149,208 | 134 | 0.526 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 142,277 | 1.423 | 20 | 20 | fits | 148,714 | 168 | 0.490 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 858,748 | 8.587 | 20 | 20 | fits | 97,287 | 73 | 0.484 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 145,862 | 1.459 | 20 | 24 | fits | 148,714 | 168 | 0.490 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 862,183 | 8.622 | 20 | 24 | fits | 97,287 | 73 | 0.484 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 144,822 | 1.448 | 20 | 50 | fits | 148,714 | 168 | 0.490 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 292,535 | 2.925 | 20 | 50 | fits | 148,103 | 191 | 0.471 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 578,872 | 5.789 | 20 | 20 | fits | 127,911 | 58 | 0.584 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 762,361 | 7.624 | 20 | 20 | fits | 76,909 | 36 | 0.429 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 658,049 | 6.580 | 20 | 20 | fits | 156,574 | 122 | 0.498 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 145,566 | 1.456 | 20 | 200 | fits | 148,244 | 187 | 0.490 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 773,688 | 7.737 | 20 | 200 | fits | 156,574 | 122 | 0.498 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 146,478 | 1.465 | 20 | 20 | fits | 148,244 | 187 | 0.490 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 855,285 | 8.553 | 20 | 20 | fits | 72,010 | 56 | 0.565 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 150,063 | 1.501 | 20 | 24 | fits | 148,244 | 187 | 0.490 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 858,720 | 8.587 | 20 | 24 | fits | 72,010 | 56 | 0.565 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 149,023 | 1.490 | 20 | 50 | fits | 148,244 | 187 | 0.490 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 777,364 | 7.774 | 20 | 50 | fits | 156,574 | 122 | 0.498 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 281,757 | 2.818 | 20 | 20 | fits | 133,189 | 94 | 0.553 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 464,861 | 4.649 | 20 | 20 | fits | 76,687 | 36 | 0.421 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 269,085 | 2.691 | 20 | 20 | fits | 156,137 | 196 | 0.495 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 145,434 | 1.454 | 20 | 200 | fits | 151,479 | 189 | 0.498 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 300,962 | 3.010 | 20 | 200 | fits | 156,137 | 196 | 0.495 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 146,346 | 1.463 | 20 | 20 | fits | 151,479 | 189 | 0.498 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 775,163 | 7.752 | 20 | 20 | fits | 149,208 | 109 | 0.521 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 149,931 | 1.499 | 20 | 24 | fits | 151,479 | 189 | 0.498 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 857,334 | 8.573 | 20 | 24 | fits | 78,736 | 66 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 148,891 | 1.489 | 20 | 50 | fits | 151,479 | 189 | 0.498 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 778,143 | 7.781 | 20 | 50 | fits | 149,208 | 109 | 0.521 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 429,423 | 4.294 | 20 | 20 | fits | 124,850 | 52 | 0.563 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 626,855 | 6.269 | 20 | 20 | fits | 81,482 | 43 | 0.527 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 684,103 | 6.841 | 20 | 20 | fits | 146,746 | 110 | 0.552 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 143,034 | 1.430 | 20 | 200 | fits | 149,928 | 185 | 0.502 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 759,248 | 7.592 | 20 | 200 | fits | 146,746 | 110 | 0.552 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 143,946 | 1.439 | 20 | 20 | fits | 149,928 | 185 | 0.502 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 863,610 | 8.636 | 20 | 20 | fits | 103,666 | 81 | 0.481 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 147,531 | 1.475 | 20 | 24 | fits | 149,928 | 185 | 0.502 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 867,045 | 8.670 | 20 | 24 | fits | 103,666 | 81 | 0.481 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 146,491 | 1.465 | 20 | 50 | fits | 149,928 | 185 | 0.502 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 762,924 | 7.629 | 20 | 50 | fits | 146,746 | 110 | 0.552 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 416,978 | 4.170 | 20 | 20 | fits | 124,684 | 53 | 0.560 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 614,098 | 6.141 | 20 | 20 | fits | 76,986 | 36 | 0.433 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 610,811 | 6.108 | 20 | 20 | fits | 144,319 | 164 | 0.509 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 152,718 | 1.527 | 20 | 200 | fits | 151,479 | 189 | 0.498 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 629,605 | 6.296 | 20 | 200 | fits | 144,319 | 164 | 0.509 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 153,630 | 1.536 | 20 | 20 | fits | 151,479 | 189 | 0.498 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 779,896 | 7.799 | 20 | 20 | fits | 149,595 | 91 | 0.530 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 157,215 | 1.572 | 20 | 24 | fits | 151,479 | 189 | 0.498 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 954,783 | 9.548 | 20 | 24 | fits | 93,764 | 80 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 156,175 | 1.562 | 20 | 50 | fits | 151,479 | 189 | 0.498 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 633,281 | 6.333 | 20 | 50 | fits | 144,319 | 164 | 0.509 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 289,127 | 2.891 | 20 | 20 | fits | 133,407 | 95 | 0.555 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 486,882 | 4.869 | 20 | 20 | fits | 76,986 | 36 | 0.433 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 769,540 | 7.695 | 20 | 20 | fits | 145,707 | 111 | 0.544 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 149,180 | 1.492 | 20 | 200 | fits | 150,049 | 186 | 0.502 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 844,246 | 8.442 | 20 | 200 | fits | 145,707 | 111 | 0.544 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 150,092 | 1.501 | 20 | 20 | fits | 150,049 | 186 | 0.502 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 940,225 | 9.402 | 20 | 20 | fits | 95,283 | 74 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 153,677 | 1.537 | 20 | 24 | fits | 150,049 | 186 | 0.502 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 943,660 | 9.437 | 20 | 24 | fits | 95,283 | 74 | 0.453 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 152,637 | 1.526 | 20 | 50 | fits | 150,049 | 186 | 0.502 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 847,922 | 8.479 | 20 | 50 | fits | 145,707 | 111 | 0.544 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 432,844 | 4.328 | 20 | 20 | fits | 124,753 | 52 | 0.565 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 622,705 | 6.227 | 20 | 20 | fits | 83,464 | 42 | 0.507 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 274,799 | 2.748 | 20 | 20 | fits | 144,953 | 189 | 0.505 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 141,206 | 1.412 | 20 | 200 | fits | 144,183 | 205 | 0.477 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 294,473 | 2.945 | 20 | 200 | fits | 144,953 | 189 | 0.505 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 142,118 | 1.421 | 20 | 20 | fits | 144,183 | 205 | 0.477 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 938,322 | 9.383 | 20 | 20 | fits | 94,926 | 74 | 0.457 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 145,703 | 1.457 | 20 | 24 | fits | 144,183 | 205 | 0.477 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 941,757 | 9.418 | 20 | 24 | fits | 94,926 | 74 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 144,663 | 1.447 | 20 | 50 | fits | 144,183 | 205 | 0.477 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 298,149 | 2.981 | 20 | 50 | fits | 144,953 | 189 | 0.505 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 422,789 | 4.228 | 20 | 20 | fits | 124,705 | 52 | 0.563 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 691,310 | 6.913 | 20 | 20 | fits | 78,054 | 37 | 0.466 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 676,465 | 6.765 | 20 | 20 | fits | 144,081 | 165 | 0.504 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 148,534 | 1.485 | 20 | 200 | fits | 151,608 | 189 | 0.498 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 695,380 | 6.954 | 20 | 200 | fits | 144,081 | 165 | 0.504 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 149,446 | 1.494 | 20 | 20 | fits | 151,608 | 189 | 0.498 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 847,890 | 8.479 | 20 | 20 | fits | 142,661 | 90 | 0.524 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 153,031 | 1.530 | 20 | 24 | fits | 151,608 | 189 | 0.498 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 944,688 | 9.447 | 20 | 24 | fits | 93,363 | 79 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 151,991 | 1.520 | 20 | 50 | fits | 151,608 | 189 | 0.498 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 699,056 | 6.991 | 20 | 50 | fits | 144,081 | 165 | 0.504 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 284,570 | 2.846 | 20 | 20 | fits | 133,034 | 94 | 0.553 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 552,895 | 5.529 | 20 | 20 | fits | 77,862 | 37 | 0.460 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 769,224 | 7.692 | 20 | 20 | fits | 146,597 | 110 | 0.551 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 144,010 | 1.440 | 20 | 200 | fits | 150,055 | 185 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 844,299 | 8.443 | 20 | 200 | fits | 146,597 | 110 | 0.551 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 144,922 | 1.449 | 20 | 20 | fits | 150,055 | 185 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 940,332 | 9.403 | 20 | 20 | fits | 95,337 | 73 | 0.456 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 148,507 | 1.485 | 20 | 24 | fits | 150,055 | 185 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 943,767 | 9.438 | 20 | 24 | fits | 95,337 | 73 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 147,467 | 1.475 | 20 | 50 | fits | 150,055 | 185 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 847,975 | 8.480 | 20 | 50 | fits | 146,597 | 110 | 0.551 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 423,064 | 4.231 | 20 | 20 | fits | 129,853 | 58 | 0.579 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 699,298 | 6.993 | 20 | 20 | fits | 81,394 | 43 | 0.526 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 639,088 | 6.391 | 20 | 20 | fits | 148,102 | 95 | 0.513 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 141,788 | 1.418 | 20 | 200 | fits | 148,412 | 188 | 0.483 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 753,612 | 7.536 | 20 | 200 | fits | 148,102 | 95 | 0.513 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 142,700 | 1.427 | 20 | 20 | fits | 148,412 | 188 | 0.483 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 847,535 | 8.475 | 20 | 20 | fits | 93,227 | 68 | 0.472 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 146,285 | 1.463 | 20 | 24 | fits | 148,412 | 188 | 0.483 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 850,970 | 8.510 | 20 | 24 | fits | 93,227 | 68 | 0.472 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 145,245 | 1.452 | 20 | 50 | fits | 148,412 | 188 | 0.483 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 296,471 | 2.965 | 20 | 50 | fits | 142,857 | 204 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 423,596 | 4.236 | 20 | 20 | fits | 127,190 | 58 | 0.577 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 607,106 | 6.071 | 20 | 20 | fits | 76,909 | 36 | 0.429 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 261,812 | 2.618 | 20 | 20 | fits | 156,617 | 196 | 0.488 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 137,693 | 1.377 | 20 | 200 | fits | 143,738 | 204 | 0.466 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 293,701 | 2.937 | 20 | 200 | fits | 156,617 | 196 | 0.488 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 138,605 | 1.386 | 20 | 20 | fits | 143,738 | 204 | 0.466 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 757,364 | 7.574 | 20 | 20 | fits | 153,397 | 95 | 0.504 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 142,190 | 1.422 | 20 | 24 | fits | 143,738 | 204 | 0.466 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 852,445 | 8.524 | 20 | 24 | fits | 82,581 | 73 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 141,150 | 1.411 | 20 | 50 | fits | 143,738 | 204 | 0.466 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 297,377 | 2.974 | 20 | 50 | fits | 156,617 | 196 | 0.488 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 422,003 | 4.220 | 20 | 20 | fits | 124,691 | 52 | 0.564 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 604,867 | 6.049 | 20 | 20 | fits | 76,613 | 36 | 0.419 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 632,442 | 6.324 | 20 | 20 | fits | 154,504 | 105 | 0.532 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 146,973 | 1.470 | 20 | 200 | fits | 154,340 | 170 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 775,822 | 7.758 | 20 | 200 | fits | 154,504 | 105 | 0.532 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 147,885 | 1.479 | 20 | 20 | fits | 154,340 | 170 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 776,518 | 7.765 | 20 | 20 | fits | 154,504 | 105 | 0.532 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 151,470 | 1.515 | 20 | 24 | fits | 154,340 | 170 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 868,288 | 8.683 | 20 | 24 | fits | 88,335 | 75 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 150,430 | 1.504 | 20 | 50 | fits | 154,340 | 170 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 297,243 | 2.972 | 20 | 50 | fits | 147,203 | 185 | 0.479 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 430,094 | 4.301 | 20 | 20 | fits | 132,916 | 94 | 0.541 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 613,299 | 6.133 | 20 | 20 | fits | 76,788 | 37 | 0.422 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 597,257 | 5.973 | 20 | 20 | fits | 152,279 | 159 | 0.515 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 145,271 | 1.453 | 20 | 200 | fits | 143,738 | 204 | 0.466 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 614,821 | 6.148 | 20 | 200 | fits | 152,279 | 159 | 0.515 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 146,183 | 1.462 | 20 | 20 | fits | 143,738 | 204 | 0.466 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 869,923 | 8.699 | 20 | 20 | fits | 94,104 | 73 | 0.447 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 149,768 | 1.498 | 20 | 24 | fits | 143,738 | 204 | 0.466 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 873,358 | 8.734 | 20 | 24 | fits | 94,104 | 73 | 0.447 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 148,728 | 1.487 | 20 | 50 | fits | 143,738 | 204 | 0.466 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 618,497 | 6.185 | 20 | 50 | fits | 152,279 | 159 | 0.515 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 281,072 | 2.811 | 20 | 20 | fits | 132,799 | 94 | 0.539 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 464,138 | 4.641 | 20 | 20 | fits | 76,687 | 36 | 0.421 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 615,109 | 6.151 | 20 | 20 | fits | 150,536 | 148 | 0.565 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 151,755 | 1.518 | 20 | 200 | fits | 151,622 | 189 | 0.491 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 634,467 | 6.345 | 20 | 200 | fits | 150,536 | 148 | 0.565 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 152,667 | 1.527 | 20 | 20 | fits | 151,622 | 189 | 0.491 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 783,468 | 7.835 | 20 | 20 | fits | 148,305 | 105 | 0.514 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 156,252 | 1.563 | 20 | 24 | fits | 151,622 | 189 | 0.491 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 880,082 | 8.801 | 20 | 24 | fits | 93,179 | 79 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 155,212 | 1.552 | 20 | 50 | fits | 151,622 | 189 | 0.491 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 786,448 | 7.864 | 20 | 50 | fits | 148,305 | 105 | 0.514 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 287,921 | 2.879 | 20 | 20 | fits | 133,164 | 94 | 0.545 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 485,527 | 4.855 | 20 | 20 | fits | 81,395 | 43 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 680,192 | 6.802 | 20 | 20 | fits | 156,476 | 121 | 0.498 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 147,011 | 1.470 | 20 | 200 | fits | 148,278 | 187 | 0.483 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 795,740 | 7.957 | 20 | 200 | fits | 156,476 | 121 | 0.498 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 147,923 | 1.479 | 20 | 20 | fits | 148,278 | 187 | 0.483 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 864,082 | 8.641 | 20 | 20 | fits | 67,646 | 49 | 0.528 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 151,508 | 1.515 | 20 | 24 | fits | 148,278 | 187 | 0.483 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 867,517 | 8.675 | 20 | 24 | fits | 67,646 | 49 | 0.528 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 150,468 | 1.505 | 20 | 50 | fits | 148,278 | 187 | 0.483 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 799,416 | 7.994 | 20 | 50 | fits | 156,476 | 121 | 0.498 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 283,039 | 2.830 | 20 | 20 | fits | 133,026 | 95 | 0.541 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 486,202 | 4.862 | 20 | 20 | fits | 82,793 | 42 | 0.495 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 282,253 | 2.823 | 20 | 20 | fits | 156,647 | 196 | 0.493 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 149,128 | 1.491 | 20 | 200 | fits | 151,795 | 190 | 0.491 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 314,408 | 3.144 | 20 | 200 | fits | 156,647 | 196 | 0.493 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 150,040 | 1.500 | 20 | 20 | fits | 151,795 | 190 | 0.491 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 779,221 | 7.792 | 20 | 20 | fits | 147,942 | 109 | 0.512 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 153,625 | 1.536 | 20 | 24 | fits | 151,795 | 190 | 0.491 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 861,289 | 8.613 | 20 | 24 | fits | 78,633 | 66 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 152,585 | 1.526 | 20 | 50 | fits | 151,795 | 190 | 0.491 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 782,201 | 7.822 | 20 | 50 | fits | 147,942 | 109 | 0.512 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 448,628 | 4.486 | 20 | 20 | fits | 130,609 | 58 | 0.587 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 632,179 | 6.322 | 20 | 20 | fits | 76,909 | 36 | 0.429 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 605,984 | 6.060 | 20 | 20 | fits | 144,162 | 107 | 0.547 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 148,147 | 1.481 | 20 | 200 | fits | 151,419 | 189 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 743,221 | 7.432 | 20 | 200 | fits | 144,162 | 107 | 0.547 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 149,059 | 1.491 | 20 | 20 | fits | 151,419 | 189 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 852,992 | 8.530 | 20 | 20 | fits | 109,075 | 87 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 152,644 | 1.526 | 20 | 24 | fits | 151,419 | 189 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 856,427 | 8.564 | 20 | 24 | fits | 109,075 | 87 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 151,604 | 1.516 | 20 | 50 | fits | 151,419 | 189 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 746,897 | 7.469 | 20 | 50 | fits | 144,162 | 107 | 0.547 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 417,788 | 4.178 | 20 | 20 | fits | 124,684 | 52 | 0.562 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 600,655 | 6.007 | 20 | 20 | fits | 76,613 | 36 | 0.419 |
| LINK_UP | `adp.link_up.if0` | 2,398 | 0.024 | 20 | 200 | fits | 22,063 | 43 (11) | 0.708 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 16,941 | 0.169 | 20 | 200 | fits | 19,091 | 23 (39) | 0.696 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 4,859 | 0.049 | 20 | 200 | fits | 2,231 | 10 (11) | 0.429 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 615,556 | 6.156 | 20 | 200 | fits | 149,060 | 145 | 0.484 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 741,208 | 7.412 | 20 | 20 | fits | 145,789 | 118 | 0.368 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 298,820 | 2.988 | 20 | 24 | fits | 77,816 | 66 | 0.386 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 555,944 | 5.559 | 20 | 50 | fits | 149,060 | 145 | 0.484 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 384,859 | 3.849 | 20 | 20 | fits | 76,647 | 36 | 0.426 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 87,048 | 0.870 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 627,111 | 6.271 | 20 | 200 | fits | 151,692 | 150 | 0.491 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 753,276 | 7.533 | 20 | 20 | fits | 146,302 | 118 | 0.397 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 313,578 | 3.136 | 20 | 24 | fits | 80,506 | 72 | 0.413 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 567,499 | 5.675 | 20 | 50 | fits | 151,692 | 150 | 0.491 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 519,946 | 5.199 | 20 | 20 | fits | 154,176 | 188 | 0.440 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 88,157 | 0.882 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 16,108 | 0.161 | 20 | 20 | fits | 26,998 | 21 (35) | 0.797 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 13,506 | 0.135 | 20 | 20 | fits | 21,266 | 17 (14) | 0.847 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 10,599 | 0.106 | 20 | 20 | fits | 21,088 | 18 (14) | 0.839 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 13,189 | 0.132 | 20 | 20 | fits | 26,863 | 21 (35) | 0.791 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 78,027 | 0.780 | 20 | 20 | fits | 63,046 | 6 | 0.882 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 35,754 | 0.358 | 20 | 20 | fits | 35,819 | 12 | 0.888 |
| malformed MRPDU discard | `srp.malformed.if0` | 13,109 | 0.131 | 20 | 20 | fits | 13,174 | 12 | 0.479 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 80,280 | 0.803 | 220 | 220 | fits | 86,175 | 9 | 0.863 |
| an event behind 15 others | `backlog.event.if0` | 171,086 | 1.711 | 20 | 200 | fits | 82,567 | 108 | 0.517 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 491,060 | 4.911 | 20 | 20 | fits | 146,384 | 98 | 0.469 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 160,410 | 1.604 | 20 | 200 | fits | 160,618 | 217 | 0.481 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 339,676 | 3.397 | 20 | 200 | fits | 97,308 | 53 | 0.625 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 156,151 | 1.562 | 20 | 20 | fits | 160,618 | 217 | 0.481 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 545,891 | 5.459 | 20 | 20 | fits | 146,384 | 98 | 0.469 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 159,736 | 1.597 | 20 | 24 | fits | 160,618 | 217 | 0.481 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 600,114 | 6.001 | 20 | 24 | fits | 50,788 | 42 | 0.455 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 158,696 | 1.587 | 20 | 50 | fits | 160,618 | 217 | 0.481 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 338,181 | 3.382 | 20 | 50 | fits | 97,308 | 53 | 0.625 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 365,396 | 3.654 | 20 | 20 | fits | 24,053 | 53 | 0.222 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 400,407 | 4.004 | 20 | 20 | fits | 16,258 | 36 | 0.021 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 603,991 | 6.040 | 20 | 20 | fits | 149,639 | 152 | 0.513 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 138,773 | 1.388 | 20 | 200 | fits | 143,455 | 207 | 0.464 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 621,640 | 6.216 | 20 | 200 | fits | 149,639 | 152 | 0.513 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 139,685 | 1.397 | 20 | 20 | fits | 143,455 | 207 | 0.464 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 866,208 | 8.662 | 20 | 20 | fits | 93,965 | 73 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 143,270 | 1.433 | 20 | 24 | fits | 143,455 | 207 | 0.464 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 869,643 | 8.696 | 20 | 24 | fits | 93,965 | 73 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 142,230 | 1.422 | 20 | 50 | fits | 143,455 | 207 | 0.464 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 625,316 | 6.253 | 20 | 50 | fits | 149,639 | 152 | 0.513 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 275,106 | 2.751 | 20 | 20 | fits | 133,331 | 94 | 0.545 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 473,597 | 4.736 | 20 | 20 | fits | 78,422 | 37 | 0.485 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 11,153 | 0.112 | 20 | 20 | fits | 21,825 | 19 | 0.768 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 138,773 | 1.388 | 20 | 200 | fits | 143,455 | 207 | 0.464 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 26,569 | 0.266 | 20 | 200 | fits | 21,825 | 19 | 0.768 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 139,685 | 1.397 | 20 | 20 | fits | 143,455 | 207 | 0.464 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 774,908 | 7.749 | 20 | 20 | fits | 149,148 | 93 | 0.522 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 143,270 | 1.433 | 20 | 24 | fits | 143,455 | 207 | 0.464 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 857,742 | 8.577 | 20 | 24 | fits | 79,399 | 66 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 142,230 | 1.422 | 20 | 50 | fits | 143,455 | 207 | 0.464 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 628,740 | 6.287 | 20 | 50 | fits | 153,063 | 149 | 0.500 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 275,106 | 2.751 | 20 | 20 | fits | 133,331 | 94 | 0.545 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 473,597 | 4.736 | 20 | 20 | fits | 78,422 | 37 | 0.485 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,260,098 | 62.601 | 20 | 20 | MISS ceiling | 16,173 | 12 | 0.693 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,026,373 | 360.264 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,026,298 | 360.263 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,026,223 | 360.262 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,026,148 | 360.261 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 151,316 | 1.513 | 20 | 200 | fits | 143,541 | 182 | 0.492 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 628,025 | 6.280 | 20 | 200 | fits | 153,927 | 157 | 0.565 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 147,057 | 1.471 | 20 | 20 | fits | 143,541 | 182 | 0.492 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 663,966 | 6.640 | 20 | 20 | fits | 40,416 | 31 | 0.490 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 150,642 | 1.506 | 20 | 24 | fits | 143,541 | 182 | 0.492 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,177,166 | 61.772 | 20 | 24 | MISS ceiling | 150,753 | 123 | 0.348 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 149,602 | 1.496 | 20 | 50 | fits | 143,541 | 182 | 0.492 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 626,530 | 6.265 | 20 | 50 | fits | 153,927 | 157 | 0.565 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 283,796 | 2.838 | 20 | 20 | fits | 134,649 | 95 | 0.555 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 470,523 | 4.705 | 20 | 20 | fits | 78,525 | 37 | 0.474 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,002 | 0.050 | 20 | 20 | fits | 19,424 | 13 (29) | 0.750 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 6,283 | 0.063 | 20 | 20 | fits | 21,212 | 19 (35) | 0.756 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 16,421 | 0.164 | 20 | 20 | fits | 26,584 | 21 (12) | 0.788 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 11,448 | 0.114 | 20 | 50 | fits | 22,063 | 43 | 0.708 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 16,881 | 0.169 | 20 | 50 | fits | 18,612 | 35 | 0.673 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 8,902 | 0.089 | 20 | 50 | fits | 18,490 | 35 | 0.667 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 11,877 | 0.119 | 20 | 50 | fits | 24,784 | 61 | 0.614 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 13,956 | 0.140 | 20 | 50 | fits | 24,784 | 61 | 0.614 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 10,680 | 0.107 | 20 | 50 | fits | 17,771 | 30 | 0.587 |
| LINK_UP | `adp.link_up.if0` | 2,398 | 0.024 | 20 | 200 | fits | 22,063 | 43 (11) | 0.708 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 16,941 | 0.169 | 20 | 200 | fits | 19,091 | 23 (39) | 0.696 |
| LINK_DOWN | `adp.link_down.if0` | 2,114 | 0.021 | 20 | 200 | fits | 19,982 | 23 (9) | 0.702 |
| LINK_UP | `adp.link_up.if0` | 2,398 | 0.024 | 20 | 200 | fits | 22,063 | 43 (11) | 0.708 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 16,941 | 0.169 | 20 | 200 | fits | 19,091 | 23 (39) | 0.696 |
| GM_CHANGE | `adp.gm_change.if0` | 2,132 | 0.021 | 20 | 200 | fits | 10,717 | 17 (11) | 0.578 |
| LINK_UP | `adp.link_up.if0` | 2,398 | 0.024 | 20 | 200 | fits | 22,063 | 43 (11) | 0.708 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 16,941 | 0.169 | 20 | 200 | fits | 19,091 | 23 (39) | 0.696 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,862 | 0.049 | 20 | 200 | fits | 11,006 | 16 (31) | 0.491 |
| LINK_UP | `adp.link_up.if0` | 2,398 | 0.024 | 20 | 200 | fits | 22,063 | 43 (11) | 0.708 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 16,941 | 0.169 | 20 | 200 | fits | 19,091 | 23 (39) | 0.696 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,862 | 0.049 | 20 | 200 | fits | 11,006 | 16 (31) | 0.491 |
| set_name | `aecp_fanout.set_name.if0` | 49,412 | 0.494 | 20 | 24 | fits | 52,950 | 88 | 0.529 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 39,537 | 0.395 | 20 | 24 | fits | 47,910 | 77 | 0.564 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 43,468 | 0.435 | 20 | 24 | fits | 43,714 | 78 | 0.514 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 36,976 | 0.370 | 20 | 24 | fits | 43,939 | 77 | 0.522 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 46,944 | 0.469 | 20 | 24 | fits | 48,497 | 66 | 0.578 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 45,655 | 0.457 | 20 | 24 | fits | 47,232 | 65 | 0.566 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 35,276 | 0.353 | 20 | 24 | fits | 45,460 | 66 | 0.556 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 42,680 | 0.427 | 20 | 24 | fits | 42,857 | 77 | 0.502 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 37,918 | 0.379 | 20 | 24 | fits | 43,634 | 78 | 0.518 |
| BIND_RX | `acmp.bind_rx.if0` | 22,553 | 0.226 | 20 | 20 | fits | 40,735 | 26 (77) | 0.776 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 8,245 | 0.082 | 20 | 20 | fits | 25,566 | 20 (32) | 0.807 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 12,719 | 0.127 | 20 | 20 | fits | 26,769 | 15 (47) | 0.753 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 14,451 | 0.145 | 20 | 20 | fits | 34,107 | 18 (50) | 0.804 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 12,612 | 0.126 | 20 | 20 | fits | 25,686 | 18 (48) | 0.735 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 12,182 | 0.122 | 20 | 20 | fits | 24,969 | 16 (48) | 0.725 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 11,912 | 0.119 | 20 | 20 | fits | 23,567 | 16 (48) | 0.694 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 10,751 | 0.108 | 20 | 20 | fits | 23,591 | 16 (48) | 0.694 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 14,967 | 0.150 | 20 | 24 | fits | 22,382 | 20 | 0.756 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 18,302 | 0.183 | 20 | 24 | fits | 26,496 | 20 | 0.689 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 19,569 | 0.196 | 20 | 24 | fits | 21,283 | 20 | 0.690 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 14,770 | 0.148 | 20 | 24 | fits | 21,702 | 20 | 0.701 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 19,759 | 0.198 | 20 | 24 | fits | 21,926 | 20 | 0.689 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 15,317 | 0.153 | 20 | 24 | fits | 22,543 | 20 | 0.711 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 14,801 | 0.148 | 20 | 24 | fits | 21,711 | 20 | 0.708 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 19,254 | 0.193 | 20 | 24 | fits | 21,384 | 20 | 0.708 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 14,215 | 0.142 | 20 | 24 | fits | 21,317 | 20 | 0.724 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 20,924 | 0.209 | 20 | 24 | fits | 23,279 | 21 | 0.604 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 13,526 | 0.135 | 20 | 24 | fits | 20,875 | 20 | 0.747 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 17,655 | 0.177 | 20 | 24 | fits | 20,297 | 20 | 0.723 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 13,676 | 0.137 | 20 | 24 | fits | 21,635 | 20 | 0.714 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 19,602 | 0.196 | 20 | 24 | fits | 21,398 | 20 | 0.690 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 14,744 | 0.147 | 20 | 24 | fits | 21,772 | 20 | 0.726 |
| get_configuration | `aecp.get_configuration.if0` | 12,664 | 0.127 | 20 | 24 | fits | 19,286 | 20 | 0.725 |
| entity_available | `aecp.entity_available.if0` | 17,189 | 0.172 | 20 | 24 | fits | 18,913 | 20 | 0.703 |
| get_name | `aecp.get_name.if0` | 15,025 | 0.150 | 20 | 24 | fits | 22,726 | 20 | 0.757 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 21,015 | 0.210 | 20 | 24 | fits | 23,067 | 27 | 0.697 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 16,299 | 0.163 | 20 | 24 | fits | 23,755 | 29 | 0.745 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 17,160 | 0.172 | 20 | 24 | fits | 19,369 | 20 | 0.723 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 12,309 | 0.123 | 20 | 24 | fits | 19,203 | 20 | 0.725 |
| set_name | `aecp.set_name.if0` | 30,786 | 0.308 | 20 | 24 | fits | 36,076 | 42 | 0.730 |
| lock_entity | `aecp.lock_entity.if0` | 22,614 | 0.226 | 20 | 24 | fits | 29,448 | 33 | 0.767 |
| unlock_entity | `aecp.unlock_entity.if0` | 23,396 | 0.234 | 20 | 24 | fits | 28,437 | 32 | 0.761 |
| LINK_UP | `fixture.link_up.if0` | 2,398 | 0.024 | 20 | 200 | fits | 22,063 | 43 (11) | 0.708 |
| malformed MRPDU discard | `fixture.malformed.if0` | 14,144 | 0.141 | 20 | 20 | fits | 14,209 | 12 | 0.643 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 26,840 | 0.268 | 20 | 24 | fits | 36,123 | 42 | 0.729 |
| LINK_DOWN | `fixture.link_down.if0` | 2,660 | 0.027 | 20 | 200 | fits | 22,296 | 23 (9) | 0.742 |
| BIND_RX | `fixture.bind_rx.if0` | 22,258 | 0.223 | 20 | 20 | fits | 40,583 | 26 (77) | 0.775 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 23,876 | 0.239 | 20 | 20 | fits | 35,734 | 35 (35) | 0.740 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 5,688 | 0.057 | 20 | 20 | fits | 20,240 | 13 (29) | 0.774 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 78,941 | 0.789 | 20 | 200 | fits | 79,044 | 51 | 0.753 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 78,941 | 0.789 | 20 | 200 | fits | 79,044 | 51 | 0.753 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 78,671 | 0.787 | 20 | 20 | fits | 79,044 | 51 | 0.753 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 78,671 | 0.787 | 20 | 20 | fits | 79,044 | 51 | 0.753 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 78,876 | 0.789 | 20 | 24 | fits | 79,044 | 51 | 0.753 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 78,876 | 0.789 | 20 | 24 | fits | 79,044 | 51 | 0.753 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 78,811 | 0.788 | 20 | 50 | fits | 79,044 | 51 | 0.753 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 78,811 | 0.788 | 20 | 50 | fits | 79,044 | 51 | 0.753 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 78,746 | 0.787 | 20 | 20 | fits | 79,044 | 51 | 0.753 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 78,746 | 0.787 | 20 | 20 | fits | 79,044 | 51 | 0.753 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
