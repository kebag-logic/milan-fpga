### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 43 paths and 0 of 44 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.134 (0.448) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.156 (0.480) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.184 (0.504) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.217 (0.541) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.159 (0.489) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.246 (0.618) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.215 (0.527) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.255 (0.585) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.159 (0.483) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.155 (0.478) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.199 (0.526) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.179 (0.502) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.187 (0.513) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.199 (0.525) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.199 (0.528) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.153 (0.477) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.203 (0.530) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.155 (0.479) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.161 (0.486) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.164 (0.491) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.203 (0.529) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.130 (0.454) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.281 (0.711) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.188 (0.512) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.206 (0.590) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.551 (2.877) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 3.360 (3.695) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 0.922 (1.139) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.511 (0.809) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.569 (0.894) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 3.206 (3.541) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.484 (0.857) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 0.612 (0.948) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.541 (0.837) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.574 (0.916) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.304 (3.627) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 3.002 (3.325) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.457 (0.758) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 3.194 (3.531) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.008 (2.384) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.795 (4.160) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 2.946 (3.312) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.402 (1.743) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp-fanout | 121 | 0 | 69,138 (0.691) | fits |
| aecp | 112 | 0 | 45,223 (0.452) | fits |
| aecp-largest-notice | 106 | 0 | 151,331 (1.513) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp-fanout | 84 | 24,018 (0.240) | 4,326 (0.043) |
| aecp | 79 | 22,048 (0.220) | 2,351 (0.024) |
| aecp-largest-notice | 78 | 22,048 (0.220) | 2,351 (0.024) |

Longest pass that carries a step: 24,018 CPU cycles (0.240 ms), aecp-fanout; longest step: 4,326 (0.043 ms), aecp-fanout.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 57,416 | 0.574 | 20 | 24 | fits | 68,167 | 95 | 0.599 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 48,435 | 0.484 | 20 | 24 | fits | 56,509 | 78 | 0.600 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 54,063 | 0.541 | 20 | 24 | fits | 55,422 | 79 | 0.581 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 46,326 | 0.463 | 20 | 24 | fits | 51,988 | 78 | 0.573 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 56,887 | 0.569 | 20 | 24 | fits | 61,191 | 66 | 0.641 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 255,144 | 2.551 | 20 | 24 | fits | 59,175 | 65 | 0.641 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 320,628 | 3.206 | 20 | 24 | fits | 63,337 | 66 | 0.652 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 336,008 | 3.360 | 20 | 24 | fits | 61,251 | 65 | 0.647 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 330,410 | 3.304 | 20 | 24 | fits | 59,403 | 73 | 0.607 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 61,243 | 0.612 | 20 | 24 | fits | 69,138 | 77 | 0.623 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 300,208 | 3.002 | 20 | 24 | fits | 60,254 | 78 | 0.609 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 51,138 | 0.511 | 20 | 24 | fits | 52,583 | 78 | 0.582 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 45,730 | 0.457 | 20 | 24 | fits | 50,997 | 79 | 0.559 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 92,172 | 0.922 | 20 | 24 | fits | 44,552 | 59 | 0.553 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 12,987 | 0.130 | 20 | 24 | fits | 28,543 | 20 | 0.789 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 25,541 | 0.255 | 20 | 24 | fits | 32,559 | 20 | 0.724 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 15,928 | 0.159 | 20 | 24 | fits | 27,628 | 20 | 0.737 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 19,867 | 0.199 | 20 | 24 | fits | 27,726 | 20 | 0.739 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 16,137 | 0.161 | 20 | 24 | fits | 27,963 | 20 | 0.734 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 16,371 | 0.164 | 20 | 24 | fits | 27,963 | 20 | 0.739 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 20,301 | 0.203 | 20 | 24 | fits | 27,060 | 20 | 0.740 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 15,527 | 0.155 | 20 | 24 | fits | 27,195 | 20 | 0.751 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 19,920 | 0.199 | 20 | 24 | fits | 26,559 | 20 | 0.751 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 17,925 | 0.179 | 20 | 24 | fits | 29,547 | 21 | 0.654 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 18,677 | 0.187 | 20 | 24 | fits | 26,321 | 20 | 0.771 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 19,868 | 0.199 | 20 | 24 | fits | 26,574 | 20 | 0.770 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 15,330 | 0.153 | 20 | 24 | fits | 26,952 | 20 | 0.738 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 20,299 | 0.203 | 20 | 24 | fits | 27,814 | 20 | 0.744 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 15,464 | 0.155 | 20 | 24 | fits | 27,295 | 20 | 0.751 |
| get_configuration | `aecp.get_configuration.if0` | 18,361 | 0.184 | 20 | 24 | fits | 24,600 | 20 | 0.752 |
| entity_available | `aecp.entity_available.if0` | 13,387 | 0.134 | 20 | 24 | fits | 24,225 | 20 | 0.729 |
| get_name | `aecp.get_name.if0` | 15,890 | 0.159 | 20 | 24 | fits | 27,528 | 20 | 0.754 |
| get_counters | `aecp.get_counters.if0` | 21,741 | 0.217 | 20 | 24 | fits | 28,527 | 20 | 0.739 |
| get_avb_info | `aecp.get_avb_info.if0` | 15,621 | 0.156 | 20 | 24 | fits | 27,284 | 20 | 0.778 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 18,826 | 0.188 | 20 | 24 | fits | 25,305 | 20 | 0.763 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 21,537 | 0.215 | 20 | 24 | fits | 24,579 | 20 | 0.742 |
| set_name | `aecp.set_name.if0` | 28,088 | 0.281 | 20 | 24 | fits | 45,223 | 43 | 0.772 |
| lock_entity | `aecp.lock_entity.if0` | 24,601 | 0.246 | 20 | 24 | fits | 35,946 | 34 | 0.784 |
| unlock_entity | `aecp.unlock_entity.if0` | 20,565 | 0.206 | 20 | 24 | fits | 37,051 | 33 | 0.785 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 140,187 | 1.402 | 20 | 24 | fits | 151,331 | 98 | 0.344 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 319,436 | 3.194 | 20 | 24 | fits | 136,532 | 70 | 0.294 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 200,814 | 2.008 | 20 | 24 | fits | 41,426 | 17 | 0.683 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 379,469 | 3.795 | 20 | 24 | fits | 91,516 | 18 | 0.653 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 294,648 | 2.946 | 20 | 24 | fits | 93,518 | 17 | 0.668 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
