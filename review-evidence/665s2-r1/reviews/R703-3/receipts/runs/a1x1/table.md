### 1x1

22 of 81 paths and 58 of 141 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 1.625 (3.957) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 24.767 (44.768) | MISS ceiling | 0 acmp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 10.373 (25.917) | MISS T_svc | 0 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 25.174 (50.781) | MISS ceiling | 0 adp | 2 | 2 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 3.339 (23.096) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 11.080 (26.313) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 6.367 (26.360) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 3.479 (23.024) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 12.025 (29.871) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 2.903 (44.038) | fits | 2 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 1.910 (22.309) | fits | 1 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 5.478 (47.980) | fits | 3 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 1.639 (21.792) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 4.568 (22.152) | fits | 2 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 7.985 (46.719) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 6.556 (26.864) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.294 (1.628) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.105 (1.462) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.078 (5.480) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.106 (4.969) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.128 (1.993) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.865 (3.568) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 4.491 (5.633) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 4.515 (5.656) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 4.422 (5.564) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 4.917 (6.059) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 4.693 (5.835) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 3.956 (5.410) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 2.495 (3.637) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 5.143 (6.285) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 4.332 (5.473) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 4.789 (5.931) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 4.730 (5.871) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 6.208 (7.349) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 4.027 (5.168) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 4.021 (5.162) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 4.491 (5.632) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 4.865 (6.006) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 4.953 (6.094) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 4.839 (5.980) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 4.485 (5.627) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 5.013 (6.154) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 4.843 (5.984) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 2.475 (3.607) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 4.809 (6.905) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 4.421 (5.562) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 3.948 (5.402) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 8.569 (9.778) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 8.203 (9.352) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 8.577 (9.788) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 8.047 (8.919) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 7.786 (8.935) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 11.332 (12.980) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 7.969 (8.807) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 8.215 (9.364) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 63.304 (70.047) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 67.932 (81.835) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 88.334 (107.649) | MISS ceiling | 4 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 15.487 (29.108) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 126.292 (130.313) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 363.984 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 5.756 (8.837) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 1.499 (4.232) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.707 (2.015) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.903 (4.969) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 1.241 (4.232) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 1.863 (3.919) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp.service.acmp.first.if0` (backlog-adp) | 18.696 | MISS T_svc | 0 acmp | 5 | 4 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 141.206 | MISS ceiling | 11 acmp | 5 | 4 |
| ADP record released under the composed load, first | 0 | `backlog-adp.service.adp.first.if0` (backlog-adp) | 18.687 | MISS T_svc | 0 adp | 5 | 4 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 101.250 | MISS T_svc | 4 adp | 5 | 4 |
| AECP record released under the composed load, first | 0 | `backlog-adp.service.aecp.first.if0` (backlog-adp) | 18.732 | MISS T_svc | 0 aecp | 5 | 4 |
| AECP record released under the composed load, last | 0 | `backlog-adp-refill.service.aecp.last.if0` (backlog-adp-refill) | 417.496 | MISS ceiling | 15 aecp | 5 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog-adp.service.maap.first.if0` (backlog-adp) | 18.721 | MISS T_svc | 0 maap | 5 | 4 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 81.546 | MISS ceiling | 6 maap | 5 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 628.320 | STARVED: never released | 0 srp | 5 | 5 |
| SRP record released under the composed load, last | 0 | `backlog-adp-refill.service.srp.last.if0` (backlog-adp-refill) | at least 628.299 | STARVED: never released | 31 srp | 5 | 5 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 4.927 (7.072) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 2.768 (2.768) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 2.149 (2.150) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 4.435 (4.969) | fits | 0 events | 1 | 0 |

Composed windows: the longest pass is the composed maximum only where the window released its whole load.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 162.912 | 27 | 740,260 (14.805) | yes | - |
| backlog-adp | 567.985 | 22 | 1,565,803 (31.316) | no | {'srp': 32} |
| backlog-adp-refill | 628.336 | 24 | 1,531,355 (30.627) | no | {'srp': 32} |
| backlog-owed | 364.034 | 44 | 582,677 (11.654) | yes | - |
| fixture | 20.000 | 3 | 418,342 (8.367) | yes | - |

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 228,411 | 4.568 | 10 | 20 | fits | 1,107,592 | 74 (14) | 0.891 |
| LINK_UP | `adp.link_up.if0` | 5,281 | 0.106 | 10 | 200 | fits | 248,452 | 88 (11) | 0.886 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 43,255 | 0.865 | 10 | 200 | fits | 101,078 | 46 (39) | 0.870 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 6,395 | 0.128 | 10 | 200 | fits | 5,288 | 9 (11) | 0.860 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 167,999 | 3.360 | 10 | 20 | fits | 1,114,854 | 95 (35) | 0.891 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 81,948 | 1.639 | 10 | 20 | fits | 1,089,588 | 72 (14) | 0.891 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 399,272 | 7.985 | 10 | 20 | fits | 1,086,257 | 73 (14) | 0.892 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 145,164 | 2.903 | 10 | 20 | fits | 1,115,665 | 95 (35) | 0.891 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 221,759 | 4.435 | 10 | 18 | fits | 248,452 | 88 | 0.886 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 138,381 | 2.768 | 10 | 18 | fits | 138,413 | 29 | 0.864 |
| malformed MRPDU discard | `srp.malformed.if0` | 87,458 | 1.749 | 10 | 18 | fits | 87,490 | 29 | 0.858 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 246,361 | 4.927 | 210 | 218 | fits | 353,587 | 78 | 0.872 |
| an event behind 15 others | `backlog.event.if0` | 774,336 | 15.487 | 10 | 200 | MISS T_svc | 715,146 | 355 | 0.879 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 3,165,192 | 63.304 | 10 | 20 | MISS ceiling | 475,100 | 216 | 0.884 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 740,156 | 14.803 | 10 | 200 | MISS T_svc | 740,260 | 388 | 0.879 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 2,551,621 | 51.032 | 10 | 200 | MISS T_svc | 514,404 | 284 | 0.882 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 738,027 | 14.761 | 10 | 20 | MISS T_svc | 740,260 | 388 | 0.879 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 3,499,707 | 69.994 | 10 | 20 | MISS ceiling | 475,100 | 216 | 0.884 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 739,819 | 14.796 | 10 | 24 | MISS T_svc | 740,260 | 388 | 0.879 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 6,959,752 | 139.195 | 10 | 24 | MISS ceiling | 316,300 | 123 | 0.888 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 739,299 | 14.786 | 10 | 50 | MISS T_svc | 740,260 | 388 | 0.879 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 2,550,873 | 51.017 | 10 | 50 | MISS ceiling | 514,404 | 284 | 0.882 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 4,205,275 | 84.105 | 10 | 18 | MISS ceiling | 361,149 | 168 | 0.889 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 7,945,932 | 158.919 | 10 | 18 | MISS ceiling | 75,111 | 29 | 0.869 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 3,396,608 | 67.932 | 10 | 20 | MISS ceiling | 1,565,803 | 365 | 0.889 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 934,343 | 18.687 | 10 | 200 | MISS T_svc | 950,310 | 387 | 0.886 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 4,075,468 | 81.509 | 10 | 200 | MISS T_svc | 1,565,803 | 365 | 0.889 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 934,799 | 18.696 | 10 | 20 | MISS T_svc | 950,310 | 387 | 0.886 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 7,023,808 | 140.476 | 10 | 20 | MISS ceiling | 1,473,907 | 271 | 0.891 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 936,592 | 18.732 | 10 | 24 | MISS T_svc | 950,310 | 387 | 0.886 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 20,838,988 | 416.780 | 10 | 24 | MISS ceiling | 1,334,076 | 184 | 0.893 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 936,072 | 18.721 | 10 | 50 | MISS T_svc | 950,310 | 387 | 0.886 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 4,077,306 | 81.546 | 10 | 50 | MISS ceiling | 1,565,803 | 365 | 0.889 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 28,398,413 | 567.968 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 28,397,406 | 567.948 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 4,416,715 | 88.334 | 10 | 20 | MISS ceiling | 1,520,863 | 303 | 0.890 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 934,343 | 18.687 | 10 | 200 | MISS T_svc | 950,310 | 387 | 0.886 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 5,062,515 | 101.250 | 10 | 200 | MISS T_svc | 1,520,863 | 303 | 0.890 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 934,799 | 18.696 | 10 | 20 | MISS T_svc | 950,310 | 387 | 0.886 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 7,060,321 | 141.206 | 10 | 20 | MISS ceiling | 1,520,863 | 303 | 0.890 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 936,592 | 18.732 | 10 | 24 | MISS T_svc | 950,310 | 387 | 0.886 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 20,874,780 | 417.496 | 10 | 24 | MISS ceiling | 1,334,033 | 184 | 0.893 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 936,072 | 18.721 | 10 | 50 | MISS T_svc | 950,310 | 387 | 0.886 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 4,042,858 | 80.857 | 10 | 50 | MISS ceiling | 1,531,355 | 358 | 0.890 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 31,415,978 | 628.320 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 31,414,971 | 628.299 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,314,582 | 126.292 | 10 | 20 | MISS ceiling | 475,598 | 190 | 0.881 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,199,180 | 363.984 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,199,143 | 363.983 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,199,105 | 363.982 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,199,068 | 363.981 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 594,233 | 11.885 | 10 | 200 | MISS T_svc | 562,433 | 340 | 0.877 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 2,249,925 | 44.998 | 10 | 200 | MISS T_svc | 520,138 | 260 | 0.881 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 592,103 | 11.842 | 10 | 20 | MISS T_svc | 562,433 | 340 | 0.877 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 2,982,629 | 59.653 | 10 | 20 | MISS ceiling | 331,376 | 80 | 0.880 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 593,896 | 11.878 | 10 | 24 | MISS T_svc | 562,433 | 340 | 0.877 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 7,664,174 | 153.283 | 10 | 24 | MISS ceiling | 319,511 | 123 | 0.887 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 593,376 | 11.868 | 10 | 50 | MISS T_svc | 562,433 | 340 | 0.877 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 2,249,178 | 44.984 | 10 | 50 | MISS T_svc | 520,138 | 260 | 0.881 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 3,298,536 | 65.971 | 10 | 18 | MISS ceiling | 314,450 | 170 | 0.875 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 9,134,500 | 182.690 | 10 | 18 | MISS ceiling | 146,417 | 35 | 0.871 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 721,092 | 14.422 | 10 | 20 | MISS T_svc | 1,126,582 | 95 (29) | 0.892 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 518,648 | 10.373 | 10 | 20 | MISS T_svc | 1,295,856 | 104 (35) | 0.891 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 95,524 | 1.910 | 10 | 20 | fits | 1,115,462 | 95 (12) | 0.891 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 45,163 | 0.903 | 10 | 50 | fits | 248,452 | 88 | 0.886 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 77,716 | 1.554 | 10 | 50 | fits | 104,332 | 37 | 0.876 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 93,164 | 1.863 | 10 | 50 | fits | 103,754 | 37 | 0.875 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 62,042 | 1.241 | 10 | 50 | fits | 135,183 | 64 | 0.881 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 74,970 | 1.499 | 10 | 50 | fits | 135,183 | 64 | 0.881 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 35,338 | 0.707 | 10 | 50 | fits | 100,762 | 47 | 0.868 |
| LINK_UP | `adp.link_up.if0` | 5,281 | 0.106 | 10 | 200 | fits | 248,452 | 88 (11) | 0.886 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 43,255 | 0.865 | 10 | 200 | fits | 101,078 | 46 (39) | 0.870 |
| LINK_DOWN | `adp.link_down.if0` | 3,917 | 0.078 | 10 | 200 | fits | 274,011 | 33 (9) | 0.879 |
| LINK_UP | `adp.link_up.if0` | 5,281 | 0.106 | 10 | 200 | fits | 248,452 | 88 (11) | 0.886 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 43,255 | 0.865 | 10 | 200 | fits | 101,078 | 46 (39) | 0.870 |
| GM_CHANGE | `adp.gm_change.if0` | 5,241 | 0.105 | 10 | 200 | fits | 73,116 | 18 (11) | 0.865 |
| LINK_UP | `adp.link_up.if0` | 5,281 | 0.106 | 10 | 200 | fits | 248,452 | 88 (11) | 0.886 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 43,255 | 0.865 | 10 | 200 | fits | 101,078 | 46 (39) | 0.870 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 14,695 | 0.294 | 10 | 200 | fits | 81,384 | 38 (31) | 0.865 |
| LINK_UP | `adp.link_up.if0` | 5,281 | 0.106 | 10 | 200 | fits | 248,452 | 88 (11) | 0.886 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 43,255 | 0.865 | 10 | 200 | fits | 101,078 | 46 (39) | 0.870 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 14,695 | 0.294 | 10 | 200 | fits | 81,384 | 38 (31) | 0.865 |
| set_name | `aecp_fanout.set_name.if0` | 566,621 | 11.332 | 10 | 24 | MISS T_svc | 649,005 | 601 | 0.887 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 402,339 | 8.047 | 10 | 24 | fits | 445,942 | 316 | 0.880 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 388,673 | 7.773 | 10 | 24 | fits | 446,073 | 299 | 0.883 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 389,281 | 7.786 | 10 | 24 | fits | 446,753 | 299 | 0.883 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 428,827 | 8.577 | 10 | 24 | fits | 489,414 | 350 | 0.880 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 428,446 | 8.569 | 10 | 24 | fits | 488,907 | 350 | 0.880 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 398,460 | 7.969 | 10 | 24 | fits | 440,347 | 317 | 0.881 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 410,172 | 8.203 | 10 | 24 | fits | 467,583 | 350 | 0.885 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 410,731 | 8.215 | 10 | 24 | fits | 468,203 | 350 | 0.885 |
| BIND_RX | `acmp.bind_rx.if0` | 81,248 | 1.625 | 10 | 20 | fits | 197,841 | 82 (77) | 0.874 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 601,231 | 12.025 | 10 | 20 | MISS T_svc | 1,493,556 | 104 (32) | 0.891 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 166,936 | 3.339 | 10 | 20 | fits | 1,154,810 | 113 (47) | 0.891 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 327,784 | 6.556 | 10 | 20 | fits | 1,343,188 | 119 (50) | 0.890 |
| PROBE_TX | `acmp.probe_tx.if0` | 173,969 | 3.479 | 10 | 20 | fits | 1,151,178 | 115 (48) | 0.891 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 318,368 | 6.367 | 10 | 20 | fits | 1,317,985 | 117 (48) | 0.891 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 1,238,343 | 24.767 | 10 | 20 | MISS ceiling | 1,315,766 | 117 (48) | 0.891 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 554,007 | 11.080 | 10 | 20 | MISS T_svc | 1,315,664 | 117 (48) | 0.891 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 123,766 | 2.475 | 10 | 24 | fits | 180,352 | 46 | 0.881 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 257,171 | 5.143 | 10 | 24 | fits | 314,234 | 124 | 0.887 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 216,609 | 4.332 | 10 | 24 | fits | 273,668 | 73 | 0.886 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 224,564 | 4.491 | 10 | 24 | fits | 281,623 | 83 | 0.886 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 224,263 | 4.485 | 10 | 24 | fits | 281,326 | 82 | 0.886 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 250,655 | 5.013 | 10 | 24 | fits | 307,718 | 89 | 0.888 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 242,152 | 4.843 | 10 | 24 | fits | 299,215 | 78 | 0.888 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 239,468 | 4.789 | 10 | 24 | fits | 296,531 | 74 | 0.888 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 236,487 | 4.730 | 10 | 24 | fits | 293,546 | 71 | 0.888 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 310,400 | 6.208 | 10 | 24 | fits | 367,459 | 166 | 0.889 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 201,335 | 4.027 | 10 | 24 | fits | 258,394 | 52 | 0.885 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 201,044 | 4.021 | 10 | 24 | fits | 258,103 | 51 | 0.886 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 243,237 | 4.865 | 10 | 24 | fits | 300,296 | 75 | 0.887 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 247,660 | 4.953 | 10 | 24 | fits | 304,719 | 81 | 0.888 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 241,937 | 4.839 | 10 | 24 | fits | 298,996 | 73 | 0.888 |
| get_configuration | `aecp.get_configuration.if0` | 221,120 | 4.422 | 10 | 24 | fits | 278,179 | 53 | 0.888 |
| entity_available | `aecp.entity_available.if0` | 224,574 | 4.491 | 10 | 24 | fits | 281,637 | 57 | 0.888 |
| get_name | `aecp.get_name.if0` | 234,665 | 4.693 | 10 | 24 | fits | 291,728 | 70 | 0.888 |
| get_counters | `aecp.get_counters.if0` | 245,872 | 4.917 | 10 | 24 | fits | 302,935 | 86 | 0.889 |
| get_avb_info | `aecp.get_avb_info.if0` | 225,726 | 4.515 | 10 | 24 | fits | 282,789 | 53 | 0.887 |
| unknown_command | `aecp.unknown_command.if0` | 221,061 | 4.421 | 10 | 24 | fits | 278,124 | 53 | 0.888 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 124,768 | 2.495 | 10 | 24 | fits | 181,831 | 50 | 0.881 |
| set_name | `aecp.set_name.if0` | 240,454 | 4.809 | 10 | 24 | fits | 345,233 | 106 | 0.882 |
| lock_entity | `aecp.lock_entity.if0` | 197,776 | 3.956 | 10 | 24 | fits | 270,477 | 66 | 0.885 |
| unlock_entity | `aecp.unlock_entity.if0` | 197,404 | 3.948 | 10 | 24 | fits | 270,094 | 65 | 0.885 |
| LINK_UP | `fixture.link_up.if0` | 5,281 | 0.106 | 10 | 200 | fits | 248,452 | 88 (11) | 0.886 |
| malformed MRPDU discard | `fixture.malformed.if0` | 107,473 | 2.149 | 10 | 18 | fits | 107,505 | 35 | 0.871 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 287,812 | 5.756 | 10 | 24 | fits | 345,891 | 106 | 0.881 |
| LINK_DOWN | `fixture.link_down.if0` | 3,917 | 0.078 | 10 | 200 | fits | 277,531 | 33 (9) | 0.879 |
| BIND_RX | `fixture.bind_rx.if0` | 81,248 | 1.625 | 10 | 20 | fits | 179,721 | 82 (77) | 0.868 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 273,899 | 5.478 | 10 | 20 | fits | 1,151,720 | 124 (35) | 0.890 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 1,258,710 | 25.174 | 10 | 20 | MISS ceiling | 1,291,990 | 98 (29) | 0.892 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 418,291 | 8.366 | 10 | 200 | fits | 418,342 | 224 | 0.882 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 418,291 | 8.366 | 10 | 200 | fits | 418,342 | 224 | 0.882 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 418,156 | 8.363 | 10 | 20 | fits | 418,342 | 224 | 0.882 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 418,156 | 8.363 | 10 | 20 | fits | 418,342 | 224 | 0.882 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 418,258 | 8.365 | 10 | 24 | fits | 418,342 | 224 | 0.882 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 418,258 | 8.365 | 10 | 24 | fits | 418,342 | 224 | 0.882 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 418,226 | 8.365 | 10 | 50 | fits | 418,342 | 224 | 0.882 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 418,226 | 8.365 | 10 | 50 | fits | 418,342 | 224 | 0.882 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 586,102 | 11.722 | 10 | 18 | MISS T_svc | 167,909 | 37 | 0.871 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 586,102 | 11.722 | 10 | 18 | MISS T_svc | 167,909 | 37 | 0.871 |

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
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
