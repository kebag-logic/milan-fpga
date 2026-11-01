### 1x1

23 of 81 paths and 67 of 141 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 6.167 (15.305) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 5.923 (25.572) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 7.101 (23.250) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 19.638 (47.081) | MISS T_svc | 0 adp | 2 | 2 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 5.890 (25.442) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 4.419 (24.420) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 4.304 (24.432) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 8.099 (26.179) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 16.816 (29.099) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 8.509 (46.627) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 6.607 (44.532) | fits | 2 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 4.236 (23.149) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 5.389 (45.818) | fits | 1 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 4.630 (25.748) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 4.972 (44.155) | fits | 1 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 5.570 (26.930) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 2.499 (7.784) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 1.996 (7.430) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 7.043 (19.321) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 1.731 (12.999) | fits | 1 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 1.311 (1.542) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 2.745 (9.012) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 5.325 (7.729) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 7.395 (12.296) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 5.834 (10.686) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 6.163 (11.929) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 6.330 (11.449) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 6.810 (12.105) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 3.030 (6.266) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 7.862 (12.891) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 6.500 (11.397) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 6.382 (11.280) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 4.598 (7.911) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 7.160 (12.057) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 5.006 (10.813) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 7.078 (12.066) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 4.745 (8.060) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 10.192 (17.485) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 6.552 (11.449) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 5.558 (7.962) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 6.498 (11.396) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 7.384 (13.189) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 4.658 (7.969) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 6.467 (11.190) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 7.649 (11.880) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 4.005 (8.857) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 4.949 (7.680) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 9.725 (14.649) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 9.331 (14.138) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 9.268 (16.792) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 7.952 (11.625) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 7.976 (12.895) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 10.400 (15.252) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 8.970 (13.746) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 8.844 (11.176) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 87.564 (96.728) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 75.215 (110.114) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 93.178 (109.794) | MISS ceiling | 6 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 25.947 (45.649) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 158.144 (166.045) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 860.002 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 15.226 (24.523) | MISS T_svc | 0 aecp | 1 | 1 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 3.246 (9.001) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 3.573 (8.219) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 4.138 (12.999) | fits | 1 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 3.104 (9.001) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 3.608 (8.190) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 24.834 | MISS ceiling | 0 acmp | 5 | 5 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 146.623 | MISS ceiling | 11 acmp | 5 | 5 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 24.876 | MISS T_svc | 0 adp | 5 | 5 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 106.504 | MISS T_svc | 6 adp | 5 | 5 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 24.869 | MISS ceiling | 0 aecp | 5 | 5 |
| AECP record released under the composed load, last | 0 | `backlog-adp.service.aecp.last.if0` (backlog-adp) | 413.799 | MISS ceiling | 15 aecp | 5 | 5 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 24.859 | MISS T_svc | 0 maap | 5 | 5 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 89.024 | MISS ceiling | 6 maap | 5 | 5 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 633.163 | STARVED: never released | 0 srp | 5 | 5 |
| SRP record released under the composed load, last | 0 | `backlog-adp-refill.service.srp.last.if0` (backlog-adp-refill) | at least 633.143 | STARVED: never released | 31 srp | 5 | 5 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 9.850 (12.702) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 10.443 (13.027) | MISS T_svc | 0 srp | 1 | 1 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 6.196 (8.225) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 10.929 (12.999) | MISS T_svc | 1 events | 1 | 1 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 249.577 | 28 | 961,354 (19.227) | yes | - |
| backlog-adp | 575.268 | 24 | 1,595,371 (31.907) | no | {'srp': 32} |
| backlog-adp-refill | 633.180 | 26 | 1,595,624 (31.912) | no | {'srp': 32} |
| backlog-owed | 860.053 | 86 | 1,014,854 (20.297) | yes | - |
| fixture | 20.000 | 2 | 699,974 (13.999) | yes | - |

Composed maximum over the 4 backlog windows: at least 1,595,624 CPU cycles (31.912 ms), backlog-adp-refill, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 1,014,854 (20.297 ms), backlog-owed.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 231,502 | 4.630 | 10 | 20 | fits | 1,287,395 | 109 (14) | 0.013 |
| LINK_UP | `adp.link_up.if0` | 86,575 | 1.731 | 10 | 200 | fits | 649,969 | 94 (11) | 0.034 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 137,230 | 2.745 | 10 | 200 | fits | 319,379 | 52 (39) | 0.034 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 65,570 | 1.311 | 10 | 200 | fits | 77,123 | 15 (11) | 0.042 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 211,802 | 4.236 | 10 | 20 | fits | 1,157,442 | 130 (35) | 0.010 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 269,431 | 5.389 | 10 | 20 | fits | 1,136,123 | 107 (14) | 0.011 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 248,603 | 4.972 | 10 | 20 | fits | 1,146,833 | 108 (14) | 0.011 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 425,475 | 8.509 | 10 | 20 | fits | 1,184,503 | 130 (35) | 0.011 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 546,474 | 10.929 | 10 | 18 | MISS T_svc | 649,969 | 94 | 0.034 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 522,153 | 10.443 | 10 | 18 | MISS T_svc | 503,333 | 35 | 0.041 |
| malformed MRPDU discard | `srp.malformed.if0` | 309,787 | 6.196 | 10 | 18 | fits | 186,887 | 29 | 0.023 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 492,475 | 9.850 | 210 | 218 | fits | 635,112 | 84 | 0.019 |
| an event behind 15 others | `backlog.event.if0` | 1,297,372 | 25.947 | 10 | 200 | MISS T_svc | 961,354 | 356 | 0.015 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 4,378,205 | 87.564 | 10 | 20 | MISS ceiling | 585,789 | 217 | 0.013 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 1,243,806 | 24.876 | 10 | 200 | MISS T_svc | 865,189 | 383 | 0.018 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 3,591,762 | 71.835 | 10 | 200 | MISS T_svc | 676,034 | 330 | 0.013 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 1,241,677 | 24.834 | 10 | 20 | MISS ceiling | 865,189 | 383 | 0.018 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 4,756,553 | 95.131 | 10 | 20 | MISS ceiling | 585,789 | 217 | 0.013 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 1,243,469 | 24.869 | 10 | 24 | MISS ceiling | 865,189 | 383 | 0.018 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 9,214,195 | 184.284 | 10 | 24 | MISS ceiling | 338,449 | 124 | 0.011 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 1,242,949 | 24.859 | 10 | 50 | MISS T_svc | 865,189 | 383 | 0.018 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 3,591,014 | 71.820 | 10 | 50 | MISS ceiling | 676,034 | 330 | 0.013 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 3,590,982 | 71.820 | 10 | 18 | MISS ceiling | 676,034 | 330 | 0.013 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 10,863,474 | 217.269 | 10 | 18 | MISS ceiling | 142,860 | 47 | 0.018 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 3,760,774 | 75.215 | 10 | 20 | MISS ceiling | 1,512,898 | 401 | 0.009 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 1,050,698 | 21.014 | 10 | 200 | MISS T_svc | 1,045,305 | 402 | 0.011 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 4,449,341 | 88.987 | 10 | 200 | MISS T_svc | 1,512,898 | 401 | 0.009 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 1,051,154 | 21.023 | 10 | 20 | MISS ceiling | 1,045,305 | 402 | 0.011 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 7,331,154 | 146.623 | 10 | 20 | MISS ceiling | 1,526,214 | 317 | 0.008 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 1,052,946 | 21.059 | 10 | 24 | MISS T_svc | 1,045,305 | 402 | 0.011 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 20,689,943 | 413.799 | 10 | 24 | MISS ceiling | 1,343,653 | 230 | 0.008 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 1,052,426 | 21.049 | 10 | 50 | MISS T_svc | 1,045,305 | 402 | 0.011 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 4,451,179 | 89.024 | 10 | 50 | MISS ceiling | 1,512,898 | 401 | 0.009 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 28,762,579 | 575.252 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 28,761,572 | 575.231 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 4,658,881 | 93.178 | 10 | 20 | MISS ceiling | 1,479,172 | 339 | 0.009 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 1,050,698 | 21.014 | 10 | 200 | MISS T_svc | 1,045,305 | 402 | 0.011 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 5,325,217 | 106.504 | 10 | 200 | MISS T_svc | 1,479,172 | 339 | 0.009 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 1,051,154 | 21.023 | 10 | 20 | MISS ceiling | 1,045,305 | 402 | 0.011 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 7,323,023 | 146.460 | 10 | 20 | MISS ceiling | 1,479,172 | 339 | 0.009 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 1,052,946 | 21.059 | 10 | 24 | MISS T_svc | 1,045,305 | 402 | 0.011 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 20,684,818 | 413.696 | 10 | 24 | MISS ceiling | 1,343,689 | 230 | 0.008 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 1,052,426 | 21.049 | 10 | 50 | MISS T_svc | 1,045,305 | 402 | 0.011 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 4,404,095 | 88.082 | 10 | 50 | MISS ceiling | 1,465,814 | 394 | 0.009 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 31,658,144 | 633.163 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 31,657,137 | 633.143 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 7,907,189 | 158.144 | 10 | 20 | MISS ceiling | 524,061 | 152 | 0.017 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 43,000,111 | 860.002 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 43,000,073 | 860.001 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 8,431,149 | 168.623 | 10 | 20 | MISS ceiling | 524,073 | 152 | 0.017 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 42,999,998 | 860.000 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 788,536 | 15.771 | 10 | 200 | MISS T_svc | 730,053 | 341 | 0.013 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 3,184,461 | 63.689 | 10 | 200 | MISS T_svc | 1,014,854 | 287 | 0.020 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 786,407 | 15.728 | 10 | 20 | MISS T_svc | 730,053 | 341 | 0.013 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 4,716,214 | 94.324 | 10 | 20 | MISS ceiling | 656,463 | 195 | 0.016 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 788,199 | 15.764 | 10 | 24 | MISS T_svc | 730,053 | 341 | 0.013 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 10,652,930 | 213.059 | 10 | 24 | MISS ceiling | 683,580 | 173 | 0.016 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 787,679 | 15.754 | 10 | 50 | MISS T_svc | 730,053 | 341 | 0.013 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 3,183,713 | 63.674 | 10 | 50 | MISS ceiling | 1,014,854 | 287 | 0.020 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 3,183,681 | 63.674 | 10 | 18 | MISS ceiling | 1,014,854 | 287 | 0.020 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 15,725,904 | 314.518 | 10 | 18 | MISS ceiling | 372,105 | 53 | 0.022 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 967,251 | 19.345 | 10 | 20 | MISS T_svc | 1,167,780 | 130 (29) | 0.010 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 355,039 | 7.101 | 10 | 20 | fits | 1,162,508 | 136 (35) | 0.010 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 330,348 | 6.607 | 10 | 20 | fits | 1,166,615 | 130 (12) | 0.011 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 206,925 | 4.138 | 10 | 50 | fits | 649,969 | 94 | 0.034 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 180,381 | 3.608 | 10 | 50 | fits | 196,417 | 37 | 0.023 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 73,601 | 1.472 | 10 | 50 | fits | 196,429 | 37 | 0.023 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 155,202 | 3.104 | 10 | 50 | fits | 290,161 | 70 | 0.023 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 162,313 | 3.246 | 10 | 50 | fits | 290,161 | 70 | 0.023 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 178,662 | 3.573 | 10 | 50 | fits | 197,685 | 47 | 0.022 |
| LINK_UP | `adp.link_up.if0` | 86,575 | 1.731 | 10 | 200 | fits | 649,969 | 94 (11) | 0.034 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 137,230 | 2.745 | 10 | 200 | fits | 319,379 | 52 (39) | 0.034 |
| LINK_DOWN | `adp.link_down.if0` | 352,158 | 7.043 | 10 | 200 | fits | 503,654 | 33 (9) | 0.023 |
| LINK_UP | `adp.link_up.if0` | 86,575 | 1.731 | 10 | 200 | fits | 649,969 | 94 (11) | 0.034 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 137,230 | 2.745 | 10 | 200 | fits | 319,379 | 52 (39) | 0.034 |
| GM_CHANGE | `adp.gm_change.if0` | 99,791 | 1.996 | 10 | 200 | fits | 158,374 | 18 (11) | 0.024 |
| LINK_UP | `adp.link_up.if0` | 86,575 | 1.731 | 10 | 200 | fits | 649,969 | 94 (11) | 0.034 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 137,230 | 2.745 | 10 | 200 | fits | 319,379 | 52 (39) | 0.034 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 124,930 | 2.499 | 10 | 200 | fits | 176,074 | 38 (31) | 0.025 |
| LINK_UP | `adp.link_up.if0` | 86,575 | 1.731 | 10 | 200 | fits | 649,969 | 94 (11) | 0.034 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 137,230 | 2.745 | 10 | 200 | fits | 319,379 | 52 (39) | 0.034 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 124,930 | 2.499 | 10 | 200 | fits | 176,074 | 38 (31) | 0.025 |
| set_name | `aecp_fanout.set_name.if0` | 520,016 | 10.400 | 10 | 24 | MISS T_svc | 762,587 | 629 | 0.011 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 397,603 | 7.952 | 10 | 24 | fits | 581,235 | 335 | 0.013 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 378,709 | 7.574 | 10 | 24 | fits | 488,239 | 311 | 0.010 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 398,818 | 7.976 | 10 | 24 | fits | 484,142 | 311 | 0.010 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 463,389 | 9.268 | 10 | 24 | fits | 577,599 | 351 | 0.012 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 486,247 | 9.725 | 10 | 24 | fits | 518,973 | 351 | 0.010 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 448,513 | 8.970 | 10 | 24 | fits | 473,947 | 318 | 0.010 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 466,532 | 9.331 | 10 | 24 | fits | 493,531 | 363 | 0.009 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 442,178 | 8.844 | 10 | 24 | fits | 558,799 | 369 | 0.011 |
| BIND_RX | `acmp.bind_rx.if0` | 308,351 | 6.167 | 10 | 20 | fits | 614,918 | 89 (77) | 0.038 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 840,789 | 16.816 | 10 | 20 | MISS T_svc | 1,454,934 | 153 (32) | 0.009 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 294,479 | 5.890 | 10 | 20 | fits | 1,272,120 | 148 (47) | 0.012 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 278,481 | 5.570 | 10 | 20 | fits | 1,346,501 | 151 (50) | 0.012 |
| PROBE_TX | `acmp.probe_tx.if0` | 404,969 | 8.099 | 10 | 20 | fits | 1,308,960 | 160 (48) | 0.010 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 215,217 | 4.304 | 10 | 20 | fits | 1,221,602 | 170 (48) | 0.014 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 296,159 | 5.923 | 10 | 20 | fits | 1,278,624 | 159 (48) | 0.009 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 220,971 | 4.419 | 10 | 20 | fits | 1,221,008 | 149 (48) | 0.011 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 323,348 | 6.467 | 10 | 24 | fits | 409,189 | 54 | 0.027 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 393,096 | 7.862 | 10 | 24 | fits | 438,226 | 132 | 0.015 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 324,994 | 6.500 | 10 | 24 | fits | 337,609 | 73 | 0.014 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 237,239 | 4.745 | 10 | 24 | fits | 403,013 | 91 | 0.015 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 324,913 | 6.498 | 10 | 24 | fits | 339,820 | 83 | 0.013 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 369,199 | 7.384 | 10 | 24 | fits | 339,948 | 83 | 0.013 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 232,907 | 4.658 | 10 | 24 | fits | 398,442 | 79 | 0.016 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 319,121 | 6.382 | 10 | 24 | fits | 333,868 | 68 | 0.014 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 229,910 | 4.598 | 10 | 24 | fits | 395,543 | 72 | 0.016 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 358,003 | 7.160 | 10 | 24 | fits | 372,745 | 160 | 0.011 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 250,298 | 5.006 | 10 | 24 | fits | 327,373 | 53 | 0.014 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 353,924 | 7.078 | 10 | 24 | fits | 390,260 | 59 | 0.017 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 509,601 | 10.192 | 10 | 24 | MISS T_svc | 447,577 | 76 | 0.019 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 327,585 | 6.552 | 10 | 24 | fits | 338,658 | 75 | 0.013 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 277,908 | 5.558 | 10 | 24 | fits | 398,112 | 74 | 0.016 |
| get_configuration | `aecp.get_configuration.if0` | 291,711 | 5.834 | 10 | 24 | fits | 317,488 | 47 | 0.014 |
| entity_available | `aecp.entity_available.if0` | 266,260 | 5.325 | 10 | 24 | fits | 386,472 | 58 | 0.017 |
| get_name | `aecp.get_name.if0` | 316,493 | 6.330 | 10 | 24 | fits | 357,644 | 64 | 0.016 |
| get_counters | `aecp.get_counters.if0` | 308,175 | 6.163 | 10 | 24 | fits | 383,303 | 86 | 0.017 |
| get_avb_info | `aecp.get_avb_info.if0` | 369,768 | 7.395 | 10 | 24 | fits | 397,984 | 54 | 0.017 |
| unknown_command | `aecp.unknown_command.if0` | 200,241 | 4.005 | 10 | 24 | fits | 312,715 | 47 | 0.014 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 151,516 | 3.030 | 10 | 24 | fits | 313,321 | 58 | 0.018 |
| set_name | `aecp.set_name.if0` | 382,454 | 7.649 | 10 | 24 | fits | 593,992 | 134 | 0.019 |
| lock_entity | `aecp.lock_entity.if0` | 340,519 | 6.810 | 10 | 24 | fits | 451,113 | 84 | 0.018 |
| unlock_entity | `aecp.unlock_entity.if0` | 247,444 | 4.949 | 10 | 24 | fits | 384,000 | 77 | 0.016 |
| LINK_UP | `fixture.link_up.if0` | 86,575 | 1.731 | 10 | 200 | fits | 649,969 | 94 (11) | 0.034 |
| malformed MRPDU discard | `fixture.malformed.if0` | 276,733 | 5.535 | 10 | 18 | fits | 205,451 | 29 | 0.029 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 761,324 | 15.226 | 10 | 24 | MISS T_svc | 624,315 | 133 | 0.020 |
| LINK_DOWN | `fixture.link_down.if0` | 33,911 | 0.678 | 10 | 200 | fits | 645,002 | 39 (9) | 0.029 |
| BIND_RX | `fixture.bind_rx.if0` | 221,284 | 4.426 | 10 | 20 | fits | 453,466 | 83 (77) | 0.032 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 192,946 | 3.859 | 10 | 20 | fits | 1,198,802 | 159 (35) | 0.010 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 981,921 | 19.638 | 10 | 20 | MISS T_svc | 1,199,892 | 140 (29) | 0.008 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 737,071 | 14.741 | 10 | 200 | MISS T_svc | 699,974 | 225 | 0.021 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 737,071 | 14.741 | 10 | 200 | MISS T_svc | 699,974 | 225 | 0.021 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 736,936 | 14.739 | 10 | 20 | MISS T_svc | 699,974 | 225 | 0.021 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 736,936 | 14.739 | 10 | 20 | MISS T_svc | 699,974 | 225 | 0.021 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 737,039 | 14.741 | 10 | 24 | MISS T_svc | 699,974 | 225 | 0.021 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 737,039 | 14.741 | 10 | 24 | MISS T_svc | 699,974 | 225 | 0.021 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 737,006 | 14.740 | 10 | 50 | MISS T_svc | 699,974 | 225 | 0.021 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 737,006 | 14.740 | 10 | 50 | MISS T_svc | 699,974 | 225 | 0.021 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 1,338,824 | 26.776 | 10 | 18 | MISS ceiling | 601,850 | 42 | 0.044 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 1,338,824 | 26.776 | 10 | 18 | MISS ceiling | 601,850 | 42 | 0.044 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `adp-advertise`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
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
- `maap`: wait quiet TIMEOUT
- `maap`: wait quiet TIMEOUT
- `adp-link`: wait quiet TIMEOUT
- `adp-link`: wait quiet TIMEOUT
- `adp-gm`: wait quiet TIMEOUT
- `adp-discover`: wait quiet TIMEOUT
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
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
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
- `fixture`: wait quiet TIMEOUT
