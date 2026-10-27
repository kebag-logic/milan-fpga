### 1x1

16 of 81 paths and 41 of 141 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 1.326 (2.632) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 8.712 (15.611) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 4.873 (15.394) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 6.966 (13.648) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 8.956 (14.003) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 8.708 (15.608) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 8.738 (15.640) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 9.186 (14.086) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 11.650 (30.545) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.728 (13.519) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.537 (13.511) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 4.192 (26.595) | fits | 1 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 1.240 (11.535) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.777 (13.453) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.939 (11.478) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 8.900 (14.320) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.225 (1.134) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.074 (1.012) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.060 (3.133) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.075 (3.311) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.360 (1.287) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 1.094 (2.961) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.156 (2.922) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 2.179 (2.944) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.118 (2.883) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 2.724 (3.490) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 2.292 (3.058) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 2.135 (3.116) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 1.434 (2.199) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 2.892 (3.657) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 2.382 (3.148) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 2.647 (3.413) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.316 (3.082) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.227 (3.993) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 2.194 (2.960) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 2.493 (3.258) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 2.787 (3.553) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 2.397 (3.163) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 2.450 (3.216) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.675 (3.440) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 2.482 (3.248) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 2.485 (3.251) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 2.381 (3.146) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.721 (2.481) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 2.688 (4.020) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.114 (2.879) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 2.439 (3.420) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 5.299 (6.105) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 5.043 (5.820) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 5.309 (6.117) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 4.975 (5.587) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 5.194 (5.971) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 7.061 (8.100) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 4.921 (5.513) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 5.055 (5.833) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 38.133 (42.327) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 39.098 (51.347) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 35.298 (54.536) | MISS ceiling | 2 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 9.445 (17.695) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 95.805 (98.536) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 362.513 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 2.959 (4.034) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.806 (2.701) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.480 (1.367) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.554 (3.311) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.638 (2.701) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 1.028 (2.897) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp.service.acmp.first.if0` (backlog-adp) | 10.198 | MISS T_svc | 0 acmp | 5 | 2 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 82.580 | MISS ceiling | 11 acmp | 5 | 4 |
| ADP record released under the composed load, first | 0 | `backlog-adp.service.adp.first.if0` (backlog-adp) | 10.189 | MISS T_svc | 0 adp | 5 | 2 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 46.861 | MISS T_svc | 7 adp | 5 | 4 |
| AECP record released under the composed load, first | 0 | `backlog-adp.service.aecp.first.if0` (backlog-adp) | 10.234 | MISS T_svc | 0 aecp | 5 | 2 |
| AECP record released under the composed load, last | 0 | `backlog-adp-refill.service.aecp.last.if0` (backlog-adp-refill) | 249.937 | MISS ceiling | 15 aecp | 5 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog-adp.service.maap.first.if0` (backlog-adp) | 10.224 | MISS T_svc | 0 maap | 5 | 2 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 46.898 | MISS T_svc | 6 maap | 5 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 575.283 | STARVED: never released | 0 srp | 5 | 4 |
| SRP record released under the composed load, last | 0 | `backlog-adp-refill.service.srp.last.if0` (backlog-adp-refill) | at least 575.263 | STARVED: never released | 31 srp | 5 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 3.345 (4.783) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 1.911 (1.912) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 1.233 (1.234) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 2.927 (3.311) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 91.207 | 21 | 449,585 (8.992) | yes | - |
| backlog-adp | 539.151 | 36 | 941,231 (18.825) | no | {'srp': 32} |
| backlog-adp-refill | 575.300 | 39 | 919,246 (18.385) | no | {'srp': 32} |
| backlog-owed | 362.564 | 52 | 437,129 (8.743) | yes | - |
| fixture | 10.189 | 3 | 300,401 (6.008) | yes | - |

Composed maximum over the 4 backlog windows: at least 941,231 CPU cycles (18.825 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 449,585 (8.992 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 38,826 | 0.777 | 10 | 20 | fits | 672,653 | 77 (14) | 0.038 |
| LINK_UP | `adp.link_up.if0` | 3,733 | 0.075 | 10 | 200 | fits | 165,536 | 88 (11) | 0.117 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 54,699 | 1.094 | 10 | 200 | fits | 67,484 | 46 (39) | 0.110 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 17,987 | 0.360 | 10 | 200 | fits | 3,671 | 9 (11) | 0.172 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 209,581 | 4.192 | 10 | 20 | fits | 590,776 | 95 (35) | 0.042 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 61,990 | 1.240 | 10 | 20 | fits | 576,730 | 72 (14) | 0.040 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 46,956 | 0.939 | 10 | 20 | fits | 573,885 | 73 (14) | 0.040 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 36,408 | 0.728 | 10 | 20 | fits | 675,963 | 98 (35) | 0.038 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 146,330 | 2.927 | 10 | 18 | fits | 165,536 | 88 | 0.117 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 95,565 | 1.911 | 10 | 18 | fits | 95,597 | 29 | 0.120 |
| malformed MRPDU discard | `srp.malformed.if0` | 61,649 | 1.233 | 10 | 18 | fits | 61,681 | 28 | 0.112 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 167,251 | 3.345 | 210 | 218 | fits | 239,127 | 78 | 0.113 |
| an event behind 15 others | `backlog.event.if0` | 472,262 | 9.445 | 10 | 200 | fits | 435,163 | 355 | 0.095 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 1,906,666 | 38.133 | 10 | 20 | MISS ceiling | 294,365 | 255 | 0.089 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 449,481 | 8.990 | 10 | 200 | fits | 449,585 | 388 | 0.096 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 1,527,106 | 30.542 | 10 | 200 | MISS T_svc | 294,114 | 278 | 0.089 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 447,352 | 8.947 | 10 | 20 | fits | 449,585 | 388 | 0.096 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 2,113,689 | 42.274 | 10 | 20 | MISS ceiling | 294,365 | 255 | 0.089 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 449,144 | 8.983 | 10 | 24 | fits | 449,585 | 388 | 0.096 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 4,114,983 | 82.300 | 10 | 24 | MISS ceiling | 211,764 | 168 | 0.083 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 448,624 | 8.972 | 10 | 50 | fits | 449,585 | 388 | 0.096 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 1,526,358 | 30.527 | 10 | 50 | MISS T_svc | 294,114 | 278 | 0.089 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 1,232,212 | 24.644 | 10 | 18 | MISS ceiling | 348,652 | 347 | 0.098 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 4,423,061 | 88.461 | 10 | 18 | MISS ceiling | 58,096 | 47 | 0.112 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 1,954,920 | 39.098 | 10 | 20 | MISS ceiling | 941,231 | 368 | 0.053 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 509,462 | 10.189 | 10 | 200 | MISS T_svc | 733,434 | 393 | 0.060 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,343,075 | 46.861 | 10 | 200 | MISS T_svc | 941,231 | 368 | 0.053 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 509,918 | 10.198 | 10 | 20 | MISS T_svc | 733,434 | 393 | 0.060 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 4,102,326 | 82.047 | 10 | 20 | MISS ceiling | 879,531 | 274 | 0.047 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 511,710 | 10.234 | 10 | 24 | MISS T_svc | 733,434 | 393 | 0.060 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 12,469,929 | 249.399 | 10 | 24 | MISS ceiling | 889,938 | 230 | 0.048 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 511,190 | 10.224 | 10 | 50 | MISS T_svc | 733,434 | 393 | 0.060 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,344,913 | 46.898 | 10 | 50 | MISS T_svc | 941,231 | 368 | 0.053 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 26,956,725 | 539.135 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 26,955,718 | 539.114 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 1,764,905 | 35.298 | 10 | 20 | MISS ceiling | 910,447 | 306 | 0.050 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 509,462 | 10.189 | 10 | 200 | MISS T_svc | 733,434 | 393 | 0.060 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 2,131,187 | 42.624 | 10 | 200 | MISS T_svc | 910,447 | 306 | 0.050 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 509,918 | 10.198 | 10 | 20 | MISS T_svc | 733,434 | 393 | 0.060 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 4,128,993 | 82.580 | 10 | 20 | MISS ceiling | 910,447 | 306 | 0.050 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 511,710 | 10.234 | 10 | 24 | MISS T_svc | 733,434 | 393 | 0.060 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 12,496,858 | 249.937 | 10 | 24 | MISS ceiling | 876,666 | 190 | 0.037 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 511,190 | 10.224 | 10 | 50 | MISS T_svc | 733,434 | 393 | 0.060 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,322,928 | 46.459 | 10 | 50 | MISS T_svc | 919,246 | 361 | 0.051 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 28,764,168 | 575.283 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 28,763,161 | 575.263 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 4,790,230 | 95.805 | 10 | 20 | MISS ceiling | 204,738 | 146 | 0.076 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,125,658 | 362.513 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,125,620 | 362.512 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,125,583 | 362.512 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,125,545 | 362.511 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 385,456 | 7.709 | 10 | 200 | fits | 341,751 | 340 | 0.092 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 1,490,464 | 29.809 | 10 | 200 | MISS T_svc | 349,161 | 280 | 0.093 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 383,327 | 7.667 | 10 | 20 | fits | 341,751 | 340 | 0.092 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 1,979,356 | 39.587 | 10 | 20 | MISS ceiling | 179,234 | 74 | 0.070 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 385,119 | 7.702 | 10 | 24 | fits | 341,751 | 340 | 0.092 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 5,455,754 | 109.115 | 10 | 24 | MISS ceiling | 185,756 | 124 | 0.072 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 384,599 | 7.692 | 10 | 50 | fits | 341,751 | 340 | 0.092 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 1,489,716 | 29.794 | 10 | 50 | MISS T_svc | 349,161 | 280 | 0.093 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 821,501 | 16.430 | 10 | 18 | MISS T_svc | 437,129 | 377 | 0.103 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 4,250,107 | 85.002 | 10 | 18 | MISS ceiling | 291,335 | 190 | 0.097 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 345,345 | 6.907 | 10 | 20 | fits | 768,307 | 101 (29) | 0.036 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 243,653 | 4.873 | 10 | 20 | fits | 769,689 | 107 (35) | 0.036 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 26,874 | 0.537 | 10 | 20 | fits | 675,565 | 98 (12) | 0.038 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 27,709 | 0.554 | 10 | 50 | fits | 165,536 | 88 | 0.117 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 51,386 | 1.028 | 10 | 50 | fits | 69,176 | 37 | 0.115 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 44,307 | 0.886 | 10 | 50 | fits | 84,136 | 43 | 0.121 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 31,911 | 0.638 | 10 | 50 | fits | 87,692 | 64 | 0.113 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 40,290 | 0.806 | 10 | 50 | fits | 87,692 | 64 | 0.113 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 23,988 | 0.480 | 10 | 50 | fits | 68,346 | 46 | 0.113 |
| LINK_UP | `adp.link_up.if0` | 3,733 | 0.075 | 10 | 200 | fits | 165,536 | 88 (11) | 0.117 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 54,699 | 1.094 | 10 | 200 | fits | 67,484 | 46 (39) | 0.110 |
| LINK_DOWN | `adp.link_down.if0` | 2,994 | 0.060 | 10 | 200 | fits | 156,668 | 27 (9) | 0.100 |
| LINK_UP | `adp.link_up.if0` | 3,733 | 0.075 | 10 | 200 | fits | 165,536 | 88 (11) | 0.117 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 54,699 | 1.094 | 10 | 200 | fits | 67,484 | 46 (39) | 0.110 |
| GM_CHANGE | `adp.gm_change.if0` | 3,724 | 0.074 | 10 | 200 | fits | 50,588 | 18 (11) | 0.107 |
| LINK_UP | `adp.link_up.if0` | 3,733 | 0.075 | 10 | 200 | fits | 165,536 | 88 (11) | 0.117 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 54,699 | 1.094 | 10 | 200 | fits | 67,484 | 46 (39) | 0.110 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 11,248 | 0.225 | 10 | 200 | fits | 56,703 | 38 (31) | 0.108 |
| LINK_UP | `adp.link_up.if0` | 3,733 | 0.075 | 10 | 200 | fits | 165,536 | 88 (11) | 0.117 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 54,699 | 1.094 | 10 | 200 | fits | 67,484 | 46 (39) | 0.110 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 11,248 | 0.225 | 10 | 200 | fits | 56,703 | 38 (31) | 0.108 |
| set_name | `aecp_fanout.set_name.if0` | 353,072 | 7.061 | 10 | 24 | fits | 404,989 | 602 | 0.122 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 248,752 | 4.975 | 10 | 24 | fits | 279,346 | 317 | 0.121 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 259,711 | 5.194 | 10 | 24 | fits | 298,537 | 336 | 0.116 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 239,214 | 4.784 | 10 | 24 | fits | 278,086 | 299 | 0.116 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 265,463 | 5.309 | 10 | 24 | fits | 305,849 | 350 | 0.117 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 264,931 | 5.299 | 10 | 24 | fits | 305,253 | 351 | 0.115 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 246,059 | 4.921 | 10 | 24 | fits | 275,673 | 317 | 0.122 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 252,144 | 5.043 | 10 | 24 | fits | 290,990 | 351 | 0.118 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 252,766 | 5.055 | 10 | 24 | fits | 291,638 | 351 | 0.119 |
| BIND_RX | `acmp.bind_rx.if0` | 66,247 | 1.325 | 10 | 20 | fits | 141,255 | 89 (77) | 0.110 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 582,487 | 11.650 | 10 | 20 | MISS T_svc | 691,714 | 101 (32) | 0.040 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 447,819 | 8.956 | 10 | 20 | fits | 700,167 | 116 (47) | 0.041 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 445,002 | 8.900 | 10 | 20 | fits | 715,985 | 119 (50) | 0.043 |
| PROBE_TX | `acmp.probe_tx.if0` | 459,288 | 9.186 | 10 | 20 | fits | 704,291 | 149 (48) | 0.041 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 436,910 | 8.738 | 10 | 20 | fits | 782,005 | 120 (48) | 0.037 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 435,585 | 8.712 | 10 | 20 | fits | 780,564 | 120 (48) | 0.037 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 435,389 | 8.708 | 10 | 20 | fits | 780,414 | 120 (48) | 0.036 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 86,073 | 1.721 | 10 | 24 | fits | 124,031 | 53 | 0.090 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 144,586 | 2.892 | 10 | 24 | fits | 182,872 | 125 | 0.073 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 119,110 | 2.382 | 10 | 24 | fits | 157,393 | 73 | 0.068 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 139,349 | 2.787 | 10 | 24 | fits | 177,632 | 90 | 0.075 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 124,124 | 2.482 | 10 | 24 | fits | 162,410 | 83 | 0.069 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 124,252 | 2.485 | 10 | 24 | fits | 162,538 | 83 | 0.069 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 119,038 | 2.381 | 10 | 24 | fits | 157,324 | 72 | 0.068 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 132,371 | 2.647 | 10 | 24 | fits | 170,657 | 74 | 0.074 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 115,795 | 2.316 | 10 | 24 | fits | 154,078 | 65 | 0.067 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 161,364 | 3.227 | 10 | 24 | fits | 199,647 | 160 | 0.075 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 109,696 | 2.194 | 10 | 24 | fits | 147,979 | 52 | 0.065 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 124,637 | 2.493 | 10 | 24 | fits | 162,920 | 58 | 0.072 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 119,865 | 2.397 | 10 | 24 | fits | 158,148 | 69 | 0.066 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 122,514 | 2.450 | 10 | 24 | fits | 160,797 | 75 | 0.067 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 133,736 | 2.675 | 10 | 24 | fits | 172,019 | 73 | 0.073 |
| get_configuration | `aecp.get_configuration.if0` | 105,876 | 2.118 | 10 | 24 | fits | 144,159 | 47 | 0.065 |
| entity_available | `aecp.entity_available.if0` | 107,824 | 2.156 | 10 | 24 | fits | 146,110 | 51 | 0.065 |
| get_name | `aecp.get_name.if0` | 114,607 | 2.292 | 10 | 24 | fits | 152,893 | 64 | 0.067 |
| get_counters | `aecp.get_counters.if0` | 136,191 | 2.724 | 10 | 24 | fits | 174,477 | 86 | 0.077 |
| get_avb_info | `aecp.get_avb_info.if0` | 108,930 | 2.179 | 10 | 24 | fits | 147,216 | 47 | 0.064 |
| unknown_command | `aecp.unknown_command.if0` | 105,682 | 2.114 | 10 | 24 | fits | 143,968 | 47 | 0.064 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 71,680 | 1.434 | 10 | 24 | fits | 109,966 | 50 | 0.083 |
| set_name | `aecp.set_name.if0` | 134,390 | 2.688 | 10 | 24 | fits | 200,983 | 107 | 0.072 |
| lock_entity | `aecp.lock_entity.if0` | 106,734 | 2.135 | 10 | 24 | fits | 155,776 | 66 | 0.069 |
| unlock_entity | `aecp.unlock_entity.if0` | 121,974 | 2.439 | 10 | 24 | fits | 170,996 | 72 | 0.075 |
| LINK_UP | `fixture.link_up.if0` | 3,733 | 0.075 | 10 | 200 | fits | 165,536 | 88 (11) | 0.117 |
| malformed MRPDU discard | `fixture.malformed.if0` | 59,028 | 1.181 | 10 | 18 | fits | 59,060 | 29 | 0.118 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 147,974 | 2.959 | 10 | 24 | fits | 201,700 | 107 | 0.071 |
| LINK_DOWN | `fixture.link_down.if0` | 2,994 | 0.060 | 10 | 200 | fits | 158,827 | 27 (9) | 0.099 |
| BIND_RX | `fixture.bind_rx.if0` | 66,314 | 1.326 | 10 | 20 | fits | 131,598 | 89 (77) | 0.109 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 176,641 | 3.533 | 10 | 20 | fits | 699,102 | 127 (35) | 0.040 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 348,324 | 6.966 | 10 | 20 | fits | 682,400 | 98 (29) | 0.039 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 300,350 | 6.007 | 10 | 200 | fits | 300,401 | 244 | 0.097 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 300,350 | 6.007 | 10 | 200 | fits | 300,401 | 244 | 0.097 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 300,215 | 6.004 | 10 | 20 | fits | 300,401 | 244 | 0.097 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 300,215 | 6.004 | 10 | 20 | fits | 300,401 | 244 | 0.097 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 300,317 | 6.006 | 10 | 24 | fits | 300,401 | 244 | 0.097 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 300,317 | 6.006 | 10 | 24 | fits | 300,401 | 244 | 0.097 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 300,285 | 6.006 | 10 | 50 | fits | 300,401 | 244 | 0.097 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 300,285 | 6.006 | 10 | 50 | fits | 300,401 | 244 | 0.097 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 300,252 | 6.005 | 10 | 18 | fits | 300,401 | 244 | 0.097 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 300,252 | 6.005 | 10 | 18 | fits | 300,401 | 244 | 0.097 |

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
