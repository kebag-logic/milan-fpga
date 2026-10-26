### 8x8

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 761,721 | 15.234 | 10 | 20 | MISS T_svc | 1,934,973 | 93 (14) | 0.889 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 271,282 | 5.426 | 10 | 20 | fits | 1,931,989 | 71 (14) | 0.889 |
| LINK_UP | `adp.link_up.if0` | 1,625,718 | 32.514 | 10 | 200 | MISS T_svc | 2,004,666 | 345 (11) | 0.865 |
| LINK_UP | `adp.link_up.if1` | 2,084,480 | 41.690 | 10 | 200 | MISS T_svc | 2,004,666 | 345 (11) | 0.865 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 132,204 | 2.644 | 10 | 200 | fits | 194,884 | 47 (39) | 0.866 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 184,969 | 3.699 | 10 | 200 | fits | 230,949 | 53 (39) | 0.869 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 53,169 | 1.063 | 10 | 200 | fits | 205,284 | 25 (11) | 0.868 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 68,695 | 1.374 | 10 | 200 | fits | 43,248 | 15 (11) | 0.886 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 924,464 | 18.489 | 10 | 50 | MISS T_svc | 1,048,452 | 178 | 0.864 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 189,196 | 3.784 | 10 | 50 | fits | 251,051 | 44 | 0.874 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 69,941 | 1.399 | 10 | 50 | fits | 214,829 | 38 | 0.872 |
| PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 195,752 | 3.915 | 10 | 50 | fits | 247,053 | 65 | 0.875 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 208,700 | 4.174 | 10 | 50 | fits | 247,053 | 65 | 0.875 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 85,813 | 1.716 | 10 | 50 | fits | 211,279 | 48 | 0.868 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 851,969 | 17.039 | 10 | 50 | MISS T_svc | 1,071,742 | 178 | 0.866 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 148,137 | 2.963 | 10 | 50 | fits | 216,431 | 37 | 0.870 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 83,279 | 1.666 | 10 | 50 | fits | 254,180 | 44 | 0.873 |
| PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 132,044 | 2.641 | 10 | 50 | fits | 286,163 | 71 | 0.875 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 144,992 | 2.900 | 10 | 50 | fits | 286,163 | 71 | 0.875 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 98,445 | 1.969 | 10 | 50 | fits | 213,312 | 48 | 0.866 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 709,672 | 14.193 | 10 | 20 | MISS T_svc | 1,296,146 | 113 (35) | 0.884 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 644,258 | 12.885 | 10 | 20 | MISS T_svc | 1,296,146 | 113 (35) | 0.884 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 221,590 | 4.432 | 10 | 20 | fits | 1,244,481 | 67 (14) | 0.884 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 261,885 | 5.238 | 10 | 20 | fits | 1,244,481 | 67 (14) | 0.884 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 1,356,847 | 27.137 | 10 | 20 | MISS ceiling | 1,237,282 | 68 (14) | 0.884 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 1,310,294 | 26.206 | 10 | 20 | MISS ceiling | 1,237,282 | 68 (14) | 0.884 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 284,715 | 5.694 | 10 | 20 | fits | 1,939,530 | 93 (35) | 0.889 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 428,855 | 8.577 | 10 | 20 | fits | 1,939,942 | 93 (35) | 0.889 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 789,405 | 15.788 | 10 | 18 | MISS T_svc | 900,485 | 124 | 0.860 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 662,320 | 13.246 | 10 | 18 | MISS T_svc | 610,130 | 160 | 0.855 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 455,724 | 9.114 | 10 | 18 | fits | 299,380 | 36 | 0.866 |
| malformed MRPDU discard | `srp.malformed.if0` | 384,759 | 7.695 | 10 | 18 | fits | 245,990 | 36 | 0.864 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 714,165 | 14.283 | 210 | 218 | fits | 780,248 | 142 | 0.850 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 416,377 | 8.328 | 10 | 18 | fits | 266,435 | 30 | 0.861 |
| malformed MRPDU discard | `srp.malformed.if1` | 284,721 | 5.694 | 10 | 18 | fits | 257,218 | 36 | 0.863 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 408,680 | 8.174 | 210 | 218 | fits | 449,780 | 39 | 0.857 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 2,272,459 | 45.449 | 10 | 20 | MISS ceiling | 1,699,407 | 177 (29) | 0.886 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 2,386,439 | 47.729 | 10 | 20 | MISS ceiling | 1,699,407 | 177 (29) | 0.886 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 1,370,524 | 27.410 | 10 | 20 | MISS ceiling | 2,072,158 | 129 (35) | 0.887 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 1,486,120 | 29.722 | 10 | 20 | MISS ceiling | 2,072,158 | 129 (35) | 0.887 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 425,632 | 8.513 | 10 | 20 | fits | 1,875,664 | 67 (12) | 0.871 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 283,246 | 5.665 | 10 | 20 | fits | 1,574,180 | 90 (12) | 0.888 |
| an event behind 15 others | `backlog.event.if0` | 2,025,714 | 40.514 | 10 | 200 | MISS T_svc | 1,302,022 | 308 | 0.876 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 5,099,106 | 101.982 | 10 | 20 | MISS ceiling | 765,335 | 254 | 0.877 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 4,946,262 | 98.925 | 10 | 20 | MISS ceiling | 291,832 | 38 | 0.869 |
| LINK_UP | `adp.link_up.if0` | 1,625,718 | 32.514 | 10 | 200 | MISS T_svc | 2,004,666 | 345 (11) | 0.865 |
| LINK_UP | `adp.link_up.if1` | 2,084,480 | 41.690 | 10 | 200 | MISS T_svc | 2,004,666 | 345 (11) | 0.865 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 132,204 | 2.644 | 10 | 200 | fits | 194,884 | 47 (39) | 0.866 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 184,969 | 3.699 | 10 | 200 | fits | 230,949 | 53 (39) | 0.869 |
| LINK_DOWN | `adp.link_down.if0` | 917,527 | 18.351 | 10 | 200 | MISS T_svc | 1,169,168 | 70 (9) | 0.876 |
| LINK_DOWN | `adp.link_down.if1` | 1,342,185 | 26.844 | 10 | 200 | MISS T_svc | 1,169,168 | 70 (9) | 0.876 |
| LINK_UP | `adp.link_up.if0` | 1,625,718 | 32.514 | 10 | 200 | MISS T_svc | 2,004,666 | 345 (11) | 0.865 |
| LINK_UP | `adp.link_up.if1` | 2,084,480 | 41.690 | 10 | 200 | MISS T_svc | 2,004,666 | 345 (11) | 0.865 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 132,204 | 2.644 | 10 | 200 | fits | 194,884 | 47 (39) | 0.866 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 184,969 | 3.699 | 10 | 200 | fits | 230,949 | 53 (39) | 0.869 |
| GM_CHANGE | `adp.gm_change.if0` | 118,927 | 2.379 | 10 | 200 | fits | 209,423 | 34 (11) | 0.867 |
| GM_CHANGE | `adp.gm_change.if1` | 125,077 | 2.502 | 10 | 200 | fits | 209,423 | 34 (11) | 0.867 |
| LINK_UP | `adp.link_up.if0` | 1,625,718 | 32.514 | 10 | 200 | MISS T_svc | 2,004,666 | 345 (11) | 0.865 |
| LINK_UP | `adp.link_up.if1` | 2,084,480 | 41.690 | 10 | 200 | MISS T_svc | 2,004,666 | 345 (11) | 0.865 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 132,204 | 2.644 | 10 | 200 | fits | 194,884 | 47 (39) | 0.866 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 184,969 | 3.699 | 10 | 200 | fits | 230,949 | 53 (39) | 0.869 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 128,423 | 2.568 | 10 | 200 | fits | 225,549 | 73 (31) | 0.867 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 142,798 | 2.856 | 10 | 200 | fits | 225,549 | 73 (31) | 0.867 |
| LINK_UP | `adp.link_up.if0` | 1,625,718 | 32.514 | 10 | 200 | MISS T_svc | 2,004,666 | 345 (11) | 0.865 |
| LINK_UP | `adp.link_up.if1` | 2,084,480 | 41.690 | 10 | 200 | MISS T_svc | 2,004,666 | 345 (11) | 0.865 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 132,204 | 2.644 | 10 | 200 | fits | 194,884 | 47 (39) | 0.866 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 184,969 | 3.699 | 10 | 200 | fits | 230,949 | 53 (39) | 0.869 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 128,423 | 2.568 | 10 | 200 | fits | 211,550 | 45 (31) | 0.867 |
| BIND_RX | `acmp.bind_rx.if0` | 225,669 | 4.513 | 10 | 20 | fits | 397,264 | 90 (77) | 0.870 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 970,162 | 19.403 | 10 | 20 | MISS T_svc | 1,756,026 | 102 (32) | 0.886 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 548,143 | 10.963 | 10 | 20 | MISS T_svc | 1,538,378 | 114 (47) | 0.886 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 337,377 | 6.748 | 10 | 20 | fits | 1,351,576 | 176 (50) | 0.884 |
| PROBE_TX | `acmp.probe_tx.if0` | 558,421 | 11.168 | 10 | 20 | MISS T_svc | 1,533,927 | 116 (48) | 0.886 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 533,518 | 10.670 | 10 | 20 | MISS T_svc | 1,533,135 | 115 (48) | 0.886 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 531,202 | 10.624 | 10 | 20 | MISS T_svc | 1,531,239 | 115 (48) | 0.886 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 531,375 | 10.627 | 10 | 20 | MISS T_svc | 1,531,412 | 115 (48) | 0.886 |
| BIND_RX | `acmp.bind_rx.if1` | 567,820 | 11.356 | 10 | 20 | MISS T_svc | 1,579,911 | 145 (77) | 0.885 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 799,519 | 15.990 | 10 | 20 | MISS T_svc | 1,960,887 | 97 (32) | 0.888 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 989,260 | 19.785 | 10 | 20 | MISS T_svc | 1,980,144 | 112 (47) | 0.888 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 990,219 | 19.804 | 10 | 20 | MISS T_svc | 2,004,171 | 115 (50) | 0.888 |
| PROBE_TX | `acmp.probe_tx.if1` | 1,050,781 | 21.016 | 10 | 20 | MISS ceiling | 2,722,461 | 330 (48) | 0.875 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 1,379,768 | 27.595 | 10 | 20 | MISS ceiling | 1,631,892 | 134 (48) | 0.887 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 1,009,034 | 20.181 | 10 | 20 | MISS ceiling | 1,629,266 | 134 (48) | 0.887 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 984,953 | 19.699 | 10 | 20 | MISS T_svc | 1,975,919 | 113 (48) | 0.889 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 295,637 | 5.913 | 10 | 24 | fits | 322,322 | 54 | 0.876 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 308,462 | 6.169 | 10 | 24 | fits | 419,415 | 125 | 0.881 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 304,685 | 6.094 | 10 | 24 | fits | 415,178 | 80 | 0.880 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 310,358 | 6.207 | 10 | 24 | fits | 420,854 | 121 | 0.880 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 347,097 | 6.942 | 10 | 24 | fits | 387,250 | 83 | 0.880 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 314,051 | 6.281 | 10 | 24 | fits | 424,778 | 90 | 0.880 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 269,182 | 5.384 | 10 | 24 | fits | 379,768 | 72 | 0.880 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 303,905 | 6.078 | 10 | 24 | fits | 378,116 | 69 | 0.880 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 264,885 | 5.298 | 10 | 24 | fits | 375,226 | 65 | 0.880 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 374,850 | 7.497 | 10 | 24 | fits | 448,860 | 160 | 0.882 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 288,349 | 5.767 | 10 | 24 | fits | 401,741 | 59 | 0.879 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 254,607 | 5.092 | 10 | 24 | fits | 366,939 | 52 | 0.879 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 311,494 | 6.230 | 10 | 24 | fits | 388,308 | 70 | 0.878 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 279,743 | 5.595 | 10 | 24 | fits | 392,458 | 75 | 0.879 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 313,215 | 6.264 | 10 | 24 | fits | 389,334 | 71 | 0.879 |
| get_configuration | `aecp.get_configuration.if0` | 741,103 | 14.822 | 10 | 24 | MISS T_svc | 429,227 | 60 | 0.880 |
| entity_available | `aecp.entity_available.if0` | 249,962 | 4.999 | 10 | 24 | fits | 360,902 | 51 | 0.880 |
| get_name | `aecp.get_name.if0` | 352,412 | 7.048 | 10 | 24 | fits | 463,357 | 99 | 0.881 |
| get_counters | `aecp.get_counters.if0` | 328,487 | 6.570 | 10 | 24 | fits | 383,452 | 80 | 0.881 |
| get_avb_info | `aecp.get_avb_info.if0` | 295,784 | 5.916 | 10 | 24 | fits | 370,724 | 48 | 0.878 |
| unknown_command | `aecp.unknown_command.if0` | 282,639 | 5.653 | 10 | 24 | fits | 393,659 | 54 | 0.880 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 175,890 | 3.518 | 10 | 24 | fits | 287,415 | 52 | 0.875 |
| set_name | `aecp.set_name.if0` | 394,061 | 7.881 | 10 | 24 | fits | 574,214 | 114 | 0.872 |
| lock_entity | `aecp.lock_entity.if0` | 415,903 | 8.318 | 10 | 24 | fits | 414,858 | 73 | 0.880 |
| unlock_entity | `aecp.unlock_entity.if0` | 280,323 | 5.606 | 10 | 24 | fits | 377,791 | 66 | 0.879 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 243,277 | 4.866 | 10 | 24 | fits | 322,957 | 52 | 0.876 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 309,523 | 6.190 | 10 | 24 | fits | 419,147 | 123 | 0.881 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 305,789 | 6.116 | 10 | 24 | fits | 415,313 | 78 | 0.881 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 276,870 | 5.537 | 10 | 24 | fits | 386,540 | 82 | 0.880 |
| get_configuration | `aecp.get_configuration.if1` | 284,520 | 5.690 | 10 | 24 | fits | 357,532 | 46 | 0.879 |
| entity_available | `aecp.entity_available.if1` | 288,329 | 5.767 | 10 | 24 | fits | 397,872 | 56 | 0.880 |
| get_name | `aecp.get_name.if1` | 260,314 | 5.206 | 10 | 24 | fits | 370,756 | 62 | 0.880 |
| get_counters | `aecp.get_counters.if1` | 310,723 | 6.214 | 10 | 24 | fits | 420,382 | 85 | 0.881 |
| get_avb_info | `aecp.get_avb_info.if1` | 260,573 | 5.211 | 10 | 24 | fits | 370,125 | 45 | 0.879 |
| unknown_command | `aecp.unknown_command.if1` | 284,265 | 5.685 | 10 | 24 | fits | 394,012 | 52 | 0.880 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 176,594 | 3.532 | 10 | 24 | fits | 286,816 | 49 | 0.875 |
| set_name | `aecp.set_name.if1` | 396,667 | 7.933 | 10 | 24 | fits | 578,124 | 147 | 0.870 |
| lock_entity | `aecp.lock_entity.if1` | 234,168 | 4.683 | 10 | 24 | fits | 391,234 | 85 | 0.880 |
| unlock_entity | `aecp.unlock_entity.if1` | 342,954 | 6.859 | 10 | 24 | fits | 390,914 | 85 | 0.879 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 2,431,624 | 48.632 | 10 | 20 | MISS ceiling | 1,522,182 | 126 | 0.886 |
