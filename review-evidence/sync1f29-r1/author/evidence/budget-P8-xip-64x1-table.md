### 8x8

104 of 116 paths and 143 of 169 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 23.420 (52.592) | MISS ceiling | 0 acmp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 45.490 (166.669) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 50.616 (166.669) | MISS ceiling | 1 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 79.581 (131.442) | MISS ceiling | 2 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 83.840 (131.442) | MISS ceiling | 3 adp | 1 | 1 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 8.076 (62.294) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 14.110 (63.927) | MISS T_svc | 1 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 19.663 (74.524) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 7.417 (97.701) | fits | 1 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 43.008 (115.791) | MISS ceiling | 6 events | 1 | 1 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 55.486 (115.940) | MISS ceiling | 4 events | 1 | 1 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 50.032 (128.644) | MISS ceiling | 3 events | 1 | 1 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 39.104 (128.634) | MISS ceiling | 6 events | 1 | 1 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 66.214 (163.250) | MISS ceiling | 7 events | 1 | 1 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 54.104 (106.057) | MISS ceiling | 7 events | 1 | 1 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 60.390 (108.268) | MISS ceiling | 8 events | 1 | 1 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 43.120 (149.216) | MISS ceiling | 5 events | 1 | 1 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 59.439 (127.795) | MISS ceiling | 9 events | 1 | 1 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 42.489 (113.689) | MISS ceiling | 4 events | 1 | 1 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 46.668 (109.722) | MISS ceiling | 6 events | 1 | 1 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 11.390 (71.232) | MISS T_svc | 1 acmp | 1 | 1 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 7.249 (22.709) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 8.026 (22.709) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 2.929 (22.725) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 3.932 (22.725) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 2.744 (61.540) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 38.983 (61.540) | MISS T_svc | 0 events | 1 | 1 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 6.947 (72.381) | fits | 1 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 14.637 (72.381) | MISS T_svc | 1 events | 5 | 5 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 14.167 (26.976) | MISS T_svc | 1 events | 1 | 1 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 7.172 (26.976) | fits | 2 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 3.936 (31.276) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 3.240 (31.276) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 18.237 (38.238) | MISS T_svc | 0 aecp | 1 | 1 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 18.178 (38.178) | MISS T_svc | 0 aecp | 1 | 1 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 38.833 (59.227) | MISS ceiling | 0 aecp | 1 | 1 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 15.264 (34.873) | MISS T_svc | 0 aecp | 1 | 1 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 14.996 (34.604) | MISS T_svc | 0 aecp | 1 | 1 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 30.649 (90.983) | MISS ceiling | 0 aecp | 1 | 1 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 19.281 (39.282) | MISS T_svc | 0 aecp | 1 | 1 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 39.688 (60.080) | MISS ceiling | 0 aecp | 1 | 1 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 18.571 (38.571) | MISS T_svc | 0 aecp | 1 | 1 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 18.649 (38.650) | MISS T_svc | 0 aecp | 1 | 1 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 39.047 (58.829) | MISS ceiling | 0 aecp | 1 | 1 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 22.234 (46.156) | MISS T_svc | 0 aecp | 1 | 1 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 17.065 (37.065) | MISS T_svc | 0 aecp | 1 | 1 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 17.041 (37.042) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 19.760 (39.675) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 19.487 (39.488) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 29.696 (49.697) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 20.999 (70.668) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 62.484 (122.987) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 34.578 (94.911) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 45.941 (66.334) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 18.960 (38.568) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 18.488 (38.488) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 18.701 (38.702) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 62.598 (123.598) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 28.400 (48.401) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 18.784 (38.785) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 39.172 (59.565) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 35.601 (55.995) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 19.090 (38.698) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 20.501 (70.170) | MISS T_svc | 0 aecp | 1 | 1 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 30.193 (49.596) | MISS ceiling | 0 aecp | 1 | 1 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 18.934 (36.973) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 22.173 (47.732) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 41.254 (66.522) | MISS ceiling | 0 aecp | 1 | 1 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 14.733 (34.341) | MISS T_svc | 0 aecp | 1 | 1 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 17.832 (37.832) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 38.880 (57.647) | MISS ceiling | 0 aecp | 1 | 1 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 29.718 (48.436) | MISS ceiling | 0 aecp | 1 | 1 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 93.669 (113.331) | MISS ceiling | 0 aecp | 1 | 1 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 113.624 (132.453) | MISS ceiling | 0 aecp | 1 | 1 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 98.110 (114.987) | MISS ceiling | 0 aecp | 1 | 1 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 101.822 (121.138) | MISS ceiling | 0 aecp | 1 | 1 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 94.098 (112.956) | MISS ceiling | 0 aecp | 2 | 2 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 147.935 (292.784) | MISS ceiling | 0 aecp | 2 | 2 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 99.445 (122.887) | MISS ceiling | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 101.626 (122.758) | MISS ceiling | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 92.130 (112.558) | MISS ceiling | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 97.337 (117.248) | MISS ceiling | 0 aecp | 1 | 1 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 120.279 (140.191) | MISS ceiling | 0 aecp | 1 | 1 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 425.242 (454.929) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 240.120 (369.607) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 369.919 (439.410) | MISS ceiling | 8 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 137.039 (240.522) | MISS T_svc | 16 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 511.540 (562.853) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 691.214 (742.529) | MISS ceiling | 11 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 16.809 (51.734) | MISS T_svc | 0 events | 1 | 1 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 11.512 (31.562) | MISS T_svc | 1 events | 1 | 1 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 18.149 (56.921) | MISS T_svc | 0 maap | 1 | 1 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 14.570 (29.084) | MISS T_svc | 0 maap | 1 | 1 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 12.570 (46.790) | MISS T_svc | 1 events | 1 | 1 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 10.440 (50.615) | MISS T_svc | 1 events | 1 | 1 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 16.357 (51.734) | MISS T_svc | 0 events | 1 | 1 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 11.061 (31.562) | MISS T_svc | 1 events | 1 | 1 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 13.356 (53.939) | MISS T_svc | 1 events | 2 | 2 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 10.860 (61.798) | MISS T_svc | 0 events | 2 | 1 |
| ACMP record released under the composed load, first | 0 | `backlog-owed.service.acmp.first.if0` (backlog-owed) | 83.705 | MISS ceiling | 0 acmp | 4 | 4 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 454.936 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog-owed.service.adp.first.if0` (backlog-owed) | 83.748 | MISS T_svc | 0 adp | 4 | 4 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 413.251 | MISS ceiling | 8 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 306.037 | MISS ceiling | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 83.741 | MISS ceiling | 0 aecp | 4 | 4 |
| AECP record released under the composed load, last | 1 | `backlog-adp-refill.service.aecp.last.if1` (backlog-adp-refill) | at least 909.909 | STARVED: never released | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog-owed.service.maap.first.if0` (backlog-owed) | 83.731 | MISS ceiling | 0 maap | 4 | 4 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 317.830 | MISS ceiling | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 909.904 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | at least 909.884 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 51.117 (71.066) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 62.017 (78.202) | MISS ceiling | 0 srp | 1 | 1 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 44.990 (70.423) | MISS ceiling | 0 srp | 1 | 1 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 56.796 (111.858) | MISS ceiling | 1 srp | 1 | 1 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 38.013 (46.790) | MISS ceiling | 1 events | 1 | 1 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 38.415 (57.839) | MISS ceiling | 0 events | 1 | 1 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 800.001 | 13 | 5,095,690 (101.914) | no | {'aecp': 2, 'srp': 32} |
| backlog-adp | 740.173 | 11 | 5,460,319 (109.206) | no | {'aecp': 5, 'srp': 32} |
| backlog-adp-refill | 909.921 | 14 | 5,209,608 (104.192) | no | {'aecp': 2, 'srp': 32} |
| backlog-owed | 860.053 | 17 | 3,845,323 (76.906) | no | {'srp': 32} |

Composed maximum over the 4 backlog windows: at least 5,460,319 CPU cycles (109.206 ms), backlog-adp, a lower bound (load unreleased in backlog, backlog-adp, backlog-adp-refill, backlog-owed).
Over the windows that released their whole load only: none.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 2,156,004 | 43.120 | 10 | 20 | MISS ceiling | 4,349,640 | 314 (14) | 0.034 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 2,971,963 | 59.439 | 10 | 20 | MISS ceiling | 1,216,184 | 46 (14) | 0.064 |
| LINK_UP | `adp.link_up.if0` | 347,331 | 6.947 | 10 | 200 | fits | 3,619,053 | 321 (11) | 0.039 |
| LINK_UP | `adp.link_up.if1` | 731,841 | 14.637 | 10 | 200 | MISS T_svc | 3,619,053 | 321 (11) | 0.039 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 196,786 | 3.936 | 10 | 200 | fits | 1,563,812 | 101 (39) | 0.067 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 162,025 | 3.240 | 10 | 200 | fits | 1,563,812 | 101 (39) | 0.067 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 708,366 | 14.167 | 10 | 200 | MISS T_svc | 329,403 | 24 (11) | 0.102 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 358,614 | 7.172 | 10 | 200 | fits | 329,403 | 24 (11) | 0.102 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 628,517 | 12.570 | 10 | 50 | MISS T_svc | 2,339,520 | 172 | 0.043 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 667,787 | 13.356 | 10 | 50 | MISS T_svc | 1,504,216 | 56 | 0.069 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 665,668 | 13.313 | 10 | 50 | MISS T_svc | 1,504,126 | 56 | 0.069 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 817,859 | 16.357 | 10 | 50 | MISS T_svc | 1,569,581 | 83 | 0.067 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 840,434 | 16.809 | 10 | 50 | MISS T_svc | 1,569,581 | 83 | 0.067 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 907,459 | 18.149 | 10 | 50 | MISS T_svc | 1,276,457 | 59 | 0.065 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 522,010 | 10.440 | 10 | 50 | MISS T_svc | 2,530,770 | 178 | 0.044 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 410,793 | 8.216 | 10 | 50 | fits | 1,505,455 | 56 | 0.068 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 542,990 | 10.860 | 10 | 50 | MISS T_svc | 3,089,923 | 272 | 0.033 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 553,031 | 11.061 | 10 | 50 | MISS T_svc | 1,578,088 | 82 | 0.066 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 575,606 | 11.512 | 10 | 50 | MISS T_svc | 1,578,088 | 82 | 0.066 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 728,502 | 14.570 | 10 | 50 | MISS T_svc | 1,454,183 | 66 | 0.065 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 1,955,185 | 39.104 | 10 | 20 | MISS ceiling | 3,310,883 | 115 (35) | 0.042 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 3,310,709 | 66.214 | 10 | 20 | MISS ceiling | 4,851,628 | 331 (35) | 0.031 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 2,705,203 | 54.104 | 10 | 20 | MISS ceiling | 2,772,140 | 97 (14) | 0.051 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 3,019,478 | 60.390 | 10 | 20 | MISS ceiling | 2,641,271 | 75 (14) | 0.049 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 2,124,430 | 42.489 | 10 | 20 | MISS ceiling | 2,624,561 | 76 (14) | 0.050 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 2,333,389 | 46.668 | 10 | 20 | MISS ceiling | 2,861,523 | 101 (14) | 0.047 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 2,150,424 | 43.008 | 10 | 20 | MISS ceiling | 2,731,921 | 98 (35) | 0.050 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 2,774,296 | 55.486 | 10 | 20 | MISS ceiling | 2,739,034 | 98 (35) | 0.050 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 1,900,654 | 38.013 | 10 | 18 | MISS ceiling | 2,339,520 | 172 | 0.043 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 1,920,733 | 38.415 | 10 | 18 | MISS ceiling | 2,891,959 | 190 | 0.048 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 3,100,838 | 62.017 | 10 | 18 | MISS ceiling | 1,872,497 | 47 | 0.071 |
| malformed MRPDU discard | `srp.malformed.if0` | 2,249,510 | 44.990 | 10 | 18 | MISS ceiling | 1,648,672 | 53 | 0.063 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 2,555,840 | 51.117 | 210 | 218 | fits | 3,553,278 | 160 | 0.048 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | - | - | - | - | no end: missing ['pass_end:4'] | - | - | - |
| malformed MRPDU discard | `srp.malformed.if1` | 2,839,792 | 56.796 | 10 | 18 | MISS ceiling | 2,492,707 | 65 | 0.069 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | - | - | - | - | no end: missing ['tx:4'] | - | - | - |
| an event behind 15 others | `backlog.event.if0` | 6,851,951 | 137.039 | 10 | 200 | MISS T_svc | 5,095,690 | 377 | 0.052 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 21,262,090 | 425.242 | 10 | 20 | MISS ceiling | 3,188,209 | 260 | 0.048 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 4,159,741 | 83.195 | 10 | 200 | MISS T_svc | 4,376,329 | 394 | 0.048 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 15,301,836 | 306.037 | 10 | 200 | MISS ceiling | 3,492,609 | 328 | 0.049 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 4,157,612 | 83.152 | 10 | 20 | MISS ceiling | 4,376,329 | 394 | 0.048 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 22,527,318 | 450.546 | 10 | 20 | MISS ceiling | 3,188,209 | 260 | 0.048 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 4,159,404 | 83.188 | 10 | 24 | MISS ceiling | 4,376,329 | 394 | 0.048 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 39,999,132 | 799.983 | 10 | 24 | STARVED: never released | 0 | - | 0.000 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 4,158,884 | 83.178 | 10 | 50 | MISS ceiling | 4,376,329 | 394 | 0.048 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 15,301,088 | 306.022 | 10 | 50 | MISS ceiling | 3,492,609 | 328 | 0.049 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 39,998,872 | 799.977 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 39,997,865 | 799.957 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 12,006,016 | 240.120 | 10 | 20 | MISS ceiling | 5,460,319 | 579 | 0.034 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 3,873,798 | 77.476 | 10 | 200 | MISS T_svc | 3,184,013 | 397 | 0.042 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 15,889,659 | 317.793 | 10 | 200 | MISS ceiling | 5,460,319 | 579 | 0.034 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 3,874,254 | 77.485 | 10 | 20 | MISS ceiling | 3,184,013 | 397 | 0.042 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 22,746,814 | 454.936 | 10 | 20 | MISS ceiling | 3,500,578 | 269 | 0.045 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 3,876,046 | 77.521 | 10 | 24 | MISS ceiling | 3,184,013 | 397 | 0.042 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 37,008,081 | 740.162 | 10 | 24 | STARVED: never released | 0 | - | 0.000 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 3,875,526 | 77.511 | 10 | 50 | MISS ceiling | 3,184,013 | 397 | 0.042 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 15,891,497 | 317.830 | 10 | 50 | MISS ceiling | 5,460,319 | 579 | 0.034 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 37,007,821 | 740.156 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 37,006,814 | 740.136 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 18,495,944 | 369.919 | 10 | 20 | MISS ceiling | 3,616,115 | 301 | 0.043 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 3,873,798 | 77.476 | 10 | 200 | MISS T_svc | 3,184,013 | 397 | 0.042 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 20,662,527 | 413.251 | 10 | 200 | MISS ceiling | 3,616,115 | 301 | 0.043 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 3,874,254 | 77.485 | 10 | 20 | MISS ceiling | 3,184,013 | 397 | 0.042 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 22,660,333 | 453.207 | 10 | 20 | MISS ceiling | 3,616,115 | 301 | 0.043 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 3,876,046 | 77.521 | 10 | 24 | MISS ceiling | 3,184,013 | 397 | 0.042 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 45,495,467 | 909.909 | 10 | 24 | STARVED: never released | 0 | - | 0.000 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 3,875,526 | 77.511 | 10 | 50 | MISS ceiling | 3,184,013 | 397 | 0.042 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 15,640,786 | 312.816 | 10 | 50 | MISS ceiling | 5,209,608 | 572 | 0.034 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 45,495,207 | 909.904 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 45,494,200 | 909.884 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 25,577,024 | 511.540 | 10 | 20 | MISS ceiling | 2,815,340 | 195 | 0.053 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 28,042,714 | 560.854 | 10 | 20 | MISS ceiling | 2,465,722 | 184 | 0.050 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 30,156,467 | 603.129 | 10 | 20 | MISS ceiling | 2,113,790 | 172 | 0.047 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 32,270,557 | 645.411 | 10 | 20 | MISS ceiling | 2,114,128 | 172 | 0.047 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 34,560,697 | 691.214 | 10 | 20 | MISS ceiling | 2,290,177 | 178 | 0.049 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 4,187,388 | 83.748 | 10 | 200 | MISS T_svc | 2,968,013 | 367 | 0.041 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 14,207,716 | 284.154 | 10 | 200 | MISS ceiling | 3,544,223 | 325 | 0.045 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 4,185,259 | 83.705 | 10 | 20 | MISS ceiling | 2,968,013 | 367 | 0.041 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 20,737,104 | 414.742 | 10 | 20 | MISS ceiling | 3,263,299 | 238 | 0.044 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 4,187,051 | 83.741 | 10 | 24 | MISS ceiling | 2,968,013 | 367 | 0.041 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 42,900,335 | 858.007 | 10 | 24 | MISS ceiling | 1,753,880 | 144 | 0.049 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 4,186,531 | 83.731 | 10 | 50 | MISS ceiling | 2,968,013 | 367 | 0.041 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 14,206,968 | 284.139 | 10 | 50 | MISS ceiling | 3,544,223 | 325 | 0.045 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 43,001,456 | 860.029 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 43,000,448 | 860.009 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 3,979,061 | 79.581 | 10 | 20 | MISS ceiling | 3,743,158 | 202 (29) | 0.041 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 4,191,986 | 83.840 | 10 | 20 | MISS ceiling | 3,743,158 | 202 (29) | 0.041 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 2,274,505 | 45.490 | 10 | 20 | MISS ceiling | 5,234,804 | 367 (35) | 0.032 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 2,530,786 | 50.616 | 10 | 20 | MISS ceiling | 5,234,804 | 367 (35) | 0.032 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 2,501,581 | 50.032 | 10 | 20 | MISS ceiling | 3,293,311 | 115 (12) | 0.041 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | - | - | - | - | no start: no deadline:3 after the mark | - | - | - |
| LINK_UP | `adp.link_up.if0` | 347,331 | 6.947 | 10 | 200 | fits | 3,619,053 | 321 (11) | 0.039 |
| LINK_UP | `adp.link_up.if1` | 731,841 | 14.637 | 10 | 200 | MISS T_svc | 3,619,053 | 321 (11) | 0.039 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 196,786 | 3.936 | 10 | 200 | fits | 1,563,812 | 101 (39) | 0.067 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 162,025 | 3.240 | 10 | 200 | fits | 1,563,812 | 101 (39) | 0.067 |
| LINK_DOWN | `adp.link_down.if0` | 137,195 | 2.744 | 10 | 200 | fits | 3,077,001 | 40 (9) | 0.063 |
| LINK_DOWN | `adp.link_down.if1` | 1,949,173 | 38.983 | 10 | 200 | MISS T_svc | 3,077,001 | 40 (9) | 0.063 |
| LINK_UP | `adp.link_up.if0` | 347,331 | 6.947 | 10 | 200 | fits | 3,619,053 | 321 (11) | 0.039 |
| LINK_UP | `adp.link_up.if1` | 731,841 | 14.637 | 10 | 200 | MISS T_svc | 3,619,053 | 321 (11) | 0.039 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 196,786 | 3.936 | 10 | 200 | fits | 1,563,812 | 101 (39) | 0.067 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 162,025 | 3.240 | 10 | 200 | fits | 1,563,812 | 101 (39) | 0.067 |
| GM_CHANGE | `adp.gm_change.if0` | 146,458 | 2.929 | 10 | 200 | fits | 1,136,246 | 40 (11) | 0.065 |
| GM_CHANGE | `adp.gm_change.if1` | 196,575 | 3.932 | 10 | 200 | fits | 1,136,246 | 40 (11) | 0.065 |
| LINK_UP | `adp.link_up.if0` | 347,331 | 6.947 | 10 | 200 | fits | 3,619,053 | 321 (11) | 0.039 |
| LINK_UP | `adp.link_up.if1` | 731,841 | 14.637 | 10 | 200 | MISS T_svc | 3,619,053 | 321 (11) | 0.039 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 196,786 | 3.936 | 10 | 200 | fits | 1,563,812 | 101 (39) | 0.067 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 162,025 | 3.240 | 10 | 200 | fits | 1,563,812 | 101 (39) | 0.067 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 362,434 | 7.249 | 10 | 200 | fits | 1,135,436 | 79 (31) | 0.061 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 401,301 | 8.026 | 10 | 200 | fits | 1,135,436 | 79 (31) | 0.061 |
| LINK_UP | `adp.link_up.if0` | 347,331 | 6.947 | 10 | 200 | fits | 3,619,053 | 321 (11) | 0.039 |
| LINK_UP | `adp.link_up.if1` | 731,841 | 14.637 | 10 | 200 | MISS T_svc | 3,619,053 | 321 (11) | 0.039 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 196,786 | 3.936 | 10 | 200 | fits | 1,563,812 | 101 (39) | 0.067 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 162,025 | 3.240 | 10 | 200 | fits | 1,563,812 | 101 (39) | 0.067 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 362,434 | 7.249 | 10 | 200 | fits | 1,096,612 | 51 (31) | 0.062 |
| set_name | `aecp_fanout.set_name.if0` | 4,972,256 | 99.445 | 10 | 24 | MISS ceiling | 4,906,519 | 1190 | 0.055 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 4,905,492 | 98.110 | 10 | 24 | MISS ceiling | 5,749,354 | 662 | 0.059 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 4,670,512 | 93.410 | 10 | 24 | MISS ceiling | 5,705,367 | 629 | 0.056 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 4,704,900 | 94.098 | 10 | 24 | MISS ceiling | 5,647,786 | 629 | 0.058 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 4,606,503 | 92.130 | 10 | 24 | MISS ceiling | 5,627,916 | 640 | 0.060 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 4,683,431 | 93.669 | 10 | 24 | MISS ceiling | 5,666,552 | 728 | 0.057 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 4,866,839 | 97.337 | 10 | 24 | MISS ceiling | 5,862,421 | 728 | 0.057 |
| set_name | `aecp_fanout.set_name.if1` | 5,081,287 | 101.626 | 10 | 24 | MISS ceiling | 6,137,889 | 1181 | 0.048 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 5,091,085 | 101.822 | 10 | 24 | MISS ceiling | 6,056,913 | 662 | 0.059 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 5,201,650 | 104.033 | 10 | 24 | MISS ceiling | 7,719,862 | 845 | 0.043 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 7,396,769 | 147.935 | 10 | 24 | MISS ceiling | 6,919,317 | 649 | 0.051 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 5,681,189 | 113.624 | 10 | 24 | MISS ceiling | 6,622,627 | 728 | 0.048 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 6,013,935 | 120.279 | 10 | 24 | MISS ceiling | 7,009,575 | 728 | 0.046 |
| BIND_RX | `acmp.bind_rx.if0` | 1,170,997 | 23.420 | 10 | 20 | MISS ceiling | 1,611,484 | 95 (77) | 0.053 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 983,164 | 19.663 | 10 | 20 | MISS T_svc | 2,114,733 | 91 (32) | 0.049 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | - | - | - | - | no end: missing ['resp:1:4101'] | - | - | - |
| UNBIND_RX | `acmp.unbind_rx.if0` | 569,484 | 11.390 | 10 | 20 | MISS T_svc | 3,561,613 | 227 (50) | 0.047 |
| PROBE_TX | `acmp.probe_tx.if0` | - | - | - | - | no end: missing ['resp:1:4103'] | - | - | - |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 705,481 | 14.110 | 10 | 20 | MISS T_svc | 3,196,346 | 164 (48) | 0.045 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | - | - | - | - | no end: missing ['resp:1:4105'] | - | - | - |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 403,778 | 8.076 | 10 | 20 | fits | 3,114,725 | 163 (48) | 0.044 |
| BIND_RX | `acmp.bind_rx.if1` | - | - | - | - | no end: missing ['resp:1:4107', 'acmp_cmd:1:PROBE_TX', 'arm:3', 'pub:710'] | - | - | - |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 370,851 | 7.417 | 10 | 20 | fits | 4,885,035 | 387 (32) | 0.033 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | - | - | - | - | no end: missing ['resp:1:4108'] | - | - | - |
| UNBIND_RX | `acmp.unbind_rx.if1` | - | - | - | - | no end: missing ['resp:1:4109', 'tmr:3'] | - | - | - |
| PROBE_TX | `acmp.probe_tx.if1` | - | - | - | - | no end: missing ['resp:1:410a'] | - | - | - |
| GET_TX_STATE | `acmp.get_tx_state.if1` | - | - | - | - | no end: missing ['resp:1:410b'] | - | - | - |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | - | - | - | - | no end: missing ['resp:1:410c'] | - | - | - |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | - | - | - | - | no end: missing ['resp:1:410d'] | - | - | - |
| register_unsolicited | `aecp.register_unsolicited.if0` | 1,509,674 | 30.193 | 10 | 24 | MISS ceiling | 1,461,686 | 61 | 0.060 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 987,977 | 19.760 | 10 | 24 | MISS T_svc | 1,983,750 | 153 | 0.053 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 1,484,805 | 29.696 | 10 | 24 | MISS ceiling | 2,484,834 | 181 | 0.060 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 935,063 | 18.701 | 10 | 24 | MISS T_svc | 1,935,095 | 112 | 0.054 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 1,780,074 | 35.601 | 10 | 24 | MISS ceiling | 1,565,335 | 97 | 0.051 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 954,485 | 19.090 | 10 | 24 | MISS T_svc | 1,934,876 | 111 | 0.054 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 1,025,070 | 20.501 | 10 | 24 | MISS T_svc | 3,508,497 | 316 | 0.032 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 3,124,224 | 62.484 | 10 | 24 | MISS ceiling | 2,640,861 | 119 | 0.061 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 1,728,912 | 34.578 | 10 | 24 | MISS ceiling | 2,104,685 | 99 | 0.057 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 2,297,035 | 45.941 | 10 | 24 | MISS ceiling | 2,082,449 | 208 | 0.052 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 947,991 | 18.960 | 10 | 24 | MISS T_svc | 1,928,382 | 80 | 0.056 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 924,376 | 18.488 | 10 | 24 | MISS T_svc | 1,924,408 | 80 | 0.056 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 1,420,016 | 28.400 | 10 | 24 | MISS ceiling | 2,420,048 | 131 | 0.058 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 939,217 | 18.784 | 10 | 24 | MISS T_svc | 1,939,249 | 103 | 0.054 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 1,958,589 | 39.172 | 10 | 24 | MISS ceiling | 1,743,698 | 91 | 0.053 |
| get_configuration | `aecp.get_configuration.if0` | 749,793 | 14.996 | 10 | 24 | MISS T_svc | 1,730,184 | 69 | 0.055 |
| entity_available | `aecp.entity_available.if0` | 911,850 | 18.237 | 10 | 24 | MISS T_svc | 1,911,885 | 79 | 0.057 |
| get_name | `aecp.get_name.if0` | 928,531 | 18.571 | 10 | 24 | MISS T_svc | 1,928,563 | 92 | 0.056 |
| get_counters | `aecp.get_counters.if0` | 964,060 | 19.281 | 10 | 24 | MISS T_svc | 1,964,092 | 113 | 0.056 |
| get_avb_info | `aecp.get_avb_info.if0` | 1,941,655 | 38.833 | 10 | 24 | MISS ceiling | 1,727,116 | 67 | 0.054 |
| unknown_command | `aecp.unknown_command.if0` | 736,660 | 14.733 | 10 | 24 | MISS T_svc | 1,717,051 | 69 | 0.055 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 853,234 | 17.065 | 10 | 24 | MISS T_svc | 1,853,266 | 79 | 0.063 |
| set_name | `aecp.set_name.if0` | 1,108,663 | 22.173 | 10 | 24 | MISS T_svc | 2,386,591 | 175 | 0.044 |
| lock_entity | `aecp.lock_entity.if0` | 1,952,368 | 39.047 | 10 | 24 | MISS ceiling | 2,941,460 | 183 | 0.055 |
| unlock_entity | `aecp.unlock_entity.if0` | 1,943,982 | 38.880 | 10 | 24 | MISS ceiling | 2,882,342 | 183 | 0.060 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 946,683 | 18.934 | 10 | 24 | MISS T_svc | 1,848,668 | 73 | 0.061 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 974,354 | 19.487 | 10 | 24 | MISS T_svc | 1,974,386 | 151 | 0.052 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 1,049,957 | 20.999 | 10 | 24 | MISS T_svc | 3,533,384 | 315 | 0.033 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 3,129,893 | 62.598 | 10 | 24 | MISS ceiling | 2,646,530 | 133 | 0.060 |
| get_configuration | `aecp.get_configuration.if1` | 1,532,471 | 30.649 | 10 | 24 | MISS ceiling | 1,902,621 | 73 | 0.057 |
| entity_available | `aecp.entity_available.if1` | 908,876 | 18.178 | 10 | 24 | MISS T_svc | 1,908,908 | 77 | 0.056 |
| get_name | `aecp.get_name.if1` | 932,443 | 18.649 | 10 | 24 | MISS T_svc | 1,932,475 | 90 | 0.056 |
| get_counters | `aecp.get_counters.if1` | 1,984,377 | 39.688 | 10 | 24 | MISS ceiling | 1,768,719 | 103 | 0.055 |
| get_avb_info | `aecp.get_avb_info.if1` | 763,198 | 15.264 | 10 | 24 | MISS T_svc | 1,743,655 | 67 | 0.053 |
| unknown_command | `aecp.unknown_command.if1` | 891,591 | 17.832 | 10 | 24 | MISS T_svc | 1,891,623 | 73 | 0.056 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 852,060 | 17.041 | 10 | 24 | MISS T_svc | 1,852,092 | 77 | 0.063 |
| set_name | `aecp.set_name.if1` | 2,062,681 | 41.254 | 10 | 24 | MISS ceiling | 2,090,325 | 160 | 0.044 |
| lock_entity | `aecp.lock_entity.if1` | 1,111,710 | 22.234 | 10 | 24 | MISS T_svc | 2,307,812 | 135 | 0.051 |
| unlock_entity | `aecp.unlock_entity.if1` | 1,485,893 | 29.718 | 10 | 24 | MISS ceiling | 2,421,810 | 141 | 0.057 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `adp-advertise`: wait quiet TIMEOUT
- `adp-advertise`: wait quiet TIMEOUT
- `maap`: wait quiet TIMEOUT
- `maap`: wait quiet TIMEOUT
- `maap`: wait quiet TIMEOUT
- `maap`: wait quiet TIMEOUT
- `maap`: wait quiet TIMEOUT
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
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
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
- `aecp-fanout`: wait tx TIMEOUT
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
- `aecp-fanout`: wait tx TIMEOUT
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
- `acmp-cmd`: wait tx TIMEOUT
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
- `acmp-cmd`: wait tx TIMEOUT
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
