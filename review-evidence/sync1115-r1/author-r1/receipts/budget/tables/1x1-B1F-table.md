### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 43 paths and 0 of 44 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.114 (0.406) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.141 (0.441) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.157 (0.449) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.198 (0.494) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.182 (0.479) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.171 (0.550) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.115 (0.409) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.227 (0.528) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.137 (0.436) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.137 (0.434) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.176 (0.472) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.159 (0.455) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.173 (0.468) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.174 (0.471) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.179 (0.476) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.135 (0.431) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.185 (0.484) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.136 (0.434) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.186 (0.483) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.142 (0.440) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.181 (0.476) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.245 (0.543) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.192 (0.441) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.160 (0.458) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.185 (0.524) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.396 (2.548) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 2.301 (2.608) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 0.781 (0.811) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.397 (0.492) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.517 (0.801) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 2.531 (2.833) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.428 (0.544) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 0.589 (0.865) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.480 (0.736) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.483 (0.624) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 2.286 (2.560) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 2.338 (2.633) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.443 (0.701) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 1.530 (1.816) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 1.483 (1.825) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 2.767 (3.105) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 2.544 (2.882) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.309 (1.454) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp-fanout | 120 | 0 | 66,942 (0.669) | fits |
| aecp | 112 | 0 | 44,075 (0.441) | fits |
| aecp-largest-notice | 107 | 0 | 145,438 (1.454) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp-fanout | 83 | 20,953 (0.210) | 1,946 (0.019) |
| aecp | 79 | 20,953 (0.210) | 1,946 (0.019) |
| aecp-largest-notice | 78 | 20,953 (0.210) | 1,946 (0.019) |

Longest pass that carries a step: 20,953 CPU cycles (0.210 ms), aecp-fanout; longest step: 1,946 (0.019 ms), aecp-fanout.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 48,286 | 0.483 | 20 | 24 | fits | 62,378 | 89 | 0.578 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 42,762 | 0.428 | 20 | 24 | fits | 54,423 | 78 | 0.590 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 47,958 | 0.480 | 20 | 24 | fits | 53,330 | 79 | 0.564 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 40,548 | 0.405 | 20 | 24 | fits | 49,967 | 78 | 0.552 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 51,670 | 0.517 | 20 | 24 | fits | 59,638 | 66 | 0.635 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 239,570 | 2.396 | 20 | 24 | fits | 57,551 | 65 | 0.629 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 253,075 | 2.531 | 20 | 24 | fits | 66,942 | 72 | 0.638 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 230,066 | 2.301 | 20 | 24 | fits | 59,178 | 65 | 0.631 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 228,551 | 2.286 | 20 | 24 | fits | 52,194 | 67 | 0.588 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 58,940 | 0.589 | 20 | 24 | fits | 66,535 | 77 | 0.609 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 233,755 | 2.338 | 20 | 24 | fits | 62,945 | 84 | 0.599 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 39,658 | 0.397 | 20 | 24 | fits | 49,178 | 78 | 0.551 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 44,348 | 0.443 | 20 | 24 | fits | 48,947 | 79 | 0.536 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 78,145 | 0.781 | 20 | 24 | fits | 40,960 | 59 | 0.494 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 24,541 | 0.245 | 20 | 24 | fits | 27,258 | 20 | 0.791 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 22,739 | 0.227 | 20 | 24 | fits | 31,503 | 20 | 0.730 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 13,715 | 0.137 | 20 | 24 | fits | 26,584 | 20 | 0.747 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 17,909 | 0.179 | 20 | 24 | fits | 26,516 | 20 | 0.743 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 18,592 | 0.186 | 20 | 24 | fits | 27,243 | 20 | 0.749 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 14,239 | 0.142 | 20 | 24 | fits | 27,000 | 20 | 0.742 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 18,067 | 0.181 | 20 | 24 | fits | 26,199 | 20 | 0.749 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 13,697 | 0.137 | 20 | 24 | fits | 26,458 | 20 | 0.758 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 17,555 | 0.176 | 20 | 24 | fits | 25,738 | 20 | 0.761 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 15,888 | 0.159 | 20 | 24 | fits | 28,525 | 21 | 0.665 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 17,312 | 0.173 | 20 | 24 | fits | 25,485 | 20 | 0.778 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 17,413 | 0.174 | 20 | 24 | fits | 25,794 | 20 | 0.778 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 13,475 | 0.135 | 20 | 24 | fits | 26,191 | 20 | 0.746 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 18,532 | 0.185 | 20 | 24 | fits | 27,264 | 20 | 0.753 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 13,594 | 0.136 | 20 | 24 | fits | 26,515 | 20 | 0.758 |
| get_configuration | `aecp.get_configuration.if0` | 15,732 | 0.157 | 20 | 24 | fits | 23,777 | 20 | 0.764 |
| entity_available | `aecp.entity_available.if0` | 11,449 | 0.114 | 20 | 24 | fits | 23,679 | 20 | 0.752 |
| get_name | `aecp.get_name.if0` | 18,180 | 0.182 | 20 | 24 | fits | 26,861 | 20 | 0.772 |
| get_counters | `aecp.get_counters.if0` | 19,822 | 0.198 | 20 | 24 | fits | 28,450 | 20 | 0.758 |
| get_avb_info | `aecp.get_avb_info.if0` | 14,115 | 0.141 | 20 | 24 | fits | 27,041 | 20 | 0.794 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 16,001 | 0.160 | 20 | 24 | fits | 24,708 | 20 | 0.779 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 11,502 | 0.115 | 20 | 24 | fits | 23,875 | 20 | 0.758 |
| set_name | `aecp.set_name.if0` | 19,206 | 0.192 | 20 | 24 | fits | 44,075 | 43 | 0.764 |
| lock_entity | `aecp.lock_entity.if0` | 17,127 | 0.171 | 20 | 24 | fits | 33,828 | 34 | 0.773 |
| unlock_entity | `aecp.unlock_entity.if0` | 18,534 | 0.185 | 20 | 24 | fits | 34,577 | 33 | 0.778 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 130,915 | 1.309 | 20 | 24 | fits | 145,438 | 92 | 0.334 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 153,011 | 1.530 | 20 | 24 | fits | 137,695 | 70 | 0.307 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 148,313 | 1.483 | 20 | 24 | fits | 40,757 | 17 | 0.698 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 276,710 | 2.767 | 20 | 24 | fits | 91,886 | 18 | 0.679 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 254,382 | 2.544 | 20 | 24 | fits | 94,339 | 17 | 0.693 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
