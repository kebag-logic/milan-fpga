### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 85 paths and 7 of 947 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.209 (0.478) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.153 (0.368) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.100 (0.338) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.202 (0.630) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.114 (0.313) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.105 (0.301) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.104 (0.306) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.114 (0.312) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.111 (0.367) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.167 (0.611) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.115 (0.359) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.287 (0.642) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.320 (0.604) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.120 (0.646) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.284 (1.501) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.162 (0.447) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.067 (0.213) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.031 (0.210) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.031 (0.332) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.034 (0.334) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.042 (0.245) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.158 (0.557) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.134 (0.524) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.132 (0.526) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.096 (0.491) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.173 (0.573) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.118 (0.508) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.222 (0.668) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.149 (0.540) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.213 (0.611) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.124 (0.516) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.115 (0.506) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.160 (0.556) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.166 (0.559) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.117 (0.519) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.154 (0.551) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.163 (0.559) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.115 (0.509) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.162 (0.560) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.119 (0.512) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.145 (0.529) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.127 (0.534) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.156 (0.554) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.112 (0.314) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.202 (0.696) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.198 (0.585) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.172 (0.617) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.419 (0.753) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.613 (1.004) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.598 (0.929) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.473 (0.850) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.611 (0.970) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.427 (0.757) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.786 (5.142) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 5.053 (5.676) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.242 (0.688) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.653 (2.135) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.529 (63.912) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.494 (64.878) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.351 (0.505) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 2.429 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.630 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 2.923 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 2.034 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.715 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.195 (0.597) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.126 (0.280) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.139 (0.334) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.176 (0.597) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.234 (0.621) | fits | 0 events | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 1.995 | fits | 0 srp | 6 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.302 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.379 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.345 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-6.service.adp.last.if0` (backlog-adp@verify-aged2-6) | 5.650 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.173 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.018 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.328 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-6.service.maap.last.if0` (backlog-adp@verify-aged2-6) | 5.688 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-6.service.srp.first.if0` (backlog-adp@verify-aged2-6) | 6.514 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-5.service.srp.last.if0` (backlog-adp@verify-aged2-5) | 10.283 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.803 (0.849) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.451 (0.451) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.241 (0.242) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.807 (0.883) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.337 | 10 | 156,461 (1.565) | yes | - |
| backlog-adp@blank-1 | 0 | 10.695 | 10 | 155,146 (1.551) | yes | - |
| backlog-adp@blank-2 | 0 | 10.649 | 10 | 156,046 (1.560) | yes | - |
| backlog-adp@blank-3 | 0 | 10.826 | 10 | 157,610 (1.576) | yes | - |
| backlog-adp@blank-4 | 0 | 11.361 | 12 | 151,778 (1.518) | yes | - |
| backlog-adp@blank-5 | 0 | 11.078 | 12 | 154,065 (1.541) | yes | - |
| backlog-adp@blank-6 | 0 | 10.833 | 11 | 154,666 (1.547) | yes | - |
| backlog-adp@blank-7 | 0 | 12.220 | 11 | 157,645 (1.576) | yes | - |
| backlog-adp@program-0 | 0 | 10.728 | 10 | 156,507 (1.565) | yes | - |
| backlog-adp@program-1 | 0 | 11.413 | 12 | 159,393 (1.594) | yes | - |
| backlog-adp@program-2 | 0 | 10.874 | 10 | 156,507 (1.565) | yes | - |
| backlog-adp@program-3 | 0 | 10.832 | 10 | 156,004 (1.560) | yes | - |
| backlog-adp@program-4 | 0 | 9.956 | 10 | 150,892 (1.509) | yes | - |
| backlog-adp@program-5 | 0 | 10.414 | 12 | 155,713 (1.557) | yes | - |
| backlog-adp@program-6 | 0 | 10.124 | 10 | 156,507 (1.565) | yes | - |
| backlog-adp@program-7 | 0 | 10.068 | 10 | 156,384 (1.564) | yes | - |
| backlog-adp@verify-0 | 0 | 11.243 | 10 | 157,176 (1.572) | yes | - |
| backlog-adp@verify-1 | 0 | 10.797 | 10 | 156,405 (1.564) | yes | - |
| backlog-adp@verify-2 | 0 | 10.765 | 10 | 157,176 (1.572) | yes | - |
| backlog-adp@verify-3 | 0 | 10.723 | 10 | 156,495 (1.565) | yes | - |
| backlog-adp@verify-4 | 0 | 11.345 | 11 | 159,359 (1.594) | yes | - |
| backlog-adp@verify-5 | 0 | 10.973 | 11 | 154,969 (1.550) | yes | - |
| backlog-adp@verify-6 | 1 | 10.672 | 9 | 156,014 (1.560) | yes | - |
| backlog-adp@verify-7 | 0 | 10.691 | 10 | 158,566 (1.586) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 11.558 | 10 | 156,423 (1.564) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 11.183 | 12 | 150,915 (1.509) | yes | - |
| backlog-adp@blank-aged2-2 | 1 | 10.795 | 10 | 151,744 (1.517) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 10.780 | 10 | 156,220 (1.562) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 10.730 | 10 | 155,146 (1.551) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 10.682 | 10 | 156,046 (1.560) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 10.662 | 10 | 155,058 (1.551) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 10.637 | 9 | 150,300 (1.503) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 11.900 | 11 | 157,279 (1.573) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 10.741 | 10 | 156,551 (1.566) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 10.699 | 10 | 159,336 (1.593) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 11.552 | 12 | 157,298 (1.573) | yes | - |
| backlog-adp@blank-aged1-4 | 1 | 11.121 | 11 | 151,091 (1.511) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 10.811 | 10 | 155,647 (1.556) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 10.767 | 10 | 154,629 (1.546) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 10.722 | 10 | 155,309 (1.553) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.152 | 11 | 159,045 (1.590) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 10.957 | 11 | 156,623 (1.566) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 10.721 | 10 | 156,171 (1.562) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 10.674 | 10 | 155,146 (1.551) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 10.651 | 9 | 156,423 (1.564) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 10.828 | 10 | 157,954 (1.580) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 10.798 | 10 | 157,498 (1.575) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 11.603 | 12 | 158,935 (1.589) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 10.894 | 10 | 156,502 (1.565) | yes | - |
| backlog-adp@program-aged1-1 | 1 | 11.149 | 11 | 159,137 (1.591) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 10.986 | 11 | 151,577 (1.516) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 10.778 | 10 | 156,461 (1.565) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 10.766 | 10 | 157,279 (1.573) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 10.716 | 10 | 156,220 (1.562) | yes | - |
| backlog-adp@program-aged1-6 | 1 | 10.688 | 9 | 153,853 (1.539) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 11.688 | 12 | 156,449 (1.564) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.879 | 11 | 156,461 (1.565) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 10.547 | 10 | 157,232 (1.572) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 10.697 | 10 | 156,220 (1.562) | yes | - |
| backlog-adp@verify-aged2-3 | 1 | 10.644 | 9 | 155,477 (1.555) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 11.332 | 11 | 151,161 (1.512) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 10.939 | 11 | 157,521 (1.575) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 10.636 | 10 | 158,724 (1.587) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 10.722 | 10 | 156,087 (1.561) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 11.703 | 11 | 156,623 (1.566) | yes | - |
| backlog-adp@verify-aged1-1 | 1 | 10.898 | 11 | 158,507 (1.585) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 10.748 | 10 | 156,092 (1.561) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 10.720 | 10 | 156,507 (1.565) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 10.702 | 10 | 157,561 (1.576) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 10.666 | 10 | 156,502 (1.565) | yes | - |
| backlog-adp@verify-aged1-6 | 1 | 10.642 | 9 | 156,518 (1.565) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 12.343 | 13 | 157,328 (1.573) | yes | - |
| backlog | 0 | 6.395 | 7 | 157,107 (1.571) | yes | - |
| backlog-adp | 0 | 9.891 | 10 | 158,806 (1.588) | yes | - |
| backlog-adp-refill | 0 | 41.087 | 23 | 155,065 (1.551) | yes | - |
| backlog-owed | 0 | 65.550 | 25 | 154,098 (1.541) | yes | - |
| fixture | 0 | 1.456 | 2 | 85,506 (0.855) | yes | - |

Composed maximum over the 4 backlog windows: 158,806 CPU cycles (1.588 ms), backlog-adp.
Over the windows that released their whole load only: 158,806 (1.588 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 119807 | 0 | 55,044 (0.550) | fits |
| save-held | 3305 | 0 | 162,311 (1.623) | fits |
| save-starved | 57286 | 0 | 162,311 (1.623) | fits |
| acmp-notk | 3606 | 0 | 47,784 (0.478) | fits |
| backlog-adp@blank-0 | 537 | 0 | 156,461 (1.565) | fits |
| backlog-adp@blank-1 | 537 | 0 | 155,146 (1.551) | fits |
| backlog-adp@blank-2 | 537 | 0 | 156,046 (1.560) | fits |
| backlog-adp@blank-3 | 537 | 0 | 157,610 (1.576) | fits |
| backlog-adp@blank-4 | 539 | 0 | 151,778 (1.518) | fits |
| backlog-adp@blank-5 | 539 | 0 | 154,065 (1.541) | fits |
| backlog-adp@blank-6 | 539 | 0 | 154,666 (1.547) | fits |
| backlog-adp@blank-7 | 540 | 0 | 157,645 (1.576) | fits |
| backlog-adp@program-0 | 893 | 0 | 156,507 (1.565) | fits |
| backlog-adp@program-1 | 895 | 0 | 159,393 (1.594) | fits |
| backlog-adp@program-2 | 895 | 0 | 156,507 (1.565) | fits |
| backlog-adp@program-3 | 895 | 0 | 156,004 (1.560) | fits |
| backlog-adp@program-4 | 896 | 0 | 150,892 (1.509) | fits |
| backlog-adp@program-5 | 898 | 0 | 155,713 (1.557) | fits |
| backlog-adp@program-6 | 898 | 0 | 156,507 (1.565) | fits |
| backlog-adp@program-7 | 898 | 0 | 156,384 (1.564) | fits |
| backlog-adp@verify-0 | 1243 | 0 | 157,176 (1.572) | fits |
| backlog-adp@verify-1 | 1243 | 0 | 156,405 (1.564) | fits |
| backlog-adp@verify-2 | 1243 | 0 | 157,176 (1.572) | fits |
| backlog-adp@verify-3 | 1243 | 0 | 156,495 (1.565) | fits |
| backlog-adp@verify-4 | 1244 | 0 | 159,359 (1.594) | fits |
| backlog-adp@verify-5 | 1245 | 0 | 154,969 (1.550) | fits |
| backlog-adp@verify-6 | 1244 | 0 | 156,014 (1.560) | fits |
| backlog-adp@verify-7 | 1245 | 0 | 158,566 (1.586) | fits |
| backlog-adp@blank-aged2-0 | 774 | 0 | 156,423 (1.564) | fits |
| backlog-adp@blank-aged2-1 | 782 | 0 | 150,915 (1.509) | fits |
| backlog-adp@blank-aged2-2 | 787 | 0 | 151,744 (1.517) | fits |
| backlog-adp@blank-aged2-3 | 793 | 0 | 156,220 (1.562) | fits |
| backlog-adp@blank-aged2-4 | 799 | 0 | 155,146 (1.551) | fits |
| backlog-adp@blank-aged2-5 | 805 | 0 | 156,046 (1.560) | fits |
| backlog-adp@blank-aged2-6 | 811 | 0 | 155,058 (1.551) | fits |
| backlog-adp@blank-aged2-7 | 817 | 0 | 150,300 (1.503) | fits |
| backlog-adp@blank-aged1-0 | 726 | 0 | 157,279 (1.573) | fits |
| backlog-adp@blank-aged1-1 | 731 | 0 | 156,551 (1.566) | fits |
| backlog-adp@blank-aged1-2 | 737 | 0 | 159,336 (1.593) | fits |
| backlog-adp@blank-aged1-3 | 745 | 0 | 157,298 (1.573) | fits |
| backlog-adp@blank-aged1-4 | 751 | 0 | 151,091 (1.511) | fits |
| backlog-adp@blank-aged1-5 | 756 | 0 | 155,647 (1.556) | fits |
| backlog-adp@blank-aged1-6 | 762 | 0 | 154,629 (1.546) | fits |
| backlog-adp@blank-aged1-7 | 768 | 0 | 155,309 (1.553) | fits |
| backlog-adp@program-aged2-0 | 1128 | 0 | 159,045 (1.590) | fits |
| backlog-adp@program-aged2-1 | 1134 | 0 | 156,623 (1.566) | fits |
| backlog-adp@program-aged2-2 | 1139 | 0 | 156,171 (1.562) | fits |
| backlog-adp@program-aged2-3 | 1145 | 0 | 155,146 (1.551) | fits |
| backlog-adp@program-aged2-4 | 1151 | 0 | 156,423 (1.564) | fits |
| backlog-adp@program-aged2-5 | 1158 | 0 | 157,954 (1.580) | fits |
| backlog-adp@program-aged2-6 | 1164 | 0 | 157,498 (1.575) | fits |
| backlog-adp@program-aged2-7 | 1172 | 0 | 158,935 (1.589) | fits |
| backlog-adp@program-aged1-0 | 1077 | 0 | 156,502 (1.565) | fits |
| backlog-adp@program-aged1-1 | 1085 | 0 | 159,137 (1.591) | fits |
| backlog-adp@program-aged1-2 | 1091 | 0 | 151,577 (1.516) | fits |
| backlog-adp@program-aged1-3 | 1096 | 0 | 156,461 (1.565) | fits |
| backlog-adp@program-aged1-4 | 1102 | 0 | 157,279 (1.573) | fits |
| backlog-adp@program-aged1-5 | 1108 | 0 | 156,220 (1.562) | fits |
| backlog-adp@program-aged1-6 | 1114 | 0 | 153,853 (1.539) | fits |
| backlog-adp@program-aged1-7 | 1123 | 0 | 156,449 (1.564) | fits |
| backlog-adp@verify-aged2-0 | 1481 | 0 | 156,461 (1.565) | fits |
| backlog-adp@verify-aged2-1 | 1486 | 0 | 157,232 (1.572) | fits |
| backlog-adp@verify-aged2-2 | 1492 | 0 | 156,220 (1.562) | fits |
| backlog-adp@verify-aged2-3 | 1498 | 0 | 155,477 (1.555) | fits |
| backlog-adp@verify-aged2-4 | 1506 | 0 | 151,161 (1.512) | fits |
| backlog-adp@verify-aged2-5 | 1512 | 0 | 157,521 (1.575) | fits |
| backlog-adp@verify-aged2-6 | 1517 | 0 | 158,724 (1.587) | fits |
| backlog-adp@verify-aged2-7 | 1523 | 0 | 156,087 (1.561) | fits |
| backlog-adp@verify-aged1-0 | 1431 | 0 | 156,623 (1.566) | fits |
| backlog-adp@verify-aged1-1 | 1438 | 0 | 158,507 (1.585) | fits |
| backlog-adp@verify-aged1-2 | 1443 | 0 | 156,092 (1.561) | fits |
| backlog-adp@verify-aged1-3 | 1449 | 0 | 156,507 (1.565) | fits |
| backlog-adp@verify-aged1-4 | 1455 | 0 | 157,561 (1.576) | fits |
| backlog-adp@verify-aged1-5 | 1461 | 0 | 156,502 (1.565) | fits |
| backlog-adp@verify-aged1-6 | 1467 | 0 | 156,518 (1.565) | fits |
| backlog-adp@verify-aged1-7 | 1477 | 0 | 157,328 (1.573) | fits |
| adp-advertise | 597 | 0 | 38,099 (0.381) | fits |
| acmp-noresp | 2021 | 0 | 47,784 (0.478) | fits |
| save | 609 | 0 | 49,413 (0.494) | fits |
| srp | 289 | 0 | 45,147 (0.451) | fits |
| backlog | 285 | 0 | 157,107 (1.571) | fits |
| backlog-adp | 312 | 0 | 158,806 (1.588) | fits |
| backlog-adp-refill | 325 | 0 | 155,065 (1.551) | fits |
| backlog-owed | 309 | 0 | 154,098 (1.541) | fits |
| acmp-disc | 936 | 0 | 47,784 (0.478) | fits |
| maap | 178 | 0 | 38,099 (0.381) | fits |
| adp-link | 89 | 0 | 44,901 (0.449) | fits |
| adp-gm | 88 | 0 | 33,443 (0.334) | fits |
| adp-discover | 88 | 0 | 33,443 (0.334) | fits |
| control | 88 | 0 | 33,443 (0.334) | fits |
| aecp-fanout | 110 | 0 | 60,563 (0.606) | fits |
| acmp-cmd | 87 | 0 | 47,784 (0.478) | fits |
| aecp | 113 | 0 | 48,161 (0.482) | fits |
| datapath-events | 116 | 0 | 33,443 (0.334) | fits |
| fixture | 161 | 0 | 85,506 (0.855) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 8.963 (20) | 11.037 |
| backlog-adp@blank-aged2-1 | 2 | none | +9.277 ms, 76,338 (0.763 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 9.240 (20) | 10.760 |
| backlog-adp@blank-aged2-2 | 2 | +7.975 ms, 76,340 (0.763 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 10.137 (20) | 9.863 |
| backlog-adp@blank-aged2-3 | 2 | +7.183 ms, 76,292 (0.763 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 10.124 (20) | 9.876 |
| backlog-adp@blank-aged2-4 | 2 | +5.525 ms, 76,645 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 10.073 (20) | 9.927 |
| backlog-adp@blank-aged2-5 | 2 | none | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 10.025 (20) | 9.975 |
| backlog-adp@blank-aged2-6 | 2 | none | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 10.002 (20) | 9.998 |
| backlog-adp@blank-aged2-7 | 2 | +4.563 ms, 76,742 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 9.976 (20) | 10.024 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 9.310 (20) | 10.690 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 9.327 (20) | 10.673 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 9.283 (20) | 10.717 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 9.232 (20) | 10.768 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 9.207 (20) | 10.793 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 9.400 (20) | 10.600 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 9.356 (20) | 10.644 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 9.310 (20) | 10.690 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 9.038 (20) | 10.962 |
| backlog-adp@program-aged2-1 | 2 | +9.013 ms, 80,496 (0.805 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 10.161 (20) | 9.839 |
| backlog-adp@program-aged2-2 | 2 | +8.112 ms, 80,205 (0.802 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 10.064 (20) | 9.936 |
| backlog-adp@program-aged2-3 | 2 | +7.216 ms, 80,205 (0.802 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 10.018 (20) | 9.982 |
| backlog-adp@program-aged2-4 | 2 | +5.485 ms, 80,634 (0.806 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 9.991 (20) | 10.009 |
| backlog-adp@program-aged2-5 | 2 | none | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 10.168 (20) | 9.832 |
| backlog-adp@program-aged2-6 | 2 | +4.786 ms, 80,906 (0.809 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 10.137 (20) | 9.863 |
| backlog-adp@program-aged2-7 | 2 | +3.146 ms, 80,840 (0.808 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 10.260 (20) | 9.740 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 8.950 (20) | 11.050 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 8.899 (20) | 11.101 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 9.174 (20) | 10.826 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 9.313 (20) | 10.687 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 9.303 (20) | 10.697 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 9.252 (20) | 10.748 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 9.221 (20) | 10.779 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 9.371 (20) | 10.629 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 9.273 (20) | 10.727 |
| backlog-adp@verify-aged2-1 | 2 | none | +9.343 ms, 77,195 (0.772 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 9.305 (20) | 10.695 |
| backlog-adp@verify-aged2-2 | 2 | +8.034 ms, 77,149 (0.771 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 10.040 (20) | 9.960 |
| backlog-adp@verify-aged2-3 | 2 | +7.215 ms, 77,066 (0.771 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 9.983 (20) | 10.017 |
| backlog-adp@verify-aged2-4 | 2 | +5.404 ms, 77,453 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 9.967 (20) | 10.033 |
| backlog-adp@verify-aged2-5 | 2 | +4.797 ms, 77,466 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 10.283 (20) | 9.717 |
| backlog-adp@verify-aged2-6 | 2 | +3.356 ms, 77,365 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 9.980 (20) | 10.020 |
| backlog-adp@verify-aged2-7 | 2 | +3.013 ms, 77,365 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 10.065 (20) | 9.935 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 8.918 (20) | 11.082 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 8.895 (20) | 11.105 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 9.329 (20) | 10.671 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 9.301 (20) | 10.699 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 9.279 (20) | 10.721 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 9.243 (20) | 10.757 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 9.217 (20) | 10.783 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 9.370 (20) | 10.630 |

Least margin over the aged windows: 9.717 ms, `backlog-adp@verify-aged2-5.service.srp.last.if0` at 10.283 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 22829.479 | 22,870 | 382 | 2 | 31.290 | yes | within |
| save-held | 4818.359 | 12,470 | 382 | - | 14.972 | no | within |
| save-starved | 12448.243 | 12,470 | 382 | - | 33.597 | yes | within |
| save | 4818.928 | 12,470 | 382 | - | 10.878 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1080 | 80,818 (0.808) | 77,628 (0.776) |
| save-held | 1562 | 100,914 (1.009) | 77,938 (0.779) |
| save-starved | 698 | 81,744 (0.817) | 78,078 (0.781) |
| acmp-notk | 1065 | 108,755 (1.088) | 78,102 (0.781) |
| backlog-adp@blank-0 | 339 | 96,249 (0.962) | 75,676 (0.757) |
| backlog-adp@blank-1 | 339 | 96,249 (0.962) | 75,676 (0.757) |
| backlog-adp@blank-2 | 339 | 96,169 (0.962) | 75,676 (0.757) |
| backlog-adp@blank-3 | 339 | 96,511 (0.965) | 75,676 (0.757) |
| backlog-adp@blank-4 | 339 | 96,666 (0.967) | 75,819 (0.758) |
| backlog-adp@blank-5 | 339 | 95,051 (0.951) | 75,725 (0.757) |
| backlog-adp@blank-6 | 339 | 96,191 (0.962) | 75,754 (0.758) |
| backlog-adp@blank-7 | 340 | 96,191 (0.962) | 75,754 (0.758) |
| backlog-adp@program-0 | 448 | 101,036 (1.010) | 78,332 (0.783) |
| backlog-adp@program-1 | 448 | 101,036 (1.010) | 78,397 (0.784) |
| backlog-adp@program-2 | 448 | 101,036 (1.010) | 78,410 (0.784) |
| backlog-adp@program-3 | 448 | 101,036 (1.010) | 78,410 (0.784) |
| backlog-adp@program-4 | 449 | 101,036 (1.010) | 78,002 (0.780) |
| backlog-adp@program-5 | 449 | 101,036 (1.010) | 78,002 (0.780) |
| backlog-adp@program-6 | 449 | 101,036 (1.010) | 78,002 (0.780) |
| backlog-adp@program-7 | 449 | 101,036 (1.010) | 78,002 (0.780) |
| backlog-adp@verify-0 | 555 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-1 | 555 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-2 | 555 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-3 | 555 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-4 | 555 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-5 | 555 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-6 | 555 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-7 | 555 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@blank-aged2-0 | 338 | 96,743 (0.967) | 75,820 (0.758) |
| backlog-adp@blank-aged2-1 | 337 | 79,435 (0.794) | 75,316 (0.753) |
| backlog-adp@blank-aged2-2 | 337 | 79,435 (0.794) | 75,302 (0.753) |
| backlog-adp@blank-aged2-3 | 337 | 79,435 (0.794) | 75,302 (0.753) |
| backlog-adp@blank-aged2-4 | 337 | 79,435 (0.794) | 75,420 (0.754) |
| backlog-adp@blank-aged2-5 | 337 | 87,509 (0.875) | 75,620 (0.756) |
| backlog-adp@blank-aged2-6 | 337 | 87,011 (0.870) | 75,516 (0.755) |
| backlog-adp@blank-aged2-7 | 337 | 79,435 (0.794) | 75,448 (0.754) |
| backlog-adp@blank-aged1-0 | 338 | 96,271 (0.963) | 75,834 (0.758) |
| backlog-adp@blank-aged1-1 | 337 | 96,591 (0.966) | 75,756 (0.758) |
| backlog-adp@blank-aged1-2 | 337 | 96,724 (0.967) | 75,821 (0.758) |
| backlog-adp@blank-aged1-3 | 337 | 96,724 (0.967) | 75,821 (0.758) |
| backlog-adp@blank-aged1-4 | 337 | 103,812 (1.038) | 76,061 (0.761) |
| backlog-adp@blank-aged1-5 | 337 | 96,233 (0.962) | 75,834 (0.758) |
| backlog-adp@blank-aged1-6 | 337 | 96,271 (0.963) | 75,834 (0.758) |
| backlog-adp@blank-aged1-7 | 337 | 96,271 (0.963) | 75,834 (0.758) |
| backlog-adp@program-aged2-0 | 447 | 101,036 (1.010) | 78,461 (0.785) |
| backlog-adp@program-aged2-1 | 446 | 101,036 (1.010) | 78,024 (0.780) |
| backlog-adp@program-aged2-2 | 446 | 101,036 (1.010) | 78,002 (0.780) |
| backlog-adp@program-aged2-3 | 446 | 101,036 (1.010) | 78,002 (0.780) |
| backlog-adp@program-aged2-4 | 446 | 101,036 (1.010) | 78,077 (0.781) |
| backlog-adp@program-aged2-5 | 446 | 101,036 (1.010) | 78,249 (0.782) |
| backlog-adp@program-aged2-6 | 446 | 101,036 (1.010) | 78,069 (0.781) |
| backlog-adp@program-aged2-7 | 447 | 101,036 (1.010) | 78,129 (0.781) |
| backlog-adp@program-aged1-0 | 447 | 101,036 (1.010) | 78,396 (0.784) |
| backlog-adp@program-aged1-1 | 446 | 101,036 (1.010) | 78,388 (0.784) |
| backlog-adp@program-aged1-2 | 446 | 101,036 (1.010) | 78,381 (0.784) |
| backlog-adp@program-aged1-3 | 446 | 101,036 (1.010) | 78,410 (0.784) |
| backlog-adp@program-aged1-4 | 446 | 101,036 (1.010) | 78,410 (0.784) |
| backlog-adp@program-aged1-5 | 446 | 101,036 (1.010) | 78,410 (0.784) |
| backlog-adp@program-aged1-6 | 446 | 101,036 (1.010) | 78,410 (0.784) |
| backlog-adp@program-aged1-7 | 447 | 101,036 (1.010) | 78,475 (0.785) |
| backlog-adp@verify-aged2-0 | 556 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-aged2-1 | 555 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-aged2-2 | 555 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-aged2-3 | 555 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-aged2-4 | 555 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-aged2-5 | 555 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-aged2-6 | 555 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-aged2-7 | 555 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-aged1-0 | 556 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-aged1-1 | 555 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-aged1-2 | 555 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-aged1-3 | 555 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-aged1-4 | 555 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-aged1-5 | 555 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-aged1-6 | 555 | 105,019 (1.050) | 78,102 (0.781) |
| backlog-adp@verify-aged1-7 | 556 | 105,019 (1.050) | 78,102 (0.781) |
| adp-advertise | 577 | 26,686 (0.267) | 2,458 (0.025) |
| acmp-noresp | 615 | 108,402 (1.084) | 78,102 (0.781) |
| save | 585 | 100,702 (1.007) | 77,784 (0.778) |
| srp | 271 | 26,626 (0.266) | 2,458 (0.025) |
| backlog | 265 | 26,626 (0.266) | 2,458 (0.025) |
| backlog-adp | 271 | 26,626 (0.266) | 2,672 (0.027) |
| backlog-adp-refill | 274 | 26,626 (0.266) | 2,672 (0.027) |
| backlog-owed | 277 | 26,626 (0.266) | 2,694 (0.027) |
| acmp-disc | 306 | 108,402 (1.084) | 75,385 (0.754) |
| maap | 166 | 26,592 (0.266) | 2,458 (0.025) |
| adp-link | 79 | 26,592 (0.266) | 2,458 (0.025) |
| adp-gm | 79 | 26,592 (0.266) | 2,458 (0.025) |
| adp-discover | 79 | 26,592 (0.266) | 2,458 (0.025) |
| control | 79 | 26,592 (0.266) | 2,458 (0.025) |
| aecp-fanout | 79 | 26,592 (0.266) | 2,458 (0.025) |
| acmp-cmd | 66 | 26,592 (0.266) | 2,690 (0.027) |
| aecp | 80 | 26,592 (0.266) | 2,458 (0.025) |
| datapath-events | 69 | 26,592 (0.266) | 2,458 (0.025) |
| fixture | 54 | 21,762 (0.218) | 2,489 (0.025) |

Longest pass that carries a step: 108,755 CPU cycles (1.088 ms), acmp-notk; longest step: 78,475 (0.785 ms), backlog-adp@program-aged1-7.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 259,687 | 2.597 | 20 | 200 | fits | 98,316 | 121 | 0.480 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 239,550 | 2.396 | 20 | 20 | fits | 98,316 | 121 | 0.480 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 292,294 | 2.923 | 20 | 24 | fits | 80,746 | 49 | 0.544 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 200,075 | 2.001 | 20 | 50 | fits | 98,316 | 121 | 0.480 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 824,918 | 8.249 | 20 | 20 | fits | 73,920 | 34 | 0.671 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 190,022 | 1.900 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 144,864 | 1.449 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 170,370 | 1.704 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 263,023 | 2.630 | 20 | 200 | fits | 101,652 | 127 | 0.499 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 242,886 | 2.429 | 20 | 20 | fits | 101,652 | 127 | 0.499 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 283,289 | 2.833 | 20 | 24 | fits | 80,447 | 60 | 0.461 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 203,411 | 2.034 | 20 | 50 | fits | 101,652 | 127 | 0.499 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 871,518 | 8.715 | 20 | 20 | fits | 45,345 | 22 | 0.776 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 175,561 | 1.756 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 158,117 | 1.581 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 199,516 | 1.995 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 11,952 | 0.120 | 20 | 20 | fits | 39,118 | 19 (14) | 0.889 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 447,523 | 4.475 | 20 | 20 | fits | 156,461 | 193 | 0.416 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 363,353 | 3.634 | 20 | 200 | fits | 150,585 | 196 | 0.406 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 519,198 | 5.192 | 20 | 200 | fits | 156,461 | 193 | 0.416 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 364,277 | 3.643 | 20 | 20 | fits | 150,585 | 196 | 0.406 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 603,844 | 6.038 | 20 | 20 | fits | 83,942 | 31 | 0.752 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 217,332 | 2.173 | 20 | 24 | fits | 149,701 | 145 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 366,927 | 3.669 | 20 | 24 | fits | 150,585 | 196 | 0.406 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 366,861 | 3.669 | 20 | 50 | fits | 150,585 | 196 | 0.406 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 522,926 | 5.229 | 20 | 50 | fits | 156,461 | 193 | 0.416 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 606,802 | 6.068 | 20 | 20 | fits | 83,942 | 31 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 992,570 | 9.926 | 20 | 20 | fits | 38,971 | 18 | 0.841 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 401,678 | 4.017 | 20 | 20 | fits | 155,146 | 204 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 300,408 | 3.004 | 20 | 200 | fits | 151,702 | 180 | 0.423 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 454,938 | 4.549 | 20 | 200 | fits | 155,146 | 204 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 301,332 | 3.013 | 20 | 20 | fits | 151,702 | 180 | 0.423 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 539,546 | 5.395 | 20 | 20 | fits | 83,904 | 31 | 0.751 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 153,270 | 1.533 | 20 | 24 | fits | 149,451 | 145 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 303,982 | 3.040 | 20 | 24 | fits | 151,702 | 180 | 0.423 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 303,916 | 3.039 | 20 | 50 | fits | 151,702 | 180 | 0.423 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 458,666 | 4.587 | 20 | 50 | fits | 155,146 | 204 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 542,504 | 5.425 | 20 | 20 | fits | 83,904 | 31 | 0.751 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 928,355 | 9.284 | 20 | 20 | fits | 38,913 | 18 | 0.840 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 398,554 | 3.986 | 20 | 20 | fits | 156,046 | 209 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 295,264 | 2.953 | 20 | 200 | fits | 150,148 | 176 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 450,694 | 4.507 | 20 | 200 | fits | 156,046 | 209 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 296,188 | 2.962 | 20 | 20 | fits | 150,148 | 176 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 535,438 | 5.354 | 20 | 20 | fits | 84,040 | 32 | 0.750 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 149,680 | 1.497 | 20 | 24 | fits | 149,451 | 145 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 298,838 | 2.988 | 20 | 24 | fits | 150,148 | 176 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 298,772 | 2.988 | 20 | 50 | fits | 150,148 | 176 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 454,422 | 4.544 | 20 | 50 | fits | 156,046 | 209 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 538,396 | 5.384 | 20 | 20 | fits | 84,040 | 32 | 0.750 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 923,900 | 9.239 | 20 | 20 | fits | 41,984 | 16 | 0.756 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 396,641 | 3.966 | 20 | 20 | fits | 157,610 | 193 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 312,321 | 3.123 | 20 | 200 | fits | 150,626 | 196 | 0.406 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 469,315 | 4.693 | 20 | 200 | fits | 157,610 | 193 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 313,245 | 3.132 | 20 | 20 | fits | 150,626 | 196 | 0.406 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 568,955 | 5.690 | 20 | 20 | fits | 87,782 | 38 | 0.760 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 166,259 | 1.663 | 20 | 24 | fits | 149,385 | 145 | 0.379 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 315,895 | 3.159 | 20 | 24 | fits | 150,626 | 196 | 0.406 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 315,829 | 3.158 | 20 | 50 | fits | 150,626 | 196 | 0.406 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 473,043 | 4.730 | 20 | 50 | fits | 157,610 | 193 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 571,913 | 5.719 | 20 | 20 | fits | 87,782 | 38 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 941,208 | 9.412 | 20 | 20 | fits | 33,286 | 12 | 0.827 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 408,714 | 4.087 | 20 | 20 | fits | 150,673 | 204 | 0.454 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 309,883 | 3.099 | 20 | 200 | fits | 151,778 | 181 | 0.424 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 470,863 | 4.709 | 20 | 200 | fits | 150,673 | 204 | 0.454 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 310,807 | 3.108 | 20 | 20 | fits | 151,778 | 181 | 0.424 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 554,831 | 5.548 | 20 | 20 | fits | 83,264 | 41 | 0.754 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 162,669 | 1.627 | 20 | 24 | fits | 149,385 | 145 | 0.379 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 313,457 | 3.135 | 20 | 24 | fits | 151,778 | 181 | 0.424 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 313,391 | 3.134 | 20 | 50 | fits | 151,778 | 181 | 0.424 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 474,591 | 4.746 | 20 | 50 | fits | 150,673 | 204 | 0.454 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 557,789 | 5.578 | 20 | 20 | fits | 83,264 | 41 | 0.754 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 938,256 | 9.383 | 20 | 20 | fits | 41,995 | 16 | 0.754 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 428,089 | 4.281 | 20 | 20 | fits | 154,065 | 200 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 318,470 | 3.185 | 20 | 200 | fits | 153,626 | 185 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 471,919 | 4.719 | 20 | 200 | fits | 154,065 | 200 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 319,394 | 3.194 | 20 | 20 | fits | 153,626 | 185 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 557,387 | 5.574 | 20 | 20 | fits | 84,764 | 37 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 159,231 | 1.592 | 20 | 24 | fits | 149,537 | 146 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 322,044 | 3.220 | 20 | 24 | fits | 153,626 | 185 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 321,978 | 3.220 | 20 | 50 | fits | 153,626 | 185 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 475,647 | 4.756 | 20 | 50 | fits | 154,065 | 200 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 560,345 | 5.603 | 20 | 20 | fits | 84,764 | 37 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 931,903 | 9.319 | 20 | 20 | fits | 33,412 | 13 | 0.823 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 422,360 | 4.224 | 20 | 20 | fits | 154,666 | 205 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 310,967 | 3.110 | 20 | 200 | fits | 150,304 | 176 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 465,017 | 4.650 | 20 | 200 | fits | 154,666 | 205 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 311,891 | 3.119 | 20 | 20 | fits | 150,304 | 176 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 550,284 | 5.503 | 20 | 20 | fits | 84,563 | 37 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 165,227 | 1.652 | 20 | 24 | fits | 148,654 | 146 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 314,541 | 3.145 | 20 | 24 | fits | 150,304 | 176 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 314,475 | 3.145 | 20 | 50 | fits | 150,304 | 176 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 468,745 | 4.687 | 20 | 50 | fits | 154,666 | 205 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 553,242 | 5.532 | 20 | 20 | fits | 84,563 | 37 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 942,281 | 9.423 | 20 | 20 | fits | 42,442 | 16 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 413,107 | 4.131 | 20 | 20 | fits | 157,645 | 196 | 0.411 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 318,001 | 3.180 | 20 | 200 | fits | 156,534 | 197 | 0.423 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 475,030 | 4.750 | 20 | 200 | fits | 157,645 | 196 | 0.411 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 318,925 | 3.189 | 20 | 20 | fits | 156,534 | 197 | 0.423 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 559,767 | 5.598 | 20 | 20 | fits | 84,033 | 31 | 0.752 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 166,031 | 1.660 | 20 | 24 | fits | 149,402 | 145 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 321,575 | 3.216 | 20 | 24 | fits | 156,534 | 197 | 0.423 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 321,509 | 3.215 | 20 | 50 | fits | 156,534 | 197 | 0.423 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 478,758 | 4.788 | 20 | 50 | fits | 157,645 | 196 | 0.411 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 562,725 | 5.627 | 20 | 20 | fits | 84,033 | 31 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 942,816 | 9.428 | 20 | 20 | fits | 33,366 | 12 | 0.828 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 382,207 | 3.822 | 20 | 20 | fits | 156,507 | 193 | 0.417 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 298,037 | 2.980 | 20 | 200 | fits | 150,364 | 196 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 453,928 | 4.539 | 20 | 200 | fits | 156,507 | 193 | 0.417 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 298,961 | 2.990 | 20 | 20 | fits | 150,364 | 196 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 538,238 | 5.382 | 20 | 20 | fits | 83,606 | 32 | 0.751 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 152,237 | 1.522 | 20 | 24 | fits | 149,378 | 145 | 0.379 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 301,611 | 3.016 | 20 | 24 | fits | 150,364 | 196 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 301,545 | 3.015 | 20 | 50 | fits | 150,364 | 196 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 457,656 | 4.577 | 20 | 50 | fits | 156,507 | 193 | 0.417 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 541,196 | 5.412 | 20 | 20 | fits | 83,606 | 32 | 0.751 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 926,369 | 9.264 | 20 | 20 | fits | 38,971 | 18 | 0.841 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 428,164 | 4.282 | 20 | 20 | fits | 159,393 | 211 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 312,361 | 3.124 | 20 | 200 | fits | 151,567 | 181 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 482,061 | 4.821 | 20 | 200 | fits | 159,393 | 211 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 313,285 | 3.133 | 20 | 20 | fits | 151,567 | 181 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 566,809 | 5.668 | 20 | 20 | fits | 84,044 | 31 | 0.757 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 165,358 | 1.654 | 20 | 24 | fits | 149,444 | 145 | 0.379 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 315,935 | 3.159 | 20 | 24 | fits | 151,567 | 181 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 315,869 | 3.159 | 20 | 50 | fits | 151,567 | 181 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 485,789 | 4.858 | 20 | 50 | fits | 159,393 | 211 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 569,767 | 5.698 | 20 | 20 | fits | 84,044 | 31 | 0.757 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 938,725 | 9.387 | 20 | 20 | fits | 33,288 | 12 | 0.827 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 396,047 | 3.960 | 20 | 20 | fits | 156,507 | 193 | 0.417 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 311,877 | 3.119 | 20 | 200 | fits | 150,243 | 196 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 467,768 | 4.678 | 20 | 200 | fits | 156,507 | 193 | 0.417 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 312,801 | 3.128 | 20 | 20 | fits | 150,243 | 196 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 558,181 | 5.582 | 20 | 20 | fits | 89,709 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 166,198 | 1.662 | 20 | 24 | fits | 149,236 | 145 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 315,451 | 3.155 | 20 | 24 | fits | 150,243 | 196 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 315,385 | 3.154 | 20 | 50 | fits | 150,243 | 196 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 471,496 | 4.715 | 20 | 50 | fits | 156,507 | 193 | 0.417 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 561,139 | 5.611 | 20 | 20 | fits | 89,709 | 39 | 0.746 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 941,051 | 9.411 | 20 | 20 | fits | 33,743 | 12 | 0.836 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 389,831 | 3.898 | 20 | 20 | fits | 156,004 | 204 | 0.428 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 305,237 | 3.052 | 20 | 200 | fits | 150,613 | 178 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 460,625 | 4.606 | 20 | 200 | fits | 156,004 | 204 | 0.428 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 306,161 | 3.062 | 20 | 20 | fits | 150,613 | 178 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 545,603 | 5.456 | 20 | 20 | fits | 84,274 | 38 | 0.726 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 159,188 | 1.592 | 20 | 24 | fits | 149,466 | 145 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 308,811 | 3.088 | 20 | 24 | fits | 150,613 | 178 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 308,745 | 3.087 | 20 | 50 | fits | 150,613 | 178 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 464,353 | 4.644 | 20 | 50 | fits | 156,004 | 204 | 0.428 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 548,561 | 5.486 | 20 | 20 | fits | 84,274 | 38 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 936,894 | 9.369 | 20 | 20 | fits | 42,021 | 16 | 0.756 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 395,934 | 3.959 | 20 | 20 | fits | 150,892 | 190 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 297,361 | 2.974 | 20 | 200 | fits | 150,860 | 197 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 458,262 | 4.583 | 20 | 200 | fits | 150,892 | 190 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 298,285 | 2.983 | 20 | 20 | fits | 150,860 | 197 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 543,576 | 5.436 | 20 | 20 | fits | 84,610 | 37 | 0.732 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 151,065 | 1.511 | 20 | 24 | fits | 149,610 | 145 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 300,935 | 3.009 | 20 | 24 | fits | 150,860 | 197 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 300,869 | 3.009 | 20 | 50 | fits | 150,860 | 197 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 461,990 | 4.620 | 20 | 50 | fits | 150,892 | 190 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 546,534 | 5.465 | 20 | 20 | fits | 84,610 | 37 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 924,196 | 9.242 | 20 | 20 | fits | 39,231 | 18 | 0.842 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 426,101 | 4.261 | 20 | 20 | fits | 155,713 | 204 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 324,538 | 3.245 | 20 | 200 | fits | 153,498 | 185 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 479,635 | 4.796 | 20 | 200 | fits | 155,713 | 204 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 325,462 | 3.255 | 20 | 20 | fits | 153,498 | 185 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 564,027 | 5.640 | 20 | 20 | fits | 83,688 | 31 | 0.752 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 165,403 | 1.654 | 20 | 24 | fits | 149,430 | 146 | 0.379 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 328,112 | 3.281 | 20 | 24 | fits | 153,498 | 185 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 328,046 | 3.280 | 20 | 50 | fits | 153,498 | 185 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 483,363 | 4.834 | 20 | 50 | fits | 155,713 | 204 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 566,985 | 5.670 | 20 | 20 | fits | 83,688 | 31 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 935,907 | 9.359 | 20 | 20 | fits | 33,294 | 13 | 0.822 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 396,407 | 3.964 | 20 | 20 | fits | 156,507 | 193 | 0.417 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 312,237 | 3.122 | 20 | 200 | fits | 150,364 | 196 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 468,128 | 4.681 | 20 | 200 | fits | 156,507 | 193 | 0.417 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 313,161 | 3.132 | 20 | 20 | fits | 150,364 | 196 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 558,541 | 5.585 | 20 | 20 | fits | 89,709 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 166,437 | 1.664 | 20 | 24 | fits | 149,449 | 145 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 315,811 | 3.158 | 20 | 24 | fits | 150,364 | 196 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 315,745 | 3.157 | 20 | 50 | fits | 150,364 | 196 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 471,856 | 4.719 | 20 | 50 | fits | 156,507 | 193 | 0.417 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 561,499 | 5.615 | 20 | 20 | fits | 89,709 | 39 | 0.746 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 941,443 | 9.414 | 20 | 20 | fits | 33,244 | 12 | 0.826 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 389,725 | 3.897 | 20 | 20 | fits | 156,384 | 205 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 305,131 | 3.051 | 20 | 200 | fits | 150,438 | 178 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 460,899 | 4.609 | 20 | 200 | fits | 156,384 | 205 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 306,055 | 3.061 | 20 | 20 | fits | 150,438 | 178 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 560,648 | 5.606 | 20 | 20 | fits | 87,847 | 44 | 0.735 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 159,257 | 1.593 | 20 | 24 | fits | 149,449 | 145 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 308,705 | 3.087 | 20 | 24 | fits | 150,438 | 178 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 308,639 | 3.086 | 20 | 50 | fits | 150,438 | 178 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 464,627 | 4.646 | 20 | 50 | fits | 156,384 | 205 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 563,606 | 5.636 | 20 | 20 | fits | 87,847 | 44 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 935,653 | 9.357 | 20 | 20 | fits | 33,414 | 12 | 0.828 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 436,764 | 4.368 | 20 | 20 | fits | 157,176 | 192 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 352,570 | 3.526 | 20 | 200 | fits | 150,425 | 196 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 509,130 | 5.091 | 20 | 200 | fits | 157,176 | 192 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 353,494 | 3.535 | 20 | 20 | fits | 150,425 | 196 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 593,572 | 5.936 | 20 | 20 | fits | 83,738 | 31 | 0.749 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 206,709 | 2.067 | 20 | 24 | fits | 149,718 | 145 | 0.378 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 356,144 | 3.561 | 20 | 24 | fits | 150,425 | 196 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 356,078 | 3.561 | 20 | 50 | fits | 150,425 | 196 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 512,858 | 5.129 | 20 | 50 | fits | 157,176 | 192 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 596,530 | 5.965 | 20 | 20 | fits | 83,738 | 31 | 0.749 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 982,236 | 9.822 | 20 | 20 | fits | 38,971 | 18 | 0.841 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 392,698 | 3.927 | 20 | 20 | fits | 156,405 | 193 | 0.416 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 308,607 | 3.086 | 20 | 200 | fits | 150,384 | 196 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 464,396 | 4.644 | 20 | 200 | fits | 156,405 | 193 | 0.416 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 309,531 | 3.095 | 20 | 20 | fits | 150,384 | 196 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 548,812 | 5.488 | 20 | 20 | fits | 83,712 | 31 | 0.749 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 162,787 | 1.628 | 20 | 24 | fits | 149,444 | 145 | 0.379 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 312,181 | 3.122 | 20 | 24 | fits | 150,384 | 196 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 312,115 | 3.121 | 20 | 50 | fits | 150,384 | 196 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 468,124 | 4.681 | 20 | 50 | fits | 156,405 | 193 | 0.416 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 551,770 | 5.518 | 20 | 20 | fits | 83,712 | 31 | 0.749 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 937,809 | 9.378 | 20 | 20 | fits | 42,131 | 16 | 0.757 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 389,252 | 3.893 | 20 | 20 | fits | 157,176 | 192 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 305,058 | 3.051 | 20 | 200 | fits | 150,425 | 196 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 461,618 | 4.616 | 20 | 200 | fits | 157,176 | 192 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 305,982 | 3.060 | 20 | 20 | fits | 150,425 | 196 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 546,194 | 5.462 | 20 | 20 | fits | 83,872 | 32 | 0.748 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 159,197 | 1.592 | 20 | 24 | fits | 149,444 | 145 | 0.379 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 308,632 | 3.086 | 20 | 24 | fits | 150,425 | 196 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 308,566 | 3.086 | 20 | 50 | fits | 150,425 | 196 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 465,346 | 4.653 | 20 | 50 | fits | 157,176 | 192 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 549,152 | 5.492 | 20 | 20 | fits | 83,872 | 32 | 0.748 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 934,594 | 9.346 | 20 | 20 | fits | 41,984 | 16 | 0.756 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 386,977 | 3.870 | 20 | 20 | fits | 156,495 | 206 | 0.431 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 302,456 | 3.025 | 20 | 200 | fits | 151,413 | 180 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 458,335 | 4.583 | 20 | 200 | fits | 156,495 | 206 | 0.431 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 303,380 | 3.034 | 20 | 20 | fits | 151,413 | 180 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 557,793 | 5.578 | 20 | 20 | fits | 87,676 | 38 | 0.758 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 155,607 | 1.556 | 20 | 24 | fits | 149,444 | 145 | 0.379 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 306,030 | 3.060 | 20 | 24 | fits | 151,413 | 180 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 305,964 | 3.060 | 20 | 50 | fits | 151,413 | 180 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 462,063 | 4.621 | 20 | 50 | fits | 156,495 | 206 | 0.431 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 560,751 | 5.608 | 20 | 20 | fits | 87,676 | 38 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 930,046 | 9.300 | 20 | 20 | fits | 33,286 | 12 | 0.827 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 414,865 | 4.149 | 20 | 20 | fits | 159,359 | 211 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 299,201 | 2.992 | 20 | 200 | fits | 151,748 | 181 | 0.424 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 468,785 | 4.688 | 20 | 200 | fits | 159,359 | 211 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 300,125 | 3.001 | 20 | 20 | fits | 151,748 | 181 | 0.424 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 559,939 | 5.599 | 20 | 20 | fits | 90,450 | 39 | 0.748 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 152,017 | 1.520 | 20 | 24 | fits | 149,444 | 145 | 0.379 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 302,775 | 3.028 | 20 | 24 | fits | 151,748 | 181 | 0.424 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 302,709 | 3.027 | 20 | 50 | fits | 151,748 | 181 | 0.424 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 472,513 | 4.725 | 20 | 50 | fits | 159,359 | 211 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 562,897 | 5.629 | 20 | 20 | fits | 90,450 | 39 | 0.748 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 901,305 | 9.013 | 20 | 20 | fits | 84,899 | 36 | 0.534 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 417,743 | 4.177 | 20 | 20 | fits | 154,969 | 205 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 306,169 | 3.062 | 20 | 200 | fits | 151,977 | 181 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 460,522 | 4.605 | 20 | 200 | fits | 154,969 | 205 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 307,093 | 3.071 | 20 | 20 | fits | 151,977 | 181 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 546,032 | 5.460 | 20 | 20 | fits | 84,806 | 37 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 148,579 | 1.486 | 20 | 24 | fits | 149,596 | 146 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 309,743 | 3.097 | 20 | 24 | fits | 151,977 | 181 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 309,677 | 3.097 | 20 | 50 | fits | 151,977 | 181 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 464,250 | 4.643 | 20 | 50 | fits | 154,969 | 205 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 548,990 | 5.490 | 20 | 20 | fits | 84,806 | 37 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 920,548 | 9.205 | 20 | 20 | fits | 33,412 | 13 | 0.823 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 395,825 | 3.958 | 20 | 20 | fits | 156,014 | 192 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 292,773 | 2.928 | 20 | 200 | fits | 150,372 | 197 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 448,171 | 4.482 | 20 | 200 | fits | 156,014 | 192 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 293,697 | 2.937 | 20 | 20 | fits | 150,372 | 197 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 533,424 | 5.334 | 20 | 20 | fits | 84,549 | 37 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 146,965 | 1.470 | 20 | 24 | fits | 148,853 | 145 | 0.371 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 296,347 | 2.963 | 20 | 24 | fits | 150,372 | 197 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 296,281 | 2.963 | 20 | 50 | fits | 150,372 | 197 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 451,899 | 4.519 | 20 | 50 | fits | 156,014 | 192 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 536,382 | 5.364 | 20 | 20 | fits | 84,549 | 37 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 925,222 | 9.252 | 20 | 20 | fits | 42,442 | 16 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 397,108 | 3.971 | 20 | 20 | fits | 158,566 | 195 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 301,374 | 3.014 | 20 | 200 | fits | 156,349 | 197 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 459,324 | 4.593 | 20 | 200 | fits | 158,566 | 195 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 302,298 | 3.023 | 20 | 20 | fits | 156,349 | 197 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 543,980 | 5.440 | 20 | 20 | fits | 83,952 | 31 | 0.751 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 149,589 | 1.496 | 20 | 24 | fits | 149,466 | 145 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 304,948 | 3.049 | 20 | 24 | fits | 156,349 | 197 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 304,882 | 3.049 | 20 | 50 | fits | 156,349 | 197 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 463,052 | 4.631 | 20 | 50 | fits | 158,566 | 195 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 546,938 | 5.469 | 20 | 20 | fits | 83,952 | 31 | 0.751 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 927,104 | 9.271 | 20 | 20 | fits | 33,366 | 12 | 0.828 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 402,371 | 4.024 | 20 | 20 | fits | 156,423 | 210 | 0.411 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 299,081 | 2.991 | 20 | 200 | fits | 149,902 | 176 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 454,888 | 4.549 | 20 | 200 | fits | 156,423 | 210 | 0.411 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 300,005 | 3.000 | 20 | 20 | fits | 149,902 | 176 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 554,680 | 5.547 | 20 | 20 | fits | 87,813 | 38 | 0.760 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 153,743 | 1.537 | 20 | 24 | fits | 148,306 | 142 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 302,655 | 3.027 | 20 | 24 | fits | 149,902 | 176 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 302,589 | 3.026 | 20 | 50 | fits | 149,902 | 176 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 458,616 | 4.586 | 20 | 50 | fits | 156,423 | 210 | 0.411 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 557,638 | 5.576 | 20 | 20 | fits | 87,813 | 38 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 896,271 | 8.963 | 20 | 20 | fits | 84,988 | 36 | 0.536 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 395,007 | 3.950 | 20 | 20 | fits | 150,915 | 190 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 296,274 | 2.963 | 20 | 200 | fits | 150,607 | 197 | 0.406 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 457,358 | 4.574 | 20 | 200 | fits | 150,915 | 190 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 297,198 | 2.972 | 20 | 20 | fits | 150,607 | 197 | 0.406 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 543,336 | 5.433 | 20 | 20 | fits | 85,274 | 37 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 150,231 | 1.502 | 20 | 24 | fits | 148,228 | 142 | 0.375 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 299,848 | 2.998 | 20 | 24 | fits | 150,607 | 197 | 0.406 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 299,782 | 2.998 | 20 | 50 | fits | 150,607 | 197 | 0.406 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 461,086 | 4.611 | 20 | 50 | fits | 150,915 | 190 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 546,294 | 5.463 | 20 | 20 | fits | 85,274 | 37 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 923,987 | 9.240 | 20 | 20 | fits | 39,303 | 18 | 0.843 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 401,284 | 4.013 | 20 | 20 | fits | 151,744 | 191 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 302,963 | 3.030 | 20 | 200 | fits | 150,755 | 197 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 454,091 | 4.541 | 20 | 200 | fits | 151,744 | 191 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 303,887 | 3.039 | 20 | 20 | fits | 150,755 | 197 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 539,831 | 5.398 | 20 | 20 | fits | 85,036 | 37 | 0.731 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 146,483 | 1.465 | 20 | 24 | fits | 148,420 | 143 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 306,537 | 3.065 | 20 | 24 | fits | 150,755 | 197 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 306,471 | 3.065 | 20 | 50 | fits | 150,755 | 197 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 457,819 | 4.578 | 20 | 50 | fits | 151,744 | 191 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 542,789 | 5.428 | 20 | 20 | fits | 85,036 | 37 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,013,734 | 10.137 | 20 | 20 | fits | 47,121 | 23 | 0.792 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 390,051 | 3.901 | 20 | 20 | fits | 156,220 | 205 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 305,451 | 3.055 | 20 | 200 | fits | 151,285 | 180 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 461,055 | 4.611 | 20 | 200 | fits | 156,220 | 205 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 306,375 | 3.064 | 20 | 20 | fits | 151,285 | 180 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 545,793 | 5.458 | 20 | 20 | fits | 84,034 | 31 | 0.752 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 158,730 | 1.587 | 20 | 24 | fits | 147,984 | 142 | 0.371 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 309,025 | 3.090 | 20 | 24 | fits | 151,285 | 180 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 308,959 | 3.090 | 20 | 50 | fits | 151,285 | 180 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 464,783 | 4.648 | 20 | 50 | fits | 156,220 | 205 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 548,751 | 5.488 | 20 | 20 | fits | 84,034 | 31 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,012,431 | 10.124 | 20 | 20 | fits | 42,149 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 403,729 | 4.037 | 20 | 20 | fits | 155,146 | 204 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 302,459 | 3.025 | 20 | 200 | fits | 151,326 | 180 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 456,989 | 4.570 | 20 | 200 | fits | 155,146 | 204 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 303,383 | 3.034 | 20 | 20 | fits | 151,326 | 180 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 547,831 | 5.478 | 20 | 20 | fits | 90,138 | 39 | 0.744 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 155,697 | 1.557 | 20 | 24 | fits | 148,146 | 142 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 306,033 | 3.060 | 20 | 24 | fits | 151,326 | 180 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 305,967 | 3.060 | 20 | 50 | fits | 151,326 | 180 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 460,717 | 4.607 | 20 | 50 | fits | 155,146 | 204 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 550,789 | 5.508 | 20 | 20 | fits | 90,138 | 39 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,007,349 | 10.073 | 20 | 20 | fits | 33,244 | 12 | 0.826 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 400,587 | 4.006 | 20 | 20 | fits | 156,046 | 209 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 297,297 | 2.973 | 20 | 200 | fits | 149,772 | 176 | 0.424 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 452,727 | 4.527 | 20 | 200 | fits | 156,046 | 209 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 298,221 | 2.982 | 20 | 20 | fits | 149,772 | 176 | 0.424 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 543,705 | 5.437 | 20 | 20 | fits | 90,274 | 40 | 0.744 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 152,089 | 1.521 | 20 | 24 | fits | 148,146 | 142 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 300,871 | 3.009 | 20 | 24 | fits | 149,772 | 176 | 0.424 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 300,805 | 3.008 | 20 | 50 | fits | 149,772 | 176 | 0.424 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 456,455 | 4.565 | 20 | 50 | fits | 156,046 | 209 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 546,663 | 5.467 | 20 | 20 | fits | 90,274 | 40 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,002,546 | 10.025 | 20 | 20 | fits | 33,302 | 12 | 0.827 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 386,296 | 3.863 | 20 | 20 | fits | 155,058 | 190 | 0.447 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 294,173 | 2.942 | 20 | 200 | fits | 150,256 | 196 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 448,615 | 4.486 | 20 | 200 | fits | 155,058 | 190 | 0.447 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 295,097 | 2.951 | 20 | 20 | fits | 150,256 | 196 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 625,166 | 6.252 | 20 | 20 | fits | 88,836 | 44 | 0.741 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 148,481 | 1.485 | 20 | 24 | fits | 148,146 | 142 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 297,747 | 2.977 | 20 | 24 | fits | 150,256 | 196 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 297,681 | 2.977 | 20 | 50 | fits | 150,256 | 196 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 452,343 | 4.523 | 20 | 50 | fits | 155,058 | 190 | 0.447 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 628,124 | 6.281 | 20 | 20 | fits | 88,836 | 44 | 0.741 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,000,174 | 10.002 | 20 | 20 | fits | 33,414 | 12 | 0.828 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 407,141 | 4.071 | 20 | 20 | fits | 150,221 | 190 | 0.467 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 290,609 | 2.906 | 20 | 200 | fits | 150,300 | 198 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 450,921 | 4.509 | 20 | 200 | fits | 150,221 | 190 | 0.467 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 291,533 | 2.915 | 20 | 20 | fits | 150,300 | 198 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 614,129 | 6.141 | 20 | 20 | fits | 85,762 | 43 | 0.709 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 144,873 | 1.449 | 20 | 24 | fits | 148,146 | 142 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 294,183 | 2.942 | 20 | 24 | fits | 150,300 | 198 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 294,117 | 2.941 | 20 | 50 | fits | 150,300 | 198 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 454,649 | 4.546 | 20 | 50 | fits | 150,221 | 190 | 0.467 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 617,087 | 6.171 | 20 | 20 | fits | 85,762 | 43 | 0.709 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 997,597 | 9.976 | 20 | 20 | fits | 41,995 | 16 | 0.754 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 391,260 | 3.913 | 20 | 20 | fits | 157,279 | 192 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 306,940 | 3.069 | 20 | 200 | fits | 150,380 | 196 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 463,603 | 4.636 | 20 | 200 | fits | 157,279 | 192 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 307,864 | 3.079 | 20 | 20 | fits | 150,380 | 196 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 548,440 | 5.484 | 20 | 20 | fits | 84,133 | 32 | 0.751 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 161,124 | 1.611 | 20 | 24 | fits | 148,306 | 142 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 310,514 | 3.105 | 20 | 24 | fits | 150,380 | 196 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 310,448 | 3.104 | 20 | 50 | fits | 150,380 | 196 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 467,331 | 4.673 | 20 | 50 | fits | 157,279 | 192 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 551,398 | 5.514 | 20 | 20 | fits | 84,133 | 32 | 0.751 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 931,006 | 9.310 | 20 | 20 | fits | 33,302 | 12 | 0.827 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 389,063 | 3.891 | 20 | 20 | fits | 156,551 | 206 | 0.431 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 304,463 | 3.045 | 20 | 200 | fits | 151,415 | 180 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 460,398 | 4.604 | 20 | 200 | fits | 156,551 | 206 | 0.431 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 305,387 | 3.054 | 20 | 20 | fits | 151,415 | 180 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 560,241 | 5.602 | 20 | 20 | fits | 87,858 | 38 | 0.760 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 157,612 | 1.576 | 20 | 24 | fits | 148,228 | 142 | 0.375 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 308,037 | 3.080 | 20 | 24 | fits | 151,415 | 180 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 307,971 | 3.080 | 20 | 50 | fits | 151,415 | 180 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 464,126 | 4.641 | 20 | 50 | fits | 156,551 | 206 | 0.431 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 563,199 | 5.632 | 20 | 20 | fits | 87,858 | 38 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 932,660 | 9.327 | 20 | 20 | fits | 33,428 | 12 | 0.828 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 417,027 | 4.170 | 20 | 20 | fits | 159,336 | 211 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 301,286 | 3.013 | 20 | 200 | fits | 151,750 | 181 | 0.423 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 470,924 | 4.709 | 20 | 200 | fits | 159,336 | 211 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 302,210 | 3.022 | 20 | 20 | fits | 151,750 | 181 | 0.423 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 556,203 | 5.562 | 20 | 20 | fits | 84,575 | 31 | 0.758 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 154,100 | 1.541 | 20 | 24 | fits | 148,228 | 142 | 0.375 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 304,860 | 3.049 | 20 | 24 | fits | 151,750 | 181 | 0.423 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 304,794 | 3.048 | 20 | 50 | fits | 151,750 | 181 | 0.423 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 474,652 | 4.747 | 20 | 50 | fits | 159,336 | 211 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 559,161 | 5.592 | 20 | 20 | fits | 84,575 | 31 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 928,301 | 9.283 | 20 | 20 | fits | 33,288 | 12 | 0.827 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 413,201 | 4.132 | 20 | 20 | fits | 157,298 | 209 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 298,105 | 2.981 | 20 | 200 | fits | 152,081 | 182 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 465,818 | 4.658 | 20 | 200 | fits | 157,298 | 209 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 299,029 | 2.990 | 20 | 20 | fits | 152,081 | 182 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 551,188 | 5.512 | 20 | 20 | fits | 84,666 | 31 | 0.759 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 150,588 | 1.506 | 20 | 24 | fits | 148,228 | 142 | 0.375 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 301,679 | 3.017 | 20 | 24 | fits | 152,081 | 182 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 301,613 | 3.016 | 20 | 50 | fits | 152,081 | 182 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 469,546 | 4.695 | 20 | 50 | fits | 157,298 | 209 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 554,146 | 5.541 | 20 | 20 | fits | 84,666 | 31 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 923,185 | 9.232 | 20 | 20 | fits | 33,288 | 12 | 0.827 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 400,924 | 4.009 | 20 | 20 | fits | 151,091 | 192 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 302,917 | 3.029 | 20 | 200 | fits | 150,754 | 197 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 453,392 | 4.534 | 20 | 200 | fits | 151,091 | 192 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 303,841 | 3.038 | 20 | 20 | fits | 150,754 | 197 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 537,210 | 5.372 | 20 | 20 | fits | 83,114 | 41 | 0.752 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 146,438 | 1.464 | 20 | 24 | fits | 148,375 | 143 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 306,491 | 3.065 | 20 | 24 | fits | 150,754 | 197 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 306,425 | 3.064 | 20 | 50 | fits | 150,754 | 197 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 457,120 | 4.571 | 20 | 50 | fits | 151,091 | 192 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 540,168 | 5.402 | 20 | 20 | fits | 83,114 | 41 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 920,702 | 9.207 | 20 | 20 | fits | 41,995 | 16 | 0.754 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 399,221 | 3.992 | 20 | 20 | fits | 155,647 | 188 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 306,795 | 3.068 | 20 | 200 | fits | 150,297 | 196 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 461,826 | 4.618 | 20 | 200 | fits | 155,647 | 188 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 307,719 | 3.077 | 20 | 20 | fits | 150,297 | 196 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 547,119 | 5.471 | 20 | 20 | fits | 84,589 | 37 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 161,062 | 1.611 | 20 | 24 | fits | 148,146 | 142 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 310,369 | 3.104 | 20 | 24 | fits | 150,297 | 196 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 310,303 | 3.103 | 20 | 50 | fits | 150,297 | 196 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 465,554 | 4.656 | 20 | 50 | fits | 155,647 | 188 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 550,077 | 5.501 | 20 | 20 | fits | 84,589 | 37 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 940,007 | 9.400 | 20 | 20 | fits | 42,149 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 396,942 | 3.969 | 20 | 20 | fits | 154,629 | 201 | 0.459 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 304,222 | 3.042 | 20 | 200 | fits | 151,332 | 180 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 458,235 | 4.582 | 20 | 200 | fits | 154,629 | 201 | 0.459 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 305,146 | 3.051 | 20 | 20 | fits | 151,332 | 180 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 543,525 | 5.435 | 20 | 20 | fits | 84,586 | 37 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 157,454 | 1.575 | 20 | 24 | fits | 148,146 | 142 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 307,796 | 3.078 | 20 | 24 | fits | 151,332 | 180 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 307,730 | 3.077 | 20 | 50 | fits | 151,332 | 180 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 461,963 | 4.620 | 20 | 50 | fits | 154,629 | 201 | 0.459 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 546,483 | 5.465 | 20 | 20 | fits | 84,586 | 37 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 935,558 | 9.356 | 20 | 20 | fits | 42,021 | 16 | 0.756 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 401,318 | 4.013 | 20 | 20 | fits | 155,309 | 203 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 299,724 | 2.997 | 20 | 200 | fits | 150,442 | 178 | 0.432 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 454,417 | 4.544 | 20 | 200 | fits | 155,309 | 203 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 300,648 | 3.006 | 20 | 20 | fits | 150,442 | 178 | 0.432 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 539,758 | 5.398 | 20 | 20 | fits | 84,637 | 38 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 153,846 | 1.538 | 20 | 24 | fits | 148,146 | 142 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 303,298 | 3.033 | 20 | 24 | fits | 150,442 | 178 | 0.432 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 303,232 | 3.032 | 20 | 50 | fits | 150,442 | 178 | 0.432 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 458,145 | 4.581 | 20 | 50 | fits | 155,309 | 203 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 542,716 | 5.427 | 20 | 20 | fits | 84,637 | 38 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 931,043 | 9.310 | 20 | 20 | fits | 42,021 | 16 | 0.756 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 415,364 | 4.154 | 20 | 20 | fits | 159,045 | 195 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 319,477 | 3.195 | 20 | 200 | fits | 150,810 | 197 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 477,906 | 4.779 | 20 | 200 | fits | 159,045 | 195 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 320,401 | 3.204 | 20 | 20 | fits | 150,810 | 197 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 562,443 | 5.624 | 20 | 20 | fits | 83,833 | 31 | 0.754 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 162,942 | 1.629 | 20 | 24 | fits | 148,464 | 143 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 323,051 | 3.231 | 20 | 24 | fits | 150,810 | 197 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 322,985 | 3.230 | 20 | 50 | fits | 150,810 | 197 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 481,634 | 4.816 | 20 | 50 | fits | 159,045 | 195 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 565,401 | 5.654 | 20 | 20 | fits | 83,833 | 31 | 0.754 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 903,785 | 9.038 | 20 | 20 | fits | 84,899 | 36 | 0.534 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 403,107 | 4.031 | 20 | 20 | fits | 156,623 | 205 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 318,295 | 3.183 | 20 | 200 | fits | 153,142 | 185 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 474,302 | 4.743 | 20 | 200 | fits | 156,623 | 205 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 319,219 | 3.192 | 20 | 20 | fits | 153,142 | 185 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 558,845 | 5.588 | 20 | 20 | fits | 83,839 | 31 | 0.755 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 159,428 | 1.594 | 20 | 24 | fits | 148,384 | 143 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 321,869 | 3.219 | 20 | 24 | fits | 153,142 | 185 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 321,803 | 3.218 | 20 | 50 | fits | 153,142 | 185 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 478,030 | 4.780 | 20 | 50 | fits | 156,623 | 205 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 561,803 | 5.618 | 20 | 20 | fits | 83,839 | 31 | 0.755 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 1,016,132 | 10.161 | 20 | 20 | fits | 38,114 | 20 | 0.827 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 384,167 | 3.842 | 20 | 20 | fits | 156,171 | 205 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 299,567 | 2.996 | 20 | 200 | fits | 151,342 | 180 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 455,122 | 4.551 | 20 | 200 | fits | 156,171 | 205 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 300,491 | 3.005 | 20 | 20 | fits | 151,342 | 180 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 539,360 | 5.394 | 20 | 20 | fits | 83,534 | 31 | 0.752 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 152,789 | 1.528 | 20 | 24 | fits | 148,134 | 142 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 303,141 | 3.031 | 20 | 24 | fits | 151,342 | 180 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 303,075 | 3.031 | 20 | 50 | fits | 151,342 | 180 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 458,850 | 4.588 | 20 | 50 | fits | 156,171 | 205 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 542,318 | 5.423 | 20 | 20 | fits | 83,534 | 31 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,006,423 | 10.064 | 20 | 20 | fits | 33,522 | 12 | 0.830 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 397,270 | 3.973 | 20 | 20 | fits | 155,146 | 204 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 296,000 | 2.960 | 20 | 200 | fits | 151,383 | 180 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 450,530 | 4.505 | 20 | 200 | fits | 155,146 | 204 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 296,924 | 2.969 | 20 | 20 | fits | 151,383 | 180 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 534,698 | 5.347 | 20 | 20 | fits | 83,464 | 31 | 0.750 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 149,181 | 1.492 | 20 | 24 | fits | 148,134 | 142 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 299,574 | 2.996 | 20 | 24 | fits | 151,383 | 180 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 299,508 | 2.995 | 20 | 50 | fits | 151,383 | 180 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 454,258 | 4.543 | 20 | 50 | fits | 155,146 | 204 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 537,656 | 5.377 | 20 | 20 | fits | 83,464 | 31 | 0.750 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,001,781 | 10.018 | 20 | 20 | fits | 33,383 | 12 | 0.828 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 395,254 | 3.953 | 20 | 20 | fits | 156,423 | 210 | 0.411 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 291,964 | 2.920 | 20 | 200 | fits | 150,955 | 181 | 0.423 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 447,771 | 4.478 | 20 | 200 | fits | 156,423 | 210 | 0.411 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 292,888 | 2.929 | 20 | 20 | fits | 150,955 | 181 | 0.423 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 543,868 | 5.439 | 20 | 20 | fits | 84,156 | 42 | 0.772 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 145,573 | 1.456 | 20 | 24 | fits | 148,134 | 142 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 295,538 | 2.955 | 20 | 24 | fits | 150,955 | 181 | 0.423 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 295,472 | 2.955 | 20 | 50 | fits | 150,955 | 181 | 0.423 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 451,499 | 4.515 | 20 | 50 | fits | 156,423 | 210 | 0.411 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 546,826 | 5.468 | 20 | 20 | fits | 84,156 | 42 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 999,111 | 9.991 | 20 | 20 | fits | 33,383 | 12 | 0.828 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 403,131 | 4.031 | 20 | 20 | fits | 157,954 | 195 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 307,960 | 3.080 | 20 | 200 | fits | 150,284 | 196 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 465,298 | 4.653 | 20 | 200 | fits | 157,954 | 195 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 308,884 | 3.089 | 20 | 20 | fits | 150,284 | 196 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 642,003 | 6.420 | 20 | 20 | fits | 85,647 | 38 | 0.737 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 162,240 | 1.622 | 20 | 24 | fits | 148,134 | 142 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 311,534 | 3.115 | 20 | 24 | fits | 150,284 | 196 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 311,468 | 3.115 | 20 | 50 | fits | 150,284 | 196 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 469,026 | 4.690 | 20 | 50 | fits | 157,954 | 195 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 644,961 | 6.450 | 20 | 20 | fits | 85,647 | 38 | 0.737 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,016,832 | 10.168 | 20 | 20 | fits | 33,325 | 12 | 0.827 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 411,543 | 4.115 | 20 | 20 | fits | 157,498 | 208 | 0.468 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 305,502 | 3.055 | 20 | 200 | fits | 151,434 | 181 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 473,224 | 4.732 | 20 | 200 | fits | 157,498 | 208 | 0.468 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 306,426 | 3.064 | 20 | 20 | fits | 151,434 | 181 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 639,075 | 6.391 | 20 | 20 | fits | 84,241 | 38 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 158,632 | 1.586 | 20 | 24 | fits | 148,134 | 142 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 309,076 | 3.091 | 20 | 24 | fits | 151,434 | 181 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 309,010 | 3.090 | 20 | 50 | fits | 151,434 | 181 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 476,952 | 4.770 | 20 | 50 | fits | 157,498 | 208 | 0.468 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 642,033 | 6.420 | 20 | 20 | fits | 84,241 | 38 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,013,722 | 10.137 | 20 | 20 | fits | 33,325 | 12 | 0.827 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 505,347 | 5.053 | 20 | 20 | fits | 158,935 | 212 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 309,870 | 3.099 | 20 | 200 | fits | 149,079 | 174 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 549,029 | 5.490 | 20 | 200 | fits | 158,935 | 212 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 310,794 | 3.108 | 20 | 20 | fits | 149,079 | 174 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 634,280 | 6.343 | 20 | 20 | fits | 84,547 | 37 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 155,189 | 1.552 | 20 | 24 | fits | 148,299 | 143 | 0.375 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 313,444 | 3.134 | 20 | 24 | fits | 149,079 | 174 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 313,378 | 3.134 | 20 | 50 | fits | 149,079 | 174 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 552,757 | 5.528 | 20 | 50 | fits | 158,935 | 212 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 637,238 | 6.372 | 20 | 20 | fits | 84,547 | 37 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,025,960 | 10.260 | 20 | 20 | fits | 42,442 | 16 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 382,749 | 3.827 | 20 | 20 | fits | 156,502 | 206 | 0.431 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 298,149 | 2.981 | 20 | 200 | fits | 151,212 | 180 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 454,035 | 4.540 | 20 | 200 | fits | 156,502 | 206 | 0.431 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 299,073 | 2.991 | 20 | 20 | fits | 151,212 | 180 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 553,398 | 5.534 | 20 | 20 | fits | 87,378 | 38 | 0.760 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 151,501 | 1.515 | 20 | 24 | fits | 148,294 | 142 | 0.375 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 301,723 | 3.017 | 20 | 24 | fits | 151,212 | 180 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 301,657 | 3.017 | 20 | 50 | fits | 151,212 | 180 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 457,763 | 4.578 | 20 | 50 | fits | 156,502 | 206 | 0.431 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 556,356 | 5.564 | 20 | 20 | fits | 87,378 | 38 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 894,989 | 8.950 | 20 | 20 | fits | 84,988 | 36 | 0.536 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 409,885 | 4.099 | 20 | 20 | fits | 159,137 | 210 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 294,343 | 2.943 | 20 | 200 | fits | 152,628 | 186 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 463,782 | 4.638 | 20 | 200 | fits | 159,137 | 210 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 295,267 | 2.953 | 20 | 20 | fits | 152,628 | 186 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 548,561 | 5.486 | 20 | 20 | fits | 84,075 | 31 | 0.758 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 146,279 | 1.463 | 20 | 24 | fits | 148,216 | 142 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 297,917 | 2.979 | 20 | 24 | fits | 152,628 | 186 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 297,851 | 2.979 | 20 | 50 | fits | 152,628 | 186 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 467,510 | 4.675 | 20 | 50 | fits | 159,137 | 210 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 551,519 | 5.515 | 20 | 20 | fits | 84,075 | 31 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 889,928 | 8.899 | 20 | 20 | fits | 84,899 | 36 | 0.534 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 408,074 | 4.081 | 20 | 20 | fits | 150,046 | 207 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 301,888 | 3.019 | 20 | 200 | fits | 151,577 | 181 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 451,318 | 4.513 | 20 | 200 | fits | 150,046 | 207 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 302,812 | 3.028 | 20 | 20 | fits | 151,577 | 181 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 536,476 | 5.365 | 20 | 20 | fits | 84,454 | 37 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 144,669 | 1.447 | 20 | 24 | fits | 148,408 | 143 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 305,462 | 3.055 | 20 | 24 | fits | 151,577 | 181 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 305,396 | 3.054 | 20 | 50 | fits | 151,577 | 181 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 455,046 | 4.550 | 20 | 50 | fits | 150,046 | 207 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 539,434 | 5.394 | 20 | 20 | fits | 84,454 | 37 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 917,430 | 9.174 | 20 | 20 | fits | 42,074 | 17 | 0.753 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 386,437 | 3.864 | 20 | 20 | fits | 156,461 | 193 | 0.416 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 302,267 | 3.023 | 20 | 200 | fits | 150,326 | 196 | 0.404 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 458,112 | 4.581 | 20 | 200 | fits | 156,461 | 193 | 0.416 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 303,191 | 3.032 | 20 | 20 | fits | 150,326 | 196 | 0.404 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 542,318 | 5.423 | 20 | 20 | fits | 83,502 | 31 | 0.751 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 156,505 | 1.565 | 20 | 24 | fits | 148,017 | 142 | 0.371 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 305,841 | 3.058 | 20 | 24 | fits | 150,326 | 196 | 0.404 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 305,775 | 3.058 | 20 | 50 | fits | 150,326 | 196 | 0.404 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 461,840 | 4.618 | 20 | 50 | fits | 156,461 | 193 | 0.416 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 545,276 | 5.453 | 20 | 20 | fits | 83,502 | 31 | 0.751 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 931,320 | 9.313 | 20 | 20 | fits | 42,358 | 16 | 0.766 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 383,633 | 3.836 | 20 | 20 | fits | 157,279 | 192 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 299,313 | 2.993 | 20 | 200 | fits | 150,367 | 196 | 0.404 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 455,976 | 4.560 | 20 | 200 | fits | 157,279 | 192 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 300,237 | 3.002 | 20 | 20 | fits | 150,367 | 196 | 0.404 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 546,379 | 5.464 | 20 | 20 | fits | 89,699 | 39 | 0.745 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 153,510 | 1.535 | 20 | 24 | fits | 148,134 | 142 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 302,887 | 3.029 | 20 | 24 | fits | 150,367 | 196 | 0.404 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 302,821 | 3.028 | 20 | 50 | fits | 150,367 | 196 | 0.404 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 459,704 | 4.597 | 20 | 50 | fits | 157,279 | 192 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 549,337 | 5.493 | 20 | 20 | fits | 89,699 | 39 | 0.745 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 930,281 | 9.303 | 20 | 20 | fits | 33,348 | 12 | 0.828 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 381,280 | 3.813 | 20 | 20 | fits | 156,220 | 205 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 296,680 | 2.967 | 20 | 200 | fits | 151,342 | 180 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 452,284 | 4.523 | 20 | 200 | fits | 156,220 | 205 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 297,604 | 2.976 | 20 | 20 | fits | 151,342 | 180 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 542,818 | 5.428 | 20 | 20 | fits | 89,830 | 40 | 0.744 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 149,902 | 1.499 | 20 | 24 | fits | 148,134 | 142 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 300,254 | 3.003 | 20 | 24 | fits | 151,342 | 180 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 300,188 | 3.002 | 20 | 50 | fits | 151,342 | 180 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 456,012 | 4.560 | 20 | 50 | fits | 156,220 | 205 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 545,776 | 5.458 | 20 | 20 | fits | 89,830 | 40 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 925,241 | 9.252 | 20 | 20 | fits | 33,302 | 12 | 0.827 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 403,470 | 4.035 | 20 | 20 | fits | 153,853 | 201 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 294,203 | 2.942 | 20 | 200 | fits | 152,509 | 185 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 447,440 | 4.474 | 20 | 200 | fits | 153,853 | 201 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 295,127 | 2.951 | 20 | 20 | fits | 152,509 | 185 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 547,060 | 5.471 | 20 | 20 | fits | 87,544 | 44 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 146,258 | 1.463 | 20 | 24 | fits | 148,134 | 142 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 297,777 | 2.978 | 20 | 24 | fits | 152,509 | 185 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 297,711 | 2.977 | 20 | 50 | fits | 152,509 | 185 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 451,168 | 4.512 | 20 | 50 | fits | 153,853 | 201 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 550,018 | 5.500 | 20 | 20 | fits | 87,544 | 44 | 0.733 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 922,065 | 9.221 | 20 | 20 | fits | 33,414 | 12 | 0.828 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 424,314 | 4.243 | 20 | 20 | fits | 151,898 | 192 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 314,760 | 3.148 | 20 | 200 | fits | 156,449 | 198 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 476,910 | 4.769 | 20 | 200 | fits | 151,898 | 192 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 315,684 | 3.157 | 20 | 20 | fits | 156,449 | 198 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 562,341 | 5.623 | 20 | 20 | fits | 84,727 | 37 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 162,875 | 1.629 | 20 | 24 | fits | 148,134 | 142 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 318,334 | 3.183 | 20 | 24 | fits | 156,449 | 198 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 318,268 | 3.183 | 20 | 50 | fits | 156,449 | 198 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 480,638 | 4.806 | 20 | 50 | fits | 151,898 | 192 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 565,299 | 5.653 | 20 | 20 | fits | 84,727 | 37 | 0.733 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 937,055 | 9.371 | 20 | 20 | fits | 33,325 | 12 | 0.827 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 388,171 | 3.882 | 20 | 20 | fits | 156,461 | 193 | 0.416 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 304,001 | 3.040 | 20 | 200 | fits | 150,273 | 196 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 459,846 | 4.598 | 20 | 200 | fits | 156,461 | 193 | 0.416 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 304,925 | 3.049 | 20 | 20 | fits | 150,273 | 196 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 544,416 | 5.444 | 20 | 20 | fits | 83,866 | 31 | 0.751 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 158,292 | 1.583 | 20 | 24 | fits | 148,236 | 142 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 307,575 | 3.076 | 20 | 24 | fits | 150,273 | 196 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 307,509 | 3.075 | 20 | 50 | fits | 150,273 | 196 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 463,574 | 4.636 | 20 | 50 | fits | 156,461 | 193 | 0.416 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 547,374 | 5.474 | 20 | 20 | fits | 83,866 | 31 | 0.751 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 927,326 | 9.273 | 20 | 20 | fits | 33,743 | 12 | 0.836 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 384,820 | 3.848 | 20 | 20 | fits | 157,232 | 192 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 300,547 | 3.005 | 20 | 200 | fits | 150,314 | 196 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 457,163 | 4.572 | 20 | 200 | fits | 157,232 | 192 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 301,471 | 3.015 | 20 | 20 | fits | 150,314 | 196 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 541,759 | 5.418 | 20 | 20 | fits | 83,892 | 31 | 0.751 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 154,797 | 1.548 | 20 | 24 | fits | 148,132 | 142 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 304,121 | 3.041 | 20 | 24 | fits | 150,314 | 196 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 304,055 | 3.041 | 20 | 50 | fits | 150,314 | 196 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 460,891 | 4.609 | 20 | 50 | fits | 157,232 | 192 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 544,717 | 5.447 | 20 | 20 | fits | 83,892 | 31 | 0.751 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 930,513 | 9.305 | 20 | 20 | fits | 38,992 | 18 | 0.841 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 382,527 | 3.825 | 20 | 20 | fits | 156,220 | 205 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 297,927 | 2.979 | 20 | 200 | fits | 151,302 | 180 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 453,531 | 4.535 | 20 | 200 | fits | 156,220 | 205 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 298,851 | 2.989 | 20 | 20 | fits | 151,302 | 180 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 538,267 | 5.383 | 20 | 20 | fits | 84,032 | 32 | 0.751 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 151,189 | 1.512 | 20 | 24 | fits | 148,132 | 142 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 301,501 | 3.015 | 20 | 24 | fits | 151,302 | 180 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 301,435 | 3.014 | 20 | 50 | fits | 151,302 | 180 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 457,259 | 4.573 | 20 | 50 | fits | 156,220 | 205 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 541,225 | 5.412 | 20 | 20 | fits | 84,032 | 32 | 0.751 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,003,991 | 10.040 | 20 | 20 | fits | 41,958 | 16 | 0.754 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 395,431 | 3.954 | 20 | 20 | fits | 155,477 | 205 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 294,161 | 2.942 | 20 | 200 | fits | 152,469 | 185 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 449,022 | 4.490 | 20 | 200 | fits | 155,477 | 205 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 295,085 | 2.951 | 20 | 20 | fits | 152,469 | 185 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 548,707 | 5.487 | 20 | 20 | fits | 87,706 | 38 | 0.759 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 146,256 | 1.463 | 20 | 24 | fits | 148,132 | 142 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 297,735 | 2.977 | 20 | 24 | fits | 152,469 | 185 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 297,669 | 2.977 | 20 | 50 | fits | 152,469 | 185 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 452,750 | 4.527 | 20 | 50 | fits | 155,477 | 205 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 551,665 | 5.517 | 20 | 20 | fits | 87,706 | 38 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 998,344 | 9.983 | 20 | 20 | fits | 33,377 | 12 | 0.828 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 399,100 | 3.991 | 20 | 20 | fits | 151,161 | 221 | 0.436 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 290,453 | 2.905 | 20 | 200 | fits | 149,144 | 199 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 451,783 | 4.518 | 20 | 200 | fits | 151,161 | 221 | 0.436 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 291,377 | 2.914 | 20 | 20 | fits | 149,144 | 199 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 535,710 | 5.357 | 20 | 20 | fits | 83,223 | 41 | 0.753 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 145,873 | 1.459 | 20 | 24 | fits | 150,032 | 111 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 294,027 | 2.940 | 20 | 24 | fits | 149,144 | 199 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 293,961 | 2.940 | 20 | 50 | fits | 149,144 | 199 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 455,511 | 4.555 | 20 | 50 | fits | 151,161 | 221 | 0.436 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 538,668 | 5.387 | 20 | 20 | fits | 83,223 | 41 | 0.753 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 996,651 | 9.967 | 20 | 20 | fits | 41,995 | 16 | 0.754 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 421,498 | 4.215 | 20 | 20 | fits | 157,521 | 191 | 0.454 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 317,446 | 3.174 | 20 | 200 | fits | 150,880 | 197 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 474,351 | 4.744 | 20 | 200 | fits | 157,521 | 191 | 0.454 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 318,370 | 3.184 | 20 | 20 | fits | 150,880 | 197 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 637,417 | 6.374 | 20 | 20 | fits | 84,896 | 38 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 160,841 | 1.608 | 20 | 24 | fits | 148,333 | 143 | 0.375 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 321,020 | 3.210 | 20 | 24 | fits | 150,880 | 197 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 320,954 | 3.210 | 20 | 50 | fits | 150,880 | 197 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 478,079 | 4.781 | 20 | 50 | fits | 157,521 | 191 | 0.454 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 640,375 | 6.404 | 20 | 20 | fits | 84,896 | 38 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,028,343 | 10.283 | 20 | 20 | fits | 38,382 | 19 | 0.846 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 492,468 | 4.925 | 20 | 20 | fits | 157,471 | 192 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 330,823 | 3.308 | 20 | 200 | fits | 155,890 | 198 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 565,043 | 5.650 | 20 | 200 | fits | 157,471 | 192 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 331,747 | 3.317 | 20 | 20 | fits | 155,890 | 198 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 565,747 | 5.657 | 20 | 20 | fits | 157,471 | 192 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 179,497 | 1.795 | 20 | 24 | fits | 158,724 | 153 | 0.351 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 334,397 | 3.344 | 20 | 24 | fits | 155,890 | 198 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 334,331 | 3.343 | 20 | 50 | fits | 155,890 | 198 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 568,771 | 5.688 | 20 | 50 | fits | 157,471 | 192 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 651,389 | 6.514 | 20 | 20 | fits | 82,684 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 997,987 | 9.980 | 20 | 20 | fits | 85,338 | 36 | 0.549 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 458,321 | 4.583 | 20 | 20 | fits | 156,087 | 204 | 0.427 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 296,597 | 2.966 | 20 | 200 | fits | 150,490 | 178 | 0.432 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 529,433 | 5.294 | 20 | 200 | fits | 156,087 | 204 | 0.427 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 297,521 | 2.975 | 20 | 20 | fits | 150,490 | 178 | 0.432 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 614,674 | 6.147 | 20 | 20 | fits | 84,537 | 37 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 150,671 | 1.507 | 20 | 24 | fits | 148,198 | 142 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 300,171 | 3.002 | 20 | 24 | fits | 150,490 | 178 | 0.432 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 300,105 | 3.001 | 20 | 50 | fits | 150,490 | 178 | 0.432 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 533,161 | 5.332 | 20 | 50 | fits | 156,087 | 204 | 0.427 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 617,632 | 6.176 | 20 | 20 | fits | 84,537 | 37 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,006,501 | 10.065 | 20 | 20 | fits | 42,021 | 16 | 0.756 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 394,385 | 3.944 | 20 | 20 | fits | 156,623 | 205 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 309,573 | 3.096 | 20 | 200 | fits | 153,232 | 185 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 465,580 | 4.656 | 20 | 200 | fits | 156,623 | 205 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 310,497 | 3.105 | 20 | 20 | fits | 153,232 | 185 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 550,516 | 5.505 | 20 | 20 | fits | 84,232 | 31 | 0.754 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 150,699 | 1.507 | 20 | 24 | fits | 148,528 | 143 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 313,147 | 3.131 | 20 | 24 | fits | 153,232 | 185 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 313,081 | 3.131 | 20 | 50 | fits | 153,232 | 185 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 469,308 | 4.693 | 20 | 50 | fits | 156,623 | 205 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 553,474 | 5.535 | 20 | 20 | fits | 84,232 | 31 | 0.754 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 891,817 | 8.918 | 20 | 20 | fits | 84,899 | 36 | 0.534 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 409,569 | 4.096 | 20 | 20 | fits | 158,507 | 210 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 305,358 | 3.054 | 20 | 200 | fits | 153,205 | 185 | 0.423 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 463,249 | 4.632 | 20 | 200 | fits | 158,507 | 210 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 306,282 | 3.063 | 20 | 20 | fits | 153,205 | 185 | 0.423 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 548,181 | 5.482 | 20 | 20 | fits | 84,228 | 31 | 0.753 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 146,511 | 1.465 | 20 | 24 | fits | 148,448 | 143 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 308,932 | 3.089 | 20 | 24 | fits | 153,205 | 185 | 0.423 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 308,866 | 3.089 | 20 | 50 | fits | 153,205 | 185 | 0.423 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 466,977 | 4.670 | 20 | 50 | fits | 158,507 | 210 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 551,139 | 5.511 | 20 | 20 | fits | 84,228 | 31 | 0.753 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 889,482 | 8.895 | 20 | 20 | fits | 84,899 | 36 | 0.534 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 409,546 | 4.095 | 20 | 20 | fits | 156,092 | 209 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 306,256 | 3.063 | 20 | 200 | fits | 149,919 | 176 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 461,732 | 4.617 | 20 | 200 | fits | 156,092 | 209 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 307,180 | 3.072 | 20 | 20 | fits | 149,919 | 176 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 546,235 | 5.462 | 20 | 20 | fits | 83,799 | 31 | 0.750 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 160,901 | 1.609 | 20 | 24 | fits | 148,198 | 142 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 309,830 | 3.098 | 20 | 24 | fits | 149,919 | 176 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 309,764 | 3.098 | 20 | 50 | fits | 149,919 | 176 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 465,460 | 4.655 | 20 | 50 | fits | 156,092 | 209 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 549,193 | 5.492 | 20 | 20 | fits | 83,799 | 31 | 0.750 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 932,933 | 9.329 | 20 | 20 | fits | 33,366 | 12 | 0.828 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 387,255 | 3.873 | 20 | 20 | fits | 156,507 | 193 | 0.417 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 303,085 | 3.031 | 20 | 200 | fits | 150,356 | 196 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 458,976 | 4.590 | 20 | 200 | fits | 156,507 | 193 | 0.417 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 304,009 | 3.040 | 20 | 20 | fits | 150,356 | 196 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 543,515 | 5.435 | 20 | 20 | fits | 83,835 | 31 | 0.751 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 157,293 | 1.573 | 20 | 24 | fits | 148,198 | 142 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 306,659 | 3.067 | 20 | 24 | fits | 150,356 | 196 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 306,593 | 3.066 | 20 | 50 | fits | 150,356 | 196 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 462,704 | 4.627 | 20 | 50 | fits | 156,507 | 193 | 0.417 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 546,473 | 5.465 | 20 | 20 | fits | 83,835 | 31 | 0.751 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 930,095 | 9.301 | 20 | 20 | fits | 33,244 | 12 | 0.826 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 383,838 | 3.838 | 20 | 20 | fits | 157,561 | 193 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 299,518 | 2.995 | 20 | 200 | fits | 150,397 | 196 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 456,463 | 4.565 | 20 | 200 | fits | 157,561 | 193 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 300,442 | 3.004 | 20 | 20 | fits | 150,397 | 196 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 552,866 | 5.529 | 20 | 20 | fits | 84,462 | 42 | 0.771 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 153,685 | 1.537 | 20 | 24 | fits | 148,198 | 142 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 303,092 | 3.031 | 20 | 24 | fits | 150,397 | 196 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 303,026 | 3.030 | 20 | 50 | fits | 150,397 | 196 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 460,191 | 4.602 | 20 | 50 | fits | 157,561 | 193 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 555,824 | 5.558 | 20 | 20 | fits | 84,462 | 42 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 927,894 | 9.279 | 20 | 20 | fits | 33,414 | 12 | 0.828 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 381,545 | 3.815 | 20 | 20 | fits | 156,502 | 206 | 0.431 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 296,945 | 2.969 | 20 | 200 | fits | 151,432 | 180 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 452,831 | 4.528 | 20 | 200 | fits | 156,502 | 206 | 0.431 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 297,869 | 2.979 | 20 | 20 | fits | 151,432 | 180 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 549,282 | 5.493 | 20 | 20 | fits | 84,504 | 42 | 0.771 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 150,077 | 1.501 | 20 | 24 | fits | 148,198 | 142 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 300,519 | 3.005 | 20 | 24 | fits | 151,432 | 180 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 300,453 | 3.005 | 20 | 50 | fits | 151,432 | 180 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 456,559 | 4.566 | 20 | 50 | fits | 156,502 | 206 | 0.431 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 552,240 | 5.522 | 20 | 20 | fits | 84,504 | 42 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 924,310 | 9.243 | 20 | 20 | fits | 33,414 | 12 | 0.828 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 417,236 | 4.172 | 20 | 20 | fits | 156,518 | 206 | 0.459 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 294,541 | 2.945 | 20 | 200 | fits | 152,783 | 186 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 461,283 | 4.613 | 20 | 200 | fits | 156,518 | 206 | 0.459 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 295,465 | 2.955 | 20 | 20 | fits | 152,783 | 186 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 547,028 | 5.470 | 20 | 20 | fits | 85,041 | 37 | 0.732 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 146,322 | 1.463 | 20 | 24 | fits | 148,198 | 142 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 298,115 | 2.981 | 20 | 24 | fits | 152,783 | 186 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 298,049 | 2.980 | 20 | 50 | fits | 152,783 | 186 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 465,011 | 4.650 | 20 | 50 | fits | 156,518 | 206 | 0.459 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 549,986 | 5.500 | 20 | 20 | fits | 85,041 | 37 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 921,726 | 9.217 | 20 | 20 | fits | 33,325 | 12 | 0.827 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 424,227 | 4.242 | 20 | 20 | fits | 151,103 | 192 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 326,222 | 3.262 | 20 | 200 | fits | 157,328 | 197 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 476,709 | 4.767 | 20 | 200 | fits | 151,103 | 192 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 327,146 | 3.271 | 20 | 20 | fits | 157,328 | 197 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 562,362 | 5.624 | 20 | 20 | fits | 84,949 | 37 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 163,292 | 1.633 | 20 | 24 | fits | 148,354 | 143 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 329,796 | 3.298 | 20 | 24 | fits | 157,328 | 197 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 329,730 | 3.297 | 20 | 50 | fits | 157,328 | 197 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 480,437 | 4.804 | 20 | 50 | fits | 151,103 | 192 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 565,320 | 5.653 | 20 | 20 | fits | 84,949 | 37 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 937,035 | 9.370 | 20 | 20 | fits | 33,325 | 12 | 0.827 |
| LINK_UP | `adp.link_up.if0` | 3,384 | 0.034 | 20 | 200 | fits | 33,443 | 43 (11) | 0.745 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,842 | 0.158 | 20 | 200 | fits | 27,934 | 23 (39) | 0.757 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 4,231 | 0.042 | 20 | 200 | fits | 3,390 | 10 (11) | 0.571 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 28,660 | 0.287 | 20 | 20 | fits | 38,306 | 27 (35) | 0.801 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 32,008 | 0.320 | 20 | 20 | fits | 34,445 | 23 (14) | 0.837 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 28,360 | 0.284 | 20 | 20 | fits | 35,189 | 25 (14) | 0.824 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 16,725 | 0.167 | 20 | 20 | fits | 37,076 | 21 (35) | 0.822 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 80,726 | 0.807 | 20 | 20 | fits | 27,772 | 8 | 0.826 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 45,081 | 0.451 | 20 | 20 | fits | 45,147 | 12 | 0.891 |
| malformed MRPDU discard | `srp.malformed.if0` | 24,032 | 0.240 | 20 | 20 | fits | 24,098 | 12 | 0.722 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 80,290 | 0.803 | 220 | 220 | fits | 42,765 | 6 | 0.913 |
| an event behind 15 others | `backlog.event.if0` | 165,338 | 1.653 | 20 | 200 | fits | 62,170 | 79 | 0.571 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 478,554 | 4.786 | 20 | 20 | fits | 79,495 | 87 | 0.381 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 434,530 | 4.345 | 20 | 200 | fits | 157,107 | 129 | 0.435 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 513,409 | 5.134 | 20 | 200 | fits | 79,495 | 87 | 0.381 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 430,208 | 4.302 | 20 | 20 | fits | 157,107 | 129 | 0.435 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 508,867 | 5.089 | 20 | 20 | fits | 79,495 | 87 | 0.381 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 150,419 | 1.504 | 20 | 24 | fits | 151,310 | 148 | 0.387 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 432,858 | 4.329 | 20 | 24 | fits | 157,107 | 129 | 0.435 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 432,792 | 4.328 | 20 | 50 | fits | 157,107 | 129 | 0.435 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 432,396 | 4.324 | 20 | 50 | fits | 157,107 | 129 | 0.435 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 511,825 | 5.118 | 20 | 20 | fits | 79,495 | 87 | 0.381 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 576,358 | 5.764 | 20 | 20 | fits | 30,614 | 57 | 0.129 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 401,571 | 4.016 | 20 | 20 | fits | 158,806 | 196 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 295,079 | 2.951 | 20 | 200 | fits | 150,525 | 198 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 463,879 | 4.639 | 20 | 200 | fits | 158,806 | 196 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 296,003 | 2.960 | 20 | 20 | fits | 150,525 | 198 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 546,443 | 5.464 | 20 | 20 | fits | 81,860 | 35 | 0.779 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 149,118 | 1.491 | 20 | 24 | fits | 149,304 | 145 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 298,653 | 2.987 | 20 | 24 | fits | 150,525 | 198 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 298,587 | 2.986 | 20 | 50 | fits | 150,525 | 198 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 467,607 | 4.676 | 20 | 50 | fits | 158,806 | 196 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 549,401 | 5.494 | 20 | 20 | fits | 81,860 | 35 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 921,150 | 9.211 | 20 | 20 | fits | 33,320 | 12 | 0.827 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 24,181 | 0.242 | 20 | 20 | fits | 34,788 | 19 | 0.816 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 295,079 | 2.951 | 20 | 200 | fits | 150,525 | 198 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 47,361 | 0.474 | 20 | 200 | fits | 34,788 | 19 | 0.816 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 296,003 | 2.960 | 20 | 20 | fits | 150,525 | 198 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 460,842 | 4.608 | 20 | 20 | fits | 155,065 | 195 | 0.389 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 149,118 | 1.491 | 20 | 24 | fits | 149,304 | 145 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 298,653 | 2.987 | 20 | 24 | fits | 150,525 | 198 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 298,587 | 2.986 | 20 | 50 | fits | 150,525 | 198 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 463,866 | 4.639 | 20 | 50 | fits | 155,065 | 195 | 0.389 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 550,986 | 5.510 | 20 | 20 | fits | 87,186 | 34 | 0.754 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 880,777 | 8.808 | 20 | 20 | fits | 76,527 | 32 | 0.569 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,352,858 | 63.529 | 20 | 20 | MISS ceiling | 24,287 | 13 | 0.635 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,377,072 | 63.771 | 20 | 20 | MISS ceiling | 24,271 | 13 | 0.610 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,401,198 | 64.012 | 20 | 20 | MISS ceiling | 24,202 | 13 | 0.618 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,425,316 | 64.253 | 20 | 20 | MISS ceiling | 24,194 | 13 | 0.627 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,449,435 | 64.494 | 20 | 20 | MISS ceiling | 24,182 | 13 | 0.627 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 168,537 | 1.685 | 20 | 200 | fits | 154,098 | 177 | 0.458 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 300,323 | 3.003 | 20 | 200 | fits | 132,402 | 207 | 0.385 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 164,215 | 1.642 | 20 | 20 | fits | 154,098 | 177 | 0.458 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,237,885 | 62.379 | 20 | 20 | MISS ceiling | 39,586 | 15 | 0.777 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 167,855 | 1.679 | 20 | 24 | fits | 154,098 | 177 | 0.458 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,201,785 | 62.018 | 20 | 24 | MISS ceiling | 154,057 | 106 | 0.420 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 166,799 | 1.668 | 20 | 50 | fits | 154,098 | 177 | 0.458 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 298,805 | 2.988 | 20 | 50 | fits | 132,402 | 207 | 0.385 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 381,139 | 3.811 | 20 | 20 | fits | 82,400 | 28 | 0.735 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 715,089 | 7.151 | 20 | 20 | fits | 84,377 | 36 | 0.508 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 7,589 | 0.076 | 20 | 20 | fits | 30,670 | 14 (29) | 0.797 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 10,029 | 0.100 | 20 | 20 | fits | 33,836 | 19 (35) | 0.807 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 11,478 | 0.115 | 20 | 20 | fits | 35,878 | 21 (12) | 0.818 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 13,931 | 0.139 | 20 | 50 | fits | 33,443 | 43 | 0.745 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 21,910 | 0.219 | 20 | 50 | fits | 29,712 | 35 | 0.725 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 23,363 | 0.234 | 20 | 50 | fits | 29,770 | 35 | 0.727 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 17,599 | 0.176 | 20 | 50 | fits | 38,099 | 67 | 0.647 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 19,549 | 0.195 | 20 | 50 | fits | 38,099 | 67 | 0.647 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 12,640 | 0.126 | 20 | 50 | fits | 27,994 | 30 | 0.653 |
| LINK_UP | `adp.link_up.if0` | 3,384 | 0.034 | 20 | 200 | fits | 33,443 | 43 (11) | 0.745 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,842 | 0.158 | 20 | 200 | fits | 27,934 | 23 (39) | 0.757 |
| LINK_DOWN | `adp.link_down.if0` | 2,724 | 0.027 | 20 | 200 | fits | 32,208 | 23 (9) | 0.795 |
| LINK_UP | `adp.link_up.if0` | 3,384 | 0.034 | 20 | 200 | fits | 33,443 | 43 (11) | 0.745 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,842 | 0.158 | 20 | 200 | fits | 27,934 | 23 (39) | 0.757 |
| GM_CHANGE | `adp.gm_change.if0` | 3,137 | 0.031 | 20 | 200 | fits | 21,031 | 17 (11) | 0.747 |
| LINK_UP | `adp.link_up.if0` | 3,384 | 0.034 | 20 | 200 | fits | 33,443 | 43 (11) | 0.745 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,842 | 0.158 | 20 | 200 | fits | 27,934 | 23 (39) | 0.757 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 6,686 | 0.067 | 20 | 200 | fits | 21,313 | 16 (31) | 0.663 |
| LINK_UP | `adp.link_up.if0` | 3,384 | 0.034 | 20 | 200 | fits | 33,443 | 43 (11) | 0.745 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,842 | 0.158 | 20 | 200 | fits | 27,934 | 23 (39) | 0.757 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 6,686 | 0.067 | 20 | 200 | fits | 21,313 | 16 (31) | 0.663 |
| set_name | `aecp_fanout.set_name.if0` | 47,256 | 0.473 | 20 | 24 | fits | 60,563 | 87 | 0.577 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 61,343 | 0.613 | 20 | 24 | fits | 56,716 | 78 | 0.599 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 59,766 | 0.598 | 20 | 24 | fits | 52,524 | 78 | 0.565 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 50,520 | 0.505 | 20 | 24 | fits | 52,557 | 77 | 0.568 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 61,078 | 0.611 | 20 | 24 | fits | 56,193 | 67 | 0.592 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 41,935 | 0.419 | 20 | 24 | fits | 51,833 | 77 | 0.559 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 42,696 | 0.427 | 20 | 24 | fits | 51,648 | 78 | 0.559 |
| BIND_RX | `acmp.bind_rx.if0` | 20,926 | 0.209 | 20 | 20 | fits | 47,784 | 26 (77) | 0.803 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 11,096 | 0.111 | 20 | 20 | fits | 36,731 | 19 (32) | 0.837 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 11,437 | 0.114 | 20 | 20 | fits | 31,293 | 16 (47) | 0.776 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 16,155 | 0.162 | 20 | 20 | fits | 44,656 | 18 (50) | 0.843 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 11,441 | 0.114 | 20 | 20 | fits | 31,211 | 17 (48) | 0.759 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 10,450 | 0.104 | 20 | 20 | fits | 30,592 | 16 (48) | 0.755 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 15,265 | 0.153 | 20 | 20 | fits | 36,835 | 24 (48) | 0.742 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 10,513 | 0.105 | 20 | 20 | fits | 30,066 | 16 (48) | 0.752 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 11,226 | 0.112 | 20 | 24 | fits | 31,441 | 20 | 0.784 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 21,271 | 0.213 | 20 | 24 | fits | 35,248 | 20 | 0.711 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 12,365 | 0.124 | 20 | 24 | fits | 31,499 | 20 | 0.736 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 16,314 | 0.163 | 20 | 24 | fits | 31,473 | 20 | 0.728 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 14,495 | 0.145 | 20 | 24 | fits | 31,100 | 20 | 0.725 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 12,715 | 0.127 | 20 | 24 | fits | 32,383 | 20 | 0.735 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 15,622 | 0.156 | 20 | 24 | fits | 31,123 | 20 | 0.731 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 11,511 | 0.115 | 20 | 24 | fits | 30,738 | 20 | 0.743 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 16,023 | 0.160 | 20 | 24 | fits | 31,263 | 20 | 0.751 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 16,603 | 0.166 | 20 | 24 | fits | 35,960 | 21 | 0.660 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 11,664 | 0.117 | 20 | 24 | fits | 30,895 | 20 | 0.772 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 15,353 | 0.154 | 20 | 24 | fits | 30,644 | 20 | 0.769 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 11,487 | 0.115 | 20 | 24 | fits | 30,871 | 20 | 0.734 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 16,213 | 0.162 | 20 | 24 | fits | 31,662 | 20 | 0.739 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 11,891 | 0.119 | 20 | 24 | fits | 31,228 | 20 | 0.737 |
| get_configuration | `aecp.get_configuration.if0` | 9,599 | 0.096 | 20 | 24 | fits | 28,196 | 20 | 0.738 |
| entity_available | `aecp.entity_available.if0` | 13,396 | 0.134 | 20 | 24 | fits | 28,158 | 20 | 0.733 |
| get_name | `aecp.get_name.if0` | 11,781 | 0.118 | 20 | 24 | fits | 30,962 | 20 | 0.749 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 17,286 | 0.173 | 20 | 24 | fits | 32,798 | 26 | 0.730 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 13,180 | 0.132 | 20 | 24 | fits | 32,622 | 28 | 0.759 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 19,842 | 0.198 | 20 | 24 | fits | 28,814 | 20 | 0.755 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 14,871 | 0.149 | 20 | 24 | fits | 28,133 | 20 | 0.729 |
| set_name | `aecp.set_name.if0` | 20,165 | 0.202 | 20 | 24 | fits | 48,161 | 41 | 0.765 |
| lock_entity | `aecp.lock_entity.if0` | 22,199 | 0.222 | 20 | 24 | fits | 40,897 | 34 | 0.785 |
| unlock_entity | `aecp.unlock_entity.if0` | 17,192 | 0.172 | 20 | 24 | fits | 40,119 | 32 | 0.783 |
| LINK_UP | `fixture.link_up.if0` | 3,384 | 0.034 | 20 | 200 | fits | 33,443 | 43 (11) | 0.745 |
| malformed MRPDU discard | `fixture.malformed.if0` | 24,117 | 0.241 | 20 | 20 | fits | 24,183 | 12 | 0.740 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 35,056 | 0.351 | 20 | 24 | fits | 50,538 | 41 | 0.784 |
| LINK_DOWN | `fixture.link_down.if0` | 3,123 | 0.031 | 20 | 200 | fits | 33,213 | 23 (9) | 0.798 |
| BIND_RX | `fixture.bind_rx.if0` | 20,757 | 0.208 | 20 | 20 | fits | 48,056 | 26 (77) | 0.812 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 25,606 | 0.256 | 20 | 20 | fits | 44,808 | 29 (35) | 0.786 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 20,201 | 0.202 | 20 | 20 | fits | 31,813 | 13 (29) | 0.821 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 85,402 | 0.854 | 20 | 200 | fits | 85,506 | 51 | 0.756 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 85,402 | 0.854 | 20 | 200 | fits | 85,506 | 51 | 0.756 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 85,128 | 0.851 | 20 | 20 | fits | 85,506 | 51 | 0.756 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 85,128 | 0.851 | 20 | 20 | fits | 85,506 | 51 | 0.756 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 85,336 | 0.853 | 20 | 24 | fits | 85,506 | 51 | 0.756 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 85,336 | 0.853 | 20 | 24 | fits | 85,506 | 51 | 0.756 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 85,270 | 0.853 | 20 | 50 | fits | 85,506 | 51 | 0.756 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 85,270 | 0.853 | 20 | 50 | fits | 85,506 | 51 | 0.756 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 85,204 | 0.852 | 20 | 20 | fits | 85,506 | 51 | 0.756 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 85,204 | 0.852 | 20 | 20 | fits | 85,506 | 51 | 0.756 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
