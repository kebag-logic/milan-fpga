### 1x1

23 of 81 paths and 67 of 141 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 7.314 (15.059) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 4.394 (24.301) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 8.647 (25.247) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 20.160 (47.256) | MISS ceiling | 0 adp | 2 | 2 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 7.906 (27.241) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 6.461 (26.201) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 6.355 (26.224) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 6.320 (24.908) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 15.001 (27.842) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 3.745 (21.932) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 7.564 (46.087) | fits | 3 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 5.427 (21.872) | fits | 2 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 5.394 (45.460) | fits | 2 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 5.582 (25.693) | fits | 1 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 2.540 (22.455) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 6.160 (27.269) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 2.749 (7.831) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 2.243 (7.475) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 8.251 (18.271) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 1.744 (13.080) | fits | 1 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.369 (1.551) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 3.752 (10.057) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 4.973 (10.794) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 5.470 (11.029) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 5.984 (10.863) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 7.569 (12.619) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 7.557 (12.797) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 6.387 (9.113) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 4.054 (6.296) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 7.925 (12.983) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 6.642 (11.567) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 6.277 (11.202) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 5.255 (10.976) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 8.139 (13.155) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 6.388 (11.312) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 5.135 (10.854) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 5.405 (11.127) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 7.509 (12.524) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 6.612 (11.536) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 5.584 (8.002) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 7.479 (12.495) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 6.191 (13.260) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 5.589 (8.007) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 7.609 (11.254) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 8.217 (15.149) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 3.991 (6.284) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 8.828 (14.019) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 8.775 (13.823) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 9.478 (14.201) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 11.306 (16.355) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 8.094 (11.675) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 8.968 (14.050) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 10.553 (15.319) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 8.008 (12.909) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 9.382 (14.133) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 88.767 (98.965) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 76.055 (110.554) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 94.239 (110.224) | MISS ceiling | 6 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 38.025 (62.579) | MISS T_svc | 16 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 159.247 (166.899) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 860.002 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 16.043 (24.136) | MISS T_svc | 0 aecp | 1 | 1 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 2.704 (9.673) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 4.671 (9.969) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 4.167 (13.080) | fits | 1 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 2.561 (9.673) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 2.482 (8.238) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 24.109 | MISS ceiling | 0 acmp | 5 | 5 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 147.576 | MISS ceiling | 11 acmp | 5 | 5 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 24.152 | MISS T_svc | 0 adp | 5 | 5 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 107.620 | MISS T_svc | 6 adp | 5 | 5 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 24.145 | MISS ceiling | 0 aecp | 5 | 5 |
| AECP record released under the composed load, last | 0 | `backlog-adp.service.aecp.last.if0` (backlog-adp) | 415.145 | MISS ceiling | 15 aecp | 5 | 5 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 24.135 | MISS T_svc | 0 maap | 5 | 5 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 89.918 | MISS ceiling | 6 maap | 5 | 5 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 634.225 | STARVED: never released | 0 srp | 5 | 5 |
| SRP record released under the composed load, last | 0 | `backlog-adp-refill.service.srp.last.if0` (backlog-adp-refill) | at least 634.205 | STARVED: never released | 31 srp | 5 | 5 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 10.131 (12.775) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 10.133 (10.133) | MISS T_svc | 0 srp | 1 | 1 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 6.384 (8.418) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 10.996 (13.080) | MISS T_svc | 1 events | 1 | 1 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 250.252 | 28 | 1,178,156 (23.563) | yes | - |
| backlog-adp | 576.108 | 24 | 1,602,501 (32.050) | no | {'srp': 32} |
| backlog-adp-refill | 634.242 | 26 | 1,602,404 (32.048) | no | {'srp': 32} |
| backlog-owed | 860.053 | 84 | 1,033,286 (20.666) | yes | - |
| fixture | 20.000 | 2 | 760,031 (15.201) | yes | - |

Composed maximum over the 4 backlog windows: at least 1,602,501 CPU cycles (32.050 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 1,178,156 (23.563 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 279,122 | 5.582 | 10 | 20 | fits | 1,284,631 | 109 (14) | 0.013 |
| LINK_UP | `adp.link_up.if0` | 87,177 | 1.744 | 10 | 200 | fits | 654,018 | 94 (11) | 0.034 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 187,592 | 3.752 | 10 | 200 | fits | 321,326 | 52 (39) | 0.034 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 18,445 | 0.369 | 10 | 200 | fits | 77,549 | 15 (11) | 0.042 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 271,341 | 5.427 | 10 | 20 | fits | 1,093,592 | 120 (35) | 0.013 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 269,718 | 5.394 | 10 | 20 | fits | 1,140,659 | 107 (14) | 0.011 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 126,994 | 2.540 | 10 | 20 | fits | 1,122,771 | 108 (14) | 0.010 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 187,268 | 3.745 | 10 | 20 | fits | 1,096,581 | 120 (35) | 0.013 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 549,821 | 10.996 | 10 | 18 | MISS T_svc | 654,018 | 94 | 0.034 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 506,628 | 10.133 | 10 | 18 | MISS T_svc | 506,660 | 35 | 0.041 |
| malformed MRPDU discard | `srp.malformed.if0` | 307,891 | 6.158 | 10 | 18 | fits | 187,988 | 29 | 0.023 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 506,551 | 10.131 | 210 | 218 | fits | 638,738 | 84 | 0.019 |
| an event behind 15 others | `backlog.event.if0` | 1,901,235 | 38.025 | 10 | 200 | MISS T_svc | 1,120,127 | 339 | 0.017 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 4,438,362 | 88.767 | 10 | 20 | MISS ceiling | 588,513 | 217 | 0.013 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 1,207,597 | 24.152 | 10 | 200 | MISS T_svc | 1,178,156 | 389 | 0.018 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 3,648,095 | 72.962 | 10 | 200 | MISS T_svc | 649,391 | 291 | 0.013 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 1,205,468 | 24.109 | 10 | 20 | MISS ceiling | 1,178,156 | 389 | 0.018 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 4,818,335 | 96.367 | 10 | 20 | MISS ceiling | 588,513 | 217 | 0.013 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 1,207,260 | 24.145 | 10 | 24 | MISS ceiling | 1,178,156 | 389 | 0.018 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 9,411,839 | 188.237 | 10 | 24 | MISS ceiling | 462,965 | 169 | 0.015 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 1,206,740 | 24.135 | 10 | 50 | MISS T_svc | 1,178,156 | 389 | 0.018 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 3,647,347 | 72.947 | 10 | 50 | MISS ceiling | 649,391 | 291 | 0.013 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 7,096,772 | 141.935 | 10 | 18 | MISS ceiling | 474,071 | 169 | 0.015 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 11,346,169 | 226.923 | 10 | 18 | MISS ceiling | 143,622 | 47 | 0.018 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 3,802,760 | 76.055 | 10 | 20 | MISS ceiling | 1,518,624 | 401 | 0.009 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 1,081,798 | 21.636 | 10 | 200 | MISS T_svc | 1,049,855 | 402 | 0.011 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 4,494,048 | 89.881 | 10 | 200 | MISS T_svc | 1,518,624 | 401 | 0.009 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 1,082,254 | 21.645 | 10 | 20 | MISS ceiling | 1,049,855 | 402 | 0.011 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 7,350,139 | 147.003 | 10 | 20 | MISS ceiling | 1,428,952 | 307 | 0.009 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 1,084,046 | 21.681 | 10 | 24 | MISS T_svc | 1,049,855 | 402 | 0.011 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 20,757,237 | 415.145 | 10 | 24 | MISS ceiling | 1,348,256 | 230 | 0.008 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 1,083,526 | 21.671 | 10 | 50 | MISS T_svc | 1,049,855 | 402 | 0.011 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 4,495,886 | 89.918 | 10 | 50 | MISS ceiling | 1,518,624 | 401 | 0.009 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 28,804,565 | 576.091 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 28,803,558 | 576.071 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 4,711,973 | 94.239 | 10 | 20 | MISS ceiling | 1,485,074 | 339 | 0.009 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 1,081,798 | 21.636 | 10 | 200 | MISS T_svc | 1,049,855 | 402 | 0.011 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 5,380,989 | 107.620 | 10 | 200 | MISS T_svc | 1,485,074 | 339 | 0.009 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 1,082,254 | 21.645 | 10 | 20 | MISS ceiling | 1,049,855 | 402 | 0.011 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 7,378,795 | 147.576 | 10 | 20 | MISS ceiling | 1,485,074 | 339 | 0.009 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 1,084,046 | 21.681 | 10 | 24 | MISS T_svc | 1,049,855 | 402 | 0.011 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 20,741,906 | 414.838 | 10 | 24 | MISS ceiling | 1,348,281 | 230 | 0.008 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 1,083,526 | 21.671 | 10 | 50 | MISS T_svc | 1,049,855 | 402 | 0.011 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 4,448,575 | 88.972 | 10 | 50 | MISS ceiling | 1,471,313 | 394 | 0.009 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 31,711,236 | 634.225 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 31,710,229 | 634.205 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 7,962,332 | 159.247 | 10 | 20 | MISS ceiling | 526,696 | 152 | 0.017 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 43,000,111 | 860.002 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 43,000,073 | 860.001 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 8,688,717 | 173.774 | 10 | 20 | MISS ceiling | 765,910 | 197 | 0.018 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 42,999,998 | 860.000 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 807,039 | 16.141 | 10 | 200 | MISS T_svc | 733,531 | 341 | 0.013 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 3,227,729 | 64.555 | 10 | 200 | MISS T_svc | 1,033,286 | 287 | 0.020 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 804,910 | 16.098 | 10 | 20 | MISS T_svc | 733,531 | 341 | 0.013 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 4,754,845 | 95.097 | 10 | 20 | MISS ceiling | 659,683 | 195 | 0.016 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 806,702 | 16.134 | 10 | 24 | MISS T_svc | 733,531 | 341 | 0.013 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 10,955,015 | 219.100 | 10 | 24 | MISS ceiling | 682,222 | 175 | 0.017 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 806,182 | 16.124 | 10 | 50 | MISS T_svc | 733,531 | 341 | 0.013 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 3,226,981 | 64.540 | 10 | 50 | MISS ceiling | 1,033,286 | 287 | 0.020 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 3,226,949 | 64.539 | 10 | 18 | MISS ceiling | 1,033,286 | 287 | 0.020 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 15,650,347 | 313.007 | 10 | 18 | MISS ceiling | 374,215 | 53 | 0.022 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 975,509 | 19.510 | 10 | 20 | MISS T_svc | 1,256,346 | 140 (29) | 0.009 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 432,328 | 8.647 | 10 | 20 | fits | 1,262,347 | 146 (35) | 0.009 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 378,207 | 7.564 | 10 | 20 | fits | 1,144,870 | 130 (12) | 0.010 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 208,345 | 4.167 | 10 | 50 | fits | 654,018 | 94 | 0.034 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 100,540 | 2.011 | 10 | 50 | fits | 260,009 | 43 | 0.026 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 124,079 | 2.482 | 10 | 50 | fits | 197,550 | 37 | 0.023 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 128,069 | 2.561 | 10 | 50 | fits | 290,387 | 70 | 0.024 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 135,180 | 2.704 | 10 | 50 | fits | 290,387 | 70 | 0.024 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 233,533 | 4.671 | 10 | 50 | fits | 285,896 | 53 | 0.029 |
| LINK_UP | `adp.link_up.if0` | 87,177 | 1.744 | 10 | 200 | fits | 654,018 | 94 (11) | 0.034 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 187,592 | 3.752 | 10 | 200 | fits | 321,326 | 52 (39) | 0.034 |
| LINK_DOWN | `adp.link_down.if0` | 365,850 | 7.317 | 10 | 200 | fits | 506,597 | 33 (9) | 0.023 |
| LINK_UP | `adp.link_up.if0` | 87,177 | 1.744 | 10 | 200 | fits | 654,018 | 94 (11) | 0.034 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 187,592 | 3.752 | 10 | 200 | fits | 321,326 | 52 (39) | 0.034 |
| GM_CHANGE | `adp.gm_change.if0` | 112,144 | 2.243 | 10 | 200 | fits | 159,308 | 18 (11) | 0.024 |
| LINK_UP | `adp.link_up.if0` | 87,177 | 1.744 | 10 | 200 | fits | 654,018 | 94 (11) | 0.034 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 187,592 | 3.752 | 10 | 200 | fits | 321,326 | 52 (39) | 0.034 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 137,447 | 2.749 | 10 | 200 | fits | 177,118 | 38 (31) | 0.025 |
| LINK_UP | `adp.link_up.if0` | 87,177 | 1.744 | 10 | 200 | fits | 654,018 | 94 (11) | 0.034 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 187,592 | 3.752 | 10 | 200 | fits | 321,326 | 52 (39) | 0.034 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 137,447 | 2.749 | 10 | 200 | fits | 177,118 | 38 (31) | 0.025 |
| set_name | `aecp_fanout.set_name.if0` | 527,628 | 10.553 | 10 | 24 | MISS T_svc | 765,929 | 629 | 0.011 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 404,715 | 8.094 | 10 | 24 | fits | 583,750 | 335 | 0.013 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 448,419 | 8.968 | 10 | 24 | fits | 559,784 | 318 | 0.012 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 383,628 | 7.673 | 10 | 24 | fits | 483,987 | 311 | 0.010 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 565,301 | 11.306 | 10 | 24 | MISS T_svc | 582,292 | 351 | 0.012 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 438,740 | 8.775 | 10 | 24 | fits | 523,196 | 351 | 0.010 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 400,390 | 8.008 | 10 | 24 | fits | 477,790 | 317 | 0.010 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 473,910 | 9.478 | 10 | 24 | fits | 495,239 | 362 | 0.009 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 469,087 | 9.382 | 10 | 24 | fits | 491,670 | 363 | 0.009 |
| BIND_RX | `acmp.bind_rx.if0` | 365,696 | 7.314 | 10 | 20 | fits | 538,617 | 82 (77) | 0.036 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 750,047 | 15.001 | 10 | 20 | MISS T_svc | 1,392,104 | 143 (32) | 0.011 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 395,291 | 7.906 | 10 | 20 | fits | 1,362,050 | 158 (47) | 0.010 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 307,977 | 6.160 | 10 | 20 | fits | 1,363,426 | 151 (50) | 0.013 |
| PROBE_TX | `acmp.probe_tx.if0` | 315,983 | 6.320 | 10 | 20 | fits | 1,245,380 | 150 (48) | 0.011 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 317,760 | 6.355 | 10 | 20 | fits | 1,311,179 | 180 (48) | 0.012 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 219,700 | 4.394 | 10 | 20 | fits | 1,215,042 | 149 (48) | 0.011 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 323,026 | 6.461 | 10 | 20 | fits | 1,310,031 | 159 (48) | 0.009 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 380,447 | 7.609 | 10 | 24 | fits | 348,368 | 48 | 0.025 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 396,268 | 7.925 | 10 | 24 | fits | 440,278 | 132 | 0.015 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 332,115 | 6.642 | 10 | 24 | fits | 339,177 | 73 | 0.014 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 270,237 | 5.405 | 10 | 24 | fits | 341,751 | 85 | 0.013 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 373,972 | 7.479 | 10 | 24 | fits | 404,797 | 90 | 0.015 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 309,548 | 6.191 | 10 | 24 | fits | 341,497 | 83 | 0.013 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 279,444 | 5.589 | 10 | 24 | fits | 400,336 | 79 | 0.016 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 313,851 | 6.277 | 10 | 24 | fits | 335,417 | 68 | 0.014 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 262,774 | 5.255 | 10 | 24 | fits | 334,290 | 66 | 0.014 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 406,974 | 8.139 | 10 | 24 | fits | 437,777 | 167 | 0.013 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 319,380 | 6.388 | 10 | 24 | fits | 328,677 | 52 | 0.014 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 256,729 | 5.135 | 10 | 24 | fits | 328,986 | 53 | 0.014 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 375,428 | 7.509 | 10 | 24 | fits | 412,062 | 76 | 0.016 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 330,580 | 6.612 | 10 | 24 | fits | 340,207 | 75 | 0.013 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 279,224 | 5.584 | 10 | 24 | fits | 400,113 | 74 | 0.016 |
| get_configuration | `aecp.get_configuration.if0` | 299,211 | 5.984 | 10 | 24 | fits | 318,993 | 47 | 0.014 |
| entity_available | `aecp.entity_available.if0` | 248,654 | 4.973 | 10 | 24 | fits | 325,413 | 52 | 0.014 |
| get_name | `aecp.get_name.if0` | 377,858 | 7.557 | 10 | 24 | fits | 422,609 | 71 | 0.018 |
| get_counters | `aecp.get_counters.if0` | 378,447 | 7.569 | 10 | 24 | fits | 384,970 | 85 | 0.017 |
| get_avb_info | `aecp.get_avb_info.if0` | 273,492 | 5.470 | 10 | 24 | fits | 336,851 | 47 | 0.015 |
| unknown_command | `aecp.unknown_command.if0` | 199,536 | 3.991 | 10 | 24 | fits | 314,178 | 47 | 0.014 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 202,682 | 4.054 | 10 | 24 | fits | 314,783 | 58 | 0.018 |
| set_name | `aecp.set_name.if0` | 410,862 | 8.217 | 10 | 24 | fits | 531,936 | 127 | 0.017 |
| lock_entity | `aecp.lock_entity.if0` | 319,344 | 6.387 | 10 | 24 | fits | 455,649 | 84 | 0.018 |
| unlock_entity | `aecp.unlock_entity.if0` | 441,419 | 8.828 | 10 | 24 | fits | 455,974 | 84 | 0.018 |
| LINK_UP | `fixture.link_up.if0` | 87,177 | 1.744 | 10 | 200 | fits | 654,018 | 94 (11) | 0.034 |
| malformed MRPDU discard | `fixture.malformed.if0` | 319,197 | 6.384 | 10 | 18 | fits | 206,724 | 29 | 0.029 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 802,150 | 16.043 | 10 | 24 | MISS T_svc | 627,821 | 133 | 0.020 |
| LINK_DOWN | `fixture.link_down.if0` | 412,533 | 8.251 | 10 | 200 | fits | 513,432 | 33 (9) | 0.024 |
| BIND_RX | `fixture.bind_rx.if0` | 233,268 | 4.665 | 10 | 20 | fits | 456,337 | 83 (77) | 0.032 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 201,137 | 4.023 | 10 | 20 | fits | 1,203,593 | 159 (35) | 0.010 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 1,008,006 | 20.160 | 10 | 20 | MISS ceiling | 1,204,508 | 140 (29) | 0.008 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 798,470 | 15.969 | 10 | 200 | MISS T_svc | 760,031 | 231 | 0.022 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 798,470 | 15.969 | 10 | 200 | MISS T_svc | 760,031 | 231 | 0.022 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 798,335 | 15.967 | 10 | 20 | MISS T_svc | 760,031 | 231 | 0.022 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 798,335 | 15.967 | 10 | 20 | MISS T_svc | 760,031 | 231 | 0.022 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 798,438 | 15.969 | 10 | 24 | MISS T_svc | 760,031 | 231 | 0.022 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 798,438 | 15.969 | 10 | 24 | MISS T_svc | 760,031 | 231 | 0.022 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 798,405 | 15.968 | 10 | 50 | MISS T_svc | 760,031 | 231 | 0.022 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 798,405 | 15.968 | 10 | 50 | MISS T_svc | 760,031 | 231 | 0.022 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 1,377,374 | 27.547 | 10 | 18 | MISS ceiling | 579,001 | 36 | 0.047 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 1,377,374 | 27.547 | 10 | 18 | MISS ceiling | 579,001 | 36 | 0.047 |

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
- `adp-gm`: wait quiet TIMEOUT
- `adp-discover`: wait quiet TIMEOUT
- `adp-discover`: wait quiet TIMEOUT
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
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
