Original file: <scratch>/budget/final/8x8-1if/table.md
Original size: 186923 bytes
Original sha256: b23ecd7fc7dcf3116a4de5cd3ac945b9f0fb7dea5d5193b9034c42fd34135911

TRUNCATED at 177870 of 186923 bytes (the original is kept in scratch, its sha256 above)

### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 85 paths and 7 of 947 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.221 (0.485) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.111 (0.311) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.097 (0.338) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.174 (0.622) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.109 (0.312) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.100 (0.295) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.110 (0.304) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.108 (0.313) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.107 (0.363) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.306 (0.753) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.259 (0.704) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.331 (0.644) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.297 (0.606) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.106 (0.612) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.268 (0.607) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.160 (0.445) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.059 (0.217) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.031 (0.216) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.032 (0.332) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.035 (0.345) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.086 (0.294) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.255 (0.666) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.274 (0.671) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.198 (0.592) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.213 (0.606) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.246 (0.645) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.289 (0.689) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.249 (0.742) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.272 (0.669) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.337 (0.742) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.285 (0.691) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.284 (0.688) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.238 (0.636) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.339 (0.742) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.233 (0.632) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.292 (0.698) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.238 (0.649) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.287 (0.693) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.240 (0.638) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.294 (0.698) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.292 (0.697) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.244 (0.644) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.294 (0.699) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.222 (0.619) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.340 (0.846) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.217 (0.609) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.339 (0.791) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.505 (0.845) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.580 (0.942) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.503 (0.847) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.591 (0.980) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.513 (0.878) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.543 (0.879) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.834 (5.122) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 4.960 (5.429) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.206 (0.649) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.675 (2.155) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.546 (63.940) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.578 (64.766) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.355 (0.511) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 3.194 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.652 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 3.124 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 2.021 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.521 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.136 (0.351) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.118 (0.286) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.141 (0.345) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.116 (0.351) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.285 (0.684) | fits | 0 events | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.830 | fits | 0 srp | 6 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.285 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.389 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.328 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 5.441 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.306 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.024 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.311 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 5.478 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-6.service.srp.first.if0` (backlog-adp@verify-aged2-6) | 6.440 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-6.service.srp.last.if0` (backlog-adp@verify-aged2-6) | 10.300 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.795 (0.839) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.456 (0.457) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.251 (0.252) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.811 (0.885) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.500 | 11 | 155,871 (1.559) | yes | - |
| backlog-adp@blank-1 | 0 | 10.795 | 10 | 157,706 (1.577) | yes | - |
| backlog-adp@blank-2 | 0 | 10.775 | 10 | 155,851 (1.559) | yes | - |
| backlog-adp@blank-3 | 0 | 10.744 | 10 | 154,723 (1.547) | yes | - |
| backlog-adp@blank-4 | 0 | 10.700 | 10 | 156,200 (1.562) | yes | - |
| backlog-adp@blank-5 | 0 | 11.288 | 12 | 152,096 (1.521) | yes | - |
| backlog-adp@blank-6 | 0 | 10.867 | 11 | 156,793 (1.568) | yes | - |
| backlog-adp@blank-7 | 0 | 10.781 | 10 | 156,262 (1.563) | yes | - |
| backlog-adp@program-0 | 0 | 10.902 | 10 | 154,698 (1.547) | yes | - |
| backlog-adp@program-1 | 0 | 10.874 | 10 | 151,900 (1.519) | yes | - |
| backlog-adp@program-2 | 0 | 11.141 | 11 | 155,768 (1.558) | yes | - |
| backlog-adp@program-3 | 0 | 10.910 | 10 | 155,776 (1.558) | yes | - |
| backlog-adp@program-4 | 0 | 10.036 | 10 | 156,092 (1.561) | yes | - |
| backlog-adp@program-5 | 0 | 10.390 | 12 | 155,686 (1.557) | yes | - |
| backlog-adp@program-6 | 0 | 10.005 | 10 | 156,938 (1.569) | yes | - |
| backlog-adp@program-7 | 0 | 9.975 | 10 | 156,691 (1.567) | yes | - |
| backlog-adp@verify-0 | 0 | 11.243 | 11 | 155,794 (1.558) | yes | - |
| backlog-adp@verify-1 | 0 | 10.736 | 10 | 155,933 (1.559) | yes | - |
| backlog-adp@verify-2 | 0 | 10.708 | 10 | 154,805 (1.548) | yes | - |
| backlog-adp@verify-3 | 0 | 10.688 | 10 | 155,943 (1.559) | yes | - |
| backlog-adp@verify-4 | 0 | 10.656 | 9 | 157,192 (1.572) | yes | - |
| backlog-adp@verify-5 | 0 | 10.879 | 10 | 159,143 (1.591) | yes | - |
| backlog-adp@verify-6 | 0 | 10.992 | 11 | 154,681 (1.547) | yes | - |
| backlog-adp@verify-7 | 0 | 10.722 | 10 | 155,649 (1.556) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 11.667 | 10 | 157,972 (1.580) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 10.794 | 10 | 152,524 (1.525) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 10.774 | 10 | 159,454 (1.595) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 10.893 | 11 | 155,728 (1.557) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 10.717 | 10 | 155,861 (1.559) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 10.715 | 10 | 156,771 (1.568) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 10.721 | 10 | 156,652 (1.567) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 10.683 | 10 | 150,608 (1.506) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 11.827 | 11 | 154,650 (1.546) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 10.672 | 10 | 155,788 (1.558) | yes | - |
| backlog-adp@blank-aged1-2 | 1 | 10.647 | 9 | 157,037 (1.570) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 11.567 | 11 | 152,437 (1.524) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 11.128 | 11 | 151,360 (1.514) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 11.135 | 12 | 155,100 (1.551) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 10.785 | 10 | 154,859 (1.549) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 10.765 | 10 | 155,512 (1.555) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.581 | 13 | 152,698 (1.527) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 10.956 | 11 | 155,673 (1.557) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 10.920 | 11 | 154,650 (1.546) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 10.753 | 10 | 154,723 (1.547) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 10.741 | 10 | 155,861 (1.559) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 10.727 | 10 | 157,302 (1.573) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 10.729 | 10 | 151,149 (1.511) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 10.725 | 10 | 152,059 (1.521) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 10.874 | 9 | 158,376 (1.584) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.677 | 9 | 150,925 (1.509) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 10.674 | 9 | 151,492 (1.515) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 10.826 | 10 | 151,109 (1.511) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 10.837 | 10 | 155,778 (1.558) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 10.827 | 10 | 153,582 (1.536) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 10.814 | 10 | 154,859 (1.549) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 10.782 | 10 | 155,955 (1.560) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.792 | 11 | 155,969 (1.560) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 10.543 | 10 | 155,870 (1.559) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 10.714 | 10 | 156,780 (1.568) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 10.700 | 10 | 157,715 (1.577) | yes | - |
| backlog-adp@verify-aged2-4 | 1 | 10.665 | 9 | 156,199 (1.562) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 11.163 | 11 | 151,912 (1.519) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 10.969 | 11 | 155,826 (1.558) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 10.770 | 10 | 155,790 (1.558) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 12.165 | 12 | 152,667 (1.527) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 10.929 | 11 | 158,466 (1.585) | yes | - |
| backlog-adp@verify-aged1-2 | 1 | 10.796 | 10 | 157,855 (1.579) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 10.787 | 10 | 155,943 (1.559) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 10.785 | 10 | 156,853 (1.569) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 10.789 | 10 | 157,073 (1.571) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 10.770 | 10 | 158,951 (1.590) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 12.480 | 12 | 151,185 (1.512) | yes | - |
| backlog | 0 | 6.647 | 8 | 153,878 (1.539) | yes | - |
| backlog-adp | 0 | 9.668 | 9 | 159,029 (1.590) | yes | - |
| backlog-adp-refill | 0 | 41.066 | 24 | 155,064 (1.551) | yes | - |
| backlog-owed | 0 | 65.411 | 24 | 156,004 (1.560) | yes | - |
| fixture | 0 | 1.475 | 2 | 85,485 (0.855) | yes | - |

Composed maximum over the 4 backlog windows: 159,029 CPU cycles (1.590 ms), backlog-adp.
Over the windows that released their whole load only: 159,029 (1.590 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 116556 | 0 | 55,688 (0.557) | fits |
| save-held | 3142 | 0 | 163,618 (1.636) | fits |
| save-starved | 55697 | 0 | 163,618 (1.636) | fits |
| acmp-notk | 3357 | 0 | 48,215 (0.482) | fits |
| backlog-adp@blank-0 | 556 | 0 | 155,871 (1.559) | fits |
| backlog-adp@blank-1 | 557 | 0 | 157,706 (1.577) | fits |
| backlog-adp@blank-2 | 557 | 0 | 155,851 (1.559) | fits |
| backlog-adp@blank-3 | 557 | 0 | 154,723 (1.547) | fits |
| backlog-adp@blank-4 | 557 | 0 | 156,200 (1.562) | fits |
| backlog-adp@blank-5 | 559 | 0 | 152,096 (1.521) | fits |
| backlog-adp@blank-6 | 558 | 0 | 156,793 (1.568) | fits |
| backlog-adp@blank-7 | 559 | 0 | 156,262 (1.563) | fits |
| backlog-adp@program-0 | 940 | 0 | 154,698 (1.547) | fits |
| backlog-adp@program-1 | 940 | 0 | 151,900 (1.519) | fits |
| backlog-adp@program-2 | 941 | 0 | 155,768 (1.558) | fits |
| backlog-adp@program-3 | 942 | 0 | 155,776 (1.558) | fits |
| backlog-adp@program-4 | 943 | 0 | 156,092 (1.561) | fits |
| backlog-adp@program-5 | 945 | 0 | 155,686 (1.557) | fits |
| backlog-adp@program-6 | 945 | 0 | 156,938 (1.569) | fits |
| backlog-adp@program-7 | 945 | 0 | 156,691 (1.567) | fits |
| backlog-adp@verify-0 | 1316 | 0 | 155,794 (1.558) | fits |
| backlog-adp@verify-1 | 1317 | 0 | 155,933 (1.559) | fits |
| backlog-adp@verify-2 | 1317 | 0 | 154,805 (1.548) | fits |
| backlog-adp@verify-3 | 1317 | 0 | 155,943 (1.559) | fits |
| backlog-adp@verify-4 | 1317 | 0 | 157,192 (1.572) | fits |
| backlog-adp@verify-5 | 1317 | 0 | 159,143 (1.591) | fits |
| backlog-adp@verify-6 | 1318 | 0 | 154,681 (1.547) | fits |
| backlog-adp@verify-7 | 1319 | 0 | 155,649 (1.556) | fits |
| backlog-adp@blank-aged2-0 | 789 | 0 | 157,972 (1.580) | fits |
| backlog-adp@blank-aged2-1 | 795 | 0 | 152,524 (1.525) | fits |
| backlog-adp@blank-aged2-2 | 801 | 0 | 159,454 (1.595) | fits |
| backlog-adp@blank-aged2-3 | 808 | 0 | 155,728 (1.557) | fits |
| backlog-adp@blank-aged2-4 | 813 | 0 | 155,861 (1.559) | fits |
| backlog-adp@blank-aged2-5 | 819 | 0 | 156,771 (1.568) | fits |
| backlog-adp@blank-aged2-6 | 825 | 0 | 156,652 (1.567) | fits |
| backlog-adp@blank-aged2-7 | 831 | 0 | 150,608 (1.506) | fits |
| backlog-adp@blank-aged1-0 | 741 | 0 | 154,650 (1.546) | fits |
| backlog-adp@blank-aged1-1 | 746 | 0 | 155,788 (1.558) | fits |
| backlog-adp@blank-aged1-2 | 752 | 0 | 157,037 (1.570) | fits |
| backlog-adp@blank-aged1-3 | 760 | 0 | 152,437 (1.524) | fits |
| backlog-adp@blank-aged1-4 | 766 | 0 | 153,153 (1.532) | fits |
| backlog-adp@blank-aged1-5 | 773 | 0 | 155,100 (1.551) | fits |
| backlog-adp@blank-aged1-6 | 777 | 0 | 154,859 (1.549) | fits |
| backlog-adp@blank-aged1-7 | 783 | 0 | 155,512 (1.555) | fits |
| backlog-adp@program-aged2-0 | 1171 | 0 | 152,698 (1.527) | fits |
| backlog-adp@program-aged2-1 | 1175 | 0 | 155,673 (1.557) | fits |
| backlog-adp@program-aged2-2 | 1181 | 0 | 154,650 (1.546) | fits |
| backlog-adp@program-aged2-3 | 1186 | 0 | 154,723 (1.547) | fits |
| backlog-adp@program-aged2-4 | 1192 | 0 | 155,861 (1.559) | fits |
| backlog-adp@program-aged2-5 | 1198 | 0 | 157,302 (1.573) | fits |
| backlog-adp@program-aged2-6 | 1204 | 0 | 151,149 (1.511) | fits |
| backlog-adp@program-aged2-7 | 1210 | 0 | 152,059 (1.521) | fits |
| backlog-adp@program-aged1-0 | 1119 | 0 | 158,376 (1.584) | fits |
| backlog-adp@program-aged1-1 | 1125 | 0 | 153,149 (1.531) | fits |
| backlog-adp@program-aged1-2 | 1131 | 0 | 153,149 (1.531) | fits |
| backlog-adp@program-aged1-3 | 1138 | 0 | 153,342 (1.533) | fits |
| backlog-adp@program-aged1-4 | 1144 | 0 | 155,778 (1.558) | fits |
| backlog-adp@program-aged1-5 | 1150 | 0 | 153,582 (1.536) | fits |
| backlog-adp@program-aged1-6 | 1156 | 0 | 154,859 (1.549) | fits |
| backlog-adp@program-aged1-7 | 1162 | 0 | 155,955 (1.560) | fits |
| backlog-adp@verify-aged2-0 | 1548 | 0 | 155,969 (1.560) | fits |
| backlog-adp@verify-aged2-1 | 1553 | 0 | 155,870 (1.559) | fits |
| backlog-adp@verify-aged2-2 | 1559 | 0 | 156,780 (1.568) | fits |
| backlog-adp@verify-aged2-3 | 1565 | 0 | 157,715 (1.577) | fits |
| backlog-adp@verify-aged2-4 | 1571 | 0 | 156,199 (1.562) | fits |
| backlog-adp@verify-aged2-5 | 1579 | 0 | 152,845 (1.528) | fits |
| backlog-adp@verify-aged2-6 | 1585 | 0 | 155,826 (1.558) | fits |
| backlog-adp@verify-aged2-7 | 1590 | 0 | 155,790 (1.558) | fits |
| backlog-adp@verify-aged1-0 | 1501 | 0 | 152,667 (1.527) | fits |
| backlog-adp@verify-aged1-1 | 1506 | 0 | 158,466 (1.585) | fits |
| backlog-adp@verify-aged1-2 | 1511 | 0 | 157,855 (1.579) | fits |
| backlog-adp@verify-aged1-3 | 1517 | 0 | 155,943 (1.559) | fits |
| backlog-adp@verify-aged1-4 | 1523 | 0 | 156,853 (1.569) | fits |
| backlog-adp@verify-aged1-5 | 1529 | 0 | 157,073 (1.571) | fits |
| backlog-adp@verify-aged1-6 | 1535 | 0 | 158,951 (1.590) | fits |
| backlog-adp@verify-aged1-7 | 1543 | 0 | 151,185 (1.512) | fits |
| adp-advertise | 598 | 0 | 35,076 (0.351) | fits |
| acmp-noresp | 1881 | 0 | 48,215 (0.482) | fits |
| save | 610 | 0 | 49,753 (0.498) | fits |
| srp | 290 | 0 | 45,663 (0.457) | fits |
| backlog | 287 | 0 | 153,878 (1.539) | fits |
| backlog-adp | 311 | 0 | 159,029 (1.590) | fits |
| backlog-adp-refill | 326 | 0 | 155,064 (1.551) | fits |
| backlog-owed | 309 | 0 | 156,004 (1.560) | fits |
| acmp-disc | 876 | 0 | 48,215 (0.482) | fits |
| maap | 179 | 0 | 35,076 (0.351) | fits |
| adp-link | 89 | 0 | 45,477 (0.455) | fits |
| adp-gm | 88 | 0 | 34,462 (0.345) | fits |
| adp-discover | 88 | 0 | 34,462 (0.345) | fits |
| control | 88 | 0 | 34,462 (0.345) | fits |
| aecp-fanout | 107 | 0 | 62,085 (0.621) | fits |
| acmp-cmd | 87 | 0 | 48,215 (0.482) | fits |
| aecp | 112 | 0 | 49,263 (0.493) | fits |
| datapath-events | 116 | 0 | 34,462 (0.345) | fits |
| fixture | 159 | 0 | 85,485 (0.855) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 9.034 (20) | 10.966 |
| backlog-adp@blank-aged2-1 | 2 | +8.970 ms, 76,849 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 10.120 (20) | 9.880 |
| backlog-adp@blank-aged2-2 | 2 | +8.191 ms, 76,849 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 10.100 (20) | 9.900 |
| backlog-adp@blank-aged2-3 | 2 | +6.460 ms, 76,763 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 10.224 (20) | 9.776 |
| backlog-adp@blank-aged2-4 | 2 | +5.516 ms, 76,815 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 10.048 (20) | 9.952 |
| backlog-adp@blank-aged2-5 | 2 | +5.511 ms, 76,815 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 10.046 (20) | 9.954 |
| backlog-adp@blank-aged2-6 | 2 | +4.594 ms, 77,077 (0.771 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 10.054 (20) | 9.946 |
| backlog-adp@blank-aged2-7 | 2 | +3.009 ms, 76,972 (0.770 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 10.014 (20) | 9.986 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 9.197 (20) | 10.803 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 9.238 (20) | 10.762 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 9.212 (20) | 10.788 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 9.209 (20) | 10.791 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 9.187 (20) | 10.813 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 9.350 (20) | 10.650 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 9.353 (20) | 10.647 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 9.333 (20) | 10.667 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 9.256 (20) | 10.744 |
| backlog-adp@program-aged2-1 | 2 | +8.995 ms, 80,945 (0.809 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 10.146 (20) | 9.854 |
| backlog-adp@program-aged2-2 | 2 | none | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 10.251 (20) | 9.749 |
| backlog-adp@program-aged2-3 | 2 | none | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 10.084 (20) | 9.916 |
| backlog-adp@program-aged2-4 | 2 | none | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 10.072 (20) | 9.928 |
| backlog-adp@program-aged2-5 | 2 | +5.567 ms, 80,860 (0.809 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 10.055 (20) | 9.945 |
| backlog-adp@program-aged2-6 | 2 | +4.655 ms, 80,822 (0.808 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 10.059 (20) | 9.941 |
| backlog-adp@program-aged2-7 | 2 | none | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 10.052 (20) | 9.948 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 8.900 (20) | 11.100 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 9.189 (20) | 10.811 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 9.185 (20) | 10.815 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 9.341 (20) | 10.659 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 9.354 (20) | 10.646 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 9.344 (20) | 10.656 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 9.331 (20) | 10.669 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 9.296 (20) | 10.704 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 8.981 (20) | 11.019 |
| backlog-adp@verify-aged2-1 | 2 | none | +9.320 ms, 77,501 (0.775 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 9.283 (20) | 10.717 |
| backlog-adp@verify-aged2-2 | 2 | +8.039 ms, 77,504 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 10.043 (20) | 9.957 |
| backlog-adp@verify-aged2-3 | 2 | +7.182 ms, 77,504 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 10.029 (20) | 9.971 |
| backlog-adp@verify-aged2-4 | 2 | +5.539 ms, 77,650 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 9.994 (20) | 10.006 |
| backlog-adp@verify-aged2-5 | 2 | +5.526 ms, 77,535 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 9.980 (20) | 10.020 |
| backlog-adp@verify-aged2-6 | 2 | +4.837 ms, 77,794 (0.778 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 10.300 (20) | 9.700 |
| backlog-adp@verify-aged2-7 | 2 | +3.081 ms, 77,797 (0.778 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 10.101 (20) | 9.899 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 9.151 (20) | 10.849 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 8.884 (20) | 11.116 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 9.214 (20) | 10.786 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 9.347 (20) | 10.653 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 9.345 (20) | 10.655 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 9.345 (20) | 10.655 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 9.328 (20) | 10.672 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 9.313 (20) | 10.687 |

Least margin over the aged windows: 9.700 ms, `backlog-adp@verify-aged2-6.service.srp.last.if0` at 10.300 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 22829.734 | 22,870 | 382 | 2 | 31.326 | yes | within |
| save-held | 4817.315 | 12,470 | 382 | - | 15.242 | no | within |
| save-starved | 12447.272 | 12,470 | 382 | - | 32.661 | yes | within |
| save | 4817.754 | 12,470 | 382 | - | 10.904 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1080 | 80,885 (0.809) | 77,829 (0.778) |
| save-held | 1562 | 101,030 (1.010) | 78,308 (0.783) |
| save-starved | 698 | 81,704 (0.817) | 78,336 (0.783) |
| acmp-notk | 1065 | 109,693 (1.097) | 78,268 (0.783) |
| backlog-adp@blank-0 | 339 | 95,854 (0.959) | 75,996 (0.760) |
| backlog-adp@blank-1 | 339 | 96,998 (0.970) | 76,073 (0.761) |
| backlog-adp@blank-2 | 339 | 96,899 (0.969) | 76,073 (0.761) |
| backlog-adp@blank-3 | 339 | 96,899 (0.969) | 76,073 (0.761) |
| backlog-adp@blank-4 | 339 | 97,164 (0.972) | 76,073 (0.761) |
| backlog-adp@blank-5 | 339 | 97,306 (0.973) | 76,073 (0.761) |
| backlog-adp@blank-6 | 339 | 99,789 (0.998) | 76,305 (0.763) |
| backlog-adp@blank-7 | 339 | 96,863 (0.969) | 76,073 (0.761) |
| backlog-adp@program-0 | 448 | 101,200 (1.012) | 78,729 (0.787) |
| backlog-adp@program-1 | 448 | 101,437 (1.014) | 78,729 (0.787) |
| backlog-adp@program-2 | 448 | 101,644 (1.016) | 78,729 (0.787) |
| backlog-adp@program-3 | 448 | 101,023 (1.010) | 78,729 (0.787) |
| backlog-adp@program-4 | 449 | 100,959 (1.010) | 78,135 (0.781) |
| backlog-adp@program-5 | 449 | 100,959 (1.010) | 78,135 (0.781) |
| backlog-adp@program-6 | 449 | 100,959 (1.010) | 78,135 (0.781) |
| backlog-adp@program-7 | 449 | 100,959 (1.010) | 78,135 (0.781) |
| backlog-adp@verify-0 | 555 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-1 | 555 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-2 | 555 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-3 | 555 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-4 | 555 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-5 | 555 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-6 | 555 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-7 | 555 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@blank-aged2-0 | 338 | 97,321 (0.973) | 76,153 (0.762) |
| backlog-adp@blank-aged2-1 | 337 | 80,551 (0.806) | 75,731 (0.757) |
| backlog-adp@blank-aged2-2 | 337 | 80,551 (0.806) | 75,731 (0.757) |
| backlog-adp@blank-aged2-3 | 337 | 80,551 (0.806) | 75,689 (0.757) |
| backlog-adp@blank-aged2-4 | 337 | 80,551 (0.806) | 75,742 (0.757) |
| backlog-adp@blank-aged2-5 | 337 | 80,551 (0.806) | 75,742 (0.757) |
| backlog-adp@blank-aged2-6 | 337 | 80,551 (0.806) | 75,650 (0.756) |
| backlog-adp@blank-aged2-7 | 337 | 80,551 (0.806) | 75,545 (0.755) |
| backlog-adp@blank-aged1-0 | 338 | 96,943 (0.969) | 76,153 (0.762) |
| backlog-adp@blank-aged1-1 | 337 | 97,120 (0.971) | 76,153 (0.762) |
| backlog-adp@blank-aged1-2 | 337 | 97,280 (0.973) | 76,153 (0.762) |
| backlog-adp@blank-aged1-3 | 337 | 97,422 (0.974) | 76,153 (0.762) |
| backlog-adp@blank-aged1-4 | 337 | 104,695 (1.047) | 76,466 (0.765) |
| backlog-adp@blank-aged1-5 | 337 | 95,912 (0.959) | 76,153 (0.762) |
| backlog-adp@blank-aged1-6 | 337 | 96,943 (0.969) | 76,153 (0.762) |
| backlog-adp@blank-aged1-7 | 337 | 96,943 (0.969) | 76,153 (0.762) |
| backlog-adp@program-aged2-0 | 447 | 101,477 (1.015) | 78,729 (0.787) |
| backlog-adp@program-aged2-1 | 446 | 100,959 (1.010) | 78,453 (0.785) |
| backlog-adp@program-aged2-2 | 446 | 100,959 (1.010) | 78,624 (0.786) |
| backlog-adp@program-aged2-3 | 446 | 100,959 (1.010) | 78,624 (0.786) |
| backlog-adp@program-aged2-4 | 446 | 100,959 (1.010) | 78,635 (0.786) |
| backlog-adp@program-aged2-5 | 446 | 100,959 (1.010) | 78,453 (0.785) |
| backlog-adp@program-aged2-6 | 446 | 100,959 (1.010) | 78,185 (0.782) |
| backlog-adp@program-aged2-7 | 446 | 100,959 (1.010) | 78,424 (0.784) |
| backlog-adp@program-aged1-0 | 447 | 101,347 (1.013) | 78,729 (0.787) |
| backlog-adp@program-aged1-1 | 446 | 101,482 (1.015) | 78,729 (0.787) |
| backlog-adp@program-aged1-2 | 446 | 101,513 (1.015) | 78,729 (0.787) |
| backlog-adp@program-aged1-3 | 446 | 101,164 (1.012) | 78,729 (0.787) |
| backlog-adp@program-aged1-4 | 446 | 100,969 (1.010) | 78,729 (0.787) |
| backlog-adp@program-aged1-5 | 446 | 100,969 (1.010) | 78,729 (0.787) |
| backlog-adp@program-aged1-6 | 446 | 100,969 (1.010) | 78,729 (0.787) |
| backlog-adp@program-aged1-7 | 446 | 101,347 (1.013) | 78,729 (0.787) |
| backlog-adp@verify-aged2-0 | 556 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-aged2-1 | 555 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-aged2-2 | 555 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-aged2-3 | 555 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-aged2-4 | 555 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-aged2-5 | 555 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-aged2-6 | 555 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-aged2-7 | 555 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-aged1-0 | 556 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-aged1-1 | 555 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-aged1-2 | 555 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-aged1-3 | 555 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-aged1-4 | 555 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-aged1-5 | 555 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-aged1-6 | 555 | 104,980 (1.050) | 78,135 (0.781) |
| backlog-adp@verify-aged1-7 | 556 | 104,980 (1.050) | 78,135 (0.781) |
| adp-advertise | 577 | 26,967 (0.270) | 2,379 (0.024) |
| acmp-noresp | 615 | 109,461 (1.095) | 78,135 (0.781) |
| save | 585 | 100,627 (1.006) | 77,962 (0.780) |
| srp | 271 | 26,967 (0.270) | 2,379 (0.024) |
| backlog | 265 | 26,967 (0.270) | 2,379 (0.024) |
| backlog-adp | 271 | 26,967 (0.270) | 2,386 (0.024) |
| backlog-adp-refill | 274 | 26,967 (0.270) | 2,386 (0.024) |
| backlog-owed | 277 | 26,967 (0.270) | 2,499 (0.025) |
| acmp-disc | 306 | 109,503 (1.095) | 75,529 (0.755) |
| maap | 166 | 26,967 (0.270) | 2,379 (0.024) |
| adp-link | 79 | 26,967 (0.270) | 2,379 (0.024) |
| adp-gm | 79 | 26,967 (0.270) | 2,379 (0.024) |
| adp-discover | 79 | 26,967 (0.270) | 2,379 (0.024) |
| control | 79 | 26,967 (0.270) | 2,379 (0.024) |
| aecp-fanout | 79 | 26,967 (0.270) | 2,379 (0.024) |
| acmp-cmd | 66 | 26,967 (0.270) | 2,379 (0.024) |
| aecp | 80 | 26,967 (0.270) | 2,379 (0.024) |
| datapath-events | 70 | 26,967 (0.270) | 2,379 (0.024) |
| fixture | 54 | 25,552 (0.256) | 2,405 (0.024) |

Longest pass that carries a step: 109,693 CPU cycles (1.097 ms), acmp-notk; longest step: 78,729 (0.787 ms), backlog-adp@program-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 261,716 | 2.617 | 20 | 200 | fits | 99,038 | 121 | 0.470 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 241,579 | 2.416 | 20 | 20 | fits | 99,038 | 121 | 0.470 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 290,168 | 2.902 | 20 | 24 | fits | 85,529 | 60 | 0.469 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 202,104 | 2.021 | 20 | 50 | fits | 99,038 | 121 | 0.470 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 826,794 | 8.268 | 20 | 20 | fits | 77,922 | 32 | 0.618 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 112,919 | 1.129 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 165,394 | 1.654 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 272,209 | 2.722 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 265,213 | 2.652 | 20 | 200 | fits | 102,535 | 127 | 0.496 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 319,367 | 3.194 | 20 | 20 | fits | 84,215 | 56 | 0.599 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 312,415 | 3.124 | 20 | 24 | fits | 86,989 | 66 | 0.465 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 195,677 | 1.957 | 20 | 50 | fits | 155,483 | 230 | 0.391 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 852,141 | 8.521 | 20 | 20 | fits | 81,022 | 38 | 0.640 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 111,677 | 1.117 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 172,462 | 1.725 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 283,005 | 2.830 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 10,620 | 0.106 | 20 | 20 | fits | 39,817 | 19 (14) | 0.892 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 492,708 | 4.927 | 20 | 20 | fits | 155,871 | 209 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 388,841 | 3.888 | 20 | 200 | fits | 153,340 | 181 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 544,096 | 5.441 | 20 | 200 | fits | 155,871 | 209 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 389,765 | 3.898 | 20 | 20 | fits | 153,340 | 181 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 628,655 | 6.287 | 20 | 20 | fits | 83,855 | 31 | 0.754 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 230,566 | 2.306 | 20 | 24 | fits | 152,726 | 146 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 392,415 | 3.924 | 20 | 24 | fits | 153,340 | 181 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 392,349 | 3.923 | 20 | 50 | fits | 153,340 | 181 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 547,824 | 5.478 | 20 | 50 | fits | 155,871 | 209 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 631,613 | 6.316 | 20 | 20 | fits | 83,855 | 31 | 0.754 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 967,792 | 9.678 | 20 | 20 | fits | 84,341 | 37 | 0.539 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 402,677 | 4.027 | 20 | 20 | fits | 157,706 | 195 | 0.392 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 306,841 | 3.068 | 20 | 200 | fits | 150,830 | 192 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 463,931 | 4.639 | 20 | 200 | fits | 157,706 | 195 | 0.392 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 307,765 | 3.078 | 20 | 20 | fits | 150,830 | 192 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 548,490 | 5.485 | 20 | 20 | fits | 83,855 | 31 | 0.754 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 160,575 | 1.606 | 20 | 24 | fits | 152,337 | 145 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 310,415 | 3.104 | 20 | 24 | fits | 150,830 | 192 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 310,349 | 3.103 | 20 | 50 | fits | 150,830 | 192 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 467,659 | 4.677 | 20 | 50 | fits | 157,706 | 195 | 0.392 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 551,448 | 5.514 | 20 | 20 | fits | 83,855 | 31 | 0.754 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 936,248 | 9.362 | 20 | 20 | fits | 38,965 | 18 | 0.837 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 392,409 | 3.924 | 20 | 20 | fits | 155,851 | 205 | 0.404 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 307,416 | 3.074 | 20 | 200 | fits | 152,714 | 180 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 462,651 | 4.627 | 20 | 200 | fits | 155,851 | 205 | 0.404 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 308,340 | 3.083 | 20 | 20 | fits | 152,714 | 180 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 547,174 | 5.472 | 20 | 20 | fits | 83,819 | 31 | 0.754 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 159,266 | 1.593 | 20 | 24 | fits | 152,096 | 145 | 0.371 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 310,990 | 3.110 | 20 | 24 | fits | 152,714 | 180 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 310,924 | 3.109 | 20 | 50 | fits | 152,714 | 180 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 466,379 | 4.664 | 20 | 50 | fits | 155,851 | 205 | 0.404 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 550,132 | 5.501 | 20 | 20 | fits | 83,819 | 31 | 0.754 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 934,361 | 9.344 | 20 | 20 | fits | 41,479 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 407,627 | 4.076 | 20 | 20 | fits | 154,723 | 204 | 0.393 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 306,020 | 3.060 | 20 | 200 | fits | 152,700 | 180 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 460,127 | 4.601 | 20 | 200 | fits | 154,723 | 204 | 0.393 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 306,944 | 3.069 | 20 | 20 | fits | 152,700 | 180 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 544,752 | 5.448 | 20 | 20 | fits | 83,921 | 32 | 0.752 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 157,884 | 1.579 | 20 | 24 | fits | 152,096 | 145 | 0.371 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 309,594 | 3.096 | 20 | 24 | fits | 152,700 | 180 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 309,528 | 3.095 | 20 | 50 | fits | 152,700 | 180 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 463,855 | 4.639 | 20 | 50 | fits | 154,723 | 204 | 0.393 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 547,710 | 5.477 | 20 | 20 | fits | 83,921 | 32 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 931,242 | 9.312 | 20 | 20 | fits | 41,479 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 406,800 | 4.068 | 20 | 20 | fits | 156,200 | 210 | 0.387 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 302,943 | 3.029 | 20 | 200 | fits | 151,005 | 176 | 0.406 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 458,527 | 4.585 | 20 | 200 | fits | 156,200 | 210 | 0.387 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 303,867 | 3.039 | 20 | 20 | fits | 151,005 | 176 | 0.406 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 554,610 | 5.546 | 20 | 20 | fits | 84,844 | 42 | 0.773 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 156,502 | 1.565 | 20 | 24 | fits | 152,096 | 145 | 0.371 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 306,517 | 3.065 | 20 | 24 | fits | 151,005 | 176 | 0.406 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 306,451 | 3.065 | 20 | 50 | fits | 151,005 | 176 | 0.406 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 462,255 | 4.623 | 20 | 50 | fits | 156,200 | 210 | 0.387 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 557,568 | 5.576 | 20 | 20 | fits | 84,844 | 42 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 926,604 | 9.266 | 20 | 20 | fits | 32,889 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 419,391 | 4.194 | 20 | 20 | fits | 151,031 | 191 | 0.458 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 301,567 | 3.016 | 20 | 200 | fits | 151,011 | 193 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 462,110 | 4.621 | 20 | 200 | fits | 151,031 | 191 | 0.458 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 302,491 | 3.025 | 20 | 20 | fits | 151,011 | 193 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 548,100 | 5.481 | 20 | 20 | fits | 85,286 | 42 | 0.704 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 155,120 | 1.551 | 20 | 24 | fits | 152,096 | 145 | 0.371 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 305,141 | 3.051 | 20 | 24 | fits | 151,011 | 193 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 305,075 | 3.051 | 20 | 50 | fits | 151,011 | 193 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 465,838 | 4.658 | 20 | 50 | fits | 151,031 | 191 | 0.458 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 551,058 | 5.511 | 20 | 20 | fits | 85,286 | 42 | 0.704 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 928,516 | 9.285 | 20 | 20 | fits | 41,479 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 416,287 | 4.163 | 20 | 20 | fits | 156,793 | 191 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 311,869 | 3.119 | 20 | 200 | fits | 153,123 | 197 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 468,046 | 4.680 | 20 | 200 | fits | 156,793 | 191 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 312,793 | 3.128 | 20 | 20 | fits | 153,123 | 197 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 553,047 | 5.530 | 20 | 20 | fits | 84,297 | 37 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 153,958 | 1.540 | 20 | 24 | fits | 152,316 | 146 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 315,443 | 3.154 | 20 | 24 | fits | 153,123 | 197 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 315,377 | 3.154 | 20 | 50 | fits | 153,123 | 197 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 471,774 | 4.718 | 20 | 50 | fits | 156,793 | 191 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 556,005 | 5.560 | 20 | 20 | fits | 84,297 | 37 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 929,739 | 9.297 | 20 | 20 | fits | 37,708 | 19 | 0.821 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 408,868 | 4.089 | 20 | 20 | fits | 156,262 | 207 | 0.389 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 305,239 | 3.052 | 20 | 200 | fits | 150,026 | 174 | 0.430 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 460,885 | 4.609 | 20 | 200 | fits | 156,262 | 207 | 0.389 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 306,163 | 3.062 | 20 | 20 | fits | 150,026 | 174 | 0.430 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 545,780 | 5.458 | 20 | 20 | fits | 84,191 | 37 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 159,777 | 1.598 | 20 | 24 | fits | 152,158 | 145 | 0.372 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 308,813 | 3.088 | 20 | 24 | fits | 150,026 | 174 | 0.430 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 308,747 | 3.087 | 20 | 50 | fits | 150,026 | 174 | 0.430 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 464,613 | 4.646 | 20 | 50 | fits | 156,262 | 207 | 0.389 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 548,738 | 5.487 | 20 | 20 | fits | 84,191 | 37 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 935,017 | 9.350 | 20 | 20 | fits | 41,645 | 16 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 418,403 | 4.184 | 20 | 20 | fits | 154,698 | 204 | 0.392 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 316,821 | 3.168 | 20 | 200 | fits | 152,846 | 180 | 0.404 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 470,903 | 4.709 | 20 | 200 | fits | 154,698 | 204 | 0.392 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 317,745 | 3.177 | 20 | 20 | fits | 152,846 | 180 | 0.404 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 554,823 | 5.548 | 20 | 20 | fits | 83,216 | 31 | 0.752 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 168,539 | 1.685 | 20 | 24 | fits | 151,793 | 145 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 320,395 | 3.204 | 20 | 24 | fits | 152,846 | 180 | 0.404 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 320,329 | 3.203 | 20 | 50 | fits | 152,846 | 180 | 0.404 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 474,631 | 4.746 | 20 | 50 | fits | 154,698 | 204 | 0.392 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 557,781 | 5.578 | 20 | 20 | fits | 83,216 | 31 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 941,822 | 9.418 | 20 | 20 | fits | 38,941 | 18 | 0.837 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 412,640 | 4.126 | 20 | 20 | fits | 151,900 | 193 | 0.407 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 312,592 | 3.126 | 20 | 200 | fits | 150,913 | 192 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 463,876 | 4.639 | 20 | 200 | fits | 151,900 | 193 | 0.407 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 313,516 | 3.135 | 20 | 20 | fits | 150,913 | 192 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 560,535 | 5.605 | 20 | 20 | fits | 85,344 | 38 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 166,243 | 1.662 | 20 | 24 | fits | 151,793 | 145 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 316,166 | 3.162 | 20 | 24 | fits | 150,913 | 192 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 316,100 | 3.161 | 20 | 50 | fits | 150,913 | 192 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 467,604 | 4.676 | 20 | 50 | fits | 151,900 | 193 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 563,493 | 5.635 | 20 | 20 | fits | 85,344 | 38 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 938,781 | 9.388 | 20 | 20 | fits | 41,479 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 409,076 | 4.091 | 20 | 20 | fits | 155,768 | 205 | 0.402 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 324,166 | 3.242 | 20 | 200 | fits | 155,073 | 185 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 479,318 | 4.793 | 20 | 200 | fits | 155,768 | 205 | 0.402 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 325,090 | 3.251 | 20 | 20 | fits | 155,073 | 185 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 569,790 | 5.698 | 20 | 20 | fits | 89,768 | 39 | 0.748 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 164,131 | 1.641 | 20 | 24 | fits | 151,977 | 146 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 327,740 | 3.277 | 20 | 24 | fits | 155,073 | 185 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 327,674 | 3.277 | 20 | 50 | fits | 155,073 | 185 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 483,046 | 4.830 | 20 | 50 | fits | 155,768 | 205 | 0.402 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 572,748 | 5.727 | 20 | 20 | fits | 89,768 | 39 | 0.748 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 909,020 | 9.090 | 20 | 20 | fits | 84,300 | 36 | 0.539 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 417,955 | 4.180 | 20 | 20 | fits | 155,776 | 208 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 314,061 | 3.141 | 20 | 200 | fits | 149,981 | 174 | 0.430 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 469,221 | 4.692 | 20 | 200 | fits | 155,776 | 208 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 314,985 | 3.150 | 20 | 20 | fits | 149,981 | 174 | 0.430 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 553,477 | 5.535 | 20 | 20 | fits | 83,552 | 37 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 168,644 | 1.686 | 20 | 24 | fits | 152,052 | 145 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 317,635 | 3.176 | 20 | 24 | fits | 149,981 | 174 | 0.430 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 317,569 | 3.176 | 20 | 50 | fits | 149,981 | 174 | 0.430 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 472,949 | 4.729 | 20 | 50 | fits | 155,776 | 208 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 556,435 | 5.564 | 20 | 20 | fits | 83,552 | 37 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 942,802 | 9.428 | 20 | 20 | fits | 41,479 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 398,885 | 3.989 | 20 | 20 | fits | 156,092 | 206 | 0.405 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 313,990 | 3.140 | 20 | 200 | fits | 152,860 | 180 | 0.404 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 469,466 | 4.695 | 20 | 200 | fits | 156,092 | 206 | 0.405 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 314,914 | 3.149 | 20 | 20 | fits | 152,860 | 180 | 0.404 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 568,216 | 5.682 | 20 | 20 | fits | 87,435 | 38 | 0.759 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 165,694 | 1.657 | 20 | 24 | fits | 152,116 | 145 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 317,564 | 3.176 | 20 | 24 | fits | 152,860 | 180 | 0.404 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 317,498 | 3.175 | 20 | 50 | fits | 152,860 | 180 | 0.404 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 473,194 | 4.732 | 20 | 50 | fits | 156,092 | 206 | 0.405 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 571,174 | 5.712 | 20 | 20 | fits | 87,435 | 38 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 907,348 | 9.073 | 20 | 20 | fits | 84,300 | 36 | 0.539 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 425,897 | 4.259 | 20 | 20 | fits | 155,686 | 209 | 0.382 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 322,215 | 3.222 | 20 | 200 | fits | 153,485 | 181 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 477,285 | 4.773 | 20 | 200 | fits | 155,686 | 209 | 0.382 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 323,139 | 3.231 | 20 | 20 | fits | 153,485 | 181 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 561,651 | 5.617 | 20 | 20 | fits | 83,662 | 31 | 0.756 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 163,786 | 1.638 | 20 | 24 | fits | 152,139 | 146 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 325,789 | 3.258 | 20 | 24 | fits | 153,485 | 181 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 325,723 | 3.257 | 20 | 50 | fits | 153,485 | 181 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 481,013 | 4.810 | 20 | 50 | fits | 155,686 | 209 | 0.382 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 564,609 | 5.646 | 20 | 20 | fits | 83,662 | 31 | 0.756 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 931,470 | 9.315 | 20 | 20 | fits | 32,977 | 13 | 0.813 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 396,389 | 3.964 | 20 | 20 | fits | 156,938 | 196 | 0.380 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 300,942 | 3.009 | 20 | 200 | fits | 150,884 | 192 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 457,264 | 4.573 | 20 | 200 | fits | 156,938 | 196 | 0.380 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 301,866 | 3.019 | 20 | 20 | fits | 150,884 | 192 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 547,613 | 5.476 | 20 | 20 | fits | 89,645 | 39 | 0.747 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 154,622 | 1.546 | 20 | 24 | fits | 151,974 | 145 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 304,516 | 3.045 | 20 | 24 | fits | 150,884 | 192 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 304,450 | 3.045 | 20 | 50 | fits | 150,884 | 192 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 460,992 | 4.610 | 20 | 50 | fits | 156,938 | 196 | 0.380 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 550,571 | 5.506 | 20 | 20 | fits | 89,645 | 39 | 0.747 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 928,215 | 9.282 | 20 | 20 | fits | 32,889 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 401,299 | 4.013 | 20 | 20 | fits | 156,691 | 208 | 0.391 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 297,580 | 2.976 | 20 | 200 | fits | 150,286 | 174 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 453,655 | 4.537 | 20 | 200 | fits | 156,691 | 208 | 0.391 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 298,504 | 2.985 | 20 | 20 | fits | 150,286 | 174 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 552,763 | 5.528 | 20 | 20 | fits | 87,790 | 44 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 151,858 | 1.519 | 20 | 24 | fits | 151,974 | 145 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 301,154 | 3.012 | 20 | 24 | fits | 150,286 | 174 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 301,088 | 3.011 | 20 | 50 | fits | 150,286 | 174 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 457,383 | 4.574 | 20 | 50 | fits | 156,691 | 208 | 0.391 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 555,721 | 5.557 | 20 | 20 | fits | 87,790 | 44 | 0.733 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 924,839 | 9.248 | 20 | 20 | fits | 32,889 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 466,432 | 4.664 | 20 | 20 | fits | 155,794 | 209 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 362,556 | 3.626 | 20 | 200 | fits | 153,207 | 181 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 517,734 | 5.177 | 20 | 200 | fits | 155,794 | 209 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 363,480 | 3.635 | 20 | 20 | fits | 153,207 | 181 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 602,150 | 6.021 | 20 | 20 | fits | 83,712 | 31 | 0.752 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 204,414 | 2.044 | 20 | 24 | fits | 152,761 | 146 | 0.372 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 366,130 | 3.661 | 20 | 24 | fits | 153,207 | 181 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 366,064 | 3.661 | 20 | 50 | fits | 153,207 | 181 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 521,462 | 5.215 | 20 | 50 | fits | 155,794 | 209 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 605,108 | 6.051 | 20 | 20 | fits | 83,712 | 31 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 941,252 | 9.413 | 20 | 20 | fits | 84,341 | 37 | 0.539 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 387,931 | 3.879 | 20 | 20 | fits | 155,933 | 205 | 0.404 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 302,856 | 3.029 | 20 | 200 | fits | 152,493 | 180 | 0.402 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 458,173 | 4.582 | 20 | 200 | fits | 155,933 | 205 | 0.404 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 303,780 | 3.038 | 20 | 20 | fits | 152,493 | 180 | 0.402 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 542,553 | 5.426 | 20 | 20 | fits | 83,676 | 31 | 0.752 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 154,927 | 1.549 | 20 | 24 | fits | 151,931 | 145 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 306,430 | 3.064 | 20 | 24 | fits | 152,493 | 180 | 0.402 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 306,364 | 3.064 | 20 | 50 | fits | 152,493 | 180 | 0.402 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 461,901 | 4.619 | 20 | 50 | fits | 155,933 | 205 | 0.404 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 545,511 | 5.455 | 20 | 20 | fits | 83,676 | 31 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 929,569 | 9.296 | 20 | 20 | fits | 41,712 | 16 | 0.750 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 403,149 | 4.031 | 20 | 20 | fits | 154,805 | 204 | 0.393 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 301,460 | 3.015 | 20 | 200 | fits | 152,479 | 180 | 0.402 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 455,649 | 4.556 | 20 | 200 | fits | 154,805 | 204 | 0.393 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 302,384 | 3.024 | 20 | 20 | fits | 152,479 | 180 | 0.402 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 539,997 | 5.400 | 20 | 20 | fits | 83,644 | 31 | 0.752 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 153,545 | 1.535 | 20 | 24 | fits | 151,931 | 145 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 305,034 | 3.050 | 20 | 24 | fits | 152,479 | 180 | 0.402 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 304,968 | 3.050 | 20 | 50 | fits | 152,479 | 180 | 0.402 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 459,377 | 4.594 | 20 | 50 | fits | 154,805 | 204 | 0.393 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 542,955 | 5.430 | 20 | 20 | fits | 83,644 | 31 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 926,770 | 9.268 | 20 | 20 | fits | 41,479 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 402,322 | 4.023 | 20 | 20 | fits | 155,943 | 209 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 298,383 | 2.984 | 20 | 200 | fits | 150,784 | 176 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 453,710 | 4.537 | 20 | 200 | fits | 155,943 | 209 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 299,307 | 2.993 | 20 | 20 | fits | 150,784 | 176 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 542,385 | 5.424 | 20 | 20 | fits | 87,971 | 38 | 0.754 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 152,163 | 1.522 | 20 | 24 | fits | 151,931 | 145 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 301,957 | 3.020 | 20 | 24 | fits | 150,784 | 176 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 301,891 | 3.019 | 20 | 50 | fits | 150,784 | 176 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 457,438 | 4.574 | 20 | 50 | fits | 155,943 | 209 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 545,343 | 5.453 | 20 | 20 | fits | 87,971 | 38 | 0.754 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 924,763 | 9.248 | 20 | 20 | fits | 32,889 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 392,202 | 3.922 | 20 | 20 | fits | 157,192 | 197 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 296,840 | 2.968 | 20 | 200 | fits | 150,623 | 192 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 453,416 | 4.534 | 20 | 200 | fits | 157,192 | 197 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 297,764 | 2.978 | 20 | 20 | fits | 150,623 | 192 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 549,414 | 5.494 | 20 | 20 | fits | 84,759 | 42 | 0.772 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 150,781 | 1.508 | 20 | 24 | fits | 151,931 | 145 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 300,414 | 3.004 | 20 | 24 | fits | 150,623 | 192 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 300,348 | 3.003 | 20 | 50 | fits | 150,623 | 192 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 457,144 | 4.571 | 20 | 50 | fits | 157,192 | 197 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 552,372 | 5.524 | 20 | 20 | fits | 84,759 | 42 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 921,373 | 9.214 | 20 | 20 | fits | 32,889 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 425,236 | 4.252 | 20 | 20 | fits | 159,143 | 208 | 0.466 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 317,902 | 3.179 | 20 | 200 | fits | 152,458 | 181 | 0.401 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 486,592 | 4.866 | 20 | 200 | fits | 159,143 | 208 | 0.466 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 318,826 | 3.188 | 20 | 20 | fits | 152,458 | 181 | 0.401 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 571,499 | 5.715 | 20 | 20 | fits | 84,203 | 37 | 0.726 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 170,008 | 1.700 | 20 | 24 | fits | 151,937 | 145 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 321,476 | 3.215 | 20 | 24 | fits | 152,458 | 181 | 0.401 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 321,410 | 3.214 | 20 | 50 | fits | 152,458 | 181 | 0.401 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 490,320 | 4.903 | 20 | 50 | fits | 159,143 | 208 | 0.466 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 574,457 | 5.745 | 20 | 20 | fits | 84,203 | 37 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 943,409 | 9.434 | 20 | 20 | fits | 32,889 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 438,542 | 4.385 | 20 | 20 | fits | 153,961 | 200 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 328,288 | 3.283 | 20 | 200 | fits | 154,681 | 185 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 481,633 | 4.816 | 20 | 200 | fits | 153,961 | 200 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 329,212 | 3.292 | 20 | 20 | fits | 154,681 | 185 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 566,499 | 5.665 | 20 | 20 | fits | 84,162 | 37 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 168,819 | 1.688 | 20 | 24 | fits | 152,130 | 146 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 331,862 | 3.319 | 20 | 24 | fits | 154,681 | 185 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 331,796 | 3.318 | 20 | 50 | fits | 154,681 | 185 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 485,361 | 4.854 | 20 | 50 | fits | 153,961 | 200 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 569,457 | 5.695 | 20 | 20 | fits | 84,162 | 37 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 955,248 | 9.552 | 20 | 20 | fits | 38,701 | 19 | 0.844 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 411,859 | 4.119 | 20 | 20 | fits | 155,649 | 206 | 0.386 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 299,364 | 2.994 | 20 | 200 | fits | 149,785 | 174 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 454,397 | 4.544 | 20 | 200 | fits | 155,649 | 206 | 0.386 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 300,288 | 3.003 | 20 | 20 | fits | 149,785 | 174 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 539,049 | 5.390 | 20 | 20 | fits | 83,948 | 37 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 154,143 | 1.541 | 20 | 24 | fits | 151,962 | 145 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 302,938 | 3.029 | 20 | 24 | fits | 149,785 | 174 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 302,872 | 3.029 | 20 | 50 | fits | 149,785 | 174 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 458,125 | 4.581 | 20 | 50 | fits | 155,649 | 206 | 0.386 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 542,007 | 5.420 | 20 | 20 | fits | 83,948 | 37 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 928,195 | 9.282 | 20 | 20 | fits | 41,645 | 16 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 403,637 | 4.036 | 20 | 20 | fits | 157,972 | 196 | 0.393 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 307,874 | 3.079 | 20 | 200 | fits | 150,660 | 192 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 465,230 | 4.652 | 20 | 200 | fits | 157,972 | 196 | 0.393 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 308,798 | 3.088 | 20 | 20 | fits | 150,660 | 192 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 564,416 | 5.644 | 20 | 20 | fits | 87,868 | 38 | 0.758 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 161,778 | 1.618 | 20 | 24 | fits | 150,736 | 142 | 0.364 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 311,448 | 3.114 | 20 | 24 | fits | 150,660 | 192 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 311,382 | 3.114 | 20 | 50 | fits | 150,660 | 192 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 468,958 | 4.690 | 20 | 50 | fits | 157,972 | 196 | 0.393 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 567,374 | 5.674 | 20 | 20 | fits | 87,868 | 38 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 903,432 | 9.034 | 20 | 20 | fits | 84,300 | 36 | 0.539 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 398,638 | 3.986 | 20 | 20 | fits | 150,612 | 203 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 309,454 | 3.095 | 20 | 200 | fits | 152,524 | 180 | 0.401 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 459,450 | 4.595 | 20 | 200 | fits | 150,612 | 203 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 310,378 | 3.104 | 20 | 20 | fits | 152,524 | 180 | 0.401 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 556,611 | 5.566 | 20 | 20 | fits | 85,887 | 38 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 161,494 | 1.615 | 20 | 24 | fits | 150,736 | 142 | 0.364 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 313,028 | 3.130 | 20 | 24 | fits | 152,524 | 180 | 0.401 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 312,962 | 3.130 | 20 | 50 | fits | 152,524 | 180 | 0.401 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 463,178 | 4.632 | 20 | 50 | fits | 150,612 | 203 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 559,569 | 5.596 | 20 | 20 | fits | 85,887 | 38 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 1,011,993 | 10.120 | 20 | 20 | fits | 41,896 | 17 | 0.746 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 425,250 | 4.253 | 20 | 20 | fits | 159,454 | 211 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 309,287 | 3.093 | 20 | 200 | fits | 152,641 | 181 | 0.402 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 478,367 | 4.784 | 20 | 200 | fits | 159,454 | 211 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 310,211 | 3.102 | 20 | 20 | fits | 152,641 | 181 | 0.402 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 563,081 | 5.631 | 20 | 20 | fits | 84,010 | 31 | 0.755 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 161,210 | 1.612 | 20 | 24 | fits | 150,736 | 142 | 0.364 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 312,861 | 3.129 | 20 | 24 | fits | 152,641 | 181 | 0.402 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 312,795 | 3.128 | 20 | 50 | fits | 152,641 | 181 | 0.402 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 482,095 | 4.821 | 20 | 50 | fits | 159,454 | 211 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 566,039 | 5.660 | 20 | 20 | fits | 84,010 | 31 | 0.755 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,010,001 | 10.100 | 20 | 20 | fits | 33,115 | 12 | 0.821 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 423,027 | 4.230 | 20 | 20 | fits | 155,728 | 209 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 319,217 | 3.192 | 20 | 200 | fits | 153,272 | 181 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 474,329 | 4.743 | 20 | 200 | fits | 155,728 | 209 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 320,141 | 3.201 | 20 | 20 | fits | 153,272 | 181 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 558,890 | 5.589 | 20 | 20 | fits | 83,857 | 31 | 0.754 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 161,110 | 1.611 | 20 | 24 | fits | 150,920 | 143 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 322,791 | 3.228 | 20 | 24 | fits | 153,272 | 181 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 322,725 | 3.227 | 20 | 50 | fits | 153,272 | 181 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 478,057 | 4.781 | 20 | 50 | fits | 155,728 | 209 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 561,848 | 5.618 | 20 | 20 | fits | 83,857 | 31 | 0.754 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,022,376 | 10.224 | 20 | 20 | fits | 38,547 | 19 | 0.842 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 404,628 | 4.046 | 20 | 20 | fits | 155,861 | 209 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 300,771 | 3.008 | 20 | 200 | fits | 150,786 | 176 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 456,016 | 4.560 | 20 | 200 | fits | 155,861 | 209 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 301,695 | 3.017 | 20 | 20 | fits | 150,786 | 176 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 546,954 | 5.470 | 20 | 20 | fits | 90,234 | 39 | 0.748 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 154,549 | 1.545 | 20 | 24 | fits | 150,687 | 142 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 304,345 | 3.043 | 20 | 24 | fits | 150,786 | 176 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 304,279 | 3.043 | 20 | 50 | fits | 150,786 | 176 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 459,744 | 4.597 | 20 | 50 | fits | 155,861 | 209 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 549,912 | 5.499 | 20 | 20 | fits | 90,234 | 39 | 0.748 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,004,755 | 10.048 | 20 | 20 | fits | 32,889 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 394,572 | 3.946 | 20 | 20 | fits | 156,771 | 196 | 0.380 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 299,292 | 2.993 | 20 | 200 | fits | 150,569 | 192 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 455,447 | 4.554 | 20 | 200 | fits | 156,771 | 196 | 0.380 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 300,216 | 3.002 | 20 | 20 | fits | 150,569 | 192 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 546,443 | 5.464 | 20 | 20 | fits | 90,292 | 39 | 0.748 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 153,287 | 1.533 | 20 | 24 | fits | 150,608 | 142 | 0.362 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 302,866 | 3.029 | 20 | 24 | fits | 150,569 | 192 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 302,800 | 3.028 | 20 | 50 | fits | 150,569 | 192 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 459,175 | 4.592 | 20 | 50 | fits | 156,771 | 196 | 0.380 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 549,401 | 5.494 | 20 | 20 | fits | 90,292 | 39 | 0.748 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,004,585 | 10.046 | 20 | 20 | fits | 32,889 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 402,207 | 4.022 | 20 | 20 | fits | 156,652 | 191 | 0.428 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 298,016 | 2.980 | 20 | 200 | fits | 150,555 | 192 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 454,052 | 4.541 | 20 | 200 | fits | 156,652 | 191 | 0.428 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 298,940 | 2.989 | 20 | 20 | fits | 150,555 | 192 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 620,157 | 6.202 | 20 | 20 | fits | 88,324 | 45 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 152,025 | 1.520 | 20 | 24 | fits | 150,608 | 142 | 0.362 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 301,590 | 3.016 | 20 | 24 | fits | 150,555 | 192 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 301,524 | 3.015 | 20 | 50 | fits | 150,555 | 192 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 457,780 | 4.578 | 20 | 50 | fits | 156,652 | 191 | 0.428 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 623,115 | 6.231 | 20 | 20 | fits | 88,324 | 45 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,005,437 | 10.054 | 20 | 20 | fits | 32,842 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 480,242 | 4.802 | 20 | 20 | fits | 150,225 | 205 | 0.405 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 296,153 | 2.962 | 20 | 200 | fits | 149,954 | 174 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 522,734 | 5.227 | 20 | 200 | fits | 150,225 | 205 | 0.405 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 297,077 | 2.971 | 20 | 20 | fits | 149,954 | 174 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 620,992 | 6.210 | 20 | 20 | fits | 86,803 | 43 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 150,763 | 1.508 | 20 | 24 | fits | 150,608 | 142 | 0.362 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 299,727 | 2.997 | 20 | 24 | fits | 149,954 | 174 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 299,661 | 2.997 | 20 | 50 | fits | 149,954 | 174 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 526,462 | 5.265 | 20 | 50 | fits | 150,225 | 205 | 0.405 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 623,950 | 6.239 | 20 | 20 | fits | 86,803 | 43 | 0.712 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,001,357 | 10.014 | 20 | 20 | fits | 41,432 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 402,136 | 4.021 | 20 | 20 | fits | 154,650 | 204 | 0.392 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 300,602 | 3.006 | 20 | 200 | fits | 152,558 | 180 | 0.401 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 454,636 | 4.546 | 20 | 200 | fits | 154,650 | 204 | 0.392 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 301,526 | 3.015 | 20 | 20 | fits | 152,558 | 180 | 0.401 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 539,127 | 5.391 | 20 | 20 | fits | 83,787 | 31 | 0.753 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 152,608 | 1.526 | 20 | 24 | fits | 150,582 | 142 | 0.364 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 304,176 | 3.042 | 20 | 24 | fits | 152,558 | 180 | 0.401 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 304,110 | 3.041 | 20 | 50 | fits | 152,558 | 180 | 0.401 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 458,364 | 4.584 | 20 | 50 | fits | 154,650 | 204 | 0.392 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 542,085 | 5.421 | 20 | 20 | fits | 83,787 | 31 | 0.753 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 919,718 | 9.197 | 20 | 20 | fits | 32,889 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 401,281 | 4.013 | 20 | 20 | fits | 155,788 | 209 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 297,497 | 2.975 | 20 | 200 | fits | 150,973 | 176 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 452,669 | 4.527 | 20 | 200 | fits | 155,788 | 209 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 298,421 | 2.984 | 20 | 20 | fits | 150,973 | 176 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 537,507 | 5.375 | 20 | 20 | fits | 84,134 | 32 | 0.754 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 151,088 | 1.511 | 20 | 24 | fits | 150,582 | 142 | 0.364 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 301,071 | 3.011 | 20 | 24 | fits | 150,973 | 176 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 301,005 | 3.010 | 20 | 50 | fits | 150,973 | 176 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 456,397 | 4.564 | 20 | 50 | fits | 155,788 | 209 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 540,465 | 5.405 | 20 | 20 | fits | 84,134 | 32 | 0.754 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 923,787 | 9.238 | 20 | 20 | fits | 38,941 | 18 | 0.837 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 391,150 | 3.912 | 20 | 20 | fits | 157,037 | 197 | 0.382 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 295,943 | 2.959 | 20 | 200 | fits | 151,848 | 197 | 0.393 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 452,364 | 4.524 | 20 | 200 | fits | 157,037 | 197 | 0.382 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 296,867 | 2.969 | 20 | 20 | fits | 151,848 | 197 | 0.393 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 551,636 | 5.516 | 20 | 20 | fits | 87,954 | 38 | 0.760 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 148,659 | 1.487 | 20 | 24 | fits | 150,582 | 142 | 0.364 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 299,517 | 2.995 | 20 | 24 | fits | 151,848 | 197 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 299,451 | 2.995 | 20 | 50 | fits | 151,848 | 197 | 0.393 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 456,092 | 4.561 | 20 | 50 | fits | 157,037 | 197 | 0.382 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 554,594 | 5.546 | 20 | 20 | fits | 87,954 | 38 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 921,229 | 9.212 | 20 | 20 | fits | 32,889 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 405,192 | 4.052 | 20 | 20 | fits | 152,437 | 191 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 295,484 | 2.955 | 20 | 200 | fits | 152,000 | 198 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 457,512 | 4.575 | 20 | 200 | fits | 152,437 | 191 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 296,408 | 2.964 | 20 | 20 | fits | 152,000 | 198 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 542,615 | 5.426 | 20 | 20 | fits | 84,399 | 37 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 148,048 | 1.480 | 20 | 24 | fits | 150,582 | 142 | 0.364 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 299,058 | 2.991 | 20 | 24 | fits | 152,000 | 198 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 298,992 | 2.990 | 20 | 50 | fits | 152,000 | 198 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 461,240 | 4.612 | 20 | 50 | fits | 152,437 | 191 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 545,573 | 5.456 | 20 | 20 | fits | 84,399 | 37 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 920,876 | 9.209 | 20 | 20 | fits | 41,479 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 402,521 | 4.025 | 20 | 20 | fits | 150,187 | 222 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 305,412 | 3.054 | 20 | 200 | fits | 151,360 | 199 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 454,983 | 4.550 | 20 | 200 | fits | 150,187 | 222 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 306,336 | 3.063 | 20 | 20 | fits | 151,360 | 199 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 546,766 | 5.468 | 20 | 20 | fits | 91,079 | 45 | 0.723 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 149,099 | 1.491 | 20 | 24 | fits | 153,153 | 112 | 0.372 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 308,986 | 3.090 | 20 | 24 | fits | 151,360 | 199 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 308,920 | 3.089 | 20 | 50 | fits | 151,360 | 199 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 458,711 | 4.587 | 20 | 50 | fits | 150,187 | 222 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 549,724 | 5.497 | 20 | 20 | fits | 91,079 | 45 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 918,743 | 9.187 | 20 | 20 | fits | 32,889 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 436,322 | 4.363 | 20 | 20 | fits | 155,100 | 205 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 323,817 | 3.238 | 20 | 200 | fits | 153,156 | 181 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 478,301 | 4.783 | 20 | 200 | fits | 155,100 | 205 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 324,741 | 3.247 | 20 | 20 | fits | 153,156 | 181 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 563,258 | 5.633 | 20 | 20 | fits | 84,253 | 37 | 0.726 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 165,708 | 1.657 | 20 | 24 | fits | 150,702 | 143 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 327,391 | 3.274 | 20 | 24 | fits | 153,156 | 181 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 327,325 | 3.273 | 20 | 50 | fits | 153,156 | 181 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 482,029 | 4.820 | 20 | 50 | fits | 155,100 | 205 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 566,216 | 5.662 | 20 | 20 | fits | 84,253 | 37 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 935,040 | 9.350 | 20 | 20 | fits | 32,930 | 13 | 0.813 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 419,059 | 4.191 | 20 | 20 | fits | 154,859 | 205 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 306,795 | 3.068 | 20 | 200 | fits | 150,932 | 176 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 461,038 | 4.610 | 20 | 200 | fits | 154,859 | 205 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 307,719 | 3.077 | 20 | 20 | fits | 150,932 | 176 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 546,135 | 5.461 | 20 | 20 | fits | 84,393 | 37 | 0.726 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 160,427 | 1.604 | 20 | 24 | fits | 150,635 | 142 | 0.362 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 310,369 | 3.104 | 20 | 24 | fits | 150,932 | 176 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 310,303 | 3.103 | 20 | 50 | fits | 150,932 | 176 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 464,766 | 4.648 | 20 | 50 | fits | 154,859 | 205 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 549,093 | 5.491 | 20 | 20 | fits | 84,393 | 37 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 935,315 | 9.353 | 20 | 20 | fits | 41,479 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 407,954 | 4.080 | 20 | 20 | fits | 155,512 | 208 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 304,372 | 3.044 | 20 | 200 | fits | 149,771 | 174 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 459,268 | 4.593 | 20 | 200 | fits | 155,512 | 208 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 305,296 | 3.053 | 20 | 20 | fits | 149,771 | 174 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 544,092 | 5.441 | 20 | 20 | fits | 84,120 | 37 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 159,165 | 1.592 | 20 | 24 | fits | 150,635 | 142 | 0.362 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 307,946 | 3.079 | 20 | 24 | fits | 149,771 | 174 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 307,880 | 3.079 | 20 | 50 | fits | 149,771 | 174 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 462,996 | 4.630 | 20 | 50 | fits | 155,512 | 208 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 547,050 | 5.471 | 20 | 20 | fits | 84,120 | 37 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 933,283 | 9.333 | 20 | 20 | fits | 41,479 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 416,795 | 4.168 | 20 | 20 | fits | 152,698 | 192 | 0.428 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 306,826 | 3.068 | 20 | 200 | fits | 150,877 | 193 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 469,115 | 4.691 | 20 | 200 | fits | 152,698 | 192 | 0.428 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 307,750 | 3.078 | 20 | 20 | fits | 150,877 | 193 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 553,647 | 5.536 | 20 | 20 | fits | 83,828 | 37 | 0.726 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 160,513 | 1.605 | 20 | 24 | fits | 150,774 | 142 | 0.364 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 310,400 | 3.104 | 20 | 24 | fits | 150,877 | 193 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 310,334 | 3.103 | 20 | 50 | fits | 150,877 | 193 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 472,843 | 4.728 | 20 | 50 | fits | 152,698 | 192 | 0.428 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 556,605 | 5.566 | 20 | 20 | fits | 83,828 | 37 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 925,592 | 9.256 | 20 | 20 | fits | 32,889 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 405,273 | 4.053 | 20 | 20 | fits | 155,673 | 205 | 0.402 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 320,458 | 3.205 | 20 | 200 | fits | 154,920 | 185 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 475,515 | 4.755 | 20 | 200 | fits | 155,673 | 205 | 0.402 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 321,382 | 3.214 | 20 | 20 | fits | 154,920 | 185 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 559,382 | 5.594 | 20 | 20 | fits | 83,163 | 31 | 0.752 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 160,644 | 1.606 | 20 | 24 | fits | 151,003 | 143 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 324,032 | 3.240 | 20 | 24 | fits | 154,920 | 185 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 323,966 | 3.240 | 20 | 50 | fits | 154,920 | 185 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 479,243 | 4.792 | 20 | 50 | fits | 155,673 | 205 | 0.402 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 562,340 | 5.623 | 20 | 20 | fits | 83,163 | 31 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 1,014,635 | 10.146 | 20 | 20 | fits | 37,924 | 20 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 421,474 | 4.215 | 20 | 20 | fits | 154,650 | 204 | 0.392 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 319,940 | 3.199 | 20 | 200 | fits | 152,883 | 180 | 0.406 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 473,974 | 4.740 | 20 | 200 | fits | 154,650 | 204 | 0.392 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 320,864 | 3.209 | 20 | 20 | fits | 152,883 | 180 | 0.406 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 557,879 | 5.579 | 20 | 20 | fits | 83,201 | 31 | 0.752 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 171,621 | 1.716 | 20 | 24 | fits | 150,838 | 143 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 323,514 | 3.235 | 20 | 24 | fits | 152,883 | 180 | 0.406 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 323,448 | 3.234 | 20 | 50 | fits | 152,883 | 180 | 0.406 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 477,702 | 4.777 | 20 | 50 | fits | 154,650 | 204 | 0.392 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 560,837 | 5.608 | 20 | 20 | fits | 83,201 | 31 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,025,108 | 10.251 | 20 | 20 | fits | 41,979 | 16 | 0.756 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 404,919 | 4.049 | 20 | 20 | fits | 154,723 | 204 | 0.393 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 303,312 | 3.033 | 20 | 200 | fits | 152,634 | 180 | 0.402 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 457,419 | 4.574 | 20 | 200 | fits | 154,723 | 204 | 0.393 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 304,236 | 3.042 | 20 | 20 | fits | 152,634 | 180 | 0.402 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 541,400 | 5.414 | 20 | 20 | fits | 83,277 | 31 | 0.753 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 155,242 | 1.552 | 20 | 24 | fits | 150,644 | 142 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 306,886 | 3.069 | 20 | 24 | fits | 152,634 | 180 | 0.402 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 306,820 | 3.068 | 20 | 50 | fits | 152,634 | 180 | 0.402 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 461,147 | 4.611 | 20 | 50 | fits | 154,723 | 204 | 0.393 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 544,358 | 5.444 | 20 | 20 | fits | 83,277 | 31 | 0.753 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,008,406 | 10.084 | 20 | 20 | fits | 41,479 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 404,868 | 4.049 | 20 | 20 | fits | 155,861 | 209 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 301,011 | 3.010 | 20 | 200 | fits | 151,049 | 176 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 456,256 | 4.563 | 20 | 200 | fits | 155,861 | 209 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 301,935 | 3.019 | 20 | 20 | fits | 151,049 | 176 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 546,818 | 5.468 | 20 | 20 | fits | 89,858 | 40 | 0.747 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 154,526 | 1.545 | 20 | 24 | fits | 150,644 | 142 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 304,585 | 3.046 | 20 | 24 | fits | 151,049 | 176 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 304,519 | 3.045 | 20 | 50 | fits | 151,049 | 176 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 459,984 | 4.600 | 20 | 50 | fits | 155,861 | 209 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 549,776 | 5.498 | 20 | 20 | fits | 89,858 | 40 | 0.747 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,007,170 | 10.072 | 20 | 20 | fits | 32,889 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 395,473 | 3.955 | 20 | 20 | fits | 157,302 | 197 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 300,001 | 3.000 | 20 | 200 | fits | 150,755 | 192 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 456,687 | 4.567 | 20 | 200 | fits | 157,302 | 197 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 300,925 | 3.009 | 20 | 20 | fits | 150,755 | 192 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 552,063 | 5.521 | 20 | 20 | fits | 84,137 | 42 | 0.769 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 153,810 | 1.538 | 20 | 24 | fits | 150,644 | 142 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 303,575 | 3.036 | 20 | 24 | fits | 150,755 | 192 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 303,509 | 3.035 | 20 | 50 | fits | 150,755 | 192 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 460,415 | 4.604 | 20 | 50 | fits | 157,302 | 197 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 555,021 | 5.550 | 20 | 20 | fits | 84,137 | 42 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,005,510 | 10.055 | 20 | 20 | fits | 32,889 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 417,088 | 4.171 | 20 | 20 | fits | 151,149 | 190 | 0.457 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 299,437 | 2.994 | 20 | 200 | fits | 150,907 | 193 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 460,098 | 4.601 | 20 | 200 | fits | 151,149 | 190 | 0.457 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 300,361 | 3.004 | 20 | 20 | fits | 150,907 | 193 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 625,509 | 6.255 | 20 | 20 | fits | 83,885 | 43 | 0.691 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 153,094 | 1.531 | 20 | 24 | fits | 150,644 | 142 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 303,011 | 3.030 | 20 | 24 | fits | 150,907 | 193 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 302,945 | 3.029 | 20 | 50 | fits | 150,907 | 193 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 463,826 | 4.638 | 20 | 50 | fits | 151,149 | 190 | 0.457 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 628,467 | 6.285 | 20 | 20 | fits | 83,885 | 43 | 0.691 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,005,918 | 10.059 | 20 | 20 | fits | 41,432 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 496,037 | 4.960 | 20 | 20 | fits | 152,059 | 204 | 0.434 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 298,087 | 2.981 | 20 | 200 | fits | 150,273 | 175 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 539,481 | 5.395 | 20 | 200 | fits | 152,059 | 204 | 0.434 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 299,011 | 2.990 | 20 | 20 | fits | 150,273 | 175 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 624,677 | 6.247 | 20 | 20 | fits | 84,492 | 42 | 0.702 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 152,378 | 1.524 | 20 | 24 | fits | 150,644 | 142 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 301,661 | 3.017 | 20 | 24 | fits | 150,273 | 175 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 301,595 | 3.016 | 20 | 50 | fits | 150,273 | 175 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 543,209 | 5.432 | 20 | 50 | fits | 152,059 | 204 | 0.434 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 627,635 | 6.276 | 20 | 20 | fits | 84,492 | 42 | 0.702 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,005,156 | 10.052 | 20 | 20 | fits | 41,479 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 399,875 | 3.999 | 20 | 20 | fits | 158,376 | 225 | 0.404 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 294,775 | 2.948 | 20 | 200 | fits | 150,334 | 198 | 0.402 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 452,535 | 4.525 | 20 | 200 | fits | 158,376 | 225 | 0.404 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 295,699 | 2.957 | 20 | 20 | fits | 150,334 | 198 | 0.402 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 551,011 | 5.510 | 20 | 20 | fits | 87,158 | 38 | 0.757 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 149,005 | 1.490 | 20 | 24 | fits | 153,149 | 111 | 0.371 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 298,349 | 2.983 | 20 | 24 | fits | 150,334 | 198 | 0.402 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 298,283 | 2.983 | 20 | 50 | fits | 150,334 | 198 | 0.402 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 456,263 | 4.563 | 20 | 50 | fits | 158,376 | 225 | 0.404 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 553,969 | 5.540 | 20 | 20 | fits | 87,158 | 38 | 0.757 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 889,976 | 8.900 | 20 | 20 | fits | 84,300 | 36 | 0.539 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 393,754 | 3.938 | 20 | 20 | fits | 150,925 | 222 | 0.405 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 294,514 | 2.945 | 20 | 200 | fits | 150,171 | 198 | 0.401 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 444,823 | 4.448 | 20 | 200 | fits | 150,925 | 222 | 0.405 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 295,438 | 2.954 | 20 | 20 | fits | 150,171 | 198 | 0.401 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 541,101 | 5.411 | 20 | 20 | fits | 84,960 | 37 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 148,907 | 1.489 | 20 | 24 | fits | 153,149 | 111 | 0.371 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 298,088 | 2.981 | 20 | 24 | fits | 150,171 | 198 | 0.401 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 298,022 | 2.980 | 20 | 50 | fits | 150,171 | 198 | 0.401 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 448,551 | 4.486 | 20 | 50 | fits | 150,925 | 222 | 0.405 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 544,059 | 5.441 | 20 | 20 | fits | 84,960 | 37 | 0.733 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 918,891 | 9.189 | 20 | 20 | fits | 38,908 | 18 | 0.837 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 403,592 | 4.036 | 20 | 20 | fits | 151,492 | 221 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 294,415 | 2.944 | 20 | 200 | fits | 150,170 | 199 | 0.401 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 455,533 | 4.555 | 20 | 200 | fits | 151,492 | 221 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 295,339 | 2.953 | 20 | 20 | fits | 150,170 | 199 | 0.401 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 540,284 | 5.403 | 20 | 20 | fits | 84,047 | 37 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 148,809 | 1.488 | 20 | 24 | fits | 153,149 | 111 | 0.371 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 297,989 | 2.980 | 20 | 24 | fits | 150,170 | 199 | 0.401 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 297,923 | 2.979 | 20 | 50 | fits | 150,170 | 199 | 0.401 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 459,261 | 4.593 | 20 | 50 | fits | 151,492 | 221 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 543,242 | 5.432 | 20 | 20 | fits | 84,047 | 37 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 918,522 | 9.185 | 20 | 20 | fits | 41,479 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 402,204 | 4.022 | 20 | 20 | fits | 150,187 | 222 | 0.411 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 304,966 | 3.050 | 20 | 200 | fits | 151,109 | 199 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 454,537 | 4.545 | 20 | 200 | fits | 150,187 | 222 | 0.411 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 305,890 | 3.059 | 20 | 20 | fits | 151,109 | 199 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 538,888 | 5.389 | 20 | 20 | fits | 83,647 | 37 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 148,904 | 1.489 | 20 | 24 | fits | 153,342 | 112 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 308,540 | 3.085 | 20 | 24 | fits | 151,109 | 199 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 308,474 | 3.085 | 20 | 50 | fits | 151,109 | 199 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 458,265 | 4.583 | 20 | 50 | fits | 150,187 | 222 | 0.411 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 541,846 | 5.418 | 20 | 20 | fits | 83,647 | 37 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 934,061 | 9.341 | 20 | 20 | fits | 47,194 | 23 | 0.789 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 394,003 | 3.940 | 20 | 20 | fits | 155,778 | 205 | 0.403 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 309,083 | 3.091 | 20 | 200 | fits | 152,705 | 180 | 0.402 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 464,245 | 4.642 | 20 | 200 | fits | 155,778 | 205 | 0.403 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 310,007 | 3.100 | 20 | 20 | fits | 152,705 | 180 | 0.402 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 554,599 | 5.546 | 20 | 20 | fits | 89,650 | 39 | 0.747 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 160,942 | 1.609 | 20 | 24 | fits | 150,752 | 142 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 312,657 | 3.127 | 20 | 24 | fits | 152,705 | 180 | 0.402 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 312,591 | 3.126 | 20 | 50 | fits | 152,705 | 180 | 0.402 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 467,973 | 4.680 | 20 | 50 | fits | 155,778 | 205 | 0.403 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 557,557 | 5.576 | 20 | 20 | fits | 89,650 | 39 | 0.747 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 935,358 | 9.354 | 20 | 20 | fits | 33,272 | 12 | 0.825 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 417,868 | 4.179 | 20 | 20 | fits | 153,582 | 200 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 307,993 | 3.080 | 20 | 200 | fits | 152,691 | 180 | 0.402 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 460,959 | 4.610 | 20 | 200 | fits | 153,582 | 200 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 308,917 | 3.089 | 20 | 20 | fits | 152,691 | 180 | 0.402 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 545,397 | 5.454 | 20 | 20 | fits | 83,734 | 37 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 159,866 | 1.599 | 20 | 24 | fits | 150,673 | 142 | 0.362 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 311,567 | 3.116 | 20 | 24 | fits | 152,691 | 180 | 0.402 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 311,501 | 3.115 | 20 | 50 | fits | 152,691 | 180 | 0.402 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 464,687 | 4.647 | 20 | 50 | fits | 153,582 | 200 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 548,355 | 5.484 | 20 | 20 | fits | 83,734 | 37 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 934,391 | 9.344 | 20 | 20 | fits | 41,479 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 417,596 | 4.176 | 20 | 20 | fits | 154,859 | 205 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 305,332 | 3.053 | 20 | 200 | fits | 151,106 | 176 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 459,575 | 4.596 | 20 | 200 | fits | 154,859 | 205 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 306,256 | 3.063 | 20 | 20 | fits | 151,106 | 176 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 544,309 | 5.443 | 20 | 20 | fits | 84,030 | 38 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 158,790 | 1.588 | 20 | 24 | fits | 150,673 | 142 | 0.362 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 308,906 | 3.089 | 20 | 24 | fits | 151,106 | 176 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 308,840 | 3.088 | 20 | 50 | fits | 151,106 | 176 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 463,303 | 4.633 | 20 | 50 | fits | 154,859 | 205 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 547,267 | 5.473 | 20 | 20 | fits | 84,030 | 38 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 933,089 | 9.331 | 20 | 20 | fits | 41,479 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 406,669 | 4.067 | 20 | 20 | fits | 155,955 | 209 | 0.386 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 302,983 | 3.030 | 20 | 200 | fits | 149,833 | 174 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 458,322 | 4.583 | 20 | 200 | fits | 155,955 | 209 | 0.386 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 303,907 | 3.039 | 20 | 20 | fits | 149,833 | 174 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 557,509 | 5.575 | 20 | 20 | fits | 87,869 | 44 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 157,714 | 1.577 | 20 | 24 | fits | 150,673 | 142 | 0.362 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 306,557 | 3.066 | 20 | 24 | fits | 149,833 | 174 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 306,491 | 3.065 | 20 | 50 | fits | 149,833 | 174 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 462,050 | 4.620 | 20 | 50 | fits | 155,955 | 209 | 0.386 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 560,467 | 5.605 | 20 | 20 | fits | 87,869 | 44 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 929,585 | 9.296 | 20 | 20 | fits | 32,889 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 423,507 | 4.235 | 20 | 20 | fits | 155,969 | 209 | 0.385 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 319,542 | 3.195 | 20 | 200 | fits | 153,125 | 181 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 474,895 | 4.749 | 20 | 200 | fits | 155,969 | 209 | 0.385 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 320,466 | 3.205 | 20 | 20 | fits | 153,125 | 181 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 559,252 | 5.593 | 20 | 20 | fits | 83,653 | 31 | 0.752 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 161,582 | 1.616 | 20 | 24 | fits | 150,738 | 143 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 323,116 | 3.231 | 20 | 24 | fits | 153,125 | 181 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 323,050 | 3.231 | 20 | 50 | fits | 153,125 | 181 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 478,623 | 4.786 | 20 | 50 | fits | 155,969 | 209 | 0.385 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 562,210 | 5.622 | 20 | 20 | fits | 83,653 | 31 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 898,120 | 8.981 | 20 | 20 | fits | 84,253 | 36 | 0.539 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 404,569 | 4.046 | 20 | 20 | fits | 155,870 | 209 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 300,703 | 3.007 | 20 | 200 | fits | 150,830 | 176 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 455,957 | 4.560 | 20 | 200 | fits | 155,870 | 209 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 301,627 | 3.016 | 20 | 20 | fits | 150,830 | 176 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 540,457 | 5.405 | 20 | 20 | fits | 83,796 | 31 | 0.753 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 154,437 | 1.544 | 20 | 24 | fits | 150,521 | 142 | 0.361 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 304,277 | 3.043 | 20 | 24 | fits | 150,830 | 176 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 304,211 | 3.042 | 20 | 50 | fits | 150,830 | 176 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 459,685 | 4.597 | 20 | 50 | fits | 155,870 | 209 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 543,415 | 5.434 | 20 | 20 | fits | 83,796 | 31 | 0.753 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 928,250 | 9.283 | 20 | 20 | fits | 38,965 | 18 | 0.837 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 393,933 | 3.939 | 20 | 20 | fits | 156,780 | 196 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 298,644 | 2.986 | 20 | 200 | fits | 150,681 | 192 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 454,808 | 4.548 | 20 | 200 | fits | 156,780 | 196 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 299,568 | 2.996 | 20 | 20 | fits | 150,681 | 192 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 539,317 | 5.393 | 20 | 20 | fits | 83,805 | 31 | 0.754 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 152,527 | 1.525 | 20 | 24 | fits | 150,521 | 142 | 0.361 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 302,218 | 3.022 | 20 | 24 | fits | 150,681 | 192 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 302,152 | 3.022 | 20 | 50 | fits | 150,681 | 192 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 458,536 | 4.585 | 20 | 50 | fits | 156,780 | 196 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 542,275 | 5.423 | 20 | 20 | fits | 83,805 | 31 | 0.754 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,004,303 | 10.043 | 20 | 20 | fits | 41,705 | 16 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 392,565 | 3.926 | 20 | 20 | fits | 157,715 | 195 | 0.391 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 296,720 | 2.967 | 20 | 200 | fits | 150,667 | 192 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 453,819 | 4.538 | 20 | 200 | fits | 157,715 | 195 | 0.391 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 297,644 | 2.976 | 20 | 20 | fits | 150,667 | 192 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 538,308 | 5.383 | 20 | 20 | fits | 83,785 | 32 | 0.751 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 150,617 | 1.506 | 20 | 24 | fits | 150,521 | 142 | 0.361 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 300,294 | 3.003 | 20 | 24 | fits | 150,667 | 192 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 300,228 | 3.002 | 20 | 50 | fits | 150,667 | 192 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 457,547 | 4.575 | 20 | 50 | fits | 157,715 | 195 | 0.391 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 541,266 | 5.413 | 20 | 20 | fits | 83,785 | 32 | 0.751 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,002,906 | 10.029 | 20 | 20 | fits | 41,479 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 382,701 | 3.827 | 20 | 20 | fits | 156,199 | 206 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 297,699 | 2.977 | 20 | 200 | fits | 153,665 | 185 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 453,282 | 4.533 | 20 | 200 | fits | 156,199 | 206 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 298,623 | 2.986 | 20 | 20 | fits | 153,665 | 185 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 549,216 | 5.492 | 20 | 20 | fits | 84,695 | 42 | 0.772 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 148,598 | 1.486 | 20 | 24 | fits | 150,521 | 142 | 0.361 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 301,273 | 3.013 | 20 | 24 | fits | 153,665 | 185 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 301,207 | 3.012 | 20 | 50 | fits | 153,665 | 185 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 457,010 | 4.570 | 20 | 50 | fits | 156,199 | 206 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 552,174 | 5.522 | 20 | 20 | fits | 84,695 | 42 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 999,375 | 9.994 | 20 | 20 | fits | 32,889 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 413,039 | 4.130 | 20 | 20 | fits | 151,912 | 219 | 0.431 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 294,869 | 2.949 | 20 | 200 | fits | 150,312 | 199 | 0.402 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 456,284 | 4.563 | 20 | 200 | fits | 151,912 | 219 | 0.431 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 295,793 | 2.958 | 20 | 20 | fits | 150,312 | 199 | 0.402 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 547,984 | 5.480 | 20 | 20 | fits | 90,996 | 45 | 0.723 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 149,121 | 1.491 | 20 | 24 | fits | 152,845 | 111 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 298,443 | 2.984 | 20 | 24 | fits | 150,312 | 199 | 0.402 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 298,377 | 2.984 | 20 | 50 | fits | 150,312 | 199 | 0.402 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 460,012 | 4.600 | 20 | 50 | fits | 151,912 | 219 | 0.431 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 550,942 | 5.509 | 20 | 20 | fits | 90,996 | 45 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 998,049 | 9.980 | 20 | 20 | fits | 32,889 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 426,965 | 4.270 | 20 | 20 | fits | 155,826 | 192 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 323,135 | 3.231 | 20 | 200 | fits | 152,849 | 197 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 478,345 | 4.783 | 20 | 200 | fits | 155,826 | 192 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 324,059 | 3.241 | 20 | 20 | fits | 152,849 | 197 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 641,012 | 6.410 | 20 | 20 | fits | 84,169 | 38 | 0.719 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 165,598 | 1.656 | 20 | 24 | fits | 150,717 | 143 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 326,709 | 3.267 | 20 | 24 | fits | 152,849 | 197 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 326,643 | 3.266 | 20 | 50 | fits | 152,849 | 197 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 482,073 | 4.821 | 20 | 50 | fits | 155,826 | 192 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 643,970 | 6.440 | 20 | 20 | fits | 84,169 | 38 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,030,003 | 10.300 | 20 | 20 | fits | 41,645 | 16 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 484,626 | 4.846 | 20 | 20 | fits | 155,790 | 208 | 0.380 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 303,311 | 3.033 | 20 | 200 | fits | 149,806 | 174 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 536,282 | 5.363 | 20 | 200 | fits | 155,790 | 208 | 0.380 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 304,235 | 3.042 | 20 | 20 | fits | 149,806 | 174 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 621,019 | 6.210 | 20 | 20 | fits | 84,033 | 37 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 158,069 | 1.581 | 20 | 24 | fits | 150,768 | 142 | 0.364 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 306,885 | 3.069 | 20 | 24 | fits | 149,806 | 174 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 306,819 | 3.068 | 20 | 50 | fits | 149,806 | 174 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 540,010 | 5.400 | 20 | 50 | fits | 155,790 | 208 | 0.380 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 623,977 | 6.240 | 20 | 20 | fits | 84,033 | 37 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,010,134 | 10.101 | 20 | 20 | fits | 41,479 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 405,871 | 4.059 | 20 | 20 | fits | 152,667 | 191 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 295,933 | 2.959 | 20 | 200 | fits | 151,948 | 198 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 458,191 | 4.582 | 20 | 200 | fits | 152,667 | 191 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 296,857 | 2.969 | 20 | 20 | fits | 151,948 | 198 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 543,151 | 5.432 | 20 | 20 | fits | 84,256 | 37 | 0.726 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 148,549 | 1.485 | 20 | 24 | fits | 150,619 | 142 | 0.362 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 299,507 | 2.995 | 20 | 24 | fits | 151,948 | 198 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 299,441 | 2.994 | 20 | 50 | fits | 151,948 | 198 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 461,919 | 4.619 | 20 | 50 | fits | 152,667 | 191 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 546,109 | 5.461 | 20 | 20 | fits | 84,256 | 37 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 915,061 | 9.151 | 20 | 20 | fits | 32,889 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 394,682 | 3.947 | 20 | 20 | fits | 158,466 | 211 | 0.416 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 307,130 | 3.071 | 20 | 200 | fits | 154,652 | 185 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 464,980 | 4.650 | 20 | 200 | fits | 158,466 | 211 | 0.416 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 308,054 | 3.081 | 20 | 20 | fits | 154,652 | 185 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 549,565 | 5.496 | 20 | 20 | fits | 83,881 | 31 | 0.754 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 147,525 | 1.475 | 20 | 24 | fits | 150,810 | 143 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 310,704 | 3.107 | 20 | 24 | fits | 154,652 | 185 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 310,638 | 3.106 | 20 | 50 | fits | 154,652 | 185 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 468,708 | 4.687 | 20 | 50 | fits | 158,466 | 211 | 0.416 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 552,523 | 5.525 | 20 | 20 | fits | 83,881 | 31 | 0.754 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 888,373 | 8.884 | 20 | 20 | fits | 84,300 | 36 | 0.539 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 410,541 | 4.105 | 20 | 20 | fits | 157,855 | 210 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 305,877 | 3.059 | 20 | 200 | fits | 154,565 | 185 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 463,116 | 4.631 | 20 | 200 | fits | 157,855 | 210 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 306,801 | 3.068 | 20 | 20 | fits | 154,565 | 185 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 547,594 | 5.476 | 20 | 20 | fits | 83,774 | 31 | 0.753 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 146,359 | 1.464 | 20 | 24 | fits | 151,901 | 143 | 0.364 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 309,451 | 3.095 | 20 | 24 | fits | 154,565 | 185 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 309,385 | 3.094 | 20 | 50 | fits | 154,565 | 185 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 466,844 | 4.668 | 20 | 50 | fits | 157,855 | 210 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 550,552 | 5.506 | 20 | 20 | fits | 83,774 | 31 | 0.753 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 921,403 | 9.214 | 20 | 20 | fits | 37,339 | 19 | 0.815 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 412,042 | 4.120 | 20 | 20 | fits | 155,943 | 209 | 0.384 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 308,103 | 3.081 | 20 | 200 | fits | 150,826 | 176 | 0.404 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 463,430 | 4.634 | 20 | 200 | fits | 155,943 | 209 | 0.384 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 309,027 | 3.090 | 20 | 20 | fits | 150,826 | 176 | 0.404 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 547,930 | 5.479 | 20 | 20 | fits | 83,796 | 31 | 0.753 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 161,841 | 1.618 | 20 | 24 | fits | 150,601 | 142 | 0.362 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 311,677 | 3.117 | 20 | 24 | fits | 150,826 | 176 | 0.404 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 311,611 | 3.116 | 20 | 50 | fits | 150,826 | 176 | 0.404 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 467,158 | 4.672 | 20 | 50 | fits | 155,943 | 209 | 0.384 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 550,888 | 5.509 | 20 | 20 | fits | 83,796 | 31 | 0.753 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 934,686 | 9.347 | 20 | 20 | fits | 41,479 | 16 | 0.744 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 402,634 | 4.026 | 20 | 20 | fits | 156,853 | 196 | 0.380 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 307,272 | 3.073 | 20 | 200 | fits | 150,711 | 192 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 463,509 | 4.635 | 20 | 200 | fits | 156,853 | 196 | 0.380 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 308,196 | 3.082 | 20 | 20 | fits | 150,711 | 192 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 554,435 | 5.544 | 20 | 20 | fits | 90,222 | 40 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 161,125 | 1.611 | 20 | 24 | fits | 150,601 | 142 | 0.362 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 310,846 | 3.108 | 20 | 24 | fits | 150,711 | 192 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 310,780 | 3.108 | 20 | 50 | fits | 150,711 | 192 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 467,237 | 4.672 | 20 | 50 | fits | 156,853 | 196 | 0.380 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 557,393 | 5.574 | 20 | 20 | fits | 90,222 | 40 | 0.746 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 934,517 | 9.345 | 20 | 20 | fits | 32,889 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 410,815 | 4.108 | 20 | 20 | fits | 157,073 | 192 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 306,542 | 3.065 | 20 | 200 | fits | 150,697 | 192 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 462,999 | 4.630 | 20 | 200 | fits | 157,073 | 192 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 307,466 | 3.075 | 20 | 20 | fits | 150,697 | 192 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 562,487 | 5.625 | 20 | 20 | fits | 88,132 | 44 | 0.732 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 160,409 | 1.604 | 20 | 24 | fits | 150,601 | 142 | 0.362 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 310,116 | 3.101 | 20 | 24 | fits | 150,697 | 192 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 310,050 | 3.100 | 20 | 50 | fits | 150,697 | 192 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 466,727 | 4.667 | 20 | 50 | fits | 157,073 | 192 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 565,445 | 5.654 | 20 | 20 | fits | 88,132 | 44 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 934,528 | 9.345 | 20 | 20 | fits | 32,889 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 415,020 | 4.150 | 20 | 20 | fits | 158,951 | 208 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 307,830 | 3.078 | 20 | 200 | fits | 152,701 | 181 | 0.402 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 476,328 | 4.763 | 20 | 200 | fits | 158,951 | 208 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 308,754 | 3.088 | 20 | 20 | fits | 152,701 | 181 | 0.402 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 561,160 | 5.612 | 20 | 20 | fits | 84,128 | 37 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 159,693 | 1.597 | 20 | 24 | fits | 150,601 | 142 | 0.362 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 311,404 | 3.114 | 20 | 24 | fits | 152,701 | 181 | 0.402 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 311,338 | 3.113 | 20 | 50 | fits | 152,701 | 181 | 0.402 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 480,056 | 4.801 | 20 | 50 | fits | 158,951 | 208 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 564,118 | 5.641 | 20 | 20 | fits | 84,128 | 37 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 932,836 | 9.328 | 20 | 20 | fits | 32,842 | 12 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 431,237 | 4.312 | 20 | 20 | fits | 151,185 | 205 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 304,531 | 3.045 | 20 | 200 | fits | 150,118 | 175 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 465,298 | 4.653 | 20 | 200 | fits | 151,185 | 205 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 305,455 | 3.055 | 20 | 20 | fits | 150,118 | 175 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 550,879 | 5.509 | 20 | 20 | fits | 84,877 | 42 | 0.700 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 158,977 | 1.590 | 20 | 24 | fits | 150,601 | 142 | 0.362 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 308,105 | 3.081 | 20 | 24 | fits | 150,118 | 175 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 308,039 | 3.080 | 20 | 50 | fits | 150,118 | 175 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 469,026 | 4.690 | 20 | 50 | fits | 151,185 | 205 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 553,837 | 5.538 | 20 | 20 | fits | 84,877 | 42 | 0.700 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 931,323 | 9.313 | 20 | 20 | fits | 41,479 | 16 | 0.744 |
| LINK_UP | `adp.link_up.if0` | 3,526 | 0.035 | 20 | 200 | fits | 34,462 | 43 (11) | 0.746 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 25,486 | 0.255 | 20 | 200 | fits | 28,650 | 23 (39) | 0.770 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 8,581 | 0.086 | 20 | 200 | fits | 3,500 | 10 (11) | 0.600 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 33,066 | 0.331 | 20 | 20 | fits | 38,655 | 27 (35) | 0.807 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 29,697 | 0.297 | 20 | 20 | fits | 34,907 | 23 (14) | 0.839 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 26,757 | 0.268 | 20 | 20 | fits | 34,823 | 24 (14) | 0.836 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 30,575 | 0.306 | 20 | 20 | fits | 41,097 | 27 (35) | 0.811 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 81,111 | 0.811 | 20 | 20 | fits | 27,242 | 8 | 0.805 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 45,597 | 0.456 | 20 | 20 | fits | 45,663 | 12 | 0.893 |
| malformed MRPDU discard | `srp.malformed.if0` | 24,470 | 0.245 | 20 | 20 | fits | 24,536 | 12 | 0.722 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 79,488 | 0.795 | 220 | 220 | fits | 42,397 | 6 | 0.910 |
| an event behind 15 others | `backlog.event.if0` | 167,460 | 1.675 | 20 | 200 | fits | 61,655 | 79 | 0.549 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 483,365 | 4.834 | 20 | 20 | fits | 79,198 | 74 | 0.409 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 432,810 | 4.328 | 20 | 200 | fits | 152,370 | 121 | 0.435 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 511,392 | 5.114 | 20 | 200 | fits | 79,198 | 74 | 0.409 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 428,488 | 4.285 | 20 | 20 | fits | 152,370 | 121 | 0.435 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 506,850 | 5.069 | 20 | 20 | fits | 79,198 | 74 | 0.409 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 152,987 | 1.530 | 20 | 24 | fits | 153,878 | 148 | 0.379 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 431,138 | 4.311 | 20 | 24 | fits | 152,370 | 121 | 0.435 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 431,072 | 4.311 | 20 | 50 | fits | 152,370 | 121 | 0.435 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 509,874 | 5.099 | 20 | 50 | fits | 79,198 | 74 | 0.409 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 509,808 | 5.098 | 20 | 20 | fits | 79,198 | 74 | 0.409 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 599,763 | 5.998 | 20 | 20 | fits | 24,100 | 28 | 0.283 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 414,661 | 4.147 | 20 | 20 | fits | 159,029 | 211 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 299,437 | 2.994 | 20 | 200 | fits | 152,296 | 181 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 467,773 | 4.678 | 20 | 200 | fits | 159,029 | 211 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 300,361 | 3.004 | 20 | 20 | fits | 152,296 | 181 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 558,240 | 5.582 | 20 | 20 | fits | 89,763 | 39 | 0.750 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 151,705 | 1.517 | 20 | 24 | fits | 151,891 | 145 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 303,011 | 3.030 | 20 | 24 | fits | 152,296 | 181 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 302,945 | 3.029 | 20 | 50 | fits | 152,296 | 181 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 471,501 | 4.715 | 20 | 50 | fits | 159,029 | 211 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 561,198 | 5.612 | 20 | 20 | fits | 89,763 | 39 | 0.750 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 897,250 | 8.973 | 20 | 20 | fits | 84,295 | 36 | 0.539 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 20,567 | 0.206 | 20 | 20 | fits | 35,012 | 19 | 0.808 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 299,437 | 2.994 | 20 | 200 | fits | 152,296 | 181 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 43,916 | 0.439 | 20 | 200 | fits | 35,012 | 19 | 0.808 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 300,361 | 3.004 | 20 | 20 | fits | 152,296 | 181 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 464,512 | 4.645 | 20 | 20 | fits | 155,064 | 210 | 0.380 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 151,705 | 1.517 | 20 | 24 | fits | 151,891 | 145 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 303,011 | 3.030 | 20 | 24 | fits | 152,296 | 181 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 302,945 | 3.029 | 20 | 50 | fits | 152,296 | 181 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 467,536 | 4.675 | 20 | 50 | fits | 155,064 | 210 | 0.380 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 555,235 | 5.552 | 20 | 20 | fits | 87,765 | 34 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 882,590 | 8.826 | 20 | 20 | fits | 75,834 | 32 | 0.569 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,354,603 | 63.546 | 20 | 20 | MISS ceiling | 24,592 | 13 | 0.645 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,383,736 | 63.837 | 20 | 20 | MISS ceiling | 27,754 | 18 | 0.705 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,407,120 | 64.071 | 20 | 20 | MISS ceiling | 25,891 | 13 | 0.625 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,432,965 | 64.330 | 20 | 20 | MISS ceiling | 25,229 | 13 | 0.671 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,457,842 | 64.578 | 20 | 20 | MISS ceiling | 24,676 | 13 | 0.650 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 160,595 | 1.606 | 20 | 200 | fits | 155,689 | 177 | 0.439 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 293,681 | 2.937 | 20 | 200 | fits | 133,702 | 207 | 0.367 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 156,273 | 1.563 | 20 | 20 | fits | 155,689 | 177 | 0.439 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,238,865 | 62.389 | 20 | 20 | MISS ceiling | 39,921 | 15 | 0.771 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 159,913 | 1.599 | 20 | 24 | fits | 155,689 | 177 | 0.439 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,202,430 | 62.024 | 20 | 24 | MISS ceiling | 156,004 | 106 | 0.397 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 158,857 | 1.589 | 20 | 50 | fits | 155,689 | 177 | 0.439 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 292,163 | 2.922 | 20 | 50 | fits | 133,702 | 207 | 0.367 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 374,369 | 3.744 | 20 | 20 | fits | 82,272 | 28 | 0.742 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 709,378 | 7.094 | 20 | 20 | fits | 84,811 | 36 | 0.548 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 6,662 | 0.067 | 20 | 20 | fits | 29,957 | 14 (29) | 0.774 |
