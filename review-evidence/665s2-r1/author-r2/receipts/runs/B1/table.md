### 1x1

4 of 20 paths and 4 of 20 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 1.625 (3.956) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.951 (2.675) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.902 (2.791) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.352 (2.241) | fits | 0 adp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.956 (2.794) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.950 (2.674) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.999 (2.724) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 1.513 (3.245) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.369 (2.457) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 1.941 (5.065) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.993 (3.036) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.861 (3.028) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 1.193 (3.888) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.191 (2.313) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.191 (3.789) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 1.068 (3.221) | fits | 0 acmp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 63.304 (70.047) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 36.721 (47.102) | MISS ceiling | 7 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 15.487 (29.108) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 125.782 (129.803) | MISS ceiling | 7 acmp | 1 | 1 |

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 9,557 | 0.191 | 10 | 20 | fits | 115,635 | 20 (14) | 0.858 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 43,051 | 0.861 | 10 | 20 | fits | 151,395 | 47 (35) | 0.875 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 59,659 | 1.193 | 10 | 20 | fits | 102,124 | 18 (14) | 0.861 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 9,538 | 0.191 | 10 | 20 | fits | 96,294 | 19 (14) | 0.861 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 97,074 | 1.941 | 10 | 20 | fits | 126,057 | 41 (35) | 0.867 |
| an event behind 15 others | `backlog.event.if0` | 774,336 | 15.487 | 10 | 200 | MISS T_svc | 715,146 | 355 | 0.879 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 3,165,198 | 63.304 | 10 | 20 | MISS ceiling | 475,216 | 216 | 0.884 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 1,836,053 | 36.721 | 10 | 20 | MISS ceiling | 574,772 | 310 | 0.880 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,289,099 | 125.782 | 10 | 20 | MISS ceiling | 475,662 | 190 | 0.881 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 17,588 | 0.352 | 10 | 20 | fits | 112,052 | 35 (29) | 0.863 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 45,099 | 0.902 | 10 | 20 | fits | 139,538 | 47 (35) | 0.870 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 49,644 | 0.993 | 10 | 20 | fits | 151,781 | 47 (12) | 0.875 |
| BIND_RX | `acmp.bind_rx.if0` | 81,248 | 1.625 | 10 | 20 | fits | 197,790 | 82 (77) | 0.874 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 18,431 | 0.369 | 10 | 20 | fits | 122,864 | 38 (32) | 0.859 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 47,813 | 0.956 | 10 | 20 | fits | 139,688 | 52 (47) | 0.867 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 53,405 | 1.068 | 10 | 20 | fits | 161,042 | 56 (50) | 0.862 |
| PROBE_TX | `acmp.probe_tx.if0` | 75,630 | 1.513 | 10 | 20 | fits | 162,260 | 61 (48) | 0.873 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 49,967 | 0.999 | 10 | 20 | fits | 136,177 | 54 (48) | 0.866 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 47,536 | 0.951 | 10 | 20 | fits | 133,746 | 54 (48) | 0.866 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 47,488 | 0.950 | 10 | 20 | fits | 133,698 | 54 (48) | 0.866 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
