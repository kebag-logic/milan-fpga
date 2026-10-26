### 1x1

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 9,557 | 0.191 | 10 | 20 | fits | 115,635 | 20 (14) | 0.858 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 43,051 | 0.861 | 10 | 20 | fits | 151,395 | 47 (35) | 0.875 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 59,659 | 1.193 | 10 | 20 | fits | 102,124 | 18 (14) | 0.861 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 9,538 | 0.191 | 10 | 20 | fits | 96,294 | 19 (14) | 0.861 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 97,074 | 1.941 | 10 | 20 | fits | 126,057 | 41 (35) | 0.867 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 17,588 | 0.352 | 10 | 20 | fits | 112,052 | 35 (29) | 0.863 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 45,099 | 0.902 | 10 | 20 | fits | 139,538 | 47 (35) | 0.870 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 49,644 | 0.993 | 10 | 20 | fits | 151,781 | 47 (12) | 0.875 |
| an event behind 15 others | `backlog.event.if0` | 706,103 | 14.122 | 10 | 200 | MISS T_svc | 685,184 | 318 | 0.879 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 3,017,792 | 60.356 | 10 | 20 | MISS ceiling | 474,015 | 216 | 0.884 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 3,789,005 | 75.780 | 10 | 20 | MISS ceiling | 120,328 | 37 | 0.878 |
| BIND_RX | `acmp.bind_rx.if0` | 81,248 | 1.625 | 10 | 20 | fits | 197,790 | 82 (77) | 0.874 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 18,431 | 0.369 | 10 | 20 | fits | 122,864 | 38 (32) | 0.859 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 47,813 | 0.956 | 10 | 20 | fits | 139,688 | 52 (47) | 0.867 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 53,405 | 1.068 | 10 | 20 | fits | 161,042 | 56 (50) | 0.862 |
| PROBE_TX | `acmp.probe_tx.if0` | 75,630 | 1.513 | 10 | 20 | fits | 162,260 | 61 (48) | 0.873 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 49,967 | 0.999 | 10 | 20 | fits | 136,177 | 54 (48) | 0.866 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 47,536 | 0.951 | 10 | 20 | fits | 133,746 | 54 (48) | 0.866 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 47,488 | 0.950 | 10 | 20 | fits | 133,698 | 54 (48) | 0.866 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 395,021 | 7.900 | 10 | 20 | fits | 125,726 | 65 | 0.862 |
