head ad2ed0e3ab3daa9697bdf42ae504b4504bfd04aa
command: results/table.md
full log: 30300 bytes, sha256 42d66786bbc25a23c1791262a4cb2c53a28afa0ba72d2b1f3f3fbecc05c3e145
---
### 1x1

13 of 81 paths and 34 of 141 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.983 (2.492) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 9.418 (14.248) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 8.723 (14.041) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 15.328 (30.841) | MISS T_svc | 0 adp | 2 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 9.645 (16.045) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 9.415 (14.248) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 9.454 (14.279) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 8.134 (14.384) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 12.514 (15.891) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.981 (13.849) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 2.134 (13.848) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 1.339 (14.309) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.700 (13.572) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 1.990 (12.078) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.748 (11.795) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 9.599 (16.346) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.224 (1.144) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.077 (1.022) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.065 (3.101) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.077 (3.241) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.786 (1.718) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.944 (2.831) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.141 (2.923) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 2.162 (2.944) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.104 (2.886) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 2.392 (3.173) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 2.261 (3.043) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 2.266 (3.230) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 1.735 (2.517) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 2.797 (3.579) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 2.344 (3.125) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 2.621 (3.403) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.284 (3.066) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.106 (3.888) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 2.175 (2.956) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 2.483 (3.264) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 2.437 (3.219) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 2.362 (3.144) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 2.409 (3.191) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.651 (3.433) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 2.741 (3.523) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 2.437 (3.218) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 2.343 (3.124) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.413 (2.187) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 2.756 (4.144) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.099 (2.881) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 2.578 (3.543) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 4.730 (5.543) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 4.610 (5.395) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 4.750 (5.565) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 4.544 (5.164) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 4.377 (5.163) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 6.350 (7.482) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 4.386 (4.986) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 4.616 (5.402) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 37.281 (41.386) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 42.055 (53.150) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 38.615 (55.069) | MISS ceiling | 4 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 9.348 (17.383) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 93.481 (96.134) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 362.726 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 2.989 (4.159) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 1.593 (3.504) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.458 (1.359) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.531 (3.241) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 1.443 (3.504) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 1.054 (2.615) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp.service.acmp.first.if0` (backlog-adp) | 9.065 | fits | 0 acmp | 5 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 85.791 | MISS ceiling | 11 acmp | 5 | 4 |
| ADP record released under the composed load, first | 0 | `backlog-adp.service.adp.first.if0` (backlog-adp) | 9.056 | fits | 0 adp | 5 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 49.690 | MISS T_svc | 7 adp | 5 | 4 |
| AECP record released under the composed load, first | 0 | `backlog-adp.service.aecp.first.if0` (backlog-adp) | 9.101 | fits | 0 aecp | 5 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp-refill.service.aecp.last.if0` (backlog-adp-refill) | 254.111 | MISS ceiling | 15 aecp | 5 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog-adp.service.maap.first.if0` (backlog-adp) | 9.090 | fits | 0 maap | 5 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 49.726 | MISS T_svc | 6 maap | 5 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 578.600 | STARVED: never released | 0 srp | 5 | 4 |
| SRP record released under the composed load, last | 0 | `backlog-adp-refill.service.srp.last.if0` (backlog-adp-refill) | at least 578.580 | STARVED: never released | 31 srp | 5 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 3.252 (4.654) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 1.904 (1.905) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 1.582 (1.583) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 2.867 (3.241) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 90.376 | 22 | 440,878 (8.818) | yes | - |
| backlog-adp | 542.108 | 36 | 985,830 (19.717) | no | {'srp': 32} |
| backlog-adp-refill | 578.617 | 38 | 985,706 (19.714) | no | {'srp': 32} |
| backlog-owed | 362.776 | 52 | 431,583 (8.632) | yes | - |
| fixture | 10.110 | 3 | 294,748 (5.895) | yes | - |

Composed maximum over the 4 backlog windows: at least 985,830 CPU cycles (19.717 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 440,878 (8.818 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 99,515 | 1.990 | 10 | 20 | fits | 603,923 | 109 (14) | 0.040 |
| LINK_UP | `adp.link_up.if0` | 3,868 | 0.077 | 10 | 200 | fits | 162,047 | 88 (11) | 0.091 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 47,209 | 0.944 | 10 | 200 | fits | 66,717 | 46 (39) | 0.087 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 39,303 | 0.786 | 10 | 200 | fits | 3,893 | 9 (11) | 0.164 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 33,075 | 0.661 | 10 | 20 | fits | 692,072 | 140 (35) | 0.035 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 35,014 | 0.700 | 10 | 20 | fits | 678,596 | 117 (14) | 0.034 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 37,422 | 0.748 | 10 | 20 | fits | 589,757 | 108 (14) | 0.038 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 49,057 | 0.981 | 10 | 20 | fits | 692,437 | 140 (35) | 0.035 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 143,329 | 2.867 | 10 | 18 | fits | 162,047 | 88 | 0.091 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 95,198 | 1.904 | 10 | 18 | fits | 95,230 | 29 | 0.112 |
| malformed MRPDU discard | `srp.malformed.if0` | 79,124 | 1.582 | 10 | 18 | fits | 79,156 | 35 | 0.113 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 162,581 | 3.252 | 210 | 218 | fits | 232,703 | 78 | 0.090 |
| an event behind 15 others | `backlog.event.if0` | 467,411 | 9.348 | 10 | 200 | fits | 428,273 | 356 | 0.073 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 1,864,062 | 37.281 | 10 | 20 | MISS ceiling | 287,170 | 256 | 0.063 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 440,774 | 8.815 | 10 | 200 | fits | 440,878 | 389 | 0.071 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 1,523,424 | 30.468 | 10 | 200 | MISS T_svc | 314,879 | 324 | 0.070 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 438,645 | 8.773 | 10 | 20 | fits | 440,878 | 389 | 0.071 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 2,066,669 | 41.333 | 10 | 20 | MISS ceiling | 287,170 | 256 | 0.063 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 440,437 | 8.809 | 10 | 24 | fits | 440,878 | 389 | 0.071 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 4,013,984 | 80.280 | 10 | 24 | MISS ceiling | 207,974 | 169 | 0.059 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 439,917 | 8.798 | 10 | 50 | fits | 440,878 | 389 | 0.071 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 1,522,676 | 30.454 | 10 | 50 | MISS T_svc | 314,879 | 324 | 0.070 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 1,207,765 | 24.155 | 10 | 18 | MISS ceiling | 339,802 | 348 | 0.073 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 4,380,734 | 87.615 | 10 | 18 | MISS ceiling | 58,085 | 47 | 0.102 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 2,102,760 | 42.055 | 10 | 20 | MISS ceiling | 948,693 | 411 | 0.042 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 452,796 | 9.056 | 10 | 200 | fits | 625,498 | 412 | 0.049 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,484,477 | 49.690 | 10 | 200 | MISS T_svc | 948,693 | 411 | 0.042 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 453,252 | 9.065 | 10 | 20 | fits | 625,498 | 412 | 0.049 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 4,263,703 | 85.274 | 10 | 20 | MISS ceiling | 889,465 | 317 | 0.038 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 455,044 | 9.101 | 10 | 24 | fits | 625,498 | 412 | 0.049 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 12,679,103 | 253.582 | 10 | 24 | MISS ceiling | 805,448 | 230 | 0.033 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 454,524 | 9.090 | 10 | 50 | fits | 625,498 | 412 | 0.049 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,486,315 | 49.726 | 10 | 50 | MISS T_svc | 948,693 | 411 | 0.042 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 27,104,565 | 542.091 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 27,103,558 | 542.071 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 1,930,747 | 38.615 | 10 | 20 | MISS ceiling | 919,254 | 349 | 0.040 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 452,796 | 9.056 | 10 | 200 | fits | 625,498 | 412 | 0.049 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 2,291,761 | 45.835 | 10 | 200 | MISS T_svc | 919,254 | 349 | 0.040 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 453,252 | 9.065 | 10 | 20 | fits | 625,498 | 412 | 0.049 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 4,289,567 | 85.791 | 10 | 20 | MISS ceiling | 919,254 | 349 | 0.040 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 455,044 | 9.101 | 10 | 24 | fits | 625,498 | 412 | 0.049 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 12,705,552 | 254.111 | 10 | 24 | MISS ceiling | 805,455 | 230 | 0.033 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 454,524 | 9.090 | 10 | 50 | fits | 625,498 | 412 | 0.049 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,465,195 | 49.304 | 10 | 50 | MISS T_svc | 927,573 | 404 | 0.041 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 28,930,010 | 578.600 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 28,929,003 | 578.580 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 4,674,061 | 93.481 | 10 | 20 | MISS ceiling | 199,752 | 147 | 0.049 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,136,287 | 362.726 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,136,249 | 362.725 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,136,212 | 362.724 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,136,174 | 362.723 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 350,430 | 7.009 | 10 | 200 | fits | 337,732 | 341 | 0.071 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 1,468,992 | 29.380 | 10 | 200 | MISS T_svc | 290,600 | 255 | 0.063 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 348,301 | 6.966 | 10 | 20 | fits | 337,732 | 341 | 0.071 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 1,951,139 | 39.023 | 10 | 20 | MISS ceiling | 178,846 | 75 | 0.064 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 350,093 | 7.002 | 10 | 24 | fits | 337,732 | 341 | 0.071 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 5,323,916 | 106.478 | 10 | 24 | MISS ceiling | 181,878 | 125 | 0.047 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 349,573 | 6.991 | 10 | 50 | fits | 337,732 | 341 | 0.071 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 1,468,244 | 29.365 | 10 | 50 | MISS T_svc | 290,600 | 255 | 0.063 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 780,929 | 15.619 | 10 | 18 | MISS T_svc | 431,583 | 378 | 0.084 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 4,144,248 | 82.885 | 10 | 18 | MISS ceiling | 251,708 | 173 | 0.068 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 320,792 | 6.416 | 10 | 20 | fits | 700,274 | 140 (29) | 0.036 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 436,131 | 8.723 | 10 | 20 | fits | 702,040 | 146 (35) | 0.037 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 106,677 | 2.134 | 10 | 20 | fits | 692,392 | 140 (12) | 0.035 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 26,555 | 0.531 | 10 | 50 | fits | 162,047 | 88 | 0.091 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 24,096 | 0.482 | 10 | 50 | fits | 69,040 | 37 | 0.097 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 52,704 | 1.054 | 10 | 50 | fits | 68,849 | 37 | 0.098 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 72,157 | 1.443 | 10 | 50 | fits | 86,099 | 64 | 0.085 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 79,628 | 1.593 | 10 | 50 | fits | 86,099 | 64 | 0.085 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 22,892 | 0.458 | 10 | 50 | fits | 67,928 | 47 | 0.096 |
| LINK_UP | `adp.link_up.if0` | 3,868 | 0.077 | 10 | 200 | fits | 162,047 | 88 (11) | 0.091 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 47,209 | 0.944 | 10 | 200 | fits | 66,717 | 46 (39) | 0.087 |
| LINK_DOWN | `adp.link_down.if0` | 3,244 | 0.065 | 10 | 200 | fits | 155,058 | 27 (9) | 0.086 |
| LINK_UP | `adp.link_up.if0` | 3,868 | 0.077 | 10 | 200 | fits | 162,047 | 88 (11) | 0.091 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 47,209 | 0.944 | 10 | 200 | fits | 66,717 | 46 (39) | 0.087 |
| GM_CHANGE | `adp.gm_change.if0` | 3,836 | 0.077 | 10 | 200 | fits | 51,101 | 18 (11) | 0.097 |
| LINK_UP | `adp.link_up.if0` | 3,868 | 0.077 | 10 | 200 | fits | 162,047 | 88 (11) | 0.091 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 47,209 | 0.944 | 10 | 200 | fits | 66,717 | 46 (39) | 0.087 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 11,214 | 0.224 | 10 | 200 | fits | 57,193 | 38 (31) | 0.104 |
| LINK_UP | `adp.link_up.if0` | 3,868 | 0.077 | 10 | 200 | fits | 162,047 | 88 (11) | 0.091 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 47,209 | 0.944 | 10 | 200 | fits | 66,717 | 46 (39) | 0.087 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 11,214 | 0.224 | 10 | 200 | fits | 57,193 | 38 (31) | 0.104 |
| set_name | `aecp_fanout.set_name.if0` | 317,503 | 6.350 | 10 | 24 | fits | 374,083 | 622 | 0.035 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 227,212 | 4.544 | 10 | 24 | fits | 258,213 | 329 | 0.043 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 218,492 | 4.370 | 10 | 24 | fits | 257,726 | 312 | 0.039 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 218,860 | 4.377 | 10 | 24 | fits | 258,137 | 312 | 0.039 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 237,500 | 4.750 | 10 | 24 | fits | 278,258 | 352 | 0.041 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 236,518 | 4.730 | 10 | 24 | fits | 277,152 | 352 | 0.039 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 219,308 | 4.386 | 10 | 24 | fits | 249,294 | 318 | 0.042 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 230,499 | 4.610 | 10 | 24 | fits | 269,755 | 363 | 0.037 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 230,822 | 4.616 | 10 | 24 | fits | 270,099 | 363 | 0.037 |
| BIND_RX | `acmp.bind_rx.if0` | 49,171 | 0.983 | 10 | 20 | fits | 124,592 | 83 (77) | 0.087 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 625,690 | 12.514 | 10 | 20 | MISS T_svc | 794,534 | 153 (32) | 0.034 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 482,229 | 9.645 | 10 | 20 | fits | 802,261 | 168 (47) | 0.034 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 479,952 | 9.599 | 10 | 20 | fits | 817,323 | 171 (50) | 0.036 |
| PROBE_TX | `acmp.probe_tx.if0` | 406,699 | 8.134 | 10 | 20 | fits | 719,213 | 191 (48) | 0.037 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 472,723 | 9.454 | 10 | 20 | fits | 713,928 | 159 (48) | 0.037 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 470,889 | 9.418 | 10 | 20 | fits | 712,420 | 159 (48) | 0.037 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 470,752 | 9.415 | 10 | 20 | fits | 712,376 | 159 (48) | 0.037 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 70,667 | 1.413 | 10 | 24 | fits | 109,357 | 48 | 0.073 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 139,834 | 2.797 | 10 | 24 | fits | 178,926 | 125 | 0.048 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 117,177 | 2.344 | 10 | 24 | fits | 156,266 | 74 | 0.054 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 121,847 | 2.437 | 10 | 24 | fits | 160,936 | 85 | 0.052 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 137,051 | 2.741 | 10 | 24 | fits | 176,143 | 90 | 0.059 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 121,826 | 2.437 | 10 | 24 | fits | 160,918 | 84 | 0.052 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 117,129 | 2.343 | 10 | 24 | fits | 156,221 | 73 | 0.054 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 131,067 | 2.621 | 10 | 24 | fits | 170,159 | 75 | 0.061 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 114,215 | 2.284 | 10 | 24 | fits | 153,304 | 66 | 0.055 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 155,319 | 3.106 | 10 | 24 | fits | 194,408 | 161 | 0.044 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 108,727 | 2.175 | 10 | 24 | fits | 147,816 | 53 | 0.057 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 124,131 | 2.483 | 10 | 24 | fits | 163,220 | 59 | 0.064 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 118,097 | 2.362 | 10 | 24 | fits | 157,186 | 70 | 0.053 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 120,464 | 2.409 | 10 | 24 | fits | 159,553 | 76 | 0.053 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 132,570 | 2.651 | 10 | 24 | fits | 171,659 | 74 | 0.061 |
| get_configuration | `aecp.get_configuration.if0` | 105,188 | 2.104 | 10 | 24 | fits | 144,277 | 48 | 0.057 |
| entity_available | `aecp.entity_available.if0` | 107,038 | 2.141 | 10 | 24 | fits | 146,130 | 52 | 0.057 |
| get_name | `aecp.get_name.if0` | 113,056 | 2.261 | 10 | 24 | fits | 152,148 | 65 | 0.056 |
| get_counters | `aecp.get_counters.if0` | 119,582 | 2.392 | 10 | 24 | fits | 158,674 | 85 | 0.056 |
| get_avb_info | `aecp.get_avb_info.if0` | 108,114 | 2.162 | 10 | 24 | fits | 147,206 | 48 | 0.057 |
| unknown_command | `aecp.unknown_command.if0` | 104,973 | 2.099 | 10 | 24 | fits | 144,065 | 48 | 0.057 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 86,759 | 1.735 | 10 | 24 | fits | 125,851 | 58 | 0.081 |
| set_name | `aecp.set_name.if0` | 137,804 | 2.756 | 10 | 24 | fits | 207,204 | 128 | 0.056 |
| lock_entity | `aecp.lock_entity.if0` | 113,286 | 2.266 | 10 | 24 | fits | 161,524 | 78 | 0.058 |
| unlock_entity | `aecp.unlock_entity.if0` | 128,920 | 2.578 | 10 | 24 | fits | 177,136 | 84 | 0.065 |
| LINK_UP | `fixture.link_up.if0` | 3,868 | 0.077 | 10 | 200 | fits | 162,047 | 88 (11) | 0.091 |
| malformed MRPDU discard | `fixture.malformed.if0` | 59,036 | 1.181 | 10 | 18 | fits | 59,068 | 29 | 0.110 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 149,467 | 2.989 | 10 | 24 | fits | 207,962 | 128 | 0.056 |
| LINK_DOWN | `fixture.link_down.if0` | 3,244 | 0.065 | 10 | 200 | fits | 157,196 | 27 (9) | 0.085 |
| BIND_RX | `fixture.bind_rx.if0` | 49,131 | 0.983 | 10 | 20 | fits | 114,666 | 83 (77) | 0.084 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 66,955 | 1.339 | 10 | 20 | fits | 715,450 | 169 (35) | 0.037 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 766,408 | 15.328 | 10 | 20 | MISS T_svc | 785,235 | 150 (29) | 0.033 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 294,697 | 5.894 | 10 | 200 | fits | 294,748 | 245 | 0.076 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 294,697 | 5.894 | 10 | 200 | fits | 294,748 | 245 | 0.076 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 294,562 | 5.891 | 10 | 20 | fits | 294,748 | 245 | 0.076 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 294,562 | 5.891 | 10 | 20 | fits | 294,748 | 245 | 0.076 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 294,664 | 5.893 | 10 | 24 | fits | 294,748 | 245 | 0.076 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 294,664 | 5.893 | 10 | 24 | fits | 294,748 | 245 | 0.076 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 294,632 | 5.893 | 10 | 50 | fits | 294,748 | 245 | 0.076 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 294,632 | 5.893 | 10 | 50 | fits | 294,748 | 245 | 0.076 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 294,599 | 5.892 | 10 | 18 | fits | 294,748 | 245 | 0.076 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 294,599 | 5.892 | 10 | 18 | fits | 294,748 | 245 | 0.076 |

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
