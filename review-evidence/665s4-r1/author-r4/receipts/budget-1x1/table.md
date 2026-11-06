### 1x1

13 of 81 paths and 34 of 141 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 1.312 (2.807) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 9.360 (15.958) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 9.913 (15.751) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 15.169 (29.058) | MISS T_svc | 0 adp | 2 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 9.589 (14.302) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 9.359 (15.956) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 9.395 (15.987) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 9.784 (14.359) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 12.432 (31.231) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 2.645 (13.811) | fits | 1 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 2.211 (13.802) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 2.156 (12.075) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 1.680 (13.535) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 1.178 (27.198) | fits | 1 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.433 (11.761) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 9.535 (14.595) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.254 (1.169) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.077 (1.019) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.064 (3.063) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.078 (3.233) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.726 (1.655) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 1.259 (3.139) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.165 (2.943) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 2.498 (3.276) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.439 (3.217) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 2.422 (3.200) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 2.288 (3.065) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 2.289 (3.253) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 1.447 (2.224) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 2.832 (3.610) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 2.371 (3.148) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 2.339 (3.117) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.311 (3.089) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.442 (4.220) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 2.201 (2.979) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 2.202 (2.980) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 2.770 (3.548) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 2.697 (3.474) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 2.436 (3.214) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.369 (3.147) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 2.460 (3.238) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 2.463 (3.241) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 2.677 (3.454) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.741 (2.512) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 2.797 (4.182) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.123 (2.901) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 2.294 (3.256) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 5.105 (5.914) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 4.676 (5.460) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 4.796 (5.606) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 4.598 (5.212) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 4.835 (5.617) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 6.444 (7.570) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 4.757 (5.351) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 4.682 (5.465) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 38.079 (42.248) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 42.315 (52.000) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 39.049 (55.336) | MISS ceiling | 4 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 9.477 (17.653) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 95.542 (98.463) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 362.352 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 3.036 (4.199) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 1.007 (2.910) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.479 (1.377) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.531 (3.233) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.859 (2.910) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 1.316 (3.499) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp.service.acmp.first.if0` (backlog-adp) | 8.991 | fits | 0 acmp | 5 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 86.286 | MISS ceiling | 11 acmp | 5 | 4 |
| ADP record released under the composed load, first | 0 | `backlog-adp.service.adp.first.if0` (backlog-adp) | 8.981 | fits | 0 adp | 5 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 50.031 | MISS T_svc | 7 adp | 5 | 4 |
| AECP record released under the composed load, first | 0 | `backlog-adp.service.aecp.first.if0` (backlog-adp) | 9.026 | fits | 0 aecp | 5 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp-refill.service.aecp.last.if0` (backlog-adp-refill) | 254.467 | MISS ceiling | 15 aecp | 5 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog-adp.service.maap.first.if0` (backlog-adp) | 9.016 | fits | 0 maap | 5 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 50.068 | MISS ceiling | 6 maap | 5 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 579.034 | STARVED: never released | 0 srp | 5 | 4 |
| SRP record released under the composed load, last | 0 | `backlog-adp-refill.service.srp.last.if0` (backlog-adp-refill) | at least 579.014 | STARVED: never released | 31 srp | 5 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 3.262 (4.671) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 1.923 (1.923) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 1.603 (1.603) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 2.859 (3.233) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 91.092 | 21 | 447,619 (8.952) | yes | - |
| backlog-adp | 542.367 | 36 | 954,354 (19.087) | no | {'srp': 32} |
| backlog-adp-refill | 579.051 | 38 | 933,267 (18.665) | no | {'srp': 32} |
| backlog-owed | 362.402 | 52 | 397,188 (7.944) | yes | - |
| fixture | 10.219 | 3 | 300,707 (6.014) | yes | - |

Composed maximum over the 4 backlog windows: at least 954,354 CPU cycles (19.087 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 447,619 (8.952 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 58,913 | 1.178 | 10 | 20 | fits | 687,501 | 119 (14) | 0.035 |
| LINK_UP | `adp.link_up.if0` | 3,906 | 0.078 | 10 | 200 | fits | 161,665 | 88 (11) | 0.089 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 62,944 | 1.259 | 10 | 200 | fits | 66,618 | 46 (39) | 0.087 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 36,309 | 0.726 | 10 | 200 | fits | 3,930 | 9 (11) | 0.164 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 107,825 | 2.156 | 10 | 20 | fits | 603,738 | 130 (35) | 0.038 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 83,984 | 1.680 | 10 | 20 | fits | 676,730 | 117 (14) | 0.033 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 21,673 | 0.433 | 10 | 20 | fits | 588,075 | 108 (14) | 0.037 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 132,272 | 2.645 | 10 | 20 | fits | 690,545 | 140 (35) | 0.034 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 142,949 | 2.859 | 10 | 18 | fits | 161,665 | 88 | 0.089 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 96,127 | 1.923 | 10 | 18 | fits | 96,159 | 29 | 0.117 |
| malformed MRPDU discard | `srp.malformed.if0` | 80,143 | 1.603 | 10 | 18 | fits | 80,175 | 35 | 0.121 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 163,123 | 3.262 | 210 | 218 | fits | 233,539 | 78 | 0.092 |
| an event behind 15 others | `backlog.event.if0` | 473,866 | 9.477 | 10 | 200 | fits | 435,012 | 356 | 0.083 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 1,903,973 | 38.079 | 10 | 20 | MISS ceiling | 292,505 | 256 | 0.076 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 447,515 | 8.950 | 10 | 200 | fits | 447,619 | 389 | 0.081 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 1,526,886 | 30.538 | 10 | 200 | MISS T_svc | 293,630 | 279 | 0.080 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 445,386 | 8.908 | 10 | 20 | fits | 447,619 | 389 | 0.081 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 2,109,744 | 42.195 | 10 | 20 | MISS ceiling | 292,505 | 256 | 0.076 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 447,178 | 8.944 | 10 | 24 | fits | 447,619 | 389 | 0.081 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 4,098,633 | 81.973 | 10 | 24 | MISS ceiling | 211,291 | 169 | 0.070 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 446,658 | 8.933 | 10 | 50 | fits | 447,619 | 389 | 0.081 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 1,526,138 | 30.523 | 10 | 50 | MISS T_svc | 293,630 | 279 | 0.080 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 1,232,476 | 24.650 | 10 | 18 | MISS ceiling | 351,033 | 348 | 0.093 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 4,417,055 | 88.341 | 10 | 18 | MISS ceiling | 60,030 | 47 | 0.124 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 2,115,729 | 42.315 | 10 | 20 | MISS ceiling | 954,354 | 411 | 0.046 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 449,075 | 8.981 | 10 | 200 | fits | 547,209 | 402 | 0.065 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,501,541 | 50.031 | 10 | 200 | MISS T_svc | 954,354 | 411 | 0.046 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 449,531 | 8.991 | 10 | 20 | fits | 547,209 | 402 | 0.065 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 4,283,806 | 85.676 | 10 | 20 | MISS ceiling | 891,074 | 317 | 0.040 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 451,323 | 9.026 | 10 | 24 | fits | 547,209 | 402 | 0.065 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 12,693,585 | 253.872 | 10 | 24 | MISS ceiling | 804,979 | 230 | 0.033 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 450,803 | 9.016 | 10 | 50 | fits | 547,209 | 402 | 0.065 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,503,379 | 50.068 | 10 | 50 | MISS ceiling | 954,354 | 411 | 0.046 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 27,117,534 | 542.351 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 27,116,527 | 542.331 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 1,952,443 | 39.049 | 10 | 20 | MISS ceiling | 922,233 | 349 | 0.042 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 449,075 | 8.981 | 10 | 200 | fits | 547,209 | 402 | 0.065 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 2,316,507 | 46.330 | 10 | 200 | MISS T_svc | 922,233 | 349 | 0.042 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 449,531 | 8.991 | 10 | 20 | fits | 547,209 | 402 | 0.065 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 4,314,313 | 86.286 | 10 | 20 | MISS ceiling | 922,233 | 349 | 0.042 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 451,323 | 9.026 | 10 | 24 | fits | 547,209 | 402 | 0.065 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 12,723,339 | 254.467 | 10 | 24 | MISS ceiling | 804,991 | 230 | 0.033 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 450,803 | 9.016 | 10 | 50 | fits | 547,209 | 402 | 0.065 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,482,292 | 49.646 | 10 | 50 | MISS T_svc | 933,267 | 404 | 0.046 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 28,951,706 | 579.034 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 28,950,699 | 579.014 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 4,777,107 | 95.542 | 10 | 20 | MISS ceiling | 288,570 | 191 | 0.082 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,117,585 | 362.352 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,117,547 | 362.351 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,117,510 | 362.350 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,117,472 | 362.349 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 350,586 | 7.012 | 10 | 200 | fits | 345,892 | 341 | 0.086 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 1,422,676 | 28.454 | 10 | 200 | MISS T_svc | 397,188 | 300 | 0.095 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 348,457 | 6.969 | 10 | 20 | fits | 345,892 | 341 | 0.086 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 1,950,060 | 39.001 | 10 | 20 | MISS ceiling | 218,232 | 95 | 0.087 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 350,249 | 7.005 | 10 | 24 | fits | 345,892 | 341 | 0.086 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 5,430,557 | 108.611 | 10 | 24 | MISS ceiling | 183,074 | 125 | 0.051 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 349,729 | 6.995 | 10 | 50 | fits | 345,892 | 341 | 0.086 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 1,421,928 | 28.439 | 10 | 50 | MISS T_svc | 397,188 | 300 | 0.095 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 1,421,896 | 28.438 | 10 | 18 | MISS ceiling | 397,188 | 300 | 0.095 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 4,863,323 | 97.266 | 10 | 18 | MISS ceiling | 288,570 | 191 | 0.082 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 402,587 | 8.052 | 10 | 20 | fits | 785,920 | 150 (29) | 0.033 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 495,632 | 9.913 | 10 | 20 | fits | 787,574 | 156 (35) | 0.034 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 110,536 | 2.211 | 10 | 20 | fits | 690,096 | 140 (12) | 0.034 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 26,565 | 0.531 | 10 | 50 | fits | 161,665 | 88 | 0.089 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 65,810 | 1.316 | 10 | 50 | fits | 84,206 | 43 | 0.108 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 58,388 | 1.168 | 10 | 50 | fits | 68,759 | 37 | 0.098 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 42,945 | 0.859 | 10 | 50 | fits | 85,904 | 64 | 0.085 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 50,371 | 1.007 | 10 | 50 | fits | 85,904 | 64 | 0.085 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 23,929 | 0.479 | 10 | 50 | fits | 68,829 | 47 | 0.106 |
| LINK_UP | `adp.link_up.if0` | 3,906 | 0.078 | 10 | 200 | fits | 161,665 | 88 (11) | 0.089 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 62,944 | 1.259 | 10 | 200 | fits | 66,618 | 46 (39) | 0.087 |
| LINK_DOWN | `adp.link_down.if0` | 3,223 | 0.064 | 10 | 200 | fits | 153,131 | 27 (9) | 0.080 |
| LINK_UP | `adp.link_up.if0` | 3,906 | 0.078 | 10 | 200 | fits | 161,665 | 88 (11) | 0.089 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 62,944 | 1.259 | 10 | 200 | fits | 66,618 | 46 (39) | 0.087 |
| GM_CHANGE | `adp.gm_change.if0` | 3,874 | 0.077 | 10 | 200 | fits | 50,962 | 18 (11) | 0.097 |
| LINK_UP | `adp.link_up.if0` | 3,906 | 0.078 | 10 | 200 | fits | 161,665 | 88 (11) | 0.089 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 62,944 | 1.259 | 10 | 200 | fits | 66,618 | 46 (39) | 0.087 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 12,718 | 0.254 | 10 | 200 | fits | 58,441 | 38 (31) | 0.118 |
| LINK_UP | `adp.link_up.if0` | 3,906 | 0.078 | 10 | 200 | fits | 161,665 | 88 (11) | 0.089 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 62,944 | 1.259 | 10 | 200 | fits | 66,618 | 46 (39) | 0.087 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 12,718 | 0.254 | 10 | 200 | fits | 58,441 | 38 (31) | 0.118 |
| set_name | `aecp_fanout.set_name.if0` | 322,193 | 6.444 | 10 | 24 | fits | 378,520 | 623 | 0.042 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 229,921 | 4.598 | 10 | 24 | fits | 260,609 | 328 | 0.050 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 241,740 | 4.835 | 10 | 24 | fits | 280,835 | 348 | 0.050 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 222,034 | 4.441 | 10 | 24 | fits | 261,172 | 311 | 0.047 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 239,818 | 4.796 | 10 | 24 | fits | 280,298 | 351 | 0.046 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 255,256 | 5.105 | 10 | 24 | fits | 295,687 | 358 | 0.051 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 237,829 | 4.757 | 10 | 24 | fits | 267,537 | 324 | 0.054 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 233,796 | 4.676 | 10 | 24 | fits | 273,016 | 362 | 0.046 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 234,108 | 4.682 | 10 | 24 | fits | 273,246 | 362 | 0.045 |
| BIND_RX | `acmp.bind_rx.if0` | 65,588 | 1.312 | 10 | 20 | fits | 140,341 | 89 (77) | 0.097 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 621,589 | 12.432 | 10 | 20 | MISS T_svc | 707,227 | 143 (32) | 0.038 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 479,473 | 9.589 | 10 | 20 | fits | 715,092 | 158 (47) | 0.037 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 476,753 | 9.535 | 10 | 20 | fits | 729,739 | 161 (50) | 0.039 |
| PROBE_TX | `acmp.probe_tx.if0` | 489,185 | 9.784 | 10 | 20 | fits | 717,964 | 191 (48) | 0.036 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 469,763 | 9.395 | 10 | 20 | fits | 799,355 | 169 (48) | 0.034 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 467,990 | 9.360 | 10 | 20 | fits | 797,889 | 169 (48) | 0.034 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 467,955 | 9.359 | 10 | 20 | fits | 797,791 | 169 (48) | 0.034 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 87,060 | 1.741 | 10 | 24 | fits | 125,621 | 54 | 0.087 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 141,605 | 2.832 | 10 | 24 | fits | 180,500 | 126 | 0.053 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 118,528 | 2.371 | 10 | 24 | fits | 157,420 | 74 | 0.059 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 138,507 | 2.770 | 10 | 24 | fits | 177,399 | 91 | 0.065 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 123,020 | 2.460 | 10 | 24 | fits | 161,915 | 84 | 0.057 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 123,148 | 2.463 | 10 | 24 | fits | 162,043 | 84 | 0.057 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 133,830 | 2.677 | 10 | 24 | fits | 172,725 | 79 | 0.066 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 116,933 | 2.339 | 10 | 24 | fits | 155,828 | 69 | 0.059 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 115,537 | 2.311 | 10 | 24 | fits | 154,429 | 66 | 0.060 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 172,091 | 3.442 | 10 | 24 | fits | 210,983 | 167 | 0.055 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 110,049 | 2.201 | 10 | 24 | fits | 148,941 | 53 | 0.062 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 110,113 | 2.202 | 10 | 24 | fits | 149,005 | 53 | 0.062 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 134,826 | 2.697 | 10 | 24 | fits | 173,718 | 76 | 0.066 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 121,786 | 2.436 | 10 | 24 | fits | 160,678 | 76 | 0.058 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 118,467 | 2.369 | 10 | 24 | fits | 157,359 | 68 | 0.059 |
| get_configuration | `aecp.get_configuration.if0` | 121,974 | 2.439 | 10 | 24 | fits | 160,866 | 54 | 0.070 |
| entity_available | `aecp.entity_available.if0` | 108,251 | 2.165 | 10 | 24 | fits | 147,146 | 52 | 0.062 |
| get_name | `aecp.get_name.if0` | 114,379 | 2.288 | 10 | 24 | fits | 153,274 | 65 | 0.061 |
| get_counters | `aecp.get_counters.if0` | 121,095 | 2.422 | 10 | 24 | fits | 159,990 | 86 | 0.061 |
| get_avb_info | `aecp.get_avb_info.if0` | 124,911 | 2.498 | 10 | 24 | fits | 163,806 | 54 | 0.069 |
| unknown_command | `aecp.unknown_command.if0` | 106,166 | 2.123 | 10 | 24 | fits | 145,061 | 48 | 0.062 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 72,351 | 1.447 | 10 | 24 | fits | 111,189 | 52 | 0.079 |
| set_name | `aecp.set_name.if0` | 139,835 | 2.797 | 10 | 24 | fits | 209,087 | 127 | 0.062 |
| lock_entity | `aecp.lock_entity.if0` | 114,453 | 2.289 | 10 | 24 | fits | 162,670 | 77 | 0.064 |
| unlock_entity | `aecp.unlock_entity.if0` | 114,698 | 2.294 | 10 | 24 | fits | 162,790 | 78 | 0.063 |
| LINK_UP | `fixture.link_up.if0` | 3,906 | 0.078 | 10 | 200 | fits | 161,665 | 88 (11) | 0.089 |
| malformed MRPDU discard | `fixture.malformed.if0` | 60,074 | 1.201 | 10 | 18 | fits | 60,106 | 29 | 0.121 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 151,823 | 3.036 | 10 | 24 | fits | 209,970 | 128 | 0.062 |
| LINK_DOWN | `fixture.link_down.if0` | 3,223 | 0.064 | 10 | 200 | fits | 155,267 | 27 (9) | 0.079 |
| BIND_RX | `fixture.bind_rx.if0` | 65,482 | 1.310 | 10 | 20 | fits | 130,424 | 89 (77) | 0.095 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 74,003 | 1.480 | 10 | 20 | fits | 714,886 | 169 (35) | 0.037 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 758,464 | 15.169 | 10 | 20 | MISS T_svc | 784,547 | 150 (29) | 0.033 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 300,656 | 6.013 | 10 | 200 | fits | 300,707 | 245 | 0.088 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 300,656 | 6.013 | 10 | 200 | fits | 300,707 | 245 | 0.088 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 300,521 | 6.010 | 10 | 20 | fits | 300,707 | 245 | 0.088 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 300,521 | 6.010 | 10 | 20 | fits | 300,707 | 245 | 0.088 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 300,623 | 6.012 | 10 | 24 | fits | 300,707 | 245 | 0.088 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 300,623 | 6.012 | 10 | 24 | fits | 300,707 | 245 | 0.088 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 300,591 | 6.012 | 10 | 50 | fits | 300,707 | 245 | 0.088 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 300,591 | 6.012 | 10 | 50 | fits | 300,707 | 245 | 0.088 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 300,558 | 6.011 | 10 | 18 | fits | 300,707 | 245 | 0.088 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 300,558 | 6.011 | 10 | 18 | fits | 300,707 | 245 | 0.088 |

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
