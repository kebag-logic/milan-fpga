### 1x1

12 of 81 paths and 33 of 141 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.931 (2.157) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 7.834 (13.469) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.468 (14.932) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 5.754 (14.902) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 9.749 (15.217) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 9.504 (15.134) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 6.317 (13.505) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 8.168 (15.171) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 10.945 (29.636) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 2.112 (13.098) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.440 (13.094) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 1.111 (13.529) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 4.106 (25.527) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 1.853 (13.050) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.938 (12.777) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 8.018 (15.497) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.186 (1.020) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.063 (0.915) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.050 (2.891) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.067 (3.029) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.370 (1.218) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.950 (2.650) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.030 (2.761) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 2.050 (2.781) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 1.989 (2.720) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 2.268 (3.000) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 2.156 (2.886) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 2.018 (2.933) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 1.321 (2.051) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 2.698 (3.432) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 2.236 (2.970) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 2.204 (2.938) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.177 (2.910) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 2.993 (3.726) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 2.067 (2.800) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 2.068 (2.801) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 2.323 (3.056) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 2.248 (2.981) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 2.301 (3.035) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.236 (2.969) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 2.326 (3.059) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 2.329 (3.063) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 2.229 (2.962) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.313 (2.037) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 2.527 (3.772) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 1.993 (2.723) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 2.018 (2.933) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 4.695 (5.460) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 4.454 (5.191) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 4.723 (5.490) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 4.412 (4.983) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 4.239 (4.977) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 6.501 (7.491) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 4.357 (4.908) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 4.465 (5.202) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 34.531 (38.231) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 35.119 (50.003) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 29.779 (52.213) | MISS ceiling | 2 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 8.542 (16.063) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 88.573 (90.323) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 363.787 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 2.776 (3.803) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.876 (2.600) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.413 (1.234) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.494 (3.029) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.729 (2.600) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.728 (2.430) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp.service.acmp.first.if0` (backlog-adp) | 8.192 | fits | 0 acmp | 5 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 76.646 | MISS ceiling | 11 acmp | 5 | 4 |
| ADP record released under the composed load, first | 0 | `backlog-adp.service.adp.first.if0` (backlog-adp) | 8.183 | fits | 0 adp | 5 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 42.409 | MISS T_svc | 7 adp | 5 | 4 |
| AECP record released under the composed load, first | 0 | `backlog-adp.service.aecp.first.if0` (backlog-adp) | 8.228 | fits | 0 aecp | 5 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp-refill.service.aecp.last.if0` (backlog-adp-refill) | 238.322 | MISS ceiling | 15 aecp | 5 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog-adp.service.maap.first.if0` (backlog-adp) | 8.218 | fits | 0 maap | 5 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 42.446 | MISS T_svc | 6 maap | 5 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 569.764 | STARVED: never released | 0 srp | 5 | 4 |
| SRP record released under the composed load, last | 0 | `backlog-adp-refill.service.srp.last.if0` (backlog-adp-refill) | at least 569.744 | STARVED: never released | 31 srp | 5 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 3.278 (4.546) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 1.713 (1.714) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 1.110 (1.111) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 2.699 (3.029) | fits | 0 events | 1 | 0 |

Composed windows: the longest pass is the composed maximum only where the window released its whole load.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 83.786 | 21 | 408,472 (8.169) | yes | - |
| backlog-adp | 535.172 | 37 | 899,129 (17.983) | no | {'srp': 32} |
| backlog-adp-refill | 569.781 | 40 | 878,605 (17.572) | no | {'srp': 32} |
| backlog-owed | 363.837 | 57 | 378,609 (7.572) | yes | - |
| fixture | 10.242 | 3 | 276,669 (5.533) | yes | - |

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 92,675 | 1.853 | 10 | 20 | fits | 652,491 | 77 (14) | 0.017 |
| LINK_UP | `adp.link_up.if0` | 3,337 | 0.067 | 10 | 200 | fits | 151,426 | 88 (11) | 0.049 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 47,496 | 0.950 | 10 | 200 | fits | 60,992 | 46 (39) | 0.044 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 18,518 | 0.370 | 10 | 200 | fits | 3,146 | 9 (11) | 0.094 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 39,739 | 0.795 | 10 | 20 | fits | 654,598 | 98 (35) | 0.016 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 205,278 | 4.106 | 10 | 20 | fits | 642,195 | 75 (14) | 0.015 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 46,894 | 0.938 | 10 | 20 | fits | 638,855 | 76 (14) | 0.015 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 105,604 | 2.112 | 10 | 20 | fits | 654,917 | 98 (35) | 0.016 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 134,958 | 2.699 | 10 | 18 | fits | 151,426 | 88 | 0.049 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 85,671 | 1.713 | 10 | 18 | fits | 85,703 | 29 | 0.052 |
| malformed MRPDU discard | `srp.malformed.if0` | 55,511 | 1.110 | 10 | 18 | fits | 55,543 | 29 | 0.044 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 163,880 | 3.278 | 210 | 218 | fits | 227,312 | 84 | 0.035 |
| an event behind 15 others | `backlog.event.if0` | 427,078 | 8.542 | 10 | 200 | fits | 394,669 | 355 | 0.027 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 1,726,548 | 34.531 | 10 | 20 | MISS ceiling | 247,108 | 210 | 0.030 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 408,368 | 8.167 | 10 | 200 | fits | 408,472 | 388 | 0.029 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 1,391,444 | 27.829 | 10 | 200 | MISS T_svc | 270,650 | 278 | 0.029 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 406,239 | 8.125 | 10 | 20 | fits | 408,472 | 388 | 0.029 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 1,908,893 | 38.178 | 10 | 20 | MISS ceiling | 247,108 | 210 | 0.030 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 408,031 | 8.161 | 10 | 24 | fits | 408,472 | 388 | 0.029 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 3,785,568 | 75.711 | 10 | 24 | MISS ceiling | 182,876 | 162 | 0.022 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 407,511 | 8.150 | 10 | 50 | fits | 408,472 | 388 | 0.029 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 1,390,696 | 27.814 | 10 | 50 | MISS T_svc | 270,650 | 278 | 0.029 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 1,120,014 | 22.400 | 10 | 18 | MISS ceiling | 318,061 | 347 | 0.032 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 4,063,410 | 81.268 | 10 | 18 | MISS ceiling | 52,303 | 47 | 0.040 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 1,755,959 | 35.119 | 10 | 20 | MISS ceiling | 899,129 | 368 | 0.019 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 409,163 | 8.183 | 10 | 200 | fits | 788,541 | 396 | 0.018 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,120,463 | 42.409 | 10 | 200 | MISS T_svc | 899,129 | 368 | 0.019 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 409,619 | 8.192 | 10 | 20 | fits | 788,541 | 396 | 0.018 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 3,810,474 | 76.209 | 10 | 20 | MISS ceiling | 844,734 | 274 | 0.018 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 411,411 | 8.228 | 10 | 24 | fits | 788,541 | 396 | 0.018 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 11,893,759 | 237.875 | 10 | 24 | MISS ceiling | 853,718 | 230 | 0.017 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 410,891 | 8.218 | 10 | 50 | fits | 788,541 | 396 | 0.018 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,122,301 | 42.446 | 10 | 50 | MISS T_svc | 899,129 | 368 | 0.019 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 26,757,764 | 535.155 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 26,756,757 | 535.135 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 1,488,926 | 29.779 | 10 | 20 | MISS ceiling | 872,770 | 306 | 0.019 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 409,163 | 8.183 | 10 | 200 | fits | 788,541 | 396 | 0.018 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 1,834,516 | 36.690 | 10 | 200 | MISS T_svc | 872,770 | 306 | 0.019 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 409,619 | 8.192 | 10 | 20 | fits | 788,541 | 396 | 0.018 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 3,832,322 | 76.646 | 10 | 20 | MISS ceiling | 872,770 | 306 | 0.019 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 411,411 | 8.228 | 10 | 24 | fits | 788,541 | 396 | 0.018 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 11,916,119 | 238.322 | 10 | 24 | MISS ceiling | 853,703 | 230 | 0.017 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 410,891 | 8.218 | 10 | 50 | fits | 788,541 | 396 | 0.018 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,101,777 | 42.036 | 10 | 50 | MISS T_svc | 878,605 | 361 | 0.018 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 28,488,189 | 569.764 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 28,487,182 | 569.744 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 4,428,644 | 88.573 | 10 | 20 | MISS ceiling | 192,237 | 146 | 0.028 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,189,326 | 363.787 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,189,288 | 363.786 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,189,251 | 363.785 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,189,213 | 363.784 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 320,589 | 6.412 | 10 | 200 | fits | 323,210 | 340 | 0.030 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 1,358,669 | 27.173 | 10 | 200 | MISS T_svc | 350,467 | 299 | 0.035 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 318,460 | 6.369 | 10 | 20 | fits | 323,210 | 340 | 0.030 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 1,810,289 | 36.206 | 10 | 20 | MISS ceiling | 243,204 | 119 | 0.037 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 320,252 | 6.405 | 10 | 24 | fits | 323,210 | 340 | 0.030 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 5,051,333 | 101.027 | 10 | 24 | MISS ceiling | 174,275 | 124 | 0.022 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 319,732 | 6.395 | 10 | 50 | fits | 323,210 | 340 | 0.030 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 1,357,921 | 27.158 | 10 | 50 | MISS T_svc | 350,467 | 299 | 0.035 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 1,007,422 | 20.148 | 10 | 18 | MISS ceiling | 378,609 | 336 | 0.035 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 3,016,325 | 60.327 | 10 | 18 | MISS ceiling | 59,683 | 32 | 0.051 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 287,686 | 5.754 | 10 | 20 | fits | 745,102 | 101 (29) | 0.014 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 23,396 | 0.468 | 10 | 20 | fits | 746,597 | 107 (35) | 0.015 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 22,011 | 0.440 | 10 | 20 | fits | 654,705 | 98 (12) | 0.016 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 24,711 | 0.494 | 10 | 50 | fits | 151,426 | 88 | 0.049 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 21,344 | 0.427 | 10 | 50 | fits | 62,571 | 37 | 0.048 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 36,408 | 0.728 | 10 | 50 | fits | 62,585 | 37 | 0.047 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 36,460 | 0.729 | 10 | 50 | fits | 79,173 | 64 | 0.041 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 43,792 | 0.876 | 10 | 50 | fits | 79,173 | 64 | 0.041 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 20,647 | 0.413 | 10 | 50 | fits | 61,722 | 47 | 0.042 |
| LINK_UP | `adp.link_up.if0` | 3,337 | 0.067 | 10 | 200 | fits | 151,426 | 88 (11) | 0.049 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 47,496 | 0.950 | 10 | 200 | fits | 60,992 | 46 (39) | 0.044 |
| LINK_DOWN | `adp.link_down.if0` | 2,484 | 0.050 | 10 | 200 | fits | 156,145 | 33 (9) | 0.043 |
| LINK_UP | `adp.link_up.if0` | 3,337 | 0.067 | 10 | 200 | fits | 151,426 | 88 (11) | 0.049 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 47,496 | 0.950 | 10 | 200 | fits | 60,992 | 46 (39) | 0.044 |
| GM_CHANGE | `adp.gm_change.if0` | 3,152 | 0.063 | 10 | 200 | fits | 45,731 | 18 (11) | 0.043 |
| LINK_UP | `adp.link_up.if0` | 3,337 | 0.067 | 10 | 200 | fits | 151,426 | 88 (11) | 0.049 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 47,496 | 0.950 | 10 | 200 | fits | 60,992 | 46 (39) | 0.044 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 9,294 | 0.186 | 10 | 200 | fits | 50,985 | 38 (31) | 0.039 |
| LINK_UP | `adp.link_up.if0` | 3,337 | 0.067 | 10 | 200 | fits | 151,426 | 88 (11) | 0.049 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 47,496 | 0.950 | 10 | 200 | fits | 60,992 | 46 (39) | 0.044 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 9,294 | 0.186 | 10 | 200 | fits | 50,985 | 38 (31) | 0.039 |
| set_name | `aecp_fanout.set_name.if0` | 325,074 | 6.501 | 10 | 24 | fits | 374,541 | 608 | 0.032 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 220,602 | 4.412 | 10 | 24 | fits | 249,128 | 317 | 0.041 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 211,665 | 4.233 | 10 | 24 | fits | 248,514 | 300 | 0.036 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 211,971 | 4.239 | 10 | 24 | fits | 248,866 | 299 | 0.037 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 236,147 | 4.723 | 10 | 24 | fits | 274,480 | 351 | 0.040 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 234,734 | 4.695 | 10 | 24 | fits | 273,001 | 351 | 0.035 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 217,874 | 4.357 | 10 | 24 | fits | 245,420 | 317 | 0.041 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 222,689 | 4.454 | 10 | 24 | fits | 259,544 | 351 | 0.033 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 223,248 | 4.465 | 10 | 24 | fits | 260,125 | 351 | 0.034 |
| BIND_RX | `acmp.bind_rx.if0` | 46,471 | 0.929 | 10 | 20 | fits | 117,436 | 82 (77) | 0.058 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 547,249 | 10.945 | 10 | 20 | MISS T_svc | 669,342 | 101 (32) | 0.018 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 487,462 | 9.749 | 10 | 20 | fits | 760,838 | 119 (47) | 0.015 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 400,892 | 8.018 | 10 | 20 | fits | 774,865 | 122 (50) | 0.017 |
| PROBE_TX | `acmp.probe_tx.if0` | 408,425 | 8.168 | 10 | 20 | fits | 758,544 | 121 (48) | 0.015 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 315,862 | 6.317 | 10 | 20 | fits | 675,226 | 117 (48) | 0.017 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 391,695 | 7.834 | 10 | 20 | fits | 673,433 | 117 (48) | 0.017 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 475,180 | 9.504 | 10 | 20 | fits | 756,685 | 120 (48) | 0.015 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 65,663 | 1.313 | 10 | 24 | fits | 101,872 | 46 | 0.038 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 134,886 | 2.698 | 10 | 24 | fits | 171,580 | 125 | 0.024 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 111,819 | 2.236 | 10 | 24 | fits | 148,478 | 73 | 0.025 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 116,164 | 2.323 | 10 | 24 | fits | 152,823 | 83 | 0.025 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 116,307 | 2.326 | 10 | 24 | fits | 152,969 | 83 | 0.025 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 116,474 | 2.329 | 10 | 24 | fits | 153,136 | 83 | 0.025 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 111,446 | 2.229 | 10 | 24 | fits | 148,108 | 71 | 0.025 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 110,220 | 2.204 | 10 | 24 | fits | 146,882 | 68 | 0.025 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 108,863 | 2.177 | 10 | 24 | fits | 145,522 | 65 | 0.026 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 149,636 | 2.993 | 10 | 24 | fits | 186,295 | 159 | 0.020 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 103,336 | 2.067 | 10 | 24 | fits | 139,995 | 52 | 0.027 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 103,400 | 2.068 | 10 | 24 | fits | 140,059 | 52 | 0.026 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 112,414 | 2.248 | 10 | 24 | fits | 149,073 | 68 | 0.025 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 115,073 | 2.301 | 10 | 24 | fits | 151,732 | 75 | 0.025 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 111,793 | 2.236 | 10 | 24 | fits | 148,452 | 67 | 0.025 |
| get_configuration | `aecp.get_configuration.if0` | 99,455 | 1.989 | 10 | 24 | fits | 135,983 | 46 | 0.026 |
| entity_available | `aecp.entity_available.if0` | 101,495 | 2.030 | 10 | 24 | fits | 138,026 | 51 | 0.025 |
| get_name | `aecp.get_name.if0` | 107,776 | 2.156 | 10 | 24 | fits | 144,307 | 64 | 0.026 |
| get_counters | `aecp.get_counters.if0` | 113,425 | 2.268 | 10 | 24 | fits | 149,988 | 80 | 0.026 |
| get_avb_info | `aecp.get_avb_info.if0` | 102,498 | 2.050 | 10 | 24 | fits | 139,029 | 46 | 0.026 |
| unknown_command | `aecp.unknown_command.if0` | 99,630 | 1.993 | 10 | 24 | fits | 136,161 | 47 | 0.026 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 66,057 | 1.321 | 10 | 24 | fits | 102,536 | 51 | 0.033 |
| set_name | `aecp.set_name.if0` | 126,329 | 2.527 | 10 | 24 | fits | 188,625 | 106 | 0.028 |
| lock_entity | `aecp.lock_entity.if0` | 100,876 | 2.018 | 10 | 24 | fits | 146,639 | 66 | 0.026 |
| unlock_entity | `aecp.unlock_entity.if0` | 100,907 | 2.018 | 10 | 24 | fits | 146,646 | 66 | 0.026 |
| LINK_UP | `fixture.link_up.if0` | 3,337 | 0.067 | 10 | 200 | fits | 151,426 | 88 (11) | 0.049 |
| malformed MRPDU discard | `fixture.malformed.if0` | 52,691 | 1.054 | 10 | 18 | fits | 52,723 | 29 | 0.049 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 138,784 | 2.776 | 10 | 24 | fits | 190,142 | 107 | 0.030 |
| LINK_DOWN | `fixture.link_down.if0` | 2,512 | 0.050 | 10 | 200 | fits | 144,539 | 27 (9) | 0.039 |
| BIND_RX | `fixture.bind_rx.if0` | 46,538 | 0.931 | 10 | 20 | fits | 107,831 | 82 (77) | 0.054 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 55,560 | 1.111 | 10 | 20 | fits | 676,469 | 127 (35) | 0.017 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 136,415 | 2.728 | 10 | 20 | fits | 660,166 | 98 (29) | 0.016 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 276,618 | 5.532 | 10 | 200 | fits | 276,669 | 245 | 0.039 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 276,618 | 5.532 | 10 | 200 | fits | 276,669 | 245 | 0.039 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 276,483 | 5.530 | 10 | 20 | fits | 276,669 | 245 | 0.039 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 276,483 | 5.530 | 10 | 20 | fits | 276,669 | 245 | 0.039 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 276,585 | 5.532 | 10 | 24 | fits | 276,669 | 245 | 0.039 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 276,585 | 5.532 | 10 | 24 | fits | 276,669 | 245 | 0.039 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 276,553 | 5.531 | 10 | 50 | fits | 276,669 | 245 | 0.039 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 276,553 | 5.531 | 10 | 50 | fits | 276,669 | 245 | 0.039 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 276,520 | 5.530 | 10 | 18 | fits | 276,669 | 245 | 0.039 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 276,520 | 5.530 | 10 | 18 | fits | 276,669 | 245 | 0.039 |

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
