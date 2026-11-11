### 1x1

13 of 81 paths and 34 of 141 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 1.283 (2.591) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 9.342 (14.207) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 8.126 (13.997) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 13.060 (29.032) | MISS T_svc | 0 adp | 2 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 9.573 (16.007) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 9.338 (14.204) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 9.365 (14.230) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 8.046 (14.338) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 12.434 (15.853) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.934 (13.815) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 2.117 (27.199) | fits | 2 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 2.789 (14.259) | fits | 2 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 1.744 (13.540) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 1.532 (28.917) | fits | 1 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.761 (13.479) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 9.515 (16.304) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.226 (1.150) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.076 (1.032) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.064 (3.124) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.077 (3.241) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.239 (1.181) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 1.140 (3.043) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.147 (2.928) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 2.172 (2.954) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.112 (2.893) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 2.712 (3.493) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 2.271 (3.052) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 2.279 (3.251) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 1.739 (2.521) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 2.806 (3.587) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 2.353 (3.135) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 2.627 (3.409) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.293 (3.074) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.116 (3.897) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 2.184 (2.965) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 2.490 (3.271) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 2.446 (3.228) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 2.370 (3.152) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 2.418 (3.200) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.657 (3.439) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 2.747 (3.529) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 2.445 (3.227) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 2.352 (3.133) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.420 (2.193) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 2.765 (4.160) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.110 (2.891) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 2.279 (3.250) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 4.857 (5.675) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 4.739 (5.530) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 4.847 (5.665) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 4.650 (5.272) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 4.495 (5.284) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 6.487 (7.623) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 4.805 (5.407) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 5.048 (5.837) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 37.282 (41.396) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 41.651 (53.021) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 38.137 (54.960) | MISS ceiling | 4 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 9.298 (17.357) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 94.039 (96.710) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 362.443 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 3.001 (4.175) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 1.294 (3.528) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.464 (1.371) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.529 (3.241) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 1.145 (3.528) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 1.255 (3.159) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp.service.acmp.first.if0` (backlog-adp) | 8.766 | fits | 0 acmp | 5 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 85.320 | MISS ceiling | 11 acmp | 5 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 8.804 | fits | 0 adp | 5 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 49.294 | MISS T_svc | 7 adp | 5 | 4 |
| AECP record released under the composed load, first | 0 | `backlog-adp.service.aecp.first.if0` (backlog-adp) | 8.801 | fits | 0 aecp | 5 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp-refill.service.aecp.last.if0` (backlog-adp-refill) | 253.289 | MISS ceiling | 15 aecp | 5 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog-adp.service.maap.first.if0` (backlog-adp) | 8.791 | fits | 0 maap | 5 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 49.331 | MISS T_svc | 6 maap | 5 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 578.123 | STARVED: never released | 0 srp | 5 | 4 |
| SRP record released under the composed load, last | 0 | `backlog-adp-refill.service.srp.last.if0` (backlog-adp-refill) | at least 578.103 | STARVED: never released | 31 srp | 5 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 3.259 (4.663) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 1.915 (1.916) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 1.249 (1.249) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 2.867 (3.241) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 90.527 | 22 | 440,320 (8.806) | yes | - |
| backlog-adp | 541.704 | 36 | 947,087 (18.942) | no | {'srp': 32} |
| backlog-adp-refill | 578.139 | 38 | 925,940 (18.519) | no | {'srp': 32} |
| backlog-owed | 362.494 | 52 | 430,034 (8.601) | yes | - |
| fixture | 10.143 | 3 | 295,022 (5.900) | yes | - |

Composed maximum over the 4 backlog windows: at least 947,087 CPU cycles (18.942 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 440,320 (8.806 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 76,606 | 1.532 | 10 | 20 | fits | 687,582 | 119 (14) | 0.034 |
| LINK_UP | `adp.link_up.if0` | 3,832 | 0.077 | 10 | 200 | fits | 162,041 | 88 (11) | 0.090 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 56,991 | 1.140 | 10 | 200 | fits | 67,071 | 46 (39) | 0.090 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 11,968 | 0.239 | 10 | 200 | fits | 3,858 | 9 (11) | 0.160 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 110,894 | 2.218 | 10 | 20 | fits | 689,999 | 140 (35) | 0.033 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 87,210 | 1.744 | 10 | 20 | fits | 676,983 | 117 (14) | 0.033 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 38,053 | 0.761 | 10 | 20 | fits | 673,925 | 118 (14) | 0.033 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 46,678 | 0.934 | 10 | 20 | fits | 690,773 | 140 (35) | 0.034 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 143,328 | 2.867 | 10 | 18 | fits | 162,041 | 88 | 0.090 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 95,750 | 1.915 | 10 | 18 | fits | 95,782 | 29 | 0.113 |
| malformed MRPDU discard | `srp.malformed.if0` | 62,441 | 1.249 | 10 | 18 | fits | 62,473 | 29 | 0.109 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 162,939 | 3.259 | 210 | 218 | fits | 233,163 | 78 | 0.090 |
| an event behind 15 others | `backlog.event.if0` | 464,925 | 9.298 | 10 | 200 | fits | 427,543 | 356 | 0.072 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 1,864,079 | 37.282 | 10 | 20 | MISS ceiling | 287,368 | 256 | 0.064 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 440,216 | 8.804 | 10 | 200 | fits | 440,320 | 389 | 0.070 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 1,523,261 | 30.465 | 10 | 200 | MISS T_svc | 315,397 | 324 | 0.071 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 438,087 | 8.762 | 10 | 20 | fits | 440,320 | 389 | 0.070 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 2,067,132 | 41.343 | 10 | 20 | MISS ceiling | 287,368 | 256 | 0.064 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 439,879 | 8.798 | 10 | 24 | fits | 440,320 | 389 | 0.070 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 4,019,058 | 80.381 | 10 | 24 | MISS ceiling | 208,361 | 169 | 0.060 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 439,359 | 8.787 | 10 | 50 | fits | 440,320 | 389 | 0.070 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 1,522,513 | 30.450 | 10 | 50 | MISS T_svc | 315,397 | 324 | 0.071 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 1,207,084 | 24.142 | 10 | 18 | MISS ceiling | 340,409 | 348 | 0.074 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 4,387,785 | 87.756 | 10 | 18 | MISS ceiling | 58,488 | 47 | 0.107 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 2,082,573 | 41.651 | 10 | 20 | MISS ceiling | 947,087 | 411 | 0.041 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 437,824 | 8.756 | 10 | 200 | fits | 623,843 | 412 | 0.048 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,464,711 | 49.294 | 10 | 200 | MISS T_svc | 947,087 | 411 | 0.041 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 438,280 | 8.766 | 10 | 20 | fits | 623,843 | 412 | 0.048 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 4,240,088 | 84.802 | 10 | 20 | MISS ceiling | 887,476 | 317 | 0.037 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 440,072 | 8.801 | 10 | 24 | fits | 623,843 | 412 | 0.048 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 12,638,200 | 252.764 | 10 | 24 | MISS ceiling | 803,690 | 230 | 0.032 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 439,552 | 8.791 | 10 | 50 | fits | 623,843 | 412 | 0.048 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,466,549 | 49.331 | 10 | 50 | MISS T_svc | 947,087 | 411 | 0.041 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 27,084,378 | 541.688 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 27,083,371 | 541.667 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 1,906,870 | 38.137 | 10 | 20 | MISS ceiling | 917,209 | 349 | 0.039 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 437,824 | 8.756 | 10 | 200 | fits | 623,843 | 412 | 0.048 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 2,268,188 | 45.364 | 10 | 200 | MISS T_svc | 917,209 | 349 | 0.039 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 438,280 | 8.766 | 10 | 20 | fits | 623,843 | 412 | 0.048 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 4,265,994 | 85.320 | 10 | 20 | MISS ceiling | 917,209 | 349 | 0.039 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 440,072 | 8.801 | 10 | 24 | fits | 623,843 | 412 | 0.048 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 12,664,446 | 253.289 | 10 | 24 | MISS ceiling | 803,655 | 230 | 0.032 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 439,552 | 8.791 | 10 | 50 | fits | 623,843 | 412 | 0.048 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,445,402 | 48.908 | 10 | 50 | MISS T_svc | 925,940 | 404 | 0.040 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 28,906,133 | 578.123 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 28,905,126 | 578.103 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 4,701,934 | 94.039 | 10 | 20 | MISS ceiling | 200,519 | 147 | 0.051 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,122,153 | 362.443 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,122,115 | 362.442 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,122,078 | 362.442 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,122,040 | 362.441 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 371,336 | 7.427 | 10 | 200 | fits | 336,167 | 341 | 0.068 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 1,489,212 | 29.784 | 10 | 200 | MISS T_svc | 291,019 | 255 | 0.064 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 369,207 | 7.384 | 10 | 20 | fits | 336,167 | 341 | 0.068 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 1,972,057 | 39.441 | 10 | 20 | MISS ceiling | 179,133 | 75 | 0.065 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 370,999 | 7.420 | 10 | 24 | fits | 336,167 | 341 | 0.068 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 5,354,010 | 107.080 | 10 | 24 | MISS ceiling | 182,584 | 125 | 0.049 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 370,479 | 7.410 | 10 | 50 | fits | 336,167 | 341 | 0.068 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 1,488,464 | 29.769 | 10 | 50 | MISS T_svc | 291,019 | 255 | 0.064 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 800,286 | 16.006 | 10 | 18 | MISS T_svc | 430,034 | 378 | 0.082 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 4,170,756 | 83.415 | 10 | 18 | MISS ceiling | 252,172 | 173 | 0.068 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 314,882 | 6.298 | 10 | 20 | fits | 698,277 | 140 (29) | 0.035 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 406,318 | 8.126 | 10 | 20 | fits | 699,847 | 146 (35) | 0.036 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 105,875 | 2.117 | 10 | 20 | fits | 603,614 | 130 (12) | 0.037 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 26,473 | 0.529 | 10 | 50 | fits | 162,041 | 88 | 0.090 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 62,741 | 1.255 | 10 | 50 | fits | 84,191 | 43 | 0.105 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 27,735 | 0.555 | 10 | 50 | fits | 69,208 | 37 | 0.101 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 57,234 | 1.145 | 10 | 50 | fits | 101,646 | 70 | 0.095 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 64,714 | 1.294 | 10 | 50 | fits | 101,646 | 70 | 0.095 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 23,184 | 0.464 | 10 | 50 | fits | 68,530 | 47 | 0.102 |
| LINK_UP | `adp.link_up.if0` | 3,832 | 0.077 | 10 | 200 | fits | 162,041 | 88 (11) | 0.090 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 56,991 | 1.140 | 10 | 200 | fits | 67,071 | 46 (39) | 0.090 |
| LINK_DOWN | `adp.link_down.if0` | 3,212 | 0.064 | 10 | 200 | fits | 156,205 | 27 (9) | 0.090 |
| LINK_UP | `adp.link_up.if0` | 3,832 | 0.077 | 10 | 200 | fits | 162,041 | 88 (11) | 0.090 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 56,991 | 1.140 | 10 | 200 | fits | 67,071 | 46 (39) | 0.090 |
| GM_CHANGE | `adp.gm_change.if0` | 3,801 | 0.076 | 10 | 200 | fits | 51,576 | 18 (11) | 0.103 |
| LINK_UP | `adp.link_up.if0` | 3,832 | 0.077 | 10 | 200 | fits | 162,041 | 88 (11) | 0.090 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 56,991 | 1.140 | 10 | 200 | fits | 67,071 | 46 (39) | 0.090 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 11,286 | 0.226 | 10 | 200 | fits | 57,477 | 38 (31) | 0.108 |
| LINK_UP | `adp.link_up.if0` | 3,832 | 0.077 | 10 | 200 | fits | 162,041 | 88 (11) | 0.090 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 56,991 | 1.140 | 10 | 200 | fits | 67,071 | 46 (39) | 0.090 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 11,286 | 0.226 | 10 | 200 | fits | 57,477 | 38 (31) | 0.108 |
| set_name | `aecp_fanout.set_name.if0` | 324,352 | 6.487 | 10 | 24 | fits | 381,146 | 623 | 0.047 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 232,476 | 4.650 | 10 | 24 | fits | 263,623 | 328 | 0.058 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 224,728 | 4.495 | 10 | 24 | fits | 264,189 | 311 | 0.056 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 224,720 | 4.494 | 10 | 24 | fits | 264,177 | 311 | 0.056 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 242,328 | 4.847 | 10 | 24 | fits | 283,235 | 351 | 0.054 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 242,875 | 4.857 | 10 | 24 | fits | 283,765 | 351 | 0.054 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 240,234 | 4.805 | 10 | 24 | fits | 270,369 | 324 | 0.062 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 236,972 | 4.739 | 10 | 24 | fits | 276,509 | 362 | 0.054 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 252,377 | 5.048 | 10 | 24 | fits | 291,834 | 369 | 0.058 |
| BIND_RX | `acmp.bind_rx.if0` | 49,222 | 0.984 | 10 | 20 | fits | 124,653 | 83 (77) | 0.088 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 621,701 | 12.434 | 10 | 20 | MISS T_svc | 792,632 | 153 (32) | 0.033 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 478,674 | 9.573 | 10 | 20 | fits | 800,352 | 168 (47) | 0.033 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 475,771 | 9.515 | 10 | 20 | fits | 815,199 | 171 (50) | 0.034 |
| PROBE_TX | `acmp.probe_tx.if0` | 402,313 | 8.046 | 10 | 20 | fits | 716,890 | 191 (48) | 0.035 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 468,266 | 9.365 | 10 | 20 | fits | 711,492 | 159 (48) | 0.036 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 467,091 | 9.342 | 10 | 20 | fits | 710,375 | 159 (48) | 0.036 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 466,902 | 9.338 | 10 | 20 | fits | 710,221 | 159 (48) | 0.036 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 71,016 | 1.420 | 10 | 24 | fits | 109,652 | 48 | 0.075 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 140,285 | 2.806 | 10 | 24 | fits | 179,367 | 125 | 0.050 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 117,647 | 2.353 | 10 | 24 | fits | 156,726 | 74 | 0.056 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 122,306 | 2.446 | 10 | 24 | fits | 161,385 | 85 | 0.054 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 137,357 | 2.747 | 10 | 24 | fits | 176,439 | 90 | 0.061 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 122,251 | 2.445 | 10 | 24 | fits | 161,333 | 84 | 0.054 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 117,588 | 2.352 | 10 | 24 | fits | 156,670 | 73 | 0.056 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 131,345 | 2.627 | 10 | 24 | fits | 170,427 | 75 | 0.063 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 114,640 | 2.293 | 10 | 24 | fits | 153,719 | 66 | 0.057 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 155,778 | 3.116 | 10 | 24 | fits | 194,857 | 161 | 0.046 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 109,186 | 2.184 | 10 | 24 | fits | 148,265 | 53 | 0.059 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 124,492 | 2.490 | 10 | 24 | fits | 163,571 | 59 | 0.065 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 118,522 | 2.370 | 10 | 24 | fits | 157,601 | 70 | 0.055 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 120,923 | 2.418 | 10 | 24 | fits | 160,002 | 76 | 0.054 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 132,864 | 2.657 | 10 | 24 | fits | 171,943 | 74 | 0.062 |
| get_configuration | `aecp.get_configuration.if0` | 105,583 | 2.112 | 10 | 24 | fits | 144,635 | 48 | 0.059 |
| entity_available | `aecp.entity_available.if0` | 107,338 | 2.147 | 10 | 24 | fits | 146,393 | 52 | 0.058 |
| get_name | `aecp.get_name.if0` | 113,544 | 2.271 | 10 | 24 | fits | 152,599 | 65 | 0.058 |
| get_counters | `aecp.get_counters.if0` | 135,579 | 2.712 | 10 | 24 | fits | 174,661 | 92 | 0.064 |
| get_avb_info | `aecp.get_avb_info.if0` | 108,625 | 2.172 | 10 | 24 | fits | 147,680 | 48 | 0.059 |
| unknown_command | `aecp.unknown_command.if0` | 105,487 | 2.110 | 10 | 24 | fits | 144,542 | 48 | 0.059 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 86,968 | 1.739 | 10 | 24 | fits | 126,050 | 58 | 0.083 |
| set_name | `aecp.set_name.if0` | 138,266 | 2.765 | 10 | 24 | fits | 208,018 | 128 | 0.058 |
| lock_entity | `aecp.lock_entity.if0` | 113,926 | 2.279 | 10 | 24 | fits | 162,564 | 78 | 0.061 |
| unlock_entity | `aecp.unlock_entity.if0` | 113,931 | 2.279 | 10 | 24 | fits | 162,493 | 78 | 0.061 |
| LINK_UP | `fixture.link_up.if0` | 3,832 | 0.077 | 10 | 200 | fits | 162,041 | 88 (11) | 0.090 |
| malformed MRPDU discard | `fixture.malformed.if0` | 59,204 | 1.184 | 10 | 18 | fits | 59,236 | 29 | 0.113 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 150,056 | 3.001 | 10 | 24 | fits | 208,772 | 128 | 0.058 |
| LINK_DOWN | `fixture.link_down.if0` | 3,212 | 0.064 | 10 | 200 | fits | 158,448 | 27 (9) | 0.090 |
| BIND_RX | `fixture.bind_rx.if0` | 64,174 | 1.283 | 10 | 20 | fits | 129,539 | 89 (77) | 0.090 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 139,431 | 2.789 | 10 | 20 | fits | 712,953 | 169 (35) | 0.035 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 653,021 | 13.060 | 10 | 20 | MISS T_svc | 783,343 | 150 (29) | 0.032 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 294,971 | 5.899 | 10 | 200 | fits | 295,022 | 245 | 0.076 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 294,971 | 5.899 | 10 | 200 | fits | 295,022 | 245 | 0.076 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 294,836 | 5.897 | 10 | 20 | fits | 295,022 | 245 | 0.076 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 294,836 | 5.897 | 10 | 20 | fits | 295,022 | 245 | 0.076 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 294,938 | 5.899 | 10 | 24 | fits | 295,022 | 245 | 0.076 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 294,938 | 5.899 | 10 | 24 | fits | 295,022 | 245 | 0.076 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 294,906 | 5.898 | 10 | 50 | fits | 295,022 | 245 | 0.076 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 294,906 | 5.898 | 10 | 50 | fits | 295,022 | 245 | 0.076 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 294,873 | 5.897 | 10 | 18 | fits | 295,022 | 245 | 0.076 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 294,873 | 5.897 | 10 | 18 | fits | 295,022 | 245 | 0.076 |

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
