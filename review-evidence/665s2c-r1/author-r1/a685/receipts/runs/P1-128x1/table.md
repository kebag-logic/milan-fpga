### 1x1

13 of 81 paths and 34 of 141 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.959 (2.414) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 8.123 (13.626) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.794 (13.422) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 6.234 (15.063) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 10.038 (15.373) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 8.109 (13.617) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 6.578 (13.656) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 8.470 (15.329) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 11.271 (29.933) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 2.653 (26.053) | fits | 2 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 1.533 (13.215) | fits | 1 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 3.066 (28.142) | fits | 2 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 1.121 (12.970) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 2.548 (26.055) | fits | 2 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.753 (12.902) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 8.300 (15.682) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.215 (1.069) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.070 (0.947) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.056 (2.949) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.069 (3.091) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.634 (1.505) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.509 (2.262) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.082 (2.819) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 2.398 (3.139) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.041 (2.778) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 2.326 (3.063) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 2.210 (2.947) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 2.067 (2.995) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 1.367 (2.103) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 2.750 (3.488) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 2.289 (3.026) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 2.257 (2.994) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.230 (2.967) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.341 (4.082) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 2.120 (2.857) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 2.122 (2.859) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 2.669 (3.411) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 2.592 (3.333) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 2.354 (3.091) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.289 (3.026) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 2.379 (3.116) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 2.383 (3.120) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 2.576 (3.318) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.358 (2.089) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 2.601 (3.862) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.043 (2.780) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 2.067 (2.994) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 4.794 (5.572) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 4.537 (5.285) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 4.815 (5.595) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 4.502 (5.085) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 4.330 (5.079) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 6.618 (7.621) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 4.446 (5.010) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 4.548 (5.296) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 35.665 (39.425) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 37.037 (51.074) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 32.215 (52.982) | MISS ceiling | 2 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 8.778 (16.543) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 91.326 (93.873) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 364.160 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 2.846 (3.888) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 1.340 (3.120) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.440 (1.285) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.505 (3.091) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 1.189 (3.120) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.707 (2.466) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp.service.acmp.first.if0` (backlog-adp) | 9.495 | fits | 0 acmp | 5 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 79.212 | MISS ceiling | 11 acmp | 5 | 4 |
| ADP record released under the composed load, first | 0 | `backlog-adp.service.adp.first.if0` (backlog-adp) | 9.486 | fits | 0 adp | 5 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 44.487 | MISS T_svc | 7 adp | 5 | 4 |
| AECP record released under the composed load, first | 0 | `backlog-adp.service.aecp.first.if0` (backlog-adp) | 9.531 | fits | 0 aecp | 5 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp-refill.service.aecp.last.if0` (backlog-adp-refill) | 242.528 | MISS ceiling | 15 aecp | 5 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog-adp.service.maap.first.if0` (backlog-adp) | 9.520 | fits | 0 maap | 5 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 44.523 | MISS T_svc | 6 maap | 5 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 572.200 | STARVED: never released | 0 srp | 5 | 4 |
| SRP record released under the composed load, last | 0 | `backlog-adp-refill.service.srp.last.if0` (backlog-adp-refill) | at least 572.180 | STARVED: never released | 31 srp | 5 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 3.095 (4.403) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 1.795 (1.796) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 1.169 (1.169) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 2.751 (3.091) | fits | 0 events | 1 | 0 |

Composed windows: the longest pass is the composed maximum only where the window released its whole load.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 89.968 | 23 | 420,150 (8.403) | yes | - |
| backlog-adp | 537.090 | 37 | 947,828 (18.957) | no | {'srp': 32} |
| backlog-adp-refill | 572.217 | 40 | 947,604 (18.952) | no | {'srp': 32} |
| backlog-owed | 364.211 | 54 | 395,963 (7.919) | yes | - |
| fixture | 9.673 | 3 | 286,008 (5.720) | yes | - |

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 127,389 | 2.548 | 10 | 20 | fits | 576,456 | 74 (14) | 0.028 |
| LINK_UP | `adp.link_up.if0` | 3,475 | 0.069 | 10 | 200 | fits | 154,559 | 88 (11) | 0.064 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 25,438 | 0.509 | 10 | 200 | fits | 62,654 | 46 (39) | 0.062 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 31,686 | 0.634 | 10 | 200 | fits | 3,477 | 9 (11) | 0.149 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 115,349 | 2.307 | 10 | 20 | fits | 660,775 | 98 (35) | 0.023 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 56,069 | 1.121 | 10 | 20 | fits | 648,502 | 75 (14) | 0.022 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 37,642 | 0.753 | 10 | 20 | fits | 645,086 | 76 (14) | 0.022 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 132,654 | 2.653 | 10 | 20 | fits | 577,986 | 95 (35) | 0.026 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 137,544 | 2.751 | 10 | 18 | fits | 154,559 | 88 | 0.064 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 89,749 | 1.795 | 10 | 18 | fits | 89,781 | 29 | 0.081 |
| malformed MRPDU discard | `srp.malformed.if0` | 58,441 | 1.169 | 10 | 18 | fits | 58,473 | 29 | 0.077 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 154,763 | 3.095 | 210 | 218 | fits | 220,139 | 78 | 0.057 |
| an event behind 15 others | `backlog.event.if0` | 438,887 | 8.778 | 10 | 200 | fits | 406,978 | 355 | 0.049 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 1,783,245 | 35.665 | 10 | 20 | MISS ceiling | 252,624 | 210 | 0.045 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 420,046 | 8.401 | 10 | 200 | fits | 420,150 | 388 | 0.048 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 1,438,000 | 28.760 | 10 | 200 | MISS T_svc | 280,091 | 278 | 0.052 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 417,917 | 8.358 | 10 | 20 | fits | 420,150 | 388 | 0.048 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 1,968,599 | 39.372 | 10 | 20 | MISS ceiling | 252,624 | 210 | 0.045 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 419,709 | 8.394 | 10 | 24 | fits | 420,150 | 388 | 0.048 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 3,880,567 | 77.611 | 10 | 24 | MISS ceiling | 174,793 | 123 | 0.035 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 419,189 | 8.384 | 10 | 50 | fits | 420,150 | 388 | 0.048 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 1,437,252 | 28.745 | 10 | 50 | MISS T_svc | 280,091 | 278 | 0.052 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 1,157,129 | 23.143 | 10 | 18 | MISS ceiling | 331,189 | 347 | 0.060 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 4,228,165 | 84.563 | 10 | 18 | MISS ceiling | 55,129 | 47 | 0.077 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 1,851,851 | 37.037 | 10 | 20 | MISS ceiling | 913,169 | 368 | 0.030 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 474,292 | 9.486 | 10 | 200 | fits | 803,349 | 396 | 0.032 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,224,329 | 44.487 | 10 | 200 | MISS T_svc | 913,169 | 368 | 0.030 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 474,748 | 9.495 | 10 | 20 | fits | 803,349 | 396 | 0.032 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 3,935,057 | 78.701 | 10 | 20 | MISS ceiling | 855,037 | 274 | 0.026 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 476,540 | 9.531 | 10 | 24 | fits | 803,349 | 396 | 0.032 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 12,099,814 | 241.996 | 10 | 24 | MISS ceiling | 947,828 | 233 | 0.023 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 476,020 | 9.520 | 10 | 50 | fits | 803,349 | 396 | 0.032 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,226,167 | 44.523 | 10 | 50 | MISS T_svc | 913,169 | 368 | 0.030 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 26,853,656 | 537.073 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 26,852,649 | 537.053 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 1,610,759 | 32.215 | 10 | 20 | MISS ceiling | 884,663 | 306 | 0.029 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 474,292 | 9.486 | 10 | 200 | fits | 803,349 | 396 | 0.032 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 1,962,785 | 39.256 | 10 | 200 | MISS T_svc | 884,663 | 306 | 0.029 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 474,748 | 9.495 | 10 | 20 | fits | 803,349 | 396 | 0.032 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 3,960,591 | 79.212 | 10 | 20 | MISS ceiling | 884,663 | 306 | 0.029 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 476,540 | 9.531 | 10 | 24 | fits | 803,349 | 396 | 0.032 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 12,126,390 | 242.528 | 10 | 24 | MISS ceiling | 947,604 | 233 | 0.023 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 476,020 | 9.520 | 10 | 50 | fits | 803,349 | 396 | 0.032 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,205,145 | 44.103 | 10 | 50 | MISS T_svc | 892,147 | 361 | 0.029 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 28,610,022 | 572.200 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 28,609,015 | 572.180 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 4,566,319 | 91.326 | 10 | 20 | MISS ceiling | 195,460 | 145 | 0.040 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,208,015 | 364.160 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,207,977 | 364.160 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,207,940 | 364.159 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,207,902 | 364.158 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 361,119 | 7.222 | 10 | 200 | fits | 334,662 | 340 | 0.053 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 1,443,449 | 28.869 | 10 | 200 | MISS T_svc | 365,395 | 299 | 0.062 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 358,990 | 7.180 | 10 | 20 | fits | 334,662 | 340 | 0.053 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 1,911,942 | 38.239 | 10 | 20 | MISS ceiling | 254,700 | 119 | 0.066 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 360,782 | 7.216 | 10 | 24 | fits | 334,662 | 340 | 0.053 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 5,215,473 | 104.309 | 10 | 24 | MISS ceiling | 193,217 | 130 | 0.041 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 360,262 | 7.205 | 10 | 50 | fits | 334,662 | 340 | 0.053 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 1,442,701 | 28.854 | 10 | 50 | MISS T_svc | 365,395 | 299 | 0.062 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 1,077,274 | 21.545 | 10 | 18 | MISS ceiling | 395,963 | 336 | 0.064 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 3,444,998 | 68.900 | 10 | 18 | MISS ceiling | 260,403 | 184 | 0.054 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 311,695 | 6.234 | 10 | 20 | fits | 753,175 | 101 (29) | 0.022 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 39,722 | 0.794 | 10 | 20 | fits | 671,121 | 104 (35) | 0.025 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 76,632 | 1.533 | 10 | 20 | fits | 660,773 | 98 (12) | 0.022 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 25,239 | 0.505 | 10 | 50 | fits | 154,559 | 88 | 0.064 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 22,665 | 0.453 | 10 | 50 | fits | 64,718 | 37 | 0.070 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 35,367 | 0.707 | 10 | 50 | fits | 64,767 | 37 | 0.070 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 59,451 | 1.189 | 10 | 50 | fits | 81,799 | 64 | 0.063 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 67,021 | 1.340 | 10 | 50 | fits | 81,799 | 64 | 0.063 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 21,996 | 0.440 | 10 | 50 | fits | 64,242 | 47 | 0.070 |
| LINK_UP | `adp.link_up.if0` | 3,475 | 0.069 | 10 | 200 | fits | 154,559 | 88 (11) | 0.064 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 25,438 | 0.509 | 10 | 200 | fits | 62,654 | 46 (39) | 0.062 |
| LINK_DOWN | `adp.link_down.if0` | 2,775 | 0.055 | 10 | 200 | fits | 159,367 | 33 (9) | 0.058 |
| LINK_UP | `adp.link_up.if0` | 3,475 | 0.069 | 10 | 200 | fits | 154,559 | 88 (11) | 0.064 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 25,438 | 0.509 | 10 | 200 | fits | 62,654 | 46 (39) | 0.062 |
| GM_CHANGE | `adp.gm_change.if0` | 3,509 | 0.070 | 10 | 200 | fits | 47,364 | 18 (11) | 0.067 |
| LINK_UP | `adp.link_up.if0` | 3,475 | 0.069 | 10 | 200 | fits | 154,559 | 88 (11) | 0.064 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 25,438 | 0.509 | 10 | 200 | fits | 62,654 | 46 (39) | 0.062 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 10,775 | 0.215 | 10 | 200 | fits | 53,456 | 37 (31) | 0.076 |
| LINK_UP | `adp.link_up.if0` | 3,475 | 0.069 | 10 | 200 | fits | 154,559 | 88 (11) | 0.064 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 25,438 | 0.509 | 10 | 200 | fits | 62,654 | 46 (39) | 0.062 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 10,775 | 0.215 | 10 | 200 | fits | 53,456 | 37 (31) | 0.076 |
| set_name | `aecp_fanout.set_name.if0` | 330,913 | 6.618 | 10 | 24 | fits | 381,051 | 608 | 0.045 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 225,096 | 4.502 | 10 | 24 | fits | 254,233 | 317 | 0.056 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 216,027 | 4.321 | 10 | 24 | fits | 253,398 | 300 | 0.050 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 216,516 | 4.330 | 10 | 24 | fits | 253,933 | 299 | 0.051 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 240,742 | 4.815 | 10 | 24 | fits | 279,740 | 351 | 0.053 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 239,691 | 4.794 | 10 | 24 | fits | 278,625 | 351 | 0.050 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 222,321 | 4.446 | 10 | 24 | fits | 250,478 | 317 | 0.056 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 226,835 | 4.537 | 10 | 24 | fits | 264,226 | 351 | 0.047 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 227,390 | 4.548 | 10 | 24 | fits | 264,807 | 351 | 0.048 |
| BIND_RX | `acmp.bind_rx.if0` | 47,969 | 0.959 | 10 | 20 | fits | 120,692 | 82 (77) | 0.075 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 563,551 | 11.271 | 10 | 20 | MISS T_svc | 677,129 | 101 (32) | 0.026 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 501,881 | 10.038 | 10 | 20 | MISS T_svc | 768,632 | 119 (47) | 0.023 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 414,979 | 8.300 | 10 | 20 | fits | 784,110 | 122 (50) | 0.025 |
| PROBE_TX | `acmp.probe_tx.if0` | 423,500 | 8.470 | 10 | 20 | fits | 766,438 | 121 (48) | 0.022 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 328,908 | 6.578 | 10 | 20 | fits | 682,801 | 117 (48) | 0.025 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 406,144 | 8.123 | 10 | 20 | fits | 681,299 | 117 (48) | 0.025 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 405,442 | 8.109 | 10 | 20 | fits | 680,851 | 117 (48) | 0.025 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 67,901 | 1.358 | 10 | 24 | fits | 104,449 | 46 | 0.054 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 137,502 | 2.750 | 10 | 24 | fits | 174,384 | 125 | 0.035 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 114,462 | 2.289 | 10 | 24 | fits | 151,309 | 73 | 0.039 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 133,471 | 2.669 | 10 | 24 | fits | 170,535 | 90 | 0.045 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 118,949 | 2.379 | 10 | 24 | fits | 155,799 | 83 | 0.038 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 119,134 | 2.383 | 10 | 24 | fits | 155,984 | 83 | 0.038 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 128,813 | 2.576 | 10 | 24 | fits | 165,880 | 78 | 0.046 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 112,862 | 2.257 | 10 | 24 | fits | 149,712 | 68 | 0.039 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 111,523 | 2.230 | 10 | 24 | fits | 148,370 | 65 | 0.040 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 167,030 | 3.341 | 10 | 24 | fits | 204,094 | 166 | 0.038 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 105,978 | 2.120 | 10 | 24 | fits | 142,825 | 52 | 0.041 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 106,099 | 2.122 | 10 | 24 | fits | 142,946 | 52 | 0.041 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 129,587 | 2.592 | 10 | 24 | fits | 166,651 | 75 | 0.046 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 117,715 | 2.354 | 10 | 24 | fits | 154,562 | 75 | 0.038 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 114,453 | 2.289 | 10 | 24 | fits | 151,300 | 67 | 0.039 |
| get_configuration | `aecp.get_configuration.if0` | 102,054 | 2.041 | 10 | 24 | fits | 138,901 | 46 | 0.041 |
| entity_available | `aecp.entity_available.if0` | 104,110 | 2.082 | 10 | 24 | fits | 140,960 | 51 | 0.040 |
| get_name | `aecp.get_name.if0` | 110,496 | 2.210 | 10 | 24 | fits | 147,346 | 64 | 0.041 |
| get_counters | `aecp.get_counters.if0` | 116,293 | 2.326 | 10 | 24 | fits | 153,175 | 80 | 0.041 |
| get_avb_info | `aecp.get_avb_info.if0` | 119,893 | 2.398 | 10 | 24 | fits | 156,960 | 53 | 0.050 |
| unknown_command | `aecp.unknown_command.if0` | 102,134 | 2.043 | 10 | 24 | fits | 138,984 | 47 | 0.040 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 68,325 | 1.367 | 10 | 24 | fits | 105,143 | 51 | 0.051 |
| set_name | `aecp.set_name.if0` | 130,061 | 2.601 | 10 | 24 | fits | 193,079 | 106 | 0.044 |
| lock_entity | `aecp.lock_entity.if0` | 103,333 | 2.067 | 10 | 24 | fits | 149,732 | 66 | 0.041 |
| unlock_entity | `aecp.unlock_entity.if0` | 103,329 | 2.067 | 10 | 24 | fits | 149,708 | 66 | 0.041 |
| LINK_UP | `fixture.link_up.if0` | 3,475 | 0.069 | 10 | 200 | fits | 154,559 | 88 (11) | 0.064 |
| malformed MRPDU discard | `fixture.malformed.if0` | 55,296 | 1.106 | 10 | 18 | fits | 55,328 | 29 | 0.080 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 142,304 | 2.846 | 10 | 24 | fits | 194,382 | 107 | 0.045 |
| LINK_DOWN | `fixture.link_down.if0` | 2,814 | 0.056 | 10 | 200 | fits | 147,449 | 27 (9) | 0.052 |
| BIND_RX | `fixture.bind_rx.if0` | 47,864 | 0.957 | 10 | 20 | fits | 110,962 | 82 (77) | 0.072 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 153,313 | 3.066 | 10 | 20 | fits | 683,853 | 127 (35) | 0.025 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 166,377 | 3.328 | 10 | 20 | fits | 751,838 | 101 (29) | 0.022 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 285,957 | 5.719 | 10 | 200 | fits | 286,008 | 245 | 0.061 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 285,957 | 5.719 | 10 | 200 | fits | 286,008 | 245 | 0.061 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 285,822 | 5.716 | 10 | 20 | fits | 286,008 | 245 | 0.061 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 285,822 | 5.716 | 10 | 20 | fits | 286,008 | 245 | 0.061 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 285,924 | 5.718 | 10 | 24 | fits | 286,008 | 245 | 0.061 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 285,924 | 5.718 | 10 | 24 | fits | 286,008 | 245 | 0.061 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 285,892 | 5.718 | 10 | 50 | fits | 286,008 | 245 | 0.061 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 285,892 | 5.718 | 10 | 50 | fits | 286,008 | 245 | 0.061 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 285,859 | 5.717 | 10 | 18 | fits | 286,008 | 245 | 0.061 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 285,859 | 5.717 | 10 | 18 | fits | 286,008 | 245 | 0.061 |

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
