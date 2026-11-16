### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 85 paths and 7 of 963 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.222 (0.481) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.115 (0.305) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.098 (0.326) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.219 (0.633) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.124 (0.309) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.111 (0.291) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.105 (0.297) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.123 (0.310) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.113 (0.356) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.162 (0.596) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.195 (0.624) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.280 (0.722) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.214 (0.649) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.183 (0.684) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.245 (0.672) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.169 (0.462) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.058 (0.218) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.030 (0.208) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.033 (0.385) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.034 (0.331) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.045 (0.239) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.143 (0.525) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.137 (0.513) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.186 (0.569) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.125 (0.502) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.112 (0.313) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.146 (0.530) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.136 (0.376) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.130 (0.508) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.186 (0.569) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.146 (0.528) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.142 (0.522) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.103 (0.301) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.214 (0.595) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.140 (0.523) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.151 (0.534) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.097 (0.294) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.141 (0.523) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.107 (0.307) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.170 (0.553) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.169 (0.551) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.155 (0.537) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.152 (0.533) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.270 (0.654) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.266 (0.762) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.129 (0.510) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.175 (0.594) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.564 (0.882) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.458 (0.801) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.565 (0.893) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.493 (0.656) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.399 (0.754) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.409 (0.724) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 5.029 (5.490) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-1.adp_available.if0` (backlog-adp@verify-1) | 4.751 (6.502) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.218 (0.648) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.703 (2.144) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.415 (63.770) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.391 (64.759) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.393 (0.545) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-burst.held.acmp.if0` (save-burst) | 3.147 | fits | 11 acmp | 4 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-burst.held.adp.if0` (save-burst) | 2.940 | fits | 7 adp | 4 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 3.160 | fits | 15 aecp | 4 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 2.496 | fits | 6 maap | 4 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 9.600 | fits | 31 srp | 4 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.278 (0.677) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.127 (0.280) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.140 (0.331) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.257 (0.677) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.257 (0.637) | fits | 0 events | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-held.mrpdu.periodic.if0` (save-held) | 3.846 | fits | 0 srp | 12 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.627 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.198 | MISS ceiling | 11 acmp | 77 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.670 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-1.service.adp.last.if0` (backlog-adp@verify-1) | 5.516 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-1.service.aecp.first.if0` (backlog-adp@verify-1) | 2.433 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.843 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.653 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-1.service.maap.last.if0` (backlog-adp@verify-1) | 5.553 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-4.service.srp.first.if0` (backlog-adp@program-4) | 6.564 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-4.service.srp.last.if0` (backlog-adp@blank-aged2-4) | 11.124 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 1.736 (1.887) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.542 (0.543) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.261 (0.261) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 1.502 (1.579) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 15.305 | 12 | 155,144 (1.551) | yes | - |
| backlog-adp@blank-1 | 0 | 15.180 | 12 | 155,144 (1.551) | yes | - |
| backlog-adp@blank-2 | 0 | 15.070 | 12 | 157,528 (1.575) | yes | - |
| backlog-adp@blank-3 | 0 | 14.945 | 12 | 157,528 (1.575) | yes | - |
| backlog-adp@blank-4 | 0 | 14.820 | 12 | 157,528 (1.575) | yes | - |
| backlog-adp@blank-5 | 0 | 14.695 | 12 | 157,528 (1.575) | yes | - |
| backlog-adp@blank-6 | 0 | 14.570 | 12 | 157,528 (1.575) | yes | - |
| backlog-adp@blank-7 | 0 | 14.445 | 12 | 157,528 (1.575) | yes | - |
| backlog-adp@program-0 | 0 | 12.100 | 10 | 154,049 (1.540) | yes | - |
| backlog-adp@program-1 | 0 | 11.850 | 10 | 154,049 (1.540) | yes | - |
| backlog-adp@program-2 | 0 | 11.600 | 10 | 154,049 (1.540) | yes | - |
| backlog-adp@program-3 | 0 | 12.343 | 10 | 155,341 (1.553) | yes | - |
| backlog-adp@program-4 | 0 | 12.382 | 10 | 157,245 (1.572) | yes | - |
| backlog-adp@program-5 | 0 | 12.132 | 10 | 157,245 (1.572) | yes | - |
| backlog-adp@program-6 | 0 | 11.882 | 10 | 157,245 (1.572) | yes | - |
| backlog-adp@program-7 | 0 | 11.632 | 10 | 157,245 (1.572) | yes | - |
| backlog-adp@verify-0 | 0 | 13.056 | 11 | 156,123 (1.561) | yes | - |
| backlog-adp@verify-1 | 0 | 13.881 | 11 | 156,226 (1.562) | yes | - |
| backlog-adp@verify-2 | 0 | 13.756 | 11 | 156,226 (1.562) | yes | - |
| backlog-adp@verify-3 | 0 | 13.631 | 11 | 156,226 (1.562) | yes | - |
| backlog-adp@verify-4 | 0 | 13.506 | 11 | 156,226 (1.562) | yes | - |
| backlog-adp@verify-5 | 0 | 13.381 | 11 | 156,226 (1.562) | yes | - |
| backlog-adp@verify-6 | 1 | 12.954 | 10 | 156,120 (1.561) | yes | - |
| backlog-adp@verify-7 | 1 | 12.954 | 10 | 156,120 (1.561) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 12.782 | 10 | 155,305 (1.553) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 13.613 | 10 | 155,346 (1.553) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 15.879 | 12 | 155,792 (1.558) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 13.953 | 12 | 154,298 (1.543) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 13.994 | 11 | 148,947 (1.489) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 13.792 | 11 | 154,919 (1.549) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 14.916 | 11 | 156,538 (1.565) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 13.881 | 11 | 153,429 (1.534) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 13.172 | 12 | 156,210 (1.562) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 12.838 | 9 | 156,914 (1.569) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 12.886 | 10 | 155,638 (1.556) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 12.794 | 9 | 155,724 (1.557) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 12.868 | 10 | 155,271 (1.553) | yes | - |
| backlog-adp@blank-aged1-5 | 1 | 16.163 | 12 | 151,085 (1.511) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 15.158 | 12 | 154,134 (1.541) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 13.987 | 10 | 150,881 (1.509) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 12.293 | 11 | 154,924 (1.549) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 12.292 | 10 | 155,165 (1.552) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 12.406 | 10 | 155,532 (1.555) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 12.308 | 10 | 155,652 (1.557) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 12.251 | 9 | 155,012 (1.550) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 13.684 | 12 | 155,470 (1.555) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 13.851 | 11 | 156,312 (1.563) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 12.550 | 11 | 155,939 (1.559) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 12.953 | 13 | 154,345 (1.543) | yes | - |
| backlog-adp@program-aged1-1 | 1 | 12.328 | 10 | 156,045 (1.560) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 12.424 | 11 | 155,710 (1.557) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 12.196 | 9 | 156,579 (1.566) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 12.276 | 10 | 154,019 (1.540) | yes | - |
| backlog-adp@program-aged1-5 | 1 | 12.223 | 9 | 148,249 (1.482) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 14.374 | 13 | 155,734 (1.557) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 12.870 | 12 | 155,123 (1.551) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 12.821 | 10 | 155,731 (1.557) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 15.884 | 12 | 154,035 (1.540) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 14.827 | 11 | 151,353 (1.514) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 13.794 | 11 | 156,700 (1.567) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 13.773 | 10 | 155,652 (1.557) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 13.673 | 10 | 153,956 (1.540) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 17.066 | 12 | 156,453 (1.565) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 16.181 | 13 | 154,852 (1.549) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 13.113 | 11 | 155,656 (1.557) | yes | - |
| backlog-adp@verify-aged1-1 | 1 | 12.829 | 9 | 155,778 (1.558) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 15.165 | 12 | 155,289 (1.553) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 14.127 | 12 | 155,532 (1.555) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 13.234 | 12 | 155,845 (1.558) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 13.033 | 11 | 154,979 (1.550) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 15.093 | 11 | 156,649 (1.566) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 14.061 | 11 | 152,577 (1.526) | yes | - |
| backlog | 0 | 6.798 | 7 | 158,330 (1.583) | yes | - |
| backlog-adp | 0 | 11.452 | 12 | 153,891 (1.539) | yes | - |
| backlog-adp-refill | 0 | 41.046 | 25 | 153,891 (1.539) | yes | - |
| backlog-owed | 0 | 65.199 | 25 | 156,011 (1.560) | yes | - |
| fixture | 0 | 1.553 | 2 | 95,306 (0.953) | yes | - |

Composed maximum over the 4 backlog windows: 158,330 CPU cycles (1.583 ms), backlog.
Over the windows that released their whole load only: 158,330 (1.583 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 124682 | 0 | 105,726 (1.057) | fits |
| save-burst | 3318 | 0 | 165,215 (1.652) | fits |
| save-held | 3363 | 0 | 165,215 (1.652) | fits |
| save-starved | 58512 | 0 | 165,215 (1.652) | fits |
| save-flight | 2945 | 0 | 165,215 (1.652) | fits |
| acmp-notk | 3357 | 0 | 109,841 (1.098) | fits |
| backlog-adp@blank-0 | 489 | 0 | 155,144 (1.551) | fits |
| backlog-adp@blank-1 | 489 | 0 | 155,144 (1.551) | fits |
| backlog-adp@blank-2 | 489 | 0 | 157,528 (1.575) | fits |
| backlog-adp@blank-3 | 489 | 0 | 157,528 (1.575) | fits |
| backlog-adp@blank-4 | 489 | 0 | 157,528 (1.575) | fits |
| backlog-adp@blank-5 | 489 | 0 | 157,528 (1.575) | fits |
| backlog-adp@blank-6 | 489 | 0 | 157,528 (1.575) | fits |
| backlog-adp@blank-7 | 489 | 0 | 157,528 (1.575) | fits |
| backlog-adp@program-0 | 526 | 0 | 154,049 (1.540) | fits |
| backlog-adp@program-1 | 526 | 0 | 154,049 (1.540) | fits |
| backlog-adp@program-2 | 526 | 0 | 154,049 (1.540) | fits |
| backlog-adp@program-3 | 526 | 0 | 155,341 (1.553) | fits |
| backlog-adp@program-4 | 526 | 0 | 157,245 (1.572) | fits |
| backlog-adp@program-5 | 526 | 0 | 157,245 (1.572) | fits |
| backlog-adp@program-6 | 526 | 0 | 157,245 (1.572) | fits |
| backlog-adp@program-7 | 526 | 0 | 157,245 (1.572) | fits |
| backlog-adp@verify-0 | 550 | 0 | 156,123 (1.561) | fits |
| backlog-adp@verify-1 | 550 | 0 | 156,226 (1.562) | fits |
| backlog-adp@verify-2 | 550 | 0 | 156,226 (1.562) | fits |
| backlog-adp@verify-3 | 550 | 0 | 156,226 (1.562) | fits |
| backlog-adp@verify-4 | 550 | 0 | 156,226 (1.562) | fits |
| backlog-adp@verify-5 | 550 | 0 | 156,226 (1.562) | fits |
| backlog-adp@verify-6 | 550 | 0 | 156,120 (1.561) | fits |
| backlog-adp@verify-7 | 550 | 0 | 156,120 (1.561) | fits |
| backlog-adp@blank-aged2-0 | 717 | 0 | 155,305 (1.553) | fits |
| backlog-adp@blank-aged2-1 | 723 | 0 | 155,346 (1.553) | fits |
| backlog-adp@blank-aged2-2 | 732 | 0 | 155,792 (1.558) | fits |
| backlog-adp@blank-aged2-3 | 738 | 0 | 154,298 (1.543) | fits |
| backlog-adp@blank-aged2-4 | 744 | 0 | 148,947 (1.489) | fits |
| backlog-adp@blank-aged2-5 | 750 | 0 | 154,919 (1.549) | fits |
| backlog-adp@blank-aged2-6 | 757 | 0 | 156,538 (1.565) | fits |
| backlog-adp@blank-aged2-7 | 763 | 0 | 153,429 (1.534) | fits |
| backlog-adp@blank-aged1-0 | 667 | 0 | 156,210 (1.562) | fits |
| backlog-adp@blank-aged1-1 | 671 | 0 | 156,914 (1.569) | fits |
| backlog-adp@blank-aged1-2 | 678 | 0 | 155,638 (1.556) | fits |
| backlog-adp@blank-aged1-3 | 684 | 0 | 155,724 (1.557) | fits |
| backlog-adp@blank-aged1-4 | 691 | 0 | 155,271 (1.553) | fits |
| backlog-adp@blank-aged1-5 | 700 | 0 | 151,085 (1.511) | fits |
| backlog-adp@blank-aged1-6 | 706 | 0 | 154,134 (1.541) | fits |
| backlog-adp@blank-aged1-7 | 711 | 0 | 150,881 (1.509) | fits |
| backlog-adp@program-aged2-0 | 767 | 0 | 154,924 (1.549) | fits |
| backlog-adp@program-aged2-1 | 772 | 0 | 155,165 (1.552) | fits |
| backlog-adp@program-aged2-2 | 779 | 0 | 155,532 (1.555) | fits |
| backlog-adp@program-aged2-3 | 785 | 0 | 155,652 (1.557) | fits |
| backlog-adp@program-aged2-4 | 791 | 0 | 155,012 (1.550) | fits |
| backlog-adp@program-aged2-5 | 800 | 0 | 155,470 (1.555) | fits |
| backlog-adp@program-aged2-6 | 806 | 0 | 156,312 (1.563) | fits |
| backlog-adp@program-aged2-7 | 812 | 0 | 155,939 (1.559) | fits |
| backlog-adp@program-aged1-0 | 717 | 0 | 154,345 (1.543) | fits |
| backlog-adp@program-aged1-1 | 721 | 0 | 156,045 (1.560) | fits |
| backlog-adp@program-aged1-2 | 728 | 0 | 155,710 (1.557) | fits |
| backlog-adp@program-aged1-3 | 733 | 0 | 156,579 (1.566) | fits |
| backlog-adp@program-aged1-4 | 740 | 0 | 154,019 (1.540) | fits |
| backlog-adp@program-aged1-5 | 746 | 0 | 149,291 (1.493) | fits |
| backlog-adp@program-aged1-6 | 756 | 0 | 155,734 (1.557) | fits |
| backlog-adp@program-aged1-7 | 761 | 0 | 155,123 (1.551) | fits |
| backlog-adp@verify-aged2-0 | 784 | 0 | 155,731 (1.557) | fits |
| backlog-adp@verify-aged2-1 | 792 | 0 | 154,035 (1.540) | fits |
| backlog-adp@verify-aged2-2 | 798 | 0 | 151,353 (1.514) | fits |
| backlog-adp@verify-aged2-3 | 804 | 0 | 156,700 (1.567) | fits |
| backlog-adp@verify-aged2-4 | 810 | 0 | 155,652 (1.557) | fits |
| backlog-adp@verify-aged2-5 | 816 | 0 | 153,956 (1.540) | fits |
| backlog-adp@verify-aged2-6 | 825 | 0 | 156,453 (1.565) | fits |
| backlog-adp@verify-aged2-7 | 832 | 0 | 154,852 (1.549) | fits |
| backlog-adp@verify-aged1-0 | 733 | 0 | 155,656 (1.557) | fits |
| backlog-adp@verify-aged1-1 | 738 | 0 | 155,778 (1.558) | fits |
| backlog-adp@verify-aged1-2 | 747 | 0 | 155,289 (1.553) | fits |
| backlog-adp@verify-aged1-3 | 753 | 0 | 155,532 (1.555) | fits |
| backlog-adp@verify-aged1-4 | 760 | 0 | 155,845 (1.558) | fits |
| backlog-adp@verify-aged1-5 | 765 | 0 | 154,979 (1.550) | fits |
| backlog-adp@verify-aged1-6 | 772 | 0 | 156,649 (1.566) | fits |
| backlog-adp@verify-aged1-7 | 778 | 0 | 152,577 (1.526) | fits |
| adp-advertise | 598 | 0 | 95,880 (0.959) | fits |
| acmp-noresp | 1886 | 0 | 105,141 (1.051) | fits |
| save | 609 | 0 | 95,880 (0.959) | fits |
| srp | 290 | 0 | 140,524 (1.405) | fits |
| backlog | 286 | 0 | 158,330 (1.583) | fits |
| backlog-adp | 316 | 0 | 153,891 (1.539) | fits |
| backlog-adp-refill | 329 | 0 | 153,891 (1.539) | fits |
| backlog-owed | 310 | 0 | 156,011 (1.560) | fits |
| acmp-disc | 877 | 0 | 109,678 (1.097) | fits |
| maap | 179 | 0 | 95,880 (0.959) | fits |
| adp-link | 89 | 0 | 95,880 (0.959) | fits |
| adp-gm | 88 | 0 | 95,880 (0.959) | fits |
| adp-discover | 88 | 0 | 95,880 (0.959) | fits |
| control | 88 | 0 | 95,880 (0.959) | fits |
| aecp-fanout | 109 | 0 | 95,880 (0.959) | fits |
| acmp-cmd | 87 | 0 | 95,880 (0.959) | fits |
| aecp | 113 | 0 | 95,880 (0.959) | fits |
| datapath-events | 116 | 0 | 95,880 (0.959) | fits |
| fixture | 161 | 0 | 95,880 (0.959) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | +10.111 ms, 76,400 (0.764 ms), read-back | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 10.073 (20) | 9.927 |
| backlog-adp@blank-aged2-1 | 2 | +9.213 ms, 76,401 (0.764 ms), read-back | none | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 10.746 (20) | 9.254 |
| backlog-adp@blank-aged2-2 | 2 | +8.409 ms, 76,401 (0.764 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 10.848 (20) | 9.152 |
| backlog-adp@blank-aged2-3 | 2 | +6.494 ms, 76,460 (0.765 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 10.747 (20) | 9.253 |
| backlog-adp@blank-aged2-4 | 2 | +5.323 ms, 76,700 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 11.124 (20) | 8.876 |
| backlog-adp@blank-aged2-5 | 2 | +4.679 ms, 76,178 (0.762 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 10.918 (20) | 9.082 |
| backlog-adp@blank-aged2-6 | 2 | +4.750 ms, 76,088 (0.761 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 10.877 (20) | 9.123 |
| backlog-adp@blank-aged2-7 | 2 | +3.073 ms, 76,411 (0.764 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 10.784 (20) | 9.216 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 9.912 (20) | 10.088 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 9.966 (20) | 10.034 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 10.014 (20) | 9.986 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 9.922 (20) | 10.078 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 9.994 (20) | 10.006 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 9.951 (20) | 10.049 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 10.170 (20) | 9.830 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 9.945 (20) | 10.055 |
| backlog-adp@program-aged2-0 | 2 | none | +10.245 ms, 80,665 (0.807 ms), issue | `backlog-adp@program-aged2-0.service.srp.last.if0` | 9.806 (20) | 10.194 |
| backlog-adp@program-aged2-1 | 2 | +9.208 ms, 80,847 (0.808 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 10.785 (20) | 9.215 |
| backlog-adp@program-aged2-2 | 2 | +8.416 ms, 80,847 (0.808 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 10.900 (20) | 9.100 |
| backlog-adp@program-aged2-3 | 2 | +6.499 ms, 80,972 (0.810 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 10.801 (20) | 9.199 |
| backlog-adp@program-aged2-4 | 2 | +5.423 ms, 81,219 (0.812 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 10.743 (20) | 9.257 |
| backlog-adp@program-aged2-5 | 2 | +4.711 ms, 80,779 (0.808 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 10.831 (20) | 9.169 |
| backlog-adp@program-aged2-6 | 2 | +4.602 ms, 80,620 (0.806 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 10.884 (20) | 9.116 |
| backlog-adp@program-aged2-7 | 2 | +3.086 ms, 80,811 (0.808 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 10.810 (20) | 9.190 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 9.937 (20) | 10.063 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 9.921 (20) | 10.079 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 10.159 (20) | 9.841 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 9.931 (20) | 10.069 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 10.010 (20) | 9.990 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 9.950 (20) | 10.050 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 10.058 (20) | 9.942 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 9.960 (20) | 10.040 |
| backlog-adp@verify-aged2-0 | 2 | none | +10.116 ms, 77,390 (0.774 ms), read-back | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 10.079 (20) | 9.921 |
| backlog-adp@verify-aged2-1 | 2 | +9.208 ms, 77,391 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 10.751 (20) | 9.249 |
| backlog-adp@verify-aged2-2 | 2 | +8.141 ms, 77,385 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 10.696 (20) | 9.304 |
| backlog-adp@verify-aged2-3 | 2 | +6.472 ms, 77,385 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 10.897 (20) | 9.103 |
| backlog-adp@verify-aged2-4 | 2 | +5.651 ms, 77,504 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 10.876 (20) | 9.124 |
| backlog-adp@verify-aged2-5 | 2 | +5.543 ms, 77,504 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 10.778 (20) | 9.222 |
| backlog-adp@verify-aged2-6 | 2 | +4.505 ms, 77,018 (0.770 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 10.755 (20) | 9.245 |
| backlog-adp@verify-aged2-7 | 2 | +3.119 ms, 77,276 (0.773 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 10.813 (20) | 9.187 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 9.982 (20) | 10.018 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 9.924 (20) | 10.076 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 10.021 (20) | 9.979 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 9.929 (20) | 10.071 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 9.988 (20) | 10.012 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 9.982 (20) | 10.018 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 10.055 (20) | 9.945 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 9.978 (20) | 10.022 |

Least margin over the aged windows: 8.876 ms, `backlog-adp@blank-aged2-4.service.srp.last.if0` at 11.124 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 22829.744 | 22,870 | 382 | 2 | 32.227 | yes | within |
| save-held | 1353.265 | 12,470 | 382 | - | 34.228 | no | within |
| save-starved | 12447.122 | 12,470 | 382 | - | 33.594 | yes | within |
| save | 1302.026 | 12,470 | 382 | - | 102.161 | no | within |

Names from their response to durable (save_burst.py; #920, the ruling of #665 issuecomment-6899740728, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-burst | 107 | 1367.528 (0) | 5,000 | 6 | - | - | sequence 6, 0 missing | within |
| save-flight | 1 | 657.720 (0) | 5,000 | 2 | - | - | 59 steps (want 59), 27.287 ms | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1080 | 81,917 (0.819) | 78,192 (0.782) |
| save-burst | 3721 | 103,782 (1.038) | 78,309 (0.783) |
| save-held | 1909 | 98,801 (0.988) | 78,068 (0.781) |
| save-starved | 698 | 82,916 (0.829) | 78,550 (0.785) |
| save-flight | 2063 | 99,469 (0.995) | 78,097 (0.781) |
| acmp-notk | 1415 | 109,841 (1.098) | 78,029 (0.780) |
| backlog-adp@blank-0 | 383 | 95,683 (0.957) | 75,989 (0.760) |
| backlog-adp@blank-1 | 383 | 95,683 (0.957) | 75,989 (0.760) |
| backlog-adp@blank-2 | 383 | 95,683 (0.957) | 75,989 (0.760) |
| backlog-adp@blank-3 | 383 | 95,683 (0.957) | 75,989 (0.760) |
| backlog-adp@blank-4 | 383 | 95,683 (0.957) | 75,989 (0.760) |
| backlog-adp@blank-5 | 383 | 95,683 (0.957) | 75,989 (0.760) |
| backlog-adp@blank-6 | 383 | 95,683 (0.957) | 75,989 (0.760) |
| backlog-adp@blank-7 | 383 | 95,683 (0.957) | 75,989 (0.760) |
| backlog-adp@program-0 | 491 | 104,360 (1.044) | 78,056 (0.781) |
| backlog-adp@program-1 | 491 | 104,360 (1.044) | 78,056 (0.781) |
| backlog-adp@program-2 | 491 | 104,360 (1.044) | 78,056 (0.781) |
| backlog-adp@program-3 | 492 | 104,360 (1.044) | 78,735 (0.787) |
| backlog-adp@program-4 | 493 | 104,360 (1.044) | 78,056 (0.781) |
| backlog-adp@program-5 | 493 | 104,360 (1.044) | 78,056 (0.781) |
| backlog-adp@program-6 | 493 | 104,360 (1.044) | 78,056 (0.781) |
| backlog-adp@program-7 | 493 | 104,360 (1.044) | 78,056 (0.781) |
| backlog-adp@verify-0 | 597 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-1 | 598 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-2 | 598 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-3 | 598 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-4 | 598 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-5 | 598 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-6 | 598 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-7 | 598 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@blank-aged2-0 | 379 | 96,571 (0.966) | 75,455 (0.755) |
| backlog-adp@blank-aged2-1 | 380 | 94,917 (0.949) | 75,464 (0.755) |
| backlog-adp@blank-aged2-2 | 382 | 101,507 (1.015) | 75,455 (0.755) |
| backlog-adp@blank-aged2-3 | 380 | 94,024 (0.940) | 75,494 (0.755) |
| backlog-adp@blank-aged2-4 | 380 | 95,208 (0.952) | 75,716 (0.757) |
| backlog-adp@blank-aged2-5 | 380 | 95,570 (0.956) | 75,998 (0.760) |
| backlog-adp@blank-aged2-6 | 381 | 95,225 (0.952) | 75,962 (0.760) |
| backlog-adp@blank-aged2-7 | 380 | 94,230 (0.942) | 75,852 (0.759) |
| backlog-adp@blank-aged1-0 | 379 | 94,222 (0.942) | 75,853 (0.759) |
| backlog-adp@blank-aged1-1 | 379 | 95,342 (0.953) | 75,954 (0.760) |
| backlog-adp@blank-aged1-2 | 379 | 95,341 (0.953) | 75,954 (0.760) |
| backlog-adp@blank-aged1-3 | 379 | 95,341 (0.953) | 75,954 (0.760) |
| backlog-adp@blank-aged1-4 | 379 | 95,601 (0.956) | 76,022 (0.760) |
| backlog-adp@blank-aged1-5 | 382 | 103,462 (1.035) | 76,203 (0.762) |
| backlog-adp@blank-aged1-6 | 381 | 95,622 (0.956) | 75,990 (0.760) |
| backlog-adp@blank-aged1-7 | 380 | 95,307 (0.953) | 75,956 (0.760) |
| backlog-adp@program-aged2-0 | 488 | 104,360 (1.044) | 78,238 (0.782) |
| backlog-adp@program-aged2-1 | 489 | 104,360 (1.044) | 78,288 (0.783) |
| backlog-adp@program-aged2-2 | 489 | 104,360 (1.044) | 78,288 (0.783) |
| backlog-adp@program-aged2-3 | 489 | 104,360 (1.044) | 78,322 (0.783) |
| backlog-adp@program-aged2-4 | 489 | 104,360 (1.044) | 78,443 (0.784) |
| backlog-adp@program-aged2-5 | 490 | 104,360 (1.044) | 78,305 (0.783) |
| backlog-adp@program-aged2-6 | 491 | 104,360 (1.044) | 78,284 (0.783) |
| backlog-adp@program-aged2-7 | 489 | 104,360 (1.044) | 78,314 (0.783) |
| backlog-adp@program-aged1-0 | 489 | 106,387 (1.064) | 78,782 (0.788) |
| backlog-adp@program-aged1-1 | 488 | 104,360 (1.044) | 78,642 (0.786) |
| backlog-adp@program-aged1-2 | 488 | 104,360 (1.044) | 78,667 (0.787) |
| backlog-adp@program-aged1-3 | 488 | 104,360 (1.044) | 78,667 (0.787) |
| backlog-adp@program-aged1-4 | 488 | 104,360 (1.044) | 78,667 (0.787) |
| backlog-adp@program-aged1-5 | 488 | 104,360 (1.044) | 78,737 (0.787) |
| backlog-adp@program-aged1-6 | 491 | 104,360 (1.044) | 78,737 (0.787) |
| backlog-adp@program-aged1-7 | 489 | 104,360 (1.044) | 78,737 (0.787) |
| backlog-adp@verify-aged2-0 | 597 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-aged2-1 | 600 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-aged2-2 | 599 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-aged2-3 | 598 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-aged2-4 | 598 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-aged2-5 | 598 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-aged2-6 | 601 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-aged2-7 | 600 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-aged1-0 | 597 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-aged1-1 | 597 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-aged1-2 | 599 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-aged1-3 | 598 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-aged1-4 | 597 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-aged1-5 | 597 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-aged1-6 | 599 | 105,091 (1.051) | 78,056 (0.781) |
| backlog-adp@verify-aged1-7 | 598 | 105,091 (1.051) | 78,056 (0.781) |
| adp-advertise | 577 | 29,004 (0.290) | 2,550 (0.025) |
| acmp-noresp | 965 | 106,816 (1.068) | 78,040 (0.780) |
| save | 937 | 97,969 (0.980) | 77,737 (0.777) |
| srp | 271 | 29,004 (0.290) | 2,550 (0.025) |
| backlog | 265 | 29,004 (0.290) | 2,550 (0.025) |
| backlog-adp | 271 | 29,004 (0.290) | 2,550 (0.025) |
| backlog-adp-refill | 274 | 29,004 (0.290) | 2,550 (0.025) |
| backlog-owed | 277 | 29,004 (0.290) | 2,550 (0.025) |
| acmp-disc | 656 | 109,678 (1.097) | 78,029 (0.780) |
| maap | 166 | 29,004 (0.290) | 2,550 (0.025) |
| adp-link | 79 | 29,004 (0.290) | 2,550 (0.025) |
| adp-gm | 79 | 29,004 (0.290) | 2,550 (0.025) |
| adp-discover | 79 | 29,004 (0.290) | 2,550 (0.025) |
| control | 79 | 29,004 (0.290) | 2,550 (0.025) |
| aecp-fanout | 79 | 29,004 (0.290) | 2,550 (0.025) |
| acmp-cmd | 66 | 29,004 (0.290) | 2,550 (0.025) |
| aecp | 80 | 29,004 (0.290) | 2,550 (0.025) |
| datapath-events | 70 | 29,004 (0.290) | 2,550 (0.025) |
| fixture | 55 | 20,121 (0.201) | 2,523 (0.025) |

Longest pass that carries a step: 109,841 CPU cycles (1.098 ms), acmp-notk; longest step: 78,782 (0.788 ms), backlog-adp@program-aged1-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-burst.held.adp.if0` | 293,990 | 2.940 | 20 | 200 | fits | 129,584 | 142 | 0.503 |
| ACMP record, every channel at its refill rate, the longest | `save-burst.held.acmp.if0` | 314,652 | 3.147 | 20 | 20 | fits | 72,440 | 51 | 0.479 |
| AECP record, every channel at its refill rate, the longest | `save-burst.held.aecp.if0` | 128,640 | 1.286 | 20 | 24 | fits | 36,748 | 23 | 0.785 |
| MAAP record, every channel at its refill rate, the longest | `save-burst.held.maap.if0` | 202,737 | 2.027 | 20 | 50 | fits | 153,724 | 216 | 0.392 |
| SRP record, every channel at its refill rate, the longest | `save-burst.held.srp.if0` | 929,404 | 9.294 | 20 | 20 | fits | 50,790 | 23 | 0.808 |
| an MRPDU its join timer owes, the longest | `save-burst.mrpdu.join.if0` | 116,762 | 1.168 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-burst.mrpdu.leaveall.if0` | 180,168 | 1.802 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-burst.mrpdu.periodic.if0` | 310,838 | 3.108 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 281,977 | 2.820 | 20 | 200 | fits | 117,702 | 133 | 0.442 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 285,121 | 2.851 | 20 | 20 | fits | 72,322 | 51 | 0.483 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 291,478 | 2.915 | 20 | 24 | fits | 67,863 | 50 | 0.518 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 239,219 | 2.392 | 20 | 50 | fits | 99,863 | 77 | 0.550 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 935,861 | 9.359 | 20 | 20 | fits | 57,912 | 20 | 0.654 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 115,618 | 1.156 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 187,645 | 1.876 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 384,645 | 3.846 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 285,249 | 2.852 | 20 | 200 | fits | 120,974 | 139 | 0.464 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 265,112 | 2.651 | 20 | 20 | fits | 120,974 | 139 | 0.464 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 316,001 | 3.160 | 20 | 24 | fits | 87,337 | 61 | 0.574 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 225,637 | 2.256 | 20 | 50 | fits | 120,974 | 139 | 0.464 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 959,956 | 9.600 | 20 | 20 | fits | 60,572 | 26 | 0.672 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 186,601 | 1.866 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 179,626 | 1.796 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 297,996 | 2.980 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 281,977 | 2.820 | 20 | 200 | fits | 117,702 | 133 | 0.442 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 261,840 | 2.618 | 20 | 20 | fits | 117,702 | 133 | 0.442 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 283,023 | 2.830 | 20 | 24 | fits | 51,527 | 35 | 0.520 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 249,571 | 2.496 | 20 | 50 | fits | 122,975 | 202 | 0.302 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 925,767 | 9.258 | 20 | 20 | fits | 46,946 | 16 | 0.720 |
| an MRPDU its join timer owes, the longest | `save-flight.mrpdu.join.if0` | 62,813 | 0.628 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-flight.mrpdu.leaveall.if0` | 61,562 | 0.616 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 314,668 | 3.147 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 18,277 | 0.183 | 20 | 20 | fits | 40,085 | 19 (14) | 0.883 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 417,381 | 4.174 | 20 | 20 | fits | 148,240 | 161 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 323,829 | 3.238 | 20 | 200 | fits | 155,144 | 218 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 471,453 | 4.715 | 20 | 200 | fits | 148,240 | 161 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 324,753 | 3.248 | 20 | 20 | fits | 155,144 | 218 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 563,417 | 5.634 | 20 | 20 | fits | 91,260 | 27 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 164,312 | 1.643 | 20 | 24 | fits | 151,277 | 165 | 0.397 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 327,403 | 3.274 | 20 | 24 | fits | 155,144 | 218 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 327,337 | 3.273 | 20 | 50 | fits | 155,144 | 218 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 475,181 | 4.752 | 20 | 50 | fits | 148,240 | 161 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 566,375 | 5.664 | 20 | 20 | fits | 91,260 | 27 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,031,710 | 10.317 | 20 | 20 | fits | 85,217 | 35 | 0.638 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 404,881 | 4.049 | 20 | 20 | fits | 148,240 | 161 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 311,329 | 3.113 | 20 | 200 | fits | 155,144 | 218 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 458,953 | 4.590 | 20 | 200 | fits | 148,240 | 161 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 312,253 | 3.123 | 20 | 20 | fits | 155,144 | 218 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 550,917 | 5.509 | 20 | 20 | fits | 91,260 | 27 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 151,812 | 1.518 | 20 | 24 | fits | 151,277 | 165 | 0.397 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 314,903 | 3.149 | 20 | 24 | fits | 155,144 | 218 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 314,837 | 3.148 | 20 | 50 | fits | 155,144 | 218 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 462,681 | 4.627 | 20 | 50 | fits | 148,240 | 161 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 553,875 | 5.539 | 20 | 20 | fits | 91,260 | 27 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 1,019,210 | 10.192 | 20 | 20 | fits | 85,217 | 35 | 0.638 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 466,609 | 4.666 | 20 | 20 | fits | 157,528 | 166 | 0.458 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 385,296 | 3.853 | 20 | 200 | fits | 147,648 | 215 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 542,208 | 5.422 | 20 | 200 | fits | 157,528 | 166 | 0.458 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 386,220 | 3.862 | 20 | 20 | fits | 147,648 | 215 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 634,209 | 6.342 | 20 | 20 | fits | 91,297 | 27 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 233,275 | 2.333 | 20 | 24 | fits | 151,310 | 165 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 388,870 | 3.889 | 20 | 24 | fits | 147,648 | 215 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 388,804 | 3.888 | 20 | 50 | fits | 147,648 | 215 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 545,936 | 5.459 | 20 | 50 | fits | 157,528 | 166 | 0.458 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 637,167 | 6.372 | 20 | 20 | fits | 91,297 | 27 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 1,102,532 | 11.025 | 20 | 20 | fits | 85,338 | 35 | 0.643 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 454,109 | 4.541 | 20 | 20 | fits | 157,528 | 166 | 0.458 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 372,796 | 3.728 | 20 | 200 | fits | 147,648 | 215 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 529,708 | 5.297 | 20 | 200 | fits | 157,528 | 166 | 0.458 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 373,720 | 3.737 | 20 | 20 | fits | 147,648 | 215 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 621,709 | 6.217 | 20 | 20 | fits | 91,297 | 27 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 220,775 | 2.208 | 20 | 24 | fits | 151,310 | 165 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 376,370 | 3.764 | 20 | 24 | fits | 147,648 | 215 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 376,304 | 3.763 | 20 | 50 | fits | 147,648 | 215 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 533,436 | 5.334 | 20 | 50 | fits | 157,528 | 166 | 0.458 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 624,667 | 6.247 | 20 | 20 | fits | 91,297 | 27 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 1,090,032 | 10.900 | 20 | 20 | fits | 85,338 | 35 | 0.643 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 441,609 | 4.416 | 20 | 20 | fits | 157,528 | 166 | 0.458 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 360,296 | 3.603 | 20 | 200 | fits | 147,648 | 215 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 517,208 | 5.172 | 20 | 200 | fits | 157,528 | 166 | 0.458 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 361,220 | 3.612 | 20 | 20 | fits | 147,648 | 215 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 609,209 | 6.092 | 20 | 20 | fits | 91,297 | 27 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 208,275 | 2.083 | 20 | 24 | fits | 151,310 | 165 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 363,870 | 3.639 | 20 | 24 | fits | 147,648 | 215 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 363,804 | 3.638 | 20 | 50 | fits | 147,648 | 215 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 520,936 | 5.209 | 20 | 50 | fits | 157,528 | 166 | 0.458 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 612,167 | 6.122 | 20 | 20 | fits | 91,297 | 27 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 1,077,532 | 10.775 | 20 | 20 | fits | 85,338 | 35 | 0.643 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 429,109 | 4.291 | 20 | 20 | fits | 157,528 | 166 | 0.458 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 347,796 | 3.478 | 20 | 200 | fits | 147,648 | 215 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 504,708 | 5.047 | 20 | 200 | fits | 157,528 | 166 | 0.458 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 348,720 | 3.487 | 20 | 20 | fits | 147,648 | 215 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 596,709 | 5.967 | 20 | 20 | fits | 91,297 | 27 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 195,775 | 1.958 | 20 | 24 | fits | 151,310 | 165 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 351,370 | 3.514 | 20 | 24 | fits | 147,648 | 215 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 351,304 | 3.513 | 20 | 50 | fits | 147,648 | 215 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 508,436 | 5.084 | 20 | 50 | fits | 157,528 | 166 | 0.458 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 599,667 | 5.997 | 20 | 20 | fits | 91,297 | 27 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 1,065,032 | 10.650 | 20 | 20 | fits | 85,338 | 35 | 0.643 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 416,609 | 4.166 | 20 | 20 | fits | 157,528 | 166 | 0.458 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 335,296 | 3.353 | 20 | 200 | fits | 147,648 | 215 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 492,208 | 4.922 | 20 | 200 | fits | 157,528 | 166 | 0.458 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 336,220 | 3.362 | 20 | 20 | fits | 147,648 | 215 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 584,209 | 5.842 | 20 | 20 | fits | 91,297 | 27 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 183,275 | 1.833 | 20 | 24 | fits | 151,310 | 165 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 338,870 | 3.389 | 20 | 24 | fits | 147,648 | 215 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 338,804 | 3.388 | 20 | 50 | fits | 147,648 | 215 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 495,936 | 4.959 | 20 | 50 | fits | 157,528 | 166 | 0.458 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 587,167 | 5.872 | 20 | 20 | fits | 91,297 | 27 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 1,052,532 | 10.525 | 20 | 20 | fits | 85,338 | 35 | 0.643 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 404,109 | 4.041 | 20 | 20 | fits | 157,528 | 166 | 0.458 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 322,796 | 3.228 | 20 | 200 | fits | 147,648 | 215 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 479,708 | 4.797 | 20 | 200 | fits | 157,528 | 166 | 0.458 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 323,720 | 3.237 | 20 | 20 | fits | 147,648 | 215 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 571,709 | 5.717 | 20 | 20 | fits | 91,297 | 27 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 170,775 | 1.708 | 20 | 24 | fits | 151,310 | 165 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 326,370 | 3.264 | 20 | 24 | fits | 147,648 | 215 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 326,304 | 3.263 | 20 | 50 | fits | 147,648 | 215 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 483,436 | 4.834 | 20 | 50 | fits | 157,528 | 166 | 0.458 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 574,667 | 5.747 | 20 | 20 | fits | 91,297 | 27 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 1,040,032 | 10.400 | 20 | 20 | fits | 85,338 | 35 | 0.643 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 450,750 | 4.508 | 20 | 20 | fits | 148,622 | 164 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 367,345 | 3.673 | 20 | 200 | fits | 154,049 | 213 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 515,351 | 5.154 | 20 | 200 | fits | 148,622 | 164 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 368,269 | 3.683 | 20 | 20 | fits | 154,049 | 213 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 516,055 | 5.161 | 20 | 20 | fits | 148,622 | 164 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 217,860 | 2.179 | 20 | 24 | fits | 151,361 | 164 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 370,919 | 3.709 | 20 | 24 | fits | 154,049 | 213 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 370,853 | 3.709 | 20 | 50 | fits | 154,049 | 213 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 519,079 | 5.191 | 20 | 50 | fits | 148,622 | 164 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 617,710 | 6.177 | 20 | 20 | fits | 88,983 | 33 | 0.802 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 1,058,708 | 10.587 | 20 | 20 | fits | 80,021 | 28 | 0.554 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 425,750 | 4.258 | 20 | 20 | fits | 148,622 | 164 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 342,345 | 3.423 | 20 | 200 | fits | 154,049 | 213 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 490,351 | 4.904 | 20 | 200 | fits | 148,622 | 164 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 343,269 | 3.433 | 20 | 20 | fits | 154,049 | 213 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 491,055 | 4.911 | 20 | 20 | fits | 148,622 | 164 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 192,860 | 1.929 | 20 | 24 | fits | 151,361 | 164 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 345,919 | 3.459 | 20 | 24 | fits | 154,049 | 213 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 345,853 | 3.459 | 20 | 50 | fits | 154,049 | 213 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 494,079 | 4.941 | 20 | 50 | fits | 148,622 | 164 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 592,710 | 5.927 | 20 | 20 | fits | 88,983 | 33 | 0.802 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 1,033,708 | 10.337 | 20 | 20 | fits | 80,021 | 28 | 0.554 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 400,750 | 4.008 | 20 | 20 | fits | 148,622 | 164 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 317,345 | 3.173 | 20 | 200 | fits | 154,049 | 213 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 465,351 | 4.654 | 20 | 200 | fits | 148,622 | 164 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 318,269 | 3.183 | 20 | 20 | fits | 154,049 | 213 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 466,055 | 4.661 | 20 | 20 | fits | 148,622 | 164 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 167,860 | 1.679 | 20 | 24 | fits | 151,361 | 164 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 320,919 | 3.209 | 20 | 24 | fits | 154,049 | 213 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 320,853 | 3.209 | 20 | 50 | fits | 154,049 | 213 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 469,079 | 4.691 | 20 | 50 | fits | 148,622 | 164 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 567,710 | 5.677 | 20 | 20 | fits | 88,983 | 33 | 0.802 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 1,008,708 | 10.087 | 20 | 20 | fits | 80,021 | 28 | 0.554 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 389,075 | 3.891 | 20 | 20 | fits | 148,190 | 162 | 0.435 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 317,512 | 3.175 | 20 | 200 | fits | 155,341 | 217 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 465,086 | 4.651 | 20 | 200 | fits | 148,190 | 162 | 0.435 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 318,436 | 3.184 | 20 | 20 | fits | 155,341 | 217 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 465,790 | 4.658 | 20 | 20 | fits | 148,190 | 162 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 166,735 | 1.667 | 20 | 24 | fits | 151,199 | 164 | 0.397 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 321,086 | 3.211 | 20 | 24 | fits | 155,341 | 217 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 321,020 | 3.210 | 20 | 50 | fits | 155,341 | 217 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 468,814 | 4.688 | 20 | 50 | fits | 148,190 | 162 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 567,357 | 5.674 | 20 | 20 | fits | 88,895 | 33 | 0.801 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 1,008,355 | 10.084 | 20 | 20 | fits | 80,021 | 28 | 0.554 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 470,666 | 4.707 | 20 | 20 | fits | 157,245 | 166 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 390,533 | 3.905 | 20 | 200 | fits | 155,299 | 217 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 547,162 | 5.472 | 20 | 200 | fits | 157,245 | 166 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 391,457 | 3.915 | 20 | 20 | fits | 155,299 | 217 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 547,866 | 5.479 | 20 | 20 | fits | 157,245 | 166 | 0.461 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 239,798 | 2.398 | 20 | 24 | fits | 151,376 | 164 | 0.399 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 394,107 | 3.941 | 20 | 24 | fits | 155,299 | 217 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 394,041 | 3.940 | 20 | 50 | fits | 155,299 | 217 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 550,890 | 5.509 | 20 | 50 | fits | 157,245 | 166 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 656,449 | 6.564 | 20 | 20 | fits | 95,494 | 31 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 1,086,508 | 10.865 | 20 | 20 | fits | 69,055 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 445,666 | 4.457 | 20 | 20 | fits | 157,245 | 166 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 365,533 | 3.655 | 20 | 200 | fits | 155,299 | 217 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 522,162 | 5.222 | 20 | 200 | fits | 157,245 | 166 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 366,457 | 3.665 | 20 | 20 | fits | 155,299 | 217 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 522,866 | 5.229 | 20 | 20 | fits | 157,245 | 166 | 0.461 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 214,798 | 2.148 | 20 | 24 | fits | 151,376 | 164 | 0.399 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 369,107 | 3.691 | 20 | 24 | fits | 155,299 | 217 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 369,041 | 3.690 | 20 | 50 | fits | 155,299 | 217 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 525,890 | 5.259 | 20 | 50 | fits | 157,245 | 166 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 631,449 | 6.314 | 20 | 20 | fits | 95,494 | 31 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 1,061,508 | 10.615 | 20 | 20 | fits | 69,055 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 420,666 | 4.207 | 20 | 20 | fits | 157,245 | 166 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 340,533 | 3.405 | 20 | 200 | fits | 155,299 | 217 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 497,162 | 4.972 | 20 | 200 | fits | 157,245 | 166 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 341,457 | 3.415 | 20 | 20 | fits | 155,299 | 217 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 497,866 | 4.979 | 20 | 20 | fits | 157,245 | 166 | 0.461 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 189,798 | 1.898 | 20 | 24 | fits | 151,376 | 164 | 0.399 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 344,107 | 3.441 | 20 | 24 | fits | 155,299 | 217 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 344,041 | 3.440 | 20 | 50 | fits | 155,299 | 217 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 500,890 | 5.009 | 20 | 50 | fits | 157,245 | 166 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 606,449 | 6.064 | 20 | 20 | fits | 95,494 | 31 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 1,036,508 | 10.365 | 20 | 20 | fits | 69,055 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 395,666 | 3.957 | 20 | 20 | fits | 157,245 | 166 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 315,533 | 3.155 | 20 | 200 | fits | 155,299 | 217 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 472,162 | 4.722 | 20 | 200 | fits | 157,245 | 166 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 316,457 | 3.165 | 20 | 20 | fits | 155,299 | 217 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 472,866 | 4.729 | 20 | 20 | fits | 157,245 | 166 | 0.461 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 164,798 | 1.648 | 20 | 24 | fits | 151,376 | 164 | 0.399 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 319,107 | 3.191 | 20 | 24 | fits | 155,299 | 217 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 319,041 | 3.190 | 20 | 50 | fits | 155,299 | 217 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 475,890 | 4.759 | 20 | 50 | fits | 157,245 | 166 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 581,449 | 5.814 | 20 | 20 | fits | 95,494 | 31 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 1,011,508 | 10.115 | 20 | 20 | fits | 69,055 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 393,033 | 3.930 | 20 | 20 | fits | 148,042 | 161 | 0.435 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 321,403 | 3.214 | 20 | 200 | fits | 156,123 | 222 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 468,829 | 4.688 | 20 | 200 | fits | 148,042 | 161 | 0.435 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 322,327 | 3.223 | 20 | 20 | fits | 156,123 | 222 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 469,533 | 4.695 | 20 | 20 | fits | 148,042 | 161 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 160,772 | 1.608 | 20 | 24 | fits | 151,021 | 165 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 324,977 | 3.250 | 20 | 24 | fits | 156,123 | 222 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 324,911 | 3.249 | 20 | 50 | fits | 156,123 | 222 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 472,557 | 4.726 | 20 | 50 | fits | 148,042 | 161 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 569,196 | 5.692 | 20 | 20 | fits | 96,705 | 30 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,014,907 | 10.149 | 20 | 20 | fits | 73,982 | 31 | 0.672 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 475,076 | 4.751 | 20 | 20 | fits | 148,224 | 160 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 403,972 | 4.040 | 20 | 200 | fits | 156,226 | 222 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 551,580 | 5.516 | 20 | 200 | fits | 148,224 | 160 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 404,896 | 4.049 | 20 | 20 | fits | 156,226 | 222 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 552,284 | 5.523 | 20 | 20 | fits | 148,224 | 160 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 243,291 | 2.433 | 20 | 24 | fits | 151,066 | 165 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 407,546 | 4.075 | 20 | 24 | fits | 156,226 | 222 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 407,480 | 4.075 | 20 | 50 | fits | 156,226 | 222 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 555,308 | 5.553 | 20 | 50 | fits | 148,224 | 160 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 641,318 | 6.413 | 20 | 20 | fits | 86,076 | 26 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 1,097,917 | 10.979 | 20 | 20 | fits | 84,948 | 35 | 0.633 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 462,576 | 4.626 | 20 | 20 | fits | 148,224 | 160 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 391,472 | 3.915 | 20 | 200 | fits | 156,226 | 222 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 539,080 | 5.391 | 20 | 200 | fits | 148,224 | 160 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 392,396 | 3.924 | 20 | 20 | fits | 156,226 | 222 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 539,784 | 5.398 | 20 | 20 | fits | 148,224 | 160 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 230,791 | 2.308 | 20 | 24 | fits | 151,066 | 165 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 395,046 | 3.950 | 20 | 24 | fits | 156,226 | 222 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 394,980 | 3.950 | 20 | 50 | fits | 156,226 | 222 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 542,808 | 5.428 | 20 | 50 | fits | 148,224 | 160 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 628,818 | 6.288 | 20 | 20 | fits | 86,076 | 26 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 1,085,417 | 10.854 | 20 | 20 | fits | 84,948 | 35 | 0.633 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 450,076 | 4.501 | 20 | 20 | fits | 148,224 | 160 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 378,972 | 3.790 | 20 | 200 | fits | 156,226 | 222 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 526,580 | 5.266 | 20 | 200 | fits | 148,224 | 160 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 379,896 | 3.799 | 20 | 20 | fits | 156,226 | 222 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 527,284 | 5.273 | 20 | 20 | fits | 148,224 | 160 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 218,291 | 2.183 | 20 | 24 | fits | 151,066 | 165 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 382,546 | 3.825 | 20 | 24 | fits | 156,226 | 222 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 382,480 | 3.825 | 20 | 50 | fits | 156,226 | 222 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 530,308 | 5.303 | 20 | 50 | fits | 148,224 | 160 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 616,318 | 6.163 | 20 | 20 | fits | 86,076 | 26 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 1,072,917 | 10.729 | 20 | 20 | fits | 84,948 | 35 | 0.633 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 437,576 | 4.376 | 20 | 20 | fits | 148,224 | 160 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 366,472 | 3.665 | 20 | 200 | fits | 156,226 | 222 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 514,080 | 5.141 | 20 | 200 | fits | 148,224 | 160 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 367,396 | 3.674 | 20 | 20 | fits | 156,226 | 222 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 514,784 | 5.148 | 20 | 20 | fits | 148,224 | 160 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 205,791 | 2.058 | 20 | 24 | fits | 151,066 | 165 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 370,046 | 3.700 | 20 | 24 | fits | 156,226 | 222 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 369,980 | 3.700 | 20 | 50 | fits | 156,226 | 222 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 517,808 | 5.178 | 20 | 50 | fits | 148,224 | 160 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 603,818 | 6.038 | 20 | 20 | fits | 86,076 | 26 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 1,060,417 | 10.604 | 20 | 20 | fits | 84,948 | 35 | 0.633 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 425,076 | 4.251 | 20 | 20 | fits | 148,224 | 160 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 353,972 | 3.540 | 20 | 200 | fits | 156,226 | 222 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 501,580 | 5.016 | 20 | 200 | fits | 148,224 | 160 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 354,896 | 3.549 | 20 | 20 | fits | 156,226 | 222 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 502,284 | 5.023 | 20 | 20 | fits | 148,224 | 160 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 193,291 | 1.933 | 20 | 24 | fits | 151,066 | 165 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 357,546 | 3.575 | 20 | 24 | fits | 156,226 | 222 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 357,480 | 3.575 | 20 | 50 | fits | 156,226 | 222 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 505,308 | 5.053 | 20 | 50 | fits | 148,224 | 160 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 591,318 | 5.913 | 20 | 20 | fits | 86,076 | 26 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 1,047,917 | 10.479 | 20 | 20 | fits | 84,948 | 35 | 0.633 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 382,226 | 3.822 | 20 | 20 | fits | 148,283 | 160 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 311,122 | 3.111 | 20 | 200 | fits | 156,120 | 222 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 458,789 | 4.588 | 20 | 200 | fits | 148,283 | 160 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 312,046 | 3.120 | 20 | 20 | fits | 156,120 | 222 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 459,493 | 4.595 | 20 | 20 | fits | 148,283 | 160 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 150,547 | 1.505 | 20 | 24 | fits | 152,264 | 165 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 314,696 | 3.147 | 20 | 24 | fits | 156,120 | 222 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 314,630 | 3.146 | 20 | 50 | fits | 156,120 | 222 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 462,517 | 4.625 | 20 | 50 | fits | 148,283 | 160 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 548,527 | 5.485 | 20 | 20 | fits | 86,076 | 26 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 1,005,126 | 10.051 | 20 | 20 | fits | 84,948 | 35 | 0.633 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 382,226 | 3.822 | 20 | 20 | fits | 148,283 | 160 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 311,122 | 3.111 | 20 | 200 | fits | 156,120 | 222 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 458,789 | 4.588 | 20 | 200 | fits | 148,283 | 160 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 312,046 | 3.120 | 20 | 20 | fits | 156,120 | 222 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 459,493 | 4.595 | 20 | 20 | fits | 148,283 | 160 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 150,547 | 1.505 | 20 | 24 | fits | 152,264 | 165 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 314,696 | 3.147 | 20 | 24 | fits | 156,120 | 222 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 314,630 | 3.146 | 20 | 50 | fits | 156,120 | 222 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 462,517 | 4.625 | 20 | 50 | fits | 148,283 | 160 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 548,527 | 5.485 | 20 | 20 | fits | 86,076 | 26 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 1,005,126 | 10.051 | 20 | 20 | fits | 84,948 | 35 | 0.633 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 384,111 | 3.841 | 20 | 20 | fits | 147,975 | 161 | 0.434 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 312,548 | 3.125 | 20 | 200 | fits | 155,305 | 217 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 459,907 | 4.599 | 20 | 200 | fits | 147,975 | 161 | 0.434 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 313,472 | 3.135 | 20 | 20 | fits | 155,305 | 217 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 460,611 | 4.606 | 20 | 20 | fits | 147,975 | 161 | 0.434 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 161,807 | 1.618 | 20 | 24 | fits | 149,148 | 161 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 316,122 | 3.161 | 20 | 24 | fits | 155,305 | 217 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 316,056 | 3.161 | 20 | 50 | fits | 155,305 | 217 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 463,635 | 4.636 | 20 | 50 | fits | 147,975 | 161 | 0.434 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 554,519 | 5.545 | 20 | 20 | fits | 90,950 | 24 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 1,007,336 | 10.073 | 20 | 20 | fits | 74,618 | 30 | 0.644 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 374,789 | 3.748 | 20 | 20 | fits | 148,452 | 161 | 0.436 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 303,749 | 3.037 | 20 | 200 | fits | 155,346 | 217 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 451,585 | 4.516 | 20 | 200 | fits | 148,452 | 161 | 0.436 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 304,673 | 3.047 | 20 | 20 | fits | 155,346 | 217 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 452,289 | 4.523 | 20 | 20 | fits | 148,452 | 161 | 0.436 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 152,967 | 1.530 | 20 | 24 | fits | 149,148 | 161 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 307,323 | 3.073 | 20 | 24 | fits | 155,346 | 217 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 307,257 | 3.073 | 20 | 50 | fits | 155,346 | 217 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 455,313 | 4.553 | 20 | 50 | fits | 148,452 | 161 | 0.436 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 546,494 | 5.465 | 20 | 20 | fits | 91,247 | 25 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 1,074,558 | 10.746 | 20 | 20 | fits | 80,613 | 29 | 0.551 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 395,792 | 3.958 | 20 | 20 | fits | 148,918 | 162 | 0.436 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 314,660 | 3.147 | 20 | 200 | fits | 155,792 | 217 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 462,962 | 4.630 | 20 | 200 | fits | 148,918 | 162 | 0.436 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 315,584 | 3.156 | 20 | 20 | fits | 155,792 | 217 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 463,666 | 4.637 | 20 | 20 | fits | 148,918 | 162 | 0.436 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 163,432 | 1.634 | 20 | 24 | fits | 149,093 | 161 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 318,234 | 3.182 | 20 | 24 | fits | 155,792 | 217 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 318,168 | 3.182 | 20 | 50 | fits | 155,792 | 217 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 466,690 | 4.667 | 20 | 50 | fits | 148,918 | 162 | 0.436 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 571,999 | 5.720 | 20 | 20 | fits | 95,673 | 31 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,084,750 | 10.848 | 20 | 20 | fits | 80,001 | 28 | 0.556 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 401,129 | 4.011 | 20 | 20 | fits | 153,087 | 170 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 304,326 | 3.043 | 20 | 200 | fits | 154,298 | 214 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 466,494 | 4.665 | 20 | 200 | fits | 153,087 | 170 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 305,250 | 3.053 | 20 | 20 | fits | 154,298 | 214 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 467,198 | 4.672 | 20 | 20 | fits | 153,087 | 170 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 154,592 | 1.546 | 20 | 24 | fits | 149,093 | 161 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 307,900 | 3.079 | 20 | 24 | fits | 154,298 | 214 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 307,834 | 3.078 | 20 | 50 | fits | 154,298 | 214 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 470,222 | 4.702 | 20 | 50 | fits | 153,087 | 170 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 561,789 | 5.618 | 20 | 20 | fits | 91,633 | 24 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,074,692 | 10.747 | 20 | 20 | fits | 80,149 | 29 | 0.556 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 373,382 | 3.734 | 20 | 20 | fits | 148,947 | 199 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 281,501 | 2.815 | 20 | 200 | fits | 147,807 | 216 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 439,529 | 4.395 | 20 | 200 | fits | 148,947 | 199 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 282,425 | 2.824 | 20 | 20 | fits | 147,807 | 216 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 527,606 | 5.276 | 20 | 20 | fits | 87,373 | 37 | 0.769 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 138,258 | 1.383 | 20 | 24 | fits | 141,599 | 120 | 0.402 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 285,075 | 2.851 | 20 | 24 | fits | 147,807 | 216 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 285,009 | 2.850 | 20 | 50 | fits | 147,807 | 216 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 443,257 | 4.433 | 20 | 50 | fits | 148,947 | 199 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 530,564 | 5.306 | 20 | 20 | fits | 87,373 | 37 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,112,353 | 11.124 | 20 | 20 | fits | 41,024 | 19 | 0.824 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 388,363 | 3.884 | 20 | 20 | fits | 154,919 | 177 | 0.465 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 308,242 | 3.082 | 20 | 200 | fits | 147,812 | 200 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 462,545 | 4.625 | 20 | 200 | fits | 154,919 | 177 | 0.465 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 309,166 | 3.092 | 20 | 20 | fits | 147,812 | 200 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 631,325 | 6.313 | 20 | 20 | fits | 91,898 | 28 | 0.779 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 156,419 | 1.564 | 20 | 24 | fits | 149,240 | 162 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 311,816 | 3.118 | 20 | 24 | fits | 147,812 | 200 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 311,750 | 3.118 | 20 | 50 | fits | 147,812 | 200 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 466,273 | 4.663 | 20 | 50 | fits | 154,919 | 177 | 0.465 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 634,283 | 6.343 | 20 | 20 | fits | 91,898 | 28 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,091,773 | 10.918 | 20 | 20 | fits | 85,338 | 35 | 0.643 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 404,056 | 4.041 | 20 | 20 | fits | 156,538 | 164 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 313,742 | 3.137 | 20 | 200 | fits | 155,758 | 217 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 469,664 | 4.697 | 20 | 200 | fits | 156,538 | 164 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 314,666 | 3.147 | 20 | 20 | fits | 155,758 | 217 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 470,368 | 4.704 | 20 | 20 | fits | 156,538 | 164 | 0.460 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 162,548 | 1.625 | 20 | 24 | fits | 149,305 | 161 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 317,316 | 3.173 | 20 | 24 | fits | 155,758 | 217 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 317,250 | 3.172 | 20 | 50 | fits | 155,758 | 217 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 473,392 | 4.734 | 20 | 50 | fits | 156,538 | 164 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 641,309 | 6.413 | 20 | 20 | fits | 91,895 | 25 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,087,679 | 10.877 | 20 | 20 | fits | 69,055 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 471,269 | 4.713 | 20 | 20 | fits | 147,391 | 177 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 302,573 | 3.026 | 20 | 200 | fits | 153,429 | 196 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 525,759 | 5.258 | 20 | 200 | fits | 147,391 | 177 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 303,497 | 3.035 | 20 | 20 | fits | 153,429 | 196 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 618,096 | 6.181 | 20 | 20 | fits | 91,633 | 28 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 153,708 | 1.537 | 20 | 24 | fits | 149,305 | 161 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 306,147 | 3.061 | 20 | 24 | fits | 153,429 | 196 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 306,081 | 3.061 | 20 | 50 | fits | 153,429 | 196 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 529,487 | 5.295 | 20 | 50 | fits | 147,391 | 177 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 621,054 | 6.211 | 20 | 20 | fits | 91,633 | 28 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,078,409 | 10.784 | 20 | 20 | fits | 80,021 | 28 | 0.554 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 390,734 | 3.907 | 20 | 20 | fits | 147,988 | 161 | 0.435 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 319,104 | 3.191 | 20 | 200 | fits | 156,210 | 222 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 466,476 | 4.665 | 20 | 200 | fits | 147,988 | 161 | 0.435 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 320,028 | 3.200 | 20 | 20 | fits | 156,210 | 222 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 467,180 | 4.672 | 20 | 20 | fits | 147,988 | 161 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 158,883 | 1.589 | 20 | 24 | fits | 149,191 | 162 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 322,678 | 3.227 | 20 | 24 | fits | 156,210 | 222 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 322,612 | 3.226 | 20 | 50 | fits | 156,210 | 222 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 470,204 | 4.702 | 20 | 50 | fits | 147,988 | 161 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 561,152 | 5.612 | 20 | 20 | fits | 91,014 | 24 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 991,209 | 9.912 | 20 | 20 | fits | 69,213 | 25 | 0.601 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 361,795 | 3.618 | 20 | 20 | fits | 156,914 | 202 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 281,265 | 2.813 | 20 | 200 | fits | 147,622 | 215 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 437,563 | 4.376 | 20 | 200 | fits | 156,914 | 202 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 282,189 | 2.822 | 20 | 20 | fits | 147,622 | 215 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 529,736 | 5.297 | 20 | 20 | fits | 91,469 | 27 | 0.785 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 138,207 | 1.382 | 20 | 24 | fits | 141,889 | 120 | 0.405 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 284,839 | 2.848 | 20 | 24 | fits | 147,622 | 215 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 284,773 | 2.848 | 20 | 50 | fits | 147,622 | 215 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 441,291 | 4.413 | 20 | 50 | fits | 156,914 | 202 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 532,694 | 5.327 | 20 | 20 | fits | 91,469 | 27 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 996,627 | 9.966 | 20 | 20 | fits | 90,953 | 32 | 0.532 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 378,044 | 3.780 | 20 | 20 | fits | 148,350 | 161 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 307,240 | 3.072 | 20 | 200 | fits | 155,638 | 217 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 454,974 | 4.550 | 20 | 200 | fits | 148,350 | 161 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 308,164 | 3.082 | 20 | 20 | fits | 155,638 | 217 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 455,678 | 4.557 | 20 | 20 | fits | 148,350 | 161 | 0.432 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 156,166 | 1.562 | 20 | 24 | fits | 149,250 | 161 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 310,814 | 3.108 | 20 | 24 | fits | 155,638 | 217 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 310,748 | 3.107 | 20 | 50 | fits | 155,638 | 217 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 458,702 | 4.587 | 20 | 50 | fits | 148,350 | 161 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 549,879 | 5.499 | 20 | 20 | fits | 91,243 | 24 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 1,001,374 | 10.014 | 20 | 20 | fits | 80,021 | 28 | 0.554 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 380,315 | 3.803 | 20 | 20 | fits | 155,724 | 179 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 290,748 | 2.907 | 20 | 200 | fits | 147,986 | 200 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 445,856 | 4.459 | 20 | 200 | fits | 155,724 | 179 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 291,672 | 2.917 | 20 | 20 | fits | 147,986 | 200 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 446,560 | 4.466 | 20 | 20 | fits | 155,724 | 179 | 0.422 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 147,326 | 1.473 | 20 | 24 | fits | 149,250 | 161 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 294,322 | 2.943 | 20 | 24 | fits | 147,986 | 200 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 294,256 | 2.943 | 20 | 50 | fits | 147,986 | 200 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 449,584 | 4.496 | 20 | 50 | fits | 155,724 | 179 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 540,952 | 5.410 | 20 | 20 | fits | 91,434 | 25 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 992,166 | 9.922 | 20 | 20 | fits | 80,021 | 28 | 0.554 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 380,169 | 3.802 | 20 | 20 | fits | 148,188 | 162 | 0.434 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 308,608 | 3.086 | 20 | 200 | fits | 155,271 | 217 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 456,180 | 4.562 | 20 | 200 | fits | 148,188 | 162 | 0.434 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 309,532 | 3.095 | 20 | 20 | fits | 155,271 | 217 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 456,884 | 4.569 | 20 | 20 | fits | 148,188 | 162 | 0.434 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 157,901 | 1.579 | 20 | 24 | fits | 149,305 | 161 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 312,182 | 3.122 | 20 | 24 | fits | 155,271 | 217 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 312,116 | 3.121 | 20 | 50 | fits | 155,271 | 217 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 459,908 | 4.599 | 20 | 50 | fits | 148,188 | 162 | 0.434 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 558,329 | 5.583 | 20 | 20 | fits | 88,876 | 33 | 0.802 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 999,410 | 9.994 | 20 | 20 | fits | 80,021 | 28 | 0.554 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 374,100 | 3.741 | 20 | 20 | fits | 151,085 | 165 | 0.459 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 291,004 | 2.910 | 20 | 200 | fits | 147,865 | 216 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 451,124 | 4.511 | 20 | 200 | fits | 151,085 | 165 | 0.459 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 291,928 | 2.919 | 20 | 20 | fits | 147,865 | 216 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 540,425 | 5.404 | 20 | 20 | fits | 88,597 | 31 | 0.803 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 147,703 | 1.477 | 20 | 24 | fits | 149,305 | 161 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 294,578 | 2.946 | 20 | 24 | fits | 147,865 | 216 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 294,512 | 2.945 | 20 | 50 | fits | 147,865 | 216 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 454,852 | 4.549 | 20 | 50 | fits | 151,085 | 165 | 0.459 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 543,383 | 5.434 | 20 | 20 | fits | 88,597 | 31 | 0.803 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 995,118 | 9.951 | 20 | 20 | fits | 90,618 | 32 | 0.514 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 410,217 | 4.102 | 20 | 20 | fits | 154,134 | 176 | 0.458 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 311,552 | 3.116 | 20 | 200 | fits | 147,957 | 200 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 465,070 | 4.651 | 20 | 200 | fits | 154,134 | 176 | 0.458 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 312,476 | 3.125 | 20 | 20 | fits | 147,957 | 200 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 556,678 | 5.567 | 20 | 20 | fits | 90,904 | 27 | 0.779 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 159,654 | 1.597 | 20 | 24 | fits | 149,378 | 162 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 315,126 | 3.151 | 20 | 24 | fits | 147,957 | 200 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 315,060 | 3.151 | 20 | 50 | fits | 147,957 | 200 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 468,798 | 4.688 | 20 | 50 | fits | 154,134 | 176 | 0.458 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 559,636 | 5.596 | 20 | 20 | fits | 90,904 | 27 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 1,017,016 | 10.170 | 20 | 20 | fits | 85,267 | 35 | 0.641 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 388,050 | 3.881 | 20 | 20 | fits | 150,881 | 207 | 0.442 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 281,652 | 2.817 | 20 | 200 | fits | 148,059 | 200 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 431,917 | 4.319 | 20 | 200 | fits | 150,881 | 207 | 0.442 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 282,576 | 2.826 | 20 | 20 | fits | 148,059 | 200 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 523,292 | 5.233 | 20 | 20 | fits | 90,671 | 33 | 0.752 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 138,157 | 1.382 | 20 | 24 | fits | 145,332 | 131 | 0.406 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 285,226 | 2.852 | 20 | 24 | fits | 148,059 | 200 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 285,160 | 2.852 | 20 | 50 | fits | 148,059 | 200 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 435,645 | 4.356 | 20 | 50 | fits | 150,881 | 207 | 0.442 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 526,250 | 5.263 | 20 | 20 | fits | 90,671 | 33 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 994,521 | 9.945 | 20 | 20 | fits | 90,981 | 32 | 0.534 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 391,374 | 3.914 | 20 | 20 | fits | 151,314 | 169 | 0.434 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 305,232 | 3.052 | 20 | 200 | fits | 154,924 | 218 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 455,930 | 4.559 | 20 | 200 | fits | 151,314 | 169 | 0.434 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 306,156 | 3.062 | 20 | 20 | fits | 154,924 | 218 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 456,634 | 4.566 | 20 | 20 | fits | 151,314 | 169 | 0.434 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 146,172 | 1.462 | 20 | 24 | fits | 149,456 | 162 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 308,806 | 3.088 | 20 | 24 | fits | 154,924 | 218 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 308,740 | 3.087 | 20 | 50 | fits | 154,924 | 218 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 459,658 | 4.597 | 20 | 50 | fits | 151,314 | 169 | 0.434 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 550,650 | 5.506 | 20 | 20 | fits | 91,058 | 24 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 980,567 | 9.806 | 20 | 20 | fits | 69,213 | 25 | 0.601 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 374,969 | 3.750 | 20 | 20 | fits | 147,921 | 161 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 303,406 | 3.034 | 20 | 200 | fits | 155,165 | 217 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 450,711 | 4.507 | 20 | 200 | fits | 147,921 | 161 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 304,330 | 3.043 | 20 | 20 | fits | 155,165 | 217 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 451,415 | 4.514 | 20 | 20 | fits | 147,921 | 161 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 152,805 | 1.528 | 20 | 24 | fits | 149,264 | 161 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 306,980 | 3.070 | 20 | 24 | fits | 155,165 | 217 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 306,914 | 3.069 | 20 | 50 | fits | 155,165 | 217 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 454,439 | 4.544 | 20 | 50 | fits | 147,921 | 161 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 545,377 | 5.454 | 20 | 20 | fits | 91,004 | 24 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 1,078,469 | 10.785 | 20 | 20 | fits | 80,596 | 29 | 0.562 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 385,044 | 3.850 | 20 | 20 | fits | 148,352 | 161 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 314,238 | 3.142 | 20 | 200 | fits | 155,532 | 217 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 461,974 | 4.620 | 20 | 200 | fits | 148,352 | 161 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 315,162 | 3.152 | 20 | 20 | fits | 155,532 | 217 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 462,678 | 4.627 | 20 | 20 | fits | 148,352 | 161 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 163,270 | 1.633 | 20 | 24 | fits | 149,209 | 161 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 317,812 | 3.178 | 20 | 24 | fits | 155,532 | 217 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 317,746 | 3.177 | 20 | 50 | fits | 155,532 | 217 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 465,702 | 4.657 | 20 | 50 | fits | 148,352 | 161 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 556,801 | 5.568 | 20 | 20 | fits | 91,165 | 24 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,090,014 | 10.900 | 20 | 20 | fits | 80,103 | 28 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 386,650 | 3.866 | 20 | 20 | fits | 148,595 | 161 | 0.434 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 305,518 | 3.055 | 20 | 200 | fits | 155,652 | 217 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 453,497 | 4.535 | 20 | 200 | fits | 148,595 | 161 | 0.434 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 306,442 | 3.064 | 20 | 20 | fits | 155,652 | 217 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 454,201 | 4.542 | 20 | 20 | fits | 148,595 | 161 | 0.434 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 154,430 | 1.544 | 20 | 24 | fits | 149,209 | 161 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 309,092 | 3.091 | 20 | 24 | fits | 155,652 | 217 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 309,026 | 3.090 | 20 | 50 | fits | 155,652 | 217 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 457,225 | 4.572 | 20 | 50 | fits | 148,595 | 161 | 0.434 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 548,335 | 5.483 | 20 | 20 | fits | 91,176 | 25 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,080,083 | 10.801 | 20 | 20 | fits | 80,021 | 28 | 0.554 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 381,173 | 3.812 | 20 | 20 | fits | 148,043 | 199 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 288,544 | 2.885 | 20 | 200 | fits | 155,012 | 218 | 0.432 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 435,971 | 4.360 | 20 | 200 | fits | 148,043 | 199 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 289,468 | 2.895 | 20 | 20 | fits | 155,012 | 218 | 0.432 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 537,687 | 5.377 | 20 | 20 | fits | 91,325 | 38 | 0.798 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 138,096 | 1.381 | 20 | 24 | fits | 141,715 | 120 | 0.403 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 292,118 | 2.921 | 20 | 24 | fits | 155,012 | 218 | 0.432 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 292,052 | 2.921 | 20 | 50 | fits | 155,012 | 218 | 0.432 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 439,699 | 4.397 | 20 | 50 | fits | 148,043 | 199 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 540,645 | 5.406 | 20 | 20 | fits | 91,325 | 38 | 0.798 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,074,268 | 10.743 | 20 | 20 | fits | 90,618 | 32 | 0.514 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 399,289 | 3.993 | 20 | 20 | fits | 149,654 | 164 | 0.486 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 307,071 | 3.071 | 20 | 200 | fits | 155,470 | 218 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 465,726 | 4.657 | 20 | 200 | fits | 149,654 | 164 | 0.486 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 307,995 | 3.080 | 20 | 20 | fits | 155,470 | 218 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 639,044 | 6.390 | 20 | 20 | fits | 91,835 | 28 | 0.781 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 156,165 | 1.562 | 20 | 24 | fits | 149,264 | 161 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 310,645 | 3.106 | 20 | 24 | fits | 155,470 | 218 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 310,579 | 3.106 | 20 | 50 | fits | 155,470 | 218 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 469,454 | 4.695 | 20 | 50 | fits | 149,654 | 164 | 0.486 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 642,002 | 6.420 | 20 | 20 | fits | 91,835 | 28 | 0.781 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,083,096 | 10.831 | 20 | 20 | fits | 80,021 | 28 | 0.554 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 380,595 | 3.806 | 20 | 20 | fits | 156,312 | 183 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 299,178 | 2.992 | 20 | 200 | fits | 147,647 | 200 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 454,874 | 4.549 | 20 | 200 | fits | 156,312 | 183 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 300,102 | 3.001 | 20 | 20 | fits | 147,647 | 200 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 627,885 | 6.279 | 20 | 20 | fits | 91,687 | 28 | 0.781 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 147,465 | 1.475 | 20 | 24 | fits | 149,404 | 162 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 302,752 | 3.028 | 20 | 24 | fits | 147,647 | 200 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 302,686 | 3.027 | 20 | 50 | fits | 147,647 | 200 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 458,602 | 4.586 | 20 | 50 | fits | 156,312 | 183 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 630,843 | 6.308 | 20 | 20 | fits | 91,687 | 28 | 0.781 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,088,351 | 10.884 | 20 | 20 | fits | 80,382 | 28 | 0.574 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 474,306 | 4.743 | 20 | 20 | fits | 155,939 | 179 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 303,872 | 3.039 | 20 | 200 | fits | 155,017 | 200 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 540,006 | 5.400 | 20 | 200 | fits | 155,939 | 179 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 304,796 | 3.048 | 20 | 20 | fits | 155,017 | 200 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 540,710 | 5.407 | 20 | 20 | fits | 155,939 | 179 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 153,419 | 1.534 | 20 | 24 | fits | 149,605 | 161 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 307,446 | 3.074 | 20 | 24 | fits | 155,017 | 200 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 307,380 | 3.074 | 20 | 50 | fits | 155,017 | 200 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 543,734 | 5.437 | 20 | 50 | fits | 155,939 | 179 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 634,674 | 6.347 | 20 | 20 | fits | 91,006 | 24 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,080,979 | 10.810 | 20 | 20 | fits | 69,055 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 403,602 | 4.036 | 20 | 20 | fits | 153,058 | 170 | 0.452 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 306,821 | 3.068 | 20 | 200 | fits | 154,345 | 214 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 468,967 | 4.690 | 20 | 200 | fits | 153,058 | 170 | 0.452 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 307,745 | 3.077 | 20 | 20 | fits | 154,345 | 214 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 469,671 | 4.697 | 20 | 20 | fits | 153,058 | 170 | 0.452 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 157,040 | 1.570 | 20 | 24 | fits | 149,169 | 161 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 310,395 | 3.104 | 20 | 24 | fits | 154,345 | 214 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 310,329 | 3.103 | 20 | 50 | fits | 154,345 | 214 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 472,695 | 4.727 | 20 | 50 | fits | 153,058 | 170 | 0.452 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 563,931 | 5.639 | 20 | 20 | fits | 91,302 | 24 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 993,674 | 9.937 | 20 | 20 | fits | 69,055 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 382,073 | 3.821 | 20 | 20 | fits | 150,412 | 166 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 307,900 | 3.079 | 20 | 200 | fits | 156,045 | 222 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 457,696 | 4.577 | 20 | 200 | fits | 150,412 | 166 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 308,824 | 3.088 | 20 | 20 | fits | 156,045 | 222 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 458,400 | 4.584 | 20 | 20 | fits | 150,412 | 166 | 0.446 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 147,719 | 1.477 | 20 | 24 | fits | 149,321 | 162 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 311,474 | 3.115 | 20 | 24 | fits | 156,045 | 222 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 311,408 | 3.114 | 20 | 50 | fits | 156,045 | 222 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 461,424 | 4.614 | 20 | 50 | fits | 150,412 | 166 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 552,284 | 5.523 | 20 | 20 | fits | 90,926 | 24 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 992,102 | 9.921 | 20 | 20 | fits | 83,969 | 35 | 0.595 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 392,216 | 3.922 | 20 | 20 | fits | 148,347 | 161 | 0.434 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 321,469 | 3.215 | 20 | 200 | fits | 155,710 | 217 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 469,200 | 4.692 | 20 | 200 | fits | 148,347 | 161 | 0.434 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 322,393 | 3.224 | 20 | 20 | fits | 155,710 | 217 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 469,904 | 4.699 | 20 | 20 | fits | 148,347 | 161 | 0.434 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 170,323 | 1.703 | 20 | 24 | fits | 149,955 | 162 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 325,043 | 3.250 | 20 | 24 | fits | 155,710 | 217 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 324,977 | 3.250 | 20 | 50 | fits | 155,710 | 217 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 472,928 | 4.729 | 20 | 50 | fits | 148,347 | 161 | 0.434 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 563,895 | 5.639 | 20 | 20 | fits | 91,033 | 24 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 1,015,879 | 10.159 | 20 | 20 | fits | 80,433 | 28 | 0.574 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 361,431 | 3.614 | 20 | 20 | fits | 156,579 | 180 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 290,436 | 2.904 | 20 | 200 | fits | 147,760 | 200 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 446,399 | 4.464 | 20 | 200 | fits | 156,579 | 180 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 291,360 | 2.914 | 20 | 20 | fits | 147,760 | 200 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 447,103 | 4.471 | 20 | 20 | fits | 156,579 | 180 | 0.432 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 147,240 | 1.472 | 20 | 24 | fits | 149,346 | 161 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 294,010 | 2.940 | 20 | 24 | fits | 147,760 | 200 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 293,944 | 2.939 | 20 | 50 | fits | 147,760 | 200 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 450,127 | 4.501 | 20 | 50 | fits | 156,579 | 180 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 541,217 | 5.412 | 20 | 20 | fits | 91,156 | 24 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 993,109 | 9.931 | 20 | 20 | fits | 80,021 | 28 | 0.554 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 390,622 | 3.906 | 20 | 20 | fits | 148,410 | 163 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 307,160 | 3.072 | 20 | 200 | fits | 154,019 | 213 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 454,954 | 4.550 | 20 | 200 | fits | 148,410 | 163 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 308,084 | 3.081 | 20 | 20 | fits | 154,019 | 213 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 455,658 | 4.557 | 20 | 20 | fits | 148,410 | 163 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 157,705 | 1.577 | 20 | 24 | fits | 149,291 | 161 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 310,734 | 3.107 | 20 | 24 | fits | 154,019 | 213 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 310,668 | 3.107 | 20 | 50 | fits | 154,019 | 213 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 458,682 | 4.587 | 20 | 50 | fits | 148,410 | 163 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 555,412 | 5.554 | 20 | 20 | fits | 96,796 | 31 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 1,001,041 | 10.010 | 20 | 20 | fits | 69,055 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 361,862 | 3.619 | 20 | 20 | fits | 148,249 | 163 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 290,641 | 2.906 | 20 | 200 | fits | 147,516 | 215 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 438,274 | 4.383 | 20 | 200 | fits | 148,249 | 163 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 291,565 | 2.916 | 20 | 20 | fits | 147,516 | 215 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 540,214 | 5.402 | 20 | 20 | fits | 91,618 | 38 | 0.799 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 147,689 | 1.477 | 20 | 24 | fits | 149,291 | 161 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 294,215 | 2.942 | 20 | 24 | fits | 147,516 | 215 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 294,149 | 2.941 | 20 | 50 | fits | 147,516 | 215 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 442,002 | 4.420 | 20 | 50 | fits | 148,249 | 163 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 543,172 | 5.432 | 20 | 20 | fits | 91,618 | 38 | 0.799 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 995,000 | 9.950 | 20 | 20 | fits | 90,618 | 32 | 0.514 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 402,694 | 4.027 | 20 | 20 | fits | 149,654 | 164 | 0.483 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 310,610 | 3.106 | 20 | 200 | fits | 155,734 | 218 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 469,375 | 4.694 | 20 | 200 | fits | 149,654 | 164 | 0.483 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 311,534 | 3.115 | 20 | 20 | fits | 155,734 | 218 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 561,595 | 5.616 | 20 | 20 | fits | 91,516 | 27 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 159,440 | 1.594 | 20 | 24 | fits | 149,346 | 161 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 314,184 | 3.142 | 20 | 24 | fits | 155,734 | 218 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 314,118 | 3.141 | 20 | 50 | fits | 155,734 | 218 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 473,103 | 4.731 | 20 | 50 | fits | 149,654 | 164 | 0.483 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 564,553 | 5.646 | 20 | 20 | fits | 91,516 | 27 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 1,005,751 | 10.058 | 20 | 20 | fits | 80,021 | 28 | 0.554 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 403,280 | 4.033 | 20 | 20 | fits | 149,440 | 178 | 0.458 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 301,159 | 3.012 | 20 | 200 | fits | 155,123 | 201 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 459,734 | 4.597 | 20 | 200 | fits | 149,440 | 178 | 0.458 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 302,083 | 3.021 | 20 | 20 | fits | 155,123 | 201 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 551,893 | 5.519 | 20 | 20 | fits | 91,455 | 27 | 0.783 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 150,600 | 1.506 | 20 | 24 | fits | 149,346 | 161 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 304,733 | 3.047 | 20 | 24 | fits | 155,123 | 201 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 304,667 | 3.047 | 20 | 50 | fits | 155,123 | 201 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 463,462 | 4.635 | 20 | 50 | fits | 149,440 | 178 | 0.458 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 554,851 | 5.549 | 20 | 20 | fits | 91,455 | 27 | 0.783 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 996,049 | 9.960 | 20 | 20 | fits | 80,021 | 28 | 0.554 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 395,814 | 3.958 | 20 | 20 | fits | 148,864 | 162 | 0.435 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 314,682 | 3.147 | 20 | 200 | fits | 155,731 | 217 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 462,930 | 4.629 | 20 | 200 | fits | 148,864 | 162 | 0.435 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 315,606 | 3.156 | 20 | 20 | fits | 155,731 | 217 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 463,634 | 4.636 | 20 | 20 | fits | 148,864 | 162 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 163,515 | 1.635 | 20 | 24 | fits | 149,036 | 161 | 0.385 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 318,256 | 3.183 | 20 | 24 | fits | 155,731 | 217 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 318,190 | 3.182 | 20 | 50 | fits | 155,731 | 217 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 466,658 | 4.667 | 20 | 50 | fits | 148,864 | 162 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 572,065 | 5.721 | 20 | 20 | fits | 95,695 | 31 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 1,007,886 | 10.079 | 20 | 20 | fits | 74,761 | 30 | 0.647 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 387,610 | 3.876 | 20 | 20 | fits | 148,627 | 164 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 304,146 | 3.041 | 20 | 200 | fits | 154,035 | 213 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 452,157 | 4.522 | 20 | 200 | fits | 148,627 | 164 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 305,070 | 3.051 | 20 | 20 | fits | 154,035 | 213 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 452,861 | 4.529 | 20 | 20 | fits | 148,627 | 164 | 0.422 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 154,675 | 1.547 | 20 | 24 | fits | 149,036 | 161 | 0.385 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 307,720 | 3.077 | 20 | 24 | fits | 154,035 | 213 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 307,654 | 3.077 | 20 | 50 | fits | 154,035 | 213 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 455,885 | 4.559 | 20 | 50 | fits | 148,627 | 164 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 561,261 | 5.613 | 20 | 20 | fits | 95,664 | 31 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 1,075,137 | 10.751 | 20 | 20 | fits | 80,685 | 29 | 0.544 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 373,240 | 3.732 | 20 | 20 | fits | 151,353 | 166 | 0.459 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 289,035 | 2.890 | 20 | 200 | fits | 147,764 | 216 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 449,545 | 4.495 | 20 | 200 | fits | 151,353 | 166 | 0.459 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 289,959 | 2.900 | 20 | 20 | fits | 147,764 | 216 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 542,047 | 5.420 | 20 | 20 | fits | 91,798 | 27 | 0.787 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 145,835 | 1.458 | 20 | 24 | fits | 149,036 | 161 | 0.385 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 292,609 | 2.926 | 20 | 24 | fits | 147,764 | 216 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 292,543 | 2.925 | 20 | 50 | fits | 147,764 | 216 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 453,273 | 4.533 | 20 | 50 | fits | 151,353 | 166 | 0.459 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 545,005 | 5.450 | 20 | 20 | fits | 91,798 | 27 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,069,623 | 10.696 | 20 | 20 | fits | 90,598 | 32 | 0.517 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 379,488 | 3.795 | 20 | 20 | fits | 156,700 | 180 | 0.435 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 308,427 | 3.084 | 20 | 200 | fits | 147,765 | 200 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 464,511 | 4.645 | 20 | 200 | fits | 156,700 | 180 | 0.435 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 309,351 | 3.094 | 20 | 20 | fits | 147,765 | 200 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 465,215 | 4.652 | 20 | 20 | fits | 156,700 | 180 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 156,526 | 1.565 | 20 | 24 | fits | 149,207 | 162 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 312,001 | 3.120 | 20 | 24 | fits | 147,765 | 200 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 311,935 | 3.119 | 20 | 50 | fits | 147,765 | 200 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 468,239 | 4.682 | 20 | 50 | fits | 156,700 | 180 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 559,508 | 5.595 | 20 | 20 | fits | 91,335 | 24 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,089,705 | 10.897 | 20 | 20 | fits | 80,493 | 28 | 0.576 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 396,196 | 3.962 | 20 | 20 | fits | 148,647 | 161 | 0.434 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 315,066 | 3.151 | 20 | 200 | fits | 155,652 | 217 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 463,097 | 4.631 | 20 | 200 | fits | 148,647 | 161 | 0.434 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 315,990 | 3.160 | 20 | 20 | fits | 155,652 | 217 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 463,801 | 4.638 | 20 | 20 | fits | 148,647 | 161 | 0.434 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 163,978 | 1.640 | 20 | 24 | fits | 149,182 | 161 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 318,640 | 3.186 | 20 | 24 | fits | 155,652 | 217 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 318,574 | 3.186 | 20 | 50 | fits | 155,652 | 217 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 466,825 | 4.668 | 20 | 50 | fits | 148,647 | 161 | 0.434 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 563,402 | 5.634 | 20 | 20 | fits | 96,643 | 30 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,087,560 | 10.876 | 20 | 20 | fits | 69,055 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 387,992 | 3.880 | 20 | 20 | fits | 148,410 | 163 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 304,530 | 3.045 | 20 | 200 | fits | 153,956 | 213 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 452,324 | 4.523 | 20 | 200 | fits | 148,410 | 163 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 305,454 | 3.055 | 20 | 20 | fits | 153,956 | 213 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 453,028 | 4.530 | 20 | 20 | fits | 148,410 | 163 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 155,138 | 1.551 | 20 | 24 | fits | 149,090 | 161 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 308,104 | 3.081 | 20 | 24 | fits | 153,956 | 213 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 308,038 | 3.080 | 20 | 50 | fits | 153,956 | 213 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 456,052 | 4.561 | 20 | 50 | fits | 148,410 | 163 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 552,602 | 5.526 | 20 | 20 | fits | 96,616 | 30 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,077,785 | 10.778 | 20 | 20 | fits | 69,055 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 369,519 | 3.695 | 20 | 20 | fits | 156,453 | 166 | 0.454 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 289,250 | 2.893 | 20 | 200 | fits | 147,516 | 215 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 445,087 | 4.451 | 20 | 200 | fits | 156,453 | 166 | 0.454 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 290,174 | 2.902 | 20 | 20 | fits | 147,516 | 215 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 618,667 | 6.187 | 20 | 20 | fits | 95,858 | 35 | 0.780 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 146,298 | 1.463 | 20 | 24 | fits | 149,090 | 161 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 292,824 | 2.928 | 20 | 24 | fits | 147,516 | 215 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 292,758 | 2.928 | 20 | 50 | fits | 147,516 | 215 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 448,815 | 4.488 | 20 | 50 | fits | 156,453 | 166 | 0.454 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 621,625 | 6.216 | 20 | 20 | fits | 95,858 | 35 | 0.780 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,075,489 | 10.755 | 20 | 20 | fits | 80,021 | 28 | 0.554 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 459,080 | 4.591 | 20 | 20 | fits | 149,321 | 178 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 307,161 | 3.072 | 20 | 200 | fits | 154,852 | 200 | 0.447 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 533,142 | 5.331 | 20 | 200 | fits | 149,321 | 178 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 308,085 | 3.081 | 20 | 20 | fits | 154,852 | 200 | 0.447 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 636,899 | 6.369 | 20 | 20 | fits | 92,808 | 28 | 0.789 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 156,873 | 1.569 | 20 | 24 | fits | 149,145 | 161 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 310,735 | 3.107 | 20 | 24 | fits | 154,852 | 200 | 0.447 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 310,669 | 3.107 | 20 | 50 | fits | 154,852 | 200 | 0.447 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 536,870 | 5.369 | 20 | 50 | fits | 149,321 | 178 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 639,857 | 6.399 | 20 | 20 | fits | 92,808 | 28 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,081,283 | 10.813 | 20 | 20 | fits | 80,021 | 28 | 0.554 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 379,235 | 3.792 | 20 | 20 | fits | 148,404 | 161 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 308,431 | 3.084 | 20 | 200 | fits | 155,656 | 217 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 456,219 | 4.562 | 20 | 200 | fits | 148,404 | 161 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 309,355 | 3.094 | 20 | 20 | fits | 155,656 | 217 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 456,923 | 4.569 | 20 | 20 | fits | 148,404 | 161 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 157,339 | 1.573 | 20 | 24 | fits | 149,145 | 161 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 312,005 | 3.120 | 20 | 24 | fits | 155,656 | 217 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 311,939 | 3.119 | 20 | 50 | fits | 155,656 | 217 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 459,947 | 4.599 | 20 | 50 | fits | 148,404 | 161 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 550,963 | 5.510 | 20 | 20 | fits | 91,082 | 24 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 998,159 | 9.982 | 20 | 20 | fits | 69,055 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 380,550 | 3.805 | 20 | 20 | fits | 155,778 | 179 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 290,983 | 2.910 | 20 | 200 | fits | 148,004 | 200 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 446,145 | 4.461 | 20 | 200 | fits | 155,778 | 179 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 291,907 | 2.919 | 20 | 20 | fits | 148,004 | 200 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 446,849 | 4.468 | 20 | 20 | fits | 155,778 | 179 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 147,543 | 1.475 | 20 | 24 | fits | 149,145 | 161 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 294,557 | 2.946 | 20 | 24 | fits | 148,004 | 200 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 294,491 | 2.945 | 20 | 50 | fits | 148,004 | 200 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 449,873 | 4.499 | 20 | 50 | fits | 155,778 | 179 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 541,080 | 5.411 | 20 | 20 | fits | 91,273 | 25 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 992,394 | 9.924 | 20 | 20 | fits | 80,021 | 28 | 0.554 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 381,250 | 3.812 | 20 | 20 | fits | 148,242 | 162 | 0.435 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 309,689 | 3.097 | 20 | 200 | fits | 155,289 | 217 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 457,315 | 4.573 | 20 | 200 | fits | 148,242 | 162 | 0.435 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 310,613 | 3.106 | 20 | 20 | fits | 155,289 | 217 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 458,019 | 4.580 | 20 | 20 | fits | 148,242 | 162 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 158,964 | 1.590 | 20 | 24 | fits | 149,090 | 161 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 313,263 | 3.133 | 20 | 24 | fits | 155,289 | 217 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 313,197 | 3.132 | 20 | 50 | fits | 155,289 | 217 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 461,043 | 4.610 | 20 | 50 | fits | 148,242 | 162 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 566,231 | 5.662 | 20 | 20 | fits | 95,476 | 31 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 1,002,052 | 10.021 | 20 | 20 | fits | 80,021 | 28 | 0.554 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 384,642 | 3.846 | 20 | 20 | fits | 151,600 | 166 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 301,092 | 3.011 | 20 | 200 | fits | 155,532 | 218 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 461,739 | 4.617 | 20 | 200 | fits | 151,600 | 166 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 302,016 | 3.020 | 20 | 20 | fits | 155,532 | 218 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 462,443 | 4.624 | 20 | 20 | fits | 151,600 | 166 | 0.461 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 150,124 | 1.501 | 20 | 24 | fits | 149,090 | 161 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 304,666 | 3.047 | 20 | 24 | fits | 155,532 | 218 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 304,600 | 3.046 | 20 | 50 | fits | 155,532 | 218 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 465,467 | 4.655 | 20 | 50 | fits | 151,600 | 166 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 557,114 | 5.571 | 20 | 20 | fits | 91,713 | 24 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 992,896 | 9.929 | 20 | 20 | fits | 80,021 | 28 | 0.554 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 402,536 | 4.025 | 20 | 20 | fits | 155,845 | 179 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 312,903 | 3.129 | 20 | 200 | fits | 147,910 | 200 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 468,132 | 4.681 | 20 | 200 | fits | 155,845 | 179 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 313,827 | 3.138 | 20 | 20 | fits | 147,910 | 200 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 468,836 | 4.688 | 20 | 20 | fits | 155,845 | 179 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 160,857 | 1.609 | 20 | 24 | fits | 149,303 | 162 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 316,477 | 3.165 | 20 | 24 | fits | 147,910 | 200 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 316,411 | 3.164 | 20 | 50 | fits | 147,910 | 200 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 471,860 | 4.719 | 20 | 50 | fits | 155,845 | 179 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 557,815 | 5.578 | 20 | 20 | fits | 86,021 | 26 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 998,838 | 9.988 | 20 | 20 | fits | 80,179 | 29 | 0.556 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 403,629 | 4.036 | 20 | 20 | fits | 147,513 | 162 | 0.455 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 311,066 | 3.111 | 20 | 200 | fits | 154,979 | 218 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 457,963 | 4.580 | 20 | 200 | fits | 147,513 | 162 | 0.455 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 311,990 | 3.120 | 20 | 20 | fits | 154,979 | 218 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 549,755 | 5.498 | 20 | 20 | fits | 91,088 | 27 | 0.780 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 151,951 | 1.520 | 20 | 24 | fits | 149,237 | 162 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 314,640 | 3.146 | 20 | 24 | fits | 154,979 | 218 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 314,574 | 3.146 | 20 | 50 | fits | 154,979 | 218 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 461,691 | 4.617 | 20 | 50 | fits | 147,513 | 162 | 0.455 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 552,713 | 5.527 | 20 | 20 | fits | 91,088 | 27 | 0.780 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 998,158 | 9.982 | 20 | 20 | fits | 84,303 | 35 | 0.605 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 389,040 | 3.890 | 20 | 20 | fits | 156,649 | 166 | 0.457 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 308,521 | 3.085 | 20 | 200 | fits | 155,165 | 217 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 464,554 | 4.646 | 20 | 200 | fits | 156,649 | 166 | 0.457 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 309,445 | 3.094 | 20 | 20 | fits | 155,165 | 217 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 465,258 | 4.653 | 20 | 20 | fits | 156,649 | 166 | 0.457 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 157,920 | 1.579 | 20 | 24 | fits | 149,091 | 161 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 312,095 | 3.121 | 20 | 24 | fits | 155,165 | 217 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 312,029 | 3.120 | 20 | 50 | fits | 155,165 | 217 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 468,282 | 4.683 | 20 | 50 | fits | 156,649 | 166 | 0.457 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 559,033 | 5.590 | 20 | 20 | fits | 90,817 | 24 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 1,005,523 | 10.055 | 20 | 20 | fits | 69,055 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 380,382 | 3.804 | 20 | 20 | fits | 148,728 | 162 | 0.427 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 297,093 | 2.971 | 20 | 200 | fits | 152,577 | 211 | 0.442 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 445,205 | 4.452 | 20 | 200 | fits | 148,728 | 162 | 0.427 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 298,017 | 2.980 | 20 | 20 | fits | 152,577 | 211 | 0.442 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 537,064 | 5.371 | 20 | 20 | fits | 91,155 | 27 | 0.781 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 149,080 | 1.491 | 20 | 24 | fits | 149,091 | 161 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 300,667 | 3.007 | 20 | 24 | fits | 152,577 | 211 | 0.442 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 300,601 | 3.006 | 20 | 50 | fits | 152,577 | 211 | 0.442 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 448,933 | 4.489 | 20 | 50 | fits | 148,728 | 162 | 0.427 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 540,022 | 5.400 | 20 | 20 | fits | 91,155 | 27 | 0.781 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 997,757 | 9.978 | 20 | 20 | fits | 80,021 | 28 | 0.554 |
| LINK_UP | `adp.link_up.if0` | 3,364 | 0.034 | 20 | 200 | fits | 33,145 | 43 (11) | 0.724 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 14,307 | 0.143 | 20 | 200 | fits | 27,119 | 23 (39) | 0.742 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 4,454 | 0.045 | 20 | 200 | fits | 3,261 | 10 (11) | 0.586 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 21,568 | 0.216 | 20 | 20 | fits | 34,967 | 21 (35) | 0.806 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 21,409 | 0.214 | 20 | 20 | fits | 30,991 | 17 (14) | 0.847 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 24,492 | 0.245 | 20 | 20 | fits | 31,141 | 18 (14) | 0.836 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 16,223 | 0.162 | 20 | 20 | fits | 35,490 | 21 (35) | 0.812 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 150,163 | 1.502 | 20 | 20 | fits | 28,896 | 8 | 0.821 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 54,248 | 0.542 | 20 | 20 | fits | 54,314 | 12 | 0.877 |
| malformed MRPDU discard | `srp.malformed.if0` | 25,497 | 0.255 | 20 | 20 | fits | 25,563 | 12 | 0.658 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 173,644 | 1.736 | 220 | 220 | fits | 140,524 | 7 | 0.820 |
| an event behind 15 others | `backlog.event.if0` | 170,254 | 1.703 | 20 | 200 | fits | 56,034 | 78 | 0.554 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 502,854 | 5.029 | 20 | 20 | fits | 81,815 | 90 | 0.313 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 466,995 | 4.670 | 20 | 200 | fits | 153,450 | 122 | 0.389 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 466,379 | 4.664 | 20 | 200 | fits | 153,450 | 122 | 0.389 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 462,673 | 4.627 | 20 | 20 | fits | 153,450 | 122 | 0.389 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 543,652 | 5.437 | 20 | 20 | fits | 81,815 | 90 | 0.313 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 157,439 | 1.574 | 20 | 24 | fits | 158,330 | 167 | 0.389 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 311,873 | 3.119 | 20 | 24 | fits | 99,390 | 26 | 0.697 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 465,257 | 4.653 | 20 | 50 | fits | 153,450 | 122 | 0.389 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 464,861 | 4.649 | 20 | 50 | fits | 153,450 | 122 | 0.389 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 546,610 | 5.466 | 20 | 20 | fits | 81,815 | 90 | 0.313 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 617,398 | 6.174 | 20 | 20 | fits | 30,995 | 41 | 0.167 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 395,861 | 3.959 | 20 | 20 | fits | 152,802 | 170 | 0.454 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 299,684 | 2.997 | 20 | 200 | fits | 153,891 | 214 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 461,385 | 4.614 | 20 | 200 | fits | 152,802 | 170 | 0.454 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 300,608 | 3.006 | 20 | 20 | fits | 153,891 | 214 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 462,089 | 4.621 | 20 | 20 | fits | 152,802 | 170 | 0.454 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 150,357 | 1.504 | 20 | 24 | fits | 150,543 | 164 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 303,258 | 3.033 | 20 | 24 | fits | 153,891 | 214 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 303,192 | 3.032 | 20 | 50 | fits | 153,891 | 214 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 465,113 | 4.651 | 20 | 50 | fits | 152,802 | 170 | 0.454 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 561,258 | 5.613 | 20 | 20 | fits | 96,211 | 30 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 991,082 | 9.911 | 20 | 20 | fits | 69,050 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 21,756 | 0.218 | 20 | 20 | fits | 33,965 | 19 | 0.799 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 299,684 | 2.997 | 20 | 200 | fits | 153,891 | 214 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 44,875 | 0.449 | 20 | 200 | fits | 33,965 | 19 | 0.799 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 300,608 | 3.006 | 20 | 20 | fits | 153,891 | 214 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 450,643 | 4.506 | 20 | 20 | fits | 141,356 | 163 | 0.417 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 150,357 | 1.504 | 20 | 24 | fits | 150,543 | 164 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 303,258 | 3.033 | 20 | 24 | fits | 153,891 | 214 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 303,192 | 3.032 | 20 | 50 | fits | 153,891 | 214 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 453,667 | 4.537 | 20 | 50 | fits | 141,356 | 163 | 0.417 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 549,138 | 5.491 | 20 | 20 | fits | 95,537 | 30 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 978,962 | 9.790 | 20 | 20 | fits | 69,050 | 24 | 0.600 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,341,457 | 63.415 | 20 | 20 | MISS ceiling | 28,876 | 18 | 0.735 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,364,950 | 63.650 | 20 | 20 | MISS ceiling | 25,332 | 13 | 0.626 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,390,067 | 63.901 | 20 | 20 | MISS ceiling | 24,753 | 13 | 0.667 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,414,614 | 64.146 | 20 | 20 | MISS ceiling | 24,595 | 13 | 0.671 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,439,145 | 64.391 | 20 | 20 | MISS ceiling | 24,528 | 13 | 0.667 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 161,574 | 1.616 | 20 | 200 | fits | 156,011 | 200 | 0.444 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 291,134 | 2.911 | 20 | 200 | fits | 130,176 | 185 | 0.368 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 157,252 | 1.573 | 20 | 20 | fits | 156,011 | 200 | 0.444 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,219,793 | 62.198 | 20 | 20 | MISS ceiling | 39,015 | 15 | 0.758 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 160,892 | 1.609 | 20 | 24 | fits | 156,011 | 200 | 0.444 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,184,264 | 61.843 | 20 | 24 | MISS ceiling | 141,486 | 106 | 0.452 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 159,836 | 1.598 | 20 | 50 | fits | 156,011 | 200 | 0.444 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 289,616 | 2.896 | 20 | 50 | fits | 130,176 | 185 | 0.368 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 380,629 | 3.806 | 20 | 20 | fits | 91,079 | 24 | 0.766 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 818,470 | 8.185 | 20 | 20 | fits | 80,397 | 28 | 0.556 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 7,965 | 0.080 | 20 | 20 | fits | 29,197 | 14 (29) | 0.763 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 9,813 | 0.098 | 20 | 20 | fits | 32,610 | 19 (35) | 0.781 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 19,511 | 0.195 | 20 | 20 | fits | 35,014 | 21 (12) | 0.806 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 13,952 | 0.140 | 20 | 50 | fits | 33,145 | 43 | 0.724 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 25,697 | 0.257 | 20 | 50 | fits | 29,630 | 35 | 0.707 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 14,826 | 0.148 | 20 | 50 | fits | 29,665 | 35 | 0.709 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 25,742 | 0.257 | 20 | 50 | fits | 35,119 | 61 | 0.649 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 27,813 | 0.278 | 20 | 50 | fits | 35,119 | 61 | 0.649 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 12,708 | 0.127 | 20 | 50 | fits | 27,992 | 30 | 0.636 |
| LINK_UP | `adp.link_up.if0` | 3,364 | 0.034 | 20 | 200 | fits | 33,145 | 43 (11) | 0.724 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 14,307 | 0.143 | 20 | 200 | fits | 27,119 | 23 (39) | 0.742 |
| LINK_DOWN | `adp.link_down.if0` | 2,981 | 0.030 | 20 | 200 | fits | 36,787 | 23 (9) | 0.775 |
| LINK_UP | `adp.link_up.if0` | 3,364 | 0.034 | 20 | 200 | fits | 33,145 | 43 (11) | 0.724 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 14,307 | 0.143 | 20 | 200 | fits | 27,119 | 23 (39) | 0.742 |
| GM_CHANGE | `adp.gm_change.if0` | 3,037 | 0.030 | 20 | 200 | fits | 20,825 | 17 (11) | 0.696 |
| LINK_UP | `adp.link_up.if0` | 3,364 | 0.034 | 20 | 200 | fits | 33,145 | 43 (11) | 0.724 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 14,307 | 0.143 | 20 | 200 | fits | 27,119 | 23 (39) | 0.742 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 5,796 | 0.058 | 20 | 200 | fits | 21,788 | 16 (31) | 0.651 |
| LINK_UP | `adp.link_up.if0` | 3,364 | 0.034 | 20 | 200 | fits | 33,145 | 43 (11) | 0.724 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 14,307 | 0.143 | 20 | 200 | fits | 27,119 | 23 (39) | 0.742 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 5,796 | 0.058 | 20 | 200 | fits | 21,788 | 16 (31) | 0.651 |
| set_name | `aecp_fanout.set_name.if0` | 49,333 | 0.493 | 20 | 24 | fits | 65,581 | 88 | 0.583 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 45,799 | 0.458 | 20 | 24 | fits | 55,385 | 77 | 0.609 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 56,513 | 0.565 | 20 | 24 | fits | 49,332 | 78 | 0.556 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 49,293 | 0.493 | 20 | 24 | fits | 50,065 | 77 | 0.560 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 39,867 | 0.399 | 20 | 24 | fits | 52,060 | 67 | 0.587 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 56,385 | 0.564 | 20 | 24 | fits | 49,602 | 77 | 0.562 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 40,918 | 0.409 | 20 | 24 | fits | 48,077 | 78 | 0.536 |
| BIND_RX | `acmp.bind_rx.if0` | 20,766 | 0.208 | 20 | 20 | fits | 47,569 | 26 (77) | 0.796 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 11,314 | 0.113 | 20 | 20 | fits | 35,557 | 19 (32) | 0.827 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 12,355 | 0.124 | 20 | 20 | fits | 30,880 | 16 (47) | 0.765 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 16,928 | 0.169 | 20 | 20 | fits | 46,242 | 18 (50) | 0.848 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 12,295 | 0.123 | 20 | 20 | fits | 30,982 | 17 (48) | 0.750 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 10,456 | 0.105 | 20 | 20 | fits | 29,715 | 16 (48) | 0.721 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 11,490 | 0.115 | 20 | 20 | fits | 30,473 | 16 (48) | 0.758 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 11,091 | 0.111 | 20 | 20 | fits | 29,142 | 16 (48) | 0.717 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 26,975 | 0.270 | 20 | 24 | fits | 30,702 | 20 | 0.794 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 18,577 | 0.186 | 20 | 24 | fits | 33,753 | 20 | 0.710 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 14,625 | 0.146 | 20 | 24 | fits | 30,191 | 20 | 0.735 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 9,749 | 0.097 | 20 | 24 | fits | 29,408 | 20 | 0.732 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 16,850 | 0.169 | 20 | 24 | fits | 30,042 | 20 | 0.732 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 15,455 | 0.155 | 20 | 24 | fits | 31,059 | 20 | 0.729 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 15,207 | 0.152 | 20 | 24 | fits | 30,161 | 20 | 0.737 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 14,181 | 0.142 | 20 | 24 | fits | 29,566 | 20 | 0.741 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 10,310 | 0.103 | 20 | 24 | fits | 30,144 | 20 | 0.756 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 21,362 | 0.214 | 20 | 24 | fits | 34,482 | 21 | 0.658 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 14,046 | 0.140 | 20 | 24 | fits | 29,681 | 20 | 0.766 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 15,099 | 0.151 | 20 | 24 | fits | 29,529 | 20 | 0.774 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 14,076 | 0.141 | 20 | 24 | fits | 29,670 | 20 | 0.731 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 10,704 | 0.107 | 20 | 24 | fits | 30,655 | 20 | 0.743 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 17,042 | 0.170 | 20 | 24 | fits | 30,179 | 20 | 0.743 |
| get_configuration | `aecp.get_configuration.if0` | 12,538 | 0.125 | 20 | 24 | fits | 27,579 | 20 | 0.750 |
| entity_available | `aecp.entity_available.if0` | 13,672 | 0.137 | 20 | 24 | fits | 27,665 | 20 | 0.752 |
| get_name | `aecp.get_name.if0` | 14,571 | 0.146 | 20 | 24 | fits | 30,305 | 20 | 0.766 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 11,206 | 0.112 | 20 | 24 | fits | 31,312 | 27 | 0.732 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 18,581 | 0.186 | 20 | 24 | fits | 31,687 | 29 | 0.768 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 12,947 | 0.129 | 20 | 24 | fits | 28,333 | 20 | 0.774 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 13,018 | 0.130 | 20 | 24 | fits | 27,360 | 20 | 0.753 |
| set_name | `aecp.set_name.if0` | 26,627 | 0.266 | 20 | 24 | fits | 53,609 | 42 | 0.771 |
| lock_entity | `aecp.lock_entity.if0` | 13,601 | 0.136 | 20 | 24 | fits | 37,578 | 33 | 0.783 |
| unlock_entity | `aecp.unlock_entity.if0` | 17,490 | 0.175 | 20 | 24 | fits | 36,509 | 32 | 0.777 |
| LINK_UP | `fixture.link_up.if0` | 3,364 | 0.034 | 20 | 200 | fits | 33,145 | 43 (11) | 0.724 |
| malformed MRPDU discard | `fixture.malformed.if0` | 26,051 | 0.261 | 20 | 20 | fits | 26,117 | 12 | 0.722 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 39,303 | 0.393 | 20 | 24 | fits | 54,478 | 42 | 0.783 |
| LINK_DOWN | `fixture.link_down.if0` | 3,342 | 0.033 | 20 | 200 | fits | 38,525 | 23 (9) | 0.797 |
| BIND_RX | `fixture.bind_rx.if0` | 22,227 | 0.222 | 20 | 20 | fits | 48,116 | 26 (77) | 0.805 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 28,017 | 0.280 | 20 | 20 | fits | 46,443 | 35 (35) | 0.775 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 21,947 | 0.219 | 20 | 20 | fits | 30,427 | 13 (29) | 0.795 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 95,202 | 0.952 | 20 | 200 | fits | 95,306 | 51 | 0.752 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 95,202 | 0.952 | 20 | 200 | fits | 95,306 | 51 | 0.752 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 94,928 | 0.949 | 20 | 20 | fits | 95,306 | 51 | 0.752 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 94,928 | 0.949 | 20 | 20 | fits | 95,306 | 51 | 0.752 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 95,136 | 0.951 | 20 | 24 | fits | 95,306 | 51 | 0.752 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 95,136 | 0.951 | 20 | 24 | fits | 95,306 | 51 | 0.752 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 95,070 | 0.951 | 20 | 50 | fits | 95,306 | 51 | 0.752 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 95,070 | 0.951 | 20 | 50 | fits | 95,306 | 51 | 0.752 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 95,004 | 0.950 | 20 | 20 | fits | 95,306 | 51 | 0.752 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 95,004 | 0.950 | 20 | 20 | fits | 95,306 | 51 | 0.752 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
