### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 44 paths and 0 of 45 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.121 (0.407) | fits | 0 aecp | 1 | 0 |
| get_as_path | 0 | `aecp.get_as_path.if0` (aecp) | 0.239 (0.528) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.142 (0.430) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.161 (0.448) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.202 (0.489) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.185 (0.477) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.186 (0.517) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.095 (0.242) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.228 (0.521) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.143 (0.433) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.141 (0.430) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.177 (0.465) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.164 (0.451) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.175 (0.462) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.174 (0.461) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.181 (0.471) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.138 (0.426) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.187 (0.477) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.138 (0.428) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.187 (0.477) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.147 (0.437) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.184 (0.471) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.250 (0.535) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.229 (0.610) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.123 (0.410) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.234 (0.567) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.370 (2.537) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 2.273 (2.577) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 0.765 (0.814) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.548 (0.825) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.508 (0.787) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 2.502 (2.795) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.436 (0.551) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 0.581 (0.850) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.547 (0.811) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.484 (0.629) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 2.283 (2.556) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 2.332 (2.620) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.450 (0.702) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 1.840 (2.121) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 1.328 (1.659) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 2.922 (3.250) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 2.390 (2.723) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.306 (1.456) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp-fanout | 119 | 0 | 66,590 (0.666) | fits |
| aecp | 113 | 0 | 44,633 (0.446) | fits |
| aecp-largest-notice | 105 | 0 | 145,642 (1.456) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp-fanout | 83 | 21,154 (0.212) | 1,918 (0.019) |
| aecp | 80 | 21,154 (0.212) | 1,918 (0.019) |
| aecp-largest-notice | 78 | 21,154 (0.212) | 1,918 (0.019) |

Longest pass that carries a step: 21,154 CPU cycles (0.212 ms), aecp-fanout; longest step: 1,918 (0.019 ms), aecp-fanout.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 48,396 | 0.484 | 20 | 24 | fits | 62,944 | 89 | 0.581 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 43,609 | 0.436 | 20 | 24 | fits | 55,105 | 78 | 0.592 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 47,322 | 0.473 | 20 | 24 | fits | 53,637 | 79 | 0.560 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 54,716 | 0.547 | 20 | 24 | fits | 50,009 | 78 | 0.549 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 50,817 | 0.508 | 20 | 24 | fits | 59,390 | 66 | 0.625 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 236,978 | 2.370 | 20 | 24 | fits | 56,719 | 65 | 0.621 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 250,211 | 2.502 | 20 | 24 | fits | 66,169 | 72 | 0.631 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 227,319 | 2.273 | 20 | 24 | fits | 58,633 | 65 | 0.622 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 228,302 | 2.283 | 20 | 24 | fits | 52,887 | 67 | 0.596 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 58,140 | 0.581 | 20 | 24 | fits | 66,590 | 77 | 0.604 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 233,154 | 2.332 | 20 | 24 | fits | 64,243 | 84 | 0.601 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 54,776 | 0.548 | 20 | 24 | fits | 50,166 | 78 | 0.558 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 45,016 | 0.450 | 20 | 24 | fits | 50,612 | 79 | 0.555 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 76,538 | 0.765 | 20 | 24 | fits | 41,684 | 59 | 0.504 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 25,005 | 0.250 | 20 | 24 | fits | 26,973 | 20 | 0.783 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 22,846 | 0.228 | 20 | 24 | fits | 31,599 | 20 | 0.722 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 14,323 | 0.143 | 20 | 24 | fits | 26,844 | 20 | 0.737 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 18,111 | 0.181 | 20 | 24 | fits | 26,650 | 20 | 0.730 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 18,720 | 0.187 | 20 | 24 | fits | 27,424 | 20 | 0.737 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 14,696 | 0.147 | 20 | 24 | fits | 27,050 | 20 | 0.728 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 18,394 | 0.184 | 20 | 24 | fits | 26,265 | 20 | 0.733 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 14,093 | 0.141 | 20 | 24 | fits | 26,535 | 20 | 0.746 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 17,747 | 0.177 | 20 | 24 | fits | 25,892 | 20 | 0.747 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 16,351 | 0.164 | 20 | 24 | fits | 28,660 | 21 | 0.647 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 17,543 | 0.175 | 20 | 24 | fits | 25,521 | 20 | 0.765 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 17,417 | 0.174 | 20 | 24 | fits | 25,751 | 20 | 0.764 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 13,788 | 0.138 | 20 | 24 | fits | 26,185 | 20 | 0.732 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 18,667 | 0.187 | 20 | 24 | fits | 27,330 | 20 | 0.739 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 13,842 | 0.138 | 20 | 24 | fits | 26,275 | 20 | 0.744 |
| get_configuration | `aecp.get_configuration.if0` | 16,116 | 0.161 | 20 | 24 | fits | 24,406 | 20 | 0.764 |
| entity_available | `aecp.entity_available.if0` | 12,069 | 0.121 | 20 | 24 | fits | 24,313 | 20 | 0.750 |
| get_name | `aecp.get_name.if0` | 18,506 | 0.185 | 20 | 24 | fits | 27,269 | 20 | 0.768 |
| get_counters | `aecp.get_counters.if0` | 20,197 | 0.202 | 20 | 24 | fits | 28,471 | 20 | 0.751 |
| get_avb_info | `aecp.get_avb_info.if0` | 14,163 | 0.142 | 20 | 24 | fits | 26,394 | 20 | 0.777 |
| get_as_path | `aecp.get_as_path.if0` | 23,858 | 0.239 | 20 | 24 | fits | 32,143 | 99 | 0.558 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 12,338 | 0.123 | 20 | 24 | fits | 24,574 | 20 | 0.767 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 9,512 | 0.095 | 20 | 24 | fits | 24,175 | 20 | 0.755 |
| set_name | `aecp.set_name.if0` | 22,939 | 0.229 | 20 | 24 | fits | 44,633 | 44 | 0.761 |
| lock_entity | `aecp.lock_entity.if0` | 18,588 | 0.186 | 20 | 24 | fits | 35,374 | 33 | 0.783 |
| unlock_entity | `aecp.unlock_entity.if0` | 23,368 | 0.234 | 20 | 24 | fits | 36,484 | 33 | 0.788 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 130,571 | 1.306 | 20 | 24 | fits | 145,642 | 92 | 0.329 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 184,012 | 1.840 | 20 | 24 | fits | 137,438 | 70 | 0.302 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 132,804 | 1.328 | 20 | 24 | fits | 40,395 | 17 | 0.688 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 292,203 | 2.922 | 20 | 24 | fits | 91,484 | 18 | 0.667 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 239,014 | 2.390 | 20 | 24 | fits | 100,607 | 32 | 0.667 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
