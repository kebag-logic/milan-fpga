### 8x8

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 181,521 | 3.630 | 10 | 20 | fits | 294,767 | 42 (14) | 0.865 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 161,842 | 3.237 | 10 | 20 | fits | 318,783 | 26 (14) | 0.865 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 126,540 | 2.531 | 10 | 20 | fits | 456,042 | 80 (35) | 0.868 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 56,859 | 1.137 | 10 | 20 | fits | 456,042 | 80 (35) | 0.868 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 72,899 | 1.458 | 10 | 20 | fits | 405,764 | 34 (14) | 0.864 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 27,167 | 0.543 | 10 | 20 | fits | 405,764 | 34 (14) | 0.864 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 158,315 | 3.166 | 10 | 20 | fits | 524,839 | 67 (14) | 0.866 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 157,495 | 3.150 | 10 | 20 | fits | 524,839 | 67 (14) | 0.866 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 85,229 | 1.705 | 10 | 20 | fits | 290,983 | 42 (35) | 0.865 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 54,075 | 1.081 | 10 | 20 | fits | 328,592 | 48 (35) | 0.868 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 58,843 | 1.177 | 10 | 20 | fits | 388,394 | 60 (29) | 0.864 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 172,823 | 3.456 | 10 | 20 | fits | 388,394 | 60 (29) | 0.864 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 172,491 | 3.450 | 10 | 20 | fits | 428,483 | 78 (35) | 0.865 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 288,087 | 5.762 | 10 | 20 | fits | 428,483 | 78 (35) | 0.865 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 242,152 | 4.843 | 10 | 20 | fits | 568,076 | 32 (12) | 0.845 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 112,552 | 2.251 | 10 | 20 | fits | 364,703 | 48 (12) | 0.869 |
| an event behind 15 others | `backlog.event.if0` | 2,025,714 | 40.514 | 10 | 200 | MISS T_svc | 1,302,022 | 308 | 0.876 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 5,099,106 | 101.982 | 10 | 20 | MISS ceiling | 765,335 | 254 | 0.877 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 4,946,262 | 98.925 | 10 | 20 | MISS ceiling | 291,832 | 38 | 0.869 |
| BIND_RX | `acmp.bind_rx.if0` | 225,669 | 4.513 | 10 | 20 | fits | 397,264 | 90 (77) | 0.870 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 147,378 | 2.948 | 10 | 20 | fits | 282,755 | 39 (32) | 0.861 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 207,476 | 4.150 | 10 | 20 | fits | 337,929 | 60 (47) | 0.867 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 199,690 | 3.994 | 10 | 20 | fits | 323,250 | 56 (50) | 0.863 |
| PROBE_TX | `acmp.probe_tx.if0` | 76,866 | 1.537 | 10 | 20 | fits | 297,377 | 56 (48) | 0.865 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 176,130 | 3.523 | 10 | 20 | fits | 296,655 | 54 (48) | 0.865 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 47,967 | 0.959 | 10 | 20 | fits | 330,822 | 61 (48) | 0.867 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 172,554 | 3.451 | 10 | 20 | fits | 294,571 | 55 (48) | 0.865 |
| BIND_RX | `acmp.bind_rx.if1` | 211,034 | 4.221 | 10 | 20 | fits | 344,430 | 84 (77) | 0.865 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 170,283 | 3.406 | 10 | 20 | fits | 319,560 | 46 (32) | 0.864 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 173,213 | 3.464 | 10 | 20 | fits | 302,084 | 55 (47) | 0.865 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 197,637 | 3.953 | 10 | 20 | fits | 324,091 | 57 (50) | 0.863 |
| PROBE_TX | `acmp.probe_tx.if1` | 205,561 | 4.111 | 10 | 20 | fits | 333,072 | 63 (48) | 0.866 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 176,387 | 3.528 | 10 | 20 | fits | 297,390 | 56 (48) | 0.864 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 209,564 | 4.191 | 10 | 20 | fits | 330,792 | 62 (48) | 0.867 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 174,190 | 3.484 | 10 | 20 | fits | 294,911 | 56 (48) | 0.864 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 763,828 | 15.277 | 10 | 20 | MISS T_svc | 285,313 | 65 | 0.863 |
