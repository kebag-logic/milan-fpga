head 3ba76ae7c75f655fb77cad80866f6799d0e73087
command: run.py --point 1x1 --record-budget-findings: results/table.md
full log: 30333 bytes, sha256 5cdaa781a1c3e5ab4db7d2f73273a0070f8822a5778cc634ddbd64dab60b3b3e
---
### 1x1

15 of 81 paths and 36 of 141 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 1.287 (2.794) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 9.421 (15.977) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 10.434 (15.764) | MISS T_svc | 0 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 15.329 (30.842) | MISS T_svc | 0 adp | 2 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 9.655 (14.325) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 9.421 (15.976) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 11.185 (16.009) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 8.124 (12.655) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 12.504 (31.295) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 4.950 (27.288) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 2.382 (27.278) | fits | 1 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 1.343 (14.309) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.973 (13.570) | fits | 1 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 1.553 (13.788) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 1.111 (13.514) | fits | 1 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 9.599 (14.625) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.224 (1.144) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.077 (1.022) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.065 (3.101) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.077 (3.241) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.763 (1.695) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.944 (2.831) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.141 (2.923) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 2.162 (2.944) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.104 (2.886) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 2.392 (3.174) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 2.261 (3.043) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 2.266 (3.231) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 1.736 (2.518) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 2.802 (3.584) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 2.344 (3.125) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 2.622 (3.403) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.284 (3.066) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.106 (3.888) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 2.175 (2.956) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 2.483 (3.265) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 2.745 (3.527) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 2.362 (3.144) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 2.409 (3.191) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.651 (3.432) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 2.434 (3.216) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 2.437 (3.218) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 2.343 (3.124) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.716 (2.490) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 2.756 (4.144) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.099 (2.881) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 2.578 (3.543) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 5.038 (5.851) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 4.605 (5.390) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 4.745 (5.560) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 4.539 (5.159) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 4.767 (5.552) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 6.355 (7.486) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 4.381 (4.981) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 4.925 (5.710) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 36.976 (40.820) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 42.071 (51.437) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 38.635 (55.075) | MISS ceiling | 4 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 9.348 (17.383) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 95.091 (97.541) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 363.387 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 2.989 (4.159) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 1.588 (3.499) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.458 (1.359) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.531 (3.241) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 1.438 (3.499) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 1.055 (2.615) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp.service.acmp.first.if0` (backlog-adp) | 9.076 | fits | 0 acmp | 5 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 85.811 | MISS ceiling | 11 acmp | 5 | 4 |
| ADP record released under the composed load, first | 0 | `backlog-adp.service.adp.first.if0` (backlog-adp) | 9.067 | fits | 0 adp | 5 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 49.705 | MISS T_svc | 7 adp | 5 | 4 |
| AECP record released under the composed load, first | 0 | `backlog-adp.service.aecp.first.if0` (backlog-adp) | 9.112 | fits | 0 aecp | 5 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp-refill.service.aecp.last.if0` (backlog-adp-refill) | 254.115 | MISS ceiling | 15 aecp | 5 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog-adp.service.maap.first.if0` (backlog-adp) | 9.102 | fits | 0 maap | 5 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 49.742 | MISS T_svc | 6 maap | 5 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 578.620 | STARVED: never released | 0 srp | 5 | 4 |
| SRP record released under the composed load, last | 0 | `backlog-adp-refill.service.srp.last.if0` (backlog-adp-refill) | at least 578.600 | STARVED: never released | 31 srp | 5 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 3.252 (4.654) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 1.904 (1.905) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 1.582 (1.583) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 2.867 (3.241) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 90.388 | 22 | 440,879 (8.818) | yes | - |
| backlog-adp | 542.124 | 36 | 948,788 (18.976) | no | {'srp': 32} |
| backlog-adp-refill | 578.637 | 38 | 927,668 (18.553) | no | {'srp': 32} |
| backlog-owed | 363.438 | 54 | 387,762 (7.755) | yes | - |
| fixture | 10.110 | 3 | 294,749 (5.895) | yes | - |

Composed maximum over the 4 backlog windows: at least 948,788 CPU cycles (18.976 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 440,879 (8.818 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 77,639 | 1.553 | 10 | 20 | fits | 689,380 | 119 (14) | 0.036 |
| LINK_UP | `adp.link_up.if0` | 3,868 | 0.077 | 10 | 200 | fits | 162,048 | 88 (11) | 0.091 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 47,222 | 0.944 | 10 | 200 | fits | 66,718 | 46 (39) | 0.087 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 38,146 | 0.763 | 10 | 200 | fits | 3,893 | 9 (11) | 0.164 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 46,439 | 0.929 | 10 | 20 | fits | 691,807 | 140 (35) | 0.035 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 48,667 | 0.973 | 10 | 20 | fits | 678,506 | 117 (14) | 0.034 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 55,575 | 1.111 | 10 | 20 | fits | 675,699 | 118 (14) | 0.034 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 247,504 | 4.950 | 10 | 20 | fits | 692,298 | 140 (35) | 0.035 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 143,330 | 2.867 | 10 | 18 | fits | 162,048 | 88 | 0.091 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 95,198 | 1.904 | 10 | 18 | fits | 95,230 | 29 | 0.112 |
| malformed MRPDU discard | `srp.malformed.if0` | 79,115 | 1.582 | 10 | 18 | fits | 79,147 | 35 | 0.113 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 162,581 | 3.252 | 210 | 218 | fits | 232,703 | 78 | 0.090 |
| an event behind 15 others | `backlog.event.if0` | 467,412 | 9.348 | 10 | 200 | fits | 428,274 | 356 | 0.073 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 1,848,816 | 36.976 | 10 | 20 | MISS ceiling | 258,315 | 211 | 0.056 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 440,775 | 8.816 | 10 | 200 | fits | 440,879 | 389 | 0.071 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 1,495,087 | 29.902 | 10 | 200 | MISS T_svc | 286,166 | 279 | 0.064 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 438,646 | 8.773 | 10 | 20 | fits | 440,879 | 389 | 0.071 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 2,038,371 | 40.767 | 10 | 20 | MISS ceiling | 258,315 | 211 | 0.056 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 440,438 | 8.809 | 10 | 24 | fits | 440,879 | 389 | 0.071 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 4,014,495 | 80.290 | 10 | 24 | MISS ceiling | 207,989 | 169 | 0.059 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 439,918 | 8.798 | 10 | 50 | fits | 440,879 | 389 | 0.071 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 1,494,339 | 29.887 | 10 | 50 | MISS T_svc | 286,166 | 279 | 0.064 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 1,208,141 | 24.163 | 10 | 18 | MISS ceiling | 340,176 | 348 | 0.073 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 4,381,306 | 87.626 | 10 | 18 | MISS ceiling | 74,176 | 53 | 0.112 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 2,103,534 | 42.071 | 10 | 20 | MISS ceiling | 948,788 | 411 | 0.042 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 453,355 | 9.067 | 10 | 200 | fits | 539,662 | 402 | 0.056 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,485,254 | 49.705 | 10 | 200 | MISS T_svc | 948,788 | 411 | 0.042 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 453,811 | 9.076 | 10 | 20 | fits | 539,662 | 402 | 0.056 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 4,264,490 | 85.290 | 10 | 20 | MISS ceiling | 889,502 | 317 | 0.038 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 455,603 | 9.112 | 10 | 24 | fits | 539,662 | 402 | 0.056 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 12,679,773 | 253.595 | 10 | 24 | MISS ceiling | 805,410 | 230 | 0.033 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 455,083 | 9.102 | 10 | 50 | fits | 539,662 | 402 | 0.056 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,487,092 | 49.742 | 10 | 50 | MISS T_svc | 948,788 | 411 | 0.042 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 27,105,339 | 542.107 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 27,104,332 | 542.087 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 1,931,726 | 38.635 | 10 | 20 | MISS ceiling | 919,254 | 349 | 0.040 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 453,355 | 9.067 | 10 | 200 | fits | 539,662 | 402 | 0.056 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 2,292,743 | 45.855 | 10 | 200 | MISS T_svc | 919,254 | 349 | 0.040 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 453,811 | 9.076 | 10 | 20 | fits | 539,662 | 402 | 0.056 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 4,290,549 | 85.811 | 10 | 20 | MISS ceiling | 919,254 | 349 | 0.040 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 455,603 | 9.112 | 10 | 24 | fits | 539,662 | 402 | 0.056 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 12,705,766 | 254.115 | 10 | 24 | MISS ceiling | 805,575 | 230 | 0.033 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 455,083 | 9.102 | 10 | 50 | fits | 539,662 | 402 | 0.056 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,465,972 | 49.319 | 10 | 50 | MISS T_svc | 927,668 | 404 | 0.041 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 28,930,989 | 578.620 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 28,929,982 | 578.600 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 4,754,529 | 95.091 | 10 | 20 | MISS ceiling | 216,643 | 153 | 0.055 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,169,352 | 363.387 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,169,314 | 363.386 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,169,277 | 363.386 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,169,239 | 363.385 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 366,270 | 7.325 | 10 | 200 | fits | 337,757 | 341 | 0.071 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 1,412,479 | 28.250 | 10 | 200 | MISS T_svc | 387,762 | 300 | 0.080 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 364,141 | 7.283 | 10 | 20 | fits | 337,757 | 341 | 0.071 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 1,894,673 | 37.893 | 10 | 20 | MISS ceiling | 264,168 | 120 | 0.085 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 365,933 | 7.319 | 10 | 24 | fits | 337,757 | 341 | 0.071 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 5,404,521 | 108.090 | 10 | 24 | MISS ceiling | 181,880 | 125 | 0.047 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 365,413 | 7.308 | 10 | 50 | fits | 337,757 | 341 | 0.071 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 1,411,731 | 28.235 | 10 | 50 | MISS T_svc | 387,762 | 300 | 0.080 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 1,411,699 | 28.234 | 10 | 18 | MISS ceiling | 387,762 | 300 | 0.080 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 4,008,355 | 80.167 | 10 | 18 | MISS ceiling | 268,233 | 185 | 0.071 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 406,642 | 8.133 | 10 | 20 | fits | 786,479 | 150 (29) | 0.033 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 521,679 | 10.434 | 10 | 20 | MISS T_svc | 788,214 | 156 (35) | 0.033 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 119,116 | 2.382 | 10 | 20 | fits | 605,690 | 130 (12) | 0.039 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 26,555 | 0.531 | 10 | 50 | fits | 162,048 | 88 | 0.091 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 24,162 | 0.483 | 10 | 50 | fits | 69,040 | 37 | 0.097 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 52,727 | 1.055 | 10 | 50 | fits | 68,849 | 37 | 0.098 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 71,920 | 1.438 | 10 | 50 | fits | 86,099 | 64 | 0.085 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 79,391 | 1.588 | 10 | 50 | fits | 86,099 | 64 | 0.085 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 22,892 | 0.458 | 10 | 50 | fits | 67,928 | 47 | 0.096 |
| LINK_UP | `adp.link_up.if0` | 3,868 | 0.077 | 10 | 200 | fits | 162,048 | 88 (11) | 0.091 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 47,222 | 0.944 | 10 | 200 | fits | 66,718 | 46 (39) | 0.087 |
| LINK_DOWN | `adp.link_down.if0` | 3,244 | 0.065 | 10 | 200 | fits | 155,059 | 27 (9) | 0.086 |
| LINK_UP | `adp.link_up.if0` | 3,868 | 0.077 | 10 | 200 | fits | 162,048 | 88 (11) | 0.091 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 47,222 | 0.944 | 10 | 200 | fits | 66,718 | 46 (39) | 0.087 |
| GM_CHANGE | `adp.gm_change.if0` | 3,836 | 0.077 | 10 | 200 | fits | 51,101 | 18 (11) | 0.097 |
| LINK_UP | `adp.link_up.if0` | 3,868 | 0.077 | 10 | 200 | fits | 162,048 | 88 (11) | 0.091 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 47,222 | 0.944 | 10 | 200 | fits | 66,718 | 46 (39) | 0.087 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 11,214 | 0.224 | 10 | 200 | fits | 57,193 | 38 (31) | 0.104 |
| LINK_UP | `adp.link_up.if0` | 3,868 | 0.077 | 10 | 200 | fits | 162,048 | 88 (11) | 0.091 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 47,222 | 0.944 | 10 | 200 | fits | 66,718 | 46 (39) | 0.087 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 11,214 | 0.224 | 10 | 200 | fits | 57,193 | 38 (31) | 0.104 |
| set_name | `aecp_fanout.set_name.if0` | 317,762 | 6.355 | 10 | 24 | fits | 374,322 | 623 | 0.035 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 226,955 | 4.539 | 10 | 24 | fits | 257,956 | 328 | 0.043 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 238,342 | 4.767 | 10 | 24 | fits | 277,576 | 348 | 0.042 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 218,603 | 4.372 | 10 | 24 | fits | 257,880 | 311 | 0.039 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 237,243 | 4.745 | 10 | 24 | fits | 278,001 | 351 | 0.041 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 251,893 | 5.038 | 10 | 24 | fits | 292,527 | 358 | 0.043 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 219,051 | 4.381 | 10 | 24 | fits | 249,037 | 317 | 0.042 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 230,242 | 4.605 | 10 | 24 | fits | 269,498 | 362 | 0.037 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 246,248 | 4.925 | 10 | 24 | fits | 285,525 | 369 | 0.043 |
| BIND_RX | `acmp.bind_rx.if0` | 64,373 | 1.287 | 10 | 20 | fits | 139,720 | 89 (77) | 0.093 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 625,211 | 12.504 | 10 | 20 | MISS T_svc | 708,241 | 143 (32) | 0.038 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 482,763 | 9.655 | 10 | 20 | fits | 716,266 | 158 (47) | 0.037 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 479,966 | 9.599 | 10 | 20 | fits | 731,246 | 161 (50) | 0.039 |
| PROBE_TX | `acmp.probe_tx.if0` | 406,207 | 8.124 | 10 | 20 | fits | 632,739 | 181 (48) | 0.041 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 559,236 | 11.185 | 10 | 20 | MISS T_svc | 800,429 | 169 (48) | 0.034 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 471,043 | 9.421 | 10 | 20 | fits | 798,843 | 169 (48) | 0.034 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 471,027 | 9.421 | 10 | 20 | fits | 798,793 | 169 (48) | 0.034 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 85,812 | 1.716 | 10 | 24 | fits | 124,502 | 54 | 0.081 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 140,093 | 2.802 | 10 | 24 | fits | 179,185 | 126 | 0.048 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 117,178 | 2.344 | 10 | 24 | fits | 156,267 | 74 | 0.054 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 137,248 | 2.745 | 10 | 24 | fits | 176,337 | 91 | 0.059 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 121,699 | 2.434 | 10 | 24 | fits | 160,791 | 84 | 0.052 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 121,827 | 2.437 | 10 | 24 | fits | 160,919 | 84 | 0.052 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 117,130 | 2.343 | 10 | 24 | fits | 156,222 | 73 | 0.054 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 131,077 | 2.622 | 10 | 24 | fits | 170,169 | 75 | 0.061 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 114,216 | 2.284 | 10 | 24 | fits | 153,305 | 66 | 0.055 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 155,320 | 3.106 | 10 | 24 | fits | 194,409 | 161 | 0.044 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 108,728 | 2.175 | 10 | 24 | fits | 147,817 | 53 | 0.057 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 124,141 | 2.483 | 10 | 24 | fits | 163,230 | 59 | 0.064 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 118,098 | 2.362 | 10 | 24 | fits | 157,187 | 70 | 0.053 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 120,465 | 2.409 | 10 | 24 | fits | 159,554 | 76 | 0.053 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 132,535 | 2.651 | 10 | 24 | fits | 171,624 | 74 | 0.061 |
| get_configuration | `aecp.get_configuration.if0` | 105,189 | 2.104 | 10 | 24 | fits | 144,278 | 48 | 0.057 |
| entity_available | `aecp.entity_available.if0` | 107,039 | 2.141 | 10 | 24 | fits | 146,131 | 52 | 0.057 |
| get_name | `aecp.get_name.if0` | 113,057 | 2.261 | 10 | 24 | fits | 152,149 | 65 | 0.056 |
| get_counters | `aecp.get_counters.if0` | 119,584 | 2.392 | 10 | 24 | fits | 158,676 | 85 | 0.056 |
| get_avb_info | `aecp.get_avb_info.if0` | 108,115 | 2.162 | 10 | 24 | fits | 147,207 | 48 | 0.057 |
| unknown_command | `aecp.unknown_command.if0` | 104,974 | 2.099 | 10 | 24 | fits | 144,066 | 48 | 0.057 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 86,787 | 1.736 | 10 | 24 | fits | 125,879 | 58 | 0.081 |
| set_name | `aecp.set_name.if0` | 137,805 | 2.756 | 10 | 24 | fits | 207,196 | 128 | 0.056 |
| lock_entity | `aecp.lock_entity.if0` | 113,287 | 2.266 | 10 | 24 | fits | 161,525 | 78 | 0.058 |
| unlock_entity | `aecp.unlock_entity.if0` | 128,921 | 2.578 | 10 | 24 | fits | 177,137 | 84 | 0.065 |
| LINK_UP | `fixture.link_up.if0` | 3,868 | 0.077 | 10 | 200 | fits | 162,048 | 88 (11) | 0.091 |
| malformed MRPDU discard | `fixture.malformed.if0` | 59,036 | 1.181 | 10 | 18 | fits | 59,068 | 29 | 0.110 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 149,468 | 2.989 | 10 | 24 | fits | 207,963 | 128 | 0.056 |
| LINK_DOWN | `fixture.link_down.if0` | 3,244 | 0.065 | 10 | 200 | fits | 157,197 | 27 (9) | 0.085 |
| BIND_RX | `fixture.bind_rx.if0` | 49,131 | 0.983 | 10 | 20 | fits | 114,667 | 83 (77) | 0.084 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 67,164 | 1.343 | 10 | 20 | fits | 715,445 | 169 (35) | 0.037 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 766,467 | 15.329 | 10 | 20 | MISS T_svc | 785,231 | 150 (29) | 0.033 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 294,698 | 5.894 | 10 | 200 | fits | 294,749 | 245 | 0.076 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 294,698 | 5.894 | 10 | 200 | fits | 294,749 | 245 | 0.076 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 294,563 | 5.891 | 10 | 20 | fits | 294,749 | 245 | 0.076 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 294,563 | 5.891 | 10 | 20 | fits | 294,749 | 245 | 0.076 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 294,665 | 5.893 | 10 | 24 | fits | 294,749 | 245 | 0.076 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 294,665 | 5.893 | 10 | 24 | fits | 294,749 | 245 | 0.076 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 294,633 | 5.893 | 10 | 50 | fits | 294,749 | 245 | 0.076 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 294,633 | 5.893 | 10 | 50 | fits | 294,749 | 245 | 0.076 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 294,600 | 5.892 | 10 | 18 | fits | 294,749 | 245 | 0.076 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 294,600 | 5.892 | 10 | 18 | fits | 294,749 | 245 | 0.076 |

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
