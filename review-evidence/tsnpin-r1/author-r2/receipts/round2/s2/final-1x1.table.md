### 1x1

13 of 81 paths and 34 of 141 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.812 (2.218) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 8.582 (15.397) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 5.865 (15.361) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 7.128 (15.300) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 8.916 (15.424) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 8.578 (15.397) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 10.319 (15.429) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 7.334 (12.061) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 11.818 (15.476) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 2.236 (26.602) | fits | 1 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 2.063 (13.407) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 3.712 (28.587) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.399 (13.230) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 1.365 (13.425) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 1.919 (13.161) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 8.720 (14.172) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.200 (1.134) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.081 (1.046) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.065 (3.099) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.081 (3.207) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.700 (1.650) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 1.178 (3.402) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.082 (2.867) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 2.122 (2.906) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.365 (3.149) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 2.661 (3.445) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 2.223 (3.007) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 2.216 (3.166) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 1.682 (2.466) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 2.753 (3.537) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 2.303 (3.087) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 2.577 (3.361) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.243 (3.027) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.065 (3.849) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 2.133 (2.918) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 2.441 (3.225) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 2.396 (3.180) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 2.321 (3.105) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 2.368 (3.152) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.302 (3.086) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 2.697 (3.481) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 2.395 (3.180) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 2.301 (3.086) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.370 (2.145) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 2.699 (4.073) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.055 (2.840) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 2.528 (3.477) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 4.410 (5.228) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 4.285 (5.075) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 4.432 (5.251) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 4.225 (4.849) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 4.058 (4.848) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 6.022 (7.159) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 4.071 (4.675) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 4.291 (5.082) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 32.943 (36.538) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 36.620 (47.426) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 32.832 (53.625) | MISS ceiling | 2 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 8.543 (15.848) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 90.860 (92.447) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 104.568 (105.619) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 2.908 (4.084) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.817 (2.760) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.406 (1.321) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.497 (3.207) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.665 (2.760) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.991 (2.911) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 7.973 | fits | 0 acmp | 5 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 79.179 | MISS ceiling | 11 acmp | 5 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 8.015 | fits | 0 adp | 5 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 43.373 | MISS T_svc | 7 adp | 5 | 4 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 8.009 | fits | 0 aecp | 5 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp-refill.service.aecp.last.if0` (backlog-adp-refill) | 244.309 | MISS ceiling | 15 aecp | 5 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 7.998 | fits | 0 maap | 5 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 43.410 | MISS T_svc | 6 maap | 5 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 572.817 | STARVED: never released | 0 srp | 5 | 4 |
| SRP record released under the composed load, last | 0 | `backlog-adp-refill.service.srp.last.if0` (backlog-adp-refill) | at least 572.797 | STARVED: never released | 31 srp | 5 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 3.233 (4.631) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 1.911 (1.912) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 1.585 (1.585) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 2.830 (3.207) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 87.979 | 23 | 400,867 (8.017) | yes | - |
| backlog-adp | 536.673 | 36 | 925,956 (18.519) | no | {'srp': 32} |
| backlog-adp-refill | 572.834 | 39 | 949,973 (18.999) | no | {'srp': 32} |
| backlog-owed | 108.547 | 30 | 369,197 (7.384) | yes | - |
| fixture | 9.756 | 3 | 227,822 (4.556) | yes | - |

Composed maximum over the 4 backlog windows: at least 949,973 CPU cycles (18.999 ms), backlog-adp-refill, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 400,867 (8.017 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 68,238 | 1.365 | 10 | 20 | fits | 671,236 | 119 (14) | 0.038 |
| LINK_UP | `adp.link_up.if0` | 4,057 | 0.081 | 10 | 200 | fits | 160,358 | 88 (11) | 0.094 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 58,916 | 1.178 | 10 | 200 | fits | 79,165 | 52 (39) | 0.109 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 35,012 | 0.700 | 10 | 200 | fits | 19,889 | 15 (11) | 0.156 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 158,547 | 3.171 | 10 | 20 | fits | 669,999 | 140 (35) | 0.036 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 19,957 | 0.399 | 10 | 20 | fits | 661,485 | 117 (14) | 0.036 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 95,928 | 1.919 | 10 | 20 | fits | 658,068 | 118 (14) | 0.036 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 111,819 | 2.236 | 10 | 20 | fits | 670,888 | 140 (35) | 0.037 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 141,489 | 2.830 | 10 | 18 | fits | 160,358 | 88 | 0.094 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 95,566 | 1.911 | 10 | 18 | fits | 95,598 | 29 | 0.113 |
| malformed MRPDU discard | `srp.malformed.if0` | 79,236 | 1.585 | 10 | 18 | fits | 79,268 | 35 | 0.113 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 161,647 | 3.233 | 210 | 218 | fits | 231,545 | 78 | 0.092 |
| an event behind 15 others | `backlog.event.if0` | 427,151 | 8.543 | 10 | 200 | fits | 391,545 | 356 | 0.065 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 1,647,172 | 32.943 | 10 | 20 | MISS ceiling | 226,941 | 211 | 0.051 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 400,763 | 8.015 | 10 | 200 | fits | 400,867 | 389 | 0.063 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 1,345,521 | 26.910 | 10 | 200 | MISS T_svc | 251,364 | 279 | 0.050 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 398,634 | 7.973 | 10 | 20 | fits | 400,867 | 389 | 0.063 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 1,824,257 | 36.485 | 10 | 20 | MISS ceiling | 226,941 | 211 | 0.051 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 400,426 | 8.009 | 10 | 24 | fits | 400,867 | 389 | 0.063 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 3,747,398 | 74.948 | 10 | 24 | MISS ceiling | 176,749 | 124 | 0.045 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 399,906 | 7.998 | 10 | 50 | fits | 400,867 | 389 | 0.063 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 1,344,773 | 26.895 | 10 | 50 | MISS T_svc | 251,364 | 279 | 0.050 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 1,093,377 | 21.868 | 10 | 18 | MISS ceiling | 302,153 | 348 | 0.056 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 4,106,494 | 82.130 | 10 | 18 | MISS ceiling | 56,865 | 47 | 0.085 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 1,830,981 | 36.620 | 10 | 20 | MISS ceiling | 891,284 | 411 | 0.039 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 385,985 | 7.720 | 10 | 200 | fits | 588,336 | 412 | 0.043 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,168,642 | 43.373 | 10 | 200 | MISS T_svc | 891,284 | 411 | 0.039 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 386,441 | 7.729 | 10 | 20 | fits | 588,336 | 412 | 0.043 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 3,936,306 | 78.726 | 10 | 20 | MISS ceiling | 925,956 | 327 | 0.034 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 388,233 | 7.765 | 10 | 24 | fits | 588,336 | 412 | 0.043 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 12,193,010 | 243.860 | 10 | 24 | MISS ceiling | 883,234 | 273 | 0.038 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 387,713 | 7.754 | 10 | 50 | fits | 588,336 | 412 | 0.043 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,170,480 | 43.410 | 10 | 50 | MISS T_svc | 891,284 | 411 | 0.039 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 26,832,786 | 536.656 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 26,831,779 | 536.636 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 1,641,604 | 32.832 | 10 | 20 | MISS ceiling | 949,973 | 359 | 0.035 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 385,985 | 7.720 | 10 | 200 | fits | 588,336 | 412 | 0.043 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 1,961,151 | 39.223 | 10 | 200 | MISS T_svc | 949,973 | 359 | 0.035 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 386,441 | 7.729 | 10 | 20 | fits | 588,336 | 412 | 0.043 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 3,958,957 | 79.179 | 10 | 20 | MISS ceiling | 949,973 | 359 | 0.035 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 388,233 | 7.765 | 10 | 24 | fits | 588,336 | 412 | 0.043 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 12,215,467 | 244.309 | 10 | 24 | MISS ceiling | 883,421 | 273 | 0.038 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 387,713 | 7.754 | 10 | 50 | fits | 588,336 | 412 | 0.043 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,153,877 | 43.078 | 10 | 50 | MISS T_svc | 874,681 | 404 | 0.037 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 28,640,867 | 572.817 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 28,639,860 | 572.797 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 4,543,017 | 90.860 | 10 | 20 | MISS ceiling | 188,019 | 147 | 0.050 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 4,747,919 | 94.958 | 10 | 20 | MISS ceiling | 204,894 | 154 | 0.056 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 4,936,088 | 98.722 | 10 | 20 | MISS ceiling | 188,252 | 148 | 0.050 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 5,140,996 | 102.820 | 10 | 20 | MISS ceiling | 204,900 | 154 | 0.056 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 5,228,423 | 104.568 | 10 | 20 | MISS ceiling | 60,564 | 34 | 0.101 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 311,773 | 6.235 | 10 | 200 | fits | 311,396 | 341 | 0.064 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 1,318,628 | 26.373 | 10 | 200 | MISS T_svc | 340,166 | 300 | 0.071 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 309,644 | 6.193 | 10 | 20 | fits | 311,396 | 341 | 0.064 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 3,629,966 | 72.599 | 10 | 20 | MISS ceiling | 214,376 | 167 | 0.052 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 311,436 | 6.229 | 10 | 24 | fits | 311,396 | 341 | 0.064 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 5,219,948 | 104.399 | 10 | 24 | MISS ceiling | 204,900 | 154 | 0.056 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 310,916 | 6.218 | 10 | 50 | fits | 311,396 | 341 | 0.064 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 1,317,880 | 26.358 | 10 | 50 | MISS T_svc | 340,166 | 300 | 0.071 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 977,682 | 19.554 | 10 | 18 | MISS ceiling | 369,197 | 337 | 0.073 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 3,201,431 | 64.029 | 10 | 18 | MISS ceiling | 176,279 | 173 | 0.089 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 267,143 | 5.343 | 10 | 20 | fits | 682,204 | 140 (29) | 0.038 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 293,229 | 5.865 | 10 | 20 | fits | 768,062 | 156 (35) | 0.035 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 103,152 | 2.063 | 10 | 20 | fits | 670,354 | 140 (12) | 0.036 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 24,864 | 0.497 | 10 | 50 | fits | 160,358 | 88 | 0.094 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 42,857 | 0.857 | 10 | 50 | fits | 83,130 | 43 | 0.111 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 49,525 | 0.991 | 10 | 50 | fits | 68,052 | 37 | 0.106 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 33,234 | 0.665 | 10 | 50 | fits | 83,792 | 64 | 0.097 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 40,826 | 0.817 | 10 | 50 | fits | 83,792 | 64 | 0.097 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 20,290 | 0.406 | 10 | 50 | fits | 66,027 | 47 | 0.094 |
| LINK_UP | `adp.link_up.if0` | 4,057 | 0.081 | 10 | 200 | fits | 160,358 | 88 (11) | 0.094 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 58,916 | 1.178 | 10 | 200 | fits | 79,165 | 52 (39) | 0.109 |
| LINK_DOWN | `adp.link_down.if0` | 3,254 | 0.065 | 10 | 200 | fits | 154,937 | 27 (9) | 0.091 |
| LINK_UP | `adp.link_up.if0` | 4,057 | 0.081 | 10 | 200 | fits | 160,358 | 88 (11) | 0.094 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 58,916 | 1.178 | 10 | 200 | fits | 79,165 | 52 (39) | 0.109 |
| GM_CHANGE | `adp.gm_change.if0` | 4,049 | 0.081 | 10 | 200 | fits | 52,316 | 18 (11) | 0.109 |
| LINK_UP | `adp.link_up.if0` | 4,057 | 0.081 | 10 | 200 | fits | 160,358 | 88 (11) | 0.094 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 58,916 | 1.178 | 10 | 200 | fits | 79,165 | 52 (39) | 0.109 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 9,999 | 0.200 | 10 | 200 | fits | 56,713 | 38 (31) | 0.096 |
| LINK_UP | `adp.link_up.if0` | 4,057 | 0.081 | 10 | 200 | fits | 160,358 | 88 (11) | 0.094 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 58,916 | 1.178 | 10 | 200 | fits | 79,165 | 52 (39) | 0.109 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 9,999 | 0.200 | 10 | 200 | fits | 56,713 | 38 (31) | 0.096 |
| set_name | `aecp_fanout.set_name.if0` | 301,107 | 6.022 | 10 | 24 | fits | 357,953 | 623 | 0.042 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 211,228 | 4.225 | 10 | 24 | fits | 242,430 | 329 | 0.056 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 202,513 | 4.050 | 10 | 24 | fits | 242,009 | 312 | 0.053 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 202,881 | 4.058 | 10 | 24 | fits | 242,420 | 312 | 0.053 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 221,580 | 4.432 | 10 | 24 | fits | 262,574 | 352 | 0.053 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 220,511 | 4.410 | 10 | 24 | fits | 261,386 | 352 | 0.051 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 203,530 | 4.071 | 10 | 24 | fits | 233,752 | 318 | 0.056 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 214,231 | 4.285 | 10 | 24 | fits | 253,744 | 363 | 0.050 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 214,543 | 4.291 | 10 | 24 | fits | 254,082 | 363 | 0.050 |
| BIND_RX | `acmp.bind_rx.if0` | 40,576 | 0.812 | 10 | 20 | fits | 110,902 | 83 (77) | 0.089 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 590,917 | 11.818 | 10 | 20 | MISS T_svc | 773,821 | 153 (32) | 0.036 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 445,824 | 8.916 | 10 | 20 | fits | 771,208 | 168 (47) | 0.035 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 436,004 | 8.720 | 10 | 20 | fits | 708,581 | 161 (50) | 0.040 |
| PROBE_TX | `acmp.probe_tx.if0` | 366,704 | 7.334 | 10 | 20 | fits | 603,042 | 181 (48) | 0.041 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 515,956 | 10.319 | 10 | 20 | MISS T_svc | 771,444 | 169 (48) | 0.035 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 429,095 | 8.582 | 10 | 20 | fits | 769,836 | 169 (48) | 0.034 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 428,899 | 8.578 | 10 | 20 | fits | 769,829 | 169 (48) | 0.034 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 68,494 | 1.370 | 10 | 24 | fits | 107,261 | 48 | 0.072 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 137,631 | 2.753 | 10 | 24 | fits | 176,847 | 125 | 0.049 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 115,145 | 2.303 | 10 | 24 | fits | 154,358 | 74 | 0.055 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 119,786 | 2.396 | 10 | 24 | fits | 158,999 | 85 | 0.053 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 134,826 | 2.697 | 10 | 24 | fits | 174,042 | 90 | 0.061 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 119,765 | 2.395 | 10 | 24 | fits | 158,981 | 84 | 0.053 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 115,068 | 2.301 | 10 | 24 | fits | 154,284 | 73 | 0.055 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 128,842 | 2.577 | 10 | 24 | fits | 168,058 | 75 | 0.063 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 112,154 | 2.243 | 10 | 24 | fits | 151,367 | 66 | 0.056 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 153,258 | 3.065 | 10 | 24 | fits | 192,471 | 161 | 0.045 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 106,666 | 2.133 | 10 | 24 | fits | 145,879 | 53 | 0.058 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 122,034 | 2.441 | 10 | 24 | fits | 161,247 | 59 | 0.065 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 116,036 | 2.321 | 10 | 24 | fits | 155,249 | 70 | 0.054 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 118,403 | 2.368 | 10 | 24 | fits | 157,616 | 76 | 0.054 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 115,084 | 2.302 | 10 | 24 | fits | 154,297 | 68 | 0.055 |
| get_configuration | `aecp.get_configuration.if0` | 118,225 | 2.365 | 10 | 24 | fits | 157,438 | 54 | 0.065 |
| entity_available | `aecp.entity_available.if0` | 104,115 | 2.082 | 10 | 24 | fits | 143,331 | 52 | 0.057 |
| get_name | `aecp.get_name.if0` | 111,158 | 2.223 | 10 | 24 | fits | 150,374 | 65 | 0.057 |
| get_counters | `aecp.get_counters.if0` | 133,043 | 2.661 | 10 | 24 | fits | 172,259 | 92 | 0.064 |
| get_avb_info | `aecp.get_avb_info.if0` | 106,081 | 2.122 | 10 | 24 | fits | 145,297 | 48 | 0.058 |
| unknown_command | `aecp.unknown_command.if0` | 102,764 | 2.055 | 10 | 24 | fits | 141,980 | 48 | 0.057 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 84,100 | 1.682 | 10 | 24 | fits | 123,316 | 58 | 0.081 |
| set_name | `aecp.set_name.if0` | 134,946 | 2.699 | 10 | 24 | fits | 203,626 | 128 | 0.054 |
| lock_entity | `aecp.lock_entity.if0` | 110,814 | 2.216 | 10 | 24 | fits | 158,293 | 78 | 0.059 |
| unlock_entity | `aecp.unlock_entity.if0` | 126,389 | 2.528 | 10 | 24 | fits | 173,851 | 84 | 0.066 |
| LINK_UP | `fixture.link_up.if0` | 4,057 | 0.081 | 10 | 200 | fits | 160,358 | 88 (11) | 0.094 |
| malformed MRPDU discard | `fixture.malformed.if0` | 59,138 | 1.183 | 10 | 18 | fits | 59,170 | 29 | 0.109 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 145,386 | 2.908 | 10 | 24 | fits | 204,203 | 127 | 0.054 |
| LINK_DOWN | `fixture.link_down.if0` | 3,254 | 0.065 | 10 | 200 | fits | 172,577 | 33 (9) | 0.096 |
| BIND_RX | `fixture.bind_rx.if0` | 40,576 | 0.812 | 10 | 20 | fits | 100,979 | 83 (77) | 0.084 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 185,611 | 3.712 | 10 | 20 | fits | 687,024 | 169 (35) | 0.037 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 356,385 | 7.128 | 10 | 20 | fits | 765,001 | 150 (29) | 0.034 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 227,771 | 4.555 | 10 | 200 | fits | 227,822 | 225 | 0.058 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 227,771 | 4.555 | 10 | 200 | fits | 227,822 | 225 | 0.058 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 227,636 | 4.553 | 10 | 20 | fits | 227,822 | 225 | 0.058 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 227,636 | 4.553 | 10 | 20 | fits | 227,822 | 225 | 0.058 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 227,738 | 4.555 | 10 | 24 | fits | 227,822 | 225 | 0.058 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 227,738 | 4.555 | 10 | 24 | fits | 227,822 | 225 | 0.058 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 227,706 | 4.554 | 10 | 50 | fits | 227,822 | 225 | 0.058 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 227,706 | 4.554 | 10 | 50 | fits | 227,822 | 225 | 0.058 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 341,614 | 6.832 | 10 | 18 | fits | 113,941 | 37 | 0.116 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 341,614 | 6.832 | 10 | 18 | fits | 113,941 | 37 | 0.116 |

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
