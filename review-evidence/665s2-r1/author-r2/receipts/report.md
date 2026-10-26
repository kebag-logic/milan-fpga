## counts
| Arm | Groups | Paths missing T_svc | Probe instances missing T_svc |
|---|---:|---:|---:|
| A1 | 17 | 10 of 61 | 11 of 78 |
| A8 | 16 | 37 of 106 | 45 of 125 |
| B1 | 7 | 4 of 20 | 4 of 20 |
| B8 | 7 | 4 of 36 | 4 of 36 |
| S1 | 2 | 0 of 2 | 0 of 2 |
| S8 | 2 | 0 of 3 | 0 of 3 |

## summaries
| Point | CPU cycles per instruction | Fetches per instruction | Mailbox read / write, CPU cycles | BRAM fetch, CPU cycles (max) | sram load/store | CSR | Flash window load | Code fetched, boot / service (largest run) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1 | 9.54 | 1.69 | 9 / 9 | 9.09 (303) | 9-10 / 9-10 | 9-10 / 9 | 262.8 mean (138-303) | 11,160 / 42,080 B |
| 8x8 | 9.51 | 1.68 | 9 / 9 | 9.13 (303) | 9-10 / 9-10 | 9-10 / 9 | 262.5 mean (138-303) | 11,396 / 43,060 B |

## passes
| Point, arm | Idle pass, CPU cycles (ms) | Worst pass, CPU cycles (ms), group | Composed maximum, CPU cycles (ms), group |
|---|---:|---:|---:|
| 1x1, A | 65,703 to 72,358 (1.31 to 1.45) | 1,565,803 (31.32), backlog-adp | 1,565,803 (31.32), backlog-adp |
| 1x1, B | 65,703 to 232,901 (1.31 to 4.66) | 740,260 (14.81), backlog | 740,260 (14.81), backlog |
| 8x8, A | 102,152 to 185,315 (2.04 to 3.71) | 2,989,496 (59.79), acmp-notk | 2,209,308 (44.19), backlog-adp-refill |
| 8x8, B | 7,081 to 293,468 (0.14 to 5.87) | 2,004,666 (40.09), acmp-notk | 1,392,016 (27.84), backlog |

## adp
| Path ([`MAILBOX_SPLIT.md:495-502`](../../../docs/design/MAILBOX_SPLIT.md#service-latency)) | 1x1 ms (bound) | 8x8 if0 / if1 ms (bound) | Accesses in the taking pass, 1x1 / 8x8 (model) |
|---|---:|---:|---:|
| RCV_ADP_DISCOVER -> TMR_DELAY armed | 0.29 (1.63) | 2.57 (9.27) / 2.86 (9.27) | 38 / 73 (31) |
| TMR_DELAY expiry -> ENTITY_AVAILABLE, TMR_ADVERTISE armed | 0.87 (3.57) | 2.64 (9.09) / 3.70 (10.87) | 46 / 47 (39) |
| TMR_ADVERTISE expiry -> TMR_DELAY armed | 0.13 (1.99) | 1.06 (8.28) / 1.37 (4.60) | 9 / 25 (11) |
| GM_CHANGE -> TMR_DELAY armed | 0.10 (1.46) | 2.38 (8.95) / 2.50 (8.95) | 18 / 34 (11) |
| LINK_UP -> TMR_DELAY armed | 0.11 (4.97) | 32.51 (73.31) **miss** / 41.69 (73.31) **miss** | 88 / 345 (11) |
| LINK_DOWN -> timer stopped | 0.08 (5.48) | 18.35 (42.60) **miss** / 26.84 (42.60) **miss** | 33 / 70 (9) |
| SHUTDOWN -> ENTITY_DEPARTING (test-only entry, `shutdown-entry` arm) | 0.58 (1.94) | 0.58 (5.14) / 1.17 (5.14) | 39 / 75 (29) |

## acmp
| Path ([`MAILBOX_SPLIT.md:645-657`](../../../docs/design/MAILBOX_SPLIT.md#acmp-service-latency)) | A: 1x1 ms (bound) | A: 8x8 if0 / if1 | B: 1x1 | B: 8x8 if0 / if1 | Accesses, A 1x1 / 8x8 (model) |
|---|---:|---:|---:|---:|---:|
| BIND_RX | 1.62 (3.96) | 4.51 (13.22) / 11.36 (31.60) **miss** | 1.62 (3.96) | 4.51 (13.22) / 4.22 (12.59) | 82 / 90 (77) |
| UNBIND_RX | 6.56 (26.86) | 6.75 (27.03) / 19.80 (40.08) **miss** | 1.07 (3.22) | 3.99 (10.46) / 3.95 (12.55) | 119 / 176 (50) |
| GET_RX_STATE | 3.34 (23.10) | 10.96 (30.77) **miss** / 19.79 (39.60) **miss** | 0.96 (2.79) | 4.15 (12.47) / 3.46 (10.05) | 113 / 114 (47) |
| PROBE_TX_RESPONSE | 12.02 (29.87) **miss** | 19.40 (35.12) **miss** / 15.99 (39.22) **miss** | 0.37 (2.46) | 2.95 (11.41) / 3.41 (11.87) | 104 / 102 (32) |
| PROBE_TX | 3.48 (23.02) | 11.17 (30.68) **miss** / 21.02 (54.45) **over ceiling** | 1.51 (3.25) | 1.54 (9.89) / 4.11 (12.26) | 115 / 116 (48) |
| GET_TX_STATE | 6.37 (26.36) | 10.67 (30.66) **miss** / 27.60 (87.09) **over ceiling** | 1.00 (2.72) | 3.52 (11.65) / 3.53 (9.89) | 117 / 115 (48) |
| DISCONNECT_TX | 24.77 (44.77) **over ceiling** | 10.62 (30.62) **miss** / 20.18 (32.59) **over ceiling** | 0.95 (2.67) | 0.96 (6.62) / 4.19 (12.34) | 117 / 115 (48) |
| GET_TX_CONNECTION | 11.08 (26.31) **miss** | 10.63 (30.63) **miss** / 19.70 (39.52) **miss** | 0.95 (2.67) | 3.45 (9.84) / 3.48 (9.85) | 117 / 115 (48) |
| the first TMR_NO_RESP | 5.48 (47.98) | 14.19 (70.11) **miss** / 12.89 (70.11) **miss** | 0.86 (3.03) | 2.53 (13.06) / 1.14 (9.12) | 124 / 113 (35) |
| the second TMR_NO_RESP | 1.64 (21.79) | 4.43 (24.89) / 5.24 (24.89) | 1.19 (3.89) | 1.46 (12.60) / 0.54 (8.12) | 72 / 67 (14) |
| TMR_RETRY | 7.99 (46.72) | 27.14 (76.55) **over ceiling** / 26.21 (76.55) **over ceiling** | 0.19 (3.79) | 3.17 (16.68) / 3.15 (14.68) | 73 / 68 (14) |
| TMR_DELAY | 2.90 (44.04) | 5.69 (38.79) / 8.58 (38.80) | 1.94 (5.06) | 1.70 (9.80) / 1.08 (6.57) | 95 / 93 (35) |
| TMR_NO_TK | 4.57 (22.15) | 15.23 (75.59) **miss** / 5.43 (38.64) | 0.19 (2.31) | 3.63 (9.89) / 3.24 (11.86) | 74 / 93 (14) |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 10.37 (25.92) **miss** | 27.41 (41.44) **over ceiling** / 29.72 (41.44) **over ceiling** | 0.90 (2.79) | 3.45 (14.07) / 5.76 (14.07) | 104 / 129 (35) |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 25.17 (50.78) **over ceiling** | 45.45 (83.13) **over ceiling** / 47.73 (83.13) **over ceiling** | 0.35 (2.24) | 1.18 (11.76) / 3.46 (11.75) | 98 / 177 (29) |
| TMR_NO_ADP (H-DISC) | 1.91 (22.31) | 8.51 (37.51) / 5.66 (31.48) | 0.99 (3.04) | 4.84 (15.30) / 2.25 (11.98) | 95 / 67 (12) |

## aecp
| AECP path | 1x1 ms (bound) | 8x8 if0 / if1 ms (bound) | Accesses, 1x1 / 8x8 |
|---|---:|---:|---:|
| READ_DESCRIPTOR type 0, 312 B | 5.14 (6.28) | 6.17 (12.33) / 6.19 (12.34) | 124 / 125 |
| READ_DESCRIPTOR type 1, 106 B | 4.33 (5.47) | 6.09 (11.91) / 6.12 (11.93) | 73 / 80 |
| READ_DESCRIPTOR type 2, 148 B | 4.49 (5.63) | 6.21 (12.03) / 5.54 (11.36) | 83 / 121 |
| READ_DESCRIPTOR type 5, 146 B | 4.49 (5.63) | 6.94 (11.69) / - | 82 / 83 |
| READ_DESCRIPTOR type 6, 146 B | 5.01 (6.15) | 6.28 (12.10) / - | 89 / 90 |
| READ_DESCRIPTOR type 9, 102 B | 4.84 (5.98) | 5.38 (11.20) / - | 78 / 72 |
| READ_DESCRIPTOR type 10, 86 B | 4.79 (5.93) | 6.08 (11.50) / - | 74 / 69 |
| READ_DESCRIPTOR type 12, 72 B | 4.73 (5.87) | 5.30 (11.12) / - | 71 / 65 |
| READ_DESCRIPTOR type 13, 452 B | 6.21 (7.35) | 7.50 (12.92) / - | 166 / 160 |
| READ_DESCRIPTOR type 14, 20 B | 4.03 (5.17) | 5.77 (11.59) / - | 52 / 59 |
| READ_DESCRIPTOR type 15, 20 B | 4.02 (5.16) | 5.09 (10.91) / - | 51 / 52 |
| READ_DESCRIPTOR type 20, 90 B | 4.86 (6.01) | 6.23 (11.69) / - | 75 / 70 |
| READ_DESCRIPTOR type 26, 113 B | 4.95 (6.09) | 5.59 (11.41) / - | 81 / 75 |
| READ_DESCRIPTOR type 36, 82 B | 4.84 (5.98) | 6.26 (11.72) / - | 73 / 71 |
| entity_available | 4.49 (5.63) | 5.00 (11.16) / 5.77 (11.59) | 57 / 51 |
| get_avb_info | 4.51 (5.66) | 5.92 (11.35) / 5.21 (11.03) | 53 / 48 |
| get_configuration | 4.42 (5.56) | 14.82 (27.43) **miss** / 5.69 (11.10) | 53 / 60 |
| get_counters | 4.92 (6.06) | 6.57 (12.39) / 6.21 (12.03) | 86 / 80 |
| get_name | 4.69 (5.83) | 7.05 (12.87) / 5.21 (11.36) | 70 / 99 |
| lock_entity | 3.96 (5.41) | 8.32 (14.50) / 8.19 (14.64) | 66 / 73 |
| MVU GET_MILAN_INFO | 2.50 (3.64) | 3.52 (9.68) / 3.53 (9.35) | 50 / 52 |
| register_unsolicited | 2.48 (3.61) | 5.91 (11.72) / 4.87 (10.68) | 46 / 54 |
| SET_NAME | 5.76 (8.84) | 7.88 (15.08) / 8.39 (15.20) | 106 / 114 |
| unknown_command | 4.42 (5.56) | 5.65 (11.47) / 5.69 (11.50) | 53 / 54 |
| unlock_entity | 3.95 (5.40) | 5.61 (11.51) / 6.12 (12.56) | 65 / 66 |

## srp maap
| SRP and MAAP path | 1x1 ms (bound) | 8x8 if0 / if1 ms (bound) | Accesses, 1x1 / 8x8 |
|---|---:|---:|---:|
| SRP startup declarations (LINK_UP) | 4.44 (4.97) | 15.79 (18.01) **miss** / 13.25 (33.17) **miss** | 88 / 124 |
| SRP Listener Ready RX (registrar; the fixture grants no licence) | 2.77 (2.77) | 9.11 (12.34) / 8.33 (9.56) | 29 / 36 |
| SRP malformed MRPDU discard | 2.15 (2.15) | 7.70 (11.04) / 5.69 (9.17) | 35 / 36 |
| SRP Domain RX -> declarations (W = JoinTime 200 ms) | 4.93 (7.07) | 14.28 (20.31) / 8.17 (21.00) | 78 / 142 |
| MAAP first PROBE (LINK_UP) | 0.90 (4.97) | 18.49 (38.98) **miss** / 17.04 (39.82) **miss** | 88 / 178 |
| MAAP PROBE retransmission (the worse of two) | 1.86 (3.92) | 3.78 (10.89) / 2.96 (9.41) | 37 / 44 |
| MAAP last PROBE retransmission | 1.24 (4.23) | 3.92 (8.86) / 2.64 (9.41) | 64 / 65 |
| MAAP ANNOUNCE | 1.50 (4.23) | 4.17 (8.86) / 2.90 (9.41) | 64 / 65 |
| MAAP conflicting PROBE -> DEFEND | 0.71 (2.02) | 1.72 (8.05) / 1.97 (8.23) | 47 / 48 |

## backlog
| Backlog row ([`MAILBOX_SPLIT.md:753-758`](../../../docs/design/MAILBOX_SPLIT.md#acmp-service-latency)) | Desk bound, accesses IF=1 / IF=2 | A: 1x1 ms (bound) [records ahead] | A: 8x8 | B: 1x1 | B: 8x8 |
|---|---:|---:|---:|---:|---:|
| an event behind 15 others | 10,569 / 13,287 | 15.49 (29.11) **miss** [15 ahead] | 44.65 (73.70) **miss** [16 ahead] | 15.49 (29.11) **miss** [15 ahead] | 44.65 (73.70) **miss** [16 ahead] |
| an ACMP command behind a full acmp ring | 38,753 / 48,719 | 63.30 (70.05) **over ceiling** [11 ahead] | 108.71 (120.30) **over ceiling** [11 ahead] | 63.30 (70.05) **over ceiling** [11 ahead] | 108.71 (120.30) **over ceiling** [11 ahead] |
| an ENTITY_AVAILABLE behind the adp ring at its burst (observed) | 77,506 / 97,438 | 67.93 (81.83) **over ceiling** [7 ahead] | 83.51 (107.83) **over ceiling** [7 ahead] | 36.72 (47.10) **over ceiling** [7 ahead] | 55.79 (76.28) **over ceiling** [7 ahead] |
| the same, its bucket refilling up to the ring's room (observed) | - | 88.33 (107.65) **over ceiling** [4 ahead] | 118.81 (156.29) **over ceiling** [6 ahead] | - | - |
| a response with 7 frames owed ahead of it | 31,707 / 39,861 | 125.79 (129.81) **over ceiling** [7 ahead] | 151.92 (161.44) **over ceiling** [7 ahead] | 125.78 (129.80) **over ceiling** [7 ahead] | 151.92 (161.44) **over ceiling** [7 ahead] |
| the same, from the moment the room returns | - | 65.79 | 91.92 | 65.78 | 91.92 |

## admission
| Channel | Burst | Refill | Ring room, records of the load's frame | Offered at once | Bound? |
|---|---:|---:|---:|---:|---|
| adp | 8 | 1 per 10 ms | 11 (23 words each) | 8 | no: observed at the burst |
| aecp | 16 | 1 per 5 ms | 30 (17 words each) | 16 | no: observed at the burst |
| maap | 8 | 1 per 20 ms | 7 (17 words each) | 7 | yes: the ring is full |
| srp | 32 | 1 per 2 ms | 60 (17 words each) | 32 | no: observed at the burst |
| acmp | 16 | 1 per 5 ms | 12 (20 words each) | 12 | yes: the ring is full |

## population
| Arm, group | Composed population committed (records; events) | Composed maximum, CPU cycles (ms) |
|---|---|---:|
| A1 backlog | adp 8, acmp 12, aecp 16, maap 7, srp 32, GM 15, LINK 1 | 740,260 (14.81) |
| A1 backlog-adp | adp 8, acmp 12, aecp 16, maap 7, srp 32, GM 15 | 1,565,803 (31.32) |
| A1 backlog-adp-refill | adp 11, acmp 12, aecp 16, maap 7, srp 32, GM 15 | 1,531,355 (30.63) |
| A1 backlog-owed | adp 8, acmp 8, aecp 16, maap 7, srp 32, GM 15 | 582,677 (11.65) |
| A8 backlog | adp 8, acmp 12, aecp 16, maap 7, srp 32, GM 15, LINK 1 | 1,392,016 (27.84) |
| A8 backlog-adp | adp 8, acmp 12, aecp 16, maap 7, srp 32, GM 15 | 2,208,710 (44.17) |
| A8 backlog-adp-refill | adp 11, acmp 12, aecp 16, maap 7, srp 32, GM 15 | 2,209,308 (44.19) |
| A8 backlog-owed | adp 8, acmp 8, aecp 16, maap 7, srp 32, GM 15 | 1,111,719 (22.23) |
| B1 backlog | adp 8, acmp 12, aecp 16, maap 7, srp 32, GM 15, LINK 1 | 740,260 (14.81) |
| B1 backlog-adp | adp 8, acmp 12, aecp 16, maap 7, srp 32, GM 15 | 645,058 (12.90) |
| B1 backlog-owed | adp 8, acmp 8, aecp 16, maap 7, srp 32, GM 15 | 582,392 (11.65) |
| B8 backlog | adp 8, acmp 12, aecp 16, maap 7, srp 32, GM 15, LINK 1 | 1,392,016 (27.84) |
| B8 backlog-adp | adp 8, acmp 12, aecp 16, maap 7, srp 32, GM 15 | 1,111,647 (22.23) |
| B8 backlog-owed | adp 8, acmp 8, aecp 16, maap 7, srp 32, GM 15 | 1,111,719 (22.23) |

A1 backlog composed 740,260: `rt_memset` 278,637, `mbx` 141,995, `rt_memcpy` 66,719, `aecp` 41,029, `acmp` 36,377, `aecp_nvm` 20,254
A1 backlog-adp composed 1,565,803: `rt_memset` 984,728, `aecp` 173,531, `mbx` 127,547, `acmp` 49,350, `rt_memcpy` 46,964, `rt_lshrdi3` 34,340
A1 backlog-adp-refill composed 1,531,355: `rt_memset` 972,114, `aecp` 173,146, `mbx` 127,173, `acmp` 38,929, `rt_memcpy` 38,274, `rt_lshrdi3` 33,018
A1 backlog-owed composed 582,677: `rt_memset` 218,625, `mbx` 123,945, `rt_memcpy` 46,200, `aecp` 41,029, `acmp` 36,835, `aecp_nvm` 20,254
A1 worst backlog-adp 1,565,803: `rt_memset` 984,728, `aecp` 173,531, `mbx` 127,547, `acmp` 49,350, `rt_memcpy` 46,964, `rt_lshrdi3` 34,340
A8 backlog composed 1,392,016: `rt_memset` 477,042, `mbx` 134,267, `rt_memcpy` 132,197, `aecp` 111,084, `acmp` 89,857, `rt_mulsi3` 67,272
A8 backlog-adp composed 2,208,710: `rt_memset` 827,831, `mrp_mad` 429,626, `aecp` 350,539, `mbx` 150,636, `rt_memcpy` 140,364, `rt_memcmp` 42,336
A8 backlog-adp-refill composed 2,209,308: `rt_memset` 827,831, `mrp_mad` 429,626, `aecp` 350,539, `mbx` 150,636, `rt_memcpy` 140,364, `rt_memcmp` 42,336
A8 backlog-owed composed 1,111,719: `mrp_mad` 441,264, `rt_memcpy` 132,674, `mbx` 111,905, `rt_memcmp` 89,198, `aecp` 73,883, `rt_memset` 66,970
A8 worst acmp-notk 2,989,496: `rt_memset` 1,286,303, `mrp_mad` 429,626, `aecp` 331,743, `nvm_flash_litespi` 327,192, `rt_memcpy` 120,080, `mbx` 101,857
B1 backlog composed 740,260: `rt_memset` 278,637, `mbx` 141,995, `rt_memcpy` 66,719, `aecp` 41,029, `acmp` 36,377, `aecp_nvm` 20,254
B1 backlog-adp composed 645,058: `rt_memset` 348,630, `mbx` 86,439, `rt_memcpy` 39,270, `acmp` 38,720, `aecp` 33,537, `rt_lshrdi3` 21,950
B1 backlog-owed composed 582,392: `rt_memset` 218,625, `mbx` 123,945, `rt_memcpy` 46,200, `aecp` 41,029, `acmp` 36,835, `aecp_nvm` 20,254
B1 worst backlog 740,260: `rt_memset` 278,637, `mbx` 141,995, `rt_memcpy` 66,719, `aecp` 41,029, `acmp` 36,377, `aecp_nvm` 20,254
B8 backlog composed 1,392,016: `rt_memset` 477,042, `mbx` 134,267, `rt_memcpy` 132,197, `aecp` 111,084, `acmp` 89,857, `rt_mulsi3` 67,272
B8 backlog-adp composed 1,111,647: `mrp_mad` 441,264, `rt_memcpy` 132,674, `mbx` 111,905, `rt_memcmp` 89,198, `aecp` 73,883, `rt_memset` 66,970
B8 backlog-owed composed 1,111,719: `mrp_mad` 441,264, `rt_memcpy` 132,674, `mbx` 111,905, `rt_memcmp` 89,198, `aecp` 73,883, `rt_memset` 66,970
B8 worst acmp-notk 2,004,666: `mrp_mad` 473,950, `rt_memset` 361,053, `rt_memcpy` 244,102, `mbx` 119,790, `rt_mulsi3` 111,201, `rt_udivsi3` 89,954
