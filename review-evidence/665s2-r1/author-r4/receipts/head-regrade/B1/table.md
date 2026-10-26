### 1x1

18 of 44 paths and 41 of 68 probe instances miss T_svc.

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
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 8.569 (9.778) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 8.746 (10.002) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 14.804 (15.954) | MISS T_svc | 0 acmp | 1 | 1 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 8.230 (9.381) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 8.577 (9.788) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 8.738 (9.997) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 8.047 (8.919) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 9.233 (10.025) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 7.786 (8.935) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 11.332 (12.980) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 7.943 (8.780) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 11.681 (12.826) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 8.204 (9.352) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 63.304 (70.047) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 36.721 (47.102) | MISS ceiling | 7 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 15.487 (29.108) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 126.281 (130.302) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 363.978 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 14.761 | MISS T_svc | 0 acmp | 3 | 3 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 69.994 | MISS ceiling | 11 acmp | 3 | 3 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 14.803 | MISS T_svc | 0 adp | 3 | 3 |
| ADP record released under the composed load, last | 0 | `backlog.service.adp.last.if0` (backlog) | 51.028 | MISS T_svc | 7 adp | 3 | 3 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 14.796 | MISS T_svc | 0 aecp | 3 | 3 |
| AECP record released under the composed load, last | 0 | `backlog-adp.service.aecp.last.if0` (backlog-adp) | 155.127 | MISS ceiling | 15 aecp | 3 | 3 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 14.786 | MISS T_svc | 0 maap | 3 | 3 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 51.013 | MISS ceiling | 6 maap | 3 | 3 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 84.105 | MISS ceiling | 0 srp | 3 | 3 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 186.483 | MISS ceiling | 31 srp | 3 | 3 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 162.905 | 27 | 740,260 (14.805) | yes | - |
| backlog-adp | 195.371 | 27 | 645,058 (12.901) | yes | - |
| backlog-owed | 364.029 | 44 | 582,392 (11.648) | yes | - |

Composed maximum over the 3 backlog windows: 740,260 CPU cycles (14.805 ms), backlog.
Over the windows that released their whole load only: 740,260 (14.805 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 9,557 | 0.191 | 10 | 20 | fits | 115,635 | 20 (14) | 0.858 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 43,051 | 0.861 | 10 | 20 | fits | 151,395 | 47 (35) | 0.875 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 59,659 | 1.193 | 10 | 20 | fits | 102,124 | 18 (14) | 0.861 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 9,538 | 0.191 | 10 | 20 | fits | 96,294 | 19 (14) | 0.861 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 97,074 | 1.941 | 10 | 20 | fits | 126,057 | 41 (35) | 0.867 |
| an event behind 15 others | `backlog.event.if0` | 774,336 | 15.487 | 10 | 200 | MISS T_svc | 715,146 | 355 | 0.879 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 3,165,198 | 63.304 | 10 | 20 | MISS ceiling | 475,216 | 216 | 0.884 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 740,156 | 14.803 | 10 | 200 | MISS T_svc | 740,260 | 388 | 0.879 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 2,551,405 | 51.028 | 10 | 200 | MISS T_svc | 514,464 | 284 | 0.883 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 738,027 | 14.761 | 10 | 20 | MISS T_svc | 740,260 | 388 | 0.879 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 3,499,713 | 69.994 | 10 | 20 | MISS ceiling | 475,216 | 216 | 0.884 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 739,819 | 14.796 | 10 | 24 | MISS T_svc | 740,260 | 388 | 0.879 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 6,959,549 | 139.191 | 10 | 24 | MISS ceiling | 316,300 | 123 | 0.888 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 739,299 | 14.786 | 10 | 50 | MISS T_svc | 740,260 | 388 | 0.879 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 2,550,657 | 51.013 | 10 | 50 | MISS ceiling | 514,464 | 284 | 0.883 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 4,205,274 | 84.105 | 10 | 18 | MISS ceiling | 361,100 | 168 | 0.889 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 7,945,599 | 158.912 | 10 | 18 | MISS ceiling | 75,111 | 29 | 0.869 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 1,836,053 | 36.721 | 10 | 20 | MISS ceiling | 574,772 | 310 | 0.880 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 597,087 | 11.942 | 10 | 200 | MISS T_svc | 599,428 | 382 | 0.881 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,352,464 | 47.049 | 10 | 200 | MISS T_svc | 574,772 | 310 | 0.880 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 597,543 | 11.951 | 10 | 20 | MISS T_svc | 599,428 | 382 | 0.881 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 3,382,446 | 67.649 | 10 | 20 | MISS ceiling | 384,576 | 147 | 0.872 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 599,336 | 11.987 | 10 | 24 | MISS T_svc | 599,428 | 382 | 0.881 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 7,756,357 | 155.127 | 10 | 24 | MISS ceiling | 319,511 | 123 | 0.887 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 598,816 | 11.976 | 10 | 50 | MISS T_svc | 599,428 | 382 | 0.881 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,354,302 | 47.086 | 10 | 50 | MISS T_svc | 574,772 | 310 | 0.880 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 3,383,903 | 67.678 | 10 | 18 | MISS ceiling | 384,576 | 147 | 0.872 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 9,324,175 | 186.483 | 10 | 18 | MISS ceiling | 118,180 | 29 | 0.861 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,314,064 | 126.281 | 10 | 20 | MISS ceiling | 475,541 | 190 | 0.881 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,198,917 | 363.978 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,198,880 | 363.978 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,198,842 | 363.977 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,198,805 | 363.976 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 594,280 | 11.886 | 10 | 200 | MISS T_svc | 562,433 | 340 | 0.877 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 2,249,630 | 44.993 | 10 | 200 | MISS T_svc | 520,132 | 260 | 0.881 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 592,150 | 11.843 | 10 | 20 | MISS T_svc | 562,433 | 340 | 0.877 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 2,982,310 | 59.646 | 10 | 20 | MISS ceiling | 331,352 | 80 | 0.880 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 593,943 | 11.879 | 10 | 24 | MISS T_svc | 562,433 | 340 | 0.877 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 7,663,744 | 153.275 | 10 | 24 | MISS ceiling | 319,511 | 123 | 0.887 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 593,423 | 11.868 | 10 | 50 | MISS T_svc | 562,433 | 340 | 0.877 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 2,248,883 | 44.978 | 10 | 50 | MISS T_svc | 520,132 | 260 | 0.881 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 3,298,095 | 65.962 | 10 | 18 | MISS ceiling | 314,328 | 170 | 0.875 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 9,133,970 | 182.679 | 10 | 18 | MISS ceiling | 146,399 | 35 | 0.871 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 17,588 | 0.352 | 10 | 20 | fits | 112,052 | 35 (29) | 0.863 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 45,099 | 0.902 | 10 | 20 | fits | 139,538 | 47 (35) | 0.870 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 49,644 | 0.993 | 10 | 20 | fits | 151,781 | 47 (12) | 0.875 |
| set_name | `aecp_fanout.set_name.if0` | 566,621 | 11.332 | 10 | 24 | MISS T_svc | 649,006 | 601 | 0.887 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 402,339 | 8.047 | 10 | 24 | fits | 445,942 | 316 | 0.880 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 388,673 | 7.773 | 10 | 24 | fits | 446,073 | 299 | 0.883 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 389,281 | 7.786 | 10 | 24 | fits | 446,753 | 299 | 0.883 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 428,827 | 8.577 | 10 | 24 | fits | 489,414 | 350 | 0.880 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 428,446 | 8.569 | 10 | 24 | fits | 488,907 | 350 | 0.880 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 436,891 | 8.738 | 10 | 24 | fits | 499,844 | 350 | 0.880 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 437,297 | 8.746 | 10 | 24 | fits | 500,124 | 350 | 0.879 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 397,147 | 7.943 | 10 | 24 | fits | 438,980 | 316 | 0.880 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 461,671 | 9.233 | 10 | 24 | fits | 501,232 | 306 | 0.879 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 584,038 | 11.681 | 10 | 24 | MISS T_svc | 641,310 | 655 | 0.888 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 411,500 | 8.230 | 10 | 24 | fits | 469,037 | 350 | 0.885 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 410,195 | 8.204 | 10 | 24 | fits | 467,595 | 350 | 0.885 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 740,205 | 14.804 | 10 | 24 | MISS T_svc | 386,020 | 478 | 0.888 |
| BIND_RX | `acmp.bind_rx.if0` | 81,248 | 1.625 | 10 | 20 | fits | 197,790 | 82 (77) | 0.874 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 18,431 | 0.369 | 10 | 20 | fits | 122,864 | 38 (32) | 0.859 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 47,813 | 0.956 | 10 | 20 | fits | 139,688 | 52 (47) | 0.867 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 53,405 | 1.068 | 10 | 20 | fits | 161,042 | 56 (50) | 0.862 |
| PROBE_TX | `acmp.probe_tx.if0` | 75,630 | 1.513 | 10 | 20 | fits | 162,260 | 61 (48) | 0.873 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 49,967 | 0.999 | 10 | 20 | fits | 136,177 | 54 (48) | 0.866 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 47,536 | 0.951 | 10 | 20 | fits | 133,746 | 54 (48) | 0.866 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 47,488 | 0.950 | 10 | 20 | fits | 133,698 | 54 (48) | 0.866 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
