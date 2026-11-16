### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 85 paths and 7 of 947 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.212 (0.472) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.107 (0.302) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.100 (0.330) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.095 (0.524) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.111 (0.305) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.099 (0.288) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.100 (0.293) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.113 (0.307) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.108 (0.350) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.302 (0.738) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.221 (0.655) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.230 (0.636) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.146 (0.589) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.110 (0.605) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.249 (0.599) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.161 (0.429) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.055 (0.208) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.028 (0.207) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.029 (0.325) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.030 (0.338) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.091 (0.291) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.206 (0.598) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.254 (0.636) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.197 (0.605) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.213 (0.590) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.247 (0.633) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.277 (0.666) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.276 (0.740) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.251 (0.636) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.315 (0.703) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.241 (0.627) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.264 (0.518) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.237 (0.632) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.322 (0.711) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.231 (0.617) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.273 (0.665) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.236 (0.628) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.263 (0.519) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.240 (0.634) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.276 (0.666) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.276 (0.664) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.245 (0.632) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.272 (0.660) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.214 (0.597) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.347 (0.832) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.215 (0.604) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.329 (0.756) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.512 (0.837) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.580 (0.928) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.521 (0.854) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.594 (0.968) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.537 (0.889) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.554 (0.876) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.806 (5.098) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 5.099 (5.612) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.280 (0.715) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.647 (2.126) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.513 (63.699) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.512 (64.701) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.344 (0.495) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 2.970 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.661 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 3.112 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 2.065 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.757 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.176 (0.577) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.113 (0.277) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.142 (0.338) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.156 (0.577) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.230 (0.617) | fits | 0 events | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.663 | fits | 0 srp | 6 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.263 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.380 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.307 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 5.435 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-aged1-0.service.aecp.first.if0` (backlog-adp@blank-aged1-0) | 2.960 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.030 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.289 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.maap.last.if0` (backlog-adp@program-aged2-7) | 5.472 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-6.service.srp.first.if0` (backlog-adp@program-aged2-6) | 6.445 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-6.service.srp.last.if0` (backlog-adp@verify-aged2-6) | 10.319 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.786 (0.831) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.443 (0.443) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.236 (0.236) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.797 (0.867) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.446 | 11 | 152,294 (1.523) | yes | - |
| backlog-adp@blank-1 | 0 | 10.648 | 9 | 152,307 (1.523) | yes | - |
| backlog-adp@blank-2 | 0 | 10.781 | 10 | 151,306 (1.513) | yes | - |
| backlog-adp@blank-3 | 0 | 10.733 | 10 | 150,611 (1.506) | yes | - |
| backlog-adp@blank-4 | 0 | 10.683 | 10 | 150,939 (1.509) | yes | - |
| backlog-adp@blank-5 | 0 | 10.830 | 10 | 159,120 (1.591) | yes | - |
| backlog-adp@blank-6 | 0 | 10.899 | 11 | 158,245 (1.582) | yes | - |
| backlog-adp@blank-7 | 0 | 10.798 | 10 | 158,669 (1.587) | yes | - |
| backlog-adp@program-0 | 0 | 10.737 | 10 | 150,895 (1.509) | yes | - |
| backlog-adp@program-1 | 0 | 10.827 | 10 | 157,318 (1.573) | yes | - |
| backlog-adp@program-2 | 0 | 10.879 | 11 | 152,296 (1.523) | yes | - |
| backlog-adp@program-3 | 0 | 10.771 | 10 | 158,614 (1.586) | yes | - |
| backlog-adp@program-4 | 0 | 10.088 | 10 | 150,939 (1.509) | yes | - |
| backlog-adp@program-5 | 0 | 10.425 | 12 | 157,065 (1.571) | yes | - |
| backlog-adp@program-6 | 0 | 9.965 | 9 | 150,610 (1.506) | yes | - |
| backlog-adp@program-7 | 0 | 10.047 | 10 | 158,599 (1.586) | yes | - |
| backlog-adp@verify-0 | 0 | 11.545 | 11 | 152,895 (1.529) | yes | - |
| backlog-adp@verify-1 | 0 | 10.749 | 10 | 150,829 (1.508) | yes | - |
| backlog-adp@verify-2 | 0 | 10.696 | 10 | 158,135 (1.581) | yes | - |
| backlog-adp@verify-3 | 0 | 10.831 | 10 | 151,513 (1.515) | yes | - |
| backlog-adp@verify-4 | 0 | 10.782 | 10 | 150,818 (1.508) | yes | - |
| backlog-adp@verify-5 | 0 | 11.292 | 12 | 155,181 (1.552) | yes | - |
| backlog-adp@verify-6 | 0 | 11.000 | 11 | 157,434 (1.574) | yes | - |
| backlog-adp@verify-7 | 0 | 10.727 | 10 | 158,252 (1.583) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 11.513 | 9 | 157,286 (1.573) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 10.801 | 10 | 154,675 (1.547) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 10.748 | 10 | 155,141 (1.551) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 10.811 | 11 | 158,124 (1.581) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 10.811 | 10 | 157,031 (1.570) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 10.785 | 10 | 151,453 (1.515) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 10.757 | 10 | 150,727 (1.507) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 10.698 | 10 | 152,185 (1.522) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 11.815 | 10 | 157,100 (1.571) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 10.764 | 10 | 150,776 (1.508) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 10.727 | 10 | 158,245 (1.582) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 11.547 | 12 | 153,415 (1.534) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 11.324 | 11 | 154,523 (1.545) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 11.111 | 12 | 152,151 (1.522) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 10.726 | 10 | 150,707 (1.507) | yes | - |
| backlog-adp@blank-aged1-7 | 1 | 10.681 | 9 | 157,165 (1.572) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.475 | 13 | 155,183 (1.552) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 10.998 | 11 | 154,537 (1.545) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 10.778 | 10 | 151,465 (1.515) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 10.730 | 10 | 151,581 (1.516) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 10.734 | 10 | 150,855 (1.509) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 10.677 | 9 | 150,915 (1.509) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 10.817 | 10 | 159,075 (1.591) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 10.777 | 10 | 154,728 (1.547) | yes | - |
| backlog-adp@program-aged1-0 | 1 | 10.866 | 9 | 158,245 (1.582) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.847 | 10 | 153,031 (1.530) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 10.803 | 10 | 155,079 (1.551) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 10.864 | 11 | 152,264 (1.523) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 10.695 | 9 | 151,961 (1.520) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 10.845 | 10 | 156,189 (1.562) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 10.806 | 10 | 158,005 (1.580) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 10.751 | 10 | 158,779 (1.588) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.914 | 12 | 152,207 (1.522) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 10.472 | 9 | 150,820 (1.508) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 10.800 | 10 | 157,990 (1.580) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 10.754 | 10 | 157,031 (1.570) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 10.708 | 10 | 151,635 (1.516) | yes | - |
| backlog-adp@verify-aged2-5 | 1 | 11.175 | 11 | 152,482 (1.525) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 10.965 | 11 | 157,434 (1.574) | yes | - |
| backlog-adp@verify-aged2-7 | 1 | 10.700 | 9 | 157,167 (1.572) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 12.189 | 13 | 155,183 (1.552) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 10.910 | 12 | 158,124 (1.581) | yes | - |
| backlog-adp@verify-aged1-2 | 1 | 10.671 | 9 | 154,258 (1.543) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 10.716 | 10 | 151,635 (1.516) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 10.695 | 10 | 150,909 (1.509) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 10.652 | 9 | 152,015 (1.520) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 10.796 | 10 | 159,075 (1.591) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 12.443 | 12 | 154,086 (1.541) | yes | - |
| backlog | 0 | 6.618 | 8 | 154,817 (1.548) | yes | - |
| backlog-adp | 0 | 9.911 | 10 | 152,548 (1.525) | yes | - |
| backlog-adp-refill | 0 | 41.117 | 24 | 152,548 (1.525) | yes | - |
| backlog-owed | 0 | 65.318 | 24 | 154,925 (1.549) | yes | - |
| fixture | 0 | 1.445 | 2 | 84,778 (0.848) | yes | - |

Composed maximum over the 4 backlog windows: 154,925 CPU cycles (1.549 ms), backlog-owed.
Over the windows that released their whole load only: 154,925 (1.549 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 121192 | 0 | 54,315 (0.543) | fits |
| save-held | 3167 | 0 | 163,464 (1.635) | fits |
| save-starved | 57625 | 0 | 163,464 (1.635) | fits |
| acmp-notk | 3357 | 0 | 46,812 (0.468) | fits |
| backlog-adp@blank-0 | 556 | 0 | 152,294 (1.523) | fits |
| backlog-adp@blank-1 | 557 | 0 | 152,307 (1.523) | fits |
| backlog-adp@blank-2 | 557 | 0 | 151,306 (1.513) | fits |
| backlog-adp@blank-3 | 557 | 0 | 150,611 (1.506) | fits |
| backlog-adp@blank-4 | 557 | 0 | 150,939 (1.509) | fits |
| backlog-adp@blank-5 | 557 | 0 | 159,120 (1.591) | fits |
| backlog-adp@blank-6 | 558 | 0 | 158,245 (1.582) | fits |
| backlog-adp@blank-7 | 559 | 0 | 158,669 (1.587) | fits |
| backlog-adp@program-0 | 940 | 0 | 150,895 (1.509) | fits |
| backlog-adp@program-1 | 940 | 0 | 157,318 (1.573) | fits |
| backlog-adp@program-2 | 941 | 0 | 152,296 (1.523) | fits |
| backlog-adp@program-3 | 942 | 0 | 158,614 (1.586) | fits |
| backlog-adp@program-4 | 943 | 0 | 150,939 (1.509) | fits |
| backlog-adp@program-5 | 945 | 0 | 157,065 (1.571) | fits |
| backlog-adp@program-6 | 945 | 0 | 150,610 (1.506) | fits |
| backlog-adp@program-7 | 945 | 0 | 158,599 (1.586) | fits |
| backlog-adp@verify-0 | 1316 | 0 | 152,895 (1.529) | fits |
| backlog-adp@verify-1 | 1317 | 0 | 150,829 (1.508) | fits |
| backlog-adp@verify-2 | 1317 | 0 | 158,135 (1.581) | fits |
| backlog-adp@verify-3 | 1317 | 0 | 151,513 (1.515) | fits |
| backlog-adp@verify-4 | 1317 | 0 | 150,818 (1.508) | fits |
| backlog-adp@verify-5 | 1319 | 0 | 155,181 (1.552) | fits |
| backlog-adp@verify-6 | 1319 | 0 | 157,434 (1.574) | fits |
| backlog-adp@verify-7 | 1319 | 0 | 158,252 (1.583) | fits |
| backlog-adp@blank-aged2-0 | 795 | 0 | 157,286 (1.573) | fits |
| backlog-adp@blank-aged2-1 | 802 | 0 | 154,675 (1.547) | fits |
| backlog-adp@blank-aged2-2 | 808 | 0 | 155,141 (1.551) | fits |
| backlog-adp@blank-aged2-3 | 815 | 0 | 158,124 (1.581) | fits |
| backlog-adp@blank-aged2-4 | 821 | 0 | 157,031 (1.570) | fits |
| backlog-adp@blank-aged2-5 | 827 | 0 | 151,453 (1.515) | fits |
| backlog-adp@blank-aged2-6 | 833 | 0 | 150,727 (1.507) | fits |
| backlog-adp@blank-aged2-7 | 839 | 0 | 152,185 (1.522) | fits |
| backlog-adp@blank-aged1-0 | 746 | 0 | 157,100 (1.571) | fits |
| backlog-adp@blank-aged1-1 | 752 | 0 | 150,776 (1.508) | fits |
| backlog-adp@blank-aged1-2 | 758 | 0 | 158,245 (1.582) | fits |
| backlog-adp@blank-aged1-3 | 766 | 0 | 153,415 (1.534) | fits |
| backlog-adp@blank-aged1-4 | 772 | 0 | 154,523 (1.545) | fits |
| backlog-adp@blank-aged1-5 | 779 | 0 | 152,151 (1.522) | fits |
| backlog-adp@blank-aged1-6 | 783 | 0 | 150,707 (1.507) | fits |
| backlog-adp@blank-aged1-7 | 789 | 0 | 157,165 (1.572) | fits |
| backlog-adp@program-aged2-0 | 1178 | 0 | 155,183 (1.552) | fits |
| backlog-adp@program-aged2-1 | 1183 | 0 | 154,537 (1.545) | fits |
| backlog-adp@program-aged2-2 | 1188 | 0 | 152,886 (1.529) | fits |
| backlog-adp@program-aged2-3 | 1194 | 0 | 151,581 (1.516) | fits |
| backlog-adp@program-aged2-4 | 1200 | 0 | 150,855 (1.509) | fits |
| backlog-adp@program-aged2-5 | 1206 | 0 | 150,915 (1.509) | fits |
| backlog-adp@program-aged2-6 | 1213 | 0 | 159,075 (1.591) | fits |
| backlog-adp@program-aged2-7 | 1219 | 0 | 154,728 (1.547) | fits |
| backlog-adp@program-aged1-0 | 1125 | 0 | 158,245 (1.582) | fits |
| backlog-adp@program-aged1-1 | 1132 | 0 | 153,031 (1.530) | fits |
| backlog-adp@program-aged1-2 | 1138 | 0 | 155,079 (1.551) | fits |
| backlog-adp@program-aged1-3 | 1145 | 0 | 152,264 (1.523) | fits |
| backlog-adp@program-aged1-4 | 1150 | 0 | 151,961 (1.520) | fits |
| backlog-adp@program-aged1-5 | 1157 | 0 | 156,189 (1.562) | fits |
| backlog-adp@program-aged1-6 | 1163 | 0 | 158,005 (1.580) | fits |
| backlog-adp@program-aged1-7 | 1169 | 0 | 158,779 (1.588) | fits |
| backlog-adp@verify-aged2-0 | 1557 | 0 | 152,207 (1.522) | fits |
| backlog-adp@verify-aged2-1 | 1561 | 0 | 150,820 (1.508) | fits |
| backlog-adp@verify-aged2-2 | 1568 | 0 | 157,990 (1.580) | fits |
| backlog-adp@verify-aged2-3 | 1574 | 0 | 157,031 (1.570) | fits |
| backlog-adp@verify-aged2-4 | 1580 | 0 | 151,635 (1.516) | fits |
| backlog-adp@verify-aged2-5 | 1588 | 0 | 152,482 (1.525) | fits |
| backlog-adp@verify-aged2-6 | 1594 | 0 | 157,434 (1.574) | fits |
| backlog-adp@verify-aged2-7 | 1599 | 0 | 157,167 (1.572) | fits |
| backlog-adp@verify-aged1-0 | 1508 | 0 | 155,183 (1.552) | fits |
| backlog-adp@verify-aged1-1 | 1513 | 0 | 158,124 (1.581) | fits |
| backlog-adp@verify-aged1-2 | 1518 | 0 | 154,258 (1.543) | fits |
| backlog-adp@verify-aged1-3 | 1524 | 0 | 151,635 (1.516) | fits |
| backlog-adp@verify-aged1-4 | 1530 | 0 | 150,909 (1.509) | fits |
| backlog-adp@verify-aged1-5 | 1536 | 0 | 152,015 (1.520) | fits |
| backlog-adp@verify-aged1-6 | 1543 | 0 | 159,075 (1.591) | fits |
| backlog-adp@verify-aged1-7 | 1551 | 0 | 154,086 (1.541) | fits |
| adp-advertise | 598 | 0 | 34,491 (0.345) | fits |
| acmp-noresp | 1881 | 0 | 46,812 (0.468) | fits |
| save | 610 | 0 | 48,568 (0.486) | fits |
| srp | 290 | 0 | 44,339 (0.443) | fits |
| backlog | 287 | 0 | 154,817 (1.548) | fits |
| backlog-adp | 312 | 0 | 152,548 (1.525) | fits |
| backlog-adp-refill | 326 | 0 | 152,548 (1.525) | fits |
| backlog-owed | 309 | 0 | 154,925 (1.549) | fits |
| acmp-disc | 876 | 0 | 46,812 (0.468) | fits |
| maap | 179 | 0 | 34,491 (0.345) | fits |
| adp-link | 89 | 0 | 43,803 (0.438) | fits |
| adp-gm | 88 | 0 | 33,791 (0.338) | fits |
| adp-discover | 88 | 0 | 33,791 (0.338) | fits |
| control | 88 | 0 | 33,791 (0.338) | fits |
| aecp-fanout | 109 | 0 | 59,921 (0.599) | fits |
| acmp-cmd | 87 | 0 | 46,812 (0.468) | fits |
| aecp | 113 | 0 | 47,330 (0.473) | fits |
| datapath-events | 118 | 0 | 33,791 (0.338) | fits |
| fixture | 151 | 0 | 84,778 (0.848) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 8.920 (20) | 11.080 |
| backlog-adp@blank-aged2-1 | 2 | +8.997 ms, 76,670 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 10.149 (20) | 9.851 |
| backlog-adp@blank-aged2-2 | 2 | +8.091 ms, 76,670 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 10.095 (20) | 9.905 |
| backlog-adp@blank-aged2-3 | 2 | +7.242 ms, 76,696 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 10.164 (20) | 9.836 |
| backlog-adp@blank-aged2-4 | 2 | +5.624 ms, 76,861 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 10.163 (20) | 9.837 |
| backlog-adp@blank-aged2-5 | 2 | +5.414 ms, 76,861 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 10.137 (20) | 9.863 |
| backlog-adp@blank-aged2-6 | 2 | +4.542 ms, 76,577 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 10.111 (20) | 9.889 |
| backlog-adp@blank-aged2-7 | 2 | +2.989 ms, 76,753 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 10.045 (20) | 9.955 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 9.229 (20) | 10.771 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 9.357 (20) | 10.643 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 9.317 (20) | 10.683 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 9.250 (20) | 10.750 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 9.226 (20) | 10.774 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 9.366 (20) | 10.634 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 9.320 (20) | 10.680 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 9.274 (20) | 10.726 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 9.210 (20) | 10.790 |
| backlog-adp@program-aged2-1 | 2 | none | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 9.210 (20) | 10.790 |
| backlog-adp@program-aged2-2 | 2 | +7.943 ms, 80,565 (0.806 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 10.132 (20) | 9.868 |
| backlog-adp@program-aged2-3 | 2 | none | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 10.083 (20) | 9.917 |
| backlog-adp@program-aged2-4 | 2 | +5.324 ms, 80,758 (0.808 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 10.087 (20) | 9.913 |
| backlog-adp@program-aged2-5 | 2 | +5.433 ms, 80,665 (0.807 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 10.024 (20) | 9.976 |
| backlog-adp@program-aged2-6 | 2 | +4.828 ms, 80,376 (0.804 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 10.164 (20) | 9.836 |
| backlog-adp@program-aged2-7 | 2 | none | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 10.124 (20) | 9.876 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 8.938 (20) | 11.062 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 9.390 (20) | 10.610 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 9.346 (20) | 10.654 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 9.415 (20) | 10.585 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 9.242 (20) | 10.758 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 9.391 (20) | 10.609 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 9.353 (20) | 10.647 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 9.293 (20) | 10.707 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 9.211 (20) | 10.789 |
| backlog-adp@verify-aged2-1 | 2 | none | +9.267 ms, 77,685 (0.777 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 9.230 (20) | 10.770 |
| backlog-adp@verify-aged2-2 | 2 | +8.139 ms, 77,579 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 10.150 (20) | 9.850 |
| backlog-adp@verify-aged2-3 | 2 | +6.474 ms, 77,639 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 10.105 (20) | 9.895 |
| backlog-adp@verify-aged2-4 | 2 | +5.487 ms, 77,679 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 10.055 (20) | 9.945 |
| backlog-adp@verify-aged2-5 | 2 | +4.613 ms, 77,559 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 10.033 (20) | 9.967 |
| backlog-adp@verify-aged2-6 | 2 | +4.846 ms, 77,559 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 10.319 (20) | 9.681 |
| backlog-adp@verify-aged2-7 | 2 | +4.580 ms, 77,559 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 10.053 (20) | 9.947 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 9.246 (20) | 10.754 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 8.919 (20) | 11.081 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 9.257 (20) | 10.743 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 9.302 (20) | 10.698 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 9.280 (20) | 10.720 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 9.233 (20) | 10.767 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 9.375 (20) | 10.625 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 9.338 (20) | 10.662 |

Least margin over the aged windows: 9.681 ms, `backlog-adp@verify-aged2-6.service.srp.last.if0` at 10.319 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 22829.732 | 22,870 | 382 | 2 | 31.373 | yes | within |
| save-held | 4817.406 | 12,470 | 382 | - | 15.429 | no | within |
| save-starved | 12447.291 | 12,470 | 382 | - | 32.663 | yes | within |
| save | 4817.897 | 12,470 | 382 | - | 10.897 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1080 | 80,939 (0.809) | 77,810 (0.778) |
| save-held | 1562 | 100,948 (1.009) | 78,182 (0.782) |
| save-starved | 698 | 81,893 (0.819) | 78,289 (0.783) |
| acmp-notk | 1065 | 108,952 (1.090) | 78,420 (0.784) |
| backlog-adp@blank-0 | 339 | 95,900 (0.959) | 76,121 (0.761) |
| backlog-adp@blank-1 | 339 | 96,261 (0.963) | 76,121 (0.761) |
| backlog-adp@blank-2 | 339 | 96,123 (0.961) | 76,121 (0.761) |
| backlog-adp@blank-3 | 339 | 96,165 (0.962) | 76,121 (0.761) |
| backlog-adp@blank-4 | 339 | 96,584 (0.966) | 76,172 (0.762) |
| backlog-adp@blank-5 | 339 | 96,656 (0.967) | 76,172 (0.762) |
| backlog-adp@blank-6 | 339 | 95,745 (0.957) | 76,172 (0.762) |
| backlog-adp@blank-7 | 339 | 96,090 (0.961) | 76,172 (0.762) |
| backlog-adp@program-0 | 448 | 100,997 (1.010) | 78,725 (0.787) |
| backlog-adp@program-1 | 448 | 100,997 (1.010) | 78,725 (0.787) |
| backlog-adp@program-2 | 448 | 102,708 (1.027) | 78,644 (0.786) |
| backlog-adp@program-3 | 448 | 100,997 (1.010) | 78,776 (0.788) |
| backlog-adp@program-4 | 449 | 100,997 (1.010) | 78,197 (0.782) |
| backlog-adp@program-5 | 449 | 100,997 (1.010) | 78,197 (0.782) |
| backlog-adp@program-6 | 449 | 100,997 (1.010) | 78,197 (0.782) |
| backlog-adp@program-7 | 449 | 100,997 (1.010) | 78,197 (0.782) |
| backlog-adp@verify-0 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-1 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-2 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-3 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-4 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-5 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-6 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-7 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@blank-aged2-0 | 338 | 96,729 (0.967) | 76,250 (0.762) |
| backlog-adp@blank-aged2-1 | 337 | 79,578 (0.796) | 75,679 (0.757) |
| backlog-adp@blank-aged2-2 | 337 | 79,578 (0.796) | 75,679 (0.757) |
| backlog-adp@blank-aged2-3 | 337 | 79,578 (0.796) | 75,679 (0.757) |
| backlog-adp@blank-aged2-4 | 337 | 79,578 (0.796) | 75,730 (0.757) |
| backlog-adp@blank-aged2-5 | 337 | 79,578 (0.796) | 75,730 (0.757) |
| backlog-adp@blank-aged2-6 | 337 | 79,578 (0.796) | 75,347 (0.753) |
| backlog-adp@blank-aged2-7 | 337 | 79,578 (0.796) | 75,497 (0.755) |
| backlog-adp@blank-aged1-0 | 338 | 96,230 (0.962) | 76,252 (0.763) |
| backlog-adp@blank-aged1-1 | 337 | 96,359 (0.964) | 76,201 (0.762) |
| backlog-adp@blank-aged1-2 | 337 | 96,613 (0.966) | 76,201 (0.762) |
| backlog-adp@blank-aged1-3 | 337 | 96,769 (0.968) | 76,201 (0.762) |
| backlog-adp@blank-aged1-4 | 337 | 96,820 (0.968) | 76,252 (0.763) |
| backlog-adp@blank-aged1-5 | 337 | 95,113 (0.951) | 76,170 (0.762) |
| backlog-adp@blank-aged1-6 | 337 | 96,230 (0.962) | 76,252 (0.763) |
| backlog-adp@blank-aged1-7 | 337 | 96,188 (0.962) | 76,252 (0.763) |
| backlog-adp@program-aged2-0 | 447 | 100,997 (1.010) | 78,776 (0.788) |
| backlog-adp@program-aged2-1 | 446 | 100,997 (1.010) | 78,509 (0.785) |
| backlog-adp@program-aged2-2 | 446 | 100,997 (1.010) | 78,349 (0.783) |
| backlog-adp@program-aged2-3 | 446 | 100,997 (1.010) | 78,520 (0.785) |
| backlog-adp@program-aged2-4 | 446 | 100,997 (1.010) | 78,484 (0.785) |
| backlog-adp@program-aged2-5 | 446 | 100,997 (1.010) | 78,482 (0.785) |
| backlog-adp@program-aged2-6 | 446 | 100,997 (1.010) | 78,197 (0.782) |
| backlog-adp@program-aged2-7 | 446 | 100,997 (1.010) | 78,197 (0.782) |
| backlog-adp@program-aged1-0 | 447 | 100,997 (1.010) | 78,774 (0.788) |
| backlog-adp@program-aged1-1 | 446 | 100,997 (1.010) | 78,725 (0.787) |
| backlog-adp@program-aged1-2 | 446 | 100,997 (1.010) | 78,725 (0.787) |
| backlog-adp@program-aged1-3 | 446 | 100,997 (1.010) | 78,776 (0.788) |
| backlog-adp@program-aged1-4 | 446 | 100,997 (1.010) | 78,776 (0.788) |
| backlog-adp@program-aged1-5 | 446 | 100,997 (1.010) | 78,776 (0.788) |
| backlog-adp@program-aged1-6 | 446 | 100,997 (1.010) | 78,776 (0.788) |
| backlog-adp@program-aged1-7 | 446 | 100,997 (1.010) | 78,776 (0.788) |
| backlog-adp@verify-aged2-0 | 556 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged2-1 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged2-2 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged2-3 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged2-4 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged2-5 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged2-6 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged2-7 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged1-0 | 556 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged1-1 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged1-2 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged1-3 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged1-4 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged1-5 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged1-6 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged1-7 | 556 | 104,873 (1.049) | 78,338 (0.783) |
| adp-advertise | 577 | 26,414 (0.264) | 2,374 (0.024) |
| acmp-noresp | 615 | 108,538 (1.085) | 78,338 (0.783) |
| save | 585 | 100,831 (1.008) | 78,036 (0.780) |
| srp | 271 | 26,388 (0.264) | 2,374 (0.024) |
| backlog | 265 | 26,388 (0.264) | 2,374 (0.024) |
| backlog-adp | 271 | 26,388 (0.264) | 2,378 (0.024) |
| backlog-adp-refill | 274 | 26,388 (0.264) | 2,376 (0.024) |
| backlog-owed | 277 | 26,388 (0.264) | 2,374 (0.024) |
| acmp-disc | 306 | 108,527 (1.085) | 75,606 (0.756) |
| maap | 166 | 26,163 (0.262) | 2,374 (0.024) |
| adp-link | 79 | 26,162 (0.262) | 2,374 (0.024) |
| adp-gm | 79 | 26,162 (0.262) | 2,374 (0.024) |
| adp-discover | 79 | 26,162 (0.262) | 2,374 (0.024) |
| control | 79 | 26,162 (0.262) | 2,374 (0.024) |
| aecp-fanout | 79 | 26,162 (0.262) | 2,374 (0.024) |
| acmp-cmd | 66 | 26,162 (0.262) | 2,374 (0.024) |
| aecp | 80 | 26,162 (0.262) | 2,374 (0.024) |
| datapath-events | 70 | 26,162 (0.262) | 2,374 (0.024) |
| fixture | 54 | 24,307 (0.243) | 2,374 (0.024) |

Longest pass that carries a step: 108,952 CPU cycles (1.090 ms), acmp-notk; longest step: 78,776 (0.788 ms), backlog-adp@program-3.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 262,659 | 2.627 | 20 | 200 | fits | 100,135 | 124 | 0.466 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 242,522 | 2.425 | 20 | 20 | fits | 100,135 | 124 | 0.466 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 311,204 | 3.112 | 20 | 24 | fits | 88,436 | 55 | 0.589 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 181,439 | 1.814 | 20 | 50 | fits | 81,651 | 106 | 0.438 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 829,564 | 8.296 | 20 | 20 | fits | 59,656 | 24 | 0.684 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 119,858 | 1.199 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 116,283 | 1.163 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 262,893 | 2.629 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 266,129 | 2.661 | 20 | 200 | fits | 103,605 | 130 | 0.490 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 296,992 | 2.970 | 20 | 20 | fits | 86,337 | 61 | 0.618 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 282,021 | 2.820 | 20 | 24 | fits | 85,293 | 66 | 0.473 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 206,517 | 2.065 | 20 | 50 | fits | 103,605 | 130 | 0.490 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 875,730 | 8.757 | 20 | 20 | fits | 53,715 | 26 | 0.731 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 186,381 | 1.864 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 152,541 | 1.525 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 266,344 | 2.663 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 10,984 | 0.110 | 20 | 20 | fits | 39,242 | 19 (14) | 0.889 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 473,405 | 4.734 | 20 | 20 | fits | 150,400 | 186 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 376,491 | 3.765 | 20 | 200 | fits | 152,294 | 197 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 526,275 | 5.263 | 20 | 200 | fits | 150,400 | 186 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 377,415 | 3.774 | 20 | 20 | fits | 152,294 | 197 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 610,602 | 6.106 | 20 | 20 | fits | 83,623 | 37 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 218,996 | 2.190 | 20 | 24 | fits | 149,483 | 146 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 380,065 | 3.801 | 20 | 24 | fits | 152,294 | 197 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 379,999 | 3.800 | 20 | 50 | fits | 152,294 | 197 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 530,003 | 5.300 | 20 | 50 | fits | 150,400 | 186 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 613,560 | 6.136 | 20 | 20 | fits | 83,623 | 37 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,004,385 | 10.044 | 20 | 20 | fits | 41,031 | 25 | 0.831 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 389,917 | 3.899 | 20 | 20 | fits | 150,752 | 215 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 293,475 | 2.935 | 20 | 200 | fits | 152,307 | 201 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 443,611 | 4.436 | 20 | 200 | fits | 150,752 | 215 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 294,399 | 2.944 | 20 | 20 | fits | 152,307 | 201 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 528,304 | 5.283 | 20 | 20 | fits | 83,989 | 37 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 145,732 | 1.457 | 20 | 24 | fits | 147,302 | 105 | 0.361 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 297,049 | 2.970 | 20 | 24 | fits | 152,307 | 201 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 296,983 | 2.970 | 20 | 50 | fits | 152,307 | 201 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 447,339 | 4.473 | 20 | 50 | fits | 150,752 | 215 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 531,262 | 5.313 | 20 | 20 | fits | 83,989 | 37 | 0.733 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 924,062 | 9.241 | 20 | 20 | fits | 47,398 | 22 | 0.793 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 413,887 | 4.139 | 20 | 20 | fits | 149,301 | 201 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 308,549 | 3.085 | 20 | 200 | fits | 151,306 | 176 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 457,234 | 4.572 | 20 | 200 | fits | 149,301 | 201 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 309,473 | 3.095 | 20 | 20 | fits | 151,306 | 176 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 541,448 | 5.414 | 20 | 20 | fits | 83,510 | 37 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 161,807 | 1.618 | 20 | 24 | fits | 148,996 | 145 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 312,123 | 3.121 | 20 | 24 | fits | 151,306 | 176 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 312,057 | 3.121 | 20 | 50 | fits | 151,306 | 176 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 460,962 | 4.610 | 20 | 50 | fits | 149,301 | 201 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 544,406 | 5.444 | 20 | 20 | fits | 83,510 | 37 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 937,489 | 9.375 | 20 | 20 | fits | 50,192 | 20 | 0.703 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 399,205 | 3.992 | 20 | 20 | fits | 150,372 | 186 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 302,278 | 3.023 | 20 | 200 | fits | 150,611 | 192 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 452,034 | 4.520 | 20 | 200 | fits | 150,372 | 186 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 303,202 | 3.032 | 20 | 20 | fits | 150,611 | 192 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 536,523 | 5.365 | 20 | 20 | fits | 83,785 | 38 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 156,231 | 1.562 | 20 | 24 | fits | 148,996 | 145 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 305,852 | 3.059 | 20 | 24 | fits | 150,611 | 192 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 305,786 | 3.058 | 20 | 50 | fits | 150,611 | 192 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 455,762 | 4.558 | 20 | 50 | fits | 150,372 | 186 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 539,481 | 5.395 | 20 | 20 | fits | 83,785 | 38 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 932,733 | 9.327 | 20 | 20 | fits | 50,390 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 393,582 | 3.936 | 20 | 20 | fits | 150,939 | 186 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 296,682 | 2.967 | 20 | 200 | fits | 150,591 | 192 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 447,005 | 4.470 | 20 | 200 | fits | 150,939 | 186 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 297,606 | 2.976 | 20 | 20 | fits | 150,591 | 192 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 543,799 | 5.438 | 20 | 20 | fits | 85,834 | 48 | 0.761 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 150,655 | 1.507 | 20 | 24 | fits | 148,996 | 145 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 300,256 | 3.003 | 20 | 24 | fits | 150,591 | 192 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 300,190 | 3.002 | 20 | 50 | fits | 150,591 | 192 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 450,733 | 4.507 | 20 | 50 | fits | 150,939 | 186 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 546,757 | 5.468 | 20 | 20 | fits | 85,834 | 48 | 0.761 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 927,296 | 9.273 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 437,848 | 4.378 | 20 | 20 | fits | 159,120 | 207 | 0.474 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 313,719 | 3.137 | 20 | 200 | fits | 153,235 | 181 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 482,298 | 4.823 | 20 | 200 | fits | 159,120 | 207 | 0.474 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 314,643 | 3.146 | 20 | 20 | fits | 153,235 | 181 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 567,083 | 5.671 | 20 | 20 | fits | 84,081 | 37 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 165,048 | 1.650 | 20 | 24 | fits | 149,061 | 145 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 317,293 | 3.173 | 20 | 24 | fits | 153,235 | 181 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 317,227 | 3.172 | 20 | 50 | fits | 153,235 | 181 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 486,026 | 4.860 | 20 | 50 | fits | 159,120 | 207 | 0.474 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 570,041 | 5.700 | 20 | 20 | fits | 84,081 | 37 | 0.733 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 941,917 | 9.419 | 20 | 20 | fits | 32,958 | 12 | 0.832 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 431,899 | 4.319 | 20 | 20 | fits | 158,245 | 205 | 0.459 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 317,354 | 3.174 | 20 | 200 | fits | 152,792 | 181 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 474,983 | 4.750 | 20 | 200 | fits | 158,245 | 205 | 0.459 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 318,278 | 3.183 | 20 | 20 | fits | 152,792 | 181 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 559,617 | 5.596 | 20 | 20 | fits | 83,930 | 37 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 159,608 | 1.596 | 20 | 24 | fits | 149,197 | 146 | 0.375 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 320,928 | 3.209 | 20 | 24 | fits | 152,792 | 181 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 320,862 | 3.209 | 20 | 50 | fits | 152,792 | 181 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 478,711 | 4.787 | 20 | 50 | fits | 158,245 | 205 | 0.459 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 562,575 | 5.626 | 20 | 20 | fits | 83,930 | 37 | 0.733 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 949,842 | 9.498 | 20 | 20 | fits | 37,473 | 19 | 0.843 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 411,376 | 4.114 | 20 | 20 | fits | 158,669 | 208 | 0.417 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 306,374 | 3.064 | 20 | 200 | fits | 149,775 | 174 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 464,427 | 4.644 | 20 | 200 | fits | 158,669 | 208 | 0.417 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 307,298 | 3.073 | 20 | 20 | fits | 149,775 | 174 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 548,878 | 5.489 | 20 | 20 | fits | 83,747 | 37 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 161,163 | 1.612 | 20 | 24 | fits | 149,134 | 145 | 0.372 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 309,948 | 3.099 | 20 | 24 | fits | 149,775 | 174 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 309,882 | 3.099 | 20 | 50 | fits | 149,775 | 174 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 468,155 | 4.682 | 20 | 50 | fits | 158,669 | 208 | 0.417 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 551,836 | 5.518 | 20 | 20 | fits | 83,747 | 37 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 939,244 | 9.392 | 20 | 20 | fits | 41,974 | 16 | 0.770 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 395,717 | 3.957 | 20 | 20 | fits | 150,517 | 186 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 298,790 | 2.988 | 20 | 200 | fits | 150,895 | 192 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 448,691 | 4.487 | 20 | 200 | fits | 150,517 | 186 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 299,714 | 2.997 | 20 | 20 | fits | 150,895 | 192 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 532,485 | 5.325 | 20 | 20 | fits | 83,090 | 37 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 152,459 | 1.525 | 20 | 24 | fits | 148,774 | 145 | 0.371 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 302,364 | 3.024 | 20 | 24 | fits | 150,895 | 192 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 302,298 | 3.023 | 20 | 50 | fits | 150,895 | 192 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 452,419 | 4.524 | 20 | 50 | fits | 150,517 | 186 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 535,443 | 5.354 | 20 | 20 | fits | 83,090 | 37 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 928,434 | 9.284 | 20 | 20 | fits | 47,149 | 22 | 0.788 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 412,593 | 4.126 | 20 | 20 | fits | 157,318 | 205 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 310,041 | 3.100 | 20 | 200 | fits | 153,329 | 180 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 466,743 | 4.667 | 20 | 200 | fits | 157,318 | 205 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 310,965 | 3.110 | 20 | 20 | fits | 153,329 | 180 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 564,372 | 5.644 | 20 | 20 | fits | 86,416 | 38 | 0.764 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 161,276 | 1.613 | 20 | 24 | fits | 148,839 | 145 | 0.371 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 313,615 | 3.136 | 20 | 24 | fits | 153,329 | 180 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 313,549 | 3.135 | 20 | 50 | fits | 153,329 | 180 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 470,471 | 4.705 | 20 | 50 | fits | 157,318 | 205 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 567,330 | 5.673 | 20 | 20 | fits | 86,416 | 38 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 937,101 | 9.371 | 20 | 20 | fits | 32,958 | 12 | 0.832 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 404,672 | 4.047 | 20 | 20 | fits | 150,400 | 186 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 307,758 | 3.078 | 20 | 200 | fits | 152,296 | 197 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 457,542 | 4.575 | 20 | 200 | fits | 150,400 | 186 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 308,682 | 3.087 | 20 | 20 | fits | 152,296 | 197 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 540,717 | 5.407 | 20 | 20 | fits | 82,471 | 41 | 0.762 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 150,260 | 1.503 | 20 | 24 | fits | 148,975 | 146 | 0.372 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 311,332 | 3.113 | 20 | 24 | fits | 152,296 | 197 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 311,266 | 3.113 | 20 | 50 | fits | 152,296 | 197 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 461,270 | 4.613 | 20 | 50 | fits | 150,400 | 186 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 543,675 | 5.437 | 20 | 20 | fits | 82,471 | 41 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 929,237 | 9.292 | 20 | 20 | fits | 46,674 | 23 | 0.779 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 402,914 | 4.029 | 20 | 20 | fits | 158,614 | 207 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 298,346 | 2.983 | 20 | 200 | fits | 150,426 | 174 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 456,344 | 4.563 | 20 | 200 | fits | 158,614 | 207 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 299,270 | 2.993 | 20 | 20 | fits | 150,426 | 174 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 540,111 | 5.401 | 20 | 20 | fits | 83,063 | 37 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 152,484 | 1.525 | 20 | 24 | fits | 148,990 | 145 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 301,920 | 3.019 | 20 | 24 | fits | 150,426 | 174 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 301,854 | 3.019 | 20 | 50 | fits | 150,426 | 174 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 460,072 | 4.601 | 20 | 50 | fits | 158,614 | 207 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 543,069 | 5.431 | 20 | 20 | fits | 83,063 | 37 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 932,028 | 9.320 | 20 | 20 | fits | 41,615 | 16 | 0.760 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 405,754 | 4.058 | 20 | 20 | fits | 150,939 | 186 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 308,854 | 3.089 | 20 | 200 | fits | 150,812 | 192 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 459,177 | 4.592 | 20 | 200 | fits | 150,939 | 186 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 309,778 | 3.098 | 20 | 20 | fits | 150,812 | 192 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 557,629 | 5.576 | 20 | 20 | fits | 87,245 | 44 | 0.740 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 162,606 | 1.626 | 20 | 24 | fits | 149,767 | 145 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 312,428 | 3.124 | 20 | 24 | fits | 150,812 | 192 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 312,362 | 3.124 | 20 | 50 | fits | 150,812 | 192 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 462,905 | 4.629 | 20 | 50 | fits | 150,939 | 186 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 560,587 | 5.606 | 20 | 20 | fits | 87,245 | 44 | 0.740 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 938,569 | 9.386 | 20 | 20 | fits | 38,841 | 18 | 0.848 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 414,522 | 4.145 | 20 | 20 | fits | 157,065 | 204 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 311,977 | 3.120 | 20 | 200 | fits | 154,715 | 185 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 468,426 | 4.684 | 20 | 200 | fits | 157,065 | 204 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 312,901 | 3.129 | 20 | 20 | fits | 154,715 | 185 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 551,205 | 5.512 | 20 | 20 | fits | 82,075 | 31 | 0.753 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 152,061 | 1.521 | 20 | 24 | fits | 149,076 | 146 | 0.372 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 315,551 | 3.156 | 20 | 24 | fits | 154,715 | 185 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 315,485 | 3.155 | 20 | 50 | fits | 154,715 | 185 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 472,154 | 4.722 | 20 | 50 | fits | 157,065 | 204 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 554,163 | 5.542 | 20 | 20 | fits | 82,075 | 31 | 0.753 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 923,597 | 9.236 | 20 | 20 | fits | 32,958 | 12 | 0.832 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 391,463 | 3.915 | 20 | 20 | fits | 150,372 | 186 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 294,536 | 2.945 | 20 | 200 | fits | 150,610 | 192 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 444,292 | 4.443 | 20 | 200 | fits | 150,372 | 186 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 295,460 | 2.955 | 20 | 20 | fits | 150,610 | 192 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 527,550 | 5.276 | 20 | 20 | fits | 82,554 | 41 | 0.762 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 148,490 | 1.485 | 20 | 24 | fits | 148,874 | 145 | 0.371 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 298,110 | 2.981 | 20 | 24 | fits | 150,610 | 192 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 298,044 | 2.980 | 20 | 50 | fits | 150,610 | 192 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 448,020 | 4.480 | 20 | 50 | fits | 150,372 | 186 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 530,508 | 5.305 | 20 | 20 | fits | 82,554 | 41 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 926,629 | 9.266 | 20 | 20 | fits | 50,331 | 20 | 0.704 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 417,016 | 4.170 | 20 | 20 | fits | 158,599 | 207 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 302,833 | 3.028 | 20 | 200 | fits | 150,220 | 174 | 0.449 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 460,816 | 4.608 | 20 | 200 | fits | 158,599 | 207 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 303,757 | 3.038 | 20 | 20 | fits | 150,220 | 174 | 0.449 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 559,309 | 5.593 | 20 | 20 | fits | 87,437 | 44 | 0.741 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 157,177 | 1.572 | 20 | 24 | fits | 148,809 | 145 | 0.371 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 306,407 | 3.064 | 20 | 24 | fits | 150,220 | 174 | 0.449 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 306,341 | 3.063 | 20 | 50 | fits | 150,220 | 174 | 0.449 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 464,544 | 4.645 | 20 | 50 | fits | 158,599 | 207 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 562,267 | 5.623 | 20 | 20 | fits | 87,437 | 44 | 0.741 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 934,305 | 9.343 | 20 | 20 | fits | 32,958 | 12 | 0.832 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 491,887 | 4.919 | 20 | 20 | fits | 149,406 | 201 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 386,485 | 3.865 | 20 | 200 | fits | 152,895 | 181 | 0.430 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 535,275 | 5.353 | 20 | 200 | fits | 149,406 | 201 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 387,409 | 3.874 | 20 | 20 | fits | 152,895 | 181 | 0.430 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 619,340 | 6.193 | 20 | 20 | fits | 83,361 | 37 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 228,388 | 2.284 | 20 | 24 | fits | 149,524 | 146 | 0.375 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 390,059 | 3.901 | 20 | 24 | fits | 152,895 | 181 | 0.430 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 389,993 | 3.900 | 20 | 50 | fits | 152,895 | 181 | 0.430 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 539,003 | 5.390 | 20 | 50 | fits | 149,406 | 201 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 622,298 | 6.223 | 20 | 20 | fits | 83,361 | 37 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,013,123 | 10.131 | 20 | 20 | fits | 41,031 | 25 | 0.831 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 399,711 | 3.997 | 20 | 20 | fits | 150,829 | 185 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 302,811 | 3.028 | 20 | 200 | fits | 150,798 | 192 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 453,024 | 4.530 | 20 | 200 | fits | 150,829 | 185 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 303,735 | 3.037 | 20 | 20 | fits | 150,798 | 192 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 537,288 | 5.373 | 20 | 20 | fits | 83,560 | 37 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 156,577 | 1.566 | 20 | 24 | fits | 148,963 | 145 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 306,385 | 3.064 | 20 | 24 | fits | 150,798 | 192 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 306,319 | 3.063 | 20 | 50 | fits | 150,798 | 192 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 456,752 | 4.568 | 20 | 50 | fits | 150,829 | 185 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 540,246 | 5.402 | 20 | 20 | fits | 83,560 | 37 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 933,130 | 9.331 | 20 | 20 | fits | 47,395 | 22 | 0.793 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 385,026 | 3.850 | 20 | 20 | fits | 158,135 | 205 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 299,742 | 2.997 | 20 | 200 | fits | 153,252 | 180 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 457,261 | 4.573 | 20 | 200 | fits | 158,135 | 205 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 300,666 | 3.007 | 20 | 20 | fits | 153,252 | 180 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 540,784 | 5.408 | 20 | 20 | fits | 82,819 | 31 | 0.756 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 151,054 | 1.511 | 20 | 24 | fits | 148,963 | 145 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 303,316 | 3.033 | 20 | 24 | fits | 153,252 | 180 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 303,250 | 3.033 | 20 | 50 | fits | 153,252 | 180 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 460,989 | 4.610 | 20 | 50 | fits | 158,135 | 205 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 543,742 | 5.437 | 20 | 20 | fits | 82,819 | 31 | 0.756 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 928,080 | 9.281 | 20 | 20 | fits | 41,476 | 16 | 0.759 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 417,604 | 4.176 | 20 | 20 | fits | 149,446 | 201 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 312,266 | 3.123 | 20 | 200 | fits | 151,513 | 176 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 461,096 | 4.611 | 20 | 200 | fits | 149,446 | 201 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 313,190 | 3.132 | 20 | 20 | fits | 151,513 | 176 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 545,323 | 5.453 | 20 | 20 | fits | 83,523 | 38 | 0.726 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 165,317 | 1.653 | 20 | 24 | fits | 148,898 | 145 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 315,840 | 3.158 | 20 | 24 | fits | 151,513 | 176 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 315,774 | 3.158 | 20 | 50 | fits | 151,513 | 176 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 464,824 | 4.648 | 20 | 50 | fits | 149,446 | 201 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 548,281 | 5.483 | 20 | 20 | fits | 83,523 | 38 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 941,533 | 9.415 | 20 | 20 | fits | 50,390 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 402,922 | 4.029 | 20 | 20 | fits | 150,659 | 187 | 0.427 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 305,995 | 3.060 | 20 | 200 | fits | 150,818 | 192 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 456,038 | 4.560 | 20 | 200 | fits | 150,659 | 187 | 0.427 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 306,919 | 3.069 | 20 | 20 | fits | 150,818 | 192 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 552,812 | 5.528 | 20 | 20 | fits | 85,808 | 48 | 0.761 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 159,741 | 1.597 | 20 | 24 | fits | 148,898 | 145 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 309,569 | 3.096 | 20 | 24 | fits | 150,818 | 192 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 309,503 | 3.095 | 20 | 50 | fits | 150,818 | 192 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 459,766 | 4.598 | 20 | 50 | fits | 150,659 | 187 | 0.427 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 555,770 | 5.558 | 20 | 20 | fits | 85,808 | 48 | 0.761 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 936,309 | 9.363 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 411,210 | 4.112 | 20 | 20 | fits | 155,181 | 192 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 300,641 | 3.006 | 20 | 200 | fits | 151,040 | 193 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 465,243 | 4.652 | 20 | 200 | fits | 155,181 | 192 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 301,565 | 3.016 | 20 | 20 | fits | 151,040 | 193 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 548,857 | 5.489 | 20 | 20 | fits | 82,910 | 41 | 0.762 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 154,165 | 1.542 | 20 | 24 | fits | 148,898 | 145 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 304,215 | 3.042 | 20 | 24 | fits | 151,040 | 193 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 304,149 | 3.041 | 20 | 50 | fits | 151,040 | 193 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 468,971 | 4.690 | 20 | 50 | fits | 155,181 | 192 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 551,815 | 5.518 | 20 | 20 | fits | 82,910 | 41 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 932,291 | 9.323 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 402,878 | 4.029 | 20 | 20 | fits | 157,434 | 201 | 0.472 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 308,281 | 3.083 | 20 | 200 | fits | 154,592 | 185 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 465,099 | 4.651 | 20 | 200 | fits | 157,434 | 201 | 0.472 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 309,205 | 3.092 | 20 | 20 | fits | 154,592 | 185 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 549,641 | 5.496 | 20 | 20 | fits | 83,838 | 37 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 148,734 | 1.487 | 20 | 24 | fits | 149,043 | 146 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 311,855 | 3.119 | 20 | 24 | fits | 154,592 | 185 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 311,789 | 3.118 | 20 | 50 | fits | 154,592 | 185 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 468,827 | 4.688 | 20 | 50 | fits | 157,434 | 201 | 0.472 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 552,599 | 5.526 | 20 | 20 | fits | 83,838 | 37 | 0.733 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 924,546 | 9.245 | 20 | 20 | fits | 33,048 | 13 | 0.828 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 413,056 | 4.131 | 20 | 20 | fits | 158,252 | 206 | 0.416 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 298,894 | 2.989 | 20 | 200 | fits | 150,415 | 174 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 456,530 | 4.565 | 20 | 200 | fits | 158,252 | 206 | 0.416 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 299,818 | 2.998 | 20 | 20 | fits | 150,415 | 174 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 540,738 | 5.407 | 20 | 20 | fits | 83,504 | 37 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 153,043 | 1.530 | 20 | 24 | fits | 149,002 | 146 | 0.372 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 302,468 | 3.025 | 20 | 24 | fits | 150,415 | 174 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 302,402 | 3.024 | 20 | 50 | fits | 150,415 | 174 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 460,258 | 4.603 | 20 | 50 | fits | 158,252 | 206 | 0.416 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 543,696 | 5.437 | 20 | 20 | fits | 83,504 | 37 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 931,131 | 9.311 | 20 | 20 | fits | 42,006 | 16 | 0.770 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 397,459 | 3.975 | 20 | 20 | fits | 157,286 | 205 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 294,907 | 2.949 | 20 | 200 | fits | 154,387 | 185 | 0.423 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 451,577 | 4.516 | 20 | 200 | fits | 157,286 | 205 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 295,831 | 2.958 | 20 | 20 | fits | 154,387 | 185 | 0.423 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 549,981 | 5.500 | 20 | 20 | fits | 87,265 | 38 | 0.767 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 145,084 | 1.451 | 20 | 24 | fits | 148,100 | 142 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 298,481 | 2.985 | 20 | 24 | fits | 154,387 | 185 | 0.423 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 298,415 | 2.984 | 20 | 50 | fits | 154,387 | 185 | 0.423 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 455,305 | 4.553 | 20 | 50 | fits | 157,286 | 205 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 552,939 | 5.529 | 20 | 20 | fits | 87,265 | 38 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 892,000 | 8.920 | 20 | 20 | fits | 85,126 | 36 | 0.566 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 407,718 | 4.077 | 20 | 20 | fits | 154,675 | 193 | 0.442 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 306,433 | 3.064 | 20 | 200 | fits | 150,796 | 192 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 460,492 | 4.605 | 20 | 200 | fits | 154,675 | 193 | 0.442 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 307,357 | 3.074 | 20 | 20 | fits | 150,796 | 192 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 556,705 | 5.567 | 20 | 20 | fits | 85,072 | 38 | 0.740 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 160,201 | 1.602 | 20 | 24 | fits | 148,035 | 142 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 310,007 | 3.100 | 20 | 24 | fits | 150,796 | 192 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 309,941 | 3.099 | 20 | 50 | fits | 150,796 | 192 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 464,220 | 4.642 | 20 | 50 | fits | 154,675 | 193 | 0.442 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 559,663 | 5.597 | 20 | 20 | fits | 85,072 | 38 | 0.740 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 1,014,850 | 10.149 | 20 | 20 | fits | 42,237 | 17 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 412,727 | 4.127 | 20 | 20 | fits | 155,141 | 192 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 301,741 | 3.017 | 20 | 200 | fits | 150,948 | 193 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 466,572 | 4.666 | 20 | 200 | fits | 155,141 | 192 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 302,665 | 3.027 | 20 | 20 | fits | 150,948 | 193 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 551,294 | 5.513 | 20 | 20 | fits | 84,018 | 37 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 155,357 | 1.554 | 20 | 24 | fits | 148,035 | 142 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 305,315 | 3.053 | 20 | 24 | fits | 150,948 | 193 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 305,249 | 3.052 | 20 | 50 | fits | 150,948 | 193 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 470,300 | 4.703 | 20 | 50 | fits | 155,141 | 192 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 554,252 | 5.543 | 20 | 20 | fits | 84,018 | 37 | 0.733 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,009,466 | 10.095 | 20 | 20 | fits | 41,786 | 16 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 395,949 | 3.959 | 20 | 20 | fits | 158,124 | 205 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 310,572 | 3.106 | 20 | 200 | fits | 154,636 | 185 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 468,080 | 4.681 | 20 | 200 | fits | 158,124 | 205 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 311,496 | 3.115 | 20 | 20 | fits | 154,636 | 185 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 551,684 | 5.517 | 20 | 20 | fits | 82,900 | 31 | 0.757 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 150,680 | 1.507 | 20 | 24 | fits | 148,202 | 143 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 314,146 | 3.141 | 20 | 24 | fits | 154,636 | 185 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 314,080 | 3.141 | 20 | 50 | fits | 154,636 | 185 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 471,808 | 4.718 | 20 | 50 | fits | 158,124 | 205 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 554,642 | 5.546 | 20 | 20 | fits | 82,900 | 31 | 0.757 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,016,421 | 10.164 | 20 | 20 | fits | 42,042 | 16 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 412,999 | 4.130 | 20 | 20 | fits | 157,031 | 204 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 310,447 | 3.104 | 20 | 200 | fits | 153,192 | 180 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 466,862 | 4.669 | 20 | 200 | fits | 157,031 | 204 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 311,371 | 3.114 | 20 | 20 | fits | 153,192 | 180 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 557,769 | 5.578 | 20 | 20 | fits | 90,203 | 39 | 0.757 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 161,819 | 1.618 | 20 | 24 | fits | 148,207 | 142 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 314,021 | 3.140 | 20 | 24 | fits | 153,192 | 180 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 313,955 | 3.140 | 20 | 50 | fits | 153,192 | 180 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 470,590 | 4.706 | 20 | 50 | fits | 157,031 | 204 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 560,727 | 5.607 | 20 | 20 | fits | 90,203 | 39 | 0.757 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,016,338 | 10.163 | 20 | 20 | fits | 32,899 | 12 | 0.831 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 409,802 | 4.098 | 20 | 20 | fits | 149,301 | 201 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 304,464 | 3.045 | 20 | 200 | fits | 151,453 | 176 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 453,149 | 4.531 | 20 | 200 | fits | 149,301 | 201 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 305,388 | 3.054 | 20 | 20 | fits | 151,453 | 176 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 536,742 | 5.367 | 20 | 20 | fits | 82,889 | 41 | 0.761 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 157,575 | 1.576 | 20 | 24 | fits | 148,207 | 142 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 308,038 | 3.080 | 20 | 24 | fits | 151,453 | 176 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 307,972 | 3.080 | 20 | 50 | fits | 151,453 | 176 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 456,877 | 4.569 | 20 | 50 | fits | 149,301 | 201 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 539,700 | 5.397 | 20 | 20 | fits | 82,889 | 41 | 0.761 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,013,730 | 10.137 | 20 | 20 | fits | 50,192 | 20 | 0.703 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 405,636 | 4.056 | 20 | 20 | fits | 149,998 | 184 | 0.469 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 299,494 | 2.995 | 20 | 200 | fits | 150,727 | 192 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 448,876 | 4.489 | 20 | 200 | fits | 149,998 | 184 | 0.469 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 300,418 | 3.004 | 20 | 20 | fits | 150,727 | 192 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 615,575 | 6.156 | 20 | 20 | fits | 89,418 | 50 | 0.718 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 153,331 | 1.533 | 20 | 24 | fits | 148,207 | 142 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 303,068 | 3.031 | 20 | 24 | fits | 150,727 | 192 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 303,002 | 3.030 | 20 | 50 | fits | 150,727 | 192 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 452,604 | 4.526 | 20 | 50 | fits | 149,998 | 184 | 0.469 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 618,533 | 6.185 | 20 | 20 | fits | 89,418 | 50 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,011,075 | 10.111 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 479,273 | 4.793 | 20 | 20 | fits | 152,185 | 205 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 294,179 | 2.942 | 20 | 200 | fits | 149,656 | 174 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 522,501 | 5.225 | 20 | 200 | fits | 152,185 | 205 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 295,103 | 2.951 | 20 | 20 | fits | 149,656 | 174 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 620,540 | 6.205 | 20 | 20 | fits | 86,651 | 43 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 149,087 | 1.491 | 20 | 24 | fits | 148,207 | 142 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 297,753 | 2.978 | 20 | 24 | fits | 149,656 | 174 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 297,687 | 2.977 | 20 | 50 | fits | 149,656 | 174 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 526,229 | 5.262 | 20 | 50 | fits | 152,185 | 205 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 623,498 | 6.235 | 20 | 20 | fits | 86,651 | 43 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,004,535 | 10.045 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 385,978 | 3.860 | 20 | 20 | fits | 157,100 | 151 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 142,845 | 1.428 | 20 | 200 | fits | 151,824 | 234 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 447,918 | 4.479 | 20 | 200 | fits | 157,100 | 151 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 143,769 | 1.438 | 20 | 20 | fits | 151,824 | 234 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 532,276 | 5.323 | 20 | 20 | fits | 83,654 | 37 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 295,998 | 2.960 | 20 | 24 | fits | 148,589 | 142 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 452,108 | 4.521 | 20 | 24 | fits | 157,100 | 151 | 0.460 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 146,353 | 1.464 | 20 | 50 | fits | 151,824 | 234 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 145,957 | 1.460 | 20 | 50 | fits | 151,824 | 234 | 0.411 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 535,234 | 5.352 | 20 | 20 | fits | 83,654 | 37 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 922,915 | 9.229 | 20 | 20 | fits | 41,615 | 16 | 0.760 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 401,937 | 4.019 | 20 | 20 | fits | 150,684 | 185 | 0.431 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 305,037 | 3.050 | 20 | 200 | fits | 150,776 | 192 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 455,105 | 4.551 | 20 | 200 | fits | 150,684 | 185 | 0.431 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 305,961 | 3.060 | 20 | 20 | fits | 150,776 | 192 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 539,612 | 5.396 | 20 | 20 | fits | 83,803 | 38 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 158,825 | 1.588 | 20 | 24 | fits | 148,058 | 142 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 308,611 | 3.086 | 20 | 24 | fits | 150,776 | 192 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 308,545 | 3.085 | 20 | 50 | fits | 150,776 | 192 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 458,833 | 4.588 | 20 | 50 | fits | 150,684 | 185 | 0.431 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 542,570 | 5.426 | 20 | 20 | fits | 83,803 | 38 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 935,697 | 9.357 | 20 | 20 | fits | 47,347 | 22 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 387,962 | 3.880 | 20 | 20 | fits | 158,245 | 206 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 302,678 | 3.027 | 20 | 200 | fits | 153,261 | 180 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 460,307 | 4.603 | 20 | 200 | fits | 158,245 | 206 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 303,602 | 3.036 | 20 | 20 | fits | 153,261 | 180 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 558,886 | 5.589 | 20 | 20 | fits | 87,392 | 38 | 0.768 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 153,981 | 1.540 | 20 | 24 | fits | 148,058 | 142 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 306,252 | 3.063 | 20 | 24 | fits | 153,261 | 180 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 306,186 | 3.062 | 20 | 50 | fits | 153,261 | 180 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 464,035 | 4.640 | 20 | 50 | fits | 158,245 | 206 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 561,844 | 5.618 | 20 | 20 | fits | 87,392 | 38 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 931,676 | 9.317 | 20 | 20 | fits | 32,958 | 12 | 0.832 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 414,628 | 4.146 | 20 | 20 | fits | 151,353 | 201 | 0.454 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 297,988 | 2.980 | 20 | 200 | fits | 153,415 | 181 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 458,992 | 4.590 | 20 | 200 | fits | 151,353 | 201 | 0.454 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 298,912 | 2.989 | 20 | 20 | fits | 153,415 | 181 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 543,761 | 5.438 | 20 | 20 | fits | 84,065 | 37 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 149,137 | 1.491 | 20 | 24 | fits | 148,058 | 142 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 301,562 | 3.016 | 20 | 24 | fits | 153,415 | 181 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 301,496 | 3.015 | 20 | 50 | fits | 153,415 | 181 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 462,720 | 4.627 | 20 | 50 | fits | 151,353 | 201 | 0.454 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 546,719 | 5.467 | 20 | 20 | fits | 84,065 | 37 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 925,028 | 9.250 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 412,140 | 4.121 | 20 | 20 | fits | 154,523 | 224 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 291,444 | 2.914 | 20 | 200 | fits | 149,592 | 195 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 455,580 | 4.556 | 20 | 200 | fits | 154,523 | 224 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 292,368 | 2.924 | 20 | 20 | fits | 149,592 | 195 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 539,128 | 5.391 | 20 | 20 | fits | 82,844 | 41 | 0.762 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 146,416 | 1.464 | 20 | 24 | fits | 150,181 | 111 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 295,018 | 2.950 | 20 | 24 | fits | 149,592 | 195 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 294,952 | 2.950 | 20 | 50 | fits | 149,592 | 195 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 459,308 | 4.593 | 20 | 50 | fits | 154,523 | 224 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 542,086 | 5.421 | 20 | 20 | fits | 82,844 | 41 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 922,562 | 9.226 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 423,219 | 4.232 | 20 | 20 | fits | 150,458 | 183 | 0.474 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 317,070 | 3.171 | 20 | 200 | fits | 152,151 | 197 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 466,912 | 4.669 | 20 | 200 | fits | 150,458 | 183 | 0.474 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 317,994 | 3.180 | 20 | 20 | fits | 152,151 | 197 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 552,986 | 5.530 | 20 | 20 | fits | 85,370 | 42 | 0.718 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 159,663 | 1.597 | 20 | 24 | fits | 148,246 | 143 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 320,644 | 3.206 | 20 | 24 | fits | 152,151 | 197 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 320,578 | 3.206 | 20 | 50 | fits | 152,151 | 197 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 470,640 | 4.706 | 20 | 50 | fits | 150,458 | 183 | 0.474 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 555,944 | 5.559 | 20 | 20 | fits | 85,370 | 42 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 936,607 | 9.366 | 20 | 20 | fits | 41,764 | 17 | 0.758 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 403,027 | 4.030 | 20 | 20 | fits | 150,331 | 183 | 0.474 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 296,891 | 2.969 | 20 | 200 | fits | 150,707 | 192 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 446,606 | 4.466 | 20 | 200 | fits | 150,331 | 183 | 0.474 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 297,815 | 2.978 | 20 | 20 | fits | 150,707 | 192 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 532,714 | 5.327 | 20 | 20 | fits | 85,404 | 42 | 0.718 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 150,748 | 1.507 | 20 | 24 | fits | 148,184 | 142 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 300,465 | 3.005 | 20 | 24 | fits | 150,707 | 192 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 300,399 | 3.004 | 20 | 50 | fits | 150,707 | 192 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 450,334 | 4.503 | 20 | 50 | fits | 150,331 | 183 | 0.474 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 535,672 | 5.357 | 20 | 20 | fits | 85,404 | 42 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 931,954 | 9.320 | 20 | 20 | fits | 50,331 | 20 | 0.704 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 390,512 | 3.905 | 20 | 20 | fits | 157,165 | 201 | 0.469 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 296,070 | 2.961 | 20 | 200 | fits | 154,318 | 185 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 452,619 | 4.526 | 20 | 200 | fits | 157,165 | 201 | 0.469 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 296,994 | 2.970 | 20 | 20 | fits | 154,318 | 185 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 537,310 | 5.373 | 20 | 20 | fits | 83,987 | 37 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 146,316 | 1.463 | 20 | 24 | fits | 148,184 | 142 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 299,644 | 2.996 | 20 | 24 | fits | 154,318 | 185 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 299,578 | 2.996 | 20 | 50 | fits | 154,318 | 185 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 456,347 | 4.563 | 20 | 50 | fits | 157,165 | 201 | 0.469 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 540,268 | 5.403 | 20 | 20 | fits | 83,987 | 37 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 927,442 | 9.274 | 20 | 20 | fits | 41,476 | 16 | 0.759 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 408,292 | 4.083 | 20 | 20 | fits | 155,183 | 192 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 297,264 | 2.973 | 20 | 200 | fits | 150,966 | 193 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 462,137 | 4.621 | 20 | 200 | fits | 155,183 | 192 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 298,188 | 2.982 | 20 | 20 | fits | 150,966 | 193 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 546,208 | 5.462 | 20 | 20 | fits | 83,367 | 37 | 0.731 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 150,862 | 1.509 | 20 | 24 | fits | 148,029 | 142 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 300,838 | 3.008 | 20 | 24 | fits | 150,966 | 193 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 300,772 | 3.008 | 20 | 50 | fits | 150,966 | 193 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 465,865 | 4.659 | 20 | 50 | fits | 155,183 | 192 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 549,166 | 5.492 | 20 | 20 | fits | 83,367 | 37 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 921,023 | 9.210 | 20 | 20 | fits | 32,958 | 12 | 0.832 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 394,167 | 3.942 | 20 | 20 | fits | 150,885 | 201 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 306,119 | 3.061 | 20 | 200 | fits | 154,537 | 185 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 456,388 | 4.564 | 20 | 200 | fits | 150,885 | 201 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 307,043 | 3.070 | 20 | 20 | fits | 154,537 | 185 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 540,295 | 5.403 | 20 | 20 | fits | 83,203 | 37 | 0.731 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 146,326 | 1.463 | 20 | 24 | fits | 148,241 | 143 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 309,693 | 3.097 | 20 | 24 | fits | 154,537 | 185 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 309,627 | 3.096 | 20 | 50 | fits | 154,537 | 185 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 460,116 | 4.601 | 20 | 50 | fits | 150,885 | 201 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 543,253 | 5.433 | 20 | 20 | fits | 83,203 | 37 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 921,020 | 9.210 | 20 | 20 | fits | 38,868 | 19 | 0.844 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 408,948 | 4.089 | 20 | 20 | fits | 150,856 | 215 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 302,805 | 3.028 | 20 | 200 | fits | 151,465 | 199 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 453,045 | 4.530 | 20 | 200 | fits | 150,856 | 215 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 303,729 | 3.037 | 20 | 20 | fits | 151,465 | 199 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 536,800 | 5.368 | 20 | 20 | fits | 83,051 | 37 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 146,223 | 1.462 | 20 | 24 | fits | 152,886 | 118 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 306,379 | 3.064 | 20 | 24 | fits | 151,465 | 199 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 306,313 | 3.063 | 20 | 50 | fits | 151,465 | 199 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 456,773 | 4.568 | 20 | 50 | fits | 150,856 | 215 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 539,758 | 5.398 | 20 | 20 | fits | 83,051 | 37 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,013,232 | 10.132 | 20 | 20 | fits | 45,940 | 23 | 0.787 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 405,165 | 4.052 | 20 | 20 | fits | 149,301 | 201 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 299,827 | 2.998 | 20 | 200 | fits | 151,581 | 176 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 448,512 | 4.485 | 20 | 200 | fits | 149,301 | 201 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 300,751 | 3.008 | 20 | 20 | fits | 151,581 | 176 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 532,081 | 5.321 | 20 | 20 | fits | 82,865 | 37 | 0.726 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 152,810 | 1.528 | 20 | 24 | fits | 148,006 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 303,401 | 3.034 | 20 | 24 | fits | 151,581 | 176 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 303,335 | 3.033 | 20 | 50 | fits | 151,581 | 176 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 452,240 | 4.522 | 20 | 50 | fits | 149,301 | 201 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 535,039 | 5.350 | 20 | 20 | fits | 82,865 | 37 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,008,290 | 10.083 | 20 | 20 | fits | 50,192 | 20 | 0.703 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 391,688 | 3.917 | 20 | 20 | fits | 150,372 | 186 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 294,761 | 2.948 | 20 | 200 | fits | 150,855 | 192 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 444,517 | 4.445 | 20 | 200 | fits | 150,372 | 186 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 295,685 | 2.957 | 20 | 20 | fits | 150,855 | 192 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 527,697 | 5.277 | 20 | 20 | fits | 82,476 | 41 | 0.761 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 148,470 | 1.485 | 20 | 24 | fits | 148,006 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 298,335 | 2.983 | 20 | 24 | fits | 150,855 | 192 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 298,269 | 2.983 | 20 | 50 | fits | 150,855 | 192 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 448,245 | 4.482 | 20 | 50 | fits | 150,372 | 186 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 530,655 | 5.307 | 20 | 20 | fits | 82,476 | 41 | 0.761 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,008,662 | 10.087 | 20 | 20 | fits | 50,391 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 388,661 | 3.887 | 20 | 20 | fits | 150,915 | 216 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 292,155 | 2.922 | 20 | 200 | fits | 150,466 | 198 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 442,454 | 4.425 | 20 | 200 | fits | 150,915 | 216 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 293,079 | 2.931 | 20 | 20 | fits | 150,466 | 198 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 538,595 | 5.386 | 20 | 20 | fits | 85,034 | 48 | 0.759 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 146,253 | 1.463 | 20 | 24 | fits | 150,129 | 111 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 295,729 | 2.957 | 20 | 24 | fits | 150,466 | 198 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 295,663 | 2.957 | 20 | 50 | fits | 150,466 | 198 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 446,182 | 4.462 | 20 | 50 | fits | 150,915 | 216 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 541,553 | 5.416 | 20 | 20 | fits | 85,034 | 48 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,002,426 | 10.024 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 433,057 | 4.331 | 20 | 20 | fits | 159,075 | 207 | 0.473 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 308,875 | 3.089 | 20 | 200 | fits | 153,474 | 181 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 477,421 | 4.774 | 20 | 200 | fits | 159,075 | 207 | 0.473 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 309,799 | 3.098 | 20 | 20 | fits | 153,474 | 181 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 641,541 | 6.415 | 20 | 20 | fits | 83,040 | 38 | 0.726 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 159,965 | 1.600 | 20 | 24 | fits | 148,071 | 142 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 312,449 | 3.124 | 20 | 24 | fits | 153,474 | 181 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 312,383 | 3.124 | 20 | 50 | fits | 153,474 | 181 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 481,149 | 4.811 | 20 | 50 | fits | 159,075 | 207 | 0.473 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 644,499 | 6.445 | 20 | 20 | fits | 83,040 | 38 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,016,435 | 10.164 | 20 | 20 | fits | 32,958 | 12 | 0.832 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 509,931 | 5.099 | 20 | 20 | fits | 154,728 | 208 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 299,922 | 2.999 | 20 | 200 | fits | 148,861 | 171 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 543,482 | 5.435 | 20 | 200 | fits | 154,728 | 208 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 300,846 | 3.008 | 20 | 20 | fits | 148,861 | 171 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 628,860 | 6.289 | 20 | 20 | fits | 84,674 | 42 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 155,625 | 1.556 | 20 | 24 | fits | 148,071 | 142 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 303,496 | 3.035 | 20 | 24 | fits | 148,861 | 171 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 303,430 | 3.034 | 20 | 50 | fits | 148,861 | 171 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 547,210 | 5.472 | 20 | 50 | fits | 154,728 | 208 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 631,818 | 6.318 | 20 | 20 | fits | 84,674 | 42 | 0.714 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,012,410 | 10.124 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 381,358 | 3.814 | 20 | 20 | fits | 158,245 | 206 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 296,074 | 2.961 | 20 | 200 | fits | 154,500 | 185 | 0.424 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 453,703 | 4.537 | 20 | 200 | fits | 158,245 | 206 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 296,998 | 2.970 | 20 | 20 | fits | 154,500 | 185 | 0.424 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 551,619 | 5.516 | 20 | 20 | fits | 86,673 | 38 | 0.766 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 146,138 | 1.461 | 20 | 24 | fits | 148,006 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 299,648 | 2.996 | 20 | 24 | fits | 154,500 | 185 | 0.424 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 299,582 | 2.996 | 20 | 50 | fits | 154,500 | 185 | 0.424 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 457,431 | 4.574 | 20 | 50 | fits | 158,245 | 206 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 554,577 | 5.546 | 20 | 20 | fits | 86,673 | 38 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 893,808 | 8.938 | 20 | 20 | fits | 85,126 | 36 | 0.566 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 419,179 | 4.192 | 20 | 20 | fits | 153,031 | 206 | 0.436 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 309,483 | 3.095 | 20 | 200 | fits | 151,635 | 176 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 461,898 | 4.619 | 20 | 200 | fits | 153,031 | 206 | 0.436 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 310,407 | 3.104 | 20 | 20 | fits | 151,635 | 176 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 557,634 | 5.576 | 20 | 20 | fits | 84,456 | 38 | 0.738 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 162,412 | 1.624 | 20 | 24 | fits | 148,071 | 142 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 313,057 | 3.131 | 20 | 24 | fits | 151,635 | 176 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 312,991 | 3.130 | 20 | 50 | fits | 151,635 | 176 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 465,626 | 4.656 | 20 | 50 | fits | 153,031 | 206 | 0.436 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 560,592 | 5.606 | 20 | 20 | fits | 84,456 | 38 | 0.738 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 938,986 | 9.390 | 20 | 20 | fits | 42,114 | 16 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 415,722 | 4.157 | 20 | 20 | fits | 155,079 | 193 | 0.458 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 304,403 | 3.044 | 20 | 200 | fits | 151,081 | 193 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 469,228 | 4.692 | 20 | 200 | fits | 155,079 | 193 | 0.458 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 305,327 | 3.053 | 20 | 20 | fits | 151,081 | 193 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 553,338 | 5.533 | 20 | 20 | fits | 83,406 | 37 | 0.731 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 157,886 | 1.579 | 20 | 24 | fits | 148,071 | 142 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 307,977 | 3.080 | 20 | 24 | fits | 151,081 | 193 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 307,911 | 3.079 | 20 | 50 | fits | 151,081 | 193 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 472,956 | 4.730 | 20 | 50 | fits | 155,079 | 193 | 0.458 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 556,296 | 5.563 | 20 | 20 | fits | 83,406 | 37 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 934,605 | 9.346 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 408,078 | 4.081 | 20 | 20 | fits | 150,800 | 185 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 311,103 | 3.111 | 20 | 200 | fits | 152,264 | 197 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 461,287 | 4.613 | 20 | 200 | fits | 150,800 | 185 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 312,027 | 3.120 | 20 | 20 | fits | 152,264 | 197 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 545,065 | 5.451 | 20 | 20 | fits | 83,074 | 37 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 153,527 | 1.535 | 20 | 24 | fits | 148,238 | 143 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 314,677 | 3.147 | 20 | 24 | fits | 152,264 | 197 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 314,611 | 3.146 | 20 | 50 | fits | 152,264 | 197 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 465,015 | 4.650 | 20 | 50 | fits | 150,800 | 185 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 548,023 | 5.480 | 20 | 20 | fits | 83,074 | 37 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 941,502 | 9.415 | 20 | 20 | fits | 46,108 | 23 | 0.789 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 388,826 | 3.888 | 20 | 20 | fits | 150,684 | 185 | 0.431 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 291,926 | 2.919 | 20 | 200 | fits | 151,961 | 197 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 441,994 | 4.420 | 20 | 200 | fits | 150,684 | 185 | 0.431 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 292,850 | 2.929 | 20 | 20 | fits | 151,961 | 197 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 525,185 | 5.252 | 20 | 20 | fits | 82,487 | 41 | 0.761 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 144,529 | 1.445 | 20 | 24 | fits | 148,096 | 142 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 295,500 | 2.955 | 20 | 24 | fits | 151,961 | 197 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 295,434 | 2.954 | 20 | 50 | fits | 151,961 | 197 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 445,722 | 4.457 | 20 | 50 | fits | 150,684 | 185 | 0.431 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 528,143 | 5.281 | 20 | 20 | fits | 82,487 | 41 | 0.761 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 924,162 | 9.242 | 20 | 20 | fits | 50,722 | 20 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 421,096 | 4.211 | 20 | 20 | fits | 156,189 | 200 | 0.462 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 309,406 | 3.094 | 20 | 200 | fits | 153,320 | 180 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 464,979 | 4.650 | 20 | 200 | fits | 156,189 | 200 | 0.462 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 310,330 | 3.103 | 20 | 20 | fits | 153,320 | 180 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 548,971 | 5.490 | 20 | 20 | fits | 83,288 | 37 | 0.731 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 160,650 | 1.607 | 20 | 24 | fits | 148,178 | 142 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 312,980 | 3.130 | 20 | 24 | fits | 153,320 | 180 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 312,914 | 3.129 | 20 | 50 | fits | 153,320 | 180 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 468,707 | 4.687 | 20 | 50 | fits | 156,189 | 200 | 0.462 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 551,929 | 5.519 | 20 | 20 | fits | 83,288 | 37 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 939,103 | 9.391 | 20 | 20 | fits | 41,476 | 16 | 0.759 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 417,842 | 4.178 | 20 | 20 | fits | 158,005 | 205 | 0.456 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 303,423 | 3.034 | 20 | 200 | fits | 151,581 | 176 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 460,812 | 4.608 | 20 | 200 | fits | 158,005 | 205 | 0.456 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 304,347 | 3.043 | 20 | 20 | fits | 151,581 | 176 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 544,972 | 5.450 | 20 | 20 | fits | 83,456 | 38 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 156,406 | 1.564 | 20 | 24 | fits | 148,178 | 142 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 306,997 | 3.070 | 20 | 24 | fits | 151,581 | 176 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 306,931 | 3.069 | 20 | 50 | fits | 151,581 | 176 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 464,540 | 4.645 | 20 | 50 | fits | 158,005 | 205 | 0.456 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 547,930 | 5.479 | 20 | 20 | fits | 83,456 | 38 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 935,348 | 9.353 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 402,424 | 4.024 | 20 | 20 | fits | 158,779 | 209 | 0.416 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 297,422 | 2.974 | 20 | 200 | fits | 149,824 | 174 | 0.445 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 455,585 | 4.556 | 20 | 200 | fits | 158,779 | 209 | 0.416 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 298,346 | 2.983 | 20 | 20 | fits | 149,824 | 174 | 0.445 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 554,263 | 5.543 | 20 | 20 | fits | 87,622 | 44 | 0.743 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 152,162 | 1.522 | 20 | 24 | fits | 148,178 | 142 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 300,996 | 3.010 | 20 | 24 | fits | 149,824 | 174 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 300,930 | 3.009 | 20 | 50 | fits | 149,824 | 174 | 0.445 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 459,313 | 4.593 | 20 | 50 | fits | 158,779 | 209 | 0.416 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 557,221 | 5.572 | 20 | 20 | fits | 87,622 | 44 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 929,339 | 9.293 | 20 | 20 | fits | 32,958 | 12 | 0.832 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 409,249 | 4.092 | 20 | 20 | fits | 150,400 | 186 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 312,335 | 3.123 | 20 | 200 | fits | 152,207 | 197 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 462,119 | 4.621 | 20 | 200 | fits | 150,400 | 186 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 313,259 | 3.133 | 20 | 20 | fits | 152,207 | 197 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 546,331 | 5.463 | 20 | 20 | fits | 83,508 | 37 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 154,872 | 1.549 | 20 | 24 | fits | 148,080 | 143 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 315,909 | 3.159 | 20 | 24 | fits | 152,207 | 197 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 315,843 | 3.158 | 20 | 50 | fits | 152,207 | 197 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 465,847 | 4.658 | 20 | 50 | fits | 150,400 | 186 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 549,289 | 5.493 | 20 | 20 | fits | 83,508 | 37 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 921,146 | 9.211 | 20 | 20 | fits | 32,958 | 12 | 0.832 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 389,573 | 3.896 | 20 | 20 | fits | 150,820 | 216 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 292,539 | 2.925 | 20 | 200 | fits | 150,560 | 198 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 442,743 | 4.427 | 20 | 200 | fits | 150,820 | 216 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 293,463 | 2.935 | 20 | 20 | fits | 150,560 | 198 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 527,164 | 5.272 | 20 | 20 | fits | 83,717 | 37 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 146,543 | 1.465 | 20 | 24 | fits | 150,170 | 111 | 0.372 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 296,113 | 2.961 | 20 | 24 | fits | 150,560 | 198 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 296,047 | 2.960 | 20 | 50 | fits | 150,560 | 198 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 446,471 | 4.465 | 20 | 50 | fits | 150,820 | 216 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 530,122 | 5.301 | 20 | 20 | fits | 83,717 | 37 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 922,965 | 9.230 | 20 | 20 | fits | 47,414 | 22 | 0.793 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 394,244 | 3.942 | 20 | 20 | fits | 157,990 | 205 | 0.431 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 308,960 | 3.090 | 20 | 200 | fits | 153,374 | 180 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 466,334 | 4.663 | 20 | 200 | fits | 157,990 | 205 | 0.431 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 309,884 | 3.099 | 20 | 20 | fits | 153,374 | 180 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 549,857 | 5.499 | 20 | 20 | fits | 82,819 | 31 | 0.756 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 160,150 | 1.601 | 20 | 24 | fits | 148,112 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 312,534 | 3.125 | 20 | 24 | fits | 153,374 | 180 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 312,468 | 3.125 | 20 | 50 | fits | 153,374 | 180 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 470,062 | 4.701 | 20 | 50 | fits | 157,990 | 205 | 0.431 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 552,815 | 5.528 | 20 | 20 | fits | 82,819 | 31 | 0.756 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,014,977 | 10.150 | 20 | 20 | fits | 41,588 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 407,082 | 4.071 | 20 | 20 | fits | 157,031 | 204 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 304,530 | 3.045 | 20 | 200 | fits | 153,374 | 180 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 460,945 | 4.609 | 20 | 200 | fits | 157,031 | 204 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 305,454 | 3.055 | 20 | 20 | fits | 153,374 | 180 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 548,880 | 5.489 | 20 | 20 | fits | 87,231 | 38 | 0.759 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 155,720 | 1.557 | 20 | 24 | fits | 148,112 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 308,104 | 3.081 | 20 | 24 | fits | 153,374 | 180 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 308,038 | 3.080 | 20 | 50 | fits | 153,374 | 180 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 464,673 | 4.647 | 20 | 50 | fits | 157,031 | 204 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 551,838 | 5.518 | 20 | 20 | fits | 87,231 | 38 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,010,466 | 10.105 | 20 | 20 | fits | 32,958 | 12 | 0.832 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 403,699 | 4.037 | 20 | 20 | fits | 149,556 | 202 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 298,361 | 2.984 | 20 | 200 | fits | 151,635 | 176 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 447,301 | 4.473 | 20 | 200 | fits | 149,556 | 202 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 299,285 | 2.993 | 20 | 20 | fits | 151,635 | 176 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 544,079 | 5.441 | 20 | 20 | fits | 85,862 | 48 | 0.761 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 151,290 | 1.513 | 20 | 24 | fits | 148,112 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 301,935 | 3.019 | 20 | 24 | fits | 151,635 | 176 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 301,869 | 3.019 | 20 | 50 | fits | 151,635 | 176 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 451,029 | 4.510 | 20 | 50 | fits | 149,556 | 202 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 547,037 | 5.470 | 20 | 20 | fits | 85,862 | 48 | 0.761 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,005,544 | 10.055 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 412,550 | 4.125 | 20 | 20 | fits | 152,482 | 189 | 0.481 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 293,957 | 2.940 | 20 | 200 | fits | 152,277 | 198 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 455,949 | 4.559 | 20 | 200 | fits | 152,482 | 189 | 0.481 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 294,881 | 2.949 | 20 | 20 | fits | 152,277 | 198 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 619,639 | 6.196 | 20 | 20 | fits | 85,427 | 43 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 146,244 | 1.462 | 20 | 24 | fits | 148,112 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 297,531 | 2.975 | 20 | 24 | fits | 152,277 | 198 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 297,465 | 2.975 | 20 | 50 | fits | 152,277 | 198 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 459,677 | 4.597 | 20 | 50 | fits | 152,482 | 189 | 0.481 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 622,597 | 6.226 | 20 | 20 | fits | 85,427 | 43 | 0.712 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,003,334 | 10.033 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 417,030 | 4.170 | 20 | 20 | fits | 157,434 | 201 | 0.472 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 322,433 | 3.224 | 20 | 200 | fits | 154,703 | 185 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 479,251 | 4.793 | 20 | 200 | fits | 157,434 | 201 | 0.472 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 323,357 | 3.234 | 20 | 20 | fits | 154,703 | 185 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 641,323 | 6.413 | 20 | 20 | fits | 83,809 | 38 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 162,636 | 1.626 | 20 | 24 | fits | 148,223 | 143 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 326,007 | 3.260 | 20 | 24 | fits | 154,703 | 185 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 325,941 | 3.259 | 20 | 50 | fits | 154,703 | 185 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 482,979 | 4.830 | 20 | 50 | fits | 157,434 | 201 | 0.472 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 644,281 | 6.443 | 20 | 20 | fits | 83,809 | 38 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,031,853 | 10.319 | 20 | 20 | fits | 42,006 | 16 | 0.770 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 390,480 | 3.905 | 20 | 20 | fits | 157,167 | 201 | 0.469 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 296,038 | 2.960 | 20 | 200 | fits | 154,204 | 185 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 452,589 | 4.526 | 20 | 200 | fits | 157,167 | 201 | 0.469 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 296,962 | 2.970 | 20 | 20 | fits | 154,204 | 185 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 614,661 | 6.147 | 20 | 20 | fits | 83,809 | 38 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 146,398 | 1.464 | 20 | 24 | fits | 149,558 | 147 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 299,612 | 2.996 | 20 | 24 | fits | 154,204 | 185 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 299,546 | 2.995 | 20 | 50 | fits | 154,204 | 185 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 456,317 | 4.563 | 20 | 50 | fits | 157,167 | 201 | 0.469 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 617,619 | 6.176 | 20 | 20 | fits | 83,809 | 38 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,005,291 | 10.053 | 20 | 20 | fits | 41,615 | 16 | 0.760 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 411,229 | 4.112 | 20 | 20 | fits | 155,183 | 192 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 300,145 | 3.001 | 20 | 200 | fits | 150,966 | 193 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 465,074 | 4.651 | 20 | 200 | fits | 155,183 | 192 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 301,069 | 3.011 | 20 | 20 | fits | 150,966 | 193 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 549,753 | 5.498 | 20 | 20 | fits | 83,975 | 37 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 153,743 | 1.537 | 20 | 24 | fits | 147,963 | 142 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 303,719 | 3.037 | 20 | 24 | fits | 150,966 | 193 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 303,653 | 3.037 | 20 | 50 | fits | 150,966 | 193 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 468,802 | 4.688 | 20 | 50 | fits | 155,183 | 192 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 552,711 | 5.527 | 20 | 20 | fits | 83,975 | 37 | 0.733 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 924,568 | 9.246 | 20 | 20 | fits | 32,958 | 12 | 0.832 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 394,382 | 3.944 | 20 | 20 | fits | 158,124 | 205 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 309,005 | 3.090 | 20 | 200 | fits | 154,672 | 185 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 466,513 | 4.665 | 20 | 200 | fits | 158,124 | 205 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 309,929 | 3.099 | 20 | 20 | fits | 154,672 | 185 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 550,080 | 5.501 | 20 | 20 | fits | 82,863 | 31 | 0.757 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 149,021 | 1.490 | 20 | 24 | fits | 148,175 | 143 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 312,579 | 3.126 | 20 | 24 | fits | 154,672 | 185 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 312,513 | 3.125 | 20 | 50 | fits | 154,672 | 185 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 470,241 | 4.702 | 20 | 50 | fits | 158,124 | 205 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 553,038 | 5.530 | 20 | 20 | fits | 82,863 | 31 | 0.757 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 891,937 | 8.919 | 20 | 20 | fits | 85,126 | 36 | 0.566 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 399,730 | 3.997 | 20 | 20 | fits | 150,471 | 201 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 294,079 | 2.941 | 20 | 200 | fits | 154,258 | 185 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 443,934 | 4.439 | 20 | 200 | fits | 150,471 | 201 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 295,003 | 2.950 | 20 | 20 | fits | 154,258 | 185 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 528,297 | 5.283 | 20 | 20 | fits | 83,659 | 37 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 144,385 | 1.444 | 20 | 24 | fits | 149,475 | 147 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 297,653 | 2.977 | 20 | 24 | fits | 154,258 | 185 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 297,587 | 2.976 | 20 | 50 | fits | 154,258 | 185 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 447,662 | 4.477 | 20 | 50 | fits | 150,471 | 201 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 531,255 | 5.313 | 20 | 20 | fits | 83,659 | 37 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 925,732 | 9.257 | 20 | 20 | fits | 51,454 | 21 | 0.729 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 406,310 | 4.063 | 20 | 20 | fits | 149,301 | 201 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 300,972 | 3.010 | 20 | 200 | fits | 151,635 | 176 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 449,657 | 4.497 | 20 | 200 | fits | 149,301 | 201 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 301,896 | 3.019 | 20 | 20 | fits | 151,635 | 176 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 533,834 | 5.338 | 20 | 20 | fits | 83,473 | 37 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 153,901 | 1.539 | 20 | 24 | fits | 148,089 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 304,546 | 3.045 | 20 | 24 | fits | 151,635 | 176 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 304,480 | 3.045 | 20 | 50 | fits | 151,635 | 176 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 453,385 | 4.534 | 20 | 50 | fits | 149,301 | 201 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 536,792 | 5.368 | 20 | 20 | fits | 83,473 | 37 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 930,151 | 9.302 | 20 | 20 | fits | 50,331 | 20 | 0.704 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 392,743 | 3.927 | 20 | 20 | fits | 150,372 | 186 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 295,816 | 2.958 | 20 | 200 | fits | 150,909 | 192 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 445,572 | 4.456 | 20 | 200 | fits | 150,372 | 186 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 296,740 | 2.967 | 20 | 20 | fits | 150,909 | 192 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 529,360 | 5.294 | 20 | 20 | fits | 83,084 | 41 | 0.762 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 149,471 | 1.495 | 20 | 24 | fits | 148,089 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 299,390 | 2.994 | 20 | 24 | fits | 150,909 | 192 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 299,324 | 2.993 | 20 | 50 | fits | 150,909 | 192 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 449,300 | 4.493 | 20 | 50 | fits | 150,372 | 186 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 532,318 | 5.323 | 20 | 20 | fits | 83,084 | 41 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 928,005 | 9.280 | 20 | 20 | fits | 50,192 | 20 | 0.703 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 389,392 | 3.894 | 20 | 20 | fits | 150,939 | 186 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 292,492 | 2.925 | 20 | 200 | fits | 152,015 | 197 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 442,815 | 4.428 | 20 | 200 | fits | 150,939 | 186 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 293,416 | 2.934 | 20 | 20 | fits | 152,015 | 197 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 539,602 | 5.396 | 20 | 20 | fits | 85,827 | 48 | 0.760 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 145,041 | 1.450 | 20 | 24 | fits | 148,089 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 296,066 | 2.961 | 20 | 24 | fits | 152,015 | 197 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 296,000 | 2.960 | 20 | 50 | fits | 152,015 | 197 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 446,543 | 4.465 | 20 | 50 | fits | 150,939 | 186 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 542,560 | 5.426 | 20 | 20 | fits | 85,827 | 48 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 923,251 | 9.233 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 433,787 | 4.338 | 20 | 20 | fits | 159,075 | 207 | 0.473 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 309,605 | 3.096 | 20 | 200 | fits | 153,528 | 181 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 478,151 | 4.782 | 20 | 200 | fits | 159,075 | 207 | 0.473 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 310,529 | 3.105 | 20 | 20 | fits | 153,528 | 181 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 562,734 | 5.627 | 20 | 20 | fits | 83,879 | 37 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 160,641 | 1.606 | 20 | 24 | fits | 148,024 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 313,179 | 3.132 | 20 | 24 | fits | 153,528 | 181 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 313,113 | 3.131 | 20 | 50 | fits | 153,528 | 181 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 481,879 | 4.819 | 20 | 50 | fits | 159,075 | 207 | 0.473 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 565,692 | 5.657 | 20 | 20 | fits | 83,879 | 37 | 0.733 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 937,549 | 9.375 | 20 | 20 | fits | 32,958 | 12 | 0.832 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 430,991 | 4.310 | 20 | 20 | fits | 154,086 | 208 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 300,562 | 3.006 | 20 | 200 | fits | 148,915 | 171 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 464,338 | 4.643 | 20 | 200 | fits | 154,086 | 208 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 301,486 | 3.015 | 20 | 20 | fits | 148,915 | 171 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 550,252 | 5.503 | 20 | 20 | fits | 85,210 | 42 | 0.715 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 156,211 | 1.562 | 20 | 24 | fits | 148,024 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 304,136 | 3.041 | 20 | 24 | fits | 148,915 | 171 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 304,070 | 3.041 | 20 | 50 | fits | 148,915 | 171 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 468,066 | 4.681 | 20 | 50 | fits | 154,086 | 208 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 553,210 | 5.532 | 20 | 20 | fits | 85,210 | 42 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 933,802 | 9.338 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| LINK_UP | `adp.link_up.if0` | 3,014 | 0.030 | 20 | 200 | fits | 33,791 | 43 (11) | 0.731 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 20,642 | 0.206 | 20 | 200 | fits | 27,497 | 23 (39) | 0.740 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 9,120 | 0.091 | 20 | 200 | fits | 3,140 | 10 (11) | 0.538 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 22,956 | 0.230 | 20 | 20 | fits | 38,679 | 27 (35) | 0.810 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 14,609 | 0.146 | 20 | 20 | fits | 34,000 | 23 (14) | 0.837 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 24,914 | 0.249 | 20 | 20 | fits | 34,476 | 24 (14) | 0.836 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 30,198 | 0.302 | 20 | 20 | fits | 40,612 | 27 (35) | 0.808 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 79,654 | 0.797 | 20 | 20 | fits | 26,802 | 8 | 0.784 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 44,273 | 0.443 | 20 | 20 | fits | 44,339 | 12 | 0.891 |
| malformed MRPDU discard | `srp.malformed.if0` | 23,118 | 0.231 | 20 | 20 | fits | 23,184 | 12 | 0.714 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 78,560 | 0.786 | 220 | 220 | fits | 42,796 | 6 | 0.905 |
| an event behind 15 others | `backlog.event.if0` | 164,708 | 1.647 | 20 | 200 | fits | 61,402 | 79 | 0.562 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 480,639 | 4.806 | 20 | 20 | fits | 78,969 | 67 | 0.492 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 430,661 | 4.307 | 20 | 200 | fits | 154,817 | 125 | 0.461 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 509,014 | 5.090 | 20 | 200 | fits | 78,969 | 67 | 0.492 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 426,339 | 4.263 | 20 | 20 | fits | 154,817 | 125 | 0.461 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 504,472 | 5.045 | 20 | 20 | fits | 78,969 | 67 | 0.492 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 150,309 | 1.503 | 20 | 24 | fits | 151,200 | 148 | 0.384 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 428,989 | 4.290 | 20 | 24 | fits | 154,817 | 125 | 0.461 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 428,923 | 4.289 | 20 | 50 | fits | 154,817 | 125 | 0.461 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 507,496 | 5.075 | 20 | 50 | fits | 78,969 | 67 | 0.492 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 507,430 | 5.074 | 20 | 20 | fits | 78,969 | 67 | 0.492 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 599,312 | 5.993 | 20 | 20 | fits | 25,089 | 32 | 0.307 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 404,242 | 4.042 | 20 | 20 | fits | 151,361 | 186 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 296,489 | 2.965 | 20 | 200 | fits | 152,548 | 198 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 457,490 | 4.575 | 20 | 200 | fits | 151,361 | 186 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 297,413 | 2.974 | 20 | 20 | fits | 152,548 | 198 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 540,986 | 5.410 | 20 | 20 | fits | 82,792 | 41 | 0.764 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 148,505 | 1.485 | 20 | 24 | fits | 148,691 | 145 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 300,063 | 3.001 | 20 | 24 | fits | 152,548 | 198 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 299,997 | 3.000 | 20 | 50 | fits | 152,548 | 198 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 461,218 | 4.612 | 20 | 50 | fits | 151,361 | 186 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 543,944 | 5.439 | 20 | 20 | fits | 82,792 | 41 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 924,459 | 9.245 | 20 | 20 | fits | 41,669 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 28,012 | 0.280 | 20 | 20 | fits | 34,055 | 19 | 0.806 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 296,489 | 2.965 | 20 | 200 | fits | 152,548 | 198 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 51,372 | 0.514 | 20 | 200 | fits | 34,055 | 19 | 0.806 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 297,413 | 2.974 | 20 | 20 | fits | 152,548 | 198 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 544,040 | 5.440 | 20 | 20 | fits | 89,285 | 39 | 0.755 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 148,505 | 1.485 | 20 | 24 | fits | 148,691 | 145 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 300,063 | 3.001 | 20 | 24 | fits | 152,548 | 198 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 299,997 | 3.000 | 20 | 50 | fits | 152,548 | 198 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 457,779 | 4.578 | 20 | 50 | fits | 147,922 | 186 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 546,998 | 5.470 | 20 | 20 | fits | 89,285 | 39 | 0.755 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 885,823 | 8.858 | 20 | 20 | fits | 85,121 | 36 | 0.566 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,351,268 | 63.513 | 20 | 20 | MISS ceiling | 23,931 | 13 | 0.639 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,379,938 | 63.799 | 20 | 20 | MISS ceiling | 27,295 | 18 | 0.716 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,402,679 | 64.027 | 20 | 20 | MISS ceiling | 25,065 | 13 | 0.600 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,427,343 | 64.273 | 20 | 20 | MISS ceiling | 24,114 | 13 | 0.637 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,451,225 | 64.512 | 20 | 20 | MISS ceiling | 23,755 | 13 | 0.630 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 159,106 | 1.591 | 20 | 200 | fits | 154,925 | 177 | 0.463 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 291,568 | 2.916 | 20 | 200 | fits | 133,078 | 207 | 0.400 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 154,784 | 1.548 | 20 | 20 | fits | 154,925 | 177 | 0.463 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,238,023 | 62.380 | 20 | 20 | MISS ceiling | 38,509 | 15 | 0.767 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 158,424 | 1.584 | 20 | 24 | fits | 154,925 | 177 | 0.463 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,203,000 | 62.030 | 20 | 24 | MISS ceiling | 153,808 | 106 | 0.409 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 157,368 | 1.574 | 20 | 50 | fits | 154,925 | 177 | 0.463 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 290,050 | 2.901 | 20 | 50 | fits | 133,078 | 207 | 0.400 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 371,560 | 3.716 | 20 | 20 | fits | 81,576 | 28 | 0.740 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 707,964 | 7.080 | 20 | 20 | fits | 85,132 | 36 | 0.555 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 7,213 | 0.072 | 20 | 20 | fits | 29,248 | 13 (29) | 0.789 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 10,032 | 0.100 | 20 | 20 | fits | 32,954 | 19 (35) | 0.793 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 22,084 | 0.221 | 20 | 20 | fits | 35,930 | 21 (12) | 0.818 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 14,151 | 0.142 | 20 | 50 | fits | 33,791 | 43 | 0.731 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 16,241 | 0.162 | 20 | 50 | fits | 29,408 | 35 | 0.727 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 23,046 | 0.230 | 20 | 50 | fits | 29,333 | 35 | 0.721 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 15,629 | 0.156 | 20 | 50 | fits | 34,491 | 61 | 0.641 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 17,598 | 0.176 | 20 | 50 | fits | 34,491 | 61 | 0.641 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 11,280 | 0.113 | 20 | 50 | fits | 27,662 | 30 | 0.635 |
| LINK_UP | `adp.link_up.if0` | 3,014 | 0.030 | 20 | 200 | fits | 33,791 | 43 (11) | 0.731 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 20,642 | 0.206 | 20 | 200 | fits | 27,497 | 23 (39) | 0.740 |
| LINK_DOWN | `adp.link_down.if0` | 2,391 | 0.024 | 20 | 200 | fits | 31,407 | 23 (9) | 0.791 |
| LINK_UP | `adp.link_up.if0` | 3,014 | 0.030 | 20 | 200 | fits | 33,791 | 43 (11) | 0.731 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 20,642 | 0.206 | 20 | 200 | fits | 27,497 | 23 (39) | 0.740 |
| GM_CHANGE | `adp.gm_change.if0` | 2,750 | 0.028 | 20 | 200 | fits | 20,707 | 17 (11) | 0.744 |
| LINK_UP | `adp.link_up.if0` | 3,014 | 0.030 | 20 | 200 | fits | 33,791 | 43 (11) | 0.731 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 20,642 | 0.206 | 20 | 200 | fits | 27,497 | 23 (39) | 0.740 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 5,491 | 0.055 | 20 | 200 | fits | 20,810 | 16 (31) | 0.655 |
| LINK_UP | `adp.link_up.if0` | 3,014 | 0.030 | 20 | 200 | fits | 33,791 | 43 (11) | 0.731 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 20,642 | 0.206 | 20 | 200 | fits | 27,497 | 23 (39) | 0.740 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 5,491 | 0.055 | 20 | 200 | fits | 20,810 | 16 (31) | 0.655 |
| set_name | `aecp_fanout.set_name.if0` | 59,388 | 0.594 | 20 | 24 | fits | 59,921 | 89 | 0.575 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 58,007 | 0.580 | 20 | 24 | fits | 55,984 | 78 | 0.596 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 52,092 | 0.521 | 20 | 24 | fits | 50,943 | 79 | 0.543 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 43,885 | 0.439 | 20 | 24 | fits | 51,092 | 78 | 0.551 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 53,701 | 0.537 | 20 | 24 | fits | 54,997 | 67 | 0.579 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 51,206 | 0.512 | 20 | 24 | fits | 50,312 | 78 | 0.539 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 55,372 | 0.554 | 20 | 24 | fits | 49,903 | 79 | 0.540 |
| BIND_RX | `acmp.bind_rx.if0` | 20,737 | 0.207 | 20 | 20 | fits | 46,812 | 26 (77) | 0.796 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 10,848 | 0.108 | 20 | 20 | fits | 35,038 | 19 (32) | 0.830 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 11,076 | 0.111 | 20 | 20 | fits | 30,520 | 16 (47) | 0.777 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 16,080 | 0.161 | 20 | 20 | fits | 42,913 | 18 (50) | 0.840 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 11,254 | 0.113 | 20 | 20 | fits | 30,723 | 17 (48) | 0.763 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 10,044 | 0.100 | 20 | 20 | fits | 29,295 | 16 (48) | 0.735 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 10,716 | 0.107 | 20 | 20 | fits | 30,215 | 16 (48) | 0.771 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,905 | 0.099 | 20 | 20 | fits | 28,850 | 16 (48) | 0.735 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 21,361 | 0.214 | 20 | 24 | fits | 30,526 | 20 | 0.777 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 31,459 | 0.315 | 20 | 24 | fits | 34,315 | 20 | 0.697 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 24,121 | 0.241 | 20 | 24 | fits | 30,899 | 20 | 0.727 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 23,642 | 0.236 | 20 | 24 | fits | 30,307 | 20 | 0.714 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 27,564 | 0.276 | 20 | 24 | fits | 30,369 | 20 | 0.714 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 24,487 | 0.245 | 20 | 24 | fits | 31,515 | 20 | 0.721 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 27,241 | 0.272 | 20 | 24 | fits | 30,059 | 20 | 0.719 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 26,418 | 0.264 | 20 | 24 | fits | 30,164 | 20 | 0.734 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 23,735 | 0.237 | 20 | 24 | fits | 30,448 | 20 | 0.741 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 32,166 | 0.322 | 20 | 24 | fits | 35,111 | 21 | 0.645 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 23,145 | 0.231 | 20 | 24 | fits | 29,858 | 20 | 0.759 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 27,312 | 0.273 | 20 | 24 | fits | 29,997 | 20 | 0.762 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 26,342 | 0.263 | 20 | 24 | fits | 30,241 | 20 | 0.725 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 23,968 | 0.240 | 20 | 24 | fits | 30,825 | 20 | 0.727 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 27,628 | 0.276 | 20 | 24 | fits | 30,611 | 20 | 0.731 |
| get_configuration | `aecp.get_configuration.if0` | 21,312 | 0.213 | 20 | 24 | fits | 27,350 | 20 | 0.724 |
| entity_available | `aecp.entity_available.if0` | 25,372 | 0.254 | 20 | 24 | fits | 27,581 | 20 | 0.725 |
| get_name | `aecp.get_name.if0` | 27,673 | 0.277 | 20 | 24 | fits | 30,712 | 20 | 0.751 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 24,660 | 0.247 | 20 | 24 | fits | 31,408 | 27 | 0.721 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 19,730 | 0.197 | 20 | 24 | fits | 33,007 | 29 | 0.777 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 21,542 | 0.215 | 20 | 24 | fits | 28,375 | 20 | 0.757 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 25,101 | 0.251 | 20 | 24 | fits | 27,234 | 20 | 0.725 |
| set_name | `aecp.set_name.if0` | 34,725 | 0.347 | 20 | 24 | fits | 47,330 | 43 | 0.760 |
| lock_entity | `aecp.lock_entity.if0` | 27,594 | 0.276 | 20 | 24 | fits | 38,691 | 34 | 0.775 |
| unlock_entity | `aecp.unlock_entity.if0` | 32,933 | 0.329 | 20 | 24 | fits | 38,703 | 33 | 0.780 |
| LINK_UP | `fixture.link_up.if0` | 3,014 | 0.030 | 20 | 200 | fits | 33,791 | 43 (11) | 0.731 |
| malformed MRPDU discard | `fixture.malformed.if0` | 23,579 | 0.236 | 20 | 20 | fits | 23,645 | 12 | 0.745 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 34,415 | 0.344 | 20 | 24 | fits | 49,473 | 43 | 0.781 |
| LINK_DOWN | `fixture.link_down.if0` | 2,875 | 0.029 | 20 | 200 | fits | 32,479 | 23 (9) | 0.798 |
| BIND_RX | `fixture.bind_rx.if0` | 21,240 | 0.212 | 20 | 20 | fits | 47,222 | 26 (77) | 0.807 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 18,888 | 0.189 | 20 | 20 | fits | 44,629 | 29 (35) | 0.784 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 9,522 | 0.095 | 20 | 20 | fits | 30,503 | 13 (29) | 0.809 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 84,674 | 0.847 | 20 | 200 | fits | 84,778 | 51 | 0.756 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 84,674 | 0.847 | 20 | 200 | fits | 84,778 | 51 | 0.756 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 84,400 | 0.844 | 20 | 20 | fits | 84,778 | 51 | 0.756 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 84,400 | 0.844 | 20 | 20 | fits | 84,778 | 51 | 0.756 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 84,608 | 0.846 | 20 | 24 | fits | 84,778 | 51 | 0.756 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 84,608 | 0.846 | 20 | 24 | fits | 84,778 | 51 | 0.756 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 84,542 | 0.845 | 20 | 50 | fits | 84,778 | 51 | 0.756 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 84,542 | 0.845 | 20 | 50 | fits | 84,778 | 51 | 0.756 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 84,476 | 0.845 | 20 | 20 | fits | 84,778 | 51 | 0.756 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 84,476 | 0.845 | 20 | 20 | fits | 84,778 | 51 | 0.756 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
