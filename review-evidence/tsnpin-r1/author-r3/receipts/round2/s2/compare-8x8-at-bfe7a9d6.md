### 8x8: S2's paths at 70936b77 and at 715589c (recorded, not graded)

| Path | Interface | ms (bound) at 70936b77 | Verdict | ms (bound) at 715589c | Verdict | Instances, misses (old -> new) |
|---|---:|---:|---|---:|---|---|
| BIND_RX | 0 | 1.431 (4.680) | fits | 0.839 (3.351) | fits | 1, 0 -> 1, 0 |
| BIND_RX | 1 | 16.944 (37.100) | MISS T_svc | 15.427 (35.693) | MISS T_svc | 1, 1 -> 1, 1 |
| DISCONNECT_TX | 0 | 16.511 (36.512) | MISS T_svc | 17.203 (37.203) | MISS T_svc | 1, 1 -> 1, 1 |
| DISCONNECT_TX | 1 | 5.052 (25.052) | fits | 7.358 (27.358) | fits | 1, 0 -> 1, 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | 22.883 (53.525) | MISS ceiling | 18.437 (27.827) | MISS T_svc **changed** | 1, 1 -> 1, 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | 24.163 (53.525) | MISS ceiling | 18.925 (27.827) | MISS T_svc **changed** | 1, 1 -> 1, 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | 17.759 (26.082) | MISS T_svc | 18.493 (27.751) | MISS T_svc | 1, 1 -> 1, 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | 19.006 (26.082) | MISS T_svc | 18.945 (27.751) | MISS T_svc | 1, 1 -> 1, 1 |
| GET_RX_STATE | 0 | 16.751 (36.632) | MISS T_svc | 17.524 (37.263) | MISS T_svc | 1, 1 -> 1, 1 |
| GET_RX_STATE | 1 | 5.834 (33.936) | fits | 4.523 (32.450) | fits | 1, 0 -> 1, 0 |
| GET_TX_CONNECTION | 0 | 16.522 (36.523) | MISS T_svc | 15.070 (35.071) | MISS T_svc | 1, 1 -> 1, 1 |
| GET_TX_CONNECTION | 1 | 1.753 (21.754) | fits | 3.640 (23.641) | fits | 1, 0 -> 1, 0 |
| GET_TX_STATE | 0 | 18.724 (38.717) | MISS T_svc | 15.124 (35.115) | MISS T_svc | 1, 1 -> 1, 1 |
| GET_TX_STATE | 1 | 8.902 (28.896) | fits | 3.682 (23.673) | fits | 1, 0 -> 1, 0 |
| PROBE_TX | 0 | 16.870 (36.550) | MISS T_svc | 17.634 (37.219) | MISS T_svc | 1, 1 -> 1, 1 |
| PROBE_TX | 1 | 5.416 (25.086) | fits | 7.823 (27.401) | fits | 1, 0 -> 1, 0 |
| PROBE_TX_RESPONSE | 0 | 4.026 (21.423) | fits | 3.415 (20.371) | fits | 1, 0 -> 1, 0 |
| PROBE_TX_RESPONSE | 1 | 7.151 (28.764) | fits | 5.861 (27.426) | fits | 1, 0 -> 1, 0 |
| TMR_DELAY | 0 | 1.488 (21.472) | fits | 2.891 (23.290) | fits | 1, 0 -> 1, 0 |
| TMR_DELAY | 1 | 3.215 (48.247) | fits | 3.105 (46.427) | fits | 1, 0 -> 1, 0 |
| TMR_NO_ADP (H-DISC) | 0 | 2.155 (23.117) | fits | 7.377 (45.230) | fits | 1, 0 -> 1, 0 |
| TMR_NO_ADP (H-DISC) | 1 | 2.558 (50.758) | fits | 2.723 (48.949) | fits | 1, 0 -> 1, 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | 3.142 (24.594) | fits | 1.301 (23.264) | fits | 1, 0 -> 1, 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | 7.910 (49.183) | fits | 6.613 (46.521) | fits | 1, 0 -> 1, 0 |
| the second TMR_NO_RESP | 0 | 2.515 (24.314) | fits | 6.894 (42.431) | fits | 1, 0 -> 1, 0 |
| the second TMR_NO_RESP | 1 | 7.659 (44.813) | fits | 5.474 (42.431) | fits | 1, 0 -> 1, 0 |
| TMR_NO_TK | 0 | 4.097 (24.646) | fits | 3.174 (23.302) | fits | 1, 0 -> 1, 0 |
| TMR_NO_TK | 1 | 3.368 (24.576) | fits | 1.940 (19.623) | fits | 1, 0 -> 1, 0 |
| TMR_RETRY | 0 | 0.359 (24.276) | fits | 4.719 (42.338) | fits | 1, 0 -> 1, 0 |
| TMR_RETRY | 1 | 8.906 (45.747) | fits | 4.605 (19.220) | fits | 1, 0 -> 1, 0 |
| UNBIND_RX | 0 | 14.530 (34.731) | MISS T_svc | 10.800 (31.159) | MISS T_svc | 1, 1 -> 1, 1 |
| UNBIND_RX | 1 | 13.468 (25.452) | MISS T_svc | 11.968 (24.144) | MISS T_svc | 1, 1 -> 1, 1 |
| RCV_ADP_DISCOVER | 0 | 0.199 (2.379) | fits | 0.202 (2.402) | fits | 2, 0 -> 2, 0 |
| RCV_ADP_DISCOVER | 1 | 0.375 (2.379) | fits | 0.376 (2.402) | fits | 1, 0 -> 1, 0 |
| GM_CHANGE | 0 | 0.079 (2.207) | fits | 0.082 (2.237) | fits | 1, 0 -> 1, 0 |
| GM_CHANGE | 1 | 0.171 (2.207) | fits | 0.174 (2.237) | fits | 1, 0 -> 1, 0 |
| LINK_DOWN | 0 | 0.063 (12.989) | fits | 0.064 (12.456) | fits | 1, 0 -> 1, 0 |
| LINK_DOWN | 1 | 5.063 (12.989) | fits | 5.011 (12.456) | fits | 1, 0 -> 1, 0 |
| LINK_UP | 0 | 0.078 (12.213) | fits | 0.079 (12.077) | fits | 5, 0 -> 5, 0 |
| LINK_UP | 1 | 0.862 (12.213) | fits | 0.796 (12.077) | fits | 5, 0 -> 5, 0 |
| TMR_ADVERTISE expiry | 0 | 0.266 (2.291) | fits | 0.420 (2.473) | fits | 1, 0 -> 1, 0 |
| TMR_ADVERTISE expiry | 1 | 0.172 (2.291) | fits | 1.328 (3.473) | fits | 1, 0 -> 1, 0 |
| TMR_DELAY expiry | 0 | 1.453 (5.908) | fits | 2.231 (6.345) | fits | 5, 0 -> 5, 0 |
| TMR_DELAY expiry | 1 | 0.848 (4.908) | fits | 1.912 (6.345) | fits | 5, 0 -> 5, 0 |
| entity_available | 0 | 2.496 (4.124) | fits | 2.840 (4.514) | fits | 1, 0 -> 1, 0 |
| entity_available | 1 | 2.927 (4.558) | fits | 2.848 (4.523) | fits | 1, 0 -> 1, 0 |
| get_avb_info | 0 | 4.588 (6.705) | fits | 2.561 (4.235) | fits | 1, 0 -> 1, 0 |
| get_avb_info | 1 | 2.618 (4.250) | fits | 2.555 (4.230) | fits | 1, 0 -> 1, 0 |
| get_configuration | 0 | 2.894 (4.524) | fits | 2.395 (4.069) | fits | 1, 0 -> 1, 0 |
| get_configuration | 1 | 2.889 (4.520) | fits | 2.819 (4.495) | fits | 1, 0 -> 1, 0 |
| get_counters | 0 | 2.772 (4.402) | fits | 2.754 (4.813) | fits | 1, 0 -> 1, 0 |
| get_counters | 1 | 2.768 (4.400) | fits | 2.704 (4.379) | fits | 1, 0 -> 1, 0 |
| get_name | 0 | 3.039 (4.668) | fits | 2.555 (4.229) | fits | 1, 0 -> 1, 0 |
| get_name | 1 | 3.048 (4.680) | fits | 2.984 (4.660) | fits | 1, 0 -> 1, 0 |
| lock_entity | 0 | 3.356 (5.212) | fits | 3.284 (5.165) | fits | 1, 0 -> 1, 0 |
| lock_entity | 1 | 2.925 (4.936) | fits | 2.856 (4.875) | fits | 1, 0 -> 1, 0 |
| MVU GET_MILAN_INFO | 0 | 2.204 (3.833) | fits | 2.138 (3.812) | fits | 1, 0 -> 1, 0 |
| MVU GET_MILAN_INFO | 1 | 1.778 (3.408) | fits | 1.706 (3.381) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (312 B) | 0 | 3.599 (5.229) | fits | 3.521 (5.195) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (312 B) | 1 | 3.590 (5.220) | fits | 3.511 (5.185) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (106 B) | 0 | 3.134 (4.764) | fits | 2.639 (4.313) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (106 B) | 1 | 2.697 (4.327) | fits | 3.063 (4.737) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (86 B) | 0 | 2.697 (4.327) | fits | 2.636 (4.310) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (72 B) | 0 | 2.668 (4.298) | fits | 2.607 (4.280) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (452 B) | 0 | 3.490 (5.120) | fits | 3.429 (5.103) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (20 B) | 0 | 2.569 (4.198) | fits | 2.507 (4.181) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (148 B) | 0 | 2.794 (4.424) | fits | 2.732 (4.406) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (148 B) | 1 | 3.350 (6.883) | fits | 2.726 (4.400) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (90 B) | 0 | 2.832 (4.462) | fits | 3.201 (4.875) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (113 B) | 0 | 2.871 (4.501) | fits | 2.810 (4.484) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (96 B) | 0 | 2.837 (4.466) | fits | 2.775 (4.449) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (146 B) | 0 | 2.801 (4.431) | fits | 3.170 (4.844) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (102 B) | 0 | 4.341 (7.990) | fits | 2.656 (4.330) | fits | 1, 0 -> 1, 0 |
| register_unsolicited | 0 | 2.199 (3.822) | fits | 1.707 (3.375) | fits | 1, 0 -> 1, 0 |
| register_unsolicited | 1 | 1.760 (3.389) | fits | 2.129 (3.804) | fits | 1, 0 -> 1, 0 |
| set_name | 0 | 4.337 (7.343) | fits | 4.271 (7.297) | fits | 1, 0 -> 1, 0 |
| set_name | 1 | 3.959 (6.645) | fits | 3.889 (6.584) | fits | 1, 0 -> 1, 0 |
| unknown_command | 0 | 2.455 (4.083) | fits | 2.394 (4.068) | fits | 1, 0 -> 1, 0 |
| unknown_command | 1 | 2.884 (4.516) | fits | 2.817 (4.492) | fits | 1, 0 -> 1, 0 |
| unlock_entity | 0 | 3.356 (5.211) | fits | 3.280 (5.160) | fits | 1, 0 -> 1, 0 |
| unlock_entity | 1 | 2.924 (4.930) | fits | 3.286 (5.300) | fits | 1, 0 -> 1, 0 |
| set_clock_source | 0 | 8.126 (9.607) | fits | 8.783 (12.378) | fits | 1, 0 -> 1, 0 |
| set_clock_source | 1 | 7.725 (9.207) | fits | 8.239 (11.834) | fits | 1, 0 -> 1, 0 |
| set_control_identify_on | 0 | 9.118 (12.805) | fits | 6.914 (10.676) | fits | 2, 0 -> 2, 0 |
| set_control_identify_on | 1 | 9.308 (12.995) | fits | 8.842 (12.604) | fits | 2, 0 -> 2, 0 |
| set_sampling_rate | 0 | 8.269 (11.769) | fits | 7.826 (10.548) | fits | 1, 0 -> 1, 0 |
| an ACMP command behind a full acmp ring | 0 | 58.721 (64.547) | MISS ceiling | 51.129 (56.134) | MISS ceiling | 1, 1 -> 1, 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | 47.983 (66.599) | MISS ceiling | 39.882 (59.325) | MISS ceiling | 1, 1 -> 1, 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | 53.763 (68.398) | MISS ceiling | 41.201 (58.546) | MISS ceiling | 1, 1 -> 1, 1 |
| an event behind 15 others | 0 | 14.843 (28.667) | MISS T_svc | 12.858 (24.647) | MISS T_svc | 1, 1 -> 1, 1 |
| a response with 7 frames owed ahead of it | 0 | 118.769 (124.507) | MISS ceiling | 112.723 (117.669) | MISS ceiling | 1, 1 -> 1, 1 |
| an ACMP command behind the owed input | 0 | at least 370.366 | NEVER ANSWERED | 138.526 (142.934) | MISS ceiling **changed** | 4, 4 -> 4, 4 |
| ANNOUNCE (TMR expiry) | 0 | 2.671 (6.719) | fits | 1.413 (5.487) | fits | 1, 0 -> 1, 0 |
| ANNOUNCE (TMR expiry) | 1 | 2.570 (6.675) | fits | 1.856 (6.018) | fits | 1, 0 -> 1, 0 |
| conflicting PROBE -> DEFEND | 0 | 1.079 (3.051) | fits | 0.594 (2.564) | fits | 1, 0 -> 1, 0 |
| conflicting PROBE -> DEFEND | 1 | 1.077 (3.078) | fits | 1.023 (3.043) | fits | 1, 0 -> 1, 0 |
| first PROBE (LINK_UP) | 0 | 0.761 (7.313) | fits | 0.695 (6.824) | fits | 1, 0 -> 1, 0 |
| first PROBE (LINK_UP) | 1 | 0.762 (6.919) | fits | 1.117 (7.289) | fits | 1, 0 -> 1, 0 |
| last PROBE retransmission (TMR expiry) | 0 | 2.522 (6.719) | fits | 1.265 (5.487) | fits | 1, 0 -> 1, 0 |
| last PROBE retransmission (TMR expiry) | 1 | 2.420 (6.675) | fits | 1.708 (6.018) | fits | 1, 0 -> 1, 0 |
| PROBE retransmission (TMR expiry) | 0 | 2.111 (6.122) | fits | 2.421 (6.878) | fits | 2, 0 -> 2, 0 |
| PROBE retransmission (TMR expiry) | 1 | 2.287 (6.357) | fits | 2.289 (6.411) | fits | 2, 0 -> 2, 0 |
| ACMP record released under the composed load, first | 0 | 14.288 | MISS T_svc | 12.271 | MISS T_svc | 4, 4 -> 4, 3 |
| ACMP record released under the composed load, last | 0 | 104.248 | MISS ceiling | 88.933 | MISS ceiling | 4, 4 -> 4, 4 |
| ADP record released under the composed load, first | 0 | 14.331 | MISS T_svc | 12.313 | MISS T_svc | 4, 4 -> 4, 3 |
| ADP record released under the composed load, last | 0 | 64.292 | MISS T_svc | 48.976 | MISS T_svc | 2, 2 -> 2, 2 |
| ADP record released under the composed load, last | 1 | 48.027 | MISS T_svc | 42.650 | MISS T_svc | 2, 2 -> 2, 2 |
| AECP record released under the composed load, first | 0 | 14.324 | MISS T_svc | 12.306 | MISS T_svc | 4, 4 -> 4, 3 |
| AECP record released under the composed load, last | 1 | 315.049 | MISS ceiling | 298.837 | MISS ceiling | 4, 4 -> 4, 4 |
| MAAP record released under the composed load, first | 0 | 14.314 | MISS T_svc | 12.296 | MISS T_svc | 4, 4 -> 4, 3 |
| MAAP record released under the composed load, last | 0 | 59.158 | MISS ceiling | 48.246 | MISS T_svc **changed** | 4, 4 -> 4, 4 |
| SRP record released under the composed load, first | 0 | at least 593.749 | STARVED: never released | at least 581.187 | STARVED: never released | 4, 4 -> 4, 4 |
| SRP record released under the composed load, last | 1 | at least 593.729 | STARVED: never released | at least 581.166 | STARVED: never released | 4, 4 -> 4, 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | 8.322 (10.070) | fits | 7.713 (9.498) | fits | 1, 0 -> 1, 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | 8.552 (10.218) | fits | 7.871 (9.564) | fits | 1, 0 -> 1, 0 |
| Listener Ready RX (registrar) | 0 | 3.308 (3.309) | fits | 3.342 (3.343) | fits | 1, 0 -> 1, 0 |
| Listener Ready RX (registrar) | 1 | 3.376 (3.377) | fits | 3.924 (3.925) | fits | 1, 0 -> 1, 0 |
| malformed MRPDU discard | 0 | 3.063 (3.064) | fits | 3.097 (3.098) | fits | 1, 0 -> 1, 0 |
| malformed MRPDU discard | 1 | 3.215 (3.216) | fits | 3.249 (3.250) | fits | 1, 0 -> 1, 0 |
| startup declarations (LINK_UP) | 0 | 6.824 (7.313) | fits | 6.317 (6.824) | fits | 1, 0 -> 1, 0 |
| startup declarations (LINK_UP) | 1 | 6.486 (6.921) | fits | 6.407 (6.865) | fits | 1, 0 -> 1, 0 |
