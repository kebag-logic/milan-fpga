### 1x1

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
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 721,092 | 14.422 | 10 | 20 | MISS T_svc | 1,126,582 | 95 (29) | 0.892 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 518,648 | 10.373 | 10 | 20 | MISS T_svc | 1,295,856 | 104 (35) | 0.891 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 95,524 | 1.910 | 10 | 20 | fits | 1,115,462 | 95 (12) | 0.891 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 45,163 | 0.903 | 10 | 50 | fits | 248,452 | 88 | 0.886 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 77,716 | 1.554 | 10 | 50 | fits | 104,332 | 37 | 0.876 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 93,164 | 1.863 | 10 | 50 | fits | 103,754 | 37 | 0.875 |
| PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 62,042 | 1.241 | 10 | 50 | fits | 135,183 | 64 | 0.881 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 74,970 | 1.499 | 10 | 50 | fits | 135,183 | 64 | 0.881 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 35,338 | 0.707 | 10 | 50 | fits | 100,762 | 47 | 0.868 |
| an event behind 15 others | `backlog.event.if0` | 706,103 | 14.122 | 10 | 200 | MISS T_svc | 685,184 | 318 | 0.879 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 3,017,704 | 60.354 | 10 | 20 | MISS ceiling | 474,075 | 216 | 0.884 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 3,787,822 | 75.756 | 10 | 20 | MISS ceiling | 120,304 | 37 | 0.878 |
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
| set_name | `aecp.set_name.if0` | 260,812 | 5.216 | 10 | 24 | fits | 345,233 | 106 | 0.882 |
| lock_entity | `aecp.lock_entity.if0` | 197,776 | 3.956 | 10 | 24 | fits | 270,477 | 66 | 0.885 |
| unlock_entity | `aecp.unlock_entity.if0` | 197,404 | 3.948 | 10 | 24 | fits | 270,094 | 65 | 0.885 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 2,194,964 | 43.899 | 10 | 20 | MISS ceiling | 1,150,413 | 160 | 0.890 |
| LINK_UP | `fixture.link_up.if0` | 5,281 | 0.106 | 10 | 200 | fits | 248,452 | 88 (11) | 0.886 |
| malformed MRPDU discard | `fixture.malformed.if0` | 107,473 | 2.149 | 10 | 18 | fits | 107,505 | 35 | 0.871 |
| SET_NAME | `fixture.set_name.if0` | 260,812 | 5.216 | 10 | 24 | fits | 344,462 | 106 | 0.882 |
| LINK_DOWN | `fixture.link_down.if0` | 3,917 | 0.078 | 10 | 200 | fits | 273,504 | 33 (9) | 0.878 |
| BIND_RX | `fixture.bind_rx.if0` | 81,248 | 1.625 | 10 | 20 | fits | 179,721 | 82 (77) | 0.868 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 282,292 | 5.646 | 10 | 20 | fits | 1,151,413 | 124 (35) | 0.890 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 1,258,586 | 25.172 | 10 | 20 | MISS ceiling | 1,292,122 | 98 (29) | 0.892 |
