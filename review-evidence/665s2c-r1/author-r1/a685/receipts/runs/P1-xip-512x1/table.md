### 1x1

19 of 81 paths and 62 of 141 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 4.758 (10.727) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 1.846 (22.108) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 9.309 (22.062) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 10.943 (20.883) | MISS T_svc | 0 adp | 2 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 4.280 (23.237) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 2.715 (22.587) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 2.833 (22.741) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 4.393 (21.824) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 11.085 (25.186) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 5.157 (38.844) | fits | 2 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 3.744 (19.403) | fits | 1 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 4.762 (19.556) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 5.059 (36.429) | fits | 2 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 2.490 (20.673) | fits | 1 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 6.096 (37.663) | fits | 2 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 3.943 (25.943) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 1.420 (3.485) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.746 (2.907) | fits | 1 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.932 (11.814) | fits | 1 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.570 (10.930) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.819 (2.751) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 3.180 (8.227) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 3.809 (6.164) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 4.134 (6.619) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 3.910 (6.264) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 4.301 (6.745) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 4.957 (7.408) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 4.103 (6.590) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 2.882 (4.929) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 4.857 (7.257) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 3.965 (6.323) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 4.606 (9.102) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 3.907 (6.265) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 4.712 (7.070) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 3.800 (6.158) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 3.801 (6.159) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 4.057 (6.414) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 3.984 (6.342) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 4.031 (6.388) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 3.966 (6.324) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 4.054 (6.412) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 4.056 (6.414) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 3.964 (6.322) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 4.182 (6.352) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 5.039 (8.433) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 3.688 (5.913) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 4.713 (7.290) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 7.507 (10.584) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 6.412 (8.735) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 9.204 (12.417) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 7.448 (10.076) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 6.889 (11.238) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 9.793 (12.912) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 7.821 (10.565) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 6.982 (9.396) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 87.130 (94.686) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 69.551 (100.653) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 83.612 (103.598) | MISS ceiling | 6 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 24.438 (43.242) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 141.799 (148.818) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 369.607 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 14.093 (24.112) | MISS T_svc | 0 aecp | 1 | 1 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 1.539 (4.986) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 2.087 (4.084) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 2.497 (10.930) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 1.309 (4.986) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 2.407 (7.324) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 23.380 | MISS ceiling | 0 acmp | 5 | 5 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 137.063 | MISS ceiling | 11 acmp | 5 | 5 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 23.423 | MISS T_svc | 0 adp | 5 | 5 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 97.107 | MISS T_svc | 6 adp | 5 | 5 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 23.416 | MISS T_svc | 0 aecp | 5 | 5 |
| AECP record released under the composed load, last | 0 | `backlog-adp-refill.service.aecp.last.if0` (backlog-adp-refill) | 360.229 | MISS ceiling | 15 aecp | 5 | 5 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 23.405 | MISS T_svc | 0 maap | 5 | 5 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 84.145 | MISS ceiling | 6 maap | 5 | 5 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 623.597 | STARVED: never released | 0 srp | 5 | 5 |
| SRP record released under the composed load, last | 0 | `backlog-adp-refill.service.srp.last.if0` (backlog-adp-refill) | at least 623.577 | STARVED: never released | 31 srp | 5 | 5 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 9.046 (11.074) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 8.454 (8.455) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 3.688 (3.688) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 9.508 (10.930) | fits | 0 events | 1 | 0 |

Composed windows: the longest pass is the composed maximum only where the window released its whole load.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 198.595 | 24 | 1,171,236 (23.425) | yes | - |
| backlog-adp | 569.604 | 28 | 1,403,934 (28.079) | no | {'srp': 32} |
| backlog-adp-refill | 623.614 | 31 | 1,375,315 (27.506) | no | {'srp': 32} |
| backlog-owed | 369.657 | 42 | 824,500 (16.490) | yes | - |
| fixture | 20.000 | 2 | 668,420 (13.368) | yes | - |

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 124,520 | 2.490 | 10 | 20 | fits | 1,033,639 | 74 (14) | 0.009 |
| LINK_UP | `adp.link_up.if0` | 28,486 | 0.570 | 10 | 200 | fits | 546,479 | 94 (11) | 0.029 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 158,994 | 3.180 | 10 | 200 | fits | 229,517 | 52 (39) | 0.023 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 40,927 | 0.819 | 10 | 200 | fits | 38,095 | 15 (11) | 0.019 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 238,084 | 4.762 | 10 | 20 | fits | 977,781 | 95 (35) | 0.008 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 252,959 | 5.059 | 10 | 20 | fits | 918,558 | 72 (14) | 0.007 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 304,785 | 6.096 | 10 | 20 | fits | 974,600 | 76 (14) | 0.006 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 257,871 | 5.157 | 10 | 20 | fits | 967,625 | 95 (35) | 0.008 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 475,397 | 9.508 | 10 | 18 | fits | 546,479 | 94 | 0.029 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 422,716 | 8.454 | 10 | 18 | fits | 422,748 | 35 | 0.034 |
| malformed MRPDU discard | `srp.malformed.if0` | 170,082 | 3.402 | 10 | 18 | fits | 170,114 | 28 | 0.021 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 452,287 | 9.046 | 210 | 218 | fits | 553,691 | 77 | 0.017 |
| an event behind 15 others | `backlog.event.if0` | 1,221,890 | 24.438 | 10 | 200 | MISS T_svc | 990,865 | 355 | 0.015 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 4,356,513 | 87.130 | 10 | 20 | MISS ceiling | 603,442 | 216 | 0.015 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 1,171,132 | 23.423 | 10 | 200 | MISS T_svc | 1,171,236 | 388 | 0.019 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 3,490,753 | 69.815 | 10 | 200 | MISS T_svc | 625,780 | 284 | 0.013 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 1,169,003 | 23.380 | 10 | 20 | MISS ceiling | 1,171,236 | 388 | 0.019 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 4,731,671 | 94.633 | 10 | 20 | MISS ceiling | 603,442 | 216 | 0.015 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 1,170,795 | 23.416 | 10 | 24 | MISS T_svc | 1,171,236 | 388 | 0.019 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 8,568,905 | 171.378 | 10 | 24 | MISS ceiling | 394,463 | 168 | 0.012 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 1,170,275 | 23.405 | 10 | 50 | MISS T_svc | 1,171,236 | 388 | 0.019 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 3,490,005 | 69.800 | 10 | 50 | MISS ceiling | 625,780 | 284 | 0.013 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 4,129,687 | 82.594 | 10 | 18 | MISS ceiling | 639,714 | 261 | 0.014 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 9,446,403 | 188.928 | 10 | 18 | MISS ceiling | 110,590 | 47 | 0.013 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 3,477,547 | 69.551 | 10 | 20 | MISS ceiling | 1,403,934 | 365 | 0.008 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 929,986 | 18.600 | 10 | 200 | MISS T_svc | 848,076 | 384 | 0.012 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 4,205,405 | 84.108 | 10 | 200 | MISS T_svc | 1,403,934 | 365 | 0.008 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 930,442 | 18.609 | 10 | 20 | MISS T_svc | 848,076 | 384 | 0.012 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 6,848,167 | 136.963 | 10 | 20 | MISS ceiling | 1,361,485 | 274 | 0.007 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 932,234 | 18.645 | 10 | 24 | MISS T_svc | 848,076 | 384 | 0.012 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 18,006,832 | 360.137 | 10 | 24 | MISS ceiling | 1,109,697 | 187 | 0.005 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 931,714 | 18.634 | 10 | 50 | MISS T_svc | 848,076 | 384 | 0.012 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 4,207,243 | 84.145 | 10 | 50 | MISS ceiling | 1,403,934 | 365 | 0.008 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 28,479,352 | 569.587 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 28,478,345 | 569.567 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 4,180,596 | 83.612 | 10 | 20 | MISS ceiling | 1,341,110 | 303 | 0.008 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 929,986 | 18.600 | 10 | 200 | MISS T_svc | 848,076 | 384 | 0.012 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 4,855,337 | 97.107 | 10 | 200 | MISS T_svc | 1,341,110 | 303 | 0.008 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 930,442 | 18.609 | 10 | 20 | MISS T_svc | 848,076 | 384 | 0.012 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 6,853,143 | 137.063 | 10 | 20 | MISS ceiling | 1,341,110 | 303 | 0.008 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 932,234 | 18.645 | 10 | 24 | MISS T_svc | 848,076 | 384 | 0.012 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 18,011,452 | 360.229 | 10 | 24 | MISS ceiling | 1,109,477 | 187 | 0.005 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 931,714 | 18.634 | 10 | 50 | MISS T_svc | 848,076 | 384 | 0.012 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 4,138,208 | 82.764 | 10 | 50 | MISS ceiling | 1,334,899 | 358 | 0.008 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 31,179,859 | 623.597 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 31,178,852 | 623.577 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 7,089,927 | 141.799 | 10 | 20 | MISS ceiling | 503,082 | 151 | 0.016 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,480,326 | 369.607 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,480,288 | 369.606 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 7,592,936 | 151.859 | 10 | 20 | MISS ceiling | 503,122 | 151 | 0.016 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,480,213 | 369.604 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 790,607 | 15.812 | 10 | 200 | MISS T_svc | 770,388 | 340 | 0.015 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 2,794,718 | 55.894 | 10 | 200 | MISS T_svc | 685,652 | 266 | 0.014 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 788,478 | 15.770 | 10 | 20 | MISS T_svc | 770,388 | 340 | 0.015 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 3,984,822 | 79.696 | 10 | 20 | MISS ceiling | 617,404 | 194 | 0.015 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 790,270 | 15.805 | 10 | 24 | MISS T_svc | 770,388 | 340 | 0.015 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 9,227,921 | 184.558 | 10 | 24 | MISS ceiling | 414,709 | 129 | 0.014 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 789,750 | 15.795 | 10 | 50 | MISS T_svc | 770,388 | 340 | 0.015 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 2,793,970 | 55.879 | 10 | 50 | MISS ceiling | 685,652 | 266 | 0.014 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 4,810,780 | 96.216 | 10 | 18 | MISS ceiling | 824,500 | 177 | 0.024 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 14,161,345 | 283.227 | 10 | 18 | MISS ceiling | 213,508 | 28 | 0.019 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 547,141 | 10.943 | 10 | 20 | MISS T_svc | 1,044,166 | 98 (29) | 0.007 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 465,444 | 9.309 | 10 | 20 | fits | 1,103,088 | 107 (35) | 0.005 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 187,194 | 3.744 | 10 | 20 | fits | 970,139 | 95 (12) | 0.008 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 124,865 | 2.497 | 10 | 50 | fits | 546,479 | 94 | 0.029 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 100,855 | 2.017 | 10 | 50 | fits | 187,353 | 37 | 0.022 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 120,336 | 2.407 | 10 | 50 | fits | 230,851 | 43 | 0.024 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 65,471 | 1.309 | 10 | 50 | fits | 249,315 | 70 | 0.021 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 76,939 | 1.539 | 10 | 50 | fits | 249,315 | 70 | 0.021 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 104,337 | 2.087 | 10 | 50 | fits | 204,223 | 46 | 0.024 |
| LINK_UP | `adp.link_up.if0` | 28,486 | 0.570 | 10 | 200 | fits | 546,479 | 94 (11) | 0.029 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 158,994 | 3.180 | 10 | 200 | fits | 229,517 | 52 (39) | 0.023 |
| LINK_DOWN | `adp.link_down.if0` | 38,670 | 0.773 | 10 | 200 | fits | 564,846 | 33 (9) | 0.027 |
| LINK_UP | `adp.link_up.if0` | 28,486 | 0.570 | 10 | 200 | fits | 546,479 | 94 (11) | 0.029 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 158,994 | 3.180 | 10 | 200 | fits | 229,517 | 52 (39) | 0.023 |
| GM_CHANGE | `adp.gm_change.if0` | 37,291 | 0.746 | 10 | 200 | fits | 145,338 | 24 (11) | 0.017 |
| LINK_UP | `adp.link_up.if0` | 28,486 | 0.570 | 10 | 200 | fits | 546,479 | 94 (11) | 0.029 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 158,994 | 3.180 | 10 | 200 | fits | 229,517 | 52 (39) | 0.023 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 71,010 | 1.420 | 10 | 200 | fits | 174,235 | 44 (31) | 0.020 |
| LINK_UP | `adp.link_up.if0` | 28,486 | 0.570 | 10 | 200 | fits | 546,479 | 94 (11) | 0.029 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 158,994 | 3.180 | 10 | 200 | fits | 229,517 | 52 (39) | 0.023 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 71,010 | 1.420 | 10 | 200 | fits | 174,235 | 44 (31) | 0.020 |
| set_name | `aecp_fanout.set_name.if0` | 489,635 | 9.793 | 10 | 24 | fits | 645,581 | 608 | 0.009 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 372,422 | 7.448 | 10 | 24 | fits | 503,822 | 316 | 0.011 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 344,475 | 6.889 | 10 | 24 | fits | 445,689 | 299 | 0.009 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 308,407 | 6.168 | 10 | 24 | fits | 428,814 | 299 | 0.008 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 460,219 | 9.204 | 10 | 24 | fits | 620,871 | 357 | 0.013 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 375,362 | 7.507 | 10 | 24 | fits | 529,175 | 350 | 0.010 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 391,037 | 7.821 | 10 | 24 | fits | 528,233 | 323 | 0.012 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 320,590 | 6.412 | 10 | 24 | fits | 436,736 | 350 | 0.008 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 349,102 | 6.982 | 10 | 24 | fits | 469,792 | 357 | 0.009 |
| BIND_RX | `acmp.bind_rx.if0` | 237,906 | 4.758 | 10 | 20 | fits | 536,372 | 82 (77) | 0.037 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 554,266 | 11.085 | 10 | 20 | MISS T_svc | 1,259,302 | 104 (32) | 0.007 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 213,977 | 4.280 | 10 | 20 | fits | 1,161,865 | 116 (47) | 0.008 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 197,167 | 3.943 | 10 | 20 | fits | 1,297,141 | 119 (50) | 0.010 |
| PROBE_TX | `acmp.probe_tx.if0` | 219,634 | 4.393 | 10 | 20 | fits | 1,091,215 | 115 (48) | 0.010 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 141,633 | 2.833 | 10 | 20 | fits | 1,137,038 | 117 (48) | 0.008 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 92,297 | 1.846 | 10 | 20 | fits | 1,105,413 | 145 (48) | 0.010 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 135,774 | 2.715 | 10 | 20 | fits | 1,129,350 | 117 (48) | 0.008 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 209,076 | 4.182 | 10 | 24 | fits | 317,581 | 46 | 0.023 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 242,855 | 4.857 | 10 | 24 | fits | 362,851 | 124 | 0.012 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 198,237 | 3.965 | 10 | 24 | fits | 316,133 | 72 | 0.012 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 202,828 | 4.057 | 10 | 24 | fits | 320,724 | 83 | 0.012 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 202,688 | 4.054 | 10 | 24 | fits | 320,587 | 82 | 0.012 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 202,816 | 4.056 | 10 | 24 | fits | 320,715 | 82 | 0.012 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 198,218 | 3.964 | 10 | 24 | fits | 316,117 | 71 | 0.012 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 230,291 | 4.606 | 10 | 24 | fits | 314,893 | 68 | 0.013 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 195,367 | 3.907 | 10 | 24 | fits | 313,263 | 64 | 0.013 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 235,616 | 4.712 | 10 | 24 | fits | 353,512 | 159 | 0.010 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 189,996 | 3.800 | 10 | 24 | fits | 307,892 | 51 | 0.013 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 190,060 | 3.801 | 10 | 24 | fits | 307,956 | 51 | 0.013 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 199,213 | 3.984 | 10 | 24 | fits | 317,109 | 68 | 0.012 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 201,526 | 4.031 | 10 | 24 | fits | 319,422 | 74 | 0.012 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 198,282 | 3.966 | 10 | 24 | fits | 316,178 | 66 | 0.012 |
| get_configuration | `aecp.get_configuration.if0` | 195,477 | 3.910 | 10 | 24 | fits | 313,220 | 46 | 0.014 |
| entity_available | `aecp.entity_available.if0` | 190,464 | 3.809 | 10 | 24 | fits | 308,210 | 50 | 0.013 |
| get_name | `aecp.get_name.if0` | 247,871 | 4.957 | 10 | 24 | fits | 370,403 | 70 | 0.015 |
| get_counters | `aecp.get_counters.if0` | 215,038 | 4.301 | 10 | 24 | fits | 337,274 | 79 | 0.014 |
| get_avb_info | `aecp.get_avb_info.if0` | 206,684 | 4.134 | 10 | 24 | fits | 330,954 | 46 | 0.015 |
| unknown_command | `aecp.unknown_command.if0` | 184,408 | 3.688 | 10 | 24 | fits | 295,646 | 46 | 0.013 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 144,119 | 2.882 | 10 | 24 | fits | 246,473 | 50 | 0.015 |
| set_name | `aecp.set_name.if0` | 251,944 | 5.039 | 10 | 24 | fits | 421,654 | 106 | 0.013 |
| lock_entity | `aecp.lock_entity.if0` | 205,136 | 4.103 | 10 | 24 | fits | 329,487 | 65 | 0.014 |
| unlock_entity | `aecp.unlock_entity.if0` | 235,648 | 4.713 | 10 | 24 | fits | 364,500 | 72 | 0.014 |
| LINK_UP | `fixture.link_up.if0` | 28,486 | 0.570 | 10 | 200 | fits | 546,479 | 94 (11) | 0.029 |
| malformed MRPDU discard | `fixture.malformed.if0` | 184,386 | 3.688 | 10 | 18 | fits | 184,418 | 28 | 0.026 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 704,663 | 14.093 | 10 | 24 | MISS T_svc | 537,188 | 112 | 0.018 |
| LINK_DOWN | `fixture.link_down.if0` | 46,579 | 0.932 | 10 | 200 | fits | 590,688 | 33 (9) | 0.028 |
| BIND_RX | `fixture.bind_rx.if0` | 218,497 | 4.370 | 10 | 20 | fits | 453,183 | 82 (77) | 0.032 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 208,109 | 4.162 | 10 | 20 | fits | 1,070,685 | 124 (35) | 0.009 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 314,525 | 6.290 | 10 | 20 | fits | 1,078,477 | 101 (29) | 0.005 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 661,196 | 13.224 | 10 | 200 | MISS T_svc | 661,247 | 224 | 0.020 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 661,196 | 13.224 | 10 | 200 | MISS T_svc | 661,247 | 224 | 0.020 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 661,061 | 13.221 | 10 | 20 | MISS T_svc | 661,247 | 224 | 0.020 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 661,061 | 13.221 | 10 | 20 | MISS T_svc | 661,247 | 224 | 0.020 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 661,163 | 13.223 | 10 | 24 | MISS T_svc | 661,247 | 224 | 0.020 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 661,163 | 13.223 | 10 | 24 | MISS T_svc | 661,247 | 224 | 0.020 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 661,131 | 13.223 | 10 | 50 | MISS T_svc | 661,247 | 224 | 0.020 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 661,131 | 13.223 | 10 | 50 | MISS T_svc | 661,247 | 224 | 0.020 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 1,329,518 | 26.590 | 10 | 18 | MISS ceiling | 668,420 | 86 | 0.027 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 1,329,518 | 26.590 | 10 | 18 | MISS ceiling | 668,420 | 86 | 0.027 |

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
- `aecp`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
