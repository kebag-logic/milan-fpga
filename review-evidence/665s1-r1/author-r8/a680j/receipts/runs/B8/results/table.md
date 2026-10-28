### 8x8

20 of 20 paths and 22 of 22 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 14.351 (17.702) | MISS T_svc | 0 aecp | 1 | 1 |
| add_audio_mappings_output | 1 | `aecp_fanout.add_audio_mappings_output.if1` (aecp-fanout) | 31.412 (38.724) | MISS ceiling | 0 aecp | 1 | 1 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 28.976 (34.775) | MISS ceiling | 0 acmp | 1 | 1 |
| BIND_RX -> GET_STREAM_INFO notice | 1 | `aecp_fanout.bind_rx_stream_info.if1` (aecp-fanout) | 28.901 (34.702) | MISS ceiling | 0 acmp | 1 | 1 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 14.260 (20.436) | MISS T_svc | 0 aecp | 1 | 1 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 14.251 (21.167) | MISS T_svc | 0 aecp | 1 | 1 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 17.506 (21.639) | MISS T_svc | 0 aecp | 1 | 1 |
| remove_audio_mappings_output | 1 | `aecp_fanout.remove_audio_mappings_output.if1` (aecp-fanout) | 16.711 (23.266) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 16.351 (19.760) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 15.424 (20.553) | MISS T_svc | 0 aecp | 1 | 1 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 26.980 (32.475) | MISS ceiling | 0 aecp | 1 | 1 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 15.977 (21.768) | MISS T_svc | 0 aecp | 2 | 2 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 16.270 (19.657) | MISS T_svc | 0 aecp | 2 | 2 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 20.456 (28.574) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 22.693 (29.428) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 13.332 (19.571) | MISS T_svc | 0 aecp | 1 | 1 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 21.963 (29.283) | MISS T_svc | 0 aecp | 1 | 1 |
| set_stream_info | 1 | `aecp_fanout.set_stream_info.if1` (aecp-fanout) | 19.785 (22.786) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 17.080 (22.880) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 17.046 (22.847) | MISS T_svc | 0 aecp | 1 | 1 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 1,022,780 | 20.456 | 10 | 24 | MISS T_svc | 1,231,178 | 1172 | 0.881 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 817,561 | 16.351 | 10 | 24 | MISS T_svc | 790,356 | 613 | 0.876 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 798,831 | 15.977 | 10 | 24 | MISS T_svc | 821,254 | 587 | 0.878 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 774,415 | 15.488 | 10 | 24 | MISS T_svc | 782,838 | 580 | 0.877 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 875,281 | 17.506 | 10 | 24 | MISS T_svc | 884,573 | 657 | 0.876 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 717,565 | 14.351 | 10 | 24 | MISS T_svc | 885,077 | 657 | 0.876 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 666,587 | 13.332 | 10 | 24 | MISS T_svc | 743,769 | 592 | 0.878 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 1,349,014 | 26.980 | 10 | 24 | MISS ceiling | 1,426,162 | 643 | 0.863 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 1,098,169 | 21.963 | 10 | 24 | MISS T_svc | 1,139,836 | 1244 | 0.886 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 713,000 | 14.260 | 10 | 24 | MISS T_svc | 823,871 | 679 | 0.880 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 853,984 | 17.080 | 10 | 24 | MISS T_svc | 860,421 | 686 | 0.880 |
| set_name | `aecp_fanout.set_name.if1` | 1,134,630 | 22.693 | 10 | 24 | MISS T_svc | 1,187,955 | 1139 | 0.882 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 771,184 | 15.424 | 10 | 24 | MISS T_svc | 829,614 | 620 | 0.877 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 761,788 | 15.236 | 10 | 24 | MISS T_svc | 786,496 | 580 | 0.878 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 813,499 | 16.270 | 10 | 24 | MISS T_svc | 785,631 | 581 | 0.878 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if1` | 835,540 | 16.711 | 10 | 24 | MISS T_svc | 881,829 | 657 | 0.875 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if1` | 1,570,597 | 31.412 | 10 | 24 | MISS ceiling | 956,640 | 670 | 0.876 |
| set_stream_info | `aecp_fanout.set_stream_info.if1` | 989,248 | 19.785 | 10 | 24 | MISS T_svc | 1,139,289 | 1244 | 0.886 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 712,526 | 14.251 | 10 | 24 | MISS T_svc | 823,367 | 679 | 0.880 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 852,316 | 17.046 | 10 | 24 | MISS T_svc | 859,604 | 686 | 0.880 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 1,448,819 | 28.976 | 10 | 24 | MISS ceiling | 784,891 | 943 | 0.885 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if1` | 1,445,070 | 28.901 | 10 | 24 | MISS ceiling | 788,939 | 943 | 0.885 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
