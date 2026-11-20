### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 18 paths and 0 of 19 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.937 (3.245) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 3.357 (3.667) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 0.764 (0.960) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.378 (0.631) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.511 (0.799) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 3.352 (3.668) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.386 (0.506) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 0.528 (0.803) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.384 (0.642) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.416 (0.563) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.190 (3.500) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 3.429 (3.711) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.360 (0.643) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 3.069 (3.361) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.517 (2.849) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.624 (3.951) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.391 (3.709) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.205 (1.360) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp-fanout | 120 | 0 | 67,062 (0.671) | fits |
| aecp-largest-notice | 106 | 0 | 135,999 (1.360) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp-fanout | 84 | 21,590 (0.216) | 2,713 (0.027) |
| aecp-largest-notice | 78 | 21,590 (0.216) | 2,682 (0.027) |

Longest pass that carries a step: 21,590 CPU cycles (0.216 ms), aecp-fanout; longest step: 2,713 (0.027 ms), aecp-fanout.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 41,555 | 0.416 | 20 | 24 | fits | 56,256 | 88 | 0.551 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 38,579 | 0.386 | 20 | 24 | fits | 50,611 | 77 | 0.583 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 38,429 | 0.384 | 20 | 24 | fits | 45,808 | 78 | 0.540 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 34,599 | 0.346 | 20 | 24 | fits | 44,585 | 78 | 0.508 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 51,122 | 0.511 | 20 | 24 | fits | 61,946 | 110 | 0.582 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 293,656 | 2.937 | 20 | 24 | fits | 67,062 | 124 | 0.589 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 335,240 | 3.352 | 20 | 24 | fits | 63,865 | 110 | 0.589 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 335,715 | 3.357 | 20 | 24 | fits | 66,849 | 116 | 0.594 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 318,990 | 3.190 | 20 | 24 | fits | 48,742 | 67 | 0.583 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 52,847 | 0.528 | 20 | 24 | fits | 61,737 | 76 | 0.604 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 342,923 | 3.429 | 20 | 24 | fits | 55,984 | 78 | 0.591 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 37,799 | 0.378 | 20 | 24 | fits | 46,822 | 77 | 0.543 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 35,983 | 0.360 | 20 | 24 | fits | 45,187 | 79 | 0.515 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 76,391 | 0.764 | 20 | 24 | fits | 39,105 | 59 | 0.507 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 120,487 | 1.205 | 20 | 24 | fits | 135,999 | 136 | 0.307 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 306,935 | 3.069 | 20 | 24 | fits | 128,119 | 113 | 0.290 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 251,745 | 2.517 | 20 | 24 | fits | 44,551 | 18 | 0.652 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 362,403 | 3.624 | 20 | 24 | fits | 81,201 | 17 | 0.663 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 339,073 | 3.391 | 20 | 24 | fits | 82,436 | 17 | 0.663 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
