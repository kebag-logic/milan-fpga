### 1x1

68 of 75 paths and 106 of 115 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 28.526 (66.611) | MISS ceiling | 0 acmp | 2 | 2 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 37.868 (108.969) | MISS ceiling | 0 acmp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 24.735 (53.128) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 49.731 (90.359) | MISS ceiling | 0 adp | 2 | 1 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 9.999 (57.948) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 11.241 (34.042) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 19.587 (46.455) | MISS T_svc | 3 events | 1 | 1 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 19.370 (95.288) | MISS T_svc | 2 events | 1 | 1 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 21.610 (54.614) | MISS ceiling | 4 events | 2 | 2 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 29.582 (105.556) | MISS ceiling | 2 events | 1 | 1 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 22.572 (91.791) | MISS ceiling | 5 events | 1 | 1 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 18.840 (44.981) | MISS T_svc | 3 events | 1 | 1 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 11.662 (72.143) | MISS T_svc | 0 acmp | 1 | 1 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 14.424 (32.699) | MISS T_svc | 0 adp | 2 | 2 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 8.220 (31.053) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 39.180 (133.818) | MISS T_svc | 1 events | 2 | 2 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 35.192 (107.604) | MISS T_svc | 1 events | 6 | 6 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 5.234 (17.720) | fits | 1 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 11.444 (37.185) | MISS T_svc | 0 events | 5 | 5 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 26.570 (46.570) | MISS ceiling | 0 aecp | 1 | 1 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 23.055 (43.056) | MISS T_svc | 0 aecp | 1 | 1 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 22.908 (42.909) | MISS T_svc | 0 aecp | 1 | 1 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 27.813 (47.814) | MISS ceiling | 0 aecp | 1 | 1 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 23.318 (43.318) | MISS T_svc | 0 aecp | 1 | 1 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 18.077 (37.339) | MISS T_svc | 0 aecp | 1 | 1 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 21.710 (41.711) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 23.975 (44.194) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 27.018 (47.019) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 23.286 (43.287) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 26.937 (46.938) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 49.519 (69.519) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 23.184 (43.185) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 26.855 (46.855) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 23.444 (43.444) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 18.866 (38.649) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 23.327 (43.545) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 27.024 (47.025) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 18.232 (38.015) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 23.224 (43.442) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 27.014 (47.015) | MISS ceiling | 0 aecp | 1 | 1 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 12.184 (32.883) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 31.030 (54.747) | MISS ceiling | 0 aecp | 1 | 1 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 26.358 (46.359) | MISS ceiling | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 30.314 (49.696) | MISS ceiling | 0 aecp | 1 | 1 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 38.016 (58.023) | MISS ceiling | 0 aecp | 1 | 1 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 46.755 (66.260) | MISS ceiling | 0 aecp | 1 | 1 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 33.386 (54.105) | MISS ceiling | 0 aecp | 1 | 1 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 43.697 (61.588) | MISS ceiling | 0 aecp | 1 | 1 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 36.840 (56.001) | MISS ceiling | 0 aecp | 2 | 2 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 41.142 (63.549) | MISS ceiling | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 32.985 (52.763) | MISS ceiling | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 32.275 (52.268) | MISS ceiling | 0 aecp | 1 | 1 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 380.011 (415.832) | MISS ceiling | 11 acmp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 122.771 (223.964) | MISS T_svc | 16 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 522.225 (536.670) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 658.129 (672.577) | MISS ceiling | 11 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 9.628 (39.873) | fits | 1 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 7.343 (21.078) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 39.642 (107.604) | MISS T_svc | 1 events | 1 | 1 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 9.135 (39.873) | fits | 1 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 11.064 (37.664) | MISS T_svc | 1 events | 2 | 1 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 69.294 | MISS ceiling | 0 acmp | 3 | 3 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 399.920 | MISS ceiling | 11 acmp | 3 | 3 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 69.336 | MISS T_svc | 0 adp | 3 | 3 |
| ADP record released under the composed load, last | 0 | `backlog.service.adp.last.if0` (backlog) | 277.338 | MISS ceiling | 7 adp | 3 | 3 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 69.330 | MISS ceiling | 0 aecp | 3 | 3 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 763.944 | MISS ceiling | 15 aecp | 3 | 3 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 69.319 | MISS ceiling | 0 maap | 3 | 3 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 277.323 | MISS ceiling | 6 maap | 3 | 3 |
| SRP record released under the composed load, first | 0 | `backlog-owed.service.srp.first.if0` (backlog-owed) | 798.334 | MISS ceiling | 0 srp | 3 | 3 |
| SRP record released under the composed load, last | 0 | `backlog-owed.service.srp.last.if0` (backlog-owed) | at least 860.009 | STARVED: never released | 31 srp | 3 | 3 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 30.290 (46.993) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 32.336 (42.942) | MISS ceiling | 0 srp | 1 | 1 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 31.218 (34.179) | MISS ceiling | 0 srp | 2 | 2 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 24.094 (39.315) | MISS ceiling | 1 events | 1 | 1 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 800.001 | 20 | 4,326,953 (86.539) | no | {'srp': 26} |
| backlog-owed | 860.053 | 18 | 4,312,794 (86.256) | no | {'srp': 29} |
| fixture | 20.000 | 1 | 2,698,975 (53.980) | no | {'aecp': 1, 'maap': 1, 'srp': 1} |

Composed maximum over 2 of 4 backlog windows, a partial figure (backlog-adp, backlog-adp-refill not run): at least 4,326,953 CPU cycles (86.539 ms), backlog, a lower bound (load unreleased in backlog, backlog-owed).
Over the windows that released their whole load only: none.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 1,128,578 | 22.572 | 10 | 20 | MISS ceiling | 2,105,689 | 79 (14) | 0.050 |
| LINK_UP | `adp.link_up.if0` | 1,759,596 | 35.192 | 10 | 200 | MISS T_svc | 3,414,438 | 134 (11) | 0.097 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 572,192 | 11.444 | 10 | 200 | MISS T_svc | 1,034,266 | 58 (39) | 0.107 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 261,683 | 5.234 | 10 | 200 | fits | 244,005 | 15 (11) | 0.147 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 673,339 | 13.467 | 10 | 20 | MISS T_svc | 2,447,438 | 110 (35) | 0.051 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 1,479,119 | 29.582 | 10 | 20 | MISS ceiling | 2,257,584 | 77 (14) | 0.065 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 942,012 | 18.840 | 10 | 20 | MISS T_svc | 2,249,043 | 78 (14) | 0.065 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 979,337 | 19.587 | 10 | 20 | MISS T_svc | 2,322,733 | 100 (35) | 0.064 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 1,204,696 | 24.094 | 10 | 18 | MISS ceiling | 1,965,756 | 64 | 0.076 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 1,616,819 | 32.336 | 10 | 18 | MISS ceiling | 1,321,444 | 34 | 0.115 |
| malformed MRPDU discard | `srp.malformed.if0` | 1,266,527 | 25.331 | 10 | 18 | MISS ceiling | 911,263 | 34 | 0.112 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 1,514,487 | 30.290 | 210 | 218 | fits | 2,349,640 | 83 | 0.090 |
| an event behind 15 others | `backlog.event.if0` | 6,138,544 | 122.771 | 10 | 200 | MISS T_svc | 4,326,953 | 356 | 0.081 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 19,000,527 | 380.011 | 10 | 20 | MISS ceiling | 3,066,028 | 258 | 0.080 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 3,466,813 | 69.336 | 10 | 200 | MISS T_svc | 3,434,257 | 389 | 0.068 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 13,866,890 | 277.338 | 10 | 200 | MISS ceiling | 3,462,065 | 326 | 0.084 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 3,464,684 | 69.294 | 10 | 20 | MISS ceiling | 3,434,257 | 389 | 0.068 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 19,995,980 | 399.920 | 10 | 20 | MISS ceiling | 3,066,028 | 258 | 0.080 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 3,466,476 | 69.330 | 10 | 24 | MISS ceiling | 3,434,257 | 389 | 0.068 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 36,593,070 | 731.861 | 10 | 24 | MISS ceiling | 1,478,907 | 142 | 0.064 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 3,465,956 | 69.319 | 10 | 50 | MISS ceiling | 3,434,257 | 389 | 0.068 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 13,866,142 | 277.323 | 10 | 50 | MISS ceiling | 3,462,065 | 326 | 0.084 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 37,809,472 | 756.189 | 10 | 18 | MISS ceiling | 1,216,662 | 67 | 0.121 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 39,997,865 | 799.957 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 26,111,240 | 522.225 | 10 | 20 | MISS ceiling | 1,836,614 | 170 | 0.069 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 27,764,161 | 555.283 | 10 | 20 | MISS ceiling | 1,652,959 | 164 | 0.065 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 29,417,015 | 588.340 | 10 | 20 | MISS ceiling | 1,652,891 | 164 | 0.065 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 31,253,579 | 625.072 | 10 | 20 | MISS ceiling | 1,836,602 | 170 | 0.069 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 32,906,467 | 658.129 | 10 | 20 | MISS ceiling | 1,652,925 | 164 | 0.065 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 2,727,424 | 54.548 | 10 | 200 | MISS T_svc | 2,855,773 | 341 | 0.071 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 13,421,410 | 268.428 | 10 | 200 | MISS ceiling | 4,312,794 | 366 | 0.080 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 2,725,295 | 54.506 | 10 | 20 | MISS ceiling | 2,855,773 | 341 | 0.071 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 19,743,495 | 394.870 | 10 | 20 | MISS ceiling | 3,152,134 | 236 | 0.078 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 2,727,087 | 54.542 | 10 | 24 | MISS ceiling | 2,855,773 | 341 | 0.071 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 38,197,203 | 763.944 | 10 | 24 | MISS ceiling | 1,501,856 | 142 | 0.064 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 2,726,567 | 54.531 | 10 | 50 | MISS ceiling | 2,855,773 | 341 | 0.071 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 13,420,662 | 268.413 | 10 | 50 | MISS ceiling | 4,312,794 | 366 | 0.080 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 39,916,680 | 798.334 | 10 | 18 | MISS ceiling | 1,719,737 | 48 | 0.120 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 43,000,448 | 860.009 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 2,486,544 | 49.731 | 10 | 20 | MISS ceiling | 2,941,250 | 120 (29) | 0.049 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 1,236,737 | 24.735 | 10 | 20 | MISS ceiling | 2,656,393 | 116 (35) | 0.055 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 968,485 | 19.370 | 10 | 20 | MISS T_svc | 2,449,523 | 110 (12) | 0.051 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 1,982,119 | 39.642 | 10 | 50 | MISS T_svc | 3,414,438 | 134 | 0.097 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 553,186 | 11.064 | 10 | 50 | MISS T_svc | 1,241,912 | 55 | 0.115 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 205,375 | 4.107 | 10 | 50 | fits | 1,241,513 | 55 | 0.115 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 456,755 | 9.135 | 10 | 50 | fits | 1,168,537 | 76 | 0.103 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 481,424 | 9.628 | 10 | 50 | fits | 1,168,537 | 76 | 0.103 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 367,157 | 7.343 | 10 | 50 | fits | 1,053,925 | 59 | 0.108 |
| LINK_UP | `adp.link_up.if0` | 1,759,596 | 35.192 | 10 | 200 | MISS T_svc | 3,414,438 | 134 (11) | 0.097 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 572,192 | 11.444 | 10 | 200 | MISS T_svc | 1,034,266 | 58 (39) | 0.107 |
| LINK_DOWN | `adp.link_down.if0` | 1,108,281 | 22.166 | 10 | 200 | MISS T_svc | 1,060,323 | 24 (9) | 0.080 |
| LINK_UP | `adp.link_up.if0` | 1,759,596 | 35.192 | 10 | 200 | MISS T_svc | 3,414,438 | 134 (11) | 0.097 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 572,192 | 11.444 | 10 | 200 | MISS T_svc | 1,034,266 | 58 (39) | 0.107 |
| GM_CHANGE | `adp.gm_change.if0` | 411,010 | 8.220 | 10 | 200 | fits | 727,675 | 24 (11) | 0.109 |
| LINK_UP | `adp.link_up.if0` | 1,759,596 | 35.192 | 10 | 200 | MISS T_svc | 3,414,438 | 134 (11) | 0.097 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 572,192 | 11.444 | 10 | 200 | MISS T_svc | 1,034,266 | 58 (39) | 0.107 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 721,199 | 14.424 | 10 | 200 | MISS T_svc | 809,982 | 43 (31) | 0.112 |
| LINK_UP | `adp.link_up.if0` | 1,759,596 | 35.192 | 10 | 200 | MISS T_svc | 3,414,438 | 134 (11) | 0.097 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 572,192 | 11.444 | 10 | 200 | MISS T_svc | 1,034,266 | 58 (39) | 0.107 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 721,199 | 14.424 | 10 | 200 | MISS T_svc | 809,982 | 43 (31) | 0.112 |
| set_name | `aecp_fanout.set_name.if0` | 2,057,109 | 41.142 | 10 | 24 | MISS ceiling | 2,132,683 | 628 | 0.049 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 2,184,871 | 43.697 | 10 | 24 | MISS ceiling | 3,079,386 | 372 | 0.071 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 1,648,086 | 32.962 | 10 | 24 | MISS ceiling | 2,661,585 | 343 | 0.063 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 1,842,009 | 36.840 | 10 | 24 | MISS ceiling | 2,800,027 | 349 | 0.067 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 1,669,311 | 33.386 | 10 | 24 | MISS ceiling | 2,705,237 | 383 | 0.062 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 1,900,795 | 38.016 | 10 | 24 | MISS ceiling | 2,901,171 | 389 | 0.065 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 1,649,238 | 32.985 | 10 | 24 | MISS ceiling | 2,638,154 | 349 | 0.066 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 2,337,747 | 46.755 | 10 | 24 | MISS ceiling | 3,313,025 | 460 | 0.069 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 1,613,746 | 32.275 | 10 | 24 | MISS ceiling | 2,613,410 | 394 | 0.062 |
| BIND_RX | `acmp.bind_rx.if0` | 509,431 | 10.189 | 10 | 20 | MISS T_svc | 1,933,710 | 128 (77) | 0.100 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 562,053 | 11.241 | 10 | 20 | MISS T_svc | 1,702,116 | 74 (32) | 0.074 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | - | - | - | - | no end: missing ['resp:1:4101'] | - | - | - |
| UNBIND_RX | `acmp.unbind_rx.if0` | 583,111 | 11.662 | 10 | 20 | MISS T_svc | 3,607,136 | 184 (50) | 0.053 |
| PROBE_TX | `acmp.probe_tx.if0` | - | - | - | - | no end: missing ['resp:1:4103'] | - | - | - |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 499,955 | 9.999 | 10 | 20 | fits | 2,897,410 | 163 (48) | 0.067 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 1,893,381 | 37.868 | 10 | 20 | MISS ceiling | 2,551,035 | 150 (48) | 0.065 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | - | - | - | - | no end: missing ['resp:1:4106'] | - | - | - |
| register_unsolicited | `aecp.register_unsolicited.if0` | 609,222 | 12.184 | 10 | 24 | MISS T_svc | 1,644,145 | 93 | 0.094 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 1,198,728 | 23.975 | 10 | 24 | MISS T_svc | 1,346,857 | 137 | 0.061 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 1,350,916 | 27.018 | 10 | 24 | MISS ceiling | 1,304,494 | 85 | 0.067 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 1,172,180 | 23.444 | 10 | 24 | MISS T_svc | 1,125,771 | 90 | 0.060 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 911,598 | 18.232 | 10 | 24 | MISS T_svc | 1,900,769 | 146 | 0.077 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 1,161,202 | 23.224 | 10 | 24 | MISS T_svc | 1,125,780 | 89 | 0.060 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 1,350,710 | 27.014 | 10 | 24 | MISS ceiling | 1,304,344 | 84 | 0.067 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 1,164,297 | 23.286 | 10 | 24 | MISS T_svc | 1,119,153 | 74 | 0.062 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 1,346,856 | 26.937 | 10 | 24 | MISS ceiling | 1,301,200 | 77 | 0.068 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 2,475,934 | 49.519 | 10 | 24 | MISS ceiling | 1,739,604 | 184 | 0.067 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 1,159,217 | 23.184 | 10 | 24 | MISS T_svc | 1,112,924 | 58 | 0.064 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 1,342,740 | 26.855 | 10 | 24 | MISS ceiling | 1,296,375 | 64 | 0.070 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 943,281 | 18.866 | 10 | 24 | MISS T_svc | 1,932,449 | 123 | 0.079 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 1,166,370 | 23.327 | 10 | 24 | MISS T_svc | 1,124,380 | 81 | 0.060 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 1,351,206 | 27.024 | 10 | 24 | MISS ceiling | 1,304,746 | 79 | 0.067 |
| get_configuration | `aecp.get_configuration.if0` | 1,145,408 | 22.908 | 10 | 24 | MISS T_svc | 1,098,758 | 53 | 0.065 |
| entity_available | `aecp.entity_available.if0` | 1,328,485 | 26.570 | 10 | 24 | MISS ceiling | 1,284,094 | 63 | 0.070 |
| get_name | `aecp.get_name.if0` | 1,165,881 | 23.318 | 10 | 24 | MISS T_svc | 1,121,493 | 70 | 0.063 |
| get_counters | `aecp.get_counters.if0` | 1,390,644 | 27.813 | 10 | 24 | MISS ceiling | 1,346,300 | 97 | 0.069 |
| get_avb_info | `aecp.get_avb_info.if0` | 1,152,743 | 23.055 | 10 | 24 | MISS T_svc | 1,106,176 | 53 | 0.064 |
| unknown_command | `aecp.unknown_command.if0` | 1,317,898 | 26.358 | 10 | 24 | MISS ceiling | 1,273,526 | 59 | 0.070 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 1,085,497 | 21.710 | 10 | 24 | MISS T_svc | 1,041,137 | 57 | 0.080 |
| set_name | `aecp.set_name.if0` | 1,551,501 | 31.030 | 10 | 24 | MISS ceiling | 1,692,781 | 139 | 0.066 |
| lock_entity | `aecp.lock_entity.if0` | 903,872 | 18.077 | 10 | 24 | MISS T_svc | 1,866,925 | 103 | 0.076 |
| unlock_entity | `aecp.unlock_entity.if0` | 1,515,689 | 30.314 | 10 | 24 | MISS ceiling | 1,430,177 | 89 | 0.071 |
| LINK_UP | `fixture.link_up.if0` | 1,759,596 | 35.192 | 10 | 200 | MISS T_svc | 3,414,438 | 134 (11) | 0.097 |
| malformed MRPDU discard | `fixture.malformed.if0` | 1,560,911 | 31.218 | 10 | 18 | MISS ceiling | 1,067,719 | 40 | 0.121 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | - | - | - | - | no end: no notification to ['0a0b0c0d0e0f0001@if0'] | - | - | - |
| LINK_DOWN | `fixture.link_down.if0` | 1,959,011 | 39.180 | 10 | 200 | MISS T_svc | 3,330,536 | 143 (9) | 0.094 |
| BIND_RX | `fixture.bind_rx.if0` | 1,426,313 | 28.526 | 10 | 20 | MISS ceiling | 3,330,536 | 143 (77) | 0.094 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 1,080,520 | 21.610 | 10 | 20 | MISS ceiling | 2,730,698 | 139 (35) | 0.054 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 339,642 | 6.793 | 10 | 20 | fits | 2,463,053 | 100 (29) | 0.068 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 2,859,379 | 57.188 | 10 | 200 | MISS T_svc | 2,698,975 | 280 | 0.071 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 2,859,379 | 57.188 | 10 | 200 | MISS T_svc | 2,698,975 | 280 | 0.071 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 2,859,244 | 57.185 | 10 | 20 | MISS ceiling | 2,698,975 | 280 | 0.071 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 2,859,244 | 57.185 | 10 | 20 | MISS ceiling | 2,698,975 | 280 | 0.071 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 2,859,347 | 57.187 | 10 | 24 | MISS ceiling | 2,698,975 | 280 | 0.071 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 2,859,347 | 57.187 | 10 | 24 | MISS ceiling | 2,698,975 | 280 | 0.071 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 2,859,314 | 57.186 | 10 | 50 | MISS ceiling | 2,698,975 | 280 | 0.071 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 2,859,314 | 57.186 | 10 | 50 | MISS ceiling | 2,698,975 | 280 | 0.071 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 11,422,188 | 228.444 | 10 | 18 | MISS ceiling | 1,872,008 | 73 | 0.086 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 11,422,188 | 228.444 | 10 | 18 | MISS ceiling | 1,872,008 | 73 | 0.086 |

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
