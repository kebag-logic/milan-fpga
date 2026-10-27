### 1x1

10 of 44 paths and 25 of 68 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.973 (2.454) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.580 (1.718) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.289 (1.524) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.260 (1.492) | fits | 0 adp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.586 (1.793) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.578 (1.715) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.609 (1.747) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.609 (1.755) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.290 (1.647) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 1.109 (3.491) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.486 (2.565) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 1.077 (3.155) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.159 (1.641) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.436 (2.770) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.737 (2.508) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.970 (2.395) | fits | 0 acmp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 4.896 (5.694) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 4.997 (5.822) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 8.695 (9.466) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 4.644 (5.413) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 4.888 (5.686) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 4.990 (5.816) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 4.581 (5.184) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 4.972 (5.529) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 4.428 (5.197) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 6.727 (7.748) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 4.522 (5.105) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 6.617 (7.378) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 4.640 (5.408) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 36.407 (40.217) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 22.210 (29.596) | MISS ceiling | 7 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 9.023 (16.967) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 94.027 (96.469) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 363.070 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 8.565 | fits | 0 acmp | 3 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 40.732 | MISS ceiling | 11 acmp | 3 | 3 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 8.607 | fits | 0 adp | 3 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 29.543 | MISS T_svc | 7 adp | 3 | 3 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 8.601 | fits | 0 aecp | 3 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 106.924 | MISS ceiling | 15 aecp | 3 | 3 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 8.590 | fits | 0 maap | 3 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 29.580 | MISS T_svc | 6 maap | 3 | 3 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 23.693 | MISS ceiling | 0 srp | 3 | 3 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 104.822 | MISS ceiling | 31 srp | 3 | 3 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 90.170 | 23 | 430,466 (8.609) | yes | - |
| backlog-adp | 107.670 | 21 | 425,420 (8.508) | yes | - |
| backlog-owed | 363.121 | 54 | 373,288 (7.466) | yes | - |

Composed maximum over 3 of 4 backlog windows, a partial figure (backlog-adp-refill not run): 430,466 CPU cycles (8.609 ms), backlog.
Over the windows that released their whole load only: 430,466 (8.609 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 21,813 | 0.436 | 10 | 20 | fits | 77,481 | 20 (14) | 0.095 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 53,830 | 1.077 | 10 | 20 | fits | 94,523 | 47 (35) | 0.092 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 7,933 | 0.159 | 10 | 20 | fits | 82,045 | 24 (14) | 0.099 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 36,859 | 0.737 | 10 | 20 | fits | 64,231 | 19 (14) | 0.093 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 55,450 | 1.109 | 10 | 20 | fits | 95,355 | 47 (35) | 0.093 |
| an event behind 15 others | `backlog.event.if0` | 451,167 | 9.023 | 10 | 200 | fits | 417,903 | 355 | 0.066 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 1,820,346 | 36.407 | 10 | 20 | MISS ceiling | 256,237 | 210 | 0.053 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 430,362 | 8.607 | 10 | 200 | fits | 430,466 | 388 | 0.064 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 1,469,718 | 29.394 | 10 | 200 | MISS T_svc | 284,311 | 278 | 0.062 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 428,233 | 8.565 | 10 | 20 | fits | 430,466 | 388 | 0.064 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 2,008,191 | 40.164 | 10 | 20 | MISS ceiling | 256,237 | 210 | 0.053 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 430,025 | 8.601 | 10 | 24 | fits | 430,466 | 388 | 0.064 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 3,939,424 | 78.788 | 10 | 24 | MISS ceiling | 177,640 | 123 | 0.045 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 429,505 | 8.590 | 10 | 50 | fits | 430,466 | 388 | 0.064 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 1,468,970 | 29.379 | 10 | 50 | MISS T_svc | 284,311 | 278 | 0.062 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 1,184,627 | 23.693 | 10 | 18 | MISS ceiling | 337,446 | 347 | 0.073 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 4,373,676 | 87.474 | 10 | 18 | MISS ceiling | 72,773 | 53 | 0.114 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 1,110,482 | 22.210 | 10 | 20 | MISS ceiling | 406,340 | 349 | 0.077 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 347,321 | 6.946 | 10 | 200 | fits | 349,662 | 382 | 0.068 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 1,477,147 | 29.543 | 10 | 200 | MISS T_svc | 406,340 | 349 | 0.077 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 347,777 | 6.956 | 10 | 20 | fits | 349,662 | 382 | 0.068 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 2,036,621 | 40.732 | 10 | 20 | MISS ceiling | 133,706 | 96 | 0.078 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 349,570 | 6.991 | 10 | 24 | fits | 349,662 | 382 | 0.068 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 4,829,159 | 96.583 | 10 | 24 | MISS ceiling | 264,475 | 168 | 0.072 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 349,050 | 6.981 | 10 | 50 | fits | 349,662 | 382 | 0.068 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 1,478,985 | 29.580 | 10 | 50 | MISS T_svc | 406,340 | 349 | 0.077 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 1,072,612 | 21.452 | 10 | 18 | MISS ceiling | 383,604 | 360 | 0.076 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 5,241,082 | 104.822 | 10 | 18 | MISS ceiling | 81,995 | 29 | 0.109 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 4,701,374 | 94.027 | 10 | 20 | MISS ceiling | 214,702 | 152 | 0.054 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,153,519 | 363.070 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,153,481 | 363.070 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,153,444 | 363.069 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,153,406 | 363.068 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 356,909 | 7.138 | 10 | 200 | fits | 329,621 | 340 | 0.065 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 1,427,530 | 28.551 | 10 | 200 | MISS T_svc | 373,288 | 299 | 0.076 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 354,780 | 7.096 | 10 | 20 | fits | 329,621 | 340 | 0.065 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 1,905,674 | 38.113 | 10 | 20 | MISS ceiling | 261,588 | 119 | 0.083 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 356,572 | 7.131 | 10 | 24 | fits | 329,621 | 340 | 0.065 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 5,346,224 | 106.924 | 10 | 24 | MISS ceiling | 180,390 | 124 | 0.045 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 356,052 | 7.121 | 10 | 50 | fits | 329,621 | 340 | 0.065 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 1,426,782 | 28.536 | 10 | 50 | MISS T_svc | 373,288 | 299 | 0.076 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 1,053,462 | 21.069 | 10 | 18 | MISS ceiling | 371,546 | 317 | 0.075 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 3,961,243 | 79.225 | 10 | 18 | MISS ceiling | 233,101 | 166 | 0.062 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 12,993 | 0.260 | 10 | 20 | fits | 74,625 | 35 (29) | 0.093 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 14,451 | 0.289 | 10 | 20 | fits | 76,175 | 41 (35) | 0.093 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 24,316 | 0.486 | 10 | 20 | fits | 80,108 | 41 (12) | 0.084 |
| set_name | `aecp_fanout.set_name.if0` | 336,371 | 6.727 | 10 | 24 | fits | 387,421 | 608 | 0.056 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 229,062 | 4.581 | 10 | 24 | fits | 259,211 | 317 | 0.068 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 221,025 | 4.420 | 10 | 24 | fits | 259,460 | 299 | 0.065 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 221,408 | 4.428 | 10 | 24 | fits | 259,857 | 300 | 0.065 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 244,386 | 4.888 | 10 | 24 | fits | 284,289 | 351 | 0.063 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 244,812 | 4.896 | 10 | 24 | fits | 284,696 | 351 | 0.063 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 249,487 | 4.990 | 10 | 24 | fits | 290,788 | 351 | 0.063 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 249,843 | 4.997 | 10 | 24 | fits | 291,125 | 350 | 0.063 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 226,094 | 4.522 | 10 | 24 | fits | 255,258 | 316 | 0.069 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 248,608 | 4.972 | 10 | 24 | fits | 276,461 | 299 | 0.066 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 330,831 | 6.617 | 10 | 24 | fits | 368,895 | 655 | 0.055 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 232,224 | 4.644 | 10 | 24 | fits | 270,651 | 351 | 0.062 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 232,003 | 4.640 | 10 | 24 | fits | 270,398 | 351 | 0.062 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 434,772 | 8.695 | 10 | 24 | fits | 232,696 | 478 | 0.072 |
| BIND_RX | `acmp.bind_rx.if0` | 48,633 | 0.973 | 10 | 20 | fits | 122,725 | 82 (77) | 0.085 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 14,525 | 0.290 | 10 | 20 | fits | 82,348 | 38 (32) | 0.093 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 29,281 | 0.586 | 10 | 20 | fits | 89,628 | 53 (47) | 0.083 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 48,496 | 0.970 | 10 | 20 | fits | 119,765 | 62 (50) | 0.096 |
| PROBE_TX | `acmp.probe_tx.if0` | 30,432 | 0.609 | 10 | 20 | fits | 87,732 | 55 (48) | 0.084 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 30,449 | 0.609 | 10 | 20 | fits | 87,360 | 54 (48) | 0.083 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 28,981 | 0.580 | 10 | 20 | fits | 85,875 | 54 (48) | 0.083 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 28,880 | 0.578 | 10 | 20 | fits | 85,774 | 54 (48) | 0.083 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
