### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 87 paths and 7 of 963 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.193 (0.443) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.087 (0.259) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.092 (0.312) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.093 (0.470) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.102 (0.274) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.101 (0.274) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.093 (0.271) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.105 (0.277) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.107 (0.342) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.298 (0.693) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.230 (0.645) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.213 (0.676) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.210 (0.615) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.140 (0.591) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.139 (0.533) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.158 (0.424) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.042 (0.186) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.018 (0.172) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.020 (0.311) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.020 (0.326) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.125 (0.302) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.149 (0.493) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.224 (0.574) | fits | 0 aecp | 1 | 0 |
| get_as_path, refused ENTITY_MISBEHAVING | 0 | `aecp.get_as_path.if0` (aecp) | 0.121 (0.469) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.220 (0.578) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.192 (0.556) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.264 (0.625) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.214 (0.570) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR held for a token (#917) | 0 | `aecp.held.read_descriptor.if0` (aecp-held) | 5.235 (5.595) | fits | 16 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.241 (0.684) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.184 (0.537) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.282 (0.642) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.216 (0.573) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.207 (0.561) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.246 (0.603) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.296 (0.657) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.207 (0.563) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.242 (0.599) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.246 (0.602) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.208 (0.563) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.252 (0.609) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.236 (0.469) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.249 (0.608) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.217 (0.574) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.246 (0.602) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.181 (0.538) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.318 (0.780) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.234 (0.592) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.250 (0.650) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.510 (0.826) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.497 (0.890) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.519 (0.830) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.559 (0.922) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.479 (0.815) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.466 (0.788) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.535 (4.935) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-1.adp_available.if0` (backlog-adp@blank-1) | 4.807 (6.328) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.231 (0.637) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.627 (2.090) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.132 (63.364) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.000 (64.235) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.327 (0.470) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-flight.held.acmp.if0` (save-flight) | 3.054 | fits | 11 acmp | 4 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-flight.held.adp.if0` (save-flight) | 3.406 | fits | 7 adp | 4 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-flight.held.aecp.if0` (save-flight) | 3.831 | fits | 14 aecp | 4 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 2.623 | fits | 6 maap | 4 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.381 | fits | 31 srp | 4 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.257 (0.626) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.131 (0.284) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.145 (0.326) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.236 (0.626) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.243 (0.590) | fits | 0 events | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-burst.mrpdu.periodic.if0` (save-burst) | 3.128 | fits | 0 srp | 10 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.185 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.106 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.228 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-7.service.adp.last.if0` (backlog-adp@verify-aged2-7) | 5.464 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 2.767 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.784 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.211 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-7.service.maap.last.if0` (backlog-adp@verify-aged2-7) | 5.501 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-5.service.srp.first.if0` (backlog-adp@program-aged2-5) | 6.862 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-5.service.srp.last.if0` (backlog-adp@program-aged2-5) | 10.015 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.766 (0.817) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.431 (0.432) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.234 (0.234) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.804 (0.883) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 14.175 | 10 | 152,404 (1.524) | yes | - |
| backlog-adp@blank-1 | 0 | 13.104 | 10 | 151,958 (1.520) | yes | - |
| backlog-adp@blank-2 | 0 | 12.979 | 10 | 151,958 (1.520) | yes | - |
| backlog-adp@blank-3 | 0 | 12.854 | 10 | 151,958 (1.520) | yes | - |
| backlog-adp@blank-4 | 0 | 12.729 | 10 | 151,958 (1.520) | yes | - |
| backlog-adp@blank-5 | 0 | 12.604 | 10 | 151,958 (1.520) | yes | - |
| backlog-adp@blank-6 | 0 | 12.479 | 10 | 151,958 (1.520) | yes | - |
| backlog-adp@blank-7 | 0 | 12.354 | 10 | 151,958 (1.520) | yes | - |
| backlog-adp@program-0 | 0 | 13.676 | 11 | 156,817 (1.568) | yes | - |
| backlog-adp@program-1 | 1 | 13.284 | 10 | 151,560 (1.516) | yes | - |
| backlog-adp@program-2 | 0 | 13.103 | 11 | 152,218 (1.522) | yes | - |
| backlog-adp@program-3 | 0 | 11.729 | 10 | 153,739 (1.537) | yes | - |
| backlog-adp@program-4 | 0 | 12.624 | 10 | 153,640 (1.536) | yes | - |
| backlog-adp@program-5 | 0 | 12.374 | 10 | 153,640 (1.536) | yes | - |
| backlog-adp@program-6 | 0 | 12.124 | 10 | 153,640 (1.536) | yes | - |
| backlog-adp@program-7 | 0 | 11.867 | 10 | 153,694 (1.537) | yes | - |
| backlog-adp@verify-0 | 0 | 12.167 | 9 | 153,643 (1.536) | yes | - |
| backlog-adp@verify-1 | 0 | 12.960 | 10 | 152,068 (1.521) | yes | - |
| backlog-adp@verify-2 | 0 | 12.835 | 10 | 152,068 (1.521) | yes | - |
| backlog-adp@verify-3 | 0 | 12.710 | 10 | 152,068 (1.521) | yes | - |
| backlog-adp@verify-4 | 0 | 12.585 | 10 | 152,068 (1.521) | yes | - |
| backlog-adp@verify-5 | 1 | 12.152 | 9 | 151,746 (1.517) | yes | - |
| backlog-adp@verify-6 | 1 | 12.152 | 9 | 151,746 (1.517) | yes | - |
| backlog-adp@verify-7 | 1 | 12.152 | 9 | 151,746 (1.517) | yes | - |
| backlog-adp@blank-aged2-0 | 1 | 12.920 | 8 | 152,519 (1.525) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 11.802 | 8 | 151,781 (1.518) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 14.753 | 10 | 151,801 (1.518) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 13.958 | 10 | 153,068 (1.531) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 12.944 | 10 | 153,567 (1.536) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 12.789 | 8 | 151,863 (1.519) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 12.716 | 8 | 151,706 (1.517) | yes | - |
| backlog-adp@blank-aged2-7 | 1 | 13.761 | 8 | 150,955 (1.510) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 12.979 | 9 | 151,863 (1.519) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 11.857 | 7 | 152,601 (1.526) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 11.949 | 8 | 151,863 (1.519) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 11.865 | 8 | 151,706 (1.517) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 14.103 | 10 | 152,040 (1.520) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 12.197 | 10 | 153,665 (1.537) | yes | - |
| backlog-adp@blank-aged1-6 | 1 | 11.882 | 7 | 150,907 (1.509) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 13.946 | 9 | 150,719 (1.507) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.727 | 10 | 153,521 (1.535) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 11.695 | 10 | 153,307 (1.533) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 11.326 | 8 | 151,550 (1.516) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 11.425 | 8 | 151,707 (1.517) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 11.337 | 8 | 151,550 (1.516) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 11.452 | 8 | 151,707 (1.517) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 14.228 | 11 | 151,946 (1.519) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 12.814 | 10 | 157,331 (1.573) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 11.663 | 9 | 151,707 (1.517) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 12.693 | 10 | 151,727 (1.517) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 11.609 | 10 | 153,542 (1.535) | yes | - |
| backlog-adp@program-aged1-3 | 1 | 11.249 | 7 | 152,794 (1.528) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 11.338 | 8 | 150,096 (1.501) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 11.273 | 8 | 151,899 (1.519) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 11.386 | 8 | 150,096 (1.501) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 11.323 | 8 | 151,149 (1.511) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 12.939 | 8 | 152,737 (1.527) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 13.943 | 10 | 151,794 (1.518) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 12.799 | 9 | 153,595 (1.536) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 12.755 | 8 | 151,727 (1.517) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 12.679 | 8 | 150,081 (1.501) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 12.796 | 8 | 151,727 (1.517) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 12.711 | 8 | 150,081 (1.501) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 15.154 | 11 | 158,156 (1.582) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 12.997 | 9 | 151,727 (1.517) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 12.011 | 8 | 151,952 (1.520) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 14.097 | 10 | 151,904 (1.519) | yes | - |
| backlog-adp@verify-aged1-3 | 1 | 14.028 | 9 | 151,334 (1.513) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 13.168 | 10 | 153,484 (1.535) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 11.884 | 7 | 152,512 (1.525) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 12.015 | 8 | 151,842 (1.518) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 13.959 | 9 | 157,731 (1.577) | yes | - |
| backlog | 0 | 6.077 | 7 | 153,873 (1.539) | yes | - |
| backlog-adp | 0 | 9.637 | 8 | 151,800 (1.518) | yes | - |
| backlog-adp-refill | 0 | 40.969 | 22 | 151,800 (1.518) | yes | - |
| backlog-owed | 0 | 65.103 | 23 | 137,967 (1.380) | yes | - |
| fixture | 0 | 1.437 | 2 | 91,404 (0.914) | yes | - |

Composed maximum over the 4 backlog windows: 153,873 CPU cycles (1.539 ms), backlog.
Over the windows that released their whole load only: 153,873 (1.539 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 142683 | 0 | 50,218 (0.502) | fits |
| save-burst | 2910 | 0 | 156,922 (1.569) | fits |
| save-held | 3062 | 0 | 163,480 (1.635) | fits |
| save-starved | 67550 | 0 | 163,480 (1.635) | fits |
| save-flight | 2578 | 0 | 163,480 (1.635) | fits |
| acmp-notk | 3604 | 0 | 111,201 (1.112) | fits |
| backlog-adp@blank-0 | 472 | 0 | 152,404 (1.524) | fits |
| backlog-adp@blank-1 | 472 | 0 | 151,958 (1.520) | fits |
| backlog-adp@blank-2 | 472 | 0 | 151,958 (1.520) | fits |
| backlog-adp@blank-3 | 472 | 0 | 151,958 (1.520) | fits |
| backlog-adp@blank-4 | 472 | 0 | 151,958 (1.520) | fits |
| backlog-adp@blank-5 | 472 | 0 | 151,958 (1.520) | fits |
| backlog-adp@blank-6 | 472 | 0 | 151,958 (1.520) | fits |
| backlog-adp@blank-7 | 472 | 0 | 151,958 (1.520) | fits |
| backlog-adp@program-0 | 507 | 0 | 156,817 (1.568) | fits |
| backlog-adp@program-1 | 507 | 0 | 153,283 (1.533) | fits |
| backlog-adp@program-2 | 508 | 0 | 152,218 (1.522) | fits |
| backlog-adp@program-3 | 507 | 0 | 153,739 (1.537) | fits |
| backlog-adp@program-4 | 507 | 0 | 153,640 (1.536) | fits |
| backlog-adp@program-5 | 507 | 0 | 153,640 (1.536) | fits |
| backlog-adp@program-6 | 507 | 0 | 153,640 (1.536) | fits |
| backlog-adp@program-7 | 507 | 0 | 153,694 (1.537) | fits |
| backlog-adp@verify-0 | 527 | 0 | 153,643 (1.536) | fits |
| backlog-adp@verify-1 | 527 | 0 | 152,068 (1.521) | fits |
| backlog-adp@verify-2 | 527 | 0 | 152,068 (1.521) | fits |
| backlog-adp@verify-3 | 527 | 0 | 152,068 (1.521) | fits |
| backlog-adp@verify-4 | 527 | 0 | 152,068 (1.521) | fits |
| backlog-adp@verify-5 | 527 | 0 | 151,746 (1.517) | fits |
| backlog-adp@verify-6 | 527 | 0 | 151,746 (1.517) | fits |
| backlog-adp@verify-7 | 527 | 0 | 151,746 (1.517) | fits |
| backlog-adp@blank-aged2-0 | 745 | 0 | 152,519 (1.525) | fits |
| backlog-adp@blank-aged2-1 | 752 | 0 | 151,781 (1.518) | fits |
| backlog-adp@blank-aged2-2 | 761 | 0 | 151,801 (1.518) | fits |
| backlog-adp@blank-aged2-3 | 769 | 0 | 153,068 (1.531) | fits |
| backlog-adp@blank-aged2-4 | 776 | 0 | 153,567 (1.536) | fits |
| backlog-adp@blank-aged2-5 | 782 | 0 | 151,863 (1.519) | fits |
| backlog-adp@blank-aged2-6 | 789 | 0 | 151,706 (1.517) | fits |
| backlog-adp@blank-aged2-7 | 797 | 0 | 150,955 (1.510) | fits |
| backlog-adp@blank-aged1-0 | 686 | 0 | 151,863 (1.519) | fits |
| backlog-adp@blank-aged1-1 | 692 | 0 | 152,601 (1.526) | fits |
| backlog-adp@blank-aged1-2 | 700 | 0 | 151,863 (1.519) | fits |
| backlog-adp@blank-aged1-3 | 707 | 0 | 151,706 (1.517) | fits |
| backlog-adp@blank-aged1-4 | 717 | 0 | 152,040 (1.520) | fits |
| backlog-adp@blank-aged1-5 | 724 | 0 | 153,665 (1.537) | fits |
| backlog-adp@blank-aged1-6 | 730 | 0 | 150,907 (1.509) | fits |
| backlog-adp@blank-aged1-7 | 738 | 0 | 150,719 (1.507) | fits |
| backlog-adp@program-aged2-0 | 759 | 0 | 153,521 (1.535) | fits |
| backlog-adp@program-aged2-1 | 767 | 0 | 153,307 (1.533) | fits |
| backlog-adp@program-aged2-2 | 772 | 0 | 151,550 (1.516) | fits |
| backlog-adp@program-aged2-3 | 780 | 0 | 151,707 (1.517) | fits |
| backlog-adp@program-aged2-4 | 787 | 0 | 151,550 (1.516) | fits |
| backlog-adp@program-aged2-5 | 795 | 0 | 151,707 (1.517) | fits |
| backlog-adp@program-aged2-6 | 805 | 0 | 151,946 (1.519) | fits |
| backlog-adp@program-aged2-7 | 811 | 0 | 157,331 (1.573) | fits |
| backlog-adp@program-aged1-0 | 699 | 0 | 151,707 (1.517) | fits |
| backlog-adp@program-aged1-1 | 707 | 0 | 151,727 (1.517) | fits |
| backlog-adp@program-aged1-2 | 715 | 0 | 153,542 (1.535) | fits |
| backlog-adp@program-aged1-3 | 720 | 0 | 152,794 (1.528) | fits |
| backlog-adp@program-aged1-4 | 728 | 0 | 150,096 (1.501) | fits |
| backlog-adp@program-aged1-5 | 735 | 0 | 151,899 (1.519) | fits |
| backlog-adp@program-aged1-6 | 743 | 0 | 150,096 (1.501) | fits |
| backlog-adp@program-aged1-7 | 750 | 0 | 151,149 (1.511) | fits |
| backlog-adp@verify-aged2-0 | 795 | 0 | 152,737 (1.527) | fits |
| backlog-adp@verify-aged2-1 | 804 | 0 | 151,794 (1.518) | fits |
| backlog-adp@verify-aged2-2 | 810 | 0 | 153,595 (1.536) | fits |
| backlog-adp@verify-aged2-3 | 817 | 0 | 151,727 (1.517) | fits |
| backlog-adp@verify-aged2-4 | 824 | 0 | 150,081 (1.501) | fits |
| backlog-adp@verify-aged2-5 | 832 | 0 | 151,727 (1.517) | fits |
| backlog-adp@verify-aged2-6 | 839 | 0 | 150,081 (1.501) | fits |
| backlog-adp@verify-aged2-7 | 850 | 0 | 158,156 (1.582) | fits |
| backlog-adp@verify-aged1-0 | 736 | 0 | 151,727 (1.517) | fits |
| backlog-adp@verify-aged1-1 | 743 | 0 | 151,952 (1.520) | fits |
| backlog-adp@verify-aged1-2 | 752 | 0 | 151,904 (1.519) | fits |
| backlog-adp@verify-aged1-3 | 759 | 0 | 151,334 (1.513) | fits |
| backlog-adp@verify-aged1-4 | 767 | 0 | 153,484 (1.535) | fits |
| backlog-adp@verify-aged1-5 | 772 | 0 | 152,512 (1.525) | fits |
| backlog-adp@verify-aged1-6 | 780 | 0 | 151,842 (1.518) | fits |
| backlog-adp@verify-aged1-7 | 788 | 0 | 157,731 (1.577) | fits |
| adp-advertise | 598 | 0 | 35,393 (0.354) | fits |
| acmp-noresp | 2021 | 0 | 110,898 (1.109) | fits |
| save | 610 | 0 | 82,357 (0.824) | fits |
| srp | 290 | 0 | 44,021 (0.440) | fits |
| backlog | 286 | 0 | 153,873 (1.539) | fits |
| backlog-adp | 310 | 0 | 151,800 (1.518) | fits |
| backlog-adp-refill | 324 | 0 | 151,800 (1.518) | fits |
| backlog-owed | 309 | 0 | 158,051 (1.581) | fits |
| acmp-disc | 936 | 0 | 111,029 (1.110) | fits |
| maap | 184 | 0 | 35,393 (0.354) | fits |
| adp-link | 89 | 0 | 45,139 (0.451) | fits |
| adp-gm | 88 | 0 | 32,612 (0.326) | fits |
| adp-discover | 88 | 0 | 32,612 (0.326) | fits |
| control | 88 | 0 | 32,612 (0.326) | fits |
| aecp-fanout | 110 | 0 | 58,875 (0.589) | fits |
| acmp-cmd | 88 | 0 | 44,780 (0.448) | fits |
| aecp | 114 | 0 | 46,126 (0.461) | fits |
| aecp-held | 105 | 0 | 36,038 (0.360) | fits |
| datapath-events | 116 | 0 | 32,612 (0.326) | fits |
| fixture | 149 | 0 | 91,404 (0.914) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 9.009 (20) | 10.991 |
| backlog-adp@blank-aged2-1 | 2 | none | +9.181 ms, 76,632 (0.766 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 9.144 (20) | 10.856 |
| backlog-adp@blank-aged2-2 | 2 | +8.576 ms, 76,569 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 9.861 (20) | 10.139 |
| backlog-adp@blank-aged2-3 | 2 | +7.359 ms, 76,569 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 9.953 (20) | 10.047 |
| backlog-adp@blank-aged2-4 | 2 | +5.943 ms, 76,721 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 9.854 (20) | 10.146 |
| backlog-adp@blank-aged2-5 | 2 | +4.609 ms, 76,455 (0.765 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 9.992 (20) | 10.008 |
| backlog-adp@blank-aged2-6 | 2 | +4.536 ms, 76,455 (0.765 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 9.919 (20) | 10.081 |
| backlog-adp@blank-aged2-7 | 2 | +4.473 ms, 76,455 (0.765 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 9.848 (20) | 10.152 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 9.066 (20) | 10.934 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 9.057 (20) | 10.943 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 9.150 (20) | 10.850 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 9.064 (20) | 10.936 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 9.178 (20) | 10.822 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 9.099 (20) | 10.901 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 9.079 (20) | 10.921 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 9.121 (20) | 10.879 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 8.985 (20) | 11.015 |
| backlog-adp@program-aged2-1 | 2 | none | +9.177 ms, 80,928 (0.809 ms), issue | `backlog-adp@program-aged2-1.service.srp.last.if0` | 9.140 (20) | 10.860 |
| backlog-adp@program-aged2-2 | 2 | +8.446 ms, 80,929 (0.809 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 9.892 (20) | 10.108 |
| backlog-adp@program-aged2-3 | 2 | +7.236 ms, 80,865 (0.809 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 9.991 (20) | 10.009 |
| backlog-adp@program-aged2-4 | 2 | none | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 9.903 (20) | 10.097 |
| backlog-adp@program-aged2-5 | 2 | none | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 10.015 (20) | 9.985 |
| backlog-adp@program-aged2-6 | 2 | +4.682 ms, 80,737 (0.807 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 9.957 (20) | 10.043 |
| backlog-adp@program-aged2-7 | 2 | +3.159 ms, 80,457 (0.805 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 10.008 (20) | 9.992 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 9.068 (20) | 10.932 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 9.067 (20) | 10.933 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 9.131 (20) | 10.869 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 9.060 (20) | 10.940 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 9.153 (20) | 10.847 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 9.087 (20) | 10.913 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 9.199 (20) | 10.801 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 9.135 (20) | 10.865 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 8.987 (20) | 11.013 |
| backlog-adp@verify-aged2-1 | 2 | none | +9.180 ms, 77,467 (0.775 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 9.142 (20) | 10.858 |
| backlog-adp@verify-aged2-2 | 2 | +8.525 ms, 77,468 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 9.853 (20) | 10.147 |
| backlog-adp@verify-aged2-3 | 2 | +7.168 ms, 77,532 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 9.925 (20) | 10.075 |
| backlog-adp@verify-aged2-4 | 2 | +5.780 ms, 77,620 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 9.851 (20) | 10.149 |
| backlog-adp@verify-aged2-5 | 2 | +4.584 ms, 77,354 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 9.969 (20) | 10.031 |
| backlog-adp@verify-aged2-6 | 2 | none | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 9.882 (20) | 10.118 |
| backlog-adp@verify-aged2-7 | 2 | none | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 9.982 (20) | 10.018 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 9.048 (20) | 10.952 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 9.180 (20) | 10.820 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 9.126 (20) | 10.874 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 9.056 (20) | 10.944 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 9.118 (20) | 10.882 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 9.053 (20) | 10.947 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 9.186 (20) | 10.814 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 9.086 (20) | 10.914 |

Least margin over the aged windows: 9.985 ms, `backlog-adp@program-aged2-5.service.srp.last.if0` at 10.015 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 22829.665 | 22,870 | 382 | 2 | 31.301 | yes | within |
| save-held | 1332.902 | 12,470 | 382 | - | 39.623 | no | within |
| save-starved | 12447.796 | 12,470 | 382 | - | 34.532 | yes | within |
| save | 1292.450 | 12,470 | 382 | - | 99.517 | no | within |

Names from their response to durable (save_burst.py; #920, the ruling of #665 issuecomment-6899740728, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-burst | 107 | 1349.303 (0) | 5,000 | 7 | - | - | sequence 7, 0 missing | within |
| save-flight | 1 | 625.599 (0) | 5,000 | 2 | - | - | 59 steps (want 59), 24.818 ms | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1080 | 81,770 (0.818) | 78,516 (0.785) |
| save-burst | 4078 | 99,560 (0.996) | 78,333 (0.783) |
| save-held | 1911 | 96,707 (0.967) | 78,597 (0.786) |
| save-starved | 698 | 82,410 (0.824) | 78,675 (0.787) |
| save-flight | 2067 | 98,683 (0.987) | 78,269 (0.783) |
| acmp-notk | 1416 | 111,201 (1.112) | 78,388 (0.784) |
| backlog-adp@blank-0 | 383 | 94,164 (0.942) | 76,014 (0.760) |
| backlog-adp@blank-1 | 382 | 92,358 (0.924) | 76,048 (0.760) |
| backlog-adp@blank-2 | 382 | 92,358 (0.924) | 76,048 (0.760) |
| backlog-adp@blank-3 | 382 | 92,358 (0.924) | 76,048 (0.760) |
| backlog-adp@blank-4 | 382 | 92,358 (0.924) | 76,048 (0.760) |
| backlog-adp@blank-5 | 382 | 92,358 (0.924) | 76,048 (0.760) |
| backlog-adp@blank-6 | 382 | 92,358 (0.924) | 76,048 (0.760) |
| backlog-adp@blank-7 | 382 | 92,358 (0.924) | 76,048 (0.760) |
| backlog-adp@program-0 | 495 | 102,850 (1.028) | 78,164 (0.782) |
| backlog-adp@program-1 | 495 | 102,850 (1.028) | 78,164 (0.782) |
| backlog-adp@program-2 | 494 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@program-3 | 493 | 97,852 (0.979) | 78,821 (0.788) |
| backlog-adp@program-4 | 495 | 102,803 (1.028) | 78,246 (0.782) |
| backlog-adp@program-5 | 495 | 102,803 (1.028) | 78,246 (0.782) |
| backlog-adp@program-6 | 495 | 102,803 (1.028) | 78,246 (0.782) |
| backlog-adp@program-7 | 495 | 104,160 (1.042) | 78,795 (0.788) |
| backlog-adp@verify-0 | 597 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@verify-1 | 598 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@verify-2 | 598 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@verify-3 | 598 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@verify-4 | 598 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@verify-5 | 598 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@verify-6 | 598 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@verify-7 | 598 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@blank-aged2-0 | 380 | 93,223 (0.932) | 76,258 (0.763) |
| backlog-adp@blank-aged2-1 | 379 | 93,917 (0.939) | 75,856 (0.759) |
| backlog-adp@blank-aged2-2 | 382 | 98,775 (0.988) | 75,856 (0.759) |
| backlog-adp@blank-aged2-3 | 381 | 93,935 (0.939) | 75,899 (0.759) |
| backlog-adp@blank-aged2-4 | 380 | 91,952 (0.920) | 76,062 (0.761) |
| backlog-adp@blank-aged2-5 | 380 | 93,136 (0.931) | 76,123 (0.761) |
| backlog-adp@blank-aged2-6 | 380 | 93,088 (0.931) | 76,123 (0.761) |
| backlog-adp@blank-aged2-7 | 381 | 93,088 (0.931) | 76,123 (0.761) |
| backlog-adp@blank-aged1-0 | 380 | 93,450 (0.934) | 76,258 (0.763) |
| backlog-adp@blank-aged1-1 | 379 | 93,271 (0.933) | 76,258 (0.763) |
| backlog-adp@blank-aged1-2 | 379 | 93,223 (0.932) | 76,258 (0.763) |
| backlog-adp@blank-aged1-3 | 379 | 93,367 (0.934) | 76,258 (0.763) |
| backlog-adp@blank-aged1-4 | 381 | 94,159 (0.942) | 76,258 (0.763) |
| backlog-adp@blank-aged1-5 | 379 | 94,675 (0.947) | 76,114 (0.761) |
| backlog-adp@blank-aged1-6 | 379 | 93,518 (0.935) | 76,258 (0.763) |
| backlog-adp@blank-aged1-7 | 381 | 93,271 (0.933) | 76,258 (0.763) |
| backlog-adp@program-aged2-0 | 489 | 97,852 (0.979) | 78,797 (0.788) |
| backlog-adp@program-aged2-1 | 489 | 97,852 (0.979) | 78,685 (0.787) |
| backlog-adp@program-aged2-2 | 489 | 97,852 (0.979) | 78,685 (0.787) |
| backlog-adp@program-aged2-3 | 489 | 97,852 (0.979) | 78,685 (0.787) |
| backlog-adp@program-aged2-4 | 489 | 97,852 (0.979) | 78,856 (0.789) |
| backlog-adp@program-aged2-5 | 489 | 97,852 (0.979) | 78,766 (0.788) |
| backlog-adp@program-aged2-6 | 493 | 97,852 (0.979) | 78,618 (0.786) |
| backlog-adp@program-aged2-7 | 491 | 97,852 (0.979) | 78,344 (0.783) |
| backlog-adp@program-aged1-0 | 489 | 97,852 (0.979) | 78,797 (0.788) |
| backlog-adp@program-aged1-1 | 490 | 97,852 (0.979) | 78,797 (0.788) |
| backlog-adp@program-aged1-2 | 488 | 97,852 (0.979) | 78,746 (0.787) |
| backlog-adp@program-aged1-3 | 488 | 97,852 (0.979) | 78,797 (0.788) |
| backlog-adp@program-aged1-4 | 488 | 97,852 (0.979) | 78,797 (0.788) |
| backlog-adp@program-aged1-5 | 488 | 97,852 (0.979) | 78,797 (0.788) |
| backlog-adp@program-aged1-6 | 488 | 97,852 (0.979) | 78,797 (0.788) |
| backlog-adp@program-aged1-7 | 488 | 97,852 (0.979) | 78,797 (0.788) |
| backlog-adp@verify-aged2-0 | 598 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@verify-aged2-1 | 599 | 102,307 (1.023) | 78,096 (0.781) |
| backlog-adp@verify-aged2-2 | 598 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@verify-aged2-3 | 598 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@verify-aged2-4 | 598 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@verify-aged2-5 | 598 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@verify-aged2-6 | 598 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@verify-aged2-7 | 600 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@verify-aged1-0 | 598 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@verify-aged1-1 | 597 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@verify-aged1-2 | 599 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@verify-aged1-3 | 599 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@verify-aged1-4 | 598 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@verify-aged1-5 | 597 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@verify-aged1-6 | 597 | 97,852 (0.979) | 78,096 (0.781) |
| backlog-adp@verify-aged1-7 | 599 | 97,852 (0.979) | 78,096 (0.781) |
| adp-advertise | 577 | 25,318 (0.253) | 2,771 (0.028) |
| acmp-noresp | 966 | 110,898 (1.109) | 78,282 (0.783) |
| save | 938 | 95,651 (0.957) | 77,910 (0.779) |
| srp | 271 | 25,318 (0.253) | 2,771 (0.028) |
| backlog | 265 | 25,318 (0.253) | 2,771 (0.028) |
| backlog-adp | 271 | 25,318 (0.253) | 2,771 (0.028) |
| backlog-adp-refill | 274 | 25,318 (0.253) | 2,771 (0.028) |
| backlog-owed | 277 | 25,318 (0.253) | 2,888 (0.029) |
| acmp-disc | 657 | 111,029 (1.110) | 78,282 (0.783) |
| maap | 171 | 25,207 (0.252) | 2,771 (0.028) |
| adp-link | 79 | 25,207 (0.252) | 2,771 (0.028) |
| adp-gm | 79 | 25,207 (0.252) | 2,771 (0.028) |
| adp-discover | 79 | 25,207 (0.252) | 2,771 (0.028) |
| control | 79 | 25,207 (0.252) | 2,771 (0.028) |
| aecp-fanout | 79 | 25,207 (0.252) | 2,771 (0.028) |
| acmp-cmd | 66 | 25,207 (0.252) | 2,771 (0.028) |
| aecp | 80 | 25,207 (0.252) | 2,771 (0.028) |
| aecp-held | 94 | 25,207 (0.252) | 2,771 (0.028) |
| datapath-events | 70 | 25,207 (0.252) | 2,771 (0.028) |
| fixture | 54 | 18,679 (0.187) | 2,654 (0.027) |

Longest pass that carries a step: 111,201 CPU cycles (1.112 ms), acmp-notk; longest step: 78,856 (0.789 ms), backlog-adp@program-aged2-4.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-burst.held.adp.if0` | 274,939 | 2.749 | 20 | 200 | fits | 108,920 | 130 | 0.449 |
| ACMP record, every channel at its refill rate, the longest | `save-burst.held.acmp.if0` | 284,632 | 2.846 | 20 | 20 | fits | 61,343 | 51 | 0.286 |
| AECP record, every channel at its refill rate, the longest | `save-burst.held.aecp.if0` | 298,850 | 2.989 | 20 | 24 | fits | 146,302 | 151 | 0.606 |
| MAAP record, every channel at its refill rate, the longest | `save-burst.held.maap.if0` | 239,238 | 2.392 | 20 | 50 | fits | 146,302 | 151 | 0.606 |
| SRP record, every channel at its refill rate, the longest | `save-burst.held.srp.if0` | 730,946 | 7.309 | 20 | 20 | fits | 102,710 | 43 | 0.724 |
| an MRPDU its join timer owes, the longest | `save-burst.mrpdu.join.if0` | 51,549 | 0.515 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-burst.mrpdu.leaveall.if0` | 48,206 | 0.482 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-burst.mrpdu.periodic.if0` | 312,801 | 3.128 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 300,842 | 3.008 | 20 | 200 | fits | 138,302 | 129 | 0.543 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 303,940 | 3.039 | 20 | 20 | fits | 90,514 | 59 | 0.510 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 291,792 | 2.918 | 20 | 24 | fits | 64,818 | 51 | 0.471 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 241,230 | 2.412 | 20 | 50 | fits | 138,302 | 129 | 0.543 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 826,185 | 8.262 | 20 | 20 | fits | 71,470 | 30 | 0.730 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 54,866 | 0.549 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 53,047 | 0.530 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 242,167 | 2.422 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 303,622 | 3.036 | 20 | 200 | fits | 141,082 | 135 | 0.554 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 283,485 | 2.835 | 20 | 20 | fits | 141,082 | 135 | 0.554 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 307,487 | 3.075 | 20 | 24 | fits | 133,558 | 75 | 0.567 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 244,010 | 2.440 | 20 | 50 | fits | 141,082 | 135 | 0.554 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 838,129 | 8.381 | 20 | 20 | fits | 71,938 | 36 | 0.707 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 58,059 | 0.581 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 59,413 | 0.594 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 246,141 | 2.461 | 49 | 49 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 340,566 | 3.406 | 20 | 200 | fits | 137,536 | 101 | 0.473 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 305,401 | 3.054 | 20 | 20 | fits | 90,829 | 59 | 0.514 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 383,062 | 3.831 | 20 | 24 | fits | 132,231 | 63 | 0.588 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 262,307 | 2.623 | 20 | 50 | fits | 128,217 | 202 | 0.323 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 816,067 | 8.161 | 20 | 20 | fits | 60,568 | 26 | 0.753 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 102,082 | 1.021 | 49 | 49 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 13,986 | 0.140 | 20 | 20 | fits | 37,796 | 19 (14) | 0.876 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 396,500 | 3.965 | 20 | 20 | fits | 143,542 | 170 | 0.385 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 304,824 | 3.048 | 20 | 200 | fits | 152,404 | 218 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 457,827 | 4.578 | 20 | 200 | fits | 143,542 | 170 | 0.385 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 305,748 | 3.057 | 20 | 20 | fits | 152,404 | 218 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 458,531 | 4.585 | 20 | 20 | fits | 143,542 | 170 | 0.385 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 156,984 | 1.570 | 20 | 24 | fits | 150,963 | 164 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 308,398 | 3.084 | 20 | 24 | fits | 152,404 | 218 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 308,332 | 3.083 | 20 | 50 | fits | 152,404 | 218 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 461,555 | 4.616 | 20 | 50 | fits | 143,542 | 170 | 0.385 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 600,317 | 6.003 | 20 | 20 | fits | 138,828 | 50 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 925,190 | 9.252 | 20 | 20 | fits | 55,108 | 20 | 0.741 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 480,723 | 4.807 | 20 | 20 | fits | 148,435 | 172 | 0.350 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 392,617 | 3.926 | 20 | 200 | fits | 151,958 | 218 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 540,436 | 5.404 | 20 | 200 | fits | 148,435 | 172 | 0.350 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 393,541 | 3.935 | 20 | 20 | fits | 151,958 | 218 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 541,140 | 5.411 | 20 | 20 | fits | 148,435 | 172 | 0.350 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 236,162 | 2.362 | 20 | 24 | fits | 151,290 | 165 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 396,191 | 3.962 | 20 | 24 | fits | 151,958 | 218 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 396,125 | 3.961 | 20 | 50 | fits | 151,958 | 218 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 544,164 | 5.442 | 20 | 50 | fits | 148,435 | 172 | 0.350 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 681,290 | 6.813 | 20 | 20 | fits | 133,087 | 45 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 1,001,018 | 10.010 | 20 | 20 | fits | 55,214 | 21 | 0.736 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 468,223 | 4.682 | 20 | 20 | fits | 148,435 | 172 | 0.350 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 380,117 | 3.801 | 20 | 200 | fits | 151,958 | 218 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 527,936 | 5.279 | 20 | 200 | fits | 148,435 | 172 | 0.350 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 381,041 | 3.810 | 20 | 20 | fits | 151,958 | 218 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 528,640 | 5.286 | 20 | 20 | fits | 148,435 | 172 | 0.350 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 223,662 | 2.237 | 20 | 24 | fits | 151,290 | 165 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 383,691 | 3.837 | 20 | 24 | fits | 151,958 | 218 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 383,625 | 3.836 | 20 | 50 | fits | 151,958 | 218 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 531,664 | 5.317 | 20 | 50 | fits | 148,435 | 172 | 0.350 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 668,790 | 6.688 | 20 | 20 | fits | 133,087 | 45 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 988,518 | 9.885 | 20 | 20 | fits | 55,214 | 21 | 0.736 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 455,723 | 4.557 | 20 | 20 | fits | 148,435 | 172 | 0.350 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 367,617 | 3.676 | 20 | 200 | fits | 151,958 | 218 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 515,436 | 5.154 | 20 | 200 | fits | 148,435 | 172 | 0.350 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 368,541 | 3.685 | 20 | 20 | fits | 151,958 | 218 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 516,140 | 5.161 | 20 | 20 | fits | 148,435 | 172 | 0.350 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 211,162 | 2.112 | 20 | 24 | fits | 151,290 | 165 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 371,191 | 3.712 | 20 | 24 | fits | 151,958 | 218 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 371,125 | 3.711 | 20 | 50 | fits | 151,958 | 218 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 519,164 | 5.192 | 20 | 50 | fits | 148,435 | 172 | 0.350 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 656,290 | 6.563 | 20 | 20 | fits | 133,087 | 45 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 976,018 | 9.760 | 20 | 20 | fits | 55,214 | 21 | 0.736 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 443,223 | 4.432 | 20 | 20 | fits | 148,435 | 172 | 0.350 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 355,117 | 3.551 | 20 | 200 | fits | 151,958 | 218 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 502,936 | 5.029 | 20 | 200 | fits | 148,435 | 172 | 0.350 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 356,041 | 3.560 | 20 | 20 | fits | 151,958 | 218 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 503,640 | 5.036 | 20 | 20 | fits | 148,435 | 172 | 0.350 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 198,662 | 1.987 | 20 | 24 | fits | 151,290 | 165 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 358,691 | 3.587 | 20 | 24 | fits | 151,958 | 218 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 358,625 | 3.586 | 20 | 50 | fits | 151,958 | 218 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 506,664 | 5.067 | 20 | 50 | fits | 148,435 | 172 | 0.350 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 643,790 | 6.438 | 20 | 20 | fits | 133,087 | 45 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 963,518 | 9.635 | 20 | 20 | fits | 55,214 | 21 | 0.736 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 430,723 | 4.307 | 20 | 20 | fits | 148,435 | 172 | 0.350 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 342,617 | 3.426 | 20 | 200 | fits | 151,958 | 218 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 490,436 | 4.904 | 20 | 200 | fits | 148,435 | 172 | 0.350 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 343,541 | 3.435 | 20 | 20 | fits | 151,958 | 218 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 491,140 | 4.911 | 20 | 20 | fits | 148,435 | 172 | 0.350 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 186,162 | 1.862 | 20 | 24 | fits | 151,290 | 165 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 346,191 | 3.462 | 20 | 24 | fits | 151,958 | 218 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 346,125 | 3.461 | 20 | 50 | fits | 151,958 | 218 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 494,164 | 4.942 | 20 | 50 | fits | 148,435 | 172 | 0.350 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 631,290 | 6.313 | 20 | 20 | fits | 133,087 | 45 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 951,018 | 9.510 | 20 | 20 | fits | 55,214 | 21 | 0.736 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 418,223 | 4.182 | 20 | 20 | fits | 148,435 | 172 | 0.350 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 330,117 | 3.301 | 20 | 200 | fits | 151,958 | 218 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 477,936 | 4.779 | 20 | 200 | fits | 148,435 | 172 | 0.350 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 331,041 | 3.310 | 20 | 20 | fits | 151,958 | 218 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 478,640 | 4.786 | 20 | 20 | fits | 148,435 | 172 | 0.350 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 173,662 | 1.737 | 20 | 24 | fits | 151,290 | 165 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 333,691 | 3.337 | 20 | 24 | fits | 151,958 | 218 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 333,625 | 3.336 | 20 | 50 | fits | 151,958 | 218 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 481,664 | 4.817 | 20 | 50 | fits | 148,435 | 172 | 0.350 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 618,790 | 6.188 | 20 | 20 | fits | 133,087 | 45 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 938,518 | 9.385 | 20 | 20 | fits | 55,214 | 21 | 0.736 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 405,723 | 4.057 | 20 | 20 | fits | 148,435 | 172 | 0.350 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 317,617 | 3.176 | 20 | 200 | fits | 151,958 | 218 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 465,436 | 4.654 | 20 | 200 | fits | 148,435 | 172 | 0.350 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 318,541 | 3.185 | 20 | 20 | fits | 151,958 | 218 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 466,140 | 4.661 | 20 | 20 | fits | 148,435 | 172 | 0.350 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 161,162 | 1.612 | 20 | 24 | fits | 151,290 | 165 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 321,191 | 3.212 | 20 | 24 | fits | 151,958 | 218 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 321,125 | 3.211 | 20 | 50 | fits | 151,958 | 218 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 469,164 | 4.692 | 20 | 50 | fits | 148,435 | 172 | 0.350 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 606,290 | 6.063 | 20 | 20 | fits | 133,087 | 45 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 926,018 | 9.260 | 20 | 20 | fits | 55,214 | 21 | 0.736 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 431,859 | 4.319 | 20 | 20 | fits | 144,916 | 172 | 0.377 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 338,290 | 3.383 | 20 | 200 | fits | 156,817 | 219 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 492,175 | 4.922 | 20 | 200 | fits | 144,916 | 172 | 0.377 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 339,214 | 3.392 | 20 | 20 | fits | 156,817 | 219 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 492,879 | 4.929 | 20 | 20 | fits | 144,916 | 172 | 0.377 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 186,037 | 1.860 | 20 | 24 | fits | 151,308 | 164 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 341,864 | 3.419 | 20 | 24 | fits | 156,817 | 219 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 341,798 | 3.418 | 20 | 50 | fits | 156,817 | 219 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 495,903 | 4.959 | 20 | 50 | fits | 144,916 | 172 | 0.377 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 628,540 | 6.285 | 20 | 20 | fits | 132,703 | 44 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 943,601 | 9.436 | 20 | 20 | fits | 54,927 | 20 | 0.736 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 392,366 | 3.924 | 20 | 20 | fits | 144,875 | 172 | 0.376 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 298,750 | 2.987 | 20 | 200 | fits | 151,560 | 219 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 452,767 | 4.528 | 20 | 200 | fits | 144,875 | 172 | 0.376 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 299,674 | 2.997 | 20 | 20 | fits | 151,560 | 219 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 453,471 | 4.535 | 20 | 20 | fits | 144,875 | 172 | 0.376 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 151,754 | 1.518 | 20 | 24 | fits | 153,283 | 164 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 302,324 | 3.023 | 20 | 24 | fits | 151,560 | 219 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 302,258 | 3.023 | 20 | 50 | fits | 151,560 | 219 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 456,495 | 4.565 | 20 | 50 | fits | 144,875 | 172 | 0.376 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 589,306 | 5.893 | 20 | 20 | fits | 132,877 | 44 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 904,400 | 9.044 | 20 | 20 | fits | 54,927 | 20 | 0.736 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 386,939 | 3.869 | 20 | 20 | fits | 143,309 | 170 | 0.386 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 303,633 | 3.036 | 20 | 200 | fits | 152,218 | 218 | 0.376 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 456,001 | 4.560 | 20 | 200 | fits | 143,309 | 170 | 0.386 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 304,557 | 3.046 | 20 | 20 | fits | 152,218 | 218 | 0.376 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 456,705 | 4.567 | 20 | 20 | fits | 143,309 | 170 | 0.386 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 155,979 | 1.560 | 20 | 24 | fits | 150,717 | 164 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 307,207 | 3.072 | 20 | 24 | fits | 152,218 | 218 | 0.376 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 307,141 | 3.071 | 20 | 50 | fits | 152,218 | 218 | 0.376 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 459,729 | 4.597 | 20 | 50 | fits | 143,309 | 170 | 0.386 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 592,522 | 5.925 | 20 | 20 | fits | 132,859 | 44 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 907,635 | 9.076 | 20 | 20 | fits | 54,964 | 20 | 0.737 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 378,262 | 3.783 | 20 | 20 | fits | 138,011 | 163 | 0.317 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 309,745 | 3.097 | 20 | 200 | fits | 153,739 | 222 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 447,140 | 4.471 | 20 | 200 | fits | 138,011 | 163 | 0.317 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 310,669 | 3.107 | 20 | 20 | fits | 153,739 | 222 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 447,844 | 4.478 | 20 | 20 | fits | 138,011 | 163 | 0.317 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 151,802 | 1.518 | 20 | 24 | fits | 150,893 | 165 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 313,319 | 3.133 | 20 | 24 | fits | 153,739 | 222 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 313,253 | 3.133 | 20 | 50 | fits | 153,739 | 222 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 450,868 | 4.509 | 20 | 50 | fits | 138,011 | 163 | 0.317 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 583,814 | 5.838 | 20 | 20 | fits | 133,012 | 44 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 899,474 | 8.995 | 20 | 20 | fits | 55,106 | 20 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 448,914 | 4.489 | 20 | 20 | fits | 138,381 | 163 | 0.322 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 380,141 | 3.801 | 20 | 200 | fits | 153,640 | 222 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 517,906 | 5.179 | 20 | 200 | fits | 138,381 | 163 | 0.322 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 381,065 | 3.811 | 20 | 20 | fits | 153,640 | 222 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 518,610 | 5.186 | 20 | 20 | fits | 138,381 | 163 | 0.322 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 222,289 | 2.223 | 20 | 24 | fits | 150,928 | 165 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 383,715 | 3.837 | 20 | 24 | fits | 153,640 | 222 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 383,649 | 3.836 | 20 | 50 | fits | 153,640 | 222 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 521,634 | 5.216 | 20 | 50 | fits | 138,381 | 163 | 0.322 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 654,509 | 6.545 | 20 | 20 | fits | 132,941 | 44 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 975,651 | 9.757 | 20 | 20 | fits | 60,575 | 26 | 0.755 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 423,914 | 4.239 | 20 | 20 | fits | 138,381 | 163 | 0.322 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 355,141 | 3.551 | 20 | 200 | fits | 153,640 | 222 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 492,906 | 4.929 | 20 | 200 | fits | 138,381 | 163 | 0.322 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 356,065 | 3.561 | 20 | 20 | fits | 153,640 | 222 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 493,610 | 4.936 | 20 | 20 | fits | 138,381 | 163 | 0.322 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 197,289 | 1.973 | 20 | 24 | fits | 150,928 | 165 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 358,715 | 3.587 | 20 | 24 | fits | 153,640 | 222 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 358,649 | 3.586 | 20 | 50 | fits | 153,640 | 222 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 496,634 | 4.966 | 20 | 50 | fits | 138,381 | 163 | 0.322 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 629,509 | 6.295 | 20 | 20 | fits | 132,941 | 44 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 950,651 | 9.507 | 20 | 20 | fits | 60,575 | 26 | 0.755 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 398,914 | 3.989 | 20 | 20 | fits | 138,381 | 163 | 0.322 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 330,141 | 3.301 | 20 | 200 | fits | 153,640 | 222 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 467,906 | 4.679 | 20 | 200 | fits | 138,381 | 163 | 0.322 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 331,065 | 3.311 | 20 | 20 | fits | 153,640 | 222 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 468,610 | 4.686 | 20 | 20 | fits | 138,381 | 163 | 0.322 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 172,289 | 1.723 | 20 | 24 | fits | 150,928 | 165 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 333,715 | 3.337 | 20 | 24 | fits | 153,640 | 222 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 333,649 | 3.336 | 20 | 50 | fits | 153,640 | 222 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 471,634 | 4.716 | 20 | 50 | fits | 138,381 | 163 | 0.322 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 604,509 | 6.045 | 20 | 20 | fits | 132,941 | 44 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 925,651 | 9.257 | 20 | 20 | fits | 60,575 | 26 | 0.755 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 403,417 | 4.034 | 20 | 20 | fits | 138,140 | 163 | 0.319 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 326,455 | 3.265 | 20 | 200 | fits | 153,694 | 222 | 0.376 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 463,979 | 4.640 | 20 | 200 | fits | 138,140 | 163 | 0.319 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 327,379 | 3.274 | 20 | 20 | fits | 153,694 | 222 | 0.376 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 464,683 | 4.647 | 20 | 20 | fits | 138,140 | 163 | 0.319 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 168,608 | 1.686 | 20 | 24 | fits | 151,020 | 165 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 330,029 | 3.300 | 20 | 24 | fits | 153,694 | 222 | 0.376 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 329,963 | 3.300 | 20 | 50 | fits | 153,694 | 222 | 0.376 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 467,707 | 4.677 | 20 | 50 | fits | 138,140 | 163 | 0.319 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 600,514 | 6.005 | 20 | 20 | fits | 132,873 | 44 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 921,566 | 9.216 | 20 | 20 | fits | 60,575 | 26 | 0.755 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 385,975 | 3.860 | 20 | 20 | fits | 138,140 | 163 | 0.319 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 309,013 | 3.090 | 20 | 200 | fits | 153,643 | 222 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 446,537 | 4.465 | 20 | 200 | fits | 138,140 | 163 | 0.319 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 309,937 | 3.099 | 20 | 20 | fits | 153,643 | 222 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 447,241 | 4.472 | 20 | 20 | fits | 138,140 | 163 | 0.319 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 150,744 | 1.507 | 20 | 24 | fits | 150,976 | 165 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 312,587 | 3.126 | 20 | 24 | fits | 153,643 | 222 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 312,521 | 3.125 | 20 | 50 | fits | 153,643 | 222 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 450,265 | 4.503 | 20 | 50 | fits | 138,140 | 163 | 0.319 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 583,176 | 5.832 | 20 | 20 | fits | 132,977 | 44 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 904,450 | 9.044 | 20 | 20 | fits | 55,353 | 21 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 466,663 | 4.667 | 20 | 20 | fits | 139,650 | 166 | 0.310 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 387,083 | 3.871 | 20 | 200 | fits | 152,068 | 218 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 526,117 | 5.261 | 20 | 200 | fits | 139,650 | 166 | 0.310 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 388,007 | 3.880 | 20 | 20 | fits | 152,068 | 218 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 526,821 | 5.268 | 20 | 20 | fits | 139,650 | 166 | 0.310 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 230,389 | 2.304 | 20 | 24 | fits | 150,920 | 165 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 390,657 | 3.907 | 20 | 24 | fits | 152,068 | 218 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 390,591 | 3.906 | 20 | 50 | fits | 152,068 | 218 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 529,845 | 5.298 | 20 | 50 | fits | 139,650 | 166 | 0.310 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 668,019 | 6.680 | 20 | 20 | fits | 138,240 | 50 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 983,835 | 9.838 | 20 | 20 | fits | 55,353 | 21 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 454,163 | 4.542 | 20 | 20 | fits | 139,650 | 166 | 0.310 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 374,583 | 3.746 | 20 | 200 | fits | 152,068 | 218 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 513,617 | 5.136 | 20 | 200 | fits | 139,650 | 166 | 0.310 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 375,507 | 3.755 | 20 | 20 | fits | 152,068 | 218 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 514,321 | 5.143 | 20 | 20 | fits | 139,650 | 166 | 0.310 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 217,889 | 2.179 | 20 | 24 | fits | 150,920 | 165 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 378,157 | 3.782 | 20 | 24 | fits | 152,068 | 218 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 378,091 | 3.781 | 20 | 50 | fits | 152,068 | 218 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 517,345 | 5.173 | 20 | 50 | fits | 139,650 | 166 | 0.310 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 655,519 | 6.555 | 20 | 20 | fits | 138,240 | 50 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 971,335 | 9.713 | 20 | 20 | fits | 55,353 | 21 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 441,663 | 4.417 | 20 | 20 | fits | 139,650 | 166 | 0.310 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 362,083 | 3.621 | 20 | 200 | fits | 152,068 | 218 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 501,117 | 5.011 | 20 | 200 | fits | 139,650 | 166 | 0.310 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 363,007 | 3.630 | 20 | 20 | fits | 152,068 | 218 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 501,821 | 5.018 | 20 | 20 | fits | 139,650 | 166 | 0.310 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 205,389 | 2.054 | 20 | 24 | fits | 150,920 | 165 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 365,657 | 3.657 | 20 | 24 | fits | 152,068 | 218 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 365,591 | 3.656 | 20 | 50 | fits | 152,068 | 218 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 504,845 | 5.048 | 20 | 50 | fits | 139,650 | 166 | 0.310 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 643,019 | 6.430 | 20 | 20 | fits | 138,240 | 50 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 958,835 | 9.588 | 20 | 20 | fits | 55,353 | 21 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 429,163 | 4.292 | 20 | 20 | fits | 139,650 | 166 | 0.310 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 349,583 | 3.496 | 20 | 200 | fits | 152,068 | 218 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 488,617 | 4.886 | 20 | 200 | fits | 139,650 | 166 | 0.310 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 350,507 | 3.505 | 20 | 20 | fits | 152,068 | 218 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 489,321 | 4.893 | 20 | 20 | fits | 139,650 | 166 | 0.310 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 192,889 | 1.929 | 20 | 24 | fits | 150,920 | 165 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 353,157 | 3.532 | 20 | 24 | fits | 152,068 | 218 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 353,091 | 3.531 | 20 | 50 | fits | 152,068 | 218 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 492,345 | 4.923 | 20 | 50 | fits | 139,650 | 166 | 0.310 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 630,519 | 6.305 | 20 | 20 | fits | 138,240 | 50 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 946,335 | 9.463 | 20 | 20 | fits | 55,353 | 21 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 385,828 | 3.858 | 20 | 20 | fits | 139,650 | 166 | 0.310 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 306,248 | 3.062 | 20 | 200 | fits | 151,746 | 218 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 445,282 | 4.453 | 20 | 200 | fits | 139,650 | 166 | 0.310 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 307,172 | 3.072 | 20 | 20 | fits | 151,746 | 218 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 445,986 | 4.460 | 20 | 20 | fits | 139,650 | 166 | 0.310 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 149,876 | 1.499 | 20 | 24 | fits | 151,080 | 165 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 309,822 | 3.098 | 20 | 24 | fits | 151,746 | 218 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 309,756 | 3.098 | 20 | 50 | fits | 151,746 | 218 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 449,010 | 4.490 | 20 | 50 | fits | 139,650 | 166 | 0.310 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 587,169 | 5.872 | 20 | 20 | fits | 138,225 | 50 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 903,031 | 9.030 | 20 | 20 | fits | 55,353 | 21 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 385,828 | 3.858 | 20 | 20 | fits | 139,650 | 166 | 0.310 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 306,248 | 3.062 | 20 | 200 | fits | 151,746 | 218 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 445,282 | 4.453 | 20 | 200 | fits | 139,650 | 166 | 0.310 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 307,172 | 3.072 | 20 | 20 | fits | 151,746 | 218 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 445,986 | 4.460 | 20 | 20 | fits | 139,650 | 166 | 0.310 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 149,876 | 1.499 | 20 | 24 | fits | 151,080 | 165 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 309,822 | 3.098 | 20 | 24 | fits | 151,746 | 218 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 309,756 | 3.098 | 20 | 50 | fits | 151,746 | 218 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 449,010 | 4.490 | 20 | 50 | fits | 139,650 | 166 | 0.310 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 587,169 | 5.872 | 20 | 20 | fits | 138,225 | 50 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 903,031 | 9.030 | 20 | 20 | fits | 55,353 | 21 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 385,828 | 3.858 | 20 | 20 | fits | 139,650 | 166 | 0.310 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 306,248 | 3.062 | 20 | 200 | fits | 151,746 | 218 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 445,282 | 4.453 | 20 | 200 | fits | 139,650 | 166 | 0.310 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 307,172 | 3.072 | 20 | 20 | fits | 151,746 | 218 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 445,986 | 4.460 | 20 | 20 | fits | 139,650 | 166 | 0.310 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 149,876 | 1.499 | 20 | 24 | fits | 151,080 | 165 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 309,822 | 3.098 | 20 | 24 | fits | 151,746 | 218 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 309,756 | 3.098 | 20 | 50 | fits | 151,746 | 218 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 449,010 | 4.490 | 20 | 50 | fits | 139,650 | 166 | 0.310 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 587,169 | 5.872 | 20 | 20 | fits | 138,225 | 50 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 903,031 | 9.030 | 20 | 20 | fits | 55,353 | 21 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 373,043 | 3.730 | 20 | 20 | fits | 138,027 | 163 | 0.317 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 296,020 | 2.960 | 20 | 200 | fits | 152,519 | 222 | 0.365 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 433,431 | 4.334 | 20 | 200 | fits | 138,027 | 163 | 0.317 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 296,944 | 2.969 | 20 | 20 | fits | 152,519 | 222 | 0.365 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 434,135 | 4.341 | 20 | 20 | fits | 138,027 | 163 | 0.317 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 148,065 | 1.481 | 20 | 24 | fits | 149,401 | 161 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 299,594 | 2.996 | 20 | 24 | fits | 152,519 | 222 | 0.365 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 299,528 | 2.995 | 20 | 50 | fits | 152,519 | 222 | 0.365 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 437,159 | 4.372 | 20 | 50 | fits | 138,027 | 163 | 0.317 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 570,219 | 5.702 | 20 | 20 | fits | 133,126 | 45 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 900,871 | 9.009 | 20 | 20 | fits | 55,108 | 20 | 0.739 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 374,929 | 3.749 | 20 | 20 | fits | 138,166 | 164 | 0.319 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 306,351 | 3.064 | 20 | 200 | fits | 151,781 | 217 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 443,901 | 4.439 | 20 | 200 | fits | 138,166 | 164 | 0.319 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 307,275 | 3.073 | 20 | 20 | fits | 151,781 | 217 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 444,605 | 4.446 | 20 | 20 | fits | 138,166 | 164 | 0.319 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 159,134 | 1.591 | 20 | 24 | fits | 149,401 | 161 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 309,925 | 3.099 | 20 | 24 | fits | 151,781 | 217 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 309,859 | 3.099 | 20 | 50 | fits | 151,781 | 217 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 447,629 | 4.476 | 20 | 50 | fits | 138,166 | 164 | 0.319 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 593,914 | 5.939 | 20 | 20 | fits | 136,410 | 51 | 0.733 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 914,396 | 9.144 | 20 | 20 | fits | 60,198 | 26 | 0.747 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 390,412 | 3.904 | 20 | 20 | fits | 143,179 | 170 | 0.381 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 299,531 | 2.995 | 20 | 200 | fits | 151,801 | 218 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 451,740 | 4.517 | 20 | 200 | fits | 143,179 | 170 | 0.381 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 300,455 | 3.005 | 20 | 20 | fits | 151,801 | 218 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 452,444 | 4.524 | 20 | 20 | fits | 143,179 | 170 | 0.381 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 152,294 | 1.523 | 20 | 24 | fits | 149,401 | 161 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 303,105 | 3.031 | 20 | 24 | fits | 151,801 | 218 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 303,039 | 3.030 | 20 | 50 | fits | 151,801 | 218 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 455,468 | 4.555 | 20 | 50 | fits | 143,179 | 170 | 0.381 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 588,300 | 5.883 | 20 | 20 | fits | 132,898 | 44 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 986,140 | 9.861 | 20 | 20 | fits | 55,758 | 21 | 0.748 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 390,618 | 3.906 | 20 | 20 | fits | 140,493 | 163 | 0.371 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 310,838 | 3.108 | 20 | 200 | fits | 153,068 | 223 | 0.365 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 460,312 | 4.603 | 20 | 200 | fits | 140,493 | 163 | 0.371 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 311,762 | 3.118 | 20 | 20 | fits | 153,068 | 223 | 0.365 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 461,016 | 4.610 | 20 | 20 | fits | 140,493 | 163 | 0.371 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 162,334 | 1.623 | 20 | 24 | fits | 149,401 | 161 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 314,412 | 3.144 | 20 | 24 | fits | 153,068 | 223 | 0.365 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 314,346 | 3.143 | 20 | 50 | fits | 153,068 | 223 | 0.365 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 464,040 | 4.640 | 20 | 50 | fits | 140,493 | 163 | 0.371 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 596,935 | 5.969 | 20 | 20 | fits | 132,961 | 44 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 995,250 | 9.953 | 20 | 20 | fits | 55,013 | 20 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 390,342 | 3.903 | 20 | 20 | fits | 138,139 | 163 | 0.319 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 313,381 | 3.134 | 20 | 200 | fits | 153,567 | 222 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 450,904 | 4.509 | 20 | 200 | fits | 138,139 | 163 | 0.319 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 314,305 | 3.143 | 20 | 20 | fits | 153,567 | 222 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 451,608 | 4.516 | 20 | 20 | fits | 138,139 | 163 | 0.319 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 155,776 | 1.558 | 20 | 24 | fits | 149,683 | 162 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 316,955 | 3.170 | 20 | 24 | fits | 153,567 | 222 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 316,889 | 3.169 | 20 | 50 | fits | 153,567 | 222 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 454,632 | 4.546 | 20 | 50 | fits | 138,139 | 163 | 0.319 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 592,563 | 5.926 | 20 | 20 | fits | 137,997 | 50 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 985,416 | 9.854 | 20 | 20 | fits | 55,211 | 21 | 0.738 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 387,135 | 3.871 | 20 | 20 | fits | 146,747 | 169 | 0.365 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 309,372 | 3.094 | 20 | 200 | fits | 151,863 | 217 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 455,503 | 4.555 | 20 | 200 | fits | 146,747 | 169 | 0.365 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 310,296 | 3.103 | 20 | 20 | fits | 151,863 | 217 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 456,207 | 4.562 | 20 | 20 | fits | 146,747 | 169 | 0.365 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 162,073 | 1.621 | 20 | 24 | fits | 149,680 | 161 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 312,946 | 3.129 | 20 | 24 | fits | 151,863 | 217 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 312,880 | 3.129 | 20 | 50 | fits | 151,863 | 217 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 459,231 | 4.592 | 20 | 50 | fits | 146,747 | 169 | 0.365 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 668,311 | 6.683 | 20 | 20 | fits | 132,691 | 45 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 999,183 | 9.992 | 20 | 20 | fits | 55,398 | 20 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 379,127 | 3.791 | 20 | 20 | fits | 146,465 | 169 | 0.358 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 302,375 | 3.024 | 20 | 200 | fits | 151,706 | 217 | 0.369 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 448,224 | 4.482 | 20 | 200 | fits | 146,465 | 169 | 0.358 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 303,299 | 3.033 | 20 | 20 | fits | 151,706 | 217 | 0.369 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 448,928 | 4.489 | 20 | 20 | fits | 146,465 | 169 | 0.358 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 155,233 | 1.552 | 20 | 24 | fits | 149,680 | 161 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 305,949 | 3.059 | 20 | 24 | fits | 151,706 | 217 | 0.369 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 305,883 | 3.059 | 20 | 50 | fits | 151,706 | 217 | 0.369 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 451,952 | 4.520 | 20 | 50 | fits | 146,465 | 169 | 0.358 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 661,249 | 6.612 | 20 | 20 | fits | 132,908 | 46 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 991,872 | 9.919 | 20 | 20 | fits | 55,108 | 20 | 0.739 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 382,346 | 3.823 | 20 | 20 | fits | 147,786 | 172 | 0.348 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 294,735 | 2.947 | 20 | 200 | fits | 150,955 | 218 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 441,905 | 4.419 | 20 | 200 | fits | 147,786 | 172 | 0.348 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 295,659 | 2.957 | 20 | 20 | fits | 150,955 | 218 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 442,609 | 4.426 | 20 | 20 | fits | 147,786 | 172 | 0.348 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 148,344 | 1.483 | 20 | 24 | fits | 149,680 | 161 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 298,309 | 2.983 | 20 | 24 | fits | 150,955 | 218 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 298,243 | 2.982 | 20 | 50 | fits | 150,955 | 218 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 445,633 | 4.456 | 20 | 50 | fits | 147,786 | 172 | 0.348 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 658,050 | 6.580 | 20 | 20 | fits | 136,028 | 52 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 984,844 | 9.848 | 20 | 20 | fits | 54,966 | 20 | 0.736 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 371,344 | 3.713 | 20 | 20 | fits | 137,992 | 163 | 0.317 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 302,025 | 3.020 | 20 | 200 | fits | 151,863 | 217 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 439,401 | 4.394 | 20 | 200 | fits | 137,992 | 163 | 0.317 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 302,949 | 3.029 | 20 | 20 | fits | 151,863 | 217 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 440,105 | 4.401 | 20 | 20 | fits | 137,992 | 163 | 0.317 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 154,726 | 1.547 | 20 | 24 | fits | 149,680 | 161 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 305,599 | 3.056 | 20 | 24 | fits | 151,863 | 217 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 305,533 | 3.055 | 20 | 50 | fits | 151,863 | 217 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 443,129 | 4.431 | 20 | 50 | fits | 137,992 | 163 | 0.317 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 575,948 | 5.759 | 20 | 20 | fits | 132,885 | 44 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 906,600 | 9.066 | 20 | 20 | fits | 60,107 | 27 | 0.776 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 364,666 | 3.647 | 20 | 20 | fits | 138,210 | 163 | 0.319 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 295,923 | 2.959 | 20 | 200 | fits | 152,601 | 222 | 0.367 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 433,517 | 4.335 | 20 | 200 | fits | 138,210 | 163 | 0.319 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 296,847 | 2.968 | 20 | 20 | fits | 152,601 | 222 | 0.367 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 434,221 | 4.342 | 20 | 20 | fits | 138,210 | 163 | 0.319 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 147,886 | 1.479 | 20 | 24 | fits | 149,680 | 161 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 299,497 | 2.995 | 20 | 24 | fits | 152,601 | 222 | 0.367 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 299,431 | 2.994 | 20 | 50 | fits | 152,601 | 222 | 0.367 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 437,245 | 4.372 | 20 | 50 | fits | 138,210 | 163 | 0.319 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 570,064 | 5.701 | 20 | 20 | fits | 132,885 | 44 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 905,727 | 9.057 | 20 | 20 | fits | 60,188 | 26 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 374,544 | 3.745 | 20 | 20 | fits | 137,992 | 163 | 0.317 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 305,225 | 3.052 | 20 | 200 | fits | 151,863 | 217 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 442,601 | 4.426 | 20 | 200 | fits | 137,992 | 163 | 0.317 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 306,149 | 3.061 | 20 | 20 | fits | 151,863 | 217 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 443,305 | 4.433 | 20 | 20 | fits | 137,992 | 163 | 0.317 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 157,926 | 1.579 | 20 | 24 | fits | 149,680 | 161 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 308,799 | 3.088 | 20 | 24 | fits | 151,863 | 217 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 308,733 | 3.087 | 20 | 50 | fits | 151,863 | 217 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 446,329 | 4.463 | 20 | 50 | fits | 137,992 | 163 | 0.317 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 579,450 | 5.795 | 20 | 20 | fits | 133,187 | 45 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 914,979 | 9.150 | 20 | 20 | fits | 55,120 | 20 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 366,971 | 3.670 | 20 | 20 | fits | 138,478 | 164 | 0.321 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 298,228 | 2.982 | 20 | 200 | fits | 151,706 | 217 | 0.369 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 436,090 | 4.361 | 20 | 200 | fits | 138,478 | 164 | 0.321 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 299,152 | 2.992 | 20 | 20 | fits | 151,706 | 217 | 0.369 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 436,794 | 4.368 | 20 | 20 | fits | 138,478 | 164 | 0.321 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 151,086 | 1.511 | 20 | 24 | fits | 149,680 | 161 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 301,802 | 3.018 | 20 | 24 | fits | 151,706 | 217 | 0.369 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 301,736 | 3.017 | 20 | 50 | fits | 151,706 | 217 | 0.369 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 439,818 | 4.398 | 20 | 50 | fits | 138,478 | 164 | 0.321 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 585,902 | 5.859 | 20 | 20 | fits | 136,278 | 51 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 906,428 | 9.064 | 20 | 20 | fits | 55,106 | 20 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 391,897 | 3.919 | 20 | 20 | fits | 143,394 | 170 | 0.387 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 308,602 | 3.086 | 20 | 200 | fits | 152,040 | 218 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 461,028 | 4.610 | 20 | 200 | fits | 143,394 | 170 | 0.387 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 309,526 | 3.095 | 20 | 20 | fits | 152,040 | 218 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 461,732 | 4.617 | 20 | 20 | fits | 143,394 | 170 | 0.387 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 161,126 | 1.611 | 20 | 24 | fits | 149,680 | 161 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 312,176 | 3.122 | 20 | 24 | fits | 152,040 | 218 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 312,110 | 3.121 | 20 | 50 | fits | 152,040 | 218 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 464,756 | 4.648 | 20 | 50 | fits | 143,394 | 170 | 0.387 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 602,715 | 6.027 | 20 | 20 | fits | 138,025 | 50 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 917,827 | 9.178 | 20 | 20 | fits | 54,964 | 20 | 0.737 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 388,725 | 3.887 | 20 | 20 | fits | 146,527 | 169 | 0.359 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 312,052 | 3.121 | 20 | 200 | fits | 153,665 | 222 | 0.374 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 457,963 | 4.580 | 20 | 200 | fits | 146,527 | 169 | 0.359 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 312,976 | 3.130 | 20 | 20 | fits | 153,665 | 222 | 0.374 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 458,667 | 4.587 | 20 | 20 | fits | 146,527 | 169 | 0.359 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 154,669 | 1.547 | 20 | 24 | fits | 150,063 | 162 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 315,626 | 3.156 | 20 | 24 | fits | 153,665 | 222 | 0.374 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 315,560 | 3.156 | 20 | 50 | fits | 153,665 | 222 | 0.374 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 461,691 | 4.617 | 20 | 50 | fits | 146,527 | 169 | 0.359 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 594,385 | 5.944 | 20 | 20 | fits | 132,760 | 44 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 909,901 | 9.099 | 20 | 20 | fits | 55,069 | 20 | 0.739 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 381,825 | 3.818 | 20 | 20 | fits | 148,959 | 178 | 0.348 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 293,008 | 2.930 | 20 | 200 | fits | 150,907 | 218 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 441,351 | 4.414 | 20 | 200 | fits | 148,959 | 178 | 0.348 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 293,932 | 2.939 | 20 | 20 | fits | 150,907 | 218 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 442,055 | 4.421 | 20 | 20 | fits | 148,959 | 178 | 0.348 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 146,665 | 1.467 | 20 | 24 | fits | 150,845 | 166 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 296,582 | 2.966 | 20 | 24 | fits | 150,907 | 218 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 296,516 | 2.965 | 20 | 50 | fits | 150,907 | 218 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 445,079 | 4.451 | 20 | 50 | fits | 148,959 | 178 | 0.348 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 577,897 | 5.779 | 20 | 20 | fits | 132,884 | 44 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 907,931 | 9.079 | 20 | 20 | fits | 59,678 | 27 | 0.771 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 367,875 | 3.679 | 20 | 20 | fits | 146,814 | 172 | 0.301 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 298,978 | 2.990 | 20 | 200 | fits | 150,719 | 215 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 445,176 | 4.452 | 20 | 200 | fits | 146,814 | 172 | 0.301 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 299,902 | 2.999 | 20 | 20 | fits | 150,719 | 215 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 445,880 | 4.459 | 20 | 20 | fits | 146,814 | 172 | 0.301 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 152,823 | 1.528 | 20 | 24 | fits | 149,401 | 161 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 302,552 | 3.026 | 20 | 24 | fits | 150,719 | 215 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 302,486 | 3.025 | 20 | 50 | fits | 150,719 | 215 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 448,904 | 4.489 | 20 | 50 | fits | 146,814 | 172 | 0.301 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 581,419 | 5.814 | 20 | 20 | fits | 132,581 | 44 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 912,091 | 9.121 | 20 | 20 | fits | 55,385 | 20 | 0.747 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 385,879 | 3.859 | 20 | 20 | fits | 138,187 | 163 | 0.320 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 308,870 | 3.089 | 20 | 200 | fits | 153,521 | 222 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 446,441 | 4.464 | 20 | 200 | fits | 138,187 | 163 | 0.320 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 309,794 | 3.098 | 20 | 20 | fits | 153,521 | 222 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 447,145 | 4.471 | 20 | 20 | fits | 138,187 | 163 | 0.320 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 151,313 | 1.513 | 20 | 24 | fits | 149,565 | 162 | 0.381 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 312,444 | 3.124 | 20 | 24 | fits | 153,521 | 222 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 312,378 | 3.124 | 20 | 50 | fits | 153,521 | 222 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 450,169 | 4.502 | 20 | 50 | fits | 138,187 | 163 | 0.320 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 582,991 | 5.830 | 20 | 20 | fits | 132,888 | 44 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 898,528 | 8.985 | 20 | 20 | fits | 55,106 | 20 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 387,341 | 3.873 | 20 | 20 | fits | 138,058 | 163 | 0.319 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 318,777 | 3.188 | 20 | 200 | fits | 153,307 | 222 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 456,219 | 4.562 | 20 | 200 | fits | 138,058 | 163 | 0.319 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 319,701 | 3.197 | 20 | 20 | fits | 153,307 | 222 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 456,923 | 4.569 | 20 | 20 | fits | 138,058 | 163 | 0.319 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 161,485 | 1.615 | 20 | 24 | fits | 149,697 | 162 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 322,351 | 3.224 | 20 | 24 | fits | 153,307 | 222 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 322,285 | 3.223 | 20 | 50 | fits | 153,307 | 222 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 459,947 | 4.599 | 20 | 50 | fits | 138,058 | 163 | 0.319 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 592,908 | 5.929 | 20 | 20 | fits | 133,027 | 44 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 913,993 | 9.140 | 20 | 20 | fits | 60,575 | 26 | 0.755 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 366,608 | 3.666 | 20 | 20 | fits | 138,210 | 163 | 0.319 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 297,865 | 2.979 | 20 | 200 | fits | 151,550 | 217 | 0.367 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 435,459 | 4.355 | 20 | 200 | fits | 138,210 | 163 | 0.319 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 298,789 | 2.988 | 20 | 20 | fits | 151,550 | 217 | 0.367 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 436,163 | 4.362 | 20 | 20 | fits | 138,210 | 163 | 0.319 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 150,879 | 1.509 | 20 | 24 | fits | 149,712 | 161 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 301,439 | 3.014 | 20 | 24 | fits | 151,550 | 217 | 0.367 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 301,373 | 3.014 | 20 | 50 | fits | 151,550 | 217 | 0.367 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 439,187 | 4.392 | 20 | 50 | fits | 138,210 | 163 | 0.319 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 572,006 | 5.720 | 20 | 20 | fits | 132,885 | 44 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 989,160 | 9.892 | 20 | 20 | fits | 67,413 | 25 | 0.735 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 377,221 | 3.772 | 20 | 20 | fits | 137,992 | 163 | 0.317 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 307,902 | 3.079 | 20 | 200 | fits | 151,707 | 217 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 445,278 | 4.453 | 20 | 200 | fits | 137,992 | 163 | 0.317 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 308,826 | 3.088 | 20 | 20 | fits | 151,707 | 217 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 445,982 | 4.460 | 20 | 20 | fits | 137,992 | 163 | 0.317 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 160,759 | 1.608 | 20 | 24 | fits | 149,712 | 161 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 311,476 | 3.115 | 20 | 24 | fits | 151,707 | 217 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 311,410 | 3.114 | 20 | 50 | fits | 151,707 | 217 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 449,006 | 4.490 | 20 | 50 | fits | 137,992 | 163 | 0.317 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 582,127 | 5.821 | 20 | 20 | fits | 133,187 | 45 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 999,100 | 9.991 | 20 | 20 | fits | 66,057 | 24 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 369,508 | 3.695 | 20 | 20 | fits | 138,210 | 163 | 0.319 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 300,765 | 3.008 | 20 | 200 | fits | 151,550 | 217 | 0.367 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 438,359 | 4.384 | 20 | 200 | fits | 138,210 | 163 | 0.319 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 301,689 | 3.017 | 20 | 20 | fits | 151,550 | 217 | 0.367 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 439,063 | 4.391 | 20 | 20 | fits | 138,210 | 163 | 0.319 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 153,779 | 1.538 | 20 | 24 | fits | 149,712 | 161 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 304,339 | 3.043 | 20 | 24 | fits | 151,550 | 217 | 0.367 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 304,273 | 3.043 | 20 | 50 | fits | 151,550 | 217 | 0.367 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 442,087 | 4.421 | 20 | 50 | fits | 138,210 | 163 | 0.319 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 571,369 | 5.714 | 20 | 20 | fits | 129,348 | 53 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 990,265 | 9.903 | 20 | 20 | fits | 65,901 | 24 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 391,075 | 3.911 | 20 | 20 | fits | 148,750 | 176 | 0.370 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 310,802 | 3.108 | 20 | 200 | fits | 151,707 | 217 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 458,936 | 4.589 | 20 | 200 | fits | 148,750 | 176 | 0.370 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 311,726 | 3.117 | 20 | 20 | fits | 151,707 | 217 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 459,640 | 4.596 | 20 | 20 | fits | 148,750 | 176 | 0.370 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 163,659 | 1.637 | 20 | 24 | fits | 149,712 | 161 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 314,376 | 3.144 | 20 | 24 | fits | 151,707 | 217 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 314,310 | 3.143 | 20 | 50 | fits | 151,707 | 217 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 462,664 | 4.627 | 20 | 50 | fits | 148,750 | 176 | 0.370 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 686,177 | 6.862 | 20 | 20 | fits | 133,936 | 45 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,001,540 | 10.015 | 20 | 20 | fits | 55,069 | 20 | 0.739 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 393,337 | 3.933 | 20 | 20 | fits | 149,762 | 175 | 0.401 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 304,061 | 3.041 | 20 | 200 | fits | 151,946 | 218 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 462,802 | 4.628 | 20 | 200 | fits | 149,762 | 175 | 0.401 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 304,985 | 3.050 | 20 | 20 | fits | 151,946 | 218 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 463,506 | 4.635 | 20 | 20 | fits | 149,762 | 175 | 0.401 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 156,679 | 1.567 | 20 | 24 | fits | 149,712 | 161 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 307,635 | 3.076 | 20 | 24 | fits | 151,946 | 218 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 307,569 | 3.076 | 20 | 50 | fits | 151,946 | 218 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 466,530 | 4.665 | 20 | 50 | fits | 149,762 | 175 | 0.401 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 680,246 | 6.802 | 20 | 20 | fits | 133,045 | 45 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 995,662 | 9.957 | 20 | 20 | fits | 55,069 | 20 | 0.739 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 474,724 | 4.747 | 20 | 20 | fits | 143,162 | 172 | 0.342 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 311,160 | 3.112 | 20 | 200 | fits | 157,331 | 218 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 534,163 | 5.342 | 20 | 200 | fits | 143,162 | 172 | 0.342 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 312,084 | 3.121 | 20 | 20 | fits | 157,331 | 218 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 534,867 | 5.349 | 20 | 20 | fits | 143,162 | 172 | 0.342 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 150,008 | 1.500 | 20 | 24 | fits | 150,021 | 162 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 314,734 | 3.147 | 20 | 24 | fits | 157,331 | 218 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 314,668 | 3.147 | 20 | 50 | fits | 157,331 | 218 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 537,891 | 5.379 | 20 | 50 | fits | 143,162 | 172 | 0.342 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 670,574 | 6.706 | 20 | 20 | fits | 132,749 | 44 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,000,803 | 10.008 | 20 | 20 | fits | 59,742 | 27 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 373,187 | 3.732 | 20 | 20 | fits | 138,260 | 164 | 0.320 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 303,868 | 3.039 | 20 | 200 | fits | 151,707 | 217 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 441,512 | 4.415 | 20 | 200 | fits | 138,260 | 164 | 0.320 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 304,792 | 3.048 | 20 | 20 | fits | 151,707 | 217 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 442,216 | 4.422 | 20 | 20 | fits | 138,260 | 164 | 0.320 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 156,725 | 1.567 | 20 | 24 | fits | 149,680 | 161 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 307,442 | 3.074 | 20 | 24 | fits | 151,707 | 217 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 307,376 | 3.074 | 20 | 50 | fits | 151,707 | 217 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 445,240 | 4.452 | 20 | 50 | fits | 138,260 | 164 | 0.320 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 591,391 | 5.914 | 20 | 20 | fits | 136,345 | 51 | 0.733 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 906,784 | 9.068 | 20 | 20 | fits | 55,106 | 20 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 379,687 | 3.797 | 20 | 20 | fits | 143,449 | 170 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 297,048 | 2.970 | 20 | 200 | fits | 151,727 | 218 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 449,527 | 4.495 | 20 | 200 | fits | 143,449 | 170 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 297,972 | 2.980 | 20 | 20 | fits | 151,727 | 218 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 450,231 | 4.502 | 20 | 20 | fits | 143,449 | 170 | 0.384 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 149,885 | 1.499 | 20 | 24 | fits | 149,680 | 161 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 300,622 | 3.006 | 20 | 24 | fits | 151,727 | 218 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 300,556 | 3.006 | 20 | 50 | fits | 151,727 | 218 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 453,255 | 4.533 | 20 | 50 | fits | 143,449 | 170 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 586,087 | 5.861 | 20 | 20 | fits | 132,898 | 44 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 906,720 | 9.067 | 20 | 20 | fits | 60,347 | 26 | 0.751 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 387,167 | 3.872 | 20 | 20 | fits | 138,183 | 163 | 0.320 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 317,798 | 3.178 | 20 | 200 | fits | 153,542 | 222 | 0.376 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 455,365 | 4.554 | 20 | 200 | fits | 138,183 | 163 | 0.320 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 318,722 | 3.187 | 20 | 20 | fits | 153,542 | 222 | 0.376 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 456,069 | 4.561 | 20 | 20 | fits | 138,183 | 163 | 0.320 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 160,252 | 1.603 | 20 | 24 | fits | 150,007 | 162 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 321,372 | 3.214 | 20 | 24 | fits | 153,542 | 222 | 0.376 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 321,306 | 3.213 | 20 | 50 | fits | 153,542 | 222 | 0.376 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 459,093 | 4.591 | 20 | 50 | fits | 138,183 | 163 | 0.320 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 591,900 | 5.919 | 20 | 20 | fits | 132,873 | 44 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 913,145 | 9.131 | 20 | 20 | fits | 55,365 | 21 | 0.741 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 364,894 | 3.649 | 20 | 20 | fits | 137,898 | 163 | 0.316 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 296,316 | 2.963 | 20 | 200 | fits | 152,794 | 222 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 433,598 | 4.336 | 20 | 200 | fits | 137,898 | 163 | 0.316 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 297,240 | 2.972 | 20 | 20 | fits | 152,794 | 222 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 434,302 | 4.343 | 20 | 20 | fits | 137,898 | 163 | 0.316 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 148,086 | 1.481 | 20 | 24 | fits | 149,422 | 161 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 299,890 | 2.999 | 20 | 24 | fits | 152,794 | 222 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 299,824 | 2.998 | 20 | 50 | fits | 152,794 | 222 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 437,326 | 4.373 | 20 | 50 | fits | 137,898 | 163 | 0.316 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 570,284 | 5.703 | 20 | 20 | fits | 133,024 | 44 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 906,047 | 9.060 | 20 | 20 | fits | 59,644 | 27 | 0.770 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 383,691 | 3.837 | 20 | 20 | fits | 139,537 | 166 | 0.309 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 304,050 | 3.041 | 20 | 200 | fits | 150,096 | 213 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 442,971 | 4.430 | 20 | 200 | fits | 139,537 | 166 | 0.309 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 304,974 | 3.050 | 20 | 20 | fits | 150,096 | 213 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 443,675 | 4.437 | 20 | 20 | fits | 139,537 | 166 | 0.309 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 158,518 | 1.585 | 20 | 24 | fits | 149,401 | 161 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 307,624 | 3.076 | 20 | 24 | fits | 150,096 | 213 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 307,558 | 3.076 | 20 | 50 | fits | 150,096 | 213 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 446,699 | 4.467 | 20 | 50 | fits | 139,537 | 166 | 0.309 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 584,821 | 5.848 | 20 | 20 | fits | 138,188 | 50 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 915,284 | 9.153 | 20 | 20 | fits | 55,398 | 20 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 367,591 | 3.676 | 20 | 20 | fits | 137,898 | 163 | 0.316 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 299,013 | 2.990 | 20 | 200 | fits | 151,899 | 217 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 436,295 | 4.363 | 20 | 200 | fits | 137,898 | 163 | 0.316 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 299,937 | 2.999 | 20 | 20 | fits | 151,899 | 217 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 436,999 | 4.370 | 20 | 20 | fits | 137,898 | 163 | 0.316 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 151,678 | 1.517 | 20 | 24 | fits | 149,401 | 161 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 302,587 | 3.026 | 20 | 24 | fits | 151,899 | 217 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 302,521 | 3.025 | 20 | 50 | fits | 151,899 | 217 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 440,023 | 4.400 | 20 | 50 | fits | 137,898 | 163 | 0.316 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 578,447 | 5.784 | 20 | 20 | fits | 138,490 | 51 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 908,659 | 9.087 | 20 | 20 | fits | 55,108 | 20 | 0.739 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 394,842 | 3.948 | 20 | 20 | fits | 148,002 | 173 | 0.350 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 307,250 | 3.072 | 20 | 200 | fits | 150,096 | 213 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 454,636 | 4.546 | 20 | 200 | fits | 148,002 | 173 | 0.350 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 308,174 | 3.082 | 20 | 20 | fits | 150,096 | 213 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 455,340 | 4.553 | 20 | 20 | fits | 148,002 | 173 | 0.350 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 161,718 | 1.617 | 20 | 24 | fits | 149,401 | 161 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 310,824 | 3.108 | 20 | 24 | fits | 150,096 | 213 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 310,758 | 3.108 | 20 | 50 | fits | 150,096 | 213 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 458,364 | 4.584 | 20 | 50 | fits | 148,002 | 173 | 0.350 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 604,433 | 6.044 | 20 | 20 | fits | 136,194 | 51 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 919,896 | 9.199 | 20 | 20 | fits | 55,069 | 20 | 0.739 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 384,044 | 3.840 | 20 | 20 | fits | 151,089 | 174 | 0.370 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 301,463 | 3.015 | 20 | 200 | fits | 151,149 | 216 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 461,451 | 4.615 | 20 | 200 | fits | 151,089 | 174 | 0.370 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 302,387 | 3.024 | 20 | 20 | fits | 151,149 | 216 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 462,155 | 4.622 | 20 | 20 | fits | 151,089 | 174 | 0.370 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 154,878 | 1.549 | 20 | 24 | fits | 149,401 | 161 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 305,037 | 3.050 | 20 | 24 | fits | 151,149 | 216 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 304,971 | 3.050 | 20 | 50 | fits | 151,149 | 216 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 465,179 | 4.652 | 20 | 50 | fits | 151,089 | 174 | 0.370 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 597,977 | 5.980 | 20 | 20 | fits | 132,864 | 44 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 913,478 | 9.135 | 20 | 20 | fits | 55,069 | 20 | 0.739 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 365,056 | 3.651 | 20 | 20 | fits | 138,340 | 164 | 0.322 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 295,657 | 2.957 | 20 | 200 | fits | 152,737 | 222 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 433,381 | 4.334 | 20 | 200 | fits | 138,340 | 164 | 0.322 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 296,581 | 2.966 | 20 | 20 | fits | 152,737 | 222 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 434,085 | 4.341 | 20 | 20 | fits | 138,340 | 164 | 0.322 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 147,484 | 1.475 | 20 | 24 | fits | 149,615 | 161 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 299,231 | 2.992 | 20 | 24 | fits | 152,737 | 222 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 299,165 | 2.992 | 20 | 50 | fits | 152,737 | 222 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 437,109 | 4.371 | 20 | 50 | fits | 138,340 | 164 | 0.322 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 583,349 | 5.833 | 20 | 20 | fits | 136,434 | 51 | 0.733 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 898,742 | 8.987 | 20 | 20 | fits | 55,106 | 20 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 395,655 | 3.957 | 20 | 20 | fits | 143,234 | 170 | 0.382 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 304,754 | 3.048 | 20 | 200 | fits | 151,794 | 218 | 0.369 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 457,018 | 4.570 | 20 | 200 | fits | 143,234 | 170 | 0.382 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 305,678 | 3.057 | 20 | 20 | fits | 151,794 | 218 | 0.369 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 457,722 | 4.577 | 20 | 20 | fits | 143,234 | 170 | 0.382 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 157,524 | 1.575 | 20 | 24 | fits | 149,615 | 161 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 308,328 | 3.083 | 20 | 24 | fits | 151,794 | 218 | 0.369 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 308,262 | 3.083 | 20 | 50 | fits | 151,794 | 218 | 0.369 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 460,746 | 4.607 | 20 | 50 | fits | 143,234 | 170 | 0.382 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 593,667 | 5.937 | 20 | 20 | fits | 132,987 | 44 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 914,210 | 9.142 | 20 | 20 | fits | 60,347 | 26 | 0.751 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 378,045 | 3.780 | 20 | 20 | fits | 138,240 | 163 | 0.321 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 308,619 | 3.086 | 20 | 200 | fits | 153,595 | 222 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 446,243 | 4.462 | 20 | 200 | fits | 138,240 | 163 | 0.321 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 309,543 | 3.095 | 20 | 20 | fits | 153,595 | 222 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 446,947 | 4.469 | 20 | 20 | fits | 138,240 | 163 | 0.321 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 151,020 | 1.510 | 20 | 24 | fits | 149,951 | 162 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 312,193 | 3.122 | 20 | 24 | fits | 153,595 | 222 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 312,127 | 3.121 | 20 | 50 | fits | 153,595 | 222 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 449,971 | 4.500 | 20 | 50 | fits | 138,240 | 163 | 0.321 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 582,867 | 5.829 | 20 | 20 | fits | 132,962 | 44 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 985,343 | 9.853 | 20 | 20 | fits | 59,126 | 28 | 0.741 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 372,683 | 3.727 | 20 | 20 | fits | 138,215 | 163 | 0.319 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 303,902 | 3.039 | 20 | 200 | fits | 151,727 | 217 | 0.369 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 441,501 | 4.415 | 20 | 200 | fits | 138,215 | 163 | 0.319 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 304,826 | 3.048 | 20 | 20 | fits | 151,727 | 217 | 0.369 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 442,205 | 4.422 | 20 | 20 | fits | 138,215 | 163 | 0.319 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 156,739 | 1.567 | 20 | 24 | fits | 149,420 | 161 | 0.381 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 307,476 | 3.075 | 20 | 24 | fits | 151,727 | 217 | 0.369 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 307,410 | 3.074 | 20 | 50 | fits | 151,727 | 217 | 0.369 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 445,229 | 4.452 | 20 | 50 | fits | 138,215 | 163 | 0.319 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 578,076 | 5.781 | 20 | 20 | fits | 132,913 | 44 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 992,465 | 9.925 | 20 | 20 | fits | 57,012 | 21 | 0.774 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 375,113 | 3.751 | 20 | 20 | fits | 139,514 | 166 | 0.308 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 295,495 | 2.955 | 20 | 200 | fits | 150,081 | 213 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 434,393 | 4.344 | 20 | 200 | fits | 139,514 | 166 | 0.308 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 296,419 | 2.964 | 20 | 20 | fits | 150,081 | 213 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 435,097 | 4.351 | 20 | 20 | fits | 139,514 | 166 | 0.308 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 149,978 | 1.500 | 20 | 24 | fits | 149,336 | 161 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 299,069 | 2.991 | 20 | 24 | fits | 150,081 | 213 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 299,003 | 2.990 | 20 | 50 | fits | 150,081 | 213 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 438,121 | 4.381 | 20 | 50 | fits | 139,514 | 166 | 0.308 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 576,271 | 5.763 | 20 | 20 | fits | 138,216 | 50 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 985,132 | 9.851 | 20 | 20 | fits | 55,192 | 20 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 383,971 | 3.840 | 20 | 20 | fits | 146,470 | 169 | 0.358 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 307,181 | 3.072 | 20 | 200 | fits | 151,727 | 217 | 0.369 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 453,035 | 4.530 | 20 | 200 | fits | 146,470 | 169 | 0.358 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 308,105 | 3.081 | 20 | 20 | fits | 151,727 | 217 | 0.369 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 453,739 | 4.537 | 20 | 20 | fits | 146,470 | 169 | 0.358 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 160,018 | 1.600 | 20 | 24 | fits | 149,336 | 161 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 310,755 | 3.108 | 20 | 24 | fits | 151,727 | 217 | 0.369 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 310,689 | 3.107 | 20 | 50 | fits | 151,727 | 217 | 0.369 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 456,763 | 4.568 | 20 | 50 | fits | 146,470 | 169 | 0.358 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 670,231 | 6.702 | 20 | 20 | fits | 136,180 | 52 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 996,892 | 9.969 | 20 | 20 | fits | 54,966 | 20 | 0.736 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 386,344 | 3.863 | 20 | 20 | fits | 148,059 | 173 | 0.350 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 298,695 | 2.987 | 20 | 200 | fits | 150,081 | 213 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 446,138 | 4.461 | 20 | 200 | fits | 148,059 | 173 | 0.350 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 299,619 | 2.996 | 20 | 20 | fits | 150,081 | 213 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 446,842 | 4.468 | 20 | 20 | fits | 148,059 | 173 | 0.350 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 153,178 | 1.532 | 20 | 24 | fits | 149,336 | 161 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 302,269 | 3.023 | 20 | 24 | fits | 150,081 | 213 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 302,203 | 3.022 | 20 | 50 | fits | 150,081 | 213 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 449,866 | 4.499 | 20 | 50 | fits | 148,059 | 173 | 0.350 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 672,840 | 6.728 | 20 | 20 | fits | 136,448 | 51 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 988,235 | 9.882 | 20 | 20 | fits | 55,069 | 20 | 0.739 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 476,491 | 4.765 | 20 | 20 | fits | 144,046 | 169 | 0.390 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 316,810 | 3.168 | 20 | 200 | fits | 158,156 | 223 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 546,378 | 5.464 | 20 | 200 | fits | 144,046 | 169 | 0.390 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 317,734 | 3.177 | 20 | 20 | fits | 158,156 | 223 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 547,082 | 5.471 | 20 | 20 | fits | 144,046 | 169 | 0.390 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 163,218 | 1.632 | 20 | 24 | fits | 149,336 | 161 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 320,384 | 3.204 | 20 | 24 | fits | 158,156 | 223 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 320,318 | 3.203 | 20 | 50 | fits | 158,156 | 223 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 550,106 | 5.501 | 20 | 50 | fits | 144,046 | 169 | 0.390 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 682,935 | 6.829 | 20 | 20 | fits | 132,895 | 44 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 998,248 | 9.982 | 20 | 20 | fits | 54,927 | 20 | 0.736 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 368,446 | 3.684 | 20 | 20 | fits | 138,215 | 163 | 0.319 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 299,665 | 2.997 | 20 | 200 | fits | 151,727 | 217 | 0.369 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 437,264 | 4.373 | 20 | 200 | fits | 138,215 | 163 | 0.319 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 300,589 | 3.006 | 20 | 20 | fits | 151,727 | 217 | 0.369 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 437,968 | 4.380 | 20 | 20 | fits | 138,215 | 163 | 0.319 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 152,502 | 1.525 | 20 | 24 | fits | 149,336 | 161 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 303,239 | 3.032 | 20 | 24 | fits | 151,727 | 217 | 0.369 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 303,173 | 3.032 | 20 | 50 | fits | 151,727 | 217 | 0.369 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 440,992 | 4.410 | 20 | 50 | fits | 138,215 | 163 | 0.319 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 574,202 | 5.742 | 20 | 20 | fits | 133,276 | 45 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 904,806 | 9.048 | 20 | 20 | fits | 55,108 | 20 | 0.739 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 379,344 | 3.793 | 20 | 20 | fits | 138,322 | 164 | 0.321 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 309,930 | 3.099 | 20 | 200 | fits | 151,952 | 217 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 447,636 | 4.476 | 20 | 200 | fits | 138,322 | 164 | 0.321 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 310,854 | 3.109 | 20 | 20 | fits | 151,952 | 217 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 448,340 | 4.483 | 20 | 20 | fits | 138,322 | 164 | 0.321 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 162,542 | 1.625 | 20 | 24 | fits | 149,336 | 161 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 313,504 | 3.135 | 20 | 24 | fits | 151,952 | 217 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 313,438 | 3.134 | 20 | 50 | fits | 151,952 | 217 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 451,364 | 4.514 | 20 | 50 | fits | 138,322 | 164 | 0.321 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 597,543 | 5.975 | 20 | 20 | fits | 136,373 | 51 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 918,028 | 9.180 | 20 | 20 | fits | 60,198 | 26 | 0.747 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 385,657 | 3.857 | 20 | 20 | fits | 143,390 | 170 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 303,042 | 3.030 | 20 | 200 | fits | 151,904 | 218 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 455,462 | 4.555 | 20 | 200 | fits | 143,390 | 170 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 303,966 | 3.040 | 20 | 20 | fits | 151,904 | 218 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 456,166 | 4.562 | 20 | 20 | fits | 143,390 | 170 | 0.383 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 155,702 | 1.557 | 20 | 24 | fits | 149,336 | 161 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 306,616 | 3.066 | 20 | 24 | fits | 151,904 | 218 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 306,550 | 3.066 | 20 | 50 | fits | 151,904 | 218 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 459,190 | 4.592 | 20 | 50 | fits | 143,390 | 170 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 592,126 | 5.921 | 20 | 20 | fits | 133,002 | 44 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 912,647 | 9.126 | 20 | 20 | fits | 54,964 | 20 | 0.737 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 388,013 | 3.880 | 20 | 20 | fits | 144,484 | 172 | 0.372 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 294,770 | 2.948 | 20 | 200 | fits | 151,334 | 219 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 448,233 | 4.482 | 20 | 200 | fits | 144,484 | 172 | 0.372 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 295,694 | 2.957 | 20 | 20 | fits | 151,334 | 219 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 448,937 | 4.489 | 20 | 20 | fits | 144,484 | 172 | 0.372 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 148,000 | 1.480 | 20 | 24 | fits | 149,336 | 161 | 0.380 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 298,344 | 2.983 | 20 | 24 | fits | 151,334 | 219 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 298,278 | 2.983 | 20 | 50 | fits | 151,334 | 219 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 451,961 | 4.520 | 20 | 50 | fits | 144,484 | 172 | 0.372 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 584,949 | 5.849 | 20 | 20 | fits | 133,054 | 44 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 905,606 | 9.056 | 20 | 20 | fits | 54,964 | 20 | 0.737 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 385,443 | 3.854 | 20 | 20 | fits | 138,398 | 163 | 0.322 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 316,653 | 3.167 | 20 | 200 | fits | 153,484 | 222 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 454,435 | 4.544 | 20 | 200 | fits | 138,398 | 163 | 0.322 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 317,577 | 3.176 | 20 | 20 | fits | 153,484 | 222 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 455,139 | 4.551 | 20 | 20 | fits | 138,398 | 163 | 0.322 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 159,184 | 1.592 | 20 | 24 | fits | 149,618 | 162 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 320,227 | 3.202 | 20 | 24 | fits | 153,484 | 222 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 320,161 | 3.202 | 20 | 50 | fits | 153,484 | 222 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 458,163 | 4.582 | 20 | 50 | fits | 138,398 | 163 | 0.322 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 596,198 | 5.962 | 20 | 20 | fits | 138,101 | 50 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 911,839 | 9.118 | 20 | 20 | fits | 55,106 | 20 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 372,946 | 3.729 | 20 | 20 | fits | 138,022 | 163 | 0.317 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 295,961 | 2.960 | 20 | 200 | fits | 152,512 | 222 | 0.366 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 433,367 | 4.334 | 20 | 200 | fits | 138,022 | 163 | 0.317 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 296,885 | 2.969 | 20 | 20 | fits | 152,512 | 222 | 0.366 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 434,071 | 4.341 | 20 | 20 | fits | 138,022 | 163 | 0.317 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 148,013 | 1.480 | 20 | 24 | fits | 149,615 | 161 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 299,535 | 2.995 | 20 | 24 | fits | 152,512 | 222 | 0.366 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 299,469 | 2.995 | 20 | 50 | fits | 152,512 | 222 | 0.366 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 437,095 | 4.371 | 20 | 50 | fits | 138,022 | 163 | 0.317 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 575,106 | 5.751 | 20 | 20 | fits | 138,077 | 50 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 905,288 | 9.053 | 20 | 20 | fits | 59,635 | 27 | 0.770 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 382,312 | 3.823 | 20 | 20 | fits | 146,580 | 169 | 0.364 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 305,331 | 3.053 | 20 | 200 | fits | 151,842 | 217 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 451,295 | 4.513 | 20 | 200 | fits | 146,580 | 169 | 0.364 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 306,255 | 3.063 | 20 | 20 | fits | 151,842 | 217 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 451,999 | 4.520 | 20 | 20 | fits | 146,580 | 169 | 0.364 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 158,053 | 1.581 | 20 | 24 | fits | 149,615 | 161 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 308,905 | 3.089 | 20 | 24 | fits | 151,842 | 217 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 308,839 | 3.088 | 20 | 50 | fits | 151,842 | 217 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 455,023 | 4.550 | 20 | 50 | fits | 146,580 | 169 | 0.364 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 588,063 | 5.881 | 20 | 20 | fits | 133,106 | 44 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 918,636 | 9.186 | 20 | 20 | fits | 55,193 | 20 | 0.746 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 381,365 | 3.814 | 20 | 20 | fits | 137,787 | 163 | 0.314 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 304,380 | 3.044 | 20 | 200 | fits | 157,731 | 222 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 441,551 | 4.416 | 20 | 200 | fits | 137,787 | 163 | 0.314 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 305,304 | 3.053 | 20 | 20 | fits | 157,731 | 222 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 442,255 | 4.423 | 20 | 20 | fits | 137,787 | 163 | 0.314 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 151,213 | 1.512 | 20 | 24 | fits | 149,615 | 161 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 307,954 | 3.080 | 20 | 24 | fits | 157,731 | 222 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 307,888 | 3.079 | 20 | 50 | fits | 157,731 | 222 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 445,279 | 4.453 | 20 | 50 | fits | 137,787 | 163 | 0.314 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 578,256 | 5.783 | 20 | 20 | fits | 133,043 | 45 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 908,558 | 9.086 | 20 | 20 | fits | 55,108 | 20 | 0.739 |
| LINK_UP | `adp.link_up.if0` | 1,994 | 0.020 | 20 | 200 | fits | 32,612 | 43 (11) | 0.671 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 14,932 | 0.149 | 20 | 200 | fits | 22,596 | 23 (39) | 0.617 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 12,461 | 0.125 | 20 | 200 | fits | 1,992 | 10 (11) | 0.429 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 14,468 | 0.145 | 20 | 20 | fits | 33,667 | 21 (35) | 0.794 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 21,032 | 0.210 | 20 | 20 | fits | 29,566 | 17 (14) | 0.826 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 13,947 | 0.139 | 20 | 20 | fits | 29,997 | 18 (14) | 0.825 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 29,840 | 0.298 | 20 | 20 | fits | 36,840 | 27 (35) | 0.764 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 80,367 | 0.804 | 20 | 20 | fits | 28,095 | 8 | 0.851 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 43,111 | 0.431 | 20 | 20 | fits | 43,177 | 12 | 0.887 |
| malformed MRPDU discard | `srp.malformed.if0` | 23,368 | 0.234 | 20 | 20 | fits | 23,434 | 12 | 0.698 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 76,579 | 0.766 | 220 | 220 | fits | 44,021 | 6 | 0.918 |
| an event behind 15 others | `backlog.event.if0` | 162,704 | 1.627 | 20 | 200 | fits | 55,092 | 78 | 0.530 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 453,492 | 4.535 | 20 | 20 | fits | 70,448 | 94 | 0.181 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 422,813 | 4.228 | 20 | 200 | fits | 149,608 | 117 | 0.297 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 492,645 | 4.926 | 20 | 200 | fits | 70,448 | 94 | 0.181 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 418,491 | 4.185 | 20 | 20 | fits | 149,608 | 117 | 0.297 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 488,103 | 4.881 | 20 | 20 | fits | 70,448 | 94 | 0.181 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 152,982 | 1.530 | 20 | 24 | fits | 153,873 | 167 | 0.393 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 271,533 | 2.715 | 20 | 24 | fits | 64,449 | 26 | 0.693 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 421,075 | 4.211 | 20 | 50 | fits | 149,608 | 117 | 0.297 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 420,679 | 4.207 | 20 | 50 | fits | 149,608 | 117 | 0.297 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 491,061 | 4.911 | 20 | 20 | fits | 70,448 | 94 | 0.181 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 552,860 | 5.529 | 20 | 20 | fits | 27,037 | 41 | 0.113 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 379,561 | 3.796 | 20 | 20 | fits | 142,622 | 170 | 0.385 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 296,930 | 2.969 | 20 | 200 | fits | 151,800 | 218 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 448,517 | 4.485 | 20 | 200 | fits | 142,622 | 170 | 0.385 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 297,854 | 2.979 | 20 | 20 | fits | 151,800 | 218 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 449,221 | 4.492 | 20 | 20 | fits | 142,622 | 170 | 0.385 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 149,694 | 1.497 | 20 | 24 | fits | 149,880 | 164 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 300,504 | 3.005 | 20 | 24 | fits | 151,800 | 218 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 300,438 | 3.004 | 20 | 50 | fits | 151,800 | 218 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 452,245 | 4.522 | 20 | 50 | fits | 142,622 | 170 | 0.385 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 584,900 | 5.849 | 20 | 20 | fits | 132,721 | 44 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 905,521 | 9.055 | 20 | 20 | fits | 54,922 | 20 | 0.736 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 23,106 | 0.231 | 20 | 20 | fits | 32,034 | 19 | 0.787 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 296,930 | 2.969 | 20 | 200 | fits | 151,800 | 218 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 45,296 | 0.453 | 20 | 200 | fits | 32,034 | 19 | 0.787 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 297,854 | 2.979 | 20 | 20 | fits | 151,800 | 218 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 434,797 | 4.348 | 20 | 20 | fits | 128,198 | 160 | 0.312 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 149,694 | 1.497 | 20 | 24 | fits | 149,880 | 164 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 300,504 | 3.005 | 20 | 24 | fits | 151,800 | 218 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 300,438 | 3.004 | 20 | 50 | fits | 151,800 | 218 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 437,821 | 4.378 | 20 | 50 | fits | 128,198 | 160 | 0.312 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 570,069 | 5.701 | 20 | 20 | fits | 132,314 | 44 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 890,644 | 8.906 | 20 | 20 | fits | 54,922 | 20 | 0.736 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,313,222 | 63.132 | 20 | 20 | MISS ceiling | 21,804 | 13 | 0.500 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,334,977 | 63.350 | 20 | 20 | MISS ceiling | 21,831 | 13 | 0.473 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,356,660 | 63.567 | 20 | 20 | MISS ceiling | 21,740 | 13 | 0.481 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,378,403 | 63.784 | 20 | 20 | MISS ceiling | 21,819 | 13 | 0.464 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,399,968 | 64.000 | 20 | 20 | MISS ceiling | 21,628 | 13 | 0.500 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 156,948 | 1.569 | 20 | 200 | fits | 158,051 | 201 | 0.290 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 276,782 | 2.768 | 20 | 200 | fits | 120,450 | 143 | 0.471 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 152,626 | 1.526 | 20 | 20 | fits | 158,051 | 201 | 0.290 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,210,562 | 62.106 | 20 | 20 | MISS ceiling | 35,640 | 15 | 0.669 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 276,716 | 2.767 | 20 | 24 | fits | 120,450 | 143 | 0.471 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,178,408 | 61.784 | 20 | 24 | MISS ceiling | 137,967 | 106 | 0.412 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 155,210 | 1.552 | 20 | 50 | fits | 158,051 | 201 | 0.290 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 275,264 | 2.753 | 20 | 50 | fits | 120,450 | 143 | 0.471 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 405,086 | 4.051 | 20 | 20 | fits | 129,888 | 82 | 0.688 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 734,553 | 7.346 | 20 | 20 | fits | 65,312 | 24 | 0.704 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 6,696 | 0.067 | 20 | 20 | fits | 27,276 | 13 (29) | 0.716 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 9,209 | 0.092 | 20 | 20 | fits | 31,202 | 19 (35) | 0.775 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 23,029 | 0.230 | 20 | 20 | fits | 33,751 | 21 (12) | 0.796 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 14,487 | 0.145 | 20 | 50 | fits | 32,612 | 43 | 0.671 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 24,296 | 0.243 | 20 | 50 | fits | 29,286 | 35 | 0.618 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 15,421 | 0.154 | 20 | 50 | fits | 29,298 | 35 | 0.621 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 23,604 | 0.236 | 20 | 50 | fits | 35,393 | 61 | 0.578 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 25,713 | 0.257 | 20 | 50 | fits | 35,393 | 61 | 0.578 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 13,124 | 0.131 | 20 | 50 | fits | 28,386 | 30 | 0.596 |
| LINK_UP | `adp.link_up.if0` | 1,994 | 0.020 | 20 | 200 | fits | 32,612 | 43 (11) | 0.671 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 14,932 | 0.149 | 20 | 200 | fits | 22,596 | 23 (39) | 0.617 |
| LINK_DOWN | `adp.link_down.if0` | 1,637 | 0.016 | 20 | 200 | fits | 29,463 | 23 (9) | 0.686 |
| LINK_UP | `adp.link_up.if0` | 1,994 | 0.020 | 20 | 200 | fits | 32,612 | 43 (11) | 0.671 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 14,932 | 0.149 | 20 | 200 | fits | 22,596 | 23 (39) | 0.617 |
| GM_CHANGE | `adp.gm_change.if0` | 1,841 | 0.018 | 20 | 200 | fits | 17,217 | 17 (11) | 0.400 |
| LINK_UP | `adp.link_up.if0` | 1,994 | 0.020 | 20 | 200 | fits | 32,612 | 43 (11) | 0.671 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 14,932 | 0.149 | 20 | 200 | fits | 22,596 | 23 (39) | 0.617 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,219 | 0.042 | 20 | 200 | fits | 18,633 | 16 (31) | 0.517 |
| LINK_UP | `adp.link_up.if0` | 1,994 | 0.020 | 20 | 200 | fits | 32,612 | 43 (11) | 0.671 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 14,932 | 0.149 | 20 | 200 | fits | 22,596 | 23 (39) | 0.617 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,219 | 0.042 | 20 | 200 | fits | 18,633 | 16 (31) | 0.517 |
| set_name | `aecp_fanout.set_name.if0` | 55,921 | 0.559 | 20 | 24 | fits | 58,875 | 89 | 0.554 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 49,749 | 0.497 | 20 | 24 | fits | 52,939 | 78 | 0.586 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 51,904 | 0.519 | 20 | 24 | fits | 47,949 | 79 | 0.544 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 50,973 | 0.510 | 20 | 24 | fits | 47,688 | 78 | 0.539 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 47,943 | 0.479 | 20 | 24 | fits | 51,220 | 67 | 0.581 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 51,013 | 0.510 | 20 | 24 | fits | 47,588 | 78 | 0.545 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 46,642 | 0.466 | 20 | 24 | fits | 46,361 | 79 | 0.516 |
| BIND_RX | `acmp.bind_rx.if0` | 19,214 | 0.192 | 20 | 20 | fits | 44,780 | 26 (77) | 0.770 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 10,717 | 0.107 | 20 | 20 | fits | 34,219 | 19 (32) | 0.821 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,212 | 0.102 | 20 | 20 | fits | 27,447 | 15 (47) | 0.707 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 15,793 | 0.158 | 20 | 20 | fits | 42,351 | 18 (50) | 0.833 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,517 | 0.105 | 20 | 20 | fits | 27,728 | 17 (48) | 0.683 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,263 | 0.093 | 20 | 20 | fits | 27,075 | 16 (48) | 0.648 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 8,681 | 0.087 | 20 | 20 | fits | 25,879 | 16 (48) | 0.619 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 10,068 | 0.101 | 20 | 20 | fits | 27,382 | 16 (48) | 0.712 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 18,146 | 0.181 | 20 | 24 | fits | 28,693 | 20 | 0.760 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 28,158 | 0.282 | 20 | 24 | fits | 32,385 | 20 | 0.678 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 21,561 | 0.216 | 20 | 24 | fits | 28,790 | 20 | 0.701 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 24,570 | 0.246 | 20 | 24 | fits | 28,262 | 20 | 0.695 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 24,948 | 0.249 | 20 | 24 | fits | 28,911 | 20 | 0.693 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 21,726 | 0.217 | 20 | 24 | fits | 29,003 | 20 | 0.695 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 24,583 | 0.246 | 20 | 24 | fits | 28,275 | 20 | 0.699 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 20,721 | 0.207 | 20 | 24 | fits | 27,764 | 20 | 0.706 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 24,644 | 0.246 | 20 | 24 | fits | 28,412 | 20 | 0.721 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 29,625 | 0.296 | 20 | 24 | fits | 33,793 | 21 | 0.620 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 20,671 | 0.207 | 20 | 24 | fits | 27,930 | 20 | 0.733 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 24,209 | 0.242 | 20 | 24 | fits | 27,977 | 20 | 0.740 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 20,833 | 0.208 | 20 | 24 | fits | 27,955 | 20 | 0.696 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 25,161 | 0.252 | 20 | 24 | fits | 29,008 | 20 | 0.707 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 23,622 | 0.236 | 20 | 24 | fits | 28,516 | 20 | 0.695 |
| get_configuration | `aecp.get_configuration.if0` | 19,225 | 0.192 | 20 | 24 | fits | 26,002 | 20 | 0.721 |
| entity_available | `aecp.entity_available.if0` | 22,389 | 0.224 | 20 | 24 | fits | 25,654 | 20 | 0.702 |
| get_name | `aecp.get_name.if0` | 21,403 | 0.214 | 20 | 24 | fits | 28,829 | 20 | 0.730 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 26,435 | 0.264 | 20 | 24 | fits | 30,147 | 26 | 0.706 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 21,953 | 0.220 | 20 | 24 | fits | 29,416 | 29 | 0.724 |
| get_as_path, refused ENTITY_MISBEHAVING | `aecp.get_as_path.if0` | 12,076 | 0.121 | 20 | 24 | fits | 29,234 | 28 | 0.747 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 23,441 | 0.234 | 20 | 24 | fits | 26,393 | 20 | 0.741 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 18,396 | 0.184 | 20 | 24 | fits | 25,277 | 20 | 0.693 |
| set_name | `aecp.set_name.if0` | 31,847 | 0.318 | 20 | 24 | fits | 46,126 | 43 | 0.745 |
| lock_entity | `aecp.lock_entity.if0` | 24,079 | 0.241 | 20 | 24 | fits | 35,097 | 34 | 0.759 |
| unlock_entity | `aecp.unlock_entity.if0` | 24,983 | 0.250 | 20 | 24 | fits | 35,549 | 33 | 0.774 |
| READ_DESCRIPTOR held for a token (#917) | `aecp.held.read_descriptor.if0` | 523,480 | 5.235 | 20 | 24 | fits | 32,822 | 17 | 0.705 |
| LINK_UP | `fixture.link_up.if0` | 1,994 | 0.020 | 20 | 200 | fits | 32,612 | 43 (11) | 0.671 |
| malformed MRPDU discard | `fixture.malformed.if0` | 23,311 | 0.233 | 20 | 20 | fits | 23,377 | 12 | 0.714 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 32,668 | 0.327 | 20 | 24 | fits | 46,967 | 43 | 0.756 |
| LINK_DOWN | `fixture.link_down.if0` | 2,029 | 0.020 | 20 | 200 | fits | 31,125 | 23 (9) | 0.733 |
| BIND_RX | `fixture.bind_rx.if0` | 19,327 | 0.193 | 20 | 20 | fits | 44,286 | 26 (77) | 0.775 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 21,265 | 0.213 | 20 | 20 | fits | 44,887 | 35 (35) | 0.769 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 9,307 | 0.093 | 20 | 20 | fits | 28,485 | 13 (29) | 0.766 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 91,300 | 0.913 | 20 | 200 | fits | 91,404 | 75 | 0.738 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 91,300 | 0.913 | 20 | 200 | fits | 91,404 | 75 | 0.738 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 91,026 | 0.910 | 20 | 20 | fits | 91,404 | 75 | 0.738 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 91,026 | 0.910 | 20 | 20 | fits | 91,404 | 75 | 0.738 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 91,234 | 0.912 | 20 | 24 | fits | 91,404 | 75 | 0.738 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 91,234 | 0.912 | 20 | 24 | fits | 91,404 | 75 | 0.738 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 91,168 | 0.912 | 20 | 50 | fits | 91,404 | 75 | 0.738 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 91,168 | 0.912 | 20 | 50 | fits | 91,404 | 75 | 0.738 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 91,102 | 0.911 | 20 | 20 | fits | 91,404 | 75 | 0.738 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 91,102 | 0.911 | 20 | 20 | fits | 91,404 | 75 | 0.738 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
