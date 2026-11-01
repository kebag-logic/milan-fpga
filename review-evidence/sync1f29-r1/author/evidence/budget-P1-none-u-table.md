### 1x1

20 of 81 paths and 55 of 141 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 2.137 (4.119) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 3.622 (23.623) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 11.855 (23.062) | MISS T_svc | 0 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 15.653 (23.006) | MISS T_svc | 0 adp | 2 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 3.830 (23.587) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 6.875 (26.876) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 3.515 (23.508) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 3.970 (23.514) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 12.782 (30.488) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 2.850 (45.029) | fits | 2 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 6.792 (48.350) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 6.146 (45.592) | fits | 1 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 2.795 (18.853) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 3.074 (22.651) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 6.402 (47.762) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 7.115 (27.423) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.294 (1.632) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.113 (1.481) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.643 (5.622) | fits | 1 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.114 (4.988) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.468 (1.817) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 1.389 (4.108) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 3.991 (5.136) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 4.016 (5.162) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 3.919 (5.064) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 4.965 (6.110) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 4.191 (5.337) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 4.168 (5.627) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 2.512 (3.658) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 5.161 (6.306) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 4.349 (5.495) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 4.283 (5.428) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 4.233 (5.378) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 6.234 (7.379) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 4.036 (5.181) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 4.038 (5.184) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 4.508 (5.654) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 4.895 (6.040) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 4.990 (6.135) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 4.340 (5.485) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 4.502 (5.648) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 5.044 (6.190) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 4.346 (5.492) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 2.492 (3.628) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 4.969 (7.199) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 3.916 (5.061) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 4.160 (5.618) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 8.596 (9.810) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 8.416 (9.569) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 8.604 (9.820) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 8.771 (9.647) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 7.968 (9.122) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 11.493 (13.281) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 8.003 (8.846) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 8.427 (9.581) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 63.740 (70.504) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 71.565 (86.478) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 92.966 (113.220) | MISS ceiling | 4 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 15.734 (29.382) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 125.668 (129.760) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 363.896 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 6.037 (9.266) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 1.770 (4.518) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 1.240 (2.552) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.912 (4.988) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 1.512 (4.518) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 1.285 (4.004) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp.service.acmp.first.if0` (backlog-adp) | 17.641 | MISS T_svc | 0 acmp | 5 | 4 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 145.944 | MISS ceiling | 11 acmp | 5 | 4 |
| ADP record released under the composed load, first | 0 | `backlog-adp.service.adp.first.if0` (backlog-adp) | 17.631 | MISS T_svc | 0 adp | 5 | 4 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 105.988 | MISS T_svc | 4 adp | 5 | 4 |
| AECP record released under the composed load, first | 0 | `backlog-adp.service.aecp.first.if0` (backlog-adp) | 17.676 | MISS T_svc | 0 aecp | 5 | 4 |
| AECP record released under the composed load, last | 0 | `backlog-adp-refill.service.aecp.last.if0` (backlog-adp-refill) | 423.961 | MISS ceiling | 15 aecp | 5 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog-adp.service.maap.first.if0` (backlog-adp) | 17.666 | MISS T_svc | 0 maap | 5 | 4 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 85.285 | MISS ceiling | 6 maap | 5 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 632.951 | STARVED: never released | 0 srp | 5 | 5 |
| SRP record released under the composed load, last | 0 | `backlog-adp-refill.service.srp.last.if0` (backlog-adp-refill) | at least 632.931 | STARVED: never released | 31 srp | 5 | 5 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 5.513 (7.658) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 3.314 (3.315) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 2.166 (2.166) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 4.454 (4.988) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 163.779 | 27 | 747,101 (14.942) | yes | - |
| backlog-adp | 571.618 | 22 | 1,591,054 (31.821) | no | {'srp': 32} |
| backlog-adp-refill | 632.968 | 24 | 1,556,613 (31.132) | no | {'srp': 32} |
| backlog-owed | 363.947 | 43 | 589,557 (11.791) | yes | - |
| fixture | 20.000 | 3 | 420,868 (8.417) | yes | - |

Composed maximum over the 4 backlog windows: at least 1,591,054 CPU cycles (31.821 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 747,101 (14.942 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 153,699 | 3.074 | 10 | 20 | fits | 1,132,554 | 109 (14) | 0.889 |
| LINK_UP | `adp.link_up.if0` | 5,708 | 0.114 | 10 | 200 | fits | 249,417 | 88 (11) | 0.885 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 69,462 | 1.389 | 10 | 200 | fits | 102,073 | 46 (39) | 0.868 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 23,381 | 0.468 | 10 | 200 | fits | 5,745 | 9 (11) | 0.863 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 196,331 | 3.927 | 10 | 20 | fits | 1,138,847 | 130 (35) | 0.890 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 139,742 | 2.795 | 10 | 20 | fits | 942,629 | 97 (14) | 0.890 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 320,082 | 6.402 | 10 | 20 | fits | 1,110,828 | 108 (14) | 0.890 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 142,482 | 2.850 | 10 | 20 | fits | 1,140,625 | 130 (35) | 0.890 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 222,724 | 4.454 | 10 | 18 | fits | 249,417 | 88 | 0.885 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 165,698 | 3.314 | 10 | 18 | fits | 165,730 | 35 | 0.871 |
| malformed MRPDU discard | `srp.malformed.if0` | 87,676 | 1.754 | 10 | 18 | fits | 87,708 | 29 | 0.856 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 275,667 | 5.513 | 210 | 218 | fits | 382,893 | 84 | 0.874 |
| an event behind 15 others | `backlog.event.if0` | 786,693 | 15.734 | 10 | 200 | MISS T_svc | 722,009 | 356 | 0.878 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 3,187,012 | 63.740 | 10 | 20 | MISS ceiling | 476,962 | 217 | 0.883 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 746,997 | 14.940 | 10 | 200 | MISS T_svc | 747,101 | 389 | 0.878 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 2,570,819 | 51.416 | 10 | 200 | MISS T_svc | 516,405 | 285 | 0.882 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 744,868 | 14.897 | 10 | 20 | MISS T_svc | 747,101 | 389 | 0.878 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 3,522,554 | 70.451 | 10 | 20 | MISS ceiling | 476,962 | 217 | 0.883 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 746,660 | 14.933 | 10 | 24 | MISS T_svc | 747,101 | 389 | 0.878 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 7,024,762 | 140.495 | 10 | 24 | MISS ceiling | 362,936 | 169 | 0.888 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 746,140 | 14.923 | 10 | 50 | MISS T_svc | 747,101 | 389 | 0.878 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 2,570,071 | 51.401 | 10 | 50 | MISS ceiling | 516,405 | 285 | 0.882 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 4,231,583 | 84.632 | 10 | 18 | MISS ceiling | 362,850 | 169 | 0.888 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 7,988,615 | 159.772 | 10 | 18 | MISS ceiling | 75,329 | 29 | 0.867 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 3,578,270 | 71.565 | 10 | 20 | MISS ceiling | 1,591,054 | 401 | 0.888 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 881,571 | 17.631 | 10 | 200 | MISS T_svc | 942,717 | 402 | 0.884 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 4,262,428 | 85.249 | 10 | 200 | MISS T_svc | 1,591,054 | 401 | 0.888 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 882,027 | 17.641 | 10 | 20 | MISS T_svc | 942,717 | 402 | 0.884 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 7,261,229 | 145.225 | 10 | 20 | MISS ceiling | 1,499,002 | 307 | 0.890 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 883,820 | 17.676 | 10 | 24 | MISS T_svc | 942,717 | 402 | 0.884 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 21,161,094 | 423.222 | 10 | 24 | MISS ceiling | 1,359,212 | 220 | 0.892 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 883,300 | 17.666 | 10 | 50 | MISS T_svc | 942,717 | 402 | 0.884 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 4,264,266 | 85.285 | 10 | 50 | MISS ceiling | 1,591,054 | 401 | 0.888 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 28,580,075 | 571.601 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 28,579,068 | 571.581 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 4,648,294 | 92.966 | 10 | 20 | MISS ceiling | 1,545,407 | 339 | 0.889 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 881,571 | 17.631 | 10 | 200 | MISS T_svc | 942,717 | 402 | 0.884 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 5,299,392 | 105.988 | 10 | 200 | MISS T_svc | 1,545,407 | 339 | 0.889 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 882,027 | 17.641 | 10 | 20 | MISS T_svc | 942,717 | 402 | 0.884 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 7,297,198 | 145.944 | 10 | 20 | MISS ceiling | 1,545,407 | 339 | 0.889 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 883,820 | 17.676 | 10 | 24 | MISS T_svc | 942,717 | 402 | 0.884 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 21,198,060 | 423.961 | 10 | 24 | MISS ceiling | 1,359,037 | 220 | 0.892 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 883,300 | 17.666 | 10 | 50 | MISS T_svc | 942,717 | 402 | 0.884 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 4,229,825 | 84.596 | 10 | 50 | MISS ceiling | 1,556,613 | 394 | 0.889 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 31,647,557 | 632.951 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 31,646,550 | 632.931 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,283,404 | 125.668 | 10 | 20 | MISS ceiling | 477,412 | 191 | 0.880 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,194,806 | 363.896 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,194,769 | 363.895 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,194,731 | 363.895 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,194,694 | 363.894 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 586,056 | 11.721 | 10 | 200 | MISS T_svc | 569,276 | 341 | 0.876 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 2,252,025 | 45.041 | 10 | 200 | MISS T_svc | 521,837 | 261 | 0.880 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 583,926 | 11.679 | 10 | 20 | MISS T_svc | 569,276 | 341 | 0.876 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 2,988,729 | 59.775 | 10 | 20 | MISS ceiling | 333,635 | 81 | 0.879 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 585,719 | 11.714 | 10 | 24 | MISS T_svc | 569,276 | 341 | 0.876 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 7,637,472 | 152.749 | 10 | 24 | MISS ceiling | 320,538 | 124 | 0.886 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 585,199 | 11.704 | 10 | 50 | MISS T_svc | 569,276 | 341 | 0.876 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 2,251,278 | 45.026 | 10 | 50 | MISS T_svc | 521,837 | 261 | 0.880 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 3,305,771 | 66.115 | 10 | 18 | MISS ceiling | 315,585 | 170 | 0.875 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 9,091,882 | 181.838 | 10 | 18 | MISS ceiling | 195,846 | 53 | 0.866 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 782,662 | 15.653 | 10 | 20 | MISS T_svc | 1,150,278 | 130 (29) | 0.890 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 592,771 | 11.855 | 10 | 20 | MISS T_svc | 1,153,116 | 136 (35) | 0.890 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 339,599 | 6.792 | 10 | 20 | fits | 1,139,709 | 130 (12) | 0.890 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 45,590 | 0.912 | 10 | 50 | fits | 249,417 | 88 | 0.885 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 64,254 | 1.285 | 10 | 50 | fits | 105,327 | 37 | 0.874 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 62,463 | 1.249 | 10 | 50 | fits | 130,893 | 43 | 0.880 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 75,597 | 1.512 | 10 | 50 | fits | 136,178 | 64 | 0.879 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 88,525 | 1.770 | 10 | 50 | fits | 136,178 | 64 | 0.879 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 61,976 | 1.240 | 10 | 50 | fits | 127,618 | 53 | 0.876 |
| LINK_UP | `adp.link_up.if0` | 5,708 | 0.114 | 10 | 200 | fits | 249,417 | 88 (11) | 0.885 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 69,462 | 1.389 | 10 | 200 | fits | 102,073 | 46 (39) | 0.868 |
| LINK_DOWN | `adp.link_down.if0` | 4,344 | 0.087 | 10 | 200 | fits | 275,718 | 33 (9) | 0.877 |
| LINK_UP | `adp.link_up.if0` | 5,708 | 0.114 | 10 | 200 | fits | 249,417 | 88 (11) | 0.885 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 69,462 | 1.389 | 10 | 200 | fits | 102,073 | 46 (39) | 0.868 |
| GM_CHANGE | `adp.gm_change.if0` | 5,648 | 0.113 | 10 | 200 | fits | 74,061 | 18 (11) | 0.862 |
| LINK_UP | `adp.link_up.if0` | 5,708 | 0.114 | 10 | 200 | fits | 249,417 | 88 (11) | 0.885 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 69,462 | 1.389 | 10 | 200 | fits | 102,073 | 46 (39) | 0.868 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 14,695 | 0.294 | 10 | 200 | fits | 81,602 | 38 (31) | 0.862 |
| LINK_UP | `adp.link_up.if0` | 5,708 | 0.114 | 10 | 200 | fits | 249,417 | 88 (11) | 0.885 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 69,462 | 1.389 | 10 | 200 | fits | 102,073 | 46 (39) | 0.868 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 14,695 | 0.294 | 10 | 200 | fits | 81,602 | 38 (31) | 0.862 |
| set_name | `aecp_fanout.set_name.if0` | 574,631 | 11.493 | 10 | 24 | MISS T_svc | 664,036 | 622 | 0.886 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 438,537 | 8.771 | 10 | 24 | fits | 482,370 | 335 | 0.880 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 397,783 | 7.956 | 10 | 24 | fits | 455,413 | 311 | 0.881 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 398,391 | 7.968 | 10 | 24 | fits | 456,093 | 311 | 0.881 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 430,196 | 8.604 | 10 | 24 | fits | 491,013 | 351 | 0.880 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 429,815 | 8.596 | 10 | 24 | fits | 490,506 | 351 | 0.879 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 400,164 | 8.003 | 10 | 24 | fits | 442,281 | 317 | 0.880 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 420,777 | 8.416 | 10 | 24 | fits | 478,446 | 362 | 0.883 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 421,329 | 8.427 | 10 | 24 | fits | 479,031 | 362 | 0.883 |
| BIND_RX | `acmp.bind_rx.if0` | 81,267 | 1.625 | 10 | 20 | fits | 197,756 | 82 (77) | 0.873 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 639,098 | 12.782 | 10 | 20 | MISS T_svc | 1,524,421 | 153 (32) | 0.890 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 191,480 | 3.830 | 10 | 20 | fits | 1,179,361 | 148 (47) | 0.890 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 355,758 | 7.115 | 10 | 20 | fits | 1,371,155 | 161 (50) | 0.889 |
| PROBE_TX | `acmp.probe_tx.if0` | 198,480 | 3.970 | 10 | 20 | fits | 1,175,696 | 150 (48) | 0.890 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 175,759 | 3.515 | 10 | 20 | fits | 1,175,376 | 149 (48) | 0.890 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 181,099 | 3.622 | 10 | 20 | fits | 1,181,136 | 180 (48) | 0.889 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 343,741 | 6.875 | 10 | 20 | fits | 1,343,778 | 159 (48) | 0.890 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 124,622 | 2.492 | 10 | 24 | fits | 181,419 | 47 | 0.879 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 258,032 | 5.161 | 10 | 24 | fits | 315,306 | 125 | 0.886 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 217,470 | 4.349 | 10 | 24 | fits | 274,740 | 74 | 0.885 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 225,425 | 4.508 | 10 | 24 | fits | 282,695 | 84 | 0.885 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 225,124 | 4.502 | 10 | 24 | fits | 282,398 | 83 | 0.885 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 252,225 | 5.044 | 10 | 24 | fits | 309,499 | 90 | 0.887 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 217,316 | 4.346 | 10 | 24 | fits | 274,590 | 73 | 0.885 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 214,139 | 4.283 | 10 | 24 | fits | 271,413 | 68 | 0.885 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 211,655 | 4.233 | 10 | 24 | fits | 268,925 | 65 | 0.885 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 311,682 | 6.234 | 10 | 24 | fits | 368,952 | 167 | 0.888 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 201,801 | 4.036 | 10 | 24 | fits | 259,071 | 52 | 0.884 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 201,905 | 4.038 | 10 | 24 | fits | 259,175 | 52 | 0.884 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 244,749 | 4.895 | 10 | 24 | fits | 302,019 | 76 | 0.886 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 249,493 | 4.990 | 10 | 24 | fits | 306,763 | 82 | 0.887 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 216,982 | 4.340 | 10 | 24 | fits | 274,252 | 68 | 0.884 |
| get_configuration | `aecp.get_configuration.if0` | 195,950 | 3.919 | 10 | 24 | fits | 253,220 | 47 | 0.885 |
| entity_available | `aecp.entity_available.if0` | 199,533 | 3.991 | 10 | 24 | fits | 256,807 | 51 | 0.885 |
| get_name | `aecp.get_name.if0` | 209,569 | 4.191 | 10 | 24 | fits | 266,843 | 64 | 0.885 |
| get_counters | `aecp.get_counters.if0` | 248,227 | 4.965 | 10 | 24 | fits | 305,501 | 92 | 0.888 |
| get_avb_info | `aecp.get_avb_info.if0` | 200,805 | 4.016 | 10 | 24 | fits | 258,079 | 48 | 0.884 |
| unknown_command | `aecp.unknown_command.if0` | 195,777 | 3.916 | 10 | 24 | fits | 253,051 | 47 | 0.885 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 125,604 | 2.512 | 10 | 24 | fits | 182,878 | 51 | 0.879 |
| set_name | `aecp.set_name.if0` | 248,464 | 4.969 | 10 | 24 | fits | 359,949 | 127 | 0.880 |
| lock_entity | `aecp.lock_entity.if0` | 208,381 | 4.168 | 10 | 24 | fits | 281,333 | 78 | 0.882 |
| unlock_entity | `aecp.unlock_entity.if0` | 208,002 | 4.160 | 10 | 24 | fits | 280,915 | 77 | 0.883 |
| LINK_UP | `fixture.link_up.if0` | 5,708 | 0.114 | 10 | 200 | fits | 249,417 | 88 (11) | 0.885 |
| malformed MRPDU discard | `fixture.malformed.if0` | 108,283 | 2.166 | 10 | 18 | fits | 108,315 | 35 | 0.869 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 301,865 | 6.037 | 10 | 24 | fits | 361,054 | 127 | 0.879 |
| LINK_DOWN | `fixture.link_down.if0` | 32,136 | 0.643 | 10 | 200 | fits | 281,111 | 33 (9) | 0.877 |
| BIND_RX | `fixture.bind_rx.if0` | 106,874 | 2.137 | 10 | 20 | fits | 205,959 | 89 (77) | 0.872 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 307,288 | 6.146 | 10 | 20 | fits | 1,004,945 | 149 (35) | 0.889 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 280,623 | 5.612 | 10 | 20 | fits | 1,320,223 | 140 (29) | 0.890 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 420,817 | 8.416 | 10 | 200 | fits | 420,868 | 225 | 0.881 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 420,817 | 8.416 | 10 | 200 | fits | 420,868 | 225 | 0.881 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 420,682 | 8.414 | 10 | 20 | fits | 420,868 | 225 | 0.881 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 420,682 | 8.414 | 10 | 20 | fits | 420,868 | 225 | 0.881 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 420,784 | 8.416 | 10 | 24 | fits | 420,868 | 225 | 0.881 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 420,784 | 8.416 | 10 | 24 | fits | 420,868 | 225 | 0.881 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 420,752 | 8.415 | 10 | 50 | fits | 420,868 | 225 | 0.881 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 420,752 | 8.415 | 10 | 50 | fits | 420,868 | 225 | 0.881 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 590,143 | 11.803 | 10 | 18 | MISS T_svc | 169,424 | 37 | 0.870 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 590,143 | 11.803 | 10 | 18 | MISS T_svc | 169,424 | 37 | 0.870 |

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
- `fixture`: wait quiet TIMEOUT
