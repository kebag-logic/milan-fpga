### 8x8

106 of 116 paths and 154 of 169 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 14.406 (32.010) | MISS T_svc | 0 acmp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 41.943 (134.104) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 47.037 (134.104) | MISS ceiling | 1 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 78.921 (130.719) | MISS ceiling | 2 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 83.155 (130.719) | MISS ceiling | 3 adp | 1 | 1 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 7.621 (61.875) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 13.614 (63.498) | MISS T_svc | 1 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 16.881 (42.009) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 6.976 (97.077) | fits | 1 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 38.403 (126.342) | MISS ceiling | 5 events | 1 | 1 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 52.773 (115.144) | MISS ceiling | 3 events | 1 | 1 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 58.313 (152.826) | MISS ceiling | 8 events | 1 | 1 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 37.206 (127.803) | MISS ceiling | 6 events | 1 | 1 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 65.078 (162.457) | MISS ceiling | 5 events | 1 | 1 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 46.606 (102.686) | MISS ceiling | 5 events | 1 | 1 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 53.076 (125.100) | MISS ceiling | 7 events | 1 | 1 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 40.984 (127.236) | MISS ceiling | 5 events | 1 | 1 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 44.902 (88.449) | MISS ceiling | 5 events | 1 | 1 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 35.372 (113.359) | MISS ceiling | 5 events | 1 | 1 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 58.718 (119.665) | MISS ceiling | 4 events | 1 | 1 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 10.871 (70.713) | MISS T_svc | 1 acmp | 1 | 1 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 10.544 (42.772) | MISS T_svc | 0 adp | 2 | 2 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 11.316 (42.772) | MISS T_svc | 1 adp | 1 | 1 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 6.253 (42.780) | fits | 1 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 7.248 (42.780) | fits | 1 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 6.069 (81.460) | fits | 1 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 42.048 (81.460) | MISS T_svc | 1 events | 1 | 1 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 6.392 (71.903) | fits | 1 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 14.026 (71.903) | MISS T_svc | 1 events | 5 | 5 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 5.223 (10.471) | fits | 1 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 3.153 (10.471) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 11.623 (55.023) | MISS T_svc | 1 events | 5 | 5 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 10.871 (34.801) | MISS T_svc | 2 events | 5 | 5 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 34.759 (55.149) | MISS ceiling | 0 aecp | 1 | 1 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 17.907 (37.908) | MISS T_svc | 0 aecp | 1 | 1 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 18.152 (38.153) | MISS T_svc | 0 aecp | 1 | 1 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 18.131 (38.131) | MISS T_svc | 0 aecp | 1 | 1 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 17.850 (37.851) | MISS T_svc | 0 aecp | 1 | 1 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 30.223 (90.343) | MISS ceiling | 0 aecp | 1 | 1 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 19.008 (39.008) | MISS T_svc | 0 aecp | 1 | 1 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 19.378 (38.991) | MISS T_svc | 0 aecp | 1 | 1 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 18.699 (38.310) | MISS T_svc | 0 aecp | 1 | 1 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 35.180 (55.569) | MISS ceiling | 0 aecp | 1 | 1 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 27.618 (47.397) | MISS ceiling | 0 aecp | 1 | 1 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 25.392 (49.329) | MISS ceiling | 0 aecp | 1 | 1 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 17.179 (36.790) | MISS T_svc | 0 aecp | 1 | 1 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 33.576 (53.966) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 19.487 (39.403) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 22.752 (42.753) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 29.348 (49.349) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 40.993 (90.874) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 61.940 (122.691) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 30.251 (38.311) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 19.113 (39.113) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 18.303 (38.303) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 18.218 (38.219) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 38.702 (59.092) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 62.437 (118.913) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 54.304 (74.694) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 23.211 (38.518) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 18.484 (38.484) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 15.338 (34.949) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 18.423 (38.424) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 20.750 (70.241) | MISS T_svc | 0 aecp | 1 | 1 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 21.129 (29.030) | MISS T_svc | 0 aecp | 1 | 1 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 40.579 (58.634) | MISS ceiling | 0 aecp | 1 | 1 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 21.886 (47.411) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 20.882 (45.380) | MISS T_svc | 0 aecp | 1 | 1 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 34.371 (54.761) | MISS ceiling | 0 aecp | 1 | 1 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 17.575 (37.575) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 23.941 (42.714) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 29.375 (48.099) | MISS ceiling | 0 aecp | 1 | 1 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 92.865 (112.532) | MISS ceiling | 0 aecp | 1 | 1 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 117.839 (136.674) | MISS ceiling | 0 aecp | 1 | 1 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 97.186 (114.081) | MISS ceiling | 0 aecp | 1 | 1 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 103.258 (152.066) | MISS ceiling | 0 aecp | 1 | 1 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 93.295 (112.157) | MISS ceiling | 0 aecp | 2 | 2 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 130.354 (273.626) | MISS ceiling | 0 aecp | 2 | 2 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 98.583 (122.004) | MISS ceiling | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 100.810 (121.938) | MISS ceiling | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 91.334 (111.758) | MISS ceiling | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 96.473 (116.385) | MISS ceiling | 0 aecp | 1 | 1 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 111.514 (131.427) | MISS ceiling | 0 aecp | 1 | 1 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 437.261 (476.071) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 236.030 (365.140) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 368.290 (438.045) | MISS ceiling | 8 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 143.021 (265.128) | MISS T_svc | 16 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 507.778 (559.086) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 682.742 (734.053) | MISS ceiling | 11 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 13.335 (51.510) | MISS T_svc | 1 events | 1 | 1 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 17.641 (51.574) | MISS T_svc | 0 events | 1 | 1 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 14.294 (56.655) | MISS T_svc | 0 maap | 1 | 1 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 14.329 (56.724) | MISS T_svc | 0 maap | 1 | 1 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 11.976 (46.473) | MISS T_svc | 1 events | 1 | 1 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 10.224 (50.278) | MISS T_svc | 1 events | 1 | 1 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 12.887 (51.510) | MISS T_svc | 1 events | 1 | 1 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 17.192 (51.574) | MISS T_svc | 0 events | 1 | 1 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 9.059 (29.869) | fits | 1 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 12.386 (50.134) | MISS T_svc | 1 events | 2 | 2 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 90.953 | MISS ceiling | 0 acmp | 4 | 4 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 462.405 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 90.996 | MISS T_svc | 0 adp | 4 | 4 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 411.352 | MISS ceiling | 8 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 318.859 | MISS ceiling | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 90.989 | MISS ceiling | 0 aecp | 4 | 4 |
| AECP record released under the composed load, last | 1 | `backlog-adp-refill.service.aecp.last.if1` (backlog-adp-refill) | at least 908.280 | STARVED: never released | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 90.979 | MISS ceiling | 0 maap | 4 | 4 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 318.844 | MISS ceiling | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 908.275 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | at least 908.255 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 43.120 (66.797) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 33.611 (37.182) | MISS ceiling | 0 srp | 1 | 1 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 16.353 (32.742) | MISS T_svc | 0 srp | 1 | 1 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 55.913 (111.083) | MISS ceiling | 1 srp | 1 | 1 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 37.260 (46.473) | MISS ceiling | 1 events | 1 | 1 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 38.011 (57.439) | MISS ceiling | 0 events | 1 | 1 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 800.001 | 14 | 5,492,818 (109.856) | no | {'aecp': 2, 'srp': 32} |
| backlog-adp | 736.082 | 12 | 5,323,522 (106.470) | no | {'aecp': 5, 'srp': 32} |
| backlog-adp-refill | 908.292 | 14 | 5,078,783 (101.576) | no | {'aecp': 2, 'srp': 32} |
| backlog-owed | 860.053 | 17 | 3,819,515 (76.390) | no | {'srp': 32} |

Composed maximum over the 4 backlog windows: at least 5,492,818 CPU cycles (109.856 ms), backlog, a lower bound (load unreleased in backlog, backlog-adp, backlog-adp-refill, backlog-owed).
Over the windows that released their whole load only: none.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 2,049,209 | 40.984 | 10 | 20 | MISS ceiling | 3,270,277 | 115 (14) | 0.041 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 2,245,110 | 44.902 | 10 | 20 | MISS ceiling | 1,908,321 | 58 (14) | 0.060 |
| LINK_UP | `adp.link_up.if0` | 319,614 | 6.392 | 10 | 200 | fits | 3,595,134 | 322 (11) | 0.038 |
| LINK_UP | `adp.link_up.if1` | 701,317 | 14.026 | 10 | 200 | MISS T_svc | 3,595,134 | 322 (11) | 0.038 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 581,169 | 11.623 | 10 | 200 | MISS T_svc | 1,740,030 | 108 (39) | 0.069 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 543,559 | 10.871 | 10 | 200 | MISS T_svc | 1,740,030 | 108 (39) | 0.069 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 261,151 | 5.223 | 10 | 200 | fits | 523,540 | 30 (11) | 0.097 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 157,649 | 3.153 | 10 | 200 | fits | 523,540 | 30 (11) | 0.097 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 598,798 | 11.976 | 10 | 50 | MISS T_svc | 2,323,652 | 172 | 0.043 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 452,954 | 9.059 | 10 | 50 | fits | 1,493,450 | 56 | 0.069 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 327,383 | 6.548 | 10 | 50 | fits | 1,493,594 | 56 | 0.069 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 644,329 | 12.887 | 10 | 50 | MISS T_svc | 1,565,429 | 83 | 0.067 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 666,773 | 13.335 | 10 | 50 | MISS T_svc | 1,565,429 | 83 | 0.067 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 714,703 | 14.294 | 10 | 50 | MISS T_svc | 1,267,310 | 59 | 0.065 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 511,178 | 10.224 | 10 | 50 | MISS T_svc | 2,513,908 | 178 | 0.044 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 594,841 | 11.897 | 10 | 50 | MISS T_svc | 1,495,431 | 56 | 0.068 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 619,287 | 12.386 | 10 | 50 | MISS T_svc | 1,495,168 | 56 | 0.068 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 859,593 | 17.192 | 10 | 50 | MISS T_svc | 1,567,204 | 83 | 0.066 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 882,037 | 17.641 | 10 | 50 | MISS T_svc | 1,567,204 | 83 | 0.066 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 716,469 | 14.329 | 10 | 50 | MISS T_svc | 1,268,979 | 59 | 0.064 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 1,860,307 | 37.206 | 10 | 20 | MISS ceiling | 3,289,088 | 115 (35) | 0.042 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 3,253,910 | 65.078 | 10 | 20 | MISS ceiling | 4,833,773 | 331 (35) | 0.032 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 2,330,311 | 46.606 | 10 | 20 | MISS ceiling | 2,620,858 | 75 (14) | 0.049 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 2,653,815 | 53.076 | 10 | 20 | MISS ceiling | 3,634,123 | 149 (14) | 0.038 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 1,768,599 | 35.372 | 10 | 20 | MISS ceiling | 3,169,986 | 93 (14) | 0.041 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 2,935,879 | 58.718 | 10 | 20 | MISS ceiling | 2,813,288 | 101 (14) | 0.047 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 1,920,132 | 38.403 | 10 | 20 | MISS ceiling | 3,240,270 | 115 (35) | 0.041 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 2,638,657 | 52.773 | 10 | 20 | MISS ceiling | 2,720,388 | 98 (35) | 0.050 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 1,863,002 | 37.260 | 10 | 18 | MISS ceiling | 2,323,652 | 172 | 0.043 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 1,900,535 | 38.011 | 10 | 18 | MISS ceiling | 2,871,971 | 190 | 0.048 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 1,680,564 | 33.611 | 10 | 18 | MISS ceiling | 1,859,092 | 47 | 0.071 |
| malformed MRPDU discard | `srp.malformed.if0` | 817,670 | 16.353 | 10 | 18 | MISS T_svc | 1,637,106 | 53 | 0.063 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 2,155,981 | 43.120 | 210 | 218 | fits | 3,339,863 | 154 | 0.047 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | - | - | - | - | no end: missing ['pass_end:4'] | - | - | - |
| malformed MRPDU discard | `srp.malformed.if1` | 2,795,639 | 55.913 | 10 | 18 | MISS ceiling | 2,474,982 | 65 | 0.069 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | - | - | - | - | no end: missing ['tx:4'] | - | - | - |
| an event behind 15 others | `backlog.event.if0` | 7,151,072 | 143.021 | 10 | 200 | MISS T_svc | 5,492,818 | 377 | 0.053 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 21,863,027 | 437.261 | 10 | 20 | MISS ceiling | 3,166,768 | 260 | 0.048 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 4,549,795 | 90.996 | 10 | 200 | MISS T_svc | 2,690,503 | 388 | 0.043 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 15,942,931 | 318.859 | 10 | 200 | MISS ceiling | 3,367,602 | 328 | 0.048 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 4,547,666 | 90.953 | 10 | 20 | MISS ceiling | 2,690,503 | 388 | 0.043 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 23,120,235 | 462.405 | 10 | 20 | MISS ceiling | 3,166,768 | 260 | 0.048 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 4,549,458 | 90.989 | 10 | 24 | MISS ceiling | 2,690,503 | 388 | 0.043 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 39,999,132 | 799.983 | 10 | 24 | STARVED: never released | 0 | - | 0.000 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 4,548,938 | 90.979 | 10 | 50 | MISS ceiling | 2,690,503 | 388 | 0.043 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 15,942,183 | 318.844 | 10 | 50 | MISS ceiling | 3,367,602 | 328 | 0.048 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 39,998,872 | 799.977 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 39,997,865 | 799.957 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 11,801,475 | 236.030 | 10 | 20 | MISS ceiling | 5,323,522 | 579 | 0.033 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 3,825,800 | 76.516 | 10 | 200 | MISS T_svc | 3,162,728 | 397 | 0.042 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 15,661,151 | 313.223 | 10 | 200 | MISS ceiling | 5,323,522 | 579 | 0.033 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 3,826,256 | 76.525 | 10 | 20 | MISS ceiling | 3,162,728 | 397 | 0.042 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 22,492,419 | 449.848 | 10 | 20 | MISS ceiling | 3,349,185 | 269 | 0.045 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 3,828,049 | 76.561 | 10 | 24 | MISS ceiling | 3,162,728 | 397 | 0.042 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 36,803,541 | 736.071 | 10 | 24 | STARVED: never released | 0 | - | 0.000 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 3,827,529 | 76.551 | 10 | 50 | MISS ceiling | 3,162,728 | 397 | 0.042 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 15,662,989 | 313.260 | 10 | 50 | MISS ceiling | 5,323,522 | 579 | 0.033 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 36,803,281 | 736.066 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 36,802,273 | 736.045 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 18,414,482 | 368.290 | 10 | 20 | MISS ceiling | 3,618,623 | 301 | 0.043 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 3,825,800 | 76.516 | 10 | 200 | MISS T_svc | 3,162,728 | 397 | 0.042 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 20,567,580 | 411.352 | 10 | 200 | MISS ceiling | 3,618,623 | 301 | 0.043 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 3,826,256 | 76.525 | 10 | 20 | MISS ceiling | 3,162,728 | 397 | 0.042 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 22,565,386 | 451.308 | 10 | 20 | MISS ceiling | 3,618,623 | 301 | 0.043 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 3,828,049 | 76.561 | 10 | 24 | MISS ceiling | 3,162,728 | 397 | 0.042 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 45,414,006 | 908.280 | 10 | 24 | STARVED: never released | 0 | - | 0.000 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 3,827,529 | 76.551 | 10 | 50 | MISS ceiling | 3,162,728 | 397 | 0.042 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 15,418,250 | 308.365 | 10 | 50 | MISS ceiling | 5,078,783 | 572 | 0.033 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 45,413,746 | 908.275 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 45,412,738 | 908.255 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 25,388,917 | 507.778 | 10 | 20 | MISS ceiling | 2,796,035 | 195 | 0.053 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 27,663,336 | 553.267 | 10 | 20 | MISS ceiling | 2,274,451 | 178 | 0.049 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 29,763,063 | 595.261 | 10 | 20 | MISS ceiling | 2,099,764 | 172 | 0.047 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 32,037,252 | 640.745 | 10 | 20 | MISS ceiling | 2,274,227 | 178 | 0.049 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 34,137,107 | 682.742 | 10 | 20 | MISS ceiling | 2,099,892 | 172 | 0.047 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 4,143,455 | 82.869 | 10 | 200 | MISS T_svc | 2,948,367 | 367 | 0.041 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 14,097,026 | 281.941 | 10 | 200 | MISS ceiling | 3,520,376 | 325 | 0.045 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 4,141,326 | 82.827 | 10 | 20 | MISS ceiling | 2,948,367 | 367 | 0.041 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 20,582,589 | 411.652 | 10 | 20 | MISS ceiling | 3,241,913 | 238 | 0.044 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 4,143,118 | 82.862 | 10 | 24 | MISS ceiling | 2,948,367 | 367 | 0.041 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 42,420,435 | 848.409 | 10 | 24 | MISS ceiling | 1,741,946 | 144 | 0.049 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 4,142,598 | 82.852 | 10 | 50 | MISS ceiling | 2,948,367 | 367 | 0.041 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 14,096,278 | 281.926 | 10 | 50 | MISS ceiling | 3,520,376 | 325 | 0.045 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 43,001,456 | 860.029 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 43,000,448 | 860.009 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 3,946,075 | 78.921 | 10 | 20 | MISS ceiling | 3,725,994 | 202 (29) | 0.041 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 4,157,770 | 83.155 | 10 | 20 | MISS ceiling | 3,725,994 | 202 (29) | 0.041 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 2,097,136 | 41.943 | 10 | 20 | MISS ceiling | 3,626,031 | 151 (35) | 0.040 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 2,351,844 | 47.037 | 10 | 20 | MISS ceiling | 3,626,031 | 151 (35) | 0.040 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | - | - | - | - | no start: no deadline:2 after the mark | - | - | - |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 2,915,632 | 58.313 | 10 | 20 | MISS ceiling | 4,550,643 | 314 (12) | 0.032 |
| LINK_UP | `adp.link_up.if0` | 319,614 | 6.392 | 10 | 200 | fits | 3,595,134 | 322 (11) | 0.038 |
| LINK_UP | `adp.link_up.if1` | 701,317 | 14.026 | 10 | 200 | MISS T_svc | 3,595,134 | 322 (11) | 0.038 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 581,169 | 11.623 | 10 | 200 | MISS T_svc | 1,740,030 | 108 (39) | 0.069 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 543,559 | 10.871 | 10 | 200 | MISS T_svc | 1,740,030 | 108 (39) | 0.069 |
| LINK_DOWN | `adp.link_down.if0` | 303,453 | 6.069 | 10 | 200 | fits | 3,061,876 | 40 (9) | 0.062 |
| LINK_DOWN | `adp.link_down.if1` | 2,102,376 | 42.048 | 10 | 200 | MISS T_svc | 3,061,876 | 40 (9) | 0.062 |
| LINK_UP | `adp.link_up.if0` | 319,614 | 6.392 | 10 | 200 | fits | 3,595,134 | 322 (11) | 0.038 |
| LINK_UP | `adp.link_up.if1` | 701,317 | 14.026 | 10 | 200 | MISS T_svc | 3,595,134 | 322 (11) | 0.038 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 581,169 | 11.623 | 10 | 200 | MISS T_svc | 1,740,030 | 108 (39) | 0.069 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 543,559 | 10.871 | 10 | 200 | MISS T_svc | 1,740,030 | 108 (39) | 0.069 |
| GM_CHANGE | `adp.gm_change.if0` | 312,641 | 6.253 | 10 | 200 | fits | 1,127,879 | 40 (11) | 0.065 |
| GM_CHANGE | `adp.gm_change.if1` | 362,380 | 7.248 | 10 | 200 | fits | 1,127,879 | 40 (11) | 0.065 |
| LINK_UP | `adp.link_up.if0` | 319,614 | 6.392 | 10 | 200 | fits | 3,595,134 | 322 (11) | 0.038 |
| LINK_UP | `adp.link_up.if1` | 701,317 | 14.026 | 10 | 200 | MISS T_svc | 3,595,134 | 322 (11) | 0.038 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 581,169 | 11.623 | 10 | 200 | MISS T_svc | 1,740,030 | 108 (39) | 0.069 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 543,559 | 10.871 | 10 | 200 | MISS T_svc | 1,740,030 | 108 (39) | 0.069 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 527,184 | 10.544 | 10 | 200 | MISS T_svc | 1,127,470 | 79 (31) | 0.061 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 565,800 | 11.316 | 10 | 200 | MISS T_svc | 1,127,470 | 79 (31) | 0.061 |
| LINK_UP | `adp.link_up.if0` | 319,614 | 6.392 | 10 | 200 | fits | 3,595,134 | 322 (11) | 0.038 |
| LINK_UP | `adp.link_up.if1` | 701,317 | 14.026 | 10 | 200 | MISS T_svc | 3,595,134 | 322 (11) | 0.038 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 581,169 | 11.623 | 10 | 200 | MISS T_svc | 1,740,030 | 108 (39) | 0.069 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 543,559 | 10.871 | 10 | 200 | MISS T_svc | 1,740,030 | 108 (39) | 0.069 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 527,184 | 10.544 | 10 | 200 | MISS T_svc | 1,088,900 | 51 (31) | 0.062 |
| set_name | `aecp_fanout.set_name.if0` | 4,929,140 | 98.583 | 10 | 24 | MISS ceiling | 4,871,345 | 1190 | 0.055 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 4,859,308 | 97.186 | 10 | 24 | MISS ceiling | 5,704,029 | 662 | 0.059 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 4,629,864 | 92.597 | 10 | 24 | MISS ceiling | 5,664,719 | 629 | 0.056 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 4,664,738 | 93.295 | 10 | 24 | MISS ceiling | 5,607,873 | 629 | 0.058 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 4,566,716 | 91.334 | 10 | 24 | MISS ceiling | 5,587,880 | 640 | 0.060 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 4,643,259 | 92.865 | 10 | 24 | MISS ceiling | 5,626,588 | 728 | 0.057 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 4,823,629 | 96.473 | 10 | 24 | MISS ceiling | 5,819,252 | 728 | 0.057 |
| set_name | `aecp_fanout.set_name.if1` | 5,040,522 | 100.810 | 10 | 24 | MISS ceiling | 6,096,875 | 1181 | 0.048 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 5,162,913 | 103.258 | 10 | 24 | MISS ceiling | 7,603,299 | 878 | 0.044 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 6,517,720 | 130.354 | 10 | 24 | MISS ceiling | 6,077,979 | 629 | 0.056 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 5,865,378 | 117.308 | 10 | 24 | MISS ceiling | 6,871,212 | 649 | 0.051 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 5,891,943 | 117.839 | 10 | 24 | MISS ceiling | 6,833,698 | 728 | 0.046 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 5,575,684 | 111.514 | 10 | 24 | MISS ceiling | 6,571,365 | 728 | 0.047 |
| BIND_RX | `acmp.bind_rx.if0` | 720,285 | 14.406 | 10 | 20 | MISS T_svc | 1,600,484 | 95 (77) | 0.053 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 844,066 | 16.881 | 10 | 20 | MISS T_svc | 2,100,446 | 91 (32) | 0.049 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | - | - | - | - | no end: missing ['resp:1:4101'] | - | - | - |
| UNBIND_RX | `acmp.unbind_rx.if0` | 543,570 | 10.871 | 10 | 20 | MISS T_svc | 3,535,637 | 227 (50) | 0.047 |
| PROBE_TX | `acmp.probe_tx.if0` | - | - | - | - | no end: missing ['resp:1:4103'] | - | - | - |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 680,684 | 13.614 | 10 | 20 | MISS T_svc | 3,174,890 | 164 (48) | 0.045 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | - | - | - | - | no end: missing ['resp:1:4105'] | - | - | - |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 381,047 | 7.621 | 10 | 20 | fits | 3,093,749 | 163 (48) | 0.044 |
| BIND_RX | `acmp.bind_rx.if1` | - | - | - | - | no end: missing ['resp:1:4107', 'acmp_cmd:1:PROBE_TX', 'arm:3', 'pub:710'] | - | - | - |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 348,819 | 6.976 | 10 | 20 | fits | 4,853,867 | 387 (32) | 0.033 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | - | - | - | - | no end: missing ['resp:1:4108'] | - | - | - |
| UNBIND_RX | `acmp.unbind_rx.if1` | - | - | - | - | no end: missing ['resp:1:4109', 'tmr:3'] | - | - | - |
| PROBE_TX | `acmp.probe_tx.if1` | - | - | - | - | no end: missing ['resp:1:410a'] | - | - | - |
| GET_TX_STATE | `acmp.get_tx_state.if1` | - | - | - | - | no end: missing ['resp:1:410b'] | - | - | - |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | - | - | - | - | no end: missing ['resp:1:410c'] | - | - | - |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | - | - | - | - | no end: missing ['resp:1:410d'] | - | - | - |
| register_unsolicited | `aecp.register_unsolicited.if0` | 1,056,431 | 21.129 | 10 | 24 | MISS T_svc | 1,451,518 | 61 | 0.060 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 974,326 | 19.487 | 10 | 24 | MISS T_svc | 1,970,134 | 153 | 0.053 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 1,467,398 | 29.348 | 10 | 24 | MISS ceiling | 2,467,427 | 181 | 0.060 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 1,935,087 | 38.702 | 10 | 24 | MISS ceiling | 1,729,197 | 104 | 0.053 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 766,882 | 15.338 | 10 | 24 | MISS T_svc | 1,747,437 | 105 | 0.053 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 921,146 | 18.423 | 10 | 24 | MISS T_svc | 1,921,178 | 111 | 0.054 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 1,037,482 | 20.750 | 10 | 24 | MISS T_svc | 3,512,072 | 316 | 0.033 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 3,097,019 | 61.940 | 10 | 24 | MISS ceiling | 2,622,493 | 119 | 0.061 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 1,512,574 | 30.251 | 10 | 24 | MISS ceiling | 1,915,552 | 93 | 0.055 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 955,633 | 19.113 | 10 | 24 | MISS T_svc | 1,955,665 | 188 | 0.050 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 915,131 | 18.303 | 10 | 24 | MISS T_svc | 1,915,163 | 80 | 0.056 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 910,920 | 18.218 | 10 | 24 | MISS T_svc | 1,910,952 | 80 | 0.056 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 2,715,211 | 54.304 | 10 | 24 | MISS ceiling | 2,509,291 | 151 | 0.060 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 1,160,574 | 23.211 | 10 | 24 | MISS T_svc | 1,925,883 | 103 | 0.054 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 924,184 | 18.484 | 10 | 24 | MISS T_svc | 1,924,216 | 99 | 0.054 |
| get_configuration | `aecp.get_configuration.if0` | 892,516 | 17.850 | 10 | 24 | MISS T_svc | 1,892,548 | 75 | 0.057 |
| entity_available | `aecp.entity_available.if0` | 1,737,954 | 34.759 | 10 | 24 | MISS ceiling | 1,531,793 | 65 | 0.054 |
| get_name | `aecp.get_name.if0` | 934,936 | 18.699 | 10 | 24 | MISS T_svc | 1,915,488 | 92 | 0.056 |
| get_counters | `aecp.get_counters.if0` | 950,383 | 19.008 | 10 | 24 | MISS T_svc | 1,950,415 | 113 | 0.056 |
| get_avb_info | `aecp.get_avb_info.if0` | 907,609 | 18.152 | 10 | 24 | MISS T_svc | 1,907,641 | 75 | 0.055 |
| unknown_command | `aecp.unknown_command.if0` | 1,718,546 | 34.371 | 10 | 24 | MISS ceiling | 1,512,340 | 61 | 0.053 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 858,944 | 17.179 | 10 | 24 | MISS T_svc | 1,839,496 | 79 | 0.063 |
| set_name | `aecp.set_name.if0` | 1,094,310 | 21.886 | 10 | 24 | MISS T_svc | 2,370,533 | 175 | 0.044 |
| lock_entity | `aecp.lock_entity.if0` | 1,380,908 | 27.618 | 10 | 24 | MISS ceiling | 2,369,853 | 122 | 0.052 |
| unlock_entity | `aecp.unlock_entity.if0` | 1,197,050 | 23.941 | 10 | 24 | MISS T_svc | 2,135,700 | 116 | 0.056 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 2,028,951 | 40.579 | 10 | 24 | MISS ceiling | 2,931,682 | 194 | 0.066 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 1,137,620 | 22.752 | 10 | 24 | MISS T_svc | 2,137,652 | 157 | 0.054 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 2,049,635 | 40.993 | 10 | 24 | MISS ceiling | 3,317,789 | 307 | 0.032 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 3,121,864 | 62.437 | 10 | 24 | MISS ceiling | 2,627,858 | 133 | 0.060 |
| get_configuration | `aecp.get_configuration.if1` | 1,511,136 | 30.223 | 10 | 24 | MISS ceiling | 1,889,315 | 73 | 0.057 |
| entity_available | `aecp.entity_available.if1` | 895,368 | 17.907 | 10 | 24 | MISS T_svc | 1,895,400 | 77 | 0.056 |
| get_name | `aecp.get_name.if1` | 1,759,022 | 35.180 | 10 | 24 | MISS ceiling | 1,551,478 | 76 | 0.053 |
| get_counters | `aecp.get_counters.if1` | 968,923 | 19.378 | 10 | 24 | MISS T_svc | 1,949,534 | 111 | 0.056 |
| get_avb_info | `aecp.get_avb_info.if1` | 906,542 | 18.131 | 10 | 24 | MISS T_svc | 1,906,574 | 73 | 0.055 |
| unknown_command | `aecp.unknown_command.if1` | 878,732 | 17.575 | 10 | 24 | MISS T_svc | 1,878,764 | 73 | 0.056 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 1,678,825 | 33.576 | 10 | 24 | MISS ceiling | 1,471,175 | 63 | 0.061 |
| set_name | `aecp.set_name.if1` | 1,044,119 | 20.882 | 10 | 24 | MISS T_svc | 2,269,005 | 168 | 0.046 |
| lock_entity | `aecp.lock_entity.if1` | 1,269,597 | 25.392 | 10 | 24 | MISS ceiling | 2,466,435 | 141 | 0.052 |
| unlock_entity | `aecp.unlock_entity.if1` | 1,468,748 | 29.375 | 10 | 24 | MISS ceiling | 2,404,974 | 141 | 0.057 |

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
- `backlog-adp`: wait tx TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait tx TIMEOUT
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
