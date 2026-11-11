### 1x1/1if: S2's paths at 70936b77 and at 715589c (recorded, not graded)

| Path | Interface | ms (bound) at 70936b77 | Verdict | ms (bound) at 715589c | Verdict | Instances, misses (old -> new) |
|---|---:|---:|---|---:|---|---|
| BIND_RX | 0 | 0.983 (2.492) | fits | 0.814 (2.220) | fits | 2, 0 -> 2, 0 |
| DISCONNECT_TX | 0 | 9.418 (14.248) | fits | 8.651 (15.427) | fits | 1, 0 -> 1, 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | 8.723 (14.041) | fits | 6.429 (15.388) | fits | 1, 0 -> 1, 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | 15.328 (30.841) | MISS T_svc | 11.811 (15.328) | MISS T_svc | 2, 1 -> 2, 1 |
| GET_RX_STATE | 0 | 9.645 (16.045) | fits | 8.991 (15.459) | fits | 1, 0 -> 1, 0 |
| GET_TX_CONNECTION | 0 | 9.415 (14.248) | fits | 8.654 (15.425) | fits | 1, 0 -> 1, 0 |
| GET_TX_STATE | 0 | 9.454 (14.279) | fits | 10.384 (15.459) | MISS T_svc **changed** | 1, 0 -> 1, 1 |
| PROBE_TX | 0 | 8.134 (14.384) | fits | 7.409 (12.100) | fits | 1, 0 -> 1, 0 |
| PROBE_TX_RESPONSE | 0 | 12.514 (15.891) | MISS T_svc | 11.889 (15.505) | MISS T_svc | 1, 1 -> 1, 1 |
| TMR_DELAY | 0 | 0.981 (13.849) | fits | 1.341 (13.464) | fits | 1, 0 -> 1, 0 |
| TMR_NO_ADP (H-DISC) | 0 | 2.134 (13.848) | fits | 2.168 (11.758) | fits | 1, 0 -> 1, 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | 1.339 (14.309) | fits | 3.409 (28.352) | fits | 2, 0 -> 2, 0 |
| the second TMR_NO_RESP | 0 | 0.700 (13.572) | fits | 1.181 (13.272) | fits | 1, 0 -> 1, 0 |
| TMR_NO_TK | 0 | 1.990 (12.078) | fits | 1.467 (26.739) | fits | 1, 0 -> 1, 0 |
| TMR_RETRY | 0 | 0.748 (11.795) | fits | 2.580 (26.438) | fits | 1, 0 -> 1, 0 |
| UNBIND_RX | 0 | 9.599 (16.346) | fits | 8.796 (14.212) | fits | 1, 0 -> 1, 0 |
| RCV_ADP_DISCOVER | 0 | 0.224 (1.144) | fits | 0.203 (1.132) | fits | 2, 0 -> 2, 0 |
| GM_CHANGE | 0 | 0.077 (1.022) | fits | 0.083 (1.044) | fits | 1, 0 -> 1, 0 |
| LINK_DOWN | 0 | 0.065 (3.101) | fits | 0.068 (3.453) | fits | 2, 0 -> 2, 0 |
| LINK_UP | 0 | 0.077 (3.241) | fits | 0.083 (3.209) | fits | 6, 0 -> 6, 0 |
| TMR_ADVERTISE expiry | 0 | 0.786 (1.718) | fits | 0.837 (1.786) | fits | 1, 0 -> 1, 0 |
| TMR_DELAY expiry | 0 | 0.944 (2.831) | fits | 0.825 (2.741) | fits | 5, 0 -> 5, 0 |
| entity_available | 0 | 2.141 (2.923) | fits | 2.082 (2.864) | fits | 1, 0 -> 1, 0 |
| get_avb_info | 0 | 2.162 (2.944) | fits | 2.121 (2.903) | fits | 1, 0 -> 1, 0 |
| get_configuration | 0 | 2.104 (2.886) | fits | 2.056 (2.838) | fits | 1, 0 -> 1, 0 |
| get_counters | 0 | 2.392 (3.173) | fits | 2.665 (3.447) | fits | 1, 0 -> 1, 0 |
| get_name | 0 | 2.261 (3.043) | fits | 2.222 (3.004) | fits | 1, 0 -> 1, 0 |
| lock_entity | 0 | 2.266 (3.230) | fits | 2.220 (3.163) | fits | 1, 0 -> 1, 0 |
| MVU GET_MILAN_INFO | 0 | 1.735 (2.517) | fits | 1.689 (2.471) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (312 B) | 0 | 2.797 (3.579) | fits | 2.752 (3.534) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (106 B) | 0 | 2.344 (3.125) | fits | 2.303 (3.084) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (86 B) | 0 | 2.621 (3.403) | fits | 2.271 (3.053) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (72 B) | 0 | 2.284 (3.066) | fits | 2.556 (3.338) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (452 B) | 0 | 3.106 (3.888) | fits | 3.065 (3.847) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (20 B) | 0 | 2.175 (2.956) | fits | 2.133 (2.915) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (148 B) | 0 | 2.437 (3.219) | fits | 2.395 (3.177) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (90 B) | 0 | 2.362 (3.144) | fits | 2.320 (3.102) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (113 B) | 0 | 2.409 (3.191) | fits | 2.368 (3.150) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (82 B) | 0 | 2.651 (3.433) | fits | 2.614 (3.396) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (146 B) | 0 | 2.741 (3.523) | fits | 2.706 (3.488) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (102 B) | 0 | 2.343 (3.124) | fits | 2.301 (3.083) | fits | 1, 0 -> 1, 0 |
| register_unsolicited | 0 | 1.413 (2.187) | fits | 1.370 (2.143) | fits | 1, 0 -> 1, 0 |
| set_name | 0 | 2.756 (4.144) | fits | 2.698 (4.066) | fits | 1, 0 -> 1, 0 |
| unknown_command | 0 | 2.099 (2.881) | fits | 2.055 (2.837) | fits | 1, 0 -> 1, 0 |
| unlock_entity | 0 | 2.578 (3.543) | fits | 2.220 (3.162) | fits | 1, 0 -> 1, 0 |
| add_audio_mappings | 0 | 4.730 (5.543) | fits | 4.365 (5.179) | fits | 1, 0 -> 1, 0 |
| remove_audio_mappings | 0 | 4.750 (5.565) | fits | 4.385 (5.202) | fits | 1, 0 -> 1, 0 |
| set_clock_source | 0 | 4.544 (5.164) | fits | 4.180 (4.801) | fits | 1, 0 -> 1, 0 |
| set_control_identify_on | 0 | 4.377 (5.163) | fits | 4.014 (4.801) | fits | 2, 0 -> 2, 0 |
| set_sampling_rate | 0 | 4.386 (4.986) | fits | 4.026 (4.627) | fits | 1, 0 -> 1, 0 |
| an ACMP command behind a full acmp ring | 0 | 37.281 (41.386) | MISS ceiling | 33.075 (36.664) | MISS ceiling | 1, 1 -> 1, 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | 42.055 (53.150) | MISS ceiling | 37.086 (47.635) | MISS ceiling | 1, 1 -> 1, 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | 38.615 (55.069) | MISS ceiling | 33.363 (53.731) | MISS ceiling | 1, 1 -> 1, 1 |
| an event behind 15 others | 0 | 9.348 (17.383) | fits | 8.632 (15.938) | fits | 1, 0 -> 1, 0 |
| a response with 7 frames owed ahead of it | 0 | 93.481 (96.134) | MISS ceiling | 94.143 (95.734) | MISS ceiling | 1, 1 -> 1, 1 |
| an ACMP command behind the owed input | 0 | at least 362.726 | NEVER ANSWERED | 104.915 (105.904) | MISS ceiling **changed** | 4, 4 -> 4, 4 |
| SET_NAME fan-out to one registered controller | 0 | 2.989 (4.159) | fits | 2.904 (4.078) | fits | 1, 0 -> 1, 0 |
| ANNOUNCE (TMR expiry) | 0 | 1.593 (3.504) | fits | 1.004 (3.263) | fits | 1, 0 -> 1, 0 |
| conflicting PROBE -> DEFEND | 0 | 0.458 (1.359) | fits | 0.408 (1.322) | fits | 1, 0 -> 1, 0 |
| first PROBE (LINK_UP) | 0 | 0.531 (3.241) | fits | 0.500 (3.209) | fits | 1, 0 -> 1, 0 |
| last PROBE retransmission (TMR expiry) | 0 | 1.443 (3.504) | fits | 0.852 (3.263) | fits | 1, 0 -> 1, 0 |
| PROBE retransmission (TMR expiry) | 0 | 1.054 (2.615) | fits | 1.520 (3.436) | fits | 2, 0 -> 2, 0 |
| ACMP record released under the composed load, first | 0 | 9.065 | fits | 8.038 | fits | 5, 0 -> 5, 0 |
| ACMP record released under the composed load, last | 0 | 85.791 | MISS ceiling | 79.989 | MISS ceiling | 5, 4 -> 5, 4 |
| ADP record released under the composed load, first | 0 | 9.056 | fits | 8.062 | fits | 5, 0 -> 5, 0 |
| ADP record released under the composed load, last | 0 | 49.690 | MISS T_svc | 43.836 | MISS T_svc | 5, 4 -> 5, 4 |
| AECP record released under the composed load, first | 0 | 9.101 | fits | 8.073 | fits | 5, 0 -> 5, 0 |
| AECP record released under the composed load, last | 0 | 254.111 | MISS ceiling | 245.188 | MISS ceiling | 5, 4 -> 5, 4 |
| MAAP record released under the composed load, first | 0 | 9.090 | fits | 8.063 | fits | 5, 0 -> 5, 0 |
| MAAP record released under the composed load, last | 0 | 49.726 | MISS T_svc | 43.873 | MISS T_svc | 5, 4 -> 5, 4 |
| SRP record released under the composed load, first | 0 | at least 578.600 | STARVED: never released | at least 573.349 | STARVED: never released | 5, 4 -> 5, 4 |
| SRP record released under the composed load, last | 0 | at least 578.580 | STARVED: never released | at least 573.329 | STARVED: never released | 5, 4 -> 5, 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | 3.252 (4.654) | fits | 3.231 (4.630) | fits | 1, 0 -> 1, 0 |
| Listener Ready RX (registrar) | 0 | 1.904 (1.905) | fits | 1.907 (1.908) | fits | 1, 0 -> 1, 0 |
| malformed MRPDU discard | 0 | 1.582 (1.583) | fits | 1.587 (1.588) | fits | 2, 0 -> 2, 0 |
| startup declarations (LINK_UP) | 0 | 2.867 (3.241) | fits | 2.835 (3.209) | fits | 1, 0 -> 1, 0 |
