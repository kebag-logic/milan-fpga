### 1x1

13 of 81 paths and 34 of 141 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 1.266 (2.751) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 8.428 (15.453) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 2.818 (13.576) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 6.466 (15.228) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 8.673 (13.853) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 8.417 (13.767) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 8.459 (15.483) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 7.197 (13.916) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 11.348 (30.262) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 2.789 (28.010) | fits | 3 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 1.373 (26.331) | fits | 2 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 3.732 (26.764) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 1.992 (13.109) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.504 (13.331) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.650 (13.043) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 10.290 (15.846) | MISS T_svc | 0 acmp | 1 | 1 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.513 (1.408) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.359 (1.272) | fits | 1 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.346 (3.301) | fits | 1 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.072 (3.186) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.567 (1.473) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 1.042 (2.867) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.122 (2.878) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 2.141 (2.898) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.381 (3.140) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 2.361 (3.117) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 2.247 (3.003) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 2.105 (3.057) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 1.405 (2.161) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 2.789 (3.545) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 2.327 (3.083) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 2.296 (3.052) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.269 (3.025) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.383 (4.141) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 2.158 (2.914) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 2.159 (2.915) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 2.713 (3.472) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 2.637 (3.395) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 2.393 (3.149) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.327 (3.083) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 2.417 (3.174) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 2.421 (3.177) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 2.620 (3.378) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.679 (2.430) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 2.636 (3.921) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.082 (2.838) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 2.106 (3.057) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 4.911 (5.707) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 4.660 (5.426) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 4.927 (5.725) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 4.615 (5.217) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 4.454 (5.221) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 6.451 (7.471) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 4.568 (5.150) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 4.672 (5.439) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 36.410 (40.219) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 37.074 (50.093) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 34.334 (55.298) | MISS ceiling | 2 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 8.989 (16.941) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 93.505 (95.484) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 363.686 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 2.881 (3.940) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 1.143 (2.993) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.451 (1.327) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.522 (3.186) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.991 (2.993) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 1.198 (3.025) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp.service.acmp.first.if0` (backlog-adp) | 8.897 | fits | 0 acmp | 5 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 81.433 | MISS ceiling | 11 acmp | 5 | 4 |
| ADP record released under the composed load, first | 0 | `backlog-adp.service.adp.first.if0` (backlog-adp) | 8.888 | fits | 0 adp | 5 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 44.629 | MISS T_svc | 7 adp | 5 | 4 |
| AECP record released under the composed load, first | 0 | `backlog-adp.service.aecp.first.if0` (backlog-adp) | 8.932 | fits | 0 aecp | 5 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp-refill.service.aecp.last.if0` (backlog-adp-refill) | 244.704 | MISS ceiling | 15 aecp | 5 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog-adp.service.maap.first.if0` (backlog-adp) | 8.922 | fits | 0 maap | 5 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 44.666 | MISS T_svc | 6 maap | 5 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 574.319 | STARVED: never released | 0 srp | 5 | 4 |
| SRP record released under the composed load, last | 0 | `backlog-adp-refill.service.srp.last.if0` (backlog-adp-refill) | at least 574.299 | STARVED: never released | 31 srp | 5 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 3.205 (4.599) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 1.875 (1.875) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 1.214 (1.215) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 2.811 (3.186) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 90.066 | 23 | 429,838 (8.597) | yes | - |
| backlog-adp | 537.127 | 37 | 948,763 (18.975) | no | {'srp': 32} |
| backlog-adp-refill | 574.336 | 39 | 966,218 (19.324) | no | {'srp': 32} |
| backlog-owed | 363.737 | 53 | 373,980 (7.480) | yes | - |
| fixture | 9.926 | 3 | 291,690 (5.834) | yes | - |

Composed maximum over the 4 backlog windows: at least 966,218 CPU cycles (19.324 ms), backlog-adp-refill, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 429,838 (8.597 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 25,223 | 0.504 | 10 | 20 | fits | 666,548 | 77 (14) | 0.032 |
| LINK_UP | `adp.link_up.if0` | 3,579 | 0.072 | 10 | 200 | fits | 159,306 | 88 (11) | 0.086 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 52,078 | 1.042 | 10 | 200 | fits | 65,119 | 46 (39) | 0.085 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 28,329 | 0.567 | 10 | 200 | fits | 3,517 | 9 (11) | 0.159 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 98,655 | 1.973 | 10 | 20 | fits | 584,087 | 95 (35) | 0.034 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 99,584 | 1.992 | 10 | 20 | fits | 655,474 | 75 (14) | 0.030 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 32,483 | 0.650 | 10 | 20 | fits | 652,127 | 76 (14) | 0.030 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 139,449 | 2.789 | 10 | 20 | fits | 668,224 | 98 (35) | 0.030 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 140,553 | 2.811 | 10 | 18 | fits | 159,306 | 88 | 0.086 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 93,730 | 1.875 | 10 | 18 | fits | 93,762 | 29 | 0.107 |
| malformed MRPDU discard | `srp.malformed.if0` | 60,702 | 1.214 | 10 | 18 | fits | 60,734 | 29 | 0.100 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 160,246 | 3.205 | 210 | 218 | fits | 229,945 | 78 | 0.086 |
| an event behind 15 others | `backlog.event.if0` | 449,427 | 8.989 | 10 | 200 | fits | 417,202 | 355 | 0.065 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 1,820,497 | 36.410 | 10 | 20 | MISS ceiling | 256,780 | 210 | 0.056 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 429,734 | 8.595 | 10 | 200 | fits | 429,838 | 388 | 0.063 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 1,468,658 | 29.373 | 10 | 200 | MISS T_svc | 284,755 | 278 | 0.063 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 427,605 | 8.552 | 10 | 20 | fits | 429,838 | 388 | 0.063 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 2,008,296 | 40.166 | 10 | 20 | MISS ceiling | 256,780 | 210 | 0.056 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 429,397 | 8.588 | 10 | 24 | fits | 429,838 | 388 | 0.063 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 3,937,823 | 78.756 | 10 | 24 | MISS ceiling | 177,397 | 123 | 0.045 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 428,877 | 8.578 | 10 | 50 | fits | 429,838 | 388 | 0.063 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 1,467,910 | 29.358 | 10 | 50 | MISS T_svc | 284,755 | 278 | 0.063 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 1,183,123 | 23.662 | 10 | 18 | MISS ceiling | 337,271 | 347 | 0.073 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 4,369,409 | 87.388 | 10 | 18 | MISS ceiling | 72,217 | 53 | 0.110 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 1,853,704 | 37.074 | 10 | 20 | MISS ceiling | 925,041 | 368 | 0.040 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 444,377 | 8.888 | 10 | 200 | fits | 717,268 | 393 | 0.043 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,231,449 | 44.629 | 10 | 200 | MISS T_svc | 925,041 | 368 | 0.040 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 444,833 | 8.897 | 10 | 20 | fits | 717,268 | 393 | 0.043 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 4,045,324 | 80.906 | 10 | 20 | MISS ceiling | 864,764 | 274 | 0.034 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 446,625 | 8.932 | 10 | 24 | fits | 717,268 | 393 | 0.043 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 12,209,294 | 244.186 | 10 | 24 | MISS ceiling | 874,206 | 230 | 0.034 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 446,105 | 8.922 | 10 | 50 | fits | 717,268 | 393 | 0.043 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,233,287 | 44.666 | 10 | 50 | MISS T_svc | 925,041 | 368 | 0.040 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 26,855,509 | 537.110 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 26,854,502 | 537.090 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 1,716,699 | 34.334 | 10 | 20 | MISS ceiling | 895,356 | 306 | 0.037 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 444,377 | 8.888 | 10 | 200 | fits | 717,268 | 393 | 0.043 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 2,073,838 | 41.477 | 10 | 200 | MISS T_svc | 895,356 | 306 | 0.037 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 444,833 | 8.897 | 10 | 20 | fits | 717,268 | 393 | 0.043 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 4,071,644 | 81.433 | 10 | 20 | MISS ceiling | 895,356 | 306 | 0.037 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 446,625 | 8.932 | 10 | 24 | fits | 717,268 | 393 | 0.043 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 12,235,196 | 244.704 | 10 | 24 | MISS ceiling | 874,198 | 230 | 0.034 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 446,105 | 8.922 | 10 | 50 | fits | 717,268 | 393 | 0.043 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,211,560 | 44.231 | 10 | 50 | MISS T_svc | 903,314 | 361 | 0.038 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 28,715,962 | 574.319 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 28,714,955 | 574.299 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 4,675,270 | 93.505 | 10 | 20 | MISS ceiling | 214,044 | 152 | 0.054 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,184,318 | 363.686 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,184,280 | 363.686 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,184,243 | 363.685 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,184,205 | 363.684 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 329,765 | 6.595 | 10 | 200 | fits | 341,065 | 340 | 0.066 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 1,402,331 | 28.047 | 10 | 200 | MISS T_svc | 373,980 | 299 | 0.078 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 327,636 | 6.553 | 10 | 20 | fits | 341,065 | 340 | 0.066 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 1,881,257 | 37.625 | 10 | 20 | MISS ceiling | 262,192 | 119 | 0.085 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 329,428 | 6.589 | 10 | 24 | fits | 341,065 | 340 | 0.066 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 5,318,426 | 106.369 | 10 | 24 | MISS ceiling | 196,300 | 130 | 0.052 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 328,908 | 6.578 | 10 | 50 | fits | 341,065 | 340 | 0.066 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 1,401,583 | 28.032 | 10 | 50 | MISS T_svc | 373,980 | 299 | 0.078 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 1,027,571 | 20.551 | 10 | 18 | MISS ceiling | 371,653 | 317 | 0.075 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 3,738,250 | 74.765 | 10 | 18 | MISS ceiling | 282,635 | 190 | 0.073 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 323,301 | 6.466 | 10 | 20 | fits | 761,387 | 101 (29) | 0.030 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 140,884 | 2.818 | 10 | 20 | fits | 678,812 | 104 (35) | 0.033 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 68,632 | 1.373 | 10 | 20 | fits | 584,291 | 95 (12) | 0.034 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 26,093 | 0.522 | 10 | 50 | fits | 159,306 | 88 | 0.086 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 59,898 | 1.198 | 10 | 50 | fits | 66,791 | 37 | 0.091 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 35,305 | 0.706 | 10 | 50 | fits | 66,840 | 37 | 0.091 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 49,558 | 0.991 | 10 | 50 | fits | 84,130 | 64 | 0.082 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 57,128 | 1.143 | 10 | 50 | fits | 84,130 | 64 | 0.082 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 22,558 | 0.451 | 10 | 50 | fits | 66,325 | 47 | 0.090 |
| LINK_UP | `adp.link_up.if0` | 3,579 | 0.072 | 10 | 200 | fits | 159,306 | 88 (11) | 0.086 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 52,078 | 1.042 | 10 | 200 | fits | 65,119 | 46 (39) | 0.085 |
| LINK_DOWN | `adp.link_down.if0` | 17,323 | 0.346 | 10 | 200 | fits | 165,038 | 33 (9) | 0.080 |
| LINK_UP | `adp.link_up.if0` | 3,579 | 0.072 | 10 | 200 | fits | 159,306 | 88 (11) | 0.086 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 52,078 | 1.042 | 10 | 200 | fits | 65,119 | 46 (39) | 0.085 |
| GM_CHANGE | `adp.gm_change.if0` | 17,964 | 0.359 | 10 | 200 | fits | 63,585 | 24 (11) | 0.098 |
| LINK_UP | `adp.link_up.if0` | 3,579 | 0.072 | 10 | 200 | fits | 159,306 | 88 (11) | 0.086 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 52,078 | 1.042 | 10 | 200 | fits | 65,119 | 46 (39) | 0.085 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 25,660 | 0.513 | 10 | 200 | fits | 70,411 | 44 (31) | 0.106 |
| LINK_UP | `adp.link_up.if0` | 3,579 | 0.072 | 10 | 200 | fits | 159,306 | 88 (11) | 0.086 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 52,078 | 1.042 | 10 | 200 | fits | 65,119 | 46 (39) | 0.085 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 25,660 | 0.513 | 10 | 200 | fits | 70,411 | 44 (31) | 0.106 |
| set_name | `aecp_fanout.set_name.if0` | 322,535 | 6.451 | 10 | 24 | fits | 373,550 | 602 | 0.055 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 230,745 | 4.615 | 10 | 24 | fits | 260,840 | 316 | 0.072 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 221,740 | 4.435 | 10 | 24 | fits | 260,051 | 299 | 0.067 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 222,696 | 4.454 | 10 | 24 | fits | 261,053 | 300 | 0.068 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 246,371 | 4.927 | 10 | 24 | fits | 286,242 | 351 | 0.067 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 245,528 | 4.911 | 10 | 24 | fits | 285,335 | 351 | 0.065 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 228,383 | 4.568 | 10 | 24 | fits | 257,498 | 317 | 0.073 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 232,983 | 4.660 | 10 | 24 | fits | 271,314 | 351 | 0.064 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 233,598 | 4.672 | 10 | 24 | fits | 271,955 | 351 | 0.065 |
| BIND_RX | `acmp.bind_rx.if0` | 63,313 | 1.266 | 10 | 20 | fits | 137,526 | 89 (77) | 0.090 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 567,383 | 11.348 | 10 | 20 | MISS T_svc | 684,863 | 101 (32) | 0.034 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 433,640 | 8.673 | 10 | 20 | fits | 692,668 | 116 (47) | 0.033 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 514,510 | 10.290 | 10 | 20 | MISS T_svc | 792,282 | 122 (50) | 0.032 |
| PROBE_TX | `acmp.probe_tx.if0` | 359,874 | 7.197 | 10 | 20 | fits | 695,793 | 149 (48) | 0.033 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 422,952 | 8.459 | 10 | 20 | fits | 774,136 | 120 (48) | 0.030 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 421,411 | 8.428 | 10 | 20 | fits | 772,671 | 120 (48) | 0.030 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 420,850 | 8.417 | 10 | 20 | fits | 688,340 | 117 (48) | 0.033 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 83,954 | 1.679 | 10 | 24 | fits | 121,496 | 53 | 0.076 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 139,427 | 2.789 | 10 | 24 | fits | 177,229 | 125 | 0.046 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 116,368 | 2.327 | 10 | 24 | fits | 154,167 | 73 | 0.051 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 135,660 | 2.713 | 10 | 24 | fits | 173,583 | 90 | 0.057 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 120,873 | 2.417 | 10 | 24 | fits | 158,675 | 83 | 0.050 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 121,040 | 2.421 | 10 | 24 | fits | 158,842 | 83 | 0.050 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 130,996 | 2.620 | 10 | 24 | fits | 168,922 | 78 | 0.059 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 114,786 | 2.296 | 10 | 24 | fits | 152,588 | 68 | 0.052 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 113,429 | 2.269 | 10 | 24 | fits | 151,228 | 65 | 0.052 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 169,146 | 3.383 | 10 | 24 | fits | 207,069 | 166 | 0.049 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 107,902 | 2.158 | 10 | 24 | fits | 145,701 | 52 | 0.054 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 107,966 | 2.159 | 10 | 24 | fits | 145,765 | 52 | 0.054 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 131,841 | 2.637 | 10 | 24 | fits | 169,764 | 75 | 0.058 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 119,639 | 2.393 | 10 | 24 | fits | 157,438 | 75 | 0.050 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 116,359 | 2.327 | 10 | 24 | fits | 154,158 | 67 | 0.051 |
| get_configuration | `aecp.get_configuration.if0` | 119,071 | 2.381 | 10 | 24 | fits | 156,994 | 53 | 0.062 |
| entity_available | `aecp.entity_available.if0` | 106,118 | 2.122 | 10 | 24 | fits | 143,920 | 51 | 0.054 |
| get_name | `aecp.get_name.if0` | 112,354 | 2.247 | 10 | 24 | fits | 150,156 | 64 | 0.053 |
| get_counters | `aecp.get_counters.if0` | 118,050 | 2.361 | 10 | 24 | fits | 155,852 | 80 | 0.053 |
| get_avb_info | `aecp.get_avb_info.if0` | 107,035 | 2.141 | 10 | 24 | fits | 144,899 | 46 | 0.055 |
| unknown_command | `aecp.unknown_command.if0` | 104,123 | 2.082 | 10 | 24 | fits | 141,925 | 47 | 0.054 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 70,264 | 1.405 | 10 | 24 | fits | 108,066 | 51 | 0.069 |
| set_name | `aecp.set_name.if0` | 131,823 | 2.636 | 10 | 24 | fits | 196,056 | 106 | 0.054 |
| lock_entity | `aecp.lock_entity.if0` | 105,274 | 2.105 | 10 | 24 | fits | 152,840 | 66 | 0.054 |
| unlock_entity | `aecp.unlock_entity.if0` | 105,305 | 2.106 | 10 | 24 | fits | 152,851 | 66 | 0.054 |
| LINK_UP | `fixture.link_up.if0` | 3,579 | 0.072 | 10 | 200 | fits | 159,306 | 88 (11) | 0.086 |
| malformed MRPDU discard | `fixture.malformed.if0` | 57,639 | 1.153 | 10 | 18 | fits | 57,671 | 29 | 0.105 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 144,039 | 2.881 | 10 | 24 | fits | 197,022 | 107 | 0.053 |
| LINK_DOWN | `fixture.link_down.if0` | 2,888 | 0.058 | 10 | 200 | fits | 152,928 | 27 (9) | 0.076 |
| BIND_RX | `fixture.bind_rx.if0` | 48,863 | 0.977 | 10 | 20 | fits | 113,015 | 82 (77) | 0.083 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 186,591 | 3.732 | 10 | 20 | fits | 607,356 | 124 (35) | 0.037 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 301,758 | 6.035 | 10 | 20 | fits | 759,983 | 101 (29) | 0.029 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 291,639 | 5.833 | 10 | 200 | fits | 291,690 | 245 | 0.074 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 291,639 | 5.833 | 10 | 200 | fits | 291,690 | 245 | 0.074 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 291,504 | 5.830 | 10 | 20 | fits | 291,690 | 245 | 0.074 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 291,504 | 5.830 | 10 | 20 | fits | 291,690 | 245 | 0.074 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 291,606 | 5.832 | 10 | 24 | fits | 291,690 | 245 | 0.074 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 291,606 | 5.832 | 10 | 24 | fits | 291,690 | 245 | 0.074 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 291,574 | 5.831 | 10 | 50 | fits | 291,690 | 245 | 0.074 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 291,574 | 5.831 | 10 | 50 | fits | 291,690 | 245 | 0.074 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 291,541 | 5.831 | 10 | 18 | fits | 291,690 | 245 | 0.074 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 291,541 | 5.831 | 10 | 18 | fits | 291,690 | 245 | 0.074 |

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
