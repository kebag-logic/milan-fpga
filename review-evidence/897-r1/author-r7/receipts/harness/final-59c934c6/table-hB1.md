### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 44 paths and 0 of 45 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.107 (0.414) | fits | 0 aecp | 1 | 0 |
| get_as_path | 0 | `aecp.get_as_path.if0` (aecp) | 0.232 (0.548) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.131 (0.447) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.158 (0.468) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.197 (0.511) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.177 (0.493) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.166 (0.540) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.152 (0.457) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.223 (0.542) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.135 (0.456) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.131 (0.449) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.173 (0.488) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.156 (0.473) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.169 (0.486) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.172 (0.488) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.181 (0.500) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.129 (0.447) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.181 (0.499) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.130 (0.451) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.138 (0.457) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.142 (0.459) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.180 (0.495) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.256 (0.568) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.202 (0.615) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.208 (0.515) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.227 (0.595) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.627 (2.941) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 3.398 (3.733) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 0.933 (1.137) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.510 (0.792) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.568 (0.883) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 3.415 (3.747) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.498 (0.819) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 0.606 (0.934) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.541 (0.821) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.526 (0.855) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.184 (3.509) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 3.225 (3.536) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.467 (0.758) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 2.445 (2.770) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.323 (2.682) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.665 (4.017) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.014 (3.366) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.357 (1.690) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp-fanout | 122 | 0 | 67,684 (0.677) | fits |
| aecp | 114 | 0 | 44,509 (0.445) | fits |
| aecp-largest-notice | 107 | 0 | 146,079 (1.461) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp-fanout | 84 | 22,118 (0.221) | 2,197 (0.022) |
| aecp | 80 | 22,118 (0.221) | 2,197 (0.022) |
| aecp-largest-notice | 78 | 22,118 (0.221) | 2,197 (0.022) |

Longest pass that carries a step: 22,118 CPU cycles (0.221 ms), aecp-fanout; longest step: 2,197 (0.022 ms), aecp-fanout.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 52,567 | 0.526 | 20 | 24 | fits | 62,145 | 89 | 0.556 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 49,791 | 0.498 | 20 | 24 | fits | 57,287 | 78 | 0.594 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 54,130 | 0.541 | 20 | 24 | fits | 54,713 | 79 | 0.544 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 46,752 | 0.468 | 20 | 24 | fits | 51,392 | 78 | 0.536 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 56,837 | 0.568 | 20 | 24 | fits | 61,061 | 66 | 0.630 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 262,686 | 2.627 | 20 | 24 | fits | 59,159 | 65 | 0.625 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 341,500 | 3.415 | 20 | 24 | fits | 63,053 | 66 | 0.637 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 339,778 | 3.398 | 20 | 24 | fits | 60,830 | 65 | 0.631 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 318,433 | 3.184 | 20 | 24 | fits | 60,127 | 73 | 0.605 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 60,616 | 0.606 | 20 | 24 | fits | 67,684 | 77 | 0.595 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 322,476 | 3.225 | 20 | 24 | fits | 60,076 | 78 | 0.591 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 51,010 | 0.510 | 20 | 24 | fits | 51,590 | 78 | 0.547 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 46,655 | 0.467 | 20 | 24 | fits | 50,388 | 79 | 0.529 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 93,328 | 0.933 | 20 | 24 | fits | 44,969 | 59 | 0.554 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 25,562 | 0.256 | 20 | 24 | fits | 28,440 | 20 | 0.785 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 22,255 | 0.223 | 20 | 24 | fits | 32,680 | 20 | 0.721 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 13,528 | 0.135 | 20 | 24 | fits | 28,117 | 20 | 0.732 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 18,144 | 0.181 | 20 | 24 | fits | 28,281 | 20 | 0.734 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 13,802 | 0.138 | 20 | 24 | fits | 28,354 | 20 | 0.731 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 14,214 | 0.142 | 20 | 24 | fits | 28,556 | 20 | 0.740 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 17,955 | 0.180 | 20 | 24 | fits | 27,542 | 20 | 0.737 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 13,078 | 0.131 | 20 | 24 | fits | 27,496 | 20 | 0.747 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 17,314 | 0.173 | 20 | 24 | fits | 27,067 | 20 | 0.750 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 15,567 | 0.156 | 20 | 24 | fits | 29,946 | 21 | 0.647 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 16,926 | 0.169 | 20 | 24 | fits | 26,906 | 20 | 0.771 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 17,191 | 0.172 | 20 | 24 | fits | 27,264 | 20 | 0.770 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 12,879 | 0.129 | 20 | 24 | fits | 27,279 | 20 | 0.732 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 18,110 | 0.181 | 20 | 24 | fits | 28,445 | 20 | 0.746 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 13,011 | 0.130 | 20 | 24 | fits | 27,668 | 20 | 0.746 |
| get_configuration | `aecp.get_configuration.if0` | 15,781 | 0.158 | 20 | 24 | fits | 25,154 | 20 | 0.750 |
| entity_available | `aecp.entity_available.if0` | 10,724 | 0.107 | 20 | 24 | fits | 24,390 | 20 | 0.723 |
| get_name | `aecp.get_name.if0` | 17,748 | 0.177 | 20 | 24 | fits | 27,920 | 20 | 0.754 |
| get_counters | `aecp.get_counters.if0` | 19,672 | 0.197 | 20 | 24 | fits | 29,335 | 20 | 0.744 |
| get_avb_info | `aecp.get_avb_info.if0` | 13,140 | 0.131 | 20 | 24 | fits | 27,717 | 20 | 0.783 |
| get_as_path | `aecp.get_as_path.if0` | 23,198 | 0.232 | 20 | 24 | fits | 33,016 | 101 | 0.541 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 20,835 | 0.208 | 20 | 24 | fits | 25,170 | 20 | 0.761 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 15,170 | 0.152 | 20 | 24 | fits | 24,430 | 20 | 0.738 |
| set_name | `aecp.set_name.if0` | 20,202 | 0.202 | 20 | 24 | fits | 44,509 | 44 | 0.750 |
| lock_entity | `aecp.lock_entity.if0` | 16,634 | 0.166 | 20 | 24 | fits | 36,139 | 33 | 0.778 |
| unlock_entity | `aecp.unlock_entity.if0` | 22,701 | 0.227 | 20 | 24 | fits | 37,053 | 33 | 0.772 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 135,736 | 1.357 | 20 | 24 | fits | 146,079 | 92 | 0.318 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 244,524 | 2.445 | 20 | 24 | fits | 138,259 | 70 | 0.294 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 232,347 | 2.323 | 20 | 24 | fits | 42,038 | 17 | 0.678 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 366,528 | 3.665 | 20 | 24 | fits | 92,296 | 18 | 0.656 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 301,405 | 3.014 | 20 | 24 | fits | 94,057 | 17 | 0.665 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
