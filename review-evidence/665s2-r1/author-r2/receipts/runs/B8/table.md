### 8x8

4 of 36 paths and 4 of 36 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 4.513 (13.219) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 4.221 (12.588) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.959 (6.616) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 4.191 (12.339) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 3.450 (14.068) | fits | 0 adp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 5.762 (14.067) | fits | 1 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 1.177 (11.756) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 3.456 (11.755) | fits | 1 adp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 4.150 (12.468) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 3.464 (10.045) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 3.451 (9.840) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 3.484 (9.845) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 3.523 (11.648) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 3.528 (9.889) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 1.537 (9.893) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 4.111 (12.260) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 2.948 (11.409) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 3.406 (11.866) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 1.705 (9.796) | fits | 0 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 1.081 (6.572) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 4.843 (15.303) | fits | 1 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 2.251 (11.977) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 2.531 (13.065) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 1.137 (9.121) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 1.458 (12.599) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 0.543 (8.115) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 3.630 (9.885) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 3.237 (11.855) | fits | 1 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 3.166 (16.684) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 3.150 (14.684) | fits | 1 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 3.994 (10.462) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 3.953 (12.552) | fits | 0 acmp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 108.712 (120.299) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 55.792 (76.284) | MISS ceiling | 7 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 44.651 (73.699) | MISS T_svc | 16 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 151.916 (161.437) | MISS ceiling | 7 acmp | 1 | 1 |

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
| an event behind 15 others | `backlog.event.if0` | 2,232,539 | 44.651 | 10 | 200 | MISS T_svc | 1,392,016 | 364 | 0.877 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 5,435,592 | 108.712 | 10 | 20 | MISS ceiling | 732,610 | 217 | 0.877 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 2,789,577 | 55.792 | 10 | 20 | MISS ceiling | 917,291 | 311 | 0.874 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 7,595,781 | 151.916 | 10 | 20 | MISS ceiling | 587,791 | 152 | 0.878 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 58,843 | 1.177 | 10 | 20 | fits | 388,394 | 60 (29) | 0.864 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 172,823 | 3.456 | 10 | 20 | fits | 388,394 | 60 (29) | 0.864 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 172,491 | 3.450 | 10 | 20 | fits | 428,483 | 78 (35) | 0.865 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 288,087 | 5.762 | 10 | 20 | fits | 428,483 | 78 (35) | 0.865 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 242,152 | 4.843 | 10 | 20 | fits | 568,076 | 32 (12) | 0.845 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 112,552 | 2.251 | 10 | 20 | fits | 364,703 | 48 (12) | 0.869 |
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

Bounded waits that timed out (the probe is graded on what the log holds):

- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
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
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
