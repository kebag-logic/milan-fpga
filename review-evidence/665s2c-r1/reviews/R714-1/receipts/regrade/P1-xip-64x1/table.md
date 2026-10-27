### 1x1

71 of 78 paths and 120 of 138 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 30.846 (71.302) | MISS ceiling | 0 acmp | 2 | 2 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 48.281 (95.000) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 41.050 (91.201) | MISS ceiling | 0 adp | 2 | 2 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 35.799 (54.762) | MISS ceiling | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 11.158 (54.294) | MISS T_svc | 1 acmp | 1 | 1 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 36.424 (106.613) | MISS ceiling | 0 acmp | 1 | 1 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 14.156 (60.860) | MISS T_svc | 1 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 9.486 (30.956) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 19.112 (85.357) | MISS T_svc | 2 events | 1 | 1 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 20.868 (87.484) | MISS ceiling | 1 events | 1 | 1 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 20.033 (88.596) | MISS ceiling | 2 events | 2 | 2 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 20.579 (83.763) | MISS ceiling | 1 events | 1 | 1 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 17.545 (74.042) | MISS T_svc | 2 events | 1 | 1 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 15.306 (85.106) | MISS T_svc | 2 events | 1 | 1 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 4.189 (15.792) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 1.182 (13.011) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 38.301 (130.986) | MISS T_svc | 2 events | 2 | 1 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 3.547 (37.834) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 7.426 (13.778) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 6.047 (14.768) | fits | 1 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 21.864 (41.865) | MISS T_svc | 0 aecp | 1 | 1 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 20.466 (40.551) | MISS T_svc | 0 aecp | 1 | 1 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 20.549 (40.550) | MISS T_svc | 0 aecp | 1 | 1 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 20.931 (40.932) | MISS T_svc | 0 aecp | 1 | 1 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 23.958 (43.959) | MISS T_svc | 0 aecp | 1 | 1 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 26.777 (46.233) | MISS ceiling | 0 aecp | 1 | 1 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 18.691 (38.691) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 18.703 (38.841) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 23.867 (43.867) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 22.368 (54.536) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 23.726 (31.295) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 21.109 (41.373) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 23.684 (43.685) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 20.515 (40.516) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 20.773 (40.773) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 32.338 (52.338) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 20.703 (40.704) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 20.638 (40.638) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 23.323 (43.323) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 20.732 (40.732) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 23.855 (43.855) | MISS T_svc | 0 aecp | 1 | 1 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 11.870 (23.247) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 23.288 (46.352) | MISS T_svc | 0 aecp | 1 | 1 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 20.097 (40.014) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 21.920 (41.924) | MISS T_svc | 0 aecp | 1 | 1 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 29.615 (49.614) | MISS ceiling | 0 aecp | 1 | 1 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 27.332 (46.597) | MISS ceiling | 0 aecp | 1 | 1 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 28.643 (49.591) | MISS ceiling | 0 aecp | 1 | 1 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 29.373 (48.308) | MISS ceiling | 0 aecp | 1 | 1 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 26.785 (47.047) | MISS ceiling | 0 aecp | 2 | 2 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 35.867 (57.377) | MISS ceiling | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 28.563 (48.349) | MISS ceiling | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 39.067 (59.072) | MISS ceiling | 0 aecp | 1 | 1 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 390.476 (415.263) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 233.143 (294.534) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 345.534 (438.082) | MISS ceiling | 8 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 139.131 (231.810) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 524.957 (541.833) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 654.492 (671.371) | MISS ceiling | 11 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 17.352 (48.865) | MISS T_svc | 0 events | 1 | 1 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 12.906 (21.114) | MISS T_svc | 0 maap | 1 | 1 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 12.009 (37.834) | MISS T_svc | 0 events | 1 | 1 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 16.772 (48.865) | MISS T_svc | 0 events | 1 | 1 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 16.068 (39.393) | MISS T_svc | 0 events | 2 | 2 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 80.397 | MISS ceiling | 0 acmp | 5 | 5 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 423.479 | MISS ceiling | 11 acmp | 5 | 5 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 80.440 | MISS T_svc | 0 adp | 5 | 5 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 383.523 | MISS ceiling | 8 adp | 5 | 5 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 80.433 | MISS ceiling | 0 aecp | 5 | 5 |
| AECP record released under the composed load, last | 0 | `backlog-adp-refill.service.aecp.last.if0` (backlog-adp-refill) | at least 885.525 | STARVED: never released | 15 aecp | 5 | 5 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 80.423 | MISS ceiling | 0 maap | 5 | 5 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 294.705 | MISS ceiling | 6 maap | 5 | 5 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 885.519 | STARVED: never released | 0 srp | 5 | 5 |
| SRP record released under the composed load, last | 0 | `backlog-adp-refill.service.srp.last.if0` (backlog-adp-refill) | at least 885.499 | STARVED: never released | 31 srp | 5 | 5 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 53.279 (76.426) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 33.787 (41.860) | MISS ceiling | 0 srp | 1 | 1 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 24.103 (40.316) | MISS ceiling | 0 srp | 2 | 2 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 30.735 (37.834) | MISS ceiling | 0 events | 1 | 1 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 800.001 | 19 | 4,478,800 (89.576) | no | {'srp': 24} |
| backlog-adp | 733.196 | 12 | 4,225,806 (84.516) | no | {'aecp': 3, 'srp': 32} |
| backlog-adp-refill | 885.536 | 15 | 4,026,726 (80.535) | no | {'aecp': 1, 'srp': 32} |
| backlog-owed | 860.053 | 20 | 4,745,634 (94.913) | no | {'srp': 28} |
| fixture | 20.000 | 1 | 2,347,161 (46.943) | no | {'adp': 1, 'acmp': 1, 'aecp': 1, 'maap': 1, 'srp': 1} |

Composed maximum over the 4 backlog windows: at least 4,745,634 CPU cycles (94.913 ms), backlog-owed, a lower bound (load unreleased in backlog, backlog-adp, backlog-adp-refill, backlog-owed).
Over the windows that released their whole load only: none.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 877,236 | 17.545 | 10 | 20 | MISS T_svc | 1,501,978 | 57 (14) | 0.050 |
| LINK_UP | `adp.link_up.if0` | 177,343 | 3.547 | 10 | 200 | fits | 1,891,712 | 100 (11) | 0.107 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 302,363 | 6.047 | 10 | 200 | fits | 738,406 | 52 (39) | 0.091 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 371,325 | 7.426 | 10 | 200 | fits | 77,073 | 9 (11) | 0.181 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 1,001,657 | 20.033 | 10 | 20 | MISS ceiling | 2,222,051 | 89 (35) | 0.048 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 1,028,938 | 20.579 | 10 | 20 | MISS ceiling | 2,126,960 | 66 (14) | 0.048 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 765,282 | 15.306 | 10 | 20 | MISS T_svc | 2,070,884 | 67 (14) | 0.047 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 955,602 | 19.112 | 10 | 20 | MISS T_svc | 2,196,961 | 89 (35) | 0.048 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 1,536,773 | 30.735 | 10 | 18 | MISS ceiling | 1,891,712 | 100 | 0.107 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 1,689,364 | 33.787 | 10 | 18 | MISS ceiling | 1,481,433 | 40 | 0.119 |
| malformed MRPDU discard | `srp.malformed.if0` | 1,205,141 | 24.103 | 10 | 18 | MISS ceiling | 1,051,117 | 41 | 0.113 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 2,663,974 | 53.279 | 210 | 218 | fits | 2,567,275 | 89 | 0.095 |
| an event behind 15 others | `backlog.event.if0` | 6,956,532 | 139.131 | 10 | 200 | MISS T_svc | 4,478,800 | 355 | 0.087 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 19,523,776 | 390.476 | 10 | 20 | MISS ceiling | 2,886,793 | 257 | 0.078 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 4,021,996 | 80.440 | 10 | 200 | MISS T_svc | 4,275,683 | 388 | 0.086 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 14,735,992 | 294.720 | 10 | 200 | MISS ceiling | 3,399,459 | 325 | 0.083 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 4,019,867 | 80.397 | 10 | 20 | MISS ceiling | 4,275,683 | 388 | 0.086 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 20,506,912 | 410.138 | 10 | 20 | MISS ceiling | 2,886,793 | 257 | 0.078 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 4,021,659 | 80.433 | 10 | 24 | MISS ceiling | 4,275,683 | 388 | 0.086 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 36,172,629 | 723.453 | 10 | 24 | MISS ceiling | 1,424,508 | 141 | 0.064 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 4,021,139 | 80.423 | 10 | 50 | MISS ceiling | 4,275,683 | 388 | 0.086 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 14,735,244 | 294.705 | 10 | 50 | MISS ceiling | 3,399,459 | 325 | 0.083 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 37,302,881 | 746.058 | 10 | 18 | MISS ceiling | 1,130,512 | 67 | 0.118 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 39,997,865 | 799.957 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 11,657,148 | 233.143 | 10 | 20 | MISS ceiling | 4,225,806 | 353 | 0.075 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 3,507,175 | 70.143 | 10 | 200 | MISS T_svc | 4,237,339 | 390 | 0.058 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 13,996,241 | 279.925 | 10 | 200 | MISS ceiling | 4,225,806 | 353 | 0.075 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 3,507,631 | 70.153 | 10 | 20 | MISS ceiling | 4,237,339 | 390 | 0.058 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 20,780,286 | 415.606 | 10 | 20 | MISS ceiling | 3,110,088 | 259 | 0.066 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 3,509,423 | 70.188 | 10 | 24 | MISS ceiling | 4,237,339 | 390 | 0.058 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 36,659,213 | 733.184 | 10 | 24 | STARVED: never released | 0 | - | 0.000 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 3,508,903 | 70.178 | 10 | 50 | MISS ceiling | 4,237,339 | 390 | 0.058 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 13,998,079 | 279.962 | 10 | 50 | MISS ceiling | 4,225,806 | 353 | 0.075 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 36,658,953 | 733.179 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 36,657,946 | 733.159 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 17,276,706 | 345.534 | 10 | 20 | MISS ceiling | 3,439,901 | 291 | 0.068 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 3,507,175 | 70.143 | 10 | 200 | MISS T_svc | 4,237,339 | 390 | 0.058 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 19,176,169 | 383.523 | 10 | 200 | MISS ceiling | 3,439,901 | 291 | 0.068 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 3,507,631 | 70.153 | 10 | 20 | MISS ceiling | 4,237,339 | 390 | 0.058 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 21,173,975 | 423.479 | 10 | 20 | MISS ceiling | 3,439,901 | 291 | 0.068 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 3,509,423 | 70.188 | 10 | 24 | MISS ceiling | 4,237,339 | 390 | 0.058 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 44,276,229 | 885.525 | 10 | 24 | STARVED: never released | 0 | - | 0.000 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 3,508,903 | 70.178 | 10 | 50 | MISS ceiling | 4,237,339 | 390 | 0.058 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 13,798,999 | 275.980 | 10 | 50 | MISS ceiling | 4,026,726 | 346 | 0.075 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 44,275,969 | 885.519 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 44,274,962 | 885.499 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 26,247,827 | 524.957 | 10 | 20 | MISS ceiling | 1,579,572 | 163 | 0.064 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 27,827,225 | 556.544 | 10 | 20 | MISS ceiling | 1,579,436 | 163 | 0.064 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 29,406,756 | 588.135 | 10 | 20 | MISS ceiling | 1,579,568 | 163 | 0.064 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 31,145,081 | 622.902 | 10 | 20 | MISS ceiling | 1,738,363 | 169 | 0.067 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 32,724,618 | 654.492 | 10 | 20 | MISS ceiling | 1,579,574 | 163 | 0.064 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 3,283,964 | 65.679 | 10 | 200 | MISS T_svc | 2,966,905 | 340 | 0.078 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 14,575,849 | 291.517 | 10 | 200 | MISS ceiling | 3,653,220 | 322 | 0.085 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 3,281,835 | 65.637 | 10 | 20 | MISS ceiling | 2,966,905 | 340 | 0.078 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 20,476,050 | 409.521 | 10 | 20 | MISS ceiling | 2,954,391 | 235 | 0.076 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 3,283,627 | 65.673 | 10 | 24 | MISS ceiling | 2,966,905 | 340 | 0.078 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 37,601,789 | 752.036 | 10 | 24 | MISS ceiling | 1,442,918 | 141 | 0.064 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 3,283,107 | 65.662 | 10 | 50 | MISS ceiling | 2,966,905 | 340 | 0.078 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 14,575,101 | 291.502 | 10 | 50 | MISS ceiling | 3,653,220 | 322 | 0.085 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 39,271,417 | 785.428 | 10 | 18 | MISS ceiling | 1,669,888 | 48 | 0.120 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 43,000,448 | 860.009 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 2,049,894 | 40.998 | 10 | 20 | MISS ceiling | 2,666,792 | 92 (29) | 0.046 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 2,414,035 | 48.281 | 10 | 20 | MISS ceiling | 2,542,224 | 98 (35) | 0.044 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 1,043,394 | 20.868 | 10 | 20 | MISS ceiling | 2,192,085 | 89 (12) | 0.048 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 600,453 | 12.009 | 10 | 50 | MISS T_svc | 1,891,712 | 100 | 0.107 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 782,416 | 15.648 | 10 | 50 | MISS T_svc | 1,345,658 | 55 | 0.129 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 803,389 | 16.068 | 10 | 50 | MISS T_svc | 1,189,025 | 49 | 0.128 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 838,582 | 16.772 | 10 | 50 | MISS T_svc | 1,668,580 | 82 | 0.136 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 867,608 | 17.352 | 10 | 50 | MISS T_svc | 1,668,580 | 82 | 0.136 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 645,311 | 12.906 | 10 | 50 | MISS T_svc | 1,055,700 | 52 | 0.127 |
| LINK_UP | `adp.link_up.if0` | 177,343 | 3.547 | 10 | 200 | fits | 1,891,712 | 100 (11) | 0.107 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 302,363 | 6.047 | 10 | 200 | fits | 738,406 | 52 (39) | 0.091 |
| LINK_DOWN | `adp.link_down.if0` | 50,209 | 1.004 | 10 | 200 | fits | 1,226,739 | 22 (9) | 0.123 |
| LINK_UP | `adp.link_up.if0` | 177,343 | 3.547 | 10 | 200 | fits | 1,891,712 | 100 (11) | 0.107 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 302,363 | 6.047 | 10 | 200 | fits | 738,406 | 52 (39) | 0.091 |
| GM_CHANGE | `adp.gm_change.if0` | 59,103 | 1.182 | 10 | 200 | fits | 650,540 | 23 (11) | 0.103 |
| LINK_UP | `adp.link_up.if0` | 177,343 | 3.547 | 10 | 200 | fits | 1,891,712 | 100 (11) | 0.107 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 302,363 | 6.047 | 10 | 200 | fits | 738,406 | 52 (39) | 0.091 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 209,426 | 4.189 | 10 | 200 | fits | 789,624 | 43 (31) | 0.113 |
| LINK_UP | `adp.link_up.if0` | 177,343 | 3.547 | 10 | 200 | fits | 1,891,712 | 100 (11) | 0.107 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 302,363 | 6.047 | 10 | 200 | fits | 738,406 | 52 (39) | 0.091 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 209,426 | 4.189 | 10 | 200 | fits | 789,624 | 43 (31) | 0.113 |
| set_name | `aecp_fanout.set_name.if0` | 1,793,336 | 35.867 | 10 | 24 | MISS ceiling | 1,909,963 | 607 | 0.045 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 1,468,650 | 29.373 | 10 | 24 | MISS ceiling | 2,415,383 | 348 | 0.060 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 1,339,233 | 26.785 | 10 | 24 | MISS ceiling | 2,352,325 | 331 | 0.058 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 1,193,711 | 23.874 | 10 | 24 | MISS T_svc | 2,143,107 | 325 | 0.056 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 1,432,165 | 28.643 | 10 | 24 | MISS ceiling | 2,479,565 | 382 | 0.058 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 1,480,755 | 29.615 | 10 | 24 | MISS ceiling | 2,480,724 | 382 | 0.058 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 1,428,141 | 28.563 | 10 | 24 | MISS ceiling | 2,417,464 | 348 | 0.061 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 1,366,599 | 27.332 | 10 | 24 | MISS ceiling | 2,329,847 | 382 | 0.058 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 1,953,357 | 39.067 | 10 | 24 | MISS ceiling | 1,790,958 | 362 | 0.056 |
| BIND_RX | `acmp.bind_rx.if0` | 514,060 | 10.281 | 10 | 20 | MISS T_svc | 1,467,219 | 94 (77) | 0.094 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 474,289 | 9.486 | 10 | 20 | fits | 1,547,800 | 57 (32) | 0.071 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 1,789,937 | 35.799 | 10 | 20 | MISS ceiling | 2,738,113 | 110 (47) | 0.046 |
| UNBIND_RX | `acmp.unbind_rx.if0` | - | - | - | - | no end: missing ['resp:1:4102', 'tmr:1'] | - | - | - |
| PROBE_TX | `acmp.probe_tx.if0` | 707,812 | 14.156 | 10 | 20 | MISS T_svc | 3,043,009 | 155 (48) | 0.056 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 1,821,224 | 36.424 | 10 | 20 | MISS ceiling | 2,287,653 | 136 (48) | 0.060 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | - | - | - | - | no end: missing ['resp:1:4105'] | - | - | - |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 557,882 | 11.158 | 10 | 20 | MISS T_svc | 2,714,699 | 151 (48) | 0.052 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 593,503 | 11.870 | 10 | 24 | MISS T_svc | 1,162,352 | 58 | 0.085 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 935,142 | 18.703 | 10 | 24 | MISS T_svc | 1,142,600 | 130 | 0.055 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 1,193,331 | 23.867 | 10 | 24 | MISS T_svc | 1,235,161 | 84 | 0.065 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 1,038,643 | 20.773 | 10 | 24 | MISS T_svc | 1,239,427 | 95 | 0.064 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 1,166,127 | 23.323 | 10 | 24 | MISS T_svc | 1,078,357 | 88 | 0.058 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 1,036,581 | 20.732 | 10 | 24 | MISS T_svc | 1,078,515 | 88 | 0.058 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 1,192,735 | 23.855 | 10 | 24 | MISS T_svc | 1,234,691 | 83 | 0.065 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 1,118,398 | 22.368 | 10 | 24 | MISS T_svc | 1,927,803 | 122 | 0.069 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 1,186,310 | 23.726 | 10 | 24 | MISS T_svc | 1,564,751 | 90 | 0.074 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 1,055,426 | 21.109 | 10 | 24 | MISS T_svc | 1,110,977 | 165 | 0.049 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 1,184,215 | 23.684 | 10 | 24 | MISS T_svc | 1,226,400 | 63 | 0.068 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 1,025,744 | 20.515 | 10 | 24 | MISS T_svc | 1,226,630 | 63 | 0.068 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 1,616,881 | 32.338 | 10 | 24 | MISS ceiling | 1,817,767 | 114 | 0.082 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 1,035,172 | 20.703 | 10 | 24 | MISS T_svc | 1,077,161 | 80 | 0.058 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 1,031,883 | 20.638 | 10 | 24 | MISS T_svc | 1,073,896 | 72 | 0.059 |
| get_configuration | `aecp.get_configuration.if0` | 1,027,460 | 20.549 | 10 | 24 | MISS T_svc | 1,069,278 | 52 | 0.064 |
| entity_available | `aecp.entity_available.if0` | 1,093,205 | 21.864 | 10 | 24 | MISS T_svc | 1,134,795 | 56 | 0.068 |
| get_name | `aecp.get_name.if0` | 1,197,920 | 23.958 | 10 | 24 | MISS T_svc | 1,239,541 | 75 | 0.067 |
| get_counters | `aecp.get_counters.if0` | 1,046,554 | 20.931 | 10 | 24 | MISS T_svc | 1,247,264 | 91 | 0.066 |
| get_avb_info | `aecp.get_avb_info.if0` | 1,023,279 | 20.466 | 10 | 24 | MISS T_svc | 1,069,320 | 52 | 0.063 |
| unknown_command | `aecp.unknown_command.if0` | 1,004,874 | 20.097 | 10 | 24 | MISS T_svc | 1,042,507 | 52 | 0.062 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 934,541 | 18.691 | 10 | 24 | MISS T_svc | 976,296 | 56 | 0.077 |
| set_name | `aecp.set_name.if0` | 1,164,382 | 23.288 | 10 | 24 | MISS T_svc | 1,518,331 | 118 | 0.063 |
| lock_entity | `aecp.lock_entity.if0` | 1,338,867 | 26.777 | 10 | 24 | MISS ceiling | 1,299,427 | 77 | 0.069 |
| unlock_entity | `aecp.unlock_entity.if0` | 1,096,013 | 21.920 | 10 | 24 | MISS T_svc | 1,134,131 | 71 | 0.063 |
| LINK_UP | `fixture.link_up.if0` | 177,343 | 3.547 | 10 | 200 | fits | 1,891,712 | 100 (11) | 0.107 |
| malformed MRPDU discard | `fixture.malformed.if0` | 1,199,302 | 23.986 | 10 | 18 | MISS ceiling | 840,102 | 34 | 0.115 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | - | - | - | - | no end: no notification to ['0a0b0c0d0e0f0001@if0'] | - | - | - |
| LINK_DOWN | `fixture.link_down.if0` | 1,915,052 | 38.301 | 10 | 200 | MISS T_svc | 3,565,092 | 143 (9) | 0.103 |
| BIND_RX | `fixture.bind_rx.if0` | 1,542,305 | 30.846 | 10 | 20 | MISS ceiling | 3,565,092 | 143 (77) | 0.103 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 699,224 | 13.984 | 10 | 20 | MISS T_svc | 2,473,120 | 118 (35) | 0.051 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 2,052,508 | 41.050 | 10 | 20 | MISS ceiling | 2,500,798 | 92 (29) | 0.044 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 3,033,574 | 60.671 | 10 | 200 | MISS T_svc | 2,347,161 | 248 | 0.075 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 3,033,574 | 60.671 | 10 | 200 | MISS T_svc | 2,347,161 | 248 | 0.075 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 3,033,439 | 60.669 | 10 | 20 | MISS ceiling | 2,347,161 | 248 | 0.075 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 3,033,439 | 60.669 | 10 | 20 | MISS ceiling | 2,347,161 | 248 | 0.075 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 3,033,542 | 60.671 | 10 | 24 | MISS ceiling | 2,347,161 | 248 | 0.075 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 3,033,542 | 60.671 | 10 | 24 | MISS ceiling | 2,347,161 | 248 | 0.075 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 3,033,509 | 60.670 | 10 | 50 | MISS ceiling | 2,347,161 | 248 | 0.075 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 3,033,509 | 60.670 | 10 | 50 | MISS ceiling | 2,347,161 | 248 | 0.075 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 11,591,660 | 231.833 | 10 | 18 | MISS ceiling | 2,008,896 | 78 | 0.088 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 11,591,660 | 231.833 | 10 | 18 | MISS ceiling | 2,008,896 | 78 | 0.088 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `adp-advertise`: wait quiet TIMEOUT
- `adp-advertise`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog`: wait tx TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `backlog-owed`: wait tx TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `maap`: wait quiet TIMEOUT
- `maap`: wait quiet TIMEOUT
- `maap`: wait quiet TIMEOUT
- `adp-link`: wait quiet TIMEOUT
- `adp-link`: wait quiet TIMEOUT
- `adp-link`: wait quiet TIMEOUT
- `adp-gm`: wait quiet TIMEOUT
- `adp-gm`: wait quiet TIMEOUT
- `adp-gm`: wait quiet TIMEOUT
- `adp-discover`: wait quiet TIMEOUT
- `adp-discover`: wait quiet TIMEOUT
- `adp-discover`: wait quiet TIMEOUT
- `control`: wait quiet TIMEOUT
- `control`: wait quiet TIMEOUT
- `control`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait tx TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT
