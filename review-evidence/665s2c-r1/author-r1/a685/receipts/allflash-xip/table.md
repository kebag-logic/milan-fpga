### 1x1

64 of 73 paths and 119 of 131 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 22.870 (63.481) | MISS ceiling | 0 acmp | 2 | 2 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 6.089 (54.199) | fits | 0 acmp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 19.627 (47.327) | MISS T_svc | 0 adp | 1 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 36.730 (55.515) | MISS ceiling | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 26.072 (45.421) | MISS ceiling | 0 acmp | 1 | 1 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 38.995 (116.334) | MISS ceiling | 0 acmp | 1 | 1 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 16.367 (62.136) | MISS T_svc | 1 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 13.521 (35.079) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 23.701 (93.426) | MISS ceiling | 1 events | 1 | 1 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 7.796 (15.983) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 4.607 (13.200) | fits | 1 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 31.052 (122.604) | MISS T_svc | 2 events | 2 | 1 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 35.371 (103.815) | MISS T_svc | 0 events | 6 | 6 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 5.977 (20.054) | fits | 1 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 12.351 (31.291) | MISS T_svc | 0 events | 5 | 5 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 20.545 (40.546) | MISS T_svc | 0 aecp | 1 | 1 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 20.601 (40.602) | MISS T_svc | 0 aecp | 1 | 1 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 23.598 (43.598) | MISS T_svc | 0 aecp | 1 | 1 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 21.155 (41.156) | MISS T_svc | 0 aecp | 1 | 1 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 20.958 (40.959) | MISS T_svc | 0 aecp | 1 | 1 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 13.210 (33.213) | MISS T_svc | 0 aecp | 1 | 1 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 19.257 (39.257) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 21.541 (41.630) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 24.002 (44.002) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 20.759 (40.760) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 20.735 (40.736) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 42.258 (62.304) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 20.687 (40.643) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 20.651 (40.652) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 20.913 (40.913) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 28.348 (48.349) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 20.929 (40.930) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 20.813 (40.813) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 24.551 (44.597) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 24.088 (44.043) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 20.821 (40.821) | MISS T_svc | 0 aecp | 1 | 1 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 20.742 (32.299) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 23.570 (47.245) | MISS T_svc | 0 aecp | 1 | 1 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 20.235 (40.235) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 22.331 (41.619) | MISS T_svc | 0 aecp | 1 | 1 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 42.507 (62.465) | MISS ceiling | 0 aecp | 1 | 1 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 48.762 (68.163) | MISS ceiling | 0 aecp | 1 | 1 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 42.996 (63.766) | MISS ceiling | 0 aecp | 1 | 1 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 44.020 (62.525) | MISS ceiling | 0 aecp | 1 | 1 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 43.085 (63.260) | MISS ceiling | 0 aecp | 2 | 2 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 45.452 (67.484) | MISS ceiling | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 45.647 (65.519) | MISS ceiling | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 39.161 (59.161) | MISS ceiling | 0 aecp | 1 | 1 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 368.407 (390.418) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 210.687 (268.028) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 306.434 (411.017) | MISS ceiling | 8 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 119.884 (205.973) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 499.172 (516.292) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 629.038 (646.162) | MISS ceiling | 11 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 9.986 (37.600) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 5.939 (16.990) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 39.838 (103.815) | MISS T_svc | 0 events | 1 | 1 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 9.409 (37.600) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 7.092 (32.112) | fits | 1 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 67.063 | MISS ceiling | 0 acmp | 5 | 5 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 398.932 | MISS ceiling | 11 acmp | 5 | 5 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 67.106 | MISS T_svc | 0 adp | 5 | 5 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 358.976 | MISS ceiling | 8 adp | 5 | 5 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 67.099 | MISS ceiling | 0 aecp | 5 | 5 |
| AECP record released under the composed load, last | 0 | `backlog-adp-refill.service.aecp.last.if0` (backlog-adp-refill) | at least 846.424 | STARVED: never released | 15 aecp | 5 | 5 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 67.089 | MISS ceiling | 0 maap | 5 | 5 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 272.799 | MISS ceiling | 6 maap | 5 | 5 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 846.419 | STARVED: never released | 0 srp | 5 | 5 |
| SRP record released under the composed load, last | 0 | `backlog-owed.service.srp.last.if0` (backlog-owed) | at least 860.009 | STARVED: never released | 31 srp | 5 | 5 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 40.248 (58.175) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 38.845 (41.223) | MISS ceiling | 0 srp | 1 | 1 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 16.567 (17.296) | MISS T_svc | 0 srp | 2 | 2 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 28.146 (39.410) | MISS ceiling | 0 events | 1 | 1 |

Composed windows: the longest pass is the composed maximum only where the window released its whole load.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 800.001 | 21 | 4,279,634 (85.593) | no | {'srp': 20} |
| backlog-adp | 710.740 | 12 | 3,900,708 (78.014) | no | {'aecp': 3, 'srp': 32} |
| backlog-adp-refill | 846.436 | 15 | 4,094,531 (81.891) | no | {'aecp': 1, 'srp': 32} |
| backlog-owed | 860.053 | 21 | 4,217,251 (84.345) | no | {'srp': 28} |
| fixture | 20.000 | 1 | 2,648,392 (52.968) | no | {'aecp': 1, 'maap': 1, 'srp': 1} |

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| LINK_UP | `adp.link_up.if0` | 1,768,548 | 35.371 | 10 | 200 | MISS T_svc | 3,220,235 | 134 (11) | 0.092 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 617,537 | 12.351 | 10 | 200 | MISS T_svc | 952,796 | 58 (39) | 0.100 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 298,871 | 5.977 | 10 | 200 | fits | 233,530 | 15 (11) | 0.143 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 1,407,279 | 28.146 | 10 | 18 | MISS ceiling | 1,970,522 | 64 | 0.077 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 1,942,272 | 38.845 | 10 | 18 | MISS ceiling | 1,449,320 | 40 | 0.115 |
| malformed MRPDU discard | `srp.malformed.if0` | 649,901 | 12.998 | 10 | 18 | MISS T_svc | 1,207,629 | 46 | 0.112 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 2,012,416 | 40.248 | 210 | 218 | fits | 2,290,668 | 83 | 0.088 |
| an event behind 15 others | `backlog.event.if0` | 5,994,191 | 119.884 | 10 | 200 | MISS T_svc | 4,279,634 | 355 | 0.080 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 18,420,353 | 368.407 | 10 | 20 | MISS ceiling | 2,937,625 | 257 | 0.077 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 3,355,286 | 67.106 | 10 | 200 | MISS T_svc | 3,447,944 | 388 | 0.069 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 13,553,574 | 271.071 | 10 | 200 | MISS ceiling | 3,347,901 | 325 | 0.081 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 3,353,157 | 67.063 | 10 | 20 | MISS ceiling | 3,447,944 | 388 | 0.069 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 19,425,679 | 388.514 | 10 | 20 | MISS ceiling | 2,937,625 | 257 | 0.077 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 3,354,949 | 67.099 | 10 | 24 | MISS ceiling | 3,447,944 | 388 | 0.069 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 34,343,333 | 686.867 | 10 | 24 | MISS ceiling | 1,241,944 | 135 | 0.056 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 3,354,429 | 67.089 | 10 | 50 | MISS ceiling | 3,447,944 | 388 | 0.069 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 13,552,826 | 271.057 | 10 | 50 | MISS ceiling | 3,347,901 | 325 | 0.081 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 35,488,595 | 709.772 | 10 | 18 | MISS ceiling | 1,145,522 | 67 | 0.116 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 39,997,865 | 799.957 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 10,534,356 | 210.687 | 10 | 20 | MISS ceiling | 3,900,708 | 353 | 0.070 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 3,016,124 | 60.322 | 10 | 200 | MISS T_svc | 3,620,403 | 387 | 0.058 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 12,796,830 | 255.937 | 10 | 200 | MISS ceiling | 3,900,708 | 353 | 0.070 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 3,016,580 | 60.332 | 10 | 20 | MISS ceiling | 3,620,403 | 387 | 0.058 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 19,572,488 | 391.450 | 10 | 20 | MISS ceiling | 3,742,585 | 302 | 0.066 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 3,018,372 | 60.367 | 10 | 24 | MISS ceiling | 3,620,403 | 387 | 0.058 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 35,536,421 | 710.728 | 10 | 24 | STARVED: never released | 0 | - | 0.000 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 3,017,852 | 60.357 | 10 | 50 | MISS ceiling | 3,620,403 | 387 | 0.058 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 12,798,668 | 255.973 | 10 | 50 | MISS ceiling | 3,900,708 | 353 | 0.070 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 35,536,161 | 710.723 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 35,535,154 | 710.703 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 15,321,696 | 306.434 | 10 | 20 | MISS ceiling | 4,094,531 | 334 | 0.068 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 3,016,124 | 60.322 | 10 | 200 | MISS T_svc | 3,620,403 | 387 | 0.058 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 17,948,792 | 358.976 | 10 | 200 | MISS ceiling | 4,094,531 | 334 | 0.068 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 3,016,580 | 60.332 | 10 | 20 | MISS ceiling | 3,620,403 | 387 | 0.058 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 19,946,598 | 398.932 | 10 | 20 | MISS ceiling | 4,094,531 | 334 | 0.068 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 3,018,372 | 60.367 | 10 | 24 | MISS ceiling | 3,620,403 | 387 | 0.058 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 42,321,219 | 846.424 | 10 | 24 | STARVED: never released | 0 | - | 0.000 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 3,017,852 | 60.357 | 10 | 50 | MISS ceiling | 3,620,403 | 387 | 0.058 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 12,558,199 | 251.164 | 10 | 50 | MISS ceiling | 3,660,239 | 346 | 0.069 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 42,320,959 | 846.419 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 42,319,952 | 846.399 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 24,958,580 | 499.172 | 10 | 20 | MISS ceiling | 1,584,215 | 163 | 0.062 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 26,542,787 | 530.856 | 10 | 20 | MISS ceiling | 1,584,245 | 163 | 0.062 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 28,283,627 | 565.673 | 10 | 20 | MISS ceiling | 1,740,877 | 169 | 0.066 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 29,867,750 | 597.355 | 10 | 20 | MISS ceiling | 1,584,161 | 163 | 0.062 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 31,451,924 | 629.038 | 10 | 20 | MISS ceiling | 1,584,211 | 163 | 0.062 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 2,899,367 | 57.987 | 10 | 200 | MISS T_svc | 2,551,971 | 340 | 0.068 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 13,640,716 | 272.814 | 10 | 200 | MISS ceiling | 4,217,251 | 365 | 0.079 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 2,897,238 | 57.945 | 10 | 20 | MISS ceiling | 2,551,971 | 340 | 0.068 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 19,699,991 | 394.000 | 10 | 20 | MISS ceiling | 3,020,954 | 235 | 0.075 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 2,899,030 | 57.981 | 10 | 24 | MISS ceiling | 2,551,971 | 340 | 0.068 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 36,313,228 | 726.265 | 10 | 24 | MISS ceiling | 1,423,603 | 141 | 0.061 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 2,898,510 | 57.970 | 10 | 50 | MISS ceiling | 2,551,971 | 340 | 0.068 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 13,639,968 | 272.799 | 10 | 50 | MISS ceiling | 4,217,251 | 365 | 0.079 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 37,950,327 | 759.007 | 10 | 18 | MISS ceiling | 1,637,359 | 48 | 0.116 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 43,000,448 | 860.009 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 1,991,885 | 39.838 | 10 | 50 | MISS T_svc | 3,220,235 | 134 | 0.092 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 354,595 | 7.092 | 10 | 50 | fits | 993,946 | 49 | 0.106 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 201,010 | 4.020 | 10 | 50 | fits | 993,665 | 49 | 0.106 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 470,472 | 9.409 | 10 | 50 | fits | 1,111,486 | 76 | 0.100 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 499,305 | 9.986 | 10 | 50 | fits | 1,111,486 | 76 | 0.100 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 296,938 | 5.939 | 10 | 50 | fits | 849,524 | 52 | 0.102 |
| LINK_UP | `adp.link_up.if0` | 1,768,548 | 35.371 | 10 | 200 | MISS T_svc | 3,220,235 | 134 (11) | 0.092 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 617,537 | 12.351 | 10 | 200 | MISS T_svc | 952,796 | 58 (39) | 0.100 |
| LINK_DOWN | `adp.link_down.if0` | 225,902 | 4.518 | 10 | 200 | fits | 1,226,541 | 30 (9) | 0.086 |
| LINK_UP | `adp.link_up.if0` | 1,768,548 | 35.371 | 10 | 200 | MISS T_svc | 3,220,235 | 134 (11) | 0.092 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 617,537 | 12.351 | 10 | 200 | MISS T_svc | 952,796 | 58 (39) | 0.100 |
| GM_CHANGE | `adp.gm_change.if0` | 230,362 | 4.607 | 10 | 200 | fits | 659,990 | 24 (11) | 0.101 |
| LINK_UP | `adp.link_up.if0` | 1,768,548 | 35.371 | 10 | 200 | MISS T_svc | 3,220,235 | 134 (11) | 0.092 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 617,537 | 12.351 | 10 | 200 | MISS T_svc | 952,796 | 58 (39) | 0.100 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 389,783 | 7.796 | 10 | 200 | fits | 799,168 | 43 (31) | 0.112 |
| LINK_UP | `adp.link_up.if0` | 1,768,548 | 35.371 | 10 | 200 | MISS T_svc | 3,220,235 | 134 (11) | 0.092 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 617,537 | 12.351 | 10 | 200 | MISS T_svc | 952,796 | 58 (39) | 0.100 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 389,783 | 7.796 | 10 | 200 | fits | 799,168 | 43 (31) | 0.112 |
| set_name | `aecp_fanout.set_name.if0` | 2,272,615 | 45.452 | 10 | 24 | MISS ceiling | 2,576,203 | 613 | 0.060 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 2,201,011 | 44.020 | 10 | 24 | MISS ceiling | 3,126,258 | 354 | 0.075 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 2,154,231 | 43.085 | 10 | 24 | MISS ceiling | 3,163,010 | 343 | 0.073 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 2,037,009 | 40.740 | 10 | 24 | MISS ceiling | 2,997,350 | 337 | 0.073 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 2,149,785 | 42.996 | 10 | 24 | MISS ceiling | 3,188,298 | 388 | 0.072 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 2,125,330 | 42.507 | 10 | 24 | MISS ceiling | 3,123,241 | 388 | 0.070 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 2,282,331 | 45.647 | 10 | 24 | MISS ceiling | 3,275,967 | 360 | 0.078 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 2,438,088 | 48.762 | 10 | 24 | MISS ceiling | 3,408,163 | 448 | 0.073 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 1,958,050 | 39.161 | 10 | 24 | MISS ceiling | 2,958,075 | 388 | 0.071 |
| BIND_RX | `acmp.bind_rx.if0` | 979,884 | 19.598 | 10 | 20 | MISS T_svc | 1,358,038 | 88 (77) | 0.092 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 676,032 | 13.521 | 10 | 20 | MISS T_svc | 1,753,941 | 63 (32) | 0.076 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 1,836,493 | 36.730 | 10 | 20 | MISS ceiling | 2,775,737 | 110 (47) | 0.045 |
| UNBIND_RX | `acmp.unbind_rx.if0` | - | - | - | - | no end: missing ['resp:1:4102', 'tmr:1'] | - | - | - |
| PROBE_TX | `acmp.probe_tx.if0` | 818,359 | 16.367 | 10 | 20 | MISS T_svc | 3,106,775 | 155 (48) | 0.056 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 1,949,768 | 38.995 | 10 | 20 | MISS ceiling | 2,709,931 | 179 (48) | 0.062 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 304,429 | 6.089 | 10 | 20 | fits | 2,709,931 | 179 (48) | 0.062 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 1,303,614 | 26.072 | 10 | 20 | MISS ceiling | 2,271,031 | 105 (48) | 0.061 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 1,037,118 | 20.742 | 10 | 24 | MISS T_svc | 1,003,184 | 52 | 0.078 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 1,077,056 | 21.541 | 10 | 24 | MISS T_svc | 1,127,537 | 130 | 0.054 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 1,200,083 | 24.002 | 10 | 24 | MISS ceiling | 1,243,870 | 84 | 0.064 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 1,045,631 | 20.913 | 10 | 24 | MISS T_svc | 1,248,281 | 95 | 0.063 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 1,227,540 | 24.551 | 10 | 24 | MISS ceiling | 1,432,672 | 131 | 0.065 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 1,204,402 | 24.088 | 10 | 24 | MISS ceiling | 1,248,292 | 94 | 0.063 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 1,041,040 | 20.821 | 10 | 24 | MISS T_svc | 1,243,673 | 83 | 0.064 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 1,037,953 | 20.759 | 10 | 24 | MISS T_svc | 1,241,456 | 79 | 0.065 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 1,036,774 | 20.735 | 10 | 24 | MISS T_svc | 1,240,251 | 76 | 0.065 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 2,112,884 | 42.258 | 10 | 24 | MISS ceiling | 1,465,375 | 177 | 0.059 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 1,034,375 | 20.687 | 10 | 24 | MISS T_svc | 1,078,835 | 57 | 0.062 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 1,032,553 | 20.651 | 10 | 24 | MISS T_svc | 1,078,977 | 57 | 0.062 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 1,417,424 | 28.348 | 10 | 24 | MISS ceiling | 1,463,839 | 108 | 0.068 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 1,046,444 | 20.929 | 10 | 24 | MISS T_svc | 1,092,854 | 80 | 0.058 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 1,040,642 | 20.813 | 10 | 24 | MISS T_svc | 1,087,188 | 72 | 0.059 |
| get_configuration | `aecp.get_configuration.if0` | 1,179,889 | 23.598 | 10 | 24 | MISS T_svc | 1,225,880 | 58 | 0.068 |
| entity_available | `aecp.entity_available.if0` | 1,027,242 | 20.545 | 10 | 24 | MISS T_svc | 1,229,773 | 62 | 0.068 |
| get_name | `aecp.get_name.if0` | 1,047,898 | 20.958 | 10 | 24 | MISS T_svc | 1,250,426 | 75 | 0.066 |
| get_counters | `aecp.get_counters.if0` | 1,057,754 | 21.155 | 10 | 24 | MISS T_svc | 1,260,527 | 91 | 0.065 |
| get_avb_info | `aecp.get_avb_info.if0` | 1,030,064 | 20.601 | 10 | 24 | MISS T_svc | 1,076,132 | 52 | 0.062 |
| unknown_command | `aecp.unknown_command.if0` | 1,011,737 | 20.235 | 10 | 24 | MISS T_svc | 1,057,921 | 52 | 0.063 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 962,832 | 19.257 | 10 | 24 | MISS T_svc | 1,008,847 | 56 | 0.078 |
| set_name | `aecp.set_name.if0` | 1,178,501 | 23.570 | 10 | 24 | MISS T_svc | 1,408,241 | 112 | 0.060 |
| lock_entity | `aecp.lock_entity.if0` | 660,488 | 13.210 | 10 | 24 | MISS T_svc | 1,660,655 | 91 | 0.070 |
| unlock_entity | `aecp.unlock_entity.if0` | 1,116,531 | 22.331 | 10 | 24 | MISS T_svc | 1,121,068 | 71 | 0.062 |
| LINK_UP | `fixture.link_up.if0` | 1,768,548 | 35.371 | 10 | 200 | MISS T_svc | 3,220,235 | 134 (11) | 0.092 |
| malformed MRPDU discard | `fixture.malformed.if0` | 828,327 | 16.567 | 10 | 18 | MISS T_svc | 864,777 | 34 | 0.116 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | - | - | - | - | no end: no notification to ['0a0b0c0d0e0f0001@if0'] | - | - | - |
| LINK_DOWN | `fixture.link_down.if0` | 1,552,620 | 31.052 | 10 | 200 | MISS T_svc | 3,174,046 | 143 (9) | 0.090 |
| BIND_RX | `fixture.bind_rx.if0` | 1,143,484 | 22.870 | 10 | 20 | MISS ceiling | 3,174,046 | 143 (77) | 0.090 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 1,185,055 | 23.701 | 10 | 20 | MISS ceiling | 2,528,772 | 118 (35) | 0.051 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 981,348 | 19.627 | 10 | 20 | MISS T_svc | 2,366,364 | 89 (29) | 0.050 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 2,715,327 | 54.307 | 10 | 200 | MISS T_svc | 2,648,392 | 279 | 0.070 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 2,715,327 | 54.307 | 10 | 200 | MISS T_svc | 2,648,392 | 279 | 0.070 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 2,715,192 | 54.304 | 10 | 20 | MISS ceiling | 2,648,392 | 279 | 0.070 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 2,715,192 | 54.304 | 10 | 20 | MISS ceiling | 2,648,392 | 279 | 0.070 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 2,715,295 | 54.306 | 10 | 24 | MISS ceiling | 2,648,392 | 279 | 0.070 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 2,715,295 | 54.306 | 10 | 24 | MISS ceiling | 2,648,392 | 279 | 0.070 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 2,715,262 | 54.305 | 10 | 50 | MISS ceiling | 2,648,392 | 279 | 0.070 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 2,715,262 | 54.305 | 10 | 50 | MISS ceiling | 2,648,392 | 279 | 0.070 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 10,349,507 | 206.990 | 10 | 18 | MISS ceiling | 1,504,101 | 60 | 0.074 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 10,349,507 | 206.990 | 10 | 18 | MISS ceiling | 1,504,101 | 60 | 0.074 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `adp-advertise`: wait quiet TIMEOUT
- `adp-advertise`: wait quiet TIMEOUT
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
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `backlog-owed`: wait tx TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
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
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
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
