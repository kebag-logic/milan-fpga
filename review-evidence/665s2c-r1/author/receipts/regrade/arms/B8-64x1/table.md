### 8x8

26 of 68 paths and 44 of 92 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.998 (4.215) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 1.423 (4.477) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.578 (3.464) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 0.994 (3.891) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.293 (4.563) | fits | 0 adp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 1.574 (4.563) | fits | 1 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.263 (4.501) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 1.514 (4.501) | fits | 1 adp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.584 (3.544) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 1.000 (3.976) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.991 (3.882) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 0.993 (3.889) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 1.020 (3.910) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 1.022 (3.918) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.605 (3.497) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 0.604 (3.502) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.293 (3.381) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 0.303 (3.395) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.560 (5.836) | fits | 0 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 2.461 (7.377) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.887 (5.890) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 0.742 (4.746) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 1.070 (7.406) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 0.499 (5.243) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 1.976 (6.705) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 2.129 (6.705) | fits | 1 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 2.238 (7.241) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 1.696 (5.822) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.285 (3.506) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 1.379 (6.593) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 1.110 (4.281) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 1.120 (4.296) | fits | 0 acmp | 1 | 0 |
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 9.993 (12.050) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings_output | 1 | `aecp_fanout.add_audio_mappings_output.if1` (aecp-fanout) | 9.939 (11.996) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 18.187 (21.831) | MISS T_svc | 0 acmp | 1 | 1 |
| BIND_RX -> GET_STREAM_INFO notice | 1 | `aecp_fanout.bind_rx_stream_info.if1` (aecp-fanout) | 18.162 (21.807) | MISS T_svc | 0 acmp | 1 | 1 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 9.695 (11.337) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 9.270 (10.912) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 11.947 (16.009) | MISS T_svc | 0 aecp | 1 | 1 |
| remove_audio_mappings_output | 1 | `aecp_fanout.remove_audio_mappings_output.if1` (aecp-fanout) | 11.500 (15.562) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 9.903 (13.382) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 9.166 (10.641) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 12.563 (15.997) | MISS T_svc | 0 aecp | 1 | 1 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 9.284 (10.924) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 10.448 (14.093) | MISS T_svc | 0 aecp | 2 | 1 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 13.248 (15.573) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 12.780 (14.940) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 8.958 (10.413) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 13.317 (15.166) | MISS T_svc | 0 aecp | 1 | 1 |
| set_stream_info | 1 | `aecp_fanout.set_stream_info.if1` (aecp-fanout) | 12.897 (14.746) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 9.255 (10.896) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 9.245 (10.886) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 58.128 (63.974) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 33.605 (43.294) | MISS ceiling | 7 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 14.487 (28.117) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 118.521 (124.187) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 371.605 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 14.023 | MISS T_svc | 0 acmp | 3 | 2 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 63.921 | MISS ceiling | 11 acmp | 3 | 3 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 14.066 | MISS T_svc | 0 adp | 3 | 2 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 43.241 | MISS T_svc | 7 adp | 1 | 1 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 47.431 | MISS T_svc | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 14.059 | MISS T_svc | 0 aecp | 3 | 2 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 142.077 | MISS ceiling | 15 aecp | 3 | 3 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 14.048 | MISS T_svc | 0 maap | 3 | 2 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 47.416 | MISS T_svc | 6 maap | 3 | 3 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 70.654 | MISS ceiling | 0 srp | 3 | 3 |
| SRP record released under the composed load, last | 1 | `backlog-owed.service.srp.last.if1` (backlog-owed) | 165.435 | MISS ceiling | 31 srp | 3 | 3 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 161.431 | 26 | 703,383 (14.068) | yes | - |
| backlog-adp | 170.795 | 24 | 638,638 (12.773) | yes | - |
| backlog-owed | 371.656 | 45 | 580,150 (11.603) | yes | - |

Composed maximum over 3 of 4 backlog windows, a partial figure (backlog-adp-refill not run): 703,383 CPU cycles (14.068 ms), backlog.
Over the windows that released their whole load only: 703,383 (14.068 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 111,882 | 2.238 | 10 | 20 | fits | 193,980 | 48 (14) | 0.045 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 84,825 | 1.696 | 10 | 20 | fits | 168,508 | 20 (14) | 0.046 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 53,485 | 1.070 | 10 | 20 | fits | 262,136 | 80 (35) | 0.043 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 24,955 | 0.499 | 10 | 20 | fits | 262,136 | 80 (35) | 0.043 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 98,797 | 1.976 | 10 | 20 | fits | 215,592 | 28 (14) | 0.039 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 106,474 | 2.129 | 10 | 20 | fits | 215,592 | 28 (14) | 0.039 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 14,265 | 0.285 | 10 | 20 | fits | 175,299 | 26 (14) | 0.046 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 68,964 | 1.379 | 10 | 20 | fits | 154,337 | 19 (14) | 0.040 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 27,984 | 0.560 | 10 | 20 | fits | 171,430 | 42 (35) | 0.041 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 123,048 | 2.461 | 10 | 20 | fits | 171,277 | 42 (35) | 0.041 |
| an event behind 15 others | `backlog.event.if0` | 724,346 | 14.487 | 10 | 200 | MISS T_svc | 702,485 | 375 | 0.044 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 2,906,381 | 58.128 | 10 | 20 | MISS ceiling | 413,387 | 217 | 0.040 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 703,279 | 14.066 | 10 | 200 | MISS T_svc | 703,383 | 392 | 0.043 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 2,371,526 | 47.431 | 10 | 200 | MISS T_svc | 447,340 | 285 | 0.040 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 701,150 | 14.023 | 10 | 20 | MISS T_svc | 703,383 | 392 | 0.043 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 3,196,035 | 63.921 | 10 | 20 | MISS ceiling | 413,387 | 217 | 0.040 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 702,942 | 14.059 | 10 | 24 | MISS T_svc | 703,383 | 392 | 0.043 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 6,195,661 | 123.913 | 10 | 24 | MISS ceiling | 292,872 | 144 | 0.050 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 702,422 | 14.048 | 10 | 50 | MISS T_svc | 703,383 | 392 | 0.043 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 2,370,778 | 47.416 | 10 | 50 | MISS T_svc | 447,340 | 285 | 0.040 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 3,532,704 | 70.654 | 10 | 18 | MISS ceiling | 335,211 | 169 | 0.054 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 7,636,798 | 152.736 | 10 | 18 | MISS ceiling | 151,137 | 48 | 0.055 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 1,680,259 | 33.605 | 10 | 20 | MISS ceiling | 532,550 | 311 | 0.039 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 482,296 | 9.646 | 10 | 200 | fits | 484,637 | 386 | 0.039 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,162,037 | 43.241 | 10 | 200 | MISS T_svc | 532,550 | 311 | 0.039 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 482,752 | 9.655 | 10 | 20 | fits | 484,637 | 386 | 0.039 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 3,127,275 | 62.545 | 10 | 20 | MISS ceiling | 382,141 | 142 | 0.047 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 484,545 | 9.691 | 10 | 24 | fits | 484,637 | 386 | 0.039 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 6,722,176 | 134.444 | 10 | 24 | MISS ceiling | 254,276 | 124 | 0.042 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 484,025 | 9.680 | 10 | 50 | fits | 484,637 | 386 | 0.039 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,163,875 | 43.277 | 10 | 50 | MISS T_svc | 532,550 | 311 | 0.039 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 1,631,292 | 32.626 | 10 | 18 | MISS ceiling | 638,638 | 386 | 0.050 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 7,974,680 | 159.494 | 10 | 18 | MISS ceiling | 193,519 | 48 | 0.059 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 5,926,055 | 118.521 | 10 | 20 | MISS ceiling | 421,922 | 191 | 0.051 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,580,268 | 371.605 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,580,230 | 371.605 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,580,193 | 371.604 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,580,155 | 371.603 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 514,144 | 10.283 | 10 | 200 | MISS T_svc | 477,042 | 344 | 0.038 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 1,929,724 | 38.594 | 10 | 200 | MISS T_svc | 446,748 | 261 | 0.039 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 512,015 | 10.240 | 10 | 20 | MISS T_svc | 477,042 | 344 | 0.038 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 2,659,258 | 53.185 | 10 | 20 | MISS ceiling | 363,243 | 101 | 0.051 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 513,807 | 10.276 | 10 | 24 | MISS T_svc | 477,042 | 344 | 0.038 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 7,103,872 | 142.077 | 10 | 24 | MISS ceiling | 369,022 | 169 | 0.054 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 513,287 | 10.266 | 10 | 50 | MISS T_svc | 477,042 | 344 | 0.038 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 1,928,976 | 38.580 | 10 | 50 | MISS T_svc | 446,748 | 261 | 0.039 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 2,660,716 | 53.214 | 10 | 18 | MISS ceiling | 363,243 | 101 | 0.051 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 8,271,742 | 165.435 | 10 | 18 | MISS ceiling | 179,931 | 36 | 0.058 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 13,135 | 0.263 | 10 | 20 | fits | 225,033 | 60 (29) | 0.034 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 75,720 | 1.514 | 10 | 20 | fits | 225,033 | 60 (29) | 0.034 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 14,658 | 0.293 | 10 | 20 | fits | 228,133 | 71 (35) | 0.035 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 78,725 | 1.574 | 10 | 20 | fits | 228,133 | 71 (35) | 0.035 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 44,348 | 0.887 | 10 | 20 | fits | 173,463 | 42 (12) | 0.041 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 37,093 | 0.742 | 10 | 20 | fits | 237,309 | 32 (12) | 0.043 |
| set_name | `aecp_fanout.set_name.if0` | 662,410 | 13.248 | 10 | 24 | MISS T_svc | 778,667 | 1137 | 0.121 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 495,132 | 9.903 | 10 | 24 | fits | 530,574 | 590 | 0.169 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 464,203 | 9.284 | 10 | 24 | fits | 546,213 | 563 | 0.166 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 442,345 | 8.847 | 10 | 24 | fits | 524,335 | 556 | 0.168 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 597,367 | 11.947 | 10 | 24 | MISS T_svc | 623,338 | 662 | 0.146 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 499,642 | 9.993 | 10 | 24 | fits | 602,515 | 655 | 0.147 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 447,901 | 8.958 | 10 | 24 | fits | 520,670 | 589 | 0.172 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 628,171 | 12.563 | 10 | 24 | MISS T_svc | 630,863 | 556 | 0.139 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 665,844 | 13.317 | 10 | 24 | MISS T_svc | 758,293 | 1239 | 0.128 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 484,744 | 9.695 | 10 | 24 | fits | 566,863 | 662 | 0.163 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 462,758 | 9.255 | 10 | 24 | fits | 544,806 | 655 | 0.165 |
| set_name | `aecp_fanout.set_name.if1` | 639,005 | 12.780 | 10 | 24 | MISS T_svc | 746,983 | 1130 | 0.121 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 458,304 | 9.166 | 10 | 24 | fits | 532,064 | 589 | 0.170 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 445,675 | 8.914 | 10 | 24 | fits | 527,685 | 556 | 0.171 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 522,397 | 10.448 | 10 | 24 | MISS T_svc | 526,485 | 556 | 0.170 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if1` | 574,994 | 11.500 | 10 | 24 | MISS T_svc | 599,928 | 655 | 0.147 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if1` | 496,932 | 9.939 | 10 | 24 | fits | 599,785 | 655 | 0.146 |
| set_stream_info | `aecp_fanout.set_stream_info.if1` | 644,841 | 12.897 | 10 | 24 | MISS T_svc | 737,290 | 1232 | 0.129 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 463,493 | 9.270 | 10 | 24 | fits | 545,612 | 655 | 0.166 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 462,272 | 9.245 | 10 | 24 | fits | 544,320 | 655 | 0.165 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 909,352 | 18.187 | 10 | 24 | MISS T_svc | 525,168 | 937 | 0.167 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if1` | 908,088 | 18.162 | 10 | 24 | MISS T_svc | 528,536 | 937 | 0.169 |
| BIND_RX | `acmp.bind_rx.if0` | 49,886 | 0.998 | 10 | 20 | fits | 210,727 | 83 (77) | 0.044 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 14,663 | 0.293 | 10 | 20 | fits | 169,042 | 38 (32) | 0.042 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 29,186 | 0.584 | 10 | 20 | fits | 177,182 | 53 (47) | 0.037 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 55,519 | 1.110 | 10 | 20 | fits | 214,070 | 63 (50) | 0.049 |
| PROBE_TX | `acmp.probe_tx.if0` | 30,232 | 0.605 | 10 | 20 | fits | 174,843 | 55 (48) | 0.037 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 51,017 | 1.020 | 10 | 20 | fits | 195,518 | 61 (48) | 0.043 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 28,902 | 0.578 | 10 | 20 | fits | 173,205 | 54 (48) | 0.037 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 49,563 | 0.991 | 10 | 20 | fits | 194,094 | 61 (48) | 0.043 |
| BIND_RX | `acmp.bind_rx.if1` | 71,160 | 1.423 | 10 | 20 | fits | 223,871 | 91 (77) | 0.046 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 15,164 | 0.303 | 10 | 20 | fits | 169,769 | 40 (32) | 0.043 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 49,981 | 1.000 | 10 | 20 | fits | 198,778 | 61 (47) | 0.044 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 56,005 | 1.120 | 10 | 20 | fits | 214,794 | 64 (50) | 0.049 |
| PROBE_TX | `acmp.probe_tx.if1` | 30,201 | 0.604 | 10 | 20 | fits | 175,102 | 56 (48) | 0.037 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 51,088 | 1.022 | 10 | 20 | fits | 195,879 | 62 (48) | 0.043 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 49,708 | 0.994 | 10 | 20 | fits | 194,529 | 62 (48) | 0.043 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 49,642 | 0.993 | 10 | 20 | fits | 194,463 | 62 (48) | 0.043 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
