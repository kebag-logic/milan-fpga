### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 42 paths and 0 of 43 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.101 (0.447) | fits | 0 aecp | 1 | 0 |
| get_as_path | 0 | `aecp.get_as_path.if0` (aecp) | 0.256 (0.598) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.256 (0.607) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.231 (0.579) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.149 (0.507) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.253 (0.604) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.278 (0.717) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.224 (0.570) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.162 (0.516) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.255 (0.607) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.246 (0.596) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.124 (0.476) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.334 (0.693) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.249 (0.613) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.120 (0.472) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.124 (0.475) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.247 (0.598) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.130 (0.482) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.252 (0.604) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.128 (0.482) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.255 (0.607) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.123 (0.475) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.223 (0.570) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.191 (0.649) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.113 (0.464) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.176 (0.568) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 2.409 (2.757) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 0.829 (0.861) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.367 (0.477) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 0.577 (0.730) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.390 (0.525) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 0.819 (1.140) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.409 (0.719) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.448 (0.808) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.157 (3.489) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 2.793 (3.163) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.406 (0.717) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 2.450 (2.824) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 1.640 (2.100) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.030 (3.445) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.783 (4.206) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.966 (2.335) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp-fanout | 119 | 0 | 93,185 (0.932) | fits |
| aecp | 113 | 0 | 45,528 (0.455) | fits |
| aecp-largest-notice | 106 | 2 | 211,441 (2.114) | OVER the share |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp-fanout | 82 | 25,282 (0.253) | 2,722 (0.027) |
| aecp | 80 | 25,282 (0.253) | 2,722 (0.027) |
| aecp-largest-notice | 78 | 25,282 (0.253) | 2,722 (0.027) |

Longest pass that carries a step: 25,282 CPU cycles (0.253 ms), aecp-fanout; longest step: 2,722 (0.027 ms), aecp-fanout.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 44,804 | 0.448 | 20 | 24 | fits | 58,268 | 88 | 0.554 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 39,000 | 0.390 | 20 | 24 | fits | 52,486 | 77 | 0.582 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 40,936 | 0.409 | 20 | 24 | fits | 47,850 | 78 | 0.552 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 38,411 | 0.384 | 20 | 24 | fits | 47,591 | 77 | 0.542 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 57,714 | 0.577 | 20 | 24 | fits | 72,963 | 110 | 0.592 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 240,909 | 2.409 | 20 | 24 | fits | 70,409 | 109 | 0.595 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 315,695 | 3.157 | 20 | 24 | fits | 51,707 | 67 | 0.596 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 81,893 | 0.819 | 20 | 24 | fits | 93,185 | 76 | 0.611 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 279,255 | 2.793 | 20 | 24 | fits | 56,758 | 78 | 0.597 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 36,704 | 0.367 | 20 | 24 | fits | 47,714 | 77 | 0.548 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 40,590 | 0.406 | 20 | 24 | fits | 47,528 | 78 | 0.540 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 82,895 | 0.829 | 20 | 24 | fits | 41,525 | 59 | 0.511 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 22,289 | 0.223 | 20 | 24 | fits | 28,268 | 20 | 0.750 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 16,176 | 0.162 | 20 | 24 | fits | 32,263 | 20 | 0.678 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 25,495 | 0.255 | 20 | 24 | fits | 28,301 | 20 | 0.701 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 12,375 | 0.124 | 20 | 24 | fits | 27,940 | 20 | 0.693 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 12,782 | 0.128 | 20 | 24 | fits | 28,607 | 20 | 0.691 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 25,542 | 0.255 | 20 | 24 | fits | 28,396 | 20 | 0.691 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 12,323 | 0.123 | 20 | 24 | fits | 27,888 | 20 | 0.697 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 24,569 | 0.246 | 20 | 24 | fits | 27,273 | 20 | 0.703 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 12,442 | 0.124 | 20 | 24 | fits | 27,999 | 20 | 0.717 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 33,409 | 0.334 | 20 | 24 | fits | 36,961 | 27 | 0.596 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 24,864 | 0.249 | 20 | 24 | fits | 27,710 | 20 | 0.733 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 12,036 | 0.120 | 20 | 24 | fits | 27,593 | 20 | 0.737 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 24,681 | 0.247 | 20 | 24 | fits | 27,464 | 20 | 0.694 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 12,975 | 0.130 | 20 | 24 | fits | 28,611 | 20 | 0.703 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 25,177 | 0.252 | 20 | 24 | fits | 28,031 | 20 | 0.695 |
| get_configuration | `aecp.get_configuration.if0` | 23,114 | 0.231 | 20 | 24 | fits | 25,612 | 20 | 0.716 |
| entity_available | `aecp.entity_available.if0` | 10,123 | 0.101 | 20 | 24 | fits | 25,426 | 20 | 0.702 |
| get_name | `aecp.get_name.if0` | 25,333 | 0.253 | 20 | 24 | fits | 28,300 | 20 | 0.728 |
| get_counters | `aecp.get_counters.if0` | 14,900 | 0.149 | 20 | 24 | fits | 30,673 | 20 | 0.724 |
| get_avb_info | `aecp.get_avb_info.if0` | 25,566 | 0.256 | 20 | 24 | fits | 28,514 | 20 | 0.761 |
| get_as_path | `aecp.get_as_path.if0` | 25,569 | 0.256 | 20 | 24 | fits | 34,124 | 100 | 0.527 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 11,288 | 0.113 | 20 | 24 | fits | 26,052 | 20 | 0.736 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 22,434 | 0.224 | 20 | 24 | fits | 24,850 | 20 | 0.691 |
| set_name | `aecp.set_name.if0` | 19,085 | 0.191 | 20 | 24 | fits | 45,528 | 43 | 0.748 |
| lock_entity | `aecp.lock_entity.if0` | 27,823 | 0.278 | 20 | 24 | fits | 34,192 | 33 | 0.752 |
| unlock_entity | `aecp.unlock_entity.if0` | 17,593 | 0.176 | 20 | 24 | fits | 34,871 | 32 | 0.773 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 196,615 | 1.966 | 20 | 24 | fits | 211,441 | 137 | 0.318 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 245,031 | 2.450 | 20 | 24 | fits | 207,929 | 118 | 0.316 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 164,004 | 1.640 | 20 | 24 | fits | 60,911 | 17 | 0.668 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 303,004 | 3.030 | 20 | 24 | fits | 101,719 | 18 | 0.665 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 378,256 | 3.783 | 20 | 24 | fits | 160,585 | 17 | 0.669 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
