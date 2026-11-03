### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 86 paths and 6 of 415 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.212 (0.389) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.101 (0.236) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.057 (0.215) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.091 (0.335) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.114 (0.276) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.101 (0.236) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.111 (0.250) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.110 (0.255) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.070 (0.302) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.127 (0.368) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.166 (0.404) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.115 (0.370) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.114 (0.377) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.084 (0.407) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.099 (0.349) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.133 (0.335) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.029 (0.103) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.015 (0.093) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.019 (0.216) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.019 (0.538) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.056 (0.152) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.146 (0.325) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.156 (0.308) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.152 (0.303) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.099 (0.164) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.194 (0.354) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.129 (0.202) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.223 (0.419) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.159 (0.314) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.219 (0.377) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.125 (0.193) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.177 (0.335) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.114 (0.182) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.152 (0.223) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.163 (0.318) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.114 (0.182) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.174 (0.331) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.172 (0.328) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.129 (0.198) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.174 (0.331) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.133 (0.203) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.184 (0.344) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.118 (0.186) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.180 (0.333) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.212 (0.344) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 0.105 (0.173) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.189 (0.380) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 0.458 (0.651) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.510 (0.693) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.524 (0.764) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.438 (0.543) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.490 (0.739) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.510 (0.721) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.481 (0.721) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.460 (0.642) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.573 (3.898) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 3.546 (5.260) | fits | 7 adp | 25 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.135 (0.393) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 0.923 (1.500) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.069 (62.233) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.210 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.249 (0.357) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 4.547 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.851 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 6.102 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 2.941 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.671 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.172 (0.374) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.085 (0.155) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.106 (0.538) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.152 (0.374) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.123 (0.306) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.434 | fits | 0 acmp | 29 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 5.954 | fits | 11 acmp | 29 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.425 | fits | 0 adp | 29 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 4.427 | fits | 7 adp | 29 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.470 | fits | 0 aecp | 29 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.931 | MISS ceiling | 15 aecp | 29 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.459 | fits | 0 maap | 29 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 4.464 | fits | 6 maap | 29 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.872 | fits | 0 srp | 29 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.srp.last.if0` (backlog-adp@blank-0) | 11.463 | fits | 31 srp | 29 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.620 (0.724) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.341 (0.342) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.137 (0.138) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.819 (0.909) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 12.536 | 18 | 111,152 (1.112) | yes | - |
| backlog-adp@blank-1 | 0 | 11.830 | 18 | 111,065 (1.111) | yes | - |
| backlog-adp@blank-2 | 0 | 12.127 | 20 | 111,065 (1.111) | yes | - |
| backlog-adp@blank-3 | 0 | 11.918 | 18 | 111,089 (1.111) | yes | - |
| backlog-adp@blank-4 | 0 | 11.942 | 19 | 113,548 (1.135) | yes | - |
| backlog-adp@blank-5 | 0 | 11.810 | 18 | 111,079 (1.111) | yes | - |
| backlog-adp@blank-6 | 0 | 11.852 | 19 | 111,079 (1.111) | yes | - |
| backlog-adp@blank-7 | 0 | 13.769 | 21 | 121,795 (1.218) | yes | - |
| backlog-adp@program-0 | 0 | 12.125 | 19 | 110,636 (1.106) | yes | - |
| backlog-adp@program-1 | 0 | 11.933 | 18 | 113,127 (1.131) | yes | - |
| backlog-adp@program-2 | 0 | 11.839 | 18 | 110,662 (1.107) | yes | - |
| backlog-adp@program-3 | 0 | 12.216 | 19 | 106,543 (1.065) | yes | - |
| backlog-adp@program-4 | 0 | 11.163 | 18 | 106,661 (1.067) | yes | - |
| backlog-adp@program-5 | 0 | 11.059 | 18 | 110,750 (1.107) | yes | - |
| backlog-adp@program-6 | 0 | 11.086 | 18 | 110,806 (1.108) | yes | - |
| backlog-adp@program-7 | 0 | 11.198 | 18 | 109,419 (1.094) | yes | - |
| backlog-adp@verify-0 | 0 | 12.522 | 18 | 110,916 (1.109) | yes | - |
| backlog-adp@verify-1 | 0 | 11.821 | 18 | 110,940 (1.109) | yes | - |
| backlog-adp@verify-2 | 0 | 12.118 | 19 | 110,940 (1.109) | yes | - |
| backlog-adp@verify-3 | 0 | 11.913 | 18 | 110,916 (1.109) | yes | - |
| backlog-adp@verify-4 | 0 | 11.929 | 19 | 120,028 (1.200) | yes | - |
| backlog-adp@verify-5 | 0 | 11.874 | 18 | 110,930 (1.109) | yes | - |
| backlog-adp@verify-6 | 0 | 11.909 | 19 | 110,930 (1.109) | yes | - |
| backlog-adp@verify-7 | 0 | 12.774 | 19 | 106,643 (1.066) | yes | - |
| backlog | 0 | 6.768 | 19 | 82,336 (0.823) | yes | - |
| backlog-adp | 0 | 11.366 | 19 | 111,075 (1.111) | yes | - |
| backlog-adp-refill | 0 | 40.558 | 27 | 111,075 (1.111) | yes | - |
| backlog-owed | 0 | 360.261 | 64 | 108,122 (1.081) | yes | - |
| fixture | 0 | 1.023 | 2 | 75,544 (0.755) | yes | - |

Composed maximum over the 4 backlog windows: 111,075 CPU cycles (1.111 ms), backlog-adp.
Over the windows that released their whole load only: 111,075 (1.111 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 2462 | 0 | 121,602 (1.216) | fits |
| backlog-adp@blank-0 | 378 | 0 | 111,152 (1.112) | fits |
| backlog-adp@blank-1 | 378 | 0 | 111,065 (1.111) | fits |
| backlog-adp@blank-2 | 380 | 0 | 111,065 (1.111) | fits |
| backlog-adp@blank-3 | 378 | 0 | 111,089 (1.111) | fits |
| backlog-adp@blank-4 | 379 | 0 | 113,548 (1.135) | fits |
| backlog-adp@blank-5 | 379 | 0 | 111,079 (1.111) | fits |
| backlog-adp@blank-6 | 380 | 0 | 111,079 (1.111) | fits |
| backlog-adp@blank-7 | 382 | 0 | 121,795 (1.218) | fits |
| backlog-adp@program-0 | 449 | 0 | 120,828 (1.208) | fits |
| backlog-adp@program-1 | 448 | 0 | 120,828 (1.208) | fits |
| backlog-adp@program-2 | 449 | 0 | 120,828 (1.208) | fits |
| backlog-adp@program-3 | 450 | 0 | 120,828 (1.208) | fits |
| backlog-adp@program-4 | 450 | 0 | 120,828 (1.208) | fits |
| backlog-adp@program-5 | 451 | 0 | 120,828 (1.208) | fits |
| backlog-adp@program-6 | 451 | 0 | 120,828 (1.208) | fits |
| backlog-adp@program-7 | 451 | 0 | 120,828 (1.208) | fits |
| backlog-adp@verify-0 | 513 | 0 | 120,828 (1.208) | fits |
| backlog-adp@verify-1 | 513 | 0 | 120,828 (1.208) | fits |
| backlog-adp@verify-2 | 515 | 0 | 120,828 (1.208) | fits |
| backlog-adp@verify-3 | 513 | 0 | 120,828 (1.208) | fits |
| backlog-adp@verify-4 | 514 | 0 | 120,828 (1.208) | fits |
| backlog-adp@verify-5 | 515 | 0 | 120,828 (1.208) | fits |
| backlog-adp@verify-6 | 516 | 0 | 120,828 (1.208) | fits |
| backlog-adp@verify-7 | 516 | 0 | 120,828 (1.208) | fits |
| adp-advertise | 588 | 0 | 53,788 (0.538) | fits |
| save-held | 3411 | 0 | 90,013 (0.900) | fits |
| save-starved | 44390 | 0 | 92,144 (0.921) | fits |
| acmp-noresp | 1461 | 0 | 120,616 (1.206) | fits |
| save | 599 | 0 | 120,202 (1.202) | fits |
| srp | 282 | 0 | 72,360 (0.724) | fits |
| backlog | 291 | 0 | 82,336 (0.823) | fits |
| backlog-adp | 309 | 0 | 111,075 (1.111) | fits |
| backlog-adp-refill | 317 | 0 | 111,075 (1.111) | fits |
| backlog-owed | 347 | 0 | 108,122 (1.081) | fits |
| acmp-disc | 682 | 0 | 120,658 (1.207) | fits |
| maap | 173 | 0 | 53,788 (0.538) | fits |
| adp-link | 86 | 0 | 53,788 (0.538) | fits |
| adp-gm | 85 | 0 | 53,788 (0.538) | fits |
| adp-discover | 85 | 0 | 53,788 (0.538) | fits |
| control | 85 | 0 | 53,788 (0.538) | fits |
| aecp-fanout | 107 | 0 | 58,071 (0.581) | fits |
| acmp-cmd | 80 | 0 | 53,788 (0.538) | fits |
| aecp | 107 | 0 | 53,788 (0.538) | fits |
| fixture | 124 | 0 | 75,544 (0.755) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---|---|
| save-held | 2019.041 | 4,070 | 102 | 15.058 | no | within |
| save-starved | 4048.987 | 4,070 | 102 | 30.982 | yes | within |
| save | 2019.220 | 4,070 | 102 | 10.918 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 121,602 (1.216) | 95,279 (0.953) |
| backlog-adp@blank-0 | 299 | 85,674 (0.857) | 76,223 (0.762) |
| backlog-adp@blank-1 | 299 | 85,754 (0.858) | 76,223 (0.762) |
| backlog-adp@blank-2 | 299 | 85,754 (0.858) | 76,223 (0.762) |
| backlog-adp@blank-3 | 299 | 85,676 (0.857) | 76,254 (0.763) |
| backlog-adp@blank-4 | 299 | 85,730 (0.857) | 76,199 (0.762) |
| backlog-adp@blank-5 | 299 | 85,730 (0.857) | 76,199 (0.762) |
| backlog-adp@blank-6 | 299 | 85,730 (0.857) | 76,199 (0.762) |
| backlog-adp@blank-7 | 300 | 121,795 (1.218) | 76,498 (0.765) |
| backlog-adp@program-0 | 328 | 120,828 (1.208) | 81,653 (0.817) |
| backlog-adp@program-1 | 328 | 120,828 (1.208) | 81,653 (0.817) |
| backlog-adp@program-2 | 328 | 120,828 (1.208) | 81,653 (0.817) |
| backlog-adp@program-3 | 329 | 120,828 (1.208) | 81,653 (0.817) |
| backlog-adp@program-4 | 329 | 120,828 (1.208) | 80,631 (0.806) |
| backlog-adp@program-5 | 329 | 120,828 (1.208) | 80,631 (0.806) |
| backlog-adp@program-6 | 329 | 120,828 (1.208) | 80,631 (0.806) |
| backlog-adp@program-7 | 329 | 120,828 (1.208) | 80,631 (0.806) |
| backlog-adp@verify-0 | 355 | 120,828 (1.208) | 95,071 (0.951) |
| backlog-adp@verify-1 | 355 | 120,828 (1.208) | 95,071 (0.951) |
| backlog-adp@verify-2 | 355 | 120,828 (1.208) | 95,071 (0.951) |
| backlog-adp@verify-3 | 355 | 120,828 (1.208) | 95,071 (0.951) |
| backlog-adp@verify-4 | 355 | 120,828 (1.208) | 95,071 (0.951) |
| backlog-adp@verify-5 | 355 | 120,828 (1.208) | 95,071 (0.951) |
| backlog-adp@verify-6 | 355 | 120,828 (1.208) | 95,071 (0.951) |
| backlog-adp@verify-7 | 356 | 120,828 (1.208) | 95,071 (0.951) |
| adp-advertise | 577 | 46,483 (0.465) | 3,170 (0.032) |
| save-held | 722 | 102,855 (1.029) | 95,119 (0.951) |
| save-starved | 418 | 96,699 (0.967) | 96,151 (0.962) |
| acmp-noresp | 615 | 120,616 (1.206) | 95,071 (0.951) |
| save | 585 | 120,202 (1.202) | 95,184 (0.952) |
| srp | 271 | 46,380 (0.464) | 3,170 (0.032) |
| backlog | 265 | 46,380 (0.464) | 3,170 (0.032) |
| backlog-adp | 271 | 46,380 (0.464) | 3,170 (0.032) |
| backlog-adp-refill | 274 | 46,380 (0.464) | 3,170 (0.032) |
| backlog-owed | 306 | 48,458 (0.485) | 3,170 (0.032) |
| acmp-disc | 305 | 120,658 (1.207) | 95,071 (0.951) |
| maap | 166 | 46,380 (0.464) | 3,170 (0.032) |
| adp-link | 80 | 37,791 (0.378) | 3,024 (0.030) |
| adp-gm | 80 | 37,791 (0.378) | 3,024 (0.030) |
| adp-discover | 80 | 37,791 (0.378) | 3,024 (0.030) |
| control | 80 | 37,791 (0.378) | 3,024 (0.030) |
| aecp-fanout | 79 | 37,791 (0.378) | 3,024 (0.030) |
| acmp-cmd | 65 | 37,791 (0.378) | 3,024 (0.030) |
| aecp | 78 | 37,791 (0.378) | 3,024 (0.030) |
| fixture | 54 | 9,991 (0.100) | 2,296 (0.023) |

Longest pass that carries a step: 121,795 CPU cycles (1.218 ms), backlog-adp@blank-7; longest step: 96,151 (0.962 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 8,371 | 0.084 | 20 | 20 | fits | 27,784 | 20 (14) | 0.882 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 354,586 | 3.546 | 20 | 20 | fits | 96,339 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 142,490 | 1.425 | 20 | 200 | fits | 77,947 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 442,697 | 4.427 | 20 | 200 | fits | 96,339 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 143,402 | 1.434 | 20 | 20 | fits | 77,947 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 595,384 | 5.954 | 20 | 20 | fits | 74,675 | 51 | 0.702 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 146,987 | 1.470 | 20 | 24 | fits | 77,947 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 1,090,856 | 10.909 | 20 | 24 | fits | 48,463 | 29 | 0.740 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 145,947 | 1.459 | 20 | 50 | fits | 77,947 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 446,373 | 4.464 | 20 | 50 | fits | 96,339 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 256,644 | 2.566 | 18 | 18 | fits | 111,152 | 138 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,146,265 | 11.463 | 18 | 18 | fits | 24,044 | 14 | 0.823 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 290,152 | 2.902 | 20 | 20 | fits | 96,339 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 78,093 | 0.781 | 20 | 200 | fits | 77,280 | 135 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 378,263 | 3.783 | 20 | 200 | fits | 96,339 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 79,005 | 0.790 | 20 | 20 | fits | 77,280 | 135 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 543,759 | 5.438 | 20 | 20 | fits | 81,168 | 50 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 82,590 | 0.826 | 20 | 24 | fits | 77,280 | 135 | 0.501 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 1,011,713 | 10.117 | 20 | 24 | fits | 48,412 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 81,550 | 0.816 | 20 | 50 | fits | 77,280 | 135 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 381,939 | 3.819 | 20 | 50 | fits | 96,339 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 192,160 | 1.922 | 18 | 18 | fits | 111,065 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 1,075,558 | 10.756 | 18 | 18 | fits | 32,503 | 17 | 0.791 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 286,546 | 2.865 | 20 | 20 | fits | 77,777 | 83 | 0.616 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 74,487 | 0.745 | 20 | 200 | fits | 77,280 | 135 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 356,095 | 3.561 | 20 | 200 | fits | 77,777 | 83 | 0.616 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 75,399 | 0.754 | 20 | 20 | fits | 77,280 | 135 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 514,530 | 5.145 | 20 | 20 | fits | 77,257 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 78,984 | 0.790 | 20 | 24 | fits | 77,280 | 135 | 0.501 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 981,898 | 9.819 | 20 | 24 | fits | 48,412 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 77,944 | 0.779 | 20 | 50 | fits | 77,280 | 135 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 359,771 | 3.598 | 20 | 50 | fits | 77,777 | 83 | 0.616 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 188,554 | 1.886 | 18 | 18 | fits | 111,065 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 1,078,207 | 10.782 | 18 | 18 | fits | 32,364 | 17 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 302,722 | 3.027 | 20 | 20 | fits | 96,565 | 81 | 0.659 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 79,629 | 0.796 | 20 | 200 | fits | 77,357 | 135 | 0.502 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 391,035 | 3.910 | 20 | 200 | fits | 96,565 | 81 | 0.659 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 80,541 | 0.805 | 20 | 20 | fits | 77,357 | 135 | 0.502 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 545,683 | 5.457 | 20 | 20 | fits | 76,704 | 44 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 84,126 | 0.841 | 20 | 24 | fits | 77,357 | 135 | 0.502 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 1,017,843 | 10.178 | 20 | 24 | fits | 30,740 | 31 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 83,086 | 0.831 | 20 | 50 | fits | 77,357 | 135 | 0.502 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 394,711 | 3.947 | 20 | 50 | fits | 96,565 | 81 | 0.659 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 193,720 | 1.937 | 18 | 18 | fits | 111,089 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 1,084,384 | 10.844 | 18 | 18 | fits | 32,637 | 17 | 0.795 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 296,182 | 2.962 | 20 | 20 | fits | 96,378 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 81,563 | 0.816 | 20 | 200 | fits | 82,897 | 146 | 0.523 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 384,369 | 3.844 | 20 | 200 | fits | 96,378 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 82,475 | 0.825 | 20 | 20 | fits | 82,897 | 146 | 0.523 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 515,959 | 5.160 | 20 | 20 | fits | 53,419 | 35 | 0.624 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 86,060 | 0.861 | 20 | 24 | fits | 82,897 | 146 | 0.523 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 990,944 | 9.909 | 20 | 24 | fits | 48,427 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 85,020 | 0.850 | 20 | 50 | fits | 82,897 | 146 | 0.523 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 388,045 | 3.880 | 20 | 50 | fits | 96,378 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 198,113 | 1.981 | 18 | 18 | fits | 113,548 | 143 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 1,086,717 | 10.867 | 18 | 18 | fits | 32,132 | 17 | 0.788 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 291,590 | 2.916 | 20 | 20 | fits | 72,237 | 72 | 0.600 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 79,567 | 0.796 | 20 | 200 | fits | 77,072 | 135 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 355,599 | 3.556 | 20 | 200 | fits | 72,237 | 72 | 0.600 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 80,479 | 0.805 | 20 | 20 | fits | 77,072 | 135 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 513,930 | 5.139 | 20 | 20 | fits | 76,937 | 44 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 84,064 | 0.841 | 20 | 24 | fits | 77,072 | 135 | 0.501 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 1,009,774 | 10.098 | 20 | 24 | fits | 48,331 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 83,024 | 0.830 | 20 | 50 | fits | 77,072 | 135 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 359,275 | 3.593 | 20 | 50 | fits | 72,237 | 72 | 0.600 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 193,648 | 1.936 | 18 | 18 | fits | 111,079 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 1,073,726 | 10.737 | 18 | 18 | fits | 32,595 | 17 | 0.794 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 267,429 | 2.674 | 20 | 20 | fits | 99,115 | 87 | 0.657 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 76,052 | 0.761 | 20 | 200 | fits | 77,072 | 135 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 355,085 | 3.551 | 20 | 200 | fits | 99,115 | 87 | 0.657 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 76,964 | 0.770 | 20 | 20 | fits | 77,072 | 135 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 509,902 | 5.099 | 20 | 20 | fits | 76,724 | 44 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 80,549 | 0.805 | 20 | 24 | fits | 77,072 | 135 | 0.501 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 981,484 | 9.815 | 20 | 24 | fits | 48,404 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 79,509 | 0.795 | 20 | 50 | fits | 77,072 | 135 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 358,761 | 3.588 | 20 | 50 | fits | 99,115 | 87 | 0.657 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 190,133 | 1.901 | 18 | 18 | fits | 111,079 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 1,077,769 | 10.778 | 18 | 18 | fits | 32,356 | 17 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 261,651 | 2.617 | 20 | 20 | fits | 97,044 | 81 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 72,446 | 0.724 | 20 | 200 | fits | 77,072 | 135 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 350,430 | 3.504 | 20 | 200 | fits | 97,044 | 81 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 73,358 | 0.734 | 20 | 20 | fits | 77,072 | 135 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 511,589 | 5.116 | 20 | 20 | fits | 82,976 | 55 | 0.696 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 76,943 | 0.769 | 20 | 24 | fits | 77,072 | 135 | 0.501 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 1,002,945 | 10.029 | 20 | 24 | fits | 48,331 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 75,903 | 0.759 | 20 | 50 | fits | 77,072 | 135 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 354,106 | 3.541 | 20 | 50 | fits | 97,044 | 81 | 0.662 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 256,997 | 2.570 | 18 | 18 | fits | 106,808 | 102 | 0.652 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 1,066,897 | 10.669 | 18 | 18 | fits | 32,595 | 17 | 0.794 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 288,207 | 2.882 | 20 | 20 | fits | 77,777 | 83 | 0.616 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 76,512 | 0.765 | 20 | 200 | fits | 77,692 | 135 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 357,756 | 3.578 | 20 | 200 | fits | 77,777 | 83 | 0.616 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 77,424 | 0.774 | 20 | 20 | fits | 77,692 | 135 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 516,191 | 5.162 | 20 | 20 | fits | 77,257 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 81,009 | 0.810 | 20 | 24 | fits | 77,692 | 135 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 1,008,582 | 10.086 | 20 | 24 | fits | 48,536 | 29 | 0.740 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 79,969 | 0.800 | 20 | 50 | fits | 77,692 | 135 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 361,432 | 3.614 | 20 | 50 | fits | 77,777 | 83 | 0.616 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 190,150 | 1.901 | 18 | 18 | fits | 110,636 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 1,072,527 | 10.725 | 18 | 18 | fits | 32,603 | 17 | 0.794 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 297,776 | 2.978 | 20 | 20 | fits | 96,346 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 83,513 | 0.835 | 20 | 200 | fits | 83,234 | 146 | 0.533 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 385,931 | 3.859 | 20 | 200 | fits | 96,346 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 84,425 | 0.844 | 20 | 20 | fits | 83,234 | 146 | 0.533 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 540,897 | 5.409 | 20 | 20 | fits | 76,863 | 44 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 88,010 | 0.880 | 20 | 24 | fits | 83,234 | 146 | 0.533 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 1,017,190 | 10.172 | 20 | 24 | fits | 48,232 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 86,970 | 0.870 | 20 | 50 | fits | 83,234 | 146 | 0.533 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 389,607 | 3.896 | 20 | 50 | fits | 96,346 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 199,642 | 1.996 | 18 | 18 | fits | 113,127 | 143 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 1,080,726 | 10.807 | 18 | 18 | fits | 32,387 | 17 | 0.791 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 289,803 | 2.898 | 20 | 20 | fits | 96,307 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 78,132 | 0.781 | 20 | 200 | fits | 77,549 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 377,882 | 3.779 | 20 | 200 | fits | 96,307 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 79,044 | 0.790 | 20 | 20 | fits | 77,549 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 512,120 | 5.121 | 20 | 20 | fits | 79,720 | 50 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 82,629 | 0.826 | 20 | 24 | fits | 77,549 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 1,007,379 | 10.074 | 20 | 24 | fits | 48,153 | 29 | 0.737 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 81,589 | 0.816 | 20 | 50 | fits | 77,549 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 381,558 | 3.816 | 20 | 50 | fits | 96,307 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 191,796 | 1.918 | 18 | 18 | fits | 110,662 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 1,071,347 | 10.713 | 18 | 18 | fits | 32,603 | 17 | 0.794 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 268,499 | 2.685 | 20 | 20 | fits | 103,269 | 92 | 0.675 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 79,514 | 0.795 | 20 | 200 | fits | 77,472 | 135 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 363,503 | 3.635 | 20 | 200 | fits | 103,269 | 92 | 0.675 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 80,426 | 0.804 | 20 | 20 | fits | 77,472 | 135 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 523,162 | 5.232 | 20 | 20 | fits | 77,224 | 44 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 84,011 | 0.840 | 20 | 24 | fits | 77,472 | 135 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 1,011,176 | 10.112 | 20 | 24 | fits | 48,412 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 82,971 | 0.830 | 20 | 50 | fits | 77,472 | 135 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 367,179 | 3.672 | 20 | 50 | fits | 103,269 | 92 | 0.675 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 263,845 | 2.638 | 18 | 18 | fits | 106,543 | 102 | 0.652 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 1,075,121 | 10.751 | 18 | 18 | fits | 32,603 | 17 | 0.794 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 271,521 | 2.715 | 20 | 20 | fits | 97,529 | 81 | 0.666 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 76,862 | 0.769 | 20 | 200 | fits | 77,619 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 360,752 | 3.608 | 20 | 200 | fits | 97,529 | 81 | 0.666 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 77,774 | 0.778 | 20 | 20 | fits | 77,619 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 516,237 | 5.162 | 20 | 20 | fits | 76,969 | 44 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 81,359 | 0.814 | 20 | 24 | fits | 77,619 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 1,016,448 | 10.164 | 20 | 24 | fits | 48,396 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 80,319 | 0.803 | 20 | 50 | fits | 77,619 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 364,428 | 3.644 | 20 | 50 | fits | 97,529 | 81 | 0.666 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 266,834 | 2.668 | 18 | 18 | fits | 106,661 | 102 | 0.659 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 1,080,416 | 10.804 | 18 | 18 | fits | 32,603 | 17 | 0.794 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 288,826 | 2.888 | 20 | 20 | fits | 96,307 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 77,017 | 0.770 | 20 | 200 | fits | 77,505 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 376,905 | 3.769 | 20 | 200 | fits | 96,307 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 77,929 | 0.779 | 20 | 20 | fits | 77,505 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 531,553 | 5.316 | 20 | 20 | fits | 76,704 | 44 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 81,514 | 0.815 | 20 | 24 | fits | 77,505 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 1,005,968 | 10.060 | 20 | 24 | fits | 48,412 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 80,474 | 0.805 | 20 | 50 | fits | 77,505 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 380,581 | 3.806 | 20 | 50 | fits | 96,307 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 190,769 | 1.908 | 18 | 18 | fits | 110,750 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 1,069,913 | 10.699 | 18 | 18 | fits | 32,603 | 17 | 0.794 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 290,214 | 2.902 | 20 | 20 | fits | 96,307 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 78,399 | 0.784 | 20 | 200 | fits | 77,428 | 135 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 378,293 | 3.783 | 20 | 200 | fits | 96,307 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 79,311 | 0.793 | 20 | 20 | fits | 77,428 | 135 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 520,707 | 5.207 | 20 | 20 | fits | 82,391 | 56 | 0.691 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 82,896 | 0.829 | 20 | 24 | fits | 77,428 | 135 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 1,008,772 | 10.088 | 20 | 24 | fits | 48,412 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 81,856 | 0.819 | 20 | 50 | fits | 77,428 | 135 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 381,969 | 3.820 | 20 | 50 | fits | 96,307 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 192,207 | 1.922 | 18 | 18 | fits | 110,806 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 1,072,617 | 10.726 | 18 | 18 | fits | 32,503 | 17 | 0.791 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 277,346 | 2.773 | 20 | 20 | fits | 97,461 | 81 | 0.666 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 79,935 | 0.799 | 20 | 200 | fits | 77,505 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 366,542 | 3.665 | 20 | 200 | fits | 97,461 | 81 | 0.666 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 80,847 | 0.808 | 20 | 20 | fits | 77,505 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 522,027 | 5.220 | 20 | 20 | fits | 76,969 | 44 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 84,432 | 0.844 | 20 | 24 | fits | 77,505 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 1,019,878 | 10.199 | 20 | 24 | fits | 52,252 | 35 | 0.758 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 83,392 | 0.834 | 20 | 50 | fits | 77,505 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 370,218 | 3.702 | 20 | 50 | fits | 97,461 | 81 | 0.666 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 272,692 | 2.727 | 18 | 18 | fits | 109,419 | 108 | 0.658 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 1,083,768 | 10.838 | 18 | 18 | fits | 32,603 | 17 | 0.794 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 352,644 | 3.526 | 20 | 20 | fits | 96,339 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 140,719 | 1.407 | 20 | 200 | fits | 78,222 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 440,755 | 4.408 | 20 | 200 | fits | 96,339 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 141,631 | 1.416 | 20 | 20 | fits | 78,222 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 593,442 | 5.934 | 20 | 20 | fits | 74,675 | 51 | 0.702 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 145,216 | 1.452 | 20 | 24 | fits | 78,222 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 1,088,890 | 10.889 | 20 | 24 | fits | 48,463 | 29 | 0.740 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 144,176 | 1.442 | 20 | 50 | fits | 78,222 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 444,431 | 4.444 | 20 | 50 | fits | 96,339 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 254,637 | 2.546 | 18 | 18 | fits | 110,916 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,144,299 | 11.443 | 18 | 18 | fits | 24,044 | 14 | 0.823 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 288,598 | 2.886 | 20 | 20 | fits | 96,339 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 76,599 | 0.766 | 20 | 200 | fits | 77,753 | 135 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 376,709 | 3.767 | 20 | 200 | fits | 96,339 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 77,511 | 0.775 | 20 | 20 | fits | 77,753 | 135 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 542,205 | 5.422 | 20 | 20 | fits | 81,168 | 50 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 81,096 | 0.811 | 20 | 24 | fits | 77,753 | 135 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 1,010,215 | 10.102 | 20 | 24 | fits | 48,412 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 80,056 | 0.801 | 20 | 50 | fits | 77,753 | 135 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 380,385 | 3.804 | 20 | 50 | fits | 96,339 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 190,541 | 1.905 | 18 | 18 | fits | 110,940 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 1,074,060 | 10.741 | 18 | 18 | fits | 32,503 | 17 | 0.791 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 284,992 | 2.850 | 20 | 20 | fits | 77,777 | 83 | 0.616 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 72,993 | 0.730 | 20 | 200 | fits | 77,753 | 135 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 354,541 | 3.545 | 20 | 200 | fits | 77,777 | 83 | 0.616 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 73,905 | 0.739 | 20 | 20 | fits | 77,753 | 135 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 512,976 | 5.130 | 20 | 20 | fits | 77,257 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 77,490 | 0.775 | 20 | 24 | fits | 77,753 | 135 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 980,400 | 9.804 | 20 | 24 | fits | 48,412 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 76,450 | 0.764 | 20 | 50 | fits | 77,753 | 135 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 358,217 | 3.582 | 20 | 50 | fits | 77,777 | 83 | 0.616 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 186,935 | 1.869 | 18 | 18 | fits | 110,940 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 1,076,709 | 10.767 | 18 | 18 | fits | 32,364 | 17 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 273,411 | 2.734 | 20 | 20 | fits | 98,851 | 87 | 0.663 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 77,981 | 0.780 | 20 | 200 | fits | 77,676 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 362,212 | 3.622 | 20 | 200 | fits | 98,851 | 87 | 0.663 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 78,893 | 0.789 | 20 | 20 | fits | 77,676 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 517,696 | 5.177 | 20 | 20 | fits | 76,989 | 44 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 82,478 | 0.825 | 20 | 24 | fits | 77,676 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 1,016,335 | 10.163 | 20 | 24 | fits | 54,394 | 40 | 0.749 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 81,438 | 0.814 | 20 | 50 | fits | 77,676 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 365,888 | 3.659 | 20 | 50 | fits | 98,851 | 87 | 0.663 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 191,899 | 1.919 | 18 | 18 | fits | 110,916 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 1,083,289 | 10.833 | 18 | 18 | fits | 32,603 | 17 | 0.794 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 295,449 | 2.954 | 20 | 20 | fits | 96,331 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 74,375 | 0.744 | 20 | 200 | fits | 77,676 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 383,528 | 3.835 | 20 | 200 | fits | 96,331 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 75,287 | 0.753 | 20 | 20 | fits | 77,676 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 514,626 | 5.146 | 20 | 20 | fits | 53,154 | 35 | 0.620 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 78,872 | 0.789 | 20 | 24 | fits | 77,676 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 988,456 | 9.885 | 20 | 24 | fits | 48,534 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 77,832 | 0.778 | 20 | 50 | fits | 77,676 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 387,204 | 3.872 | 20 | 50 | fits | 96,331 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 197,405 | 1.974 | 18 | 18 | fits | 120,028 | 155 | 0.638 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 1,084,842 | 10.848 | 18 | 18 | fits | 32,364 | 17 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 289,288 | 2.893 | 20 | 20 | fits | 88,109 | 77 | 0.659 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 77,349 | 0.773 | 20 | 200 | fits | 77,468 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 369,169 | 3.692 | 20 | 200 | fits | 88,109 | 77 | 0.659 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 78,261 | 0.783 | 20 | 20 | fits | 77,468 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 528,475 | 5.285 | 20 | 20 | fits | 76,921 | 44 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 81,846 | 0.818 | 20 | 24 | fits | 77,468 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 1,015,474 | 10.155 | 20 | 24 | fits | 48,339 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 80,806 | 0.808 | 20 | 50 | fits | 77,468 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 372,845 | 3.728 | 20 | 50 | fits | 88,109 | 77 | 0.659 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 191,281 | 1.913 | 18 | 18 | fits | 110,930 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 1,079,442 | 10.794 | 18 | 18 | fits | 32,603 | 17 | 0.794 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 265,036 | 2.650 | 20 | 20 | fits | 99,115 | 87 | 0.657 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 73,743 | 0.737 | 20 | 200 | fits | 77,468 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 352,692 | 3.527 | 20 | 200 | fits | 99,115 | 87 | 0.657 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 74,655 | 0.747 | 20 | 20 | fits | 77,468 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 507,509 | 5.075 | 20 | 20 | fits | 76,724 | 44 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 78,240 | 0.782 | 20 | 24 | fits | 77,468 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 995,011 | 9.950 | 20 | 24 | fits | 48,339 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 77,200 | 0.772 | 20 | 50 | fits | 77,468 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 356,368 | 3.564 | 20 | 50 | fits | 99,115 | 87 | 0.657 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 187,675 | 1.877 | 18 | 18 | fits | 110,930 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 1,082,884 | 10.829 | 18 | 18 | fits | 23,905 | 14 | 0.822 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 267,946 | 2.679 | 20 | 20 | fits | 97,159 | 81 | 0.663 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 78,885 | 0.789 | 20 | 200 | fits | 77,545 | 135 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 356,840 | 3.568 | 20 | 200 | fits | 97,159 | 81 | 0.663 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 79,797 | 0.798 | 20 | 20 | fits | 77,545 | 135 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 517,999 | 5.180 | 20 | 20 | fits | 82,976 | 55 | 0.696 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 83,382 | 0.834 | 20 | 24 | fits | 77,545 | 135 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 1,009,342 | 10.093 | 20 | 24 | fits | 48,339 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 82,342 | 0.823 | 20 | 50 | fits | 77,545 | 135 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 360,516 | 3.605 | 20 | 50 | fits | 97,159 | 81 | 0.663 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 263,292 | 2.633 | 18 | 18 | fits | 106,643 | 102 | 0.651 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 1,073,310 | 10.733 | 18 | 18 | fits | 32,603 | 17 | 0.794 |
| LINK_UP | `adp.link_up.if0` | 1,912 | 0.019 | 20 | 200 | fits | 53,788 | 49 (11) | 0.738 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 14,585 | 0.146 | 20 | 200 | fits | 18,665 | 31 (39) | 0.573 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 5,584 | 0.056 | 20 | 200 | fits | 3,717 | 15 (11) | 0.292 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 276,364 | 2.764 | 20 | 200 | fits | 73,083 | 84 | 0.569 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 438,732 | 4.387 | 20 | 20 | fits | 58,470 | 32 | 0.701 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 556,731 | 5.567 | 20 | 24 | fits | 22,138 | 21 | 0.600 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 281,970 | 2.820 | 20 | 50 | fits | 65,218 | 55 | 0.656 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 808,806 | 8.088 | 18 | 18 | fits | 47,895 | 29 | 0.737 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 285,099 | 2.851 | 20 | 200 | fits | 76,499 | 90 | 0.597 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 454,667 | 4.547 | 20 | 20 | fits | 59,936 | 38 | 0.695 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 610,192 | 6.102 | 20 | 24 | fits | 24,871 | 27 | 0.642 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 294,069 | 2.941 | 20 | 50 | fits | 68,582 | 61 | 0.678 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 867,093 | 8.671 | 18 | 18 | fits | 53,114 | 41 | 0.739 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 11,470 | 0.115 | 20 | 20 | fits | 25,898 | 23 (35) | 0.763 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 11,363 | 0.114 | 20 | 20 | fits | 20,313 | 18 (14) | 0.837 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 9,858 | 0.099 | 20 | 20 | fits | 19,977 | 19 (14) | 0.825 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 12,703 | 0.127 | 20 | 20 | fits | 26,464 | 23 (35) | 0.776 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 81,901 | 0.819 | 18 | 18 | fits | 37,076 | 13 | 0.845 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 34,123 | 0.341 | 18 | 18 | fits | 34,188 | 14 | 0.889 |
| malformed MRPDU discard | `srp.malformed.if0` | 12,891 | 0.129 | 18 | 18 | fits | 12,956 | 14 | 0.600 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 62,021 | 0.620 | 218 | 218 | fits | 72,360 | 21 | 0.865 |
| an event behind 15 others | `backlog.event.if0` | 92,317 | 0.923 | 20 | 200 | fits | 67,677 | 104 | 0.513 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 357,266 | 3.573 | 20 | 20 | fits | 49,798 | 44 | 0.514 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 82,128 | 0.821 | 20 | 200 | fits | 82,336 | 138 | 0.509 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 288,742 | 2.887 | 20 | 200 | fits | 58,246 | 55 | 0.543 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 77,869 | 0.779 | 20 | 20 | fits | 82,336 | 138 | 0.509 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 384,473 | 3.845 | 20 | 20 | fits | 49,798 | 44 | 0.514 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 81,454 | 0.815 | 20 | 24 | fits | 82,336 | 138 | 0.509 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 622,162 | 6.222 | 20 | 24 | fits | 23,362 | 29 | 0.488 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 80,414 | 0.804 | 20 | 50 | fits | 82,336 | 138 | 0.509 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 287,247 | 2.872 | 20 | 50 | fits | 58,246 | 55 | 0.543 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 287,182 | 2.872 | 18 | 18 | fits | 58,246 | 55 | 0.543 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 649,165 | 6.492 | 18 | 18 | fits | 9,337 | 17 | 0.304 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 283,419 | 2.834 | 20 | 20 | fits | 77,475 | 83 | 0.614 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 71,638 | 0.716 | 20 | 200 | fits | 76,320 | 135 | 0.487 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 352,782 | 3.528 | 20 | 200 | fits | 77,475 | 83 | 0.614 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 72,550 | 0.726 | 20 | 20 | fits | 76,320 | 135 | 0.487 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 511,170 | 5.112 | 20 | 20 | fits | 77,252 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 76,135 | 0.761 | 20 | 24 | fits | 76,320 | 135 | 0.487 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 1,003,511 | 10.035 | 20 | 24 | fits | 48,407 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 75,095 | 0.751 | 20 | 50 | fits | 76,320 | 135 | 0.487 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 356,458 | 3.565 | 20 | 50 | fits | 77,475 | 83 | 0.614 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 185,715 | 1.857 | 18 | 18 | fits | 111,075 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,067,446 | 10.674 | 18 | 18 | fits | 32,598 | 17 | 0.794 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 13,526 | 0.135 | 20 | 20 | fits | 21,890 | 20 | 0.761 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 71,638 | 0.716 | 20 | 200 | fits | 76,320 | 135 | 0.487 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 29,247 | 0.292 | 20 | 200 | fits | 21,890 | 20 | 0.761 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 72,550 | 0.726 | 20 | 20 | fits | 76,320 | 135 | 0.487 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 501,130 | 5.011 | 20 | 20 | fits | 77,161 | 44 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 76,135 | 0.761 | 20 | 24 | fits | 76,320 | 135 | 0.487 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 993,469 | 9.935 | 20 | 24 | fits | 48,407 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 75,095 | 0.751 | 20 | 50 | fits | 76,320 | 135 | 0.487 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 346,746 | 3.467 | 20 | 50 | fits | 67,763 | 73 | 0.606 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 185,715 | 1.857 | 18 | 18 | fits | 111,075 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,058,835 | 10.588 | 18 | 18 | fits | 34,029 | 21 | 0.747 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,206,949 | 62.069 | 20 | 20 | MISS ceiling | 28,855 | 25 | 0.613 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,021,006 | 360.210 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,020,931 | 360.209 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,020,856 | 360.209 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,020,781 | 360.208 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 76,810 | 0.768 | 20 | 200 | fits | 72,722 | 129 | 0.484 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 358,166 | 3.582 | 20 | 200 | fits | 83,675 | 67 | 0.667 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 72,551 | 0.726 | 20 | 20 | fits | 72,722 | 129 | 0.484 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 475,235 | 4.752 | 20 | 20 | fits | 59,140 | 33 | 0.763 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 76,136 | 0.761 | 20 | 24 | fits | 72,722 | 129 | 0.484 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,293,111 | 62.931 | 20 | 24 | MISS ceiling | 22,143 | 21 | 0.600 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 75,096 | 0.751 | 20 | 50 | fits | 72,722 | 129 | 0.484 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 356,671 | 3.567 | 20 | 50 | fits | 83,675 | 67 | 0.667 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 182,763 | 1.828 | 18 | 18 | fits | 108,122 | 131 | 0.642 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 837,544 | 8.375 | 18 | 18 | fits | 32,499 | 20 | 0.788 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 4,352 | 0.044 | 20 | 20 | fits | 19,517 | 14 (29) | 0.748 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 5,655 | 0.057 | 20 | 20 | fits | 21,457 | 20 (35) | 0.761 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 16,590 | 0.166 | 20 | 20 | fits | 25,944 | 23 (12) | 0.763 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 10,597 | 0.106 | 20 | 50 | fits | 53,788 | 49 | 0.738 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 12,307 | 0.123 | 20 | 50 | fits | 16,918 | 37 | 0.639 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 8,359 | 0.084 | 20 | 50 | fits | 16,553 | 37 | 0.625 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 15,185 | 0.152 | 20 | 50 | fits | 25,338 | 70 | 0.569 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 17,181 | 0.172 | 20 | 50 | fits | 25,338 | 70 | 0.569 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 8,490 | 0.085 | 20 | 50 | fits | 15,475 | 32 | 0.547 |
| LINK_UP | `adp.link_up.if0` | 1,912 | 0.019 | 20 | 200 | fits | 53,788 | 49 (11) | 0.738 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 14,585 | 0.146 | 20 | 200 | fits | 18,665 | 31 (39) | 0.573 |
| LINK_DOWN | `adp.link_down.if0` | 1,542 | 0.015 | 20 | 200 | fits | 19,941 | 22 (9) | 0.758 |
| LINK_UP | `adp.link_up.if0` | 1,912 | 0.019 | 20 | 200 | fits | 53,788 | 49 (11) | 0.738 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 14,585 | 0.146 | 20 | 200 | fits | 18,665 | 31 (39) | 0.573 |
| GM_CHANGE | `adp.gm_change.if0` | 1,483 | 0.015 | 20 | 200 | fits | 9,266 | 18 (11) | 0.512 |
| LINK_UP | `adp.link_up.if0` | 1,912 | 0.019 | 20 | 200 | fits | 53,788 | 49 (11) | 0.738 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 14,585 | 0.146 | 20 | 200 | fits | 18,665 | 31 (39) | 0.573 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 2,866 | 0.029 | 20 | 200 | fits | 10,297 | 17 (31) | 0.547 |
| LINK_UP | `adp.link_up.if0` | 1,912 | 0.019 | 20 | 200 | fits | 53,788 | 49 (11) | 0.738 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 14,585 | 0.146 | 20 | 200 | fits | 18,665 | 31 (39) | 0.573 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 2,866 | 0.029 | 20 | 200 | fits | 10,297 | 17 (31) | 0.547 |
| set_name | `aecp_fanout.set_name.if0` | 51,011 | 0.510 | 20 | 24 | fits | 58,071 | 121 | 0.378 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 43,796 | 0.438 | 20 | 24 | fits | 54,261 | 117 | 0.435 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 48,991 | 0.490 | 20 | 24 | fits | 48,513 | 111 | 0.355 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 41,845 | 0.418 | 20 | 24 | fits | 46,003 | 111 | 0.362 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 52,354 | 0.524 | 20 | 24 | fits | 52,961 | 99 | 0.402 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 45,776 | 0.458 | 20 | 24 | fits | 50,976 | 99 | 0.403 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 48,125 | 0.481 | 20 | 24 | fits | 48,406 | 99 | 0.393 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 51,038 | 0.510 | 20 | 24 | fits | 50,465 | 111 | 0.381 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 45,961 | 0.460 | 20 | 24 | fits | 46,341 | 111 | 0.345 |
| BIND_RX | `acmp.bind_rx.if0` | 21,068 | 0.211 | 20 | 20 | fits | 39,206 | 29 (77) | 0.750 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 6,998 | 0.070 | 20 | 20 | fits | 30,217 | 30 (32) | 0.796 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 11,389 | 0.114 | 20 | 20 | fits | 27,570 | 17 (47) | 0.758 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,275 | 0.133 | 20 | 20 | fits | 33,549 | 20 (50) | 0.792 |
| PROBE_TX | `acmp.probe_tx.if0` | 10,993 | 0.110 | 20 | 20 | fits | 25,538 | 19 (48) | 0.729 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 11,064 | 0.111 | 20 | 20 | fits | 24,956 | 18 (48) | 0.707 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 10,144 | 0.101 | 20 | 20 | fits | 23,648 | 18 (48) | 0.680 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 10,130 | 0.101 | 20 | 20 | fits | 23,552 | 18 (48) | 0.677 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 17,953 | 0.180 | 20 | 24 | fits | 20,520 | 22 | 0.727 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 21,900 | 0.219 | 20 | 24 | fits | 24,395 | 22 | 0.672 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 12,499 | 0.125 | 20 | 24 | fits | 19,274 | 22 | 0.657 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 17,423 | 0.174 | 20 | 24 | fits | 19,713 | 22 | 0.650 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 13,342 | 0.133 | 20 | 24 | fits | 20,319 | 22 | 0.638 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 18,395 | 0.184 | 20 | 24 | fits | 21,058 | 22 | 0.667 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 11,792 | 0.118 | 20 | 24 | fits | 18,616 | 22 | 0.638 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 17,671 | 0.177 | 20 | 24 | fits | 20,109 | 22 | 0.685 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 11,429 | 0.114 | 20 | 24 | fits | 18,191 | 22 | 0.638 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 15,232 | 0.152 | 20 | 24 | fits | 22,250 | 22 | 0.574 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 16,259 | 0.163 | 20 | 24 | fits | 18,500 | 22 | 0.681 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 11,398 | 0.114 | 20 | 24 | fits | 18,218 | 22 | 0.653 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 17,213 | 0.172 | 20 | 24 | fits | 19,503 | 22 | 0.669 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 12,879 | 0.129 | 20 | 24 | fits | 19,777 | 22 | 0.652 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 17,356 | 0.174 | 20 | 24 | fits | 19,782 | 22 | 0.685 |
| get_configuration | `aecp.get_configuration.if0` | 9,938 | 0.099 | 20 | 24 | fits | 16,426 | 22 | 0.628 |
| entity_available | `aecp.entity_available.if0` | 15,551 | 0.156 | 20 | 24 | fits | 17,518 | 22 | 0.650 |
| get_name | `aecp.get_name.if0` | 12,936 | 0.129 | 20 | 24 | fits | 20,166 | 22 | 0.690 |
| get_counters | `aecp.get_counters.if0` | 19,412 | 0.194 | 20 | 24 | fits | 22,096 | 29 | 0.680 |
| get_avb_info | `aecp.get_avb_info.if0` | 15,229 | 0.152 | 20 | 24 | fits | 19,107 | 22 | 0.708 |
| unknown_command | `aecp.unknown_command.if0` | 10,469 | 0.105 | 20 | 24 | fits | 17,263 | 22 | 0.672 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 15,852 | 0.159 | 20 | 24 | fits | 18,096 | 22 | 0.679 |
| set_name | `aecp.set_name.if0` | 21,189 | 0.212 | 20 | 24 | fits | 34,396 | 46 | 0.677 |
| lock_entity | `aecp.lock_entity.if0` | 22,295 | 0.223 | 20 | 24 | fits | 27,854 | 36 | 0.722 |
| unlock_entity | `aecp.unlock_entity.if0` | 18,851 | 0.189 | 20 | 24 | fits | 25,098 | 36 | 0.656 |
| LINK_UP | `fixture.link_up.if0` | 1,912 | 0.019 | 20 | 200 | fits | 53,788 | 49 (11) | 0.738 |
| malformed MRPDU discard | `fixture.malformed.if0` | 13,730 | 0.137 | 18 | 18 | fits | 13,795 | 14 | 0.695 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 24,925 | 0.249 | 20 | 24 | fits | 35,664 | 46 | 0.695 |
| LINK_DOWN | `fixture.link_down.if0` | 1,923 | 0.019 | 20 | 200 | fits | 21,597 | 22 (9) | 0.784 |
| BIND_RX | `fixture.bind_rx.if0` | 21,235 | 0.212 | 20 | 20 | fits | 38,873 | 29 (77) | 0.746 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 10,944 | 0.109 | 20 | 20 | fits | 33,175 | 31 (35) | 0.713 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 9,052 | 0.091 | 20 | 20 | fits | 19,424 | 14 (29) | 0.750 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 75,441 | 0.754 | 20 | 200 | fits | 75,544 | 55 | 0.750 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 75,441 | 0.754 | 20 | 200 | fits | 75,544 | 55 | 0.750 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 75,171 | 0.752 | 20 | 20 | fits | 75,544 | 55 | 0.750 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 75,171 | 0.752 | 20 | 20 | fits | 75,544 | 55 | 0.750 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 75,376 | 0.754 | 20 | 24 | fits | 75,544 | 55 | 0.750 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 75,376 | 0.754 | 20 | 24 | fits | 75,544 | 55 | 0.750 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 75,311 | 0.753 | 20 | 50 | fits | 75,544 | 55 | 0.750 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 75,311 | 0.753 | 20 | 50 | fits | 75,544 | 55 | 0.750 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 75,246 | 0.752 | 18 | 18 | fits | 75,544 | 55 | 0.750 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 75,246 | 0.752 | 18 | 18 | fits | 75,544 | 55 | 0.750 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
