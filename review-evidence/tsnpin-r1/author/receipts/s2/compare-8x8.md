### 8x8/2if: S2's paths at 70936b77 and at 715589c (recorded, not graded)

| Path | Interface | ms (bound) at 70936b77 | Verdict | ms (bound) at 715589c | Verdict | Instances, misses (old -> new) |
|---|---:|---:|---|---:|---|---|
| BIND_RX | 0 | 1.431 (4.680) | fits | 0.837 (3.358) | fits | 1, 0 -> 1, 0 |
| BIND_RX | 1 | 16.944 (37.100) | MISS T_svc | 15.393 (35.662) | MISS T_svc | 1, 1 -> 1, 1 |
| DISCONNECT_TX | 0 | 16.511 (36.512) | MISS T_svc | 17.162 (37.162) | MISS T_svc | 1, 1 -> 1, 1 |
| DISCONNECT_TX | 1 | 5.052 (25.052) | fits | 7.328 (27.328) | fits | 1, 0 -> 1, 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | 22.883 (53.525) | MISS ceiling | 18.200 (27.797) | MISS T_svc **changed** | 1, 1 -> 1, 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | 24.163 (53.525) | MISS ceiling | 18.687 (27.797) | MISS T_svc **changed** | 1, 1 -> 1, 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | 17.759 (26.082) | MISS T_svc | 18.445 (27.714) | MISS T_svc | 1, 1 -> 1, 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | 19.006 (26.082) | MISS T_svc | 18.893 (27.714) | MISS T_svc | 1, 1 -> 1, 1 |
| GET_RX_STATE | 0 | 16.751 (36.632) | MISS T_svc | 17.484 (37.225) | MISS T_svc | 1, 1 -> 1, 1 |
| GET_RX_STATE | 1 | 5.834 (33.936) | fits | 4.496 (32.453) | fits | 1, 0 -> 1, 0 |
| GET_TX_CONNECTION | 0 | 16.522 (36.523) | MISS T_svc | 15.036 (35.037) | MISS T_svc | 1, 1 -> 1, 1 |
| GET_TX_CONNECTION | 1 | 1.753 (21.754) | fits | 3.620 (23.620) | fits | 1, 0 -> 1, 0 |
| GET_TX_STATE | 0 | 18.724 (38.717) | MISS T_svc | 15.087 (35.078) | MISS T_svc | 1, 1 -> 1, 1 |
| GET_TX_STATE | 1 | 8.902 (28.896) | fits | 3.660 (23.651) | fits | 1, 0 -> 1, 0 |
| PROBE_TX | 0 | 16.870 (36.550) | MISS T_svc | 17.595 (37.183) | MISS T_svc | 1, 1 -> 1, 1 |
| PROBE_TX | 1 | 5.416 (25.086) | fits | 7.793 (27.374) | fits | 1, 0 -> 1, 0 |
| PROBE_TX_RESPONSE | 0 | 4.026 (21.423) | fits | 3.406 (20.353) | fits | 1, 0 -> 1, 0 |
| PROBE_TX_RESPONSE | 1 | 7.151 (28.764) | fits | 5.854 (27.414) | fits | 1, 0 -> 1, 0 |
| TMR_DELAY | 0 | 1.488 (21.472) | fits | 0.892 (23.263) | fits | 1, 0 -> 1, 0 |
| TMR_DELAY | 1 | 3.215 (48.247) | fits | 6.668 (46.260) | fits | 1, 0 -> 1, 0 |
| TMR_NO_ADP (H-DISC) | 0 | 2.155 (23.117) | fits | 6.232 (45.204) | fits | 1, 0 -> 1, 0 |
| TMR_NO_ADP (H-DISC) | 1 | 2.558 (50.758) | fits | 3.375 (19.574) | fits | 1, 0 -> 1, 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | 3.142 (24.594) | fits | 6.568 (42.758) | fits | 1, 0 -> 1, 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | 7.910 (49.183) | fits | 6.197 (42.758) | fits | 1, 0 -> 1, 0 |
| the second TMR_NO_RESP | 0 | 2.515 (24.314) | fits | 1.452 (42.387) | fits | 1, 0 -> 1, 0 |
| the second TMR_NO_RESP | 1 | 7.659 (44.813) | fits | 4.959 (42.387) | fits | 1, 0 -> 1, 0 |
| TMR_NO_TK | 0 | 4.097 (24.646) | fits | 8.462 (46.393) | fits | 1, 0 -> 1, 0 |
| TMR_NO_TK | 1 | 3.368 (24.576) | fits | 0.911 (23.283) | fits | 1, 0 -> 1, 0 |
| TMR_RETRY | 0 | 0.359 (24.276) | fits | 5.018 (42.303) | fits | 1, 0 -> 1, 0 |
| TMR_RETRY | 1 | 8.906 (45.747) | fits | 1.763 (19.198) | fits | 1, 0 -> 1, 0 |
| UNBIND_RX | 0 | 14.530 (34.731) | MISS T_svc | 10.779 (31.135) | MISS T_svc | 1, 1 -> 1, 1 |
| UNBIND_RX | 1 | 13.468 (25.452) | MISS T_svc | 11.974 (24.118) | MISS T_svc | 1, 1 -> 1, 1 |
| RCV_ADP_DISCOVER | 0 | 0.199 (2.379) | fits | 0.622 (2.833) | fits | 2, 0 -> 2, 0 |
| RCV_ADP_DISCOVER | 1 | 0.375 (2.379) | fits | 0.796 (2.833) | fits | 1, 0 -> 1, 0 |
| GM_CHANGE | 0 | 0.079 (2.207) | fits | 0.498 (2.656) | fits | 1, 0 -> 1, 0 |
| GM_CHANGE | 1 | 0.171 (2.207) | fits | 0.584 (2.656) | fits | 1, 0 -> 1, 0 |
| LINK_DOWN | 0 | 0.063 (12.989) | fits | 0.484 (12.950) | fits | 1, 0 -> 1, 0 |
| LINK_DOWN | 1 | 5.063 (12.989) | fits | 5.460 (12.950) | fits | 1, 0 -> 1, 0 |
| LINK_UP | 0 | 0.078 (12.213) | fits | 0.489 (12.146) | fits | 5, 0 -> 5, 0 |
| LINK_UP | 1 | 0.862 (12.213) | fits | 1.225 (12.146) | fits | 5, 0 -> 5, 0 |
| TMR_ADVERTISE expiry | 0 | 0.266 (2.291) | fits | 0.548 (2.611) | fits | 1, 0 -> 1, 0 |
| TMR_ADVERTISE expiry | 1 | 0.172 (2.291) | fits | 0.456 (2.611) | fits | 1, 0 -> 1, 0 |
| TMR_DELAY expiry | 0 | 1.453 (5.908) | fits | 1.060 (5.510) | fits | 5, 0 -> 5, 0 |
| TMR_DELAY expiry | 1 | 0.848 (4.908) | fits | 0.378 (2.699) | fits | 5, 0 -> 5, 0 |
| entity_available | 0 | 2.496 (4.124) | fits | 2.438 (4.108) | fits | 1, 0 -> 1, 0 |
| entity_available | 1 | 2.927 (4.558) | fits | 2.433 (4.104) | fits | 1, 0 -> 1, 0 |
| get_avb_info | 0 | 4.588 (6.705) | fits | 2.576 (4.246) | fits | 1, 0 -> 1, 0 |
| get_avb_info | 1 | 2.618 (4.250) | fits | 2.571 (4.241) | fits | 1, 0 -> 1, 0 |
| get_configuration | 0 | 2.894 (4.524) | fits | 2.409 (4.079) | fits | 1, 0 -> 1, 0 |
| get_configuration | 1 | 2.889 (4.520) | fits | 2.834 (4.504) | fits | 1, 0 -> 1, 0 |
| get_counters | 0 | 2.772 (4.402) | fits | 4.477 (8.203) | fits | 1, 0 -> 1, 0 |
| get_counters | 1 | 2.768 (4.400) | fits | 3.149 (4.820) | fits | 1, 0 -> 1, 0 |
| get_name | 0 | 3.039 (4.668) | fits | 2.984 (4.654) | fits | 1, 0 -> 1, 0 |
| get_name | 1 | 3.048 (4.680) | fits | 2.565 (4.236) | fits | 1, 0 -> 1, 0 |
| lock_entity | 0 | 3.356 (5.212) | fits | 2.868 (4.745) | fits | 1, 0 -> 1, 0 |
| lock_entity | 1 | 2.925 (4.936) | fits | 2.869 (4.881) | fits | 1, 0 -> 1, 0 |
| MVU GET_MILAN_INFO | 0 | 2.204 (3.833) | fits | 1.726 (3.396) | fits | 1, 0 -> 1, 0 |
| MVU GET_MILAN_INFO | 1 | 1.778 (3.408) | fits | 1.722 (3.392) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (312 B) | 0 | 3.599 (5.229) | fits | 3.534 (5.204) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (312 B) | 1 | 3.590 (5.220) | fits | 3.531 (5.201) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (106 B) | 0 | 3.134 (4.764) | fits | 2.653 (4.323) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (106 B) | 1 | 2.697 (4.327) | fits | 2.649 (4.319) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (86 B) | 0 | 2.697 (4.327) | fits | 2.650 (4.320) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (72 B) | 0 | 2.668 (4.298) | fits | 2.621 (4.291) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (452 B) | 0 | 3.490 (5.120) | fits | 3.443 (5.113) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (20 B) | 0 | 2.569 (4.198) | fits | 2.521 (4.191) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (148 B) | 0 | 2.794 (4.424) | fits | 2.747 (4.417) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (148 B) | 1 | 3.350 (6.883) | fits | 2.745 (4.416) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (90 B) | 0 | 2.832 (4.462) | fits | 3.214 (4.884) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (113 B) | 0 | 2.871 (4.501) | fits | 2.824 (4.494) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (96 B) | 0 | 2.837 (4.466) | fits | 2.789 (4.459) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (146 B) | 0 | 2.801 (4.431) | fits | 2.754 (4.424) | fits | 1, 0 -> 1, 0 |
| READ_DESCRIPTOR (102 B) | 0 | 4.341 (7.990) | fits | 2.670 (4.340) | fits | 1, 0 -> 1, 0 |
| register_unsolicited | 0 | 2.199 (3.822) | fits | 1.723 (3.388) | fits | 1, 0 -> 1, 0 |
| register_unsolicited | 1 | 1.760 (3.389) | fits | 2.144 (3.815) | fits | 1, 0 -> 1, 0 |
| set_name | 0 | 4.337 (7.343) | fits | 4.279 (7.299) | fits | 1, 0 -> 1, 0 |
| set_name | 1 | 3.959 (6.645) | fits | 3.901 (6.587) | fits | 1, 0 -> 1, 0 |
| unknown_command | 0 | 2.455 (4.083) | fits | 2.409 (4.079) | fits | 1, 0 -> 1, 0 |
| unknown_command | 1 | 2.884 (4.516) | fits | 2.404 (4.075) | fits | 1, 0 -> 1, 0 |
| unlock_entity | 0 | 3.356 (5.211) | fits | 3.296 (5.172) | fits | 1, 0 -> 1, 0 |
| unlock_entity | 1 | 2.924 (4.930) | fits | 2.869 (4.879) | fits | 1, 0 -> 1, 0 |
| set_clock_source | 0 | 8.126 (9.607) | fits | 7.509 (9.032) | fits | 1, 0 -> 1, 0 |
| set_clock_source | 1 | 7.725 (9.207) | fits | 8.293 (11.893) | fits | 1, 0 -> 1, 0 |
| set_control_identify_on | 0 | 9.118 (12.805) | fits | 8.896 (12.663) | fits | 2, 0 -> 2, 0 |
| set_control_identify_on | 1 | 9.308 (12.995) | fits | 6.843 (8.534) | fits | 2, 0 -> 2, 0 |
| set_sampling_rate | 0 | 8.269 (11.769) | fits | 7.886 (11.465) | fits | 1, 0 -> 1, 0 |
| an ACMP command behind a full acmp ring | 0 | 58.721 (64.547) | MISS ceiling | 50.281 (55.301) | MISS ceiling | 1, 1 -> 1, 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | 47.983 (66.599) | MISS ceiling | 39.365 (59.334) | MISS ceiling | 1, 1 -> 1, 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | 53.763 (68.398) | MISS ceiling | 40.657 (58.497) | MISS ceiling | 1, 1 -> 1, 1 |
| an event behind 15 others | 0 | 14.843 (28.667) | MISS T_svc | 20.637 (33.358) | MISS T_svc | 1, 1 -> 1, 1 |
| a response with 7 frames owed ahead of it | 0 | 118.769 (124.507) | MISS ceiling | 111.934 (116.885) | MISS ceiling | 1, 1 -> 1, 1 |
| an ACMP command behind the owed input | 0 | at least 370.366 | NEVER ANSWERED | 137.688 (142.098) | MISS ceiling **changed** | 4, 4 -> 4, 4 |
| ANNOUNCE (TMR expiry) | 0 | 2.671 (6.719) | fits | 1.878 (5.410) | fits | 1, 0 -> 1, 0 |
| ANNOUNCE (TMR expiry) | 1 | 2.570 (6.675) | fits | 2.742 (5.485) | fits | 1, 0 -> 1, 0 |
| conflicting PROBE -> DEFEND | 0 | 1.079 (3.051) | fits | 0.605 (2.591) | fits | 1, 0 -> 1, 0 |
| conflicting PROBE -> DEFEND | 1 | 1.077 (3.078) | fits | 1.034 (3.061) | fits | 1, 0 -> 1, 0 |
| first PROBE (LINK_UP) | 0 | 0.761 (7.313) | fits | 1.122 (7.284) | fits | 1, 0 -> 1, 0 |
| first PROBE (LINK_UP) | 1 | 0.762 (6.919) | fits | 1.134 (7.328) | fits | 1, 0 -> 1, 0 |
| last PROBE retransmission (TMR expiry) | 0 | 2.522 (6.719) | fits | 1.730 (5.410) | fits | 1, 0 -> 1, 0 |
| last PROBE retransmission (TMR expiry) | 1 | 2.420 (6.675) | fits | 2.594 (5.485) | fits | 1, 0 -> 1, 0 |
| PROBE retransmission (TMR expiry) | 0 | 2.111 (6.122) | fits | 2.530 (5.075) | fits | 2, 0 -> 2, 0 |
| PROBE retransmission (TMR expiry) | 1 | 2.287 (6.357) | fits | 1.822 (5.958) | fits | 2, 0 -> 2, 0 |
| ACMP record released under the composed load, first | 0 | 14.288 | MISS T_svc | 12.660 | MISS T_svc | 4, 4 -> 4, 3 |
| ACMP record released under the composed load, last | 0 | 104.248 | MISS ceiling | 89.225 | MISS ceiling | 4, 4 -> 4, 4 |
| ADP record released under the composed load, first | 0 | 14.331 | MISS T_svc | 12.703 | MISS T_svc | 4, 4 -> 4, 3 |
| ADP record released under the composed load, last | 0 | 64.292 | MISS T_svc | 48.438 | MISS T_svc | 2, 2 -> 2, 2 |
| ADP record released under the composed load, last | 1 | 48.027 | MISS T_svc | 41.799 | MISS T_svc | 2, 2 -> 2, 2 |
| AECP record released under the composed load, first | 0 | 14.324 | MISS T_svc | 12.696 | MISS T_svc | 4, 4 -> 4, 3 |
| AECP record released under the composed load, last | 1 | 315.049 | MISS ceiling | 296.145 | MISS ceiling | 4, 4 -> 4, 4 |
| MAAP record released under the composed load, first | 0 | 14.314 | MISS T_svc | 12.686 | MISS T_svc | 4, 4 -> 4, 3 |
| MAAP record released under the composed load, last | 0 | 59.158 | MISS ceiling | 47.746 | MISS T_svc **changed** | 4, 4 -> 4, 4 |
| SRP record released under the composed load, first | 0 | at least 593.749 | STARVED: never released | at least 580.642 | STARVED: never released | 4, 4 -> 4, 4 |
| SRP record released under the composed load, last | 1 | at least 593.729 | STARVED: never released | at least 580.622 | STARVED: never released | 4, 4 -> 4, 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | 8.322 (10.070) | fits | 8.246 (10.051) | fits | 1, 0 -> 1, 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | 8.552 (10.218) | fits | 8.476 (10.195) | fits | 1, 0 -> 1, 0 |
| Listener Ready RX (registrar) | 0 | 3.308 (3.309) | fits | 3.784 (3.784) | fits | 1, 0 -> 1, 0 |
| Listener Ready RX (registrar) | 1 | 3.376 (3.377) | fits | 3.411 (3.412) | fits | 1, 0 -> 1, 0 |
| malformed MRPDU discard | 0 | 3.063 (3.064) | fits | 2.585 (2.586) | fits | 1, 0 -> 1, 0 |
| malformed MRPDU discard | 1 | 3.215 (3.216) | fits | 3.250 (3.251) | fits | 1, 0 -> 1, 0 |
| startup declarations (LINK_UP) | 0 | 6.824 (7.313) | fits | 6.768 (7.284) | fits | 1, 0 -> 1, 0 |
| startup declarations (LINK_UP) | 1 | 6.486 (6.921) | fits | 6.439 (6.903) | fits | 1, 0 -> 1, 0 |
