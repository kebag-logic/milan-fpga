### 1x1

12 of 81 paths and 33 of 141 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.938 (2.368) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 7.865 (13.484) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.722 (14.944) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 5.804 (14.917) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 9.791 (15.235) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 9.544 (15.153) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 6.375 (13.530) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 8.228 (15.186) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 10.983 (29.660) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 1.676 (13.139) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.673 (13.125) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 2.290 (13.115) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 1.999 (25.552) | fits | 1 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 4.026 (25.850) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 4.407 (27.184) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 8.069 (15.530) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.190 (1.045) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.067 (0.940) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.055 (2.938) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.066 (3.081) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.730 (1.600) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.405 (2.157) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.068 (2.804) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 2.368 (3.111) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.029 (2.765) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 2.304 (3.042) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 2.195 (2.932) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 2.054 (2.976) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 1.351 (2.087) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 2.734 (3.472) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 2.274 (3.011) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 2.242 (2.979) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.214 (2.951) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.031 (3.768) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 2.104 (2.841) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 2.106 (2.843) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 2.361 (3.098) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 2.286 (3.023) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 2.340 (3.076) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.273 (3.010) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 2.364 (3.101) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 2.366 (3.103) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 2.546 (3.287) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.340 (2.070) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 2.568 (3.817) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.028 (2.765) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 2.052 (2.973) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 4.634 (5.407) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 4.379 (5.124) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 4.642 (5.416) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 4.329 (4.908) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 4.165 (4.910) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 6.435 (7.431) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 4.277 (4.836) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 4.385 (5.130) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 34.700 (38.421) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 35.403 (50.175) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 30.141 (52.320) | MISS ceiling | 2 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 8.570 (16.154) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 90.069 (92.604) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 364.418 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 2.809 (3.840) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 1.297 (3.073) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.420 (1.258) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.499 (3.081) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 1.149 (3.073) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 1.080 (2.835) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp.service.acmp.first.if0` (backlog-adp) | 8.367 | fits | 0 acmp | 5 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 77.031 | MISS ceiling | 11 acmp | 5 | 4 |
| ADP record released under the composed load, first | 0 | `backlog-adp.service.adp.first.if0` (backlog-adp) | 8.358 | fits | 0 adp | 5 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 42.719 | MISS T_svc | 7 adp | 5 | 4 |
| AECP record released under the composed load, first | 0 | `backlog-adp.service.aecp.first.if0` (backlog-adp) | 8.403 | fits | 0 aecp | 5 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp-refill.service.aecp.last.if0` (backlog-adp-refill) | 239.085 | MISS ceiling | 15 aecp | 5 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog-adp.service.maap.first.if0` (backlog-adp) | 8.393 | fits | 0 maap | 5 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 42.755 | MISS T_svc | 6 maap | 5 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 570.126 | STARVED: never released | 0 srp | 5 | 4 |
| SRP record released under the composed load, last | 0 | `backlog-adp-refill.service.srp.last.if0` (backlog-adp-refill) | at least 570.106 | STARVED: never released | 31 srp | 5 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 3.380 (4.690) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 1.781 (1.782) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 1.153 (1.153) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 2.738 (3.081) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 86.102 | 23 | 409,652 (8.193) | yes | - |
| backlog-adp | 535.456 | 37 | 900,689 (18.014) | no | {'srp': 32} |
| backlog-adp-refill | 570.143 | 40 | 880,522 (17.610) | no | {'srp': 32} |
| backlog-owed | 364.469 | 56 | 383,788 (7.676) | yes | - |
| fixture | 9.525 | 3 | 279,783 (5.596) | yes | - |

Composed maximum over the 4 backlog windows: at least 900,689 CPU cycles (18.014 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 409,652 (8.193 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 201,290 | 4.026 | 10 | 20 | fits | 653,751 | 77 (14) | 0.018 |
| LINK_UP | `adp.link_up.if0` | 3,299 | 0.066 | 10 | 200 | fits | 154,032 | 88 (11) | 0.062 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 20,247 | 0.405 | 10 | 200 | fits | 62,641 | 46 (39) | 0.061 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 36,522 | 0.730 | 10 | 200 | fits | 3,352 | 9 (11) | 0.130 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 114,485 | 2.290 | 10 | 20 | fits | 655,726 | 98 (35) | 0.017 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 99,972 | 1.999 | 10 | 20 | fits | 643,174 | 75 (14) | 0.016 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 220,335 | 4.407 | 10 | 20 | fits | 640,403 | 76 (14) | 0.016 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 83,776 | 1.676 | 10 | 20 | fits | 656,935 | 98 (35) | 0.018 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 136,903 | 2.738 | 10 | 18 | fits | 154,032 | 88 | 0.062 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 89,053 | 1.781 | 10 | 18 | fits | 89,085 | 29 | 0.075 |
| malformed MRPDU discard | `srp.malformed.if0` | 57,626 | 1.153 | 10 | 18 | fits | 57,658 | 29 | 0.068 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 168,983 | 3.380 | 210 | 218 | fits | 234,511 | 84 | 0.056 |
| an event behind 15 others | `backlog.event.if0` | 428,478 | 8.570 | 10 | 200 | fits | 398,069 | 355 | 0.033 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 1,735,006 | 34.700 | 10 | 20 | MISS ceiling | 248,143 | 210 | 0.032 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 409,548 | 8.191 | 10 | 200 | fits | 409,652 | 388 | 0.030 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 1,398,895 | 27.978 | 10 | 200 | MISS T_svc | 272,151 | 278 | 0.031 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 407,419 | 8.148 | 10 | 20 | fits | 409,652 | 388 | 0.030 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 1,918,398 | 38.368 | 10 | 20 | MISS ceiling | 248,143 | 210 | 0.032 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 409,211 | 8.184 | 10 | 24 | fits | 409,652 | 388 | 0.030 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 3,802,529 | 76.051 | 10 | 24 | MISS ceiling | 184,636 | 162 | 0.029 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 408,691 | 8.174 | 10 | 50 | fits | 409,652 | 388 | 0.030 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 1,398,147 | 27.963 | 10 | 50 | MISS T_svc | 272,151 | 278 | 0.031 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 1,125,964 | 22.519 | 10 | 18 | MISS ceiling | 319,431 | 347 | 0.034 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 4,177,365 | 83.547 | 10 | 18 | MISS ceiling | 47,483 | 29 | 0.048 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 1,770,173 | 35.403 | 10 | 20 | MISS ceiling | 900,689 | 368 | 0.020 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 417,901 | 8.358 | 10 | 200 | fits | 790,410 | 396 | 0.020 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,135,931 | 42.719 | 10 | 200 | MISS T_svc | 900,689 | 368 | 0.020 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 418,357 | 8.367 | 10 | 20 | fits | 790,410 | 396 | 0.020 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 3,829,369 | 76.587 | 10 | 20 | MISS ceiling | 846,562 | 274 | 0.019 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 420,149 | 8.403 | 10 | 24 | fits | 790,410 | 396 | 0.020 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 11,931,901 | 238.638 | 10 | 24 | MISS ceiling | 858,079 | 230 | 0.020 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 419,629 | 8.393 | 10 | 50 | fits | 790,410 | 396 | 0.020 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,137,769 | 42.755 | 10 | 50 | MISS T_svc | 900,689 | 368 | 0.020 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 26,771,978 | 535.440 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 26,770,971 | 535.419 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 1,507,058 | 30.141 | 10 | 20 | MISS ceiling | 874,104 | 306 | 0.020 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 417,901 | 8.358 | 10 | 200 | fits | 790,410 | 396 | 0.020 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 1,853,767 | 37.075 | 10 | 200 | MISS T_svc | 874,104 | 306 | 0.020 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 418,357 | 8.367 | 10 | 20 | fits | 790,410 | 396 | 0.020 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 3,851,573 | 77.031 | 10 | 20 | MISS ceiling | 874,104 | 306 | 0.020 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 420,149 | 8.403 | 10 | 24 | fits | 790,410 | 396 | 0.020 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 11,954,271 | 239.085 | 10 | 24 | MISS ceiling | 858,090 | 230 | 0.020 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 419,629 | 8.393 | 10 | 50 | fits | 790,410 | 396 | 0.020 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,117,602 | 42.352 | 10 | 50 | MISS T_svc | 880,522 | 361 | 0.019 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 28,506,321 | 570.126 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 28,505,314 | 570.106 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 4,503,459 | 90.069 | 10 | 20 | MISS ceiling | 194,296 | 146 | 0.035 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,220,925 | 364.418 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,220,887 | 364.418 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,220,850 | 364.417 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,220,812 | 364.416 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 325,298 | 6.506 | 10 | 200 | fits | 312,853 | 340 | 0.030 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 1,386,194 | 27.724 | 10 | 200 | MISS T_svc | 353,960 | 299 | 0.041 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 323,169 | 6.463 | 10 | 20 | fits | 312,853 | 340 | 0.030 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 1,842,673 | 36.853 | 10 | 20 | MISS ceiling | 246,844 | 119 | 0.046 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 324,961 | 6.499 | 10 | 24 | fits | 312,853 | 340 | 0.030 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 5,132,955 | 102.659 | 10 | 24 | MISS ceiling | 176,034 | 123 | 0.030 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 324,441 | 6.489 | 10 | 50 | fits | 312,853 | 340 | 0.030 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 1,385,446 | 27.709 | 10 | 50 | MISS T_svc | 353,960 | 299 | 0.041 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 1,031,454 | 20.629 | 10 | 18 | MISS ceiling | 383,788 | 336 | 0.043 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 3,195,942 | 63.919 | 10 | 18 | MISS ceiling | 180,292 | 170 | 0.057 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 290,189 | 5.804 | 10 | 20 | fits | 745,866 | 101 (29) | 0.015 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 36,102 | 0.722 | 10 | 20 | fits | 747,206 | 107 (35) | 0.015 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 33,635 | 0.673 | 10 | 20 | fits | 656,235 | 98 (12) | 0.017 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 24,970 | 0.499 | 10 | 50 | fits | 154,032 | 88 | 0.062 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 54,004 | 1.080 | 10 | 50 | fits | 64,518 | 37 | 0.069 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 49,588 | 0.992 | 10 | 50 | fits | 78,538 | 43 | 0.075 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 57,455 | 1.149 | 10 | 50 | fits | 81,091 | 64 | 0.057 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 64,866 | 1.297 | 10 | 50 | fits | 81,091 | 64 | 0.057 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 21,025 | 0.420 | 10 | 50 | fits | 62,918 | 47 | 0.056 |
| LINK_UP | `adp.link_up.if0` | 3,299 | 0.066 | 10 | 200 | fits | 154,032 | 88 (11) | 0.062 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 20,247 | 0.405 | 10 | 200 | fits | 62,641 | 46 (39) | 0.061 |
| LINK_DOWN | `adp.link_down.if0` | 2,654 | 0.053 | 10 | 200 | fits | 158,526 | 33 (9) | 0.054 |
| LINK_UP | `adp.link_up.if0` | 3,299 | 0.066 | 10 | 200 | fits | 154,032 | 88 (11) | 0.062 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 20,247 | 0.405 | 10 | 200 | fits | 62,641 | 46 (39) | 0.061 |
| GM_CHANGE | `adp.gm_change.if0` | 3,331 | 0.067 | 10 | 200 | fits | 46,994 | 18 (11) | 0.062 |
| LINK_UP | `adp.link_up.if0` | 3,299 | 0.066 | 10 | 200 | fits | 154,032 | 88 (11) | 0.062 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 20,247 | 0.405 | 10 | 200 | fits | 62,641 | 46 (39) | 0.061 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 9,484 | 0.190 | 10 | 200 | fits | 52,261 | 38 (31) | 0.056 |
| LINK_UP | `adp.link_up.if0` | 3,299 | 0.066 | 10 | 200 | fits | 154,032 | 88 (11) | 0.062 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 20,247 | 0.405 | 10 | 200 | fits | 62,641 | 46 (39) | 0.061 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 9,484 | 0.190 | 10 | 200 | fits | 52,261 | 38 (31) | 0.056 |
| set_name | `aecp_fanout.set_name.if0` | 321,733 | 6.435 | 10 | 24 | fits | 371,532 | 608 | 0.024 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 216,472 | 4.329 | 10 | 24 | fits | 245,377 | 317 | 0.026 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 208,175 | 4.163 | 10 | 24 | fits | 245,372 | 300 | 0.023 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 208,241 | 4.165 | 10 | 24 | fits | 245,504 | 299 | 0.023 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 232,111 | 4.642 | 10 | 24 | fits | 270,812 | 351 | 0.026 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 231,723 | 4.634 | 10 | 24 | fits | 270,361 | 351 | 0.026 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 213,853 | 4.277 | 10 | 24 | fits | 241,802 | 317 | 0.027 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 218,961 | 4.379 | 10 | 24 | fits | 256,182 | 351 | 0.020 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 219,254 | 4.385 | 10 | 24 | fits | 256,494 | 351 | 0.020 |
| BIND_RX | `acmp.bind_rx.if0` | 46,895 | 0.938 | 10 | 20 | fits | 118,402 | 82 (77) | 0.064 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 549,136 | 10.983 | 10 | 20 | MISS T_svc | 670,195 | 101 (32) | 0.018 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 489,557 | 9.791 | 10 | 20 | fits | 761,727 | 119 (47) | 0.016 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 403,437 | 8.069 | 10 | 20 | fits | 776,481 | 122 (50) | 0.018 |
| PROBE_TX | `acmp.probe_tx.if0` | 411,413 | 8.228 | 10 | 20 | fits | 759,299 | 121 (48) | 0.016 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 318,772 | 6.375 | 10 | 20 | fits | 676,510 | 117 (48) | 0.019 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 393,272 | 7.865 | 10 | 20 | fits | 674,214 | 117 (48) | 0.018 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 477,188 | 9.544 | 10 | 20 | fits | 757,648 | 120 (48) | 0.016 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 67,005 | 1.340 | 10 | 24 | fits | 103,482 | 46 | 0.048 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 136,710 | 2.734 | 10 | 24 | fits | 173,586 | 125 | 0.032 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 113,714 | 2.274 | 10 | 24 | fits | 150,555 | 73 | 0.036 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 118,035 | 2.361 | 10 | 24 | fits | 154,876 | 83 | 0.034 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 118,216 | 2.364 | 10 | 24 | fits | 155,060 | 83 | 0.034 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 118,325 | 2.366 | 10 | 24 | fits | 155,169 | 83 | 0.034 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 127,319 | 2.546 | 10 | 24 | fits | 164,349 | 78 | 0.040 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 112,092 | 2.242 | 10 | 24 | fits | 148,936 | 68 | 0.035 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 110,714 | 2.214 | 10 | 24 | fits | 147,555 | 65 | 0.036 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 151,542 | 3.031 | 10 | 24 | fits | 188,383 | 159 | 0.029 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 105,210 | 2.104 | 10 | 24 | fits | 142,051 | 52 | 0.037 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 105,309 | 2.106 | 10 | 24 | fits | 142,150 | 52 | 0.037 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 114,285 | 2.286 | 10 | 24 | fits | 151,126 | 68 | 0.035 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 116,982 | 2.340 | 10 | 24 | fits | 153,823 | 75 | 0.035 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 113,644 | 2.273 | 10 | 24 | fits | 150,485 | 67 | 0.035 |
| get_configuration | `aecp.get_configuration.if0` | 101,434 | 2.029 | 10 | 24 | fits | 138,275 | 46 | 0.038 |
| entity_available | `aecp.entity_available.if0` | 103,377 | 2.068 | 10 | 24 | fits | 140,221 | 51 | 0.037 |
| get_name | `aecp.get_name.if0` | 109,743 | 2.195 | 10 | 24 | fits | 146,587 | 64 | 0.037 |
| get_counters | `aecp.get_counters.if0` | 115,204 | 2.304 | 10 | 24 | fits | 152,101 | 80 | 0.036 |
| get_avb_info | `aecp.get_avb_info.if0` | 118,416 | 2.368 | 10 | 24 | fits | 155,540 | 53 | 0.044 |
| unknown_command | `aecp.unknown_command.if0` | 101,390 | 2.028 | 10 | 24 | fits | 138,234 | 47 | 0.036 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 67,566 | 1.351 | 10 | 24 | fits | 104,370 | 51 | 0.046 |
| set_name | `aecp.set_name.if0` | 128,386 | 2.568 | 10 | 24 | fits | 190,861 | 106 | 0.036 |
| lock_entity | `aecp.lock_entity.if0` | 102,719 | 2.054 | 10 | 24 | fits | 148,795 | 66 | 0.035 |
| unlock_entity | `aecp.unlock_entity.if0` | 102,592 | 2.052 | 10 | 24 | fits | 148,644 | 66 | 0.035 |
| LINK_UP | `fixture.link_up.if0` | 3,299 | 0.066 | 10 | 200 | fits | 154,032 | 88 (11) | 0.062 |
| malformed MRPDU discard | `fixture.malformed.if0` | 54,593 | 1.092 | 10 | 18 | fits | 54,625 | 29 | 0.071 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 140,456 | 2.809 | 10 | 24 | fits | 192,021 | 107 | 0.036 |
| LINK_DOWN | `fixture.link_down.if0` | 2,732 | 0.055 | 10 | 200 | fits | 146,893 | 27 (9) | 0.050 |
| BIND_RX | `fixture.bind_rx.if0` | 46,764 | 0.935 | 10 | 20 | fits | 108,726 | 82 (77) | 0.059 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 77,869 | 1.557 | 10 | 20 | fits | 677,111 | 127 (35) | 0.018 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 138,665 | 2.773 | 10 | 20 | fits | 661,583 | 98 (29) | 0.017 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 279,732 | 5.595 | 10 | 200 | fits | 279,783 | 245 | 0.046 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 279,732 | 5.595 | 10 | 200 | fits | 279,783 | 245 | 0.046 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 279,597 | 5.592 | 10 | 20 | fits | 279,783 | 245 | 0.046 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 279,597 | 5.592 | 10 | 20 | fits | 279,783 | 245 | 0.046 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 279,699 | 5.594 | 10 | 24 | fits | 279,783 | 245 | 0.046 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 279,699 | 5.594 | 10 | 24 | fits | 279,783 | 245 | 0.046 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 279,667 | 5.593 | 10 | 50 | fits | 279,783 | 245 | 0.046 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 279,667 | 5.593 | 10 | 50 | fits | 279,783 | 245 | 0.046 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 279,634 | 5.593 | 10 | 18 | fits | 279,783 | 245 | 0.046 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 279,634 | 5.593 | 10 | 18 | fits | 279,783 | 245 | 0.046 |

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
