### 1x1

14 of 81 paths and 35 of 141 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.814 (2.220) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 8.651 (15.427) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 6.429 (15.388) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 11.811 (15.328) | MISS T_svc | 0 adp | 2 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 8.991 (15.459) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 8.654 (15.425) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 10.384 (15.459) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 7.409 (12.100) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 11.889 (15.505) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 1.341 (13.464) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 2.168 (11.758) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 3.409 (28.352) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 1.181 (13.272) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 1.467 (26.739) | fits | 1 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 2.580 (26.438) | fits | 1 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 8.796 (14.212) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.203 (1.132) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.083 (1.044) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.068 (3.453) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.083 (3.209) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.837 (1.786) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.825 (2.741) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.082 (2.864) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 2.121 (2.903) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.056 (2.838) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 2.665 (3.447) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 2.222 (3.004) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 2.220 (3.163) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 1.689 (2.471) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 2.752 (3.534) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 2.303 (3.084) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 2.271 (3.053) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.556 (3.338) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.065 (3.847) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 2.133 (2.915) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 2.448 (3.230) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 2.395 (3.177) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 2.320 (3.102) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 2.368 (3.150) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.614 (3.396) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 2.706 (3.488) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 2.395 (3.177) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 2.301 (3.083) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.370 (2.143) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 2.698 (4.066) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.055 (2.837) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 2.220 (3.162) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 4.365 (5.179) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 4.243 (5.030) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 4.385 (5.202) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 4.180 (4.801) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 4.014 (4.801) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 6.290 (7.424) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 4.026 (4.627) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 4.249 (5.036) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 33.075 (36.664) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 37.086 (47.635) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 33.363 (53.731) | MISS ceiling | 2 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 8.632 (15.938) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 94.143 (95.734) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 104.915 (105.904) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 2.904 (4.078) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 1.004 (3.263) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.408 (1.322) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.500 (3.209) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.852 (3.263) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 1.520 (3.436) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp.service.acmp.first.if0` (backlog-adp) | 8.038 | fits | 0 acmp | 5 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 79.989 | MISS ceiling | 11 acmp | 5 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 8.062 | fits | 0 adp | 5 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 43.836 | MISS T_svc | 7 adp | 5 | 4 |
| AECP record released under the composed load, first | 0 | `backlog-adp.service.aecp.first.if0` (backlog-adp) | 8.073 | fits | 0 aecp | 5 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp-refill.service.aecp.last.if0` (backlog-adp-refill) | 245.188 | MISS ceiling | 15 aecp | 5 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog-adp.service.maap.first.if0` (backlog-adp) | 8.063 | fits | 0 maap | 5 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 43.873 | MISS T_svc | 6 maap | 5 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 573.349 | STARVED: never released | 0 srp | 5 | 4 |
| SRP record released under the composed load, last | 0 | `backlog-adp-refill.service.srp.last.if0` (backlog-adp-refill) | at least 573.329 | STARVED: never released | 31 srp | 5 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 3.231 (4.630) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 1.907 (1.908) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 1.587 (1.588) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 2.835 (3.209) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 88.079 | 23 | 403,220 (8.064) | yes | - |
| backlog-adp | 537.139 | 36 | 927,521 (18.550) | no | {'srp': 32} |
| backlog-adp-refill | 573.366 | 39 | 951,334 (19.027) | no | {'srp': 32} |
| backlog-owed | 108.811 | 29 | 370,044 (7.401) | yes | - |
| fixture | 9.765 | 3 | 228,231 (4.565) | yes | - |

Composed maximum over the 4 backlog windows: at least 951,334 CPU cycles (19.027 ms), backlog-adp-refill, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 403,220 (8.064 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 73,328 | 1.467 | 10 | 20 | fits | 673,026 | 119 (14) | 0.039 |
| LINK_UP | `adp.link_up.if0` | 4,142 | 0.083 | 10 | 200 | fits | 160,452 | 88 (11) | 0.093 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 41,270 | 0.825 | 10 | 200 | fits | 64,004 | 46 (39) | 0.101 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 41,847 | 0.837 | 10 | 200 | fits | 4,198 | 9 (11) | 0.193 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 170,438 | 3.409 | 10 | 20 | fits | 672,018 | 140 (35) | 0.038 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 59,048 | 1.181 | 10 | 20 | fits | 663,618 | 117 (14) | 0.038 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 128,976 | 2.580 | 10 | 20 | fits | 576,140 | 108 (14) | 0.042 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 67,044 | 1.341 | 10 | 20 | fits | 673,225 | 140 (35) | 0.038 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 141,727 | 2.835 | 10 | 18 | fits | 160,452 | 88 | 0.093 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 95,369 | 1.907 | 10 | 18 | fits | 95,401 | 29 | 0.112 |
| malformed MRPDU discard | `srp.malformed.if0` | 79,349 | 1.587 | 10 | 18 | fits | 79,381 | 35 | 0.114 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 161,528 | 3.231 | 210 | 218 | fits | 231,476 | 78 | 0.092 |
| an event behind 15 others | `backlog.event.if0` | 431,596 | 8.632 | 10 | 200 | fits | 393,691 | 356 | 0.068 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 1,653,762 | 33.075 | 10 | 20 | MISS ceiling | 226,928 | 211 | 0.051 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 403,116 | 8.062 | 10 | 200 | fits | 403,220 | 389 | 0.066 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 1,351,509 | 27.030 | 10 | 200 | MISS T_svc | 251,552 | 279 | 0.050 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 400,987 | 8.020 | 10 | 20 | fits | 403,220 | 389 | 0.066 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 1,830,578 | 36.612 | 10 | 20 | MISS ceiling | 226,928 | 211 | 0.051 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 402,779 | 8.056 | 10 | 24 | fits | 403,220 | 389 | 0.066 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 3,753,122 | 75.062 | 10 | 24 | MISS ceiling | 176,580 | 124 | 0.044 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 402,259 | 8.045 | 10 | 50 | fits | 403,220 | 389 | 0.066 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 1,350,761 | 27.015 | 10 | 50 | MISS T_svc | 251,552 | 279 | 0.050 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 1,099,177 | 21.984 | 10 | 18 | MISS ceiling | 303,454 | 348 | 0.058 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 4,111,646 | 82.233 | 10 | 18 | MISS ceiling | 56,707 | 47 | 0.083 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 1,854,288 | 37.086 | 10 | 20 | MISS ceiling | 893,466 | 411 | 0.040 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 401,426 | 8.029 | 10 | 200 | fits | 591,057 | 412 | 0.045 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,191,804 | 43.836 | 10 | 200 | MISS T_svc | 893,466 | 411 | 0.040 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 401,882 | 8.038 | 10 | 20 | fits | 591,057 | 412 | 0.045 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 3,962,988 | 79.260 | 10 | 20 | MISS ceiling | 927,521 | 327 | 0.035 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 403,674 | 8.073 | 10 | 24 | fits | 591,057 | 412 | 0.045 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 12,237,241 | 244.745 | 10 | 24 | MISS ceiling | 885,217 | 273 | 0.039 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 403,154 | 8.063 | 10 | 50 | fits | 591,057 | 412 | 0.045 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,193,642 | 43.873 | 10 | 50 | MISS T_svc | 893,466 | 411 | 0.040 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 26,856,093 | 537.122 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 26,855,086 | 537.102 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 1,668,174 | 33.363 | 10 | 20 | MISS ceiling | 951,334 | 359 | 0.036 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 401,426 | 8.029 | 10 | 200 | fits | 591,057 | 412 | 0.045 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 1,987,408 | 39.748 | 10 | 200 | MISS T_svc | 951,334 | 359 | 0.036 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 401,882 | 8.038 | 10 | 20 | fits | 591,057 | 412 | 0.045 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 3,985,214 | 79.704 | 10 | 20 | MISS ceiling | 951,334 | 359 | 0.036 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 403,674 | 8.073 | 10 | 24 | fits | 591,057 | 412 | 0.045 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 12,259,422 | 245.188 | 10 | 24 | MISS ceiling | 885,379 | 273 | 0.039 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 403,154 | 8.063 | 10 | 50 | fits | 591,057 | 412 | 0.045 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,177,194 | 43.544 | 10 | 50 | MISS T_svc | 877,018 | 404 | 0.038 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 28,667,437 | 573.349 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 28,666,430 | 573.329 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 4,707,149 | 94.143 | 10 | 20 | MISS ceiling | 204,691 | 153 | 0.056 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 4,894,651 | 97.893 | 10 | 20 | MISS ceiling | 187,512 | 147 | 0.048 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 5,081,848 | 101.637 | 10 | 20 | MISS ceiling | 187,234 | 146 | 0.049 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 5,185,693 | 103.714 | 10 | 20 | MISS ceiling | 77,090 | 39 | 0.109 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 5,245,726 | 104.915 | 10 | 20 | MISS ceiling | 56,686 | 31 | 0.099 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 313,826 | 6.277 | 10 | 200 | fits | 314,437 | 341 | 0.068 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 1,324,875 | 26.497 | 10 | 200 | MISS T_svc | 340,751 | 300 | 0.072 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 311,697 | 6.234 | 10 | 20 | fits | 314,437 | 341 | 0.068 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 3,999,428 | 79.989 | 10 | 20 | MISS ceiling | 214,690 | 168 | 0.051 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 313,489 | 6.270 | 10 | 24 | fits | 314,437 | 341 | 0.068 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 5,159,999 | 103.200 | 10 | 24 | MISS ceiling | 187,234 | 146 | 0.049 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 312,969 | 6.259 | 10 | 50 | fits | 314,437 | 341 | 0.068 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 1,324,127 | 26.483 | 10 | 50 | MISS T_svc | 340,751 | 300 | 0.072 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 983,344 | 19.667 | 10 | 18 | MISS ceiling | 370,044 | 337 | 0.074 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 3,338,664 | 66.773 | 10 | 18 | MISS ceiling | 257,963 | 172 | 0.069 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 356,795 | 7.136 | 10 | 20 | fits | 768,003 | 150 (29) | 0.035 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 321,432 | 6.429 | 10 | 20 | fits | 769,422 | 156 (35) | 0.035 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 108,392 | 2.168 | 10 | 20 | fits | 587,877 | 130 (12) | 0.042 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 25,019 | 0.500 | 10 | 50 | fits | 160,452 | 88 | 0.093 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 75,976 | 1.520 | 10 | 50 | fits | 83,763 | 43 | 0.115 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 22,247 | 0.445 | 10 | 50 | fits | 68,074 | 37 | 0.105 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 42,609 | 0.852 | 10 | 50 | fits | 99,777 | 70 | 0.106 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 50,201 | 1.004 | 10 | 50 | fits | 99,777 | 70 | 0.106 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 20,422 | 0.408 | 10 | 50 | fits | 66,086 | 47 | 0.093 |
| LINK_UP | `adp.link_up.if0` | 4,142 | 0.083 | 10 | 200 | fits | 160,452 | 88 (11) | 0.093 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 41,270 | 0.825 | 10 | 200 | fits | 64,004 | 46 (39) | 0.101 |
| LINK_DOWN | `adp.link_down.if0` | 3,360 | 0.067 | 10 | 200 | fits | 154,766 | 27 (9) | 0.090 |
| LINK_UP | `adp.link_up.if0` | 4,142 | 0.083 | 10 | 200 | fits | 160,452 | 88 (11) | 0.093 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 41,270 | 0.825 | 10 | 200 | fits | 64,004 | 46 (39) | 0.101 |
| GM_CHANGE | `adp.gm_change.if0` | 4,161 | 0.083 | 10 | 200 | fits | 52,189 | 18 (11) | 0.107 |
| LINK_UP | `adp.link_up.if0` | 4,142 | 0.083 | 10 | 200 | fits | 160,452 | 88 (11) | 0.093 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 41,270 | 0.825 | 10 | 200 | fits | 64,004 | 46 (39) | 0.101 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 10,135 | 0.203 | 10 | 200 | fits | 56,604 | 38 (31) | 0.094 |
| LINK_UP | `adp.link_up.if0` | 4,142 | 0.083 | 10 | 200 | fits | 160,452 | 88 (11) | 0.093 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 41,270 | 0.825 | 10 | 200 | fits | 64,004 | 46 (39) | 0.101 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 10,135 | 0.203 | 10 | 200 | fits | 56,604 | 38 (31) | 0.094 |
| set_name | `aecp_fanout.set_name.if0` | 314,504 | 6.290 | 10 | 24 | fits | 371,194 | 629 | 0.043 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 208,993 | 4.180 | 10 | 24 | fits | 240,041 | 329 | 0.050 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 200,355 | 4.007 | 10 | 24 | fits | 239,650 | 312 | 0.046 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 200,723 | 4.014 | 10 | 24 | fits | 240,061 | 312 | 0.046 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 219,257 | 4.385 | 10 | 24 | fits | 260,097 | 352 | 0.048 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 218,234 | 4.365 | 10 | 24 | fits | 258,955 | 352 | 0.045 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 201,297 | 4.026 | 10 | 24 | fits | 231,365 | 318 | 0.050 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 212,168 | 4.243 | 10 | 24 | fits | 251,480 | 363 | 0.045 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 212,466 | 4.249 | 10 | 24 | fits | 251,804 | 363 | 0.044 |
| BIND_RX | `acmp.bind_rx.if0` | 40,719 | 0.814 | 10 | 20 | fits | 111,022 | 83 (77) | 0.088 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 594,445 | 11.889 | 10 | 20 | MISS T_svc | 775,228 | 153 (32) | 0.036 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 449,542 | 8.991 | 10 | 20 | fits | 772,939 | 168 (47) | 0.035 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 439,808 | 8.796 | 10 | 20 | fits | 710,582 | 161 (50) | 0.041 |
| PROBE_TX | `acmp.probe_tx.if0` | 370,457 | 7.409 | 10 | 20 | fits | 604,999 | 181 (48) | 0.042 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 519,203 | 10.384 | 10 | 20 | MISS T_svc | 772,965 | 169 (48) | 0.035 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 432,545 | 8.651 | 10 | 20 | fits | 771,354 | 169 (48) | 0.035 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 432,699 | 8.654 | 10 | 20 | fits | 771,266 | 169 (48) | 0.035 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 68,493 | 1.370 | 10 | 24 | fits | 107,128 | 48 | 0.071 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 137,605 | 2.752 | 10 | 24 | fits | 176,700 | 125 | 0.048 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 115,125 | 2.303 | 10 | 24 | fits | 154,217 | 74 | 0.054 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 119,766 | 2.395 | 10 | 24 | fits | 158,858 | 85 | 0.052 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 135,284 | 2.706 | 10 | 24 | fits | 174,379 | 90 | 0.061 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 119,745 | 2.395 | 10 | 24 | fits | 158,840 | 84 | 0.052 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 115,048 | 2.301 | 10 | 24 | fits | 154,143 | 73 | 0.054 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 113,530 | 2.271 | 10 | 24 | fits | 152,625 | 69 | 0.054 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 127,815 | 2.556 | 10 | 24 | fits | 166,907 | 72 | 0.064 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 153,238 | 3.065 | 10 | 24 | fits | 192,330 | 161 | 0.044 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 106,646 | 2.133 | 10 | 24 | fits | 145,738 | 53 | 0.057 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 122,419 | 2.448 | 10 | 24 | fits | 161,511 | 59 | 0.066 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 116,016 | 2.320 | 10 | 24 | fits | 155,108 | 70 | 0.053 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 118,383 | 2.368 | 10 | 24 | fits | 157,475 | 76 | 0.053 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 130,705 | 2.614 | 10 | 24 | fits | 169,797 | 74 | 0.062 |
| get_configuration | `aecp.get_configuration.if0` | 102,820 | 2.056 | 10 | 24 | fits | 141,912 | 48 | 0.057 |
| entity_available | `aecp.entity_available.if0` | 104,108 | 2.082 | 10 | 24 | fits | 143,203 | 52 | 0.056 |
| get_name | `aecp.get_name.if0` | 111,092 | 2.222 | 10 | 24 | fits | 150,187 | 65 | 0.056 |
| get_counters | `aecp.get_counters.if0` | 133,261 | 2.665 | 10 | 24 | fits | 172,356 | 92 | 0.064 |
| get_avb_info | `aecp.get_avb_info.if0` | 106,061 | 2.121 | 10 | 24 | fits | 145,156 | 48 | 0.057 |
| unknown_command | `aecp.unknown_command.if0` | 102,744 | 2.055 | 10 | 24 | fits | 141,839 | 48 | 0.056 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 84,473 | 1.689 | 10 | 24 | fits | 123,568 | 58 | 0.082 |
| set_name | `aecp.set_name.if0` | 134,923 | 2.698 | 10 | 24 | fits | 203,292 | 128 | 0.053 |
| lock_entity | `aecp.lock_entity.if0` | 111,005 | 2.220 | 10 | 24 | fits | 158,159 | 78 | 0.058 |
| unlock_entity | `aecp.unlock_entity.if0` | 110,978 | 2.220 | 10 | 24 | fits | 158,115 | 78 | 0.058 |
| LINK_UP | `fixture.link_up.if0` | 4,142 | 0.083 | 10 | 200 | fits | 160,452 | 88 (11) | 0.093 |
| malformed MRPDU discard | `fixture.malformed.if0` | 59,142 | 1.183 | 10 | 18 | fits | 59,174 | 29 | 0.109 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 145,201 | 2.904 | 10 | 24 | fits | 203,882 | 127 | 0.053 |
| LINK_DOWN | `fixture.link_down.if0` | 3,384 | 0.068 | 10 | 200 | fits | 172,635 | 33 (9) | 0.096 |
| BIND_RX | `fixture.bind_rx.if0` | 40,719 | 0.814 | 10 | 20 | fits | 100,868 | 83 (77) | 0.083 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 30,351 | 0.607 | 10 | 20 | fits | 689,082 | 169 (35) | 0.039 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 590,530 | 11.811 | 10 | 20 | MISS T_svc | 766,381 | 150 (29) | 0.035 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 228,180 | 4.564 | 10 | 200 | fits | 228,231 | 225 | 0.058 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 228,180 | 4.564 | 10 | 200 | fits | 228,231 | 225 | 0.058 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 228,045 | 4.561 | 10 | 20 | fits | 228,231 | 225 | 0.058 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 228,045 | 4.561 | 10 | 20 | fits | 228,231 | 225 | 0.058 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 228,147 | 4.563 | 10 | 24 | fits | 228,231 | 225 | 0.058 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 228,147 | 4.563 | 10 | 24 | fits | 228,231 | 225 | 0.058 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 228,115 | 4.562 | 10 | 50 | fits | 228,231 | 225 | 0.058 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 228,115 | 4.562 | 10 | 50 | fits | 228,231 | 225 | 0.058 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 342,162 | 6.843 | 10 | 18 | fits | 114,080 | 37 | 0.117 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 342,162 | 6.843 | 10 | 18 | fits | 114,080 | 37 | 0.117 |

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
