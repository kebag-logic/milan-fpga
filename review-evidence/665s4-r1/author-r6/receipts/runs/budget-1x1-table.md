### 1x1

13 of 81 paths and 34 of 141 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.985 (2.484) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 9.367 (14.224) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 8.328 (14.012) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 15.183 (30.787) | MISS T_svc | 0 adp | 2 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 9.599 (16.024) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 9.366 (14.225) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 9.403 (14.252) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 8.084 (14.361) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 12.453 (15.866) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 1.178 (12.107) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 1.917 (27.220) | fits | 2 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 1.454 (14.284) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.176 (13.549) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.455 (12.054) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 3.921 (28.628) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 9.556 (16.322) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.224 (1.139) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.077 (1.017) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.065 (3.072) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.077 (3.232) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.699 (1.627) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.476 (2.353) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.139 (2.914) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 2.160 (2.936) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.102 (2.877) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 2.701 (3.476) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 2.259 (3.035) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 2.266 (3.224) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 1.729 (2.505) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 2.795 (3.570) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 2.341 (3.117) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 2.615 (3.390) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.282 (3.058) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.104 (3.880) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 2.172 (2.948) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 2.480 (3.256) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 2.435 (3.210) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 2.360 (3.135) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 2.407 (3.183) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.647 (3.423) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 2.736 (3.512) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 2.434 (3.210) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 2.340 (3.116) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.412 (2.181) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 2.754 (4.132) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.097 (2.873) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 2.574 (3.532) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 4.727 (5.535) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 4.607 (5.388) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 4.731 (5.540) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 4.534 (5.148) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 4.375 (5.156) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 6.346 (7.466) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 4.378 (4.972) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 4.614 (5.395) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 37.156 (41.251) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 41.767 (53.053) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 38.270 (54.983) | MISS ceiling | 4 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 9.299 (17.300) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 94.558 (96.315) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 362.497 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 2.982 (4.146) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 1.351 (3.253) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.458 (1.354) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.530 (3.232) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 1.202 (3.253) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 1.168 (3.046) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp.service.acmp.first.if0` (backlog-adp) | 8.844 | fits | 0 acmp | 5 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 85.434 | MISS ceiling | 11 acmp | 5 | 4 |
| ADP record released under the composed load, first | 0 | `backlog-adp.service.adp.first.if0` (backlog-adp) | 8.835 | fits | 0 adp | 5 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 49.392 | MISS T_svc | 7 adp | 5 | 4 |
| AECP record released under the composed load, first | 0 | `backlog-adp.service.aecp.first.if0` (backlog-adp) | 8.880 | fits | 0 aecp | 5 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp-refill.service.aecp.last.if0` (backlog-adp-refill) | 253.443 | MISS ceiling | 15 aecp | 5 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog-adp.service.maap.first.if0` (backlog-adp) | 8.869 | fits | 0 maap | 5 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 49.428 | MISS T_svc | 6 maap | 5 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 578.255 | STARVED: never released | 0 srp | 5 | 4 |
| SRP record released under the composed load, last | 0 | `backlog-adp-refill.service.srp.last.if0` (backlog-adp-refill) | at least 578.235 | STARVED: never released | 31 srp | 5 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 3.250 (4.650) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 1.907 (1.908) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 1.576 (1.577) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 2.857 (3.232) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 90.069 | 22 | 438,881 (8.778) | yes | - |
| backlog-adp | 541.820 | 36 | 947,356 (18.947) | no | {'srp': 32} |
| backlog-adp-refill | 578.272 | 38 | 926,253 (18.525) | no | {'srp': 32} |
| backlog-owed | 362.547 | 54 | 431,056 (8.621) | yes | - |
| fixture | 10.039 | 3 | 245,725 (4.915) | yes | - |

Composed maximum over the 4 backlog windows: at least 947,356 CPU cycles (18.947 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 438,881 (8.778 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 22,745 | 0.455 | 10 | 20 | fits | 602,679 | 109 (14) | 0.039 |
| LINK_UP | `adp.link_up.if0` | 3,858 | 0.077 | 10 | 200 | fits | 161,590 | 88 (11) | 0.088 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 23,797 | 0.476 | 10 | 200 | fits | 66,487 | 46 (39) | 0.086 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 34,941 | 0.699 | 10 | 200 | fits | 3,884 | 9 (11) | 0.160 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 23,239 | 0.465 | 10 | 20 | fits | 690,945 | 140 (35) | 0.034 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 8,779 | 0.176 | 10 | 20 | fits | 677,447 | 117 (14) | 0.033 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 196,031 | 3.921 | 10 | 20 | fits | 674,436 | 118 (14) | 0.033 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 58,920 | 1.178 | 10 | 20 | fits | 605,327 | 130 (35) | 0.038 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 142,869 | 2.857 | 10 | 18 | fits | 161,590 | 88 | 0.088 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 95,371 | 1.907 | 10 | 18 | fits | 95,403 | 29 | 0.111 |
| malformed MRPDU discard | `srp.malformed.if0` | 78,800 | 1.576 | 10 | 18 | fits | 78,832 | 35 | 0.111 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 162,517 | 3.250 | 210 | 218 | fits | 232,512 | 78 | 0.088 |
| an event behind 15 others | `backlog.event.if0` | 464,944 | 9.299 | 10 | 200 | fits | 426,113 | 356 | 0.071 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 1,857,817 | 37.156 | 10 | 20 | MISS ceiling | 286,370 | 256 | 0.063 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 438,777 | 8.776 | 10 | 200 | fits | 438,881 | 389 | 0.069 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 1,518,057 | 30.361 | 10 | 200 | MISS T_svc | 314,223 | 324 | 0.069 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 436,648 | 8.733 | 10 | 20 | fits | 438,881 | 389 | 0.069 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 2,059,921 | 41.198 | 10 | 20 | MISS ceiling | 286,370 | 256 | 0.063 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 438,440 | 8.769 | 10 | 24 | fits | 438,881 | 389 | 0.069 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 4,007,792 | 80.156 | 10 | 24 | MISS ceiling | 207,307 | 169 | 0.058 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 437,920 | 8.758 | 10 | 50 | fits | 438,881 | 389 | 0.069 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 1,517,309 | 30.346 | 10 | 50 | MISS T_svc | 314,223 | 324 | 0.069 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 1,203,054 | 24.061 | 10 | 18 | MISS ceiling | 339,248 | 348 | 0.073 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 4,366,340 | 87.327 | 10 | 18 | MISS ceiling | 51,720 | 29 | 0.097 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 2,088,370 | 41.767 | 10 | 20 | MISS ceiling | 947,356 | 411 | 0.041 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 441,731 | 8.835 | 10 | 200 | fits | 624,479 | 412 | 0.048 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,469,584 | 49.392 | 10 | 200 | MISS T_svc | 947,356 | 411 | 0.041 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 442,187 | 8.844 | 10 | 20 | fits | 624,479 | 412 | 0.048 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 4,245,786 | 84.916 | 10 | 20 | MISS ceiling | 887,986 | 317 | 0.037 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 443,979 | 8.880 | 10 | 24 | fits | 624,479 | 412 | 0.048 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 12,646,174 | 252.923 | 10 | 24 | MISS ceiling | 804,006 | 230 | 0.033 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 443,459 | 8.869 | 10 | 50 | fits | 624,479 | 412 | 0.048 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,471,422 | 49.428 | 10 | 50 | MISS T_svc | 947,356 | 411 | 0.041 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 27,090,175 | 541.803 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 27,089,168 | 541.783 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 1,913,477 | 38.270 | 10 | 20 | MISS ceiling | 917,685 | 349 | 0.039 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 441,731 | 8.835 | 10 | 200 | fits | 624,479 | 412 | 0.048 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 2,273,918 | 45.478 | 10 | 200 | MISS T_svc | 917,685 | 349 | 0.039 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 442,187 | 8.844 | 10 | 20 | fits | 624,479 | 412 | 0.048 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 4,271,724 | 85.434 | 10 | 20 | MISS ceiling | 917,685 | 349 | 0.039 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 443,979 | 8.880 | 10 | 24 | fits | 624,479 | 412 | 0.048 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 12,672,131 | 253.443 | 10 | 24 | MISS ceiling | 804,060 | 230 | 0.033 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 443,459 | 8.869 | 10 | 50 | fits | 624,479 | 412 | 0.048 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,450,319 | 49.006 | 10 | 50 | MISS T_svc | 926,253 | 404 | 0.041 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 28,912,740 | 578.255 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 28,911,733 | 578.235 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 4,727,902 | 94.558 | 10 | 20 | MISS ceiling | 199,387 | 147 | 0.048 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,124,832 | 362.497 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,124,794 | 362.496 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,124,757 | 362.495 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,124,719 | 362.494 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 337,151 | 6.743 | 10 | 200 | fits | 336,884 | 341 | 0.070 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 1,385,450 | 27.709 | 10 | 200 | MISS T_svc | 306,980 | 261 | 0.066 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 335,022 | 6.700 | 10 | 20 | fits | 336,884 | 341 | 0.070 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 1,867,249 | 37.345 | 10 | 20 | MISS ceiling | 178,562 | 75 | 0.063 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 336,814 | 6.736 | 10 | 24 | fits | 336,884 | 341 | 0.070 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 5,376,468 | 107.529 | 10 | 24 | MISS ceiling | 181,458 | 125 | 0.046 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 336,294 | 6.726 | 10 | 50 | fits | 336,884 | 341 | 0.070 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 1,384,702 | 27.694 | 10 | 50 | MISS T_svc | 306,980 | 261 | 0.066 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 767,123 | 15.342 | 10 | 18 | MISS T_svc | 431,056 | 378 | 0.083 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 4,199,204 | 83.984 | 10 | 18 | MISS ceiling | 284,899 | 191 | 0.074 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 316,238 | 6.325 | 10 | 20 | fits | 698,749 | 140 (29) | 0.036 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 416,409 | 8.328 | 10 | 20 | fits | 700,602 | 146 (35) | 0.036 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 95,841 | 1.917 | 10 | 20 | fits | 604,060 | 130 (12) | 0.038 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 26,514 | 0.530 | 10 | 50 | fits | 161,590 | 88 | 0.088 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 58,416 | 1.168 | 10 | 50 | fits | 83,542 | 43 | 0.101 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 34,645 | 0.693 | 10 | 50 | fits | 68,538 | 37 | 0.096 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 60,103 | 1.202 | 10 | 50 | fits | 85,758 | 64 | 0.084 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 67,562 | 1.351 | 10 | 50 | fits | 85,758 | 64 | 0.084 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 22,890 | 0.458 | 10 | 50 | fits | 67,702 | 47 | 0.095 |
| LINK_UP | `adp.link_up.if0` | 3,858 | 0.077 | 10 | 200 | fits | 161,590 | 88 (11) | 0.088 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 23,797 | 0.476 | 10 | 200 | fits | 66,487 | 46 (39) | 0.086 |
| LINK_DOWN | `adp.link_down.if0` | 3,240 | 0.065 | 10 | 200 | fits | 153,583 | 27 (9) | 0.081 |
| LINK_UP | `adp.link_up.if0` | 3,858 | 0.077 | 10 | 200 | fits | 161,590 | 88 (11) | 0.088 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 23,797 | 0.476 | 10 | 200 | fits | 66,487 | 46 (39) | 0.086 |
| GM_CHANGE | `adp.gm_change.if0` | 3,827 | 0.077 | 10 | 200 | fits | 50,857 | 18 (11) | 0.095 |
| LINK_UP | `adp.link_up.if0` | 3,858 | 0.077 | 10 | 200 | fits | 161,590 | 88 (11) | 0.088 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 23,797 | 0.476 | 10 | 200 | fits | 66,487 | 46 (39) | 0.086 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 11,209 | 0.224 | 10 | 200 | fits | 56,942 | 38 (31) | 0.102 |
| LINK_UP | `adp.link_up.if0` | 3,858 | 0.077 | 10 | 200 | fits | 161,590 | 88 (11) | 0.088 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 23,797 | 0.476 | 10 | 200 | fits | 66,487 | 46 (39) | 0.086 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 11,209 | 0.224 | 10 | 200 | fits | 56,942 | 38 (31) | 0.102 |
| set_name | `aecp_fanout.set_name.if0` | 317,301 | 6.346 | 10 | 24 | fits | 373,314 | 622 | 0.034 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 226,705 | 4.534 | 10 | 24 | fits | 257,410 | 329 | 0.042 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 218,348 | 4.367 | 10 | 24 | fits | 257,336 | 312 | 0.039 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 218,728 | 4.375 | 10 | 24 | fits | 257,777 | 312 | 0.039 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 236,537 | 4.731 | 10 | 24 | fits | 277,005 | 352 | 0.038 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 236,362 | 4.727 | 10 | 24 | fits | 276,749 | 352 | 0.038 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 218,892 | 4.378 | 10 | 24 | fits | 248,588 | 318 | 0.040 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 230,375 | 4.607 | 10 | 24 | fits | 269,385 | 363 | 0.037 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 230,710 | 4.614 | 10 | 24 | fits | 269,759 | 363 | 0.037 |
| BIND_RX | `acmp.bind_rx.if0` | 49,239 | 0.985 | 10 | 20 | fits | 124,180 | 83 (77) | 0.086 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 622,669 | 12.453 | 10 | 20 | MISS T_svc | 793,311 | 153 (32) | 0.034 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 479,930 | 9.599 | 10 | 20 | fits | 801,176 | 168 (47) | 0.033 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 477,782 | 9.556 | 10 | 20 | fits | 816,109 | 171 (50) | 0.035 |
| PROBE_TX | `acmp.probe_tx.if0` | 404,221 | 8.084 | 10 | 20 | fits | 718,071 | 191 (48) | 0.036 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 470,155 | 9.403 | 10 | 20 | fits | 712,591 | 159 (48) | 0.036 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 468,367 | 9.367 | 10 | 20 | fits | 711,193 | 159 (48) | 0.036 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 468,294 | 9.366 | 10 | 20 | fits | 711,260 | 159 (48) | 0.036 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 70,601 | 1.412 | 10 | 24 | fits | 109,056 | 48 | 0.072 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 139,725 | 2.795 | 10 | 24 | fits | 178,507 | 125 | 0.047 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 117,066 | 2.341 | 10 | 24 | fits | 155,845 | 74 | 0.053 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 121,736 | 2.435 | 10 | 24 | fits | 160,515 | 85 | 0.051 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 136,794 | 2.736 | 10 | 24 | fits | 175,576 | 90 | 0.058 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 121,715 | 2.434 | 10 | 24 | fits | 160,497 | 84 | 0.051 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 117,018 | 2.340 | 10 | 24 | fits | 155,800 | 73 | 0.053 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 130,727 | 2.615 | 10 | 24 | fits | 169,509 | 75 | 0.060 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 114,104 | 2.282 | 10 | 24 | fits | 152,883 | 66 | 0.054 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 155,208 | 3.104 | 10 | 24 | fits | 193,987 | 161 | 0.043 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 108,616 | 2.172 | 10 | 24 | fits | 147,395 | 53 | 0.055 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 124,008 | 2.480 | 10 | 24 | fits | 162,787 | 59 | 0.062 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 117,986 | 2.360 | 10 | 24 | fits | 156,765 | 70 | 0.052 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 120,353 | 2.407 | 10 | 24 | fits | 159,132 | 76 | 0.052 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 132,347 | 2.647 | 10 | 24 | fits | 171,126 | 74 | 0.060 |
| get_configuration | `aecp.get_configuration.if0` | 105,089 | 2.102 | 10 | 24 | fits | 143,868 | 48 | 0.056 |
| entity_available | `aecp.entity_available.if0` | 106,939 | 2.139 | 10 | 24 | fits | 145,721 | 52 | 0.056 |
| get_name | `aecp.get_name.if0` | 112,962 | 2.259 | 10 | 24 | fits | 151,744 | 65 | 0.055 |
| get_counters | `aecp.get_counters.if0` | 135,038 | 2.701 | 10 | 24 | fits | 173,820 | 92 | 0.062 |
| get_avb_info | `aecp.get_avb_info.if0` | 107,998 | 2.160 | 10 | 24 | fits | 146,780 | 48 | 0.056 |
| unknown_command | `aecp.unknown_command.if0` | 104,862 | 2.097 | 10 | 24 | fits | 143,644 | 48 | 0.056 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 86,461 | 1.729 | 10 | 24 | fits | 125,243 | 58 | 0.079 |
| set_name | `aecp.set_name.if0` | 137,715 | 2.754 | 10 | 24 | fits | 206,618 | 128 | 0.055 |
| lock_entity | `aecp.lock_entity.if0` | 113,288 | 2.266 | 10 | 24 | fits | 161,214 | 78 | 0.057 |
| unlock_entity | `aecp.unlock_entity.if0` | 128,716 | 2.574 | 10 | 24 | fits | 176,620 | 84 | 0.064 |
| LINK_UP | `fixture.link_up.if0` | 3,858 | 0.077 | 10 | 200 | fits | 161,590 | 88 (11) | 0.088 |
| malformed MRPDU discard | `fixture.malformed.if0` | 58,855 | 1.177 | 10 | 18 | fits | 58,887 | 29 | 0.109 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 149,098 | 2.982 | 10 | 24 | fits | 207,302 | 127 | 0.055 |
| LINK_DOWN | `fixture.link_down.if0` | 3,240 | 0.065 | 10 | 200 | fits | 155,721 | 27 (9) | 0.080 |
| BIND_RX | `fixture.bind_rx.if0` | 49,199 | 0.984 | 10 | 20 | fits | 114,294 | 83 (77) | 0.084 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 72,722 | 1.454 | 10 | 20 | fits | 714,217 | 169 (35) | 0.036 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 759,128 | 15.183 | 10 | 20 | MISS T_svc | 783,886 | 150 (29) | 0.032 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 245,674 | 4.913 | 10 | 200 | fits | 245,725 | 225 | 0.064 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 245,674 | 4.913 | 10 | 200 | fits | 245,725 | 225 | 0.064 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 245,539 | 4.911 | 10 | 20 | fits | 245,725 | 225 | 0.064 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 245,539 | 4.911 | 10 | 20 | fits | 245,725 | 225 | 0.064 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 245,641 | 4.913 | 10 | 24 | fits | 245,725 | 225 | 0.064 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 245,641 | 4.913 | 10 | 24 | fits | 245,725 | 225 | 0.064 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 245,609 | 4.912 | 10 | 50 | fits | 245,725 | 225 | 0.064 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 245,609 | 4.912 | 10 | 50 | fits | 245,725 | 225 | 0.064 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 359,140 | 7.183 | 10 | 18 | fits | 113,564 | 37 | 0.114 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 359,140 | 7.183 | 10 | 18 | fits | 113,564 | 37 | 0.114 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-owed`: wait tx TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
