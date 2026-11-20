### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 18 paths and 0 of 19 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 3.147 (3.454) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 3.414 (3.721) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 0.850 (1.044) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.469 (0.625) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.601 (0.887) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 3.409 (3.723) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.497 (0.771) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 0.619 (0.890) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.477 (0.731) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.500 (0.795) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.250 (3.558) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 3.188 (3.467) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.454 (0.734) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 3.286 (3.575) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.435 (2.763) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.683 (4.006) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.452 (3.767) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.294 (1.594) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp-fanout | 121 | 0 | 66,717 (0.667) | fits |
| aecp-largest-notice | 107 | 0 | 135,215 (1.352) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp-fanout | 84 | 21,424 (0.214) | 2,524 (0.025) |
| aecp-largest-notice | 78 | 21,424 (0.214) | 2,524 (0.025) |

Longest pass that carries a step: 21,424 CPU cycles (0.214 ms), aecp-fanout; longest step: 2,524 (0.025 ms), aecp-fanout.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 50,048 | 0.500 | 20 | 24 | fits | 54,880 | 88 | 0.550 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 49,724 | 0.497 | 20 | 24 | fits | 49,932 | 77 | 0.584 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 47,740 | 0.477 | 20 | 24 | fits | 45,662 | 78 | 0.538 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 44,044 | 0.440 | 20 | 24 | fits | 44,485 | 78 | 0.506 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 60,130 | 0.601 | 20 | 24 | fits | 61,642 | 110 | 0.583 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 314,742 | 3.147 | 20 | 24 | fits | 66,717 | 124 | 0.589 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 340,929 | 3.409 | 20 | 24 | fits | 63,446 | 110 | 0.589 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 341,383 | 3.414 | 20 | 24 | fits | 66,360 | 116 | 0.594 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 325,028 | 3.250 | 20 | 24 | fits | 48,623 | 67 | 0.583 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 61,880 | 0.619 | 20 | 24 | fits | 61,388 | 76 | 0.604 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 318,817 | 3.188 | 20 | 24 | fits | 55,688 | 78 | 0.590 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 46,863 | 0.469 | 20 | 24 | fits | 46,425 | 77 | 0.543 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 45,439 | 0.454 | 20 | 24 | fits | 45,145 | 79 | 0.515 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 85,034 | 0.850 | 20 | 24 | fits | 38,709 | 59 | 0.507 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 129,410 | 1.294 | 20 | 24 | fits | 135,215 | 136 | 0.307 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 328,568 | 3.286 | 20 | 24 | fits | 127,797 | 113 | 0.291 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 243,545 | 2.435 | 20 | 24 | fits | 44,461 | 18 | 0.652 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 368,305 | 3.683 | 20 | 24 | fits | 81,093 | 17 | 0.663 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 345,195 | 3.452 | 20 | 24 | fits | 82,237 | 17 | 0.663 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
