### 1x1

69 of 76 paths and 104 of 116 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 32.725 (67.337) | MISS ceiling | 0 acmp | 2 | 2 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 38.276 (115.939) | MISS ceiling | 0 acmp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 24.084 (54.150) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 50.386 (91.007) | MISS ceiling | 0 adp | 2 | 2 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 4.658 (57.574) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 10.505 (58.364) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 11.470 (34.281) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 18.743 (94.225) | MISS T_svc | 2 events | 1 | 1 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 20.977 (96.586) | MISS ceiling | 1 events | 1 | 1 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 19.108 (100.888) | MISS T_svc | 4 events | 2 | 2 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 30.549 (106.391) | MISS ceiling | 2 events | 1 | 1 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 22.559 (79.250) | MISS ceiling | 3 events | 1 | 1 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 19.741 (92.152) | MISS T_svc | 3 events | 1 | 1 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 12.192 (72.676) | MISS T_svc | 0 acmp | 1 | 1 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 14.751 (32.949) | MISS T_svc | 0 adp | 2 | 2 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 8.312 (30.967) | fits | 1 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 40.619 (127.059) | MISS T_svc | 0 events | 2 | 2 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 35.969 (108.394) | MISS T_svc | 1 events | 6 | 6 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 5.065 (21.557) | fits | 1 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 7.783 (33.584) | fits | 1 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 26.899 (46.899) | MISS ceiling | 0 aecp | 1 | 1 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 27.065 (47.065) | MISS ceiling | 0 aecp | 1 | 1 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 23.216 (43.216) | MISS T_svc | 0 aecp | 1 | 1 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 28.149 (48.150) | MISS ceiling | 0 aecp | 1 | 1 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 23.629 (43.630) | MISS T_svc | 0 aecp | 1 | 1 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 18.346 (37.609) | MISS T_svc | 0 aecp | 1 | 1 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 25.712 (45.713) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 24.153 (44.374) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 27.447 (47.448) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 27.305 (47.305) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 23.589 (43.590) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 50.014 (70.014) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 27.205 (47.191) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 31.894 (51.894) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 23.756 (43.757) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 27.378 (47.378) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 23.814 (43.815) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 27.369 (47.370) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 18.509 (38.291) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 23.537 (43.757) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 27.346 (47.346) | MISS ceiling | 0 aecp | 1 | 1 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 21.090 (46.095) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 27.696 (51.430) | MISS ceiling | 0 aecp | 1 | 1 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 22.998 (42.999) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 28.271 (47.429) | MISS ceiling | 0 aecp | 1 | 1 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 34.731 (54.739) | MISS ceiling | 0 aecp | 1 | 1 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 47.230 (66.730) | MISS ceiling | 0 aecp | 1 | 1 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 37.456 (58.181) | MISS ceiling | 0 aecp | 1 | 1 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 40.452 (58.328) | MISS ceiling | 0 aecp | 1 | 1 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 37.035 (57.305) | MISS ceiling | 0 aecp | 2 | 2 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 45.271 (67.695) | MISS ceiling | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 37.058 (56.836) | MISS ceiling | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 32.643 (52.636) | MISS ceiling | 0 aecp | 1 | 1 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 383.568 (418.857) | MISS ceiling | 11 acmp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 124.444 (225.592) | MISS T_svc | 16 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 522.118 (536.296) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 666.377 (680.558) | MISS ceiling | 11 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 13.299 (40.173) | MISS T_svc | 1 events | 1 | 1 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 7.554 (17.534) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 40.452 (108.394) | MISS T_svc | 1 events | 1 | 1 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 12.803 (40.173) | MISS T_svc | 1 events | 1 | 1 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 7.986 (20.884) | fits | 1 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 70.580 | MISS ceiling | 0 acmp | 3 | 3 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 403.610 | MISS ceiling | 11 acmp | 3 | 3 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 70.622 | MISS T_svc | 0 adp | 3 | 3 |
| ADP record released under the composed load, last | 0 | `backlog.service.adp.last.if0` (backlog) | 280.141 | MISS ceiling | 7 adp | 3 | 3 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 70.616 | MISS ceiling | 0 aecp | 3 | 3 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 769.239 | MISS ceiling | 15 aecp | 3 | 3 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 70.605 | MISS ceiling | 0 maap | 3 | 3 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 280.126 | MISS ceiling | 6 maap | 3 | 3 |
| SRP record released under the composed load, first | 0 | `backlog-owed.service.srp.first.if0` (backlog-owed) | 803.889 | MISS ceiling | 0 srp | 3 | 3 |
| SRP record released under the composed load, last | 0 | `backlog-owed.service.srp.last.if0` (backlog-owed) | at least 860.009 | STARVED: never released | 31 srp | 3 | 3 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 48.644 (64.443) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 32.846 (43.261) | MISS ceiling | 0 srp | 1 | 1 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 30.114 (47.268) | MISS ceiling | 0 srp | 2 | 2 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 24.788 (39.599) | MISS ceiling | 1 events | 1 | 1 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 800.001 | 19 | 4,358,434 (87.169) | no | {'srp': 27} |
| backlog-owed | 860.053 | 18 | 4,344,402 (86.888) | no | {'srp': 29} |
| fixture | 20.000 | 1 | 2,512,972 (50.259) | no | {'adp': 1, 'acmp': 1, 'aecp': 1, 'maap': 1, 'srp': 1} |

Composed maximum over 2 of 4 backlog windows, a partial figure (backlog-adp, backlog-adp-refill not run): at least 4,358,434 CPU cycles (87.169 ms), backlog, a lower bound (load unreleased in backlog, backlog-owed).
Over the windows that released their whole load only: none.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 1,127,940 | 22.559 | 10 | 20 | MISS ceiling | 1,569,488 | 63 (14) | 0.076 |
| LINK_UP | `adp.link_up.if0` | 1,798,455 | 35.969 | 10 | 200 | MISS T_svc | 3,439,798 | 134 (11) | 0.097 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 389,134 | 7.783 | 10 | 200 | fits | 1,033,007 | 58 (39) | 0.106 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 253,273 | 5.065 | 10 | 200 | fits | 245,873 | 15 (11) | 0.147 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 749,923 | 14.998 | 10 | 20 | MISS T_svc | 2,452,382 | 110 (35) | 0.051 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 1,527,439 | 30.549 | 10 | 20 | MISS ceiling | 2,283,481 | 77 (14) | 0.065 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 987,042 | 19.741 | 10 | 20 | MISS T_svc | 2,230,974 | 78 (14) | 0.064 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 937,129 | 18.743 | 10 | 20 | MISS T_svc | 2,480,281 | 110 (35) | 0.052 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 1,239,399 | 24.788 | 10 | 18 | MISS ceiling | 1,979,926 | 64 | 0.076 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 1,642,289 | 32.846 | 10 | 18 | MISS ceiling | 1,331,355 | 34 | 0.115 |
| malformed MRPDU discard | `srp.malformed.if0` | 1,505,711 | 30.114 | 10 | 18 | MISS ceiling | 1,115,626 | 41 | 0.115 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 2,432,195 | 48.644 | 210 | 218 | fits | 2,559,818 | 89 | 0.092 |
| an event behind 15 others | `backlog.event.if0` | 6,222,184 | 124.444 | 10 | 200 | MISS T_svc | 4,358,434 | 356 | 0.081 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 19,178,400 | 383.568 | 10 | 20 | MISS ceiling | 3,088,258 | 258 | 0.080 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 3,531,122 | 70.622 | 10 | 200 | MISS T_svc | 3,459,242 | 389 | 0.068 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 14,007,032 | 280.141 | 10 | 200 | MISS ceiling | 3,487,556 | 326 | 0.084 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 3,528,993 | 70.580 | 10 | 20 | MISS ceiling | 3,459,242 | 389 | 0.068 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 20,180,492 | 403.610 | 10 | 20 | MISS ceiling | 3,088,258 | 258 | 0.080 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 3,530,785 | 70.616 | 10 | 24 | MISS ceiling | 3,459,242 | 389 | 0.068 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 37,079,959 | 741.599 | 10 | 24 | MISS ceiling | 1,489,272 | 142 | 0.064 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 3,530,265 | 70.605 | 10 | 50 | MISS ceiling | 3,459,242 | 389 | 0.068 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 14,006,284 | 280.126 | 10 | 50 | MISS ceiling | 3,487,556 | 326 | 0.084 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 38,305,550 | 766.111 | 10 | 18 | MISS ceiling | 1,225,851 | 67 | 0.121 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 39,997,865 | 799.957 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 26,105,914 | 522.118 | 10 | 20 | MISS ceiling | 1,664,559 | 164 | 0.065 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 27,955,368 | 559.107 | 10 | 20 | MISS ceiling | 1,849,492 | 170 | 0.069 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 29,804,991 | 596.100 | 10 | 20 | MISS ceiling | 1,849,660 | 170 | 0.069 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 31,469,370 | 629.387 | 10 | 20 | MISS ceiling | 1,664,417 | 164 | 0.065 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 33,318,865 | 666.377 | 10 | 20 | MISS ceiling | 1,849,532 | 170 | 0.069 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 2,618,550 | 52.371 | 10 | 200 | MISS T_svc | 2,729,411 | 341 | 0.069 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 13,509,660 | 270.193 | 10 | 200 | MISS ceiling | 4,344,402 | 366 | 0.080 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 2,616,421 | 52.328 | 10 | 20 | MISS ceiling | 2,729,411 | 341 | 0.069 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 19,877,578 | 397.552 | 10 | 20 | MISS ceiling | 3,175,186 | 236 | 0.078 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 2,618,213 | 52.364 | 10 | 24 | MISS ceiling | 2,729,411 | 341 | 0.069 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 38,461,930 | 769.239 | 10 | 24 | MISS ceiling | 1,512,361 | 142 | 0.064 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 2,617,693 | 52.354 | 10 | 50 | MISS ceiling | 2,729,411 | 341 | 0.069 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 13,508,912 | 270.178 | 10 | 50 | MISS ceiling | 4,344,402 | 366 | 0.080 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 40,194,461 | 803.889 | 10 | 18 | MISS ceiling | 1,732,791 | 48 | 0.120 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 43,000,448 | 860.009 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 2,519,283 | 50.386 | 10 | 20 | MISS ceiling | 2,962,702 | 120 (29) | 0.049 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 1,204,195 | 24.084 | 10 | 20 | MISS ceiling | 2,707,494 | 116 (35) | 0.056 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 1,048,842 | 20.977 | 10 | 20 | MISS ceiling | 2,487,532 | 110 (12) | 0.052 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 2,022,620 | 40.452 | 10 | 50 | MISS T_svc | 3,439,798 | 134 | 0.097 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 307,936 | 6.159 | 10 | 50 | fits | 1,066,247 | 49 | 0.110 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 399,279 | 7.986 | 10 | 50 | fits | 1,044,217 | 48 | 0.109 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 640,131 | 12.803 | 10 | 50 | MISS T_svc | 1,362,326 | 82 | 0.108 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 664,940 | 13.299 | 10 | 50 | MISS T_svc | 1,362,326 | 82 | 0.108 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 377,721 | 7.554 | 10 | 50 | fits | 876,704 | 52 | 0.103 |
| LINK_UP | `adp.link_up.if0` | 1,798,455 | 35.969 | 10 | 200 | MISS T_svc | 3,439,798 | 134 (11) | 0.097 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 389,134 | 7.783 | 10 | 200 | fits | 1,033,007 | 58 (39) | 0.106 |
| LINK_DOWN | `adp.link_down.if0` | 1,122,395 | 22.448 | 10 | 200 | MISS T_svc | 1,240,813 | 30 (9) | 0.086 |
| LINK_UP | `adp.link_up.if0` | 1,798,455 | 35.969 | 10 | 200 | MISS T_svc | 3,439,798 | 134 (11) | 0.097 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 389,134 | 7.783 | 10 | 200 | fits | 1,033,007 | 58 (39) | 0.106 |
| GM_CHANGE | `adp.gm_change.if0` | 415,608 | 8.312 | 10 | 200 | fits | 902,076 | 30 (11) | 0.113 |
| LINK_UP | `adp.link_up.if0` | 1,798,455 | 35.969 | 10 | 200 | MISS T_svc | 3,439,798 | 134 (11) | 0.097 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 389,134 | 7.783 | 10 | 200 | fits | 1,033,007 | 58 (39) | 0.106 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 737,557 | 14.751 | 10 | 200 | MISS T_svc | 1,001,144 | 50 (31) | 0.116 |
| LINK_UP | `adp.link_up.if0` | 1,798,455 | 35.969 | 10 | 200 | MISS T_svc | 3,439,798 | 134 (11) | 0.097 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 389,134 | 7.783 | 10 | 200 | fits | 1,033,007 | 58 (39) | 0.106 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 737,557 | 14.751 | 10 | 200 | MISS T_svc | 1,001,144 | 50 (31) | 0.116 |
| set_name | `aecp_fanout.set_name.if0` | 2,263,547 | 45.271 | 10 | 24 | MISS ceiling | 2,332,179 | 634 | 0.052 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 2,022,576 | 40.452 | 10 | 24 | MISS ceiling | 2,916,413 | 366 | 0.068 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 1,851,767 | 37.035 | 10 | 24 | MISS ceiling | 2,865,271 | 349 | 0.066 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 1,677,333 | 33.547 | 10 | 24 | MISS ceiling | 2,635,034 | 343 | 0.064 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 1,872,818 | 37.456 | 10 | 24 | MISS ceiling | 2,909,033 | 389 | 0.065 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 1,736,546 | 34.731 | 10 | 24 | MISS ceiling | 2,736,927 | 383 | 0.062 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 1,852,880 | 37.058 | 10 | 24 | MISS ceiling | 2,841,791 | 355 | 0.068 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 2,361,489 | 47.230 | 10 | 24 | MISS ceiling | 3,336,488 | 460 | 0.069 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 1,632,133 | 32.643 | 10 | 24 | MISS ceiling | 2,631,787 | 394 | 0.062 |
| BIND_RX | `acmp.bind_rx.if0` | 954,091 | 19.082 | 10 | 20 | MISS T_svc | 1,530,355 | 94 (77) | 0.096 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 573,479 | 11.470 | 10 | 20 | MISS T_svc | 1,714,029 | 74 (32) | 0.074 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | - | - | - | - | no end: missing ['resp:1:4101'] | - | - | - |
| UNBIND_RX | `acmp.unbind_rx.if0` | 609,590 | 12.192 | 10 | 20 | MISS T_svc | 3,633,806 | 184 (50) | 0.053 |
| PROBE_TX | `acmp.probe_tx.if0` | - | - | - | - | no end: missing ['resp:1:4103'] | - | - | - |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 525,233 | 10.505 | 10 | 20 | MISS T_svc | 2,918,211 | 163 (48) | 0.067 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 1,913,805 | 38.276 | 10 | 20 | MISS ceiling | 2,878,719 | 193 (48) | 0.065 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 232,882 | 4.658 | 10 | 20 | fits | 2,878,719 | 193 (48) | 0.065 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 1,054,501 | 21.090 | 10 | 24 | MISS T_svc | 1,238,489 | 59 | 0.087 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 1,207,653 | 24.153 | 10 | 24 | MISS ceiling | 1,349,427 | 137 | 0.061 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 1,372,350 | 27.447 | 10 | 24 | MISS ceiling | 1,313,672 | 85 | 0.067 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 1,187,821 | 23.756 | 10 | 24 | MISS T_svc | 1,133,605 | 90 | 0.060 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 925,463 | 18.509 | 10 | 24 | MISS T_svc | 1,914,560 | 146 | 0.077 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 1,176,875 | 23.537 | 10 | 24 | MISS T_svc | 1,133,578 | 89 | 0.060 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 1,367,290 | 27.346 | 10 | 24 | MISS ceiling | 1,313,274 | 84 | 0.067 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 1,365,229 | 27.305 | 10 | 24 | MISS ceiling | 1,311,782 | 80 | 0.068 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 1,179,458 | 23.589 | 10 | 24 | MISS T_svc | 1,125,983 | 71 | 0.062 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 2,500,686 | 50.014 | 10 | 24 | MISS ceiling | 1,751,806 | 184 | 0.067 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 1,360,249 | 27.205 | 10 | 24 | MISS ceiling | 1,305,509 | 64 | 0.070 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 1,594,677 | 31.894 | 10 | 24 | MISS ceiling | 1,540,643 | 92 | 0.074 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 1,368,880 | 27.378 | 10 | 24 | MISS ceiling | 1,314,750 | 81 | 0.066 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 1,190,698 | 23.814 | 10 | 24 | MISS T_svc | 1,132,283 | 81 | 0.060 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 1,368,471 | 27.369 | 10 | 24 | MISS ceiling | 1,314,008 | 79 | 0.067 |
| get_configuration | `aecp.get_configuration.if0` | 1,160,783 | 23.216 | 10 | 24 | MISS T_svc | 1,106,550 | 53 | 0.065 |
| entity_available | `aecp.entity_available.if0` | 1,344,930 | 26.899 | 10 | 24 | MISS ceiling | 1,292,929 | 63 | 0.070 |
| get_name | `aecp.get_name.if0` | 1,181,469 | 23.629 | 10 | 24 | MISS T_svc | 1,129,361 | 70 | 0.063 |
| get_counters | `aecp.get_counters.if0` | 1,407,463 | 28.149 | 10 | 24 | MISS ceiling | 1,355,714 | 97 | 0.069 |
| get_avb_info | `aecp.get_avb_info.if0` | 1,353,226 | 27.065 | 10 | 24 | MISS ceiling | 1,298,812 | 59 | 0.070 |
| unknown_command | `aecp.unknown_command.if0` | 1,149,908 | 22.998 | 10 | 24 | MISS T_svc | 1,097,754 | 53 | 0.064 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 1,285,601 | 25.712 | 10 | 24 | MISS ceiling | 1,233,545 | 63 | 0.086 |
| set_name | `aecp.set_name.if0` | 1,384,778 | 27.696 | 10 | 24 | MISS ceiling | 1,704,301 | 139 | 0.066 |
| lock_entity | `aecp.lock_entity.if0` | 917,281 | 18.346 | 10 | 24 | MISS T_svc | 1,880,448 | 103 | 0.076 |
| unlock_entity | `aecp.unlock_entity.if0` | 1,413,529 | 28.271 | 10 | 24 | MISS ceiling | 2,371,460 | 164 | 0.083 |
| LINK_UP | `fixture.link_up.if0` | 1,798,455 | 35.969 | 10 | 200 | MISS T_svc | 3,439,798 | 134 (11) | 0.097 |
| malformed MRPDU discard | `fixture.malformed.if0` | 979,049 | 19.581 | 10 | 18 | MISS ceiling | 1,075,700 | 40 | 0.121 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | - | - | - | - | no end: no notification to ['0a0b0c0d0e0f0001@if0'] | - | - | - |
| LINK_DOWN | `fixture.link_down.if0` | 2,030,962 | 40.619 | 10 | 200 | MISS T_svc | 3,366,825 | 143 (9) | 0.094 |
| BIND_RX | `fixture.bind_rx.if0` | 1,636,254 | 32.725 | 10 | 20 | MISS ceiling | 3,366,825 | 143 (77) | 0.094 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 955,400 | 19.108 | 10 | 20 | MISS T_svc | 2,736,757 | 139 (35) | 0.054 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 547,498 | 10.950 | 10 | 20 | MISS T_svc | 2,480,366 | 100 (29) | 0.068 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 3,484,015 | 69.680 | 10 | 200 | MISS T_svc | 2,512,972 | 249 | 0.078 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 3,484,015 | 69.680 | 10 | 200 | MISS T_svc | 2,512,972 | 249 | 0.078 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 3,483,880 | 69.678 | 10 | 20 | MISS ceiling | 2,512,972 | 249 | 0.078 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 3,483,880 | 69.678 | 10 | 20 | MISS ceiling | 2,512,972 | 249 | 0.078 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 3,483,983 | 69.680 | 10 | 24 | MISS ceiling | 2,512,972 | 249 | 0.078 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 3,483,983 | 69.680 | 10 | 24 | MISS ceiling | 2,512,972 | 249 | 0.078 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 3,483,950 | 69.679 | 10 | 50 | MISS ceiling | 2,512,972 | 249 | 0.078 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 3,483,950 | 69.679 | 10 | 50 | MISS ceiling | 2,512,972 | 249 | 0.078 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 11,727,159 | 234.543 | 10 | 18 | MISS ceiling | 1,890,306 | 74 | 0.086 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 11,727,159 | 234.543 | 10 | 18 | MISS ceiling | 1,890,306 | 74 | 0.086 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `adp-advertise`: wait quiet TIMEOUT
- `adp-advertise`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog`: wait tx TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `backlog-owed`: wait tx TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `maap`: wait quiet TIMEOUT
- `maap`: wait quiet TIMEOUT
- `maap`: wait quiet TIMEOUT
- `adp-link`: wait quiet TIMEOUT
- `adp-link`: wait quiet TIMEOUT
- `adp-link`: wait quiet TIMEOUT
- `adp-gm`: wait quiet TIMEOUT
- `adp-gm`: wait quiet TIMEOUT
- `adp-gm`: wait quiet TIMEOUT
- `adp-discover`: wait quiet TIMEOUT
- `adp-discover`: wait quiet TIMEOUT
- `adp-discover`: wait quiet TIMEOUT
- `control`: wait quiet TIMEOUT
- `control`: wait quiet TIMEOUT
- `control`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait tx TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait tx TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
