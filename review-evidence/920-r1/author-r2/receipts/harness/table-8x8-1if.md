### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 85 paths and 7 of 963 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.221 (0.484) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.172 (0.394) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.113 (0.353) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.080 (0.312) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.120 (0.321) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.112 (0.302) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.107 (0.309) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.123 (0.322) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.119 (0.373) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.313 (0.782) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.239 (0.703) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.337 (0.759) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.310 (0.619) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.139 (0.660) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.328 (0.628) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.172 (0.454) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.053 (0.215) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.026 (0.220) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.027 (0.332) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.031 (0.350) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.216 (0.431) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.186 (0.611) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.106 (0.519) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.217 (0.628) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.267 (0.673) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.299 (0.715) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.288 (0.694) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.328 (0.844) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.098 (0.511) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.155 (0.362) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.292 (0.702) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.287 (0.696) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.129 (0.548) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.172 (0.591) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.286 (0.696) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.123 (0.542) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.123 (0.542) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.285 (0.696) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.132 (0.551) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.127 (0.546) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.126 (0.546) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.299 (0.708) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.128 (0.548) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.257 (0.670) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.199 (0.556) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.267 (0.673) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.170 (0.630) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.518 (0.866) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.579 (0.950) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.520 (0.867) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.595 (0.991) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.512 (0.885) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.555 (0.898) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.786 (5.120) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 5.016 (5.664) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.280 (0.747) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.717 (2.191) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.597 (63.993) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.658 (65.036) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.366 (0.524) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-burst.held.acmp.if0` (save-burst) | 3.064 | fits | 11 acmp | 4 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-flight.held.adp.if0` (save-flight) | 3.215 | fits | 7 adp | 4 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 3.202 | fits | 15 aecp | 4 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 2.799 | fits | 6 maap | 4 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 9.053 | fits | 31 srp | 4 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.294 (0.717) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.119 (0.297) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.139 (0.350) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.275 (0.717) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.257 (0.672) | fits | 0 events | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-flight.mrpdu.periodic.if0` (save-flight) | 2.856 | fits | 0 srp | 12 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.290 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.399 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.333 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-7.service.adp.last.if0` (backlog-adp@verify-aged2-7) | 5.637 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-4.service.aecp.first.if0` (backlog-adp@blank-4) | 3.053 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.035 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.316 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-7.service.maap.last.if0` (backlog-adp@verify-aged2-7) | 5.674 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-7.service.srp.first.if0` (backlog-adp@verify-aged2-7) | 6.527 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-5.service.srp.last.if0` (backlog-adp@program-aged2-5) | 10.494 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.815 (0.866) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.460 (0.460) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.253 (0.254) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.832 (0.908) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 1 | 14.640 | 10 | 159,363 (1.594) | yes | - |
| backlog-adp@blank-1 | 1 | 14.640 | 10 | 159,363 (1.594) | yes | - |
| backlog-adp@blank-2 | 1 | 14.640 | 10 | 159,363 (1.594) | yes | - |
| backlog-adp@blank-3 | 0 | 14.726 | 11 | 157,648 (1.576) | yes | - |
| backlog-adp@blank-4 | 0 | 14.629 | 10 | 157,069 (1.571) | yes | - |
| backlog-adp@blank-5 | 0 | 14.466 | 11 | 158,253 (1.583) | yes | - |
| backlog-adp@blank-6 | 0 | 14.341 | 11 | 158,253 (1.583) | yes | - |
| backlog-adp@blank-7 | 0 | 14.216 | 11 | 158,253 (1.583) | yes | - |
| backlog-adp@program-0 | 0 | 13.105 | 12 | 157,627 (1.576) | yes | - |
| backlog-adp@program-1 | 0 | 12.855 | 12 | 157,627 (1.576) | yes | - |
| backlog-adp@program-2 | 0 | 12.605 | 11 | 157,627 (1.576) | yes | - |
| backlog-adp@program-3 | 0 | 12.560 | 12 | 157,643 (1.576) | yes | - |
| backlog-adp@program-4 | 0 | 12.099 | 12 | 158,498 (1.585) | yes | - |
| backlog-adp@program-5 | 1 | 11.286 | 11 | 152,893 (1.529) | yes | - |
| backlog-adp@program-6 | 1 | 11.286 | 11 | 152,893 (1.529) | yes | - |
| backlog-adp@program-7 | 1 | 11.286 | 11 | 152,893 (1.529) | yes | - |
| backlog-adp@verify-0 | 0 | 13.914 | 12 | 157,290 (1.573) | yes | - |
| backlog-adp@verify-1 | 0 | 13.789 | 12 | 157,290 (1.573) | yes | - |
| backlog-adp@verify-2 | 0 | 14.823 | 13 | 157,388 (1.574) | yes | - |
| backlog-adp@verify-3 | 0 | 14.698 | 13 | 157,388 (1.574) | yes | - |
| backlog-adp@verify-4 | 0 | 14.573 | 13 | 157,388 (1.574) | yes | - |
| backlog-adp@verify-5 | 1 | 12.710 | 11 | 155,499 (1.555) | yes | - |
| backlog-adp@verify-6 | 1 | 12.710 | 11 | 155,499 (1.555) | yes | - |
| backlog-adp@verify-7 | 1 | 12.710 | 11 | 155,499 (1.555) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 12.533 | 11 | 156,804 (1.568) | yes | - |
| backlog-adp@blank-aged2-1 | 1 | 12.147 | 9 | 152,024 (1.520) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 14.479 | 12 | 156,968 (1.570) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 14.500 | 12 | 156,968 (1.570) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 13.356 | 11 | 157,111 (1.571) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 13.239 | 10 | 156,766 (1.568) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 17.721 | 13 | 156,771 (1.568) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 14.313 | 10 | 157,734 (1.577) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 12.603 | 11 | 156,812 (1.568) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 12.473 | 10 | 156,914 (1.569) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 12.510 | 10 | 156,914 (1.569) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 12.300 | 9 | 151,542 (1.515) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 13.653 | 12 | 157,577 (1.576) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 12.718 | 12 | 156,956 (1.570) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 12.585 | 11 | 157,236 (1.572) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 14.615 | 11 | 156,968 (1.570) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.869 | 11 | 157,330 (1.573) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 11.528 | 9 | 151,680 (1.517) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 11.814 | 10 | 156,859 (1.569) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 11.830 | 10 | 156,859 (1.569) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 12.253 | 12 | 156,859 (1.569) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 12.047 | 11 | 157,090 (1.571) | yes | - |
| backlog-adp@program-aged2-6 | 1 | 11.787 | 9 | 159,526 (1.595) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 13.182 | 11 | 156,969 (1.570) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 12.103 | 12 | 157,272 (1.573) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 12.175 | 12 | 157,182 (1.572) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 11.832 | 10 | 156,863 (1.569) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 11.671 | 9 | 150,899 (1.509) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 11.671 | 10 | 156,969 (1.570) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 11.773 | 10 | 156,969 (1.570) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 13.637 | 12 | 156,969 (1.570) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 12.409 | 12 | 157,155 (1.572) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 13.528 | 12 | 157,108 (1.571) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 13.600 | 12 | 157,018 (1.570) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 13.280 | 10 | 156,969 (1.570) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 13.096 | 9 | 152,029 (1.520) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 13.140 | 10 | 156,805 (1.568) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 13.187 | 10 | 157,508 (1.575) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 15.771 | 13 | 156,939 (1.569) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 14.646 | 12 | 156,991 (1.570) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 12.546 | 11 | 156,969 (1.570) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 14.730 | 12 | 158,523 (1.585) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 12.613 | 11 | 157,182 (1.572) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 12.470 | 10 | 156,749 (1.567) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 12.515 | 10 | 156,859 (1.569) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 12.393 | 9 | 157,228 (1.572) | yes | - |
| backlog-adp@verify-aged1-6 | 1 | 12.360 | 9 | 150,883 (1.509) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 14.671 | 12 | 157,023 (1.570) | yes | - |
| backlog | 0 | 6.710 | 8 | 161,259 (1.613) | yes | - |
| backlog-adp | 0 | 10.232 | 11 | 151,232 (1.512) | yes | - |
| backlog-adp-refill | 0 | 41.524 | 26 | 151,232 (1.512) | yes | - |
| backlog-owed | 0 | 65.505 | 24 | 156,693 (1.567) | yes | - |
| fixture | 0 | 1.518 | 2 | 86,723 (0.867) | yes | - |

Composed maximum over the 4 backlog windows: 161,259 CPU cycles (1.613 ms), backlog.
Over the windows that released their whole load only: 161,259 (1.613 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 112264 | 0 | 57,098 (0.571) | fits |
| save-burst | 3316 | 0 | 162,225 (1.622) | fits |
| save-held | 3475 | 0 | 158,637 (1.586) | fits |
| save-starved | 52931 | 0 | 158,637 (1.586) | fits |
| save-flight | 3006 | 0 | 158,637 (1.586) | fits |
| acmp-notk | 3388 | 0 | 115,570 (1.156) | fits |
| backlog-adp@blank-0 | 474 | 0 | 159,363 (1.594) | fits |
| backlog-adp@blank-1 | 474 | 0 | 159,363 (1.594) | fits |
| backlog-adp@blank-2 | 474 | 0 | 159,363 (1.594) | fits |
| backlog-adp@blank-3 | 475 | 0 | 157,648 (1.576) | fits |
| backlog-adp@blank-4 | 475 | 0 | 157,069 (1.571) | fits |
| backlog-adp@blank-5 | 475 | 0 | 158,253 (1.583) | fits |
| backlog-adp@blank-6 | 475 | 0 | 158,253 (1.583) | fits |
| backlog-adp@blank-7 | 475 | 0 | 158,253 (1.583) | fits |
| backlog-adp@program-0 | 511 | 0 | 157,627 (1.576) | fits |
| backlog-adp@program-1 | 511 | 0 | 157,627 (1.576) | fits |
| backlog-adp@program-2 | 511 | 0 | 157,627 (1.576) | fits |
| backlog-adp@program-3 | 512 | 0 | 157,643 (1.576) | fits |
| backlog-adp@program-4 | 511 | 0 | 158,498 (1.585) | fits |
| backlog-adp@program-5 | 511 | 0 | 152,893 (1.529) | fits |
| backlog-adp@program-6 | 511 | 0 | 152,893 (1.529) | fits |
| backlog-adp@program-7 | 511 | 0 | 152,893 (1.529) | fits |
| backlog-adp@verify-0 | 534 | 0 | 157,290 (1.573) | fits |
| backlog-adp@verify-1 | 534 | 0 | 157,290 (1.573) | fits |
| backlog-adp@verify-2 | 535 | 0 | 157,388 (1.574) | fits |
| backlog-adp@verify-3 | 535 | 0 | 157,388 (1.574) | fits |
| backlog-adp@verify-4 | 535 | 0 | 157,388 (1.574) | fits |
| backlog-adp@verify-5 | 534 | 0 | 155,499 (1.555) | fits |
| backlog-adp@verify-6 | 534 | 0 | 155,499 (1.555) | fits |
| backlog-adp@verify-7 | 534 | 0 | 155,499 (1.555) | fits |
| backlog-adp@blank-aged2-0 | 677 | 0 | 156,804 (1.568) | fits |
| backlog-adp@blank-aged2-1 | 681 | 0 | 156,968 (1.570) | fits |
| backlog-adp@blank-aged2-2 | 689 | 0 | 156,968 (1.570) | fits |
| backlog-adp@blank-aged2-3 | 695 | 0 | 156,968 (1.570) | fits |
| backlog-adp@blank-aged2-4 | 700 | 0 | 157,111 (1.571) | fits |
| backlog-adp@blank-aged2-5 | 705 | 0 | 156,766 (1.568) | fits |
| backlog-adp@blank-aged2-6 | 714 | 0 | 156,771 (1.568) | fits |
| backlog-adp@blank-aged2-7 | 717 | 0 | 157,734 (1.577) | fits |
| backlog-adp@blank-aged1-0 | 630 | 0 | 156,812 (1.568) | fits |
| backlog-adp@blank-aged1-1 | 635 | 0 | 156,914 (1.569) | fits |
| backlog-adp@blank-aged1-2 | 641 | 0 | 156,914 (1.569) | fits |
| backlog-adp@blank-aged1-3 | 646 | 0 | 156,750 (1.567) | fits |
| backlog-adp@blank-aged1-4 | 654 | 0 | 157,577 (1.576) | fits |
| backlog-adp@blank-aged1-5 | 660 | 0 | 156,956 (1.570) | fits |
| backlog-adp@blank-aged1-6 | 665 | 0 | 157,236 (1.572) | fits |
| backlog-adp@blank-aged1-7 | 671 | 0 | 156,968 (1.570) | fits |
| backlog-adp@program-aged2-0 | 714 | 0 | 157,330 (1.573) | fits |
| backlog-adp@program-aged2-1 | 718 | 0 | 156,859 (1.569) | fits |
| backlog-adp@program-aged2-2 | 724 | 0 | 156,859 (1.569) | fits |
| backlog-adp@program-aged2-3 | 730 | 0 | 156,859 (1.569) | fits |
| backlog-adp@program-aged2-4 | 738 | 0 | 156,859 (1.569) | fits |
| backlog-adp@program-aged2-5 | 743 | 0 | 157,090 (1.571) | fits |
| backlog-adp@program-aged2-6 | 748 | 0 | 159,526 (1.595) | fits |
| backlog-adp@program-aged2-7 | 755 | 0 | 156,969 (1.570) | fits |
| backlog-adp@program-aged1-0 | 668 | 0 | 157,272 (1.573) | fits |
| backlog-adp@program-aged1-1 | 674 | 0 | 157,182 (1.572) | fits |
| backlog-adp@program-aged1-2 | 678 | 0 | 156,863 (1.569) | fits |
| backlog-adp@program-aged1-3 | 683 | 0 | 150,899 (1.509) | fits |
| backlog-adp@program-aged1-4 | 689 | 0 | 156,969 (1.570) | fits |
| backlog-adp@program-aged1-5 | 695 | 0 | 156,969 (1.570) | fits |
| backlog-adp@program-aged1-6 | 703 | 0 | 156,969 (1.570) | fits |
| backlog-adp@program-aged1-7 | 709 | 0 | 157,155 (1.572) | fits |
| backlog-adp@verify-aged2-0 | 726 | 0 | 157,108 (1.571) | fits |
| backlog-adp@verify-aged2-1 | 732 | 0 | 157,018 (1.570) | fits |
| backlog-adp@verify-aged2-2 | 736 | 0 | 156,969 (1.570) | fits |
| backlog-adp@verify-aged2-3 | 741 | 0 | 156,805 (1.568) | fits |
| backlog-adp@verify-aged2-4 | 747 | 0 | 156,805 (1.568) | fits |
| backlog-adp@verify-aged2-5 | 753 | 0 | 157,508 (1.575) | fits |
| backlog-adp@verify-aged2-6 | 762 | 0 | 156,939 (1.569) | fits |
| backlog-adp@verify-aged2-7 | 767 | 0 | 156,991 (1.570) | fits |
| backlog-adp@verify-aged1-0 | 678 | 0 | 156,969 (1.570) | fits |
| backlog-adp@verify-aged1-1 | 685 | 0 | 158,523 (1.585) | fits |
| backlog-adp@verify-aged1-2 | 690 | 0 | 157,182 (1.572) | fits |
| backlog-adp@verify-aged1-3 | 695 | 0 | 156,749 (1.567) | fits |
| backlog-adp@verify-aged1-4 | 701 | 0 | 156,859 (1.569) | fits |
| backlog-adp@verify-aged1-5 | 706 | 0 | 157,228 (1.572) | fits |
| backlog-adp@verify-aged1-6 | 712 | 0 | 157,023 (1.570) | fits |
| backlog-adp@verify-aged1-7 | 720 | 0 | 157,023 (1.570) | fits |
| adp-advertise | 597 | 0 | 39,358 (0.394) | fits |
| acmp-noresp | 2021 | 0 | 115,380 (1.154) | fits |
| save | 609 | 0 | 85,021 (0.850) | fits |
| srp | 289 | 0 | 46,034 (0.460) | fits |
| backlog | 286 | 0 | 161,259 (1.613) | fits |
| backlog-adp | 314 | 0 | 151,232 (1.512) | fits |
| backlog-adp-refill | 329 | 0 | 151,232 (1.512) | fits |
| backlog-owed | 308 | 0 | 156,693 (1.567) | fits |
| acmp-disc | 937 | 0 | 115,406 (1.154) | fits |
| maap | 178 | 0 | 39,358 (0.394) | fits |
| adp-link | 89 | 0 | 45,376 (0.454) | fits |
| adp-gm | 88 | 0 | 35,008 (0.350) | fits |
| adp-discover | 88 | 0 | 35,008 (0.350) | fits |
| control | 88 | 0 | 35,008 (0.350) | fits |
| aecp-fanout | 110 | 0 | 62,972 (0.630) | fits |
| acmp-cmd | 87 | 0 | 48,316 (0.483) | fits |
| aecp | 112 | 0 | 55,615 (0.556) | fits |
| datapath-events | 118 | 0 | 35,008 (0.350) | fits |
| fixture | 150 | 0 | 86,723 (0.867) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | +9.818 ms, 76,672 (0.767 ms), read-back | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 9.528 (20) | 10.472 |
| backlog-adp@blank-aged2-1 | 2 | none | +9.424 ms, 76,700 (0.767 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 9.386 (20) | 10.614 |
| backlog-adp@blank-aged2-2 | 2 | +8.064 ms, 76,774 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 10.212 (20) | 9.788 |
| backlog-adp@blank-aged2-3 | 2 | +6.501 ms, 76,691 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 10.233 (20) | 9.767 |
| backlog-adp@blank-aged2-4 | 2 | +5.634 ms, 76,900 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 10.427 (20) | 9.573 |
| backlog-adp@blank-aged2-5 | 2 | +4.749 ms, 77,003 (0.770 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 10.308 (20) | 9.692 |
| backlog-adp@blank-aged2-6 | 2 | +4.796 ms, 77,003 (0.770 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 10.341 (20) | 9.659 |
| backlog-adp@blank-aged2-7 | 2 | +4.525 ms, 76,947 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 10.173 (20) | 9.827 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 9.423 (20) | 10.577 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 9.544 (20) | 10.456 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 9.577 (20) | 10.423 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 9.364 (20) | 10.636 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 9.384 (20) | 10.616 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 9.422 (20) | 10.578 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 9.652 (20) | 10.348 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 9.514 (20) | 10.486 |
| backlog-adp@program-aged2-0 | 2 | none | +9.786 ms, 80,695 (0.807 ms), issue | `backlog-adp@program-aged2-0.service.srp.last.if0` | 9.496 (20) | 10.504 |
| backlog-adp@program-aged2-1 | 2 | none | +9.442 ms, 80,617 (0.806 ms), issue | `backlog-adp@program-aged2-1.service.srp.last.if0` | 9.405 (20) | 10.595 |
| backlog-adp@program-aged2-2 | 2 | +8.164 ms, 80,566 (0.806 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 10.266 (20) | 9.734 |
| backlog-adp@program-aged2-3 | 2 | +6.594 ms, 80,566 (0.806 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 10.282 (20) | 9.718 |
| backlog-adp@program-aged2-4 | 2 | +5.665 ms, 80,630 (0.806 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 10.328 (20) | 9.672 |
| backlog-adp@program-aged2-5 | 2 | +4.810 ms, 80,259 (0.803 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 10.494 (20) | 9.506 |
| backlog-adp@program-aged2-6 | 2 | +4.534 ms, 80,342 (0.803 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 10.231 (20) | 9.769 |
| backlog-adp@program-aged2-7 | 2 | +3.271 ms, 80,351 (0.804 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 10.388 (20) | 9.612 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 9.389 (20) | 10.611 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 9.508 (20) | 10.492 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 9.535 (20) | 10.465 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 9.372 (20) | 10.628 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 9.374 (20) | 10.626 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 9.473 (20) | 10.527 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 9.488 (20) | 10.512 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 9.504 (20) | 10.496 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 9.400 (20) | 10.600 |
| backlog-adp@verify-aged2-1 | 2 | none | none | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 9.521 (20) | 10.479 |
| backlog-adp@verify-aged2-2 | 2 | +8.093 ms, 77,692 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 10.339 (20) | 9.661 |
| backlog-adp@verify-aged2-3 | 2 | +7.117 ms, 77,609 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 10.155 (20) | 9.845 |
| backlog-adp@verify-aged2-4 | 2 | +5.572 ms, 77,669 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 10.196 (20) | 9.804 |
| backlog-adp@verify-aged2-5 | 2 | none | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 10.239 (20) | 9.761 |
| backlog-adp@verify-aged2-6 | 2 | +4.896 ms, 77,905 (0.779 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 10.283 (20) | 9.717 |
| backlog-adp@verify-aged2-7 | 2 | +3.371 ms, 77,677 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 10.345 (20) | 9.655 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 9.353 (20) | 10.647 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 9.479 (20) | 10.521 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 9.522 (20) | 10.478 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 9.524 (20) | 10.476 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 9.568 (20) | 10.432 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 9.444 (20) | 10.556 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 9.410 (20) | 10.590 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 9.439 (20) | 10.561 |

Least margin over the aged windows: 9.506 ms, `backlog-adp@program-aged2-5.service.srp.last.if0` at 10.494 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 22829.581 | 22,870 | 382 | 2 | 31.383 | yes | within |
| save-held | 1356.148 | 12,470 | 382 | - | 33.735 | no | within |
| save-starved | 12448.066 | 12,470 | 382 | - | 33.736 | yes | within |
| save | 1308.802 | 12,470 | 382 | - | 104.302 | no | within |

Names from their response to durable (save_burst.py; #920, the ruling of #665 issuecomment-6899740728, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-burst | 107 | 1370.301 (0) | 5,000 | 6 | - | - | sequence 6, 0 missing | within |
| save-flight | 1 | 663.104 (0) | 5,000 | 2 | - | - | 59 steps (want 59), 26.13 ms | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1080 | 81,632 (0.816) | 77,669 (0.777) |
| save-burst | 3717 | 103,370 (1.034) | 78,345 (0.783) |
| save-held | 1909 | 103,507 (1.035) | 77,795 (0.778) |
| save-starved | 698 | 82,659 (0.827) | 78,003 (0.780) |
| save-flight | 2063 | 102,914 (1.029) | 77,977 (0.780) |
| acmp-notk | 1414 | 115,570 (1.156) | 77,800 (0.778) |
| backlog-adp@blank-0 | 383 | 102,115 (1.021) | 76,010 (0.760) |
| backlog-adp@blank-1 | 383 | 102,115 (1.021) | 76,010 (0.760) |
| backlog-adp@blank-2 | 383 | 102,115 (1.021) | 76,010 (0.760) |
| backlog-adp@blank-3 | 383 | 102,115 (1.021) | 76,010 (0.760) |
| backlog-adp@blank-4 | 383 | 102,115 (1.021) | 76,010 (0.760) |
| backlog-adp@blank-5 | 383 | 102,115 (1.021) | 76,010 (0.760) |
| backlog-adp@blank-6 | 383 | 102,115 (1.021) | 76,010 (0.760) |
| backlog-adp@blank-7 | 383 | 102,115 (1.021) | 76,010 (0.760) |
| backlog-adp@program-0 | 493 | 102,115 (1.021) | 77,639 (0.776) |
| backlog-adp@program-1 | 493 | 102,115 (1.021) | 77,639 (0.776) |
| backlog-adp@program-2 | 493 | 102,115 (1.021) | 77,639 (0.776) |
| backlog-adp@program-3 | 493 | 103,745 (1.037) | 78,470 (0.785) |
| backlog-adp@program-4 | 493 | 102,115 (1.021) | 77,639 (0.776) |
| backlog-adp@program-5 | 493 | 102,115 (1.021) | 77,639 (0.776) |
| backlog-adp@program-6 | 493 | 102,115 (1.021) | 77,639 (0.776) |
| backlog-adp@program-7 | 493 | 102,115 (1.021) | 77,639 (0.776) |
| backlog-adp@verify-0 | 598 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-1 | 598 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-2 | 599 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-3 | 599 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-4 | 599 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-5 | 598 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-6 | 598 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-7 | 598 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@blank-aged2-0 | 379 | 98,820 (0.988) | 75,463 (0.755) |
| backlog-adp@blank-aged2-1 | 379 | 99,764 (0.998) | 75,609 (0.756) |
| backlog-adp@blank-aged2-2 | 381 | 99,642 (0.996) | 75,610 (0.756) |
| backlog-adp@blank-aged2-3 | 381 | 99,642 (0.996) | 75,610 (0.756) |
| backlog-adp@blank-aged2-4 | 380 | 97,010 (0.970) | 75,747 (0.757) |
| backlog-adp@blank-aged2-5 | 380 | 97,083 (0.971) | 75,882 (0.759) |
| backlog-adp@blank-aged2-6 | 384 | 99,436 (0.994) | 75,882 (0.759) |
| backlog-adp@blank-aged2-7 | 381 | 97,083 (0.971) | 75,882 (0.759) |
| backlog-adp@blank-aged1-0 | 379 | 96,776 (0.968) | 76,012 (0.760) |
| backlog-adp@blank-aged1-1 | 379 | 97,446 (0.974) | 76,090 (0.761) |
| backlog-adp@blank-aged1-2 | 379 | 97,327 (0.973) | 76,090 (0.761) |
| backlog-adp@blank-aged1-3 | 379 | 97,666 (0.977) | 76,090 (0.761) |
| backlog-adp@blank-aged1-4 | 380 | 99,617 (0.996) | 76,090 (0.761) |
| backlog-adp@blank-aged1-5 | 379 | 96,412 (0.964) | 76,022 (0.760) |
| backlog-adp@blank-aged1-6 | 379 | 97,291 (0.973) | 76,090 (0.761) |
| backlog-adp@blank-aged1-7 | 381 | 97,291 (0.973) | 76,090 (0.761) |
| backlog-adp@program-aged2-0 | 488 | 102,115 (1.021) | 78,192 (0.782) |
| backlog-adp@program-aged2-1 | 488 | 102,115 (1.021) | 78,270 (0.783) |
| backlog-adp@program-aged2-2 | 489 | 102,115 (1.021) | 78,270 (0.783) |
| backlog-adp@program-aged2-3 | 489 | 102,115 (1.021) | 78,270 (0.783) |
| backlog-adp@program-aged2-4 | 489 | 102,115 (1.021) | 78,199 (0.782) |
| backlog-adp@program-aged2-5 | 489 | 102,115 (1.021) | 77,830 (0.778) |
| backlog-adp@program-aged2-6 | 489 | 102,115 (1.021) | 77,857 (0.779) |
| backlog-adp@program-aged2-7 | 490 | 102,115 (1.021) | 77,928 (0.779) |
| backlog-adp@program-aged1-0 | 488 | 103,797 (1.038) | 78,392 (0.784) |
| backlog-adp@program-aged1-1 | 488 | 102,115 (1.021) | 78,492 (0.785) |
| backlog-adp@program-aged1-2 | 488 | 102,115 (1.021) | 78,605 (0.786) |
| backlog-adp@program-aged1-3 | 488 | 102,115 (1.021) | 78,605 (0.786) |
| backlog-adp@program-aged1-4 | 488 | 102,115 (1.021) | 78,605 (0.786) |
| backlog-adp@program-aged1-5 | 488 | 102,115 (1.021) | 78,605 (0.786) |
| backlog-adp@program-aged1-6 | 491 | 107,048 (1.070) | 78,605 (0.786) |
| backlog-adp@program-aged1-7 | 489 | 108,624 (1.086) | 78,737 (0.787) |
| backlog-adp@verify-aged2-0 | 598 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-aged2-1 | 598 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-aged2-2 | 598 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-aged2-3 | 598 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-aged2-4 | 598 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-aged2-5 | 598 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-aged2-6 | 600 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-aged2-7 | 599 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-aged1-0 | 597 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-aged1-1 | 599 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-aged1-2 | 597 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-aged1-3 | 597 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-aged1-4 | 597 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-aged1-5 | 597 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-aged1-6 | 597 | 102,115 (1.021) | 77,664 (0.777) |
| backlog-adp@verify-aged1-7 | 599 | 104,167 (1.042) | 77,664 (0.777) |
| adp-advertise | 577 | 28,588 (0.286) | 2,348 (0.023) |
| acmp-noresp | 964 | 115,380 (1.154) | 77,664 (0.777) |
| save | 936 | 98,912 (0.989) | 77,729 (0.777) |
| srp | 271 | 28,541 (0.285) | 2,348 (0.023) |
| backlog | 265 | 28,541 (0.285) | 2,348 (0.023) |
| backlog-adp | 271 | 28,541 (0.285) | 2,385 (0.024) |
| backlog-adp-refill | 274 | 28,541 (0.285) | 2,348 (0.023) |
| backlog-owed | 277 | 28,541 (0.285) | 2,348 (0.023) |
| acmp-disc | 655 | 115,406 (1.154) | 77,664 (0.777) |
| maap | 166 | 28,541 (0.285) | 2,348 (0.023) |
| adp-link | 79 | 28,541 (0.285) | 2,348 (0.023) |
| adp-gm | 79 | 28,541 (0.285) | 2,348 (0.023) |
| adp-discover | 79 | 28,541 (0.285) | 2,348 (0.023) |
| control | 79 | 28,541 (0.285) | 2,348 (0.023) |
| aecp-fanout | 79 | 28,541 (0.285) | 2,348 (0.023) |
| acmp-cmd | 66 | 28,541 (0.285) | 2,366 (0.024) |
| aecp | 80 | 28,541 (0.285) | 3,751 (0.038) |
| datapath-events | 70 | 28,541 (0.285) | 2,348 (0.023) |
| fixture | 54 | 26,108 (0.261) | 2,348 (0.023) |

Longest pass that carries a step: 115,570 CPU cycles (1.156 ms), acmp-notk; longest step: 78,737 (0.787 ms), backlog-adp@program-aged1-7.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-burst.held.adp.if0` | 321,140 | 3.211 | 20 | 200 | fits | 131,075 | 110 | 0.567 |
| ACMP record, every channel at its refill rate, the longest | `save-burst.held.acmp.if0` | 306,436 | 3.064 | 20 | 20 | fits | 60,554 | 42 | 0.511 |
| AECP record, every channel at its refill rate, the longest | `save-burst.held.aecp.if0` | 251,883 | 2.519 | 20 | 24 | fits | 131,075 | 110 | 0.567 |
| MAAP record, every channel at its refill rate, the longest | `save-burst.held.maap.if0` | 261,397 | 2.614 | 20 | 50 | fits | 131,075 | 110 | 0.567 |
| SRP record, every channel at its refill rate, the longest | `save-burst.held.srp.if0` | 802,933 | 8.029 | 20 | 20 | fits | 86,560 | 36 | 0.800 |
| an MRPDU its join timer owes, the longest | `save-burst.mrpdu.join.if0` | 188,918 | 1.889 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-burst.mrpdu.leaveall.if0` | 146,068 | 1.461 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-burst.mrpdu.periodic.if0` | 224,495 | 2.245 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 270,606 | 2.706 | 20 | 200 | fits | 112,909 | 130 | 0.454 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 299,446 | 2.994 | 20 | 20 | fits | 85,569 | 55 | 0.571 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 320,159 | 3.202 | 20 | 24 | fits | 85,051 | 60 | 0.480 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 174,402 | 1.744 | 20 | 50 | fits | 147,702 | 217 | 0.384 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 875,379 | 8.754 | 20 | 20 | fits | 52,570 | 20 | 0.729 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 187,181 | 1.872 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 144,273 | 1.443 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 223,609 | 2.236 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 273,611 | 2.736 | 20 | 200 | fits | 115,914 | 136 | 0.479 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 253,474 | 2.535 | 20 | 20 | fits | 115,914 | 136 | 0.479 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 301,777 | 3.018 | 20 | 24 | fits | 82,293 | 60 | 0.479 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 189,272 | 1.893 | 20 | 50 | fits | 87,381 | 112 | 0.465 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 905,315 | 9.053 | 20 | 20 | fits | 56,127 | 26 | 0.748 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 109,831 | 1.098 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 168,653 | 1.687 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 247,595 | 2.476 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 321,512 | 3.215 | 20 | 200 | fits | 93,113 | 90 | 0.322 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 292,139 | 2.921 | 20 | 20 | fits | 70,718 | 51 | 0.478 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 297,969 | 2.980 | 20 | 24 | fits | 67,005 | 44 | 0.462 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 279,914 | 2.799 | 20 | 50 | fits | 123,965 | 202 | 0.303 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 869,495 | 8.695 | 20 | 20 | fits | 43,511 | 16 | 0.778 |
| an MRPDU its join timer owes, the longest | `save-flight.mrpdu.join.if0` | 59,805 | 0.598 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-flight.mrpdu.leaveall.if0` | 55,105 | 0.551 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 285,631 | 2.856 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 13,939 | 0.139 | 20 | 20 | fits | 41,104 | 19 (14) | 0.896 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 389,319 | 3.893 | 20 | 20 | fits | 159,363 | 201 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 293,296 | 2.933 | 20 | 200 | fits | 152,357 | 185 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 452,043 | 4.520 | 20 | 200 | fits | 159,363 | 201 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 294,220 | 2.942 | 20 | 20 | fits | 152,357 | 185 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 538,912 | 5.389 | 20 | 20 | fits | 86,165 | 37 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 145,503 | 1.455 | 20 | 24 | fits | 147,187 | 145 | 0.407 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 296,870 | 2.969 | 20 | 24 | fits | 152,357 | 185 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 296,804 | 2.968 | 20 | 50 | fits | 152,357 | 185 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 455,771 | 4.558 | 20 | 50 | fits | 159,363 | 201 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 541,870 | 5.419 | 20 | 20 | fits | 86,165 | 37 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 953,939 | 9.539 | 20 | 20 | fits | 70,648 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 389,319 | 3.893 | 20 | 20 | fits | 159,363 | 201 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 293,296 | 2.933 | 20 | 200 | fits | 152,357 | 185 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 452,043 | 4.520 | 20 | 200 | fits | 159,363 | 201 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 294,220 | 2.942 | 20 | 20 | fits | 152,357 | 185 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 538,912 | 5.389 | 20 | 20 | fits | 86,165 | 37 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 145,503 | 1.455 | 20 | 24 | fits | 147,187 | 145 | 0.407 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 296,870 | 2.969 | 20 | 24 | fits | 152,357 | 185 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 296,804 | 2.968 | 20 | 50 | fits | 152,357 | 185 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 455,771 | 4.558 | 20 | 50 | fits | 159,363 | 201 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 541,870 | 5.419 | 20 | 20 | fits | 86,165 | 37 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 953,939 | 9.539 | 20 | 20 | fits | 70,648 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 389,319 | 3.893 | 20 | 20 | fits | 159,363 | 201 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 293,296 | 2.933 | 20 | 200 | fits | 152,357 | 185 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 452,043 | 4.520 | 20 | 200 | fits | 159,363 | 201 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 294,220 | 2.942 | 20 | 20 | fits | 152,357 | 185 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 538,912 | 5.389 | 20 | 20 | fits | 86,165 | 37 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 145,503 | 1.455 | 20 | 24 | fits | 147,187 | 145 | 0.407 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 296,870 | 2.969 | 20 | 24 | fits | 152,357 | 185 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 296,804 | 2.968 | 20 | 50 | fits | 152,357 | 185 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 455,771 | 4.558 | 20 | 50 | fits | 159,363 | 201 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 541,870 | 5.419 | 20 | 20 | fits | 86,165 | 37 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 953,939 | 9.539 | 20 | 20 | fits | 70,648 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 416,292 | 4.163 | 20 | 20 | fits | 151,551 | 182 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 319,452 | 3.195 | 20 | 200 | fits | 156,920 | 198 | 0.442 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 470,387 | 4.704 | 20 | 200 | fits | 151,551 | 182 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 320,376 | 3.204 | 20 | 20 | fits | 156,920 | 198 | 0.442 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 556,620 | 5.566 | 20 | 20 | fits | 85,529 | 31 | 0.763 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 167,096 | 1.671 | 20 | 24 | fits | 157,648 | 155 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 323,026 | 3.230 | 20 | 24 | fits | 156,920 | 198 | 0.442 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 322,960 | 3.230 | 20 | 50 | fits | 156,920 | 198 | 0.442 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 474,115 | 4.741 | 20 | 50 | fits | 151,551 | 182 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 559,578 | 5.596 | 20 | 20 | fits | 85,529 | 31 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 962,457 | 9.625 | 20 | 20 | fits | 61,589 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 407,780 | 4.078 | 20 | 20 | fits | 151,501 | 145 | 0.481 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 143,629 | 1.436 | 20 | 200 | fits | 151,245 | 232 | 0.376 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 451,583 | 4.516 | 20 | 200 | fits | 151,501 | 145 | 0.481 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 144,553 | 1.446 | 20 | 20 | fits | 151,245 | 232 | 0.376 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 538,654 | 5.387 | 20 | 20 | fits | 86,367 | 37 | 0.732 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 305,262 | 3.053 | 20 | 24 | fits | 157,069 | 152 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 455,773 | 4.558 | 20 | 24 | fits | 151,501 | 145 | 0.481 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 147,137 | 1.471 | 20 | 50 | fits | 151,245 | 232 | 0.376 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 146,741 | 1.467 | 20 | 50 | fits | 151,245 | 232 | 0.376 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 541,612 | 5.416 | 20 | 20 | fits | 86,367 | 37 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 953,504 | 9.535 | 20 | 20 | fits | 70,648 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 488,010 | 4.880 | 20 | 20 | fits | 152,990 | 187 | 0.394 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 388,940 | 3.889 | 20 | 200 | fits | 155,417 | 194 | 0.449 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 541,314 | 5.413 | 20 | 200 | fits | 152,990 | 187 | 0.394 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 389,864 | 3.899 | 20 | 20 | fits | 155,417 | 194 | 0.449 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 627,510 | 6.275 | 20 | 20 | fits | 85,492 | 31 | 0.763 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 238,087 | 2.381 | 20 | 24 | fits | 158,253 | 155 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 392,514 | 3.925 | 20 | 24 | fits | 155,417 | 194 | 0.449 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 392,448 | 3.924 | 20 | 50 | fits | 155,417 | 194 | 0.449 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 545,042 | 5.450 | 20 | 50 | fits | 152,990 | 187 | 0.394 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 630,468 | 6.305 | 20 | 20 | fits | 85,492 | 31 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 1,032,494 | 10.325 | 20 | 20 | fits | 61,518 | 24 | 0.681 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 475,510 | 4.755 | 20 | 20 | fits | 152,990 | 187 | 0.394 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 376,440 | 3.764 | 20 | 200 | fits | 155,417 | 194 | 0.449 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 528,814 | 5.288 | 20 | 200 | fits | 152,990 | 187 | 0.394 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 377,364 | 3.774 | 20 | 20 | fits | 155,417 | 194 | 0.449 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 615,010 | 6.150 | 20 | 20 | fits | 85,492 | 31 | 0.763 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 225,587 | 2.256 | 20 | 24 | fits | 158,253 | 155 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 380,014 | 3.800 | 20 | 24 | fits | 155,417 | 194 | 0.449 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 379,948 | 3.799 | 20 | 50 | fits | 155,417 | 194 | 0.449 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 532,542 | 5.325 | 20 | 50 | fits | 152,990 | 187 | 0.394 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 617,968 | 6.180 | 20 | 20 | fits | 85,492 | 31 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 1,019,994 | 10.200 | 20 | 20 | fits | 61,518 | 24 | 0.681 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 463,010 | 4.630 | 20 | 20 | fits | 152,990 | 187 | 0.394 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 363,940 | 3.639 | 20 | 200 | fits | 155,417 | 194 | 0.449 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 516,314 | 5.163 | 20 | 200 | fits | 152,990 | 187 | 0.394 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 364,864 | 3.649 | 20 | 20 | fits | 155,417 | 194 | 0.449 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 602,510 | 6.025 | 20 | 20 | fits | 85,492 | 31 | 0.763 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 213,087 | 2.131 | 20 | 24 | fits | 158,253 | 155 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 367,514 | 3.675 | 20 | 24 | fits | 155,417 | 194 | 0.449 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 367,448 | 3.674 | 20 | 50 | fits | 155,417 | 194 | 0.449 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 520,042 | 5.200 | 20 | 50 | fits | 152,990 | 187 | 0.394 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 605,468 | 6.055 | 20 | 20 | fits | 85,492 | 31 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 1,007,494 | 10.075 | 20 | 20 | fits | 61,518 | 24 | 0.681 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 460,260 | 4.603 | 20 | 20 | fits | 155,206 | 192 | 0.408 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 359,088 | 3.591 | 20 | 200 | fits | 157,627 | 197 | 0.443 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 513,678 | 5.137 | 20 | 200 | fits | 155,206 | 192 | 0.408 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 360,012 | 3.600 | 20 | 20 | fits | 157,627 | 197 | 0.443 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 600,331 | 6.003 | 20 | 20 | fits | 85,949 | 37 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 196,487 | 1.965 | 20 | 24 | fits | 147,037 | 146 | 0.411 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 362,662 | 3.627 | 20 | 24 | fits | 157,627 | 197 | 0.443 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 362,596 | 3.626 | 20 | 50 | fits | 157,627 | 197 | 0.443 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 517,406 | 5.174 | 20 | 50 | fits | 155,206 | 192 | 0.408 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 603,289 | 6.033 | 20 | 20 | fits | 85,949 | 37 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 1,006,590 | 10.066 | 20 | 20 | fits | 76,877 | 35 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 435,260 | 4.353 | 20 | 20 | fits | 155,206 | 192 | 0.408 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 334,088 | 3.341 | 20 | 200 | fits | 157,627 | 197 | 0.443 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 488,678 | 4.887 | 20 | 200 | fits | 155,206 | 192 | 0.408 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 335,012 | 3.350 | 20 | 20 | fits | 157,627 | 197 | 0.443 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 575,331 | 5.753 | 20 | 20 | fits | 85,949 | 37 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 171,487 | 1.715 | 20 | 24 | fits | 147,037 | 146 | 0.411 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 337,662 | 3.377 | 20 | 24 | fits | 157,627 | 197 | 0.443 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 337,596 | 3.376 | 20 | 50 | fits | 157,627 | 197 | 0.443 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 492,406 | 4.924 | 20 | 50 | fits | 155,206 | 192 | 0.408 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 578,289 | 5.783 | 20 | 20 | fits | 85,949 | 37 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 981,590 | 9.816 | 20 | 20 | fits | 76,877 | 35 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 410,260 | 4.103 | 20 | 20 | fits | 155,206 | 192 | 0.408 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 309,088 | 3.091 | 20 | 200 | fits | 157,627 | 197 | 0.443 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 463,678 | 4.637 | 20 | 200 | fits | 155,206 | 192 | 0.408 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 310,012 | 3.100 | 20 | 20 | fits | 157,627 | 197 | 0.443 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 550,331 | 5.503 | 20 | 20 | fits | 85,949 | 37 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 146,487 | 1.465 | 20 | 24 | fits | 147,037 | 146 | 0.411 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 312,662 | 3.127 | 20 | 24 | fits | 157,627 | 197 | 0.443 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 312,596 | 3.126 | 20 | 50 | fits | 157,627 | 197 | 0.443 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 467,406 | 4.674 | 20 | 50 | fits | 155,206 | 192 | 0.408 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 553,289 | 5.533 | 20 | 20 | fits | 85,949 | 37 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 956,590 | 9.566 | 20 | 20 | fits | 76,877 | 35 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 410,077 | 4.101 | 20 | 20 | fits | 155,511 | 191 | 0.414 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 308,939 | 3.089 | 20 | 200 | fits | 157,643 | 197 | 0.443 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 463,834 | 4.638 | 20 | 200 | fits | 155,511 | 191 | 0.414 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 309,863 | 3.099 | 20 | 20 | fits | 157,643 | 197 | 0.443 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 550,500 | 5.505 | 20 | 20 | fits | 85,962 | 37 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 146,278 | 1.463 | 20 | 24 | fits | 146,893 | 146 | 0.410 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 312,513 | 3.125 | 20 | 24 | fits | 157,643 | 197 | 0.443 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 312,447 | 3.124 | 20 | 50 | fits | 157,643 | 197 | 0.443 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 467,562 | 4.676 | 20 | 50 | fits | 155,511 | 191 | 0.414 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 553,458 | 5.535 | 20 | 20 | fits | 85,962 | 37 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 939,467 | 9.395 | 20 | 20 | fits | 70,643 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 482,881 | 4.829 | 20 | 20 | fits | 154,307 | 189 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 393,615 | 3.936 | 20 | 200 | fits | 156,785 | 198 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 547,306 | 5.473 | 20 | 200 | fits | 154,307 | 189 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 394,539 | 3.945 | 20 | 20 | fits | 156,785 | 198 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 632,989 | 6.330 | 20 | 20 | fits | 84,979 | 31 | 0.760 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 231,856 | 2.319 | 20 | 24 | fits | 158,498 | 156 | 0.402 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 397,189 | 3.972 | 20 | 24 | fits | 156,785 | 198 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 397,123 | 3.971 | 20 | 50 | fits | 156,785 | 198 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 551,034 | 5.510 | 20 | 50 | fits | 154,307 | 189 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 635,947 | 6.359 | 20 | 20 | fits | 84,979 | 31 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 1,012,910 | 10.129 | 20 | 20 | fits | 61,584 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 393,374 | 3.934 | 20 | 20 | fits | 152,893 | 201 | 0.427 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 303,516 | 3.035 | 20 | 200 | fits | 152,204 | 185 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 455,793 | 4.558 | 20 | 200 | fits | 152,893 | 201 | 0.427 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 304,440 | 3.044 | 20 | 20 | fits | 152,204 | 185 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 542,761 | 5.428 | 20 | 20 | fits | 86,264 | 37 | 0.732 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 146,006 | 1.460 | 20 | 24 | fits | 152,707 | 146 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 307,090 | 3.071 | 20 | 24 | fits | 152,204 | 185 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 307,024 | 3.070 | 20 | 50 | fits | 152,204 | 185 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 459,521 | 4.595 | 20 | 50 | fits | 152,893 | 201 | 0.427 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 545,719 | 5.457 | 20 | 20 | fits | 86,264 | 37 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 931,726 | 9.317 | 20 | 20 | fits | 70,643 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 393,374 | 3.934 | 20 | 20 | fits | 152,893 | 201 | 0.427 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 303,516 | 3.035 | 20 | 200 | fits | 152,204 | 185 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 455,793 | 4.558 | 20 | 200 | fits | 152,893 | 201 | 0.427 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 304,440 | 3.044 | 20 | 20 | fits | 152,204 | 185 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 542,761 | 5.428 | 20 | 20 | fits | 86,264 | 37 | 0.732 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 146,006 | 1.460 | 20 | 24 | fits | 152,707 | 146 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 307,090 | 3.071 | 20 | 24 | fits | 152,204 | 185 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 307,024 | 3.070 | 20 | 50 | fits | 152,204 | 185 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 459,521 | 4.595 | 20 | 50 | fits | 152,893 | 201 | 0.427 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 545,719 | 5.457 | 20 | 20 | fits | 86,264 | 37 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 931,726 | 9.317 | 20 | 20 | fits | 70,643 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 393,374 | 3.934 | 20 | 20 | fits | 152,893 | 201 | 0.427 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 303,516 | 3.035 | 20 | 200 | fits | 152,204 | 185 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 455,793 | 4.558 | 20 | 200 | fits | 152,893 | 201 | 0.427 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 304,440 | 3.044 | 20 | 20 | fits | 152,204 | 185 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 542,761 | 5.428 | 20 | 20 | fits | 86,264 | 37 | 0.732 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 146,006 | 1.460 | 20 | 24 | fits | 152,707 | 146 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 307,090 | 3.071 | 20 | 24 | fits | 152,204 | 185 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 307,024 | 3.070 | 20 | 50 | fits | 152,204 | 185 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 459,521 | 4.595 | 20 | 50 | fits | 152,893 | 201 | 0.427 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 545,719 | 5.457 | 20 | 20 | fits | 86,264 | 37 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 931,726 | 9.317 | 20 | 20 | fits | 70,643 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 428,157 | 4.282 | 20 | 20 | fits | 157,103 | 192 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 314,811 | 3.148 | 20 | 200 | fits | 157,290 | 198 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 481,740 | 4.817 | 20 | 200 | fits | 157,103 | 192 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 315,735 | 3.157 | 20 | 20 | fits | 157,290 | 198 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 569,061 | 5.691 | 20 | 20 | fits | 86,617 | 37 | 0.735 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 162,085 | 1.621 | 20 | 24 | fits | 146,577 | 145 | 0.405 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 318,385 | 3.184 | 20 | 24 | fits | 157,290 | 198 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 318,319 | 3.183 | 20 | 50 | fits | 157,290 | 198 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 485,468 | 4.855 | 20 | 50 | fits | 157,103 | 192 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 572,019 | 5.720 | 20 | 20 | fits | 86,617 | 37 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 958,065 | 9.581 | 20 | 20 | fits | 70,643 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 415,657 | 4.157 | 20 | 20 | fits | 157,103 | 192 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 302,311 | 3.023 | 20 | 200 | fits | 157,290 | 198 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 469,240 | 4.692 | 20 | 200 | fits | 157,103 | 192 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 303,235 | 3.032 | 20 | 20 | fits | 157,290 | 198 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 556,561 | 5.566 | 20 | 20 | fits | 86,617 | 37 | 0.735 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 149,585 | 1.496 | 20 | 24 | fits | 146,577 | 145 | 0.405 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 305,885 | 3.059 | 20 | 24 | fits | 157,290 | 198 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 305,819 | 3.058 | 20 | 50 | fits | 157,290 | 198 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 472,968 | 4.730 | 20 | 50 | fits | 157,103 | 192 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 559,519 | 5.595 | 20 | 20 | fits | 86,617 | 37 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 945,565 | 9.456 | 20 | 20 | fits | 70,643 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 499,024 | 4.990 | 20 | 20 | fits | 156,707 | 191 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 386,413 | 3.864 | 20 | 200 | fits | 157,388 | 198 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 552,946 | 5.529 | 20 | 200 | fits | 156,707 | 191 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 387,337 | 3.873 | 20 | 20 | fits | 157,388 | 198 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 640,243 | 6.402 | 20 | 20 | fits | 86,593 | 37 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 233,589 | 2.336 | 20 | 24 | fits | 146,636 | 145 | 0.405 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 389,987 | 3.900 | 20 | 24 | fits | 157,388 | 198 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 389,921 | 3.899 | 20 | 50 | fits | 157,388 | 198 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 556,674 | 5.567 | 20 | 50 | fits | 156,707 | 191 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 643,201 | 6.432 | 20 | 20 | fits | 86,593 | 37 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 1,029,247 | 10.292 | 20 | 20 | fits | 70,643 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 486,524 | 4.865 | 20 | 20 | fits | 156,707 | 191 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 373,913 | 3.739 | 20 | 200 | fits | 157,388 | 198 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 540,446 | 5.404 | 20 | 200 | fits | 156,707 | 191 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 374,837 | 3.748 | 20 | 20 | fits | 157,388 | 198 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 627,743 | 6.277 | 20 | 20 | fits | 86,593 | 37 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 221,089 | 2.211 | 20 | 24 | fits | 146,636 | 145 | 0.405 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 377,487 | 3.775 | 20 | 24 | fits | 157,388 | 198 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 377,421 | 3.774 | 20 | 50 | fits | 157,388 | 198 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 544,174 | 5.442 | 20 | 50 | fits | 156,707 | 191 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 630,701 | 6.307 | 20 | 20 | fits | 86,593 | 37 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 1,016,747 | 10.167 | 20 | 20 | fits | 70,643 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 474,024 | 4.740 | 20 | 20 | fits | 156,707 | 191 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 361,413 | 3.614 | 20 | 200 | fits | 157,388 | 198 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 527,946 | 5.279 | 20 | 200 | fits | 156,707 | 191 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 362,337 | 3.623 | 20 | 20 | fits | 157,388 | 198 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 615,243 | 6.152 | 20 | 20 | fits | 86,593 | 37 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 208,589 | 2.086 | 20 | 24 | fits | 146,636 | 145 | 0.405 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 364,987 | 3.650 | 20 | 24 | fits | 157,388 | 198 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 364,921 | 3.649 | 20 | 50 | fits | 157,388 | 198 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 531,674 | 5.317 | 20 | 50 | fits | 156,707 | 191 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 618,201 | 6.182 | 20 | 20 | fits | 86,593 | 37 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 1,004,247 | 10.042 | 20 | 20 | fits | 70,643 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 405,057 | 4.051 | 20 | 20 | fits | 155,499 | 191 | 0.414 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 303,931 | 3.039 | 20 | 200 | fits | 150,194 | 197 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 458,814 | 4.588 | 20 | 200 | fits | 155,499 | 191 | 0.414 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 304,855 | 3.049 | 20 | 20 | fits | 150,194 | 197 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 545,709 | 5.457 | 20 | 20 | fits | 86,191 | 37 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 148,613 | 1.486 | 20 | 24 | fits | 150,227 | 146 | 0.408 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 307,505 | 3.075 | 20 | 24 | fits | 150,194 | 197 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 307,439 | 3.074 | 20 | 50 | fits | 150,194 | 197 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 462,542 | 4.625 | 20 | 50 | fits | 155,499 | 191 | 0.414 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 548,667 | 5.487 | 20 | 20 | fits | 86,191 | 37 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 934,676 | 9.347 | 20 | 20 | fits | 70,643 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 405,057 | 4.051 | 20 | 20 | fits | 155,499 | 191 | 0.414 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 303,931 | 3.039 | 20 | 200 | fits | 150,194 | 197 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 458,814 | 4.588 | 20 | 200 | fits | 155,499 | 191 | 0.414 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 304,855 | 3.049 | 20 | 20 | fits | 150,194 | 197 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 545,709 | 5.457 | 20 | 20 | fits | 86,191 | 37 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 148,613 | 1.486 | 20 | 24 | fits | 150,227 | 146 | 0.408 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 307,505 | 3.075 | 20 | 24 | fits | 150,194 | 197 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 307,439 | 3.074 | 20 | 50 | fits | 150,194 | 197 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 462,542 | 4.625 | 20 | 50 | fits | 155,499 | 191 | 0.414 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 548,667 | 5.487 | 20 | 20 | fits | 86,191 | 37 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 934,676 | 9.347 | 20 | 20 | fits | 70,643 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 405,057 | 4.051 | 20 | 20 | fits | 155,499 | 191 | 0.414 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 303,931 | 3.039 | 20 | 200 | fits | 150,194 | 197 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 458,814 | 4.588 | 20 | 200 | fits | 155,499 | 191 | 0.414 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 304,855 | 3.049 | 20 | 20 | fits | 150,194 | 197 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 545,709 | 5.457 | 20 | 20 | fits | 86,191 | 37 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 148,613 | 1.486 | 20 | 24 | fits | 150,227 | 146 | 0.408 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 307,505 | 3.075 | 20 | 24 | fits | 150,194 | 197 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 307,439 | 3.074 | 20 | 50 | fits | 150,194 | 197 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 462,542 | 4.625 | 20 | 50 | fits | 155,499 | 191 | 0.414 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 548,667 | 5.487 | 20 | 20 | fits | 86,191 | 37 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 934,676 | 9.347 | 20 | 20 | fits | 70,643 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 386,003 | 3.860 | 20 | 20 | fits | 151,180 | 180 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 318,392 | 3.184 | 20 | 200 | fits | 150,568 | 197 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 468,956 | 4.690 | 20 | 200 | fits | 151,180 | 180 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 319,316 | 3.193 | 20 | 20 | fits | 150,568 | 197 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 555,408 | 5.554 | 20 | 20 | fits | 85,748 | 32 | 0.764 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 172,388 | 1.724 | 20 | 24 | fits | 156,804 | 152 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 321,966 | 3.220 | 20 | 24 | fits | 150,568 | 197 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 321,900 | 3.219 | 20 | 50 | fits | 150,568 | 197 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 472,684 | 4.727 | 20 | 50 | fits | 151,180 | 180 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 558,366 | 5.584 | 20 | 20 | fits | 85,748 | 32 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 952,769 | 9.528 | 20 | 20 | fits | 61,589 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 386,337 | 3.863 | 20 | 20 | fits | 152,024 | 184 | 0.407 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 299,176 | 2.992 | 20 | 200 | fits | 148,792 | 198 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 450,584 | 4.506 | 20 | 200 | fits | 152,024 | 184 | 0.407 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 300,100 | 3.001 | 20 | 20 | fits | 148,792 | 198 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 551,562 | 5.516 | 20 | 20 | fits | 89,957 | 38 | 0.775 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 154,948 | 1.549 | 20 | 24 | fits | 156,968 | 152 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 302,750 | 3.027 | 20 | 24 | fits | 148,792 | 198 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 302,684 | 3.027 | 20 | 50 | fits | 148,792 | 198 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 454,312 | 4.543 | 20 | 50 | fits | 152,024 | 184 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 554,520 | 5.545 | 20 | 20 | fits | 89,957 | 38 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 938,616 | 9.386 | 20 | 20 | fits | 68,552 | 30 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 404,995 | 4.050 | 20 | 20 | fits | 154,457 | 186 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 306,065 | 3.061 | 20 | 200 | fits | 150,883 | 198 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 469,991 | 4.700 | 20 | 200 | fits | 154,457 | 186 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 306,989 | 3.070 | 20 | 20 | fits | 150,883 | 198 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 556,380 | 5.564 | 20 | 20 | fits | 85,685 | 31 | 0.766 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 159,746 | 1.597 | 20 | 24 | fits | 156,968 | 152 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 309,639 | 3.096 | 20 | 24 | fits | 150,883 | 198 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 309,573 | 3.096 | 20 | 50 | fits | 150,883 | 198 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 473,719 | 4.737 | 20 | 50 | fits | 154,457 | 186 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 559,338 | 5.593 | 20 | 20 | fits | 85,685 | 31 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,021,151 | 10.212 | 20 | 20 | fits | 61,631 | 24 | 0.684 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 418,882 | 4.189 | 20 | 20 | fits | 154,339 | 187 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 308,544 | 3.085 | 20 | 200 | fits | 148,948 | 195 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 472,314 | 4.723 | 20 | 200 | fits | 154,339 | 187 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 309,468 | 3.095 | 20 | 20 | fits | 148,948 | 195 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 558,884 | 5.589 | 20 | 20 | fits | 85,866 | 31 | 0.767 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 164,160 | 1.642 | 20 | 24 | fits | 156,968 | 152 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 312,118 | 3.121 | 20 | 24 | fits | 148,948 | 195 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 312,052 | 3.121 | 20 | 50 | fits | 148,948 | 195 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 476,042 | 4.760 | 20 | 50 | fits | 154,339 | 187 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 561,842 | 5.618 | 20 | 20 | fits | 85,866 | 31 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,023,301 | 10.233 | 20 | 20 | fits | 61,589 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 410,852 | 4.109 | 20 | 20 | fits | 152,322 | 184 | 0.405 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 322,641 | 3.226 | 20 | 200 | fits | 149,166 | 198 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 474,347 | 4.743 | 20 | 200 | fits | 152,322 | 184 | 0.405 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 323,565 | 3.236 | 20 | 20 | fits | 149,166 | 198 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 558,767 | 5.588 | 20 | 20 | fits | 83,716 | 35 | 0.779 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 168,717 | 1.687 | 20 | 24 | fits | 157,111 | 153 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 326,215 | 3.262 | 20 | 24 | fits | 149,166 | 198 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 326,149 | 3.261 | 20 | 50 | fits | 149,166 | 198 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 478,075 | 4.781 | 20 | 50 | fits | 152,322 | 184 | 0.405 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 561,725 | 5.617 | 20 | 20 | fits | 83,716 | 35 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,042,744 | 10.427 | 20 | 20 | fits | 76,831 | 35 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 405,756 | 4.058 | 20 | 20 | fits | 152,691 | 169 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 317,467 | 3.175 | 20 | 200 | fits | 156,766 | 215 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 469,542 | 4.695 | 20 | 200 | fits | 152,691 | 169 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 318,391 | 3.184 | 20 | 20 | fits | 156,766 | 215 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 632,214 | 6.322 | 20 | 20 | fits | 84,965 | 32 | 0.755 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 165,265 | 1.653 | 20 | 24 | fits | 156,750 | 152 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 321,041 | 3.210 | 20 | 24 | fits | 156,766 | 215 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 320,975 | 3.210 | 20 | 50 | fits | 156,766 | 215 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 473,270 | 4.733 | 20 | 50 | fits | 152,691 | 169 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 635,172 | 6.352 | 20 | 20 | fits | 84,965 | 32 | 0.755 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,030,763 | 10.308 | 20 | 20 | fits | 61,518 | 24 | 0.681 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 410,135 | 4.101 | 20 | 20 | fits | 152,990 | 168 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 321,886 | 3.219 | 20 | 200 | fits | 156,771 | 215 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 474,260 | 4.743 | 20 | 200 | fits | 152,990 | 168 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 322,810 | 3.228 | 20 | 20 | fits | 156,771 | 215 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 637,070 | 6.371 | 20 | 20 | fits | 85,103 | 33 | 0.754 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 169,679 | 1.697 | 20 | 24 | fits | 156,750 | 152 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 325,460 | 3.255 | 20 | 24 | fits | 156,771 | 215 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 325,394 | 3.254 | 20 | 50 | fits | 156,771 | 215 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 477,988 | 4.780 | 20 | 50 | fits | 152,990 | 168 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 640,028 | 6.400 | 20 | 20 | fits | 85,103 | 33 | 0.754 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,034,052 | 10.341 | 20 | 20 | fits | 61,518 | 24 | 0.681 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 393,099 | 3.931 | 20 | 20 | fits | 157,734 | 220 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 290,044 | 2.900 | 20 | 200 | fits | 148,301 | 198 | 0.423 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 447,162 | 4.472 | 20 | 200 | fits | 157,734 | 220 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 290,968 | 2.910 | 20 | 20 | fits | 148,301 | 198 | 0.423 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 614,786 | 6.148 | 20 | 20 | fits | 89,973 | 44 | 0.732 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 146,307 | 1.463 | 20 | 24 | fits | 150,598 | 111 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 293,618 | 2.936 | 20 | 24 | fits | 148,301 | 198 | 0.423 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 293,552 | 2.936 | 20 | 50 | fits | 148,301 | 198 | 0.423 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 450,890 | 4.509 | 20 | 50 | fits | 157,734 | 220 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 617,744 | 6.177 | 20 | 20 | fits | 89,973 | 44 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,017,290 | 10.173 | 20 | 20 | fits | 70,648 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 393,275 | 3.933 | 20 | 20 | fits | 154,403 | 171 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 313,571 | 3.136 | 20 | 200 | fits | 156,649 | 215 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 467,358 | 4.674 | 20 | 200 | fits | 154,403 | 171 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 314,495 | 3.145 | 20 | 20 | fits | 156,649 | 215 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 468,062 | 4.681 | 20 | 20 | fits | 154,403 | 171 | 0.409 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 161,486 | 1.615 | 20 | 24 | fits | 156,812 | 152 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 317,145 | 3.171 | 20 | 24 | fits | 156,649 | 215 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 317,079 | 3.171 | 20 | 50 | fits | 156,649 | 215 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 471,086 | 4.711 | 20 | 50 | fits | 154,403 | 171 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 556,647 | 5.566 | 20 | 20 | fits | 85,627 | 28 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 942,282 | 9.423 | 20 | 20 | fits | 52,960 | 20 | 0.733 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 379,837 | 3.798 | 20 | 20 | fits | 151,180 | 180 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 312,226 | 3.122 | 20 | 200 | fits | 150,744 | 197 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 462,790 | 4.628 | 20 | 200 | fits | 151,180 | 180 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 313,150 | 3.131 | 20 | 20 | fits | 150,744 | 197 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 549,267 | 5.493 | 20 | 20 | fits | 85,773 | 31 | 0.765 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 166,046 | 1.660 | 20 | 24 | fits | 156,914 | 152 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 315,800 | 3.158 | 20 | 24 | fits | 150,744 | 197 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 315,734 | 3.157 | 20 | 50 | fits | 150,744 | 197 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 466,518 | 4.665 | 20 | 50 | fits | 151,180 | 180 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 552,225 | 5.522 | 20 | 20 | fits | 85,773 | 31 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 954,358 | 9.544 | 20 | 20 | fits | 68,656 | 30 | 0.732 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 401,800 | 4.018 | 20 | 20 | fits | 150,926 | 180 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 316,678 | 3.167 | 20 | 200 | fits | 150,782 | 197 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 466,988 | 4.670 | 20 | 200 | fits | 150,926 | 180 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 317,602 | 3.176 | 20 | 20 | fits | 150,782 | 197 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 553,289 | 5.533 | 20 | 20 | fits | 85,597 | 32 | 0.762 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 170,460 | 1.705 | 20 | 24 | fits | 156,914 | 152 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 320,252 | 3.203 | 20 | 24 | fits | 150,782 | 197 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 320,186 | 3.202 | 20 | 50 | fits | 150,782 | 197 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 470,716 | 4.707 | 20 | 50 | fits | 150,926 | 180 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 556,247 | 5.562 | 20 | 20 | fits | 85,597 | 32 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 957,663 | 9.577 | 20 | 20 | fits | 61,589 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 394,310 | 3.943 | 20 | 20 | fits | 151,542 | 183 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 297,418 | 2.974 | 20 | 200 | fits | 148,776 | 198 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 448,344 | 4.483 | 20 | 200 | fits | 151,542 | 183 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 298,342 | 2.983 | 20 | 20 | fits | 148,776 | 198 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 549,224 | 5.492 | 20 | 20 | fits | 89,943 | 38 | 0.775 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 153,206 | 1.532 | 20 | 24 | fits | 156,750 | 152 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 300,992 | 3.010 | 20 | 24 | fits | 148,776 | 198 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 300,926 | 3.009 | 20 | 50 | fits | 148,776 | 198 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 452,072 | 4.521 | 20 | 50 | fits | 151,542 | 183 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 552,182 | 5.522 | 20 | 20 | fits | 89,943 | 38 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 936,445 | 9.364 | 20 | 20 | fits | 61,589 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 412,507 | 4.125 | 20 | 20 | fits | 156,453 | 191 | 0.435 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 310,633 | 3.106 | 20 | 200 | fits | 157,577 | 201 | 0.424 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 476,467 | 4.765 | 20 | 200 | fits | 156,453 | 191 | 0.435 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 311,557 | 3.116 | 20 | 20 | fits | 157,577 | 201 | 0.424 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 477,171 | 4.772 | 20 | 20 | fits | 156,453 | 191 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 157,620 | 1.576 | 20 | 24 | fits | 156,750 | 152 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 314,207 | 3.142 | 20 | 24 | fits | 157,577 | 201 | 0.424 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 314,141 | 3.141 | 20 | 50 | fits | 157,577 | 201 | 0.424 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 480,195 | 4.802 | 20 | 50 | fits | 156,453 | 191 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 570,386 | 5.704 | 20 | 20 | fits | 90,257 | 34 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 938,366 | 9.384 | 20 | 20 | fits | 52,530 | 20 | 0.721 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 412,708 | 4.127 | 20 | 20 | fits | 150,775 | 180 | 0.447 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 315,955 | 3.160 | 20 | 200 | fits | 149,166 | 198 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 466,114 | 4.661 | 20 | 200 | fits | 150,775 | 180 | 0.447 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 316,879 | 3.169 | 20 | 20 | fits | 149,166 | 198 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 553,021 | 5.530 | 20 | 20 | fits | 86,203 | 37 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 162,240 | 1.622 | 20 | 24 | fits | 156,956 | 153 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 319,529 | 3.195 | 20 | 24 | fits | 149,166 | 198 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 319,463 | 3.195 | 20 | 50 | fits | 149,166 | 198 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 469,842 | 4.698 | 20 | 50 | fits | 150,775 | 180 | 0.447 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 555,979 | 5.560 | 20 | 20 | fits | 86,203 | 37 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 942,170 | 9.422 | 20 | 20 | fits | 70,827 | 29 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 417,588 | 4.176 | 20 | 20 | fits | 152,890 | 168 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 329,439 | 3.294 | 20 | 200 | fits | 156,738 | 215 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 481,713 | 4.817 | 20 | 200 | fits | 152,890 | 168 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 330,363 | 3.304 | 20 | 20 | fits | 156,738 | 215 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 567,553 | 5.676 | 20 | 20 | fits | 85,136 | 31 | 0.761 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 177,265 | 1.773 | 20 | 24 | fits | 157,236 | 153 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 333,013 | 3.330 | 20 | 24 | fits | 156,738 | 215 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 332,947 | 3.329 | 20 | 50 | fits | 156,738 | 215 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 485,441 | 4.854 | 20 | 50 | fits | 152,890 | 168 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 570,511 | 5.705 | 20 | 20 | fits | 85,136 | 31 | 0.761 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 965,188 | 9.652 | 20 | 20 | fits | 62,033 | 24 | 0.696 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 403,014 | 4.030 | 20 | 20 | fits | 152,028 | 183 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 315,761 | 3.158 | 20 | 200 | fits | 155,765 | 198 | 0.439 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 467,173 | 4.672 | 20 | 200 | fits | 152,028 | 183 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 316,685 | 3.167 | 20 | 20 | fits | 155,765 | 198 | 0.439 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 553,599 | 5.536 | 20 | 20 | fits | 85,722 | 31 | 0.766 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 164,560 | 1.646 | 20 | 24 | fits | 156,968 | 152 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 319,335 | 3.193 | 20 | 24 | fits | 155,765 | 198 | 0.439 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 319,269 | 3.193 | 20 | 50 | fits | 155,765 | 198 | 0.439 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 470,901 | 4.709 | 20 | 50 | fits | 152,028 | 183 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 556,557 | 5.566 | 20 | 20 | fits | 85,722 | 31 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 951,378 | 9.514 | 20 | 20 | fits | 61,589 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 411,423 | 4.114 | 20 | 20 | fits | 152,205 | 184 | 0.404 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 323,281 | 3.233 | 20 | 200 | fits | 157,330 | 200 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 474,870 | 4.749 | 20 | 200 | fits | 152,205 | 184 | 0.404 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 324,205 | 3.242 | 20 | 20 | fits | 157,330 | 200 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 475,574 | 4.756 | 20 | 20 | fits | 152,205 | 184 | 0.404 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 170,515 | 1.705 | 20 | 24 | fits | 157,020 | 152 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 326,855 | 3.269 | 20 | 24 | fits | 157,330 | 200 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 326,789 | 3.268 | 20 | 50 | fits | 157,330 | 200 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 478,598 | 4.786 | 20 | 50 | fits | 152,205 | 184 | 0.404 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 564,081 | 5.641 | 20 | 20 | fits | 85,549 | 28 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 949,633 | 9.496 | 20 | 20 | fits | 52,960 | 20 | 0.733 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 385,105 | 3.851 | 20 | 20 | fits | 151,680 | 184 | 0.398 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 297,488 | 2.975 | 20 | 200 | fits | 148,791 | 198 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 448,552 | 4.486 | 20 | 200 | fits | 151,680 | 184 | 0.398 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 298,412 | 2.984 | 20 | 20 | fits | 148,791 | 198 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 534,749 | 5.347 | 20 | 20 | fits | 85,493 | 31 | 0.764 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 153,261 | 1.533 | 20 | 24 | fits | 156,859 | 152 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 301,062 | 3.011 | 20 | 24 | fits | 148,791 | 198 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 300,996 | 3.010 | 20 | 50 | fits | 148,791 | 198 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 452,280 | 4.523 | 20 | 50 | fits | 151,680 | 184 | 0.398 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 537,707 | 5.377 | 20 | 20 | fits | 85,493 | 31 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 940,461 | 9.405 | 20 | 20 | fits | 68,538 | 30 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 389,654 | 3.897 | 20 | 20 | fits | 154,163 | 172 | 0.403 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 309,851 | 3.099 | 20 | 200 | fits | 156,740 | 215 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 463,398 | 4.634 | 20 | 200 | fits | 154,163 | 172 | 0.403 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 310,775 | 3.108 | 20 | 20 | fits | 156,740 | 215 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 464,102 | 4.641 | 20 | 20 | fits | 154,163 | 172 | 0.403 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 157,675 | 1.577 | 20 | 24 | fits | 156,859 | 152 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 313,425 | 3.134 | 20 | 24 | fits | 156,740 | 215 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 313,359 | 3.134 | 20 | 50 | fits | 156,740 | 215 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 467,126 | 4.671 | 20 | 50 | fits | 154,163 | 172 | 0.403 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 552,526 | 5.525 | 20 | 20 | fits | 85,466 | 29 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,026,646 | 10.266 | 20 | 20 | fits | 52,737 | 20 | 0.728 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 394,031 | 3.940 | 20 | 20 | fits | 154,505 | 172 | 0.410 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 314,270 | 3.143 | 20 | 200 | fits | 156,745 | 215 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 468,159 | 4.682 | 20 | 200 | fits | 154,505 | 172 | 0.410 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 315,194 | 3.152 | 20 | 20 | fits | 156,745 | 215 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 468,863 | 4.689 | 20 | 20 | fits | 154,505 | 172 | 0.410 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 162,089 | 1.621 | 20 | 24 | fits | 156,859 | 152 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 317,844 | 3.178 | 20 | 24 | fits | 156,745 | 215 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 317,778 | 3.178 | 20 | 50 | fits | 156,745 | 215 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 471,887 | 4.719 | 20 | 50 | fits | 154,505 | 172 | 0.410 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 571,298 | 5.713 | 20 | 20 | fits | 89,160 | 35 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,028,188 | 10.282 | 20 | 20 | fits | 52,530 | 20 | 0.721 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 394,172 | 3.942 | 20 | 20 | fits | 155,220 | 187 | 0.447 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 312,760 | 3.128 | 20 | 200 | fits | 150,821 | 198 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 477,449 | 4.774 | 20 | 200 | fits | 155,220 | 187 | 0.447 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 313,684 | 3.137 | 20 | 20 | fits | 150,821 | 198 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 561,793 | 5.618 | 20 | 20 | fits | 83,640 | 35 | 0.778 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 166,503 | 1.665 | 20 | 24 | fits | 156,859 | 152 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 316,334 | 3.163 | 20 | 24 | fits | 150,821 | 198 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 316,268 | 3.163 | 20 | 50 | fits | 150,821 | 198 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 481,177 | 4.812 | 20 | 50 | fits | 155,220 | 187 | 0.447 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 564,751 | 5.648 | 20 | 20 | fits | 83,640 | 35 | 0.778 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,032,848 | 10.328 | 20 | 20 | fits | 70,648 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 430,777 | 4.308 | 20 | 20 | fits | 150,772 | 180 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 325,493 | 3.255 | 20 | 200 | fits | 149,503 | 198 | 0.432 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 475,649 | 4.756 | 20 | 200 | fits | 150,772 | 180 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 326,417 | 3.264 | 20 | 20 | fits | 149,503 | 198 | 0.432 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 642,919 | 6.429 | 20 | 20 | fits | 86,307 | 38 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 171,148 | 1.711 | 20 | 24 | fits | 157,090 | 153 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 329,067 | 3.291 | 20 | 24 | fits | 149,503 | 198 | 0.432 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 329,001 | 3.290 | 20 | 50 | fits | 149,503 | 198 | 0.432 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 479,377 | 4.794 | 20 | 50 | fits | 150,772 | 180 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 645,877 | 6.459 | 20 | 20 | fits | 86,307 | 38 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,049,441 | 10.494 | 20 | 20 | fits | 76,908 | 35 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 403,775 | 4.038 | 20 | 20 | fits | 159,526 | 206 | 0.436 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 289,083 | 2.891 | 20 | 200 | fits | 151,891 | 185 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 447,993 | 4.480 | 20 | 200 | fits | 159,526 | 206 | 0.436 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 290,007 | 2.900 | 20 | 20 | fits | 151,891 | 185 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 615,303 | 6.153 | 20 | 20 | fits | 86,264 | 38 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 141,756 | 1.418 | 20 | 24 | fits | 148,272 | 147 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 292,657 | 2.927 | 20 | 24 | fits | 151,891 | 185 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 292,591 | 2.926 | 20 | 50 | fits | 151,891 | 185 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 451,721 | 4.517 | 20 | 50 | fits | 159,526 | 206 | 0.436 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 618,261 | 6.183 | 20 | 20 | fits | 86,264 | 38 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,023,148 | 10.231 | 20 | 20 | fits | 70,819 | 28 | 0.656 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 501,615 | 5.016 | 20 | 20 | fits | 152,924 | 187 | 0.395 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 322,327 | 3.223 | 20 | 200 | fits | 154,671 | 194 | 0.447 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 554,986 | 5.550 | 20 | 200 | fits | 152,924 | 187 | 0.395 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 323,251 | 3.233 | 20 | 20 | fits | 154,671 | 194 | 0.447 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 641,341 | 6.413 | 20 | 20 | fits | 85,651 | 31 | 0.765 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 172,220 | 1.722 | 20 | 24 | fits | 156,969 | 152 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 325,901 | 3.259 | 20 | 24 | fits | 154,671 | 194 | 0.447 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 325,835 | 3.258 | 20 | 50 | fits | 154,671 | 194 | 0.447 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 558,714 | 5.587 | 20 | 50 | fits | 152,924 | 187 | 0.395 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 644,299 | 6.443 | 20 | 20 | fits | 85,651 | 31 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,038,821 | 10.388 | 20 | 20 | fits | 61,518 | 24 | 0.681 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 409,732 | 4.097 | 20 | 20 | fits | 151,854 | 184 | 0.401 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 321,941 | 3.219 | 20 | 200 | fits | 149,586 | 198 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 473,179 | 4.732 | 20 | 200 | fits | 151,854 | 184 | 0.401 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 322,865 | 3.229 | 20 | 20 | fits | 149,586 | 198 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 559,308 | 5.593 | 20 | 20 | fits | 85,425 | 31 | 0.764 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 167,585 | 1.676 | 20 | 24 | fits | 157,272 | 153 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 325,515 | 3.255 | 20 | 24 | fits | 149,586 | 198 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 325,449 | 3.254 | 20 | 50 | fits | 149,586 | 198 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 476,907 | 4.769 | 20 | 50 | fits | 151,854 | 184 | 0.401 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 562,266 | 5.623 | 20 | 20 | fits | 85,425 | 31 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 938,911 | 9.389 | 20 | 20 | fits | 61,513 | 24 | 0.681 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 413,915 | 4.139 | 20 | 20 | fits | 152,383 | 184 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 325,643 | 3.256 | 20 | 200 | fits | 148,964 | 198 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 477,410 | 4.774 | 20 | 200 | fits | 152,383 | 184 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 326,567 | 3.266 | 20 | 20 | fits | 148,964 | 198 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 563,652 | 5.637 | 20 | 20 | fits | 85,538 | 31 | 0.765 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 171,909 | 1.719 | 20 | 24 | fits | 157,182 | 153 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 329,217 | 3.292 | 20 | 24 | fits | 148,964 | 198 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 329,151 | 3.292 | 20 | 50 | fits | 148,964 | 198 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 481,138 | 4.811 | 20 | 50 | fits | 152,383 | 184 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 566,610 | 5.666 | 20 | 20 | fits | 85,538 | 31 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 950,822 | 9.508 | 20 | 20 | fits | 68,779 | 31 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 401,658 | 4.017 | 20 | 20 | fits | 154,163 | 172 | 0.403 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 321,855 | 3.219 | 20 | 200 | fits | 156,863 | 215 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 475,402 | 4.754 | 20 | 200 | fits | 154,163 | 172 | 0.403 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 322,779 | 3.228 | 20 | 20 | fits | 156,863 | 215 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 476,106 | 4.761 | 20 | 20 | fits | 154,163 | 172 | 0.403 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 169,556 | 1.696 | 20 | 24 | fits | 156,805 | 152 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 325,429 | 3.254 | 20 | 24 | fits | 156,863 | 215 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 325,363 | 3.254 | 20 | 50 | fits | 156,863 | 215 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 479,130 | 4.791 | 20 | 50 | fits | 154,163 | 172 | 0.403 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 564,564 | 5.646 | 20 | 20 | fits | 85,500 | 28 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 953,510 | 9.535 | 20 | 20 | fits | 61,518 | 24 | 0.681 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 386,198 | 3.862 | 20 | 20 | fits | 150,899 | 217 | 0.413 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 289,895 | 2.899 | 20 | 200 | fits | 148,275 | 198 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 440,178 | 4.402 | 20 | 200 | fits | 150,899 | 217 | 0.413 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 290,819 | 2.908 | 20 | 20 | fits | 148,275 | 198 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 527,177 | 5.272 | 20 | 20 | fits | 86,295 | 37 | 0.731 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 146,184 | 1.462 | 20 | 24 | fits | 150,653 | 111 | 0.407 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 293,469 | 2.935 | 20 | 24 | fits | 148,275 | 198 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 293,403 | 2.934 | 20 | 50 | fits | 148,275 | 198 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 443,906 | 4.439 | 20 | 50 | fits | 150,899 | 217 | 0.413 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 530,135 | 5.301 | 20 | 20 | fits | 86,295 | 37 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 937,230 | 9.372 | 20 | 20 | fits | 79,278 | 32 | 0.621 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 388,864 | 3.889 | 20 | 20 | fits | 154,505 | 172 | 0.410 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 309,103 | 3.091 | 20 | 200 | fits | 156,753 | 215 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 462,992 | 4.630 | 20 | 200 | fits | 154,505 | 172 | 0.410 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 310,027 | 3.100 | 20 | 20 | fits | 156,753 | 215 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 463,696 | 4.637 | 20 | 20 | fits | 154,505 | 172 | 0.410 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 156,914 | 1.569 | 20 | 24 | fits | 156,969 | 152 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 312,677 | 3.127 | 20 | 24 | fits | 156,753 | 215 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 312,611 | 3.126 | 20 | 50 | fits | 156,753 | 215 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 466,720 | 4.667 | 20 | 50 | fits | 154,505 | 172 | 0.410 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 560,347 | 5.603 | 20 | 20 | fits | 83,460 | 37 | 0.788 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 937,393 | 9.374 | 20 | 20 | fits | 61,589 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 386,518 | 3.865 | 20 | 20 | fits | 151,958 | 183 | 0.458 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 307,431 | 3.074 | 20 | 200 | fits | 150,667 | 197 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 458,773 | 4.588 | 20 | 200 | fits | 151,958 | 183 | 0.458 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 308,355 | 3.084 | 20 | 20 | fits | 150,667 | 197 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 558,109 | 5.581 | 20 | 20 | fits | 88,209 | 38 | 0.744 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 161,328 | 1.613 | 20 | 24 | fits | 156,969 | 152 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 311,005 | 3.110 | 20 | 24 | fits | 150,667 | 197 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 310,939 | 3.109 | 20 | 50 | fits | 150,667 | 197 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 462,501 | 4.625 | 20 | 50 | fits | 151,958 | 183 | 0.458 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 561,067 | 5.611 | 20 | 20 | fits | 88,209 | 38 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 947,326 | 9.473 | 20 | 20 | fits | 70,648 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 418,215 | 4.182 | 20 | 20 | fits | 151,493 | 182 | 0.464 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 312,019 | 3.120 | 20 | 200 | fits | 150,841 | 198 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 472,854 | 4.729 | 20 | 200 | fits | 151,493 | 182 | 0.464 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 312,943 | 3.129 | 20 | 20 | fits | 150,841 | 198 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 559,784 | 5.598 | 20 | 20 | fits | 86,226 | 37 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 165,742 | 1.657 | 20 | 24 | fits | 156,969 | 152 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 315,593 | 3.156 | 20 | 24 | fits | 150,841 | 198 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 315,527 | 3.155 | 20 | 50 | fits | 150,841 | 198 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 476,582 | 4.766 | 20 | 50 | fits | 151,493 | 182 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 562,742 | 5.627 | 20 | 20 | fits | 86,226 | 37 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 948,796 | 9.488 | 20 | 20 | fits | 70,648 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 431,466 | 4.315 | 20 | 20 | fits | 155,677 | 193 | 0.411 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 329,887 | 3.299 | 20 | 200 | fits | 154,947 | 194 | 0.453 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 484,948 | 4.849 | 20 | 200 | fits | 155,677 | 193 | 0.411 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 330,811 | 3.308 | 20 | 20 | fits | 154,947 | 194 | 0.453 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 570,788 | 5.708 | 20 | 20 | fits | 85,136 | 31 | 0.762 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 170,342 | 1.703 | 20 | 24 | fits | 157,155 | 153 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 333,461 | 3.335 | 20 | 24 | fits | 154,947 | 194 | 0.453 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 333,395 | 3.334 | 20 | 50 | fits | 154,947 | 194 | 0.453 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 488,676 | 4.887 | 20 | 50 | fits | 155,677 | 193 | 0.411 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 573,746 | 5.737 | 20 | 20 | fits | 85,136 | 31 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 950,377 | 9.504 | 20 | 20 | fits | 61,518 | 24 | 0.681 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 409,616 | 4.096 | 20 | 20 | fits | 152,059 | 183 | 0.407 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 322,252 | 3.223 | 20 | 200 | fits | 149,085 | 198 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 473,695 | 4.737 | 20 | 200 | fits | 152,059 | 183 | 0.407 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 323,176 | 3.232 | 20 | 20 | fits | 149,085 | 198 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 560,061 | 5.601 | 20 | 20 | fits | 85,662 | 31 | 0.765 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 168,486 | 1.685 | 20 | 24 | fits | 157,108 | 153 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 325,826 | 3.258 | 20 | 24 | fits | 149,085 | 198 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 325,760 | 3.258 | 20 | 50 | fits | 149,085 | 198 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 477,423 | 4.774 | 20 | 50 | fits | 152,059 | 183 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 563,019 | 5.630 | 20 | 20 | fits | 85,662 | 31 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 940,036 | 9.400 | 20 | 20 | fits | 61,584 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 414,348 | 4.143 | 20 | 20 | fits | 152,094 | 183 | 0.408 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 327,072 | 3.271 | 20 | 200 | fits | 149,581 | 198 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 478,550 | 4.785 | 20 | 200 | fits | 152,094 | 183 | 0.408 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 327,996 | 3.280 | 20 | 20 | fits | 149,581 | 198 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 564,899 | 5.649 | 20 | 20 | fits | 85,645 | 31 | 0.765 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 172,810 | 1.728 | 20 | 24 | fits | 157,018 | 153 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 330,646 | 3.306 | 20 | 24 | fits | 149,581 | 198 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 330,580 | 3.306 | 20 | 50 | fits | 149,581 | 198 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 482,278 | 4.823 | 20 | 50 | fits | 152,094 | 183 | 0.408 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 567,857 | 5.679 | 20 | 20 | fits | 85,645 | 31 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 952,133 | 9.521 | 20 | 20 | fits | 68,779 | 31 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 384,803 | 3.848 | 20 | 20 | fits | 151,180 | 180 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 317,142 | 3.171 | 20 | 200 | fits | 150,837 | 197 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 467,706 | 4.677 | 20 | 200 | fits | 151,180 | 180 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 318,066 | 3.181 | 20 | 20 | fits | 150,837 | 197 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 554,301 | 5.543 | 20 | 20 | fits | 85,891 | 31 | 0.766 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 170,869 | 1.709 | 20 | 24 | fits | 156,969 | 152 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 320,716 | 3.207 | 20 | 24 | fits | 150,837 | 197 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 320,650 | 3.207 | 20 | 50 | fits | 150,837 | 197 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 471,434 | 4.714 | 20 | 50 | fits | 151,180 | 180 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 557,259 | 5.573 | 20 | 20 | fits | 85,891 | 31 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,033,887 | 10.339 | 20 | 20 | fits | 70,710 | 28 | 0.652 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 385,093 | 3.851 | 20 | 20 | fits | 152,029 | 183 | 0.407 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 297,882 | 2.979 | 20 | 200 | fits | 148,831 | 198 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 449,295 | 4.493 | 20 | 200 | fits | 152,029 | 183 | 0.407 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 298,806 | 2.988 | 20 | 20 | fits | 148,831 | 198 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 535,817 | 5.358 | 20 | 20 | fits | 85,818 | 31 | 0.765 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 153,615 | 1.536 | 20 | 24 | fits | 156,805 | 152 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 301,456 | 3.015 | 20 | 24 | fits | 148,831 | 198 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 301,390 | 3.014 | 20 | 50 | fits | 148,831 | 198 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 453,023 | 4.530 | 20 | 50 | fits | 152,029 | 183 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 538,775 | 5.388 | 20 | 20 | fits | 85,818 | 31 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,015,522 | 10.155 | 20 | 20 | fits | 70,648 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 389,397 | 3.894 | 20 | 20 | fits | 151,021 | 181 | 0.416 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 304,225 | 3.042 | 20 | 200 | fits | 150,760 | 197 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 454,630 | 4.546 | 20 | 200 | fits | 151,021 | 181 | 0.416 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 305,149 | 3.051 | 20 | 20 | fits | 150,760 | 197 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 552,540 | 5.525 | 20 | 20 | fits | 87,017 | 42 | 0.778 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 158,029 | 1.580 | 20 | 24 | fits | 156,805 | 152 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 307,799 | 3.078 | 20 | 24 | fits | 150,760 | 197 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 307,733 | 3.077 | 20 | 50 | fits | 150,760 | 197 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 458,358 | 4.584 | 20 | 50 | fits | 151,021 | 181 | 0.416 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 555,498 | 5.555 | 20 | 20 | fits | 87,017 | 42 | 0.778 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,019,641 | 10.196 | 20 | 20 | fits | 70,648 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 415,051 | 4.151 | 20 | 20 | fits | 153,306 | 188 | 0.445 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 315,387 | 3.154 | 20 | 200 | fits | 157,508 | 200 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 468,077 | 4.681 | 20 | 200 | fits | 153,306 | 188 | 0.445 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 316,311 | 3.163 | 20 | 20 | fits | 157,508 | 200 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 643,817 | 6.438 | 20 | 20 | fits | 87,751 | 32 | 0.776 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 162,443 | 1.624 | 20 | 24 | fits | 156,805 | 152 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 318,961 | 3.190 | 20 | 24 | fits | 157,508 | 200 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 318,895 | 3.189 | 20 | 50 | fits | 157,508 | 200 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 471,805 | 4.718 | 20 | 50 | fits | 153,306 | 188 | 0.445 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 646,775 | 6.468 | 20 | 20 | fits | 87,751 | 32 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,023,887 | 10.239 | 20 | 20 | fits | 61,589 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 420,304 | 4.203 | 20 | 20 | fits | 155,607 | 176 | 0.456 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 319,232 | 3.192 | 20 | 200 | fits | 156,939 | 216 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 484,255 | 4.843 | 20 | 200 | fits | 155,607 | 176 | 0.456 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 320,156 | 3.202 | 20 | 20 | fits | 156,939 | 216 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 648,260 | 6.483 | 20 | 20 | fits | 85,396 | 32 | 0.757 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 166,857 | 1.669 | 20 | 24 | fits | 156,805 | 152 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 322,806 | 3.228 | 20 | 24 | fits | 156,939 | 216 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 322,740 | 3.227 | 20 | 50 | fits | 156,939 | 216 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 487,983 | 4.880 | 20 | 50 | fits | 155,607 | 176 | 0.456 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 651,218 | 6.512 | 20 | 20 | fits | 85,396 | 32 | 0.757 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,028,322 | 10.283 | 20 | 20 | fits | 61,589 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 499,073 | 4.991 | 20 | 20 | fits | 154,271 | 189 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 332,335 | 3.323 | 20 | 200 | fits | 156,191 | 198 | 0.445 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 563,667 | 5.637 | 20 | 200 | fits | 154,271 | 189 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 333,259 | 3.333 | 20 | 20 | fits | 156,191 | 198 | 0.445 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 649,744 | 6.497 | 20 | 20 | fits | 85,373 | 31 | 0.763 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 171,457 | 1.715 | 20 | 24 | fits | 156,991 | 153 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 335,909 | 3.359 | 20 | 24 | fits | 156,191 | 198 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 335,843 | 3.358 | 20 | 50 | fits | 156,191 | 198 | 0.445 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 567,395 | 5.674 | 20 | 50 | fits | 154,271 | 189 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 652,702 | 6.527 | 20 | 20 | fits | 85,373 | 31 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,034,479 | 10.345 | 20 | 20 | fits | 66,363 | 31 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 390,747 | 3.907 | 20 | 20 | fits | 154,258 | 173 | 0.404 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 310,894 | 3.109 | 20 | 200 | fits | 156,862 | 215 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 464,536 | 4.645 | 20 | 200 | fits | 154,258 | 173 | 0.404 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 311,818 | 3.118 | 20 | 20 | fits | 156,862 | 215 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 465,240 | 4.652 | 20 | 20 | fits | 154,258 | 173 | 0.404 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 158,596 | 1.586 | 20 | 24 | fits | 156,969 | 152 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 314,468 | 3.145 | 20 | 24 | fits | 156,862 | 215 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 314,402 | 3.144 | 20 | 50 | fits | 156,862 | 215 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 468,264 | 4.683 | 20 | 50 | fits | 154,258 | 173 | 0.404 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 567,616 | 5.676 | 20 | 20 | fits | 89,140 | 35 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 935,310 | 9.353 | 20 | 20 | fits | 52,459 | 20 | 0.720 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 408,946 | 4.089 | 20 | 20 | fits | 158,523 | 178 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 315,476 | 3.155 | 20 | 200 | fits | 157,030 | 216 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 483,542 | 4.835 | 20 | 200 | fits | 158,523 | 178 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 316,400 | 3.164 | 20 | 20 | fits | 157,030 | 216 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 484,246 | 4.842 | 20 | 20 | fits | 158,523 | 178 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 163,010 | 1.630 | 20 | 24 | fits | 156,969 | 152 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 319,050 | 3.191 | 20 | 24 | fits | 157,030 | 216 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 318,984 | 3.190 | 20 | 50 | fits | 157,030 | 216 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 487,270 | 4.873 | 20 | 50 | fits | 158,523 | 178 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 572,529 | 5.725 | 20 | 20 | fits | 85,325 | 28 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 947,882 | 9.479 | 20 | 20 | fits | 52,863 | 20 | 0.729 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 409,301 | 4.093 | 20 | 20 | fits | 152,094 | 183 | 0.408 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 322,025 | 3.220 | 20 | 200 | fits | 149,581 | 198 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 473,503 | 4.735 | 20 | 200 | fits | 152,094 | 183 | 0.408 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 322,949 | 3.229 | 20 | 20 | fits | 149,581 | 198 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 559,850 | 5.598 | 20 | 20 | fits | 85,643 | 31 | 0.764 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 167,637 | 1.676 | 20 | 24 | fits | 157,182 | 153 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 325,599 | 3.256 | 20 | 24 | fits | 149,581 | 198 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 325,533 | 3.255 | 20 | 50 | fits | 149,581 | 198 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 477,231 | 4.772 | 20 | 50 | fits | 152,094 | 183 | 0.408 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 562,808 | 5.628 | 20 | 20 | fits | 85,643 | 31 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 952,190 | 9.522 | 20 | 20 | fits | 66,538 | 31 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 377,549 | 3.775 | 20 | 20 | fits | 151,123 | 180 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 309,945 | 3.099 | 20 | 200 | fits | 150,602 | 197 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 460,452 | 4.605 | 20 | 200 | fits | 151,123 | 180 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 310,869 | 3.109 | 20 | 20 | fits | 150,602 | 197 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 547,049 | 5.470 | 20 | 20 | fits | 85,893 | 31 | 0.766 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 163,907 | 1.639 | 20 | 24 | fits | 156,749 | 152 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 313,519 | 3.135 | 20 | 24 | fits | 150,602 | 197 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 313,453 | 3.135 | 20 | 50 | fits | 150,602 | 197 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 464,180 | 4.642 | 20 | 50 | fits | 151,123 | 180 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 550,007 | 5.500 | 20 | 20 | fits | 85,893 | 31 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 952,385 | 9.524 | 20 | 20 | fits | 62,104 | 24 | 0.697 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 400,066 | 4.001 | 20 | 20 | fits | 150,976 | 180 | 0.416 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 314,894 | 3.149 | 20 | 200 | fits | 150,821 | 197 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 465,254 | 4.653 | 20 | 200 | fits | 150,976 | 180 | 0.416 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 315,818 | 3.158 | 20 | 20 | fits | 150,821 | 197 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 549,756 | 5.498 | 20 | 20 | fits | 83,798 | 35 | 0.778 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 168,637 | 1.686 | 20 | 24 | fits | 156,859 | 152 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 318,468 | 3.185 | 20 | 24 | fits | 150,821 | 197 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 318,402 | 3.184 | 20 | 50 | fits | 150,821 | 197 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 468,982 | 4.690 | 20 | 50 | fits | 150,976 | 180 | 0.416 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 552,714 | 5.527 | 20 | 20 | fits | 83,798 | 35 | 0.778 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 956,759 | 9.568 | 20 | 20 | fits | 70,648 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 407,158 | 4.072 | 20 | 20 | fits | 150,949 | 145 | 0.480 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 143,251 | 1.433 | 20 | 200 | fits | 153,257 | 234 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 450,812 | 4.508 | 20 | 200 | fits | 150,949 | 145 | 0.480 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 144,175 | 1.442 | 20 | 20 | fits | 153,257 | 234 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 538,127 | 5.381 | 20 | 20 | fits | 86,611 | 38 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 305,043 | 3.050 | 20 | 24 | fits | 157,228 | 152 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 455,002 | 4.550 | 20 | 24 | fits | 150,949 | 145 | 0.480 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 146,759 | 1.468 | 20 | 50 | fits | 153,257 | 234 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 146,363 | 1.464 | 20 | 50 | fits | 153,257 | 234 | 0.385 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 541,085 | 5.411 | 20 | 20 | fits | 86,611 | 38 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 944,391 | 9.444 | 20 | 20 | fits | 70,648 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 395,782 | 3.958 | 20 | 20 | fits | 150,883 | 182 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 299,469 | 2.995 | 20 | 200 | fits | 149,030 | 198 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 449,736 | 4.497 | 20 | 200 | fits | 150,883 | 182 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 300,393 | 3.004 | 20 | 20 | fits | 149,030 | 198 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 551,856 | 5.519 | 20 | 20 | fits | 91,076 | 44 | 0.749 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 155,003 | 1.550 | 20 | 24 | fits | 157,023 | 152 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 303,043 | 3.030 | 20 | 24 | fits | 149,030 | 198 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 302,977 | 3.030 | 20 | 50 | fits | 149,030 | 198 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 453,464 | 4.535 | 20 | 50 | fits | 150,883 | 182 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 554,814 | 5.548 | 20 | 20 | fits | 91,076 | 44 | 0.749 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 941,032 | 9.410 | 20 | 20 | fits | 70,648 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 413,494 | 4.135 | 20 | 20 | fits | 156,018 | 190 | 0.435 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 311,976 | 3.120 | 20 | 200 | fits | 156,131 | 199 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 477,502 | 4.775 | 20 | 200 | fits | 156,018 | 190 | 0.435 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 312,900 | 3.129 | 20 | 20 | fits | 156,131 | 199 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 563,924 | 5.639 | 20 | 20 | fits | 85,718 | 31 | 0.766 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 160,409 | 1.604 | 20 | 24 | fits | 157,023 | 152 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 315,550 | 3.155 | 20 | 24 | fits | 156,131 | 199 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 315,484 | 3.155 | 20 | 50 | fits | 156,131 | 199 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 481,230 | 4.812 | 20 | 50 | fits | 156,018 | 190 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 566,882 | 5.669 | 20 | 20 | fits | 85,718 | 31 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 943,924 | 9.439 | 20 | 20 | fits | 61,589 | 24 | 0.682 |
| LINK_UP | `adp.link_up.if0` | 3,068 | 0.031 | 20 | 200 | fits | 35,008 | 43 (11) | 0.740 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,642 | 0.186 | 20 | 200 | fits | 27,794 | 23 (39) | 0.755 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 21,635 | 0.216 | 20 | 200 | fits | 2,816 | 10 (11) | 0.586 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 33,158 | 0.332 | 20 | 20 | fits | 40,408 | 27 (35) | 0.818 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 31,049 | 0.310 | 20 | 20 | fits | 35,598 | 23 (14) | 0.848 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 32,820 | 0.328 | 20 | 20 | fits | 36,367 | 24 (14) | 0.848 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 31,323 | 0.313 | 20 | 20 | fits | 38,400 | 21 (35) | 0.831 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 83,229 | 0.832 | 20 | 20 | fits | 28,504 | 8 | 0.766 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 45,968 | 0.460 | 20 | 20 | fits | 46,034 | 12 | 0.895 |
| malformed MRPDU discard | `srp.malformed.if0` | 24,368 | 0.244 | 20 | 20 | fits | 24,434 | 12 | 0.711 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 81,496 | 0.815 | 220 | 220 | fits | 44,249 | 6 | 0.898 |
| an event behind 15 others | `backlog.event.if0` | 171,680 | 1.717 | 20 | 200 | fits | 57,793 | 78 | 0.566 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 478,554 | 4.786 | 20 | 20 | fits | 78,423 | 71 | 0.416 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 433,344 | 4.333 | 20 | 200 | fits | 150,728 | 120 | 0.434 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 511,151 | 5.112 | 20 | 200 | fits | 78,423 | 71 | 0.416 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 429,022 | 4.290 | 20 | 20 | fits | 150,728 | 120 | 0.434 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 506,609 | 5.066 | 20 | 20 | fits | 78,423 | 71 | 0.416 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 160,368 | 1.604 | 20 | 24 | fits | 161,259 | 158 | 0.402 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 431,672 | 4.317 | 20 | 24 | fits | 150,728 | 120 | 0.434 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 431,606 | 4.316 | 20 | 50 | fits | 150,728 | 120 | 0.434 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 431,210 | 4.312 | 20 | 50 | fits | 150,728 | 120 | 0.434 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 509,567 | 5.096 | 20 | 20 | fits | 78,423 | 71 | 0.416 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 604,762 | 6.048 | 20 | 20 | fits | 23,978 | 24 | 0.333 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 409,960 | 4.100 | 20 | 20 | fits | 150,741 | 199 | 0.396 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 302,598 | 3.026 | 20 | 200 | fits | 151,232 | 181 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 452,723 | 4.527 | 20 | 200 | fits | 150,741 | 199 | 0.396 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 303,522 | 3.035 | 20 | 20 | fits | 151,232 | 181 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 538,194 | 5.382 | 20 | 20 | fits | 84,767 | 41 | 0.750 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 146,434 | 1.464 | 20 | 24 | fits | 146,620 | 146 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 306,172 | 3.062 | 20 | 24 | fits | 151,232 | 181 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 306,106 | 3.061 | 20 | 50 | fits | 151,232 | 181 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 456,451 | 4.565 | 20 | 50 | fits | 150,741 | 199 | 0.396 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 541,152 | 5.412 | 20 | 20 | fits | 84,767 | 41 | 0.750 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 953,293 | 9.533 | 20 | 20 | fits | 85,527 | 39 | 0.689 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 28,049 | 0.280 | 20 | 20 | fits | 36,526 | 19 | 0.816 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 302,598 | 3.026 | 20 | 200 | fits | 151,232 | 181 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 52,447 | 0.524 | 20 | 200 | fits | 36,526 | 19 | 0.816 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 303,522 | 3.035 | 20 | 20 | fits | 151,232 | 181 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 534,189 | 5.342 | 20 | 20 | fits | 83,179 | 35 | 0.775 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 146,434 | 1.464 | 20 | 24 | fits | 146,620 | 146 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 306,172 | 3.062 | 20 | 24 | fits | 151,232 | 181 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 306,106 | 3.061 | 20 | 50 | fits | 151,232 | 181 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 454,034 | 4.540 | 20 | 50 | fits | 148,324 | 200 | 0.360 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 537,147 | 5.371 | 20 | 20 | fits | 83,179 | 35 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 928,139 | 9.281 | 20 | 20 | fits | 75,515 | 35 | 0.683 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,359,667 | 63.597 | 20 | 20 | MISS ceiling | 25,341 | 13 | 0.667 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,384,933 | 63.849 | 20 | 20 | MISS ceiling | 25,342 | 13 | 0.634 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,410,202 | 64.102 | 20 | 20 | MISS ceiling | 25,326 | 13 | 0.634 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,435,383 | 64.354 | 20 | 20 | MISS ceiling | 25,257 | 13 | 0.642 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,465,771 | 64.658 | 20 | 20 | MISS ceiling | 28,681 | 18 | 0.743 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 169,043 | 1.690 | 20 | 200 | fits | 152,271 | 173 | 0.473 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 304,091 | 3.041 | 20 | 200 | fits | 135,664 | 210 | 0.351 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 164,721 | 1.647 | 20 | 20 | fits | 152,271 | 173 | 0.473 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,239,900 | 62.399 | 20 | 20 | MISS ceiling | 39,863 | 15 | 0.761 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 168,361 | 1.684 | 20 | 24 | fits | 152,271 | 173 | 0.473 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,203,523 | 62.035 | 20 | 24 | MISS ceiling | 156,693 | 106 | 0.438 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 167,305 | 1.673 | 20 | 50 | fits | 152,271 | 173 | 0.473 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 302,573 | 3.026 | 20 | 50 | fits | 135,664 | 210 | 0.351 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 385,704 | 3.857 | 20 | 20 | fits | 83,197 | 28 | 0.751 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 732,497 | 7.325 | 20 | 20 | fits | 87,632 | 36 | 0.592 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 8,028 | 0.080 | 20 | 20 | fits | 31,182 | 14 (29) | 0.791 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 11,291 | 0.113 | 20 | 20 | fits | 35,281 | 19 (35) | 0.805 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 23,896 | 0.239 | 20 | 20 | fits | 37,944 | 21 (12) | 0.826 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 13,927 | 0.139 | 20 | 50 | fits | 35,008 | 43 | 0.740 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 25,670 | 0.257 | 20 | 50 | fits | 31,104 | 35 | 0.725 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 21,276 | 0.213 | 20 | 50 | fits | 30,945 | 35 | 0.719 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 27,495 | 0.275 | 20 | 50 | fits | 39,358 | 67 | 0.630 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 29,447 | 0.294 | 20 | 50 | fits | 39,358 | 67 | 0.630 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 11,855 | 0.119 | 20 | 50 | fits | 29,725 | 30 | 0.661 |
| LINK_UP | `adp.link_up.if0` | 3,068 | 0.031 | 20 | 200 | fits | 35,008 | 43 (11) | 0.740 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,642 | 0.186 | 20 | 200 | fits | 27,794 | 23 (39) | 0.755 |
| LINK_DOWN | `adp.link_down.if0` | 2,506 | 0.025 | 20 | 200 | fits | 32,157 | 23 (9) | 0.792 |
| LINK_UP | `adp.link_up.if0` | 3,068 | 0.031 | 20 | 200 | fits | 35,008 | 43 (11) | 0.740 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,642 | 0.186 | 20 | 200 | fits | 27,794 | 23 (39) | 0.755 |
| GM_CHANGE | `adp.gm_change.if0` | 2,555 | 0.026 | 20 | 200 | fits | 21,956 | 17 (11) | 0.772 |
| LINK_UP | `adp.link_up.if0` | 3,068 | 0.031 | 20 | 200 | fits | 35,008 | 43 (11) | 0.740 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,642 | 0.186 | 20 | 200 | fits | 27,794 | 23 (39) | 0.755 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 5,336 | 0.053 | 20 | 200 | fits | 21,503 | 16 (31) | 0.663 |
| LINK_UP | `adp.link_up.if0` | 3,068 | 0.031 | 20 | 200 | fits | 35,008 | 43 (11) | 0.740 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,642 | 0.186 | 20 | 200 | fits | 27,794 | 23 (39) | 0.755 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 5,336 | 0.053 | 20 | 200 | fits | 21,503 | 16 (31) | 0.663 |
| set_name | `aecp_fanout.set_name.if0` | 59,481 | 0.595 | 20 | 24 | fits | 62,972 | 87 | 0.582 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 57,871 | 0.579 | 20 | 24 | fits | 57,980 | 77 | 0.605 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 51,953 | 0.520 | 20 | 24 | fits | 52,680 | 78 | 0.556 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 41,276 | 0.413 | 20 | 24 | fits | 53,551 | 77 | 0.564 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 51,227 | 0.512 | 20 | 24 | fits | 54,932 | 67 | 0.586 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 51,833 | 0.518 | 20 | 24 | fits | 52,965 | 77 | 0.561 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 55,541 | 0.555 | 20 | 24 | fits | 52,214 | 78 | 0.552 |
| BIND_RX | `acmp.bind_rx.if0` | 20,618 | 0.206 | 20 | 20 | fits | 48,316 | 26 (77) | 0.798 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 11,859 | 0.119 | 20 | 20 | fits | 37,350 | 19 (32) | 0.839 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 12,038 | 0.120 | 20 | 20 | fits | 32,142 | 16 (47) | 0.789 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 17,178 | 0.172 | 20 | 20 | fits | 45,362 | 18 (50) | 0.847 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 12,326 | 0.123 | 20 | 20 | fits | 32,158 | 17 (48) | 0.769 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 10,730 | 0.107 | 20 | 20 | fits | 30,943 | 16 (48) | 0.741 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 17,226 | 0.172 | 20 | 20 | fits | 39,436 | 24 (48) | 0.762 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 11,182 | 0.112 | 20 | 20 | fits | 30,242 | 16 (48) | 0.741 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 25,748 | 0.257 | 20 | 24 | fits | 32,251 | 20 | 0.782 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 15,495 | 0.155 | 20 | 24 | fits | 36,214 | 20 | 0.705 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 29,165 | 0.292 | 20 | 24 | fits | 32,479 | 20 | 0.731 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 12,329 | 0.123 | 20 | 24 | fits | 32,161 | 20 | 0.731 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 12,639 | 0.126 | 20 | 24 | fits | 32,774 | 20 | 0.728 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 29,855 | 0.299 | 20 | 24 | fits | 33,319 | 20 | 0.728 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 12,803 | 0.128 | 20 | 24 | fits | 32,962 | 20 | 0.734 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 28,700 | 0.287 | 20 | 24 | fits | 32,055 | 20 | 0.738 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 12,930 | 0.129 | 20 | 24 | fits | 32,945 | 20 | 0.754 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 17,185 | 0.172 | 20 | 24 | fits | 37,205 | 21 | 0.658 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 28,633 | 0.286 | 20 | 24 | fits | 32,018 | 20 | 0.765 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 12,312 | 0.123 | 20 | 24 | fits | 32,030 | 20 | 0.772 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 28,532 | 0.285 | 20 | 24 | fits | 31,972 | 20 | 0.728 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 13,241 | 0.132 | 20 | 24 | fits | 33,286 | 20 | 0.741 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 12,748 | 0.127 | 20 | 24 | fits | 32,695 | 20 | 0.740 |
| get_configuration | `aecp.get_configuration.if0` | 26,698 | 0.267 | 20 | 24 | fits | 29,640 | 20 | 0.747 |
| entity_available | `aecp.entity_available.if0` | 10,568 | 0.106 | 20 | 24 | fits | 29,988 | 20 | 0.747 |
| get_name | `aecp.get_name.if0` | 28,775 | 0.288 | 20 | 24 | fits | 31,814 | 20 | 0.747 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 29,854 | 0.299 | 20 | 24 | fits | 33,209 | 27 | 0.723 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 21,728 | 0.217 | 20 | 24 | fits | 33,658 | 29 | 0.760 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 26,744 | 0.267 | 20 | 24 | fits | 29,612 | 20 | 0.748 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 9,834 | 0.098 | 20 | 24 | fits | 29,224 | 20 | 0.740 |
| set_name | `aecp.set_name.if0` | 19,886 | 0.199 | 20 | 24 | fits | 55,615 | 47 | 0.769 |
| lock_entity | `aecp.lock_entity.if0` | 32,790 | 0.328 | 20 | 24 | fits | 41,114 | 33 | 0.783 |
| unlock_entity | `aecp.unlock_entity.if0` | 17,036 | 0.170 | 20 | 24 | fits | 40,535 | 32 | 0.783 |
| LINK_UP | `fixture.link_up.if0` | 3,068 | 0.031 | 20 | 200 | fits | 35,008 | 43 (11) | 0.740 |
| malformed MRPDU discard | `fixture.malformed.if0` | 25,287 | 0.253 | 20 | 20 | fits | 25,353 | 12 | 0.755 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 36,642 | 0.366 | 20 | 24 | fits | 52,384 | 41 | 0.786 |
| LINK_DOWN | `fixture.link_down.if0` | 2,693 | 0.027 | 20 | 200 | fits | 33,237 | 23 (9) | 0.800 |
| BIND_RX | `fixture.bind_rx.if0` | 22,115 | 0.221 | 20 | 20 | fits | 48,413 | 26 (77) | 0.804 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 33,694 | 0.337 | 20 | 20 | fits | 49,199 | 35 (35) | 0.784 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 7,789 | 0.078 | 20 | 20 | fits | 32,572 | 13 (29) | 0.818 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 86,619 | 0.866 | 20 | 200 | fits | 86,723 | 51 | 0.760 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 86,619 | 0.866 | 20 | 200 | fits | 86,723 | 51 | 0.760 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 86,345 | 0.863 | 20 | 20 | fits | 86,723 | 51 | 0.760 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 86,345 | 0.863 | 20 | 20 | fits | 86,723 | 51 | 0.760 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 86,553 | 0.866 | 20 | 24 | fits | 86,723 | 51 | 0.760 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 86,553 | 0.866 | 20 | 24 | fits | 86,723 | 51 | 0.760 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 86,487 | 0.865 | 20 | 50 | fits | 86,723 | 51 | 0.760 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 86,487 | 0.865 | 20 | 50 | fits | 86,723 | 51 | 0.760 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 86,421 | 0.864 | 20 | 20 | fits | 86,723 | 51 | 0.760 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 86,421 | 0.864 | 20 | 20 | fits | 86,723 | 51 | 0.760 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
