### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 20 paths and 0 of 22 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 2.985 (3.448) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings_output | 1 | `aecp_fanout.add_audio_mappings_output.if1` (aecp-fanout) | 2.461 (2.829) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 2.013 (2.089) | fits | 0 acmp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 1 | `aecp_fanout.bind_rx_stream_info.if1` (aecp-fanout) | 1.184 (1.538) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.660 (1.084) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 0.615 (1.045) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 0.876 (1.341) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 1 | `aecp_fanout.remove_audio_mappings_output.if1` (aecp-fanout) | 0.885 (1.348) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.682 (1.129) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 0.693 (1.141) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 1.028 (1.488) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.663 (1.088) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 0.650 (0.959) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.655 (1.131) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 0.618 (1.089) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 2.778 (3.230) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 1.442 (1.894) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 1 | `aecp_fanout.set_stream_info.if1` (aecp-fanout) | 2.836 (3.293) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.639 (0.942) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 0.666 (1.091) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp-fanout | 173 | 0 | 110,248 (1.102) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp-fanout | 101 | 73,449 (0.734) | 4,159 (0.042) |

Longest pass that carries a step: 73,449 CPU cycles (0.734 ms), aecp-fanout; longest step: 4,159 (0.042 ms), aecp-fanout.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 65,492 | 0.655 | 20 | 24 | fits | 75,537 | 160 | 0.395 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 68,180 | 0.682 | 20 | 24 | fits | 70,294 | 139 | 0.421 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 66,313 | 0.663 | 20 | 24 | fits | 66,089 | 139 | 0.383 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 60,060 | 0.601 | 20 | 24 | fits | 64,110 | 140 | 0.341 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 87,626 | 0.876 | 20 | 24 | fits | 91,599 | 160 | 0.462 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 298,515 | 2.985 | 20 | 24 | fits | 90,003 | 161 | 0.455 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 277,828 | 2.778 | 20 | 24 | fits | 67,613 | 116 | 0.421 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 102,835 | 1.028 | 20 | 24 | fits | 110,248 | 139 | 0.442 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 144,184 | 1.442 | 20 | 24 | fits | 73,128 | 128 | 0.439 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 66,020 | 0.660 | 20 | 24 | fits | 65,944 | 140 | 0.382 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 63,854 | 0.639 | 20 | 24 | fits | 64,923 | 140 | 0.356 |
| set_name | `aecp_fanout.set_name.if1` | 61,823 | 0.618 | 20 | 24 | fits | 68,874 | 117 | 0.364 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 69,281 | 0.693 | 20 | 24 | fits | 71,249 | 139 | 0.417 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 65,046 | 0.650 | 20 | 24 | fits | 66,503 | 139 | 0.372 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 61,147 | 0.611 | 20 | 24 | fits | 65,271 | 140 | 0.347 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if1` | 88,534 | 0.885 | 20 | 24 | fits | 92,279 | 160 | 0.459 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if1` | 246,082 | 2.461 | 20 | 24 | fits | 90,909 | 161 | 0.454 |
| set_stream_info | `aecp_fanout.set_stream_info.if1` | 283,643 | 2.836 | 20 | 24 | fits | 73,955 | 129 | 0.439 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 61,450 | 0.615 | 20 | 24 | fits | 66,000 | 140 | 0.364 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 66,567 | 0.666 | 20 | 24 | fits | 66,440 | 140 | 0.371 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 201,295 | 2.013 | 20 | 24 | fits | 73,449 | 113 | 0.472 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if1` | 118,364 | 1.184 | 20 | 24 | fits | 61,776 | 109 | 0.322 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
